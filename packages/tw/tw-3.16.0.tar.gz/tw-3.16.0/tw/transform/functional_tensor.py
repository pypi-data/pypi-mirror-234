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


def to_float(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  """convert to float
  """
  if inputs.dtype == torch.float:
    return inputs
  return inputs.float()


def to_round_uint8(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  """convert to round uint8
  """
  return inputs.round().clamp(0, 255).byte()


def to_data_range(inputs: torch.Tensor, src_range, dst_range, **kwargs) -> torch.Tensor:
  return inputs * (float(dst_range) / float(src_range))


def to_tensor(inputs: torch.Tensor, scale=None, mean=None, std=None, **kwargs) -> torch.Tensor:
  mean = torch.tensor(mean) if mean is not None else None
  std = torch.tensor(std) if std is not None else None

  m = inputs.type(torch.FloatTensor)

  if scale is not None:
    m = m.float().div(scale)
  if mean is not None:
    m.sub_(mean[:, None, None])
  if std is not None:
    m.div_(std[:, None, None])

  return m


def to_pil(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  return tvf.to_pil_image(inputs)


def to_numpy(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  return inputs.detach().cpu().numpy()

#!<-----------------------------------------------------------------------------
#!< FLIP
#!<-----------------------------------------------------------------------------


def hflip(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  return tvf.hflip(inputs)


def vflip(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  return tvf.vflip(inputs)


def flip(inputs: torch.Tensor, mode, **kwargs) -> torch.Tensor:
  if mode == 0:
    return inputs
  elif mode == 1:
    return inputs.rot90(1, [-2, -1]).flip([-2])
  elif mode == 2:
    return inputs.flip([-2])
  elif mode == 3:
    return inputs.rot90(3, [-2, -1])
  elif mode == 4:
    return inputs.rot90(2, [-2, -1]).flip([-2])
  elif mode == 5:
    return inputs.rot90(1, [-2, -1])
  elif mode == 6:
    return inputs.rot90(2, [-2, -1])
  elif mode == 7:
    return inputs.rot90(3, [-2, -1]).flip([-2])

#!<-----------------------------------------------------------------------------
#!< ROTATE
#!<-----------------------------------------------------------------------------


def rotate(inputs: torch.Tensor, angle, interpolation=T.RESIZE_MODE.BILINEAR,
           border_mode=T.BORDER_MODE.CONSTANT, border_value=0, **kwargs) -> torch.Tensor:
  return tvf.rotate(inputs,
                    angle=angle,
                    interpolation=T.RESIZE_MODE_TO_TVF[interpolation],
                    expand=False)

#!<-----------------------------------------------------------------------------
#!< AFFINE
#!<-----------------------------------------------------------------------------


def affine(inputs: torch.Tensor, angle: float, tx: float, ty: float, scale: float,
           shear: float, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs) -> torch.Tensor:
  return tvf.affine(inputs, angle=angle, translate=(tx, ty), scale=scale, shear=(
      shear, shear), interpolation=T.RESIZE_MODE_TO_TVF[interpolation])


def affine_theta(inputs: torch.Tensor, theta, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs) -> torch.Tensor:
  return tvf.F_t.affine(inputs, matrix=inputs, interpolation=T.RESIZE_MODE_TO_TVF[interpolation])

#!<-----------------------------------------------------------------------------
#!< COLORSPACE
#!<-----------------------------------------------------------------------------


def change_colorspace(inputs: torch.Tensor, src: T.COLORSPACE, dst: T.COLORSPACE, **kwargs) -> torch.Tensor:
  if src == T.COLORSPACE.BGR and dst == T.COLORSPACE.RGB:
    return inputs.flip(dims=[-3])
  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.BGR:
    return inputs.flip(dims=[-3])

  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.YUV709F:
    return rgb_to_yuv709f(inputs)
  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.YUV709V:
    return rgb_to_yuv709v(inputs)
  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.YUV601F:
    return rgb_to_yuv601(inputs)
  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.YUV601V:
    return rgb_to_yuv601(inputs)

  elif src == T.COLORSPACE.BGR and dst == T.COLORSPACE.YUV709F:
    return rgb_to_yuv709f(inputs.flip(dims=[-3]))
  elif src == T.COLORSPACE.BGR and dst == T.COLORSPACE.YUV709V:
    return rgb_to_yuv709v(inputs.flip(dims=[-3]))
  elif src == T.COLORSPACE.BGR and dst == T.COLORSPACE.YUV601F:
    return rgb_to_yuv601(inputs.flip(dims=[-3]))
  elif src == T.COLORSPACE.BGR and dst == T.COLORSPACE.YUV601V:
    return rgb_to_yuv601(inputs.flip(dims=[-3]))

  elif src == T.COLORSPACE.YUV709F and dst == T.COLORSPACE.RGB:
    return yuv709f_to_rgb(inputs)
  elif src == T.COLORSPACE.YUV709V and dst == T.COLORSPACE.RGB:
    return yuv709v_to_rgb(inputs)
  elif src == T.COLORSPACE.YUV601F and dst == T.COLORSPACE.RGB:
    return yuv601_to_rgb(inputs)
  elif src == T.COLORSPACE.YUV601V and dst == T.COLORSPACE.RGB:
    return yuv601_to_rgb(inputs)

  elif src == T.COLORSPACE.YUV709F and dst == T.COLORSPACE.BGR:
    return yuv709f_to_rgb(inputs).flip(dims=[-3])
  elif src == T.COLORSPACE.YUV709V and dst == T.COLORSPACE.BGR:
    return yuv709v_to_rgb(inputs).flip(dims=[-3])
  elif src == T.COLORSPACE.YUV601F and dst == T.COLORSPACE.BGR:
    return yuv601_to_rgb(inputs).flip(dims=[-3])
  elif src == T.COLORSPACE.YUV601V and dst == T.COLORSPACE.BGR:
    return yuv601_to_rgb(inputs).flip(dims=[-3])

  raise NotImplementedError


def to_color(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  h, w = inputs.shape[-2:]
  if inputs.ndim == 4 and inputs.shape[1] == 1:
    return inputs.reshape(-1, 1, h, w).repeat(1, 3, 1, 1)
  elif inputs.ndim == 3 and inputs.shape[0] == 1:
    return inputs.reshape(1, h, w).repeat(3, 1, 1)
  elif inputs.ndim == 2:
    return inputs.reshape(1, h, w).repeat(3, 1, 1)
  return inputs


def to_grayscale(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  h, w = inputs.shape[-2:]
  if inputs.ndim == 4 and inputs.shape[1] != 1:
    return inputs.mean(dim=1, keepdim=True)
  elif inputs.ndim == 3 and inputs.shape[0] != 1:
    return inputs.mean(dim=0, keepdim=True)
  elif inputs.ndim == 2:
    return inputs.reshape(1, h, w)


def rgb_to_yuv709v(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  R, G, B = torch.split(inputs, 1, dim=-3)
  Y = 0.1826 * R + 0.6142 * G + 0.0620 * B + 16  # [16, 235]
  U = -0.1007 * R - 0.3385 * G + 0.4392 * B + 128  # [16, 240]
  V = 0.4392 * R - 0.3990 * G - 0.0402 * B + 128  # [16, 240]
  return torch.cat([Y, U, V], dim=-3)


def rgb_to_yuv709f(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  R, G, B = torch.split(inputs, 1, dim=-3)
  Y = 0.2126 * R + 0.7152 * G + 0.0722 * B  # [0, 255]
  U = -0.1146 * R - 0.3854 * G + 0.5000 * B + 128  # [0, 255]
  V = 0.5000 * R - 0.4542 * G - 0.0468 * B + 128  # [0, 255]
  return torch.cat([Y, U, V], dim=-3)


def yuv709v_to_rgb(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  Y, U, V = torch.split(inputs, 1, dim=-3)
  Y = Y - 16
  U = U - 128
  V = V - 128
  R = 1.1644 * Y + 1.7927 * V
  G = 1.1644 * Y - 0.2132 * U - 0.5329 * V
  B = 1.1644 * Y + 2.1124 * U
  return torch.cat([R, G, B], dim=-3)


def yuv709f_to_rgb(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  Y, U, V = torch.split(inputs, 1, dim=-3)
  Y = Y
  U = U - 128
  V = V - 128
  R = 1.000 * Y + 1.570 * V
  G = 1.000 * Y - 0.187 * U - 0.467 * V
  B = 1.000 * Y + 1.856 * U
  return torch.cat([R, G, B], dim=-3)


def rgb_to_bgr(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  r, g, b = torch.split(inputs, 1, dim=-3)
  return torch.cat([b, g, r], dim=-3)


def bgr_to_rgb(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  r, g, b = torch.split(inputs, 1, dim=-3)
  return torch.cat([b, g, r], dim=-3)


def rgb_to_yuv601(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  """Convert a batch of RGB images to a batch of YCbCr images

  It implements the ITU-R BT.601 conversion for standard-definition
  television. See more details in
  https://en.wikipedia.org/wiki/YCbCr#ITU-R_BT.601_conversion.

  Args:
      x: Batch of images with shape (N, 3, H, W). RGB color space, range [0, 255].

  Returns:
      Batch of images with shape (N, 3, H, W). YCbCr color space.
  """
  ndim = inputs.ndim
  if inputs.ndim == 3:
    inputs = inputs.unsqueeze(dim=0)

  assert inputs.ndim == 4 and inputs.size(1) == 3
  weigth = torch.tensor([
      [65.481, -37.797, 112.0],
      [128.553, -74.203, -93.786],
      [24.966, 112.0, -18.214]]).to(inputs.device)
  bias = torch.tensor([16, 128, 128]).view(1, 3, 1, 1).to(inputs.device)
  inputs = torch.matmul(inputs.permute(0, 2, 3, 1), weigth).permute(0, 3, 1, 2) + bias

  if ndim == 3:
    inputs = inputs.squeeze(dim=0)
  return inputs


def yuv601_to_rgb(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  """Convert a batch of YCbCr images to a batch of RGB images

  It implements the inversion of the above rgb2ycbcr function.

  Args:
      x: Batch of images with shape (N, 3, H, W). YCbCr color space, range [0, 255].

  Returns:
      Batch of images with shape (N, 3, H, W). RGB color space.
  """
  ndim = inputs.ndim
  if inputs.ndim == 3:
    inputs = inputs.unsqueeze(dim=0)

  assert inputs.ndim == 4 and inputs.size(1) == 3
  weight = 255. * torch.tensor([
      [0.00456621, 0.00456621, 0.00456621],
      [0, -0.00153632, 0.00791071],
      [0.00625893, -0.00318811, 0]]).to(inputs)
  bias = torch.tensor([-222.921, 135.576, -276.836]).view(1, 3, 1, 1).to(inputs)
  inputs = torch.matmul(inputs.permute(0, 2, 3, 1), weight).permute(0, 3, 1, 2) + bias

  if ndim == 3:
    inputs = inputs.squeeze(dim=0)
  return inputs


def rgb_to_yiq(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  """Convert a batch of RGB images to a batch of YIQ images

  Args:
      x: Batch of images with shape (N, 3, H, W). RGB colour space.

  Returns:
      Batch of images with shape (N, 3, H, W). YIQ colour space.
  """
  ndim = inputs.ndim
  if inputs.ndim == 3:
    inputs = inputs.unsqueeze(dim=0)

  x = inputs
  yiq_weights = torch.tensor([[0.299, 0.587, 0.114], [0.5959, -0.2746, -0.3213], [0.2115, -0.5227, 0.3112]]).t().to(x)
  inputs = torch.matmul(x.permute(0, 2, 3, 1), yiq_weights).permute(0, 3, 1, 2)

  if ndim == 3:
    inputs = inputs.squeeze(dim=0)
  return inputs


def rgb_to_lhm(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  """Convert a batch of RGB images to a batch of LHM images

  Args:
      x: Batch of images with shape (N, 3, H, W). RGB colour space.

  Returns:
      Batch of images with shape (N, 3, H, W). LHM colour space.

  Reference:
      https://arxiv.org/pdf/1608.07433.pdf
  """
  ndim = inputs.ndim
  if inputs.ndim == 3:
    inputs = inputs.unsqueeze(dim=0)

  x = inputs
  lhm_weights = torch.tensor([[0.2989, 0.587, 0.114], [0.3, 0.04, -0.35], [0.34, -0.6, 0.17]]).t().to(x)
  inputs = torch.matmul(x.permute(0, 2, 3, 1), lhm_weights).permute(0, 3, 1, 2)

  if ndim == 3:
    inputs = inputs.squeeze(dim=0)
  return inputs


def _safe_frac_pow(x: torch.Tensor, p) -> torch.Tensor:
  EPS = torch.finfo(x.dtype).eps
  return torch.sign(x) * torch.abs(x + EPS).pow(p)


def rgb_to_xyz(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  """Convert a batch of RGB images to a batch of XYZ images

  Args:
      x: Batch of images with shape (N, 3, H, W). RGB colour space.

  Returns:
      Batch of images with shape (N, 3, H, W). XYZ colour space.
  """
  ndim = inputs.ndim
  if inputs.ndim == 3:
    inputs = inputs.unsqueeze(dim=0)

  x = inputs
  mask_below = (x <= 0.04045).to(x)
  mask_above = (x > 0.04045).to(x)

  tmp = x / 12.92 * mask_below + torch.pow((x + 0.055) / 1.055, 2.4) * mask_above

  weights_rgb_to_xyz = torch.tensor([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750],
                                     [0.0193339, 0.1191920, 0.9503041]]).to(x)

  inputs = torch.matmul(tmp.permute(0, 2, 3, 1), weights_rgb_to_xyz.t()).permute(0, 3, 1, 2)

  if ndim == 3:
    inputs = inputs.squeeze(dim=0)
  return inputs


def xyz_to_lab(inputs: torch.Tensor, illuminant: str = 'D50', observer: str = '2', **kwargs) -> torch.Tensor:
  """Convert a batch of XYZ images to a batch of LAB images

  Args:
      x: Batch of images with shape (N, 3, H, W). XYZ colour space.
      illuminant: {“A”, “D50”, “D55”, “D65”, “D75”, “E”}, optional. The name of the illuminant.
      observer: {“2”, “10”}, optional. The aperture angle of the observer.

  Returns:
      Batch of images with shape (N, 3, H, W). LAB colour space.
  """
  ndim = inputs.ndim
  if inputs.ndim == 3:
    inputs = inputs.unsqueeze(dim=0)

  x = inputs
  epsilon = 0.008856
  kappa = 903.3
  illuminants = {
      'A': {'2': (1.098466069456375, 1, 0.3558228003436005),
            '10': (1.111420406956693, 1, 0.3519978321919493)},
      'D50': {'2': (0.9642119944211994, 1, 0.8251882845188288),
              '10': (0.9672062750333777, 1, 0.8142801513128616)},
      'D55': {'2': (0.956797052643698, 1, 0.9214805860173273),
              '10': (0.9579665682254781, 1, 0.9092525159847462)},
      'D65': {'2': (0.95047, 1., 1.08883),  # This was: `lab_ref_white`
              '10': (0.94809667673716, 1, 1.0730513595166162)},
      'D75': {'2': (0.9497220898840717, 1, 1.226393520724154),
              '10': (0.9441713925645873, 1, 1.2064272211720228)},
      'E': {'2': (1.0, 1.0, 1.0),
            '10': (1.0, 1.0, 1.0)}}

  illuminants_to_use = torch.tensor(illuminants[illuminant][observer]).to(x).view(1, 3, 1, 1)

  tmp = x / illuminants_to_use

  mask_below = tmp <= epsilon
  mask_above = tmp > epsilon
  tmp = _safe_frac_pow(tmp, 1. / 3.) * mask_above + (kappa * tmp + 16.) / 116. * mask_below

  weights_xyz_to_lab = torch.tensor([[0, 116., 0], [500., -500., 0], [0, 200., -200.]]).to(x)
  bias_xyz_to_lab = torch.tensor([-16., 0., 0.]).to(x).view(1, 3, 1, 1)

  inputs = torch.matmul(tmp.permute(0, 2, 3, 1), weights_xyz_to_lab.t()).permute(0, 3, 1, 2) + bias_xyz_to_lab

  if ndim == 3:
    inputs = inputs.squeeze(dim=0)
  return inputs

#!<-----------------------------------------------------------------------------
#!< PHOTOMETRIC
#!<-----------------------------------------------------------------------------


def adjust_sharpness(inputs: torch.Tensor, factor, **kwargs) -> torch.Tensor:
  return tvf.adjust_sharpness(inputs, sharpness_factor=factor)


def adjust_brightness(inputs: torch.Tensor, factor, **kwargs) -> torch.Tensor:
  return tvf.adjust_brightness(inputs, brightness_factor=factor)


def adjust_contrast(inputs: torch.Tensor, factor, **kwargs) -> torch.Tensor:
  return tvf.adjust_contrast(inputs, contrast_factor=factor)


def adjust_gamma(inputs: torch.Tensor, factor, gain, **kwargs) -> torch.Tensor:
  return tvf.adjust_gamma(inputs, gamma=factor, gain=gain)


def adjust_hue(inputs: torch.Tensor, factor, **kwargs) -> torch.Tensor:
  return tvf.adjust_hue(inputs, hue_factor=factor)


def adjust_saturation(inputs: torch.Tensor, factor, **kwargs) -> torch.Tensor:
  return tvf.adjust_saturation(inputs, saturation_factor=factor)


def photometric_distortion(inputs: torch.Tensor,
                           brightness_delta=32,
                           contrast_range=(0.5, 1.5),
                           saturation_range=(0.5, 1.5),
                           hue_delta=18,
                           **kwargs) -> torch.Tensor:
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< CROP
#!<-----------------------------------------------------------------------------


def crop(inputs: torch.Tensor, top, left, height, width, **kwargs) -> torch.Tensor:
  return tvf.crop(inputs, top, left, height, width)


def center_crop(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError


def center_crop_and_pad(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError


def resized_crop(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError


def ten_crop(inputs: torch.Tensor, crop_height, crop_width, vertical_flip, **kwargs) -> torch.Tensor:
  """crop the given image into four corners and the central crop with flip image.
  """
  return tvf.ten_crop(inputs, size=(crop_height, crop_width), vertical_flip=vertical_flip)


def five_crop(inputs: torch.Tensor, crop_height, crop_width, **kwargs) -> torch.Tensor:
  """crop the given image into four corners and the central crop.
  """
  return tvf.five_crop(inputs, size=(crop_height, crop_width))


def non_overlap_crop_patch(inputs: torch.Tensor, patch_size=32, stride=32, **kwargs) -> torch.Tensor:
  h, w = inputs.shape[-2:]
  patches = []
  for y in range(0, h - stride, stride):
    for x in range(0, w - stride, stride):
      patch = inputs[..., y: y + patch_size, x: x + patch_size]
      patches.append(patch)
  inputs = torch.stack(patches, dim=0).to(inputs)
  return inputs

#!<-----------------------------------------------------------------------------
#!< FILTER
#!<-----------------------------------------------------------------------------


def iso_noise(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError


def gaussian_noise(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError


def gaussian_blur(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError


def motion_blur(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError


def median_blur(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError


def sobel(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< MORPHOLOGY
#!<-----------------------------------------------------------------------------


def alpha_to_trimap(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< NORMALIZE
#!<-----------------------------------------------------------------------------


def equal_hist(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError


def truncated_standardize(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError


def local_contrast_normalize(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< PADDING
#!<-----------------------------------------------------------------------------


def pad(inputs: torch.Tensor, left, top, right, bottom, fill_value=0, mode='constant', **kwargs) -> torch.Tensor:
  return tvf.pad(inputs, [left, top, right, bottom], padding_mode=mode, fill=fill_value)


def crop_and_pad(inputs: torch.Tensor,
                 src_crop_y,
                 src_crop_x,
                 src_crop_h,
                 src_crop_w,
                 dst_crop_y,
                 dst_crop_x,
                 dst_height,
                 dst_width,
                 fill_value=0,
                 mode='constant',
                 **kwargs) -> torch.Tensor:
  new_shape = list(inputs.shape)
  h, w = new_shape[-2:]
  new_shape[-2] = dst_height
  new_shape[-1] = dst_width
  new_image = torch.ones(*new_shape).to(inputs) * fill_value

  sy1 = max(src_crop_y, 0)
  sy2 = min(src_crop_y + src_crop_h, h)
  sx1 = max(src_crop_x, 0)
  sx2 = min(src_crop_x + src_crop_w, w)

  dy1 = max(dst_crop_y, 0)
  dy2 = min(dst_crop_y + src_crop_h, dst_height)
  dx1 = max(dst_crop_x, 0)
  dx2 = min(dst_crop_x + src_crop_w, dst_width)

  # actual crop size
  ch = min(dy2 - dy1, sy2 - sy1)
  cw = min(dx2 - dx1, sx2 - sx1)

  # update crop area
  sy2 = sy1 + ch
  sx2 = sx1 + cw
  dy2 = dy1 + ch
  dx2 = dx1 + cw

  # print(new_image.shape, inputs.shape)
  new_image[..., dy1:dy2, dx1:dx2] = inputs[..., sy1:sy2, sx1:sx2]
  return new_image


def pad_to_size_divisible(inputs: torch.Tensor, size_divisible, **kwargs) -> torch.Tensor:
  shape = list(inputs.shape)
  shape[-1] = int(math.ceil(shape[-1] / size_divisible) * size_divisible)
  shape[-2] = int(math.ceil(shape[-2] / size_divisible) * size_divisible)
  outputs = torch.zeros(*shape).to(inputs)
  outputs[..., :inputs.shape[-2], :inputs.shape[-1]] = inputs
  return outputs


def pad_to_square(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError


def pad_to_target_size(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< RESIZE
#!<-----------------------------------------------------------------------------


def shortside_resize(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError


def resize(inputs: torch.Tensor, height, width, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs) -> torch.Tensor:
  return tvf.resize(inputs, (height, width), interpolation=T.RESIZE_MODE_TO_TVF[interpolation])


def adaptive_resize(inputs: torch.Tensor, **kwargs) -> torch.Tensor:
  raise NotImplementedError
