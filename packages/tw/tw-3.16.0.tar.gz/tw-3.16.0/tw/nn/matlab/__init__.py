"""This folder contains pytorch implementations of matlab functions.
And should produce the same results as matlab.

Note: to enable GPU acceleration, all functions take batched tensors as inputs,
and return batched results.

"""
from .resize import imresize

from .functions import fspecial
from .functions import conv2d
from .functions import imfilter
from .functions import filter2
from .functions import dct
from .functions import dct2d
from .functions import fitweibull
from .functions import cov
from .functions import nancov
from .functions import nanmean
from .functions import im2col
from .functions import blockproc

from .scfpyr_util import SCFpyr_PyTorch

from .color_util import safe_frac_pow
from .color_util import to_y_channel
from .color_util import rgb2ycbcr
from .color_util import ycbcr2rgb
from .color_util import rgb2lmn
from .color_util import rgb2xyz
from .color_util import xyz2lab
from .color_util import rgb2lab
from .color_util import rgb2yiq
from .color_util import rgb2lhm

from .arch_util import dist_to_mos
from .arch_util import clean_state_dict
from .arch_util import load_pretrained_network
from .arch_util import _ntuple
from .arch_util import default_init_weights
from .arch_util import symm_pad
from .arch_util import excact_padding_2d
from .arch_util import ExactPadding2d

from .multiscale_patches import get_multiscale_patches

from .nss import extract_2d_patches
from .nss import torch_cov
from .nss import safe_sqrt
from .nss import diff_round
from .nss import normalize_img_with_guass
from .nss import scharr_filter
from .nss import gradient_map
from .nss import similarity_map
from .nss import ifftshift
from .nss import get_meshgrid
from .nss import estimate_ggd_param
from .nss import estimate_aggd_param
