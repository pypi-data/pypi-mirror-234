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
import functools

from PIL import Image
import numpy as np

import torch

import tw
from tw import transform as T

from . import functional_np as F_np
from . import functional_pil as F_pil
from . import functional_tensor as F_t


def supports(support=[np.ndarray, Image.Image, torch.Tensor, T.MetaBase], *args, **kwargs):
  """Decorator for supplying meta actions.

    1. convert single meta into list of metas
    2. select user-specific meta index to augment
    3. checking if current augment to allow meta type pass.
    4. shape checking

  """
  def wrapper(transform):
    @functools.wraps(transform)
    def kernel(inputs, *args, **kwargs):
      # convert metabase to list
      if isinstance(inputs, T.MetaBase):
        inputs = [inputs]

      # allow class
      if len(support) > 0:
        # for [metabase, ]
        if isinstance(inputs, (list, tuple)):
          for inp in inputs:
            assert isinstance(inp, tuple(support)), f"Failed to find {type(inp)} in {support} on {transform}."
        else:
          assert isinstance(inputs, tuple(support)), f"Failed to find {type(inputs)} in {support} on {transform}."

      # check shape
      if isinstance(inputs, np.ndarray):
        assert inputs.ndim in [1, 2, 3], "inputs should be [N], [H, W], [H, W, C]."
      elif isinstance(inputs, torch.Tensor):
        assert inputs.ndim in [2, 3, 4], "inputs should be [B, C, H, W], [C, H, W], [H, W]"

      # there should not be metabase
      assert not isinstance(inputs, T.MetaBase)

      # doing for meta-class
      if isinstance(inputs, (list, tuple)):
        # all input in inputs has same seed.
        seed = random.randint(0, 2 ** 64)
        for meta in inputs:
          random.seed(seed)
          if hasattr(meta, transform.__name__):
            getattr(meta, transform.__name__)(*args, **kwargs)
          else:
            tw.logger.warn(f'{meta.__class__.__name__} does not implement {transform.__name__} method.')
        return default_return_meta(inputs, *args, **kwargs)

      return transform(inputs, *args, **kwargs)
    return kernel
  return wrapper


def default_return_meta(inputs, *args, **kwargs):
  return inputs


def get_inputs_hw(inputs):
  """get inputs h, w size
  """
  if isinstance(inputs, np.ndarray):
    h, w = inputs.shape[:2]
  elif isinstance(inputs, Image.Image):
    h, w = inputs.height, inputs.width
  elif isinstance(inputs, torch.Tensor):
    if inputs.ndim in [2, 3, 4, 5]:
      h, w = inputs.shape[-2:]
    else:
      raise NotImplementedError
  return h, w


def process(func, inputs, *args, **kwargs):
  """process by inputs type
  """
  if isinstance(inputs, np.ndarray):
    return getattr(F_np, func)(inputs, *args, **kwargs)
  elif isinstance(inputs, Image.Image):
    return getattr(F_pil, func)(inputs, *args, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return getattr(F_t, func)(inputs, *args, **kwargs)
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< DATA TYPE CONVERSION
#!<-----------------------------------------------------------------------------


@supports()
def to_float(inputs, **kwargs):
  return process('to_float', inputs, **kwargs)


@supports()
def to_round_uint8(inputs, **kwargs):
  return process('to_round_uint8', inputs, **kwargs)


@supports()
def to_data_range(inputs, src_range, dst_range, **kwargs):
  if src_range == dst_range:
    return inputs
  return process('to_data_range',
                 inputs,
                 src_range=src_range,
                 dst_range=dst_range,
                 **kwargs)


@supports()
def to_tensor(inputs, scale=None, mean=None, std=None, **kwargs):
  return process('to_tensor',
                 inputs,
                 scale=scale,
                 mean=mean,
                 std=std,
                 **kwargs)


@supports()
def to_pil(inputs, **kwargs):
  return process('to_pil', inputs, **kwargs)


@supports()
def to_numpy(inputs, **kwargs):
  return process('to_numpy', inputs, **kwargs)


#!<-----------------------------------------------------------------------------
#!< COLORSPACE
#!<-----------------------------------------------------------------------------


@supports()
def change_colorspace(inputs, src: T.COLORSPACE, dst: T.COLORSPACE, **kwargs):
  return process('change_colorspace', inputs, src=src, dst=dst, **kwargs)


@supports()
def to_color(inputs, **kwargs):
  return process('to_color', inputs, **kwargs)


@supports()
def to_grayscale(inputs, **kwargs):
  return process('to_grayscale', inputs, **kwargs)


@supports()
def rgb_to_yuv709v(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  outputs = process('rgb_to_yuv709v', inputs, data_range=data_range, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def bgr_to_yuv709v(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  inputs = change_colorspace(inputs, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
  outputs = process('rgb_to_yuv709v', inputs, data_range=data_range, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def bgr_to_yuv709f(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  inputs = change_colorspace(inputs, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
  outputs = process('rgb_to_yuv709f', inputs, data_range=data_range, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def rgb_to_yuv709f(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  outputs = process('rgb_to_yuv709f', inputs, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def yuv709v_to_rgb(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  outputs = process('yuv709v_to_rgb', inputs, data_range=data_range, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def yuv709f_to_rgb(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  outputs = process('yuv709f_to_rgb', inputs, data_range=data_range, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def rgb_to_bgr(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  outputs = process('rgb_to_bgr', inputs, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def bgr_to_rgb(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  outputs = process('bgr_to_rgb', inputs, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def rgb_to_yuv601v(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  outputs = process('rgb_to_yuv601v', inputs, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def rgb_to_yuv601f(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  outputs = process('rgb_to_yuv601f', inputs, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def yuv601v_to_rgb(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  outputs = process('yuv601v_to_rgb', inputs, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def yuv601f_to_rgb(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  outputs = process('yuv601f_to_rgb', inputs, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def rgb_to_yuv601(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  outputs = process('rgb_to_yuv601', inputs, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def yuv601_to_rgb(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  outputs = process('yuv601_to_rgb', inputs, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def rgb_to_yiq(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  outputs = process('rgb_to_yiq', inputs, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def rgb_to_lhm(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=255.0)
  outputs = process('rgb_to_lhm', inputs, **kwargs)
  return to_data_range(outputs, src_range=255.0, dst_range=data_range)


@supports()
def rgb_to_xyz(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, src_range=data_range, dst_range=1.0)
  outputs = process('rgb_to_xyz', inputs, **kwargs)
  return to_data_range(outputs, src_range=1.0, dst_range=data_range)


@supports()
def xyz_to_lab(inputs, **kwargs):
  return process('xyz_to_lab', inputs, **kwargs)


@supports()
def rgb_to_lab(inputs, data_range=255.0, **kwargs):
  return xyz_to_lab(rgb_to_xyz(inputs, data_range=data_range, **kwargs), **kwargs)


@supports()
def yuv420_to_yuv444(inputs, height, width, interpolation: T.RESIZE_MODE, **kwargs):
  return process('yuv420_to_yuv444',
                 inputs,
                 height=height,
                 width=width,
                 interpolation=interpolation,
                 **kwargs)


@supports()
def yuv444_to_yuv420(inputs, height, width, interpolation: T.RESIZE_MODE, **kwargs):
  return process('yuv444_to_yuv420',
                 inputs,
                 height=height,
                 width=width,
                 interpolation=interpolation,
                 **kwargs)


#!<-----------------------------------------------------------------------------
#!< Related with Shapren
#!<-----------------------------------------------------------------------------


@supports()
def usm_sharpen(inputs, kernel_size=3, sigma=0.8, coeff=0.5, **kwargs):
  return process('usm_sharpen',
                 inputs,
                 kernel_size=kernel_size,
                 sigma=sigma,
                 coeff=coeff,
                 **kwargs)


@supports()
def bilateral_usm_sharpen(inputs, kernel_size=3, sigma_blur=0.8, sigma_color=10, sigma_space=1, coeff=1.2, **kwargs):
  return process('bilateral_usm_sharpen',
                 inputs,
                 kernel_size=kernel_size,
                 sigma_blur=sigma_blur,
                 sigma_color=sigma_color,
                 sigma_space=sigma_space,
                 coeff=coeff,
                 **kwargs)


@supports()
def adaptive_usm_sharpen(inputs, **kwargs):
  raise NotImplementedError


@supports()
def high_contrast_sharpen(inputs, sigma_color=10, sigma_space=1, coeff=2.0, **kwargs):
  return process('high_contrast_sharpen',
                 inputs,
                 sigma_color=sigma_color,
                 sigma_space=sigma_space,
                 coeff=coeff,
                 **kwargs)


@supports()
def photoshop_usm_sharpen(inputs, kernel_size=5, sigma=1.5, amount=0.5, **kwargs):
  return process('photoshop_usm_sharpen',
                 inputs,
                 kernel_size=kernel_size,
                 sigma=sigma,
                 amount=amount,
                 **kwargs)


#!<-----------------------------------------------------------------------------
#!< Related with Blur
#!<-----------------------------------------------------------------------------


@supports()
def gaussian_blur(inputs, kernel_size=3, sigma=0, **kwargs):
  return process('gaussian_blur',
                 inputs,
                 kernel_size=kernel_size,
                 sigma=sigma,
                 **kwargs)


@supports()
def motion_blur(inputs, kernel_size=7, allow_shifted=False, dist_range=None, **kwargs):
  return process('motion_blur',
                 inputs,
                 kernel_size=kernel_size,
                 allow_shifted=allow_shifted,
                 dist_range=dist_range,
                 **kwargs)


@supports()
def median_blur(inputs, kernel_size=3, **kwargs):
  return process('median_blur',
                 inputs,
                 kernel_size=kernel_size,
                 **kwargs)


@supports()
def glass_blur(inputs, sigma=0.7, max_delta=4, iterations=2, mode='fast', **kwargs):
  return process('glass_blur',
                 inputs,
                 sigma=sigma,
                 max_delta=max_delta,
                 iterations=iterations,
                 mode=mode,
                 **kwargs)


@supports()
def advanced_blur(inputs, kernel_size=3, sigma=0.8, rotate=0, beta=1.0, noise=(0.75, 1.25), **kwargs):
  return process('advanced_blur',
                 inputs,
                 kernel_size=kernel_size,
                 sigma=sigma,
                 rotate=rotate,
                 beta=beta,
                 noise=noise,
                 **kwargs)


@supports()
def defocus_blur(inputs, radius=3, alias_blur=0.1, **kwargs):
  return process('defocus_blur',
                 inputs,
                 radius=radius,
                 alias_blur=alias_blur,
                 **kwargs)


@supports()
def zoom_blur(inputs, zoom_factor=1.1, step_factor=0.01, **kwargs):
  return process('zoom_blur',
                 inputs,
                 zoom_factor=zoom_factor,
                 step_factor=step_factor,
                 **kwargs)

#!<-----------------------------------------------------------------------------
#!< Related with Noise/Denoise
#!<-----------------------------------------------------------------------------


@supports()
def iso_noise(inputs, color_shift=0.01, intensity=0.1, **kwargs):
  return process('iso_noise',
                 inputs,
                 color_shift=color_shift,
                 intensity=intensity,
                 **kwargs)


@supports()
def gaussian_noise(inputs, mean=0, std=0.01, per_channel=True, **kwargs):
  return process('gaussian_noise',
                 inputs,
                 mean=mean,
                 std=std,
                 per_channel=per_channel,
                 **kwargs)


@supports()
def poisson_noise(inputs, lam=1.0, per_channel=True, elementwise=True, **kwargs):
  return process('poisson_noise',
                 inputs,
                 lam=lam,
                 per_channel=per_channel,
                 elementwise=elementwise,
                 **kwargs)


@supports()
def multiplicative_noise(inputs, multiplier=(0.9, 1.1), per_channel=True, elementwise=True, **kwargs):
  return process('multiplicative_noise',
                 inputs,
                 multiplier=multiplier,
                 per_channel=per_channel,
                 elementwise=elementwise,
                 **kwargs)

#!<-----------------------------------------------------------------------------
#!< Related with Color
#!<-----------------------------------------------------------------------------


@supports()
def adjust_sharpness(inputs, factor=1.0, **kwargs):
  return process('adjust_sharpness',
                 inputs,
                 factor=factor,
                 **kwargs)


@supports()
def adjust_brightness(inputs, factor=1.0, **kwargs):
  return process('adjust_brightness',
                 inputs,
                 factor=factor,
                 **kwargs)


@supports()
def adjust_contrast(inputs, factor=1.0, **kwargs):
  return process('adjust_contrast',
                 inputs,
                 factor=factor,
                 **kwargs)


@supports()
def adjust_gamma(inputs, factor=1.0, gain=1.0, **kwargs):
  return process('adjust_gamma',
                 inputs,
                 factor=factor,
                 gain=gain,
                 **kwargs)


@supports()
def adjust_hue(inputs, factor=1.0, **kwargs):
  return process('adjust_hue',
                 inputs,
                 factor=factor,
                 **kwargs)


@supports()
def adjust_saturation(inputs, factor=1.0, gamma=0.0, **kwargs):
  return process('adjust_saturation',
                 inputs,
                 factor=factor,
                 gamma=gamma,
                 **kwargs)


@supports()
def photometric_distortion(inputs,
                           brightness_delta=32,
                           contrast_range=(0.5, 1.5),
                           saturation_range=(0.5, 1.5),
                           hue_delta=18,
                           **kwargs):
  return process('photometric_distortion',
                 inputs,
                 brightness_delta=brightness_delta,
                 contrast_range=contrast_range,
                 saturation_range=saturation_range,
                 hue_delta=hue_delta,
                 **kwargs)

#!<-----------------------------------------------------------------------------
#!< Related with Image Tone Changing
#!<-----------------------------------------------------------------------------


@supports()
def equal_hist(inputs, **kwargs):
  return process('equal_hist', inputs, **kwargs)


@supports()
def match_hist(inputs, **kwargs):
  return process('match_hist', inputs, **kwargs)


@supports()
def truncated_standardize(inputs, **kwargs):
  return process('truncated_standardize', inputs, **kwargs)


@supports()
def local_contrast_normalize(inputs, **kwargs):
  return process('local_contrast_normalize', inputs, **kwargs)


@supports()
def change_tone_curve(inputs, low=0.25, high=0.75, **kwargs):
  return process('change_tone_curve', inputs, low=low, high=high, **kwargs)


@supports()
def clahe(inputs, clip_limit=4.0, tile_grid_size=(8, 8), **kwargs):
  return process('clahe',
                 inputs,
                 clip_limit=clip_limit,
                 tile_grid_size=tile_grid_size,
                 **kwargs)


@supports()
def homomorphic(inputs, **kwargs):
  return process('homomorphic', inputs, **kwargs)


@supports()
def sepia(inputs, alpha=1.0, **kwargs):
  return process('sepia', inputs, alpha=alpha, **kwargs)


@supports()
def solarize(inputs, threshold=128, **kwargs):
  return process('solarize', inputs, threshold=threshold, **kwargs)


@supports()
def posterize(inputs, **kwargs):
  return process('posterize', inputs, **kwargs)


@supports()
def rgb_shift(inputs, r_shift=20, g_shift=20, b_shift=20, **kwargs):
  return process('rgb_shift',
                 inputs,
                 r_shift=r_shift,
                 g_shift=g_shift,
                 b_shift=b_shift,
                 **kwargs)


@supports()
def hsv_shift(inputs, hue_shift=20, sat_shift=20, val_shift=20, **kwargs):
  return process('hsv_shift',
                 inputs,
                 hue_shift=hue_shift,
                 sat_shift=sat_shift,
                 val_shift=val_shift,
                 **kwargs)

#!<-----------------------------------------------------------------------------
#!< Related with DCT
#!<-----------------------------------------------------------------------------


@supports()
def jpeg_compress(inputs, quality=90, **kwargs):
  return process('jpeg_compress', inputs, quality=quality, **kwargs)


@supports()
def sobel(inputs, **kwargs):
  return process('sobel', inputs, **kwargs)

#!<-----------------------------------------------------------------------------
#!< Related with Image Effect
#!<-----------------------------------------------------------------------------


@supports()
def add_snow(inputs, **kwargs):
  return process('add_snow', inputs, **kwargs)


@supports()
def add_fog(inputs, **kwargs):
  return process('add_fog', inputs, **kwargs)


@supports()
def add_rain(inputs, **kwargs):
  return process('add_rain', inputs, **kwargs)


@supports()
def add_sunflare(inputs, **kwargs):
  return process('add_sunflare', inputs, **kwargs)


@supports()
def add_shadow(inputs, **kwargs):
  return process('add_shadow', inputs, **kwargs)


@supports()
def add_spatter(inputs, **kwargs):
  return process('add_spatter', inputs, **kwargs)


@supports()
def add_ringing_overshoot(inputs, **kwargs):
  return process('add_ringing_overshoot', inputs, **kwargs)

#!<-----------------------------------------------------------------------------
#!< Related with Image Morphology
#!<-----------------------------------------------------------------------------


@supports()
def alpha_to_trimap(inputs, **kwargs):
  return process('alpha_to_trimap', inputs, **kwargs)


#!<-----------------------------------------------------------------------------
#!< Related with Flip
#!<-----------------------------------------------------------------------------


@supports()
def hflip(inputs, **kwargs):
  return process('hflip', inputs, **kwargs)


@supports()
def random_hflip(inputs, p=0.5, **kwargs):
  if random.random() > p:
    return hflip(inputs, **kwargs)
  return inputs


@supports()
def vflip(inputs, **kwargs):
  return process('vflip', inputs, **kwargs)


@supports()
def random_vflip(inputs, p=0.5, **kwargs):
  if random.random() > p:
    return vflip(inputs, **kwargs)
  return inputs


@supports()
def flip(inputs, mode, **kwargs):
  return process('flip', inputs, mode=mode, **kwargs)

#!<-----------------------------------------------------------------------------
#!< Related with Rotation
#!<-----------------------------------------------------------------------------


@supports()
def rotate(inputs, angle, interpolation=T.RESIZE_MODE.BILINEAR,
           border_mode=T.BORDER_MODE.CONSTANT, border_value=0, **kwargs):
  return process('rotate',
                 inputs,
                 angle=angle,
                 interpolation=interpolation,
                 border_mode=border_mode,
                 border_value=border_value,
                 **kwargs)


@supports()
def random_rotate(inputs, angle_range=(-30, 30), interpolation=T.RESIZE_MODE.BILINEAR,
                  border_mode=T.BORDER_MODE.CONSTANT, border_value=0, **kwargs):
  angle = random.uniform(angle_range[0], angle_range[1])
  return rotate(inputs,
                angle=angle,
                interpolation=interpolation,
                border_mode=border_mode,
                border_value=border_value,
                **kwargs)


@supports()
def affine(inputs, angle: float, tx: float, ty: float, scale: float,
           shear: float, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
  return process('affine',
                 inputs,
                 angle=angle,
                 tx=tx,
                 ty=ty,
                 scale=scale,
                 shear=shear,
                 interpolation=interpolation,
                 **kwargs)


@supports()
def affine_theta(inputs, theta, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
  return process('affine_theta',
                 inputs,
                 theta=theta,
                 interpolation=interpolation,
                 **kwargs)


@supports()
def random_affine(inputs, translates=(0.05, 0.05), zoom=(1.0, 1.5), shear=(0.86, 1.16),
                  rotate=(-10., 10.), preserve_valid=True, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
  theta = F_np._generate_random_affine_theta(translates, zoom, shear, rotate, preserve_valid)
  return affine_theta(inputs, theta, interpolation=interpolation, **kwargs)


#!<-----------------------------------------------------------------------------
#!< Related with Padding
#!<-----------------------------------------------------------------------------

@supports()
def pad(inputs, left, top, right, bottom, fill_value=0, mode='constant', **kwargs):
  return process('pad',
                 inputs,
                 left=left,
                 top=top,
                 right=right,
                 bottom=bottom,
                 fill_value=fill_value,
                 mode=mode,
                 **kwargs)


@supports()
def pad_to_size_divisible(inputs, size_divisible=32, **kwargs):
  return process('pad_to_size_divisible',
                 inputs,
                 size_divisible=size_divisible,
                 **kwargs)


@supports()
def pad_to_square(inputs, fill_value=0, **kwargs):
  """pad input to square (old image located on left top of new image.)

  Args:
      fill_value (int, optional): [description]. Defaults to 0.

  """
  h, w = get_inputs_hw(inputs)
  long_side = max(w, h)
  w_pad = w - long_side
  h_pad = h - long_side
  return pad(inputs, left=0, right=w_pad, top=0, bottom=h_pad, fill_value=fill_value, **kwargs)


@supports()
def pad_to_target_size(inputs, height, width, fill_value=0, **kwargs):
  h, w = get_inputs_hw(inputs)
  assert height >= h and width >= w
  h_pad = height - h
  w_pad = width - w
  return pad(inputs, left=0, right=w_pad, top=0, bottom=h_pad, fill_value=fill_value, **kwargs)

#!<-----------------------------------------------------------------------------
#!< Related with Resize
#!<-----------------------------------------------------------------------------


@supports()
def resize(inputs, height, width, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
  """resize to given size
  """
  return process('resize',
                 inputs,
                 height=height,
                 width=width,
                 interpolation=interpolation,
                 **kwargs)


@supports()
def random_resize(inputs, scale_range=(1, 4), interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
  """random resize inputs with aspect ratio.
  """
  _min, _max = scale_range
  scale = random.random() * (_max - _min) + _min
  h, w = get_inputs_hw(inputs)
  return resize(inputs,
                height=int(h * scale),
                width=int(w * scale),
                interpolation=interpolation,
                **kwargs)


@supports()
def shortside_resize(inputs, min_size=256, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
  """inputs will be aspect sized by short side to min_size.

  Args:
      inputs ([type]): [description]
      min_size (int): image will aspect resize according to short side size.
      interpolation ([type], optional): [description]. Defaults to .INTER_LINEAR.

  Returns:
      [type]: [description]
  """
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

  h, w = get_inputs_hw(inputs)
  oh, ow = _get_shortside_shape(h, w, min_size)

  return resize(inputs, height=oh, width=ow, interpolation=interpolation, **kwargs)


@supports()
def adaptive_resize(inputs, height, width, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
  """resize image make it less than target height and width
  """
  h, w = get_inputs_hw(inputs)
  if h < height or w < width:
    return inputs
  return shortside_resize(inputs, min_size=min(height, width), interpolation=interpolation, **kwargs)


@supports()
def downscale(inputs, downscale=4.0, upscale=4.0, interpolation=T.RESIZE_MODE.NEAREST, **kwargs):
  return process('downscale',
                 inputs,
                 downscale=downscale,
                 upscale=upscale,
                 interpolation=interpolation,
                 **kwargs)

#!<-----------------------------------------------------------------------------
#!< Related with Crop
#!<-----------------------------------------------------------------------------


@supports()
def crop(inputs, top, left, height, width, **kwargs):
  """Crop the given image at specified location and output size.
  If the image is torch Tensor, it is expected to have [..., H, W] shape, where ... means an arbitrary number of leading dimensions.
  If image size is smaller than output size along any edge, image is padded with 0 and then cropped.

  Args:
      inputs: Image to be cropped. (0,0) denotes the top left corner of the image.
      top (int): Vertical component of the top left corner of the crop box.
      left (int): Horizontal component of the top left corner of the crop box.
      height (int): Height of the crop box.
      width (int): Width of the crop box.

  """
  return process('crop',
                 inputs,
                 top=top,
                 left=left,
                 height=height,
                 width=width,
                 **kwargs)


@supports()
def crop_and_pad(inputs,
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
                 **kwargs):
  """crop an area from source image and paste to dst
  """
  return process('crop_and_pad',
                 inputs,
                 src_crop_y=src_crop_y,
                 src_crop_x=src_crop_x,
                 src_crop_h=src_crop_h,
                 src_crop_w=src_crop_w,
                 dst_crop_x=dst_crop_x,
                 dst_crop_y=dst_crop_y,
                 dst_height=dst_height,
                 dst_width=dst_width,
                 fill_value=fill_value,
                 mode=mode,
                 **kwargs)


@supports()
def random_crop(inputs, height, width, **kwargs):
  """random crop, require width and height less than image

  Args:
      height (int or float): output height, or keep ratio (0 ~ 1)
      width (int or float): output width, or keep ratio (0 ~ 1)

  """
  def _get_coords(img_h, img_w, crop_h, crop_w, rh, rw):
    y1 = int((img_h - crop_h) * rh)
    y2 = y1 + crop_h
    x1 = int((img_w - crop_w) * rw)
    x2 = x1 + crop_w
    return x1, y1, x2, y2

  h, w = get_inputs_hw(inputs)
  rh = random.random()
  rw = random.random()

  new_width = int(w * width) if width < 1 else width
  new_height = int(h * height) if height < 1 else height
  x1, y1, x2, y2 = _get_coords(h, w, new_height, new_width, rh, rw)

  return crop(inputs, y1, x1, y2 - y1, x2 - x1, **kwargs)


@supports()
def center_crop(inputs, height, width, **kwargs):
  """crop inputs to target height and width.

  Args:
      height (int or float): output height
      width (int or float): output width

  """
  def _get_coords(height, width, crop_height, crop_width):
    y1 = (height - crop_height) // 2
    y2 = y1 + crop_height
    x1 = (width - crop_width) // 2
    x2 = x1 + crop_width
    return x1, y1, x2, y2

  h, w = get_inputs_hw(inputs)
  x1, y1, x2, y2 = _get_coords(h, w, height, width)

  return crop(inputs, y1, x1, y2 - y1, x2 - x1, **kwargs)


@supports()
def center_crop_and_pad(inputs, height, width, fill_value=0, **kwargs):
  """center crop and padding image to target_height and target_width

    if image width or height is smaller than target size, it will prefer to pad
      to max side and then implement center crop.

    if image width or height is less than target size, it will center paste image
      to target size.

  Args:
      height ([int]): target height
      width ([int]): target width
      fill_value ([float]): default to 0
  """
  h, w = get_inputs_hw(inputs)
  crop_x = max([0, (w - width) // 2])
  crop_y = max([0, (h - height) // 2])
  crop_h = min([height, h])
  crop_w = min([width, w])
  dst_y = max([0, (height - h) // 2])
  dst_x = max([0, (width - w) // 2])
  return crop_and_pad(
      inputs,
      src_crop_y=crop_y,
      src_crop_x=crop_x,
      src_crop_h=crop_h,
      src_crop_w=crop_w,
      dst_crop_y=dst_y,
      dst_crop_x=dst_x,
      dst_height=height,
      dst_width=width,
      fill_value=fill_value,
      mode='constant')


@supports()
def random_crop_and_pad(inputs, height, width, fill_value=0, **kwargs):
  """random crop and padding image to target_height and target_width

    if image width or height is smaller than target size, it will prefer to pad
      to max side and then implement center crop.

    if image width or height is less than target size, it will center paste image
      to target size.

  Args:
      height ([int]): target height
      width ([int]): target width
      fill_value ([float]): default to 0
  """
  h, w = get_inputs_hw(inputs)
  crop_x = random.randint(0, max(0, w - width))
  crop_y = random.randint(0, max(0, h - height))
  crop_h = height
  crop_w = width
  dst_y = 0
  dst_x = 0
  return crop_and_pad(
      inputs,
      src_crop_y=crop_y,
      src_crop_x=crop_x,
      src_crop_h=crop_h,
      src_crop_w=crop_w,
      dst_crop_y=dst_y,
      dst_crop_x=dst_x,
      dst_height=height,
      dst_width=width,
      fill_value=fill_value,
      mode='constant')


@supports()
def resized_crop(inputs, **kwargs):
  return process('resized_crop', inputs, **kwargs)


@supports()
def five_crop(inputs, crop_height, crop_width, **kwargs):
  return process('five_crop', inputs, crop_height=crop_height, crop_width=crop_width, **kwargs)


@supports()
def ten_crop(inputs, crop_height, crop_width, vertical_flip=False, **kwargs):
  return process('ten_crop',
                 inputs,
                 crop_height=crop_height,
                 crop_width=crop_width,
                 vertical_flip=vertical_flip,
                 **kwargs)


@supports()
def non_overlap_crop_patch(inputs, patch_size=32, stride=32, **kwargs):
  """non-overlapp crop.

    For a image [H, W, C], it will be divided into [N, patch_size, patch_size, C]
      N = ((h + patch_size) // (patch_size * stride)) * ((w + patch_size) // (patch_size * stride))

  Args:
      patch_size (int, optional): Defaults to 32.
      stride (int, optional): Defaults to 32.

  """
  return process('non_overlap_crop_patch',
                 inputs,
                 patch_size=patch_size,
                 stride=stride,
                 **kwargs)

#!<-----------------------------------------------------------------------------
#!< Related with Pixel/Block Changing
#!<-----------------------------------------------------------------------------


@supports()
def pixel_dropout(inputs, dropout_prob=0.1, per_channel=False, drop_value=0, **kwargs):
  return process('pixel_dropout',
                 inputs,
                 dropout_prob=dropout_prob,
                 per_channel=per_channel,
                 drop_value=drop_value,
                 **kwargs)


@supports()
def cutout(inputs, num_holes=8, h_size=20, w_size=20, fill_value=(255, 255, 255), **kwargs):
  return process('cutout',
                 inputs,
                 num_holes=num_holes,
                 h_size=h_size,
                 w_size=w_size,
                 fill_value=fill_value,
                 **kwargs)


@supports()
def channel_dropout(inputs, **kwargs):
  return process('channel_dropout', inputs, **kwargs)


@supports()
def coarse_dropout(inputs, **kwargs):
  return process('coarse_dropout', inputs, **kwargs)


@supports()
def grid_dropout(inputs, **kwargs):
  return process('grid_dropout', inputs, **kwargs)


@supports()
def grid_shuffle(inputs, **kwargs):
  return process('grid_shuffle', inputs, **kwargs)

#!<-----------------------------------------------------------------------------
#!< Related with Composed Augmentations
#!<-----------------------------------------------------------------------------


@supports()
def quality_aware_transforms(inputs, num_augs=5, iou_range=[
                             0.1, 0.3], patch_size=160, num_order=1, num_pairs=1, method='pair_crop', **kwargs):
  return process('quality_aware_transforms',
                 inputs,
                 num_augs=num_augs,
                 iou_range=iou_range,
                 patch_size=patch_size,
                 num_order=num_order,
                 num_pairs=num_pairs,
                 method=method,
                 **kwargs)
