# 80s Anime (`anime-80s`)

A 1980s cel-anime TV opening with a city-pop mood: ink-lined characters and props in flat cel colours, held at
12 drawings a second, over hand-painted backgrounds that pan smoothly. Nostalgic, romantic and unhurried.

**Reference film:** a driver in an original red convertible cruises a coastal highway at sunset, a flare cuts to
her profile, an iris opens on the night city and "MIDNIGHT COAST" slams in · `styles/anime-80s/`

## Signature
- A hand-painted background behind the cels, in soft gradients and visible brush strokes, lit from one dramatic
  source, a low sun or neon night (in the demo: an indigo-to-amber sunset sky, cel-shaded cloud banks lit amber from
  below, a pale sun on the horizon, a teal sea with glitter; `paintSky()`, `cloudBank()`).
- Flat cel figures with a plum ink line (`P.ink`): one hard-edged shade, a warm rim on the lit side, opaque cream
  glints on glossy surfaces and a highlight ring on hair (in the demo: the car body; a lilac ring on plum hair).
- Characters on held 12 fps cels (`cel(t, 12)`) over backgrounds that pan at a smooth 30 fps with deep parallax:
  a foreground object whips past with a ghost smear (palms in the demo).
- Film finish: lens flare streak and ghost discs, bloom, warm bleed, grain, vignette, weave (`finish()`, `flare()`).

## Palette
| Role | Colour | In code |
|---|---|---|
| Ink line on every cel | `#2a1328` | `P.ink` |
| Sky (top to horizon), sun disc | `#2c2455` `#7c3a7a` `#e2657c` `#f6a45a` `#ffdb9c` `#fff3c8` | `P.skyTop` … `P.skyGlow`, `P.sun` in `paintSky()` |
| Cloud shade, mid, lit, hot underside | `#6c3a70` `#b44f80` `#f79a72` `#ffd08c` | `P.cloudShade` … `P.cloudHot` in `cloudBank()` |
| Sea (horizon to front) and its strokes | `#3a6e80` `#244a62` `#172f48` `#4f8c95` `#2d5563` `#e0708a` | `P.sea0` … `P.sea2`, `P.teal`, `P.tealDk` |
| Car body, shade, sunset reflection band | `#d42a3e` `#8c1a3c` `#ff7a64` `#ffc070` | `P.red`, `P.redDk`, `P.redHi`, `drawCarSide()` |
| Hair base, mid, highlight ring, sun rim | `#3b2358` `#5a3478` `#c78ad0` `#ffb070` | `HAIR` |
| Skin, shade, lit; eye iris | `#ffd6bc` `#e08a8a` `#ffe9c8` `#1f4a5c` `#4fb0b4` | `skin`, `skinSh`, `skinLit` in `drawDriver()` |
| Jacket, cool shade, warm rim, collar | `#efe4ee` `#9d86b8` `#ffc890` `#4f8c95` | `drawDriver()` |
| Night sky | `#0d0c26` `#1f1846` `#3b2458` `#8a3a6a` | `P.night0` … `P.night2`, `initC()` |
| Night skyline, windows, neon bars | `#3a2c68` `#221a48` `#ffd27a` `#9ff0e8` `#ff8fb8` `#ff4fa0` `#4ff0e0` | `initC()` |
| Title fill (top to bottom), extrude; tagline slab and text | `#fff6d8` `#ffd070` `#ff8a4a` `#ff4f8a` `#b02a8a` `#130a2c` `#2a1a5c` `#fff4e4` | `initTitle()`, `drawTitle()` |
| Colour-bleed tint, vignette edge, default flare tint | `#ff5a3c` `rgba(20,6,24,.55)` `[255, 190, 120]` | `finish()`, `initFX()`, `flare()` |

- Gradients only in painted backgrounds and glows; characters and props are flat two- or three-tone cel fills.
- One light direction and one world per shot: sunset gives amber rims and reflection bands; night gives cyan and
  magenta edges (`rgba(160,230,240,.55)` in `drawCarRear()`) and darker fills (`#b02240`, `#6a1236` shade).

## Typography and copy
- `fonts/RussoOne-400-normal-400-latin.woff2`: the title only, uppercase, 160 px (`TT.size`). `initTitle()`
  prerenders each letter: italic shear, stepped extrude (18 px) down-right, dark 16 px stroke, sunset gradient split
  hard from amber to magenta, three speed cuts (5, 7, 9 px), a white shine stripe (8 px), a cream hairline (3 px):
  the period chrome logo. Those sizes are pixels: scale them by `TT.size / 160` far from 160.
- `fonts/BarlowCondensed-italic-600-latin.woff2`: the tagline, uppercase, 38 px, on a sheared magenta slab.
  `fonts/BarlowCondensed-normal-600-latin.woff2`: small signage (the plate "MC 85" in `drawCarRear()`).
- Fonts cover Latin-1 only (`fonts.css`): no Japanese, Cyrillic or Central European letters. Load each face in
  `window.ready` before `initTitle()` runs, since it measures the letters once.
- Copy is a TV-series opening: a one-to-three-word show title, then an episode tagline ("EPISODE 01 · AFTER THE
  SUN GOES DOWN" in the demo). Evocative, never jokey; no captions over the action.
- Width: "MIDNIGHT COAST" is 1510 px at 160 px (about 108 px a letter with the gap; M and W 145–160 px): at most
  15 characters per line in 16:9, or lower `TT.size`. Two lines: `initTitle()` reads `TT.words` and overwrites
  `TT.letters`, so pass the words in, keep one letters array, one y per line (1.07 × `TT.size` apart) and one
  letter index. `drawTitle()` puts slab and tagline 150 px below `TT.y` (the last line), the glint 70 px above
  (the first) and sweeps it ±700 px, the demo title's half-width: match it. Tagline: about 14 px a character,
  under about 55, or widen the 940 px slab.

## Texture and finish
- `finish(out, src, t, o)` composes the scene canvas onto the output each frame: gate weave of ±1.2 px held at
  12 fps; colour bleed (a copy tinted `#ff5a3c`, lightened in at 0.35, 5 px right); bloom (480 × 270, blurred
  10 px, screened at `o.bloom`, 0.32); six 960 × 540 grain canvases from `initFX()` cycled at 12 fps under overlay
  at `o.grain` (0.16); the plum vignette; zero to three dust specks or hairs per cel; `o.fade` for fades.
- Backgrounds are painted once in the init functions (soft horizontal strokes, `dabs()`) and only moved per frame.
- `flare(g, x, y, k, col)`: radial core, 1800 px horizontal streak and five coloured ghost discs on the line
  through the frame centre, all additive. A weak flare rides the low sun through every sunlit shot; a strong one
  cuts. Water glitter (the demo's sea) is 60 short dashes under the sun, redrawn per held cel from `rng(500 + …)`
  (40 in the close-up, from `rng(900 + …)`).

## Shapes, line and figures
- Build every cel with `celShape(g, build, fill, line, lw)` (fill, then a round-joined ink stroke) and paint its
  shading with `celClip(g, build, inner)`: a hard-edged darker shape on the side away from the light, an amber
  band or rim on the lit side, and one or two opaque cream parallelograms where the surface is glossy.
- Ink is `P.ink` at about 3–4 px on screen: for a small figure raise `lw` against the scale (`lw: 11` at 0.2 in
  shot A) and drop face details (`detail: false`). Background props take a darker line of their own colour
  (`cols.line` in `paintPalm()`); far layers have none. Outline weight tells foreground from background.
- Machines: original, with period cues (demo car: wedge `carSidePath()`, five-spoke `wheel()`, louvered tail lights).
- People have 80s anime proportions (`drawDriver()`): long neck, sharp nose and chin, a large eye with twin
  highlights and a heavy upper lash, four blush hatches; hair in pointed locks (`hairMass()`, `strand()`) under a
  glossy highlight ring with a zig-zag lower edge. Costume, accessories and eye colour belong to the character (the
  demo's driver: teal eyes, a hoop earring, a padded jacket, hair streaming in the wind).
- A new object belongs when it has a path builder, a flat palette base, one shade and one lit edge in
  `celClip()`, the plum line, and a light direction that matches the shot's light source (sun or city in the demo).

## Composition and camera
- Wide tracking shot (the demo's shot A): side-on, horizon just below centre (`A.HZ` 560), the light source right
  of centre (`A.SUNX`), the moving subject in the lower third (the car at scale 1.22). Layers pan at fractions of
  `A.SPEED` by depth: sky 0.01, clouds 0.025, the far skyline 0.045, the far ground or water plane 0.09, mid props
  0.35, a near rail 0.85, ground marks 1, foreground objects 1.9 with a 35 % ghost copy 60 px behind (in the demo:
  city, sea, mid palms, guardrail, road dashes, palms).
- Close-up (the demo's shot B): one face in profile facing right, the way the subject travels, near centre (`B.OX`,
  `B.OY`, `B.S`), the low light source behind the head (`B.SUNX`), low horizon (`B.HZ`), a foreground edge framing
  one side and the bottom (the car's A-pillar at the right and red door strip), a 3 % push-in, background objects
  smeared past behind the head in four copies (palms).
- Perspective shot (the demo's shot C), one-point: vanishing point `C.VX`, `C.VY`, focal length `C.F`; `projX(X, z)`
  and `projY(Y, z)` place things on the ground (lamps, dashes, the car). The camera tilts up 30 px; the title holds
  the upper third (`TT.y`). One focus per shot (in the demo: the car, then the face, then the title).
- 9:16 (1080 × 1920; rendered):
  - Shot A: `A.HZ` 864 and every absolute y below it moved down 304 (guardrail 1004, road 1084, mid palms 1094,
    streaks 1104, dashes 1176, car 1239; the sea follows `A.HZ`); the car at scale 1.0 drifting from x 390 to 560;
    `A.SUNX` about 760 and the headland city drawn from x −600, not −120, in `drawA()`, or the sun leaves the frame
    or hides behind the towers; the flash-cut flare from (`A.SUNX` + 260, `A.HZ` − 140), which is 16:9's (1500,
    420). Below the road, not a flat verge (y 1264–1920 would be a third of the frame in one tone): on a
    `mk(W, H - 1084)` road canvas a 22 px kerb (#b8a0b8, 5 px #ffc89a lit top, `P.ink` edge lines), then a
    promenade darkening #6e5074 → #4a3458 → #1c1026 with `dabs()` on its own `rng()` seed (the palms keep their
    shapes), and in `drawA()` paving joints 260 px apart panned at 1.35 × the camera, splaying downward, plus two
    faint cross-lines; it stays calm because y 1440–1920 is review.md's bottom caption band (keep subject and
    text above it). Clouds: rows [360, 250, 640, 230, 1], [1120, 160, 560, 190, .85], [820, 470, 600, 200, 1],
    [1340, 420, 520, 210, .8], drawn 170 px lower; the demo's rows fit a 2320 px canvas and leave the sky bare.
  - Shot A palms: heights 1450 and 1350 (for 1050 and 980), bases 40 px below the frame. A crown stands at
    y H + 44 − h; the wide blades end about a third of h below it, the outer blades taper to about 0.45 h and
    their bare spines hang to two-thirds, 0.3 h to each side. For a subject taller than the car raise h until the
    crown and dense canopy clear its head (1900 and 1800 for a cyclist's head at y ≈ 650); the trunk and two outer
    blades still cross the face for two or three frames each, which reads as the whip. The spacing is `fsp`
    (2300) and the phase the `+ 900` in `drawA()`: a trunk crosses the centre at t = (900 − W / 2 + k · `fsp`) /
    (1.9 · `A.SPEED`), 0.18, 1.33, 2.49 and 3.64 s in 9:16; for one whip at t₀ set `fsp` to 3200 or more and the
    phase to W / 2 + 1.9 · `A.SPEED` · t₀.
  - Shot B: `B.S` 1.6, `B.OX` 470, `B.OY` 760 (the jacket then meets the door); in `drawDriver()` `lw` 2.4 (3.6
    draws 6 px lines here) and the `arm` at elbow [−60, 600], hand [250, 470], wheel [212, 300, 326, 700], or the
    fist leaves the frame; `B.HZ` 1250, `B.SUNX` 230; the sea canvas as tall as the frame below `B.HZ`; rail at
    `B.HZ` + 140, palm bases at `B.HZ` + 460; the door strip on the bottom edge, its cream glint moved from
    x 1080–1260 to x 620–800, 18–48 px up; the A-pillar from (1100, 1920) to (960, 900), clear of the hand.
  - Shot C: `C.VX` at `W / 2`, `C.VY` about 1000, the moon at x about 860 (`initC()` draws it from x 1300 to
    1690), `TT.y` about 520, `TT.size` 140 and an 800 px slab, so a title under about
    800 px wide clears the right 12 % band ("MIDNIGHT", 782 px, spans x 138–939; "MOONWAVE", 905 px, reaches
    x 1000: lower `TT.size`), the glint sweep ±400; longer titles on two lines 150 px apart (slab at y 820).
    Camera height 2: ground Y 2, not 1, in every `projY()` call (dashes, lamp bases, car, `C.irisY`), lamp tops
    −1.2, lamps at X ±3.8; at height 1 the kerbs leave the frame 159 px below the vanishing point and a figure
    taller than the car rises into the slab. `initC()` paints road and kerbs to `projX(±3.4, 1)` at y = H, right
    only when `C.VY` + `C.F` = H: paint them to x = `C.VX` ± 3.4 (H − `C.VY`) / 2 (rendered: car and cyclist).
- 1:1 (1080 × 1080; rendered): shot A as in 9:16 but `A.HZ` 540, y values 20 above 16:9's (guardrail 680, road
  760, car 915, foreground palms 1160), the road canvas 20 px taller (at `mk(W, H - 780)` the verge stops at
  y 1060), the plain verge (13 % of the frame), the demo's clouds and palms, the flare from (1020, 400); shot B
  with `B.OX` 470, `B.SUNX` 200, the A-pillar from (1040, 1080) to (820, 380), the door glint at x 620–800; shot C
  with `C.VX` at `W / 2`, camera height 1 (610 + 470 = H), the moon at about 860, one title line up to 8 letters
  at 160 px, the glint sweep ±450.

## Motion
- Two clocks: `cel(t, 12)` drives what is drawn as animation (car bob and wheels, hair waves, smile, glitter,
  weave, grain, dust, the receding car in shot C, title letters); raw `t` drives pans, parallax, push-ins, flares,
  irises, slab, glint, fades, the on/off blink and the eye sparkle. Shot A's slow forward drift of the car runs on
  raw `t` too: treat it as camera. Held drawings over smooth pans are the look. Secondary motion runs on cels: hair
  and cloth waves, small wobbles and bobs, a machine's jolt every few cels (in the demo: hair waves, a 3 Hz bang
  wobble, a head bob, a car bob that jolts every fifth cel).
- Easing: `eInOut` for camera drifts, the iris closing and the fade-out; `eIn` for the flare swell and the iris
  opening; `eOut` for the slab and the smile; `bump(t, a, b)` for one-shot pulses (eye sparkle, flare strength).
- Overshoot appears once: `eBack` on the title letters (2.2× to 1×). Characters and cameras never overshoot,
  bounce, squash or shake, and no cut is bare: each has a flash or an iris.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.6 | Fade in from black on the sunset drive | `finish()` fade, `seg(t, 0, .6)` |
| 0–3.45 | Wide tracking shot: car drifts forward, foreground palms whip past | `drawA()`, `A.SPEED` |
| 3.45–3.75 | A flare swells across the frame under a warm white wash: flash cut | `flare()`, `T.cutB` |
| 3.75–4.1 | Close-up opens as the wash decays | `T.cutB`, `drawB()` |
| 4.1–6.05 | Profile, hair streaming, push-in; blink 4.55–4.72, smile 5.2–5.6, sparkle 5.55–5.95 | `drawB()`, `drawDriver()` |
| 6.05–6.6 | Iris closes on her eye, then 0.1 s of black | `T.irisA`, `T.irisB`, `iris()` |
| 6.6–7.15 | Iris opens from the taillights onto the night boulevard | `T.cutC`, `T.irisO`, `drawC()` |
| 6.6–10 | Car recedes on held cels, lamps stream past, camera tilts up 30 px | `drawC()`, `projX()` |
| 7.7–8.54 | Title letters slam in, staggered 0.045 s, 0.3 s each | `T.title`, `drawTitle()` |
| 8.25–8.7 | Magenta slab wipes out from the centre, tagline fades in | `drawTitle()` |
| 8.6–9.2 | Glint star sweeps the logo with a pink flare | `drawTitle()`, `flare()` |
| 9.25–10 | Fade to black | `T.fade0`, `T.fade1` |

- Each shot opens on a transition, holds 2.5–3.5 s with one secondary action (blink, smile) and hands over by a
  flash cut or an iris (closing on a detail, opening on the next scene); these and the title slam are reusable.
- The demo's glint ends at 9.2 s and its fade starts at 9.25 s, so it barely holds the finished card; hold a new
  one at least 0.8 s after the glint ends. Key moments for contact_sheet.sh KEYS: 3.73 (flash peak; the square at
  its core is the flare() defect in Technical notes), 4.62 (blink), 5.75 (smile and sparkle), 6.35 (iris on the
  eye), 6.9 (iris opening on the taillights), 9.2 (finished card, before the fade).

## Sound
audio.py synthesizes everything with NumPy (seeded `rs`), soft-clips, fades in 0.4 s and out over the last 0.9 s.
- City-pop bed at fixed times, not from cues: four 2.4 s bars at 100 bpm (`beat` 0.6 s) from 0.35 s, each a `prog`
  chord (Fmaj7, Em7, Dm7, Cmaj7/E) twice on `epiano()`, a five-note `bass()` line on `roots`, swung `hat()`
  eighths. The last, Cmaj7/E, starts at 7.55 s, under the title's C-major sting: start that bar at a new title.
- `engine` (t, `d` = length): the car's low saw drone; for a bike, runner or animal leave it out and let `wind` and
  `pass` carry the speed, or add a cue in the same synthesized character. `pass` (t): a 0.6 s whoosh panned at
  random that peaks 0.3 s in: emit it just before something whips across the centre, in the foreground of a wide
  shot or smeared behind a close-up (in the demo 0.9, 2.05, 3.2 s for shot A's palms, 4.4 s for shot B's).
- `flare` (t): shimmer chord and whoosh at a flash cut. `wind` (t, `d`): gusting noise under open-air close-ups.
  `city` (t, `d`): low night hum with no fade-out: run it to the end of the film or it stops dead.
- `iris` (t, optional `v`): a 0.45 s zip, rising without `v` (closing), falling with any non-zero `v` (opening;
  `v: 0` counts as absent). `sting` (t): six-note brass chord, low C and a thump, 2.2 s, on the title slam;
  `glint` (t): four chimes 0.9 s later.
- audio.py looks up no cue by name and runs with any subset, but `engine`, `wind` and `city` read `d` (KeyError
  without it); `wind` or `city` with `d: 0` raise a ValueError and a `wind` under 0.5 ms gives NaN (silence): keep
  every `d` above a few frames. No field reaches a pan; cues outside 0–`DUR` are dropped silently.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Film finish | `common.js` → `finish` | `finish(out, src, t, o)`: src is the scene canvas; `o.fade`, `o.bloom`, `o.grain`; needs `initFX()` in `window.ready` | as is |
| Timing, maths, palette | `common.js` → `cel`, `P` | `cel(t, fps)`, `seg(t, a, b)`, `eIn`, `eOut`, `eInOut`, `eBack`, `bump(t, a, b)`, `lerp`, `rng(seed)`, `mk(w, h)`; `P.<name>`, `rgba(c, a)`, `mixc(a, b, u)` | as is; add colours as hex in `P` |
| Cel primitives | `common.js` → `celShape` | `celShape(g, build, fill, line, lw)`, `celClip(g, build, inner)`; build is a function that adds path segments | as is |
| Brush texture | `common.js` → `dabs` | `dabs(g, R, n, x0, y0, x1, y1, cols, len, wid, ang, alpha, angJ)`: n ellipses in a box | as is |
| Sunset clouds | `common.js` → `cloudBank` | `cloudBank(g, R, cx, cy, wid, hgt, lit, cols)`; `cols` overrides shade, mid, lit, hot | as is |
| Lens flare | `common.js` → `flare` | `flare(g, x, y, k, col)`: k strength (0.35–0.6 on a sun, up to 2.2 for a cut), col as [r, g, b] | as is |
| Sky and cloud layers | `shotA.js` → `paintSky`, `shotA.js` → `paintClouds` | `paintSky(w, h, hz, sunx, R)`; `paintClouds(w, R, list)` with rows [x, y, w, h, lit] | as is; adapt gradient stops for another hour |
| Palm tree | `props.js` → `paintPalm` | `paintPalm(R, h, lean, cols)` returns { c, ax, ay } (canvas and base anchor); `cols` trunk, lit, leaf, leafDk, line | as is |
| Car, side and rear | `props.js` → `drawCarSide`, `shotC.js` → `drawCarRear` | `drawCarSide(g, x, y, tc, driver)`: origin on the road line, faces right, driver callback draws in the cockpit; `drawCarRear(g, x, y, s, tc)` | adapt or replace with the new subject |
| Profile character | `props.js` → `drawDriver` | `drawDriver(g, tc, o)`: `o.lw`, `o.blink`, `o.smile`, `o.detail`, `o.arm` (elbow, hand, wheel, fistRot); ear at 0,0, crown −200, chin 156; light is baked on the face side (rim on the jacket front, `skinLit` on the brow); faces right and the hair streams to −x | adapt: template for any profile face; flip the shade and rim when the light is behind the figure; for a left-facing figure mirror the whole call with a negative x scale; for a head on another body, clip `drawDriver()` above y ≈ 240 (where the jacket starts), tuck its neck under your collar and raise `lw` against the scale (× 4 at 0.25), or build it from the top-level `skinPath()`, `hairCapPath()` and `hairMass()`; the eye, blush, earring and limb helper `tube()` live inside `drawDriver()`: copy them out |
| Wind-blown hair | `props.js` → `strand` | `strand(g, ax, ay, len, wid, ph, tc, amp, lift, col, hi, lw)`; `hairMass(g, tc, lw)` | as is (also scarves, flags) |
| Flash cut | `anim.html` → `drawFrame` | strong `flare()` from (1500, 420) sliding 500 px left, k up to 2.2 with `eIn` over 0.3 s, under a warm white wash to 0.85; the next shot's wash decays as f² over 0.35 s | adapt: lift into a function |
| Iris transition | `anim.html` → `iris` | `iris(g, x, y, r)`: black frame with a round hole | as is |
| Title card | `shotC.js` → `initTitle`, `shotC.js` → `drawTitle` | `TT` (words, y, size); tagline string and slab inside `drawTitle()` | adapt: new words, timing |
| Perspective road | `shotC.js` → `projX` | `projX(X, z)`, `projY(Y, z)` with `C` (VX, VY, F); camera one unit above the road (two in 9:16) | as is |
| Background builders | `shotA.js` → `initA`, `shotC.js` → `initC` | inline in `initA()`: headland city, stroked sea, guardrail tile, road; inline in `initC()`: night sky, stars and moon, the `skyline` helper (far and near layers with window grids, neon bars, beacons), wet-road streaks; street lamps on `projX()` in `drawC()` | adapt: lift out the layers a new scene needs |
| Demo shots and timeline | `shotA.js` → `drawA`, `shotB.js` → `drawB`, `shotC.js` → `drawC`, `anim.html` → `drawFrame` | `T`, `window.events` | replace |

## Adapting
- **Style vs demo plot:** the style is the brush-painted background lit from one dramatic source (soft gradients,
  brush strokes and glows; the demo's sunset sky, cloud banks, sea and headland city are its setting), the plum line
  with one hard shade and a warm rim, held 12 fps cels over smooth parallax with a foreground whip, the film finish,
  flash cut, iris and chrome title slam. Plot: the driver, convertible, coastal highway, palms, "MIDNIGHT COAST". A
  transformation: the hour turning (sunset to night, as here), an iris from a detail into a new place, the title slam.
- **New subject:** keep `finish()`, the palette, the cel primitives, painted backgrounds, the two clocks, the
  flare and the iris; draw the subject with `celShape()` and `celClip()`. Shot times live in the code, not in
  `T`: `drawB()` uses `t - 3.75`, `drawC()` `t - 6.6` and `seg(tc, 6.6, 9.9)`, `drawTitle()` `t - 7.7`, the flash
  starts at 3.45 in `drawFrame()`, the blink, smile and sparkle are absolute, shot lengths are literals (3.75 in
  `drawA()` and the sun flare, 2.85 in `drawB()`, 3.4 in `drawC()`), and `window.events` uses numbers: derive
  all from `T`. An iris needs its target's screen position, stored by the draw function (`B.eyeX`, `C.irisX`).
- **Length:** add shots in the same grammar rather than stretching one (a held shot past about 4 s goes slack).
  `DUR` in common.js is unread. In audio.py set `DUR`, loop the bed's `for b in range(4)` over more bars with
  `prog` and `roots` indexed by the bar number modulo 4, and size the `d` of `engine`, `wind` and `city`.
- **Shorter:** down to about 7.5 s keep all three shots and trim the holds (three shots of about 2.5 s with the
  flash, the iris pair and the 2.3 s card need that much). Rendered 8 s 9:16: shot A 0–2.5 s, flash from 2.2 s;
  shot B 2.5–5.0 s, blink, smile and sparkle 0.6, 1.1 and 1.45 s after the cut, iris 4.45–4.9 s; shot C
  5.0–8.0 s, title at 5.6 s, fade 7.4–8.0 s. Under about 7.5 s, cut whole shots. Rendered 4 s 9:16 plan: fade in
  over 0.3 s, not 0.6; shot A 0–1.5 s with one whip in the clear (`fsp` 3200, a trunk across the centre at 0.7 s);
  its flash cut swelling from 1.2 s straight into shot C (`drawFrame()` branches from A to C with the wash decay);
  the title at 1.7 s, letters by 2.32 s (8 letters; each more adds 0.045 s: start the glint after the last), slab
  and tagline by 2.7 s, the glint shortened to `seg(lt, .65, .95)` to end with them and its `glint` cue at the
  title + 0.65; the card held 2.7–3.65 s; fade 3.65–4 s. Drop the close-up and the iris pair (1.1 s with its
  black); keep shot C or make its title calls yourself. The card costs about 2.3 s: 1.0 s in, 0.95 s held, a
  0.35 s fade. In audio.py set `DUR` (bars past it drop silently; a late `sting` is cut by the fade-out).
- **Other formats:** set the `<canvas>` size and `W`, `H`; values in Composition, hard-coded sizes in Technical notes.

## Boundaries
- **Distinct from:** `synthwave` (neon grid, wireframe mountains, CRT scanlines, RGB split, VHS glitches, a shake
  on the logo slam; it shares the sunset, palms and chrome logo, so cel characters on held drawings, brushwork and
  a film finish set this style apart); `lofi-anime` (one quiet 90s rainy interior, a single slow push-in, no
  cuts); `manga` (black ink and screentone); `vaporwave` (pastel marble, irony); `cel-shaded-3d` (toon 3D).
- **Poor fit:** charts and numbers (`data-visualization`), technical details and inner workings (`blueprint`),
  step-by-step lessons (`whiteboard`), caption-heavy social posts (`bold-captions`).
- **Do not:** copy characters, mechs, logos or scenes from real anime, or real car models. No katakana or mock
  Japanese (the fonts lack it, and it reads as pastiche): titles in Latin script. Keep characters adult.

## Technical notes
- Dependencies: common.js (maths, `P`, `celShape()`, `finish()`, `flare()`) serves every file; props.js (palm,
  side car, driver) serves shots A and B. `initB()` calls `paintSky()` and `paintClouds()` from shotA.js: keep them
  when you replace shot A. `initC()` calls `initTitle()`, `drawC()` calls `drawTitle()`: a film not ending on shot
  C makes both calls itself. anim.html holds `T`, `window.ready` (fonts, then `initFX()`, `initA()`, `initB()`,
  `initC()`), `drawFrame()` (picks the shot by `T.cutB`, `T.cutC`; draws the flash cut and irises), `iris()`,
  `window.draw` and `window.events`; a new shot needs a script tag, an init call, a `T` key and a branch there.
- No vendored libraries, no `render.json`: plain Canvas 2D, about 45 s for 300 frames with 2 workers.
- Shots draw onto the offscreen `scene` canvas, which `finish()` copies to `cv`. It is never cleared, so the tilt
  in `drawC()` leaves the previous frame in its top rows: fill `scene` with `P.night0` first in `drawFrame()`
  (black shows as a band) and, inside the tilt, draw `g.drawImage(C.bg, 0, 0, W, 30, 0, -30, W, 30)` after the
  background, or the fill shows as a flat strip. Canvas state leaks too: the door's `celShape()` in `drawB()` runs
  outside `save()` and leaves round line joins that change the next shot C frame's lamp posts, so wrap each
  shot's draw call in `drawFrame()` in `save()`/`restore()`, or the determinism test fails.
- Randomness is seeded (`rng(1985)` to `rng(1987)` in the init functions, per-cel seeds in the draw code). Each
  init function takes its whole layout from one stream: a call inserted early reshuffles every later layer.
- `paintPalm()` paints on a canvas 1.15 h tall, slicing upright fronds flat where its top shows (in 9:16): make it
  1.5 h (the second `mk()` argument); the random draws stay the same.
- Sizes tied to the 16:9 frame: the 480 × 270 bloom and 960 × 540 grain buffers in common.js (keep a quarter and
  a half of the frame, or the grain stretches); the vignette radii `H * .35` and `H * 1.05` in `initFX()` (base
  them on the shorter side, or 9:16 loses most of the vignette); `mk(w, 560)` in `paintClouds()`; the flare and
  shot layouts in Composition. The guardrail tile (`mk(1920, 90)`, `% 1920`) covers frames up to 1920 wide. The
  iris radius 1500 must reach the corner farthest from the iris centre: true for shot B's eye in 9:16 (about
  1350 px) and for 1:1, not for a centre in a 9:16 frame's top or bottom quarter, which includes shot C's
  taillights at camera height 2 (about 1645 px). The opening iris's last frame reaches only 0.9 of the radius
  (`eIn`), so use 1850 there in 9:16: at 1700 the top corners are still black at 7.13 s.
- `flare()` fills its core into a fixed 600 × 600 square while the core's radius is 260 k, so above k ≈ 1.15 the
  square's edge shows in the flash cut's last frames: fill `x - 260 * k, y - 260 * k, 520 * k, 520 * k` instead.
