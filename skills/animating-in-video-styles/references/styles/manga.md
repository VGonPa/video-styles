# Manga (`manga`)

A black-and-white shōnen manga page in motion: tapered G-pen ink, 45° dot screentones, speed and focus lines and sound
effects lettered as artwork on warm paper. Panels slam in, read right to left, as the camera hops between them; tension
builds to an inverted impact frame, a breakout panel and a page turn onto a splash. Loud and tense.

**Reference film:** a sprinter's 100 m final over two pages, from the blocks to a 9.87 record · `styles/manga/`

## Signature
- A warm off-white page cut into slanted panels by ink borders and paper gutters (white gutters only round the breakout
  and the inset). Each panel slams in with overshoot, a slight tilt and a camera shake as the camera hops to it in
  right-to-left, top-to-bottom order, a new panel about every 0.9 s.
- No grey: every mid-tone is a 45° dot screentone, flat in three densities or graded (in the demo: stands, track, sky,
  iris, shoe); solid blacks carry thin white-ink glints (in the demo: hair, sole, block, pistol).
- Tapered G-pen ink. Close-ups carry the heaviest ink: contours 4–9 units with 15–25 on the telling edge, a graded tone
  for form, two white-ink highlights and a tension mark such as a sweat drop or trembling strokes (in the demo: the eye
  at 1.2 s, its lash line 17 and brow 24).
- Lettering: capitals in a white oval balloon whose tail leaves the panel, a boxed caption, and one sound word drawn as
  art, black with a white halo, pulsing in time with the sound it names (in the demo: ON YOUR MARKS... at 0.62 s;
  BA-DUM in Potta One, swelling about 20 % per heartbeat, 2.22 s).
- Each panel gets the effect lines of its emotion: dread lines hanging from the top for suspense, emphasis strokes round
  a sound word, radial hairlines behind a held object; from the impact on, focus and speed lines re-inked on twos.

## Palette
| Role | Colour | In code |
|---|---|---|
| Ink: every line, solid black, tone dot and letter | `#151412` | `INK` |
| Paper page; its fibres | `#f3efe5`; `rgba(120,105,80,0.07)` | `PAPER`, `buildTextures()` |
| Panel ground under the paper texture | `#fbf9f3` | `panel()` |
| White ink: balloons, captions, halos, highlights, breakout gutters | `#fff` | `bubble()`, `sfx()`, `panel()`, `pen()` |
| Desk behind the page (where a shake or the turn uncovers it); page numbers | `#d8d2c4`; `#6d675c` | `render()`, `pageNo()` |
| Impact frame: difference with white, then saturation with grey | `#fff`, `#808080` | `page1()` |
| Page turn: shadow on the new page; flap shading; flap edge | `rgba(0,0,0,0.38)`; `rgba(60,50,35,0.30)`, `rgba(255,255,255,0.10)`, `rgba(60,50,35,0.12)`; `rgba(40,35,25,.55)` | `render()` |

- Ink, paper and white only (page numbers, desk and turn shadows excepted): shade with tone, black or white ink.

## Typography and copy
- `SFX` = Dela Gothic One (`fonts/DelaGothicOne-400.woff2`): impact and mechanical sounds, numbers in the art (in the
  demo: BANG!, WHOOSH, 9.87). `BRUSH` = Potta One (`fonts/PottaOne-400.woff2`): organic sounds (in the demo: BA-DUM).
  `LET` = Comic Neue 700 (`fonts/ComicNeue-700.woff2`): balloons, captions, page numbers; lines 1.08 × size apart.
- Glyphs: all four files are 78-character subsets (A–Z, a–z, 0–9, space, ! " # & ' ( ) , - . : ; ? — …): no accents, %, $,
  / or @ (a system face stands in) and no kana. The demo letters every sound in English.
- `sfx()` jitters each letter (y ± 6 % of size, angle ± 0.09 rad, scale ± 8 %; `o.seed`) and draws black letters with a
  white halo, or white ones rimmed in ink (`o.white`); `o.skew` leans a motion word. One word of 3–6 letters; it may
  cross art, never the frame edge. A word drawn in `contentP1()`–`contentP7()` is clipped at that panel's border; to
  break a border, draw it in `page1()` or `page2()` after the `panel()` calls, as the impact word is.
- A sound word's width on screen is (k × letters + 0.3) × size × zoom: k 0.9 in Dela Gothic One (M, W 1.1; ! 0.3, - 0.5,
  digits 0.85) and 0.75 in Potta One (M 0.95, W 1.1; ! 0.4, - 0.6, digits 0.6); 0.3 is the halo; `sfx()` closes each gap
  by 0.04 × size. At its widest moment: × the pulse's peak (1.2 with the demo's `beat()`, 1.35 for a true 35 % swell),
  × 1.08 for a grow-in from half size with `eBack()` (1.15 from zero), × 1.27 for an impact word dropping from 1.5×
  (first frame), + 0.3 × size if skewed.
  Centre it in its room (Other formats): its panel's borders in a hold (their ink reaches 3 × zoom inside the polygon),
  the frame on a page shot.
- `bubble()` takes rx, ry and hand-broken lines (Comic Neue capitals about 0.61 × size). Minimum that fits: oval rx =
  0.6 × widest line + size, ry = 0.6 × lines × size + 0.7 × size (tested on 1–3 lines); for a shout, dividing by 0.86
  oversizes it (the demo's NEW RECORD!, 342 px at 54, is 250 × 92). 1–3 words a line, at most 3 lines, capitals;
  "..." for suspense, "!" for the payoff; a shout's spikes reach 1.34 × rx.
- `caption()` draws one line (30–34 px) in a plain box you size: text + about 2 × size (THE FINAL. 100 M. is 266 px in
  340), under 25 characters; capitals for narration and the closing line; sentence case for inner voice ("Breathe.").
- Entrances: balloons pop in 0.22 s; captions fade in over 0.18 s, widening from 90 %; a pulsing word appears whole; a
  motion word slides in growing from 60 % with three ghosts; an impact word grows from half size or drops from 1.5×.
  Text leaves only with its page.

## Texture and finish
- `buildTextures()`, once in `window.ready`: `PAPERTEX` (`PAPER`, ±4.5-level noise, 260 fibres) is the page and the
  ground of every panel; `GRAIN`, four noise canvases in overlay at 0.12, swapped on twos. Fades: `fst`, `fin`.
- `TONE` patterns from `dotTile(s, r)` (45° screens): `l` (cell 10, radius 1.5), `m` (10, 2.5), `d` (10, 3.4), `f` (7,
  1.35), filled into clipped paths, in page space: dots grow with the camera (13 px apart at 1.8×), never swim.
- `gradT()` draws `TONE.g` (radius 0 → 5.4) or `TONE.gs` (0 → 3.2): light at the anchor, darkest after `len` toward
  `ang`, pitch 10 × len / 700 or / 500: fine in an iris (len 218), 12.6 units over a 980-unit panel (len 880).

## Shapes, line and figures
- `pen(x, pts, w, o)` fills a polygon along points, w wide in the middle, tapering over the first `o.a` and last `o.b`
  (default 0.25) to `o.min` (0.35); `o.col` '#fff' gives white ink; `bz()` samples a curve. Even strokes only for
  borders (6, breakouts 7–8), balloons (9), caption boxes (3.5), bursts and small props; contours 4–9, heavier on the
  shadow side (in the demo: shoe 5, its underside 9); hatching 3–4.
- Any new object: a white fill; inside its clip, a flat tone for its value and a `gradT()` ramp for its form shadow;
  solid black for dark materials with thin white glints; dashed detail (`setLineDash([7, 6])`); a tapered contour. Never
  stack two screens of near pitch: a ramp over a flat tone stays short (len under about 200 with `TONE.gs`, 140 with
  `TONE.g`); a large area takes either a flat tone or a ramp, or the dots beat into a plaid moiré.
- Figures are close-ups, never whole bodies: crop every body part with a panel border, so it reads as a close-up, never
  as a figure missing its body. The kit (`eye()`, `hair()`, `shoe()`, `pistol()`) is realistic shōnen, not big shōjo
  eyes. A sweat drop sits on the temple, between hair and eye (on the eye it reads as a tear). No face or body exists.
- Marks: `sweat()`, `burst()` (1.5× wider than tall), `sparkle()`, `ribbon()`; `focus()` wedges from 2600 px out to a
  jittered ellipse; `speed()` streaks (`streak()`) along +x of the current transform. Both reseed on twos.

## Composition and camera
- Page space is the canvas (1920 × 1080); `panel()` clips content, drawn in page coordinates, to a polygon (`P1`–`P7`).
  Margins 44, paper gutters about 22, all slanted. Reading order is right to left, then down (`P1`–`P4`). A caption
  takes a corner (top right for the opening narration), balloon tails leave the panel toward an unseen speaker, sound
  words fill the side the subject leaves empty. `P5` breaks out (a band rising about 10°); page 2 is a splash (`P6`)
  with an inset (`P7`). Crop hard, with low ground lines and one vanishing point per panel (`VP1`, `C6`).
- `camAt(K, t)` eases [t, x, y, zoom] keys (`K1`, `K2`) with `eInOut()`, clamped to the page; `applyCam()` adds
  `slamShake()`. Holds at 1.5–1.8× on one panel (P4 pushes 1.6 → 1.72), a 0.12 s snap out for the impact, a drift to
  1.08 under the breakout, page 2 easing out from 1.14 to 1.0. 9:16 and 1:1: Other formats.
- The turn sweeps left to right, as in a right-bound book: replace the two lines below in `render()` (rendered). The
  demo's sweep (fold from W + 160 to −260) is the Western variant, for a film that reads left to right.

```js
const p = eInOut(seg(t, T.turn0, T.turn1)), fx = lerp(-160, W + 260, p), tilt = -(.22 - .1 * p);
const d = [Math.sin(tilt), Math.cos(tilt)], n = [-d[1], d[0]], F = [fx, H / 2];   // the rest unchanged
```

## Motion
- Easing: `eBack()` (overshoot 2.2) for arrivals (slams 0.2 s, breakouts 0.22, balloons, sound words, burst, sparkles);
  `eOut()` for captions, slam tilt, the tape; `eInOut()` for camera, turn, the fade-out, pupil, sweat drop.
- A slam starts at `o.s0` (1.22; breakouts 1.3–1.35) and tilt `o.rot` (±0.04–0.08); `slamShake()` follows 0.12 s later,
  a decaying sine cut at 0.45 s (under 0.2 units): 6–9 units per panel, 26 impact, 16 breakout, 12 splash reveal. On
  twos (`STEP` 15, `stepIx()`): effect lines, burst outline, dust, trembling marks, jitter, grain; the rest at 30 fps.
- The impact: one white frame at `T.bang`, then focus lines and the word on an inverted frame until `T.inv1`; the word
  then swells 15 % until the breakout covers it. Put `T.bang` between frames (3.75, 1.85) or start the drop at 1.3×: on
  a frame boundary the flash shows the word at 1.5×, wider than the frame.
- Ambient (may continue in the final hold): effect lines re-inked in place on twos (each step draws a new seed, so they
  boil rather than travel), an idle flutter, bob or wobble on something that has arrived, grain, a slow camera drift.
  Action (must have stopped): anything still flying, scaling, sliding or shaking, and the debris it sheds. Speed lines
  scrolled with one fixed seed travel: stop them before the hold (in the demo: tape flutter and ROAAAR's wobble are
  ambient, confetti is action). Never: colour, grey fills, blur, cross-fades between shots, drifting lettering.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.95 | Fade in with the camera at 1.8× on the top-right panel; P1 slams 0.25 (stands, track to a vanishing point); caption 0.43; ON YOUR MARKS... 0.62 | `fst`, `K1`, `T.p1`, `contentP1()`, `bubble()` |
| 0.95–2.35 | Pan right to left; P2 slams 1.2: eye close-up, sweat drop from 1.35 sliding 1 s, pupil tightening 1.45–2.0, Breathe. 1.45 | `contentP2()`, `eye()`, `hair()`, `sweat()` |
| 1.9–2.8 | Camera to P3 (1.5×); P3 slams 2.02: shoe in the block, dread lines; BA-DUM pulses at 2.22 and 2.66 | `contentP3()`, `shoe()`, `T.beat1`, `T.beat2` |
| 2.8–3.64 | Pan right to left to P4; P4 slams 2.98, SET... 3.2, slow push, trembling marks from 3.28 | `contentP4()`, `pistol()`, `T.b4` |
| 3.64–5.35 | Snap out; BANG! 3.75: white frame, focus lines, page inverted to 4.1; breakout P5 4.2: runner, speed lines, dust, WHOOSH 4.32 | `page1()`, `T.bang`, `contentP5()`, `speed()` |
| 5.35–6.05 | Page turn (the demo's Western sweep) | `render()`, `T.turn0`, `T.turn1` |
| 6.05–8.65 | Splash under boiling focus lines; SNAP! 6.22 (burst, tape halves fly, confetti); ROAAAR 6.57; inset 7.1 (9.87); NEW RECORD! 7.5; arrow banner 8.3 (replace it with the closing caption below; see Do not) | `contentP6()`, `contentP7()`, `T.snap`, `T.cont` |
| 9.25–10 | Fade to the paper; the camera eased out until 9.2 | `fin`, `K2` |

- A panel beat: camera move (0.3–0.35 s), slam on arrival, one action and one line or sound, about 0.5 s to read. The
  reusable arc: a tension run-up on the grid (narration caption, close-up with a tension mark, pulsing sound word,
  countdown balloon), one impact frame, a breakout, a turn onto a splash reveal, then the optional inset and caption.
- KEYS for contact_sheet.sh: 0.9, 1.9, 2.45 (the pulse's peak), 3.5, 3.9, 4.9, 5.7, 6.45, 9.0.
- The demo's ending holds 18 frames (8.667–9.25, against the same frame with every action finished) while confetti fall
  through the fade. Tested fix, settled 8.200–9.233 (32 frames, also 9:16 and 1:1); `K2` drifts to the end:

```js
// T: cont 8.0 (was 8.3)
const K2 = [[5.4, 960, 500, 1.14], [6.1, 960, 500, 1.14], [10, 960, 540, 1.0]];
caption(x, t, T.cont, 1476, 944, 370, 62, 'TO BE CONTINUED...', 34);   // page2(): replaces the whole arrow-banner block
x.save(); x.globalAlpha *= 1 - seg(d, .9, 1.3); x.translate(px, py); /* ... */   // contentP6() confetti loop
```

## Sound
- audio.py reads `events.json`, {t, k} with optional `v` (slam loudness) and `d` (seconds); fixed pans (slams seeded
  within ±0.25); a room-noise bed at 0.004; fades 0.15 s in and 0.7 s out. Kinds: `slam` (thud, paper slap), `pop`,
  `beat` (lub-dub), `drone` (low sines, rising tremolo), `bang` (crack, boom, 2.2 s tail), `whoosh`, `flip` (rustle),
  `snap`, `crowd` (a roar fading over its last 2.2 s), `beep`, `sting` (D major, 1.3 s), `chord` (G major ninth, 1.8 s).
- Cue by role: `slam` 0.12 s after each panel slam (0.1 s and `v` 1.3 for a breakout); `pop` with each oval balloon;
  `beat` with each pulse of a pulsing sound word; `drone` from the first panel to the impact (`d` = impact − start);
  `bang` on the impact frame; `whoosh` (`d` about 1) 0.1 s before the breakout's motion word; `flip` over the turn (`d`
  = its length); `snap` on the splash reveal; `crowd` from just after the reveal to the end; `beep` with the inset's
  small mechanical detail; `sting` with the payoff shout; `chord` with the closing caption; captions are silent (in the
  demo: heartbeat, gun, tape, stopwatch). `window.events` derives all times from `T` (the drone starts at a literal 0.3).
- Crashes (tested), even for a cue parked past `DUR`: `crowd` or `flip` with `d` ≤ 0, `whoosh` under a sample, and
  `drone`, `whoosh`, `flip` or `crowd` without `d`. Guard the crowd with `Math.max(2.2, DUR - T.snap - .1)` (shorter never
  reaches full level). Negative `t` and unknown kinds drop silently; check_audio passes on the bed alone: expect ~0.79.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Paper, grain, tones | `anim.html` → `buildTextures` | builds `PAPERTEX`, `GRAIN`, `TONE`; `gradT(x, ax, ay, ang, len, img)` draws a graded tone | as is |
| G-pen ink | `pen()`, `line()`, `bz()`, `poly()` | `pen(x, pts, w, o)`: taper fractions o.a, o.b; o.min; o.col | as is |
| Effect lines | `focus()`, `speed()`, `streak()`, `stepIx` | `focus(x, cx, cy, rx, ry, n, seed, o)`; `speed(x, x0, y0, w, h, n, seed, phase, o)`; seeds from `stepIx(t)` | as is |
| Lettering, balloons, captions, effects | `sfx()`, `bubble()`, `caption()`, `textLines()`, `burst()`, `sparkle()`, `sweat()`, `ribbon()` | `sfx(x, str, cx, cy, size, rot, o)`; `bubble(x, t, t0, cx, cy, rx, ry, lines, fs, tail, shout, seed)`; `caption(x, t, t0, bx, by, w, h, txt, fs)`; `burst(x, cx, cy, R, seed)`; `sparkle(x, px, py, s, rot)` | as is |
| Panels, shake | `panel()`, `slamShake`, `cen`, `P1`–`P7` | `panel(x, t, t0, P, content, o)`: o.s0, o.rot, o.dur, o.gutter, o.border | as is; new polygons |
| Camera, pages, turn | `camAt()`, `applyCam()`, `K1`, `K2`, `page1()`, `page2()`, `render()`, `pageNo()` | keys [t, x, y, zoom]; the impact block in `page1()`; the turn in `render()` | adapt: mirrored turn, closing caption |
| Close-up kit, demo scenes, cues | `eye()`, `hair()`, `shoe()`, `pistol()`, `contentP1()`–`contentP7()`, `T`, `VP1`, `PIST`, `C6`, `window.events` | local coordinates; `shoe(x, o)` with o.leg | replace (adapt the kit) |
| Synth | `audio.py` → `thud` | kinds and fields in Sound | as is; set DUR |

## Adapting
- **Style vs demo plot:** the Signature's kit plus the reusable arc in Film grammar; the inset and the closing caption
  are optional (Shorter gives the drop order). The race is plot.
- **New subject:** write new `contentP1()`–`contentP7()` in page coordinates on the context they receive (`x`, a page
  buffer, not `ctx`), then `T`, `K1`, `K2`, the cues. `page1()` draws the impact word ('BANG!', 330 px) and calls
  `panel()` for P1–P4; `slamShake()` lists one [T key, amplitude] pair per slam: change all three with the panels.
  Shape-dependent (hourglass stand-in): the pulsing word's place, the subject's size in the band (a 480-unit stand-in
  fitted at 0.72 scale), the dust's start, `o.leg`, and in 9:16 a subject under 440 beside a pulsing word.
- **Length:** add panels at about 0.9–1 s each; a page holds 4–6 plus a breakout. A third page needs a page3 function and
  a second turn in `render()`, which has two buffers (untested). Shake and boil tire after about six panels: give quiet
  panels no shake. Set `DUR` in audio.py and in anim.html (it sets the crowd's length) to the same value.
- **Shorter:** drop panel visits rather than shrink beats. Minimums: fade-in 0.25 s; slam 0.2 (shake to its start +
  0.57); balloon 0.22; caption 0.18; camera move 0.3–0.35; impact 0.45; turn 0.6; a splash's flying pieces settle 0.7 s
  after the snap. The opening panel shows paper, borders, tone, ink, caption and balloon 0.6 s after the fade-in; effect
  lines and a sound word come with the next panel, so under about 5 s give the opening panel its own, to show the whole
  signature by 1.5 s. Drop the middle grid visits first (close-ups between the opening and the trigger panel), then the
  closing caption, then the inset; keep opening, trigger, impact and breakout (in the demo: drop the shoe, then the eye).
  A dropped visit's panel draws complete from frame 0 (negative `T`, cues dropped); boil, flutter, bob stay on film time.

```js
// any re-timing: eye() seg(t, T.sweat + .1, T.sweat + .65); contentP2() jitter t > T.sweat + .25, tension marks t > T.sweat + .35;
// contentP6() both seg(t, 6, T.snap) -> seg(t, T.turn1 - .05, T.snap); events() drone { t: T.p1 + .05, d: T.bang - T.p1 - .05 }
// 6 s (P2, P3 drawn complete, no closing caption); mirrored turn; confetti fade seg(d, .5, .8); DUR 6 in both files
const T = { p1: .25, b1: .62, p2: -1, sweat: -1, p3: -1, beat1: -2, beat2: -1.5, p4: 1.2, b4: 1.4, bang: 1.85, inv1: 2.2,
  p5: 2.3, whoosh: 2.42, turn0: 3.0, turn1: 3.6, snap: 3.75, p7: 4.25, b7: 4.55, cont: 99, fade0: 5.7, fade1: 6.0 };
const K1 = [[0, 1330, 290, 1.8], [.9, 1330, 290, 1.8], [1.25, 380, 780, 1.6], [1.74, 380, 760, 1.72], [1.86, 960, 540, 1.0],
  [2.3, 960, 540, 1.0], [3.05, 960, 555, 1.06]];
const K2 = [[3.05, 960, 500, 1.14], [3.6, 960, 500, 1.14], [6, 960, 540, 1.0]];
// 4 s: as 6 s up to the breakout, which ends the film; no page 2: delete the flip, snap, crowd, beep, sting, chord cues
// T: turn0 99, turn1 99.7, snap 99.9, p7 100, b7 100, cont 100, fade0 3.7, fade1 4.0; DUR 4; K1's last key → [4, 960, 552, 1.05]
// rendered, audio checked, measured as for the ending: 6 s settled 4.833–5.700 (27 frames), 4 s 2.900–3.700 (25)
```
- **Other formats:** 9:16 and 1:1 keep the 2×2 right-to-left grid, margins 44. The vertical gutter (about 22 wide) is
  centred and leans about 3°; the horizontal one sits at 47–48 % of the height, dropping to the left. The breakout band
  crosses the full width rising about 11°, centred at 57 % (9:16) or 59 % (1:1) of the height, a quarter or two fifths
  of it thick. The splash's focal point sits at 42 % or 40 % of the height; the inset lower left, about 42 % of the
  width. Hold each panel at the zoom where the whole panel just fits: the smaller of frame width ÷ panel width and frame
  height ÷ panel height, less about 5 % (1.85–2.0 here). `camAt()` clamps to the page, so an edge panel shows a slice of
  its neighbour (P4: about a fifth of the frame), as in 16:9. Snap to 1.0 for the impact; key times follow `T`. Compose
  at scale 1 (scaling enlarges dots and ink). Rendered:

```js
// 9:16 (1080 x 1920); contentP5 origin (540, 1090), angle Math.atan2(730 - 980, 1240); pageNo at x 50 or W - 50, y H - 18
const P1 = [[562, 44], [1036, 44], [1036, 872], [518, 900]], P2 = [[44, 44], [540, 44], [496, 901], [44, 924]];
const P3 = [[518, 922], [1036, 894], [1036, 1876], [462, 1876]], P4 = [[44, 946], [496, 923], [440, 1876], [44, 1876]];
const P5 = [[-80, 980], [1160, 730], [1160, 1200], [-80, 1450]], P6 = [[44, 44], [1036, 44], [1036, 1876], [44, 1876]];
const P7 = [[70, 1072], [520, 1050], [536, 1352], [80, 1368]];   // closing caption 560, 1340, 370 x 62, 34 px
const K1 = [[0, 777, 480, 2.0], [.95, 777, 480, 2.0], [1.3, 270, 480, 2.0], [1.9, 270, 480, 2.0], [2.25, 749, 1400, 1.85],
  [2.8, 749, 1400, 1.85], [3.12, 270, 1400, 1.85], [3.64, 270, 1390, 1.95], [3.76, 540, 960, 1.0], [4.2, 540, 960, 1.0], [5.4, 540, 1000, 1.06]];
const K2 = [[5.4, 540, 940, 1.1], [6.1, 540, 940, 1.1], [10, 540, 960, 1.0]];
// 1:1 (1080 x 1080); contentP5 origin (540, 640), angle Math.atan2(320 - 540, 1240); closing caption 685, 948, 327 x 56, 30 px
const P1 = [[560, 44], [1036, 44], [1036, 500], [530, 520]], P2 = [[44, 44], [538, 44], [508, 521], [44, 540]];
const P3 = [[530, 542], [1036, 522], [1036, 1036], [490, 1036]], P4 = [[44, 562], [508, 543], [468, 1036], [44, 1036]];
const P5 = [[-80, 540], [1160, 320], [1160, 740], [-80, 960]], P6 = [[44, 44], [1036, 44], [1036, 1036], [44, 1036]];
const P7 = [[70, 620], [500, 600], [512, 880], [80, 896]];
// K1 as 9:16, holds (783, 282), (275, 282) at 2.0, (773, 784), (284, 790) at 1.9 (P4 to 2.0), page (540, 540); K2 to (540, 540) 1.0
```

  - Sizes that transfer (9:16 / 1:1): impact word 150 / 175 px, focus 300 × 420 / 360 × 300; splash focus 380 × 440 /
    400 × 280, burst radius 190 / 170, sparkles at its centre (100), (−300, −240), (330, 120) (46, 36); balloons 40–50
    px; captions 34 / 30; inset sparkles (170, −90), (−130, 110) from its object; a shout beside the inset (9:16: (745,
    1225), rx 200, ry 84, 50 px, tail (990, 1110)).
  - In a 9:16 hold at zoom z centred on page (cx, cy): screen x = (x − cx) × z + 540, screen y = (y − cy) × z + 960.
    Keep captions, balloon text and sound words in screen y 288–1440 and left of x 950 (2×, cy 480: page y 144–720); the
    bottom band shows ground or panels. Zoom for sizing: 1.85–2.0 in holds, 1.0 for the impact, 1.0–1.06 for the
    breakout, 1.1 → 1.0 for the splash. A hold's room, from the border to x 950 or the far border: about 845 px in 9:16
    (P4 780: its right border sits at screen x 830–950), 915 in 1:1 (P4 830). A page shot's: under 880 px left of x 950,
    centred near x 475 (9:16), or 990 (1:1); the impact word, centred on the frame, has 820 (9:16). Tested in 9:16: in
    P2 at 2.0×, BOOM pulsing 35 % at 76 px (834 px wide) and THWACK still at 72 (844); in P4, DONG pulsing 35 % at 76
    (777); on the splash a 6-letter impact word at 130 (855 at its overshoot); on the breakout a skewed 6-letter motion
    word at 130 (795) with its ghosts 30 units apart, not 60 (at 60 they reach x 1064). 9:16 demo, tested clear: BA-
    (800, 1135) 110 px, DUM (745, 1265) 125 px (Potta One: 536 and 698 px at the pulse), WHOOSH (430, 1000) 110 px,
    SNAP! (510, 470) 160 px, ROAAAR (700, 650) 70 px (at y 560 it overlaps SNAP!).
  - In a tall panel a close-up fills only its upper half: carry tone into the lower half (a `gradT()` ramp from mid-height
    into bare paper, hatching or a second detail) or move the group down (9:16 demo: `eye()` and the sweat drop offset
    (−80, 140), the drop at page (70, 390) → (64, 510); `hair()` at (−80, 14), cropped by the top border; a ramp from y
    520 over 420; the temple tension strokes fall outside the narrow panel).

## Boundaries
- **Distinct from:** `tonal-manga` (full-frame shots, tones laid in step by step, a yellow marker stroke; no panels,
  slams, effect lines or sound words); `comic-book` (colour dots, left to right); `comic-strip` (dry four-panel wit);
  `clear-line` (flat colour); `anime-80s` and `lofi-anime` (colour anime, no panels); `dark-comic` (noir colour).
- **Poor fit:** quiet moments (`tonal-manga`); cosy moods (`lofi-anime`); colour brands (`comic-book`, `digital-comic`);
  stories that need a whole character on screen (a presenter, a walking mascot, two faces in dialogue): tell them with
  objects, or use `comic-strip` or `clear-line`; charts (`data-visualization`); a film under about 4 s.
- **Do not:** invent pseudo-Japanese (Latin letters dressed as kana, random kana or kanji as texture). Real Japanese only
  when the user asks, checked by a reader of Japanese (ドキドキ: a racing heart; ドクン: one heavy beat), with the full
  Google Fonts files of Dela Gothic One and Potta One (OFL; the shipped subsets have no kana), subset to the characters
  used; Comic Neue has no kana, and `textLines()` cannot set vertical balloons. Do not reproduce a series' characters,
  hairstyles, emblems, title lettering or famous panels, nor the arrow-shaped "To Be Continued" end card. No colour.

## Technical notes
- No `render.json`, no `vendor/`: canvas 2D, about 0.12 s a still; deterministic (stills test at 4.9 and 5.2 s, also 9:16
  and the 6 s plan). Pages draw into `BUF1`/`BUF2` (contexts `B1`, `B2`), page 1 frozen at `T.turn0` − 0.001 in the turn.
- `caption()`, the WHOOSH ghosts and the banner assign `globalAlpha`: multiply instead if you add a page fade.
- Hard-coded to 1920 × 1080: canvas, `W`/`H`, `panel()`'s ground (fillRect −100, −100, 2200, 1300; W + 200 by H + 200 elsewhere), polygons, `VP1`, `PIST`,
  `C6`, content, `K1`/`K2`, the impact's 960/540, the banner, `pageNo()`'s 1870/1062. Unused: `TONE.fm`, `grad()`, `eIn()`.
