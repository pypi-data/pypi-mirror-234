# Copyright 2021 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Synchronized BN for nn.DataParallel

Ref: https://github.com/chrisway613/Synchronized-BatchNormalization

"""
import threading
import time
import queue
import collections
import functools

import torch
import torch.nn.functional as F
from torch.nn.parallel._functions import ReduceAddCoalesced, Broadcast
from torch.nn import DataParallel, BatchNorm1d, BatchNorm2d, BatchNorm3d
from torch.nn.modules.batchnorm import _BatchNorm


__all__ = (
    'FutureResult',
    'sum_ft',
    'unsqueeze_ft',
    'DataParallelWithCallBack',
    'FutureResult',
    'SlavePipe',
    'SyncMaster'
    'patch_replication_callback',
    'convert_model'
    'SynchronizedBatchNorm1d',
    'SynchronizedBatchNorm2d',
    'SynchronizedBatchNorm3d',
)


class FutureResult:
  """A thread-safe future implementation. Used only as one-to-one pipe."""

  def __init__(self, wait_timeout=30.):
    self._wait_timeout = wait_timeout

    self._result = None
    self._lock = threading.Lock()
    self._cond = threading.Condition(self._lock)

  def put(self, result):
    with self._lock:
      assert self._result is None, 'Previous result has not been fetched!'
      self._result = result
      self._cond.notify()

  def get(self):
    with self._lock:
      if self._result is None:
        self._cond.wait(timeout=self._wait_timeout)

      res = self._result
      self._result = None

      return res


def sum_ft(tensor):
  """sum over the first and last dimension"""
  return tensor.sum(dim=0).sum(dim=-1)


def unsqueeze_ft(tensor):
  """add new dimensions at the front and the tail"""
  return tensor.unsqueeze(0).unsqueeze(-1)


class DataParallelContext:
  """
  Context data structure for data parallel.
  Multiple copies of a module on different devices share the same context,
  Thus with this context, different copies can share some information.
  """

  def __init__(self):
    self.sync_master = None


class DataParallelWithCallBack(DataParallel):
  """
      Data Parallel with a replication callback.

      An replication callback `__data_parallel_replicate__` of each module will be invoked after being created by
      original `replicate` function.
      The callback will be invoked with arguments `__data_parallel_replicate__(ctx, copy_id)`

      Examples:
          > sync_bn = SynchronizedBatchNorm1d(10, eps=1e-5, affine=False)
          > sync_bn = DataParallelWithCallback(sync_bn, device_ids=[0, 1])
          # sync_bn.sync_replicas will be invoked.
      """
  @classmethod
  def _callback(cls, replicas):
    master_copy = replicas[0]
    replicas_ctx = [DataParallelContext() for _ in master_copy.modules()]

    for copy_id, module_replicated in enumerate(replicas):
      for idx, m in enumerate(module_replicated.modules()):
        if 'SynchronizedBatchNorm' in type(m).__name__ and hasattr(m, '_sync_replicas'):
          m._sync_replicas(replicas_ctx[idx], copy_id)

  def __init__(self, module, device_ids=None, output_device=None, dim=0):
    """
    Initialization.
    :param module: module to be parallelized;
    :param device_ids: CUDA devices (default: all devices);
    :param output_device: device location of output (default: device_ids[0]);
    :param dim: dim of input data to be scattered & gathered.
    """
    super(DataParallelWithCallBack, self).__init__(
        module, device_ids, output_device, dim
    )

  def replicate(self, module, device_ids):
    """
    Replication with callback.
    :param module: (nn.Module) module to be parallelized;
    :param device_ids: (list of int or torch.device) CUDA devices (default: all devices);
    :return: module replicated on each device.
    """
    replicas = super(DataParallelWithCallBack, self).replicate(module, device_ids)
    self._callback(replicas)

    return replicas

  def forward(self, *inputs, **kwargs):
    """
    Note that this method will invoke the methods as below(in order):
    i). self.scatter;
    ii). self.replicate;
    iii). self.parallel_apply;
    iv). self.gather
    """
    return super(DataParallelWithCallBack, self).forward(*inputs, **kwargs)


_Registry = collections.namedtuple('_Registry', ('result',))
_SlavePipeBase = collections.namedtuple('_SlavePipeBase', ('identifier', 'queue', 'result'))


class SlavePipe(_SlavePipeBase):
  """Pipe for master <=> slave communication."""

  def run_slave(self, msg):
    # Put msg to the queue which shared with master & all other slave copies.
    self.queue.put((self.identifier, msg))
    # Get result from master
    ret = self.result.get()
    # Notify master that result is already got.
    self.queue.put(True)

    return ret


class SyncMaster:
  """An abstract `SyncMaster` object.
  - During the replication, as the data parallel will trigger an callback of each module, all slave devices should
  call `register(id)` and obtain an `SlavePipe` to communicate with the master.
  - During the forward pass, master device invokes `run_master`, all messages from slave devices will be collected,
  and passed to a registered callback.
  - After receiving the messages, the master device should gather the information and determine to message passed
  back to each slave devices.
  """

  def __init__(self, callback=None, sync_timeout=15.):
    """
    Args:
        callback: a callback method to be invoked after having collected messages from slave devices.
    """
    self._callback = callback
    self._sync_timeout = sync_timeout

    self._activated = False
    self._queue = queue.Queue()
    self._registry = collections.OrderedDict()

  @property
  def num_slaves(self):
    return len(self._registry)

  def register_slave(self, identifier):
    """
    Register an slave device.
    The 'future' data structure stores slave's results;
    The '_registry' attribute records the mapping relation between slave's copy id & results;
    Master & its all copies share the same queue.

    Args:
        identifier: an identifier, usually is the device id.

    Returns: a `SlavePipe` object which can be used to communicate with the master device.
    """
    if self._activated:
      # assert self._queue.empty(), 'Queue is not cleaned before next initialization!'
      self._queue.queue.clear()
      self._activated = False
      self._registry.clear()

    future = FutureResult(wait_timeout=2 * self._sync_timeout)
    self._registry[identifier] = _Registry(future)

    return SlavePipe(identifier, self._queue, future)

  def run_master(self, msg):
    """
    Main entry for the master device in each forward pass.
    The messages were first collected from each devices (including the master device), and then
    an callback will be invoked to compute the message to be sent back to each devices
    (including the master device).

    Note that if timeout occurred, this method will not be invoked.

    Args:
        msg: the message that the master want to send to itself. This will be placed as the first
        message when calling `master_callback`. For detailed usage, see `_SynchronizedBatchNorm` for an example.

    Returns: the message to be sent back to the master device.

    """
    self._activated = True

    intermediates = [(0, msg)]
    prev_time = time.time()
    # Until gather all slaves' msg or timeout occurred.
    while self._queue.qsize() != self.num_slaves:
      cur_time = time.time()
      time_used = cur_time - prev_time

      if time_used > self._sync_timeout:
        return None

    intermediates.extend([self._queue.get() for _ in range(self.num_slaves)])
    # print("intermediates: ", intermediates)
    results = self._callback(intermediates)
    # print(results)
    assert results[0][0] == 0, 'The first result should belongs to the master!'

    # results[0] belongs to master
    for i, res in results[1:]:
      # Return result to slave.
      self._registry[i].result.put(res)

    # Checkout whether slave has already got the result.
    for i in range(self.num_slaves):
      assert self._queue.get() is True

    # Return the result to master which belongs to itself.
    return results[0][1]


def convert_model(module):
  """
  Convert input module and its child recursively.
  :param module: the input module needs to be convert to SyncBN model;
  :return:
  Examples:
      >>> import torch.nn as nn
      >>> import torchvision
      >>> # m is a standard pytorch model
      >>> m = torchvision.models.resnet18(True)
      >>> m = nn.DataParallel(m)
      >>> # after convert, m is using SyncBN
      >>> m = convert_model(m)
  """

  def _convert(mod_old):
    if 'BatchNorm' not in type(mod_old).__name__:
      return mod_old

    mod_new = mod_old
    for pth_module, sync_module in zip(
            [BatchNorm1d,
             BatchNorm2d,
             BatchNorm3d],
            [SynchronizedBatchNorm1d,
             SynchronizedBatchNorm2d,
             SynchronizedBatchNorm3d]
    ):
      if isinstance(mod_old, pth_module):
        mod_new = sync_module(mod_old.num_features, mod_old.eps, mod_old.momentum, mod_old.affine)
        mod_new.running_mean = mod_old.running_mean
        mod_new.running_var = mod_old.running_var

        if mod_old.affine:
          mod_new.weight.data = mod_old.weight.data.clone().detach()
          mod_new.bias.data = mod_old.bias.data.clone().detach()

    return mod_new

  if isinstance(module, torch.nn.DataParallel):
    # Top model inside DataParallel.
    mod = module.module
    mod = convert_model(mod)
    mod = DataParallelWithCallBack(mod, device_ids=module.device_ids)

    return mod

  mod_cvt = _convert(module)
  for name, child in module.named_children():
    mod_cvt.add_module(name, _convert(child))

  return mod_cvt


def patch_replication_callback(data_parallel):
  """
  Monkey-patch an existing `DataParallel` object. Add the replication callback.
  Useful when you have customized `DataParallel` implementation.

  Examples:
      > sync_bn = SynchronizedBatchNorm1d(10, eps=1e-5, affine=False)
      > sync_bn = DataParallel(sync_bn, device_ids=[0, 1])
      > patch_replication_callback(sync_bn)
      # this is equivalent to
      > sync_bn = SynchronizedBatchNorm1d(10, eps=1e-5, affine=False)
      > sync_bn = DataParallelWithCallback(sync_bn, device_ids=[0, 1])
  """

  assert isinstance(data_parallel, DataParallel)
  old_replicate = data_parallel.replicate

  @functools.wraps(old_replicate)
  def new_replicate(module, device_ids):
    replicas = old_replicate(module, device_ids)
    # execute_replication_callbacks(modules)
    DataParallelWithCallBack._callback(replicas)

    return replicas

  data_parallel.replicate = new_replicate


_MessageToCollect = collections.namedtuple('_ChildMessage', ('sum', 'ssum', 'sum_size'))
_MessageToBroadcast = collections.namedtuple('_MasterMessage', ('mean', 'inv_std'))


class _SynchronizedBatchNorm(_BatchNorm):
  def __init__(self, num_features, eps=1e-5, momentum=0.1, affine=True, sync_timeout=15.):
    assert ReduceAddCoalesced is not None, 'Can not use Synchronized Batch Normalization without CUDA support.'

    super(_SynchronizedBatchNorm, self).__init__(num_features, eps=eps, momentum=momentum, affine=affine)

    self._is_parallel = False
    self._parallel_id = None

    self._sync_master = SyncMaster(callback=self._coalesce_and_compute, sync_timeout=sync_timeout)
    self._slave_pipe = None

  @property
  def _is_master(self):
    assert self._parallel_id is not None, "parallel replicate method should be executed first!"
    return self._parallel_id == 0

  def forward(self, inputs):
    # If it is not parallel computation or is in evaluation mode, use PyTorch's implementation.
    if not (self._is_parallel and self.training):
      return F.batch_norm(
          inputs, self.running_mean, self.running_var, self.weight, self.bias,
          self.training, self.momentum, self.eps
      )

    inputs_shape = inputs.shape
    # Reshape to (N, C, -1), whereas N is batch size, C is number of features/classes.
    inputs = inputs.reshape(inputs_shape[0], self.num_features, -1)
    # Compute the sum and square-sum.
    sum_size = inputs.size(0) * inputs.size(2)
    input_sum = sum_ft(inputs)
    input_ssum = sum_ft(inputs ** 2)
    # Master will collect message as below from all copies.
    msg = _MessageToCollect(input_sum, input_ssum, sum_size)
    # Reduce & broadcast the statistics.
    if self._is_master:
      # print("run master\n")
      result = self._sync_master.run_master(msg)

      # When timeout occurred during synchronizing with slaves,
      # the result will be None,
      # then use PyTorch's implementation.
      if result is None:
        return F.batch_norm(
            inputs, self.running_mean, self.running_var, self.weight, self.bias,
            self.training, self.momentum, self.eps
        )
      else:
        mean, inv_std = result
    else:
      # print("run slave\n")
      result_from_master = self._slave_pipe.run_slave(msg)

      # When timeout occurred during synchronizing with master,
      # the result from master will be None,
      # then use PyTorch's implementation.
      if result_from_master is None:
        return F.batch_norm(
            inputs, self.running_mean, self.running_var, self.weight, self.bias,
            self.training, self.momentum, self.eps
        )
      else:
        mean, inv_std = result_from_master

    # Compute the output.
    if self.affine:
      outputs = (inputs - unsqueeze_ft(mean)) * unsqueeze_ft(inv_std * self.weight) + unsqueeze_ft(self.bias)
    else:
      outputs = (inputs - unsqueeze_ft(mean)) * unsqueeze_ft(inv_std)

    # Reshape to original input shape
    return outputs.reshape(inputs_shape)

  def _sync_replicas(self, ctx, copy_id):
    """
    Synchronize all copies from a module.
    :param ctx: a context data structure for communication;
    :param copy_id: id of a copied module (usually the device id).
    :return:
    """
    self._is_parallel = True
    self._parallel_id = copy_id

    # parallel_id == 0 means master device
    if self._parallel_id == 0:
      ctx.sync_master = self._sync_master
    else:
      self._slave_pipe = ctx.sync_master.register_slave(copy_id)

  def _coalesce_and_compute(self, intermediates):
    """Reduce the sum and square-sum, compute the statistics, and broadcast it."""

    # Ensure that master being the first one.
    intermediates = sorted(intermediates, key=lambda i: i[0])

    # Get sum & square sum of from every device.
    to_reduce = [i[1][:2] for i in intermediates]
    # Flatten
    to_reduce = [j for i in to_reduce for j in i]
    # Size of data from every device.
    sum_size = sum([i[1].sum_size for i in intermediates])
    # Device of every copies
    target_gpus = [i[1].sum.get_device() for i in intermediates]
    # print("target gpus: ", target_gpus)

    # Add all sum & square sum individually from every copies,
    # and put the result to the master device.
    # 2 means that has 2 types input data.
    sum_, ssum = ReduceAddCoalesced.apply(target_gpus[0], 2, *to_reduce)
    mean, inv_std = self._compute_mean_std(sum_, ssum, sum_size)
    # Copied results for every device that to broadcasted.
    broadcasted = Broadcast.apply(target_gpus, mean, inv_std)
    # print("broadcasted: ", broadcasted)

    outputs = []
    for i, rec in enumerate(intermediates):
      outputs.append((rec[0], _MessageToBroadcast(*broadcasted[i * 2:i * 2 + 2])))

    # print("outputs: ", outputs)
    return outputs

  def _compute_mean_std(self, sum_, ssum, size):
    """
    Compute the mean and standard-deviation with sum and square-sum. This method
    also maintains the moving average on the master device.
    """
    assert size > 1, 'BatchNorm computes unbiased standard-deviation, which requires size > 1!'

    def _compute():
      self.running_mean = (1 - self.momentum) * self.running_mean + self.momentum * mean.data
      self.running_var = (1 - self.momentum) * self.running_var + self.momentum * unbias_var.data

    mean = sum_ / size
    sum_var = ssum - sum_ * mean
    unbias_var = sum_var / (size - 1)
    bias_var = sum_var / size

    if hasattr(torch, 'no_grad'):
      with torch.no_grad():
        _compute()
    else:
      _compute()

    return mean, bias_var.clamp(self.eps) ** -.5


class SynchronizedBatchNorm1d(_SynchronizedBatchNorm):
  r"""Applies Synchronized Batch Normalization over a 2d or 3d input that is seen as a
  mini-batch.

  .. math::

      y = \frac{x - mean[x]}{ \sqrt{Var[x] + \epsilon}} * gamma + beta

  This module differs from the built-in PyTorch BatchNorm1d as the mean and
  standard-deviation are reduced across all devices during training.

  For example, when one uses `nn.DataParallel` to wrap the network during
  training, PyTorch's implementation normalize the tensor on each device using
  the statistics only on that device, which accelerated the computation and
  is also easy to implement, but the statistics might be inaccurate.
  Instead, in this synchronized version, the statistics will be computed
  over all training samples distributed on multiple devices.

  Note that, for one-GPU or CPU-only case, this module behaves exactly same
  as the built-in PyTorch implementation.

  The mean and standard-deviation are calculated per-dimension over
  the mini-batches and gamma and beta are learnable parameter vectors
  of size C (where C is the input size).

  During training, this layer keeps a running estimate of its computed mean
  and variance. The running sum is kept with a default momentum of 0.1.

  During evaluation, this running mean/variance is used for normalization.

  Because the BatchNorm is done over the `C` dimension, computing statistics
  on `(N, L)` slices, it's common terminology to call this Temporal BatchNorm

  Args:
      num_features: num_features from an expected input of size
          `batch_size x num_features [x width]`
      eps: a value added to the denominator for numerical stability.
          Default: 1e-5
      momentum: the value used for the running_mean and running_var
          computation. Default: 0.1
      affine: a boolean value that when set to ``True``, gives the layer learnable
          affine parameters. Default: ``True``

  Shape::
      - Input: :math:`(N, C)` or :math:`(N, C, L)`
      - Output: :math:`(N, C)` or :math:`(N, C, L)` (same shape as input)

  Examples:
      >>> # With Learnable Parameters
      >>> m = SynchronizedBatchNorm1d(100)
      >>> # Without Learnable Parameters
      >>> m = SynchronizedBatchNorm1d(100, affine=False)
      >>> inputs = torch.autograd.Variable(torch.randn(20, 100))
      >>> output = m(inputs)
  """

  def _check_input_dim(self, input):
    if input.dim() != 2 and input.dim() != 3:
      raise ValueError(
          'expected 2D or 3D input (got {}D input)'.format(input.dim())
      )


class SynchronizedBatchNorm2d(_SynchronizedBatchNorm):
  r"""Applies Batch Normalization over a 4d input that is seen as a mini-batch
  of 3d inputs

  .. math::

      y = \frac{x - mean[x]}{ \sqrt{Var[x] + \epsilon}} * gamma + beta

  This module differs from the built-in PyTorch BatchNorm2d as the mean and
  standard-deviation are reduced across all devices during training.

  For example, when one uses `nn.DataParallel` to wrap the network during
  training, PyTorch's implementation normalize the tensor on each device using
  the statistics only on that device, which accelerated the computation and
  is also easy to implement, but the statistics might be inaccurate.
  Instead, in this synchronized version, the statistics will be computed
  over all training samples distributed on multiple devices.

  Note that, for one-GPU or CPU-only case, this module behaves exactly same
  as the built-in PyTorch implementation.

  The mean and standard-deviation are calculated per-dimension over
  the mini-batches and gamma and beta are learnable parameter vectors
  of size C (where C is the input size).

  During training, this layer keeps a running estimate of its computed mean
  and variance. The running sum is kept with a default momentum of 0.1.

  During evaluation, this running mean/variance is used for normalization.

  Because the BatchNorm is done over the `C` dimension, computing statistics
  on `(N, H, W)` slices, it's common terminology to call this Spatial BatchNorm

  Args:
      num_features: num_features from an expected input of
          size batch_size x num_features x height x width
      eps: a value added to the denominator for numerical stability.
          Default: 1e-5
      momentum: the value used for the running_mean and running_var
          computation. Default: 0.1
      affine: a boolean value that when set to ``True``, gives the layer learnable
          affine parameters. Default: ``True``

  Shape::
      - Input: :math:`(N, C, H, W)`
      - Output: :math:`(N, C, H, W)` (same shape as input)

  Examples:
      >>> # With Learnable Parameters
      >>> m = SynchronizedBatchNorm2d(100)
      >>> # Without Learnable Parameters
      >>> m = SynchronizedBatchNorm2d(100, affine=False)
      >>> inputs = torch.autograd.Variable(torch.randn(20, 100, 35, 45))
      >>> outputs = m(inputs)
  """

  def _check_input_dim(self, input):
    if input.dim() != 4:
      raise ValueError(
          'expected 4D input (got {}D input)'.format(input.dim())
      )


class SynchronizedBatchNorm3d(_SynchronizedBatchNorm):
  r"""Applies Batch Normalization over a 5d input that is seen as a mini-batch
  of 4d inputs

  .. math::

      y = \frac{x - mean[x]}{ \sqrt{Var[x] + \epsilon}} * gamma + beta

  This module differs from the built-in PyTorch BatchNorm3d as the mean and
  standard-deviation are reduced across all devices during training.

  For example, when one uses `nn.DataParallel` to wrap the network during
  training, PyTorch's implementation normalize the tensor on each device using
  the statistics only on that device, which accelerated the computation and
  is also easy to implement, but the statistics might be inaccurate.
  Instead, in this synchronized version, the statistics will be computed
  over all training samples distributed on multiple devices.

  Note that, for one-GPU or CPU-only case, this module behaves exactly same
  as the built-in PyTorch implementation.

  The mean and standard-deviation are calculated per-dimension over
  the mini-batches and gamma and beta are learnable parameter vectors
  of size C (where C is the input size).

  During training, this layer keeps a running estimate of its computed mean
  and variance. The running sum is kept with a default momentum of 0.1.

  During evaluation, this running mean/variance is used for normalization.

  Because the BatchNorm is done over the `C` dimension, computing statistics
  on `(N, D, H, W)` slices, it's common terminology to call this Volumetric BatchNorm
  or Spatio-temporal BatchNorm

  Args:
      num_features: num_features from an expected input of
          size batch_size x num_features x depth x height x width
      eps: a value added to the denominator for numerical stability.
          Default: 1e-5
      momentum: the value used for the running_mean and running_var
          computation. Default: 0.1
      affine: a boolean value that when set to ``True``, gives the layer learnable
          affine parameters. Default: ``True``

  Shape::
      - Input: :math:`(N, C, D, H, W)`
      - Output: :math:`(N, C, D, H, W)` (same shape as input)

  Examples:
      >>> # With Learnable Parameters
      >>> m = SynchronizedBatchNorm3d(100)
      >>> # Without Learnable Parameters
      >>> m = SynchronizedBatchNorm3d(100, affine=False)
      >>> inputs = torch.autograd.Variable(torch.randn(20, 100, 35, 45, 10))
      >>> output = m(inputs)
  """

  def _check_input_dim(self, input):
    if input.dim() != 5:
      raise ValueError(
          'expected 5D input (got {}D input)'.format(input.dim())
      )
