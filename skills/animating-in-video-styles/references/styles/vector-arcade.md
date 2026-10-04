# Vector Arcade (`vector-arcade`)

An early-80s vector-display arcade cabinet in attract mode: thin glowing beam lines on a black tube in three
phosphors, with afterglow trails, bloom, flicker and a hand-built stroke font, after the X–Y monitor games of
1979–83 (wireframe space fields, tube webs, high-score tables). Crisp, electric, nostalgic.

**Reference film:** a warm-up dot; the invented title "ORBITAL" (its O a ringed wireframe planet) flies together
stroke by stroke and extrudes; a rush down a web; a ship splits wireframe rocks until a stray rock destroys it; GAME
OVER, high-score initials, INSERT COIN; power-off · `styles/vector-arcade/`

## Signature
- Bare black tube from frame 0; at 0.05–0.7 s a white dot swells at the title's centre with a cyan line through it
  and fades (`drawWarm()`): the power-on.
- Everything is beam line: thin white-hot strokes with a halo, bloom and a white dot at each polyline end, in three
  phosphors only, adding up where lines cross (`render()`). No fill or raster type anywhere.
- Persistence: anything that moves leaves six fading ghost copies over 0.19 s (`TRAIL`), clear on the title's
  strokes (27 in the demo), which fly in from all sides, spinning, between 0.45 and 1.8 s and land with an overshoot flash.
- Stroke-font capitals built from straight segments on a 4 × 6 grid (`G`), and a spinning wireframe object (in the
  demo, the O's planet from 0.95 s) whose see-through edges show front and back.
- At 1.8 s the letters extrude 64 px into cyan 3D depth with an overshoot and start to sway; a cyan rule, a green
  © line with a year and an invented maker written on by the beam (in the demo, "© 1981 NOVATRON") and a blinking
  "1 COIN 1 PLAY" appear (1.72–2.3 s).

## Palette
| Role | Colour | In code |
|---|---|---|
| White-blue phosphor: objects, title faces, rocks, ship, most text | `#e6eeff` | `COL`, `WHITE` |
| Cyan phosphor: depth and back edges, rings, rules, tunnel rings, the player's row, INSERT COIN, every third ship-burst dot, the second shock ring | `#56f0ff` | `COL`, `CYAN` |
| Green phosphor: scores, the table, ©, CREDITS, every fourth rock-debris dot, every third tunnel star | `#62ff93` | `COL`, `GREEN` |
| Hot centre pass and endpoint dwell | `#ffffff` | `render()` |
| Tube face under the beam; beam layer clear | `#020304`; `#000` | `render()` |
| Vignette, 0.75 of the way out → edge | `rgba(0,0,0,0.25)` → `rgba(0,0,0,0.85)` | `buildGlass()` |
| Glass reflection (elliptical, top left) | `rgba(160,190,220,0.03)` | `buildGlass()` |

- Colour is an index (`WHITE`, `CYAN`, `GREEN`) passed to `line()`; brightness is the alpha, and an alpha above 1
  reads as "hot" (an extra 12 px halo). Lines add (`'lighter'`), so crossings and stacked ghosts burn whiter.
  Never a fourth hue, a gradient fill or a tinted background.

## Typography and copy
- No font files. `text(str, x, y, sc, c, a, align, reveal)` draws glyphs from `G`: polylines on a 4 × 6 grid (y
  down), cap height 6·sc px, advance `ADV` 6 units, width `textW()` = (n·6 − 2)·sc; align 'l', 'c' or 'r'.
  `reveal` 0–1 draws the strokes in order with a hot white head: text is written by the beam, never faded or slid in.
- Glyphs: A–Z, 0–9 (zero slashed), - . : _ / ©. Any other character (lowercase, ! ? , & ') is skipped silently,
  leaving a gap: add a glyph to `G` (a list of polylines in grid units) or rephrase.
- Sizes (sc): title 34 (`TS`, 3D); GAME OVER 15; PLAYER 1, INSERT COIN 9; rows, score 7 (+0.8 for 0.18 s per kill);
  © 6.5; NEW HIGH SCORE 5.5; HI, 00 5; 1 COIN 1 PLAY 4.2; ENTER, CREDITS 4; below 3.4 caps fall under 20 px.
  Characters a line, (width / sc + 2) / 6, in 16:9 (1680 px) and 9:16 (850 px, x 100–950): sc 15: 19 and 9; 9: 31
  and 16; 7: 40 and 20; 5: 56 and 28; 4: 70 and 35. 16:9 fits about 8 glyph slots at `TS` 34 (1680 / 204 px).
- Copy is attract-mode machine talk: capitals and numbers, 1–3 words a line (title word, © year and invented maker,
  PLAYER 1, HI and score, GAME OVER, three initials, INSERT COIN); longer copy takes a smaller size or a second line.

## Texture and finish
- `render(t)` clears `BEAM` to black, then for each `TRAIL` instant (0, 0.016, 0.034, 0.056, 0.085, 0.13, 0.19 s
  back; gains 1, .36, .2, .12, .075, .045, .025) empties `OUT`, sets `GAIN` and calls `scene()` at that past time.
  The current sample is stroked four times (7 px at 0.10 a, 3.2 px at 0.42 a, 1.7 px at 0.9 a, a 0.9 px white core
  at 0.55 a), plus the hot halo and 2.6 px white endpoint squares; past samples once, 2.2 px at 0.8 a. Persistence is
  recomputed from t, never carried from an earlier frame, and adds 0.19 s to the end of every motion.
- Flicker: the whole frame's `GAIN` is 0.93–1.0 from `hash()` of the frame number, with a 0.12 dip on about one
  frame in 30. Wobble: `wob()` bends every point by up to 0.9 px from sines of position and `NOW` (scene time).
- Bloom: `BEAM` blurred into `SM` (480 × 270, `blur(7px)`) and `MD` (960 × 540, `blur(2.5px)`), both added back
  at 1.0 and 0.9 over the `#020304` face; then `GLASS` (vignette and reflection, built once by `buildGlass()`).
- Nothing else: no scanlines, shadow mask, grain, RGB split or barrel distortion; this tube draws lines, not rasters.

## Shapes, line and figures
- Every shape is points sent to the emitter: `line(pts, c, a)` (a screen-space polyline), `dot()` (a 2r-long line),
  `line3(vs, cam, c, a)` (3D points through `proj()`, camera `{ f, d, cx, cy }`, turned by `rotX`, `rotY`, `rotZ`).
  It applies `GAIN`, `wob()` and the power-off squash `POST`: drawing on a context directly skips the whole look.
- Line width belongs to the tube, not the object: a 1462 px title and a 26 px rock get the same strokes. Emphasis
  is alpha (GAME OVER 1.25, bullets 1.8, landing strokes up to 2.2), never thickness.
- Demo kit: rocks `ICO`, `OCT`, `OCT6` (`mkRock()`, `SIZE` 82, 46, 26 px) turn at 0.5–1.3 rad/s, front edges
  brighter (`drawRock()`); the ship is three segments, about 75 px long (`SHIP`), with a flickering flame and a 5 px
  recoil; the planet is 5 latitudes and 12 spinning meridians, two cyan rings, a moon dot; the web a 16-vertex,
  four-lobed ring (`webV`) repeated in depth. Death bursts an object into its own segments (drifting, spinning,
  fading over 1.6 s) with 34 dots and two shock rings to 400 px; rocks die in 10–20 dots (0.8 s) and split in two.
- A new object reads as a vector sprite when it is: an outline of straight segments with few vertices (curves as
  24–64-point polylines, as the rings and latitudes); see-through, with no hidden-line removal, fill or shading
  (depth only as brightness and perspective); one phosphor (white for things, cyan for structure and depth, green
  for numbers); lines far enough apart to stay separate at their final size, as the halo and bloom do not shrink
  (the planet's 5 latitudes and 12 meridians read at 93 px radius, but merge into a white disc at 49 px, f 580,
  where 3 and 6 read); moved by rigid turns, glides and an `eBack` pop, never deformed; burst into its own segments.
  Everything is drawn seven times a frame: keep a scene to a few hundred segments.
- No people in the demo, and none tested: tell the story with craft, objects, wireframes and words.

## Composition and camera
- 16:9: centred on x 960 but for the HUD (y 52: score right at x 360, nose-up half-size life icons from x 330 at
  y 132, HI centred, 00 at x 1560) and CREDITS (right at 1860, 1010). Title at `titleCam()` cy 430, rule, © and 1 COIN
  260, 292, 370 px below; PLAYER 1 y 330; GAME OVER 170, NEW HIGH SCORE 318, ENTER 370, rows 470 + 78 i (rank x 640,
  score right 1060, initials 1150), INSERT COIN 900.
- Cameras: the title is 3D (`titleCam()`: f 1100, d 1100, pushed to 20 by `eIn` over 0.5 s at `T.fly`); the tunnel
  rolls 0.55 rad/s and sways ±40 px (`drawTunnel()`, f 900); the game is a flat screen, rocks wrapping 150 px past
  each edge (`wrap`, `WR`), with no zoom, pan or shake.
- 9:16 and 1:1, rendered at every beat at its widest and through the power-off (1:1 after `//`). Every centred
  x 960 (title stack, PLAYER 1, HI, `drawTable()`, INSERT COIN) becomes 540. The demo's title leaves 28 % black above
  it; every format, 16:9 included, fills that with the rock field drifting dimly behind the title, as it drifts
  behind the table (16:9 cards: 28–35 % → 12–14 %, tested at 10, 8 and 6 s).

```js
canvas width="1080" height="1920"; W = 1080, H = 1920                       // 1:1: 1080 x 1080
titleCam(): f 580, cx 500, cy 700 (d unchanged)                              // f 580, cx 500, cy 420
drawTitle(): planet 3 latitudes (k < 4, la step Math.PI / 4), 6 meridians (k < 6, lo step Math.PI / 3)   // same
drawSubtitle(): rule 760 wide at cy + 150; © at cy + 180; 1 COIN at cy + 240     // same
drawWarm(): dot and line at (540, cy)                                        // same
webV() y factor 0.8 -> 1.3, also the stars' and far flash's .8; tunnel cam cx 540 + 40 sin, cy 960;
  far flash centre (540, 960)                                                // 0.85; cy 540; (540, 540)
shipDisp(): [470 + 50 * u1 + 40 * u2, 1040 - 60 * u1 - 50 * u2]  // [480 + 50 * u1 + 40 * u2, 600 - 30 * u1 - 30 * u2]
mkRock A [230, 470] [20, 34], B [880, 430] [-26, 30], C [760, 1700] [-16, 30], E [220, 1420] [24, -40], F [880, 1180] [-32, 18]
  // 1:1: A [200, 300] [30, 22], B [840, 290] [-28, 28], C [820, 860] [-36, -18], E [220, 840] [36, -22], F [960, 700] [-22, 30]
stray rock p0 [1180, 300]                                                    // [1180, 120]
SHOTS: the 'C0' shot (5.74; 4.47 in the 8 s plan) targets 'A01' (C0 is born too late)   // 1:1 keeps C0 (tested)
HUD y 300: score right at x 300, '00' at 760; lives: first icon x 330 -> 270, y 132 -> 380; PLAYER 1 y 780   // y 52; x 270, y 132; y 420
drawTable(): GAME OVER y 360; NEW HIGH SCORE 530; ENTER 582; rows 710 + 100 * i, rank x 200, score right 620,
  initials 710; INSERT COIN 1280; CREDITS right at (940, 1390)   // 140; 290; 342; 440 + 78 * i, same x; 880; (1020, 1010)
scene(): power-off centre (540, 960) in POST and in the final dot()        // (540, 540)
buildGlass(): gradient centre (540, 960), radii 300 and 1150 kept; reflection translate(340, 440)   // (540, 540); (340, 250)
window.ready: SM = mk(270, 480), MD = mk(540, 960)                          // mk(270, 270), mk(540, 540)
```
```js
// drawGame(), first line, every format: the field drifts dimly (the table's 0.1 level) behind the title
if (t < T.game - 0.05) { const pre = 0.085 * seg(t, T.title, T.title + 0.5) * (1 - seg(t, T.fly, T.fly + 0.3));
  if (pre > 0) for (const id of ['A', 'B', 'C', 'E', 'F']) drawRock(ROCKS[id], t, pre); return; }
```
- 9:16 lands: title x 35–938 over a whole sway cycle, GAME OVER x 150–930, y 360–450, table y 360–1152, INSERT
  COIN y 1280–1334: key text inside x 35–940, y 300–1334. GAME OVER stays 18 px or more below the HUD (bottom 342),
  which is still fading when it starts writing. Largest empty band from warm-up to power-off 14–18 % (end card
  16–18 %; 1:1 18 % or less); rocks carry the bottom band.
- Stand-in (9:16): BEACON, no emblem, and a 340 px-tall wireframe rocket in the ship's place; HUD, table, tunnel,
  rocks and glass held. Subject-dependent: the title's f (about 858000 / `TW`: 580 ORBITAL, 740 BEACON) and cx (500,
  510), the emblem's line count (it shrinks with f), PLAYER 1's y (above the subject: 620), the stray rock's aim
  point (the rocket's nose, 200 px above its centre), the burst's segments, the life icons (drawn from `SHIP`).

## Motion
- Easing: `eBack` overshoot for every arrival (title strokes 1.5, planet 2.0, rings 1.6, extrusion 2.2, rocks
  popping in 2); `eOut` for GAME OVER's write-on, the rule and expanding rings (other text writes on at a constant
  beam speed, `reveal` = `seg()`); `eIn` for the camera push; the power-off squashes to a line with `eOut` and to a
  dot with `eIn` to the power 0.6; `eInOut` for ship glides, 0.2 s aiming turns and the sway's ramp. Smooth 30 fps.
- Strokes animate in: the title's segments (27 in the demo) 0.036 s apart, each flying 0.42 s from 500–1200 px,
  spinning ±3.5 rad, z ±450, landing with a 0.3 s flash; text is written by `reveal`.
- Blinks are hard square waves from Math.floor(t × rate) % 2: 1 COIN 1 PLAY 4 toggles a second (dims to 0.45),
  PLAYER 1 6.5, the initials cursor 7, the confirmed row 8 (×1.9), INSERT COIN 2.6, the last life 12. Persistence
  softens each switch-off for 0.19 s.
- Ambient, allowed through holds: the title's sway (yaw 0.05 ± 0.16 rad, pitch ±0.07), planet spin and moon,
  drifting rocks, flicker, wobble, INSERT COIN and the confirmed row's flash, which loops until the power-off like
  INSERT COIN, so holds are measured with it running. It is the only hot blink (1.9 crosses a > 1); for a quieter
  end card set the 8 in its `fl` line to 2.6 (tested: same hold). Actions: anything arriving, drawing on or ramping.
- Never: thick lines, fills, motion blur (persistence is the blur), dissolves, hard cuts, shake, eased blinks.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0.05–0.7 | Warm-up dot and cyan line at the title's centre, fading 0.35–0.7 | `drawWarm()` |
| 0.45–1.81 | 27 title strokes fly in and land with a flash, 0.036 s apart; from 0.95 the O grows into the spinning planet (rings, moon from 1.2) | `TSEGS`, `segLand`, `drawTitle()`, `T.title`, `T.planet` |
| 1.72–2.4 | Rule, © line written on, 1 COIN 1 PLAY blinking; letters extrude from 1.8, the sway ramps in | `drawSubtitle()`, `T.sub`, `T.extrude`, `titleRot()` |
| 2.72–3.27 | The title rushes at the camera, brightening, and is gone | `titleCam()`, `T.fly` |
| 2.82–3.87 | Web tunnel rushes past, rolling; three white rings flash open at its end (3.52–3.87) | `drawTunnel()`, `tunnelZ()`, `T.tunnel` |
| 3.82–4.48 | Rocks pop in, HUD fades on, PLAYER 1 blinks | `drawGame()`, `T.game`, `T.player` |
| 4.0–6.04 | Two thrust glides; ten shots split rocks (20, 50, 100 points), the score rolls | `shipDisp()`, `SHOTS`, `kill()`, `scoreAt()` |
| 6.12–7.72 | A stray rock hits the ship: segments, dots, shock rings | `drawGame()`, `TC`, `T.crash` |
| 6.72–7.27 | GAME OVER written on; HUD out; rocks dim to 0.1 by 7.22 | `drawTable()`, `T.over` |
| 7.22–7.86 | NEW HIGH SCORE, ENTER YOUR INITIALS, five rows written on | `T.table`, `TABLE` |
| 7.55–9.35 | Initials cycle into ACE (9.04), then the row flashes; INSERT COIN blinks and CREDITS 0 from 8.35 | `initStep()`, `CYC`, `T.init`, `T.coin` |
| 9.35–9.95 | Power-off: squash to a line (0.22 s), then to a dot (to 9.75), the dot fades 9.8–9.95 | `scene()`, `T.off` |

- Scenes hand over by a beam event, never a cut (push, tunnel flash, pop-in, burst, GAME OVER over the dimming
  field, power-off); beats run 0.6–1.4 s. Every beat is reusable; ORBITAL, its planet, NOVATRON, the rocks' rules
  and ACE are one-off.
- A hold starts 0.19 s after the last action ends. The demo's ending is too short: the confirm lands at 9.04, its
  trail clears at 9.23, the power-off starts at 9.35: the final state holds 4 frames (0.13 s). Its title card holds
  2.6–2.7 (4 frames) before the push; it reads from 1.8 s, while it settles.
- Tested 10 s fix (16:9, 9:16, 1:1): `T.table` 7.05, `T.init` 7.35, `T.coin` 7.9, `CYC` ['ZA', 'BC', 'DE'], the 0.24
  in `initStep()` → 0.2. Settled 8.50–9.33 s (26 frames, 0.87 s), so a longer `CYC` breaks it; audio.py unchanged.
- KEYS for contact_sheet.sh: 1.3 (strokes and trails), 2.5 (title), 3.3 (tunnel), 4.6 (play), 6.3 (burst), 8.1
  (initials), 9.25 (end card; 9.0 after the fix), 9.55 (power-off line).

## Sound
audio.py reads `events.json` (a list of `{t, k}` cues, some with `v` or `d`) and synthesizes 48 kHz stereo, `DUR`
10.0, through a 0.02 s fade-in, a 0.3 s fade-out and a tanh limiter; it prints the peak. Arcade board sounds, sent by
role (`planet` for any emblem forming, `boom` with `v` by size for each small burst, `shipboom` for the main one):
- `on` (power-on thump and click), `zap` (one per landing title stroke, at least 0.045 s apart; `v` 0.7–1.0 sets
  the pitch), `planet` (rising sweep with tremolo), `swell` (220/330/440 Hz square chord, the extrusion), `warp`
  (`d`: riser and noise through push and tunnel, d = `T.game` − `T.fly` + 0.1), `flash` (noise boom, tunnel end),
  `fire` (square pew), `boom` (`v` = rock level 0, 1, 2: longer and darker for bigger rocks), `beat` (`v` 0 or 1:
  the 49/55 Hz heartbeat bass, from `T.game` + 0.2 to the crash, its gap shrinking from 0.5 to 0.24 s), `thrust`
  (`d`: rumble), `shipboom` (big boom with a falling sine), `over` (falling five-note arpeggio), `tick` (row
  written), `blip` (initials letter change), `confirm` (rising four-note chime), `coin` (two-note chirp, every 0.77
  s with the INSERT COIN blink), `off` (down-sweep and click). `blip` and `confirm` come from a loop in
  `window.events` that stops at `T.coin`, so the demo never plays `confirm` and drops the last letter's blips: change
  its `tt < T.coin` to `tt < T.off` (tested: the confirm sounds at 9.05, or 8.28 with the 10 s fix).
- No music beyond the heartbeat. Fixed times: the `bed` (60 Hz `hum` and 7800 Hz `whine`) ramps out at 9.55 (set it
  to `T.off` + 0.2), and `window.events` writes the two `thrust` cues at 3.98 and 5.23 (move them with
  `thrustOn()`). Everything else follows `T`, `TSEGS`, `BULLETS`, `BOOMS` and `initStep()`.
- No cue is looked up by name; unknown kinds are skipped. Cues outside 0–`DUR` are synthesized, then dropped, so a
  bad field there still breaks audio.py: `boom` with `v` 3 or more raises IndexError, `warp` or `thrust` without `d`
  KeyError, with `d` 0 or below ValueError (tested). Pans are random or fixed, so no NaN; any `DUR` works.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Helpers | `anim.html` → `seg` | `seg(t, a, b)`, `clamp`, `lerp`, `eOut`, `eIn`, `eInOut`, `eBack(u, s)`, `rng(seed)`, `hash(n)`, `mk(w, h)` | as is |
| Beam emitter, 3D | `anim.html` → `line`, `anim.html` → `line3` | `line(pts, c, a)`, `dot(x, y, c, a, r)` (colour `WHITE`, `CYAN`, `GREEN`; a > 1 hot); `line3(vs, cam, c, a)`, `proj(v, cam)`, `rotX`, `rotY`, `rotZ` | as is: draw everything through them |
| Stroke font | `anim.html` → `text` | `text(str, x, y, sc, c, a, align, reveal)`, `textW(s, sc)`, `G`, `ADV` | as is; add glyphs |
| Phosphor renderer | `anim.html` → `render` | `TRAIL`; `render()` strokes the current sample four times through `stroke()`; flicker, `SM`, `MD`, `GLASS` from `buildGlass()` | as is; sizes per format |
| Warm-up, power-off | `drawWarm()`, `scene()` | `T.off`; `POST` squash, final `dot()` | as is; keep `T.off` ≤ `DUR` − 0.55 |
| Stroke title, emblem, subtitle | `TSEGS`, `drawTitle()`, `titleCam()`, `titleRot()`, `drawSubtitle()` | `TS`, `TITLE`, `OGAP`, `O_C`; stagger 0.036 in the `TSEGS` block; planet R 2.75 `TS` | adapt the word and copy; replace or drop the planet |
| Tunnel | `drawTunnel()`, `webV`, `tunnelZ()`, `NS`, `TR` | | as is |
| Wireframe rocks | `ICO`, `OCT`, `OCT6`, `mkRock()`, `rockPos()`, `drawRock()` | `mkRock(id, lvl, p0, v, tb, seed)`; children `id + '0'`, `id + '1'` | as is; your solids in the same form |
| Ship, aiming | `SHIP`, `drawShip()`, `shipDisp()`, `thrustOn()`, `shipAng()`, `AIM` | glide times are literals in `shipDisp()` and `thrustOn()` | replace |
| Shots, score, bursts | `SHOTS`, `kill()`, `BULLETS`, `BOOMS`, `SCORE_EV`, `scoreAt()`, `PTS`; bursts in `drawGame()` | rows `[time, rock id]`, aim and hit computed; burst 1.6 s | adapt; shorter bursts in short films |
| HUD, table, initials, coin | `drawGame()` HUD block, `drawTable()`, `TABLE`, `initStep()`, `CYC`, `INIT`, `ME` | `FINAL` sets `TABLE` | adapt positions, copy |
| Timeline, cues | `T`, `window.events` | | replace |
| Sounds | `audio.py` → `noise_boom` | kinds in Sound; `sweep()`, `env()`, `lp()`, `band()`, `add()` | as is; `DUR`, the bed's 9.55 |

## Adapting
- **Style vs demo plot:** style is the renderer, the stroke font, three phosphors, wireframe objects, warm-up and
  power-off, the board sounds and the attract-mode grammar (a word from flying strokes, extruded; a web rush; play
  under a HUD; bursts; GAME OVER, initials, INSERT COIN). Plot: ORBITAL and its planet, NOVATRON, rocks, ship, scores,
  ACE. Transformations: strokes assembling, extrusion, the rush, splitting, a burst, initials resolving, power-off.
- **New subject:** keep renderer, font, warm-up, tunnel and power-off; rewrite the word, game objects, copy and
  `window.events`. Traps: the `TSEGS` block skips every O and `drawTitle()` puts the planet in slot 0 with a 3-unit
  gap (no emblem: `OGAP` 0, the skip removed, `T.planet` 99); `TABLE` and HI derive from `FINAL`; glide, thrust and
  stray-rock times (`shipDisp()`, `thrustOn()`, the stray-rock block's 4.55, `SHOTS`) are literals, not `T` keys. A
  shot at a rock not yet born (children appear 0.2–0.5 s after the parent's shot) is skipped, and render.mjs and
  events.mjs print `[console] bad shot <id>`: after changing rocks, ship or `SHOTS`, check for that line and for one
  `fire` cue per `SHOTS` row in events.json.
- **Length:** past 10 s spend it in play: more rocks, more `SHOTS` (one every 0.15–0.25 s), a second glide
  (untested: re-check bad-shot lines and the beat count); a held table tires after 2–3 s (a 15 s cut holding it to
  14.35 settled from 8.5, checked clean). Re-time `T`, the literals above, both `DUR` and the bed's 9.55.
- **Shorter:** to about 7 s keep every scene; shorten the title's stagger (0.036 → 0.015 s reads), the tunnel
  (0.75 s, the least tested), the initials (one letter a slot), then play (literals shifted with `T.game`; three
  shots and a glide fit 0.9 s). The floor: a burst needs 1.6 + 0.19 s to clear before the final hold, or shorten it
  (the 1.6 in `fa` to 0.9, both 1.1 in the dots' line to 0.8); `T.off` ≤ `DUR` − 0.55, or the last `seg()` has no
  length. Under 6 s cut whole beats: table and initials first (GAME OVER and INSERT COIN stay), then the tunnel, then
  play. The signature reads once the strokes land (1.16 s at stagger 0.015; the warm-up is the fade-in). A title card
  costs its build, `T.extrude` + 0.79 to settle and 0.8 s; a GAME OVER end card 0.74 + 0.8 s and the 0.55 s
  power-off. The 8 s and 6 s plans share `T` title 0.35, planet 0.55, extrude 1.05, sub 1.0, fly 1.75, tunnel 1.8,
  game 2.55, player 2.58, stagger 0.015 and the burst's 0.9 and 0.8.
  - Tested 8 s (16:9, 9:16, 1:1; 1:1 keeps C0), every scene: `DUR` 8.0; crash 4.85, over 5.3, table 5.5, init
    5.7, coin 5.95, off 7.45; every game literal 1.27 s earlier (glides 2.73–3.43 and 3.98–4.68, thrust 2.71 and
    3.96 in `thrustOn()` and the cues, stray rock 3.28, `SHOTS` 3.03 to 4.77); `CYC` ['A', 'C', 'E'], the 0.24 in
    `initStep()` 0.15. audio.py `DUR` 8.0, bed to 7.65: peak 0.717. Settled 6.533–7.433 s (28 frames, 0.93 s).
  - Tested 6 s (16:9, 9:16, 1:1): `DUR` 6.0; crash 3.45, over 3.75, table 98, init 98.5, coin 3.85, off 5.4;
    `shipDisp()` u1 over 2.73–3.43, u2 0; `thrustOn()` 2.71–3.23 and one `thrust` cue at 2.71; stray rock 2.75;
    `SHOTS` [3.0, 'A'], [3.18, 'B'], [3.42, 'A0']; GAME OVER at y 380 and INSERT COIN 640 (1:1 the same; 9:16 760
    and 1060). audio.py `DUR` 6.0, bed to 5.6: peak 0.746. Settled 4.533–5.4 s (27 frames, 0.9 s; 1:1 from 4.5).
  - Tested 4 s (16:9, 9:16, 1:1), the title sting: `DUR` 4.0; `T` title 0.4, planet 0.6, extrude 1.3, sub 1.25, off
    3.45, every other key parked at 98–99.9 in order, so `warp`'s d = `T.game` − `T.fly` + 0.1 stays positive;
    stagger 0.02; `thrustOn()` false and no `thrust` cues; stray rock 99.2; `SHOTS` [99.3, 'A']; the five base rocks'
    tb 2.5 instead of `T.game`, so the field sits in frame (largest band 14–20 %). audio.py `DUR` 4.0, bed to 3.65:
    peak 0.560. Settled 2.1–3.433 s (41 frames, 1.37 s).
- **Other formats:** in Composition and camera; the shorter plans use those values but for their end-card heights.

## Boundaries
- **Distinct from:** `oscilloscope` is one green trace of a sampled X–Y signal inside a modelled instrument
  (bezel, graticule, knobs), heard as the soundtrack; here a bare cabinet tube, three phosphors, many independent
  strokes redrawn at past instants, a stroke font, a HUD and arcade effects. `synthwave` is a raster neon world
  (magenta grid, banded sun, chrome type, scanlines, RGB split, grain); `nes-8bit` and `pixel-art` build sprites
  from pixels on a grid.
- **Poor fit:** long text (`kinetic-typography`), real data (`data-visualization`), characters who act or feel
  (`clay`, `storytime`), interface walkthroughs (`product-ui`), soft organic subjects (`watercolor-memory`).
- **Do not:** copy a real cabinet's ship outline, title lettering, playfield layout, web shapes, attract text or
  maker; keep the game, maker and scores invented (ORBITAL, NOVATRON). No fills, gradients, pixels, scanlines,
  raster fonts, a fourth colour, or lines thickened for emphasis.

## Technical notes
- No render.json, fonts, vendor folder or WebGL: Canvas 2D in anim.html alone, about 0.05–0.07 s a frame on one page.
  Byte-identical in review.md's determinism test (4.2 and 8.9 s; 16:9, 9:16, the 6 s plan): seeded `rng()` (7, 99,
  404, each rock's seed), flicker and wobble from t; audio `default_rng(36)`.
- `render()` resets composite, alpha and fill on every canvas each frame; `stroke()` assigns `globalAlpha` on `BEAM`'s
  context, which is safe because scene drawers never touch a context: fades multiply through `GAIN` and alphas.
