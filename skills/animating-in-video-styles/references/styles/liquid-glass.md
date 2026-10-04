# Liquid Glass (`liquid-glass`)

Clear, liquid glass over a night sky full of aurora: drops and panels that bend the light behind them, split and
melt into one another like water, and finally pour themselves into a glass mark. It draws on premium launch films
and interface motion in general, with no company or product behind it. Calm, polished and luminous.

**Reference film:** a glass bead glides over "Introducing", splits into three, melts into a three-mode switch whose
lens recolours the sky, then pours into the lockup "Liquid / Glass", crossed by a glint · `styles/liquid-glass/`

## Signature
- A near-black night sky, faded up over 0.6 s, with three drifting aurora curtains: a bright green hem rising into
  teal and violet rays, a few stars, bloom and a dark vignette. It fills the frame behind everything.
- Glass with no colour of its own, bending what lies behind it: white type or line art under a glass drop is
  magnified, displaced and fringed red and blue at the rim; a pin-point highlight at upper left, a hairline bright
  rim, a glowing inner edge at lower right and a soft shadow cast down and right (in the demo: from 0.45 s).
- The glass behaves like liquid: shapes land on springs with a stretch along their path, squeeze before they change,
  and split or merge through smooth necks; they melt, never cut or cross-fade (in the demo: one bead splits into
  three at 2.0 s).
- Clean white Inter Tight, small and well spaced, glowing softly, set where the glass will pass over it.

## Palette
| Role | Colour | In code |
|---|---|---|
| sky, top → bottom (linear light) | `vec3(.0022, .0026, .0100)` → `vec3(.0012, .0040, .0080)` | `AURORA` |
| aurora at the opening: hem, mid, top | `[0.10, 1.00, 0.52]`, `[0.03, 0.72, 0.80]`, `[0.50, 0.22, 1.00]` | `PAL.open` |
| aurora behind the mark | `[0.12, 1.00, 0.60]`, `[0.10, 0.62, 1.00]`, `[0.85, 0.25, 0.95]` | `PAL.title` |
| stars | `vec3(.75, .88, 1.)` | `AURORA` |
| type under the glass / on a glass panel (HDR white, blooms) | `vec3(2.4)` / `vec3(2.3)` | `AURORA` / `GLASS` |
| glass tint: frosted panel, mark, lens over glass (clear drop: none) | `[0.60, 0.67, 0.86]`, `[0.94, 0.97, 1.04]`, `[1.25, 1.27, 1.32]` | `stage()` → `tint` |

- Linear-light RGB on half-float targets, toned by `1. - exp(-c * 1.15)` and gamma 2.2 (`FINAL`); no flat fills.
- Each state may give the sky its own colours (in the demo `PAL.focus`, `PAL.flow`, `PAL.rest`), blended by `mixHue()`
  through hue, never grey or amber. Glass multiplies (`tint`), adds white (`milk`) and the sky's colour (`env`).

## Typography and copy
- Inter Tight (`fonts/InterTight-normal-300-800-latin.woff2`, `-latin-ext.woff2`); `window.ready` loads 400–800 only
  for the text of `KICKER`, `TITLE` and `LABELS`, so put new copy there (`fonts.css` serves latin-ext on demand).
- One offscreen canvas holds the text, one channel per role (`paintText()`, composited `lighter`):
  - blue, under the glass: a short line, 500 at 66 px, 1.5 px tracking, set by `typeset()` (kerning kept); `AURORA`
    mixes it toward HDR white, so glass over it refracts it and it blooms (in the demo: the kicker);
  - red, on a glass panel: labels, 600 at 50 px, refracted only by a lens over the panel; the selected one scales to
    1.1 and goes from 62 % to full alpha within 210 px of the lens;
  - green, overlay: `tx2.fillStyle = '#0f0'`; `FINAL` draws it crisp near-white `vec3(.97, .98, 1.)` with a soft
    shadow (tested at 48 px), for a line that must not be glass, such as a URL.
- The mark is a distance field, not text: `titleField()` sets `TITLE` in 800 at `TITLE_PX` 310, `letterSpacing`
  6 px, two centred lines `TITLE_LEAD` 340 apart.
- Voice: a launch film's minimum: a one- or two-word line under the glass, one-word labels, a short name as the
  mark; sentence case, no punctuation. Text fades as the glass changes (labels also rise 14 px, 0.08 s apart).
- Copy limits (measured): the line under the glass up to about 16 characters (about 30 px each); a drop (300 px;
  260 px in 9:16) magnifies about 10 at a time and is not meant to cover it whole. Labels: three, one word, up to 9
  characters in 16:9 and 6 in 9:16. Mark: limit each line by its ink width (`measureText()`, left plus right
  bounding box, at 800 with 6 px `letterSpacing`), not by letters: under about 800 px in 9:16 and 1:1, so the ink
  ends left of x 950, and about 1,350 px in 16:9; most six-letter words need 200 px in 9:16 ("Liquid" 730 px at 250,
  "Window" 1,010). For more, lower `TITLE_PX` and `TITLE_LEAD` together and measure again: 150 px still reads as
  glass but closes the counters of e and a. Nothing auto-fits: an overlong line runs off the frame.
- Glyphs: Latin-1 and Latin Extended; a missing glyph silently becomes a system face inside the glass.

## Texture and finish
- `FINAL`: bloom of everything brighter than about 1 (`BRIGHT` at mip 2, `BLUR` at a quarter and a sixteenth of
  the frame, added at .26 and .34), a vignette darkening the corners by about 40 %, a little extra contrast, and a
  static dither of under one level from `h2()`. No grain, paper, scanlines or chromatic aberration outside the glass.
- Stars are fixed, left out of the band the glass crosses (a rim smears them); the aurora drifts on film time
  (`curtain()`, `n1t()`), and only the sky zooms, 0.7 % a second (`zoom`).

## Shapes, line and figures
- No outlines and no fills: every object is glass, one `GLASS` pass per layer over the image beneath:
  - height: `cap()` is a spherical-cap bevel, 70° at the rim, over the outer `bevel` px (40 on the mark), flat inside;
  - refraction offsets the background by the slope times `refr` (30–40 px), sampled at eight wavelengths, red
    bending least by `disp` (0.06 clear drop, 0.13 frosted panel, 0.17 mark, 0.2 lens);
  - frost (`frost`, 3.3 on a panel, 0 elsewhere) reads a blurred mip and eight `RING` taps, about 10 px;
  - lit from the upper left: the inner rim facing the light darkens 36 %, the far rim gathers the sky's light
    (`env`), a pin-point and a broad specular, a 1–2 px rim line, a sheen of the sky's colour on steep slopes all
    round, and `milk` haze (0.11 on a lens);
  - shadows: a cast shadow offset 16, 30 px (weight .58) and a contact shadow within 22 px (.34), both scaled by
    `shadow` (0.6 for drops, panels and lenses; 0.85 for the mark).
- Moving shapes are signed-distance primitives, not metaballs: up to six per layer in `boxes`, each [cx, cy, hw, hh,
  rad, sq], an ellipse (`sdEll`; rad equal to min(hw, hh) and `bevel` gives a lens with no pinch) or a rounded box
  (`sdBox`, sq 1). The first `split` boxes and the rest form two `smin` groups (radius `k`: 78 drops, 40 panels);
  `blend` fades group to group, `textMix` to the mark's field. A split moves boxes apart until the neck breaks, a
  merge shrinks them into a neighbour (`absorb`); a second layer draws glass over glass (in the demo: the lens).
- A shape whose `bevel` exceeds its half-thickness creases star-like at its centre: when a pour starts from anything
  but a panel, give `bevel` and `k` the panel's values once the blobs appear (as the 4 s plan does).
- The mark (logo, word, object, icon) is a filled silhouette drawn solid white into the canvas in `titleField()`:
  text, a Path2D fill (even-odd for counters) or an image's alpha as a white shape; red is read as coverage. `edt()`
  makes it exact and a Gaussian (`SIGMA` 6.5) rounds it. Keep strokes 40 px or wider and counters 35 px or wider,
  inside the rows `Y0` to `Y0` + `ROWS` (the field outside them is extrapolated); one mark field exists (`sdfTex`).
  Its pour needs blobs: `titleField()` returns `letters`, stored by `setup()` as `letterBlobs`, {cx, cy, hw, hh}
  ellipses about 1.2× each part's half-extent (the code: hw = max(0.62 × width, 70), hh = 0.6 × height), listed left
  to right since they swell 0.06 s apart in list order, five at most since the panel's box makes six.
- Other objects appear as white line art under the glass: in `paintText()`, stroke them in '#00f' with a 10 px line
  (like the type's stems), fade them with an alpha from `stage()` as `kicker` is, and size them about the drop
  (200–300 px in 9:16); a bread loaf and a train front refract and fringe like type. Fill only dot-sized details
  (24 px, like the dot of an i): a 140 × 72 px filled window blooms into a blob that blows out the glass over it.
- Stand-in rendered in 9:16: a 430 px teardrop with a counter above the word "Calm" (Path2D and `fillText()`, four
  blobs) pours and settles like the lockup; only `Y0`/`ROWS` (420, 960), the blobs and the layout depend on it.

## Composition and camera
- One element at a time, centred on `CX`, `CY`. The aurora's hem slopes up from lower left to right; the lower right
  is dark ground with stars (the bottom fifth).
- Glass must sit over the bright curtains: over the dark ground it reads dark grey. The hem moves with film time and
  rises to the right, so an earlier end card or a wider lower line meets it (as written, 23–32 % of "Glass" at the
  8, 6 and 4 s end cards; at 10 s, 10 % of a 1,240 px "Morning" and its last pour blob). So every new 16:9 film
  lowers the sky, not the lockup (`vec2(.89, .42)`, star gap .42, as every plan in Shorter does); with a new mark or
  length, render the pour's widest moment and the final key and check the lower line sits over the curtains.
- Camera: none.
- Other formats: 9:16 and 1:1 were rendered at every shot's widest moment and end card in every plan, all glass over
  the curtains. 9:16 arrangement: keep everything inside y 500–1260; centre the mark on y 860 with its ink inside
  x 140–940 (demo copy: ink x 178–902, panel overshoot to x 990); leave the bottom 15 % as dark ground with stars.
  In 1:1 the bottom 20 % is dark ground, as in 16:9.

| Value in code | 16:9 demo | 9:16 (1080 × 1920) | 1:1 (1080 × 1080) |
|---|---|---|---|
| canvas, `W`, `H` | 1920 × 1080 | 1080 × 1920 | 1080 × 1080 |
| `b1`, `b2` in `setup()`: `target(W / 16, 68)` | 120 × 68 | `target(68, 120)` | `target(68, 68)` |
| `BEAD_R`, `SMALL_R` | 150, 100 | 130, 86 | 130, 86 |
| `GAP`, `PILL_HW`, `PILL_HH`, `THUMB_HW`, `THUMB_HH` | 360, 560, 105, 172, 84 | 240, 420, 105, 150, 84 | as 9:16 |
| label reach `/ 210` in `labels`; glide `1150` in `stIn` | 210; 1150 | 140; 760 | 140; 760 |
| `TITLE_PX`, `TITLE_LEAD`, `TITLE_CY` | 310, 340, 466 | 250, 280, 860 | 250, 280, 500 |
| `Y0`, `ROWS` in `titleField()` | 110, 760 | 500, 760 | 110, 760 |
| glint sweep `mix(-640, 640, …)` | ±640 | ±520 | ±520 |
| sky mapping in `AURORA`: `/ uRes.y`, `vec2(.89, .5)` | as written | `/ vec2(1350., 2400.)`, `vec2(.89, .42)` | `/ uRes.y`, `vec2(.89, .4)` |
| star gap `abs(q.y - .5)` | .5 | .4 | .4 |

- 9:16, why: height-only scaling gives 1.8× rays and a dark bottom third; the split sky scale keeps rays about 1.25×
  their 16:9 width while the curtains fill the height (hem near y 1450). Keep the 16:9 lens heights: a lens under
  about 168 px refracts cyan fragments of its label into its rim.

## Motion
- Everything is a closed-form function of t in `stage()`, from `T` plus fixed offsets. Moves are under-damped
  springs (`spring()`, `springVel()`), ramps `smooth`, `easeOut` (labels) and `easeIO` (hand-overs, pour, glint).
- Springs by move (Hz, damping, overshoot; demo values): an entrance glide 0.95, 0.7, 5 %, arcing up from 70 px
  below; a split 2.0, 0.5, 16 %, the second drop 0.09 s later; a stretch into a panel 2.2, 0.6, 10 %; a pop 2.6,
  0.55, 13 %; a slide 1.9, 0.68, 5 %; the pour's blobs 2.4, 0.5 from half size, 0.06 s apart left to right. Fast
  shapes stretch along their path by `springVel()` (up to 22–26 %) and thin across it.
- Anticipation before each change: a squeeze before a split (`squeeze`), a lean-in before a merge (`gather`), a
  draw-in before a pour (`ant`, 64 px on the panel). A mark lands with a 6 px ring at 2.2 Hz (`ring`). Each change
  of state recolours the sky over 0.6 s; the pour brightens it (`gain` to 1.4) before it calms to 1.12.
- Never: cuts, cross-fades between shapes, rotation, camera moves, linear moves, bounce on text, opaque glass.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.6 | fade up from black; aurora drifting | `fade`, `AURORA` |
| 0.1–0.6 | "Introducing" fades up, centred, under the glass | `T.word`, `kicker` |
| 0.45–1.4 | bead glides in from the left and settles over the word (land cue 1.09) | `T.bead`, `eIn`, `stIn` |
| 1.45–2.0 | the word fades out; the bead squeezes | `T.wordOut`, `T.squeeze` |
| 2.0–2.5 | split into three beads; the centre one shrinks to `SMALL_R` | `T.split`, `give` |
| 2.8–3.4 | lean in, then melt into the switch: side beads absorbed, stretch, frost | `T.gather`, `T.pill`, `grow`, `asPill` |
| 3.2–3.7 | labels arrive; at 3.5 the lens pops onto Focus, sky to Focus over 0.6 s | `T.labels`, `T.thumb`, `pop` |
| 4.15, 4.9 | lens slides to Flow, then Rest; sky follows | `T.slide1`, `T.slide2` |
| 5.45–5.88 | lens swells and vanishes, labels fade, the switch draws in | `T.clear`, `leave`, `ant` |
| 5.88–6.7 | pour: five blobs swell, resolve into the wordmark; sky to the mark's palette, brightening | `T.morph`, `T.resolve`, `blobs`, `m` |
| 6.7–8.0 | the mark lands with a ring; sky calms | `T.title`, `ring`, `swell` |
| 8.05–8.85 | glint sweeps left to right across the glass | `T.glint`, `glint` |
| 9.3–9.96 | fade to black | `T.fade` |

- One continuous shot; each scene melts into the next shape; beats last 0.6–1.3 s: a line under a drop, a split
  or merge, a panel whose lens changes the sky's state, a pour into the mark, a glint, a hold.
- KEYS for contact_sheet.sh, the last being the settled final state (all rendered in 9:16): demo 1.1, 2.4, 3.6, 4.6,
  5.3 (lens on Rest as the sky turns rose), 6.3, 8.45, 9.0; 10 s held plan the same with the glint at 7.55 and the
  end at 8.6; 8 s 1.04, 2.03, 3.1, 3.71, 4.21, 5.13, 6.0, 6.6; 6 s 0.95, 1.78, 2.38, 3.56, 4.25, 5.0; 4 s 0.6, 1.66,
  2.35, 3.2.

## Sound
audio.py reads `events.json` as `{t, k, …}` cues and synthesizes everything with NumPy (seeded), a 2 s reverb, tanh
limiting and a 0.84 peak.
- Bed, not cued: a pad on a D major add-9 chord in detuned, breathing pairs, its `swell` attack of 1.6 s written
  from t = 0; three upper voices open over 1.2 s from 0.5 s before the `title` cue (`opened`); a thread of high
  `air` noise. The master fades from the `fade` cue to `DUR` − 0.03.
- `glide` (`d`): a whoosh panned left to centre. `land`: a water-drop `bloop()` and a high `glass()` ping. `split`:
  a falling bloop. `bead` (`i` 0 or 1): bloop and ping, panned ∓0.6. `merge`: a gulp, sub thump and whoosh. `label`
  (`i`): a tick. `select` (`i`): a struck-glass note from `ARPEGGIO` (D5, F#5, A5) with its octave. `slide`: a whoosh
  panned one step further right each time (`slides` counts them). `clear`: a rising hiss. `morph` (`d`): a whoosh
  and thirteen bubbles over `d`. `title`: a sub drop and a six-note glass bell chord. `glint` (`d`): a shimmer.
- Required: `title` and `fade`, looked up by name (KeyError without them). A new film emits `glide`/`land` for an
  entrance, `split`/`bead` for a split, `merge` for a merge, `label`/`select`/`slide` for labels and a lens, `clear`,
  `morph` with `d` = title − morph, `title`, `glint` and `fade`.
- Breakers (tested): `label` `i` outside 0–2, `select` `i` −1 and a third `slide` pan past ±1 (NaN, silent);
  `select` `i` 3 IndexError; `bead` without `i` KeyError; `glide`, `morph`, `glint` with `d` 0 ValueError. A `fade`
  cue at or after `DUR` − 0.03 silences the track (NaN, or "mostly silent" in check_audio.py), so keep `T.fade` plus
  the picture's fade at or below it. Cues past `DUR` are dropped.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Aurora sky | `anim.html` → `AURORA`, `curtain()`, `ramp()` | uniforms from `render()`: time, `gain`, `zoom`, palette from `blend()` of `PAL` | as is; format values in Composition |
| Glass layer | `anim.html` → `GLASS`, `glassValues()` | the layer object (keys in Shapes; `boxes` at most six) | as is; copy the demo's layer values |
| Mark field | `anim.html` → `titleField()`, `edt()` | draws `TITLE` (or any white silhouette) at 2× in rows `Y0`…`Y0` + `ROWS`; returns the field and `letters` (stored as `letterBlobs`), from `TITLE_BLOBS` ([line, from, to], at most five) | adapt: copy, logo, band |
| Text channels | `anim.html` → `paintText()`, `typeset()` | blue under glass, red on a panel, green overlay | adapt: copy, line art |
| WebGL, bloom, finish | `anim.html` → `program()`, `target()`, `pass()`, `setup()`, `render()`, `BRIGHT`, `BLUR`, `FINAL` | `render()` runs sky, layer 1, layer 2 if present, bloom, final | as is |
| Motion helpers | `anim.html` → `spring()`, `springVel()`, `smooth`, `easeIO`, `seg` | `spring(tau, hz, zeta)` from 0 to 1 | as is |
| Timeline and layers | `anim.html` → `T`, `stage()` | the beat sheet and each layer's values as functions of t | adapt: re-time `T`, keep the offsets' logic |
| Glass panel and lens | `anim.html` → `stage()` (`layer2`, `labels`), `LABELS` | `GAP`, `PILL_HW`, `THUMB_HW`; the slide sums two springs | adapt or drop |
| Sound | `audio.py` → `put()`, `bloop()`, `glass()`, `whoosh()` | per-cue handlers, pad and air bed | adapt: `DUR`, cue times |
| Demo plot | `KICKER`, `LABELS`, `TITLE`, `TITLE_BLOBS`, `PAL` state palettes | | replace |

## Adapting
- **Style vs demo plot:** the style is the aurora sky and its finish, the glass, liquid behaviour (springs, stretch,
  smooth melts), white type or line art under a drop, optionally a glass panel whose lens recolours the sky per item,
  and a glass mark that a glint crosses before the hold. The plot is the demo's kicker, the split into three, the
  Focus/Flow/Rest switch and its colours, and the five-blob pour. Any melt counts as the transformation.
- **New subject:** it enters three ways: a short line or line art under a drop (blue), labels on a glass panel
  whose lens recolours the sky per item (red), and the mark (a name, a logo or an object's bold silhouette, or one
  above the other as in the stand-in). A bakery, say: a drop over "Fresh daily", a panel reading Bread / Pastry /
  Coffee, a pour into a loaf above the bakery's name. Replace the copy constants and `TITLE_BLOBS` (at most five,
  ranges inside each line) or list a logo's blobs (Shapes). Traps: a split still alive when the blobs arrive makes
  more than six boxes (RangeError in `glassValues()`); `titleField()` reads two lines: for one, centre on its ink.
- **Length:** past 10 s, stretch the holds; the sky drifts on film time with no seam, and `zoom` keeps growing (tested
  to 60 s, 42 %: nothing breaks). Change `DUR` in audio.py and keep `fade` before its end; nothing else in the score
  is fixed. A fourth panel item (16:9 only; four labels and a lens do not fit 9:16): a fourth `LABELS` entry and
  `PAL` palette; slides at 4.0, 4.6, 5.2, with a slide3 key in `T`, a third spring term in `slide` and `stS`, and a
  third `pal = blend(...)` line; `T.clear` 5.85, `T.title` 7.0; labels, the `sel` test and the lens at
  `CX + (i - 1.5) * GAP`, `PILL_HW` 740; cues add a third `slide` and `select` `i` 3; in audio.py a fourth
  `ARPEGGIO` note (86), `label` and `select` pans (i − 1.5) × 0.6 and × 0.55, and `slide` from −0.55 + 0.37 ×
  `slides` travelling 0.37.
- **Shorter:** re-time `T` and the cues; the aurora and `zoom` stay on film time. Holds: pixel difference against a
  twin whose every `T` key but `fade` is 100 s earlier, settled at no pixel more than 2 levels off; every plan's audio
  passes check_audio.py. Between 6 s and the demo keep every beat and shorten the gaps, not the ramps (fixed offsets
  in `stage()`): the 8 s plan holds each lens position 0.5 s (a slide arrives in about 0.35 s) and the three drops
  0.65 s, with the demo's copy.

| `T` keys and edits | demo | 10 s, held | 8 s, all beats | 6 s, no lens | 4 s, drop to mark |
|---|---|---|---|---|---|
| word, bead, wordOut | .1, .45, 1.45 | as demo | .1, .4, 1.25 | .1, .3, 1.05 | .05, .15, .85 |
| squeeze, split, gather, pill | 1.75, 2.0, 2.8, 3.0 | as demo | 1.45, 1.65, 2.3, 2.45 | 1.2, 1.4, 1.95, 2.1 | 99 (never) |
| labels, thumb, slide1, slide2 | 3.2, 3.5, 4.15, 4.9 | as demo | 2.6, 2.85, 3.35, 3.85 | 99 | 99 |
| clear, morph, resolve, title | 5.55, 5.88, 6.2, 6.7 | as demo | 4.35, 4.65, 4.97, 5.47 | 2.75, 3.08, 3.4, 3.9 | .85, 1.18, 1.5, 2.0 |
| glint, fade | 8.05, 9.3 | 7.15, 9.3 | 5.6, 7.3 | 3.85, 5.55 | 1.95, 3.6 |
| ring taper; sky calm (1.3 after title); fade length | –; 1.3; .66 | yes; 1.3; .66 | yes; 0.9; .66 | yes; 0.7; 0.4 | yes; 0.7; 0.35 |
| 16:9 sky in `AURORA`: vec2(.89, .5), star gap abs(q.y - .5) | as written | .42, .42 | .42, .42 | .42, .42 | .42, .42 |
| audio.py `DUR`; pad attack | 10; 1.6 | 10; 1.6 | 8; 1.6 | 6; 0.8 | 4; 0.8 |
| settled → fade (measured) | 8.867–9.3 (0.43 s) | 7.967–9.3 | 6.40–7.3 | 4.667–5.55 | 2.767–3.6 |

```js
// Every plan: the landing ring decays forever; taper it to zero (no visible change):
const ring = settle > 0 ? -6 * Math.exp(-6 * settle) * Math.sin(2 * Math.PI * 2.2 * settle) * smooth(seg(settle, 0, 0.08)) * (1 - seg(settle, 0.25, 0.6)) : 0;
// 8, 6, 4 s: the sky calms sooner, in swell (0.9 for 8 s):
... * (1 - 0.7 * smooth(seg(t, T.title + 0.1, T.title + 0.7)));
// 6 and 4 s: a shorter closing fade, in stage()'s return (0.35 for 4 s):
fade: smooth(seg(t, 0, 0.6)) * (1 - smooth(seg(t, T.fade, T.fade + 0.4))),
// 4 s (pour from the bead): lighter anticipation; panel blend radius and bevel for the blobs
hw = mix(hw, PILL_HW, grow) - 16 * ant;
hh = mix(hh, PILL_HH, clamp(grow)) + 6 * ant;
k: mix(78, 40, Math.max(asPill, blobs)),          // in layer1
bevel: mix(mix(beadBevel, 38, Math.max(asPill, blobs)), 40, m),
```
```python
swell = np.clip(time / 0.8, 0, 1) ** 1.5    # audio.py, 6 and 4 s: the pad's attack
```
  - Cut in this order: the lens and labels (6 s: the drops melt into a plain panel); the split and the panel (4 s:
    the drop pours straight into the mark). Keep the split only with the panel: without it the side drops never
    leave and the blobs push a layer past six boxes. Delete the cues of cut beats; set to 99 they are dropped.
  - Shortest opening: the fade-in is a fixed 0.6 s; in the 4 s plan the drop refracts the line from 0.6 s.
  - A title card costs about 2.4 s from `T.morph` plus the fade: 0.82 s pour, about 0.77 s until the sky has calmed
    and the glint has passed, 0.8 s hold. The glint is the last action in every plan; the 6 and 4 s plans start it
    0.05 s before `T.title`; drop it if time is shorter still.
- **Other formats:** the rendered 9:16 and 1:1 values and checks are in Composition and camera.

## Boundaries
- **Distinct from:** `liquid-motion` (opaque satin metaballs and gooey type in warm coral and plum gradients;
  nothing refracts); `inflated-3d` (also inflates silhouettes from a distance field, but into opaque matte pastel
  balloons in three.js on a light set); `blob-sim` (cute shaded creatures in a rule-based simulation); `particles`
  (forms made only of additive particle trails on navy, no surfaces); `frutiger-aero` (2000s candy gloss, bubbles,
  blue daytime sky and grass).
- **Poor fit:** copy-heavy messages (`kinetic-typography`, `bold-captions`), numbers and charts
  (`data-visualization`), step-by-step app walkthroughs (`product-ui`), warm or organic brands (`liquid-motion`),
  playful cartoon features (`inflated-3d`), people or characters (glass has no limbs).
- **Do not:** present it as a real company's design system or product: no real platform's status bars, system
  controls or icons, no real product or company names or logos; a panel is generic and its labels invented. Do not
  reuse the demo's "Liquid / Glass" lockup as a film's title or wordmark: the phrase names a real platform's
  interface material. Do not give the glass an opaque fill or an outline, place it over the dark ground, cut
  between shapes, or swap the night sky for a light or warm background.

## Technical notes
- `render.json` is `{ "gpu": "metal" }`: ANGLE on Metal; one worker renders the 10 s film's 300 frames in about 10 s
  on an Apple M2 (launch included). Without GPU flags (SwiftShader, the default off macOS) 10 s takes about 2–2.5
  minutes. `window.ready` takes about 0.8 s (the distance transform).
- Deterministic (stills byte-identical alone and after other frames): no PSNR allowance within one backend. Metal
  and SwiftShader differ by about 61 dB PSNR (same look): keep one backend per film.
- Needs WebGL2 with `EXT_color_buffer_float` (SwiftShader has it). Without it every frame is black while render.mjs
  still reports success; the only sign is the console line "half-float render targets are not available".
- Sizes hard-coded outside `W`/`H`: every row of the Composition table.
