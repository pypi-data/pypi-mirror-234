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
"""this file including four dataset

    Helen: 11 classes
        2000, 230, 100

    CelebAMask-HQ: 11 classes + 8 classes (left/right ear, eye glass earing necklace neck cloth)
        24183, 2993, 2824

    LaPa: 11 classes
        18,176, 2000, 2000

    Microsoft Synthetics100k

"""
import os
import glob
import pickle
import torch
import numpy as np
import tw
import tw.transform as T


class HelenParsing(torch.utils.data.Dataset):

  def __init__(self, path, transform, phase, **kwargs):
    super(HelenParsing, self).__init__()
    tw.logger.info("Total load %d images." % len(self))

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, idx):
    """
    """
    image_path, mask_path = self.targets[idx]

    img_meta = T.ImageMeta(path=image_path)
    img_meta.load().numpy()

    mask_meta = T.ImageMeta(path=mask_path, source=T.COLORSPACE.HEATMAP)
    mask_meta.load().numpy()

    return self.transform(img_meta, mask_meta)


class CelebAMaskHQ(torch.utils.data.Dataset):

  """File structure

    ./CelebAMask-HQ
      - train_img
      - train_label
      - test_img
      - test_label
      - val_img
      - val_label

  """

  def __init__(self, root, transform, phase, **kwargs):
    super(CelebAMaskHQ, self).__init__()
    self.transform = transform
    self.targets = []
    for image_path in glob.glob(f'{os.path.join(root, phase.name)}_img/*.jpg'):
      label_path = image_path.replace('_img/', '_label/').replace('.jpg', '.png')
      self.targets.append((image_path, label_path))
    tw.logger.info("Total load %d images." % len(self))

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, idx):
    """
    """
    image_path, label_path = self.targets[idx]

    img_meta = T.ImageMeta(path=image_path)
    img_meta.load().numpy()

    mask_meta = T.ImageMeta(path=label_path, source=T.COLORSPACE.HEATMAP)
    mask_meta.load().numpy()

    return self.transform(img_meta, mask_meta)


class LaPa(torch.utils.data.Dataset):

  """File Structure

   - LaPa
    - train
      - images
      - labels
      - landmarks
    - val
      - images
      - labels
      - landmarks
    - test
      - images
      - labels
      - landmarks

  """

  def __init__(self, root, transform, phase, **kwargs):
    super(LaPa, self).__init__()
    self.transform = transform
    self.targets = []
    for image_path in glob.glob(f'{os.path.join(root, phase.name)}/images/*.jpg'):
      label_path = image_path.replace('/images/', '/labels/').replace('.jpg', '.png')
      ldmk_path = image_path.replace('/images/', '/landmarks/').replace('.jpg', '.txt')
      self.targets.append((image_path, label_path, ldmk_path))
    tw.logger.info("Total load %d images." % len(self))

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, idx):
    """
    """
    image_path, label_path, ldmk_path = self.targets[idx]

    img_meta = T.ImageMeta(path=image_path)
    img_meta.load().numpy()

    mask_meta = T.ImageMeta(path=label_path, source=T.COLORSPACE.HEATMAP)
    mask_meta.load().numpy()

    ldmk_meta = T.KpsListMeta()
    with open(ldmk_path) as fp:
      for i, line in enumerate(fp):
        if i == 0:
          continue
        x, y = line.strip().split(' ')
        x, y = int(float(x)), int(float(y))
        ldmk_meta.add(x, y)
    ldmk_meta.set_affine_size(max_h=img_meta.h, max_w=img_meta.w)
    ldmk_meta.numpy()

    return self.transform(img_meta, mask_meta, ldmk_meta)


class FaceSynth100k(torch.utils.data.Dataset):

  def __init__(self, path, transform, phase, **kwargs):
    super(FaceSynth100k, self).__init__()
    tw.logger.info("Total load %d images." % len(self))

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, idx):
    """
    """
    image_path, mask_path = self.targets[idx]

    img_meta = T.ImageMeta(path=image_path)
    img_meta.load().numpy()

    mask_meta = T.ImageMeta(path=mask_path, source=T.COLORSPACE.HEATMAP)
    mask_meta.load().numpy()

    return self.transform(img_meta, mask_meta)


class MultiTaskFaceParsing(torch.utils.data.Dataset):

  """ Multi-Task Face Parsing dataset include multiple info.

    {
      name             : str, name without extension
      path             : str, filepath
      subset           : str, 'train', 'val', 'test'
      split            : str, 'CelebAMask-HQ', 'LaPa', 'Helen', 'Synth100k'
      landmark         : np.ndarray, [68, 2] float32 in full-size image
      bbox             : list, [x1, y1, x2, y2] in full-size image
      image            : np.ndarray, [h, w, 3] uint8 in full-size image
      mask             : np.ndarray, [h, w] uint8 in full-size mask
      crop_image       : np.ndarray, [h', w', 3] uint8 in crop-size image
      crop_mask        : np.ndarray, [h', w'] uint8 in crop-size mask
      crop_landmark    : np.ndarray, [h', w', 3] uint8 in crop-size image
      num_classess     : int, number of semantic classes
    }

  """

  def __init__(self, root, transform, phase, version=1, **kwargs):
    super(MultiTaskFaceParsing, self).__init__()
    self.transform = transform
    self.phase = phase
    self.version = version
    self.targets = sorted(glob.glob(f'{root}/{phase.name}/*.pth'))
    tw.logger.info("Total load %d images." % len(self))

  def __len__(self):
    return len(self.targets)

  def convert_mask(self, mask, subset):
    """mapping differnt dataset to MTFPv1

      MTFPv1:
       0 - background
       1 - skin
       2 - brow
       3 - eye
       4 - lip
       5 - mouth
       6 - hair

    """
    if subset == 'CelebAMask-HQ':
      mapping = {0: 0, 1: 1, 2: 4, 3: 0, 4: 3, 5: 3, 6: 2, 7: 2, 8: 0, 9: 0, 10: 6, 11: 5, 12: 5, 13: 7, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, }  # nopep8
    elif subset == 'LaPa':
      mapping = {0: 0, 1: 1, 2: 2, 3: 2, 4: 3, 5: 3, 6: 4, 7: 5, 8: 6, 9: 5, 10: 7, }  # nopep8
    elif subset == 'Helen':
      mapping = {0: 0, 1: 1, 2: 2, 3: 2, 4: 3, 5: 3, 6: 4, 7: 5, 8: 6, 9: 5, 10: 7, }  # nopep8
    elif subset == 'Synth100k':
      mapping = {0: 0, 1: 1, 2: 4, 3: 3, 4: 3, 5: 2, 6: 2, 7: 0, 8: 0, 9: 6, 10: 5, 11: 5, 12: 0, 13: 7, 14: 7, 15: 0, 16: 0, 17: 0, 18: 0, }  # nopep8
    else:
      raise NotImplementedError(subset)

    new_mask = np.ones_like(mask) * 255
    for ori_cls, new_cls in mapping.items():
      new_mask[mask == ori_cls] = new_cls

    return new_mask

  def __getitem__(self, idx):
    """

      meta['name']
      meta['path']
      meta['subset']
      meta['split']
      meta['landmark']
      meta['bbox']
      meta['image']
      meta['mask']
      meta['crop_image']
      meta['crop_mask']
      meta['crop_landmark']
      meta['num_classess']

    """
    meta = torch.load(self.targets[idx])
    image = meta['crop_image'].copy()
    mask = self.convert_mask(meta['crop_mask'], meta['subset'])

    img_meta = T.ImageMeta(binary=image, source=T.COLORSPACE.BGR)
    img_meta.bin = img_meta.bin.astype('float32')
    mask_meta = T.ImageMeta(binary=mask, source=T.COLORSPACE.HEATMAP)
    mask_meta.bin = mask_meta.bin.astype('uint8')

    ldmk_meta = T.KpsListMeta()
    for x, y in meta['crop_landmark']:
      ldmk_meta.add(int(x), int(y))
    ldmk_meta.set_affine_size(max_h=img_meta.h, max_w=img_meta.w)
    ldmk_meta.numpy()

    return self.transform(img_meta, mask_meta, ldmk_meta)
