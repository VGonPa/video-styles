#!/bin/bash
# Render stills spread over the clip, tile them into one image to look at, and keep two full-size key frames.
#
#   scripts/contact_sheet.sh <project-dir> [duration=10] [count=16] [out=_review]
#
# Writes <project-dir>/<out>/sheet.jpg (4 columns), key-1.jpg (at 1/3 of the clip) and key-2.jpg (at 2/3).
# KEYS="3.75,3.9" adds full-size stills at those times as key-3.jpg, key-4.jpg… (e.g. the held final pose).
# Run it once with out=_reference/original before editing, to keep full-resolution stills of the original.
# WORKERS=1 renders with one browser page (default 2). Needs what build.sh needs for frames (Node +
# Playwright) plus ffmpeg and python3.
set -euo pipefail
DIR=${1:?usage: contact_sheet.sh <project-dir> [duration] [count] [out]}
DUR=${2:-10}; N=${3:-16}; OUT=${4:-_review}
cd "$DIR"
[ -f render.mjs ] && [ -f anim.html ] || { echo "$DIR has no render.mjs and anim.html; fetch a style first" >&2; exit 1; }
TMP=$(mktemp -d "${TMPDIR:-/tmp}/sheet.XXXX"); trap 'rm -rf "$TMP"' EXIT
mkdir -p "$OUT"
# Times at the middle of N equal slices, two decimals: render.mjs names stills t_<t.toFixed(2)>.jpg.
TIMES=$(python3 -c "d, n = float('$DUR'), int('$N'); print(','.join(f'{(i + .5) * d / n:.2f}' for i in range(n)))")
KEYT=$(python3 -c "d = float('$DUR'); extra = [float(x) for x in '${KEYS:-}'.split(',') if x.strip()]; print(','.join(f'{x:.2f}' for x in [d / 3, 2 * d / 3, *extra]))")
node render.mjs "$TMP" 30 0 "$DUR" "${WORKERS:-2}" "$TIMES,$KEYT"
k=0
IFS=, read -ra KLIST <<< "$KEYT"
for t in "${KLIST[@]}"; do
  k=$((k + 1)); cp "$TMP/t_$t.jpg" "$OUT/key-$k.jpg"
done
i=0
IFS=, read -ra LIST <<< "$TIMES"
for t in "${LIST[@]}"; do
  i=$((i + 1)); cp "$TMP/t_$t.jpg" "$TMP/$(printf %03d "$i").jpg"
done
ffmpeg -v error -y -framerate 1 -i "$TMP/%03d.jpg" -vf "scale=480:-1,tile=4x$(( (N + 3) / 4 ))" -frames:v 1 "$OUT/sheet.jpg"

echo "$PWD/$OUT/sheet.jpg  (stills at $TIMES s; keys at $KEYT s)"
