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
import tqdm
import glob
import random
import copy
from collections import OrderedDict

import torch
import cv2
import numpy as np
import imageio.v2 as imageio

import tw
import tw.transform as T


class MITAdobeFiveK(torch.utils.data.Dataset):

  """Following previous settings, we should ExpertC as groundtruth.

    fiveK(root):
     - expertC
      - JPG
        - 480p
     - input
      - JPG
        - 480p
        - 1080p_test
        - original
      - PNG
     - test.txt
     - train_input.txt
     - train_label.txt

  """

  def __init__(self, root, transform, phase, is_meta=True, **kwargs):
    super(MITAdobeFiveK, self).__init__()
    self.transform = transform
    self.targets = []
    self.is_meta = is_meta

    gt_root = f'{root}/expertC/JPG/480p/'
    in_root = f'{root}/input/JPG/480p/'

    if phase == tw.phase.train:
      with open(f'{root}/train_input.txt') as fp:
        for line in fp:
          self.targets.append((f'{in_root}/{line.strip()}.jpg', f'{gt_root}/{line.strip()}.jpg'))
      with open(f'{root}/train_label.txt') as fp:
        for line in fp:
          self.targets.append((f'{in_root}/{line.strip()}.jpg', f'{gt_root}/{line.strip()}.jpg'))
    else:
      with open(f'{root}/test.txt') as fp:
        for line in fp:
          self.targets.append((f'{in_root}/{line.strip()}.jpg', f'{gt_root}/{line.strip()}.jpg'))

    tw.logger.info("Total load %d images." % len(self))

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, idx):
    lr, hr = self.targets[idx]

    lr_meta = T.ImageMeta(path=lr, source=T.COLORSPACE.BGR)
    lr_meta.load().numpy()
    hr_meta = T.ImageMeta(path=hr, source=T.COLORSPACE.BGR)
    hr_meta.load().numpy()

    # meta or not
    if self.is_meta:
      return self.transform([lr_meta, hr_meta])
    else:
      return self.transform(lr_meta.bin, hr_meta.bin)


class PPR10K(torch.utils.data.Dataset):

  """https://github.com/csjliang/PPR10K

    /cephFS/video_lab/datasets/bigolive_color_enhance/ppr10k
     - train_val_images_tif_360p
      - train
        - masks
          - 0_0.png
        - source
          - 0_0.tif
        - target_a
          - 0_0.tif
      - val
        - masks
          - 1356_0.png
        - source
          - 1356_0.tif
        - target_a
          - 1356_0.tif

    Note that:
      img: normalize to [0, 1] float32 bgr [H, W, C]
      gt: normalize to [0, 1] float32 bgr [H, W, C]
      mask: normalize to [0, 1] float32  [H, W, 1]

  """

  def __init__(self, root, transform, phase, is_meta=True, **kwargs):
    super(PPR10K, self).__init__()
    self.transform = transform
    self.targets = []
    self.is_meta = is_meta

    if phase == tw.phase.train:
      mask_root = f'{root}/train_val_images_tif_360p/train/masks/*.png'
      input_root = f'{root}/train_val_images_tif_360p/train/source/*.tif'
      gt_root = f'{root}/train_val_images_tif_360p/train/target_a/*.tif'

    elif phase == tw.phase.val:
      mask_root = f'{root}/train_val_images_tif_360p/val/masks/*.png'
      input_root = f'{root}/train_val_images_tif_360p/val/source/*.tif'
      gt_root = f'{root}/train_val_images_tif_360p/val/target_a/*.tif'

    else:
      raise NotImplementedError(phase.name)

    # collection
    gt_files = sorted(glob.glob(gt_root))
    mask_files = sorted(glob.glob(mask_root))
    input_files = sorted(glob.glob(input_root))

    assert len(gt_files) == len(mask_files) == len(input_files)

    for gt, mask, input in zip(gt_files, mask_files, input_files):
      self.targets.append((input, gt, mask))

    tw.logger.info("Total load %d images." % len(self))

  def __len__(self):
    return len(self.targets)

  def read_img(self, path):
    """reading image from path
    """
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img.dtype == np.uint8:
      img = img.astype(np.float32) / 255.
    elif img.dtype == np.uint16:
      img = img.astype(np.float32) / 65535.
    if img.ndim == 2:
      img = np.expand_dims(img, axis=2)
    # some images have 4 channels
    if img.shape[2] > 3:
      img = img[:, :, :3]
    return img

  def __getitem__(self, idx):
    inp, gt, mask = self.targets[idx]

    inp = self.read_img(inp)
    gt = self.read_img(gt)
    mask = self.read_img(mask)

    inp_meta = T.ImageMeta(binary=inp, source=T.COLORSPACE.BGR)
    gt_meta = T.ImageMeta(binary=gt, source=T.COLORSPACE.BGR)
    mask_meta = T.ImageMeta(binary=mask, source=T.COLORSPACE.GRAY)

    # meta or not
    if self.is_meta:
      return self.transform([inp_meta, gt_meta, mask_meta])
    else:
      return self.transform(inp_meta.bin, gt_meta.bin, mask_meta.bin)


class NeurOP(torch.utils.data.Dataset):

  """https://github.com/amberwangyili/neurop

    root='xxxx/dataset-init'

    dataset-init/
      - BC
        - 0123-08.png
        - ...
      - EX
        - 0123-08.png
        - ...
      - VB
        - 0123-08.png
        - ...

    Each item:
      a pair of images with BC/EX/VB, 2x3 = 6 samples


    Note that:
      img: normalize to [0, 1] float32 bgr [H, W, C]
      gt: normalize to [0, 1] float32 bgr [H, W, C]
      mask: normalize to [0, 1] float32  [H, W, 1]

  """

  def __init__(self, root, transform, phase, is_meta=True, **kwargs):
    super(NeurOP, self).__init__()
    self.transform = transform
    self.targets = {}
    self.ids_to_name = []
    self.is_meta = is_meta

    # each file following ids-{strength}.png
    for distort in ['EX', 'BC', 'VB']:
      for file in glob.glob(f'{root}/{distort}/*.png'):
        # file: 'xxx/xxxx/xxx/yyy-degree.png'
        name, degree = os.path.splitext(os.path.basename(file))[0].split('-')

        if name not in self.targets:
          self.targets[name] = {}
          self.ids_to_name.append(name)

        if distort not in self.targets[name]:
          self.targets[name][distort] = []

        self.targets[name][distort].append((int(degree), file))

    tw.logger.info("Total load %d images." % len(self))

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, idx):

    names = self.targets[self.ids_to_name[idx]]

    A_ex, B_ex = random.choices(names['EX'], k=2)
    A_bc, B_bc = random.choices(names['BC'], k=2)
    A_vb, B_vb = random.choices(names['VB'], k=2)

    # img

    img_A_ex = np.array(imageio.imread(A_ex[1]), dtype='float32') / 255.0
    img_B_ex = np.array(imageio.imread(B_ex[1]), dtype='float32') / 255.0

    img_A_bc = np.array(imageio.imread(A_bc[1]), dtype='float32') / 255.0
    img_B_bc = np.array(imageio.imread(B_bc[1]), dtype='float32') / 255.0

    img_A_vb = np.array(imageio.imread(A_vb[1]), dtype='float32') / 255.0
    img_B_vb = np.array(imageio.imread(B_vb[1]), dtype='float32') / 255.0

    # meta
    # it is very very important to normalize label to [-1, 1]
    # pay attention how label introduce into the network
    # y_code = x_code + val # due to input-x should in [0, 1]
    # possibly, using multiply is more suitable

    img_A_ex = T.ImageMeta(binary=img_A_ex, source=T.COLORSPACE.RGB)
    img_A_ex.label = (B_ex[0] - A_ex[0]) / 20.0
    img_B_ex = T.ImageMeta(binary=img_B_ex, source=T.COLORSPACE.RGB)

    img_A_bc = T.ImageMeta(binary=img_A_bc, source=T.COLORSPACE.RGB)
    img_A_bc.label = (B_bc[0] - A_bc[0]) / 20.0
    img_B_bc = T.ImageMeta(binary=img_B_bc, source=T.COLORSPACE.RGB)

    img_A_vb = T.ImageMeta(binary=img_A_vb, source=T.COLORSPACE.RGB)
    img_A_vb.label = (B_vb[0] - A_vb[0]) / 20.0
    img_B_vb = T.ImageMeta(binary=img_B_vb, source=T.COLORSPACE.RGB)

    # meta or not
    if self.is_meta:
      return self.transform([
          img_A_ex, img_B_ex,
          img_A_bc, img_B_bc,
          img_A_vb, img_B_vb
      ])
    else:
      return self.transform(
          img_A_ex.bin, img_B_ex.bin, img_A_ex.label,
          img_A_bc.bin, img_B_bc.bin, img_A_bc.label,
          img_A_vb.bin, img_B_vb.bin, img_A_vb.label,
      )


class BigoNeurOP(torch.utils.data.Dataset):

  def __init__(self, root, transform, phase, **kwargs):
    super(BigoNeurOP, self).__init__()
    self.transform = transform
    self.targets = {}
    self.detector = tw.contrib.matting.BigoRvm()

    # load all imgs
    imgs, vids = tw.media.collect(root, if_check_path=False)
    for file in imgs:
      names = os.path.splitext(os.path.basename(file))[0].split('-')
      filename = '-'.join(names[0:-1])
      degree = float(names[-1])
      if filename not in self.targets:
        self.targets[filename] = []
      self.targets[filename].append([file, degree])

    # split dataset by 9:1
    total = int(len(self.targets) * 0.9)
    self.ids_to_names = {}
    count = 0
    npairs = []
    for i, filename in enumerate(self.targets):
      if (i < total and phase == tw.phase.train) or (i >= total and phase in [tw.phase.val, tw.phase.test]):
        self.ids_to_names[count] = filename
        count += 1
      npairs.append(len(self.targets[filename]))

    tw.logger.info("Total load %d with %f levels images." % (len(self), np.mean(npairs)))

  def __len__(self):
    return len(self.ids_to_names)

  def __getitem__(self, idx):
    """generation from img1 to img2
    """
    album = self.targets[self.ids_to_names[idx]]
    (path1, degree1), (path2, degree2) = random.choices(album, k=2)

    img1 = np.array(imageio.imread(path1), dtype='float32')
    img2 = np.array(imageio.imread(path2), dtype='float32')

    # using bigorvm for inference
    pha, seg, pha_color, seg_color = self.detector(cv2.cvtColor(img1, cv2.COLOR_RGB2BGR))

    # filter out the image without face
    if pha.sum() == 0 or (seg == 1).sum() == 0:
      return self.__getitem__(idx + 1)

    img_1_meta = T.ImageMeta(binary=img1 / 255.0, source=T.COLORSPACE.RGB)
    img_1_meta.label = (degree2 - degree1) / float(len(album))
    img_2_meta = T.ImageMeta(binary=img2 / 255.0, source=T.COLORSPACE.RGB)

    img_1_mask = T.ImageMeta(binary=pha, source=T.COLORSPACE.HEATMAP)
    img_1_seg = T.ImageMeta(binary=seg, source=T.COLORSPACE.HEATMAP)

    # meta or not
    return self.transform([img_1_meta, img_2_meta, img_1_mask, img_1_seg])


class BigoColorEnhance(torch.utils.data.Dataset):
  """
  """

  def __init__(self, source_dir, target_dir, transform, phase, **kwargs):
    super(BigoColorEnhance, self).__init__()
    self.transform = transform
    self.targets = []
    self.detector = tw.contrib.matting.BigoRvm()

    # load source
    source_files, _ = tw.media.collect(source_dir, if_check_path=False)
    target_files, _ = tw.media.collect(target_dir, if_check_path=False)

    source_files = sorted(source_files)
    target_files = sorted(target_files)

    # fusion
    for source, target in zip(source_files, target_files):
      src_name = os.path.splitext(os.path.basename(source))[0]
      tgt_name = os.path.splitext(os.path.basename(target))[0]
      assert src_name == tgt_name, f"{source} vs {target}."
      self.targets.append((source, target))

    # split dataset by 9:1
    total = int(len(self.targets) * 0.9)
    if phase == tw.phase.train:
      self.targets = self.targets[:total]
    else:
      self.targets = self.targets[total:]

    tw.logger.info(f"Total load {len(self)} images in {phase.name}.")

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, idx):
    """input source and target
    """
    source_path, target_path = self.targets[idx]
    
    src_img = np.array(imageio.imread(source_path), dtype='float32')
    tgt_img = np.array(imageio.imread(target_path), dtype='float32')

    # using bigorvm for inference
    pha, seg, pha_color, seg_color = self.detector(cv2.cvtColor(src_img, cv2.COLOR_RGB2BGR))
    
    # filter out the image without face
    if pha.sum() == 0 or (seg == 1).sum() == 0:
      return self.__getitem__(idx + 1)

    src_meta = T.ImageMeta(binary=src_img / 255.0, source=T.COLORSPACE.RGB)
    tgt_meta = T.ImageMeta(binary=tgt_img / 255.0, source=T.COLORSPACE.RGB)

    mask_meta = T.ImageMeta(binary=pha, source=T.COLORSPACE.HEATMAP)
    seg_meta = T.ImageMeta(binary=seg, source=T.COLORSPACE.HEATMAP)

    return self.transform([src_meta, tgt_meta, mask_meta, seg_meta])
