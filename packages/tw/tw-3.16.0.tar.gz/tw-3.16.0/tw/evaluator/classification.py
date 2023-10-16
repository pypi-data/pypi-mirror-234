# Copyright 2018 The KaiJIN Authors. All Rights Reserved.
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
import torch
import numpy as np
from .base import Evaluator


class TopkEvaluator(Evaluator):

  def __init__(self, topk, offset=0):
    super().__init__()
    self.topk = [i + 1 for i in range(topk)]
    self.offset = offset
    self.metrics = []

  def reset(self):
    self.metrics.clear()

  def append(self, values):
    r"""values should be a confusion_matrix"""
    self.metrics.append(values)

  def compute(self, preds, targets):
    r"""Computes the precision@k for the specified values of k

    Args:
      preds: [N, C]
      targets: [N, ]

    Returns:
      list with shape(k): the correct percentage among N inputs.

    """
    maxk = max(self.topk)
    batch_size = targets.size(0)

    _, pred = preds.topk(maxk, 1, True, True)
    pred = self.offset + pred.t()
    correct = pred.eq(targets.reshape(1, -1).expand_as(pred))

    tops = []
    for k in self.topk:
      correct_k = correct[:k].reshape(-1).float().sum(0)
      tops.append(correct_k.mul_(100.0 / batch_size))

    return tops

  def TopN(self, n):
    result = 0.0
    for metric in self.metrics:
      result += metric[n - 1].cpu().item()
    return result / len(self.metrics)

  def Top1(self):
    return self.TopN(1)

  def Top5(self):
    return self.TopN(5)

  def accumulate(self):
    return {'top1': self.Top1(), 'top5': self.Top5()}


class MultiLabelClsEvaluator(Evaluator):
  def __init__(self, topk, num_classes):
    super().__init__()
    self.topk = topk
    self.num_classes = num_classes
    self.metrics = []

  def reset(self):
    self.metrics.clear()

  def append(self, values):
    r"""values should be a confusion_matrix"""
    self.metrics.append(values)

  def compute(self, preds, targets):
    r"""Computes the precision@k for the specified values of k

    Arguments:
      preds: [N, C] float value range from 0 to 1
      targets: [N, C] long value 0 or 1

    Returns:
      list with shape(k): the correct percentage among N inputs.
    """
    device = preds.device
    preds = torch.where(preds > 0.5, torch.tensor(1).to(device), torch.tensor(0).to(device))

    tops = []
    for i in range(self.topk):
      acc = ((preds == targets).sum(dim=1) >= (self.num_classes - i)).sum()
      acc = acc.float() / preds.size(0)
      tops.append(acc)

    return tops

  def TopN(self, n):
    result = 0.0
    for metric in self.metrics:
      result += metric[n - 1].cpu().item()
    return result / len(self.metrics)

  def accumulate(self):
    acc = {}
    for i in range(self.topk):
      acc['top%d' % (i + 1)] = self.TopN(i + 1)
    return acc


class ConfusionMatrixEvaluator(Evaluator):

  def __init__(self, num_classes):
    super().__init__()
    self.num_classes = num_classes
    # groundtruth - prediction
    self.confusion_matrix = torch.zeros((num_classes, num_classes))

  def reset(self):
    self.confusion_matrix.zero_()

  def append(self, values):
    r"""values should be a confusion_matrix"""
    pass

  def compute(self, preds: torch.Tensor, targets: torch.Tensor):
    r"""Computes the precision@k for the specified values of k

    Args:
      preds: [N, C]
      targets: [N, ]

    Returns:
      list with shape(k): the correct percentage among N inputs.

    """
    assert preds.ndim == 2 and targets.ndim == 1
    pred = preds.argmax(dim=1)

    for i, target in enumerate(targets):
      self.confusion_matrix[target][pred[i]] += 1

  def accumulate(self):
    pred_class_num = self.confusion_matrix.sum(dim=0)
    gt_class_num = self.confusion_matrix.sum(dim=1)
    class_precision = torch.zeros(self.num_classes)
    class_recall = torch.zeros(self.num_classes)

    results = {
        'avg_accuracy': (torch.trace(self.confusion_matrix) / self.confusion_matrix.sum()).item(),
    }

    for i in range(self.num_classes):
      results[f'prec@{i}'] = (self.confusion_matrix[i][i] / pred_class_num[i]).item()
      results[f'recall@{i}'] = (self.confusion_matrix[i][i] / gt_class_num[i]).item()

    return results


class MultiLabelClsRegEvaluator(Evaluator):
  """MultiLabel classification and regression evaluator

   - top1, topn accuracy over each classes and mean accuracy
   - convert classification to regression and computing mae/rmse etc.

  """

  def __init__(self, root=None, topk=5, labels=None, ignore=-1, **kwargs):
    super().__init__()
    self.topk = topk
    self.ignore = ignore

  def compute(self, inputs, targets, **kwargs):
    """computing regression and classification index.

    Args:
        inputs (torch.FloatTensor): [batch, num_classes, num_labels] each label with num_classes
        targets (torch.LongTensor): [batch, num_labels]

    """
    assert targets.ndim == 2, "require targets with (batch, num_labels)"
    assert inputs.ndim == 3, "require inputs with (batch, num_classes, num_labels)"
    bs, num_classes, num_labels = inputs.shape

    # ignore labels
    if self.ignore >= 0:
      inds = (targets != self.ignore).nonzero(as_tuple=True)
      targets = targets[inds]  # [batch, ]
      inputs = inputs.permute(0, 2, 1)[inds]  # [batch, num_classes]
      bs = targets.size(0)
      if bs == 0:
        return {
            'top1': torch.zeros(1).cpu(),
            'topk': torch.zeros(1).cpu(),
            'mae': torch.zeros(1).cpu(),
            'mse': torch.zeros(1).cpu(),
        }

      top_vals, top_inds = inputs.max(dim=1)
      top1_res = top_inds.eq(targets).float().sum(dim=0).div(bs)

      topk_vals, topk_inds = inputs.topk(self.topk, 1, True, True)
      topk_res = topk_inds.eq(targets.reshape(-1, 1).expand_as(topk_inds)).sum(dim=[0, 1]).div(bs)

      return {
          'top1': top1_res.reshape(1).cpu(),
          'topk': topk_res.reshape(1).cpu(),
          'mae': torch.zeros(1).cpu(),
          'mse': torch.zeros(1).cpu(),
      }

    else:
      # cls head
      top_vals, top_inds = inputs.max(dim=1)
      top1_res = top_inds.eq(targets).float().sum(dim=0).div(bs)

      topk_vals, topk_inds = inputs.topk(self.topk, 1, True, True)
      topk_res = topk_inds.eq(targets.reshape(bs, 1, num_labels).expand_as(topk_inds)).sum(dim=[0, 1]).div(bs)

      # reg head -> cls result to regression
      coeffs = torch.arange(0, num_classes).reshape(1, 1, num_classes).repeat(
          bs, num_labels, 1).transpose(1, 2).to(inputs)
      error = ((coeffs * inputs.softmax(dim=1)).sum(dim=1) - targets.float()).mean(dim=0)
      mae = error.abs()
      mse = error.pow(2)

      return {
          'top1': top1_res,
          'topk': topk_res,
          'mae': mae,
          'mse': mse,
      }

  def accumulate(self):

    top1, topk, mae, mse = [], [], [], []
    for t in self.metrics:
      top1.append(t['top1'])
      mae.append(t['mae'])
      mse.append(t['mse'])
      topk.append(t['topk'])
    top1 = torch.stack(top1, dim=0).mean(dim=0).cpu().numpy()
    topk = torch.stack(topk, dim=0).mean(dim=0).cpu().numpy()
    mae = torch.stack(mae, dim=0).mean(dim=0).cpu().numpy()
    rmse = torch.stack(mse, dim=0).mean(dim=0).sqrt().cpu().numpy()

    return {
        'top1': top1.tolist(),
        'topk': topk.tolist(),
        'mae': mae.tolist(),
        'rmse': rmse.tolist(),
        'mean_top1': np.mean(top1),
        'mean_mae': np.mean(mae),
        'mean_rmse': np.mean(rmse),
    }
