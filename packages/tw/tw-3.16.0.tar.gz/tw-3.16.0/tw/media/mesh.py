# Copyright 2022 The KaiJIN Authors. All Rights Reserved.
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
"""mesh manipulation tools
"""
import os
import tqdm
import random
import pickle
import time
import math

import torch
from torch.nn import functional as F

import kornia
import numpy as np
import cv2
from PIL import Image
import trimesh

from scipy import io as scipy_io
from skimage import io as skimage_io
from skimage import transform as skimage_trans

from tw.utils import drawer

__all__ = [
    # constant
    "BFM_68P_CONTOUR_LINE",
    "BS_NAMES",
    "LDMK_SEMANTIC_IDX",
    # landmark
    "load_bfm_ldmk3d",
    "landmark_march",
    "landmark_240_to_106",
    "landmark_106_to_68",
    "landmark_106_to_mesh68",
    # project
    "compute_rotation_matrix",
    "projection_layer",
    # estimate
    "estimate_norm",
    "estimate_norm_torch",
    "estimate_transform",
    # contour line
    "find_matched_contour",
    "find_minmum_index_on_contour",
    "find_contour_line",
    "find_contour_candidates",
    "dynamic_contour_index",
    # align
    "warp_face",
    "align_image",
    "realign",
    "warp_affine",
    # facemesh
    "export_facemesh",
    "visualize_facemesh",
    "visualize_facemesh_orgin",
    # pose-vis
    "visualize_pose_cube",
    "visualize_axis3d",
    # pose
    "compute_normalize_vector",
    "compute_cross_product",
    "compute_rotation_matrix_from_ortho6d",
    "compute_euler_angles_from_rotation_matrices",
]

#!<----------------------------------------------------------------------------
#!< BFM FACE MODEL CONSTANT
#!<----------------------------------------------------------------------------

BFM_68P_CONTOUR_LINE = [
    [412, 413, 414, 415, 416, 417, 418, 2740, 2761, 3392, 3530, 3535],  # 0
    [2693, 2695, 2741, 2760, 2762, 3393, 3668, 3884, 4144, 4314, 4315],  # 1
    [57, 83, 84, 89, 327, 339, 2694, 2739, 3391, 3545, 3548],  # 2
    [3544, 3546, 3547, 3549, 3550, 3551, 4229, 4230, 4231, 4232, 4233],  # 3
    [424, 425, 426, 427, 428, 429, 2578, 2743, 2764, 2906, 3390],  # 4
    [2579, 2581, 2742, 2744, 2763, 2908, 3841, 3885, 3891, 3936, 4143],  # 5
    [39, 40, 41, 90, 229, 338, 372, 2580, 2586, 2765, 2945, 3388, 3461],  # 6
    [2571, 2582, 2584, 2585, 2587, 2766, 2961, 3842, 3843, 3892, 3953, 4142, 4180],  # 7
    [444, 445, 446, 447, 448, 449, 450, 2572, 2583, 2588, 2767, 2962, 3389, 3462],  # 8
    [3561, 3562, 3563, 3564, 3565, 3566, 3567, 4243, 4244, 4245, 4246, 4247, 4248, 4249],  # 9
    [255, 256, 257, 258, 259, 260, 337, 371, 3244, 3247, 3249, 3255, 3258, 3261, 3387, 3459],  # 10
    [3245, 3248, 3250, 3252, 3254, 3257, 3259, 3262, 4062, 4063, 4064, 4065, 4066, 4067, 4141, 4179],  # 11
    [1097, 1098, 1099, 1100, 1101, 1102, 1103, 1104, 3243, 3246, 3251, 3253, 3256, 3260, 3386, 3460, 12369],  # 12
    [2341, 2342, 2343, 2344, 2345, 2346, 2347, 2348, 4882, 4883, 4884, 4885, 4886, 4887, 4888, 4889, 8933],  # 13
    [36, 44, 45, 131, 135, 228, 246, 336, 370, 2606, 2615, 2770, 2942, 2969, 3219, 3385, 3458],  # 14
    [2570, 2605, 2607, 2612, 2614, 2769, 2943, 2968, 2970, 3848, 3850, 3893, 3946, 3955, 4052, 4140, 4178],  # 15
    [268, 269, 270, 271, 272, 273, 274, 335, 369, 2604, 2613, 2768, 2941, 2967, 3218, 3384, 3457],  # 16
    [3273, 3274, 3275, 3276, 3277, 3278, 3279, 3280, 3281, 4076, 4077, 4078, 4079, 4080, 4081, 4139, 4177],  # 17
    [37, 46, 47, 132, 137, 227, 245, 334, 368, 2602, 2796, 2802, 2963, 2992, 3217, 3383, 3456],  # 18
    [2601, 2603, 2797, 2799, 2801, 2937, 2964, 2966, 2991, 3847, 3903, 3904, 3954, 3964, 4051, 4138, 4176],  # 19
    [282, 283, 284, 285, 286, 287, 288, 333, 367, 2600, 2798, 2800, 2965, 2990, 3216, 3382, 3455],  # 20
    [3292, 3294, 3295, 3296, 3298, 3300, 3301, 3302, 3304, 4090, 4091, 4092, 4093, 4094, 4095, 4137, 4175],  # 21
    [8861, 8863, 8867, 8869, 11036, 11038, 11040, 11500, 11502, 11504, 12276, 14135],  # 22
    [362, 363, 364, 365, 1095, 2335, 2856, 2993, 3215, 3647],  # 23
    [225, 3449, 3450, 3451, 4172, 4173, 4174, 4297],  # 24
    [50, 148, 243, 2858, 3212],  # 25
    [2859, 2861, 3213, 3921, 4049],  # 26
    [215, 216, 242, 2860, 3210],  # 27
    [3190, 3191, 3211, 4036, 4048],  # 28
    [217, 218, 241, 2863, 3207],  # 29
    [2862, 2864, 3208, 3922, 4047],  # 30
    [564, 565, 566, 2865, 3209],  # 31
    [3717, 3719, 3721, 4351, 4352],  # 32
    [4, 18, 240, 3720, 3722],  # 33
    [2332, 2333, 2334, 4875, 4876],  # 34
    [1092, 1093, 1094, 1518, 1873],  # 35
    [1519, 1521, 1874, 4449, 4578],  # 36
    [759, 760, 781, 1520, 1875],  # 37
    [1854, 1855, 1876, 4566, 4579],  # 38
    [757, 758, 782, 1515, 1877],  # 39
    [1514, 1516, 1878, 4448, 4580],  # 40
    [592, 690, 783, 1517, 1879],  # 41
    [2079, 2080, 2081, 4697, 4698, 4699, 7636],  # 42
    [898, 899, 900, 901, 1096, 1511, 1656, 1861, 1880],  # 43
    [1510, 1512, 1653, 1655, 1862, 4494, 4571, 4581],  # 44
    [678, 689, 768, 784, 902, 1513, 1654, 1860, 1881, 2085],  # 45
    [1959, 1960, 1961, 1962, 1963, 4620, 4621, 4622, 4623, 4700, 18292],  # 46
    [824, 825, 826, 827, 828, 871, 903, 1456, 1461, 1618, 1652, 2031, 2084, 3789, 6776],  # 47
    [1455, 1457, 1460, 1617, 1619, 3786, 3788, 4370, 4430, 4431, 4481, 4493, 4670, 4701, 6771],  # 48
    [579, 588, 589, 674, 679, 769, 872, 904, 1458, 1459, 1620, 1650, 2033, 2086, 3787],  # 49
    [1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 4608, 4609, 4610, 4611, 4612, 4671, 4702],  # 50
    [809, 810, 811, 812, 813, 814, 873, 905, 1429, 1598, 1624, 2034, 2087, 3793, 3800],  # 51
    [1428, 1596, 1621, 1623, 3790, 3792, 3799, 3801, 4371, 4373, 4420, 4473, 4482, 4672, 4703],  # 52
    [578, 586, 587, 673, 677, 770, 874, 906, 1427, 1597, 1622, 2035, 2088, 3791, 3798],  # 53
    [2373, 2374, 2375, 2376, 2377, 2378, 2379, 2380, 4911, 4912, 4913, 4914, 4915, 4916, 4917],  # 54
    [1127, 1128, 1129, 1130, 1131, 1132, 1133, 1134, 1914, 1915, 1920, 1925, 1928, 2037, 2089],  # 55
    [1909, 1912, 1916, 1919, 1921, 1922, 1924, 1926, 4594, 4595, 4596, 4597, 4598, 4673, 4704],  # 56
    [795, 796, 797, 798, 799, 800, 875, 907, 1913, 1917, 1918, 1923, 1927, 2036, 2090],  # 57
    [2186, 2187, 2188, 2189, 2190, 2191, 2192, 2193, 4768, 4769, 4770, 4771, 4772, 4773, 4774],  # 58
    [978, 979, 980, 981, 982, 983, 984, 1425, 1615, 2038, 2091, 3758, 3769, 3771],  # 59
    [1426, 1616, 3759, 3768, 3770, 3772, 3774, 4362, 4365, 4366, 4419, 4480, 4674, 4705],  # 60
    [581, 582, 583, 632, 771, 876, 908, 1422, 1601, 2039, 2092, 3765, 3773],  # 61
    [867, 1401, 1403, 1424, 3764, 3766, 4364, 4411, 4418, 4675, 5657, 5771, 7689, 18616],  # 62
    [958, 959, 960, 961, 962, 963, 1402, 1423, 1563, 2040, 3767],  # 63
    [2171, 2172, 2174, 2175, 2176, 2177, 4754, 4755, 4756, 4757, 4758],  # 64
    [599, 625, 626, 631, 865, 877, 1341, 1400, 1406, 2043, 2173],  # 65
    [1340, 1342, 1398, 1405, 1407, 2041, 4394, 4410, 4412, 4676, 4839, 5187],  # 66
    [946, 947, 948, 949, 950, 951, 952, 1343, 1399, 1404, 1420, 2042, 2161]  # 67
]


BS_NAMES = [
    "browDown_L",
    "browDown_R",
    "browInnerUp",
    "browOuterUp_L",
    "browOuterUp_R",
    "cheekPuff",
    "eyeBlink_L",
    "eyeBlink_R",
    "eyeLookDown_L",
    "eyeLookDown_R",
    "eyeLookIn_L",
    "eyeLookIn_R",
    "eyeLookOut_L",
    "eyeLookOut_R",
    "eyeLookUp_L",
    "eyeLookUp_R",
    "eyeSquint_L",
    "eyeSquint_R",
    "eyeWide_L",
    "eyeWide_R",
    "jawForward",
    "jawLeft",
    "jawOpen",
    "jawOpenMouthClose",
    "jawRight",
    "mouthSmile_L",
    "mouthSmile_R",
    "mouthDimple_L",
    "mouthDimple_R",
    "mouthFrown_L",
    "mouthFrown_R",
    "mouthFunnel",
    "mouthLeft",
    "mouthLowerDown_L",
    "mouthLowerDown_R",
    "mouthPucker",
    "mouthRight",
    "mouthRollLower",
    "mouthRollUpper",
    "mouthShrugLower",
    "mouthShrugUpper",
    "mouthTightener",
    "mouthUpperUp_L",
    "mouthUpperUp_R",
    "noseSneer_L",
    "noseSneer_R",
]

LDMK_SEMANTIC_IDX = {
    'contour_left': [0, 1, 2, 3, 4, 5, 6, 7, 8],
    'contour_right': [9, 10, 11, 12, 13, 14, 15, 16],
    'eyebrow_left': [17, 18, 19, 20, 21],
    'eyebrow_right': [22, 23, 24, 25, 26],
    'nose_line': [27, 28, 29, 30],
    'nose_bottom': [31, 32, 33, 34, 35],
    'eye_left': [36, 37, 38, 39, 40, 41],
    'eye_right': [42, 43, 44, 45, 46, 47],
    'mouth_ex': [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
    'mouth_in': [60, 61, 62, 63, 64, 65, 66, 67],
}


def load_bfm_ldmk3d(face_model_lm3d_path, use_five_anchor=False):
  """load standard facemodel landmark 3d points.

  Args:
      face_model_lm3d_path (_type_): _description_
      use_five_anchor (bool, optional): _description_. Defaults to False.

  """
  ldmk3d = scipy_io.loadmat(face_model_lm3d_path)
  ldmk3d = ldmk3d['lm']
  if use_five_anchor:
      # calculate 5 facial landmarks using 68 landmarks
    lm_idx = np.array([31, 37, 40, 43, 46, 49, 55]) - 1
    ldmk3d = np.stack(
        [
            ldmk3d[lm_idx[0], :],
            np.mean(ldmk3d[lm_idx[[1, 2]], :], 0),
            np.mean(ldmk3d[lm_idx[[3, 4]], :], 0),
            ldmk3d[lm_idx[5], :],
            ldmk3d[lm_idx[6], :],
        ], axis=0)
    ldmk3d = ldmk3d[[1, 2, 0, 3, 4], :]
  else:
    ldmk3d = ldmk3d
  return ldmk3d


#!<----------------------------------------------------------------------------
#!< FACEMSH CONTOUR OPERATION in NUMPY
#!<----------------------------------------------------------------------------


def find_matched_contour(ldmk68, rotation, mean_face):
  """_summary_

  Args:
      ldmk68 (np.ndarray): [68, 2]
      rotation (np.ndarray): [3, ]
      mean_face (np.ndarray): [N, 3]

  Returns:
      _type_: _description_
  """
  rot_m = compute_rotation_matrix(rotation[np.newaxis, :])
  uv, z_buffer, z_axis = projection_layer(mean_face[np.newaxis, :], rot_m, np.zeros((1, 3)))
  uv = uv[0]

  selected_contour_vtx_idx = []
  contours_left = BFM_68P_CONTOUR_LINE[:34]
  for i in range(9):  # 9 left profile contour points in ldmk_68pts
    ldmk = ldmk68[i]
    min_line_idx, min_vtx_idx = find_minmum_index_on_contour(ldmk, uv, contours_left)
    selected_contour_vtx_idx.append(min_vtx_idx)

  contours_right = BFM_68P_CONTOUR_LINE[34:]
  for i in range(9, 17):
    ldmk = ldmk68[i]
    min_line_idx, min_vtx_idx = find_minmum_index_on_contour(ldmk, uv, contours_right)
    selected_contour_vtx_idx.append(min_vtx_idx)

  return selected_contour_vtx_idx


def find_minmum_index_on_contour(ldmk, uv, contour_candidates):
  """specific a 2d landmark, search matched index on contour_candidates and
    return line idx and vertex index.

  Args:
      ldmk (np.ndarray): (2, ) a landmark point.
      uv (np.ndarray): a (N, 2) uv
      contour_candidates (list): _description_
  """
  min_line_idx = 0
  min_vtx_idx = 0
  min_val = np.Infinity
  for i in range(len(contour_candidates)):
    vtx_line = contour_candidates[i]
    dist = np.sqrt(np.sum(np.square(uv[vtx_line] - ldmk), axis=-1))
    min_idx_cur = np.argmin(dist)
    if dist[min_idx_cur] < min_val:
      min_line_idx = i
      min_vtx_idx = vtx_line[min_idx_cur]
      min_val = dist[min_idx_cur]
  return min_line_idx, min_vtx_idx


def find_contour_line(face_shape, contours=BFM_68P_CONTOUR_LINE):
  """find contour line in [-90, 90] degree (yaw)

  Method:
    project 3d face into uv plane, and for each contour line to search for
      far left and far right index on 3d face.

  Args:
      face_shape (np.ndarray): [N, 3]
      contours (list[int]): Defaults to BFM_68P_CONTOUR_LINE.

  Returns:
      contours_on_rot: 180 list of contour idx
  """
  assert len(contours) == 68

  contours_on_rot = []
  for i in range(-90, 91, 1):
    angle = np.array([0, i * np.pi / 180, 0])
    rotation = compute_rotation_matrix(angle[np.newaxis, :])
    uv, _, _ = projection_layer(face_shape[np.newaxis, :], rotation, np.zeros((1, 3)))
    uv = uv[0]
    uv[:, 1] = 224 - uv[:, 1]
    ind_list = []

    # contour lines of left profile
    for contour_list in contours[:34]:
      min_u = 300
      min_ind = 3e5
      for ind in contour_list:
        if uv[ind][0] <= min_u:
          min_u = uv[ind][0]
          min_ind = ind
      ind_list.append(min_ind)

    # contour lines of right profile
    for contour_list in contours[34:]:
      max_u = 0
      max_ind = 3e5
      for ind in contour_list:
        if uv[ind][0] >= max_u:
          max_u = uv[ind][0]
          max_ind = ind
      ind_list.append(max_ind)
    contours_on_rot.append(ind_list)

  return contours_on_rot

#!<----------------------------------------------------------------------------
#!< FACEMSH CONTOUR OPERATION in TORCH
#!<----------------------------------------------------------------------------


def find_contour_candidates(vertex_norm_rotated):
  """Find the indices of mesh contour from the candidates.

  Note:
    1. if all z's are negative on this line, it's invisible
    2. find the minimum positive abs(z) as contour line

  Args:
      vertex_norm_rotated (numpy array): vertex normals array
          of shape [batch_size, N, 3], N is the number of
          vertices.
  Returns:
      selected_idx (numpy array): selected contour point indices
          of shape (batch_size, #contour lines), one point for
          each contour line. There are 68 contour lines in total.
      line_visibility (boolean numpy array): visibility of each
          contour point.
  """
  device = vertex_norm_rotated.device

  batch_size = vertex_norm_rotated.shape[0]
  line_visibility = []
  selected_idx = []
  for line in BFM_68P_CONTOUR_LINE:  # there are 68 contour lines
    # extract points in the line
    # shape = [batch_size, len(line), 3]
    vtx_norm = torch.index_select(
        vertex_norm_rotated,
        dim=1,
        index=torch.tensor(line).to(device),
    )

    # extract z axis, get a tensor of shape [batch_size, len(line)]
    vtx_norm_z = torch.select(vtx_norm, dim=-1, index=2)

    # if all z's are negative on this line, it's invisible
    # shape = (batch_size, 1), boolean
    vis = torch.any(torch.ge(vtx_norm_z, 0), dim=-1, keepdim=True)
    line_visibility.append(vis)

    # find the minimum positive z, shape = (batch_size)
    min_idx = torch.argmin(torch.abs(vtx_norm_z), dim=-1)

    # shape = (batch_size, 1)
    idx = torch.index_select(torch.tensor(line).to(device), dim=-1, index=min_idx).unsqueeze(-1)
    selected_idx.append(idx)

  # concatenate all sub-tensors into one of shape (batch_size, 68)
  selected_idx = torch.cat(selected_idx, axis=-1)
  line_visibility = torch.cat(line_visibility, axis=-1)

  return selected_idx, line_visibility


def landmark_march(selected_idx, line_visibility, uvs, landmarks_gt):
  """Find the closest mesh point for each 2D contour landmark
  point.

  Args:
      selected_idx (torch.Tensor): A tensor of mesh contour indices,
          shape=(batch_size, 68). 68 is the number of mesh
          contour points we selected.
      line_visibility (torch.Tensor): A boolean tensor of visibility
          of each points in selected_idx.
      uvs (torch.Tensor): [bs, 20084, 2] projected 3d-2d points
      landmarks_gt (torch.Tensor): [bs, num_points, 2] groundtruth from landmark detector

  Returns:
      selected_idx_ldmk (numpy array): selected contour point
          indices of shape (batch_size, 17), one point for each
          contour 2d landmark. There are 17 contour landmarks.
      visibility_ldmk (boolean numpy array): visibility of each
          contour point
  """
  batch_size = selected_idx.shape[0]
  selected_idx_ldmk = []
  visibility_ldmk = []

  # uvs shape = (batch_size, vertices_num, 2)
  # selected_idx shape = (batch_size, 68), uv_contour shape = (batch_size, 68, 2)
  selected_idx_repeat = selected_idx.unsqueeze(-1).repeat(1, 1, uvs.shape[2])
  uv_contour = torch.gather(uvs, dim=1, index=selected_idx_repeat)

  # select 17 contour point from 2d ldmk
  for i in range(17):
    # landmarks_gt: (batch_size, 68, 2), out shape = (batch_size, 1, 2)
    ldmk = torch.index_select(landmarks_gt, dim=1, index=torch.tensor([i]).to(landmarks_gt.device))

    # shape = (batch_size, n), n is decremented by 1 each iteration.
    dist = torch.sum((uv_contour - ldmk) ** 2, dim=-1)

    # min_idx shape = (batch_size, 1)
    # torch argmin will get different idx when there are same data in dist
    min_idx = torch.argmin(dist, dim=-1, keepdim=True)

    # np_min_idx = np.argmin(dist.numpy(), axis=-1)
    # pt_min_idx = torch.argmin(dist, dim=-1)
    # print("----------pytorch", pt_min_idx.numpy())
    # print("----------numpy", np_min_idx)

    # idx shape = (batch_size, 1)
    idx = torch.gather(selected_idx, dim=1, index=min_idx)
    selected_idx_ldmk.append(idx)

    # shape=(batch_size, 1)
    vis = torch.gather(line_visibility, dim=1, index=min_idx)
    min_dist = torch.gather(dist, dim=1, index=min_idx)

    # ignore remote closest mesh point, 100 is a hard-coded
    # value. A point is visible only if its visible on the
    # mesh, and its distance to the corresponding landmark
    # is less than 100.
    visibility_ldmk.append(torch.logical_and(vis, torch.lt(min_dist, 100)))

    # remove min_idx from selected_idx and line_visibility
    num_contours_left = selected_idx.shape[1]

    # mask is a boolean tensor, of shape
    # (batch_size, num_contours_left)
    mask = F.one_hot(
        torch.squeeze(min_idx, dim=-1), num_classes=num_contours_left
    ).eq(0)

    # shape=(batch_size, num_contours_left - 1)
    selected_idx = torch.reshape(
        torch.masked_select(selected_idx, mask), (batch_size, num_contours_left - 1)
    )

    line_visibility = torch.reshape(
        torch.masked_select(line_visibility, mask),
        (batch_size, num_contours_left - 1),
    )

    # shape = (batch_size, num_contours_left - 1, 2)
    selected_idx_repeat = selected_idx.unsqueeze(-1).repeat(1, 1, uvs.shape[2])
    uv_contour = torch.gather(uvs, dim=1, index=selected_idx_repeat)

  selected_idx_ldmk = torch.cat(selected_idx_ldmk, axis=1)
  visibility_ldmk = torch.cat(visibility_ldmk, axis=1)

  return selected_idx_ldmk, visibility_ldmk


def dynamic_contour_index(input_vertices_idx, visibility, vertex_norm_rotated, uvs, ldmk_gt):
  """ dynamically find contour points

  Args:
      input_vertices_idx (torch.Tensor): [bs, 68]
      visibility (torch.Tensor): [bs, 68]
      vertex_norm_rotated (torch.Tensor): [bs, 20084, 3]
      uvs (torch.Tensor): [bs, 20084, 2]
      ldmk_gt (torch.Tensor): [bs, 68, 2]

  Returns:
      _type_: _description_
  """
  # select contour line from norm_rotated vertex
  # [bs, 68], [bs, 68]: this 68 means that 68 contour line rather than 2d keypoint.
  selected_idx, line_visibility = find_contour_candidates(vertex_norm_rotated)

  selected_idx_ldmk, visibility_ldmk = landmark_march(selected_idx, line_visibility, uvs, ldmk_gt)

  vertices_idx = torch.cat(
      [
          selected_idx_ldmk,
          torch.index_select(
              input_vertices_idx,
              dim=-1,
              index=torch.tensor(list(range(17, 68))).to(input_vertices_idx.device),
          ),
      ],
      dim=-1,
  )

  contour_vis = torch.logical_and(
      visibility_ldmk,
      torch.index_select(
          visibility,
          dim=-1,
          index=torch.tensor(list(range(17))).to(visibility.device),
      ).eq(1.0),
  )

  visibility = torch.cat(
      [
          contour_vis.float(),
          torch.index_select(
              visibility,
              dim=-1,
              index=torch.tensor(list(range(17, 68))).to(visibility.device),
          ),
      ],
      dim=-1,
  )

  return vertices_idx, visibility

#!<----------------------------------------------------------------------------
#!< LANDMARK TRANSFORM
#!<----------------------------------------------------------------------------


def landmark_240_to_106(landmark_240):
  """Extract eyes and mouth landmarks form 240pts to replace those in
  106pts.

  Arguments:
      ldmks {numpy array} -- numpy array of shape (240, 2)

  """
  ldmks_106pts = landmark_240[:106, :]
  ldmks_134pts = landmark_240[106:, :]
  eyes_idx = [11, 14, 19, 10, 7, 2, 32, 41, 36, 33, 24, 29]
  ldmks_106pts[52:64, :] = ldmks_134pts[eyes_idx]
  mouth_idx = [70, 73, 76, 78, 80, 83, 86, 131, 128, 126, 124, 121, 87, 91, 95, 99, 103, 115, 111, 107]
  ldmks_106pts[84:104, :] = ldmks_134pts[mouth_idx]
  return ldmks_106pts


def landmark_106_to_68(landmark_106):
  index = [0, 1, 3, 5, 7, 10, 12, 14, 16, 17, 19, 21, 23, 26, 28, 30, 32, 35, 36, 37, 39, 41, 42, 43, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
           58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 78, 79, 80, 84, 85, 86, 89, 90, 91, 93, 95, 96, 101, 102, 103, 104, 105]
  return landmark_106[index]


def landmark_106_to_mesh68(landmark_106):
  """standard 106 landmark detector to facemesh 68 landmark order
  """
  index = [
      0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32,  # contour
      33, 34, 35, 36, 37,  # left eyebow
      42, 43, 44, 45, 46,  # right eyebow
      51, 52, 53, 54,  # nose line
      58, 59, 60, 61, 62,  # nose bottom
      66, 67, 69, 70, 71, 73,  # left eye
      75, 76, 78, 79, 80, 82,  # right eye
      84, 85, 86, 87, 88, 89, 90,  # upper lip up
      91, 92, 93, 94, 95,  # bottom lip down
      96, 97, 98, 99, 100,  # upper lip down
      101, 102, 103,  # bottom lip up
  ]
  return landmark_106[index]


#!<----------------------------------------------------------------------------
#!< 3D FACEMESH TRANSFORM
#!<----------------------------------------------------------------------------

def compute_rotation_matrix(angles):
  angle_x = angles[:, 0][0]
  angle_y = angles[:, 1][0]
  angle_z = angles[:, 2][0]

  # compute rotation matrix for X,Y,Z axis respectively
  rotation_X = np.array([1.0, 0, 0,
                         0, np.cos(angle_x), -np.sin(angle_x),
                         0, np.sin(angle_x), np.cos(angle_x)])
  rotation_Y = np.array([np.cos(angle_y), 0, np.sin(angle_y),
                         0, 1, 0,
                         -np.sin(angle_y), 0, np.cos(angle_y)])
  rotation_Z = np.array([np.cos(angle_z), -np.sin(angle_z), 0,
                         np.sin(angle_z), np.cos(angle_z), 0,
                         0, 0, 1])

  rotation_X = np.reshape(rotation_X, [1, 3, 3])
  rotation_Y = np.reshape(rotation_Y, [1, 3, 3])
  rotation_Z = np.reshape(rotation_Z, [1, 3, 3])

  rotation = np.matmul(np.matmul(rotation_Z, rotation_Y), rotation_X)
  rotation = np.transpose(rotation, axes=[0, 2, 1])  # transpose row and column (dimension 1 and 2)

  return rotation


def projection_layer(face_shape, rotation, translation, focal=1015.0, center=112.0):
  """compute re-project position on uv-plane: uv = KMp

  Ref: https://tensors.space/2019/08/%E4%B8%89%E7%BB%B4%E9%87%8D%E5%BB%BA%E6%96%B9%E6%B3%95/

  Args:
      face_shape (np.ndarray): [1, N, 3]
      rotation (np.ndarray): [1, 3, 3]
      translation (np.ndarray): [1, 3]
      focal (float): _description_. Defaults to 1015.0.
      center (float): we choose the focal length and camera position empirically

  Returns:
      face_projection (np.ndarray): [1, N, 2]
      z_buffer (np.ndarray): [1, N, 1]
      z_axis (np.ndarray): [1, N]
  """
  #!< step1. 世界坐标系到相机坐标系: M = [[R, t], [0^T, 1]]
  #!< step1.1 将人脸的平均深度放置到世界 z=0 位置
  # calculate face position in camera space
  face_shape_r = np.matmul(face_shape, rotation)
  # mass center -> normalize z to 0
  mass_center = np.mean(face_shape_r, axis=1)
  z_axis = face_shape_r.copy()[:, :, 2] - mass_center[0][2]
  # apply external translation
  face_shape_t = face_shape_r + np.reshape(translation, [1, 1, 3])
  # 固定相机在平面外
  camera_pos = np.reshape(np.array([0.0, 0.0, 10.0]), [1, 1, 3])  # camera position
  # 原本3dmm构建的人脸是朝着平面向里，现在需要将它反过来
  reverse_z = np.reshape(np.array([1.0, 0, 0, 0, 1, 0, 0, 0, -1.0]), [1, 3, 3])
  face_shape_t = np.matmul(face_shape_t, reverse_z) + camera_pos
  # 至此，相机成为了世界的中心

  #!< step2. 相机坐标系到像素坐标系 [[f/dx, 0, u0], [0, f/dy, v0], [0, 0, 1]]
  p_matrix = np.concatenate([[focal], [0.0], [center], [0.0], [focal], [center],
                            [0.0], [0.0], [1.0]], axis=0)  # projection matrix
  p_matrix = np.reshape(p_matrix, [1, 3, 3])
  # calculate projection of face vertex using perspective projection
  aug_projection = np.matmul(face_shape_t, np.transpose(p_matrix, [0, 2, 1]))
  # normalized by z
  face_projection = aug_projection[:, :, 0:2] / np.reshape(aug_projection[:, :, 2], [1, np.shape(aug_projection)[1], 1])
  z_buffer = np.reshape(aug_projection[:, :, 2], [1, -1, 1])

  return face_projection, z_buffer, z_axis


def estimate_norm(lm_68p, H):
  """similarity transform

  Args:
      lm_68p (_type_): _description_
      H (_type_): _description_

  Returns:
      _type_: _description_
  """
  # 68 points to 5 points
  lm_idx = np.array([31, 37, 40, 43, 46, 49, 55]) - 1
  lm5p = np.stack(
      [
          lm_68p[lm_idx[0], :],
          np.mean(lm_68p[lm_idx[[1, 2]], :], 0),
          np.mean(lm_68p[lm_idx[[3, 4]], :], 0),
          lm_68p[lm_idx[5], :],
          lm_68p[lm_idx[6], :],
      ],
      axis=0,
  )
  lm = lm5p[[1, 2, 0, 3, 4], :]

  lm[:, -1] = H - 1 - lm[:, -1]
  tform = skimage_trans.SimilarityTransform()
  src = np.array(
      [
          [38.2946, 51.6963],
          [73.5318, 51.5014],
          [56.0252, 71.7366],
          [41.5493, 92.3655],
          [70.7299, 92.2041],
      ],
      dtype=np.float32)
  tform.estimate(lm, src)
  M = tform.params
  if np.linalg.det(M) == 0:
    M = np.eye(3)

  return M[0:2, :]


def estimate_norm_torch(lm_68p, H):
  lm_68p_ = lm_68p.detach().cpu().numpy()
  M = []
  for i in range(lm_68p_.shape[0]):
    M.append(estimate_norm(lm_68p_[i], H))
  M = torch.tensor(np.array(M), dtype=torch.float32).to(lm_68p.device)
  return M


def estimate_transform(xp, x):
  npts = xp.shape[1]

  A = np.zeros([2 * npts, 8])

  A[0: 2 * npts - 1: 2, 0:3] = x.transpose()
  A[0: 2 * npts - 1: 2, 3] = 1

  A[1: 2 * npts: 2, 4:7] = x.transpose()
  A[1: 2 * npts: 2, 7] = 1

  b = np.reshape(xp.transpose(), [2 * npts, 1])

  k, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

  R1 = k[0:3]
  R2 = k[4:7]
  sTx = k[3]
  sTy = k[7]
  s = (np.linalg.norm(R1) + np.linalg.norm(R2)) / 2
  t = np.stack([sTx, sTy], axis=0)

  return t, s


def warp_face(image, x1, y1, x2, y2, scale, crop_size):
  """some detector require a simiarity transform
  """
  old_size = (x2 - x1 + y2 - y1) / 2
  center = np.array([x2 - (x2 - x1) / 2.0, y2 - (y2 - y1) / 2.0])
  size = int(old_size * scale)

  # crop image
  src_pts = np.array([
      [center[0] - size / 2, center[1] - size / 2],
      [center[0] - size / 2, center[1] + size / 2],
      [center[0] + size / 2, center[1] - size / 2],
  ])

  dst_pts = np.array([[0, 0], [0, crop_size - 1], [crop_size - 1, 0]])
  tform = skimage_trans.estimate_transform('similarity', src_pts, dst_pts)
  dst_image = skimage_trans.warp(image / 255.0, tform.inverse, output_shape=(crop_size, crop_size)) * 255

  return dst_image.astype('float32')


def align_image(image, ldmk, ldmk3d, mask=None, rescale_factor=102.0,
                target_size=224, use_five_anchor=False, return_params=False):
  """align image to standard BFM model transformation

  Args:
      image (np.ndarray): [H, W, 3] orginal image
      ldmk (np.ndarray): [68, 2] / [5, 2] 2d landmark points
      ldmk3d (np.ndarray): [68, 3] / [5, 3] 3d standard face model landmark

  """
  h0, w0 = image.shape[:2]

  # because 3dfacemesh use reversed y coordinate
  ldmk[..., 1] = h0 - 1 - ldmk[..., 1]

  # mapping 68 points to 5 points
  if use_five_anchor and ldmk.shape[0] != 5:
    lm_idx = np.array([31, 37, 40, 43, 46, 49, 55]) - 1
    lm5p = np.stack(
        [
            ldmk[lm_idx[0], :],
            np.mean(ldmk[lm_idx[[1, 2]], :], 0),
            np.mean(ldmk[lm_idx[[3, 4]], :], 0),
            ldmk[lm_idx[5], :],
            ldmk[lm_idx[6], :],
        ],
        axis=0)
    lm5p = lm5p[[1, 2, 0, 3, 4], :]
  else:
    lm5p = ldmk

  # calculate translation and scale factors using 5 facial landmarks and standard landmarks of a 3D face
  # calculating least square problem for image alignment
  t, s = estimate_transform(lm5p.transpose(), ldmk3d.transpose())
  s = rescale_factor / s

  # processing image: resize and crop image
  w = (w0 * s).astype(np.int32)
  h = (h0 * s).astype(np.int32)
  left = (w / 2 - target_size / 2 + float((t[0] - w0 / 2) * s)).astype(np.int32)
  right = left + target_size
  up = (h / 2 - target_size / 2 + float((h0 / 2 - t[1]) * s)).astype(np.int32)
  below = up + target_size

  image = cv2.resize(image, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 255.0)
  img_new = np.array(Image.fromarray(image.astype('uint8')).crop((left, up, right, below))).astype('float32')

  if mask is not None:
    mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 255.0)
    mask_new = np.array(Image.fromarray(mask.astype('uint8')).crop((left, up, right, below))).astype('float32')
  else:
    mask_new = None

  lm_new = np.stack([ldmk[:, 0] - t[0] + w0 / 2, ldmk[:, 1] - t[1] + h0 / 2], axis=1) * s
  lm_new = lm_new - np.array([(w / 2 - target_size / 2), (h / 2 - target_size / 2)]).reshape([1, 2])

  if return_params:
    return img_new, lm_new, mask_new, t, s
  else:
    return img_new, lm_new, mask_new


def realign(ldmk, t, s, size=224):
  ldmk[..., 0] = (ldmk[..., 0] - size / 2.0) / s + t[0]
  ldmk[..., 1] = (ldmk[..., 1] - size / 2.0) / s + t[1]
  return ldmk


def warp_affine(src, M, dsize, mode='bilinear', padding_mode='zeros', align_corners=None):
  return kornia.warp_affine(src, M, dsize, mode=mode, padding_mode=padding_mode, align_corners=align_corners)

#!<----------------------------------------------------------------------------
#!< 3D FACEMESH EXPORT
#!<----------------------------------------------------------------------------


@torch.no_grad()
def export_facemesh(path, vertex, color, face_buf, lmdk_index=None, camera_distance=10.0, mode='normal'):
  """ save rendered obj with trimesh

  Args:
      path (str): output path
      vertex (torch.Tensor): [1, 20084, 3]
      color (torch.Tensor): [1, 20084, 3]
      face_buf (torch.Tensor): [39744, 3]
      lmdk_index (torch.Tensor): [68] 2d landmark index for 3d facemesh
      camera_distance (float): default to 10.0
      mode (str): 'normal', 'now'

  """
  vertex = vertex.cpu().numpy()  # get reconstructed shape
  vertex[..., -1] = (camera_distance - vertex[..., -1])  # from camera space to world space
  color = color.cpu().numpy()
  tri = face_buf.cpu().numpy()

  for i, (recon_shape, recon_color) in enumerate(zip(vertex, color)):
    cur_path = path if i == 0 else f'{path}_{i}'

    if mode == 'normal':
      mesh = trimesh.Trimesh(
          vertices=recon_shape,
          faces=tri,
          vertex_colors=np.clip(255.0 * recon_color, 0, 255).astype(np.uint8))
      mesh.export(cur_path + '.obj')

    elif mode == 'now':
      mesh = trimesh.Trimesh(vertices=recon_shape, faces=tri)
      mesh.export(cur_path + '.obj')
      ldmk3d = recon_shape[lmdk_index.cpu().numpy(), :]
      key3d = np.zeros((7, 3), dtype=np.float32)
      key3d[0] = ldmk3d[36]
      key3d[1] = ldmk3d[39]
      key3d[2] = ldmk3d[42]
      key3d[3] = ldmk3d[45]
      key3d[4] = ldmk3d[33]
      key3d[5] = ldmk3d[48]
      key3d[6] = ldmk3d[54]
      np.save(cur_path + '.npy', key3d)

    else:
      raise NotImplementedError(mode)


def visualize_facemesh(image,
                       mask,
                       overlay,
                       landmark,
                       landmark_gt=None,
                       contours=None,
                       render_normal=None,
                       render_mask=None,
                       face_proj=None):
  """render network output

  Args:
      image (torch.Tensor): [1, 3, 224, 224] original image range from [0, 1]
      mask (torch.Tensor): [1, 1, 224, 224] skin mask [0, 1]
      overlay (torch.Tensor): [1, 3, 224, 224] rendered image over 3d facemesh [0, 1]
      landmark (torch.Tensor): [1, 68, 2] project 3d facemesh to 2d landmark
      landmark_gt (torch.Tensor, optional): [1, 68, 2] groundtruth of 2d landmark

  Returns:
      rendered image (list[np.ndarray]): [[224, 224, 3], ...]

  """
  bs, c, h, w = image.shape
  outputs = []

  for i in range(bs):
    concats = []

    image_i = image[i].cpu().mul(255).clamp(0, 255).permute(1, 2, 0).numpy()
    concats.append(image_i)

    if mask is not None and overlay is not None:
      mask_i = mask[i].cpu().permute(1, 2, 0).numpy()
      overlay_i = overlay[i].mul(255).clamp(0, 255).cpu().permute(1, 2, 0).numpy()
      blend_i = overlay_i * mask_i + (1.0 - mask_i) * image_i
      concats.append(blend_i)

    if landmark is not None:
      ldmk_i = landmark[i].cpu().numpy()
      ldmk_i[..., 1] = h - ldmk_i[..., 1] - 1
      ldmk_i = drawer.keypoints(image_i.copy(), ldmk_i, color=(255, 255, 0), radius=1)

    if landmark is not None and landmark_gt is not None:
      ldmk_gt_i = landmark_gt[i].cpu().numpy()
      ldmk_gt_i[..., 1] = h - ldmk_gt_i[..., 1] - 1
      ldmk_i = drawer.keypoints(ldmk_i, ldmk_gt_i, color=(255, 0, 0), radius=1)

    if landmark is not None:
      concats.append(ldmk_i)

    if contours is not None and face_proj is not None:
      contour_i = image_i.copy()
      face_proj_i = face_proj[i].cpu().numpy()
      face_proj_i[..., 1] = h - face_proj_i[..., 1] - 1
      for contour in contours:
        proj = face_proj_i[contour]
        proj = [proj.reshape(-1, 1, 2).astype('int32')]
        contour_i = cv2.polylines(contour_i, proj, True, (255, 255, 255), 1)
      concats.append(contour_i)

    if render_normal is not None:
      render_normal_i = render_normal[i].cpu().permute(1, 2, 0).numpy()
      concats.append((render_normal_i + 1.0) / 2.0 * 255.0)

    if render_mask is not None:
      render_mask_i = render_mask[i].cpu().permute(1, 2, 0).numpy()
      concats.append(render_mask_i * 255.0)

    vis = np.concatenate(concats, axis=-2)
    outputs.append(vis)

  return outputs


def visualize_facemesh_orgin(t,
                             s,
                             image,
                             mask,
                             overlay=None,
                             landmark=None,
                             landmark_gt=None,
                             contours=None,
                             render_normal=None,
                             render_mask=None,
                             face_proj=None,
                             size=224):
  """render facemesh on orginal image

  Optimize:
    From
      1 401.0019302368164
      2 1.5652179718017578
      3 1.1909008026123047
      4 0.00095367431640625
      5 26.248455047607422
      6 380.81884384155273
      7 265.5680179595947
    To
      1 10.508537292480469
      2 1.0211467742919922
      3 0.5130767822265625
      4 0.0007152557373046875
      5 20.08509635925293
      6 20.233631134033203
      7 14.40286636352539

  Args:
      image (np.ndarray): [original_h, original_w, 3]
      t (np.array([t0 , t1])): center point of face in original image
      s (float): scale for image resize
      mask (torch.Tensor):
      overlay (torch.Tensor):
      landmark (torch.Tensor):
      landmark_gt (torch.Tensor):
      contours (torch.Tensor):
      render_normal (torch.Tensor):
      render_mask (torch.Tensor):
      face_proj (torch.Tensor):

  """
  assert len(image.shape) and isinstance(image, np.ndarray)
  h0, w0, c = image.shape
  outputs = []
  offset = realign(np.array([[0, 0]]), t, s, size=224)
  th, tw = int(224 / s), int(224 / s)
  x1, y1 = int(offset[0][0]), h0 - int(offset[0][1]) - th

  for i in range(mask.size(0)):
    concats = []

    image_i = image.copy()
    ih, iw = image_i.shape[:2]
    concats.append(image_i)

    # compute padding size
    ph, pw = ih + 2 * th, iw + 2 * tw
    # compute padding start point
    py, px = y1 + th, x1 + tw

    if mask is not None and overlay is not None:
      mask_i = mask[i].cpu().permute(1, 2, 0).numpy()
      mask_i = cv2.resize(mask_i, (tw, th), interpolation=cv2.INTER_NEAREST)
      mask_i = np.stack([mask_i, mask_i, mask_i], axis=2)
      overlay_i = overlay[i].mul(255).clamp(0, 255).cpu().permute(1, 2, 0).numpy()
      overlay_i = cv2.resize(overlay_i, (tw, th), interpolation=cv2.INTER_NEAREST)
      # padding and then blend
      tmp = np.zeros([ph, pw, 3]).astype('float32')
      tmp[th: th + ih, tw: tw + iw] = image_i
      tmp[py: py + th, px: px + tw] = overlay_i * mask_i + (1 - mask_i) * tmp[py: py + th, px: px + tw]
      # crop back
      tmp = tmp[th: th + ih, tw: tw + iw]
      concats.append(tmp)

    if landmark is not None:
      ldmk_i = landmark[i].cpu().numpy()
      ldmk_i = realign(ldmk_i, t, s, size)
      ldmk_i[..., 1] = h0 - ldmk_i[..., 1] - 1
      ldmk_i = drawer.keypoints(image_i.copy(), ldmk_i, color=(255, 255, 0), radius=2)

    if landmark is not None and landmark_gt is not None:
      ldmk_gt_i = landmark_gt[i].cpu().numpy()
      ldmk_gt_i = realign(ldmk_gt_i, t, s, size)
      ldmk_gt_i[..., 1] = h0 - ldmk_gt_i[..., 1] - 1
      ldmk_i = drawer.keypoints(ldmk_i, ldmk_gt_i, color=(255, 0, 0), radius=2)

    if landmark is not None:
      concats.append(ldmk_i)

    if contours is not None and face_proj is not None:
      contour_i = image_i.copy()
      face_proj_i = realign(face_proj[i].cpu().numpy(), t, s, size)
      face_proj_i[..., 1] = h0 - face_proj_i[..., 1] - 1
      for contour in contours:
        proj = face_proj_i[contour]
        proj = [proj.reshape(-1, 1, 2).astype('int32')]
        contour_i = cv2.polylines(contour_i, proj, True, (255, 255, 255), 1)
      concats.append(contour_i)

    if render_normal is not None:
      render_normal_i = render_normal[i].cpu().permute(1, 2, 0).numpy()
      render_normal_i = cv2.resize(render_normal_i, (tw, th), interpolation=cv2.INTER_NEAREST)
      # padding
      tmp = np.zeros([ph, pw, 3]).astype('float32')
      tmp[th: th + ih, tw: tw + iw] = image_i
      cond = np.all(np.abs(render_normal_i) > 0, axis=2)
      tmp[py: py + th, px: px + tw][cond] = (render_normal_i[cond] + 1.0) / 2.0 * 255
      # crop back
      tmp = tmp[th: th + ih, tw: tw + iw]
      concats.append(tmp)

    if render_mask is not None:
      render_mask_i = render_mask[i].cpu().permute(1, 2, 0).numpy()
      render_mask_i = cv2.resize(render_mask_i, (tw, th), interpolation=cv2.INTER_NEAREST)
      # padding
      tmp = np.zeros([ph, pw, 3]).astype('float32')
      tmp[th: th + ih, tw: tw + iw] = image_i
      cond = np.any(np.abs(render_mask_i) > 0, axis=2)
      tmp[py: py + th, px: px + tw][cond] = render_mask_i[cond] * 255.0
      # crop back
      tmp = tmp[th: th + ih, tw: tw + iw]
      concats.append(tmp)

    vis = np.concatenate(concats, axis=-2)
    outputs.append(vis)

  return outputs

#!<----------------------------------------------------------------------------
#!< POSE RELATED FUNCTION
#!<----------------------------------------------------------------------------


def visualize_pose_cube(img, yaw, pitch, roll, tdx=None, tdy=None, size=150.):
  # Input is a cv2 image
  # pose_params: (pitch, yaw, roll, tdx, tdy)
  # Where (tdx, tdy) is the translation of the face.
  # For pose we have [pitch yaw roll tdx tdy tdz scale_factor]

  p = pitch * np.pi / 180
  y = -yaw * np.pi / 180
  r = roll * np.pi / 180

  if tdx is not None and tdy is not None:
    face_x = int(tdx - 0.50 * size)
    face_y = int(tdy - 0.50 * size)
  else:
    height, width = img.shape[:2]
    face_x = int(width / 2 - 0.5 * size)
    face_y = int(height / 2 - 0.5 * size)

  x1 = int(size * (math.cos(y) * math.cos(r)) + face_x)
  y1 = int(size * (math.cos(p) * math.sin(r) + math.cos(r) * math.sin(p) * math.sin(y)) + face_y)
  x2 = int(size * (-math.cos(y) * math.sin(r)) + face_x)
  y2 = int(size * (math.cos(p) * math.cos(r) - math.sin(p) * math.sin(y) * math.sin(r)) + face_y)
  x3 = int(size * (math.sin(y)) + face_x)
  y3 = int(size * (-math.cos(y) * math.sin(p)) + face_y)

  # Draw base in red
  cv2.line(img, (face_x, face_y), (x1, y1), (0, 0, 255), 3)
  cv2.line(img, (face_x, face_y), (x2, y2), (0, 0, 255), 3)
  cv2.line(img, (x2, y2), (x2 + x1 - face_x, y2 + y1 - face_y), (0, 0, 255), 3)
  cv2.line(img, (x1, y1), (x1 + x2 - face_x, y1 + y2 - face_y), (0, 0, 255), 3)
  # Draw pillars in blue
  cv2.line(img, (face_x, face_y), (x3, y3), (255, 0, 0), 2)
  cv2.line(img, (x1, y1), (x1 + x3 - face_x, y1 + y3 - face_y), (255, 0, 0), 2)
  cv2.line(img, (x2, y2), (x2 + x3 - face_x, y2 + y3 - face_y), (255, 0, 0), 2)
  cv2.line(img, (x2 + x1 - face_x, y2 + y1 - face_y), (x3 + x1 + x2 - 2 * face_x, y3 + y2 + y1 - 2 * face_y), (255, 0, 0), 2)  # nopep8
  # Draw top in green
  cv2.line(img, (x3 + x1 - face_x, y3 + y1 - face_y), (x3 + x1 + x2 - 2 * face_x, y3 + y2 + y1 - 2 * face_y), (0, 255, 0), 2)  # nopep8
  cv2.line(img, (x2 + x3 - face_x, y2 + y3 - face_y), (x3 + x1 + x2 - 2 * face_x, y3 + y2 + y1 - 2 * face_y), (0, 255, 0), 2)  # nopep8
  cv2.line(img, (x3, y3), (x3 + x1 - face_x, y3 + y1 - face_y), (0, 255, 0), 2)
  cv2.line(img, (x3, y3), (x3 + x2 - face_x, y3 + y2 - face_y), (0, 255, 0), 2)

  return img


def visualize_axis3d(img, yaw, pitch, roll, tdx=None, tdy=None, size=100):
  """
  """
  pitch = pitch * np.pi / 180
  yaw = -yaw * np.pi / 180
  roll = roll * np.pi / 180

  if tdx is not None and tdy is not None:
    tdx = tdx
    tdy = tdy
  else:
    height, width = img.shape[:2]
    tdx = width / 2
    tdy = height / 2

  # X-Axis pointing to right. drawn in red
  x1 = size * (math.cos(yaw) * math.cos(roll)) + tdx
  y1 = size * (math.cos(pitch) * math.sin(roll) + math.cos(roll) * math.sin(pitch) * math.sin(yaw)) + tdy

  # Y-Axis | drawn in green
  #        v
  x2 = size * (-math.cos(yaw) * math.sin(roll)) + tdx
  y2 = size * (math.cos(pitch) * math.cos(roll) - math.sin(pitch) * math.sin(yaw) * math.sin(roll)) + tdy

  # Z-Axis (out of the screen) drawn in blue
  x3 = size * (math.sin(yaw)) + tdx
  y3 = size * (-math.cos(yaw) * math.sin(pitch)) + tdy

  cv2.line(img, (int(tdx), int(tdy)), (int(x1), int(y1)), (0, 0, 255), 4)
  cv2.line(img, (int(tdx), int(tdy)), (int(x2), int(y2)), (0, 255, 0), 4)
  cv2.line(img, (int(tdx), int(tdy)), (int(x3), int(y3)), (255, 0, 0), 4)

  return img


def compute_normalize_vector(v):
  """normalize vector a = v / |v|

  Args:
      v (_type_): _description_

  Returns:
      _type_: _description_
  """
  device = v.device
  batch = v.shape[0]
  v_mag = torch.sqrt(v.pow(2).sum(1))  # batch
  eps = 1e-8
  v_mag = torch.max(v_mag, torch.tensor(eps).to(device))
  v = v / v_mag
  return v


def compute_cross_product(u, v):
  """compute norm vector of u, v vector

  Args:
      u (torch.Tnesor): [B, 3]
      v (torch.Tnesor): [B, 3]

  Returns:
      norm: [B, 3]
  """
  batch = u.shape[0]
  i = u[:, 1] * v[:, 2] - u[:, 2] * v[:, 1]
  j = u[:, 2] * v[:, 0] - u[:, 0] * v[:, 2]
  k = u[:, 0] * v[:, 1] - u[:, 1] * v[:, 0]
  out = torch.cat((i.view(batch, 1), j.view(batch, 1), k.view(batch, 1)), 1)
  return out


def compute_rotation_matrix_from_ortho6d(poses):
  """compute ration matrix from ortho6d

  Args:
      poses (torch.Tensor): [B, 6]
  """
  x_raw = poses[:, 0:3]  # [batch, 3]
  y_raw = poses[:, 3:6]  # [batch, 3]

  x = compute_normalize_vector(x_raw)  # [batch, 3]
  z = compute_cross_product(x, y_raw)  # [batch, 3]
  z = compute_normalize_vector(z)  # [batch, 3]
  y = compute_cross_product(z, x)  # [batch, 3]

  x = x.view(-1, 3, 1)
  y = y.view(-1, 3, 1)
  z = z.view(-1, 3, 1)
  matrix = torch.cat((x, y, z), 2)  # [batch, 3, 3]
  return matrix


def compute_euler_angles_from_rotation_matrices(rotation_matrices):
  """compute euler angles from rotation matrices

  Args:
      rotation_matrices (torch.Tensor): [B, 3, 3]

  Returns:
      euler degree: [B, 3]
  """
  batch = rotation_matrices.shape[0]
  R = rotation_matrices
  sy = torch.sqrt(R[:, 0, 0] * R[:, 0, 0] + R[:, 1, 0] * R[:, 1, 0])
  singular = sy < 1e-6
  singular = singular.float()

  x = torch.atan2(R[:, 2, 1], R[:, 2, 2])
  y = torch.atan2(-R[:, 2, 0], sy)
  z = torch.atan2(R[:, 1, 0], R[:, 0, 0])

  xs = torch.atan2(-R[:, 1, 2], R[:, 1, 1])
  ys = torch.atan2(-R[:, 2, 0], sy)
  zs = R[:, 1, 0] * 0

  out_euler = torch.zeros(batch, 3).to(rotation_matrices.device)
  out_euler[:, 0] = x * (1 - singular) + xs * singular
  out_euler[:, 1] = y * (1 - singular) + ys * singular
  out_euler[:, 2] = z * (1 - singular) + zs * singular

  return out_euler
