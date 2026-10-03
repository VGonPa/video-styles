#!/usr/bin/env python3
"""Copy a style's reference film into a new project folder, ready to adapt.

  python3 scripts/fetch_style.py blueprint ./heat-pump-explainer
  python3 scripts/fetch_style.py clay ./teaser --repo ~/code/video-styles   # use a local clone
  python3 scripts/fetch_style.py clay ./teaser --ref v1.1.0                 # download another git ref

The project gets the style's anim.html, audio.py, build.sh, render.mjs, events.mjs, fonts and vendored
libraries (rendered media, meta.json and the generated README are skipped), plus _licenses/ with the
catalog's MIT license, the font license texts and the FONTS.md rows for this style. The folder name becomes
the output file name, so it may only use letters, digits, dots, dashes and underscores.

Where the code comes from, in order: --repo, $VIDEO_STYLES_REPO, a clone that contains this skill or the
current directory, then GitHub (a sparse git clone, or the source tarball when git is missing). --ref always
downloads from GitHub.

It also saves the catalog's preview GIF of the original clip to _reference/original-preview.gif and, when
ffmpeg is installed, a 4x4 contact sheet of it (_reference/original-sheet.jpg) to look at.
Needs Python 3.8+; network access only when no local clone is used.
"""

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SKIP = ("*.mp4", "*.gif", "*.wav", "README.md", "meta.json", "_frames", "out", "__pycache__", ".DS_Store")
# Older catalog versions ran audio.py through uv in four styles; plain python3 + NumPy is all it needs.
UV_LINE = re.compile(r"uv run --no-project --with numpy --index-url \S+ python audio\.py")


def catalog():
    return json.loads((SKILL / "assets" / "catalog.json").read_text(encoding="utf-8"))


def local_clone(slug, explicit):
    """The root of a local clone that has styles/<slug>, or None."""
    candidates = [Path(explicit).expanduser()] if explicit else []
    if os.environ.get("VIDEO_STYLES_REPO"):
        candidates.append(Path(os.environ["VIDEO_STYLES_REPO"]).expanduser())
    candidates += list(SKILL.parents) + [Path.cwd(), *Path.cwd().parents]
    for root in candidates:
        if (root / "styles" / slug / "anim.html").is_file():
            return root
    if explicit:
        sys.exit(f"{explicit} has no styles/{slug}/anim.html")
    return None


def from_git(repo, ref, slug, work):
    url = f"https://github.com/{repo}.git"
    root = work / "repo"
    subprocess.run(["git", "clone", "--quiet", "--depth", "1", "--filter=blob:none", "--sparse",
                    "--branch", ref, url, str(root)], check=True)
    # Cone mode always includes the files at the root (LICENSE, FONTS.md).
    subprocess.run(["git", "-C", str(root), "sparse-checkout", "set", f"styles/{slug}", "licenses"], check=True)
    if not (root / "styles" / slug / "anim.html").is_file():
        raise RuntimeError(f"styles/{slug} not found at {ref}")
    return root


def from_tarball(repo, ref, slug, work):
    url = f"https://github.com/{repo}/archive/{ref}.tar.gz"
    with urllib.request.urlopen(url, timeout=120) as response:
        data = io.BytesIO(response.read())
    root = work / "tar"
    with tarfile.open(fileobj=data, mode="r:gz") as tar:
        for member in tar.getmembers():
            parts = Path(member.name).parts
            if len(parts) < 2 or ".." in parts or not (member.isfile() or member.isdir()):
                continue
            inside = parts[1:]
            wanted = inside[:2] == ("styles", slug) or inside[0] == "licenses" or inside in (("LICENSE",), ("FONTS.md",))
            if wanted:
                member.name = str(Path(*inside))
                if hasattr(tarfile, "data_filter"):
                    tar.extract(member, root, filter="data")
                else:
                    tar.extract(member, root)
    if not (root / "styles" / slug / "anim.html").is_file():
        raise RuntimeError(f"styles/{slug} not found in {url}")
    return root


def licenses(root, slug, dest):
    out = dest / "_licenses"
    out.mkdir(exist_ok=True)
    if (root / "LICENSE").is_file():
        shutil.copy(root / "LICENSE", out / "LICENSE-video-styles.txt")
    for text in sorted((root / "licenses").glob("*.txt")):
        shutil.copy(text, out / text.name)
    fonts = root / "FONTS.md"
    if fonts.is_file():
        lines = fonts.read_text(encoding="utf-8").splitlines()
        header = [l for l in lines if l.startswith("| Family") or l.startswith("|---")][:2]
        rows = [l for l in lines if l.startswith("|") and f"(styles/{slug})" in l]
        if not rows and (dest / "fonts").is_dir():
            files = ", ".join(sorted(x.name for x in (dest / "fonts").iterdir()))
            rows = [f"| (not listed in FONTS.md: {files}) | see the font's own license | {slug} |"]
            print(f"note: FONTS.md has no row for {slug}; check the licenses of: {files}", file=sys.stderr)
        (out / "FONTS.md").write_text(
            f"# Fonts used by the {slug} style\n\nFrom the catalog's FONTS.md; license texts are in this folder.\n"
            "Links are relative to the catalog repository.\n\n" + "\n".join(header + rows) + "\n", encoding="utf-8")


def reference(style, dest):
    ref = dest / "_reference"
    ref.mkdir(exist_ok=True)
    gif = ref / "original-preview.gif"
    try:
        with urllib.request.urlopen(style["preview"], timeout=60) as response:
            gif.write_bytes(response.read())
    except OSError as err:
        print(f"note: could not download the preview GIF ({err}); open {style['preview']}", file=sys.stderr)
        return
    if not shutil.which("ffmpeg"):
        print("note: ffmpeg not found, so no _reference/original-sheet.jpg; view original-preview.gif instead",
              file=sys.stderr)
        return
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(gif), "-vf", "fps=1.6,scale=480:-1,tile=4x4",
                    "-frames:v", "1", str(ref / "original-sheet.jpg")], check=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="style slug, e.g. blueprint (find one with scripts/find_style.py)")
    parser.add_argument("dest", help="new project folder; its name becomes the output file name")
    parser.add_argument("--repo", help="path to a local clone of the catalog repository")
    parser.add_argument("--ref", help="git branch or tag to download from GitHub (default: the catalog's ref)")
    parser.add_argument("--no-reference", action="store_true", help="skip downloading the original preview GIF")
    args = parser.parse_args()

    cat = catalog()
    style = next((s for s in cat["styles"] if s["slug"] == args.slug), None)
    if style is None:
        sys.exit(f"unknown style {args.slug!r}; search with: python3 scripts/find_style.py <words>")
    dest = Path(args.dest).expanduser().resolve()
    if not re.fullmatch(r"[A-Za-z0-9._-]+", dest.name):
        suggestion = re.sub(r"[^A-Za-z0-9._-]+", "-", dest.name).strip("-") or "my-video"
        sys.exit(f"folder name {dest.name!r} would break build.sh; use letters, digits, '.', '-' and '_', "
                 f"e.g. {suggestion}")
    if dest == SKILL or SKILL in dest.parents:
        sys.exit(f"{dest} is inside the skill folder; create the project in the user's working directory")
    if dest.exists() and any(dest.iterdir()):
        sys.exit(f"{dest} already exists and is not empty; choose a new folder")

    with tempfile.TemporaryDirectory() as tmp:
        root = None if args.ref else local_clone(args.slug, args.repo)
        origin = str(root) if root else None
        if root is None:
            ref = args.ref or cat["ref"]
            try:
                if not shutil.which("git"):
                    raise RuntimeError("git not installed")
                root = from_git(cat["repository"], ref, args.slug, Path(tmp))
            except (RuntimeError, subprocess.CalledProcessError) as err:
                print(f"note: sparse git clone failed ({err}); downloading the tarball", file=sys.stderr)
                try:
                    root = from_tarball(cat["repository"], ref, args.slug, Path(tmp))
                except (OSError, RuntimeError, tarfile.TarError) as err2:
                    sys.exit(f"could not download styles/{args.slug} from {cat['repository']}@{ref}: {err2}\n"
                             "No network (e.g. a sandbox)? Ask for network access, or pass --repo <path to a clone>.")
            origin = f"github.com/{cat['repository']}@{ref}"
        shutil.copytree(root / "styles" / args.slug, dest, ignore=shutil.ignore_patterns(*SKIP), dirs_exist_ok=True)
        licenses(root, args.slug, dest)

    build = dest / "build.sh"
    if build.exists():
        build.write_text(UV_LINE.sub("python3 audio.py", build.read_text()))
        build.chmod(build.stat().st_mode | 0o111)
    if not args.no_reference:
        reference(style, dest)
    print(f"{style['name']} ({args.slug}) copied from {origin} to {dest}")
    if style["recipe"]:
        print(f"next: read references/styles/{args.slug}.md, look at {dest.name}/_reference/, then adapt anim.html")
    else:
        print(f"next: this style has no recipe yet; look at {dest.name}/_reference/ and follow the fallback in "
              "SKILL.md step 3 before adapting anim.html")


if __name__ == "__main__":
    main()
