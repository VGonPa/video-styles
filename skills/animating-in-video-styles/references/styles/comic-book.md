# Comic Book (`comic-book`)

A 1960s American comic-book page printed on newsprint. Four-colour process is faked with off-register cyan, magenta and
yellow Ben-Day dot screens under a heavy black line, and the camera dives from the whole page into one panel after
another. The joke is gentle, never grim.

**Reference film:** "Captain Clarity vs. the Runaway Robot": a robot vacuum bumps a museum vase, a heroine stops its leap
with a gentle POW! on her palm, it sweeps up, and the page closes on "THE END?" as a second robot peeks in · `styles/comic-book/`

## Signature
- A cream newsprint page lifted off a dark desk, seen whole (`WIDE`, zoom 0.52). The title pops on letter by letter in
  Bangers with a stepped ink shadow (0.15–0.6 s), then the subtitle, the issue line and a double rule.
- Four panels fade in on their own dot-screen grounds as thick black borders ink themselves clockwise, 0.1 s apart
  (0.3–1.05 s): two landscape panels on top, a wide one and a square one below, 50-unit gutters.
- Areas of colour are cyan, magenta and yellow dot screens on a colour plate printed slightly off the black line; only
  lettering, bursts, sparkles and small accents (eyes, lips, lit windows) are flat ink. The dots stay visible at every
  zoom and grow on a dive.
- The camera dives into panel 1 (0.95–1.4 s, 2.5×) and holds still. A yellow caption box unrolls, VROOOM! and BONK!
  burst on letter by letter, and a zigzag balloon pops (all by 2.55 s).
- Every shape is a cream fill, a screen and a round-jointed ink outline 3–11 units thick: no gradients, no blur.

## Palette
| Role | Colour | In code |
|---|---|---|
| Black: line, letters, ink-dot greys, solid hair | `#1b1716` | `INK` |
| Newsprint page | `#efe2c0` | `PAPER`, `newsprint()` |
| Unprinted white: shape bases, balloons, panel grounds | `#fbf6e6` | `CREAM` |
| Desk around the page | `#2e2622` | `DESK` |
| Cyan plate: suit, sky, glass, shading strips | `#2f9fd8` | `CYAN`, `SUIT` |
| Magenta plate: cape, boots, floors, skin dots | `#e0393e` | `MAGENTA`, `RED`, `SKIN` |
| Yellow plate: gloves, caption boxes, sound effects, bursts | `#f5c928` | `YELLOW`, `GOLD` |
| Flat tints under the dots (specs; caption box; belt) | `rgba(47,159,216,0.30)`, `rgba(224,57,62,0.45)`, `rgba(245,201,40,0.55)`, `rgba(240,160,130,0.18)`; `rgba(245,201,40,0.35)`; `rgba(245,201,40,0.95)` | `SUIT`, `RED`, `GOLD`, `SKIN`; `captionBox()`; `hero()` |
| Paper fibres; edge darkening; page shadow | `rgba(150,120,70,0.10)`; `rgba(170,130,70,0.28)`; `rgba(0,0,0,0.55)` | `newsprint()`; `page()` |
| Closing fade ("black ink") | `rgba(20,16,14,${easeInOut(dark)})` | `compose()` |

- A colour is a dot screen (`screen()`), usually over a flat tint of the same ink, both multiplied through
  `overprint()`, which shifts the colour plate by `SHIFT` (5, −4 page units). Secondary colours are two screens
  printed over each other (the painting's green hill is yellow plus cyan).
- Line and lettering are black, unshifted and on top. Greys are ink dot screens on the colour plate (robot shell, dust,
  shadows, the back skyline). Solid black fills (`SOLID`: hair, ponytail) also go through `overprint()`, so they sit
  off register.

## Typography and copy
- `FONT_BANG` = Bangers (`fonts/Bangers-400-latin-J5hm24.woff2`): title (180 units), subtitle (84) and every sound
  effect, always through `boom()`: tracking 0.04 × size, an ink outline of 0.1 × size, a shadow stepped down-right from
  10 to 1 unit, one fill (`YELLOW`, `CYAN`, `MAGENTA`). `FONT_HAND` = Patrick Hand
  (`fonts/PatrickHand-400-latin-ubg58w.woff2`): balloons (46–58), captions (46), the issue line (44, right-aligned).
  `fonts.css` also loads each face's Latin-extended subset. All capitals. Sizes are page units: a 46-unit caption shows
  at 61 px on a 1.32 dive and 24 px on the closing page.
- Measured: Patrick Hand capitals about 0.49 × size each (22.6 at 46), a space 0.23 × size; Bangers about 0.46 × size
  per letter with its tracking ("VROOOM!" 358 at 104, "POW!" 396 at 210, "CAPTAIN CLARITY" 1074 at 180).
- `captionBox()` is one line sized to its text (width + 60, height size + 36), unrolling downward; the longest in the
  demo is 32 characters (606 units). Keep captions under about 40 characters in a 1000-unit panel.
- `speech()` and `robotSpeech()` do not fit the text: you give `rx`, `ry` and hand-broken `lines` (spaced 1.02 ×
  size). Size one from its widest line w and line count n. Oval: `rx` = 0.71 w + size, `ry` = 0.72 n × size + 0.25 ×
  size, which reproduces "NOT ON / MY WATCH!" (227, 98; the demo has 236, 96). Zigzag: `rx` = 0.8 w + 0.4 × size, `ry` =
  0.85 n × size + 0.3 × size. Tested on one to three lines, "BEEP!" to 27 characters. In a 1000-unit panel keep a line
  under about 25 characters at 46, and two to four words per balloon.
- Sound effects: one word of 3–7 letters with "!", 104–116 units inside a panel and 190–220 for the climax and the end
  panel, tilted −0.02 to −0.14 rad, beside their source.
- Voice: pulp narration in captions ("MEANWHILE, AT THE CITY MUSEUM..."), catchphrases in balloons, onomatopoeia for
  every impact, "!" on nearly every line; a hero's name with a "VS." subtitle and an invented issue line.
- Glyphs: a character outside Latin-1 (Ł, Ź, ő) missing from `TEXT_SAMPLE` draws in a fallback serif until its subset
  loads, so frames change face and the determinism test fails (tested): add every new character to `TEXT_SAMPLE`.
  Greek and Cyrillic need other font files.

## Texture and finish
- `NEWSPRINT`, built once by `newsprint()` at half page size: warm per-pixel noise (±8 levels around `PAPER`), a faint
  wave, 900 short fibres, edge darkening. `page()` draws it as the sheet with a soft shadow on the desk, then again over
  everything, multiplied at 0.55, so ink and colour look printed into the paper.
- Dot screens: `screen(col, r, cell, ang)` is a cached pattern turned `ang` degrees: cyan at 15°, magenta at 75°,
  yellow at 45°, ink at 30–45°. Demo cells are 8–18 units with radii 1.9–9, so 11–24 px on screen at zoom 1.32.
- `gradedScreen(area, col, radiusAt, cell, ang)` sets each dot's radius from its position (angle in radians here). It
  makes the sun glow in panel 2 and the POW radiance, the style's only gradients.
- No fade-in (frame 0 is the blank page). `compose()` fades to dark ink over 9.5–9.97 s with `easeInOut`.

## Shapes, line and figures
- `printShape(shape, spec, lw)` paints in this order: a `CREAM` base, the spec's screen and tint, then `outline()`
  (round joins and caps, `INK`). Shapes are closures from `blob()`, `capsule()`, `tube()` and `rectShape()`.
- Weights in page units: panel borders 10, POW burst 11 and 7, balloons 8 (zigzag 7), caption box and robot 7, figures
  4.5–6, interior detail 3–4. The line is uniform: no taper, hatching or feathering.
- The heroine is a jointed profile figure: `hero(p)` draws cape, limbs, torso and belt, neck and head from a pose
  (`flyPose(t)`, `standPose(t, raise)`). The head is built from `FACE`, `HAIR` and `MASK` and scaled by hand in
  `heroHead()`, so its dots stay in page units. A new person keeps the joints and head and changes costume and hair.
- `robot(cx, groundY, scale, o)` is scaled with `pen.scale`, so its dots scale too. Effects: `speedBurst()` (ink wedges
  clipped by the panel), `starburst()` (a spiky outline stretched 1.25× sideways), streaks and speed lines in plain ink.
- A new object belongs when it is a cream shape with one screen (two overprinted for green, orange or purple), a 6–7
  unit outline, 3–4 unit interior lines, a darker screen strip down its right side for shade, and an ink-dot ellipse
  shadow (`screenFill()` with `INK`, radius 3.4–4.2, cell 12, 45°). Skin is fine magenta dots (`SKIN`).

## Composition and camera
- `PAGE`, the title block and `BOX` are in the format table's 16:9 column: a title band, then four panels with
  100-unit margins and 50-unit gutters, read in Z order.
- Inside a panel: a caption box at a top corner (36, 34 from the box); a ground band in the lower quarter (a magenta-dot
  floor with receding board lines); characters on the ground line; sound effects beside their source; balloons above
  the speaker with the tail toward it. The climax panel is flooded with radiance and speed lines.
- `camera(t)` follows `STOPS` with `easeInOut`: 0.45 s for the dive and pans, 0.55 s for the pull back; dives centre a
  panel at 1.32 (P1, P2) or 0.99 (the wide P3). Holds are dead still, because slowly moving dot screens change every
  pixel; only the closing page drifts (0.53 → 0.545, 8.2–10 s). Other formats: Adapting.

## Motion
- Easing: `easeOut` (cubic) for border inking, caption unrolls and arrivals; `easeInOut` for camera, sweep and fade;
  `backOut()` overshoot for every pop (balloons 2.4, letters 2.6, the burst 2.4, the fly-in 1.3, arm raise 1.6, peek
  1.8). `boom()` pops letters one after another, alternate ones nudged up or down and leaning opposite ways.
- Impacts: a contact frame (BONK!, POW!) and then damped sine motion. The vase rocks, the robot squashes and is knocked
  back, the heroine recoils 10 units. Dizzy stars orbit for 0.35 s; streaks and shrinking dust puffs trail a charge.
- Idle motion keeps running (cape flap, ponytail flick, breathing, the flyer's bob, antenna sway, brush spin, sparkle
  twinkle); text never leaves. Never: cuts, cross-fades, camera shake, motion blur, frame stepping, drift in a hold.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.7 | Blank page on the desk to 0.15; title pops; subtitle, issue line and rule fade in 0.4–0.7 | `WIDE`, `titleBlock()` |
| 0.3–1.05 | Panels fade in, borders ink clockwise, 0.45 s each, 0.1 s apart | `PANELS`, `inkBorder()` |
| 0.95–1.4 | Dive into panel 1 | `STOPS`, `camera()` |
| 1.3–1.55 | Caption unrolls | `captionBox()` |
| 1.35–1.95 | Robot charges in with streaks and dust; VROOOM! 1.45–1.8 | `museumScene()` |
| 1.95–2.25 | Bump: BONK!, the vase rocks, the robot is knocked back | `BUMP` |
| 2.25–2.55 | Zigzag balloon; hold to 3.1 | `robotSpeech()` |
| 3.1–3.55 | Pan to panel 2; caption 3.4–3.65 | `STOPS` |
| 3.45–3.95 | Heroine flies in with overshoot and speed lines; WHOOSH! 3.55–3.9 | `cityScene()`, `flyPose()` |
| 4.05–4.4 | Balloon "NOT ON MY WATCH!"; hold to 5.0 | `speech()` |
| 5.0–5.45 | Move to panel 3; the robot charges (5.3) and leaps; she raises her palm (5.4–5.7) | `showdownScene()` |
| 5.85–6.25 | Hit: radiance spreads (0.35 s), the POW burst grows, POW! letters, the robot bounces back | `HIT`, `starburst()` |
| 6.2–6.55 | It lands, dizzy stars, turns happy (6.3–6.42); caption | `robot()` |
| 6.5–7.4 | Sweep: the dust pile shrinks, sparkles appear; balloon 7.0–7.3 | `PILE`, `GLINTS` |
| 7.65–8.2 | Pull back to the whole page | `STOPS` |
| 8.0–8.75 | THE, then END? 0.12 s later, pop in panel 4; a second robot rises from the bottom edge (8.45–8.75) and blinks at 9.43 | `finaleScene()` |
| 9.5–9.97 | Fade to dark ink | `compose()` |

- A panel beat: the border is already inked; the camera arrives (0.45 s); the caption unrolls; the action with its
  sound effect; the balloon; about 0.55 s held complete; the camera leaves with the balloon still in view.
- KEYS for contact_sheet.sh: 2.6 (panel 1), 4.6 (panel 2), 6.06 (burst at its largest), 7.5 (panel 3), 9.3 (page).
- The demo's ending is too short to copy. Holds are measured against the same frame with every scene clock at its end
  (idle terms and camera on `t`); settled means no pixel differs by more than 2 levels.
  - The vase's damped rock never reaches zero and keeps a few dot-screen pixels moving: stop it 2.5 s after the bump
    (since < 2.5, a sub-pixel cut). Then the demo settles at 8.767 s and the robot blinks at 9.433: 20 frames (0.67 s).
  - Tested fixes, both with the rock stopped and no blink, both 29 frames: (1) keep the lettering times and fade over
    9.67–9.97 (settled 8.767–9.700); or (2) THE `span(t, 7.85, 8.15)`, END? `span(t, 7.97, 8.3)`, peek
    `span(t, 8.3, 8.6)`, cues `ding` 7.85 and `beepq` 8.35 (settled 8.600–9.533; THE pops during the pull back).

## Sound
- audio.py reads a flat list `{t, k}` with no other fields and synthesizes each cue in NumPy. The mix is mono, copied
  to both channels: with no pan, no cue value can turn it to NaN.
- Kinds: `paper` (a 0.12 s woodblock tick); `vroom` and `vroom2` (a rising motor of 0.65 s and 0.45 s); `bonk` (a
  falling blip and a woodblock); `beep` (three square beeps and a noise burst, 0.45 s); `whoosh` (0.7 s of swelling
  filtered noise); `boing` (a 0.35 s rising chirp); `pow` (a deep thump, a noise hit and a click); `boop` (two rising
  blips); `sweep` (five short whooshes over 0.9 s); `sparkle` (three high pings); `ding` (two bells 0.12 s apart,
  ringing 1.72 s); `beepq` (a questioning beep).
- No music, bed or fixed times: re-timing `CUES` re-times the score. Set `DUR` to the film (tested 4.0–9.2 s).
- Breakers, tested: a negative `t` stops audio.py with a ValueError, or wraps a short sound more than its length before
  zero to the end (a `paper` at −0.5 sounds at 9.5 s). A cue at or past `DUR` and an unknown kind are dropped silently.
  Skipping cues outside 0 to `DUR` at the top of the cue loop removes the crash.
- The master is `np.tanh` soft clipping with no fade-out: send each cue its own length before the end. `ding` (1.72 s)
  may start 1.6 s before the end; its tail is then below −40 dBFS (the 6 s and 4 s plans).
- A new film sends `paper` per panel, a sound for each sound-effect word (`vroom`, `bonk`, `whoosh`, `pow`), one per
  balloon (`boing`, `beep`, `boop`) and `ding` with the end lettering. Captions are silent. No cue is looked up by name.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Newsprint | `anim.html` → `newsprint` | built once in `prepare()` from `PAGE`; `page()` draws it under and over | as is |
| Dot screens, plate shift | `screen()`, `overprint()`, `screenFill()`, `tintFill()`, `gradedScreen()`, `SHIFT` | `screen(col, r, cell, ang)`; `screenFill(shape, col, r, cell, ang)` | as is |
| Printed shape | `printShape()`, `ink()`, `outline()` | `printShape(shape, spec, lw)`; `ink(dot, r, cell, ang, tint)` makes specs `SUIT`, `RED`, `GOLD`, `SKIN`, `SOLID` | as is |
| Geometry | `blob()`, `capsule()`, `tube()`, `rectShape()`, `areaShape()` | closures that build a path; `capsule(a, b, ra, rb)`, `tube(spine, radii)` | as is |
| Sound-effect lettering | `boom()` | `boom(text, [cx, cy], size, rot, prog, fill, shadow)` | as is |
| Balloons, captions | `speech()`, `robotSpeech()`, `captionBox()` | `speech({ at, rx, ry, tail: [tipX, tipY, a0, a1], lines, size }, prog)`; zigzag `tail: [tipX, tipY]`; `captionBox(at, text, size, prog)` | as is; size balloons by the formulas |
| Effects | `speedBurst()`, `starburst()`, `sparkle()`, `dust()` | `speedBurst([cx, cy], r0, count, seed)`; `starburst(R, spikes, seed, jitter)` | as is |
| Page and panels | `PAGE`, `BOX`, `PANELS`, `paintPanel()`, `inkBorder()`, `titleBlock()`, `page()` | `PANELS` row: box, start, base screens, scene | adapt: layout, title |
| Camera | `STOPS`, `camera()`, `compose()` | `{ t, v: { x, y, z }, ease }`, a pair per panel | adapt |
| Heroine | `hero()`, `heroHead()`, `flyPose()`, `standPose()`, `glove()`, `arm()`, `leg()` | pose of joints; head radius 40 | adapt: costume, poses |
| Robot, scenes and props | `robot()`, `museumScene()`, `cityScene()`, `showdownScene()`, `finaleScene()`, `columns()`, `vase()`, `skyline()`, `PILE`, `GLINTS` | `robot(cx, groundY, scale, o)`; times and positions are literals | replace |
| Copy, fonts | `TEXT_SAMPLE`, `prepare()`, `FONT_BANG`, `FONT_HAND` | every new character goes in `TEXT_SAMPLE` | adapt |
| Cues | `CUES`, `window.events` | `[time, kind]` rows | replace |

## Adapting
- **Style vs demo plot:** always the style: the newsprint page with title and inked panel grid, off-register CMY screens,
  the heavy line, captions, balloons, `boom()` lettering, the dive into each panel with still holds, the pull back and
  the end lettering. Plot: the robot, vase, flight, sweep and peek gag. A transformation: the climax burst flooding a
  panel, a character changing state (the mood flip), or the page completing on the pull back.
- **New subject:**
  - Move `STOPS` to the new panel centres; rewrite `CUES`, `TEXT_SAMPLE` and the title block. Times are literals in the
    scenes (`BUMP`, `HIT`, every `span()` and the bare thresholds 1.35, 1.4, 3.45, 3.95, 5.3, 5.62, 6.1, 6.2, 6.45, 8.8
    and 8.9), `PANELS`, `STOPS`, the fade in `compose()` and `CUES`.
  - Sparkles left by a sweep: `showdownScene()` draws a glint once `broom` passes its x + 60. Every `GLINTS` x must
    therefore lie between the sweep start − 60 and the sweep end − 140, or it shows before the sweep (below) or never
    fully appears (above; the demo's glint at 1390 is never drawn).
  - Stand-in test: a tall potted cactus (overprinted cyan and yellow, `RED` pot), drawn with the same call as `robot()`,
    reads in the style. Values tied to the robot's squat shape:
    - Its height places the balloons, the sound effects (VROOOM! sat on the cactus until moved above its head) and the
      dizzy stars (groundY − 205); POW! lettering must clear its head (the burst is drawn behind the characters).
    - The peek starts 150 units below panel 4's edge (hiding the 160-unit robot) and rises 200: start a taller subject
      its own height below, and keep its top under END? (box y 530): about 210 units visible in 1:1, 835 in 9:16.
    - Its half-width places the contact point `HIT`: px + 178 is the pedestal's half (72) plus the robot's (106); px +
      156 fits the cactus. It also places the dust and streak offsets (+150, +170).
- **Length:** past 10 s, add panels at about 2–2.5 s each (a 0.45 s move, the action, a balloon read at about 4 words a
  second). A page may hold four to six panels (untested); a second page needs a transition the code lacks (untested).
- **Shorter:** the demo is near its minimum. Tested minimums: page build 0.67 s (no fade-in, so the signature starts at
  frame 0); a camera move 0.4 s; a panel's action plus balloon about 1.25 s; a caption read 0.35 s plus the move away;
  the end lettering 0.55 s; then 0.8 s held and a 0.27 s fade.
  - Re-time with knot maps, one clock per scene (code below), and keep on film time the idle terms that use `t` in
    `museumScene()`, `cityScene()` (bob, `flyPose()`), `showdownScene()` (`standPose()`, twinkle, robot) and
    `finaleScene()`. Phase the flyer's bob from its arrival in film time, or it jumps 3 units on that frame.
  - Remove the periodic blink and stop the vase's rock as in the ending fix. A cue's film time is when its scene's clock
    passes the demo cue time. A clock that waits at that time passes it when it starts moving (`vroom2` at 2.8 s in the
    6 s plan, 0.7 s in the 4 s plan), and a frozen clock never does. Drop a cut beat's cues as well (the 6 s plan's
    `sweep`). Every plan was rendered (contact sheet, audio.py, check_audio.py).
  - 8 s, every panel: one map for all scenes and the camera, `[[0, 0], [0.8, 0.95], [1.2, 1.4], [2.2, 2.55],
    [2.5, 3.1], [2.9, 3.55], [3.6, 4.4], [3.9, 5.0], [4.3, 5.45], [5.7, 7.3], [5.9, 7.65], [6.3, 8.2], [6.55, 8.45],
    [6.85, 8.75], [8.0, 9.9]]`; fade 7.65–7.97; settled 6.867–7.667 (25 frames).
  - Under about 7 s cut whole beats in this order: (1) the dive into panel 2 (draw it settled at demo time 5.0); (2) the
    sweep and closing balloon (hold `sweep` at 0 so the brush idles at 6 rad/s; the clock can then stop at 6.56, caption
    complete); (3) the peek; (4) the dive into panel 1. Keep the page build, one dive, the pull back and the lettering.
  - 6 s, beats 1–3 cut: `STOPS` `WIDE` to 0.6, `MUSEUM` at 1.0 (ease) held to 2.55, `SHOWDOWN` at 3.0 (ease) held to
    4.25, the page at zoom 0.53 by 4.7 (ease) and 0.542 at 6; fade 5.7–5.97; settled 4.867–5.733 (27 frames).
  - 4 s, beats 1–4 and panel 3's caption cut: `WIDE` to 0.5, `SHOWDOWN` at 0.9 (ease) held to 2.1, the page at 0.53 by
    2.5 (ease) and 0.538 at 4; fade 3.7–3.97; settled 2.800–3.733 (29 frames).
```js
// clocks, [film s, demo s]; clk(key, t) is a piecewise-linear lookup. paintPanel calls p.paint(clk(p.key, t), t): each scene
// takes (clock time, film time), actions read the first, idle terms the second. titleBlock and the panel build take clk('page', t).
const KN6 = { page: [[0, 0], [0.85, 1.1], [10, 10.25]], P1: [[0, 0], [0.9, 1.3], [2.15, 2.55], [10, 10.4]], P2: [[0, 5], [10, 5]],
  P3: [[0, 5.3], [2.8, 5.3], [3.2, 5.85], [3.85, 6.5], [4.0, 6.56], [10, 6.56]], P4: [[0, 7.9], [4.3, 7.9], [4.85, 8.45], [10, 8.45]] };
const KN4 = { page: [[0, 0], [0.7, 1.1], [10, 10.4]], P1: [[0, 3.1], [10, 3.1]], P2: [[0, 5], [10, 5]],
  P3: [[0, 5.3], [0.7, 5.3], [1.05, 5.85], [1.7, 6.5], [10, 6.5]], P4: [[0, 7.9], [2.25, 7.9], [2.8, 8.45], [10, 8.45]] };
```
- **Other formats:** a single column kills the dive, so both keep two columns and reshape the panels. Rendered at each
  shot's widest moment and on the closing page; scene values in box coordinates, "demo" meaning unchanged:

| Value | 16:9 (demo) | 9:16, 1080 × 1920 | 1:1, 1080 × 1080 |
|---|---|---|---|
| `FRAME`; `PAGE` | 1920 × 1080; 3050 × 2130 | 1080 × 1920; 2250 × 3500 | 1080 × 1080; 2250 × 2250 |
| `BOX` P1, P2 (x, y, w, h) | 100 and 1500, 340, 1350, 740 | 100 and 1150, 450, 1000, 1415 | 100 and 1150, 450, 1000, 790 |
| `BOX` P3; P4 | 100, 1130, 1900, 800; 2050, 1130, 800, 800 | 100 and 1150, 1915, 1000, 1415 | 100, 1290, 1300, 790; 1450, 1290, 700, 790 |
| `titleBlock()`: title; subtitle; issue; rules | 800, 180; 1860, 196; 2850, 205; y 290, 302 to 2850 | 1125, 190; 600, 330; 2150, 335; y 405, 417 to 2150 | as 9:16 |
| `WIDE`; closing drift | 1475, 1030, 0.52; 0.53 → 0.545 | 1125, 1500, 0.48; 0.48 → 0.493 | 1125, 1125, 0.45; 0.45 → 0.462 |
| `MUSEUM`, `CITY`; `SHOWDOWN` | 775 and 2175, 710, 1.32; 1050, 1530, 0.99 | 600 and 1650, 1157.5, 1.0; 600, 2540, 1.0 | 600 and 1650, 845, 1.0; 750, 1550, 0.77 |
| P1, P2 captions | 36, 34 | 36, 60 | 36, 40 |
| P1 floor, ground; columns; painting x, y, size | 560, 612; 110, 1245; 780, 130, 300 × 210 | 1130, 1182; 95, 905; 470, 210, demo | 600, 652; 95, 905; 500, 160, 260 × 180 |
| P1 pedestal x; its top, cap, arc centre | 470; `oy + 400`, `oy + 384`, `oy + 300` | 330; groundY − 212, − 228, − 312 | as 9:16 |
| P1 VROOOM!; BONK! | 1040, 668; 250, 470 | 640, 960; 160, 790 | 760, 725; 160, 400 |
| P1 balloon; tail | 1010, 430; [−200, 60] | 680, 610; [−70, 230] | 700, 470; [−110, 75] |
| P2 glow centre; skylines (base, heights) | 820, 330; 600 (60–180), 700 (20–140) | 620, 520; 1150 (150–450), 1300 (60–300) | 620, 330; 640 and 750, demo heights |
| P2 flyer x end; y | 520; 470 → 380 | 470; 680 → 580 | 470; 540 → 450 |
| P2 WHOOSH!; balloon; tail | 300, 610; 1070, 170; [−190, 100, 1.9, 2.4] | 290, 830; 630, 310; [60, 180, 1.25, 1.75] | 290, 650; 650, 220; [40, 130, 1.25, 1.75] |
| P3 floor, ground; burst centre; columns; heroine x | 690, 745; 800, 300; 1200, 1760; 330 | 1100, 1155; 680, 710; 870; 230 | 680, 735; 770, 290; 1150; 300 |
| P3 charge, hit (x, y), landing; sweep | 1060, 700, 330, 930; 930 → 1430 | 870, 580, 740, 680; 680 → 870 | 1130, 670, 320, 900; 900 → 1170 |
| P3 `PILE` (x, lift, size) | five, x 1300–1530 | 800, 20, 1.0; 850, 38, 1.2; 905, 14, 0.9 | x 1100, 1150, 1205, lifts and sizes as 9:16 |
| P3 `GLINTS` x (lifts 60, 30, 70, 40, 66) | 980, 1080, 1190, 1290, 1390 | 625, 651, 678, 704, 730 | 845, 891, 938, 984, 1030 |
| P3 caption; balloon; tail | 1180, 34; 1620, 390; [−150, 150, 2.0, 2.45] | 36, 60; 640, 330; [130, 190, 0.9, 1.4] | 729, 40; 1080, 430; [60, 130, 1.2, 1.7] |
| P4 burst centre y; peek x | 330; 600 | 400; demo | demo; 480 |

  - 9:16, checked: in the dives key text stays within frame x 60–925 and y 305–1280, clear of the bands. The panel 1 and
    2 dives show the title's lower edge sliced at the top, and floors, gutter and the next panel fill the bottom band. On
    the page shots the title sits at y 270–370, END? ends by y 1425 and x 912, and a 240 px desk band shows above the page.
  - 1:1: zoom 0.45 leaves about 34 px of desk round the page (at 0.48 it vanishes); captions show at 21 px on the page
    shots. The panel 1 and 3 balloons sit at the robot's height: raise them above a taller subject.

## Boundaries
- **Distinct from:** `golden-age-comic` (pulpy aged 1940s print, crude brush ink; this one is clean 1960s halftone);
  `comic-strip` (black-and-white dry wit); `manga` (black-and-white screentone, tapered G-pen); `clear-line` (flat colour,
  no dots); `dark-comic` (spotted blacks, muted colour); `digital-comic` (airbrushed gradients); `pop-art` (gallery
  images, no panel story); `magazine-cartoon` (one wash panel); `risograph` (fluorescent spot-ink poster, no panels);
  `sunday-strip` (watercolour washes, multi-tier strip); `underground-comix` (boiling cross-hatching, no screens).
- **Poor fit:** dry or understated humour (`comic-strip`, `magazine-cartoon`); brooding stories (`dark-comic`); charts
  and numbers (`stick-webcomic`); long narration (`clear-line`); glossy product heroics (`digital-comic`); a film under
  about 4 s, which cannot fit a page build, a dive and a held ending.
- **Do not:** reproduce a publisher's characters, costumes, emblems, logos, cover corner boxes or trade dress; invent
  the hero, the title and the issue line. No shading outside the dot screens.

## Technical notes
- No `render.json`, no `vendor/`: plain canvas 2D, no GPU. Stills take about 0.1 s each on one worker.
- Deterministic as shipped (stills cmp test at 4.2 and 9.3 s): `seeded()` drives texture, bursts, dust, skylines.
- Scenes and the title block fade in through `globalAlpha *=`; a new drawer that assigns `globalAlpha` ignores the
  panel fade. Wrap every new drawer in `save()`/`restore()`: a leaked `letterSpacing` or `font` changes the width
  `captionBox()` measures, frame to frame.
- Size lives in `FRAME`; render.mjs's 1920 × 1080 viewport does not limit the canvas. Every value in the format table
  is a literal in the code; `newsprint()` follows `PAGE`.
