#!/bin/bash
# surrealism: render the frames → write the sound cues → synthesise audio.wav → encode the mp4
# (H.264 at 30 fps, full range from the JPEG frames, CRF 18; AAC 192k, 48 kHz stereo; faststart)
# → remove the frames and the wav → preview.gif with the catalog's make_previews settings.
# Needs Node + Playwright (global @playwright/test, or PLAYWRIGHT_DIR=<playwright-core dir>), the chromium
# headless shell (WebGL2 through ANGLE on Metal, see render.json), ffmpeg, python3 + numpy.
# WORKERS sets the number of browser pages (2 at most).
set -e; cd "$(dirname "$0")"; SLUG=$(basename "$PWD"); DUR=${DUR:-10.4}; WORKERS=${WORKERS:-2}; CRF=${CRF:-18}
FR=$(mktemp -d "${TMPDIR:-/tmp}/${SLUG}_frames.XXXX")
trap 'rm -rf "$FR"' EXIT
node render.mjs "$FR" 30 0 $DUR $WORKERS
node events.mjs && python3 audio.py
ffmpeg -loglevel error -y -framerate 30 -i "$FR/%05d.jpg" -i audio.wav -map 0:v -map 1:a \
  -c:v libx264 -preset slow -crf $CRF -pix_fmt yuvj420p -r 30 \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest -movflags +faststart $SLUG.mp4
rm -rf "$FR" audio.wav
# preview, filtered exactly like make_previews.py
ffmpeg -nostdin -v error -y -i $SLUG.mp4 -filter_complex "[0:v]fps=6,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" -loop 0 preview.gif
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,pix_fmt,color_range,sample_rate,channels -of compact $SLUG.mp4
