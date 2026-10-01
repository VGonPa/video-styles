#!/usr/bin/env python3
"""Rebuild styles/<slug>/preview.gif from styles/<slug>/<slug>.mp4.

    python3 make_previews.py              # every style in the manifest
    python3 make_previews.py clay linocut # only these slugs

The GIF is 480 px wide at 6 fps with a 96-colour palette and ordered dithering; build.sh scripts
use the same filter so a preview looks the same whichever tool produced it.
"""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import sys

import manifest

STYLES_DIR = Path(__file__).resolve().parent / "styles"
GIF_FILTER = ("[0:v]fps=6,scale=480:-1:flags=lanczos,split[a][b];"
              "[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=4")


def make_preview(slug):
    folder = STYLES_DIR / slug
    clip, gif = folder / f"{slug}.mp4", folder / "preview.gif"
    if not clip.is_file():
        raise SystemExit(f"no clip for {slug}: {clip}")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(clip),
                    "-filter_complex", GIF_FILTER, "-loop", "0", str(gif)], check=True)
    return f"{slug}: {gif.stat().st_size // 1024} KiB"


def main(slugs):
    slugs = slugs or [style["slug"] for style in manifest.load()["styles"]]
    with ThreadPoolExecutor(max_workers=3) as pool:
        for line in pool.map(make_preview, slugs):
            print(line, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
