---
name: animating-in-video-styles
description: Makes short animated videos in a chosen visual style. Use it whenever someone wants to create, animate or render a video or motion graphic with a particular look, asks which animation style suits a topic or audience, or wants to recreate or adapt a style from the VGonPa/video-styles catalog for their own content, even without naming the catalog. Covers explainers, product teasers, social clips, title sequences and data stories in over a hundred ready-made styles, such as blueprint, chalkboard, ukiyo-e, synthwave, clay stop-motion, pixel art, manga, Manim-style math, newspaper comic strips, noir comics or inflated 3D icons, and styles inspired by Kurzgesagt, 3Blue1Brown, Saul Bass, Wes Anderson or Van Gogh. Films are drawn on an HTML canvas and rendered to MP4 with synthesized sound. Not for editing existing footage or live-action video.
license: MIT
compatibility: Needs bash (macOS or Linux; WSL on Windows), Node.js 18+ with Playwright and Chromium, ffmpeg, and Python 3 with NumPy. Fetching a style needs git or HTTPS access to GitHub unless you work inside a clone of VGonPa/video-styles. GPU flags target macOS; elsewhere WebGL styles render in software, more slowly.
metadata:
  repository: https://github.com/VGonPa/video-styles
  version: "1.0"
---

# Animating in video styles

Each style in the catalog is a working short film: an `anim.html` that draws every frame on a canvas as a
pure function of time, an `audio.py` that synthesizes the soundtrack from cues the film emits, and a
`build.sh` that renders and encodes it. You make a new video by starting from the style's film and replacing
its subject with the user's while keeping what makes the style recognisable. The style's recipe says what
that is and which parts of the code carry it, so the work is adaptation, not invention from scratch.

`<skill>` below is this skill's folder. Run its scripts by path from the user's working directory
(`python3 <skill>/scripts/find_style.py …`), so projects are created there and never inside the skill folder.

## Workflow

### 1. Pin down the brief
Subject and message, audience, length, aspect ratio, on-screen language, brand assets (logos, product
shots), sound. Default to 16:9 at 1920 × 1080, 10–20 s, English text and synthesized sound, and ask only for
what you cannot default. If the user only wants advice on which style to use, stop after step 2.

### 2. Choose the style
- The user named a style or a creator: resolve it with `python3 <skill>/scripts/find_style.py <words>`.
- Otherwise filter by use case, family or one to three content words (not a sentence), e.g.
  `find_style.py --use-case explainer --family technical` or `find_style.py kids science`.
  Use cases: explainer, tutorial, product, social, story, data, news, titles. `--list` shows families.
- For a broad look across everything, or when the matches look wrong, read `<skill>/references/catalog.md`
  (one line per style, grouped by family).
- Offer two or three candidates, one line each on why they fit, with their preview GIF links
  (`find_style.py --json <slug>` prints them). Say when a candidate is marked WebGL: it renders slowly
  without a GPU.

### 3. Read the recipe
Read `<skill>/references/styles/<slug>.md` in full before touching code. It gives the 3-second signature, palette,
type and copy, texture, composition, motion, the film's beat structure, sound, a reuse map of the code with
call signatures, how to adapt length and format, and what the style must not become.

If the style is marked "no recipe yet", build that knowledge yourself before editing, and tell the user you
did: from the code and the original's contact sheet (step 4), note what makes the first 3 seconds
recognisable, the palette constants, the fonts, the texture and finish functions, the easing functions, the
timeline, and the cue kinds audio.py handles.

### 4. Set up the project
1. `bash <skill>/scripts/check_env.sh` checks the tools; install what it reports missing.
2. `python3 <skill>/scripts/fetch_style.py <slug> <project-dir>` copies the style's film into a new folder,
   named with letters, digits and dashes (the output file takes that name). Inside a clone of the catalog, use
   `projects/<name>` (git-ignored), not a folder under `styles/`. No network, as in some sandboxes? Ask for
   network access, or pass `--repo <path to a clone>`. `--ref <tag>` downloads a given version;
   `_reference/SOURCE.txt` records where the code came from.
3. Before editing, render the original at full resolution: `KEYS=<times> bash <skill>/scripts/contact_sheet.sh
   <project-dir> 10 16 _reference/original`, with `KEYS` set to the moments the recipe's Film grammar names (the
   default stills can miss a punchline or a reveal). This render, not the catalog's preview GIF, is the reference. Look at `_reference/original/` (sheet and two key frames) now, so you know what
   the result should feel like; `_reference/original-sheet.jpg` comes from the catalog's small GIF.

Work only inside the project folder. Read `<skill>/references/contract.md` before editing: it explains the
anim.html contract, where duration and size live, how to use the user's images, and how sound is wired.

### 5. Plan the film
Write a beat sheet: time ranges, what is on screen, what moves, what sounds. Put the style's signature in the
first 3 seconds, keep one focus at a time, include at least one transformation or scene change, and end on a
settle, fade or held final pose. Borrow the recipe's film grammar: how its scenes open, hold and hand over.
Keep what the recipe calls the style and replace the demo's plot. Most demos run 10 s. A little shorter (about 6 s up
to the demo), keep the scenes and shorten holds and copy within the recipe's minimums. Under about 6 s, cut
whole scenes rather than compressing every beat: keep the signature opening (about
1–1.5 s), one or two events with a transformation (a change of state such as lights coming on, nightfall or
an arrival counts), a held final state of at least 0.8 s (counted from when nothing is still sweeping, glinting or arriving) and a
fade of at least 0.25 s. The recipe's "Shorter"
note says which scenes go first.

### 6. Adapt the code
Follow the recipe's reuse map: keep the kit (textures, palette, primitives, finish, instruments), replace the
demo's scenes, timeline and copy. Keep frames a pure function of `t`, with seeded randomness only, because
frames render out of order in parallel. Change length in all three places listed in contract.md, or the clip
is silently cut short. For 9:16 or 1:1, change the canvas size and recompose with the recipe's composition
notes. Embed the user's images as data URIs (`<skill>/scripts/embed_image.py`); a file path breaks the render.

### 7. Score it
Emit cues from the new scenes with the cue kinds and fields audio.py already handles; extend audio.py only
for sounds the style lacks, in the same synthesized character. Re-time any music or bed that audio.py writes
at fixed times for the original (see "Duration" in contract.md), or it stops early or ends at the wrong time.
Then run `node events.mjs && python3 audio.py` in the project folder: it takes seconds and catches a crash (a
missing field, a cue looked up by name) or a `nan` peak, while build.sh reaches audio.py only after rendering
every frame, and deletes them when it fails. A cue kind audio.py has no handler for is silently dropped in most
styles (some crash on it instead, which this run catches), so check every kind you emit against audio.py.

### 8. Look, critique, fix
Run `bash <skill>/scripts/contact_sheet.sh <project-dir> <seconds>` and look at `_review/sheet.jpg` and the
key frames next to the original's in `_reference/original/`; add `KEYS=<t1>,<t2>` for full-size stills
of the beats the film exists for (the punchline, the reveal), each transition at its peak (a flash, wipe or
iris) and the held final state (e.g. `KEYS=1.4,2.9,3.6` in a 4 s film); `_review/keys.txt` maps each key file to
its time. Critique against the recipe's signature and
`<skill>/references/review.md`, fix, and render again. Do at least two passes: first renders almost always have
clipped text, crowded frames or a weak ending. If you cannot view images, ask the user to compare the sheets
and describe what they see; do not skip the review.

### 9. Build and deliver
Run `DUR=<seconds> ./build.sh` in the project folder (it takes minutes; use a long timeout or run it in the
background). It writes `<folder>.mp4` and `preview.gif` and prints an ffprobe summary: check the duration and
the audio stream. Report the file paths, what the film shows and any known defects. If the user shares the
project's source, keep `_licenses/`, `THIRD_PARTY_NOTICES.md` and the license files in `vendor/` with it.

## Guardrails
- Styles inspired by a creator take the visual language and tone only: never their characters, mascots,
  logos, lettering or signature jokes, and do not imply endorsement.
- Cultural styles: respect the tradition, use no sacred or religious iconography as decoration, and invent
  no script that pretends to be a real language.
- Show real brands, logos, products or people only when the user owns or supplies them.

## Files
- `scripts/find_style.py`: search the catalog. `scripts/fetch_style.py`: start a project from a style.
  `scripts/contact_sheet.sh`: stills to review. `scripts/embed_image.py`: images as data URIs.
  `scripts/check_env.sh`: dependency check.
- `references/catalog.md`: every style on one page. `references/styles/<slug>.md`: one recipe per style.
- `references/contract.md`: how a film is built. `references/review.md`: what to check in the frames.
- `assets/catalog.json`: machine-readable catalog used by the scripts (generated; do not edit).
