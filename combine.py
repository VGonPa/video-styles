#!/usr/bin/env python3
"""Assemble catalog/catalog.mp4: a title card before each style clip, then a closing card.

Clips run in manifest.shuffled() order. Each card names the style's family, the style and its
credits. Intermediate files go to _catalog_build/ (git-ignored). The reel is scaled to 720p and
compressed hard. It is not committed: catalog/*.mp4 is git-ignored and the reel is uploaded as
the catalog.mp4 asset of each GitHub release.
"""

from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont

import manifest

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "_catalog_build"
REEL = ROOT / "catalog" / "catalog.mp4"

CARD_SECONDS, END_SECONDS = 1.4, 3
BACKGROUND = (28, 26, 22)
# (top y, font size, italic, colour) for the kicker, title and footer lines of a card.
CARD_LINES = [(430, 34, True, (163, 155, 139)),
              (515, 84, False, (243, 238, 226)),
              (635, 34, True, (163, 155, 139))]
SERIF = {False: ["Georgia.ttf", "DejaVuSerif.ttf"], True: ["Georgia Italic.ttf", "DejaVuSerif-Italic.ttf"]}
FONT_DIRS = [Path("/System/Library/Fonts/Supplemental"), Path("/usr/share/fonts/truetype/dejavu")]


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *map(str, args)], check=True)


def serif(size, italic):
    candidates = [d / name for d in FONT_DIRS for name in SERIF[italic]]
    found = next((p for p in candidates if p.exists()), None)
    return ImageFont.truetype(found, size) if found else ImageFont.load_default(size=size)


def title_card(texts, seconds, stem):
    """Render a still card with three centred lines and encode it as a clip with silent audio."""
    png, clip = WORK / f"{stem}.png", WORK / f"{stem}.mp4"
    img = Image.new("RGB", (1920, 1080), BACKGROUND)
    pen = ImageDraw.Draw(img)
    for text, (y, size, italic, colour) in zip(texts, CARD_LINES):
        face = serif(size, italic)
        pen.text(((1920 - pen.textlength(text, font=face)) / 2, y), text, font=face, fill=colour)
    img.save(png)
    ffmpeg("-loop", 1, "-framerate", 30, "-i", png, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
           "-t", seconds, "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", 18, "-r", 30,
           "-c:a", "aac", "-b:a", "192k", "-shortest", clip)
    return clip


def main():
    data = manifest.load()
    styles = manifest.shuffled(data["styles"])
    missing = [s["slug"] for s in styles if not (ROOT / "styles" / s["slug"] / f"{s['slug']}.mp4").is_file()]
    if missing:
        raise SystemExit(f"missing clips: {', '.join(missing)}")
    WORK.mkdir(exist_ok=True)
    REEL.parent.mkdir(exist_ok=True)

    parts = []
    for i, s in enumerate(styles, 1):
        family = data["families"][s["family"]]["title"].upper()
        credits = " · ".join(manifest.credit_text(c) for c in s.get("credits", []))
        parts.append(title_card((family, s["name"], credits), CARD_SECONDS, f"card-{i:03d}"))
        parts.append(ROOT / "styles" / s["slug"] / f"{s['slug']}.mp4")
        print(f"{i:02d}/{len(styles)} {s['name']}", flush=True)
    parts.append(title_card(("ANIMATION STYLE CATALOG", f"{len(styles)} styles",
                             "Built on Yasin Özmen's original catalog"), END_SECONDS, "end"))

    playlist = WORK / "list.txt"
    playlist.write_text("".join(f"file '{p}'\n" for p in parts))
    joined = WORK / "master.mp4"
    ffmpeg("-f", "concat", "-safe", 0, "-i", playlist, "-c", "copy", joined)
    ffmpeg("-i", joined, "-vf", "scale=1280:720,format=yuv420p", "-c:v", "libx264", "-crf", 34,
           "-preset", "slow", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", REEL)
    print(f"Created {REEL} ({REEL.stat().st_size / 2**20:.1f} MiB)")


if __name__ == "__main__":
    main()
