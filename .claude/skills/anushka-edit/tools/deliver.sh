#!/bin/sh
# Shareable copies under the 30 MB chat upload limit, keeping the master untouched.
# Usage: sh deliver.sh <master.mp4> <out-dir>
# Writes <name>-share.mp4 (same resolution, bitrate sized to ~26 MB) and, for vertical video, <name>-phone.mp4 (720p).
set -e
m="$1"; out="${2:-.}"; mkdir -p "$out"
n=$(basename "$m" .mp4); d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$m")
kb=$(awk -v d="$d" 'BEGIN{b=int(26*8192/d)-256; if(b>40000)b=40000; print b}')
ffmpeg -v error -y -i "$m" -c:v libx264 -preset slow -b:v ${kb}k -maxrate $((kb*12/10))k -bufsize $((kb*2))k -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 192k -movflags +faststart "$out/$n-share.mp4"
w=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$m")
if [ "${w%,*}" -lt "${w#*,}" ]; then
  ffmpeg -v error -y -i "$m" -vf scale=720:-2 -c:v libx264 -preset slow -crf 27 -c:a aac -b:a 128k -movflags +faststart "$out/$n-phone.mp4"
fi
ls -la "$out/$n"-*.mp4
