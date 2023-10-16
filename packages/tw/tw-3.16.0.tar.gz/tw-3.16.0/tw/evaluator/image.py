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
import torch
import numpy as np
from .base import Evaluator
from tw.nn.losses import PSNRLoss, StructuralSimilarityLoss
from skimage import metrics, color

import tw.transform as T


class ImageSimilarityEvaluator(Evaluator):

  def __init__(self, use_psnr=True, use_ssim=True, use_delta_e=False, use_lpips=False):
    super(ImageSimilarityEvaluator, self).__init__()
    self.root = None
    self.use_psnr = use_psnr
    self.use_ssim = use_ssim
    self.use_lpips = use_lpips
    self.use_delta_e = use_delta_e

    try:
      import lpips
    except ImportError:
      raise ImportError('Failed to import lpips library, please `pip install lpips` first.')

    if self.use_lpips:
      self.lpips = lpips.LPIPS(net='vgg')

  def reset(self):
    """reset accumulate information"""
    self.metrics = []

  def append(self, values):
    """append values"""
    self.metrics.append(values)

  def compute(self, preds, targets, **kwargs):
    """compute intermediate information during validation

    Args:
      preds: [N, C, H, W] Tensor
      targets: [N, C, H, W] Tensor

    Returns:

    """
    metric = {}
    assert preds.size(0) == 1

    # support for list
    # if isinstance(preds, list):
    #   if self.use_psnr:
    #     metric['psnr'] = 0.0
    #     for pred, target in zip(preds, targets):
    #       metric['psnr'] += PSNRLoss.psnr(pred, target).item()
    #     metric['psnr'] /= len(preds)
    #   if self.use_ssim:
    #     metric['ssim'] = 0.0
    #     for pred, target in zip(preds, targets):
    #       metric['ssim'] += StructuralSimilarityLoss.structural_similarity(pred, target).item()
    #     metric['ssim'] /= len(preds)
    #   if self.use_lpips:
    #     metric['lpips'] = 0.0
    #     for pred, target in zip(preds, targets):
    #       metric['lpips'] += self.lpips(pred, target, normalize=True).mean().item()  # nopep8
    #     metric['lpips'] /= len(preds)

    # else:
    #   if self.use_psnr:
    #     metric['psnr'] = PSNRLoss.psnr(preds, targets).item()
    #   if self.use_ssim:
    #     metric['ssim'] = StructuralSimilarityLoss.structural_similarity(preds, targets).item()
    #   if self.use_lpips:
    #     # where we assume preds and targets is [0, 1]
    #     metric['lpips'] = self.lpips(preds, targets, normalize=True).mean().item()  # nopep8

    preds = preds.clamp(0.0, 1.0)
    targets = targets.clamp(0.0, 1.0)

    pred = preds[0].permute(1, 2, 0).cpu().clamp(0, 1.0).numpy().astype('float32')
    target = targets[0].permute(1, 2, 0).cpu().clamp(0, 1.0).numpy().astype('float32')

    if self.use_psnr:
      metric['psnr'] = metrics.peak_signal_noise_ratio(pred, target)
    if self.use_ssim:
      metric['ssim'] = metrics.structural_similarity(pred, target, gaussian_weights=True, multichannel=True, channel_axis=2, data_range=1)  # nopep8
    if self.use_lpips:
      metric['lpips'] = self.lpips(preds, targets, normalize=True).mean().item()
    if self.use_delta_e:
      metric['delta_e'] = np.array(color.deltaE_cie76(color.rgb2lab(pred), color.rgb2lab(target))).mean()

      # preds_lab = T.rgb_to_lab(preds, data_range=1.0)
      # targets_lab = T.rgb_to_lab(targets, data_range=1.0)
      # metric['delta_e'] = (preds_lab - targets_lab).pow(2).sum(dim=1).sqrt().mean().item()

    if 'path' in kwargs:
      assert len(kwargs['path']) == 1
      metric['path'] = kwargs['path'][0]

    return metric

  def accumulate(self):
    """accumulate total results"""
    results = {}

    if self.use_psnr:
      results['psnr'] = []
    if self.use_lpips:
      results['lpips'] = []
    if self.use_ssim:
      results['ssim'] = []
    if self.use_delta_e:
      results['delta_e'] = []

    for key in results:
      for metric in self.metrics:
        results[key].append(metric[key])
      results[key] = np.mean(results[key])

    if self.root is not None:
      with open(self.root + '/summary.txt', 'w') as fw:
        for metric in self.metrics:
          line = ''
          for key in ['path', 'psnr', 'lpips', 'ssim']:
            if key in metric:
              line += str(metric[key]) + ' '
          line += '\n'
          fw.write(line)

    return results

  def __len__(self):
    return len(self.metrics)
