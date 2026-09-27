#!/usr/bin/env python3
"""Build the English catalog video from the style clips listed in the style manifest."""

from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

import manifest


ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "_catalog_build"
OUTPUT = ROOT / "catalog" / "catalog.mp4"
MANIFEST = manifest.load()
STYLES = [(s["slug"], s["name"], MANIFEST["families"][s["family"]]["title"].upper())
          for s in MANIFEST["styles"]]


def run(*args):
    subprocess.run(args, check=True)


def font(size, italic=False):
    roots = [
        Path("/System/Library/Fonts/Supplemental"),
        Path("/usr/share/fonts/truetype/dejavu"),
    ]
    names = ["Georgia Italic.ttf", "DejaVuSerif-Italic.ttf"] if italic else ["Georgia.ttf", "DejaVuSerif.ttf"]
    for root in roots:
        for name in names:
            if (root / name).exists():
                return ImageFont.truetype(root / name, size)
    return ImageFont.load_default(size=size)


def card(lines, destination):
    image = Image.new("RGB", (1920, 1080), (28, 26, 22))
    draw = ImageDraw.Draw(image)
    positions = [430, 515, 635]
    for i, line in enumerate(lines):
        size = 34 if i != 1 else 84
        face = font(size, italic=(i != 1))
        width = draw.textlength(line, font=face)
        draw.text(((1920 - width) / 2, positions[i]), line, font=face,
                  fill=(243, 238, 226) if i == 1 else (163, 155, 139))
    image.save(destination)


def encode_card(png, mp4, duration):
    run("ffmpeg", "-nostdin", "-v", "error", "-y", "-loop", "1", "-framerate", "30",
        "-i", str(png), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", str(duration), "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "18",
        "-r", "30", "-c:a", "aac", "-b:a", "192k", "-shortest", str(mp4))


def main():
    BUILD.mkdir(exist_ok=True)
    OUTPUT.parent.mkdir(exist_ok=True)
    entries = []
    for number, (slug, title, group) in enumerate(STYLES, 1):
        clip = ROOT / "styles" / slug / (slug + ".mp4")
        if not clip.is_file():
            sys.exit("Missing clip: " + str(clip))
        label = f"{number:02d}  ·  {title}"
        png = BUILD / f"card-{number:02d}.png"
        mp4 = BUILD / f"card-{number:02d}.mp4"
        card((group, label, ""), png)
        encode_card(png, mp4, 1.4)
        entries.extend((mp4, clip))
        print(f"{number:02d}/{len(STYLES)} {title}", flush=True)

    png = BUILD / "end.png"
    mp4 = BUILD / "end.mp4"
    card(("ANIMATION STYLE CATALOG", "irticalen", "English adaptation · Original by Yasin Özmen"), png)
    encode_card(png, mp4, 3)
    entries.append(mp4)

    list_file = BUILD / "list.txt"
    list_file.write_text("".join("file '" + str(path) + "'\n" for path in entries))
    master = BUILD / "master.mp4"
    run("ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i",
        str(list_file), "-c", "copy", str(master))
    run("ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(master),
        "-vf", "scale=1280:720,format=yuv420p", "-c:v", "libx264", "-crf", "27",
        "-preset", "medium", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
        str(OUTPUT))
    print(f"Created {OUTPUT} ({OUTPUT.stat().st_size / 1024 / 1024:.1f} MiB)")


if __name__ == "__main__":
    main()
