#!/usr/bin/env python3
"""Download all release assets or just selected styles, verifying size and SHA-256."""

import argparse
import hashlib
import os
from pathlib import Path
import tempfile
from urllib.request import Request, urlopen

import manifest
import media


def matches(path, item):
    if path.stat().st_size != item["size"]:
        return False
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest() == item["sha256"]


def fetch(slug, kind):
    item = media.asset(slug, kind)
    folder = manifest.ROOT / "styles" / slug
    target = folder / (slug + ".mp4" if kind == "video" else "preview.gif")
    if target.exists():
        if matches(target, item):
            return f"{slug} {kind}: already verified"
        raise ValueError(f"{target} differs from the release; move it aside before downloading")
    folder.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=folder, delete=False) as output:
            temporary = Path(output.name)
            request = Request(media.url(slug, kind), headers={"User-Agent": "video-styles-media"})
            with urlopen(request, timeout=120) as response:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
        if not matches(temporary, item):
            raise ValueError(f"{slug} {kind}: release download failed its size/SHA-256 check")
        # A concurrent rebuild/download must not be overwritten.
        os.link(temporary, target)
        return f"{slug} {kind}: downloaded and verified"
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slugs", nargs="*", help="style slugs; omit to download all styles")
    parser.add_argument("--kind", choices=("all", "video", "preview"), default="all")
    args = parser.parse_args()
    available = media.load()["styles"]
    unknown = set(args.slugs) - set(available)
    if unknown:
        parser.error("unknown styles: " + ", ".join(sorted(unknown)))
    kinds = ("video", "preview") if args.kind == "all" else (args.kind,)
    for slug in dict.fromkeys(args.slugs or available):
        for kind in kinds:
            print(fetch(slug, kind), flush=True)


if __name__ == "__main__":
    main()
