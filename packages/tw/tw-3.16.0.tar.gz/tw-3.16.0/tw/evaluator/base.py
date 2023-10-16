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
r"""Evaluator Base

Usage:

  # create a instance
  evaluator = Evaluator()

  # reset to zero before executing it.
  evaluator.reset()

  # loop for collecting results.
  for step in range(total_steps):
    evaluator.append(model(...))

  # accumulate all data into a result.
  results = evaluator.accumulate()

"""
import torch
from torch import nn


class Evaluator(nn.Module):

  def __init__(self, root=None, **kwargs):
    super(Evaluator, self).__init__()
    self.metrics = []
    self.root = root

  def reset(self):
    r"""reset accumulate information"""
    self.metrics = []

  def compute(self, *args, **kwargs):
    r"""compute intermediate information during validation"""
    raise NotImplementedError

  def append(self, values):
    r"""append values"""
    self.metrics.append(values)

  def accumulate(self):
    r"""accumulate total results"""
    return {}

  def __len__(self):
    return len(self.metrics)


class ComposeEvaluator(Evaluator):

  def __init__(self, evaluators):
    self.evaluators = evaluators

  def reset(self):
    """reset accumulate information"""
    for evaluator in self.evaluators:
      evaluator.reset()

  def compute(self, *args, **kwargs):
    """compute intermediate information during validation"""
    for evaluator in self.evaluators:
      evaluator.compute(*args, **kwargs)

  def append(self, values):
    """append values"""
    for evaluator in self.evaluators:
      evaluator.append(values)

  def accumulate(self):
    """accumulate total results"""
    results = {}
    for evaluator in self.evaluators:
      results.update(evaluator.accumulate())
    return results

  def __len__(self):
    return len(self.evaluators)
