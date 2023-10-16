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
"""UNIQUE
"""
import torch
import torch.nn as nn
from torchvision import models

import tw


default_model_urls = {
    'resnet34': '/cephFS/video_lab/checkpoints/pretrained/unique_basecnn.pt',
}


class BCNN(nn.Module):
  def __init__(self, thresh=1e-8, is_vec=True, input_dim=512):
    super(BCNN, self).__init__()
    self.thresh = thresh
    self.is_vec = is_vec
    self.output_dim = input_dim * input_dim

  def _bilinearpool(self, x):
    batchSize, dim, h, w = x.data.shape
    x = x.reshape(batchSize, dim, h * w)
    x = 1. / (h * w) * x.bmm(x.transpose(1, 2))
    return x

  def _signed_sqrt(self, x):
    x = torch.mul(x.sign(), torch.sqrt(x.abs() + self.thresh))
    return x

  def _l2norm(self, x):
    x = nn.functional.normalize(x)
    return x

  def forward(self, x):
    x = self._bilinearpool(x)
    x = self._signed_sqrt(x)
    if self.is_vec:
      x = x.view(x.size(0), -1)
    x = self._l2norm(x)
    return x


class UNIQUE(nn.Module):

  def __init__(self,
               backbone='resnet34',
               std_modeling=True,
               representation_model='BCNN',
               fc=True,
               pretrained_model_path=None,
               **kwargs):
    """Declare all needed layers."""
    nn.Module.__init__(self)
    self.std_modeling = std_modeling
    self.representation_model = representation_model

    if backbone == 'resnet18':
      self.backbone = models.resnet18(pretrained=True)
    elif backbone == 'resnet34':
      self.backbone = models.resnet34(pretrained=True)
    elif backbone == 'resnet50':
      self.backbone = models.resnet50(pretrained=True)

    if std_modeling:
      outdim = 2
    else:
      outdim = 1

    if self.representation_model == 'BCNN':
      self.representation = BCNN()
      self.fc = nn.Linear(512 * 512, outdim)
    else:
      self.fc = nn.Linear(512, outdim)

    if fc:
      # Freeze all previous layers.
      for param in self.backbone.parameters():
        param.requires_grad = False
      # Initialize the fc layers.
      nn.init.kaiming_normal_(self.fc.weight.data)
      if self.fc.bias is not None:
        nn.init.constant_(self.fc.bias.data, val=0)

    if pretrained_model_path is None:
      ckpt = torch.load(default_model_urls[backbone])
      ckpt = tw.checkpoint.replace_prefix(ckpt, 'module.', '')
      tw.checkpoint.load_matched_state_dict(self, ckpt)

    self.mean = torch.Tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
    self.std = torch.Tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)

  def preprocess(self, x):
    x = tw.transform.adaptive_resize(x, 768, 768)
    x = (x - self.mean.to(x)) / self.std.to(x)
    return x

  def forward(self, x):
    """Forward pass of the network.
    """
    x = self.backbone.conv1(x)
    x = self.backbone.bn1(x)
    x = self.backbone.relu(x)
    x = self.backbone.maxpool(x)
    x = self.backbone.layer1(x)
    x = self.backbone.layer2(x)
    x = self.backbone.layer3(x)
    x = self.backbone.layer4(x)

    if self.representation_model == 'BCNN':
      x = self.representation(x)
    else:
      x = self.backbone.avgpool(x)
      x = torch.flatten(x, start_dim=1)

    x = self.fc(x)

    if self.std_modeling:
      mean = x[:, 0]
      t = x[:, 1]
      var = nn.functional.softplus(t)
      return mean, var
    else:
      return x

  def postprocess(self, mean, var):
    return mean
