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
"""Blind Esimation Model
"""
import torch
from torch import nn
import numpy as np

from .base import Evaluator
from . import models


class BlindIQA(Evaluator):

  def __init__(self, qs_models=['qsv3', 'unique', 'censeoqoe'], device='cpu'):
    super(BlindIQA, self).__init__()
    self.models = nn.ModuleDict()
    self.device = device
    self.qs = {}

    # traverse all models
    for name in qs_models:
      self.qs[name] = []
      if name == 'qsv3':
        self.models[name] = models.AttributeNet(backbone='mobilenet_v2', attrs=[1, 1, 1, 1, 1, 1, 1, 6])
        self.models[name].eval().to(device)
      elif name == 'unique':
        self.models[name] = models.UNIQUE()
        self.models[name].eval().to(device)
      elif name == 'censeoqoe':
        self.models[name] = models.CenseoIVQAModel(pretrained='ugc')
        self.models[name].eval().to(device)
      else:
        raise NotImplementedError(name)

  def reset(self):
    for name in self.qs:
      self.qs[name] = []

  @torch.no_grad()
  def append(self, results):
    """append compute results

    results:
      qsv3: [N, C1]
      unique: [N, C2]
      censeoqoe: [N, C3]

    """
    for name, val in results.items():
      self.qs[name].append(val)

  @torch.no_grad()
  def compute(self, inputs):
    """quality assessment evalutor

    Args:
        inputs (N, C, H, W): require input as a RGB in [0, 1]

    """
    results = {}
    inputs = inputs.to(self.device)

    for name, module in self.models.items():
      inp = inputs.clone()

      if hasattr(module, 'preprocess'):
        inp = module.preprocess(inp)

      outputs = module(inp)

      if hasattr(module, 'postprocess'):
        if isinstance(outputs, (tuple, list)):
          outputs = module.postprocess(*outputs)
        else:
          outputs = module.postprocess(outputs)

      if name == 'qsv3':
        outputs = outputs[:, 0]

      results[name] = outputs.reshape(-1, 1)

    return results

  def accumulate(self):
    """accumulate scores
    """
    results = {}
    for name in self.qs:
      self.qs[name] = torch.stack(self.qs[name], dim=0)
      results[name] = self.qs[name].mean().item()
    return results
