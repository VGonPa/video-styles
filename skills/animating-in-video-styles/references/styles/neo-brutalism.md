# Neo-Brutalism (`neo-brutalism`)

The neubrutalist look of startup websites and punchy promos as motion graphics: chunky rounded cards, buttons and
stickers with thick ink outlines and solid ink shadows on cream graph paper, flat loud colours, heavy grotesque type.
Everything behaves like a physical interface that pops, drops, stacks and sinks into its shadow when pressed.

**Reference film:** a launch spot for an invented task app: a title with a "NEW!" sticker, a slide to its board where
cards drop, reorder and tick off and a cursor presses "Ship it", a block wipe, an end card · `styles/neo-brutalism/`

## Signature
- Cream graph paper on every frame: a faint 60 px ink grid with darker dots on every fourth crossing (`buildGrid()`,
  `bg()`). The film opens on the bare paper and builds on it.
- Every element is a flat-filled box: a rounded rect, pill or polygon with a 5 px ink outline and a solid ink shadow
  10 px straight down-right, no blur, kept screen-aligned when the element tilts or scales (`box()`, `shape()`,
  `shv()`; `LW`, `SH`). In the demo: logo tile, highlight card, caption chip, then window, cards and buttons.
- A loud flat palette on ink and white: lime, pink, electric blue, sky, yellow and orange, one per element.
- Type as interface: Archivo Black display in sentence case with one line set on a slightly tilted colour highlight
  card that grows from the left (in the demo "Zero chaos." on pink, 1.0–1.45 s), Space Grotesk bold for labels.
- Stickers and pops: a slowly spinning starburst with a one-word shout (NEW! in the demo, 1.35 s) and 4-point
  sparkles; everything arrives with a hard spring overshoot (`popScale()`; the first pop at 0.2 s).

## Palette
| Role | Colour | In code |
|---|---|---|
| Paper | `#FFF6E5` | `BG` |
| Ink: outlines, shadows, text | `#111111` | `INK` |
| White: content cards, chips, outlined letters, cursor | `#FFFFFF` | `WHITE` |
| Lime: logo tile, done state, progress fill, band | `#B8FF5C` | `LIME` |
| Pink: highlight card, CTA, badge | `#FF6BCB` | `PINK` |
| Electric blue: header bar, wipe block | `#4D6BFF` | `BLUE` |
| Sky | `#8FB0FF` | `SKY` |
| Yellow: starburst, primary button, wipe block | `#FFD23F` | `YEL` |
| Orange | `#FF8A4C` | `ORNG` |
| Grid lines, grid dots | `rgba(17,17,17,0.10)`, `rgba(17,17,17,0.22)` | `buildGrid()` |
| Empty-slot outline and text | `rgba(17,17,17,.45)`, `rgba(17,17,17,.5)` | `scene2()` |

- One flat fill per element, neighbours in different brights, white for content surfaces; ink is the only dark.

## Typography and copy
- Archivo Black (`HF`; `fonts/ArchivoBlack-400-latin.woff2` and `fonts/ArchivoBlack-400-latin-ext.woff2`) for every
  display role; Space Grotesk (`GF`; `fonts/SpaceGrotesk-latin.woff2`, variable, used at 700) for labels, with tags and
  pills in capitals at 24–34 px. Ink on colour, white on the blue header. The wordmark and wipe word are outlined
  letters, white with a 7–8 px ink stroke and an ink copy 12–16 px down-right (`scene3()`, `wipeBlock()`).
- Text moves like objects: headline words drop from 140 px above, stretched 1.25 → 1 vertically, 0.18 s apart; the
  highlight line rides in from the left inside its growing card (clipped); wordmark letters rise 90 px and grow from
  0.35, 0.045 s apart; the tagline rises 90 px inside a clip. Nothing fades or types on; text leaves with its scene.
- Register: short declarative fragments with full stops; a two-beat headline (set-up line, then the punch on the
  highlight card); one plain caption sentence; one-word capital tags; a two- or three-word imperative CTA with an
  arrow; a shouted sticker word with "!"; a capitals slogan for the marquee. For a bakery: "Baked at 5." / "Gone by 9."
- Sizes and limits (measured): headline 150 px, line 1 ≤ 880 px (about 10 characters; "Your tasks." is 921 and grazes
  the starburst's overshoot), highlight line ≤ 1240 (13); caption 40 px, ≤ 1100 (50); card labels 48 px, ≤ 500 (22,
  beside a six-letter tag); button 84 px, label ≤ 320 (the arrow sits at a fixed +430); done label 76 px, ≤ 420; CTA 54
  px, ≤ 300 (arrow at +400); wordmark 200 px, ≤ 1430; sticker word 64 px, ≤ 190 (4–5 capitals); wipe word 330 px, ≤
  1200; stat numeral 140, header title 50, tagline 62; marquees 78 (Archivo Black) and 44 (Space Grotesk), any length
  (they tile). Longer copy: a smaller size, or the arrow at the label's end + 40 (tested); never a wrap.
- Glyphs: Latin and Latin Extended. The fonts have no →, ✓ or ★: draw them with `arrowGlyph()`, `checkGlyph()` and
  `starPts()`. Add new copy to the `document.fonts.load` sample string in `window.ready`.

## Texture and finish
- `buildGrid()`, once in `window.ready`: a `BG` fill, 2 px lines every `GRID` (60) px (horizontals from y 30), 9 px
  dots every fourth crossing; the canvas is two cells wider than `W` so `bg(cam)` scrolls it with the camera.
- Nothing else: no grain, blur, glow, gradient or vignette; transparency only in the grid, the dashed empty slot and
  the closing fade. The clean screen finish is what makes it read as interface.

## Shapes, line and figures
- Inside `withT()`, pass the current rotation and scale to `box()` and `shape()` as `ang` and `sc`, so the shadow
  (offset by `shv()`) still falls down-right on screen and the outline keeps its width.
- Shadow length is elevation: 10 px at rest, 14 for the largest container, 18–24 while an item falls or is lifted, 8
  for chips and the badge, 6 for sparkles and the cursor, 5 for confetti, none for parts inside a card (checkbox, tag
  chip, pill): one shadow per object. A pressed button sits on its shadow.
- Outlines 5 px (`LW`), 6 on buttons, 4 on chips, dots and confetti, 7–8 on outlined type. Icons are fat round-capped
  strokes (`arrowGlyph()` 9–14 px; `checkGlyph()` drawn on in 0.16 s). Radii 20–28; pills h/2; a tile 16 % of its side.
- Stickers: the starburst `starPts(14, 140, 108)` and badge `starPts(12, 92, 74)` carry a word turned against the
  star; `sparkle()` is a 4-point star; `cursor()` is a white arrow pointer, ink outline, tilted −8°. Interface devices,
  all boxes (in the demo, a task app): a container card with a coloured header bar, item cards with a checkbox and a
  tag chip, a dashed empty slot, a stat card (big numeral, pill, segmented bar), a button with a label and an arrow.
- A new object: rounded rects, circles and polygons seen from the front, one palette fill each, the ink outline,
  details as smaller outlined shapes or round-capped strokes, labels in ink. For one object built from several parts,
  fill every part's shadow first (`INK`, offset `SH` down-right), then draw the parts with sh 0. Separate stacked items
  (cake tiers, cards) keep one shadow each. No people in the demo or here: let objects, interface and the cursor act.

## Composition and camera
- Flat and frontal, big elements with paper between groups; everything sits square except tilts that make a sticker:
  −2.5° on a highlight card, −6° on the logo tile, 12–14° on a sticker word, ±2.2–2.4° on marquee bands.
- A title is a row: logo tile on the left, a left-aligned text block right of it (line 1, highlight card, caption
  chip), the starburst overlapping the block's top-right corner, sparkles in open corners. A working shot has two
  columns: the large container on the left, a narrow right column with the stat card above the action button; the
  cursor enters from the bottom-right corner. An end card is a centred lockup (tile + wordmark, tagline, CTA) framed
  by two tilted marquee bands running edge to edge, the badge on the wordmark's top-right corner.
- In the demo: tile (340, 520), 250 px; text from x 560 (line 1 baseline 460, card y 535, chip y 835); starburst (1640,
  250); window x 130–1090, y 120–960; stat card (1190, 160), 600 × 320; button (1190, 620), 600 × 190; lockup at y 430
  (tile 210, gap 56), tagline 620, CTA 690, marquees at y 118 and 952.
- Camera: static shots joined by one horizontal slide of exactly one frame width (`eInOut()`, 0.42 s) with a 26 px
  anticipation drift before and a damped 18 px settle after, the grid scrolling along (`render()`), and by the block
  wipe. No zoom, perspective or parallax. 9:16 and 1:1 stack the rows into columns (Adapting).

## Motion
- Easing: `spring(sec, f, z)` through `popScale(t, t0, f, z)` for every pop (f 2.6–3.2, z 5.5–7: about 35 % overshoot
  at 0.15–0.2 s); `backOut(u, s)` for growth (s 1.6–3); `eOut()`, `eOut5()` for text riding in and bands entering;
  `eInOut()` (quintic) for slides and reorders; `eIn()` for exits.
- Interface physics: a drop falls 0.26 s on u² from above the frame, tilted and with a longer shadow, then lands with
  a vertical squash to 0.88 and a small bounce (`cardState()`); a lifted item rises (shadow +14, scale 1.05), arcs 70
  px aside and slides to its new slot while the others step down; a press drops the button onto its shadow in 0.06 s,
  holds 0.14 s and springs back past rest, after a 3 px hover lift (`pressState(t, tp, tr, tHover)`); the cursor squashes
  to 0.9 while pressing. Staggers: 0.18 s words, 0.25 s drops, 0.15 s ticks, 0.045 s letters.
- Ambient, allowed through a hold: starburst spin 0.5 rad/s, sparkles 0.9–1.2, badge 0.35, marquee separators 0.8, and
  the marquee scroll (170 and 260 px/s) until its brake (`mqPos()`). Everything else is action.
- Damped motions never reach rest; taper them before a hold:

```js
// exact rest after 0.8 s (pops) and 0.6 s (bounces); the look does not change
const spring = (sec, f = 3.2, z = 5.5) => sec <= 0 ? 0 : 1 - Math.exp(-z * sec) * Math.cos(TAU * f * sec) * (1 - seg(sec, .45, .8));
const tp = s => 1 - seg(s, .3, .6);  // multiply the landing bounce, squash and tilt in cardState(), taskCard()'s checkbox
                                     // pulse, the reorder's sc and render()'s slide settle by tp(seconds since it started)
// pressState(): v = (1 - spring(s, 2.8, 6)) * (1 - seg(s, .25, .5));
```

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–1.45 | Bare paper (no fade-in); logo tile slams in turning −28° → −6° (0.2); words drop (0.5, 0.68); highlight card grows (1.0) | `T.logo`, `T.w1`, `T.hl`, `scene1()` |
| 1.35–2.3 | Starburst pops and keeps spinning; caption chip (1.65); sparkles (1.9) | `T.sticker`, `T.cap`, `T.spark` |
| 2.16–2.72 | Anticipation drift, slide one frame width to the board, settle | `T.slide`, `T.slideEnd`, `render()` |
| 2.85–4.4 | Four cards fall and land with squash, 0.25 s apart; one lifts and slides to the top (3.95) | `T.drops`, `T.shuffle`, `cardState()` |
| 4.5–4.95 | Ticks top to bottom, strike-through, counter punches 0/4 → 4/4, bar fills | `T.checks`, `taskCard()`, `progressCard()` |
| 4.95–5.64 | Cursor glides in (to 5.33), hover lift, press 5.5, release 5.64 | `cursorPath()`, `pressState()` |
| 5.64–6.3 | Button springs back lime as "Shipped!" with a drawn check; confetti from 5.52; cursor leaves 5.95–6.3 | `shipButton()`, `confetti()` |
| 6.25–7.03 | Yellow then blue block sweep right to left, "GO!" on the blue; the end card shows as they leave (6.62) | `wipe()`, `wipeBlock()` |
| 6.8–8.0 | Marquees slide in from opposite sides; tile (6.8); letters 6.98–7.25; tagline 7.45; CTA 7.7; badge 8.0 | `marquee()`, `T.endWord`, `T.cta`, `T.badge` |
| 8.3–9.6 | Second cursor presses the CTA (8.75–8.87), leaves 9.05–9.5, is removed at 9.6 | `T.cur2`, `T.press2`, `scene3()` |
| 9.15–9.94 | Marquees brake to a stop (to 9.9); fade to paper from 9.55 | `T.brake`, `T.fade` |

- A scene assembles on the paper one element every 0.15–0.35 s, performs one physical action, then leaves by the
  slide or the wipe: 2–3 s per scene. Reusable: title build, slide, drop-and-stack, lift-and-reorder, tick-off with a
  counter, the press, two-block wipe with a shouted word, end card with marquees, brake and fade. One-off demo
  content: the task app, its window chrome, task labels and tags, the stack icon (`stackIcon()`), the name and copy.
- The press is the payoff of every film: the button sinks into its shadow and springs back changed (in the demo yellow
  "Ship it" → lime "Shipped!" with a drawn check) while confetti bursts.
- Holds here are measured by drawing each frame twice, once with every action at t = 40 (after every action, before
  the beats parked at 50) while the ambient spins and the marquee scroll keep the real t, and comparing pixels. The demo
  holds 0 frames: the second cursor sits on the bottom edge until it is removed at 9.6, and the CTA and badge still
  spring when the fade starts at 9.55. Tested fix, 16:9, 9:16 and 1:1, settled from 8.733 s, 26 frames: the tapers;
  `T` cta 7.55, badge 7.8, cur2 7.65, press2 8.1, release2 8.22, brake 7.85, fade 9.6; cursor exit `seg(t, 8.35, 8.65)`
  with offsets (420, 420), not (420, 300), and no 9.6 cut-off.
- The wordmark grows with its copy, so the end card settles at the latest of: last letter + 0.8, tagline + 0.9, CTA +
  0.8, badge + 0.8, second release + 0.5, brake + 0.75, and the cursor gone; start the fade at least 0.8 s later.
- `KEYS=2.1,4.17,5.0,5.9,6.6,8.8,9.5` (title, lift, ticks, payoff, wipe, CTA press, end); fixed: `KEYS=2.1,4.17,5.0,5.9,6.6,8.15,9.0`.

## Sound
audio.py synthesizes the `events.json` cues (`t`, `k`, optional `f`, `d`, and `v`, a gain read only by `pop`, `thud`,
`press` and `release`) over a bed written at fixed times; 48 kHz stereo, `DUR` 10.0. Kinds and roles (demo values):
- `pop` (a sweep from 900·f to 320·f Hz with a click): every element popping in, `f` rising through a line (words 1,
  1.25, 1.5; letters 1.4 + 0.12 each); `swipe` (`d` s of bright noise): a card growing, an item reordering, a line
  rising; `whoosh` (`d` s of swelling noise): each slide and each half of a wipe; `thud` (low sweep): each landing (`v`
  0.9 down to 0.75; 1 for the end logo); `boing` (rising wobble): each sticker; `tick` (click): the cursor arriving.
- `press` (thump and click) and `release` (click and high pop): each press (`v` 0.6 for a secondary one); `confetti`
  (26 random high blips within 0.44 s): the burst; `chime` (C–E–G–C arpeggio): success, after the release; `check` (a
  bell note, E5, F♯5, G♯5 or B5 for `f` 0–3): each tick, `f` climbing; `chord` (a 2.6 s C major spread): the end logo
  landing; `brake` (falling sweep, 0.7 s): the bands slowing; `outro` (soft C major arpeggio): just before the fade.
- The bed: 120 BPM from 0 (kick on every beat, clap on 2 and 4, off-beat hats, an open hat each bar) and off-beat bass
  plucks over `roots` (C, C, F, G, one per bar). Both skip beats in 6.2 ≤ t < 6.8 (the wipe); the bed stops after 9.1
  (loop bound 9.2), the bass at 9.0: re-time these with any new timeline. A 0.02 s fade-in, a 0.6 s fade-out (`fo`)
  and a tanh limiter close the mix.
- Nothing is looked up by name; unknown kinds and cues outside 0–`DUR` drop silently. `window.events` emits a literal
  seven letter pops for the wordmark: emit one per letter of yours.
- What breaks it (tested): `check` with `f` above 3, a fractional `f` or no `f` (IndexError, TypeError, KeyError;
  negative values wrap silently to other notes); `whoosh` or `swipe` without `d` (KeyError) or with `d` under 1/48000 s
  (ValueError); a cue without `t`. Pans are fixed or random within ±0.8, so no field gives NaN; a big `v` saturates.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Grid paper | `anim.html` → `buildGrid`, `anim.html` → `bg` | `bg(cam)`: cam = camera x | as is |
| Box kit, transform, text | `anim.html` → `box`, `anim.html` → `shape`, `rr()`, `shv()`, `poly()`, `starPts()`, `withT()`, `txt()` | `box(x, y, w, h, r, fill, sh, ang, sc, lw)`; `shape(pts, fill, sh, ang, sc, lw)`; `withT(x, y, ang, sc, fn)`; `txt(s, x, y, font, color, align, base)` | as is |
| Easing | `anim.html` → `spring`, `popScale()`, `backOut()`, `eOut()`, `eOut5()`, `eIn()`, `eInOut()`, `seg()` | `popScale(t, t0, f, z)` | as is, tapered |
| Icons, cursor, stickers | `arrowGlyph()`, `checkGlyph()`, `cursor()`, `logoTile()`, `sparkle()`; starburst in `scene1()`, badge in `scene3()` | `checkGlyph(cx, cy, s, u, color, lw)`, u = drawn fraction; `cursor(x, y, sc)`, tip at x, y; `sparkle(x, y, s, fill, ang)` | as is; replace `stackIcon()` and the words |
| Press | `anim.html` → `pressState` | `pressState(t, tp, tr, tHover)` → d (sink, 0–`SH`), sh (shadow left) | as is |
| Confetti | `buildConfetti()`, `confetti()` | `confetti(t, t0, ox, oy)`; 46 pieces from `rng(77)` | as is |
| Wipe | `wipe()`, `wipeBlock()` | `wipeBlock(Lx, Rx, fill, label)` | adapt label, times |
| Marquee | `anim.html` → `marquee`, `mqPos()` | `marquee(t, cy, ang, h, fill, color, font, words, v, sepFill, enterFrom, t0)` | as is |
| Demo devices | `taskCard()`, `cardState()`, `progressCard()`, `shipButton()`, `cursorPath()`, `WIN`, `CARD`, `BTN`, `TASKS` | | adapt: keep the physics, replace content |
| Scenes, timeline, cues | `scene1()`, `scene2()`, `scene3()`, `S1`, `T`, `render()`, `window.events` | | replace |
| Sound | `audio.py` | kinds in Sound | as is; re-time the bed |

## Adapting
- **Style vs demo plot:** style is everything in Signature plus the fat icons and cursor, the title build, the drop,
  reorder, tick-off and press physics with elevation shown by shadow length, the slide, the two-block wipe with a
  shouted outlined word, the end card with tilted marquee bands that brake, geometric confetti, the beat and UI
  sounds. Plot is the task app's content: the window chrome (traffic-light dots, "Today", "Launch week"), the task
  labels and tags, "Ship it" and "Shipped!", the stack icon, "Stackly" and its copy. The devices themselves (container
  card with header bar, item cards, stat card with counter, button) are style. Transformations that fit: a press that
  flips a state, a counter filling, items stacking into order, a wipe to the next scene.
- **New subject:** make its things into boxes and its action into a press. Bakery: products that drop and stack (cake
  tiers), menu cards with price chips, a loaves-left counter, "Order it" → "Ordered!". Train: departures as stacked
  cards with time chips, a carriage of boxes on circle wheels, "Board". Product: a hero sticker with spec chips, "Add to
  cart". The cursor stays the viewer's hand even for physical subjects. Traps: the seven literal letter cues; `checkAt()` ticks in `slot1` order, so set `slot1` to `slot0` when
  you drop the reorder; the tagline assigns `ctx.globalAlpha = 1`, so multiply instead if you fade a scene with
  `globalAlpha`; fixed arrow positions; pops overshoot about 35 %, so leave that room (a left-anchored chip grows right).
- **Length:** add a working scene behind another slide or wipe (2.5–3 s each), more reorders or a second press; one
  pop rhythm tires after about 15 s, so vary staggers and springs, and reseed a second confetti burst. Re-time `T`, the literals in `cursorPath()` (exit 5.95–6.3) and `scene3()` (exit 9.05–9.5, removal at 9.6),
  the `outro` cue at 9.35, and in audio.py `DUR`, the bed's 9.2 and 9.1, the bass's 9.0 and one gap per wipe.
- **Shorter:** keep the tapers. There is no fade-in; the signature is complete once the starburst pops (1.35 s in the
  demo, 0.85 s in the 4 s plan); it peaks about 0.2 s later and rests at 0.8 s. Minimums: a slide 0.42 s, a drop 0.26
  plus 0.3 of squash, a press 0.5 from release to rest, the wipe 0.78; confetti needs 1.6 s (16:9) to clear, too long
  for 4 s. An end card costs about 1.5 s of assembly, 0.8 s of hold and a 0.3 s fade. Drop first the reorder, then the second cursor and the end card, then the drops and ticks (the board slides
  in done); keep the caption chip, the title's only plain sentence, to the last. Tested in 16:9 and measured in 9:16
  and 1:1 with the Other formats values (same settle times and holds):

```js
// 8 s, all three scenes; no reorder, no second cursor. Set every TASKS slot1 = slot0; the outro cue to 7.45.
Object.assign(T, { logo: .2, w1: .45, w2: .6, hl: .85, sticker: 1.15, cap: 1.4, spark: 1.55, slide: 1.9, slideEnd: 2.32,
  drops: [2.4, 2.58, 2.76, 2.94], shuffle: 50, shuffleEnd: 50, checks: [3.3, 3.45, 3.6, 3.75], cur: 3.7, curArr: 4.05,
  press: 4.2, release: 4.34, wipeIn: 4.85, wipeOut: 5.22, end: 5.3, endTile: 5.38, endWord: 5.5, tag: 5.8, cta: 5.95,
  badge: 5.65, cur2: 50, press2: 50, release2: 50, brake: 5.95, fade: 7.64 });   // DUR 8
// cursor exit seg(t, 4.6, 4.9). audio.py: DUR 8.0, bed loop bound 7.5 and stop 7.4, bass 7.3, gap 4.8-5.4. Settled 6.767 s: 26 frames.
// 4 s, title then the board's press: the board slides in already done; no confetti() call, no confetti cue.
Object.assign(T, { logo: .1, w1: .3, w2: .48, hl: .6, sticker: .85, cap: 1.05, spark: 1.15, slide: 1.5, slideEnd: 1.92,
  drops: [-5, -5, -5, -5], shuffle: -5, shuffleEnd: -4.5, checks: [-3, -3, -3, -3], cur: 1.75, curArr: 2.08, press: 2.2,
  release: 2.34, wipeIn: 50, wipeOut: 50, end: 50, endTile: 50, endWord: 50, tag: 50, cta: 50, badge: 50, cur2: 50,
  press2: 50, release2: 50, brake: 50, fade: 3.69 });   // DUR 4
// cursor exit seg(t, 2.5, 2.8); outro cue 3.45. audio.py: DUR 4.0, bed bound 3.5 and stop 3.4, bass 3.3, no gap. Settled 2.867 s: 25 frames.
// Both pass check_audio. Park dropped beats at 50 and force actions to 40. A forced time past a parked beat draws that
// beat (the end card); a beat parked exactly at the forced time draws its first frame (the CTA pressed).
```

- **Other formats:** rendered at 10 s with the fixed ending, every shot checked at its widest moment (pops at peak
  overshoot) and frame by frame for collisions. Rows become columns; the board keeps its demo coordinates inside
  scaled groups. Outlines and shadows drawn by `box()` and `shape()` stay 5 px and 10 px; strokes drawn directly (the
  header divider, the dots, the dashed slot, the bar ticks, and the `arrowGlyph()` and `checkGlyph()` widths) shrink
  with the group: divide their lineWidth by GS if they must match. 9:16, 1:1 after `//`:

```js
let GS = 1;  // add `sc *= GS;` as the first line of box() and shape()
function inGroup(g, fn) { ctx.save(); ctx.translate(g.x, g.y); ctx.scale(g.s, g.s); ctx.translate(-g.lx, -g.ly);
  const g0 = GS; GS = g.s; fn(); GS = g0; ctx.restore(); }
// groups {lx, ly} -> {x, y} at scale s; labels inside a group are set at 20 / s px or more
window and cards (130, 120) -> (108, 300) s .9    // (200, 60) s .7; header chip text 29px
stat card (1190, 160) -> (72, 1110) s .75         // (90, 700) s .62; pill text 33px
button (1190, 620) -> (560, 1140) s .75           // (600, 730) s .62
shipButton(): divide the SH added to its shadow rect, and its 6 px outline, by GS (dividing the sink p.d too: tested)
cardState(): fall from -440 instead of -220 (the group maps -220 to y -6)   // -220 is fine (y -91)
cursorPath(): p0 (1180, 2020), p1 (1000, 1600), p2 = (1560, 735) through the button group   // p0 (1180, 1180), p1 (1050, 1000)
confetti origin: the button's top centre through its group
title: tile (250, 520) 280; headline 120px from x 90, line 1 baseline 900; card at (70, 960), height 152, text baseline
  118; chip (100, 1230) at 32px; starburst (800, 470); sparkles (900, 1390) 44, (990, 830) 28, (140, 330) 34
  // tile (200, 250) 230; 112px from x 110, baseline 560; card (90, 610) 142, 110; chip (100, 850) 32px; starburst
  // (800, 240); sparkles (960, 900) 40, (990, 520) 28, (60, 420) 30
wipe(): 100 instead of the 400 px added to each block, so the word centres while the blue covers   // same
end card: marquees at y 210 and 1560; tile (540, 560) 230 above the wordmark, 190px centred, baseline 900; badge
  (830, 470); tagline baseline 1030, its clip from 950; CTA top 1100; sparkles (100, 1260) 46, (975, 1150) 36, (960,
  700) 28; second cursor (1000, 2000) -> (690, 1180)
  // marquees 100 and 975; tile (540, 290) 180; wordmark 160px, baseline 575; badge (810, 310); tagline 670, its clip
  // from 590; CTA 720; sparkles (110, 800) 40, (975, 790) 32, (930, 470) 26; cursor (1000, 1100) -> (690, 800)
```

  - The board lacks a sticker and the highlight card, and the end card the highlight card, as in 16:9. Key text stays
    in x 90–950, y 300–1440; only repeating marquee copy enters the top and caption bands (the lower marquee textures
    the caption band on the end card; elsewhere it is grid paper). Smallest text 21 px in both formats.
  - 9:16 limits: headline lines ≤ 850 px at 120 (about 11 characters); chip ≤ 696 px (it grows 35 % to the right, to x
    1037); wordmark ≤ 800 px; wipe word ≤ 750 px. 1:1 limits: chip ≤ 711 px; "Stackly" is 658 px at 160.
  - Stand-in (9:16, 10 s, a bakery): a cake dropping tier by tier, "TODAY 3/3", "Order it" → "Ordered!", "YUM!" at 260
    px. Only the hero's box depends on the subject: fit it in x 60–1020, y 300–1090. Hold 26 frames; audio passes.

## Boundaries
- **Distinct from:** `memphis`, the closest: the same loud hues, ink outlines, hard offset shadows, overshoot,
  starburst and geometric confetti, but it decorates: terrazzo, polka and hatch fills, coloured shadows, a script
  second voice, a field of squiggles that keeps bobbing. Neo-brutalism builds interface-like cards and buttons in flat
  fills on graph paper with ink-only shadows and sparse stickers; add pattern fills, coloured shadows and an ornament
  field and it reads as memphis. `product-ui` (a polished, realistic app demo with soft shadows, zooms, callouts);
  `flat-design` (long 45° shadows, no outlines); `bauhaus` (primaries, no outlines or shadows, a still poster);
  `pop-art` (Ben-Day dots, comic outlines); `isometric` (a 3D model world); `kinetic-typography` (type alone).
- **Poor fit:** serious, sad or luxurious subjects (`editorial-illustration`, `dark-documentary`, `liquid-glass`);
  dense charts (`data-visualization`); character stories (`corporate-memphis`); a real interface's demo (`product-ui`).
- **Do not:** blur or colour the shadows, add gradients, glass or gloss, soften the outlines, cross-dissolve, use slow
  eases, aimless drift or 3D turns. Do not copy a real product's interface, logo or site: invent it, as the demo does.

## Technical notes
- Canvas 2D only: no WebGL, vendored library or `render.json`. 300 frames render in about 5 s with one worker; the
  determinism test passes (the only randomness is `rng(77)` for confetti).
- Hard-coded for 1920 × 1080 besides the canvas and `W`/`H`: Composition's "In the demo" coordinates (`WIN`, `CARD`,
  `BTN`, `S1`; the logo tile, caption chip and the end card's tile and gap are literals in `scene1()` and `scene3()`),
  the sparkle positions, the paths in `cursorPath()` and `scene3()`, the tagline clip at y 540 and the 400 in `wipe()`.
  `buildGrid()` follows `W`/`H`; the marquee width `Wd` (2600) and entry offset (2400) are fixed but fit 1080 and 1920.
