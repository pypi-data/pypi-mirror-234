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
import os
import shutil
import pickle
from urllib.parse import urlparse
import torch
from torch import nn

from .logger import logger
from . import filesystem as fs
from . import env


def download_url_to_file(url, dst=None):
  if dst is None:
    dst = os.path.join(env.DEFAULT_MODEL_DIR, os.path.basename(urlparse(url).path))
  if not os.path.exists(dst):
    torch.hub.download_url_to_file(url, dst)
  return dst


def load(path: str, verbose=True) -> dict:
  """loading model parameter, this is a default load function.

  Args:
    path(str): a path to source.

  Returns:
    state_dict(dict): vanilla data.

  """
  if verbose:
    logger.info('Loading model from %s' % path)

  if path.startswith('http'):

    has_file = env.DEFAULT_MODEL_DIR + os.path.basename(urlparse(path).path)

    if os.path.exists(has_file):
      if verbose:
        logger.info('Loading model from cache: %s' % has_file)
      content = fs.load(has_file, backend='torch')

    else:
      content = torch.hub.load_state_dict_from_url(path, env.DEFAULT_MODEL_DIR, 'cpu')

  else:
    content = fs.load(path, backend='torch')

  return content


def replace_prefix(state_dict: dict, old_prefix='', new_prefix=''):
  """replace state_dict key old_prefix with new_prefix
  """
  content = {}
  for k, v in state_dict.items():
    k = k[k.startswith(old_prefix) and len(old_prefix):]
    k = new_prefix + k
    content[k] = v
  return content


def replace_substr(state_dict: dict, old_substr='', new_substr=''):
  """replace state_dict key old_substr with new_substr
  """
  content = {}
  for k, v in state_dict.items():
    content[k.replace(old_substr, new_substr)] = v
  return content


def add_prefix(state_dict: dict, prefix=''):
  """add state_dict key prefix
  """
  content = {}
  for k, v in state_dict.items():
    content[prefix + k] = v
  return content


def load_matched_state_dict(model: torch.nn.Module, state_dict: dict, verbose=True):
  """Only loads weights that matched in key and shape. Ignore other weights.

  Args:
    model:
    state_dict:
    verbose:

  """
  num_matched = 0
  num_total = 0
  curr_state_dict = model.state_dict()

  if verbose:
    logger.net('IMPORT PRETRAINED MODELS:')
    logger.net('{:80} {:20} {:20} {:5}'.format('NAME', 'MODEL_SHAPE', 'CHECKPOINT', 'IMPORTED'))

  for key in curr_state_dict.keys():
    num_total += 1
    curr_shape = str(list(curr_state_dict[key].shape))
    shape = str(list(state_dict[key].shape)) if key in state_dict else None

    if key in state_dict and curr_shape == shape:
      curr_state_dict[key] = state_dict[key]
      num_matched += 1
      if verbose:
        logger.net('{:80} {:20} {:20} {:5}'.format(key, curr_shape, shape, True))

    elif key in state_dict and curr_shape != shape:
      logger.warn('{:80} {:20} {:20} {:5}'.format(key, curr_shape, shape, False))

    elif key not in state_dict:
      logger.warn('{:80} {:20} {:20} {:5}'.format(key, curr_shape, 'UNDEFINED', False))

    else:
      pass

  model.load_state_dict(curr_state_dict)

  if verbose:
    logger.sys('Checkpoint file total with %d tensors.' % len(state_dict))
    logger.sys(f'Loaded state_dict: {num_matched}/{num_total} matched')

  return model


def print_trainable_variables(model: nn.Module):
  """fetch trainable variables
  """
  logger.net('TRAINABLE VARIABLES:')
  max_len = max(max([len(name) for name, p in model.named_parameters()]), 60)
  logger.net(('{:%d} {:20} {:^8} {:^8} {:^8}' % (max_len + 5)).format('WEIGHT', 'SHAPE', 'TRAIN', 'MEAN', 'STD'))
  for name, p in model.named_parameters():
    logger.net(('{:%d} {:20} {:^8d} {:^8.4f} {:^8.4f}' % (max_len + 5)).format(
        name, str(list(p.shape)), p.requires_grad, p.mean(), p.std()))


def load_state_dict_from_url(model: nn.Module, path, key=None, verbose=True, **kwargs):
  """download and open checkpoint from url/path, and load into model.

  Args:
      model (nn.Module): model.
      path ([type]): url or file path.
  """
  state_dict = load(path)
  if key is not None:
    state_dict = state_dict[key]
  load_matched_state_dict(model, state_dict, verbose=verbose)


def compare_tensor(*tensors, name=None):
  """compare two tensor value with stat

  Args:
      tensors (torch.Tensor): any
      name (str, optional): Defaults to None.

  """
  if name is None:
    name = 'var'
  for i, tensor in enumerate(tensors):
    t = tensor.cpu()
    logger.info('[{}] shape:{}, sum:{:.4f}, mean:{:.4f}, var:{:.4f}, max:{:.4f}, min:{:.4f}'.format(
        f'{name}:{i}', str(t.shape), t.sum().item(), t.mean().item(), t.var().item(), t.max().item(), t.min().item()))


def print_tensor_title(name=None):
  """to corresponding to print tensor
  """
  s = ''
  if name is not None:
    s += f'<=========== [{name}] ===========>\n'
  s += '{:30s} {:25s} {:20s} {:15s} {:15s} {:15s} {:15s}'.format('NAME', 'SHAPE', 'SUM', 'MEAN', 'VAR', 'MAX', 'MIN')
  # logger.info(s)
  return s


def print_tensor(t, name=None):
  """print tensor info

  Args:
      tensors (torch.Tensor): any
      name (str, optional): Defaults to None.

  """
  if name is None:
    name = 'tensor'
  if t is None:
    return ''
  if torch.is_complex(t):
    t = torch.real(t)
  s = '{:30s} {:25s} {:<20.3f} {:<15.3f} {:<15.3f} {:<15.3f} {:<15.3f}'.format(
      f'{name}', str(list(t.shape)), t.sum().item(), t.float().mean().item(), t.float().var().item(), t.max().item(), t.min().item())
  # logger.info()
  return s
