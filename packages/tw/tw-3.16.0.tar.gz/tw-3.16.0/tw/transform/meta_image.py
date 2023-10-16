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


class ImageMeta(T.MetaBase):
  """ImageMeta

  Args:
    name (string/int): the identifier
    source (string): 'image' for normal rgb, 'mask' for heatmap.
    path (string): path to source
    binary: binary format like nd.array

  """

  def __init__(self, name='ImageMeta', source=T.COLORSPACE.BGR, path=None, binary=None):
    super(ImageMeta, self).__init__(name)
    self.source = source

    if path is not None:
      fs.raise_path_not_exist(path)

    self.path = path  # path to image
    self.bin = binary   # raw inputs format

    self.label = []
    self.caption = []
    self.transform = []   # transform op

  @property
  def h(self):
    return self.bin.shape[0]

  @property
  def w(self):
    return self.bin.shape[1]

  @property
  def c(self):
    if self.bin.ndim == 3:
      return self.bin.shape[2]
    elif self.bin.ndim == 2:
      return 1
    else:
      return -1

  def __str__(self):
    s = f'  ImageMeta => {self.name}\n'
    s += f'    source: {self.source}\n'
    s += f'    path: {self.path}\n'
    s += f'    shape: (h={self.h}, w={self.w}, c={self.c})\n'
    s += f'    type: {type(self.bin).__name__}, {self.bin.dtype}\n'
    if self.bin is not None:
      s += f'    binary: (h={self.h}, w={self.w}, c={self.c}, type={self.bin.__class__.__name__})\n'
      s += f'    numerical: (max={self.bin.max()}, min={self.bin.min()}, avg={self.bin.mean()})\n'
    if self.label:
      s += f'    label: {self.label}\n'
    if self.caption:
      s += f'    captions: {self.caption}\n'
    if self.transform is not None:
      s += f'    transform: {self.transform}\n'
    return s

  def numpy(self):
    if self.source in [T.COLORSPACE.HEATMAP, ]:
      self.bin = np.array(self.bin).astype('uint8')
    else:
      self.bin = np.array(self.bin).astype('float32')
    return self

  def load(self, backend='cv2'):
    # if binary file has existed, return self
    if self.bin is not None:
      return self

    if backend == 'cv2':
      self.bin = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
      if self.source == T.COLORSPACE.RGB:
        self.bin = cv2.cvtColor(self.bin, cv2.COLOR_BGR2RGB)

    elif backend == 'pil':
      self.bin = Image.open(self.path)
      if self.source == T.COLORSPACE.RGB:
        self.bin = self.bin.convert('RGB')

    else:
      raise NotImplementedError(backend)

    return self

  def to_float(self, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
      return self
    self.bin = T.to_float(self.bin, **kwargs)
    return self

  def to_round_uint8(self, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
      return self
    self.bin = T.to_round_uint8(self.bin, **kwargs)
    return self

  def to_data_range(self, src_range, dst_range, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
      return self
    self.bin = T.to_data_range(self.bin, src_range=src_range, dst_range=dst_range, **kwargs)
    return self

  def to_tensor(self, scale=None, mean=None, std=None, **kwargs):
    self.bin = T.to_tensor(self.bin, scale=scale, mean=mean, std=std, **kwargs)
    return self

  def to_pil(self, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
      return self
    self.bin = T.to_pil(self.bin, **kwargs)
    return self

  def to_numpy(self, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
      return self
    self.bin = T.to_numpy(self.bin, **kwargs)
    return self

  def hflip(self, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      self.bin = self.bin * [-1, 1]
    else:
      self.bin = T.hflip(self.bin)
    return self

  def random_hflip(self, p=0.5, **kwargs):
    if random.random() > p:
      return self.hflip(**kwargs)
    return self

  def vflip(self, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      self.bin = self.bin * [1, -1]
    else:
      self.bin = T.vflip(self.bin)
    return self

  def random_vflip(self, p=0.5, **kwargs):
    if random.random() > p:
      return self.vflip(**kwargs)
    return self

  def flip(self, mode, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    self.bin = T.flip(self.bin, mode=mode, **kwargs)
    return self

  def rotate(self, angle, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
    if self.source == T.COLORSPACE.OPTICALFLOW:
      raise NotImplementedError
    if self.source == T.COLORSPACE.HEATMAP:
      interpolation = T.RESIZE_MODE.NEAREST
    self.bin = T.rotate(self.bin, angle=angle, interpolation=interpolation, **kwargs)
    return self

  def affine(self, angle, tx, ty, scale, shear, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
    if self.source == T.COLORSPACE.OPTICALFLOW:
      raise NotImplementedError
    if self.source == T.COLORSPACE.HEATMAP:
      interpolation = T.RESIZE_MODE.NEAREST
    self.bin = T.affine(self.bin, angle=angle, tx=tx, ty=ty, scale=scale,
                        shear=shear, interpolation=interpolation, **kwargs)
    return self

  def affine_theta(self, theta, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
    if self.source == T.COLORSPACE.OPTICALFLOW:
      raise NotImplementedError
    if self.source == T.COLORSPACE.HEATMAP:
      interpolation = T.RESIZE_MODE.NEAREST
    self.bin = T.affine_theta(self.bin, theta=theta, interpolation=interpolation, **kwargs)
    return self

  def to_color(self):
    if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
      return self
    self.bin = T.to_color(self.bin)
    self.source = T.COLORSPACE.RGB
    return self

  def to_grayscale(self):
    if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
      return self
    self.bin = T.to_grayscale(self.bin)
    return self

  def change_colorspace(self, src: T.COLORSPACE, dst: T.COLORSPACE):
    if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
      return self
    self.bin = T.change_colorspace(self.bin, src=src, dst=dst)
    return self

  def rgb_to_yuv709v(self):
    if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
      return self
    if self.source != T.COLORSPACE.RGB:
      raise RuntimeError
    self.bin = T.rgb_to_yuv709v(self.bin)
    self.source = T.COLORSPACE.YUV709V
    return self

  def rgb_to_yuv709f(self):
    if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
      return self
    if self.source != T.COLORSPACE.RGB:
      raise RuntimeError
    self.bin = T.rgb_to_yuv709f(self.bin)
    self.source = T.COLORSPACE.YUV709F
    return self

  def yuv709v_to_rgb(self):
    if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
      return self
    if self.source != T.COLORSPACE.YUV709V:
      raise RuntimeError
    self.bin = T.yuv709v_to_rgb(self.bin)
    self.source = T.COLORSPACE.RGB
    return self

  def yuv709f_to_rgb(self):
    if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
      return self
    if self.source != T.COLORSPACE.YUV709F:
      raise RuntimeError
    self.bin = T.yuv709f_to_rgb(self.bin)
    self.source = T.COLORSPACE.RGB
    return self

  def rgb_to_bgr(self):
    if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
      return self
    if self.source != T.COLORSPACE.RGB:
      raise RuntimeError
    self.bin = T.rgb_to_bgr(self.bin)
    self.source = T.COLORSPACE.BGR
    return self

  def bgr_to_rgb(self):
    if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
      return self
    if self.source != T.COLORSPACE.BGR:
      raise RuntimeError
    self.bin = T.bgr_to_rgb(self.bin)
    self.source = T.COLORSPACE.RGB
    return self

  # def adjust_sharpness(self, factor, **kwargs):
  #   if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
  #     return self
  #   self.bin = T.adjust_sharpness(self.bin, factor=factor, **kwargs)
  #   return self

  # def adjust_brightness(self, factor, **kwargs):
  #   if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
  #     return self
  #   self.bin = T.adjust_brightness(self.bin, factor=factor, **kwargs)
  #   return self

  # def adjust_contrast(self, factor, **kwargs):
  #   if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
  #     return self
  #   self.bin = T.adjust_contrast(self.bin, factor=factor, **kwargs)
  #   return self

  # def adjust_gamma(self, factor, gain, **kwargs):
  #   if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
  #     return self
  #   self.bin = T.adjust_gamma(self.bin, factor=factor, gain=gain, **kwargs)
  #   return self

  # def adjust_hue(self, factor, **kwargs):
  #   if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
  #     return self
  #   self.bin = T.adjust_hue(self.bin, factor=factor, **kwargs)
  #   return self

  # def adjust_saturation(self, factor, **kwargs):
  #   if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
  #     return self
  #   self.bin = T.adjust_saturation(self.bin, factor=factor, **kwargs)
  #   return self

  def photometric_distortion(self,
                             brightness_delta=32,
                             contrast_range=(0.5, 1.5),
                             saturation_range=(0.5, 1.5),
                             hue_delta=18,
                             **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW, T.COLORSPACE.HEATMAP]:
      return self
    self.bin = T.photometric_distortion(
        self.bin,
        brightness_delta=brightness_delta,
        contrast_range=contrast_range,
        saturation_range=saturation_range,
        hue_delta=hue_delta)
    return self

  def crop(self, top, left, height, width, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    self.bin = T.crop(self.bin, top=top, left=left, height=height, width=width, **kwargs)
    return self

  def center_crop(self, height, width, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    self.bin = T.center_crop(self.bin, height=height, width=width, **kwargs)
    return self

  def random_crop(self, height, width, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    self.bin = T.random_crop(self.bin, height=height, width=width, **kwargs)
    return self

  def center_crop_and_pad(self, height, width, fill_value=0, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    self.bin = T.center_crop_and_pad(self.bin, height=height, width=width, fill_value=fill_value, **kwargs)
    return self

  def random_crop_and_pad(self, height, width, fill_value=0, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    self.bin = T.random_crop_and_pad(self.bin, height=height, width=width, fill_value=fill_value, **kwargs)
    return self

  def non_overlap_crop_patch(self, patch_size=32, stride=32, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    self.bin = T.non_overlap_crop_patch(self.bin, patch_size=patch_size, stride=stride, **kwargs)
    return self

  def pad(self, left, top, right, bottom, fill_value=0, mode='constant', **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    self.bin = T.pad(
        self.bin,
        left=left,
        top=top,
        right=right,
        bottom=bottom,
        fill_value=fill_value,
        mode=mode,
        **kwargs)
    return self

  def shortside_resize(self, min_size=256, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    if self.source in [T.COLORSPACE.HEATMAP]:
      interpolation = T.RESIZE_MODE.NEAREST
    self.bin = T.shortside_resize(self.bin, min_size=min_size, interpolation=interpolation, **kwargs)
    return self

  def resize(self, height, width, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    if self.source == T.COLORSPACE.HEATMAP:
      interpolation = T.RESIZE_MODE.NEAREST
    self.bin = T.resize(self.bin, height=height, width=width, interpolation=interpolation, **kwargs)
    return self

  #!<-----------------------------------------------------------------------------
  #!< FILTER
  #!<-----------------------------------------------------------------------------

  def iso_noise(self, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    if self.source == T.COLORSPACE.HEATMAP:
      return self
    self.bin = T.iso_noise(self.bin, **kwargs)
    return self

  def gaussian_noise(self, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    if self.source == T.COLORSPACE.HEATMAP:
      return self
    self.bin = T.gaussian_noise(self.bin, **kwargs)
    return self

  def gaussian_blur(self, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    if self.source == T.COLORSPACE.HEATMAP:
      return self
    self.bin = T.gaussian_blur(self.bin, **kwargs)
    return self

  def motion_blur(self, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    if self.source == T.COLORSPACE.HEATMAP:
      return self
    self.bin = T.motion_blur(self.bin, **kwargs)
    return self

  def median_blur(self, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    if self.source == T.COLORSPACE.HEATMAP:
      return self
    self.bin = T.median_blur(self.bin, **kwargs)
    return self

  def sobel(self, **kwargs):
    if self.source in [T.COLORSPACE.OPTICALFLOW]:
      raise NotImplementedError
    if self.source == T.COLORSPACE.HEATMAP:
      return self
    self.bin = T.sobel(self.bin, **kwargs)
    return self
