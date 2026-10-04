# Third-party notices

This project is released under the [MIT License](LICENSE). The components below are not
ours. They are redistributed or adapted under their own licenses, which still apply to them.
Each style that uses one also lists it in its own `THIRD_PARTY_NOTICES.md`.

## Code

### three.js r159 — MIT License

Copyright © 2010-2023 three.js authors. Vendored as `vendor/three.min.js`, with the full
license text in `vendor/LICENSE-three.txt`, in:
[blob-sim](styles/blob-sim/THIRD_PARTY_NOTICES.md),
[cel-shaded-3d](styles/cel-shaded-3d/THIRD_PARTY_NOTICES.md),
[feature-animation-3d](styles/feature-animation-3d/THIRD_PARTY_NOTICES.md),
[inflated-3d](styles/inflated-3d/THIRD_PARTY_NOTICES.md),
[low-poly](styles/low-poly/THIRD_PARTY_NOTICES.md),
[mascot-beat-reel](styles/mascot-beat-reel/THIRD_PARTY_NOTICES.md),
[origami](styles/origami/THIRD_PARTY_NOTICES.md),
[technical-cutaway](styles/technical-cutaway/THIRD_PARTY_NOTICES.md),
[voxel](styles/voxel/THIRD_PARTY_NOTICES.md).

### Rough.js 4.6.6 — MIT License

Copyright (c) 2019 Preet Shihn. Vendored as
[`styles/watercolor-memory/vendor/rough.min.js`](styles/watercolor-memory/vendor/rough.min.js),
with the full license text in `vendor/LICENSE-roughjs.txt`
([notice](styles/watercolor-memory/THIRD_PARTY_NOTICES.md)).

### "Memory Fading Into Watercolor" by Techartist — MIT License

Copyright (c) 2026 Techartist, <https://github.com/iamtechartist/memory-fading-into-watercolor>.
The pigment-transport simulation and the edge-pooling, back-run and granulation pigment model
in [`styles/watercolor-memory/anim.html`](styles/watercolor-memory/anim.html) are adapted from it.
The full license text is reproduced in
[styles/watercolor-memory/THIRD_PARTY_NOTICES.md](styles/watercolor-memory/THIRD_PARTY_NOTICES.md).

### Hershey fonts — public domain

The single-stroke tube paths in [`styles/neon-sign/glyphs.js`](styles/neon-sign/glyphs.js)
were exported from the Hershey fonts (created by Dr. A. V. Hershey at the U.S. National
Bureau of Standards) as packaged by the `Hershey-Fonts` Python package (MIT)
([notice](styles/neon-sign/THIRD_PARTY_NOTICES.md)).

## Fonts

All webfonts under `styles/*/fonts/` are third-party fonts: Google Fonts families under the
SIL Open Font License 1.1 or the Apache License 2.0, and the KaTeX fonts under the MIT
License. [FONTS.md](FONTS.md) lists each family, its license, its copyright notice and the
styles that use it; the license texts are in [licenses/](licenses/).

## Tools used to make the clips (not redistributed)

[Playwright](https://playwright.dev) and headless Chromium render the frames, and
[FFmpeg](https://ffmpeg.org) encodes the video, audio and GIF previews. The scripts call them;
none of their code is included in this repository.
