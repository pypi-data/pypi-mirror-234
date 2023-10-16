# Copyright 2022 The KaiJIN Authors. All Rights Reserved.
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
"""META
"""
import os
import math
import random
import typing
import functools
from enum import Enum

import cv2
import PIL
from PIL import Image
import numpy as np

import torch
import torchvision.transforms.functional as tvf
import torchvision.transforms as tvt

from tw import transform as T
from tw.utils.logger import logger
from tw.utils import filesystem as fs


class VideoMeta(T.MetaBase):
  """VideoMeta: a list of images with same size.

  Args:
    name (string/int): the identifier
    source (string): 'image' for normal rgb, 'mask' for heatmap.
    path (list of string): a list of images
    binary (a numpy file): [frame, h, w, c]

  """

  def __init__(self, name='VideoMeta', source=T.COLORSPACE.BGR, path=None, binary=None):
    super(VideoMeta, self).__init__(name)
    self.source = source

    # path
    if path is not None:
      assert isinstance(path, list), "path should be a image path list."
      for p in path:
        fs.raise_path_not_exist(path)
    self.path = path

    # attribute
    self.bin = binary
    if self.bin is None:
      self.h = 0
      self.w = 0
      self.c = 0
      self.n = 0
    else:
      self.numpy()
      self.n, self.h, self.w, self.c = self.bin.shape

    # labels
    self.label = []
    self.caption = []
    self.transform = []   # transform op

  def __str__(self):
    s = '  VideoMeta=> {}\n'.format(self.name)
    s += '    source: {}\n'.format(self.source)
    s += '    path: {}\n'.format(self.path)
    s += '    shape: (h={}, w={}, c={})\n'.format(self.h, self.w, self.c)

    if self.bin is not None:
      if len(self.bin.shape) == 4:
        n, h, w, c = self.bin.shape
      else:
        raise NotImplementedError(self.bin.shape)

      s += '    binary: (n={}, h={}, w={}, c={}, type={})\n'.format(
          n, h, w, c, self.bin.__class__.__name__)
      s += '    numerical: (max={}, min={}, avg={})\n'.format(
          self.bin.max(), self.bin.min(), self.bin.mean())
    if self.label:
      s += '    label: {}\n'.format(self.label)
    if self.caption:
      s += '    captions: {}\n'.format(self.caption)
    if self.transform is not None:
      s += '    transform: {}\n'.format(self.transform)
    return s

  def numpy(self):
    if self.source == T.COLORSPACE.HEATMAP:
      self.bin = np.array(self.bin).astype('uint8')
    else:
      self.bin = np.array(self.bin).astype('float32')
    return self

  def load(self):
    if self.bin is None:
      self.bin = np.array([cv2.imread(p, cv2.IMREAD_UNCHANGED) for p in self.path])  # nopep8
      if len(self.bin.shape) == 4:
        self.n, self.h, self.w, self.c = self.bin.shape
      else:
        raise NotImplementedError(self.bin.shape, self.path)
    return self

  def to_tensor(self, scale=None, mean=None, std=None, **kwargs):
    if self.bin.ndim == 4:
      m = torch.from_numpy(np.ascontiguousarray(self.bin.transpose((3, 0, 1, 2))))
    else:
      raise NotImplementedError(self.bin.ndim)
    m = m.type(torch.FloatTensor)
    if scale is not None:
      m = m.float().div(scale)
    if mean is not None:
      m.sub_(mean[:, None, None, None])
    if std is not None:
      m.div_(std[:, None, None, None])
    self.bin = m
    return self
