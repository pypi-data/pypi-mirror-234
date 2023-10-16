# Copyright 2020 The KaiJIN Authors. All Rights Reserved.
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
import argparse
import tw


def cmd_video_to_image(config):
  """Usage:

    python -m tw.tools.media -t video_to_image -s xxx/aaa.mp4 -d aaa

  """
  def convert(src, dst):
    if dst is None:
      dst = os.path.join(os.path.dirname(src), os.path.splitext(os.path.basename(src))[0])
      if not os.path.exists(dst):
        os.makedirs(dst)
    else:
      if not os.path.exists(dst):
        os.makedirs(dst)
      elif not os.path.isdir(dst):
        raise ValueError(dst)
    assert os.path.isfile(src), "src should be a valid file."
    cmd = 'ffmpeg -i {} -vf scale=in_color_matrix=bt709:in_range=pc {}/%08d.png'.format(src, dst)
    tw.logger.info(cmd)
    os.system(cmd)

  dst = config.dst
  src = config.src
  if os.path.isfile(src):
    convert(src, dst)
  else:
    _, videos = tw.media.collect(src)
    for path in videos:
      convert(path, os.path.join(dst, os.path.basename(path)))


def cmd_image_to_video(parser):
  """Usage: convert image folder to x264 mp4.

    python -m tw.tools.media -t image_to_folder -s xxx/%08d.png -d xxx.mp4

  """

  parser.add_argument('--crf', type=int, default=8, help='crf')
  parser.add_argument('--fps', type=int, default=24, help='frame rate')
  args, _ = parser.parse_known_args()

  dst = args.dst
  src = args.src
  fps = args.fps
  crf = args.crf

  assert os.path.isdir(src), "require src to be folder."
  if dst is None:
    dst = os.path.dirname(src) + '.mp4'

  cmd = f"ffmpeg -y -i {src}/%08d.png -c:v libx264 -pix_fmt yuv420p -vf scale=out_color_matrix=bt709:out_range=pc -colorspace bt709 -r {fps} -crf {crf} {dst}"

  tw.logger.info(cmd)
  os.system(cmd)


def cmd_image_concat(config):
  pass


def cmd_image_concat_vertical(config):
  pass


def cmd_video_concat(config):
  pass


def cmd_video_concat_vertical(config):
  pass


def cmd_resize(config):
  pass


if __name__ == "__main__":

  choices = [
      'video_to_image',
      'image_to_video',
      'image_concat',
      'image_concat_vertical',
      'video_concat',
      'video_concat_vertical',
      'resize'
  ]

  parser = argparse.ArgumentParser()
  parser.add_argument('-t', '--task', type=str, choices=choices)
  parser.add_argument('-s', '--src', type=str, default=None)
  parser.add_argument('-d', '--dst', type=str, default=None)

  args, _ = parser.parse_known_args()

  if args.task == 'video_to_image':
    cmd_video_to_image(args)

  elif args.task == 'image_to_video':
    cmd_image_to_video(parser)

  elif args.task == 'image_concat':
    cmd_image_concat(args)

  elif args.task == 'image_concat_vertical':
    cmd_image_concat_vertical(args)

  elif args.task == 'video_concat':
    cmd_video_concat(args)

  elif args.task == 'video_concat_vertical':
    cmd_video_concat_vertical(args)

  elif args.task == 'resize':
    cmd_resize(args)
