# Style recipe template

Every style has a recipe at `skills/animating-in-video-styles/references/styles/<slug>.md`, the file the agent
skill reads before it adapts the style. The reader is an agent that has never seen the style: it has the
recipe, the original's contact sheet and the reference code, and must make a film on a new subject, at a new
length and possibly in 9:16, that a viewer would recognise as this style.

## How to write one

- **Look before you write.** Fetch the style into a scratch folder and render it:
  `python3 skills/animating-in-video-styles/scripts/fetch_style.py <slug> /tmp/<slug>-ref`, then
  `bash skills/animating-in-video-styles/scripts/contact_sheet.sh /tmp/<slug>-ref` and stills at 0.5, 1.5 and
  2.5 s (`node render.mjs stills 30 0 10 1 0.5,1.5,2.5` in that folder). Check the Signature against them.
- **Derive every fact from the current code** (`styles/<slug>/anim.html` and the scripts it loads, `audio.py`,
  `render.json`, `fonts.css`). The style's original brief or PR description, when you have them, explain the
  intent; where they disagree with the code, the code wins.
- **Name what the reader can find:** functions, constants, files (paths relative to the style folder, such as
  `js/lib.js` or `vendor/three.min.js`), with their parameters. Never line numbers. `check_catalog.py` verifies
  that every file and identifier in backticks in the Palette's "In code" column, the Film grammar's "In code"
  column, the Reuse map and the Typography and Sound sections exists in the style's code (font names and cue
  kinds included), that in `path` → `name` the file defines that name, that every call in backticks anywhere
  (`drawTitle()`) exists, and that every palette colour occurs in the code. Write `()` only after functions
  that exist; name a function you suggest the reader write without parentheses.
- **Write each colour as the code writes it:** `#rrggbb`, `0xrrggbb` or r,g,b numbers. When the code computes it
  (a GLSL `vec3(…)`, an `hsl()` template, a blend function), put that expression in backticks in the Colour
  column, exactly as written in the code, instead of a hex you worked out.
- **Explain why** a rule matters when it is not obvious, so the reader can apply it to scenes the demo never
  had ("no overshoot: Manim's `smooth` rate function is part of the look").
- **Stay concise:** about 100–200 lines, one fact per bullet, no praise or history. The catalog already holds
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
(title card, reveal, transition, sign-off) and which are one-off demo content.>

## Sound
<What audio.py synthesizes, which cue kinds trigger each sound and the fields and ranges they carry (d, v, f,
n…), the bed, the mix. Which cues a new scene should emit.>

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| <paper texture> | `anim.html` → `<name>` | <built once in window.ready> | as is |
| <a drawing primitive> | `<function>()` | `<function>(x, y, size, t0)`: <what the params do> | as is / adapt: <how> |
| <the demo subject> | `<scene functions>`, `<timeline>` | | replace |

## Adapting
- **New subject:** <what to keep, what to rewrite, common traps>
- **Length:** <how it stretches past 10 s: repeatable beats, what gets tiresome, rendering cost>
- **Other formats:** <9:16 and 1:1: what recomposes easily and what does not>

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
4. The Film grammar table matches the code's timeline; the Sound cues match what audio.py reads.
5. A cold reader could draw an object the demo never had, in this style, from Shapes, Palette and Texture
   alone, and could recompose it for 9:16 from Composition and Adapting.
6. It is concise, explains the why, names no line numbers and repeats nothing the catalog already holds.

The reviewer writes a report of required changes; the author fixes them; a new reviewer checks the next round.
