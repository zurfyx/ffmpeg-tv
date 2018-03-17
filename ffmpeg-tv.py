#!/usr/bin/env python
#
# --------------------------------------------------------------------------------------------------
# == FFMPEG TV STANDARDS ==
# UPDATED FOR 2016 STANDARDS https://scenerules.org/t.html?id=tvx2642k16.nfo
# Author: zurfyx (https://stackoverflow.com/users/2013580/zurfyx)
# Special thanks to: slhck (https://superuser.com/users/48078/slhck)
# https://superuser.com/questions/582198/how-can-i-get-high-quality-low-size-mp4s-like-the-lol-release-group
# --------------------------------------------------------------------------------------------------
#
# Example usages:
# ./ffmpeg-tv.py input.flv output.mkv
# (Resize to HD) ./ffmpeg-tv.py input.mp4 output.mkv --scale "1920:1080"

import argparse
import subprocess

class Default:
  # 1.3) Providers which downscale 1080i to 720p (e.g. BellTV) are not allowed.
  # 5.10) Resized video must be within 0.5% of the original aspect ratio.
  scale="-1:-1" # <width>:<height>; -1 maintain ratio.

  # 4.1) Video must be H.264/MPEG-4 AVC encoded with x264 8-bit.
  video_encoder="libx264"

  # 4.4) Constant Rate Factor (--crf) must be used.
  # 4.4.1) CRF values below 18 and above 23 are never allowed.
  # http://slhck.info/video/2017/02/24/crf-guide.html
  # (lossless) 0 <- (better) 23 <- (worst) 51
  # ┌─────────────────┬───────┬───────────────────────────────────────────┐
  # │ Compressibility      │  CRF    │ General Examples                                      │
  # ├─────────────────┼───────┼───────────────────────────────────────────┤
  # │ High                 │ 18-19   │ Scripted, Talk Shows, Animation, Stand-Up             │
  # │ Medium               │ 20-21   │ Documentary, Reality, Variety, Poker                  │
  # │ Low                  │ 22-23   │ Sports, Awards, Live Events                           │
  # └─────────────────┴───────┴───────────────────────────────────────────┘
  crf="19"

  # 4.6) Settings cannot go below what is specified by preset (--preset) 'slow'.
  preset="slow"

  # 4.7) Level (--level) must be '4.1'.
  level="4.1"

  # 6.4) Only sharp resizers, such as Spline36Resize, BlackmanResize or LanczosResize/Lanczos4Resize,
  # must be used.
  # 6.4.1) Simple resizers, such as Bicubic, PointResize or Simple, are not allowed. 
  resizer="lanczos"

  # 4.17) Optional tuning (--tune) parameters allowed are: 'film', 'grain' or 'animation'. 
  # https://superuser.com/questions/564402/explanation-of-x264-tune
  # film – intended for high-bitrate/high-quality movie content. Lower deblocking is used here.
  tune="film"

  # 8.1) Audio must be in the original format provided.
  # 8.1.1) Transcoding audio is not allowed.
  # 8.2) Multiple language audio tracks are allowed.
  # Since we cannot ensure that the external content is in an acceptable TV format, we'll recode
  # it into aac. We're just playing safe here.
  # 
  # FFmpeg supports two AAC-LC encoders (aac and libfdk_aac) and one HE-AAC (v1/2) encoder
  # (libfdk_aac). The license of libfdk_aac is not compatible with GPL, so the GPL does not permit
  # distribution of binaries containing incompatible code when GPL-licensed code is also included.
  # libfdk_aac is "non-free", and requires ffmpeg to be compiled manually.
  # Second best encoder is the native FFmpeg AAC encoder. (aac)
  audio_encoder="aac"

  # Audio quality (bit rate).
  # Use either VBR or CBR. VBR is the easiest.
  # https://trac.ffmpeg.org/wiki/Encode/AAC#fdk_vbr
  # VBR: Target a quality, rather than a specific bit rate. 1 is lowest quality and 5 is highest
  # quality.
  # https://trac.ffmpeg.org/wiki/Encode/AAC#fdk_cbr
  # http://wiki.hydrogenaud.io/index.php?title=Fraunhofer_FDK_AAC#Bitrate_Modes
  # CBR: kbps
  vbr="5"
  cbr=None

  # 8.2) Multiple language audio tracks are allowed.
  # 8.2.1) The default audio track must be the language intended for release (e.g. An English release
  # containing English, German and Russian audio tracks, must have the default flag set on the English
  # track).
  # https://trac.ffmpeg.org/wiki/Map
  # Include "all" inputs to the output: -map 0
  map="0"

  # Sample (encode few seconds only).
  time_start=None # Seconds (i.e. 30) or timestamp (i.e. 00:00:30.0).
  time_duration=None # Seconds

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description='FFmpeg TV.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
  )
  parser.add_argument('input', type=str, help='input video'),
  parser.add_argument('output', type=str, help='output video'),
  parser.add_argument('-s', '--scale', type=str, default=Default.scale, help='scale', metavar='')
  parser.add_argument('-ve', '--video-encoder', type=str, default=Default.video_encoder, help='video encoder', metavar='')
  parser.add_argument('-c', '--crf', type=str, default=Default.crf, help='constant rate factor (crf)', metavar='')
  parser.add_argument('-p', '--preset', type=str, default=Default.preset, help='preset', metavar='')
  parser.add_argument('-l', '--level', type=str, default=Default.level, help='level', metavar='')
  parser.add_argument('-r', '--resizer', type=str, default=Default.resizer, help='resizer', metavar='')
  parser.add_argument('-t', '--tune', type=str, default=Default.tune, help='tune', metavar='')
  parser.add_argument('-ae', '--audio-encoder', type=str, default=Default.audio_encoder, help='audio encoder', metavar='')
  parser.add_argument('-vb', '--vbr', type=str, default=Default.vbr, help='variable bitrate (vbr)', metavar='')
  parser.add_argument('-cb', '--cbr', type=str, default=Default.cbr, help='constant bitrate (cbr)', metavar='')
  parser.add_argument('-m', '--map', type=str, default=Default.map, help='map', metavar='')
  parser.add_argument('-ts', '--time-start', type=str, default=Default.time_start, help='time start', metavar='')
  parser.add_argument('-td', '--time-duration', type=str, default=Default.time_duration, help='time duration', metavar='')
  
  args = parser.parse_args()
  
  ffmpeg_query = ['ffmpeg']
  ffmpeg_query += ['-i', args.input]
  if (args.scale):
    ffmpeg_query += ['-filter:v', 'scale=%s' % args.scale]
  if (args.video_encoder):
    ffmpeg_query += ['-c:v', args.video_encoder]
  if (args.crf):
    ffmpeg_query += ['-crf', args.crf]
  if (args.preset):
    ffmpeg_query += ['-preset', args.preset]
  if (args.level):
    ffmpeg_query += ['-level', args.level]
  if (args.resizer):
    ffmpeg_query += ['-sws_flags', args.resizer]
  if (args.tune):
    ffmpeg_query += ['-tune', args.tune]
  if (args.audio_encoder):
    ffmpeg_query += ['-c:a', args.audio_encoder]
  if (args.vbr):
    ffmpeg_query += ['-vbr', args.vbr]
  if (args.cbr):
    ffmpeg_query += ['-b:a', args.cbr]
  if (args.map):
    ffmpeg_query += ['-map', args.map]
  if (args.time_start):
    ffmpeg_query += ['-ss', args.time_start]
  if (args.time_duration):
    ffmpeg_query += ['-t', args.time_duration]
  ffmpeg_query += [args.output]
  
  print('> ' + ' '.join(ffmpeg_query))
  subprocess.call(ffmpeg_query)
