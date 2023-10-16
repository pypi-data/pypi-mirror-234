# Copyright 2023 The KaiJIN Authors. All Rights Reserved.
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
"""https://github.com/PeterL1n/RobustVideoMatting
"""
from typing import Tuple, Optional, List, Callable

import torch
from torch import Tensor
from torch import nn
from torch.nn import functional as F

import numpy as np

from torchvision.models.resnet import ResNet, Bottleneck
from torchvision.models.mobilenetv3 import MobileNetV3, InvertedResidualConfig
from torchvision.transforms.functional import normalize

import tw

__all__ = [
    'MobileNetV3LargeEncoder',
    'MobileNetV3SmallEncoder',
    'ResNet50Encoder',
    'LRASPP',
    'RecurrentDecoder',
    'AvgPool',
    'BottleneckBlock',
    'UpsamplingBlock',
    'OutputBlock',
    'ConvGRU',
    'Projection',
    'DeepGuidedFilterRefiner',
    'FastGuidedFilterRefiner',
    'FastGuidedFilter',
    'BoxFilter',
    'MattingNetwork',
]

#!<----------------------------------------------------------------------------
#!< MOBILENET-v3
#!<----------------------------------------------------------------------------


class MobileNetV3LargeEncoder(MobileNetV3):
  def __init__(self, pretrained: bool = False):
    super().__init__(
        inverted_residual_setting=[
            # first conv
            InvertedResidualConfig(16, 3, 16, 16, False, "RE", 1, 1, 1),
            # got f1, 1/2
            InvertedResidualConfig(16, 3, 64, 24, False, "RE", 2, 1, 1),  # C1
            InvertedResidualConfig(24, 3, 72, 24, False, "RE", 1, 1, 1),
            # got f2, 1/4
            InvertedResidualConfig(24, 5, 72, 40, True, "RE", 2, 1, 1),  # C2
            InvertedResidualConfig(40, 5, 120, 40, True, "RE", 1, 1, 1),
            InvertedResidualConfig(40, 5, 120, 40, True, "RE", 1, 1, 1),
            # got f3, 1/8
            InvertedResidualConfig(40, 3, 240, 80, False, "HS", 2, 1, 1),  # C3
            InvertedResidualConfig(80, 3, 200, 80, False, "HS", 1, 1, 1),
            InvertedResidualConfig(80, 3, 184, 80, False, "HS", 1, 1, 1),
            InvertedResidualConfig(80, 3, 184, 80, False, "HS", 1, 1, 1),
            InvertedResidualConfig(80, 3, 480, 112, True, "HS", 1, 1, 1),
            InvertedResidualConfig(112, 3, 672, 112, True, "HS", 1, 1, 1),
            InvertedResidualConfig(112, 5, 672, 160, True, "HS", 2, 2, 1),  # C4
            InvertedResidualConfig(160, 5, 960, 160, True, "HS", 1, 2, 1),
            InvertedResidualConfig(160, 5, 960, 160, True, "HS", 1, 2, 1),
            # last conv
            # got f4, 1/16
        ],
        last_channel=1280
    )

    if pretrained:
      self.load_state_dict(torch.hub.load_state_dict_from_url(
          'https://download.pytorch.org/models/mobilenet_v3_large-8738ca79.pth'))

    del self.avgpool
    del self.classifier

  def forward_single_frame(self, x):
    # assume the input shape is [3, 432, 432]
    x = normalize(x, [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

    x = self.features[0](x)     # first conv, [16, 216, 216]
    x = self.features[1](x)     # IRConfig[0], f1 = [16, 216, 216]
    f1 = x
    x = self.features[2](x)     # IRConfig[1], [24, 108, 108]
    x = self.features[3](x)     # IRConfig[2], f2 = [24, 108, 108]
    f2 = x
    x = self.features[4](x)     # IRConfig[3], [40, 54, 54]
    x = self.features[5](x)     # IRConfig[4], [40, 54, 54]
    x = self.features[6](x)     # IRConfig[5], f3 = [40, 54, 54]
    f3 = x
    x = self.features[7](x)     # IRConfig[6], [80, 27, 27]
    x = self.features[8](x)     # IRConfig[7], [80, 27, 27]
    x = self.features[9](x)     # IRConfig[8], [80, 27, 27]
    x = self.features[10](x)    # IRConfig[9], [80, 27, 27]
    x = self.features[11](x)    # IRConfig[10], [112, 27, 27]
    x = self.features[12](x)    # IRConfig[11], [112, 27, 27]
    x = self.features[13](x)    # IRConfig[12], [160, 27, 27]
    x = self.features[14](x)    # IRConfig[13], [160, 27, 27]
    x = self.features[15](x)    # IRConfig[14], [160, 27, 27]
    x = self.features[16](x)    # last conv, f4 = [960, 27, 27]
    f4 = x
    return [f1, f2, f3, f4]

  def forward_time_series(self, x):
    B, T = x.shape[:2]
    features = self.forward_single_frame(x.flatten(0, 1))
    features = [f.unflatten(0, (B, T)) for f in features]
    return features

  def forward(self, x):
    if x.ndim == 5:
      return self.forward_time_series(x)
    else:
      return self.forward_single_frame(x)


class MobileNetV3SmallEncoder(MobileNetV3):
  def __init__(self, pretrained: bool = False):
    super().__init__(
        inverted_residual_setting=[
            # first conv
            # got f1, 1/2
            InvertedResidualConfig(16, 3, 16, 16, True, "RE", 2, 1, 1),  # C1
            # got f2, 1/4
            InvertedResidualConfig(16, 3, 72, 24, False, "RE", 2, 1, 1),  # C2
            InvertedResidualConfig(24, 3, 88, 24, False, "RE", 1, 1, 1),
            # got f3, 1/8
            InvertedResidualConfig(24, 5, 96, 40, True, "HS", 2, 1, 1),  # C3
            InvertedResidualConfig(40, 5, 240, 40, True, "HS", 1, 1, 1),
            InvertedResidualConfig(40, 5, 240, 40, True, "HS", 1, 1, 1),
            InvertedResidualConfig(40, 5, 120, 48, True, "HS", 1, 1, 1),
            InvertedResidualConfig(48, 5, 144, 48, True, "HS", 1, 1, 1),
            InvertedResidualConfig(48, 5, 288, 96, True, "HS", 2, 2, 1),  # C4
            InvertedResidualConfig(96, 5, 576, 96, True, "HS", 1, 2, 1),
            InvertedResidualConfig(96, 5, 576, 96, True, "HS", 1, 2, 1),
            # last conv
            # got f4, 1/16
        ],
        last_channel=1024
    )

    if pretrained:
      self.load_state_dict(torch.hub.load_state_dict_from_url(
          'https://download.pytorch.org/models/mobilenet_v3_small-047dcff4.pth'))

    del self.avgpool
    del self.classifier

  def forward_single_frame(self, x):
    # assume the input shape is [3, 432, 432]
    x = normalize(x, [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

    x = self.features[0](x)     # first conv, f1 = [16, 216, 216]
    f1 = x
    x = self.features[1](x)     # IRConfig[0], f2 = [16, 108, 108]
    f2 = x
    x = self.features[2](x)     # IRConfig[1], [24, 54, 54]
    x = self.features[3](x)     # IRConfig[2], f3 = [24, 54, 54]
    f3 = x
    x = self.features[4](x)     # IRConfig[3], [40, 27, 27]
    x = self.features[5](x)     # IRConfig[4], [40, 27, 27]
    x = self.features[6](x)     # IRConfig[5], [40, 27, 27]
    x = self.features[7](x)     # IRConfig[6], [48, 27, 27]
    x = self.features[8](x)     # IRConfig[7], [48, 27, 27]
    x = self.features[9](x)     # IRConfig[8], [96, 27, 27]
    x = self.features[10](x)    # IRConfig[9], [96, 27, 27]
    x = self.features[11](x)    # IRConfig[10], [96, 27, 27]
    x = self.features[12](x)    # last conv, f4 = [576, 27, 27]
    f4 = x
    return [f1, f2, f3, f4]

  def forward_time_series(self, x):
    B, T = x.shape[:2]
    features = self.forward_single_frame(x.flatten(0, 1))
    features = [f.unflatten(0, (B, T)) for f in features]
    return features

  def forward(self, x):
    if x.ndim == 5:
      return self.forward_time_series(x)
    else:
      return self.forward_single_frame(x)


#!<----------------------------------------------------------------------------
#!< RESNET
#!<----------------------------------------------------------------------------


class ResNet50Encoder(ResNet):
  def __init__(self, pretrained: bool = False):
    super().__init__(
        block=Bottleneck,
        layers=[3, 4, 6, 3],
        replace_stride_with_dilation=[False, False, True],
        norm_layer=None)

    if pretrained:
      self.load_state_dict(torch.hub.load_state_dict_from_url(
          'https://download.pytorch.org/models/resnet50-0676ba61.pth'))

    del self.avgpool
    del self.fc

  def forward_single_frame(self, x):
    x = self.conv1(x)
    x = self.bn1(x)
    x = self.relu(x)
    f1 = x  # 1/2
    x = self.maxpool(x)
    x = self.layer1(x)
    f2 = x  # 1/4
    x = self.layer2(x)
    f3 = x  # 1/8
    x = self.layer3(x)
    x = self.layer4(x)
    f4 = x  # 1/16
    return [f1, f2, f3, f4]

  def forward_time_series(self, x):
    B, T = x.shape[:2]
    features = self.forward_single_frame(x.flatten(0, 1))
    features = [f.unflatten(0, (B, T)) for f in features]
    return features

  def forward(self, x):
    if x.ndim == 5:
      return self.forward_time_series(x)
    else:
      return self.forward_single_frame(x)


#!<----------------------------------------------------------------------------
#!< LRASPP
#!<----------------------------------------------------------------------------


class LRASPP(nn.Module):
  def __init__(self, in_channels, out_channels):
    super().__init__()
    self.aspp1 = nn.Sequential(
        nn.Conv2d(in_channels, out_channels, 1, bias=False),
        nn.BatchNorm2d(out_channels),
        nn.ReLU(True)
    )
    self.aspp2 = nn.Sequential(
        nn.AdaptiveAvgPool2d(1),
        nn.Conv2d(in_channels, out_channels, 1, bias=False),
        nn.Sigmoid()
    )

  def forward_single_frame(self, x):
    return self.aspp1(x) * self.aspp2(x)

  def forward_time_series(self, x):
    B, T = x.shape[:2]
    x = self.forward_single_frame(x.flatten(0, 1)).unflatten(0, (B, T))
    return x

  def forward(self, x):
    if x.ndim == 5:
      return self.forward_time_series(x)
    else:
      return self.forward_single_frame(x)

#!<----------------------------------------------------------------------------
#!< DECODER
#!<----------------------------------------------------------------------------


class RecurrentDecoder(nn.Module):
  def __init__(self, feature_channels, decoder_channels):
    super().__init__()
    self.avgpool = AvgPool()
    self.decode4 = BottleneckBlock(feature_channels[3])
    self.decode3 = UpsamplingBlock(feature_channels[3], feature_channels[2], 3, decoder_channels[0])
    self.decode2 = UpsamplingBlock(decoder_channels[0], feature_channels[1], 3, decoder_channels[1])
    self.decode1 = UpsamplingBlock(decoder_channels[1], feature_channels[0], 3, decoder_channels[2])
    self.decode0 = OutputBlock(decoder_channels[2], 3, decoder_channels[3])

  def forward(self,
              s0: Tensor, f1: Tensor, f2: Tensor, f3: Tensor, f4: Tensor,
              r1: Optional[Tensor], r2: Optional[Tensor],
              r3: Optional[Tensor], r4: Optional[Tensor]):
    s1, s2, s3 = self.avgpool(s0)   # [1, 3, 432^2] -> [1, 3, 216^2] [1, 3, 108^2] [1, 3, 54^2]
    x4, r4 = self.decode4(f4, r4)   # [1, 128, 27^2] [1, 64, 27^2] -> [1, 128, 27^2] [1, 64, 27^2]
    # [1, 128, 27^2] [1, 40, 54^2] [1, 3, 54^2] [1, 40, 54^2] -> [1, 80, 54^2] [1, 40, 54^2]
    x3, r3 = self.decode3(x4, f3, s3, r3)
    # [1, 80, 54^2] [1, 24, 108^2] [1, 3, 108^2] [1, 20, 108^2] -> [1, 40, 108^2] [1, 20, 108^2]
    x2, r2 = self.decode2(x3, f2, s2, r2)
    # [1, 40, 108^2] [1, 16, 216^2] [1, 3, 216^2] [1, 16, 216^2] -> [1, 32, 216^2] [1, 16, 216^2]
    x1, r1 = self.decode1(x2, f1, s1, r1)
    x0 = self.decode0(x1, s0)               # [1, 32, 216^2] [1, 3, 432^2] -> [1, 16, 432^2]
    return x0, r1, r2, r3, r4


class AvgPool(nn.Module):
  def __init__(self):
    super().__init__()
    self.avgpool = nn.AvgPool2d(2, 2, count_include_pad=False, ceil_mode=True)

  def forward_single_frame(self, s0):
    s1 = self.avgpool(s0)
    s2 = self.avgpool(s1)
    s3 = self.avgpool(s2)
    return s1, s2, s3

  def forward_time_series(self, s0):
    B, T = s0.shape[:2]
    s0 = s0.flatten(0, 1)
    s1, s2, s3 = self.forward_single_frame(s0)
    s1 = s1.unflatten(0, (B, T))
    s2 = s2.unflatten(0, (B, T))
    s3 = s3.unflatten(0, (B, T))
    return s1, s2, s3

  def forward(self, s0):
    if s0.ndim == 5:
      return self.forward_time_series(s0)
    else:
      return self.forward_single_frame(s0)


class BottleneckBlock(nn.Module):
  def __init__(self, channels):
    super().__init__()
    self.channels = channels
    self.gru = ConvGRU(channels // 2)

  def forward(self, x, r: Optional[Tensor]):
    a, b = x.split(self.channels // 2, dim=-3)
    b, r = self.gru(b, r)
    x = torch.cat([a, b], dim=-3)
    return x, r


class UpsamplingBlock(nn.Module):
  def __init__(self, in_channels, skip_channels, src_channels, out_channels):
    super().__init__()
    self.out_channels = out_channels
    self.upsample = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False)
    self.conv = nn.Sequential(
        nn.Conv2d(in_channels + skip_channels + src_channels, out_channels, 3, 1, 1, bias=False),
        nn.BatchNorm2d(out_channels),
        nn.ReLU(True),
    )
    self.gru = ConvGRU(out_channels // 2)

  def forward_single_frame(self, x, f, s, r: Optional[Tensor]):
    x = self.upsample(x)
    x = x[:, :, :s.size(2), :s.size(3)]
    x = torch.cat([x, f, s], dim=1)
    x = self.conv(x)
    a, b = x.split(self.out_channels // 2, dim=1)
    b, r = self.gru(b, r)
    x = torch.cat([a, b], dim=1)
    return x, r

  def forward_time_series(self, x, f, s, r: Optional[Tensor]):
    B, T, _, H, W = s.shape
    x = x.flatten(0, 1)
    f = f.flatten(0, 1)
    s = s.flatten(0, 1)
    x = self.upsample(x)
    x = x[:, :, :H, :W]
    x = torch.cat([x, f, s], dim=1)
    x = self.conv(x)
    x = x.unflatten(0, (B, T))
    a, b = x.split(self.out_channels // 2, dim=2)
    b, r = self.gru(b, r)
    x = torch.cat([a, b], dim=2)
    return x, r

  def forward(self, x, f, s, r: Optional[Tensor]):
    if x.ndim == 5:
      return self.forward_time_series(x, f, s, r)
    else:
      return self.forward_single_frame(x, f, s, r)


class OutputBlock(nn.Module):
  def __init__(self, in_channels, src_channels, out_channels):
    super().__init__()
    self.upsample = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False)
    self.conv = nn.Sequential(
        nn.Conv2d(in_channels + src_channels, out_channels, 3, 1, 1, bias=False),
        nn.BatchNorm2d(out_channels),
        nn.ReLU(True),
        nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias=False),
        nn.BatchNorm2d(out_channels),
        nn.ReLU(True),
    )

  def forward_single_frame(self, x, s):
    x = self.upsample(x)
    x = x[:, :, :s.size(2), :s.size(3)]
    x = torch.cat([x, s], dim=1)
    x = self.conv(x)
    return x

  def forward_time_series(self, x, s):
    B, T, _, H, W = s.shape
    x = x.flatten(0, 1)
    s = s.flatten(0, 1)
    x = self.upsample(x)
    x = x[:, :, :H, :W]
    x = torch.cat([x, s], dim=1)
    x = self.conv(x)
    x = x.unflatten(0, (B, T))
    return x

  def forward(self, x, s):
    if x.ndim == 5:
      return self.forward_time_series(x, s)
    else:
      return self.forward_single_frame(x, s)


class ConvGRU(nn.Module):
  def __init__(self,
               channels: int,
               kernel_size: int = 3,
               padding: int = 1):
    super().__init__()
    self.channels = channels
    self.ih = nn.Sequential(
        nn.Conv2d(channels * 2, channels * 2, kernel_size, padding=padding),
        nn.Sigmoid()
    )
    self.hh = nn.Sequential(
        nn.Conv2d(channels * 2, channels, kernel_size, padding=padding),
        nn.Tanh()
    )

  def forward_single_frame(self, x, h):
    r, z = self.ih(torch.cat([x, h], dim=1)).split(self.channels, dim=1)
    c = self.hh(torch.cat([x, r * h], dim=1))
    h = (1 - z) * h + z * c
    return h, h

  def forward_time_series(self, x, h):
    o = []
    for xt in x.unbind(dim=1):
      ot, h = self.forward_single_frame(xt, h)
      o.append(ot)
    o = torch.stack(o, dim=1)
    return o, h

  def forward(self, x, h: Optional[Tensor]):
    if h is None:
      h = torch.zeros((x.size(0), x.size(-3), x.size(-2), x.size(-1)),
                      device=x.device, dtype=x.dtype)

    if x.ndim == 5:
      return self.forward_time_series(x, h)
    else:
      return self.forward_single_frame(x, h)


class Projection(nn.Module):
  def __init__(self, in_channels, out_channels):
    super().__init__()
    self.conv = nn.Conv2d(in_channels, out_channels, 1)

  def forward_single_frame(self, x):
    return self.conv(x)

  def forward_time_series(self, x):
    B, T = x.shape[:2]
    return self.conv(x.flatten(0, 1)).unflatten(0, (B, T))

  def forward(self, x):
    if x.ndim == 5:
      return self.forward_time_series(x)
    else:
      return self.forward_single_frame(x)


#!<----------------------------------------------------------------------------
#!< GUIDED FILTER
#!<----------------------------------------------------------------------------


"""
Adopted from <https://github.com/wuhuikai/DeepGuidedFilter/>
"""


class DeepGuidedFilterRefiner(nn.Module):
  def __init__(self, hid_channels=16):
    super().__init__()
    self.box_filter = nn.Conv2d(4, 4, kernel_size=3, padding=1, bias=False, groups=4)
    self.box_filter.weight.data[...] = 1 / 9
    self.conv = nn.Sequential(
        nn.Conv2d(4 * 2 + hid_channels, hid_channels, kernel_size=1, bias=False),
        nn.BatchNorm2d(hid_channels),
        nn.ReLU(True),
        nn.Conv2d(hid_channels, hid_channels, kernel_size=1, bias=False),
        nn.BatchNorm2d(hid_channels),
        nn.ReLU(True),
        nn.Conv2d(hid_channels, 4, kernel_size=1, bias=True)
    )

  def forward_single_frame(self, fine_src, base_src, base_fgr, base_pha, base_hid):
    fine_x = torch.cat([fine_src, fine_src.mean(1, keepdim=True)], dim=1)
    base_x = torch.cat([base_src, base_src.mean(1, keepdim=True)], dim=1)
    base_y = torch.cat([base_fgr, base_pha], dim=1)

    mean_x = self.box_filter(base_x)
    mean_y = self.box_filter(base_y)
    cov_xy = self.box_filter(base_x * base_y) - mean_x * mean_y
    var_x = self.box_filter(base_x * base_x) - mean_x * mean_x

    A = self.conv(torch.cat([cov_xy, var_x, base_hid], dim=1))
    b = mean_y - A * mean_x

    H, W = fine_src.shape[2:]
    A = F.interpolate(A, (H, W), mode='bilinear', align_corners=False)
    b = F.interpolate(b, (H, W), mode='bilinear', align_corners=False)

    out = A * fine_x + b
    fgr, pha = out.split([3, 1], dim=1)
    return fgr, pha

  def forward_time_series(self, fine_src, base_src, base_fgr, base_pha, base_hid):
    B, T = fine_src.shape[:2]
    fgr, pha = self.forward_single_frame(
        fine_src.flatten(0, 1),
        base_src.flatten(0, 1),
        base_fgr.flatten(0, 1),
        base_pha.flatten(0, 1),
        base_hid.flatten(0, 1))
    fgr = fgr.unflatten(0, (B, T))
    pha = pha.unflatten(0, (B, T))
    return fgr, pha

  def forward(self, fine_src, base_src, base_fgr, base_pha, base_hid):
    if fine_src.ndim == 5:
      return self.forward_time_series(fine_src, base_src, base_fgr, base_pha, base_hid)
    else:
      return self.forward_single_frame(fine_src, base_src, base_fgr, base_pha, base_hid)


"""
Adopted from <https://github.com/wuhuikai/DeepGuidedFilter/>
"""


class FastGuidedFilterRefiner(nn.Module):
  def __init__(self, *args, **kwargs):
    super().__init__()
    self.guilded_filter = FastGuidedFilter(1)

  def forward_single_frame(self, fine_src, base_src, base_fgr, base_pha):
    fine_src_gray = fine_src.mean(1, keepdim=True)
    base_src_gray = base_src.mean(1, keepdim=True)

    fgr, pha = self.guilded_filter(
        torch.cat([base_src, base_src_gray], dim=1),
        torch.cat([base_fgr, base_pha], dim=1),
        torch.cat([fine_src, fine_src_gray], dim=1)).split([3, 1], dim=1)

    return fgr, pha

  def forward_time_series(self, fine_src, base_src, base_fgr, base_pha):
    B, T = fine_src.shape[:2]
    fgr, pha = self.forward_single_frame(
        fine_src.flatten(0, 1),
        base_src.flatten(0, 1),
        base_fgr.flatten(0, 1),
        base_pha.flatten(0, 1))
    fgr = fgr.unflatten(0, (B, T))
    pha = pha.unflatten(0, (B, T))
    return fgr, pha

  def forward(self, fine_src, base_src, base_fgr, base_pha, base_hid):
    if fine_src.ndim == 5:
      return self.forward_time_series(fine_src, base_src, base_fgr, base_pha)
    else:
      return self.forward_single_frame(fine_src, base_src, base_fgr, base_pha)


class FastGuidedFilter(nn.Module):
  def __init__(self, r: int, eps: float = 1e-5):
    super().__init__()
    self.r = r
    self.eps = eps
    self.boxfilter = BoxFilter(r)

  def forward(self, lr_x, lr_y, hr_x):
    mean_x = self.boxfilter(lr_x)
    mean_y = self.boxfilter(lr_y)
    cov_xy = self.boxfilter(lr_x * lr_y) - mean_x * mean_y
    var_x = self.boxfilter(lr_x * lr_x) - mean_x * mean_x
    A = cov_xy / (var_x + self.eps)
    b = mean_y - A * mean_x
    A = F.interpolate(A, hr_x.shape[2:], mode='bilinear', align_corners=False)
    b = F.interpolate(b, hr_x.shape[2:], mode='bilinear', align_corners=False)
    return A * hr_x + b


class BoxFilter(nn.Module):
  def __init__(self, r):
    super(BoxFilter, self).__init__()
    self.r = r

  def forward(self, x):
    # Note: The original implementation at <https://github.com/wuhuikai/DeepGuidedFilter/>
    #       uses faster box blur. However, it may not be friendly for ONNX export.
    #       We are switching to use simple convolution for box blur.
    kernel_size = 2 * self.r + 1
    kernel_x = torch.full((x.data.shape[1], 1, 1, kernel_size), 1 / kernel_size, device=x.device, dtype=x.dtype)
    kernel_y = torch.full((x.data.shape[1], 1, kernel_size, 1), 1 / kernel_size, device=x.device, dtype=x.dtype)
    x = F.conv2d(x, kernel_x, padding=(0, self.r), groups=x.data.shape[1])
    x = F.conv2d(x, kernel_y, padding=(self.r, 0), groups=x.data.shape[1])
    return x

#!<----------------------------------------------------------------------------
#!< RVM
#!<----------------------------------------------------------------------------


class MattingNetwork(nn.Module):
  def __init__(self,
               variant: str = 'mobilenetv3',
               refiner: str = 'deep_guided_filter',
               pretrained_backbone: bool = False):
    super().__init__()
    assert variant in ['mobilenetv3', 'mobilenetv3_thin_decoder0',
                       'mobilenetv3_thin_decoder1', 'mobilenetv3_small', 'resnet50']
    assert refiner in ['fast_guided_filter', 'deep_guided_filter']

    if variant == 'mobilenetv3':
      '''
          official backbone
          5.78GMac, 3.75M params
      '''
      self.backbone = MobileNetV3LargeEncoder(pretrained_backbone)
      self.aspp = LRASPP(960, 128)
      self.last_channel = 16
      self.decoder = RecurrentDecoder([16, 24, 40, 128], [80, 40, 32, self.last_channel])
    elif variant == "mobilenetv3_thin_decoder0":
      '''
          reduce the channels of dec3 ~ dec0 to 80%, 80%, 50%, 50%
          3.42GMac(60%), 3.65M params(97%)
      '''
      self.backbone = MobileNetV3LargeEncoder(pretrained_backbone)
      self.aspp = LRASPP(960, 128)
      self.last_channel = 8
      self.decoder = RecurrentDecoder([16, 24, 40, 128], [64, 32, 16, self.last_channel])
    elif variant == 'mobilenetv3_thin_decoder1':
      '''
          reduce the channels of dec3 ~ dec0 to 50%, 50%, 25%, 25%
          2.34GMac(40%), 3.55M params(95%)
      '''
      self.backbone = MobileNetV3LargeEncoder(pretrained_backbone)
      self.aspp = LRASPP(960, 128)
      self.last_channel = 4
      self.decoder = RecurrentDecoder([16, 24, 40, 128], [40, 20, 8, self.last_channel])
    elif variant == 'mobilenetv3_small':
      '''
          mobilenetv3 small backbone and a thin decoder
          1.32GMac(23%), 1.39M params(37%)
      '''
      self.backbone = MobileNetV3SmallEncoder(pretrained_backbone)
      self.aspp = LRASPP(576, 128)
      self.last_channel = 4
      self.decoder = RecurrentDecoder([16, 16, 24, 128], [40, 20, 8, self.last_channel])
    else:
      '''
          official backbone
          34.56GMac, 26.89M params
      '''
      self.backbone = ResNet50Encoder(pretrained_backbone)
      self.aspp = LRASPP(2048, 256)
      self.last_channel = 16
      self.decoder = RecurrentDecoder([64, 256, 512, 256], [128, 64, 32, self.last_channel])

    self.project_mat = Projection(self.last_channel, 4)
    self.project_seg = Projection(self.last_channel, 1)
    self.project_live_seg = Projection(self.last_channel, 5)

    if refiner == 'deep_guided_filter':
      self.refiner = DeepGuidedFilterRefiner(self.last_channel)
    else:
      self.refiner = FastGuidedFilterRefiner()

  def forward(self,
              src: Tensor,
              r1: Optional[Tensor] = None,
              r2: Optional[Tensor] = None,
              r3: Optional[Tensor] = None,
              r4: Optional[Tensor] = None,
              downsample_ratio: float = 1,
              segmentation_pass: bool = False,
              live_seg_pass: bool = False):

    if downsample_ratio != 1:
      src_sm = self._interpolate(src, scale_factor=downsample_ratio)
    else:
      src_sm = src

    f1, f2, f3, f4 = self.backbone(src_sm)
    f4 = self.aspp(f4)
    hid, *rec = self.decoder(src_sm, f1, f2, f3, f4, r1, r2, r3, r4)

    if not segmentation_pass and not live_seg_pass:
      fgr_residual, pha = self.project_mat(hid).split([3, 1], dim=-3)
      if downsample_ratio != 1:
        fgr_residual, pha = self.refiner(src, src_sm, fgr_residual, pha, hid)
      fgr = fgr_residual + src
      fgr = fgr.clamp(0., 1.)
      pha = pha.clamp(0., 1.)
      return [fgr, pha, *rec]
    elif segmentation_pass:
      seg = self.project_seg(hid)
      return [seg, *rec]
    else:
      seg = self.project_live_seg(hid)
      return [seg, *rec]

  def _interpolate(self, x: Tensor, scale_factor: float):
    if x.ndim == 5:
      B, T = x.shape[:2]
      x = F.interpolate(x.flatten(0, 1), scale_factor=scale_factor,
                        mode='bilinear', align_corners=False, recompute_scale_factor=False)
      x = x.unflatten(0, (B, T))
    else:
      x = F.interpolate(x, scale_factor=scale_factor,
                        mode='bilinear', align_corners=False, recompute_scale_factor=False)
    return x


class RobustVideoMatting(nn.Module):
  """Robust Video Matting

    mode: image, video, video_as_image
      - image: process a single image [N, C, H, W]
      - video: process a video [N, T, C, H, W]
      - video_as_image: process a video as a single image [N, C, H, W] but with temporal information rec

  """

  def __init__(self, variant='mobilenetv3', device='cpu', mode='image', checkpoint=None):
    super(RobustVideoMatting, self).__init__()
    assert variant in ['mobilenetv3', 'resnet50']
    assert mode in ['image', 'video', 'video_as_image']
    self.device = device
    self.mode = mode
    self.model = MattingNetwork(variant=variant).eval().to(device)

    if checkpoint is None:
      if variant == 'mobilenetv3':
        checkpoint = '/cephFS/video_lab/checkpoints/matting/rvm/rvm_mobilenetv3.pth'
      elif variant == 'resnet50':
        checkpoint = '/cephFS/video_lab/checkpoints/matting/rvm/rvm_resnet50.pth'

    state_dict = torch.load(checkpoint, map_location=device)
    tw.checkpoint.load_matched_state_dict(self.model, state_dict, verbose=False)

    self.model = torch.jit.script(self.model)
    self.model = torch.jit.freeze(self.model)

    # background
    self.bgr = torch.tensor([120, 255, 155], device=device).div(255).view(1, 1, 3, 1, 1)
    self.rec = [None] * 4

  def auto_downsample_ratio(self, h, w):
    """
    Automatically find a downsample ratio so that the largest side of the resolution be 512px.
    """
    return min(512 / max(h, w), 1)

  def reset(self):
    """reset network status, called for different videos
    """
    self.rec = [None] * 4

  @torch.no_grad()
  def process(self, frame, is_bgr=True):
    """require input frame in BGR [0, 255] in unit8/float type

    Args:
        frame (np.ndarray): [H, W, 3]
        is_bgr (bool, optional): whether the input frame is in BGR format. Defaults to True.

    Returns:
        pha (np.ndarray): [H, W]
        fgr (np.ndarray): [H, W, 3]
        com (np.ndarray): [H, W, 3]

    """
    if is_bgr:
      frame = frame[..., ::-1]

    inputs = torch.from_numpy(np.array(frame, dtype='float32') / 255.0)
    inputs = torch.permute(inputs, (2, 0, 1)).unsqueeze(0)

    pha, fgr, com = self.forward(inputs)

    pha = pha[0, 0].cpu().numpy()  # [H, W]
    fgr = fgr[0].permute(1, 2, 0).cpu().numpy()  # [H, W, 3]
    com = com[0].permute(1, 2, 0).cpu().numpy()  # [H, W, 3]

    return pha, fgr, com

  @torch.no_grad()
  def forward(self, src):
    """x is a tensor in [0, 1.0] float type in rgb

    Args:
        x (torch.Tensor): [N, 3, H, W]

    """
    device = self.device
    h, w = src.shape[-2:]

    # if downsample_ratio is None:
    downsample_ratio = self.auto_downsample_ratio(h, w)

    src = src.to(device, non_blocking=True).unsqueeze(0)  # [N, 1, C, H, W]
    fgr, pha, *rec = self.model(src, *self.rec,
                                downsample_ratio=downsample_ratio,
                                segmentation_pass=False,
                                live_seg_pass=False)

    com = pha * fgr + (1 - pha) * self.bgr

    if self.mode == 'video':
      self.rec = rec

    # [B, T, C, H, W] -> [1, C, H, W]
    return pha[0], fgr[0], com[0]


if __name__ == '__main__':
  net = RobustVideoMatting()
  inputs = torch.rand(1, 3, 720, 1280)
  net(inputs)
