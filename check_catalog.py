#!/usr/bin/env python3
"""Check that every style is complete: metadata, clip specs, preview, and index pages.

Run after build_index.py. Add --media to also validate downloaded or rebuilt clips and GIFs.
"""

import json
import argparse
import subprocess
import sys

import manifest
import media

ROOT = manifest.ROOT
MANIFEST = manifest.load()
REQUIRED = {"number", "name", "feel", "best_for", "family", "use_cases"}
# Every style folder carries an unmodified copy of these shared scripts from tools/.
SHARED_SCRIPTS = ["render.mjs", "events.mjs"]
# The hand-drawn styles also share tools/common.js.
COMMON_JS_STYLES = {"whiteboard", "chalkboard", "blueprint", "single-line"}


def probe(clip):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt,color_range,sample_rate,channels"
         ":format=duration", "-of", "json", str(clip)],
        capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def check_clip(s, problems):
    clip = ROOT / "styles" / s["slug"] / f"{s['slug']}.mp4"
    if not clip.is_file():
        problems.append("missing clip")
        return
    info = probe(clip)
    video = [x for x in info["streams"] if x["codec_type"] == "video"]
    audio = [x for x in info["streams"] if x["codec_type"] == "audio"]
    duration = float(info["format"]["duration"])
    if not 8 <= duration <= 10.5:
        problems.append(f"duration {duration:.2f}s")
    if not video:
        problems.append("no video stream")
    else:
        v = video[0]
        expected = {"codec_name": "h264", "width": 1920, "height": 1080, "r_frame_rate": "30/1"}
        problems += [f"{k}={v.get(k)}" for k, want in expected.items() if v.get(k) != want]
        # The original clips are encoded full range from JPEG frames.
        if v.get("pix_fmt") != "yuvj420p" and v.get("color_range") != "pc":
            problems.append(f"range {v.get('pix_fmt')}/{v.get('color_range')} (want full range)")
    if not audio:
        problems.append("no audio stream")
    elif audio[0].get("codec_name") != "aac" or audio[0].get("sample_rate") != "48000" \
            or audio[0].get("channels") != 2:
        problems.append("audio is not AAC 48 kHz stereo")


def check_pages(s, problems):
    target = media.url(s["slug"], "preview")
    video = media.url(s["slug"], "video")
    pages = [ROOT / "README.md", ROOT / "categories" / "families" / f"{s['family']}.md"]
    pages += [ROOT / "categories" / "use-cases" / f"{u}.md" for u in s["use_cases"]]
    for page in pages:
        if not page.is_file() or target not in page.read_text() or video not in page.read_text():
            problems.append(f"not listed in {page.relative_to(ROOT)}")
    style_page = ROOT / "styles" / s["slug"] / "README.md"
    if not style_page.is_file() or f"# {s['name']}\n" not in style_page.read_text() \
            or target not in style_page.read_text() or video not in style_page.read_text():
        problems.append("missing or stale styles/<slug>/README.md")


def check_shared_scripts(s, problems):
    folder = ROOT / "styles" / s["slug"]
    names = SHARED_SCRIPTS + (["common.js"] if s["slug"] in COMMON_JS_STYLES else [])
    for name in names:
        copy = folder / name
        if not copy.is_file():
            problems.append(f"missing {name}")
        elif copy.read_bytes() != (ROOT / "tools" / name).read_bytes():
            problems.append(f"{name} differs from tools/{name}")


# The unlicensed original catalog; our code must not carry it forward. A tag rather than a
# commit hash, so it survives history rewrites (git filter-repo rewrites tags with the commits).
ORIGINAL = "original-catalog"


def require_original():
    """Fail loudly when the original is unreachable: without it the derived-code check is void."""
    found = subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"{ORIGINAL}^{{commit}}"],
                           capture_output=True, cwd=ROOT).returncode == 0
    if not found:
        sys.exit(f"tag {ORIGINAL} not found: run `git fetch --tags` (a full, non-shallow clone "
                 "is needed to check styles against the original catalog)")


def derived_lines(slug):
    """Lines (over 15 chars) of anim.html that also appear in the original catalog's version."""
    try:
        old = subprocess.run(["git", "show", f"{ORIGINAL}:styles/{slug}/anim.html"],
                             capture_output=True, text=True, check=True, cwd=ROOT).stdout
    except subprocess.CalledProcessError:
        return 0  # style not in the original
    orig = {l.strip() for l in old.splitlines() if len(l.strip()) > 15}
    cur = (ROOT / "styles" / slug / "anim.html").read_text().splitlines()
    return sum(1 for l in cur if l.strip() in orig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--media", action="store_true", help="also probe local clips and check GIFs")
    args = parser.parse_args()
    media.load()
    require_original()
    failed = False
    for s in MANIFEST["styles"]:
        problems = []
        missing = REQUIRED - s.keys()
        if missing:
            problems.append(f"meta.json missing {sorted(missing)}")
        if s.get("family") not in MANIFEST["families"]:
            problems.append(f"unknown family {s.get('family')}")
        problems += [f"unknown use case {u}" for u in s.get("use_cases", [])
                     if u not in MANIFEST["use_cases"]]
        if args.media and not (ROOT / "styles" / s["slug"] / "preview.gif").is_file():
            problems.append("missing preview.gif")
        check_shared_scripts(s, problems)
        if args.media:
            check_clip(s, problems)
        check_pages(s, problems)
        if (n := derived_lines(s["slug"])) > 5:
            problems.append(f"{n} lines shared with the original catalog")
        status = "ok" if not problems else "; ".join(problems)
        failed |= bool(problems)
        print(f"{s['number']:02d} {s['slug']:<20} {status}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
