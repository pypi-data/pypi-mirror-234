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
import sys
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


class BoxListMeta(T.MetaBase):
  def __init__(self, name='BoxListMeta'):
    super(BoxListMeta, self).__init__(name)
    self.format = 'xyxy'
    self.bboxes = []
    self.bboxes_count = 0
    self.label = []
    self.caption = []
    self.transform = []
    self.extra = []

    # affine to image size
    self.max_x = sys.float_info.max
    self.min_x = -sys.float_info.max
    self.max_y = sys.float_info.max
    self.min_y = -sys.float_info.max
    self.is_affine_size = False
    self.visibility = True
    self.min_area = 0.0

  def set_affine_size(self, max_h, max_w, min_area=0.0, visibility=True):
    self.min_area = min_area
    self.visibility = visibility
    self.is_affine_size = True
    self.min_x, self.max_x, self.min_y, self.max_y = 0, max_w - 1, 0, max_h - 1
    return self

  def clip_with_affine_size(self):
    assert isinstance(self.bboxes, np.ndarray)
    self.bboxes = self.bboxes.clip(
        [self.min_x, self.min_y, self.min_x, self.min_y],
        [self.max_x, self.max_y, self.max_x, self.max_y])
    return self

  def numpy(self):
    self.bboxes = np.array(self.bboxes).astype('float32')
    return self

  def __str__(self):
    s = '  BoxListMeta => {}\n'.format(self.name)
    total = []
    if self.bboxes_count:
      total.append(self.bboxes)
    if self.label is not None:
      total.append(self.label)
    if len(self.caption):
      total.append(self.caption)
    if len(self.extra) != 0:
      for key in self.extra:
        total.append(getattr(self, key))
    for i, item in enumerate(zip(*total)):
      s += '    {}: {}\n'.format(i, item)
    if self.transform is not None:
      s += '    transform: {}\n'.format(self.transform)
    return s

  def add(self, x1, y1, x2, y2, label=None, caption=None, **kwargs):
    self.bboxes.append([x1, y1, x2, y2])
    self.bboxes_count += 1
    if label is not None:
      self.label.append(label)
    if caption is not None:
      self.caption.append(caption)
    for key, value in kwargs.items():
      if hasattr(self, key):
        getattr(self, key).append(value)
      else:
        setattr(self, key, [value, ])
        self.extra.append(key)

    return self

  def hflip(self, **kwargs):
    assert self.is_affine_size
    x1, y1 = self.bboxes[..., 0], self.bboxes[..., 1]
    x2, y2 = self.bboxes[..., 2], self.bboxes[..., 3]
    self.bboxes = np.stack([self.max_x - x2, y1, self.max_x - x1, y2], axis=1)
    return self

  def vflip(self, **kwargs):
    assert self.is_affine_size
    x1, y1 = self.bboxes[..., 0], self.bboxes[..., 1]
    x2, y2 = self.bboxes[..., 2], self.bboxes[..., 3]
    self.bboxes = np.stack([x1, self.max_y - y2, x2, self.max_y - y1], axis=1)

  def rotate(self, angle, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
    scale = 1.0
    shift = (0, 0)

    width, height = self.max_x, self.max_y
    center = (width / 2, height / 2)
    matrix = cv2.getRotationMatrix2D(center, angle, scale)
    matrix[0, 2] += shift[0]
    matrix[1, 2] += shift[1]

    bbox = np.stack([self.bboxes[:, 0], self.bboxes[:, 1],
                     self.bboxes[:, 2], self.bboxes[:, 1],
                     self.bboxes[:, 0], self.bboxes[:, 3],
                     self.bboxes[:, 2], self.bboxes[:, 3]], axis=1).reshape(-1, 2)
    bbox = cv2.transform(bbox[None], matrix).squeeze().reshape(-1, 8)
    self.bboxes = np.stack([
        np.amin(bbox[..., ::2], axis=1),
        np.amin(bbox[..., 1::2], axis=1),
        np.amax(bbox[..., ::2], axis=1),
        np.amax(bbox[..., 1::2], axis=1),
    ], axis=1)

    if self.visibility:
      self.clip_with_affine_size()

    return self

  def pad(self, left, top, right, bottom, fill_value=0, mode='constant', **kwargs):
    assert self.is_affine_size
    self.bboxes += [left, top, left, top]
    width = self.max_x + left + right
    height = self.max_y + top + bottom
    self.set_affine_size(height, width)
    self.clip_with_affine_size()

  def shortside_resize(self, min_size=256, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
    def _get_shortside_shape(h, w, min_size):
      if (w <= h and w == min_size) or (h <= w and h == min_size):
        ow, oh = w, h
      # resize
      if w < h:
        ow = min_size
        oh = int(min_size * h / w)
      else:
        oh = min_size
        ow = int(min_size * w / h)
      return oh, ow

    assert self.is_affine_size
    oh, ow = _get_shortside_shape(self.max_y, self.max_x, min_size)
    scale_w = float(ow) / self.max_x
    scale_h = float(oh) / self.max_y
    self.bboxes *= [scale_w, scale_h, scale_w, scale_h]
    self.set_affine_size(oh, ow)

  def resize(self, height, width, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
    assert self.is_affine_size
    scale_w = float(width) / self.max_x
    scale_h = float(height) / self.max_y
    if len(self.bboxes) > 0:
      self.bboxes *= np.array([scale_w, scale_h, scale_w, scale_h])
    self.transform.append(('resize', self.max_y, height, self.max_x, width))
    self.set_affine_size(height, width)
