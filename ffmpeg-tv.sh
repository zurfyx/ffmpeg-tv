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
# (HD) ./ffmpeg-tv.py input.mp4 output.mkv --scale="-1:1080"

input=$1
output=$2

# DEBUG (encode few seconds only).
start="30" # Seconds (30) or timestamp (00:00:30.0).
seconds="30"

# 1.3) Providers which downscale 1080i to 720p (e.g. BellTV) are not allowed.
scale="-1:720" # <width>:<height>; -1 maintain ratio.

# 4.1) Video must be H.264/MPEG-4 AVC encoded with x264 8-bit.
videoEncoder="libx264"

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
audioEncoder="aac"

# Audio quality (bit rate).
# Use either VBR or CBR. VBR is the easiest.
# https://trac.ffmpeg.org/wiki/Encode/AAC#fdk_vbr
# VBR: Target a quality, rather than a specific bit rate. 1 is lowest quality and 5 is highest
# quality.
# https://trac.ffmpeg.org/wiki/Encode/AAC#fdk_cbr
# http://wiki.hydrogenaud.io/index.php?title=Fraunhofer_FDK_AAC#Bitrate_Modes
# CBR: kbps
VBR=""
CBR=""

# 8.2) Multiple language audio tracks are allowed.
# 8.2.1) The default audio track must be the language intended for release (e.g. An English release
# containing English, German and Russian audio tracks, must have the default flag set on the English
# track).
# https://trac.ffmpeg.org/wiki/Map
# Include "all" inputs to the output: -map 0
map="-map 0"

ffmpeg -i $INPUT -c:v libx264 -crf 19 -level 4.1 -preset slow -tune film -filter:v scale=-1:1080 -sws_flags lanczos -c:a aac -vbr 5 -ss 30 -t 5 -map 0 $OUTPUT