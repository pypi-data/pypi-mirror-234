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
"""RetinaNet
"""
import torch
from torch import nn
from torch.nn import functional as F


def conv_bn(inp, oup, stride=1, leaky=0):
  return nn.Sequential(
      nn.Conv2d(inp, oup, 3, stride, 1, bias=False),
      nn.BatchNorm2d(oup),
      nn.LeakyReLU(negative_slope=leaky, inplace=True))


def conv_bn_no_relu(inp, oup, stride):
  return nn.Sequential(
      nn.Conv2d(inp, oup, 3, stride, 1, bias=False),
      nn.BatchNorm2d(oup))


def conv_bn1X1(inp, oup, stride, leaky=0):
  return nn.Sequential(
      nn.Conv2d(inp, oup, 1, stride, padding=0, bias=False),
      nn.BatchNorm2d(oup),
      nn.LeakyReLU(negative_slope=leaky, inplace=True))


def conv_dw(inp, oup, stride, leaky=0.1):
  return nn.Sequential(
      nn.Conv2d(inp, inp, 3, stride, 1, groups=inp, bias=False),
      nn.BatchNorm2d(inp),
      nn.LeakyReLU(negative_slope=leaky, inplace=True),
      nn.Conv2d(inp, oup, 1, 1, 0, bias=False),
      nn.BatchNorm2d(oup),
      nn.LeakyReLU(negative_slope=leaky, inplace=True))


class MobileNetV1(nn.Module):
  def __init__(self, in_channels):
    super(MobileNetV1, self).__init__()
    self.stage1 = nn.Sequential(
        conv_bn(in_channels, 8, 2, leaky=0.1),  # 3
        conv_dw(8, 16, 1),   # 7
        conv_dw(16, 32, 2),  # 11
        conv_dw(32, 32, 1),  # 19
        conv_dw(32, 64, 2),  # 27
        conv_dw(64, 64, 1),  # 43
    )
    self.stage2 = nn.Sequential(
        conv_dw(64, 128, 2),  # 43 + 16 = 59
        conv_dw(128, 128, 1),  # 59 + 32 = 91
        conv_dw(128, 128, 1),  # 91 + 32 = 123
        conv_dw(128, 128, 1),  # 123 + 32 = 155
        conv_dw(128, 128, 1),  # 155 + 32 = 187
        conv_dw(128, 128, 1),  # 187 + 32 = 219
    )
    self.stage3 = nn.Sequential(
        conv_dw(128, 256, 2),  # 219 +3 2 = 241
        conv_dw(256, 256, 1),  # 241 + 64 = 301
    )
    # self.avg = nn.AdaptiveAvgPool2d((1, 1))
    # self.fc = nn.Linear(256, 1000)

  def forward(self, x):
    x1 = self.stage1(x)
    x2 = self.stage2(x1)
    x3 = self.stage3(x2)
    # x = self.avg(x)
    # x = x.view(-1, 256)
    # x = self.fc(x)
    return x1, x2, x3


class SSH(nn.Module):
  def __init__(self, in_channel, out_channel):
    super(SSH, self).__init__()
    assert out_channel % 4 == 0
    leaky = 0
    if (out_channel <= 64):
      leaky = 0.1
    self.conv3X3 = conv_bn_no_relu(in_channel, out_channel // 2, stride=1)

    self.conv5X5_1 = conv_bn(in_channel, out_channel // 4, stride=1, leaky=leaky)
    self.conv5X5_2 = conv_bn_no_relu(out_channel // 4, out_channel // 4, stride=1)

    self.conv7X7_2 = conv_bn(out_channel // 4, out_channel // 4, stride=1, leaky=leaky)
    self.conv7x7_3 = conv_bn_no_relu(out_channel // 4, out_channel // 4, stride=1)

  def forward(self, input):
    conv3X3 = self.conv3X3(input)

    conv5X5_1 = self.conv5X5_1(input)
    conv5X5 = self.conv5X5_2(conv5X5_1)

    conv7X7_2 = self.conv7X7_2(conv5X5_1)
    conv7X7 = self.conv7x7_3(conv7X7_2)

    out = torch.cat([conv3X3, conv5X5, conv7X7], dim=1)
    out = F.relu(out)
    return out


class FPN(nn.Module):

  def __init__(self, in_channels_list, out_channels):
    super(FPN, self).__init__()
    leaky = 0
    if (out_channels <= 64):
      leaky = 0.1
    self.output1 = conv_bn1X1(in_channels_list[0], out_channels, stride=1, leaky=leaky)
    self.output2 = conv_bn1X1(in_channels_list[1], out_channels, stride=1, leaky=leaky)
    self.output3 = conv_bn1X1(in_channels_list[2], out_channels, stride=1, leaky=leaky)

    self.merge1 = conv_bn(out_channels, out_channels, leaky=leaky)
    self.merge2 = conv_bn(out_channels, out_channels, leaky=leaky)

  def forward(self, input):
    # names = list(input.keys())
    # input = list(input.values())

    output1 = self.output1(input[0])
    output2 = self.output2(input[1])
    output3 = self.output3(input[2])

    # print(output3.shape)  # 8
    # print(output2.shape)  # 16
    # print(output1.shape)  # 32

    # up3 = F.interpolate(output3, size=[int(output2.size(2)), int(output2.size(3))], mode="bilinear")
    up3 = F.interpolate(output3, scale_factor=2, mode="bilinear", align_corners=False)
    output2 = output2 + up3
    output2 = self.merge2(output2)

    # up2 = F.interpolate(output2, size=[int(output1.size(2)), int(output1.size(3))], mode="bilinear")
    up2 = F.interpolate(output2, scale_factor=2, mode="bilinear", align_corners=False)
    output1 = output1 + up2
    output1 = self.merge1(output1)

    out = [output1, output2, output3]
    return out

#!<----------------------------------------------------------------------------
#!< heads
#!<----------------------------------------------------------------------------


class ClassHead(nn.Module):
  def __init__(self, inchannels=512, num_anchors=3):
    super(ClassHead, self).__init__()
    self.num_anchors = num_anchors
    self.conv1x1 = nn.Conv2d(inchannels, self.num_anchors * 2, kernel_size=(1, 1), stride=1, padding=0)

  def forward(self, x):
    out = self.conv1x1(x)
    out = out.permute(0, 2, 3, 1).contiguous()

    return out.view(out.shape[0], -1, 2)


class BboxHead(nn.Module):
  def __init__(self, inchannels=512, num_anchors=3):
    super(BboxHead, self).__init__()
    self.conv1x1 = nn.Conv2d(inchannels, num_anchors * 4, kernel_size=(1, 1), stride=1, padding=0)
    self.conviou = nn.Conv2d(inchannels, num_anchors, kernel_size=(3, 3), stride=1, padding=1)

  def forward(self, x):
    out = self.conv1x1(x)
    out = out.permute(0, 2, 3, 1).contiguous()

    out_iou = self.conviou(x)
    out_iou = out_iou.permute(0, 2, 3, 1).contiguous()

    return out.view(out.shape[0], -1, 4), out_iou.view(out_iou.shape[0], -1, 1)


class LandmarkHead(nn.Module):
  def __init__(self, inchannels=512, num_anchors=3):
    super(LandmarkHead, self).__init__()
    self.conv1x1 = nn.Conv2d(inchannels, num_anchors * 10, kernel_size=(1, 1), stride=1, padding=0)

  def forward(self, x):
    out = self.conv1x1(x)
    out = out.permute(0, 2, 3, 1).contiguous()

    return out.view(out.shape[0], -1, 10)

#!<----------------------------------------------------------------------------
#!< retinaface
#!<----------------------------------------------------------------------------


class FaceNet(nn.Module):

  def __init__(self, arch='mobilenet',
               in_channels=3,
               fpn_in_channels=32,
               fpn_out_channels=64,
               anchor_num=[2, 2, 2]):
    super(FaceNet, self).__init__()

    if arch == 'mobilenet':
      self.body = MobileNetV1(in_channels=in_channels)

    else:
      raise NotImplementedError(arch)

    in_channels_stage2 = fpn_in_channels
    in_channels_list = [
        in_channels_stage2 * 2,
        in_channels_stage2 * 4,
        in_channels_stage2 * 8,
    ]
    out_channels = fpn_out_channels

    self.fpn = FPN(in_channels_list, out_channels)
    self.ssh1 = SSH(out_channels, out_channels)
    self.ssh2 = SSH(out_channels, out_channels)
    self.ssh3 = SSH(out_channels, out_channels)

    self.ClassHead = self._make_class_head(
        fpn_num=3,
        inchannels=fpn_out_channels,
        anchor_num=anchor_num)
    self.BboxHead = self._make_bbox_head(
        fpn_num=3,
        inchannels=fpn_out_channels,
        anchor_num=anchor_num)
    self.LandmarkHead = self._make_landmark_head(
        fpn_num=3,
        inchannels=fpn_out_channels,
        anchor_num=anchor_num)

  def _make_class_head(self, fpn_num=3, inchannels=64, anchor_num=[2, 2, 2]):
    classhead = nn.ModuleList()
    for i in range(fpn_num):
      classhead.append(ClassHead(inchannels, anchor_num[i]))
    return classhead

  def _make_bbox_head(self, fpn_num=3, inchannels=64, anchor_num=[2, 2, 2]):
    bboxhead = nn.ModuleList()
    for i in range(fpn_num):
      bboxhead.append(BboxHead(inchannels, anchor_num[i]))
    return bboxhead

  def _make_landmark_head(self, fpn_num=3, inchannels=64, anchor_num=[2, 2, 2]):
    landmarkhead = nn.ModuleList()
    for i in range(fpn_num):
      landmarkhead.append(LandmarkHead(inchannels, anchor_num[i]))
    return landmarkhead

  def forward(self, inputs):
    out = self.body(inputs)

    # FPN
    fpn = self.fpn(out)

    # SSH
    feature1 = self.ssh1(fpn[0])
    feature2 = self.ssh2(fpn[1])
    feature3 = self.ssh3(fpn[2])
    features = [feature1, feature2, feature3]

    bbox_reg, iou_reg, cls_score, ldm_reg = [], [], [], []
    for i, feature in enumerate(features):
      bbox, iou = self.BboxHead[i](feature)
      bbox_reg.append(bbox)
      cls_score.append(self.ClassHead[i](feature))
      iou_reg.append(iou)
      ldm_reg.append(self.LandmarkHead[i](feature))

    # [4032, 4] [4032, 1] [4032, 2] [4032, 10]
    bbox_reg = torch.cat(bbox_reg, dim=1)
    iou_reg = torch.cat(iou_reg, dim=1)
    cls_score = torch.cat(cls_score, dim=1)
    ldm_reg = torch.cat(ldm_reg, dim=1)

    if self.training:
      output = (bbox_reg, cls_score, ldm_reg, iou_reg)
    else:
      output = (bbox_reg, nn.functional.softmax(cls_score, dim=-1), ldm_reg, iou_reg)
      # output = (bbox_reg, nn.functional.softmax(cls_score, dim=-1))
    return output
