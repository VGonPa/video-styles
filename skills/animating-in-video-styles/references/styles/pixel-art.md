# Pixel Art (`pixel-art`)

A level of a 16-bit console game, painted on a tiny 320 × 180 screen and blown up six times with hard square
pixels: a dithered backdrop, parallax layers scrolling at different speeds, a hero sprite with an ink outline,
collectibles that spark and pop score numbers, a HUD, a world-card title, a colour-cycling "LEVEL CLEAR!" and a
world map with the next level waiting. It draws on the side-scrollers of the early nineties; the mood is bright,
busy and triumphant.

**Reference film:** "WORLD 3-2 CORAL DEEP": a diver swims a coral reef collecting pearls, ducks under an inflating pufferfish, opens a treasure chest, gets "LEVEL CLEAR!" and PEARLS 12/12, then a mosaic fade to the world map where the cleared node turns gold and the diver hops to 3-3 · `styles/pixel-art/`

## Signature
- Hard 6 × 6 pixels everywhere: the frame is a 320 × 180 picture (`LO`) enlarged 6× with smoothing off, and every sprite, letter and position lands on that grid. It opens with a mosaic from black (16-px blocks to clean, 0–0.45 s).
- A side-scrolling level in layers, each at its own speed: a Bayer-dithered backdrop gradient, a hazy far layer, a mid layer, the floor the hero moves along and a foreground layer that passes in front of the hero, plus at least one stepped ambient cycle (in the demo's reef: a water gradient with dotted light shafts and a shimmering surface band, far rocks, coral, rippled sand with moving caustics, foreground kelp).
- A HUD band over the top edge: the collectible's icon and counter, a six-digit SCORE and a cell meter, in a chunky 6 × 7 bitmap font with a 1-px ink ring and one- to three-band colour fills (in the demo: a pearl icon, PEARLS 00/12, SCORE 008400, an AIR meter of eight cells).
- A sprite hero with a 1-px ink outline and a stepped six-frame movement cycle enters from the left along a row of collectibles; each pickup throws an eight-point pixel star and flashes the counter, and some pop a score number that rises and blinks out (in the demo: a diver kicking past eleven pearls; three of them and the chest's big pearl pop scores).
- A world card (a world-level number over the level's name; "WORLD 3-2" over "CORAL DEEP" in the demo) drops in from the top with an overshoot at 0.35–0.6 s.

## Palette
| Role | Colour | In code |
|---|---|---|
| Ink: every sprite outline, glyph ring and box frame | 0c0b1b (`P[tok]`) | `P.ink`, `bake` |
| Water, surface to depth; bubbles, shafts, glints, card and box fills (w6) | 9eefed, 50c2d8, 2b94c3, 2070a7, 195892, 133f74, 0d2b56 (`P[tok]`) | `P.w0` to `P.w6`, `genGrad()` |
| HUD band (the only translucent fill) | `rgba(12,42,85,0.55)` | `paintHud()` |
| Gold, orange, red, dark red: title bands, chest bands, burst, fins, cleared node | ffd240, fe7a30, d6273e, 89192f (`P[tok]`) | `P.gold`, `P.orange`, `P.red`, `P.dred`, `cGold` |
| White, cloud, sky, silver, grey: text, highlights, locked node | ffffff, e7f5ff, 8ed0fe, b8c2d1, 6c7892 (`P[tok]`) | `P.white`, `P.cloud`, `P.sky2`, `P.silver`, `P.gray` |
| Sand light to shadow; caustic light | f1d58f, e2b86d, b88a4d, 8d6541; `#f0d49a` | `P.sandL`, `P.sandM`, `P.sandD`, `P.sandS`, `genCaustics()` |
| Reef rock (the far layer uses w3 and w5) | 3f4a8b, 2d3469, 1e2251 (`P[tok]`) | `P.rockL`, `P.rock`, `P.rockD`, `genFar()` |
| Corals and sea fans | fe6f92, feb3c7, c1418e, 7a40a1 (`P[tok]`) | `P.pink`, `P.lpink`, `P.magenta`, `P.violet` |
| Kelp; island grass | 207a4b, 15543b, 62c34b; `#45a347` | `P.kelp`, `P.kelpD`, `P.kelpL`, `genMap()` |
| Wood (chest, palms, mast), brain coral; tank and chest highlight | a7693b, 6a3f27, dfa161; `#fff0a0` | `P.dirt`, `P.ddirt`, `P.sand`, `genChest()` |
| Diver skin, hood; pearl shading; pufferfish belly, body | f1b27f, c37c53, 2b2539; e5e9f6, b6a7d7; `#fff1c4`, `#f5c542` | `P.skin`, `P.skinD`, `P.hood`, `P.pearl`, `P.lilac`, `genPuffer()` |
| Fades and the gap between scenes | `#000` | `fadeSteps()`, `composeFrame()` |

- The `P` string lists names and bare hex (`P[tok]` adds the `#`): about 44 colours with the literals, each object
  in two to four plus ink. Fills are flat; a gradient is two adjacent colours mixed through the 4 × 4 `BAYER` matrix
  (`genGrad()`, the shafts), never a blend. The only alpha: the HUD band and `fadeSteps()` in eighths.

## Typography and copy
- No font files: one bitmap face from `GLYPH_ART` (6 × 7, 2-px stems, 1-px bars). `textBitmap()` caches each string
  with a 1-px `P.ink` ring on all eight sides and a colour function painted row by row: `bands()` gives `cWhite`,
  `cSilver`, `cGold` (gold, orange, red), `cAqua`, `cPearl`; `cCycle` scrolls 2-px stripes of `CYCLE_COLS` at 12 fps.
  `drawText(g, str, size, x, top, colFn, align)` draws 1× (42 screen px tall) for `size` under 16, else 2×: no other.
- Glyphs: capitals A C D E H I K L N O P R S T U V W X, digits, `- + ! /`, space. A missing character draws
  nothing but keeps its 7-px gap ("BONUS" shows " ONUS"). Write copy in capitals and add the glyphs it needs to
  `GLYPH_ART`; these were rendered beside the demo's letters and match (the punctuation is 2 px wide):
```
B #####. ##..## ##..## #####. ##..## ##..## #####.
F ###### ##.... ##.... #####. ##.... ##.... ##....
G .####. ##..## ##.... ##.### ##..## ##..## .#####
J ....## ....## ....## ....## ##..## ##..## .####.
M ##...## ###.### ####### ##.#.## ##...## ##...## ##...##
Q .####. ##..## ##..## ##..## ##.### ##.##. .##.##
Y ##..## ##..## ##..## .####. ..##.. ..##.. ..##..
Z ###### ....## ...##. ..##.. .##... ##.... ######
? .####. ##..## ....## ...##. ..##.. ...... ..##..
. .. .. .. .. .. ## ##
, .. .. .. .. ## .# #.
: .. ## ## .. ## ## ..
' ## ## #. .. .. .. ..
```
- For anything still missing (lowercase, % & # ( ) and other symbols), reword: "PCT", "AND".
- Width (`textBitmap()` on real lines): 7 px a character, 8 for W and M, 3 for . , : ', 4 a space, less 1; double
  at 2×: "CORAL DEEP" 66 / 132 px, "LEVEL CLEAR!" 80 / 160 (1× / 2×). Per line, 8 px from the edges: 16:9 43 at 1×,
  21 at 2× (the world card's fill holds 10); 9:16 (x 8–152) 20 and 10; 1:1 (x 10–170) 23 and 11.
- Copy is game text, two to four words a card (a world number and level name, HUD labels, "+200", "LEVEL CLEAR!",
  "NEXT" and a name); longer copy takes a second line or card. The counts are literal strings: `'/12'` in
  `paintHud()`, "PEARLS 12/12" in `drawClear()`, "12/12" in `drawMap()`.

## Texture and finish
- `buildSprites()` precomputes into `SPR`: the water, two shaft tiles (`genRays()` over `SHAFTS`, swapped at 4 fps),
  640-px tiles for the far layer (`genFar()`) and reef (`genReef()`: mounds, `coralBranch()` trees, sea fans, brain
  coral), the sand (`genSand()`), eight caustic frames (`genCaustics()`, 8 fps) and every sprite frame. Per frame
  `paintLevel()` adds the surface band (8 fps), nine fish, two vent bubble streams, kelp in 10 fps steps, the HUD.
- No scanlines, CRT, bloom, grain or vignette: the finish is the grid, the dither and the ink. `transition()` is a
  `pixelate()` mosaic through `MOSAIC_SIZES` (1–16) plus `fadeSteps()` in eight steps, like a console's fade register.

## Shapes, line and figures
- Sprites are authored on a cell grid with `pixBuf()`: `put` cells, `dot` discs, `line` thick strokes, then `bake`
  draws each cell as one pixel and rings the silhouette with `P.ink`, 1 px outside. A part that must read over
  another gets its own ink first, as the near leg in `genDiver()`.
- Shading is two or three flat tones plus one white highlight pixel on anything round. Motion is pre-generated
  frames, never a scaled or rotated image (in the demo: six kick phases per arm pose, `SPR.diver`, `SPR.diverUp`; 22
  pufferfish, radius 5–15, calm and angry; three chest states; diver 52 × 30, anchor `DV`, chest 34 × 32, pearl 9).
  A new object belongs at 8–50 px in three to five colours plus a highlight, ink-ringed, its states as frames.
- The diver's legs mostly read as one mass (a known defect): ink each near limb of a figure separately. Effects
  are plotted pixel by pixel: `drawBurst()` computes twelve dashed rays with `px()`, turning in 8 fps steps.

## Composition and camera
- 16:9 (320 × 180): HUD rows 0–16; the floor line low, y 150 ± 2 (`floorY`); the far layer's highest peaks near
  mid-height. Parallax by depth: backdrop details 0.1, far layer 0.2, distant movers 0.35, mid layer 0.5, floor,
  props and actors 1.0, foreground 1.35 (in front of the hero). `camX` follows the hero once it passes x 110 and
  eases to a stop near 190. Props stand on `floorY` at world x values in `paintLevel()`. In the demo's reef: surface
  16–22, far rocks from about y 88, reef mounds 118–156, sand from `SAND_Y` 140; shafts 0.1, fish 0.35, reef and
  its vent bubbles 0.5, kelp from below the frame at 1.35.
- Cards: the world card fills x 164–308 (right of centre, away from the hero entering left) at y 32–72; the
  LEVEL CLEAR! box is 228 × 48 on (160, 56); the map is full screen inside a 2-px ink and 1-px gold border.
- Other formats keep 6× (rendered): 9:16 is a 180 × 320 buffer, 1:1 a 180 × 180 one. 9:16 key text spans buffer
  x 5–149, y 50–233 (screen 300–1398 px), clear of review.md's bands; the bottom band holds the reef's foot and
  sand (the map's: sea and compass). Changes from the 16:9 code (OY, HY are new constants):
```
9:16  canvas 1080 x 1920; W 1080, H 1920, LW 180, LH 320; OY = 110 (world layers down), HY = 46 (HUD top)
  water genGrad stops [[0,w1],[80,w2],[190,w3],[250,w4],[320,w5]]; genRays top 6, depth 250; surface fillRect(i, 0, 1, y0), y0 = 4 + wave
  paintLevel: L.save(); L.translate(0, OY) before par(SPR.far, 0.2), L.restore() before the world card
  drawKelp base 182 (was LH + 2); both bubble cut-offs 22 -> 22 - OY; genFar ph = 60 + r() * 80, kh = 80 + r() * 90
  camX: d = x - 60, soft limit 230 (was 110 and 150); the chest ends at x 115-149, the hero at 94
  world card: ink rect x 8 (144 wide), fill and top line x 9 (142), texts on 80; yy = R(-40 + 126 * easeOutBack(u) - 150 * v * v)
  HUD band (0, HY, LW, 26), ink rows HY - 1 and HY + 26; pearl icon at (5, HY + 3); left-aligned text tops HY + 4:
    count x 17 (no word PEARLS), SCORE x 62, digits x 102; AIR at (5, HY + 15); cell k: ink (31 + 8k - 1, HY + 14, 8, 9)
  LEVEL CLEAR boxW = R(140 * Math.min(1, open / 0.87)), boxH = R(64 * open), left = 80 - (boxW >> 1),
    top = 128 - (boxH >> 1); 'LEVEL' top 101, 'CLEAR!' top 119 (size 16, centred on 80);
    row R(146 - 6 * slide), pearl x 30, text on 86; confetti ceiling HY + 28
  map NODES [[46,196],[128,160],[50,128],[128,96]]; MAP_PATHS controls [84,158] [100,120] [84,92]; genMap stops
    [[0,w2],[160,w3],[320,w4]]; palms [[22,200],[150,164],[72,132]]; mast x 66 from y 136 up, yard y 128, flag from
    (67, 125); tower x 141, base 98, cap (141, 91-92); compass (30, 284); glints x R(r()*160+10), y R(r()*290+20);
    banner (10, 52, 142, 22), 'WORLD 3' on 46, 'CORAL SEA' on 112, top 59; tally pearl x NODES[1][0] - 26, '12/12' on NODES[1][0] + 4 at NODES[1][1] + 20 + 4 * (1 - v);
    NEXT yy = R(320 - 94 * easeOutBack(v)) (rests 226), box (10, yy - 6, 142, 20), 'NEXT' x 16, name x 50
1:1   canvas 1080 x 1080; LW 180, LH 180; OY 0, HY 0 (the two-row HUD at 0-26); far layer and kelp as 16:9
  water stops [[26,w1],[60,w2],[100,w3],[140,w4],[180,w5]]; rays top 30, depth 120; surface fillRect(i, 27, 1, y0 - 27),
    y0 = 31 + wave; bubble cut-offs 32; confetti ceiling, HUD and camX as 9:16
  card rects at x 18 / 19, texts on 90, yy = R(-40 + 80 * easeOutBack(u) - 150 * v * v)
  LEVEL CLEAR box as 9:16 with left = 90 - (boxW >> 1), top = 62 - (boxH >> 1) (clears the prize in the raised hand);
    'LEVEL' 35, 'CLEAR!' 53 (centred on 90); row R(80 - 6 * slide), pearl x 40, text on 96
  map NODES [[42,120],[132,98],[48,64],[138,48]]; controls [84,92] [104,66] [92,40]; stops [[0,w2],[90,w3],[180,w4]];
    palms [[18,124],[158,102],[70,68]]; mast x 64 from 72 up, yard 64, flag (65, 61); tower x 151, base 50, cap (151, 43-44); compass (16, 40);
    glints x R(r()*160+10), y R(r()*150+20); banner (20, 6, 142, 22), texts on 56 and 122, top 13; tally as 9:16;
    NEXT yy = R(180 - 30 * easeOutBack(v)), box (20, yy - 6, 142, 20), 'NEXT' x 26, name x 60
```

## Motion
- Positions move only by whole buffer pixels (`R()` rounds every draw, `px()` truncates), so motion advances in
  6-screen-px steps. Keep it so: no sub-pixel offsets, never `imageSmoothingEnabled` back on (`mk()` turns it off),
  no rotated or scaled sprites, motion blur, cross-dissolve or alpha fade on an object.
- Cycles are stepped at 4–12 fps, never smooth: the hero's cycle faster travelling than idle, ambient loops at 4–10,
  effects at 8, colour cycling at 12 (in the demo: kick 11 fps swimming and 5 hovering, `hover`; caustics and surface
  8, shafts 4, kelp 10, fish tails 6, pearl glints 8, burst 8, confetti flips 8, title colour cycle 12, map glints 6).
- Easing: `easeOutBack` (k 1.9, about 12 % overshoot) for arrivals (card, pufferfish inflating in 0.22 s, NEXT box);
  the card leaves on `v * v`; the hero follows a cubic Hermite path through `PATH` (`pathAt()`) plus a 1.4-px sine
  bob; pearls bob 1 px. Shakes flip ±1 px 24 (chest rattle) or 30 (pufferfish shiver) times a second.
- Things vanish by blinking: pops rise 22 px/s for 0.6 s, blinking at 10 Hz for the last 0.2; "!" blinks at 6 Hz,
  the full counter (3 Hz) and the last air cell (2 Hz) blink as idle loops.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.45 | Mosaic-in from black: six block sizes, eight brightness steps | `transition()`, `composeFrame()` |
| 0.35–2.1 | World card drops (to 0.6), holds still 0.6–1.8 (measured in its box), rises out by 2.1 | `T_CARD` |
| 0–2.6 | Diver swims in; pearls 1–7 at 0.95–2.6 with +200, +150 pops; the camera scrolls from about 1.9 | `PATH`, `PEARL_T`, `camX` |
| 3.25–5.15 | "!" and shiver; the pufferfish inflates angry, the diver ducks under (lowest at 4.1); it deflates at 4.55 and flees; pearls 8–11, +200 | `T_WARN`, `T_PUFF`, `T_DEFL`, `puffR`, `puffPos` |
| 5.75–6.5 | Chest rattles; lid flips at 6.08 with a gold burst; the big pearl arcs to the raised hand, +500 | `T_RATTLE`, `T_OPEN`, `T_GRAB`, `drawBurst()` |
| 6.75–7.55 | LEVEL CLEAR!: confetti, box unfolds by 7.05, title colour-cycles, PEARLS 12/12 slides in 7.05–7.2, score tallies 7.15–7.55 | `T_CLEAR`, `drawClear()`, `scoreAt()` |
| 7.95–8.3 | Mosaic-out and stepped fade (0.3 s), black until 8.3 | `T_OUT`, `levelEnd` |
| 8.3–8.95 | Map mosaics in (0.28 s); node 3-2 flips gold and hops, star burst, path dots light 8.69–8.93, 12/12 slides in | `T_MAP`, `drawMap()` |
| 8.92–9.3 | The diver's head hops three times to 3-3; NEXT box rises 9.15–9.3; 3-3 blinks from 9.25 | `drawMap()`, `bez()` |
| 9.3–10 | Still for 0.7 s, then a hard cut: no fade | `composeFrame()` |

- Mosaic-in under the card, beats of 1–1.5 s (pickups, hazard, prize), LEVEL CLEAR!, mosaic-out to the map sign-off:
  all reusable patterns (with the "!" warning, prize burst, hop and NEXT); the rest is demo content.
- The demo's ending is short: the map settles (sea glints, 3-3's blink, the head's bob kept) only at 9.30 and the
  clip cuts at 10.0 mid-chord. Tested 10 s fix: `T_OUT` 7.55, `T_MAP` 7.9, and the map branch of `composeFrame()`
  calls `transition(t > DUR - 0.3 ? seg(t, DUR - 0.3, DUR) : 1 - seg(t, T_MAP, T_MAP + 0.28))` (its only use of
  anim.html's `DUR`, which must equal the film's length): still 8.90–9.74,
  near-black at 10, the chord over at 9.85; LEVEL CLEAR! still reads 7.05–7.55.
- Review keys: KEYS=1.2,3.7,6.4,7.4,9.5 (card held, pufferfish inflated, full burst, LEVEL CLEAR!, settled map); in
  a new film the card, the hazard, LEVEL CLEAR! and a frame inside the final hold.

## Sound
audio.py synthesizes console channels at 48 kHz stereo (`sq()` pulse waves with duty and sweeps, `tri()` a 4-bit
stepped triangle, `noise()`), `DUR` 10.0, from `events.json` cues `{t, k}`:
- Music at fixed times, not from cues: a 128 `BPM` groove of eighths (`E8`) from 0.45 s (the mosaic-in's end) to
  `T_END` 6.7 (0.05 s before LEVEL CLEAR!), fading over its last 0.4 s: triangle bass, a 12.5 % pulse arpeggio
  panned ±0.35 and a noise tick, looping `prog` (Am, F, C, G, eight eighths each: 7.5 s a cycle).
- Cues, sent by role, not by the demo's names: `pearl` per collectible, with `n` the pickup index from 0 (a two-note
  chime climbing an 11-step scale by `n`); `warn`, `puff` and `deflate` for a hazard's alert, threat and retreat;
  `rattle` (sent three times), `open` and `bigpearl` for the prize's container shaking, opening and the grab;
  `bubble` for the hero's breath or any small puff; `card` for the world card; `fanfare` (seven-note melody over two
  bass notes, 1.35 s) and `tally` (14 blips, about 0.5 s) for LEVEL CLEAR!; `swoosh_in` and `swoosh_out` (0.4 and
  0.35 s sweeps) for the mosaic-in and mosaic-out; `flag` (node cleared), `dot` (eight), `hop` (three) and `select`
  for the map, `select` carrying the closing chord: a triangle arpeggio from 0.2 to 1.1 s after it.
- What breaks it (tested): `pearl` without `n` raises KeyError; `n` of 11 or more raises IndexError (extend the
  scale for a twelfth pickup, as the 4 s plan does); a negative `n` plays a wrong note. Pans are constants, so no
  field reaches NaN. audio.py prints only "audio.wav ok"; the plans' peaks come from the skill's check_audio.py.
  Cues before 0 or past `DUR` and unknown kinds drop silently; none is looked up by name.
- No master fade (a tanh limiter only): a sound ringing at `DUR` clicks off, as the demo's chord does; send `select`
  1.1 s and a closing `swoosh_out` 0.35 s or more before `DUR`.
- Re-timing: set `DUR`; move the groove's start (the `t` set beside `T_END`) to your mosaic-in's end and `T_END` to
  LEVEL CLEAR! − 0.05, or the groove plays under the fanfare and the chord. The film derives the other cues from its
  timing constants, with `swoosh_in` at 0.05 and fixed offsets for `card`, `tally` and the map.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Back buffer and upscale | `anim.html` → `composeFrame` | paint into `L` (`LO`, `LW` × `LH`), one `drawImage` to `W` × `H` with smoothing off | as is; sizes per format |
| Helpers and palette | `mk()`, `px()`, `R`, `seg()`, `rng()`, `BAYER`, `P` | `mk(w, h)` canvas without smoothing; `px(g, x, y, col)` one pixel; `rng(seed)` seeded floats | as is; add `P` entries |
| Bitmap text | `textBitmap()`, `drawText()` | `drawText(g, str, size, x, top, colFn, align)`; colour functions from `bands()` or `cCycle` | as is; add rows to `GLYPH_ART` |
| Sprite builder | `pixBuf()` | `pixBuf(w, h)` → `put`, `dot`, `line`, `bake(outline)` | as is |
| Dithered layers | `genGrad()`, `genRays()`, `genFar()`, `genReef()`, `genSand()`, `genCaustics()` | `genGrad(stops, w, h)` with [row, colour] stops; drawn by `par` with a parallax factor | adapt: a new world |
| Transitions | `transition()` | `transition(amount)`: 0 clean, 1 biggest blocks and near-black | as is |
| HUD, clear banner | `paintHud()`, `drawClear()` | counter, score from `scoreAt()`, air meter; from `T_CLEAR`: confetti, box, `cCycle` title, row | adapt: labels, counts, copy, layout |
| World map | `genMap()`, `drawMap()`, `genNode()`, `genHead()` | `NODES`, `MAP_PATHS`, `bez()`; actions keyed to `T_MAP` | adapt: names, layout |
| Demo level | `genDiver()`, `genPuffer()`, `genChest()`, `genPearl()`, `PATH`, `PEARL_T`, `EXHALES`, `PUFF`, `CHEST`, `T_CARD` … `T_MAP` | | replace |
| Cues | `window.events` | one `cue(t, k, extra)` per sound, from the timing constants | adapt |

## Adapting
- **Style vs demo plot:** style is everything in Signature (6× grid and mosaics, layered scroller with a dithered
  backdrop, HUD band, ink-ringed stepped sprites, pickup stars and pops, dropping world card) plus the "!" warning,
  prize burst, LEVEL CLEAR!, map and chiptune; plot is the sea and reef, diver, pearls, pufferfish, chest, the AIR
  and PEARLS labels and all names. Transformation: the counter filling to LEVEL CLEAR!, the node turning gold.
- **New subject:** make the brief a level: a hero, a collectible that counts the message (steps, coins, stars), one
  hazard, one prize. Replace the generators and the world; keep the kit. Traps: the count strings are literal;
  missing glyphs leave gaps; `hover` is the literal `t > 5.85`; `placeWorld()` puts each pickup at `pathAt()` +
  `HAND` at its time, so moving `PATH` moves the pickups; the pop list in `paintLevel()` indexes pickups by position
  (index = pickup count is the prize) and its strings are decorative (`scoreAt()` adds 50 a pickup and 500 for the
  prize; the demo's +200 and +150 sit on 50-point pearls, so keep '+500' for the prize only).
- **Values that follow the hero's shape** (an upright 30 × 44 seahorse rendered in 9:16): `DV`, `HAND`, `HAND_UP`
  (pickups, grab pop, held prize), the exhale origin (path +17, +1), the "!" offset (+12, −18), the hover point
  (`CHEST` x − 41), the duck depth (y 127 keeps the diver's 30-px box 8 px above the floor; the seahorse's tail
  touched it). Layout, camera, HUD, cards and map did not change.
- **Length:** the level is a scroll: lengthen `PATH`, raise the camera's limit (150 + 40 in `camX`; 230 + 40 in 9:16
  and 1:1) and set `SAND_W` to at least the camera's final value + `LW` + 40. The sand and caustic strips are drawn
  once at −`camX` and do not wrap: at 640 the floor ends at buffer x 640 − `camX` (rendered: `camX` 400 in 16:9
  leaves x 240–320 bare, 600 in 9:16 leaves x 40–180; `SAND_W` 1200 fixes both). Only the shafts, far and reef tiles
  wrap (every 640 px). Add props and floor details (the demo's mid kelp) along the route at world x (screen x = x −
  `camX`); mid-layer pieces move at 0.5 (screen x = vx − 0.5 · `camX`, the demo's vent streams) and foreground pieces
  at 1.35 (kx − 1.35 · `camX`, the demo's kelp). Extend the hero's ambient puffs (`EXHALES`, every 1.1 s, stopping
  at 7.05) to the level's end. One pickup run, hazard or prize per 1–1.5 s; past 15 s, two levels with a map between.
  AIR empties at 17.6 s. Re-time anim.html's `DUR` (unused in the demo, but the fix's closing fade reads it: left at
  10 in a 14 s film, the whole map renders black), `T_END`, audio.py's `DUR` and build.sh's `DUR`.
- **Shorter:** to about 7 s keep every beat and shorten holds as the 6 s plan did: card hold 0.85 s, pickups 0.11 s
  apart, the swim up to twice the demo's 60–85 px a second, LEVEL CLEAR! until `T_CLEAR` + 0.8 (the tally's end,
  0.5 s after the title). Then drop the hazard (1.6 s), then the prize and the map, ending on LEVEL CLEAR!; never the
  mosaic-in, counter or LEVEL CLEAR!. A dropped beat stays in the code: times to 99 (its cues fall past `DUR`), its
  object off the world (`PUFF` x −999, `CHEST` x 9999), or the pufferfish idles and a closed chest sits on the floor.
  The signature reads once the mosaic-in ends (0.45 s, 0.3 tested); the card overlays the action, so it costs no time
  of its own (drop 0.25, hold, exit 0.3). Late settlers: the burst at `T_OPEN` + 2.01; confetti 4.05 s after
  `T_CLEAR` in 16:9 and 6.15 s in 9:16 (hidden by the mosaic-out; a film ending on LEVEL CLEAR! drops it); the
  demo's `PATH`, which drifts to the end with the camera (end on two equal points). Holds below match the frame with
  every action (pops, flash, burst, confetti, card, NEXT box, mosaics) forced to its end; loops with no end state
  that run from their first appearance, as on a console's cleared screen, keep going (water, shafts, fish, bubbles,
  kelp, the hero's kick, bob and breath, colour cycling, HUD blinks). Both plans ran events.mjs and audio.py:
```
6 s, 16:9 (peak 0.604): mosaic-in seg(t, 0, 0.3); T_CARD 0.15, card window T_CARD + 1.4, v = seg(t, T_CARD + 1.1, T_CARD + 1.4);
  no hazard: T_WARN = T_PUFF = T_DEFL = 99, PUFF.x -999; T_RATTLE 1.75, T_OPEN 2.08, T_GRAB 2.5, T_CLEAR 2.75,
  T_OUT 3.55, T_MAP 3.9; CHEST.x 270; hover = t > T_RATTLE + 0.1; EXHALES [0.45, 1.55, 2.65]; DUR 6.0, end transition as the fix
  PATH [[-0.3,-64,84],[0.45,8,80],[0.95,62,64],[1.35,115,76],[1.75,175,102],[2.1,222,118],[2.5,228,119],[3.2,230,121],[6,232,120]]
  PEARL_T [0.55,0.66,0.77,0.88,1.05,1.16,1.27,1.42,1.53,1.64,1.75]; audio.py DUR 6.0, groove from 0.3, T_END 2.7. Still 4.90-5.74.
4 s, 9:16 layout (peak 0.544): level only, its out-transition is the ending: T_CLEAR 1.9, T_OUT 3.7; T_MAP, T_WARN,
  T_PUFF, T_DEFL, T_RATTLE, T_OPEN, T_GRAB = 99; PUFF.x -999, CHEST.x 9999; mosaic-in and card as 6 s; hover = t > T_CLEAR
  PATH [[-0.3,-40,84],[0.4,18,78],[0.85,66,62],[1.3,112,84],[1.7,150,96],[2.1,160,92],[2.6,160,92],[4,160,92]]
  PEARL_T [0.45,0.55,0.65,0.75,0.87,0.97,1.07,1.19,1.31,1.43,1.54,1.65] (12); confetti loop n < 0;
  pops [[3,'+200'],[7,'+150'],[11,'+200']]; cue(T_OUT - 0.05, 'swoosh_out'); audio.py DUR 4.0, groove from 0.3,
  T_END 1.85, pearl scale + 19. Still 2.70-3.74 (the tally ends at 2.70).
```
- **Other formats:** recompose by moving coordinates, never by scaling (values in Composition): 9:16 raises the far
  spires and breaks titles in two; 1:1 keeps the 16:9 heights. The hero stays on screen to the last frame in both.

## Boundaries
- **Distinct from:** `nes-8bit` (256 × 240 at 4×, pillarboxed, 64-colour palette, three-colour sprites, one scrolling
  plane, no dither, Press Start 2P); `jrpg` (384 × 216 at 5×, battle menus, portraits, dialogue); `point-and-click`
  (320 × 200 windowed, painted rooms, inventory, speech); `handheld-lcd` (four greens, ghosting); `dither-1bit` (two
  inks); `voxel` (3D blocks). Here: a full-frame side-scroller, many colours, dithered gradients, HUD, colour cycling.
- **Poor fit:** dialogue or long text (`point-and-click`, `jrpg`), real charts (`data-visualization`), product shots
  (`product-ui`), solemn or tender subjects (`picture-book`), smooth vector motion.
- **Do not:** copy a real game's characters, level names, HUD layout, sounds or logo; break the grid (smoothing,
  fractional offsets, rotation, scaled sprites); add CRT or VHS effects, which belong to other styles.

## Technical notes
- No render.json, fonts or vendored libraries: canvas 2D in `anim.html` (canvas `#screen`). 300 frames render in
  6.7 s on one page (Apple silicon); events.mjs and audio.py take under a second.
- Deterministic (`rng()` with fixed seeds; audio `default_rng(14)`); the determinism test passes on the original and
  the 9:16 version. Wrap a `L.translate()` you add in `save()`/`restore()`.
- Sizes outside `W`/`H`: every value the 9:16 block changes, plus the canvas tag and `SAND_W`.
