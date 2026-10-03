#!/usr/bin/env python3
"""Turn an image into a JavaScript constant holding a data: URI, so anim.html can draw it.

  python3 scripts/embed_image.py logo.png LOGO >> my-project/assets.js

anim.html then loads it with <script src="assets.js"></script> and decodes it inside window.ready:

  const logo = new Image(); logo.src = LOGO; await logo.decode();   // then ctx.drawImage(logo, ...)

Why: render.mjs opens anim.html from a file:// URL. An image loaded from a file path counts as cross-origin,
taints the canvas, and toDataURL() then throws "Tainted canvases may not be exported". A data: URI does not.
Supports PNG, JPEG, WebP, GIF and SVG. Needs Python 3.8+.
"""

import base64
import re
import sys
from pathlib import Path

TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp",
         ".gif": "image/gif", ".svg": "image/svg+xml"}


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    path, name = Path(sys.argv[1]), sys.argv[2]
    if not re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", name):
        sys.exit(f"{name!r} is not a valid JavaScript constant name")
    mime = TYPES.get(path.suffix.lower())
    if mime is None:
        sys.exit(f"unsupported image type {path.suffix!r}; use one of {', '.join(TYPES)}")
    try:
        data = base64.b64encode(path.read_bytes()).decode("ascii")
    except OSError as err:
        sys.exit(f"cannot read {path}: {err}")
    print(f"const {name} = 'data:{mime};base64,{data}';  // {path.name}")


if __name__ == "__main__":
    main()
