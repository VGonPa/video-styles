# Paper Cutout (`paper-cutout`)

A toy-theatre diorama of cut card: flat matte paper pieces in layered cards, each casting a soft shadow on the one
behind, lit by one warm or cool light, with a jointed paper puppet held by brass split pins. Motion is smooth and
gentle, like a motion-control camera over a real model, not stop-motion. Storybook, quiet, cosy.

**Reference film:** a paper fox trots through a winter valley at dusk; a night card is pulled across the sky, the
moon rises, stars come down on threads, the fox curls up under a pine, cabin windows light and a torn title card is
lowered on strings · `styles/paper-cutout/`

## Signature
- Landscape cards stacked in depth (mountains, hill, forest, near bank, foreground wings), each a flat silhouette
  with a wavy, zigzag or scalloped top, rising from below with a small overshoot (0.15–1.59 s, `riseOffset`) and
  throwing a blurred dark copy of itself onto the card behind (`bakeSheet()`, drawn offset in `paint()`).
- Every piece is matte paper: a flat fill, a 2 px paler lip on its upper-left cut edge, a faint fibre grain
  (`cutShape()`, `GRAIN`); details are separate pieces glued on with their own small shadow (`gluedShadow()`).
- A paper sky: five scalloped dusk bands (`buildDusk()`) and a cut sun of curled petals, later covered by a navy card
  slid in from the side (`buildNight()`); snow-capped pines of three tiers (`pine()`) at four sizes on three cards,
  largest in front, and two giant pines cut off by the frame edges as theatre wings (`buildWings()`).
- One light: every live cast (card shades, `place()` casts, the fox, the title words, snow) follows one light vector
  that swings as dusk turns to night, and a multiply tint plus vignette warms or cools everything (`paint()`). The
  lip and glued shadows are baked for a fixed upper-left light; kept at 2–5 px they read as paper relief.

## Palette
| Role | Colour | In code |
|---|---|---|
| Dusk bands, top to bottom | `#6f67a6`, `#a476a4`, `#dc8f8e`, `#f2b48c`, `#f8d3a4` | `buildDusk()` |
| Night card; its lower band | `#26306c`; `#34428a` | `buildNight()` |
| Mountains; snow grounds far to near (hill, forest, bank, wings strip) | `#8583bb`; `#d4d9ea`, `#e6e9f2`, `#f4f1ea`, `#e9e6e0` | `buildMountains()`, `buildHill()`, `buildForest()`, `buildBank()`, `buildWings()` |
| Snow caps and roof; falling snow; trunks; twigs | `#f3efe6`; `#fbf8f1`; `#4a3530`; `#6a4a3e` | `SNOWPAPER`; `ART.dot`, `ART.flake`; `BARK`; `buildBank()` |
| Pine greens: hill; forest; tall pine; wings | `#3d6560`, `#35605a`; `#24504a`, `#2c5d52`; `#214a44`; `#173631`, `#1b3d37` | `pine()` calls in the card builders |
| Cabin wall, roof, chimney, door, window bars | `#a8553a`, `#5b3a38`, `#6b4a42`, `#4a2d27`, `#3b2622` | `buildHill()` |
| Lamp behind the window holes, off to lit | `blendHex('#2a2436', '#ffcf73', lampLevel(t, j))` | `paint()` |
| Fox fur, socks and paws, bib and tail tip; far limbs | `#d9642a`, `#3b2620`, `#f6ecdc`; `tint(FUR, 0.7)` | `FUR`, `SOCK`, `BIB`; `foxLeg()` |
| Nose; eye; glint; brass pins | `#221512`; `#1d1210`; `#fff5e0`; `#b88f3e`, `#f3dc9a` | `paintFox()`, `brad()` |
| Sun petals, disc; moon, crescent; stars, their dull back | `#e9713f`, `#f5a24a`; `#f3e5c2`, `#e6d4ab`; `#f6d98a`, `#5a4020` | `buildSkyPieces()`, `hangingStars()` |
| Title card; backing and title; kicker and rule; flakes | `#f3ecdc`; `#2b2d5c`; `#c24f39`; `#8e9fc9` | `buildTitle()` |
| Shadows: glued pieces; card silhouettes | `rgba(16,10,18,${alpha})`; `#0d0a14` | `gluedShadow()`; `bakeSheet()` |
| Multiply tint; vignette edge (dusk to night) | `blendHex('#fff1e2', '#aab4e2', nightfall)`; `blendHex('#c9a98e', '#8e86a8', nightfall)` | `paint()` |
| Lamp halo (screen); smoke; fade | `rgba(255,186,90,${0.5 * glow})`; `#f1eef4`; `rgba(12,10,20,${1 - shown})` | `paint()`, `chimneySmoke()` |

- Flat fills only: shading comes from the lip, grain, shadows and global tint. Nearer layers are larger, with darker
  greens and paler snow. The night tint dulls warm colours (the fox reads brown): give a warm subject a lighter fill.

## Typography and copy
- Fraunces only (`fonts/*.woff2`, `fonts.css`: Latin and Latin Extended subsets), via `SERIF`. Kicker 700 at 58 px,
  tracking 5 px, `#c24f39`; title 900 at 124 px, tracking −1 px, `#2b2d5c`; centred, title case (`buildTitle()`).
- Text lives only on the hanging card (the wider line + 190 px by 300; a third line needs `TITLE.h`, the rule's
  y 116 and the flakes moved). Each word is a piece drawn live with `fillText`, popping 0.16 s after the last with
  `backOut(q, 2.2)`, lifting 16 px, untilting from ±0.1 rad, shadowed along the light, white-edged (`paintTitle()`).
- Copy: a short kicker ("A Fox's") over a two-word title, at most three words a line. 60 px a lowercase letter, 83 a
  capital at 124 px; 32 and 43 at 58 px. 16:9 lines stay under 890 px (about 14 title or 27 kicker characters) to
  clear the moon at x 1541; the 9:16 and 1:1 sizes fit "Winter Night" (12): scale longer copy down in proportion.
- Latin and Latin Extended only. Add every new string to the `document.fonts.load` samples in `window.ready`:
  `buildTitle()` measures at load, and "Śnieżna Łąka" left out was spaced from fallback metrics (tested).

## Texture and finish
- `GRAIN`: one 512 px tile built at load (value and white noise at most about 5 % alpha, 1400 fibre strokes), filled
  over every piece in `cutShape()` through `grainOn()`. Baked into the cards, so it never boils.
- Lip: `cutShape(c, shape, colour, lipGain = 1.18)` fills the shape, then the shape minus a copy shifted `LIP_SHIFT`
  (1.8, 2.4 px) paler (1.25 fox haunch, 1.06 sky, 1.05 snow, 1 night card). `gluedShadow(c, shape, dx, dy, blur = 6,
  alpha = 0.35)` goes before the piece, offsets (2–4, 2–5) px; fox parts (1.5, 2.5), blur 4.
- Card shadow: `bakeSheet()` keeps each sheet's silhouette in `#0d0a14`, blurred 12–18 px for cards (3–12 for small
  pieces); `paint()` draws it at alpha 0.55, offset 1.65 × the light vector (2.4 for the mountains, so the sky looks
  farther back); sky bands get a canvas shadow (blur 16, offset 3, 5) from `layBand()`. Other casts (bigger hangs
  farther out): sun 1.6, moon 1.8, stars 2, fox 2.2 plus a blurred ground ellipse, title 3.2, snow 1.2 + 1.4 × band.
- Over the frame: multiply tint, vignette about (960, 440), screen lamp halo, fade overlay; no film grain or bloom.

## Shapes, line and figures
- Every shape is a `Path2D`: `poly()`, `box()`, `disc()`, `ridge()` (area under a curve, for card tops), `bandShape()`
  (scallops), `teeth()` (zigzag snow), `starPts()`, `flakeShape()`, `tornRect()`, `limb()`. Clean blade cuts, smooth
  or straight; torn edges only on the title card (`tornRect()`, ±3 px every 24 px) and the smoke puffs. No outlines:
  the only strokes are threads, the words' white edge and the fox's closed eye.
- Rules for a new piece: one flat palette fill through `cutShape()`; details as glued pieces, never painted lines;
  baked with `bakeSheet()` and drawn with `place()` and a cast multiple for its depth; a closed silhouette easy to
  cut with scissors; moving parts as separate rigid pieces joined at `brad()` pins; sized by depth like the pines
  (hill 0.38–0.62, forest 0.78–1.33, tall pine 2.2, bank 0.8–1.35 (twigs 0.8–1.2), wings 3.9–4.3).
- A moving piece on a card other than the puppet's is drawn in the `ART.cards` loop right after that card's
  `drawImage`, as the smoke is (light seen through holes goes just before it, as the lamps do), offset by that card's
  dx and dy so it pans and rises with it, with `place()` and a cast of about 0.5 × the light vector.
- The puppet: `paintFox()` draws into `FOX.cv` (760 × 340) at `FOX_SCALE` 0.88: far legs (darker, unpinned), `TORSO`,
  `CHEST`, `HAUNCH`, near legs, a three-bone tail smoothed by `chaikin()` into a tufted brush (`tailShape()`), `HEAD`
  turned about its neck pin. Legs are two `limb()` capsules and a paw, angled from straight down (`foxLeg()`); pins
  at hips, shoulders, neck, tail root; each part is `foxPart()` (glued shadow, then cut piece).

## Composition and camera
- 16:9, back to front: dusk card; sun at x 330 sinking from y 430 to 760; mountains (peaks y 385–470, foot 660);
  hill (`hillTop`, about 668; `CABIN` x 640); forest (`forestTop`, about 800; `TALL_PINE` 1345); the fox on
  `FOX_GROUND` 915 in the forest card's slot; bank (`bankTop`, about 958); wings (strip 1046, pines at x 110 and
  SW + 90). The night card, moon (to 1650, 235) and stars (x 150, 320, 1790, 1880) are drawn between the sun and the
  mountains, so the moon rises from behind the peaks; only the title (x 960, `TITLE.restY` 285) hangs in front of
  everything.
- Camera: a horizontal pan only, `cameraX()` from −40 to 140 over 1.0–6.6 s. Cards move −0.22 × depth × cam (depth
  1–5), the fox −0.66, sun and moon −0.15, stars −0.1; sky cards and title stay. Cards are baked at 1× and
  overscan by `PADX` 160 px a side, so 0.22 × 5 × |cam| stays under 160: no zoom, cut or shake. 9:16 and 1:1
  rebuild the set at the new size (Adapting).

## Motion
- Easing: `inOutCubic` for sun, night card, tint, light swing, camera, lying down and tail curl; `outCubic` for the
  moonrise and word lift; `backOut(v, over)` for arrivals (cards 1.35, title drop 1.6, words 2.2, stars 2.6).
- Smooth 30 fps, no held frames, stepping or jitter: rigid pieces turn about pins, never bend or morph; scale only
  fakes a turn (snow and stars flip edge-on) or a small squash (the lying fox 0.88 × 0.9, breath ±1.8 %).
- Gait: the fox slows with 1 − (1 − u)^1.7 (`foxAt()`); phase = distance / 150 × 2π, so paws never skate; diagonal
  legs swing together (0.5 × amp rad), the body bobs 3.5 px, the tail sways at half rate, the gait fades at the end.
- Ambient, on film time, allowed through the final hold: snow (`SNOWFALL`, 55–150 px/s, drifting and flipping),
  smoke (2.7 s loop), breathing, the stars' 0.03 rad sway and spin, the sun's turn. No jitter loop; all else is action.
- The stars' damped swing never settles in the demo (fix in Adapting). The title's swing is tapered to zero at the
  literal 8.45 s: write it as `TITLE.at` + 1.45 (+ 1.25 in the 6 and 4 s plans).

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.6 | Fade up from dark | `paint()` |
| 0.15–1.59 | Five cards rise from 620–860 px below, 0.16 s apart, 0.8 s each | `riseStart`, `riseOffset`, `ART.cards` |
| 1.0–6.6 | Camera pans 180 px right with parallax | `cameraX` |
| 1.2–5.3 | Fox trots in from x −330, behind the left wing, to 1290, slowing | `foxAt()`, `TROT_FROM`, `TROT_TO` |
| 1.3–3.6 | Sun sinks behind the mountains | `ART.sun`, `paint()` |
| 2.3–10 | Paper snow in three depth bands | `SNOW_START`, `snowfall()` |
| 3.0–4.6 | Night card pulled in from the right (to 4.2), tint cools (to 4.3), shadows swing down-left | `buildNight()`, `paint()` |
| 3.9–5.6 | Moon rises to (1650, 235) | `ART.moon` |
| 4.35–5.47 | Four stars lowered on threads, 0.14 s apart, then swing | `hangingStars()`, `HANGING`, `STARS_FROM` |
| 5.3–6.85 | Fox nods, lies down (5.75–6.45), curls its tail (6.0–6.85), shuts its eyes (6.55–6.8) | `foxAt()` |
| 6.35–7.03 | Windows light at 6.35 (one flicker), 6.7, 6.95; halo; smoke from 7.05 | `WINDOWS`, `lampLevel`, `SMOKE_FROM` |
| 7.2–8.6 | Title drops on threads (to 7.95), swing dies by 8.45; words pop 7.7–8.6 | `TITLE`, `paintTitle()` |
| 8.6–9.35 | Hold (0.72 s; the stars never settle) | |
| 9.35–10 | Dims to dark | `paint()` |

- Scenes open by assembling (cards rise, nearest last), move by pull-tab cards, threads, light and the puppet, and
  close on a card hung in front of the set; 0.5–1.5 s beats overlap. All but the fox, cabin and valley are reusable.
- Demo faults: the stars never settle (fix in Adapting); the fox turns dull brown at night (Palette); in 16:9 and 1:1
  the card hides the tall pine's apex from 7.4 s (accept it, or move `TALL_PINE` out of the card's x span).
- `KEYS=0.5,2.5,3.6,5.0,7.0,8.5,9.2`: rise, fox, night pull, moon and stars, lamps, title landed, final hold.

## Sound
audio.py reads events.json (cues with `t`, `k` and optional `v`, `f`, `d`), synthesizes 48 kHz stereo at `DUR` 10.0
and limits with tanh.
- Bed, not from cues: wind (150–1400 Hz noise swelling every 2.9 s) on the whole buffer; a four-note D-major pad at
  fixed times, `tone()` from 0.2 s for 9.7 s (1.8 s attack, 1.4 s release) with a ±12 % tremolo at 0.21 Hz sized by
  `tt()` of the same 9.7. The master fade-in 0.3 s and last-0.8 s fade-out follow `DUR`.
- Cues: `slide` (card; `v`), `tap` (knock; `f`, default 140; `v`), `step` (crunch; `v`), `tab` (pull tab; `d`), `moon`,
  `star` (bell at `f`), `sniff`, `rustle` (`d`), `light` (click and bell at `f`), `whoosh` (`d`), `pop` (`f`), `chord`
  (2.2 s close). Literal times: `tab`, the night card's `tap` (4.18), `moon`, `sniff`, `rustle`; the rest follow cards,
  fox (a `step` per 75 px), stars, windows, title. No cue is looked up by name; unknown kinds and cues past `DUR` drop.
- What breaks it (tested): `star`, `light` or `pop` without `f` (KeyError; a fifth star or fourth window, as `f` comes
  from four chimes and three bells); `tab`, `rustle` or `whoosh` without `d` (KeyError) or with `d` ≤ 0 (ValueError);
  the pad's 9.7 changed in `tone()` but not `tt()` (ValueError); a pad attack of 0 (one NaN sample: "ok nan", and
  check_audio.py passes it). Pans are literals or random within ±0.6. Fractional `DUR` works (6.3333).
- Safer: pitches `chimes[i % chimes.length]`, `bells[i % bells.length]`; the pad length once (PAD = `DUR` − 0.3) for
  `tone()` and `tt()`, attack under a quarter of the film (tested 1.5 s at 8 s, 1.0 at 6, 0.6 at 4; 14 s as is).

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Numbers, easing, random, colour | `anim.html` → `span`, `anim.html` → `backOut`, `anim.html` → `seeded`, `anim.html` → `blendHex` | `span(t, t0, t1)`, `mix`, `unit`, `outCubic`, `inOutCubic`, `backOut(v, over)`, `seeded(n)`, `tint(hex, k)` | as is |
| Grain, cut piece, glue | `anim.html` → `GRAIN`, `anim.html` → `cutShape`, `anim.html` → `gluedShadow` | `cutShape(c, shape, colour, lipGain)`, `gluedShadow(c, shape, dx, dy, blur, alpha)`; grain built once | as is |
| Card / sheet | `anim.html` → `bakeSheet`, `anim.html` → `place` | `bakeSheet({ w, h, ax, ay, parts: [{ shape, fill, glue, lip }], blur, after })`; `place(sheet, x, y, { sx, sy, turn, alpha, cast: [dx, dy, a] })` | as is |
| Shape kit and pine | `poly()`, `box()`, `disc()`, `ridge()`, `bandShape()`, `teeth()`, `starPts()`, `flakeShape()`, `tornRect()`, `pine()` | `pine(x, base, s, green)` returns parts | as is |
| Sky and landscape cards | `buildDusk()`, `buildNight()`, `layBand()`, `buildMountains()`, `buildHill()`, `buildForest()`, `buildBank()`, `buildWings()`, `hillTop`, `forestTop`, `bankTop` | `ART.cards` rows `{ sheet, depth, fox }` | adapt per set |
| Rise, parallax, light, finish | `riseStart`, `riseOffset`, `cameraX`, `paint()` | | as is; tint colours per time of day |
| Snowfall | `SNOWFALL`, `snowfall()` | `snowfall(t, depth, sun)`: 0 behind the forest, 1 in front of the puppet, 2 in front of all | as is |
| Things on threads | `hangingStars()`, `HANGING`, `STARS_FROM` | rows of x, thread length, scale, phase | as is, plus the taper fix |
| Puppet kit | `limb()`, `foxPart()`, `brad()`, `chaikin()`, `tailShape()`, `FOX` | `limb(x0, y0, r0, x1, y1, r1)` | as is |
| The fox | `paintFox()`, `foxLeg()`, `HEAD`, `TORSO`, `CHEST`, `HAUNCH`, `foxAt()`, `pawPrints()` | | replace |
| Lamps and smoke | `CABIN`, `WINDOWS`, `lampLevel`, `chimneySmoke()` | holes cut in `buildHill()`, light drawn behind the card | demo; reuse the technique |
| Title card | `buildTitle()`, `paintTitle()`, `TITLE` | words, fonts, `restY` | adapt copy |
| Timeline, cues, sounds | `paint()`, `window.events`, `audio.py` | cue kinds in Sound | replace; audio.py as is but `DUR` and pad |

## Adapting
- **Style vs demo plot:** style is the rising card stack, cut pieces with lip, grain and shadows, one light, paper sky,
  capped pines, pinned puppet, pull-tab and thread moves, hanging title; plot is the fox, valley, cabin, moon, stars.
  Transformations: a sky card pulled across, lamps lit through cut holes, things on threads, a puppet arriving.
- **New subject:** build it by the rules in Shapes in its own canvas, in the card slot it walks in (the `fox` flag
  in `ART.cards`). A child (coat, scarf, pompom hat, capsule limbs, boots, pins at hip, shoulder and neck) read
  clearly at about 400 px tall in 16:9 and 420 px in 9:16 (420 px under the 16:9 card lost its pompom behind the
  card's overshoot for 4 frames). Shape-dependent: canvas and origin (fox 760 × 340 at 400, 290; child
  520 × 480 at 240, 450), ground-shadow width (120–150; 70), paw prints and the 75 px step spacing (half the 150 px
  stride), the stop point against `TALL_PINE`, and title clearance: the card's bottom reaches `restY` + 220 at its
  overshoot (+ 243 in 9:16), so in 16:9 a subject under it stays under 410 px.
- **Fixes, tested:** multiply the damped term in `hangingStars()` by (1 − span(age, 0.7, 1.9)), set `TITLE.at` to 7.0
  and keep the swing's end at 8.45 (`TITLE.at` + 1.45): the demo settles at 8.433 s and holds 0.92 s in every
  format. The action clock below compresses the film and measures holds: render every frame of the ending in the
  project and in a copy with FORCE true; the hold runs from the first time every later pair is identical to the fade.

```js
let FORCE = false;                       // true: every action at its end state
const K = 1;                             // action speed (1.25 in the 8 s plan)
const A = t => (FORCE ? 99 : K * t);     // the action clock
// paint(): span(A(t), …) for nightfall, lightAngle, sunY, nightX, moonUp; if (A(t) < 4.3) for the sun; cameraX(A(t));
//   riseOffset(i, A(t)) and lampLevel(A(t), j), also in the halo; paintTitle(A(t), sun); pose = foxAt(A(t)), breath on t.
// hangingStars(): A(t) < t0, span(A(t), t0, t0 + 0.7), age = A(t) - t0, damped term * (FORCE ? 0 : 1).
// on film time: snowfall(t, …), chimneySmoke(t, …), the sun's turn, the stars' sway and spin, the fade.
```
- **Length:** past 10 s add reusable beats (another pull-tab card, more threads, a second puppet action), 1–1.5 s
  each; a set with no new event tires after about 3 s. Ambient loops hold to 14 s (tested with only the fade moved).
- **Shorter:** 7–10 s keeps every beat with a faster action clock (`K` up to 1.3, limited by the trot's cadence).
  Under 7 s cut whole beats with their cues: stars and nod, then the trot (the fox already stands under the pine).
  Keep the card rise (complete at 1.59 s, 1.0 s after the 0.6 s fade-in; 1.28 s in the 4 s plan), a sky change and
  the lamps; in 9:16 keep the title or the stars. The title costs 1.4 s to its last word (1.25 s with words 0.12 s
  apart over 0.36 s), then 0.8 s of hold. All plans tested in 16:9, 9:16 and 1:1 (peaks 16:9; 9:16 and 1:1):

```js
// 8 s, every beat, with both fixes (without them the stars still swing into the fade): K = 1.25; SNOW_START,
//   SMOKE_FROM and the breath's 6.9 divided by K; fade span(t, 7.6, 8); cues t / K. audio.py DUR 8.0,
//   pad tone(.., 7.7, 1.5, 1.2) and tt(7.7). Settled 6.767, held 0.83 s; peak 0.669; 0.626.
// 6 s, stars and nod cut: cameraX (0.9, 4.0); sunY (0.9, 2.3), sun while t < 3.0; nightfall (1.9, 3.0), lightAngle
//   (1.9, 3.2), nightX (1.9, 2.9); moonUp (2.5, 3.7); SNOW_START 1.4; no hangingStars(); TROT_FROM 0.9, TROT_TO 3.3,
//   FOX_START 150 in 16:9 (1.2 x the demo's speed), -330 in 9:16 and 1:1 (1.1 x); dip 0; lie (3.4, 4.0), tail (3.6,
//   4.3), eye (3.95, 4.15), breath from 4.3; WINDOWS 3.8, 4.0, 4.15; SMOKE_FROM 4.2; TITLE.at 3.3; fade (5.55, 6).
//   Cues: tab 1.9 (d 1.0), tap 2.88, moon 2.55, rustle 3.45, 3.65 (d 0.6), no star or sniff. audio.py DUR 6.0,
//   tone(.., 5.7, 1.0, 1.0), tt(5.7). Settled 4.70, held 0.85 s; 0.650; 0.501.
// 4 s, trot, stars and nod cut: riseStart 0.1 + 0.12 * i, rise 0.7 s, tap at riseStart + 0.45; cameraX (0.3, 2.6);
//   sunY (0.6, 1.6), sun while t < 2.0; nightfall (1.1, 2.0), lightAngle (1.1, 2.1), nightX (1.1, 1.9); moonUp (1.5,
//   2.6); SNOW_START 1.2; TROT_FROM -2, TROT_TO -1 (the fox stands at FOX_STOP), no step loop; dip 0; lie (1.9, 2.4),
//   tail (2.0, 2.6), eye (2.3, 2.5), breath from 2.6; WINDOWS 2.2, 2.4, 2.55; SMOKE_FROM 2.6; TITLE.at 1.4, word t0
//   TITLE.at + 0.5 + 0.12 * i over 0.36 s; fade (3.5, 4). Cues: tab 1.1 (d 0.8), tap 1.88, moon 1.55, rustle 1.9,
//   2.05 (d 0.5), pops TITLE.at + 0.65 + 0.12 * i, chord TITLE.at + 1.2. audio.py DUR 4.0, tone(.., 3.7, 0.6, 0.8),
//   tt(3.7). Settled 2.633, held 0.87 s; 0.382 all. Both short plans end the title's swing at TITLE.at + 1.25.
```
- **Other formats:** rebuild every card at the new size, fixes included. Rendered, and checked frame by frame for
  shared pixels between title, threads, stars and moon and for pieces crossing the frame edge; 1:1 after `//`:

```js
canvas 1080 x 1920; const SW = 1080, SH = 1920, OY = 505;                  // 1080 x 1080, OY = 0
hillTop, forestTop, FOX_GROUND + OY; buildMountains(): py + OY in top() and the cap teeth, 660 + OY
riseOffset(): (620 + OY + 60 * i) * …   // 1:1 unchanged; without + OY the 9:16 cards sit in the lower third at t = 0
bankTop 958 + OY + 130, parabola about SW / 2; buildWings() strip and pine bases + OY + 200   // 958, SW / 2; + 0
buildBank() twigs [150, 420, 1000]; CABIN.x 300; TALL_PINE 780; FOX_STOP 725   // same
buildDusk() band y0 -10, 300, 560, 760, 940; buildNight() band 975          // 16:9 bands; 470
buildNight() in 9:16, before the 975 band: layBand(c, bandShape(w, 400, 70, 14, x => 9 * Math.sin(x / 110 + 1)), '#2d397a', 0.4);
                                           layBand(c, bandShape(w, 690, 64, 15, x => 10 * Math.sin(x / 100 + 2)), '#334089', 0.42);
sun x 250, y + OY; moon x 1000, from SH + 170 up to y 850       // sun x 200; moon x 1000 to 245, place() sx = sy = 0.85
HANGING [[75, 330, 0.95, 0.2], [140, 150, 0.7, 1.3], [1010, 420, 0.8, 3.84]]   // phase 3.84: its first swing goes left, so it stays in frame
                                  // 1:1 [[70, 330, 0.95, 0.2], [130, 120, 0.75, 1.3], [190, 470, 0.6, 2.1]]
vignette createRadialGradient(540, 860, 300, 540, 960, 1300)               // (540, 440, 200, 540, 540, 800)
TITLE.restY 520; title 900 92px, kicker 700 54px                            // 300; 78px, 48px
paintTitle(): drop from TITLE.restY + 275 instead of 560 (16:9: 285 + 275 = 560)   // 560
```
- 9:16 at 8.5 s: card x 175–905 (backing 925), y 370–690; text x 275–810, y 430–640; moon x 891–1066, low, as the
  card's path and threads fill the sky; stars outside the card's x span and inside the frame (with phase 0.7 the
  third star swings 98 % out of the right edge at 4.93 s); the fox above y 1440, bank, twigs and wings in the
  caption band. The extra night bands keep the largest flat area at 19 % (4.25 s) and 15 % (4.8–7.0 s; one band:
  46 % and 30 %), the same in the 8 s plan. 1:1: card x 214–866 (backing 886), moon x 904–1054. Signature check at
  0.1–8.5 s in both: every item visible and whole once risen (in 1:1 the pine's apex hides behind the title from
  7.4 s). Not carried over: a fourth star.

## Boundaries
- **Distinct from:** `collage` (flat scrapbook of torn scraps, tape and halftone at 12 fps with jitter);
  `chinese-papercut` (one red sheet cut live into symmetric lace, then unfolded); `felt-stopmotion` (fuzzy wool,
  boiling fibres, 12 fps); `clay` (plasticine, fingerprints, 12 fps jitter); `origami` (folded 3D paper, WebGL);
  `silhouette` (black backlit puppets on coloured light, on twos); `title-sequence` (flat ragged bars, jazzy credits);
  `victorian-engraving` (engraved cut-outs, stiff 15 fps pivots); `map-documentary` (pinned paper map with red
  string, objects on twos); `papel-picado` (perforated tissue lit from behind); `picture-book` (painted gouache
  pages). A pop-up book look, with panels folding up out of a spread, has no catalog style: these cards never fold.
- **Poor fit:** data (`data-visualization`), dense text (`kinetic-typography`), interfaces (`product-ui`), fast gags
  (`saturday-cartoon`), a truly handmade stepped stop-motion feel (`felt-stopmotion`, `clay`).
- **Do not:** step or jitter the motion, tear every edge, gloss pieces; keep one light direction for every live cast.

## Technical notes
- No render.json, no vendor folder: Canvas 2D, no GPU; anim.html, fonts.css and two woff2 files. 300 frames take
  about 40 s with WORKERS 1 (60 frames in 7.3 s, tested). Deterministic (tested in 16:9 and 9:16). audio.py draws
  every random value from one `np.random.default_rng(9)` stream: adding a cue changes later pans and crunches.
- `place()`, `chimneySmoke()`, the star backs and the card shadows assign `globalAlpha` instead of multiplying it, so
  a scene faded with `globalAlpha` leaves them opaque: fade with an overlay fill, as the demo does, or multiply.
- `buildTitle()` leaves `out.font` and `out.letterSpacing` (−1 px) set on the main context; a new text drawer sets its
  own. `letterSpacing` needs Chromium 99 or later (Playwright's is).
