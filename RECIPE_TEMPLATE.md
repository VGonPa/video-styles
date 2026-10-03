# Style recipe template

Each style's recipe lives at `skills/animating-in-video-styles/references/styles/<slug>.md`, the file the agent
skill reads before it adapts the style. The reader is an agent that has never seen the style: it has the
recipe, the original's contact sheet and the reference code, and must make a film on a new subject, at a new
length and possibly in 9:16, that a viewer would recognise as this style.

## How to write one

- **Look before you write.** Fetch the style into a scratch folder and render it:
  `python3 skills/animating-in-video-styles/scripts/fetch_style.py <slug> /tmp/<slug>-ref`, then
  `bash skills/animating-in-video-styles/scripts/contact_sheet.sh /tmp/<slug>-ref` and stills at 0.5, 1.5 and
  2.5 s (`node render.mjs stills 30 0 10 1 0.5,1.5,2.5` in that folder). Check the Signature against them.
- **Render the formats you advise on.** In a scratch copy, set the canvas and `W`/`H` to 1080 × 1920, apply
  your 9:16 values and render stills of every shot, each at the moment its characters and props reach their
  widest position, plus the end card; then go through every Signature item in every shot of every format and
  confirm each is visible and whole (a sun hidden behind a city or a cropped crown fails), check that nothing
  defining the look leaves the frame, nothing is left unpainted, no flat or empty band larger than about a fifth
  of the frame remains (even if painted in one tone); the 9:16 bottom caption band (y 1440–1920) may stay
  low in detail, but carries the scene's ground and texture rather than a flat fill, because without captions it
  shows, and key text stays out of the bands in
  review.md. Re-render once with a stand-in subject of another silhouette (taller, or not a vehicle) and say
  which values depend on the demo subject's shape. Give only values you rendered; if you could not test one, say so. Untested format advice was the
  most common serious error in the pilot recipes.
- **Derive every fact from the current code** (`styles/<slug>/anim.html` and the scripts it loads, `audio.py`,
  `render.json`, `fonts.css`). The style's original brief or PR description, when you have them, explain the
  intent; where they disagree with the code, the code wins.
- **Name what the reader can find:** functions with their parameters, constants, fonts and files (paths relative
  to the style folder, such as `js/lib.js` or `vendor/three.min.js`); never line numbers. Backticks mean "this is
  in the style's code or its vendored library", and `()` marks a function that exists. Write everything else in
  plain words: a value without a name in the code (the third value of an array row), or a function you suggest
  the reader create (a drawLogo function); to give its code, use a fenced code block, which the
  checker treats as code to write and skips. In Sound, backtick only cue kinds and fields audio.py reads and names
  audio.py itself defines; leave out cues that anim.html emits but audio.py ignores (they are silent).
- **`check_catalog.py` catches slips, not wrong facts.** It fails a recipe when a backticked file or name
  (outside Boundaries and Technical notes) is not in the code, when in `path` → `name` the file does not define
  the name, when a palette colour does not occur in the code, or when Boundaries names a style the catalog
  lacks. It cannot tell whether easing, timing or sound facts are right; the reviewer checks those.
- **Write each colour as the code writes it:** `#rrggbb`, `0xrrggbb` or r,g,b numbers. When the code computes it
  (a GLSL `vec3(…)`, an `hsl()` template, a blend function), put that expression in backticks in the Colour
  column, exactly as written in the code, instead of a hex you worked out.
- **Explain why** a rule matters when it is not obvious, so the reader can apply it to scenes the demo never
  had ("no overshoot: Manim's `smooth` rate function is part of the look").
- **Stay concise:** about 150–250 lines (rendered format values, the short-film plan and the tables earn the
  upper end; prose does not), one fact per bullet, no praise or history. The catalog already holds
  family, use cases, feel, "best for" and credits; do not repeat them.
- **Keep every heading below, in this order** (`check_catalog.py` enforces it). The Palette, Film grammar and
  Reuse map tables are required, with the headers shown; elsewhere write "None." rather than dropping a
  section. English, in the repository's plain style.

## Template

```markdown
# <Name> (`<slug>`)

<What the style is, what it evokes, the tradition or creator it draws on, its mood. Two to four sentences.>

**Reference film:** <the demo clip's subject in one sentence> · `styles/<slug>/`

## Signature
<Three to five bullets: what must be on screen within the first 3 seconds for the style to read. A reviewer
checks these first.>

## Palette
| Role | Colour | In code |
|---|---|---|
| <background, ink, accent…> | `#rrggbb` | `<constant or function>` |

<One or two bullets on how colour is applied: flat fills, limited inks, gradients, off-register, glow.>

## Typography and copy
<Families and files in fonts/ and their roles; case, tracking, how text enters and leaves; glyph coverage
limits. Copy: voice and register (deadpan, shouty, technical labels…), words per card or caption, the maximum
characters per line at each size used, and what to do with longer copy.>

## Texture and finish
<Paper, grain, halftone, scanlines, bloom, vignette, gate weave… how each is made (precomputed once, refreshed
at N fps) and which function or block makes it.>

## Shapes, line and figures
<Line weight and quality, outlines, shading, perspective, how objects and people are built. What a new object
must look like to belong.>

## Composition and camera
<Framing and grid, where the focus sits, symmetry, margins, depth layers and parallax, a 2D or 3D camera and
its moves. What changes for 9:16 and 1:1.>

## Motion
<Easing (named functions), timing, frame-rate stepping, entrances and exits, secondary motion. What the style
never does.>

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| <0–0.8> | <title types on> | `<T key or function>` |

<How a scene opens, holds and hands over to the next; typical beat length; which beats are reusable patterns
(title card, reveal, transition, sign-off) and which are one-off demo content. The moments a reviewer must see
in full (the punchline held, the reveal, the end card), with their demo times, for `contact_sheet.sh` `KEYS`.>

## Sound
<What audio.py synthesizes, which cue kinds trigger each sound and the fields and ranges they carry (d, v, f,
n…), the bed, the mix. Which cues a new scene should emit, and which ones audio.py looks up by name and cannot
run without (often the cue it times the music from). Which music and bed parts audio.py writes at fixed times
rather than from cues, and where. The field values or cue counts beyond which audio.py breaks (a pan formula
that passes ±1 gives NaN and a silent track).>

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| <paper texture> | `anim.html` → `<name>` | <built once in window.ready> | as is |
| <a drawing primitive> | `<function>()` | `<function>(x, y, size, t0)`: <what the params do> | as is / adapt: <how> |
| <the demo subject> | `<scene functions>`, `<timeline>` | | replace |

## Adapting
- **Style vs demo plot:** <what is always the style (kit, grade, finish, signature moves) and which demo events
  are plot a new film replaces; what can count as the transformation in a new story>
- **New subject:** <what to keep, what to rewrite, common traps>
- **Length:** <how it stretches past 10 s: repeatable beats, what gets tiresome, rendering cost, and what in
  audio.py must be re-timed>
- **Shorter:** <how it compresses below the demo's length: between about 6 s and the demo, which holds and how
  much copy shorten within the style's minimums; for 3–6 s, cut whole beats rather than compressing each; which to keep, which to
  drop first, the shortest opening that still shows the signature (counted after the fade-in, whose length you give), what a
  title card costs (its final hold counted from the moment everything on it has settled), and any helper that
  must be removed with a dropped scene; a tested plan for 4 s if you can>
- **Other formats:** <9:16 and 1:1: what recomposes easily and what does not; rendered values for the subject
  staying on screen to the end, not only for the demo's end card>

## Boundaries
- **Distinct from:** <neighbouring styles by slug, and the difference>
- **Poor fit:** <content this style handles badly, and the style (by slug) to use instead>
- **Do not:** <copying limits for inspired-by styles, cultural notes, anything the look forbids>

## Technical notes
<render.json flags, WebGL or GPU needs, vendored libraries, approximate render time for 10 s, determinism traps,
files besides anim.html, and frame sizes hard-coded outside `W`/`H` (1920, 1080, 960, 540) that a 9:16 version
must change.>
```

## Reviewing a recipe

Someone other than the author reviews every recipe. Check:

1. The title line and every heading, in order; `python3 check_catalog.py` passes for the style.
2. Every identifier, file and font named exists (grep the code and `fonts/`); every colour matches the code.
3. The Signature items are visible in the original's first 3 seconds (`_reference/original-sheet.jpg` and
   stills), and nothing visible there that defines the look is missing.
4. The Film grammar table matches the code's timeline; the Sound cues match what audio.py reads, and the recipe
   says which sounds are timed for the demo and which cues audio.py cannot run without.
5. A cold reader could draw an object the demo never had, in this style, from Shapes, Palette and Texture
   alone, and could recompose it for 9:16 from Composition and Adapting: render the recipe's 9:16 values in a
   scratch copy and look (sun, title, characters in frame; nothing unpainted; text clear of the bands).
6. It is concise, explains the why, names no line numbers and repeats nothing the catalog already holds.

The reviewer writes a report of required changes; the author fixes them; a new reviewer checks the next round.
