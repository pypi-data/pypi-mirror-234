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
"""Cityscape Dataset"""
import os
from collections import namedtuple
import torch
import tw
import tw.transform as T


_S = namedtuple('_S', ['name', 'id', 'train_id', 'category', 'category_id',
                       'has_instances', 'ignore_in_eval', 'color'])
_CLASS = [
    _S('unlabeled', 0, 255, 'void', 0, False, True, (0, 0, 0)),
    _S('ego vehicle', 1, 255, 'void', 0, False, True, (0, 0, 0)),
    _S('rectification border', 2, 255, 'void', 0, False, True, (0, 0, 0)),
    _S('out of roi', 3, 255, 'void', 0, False, True, (0, 0, 0)),
    _S('static', 4, 255, 'void', 0, False, True, (0, 0, 0)),
    _S('dynamic', 5, 255, 'void', 0, False, True, (111, 74, 0)),
    _S('ground', 6, 255, 'void', 0, False, True, (81, 0, 81)),
    _S('road', 7, 0, 'flat', 1, False, False, (128, 64, 128)),
    _S('sidewalk', 8, 1, 'flat', 1, False, False, (244, 35, 232)),
    _S('parking', 9, 255, 'flat', 1, False, True, (250, 170, 160)),
    _S('rail track', 10, 255, 'flat', 1, False, True, (230, 150, 140)),
    _S('building', 11, 2, 'construction', 2, False, False, (70, 70, 70)),
    _S('wall', 12, 3, 'construction', 2, False, False, (102, 102, 156)),
    _S('fence', 13, 4, 'construction', 2, False, False, (190, 153, 153)),
    _S('guard rail', 14, 255, 'construction', 2, False, True, (180, 165, 180)),
    _S('bridge', 15, 255, 'construction', 2, False, True, (150, 100, 100)),
    _S('tunnel', 16, 255, 'construction', 2, False, True, (150, 120, 90)),
    _S('pole', 17, 5, 'object', 3, False, False, (153, 153, 153)),
    _S('polegroup', 18, 255, 'object', 3, False, True, (153, 153, 153)),
    _S('traffic light', 19, 6, 'object', 3, False, False, (250, 170, 30)),
    _S('traffic sign', 20, 7, 'object', 3, False, False, (220, 220, 0)),
    _S('vegetation', 21, 8, 'nature', 4, False, False, (107, 142, 35)),
    _S('terrain', 22, 9, 'nature', 4, False, False, (152, 251, 152)),
    _S('sky', 23, 10, 'sky', 5, False, False, (70, 130, 180)),
    _S('person', 24, 11, 'human', 6, True, False, (220, 20, 60)),
    _S('rider', 25, 12, 'human', 6, True, False, (255, 0, 0)),
    _S('car', 26, 13, 'vehicle', 7, True, False, (0, 0, 142)),
    _S('truck', 27, 14, 'vehicle', 7, True, False, (0, 0, 70)),
    _S('bus', 28, 15, 'vehicle', 7, True, False, (0, 60, 100)),
    _S('caravan', 29, 255, 'vehicle', 7, True, True, (0, 0, 90)),
    _S('trailer', 30, 255, 'vehicle', 7, True, True, (0, 0, 110)),
    _S('train', 31, 16, 'vehicle', 7, True, False, (0, 80, 100)),
    _S('motorcycle', 32, 17, 'vehicle', 7, True, False, (0, 0, 230)),
    _S('bicycle', 33, 18, 'vehicle', 7, True, False, (119, 11, 32)),
    _S('license plate', -1, -1, 'vehicle', 7, False, True, (0, 0, 142)),
]


class Cityscapes(torch.utils.data.Dataset):
  """`Cityscapes <http://www.cityscapes-dataset.com/>`_ Dataset.
  """

  def __init__(self, root, phase, transform, **kwargs):
    super(Cityscapes, self).__init__()
    # transform
    self.transform = transform

    # loading
    images_dir = os.path.join(root, 'leftImg8bit', phase.name)
    targets_dir = os.path.join(root, 'gtFine', phase.name)

    # metas
    self.num_classes = 19
    self.images = []
    self.targets = []
    for city in os.listdir(images_dir):
      img_dir = os.path.join(images_dir, city)
      target_dir = os.path.join(targets_dir, city)
      for file_name in os.listdir(img_dir):
        # add-in image
        self.images.append('{}/{}'.format(img_dir, file_name))
        # add-in target
        base = '{}_{}_'.format(file_name.split('_leftImg8bit')[0], 'gtFine')
        self.targets.append({
            'instance': os.path.join(target_dir, base + 'instanceIds.png'),
            'label': os.path.join(target_dir, base + 'labelIds.png'),
            'polygon': os.path.join(target_dir, base + 'polygons.json'),
            'color': os.path.join(target_dir, base + 'color.png'),
        })
        tw.fs.raise_path_not_exist(self.images[-1])
        tw.fs.raise_path_not_exist(self.targets[-1])

    # mapping semantic label
    self.heatmap_valid_mapping = {}
    for c in _CLASS:
      self.heatmap_valid_mapping[c.id] = c.train_id

    # compute weights balance
    if (False):
      import cv2
      import torch
      hists = torch.zeros(self.num_classes)
      for i, tg in enumerate(self.targets):
        label = cv2.imread(tg['label'], cv2.IMREAD_GRAYSCALE)
        for idx, train_idx in self.heatmap_valid_mapping.items():
          label[label == idx] = train_idx
        hists += torch.tensor(label).float().histc(
            self.num_classes, 0, self.num_classes - 1)
        if i % 100 == 0:
          print(i)
      norm_hist = 1.0 / torch.log(1.1 + hists / hists.sum())
      print(norm_hist)

    tw.logger.info("Total load %d images." % len(self))

  def __len__(self):
    return len(self.images)

  def __getitem__(self, idx):
    img_meta = T.ImageMeta(path=self.images[idx])
    img_meta.load().numpy()
    mask_meta = T.ImageMeta(path=self.targets[idx]['label'], source=T.COLORSPACE.HEATMAP)
    mask_meta.load().numpy()
    mask_meta.heatmap_valid_mapping = self.heatmap_valid_mapping
    return self.transform(img_meta, mask_meta)
