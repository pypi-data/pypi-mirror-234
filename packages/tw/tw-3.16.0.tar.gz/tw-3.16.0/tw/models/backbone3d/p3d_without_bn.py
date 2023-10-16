# Copyright 2018 The KaiJIN Authors. All Rights Reserved.
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
import math
import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
from torch.autograd import Variable
from functools import partial


def conv_S(in_planes, out_planes, stride=1, padding=1):
  # as is descriped, conv S is 1x3x3
  return nn.Conv3d(in_planes, out_planes, kernel_size=(1, 3, 3), stride=1,
                   padding=padding, bias=False)


def conv_T(in_planes, out_planes, stride=1, padding=1):
  # conv T is 3x1x1
  return nn.Conv3d(in_planes, out_planes, kernel_size=(3, 1, 1), stride=1,
                   padding=padding, bias=False)


def downsample_basic_block(x, planes, stride):
  out = F.avg_pool3d(x, kernel_size=1, stride=stride)
  zero_pads = torch.Tensor(out.size(0), planes - out.size(1),
                           out.size(2), out.size(3),
                           out.size(4)).zero_()
  if isinstance(out.data, torch.cuda.FloatTensor):
    zero_pads = zero_pads.cuda()

  out = Variable(torch.cat([out.data, zero_pads], dim=1))

  return out


class Bottleneck(nn.Module):
  expansion = 4

  def __init__(self, inplanes, planes, stride=1, downsample=None, n_s=0, depth_3d=47, ST_struc=('A', 'B', 'C')):
    super(Bottleneck, self).__init__()
    self.downsample = downsample
    self.depth_3d = depth_3d
    self.ST_struc = ST_struc
    self.len_ST = len(self.ST_struc)

    stride_p = stride
    if not self.downsample is None:
      stride_p = (1, 2, 2)
    if n_s < self.depth_3d:
      if n_s == 0:
        stride_p = 1
      self.conv1 = nn.Conv3d(
          inplanes, planes, kernel_size=1, bias=False, stride=stride_p)
    else:
      if n_s == self.depth_3d:
        stride_p = 2
      else:
        stride_p = 1
      self.conv1 = nn.Conv2d(
          inplanes, planes, kernel_size=1, bias=False, stride=stride_p)
    # self.conv2 = nn.Conv3d(planes, planes, kernel_size=3, stride=stride,
    #                        padding=1, bias=False)
    self.id = n_s
    self.ST = list(self.ST_struc)[self.id % self.len_ST]
    if self.id < self.depth_3d:
      self.conv2 = conv_S(planes, planes, stride=1, padding=(0, 1, 1))
      #
      self.conv3 = conv_T(planes, planes, stride=1, padding=(1, 0, 0))
    else:
      self.conv_normal = nn.Conv2d(
          planes, planes, kernel_size=3, stride=1, padding=1, bias=False)

    if n_s < self.depth_3d:
      self.conv4 = nn.Conv3d(planes, planes * 4, kernel_size=1, bias=False)
    else:
      self.conv4 = nn.Conv2d(planes, planes * 4, kernel_size=1, bias=False)
    self.relu = nn.ReLU(inplace=True)

    self.stride = stride

  def ST_A(self, x):
    x = self.conv2(x)
    x = self.relu(x)

    x = self.conv3(x)
    x = self.relu(x)

    return x

  def ST_B(self, x):
    tmp_x = self.conv2(x)
    tmp_x = self.relu(tmp_x)

    x = self.conv3(x)
    x = self.relu(x)

    return x + tmp_x

  def ST_C(self, x):
    x = self.conv2(x)
    x = self.relu(x)

    tmp_x = self.conv3(x)
    tmp_x = self.relu(tmp_x)

    return x + tmp_x

  def forward(self, x):
    residual = x

    out = self.conv1(x)
    out = self.relu(out)

    # out = self.conv2(out)
    # out = self.relu(out)
    if self.id < self.depth_3d:  # C3D parts:

      if self.ST == 'A':
        out = self.ST_A(out)
      elif self.ST == 'B':
        out = self.ST_B(out)
      elif self.ST == 'C':
        out = self.ST_C(out)
    else:
      out = self.conv_normal(out)  # normal is res5 part, C2D all.
      out = self.relu(out)

    out = self.conv4(out)

    if self.downsample is not None:
      residual = self.downsample(x)

    out += residual
    out = self.relu(out)

    return out


class P3D(nn.Module):

  def __init__(self, block, layers, modality='RGB',
               shortcut_type='B', num_classes=400, dropout=0.5, ST_struc=('A', 'B', 'C')):

    self.inplanes = 64
    super(P3D, self).__init__()
    # self.conv1 = nn.Conv3d(3, 64, kernel_size=7, stride=(1, 2, 2),
    #                        padding=(3, 3, 3), bias=False)
    self.input_channel = 3 if modality == 'RGB' else 2  # 2 is for flow
    self.ST_struc = ST_struc

    self.conv1_custom = nn.Conv3d(self.input_channel, 64, kernel_size=(1, 7, 7), stride=(1, 2, 2),
                                  padding=(0, 3, 3), bias=False)

    # C3D layers are only (res2,res3,res4),  res5 is C2D
    self.depth_3d = sum(layers[:3])

    self.cnt = 0
    self.relu = nn.ReLU(inplace=True)
    # pooling layer for conv1.
    self.maxpool = nn.MaxPool3d(kernel_size=(
        2, 3, 3), stride=2, padding=(0, 1, 1))
    self.maxpool_2 = nn.MaxPool3d(kernel_size=(2, 1, 1), padding=0,
                                  stride=(2, 1, 1))  # pooling layer for res2, 3, 4.

    self.layer1 = self._make_layer(block, 64, layers[0], shortcut_type)
    self.layer2 = self._make_layer(
        block, 128, layers[1], shortcut_type, stride=2)
    self.layer3 = self._make_layer(
        block, 256, layers[2], shortcut_type, stride=2)
    self.layer4 = self._make_layer(
        block, 512, layers[3], shortcut_type, stride=2)

    # pooling layer for res5.
    # [NOTE] we change 5x5 to 4x4 to fit with the input size
    self.avgpool = nn.AvgPool2d(kernel_size=(4, 4), stride=1)
    self.dropout = nn.Dropout(p=dropout)
    self.fc = nn.Linear(512 * block.expansion, num_classes)

    for m in self.modules():
      if isinstance(m, nn.Conv3d):
        n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
        m.weight.data.normal_(0, 0.01)  # math.sqrt(2. / n))

  def _make_layer(self, block, planes, blocks, shortcut_type, stride=1):
    downsample = None
    stride_p = stride  # especially for downsample branch.

    if self.cnt < self.depth_3d:
      if self.cnt == 0:
        stride_p = 1
      else:
        stride_p = (1, 2, 2)
      if stride != 1 or self.inplanes != planes * block.expansion:
        if shortcut_type == 'A':
          downsample = partial(downsample_basic_block,
                               planes=planes * block.expansion,
                               stride=stride)
        else:
          downsample = nn.Sequential(
              nn.Conv3d(self.inplanes, planes * block.expansion,
                        kernel_size=1, stride=stride_p, bias=False),
          )

    else:
      if stride != 1 or self.inplanes != planes * block.expansion:
        if shortcut_type == 'A':
          downsample = partial(downsample_basic_block,
                               planes=planes * block.expansion,
                               stride=stride)
        else:
          downsample = nn.Sequential(
              nn.Conv2d(self.inplanes, planes * block.expansion,
                        kernel_size=1, stride=2, bias=False),
          )
    layers = []
    layers.append(block(self.inplanes, planes, stride, downsample, n_s=self.cnt, depth_3d=self.depth_3d,
                        ST_struc=self.ST_struc))
    self.cnt += 1

    self.inplanes = planes * block.expansion
    for i in range(1, blocks):
      layers.append(block(self.inplanes, planes, n_s=self.cnt,
                          depth_3d=self.depth_3d, ST_struc=self.ST_struc))
      self.cnt += 1

    return nn.Sequential(*layers)

  def forward(self, x):
    x = self.conv1_custom(x)
    x = self.relu(x)
    x = self.maxpool(x)

    x = self.maxpool_2(self.layer1(x))  # Part Res2
    x = self.maxpool_2(self.layer2(x))  # Part Res3
    x = self.maxpool_2(self.layer3(x))  # Part Res4

    sizes = x.size()
    x = x.view(-1, sizes[1], sizes[3], sizes[4])  # Part Res5
    x = self.layer4(x)
    x = self.avgpool(x)

    x = x.view(-1, self.fc.in_features)
    x = self.fc(self.dropout(x))

    return x


def P3D63_without_bn(**kwargs):
  """Construct a P3D63 modelbased on a ResNet-50-3D model.
  """
  model = P3D(Bottleneck, [3, 4, 6, 3], **kwargs)
  return model


def P3D131_without_bn(**kwargs):
  """Construct a P3D131 model based on a ResNet-101-3D model.
  """
  model = P3D(Bottleneck, [3, 4, 23, 3], **kwargs)
  return model


def P3D199_without_bn(modality='RGB', **kwargs):
  """construct a P3D199 model based on a ResNet-152-3D model.
  """
  model = P3D(Bottleneck, [3, 8, 36, 3], modality=modality, **kwargs)
  return model


if __name__ == '__main__':
  model = P3D199(pretrained=True, num_classes=400)
  model = model.cuda()
  # if modality=='Flow', please change the 2nd dimension 3==>2
  data = torch.autograd.Variable(torch.rand(10, 3, 16, 160, 160)).cuda()
  out = model(data)
  print(out.size(), out)
