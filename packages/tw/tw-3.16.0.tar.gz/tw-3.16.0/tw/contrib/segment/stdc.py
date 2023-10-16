#!/usr/bin/python
# -*- encoding: utf-8 -*-

import math

import cv2
import numpy as np

import torch
import torch.nn as nn
from torch.nn import init
import torch.nn.functional as F
from torch.nn import BatchNorm2d

import tw


class UpSample(nn.Module):

  def __init__(self, n_chan, factor=2):
    super(UpSample, self).__init__()
    out_chan = n_chan * factor * factor
    self.proj = nn.Conv2d(n_chan, out_chan, 1, 1, 0)
    self.up = nn.PixelShuffle(factor)
    self.init_weight()

  def forward(self, x):
    feat = self.proj(x)
    feat = self.up(feat)
    return feat

  def init_weight(self):
    nn.init.xavier_normal_(self.proj.weight, gain=1.)


class ConvX(nn.Module):
  def __init__(self, in_planes, out_planes, kernel=3, stride=1):
    super(ConvX, self).__init__()
    self.conv = nn.Conv2d(in_planes, out_planes, kernel_size=kernel, stride=stride, padding=kernel // 2, bias=False)
    self.bn = nn.BatchNorm2d(out_planes)
    self.relu = nn.ReLU(inplace=True)

  def forward(self, x):
    out = self.relu(self.bn(self.conv(x)))
    return out


class AddBottleneck(nn.Module):
  def __init__(self, in_planes, out_planes, block_num=3, stride=1):
    super(AddBottleneck, self).__init__()
    assert block_num > 1, print("block number should be larger than 1.")
    self.conv_list = nn.ModuleList()
    self.stride = stride
    if stride == 2:
      self.avd_layer = nn.Sequential(
          nn.Conv2d(
              out_planes // 2,
              out_planes // 2,
              kernel_size=3,
              stride=2,
              padding=1,
              groups=out_planes // 2,
              bias=False),
          nn.BatchNorm2d(out_planes // 2),
      )
      self.skip = nn.Sequential(
          nn.Conv2d(in_planes, in_planes, kernel_size=3, stride=2, padding=1, groups=in_planes, bias=False),
          nn.BatchNorm2d(in_planes),
          nn.Conv2d(in_planes, out_planes, kernel_size=1, bias=False),
          nn.BatchNorm2d(out_planes),
      )
      stride = 1

    for idx in range(block_num):
      if idx == 0:
        self.conv_list.append(ConvX(in_planes, out_planes // 2, kernel=1))
      elif idx == 1 and block_num == 2:
        self.conv_list.append(ConvX(out_planes // 2, out_planes // 2, stride=stride))
      elif idx == 1 and block_num > 2:
        self.conv_list.append(ConvX(out_planes // 2, out_planes // 4, stride=stride))
      elif idx < block_num - 1:
        self.conv_list.append(ConvX(out_planes // int(math.pow(2, idx)), out_planes // int(math.pow(2, idx + 1))))
      else:
        self.conv_list.append(ConvX(out_planes // int(math.pow(2, idx)), out_planes // int(math.pow(2, idx))))

  def forward(self, x):
    out_list = []
    out = x

    for idx, conv in enumerate(self.conv_list):
      if idx == 0 and self.stride == 2:
        out = self.avd_layer(conv(out))
      else:
        out = conv(out)
      out_list.append(out)

    if self.stride == 2:
      x = self.skip(x)

    return torch.cat(out_list, dim=1) + x


class CatBottleneck(nn.Module):
  def __init__(self, in_planes, out_planes, block_num=3, stride=1):
    super(CatBottleneck, self).__init__()
    assert block_num > 1, print("block number should be larger than 1.")
    self.conv_list = nn.ModuleList()
    self.stride = stride
    if stride == 2:
      self.avd_layer = nn.Sequential(
          nn.Conv2d(
              out_planes // 2,
              out_planes // 2,
              kernel_size=3,
              stride=2,
              padding=1,
              groups=out_planes // 2,
              bias=False),
          nn.BatchNorm2d(out_planes // 2),
      )
      self.skip = nn.AvgPool2d(kernel_size=3, stride=2, padding=1)
      stride = 1

    for idx in range(block_num):
      if idx == 0:
        self.conv_list.append(ConvX(in_planes, out_planes // 2, kernel=1))
      elif idx == 1 and block_num == 2:
        self.conv_list.append(ConvX(out_planes // 2, out_planes // 2, stride=stride))
      elif idx == 1 and block_num > 2:
        self.conv_list.append(ConvX(out_planes // 2, out_planes // 4, stride=stride))
      elif idx < block_num - 1:
        self.conv_list.append(ConvX(out_planes // int(math.pow(2, idx)), out_planes // int(math.pow(2, idx + 1))))
      else:
        self.conv_list.append(ConvX(out_planes // int(math.pow(2, idx)), out_planes // int(math.pow(2, idx))))

  def forward(self, x):
    out_list = []
    out1 = self.conv_list[0](x)

    for idx, conv in enumerate(self.conv_list[1:]):
      if idx == 0:
        if self.stride == 2:
          out = conv(self.avd_layer(out1))
        else:
          out = conv(out1)
      else:
        out = conv(out)
      out_list.append(out)

    if self.stride == 2:
      out1 = self.skip(out1)
    out_list.insert(0, out1)

    out = torch.cat(out_list, dim=1)
    return out

# STDC2Net


class STDCNet1446(nn.Module):
  def __init__(self, base=64, layers=[4, 5, 3], block_num=4, type="cat",
               num_classes=1000, dropout=0.20, pretrain_model='', use_conv_last=False):
    super(STDCNet1446, self).__init__()
    if type == "cat":
      block = CatBottleneck
    elif type == "add":
      block = AddBottleneck
    self.use_conv_last = use_conv_last
    self.features = self._make_layers(base, layers, block_num, block)
    self.conv_last = ConvX(base * 16, max(1024, base * 16), 1, 1)
    self.gap = nn.AdaptiveAvgPool2d(1)
    self.fc = nn.Linear(max(1024, base * 16), max(1024, base * 16), bias=False)
    self.bn = nn.BatchNorm1d(max(1024, base * 16))
    self.relu = nn.ReLU(inplace=True)
    self.dropout = nn.Dropout(p=dropout)
    self.linear = nn.Linear(max(1024, base * 16), num_classes, bias=False)

    self.x2 = nn.Sequential(self.features[:1])
    self.x4 = nn.Sequential(self.features[1:2])
    self.x8 = nn.Sequential(self.features[2:6])
    self.x16 = nn.Sequential(self.features[6:11])
    self.x32 = nn.Sequential(self.features[11:])

    if pretrain_model:
      print('use pretrain model {}'.format(pretrain_model))
      self.init_weight(pretrain_model)
    else:
      self.init_params()

  def init_weight(self, pretrain_model):

    state_dict = torch.load(pretrain_model)["state_dict"]
    self_state_dict = self.state_dict()
    for k, v in state_dict.items():
      self_state_dict.update({k: v})
    self.load_state_dict(self_state_dict)

  def init_params(self):
    for m in self.modules():
      if isinstance(m, nn.Conv2d):
        init.kaiming_normal_(m.weight, mode='fan_out')
        if m.bias is not None:
          init.constant_(m.bias, 0)
      elif isinstance(m, nn.BatchNorm2d):
        init.constant_(m.weight, 1)
        init.constant_(m.bias, 0)
      elif isinstance(m, nn.Linear):
        init.normal_(m.weight, std=0.001)
        if m.bias is not None:
          init.constant_(m.bias, 0)

  def _make_layers(self, base, layers, block_num, block):
    features = []
    features += [ConvX(3, base // 2, 3, 2)]
    features += [ConvX(base // 2, base, 3, 2)]

    for i, layer in enumerate(layers):
      for j in range(layer):
        if i == 0 and j == 0:
          features.append(block(base, base * 4, block_num, 2))
        elif j == 0:
          features.append(block(base * int(math.pow(2, i + 1)), base * int(math.pow(2, i + 2)), block_num, 2))
        else:
          features.append(block(base * int(math.pow(2, i + 2)), base * int(math.pow(2, i + 2)), block_num, 1))

    return nn.Sequential(*features)

  def forward(self, x):
    feat2 = self.x2(x)
    feat4 = self.x4(feat2)
    feat8 = self.x8(feat4)
    feat16 = self.x16(feat8)
    feat32 = self.x32(feat16)
    if self.use_conv_last:
      feat32 = self.conv_last(feat32)

    return feat2, feat4, feat8, feat16, feat32

  def forward_impl(self, x):
    out = self.features(x)
    out = self.conv_last(out).pow(2)
    out = self.gap(out).flatten(1)
    out = self.fc(out)
    # out = self.bn(out)
    out = self.relu(out)
    # out = self.relu(self.bn(self.fc(out)))
    out = self.dropout(out)
    out = self.linear(out)
    return out

# STDC1Net


class STDCNet813(nn.Module):
  def __init__(self, base=64, layers=[2, 2, 2], block_num=4, type="cat",
               num_classes=1000, dropout=0.20, pretrain_model='', use_conv_last=False):
    super(STDCNet813, self).__init__()
    if type == "cat":
      block = CatBottleneck   # STDC module
    elif type == "add":
      block = AddBottleneck
    self.use_conv_last = use_conv_last
    self.features = self._make_layers(base, layers, block_num, block)   # convx1, convx2, stage3, stage4, stage5
    self.conv_last = ConvX(base * 16, max(1024, base * 16), 1, 1)           # convx6
    self.gap = nn.AdaptiveAvgPool2d(1)
    self.fc = nn.Linear(max(1024, base * 16), max(1024, base * 16), bias=False)
    self.bn = nn.BatchNorm1d(max(1024, base * 16))
    self.relu = nn.ReLU(inplace=True)
    self.dropout = nn.Dropout(p=dropout)
    self.linear = nn.Linear(max(1024, base * 16), num_classes, bias=False)

    self.x2 = nn.Sequential(self.features[:1])      # convx1
    self.x4 = nn.Sequential(self.features[1:2])     # convx2
    self.x8 = nn.Sequential(self.features[2:4])     # stage3
    self.x16 = nn.Sequential(self.features[4:6])    # stage4
    self.x32 = nn.Sequential(self.features[6:])     # stage5

    if pretrain_model:
      print('use pretrain model {}'.format(pretrain_model))
      self.init_weight(pretrain_model)
    else:
      self.init_params()

  def init_weight(self, pretrain_model):

    state_dict = torch.load(pretrain_model)["state_dict"]
    self_state_dict = self.state_dict()
    for k, v in state_dict.items():
      self_state_dict.update({k: v})
    self.load_state_dict(self_state_dict)

  def init_params(self):
    for m in self.modules():
      if isinstance(m, nn.Conv2d):
        init.kaiming_normal_(m.weight, mode='fan_out')
        if m.bias is not None:
          init.constant_(m.bias, 0)
      elif isinstance(m, nn.BatchNorm2d):
        init.constant_(m.weight, 1)
        init.constant_(m.bias, 0)
      elif isinstance(m, nn.Linear):
        init.normal_(m.weight, std=0.001)
        if m.bias is not None:
          init.constant_(m.bias, 0)

  def _make_layers(self, base, layers, block_num, block):
    features = []
    features += [ConvX(3, base // 2, 3, 2)]
    features += [ConvX(base // 2, base, 3, 2)]

    for i, layer in enumerate(layers):
      for j in range(layer):
        if i == 0 and j == 0:
          features.append(block(base, base * 4, block_num, 2))
        elif j == 0:
          features.append(block(base * int(math.pow(2, i + 1)), base * int(math.pow(2, i + 2)), block_num, 2))
        else:
          features.append(block(base * int(math.pow(2, i + 2)), base * int(math.pow(2, i + 2)), block_num, 1))

    return nn.Sequential(*features)

  def forward(self, x):
    feat2 = self.x2(x)
    feat4 = self.x4(feat2)
    feat8 = self.x8(feat4)
    feat16 = self.x16(feat8)
    feat32 = self.x32(feat16)
    if self.use_conv_last:
      feat32 = self.conv_last(feat32)

    return feat2, feat4, feat8, feat16, feat32

  def forward_impl(self, x):
    out = self.features(x)
    out = self.conv_last(out).pow(2)
    out = self.gap(out).flatten(1)
    out = self.fc(out)
    # out = self.bn(out)
    out = self.relu(out)
    # out = self.relu(self.bn(self.fc(out)))
    out = self.dropout(out)
    out = self.linear(out)
    return out

# if __name__ == "__main__":
#     model = STDCNet813(num_classes=1000, dropout=0.00, block_num=4)
#     model.eval()
#     x = torch.randn(1,3,224,224)
#     y = model(x)
#     torch.save(model.state_dict(), 'cat.pth')
#     print(y.size())


##################################################################

class ConvBNReLU(nn.Module):
  def __init__(self, in_chan, out_chan, ks=3, stride=1, padding=1, *args, **kwargs):
    super(ConvBNReLU, self).__init__()
    self.conv = nn.Conv2d(in_chan,
                          out_chan,
                          kernel_size=ks,
                          stride=stride,
                          padding=padding,
                          bias=False)
    self.bn = BatchNorm2d(out_chan)
    # self.bn = BatchNorm2d(out_chan, activation='none')
    self.relu = nn.ReLU()
    self.init_weight()

  def forward(self, x):
    x = self.conv(x)
    x = self.bn(x)
    x = self.relu(x)
    return x

  def init_weight(self):
    for ly in self.children():
      if isinstance(ly, nn.Conv2d):
        nn.init.kaiming_normal_(ly.weight, a=1)
        if not ly.bias is None:
          nn.init.constant_(ly.bias, 0)


class BiSeNetOutput(nn.Module):
  def __init__(self, in_chan, mid_chan, n_classes, up_factor=-1, is_replace_upsample=False, *args, **kwargs):
    super(BiSeNetOutput, self).__init__()
    self.up_factor = up_factor
    self.conv = ConvBNReLU(in_chan, mid_chan, ks=3, stride=1, padding=1)
    self.conv_out = nn.Conv2d(mid_chan, n_classes, kernel_size=1, bias=True)
    self.is_replace_upsample = is_replace_upsample
    if self.up_factor > 1:
      self.up = UpSample(n_classes, self.up_factor) if is_replace_upsample else \
          nn.Upsample(scale_factor=self.up_factor, mode='bilinear', align_corners=False)
    self.init_weight()

  def forward(self, x):
    x = self.conv(x)
    x = self.conv_out(x)
    if self.up_factor > 1:
      x = self.up(x)
    return x

  def init_weight(self):
    for ly in self.children():
      if isinstance(ly, nn.Conv2d):
        nn.init.kaiming_normal_(ly.weight, a=1)
        if not ly.bias is None:
          nn.init.constant_(ly.bias, 0)

  def get_params(self):
    wd_params, nowd_params = [], []
    for name, module in self.named_modules():
      if isinstance(module, (nn.Linear, nn.Conv2d)):
        wd_params.append(module.weight)
        if not module.bias is None:
          nowd_params.append(module.bias)
      elif isinstance(module, BatchNorm2d):
        nowd_params += list(module.parameters())
    return wd_params, nowd_params


class AttentionRefinementModule(nn.Module):
  def __init__(self, in_chan, out_chan, *args, **kwargs):
    super(AttentionRefinementModule, self).__init__()
    self.conv = ConvBNReLU(in_chan, out_chan, ks=3, stride=1, padding=1)
    self.conv_atten = nn.Conv2d(out_chan, out_chan, kernel_size=1, bias=False)
    self.bn_atten = BatchNorm2d(out_chan)
    self.sigmoid_atten = nn.Sigmoid()
    self.init_weight()

  def forward(self, x):
    feat = self.conv(x)
    atten = torch.mean(feat, dim=(2, 3), keepdim=True)
    atten = self.conv_atten(atten)
    atten = self.bn_atten(atten)
    atten = self.sigmoid_atten(atten)
    out = torch.mul(feat, atten)
    return out

  def init_weight(self):
    for ly in self.children():
      if isinstance(ly, nn.Conv2d):
        nn.init.kaiming_normal_(ly.weight, a=1)
        if not ly.bias is None:
          nn.init.constant_(ly.bias, 0)


class ContextPath(nn.Module):
  def __init__(self, backbone='CatNetSmall', pretrain_model='',
               use_conv_last=False, is_replace_upsample=False, *args, **kwargs):
    super(ContextPath, self).__init__()

    if backbone == 'STDCNet1446':
      self.backbone = STDCNet1446(pretrain_model=pretrain_model, use_conv_last=use_conv_last)
    elif backbone == 'STDCNet813':
      self.backbone = STDCNet813(pretrain_model=pretrain_model, use_conv_last=use_conv_last)
    else:
      print("backbone is not in backbone lists")
      exit(0)

    self.arm16 = AttentionRefinementModule(512, 128)
    self.arm32 = AttentionRefinementModule(1024, 128)
    self.conv_head32 = ConvBNReLU(128, 128, ks=3, stride=1, padding=1)
    self.conv_head16 = ConvBNReLU(128, 128, ks=3, stride=1, padding=1)
    self.conv_avg = ConvBNReLU(1024, 128, ks=1, stride=1, padding=0)
    self.up32 = UpSample(128, 2) if is_replace_upsample else nn.Upsample(scale_factor=2.)
    self.up16 = UpSample(128, 2) if is_replace_upsample else nn.Upsample(scale_factor=2.)

    self.init_weight()

  def forward(self, x):
    feat2, feat4, feat8, feat16, feat32 = self.backbone(x)

    avg = torch.mean(feat32, dim=(2, 3), keepdim=True)
    avg = self.conv_avg(avg)

    feat32_arm = self.arm32(feat32)
    feat32_sum = feat32_arm + avg
    feat32_up = self.up32(feat32_sum)
    feat32_up = self.conv_head32(feat32_up)

    feat16_arm = self.arm16(feat16)
    feat16_sum = feat16_arm + feat32_up
    feat16_up = self.up16(feat16_sum)
    feat16_up = self.conv_head16(feat16_up)

    return feat2, feat4, feat8, feat16, feat16_up, feat32_up  # x8, x16

  def init_weight(self):
    for ly in self.children():
      if isinstance(ly, nn.Conv2d):
        nn.init.kaiming_normal_(ly.weight, a=1)
        if not ly.bias is None:
          nn.init.constant_(ly.bias, 0)

  def get_params(self):
    wd_params, nowd_params = [], []
    for name, module in self.named_modules():
      if isinstance(module, (nn.Linear, nn.Conv2d)):
        wd_params.append(module.weight)
        if not module.bias is None:
          nowd_params.append(module.bias)
      elif isinstance(module, BatchNorm2d):
        nowd_params += list(module.parameters())
    return wd_params, nowd_params


class FeatureFusionModule(nn.Module):
  def __init__(self, in_chan, out_chan, *args, **kwargs):
    super(FeatureFusionModule, self).__init__()
    self.convblk = ConvBNReLU(in_chan, out_chan, ks=1, stride=1, padding=0)
    # use conv-bn instead of 2 layer mlp, so that tensorrt 7.2.3.4 can work for fp16
    self.conv = nn.Conv2d(out_chan,
                          out_chan,
                          kernel_size=1,
                          stride=1,
                          padding=0,
                          bias=False)
    self.bn = nn.BatchNorm2d(out_chan)
    # self.conv1 = nn.Conv2d(out_chan,
    #         out_chan//4,
    #         kernel_size = 1,
    #         stride = 1,
    #         padding = 0,
    #         bias = False)
    # self.conv2 = nn.Conv2d(out_chan//4,
    #         out_chan,
    #         kernel_size = 1,
    #         stride = 1,
    #         padding = 0,
    #         bias = False)
    # self.relu = nn.ReLU(inplace=True)
    self.sigmoid = nn.Sigmoid()
    self.init_weight()

  def forward(self, fsp, fcp):
    fcat = torch.cat([fsp, fcp], dim=1)
    feat = self.convblk(fcat)
    atten = torch.mean(feat, dim=(2, 3), keepdim=True)
    atten = self.conv(atten)
    atten = self.bn(atten)
    # atten = self.conv1(atten)
    # atten = self.relu(atten)
    # atten = self.conv2(atten)
    atten = self.sigmoid(atten)
    feat_atten = torch.mul(feat, atten)
    feat_out = feat_atten + feat
    return feat_out

  def init_weight(self):
    for ly in self.children():
      if isinstance(ly, nn.Conv2d):
        nn.init.kaiming_normal_(ly.weight, a=1)
        if not ly.bias is None:
          nn.init.constant_(ly.bias, 0)

  def get_params(self):
    wd_params, nowd_params = [], []
    for name, module in self.named_modules():
      if isinstance(module, (nn.Linear, nn.Conv2d)):
        wd_params.append(module.weight)
        if not module.bias is None:
          nowd_params.append(module.bias)
      elif isinstance(module, BatchNorm2d):
        nowd_params += list(module.parameters())
    return wd_params, nowd_params


class BiSeNet(nn.Module):
  def __init__(self, backbone, seg_classes, sod_classes, aux_mode='train', pretrain_model='',
               use_conv_last=False, is_replace_upsample=False, mode='seg', is_onnx=False, *args, **kwargs):
    super(BiSeNet, self).__init__()
    self.cp = ContextPath(backbone, pretrain_model, use_conv_last=use_conv_last,
                          is_replace_upsample=is_replace_upsample)
    self.mode = mode
    self.seg_classes = seg_classes
    self.sod_classes = sod_classes
    self.is_onnx = is_onnx

    if backbone == 'STDCNet1446':
      conv_out_inplanes = 128
      sp2_inplanes = 32
      sp4_inplanes = 64
      sp8_inplanes = 256
      sp16_inplanes = 512
      inplane = sp8_inplanes + conv_out_inplanes

    elif backbone == 'STDCNet813':
      conv_out_inplanes = 128
      sp2_inplanes = 32
      sp4_inplanes = 64
      sp8_inplanes = 256
      sp16_inplanes = 512
      inplane = sp8_inplanes + conv_out_inplanes

    else:
      print("backbone is not in backbone lists")
      exit(0)

    self.ffm = FeatureFusionModule(inplane, 256)

    # seg and sod separately
    if self.mode == 'seg' or 'joint' in self.mode:
      self.seg_conv_out = BiSeNetOutput(256, 256, self.seg_classes, up_factor=8,
                                        is_replace_upsample=is_replace_upsample)
      self.aux_mode = aux_mode
      if self.aux_mode == 'train':
        self.seg_conv_out16 = BiSeNetOutput(conv_out_inplanes, 64, self.seg_classes,
                                            up_factor=8)  # no need to replace upsample for aux node
        self.seg_conv_out32 = BiSeNetOutput(conv_out_inplanes, 64, self.seg_classes, up_factor=16)
        self.seg_conv_out_detail = BiSeNetOutput(sp8_inplanes, 64, 1)   # res8 for detail

    if self.mode == 'sod' or 'joint' in self.mode:
      self.sod_conv_out = BiSeNetOutput(256, 256, self.sod_classes, up_factor=8, is_replace_upsample=False)
      self.aux_mode = aux_mode
      if self.aux_mode == 'train':
        self.sod_conv_out16 = BiSeNetOutput(conv_out_inplanes, 64, self.sod_classes,
                                            up_factor=8)  # no need to replace upsample for aux node
        self.sod_conv_out32 = BiSeNetOutput(conv_out_inplanes, 64, self.sod_classes, up_factor=16)
        self.sod_conv_out_detail = BiSeNetOutput(sp8_inplanes, 64, 1)   # res8 for detail

    self.init_weight()

  def forward(self, x):

    feat_res2, feat_res4, feat_res8, feat_res16, feat_cp8, feat_cp16 = self.cp(x)
    feat_fuse = self.ffm(feat_res8, feat_cp8)

    if self.mode == 'seg' or 'joint' in self.mode:
      # seg
      seg_feat_out = self.seg_conv_out(feat_fuse)
      seg_feat_out16 = self.seg_conv_out16(feat_cp8)
      seg_feat_out32 = self.seg_conv_out32(feat_cp16)
      seg_feat_out_d = self.seg_conv_out_detail(feat_res8)                # res8 for detail

    if self.mode == 'sod' or 'joint' in self.mode:
      # sod
      sod_feat_out = self.sod_conv_out(feat_fuse)
      sod_feat_out16 = self.sod_conv_out16(feat_cp8)
      sod_feat_out32 = self.sod_conv_out32(feat_cp16)
      sod_feat_out_d = self.sod_conv_out_detail(feat_res8)                # res8 for detail

    if self.mode == 'seg':
      return seg_feat_out, seg_feat_out16, seg_feat_out32, seg_feat_out_d
    elif self.mode == 'sod':
      return sod_feat_out, sod_feat_out16, sod_feat_out32, sod_feat_out_d
    elif self.mode == 'joint':
      return seg_feat_out, seg_feat_out16, seg_feat_out32, seg_feat_out_d, sod_feat_out, sod_feat_out16, sod_feat_out32, sod_feat_out_d
    elif self.mode == 'joint_pred':
      seg_feat_out = torch.argmax(seg_feat_out, dim=1, keepdim=True)
      sod_feat_out = torch.argmax(sod_feat_out, dim=1, keepdim=True)
      if self.is_onnx:
        return torch.cat((seg_feat_out, sod_feat_out), dim=1)
      else:
        return seg_feat_out, sod_feat_out

  def init_weight(self):
    for ly in self.children():
      if isinstance(ly, nn.Conv2d):
        nn.init.kaiming_normal_(ly.weight, a=1)
        if not ly.bias is None:
          nn.init.constant_(ly.bias, 0)

  def get_params(self):
    wd_params, nowd_params, lr_mul_wd_params, lr_mul_nowd_params = [], [], [], []
    for name, child in self.named_children():
      child_wd_params, child_nowd_params = child.get_params()
      if isinstance(child, (FeatureFusionModule, BiSeNetOutput)):
        lr_mul_wd_params += child_wd_params
        lr_mul_nowd_params += child_nowd_params
      else:
        wd_params += child_wd_params
        nowd_params += child_nowd_params
    return wd_params, nowd_params, lr_mul_wd_params, lr_mul_nowd_params


class STDCNet(nn.Module):

  """classes

    #ffffff 0 未定义 不属于以下任何一个类别的；
    #b71c1c 1 面部
    #ffccbc 2 面部外的皮肤
    #010101 3 头发
    #4a148c 4 服饰 包括衣服、裤子、帽子、头巾、口罩等；
    #969696 5 玩偶
    #0d47a1 6 话筒 麦克风的主体部分，不包含支架、电线等；
    #2196f3 7 头戴式耳机
    #006064 8 坐具 各种类型的椅子、凳子等；
    #f57f17 9 弦乐器 例如吉他、提琴、古筝等
    #fbc02d 10 管乐器 例如萨克斯、长笛、黑管等
    #ffeb3b 11 键盘乐器 例如电子琴、钢琴等的琴键部分
    #e65100 12 DJ控制器

  """

  def __init__(self,
               backbone='STDCNet813',
               num_classes=13,
               ckpt_path='/cephFS/video_lab/checkpoints/segment2d/model_joint_stdc_bilinear_0.87_0.95.pth',
               device='cpu'):
    super(STDCNet, self).__init__()
    self.device = device
    self.seg = BiSeNet(backbone,
                       seg_classes=num_classes,
                       sod_classes=2,
                       is_replace_upsample=False,
                       mode='joint_pred')
    self.seg.eval()
    self.seg.to(self.device)

    if ckpt_path is not None:
      tw.checkpoint.load_state_dict_from_url(self.seg, ckpt_path, verbose=False)

    self.mean = torch.tensor((0.5081, 0.4480, 0.4340)).reshape(1, 3, 1, 1).to(self.device)
    self.std = torch.tensor((0.2822, 0.2757, 0.2734)).reshape(1, 3, 1, 1).to(self.device)

  @torch.no_grad()
  def process(self, frame, is_bgr=True):
    """require input frame in BGR [0, 255] in unit8/float type
    """
    if is_bgr:
      frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = frame.astype('float32')

    # require input size is divisible by 32
    h, w = frame.shape[:2]
    input = tw.transform.pad_to_size_divisible(frame, size_divisible=32)
    input = tw.transform.to_tensor(input, scale=255.0, mean=(0.5081, 0.4480, 0.4340), std=(0.2822, 0.2757, 0.2734))
    input = input.unsqueeze(dim=0)
    seg_out, sod_out = self.seg(input.to(self.device))

    # [h, w] with classes value
    return seg_out[0, 0, :h, :w].cpu().numpy()

  @torch.no_grad()
  def forward(self, x):
    """x is a tensor in [0, 1.0] float type in rgb

    Args:
        x (torch.Tensor): [N, 3, H, W]
    """
    x = (x - self.mean.to(x)) / self.std.to(x)
    h, w = x.shape[-2:]

    x = tw.transform.pad_to_size_divisible(x, size_divisible=32)
    seg_out, sod_out = self.seg(x)

    return seg_out[..., :h, :w]

  def viz(self, seg_out):
    """render seg_out into differen colors
    """
    from PIL import ImageColor

    color_matrix = [
        ImageColor.getcolor('#ffffff', 'RGB')[::-1],
        ImageColor.getcolor('#b71c1c', 'RGB')[::-1],
        ImageColor.getcolor('#ffccbc', 'RGB')[::-1],
        ImageColor.getcolor('#010101', 'RGB')[::-1],
        ImageColor.getcolor('#4a148c', 'RGB')[::-1],
        ImageColor.getcolor('#969696', 'RGB')[::-1],
        ImageColor.getcolor('#0d47a1', 'RGB')[::-1],
        ImageColor.getcolor('#2196f3', 'RGB')[::-1],
        ImageColor.getcolor('#006064', 'RGB')[::-1],
        ImageColor.getcolor('#f57f17', 'RGB')[::-1],
        ImageColor.getcolor('#fbc02d', 'RGB')[::-1],
        ImageColor.getcolor('#ffeb3b', 'RGB')[::-1],
        ImageColor.getcolor('#e65100', 'RGB')[::-1],
    ]

    h, w = seg_out.shape
    out = np.zeros([h, w, 3]).astype('uint8')

    for idx, color in enumerate(color_matrix):
      out[seg_out == idx, :] = color

    return out


if __name__ == "__main__":
  model = STDCNet()
  img = cv2.imread('/data/jk/tw/assets/coco/people.jpg')
  model.process(img)
