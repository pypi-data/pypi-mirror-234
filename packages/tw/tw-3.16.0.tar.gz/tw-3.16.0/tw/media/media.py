# Copyright 2017 The KaiJIN Authors. All Rights Reserved.
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
r"""Stream Media
"""
import os
import cv2
import glob
import tqdm
import functools
import subprocess
import numpy as np

import torch

from tw.utils.parser import parse_from_text
from tw.utils.logger import logger
from tw.utils import timer

import tw.transform as T

try:
  import ffmpeg
except ImportError:
  ffmpeg = None


IMAGE_EXT = ['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'bmp', 'BMP', 'tif']
VIDEO_EXT = ['mp4', 'avi', 'qt', 'mov']
YUV_EXT = ['yuv', 'bin']
RAW_EXT = ['cr2', 'CR2', 'nef', 'NEF', 'arw', 'ARW']
POINTCLOUD_EXT = ['ply', 'PLY']

#!<-----------------------------------------------------------------------------
#!< file
#!<-----------------------------------------------------------------------------


def is_image(filepath: str, if_check_path=True):
  if if_check_path and not os.path.exists(filepath):
    return False
  if if_check_path and not os.path.isfile(filepath):
    return False
  for ext in IMAGE_EXT:
    if filepath.lower().endswith(ext):
      return True
  return False


def is_video(filepath: str, if_check_path=True):
  if if_check_path and not os.path.exists(filepath):
    return False
  if if_check_path and not os.path.isfile(filepath):
    return False
  for ext in VIDEO_EXT:
    if filepath.lower().endswith(ext):
      return True
  return False


def collect(path: str, salience=False, if_check_path=True):
  """Collect all images/videos:
    1. from .txt file
    2. traverse all folder

  Args:
    path: a txt filepath or a folder path

  Returns:
    list (image_files, video_files)

  """
  image_files = []
  video_files = []

  if not os.path.exists(path):
    raise FileNotFoundError(path)

  if path.endswith('.txt') and os.path.isfile(path):
    res, _ = parse_from_text(path, [str, ], [True, ], if_check_path=if_check_path)
    for lq in res[0]:
      if is_image(lq, if_check_path=if_check_path):
        image_files.append(lq)
      elif is_video(lq, if_check_path=if_check_path):
        video_files.append(lq)

  elif os.path.isfile(path):
    if is_image(path, if_check_path=if_check_path):
      image_files.append(path)
    elif is_video(path, if_check_path=if_check_path):
      video_files.append(path)

  elif os.path.isdir(path):
    for root, _, fnames in os.walk(path):
      for name in fnames:
        filepath = os.path.join(root, name)
        if is_video(filepath, if_check_path=if_check_path):
          video_files.append(filepath)
        elif is_image(filepath, if_check_path=if_check_path):
          image_files.append(filepath)

  else:
    raise "Unknown input path attribution %s." % path

  if not salience:
    logger.info('Total loading %d image.' % len(image_files))
    logger.info('Total loading %d video.' % len(video_files))

  return image_files, video_files


#!<-----------------------------------------------------------------------------
#!< video <-> image
#!<-----------------------------------------------------------------------------

def video_to_image(filepath, transform=None):
  r"""Video to images

  Args:
    filepath: file path
    transform(optional): transform for every image

  """
  if not os.path.exists(filepath):
    raise FileNotFoundError(filepath)

  def _to_images(video_path, transform=None):
    vidcap = cv2.VideoCapture(video_path)
    total = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    success, frame = vidcap.read()

    img_root = os.path.join(os.path.splitext(video_path)[0])
    if not os.path.exists(img_root):
      os.makedirs(img_root)

    count = 0
    for _ in tqdm.tqdm(range(total)):
      img_path = os.path.join(img_root, '%08d.png' % count)
      if transform:
        frame = transform(frame)
      cv2.imwrite(img_path, frame)
      success, frame = vidcap.read()
      count += 1

  if os.path.isfile(filepath):
    _to_images(filepath, transform)
  else:
    for name in tqdm.tqdm(sorted(os.listdir(filepath))):
      video_path = os.path.join(filepath, name)
      if is_video(video_path):
        _to_images(video_path, transform)


def image_to_video(image_folder, video_path, fps=30):
  r"""Image to video
  """
  fourcc = cv2.VideoWriter_fourcc(*'XVID')
  for idx, name in enumerate(sorted(os.listdir(image_folder))):
    img_path = os.path.join(image_folder, name)
    assert os.path.exists(img_path)
    frame = cv2.imread(img_path)
    if idx == 0:
      h, w, c = frame.shape
      out = cv2.VideoWriter(video_path, fourcc, fps, (w, h))
    else:
      nh, nw, nc = frame.shape
      assert nh == h and nw == w and nc == c
    out.write(frame)
  out.release()


#!<-----------------------------------------------------------------------------
#!< video transcode
#!<-----------------------------------------------------------------------------

def video_transcode(video_path: str, codec='libx264', crf=24, output_path=None):
  r"""Video transcode (ffmpeg)
  """
  if output_path:
    dst_path = output_path
  else:
    dst_path = '%s.%s.%d.mp4' % (os.path.splitext(video_path)[0], codec, crf)

  # -vsync parameter
  # Video sync method. For compatibility reasons old values can be specified
  # as numbers. Newly added values will have to be specified as strings
  # always.

  # 0, passthrough
  # Each frame is passed with its timestamp from the demuxer to the muxer.

  # 1, cfr
  # Frames will be duplicated and dropped to achieve exactly the requested constant frame rate.

  # 2, vfr
  # Frames are passed through with their timestamp or dropped so as to prevent 2 frames from having the same timestamp.

  # drop
  # As passthrough but destroys all timestamps, making the muxer generate fresh timestamps based on frame-rate.

  # -1, auto
  # Chooses between 1 and 2 depending on muxer capabilities. This is the default method.

  # The presence of -an disables audio stream selection for video.

  cmd = 'ffmpeg -y -i {} -threads 16 -vsync 0 -c:v {} -pix_fmt yuvj420p -an -crf {} {}'.format(video_path, codec, crf, dst_path)  # nopep8
  logger.info(cmd)
  return subprocess.call(cmd, shell=True)


def video_resize(video_path: str, target_h, target_w, output_path):
  cmd = 'ffmpeg -y -i {} -vsync 0 -threads 16 -vf scale={}:{} -pix_fmt yuvj420p -strict -2 {}'.format(
      video_path, target_w, target_h, output_path)
  logger.info(cmd)
  return subprocess.call(cmd, shell=True)


class YuvReader():
  def __init__(self, path: str, height: int, width: int, separate=False):
    assert os.path.exists(path)
    self.size = height * width + height * width // 2
    self.handle = open(path, 'rb')
    self.count = os.path.getsize(path) // self.size

    assert height > 0 and height % 2 == 0
    assert width > 0 and width % 2 == 0
    self.height = height
    self.width = width
    self.separate = separate

    # preload first
    h, w = height, width
    s = width * height
    uPlanePos = s
    vPlanePos = s + (width // 2) * (height // 2)

    self.frames = []
    for i in range(self.count):
      arr = np.array([i for i in self.handle.read(self.size)]).astype('uint8')
      y = arr[:uPlanePos]
      u = arr[uPlanePos: vPlanePos]
      v = arr[vPlanePos:]
      y = np.reshape(y, [h, w])
      u = u.reshape(h // 2, w // 2)
      v = v.reshape(h // 2, w // 2)
      if self.separate:
        self.frames.append([y, u, v])
      else:
        u = cv2.resize(u, dsize=(w, h))
        v = cv2.resize(v, dsize=(w, h))
        yuv = np.stack([y, u, v], axis=2)
        self.frames.append(yuv)

  def __len__(self):
    return len(self.frames)

  def __getitem__(self, idx):
    return self.frames[idx]

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    self.handle.close()


class YuvWriter():
  def __init__(self, path: str, height: int, width: int):
    assert height > 0 and height % 2 == 0
    assert width > 0 and width % 2 == 0
    self.height = height
    self.width = width
    self.handle = open(path, 'wb')

  def __len__(self):
    return len(self.frames)

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    self.handle.close()

  def write(self, y: np.ndarray, u: np.ndarray, v: np.ndarray):
    assert y.shape[0] == self.height and y.shape[1] == self.width
    assert u.shape[0] == self.height // 2 and u.shape[1] == self.width // 2
    assert v.shape[0] == self.height // 2 and v.shape[1] == self.width // 2

    self.handle.write(y.astype('uint8').tobytes())
    self.handle.write(u.astype('uint8').tobytes())
    self.handle.write(v.astype('uint8').tobytes())


class VideoReader():

  def __init__(self, path: str, to_rgb=False, to_tensor=False):
    self.cap = cv2.VideoCapture(path)
    self.frame = None
    self.to_rgb = to_rgb
    self.to_tensor = to_tensor

    if not self.cap.isOpened():
      logger.warn('Failed to open {}'.format(path))
      self.valid = False
      self.fps = -1
      self.width = -1
      self.height = -1
      self.count = 0

    else:
      self.valid = True
      self.fps = self.cap.get(cv2.CAP_PROP_FPS)
      self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
      self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
      self.count = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)

  def __len__(self):
    return int(self.count)

  def __getitem__(self, idx):
    # return a clip
    if isinstance(idx, slice):
      return [self[i] for i in range(*idx.indices(len(self)))]

    if self.cap.get(cv2.CAP_PROP_POS_FRAMES) != idx:
      self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx)

    ret, img = self.cap.read()
    if not ret:
      raise IndexError

    if self.to_rgb:
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if self.to_tensor:
      img = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0

    return img

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    self.cap.release()


class VideoWriter():

  def __init__(self, path: str, width: int, height: int, fps: float):
    self.cap = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(width), int(height)))

  def write_tensor(self, tensor, is_rgb=True):
    r"""Assume tensor is [0~1] [N, C, H, W] float32 format.
    """
    frames = tensor.mul(255).byte().cpu().permute(0, 2, 3, 1).numpy()
    for i in range(frames.shape[0]):
      if is_rgb:
        self.cap.write(cv2.cvtColor(frames[i], cv2.COLOR_RGB2BGR))
      else:
        self.cap.write(frames[i])

  def write(self, array: np.array):
    if array.ndim == 3:
      self.cap.write(array)
    elif array.ndim == 4:
      for i in range(array.shape[0]):
        self.cap.write(array[i])

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    self.cap.release()


class FolderReader():
  """Loading images from folder
  """

  def __init__(self, path: str, ext='.png', to_rgb=False, to_tensor=False):
    self.files = sorted(glob.glob(f'{path}/*{ext}'))
    self.count = len(self.files)
    self.to_rgb = to_rgb
    self.to_tensor = to_tensor

  def __getitem__(self, idx):
    # return a clip
    if isinstance(idx, slice):
      return [self[i] for i in range(*idx.indices(len(self)))]
    img = cv2.imread(self.files[idx])
    if self.to_rgb:
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if self.to_tensor:
      img = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0
    return img


class FolderWriter():
  """Writing images to folder
  """

  def __init__(self, path: str):
    self.count = 0
    self.dst = path
    if not os.path.exists(self.dst):
      os.system(f'mkdir -p {self.dst}')

  def write(self, array: np.array):
    if array.ndim == 3:
      self.count += 1
      cv2.imwrite('{}/{:08d}.png'.format(self.dst, self.count), array)
    elif array.ndim == 4:
      for i in range(array.shape[0]):
        self.count += 1
        cv2.imwrite('{}/{:08d}.png'.format(self.dst, self.count), array[i])


class FFmpegReader():
  """Becuase using OpenCV will result in color mismatch between bt601 and bt709,
    we use ffmpeg to decode the mp4 and then loading png format image.
  """

  def convert_yuv_to_bgr(self, inputs, color_space, color_range, to_rgb=False):
    """Convert yuv420 to bgr
    """
    dst = T.COLORSPACE.RGB if to_rgb else T.COLORSPACE.BGR

    if color_space == 'bt709' and color_range == 'tv':
      src = T.COLORSPACE.YUV709V
    elif color_space == 'bt709' and color_range == 'pc':
      src = T.COLORSPACE.YUV709F
    elif color_space == 'bt601' and color_range == 'tv':
      src = T.COLORSPACE.YUV601V
    elif color_space == 'bt601' and color_range == 'pc':
      src = T.COLORSPACE.YUV601F
    elif color_space == 'bt470bg' and color_range == 'tv':
      src = T.COLORSPACE.YUV601V
    elif color_space == 'bt470bg' and color_range == 'pc':
      src = T.COLORSPACE.YUV601F
    else:
      raise NotImplementedError(f'Unknown color_space {color_space} or color_range {color_range}')

    return T.change_colorspace(inputs, src, dst)

  def __init__(self, path: str, to_rgb=False, to_tensor=False, **kwargs):
    """Default to BGR colorspace
    """
    probe = ffmpeg.probe(path, v='error')
    stream = probe['streams'][0]
    pix_fmt = 'rgb24' if to_rgb else 'bgr24'
    self.to_tensor = to_tensor

    # video parameters
    self.valid = True
    avg_rate = stream.get('avg_frame_rate', 0).split('/')
    self.fps = float(avg_rate[0]) / float(avg_rate[1])
    self.width = int(stream.get('width', -1))
    self.height = int(stream.get('height', -1))
    self.count = int(stream.get('nb_frames', -1))
    self.pix_fmt = stream.get('pix_fmt', 'yuv420p')
    self.color_range = stream.get('color_range', 'tv')
    self.color_space = stream.get('color_space', 'bt709')
    self.bitrate = int(stream.get('bit_rate', -1))

    # preload all frames: automatically convert to yuv444p
    # scale=in_color_matrix=bt709:in_range=pc
    out, _ = (
        ffmpeg
        .input(path, v='error', vsync=0)
        .output('pipe:', format='rawvideo', vsync=0, pix_fmt='yuv420p')
        .run(capture_stdout=True)
    )

    frames = np.frombuffer(out, np.uint8).reshape([-1, int(self.height * self.width * 1.5)])
    self.frames = []
    for frame in frames:
      frame = T.yuv420_to_yuv444(frame, self.height, self.width, interpolation=T.RESIZE_MODE.BILINEAR)
      frame = self.convert_yuv_to_bgr(frame, self.color_space, self.color_range, to_rgb)
      self.frames.append(frame)
    self.count = len(self.frames)

  def __len__(self):
    return int(self.count)

  def __getitem__(self, idx):
    # return a clip
    if isinstance(idx, slice):
      return [self[i] for i in range(*idx.indices(len(self)))]

    if idx >= self.count:
      raise IndexError

    img = self.frames[idx]

    if self.to_tensor:
      img = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0

    return img

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    pass


class FFmpegWriter():

  def convert_bgr_to_yuv(self, inputs, color_space, color_range, from_rgb=False):
    """Convert yuv420 to bgr
    """
    src = T.COLORSPACE.RGB if from_rgb else T.COLORSPACE.BGR

    if color_space == 'bt709' and color_range == 'tv':
      dst = T.COLORSPACE.YUV709V
    elif color_space == 'bt709' and color_range == 'pc':
      dst = T.COLORSPACE.YUV709F
    elif color_space == 'bt601' and color_range == 'tv':
      dst = T.COLORSPACE.YUV601V
    elif color_space == 'bt601' and color_range == 'pc':
      dst = T.COLORSPACE.YUV601F
    elif color_space == 'bt470bg' and color_range == 'tv':
      dst = T.COLORSPACE.YUV601V
    elif color_space == 'bt470bg' and color_range == 'pc':
      dst = T.COLORSPACE.YUV601F
    else:
      raise NotImplementedError(f'Unknown color_space {color_space} or color_range {color_range}')

    return T.change_colorspace(inputs, src, dst)

  def __init__(self,
               path: str,
               width: int,
               height: int,
               fps: float,
               crf=12,
               color_range='tv',
               color_space='bt709',
               pix_fmt='yuv420p'):
    """Default from BGR colorspace"""
    assert color_range in ['tv', 'pc'], f'color_range should be tv or pc, but got {color_range}'
    assert color_space in ['bt709', 'bt601', 'bt470bg'], f'color_space should be bt709 or bt601, but got {color_space}'
    assert pix_fmt in ['yuv420p', 'yuvj420p'], f'pix_fmt should be yuv420p, yuvj420p, but got {pix_fmt}'

    self.color_space = color_space
    self.color_range = color_range
    self.pix_fmt = pix_fmt
    self.width = width
    self.height = height

    s = '{}x{}'.format(width, height)
    self.pipeline = (
        ffmpeg
        .input('pipe:', format='rawvideo', pix_fmt='yuv420p', s=s, v='error', vsync=0)
        .output(path,
                crf=crf,
                preset='veryslow',
                pix_fmt=pix_fmt,
                vcodec='h264',
                s=s,
                colorspace=self.color_space,
                color_range=self.color_range,
                framerate=fps,
                v='error',
                vsync=0)
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )

  def write(self, frame, from_rgb=False):
    """write BGR frame (0-255) to video file
    """
    # require input tensor should be [0 ~ 1]
    if isinstance(frame, torch.Tensor):
      if frame.ndim == 4:
        assert frame.size(0) == 1
        frame = frame[0]
      frame = frame.mul(255).round().clip(0, 255).byte().cpu().permute(1, 2, 0).numpy()

    # numpy datatype
    else:
      frame = frame.round().clip(0, 255).astype('uint8')

    # bgr to yuv444
    frame = self.convert_bgr_to_yuv(frame, self.color_space, self.color_range, from_rgb)

    # yuv444 to yuv420
    frame = T.yuv444_to_yuv420(frame, self.height, self.width, interpolation=T.RESIZE_MODE.BILINEAR)

    # write to ffmpeg
    self.pipeline.stdin.write(frame.tobytes())

  def __enter__(self):
    return self

  def close(self):
    self.pipeline.stdin.close()
    self.pipeline.wait()

  def __exit__(self, exc_type, exc_value, exc_traceback):
    self.close()
