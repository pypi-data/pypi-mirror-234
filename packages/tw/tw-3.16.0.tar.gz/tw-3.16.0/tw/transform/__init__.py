# Copyright 2017 The KaiJIN Authors. All Rights Reserved.
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
"""TensorWrapper Transform

  There are four core components to describe a variety of data type.

  - Meta: used in datasets and transform: it is usually used in Datasets class
    and maintains a numpy-like binary information. Generally, we use opencv or
    numpy to manipulate them.

  - [P]pil: it use Image.PIL as inputs.
    e.g: <T._random_crop_pil, T.RandomCropPIL>

  - [F]functional: it use SampleMetas as inputs.
    e.g. <T._random_crop_meta, T.RandomCropMeta>
      - store in: meta.bin [H, W], [H, W, C], [D, H, W, C]

  - [T]tensor: it use torch.Tensor as inputs.
    e.g. <T._random_crop_tensor, T.RandomCropTensor>
      - store in: [N, C, H, W], [C, H, W], [H, W]

  - [N]numpy: it use np.array as inputs
    e.g. <T._random_crop_np, T.RandomCropNumpy>
    - store in: [H, W], [H, W, C], [D, H, W, C]

    [2023/06/08 update]
    - all inputs should be range in [0, 255] uint8 or float32.
    - all inputs should be same dtype with input and output.



  - General: <T.random_crop, T.RandomCrop> to dispatch.

"""
# autopep8: off

from enum import Enum
import cv2
import PIL
from PIL import Image
from torchvision.transforms import InterpolationMode
import numpy as np

# conversion
class RESIZE_MODE(Enum):
  """Interpolation modes
  """
  NEAREST = "nearest"
  BILINEAR = "bilinear"
  BICUBIC = "bicubic"
  # For PIL compatibility
  BOX = "box"
  HAMMING = "hamming"
  LANCZOS = "lanczos"

RESIZE_MODE_TO_PIL = {
    RESIZE_MODE.NEAREST: Image.Resampling.NEAREST,
    RESIZE_MODE.BILINEAR: Image.Resampling.BILINEAR,
    RESIZE_MODE.BICUBIC: Image.Resampling.BICUBIC,
    RESIZE_MODE.BOX: Image.Resampling.BOX,
    RESIZE_MODE.HAMMING: Image.Resampling.HAMMING,
    RESIZE_MODE.LANCZOS: Image.Resampling.LANCZOS,
}

RESIZE_MODE_TO_TVF = {
    RESIZE_MODE.NEAREST: InterpolationMode.NEAREST,
    RESIZE_MODE.BILINEAR: InterpolationMode.BILINEAR,
    RESIZE_MODE.BICUBIC: InterpolationMode.BICUBIC,
    RESIZE_MODE.BOX: InterpolationMode.BOX,
    RESIZE_MODE.HAMMING: InterpolationMode.HAMMING,
    RESIZE_MODE.LANCZOS: InterpolationMode.LANCZOS,
}

RESIZE_MODE_TO_CV = {
    RESIZE_MODE.NEAREST: cv2.INTER_NEAREST,
    RESIZE_MODE.BILINEAR: cv2.INTER_LINEAR,
    RESIZE_MODE.BICUBIC: cv2.INTER_CUBIC,
    RESIZE_MODE.BOX: cv2.INTER_AREA,
    RESIZE_MODE.HAMMING: None,
    RESIZE_MODE.LANCZOS: cv2.INTER_LANCZOS4,
}

class BORDER_MODE(Enum):
  """padding or resize with border
  """
  CONSTANT = "constant"
  EDGE = "edge"
  REFLECT = "reflect"
  SYMMETRIC = "symmetric"


BORDER_MODE_TO_PIL = {
    BORDER_MODE.CONSTANT: "constant",
    BORDER_MODE.EDGE: "edge",
    BORDER_MODE.REFLECT: "reflect",
    BORDER_MODE.SYMMETRIC: "symmetric",
}

BORDER_MODE_TO_CV = {
    BORDER_MODE.CONSTANT: cv2.BORDER_CONSTANT,
    BORDER_MODE.EDGE: cv2.BORDER_ISOLATED,
    BORDER_MODE.REFLECT: cv2.BORDER_REFLECT,
    BORDER_MODE.SYMMETRIC: cv2.BORDER_REPLICATE,
}

class COLORSPACE(Enum):
  """Colorspace
  """
  # rgb24
  RGB = "rgb"
  BGR = "bgr"
  # rgb24
  RGBA = "rgba"
  BGRA = "bgra"
  # others
  HLS = "hls"
  HSV = "hsv"
  YIQ = "yiq"
  LHM = "lhm"
  XYZ = "xyz"
  LAB = "lab"
  # 709
  YUV709V = "yuv709v"
  YUV709F = "yuv709f"
  # 601
  YUV601V = "yuv601v"
  YUV601F = "yuv601f"
  # hdr
  HDR = "hdr"
  # raw
  BAYER = "bayer"
  XTRANS = "xtrans"
  # specific data
  OPTICALFLOW = "optical_flow"  # data represent direction and distance
  HEATMAP = "heatmap"  # data should not be changed by resize
  GRAY = "gray" # single channel


class MetaBase():
  def __init__(self, name='MetaBase'):
    self.name = name
    self.source = None
    self.path = None
    self.bin = None

  def numpy(self):
    return self

  def to(self, device):
    return self

  def __str__(self):
    return 'MetaBase'

  def __len__(self):
    return 0

# container
from .meta_image import ImageMeta
from .meta_video import VideoMeta
from .meta_bbox import BoxListMeta
from .meta_keypoints import KpsListMeta

#!<-----------------------------------------------------------------------------
#!< Related with Data Type
#!<-----------------------------------------------------------------------------
# data conversion
from .functional import to_float
from .functional import to_round_uint8
from .functional import to_data_range

# type conversion
from .functional import to_tensor
from .functional import to_pil
from .functional import to_numpy

#!<-----------------------------------------------------------------------------
#!< Related with Colorspace
#!<-----------------------------------------------------------------------------
from .functional import change_colorspace
from .functional import to_color
from .functional import to_grayscale
from .functional import rgb_to_yuv709v
from .functional import bgr_to_yuv709v
from .functional import rgb_to_yuv709f
from .functional import bgr_to_yuv709f
from .functional import yuv709v_to_rgb
from .functional import yuv709f_to_rgb
from .functional import rgb_to_bgr
from .functional import bgr_to_rgb
from .functional import rgb_to_yuv601
from .functional import yuv601_to_rgb
from .functional import rgb_to_yiq
from .functional import rgb_to_lhm
from .functional import rgb_to_xyz
from .functional import xyz_to_lab
from .functional import rgb_to_lab

from .functional import yuv420_to_yuv444
from .functional import yuv444_to_yuv420

#!<-----------------------------------------------------------------------------
#!< Related with Shapren
#!<-----------------------------------------------------------------------------
# sharpen
from .functional import usm_sharpen
from .functional import bilateral_usm_sharpen
from .functional import adaptive_usm_sharpen
from .functional import high_contrast_sharpen
from .functional import photoshop_usm_sharpen

#!<-----------------------------------------------------------------------------
#!< Related with Blur
#!<-----------------------------------------------------------------------------
# blur
from .functional import gaussian_blur
from .functional import motion_blur
from .functional import median_blur
from .functional import glass_blur
from .functional import advanced_blur
from .functional import defocus_blur
from .functional import zoom_blur

#!<-----------------------------------------------------------------------------
#!< Related with Noise/Denoise
#!<-----------------------------------------------------------------------------
# noise
from .functional import iso_noise
from .functional import gaussian_noise
# speckle_noise, multiplicated_noise
from .functional import poisson_noise
from .functional import multiplicative_noise

#!<-----------------------------------------------------------------------------
#!< Related with Color
#!<-----------------------------------------------------------------------------
# photometric
from .functional import adjust_sharpness
from .functional import adjust_brightness
from .functional import adjust_contrast
from .functional import adjust_gamma
from .functional import adjust_hue
from .functional import adjust_saturation

#!<-----------------------------------------------------------------------------
#!< Related with Image Tone Changing
#!<-----------------------------------------------------------------------------
# noramlize
from .functional import equal_hist
from .functional import match_hist
from .functional import truncated_standardize
from .functional import local_contrast_normalize

from .functional import change_tone_curve
from .functional import clahe
from .functional import homomorphic

from .functional import sepia
from .functional import solarize
from .functional import posterize

from .functional import rgb_shift
from .functional import hsv_shift

#!<-----------------------------------------------------------------------------
#!< Related with DCT
#!<-----------------------------------------------------------------------------
# compression
from .functional import jpeg_compress

# gradient
from .functional import sobel

#!<-----------------------------------------------------------------------------
#!< Related with Image Effect
#!<-----------------------------------------------------------------------------
# effect
from .functional import add_snow
from .functional import add_fog
from .functional import add_rain
from .functional import add_sunflare
from .functional import add_shadow
from .functional import add_spatter
from .functional import add_ringing_overshoot

#!<-----------------------------------------------------------------------------
#!< Related with Image Morphology
#!<-----------------------------------------------------------------------------
# morphology
from .functional import alpha_to_trimap

#!<-----------------------------------------------------------------------------
#!< Related with Flip
#!<-----------------------------------------------------------------------------
# flip
from .functional import hflip
from .functional import random_hflip
from .functional import vflip
from .functional import random_vflip
from .functional import flip

#!<-----------------------------------------------------------------------------
#!< Related with Rotation
#!<-----------------------------------------------------------------------------
# affine
from .functional import rotate
from .functional import random_rotate
from .functional import affine_theta
from .functional import affine
from .functional import random_affine

#!<-----------------------------------------------------------------------------
#!< Related with Padding
#!<-----------------------------------------------------------------------------
# padding
from .functional import pad
from .functional import pad_to_size_divisible
from .functional import pad_to_square
from .functional import pad_to_target_size

#!<-----------------------------------------------------------------------------
#!< Related with Resize
#!<-----------------------------------------------------------------------------
# resize
from .functional import resize
from .functional import random_resize
from .functional import shortside_resize
from .functional import adaptive_resize
from .functional import downscale

#!<-----------------------------------------------------------------------------
#!< Related with Crop
#!<-----------------------------------------------------------------------------
# crop
from .functional import crop
from .functional import crop_and_pad
from .functional import random_crop
from .functional import center_crop
from .functional import center_crop_and_pad
from .functional import random_crop_and_pad
from .functional import resized_crop
from .functional import five_crop
from .functional import ten_crop
from .functional import non_overlap_crop_patch

#!<-----------------------------------------------------------------------------
#!< Related with Pixel/Block Changing
#!<-----------------------------------------------------------------------------
# dropout pixel, block, channels
from .functional import pixel_dropout
from .functional import cutout
from .functional import channel_dropout
from .functional import coarse_dropout
from .functional import grid_dropout

# block shuffle
from .functional import grid_shuffle

#!<-----------------------------------------------------------------------------
#!< Related with Composed Augmentations
#!<-----------------------------------------------------------------------------

from .functional import quality_aware_transforms

# bbox
from . import bbox

# autopep8: on