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
"""Functional
"""
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

import tw
from tw import transform as T


#!<-----------------------------------------------------------------------------
#!< DATA TYPE CONVERSION
#!<-----------------------------------------------------------------------------


def to_float(inputs: Image.Image, **kwargs) -> Image.Image:
  """convert to float
  """
  raise NotImplementedError


def to_round_uint8(inputs: Image.Image, **kwargs) -> Image.Image:
  """convert to round uint8
  """
  raise NotImplementedError


def to_data_range(inputs: Image.Image, src_range, dst_range, **kwargs) -> Image.Image:
  raise NotImplementedError


def to_tensor(inputs: Image.Image, scale=None, mean=None, std=None, **kwargs) -> Image.Image:
  mean = torch.tensor(mean) if mean is not None else None
  std = torch.tensor(std) if std is not None else None

  m = tvt.functional.pil_to_tensor(inputs)
  m = m.type(torch.FloatTensor)

  if scale is not None:
    m = m.float().div(scale)
  if mean is not None:
    m.sub_(mean[:, None, None])
  if std is not None:
    m.div_(std[:, None, None])

  return m


def to_pil(inputs: Image.Image, **kwargs) -> Image.Image:
  return inputs


def to_numpy(inputs: Image.Image, **kwargs) -> Image.Image:
  return np.array(inputs)

#!<-----------------------------------------------------------------------------
#!< FLIP
#!<-----------------------------------------------------------------------------


def hflip(inputs: Image.Image, **kwargs) -> Image.Image:
  return tvf.hflip(inputs)


def vflip(inputs: Image.Image, **kwargs) -> Image.Image:
  return tvf.vflip(inputs)


def flip(inputs: Image.Image, mode, **kwargs) -> Image.Image:
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< ROTATE
#!<-----------------------------------------------------------------------------


def rotate(inputs: Image.Image, angle, interpolation=T.RESIZE_MODE.BILINEAR,
           border_mode=T.BORDER_MODE.CONSTANT, border_value=0, **kwargs) -> Image.Image:
  return tvf.rotate(inputs,
                    angle=angle,
                    interpolation=T.RESIZE_MODE_TO_PIL[interpolation],
                    expand=False)

#!<-----------------------------------------------------------------------------
#!< AFFINE
#!<-----------------------------------------------------------------------------


def affine(inputs: Image.Image, angle: float, tx: float, ty: float, scale: float,
           shear: float, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs) -> Image.Image:
  return tvf.affine(inputs, angle=angle, translate=(tx, ty), scale=scale, shear=(
      shear, shear), interpolation=T.RESIZE_MODE_TO_PIL[interpolation])


def affine_theta(inputs: Image.Image, theta, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs) -> Image.Image:
  return tvf.F_pil.affine(inputs, matrix=theta, interpolation=T.RESIZE_MODE_TO_PIL[interpolation])

#!<-----------------------------------------------------------------------------
#!< COLORSPACE
#!<-----------------------------------------------------------------------------


def change_colorspace(inputs: Image.Image, src: T.COLORSPACE, dst: T.COLORSPACE, **kwargs) -> Image.Image:
  raise NotImplementedError


def to_color(inputs: Image.Image, **kwargs) -> Image.Image:
  return inputs.convert(mode='RGB')


def to_grayscale(inputs: Image.Image, **kwargs) -> Image.Image:
  return tvf.to_grayscale(inputs)


def rgb_to_yuv709v(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def rgb_to_yuv709f(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def yuv709v_to_rgb(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def yuv709f_to_rgb(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def rgb_to_bgr(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def bgr_to_rgb(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def rgb_to_yuv601(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def yuv601_to_rgb(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def rgb_to_yiq(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def rgb_to_lhm(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def rgb_to_xyz(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def xyz_to_lab(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def rgb_to_lab(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


#!<-----------------------------------------------------------------------------
#!< PHOTOMETRIC
#!<-----------------------------------------------------------------------------

def adjust_sharpness(inputs: Image.Image, factor, **kwargs) -> Image.Image:
  return tvf.adjust_sharpness(inputs, sharpness_factor=factor)


def adjust_brightness(inputs: Image.Image, factor, **kwargs) -> Image.Image:
  return tvf.adjust_brightness(inputs, brightness_factor=factor)


def adjust_contrast(inputs: Image.Image, factor, **kwargs) -> Image.Image:
  return tvf.adjust_contrast(inputs, contrast_factor=factor)


def adjust_gamma(inputs: Image.Image, factor, gain, **kwargs) -> Image.Image:
  return tvf.adjust_gamma(inputs, gamma=factor, gain=gain)


def adjust_hue(inputs: Image.Image, factor, **kwargs) -> Image.Image:
  return tvf.adjust_hue(inputs, hue_factor=factor)


def adjust_saturation(inputs: Image.Image, factor, **kwargs) -> Image.Image:
  return tvf.adjust_saturation(inputs, saturation_factor=factor)


def photometric_distortion(inputs: Image.Image,
                           brightness_delta=32,
                           contrast_range=(0.5, 1.5),
                           saturation_range=(0.5, 1.5),
                           hue_delta=18,
                           **kwargs) -> Image.Image:
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< CROP
#!<-----------------------------------------------------------------------------


def crop(inputs: Image.Image, top, left, height, width, **kwargs) -> Image.Image:
  return tvf.crop(inputs, top, left, height, width)


def center_crop(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def center_crop_and_pad(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def resized_crop(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def ten_crop(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def five_crop(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def non_overlap_crop_patch(inputs: Image.Image, patch_size=32, stride=32, **kwargs) -> Image.Image:
  """non-overlapp crop.

    For a image [H, W, C], it will be divided into [N, patch_size, patch_size, C]
      N = ((h + patch_size) // (patch_size * stride)) * ((w + patch_size) // (patch_size * stride))

  Args:
      patch_size (int, optional): Defaults to 32.
      stride (int, optional): Defaults to 32.

  """
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< FILTER
#!<-----------------------------------------------------------------------------


def iso_noise(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def gaussian_noise(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def gaussian_blur(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def motion_blur(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def median_blur(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def sobel(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< MORPHOLOGY
#!<-----------------------------------------------------------------------------


def alpha_to_trimap(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< NORMALIZE
#!<-----------------------------------------------------------------------------


def equal_hist(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def truncated_standardize(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def local_contrast_normalize(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< PADDING
#!<-----------------------------------------------------------------------------


def pad(inputs: Image.Image, left, top, right, bottom, fill_value=0, mode='constant', **kwargs) -> Image.Image:
  return tvf.pad(inputs, [left, top, right, bottom], padding_mode=mode, fill=fill_value)


def crop_and_pad(inputs: Image.Image,
                 src_crop_y,
                 src_crop_x,
                 src_crop_h,
                 src_crop_w,
                 dst_crop_x,
                 dst_crop_y,
                 dst_height,
                 dst_width,
                 fill_value=0,
                 mode='constant',
                 **kwargs) -> Image.Image:
  raise NotImplementedError


def pad_to_size_divisible(inputs: Image.Image, size_divisible, **kwargs) -> Image.Image:
  raise NotImplementedError


def pad_to_square(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def pad_to_target_size(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< RESIZE
#!<-----------------------------------------------------------------------------


def shortside_resize(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError


def resize(inputs: Image.Image, height, width, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs) -> Image.Image:
  return tvf.resize(inputs, (height, width), interpolation=T.RESIZE_MODE_TO_PIL[interpolation])


def adaptive_resize(inputs: Image.Image, **kwargs) -> Image.Image:
  raise NotImplementedError
