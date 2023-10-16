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
"""https://git.sysop.bigo.sg/codec_policy/video_preprocess_policy/bigo_rvm_release
"""
import os
import cv2
import onnxruntime as ort
import numpy as np


class BigoRvm(object):
  def __init__(self, onnx_path='/cephFS/video_lab/checkpoints/matting/bigo_rvm_release/model/BigoRvm.onnx',
               infer_size=(432, 432), precision='fp32', device='cpu'):
    assert precision in ['fp32', 'fp16'], 'Invalid precision'
    assert device in ['cpu', 'cuda'], 'Invalid device'
    self.onnx_path = onnx_path
    self.infer_size = infer_size
    self.dt = np.float32 if precision == 'fp32' else np.float16
    self.lut = np.array([[255, 255, 255],
                         [183, 28, 28],
                         [255, 204, 188],
                         [1, 1, 1],
                         [74, 20, 140],
                         ], dtype=np.uint8)[..., ::-1]    # bgr
    self.device = device
    self.init_model()

  def init_model(self):
    if self.device == 'cuda':
      # Load model.
      self.sess = ort.InferenceSession(self.onnx_path, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])

      # Create an io binding.
      self.io = self.sess.io_binding()

      # Set output binding.
      for name in ['pha', 'seg', 'r1o', 'r2o', 'r3o', 'r4o']:
        self.io.bind_output(name, 'cuda')
    else:
      # Load model.
      self.sess = ort.InferenceSession(self.onnx_path, providers=['CPUExecutionProvider'])

    # Create rec.
    self.reset()

  def reset(self):
    self.rec = [np.zeros([1, 4, 216, 216], dtype=self.dt),
                np.zeros([1, 10, 108, 108], dtype=self.dt),
                np.zeros([1, 20, 54, 54], dtype=self.dt),
                np.zeros([1, 64, 27, 27], dtype=self.dt)]
    if self.device == 'cuda':
      self.rec = [ort.OrtValue.ortvalue_from_numpy(r, 'cuda') for r in self.rec]

  def __call__(self, frame):
    '''
    Args:
        frame (numpy ndarray): bgr frame with shape [H, W, 3]

    Returns:
        pha (numpy ndarray): alpha mask, [H, W]
        seg (numpy ndarray): segmentation mask, [H, W]
        pha_color (numpy ndarray): bgr alpha mask for visualization, [H, W, 3]
        seg_color (numpy ndarray): bgr segmentation mask for visualization, [H, W, 3]
    '''
    h, w, _ = frame.shape

    # bgr2rgb
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # resize
    dst_h, dst_w = self.infer_size
    s_frame = cv2.resize(frame_rgb, (dst_w, dst_h), interpolation=cv2.INTER_LINEAR)

    # infer
    s_frame = s_frame / 255.
    s_frame = s_frame[np.newaxis, ...].transpose((0, 3, 1, 2)).astype(self.dt)                      # [N, C, H, W]

    if self.device == 'cuda':
      self.io.bind_cpu_input('src', s_frame)
      self.io.bind_ortvalue_input('r1i', self.rec[0])
      self.io.bind_ortvalue_input('r2i', self.rec[1])
      self.io.bind_ortvalue_input('r3i', self.rec[2])
      self.io.bind_ortvalue_input('r4i', self.rec[3])

      self.sess.run_with_iobinding(self.io)

      pha, seg, *self.rec = self.io.get_outputs()

      # Only transfer `pha` and `seg` to CPU.
      pha = pha.numpy()
      seg = seg.numpy()
    else:
      pha, seg, *self.rec = self.sess.run(
          ['pha', 'seg', 'r1o', 'r2o', 'r3o', 'r4o'],
          {
              'src': ort.OrtValue.ortvalue_from_numpy(s_frame),
              'r1i': ort.OrtValue.ortvalue_from_numpy(self.rec[0]),
              'r2i': ort.OrtValue.ortvalue_from_numpy(self.rec[1]),
              'r3i': ort.OrtValue.ortvalue_from_numpy(self.rec[2]),
              'r4i': ort.OrtValue.ortvalue_from_numpy(self.rec[3])
          }
      )

    # [N, 1, H, W], float -> [H, W], float
    pha = pha.squeeze((0, 1)).astype(np.float32)
    # [N, 1, H, W], int64 -> [H, W], uint8
    seg = seg.squeeze((0, 1)).astype(np.uint8)

    # resize back
    pha = cv2.resize(pha, (w, h), interpolation=cv2.INTER_LINEAR)
    seg = cv2.resize(seg, (w, h), interpolation=cv2.INTER_NEAREST)

    # visual
    pha_color = np.repeat((pha * 255)[..., np.newaxis], 3, axis=2).astype(np.uint8)                 # [H, W, 3]
    seg_color = self.lut[seg]

    return pha, seg.astype('float32'), pha_color, seg_color


class BigoRvmLite(object):
  def __init__(self, onnx_path='/cephFS/video_lab/checkpoints/matting/bigo_rvm_release/model/BigoRvmLite.onnx',
               infer_size=(320, 320), precision='fp32', device='cpu'):
    assert precision in ['fp32', 'fp16'], 'Invalid precision'
    assert device in ['cpu', 'cuda'], 'Invalid device'
    self.onnx_path = onnx_path
    self.infer_size = infer_size
    self.dt = np.float32 if precision == 'fp32' else np.float16
    self.lut = np.array([[255, 255, 255],
                         [183, 28, 28],
                         [255, 204, 188],
                         [1, 1, 1],
                         [74, 20, 140],
                         ], dtype=np.uint8)[..., ::-1]    # bgr
    self.device = device
    self.init_model()

  def init_model(self):
    if self.device == 'cuda':
      # Load model.
      self.sess = ort.InferenceSession(self.onnx_path, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])

      # Create an io binding.
      self.io = self.sess.io_binding()

      # Set output binding.
      for name in ['pha', 'seg']:
        self.io.bind_output(name, 'cuda')
    else:
      # Load model.
      self.sess = ort.InferenceSession(self.onnx_path, providers=['CPUExecutionProvider'])

  def reset(self):
    pass

  def __call__(self, frame):
    '''
    Args:
        frame (numpy ndarray): bgr frame with shape [H, W, 3]

    Returns:
        pha (numpy ndarray): alpha mask, [H, W]
        seg (numpy ndarray): segmentation mask, [H, W]
        pha_color (numpy ndarray): bgr alpha mask for visualization, [H, W, 3]
        seg_color (numpy ndarray): bgr segmentation mask for visualization, [H, W, 3]
    '''
    h, w, _ = frame.shape

    # bgr2rgb
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # resize
    dst_h, dst_w = self.infer_size
    s_frame = cv2.resize(frame_rgb, (dst_w, dst_h), interpolation=cv2.INTER_LINEAR)

    # infer
    s_frame = s_frame / 255.
    s_frame = s_frame[np.newaxis, ...].transpose((0, 3, 1, 2)).astype(self.dt)                      # [N, C, H, W]

    if self.device == 'cuda':
      self.io.bind_cpu_input('src', s_frame)
      self.sess.run_with_iobinding(self.io)
      pha, seg = self.io.copy_outputs_to_cpu()
    else:
      pha, seg = self.sess.run(['pha', 'seg'], {'src': s_frame})

    # [N, 1, H, W], float -> [H, W], float
    pha = pha.squeeze((0, 1)).astype(np.float32)
    # [N, 1, H, W], int64 -> [H, W], uint8
    seg = seg.squeeze((0, 1)).astype(np.uint8)

    # resize back
    pha = cv2.resize(pha, (w, h), interpolation=cv2.INTER_LINEAR)
    seg = cv2.resize(seg, (w, h), interpolation=cv2.INTER_NEAREST)

    # visual
    pha_color = np.repeat((pha * 255)[..., np.newaxis], 3, axis=2).astype(np.uint8)                 # [H, W, 3]
    seg_color = self.lut[seg]

    return pha, seg.astype('float32'), pha_color, seg_color
