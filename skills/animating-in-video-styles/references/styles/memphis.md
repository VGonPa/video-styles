# Memphis (`memphis`)

The 1980s Milan design movement as motion graphics: clashing pastels and loud primaries, squiggles, zigzags and
confetti, terrazzo and dot-grid patterns, and chunky geometric solids that sit on hard offset shadows like stickers,
all bouncing in with overshoot. It borrows the movement's grammar, not any one object or designer. Loud, cheerful,
deliberately un-tasteful.

**Reference film:** an office party invite: ornaments, a terrazzo disc and a whirling pizza slice under the bouncing
title "PIZZA FRIDAY!", then a zigzag band wipes to a cream invitation card whose details pop in · `styles/memphis/`

## Signature
- A flat pastel ground with a staggered grid of soft dots (`backdrop()`), crowded by ornaments that pop in with
  overshoot and never stop bobbing: squiggle, zigzag, 4 × 4 dot grid, ring, triangle, cross, capsule, hatched dome,
  terrazzo pebble, confetti sprinkle (`ORNAMENT`; in the demo from 0.12 s).
- Terrazzo and pattern fills: the main object, built from `TEX`-filled stickers, stands on a cream terrazzo disc
  with ink specks and a dashed ring (in the demo a slice of cheese terrazzo and polka pepperoni, 0.35–1.35 s).
- Hard offset shadows and 7 px ink outlines on every solid, shadows in ink or a colour (`sticker()`, `shoutText()`).
- Bouncy type: Rubik 900 capitals, one pastel or primary per letter, falling one by one, squashing, then hopping in a
  wave, beside a tilted Shrikhand script tag (in the demo the tag pops 0.5–0.9 s; the letters land by 1.87 s).
- A confetti burst of outlined squares, dots and triangles (`popConfetti()`; in the demo at 1.05 s).

## Palette
| Role | Colour | In code |
|---|---|---|
| Ink: outlines, shadows, specks, card text | `#161616` | `PAL.ink` |
| Cream: terrazzo base, card, chip pills | `#fff8ec` | `PAL.cream` |
| First ground and its dots | `#ffd9ea`, `rgba(255,113,206,0.35)` | `PAL.roseBg`, `BACKDROP_A` |
| Second ground and its dots | `#c4eedf`, `rgba(106,123,180,0.25)` | `PAL.mintBg`, `BACKDROP_B` |
| Pastels: pink, sun, mint, violet | `#ff71ce`, `#ffce5c`, `#86ccca`, `#6a7bb4` | `PAL.pink`, `PAL.sun`, `PAL.mint`, `PAL.violet` |
| Primaries: hot pink (disc and card shadows), cobalt (title shadows, cross) | `#ff2e88`, `#2d5bff` | `PAL.hot`, `PAL.cobalt` |
| Small accents (in the demo basil; crust and chips) | `#d7ff3c`, `#ff8a3d` | `PAL.lime`, `PAL.tang` |

- The clash is the point: each ornament, letter and chip takes a different hue, pastels against hot pink and cobalt
  (`CONFETTI_HUES`). Flat colours or `TEX` tiles only, no gradients, blur or glow; shadows are solid down-right copies.

## Typography and copy
- Rubik (`SANS`; `fonts/rubik_v31_*.woff2`, Latin and Latin Extended subsets, weights 600, 800, 900 in `fonts.css`)
  and Shrikhand (`SCRIPT`, 400). Rubik 900 capitals for titles, headline and chips; 800 for small lines; Shrikhand in
  sentence case for the tag and the card's pill: the script is the second voice.
- Titles are drawn letter by letter: `bouncyWord()` (tracking −6, letters 0.07 s apart, a cobalt shadow 12 px off,
  10 px ink edge) and `cardHeadline()` (ink letters, mint shadow 10 px off, 0.055 s apart). Text pops, drops or
  scales in with overshoot; only the footer fades (`cardFooter()`).
- Widths (demo copy, measured with `g.measureText` as the code sets them): PIZZA 683 px at 220, FRIDAY! 733 at 180
  in `bouncyWord()`; "PIZZA FRIDAY!" 1195 at 158 (the card's limit); FRIDAY! 791, PIZZA 611 at 190; chips 161–327 at
  66 plus 84 of pill; footer 897 at 44; tag 638 at 104; pill 608 at 70. Measure new copy at its target size.
- Copy is a shouted announcement: a script tag of two or three words, one word per title line, a headline that fits
  the card, three one- or two-word chips for the key facts (in the demo day, time, place), one footer line, a short
  badge word. Nothing wraps: longer copy gets a smaller size or another line (as the 9:16 headline does).
- Glyphs: Latin and Latin Extended only. Add every new string to the `document.fonts.load` samples in `window.ready`:
  an unsampled Latin Extended word measured 433 px on first use and 444 px once its subset loaded (tested).

## Texture and finish
- `buildTextures()` (from `window.ready`) makes repeating `createPattern()` tiles in `TEX`, which turn and scale with
  each shape: `polkaTile(base, spot, rad)`, `hatchTile(base)` (7 px ink diagonals), `chevronTile(base, line)`,
  `terrazzo(size, base, chipHues, count, minR, maxR, seed)` (seamless 4–6-sided chips and ink specks, `seeded()`).
- `backdrop(base, dotColour)`: flat colour and a staggered dot grid (pitch 48, radius 3.2) at `WIDTH` × `HEIGHT`.
- Nothing else: no grain, paper, halftone, misregistration, vignette or bloom. The finish is clean vector print.

## Shapes, line and figures
- Every solid is a `sticker(trace, fill, { shadow, off, outline })`: the path in `shadow` (ink, offset 12 by default)
  shifted down-right, the fill, then a 7 px round ink outline (`INK_W`). Lines: `fatLine(colour, width, drop)`, a fat
  stroke over an ink copy. Paths: `wavePath()`, `sawPath()`, `lumpPath(r, lobes, wobble, offset)`, `confetto()`.
- Ornaments (`ORNAMENT`): squiggle, zigzag, triangle, ring, dome, grid, cross, capsule, pebble, sprinkle, placed by
  `layout(list, scale, first, stagger, leaveFor)` rows (kind, x, y, colour, tilt) and drawn by `drawOrnament(o, t)`.
- A new object: break it into triangles, circles, capsules, half discs and lumps; give each a flat palette colour or
  a `TEX` tile, an ink outline and a hard shadow 9–20 px down-right; details are smaller stickers or fat squiggles;
  frontal and flat, no perspective or shading (in the demo `paintSlice()`: `wedge()`, `crustBar()`, `TOPPINGS`). No
  people: the movement made objects, and figures with limbs belong to `corporate-memphis`.

## Composition and camera
- 16:9: main object on its disc left (`SLICE_AT`), type block right under the tag; the card scene centres `CARD`
  (tilted −0.025, 26 px hot shadow) with header, pill, headline, chips, footer, corner badges; ornaments at the edges.
- Collage depth only (ground, ornaments, disc, object, type, confetti, the band wipe on top); no camera move, zoom
  or parallax. 9:16 and 1:1 stack the scene: object above the title, a taller card with a two-line headline (Adapting).

## Motion
- Easing (`ease`): `back(k, pull)` for ornaments (0.45 s, with a 1.4 rad untwist), tag, pill, headline growth, chips
  (pull 3.4) and badge; `spring` for disc, main object, card and corner copy; `cubicOut` for drops; `quartOut` for
  whirls; `cubicInOut` for flips; `quadInOut` for the band. Everything overshoots; staggers 0.045–0.07 s (letters,
  ornaments), 0.27 s (chips). `jiggle(since, decay, freq, amp)` squashes each landing and never settles (Adapting).
- Ambient means a loop with no destination and may run through the hold (list in the fixed-timing block). The rain
  is weather, not debris from an action, so it keeps falling (pieces start up to 8.3 s on the rain clock, see
  Length). Bursts, drops, exits and pulses are actions. Never a cross-dissolve, cut, blur or camera move.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.2 | Fade up from the first ground | `render()` |
| 0.12–1.12 | Twelve ornaments pop in, 0.05 s apart, then bob and sway | `ACT1_ORNAMENTS`, `drawOrnament()` |
| 0.15–1.35 | Terrazzo disc springs in (to 0.95); the slice springs and whirls on (0.35–1.35) | `actOne()`, `slicePose()` |
| 0.5–1.87 | Tag pops (0.5–0.9); title lines drop letter by letter (from 0.62 and 0.95) and squash | `bouncyWord()` |
| 1.05–2.65 | Confetti burst from the slice | `popConfetti()`, `POPPER` |
| 1.7–3.75 | Letters hop in a wave; it stops dead at 3.75 | `bouncyWord()` |
| 2.15–3.25 | Slice squashes, flips about its vertical axis rising 60 px, wobbles; second burst 3.25 | `slicePose()` |
| 3.85–4.75 | Zigzag-edged band (hot, terrazzo, sun) sweeps left to right; the scene switches under it at 4.3 | `sweep()`, `stripe()` |
| 4.35–5.4 | Card springs in (to 5.05); ornaments 4.55–5.4; confetti rain from 4.4; pill 4.85–5.2 | `actTwo()`, `ACT2_ORNAMENTS`, `cardHeader()` |
| 5.05–6.3 | Headline letters drop, grow and untwist (to 6.06); corner slice whirls on (5.5–6.2); underline draws (5.95–6.3) | `cardHeadline()`, `sliceBadge()` |
| 6.15–7.6 | Chips pop 0.27 s apart (to 7.11); star badge and a burst behind the card (6.95–7.45); footer (7.2–7.6) | `cardChips()`, `CHIPS`, `freeBadge()`, `cardFooter()` |
| 7.85–8.78 | Finale: ripple through the headline, corner slice spins (8.0–8.7), chips hop (8.3–8.78) | `cardHeadline()`, `sliceBadge()`, `cardChips()` |
| 8.56–9.5 | Seven ornaments shrink away (to 9.12); card pulses from 8.75; fade to the second ground 9.1–9.5 | `exitScale()`, `actTwo()`, `render()` |

- Pattern: a scene opens by assembling (ornaments, the main solid, then type), runs one flourish (flip, burst, hop
  wave, ripple) and hands over with the band wipe. All of it is reusable; the slice, toppings and copy are demo content.
- Demo faults (pixel difference against every action forced to its end): it never settles (the card's `jiggle()` pulse
  and exits run into the fade); title lines fall through the line or tag above (0.63–1.43 s); the hop wave's cut-off
  drops letters 23 px at 3.75 s; the sprinkle at (1010, 460) touches the title from 0.8 s; the third chip grazes the
  underline at 6.8 s. Fixes in Adapting.
- `KEYS=1.75,2.8,4.3,7.6,8.45,9.0` (landed, mid-flip, band, card, finale, end); fixed timing `KEYS=1.75,2.8,4.3,7.0,7.4,8.6`.

## Sound
audio.py reads `events.json` (`{ t, k }` cues with optional `f` (default 600), `v` (default 1) and `d`) and writes
48 kHz stereo, `DUR` 9.5, through a fade (0.05 s in, last 0.5 s out, `fo`) and a tanh limiter (×0.85).
- Cue kinds: `pop` (`f` falling to 0.45 f, 0.09 s), `bloop` (rising 2.4×), `bloopdn` (falling), `thud` (low, 0.25 s),
  `tick` (40 ms), `clack` (square wave), `boing` (wobbling pitch, 0.4 s), `whoosh` (`d`, filtered noise), `confetti`
  (0.9 s crackle), `squeak` (`d`), `chime` (four notes on `f`, a major arpeggio 0.06 s apart, 1.4 s each).
- Send cues by role, as the demo does (demo times): a `pop` per ornament; `boing` 0.2 and `whoosh` 0.4 as the disc
  and main object spring and whirl on; `bloop` 0.55 for the tag; `boing` and `confetti` per burst; a `thud` per title
  letter; `bloopdn` and `whoosh` for the flip; `whoosh` 3.8 (band); `boing` 4.35 (card); a `tick` per headline letter;
  `squeak` (underline); `whoosh` 5.5 (the corner copy whirls on); `clack` and `pop` per chip; `bloop` for pill and
  footer; finale `tick`s, `pop`s and `whoosh`; a `bloopdn` per exit; `chime` 8.75, the close.
- Fixed times, not cues: the bed (124 BPM: `kick` on each beat, off-beat `hat`, square-wave `bass` over
  `line`) runs from `b0` 0.25 to the literal 8.6 (before the chime) and ducks to 0.55 for beats between 3.8 and 4.5
  (the band). Re-time both with the film, or the bed runs into the fade or ducks at nothing.
- No cue is looked up by name; unknown kinds and cues outside the buffer drop silently.
- What breaks it (tested): `whoosh` or `squeak` without `d` (KeyError), `whoosh` with `d` 0 (ValueError), `f` 0 on
  `pop`, `bloop`, `bloopdn`, `thud`, `tick` or `clack` (ZeroDivisionError), a cue without `t`, `DUR` under 0.5.
  Pans are random within ±0.35 or fixed, so no field gives NaN; a huge `v` only saturates. Any `DUR` works (6.3333
  tested). All randomness comes from one `rs` stream: adding a cue shifts later pans and noise.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Maths, easing, random | `anim.html` → `phase`, `anim.html` → `ease`, `anim.html` → `jiggle`, `anim.html` → `seeded` | `phase(t, start, end)`, `mix`, `unit`; `ease.back(k, pull)`, `ease.spring`; `jiggle(since, decay, freq, amp)` | as is, plus the taper |
| Palette | `anim.html` → `PAL` | `PAL.*`, `CONFETTI_HUES` | as is |
| Pattern tiles and grounds | `anim.html` → `buildTextures` | `TEX.*` from `polkaTile()`, `hatchTile()`, `chevronTile()`, `terrazzo()`; `backdrop(base, dotColour)` → `BACKDROP_A`, `BACKDROP_B` | as is |
| Sticker, type, lines | `anim.html` → `sticker`, `anim.html` → `shoutText`, `anim.html` → `fatLine` | `sticker(trace, fill, { shadow, off, outline })`; `shoutText(txt, x, y, size, fill, { family, weight, shadow, off, edge })`; `wavePath()`, `sawPath()`, `lumpPath()` | as is |
| Ornament field | `anim.html` → `ORNAMENT`, `anim.html` → `layout`, `drawOrnament()` | rows [kind, x, y, colour, tilt]; `layout(list, scale, first, stagger, leaveFor)`; `exitScale(t, leaveAt)` | adapt positions per format |
| Confetti | `anim.html` → `popConfetti`, `anim.html` → `confettiRain` | `popConfetti(t, t0, ox, oy)` (1.6 s); `DRIFT` (46 pieces) | as is |
| Bouncing title | `anim.html` → `bouncyWord` | `bouncyWord(t, word, centreX, baseY, size, firstAt, hues, hopAt)` | adapt copy, order, drop |
| Band wipe | `anim.html` → `sweep`, `stripe()` | travels −1700 to `WIDTH` + 1700 over 3.85–4.75 | as is (covers 9:16 and 1:1) |
| Card | `anim.html` → `CARD`, `cardHeader()`, `cardHeadline()`, `cardChips()`, `cardFooter()`, `freeBadge()` | `CHIPS` rows { label, tex, at, tilt }, `HEADLINE`, `LETTER_TILT` | adapt copy and layout |
| Main object (demo: the slice) | `paintSlice()`, `wedge()`, `crustBar()`, `TOPPINGS`, `slicePose()`, `sliceBadge()` | | replace the drawing; keep the pose |
| Timeline and cues | `actOne()`, `actTwo()`, `render()`, `window.events` | | replace |
| Sounds | `audio.py` | kinds in Sound | as is; `DUR`, bed end and duck |

## Adapting
- **Style vs demo plot:** style is the grammar above: one clashing hue per element and coloured hard shadows (`PAL`);
  squiggles, zigzags and confetti; terrazzo and grid patterns (`TEX`, the dotted ground); solids through `sticker()`;
  chunky Rubik letters against a script voice; overshoot, the band wipe, synth pops and bed. Plot is replaced (in
  the demo: pizza, office party, copy). Transformations: an object flipping or whirling on, a band wipe, a card building.
- **New subject:** draw it like `paintSlice()` from stickers and tiles inside its local box (x ±240, y −262 to 270),
  which the burst origin (`SLICE_AT`.y − 260), the 60 px flip rise and the corner copy `sliceBadge()` assume; keep
  `slicePose()`. Taller at full size, it hits the tag in 9:16 and 1:1 and its corner copy meets the 16:9 frame top (an
  804 px cone, fixed at 0.66). Times are literals in each drawer and `window.events`; `LETTER_TILT` has 13 entries.
- **Fixed timing (tested, 9.5 s, all formats):** taper `jiggle()` and the hop wave, land the title bottom-up (a line
  falling through text on screen is the demo's fault), move the 16:9 type 30 px right, lower the chip row, and run the
  card scene 1.25× faster. Settled 8.2 s, held 0.9 s, fade 9.1–9.5; bed end 7.75; peak 0.637.

```js
// jiggle(): multiply by (1 - phase(since, 0.15, 0.4))  -> exactly 0 from 0.4 s; the squash looks the same
// bouncyWord(): hop *= 1 - phase(t, 3.5, 3.75)
// actOne(): the lower title line lands first (firstAt 0.62), the upper at 0.95; the tag phase(t, 1.3, 1.7).
//   16:9: both lines centred on x 1430, the tag at (1420, 295). Cues: a thud per letter at firstAt + 0.36 + 0.07 n
//   (demo f: lower line 170 + 10 n, upper 150 + 12 n), the tag's bloop at 1.35
// cardChips(): row = 190
const KNOTS = [[0, 0], [4.35, 4.35], [8.2, 9.15]];           // [film s, demo s]; actions only
function lerpK(x, a, b) { const K = KNOTS; if (x <= K[0][a]) return K[0][b];
  for (let i = 1; i < K.length; i++) if (x <= K[i][a]) return K[i - 1][b] + (x - K[i - 1][a]) / (K[i][a] - K[i - 1][a]) * (K[i][b] - K[i - 1][b]);
  return K[K.length - 1][b]; }
const toDemo = t => lerpK(t, 0, 1), fromDemo = t => lerpK(t, 1, 0);
let TF = 0, FORCE = false;                                     // film time; FORCE: every action at its end state
// render(t): TF = t; scenes get FORCE ? 99 : toDemo(t); the fade stays on t.
// Ambient, on TF: the bob and sway in drawOrnament(), the disc's 0.15 * t turn, the slice's 0.05 * sin(2.1 t),
//   the card's 0.006 * sin(1.8 t) (drop its phase(t, 8.6, 9) taper), the badge's floor(4 * t) tick, the corner slice's 0.12 * sin(2.3 t),
//   and confettiRain(TF + 4.3 - fromDemo(4.3)).
// Cues: t -> fromDemo(t); d -> fromDemo(t + d) - fromDemo(t). audio.py: 8.6 -> fromDemo(8.6), duck 3.8-4.5 -> mapped.
// Hold: settled from the first frame after which every FORCE false / FORCE true pair of frames is identical.
```
- **Length:** past 9.5 s add a scene behind another band wipe (4–5 s each: assemble, one flourish, hand over), more
  chips or a second flip; a settled card tires after about 3 s. `DRIFT` pieces start between 4.4 and 8.3 s and clear
  a 1080 px frame within about 4.5 s (9:16: up to 7.7 s): widen that range for a longer card scene. In audio.py set
  `DUR`, the bed's end and a duck per wipe; `line` loops to any length.
- **Shorter:** keep the fixes. 6–9.5 s keeps both scenes: drop the finale (move `chime` to the footer's landing),
  then the hop-wave lull, then badge and footer with their cues. Under 6 s end on the title scene. The signature is
  complete when the tag lands, 1.7 s (1.5 s after the 0.2 s fade-in); the card costs 3.25 s to its footer at demo
  speed, then 0.8 s of hold. Tested in 16:9, 9:16 and 1:1:

```js
// 8 s: KNOTS [[0,0],[1.9,1.9],[3.25,3.85],[4.15,4.75],[6.85,8.55]]; no finale or exits, nor their cues; chime at
//   demo 7.6; rain shift 0.6; fade (7.7, 8). Settled 6.667 (16:9, 1:1), 6.833 (9:16); held 1.03 / 0.87 s.
//   audio.py DUR 8, bed end 6.1, duck 3.22-3.9; peak 0.657.
// 6 s: KNOTS [[0,0],[2.2,2.65],[2.201,3.85],[2.95,4.75],[4.85,7.51]] (the jump skips the lull once burst 1 is
//   gone); no flip, hop wave, second burst, badge, footer, finale or exits, nor their cues; chime at demo 7.15; rain
//   shift 1.724; fade (5.7, 6). Settled 4.867, held 0.83 s. DUR 6, bed end 4.5, duck 2.2-2.74; peak 0.682.
// 4 s, title scene only: KNOTS [[0,0],[1.75,2.0],[1.85,2.15],[2.55,3.25],[2.85,3.65]]; render() always calls actOne(),
//   no sweep(), fade colour PAL.roseBg; no hop wave or second burst; drop burst 2's boing and confetti cues (demo
//   3.25) and every cue from 3.7; beats compressed (up to 1.57x in the flip), not cut: burst 1 flies until 2.65 and a
//   jump would teleport its bits; chime at demo 3.3; fade (3.7, 4). Settled 2.867, held 0.83 s. DUR 4, bed end 2.55.
// The ripple runs letter by letter, so a long headline eats the hold (demo s; without the finale use 8.55, the badge
// burst, or 7.51 without badge and footer, and 5.05 + 0.055 * (HEADLINE.length - 1) + 0.75):
if (fromDemo(Math.max(9.15, 7.85 + 0.045 * (HEADLINE.length - 1) + 0.3)) > FADE_START - 0.8) console.error('hold < 24 frames');
```
- **Other formats:** rendered with the fixed timing, every shot checked at its widest moment and frame by frame for
  shared ink (none left, except that each chip's pop overshoots its separator dot for a few frames, the 1:1 card's
  spring and final pulse brush the bottom row for 1–3 frames, and confetti bursts pass over text as in the demo: in
  9:16 and 1:1 burst 1 sprays across the tag while it lands, 1.33–1.77 s). Set the canvas `width`/`height`;
  `WIDTH`/`HEIGHT`, `backdrop()`, `DRIFT`, the band and the fade follow. 9:16 first, 1:1 after `//`; line 1 and line
  2 are the title lines (in the demo PIZZA, FRIDAY!):

```js
SLICE_AT {540, 700}, disc and object at 0.75 (also its 10 px offset, 60 px rise, burst origins)  // {540, 385}, 0.55
tag (520, 390) 104px                       // (540, 140) 72px
line 1 (500, 1240) 220px, drop 75 px instead of 180; line 2 (500, 1420) 170px   // (520, 790) 150px drop 80; (520, 950) 125px
first rows: squiggle 170,140 · pebble 990,300 · grid 880,130 · ring 560,1730 · zigzag 890,1590 · dome 160,1610 ·
  cross 990,620 · capsule 500,90 · squiggle 300,1850 · triangle 100,650 · sprinkle 930,1830 · sprinkle 990,1010
  // 140,110 · 950,330 · 930,110 · 150,900 · 930,990 · 130,620 · 960,610 · 170,330 · 910,800 · 850,230 · 170,730 · 390,1045; scale 0.8
CARD {540, 885, 960 x 1100, header 150}    // {540, 560, 960 x 790, header 130}
pill size 56 at (0, top + 78)              // 54 at (-40, top + 60); the 108 px pill and its text scale with the size
headline 190px in two lines, line 2 landing first: line 1 at -190, line 2 at 10; underline as wide as line 2,
  48 px under its baseline                 // 150px, -100 and 65, underline 38 px under
  each line centred on x -10 as in the demo; letters timed in landing order (line 2 n = 0-6, then line 1 n = 7-11,
  no slot for the space); LETTER_TILT[n] and the ripple use the same n
chips: label 62px; padding (84, 36), heights (108, 80) and radii scale by 62/66, outlines and the 10 px shadow stay;
  rest centres in card space (-160, 225), (175, 225), (0, 430), no dots   // one row, 50px (50/66), row 232, spacing 56
footer 36px at 528                         // 34px at 347
freeBadge at (-380, -570) x 0.65; sliceBadge at (420, -600) x 0.38      // (-410, -410) x 0.55; (400, -400) x 0.36
card rows: zigzag 160,140 · ring 770,110 · grid 580,140 · triangle 880,1780 · squiggle 170,1590 · cross 930,1560 ·
  pebble 390,160 · sprinkle 620,1590 · dome 420,1760 · capsule 180,1850; scale 0.85; only grid and pebble leave
  // zigzag 300,70 · ring 760,70 · violet zigzag 360,1052 (tilt 0) · squiggle 170,1030 · cross 940,1020 ·
  // pebble 530,60 · dome 540,1045 · capsule 760,1035; no grid or sprinkle; scale 0.7; only the pebble leaves
```
- 9:16: text in x 134–948, y 290–1439 (badge word highest); object and disc y 437–983; bottom band: five ornaments,
  then six plus the rain. Empty band settled 5.2 % (title), 3.9 % (card), 34 % at 0.3 s while the title assembles;
  keep the exits out or the bottom band empties. 1:1 card: 1.5 %. Widths these positions hold (demo copy plus tested
  limits): 9:16 tag up to about 750 px (the pebble at (990, 300) starts at x 910; "Grand opening", 818 px at 104, sat
  on it through the hold), title lines up to 750, headline lines up to 791 (x 134–948), the side-by-side chips up to
  317 + 230 px with 61 px between (wider: move both centres outward equally or give each chip its own row), the lone
  chip up to 386, the footer up to 734; 1:1 chip row 865 px of the card's 960 (longer: a smaller size or the 9:16
  two-row layout). Wider copy gets a smaller size, never a neighbouring ornament.

## Boundaries
- **Distinct from:** `corporate-memphis` (despite the name: flat human figures with tiny heads and noodle limbs,
  blobs and leaves, no outlines, shadows or patterns); `neo-brutalism` (the closest neighbour: the same loud hues,
  black outlines, hard offset shadows, overshoot pops, a starburst sticker and geometric confetti, but it draws UI
  (windows, task cards, buttons, a cursor) in flat fills on graph paper with black shadows only). A Memphis card stays
  Memphis through its terrazzo header, `TEX`-filled chips, coloured shadows (hot under the card, mint under the
  headline, cobalt under titles), the script pill and the bobbing ornament field around it. Drop those and it reads
  as neo-brutalism. `bauhaus` (three primaries on paper, a grid, no outlines, shadows or decoration, a frozen poster);
  `pop-art` (process-ink overprint and Ben-Day dots as shading, comic outlines, repetition; Memphis polka is a flat
  pattern fill on one solid, never tonal shading); `kawaii` (pastel chibi stickers with faces); `grainy-flat`
  (stipple-grain shading, no outlines); `risograph` (fluorescent overprint, halftone); `synthwave`, `anime-80s`,
  `vector-arcade` and `dark-comic` (the 1980s as neon, glow and sunsets; Memphis has no glow).
- **Poor fit:** serious or sad subjects (`editorial-illustration`); data and numbers (`data-visualization`,
  `infographic`); long text (`kinetic-typography`); interfaces (`product-ui`); character stories (`storytime`).
- **Do not:** copy a known Memphis piece (Sottsass's Carlton bookcase or Bacterio laminate, Du Pasquier's textile
  prints, Bedin's Super lamp, the Memphis Milano logo): invent objects from the kit instead, as the demo invents its
  slice. Do not write "Memphis" on screen or imply the group made or endorses the film. No people, gradients, glow,
  grain, halftone or perspective: they turn it into a neighbouring style.

## Technical notes
- No render.json or vendor folder: Canvas 2D, no GPU; anim.html, fonts.css and four woff2 files. The canvas is
  `stage` (context `g`); 285 frames render in about 8 s on one page. Deterministic (tested 16:9 and 9:16); textures
  come from `seeded()` in `window.ready`. The scene switch (`t < 4.3`) and fade colour (`t < 1`) are literals in `render()`.
- `paintSlice()` (the drips), `popConfetti()` and `cardFooter()` assign `globalAlpha` instead of multiplying it, so a
  scene faded with `globalAlpha` leaves them opaque: fade with the overlay fill, as `render()` does, or multiply.
