# Copyright 2021 The KaiJIN Authors. All Rights Reserved.
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
"""VQA-III by semi-supervised method to calibrate result.
"""
import torch
from torch import nn
import tw
import tw.transform as T

default_urls = {
    'vqa-iii': '/cephFS/video_lab/checkpoints/quality_assess/vqa_v3/VQA_V3_YUV_211109.pth'
}


class MOSHead(nn.Module):

  def __init__(self, in_channels):
    super(MOSHead, self).__init__()
    self.head = nn.Sequential(
        nn.AdaptiveAvgPool2d(1),
        nn.Flatten(1),
        nn.Linear(in_channels, 1024),
        nn.BatchNorm1d(1024),
        nn.PReLU(),
        nn.Dropout(0.5),
        nn.Linear(1024, 512),
        nn.BatchNorm1d(512),
        nn.PReLU(),
        nn.Dropout(0.5),
        nn.Linear(512, 1))

  def forward(self, x):
    return self.head(x)


class AttributeHead(nn.Module):

  def __init__(self, in_channels, num_attr=1):
    super(AttributeHead, self).__init__()
    assert num_attr >= 1, "at least number of attributes should be larger than 1."
    self.num_attr = num_attr
    self.head = nn.Sequential(
        nn.AdaptiveAvgPool2d(1),
        nn.Flatten(1),
        nn.Linear(in_channels, 1024),
        nn.BatchNorm1d(1024),
        nn.PReLU(),
        nn.Dropout(0.5))

    # extra attribution
    if self.num_attr > 1:
      self.attrs = nn.ModuleList([nn.Sequential(
          nn.Linear(1024, 256),
          nn.BatchNorm1d(256),
          nn.PReLU(),
          nn.Linear(256, 1)) for _ in range(self.num_attr - 1)])

    # fuse extra attributions
    self.fuse = nn.Sequential(
        nn.Linear(1024 + num_attr - 1, 512),
        nn.BatchNorm1d(512),
        nn.PReLU(),
        nn.Dropout(0.5),
        nn.Linear(512, 1))

  def forward(self, x: torch.Tensor):
    """
      x -> head -> f_1024
      f_1024 -> attr[0] -> attr_0
      f_1024 -> attr[1] -> attr_1
      f_1024 -> attr[2] -> attr_2
      ...
      f_1024 -> fuse -> mos

    Args:
        x ([torch.Tensor]): [N, C, H, W] feature maps

    Returns:
        [mos + attribution]: [N, 1 + num_attr]
    """
    assert x.ndim == 4
    feature = self.head(x)

    # attributions
    if self.num_attr > 1:
      attrs = torch.cat([m(feature) for m in self.attrs], dim=1)
      mos = self.fuse(torch.cat([feature, attrs], dim=1))
      return torch.cat([mos, attrs], dim=1)
    else:
      mos = self.fuse(feature)
      return mos


class AttributeNet(nn.Module):
  """Attribution Network
  """

  def __init__(self, backbone, attrs=[6, ], pretrained=None, output_score_only=False, **kwargs):
    super(AttributeNet, self).__init__()
    self.output_score_only = output_score_only

    # backbone
    self.backbone = tw.models.mobilenet_v2.mobilenet_v2(pretrained=True, output_backbone=True)

    # attrs
    self.attrs = nn.ModuleList([AttributeHead(1280, attr) for attr in attrs])

    # load pretrained
    if pretrained is None:
      ckpt = tw.checkpoint.load(default_urls['vqa-iii'])
      tw.checkpoint.load_matched_state_dict(self, ckpt['state_dict'])

    # norm
    self.mean = torch.tensor([0.485, 0.456, 0.406]).reshape(1, 3, 1, 1)
    self.std = torch.tensor([0.229, 0.224, 0.225]).reshape(1, 3, 1, 1)

    # coeff
    self.coeffs = [
        [' vqa-ii ', 0.5186, 0.1850, 2.0000, -2.0000, True],
        ['  koniq ', 0.4789, 0.1782, 2.0000, -2.0000, True],
        ['live2005', 0.4277, 0.1302, 2.0000, -2.0000, False],
        ['  livec ', 0.4688, 0.2300, 2.0000, -2.0000, True],
        [' livemd ', 0.3814, 0.1430, 2.0000, -2.0000, False],
        [' tid2013', 0.4458, 0.1446, 2.0000, -2.0000, True],
        ['  csiq  ', 0.3168, 0.1540, 2.0000, -2.0000, False],
        ['  spaq  ', 0.6426, 0.1019, 2.0000, -2.0000, True],
        [' bright ', 0.6277, 0.1142, 1.7643, -2.0000, True],
        ['  color ', 0.6853, 0.0817, 1.9123, -2.0000, True],
        ['contrast', 0.6602, 0.0871, 1.6427, -2.0000, True],
        ['  noise ', 0.6715, 0.0702, 2.0000, -2.0000, True],
        ['  sharp ', 0.6626, 0.1045, 2.0000, -2.0000, True],
    ]

  def preprocess(self, x):
    """if inputs is a [1, C, H, W] in RGB [0, 1]
    """
    x = T.rgb_to_yuv709f(x, data_range=1.0)
    x = T.shortside_resize(x, min_size=448)
    x = T.center_crop_and_pad(x, height=672, width=448, fill_value=0)
    x = (x - self.mean.to(x)) / self.std.to(x)
    return x

  def forward(self, x):
    """
    Args:
        x ([torch.Tensor]): [N, C, H, W]

    Returns:
        [torch.Tensor]: [N, K]
    """
    c1, c2, c3, x = self.backbone(x)

    # attributes
    scores = [m(x) for m in self.attrs]

    # final list
    scores = torch.cat(scores, dim=1)

    return scores

  def postprocess(self, scores, **kwargs):
    """output final score
    """
    for col, v in enumerate(self.coeffs):
      name, mean, std, max_v, min_v, reverse = self.coeffs[col]
      scores[:, col] = (((scores[:, col] - mean) / std).clamp(min_v, max_v) - min_v) / (max_v - min_v)
      if not reverse:
        scores[:, col] = 1 - scores[:, col]
    final = (1 - scores[:, 6]) * scores[:, 6] + scores[:, 6] * scores[:, 0]
    return torch.cat([final.unsqueeze(dim=0), scores], dim=1)


if __name__ == "__main__":
  import tw
  model = AttributeNet(backbone='mobilenet_v2', attrs=[5, ])
  # print(model.state_dict().keys())
  model.eval()
  tw.flops.register(model)
  print(model(torch.rand(1, 3, 684, 484)).shape)
  print(tw.flops.accumulate(model))
