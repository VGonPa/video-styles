# Synthwave (`synthwave`)

An 1980s retro-futurist title sequence seen on a CRT: an endless magenta grid scrolling to a centred horizon, a
banded sunset sun, wireframe mountains and palm silhouettes, chrome extruded lettering that slams in, a cyan neon
script, and a finish of bloom, RGB split, scanlines and VHS grain. It draws on outrun and synthwave cover art and
80s TV openers; the mood is fast, glowing and nostalgic.

**Reference film:** "NIGHT DRIVE": the CRT powers on over a drive toward the sun, "MIDNIGHT ARCADE PRESENTS", twin
lasers open the title view, the chrome logo slams in, "The Long Way Home" writes on, the sun sets under "ALL NEW ·
FRIDAYS 11 PM" and the CRT powers off · `styles/synthwave/`

## Signature
- A one-point-perspective magenta grid that scrolls toward the camera without a seam, fogging into a hot pink haze
  and a bright horizon line at the centred vanishing point (`drawGround()`), whole once the CRT power-on ends (0.5 s).
- A yellow-to-magenta sun on the horizon with horizontal cuts that drift downward and thicken toward its base, in a
  pink halo, clipped at the horizon (`drawSun()`), over a violet-to-pink sky with twinkling stars (`drawSky()`).
- Dark wireframe mountains with cyan and violet wire, low at the centre and high at the edges (`drawMountains()`),
  and black palm silhouettes whipping past on both sides (`drawPalms()`).
- Chrome type: Exo 2 Black Italic with a sky-blue top, a white horizon line, a dark band and a sunset-pink base, a
  30-step magenta extrusion, star glints and a light sweep (`buildTitle()`, `drawTitle()`), slammed in at 3.0 s.
- A CRT/VHS finish on every frame: bloom, an RGB split widening toward the edges, scanlines, grain, vignette,
  CRT power-on and power-off, and short tracking glitches at cuts (`post()`).

## Palette
| Role | Colour | In code |
|---|---|---|
| Sky, top to horizon, mixed toward dusk by `P.dusk`; stars | `#08011c` `#1f0746` `#5a1370` `#c2307f` `#ff6f91`; dusk `#030010` `#0b0228` `#2a0a4f` `#6a1a6e` `#c93f86`; rgba(255,236,255,…) | `drawSky()`, `mix()`, `STARS` |
| Sun disc, top to bottom; halo | `#fff3a0` `#ffd24a` `#ff9038` `#ff3f73` `#e0147f`; rgba(255,70,150,…), rgba(255,40,140,…) | `drawSun()` |
| Sun cuts (sky-coloured bars), day and dusk | `#2a0a52` → `#a82a7c`; `#140434` → `#4a1260` | `drawSun()` |
| Far and near ridge: fill, wire; palms; title outline | `#1a0638`, rgba(170,80,255,.55); `#0d0322`, rgba(60,235,255,.85); `#07010f`; `#0a0118` | `drawMountains()`, `buildPalms()`, `buildTitle()` |
| Ground under the grid; horizon haze and line | `#3a0b52` (dusk `#1c0536`) → `#12032a` → `#070113`; rgba(255,110,180,…), rgba(255,220,240,…) | `drawGround()` |
| Grid lines (magenta, bluer at dusk) | `rgba(255,${Math.round(lerp(56, 90, d))},${Math.round(lerp(214, 255, d))},${a})` | `col` in `drawGround()` |
| Chrome face, top to bottom; extrusion near to deep; pink rim | `#16236b` `#2f68d6` `#98d8ff` `#ffffff` `#fbf0ff` `#16041f` `#380c40` `#a82a72` `#ff94b8` `#ffe8ef`; `#ff3fcf` → `#1b0436`; `#ff7ad9` | `buildTitle()` |
| Neon script: glow, tube, core; dark edge | `#00d9ff`, `#18c8f0`, `#7ff3ff`, `#e9ffff`; rgba(8,0,24,.9) | `buildScript()` |
| Orbitron lines: fill and glow; tag band | `#dffcff`/`#00e1ff`, `#ffe3f6`/`#ff2bd6`, `#ffffff`/`#ff2bd6`; underline `#00e5ff`, rgba(180,250,255,1); rgba(8,0,24,.45) | `drawPresents()`, `drawTag()` |
| Lasers; impact band, flash, glints | 0,240,255 and 255,60,220; rgba(255,200,250,…), rgba(255,235,250,…), rgba(200,240,255,…) | `render()`, `glint()` |

- Light is additive and drawn live: `'lighter'` composites, shadow blurs, doubled strokes (a wide faint pass, then the
  core). Darks are only silhouettes, the ground and the top of the sky. The sun's cuts are bars painted in a sky
  gradient, not holes: change the sky and repaint them, or they read as stripes.

## Typography and copy
- Three faces, Latin-1 subsets only (no Greek, Cyrillic, ł, ő, š, ž): Exo 2 Black Italic
  (`fonts/Exo2-italic-900-latin.woff2`, `FT`) for the chrome title, 238 px, 6 px tracking, capitals; Mr Dafoe
  (`fonts/MrDafoe-normal-400-latin.woff2`, `FS`) for the neon script, 148 px, title case, tilted −0.07 rad; Orbitron
  700 (`fonts/Orbitron-normal-400-900-latin.woff2`, `FO`) for tracked capitals: the credit at 44 px over 26 px, the
  tag at 38 px with 12 px tracking.
- Copy is a show open: a one- to three-word title, a three- or four-word script tagline, "X PRESENTS", one schedule
  or call-to-action line. Strings live in `buildTitle()`, `buildScript()`, `drawPresents()`; the tag is written twice,
  in `drawTag()` and `window.events` (its typing ticks). Text enters by slam, write-on behind a hot tip, neon flicker
  (`flick()`) with widening tracking, or typing; the script flickers out, the rest leaves with the CRT power-off.
- Widths (`measureText` on real lines, tracking included). 16:9: title 161.5 px a letter on average (W 243, I 83;
  "NIGHT DRIVE" 1541 px), about 10 letters a line; script 52–63 px a character in title case ("The Long Way Home"
  1034), about 22 a line centred on x 1180; credit 62 px a capital at its final tracking; tag 35 px a character
  (the demo's 25 make 874 px over a 760 px underline). 9:16: a title line up to 755 px at 238 px, scaled down
  beyond (about 5 letters: NIGHT 755, DRIVE 730); script at 110 px 39–47 px a character, about 16 a line (the
  demo's 17 reach x 960, into the right band); credit 52 px a capital at tracking 16, 15 a line; tag at 32 px 27–30 px
  a character ("ALL NEW · FRIDAYS 11 PM" 683; wide capitals run wider: "SEASON TWO · SUNDAYS 10 PM" 824), about 27 a line.

## Texture and finish
- Precomputed in `buildPost()`: `SCAN` (a 1 px rgba(0,0,0,.26) line every 3 px), `VIG` (radial, 0 to .72 black)
  and four 480 × 270 grey `NOISE` frames, drawn `'soft-light'` at .35 and cycled every frame. The title (stroke,
  extrusion and face, no glow), its mask `TMASK` and the script (its cyan glows baked in) are sprites built once.
- Per frame in `post()`: bloom (the frame drawn into `BL1`, 480 × 270, through `'brightness(.85) contrast(1.9)
  blur(5px)'`, then into `BL2`, 240 × 135, blurred 7 px; both added `'lighter'` at .34 and .42); the RGB split
  (`getImageData`: red read from 2–4 px right, blue from 2–4 px left, wider toward the edges); a tracking glitch
  (five displaced strips and a white line, seeded by frame) around `T.wipe`, `T.outro` and `T.off`; noise,
  scanlines, vignette; then the CRT power-on or power-off onto the output canvas.

## Shapes, line and figures
- Two kinds of form: glowing line (grid, wire, lasers) and dark silhouette (palms, ridges); no ink, no shading.
- `ridge()` builds each mountain line once (`MTN_FAR`, `MTN_NEAR`): jagged points under an envelope that is zero
  near the centre, so the sun stays clear. `drawMountains()` fills it dark, strokes the wire, and adds struts from
  each peak to a point pulled 45 % toward the horizon and verticals down to it.
- Palms: three 700 × 1100 sprites (a curved trunk, nine serrated drooping fronds), placed by `PALMS` alternately
  left and right, one every 1.6–3.0 units of z, sized by F / z, mirrored at random, fading in from z 16 to 11.
- Chrome title layers: a 16 px `#0a0118` stroke, 30 extrusion copies (0.55 px right, 1 px down each), white and pink
  rims offset up-left and down-right, the face gradient. The script: a 14 px dark stroke for legibility, cyan blurs.
- A new object belongs as a near-black `#07010f` silhouette on the grid, scaled by the same F / z (a car, pylon,
  skyline), or as a glowing wireframe with a halo stroke.

## Composition and camera
- Symmetric one-point perspective: vanishing point (W / 2, HY), the sun on it, the title centred (`drawTitle()`'s
  cx = W / 2 + 10). Back to front: sky, sun, ridges, grid, palms (far to near), title, script and tag, post.
- Two cameras, each a plain object read by `drawWorld()`: `camA()` the drive (HY 560, F 520, sun R 235 → 285 over
  0–2.8 s, lifted 140), `camB()` the title view (HY 690, F 390, R 330, lift 175 → −350 as it sets, `pw` 1.9 pushes
  the palms out from under the title).
- The grid (`drawGround()`): horizontals at depth z = k · S − (camera z mod S), S 0.45, projected to y = HY + h · F
  / z between `zN` 0.28 and `zF` 46, so the pattern repeats exactly every S and never jumps; verticals k = −44…44 at
  world x k · S, in five depth bands with alpha 1, .9, .65, .38, .16. Fog pow(1 − z / 46, 3.2); width 5.5 / z.
- The code keeps F = H − HY: cells are square at the bottom edge, W · h / (S · (H − HY)) across (11 in the 16:9
  title view, 8 in the drive). Speed: `camA()` z = 7.2 t + 0.6 t² (accelerating), `camB()` 3.4 a second, braking
  after `T.outro`; a bottom row moves z' / (30 S) of a cell a frame (0.25 in the title view): keep that, so 9:16
  raises the camera height h rather than shrinking S.
- 9:16 and 1:1, rendered at every beat. Change the canvas, `W`, `H`, then:
```
9:16  camA: HY 1040, F 880, h 1.8, sunR lerp(300, 340, …), sunLift 170
      camB: HY 1200, F 720, h 1.8, sunR 330, sunLift lerp(150, -360, set), pw 1.5;   STARS y × 1000 (was 700)
      drawPalms: hh = p.s * P.h * sc_ (palms scale with the camera height, or they shrink to stubs under the ridges)
      buildTitle: two lines (code below; set a three-word title as two lines, e.g. THE LAST / ARCADE: a third line
        reaches y 838, covers the sun's top and meets the tag band)
      drawTitle cx = W / 2 - 10; titleState y lerp(575, 480, r), scale lerp(1, 0.7, r)
      impact band in render(): gradient and fillRect centred on y 575 (575 - 90 to 575 + 90; was 430 and 340)
      pulseB's 690 (twice) and the pre-wipe laser's 690 -> camB(t).HY
      buildScript fs 110; drawScript cx 550, cy 860; drawPresents y 330 and 384, tracking lerp(10, 16, k), lerp(10, 14, k)
      drawTag y 720, `700 32px` with 8 px tracking (both places), underline 640 * lz
      BL1 270 x 480, BL2 135 x 240, NOISE frames 270 x 480 (in mk(), createImageData() and post()'s clearRect/drawImage)
      VIG createRadialGradient(W / 2, H / 2, W * .45, W / 2, H / 2, H * .62)
1:1   camA: HY 600, F 480, h 1, sunR lerp(220, 260, …), sunLift 130;  camB: HY 720, F 360, sunR 270, sunLift lerp(150, -300, set), pw 1.9
      STARS × 600; one-line title, titleState scale lerp(1, 0.64, r) * 0.6, y lerp(400, 270, r); impact band on 400;
      a longer line: multiply that scale by 1541 / the line's width at 238 px, or stack it with the 9:16 buildTitle
      script fs 110 at (560, 540); presents y 96 / 148 with the 9:16 tracking; tag as 9:16 at y 380
      690s -> camB(t).HY; BL1 360 x 360, BL2 180 x 180, NOISE 360 x 360; VIG unchanged
```
```js
function buildTitle(lines = ['NIGHT', 'DRIVE'], gap = 50) {           // 9:16: lines stacked, each centred
  const fs = 238, font = `italic 900 ${fs}px ${FT}`, m0 = mk(10, 10).getContext('2d'); m0.font = font; m0.letterSpacing = '6px';
  const ws = lines.map(l => m0.measureText(l).width), tw = Math.max(...ws), asc = m0.measureText(lines.join('')).actualBoundingBoxAscent;
  const pad = 110, depth = 30, lh = asc + gap, c = mk(Math.ceil(tw + pad * 2 + depth), Math.ceil(asc + lh * (lines.length - 1) + pad * 2 + depth));
  const g = c.getContext('2d'), mc = mk(c.width, c.height), mg = mc.getContext('2d'), at = i => [pad + (tw - ws[i]) / 2, pad + asc + i * lh];
  for (const k of [g, mg]) { k.font = font; k.letterSpacing = '6px'; k.textBaseline = 'alphabetic'; }
  lines.forEach((text, i) => { const [x0, y0] = at(i); g.lineJoin = 'round'; g.strokeStyle = '#0a0118'; g.lineWidth = 16; g.strokeText(text, x0 + depth * .55, y0 + depth); g.strokeText(text, x0, y0);
    for (let k = depth; k >= 1; k--) { g.fillStyle = mix('#ff3fcf', '#1b0436', Math.pow(k / depth, .7)); g.fillText(text, x0 + k * .55, y0 + k); }
    const gr = g.createLinearGradient(0, y0 - asc, 0, y0); [[0, '#16236b'], [.16, '#2f68d6'], [.38, '#98d8ff'], [.485, '#ffffff'], [.5, '#fbf0ff'], [.512, '#16041f'], [.58, '#380c40'], [.74, '#a82a72'], [.9, '#ff94b8'], [1, '#ffe8ef']].forEach(([o, col]) => gr.addColorStop(o, col));
    g.fillStyle = '#ffffff'; g.fillText(text, x0 - 2.5, y0 - 2.5); g.fillStyle = '#ff7ad9'; g.fillText(text, x0 + 2, y0 + 2); g.fillStyle = gr; g.fillText(text, x0, y0);
    mg.fillStyle = '#fff'; mg.fillText(text, x0, y0); }); TITLE = c; TMASK = mc; const L = lines.length - 1, [xa, ya] = at(0), [xb, yb] = at(L);
  TGEO = { w: c.width, h: c.height, x0: pad, y0: pad + asc, asc, glints: [[xa + asc * .2 + 4, ya - asc + 4],
    [xa + ws[0] + asc * .2 - 10, ya - asc + 6], [xb + ws[L] - 12, yb - 4], [xb + ws[L] * .55 + asc * .12, yb - asc * .55]] };
}
```
  - 9:16 lands: title x 118–935, y 351–799 at the drift peak, stroke and extrusion included (outro y 330–635);
    script x 150–960, y 780–940 (glyphs and dark edge; the tilt lifts its right end); title-view sun x 210–870 from
    y 720, under the title (a two-line title hides a sun placed as in 16:9). Title, credit and tag stay inside x 118–935,
    y 288–1440; the grid fills the bottom band. Checked at every beat: sun whole until it sets, grid to the bottom
    edge, ridges, palms against sun and sky, title whole, finish everywhere.
  - Stand-in (9:16, STARLIGHT / EXPRESS (scaled by the rule below), script "Platform Nine", lattice pylons in
    360 × 1400 sprites): cameras, sun, grid and text positions held. Subject-dependent: the title scale (755 / the widest line at 238 px, matching
    NIGHT; HORIZON tested: x 126–922), `pw`, `drawPalms()`'s 700 / 1100 width ratio and 1090 / 1100 base anchor.

## Motion
- Easing: `eOut`, `eIn`, `eInOut` (cubic) via `seg(t, a, b)`; linear only for typing and the scrolls. The slam:
  the title falls from 2.9× to 1× in 0.2 s (`eIn`) with three trailing copies, then a spring squash
  1 − 0.07 e^(−6u) sin 30u, a 16 px shake decaying e^(−9u), a white flash (0.32 s), a magenta band through the logo
  (0.5 s) and a bright pulse down the grid (`pulseB`, 1.0 s: it travels for 0.8 s, then dims the bottom rows slightly
  until slam + 1). Then glints (0.5 s each, rotating 0.6 rad), a diagonal sweep across `TMASK` (0.75 s), and a 3.5 %
  drift up to `T.outro` + 0.2 (action: it stops).
- The ring and shake decay forever: taper both to zero by slam + 1 s, or a hold that starts within about 1.8 s of
  the slam never settles (tested; the demo's and the 6 s plan's holds start later and are unaffected):
```js
const shake = t > T.slam ? Math.exp(-(t - T.slam) * 9) * 16 * (1 - seg(t, T.slam + .6, T.slam + 1)) : 0;   // render()
else s = 1 + 0.07 * Math.exp(-u * 6) * Math.sin(u * 30) * -1 * (1 - seg(u, .6, 1));                        // titleState()
```
- Outro: the title rises and shrinks over 0.85 s; the sun lowers 525 px as the palette mixes to dusk and the stars
  brighten (`camB()`'s `set`, `T.sunset` to a literal 9.25).
- Ambient, never stopping: grid and palms (camera z), star twinkle, sun cuts (a bar every 1.8 s), the script's
  47 rad/s hum, grain. Re-time `T` only and these keep film time.
- Never: cross-dissolves, other cuts than the laser wipe and CRT, camera tilt, an off-centre horizon, wobble.
  `drawPalms()`, `drawTitle()`, `drawScript()` and `spaced()` assign `globalAlpha` (contract.md).

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.5 | CRT power-on: a white line opens to full frame, the flash fades | `post()`, `T.on`, `T.onEnd` |
| 0–2.52 | Drive: accelerating over the grid toward a growing sun, palms whipping past | `camA()`, `drawWorld()` |
| 0.8–2.2 | MIDNIGHT ARCADE PRESENTS flickers on (0.45 s), tracking widens, fades from 1.9 | `drawPresents()`, `T.pres`, `T.presOut` |
| 2.22–2.98 | Laser ignites at the title view's horizon (130 px below the drive's); glitch; twin lasers open the title view | `render()`, `T.wipe`, `T.wipeEnd`, `camB()` |
| 2.8–4.53 | Title falls in, slams on the downbeat (flash, shake, band, grid pulse); two glints 3.42; sweep 3.78 | `titleState()`, `drawTitle()`, `T.slam`, `T.glint`, `T.sweep` |
| 4.55–6.82 | Script writes on (to 5.55); two glints at 6.1 | `drawScript()`, `T.sub`, `T.subEnd`, `T.glint2` |
| 7.0–8.0 | Glitch; script flickers out (0.35 s); title rises to y 285 at 0.64× | `T.outro`, `T.rise` |
| 7.0–9.25 | Sun sets, palette mixes to dusk | `camB()`, `T.sunset` |
| 7.65–9.38 | Laser underline draws; the tag types on (to 8.45); a sweep and two glints 8.35–9.38 | `drawTag()`, `T.tag`, `T.tagEnd`, `T.glint3` |
| 9.18–9.93 | Glitch; CRT power-off to a line and a dot; black | `T.off`, `T.offEnd` |

- Grammar: power on into motion; credit over the drive; laser wipe; slam; ornament (glints, sweep, script); outro
  change (sunset, title up, tag); power off. A hold ends where the closing glitch starts (`T.off` − 0.12).
- The demo never settles: the last glint runs to 9.38, past the power-off. Tested 10 s fix (peak 0.795): `T.tag`
  7.7, `T.tagEnd` 8.25, `T.glint3` 7.6, the sunset's 9.25 → 8.3; settled from 8.30, glitch from 9.18: 0.88 s held
  (16:9, 9:16, 1:1). Start the tag 0.55 s or more after `T.rise`, or its first letters and band land on the rising logo.
- Review keys: KEYS=1.5,3.05,3.9,5.6,8.7 (credit over the drive, slam, title and glint, script, end card; 8.7 is a
  hold only after the 10 s re-timing); in a new film the slam, the title held and a frame inside the final hold.

## Sound
audio.py synthesizes 48 kHz stereo (`DUR` 10.0) from `events.json` cues `{t, k}`, through a tanh limiter with a
0.05 s fade-in and a 0.35 s fade-out; it prints the peak.
- Music at fixed times, not cues: 100 bpm (`BEAT` 0.6), bars at `bar()` = `M0` + 2.4 k with `M0` 0.6: a dark Am pad
  pre-roll and quiet bass in bar 0, then from bar 1 (3.0 s, the slam) F, C, G pads (`pad()`, detuned saws), rolling
  16th bass (`bassnote()`), kick on every beat, gated snare on 2 and 4, hats (`for b in range(4, 16)`), and from bar 2
  a plucked arpeggio with an eighth-note echo (0.3 s, `pluck()`). Bass stops at `tb > 9.35`, drums and plucks at 9.3
  (the power-off). The fifth chord (Am tail at bar 4, 10.2 s) never sounds in 10 s.
- Cues: `crton`, `zap`, `charge` (the 0.3 s laser ignition), `laser` (wipe), `fall`, `slam` (sub drop, crash, snare
  and a chord), `glint`, `sweep` (shimmer), `neon` (1.1 s buzz with flicker, for the write-on), `flickoff`, `whoosh`
  (`d`, length), `laser2` (underline), `tick` (one per typed character but spaces), `pass` (a palm crossing the
  camera: `pan` ±0.7, `v` 1 in the drive, 0.5 in the title view, computed in `window.events` from the cameras), `crtoff`.
- No cue is looked up by name; unknown kinds and cues past `DUR` are dropped silently (glints left at 99 cost
  nothing). The drop is timed only by `M0`: keep slam = `M0` + 4 · `BEAT` (negative `M0` is fine, tested). Re-time
  `DUR`, `M0` and the 9.35 and 9.3 cut-offs to `T.off` (+0.05 for bass); more bars for a longer film (Adapting).
- Breaks (tested): `pass` without `pan` or `whoosh` without `d` raise KeyError; `d` ≤ 0 raises ValueError; a `pan`
  past ±1 makes audio.py print "nan" and leaves that whole channel exactly silent for the cue's 0.35 s, music too:
  keep |pan| ≤ 1 (clamp it in `window.events`); `python3 <skill>/scripts/check_audio.py audio.wav 10` fails on that gap.
  Any `DUR` works (`N` is truncated; 7.33333 tested). `v` is a plain gain.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Helpers | `anim.html` → `seg` | `seg(t, a, b)` 0–1 ramp, `eOut`, `eIn`, `eInOut`, `lerp`, `mix(a, b, u)` hex blend, `rng(seed)`, `mk(w, h)` | as is |
| Timeline | `T` | every beat; the sunset end is a literal in `camB()` | adapt |
| Cameras | `camA()`, `camB()` | `{ HY, F, h, z, x, sunR, sunLift, mtn, dusk, pw }` per t | adapt per format (Composition) |
| World | `drawWorld()` | `drawWorld(P, t, pulse)`: `drawSky()`, `drawSun()`, `drawMountains()`, `drawGround()`, `drawPalms()` | as is |
| Frame | `render()` | shake, wipe, lasers, impact, flash, then `post()`; add `ctx.clearRect(0, 0, W, H)` as its first line | adapt: clear first |
| Roadside props | `buildPalms()`, `PALMS`, `drawPalms()` | three sprites in `PALM`; `PALMS` z, x, s, f (flip), v (variant) | as is, or new sprites with new ratios |
| Chrome title, glint | `buildTitle()`, `titleState()`, `drawTitle()`, `glint()` | text inside `buildTitle()`; `glint(x, y, s, a)` at `TGEO.glints` | adapt copy; two lines for 9:16 |
| Neon script | `buildScript()`, `drawScript()` | text and fs inside `buildScript()`; position in `drawScript()` | adapt copy, position |
| Credit, tag | `drawPresents()`, `drawTag()`, `spaced()`, `flick()` | `spaced(txt, x, y, font, sp, fill, glow, a, n)`, n characters shown; `flick(t, t0, dur, seed)` | adapt copy |
| Finish | `buildPost()`, `post()` | `SCAN`, `VIG`, `NOISE`, `BL1`, `BL2`, glitch windows, CRT | as is; sizes per format |
| Score and SFX | `audio.py` → `pad` | cue kinds in Sound | as is; re-time `M0`, cut-offs |
| Demo copy and plot | `drawPresents()`, `drawTag()`, `window.events` | | replace |

## Adapting
- **Style vs demo plot:** style is the world, chrome slam with glints and sweep, neon script, tracked Orbitron, laser
  wipe, CRT on and off, the post chain and the score. Plot: the copy, the drive-then-title order, the sunset outro.
  Transformations: drive to title view, the slam, sunset to dusk, a script appearing.
- **New subject:** replace the copy and, for a thing, put its silhouette among or instead of the palms. Traps: a
  long title outgrowing the frame or hiding the sun; the palm sprite ratios in `drawPalms()`; new sky, old cut colours.
- **Length:** past 10 s hold the title view longer or add beats (another glint pair, a second script line). The
  palm road ahead empties after about 10.7 s of `camA()` or 25 s of `camB()` (`PALMS`, 70 palms to z 160.9): add
  palms. `camB()`'s braking stops the camera 3.8 s after `T.outro` and then reverses it; for a longer hold floor
  its speed (tested: 0.25 a second from 3.5 s after `T.outro`; clamping v alone jumps back to full speed):
```js
const vv = Math.min(v, 3.5), z = 60 + 3.4 * u - 0.45 * vv * vv - 0.9 * vv * (v - vv);   // camB(), replaces z
```
  In audio.py set NB = ceil((`T.off` − `M0`) / 2.4) bars and loop the chords: pads and bass over range(NB) with
  CH[k % 4] and ROOT[k % 4], drums range(4, 4 * NB), plucks range(2, NB) also with CH[k % 4], the Am tail at bar(NB),
  cut-offs to `T.off` (15 s with NB 6, peak 0.795; 16 s with NB 7, 0.798). Set anim.html's `DUR` too (the palm cues
  loop to it). The floored end hold barely moves: spend extra length in the title view before `T.outro`, not on a
  long end card.
- **Shorter:** to 6 s keep every beat and shorten holds: credit 0.9 s, script write 0.65 s, no third glint pair
  (`T.glint3` 99), a faster sunset; the power-off can shrink to 0.4 s. Under 6 s drop whole beats, the credit first,
  then the script, then the outro, ending on the title view; a dropped beat keeps its code with its `T` keys at 99
  (cues fall past `DUR`), and without the outro the drift needs its own end. The signature reads at `T.onEnd` (0.4 s
  tested; the power-on is the fade-in); the title card costs 0.2 s of fall, then 1.15 s from the slam to settled
  (glints at slam + 0.25, sweep at + 0.4; with the taper in Motion, without it never), then 0.8 s. Both plans set
  `T`, anim.html's `DUR` (the palm cues loop to it), audio.py's `DUR`, `M0` and cut-offs:
```
6 s, 16:9 (peak 0.792): onEnd 0.4, pres 0.45, presOut 1.35, wipe 1.45, wipeEnd 1.83, slam 1.85, glint 2.08, sweep 2.2,
  sub 2.35, subEnd 3.0, glint2 3.15, outro 3.55, rise 3.55, sunset 3.55 (camB end 4.45), tag 4.1, tagEnd 4.42, glint3 99,
  off 5.4, offEnd 5.8; audio M0 -0.55, cut-offs 5.45 / 5.4. Settled from 4.467, glitch 5.28: 0.81 s held; black at 5.95.
4 s, 9:16 values (peak 0.795): onEnd 0.4, wipe 0.9, wipeEnd 1.28, slam 1.3, glint 1.55, sweep 1.7, off 3.4, offEnd 3.8;
  pres 99, presOut 99.5, sub 99, subEnd 99.5, glint2, outro, rise, sunset and tag 99, tagEnd 99.5, glint3 99, sunset end 100;
  drift end T.outro + .2 -> T.slam + 1.15; shake and ring tapered (Motion); audio M0 -1.1, cut-offs 3.45 / 3.4.
  Settled from 2.467, glitch 3.28: 0.81 s held. The wipe and slam are the change.
```
- **Other formats:** see Composition and camera.

## Boundaries
- **Distinct from:** `neon-sign` (real glass tubes on wet brick with reflections, no grid, sun or chrome);
  `anime-80s` (painted cel sunset, ink-lined characters on 12 fps, film flare and grain, no CRT); `vaporwave`
  (pastel, a marble bust, checkerboard floor, 95 windows, JPEG crunch); `vector-arcade` (phosphor line art on
  black, no fills); `glitch` (corruption as the subject; here glitches are 0.2 s cuts).
- **Poor fit:** several facts or long text (`kinetic-typography`), charts (`data-visualization`), interface demos
  (`product-ui`), tender or calm stories (`picture-book`), HUD diagnostics (`sci-fi-interface`).
- **Do not:** copy real logos or title lettering (80s films, TV shows, album covers, game brands); drop the CRT
  finish or the glow; go pastel or add marble and checkerboards (`vaporwave`); move the vanishing point off centre.

## Technical notes
- No render.json, vendor folder or WebGL: canvas 2D; three woff2 fonts in fonts.css. About 0.12 s a frame on one
  page; `post()`'s per-pixel RGB split is most of it. Frames draw into `sc` (`willReadFrequently`), then onto `#c`.
- `render()` never clears `sc`, and the shake translates the world, so during the slam (to slam + 0.6 s, up to 158
  levels) the uncovered edge strip keeps the previous frame: a state leak. With `ctx.clearRect(0, 0, W, H)` first
  (contract.md: repaint every pixel) every frame is byte-identical (tested in 16:9, 9:16, 1:1 and the 4 s plan).
- Seeded: `rng()` 1984 (stars), 7 and 21 (ridges), 77 (palms), 300 + v (palm shapes), 900 + k (noise), and 11, 55,
  1, 3, 9, 13 plus the frame number (flicker, glitches); audio `default_rng(1986)`. audio.py ignores `window.MUSIC`.
- Sizes outside `W`/`H`: every literal is in the 9:16 block; `grep` for 1920 or 1080 finds only the canvas and `W`/`H`.
