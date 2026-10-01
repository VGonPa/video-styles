#!/bin/bash
# vaporwave: draw frames → events → synth audio → mp4 (H.264 30fps, full-range yuv420p like the other styles, crf18 + AAC 48k stereo) → delete frames → preview.gif
# Needs Node + Playwright (global @playwright/test, or PLAYWRIGHT_DIR=<playwright-core dir>), chromium headless shell, ffmpeg, python3 + numpy.
set -e; cd "$(dirname "$0")"; SLUG=$(basename "$PWD"); DUR=${DUR:-10}; WORKERS=${WORKERS:-2}
FR=$(mktemp -d "${TMPDIR:-/tmp}/${SLUG}_frames.XXXX")
trap 'rm -rf "$FR"' EXIT
node render.mjs "$FR" 30 0 $DUR $WORKERS
node events.mjs && python3 audio.py
ffmpeg -loglevel error -y -framerate 30 -i "$FR/%05d.jpg" -i audio.wav -map 0:v -map 1:a \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest -movflags +faststart $SLUG.mp4
rm -rf "$FR" audio.wav
# preview: same settings as make_previews.py
ffmpeg -nostdin -v error -y -i $SLUG.mp4 -filter_complex "[0:v]fps=6,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" -loop 0 preview.gif
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels -of compact $SLUG.mp4
