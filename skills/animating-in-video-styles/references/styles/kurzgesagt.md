# Kurzgesagt (`kurzgesagt`)

A bright, layered science-documentary look inspired by Kurzgesagt – In a Nutshell. Each beat shows one consequence
of a "what if" at scale; the camera dives into places and irises back out to the planet. Curious, cute but precise,
never grim.

**Reference film:** "What if the Moon disappeared?": the Moon bursts into sparks beside Earth; a dive to a dusk coast
where a gauge shows the tides flattening; night, a critter with a lantern; an iris out to Earth, its axis wobbling
past season icons; Earth alone under the question · `styles/kurzgesagt/`

## Signature
- A deep-space backdrop fading up from navy in 0.4 s: gradient `C.sky0` → `C.sky1`, three soft colour clouds
  (magenta, teal, violet), 320 twinkling stars whose largest are four-point sparkles, a dark vignette.
- One big outline-free planet on the centre line, rising with a small overshoot (0.2–1.6 s): ocean gradient, blobby
  continents with sandy cores, pill clouds, caps, a navy crescent lower right, a pale rim upper left, a cyan halo.
- A white rounded headline (Fredoka 600, 84 px) popping in word by word at top centre with a soft blue glow
  (0.55–1.41 s), and a small tracked-caps kicker fading up under it (1.05 s).
- A companion on a tilted orbit pops in, swells, flashes white and bursts into four-point sparks, leaving a dashed
  outline (the Moon, 0.75–2.45 s).

## Palette
| Role | Colour | In code |
|---|---|---|
| Space gradient, top and bottom (also the fades); stars | `#0a1030` `#1c1552` `#fff4d8` | `C.sky0`, `C.sky1`, `C.star` |
| Planet: ocean lit spot to rim, continents, sandy cores, shade crescent, lit rim | `#2aa3e0` `#145a9c` `#5cd07a` `#ffc94d` `rgba(12,6,58,0.5)` `rgba(200,245,255,0.35)` | `drawPlanet()`, `C.oceanD`, `C.land2`, `C.land`, `shadeCircle()` |
| Clouds; polar caps; atmosphere halo | `rgba(240,250,255,0.92)` `rgba(240,250,255,0.95)` `rgba(99,214,255,0.55)` | `CLOUD_WHITE`, `drawPlanet()`, `ATMO` |
| Moon, craters, dashed ghost | `#c7b3f5` `#8a6fcf` `rgba(199,179,245,0.8)` | `C.moon`, `C.moonD`, `ghostMoon()` |
| Cyan accent (iris rim, sparks, axis glow); flash veil | `#86e8ff` `#8fe4ff` | `C.crest`, `renderFrame()` |
| Navy (icon discs, lantern, pupils); gold (arc, readout, bracket); headline glow; kicker, warm kicker | `#27265e` `#ffd36b` `rgba(120,200,255,0.5)` `#c3cfff` `#ffd9a0` | `C.navy`, `C.gold`, `popText()`, `kicker()` |
| Nebula clouds; vignette | `196,52,150` `40,190,200` `120,70,220` `rgba(5,5,25,0.55)` | `NEB`, `VIG` |
| Coast at dusk (sky top and its night twin; water, soil, grass, hut) | `#35308c` `#060a22` `#3ab4ea` `#e0913f` `#5cd07a` `#ff7a6b` | `K`, `kc()` |
| Lantern light; critter fur and belly; icons (with cyan) | `rgba(255,214,120,0.95)` `#ff9d6c` `#ffe0c4` `#ffcb57` `#ff78ad` `#ff8a4c` | `WARM`, `drawCritter()`, `SEASONS` |

- Flat fills, gradients only for sky, ocean and halos; depth from navy crescents, additive glows and the vignette.
  Night is a palette: `K` night twins mixed by `kc(name, n)`, a navy tint (`rgba(4,6,28,…)`) sparing the lantern.

## Typography and copy
- One family, Fredoka (`FT`), two files in `fonts/` (Latin and Latin Extended subsets) declared in `fonts.css` at
  500, 600 and 700. Western and Central European Latin and °; no Greek, Cyrillic or CJK, partial Vietnamese.
- Headline, `popText()`: 600, 84 px opening, 76 coast, 72 diagram, 88 end card; sentence case, white, 28 px blue glow
  (warm at night); one line centred at x 960, y 120–160. Each word rises 0.35 em and scales with `eBack()`, capped so
  neighbours keep 60 % of the gap; on exit each shrinks to 60 % and fades in 0.3 s, 0.04 s apart. Words never wrap.
- Kicker, `kicker()`: 600, 32 px, letter-spacing 6 px, capitals, `#c3cfff` (warm `#ffd9a0` at night and on the
  diagram), 76–84 px under the headline; fades and rises 12 px over 0.4 s, leaves in 0.25 s. Diagram labels: 600,
  22–26 px, capitals, spacing 3–4 px; numbers 700, 52 px, gold, glowing.
- Voice: a calm, curious explainer. A headline is one consequence in the conditional ("The tides would flatten") or
  the question, 3–6 words; the kicker gives the reason or stakes in 2–5 words. No puns, exclamation marks or slang.
- Measured with `measureText` as `popText()` lays words out (space + 0.15 em gaps): 44.6 px a character at 88 px,
  42.5 at 84, 38.5 at 76, 36.5 at 72 ("What if the Moon disappeared?", 29 characters, is 1233 px at 84); kicker 24.5.
  16:9: one line under 1600 px (about 37 characters at 84). 9:16: lines under 820 px, about 19 characters at 84, 21
  at 76, 22 at 72 ("The tides would flatten" is 829 px at 76: two lines); kicker under 33. 1:1: under 960 px.
- Two lines: two `popText()` calls 1.12–1.18 × size apart, the second with t0 + (words in line 1) × stag and out +
  (words in line 1) × 0.04, so pops and `pop` cues run as one sentence. Longer copy is another beat; never < 64 px.

## Texture and finish
- No grain, paper or noise. Sprites built once in `buildSprites()`: `NEB` (three radial clouds on one canvas), and
  with `radialSprite()` `ATMO` (halo, 0.93–1.63 radii), `GLOW`, `WARM`, `VIG` (radii 500–1250, over every frame).
  `drawStars()` twinkles (0.55 + 0.45 sin, rates 0.8–3.0), draws the largest as `sparkle()` stars, drifts two layers.

## Shapes, line and figures
- Things have no outlines: flat fills from circles, ellipses, rounded rectangles and smooth blobs (`blobPath()`).
  Strokes are for diagrams: dashed white lines with round caps and a cyan glow, a gold arc, dashed ghosts of what is
  gone. Round forms get `shadeCircle(x, y, r, k, dark, lite)`: a translucent navy crescent on the lower right (k
  0.25–0.28) and a thin pale rim on the upper left; the light always comes from the top left.
- Planet, `drawPlanet()`: continents from `CONT` through the orthographic `project()`, clouds 1.3× faster than the
  surface, caps, shade, a bright stroke on the lit limb, `ATMO` behind; `tilt` turns the surface only.
- Landscape, `sceneCoast()`: summed-sine hills, a smooth-step slope (`groundY()`), soil with a darker band 70 px
  down, a 34 px sand crust, grass, lollipop trees, a hut (rounded box, triangle roof, round-topped door). Creature,
  `drawCritter()`: round body, paler belly, shade cut-out, big white eye with navy pupil and catch-light, blush, short
  legs, round ears, curled tail, `CS` 1.25 (150 px wide). Icons, `seasonIcon()`: navy disc, 6 px ring, one glyph.
- A new object: two or three flat palette fills (a base, a paler or darker patch), `shadeCircle()` on round parts, a
  glow only if it gives light.

## Composition and camera
- 16:9: one subject on the centre line, low enough to leave the top 260 px to the text (`PA` 960, 660, radius 270;
  `PD` 960, 610, radius 250); companions orbit or flank it symmetrically (the Moon on a 600 × 170 ellipse tilted −0.16
  rad, icons at x 470 / 1450, y 440 / 810). 2D camera, `zoomAbout()`: dive 1 → 10× with `eIn` into a point inside the
  subject; iris push 1 → 1.25× while a circle closes onto `PD`; stars drift.
- 9:16 and 1:1, every value rendered (stills of each beat at its widest moment and the end card):

```js
// 9:16 — canvas width="1080" height="1920"; W = 1080; H = 1920; x 960 → W / 2 in kicker() and every popText()
// NEB rows (x, y, radius): [160, 450, 700] [980, 250, 650] [540, 1950, 900]
// space: PA = { x: 540, y: 1150, r: 270 }; lerp(2450, PA.y, …); orbitPos(th, 400, 130, -0.16, PA.x, py - 40);
//   dive zoomAbout(600, 1100, …); coast zoomAbout(W / 2, H / 2, …); headline 84 px, words 4 + 1 at y 400 / 500;
//   kicker y 585
// coast: TIDE0 = 1220; groundY: x < 100 → 1480 + 8 sin(x / 90); x < 850 → lerp(1480 + 8 sin(100 / 90), 1080,
//   smooth((x - 100) / 750)); else 1080 - 14 sin((x - 850) / 160); foam search lo 100, hi 850
//   sky gradient to 1140; drawStars maxY 960; ghostMoon(200, 780, 64, …); mountains base 1060; hills 1120
//   water to x 800 (both 1400s); highlights [[60, 40, 200], [330, 80, 120], [180, 130, 220], [30, 190, 140]]
//   gx = 130; post roundRect(gx - 11, 1040, 22, 420, 8); stripes y 1060 while < 1440; grass 1290 → 700 (all eight)
//   after the soilD fill: a stratum in kc('trunk', n), top max(surface + 300, 1660) + 22 sin(x / 120 + 1), and twelve
//   flat stones (ellipse 1.5 r × r, r 9–20): kc('soil', n) inside the soilD band, kc('soilD', n) inside the stratum
//   wx = 725; hx = 975; TREES = [[760, 1.0], [860, 0.78]]; CRITTER_X lerp(980, 640, …); 1790 → 980 in critterPose()
//   and twice in the step loop of window.events; headlines 76 px at y 400 / 490 (words 2 + 2, 3 + 2); kickers y 570
// earth: PD = { x: 540, y: 1000, r: 250 }; endK target y 1030; orbit ellipse 470 × 130; SEASONS x 200 / 880,
//   y 700 / 1300; headline 72 px at 400 / 485 (2 + 2), kicker 560; end title 88 px at 400 / 505 (4 + 1);
//   'EARTH, ALONE' y 1380
// 1:1 — canvas 1080 × 1080, W = 1080; x and coast zoom as 9:16; NEB [180, 260, 600] [960, 160, 560] [540, 1100, 800]
// space: PA 540, 660, r 230; rise from 1450; orbit 420 × 130; dive (600, 610); headline 84 px, words 4 + 1, at
//   115 / 210; kicker 285
// coast: 16:9 heights and gauge; groundY breakpoints 250 and 850 (smooth over 600), foam search 250–850; water to 900;
//   grass, highlights, gx, TREES, hx, critter path and its 1790s as 9:16; wx = 742; ghostMoon(170, 420, …);
//   tides headline one line at 140 (kicker 220 as 16:9); night headline 120 / 205 (3 + 2), kicker 275
// earth: PD 540, 600, r 230; endK target 630; orbit 470 × 130; icons x 190 / 890, y 430 / 800; headline one line at
//   110, kicker 185; end title 88 px at 110 / 210 (4 + 1); 'EARTH, ALONE' y 965
```
- 9:16 Signature check per shot: space (nebula, sparkles; planet whole at 270–810 × 880–1420 with crescent, rim, halo;
  Moon whole at its widest, x ≤ 995; sparks may leave the edge), dive flash, coast (gauge, slope, trees, hut whole, 23
  px from the edge), night (stars, glows, critter whole from its start), iris (critter fading with the coast, not over
  the planet), diagram (axis 645–1355, readout, icons whole at peak overshoot and shake, x 105–975), end card. Text
  stays in y 360–1395, x 175–905, clear of review.md's bands; the bottom band holds stars and nebula, or soil strata
  and stones (coast; without them the band is 94 % one fill).
- Stand-in (9:16 rocket, about 300 × 900 px, in the opening and end card): backdrop, text, transitions and coast held.
  Shape-dependent: its top at least 100 px under the kicker; the orbit clear of it where the Moon shows; the rise from
  below the frame by half its height plus glow; the subject reaching at least 60 px left of the dive target, 48 px
  right, 110 px above and 82 px below (at 10× the frame spans px / 10, (W − px) / 10, py / 10 and (H − py) / 10 around
  the target; off the rocket's axis, space showed beside the body); end card: `endK` target y 990, scale 0.85, kicker
  at 1415, so the flame clears it.

## Motion
- Easing: `eOut` (cubic) for arrivals and the coast settle, `eIn` for exits, the dive and the iris push, `eInOut` for
  tides, nightfall, the iris circle and the end move, `eBack(k, over)` for pops: 1.9 (12 % overshoot) for words, the
  Moon and the lantern lift, 1.25 (6 %) for the planet's rise, 2.2 (15 %) for icons. Smooth 30 fps, no stepping.
- Each word pops over 0.5 s, 0.09 s apart (0.06 on the end card), so five words land in 0.86 s; the kicker follows
  about 0.5 s after the headline (0.25 s at the shortest, as in the 8 s plan, where it starts before the last words
  pop); transitions take 0.65–0.7 s.
- Ambient, always running: planet spin 0.22 rad/s, star twinkle and drift, water ripple, tree sway (±3 px), lantern
  flicker (±9 %), the critter's bob, legs and lantern sway while walking, icon shake tied to the wobble.
- Never: a hard cut (every change is a dive with a cyan flash or an iris with a cyan rim), outlines on figures,
  camera shake, squash and stretch of the subject, typed-on text, a new headline over an old one.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–1.6 | Fade up from navy (0.4 s; nebula to 1.2, stars to 0.9); Earth rises from y 1560 from 0.2 and overshoots; the Moon pops onto its orbit 0.75–1.25 (behind Earth on the far side) | `veil()`, `paintSpace()`, `drawSpaceScene()`, `PA`, `orbitPos()` |
| 0.55–1.45 | Headline pops (to 1.41); kicker 1.05–1.45 | `popText()`, `kicker()` |
| 1.57–2.85 | Moon swells, whitens, shrinks (1.75–2.1); flash and 26 sparks 1.95–2.85; ghost 2.2–2.45; text leaves 2.2–2.71 | `T_VANISH`, `SPARKS`, `ghostMoon()` |
| 2.3–3.25 | Dive into Earth; cyan flash 2.72–3.25 hides the cut; coast fades in 2.85–3.0, settles to 4.0 | `zoomAbout()`, `veil()` |
| 2.95–5.42 | Tides swing ±110 px every 1.3 s, then flatten 3.55–4.95 as the gold bracket shrinks; "The tides would flatten" 3.15, kicker 3.6, both leaving from 5.0 | `tideAmp`, `tideLevel`, `sceneCoast()` |
| 5.0–7.0 | Dusk to night by 5.9 (palette pairs, stars, window glow); critter fades in 5.2, walks downhill with a lantern to 6.55, lifts it to 7.0; headline 5.3, kicker 5.8 | `kc()`, `drawCritter()`, `critterPose()`, `CRITTER_X` |
| 6.85–7.55 | Iris onto Earth with a cyan rim; the coast pushes in and fades 7.3–7.55 | `renderFrame()` |
| 7.35–8.4 | Axis arrow, vertical, gold arc, live tilt readout; wobble grows to ±22° (0.8 s period) | `sceneEarth()`, `wobAmp`, `tiltDeg` |
| 7.45–8.45 | "Earth's axis would wobble", kicker 7.95; four icons pop 7.7–8.0 and shake | `SEASONS`, `seasonIcon()` |
| 8.5–10 | Diagram leaves (to 8.89), wobble dies (to 9.1), Earth drops; end card: question, empty orbit 8.8–9.3, "EARTH, ALONE" 9.1; fade to navy 9.65–10 | `endK`, `popText()`, `kicker()`, `veil()` |

- A beat runs about 2 s: headline, kicker, the change under them, both leaving as the transition starts; dives (space
  to place) alternate with irises (place to space). Reusable: opening, headline and kicker, vanish into sparks,
  diagrams, nightfall by palette pairs, dive, iris, end card. One-off: Moon, tides, critter, wobble, seasons, copy.
- The demo settles at 9.5 s and fades at 9.65: a 0.15 s hold (measured as under Shorter); the 10 s plan fixes it.
- KEYS for contact_sheet.sh: 2.2 (sparks), 2.95 (flash over the dive), 4.6 (tides nearly flat), 7.2 (iris half
  closed, rim visible, lantern up inside), 8.1 (wobble and icons), 9.55 (end card); the thirds miss vanish and wobble.

## Sound
audio.py reads `events.json`, cues with a kind `k` and a time `t`, and synthesizes 48 kHz stereo with NumPy, `DUR`
10.0. Unknown kinds are skipped; no cue is looked up by name, so it runs with any subset, even none.
- At fixed times, not from cues: the `bed` pad (D major add9, `tone()` over all of `DUR`, attack 1.2 s, release
  1.0 s: it follows `DUR`) with a 45 % night dip from 5.0 s, back by 7.2 s; the `sea` bed 2.85–7.3 s, quietening from
  3.55 s over 1.4 s with the tides; crickets from 5.45 s until 7.0 s (seeded `rs`).
- Cues: `pop` (`f` 820, 910, 1000 by word) per headline word, sent by the words helper in window.events with its
  headline's t0 and stag; `blip` (`f`) the Moon's pop; `rise` and `land` an arrival and its landing (`land` also as an
  iris closes); `suck` before the vanish and as the diagram clears; `shimmer` at the burst; `whoosh` (`d`); `splash`
  at the coast; `wave` (`v`, tidal range 1 to 0.3) per high tide, from a loop over the tidal range; `dusk`; `step` per
  footstep, from a loop over the critter's path; `tinkle`; `wobble` (`d` 1.4); `bloop` (`f` 300–480) per icon;
  `chord`, five notes and a low D, 1.4 s each.
- What breaks it (tested): `pop`, `blip` or `bloop` without `f`, `whoosh` without `d`, `wave` without `v`: KeyError;
  `f` 0: ZeroDivisionError; `whoosh` with `d` ≤ 0: ValueError. Pans are fixed or random within ±0.6, so no field
  can make a NaN; a large `v` only saturates the limiter. Cues before 0 or past `DUR` drop silently. Master: 0.2 s
  fade-in, 0.5 s fade-out (`fo`), tanh limiter, so send `chord` at least 1.4 s before the end.
- A new scene sends the words helper per headline, `whoosh` per dive or iris with `d` about its length (0.75 for the
  0.65 s dive, 0.7 for the 0.7 s iris), `land` as an iris closes, `chord` with the end card; move or delete the `bed`
  dip, `sea` and crickets, or they duck and chirp at the demo's times, even after a shorter film's closing chord.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Maths and easing | `anim.html` → `seg`, `anim.html` → `eBack` | `seg(t, t0, t1)` 0→1 progress; `eOut`, `eIn`, `eInOut`, `eBack(k, over)`, `smooth`, `lerp`, `rng(seed)` | as is |
| Colours | `anim.html` → `C`, `anim.html` → `kc` | `C.<name>`; `kc(name, n)` mixes a `K` pair by night amount; `mix(a, b, k)`, `hexA(hex, alpha)` | as is; add `K` pairs |
| Sprites, backdrop, shading, glow | `buildSprites()`, `paintSpace()`, `drawStars()`, `shadeCircle()`, `glow()`, `sparkle()`, `blobPath()` | `NEB` (three gradients), and `ATMO`, `GLOW`, `WARM`, `VIG` from `radialSprite(w, h, inner, outer, stops)`, in `window.ready`; `paintSpace(nebula)`; `drawStars(t, drift, alpha, maxY)`; `shadeCircle(x, y, r, k, dark, lite)`; `glow(x, y, size, alpha, sprite)`; `sparkle(x, y, k)`; `blobPath(pts)` | as is (move `NEB` for other formats) |
| Planet, Moon, orbit, ghost | `drawPlanet()`, `CONT`, `project()`, `paintMoon()`, `orbitPos()`, `ghostMoon()` | `drawPlanet(cx, cy, R, rot, tilt)`, continents as loops in `CONT` (seed 4242); `orbitPos(angle, rx, ry, tilt, cx, cy)` returns x, y and the side (> 0 near); `ghostMoon(x, y, r, alpha)` | as is; edit `CONT` for another world |
| Headline and kicker | `popText()`, `kicker()`, `popTimes()` | `popText(str, x, y, size, t0, t, { w, stag, out, col, glow })`; `kicker(str, y, tin, tout, t, col)` | as is (kicker x → `W` / 2) |
| Transitions | `zoomAbout()`, `veil()`, `renderFrame()` | dive `zoomAbout(px, py, 1 + 9 * eIn(…))` plus flash; iris: clip circle onto `PD`, cyan rim, coast push | adapt times and targets; drawers in a fading scene must multiply alpha (Technical notes) |
| Coast and critter | `sceneCoast()`, `groundY()`, `TREES`, `WRACK`, `drawCritter()`, `critterPose()`, `lanternPos()`, `lanternGlow()`, `CRITTER_X`, `CS` | ground profile, gauge, hut, trees, night via `kc()`; walk and lift from `seg()` windows; the critter's start, 1790, also sits in two other places | adapt or replace; a new creature keeps the build rules |
| Diagram and icons | `sceneEarth()`, `wobAmp`, `tiltDeg`, `SEASONS`, `seasonIcon()` | axis, arc, readout; icons `{ k, x, y, c, t0 }` | adapt |
| Timeline and cues | `renderFrame()`, `window.events` | scene gates `t < 3.0`, `t >= 6.85`, `t < 7.55` | replace |

## Adapting
- **Style vs demo plot:** the style is the space backdrop, a glowing outline-free subject, the pops, diagrams in white,
  cyan and gold, dive and iris, navy fades, pad and whooshes. Plot: the Moon, coast, gauge, critter, wobble, seasons,
  copy. The transformation: any change at scale (vanishing in sparks, a gauge collapsing, nightfall).
- **New subject:** one subject on the centre line, one headline at a time, new objects by the shape rules. Traps:
  the scene gates in `renderFrame()` move with the transitions; `T_VANISH` also times two cues; each `words()` call
  repeats its `popText()` t0; the `wave` and `step` loops run from their own windows even after their scene is gone.
- **Length:** beats joined by dives and irises; past four, alternate space and ground or the rhythm turns
  predictable. In audio.py set `DUR` and move the fixed parts.
- **Shorter:** the demo has no slack (its diagram headline gets 1.0 s, its end card 0.15 s), so below 10 s cut whole
  beats: the diagram first, then the night; keep the opening. Minimums: a headline on screen 0.25 s per word from its
  first word to its exit (the demo's easy pace is 0.35–0.45 s); a kicker fully opaque for at least about 0.6 s; a new
  headline 0.3 s after the last one's exit at the earliest, as the demo's tides-to-night handover (5.0 → 5.3 s): its
  first words rise while the old line's last words fade at the other end, never in the same place; demo transitions;
  fades 0.25–0.4 s; a 0.8 s final hold. The signature reads 0.9 s after a 0.3 s fade-in (4 s plan); an end card costs
  about 2 s. All plans rendered in 16:9 with events.mjs and audio.py (peaks 0.39–0.45); holds measured as the template
  says, the ambient loops in Motion running (and the ±6 px tide left after flattening). A window keeps its demo
  length unless both ends are given (critter alpha 0.2 s, glow 0.4 s, walking ramps 0.2 s). "=" as demo, "drop" delete.

| Change in anim.html | Demo | 10 s (fixed) | 8 s | 6 s | 4 s |
|---|---|---|---|---|---|
| fade-in; nebula; stars; rise; Moon pop | 0.4; 0–1.2; 0.05–0.9; 0.2–1.6; 0.75–1.25 | = | = | = | 0.3; 0–0.8; 0.05–0.6; 0.1–1.1; 0.45–0.95 |
| space headline t0 / out; kicker in / out | 0.55 / 2.25; 1.05 / 2.2 | 0.55 / 2.1; 1.05 / 2.05 | as 10 s | = | 0.3 / 99; 0.8 / 99 |
| `T_VANISH` | 1.75 | 1.6 | 1.6 | = | 1.5; the ghost's drift 0.08 → 0 |
| dive; `t < 3.0`; flash; `coastIn`; coast settle; `T_TIDE` | 2.3–2.95; 3.0; 2.72–3.25; 2.85–3.0; 2.85–4.0; 2.95 | 2.15–2.8; 2.85; 2.57–3.1; 2.7–2.85; 2.7–3.85; 2.8 | as 10 s | = | drop dive, flash, coast: space scene only |
| tides headline t0 / out; kicker; `tideAmp` flattening | 3.15 / 5.0; 3.6–5.0; 3.55–4.95 | 3.0 / 4.6; 3.45–4.6; 3.4–4.55 | 3.0 / 4.25; 3.25–4.25; 3.4–4.2 | 3.15 / 99; 3.6–99; 3.55–4.6 | drop |
| night `n`; critter in (`t >`, alpha, glow); walk; lift end | 5.0–5.9; 5.2; 5.3–6.55; 7.0 | 4.6–5.5; 4.8; 4.9–5.9; 6.35 | 4.25–5.15; 4.45; 4.55–5.6; 6.05 | `n` 0; drop critter | drop |
| night headline t0 / out; kicker in / out | 5.3 / 99; 5.8 / 99 | 4.9 / 99; 5.4 / 99 | 4.55 / 5.8; 4.8 / 5.8 | drop | drop |
| iris (and the `t >= 6.85`, `t < 7.55` gates); coast fade start (alpha, rim) | 6.85–7.55; 7.3 | 6.05–6.75; 6.5 | 5.75–6.45; 6.2 | none | none |
| `axA` in, out; axis length; `wobAmp` up, down; `tiltDeg` start | 7.35–7.7, 8.5–8.8; 7.35–7.75; 7.45–8.4, 8.5–9.1; 7.45 | 6.55–6.9, 7.7–8.0; 6.55–6.95; 6.65–7.6, 7.7–8.3; 6.65 | `wobAmp`, `axA` 0 | drop | drop |
| `SEASONS` t0; `seasonIcon()` exit; headline t0 / out; kicker | 7.7–8.0; 8.5 (8.8) + (s.t0 − 7.7) × 0.3; 7.45 / 8.45; 7.95–8.45 | 6.9–7.2; 7.7 (8.0) + (s.t0 − 6.9) × 0.3; 6.65 / 7.65; kicker: drop | drop both `SEASONS` loops, headline, kicker | drop | drop |
| `endK`; empty orbit; end title t0; "EARTH, ALONE" | 8.5–9.4; 8.8–9.3; 8.7; 9.1 | 7.7–8.5; 8.0–8.45; 8.07; 8.4 | 0; 6.3–6.75; 6.1; 6.4 | drop | drop |
| fade start; `DUR` | 9.65; 10 | 9.65; 10 | 7.7; 8 | 5.7; 6 | 3.75; 4 |
| settled from → final hold | 9.5 → 0.15 s | 8.83 → 0.82 s | 6.87 → 0.83 s | 4.6 → 1.1 s | 2.6 → 1.15 s |

| Change in cues and audio.py | Demo | 10 s (fixed) | 8 s | 6 s | 4 s |
|---|---|---|---|---|---|
| `rise`, `land`, words, `blip`; `whoosh`, `splash`; tides words | 0.2, 1.2, 0.55, 0.8; 2.3, 2.9; 3.15 | =; 2.15, 2.75; 3.0 | as 10 s | = | 0.1, 0.8, 0.3, 0.5; drop the rest |
| `wave` loop end; `dusk`; night words; `step` loop; `tinkle` | 5.3; 5.0; 5.3; 5.3–6.55; 6.62 | 4.9; 4.6; 4.9; 4.9–5.9; 5.97 | 4.55; 4.25; 4.55; 4.55–5.6; 5.67 | =; drop the rest | drop the `wave` loop but keep `dt`, which the `step` loop reads; rest past `DUR` |
| iris `whoosh`, `land`; diagram words, `wobble`; `bloop` base; `suck` | 6.85, 7.5; 7.45, 7.5; 7.7; 8.5 | 6.05, 6.7; 6.65, 6.7; 6.9; 7.7 | 5.75, 6.4; drop the rest | past `DUR` | past `DUR` |
| end words and `chord` | 8.7 | 8.07 | 6.1 | `chord` 4.3 | `chord` 2.0 |
| `bed` dip down from, back by; crickets first, stop | 5.0, 7.2; 5.45, 7.0 | 4.6, 6.4; 5.05, 6.2 | 4.25, 6.1; 4.7, 5.9 | delete both | nothing (both start after 4 s) |
| `sea`: in, out; flattening start over | 2.85, 7.3; 3.55 over 1.4 | 2.7, 6.5; 3.4 over 1.15 | 2.7, 6.2; 3.4 over 0.8 | =; 3.55 over 1.05 | delete its mix |

  - 10 s: the opening gives up 0.15 s, the tides beat 0.25 s, the night beat 0.4 s (walk 1.0 s instead of 1.25), so
    the tides headline keeps 1.6 s, its kicker 0.75 s fully opaque, and the end title starts at 8.07, after the
    diagram headline's words are gone. The diagram beat stays as tight as the demo's: its headline, at the floor of
    0.25 s a word, is fully landed for 0.23 s, and its kicker (0.1 s opaque in the demo) is dropped. For more room,
    start from the 8 s plan and give the 2 s to holds. 8 s: its kickers start 0.25 s after their headlines (3.25, 4.8)
    to stay opaque 0.6 s; the end title pops while the iris closes; for 0.16 s (6.1–6.26) its first words show outside
    the circle while the night headline's last words fade inside it. 6 s ends on the coast, the tides headline held
    (`n` 0, both `t > 5.2` critter calls deleted). 4 s is the opening alone: `renderFrame()` draws `drawSpaceScene()`
    unzoomed and ungated, without the coast block and the flash; its headline and kicker stay as the end card.
  - A dropped beat takes its cue loops and fixed audio with it (rows above). Between plans, take the shorter one and
    give the spare time to headline holds and the final hold.
- **Other formats:** values in Composition. Space, diagram and end card recompose by moving centres and splitting
  headlines; the coast needs a new ground profile and every prop placed again.

## Boundaries
- **Distinct from:** `flat-design` (45° long shadows, thin Lato, UI colours); `infographic` (also Fredoka, but a pale
  page, a squash-and-stretch character, counters); `grainy-flat` (stipple-grain shading, pastels); `cosmic-epic`
  (WebGL light, deep time); `corporate-memphis` (people with noodle limbs); `kawaii` (bouncing pastel stickers).
- **Poor fit:** equations and proofs (`3blue1brown`); fast stats with counters (`infographic`, `data-visualization`);
  personal anecdotes carried by people (`storytime`); app walkthroughs (`product-ui`); how a machine works part by
  part (`technical-cutaway`); a step-by-step lesson (`whiteboard`).
- **Do not:** take more than the visual language and tone. Generic flat-vector explainer language, free to use:
  outline-free shapes, crescent shading, glows, star fields, a rounded sans popping word by word, dives and irises, a
  small invented creature as a scale cue. Imitation if pushed further: their characters, logo, wordmark or title
  lettering, intro or end-screen sign-off, running jokes, or a video's title or opening. Invent each creature for the
  film's subject from the shape rules, as the demo's lantern critter is, and model none on a character from one of
  their videos; never a small round bird as narrator or mascot (a film about birds draws its real species, such as a
  swallow or a heron). Never show the channel's name or "In a Nutshell" in a film, and nothing that suggests they made
  or endorse it.

## Technical notes
- No render.json or vendor folder: Canvas 2D, no GPU; anim.html, fonts.css, two woff2 files. 300 frames render in
  about 8 s on one worker (measured); events.mjs and audio.py take about a second each.
- Deterministic: `rng()` seeds 7 (stars), 4242 (continents), 31 (sparks), 55 (seaweed); audio.py's `rs` is 21; 7.9 s
  and 5.6 s alone and after earlier frames gave identical files. `renderFrame()` resets transform, alpha, composite
  and filter and wraps the space and coast scenes in save and restore, not `sceneEarth()`: wrap drawers added there.
- The coast fades by the alpha `renderFrame()` sets before `sceneCoast()`, but `popText()`, `kicker()`,
  `drawCritter()`, `glow()` and `lanternGlow()` (its glows and its ground ellipse), `ghostMoon()`, `drawStars()` and
  the gauge labels set `globalAlpha` outright and ignore it. In 16:9 the closing iris wipes the critter off; in 9:16
  and 1:1 it ends inside the final circle, sits opaque on the planet through the fade (6.5–6.75 s in the 10 s plan)
  and vanishes in one frame. Multiply instead (ctx.globalAlpha *= a; in `drawStars()` keep the outer alpha in a
  variable before its loop): figures then fade with the scene, and every other frame and the hold stay the same
  (tested).
- Sizes outside `W`/`H`: the canvas tag and every value the 9:16 block changes. The iris's start radius 1250 covers
  all formats; the vignette suits 9:16 and leaves 1:1 corners lighter (fine).
