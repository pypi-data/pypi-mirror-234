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
import os
import time
import math

import cv2
import numpy as np

import torch
import torchvision

import tw
from tw import transform as T

from .facenet import FaceNet


img_mean = np.array([104., 117., 123.])[:, np.newaxis, np.newaxis].astype('float32')


class VOD3():

  def __init__(self, device='cuda:0',
               pretrain='/cephFS/video_lab/checkpoints/detection/bigolive_face_detector/bigolive_face_detector.mobilenet.Y.G17.giou.bbox.epoch-250.pth'):
    self.device = device

    # anchor setting
    anchor_sizes = [[8, 16], [32, 64], [128, 256]]
    anchor_strides = [8, 16, 32]
    anchor_ratios = [1.0, ]

    # build anchor
    self.Anchor = tw.nn.RetinaFaceAnchorGenerator(
        anchor_sizes=anchor_sizes,
        anchor_strides=anchor_strides,
        anchor_ratios=anchor_ratios)
    anchor_nums = [len(sizes) * len(anchor_ratios) for sizes in anchor_sizes]

    # model
    self.Model = FaceNet(
        arch='mobilenet',
        in_channels=1,
        fpn_in_channels=32,
        fpn_out_channels=64,
        anchor_num=anchor_nums)

    # load state dict
    ckpt = tw.checkpoint.load(pretrain, verbose=False)
    content = tw.checkpoint.replace_prefix(ckpt['state_dict'], 'module.', '')
    tw.checkpoint.load_matched_state_dict(self.Model, content, verbose=False)

    # box coder
    self.BoxCoder = tw.nn.GeneralBoxCoder(
        means=[0, 0, 0, 0],
        variances=[0.1, 0.1, 0.2, 0.2])

    # nms
    self.NMS = torchvision.ops.nms

    # inference
    self.Anchor.to(self.device)
    self.Model.eval().to(self.device)

  @torch.no_grad()
  def detect_faces(self, image, pre_conf_thresh=0.5, nms_thresh=0.4, post_conf_thresh=0.9, resize_longside=320, **kwargs):  # nopep8
    """detect faces

    Args:
      image: (h, w, 3) in BGR format [0, 255]

    """
    ih, iw = image.shape[:2]
    device = self.device

    if ih < iw:
      input_width = resize_longside
      input_height = int(ih * resize_longside / iw // 32 * 32)
    else:
      input_height = resize_longside
      input_width = int(iw * resize_longside / ih // 32 * 32)

    # resize frame into network
    ih, iw = image.shape[:2]
    resized_image = cv2.resize(image, (input_width, input_height), interpolation=cv2.INTER_LINEAR)
    h, w = resized_image.shape[:2]

    # compute ratio to restore
    rh = ih / h
    rw = iw / w

    # transform
    inputs = T.to_tensor(resized_image, mean=[104, 117, 123])
    inputs = T.change_colorspace(inputs, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.YUV709F)
    inputs = inputs[0][None].to(device).unsqueeze(0)

    # inference
    loc, conf, _, _ = self.Model(inputs)
    loc, conf = loc[0], conf[0]

    # use anchor to restore vanilla pts
    priorbox = self.Anchor.forward(
        [[math.ceil(h / 8), math.ceil(w / 8)],
         [math.ceil(h / 16), math.ceil(w / 16)],
         [math.ceil(h / 32), math.ceil(w / 32)]],
        img_h=h, img_w=w)
    priorbox = torch.cat(priorbox, dim=0)
    boxes = self.BoxCoder.decode(loc, priorbox)

    # postprocess
    select = conf[:, 1] > pre_conf_thresh
    boxes = torch.cat([boxes, conf[:, 1].unsqueeze(1)], dim=1)[select]
    nms_inds = self.NMS(
        boxes=boxes[:, :4],
        scores=boxes[:, 4],
        iou_threshold=nms_thresh)
    nms_boxes = boxes[nms_inds].cpu().numpy()
    post_select = nms_boxes[:, -1] > post_conf_thresh
    nms_boxes = nms_boxes[post_select]
    dets = nms_boxes * np.array([rw, rh, rw, rh, 1.0])

    # [[x1, y1, x2, y2, conf]]
    return dets
