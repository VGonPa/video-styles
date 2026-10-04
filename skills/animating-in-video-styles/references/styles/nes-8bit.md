# 8-Bit Console (`nes-8bit`)

A cartridge game for a third-generation home console, as it looked on a television: a 256 × 240 picture of 8 × 8
tiles in a handful of hardware colours, enlarged with hard square pixels, a black HUD band, a tiny three-colour hero
and four-channel chiptune (two pulses, triangle, noise). Scenes change the way the hardware could, by scrolling whole
screens and stepping the palette to black. Cheerful, terse and game-like: a quest told as a level.

**Reference film:** "MONDAY QUEST": an office worker runs a work-week stage collecting coffee and dodging emails,
flip-scrolls into a boss room, stomps an inbox monster and touches a weekend flag for LEVEL CLEAR · `styles/nes-8bit/`

## Signature
- A 256 × 240 screen (256 × 480 in 9:16; `VC`) enlarged 4× with smoothing off and centred in black bars, like a console on a
  widescreen set (`SC`, `OX`, `OY` in `render()`). It opens with a palette fade-in from black in four brightness
  steps over 0.36 s, never an alpha fade.
- Hardware colours only: every fill is an entry of the 64-entry `NESPAL` (55 distinct colours), about 16 per film
  through `P`; each character and item sprite has three colours plus transparent, one usually black. Flat fills; no
  dither, gradient, alpha or blending.
- A side-view level on the 8 × 8 tile grid, all on one scrolling plane (no parallax), over a floor of 8-px brick
  rows; a sprite hero about three tiles tall runs on a three-frame cycle, jumps on stiff parabolas and collects
  items that pop a score number (in the demo: an office worker, coffee cups, "500").
- An opaque black HUD band four tiles tall over the playfield: white labels over a six-digit score, hearts for lives,
  an item counter with its icon and a timer (in the demo: COFFEE x1…x3 and a Monday clock from 09:00 to 17:00).
- Every letter in the 8 × 8 Press Start 2P face, thresholded to hard pixels in one palette colour with an optional
  offset shadow, at whole-number scales (HUD 1×, cards 2×, the logo 3×; 4× in 9:16).

## Palette
| Role | Colour | In code |
|---|---|---|
| Black: HUD band, outlines, hair, title screen, dark rooms, cards, shadows | `#000000` (0x0F) | `P.k` |
| White: labels, highlights, enemy bodies, pole, card rules | `#FCFCFC` (0x30) | `P.w` |
| Sky in windows; pale panels, skylines, subtitle and bonus text | `#3CBCFC` (0x21); `#A4E4FC` (0x31) | `P.sky`, `P.lc` |
| Blue: hero's shirt, logo shadow, room floor top; deep blue: night panes, screens, room floor | `#0058F8` (0x12); `#0000BC` (0x02) | `P.bl`, `P.db` |
| Skin; light wall | `#FCA044` (0x27); `#FCE0A8` (0x37) | `P.sk`, `P.cr` |
| Orange: furniture, rails, title rules; brown: skirting, wood shading, coffee | `#E45C10` (0x17); `#881400` (0x07) | `P.or`, `P.br` |
| Red: hearts, badge, boss name and HP, shadows of the clear title | `#F83800` (0x16) | `P.rd` |
| Gold: logo, counters, goal flag, explosion core | `#F8B800` (0x28) | `P.gd` |
| Greens: foliage | `#00A800` (0x1A), `#58D854` (0x2A) | `P.gn`, `P.lg` |
| Greys: floor bricks, metal, © line; light grey: floor top, frames | `#7C7C7C` (0x00); `#BCBCBC` (0x10) | `P.gy`, `P.lgy` |
| Side bars and page | `#000` | `render()` |

- Drawers take a palette index, not a colour (`rect(x, y, w, h, ci)`, `txt(…, ci)`, `grid()` maps), so the limit
  holds by construction; name more `NESPAL` indices in `P` to add colours. A scene's backdrop uses four or five.
- Palette tricks replace effects: `FADE` steps every colour down one brightness row (0x10); the hero cycles `HPALS`
  rows 1–3 each frame for a power-up (row 0 is normal). A colour outside `NESPAL` (a blend) turns black in a fade.

## Typography and copy
- One face, `fonts/PressStart2P-400-latin.woff2` (`fonts.css`). `textCan()` writes a string at 8 px, sets pixels
  above alpha 110 to one palette colour, the rest clear, and caches it; `txt(s, x, y, ci, sc, sh, sho)` draws it at
  whole-number scale `sc` with an optional shadow in colour `sh`, `sho` console pixels down-right; `txtC()` centres.
  In the demo, 2-px shadows: red under LEVEL CLEAR! (2×), orange and blue under the two logo lines (3×).
- Each character is 8 × 8 × `sc`: 28, 14, 9 characters a line at 1×, 2×, 3× within 16-px margins (9:16, left of
  review.md's right band at x 230: 25, 12, 8, and 6 at 4×). The clear card's box holds 12 at 2×; the HUD labels (x 16,
  72, 112, 176) 7, 5, 8, 8 (6 in 9:16); a boss name 10 before its bar at x 96; the goal flag 3 at 1× (for four, widen
  its three rects 8 px left: x − 40, 39 wide; x − 39, 37 wide for both inner rects; the word at x − 37). Longer copy takes a second line
  or the next size down, never a fractional scale.
- Glyphs: the woff2's Latin-1 range (fonts.css `unicode-range`); anything else falls back to a system font that the
  threshold turns ragged. Copy is game text in capitals, lowercase only in multipliers ("x1", "COMBO x5"): a one- or
  two-word title, a stage line, one-word HUD labels, popups of a number or two words with "!", a clear card (fixed
  exclamation, one payoff line, a tally) and a © line with an invented maker. Bakery: FRESH RUN / FLOUR x3 / SHOP OPEN!

## Texture and finish
- None beyond the pixels: no scanlines, curvature, bloom, grain, vignette or dither. The finish is the hard 4× grid,
  the black bars, palette-step fades and frame-stepped flicker; drawing into `VC` and copying once (`render()`) keeps
  every edge on a console pixel. Built at load: every pose in every palette (`HERO`), `COFFEE`, `MAIL`, `HEART`,
  `MUGI`, `PUFF` (`puff()`), `FADE`'s maps; scenery is `rect()` calls per frame.

## Shapes, line and figures
- Sprites are character grids (`grid(rows, map)`, '.' transparent) or a pose skeleton: `makeHero(pose, pal)`
  rasterises `HEAD`, a torso box and jointed limbs from `POSES` (lines 3 px thick for arms, 2 for legs, 2 × 2 hands,
  4 × 2 feet) into an 18 × 25 grid in three colours (outline and hair, skin, shirt). Seven poses ('stand', three run
  frames, 'jump', 'hurt', 'cheer'); facing is a mirrored draw (`spr(c, x, y, flip)`).
- Sizes in tiles: hero about 2 × 3, items one (10 × 10, 18 × 10 in the demo), hearts 7 × 6, explosion 2 × 2 (`PUFF`,
  up to four colours, like the goal flag); a boss about 6 × 5.5 (48 × 44), drawn like background tiles from rects in
  five colours (`drawBoss()`; in the demo a mail tray with eyes, teeth and an unread badge).
- Scenery is rects with 1-px black outlines, two flat tones and a white glint; curves are stepped (a clock is an
  octagon of rects). `floorTiles()`: a highlighted top row, brick rows 8 high, 16-px bricks offset on alternate rows.
- A new object: 8–48 px on whole pixels, three colours (one black) if it moves, four or five if big and static, a
  white glint at most, its states as separate frames.

## Composition and camera
- One side-on plane: HUD band 0–32, playfield, floor top at y 208 (four tile rows of floor); sprites stand on the
  floor line. Repeat scenery at a fixed pitch along x (windows every 96 px) so the scroll reads; enemies and the
  boss on the right, the hero entering from the left.
- Camera: horizontal only, whole pixels; `camX` keeps the hero at screen x 112, left of centre so it sees what comes,
  clamped to the level (`LVLW`); no zoom, rotation, vertical follow or parallax. Screen changes are full-screen
  scrolls: the title slides up as the stage rises in 4-px steps (`BUF_A`, `BUF_B`); a 256-px "flip" pushes the room
  left in 0.5 s as the hero walks with it. A hard landing shakes the playfield ±2 px on alternate frames for 0.3 s,
  the HUD still.
- Cards centre on x 128: the title stacks rule, two logo lines, subtitle, rule, legend strip, PUSH START, ©; the clear
  card is a black box with white rules (24–232, y 54–116), the goal pole under its right end (x 226, top y 120).
- 1:1 changes the canvas and `W`, `H` only (28 / 60 px bars). 9:16 (rendered): the screen grows to 256 × 480, the
  HUD moves below review.md's top band, the world moves down above the caption band, the backdrop grows up to the HUD:

```
9:16  canvas 1080 x 1920; W 1080, H 1920, VH 480 (VW 256, SC 4 -> OX 28, OY 0); new constants HY = 72 (HUD top), GY = 120 (world down)
  render(): const oy = GY + shake; the title-to-stage scroll moves VH (R(VH * seg(...) / 4) * 4, BUF_B at VH - so)
    and its incoming screen is drawOffice(0, GY, L0) with the hero at 184 + GY
  floorTiles(): rows from 208 while y < VH - GY (floor 328-480, the whole caption band)
  drawHUD(): band rect(0, 0, VW, HY + 32, P.k); every label, value, heart, icon and HP cell y + HY (labels 80, values 90, boss row 112)
  drawOffice(): wall rect(0, -16 + oy, VW, 224, P.cr); windowPane at y 0 and 72 (+ oy) instead of one row at 56
  drawBossRoom(): wall rect(sx, -16 + oy, VW, 224, P.k); panes from y 8, 136 tall (glass and vertical bar 11 and 130, both draws; horizontal bar at 74); towers bh = 30 + F(rs() * 70)
  render(): CAFFEINATED! at clamp(R(hx) - 38, 16, 134) (it follows the hero; 156 reached the right band, 4 the frame edge);
    pickup popups at Math.min(c[0] - camX - 6, 206) (the last pickup sits at the level's end, where "500" reached x 1008)
  drawTitle(): after the subtitle line (the rising logo passes behind the ground), floorTiles(0, VW, 0, 120 + oy, P.lgy, P.gy, P.k);
    logo rise 400 px (was 240); rules 88 and 208; logo lines 4x at 104 and 144; subtitle 192; PUSH START 248;
    (c) line 280; legend strip by = 328, no grey line
1:1   canvas 1080 x 1080; W 1080, H 1080; nothing else
```
- 9:16 checked at every shot's widest moment and through the title rise: Signature whole; text in x 92–944,
  y 320–1176; feet at y 1312; bricks in the caption band. Largest one-tone band 16.7 % (level), 18.3 % (title), 16.9 %
  (scroll); black above the rising logo until 0.75 s, as in 16:9. 1:1: 8.5 % (office), 15.9 % (boss room),
  title 16.7 % (20.4 % while PUSH START blinks off), scroll 20.4 % for 0.3 s.
- Stand-in (9:16, a 16 × 32 three-colour robot): all held but what follows the hero's shape: its height (`- 24` in
  the office and room draws, 184 in the flip and scroll, `by - 25` in the legend), half its width (`heroLevelX(t) + 9`
  in `CUP_T`), its front (`+ 12` in `BMAIL`), `R(hx) - 38` and the touch x in `heroRoomXY()` (202; 72 in the no-boss
  room; 5 px from the pole).

## Motion
- Whole pixels everywhere: `rect()`, `spr()` and `txt()` round every coordinate; never smoothing, sub-pixel offsets,
  rotation, fractional scale or motion blur. Runs are linear (`VRUN` 140 px/s; dashes, the goal run included,
  150–200), jumps and drops parabolic (`jumpY(s, y0, y1, h)`; a fall at 900 px/s², y = 176 + 450 t²): no
  anticipation, squash or ease; poses switch on the frame the move starts.
- Cycles step at fixed rates, never interpolated: run 12 fps (three frames), steam 4, wing flap 8, bob 5, boss eyes
  6, idle bob 4, goal flag 6, `CAFFEINATED!` blink 10, power-up palette every frame, PUSH START 2 Hz (15 after START).
- Hardware tricks are motion: a hit throws the hero back 16 px in 'hurt', greys a heart and blinks the sprite on
  alternate frames for 1.1 s; over three projectiles on screen draw on alternate frames (sprite flicker); a struck
  boss alternates a white-and-red flash with a 1-px jolt; a meter fills and drains cell by cell (0.35 s, 0.23 s).
- Things appear and vanish in one frame: popups rise 15 px over 0.5 s and are gone (`popup()`), a puff runs four
  frames, a pole grows in 8-px steps. Only the whole screen fades, in palette steps (0.09 s in, 0.12 s out); never
  dissolves, cuts or eased slides.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.36 | Palette fade-in from black, four steps | `FADE`, `render()` |
| 0.1–1.5 | Logo rises into place by 0.75 in 2-px steps; legend strip from 0.55; PUSH START blinks, START at 1.1, then fast blink | `drawTitle()` |
| 1.5–1.95 | Vertical full-screen scroll: the title slides up, the stage rises with its HUD | `T_SCROLL`, `L0`, `BUF_A`, `BUF_B` |
| 1.95–5.41 | The run: camera follows; pickups at 2.46, 3.05 (during the jump onto a desk) and 5.29 pop "500"; jumps at 2.82, 3.85, 4.45 | `heroLevelX()`, `heroLevelY()`, `CUPS`, `CUP_T`, `J1`, `J2`, `J3` |
| 4.62–5.72 | An email hits: 'hurt' pose, knock-back, a heart greys, the hero blinks 1.1 s | `T_HIT`, `T_LAND`, `T_RES`, `LMAIL` |
| 5.41–5.91 | Flip scroll into the boss room | `T_FLIP`, `T_ROOM` |
| 6.0–6.75 | The boss drops in, lands with a shake; its name and HP bar fill | `T_DROP`, `T_BLAND`, `T_HP`, `bossY()` |
| 6.75–7.43 | A five-mail volley (flickering above three); power-up palette cycle and CAFFEINATED!; the dash bursts the mails, COMBO x5 | `T_FIRE`, `T_POW`, `T_DASH`, `BMAIL` |
| 7.4–8.55 | Jump and stomp at 7.72: flash, HP drains, "5000"; bounce back; nine puffs 7.95–8.55 | `J5`, `J6`, `T_BOOM`, `BOOMS` |
| 8.3–9.05 | Goal pole grows; the hero runs, touches at 8.82, the flag climbs | `T_POLE`, `T_RUN2`, `T_TOUCH`, `drawFlag()` |
| 8.9–9.45 | LEVEL CLEAR! card, a payoff line at 9.1, time bonus tallies while the HUD clock finishes | `T_CLEAR`, `T_WKND`, `T_TALLY`, `score()` |
| 9.5–10 | Palette fade-out, four steps, black from 9.86 | `T_FADE` |

- Reusable beats, in order: the title screen (a black screen whose logo scrolls up over a legend strip of the game's
  sprites, PUSH START blinking, a © line with a year and an invented maker; in 9:16 the strip stands on the level's
  floor), which opens any film longer than about 6 s and costs about 1.1 s → vertical scroll → a run with pickups and
  one hazard → flip scroll → boss (drop and shake, meter fill, attack, power-up, decisive stomp, explosion) → goal
  pole → clear card with a tally → palette fade. Beats last 0.4–0.8 s, overlap the run, and scroll away, never cut.
- Holds: pixel difference against the same frame with every action forced to its end, ambient loops (flag wave,
  steam, flaps, eye bob, blinks) on film time; tallies, the clock, a growing pole, a climbing flag, puffs and popups
  are actions. The title holds 0.767–1.467 (22 frames); the demo's ending one frame (9.467): fix in Adapting.
- KEYS: 1.0 (title), 2.5 (HUD, a pickup popup), 4.67 (hit, 'hurt' pose; the next frame blinks it out), 6.5 (boss
  landed, meter filling), 7.2 (volley, power-up), 7.75 (stomp flash), 8.1 (explosion), 9.3 (clear card; 9.0 fixed).

## Sound
audio.py reads `events.json` (cues `{k, t}`; `music` adds `s`) and writes 48 kHz mono on both channels, `DUR` 10.0,
through a ~90 Hz DC block, a ~12 kHz low-pass, a 0.05 s fade-in, a 0.5 s fade-out and a tanh limiter.
- Sound-chip voices: `pulse()` at 12.5, 25 or 50 % duty, `tri()` in 16 steps, `noise()` from a 15-bit LFSR (`seq`),
  envelopes in 16 volumes (`env()`), drums `hat()`, `snare()`, `kick()`. Music uses two pulses, a triangle and noise,
  but not as four voices: `kick()` is a triangle sweep that sounds over the triangle bass, `hat()` and `snare()`
  overlap, and effects mix on top. For strict hardware voicing, drop the kick or gate the bass on kick beats.
- Music, each part from a named cue: the title jingle (C-major arpeggio, 0.9 s) at `music` with `s` `title`; the
  stage theme (150 bpm, `E8` 0.2 s: a 25 % pulse `lead`, triangle `bass`, 12.5 % `arp`, drums) from `music` `level`
  to the first `stop`; the boss theme (A minor, `S16` 0.075 s: `blead`, a triangle octave bass, drums) from `music`
  `boss` to the second `stop`; the `fanfare` (three voices and two snares, 1.8 s).
- Fixed lengths: `seqplay()` plays each list once (stage 4.8 s, boss melody 2.4 s after the cue) while drums loop to
  the `stop`: repeat the lists for longer scenes (the lead twice, for example). The fanfare's last note starts 1.08 s
  in: send it 1.8 s before `DUR` to hear it whole (the demo's is cut by the end; the fix's plays under the fade-out).
- Effects, sent by role: `start` (the START press), `jump` (every jump), `coin` (every pickup), `hurt` (a hit),
  `drop` and `thud` (a big arrival and its landing), `tick` and `tickd` (each meter cell filling, draining), `shoot`
  (each enemy projectile), `pop` (each destroyed), `power` (a power-up), `stomp` (the decisive hit), `boom` (each
  puff), `rise` (a goal object appearing), `flag` (reaching it), `tally` (each bonus step). None carries a field.
- What breaks it (tested): no `music` cue with `s` `title`, `level` or `boss`, or no `fanfare`: StopIteration; fewer
  than two `stop` cues: StopIteration or IndexError; a `music` cue without `s` or any cue without `t`: KeyError; `DUR`
  under 0.5 s: ValueError. A first `stop` before `music` `level` silently drops the stage theme. Park unused parts'
  cues past `DUR` (t 99). Unknown kinds and cues outside 0–`DUR` drop; no pan or field, so no NaN. Run check_audio.py.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Virtual screen and upscale | `anim.html` → `render` | draw into `V` (256 × `VH`), one `drawImage` at `SC` 4 to (`OX`, `OY`); `FADE` step at the end | as is; `VH`, `W`, `H` per format |
| Palette | `NESPAL`, `P`, `hex()` | `P` names hardware indices; `hex(i)` gives the colour | as is; add `P` names from `NESPAL` only |
| Helpers, sprites | `mk()`, `rect()`, `seg()`, `clamp`, `rng()`, `grid()`, `spr()` | `rect(x, y, w, h, ci)` rounds and fills; `grid(rows, map)` char rows, char → index; `spr(c, x, y, flip)` | as is |
| Hero builder | `makeHero()`, `POSES`, `HEAD`, `HPALS`, `HERO` | `makeHero(pose, pal)`: joints per pose, `pal` = [outline, skin, shirt]; `HPALS` row 0 normal, 1–3 power-up | adapt: head, torso and joints, or `grid()` frames |
| Pixel text | `textCan()`, `txt()`, `txtC()` | `txt(s, x, y, ci, sc, sh, sho)`; `txtC(s, cx, y, …)` centred | as is |
| Floor tiles | `floorTiles()` | `floorTiles(sx, ex, camX, oy, top, body, seam)` | as is; colours per scene |
| Demo scenery | `drawOffice()`, `drawBossRoom()`, `windowPane()`, `plant()`, `cooler()`, `wallClock()`, `desk()`, `monitor()` | world x minus `camX`; `oy` for shake | replace |
| HUD | `drawHUD()`, `score()`, `SCORE_EV`, `clockMin()`, `pad()`, `HEART`, `MUGI` | `drawHUD(t, room)`; `room` adds the boss name and HP bar | adapt: labels, icon, timer |
| Effects | `PUFF`, `popup()`, the flicker lines in `render()` | `popup(s, x, y, t0, t, ci)` | as is |
| Boss | `drawBoss()`, `bossY()`, `BOSS_X`, `BMAIL`, `BOOMS` | `drawBoss(x, y, t, flash, mouthOpen)` | adapt: a new body, same drop, flash and bar |
| Goal and clear card | `drawFlag()`, the `T_CLEAR` block in `render()` | `drawFlag(x, t, oy)`; card copy literal | adapt: flag word, copy |
| Title screen | `drawTitle()` | `drawTitle(oy, t)`; rise, legend and blink times literal | adapt: logo, subtitle, legend sprites, © |
| Timeline and paths | `T_SCROLL` … `T_FADE`, `J1`, `J2`, `J3`, `J5`, `J6`, `heroLevelX()`, `heroLevelY()`, `heroRoomXY()`, `heroPose()`, `CUPS`, `LMAIL` | | replace |
| Cues | `window.events` | one push per sound, from the timing constants | adapt |
| Chiptune | `audio.py` → `seqplay` | `seqplay(t0, step, notes, ch, g, duty, t_end)`; `pulse()`, `tri()`, `noise()`, `sweep()` | as is; lists, `DUR` |

## Adapting
- **Style vs demo plot:** the style is everything in Signature plus the title screen, palette fades, full-screen
  scrolls, camera follow, stiff jumps, pickup popups, the hit with knock-back and blinking, sprite flicker, the
  power-up palette cycle, a boss (drop, shake, HP bar, flash, puffs), the goal pole, the clear card with its tally and
  the chiptune. The plot is the office, Monday and its clock, the worker, coffee, emails, the inbox monster and its
  99+, CAFFEINATED!, the SAT flag, WEEKEND UNLOCKED, MONDAY QUEST and TINYCART SOFT. Transformations: the counter
  filling, the boss's bar draining to an explosion, the flip into a new room, the clear card.
- **New subject:** cast the brief as a stage. The hero is whoever acts (a courier, a customer, a product's mascot);
  the pickup is the unit the message counts (orders, stars, steps), named in a HUD slot; the hazard and the boss
  are the obstacle as enemies (a bakery: flying rolling pins, then THE RUSH, a ticket printer); the goal object and
  the card carry the payoff (OPEN, with the widened flag; SHOP OPEN!); the timer comes from the brief.
  Traps: `CUP_T` and the volley's bursts come from scanning the hero's path (move a jump, they move); `LMAIL` rows are
  [x at a reference time, that time, speed, y]; literals: 8, 172, 120 (150 after the fix), 202 in `heroRoomXY()`, 432 and 456 in the flip,
  the HUD's lives and three-cup drain, the popups' strings, `score()`'s values, START's 1.1 in the blink and the
  `start` cue; `T_GONE` is unused.
- **Length:** add 70–110 px of level per beat (pickup, jump, hazard), raise `LVLW` and the window count in
  `drawOffice()` (5); more volleys lengthen the boss; past 15 s, a second stage after another flip. `clockMin()`
  stretches to `T_TALLY`; in audio.py set `DUR` and repeat the lists. A run with nothing happening for a second tires.
- **Shorter:** re-time actions and their cues only; ambient loops run on `t`, untouched. To 8.5 s keep every scene:
  shorten the title (rise 0.5 s, still 0.3, scroll 0.3), the flip (0.4) and the boss's intro, and cut the run's
  quietest beat (the demo's jump over the first email, 80 px; shortest tested title: logo seg(t, 0.1, 0.55), legend
  and START from 0.55 and 0.65, T_SCROLL 0.85, L0 1.1, still 0.567–0.833). Below that drop the boss fight and its
  theme (about 2 s), ending in a goal room with only the pole; at about 6 s drop the title too (a tested 6.2 s cut
  kept it only by also losing the quietest beat), opening on the level: the signature is complete when the 0.36 s
  fade-in ends. For 4 s drop the hazard and the hit. Keep the HUD, the clear card and the fades. Dropped times go to
  99, named music cues stay. Each plan passed events.mjs, audio.py, check_audio.py, the hold measure and a
  frame-by-frame text overlap check (left: puffs passing behind the rising flag, up to 7 frames):

```
All: tally cues T_TALLY[0] + i * (T_TALLY[1] - T_TALLY[0]) / 8 in window.events (was i * 0.35 / 8); popups '5000' at x 190 and
  'COMBO x5' at x 24, CAFFEINATED! until J5[0] (was 7.55; all three crossed the hero); T_FADE = DUR - 0.4
  (black, T_FADE + 0.36, by the last frame DUR - 1/30) and at least 0.81 s after T_TALLY[1] (25 held frames)
With a boss: J6 bounces back to x 150 and the goal run starts there: in heroRoomXY() 172 - 22 * s, [150, 208] and
  150 + (202 - 150) * seg(t, T_RUN2, T_TOUCH) (was 52, 120, 120: a 234 px/s run in the fix)
10 s fix: T_POLE 8.12, T_RUN2 8.12, T_TOUCH 8.47, T_CLEAR 8.47, T_WKND 8.55, T_TALLY [8.55, 8.75], T_FADE 9.6; legend strip t > 0.75
  (it appeared under the rising logo). Final hold 8.767-9.567 (25 frames; 16:9, 9:16, 1:1), black 9.96; peak 0.566
8.5 s, every scene: logo seg(t, 0.1, 0.6), legend t > 0.6, START 0.75 (blink and cue); T_SCROLL 0.95, L0 1.25;
  J1 [2.121, 2.621], T_FALL 2.7, J2 [99, 99.5], J3 [3.171, 3.671], T_HIT 3.341, T_LAND 3.711, T_RES 3.771;
  LVLW 368, CUPS [[100,197],[182,134],[340,197]], LMAIL [[329,3.421,110,192],[xHit + 6,T_HIT,130,150]], second plant x 264;
  flip hero x = LVLW - 16 + 24 * seg(t, T_FLIP, T_ROOM); T_FLIP 4.137, T_ROOM 4.537;
  T_DROP 4.6, T_BLAND 4.9, T_HP 4.95, T_FIRE 5.3, T_POW 5.5, T_DASH 5.55, J5 [5.9, 6.22], J6 [6.22, 6.6], T_BOOM 6.45;
  T_POLE 6.62, T_RUN2 6.62, T_TOUCH 6.97, T_CLEAR 6.97, T_WKND 7.05, T_TALLY [7.05, 7.25], T_FADE 8.1; DUR 8.5 (audio.py too)
  Title still 0.633-0.933; final hold 7.267-8.067 (25 frames); peak 0.566
6 s, no title (16:9, 9:16): T_SCROLL 0, L0 0 (the fade-in plays over the level); music 'title' cue at 99, no 'start' cue;
  the demo's level 1.95 s earlier: J1 [0.872, 1.372], T_FALL 1.45, J2 [1.9, 2.4], J3 [2.5, 3.0], T_HIT 2.67, T_LAND 3.04,
  T_RES 3.1, LMAIL [[325, 2.15, 110, 190], [409, 2.75, 110, 192], [xHit + 6, T_HIT, 130, 150]]; T_FLIP 3.46, T_ROOM 3.96;
  no boss: T_DROP, T_BLAND, T_HP, T_FIRE, T_POW, T_DASH 99, J5 [99, 99.3], J6 [99.3, 99.6], T_BOOM 99.4 (its cues fall past DUR);
  pole drawFlag(96, t, oy); heroRoomXY(t) returns [8 + (72 - 8) * seg(t, T_RUN2, T_TOUCH), 208]; heroPose() after T_ROOM:
  'stand' until T_RUN2, run until T_TOUCH, then 'cheer' (replacing the T_DASH ... lines);
  T_POLE 3.96, T_RUN2 4.01, T_TOUCH 4.33, T_CLEAR 4.33, T_WKND 4.41, T_TALLY [4.41, 4.61], T_FADE 5.6; DUR 6
  Final hold 4.633-5.567 (29 frames, both formats); peak 0.568
4 s, no title, no hazard (16:9, 9:16): opening, no-boss room, pole, path and poses as 6 s;
  J1 [0.871, 1.371], T_FALL 1.45, J2 and J3 [99, 99.5], T_HIT 99, T_LAND 99.37, T_RES 99.43; CUPS [[100,197],[182,134]]; LMAIL [];
  LVLW 288, T_FLIP 1.771, T_ROOM 2.121, flip hero x as 8.5 s;
  T_POLE 2.121, T_RUN2 2.121, T_TOUCH 2.441, T_CLEAR 2.441, T_WKND 2.521, T_TALLY [2.521, 2.721], T_FADE 3.6; DUR 4
  Final hold 2.733-3.567 (26 frames, both formats); peak 0.568
```
- **Other formats:** Composition and camera's values (rendered with the fix, the 6 s and 4 s plans): 9:16 adds height
  above and below the action instead of scaling it; 1:1 needs no recomposition; the hero stays on screen to the end.

## Boundaries
- **Distinct from:** `pixel-art` is a 16-bit level: 320 × 180 at 6× filling the frame, about 44 colours, dithered
  gradients, parallax, ink-ringed sprites and font, a translucent HUD, colour cycling, mosaics, one groove and a
  fanfare. `vector-arcade` draws glowing beam lines on a black tube in three phosphors with persistence and a stroke
  font, no pixels or fills, and arcade board sounds, not music. `handheld-lcd` has four greens and ghosting; `jrpg`
  16-bit battle menus; `point-and-click` painted rooms and dialogue; `dither-1bit` two inks; `voxel` 3D blocks.
- **Poor fit:** dialogue or long text (`point-and-click`, `jrpg`), real data (`data-visualization`), product
  walkthroughs (`product-ui`), solemn or tender subjects (`picture-book`), smooth or detailed motion (`vector-arcade`
  for line-drawn arcade energy).
- **Do not:** copy a real game's characters, level layout, HUD, tunes, sounds or logo, or show a real console or
  publisher name: invent the game and maker (as MONDAY QUEST, TINYCART SOFT). Keep sprites and music made in code:
  THIRD_PARTY_NOTICES.md covers only the font (OFL; keep its licence with the project) and the palette's values.
  No CRT, scanline, bloom or VHS finish, dither (`pixel-art`), smoothing, alpha, rotation, fractional scale or colour
  outside `NESPAL`.

## Technical notes
- No render.json, vendor folder or WebGL: Canvas 2D (canvas `#c`), fonts.css, one woff2; 300 frames in about 4 s on
  one page (Apple silicon). Deterministic: `rng()` with fixed seeds (77, 40–42), byte-identical in 16:9 and 9:16. No
  drawer touches `globalAlpha` (it would make colours the fade cannot map).
- `OX`, `OY` derive from `W`/`H`; `VW` 256, `VH` 240 (480 in 9:16), the floor line, HUD rows and scenery y are
  literals: the 9:16 block lists every change, plus the canvas tag.
