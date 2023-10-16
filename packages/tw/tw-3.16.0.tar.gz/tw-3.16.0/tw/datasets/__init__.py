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

from .base import SampleCollator
from .base import BatchMultiSampler

from .prefetcher import CPUPrefetcher
from .prefetcher import CUDAPrefetcher

from .mnist import Mnist
from .cifar import Cifar10
from .imagenet import ImageNet
from .coco import CocoDetection

from .face import WiderFace, WiderFaceTest
from .face import Face300W
# from .face import Face300W_LP
# from .face import AFLW2000
from .face import COFW
from .face import JD106
# from .face import WFLW

from .face_parsing import HelenParsing
from .face_parsing import CelebAMaskHQ
from .face_parsing import LaPa
from .face_parsing import FaceSynth100k
from .face_parsing import MultiTaskFaceParsing

from .facemesh import NoW
from .facemesh import BigoFaceMesh
from .facemesh import BigoVideoFaceMesh

from .avec2014 import Avec2014
from .avec2014 import Avec2014Video

from .general import ImageLabel
from .general import ImageSalientDet
from .general import ImagesDataset
from .general import ImageRestoration
from .general import VideoRestoration

from .quality_assess import PIPAL
from .quality_assess import TID2013
from .quality_assess import KonIQ10k
from .quality_assess import SPAQ
from .quality_assess import LIVEC
from .quality_assess import LIVE2005
from .quality_assess import LIVEMD
from .quality_assess import CSIQ
from .quality_assess import FLIVE
from .quality_assess import VQA_III
from .quality_assess import PIQ2023

from .optical_flow import MPISintel
from .optical_flow import FlyingChairs
from .optical_flow import FlyingThings3D

from .denoise import SIDD_sRGB

from .color_enhance import MITAdobeFiveK
from .color_enhance import PPR10K
from .color_enhance import NeurOP
from .color_enhance import BigoNeurOP, BigoColorEnhance

from .point_cloud import SensatUrban
from .point_cloud import SensatUrbanDefaultFetcher, SensatUrbanNullFetcher
from .point_cloud import SensatUrbanDefaultSampler, SensatUrbanClassprobSampler
from .point_cloud import STPLS3D

from .super_resolution import Flickr1024

from . import pil

# from torch.utils.data import *

from .cityscapes import Cityscapes
