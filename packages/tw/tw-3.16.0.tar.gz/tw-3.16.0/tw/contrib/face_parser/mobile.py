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
"""face parser
"""
import time
import numpy as np
import cv2

import tw
import tw.transform as T


class MobileFaceParser():

  """Sematics

    label	class
    0	background
    1	skin
    2	left eyebrow
    3	right eyebrow
    4	left eye
    5	right eye
    6	nose
    7	upper lip
    8	inner mouth
    9	lower lip
    10 hair

  """

  def __init__(self, path='/cephFS/video_lab/checkpoints/segment2d/fastscnn10_c11_cl_wrapper.onnx', use_bvt=True):
    import onnxruntime
    self.sess = onnxruntime.InferenceSession(path, providers=['CPUExecutionProvider'])
    self.use_bvt = use_bvt

    # face detector
    if self.use_bvt:
      import BVT
      self.detector = BVT.Engine()
      self.detector.init_humanface_module(faceDetection=True, faceLandmark=True, advancedLandmark=True)
    else:
      self.detector = tw.contrib.face_detection.VOD3(device='cpu')

  def process(self, frame):
    """frame in BGR [0, 255]
    """
    in_h = 256
    in_w = 256
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    # detection
    if self.use_bvt:
      result = self.detector.get_face(frame, det_interval=1, run_mode=0, run_level="platinum")
      if len(result) <= 0:
        return np.zeros_like(frame)[..., 0]  # [H, W]
      x1, y1, w, h = result[0].x, result[0].y, result[0].width, result[0].height
      x2 = x1 + w
      y2 = y1 + h
    else:
      bboxes = self.detector.detect_faces(frame)
      if len(bboxes) == 0:
        return np.zeros_like(frame)[..., 0]  # [H, W]
      # only process first face
      x1, y1, x2, y2, conf = bboxes[0]
      # convert to bvt size
      y1 = max(y2 - (x2 - x1), 0)
      w, h = x2 - x1, y2 - y1

    # crop 2x bbox
    ih, iw = frame.shape[:2]
    cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    side = w if w >= h else h

    # crop center to 2x
    cx1 = int(cx - side)
    cx2 = int(cx + side)
    cy1 = int(cy - side)
    cy2 = int(cy + side)
    ch, cw = cy2 - cy1, cx2 - cx1

    # crop source to dst
    crop = np.zeros([ch, cw, 3]).astype(frame.dtype)

    sy1 = max(cy1, 0)
    sy2 = min(cy1 + ch, ih)
    sx1 = max(cx1, 0)
    sx2 = min(cx1 + cw, iw)

    dy1 = 0
    dy2 = ch
    dx1 = 0
    dx2 = cw

    # actual crop size
    ach = min(dy2 - dy1, sy2 - sy1)
    acw = min(dx2 - dx1, sx2 - sx1)

    # update crop area
    sy2 = sy1 + ach
    sx2 = sx1 + acw
    dy2 = dy1 + ach
    dx2 = dx1 + acw

    # crop from frame
    crop[dy1:dy2, dx1:dx2] = frame[sy1:sy2, sx1:sx2]
    ch, cw = crop.shape[:2]

    rh, rw = ch / in_h, cw / in_w

    inp = cv2.resize(crop, (in_w, in_h), interpolation=cv2.INTER_LINEAR)
    inp = T.change_colorspace(inp, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    inp = (inp / 255.0 - mean) / std
    inp = np.transpose(inp, (2, 0, 1)).reshape(1, 3, in_h, in_w).astype('float32')

    inputs = {'input': inp}
    outputs = self.sess.run([], inputs)[0][0]
    outputs = np.transpose(outputs, (1, 2, 0))

    # return to vanilla image
    result = cv2.resize(outputs, (int(in_w * rw), int(in_h * rh)), interpolation=cv2.INTER_LINEAR)
    result = np.argmax(result, axis=2)

    final = np.zeros_like(frame)[..., 0]
    final[sy1:sy2, sx1:sx2] = result[dy1:dy2, dx1:dx2]

    return final

  def viz(self, seg_out):
    """visualize
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
        # ImageColor.getcolor('#e65100', 'RGB')[::-1],
    ]

    h, w = seg_out.shape
    out = np.zeros([h, w, 3]).astype('uint8')

    for idx, color in enumerate(color_matrix):
      out[seg_out == idx, :] = color

    return out
