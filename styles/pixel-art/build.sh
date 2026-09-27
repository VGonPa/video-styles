#!/bin/bash
# draw frames → mp4 (H.264 30fps yuv420p crf18 + AAC) → delete frames folder
set -e; cd "$(dirname "$0")"; SLUG=$(basename "$PWD"); DUR=${DUR:-10}
while [ "$(memory_pressure | tail -1 | grep -oE '[0-9]+')" -lt 25 ]; do echo "Low memory, waiting"; sleep 20; done
rm -rf _frames; node render.mjs _frames 30 0 $DUR 2
node events.mjs && python3 audio.py
ffmpeg -loglevel error -y -framerate 30 -i _frames/%05d.jpg -i audio.wav -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k -shortest -movflags +faststart out/$SLUG.mp4
rm -rf _frames
ffmpeg -loglevel error -y -i out/$SLUG.mp4 -vf "fps=2,scale=480:-1,tile=4x5" -frames:v 1 _contact_sheet.jpg
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact out/$SLUG.mp4
