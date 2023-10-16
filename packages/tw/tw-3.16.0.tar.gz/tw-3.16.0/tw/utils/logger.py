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
import time
import logging
from datetime import datetime


class Logger():
  r"""Logger helper"""

  def __init__(self):
    self._initialized = False
    self._start_timer = time.time()
    self._logger = None
    try:
      import wandb
      self._wandb = wandb
    except ImportError:
      self._wandb = None

  @property
  def logger(self):
    if self._logger is None:
      if not os.path.exists('_outputs'):
        os.mkdir('_outputs')
      temp = '_outputs/tw.{}.log'.format(datetime.strftime(datetime.now(), '%y%m%d%H%M%S'))
      self.init(temp, './')
      self.warn(f'Initialize a default logger <{temp}>.')
    return self._logger

  def is_init(self):
    return self._initialized

  def init(self, name, output_dir, stdout=True):
    if self._initialized:
      return

    r"""init the logger"""
    logging.root.handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG, filename=os.path.join(output_dir, name))
    self._logger = logging.getLogger(name)
    if stdout:
      ch = logging.StreamHandler()
      ch.setLevel(logging.DEBUG)
      ch.setFormatter(logging.Formatter('%(message)s'))
      self._logger.addHandler(ch)
    self._initialized = True

  def _print(self, show_type, content):
    r"""Format print string"""
    str_date = '[' + datetime.strftime(datetime.now(), '%y.%m.%d %H:%M:%S') + '] '
    self.logger.info(str_date + show_type + ' ' + content)

  def sys(self, content):
    self._print('[SYS]', content)

  def net(self, content):
    self._print('[NET]', content)

  def train(self, content):
    self._print('[TRN]', content)

  def val(self, content):
    self._print('[VAL]', content)

  def test(self, content):
    self._print('[TST]', content)

  def warn(self, content):
    self._print('[WAN]', content)

  def info(self, content):
    self._print('[INF]', content)

  def cfg(self, content):
    self._print('[CFG]', content)

  def error(self, content):
    self._print('[ERR]', content)
    exit(-1)

  def server(self, content):
    self._print('[SERVER]', content)

  def client(self, content):
    self._print('[CLIENT]', content)

  def iters(self, keys, values, **kwargs):
    # iter/epoch
    if 'step' in kwargs and 'epoch' in kwargs and 'iters_per_epoch' in kwargs:
      _data = '[%d] Iter:%d/%d' % (kwargs['epoch'],
                                   kwargs['step'] % kwargs['iters_per_epoch'],
                                   kwargs['iters_per_epoch'])
    else:
      _data = []
      if 'epoch' in kwargs:
        _data.append('Epoch:%d' % kwargs['epoch'])
      if 'step' in kwargs:
        _data.append('Iter:%d' % kwargs['step'])
      _data = ', '.join(_data)

    # other info
    commits = {}
    for i, key in enumerate(keys):
      if isinstance(values[i], (int, str)):
        value = values[i]
        _data += ', {:}:{:}'.format(key, value)
      elif key == 'lr':
        value = round(float(values[i]), 6)
        _data += ', {:}:{:}'.format(key, value)
      elif isinstance(values[i], (list, tuple)):
        value = str([round(float(v), 4) for v in values[i]])
        _data += ', {:}:{}'.format(key, value)
      else:
        value = round(float(values[i]), 4)
        _data += ', {:}:{:.4f}'.format(key, value)

      # wandb
      if not isinstance(value, str):
        commits[key] = value
        # wandb.log({key: value}, commit=False)

    if self._wandb is not None:
      if self._wandb.run is not None and len(commits):
        self._wandb.log(commits)

    return _data

  def tic(self):
    self._start_timer = time.time()

  def toc(self):
    return (time.time() - self._start_timer) * 1000

  def tick(self):
    return time.time()

  def duration(self, start_time, end_time):
    return (end_time - start_time) * 1000


logger = Logger()
