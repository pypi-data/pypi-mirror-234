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
import itertools
import typing
import functools
from enum import Enum
from collections import OrderedDict

import skimage

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
#!< Wrapper
#!<-----------------------------------------------------------------------------


def autotype(func):
  """auto conversion for inputs datatype
  """
  @functools.wraps(func)
  def wrapper(inputs: np.ndarray, *args, **kwargs):
    if inputs.dtype == np.uint8:
      return to_round_uint8(func(inputs, *args, **kwargs))
    else:
      return func(inputs, *args, **kwargs)
  return wrapper

#!<-----------------------------------------------------------------------------
#!< Related with Data Type
#!<-----------------------------------------------------------------------------


def to_float(inputs: np.ndarray, **kwargs) -> np.ndarray:
  """convert to float
  """
  if inputs.dtype == 'float32':
    return inputs
  return inputs.astype('float32')


def to_round_uint8(inputs: np.ndarray, **kwargs) -> np.ndarray:
  """convert to round uint8
  """
  return inputs.round().clip(0, 255).astype('uint8')


def to_data_range(inputs: np.ndarray, src_range, dst_range, **kwargs) -> np.ndarray:
  if src_range == dst_range:
    return inputs
  return inputs * (float(dst_range) / float(src_range))


def to_tensor(inputs: np.ndarray, scale=None, mean=None, std=None, **kwargs) -> np.ndarray:
  # mean = torch.tensor(mean) if mean is not None else None
  # std = torch.tensor(std) if std is not None else None

  if inputs.ndim == 3:
    m = torch.from_numpy(np.ascontiguousarray(inputs.transpose((2, 0, 1))))
  elif inputs.ndim == 2:
    m = torch.from_numpy(np.ascontiguousarray(inputs)).unsqueeze(dim=0)
  elif inputs.ndim == 4:
    m = torch.from_numpy(np.ascontiguousarray(inputs.transpose((0, 3, 1, 2))))
  else:
    raise NotImplementedError(inputs.ndim)

  m = m.type(torch.FloatTensor)
  if scale is not None:
    m = m.float().div(scale)
  if mean is not None:
    m.sub_(torch.tensor(mean)[:, None, None])
  if std is not None:
    m.div_(torch.tensor(std)[:, None, None])
  return m


def to_pil(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return tvf.to_pil_image(to_round_uint8(inputs))


def to_numpy(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return inputs

#!<-----------------------------------------------------------------------------
#!< Related with Colorspace
#!<-----------------------------------------------------------------------------


@autotype
def change_colorspace(inputs: np.ndarray, src: T.COLORSPACE, dst: T.COLORSPACE, **kwargs) -> np.ndarray:

  if src == T.COLORSPACE.BGR and dst == T.COLORSPACE.RGB:
    out = cv2.cvtColor(inputs, cv2.COLOR_BGR2RGB)
  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.BGR:
    out = cv2.cvtColor(inputs, cv2.COLOR_RGB2BGR)

  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.HSV:
    out = cv2.cvtColor(inputs, cv2.COLOR_RGB2HSV)
  elif src == T.COLORSPACE.HSV and dst == T.COLORSPACE.RGB:
    out = cv2.cvtColor(inputs, cv2.COLOR_HSV2RGB)

  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.YUV709F:
    out = rgb_to_yuv709f(inputs)
  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.YUV709V:
    out = rgb_to_yuv709v(inputs)
  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.YUV601F:
    out = rgb_to_yuv601f(inputs)
  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.YUV601V:
    out = rgb_to_yuv601v(inputs)

  elif src == T.COLORSPACE.BGR and dst == T.COLORSPACE.YUV709F:
    out = rgb_to_yuv709f(inputs[..., ::-1])
  elif src == T.COLORSPACE.BGR and dst == T.COLORSPACE.YUV709V:
    out = rgb_to_yuv709v(inputs[..., ::-1])
  elif src == T.COLORSPACE.BGR and dst == T.COLORSPACE.YUV601F:
    out = rgb_to_yuv601f(inputs[..., ::-1])
  elif src == T.COLORSPACE.BGR and dst == T.COLORSPACE.YUV601V:
    out = rgb_to_yuv601v(inputs[..., ::-1])

  elif src == T.COLORSPACE.YUV709F and dst == T.COLORSPACE.RGB:
    out = yuv709f_to_rgb(inputs)
  elif src == T.COLORSPACE.YUV709V and dst == T.COLORSPACE.RGB:
    out = yuv709v_to_rgb(inputs)
  elif src == T.COLORSPACE.YUV601F and dst == T.COLORSPACE.RGB:
    out = yuv601f_to_rgb(inputs)
  elif src == T.COLORSPACE.YUV601V and dst == T.COLORSPACE.RGB:
    out = yuv601v_to_rgb(inputs)

  elif src == T.COLORSPACE.YUV709F and dst == T.COLORSPACE.BGR:
    out = yuv709f_to_rgb(inputs)[..., ::-1]
  elif src == T.COLORSPACE.YUV709V and dst == T.COLORSPACE.BGR:
    out = yuv709v_to_rgb(inputs)[..., ::-1]
  elif src == T.COLORSPACE.YUV601F and dst == T.COLORSPACE.BGR:
    out = yuv601f_to_rgb(inputs)[..., ::-1]
  elif src == T.COLORSPACE.YUV601V and dst == T.COLORSPACE.BGR:
    out = yuv601v_to_rgb(inputs)[..., ::-1]

  else:
    raise NotImplementedError(src, dst)

  return out


@autotype
def to_color(inputs: np.ndarray, **kwargs) -> np.ndarray:
  if inputs.ndim == 3 and inputs.shape[2] == 3:
    return inputs
  h, w = inputs.shape[:2]
  inputs = inputs.reshape([h, w, 1])
  return np.repeat(inputs, 3, axis=2)


@autotype
def to_grayscale(inputs: np.ndarray, **kwargs) -> np.ndarray:
  h, w = inputs.shape[:2]
  if inputs.ndim == 3 and inputs.shape[2] != 1:
    return np.mean(inputs, axis=2, keepdims=True)
  elif inputs.ndim == 2:
    return inputs.reshape(h, w, 1)


@autotype
def rgb_to_yuv709v(inputs: np.ndarray, **kwargs) -> np.ndarray:
  R, G, B = np.split(inputs.astype('float32'), 3, axis=2)
  Y = 0.1826 * R + 0.6142 * G + 0.0620 * B + 16  # [16, 235]
  U = -0.1007 * R - 0.3385 * G + 0.4392 * B + 128  # [16, 240]
  V = 0.4392 * R - 0.3990 * G - 0.0402 * B + 128  # [16, 240]
  YUV = np.concatenate([Y, U, V], axis=2)
  return YUV


@autotype
def rgb_to_yuv709f(inputs: np.ndarray, **kwargs) -> np.ndarray:
  R, G, B = np.split(inputs.astype('float32'), 3, axis=2)
  Y = 0.2126 * R + 0.7152 * G + 0.0722 * B  # [0, 255]
  U = -0.1146 * R - 0.3854 * G + 0.5000 * B + 128  # [0, 255]
  V = 0.5000 * R - 0.4542 * G - 0.0468 * B + 128  # [0, 255]
  YUV = np.concatenate([Y, U, V], axis=2)
  return YUV


@autotype
def yuv709v_to_rgb(inputs: np.ndarray, **kwargs) -> np.ndarray:
  Y, U, V = np.split(inputs.astype('float32'), 3, axis=2)
  Y = Y - 16
  U = U - 128
  V = V - 128
  R = 1.1644 * Y + 1.7927 * V
  G = 1.1644 * Y - 0.2132 * U - 0.5329 * V
  B = 1.1644 * Y + 2.1124 * U
  RGB = np.concatenate([R, G, B], axis=2)
  return RGB


@autotype
def yuv709f_to_rgb(inputs: np.ndarray, **kwargs) -> np.ndarray:
  Y, U, V = np.split(inputs.astype('float32'), 3, axis=2)
  Y = Y
  U = U - 128
  V = V - 128
  R = 1.000 * Y + 1.5748 * V
  G = 1.000 * Y - 0.1873 * U - 0.4681 * V
  B = 1.000 * Y + 1.8556 * U
  RGB = np.concatenate([R, G, B], axis=2)
  return RGB


@autotype
def rgb_to_bgr(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return cv2.cvtColor(inputs, cv2.COLOR_RGB2BGR)


@autotype
def bgr_to_rgb(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return cv2.cvtColor(inputs, cv2.COLOR_RGB2BGR)


@autotype
def rgb_to_yuv601v(inputs: np.ndarray, **kwargs) -> np.ndarray:
  R, G, B = np.split(inputs.astype('float32'), 3, axis=2)
  Y = 0.257 * R + 0.504 * G + 0.098 * B + 16  # [16, 235]
  U = -0.148 * R - 0.291 * G + 0.439 * B + 128  # [16, 240]
  V = 0.439 * R - 0.368 * G - 0.071 * B + 128  # [16, 240]
  YUV = np.concatenate([Y, U, V], axis=2)
  return YUV


@autotype
def rgb_to_yuv601f(inputs: np.ndarray, **kwargs) -> np.ndarray:
  R, G, B = np.split(inputs.astype('float32'), 3, axis=2)
  Y = 0.299 * R + 0.587 * G + 0.114 * B  # [0, 255]
  U = -0.169 * R - 0.331 * G + 0.500 * B + 128  # [0, 255]
  V = 0.500 * R - 0.419 * G - 0.081 * B + 128  # [0, 255]
  YUV = np.concatenate([Y, U, V], axis=2)
  return YUV


@autotype
def yuv601v_to_rgb(inputs: np.ndarray, **kwargs) -> np.ndarray:
  Y, U, V = np.split(inputs.astype('float32'), 3, axis=2)
  Y = Y - 16
  U = U - 128
  V = V - 128
  R = 1.164 * Y + 1.596 * V
  G = 1.164 * Y - 0.392 * U - 0.813 * V
  B = 1.164 * Y + 2.017 * U
  RGB = np.concatenate([R, G, B], axis=2)
  return RGB


@autotype
def yuv601f_to_rgb(inputs: np.ndarray, **kwargs) -> np.ndarray:
  Y, U, V = np.split(inputs.astype('float32'), 3, axis=2)
  Y = Y
  U = U - 128
  V = V - 128
  R = 1.000 * Y + 1.402 * V
  G = 1.000 * Y - 0.344 * U - 0.714 * V
  B = 1.000 * Y + 1.772 * U
  RGB = np.concatenate([R, G, B], axis=2)
  return RGB


@autotype
def rgb_to_yuv601(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return skimage.color.rgb2ycbcr(inputs.astype('float32'))


@autotype
def yuv601_to_rgb(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return skimage.color.ycbcr2rgb(inputs.astype('float32'))


@autotype
def rgb_to_yiq(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return skimage.color.rgb2yiq(inputs.astype('float32'))


@autotype
def rgb_to_lhm(inputs: np.ndarray, **kwargs) -> np.ndarray:
  tw.logger.warn('currently not support.')
  return inputs


@autotype
def rgb_to_xyz(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return skimage.color.rgb2xyz(inputs)


@autotype
def xyz_to_lab(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return skimage.color.xyz2lab(inputs)


@autotype
def rgb_to_lab(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return skimage.color.rgb2lab(inputs)


@autotype
def yuv420_to_yuv444(inputs: np.ndarray, height: int, width: int, interpolation: T.RESIZE_MODE, **kwargs):
  """convert yuv420 to yuv444
  """
  inputs = inputs.astype('float32')
  assert inputs.ndim == 1, "inputs must be 1-dim"
  assert height % 2 == 0 and width % 2 == 0, "height and width must be even"

  step = height * width
  y = inputs[: step].reshape([height, width])
  u = inputs[step: step + step // 4].reshape([height // 2, width // 2])
  v = inputs[step + step // 4:].reshape([height // 2, width // 2])

  u = cv2.resize(u, (width, height), interpolation=T.RESIZE_MODE_TO_CV[interpolation])
  v = cv2.resize(v, (width, height), interpolation=T.RESIZE_MODE_TO_CV[interpolation])

  return np.stack([y, u, v], axis=2)


@autotype
def yuv444_to_yuv420(inputs: np.ndarray, height: int, width: int, interpolation: T.RESIZE_MODE, **kwargs):
  """convert yuv444 to yuv420
  """
  inputs = inputs.astype('float32')
  assert height % 2 == 0 and width % 2 == 0, "height and width must be even"

  if inputs.ndim == 1:
    step = height * width
    y = inputs[: step].reshape([height, width])
    u = inputs[step: step + step].reshape([height, width])
    v = inputs[step + step: step + step + step].reshape([height, width])
  elif inputs.ndim == 3:
    y, u, v = np.split(inputs, 3, axis=2)

  u = cv2.resize(u, (width // 2, height // 2), interpolation=T.RESIZE_MODE_TO_CV[interpolation])
  v = cv2.resize(v, (width // 2, height // 2), interpolation=T.RESIZE_MODE_TO_CV[interpolation])

  y = y.reshape([height * width])
  u = u.reshape([height * width // 4])
  v = v.reshape([height * width // 4])

  return np.concatenate([y, u, v], axis=0)


#!<-----------------------------------------------------------------------------
#!< Related with Shapren
#!<-----------------------------------------------------------------------------


@autotype
def usm_sharpen(inputs: np.ndarray, kernel_size=3, sigma=0.8, coeff=0.5, **kwargs) -> np.ndarray:
  inputs = inputs.astype('float32')

  guassian = cv2.GaussianBlur(inputs, (kernel_size, kernel_size), sigma)
  outputs = (1.0 + coeff) * inputs - coeff * guassian
  return outputs


@autotype
def bilateral_usm_sharpen(inputs: np.ndarray, kernel_size=3, sigma_blur=0.8,
                          sigma_color=10, sigma_space=1, coeff=1.2, **kwargs) -> np.ndarray:
  inputs = inputs.astype('float32')

  guassian = cv2.GaussianBlur(inputs, (kernel_size, kernel_size), sigma_blur)
  bfilter = cv2.bilateralFilter(src=inputs, d=5, sigmaColor=sigma_color, sigmaSpace=sigma_space)
  outputs = bfilter + coeff * (inputs - guassian)

  return outputs


@autotype
def adaptive_usm_sharpen(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


@autotype
def high_contrast_sharpen(inputs: np.ndarray, sigma_color=10, sigma_space=1, coeff=2.0, **kwargs) -> np.ndarray:
  inputs = inputs.astype('float32')

  avg_blur = cv2.blur(inputs, (3, 3))
  hPass = inputs - avg_blur + 127
  bfilter = cv2.bilateralFilter(src=inputs, d=5, sigmaColor=sigma_color, sigmaSpace=sigma_space)
  outputs = coeff * hPass + bfilter - 255.0

  return outputs


@autotype
def photoshop_usm_sharpen(inputs: np.ndarray, kernel_size=5, sigma=1.5, amount=0.5, **kwargs) -> np.ndarray:
  inputs = inputs.astype('float32')

  height, width = inputs.shape[:2]
  G = cv2.GaussianBlur(inputs, (kernel_size, kernel_size), sigma)
  value = inputs - G
  threshold = 0
  mask = np.zeros((height, width, 3), np.float32)
  mask[value > threshold] = 255
  alpha = cv2.GaussianBlur(mask, (kernel_size, kernel_size), sigma)
  K = inputs + amount * value
  outputs = (K * alpha + inputs * (255 - alpha)) / 255.0

  return outputs


#!<-----------------------------------------------------------------------------
#!< Related with Blur
#!<-----------------------------------------------------------------------------

@autotype
def gaussian_blur(inputs: np.ndarray, kernel_size=3, sigma=0, **kwargs) -> np.ndarray:
  """Blur the input image using a Gaussian filter with a random kernel size.

  Args:
      kernel_size (int, (int, int)): maximum Gaussian kernel size for blurring the input image.
          Must be zero or odd and in range [0, inf). If set to 0 it will be computed from sigma
          as `round(sigma * (3 if img.dtype == np.uint8 else 4) * 2 + 1) + 1`.
          If set single value `blur_limit` will be in range (0, blur_limit).
          Default: (3, 7).
      sigma (float, (float, float)): Gaussian kernel standard deviation. Must be in range [0, inf).
          If set single value `sigma_limit` will be in range (0, sigma_limit).
          If set to 0 sigma will be computed as `sigma = 0.3*((ksize-1)*0.5 - 1) + 0.8`. Default: 0.

  Targets:
      image

  Image types:
      uint8, float32
  """
  inputs = inputs.astype('float32')
  return cv2.GaussianBlur(inputs, ksize=(kernel_size, kernel_size), sigmaX=sigma)


@autotype
def motion_blur(inputs: np.ndarray, kernel_size=7, allow_shifted=False, dist_range=None, **kwargs) -> np.ndarray:
  """Apply motion blur to the input image using a random-sized kernel.

  Args:
      kernel_size (int): maximum kernel size for blurring the input image.
          Should be in range [3, inf). Default: (3, 7).
      allow_shifted (bool): if set to true creates non shifted kernels only,
          otherwise creates randomly shifted kernels. Default: True.
      dist_range ((int, int)): motion kernel shift distance range.
          must be range in (0, 1].

  Targets:
      image

  Image types:
      uint8, float32
  """
  inputs = inputs.astype('float32')

  def generate_line(ksize, allow_shifted):
    x1, x2 = random.randint(0, ksize - 1), random.randint(0, ksize - 1)
    if x1 == x2:
      y1, y2 = random.sample(range(ksize), 2)
    else:
      y1, y2 = random.randint(0, ksize - 1), random.randint(0, ksize - 1)

    def make_odd_val(v1, v2):
      len_v = abs(v1 - v2) + 1
      if len_v % 2 != 1:
        if v2 > v1:
          v2 -= 1
        else:
          v1 -= 1
      return v1, v2

    if not allow_shifted:
      x1, x2 = make_odd_val(x1, x2)
      y1, y2 = make_odd_val(y1, y2)

      xc = (x1 + x2) / 2
      yc = (y1 + y2) / 2

      center = ksize / 2 - 0.5
      dx = xc - center
      dy = yc - center
      x1, x2 = [int(i - dx) for i in [x1, x2]]
      y1, y2 = [int(i - dy) for i in [y1, y2]]

    return x1, y1, x2, y2

  if dist_range is not None:
    a, b = dist_range
    assert a >= 0 and b <= 1, "dist_range must be in range [0, 1)"
    max_dist = np.sqrt((kernel_size - 1) * (kernel_size - 1))
    a, b = max_dist * a, max_dist * b
    while True:
      x1, y1, x2, y2 = generate_line(kernel_size, allow_shifted)
      if np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) >= a and np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) < b:
        break
  else:
    x1, y1, x2, y2 = generate_line(kernel_size, allow_shifted)

  kernel = np.zeros((kernel_size, kernel_size), dtype=np.uint8)
  kernel = cv2.line(kernel, (x1, y1), (x2, y2), 1, thickness=1)
  kernel = kernel.astype(np.float32) / np.sum(kernel)

  outputs = cv2.filter2D(inputs, ddepth=-1, kernel=kernel)
  return outputs


@autotype
def median_blur(inputs: np.ndarray, kernel_size=3, **kwargs) -> np.ndarray:
  """Blur the input image using a median filter with a random aperture linear size.

  Args:
      kernel_size (int): maximum aperture linear size for blurring the input image.
          Must be odd and in range [3, inf). Default: (3, 7).

  Targets:
      image

  Image types:
      uint8, float32
  """
  inputs = to_round_uint8(inputs)
  assert kernel_size >= 3 and kernel_size % 2 == 1, "kernel_size must be odd and greater than 3"
  return cv2.medianBlur(inputs, ksize=kernel_size)


@autotype
def glass_blur(inputs: np.ndarray, sigma=0.7, max_delta=4, iterations=2, mode='fast', **kwargs) -> np.ndarray:
  """Apply glass noise to the input image.

  Args:
      sigma (float): standard deviation for Gaussian kernel.
      max_delta (int): max distance between pixels which are swapped.
      iterations (int): number of repeats.
          Should be in range [1, inf). Default: (2).
      mode (str): mode of computation: fast or exact. Default: "fast".
      p (float): probability of applying the transform. Default: 0.5.

  Targets:
      image

  Image types:
      uint8, float32

  Reference:
  |  https://arxiv.org/abs/1903.12261
  |  https://github.com/hendrycks/robustness/blob/master/ImageNet-C/create_c/make_imagenet_c.py
  """
  inputs = inputs.astype('float32')

  # generate array containing all necessary values for transformations
  width_pixels = inputs.shape[0] - max_delta * 2
  height_pixels = inputs.shape[1] - max_delta * 2
  total_pixels = width_pixels * height_pixels
  dxy = np.random.randint(-max_delta, max_delta, size=(total_pixels, iterations, 2))

  x = cv2.GaussianBlur(np.array(inputs), sigmaX=sigma, ksize=(0, 0))

  if mode == "fast":
    hs = np.arange(inputs.shape[0] - max_delta, max_delta, -1)
    ws = np.arange(inputs.shape[1] - max_delta, max_delta, -1)
    h = np.tile(hs, ws.shape[0])
    w = np.repeat(ws, hs.shape[0])

    for i in range(iterations):
      dy = dxy[:, i, 0]
      dx = dxy[:, i, 1]
      x[h, w], x[h + dy, w + dx] = x[h + dy, w + dx], x[h, w]

  elif mode == "exact":
    for ind, (i, h, w) in enumerate(
        itertools.product(
            range(iterations),
            range(inputs.shape[0] - max_delta, max_delta, -1),
            range(inputs.shape[1] - max_delta, max_delta, -1),
        )
    ):
      ind = ind if ind < len(dxy) else ind % len(dxy)
      dy = dxy[ind, i, 0]
      dx = dxy[ind, i, 1]
      x[h, w], x[h + dy, w + dx] = x[h + dy, w + dx], x[h, w]

  else:
    ValueError(f"Unsupported mode `{mode}`. Supports only `fast` and `exact`.")

  return cv2.GaussianBlur(x, sigmaX=sigma, ksize=(0, 0))


@autotype
def advanced_blur(inputs: np.ndarray, kernel_size=3, sigma=0.8, rotate=0,
                  beta=1.0, noise=(0.75, 1.25), **kwargs) -> np.ndarray:
  """Blur the input image using a Generalized Normal filter with a randomly selected parameters.
        This transform also adds multiplicative noise to generated kernel before convolution.

  Args:
      blur_limit: maximum Gaussian kernel size for blurring the input image.
          Must be zero or odd and in range [0, inf). If set to 0 it will be computed from sigma
          as `round(sigma * (3 if img.dtype == np.uint8 else 4) * 2 + 1) + 1`.
          If set single value `blur_limit` will be in range (0, blur_limit).
          Default: (3, 7).
      sigmaX_limit: Gaussian kernel standard deviation. Must be in range [0, inf).
          If set single value `sigmaX_limit` will be in range (0, sigma_limit).
          If set to 0 sigma will be computed as `sigma = 0.3*((ksize-1)*0.5 - 1) + 0.8`. Default: 0.
      sigmaY_limit: Same as `sigmaY_limit` for another dimension.
      rotate_limit: Range from which a random angle used to rotate Gaussian kernel is picked.
          If limit is a single int an angle is picked from (-rotate_limit, rotate_limit). Default: (-90, 90).
      beta_limit: Distribution shape parameter, 1 is the normal distribution. Values below 1.0 make distribution
          tails heavier than normal, values above 1.0 make it lighter than normal. Default: (0.5, 8.0).
      noise_limit: Multiplicative factor that control strength of kernel noise. Must be positive and preferably
          centered around 1.0. If set single value `noise_limit` will be in range (0, noise_limit).
          Default: (0.75, 1.25).
      p (float): probability of applying the transform. Default: 0.5.

  Reference:
      https://arxiv.org/abs/2107.10833

  Targets:
      image

  Image types:
      uint8, float32
  """
  inputs = inputs.astype('float32')

  ksize = kernel_size
  sigmaX = sigma
  sigmaY = sigma
  angle = np.deg2rad(rotate)
  beta = beta
  noise_matrix = np.random.uniform(noise[0], noise[1], size=ksize)

  # Generate mesh grid centered at zero.
  ax = np.arange(-ksize // 2 + 1.0, ksize // 2 + 1.0)
  # Shape (ksize, ksize, 2)
  grid = np.stack(np.meshgrid(ax, ax), axis=-1)

  # Calculate rotated sigma matrix
  d_matrix = np.array([[sigmaX**2, 0], [0, sigmaY**2]])
  u_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
  sigma_matrix = np.dot(u_matrix, np.dot(d_matrix, u_matrix.T))

  inverse_sigma = np.linalg.inv(sigma_matrix)
  # Described in "Parameter Estimation For Multivariate Generalized Gaussian Distributions"
  kernel = np.exp(-0.5 * np.power(np.sum(np.dot(grid, inverse_sigma) * grid, 2), beta))
  # Add noise
  kernel = kernel * noise_matrix

  # Normalize kernel
  kernel = kernel.astype(np.float32) / np.sum(kernel)

  outputs = cv2.filter2D(inputs, ddepth=-1, kernel=kernel)
  return outputs


@autotype
def defocus_blur(inputs: np.ndarray, radius=3, alias_blur=0.1, **kwargs) -> np.ndarray:
  """
  Apply defocus transform. See https://arxiv.org/abs/1903.12261.

  Args:
      radius ((int, int) or int): range for radius of defocusing.
          If limit is a single int, the range will be [1, limit]. Default: (3, 10).
      alias_blur ((float, float) or float): range for alias_blur of defocusing (sigma of gaussian blur).
          If limit is a single float, the range will be (0, limit). Default: (0.1, 0.5).
      p (float): probability of applying the transform. Default: 0.5.

  Targets:
      image

  Image types:
      Any
  """
  if radius <= 0:
    raise ValueError("Parameter radius must be positive")

  if alias_blur < 0:
    raise ValueError("Parameter alias_blur must be non-negative")

  inputs = inputs.astype('float32')

  length = np.arange(-max(8, radius), max(8, radius) + 1)
  ksize = 3 if radius <= 8 else 5

  x, y = np.meshgrid(length, length)
  aliased_disk = np.array((x**2 + y**2) <= radius**2, dtype=np.float32)
  aliased_disk /= np.sum(aliased_disk)

  kernel = gaussian_blur(aliased_disk, ksize, sigma=alias_blur)
  return cv2.filter2D(inputs, ddepth=-1, kernel=kernel)


@autotype
def zoom_blur(inputs: np.ndarray, zoom_factor=1.1, step_factor=0.01, **kwargs) -> np.ndarray:
  """
  Apply zoom blur transform. See https://arxiv.org/abs/1903.12261.

  Args:
      max_factor ((float, float) or float): range for max factor for blurring.
          If max_factor is a single float, the range will be (1, limit). Default: (1, 1.31).
          All max_factor values should be larger than 1.
      step_factor ((float, float) or float): If single float will be used as step parameter for np.arange.
          If tuple of float step_factor will be in range `[step_factor[0], step_factor[1])`. Default: (0.01, 0.03).
          All step_factor values should be positive.

  Targets:
      image

  Image types:
      Any
  """
  inputs = inputs.astype('float32')

  def central_zoom(img: np.ndarray, zoom_factor: int) -> np.ndarray:
    h, w = img.shape[:2]
    h_ch, w_ch = math.ceil(h / zoom_factor), math.ceil(w / zoom_factor)
    h_top, w_top = (h - h_ch) // 2, (w - w_ch) // 2
    crop = img[h_top: h_top + h_ch, w_top: w_top + w_ch]
    new_h, new_w = int(crop.shape[0] * zoom_factor), int(crop.shape[1] * zoom_factor)
    img = cv2.resize(crop, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    h_trim_top, w_trim_top = (img.shape[0] - h) // 2, (img.shape[1] - w) // 2
    return img[h_trim_top: h_trim_top + h, w_trim_top: w_trim_top + w]

  zoom_factors = np.arange(1.0, zoom_factor, step_factor)
  out = np.zeros_like(inputs, dtype=np.float32)

  for zoom_factor in zoom_factors:
    out += central_zoom(inputs, zoom_factor)
  inputs = ((inputs + out) / (len(zoom_factors) + 1)).astype(inputs.dtype)

  return inputs

#!<-----------------------------------------------------------------------------
#!< Related with Noise/Denoise
#!<-----------------------------------------------------------------------------


@autotype
def iso_noise(inputs: np.ndarray, color_shift=0.01, intensity=0.1, **kwargs) -> np.ndarray:
  """Apply poisson noise to image to simulate camera sensor noise.

  Args:
      image (numpy.ndarray): Input image, currently, only RGB, uint8 images are supported.
      color_shift (float): variance range for color hue change.
          Measured as a fraction of 360 degree Hue angle in HLS colorspace.
      intensity (float): Multiplication factor for noise values.
          Values of ~0.5 are produce noticeable, yet acceptable level of noise.

  Returns:
      numpy.ndarray: Noised image

  Image types:
      uint8, float32
  """
  inputs = inputs.astype(np.float32)

  one_over_255 = float(1.0 / 255.0)
  inputs = np.multiply(inputs, one_over_255, dtype=np.float32)
  hls = cv2.cvtColor(inputs, cv2.COLOR_RGB2HLS)
  _, stddev = cv2.meanStdDev(hls)

  luminance_noise = np.random.poisson(stddev[1] * intensity * 255, size=hls.shape[:2])
  color_noise = np.random.normal(0, color_shift * 360 * intensity, size=hls.shape[:2])

  hue = hls[..., 0]
  hue += color_noise
  hue[hue < 0] += 360
  hue[hue > 360] -= 360

  luminance = hls[..., 1]
  luminance += (luminance_noise / 255) * (1.0 - luminance)

  return cv2.cvtColor(hls, cv2.COLOR_HLS2RGB) * 255


@autotype
def gaussian_noise(inputs: np.ndarray, mean=0, std=0.01, per_channel=True, **kwargs) -> np.ndarray:
  """Apply gaussian noise to the input image.

  Args:
      mean (float): mean of the noise. Default: 0
      std (float): variance range for noise. If var_limit is a single float, the range
          will be (0, var_limit). Default: (10.0, 50.0).
      per_channel (bool): if set to True, noise will be sampled for each channel independently.
          Otherwise, the noise will be sampled once for all channels. Default: True

  Targets:
      image

  Image types:
      uint8, float32
  """
  inputs = inputs.astype(np.float32)

  if per_channel:
    gauss = np.random.normal(mean, std, inputs.shape)
  else:
    gauss = np.random.normal(mean, std, inputs.shape[:2])
    if len(inputs.shape) == 3:
      gauss = np.expand_dims(gauss, -1)

  return inputs + gauss


@autotype
def poisson_noise(inputs: np.ndarray, lam=1.0, per_channel=True, elementwise=True, **kwargs) -> np.ndarray:
  """possion noise

  Args:
      lam (float or tuple of floats): If single float image will be multiplied to this number.
          If tuple of float multiplier will be in range `[multiplier[0], multiplier[1])`. Default: (0.9, 1.1).
      per_channel (bool): If `False`, same values for all channels will be used.
          If `True` use sample values for each channels. Default False.
      elementwise (bool): If `False` multiply multiply all pixels in an image with a random value sampled once.
          If `True` Multiply image pixels with values that are pixelwise randomly sampled. Defaule: False.

  Targets:
      image

  Image types:
      Any
  """
  inputs = inputs.astype('float32')
  h, w = inputs.shape[:2]

  if per_channel:
    if inputs.ndim == 2:
      c = 1
    else:
      c = inputs.shape[-1]
  else:
    c = 1

  if elementwise:
    shape = [h, w, c]
  else:
    shape = [c]

  noise = np.random.poisson(lam, size=shape)

  if inputs.ndim == 2:
    noise = np.squeeze(noise)

  return inputs + noise


@autotype
def multiplicative_noise(inputs: np.ndarray, multiplier=(
        0.9, 1.1), per_channel=True, elementwise=True, **kwargs) -> np.ndarray:
  """multiplicative noise

  Args:
      multiplier (float or tuple of floats): If single float image will be multiplied to this number.
            If tuple of float multiplier will be in range `[multiplier[0], multiplier[1])`. Default: (0.9, 1.1).
      per_channel (bool): If `False`, same values for all channels will be used.
          If `True` use sample values for each channels. Default False.
      elementwise (bool): If `False` multiply multiply all pixels in an image with a random value sampled once.
          If `True` Multiply image pixels with values that are pixelwise randomly sampled. Defaule: False.

  Targets:
      image

  Image types:
      Any
  """
  inputs = inputs.astype('float32')
  h, w = inputs.shape[:2]

  if per_channel:
    if inputs.ndim == 2:
      c = 1
    else:
      c = inputs.shape[-1]
  else:
    c = 1

  if elementwise:
    shape = [h, w, c]
  else:
    shape = [c]

  noise = np.random.uniform(multiplier[0], multiplier[1], size=shape)

  if inputs.ndim == 2:
    noise = np.squeeze(noise)

  return inputs * noise


#!<-----------------------------------------------------------------------------
#!< Related with Color
#!<-----------------------------------------------------------------------------

@autotype
def adjust_sharpness(inputs: np.ndarray, factor=1.0, **kwargs):
  """adjust brightness of the input image

  Args:
      inputs (np.ndarray): input image
      factor (float, optional): sharpness factor. Defaults to 1.0.

  Targets:
      image

  Image types:
      uint8, float32
  """
  inputs = inputs.astype('float32')
  kernel = np.array([
      1, 1, 1,
      1, 5, 1,
      1, 1, 1
  ]).reshape((3, 3)).astype(np.float32) / 13.0
  blur = cv2.filter2D(inputs, ddepth=-1, kernel=kernel)
  return (1 - factor) * blur + factor * inputs


@autotype
def adjust_brightness(inputs: np.ndarray, factor=1.0, **kwargs):
  """adjust brightness of the input image

  Args:
      inputs (np.ndarray): input image
      factor (float, optional): brightness factor. Defaults to 1.0.

  Targets:
      image

  Image types:
      uint8, float32
  """
  inputs = to_round_uint8(inputs)
  lut = np.arange(0, 256) * factor
  lut = to_round_uint8(lut)
  return cv2.LUT(inputs, lut)


@autotype
def adjust_contrast(inputs: np.ndarray, factor=1.0, **kwargs):
  """adjust contrast of the input image

  Args:
      inputs (np.ndarray): input image
      factor (float, optional): contrast factor. Defaults to 1.0.

  Targets:
      image

  Image types:
      uint8, float32
  """
  inputs = to_round_uint8(inputs)
  if inputs.ndim == 3:
    mean = cv2.cvtColor(inputs, cv2.COLOR_RGB2GRAY).mean()
  else:
    mean = inputs.mean()

  lut = np.arange(0, 256) * factor
  lut = lut + mean * (1 - factor)
  lut = to_round_uint8(lut)

  return cv2.LUT(inputs, lut)


@autotype
def adjust_gamma(inputs: np.ndarray, factor=1.0, gain=1.0, **kwargs):
  """adjust gamma of the input image

  Args:
      inputs (np.ndarray): input image
      factor (float, optional): gamma factor. Defaults to 1.0.

  Targets:
      image

  Image types:
      uint8, float32
  """
  if inputs.dtype == np.uint8:
    table = to_round_uint8((np.arange(0, 256.0 / 255, 1.0 / 255) ** factor) * 255 * gain)
    return cv2.LUT(inputs, table)
  else:
    return gain * np.power(inputs, factor)


@autotype
def adjust_hue(inputs: np.ndarray, factor=1.0, **kwargs):
  """adjust hue of the input image

  Args:
      inputs (np.ndarray): input image
      factor (float, optional): hue factor. Defaults to 1.0.

  Targets:
      image

  Image types:
      uint8, float32

  """
  if inputs.ndim == 2:
    return inputs
  inputs = inputs.astype('float32')

  inputs = cv2.cvtColor(inputs, cv2.COLOR_RGB2HSV)
  inputs[..., 0] = np.mod(inputs[..., 0] + factor * 360, 360)
  return cv2.cvtColor(inputs, cv2.COLOR_HSV2RGB)


@autotype
def adjust_saturation(inputs: np.ndarray, factor=1.0, gamma=0, **kwargs):
  """adjust saturation of the input image

  Args:
      inputs (np.ndarray): input image
      factor (float, optional): saturation factor. Defaults to 1.0.
      gamma (int, optional): gamma correction. Defaults to 0.

  Targets:
      image

  Image types:
      uint8, float32
  """
  if inputs.ndim == 2:
    return inputs
  inputs = to_round_uint8(inputs)

  gray = cv2.cvtColor(inputs, cv2.COLOR_RGB2GRAY)
  gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

  return cv2.addWeighted(inputs, factor, gray, 1 - factor, gamma=gamma)


@autotype
def photometric_distortion(inputs: np.ndarray,
                           brightness_delta=32,
                           contrast_range=(0.5, 1.5),
                           saturation_range=(0.5, 1.5),
                           hue_delta=18,
                           **kwargs) -> np.ndarray:
  """photometric distortion

  Args:
      inputs (np.ndarray): input image
      brightness_delta (int, optional): brightness delta. Defaults to 32.
      contrast_range (tuple, optional): contrast range. Defaults to (0.5, 1.5).
      saturation_range (tuple, optional): saturation range. Defaults to (0.5, 1.5).
      hue_delta (int, optional): hue delta. Defaults to 18.

  Targets:
      image

  Image types:
      uint8, float32
  """
  inputs = inputs.astype('float32')

  # random brightness
  if random.randint(0, 2):
    delta = random.uniform(-brightness_delta, brightness_delta)
    inputs += delta

  # mode == 0 --> do random contrast first
  # mode == 1 --> do random contrast last
  mode = random.randint(0, 2)
  if mode == 1:
    if random.randint(0, 2):
      alpha = random.uniform(contrast_range[0], contrast_range[1])
      inputs *= alpha

  # convert color from BGR to HSV
  inputs = change_colorspace(inputs, src=T.COLORSPACE.RGB, dst=T.COLORSPACE.HSV)

  # random saturation
  if random.randint(0, 2):
    inputs[..., 1] *= random.uniform(saturation_range[0], saturation_range[1])

  # random hue
  if random.randint(0, 2):
    inputs[..., 0] += random.uniform(-hue_delta, hue_delta)
    inputs[..., 0][inputs[..., 0] > 360] -= 360
    inputs[..., 0][inputs[..., 0] < 0] += 360

  # convert color from HSV to BGR
  inputs = change_colorspace(inputs, src=T.COLORSPACE.HSV, dst=T.COLORSPACE.RGB)

  # random contrast
  if mode == 0:
    if random.randint(0, 2):
      alpha = random.uniform(contrast_range[0], contrast_range[1])
      inputs *= alpha

  # randomly swap channels
  # if random.randint(0, 2):
  #   axis = [0, 1, 2]
  #   random.shuffle(axis)
  #   inputs = inputs[..., axis]

  return inputs

#!<-----------------------------------------------------------------------------
#!< Related with Image Tone Changing
#!<-----------------------------------------------------------------------------


@autotype
def equal_hist(inputs: np.ndarray, per_channel=True, **kwargs):
  """equalize histogram of the input image

  Args:
      inputs (np.ndarray): input image
      per_channel (bool, optional): whether to equalize histogram per channel. Defaults to True.

  Targets:
      image

  Image types:
      uint8, float32
  """
  x = to_round_uint8(inputs)

  # if per_channel:
  #   for i in range(inputs.shape[-1]):
  #     inputs[..., i] = cv2.equalizeHist(inputs[..., i])
  # else:
  #   inputs = cv2.equalizeHist(inputs)

  for c in range(x.shape[2]):
    img = x[..., c]
    histogram = cv2.calcHist([img], [0], None, [256], (0, 256)).ravel()
    h = [_f for _f in histogram if _f]
    if len(h) <= 1:
      return img.copy()
    step = np.sum(h[:-1]) // 255
    if not step:
      return img.copy()
    lut = np.empty(256, dtype=np.uint8)
    n = step // 2
    for i in range(256):
      lut[i] = min(n // step, 255)
      n += histogram[i]
    x[..., c] = cv2.LUT(img, np.array(lut))

  return x


@autotype
def match_hist(inputs: np.ndarray, **kwargs):
  raise NotImplementedError(__name__)


@autotype
def truncated_standardize(inputs: np.ndarray, **kwargs):
  """truncated standardization

  Args:
      inputs (np.ndarray): input image

  Targets:
      image

  Image types:
      float32
  """
  assert inputs.dtype == np.float32, "inputs.dtype must be float32"

  if inputs.ndim == 3:
    h, w, c = inputs.shape
  elif inputs.ndim == 2:
    h, w = inputs.shape
    c = 1
  else:
    raise NotImplementedError(inputs.ndim)

  min_std = 1.0 / math.sqrt(float(h * w * c))
  adjust_std = max(np.std(inputs), min_std)
  outputs = (inputs - np.mean(inputs)) / adjust_std
  return outputs


@autotype
def local_contrast_normalize(inputs: np.ndarray, p=3, q=3, c=1, **kwargs):
  """local contrast normalize

  Ref:
    "No-Reference Image Quality Assessment in the Spatial Domain"

  Note:
      a smaller normalization window size improves the performance. In practice
  we pick P = Q = 3 so the window size is much smaller than the input image patch.
  Note that with this local normalization each pixel may have a different local
  mean and variance.

  Args:
      inputs ([type]):
      p (int, optional):  the normalization window size.
      q (int, optional):  the normalization window size.
      c (int, optional):  C is a positive constant that prevents dividing by zero

  Returns:
      [type]: [description]
  """
  raise NotImplementedError(__name__)


@autotype
def change_tone_curve(inputs: np.ndarray, low=0.25, high=0.75, **kwargs):
  """Rescales the relationship between bright and dark areas of the image by manipulating its tone curve.

  Args:
      img (numpy.ndarray): RGB or grayscale image.
      low_y (float): y-position of a Bezier control point used
          to adjust the tone curve, must be in range [0, 1]
      high_y (float): y-position of a Bezier control point used
          to adjust image tone curve, must be in range [0, 1]


  Targets:
      image

  Image types:
      uint8
  """
  assert 0 < low < 1 and 0 < high < 1, "low and high must be in range [0, 1]"
  inputs = to_round_uint8(inputs)

  t = np.linspace(0.0, 1.0, 256)

  # Defines responze of a four-point bezier curve
  def evaluate_bez(t):
    return 3 * (1 - t) ** 2 * t * low + 3 * (1 - t) * t**2 * high + t**3

  evaluate_bez = np.vectorize(evaluate_bez)
  remapping = np.rint(evaluate_bez(t) * 255).astype(np.uint8)

  return cv2.LUT(inputs, remapping)


@autotype
def clahe(inputs: np.ndarray, clip_limit=4.0, tile_grid_size=(8, 8), **kwargs):
  """Apply Contrast Limited Adaptive Histogram Equalization to the input image.

  Args:
      clip_limit (float or (float, float)): upper threshold value for contrast limiting.
          If clip_limit is a single float value, the range will be (1, clip_limit). Default: (1, 4).
      tile_grid_size ((int, int)): size of grid for histogram equalization. Default: (8, 8).

  Targets:
      image

  Image types:
      uint8
  """
  inputs = to_round_uint8(inputs)

  clahe_mat = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)

  if len(inputs.shape) == 2 or inputs.shape[2] == 1:
    inputs = clahe_mat.apply(inputs)
  else:
    inputs = cv2.cvtColor(inputs, cv2.COLOR_RGB2LAB)
    inputs[:, :, 0] = clahe_mat.apply(inputs[:, :, 0])
    inputs = cv2.cvtColor(inputs, cv2.COLOR_LAB2RGB)

  return inputs


@autotype
def homomorphic(inputs: np.ndarray, **kwargs):
  raise NotImplementedError(__name__)


@autotype
def sepia(inputs: np.ndarray, alpha=1.0, **kwargs):
  assert alpha >= 0.0 and alpha <= 1.0, "alpha must be in range [0, 1]"
  sepia_transformation_matrix = np.matrix([
      [0.393, 0.769, 0.189],
      [0.349, 0.686, 0.168],
      [0.272, 0.534, 0.131]
  ])
  aug = cv2.transform(inputs, sepia_transformation_matrix)
  return (1.0 - alpha) * inputs + alpha * aug


@autotype
def solarize(inputs: np.ndarray, threshold=128, **kwargs):
  """Invert all pixel values above a threshold.

  Args:
      inputs (numpy.ndarray): The image to solarize.
      threshold (int): All pixels above this greyscale level are inverted.

  Returns:
      numpy.ndarray: Solarized image.

  """
  dtype = inputs.dtype
  max_val = 255

  if dtype == np.dtype("uint8"):
    lut = [(i if i < threshold else max_val - i) for i in range(max_val + 1)]

    prev_shape = inputs.shape
    inputs = cv2.LUT(inputs, np.array(lut, dtype=dtype))

    if len(prev_shape) != len(inputs.shape):
      inputs = np.expand_dims(inputs, -1)
    return inputs

  result_img = inputs.copy()
  cond = inputs >= threshold
  result_img[cond] = max_val - result_img[cond]
  return result_img


@autotype
def posterize(inputs: np.ndarray, **kwargs):
  raise NotImplementedError(__name__)


@autotype
def rgb_shift(inputs: np.ndarray, r_shift=20, g_shift=20, b_shift=20, **kwargs):
  """Randomly shift values for each channel of the input RGB image.
  """
  inputs = to_float(inputs)
  result_img = np.empty_like(inputs)
  shifts = [r_shift, g_shift, b_shift]
  for i, shift in enumerate(shifts):
    result_img[..., i] = inputs[..., i] + shift
  return result_img


@autotype
def hsv_shift(inputs: np.ndarray, hue_shift=20, sat_shift=20, val_shift=20, **kwargs):
  inputs = to_float(inputs)

  img = cv2.cvtColor(inputs, cv2.COLOR_RGB2HSV)
  hue, sat, val = cv2.split(img)

  if hue_shift != 0:
    hue = cv2.add(hue, hue_shift)
    hue = np.mod(hue, 360)  # OpenCV fails with negative values

  if sat_shift != 0:
    sat = cv2.add(sat, sat_shift)

  if val_shift != 0:
    val = cv2.add(val, val_shift)

  img = cv2.merge((hue, sat, val))
  img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
  return img

#!<-----------------------------------------------------------------------------
#!< Related with DCT
#!<-----------------------------------------------------------------------------


@autotype
def jpeg_compress(inputs: np.ndarray, quality=90, **kwargs):
  """Compress the input image using JPEG encoding.

  Args:
      quality (int): Quality of the compression from 0 to 100 (the higher is the better). Default: 90.

  Targets:
      image

  Image types:
      uint8, float32
  """
  _, encoded_img = cv2.imencode('.jpg', inputs, (int(cv2.IMWRITE_JPEG_QUALITY), quality))
  outputs = cv2.imdecode(encoded_img, cv2.IMREAD_UNCHANGED)
  return outputs


@autotype
def sobel(inputs: np.ndarray, **kwargs):
  raise NotImplementedError(__name__)

#!<-----------------------------------------------------------------------------
#!< Related with Image Effect
#!<-----------------------------------------------------------------------------


@autotype
def add_snow(inputs: np.ndarray, **kwargs):
  raise NotImplementedError(__name__)


@autotype
def add_fog(inputs: np.ndarray, **kwargs):
  raise NotImplementedError(__name__)


@autotype
def add_rain(inputs: np.ndarray, **kwargs):
  raise NotImplementedError(__name__)


@autotype
def add_sunflare(inputs: np.ndarray, **kwargs):
  raise NotImplementedError(__name__)


@autotype
def add_shadow(inputs: np.ndarray, **kwargs):
  raise NotImplementedError(__name__)


@autotype
def add_spatter(inputs: np.ndarray, **kwargs):
  raise NotImplementedError(__name__)


@autotype
def add_ringing_overshoot(inputs: np.ndarray, **kwargs):
  raise NotImplementedError(__name__)

#!<-----------------------------------------------------------------------------
#!< Related with Image Morphology
#!<-----------------------------------------------------------------------------


@autotype
def alpha_to_trimap(inputs: np.ndarray, **kwargs):
  raise NotImplementedError(__name__)

#!<-----------------------------------------------------------------------------
#!< Related with Flip
#!<-----------------------------------------------------------------------------


@autotype
def hflip(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return np.ascontiguousarray(inputs[:, ::-1, ...])


@autotype
def vflip(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return np.ascontiguousarray(inputs[::-1, ...])


@autotype
def flip(inputs: np.ndarray, mode, **kwargs) -> np.ndarray:
  if mode == 0:
    return inputs
  elif mode == 1:
    return np.flipud(np.rot90(inputs))
  elif mode == 2:
    return np.flipud(inputs)
  elif mode == 3:
    return np.rot90(inputs, k=3)
  elif mode == 4:
    return np.flipud(np.rot90(inputs, k=2))
  elif mode == 5:
    return np.rot90(inputs)
  elif mode == 6:
    return np.rot90(inputs, k=2)
  elif mode == 7:
    return np.flipud(np.rot90(inputs, k=3))

#!<-----------------------------------------------------------------------------
#!< Related with Rotation
#!<-----------------------------------------------------------------------------


@autotype
def rotate(inputs: np.ndarray, angle, interpolation=T.RESIZE_MODE.BILINEAR,
           border_mode=T.BORDER_MODE.CONSTANT, border_value=0, **kwargs) -> np.ndarray:
  scale = 1.0
  shift = (0, 0)
  height, width = inputs.shape[:2]
  matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, scale)
  matrix[0, 2] += shift[0]
  matrix[1, 2] += shift[1]
  cv2.warpAffine(inputs,
                 M=matrix,
                 dsize=(width, height),
                 dst=inputs,
                 flags=T.RESIZE_MODE_TO_CV[interpolation],
                 borderMode=T.BORDER_MODE_TO_CV[border_mode],
                 borderValue=border_value)
  return inputs

# def _apply_affine_flow_np(flow, theta=None, t_x=0, t_y=0, zoom=1.0,
# shear=1.0, phi=0.0, interpolation=cv2.INTER_LINEAR):

#   h, w = flow.shape[:2]

#   if theta is None:
#     theta = _generate_affine_theta(t_x, t_y, zoom, shear, phi)

#   # T is similar transform matrix
#   T = np.array([[1. / (w - 1.), 0., -0.5], [0., 1. / (h - 1.), -0.5],
#                 [0., 0., 1.]], np.float32)

#   T_inv = np.linalg.inv(T)

#   # theta is affine transformations in world coordinates, with origin at top
#   # left corner of pictures and picture's width range and height range
#   # from [0, width] and [0, height].
#   theta_world = T_inv @ theta @ T

#   flow = cv2.warpAffine(flow, theta_world[:2, :], (w, h), flags=interpolation)

#   """
#   X1                 Affine(theta1)             X1'
#               x                                   x
#   theta1(-1) y           ->                      y
#               1                                   1

#   X2                 Affine(theta2)             X2'
#               x   u                                         x   u
#   theta1(-1) y + v       ->           theta2 x {theta1(-1) y + v}
#               1   0                                         1   0
#                                       flow' = X2' -X1'
#   """

#   # (u, v) -> (u, v, 0); shape (height, width, 2) -> (height, width, 3)
#   homo_flow = np.concatenate((flow, np.zeros((height, width, 1))), axis=2)

#   xx, yy = np.meshgrid(range(width), range(height))

#   # grid of homogeneous coordinates
#   homo_grid = np.stack((xx, yy, np.ones((height, width))), axis=2).astype(flow.dtype)

#   # theta2 x [u, v, 0]T + (theta2 x theta1(-1) - [1, 1, 1]) x [x, y, 1]T
#   flow_final = homo_grid @ (theta2 @ np.linalg.inv(theta1) - np.eye(3)).T + homo_flow @ theta2.T

#   return flow_final[:, :, :2]


def generate_random_affine_theta(translates, zoom, shear, rotate, preserve_valid):
  """A valid affine transform is an affine transform which guarantees the
    transformed image covers the whole original picture frame.
  """
  def is_valid(theta):
    bounds = np.array([
        [-0.5, -0.5, 1.],  # left top
        [-0.5, 0.5, 1.],  # left bottom
        [0.5, -0.5, 1.],  # right top
        [0.5, 0.5, 1.],  # right bottom
    ])
    """
    (-0.5, -0.5)          (0.5, -0.5)
                 --------
                |        |
                |        |
                |        |
                 --------
    (-0.5, 0.5)          (0.5, 0.5)
    """
    bounds = (np.linalg.inv(theta) @ bounds.T).T

    valid = ((bounds[:, :2] >= -0.5) & (bounds[:, :2] <= 0.5)).all()
    return valid

  valid = False
  theta = np.identity(3)

  while not valid:
    zoom_ = np.random.uniform(zoom[0], zoom[1])
    shear_ = np.random.uniform(shear[0], shear[1])
    t_x = np.random.uniform(-translates[0], translates[0])
    t_y = np.random.uniform(-translates[1], translates[1])
    phi = np.random.uniform(rotate[0] * np.pi / 180., rotate[1] * np.pi / 180.)
    T = generate_affine_theta(t_x, t_y, zoom_, shear_, phi)
    theta_propose = T @ theta
    if not preserve_valid:
      break
    valid = is_valid(theta_propose)

  return theta_propose


def generate_affine_theta(t_x, t_y, zoom, shear, phi):
  """generate a affine matrix
  """
  sin_phi = np.sin(phi)
  cos_phi = np.cos(phi)

  translate_mat = np.array([
      [1., 0., t_x],
      [0., 1., t_y],
      [0., 0., 1.],
  ])

  rotate_mat = np.array([
      [cos_phi, -sin_phi, 0.],
      [sin_phi, cos_phi, 0.],
      [0., 0., 1.],
  ])

  shear_mat = np.array([
      [shear, 0., 0.],
      [0., 1. / shear, 0.],
      [0., 0., 1.],
  ])

  zoom_mat = np.array([
      [zoom, 0., 0.],
      [0., zoom, 0.],
      [0., 0., 1.],
  ])

  T = translate_mat @ rotate_mat @ shear_mat @ zoom_mat
  return T


@autotype
def affine_theta(inputs: np.ndarray, theta, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs) -> np.ndarray:
  # T is similar transform matrix
  h, w = inputs.shape[:2]
  trans = np.array([[1. / (w - 1.), 0., -0.5], [0., 1. / (h - 1.), -0.5], [0., 0., 1.]], np.float32)

  trans_inv = np.linalg.inv(trans)

  # theta is affine transformations in world coordinates, with origin at top
  # left corner of pictures and picture's width range and height range
  # from [0, width] and [0, height].
  theta_world = trans_inv @ theta @ trans

  return cv2.warpAffine(inputs, theta_world[:2, :], (w, h), flags=T.RESIZE_MODE_TO_CV[interpolation])


@autotype
def affine(inputs: np.ndarray, angle: float, tx: float, ty: float, scale: float,
           shear: float, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs) -> np.ndarray:
  theta = generate_affine_theta(tx, ty, scale, shear, angle)
  return affine_theta(inputs, theta, interpolation=interpolation, **kwargs)


#!<-----------------------------------------------------------------------------
#!< Related with Padding
#!<-----------------------------------------------------------------------------

@autotype
def pad(inputs: np.ndarray, left, top, right, bottom, fill_value=0, mode='constant', **kwargs) -> np.ndarray:
  if inputs.ndim == 3:
    inputs = np.pad(inputs, ((top, bottom), (left, right), (0, 0)), mode=mode, constant_values=fill_value)
  elif inputs.ndim == 2:
    inputs = np.pad(inputs, ((top, bottom), (left, right)), mode=mode, constant_values=fill_value)
  return inputs


@autotype
def pad_to_size_divisible(inputs: np.ndarray, size_divisible, **kwargs) -> np.ndarray:
  shape = list(inputs.shape)
  shape[0] = int(math.ceil(shape[0] / size_divisible) * size_divisible)
  shape[1] = int(math.ceil(shape[1] / size_divisible) * size_divisible)
  outputs = np.zeros(shape).astype(inputs.dtype)
  outputs[:inputs.shape[0], :inputs.shape[1]] = inputs
  return outputs

#!<-----------------------------------------------------------------------------
#!< Related with Resize
#!<-----------------------------------------------------------------------------


@autotype
def resize(inputs: np.ndarray, height, width, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs) -> np.ndarray:
  return cv2.resize(inputs, dsize=(width, height), interpolation=T.RESIZE_MODE_TO_CV[interpolation])


@autotype
def downscale(inputs: np.ndarray, downscale=4.0, upscale=4.0, interpolation=T.RESIZE_MODE.NEAREST, **kwargs):
  h, w = inputs.shape[:2]
  down = resize(inputs, int(h // downscale), int(w // downscale), interpolation=interpolation)
  h, w = down.shape[:2]
  up = resize(down, int(h * upscale), int(w * upscale), interpolation=interpolation)
  return up

#!<-----------------------------------------------------------------------------
#!< Related with Crop
#!<-----------------------------------------------------------------------------


@autotype
def crop(inputs: np.ndarray, top, left, height, width, **kwargs) -> np.ndarray:
  return inputs[top: top + height, left: left + width]


@autotype
def crop_and_pad(inputs: np.ndarray,
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
                 **kwargs) -> np.ndarray:
  new_shape = list(inputs.shape)
  h, w = new_shape[:2]
  new_shape[0] = dst_height
  new_shape[1] = dst_width
  new_image = np.ones([*new_shape]).astype(inputs.dtype) * fill_value

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

  new_image[dy1:dy2, dx1:dx2] = inputs[sy1:sy2, sx1:sx2]
  return new_image


@autotype
def resized_crop(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


@autotype
def five_crop(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


@autotype
def ten_crop(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


@autotype
def non_overlap_crop_patch(inputs: np.ndarray, patch_size=32, stride=32, **kwargs) -> np.ndarray:
  h, w = inputs.shape[:2]
  patches = []
  for y in range(0, h - stride, stride):
    for x in range(0, w - stride, stride):
      patch = inputs[y: y + patch_size, x: x + patch_size]
      patches.append(patch)
  inputs = np.stack(patches, axis=0).to(inputs)
  return inputs

#!<-----------------------------------------------------------------------------
#!< Related with Pixel/Block Changing
#!<-----------------------------------------------------------------------------


@autotype
def pixel_dropout(inputs: np.ndarray, dropout_prob=0.1, per_channel=False, drop_value=0, **kwargs):
  """Set pixels to 0 with some probability.

  Args:
    dropout_prob (float): pixel drop probability. Default: 0.01
    per_channel (bool): if set to `True` drop mask will be sampled fo each channel,
        otherwise the same mask will be sampled for all channels. Default: False
    drop_value (number or sequence of numbers or None): Value that will be set in dropped place.
        If set to None value will be sampled randomly, default ranges will be used:
            - uint8 - [0, 255]
            - uint16 - [0, 65535]
            - uint32 - [0, 4294967295]
            - float, double - [0, 1]
        Default: 0

  Targets:
    image, mask

  Image types:
    any

  """
  shape = inputs.shape[:2]
  rnd = np.random.RandomState(random.randint(0, 1 << 32))
  drop_mask = rnd.choice([True, False], shape, p=[dropout_prob, 1 - dropout_prob])

  if drop_mask.ndim != inputs.ndim:
    drop_mask = np.expand_dims(drop_mask, -1)

  outputs = np.where(drop_mask, drop_value, inputs)
  return outputs


@autotype
def cutout(inputs: np.ndarray, num_holes=8, h_size=20, w_size=20, fill_value=(255, 255, 255), **kwargs):
  """CoarseDropout of the square regions in the image.

  Args:
      num_holes (int): number of regions to zero out
      max_h_size (int): maximum height of the hole
      max_w_size (int): maximum width of the hole
      fill_value (int, float, list of int, list of float): value for dropped pixels.

  Targets:
      image

  Image types:
      uint8, float32

  Reference:
  |  https://arxiv.org/abs/1708.04552
  |  https://github.com/uoguelph-mlrg/Cutout/blob/master/util/cutout.py
  |  https://github.com/aleju/imgaug/blob/master/imgaug/augmenters/arithmetic.py
  """
  height, width = inputs.shape[:2]

  holes = []
  for _ in range(num_holes):
    y = random.randint(0, height)
    x = random.randint(0, width)

    y1 = np.clip(y - h_size // 2, 0, height)
    y2 = np.clip(y1 + h_size, 0, height)
    x1 = np.clip(x - w_size // 2, 0, width)
    x2 = np.clip(x1 + w_size, 0, width)

    holes.append((x1, y1, x2, y2))

  inputs = inputs.copy()
  for x1, y1, x2, y2 in holes:
    inputs[y1:y2, x1:x2] = fill_value

  return inputs


@autotype
def channel_dropout(inputs: np.ndarray, **kwargs):
  raise NotImplementedError


@autotype
def coarse_dropout(inputs: np.ndarray, **kwargs):
  """CoarseDropout of the rectangular regions in the image.

  Args:
      max_holes (int): Maximum number of regions to zero out.
      max_height (int, float): Maximum height of the hole.
      If float, it is calculated as a fraction of the image height.
      max_width (int, float): Maximum width of the hole.
      If float, it is calculated as a fraction of the image width.
      min_holes (int): Minimum number of regions to zero out. If `None`,
          `min_holes` is be set to `max_holes`. Default: `None`.
      min_height (int, float): Minimum height of the hole. Default: None. If `None`,
          `min_height` is set to `max_height`. Default: `None`.
          If float, it is calculated as a fraction of the image height.
      min_width (int, float): Minimum width of the hole. If `None`, `min_height` is
          set to `max_width`. Default: `None`.
          If float, it is calculated as a fraction of the image width.

      fill_value (int, float, list of int, list of float): value for dropped pixels.
      mask_fill_value (int, float, list of int, list of float): fill value for dropped pixels
          in mask. If `None` - mask is not affected. Default: `None`.

  Targets:
      image, mask, keypoints

  Image types:
      uint8, float32

  Reference:
  |  https://arxiv.org/abs/1708.04552
  |  https://github.com/uoguelph-mlrg/Cutout/blob/master/util/cutout.py
  |  https://github.com/aleju/imgaug/blob/master/imgaug/augmenters/arithmetic.py
  """
  raise NotImplementedError


@autotype
def grid_dropout(inputs: np.ndarray, **kwargs):
  """GridDropout, drops out rectangular regions of an image and the corresponding mask in a grid fashion.

  Args:
      ratio (float): the ratio of the mask holes to the unit_size (same for horizontal and vertical directions).
          Must be between 0 and 1. Default: 0.5.
      unit_size_min (int): minimum size of the grid unit. Must be between 2 and the image shorter edge.
          If 'None', holes_number_x and holes_number_y are used to setup the grid. Default: `None`.
      unit_size_max (int): maximum size of the grid unit. Must be between 2 and the image shorter edge.
          If 'None', holes_number_x and holes_number_y are used to setup the grid. Default: `None`.
      holes_number_x (int): the number of grid units in x direction. Must be between 1 and image width//2.
          If 'None', grid unit width is set as image_width//10. Default: `None`.
      holes_number_y (int): the number of grid units in y direction. Must be between 1 and image height//2.
          If `None`, grid unit height is set equal to the grid unit width or image height, whatever is smaller.
      shift_x (int): offsets of the grid start in x direction from (0,0) coordinate.
          Clipped between 0 and grid unit_width - hole_width. Default: 0.
      shift_y (int): offsets of the grid start in y direction from (0,0) coordinate.
          Clipped between 0 and grid unit height - hole_height. Default: 0.
      random_offset (boolean): weather to offset the grid randomly between 0 and grid unit size - hole size
          If 'True', entered shift_x, shift_y are ignored and set randomly. Default: `False`.
      fill_value (int): value for the dropped pixels. Default = 0
      mask_fill_value (int): value for the dropped pixels in mask.
          If `None`, transformation is not applied to the mask. Default: `None`.

  Targets:
      image, mask

  Image types:
      uint8, float32

  References:
      https://arxiv.org/abs/2001.04086

  """


@autotype
def grid_shuffle(inputs: np.ndarray, **kwargs):
  raise NotImplementedError


#!<-----------------------------------------------------------------------------
#!<  Related with Composed Augmentations
#!<-----------------------------------------------------------------------------

class QualityAwareTransform():
  """Quality-aware Pre-trained Models for Blind Image Quality Assessment
  """

  def __init__(self, num_augs=5, iou_range=[0.1, 0.3], patch_size=160,
               num_order=1, num_pairs=1, method='pair_crop', **kwargs):
    """image quality transform

    Args:
        num_augs (int): number of augmentations, should be less than 26
        iou_range (list): iou range for patch extraction [min, max] (default: [0.1, 0.3])
        patch_size (int): patch size (default: 160)
        num_order (int): number of order (default: 1)
        num_pairs (int): number of pairs (default: 1)
    """
    assert method in ['pair_crop', 'single']
    self.method = method

    self.augments = [
        self.random_usm_sharpen,
        # self.random_bilateral_usm_sharpen,
        # self.random_high_contrast_sharpen,
        # self.random_photoshop_usm_sharpen,
        self.random_gaussian_blur,
        self.random_motion_blur,
        self.random_median_blur,
        self.random_glass_blur,
        self.random_advanced_blur,
        self.random_defocus_blur,
        self.random_zoom_blur,
        self.random_iso_noise,
        self.random_gaussian_color_noise,
        self.random_gaussian_gray_noise,
        # self.random_poisson_noise,
        self.random_multiplicative_noise,
        self.random_add_brightness,
        self.random_reduce_brightness,
        self.random_add_contrast,
        self.random_reduce_contrast,
        self.random_add_gamma,
        self.random_reduce_gamma,
        self.random_add_hue,
        self.random_reduce_hue,
        self.random_add_saturation,
        self.random_reduce_saturation,
        self.random_jpeg_compress,
        self.random_downscale_nearest,
        self.random_downscale_bilinear,
        self.random_downscale_bicubic,
    ]
    assert num_augs <= len(self.augments)
    self.num_augs = num_augs
    self.iou_range = iou_range
    self.patch_size = patch_size
    self.num_order = num_order
    self.num_pairs = num_pairs

  #!<---------------------------------------------------------------------------
  #!< Related with Shapren
  #!<---------------------------------------------------------------------------

  def random_usm_sharpen(self, x, coeffs=[0.5, 0.7, 0.9, 1.1, 1.3], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.usm_sharpen(x, coeff=coeffs[ids]), ids

  def random_bilateral_usm_sharpen(self, x, coeffs=[1.2, 1.4, 1.6, 1.8, 2.0], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.bilateral_usm_sharpen(x, coeff=coeffs[ids]), ids

  def random_high_contrast_sharpen(self, x, coeffs=[1.2, 1.4, 1.6, 1.8, 2.0], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.high_contrast_sharpen(x, coeff=coeffs[ids]), ids

  def random_photoshop_usm_sharpen(self, x, coeffs=[0.5, 0.7, 0.9, 1.1, 1.3], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.photoshop_usm_sharpen(x, amount=coeffs[ids]), ids

  #!<---------------------------------------------------------------------------
  #!< Related with Blur
  #!<---------------------------------------------------------------------------

  def random_gaussian_blur(self, x, coeffs=[0.5, 1.0, 1.5, 2.0, 2.5], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.gaussian_blur(x, sigma=coeffs[ids]), ids

  def random_motion_blur(self, x, coeffs=[(0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0)], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.motion_blur(x, dist_range=coeffs[ids]), ids

  def random_median_blur(self, x, coeffs=[3, 5, 7, 9, 11], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.median_blur(x, kernel_size=coeffs[ids]), ids

  def random_glass_blur(self, x, coeffs=[(0.1, 1), (0.3, 2), (0.5, 3), (0.7, 4), (0.9, 5)], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.glass_blur(x, sigma=coeffs[ids][0], max_delta=coeffs[ids][1], iterations=1), ids

  def random_advanced_blur(self, x, coeffs=[0.5, 1.0, 1.5, 2.0, 2.5], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.advanced_blur(x, kernel_size=7, sigma=coeffs[ids]), ids

  def random_defocus_blur(self, x, coeffs=[3, 4, 5, 6, 7], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.defocus_blur(x, radius=coeffs[ids]), ids

  def random_zoom_blur(self, x, coeffs=[1.02, 1.04, 1.06, 1.08, 1.1], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.zoom_blur(x, zoom_factor=coeffs[ids], step_factor=0.01), ids

  #!<---------------------------------------------------------------------------
  #!< Related with Noise/Denoise
  #!<---------------------------------------------------------------------------

# noise
  def random_iso_noise(self, x, coeffs=[(0.01, 0.1), (0.015, 0.3), (0.02, 0.5), (0.025, 0.7), (0.03, 0.9)], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.iso_noise(x, color_shift=coeffs[ids][0], intensity=coeffs[ids][1]), ids

  def random_gaussian_color_noise(self, x, coeffs=[(0, 4), (0, 8), (0, 12), (0, 16), (0, 18)], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.gaussian_noise(x, mean=coeffs[ids][0], std=coeffs[ids][1], per_channel=True), ids

  def random_gaussian_gray_noise(self, x, coeffs=[(0, 4), (0, 8), (0, 12), (0, 16), (0, 18)], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.gaussian_noise(x, mean=coeffs[ids][0], std=coeffs[ids][1], per_channel=False), ids

  # def random_poisson_noise(self, x, coeffs=[8, 16, 24, 32, 40], ids=None):
  #   ids = random.choice(range(len(coeffs))) if ids is None else ids
  #   return tw.transform.poisson_noise(x, lam=coeffs[ids]), ids

  def random_multiplicative_noise(
          self, x, coeffs=[(0.95, 1.05), (0.90, 1.10), (0.85, 1.15), (0.80, 1.20), (0.75, 1.25)], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.multiplicative_noise(x, multiplier=coeffs[ids]), ids

  #!<---------------------------------------------------------------------------
  #!< Related with Color
  #!<---------------------------------------------------------------------------

  def random_add_brightness(self, x, coeffs=[1.05, 1.10, 1.15, 1.20, 1.25], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.adjust_brightness(x, factor=coeffs[ids]), ids

  def random_reduce_brightness(self, x, coeffs=[0.95, 0.90, 0.85, 0.80, 0.75], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.adjust_brightness(x, factor=coeffs[ids]), ids

  def random_add_contrast(self, x, coeffs=[1.05, 1.10, 1.15, 1.20, 1.25], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.adjust_contrast(x, factor=coeffs[ids]), ids

  def random_reduce_contrast(self, x, coeffs=[0.95, 0.90, 0.85, 0.80, 0.75], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.adjust_contrast(x, factor=coeffs[ids]), ids

  def random_add_gamma(self, x, coeffs=[1.025, 1.05, 1.075, 1.10, 1.125], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.adjust_gamma(x, factor=coeffs[ids]), ids

  def random_reduce_gamma(self, x, coeffs=[0.95, 0.925, 0.90, 0.875, 0.85], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.adjust_gamma(x, factor=coeffs[ids]), ids

  def random_add_hue(self, x, coeffs=[1.01, 1.02, 1.03, 1.04, 1.05], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.adjust_hue(x, factor=coeffs[ids]), ids

  def random_reduce_hue(self, x, coeffs=[0.99, 0.98, 0.97, 0.96, 0.95], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.adjust_hue(x, factor=coeffs[ids]), ids

  def random_add_saturation(self, x, coeffs=[1.1, 1.2, 1.3, 1.4, 1.5], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.adjust_saturation(x, factor=coeffs[ids]), ids

  def random_reduce_saturation(self, x, coeffs=[0.9, 0.8, 0.7, 0.6, 0.5], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.adjust_saturation(x, factor=coeffs[ids]), ids

  #!<---------------------------------------------------------------------------
  #!< Related with DCT
  #!<---------------------------------------------------------------------------

  def random_jpeg_compress(self, x, coeffs=[90, 70, 50, 30, 10], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    return tw.transform.jpeg_compress(x, quality=coeffs[ids]), ids

  #!<---------------------------------------------------------------------------
  #!< Related with Resize
  #!<---------------------------------------------------------------------------

  def random_downscale_nearest(self, x, coeffs=[2.0, 2.5, 3.0, 3.5, 4.0], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    ih, iw = x.shape[:2]
    aug = tw.transform.downscale(x, downscale=coeffs[ids], upscale=coeffs[ids],
                                 interpolation=tw.transform.RESIZE_MODE.NEAREST)
    oh, ow = aug.shape[:2]
    if ih != oh or iw != ow:
      aug = tw.transform.resize(aug, height=ih, width=iw, interpolation=tw.transform.RESIZE_MODE.NEAREST)
    return aug, ids

  def random_downscale_bilinear(self, x, coeffs=[2.0, 2.5, 3.0, 3.5, 4.0], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    ih, iw = x.shape[:2]
    aug = tw.transform.downscale(x, downscale=coeffs[ids], upscale=coeffs[ids],
                                 interpolation=tw.transform.RESIZE_MODE.BILINEAR)
    oh, ow = aug.shape[:2]
    if ih != oh or iw != ow:
      aug = tw.transform.resize(aug, height=ih, width=iw, interpolation=tw.transform.RESIZE_MODE.BILINEAR)
    return aug, ids

  def random_downscale_bicubic(self, x, coeffs=[2.0, 2.5, 3.0, 3.5, 4.0], ids=None):
    ids = random.choice(range(len(coeffs))) if ids is None else ids
    ih, iw = x.shape[:2]
    aug = tw.transform.downscale(x, downscale=coeffs[ids], upscale=coeffs[ids],
                                 interpolation=tw.transform.RESIZE_MODE.BICUBIC)
    oh, ow = aug.shape[:2]
    if ih != oh or iw != ow:
      aug = tw.transform.resize(aug, height=ih, width=iw, interpolation=tw.transform.RESIZE_MODE.BICUBIC)
    return aug, ids

  #!<---------------------------------------------------------------------------
  #!< OLA crop
  #!<---------------------------------------------------------------------------

  def random_twocrops_with_overlap(self, image, patch_size=160, low_iou_threshold=0.1, high_iou_threshold=0.3):
    """
    """
    min_side, max_side = math.sqrt(low_iou_threshold), math.sqrt(high_iou_threshold)
    image_height, image_width = image.shape[:2]
    out_size = int(patch_size * (1 - min_side))

    max_out_size = out_size * 2 + patch_size
    valid_height = min(max_out_size, image_height)
    valid_width = min(max_out_size, image_width)

    loop = 1
    count = 0
    while True:
      # valid_y = random.randint(0, image_height - patch_size)
      # valid_x = random.randint(0, image_width - patch_size)

      out_y1 = random.randint(0, 0 + image_height - patch_size)
      out_x1 = random.randint(0, 0 + image_width - patch_size)

      out_y2 = random.randint(0, 0 + image_height - patch_size)
      out_x2 = random.randint(0, 0 + image_width - patch_size)

      count += 1
      if count == 50:
        out_x1, out_y1, out_x2, out_y2 = 0, 0, 0, 0
        tw.logger.warn(f'failed to find suitable crops in h:{image_height}, w:{image_width}')
        break

      if out_x1 + patch_size > image_width or out_y1 + patch_size > image_height or \
              out_x2 + patch_size > image_width or out_y2 + patch_size > image_height:
        continue

      # Compute IoU between two patches
      x1 = max(out_x1, out_x2)
      y1 = max(out_y1, out_y2)
      x2 = min(out_x1 + patch_size, out_x2 + patch_size)
      y2 = min(out_y1 + patch_size, out_y2 + patch_size)
      intersection = max(0, x2 - x1) * max(0, y2 - y1)
      iou = intersection / (patch_size * patch_size * 2 - intersection)

      if high_iou_threshold >= iou >= low_iou_threshold:
        break
      loop += 1

    crop1 = image[out_y1:out_y1 + patch_size, out_x1:out_x1 + patch_size]
    crop2 = image[out_y2:out_y2 + patch_size, out_x2:out_x2 + patch_size]

    return crop1, crop2

  #!<---------------------------------------------------------------------------
  #!< Test
  #!<---------------------------------------------------------------------------

  def test_augments(self, image_path='cases/140_1816049640_296703045_20220926-000849_540x960.png'):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    for aug in self.augments:
      print(aug.__name__)
      outs = [img, ]
      for ids in range(5):
        outs.append(aug(img, ids=ids)[0])
      outs = np.concatenate(outs, axis=1)
      if outs.dtype in [np.float32, np.float64]:
        outs = tw.transform.to_round_uint8(outs)
      cv2.imwrite(f'quality_transform_{aug.__name__}.png', cv2.cvtColor(outs, cv2.COLOR_RGB2BGR))

  def test_crops(self, image_path='cases/140_1816049640_296703045_20220926-000849_540x960.png'):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    samples = self(img)
    for i, (crop1, crop2, labels) in enumerate(samples):
      for label in labels.items():
        print(label)
      print(crop1.shape, crop2.shape)
      outs = np.concatenate([crop1, crop2], axis=1)
      cv2.imwrite(f'quality_transform_crop_pairs_{i}.png', cv2.cvtColor(outs, cv2.COLOR_RGB2BGR))

  #!<---------------------------------------------------------------------------
  #!< Call
  #!<---------------------------------------------------------------------------

  def generate_single(self, x):
    """image quality augmentation

      1) randomly select a subset of augmentations (skip / shuffle)
      2) repeat multiple times (num_order)
      3) randomly select two crops with different augmentations (num_pairs)
    """
    if isinstance(x, Image.Image):
      x = np.array(x)

    num_augs = self.num_augs
    # iou_low, iou_high = self.iou_range
    # patch_size = self.patch_size
    # num_order = self.num_order
    # num_pairs = self.num_pairs

    # record augment value
    labels = OrderedDict()
    for augment in self.augments:
      labels[augment.__name__] = 0

    # simluate randomly skip / shuffle / repeitive
    augments = random.choices(self.augments, k=num_augs)

    # augment
    aug_x = x.copy()
    for augment in augments:
      aug_x, label = augment(aug_x)
      # make sure aug_x also range in [0, 255]
      aug_x = np.clip(aug_x, 0, 255)
      labels[augment.__name__] = label

    return aug_x, labels

  def generate_pair_crops(self, x):
    """generate single image
    """
    if isinstance(x, Image.Image):
      x = np.array(x)

    num_augs = self.num_augs
    iou_low, iou_high = self.iou_range
    patch_size = self.patch_size
    num_order = self.num_order
    num_pairs = self.num_pairs
    samples = []

    for _ in range(num_pairs):
      # record augment value
      labels = OrderedDict()
      for augment in self.augments:
        labels[augment.__name__] = 0

      # simluate randomly skip / shuffle / repeitive
      augments = random.choices(self.augments, k=num_augs)

      # augment
      aug_x = x.copy()
      for augment in augments:
        aug_x, label = augment(aug_x)
        # make sure aug_x also range in [0, 255]
        aug_x = np.clip(aug_x, 0, 255)
        labels[augment.__name__] = label

      # select two crops with certain overlapping
      crop1, crop2 = self.random_twocrops_with_overlap(
          image=aug_x,
          patch_size=patch_size,
          low_iou_threshold=iou_low,
          high_iou_threshold=iou_high)

      samples.append((crop1, crop2, labels))

    return samples

  def __call__(self, x):
    if self.method == 'pair_crop':
      return self.generate_pair_crops(x)
    elif self.method == 'single':
      return self.generate_single(x)
    else:
      raise NotImplementedError(self.method)


def quality_aware_transforms(inputs, num_augs=5, iou_range=[
                             0.1, 0.3], patch_size=160, num_order=1, num_pairs=1, method='pair_crop', **kwargs):
  """image quality-awared transforms

  Returns:
    [
      [aug1-crop1, aug1-crop2, aug1-labels],
      [aug2-crop1, aug2-corp2, aug2-labels],
      ...
    ]

  """
  transform = QualityAwareTransform(num_augs=num_augs,
                                    iou_range=iou_range,
                                    patch_size=patch_size,
                                    num_order=num_order,
                                    num_pairs=num_pairs,
                                    method=method,
                                    **kwargs)
  return transform(inputs)
