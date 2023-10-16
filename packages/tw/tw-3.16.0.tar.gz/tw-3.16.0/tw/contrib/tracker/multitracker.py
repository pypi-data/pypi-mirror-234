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
"""MultiTracker from OpenCV

  Installation:
    pip uninstall opencv-contrib-python opencv-python opencv-contrib-python-headless
    pip install opencv-contrib-python

"""
import sys
import cv2
import time


class MultiTracker():

  def __init__(self):
    super(MultiTracker, self).__init__()
    self.trackers = []

  def reset(self):
    self.trackers = []

  def add(self, tracker):
    self.trackers.append(tracker)

  def update(self, frame, autoremove=True):
    bboxes = []
    remove_trackers = []
    succ_all = True
    for i, tracker in enumerate(self.trackers):
      success, bbox = tracker.update(frame)
      if success:
        bboxes.append(bbox)
      else:
        succ_all = False
      # if autoremove:
      #   remove_trackers.append(tracker)
    # for t in remove_trackers:
    #   self.trackers.remove(t)
    return succ_all, bboxes


class SingleTracker():
  """tracking bboxes

      BOOSTING: 23.74, occlusion
      MIL: 24.13, occlusion
      KCF: 29.97, stable
      TLD: 80.13, jitter
      MEDIANFLOW: 3.81, stable
      GOTURN
      MOSSE: 2.08, stable
      CSRT: 30.13, jitter

  """

  def __init__(self, name):
    super(SingleTracker, self).__init__()
    self.tracker = self.create_tracker(name)
    self.record = []

  def create_tracker(self, name):
    """create a single object tracker
    """
    if name == 'BOOSTING':
      tracker = cv2.legacy.TrackerBoosting_create()
    elif name == 'MIL':
      tracker = cv2.legacy.TrackerMIL_create()
    elif name == 'KCF':
      tracker = cv2.legacy.TrackerKCF_create()
    elif name == 'TLD':
      tracker = cv2.legacy.TrackerTLD_create()
    elif name == 'MEDIANFLOW':
      tracker = cv2.legacy.TrackerMedianFlow_create()
    elif name == 'GOTURN':
      tracker = cv2.legacy.TrackerGOTURN_create()
    elif name == 'MOSSE':
      tracker = cv2.legacy.TrackerMOSSE_create()
    elif name == 'CSRT':
      tracker = cv2.legacy.TrackerCSRT_create()
    else:
      raise NotImplementedError(name)
    return tracker

  def init(self, frame, bbox):
    """init a new tracking object

    Args:
      frame: BGR [H, W, C] in [0, 255]
      bbox: x1, y1, w, h

    """
    t1 = time.time()
    self.tracker.init(frame, bbox)
    t2 = time.time()
    self.record.append(((t2 - t1) * 1000, 'init'))
    return self

  def update(self, frame):
    """return a tracked bbox from frame

    Args:
      frame: BGR [H, W, C] in [0, 255]

    Returns:
      flag: true for succcess
      a updated bbox: x, y, w, h

    """
    t1 = time.time()
    success, bbox = self.tracker.update(frame)
    t2 = time.time()
    self.record.append(((t2 - t1) * 1000, 'update'))
    return success, bbox
