#!/usr/bin/env python3
"""Generate English animated GIF previews from the MP4 clips (all styles with a meta.json, or the slugs given as arguments)."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import sys

import manifest

ROOT = Path(__file__).resolve().parent / 'styles'


def render(folder):
    clip = folder / (folder.name + '.mp4')
    preview = folder / 'preview.gif'
    if not clip.is_file():
        raise FileNotFoundError(clip)
    subprocess.run([
        'ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(clip),
        '-filter_complex', '[0:v]fps=6,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=4',
        '-loop', '0', str(preview),
    ], check=True)
    print(folder.name, round(preview.stat().st_size / 1024), 'KiB', flush=True)


if __name__ == '__main__':
    slugs = sys.argv[1:] or [s['slug'] for s in manifest.load()['styles']]
    folders = [ROOT / slug for slug in slugs]
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(render, folders))
