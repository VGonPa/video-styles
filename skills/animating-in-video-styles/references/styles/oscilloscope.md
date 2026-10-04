# Oscilloscope (`oscilloscope`)

An analog X–Y vector monitor seen head-on: one green phosphor beam draws waveforms, Lissajous knots, a wireframe and
beam-lettered words inside an amber graticule, with persistence and bloom, and the soundtrack is the beam's own
deflection signal (left = X, right = Y). It draws on lab oscilloscopes and oscilloscope music. Precise, quiet and
hypnotic: an instrument worked by an unseen hand.

**Reference film:** the invented "Halvard Model 12" powers on, a dot crawls into a cosine that spins up, a 3:4 then 2:3
Lissajous, a rotating cube, the word SIGNAL, a collapse to a parked dot, power-off · `styles/oscilloscope/`

## Signature
- The instrument from frame 0, locked off: a rounded CRT screen in a dark moulded bezel (left two-thirds) beside a
  brushed-metal strip with an invented maker's nameplate (HALVARD in the demo), POWER and MODE lamps, a green readout
  and knurled FREQ and INTENSITY knobs (`buildStatic()`, `panel()`); X/Y GAIN knobs, model line and AUDIO OUT jacks
  are dressing.
- Dark green-grey glass under an amber 10 × 8 graticule with ticked centre axes and 100 / 0% rise-time rows, faint at
  first and brightening with the power from 0.13 s (`GRAT`).
- One green beam, white-hot where it dwells, with halo and bloom (`phosphor()`): a defocused dot appears at the left
  edge at 0.22 s, crawls right drawing the opening waveform in one slow pass (in the demo, a three-cycle cosine; any
  y = f(x)), then spins up until the trace stands still at 2.15 s.
- Persistence: a long fading tail on the slow crawl, a crisp standing trace at audio rate (`decayAt`). The readout
  follows the signal (CH1 X 0.60 Hz climbing to 55.0 Hz), and the hum rising out of silence is the trace itself.

## Palette
| Role | Colour | In code |
|---|---|---|
| Glass, centre → edge; sheen | `#0e1714` → `#060a09`; `rgba(200,230,220,0.06)` | `BG`, `GLARE` |
| Trace, red; green; blue | `255 * (c * 0.30 + hot * 0.62 + glow * 0.16)`; `255 * (g + hot * 0.1)`; `255 * (c * 0.52 + hot * 0.45 + glow * 0.30)` | `compose()` |
| Graticule lines and labels (drawn at alpha 0.12 → 0.5) | `rgba(255,186,120,1)` | `GRAT`, `render()` |
| Panel, top → bottom; bezel ring; its edge | `#2a2f31` → `#1b1f21`; `#0d0f10`; `#3a3f42` → `#15181a` → `#2b3033` | `FRONT` |
| Nameplate, jack labels; control labels; model line; tagline | `#e4ded0`; `#c9c4b6`; `#a9a69c`; `#8f8c83` | `buildStatic()` |
| Rules; readout window, rim, top band | `rgba(228,222,208,0.25)`; `#050807`, `#3c4245`, `rgba(160,255,190,0.04)` | `buildStatic()` |
| Readout label; value; glow | `#5fdc8c`; `#b8ffd0`; `rgba(110,255,160,0.9)` | `panel()` |
| Power lamp; mode lamps | `255, 120, 60`; `110, 255, 150` | `panel()`, `lamp()` |
| Knob body; cap; pointer | `#4a4f52` → `#141718`; `#c9cdcf` → `#6d7376` → `#3a3f42`; `#f2ede0` | `knob()` |

- The trace has no stroke colour: `compose()` maps beam energy e to a green core (1 − e^(−1.1e)), a white-hot centre
  above e = 1.6 and a greener halo and bloom, added to the glass, so crossings and slow spots go white. Outside the
  screen only dull metal and bone legends; the sole saturated colours are the two greens and the orange power lamp.

## Typography and copy
- `FONT` is Barlow Condensed 600 (`fonts/BarlowCondensed-600-latin.woff2`), `MONO` is IBM Plex Mono 500
  (`fonts/IBMPlexMono-500-latin.woff2`), in `fonts.css`. Barlow sets every panel legend in capitals, tracked per
  letter by `spaced()`; Plex Mono the readout.
- Sizes in px (tracking): nameplate 50 (9); model line 22 (3); control and knob labels 22 (2.5; Y–T and X–Y 1.5);
  tagline 20 (1.6); jack labels 26 (2); graticule labels 20. Readout 30 with a 12 px glow, label at `P0` + 24, value
  right-aligned at `P0` + 416, rows 58 px apart; values count with the signal, labels swap at beat boundaries, never
  typed; it flickers 4% (`vfd`). Legends are in `FRONT`.
- Copy is instrument nomenclature: channel names, values with units in their own case (Hz, V), ratios, states (VECTOR,
  PARKED), otherwise capitals. Measured with `measureText`: readout 18 px a character, so 21 characters a row with a
  space (PATH + "CUBE  110 Hz" is 16); nameplate about 13 capitals (HALVARD 214 px of 440); model line about 38
  characters (349 px for 31); tagline about 30 after AUDIO OUT (270 px for 28).
- The screen never shows a font. The beam writes words from `GLYPHS`: strokes in cap units (y down, x from 0 to the
  letter's `w`), polylines and `arc()` runs, scaled in `WORD` to h = 0.47 signal units (211 px) with gaps of 0.34 h.
  Only S, I, G, N, A and L exist (adding letters: Adapting). Width = h × (sum of `w` + 0.34 × (letters − 1)): SIGNAL
  is 2.27 units (1024 px) of the graticule's 2.67; keep words under about 2.4 and lower h for longer ones (about 0.32
  for eight letters). One word per beat: two lines double the path and halve its brightness.
- Glyphs in both faces: Latin-1 (µ, °, ±, ×, ·), – and …; no →, Ω, ≈, Δ, π or Ł, ő, š: write TO, OHM, APPROX.

## Texture and finish
- Phosphor: `phosphor(t)` clears `E` and integrates the precomputed signal over the last min(t, 4.5 × `decayAt`) s.
  Each sample deposits its time step × e^(−age / decay) × `beamAt` × exposure (`GAIN` 350000 × `expoAt`, +45% while
  the Lissajous is up) in bilinear splats every 0.8 px along the segment from the previous sample.
- Persistence is 0.42 s on the crawl, 0.034 s from 2.0 s; exposure rises from 0.012 to 1 over 1.15–2.05 s, so the
  slow, hot crawl does not burn. Both ramps are literal times.
- Spot and glow: a [1, 2, 1] blur; samples spread over a `spreadAt` disc while warming up (7 px, gone by 0.67 s) and
  on the parked dot (3.2 px). A soft-clipped copy, e / (1 + 0.015e), is box-blurred at 1/4 size into `HALO` and 1/16
  into `BLOOM`; `compose()` adds 0.55 halo + 0.5 bloom.
- Layers: `BG` under the phosphor (a radial gradient with ±2.5-level grain from `rng(12)`, painted once); then, in
  `render()`, `GRAT` (1.6 px lines, 0.2-division axis ticks, over the trace), `GLARE` (an elliptical sheen top-left, a
  50 px inner rim shadow in the 40 px rounded corners), `FRONT` (brushed metal from `rng(7)`, vignette, bezel, screws,
  legends). No scanlines, shadow mask or barrel distortion: a vector tube, read through bezel and sheen.

## Shapes, line and figures
- Inside the glass there is one point moving at 48 kHz. `buildSignal()` writes x, y in signal units into `SXa`, `SYa`
  (x right, y up; screen x = `CX` + x × `U`, y = `CY` − y × `U`, `U` 450 px); no canvas strokes.
- Beam modes: Y–T, a triangle time base sweeping x across ±1.2 and back with y a function of x, so both passes retrace
  one curve and there is no flyback line (a new waveform must also be y = f(x)); Lissajous, x and y = 0.84 × sin of
  two phase accumulators; vector paths, `makePath()` tables walked `FR` = 110 times a second by `pathAt()`; 3D,
  projected per sample (the cube: rotation, perspective 3.6 / (d + 3.6), scale 0.4).
- A new figure is one continuous loop per refresh, or a palindrome (strokes forward, then back, as `WORD`): there is
  no blanking, every move leaves light. Jumps get a tiny weight (`WORD`: 0.001 + 0.02 × length) and leave faint lines,
  as on a real vector scope. Weights are time: equal weight per unit length gives even brightness, an edge traced
  twice gets about half each (`CUBE_W` walks the four verticals twice at 0.55). Change frequency through accumulators
  (phase += f / `SR` per sample), never sin(2π f(t) t).
- Brightness is exposure ÷ beam speed: energy per sample is fixed, so a slow beam burns and a fast jump stays faint.
  At full exposure the demo's figures travel 360000–850000 px/s at `U` 450 (cube about 4900 px a refresh, SIGNAL 7760
  with every stroke twice). A heart of 1900 px glowed 2.6× brighter and still read; far outside that range, scale the
  exposure in `phosphor()` for that beat, as the Lissajous +45% does.
- Resolution: samples are joined by chords of path px × `FR` / 48000 (11 px on the cube, 18 on the word); keep them
  under about 20 px (SIGNAL allows about 120 Hz; at 440 Hz it broke into 71 px chords, at 40 Hz it rendered clean).
  Line: a 3 px core with halo and bloom; no fills, no second colour, no outlines.
- People: a one-line frontal pictogram (head, neck, shoulders, arms and hands, legs; one `makePath()` loop 1.3 units
  tall) reads as a person (tested in 16:9 and 9:16); characters that act or turn in profile are untested. It is a
  sign, not a character: it has no profile or joints, which review.md asks of people. Use it for one beat at most, and
  tell stories with waveforms, orbits, objects and words.

## Composition and camera
- One locked-off frontal view for the whole film: no camera moves, cuts or zooms; the action is on the screen.
- `SW` and `SH` stay multiples of 16 (`HALO` and `BLOOM` are 1/4 and 1/16 of them); coordinates for every format are
  in the table under Other formats.
- Figures centre on the graticule, sized in signal units: sweep ±1.2 (half a division inside the edge), Lissajous
  ±0.84, cube about ±0.7, word ±1.14 by ±0.24. One figure at a time.

## Motion
- Easing: `sm` (smoothstep) for lamps, ramps and the first two morphs; `eInOut` for the word morph, the glide and the
  power-off knob; `eOut` for INTENSITY coming up; `eBack` (1.3) for the FREQ knob and cycle count (overshoot past 5).
  Panel causes: FREQ turns for the cycle beat, X–Y switch and glide; MODE lamps swap at `T.xy0` + 0.05.
- Morphs blend two signals point by point over 0.5–0.6 s; between unrelated figures they read as a scribble for about
  half a second, an accepted compromise. SIGNAL lands with a damped wobble from `T.word1`: scale 1 + 0.045 ×
  e^(−Δt/0.18) × sin(2π × 3.2Δt). The collapse: a 6% swell over 0.11 s (`eOut`), then a shrink to the centre (`eIn`)
  by `T.dot` (`sizeAt`).
- Ambient through holds: the readout flicker, the dot's shimmer and a vector figure's refresh phase (at `FR` 110 the
  brightest stretch steps around the path with a period of three frames, up to 64 levels between neighbouring frames
  and identical every third). Measure holds against an end-state frame drawn at the same t, not against the previous
  frame. Never cuts, shake, glitches, trace flicker, motion blur or frame stepping; fast beam motion shows as trails
  and meshes of light.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.2 | instrument already visible; POWER lamp, readout and Y–T lamp on (0.08–0.2); INTENSITY up (0.02–0.52); graticule light (0.13–0.43) | `T.lamp`, `panel()`, `render()` |
| 0.22–0.67 | beam fades in as a defocused dot at the left edge and focuses | `T.beam`, `beamAt`, `spreadAt` |
| 0.42–1.05 | time base crawls at 0.6 Hz; the dot draws one cosine with a long tail; amplitude ramps up | `T.sweep`, `fxAt`, `ampYAt` |
| 1.05–2.15 | spin-up to 55 Hz; persistence shortens (1.2–2.0), exposure rises (1.15–2.05); the trace stands still | `T.spin0`, `T.spin1`, `decayAt`, `expoAt` |
| 2.62–3.3 | FREQ knob: 3 → 5 cycles with overshoot; RATIO 1 : 6.0 → 1 : 10 | `T.knob0`, `T.knob1`, `cycAt` |
| 3.55–4.15 | MODE to X–Y; the trace melts into a rotating 3:4 Lissajous (165 : 220 Hz, X detuned 0.24 Hz) | `T.xy0`, `T.xy1`, `liss` |
| 4.7–5.05 | glide to 2:3 (220 : 330 Hz); FREQ knob turns; the readout shows the passing ratio | `T.glide0`, `T.glide1` |
| 5.45–7.0 | morph (to 6.0) into a wireframe cube on a 110 Hz path, which turns and nods | `T.cube0`, `T.cube1`, `CUBE_W` |
| 7.0–8.45 | morph (to 7.5) into SIGNAL, PATH CUBE → TEXT at 7.25; it lands with a wobble and holds | `T.word0`, `T.word1`, `WORD` |
| 8.45–8.8 | swell and collapse to the centre; BEAM PARKED from 8.68 | `T.swell`, `T.dot`, `sizeAt` |
| 8.7–9.55 | dot blooms to 3.2 px (to 9.05); parked dot held | `spreadAt` |
| 9.55–10 | power-off: INTENSITY down (9.55–9.95), beam out (9.65–9.96), graticule light and lamps out (by 9.98), frame darkens 60% (9.88–10) | `T.off0`, `T.off1`, `render()` |

- One shot; a beat opens on a panel event, morphs 0.35–0.6 s, holds 0.4–1.5 s. Reusable: crawl and spin-up (opening),
  knob beat, X–Y switch, beam word (title card), collapse and power-off (sign-off). One-off: ratios, cube, SIGNAL.
- KEYS for contact_sheet.sh: 0.5 (dot and tail), 1.5 (the crawl's fading pass beside the faster one), 3.3 (five
  cycles), 4.4 (3:4 knot), 5.3 (2:3), 6.5 (cube), 8.2 (SIGNAL landed), 9.3 (parked dot), 9.85 (power-off).
- Settled means every pixel within 2 levels of the same frame drawn with every action at its end state and no
  power-off (ranges give first and last settled frames). The parked dot becomes identical; a word's wobble never does.
- The demo's ending is too short to copy: the parked dot is settled only 9.067–9.533 s (15 frames, 0.5 s). It settles
  at `T.dot` + 0.27 (the bloom) and the INTENSITY knob moves from `T.off0` − 0.05, so keep `T.dot` ≤ `T.off0` − 1.1
  (at equality the dot holds 24 frames, exactly 0.8 s; the tested plans use 1.2 for 27). Tested 10 s timing (16:9 and
  9:16): `T.word0` 6.8, `T.word1` 7.3, `T.swell` 8.05, `T.dot` 8.4, the rest as the demo; settled 8.667–9.533 s (27
  frames, 0.9 s).
- The power-off is the closing fade (beam out in 0.31 s). The last frame is the unlit instrument at about half the
  hold's brightness (the 60% darkening ends at `DUR`, never drawn): acceptable, as beam and lamps are already out.

## Sound
- No cues: `render.json` sets `signal` to `xy.f32`, so events.mjs saves `window.signal()` (float32 x, y pairs from
  `SXa`, `SYa`) and audio.py plays it, left = X, right = Y, as long as the signal (`NS` samples in anim.html).
- audio.py only conditions it (`dc_block()` 18 Hz, two `onepole_lp()` 3 kHz, 0.03 s and 0.08 s fades, peak −8.5 dBFS).
  No music or fixed times: re-timing `T` re-times the sound, so no note is left over or doubled. check_audio.py's note
  that nothing sounds after `T.dot` is expected: the parked beam is silent.
- You hear: near silence to about 1.2 s (the crawl is subsonic), a buzz rising with the spin-up, the pitch climbing
  330 → 550 Hz with the FREQ knob, a fourth (165 + 220 Hz) gliding to a fifth, the 110 Hz buzz of every vector path.
- What breaks it, both tested: a `DUR` such as 4.1, 8.2 or 9.2 makes `SR` × `DUR` fall just under a whole number, so
  `window.signal()` writes an odd number of floats and audio.py stops at its reshape; write `NS` as
  Math.round(SR * DUR). One NaN sample (`T.knob0` = `T.knob1` = 2.0 divides 0 by 0 in `seg()` at 2.0 s) silences its
  channel from there on, the filters being recursive: audio.py prints a nan peak and check_audio.py fails the track (R
  silent from 2.00 s, L sounding to 8.80 s). Never give a ramp zero length; park unused keys at 98 and 99.
- A film ending on a held figure keeps its drone through the power-off (INTENSITY dims the picture, not the signal):
  set audio.py's fade-out, the 0.08 next to `n / SR - t`, to `T.off1` − `T.off0` − 0.05 (0.3 in the 4 s plan), so the
  drone fades with the beam, or end on the silent parked dot. Mixed-in voice or music breaks the conceit.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Deflection signal | `anim.html` → `buildSignal` | once in `window.ready`; per sample: accumulators, blends `m1`, `m2`, `m3` (gates `m1 > 0 && m2 < 1` etc.), `sizeAt`; writes `SXa`, `SYa` | adapt: your figures |
| Timeline | `anim.html` → `T` | keys in seconds, read by `fxAt`, `cycAt`, `ampYAt`, `liss`, `sizeAt`; `decayAt` (1.2–2.0) and `expoAt` (1.15–2.05) are literals tied to the spin-up | replace |
| Vector path | `anim.html` → `makePath` | `makePath(pts, wts)`: points in signal units, one time weight per segment; `pathAt(P, f, out)` writes the point at phase f in [0, 1) | as is |
| Cube | `CUBE_V`, `CUBE_W`, `CUBE_CUM`, the `m2` block | rotation `ry`, `rx` from t; perspective 3.6, scale 0.4 | replace: your figure slot |
| Beam lettering | `anim.html` → `GLYPHS` | `arc(cx, cy, rx, ry, a0, a1, n)` in cap units and degrees; `WORD`: h 0.47, gap 0.34, `txt` | adapt: add letters, set `txt` and h |
| Phosphor | `anim.html` → `phosphor` | `phosphor(t)`, `compose()`, `boxBlur()`, `down()`; `GAIN`, `expoAt`, `decayAt`, `beamAt`, `spreadAt` | as is; per-beat exposure for odd path lengths |
| Glass, graticule, bezel, legends | `anim.html` → `buildStatic` | `BG`, `GRAT`, `GLARE`, `FRONT`; `rr()`, `spaced(c, s, x, y, sp, center)`, `screw()`, `jack()` | as is; move for other formats |
| Controls | `anim.html` → `panel` | `KNOBS`, `knob(k, ang)` (radians from 12 o'clock), `lamp(x, y, on, col)`, `fmtHz()`; readout lines picked by t against `T.xy0`, the cube morph's middle, the word morph's middle (the PATH label) and `T.dot` | adapt: strings and angles per beat |
| Soundtrack | `audio.py` → `dc_block` | `dc_block(x, fc)`, `onepole_lp(x, fc)`, fades, normalisation | as is; longer fade-out for held endings |

## Adapting
- **Style vs demo plot:** the style is the Signature plus a panel cause for every change, the collapse to a parked dot
  and the power-off. Plot: HALVARD, cycle counts, ratios, the cube, SIGNAL. The transformation can be a morph between
  figures, the Y–T to X–Y switch, a frequency glide, a word assembling, or the collapse.
- **New subject:** translate it into figures the beam draws: a waveform in Y–T (a heartbeat, an envelope), an orbit or
  ratio as a Lissajous, an outline, wireframe or pictogram as a vector path, the message as beam lettering. Put your
  figure in the cube's slot and your word in the word's, so `panel()` and the exposure stay keyed, with readout
  strings for each. Keep the maker invented. Stand-in tested in 16:9 and 9:16 (a beating heart, taller than wide, and
  PULSE): figure size, the word's h and the exposure depend on the subject; `U` and the screen do not.

```js
// m2 block: replace the cube's lines from `const ry` to `const cxv` (keep the lerp after them); f = 110 Hz path phase
// and in panel() print 'HEART ' + FR + ' Hz' instead of 'CUBE  ' + FR + ' Hz'
const th = TAU * f, beat = 1 + 0.07 * Math.exp(-((t - T.cube0) % 0.8) / 0.12), ry = 0.5 * Math.sin(1.3 * (t - T.cube0));
const hx = Math.pow(Math.sin(th), 3), hy = (13 * Math.cos(th) - 5 * Math.cos(2 * th) - 2 * Math.cos(3 * th) - Math.cos(4 * th)) / 16;
const cxv = 0.6 * beat * hx * Math.cos(ry), cyv = 0.75 * beat * (hy + 0.15);
// GLYPHS additions (cap units, y down); then txt = 'PULSE'
P: { w: 0.52, s: [[[0, 1], [0, 0], ...arc(0.24, 0.26, 0.28, 0.26, -90, 90), [0, 0.52]]] },
U: { w: 0.56, s: [[[0, 0], ...arc(0.28, 0.72, 0.28, 0.28, 180, 0), [0.56, 0]]] },
E: { w: 0.5, s: [[[0.5, 0], [0, 0], [0, 1], [0.5, 1]], [[0, 0.5], [0.4, 0.5]]] },
```
- **Length:** past 10 s add figure beats of 1–2.5 s, a new figure each time; a long static knot goes dead. A further
  slot copies the word block's pattern: its own blend weight from two new `T` keys, the previous block gated by that
  weight < 1. Re-time `DUR` in anim.html and write `NS` as Math.round(SR * DUR) (sound follows; tested at 30 s), then
  `T`, the ramps in `decayAt` and `expoAt`, `panel()`'s readout branches, build.sh's `DUR`.
- **Shorter:** down to about 6.5 s keep every scene and shorten holds (`T.lamp` stays 0.08); the tested 6 s plan below
  already drops the knob and the glide. Tested minimums: crawl 0.24 s, spin-up 0.6, knob 0.45, X–Y morph 0.35,
  Lissajous hold 0.3, glide 0.3, cube 0.4 + 0.4 hold, word 0.35 + 0.55 to read, collapse 0.35, dot 0.27 + 0.8,
  power-off 0.35. Put the decay ramp at `T.spin0` + 0.15 → `T.spin1` − 0.15 and exposure at `T.spin0` + 0.1 →
  `T.spin1` − 0.1 (the literals in `decayAt` and `expoAt`), as the demo does. An 8 s cut keeps every scene at these
  minimums.
  - Tested 6 s (16:9 and 9:16), knob and glide dropped: `DUR` 6.0; `T` beam 0.2, sweep 0.38, spin0 0.75, spin1 1.45,
    xy0 1.55, xy1 1.95, cube0 2.3, cube1 2.7, word0 3.1, word1 3.5, swell 4.05, dot 4.4, off0 5.6, off1 6.0, knob0 and
    glide0 98, knob1 and glide1 99; decay 0.9–1.3, exposure 0.85–1.35. Dot settled 4.667–5.533 s (27 frames, 0.9 s).
  - Under 6 s cut whole beats: first the glide, then the FREQ knob, then the cube slot (or the word, whichever does
    not carry the message), then the collapse (end on the held word, the power-off as fade). Do not end on the figure
    slot: the cube's `ry` and `rx`, and the stand-in heart's beat, follow t and never settle. To end on a figure, stop
    its motion first, by easing its angles to fixed values before the last 0.8 s, and measure the hold. No fade-in;
    the opening (dot, tail, standing trace) needs 1.2 s. Dropping the cube: re-key `(T.cube0 + T.cube1) / 2` in
    `panel()` and `(1 - sm(seg(t, T.cube0, T.cube1)))` in `phosphor()` to `T.word0` and `T.word1`; otherwise the
    readout keeps the Lissajous lines and the word its +45% exposure. Dropping the collapse: `T.swell` 98, `T.dot` 99.
    A word as the final card costs its morph, the wobble's settle (1.4 s after `T.word1` at the demo's 0.18 time
    constant, 0.5 s at 0.07), 0.8 s held, and the power-off. Keep the X–Y switch before the first vector figure even
    when the Lissajous has no story role (tested minimums: morph 0.35 s, hold 0.3 s). `panel()` shows the Y–T readout
    and lights the Y–T lamp until `T.xy0` + 0.05, so parking `T.xy0` at 98 leaves CH1 X 55.0 Hz and RATIO 1 : 10 under
    every later figure.
  - Tested 4 s (16:9 and 9:16): `DUR` 4.0; `T` beam 0.2, sweep 0.36, spin0 0.6, spin1 1.2, xy0 1.3, xy1 1.65, word0
    1.95, word1 2.3, off0 3.65, off1 4.0, knob0, glide0, cube0 and swell 98, knob1, glide1, cube1 and dot 99; decay
    0.75–1.05, exposure 0.7–1.1; the cube re-keyed as above; the 0.18 in `buildSignal()` set to 0.07; audio.py
    fade-out 0.3. SIGNAL settled 2.8–3.6 s (25 frames, 0.83 s), beam out 3.7–3.96 s.
- **Other formats:** everything inside the glass scales with `U`; the strip is literal coordinates. Rendered:

| Value | 16:9 (demo) | 9:16, 1080 × 1920 | 1:1, 1080 × 1080 |
|---|---|---|---|
| `SX`, `SY`, `SW`, `SH` | 96, 44, 1248, 992 | 68, 296, 944, 928 | 60, 96, 960, 704 |
| `CX`, `CY`, `DIV`, `U` | 720, 540, 120, 450 | 540, 760, 112, 330 | 540, 448, 84, 315 |
| Graticule (`buildStatic()`) | 10 × 8 | 8 × 8: every `5 * DIV` → `4 * DIV`; the vertical-line loop's `i <= 10` → 8 (not the knob scale's); both `i <= 50` → 40 | 10 × 8 |
| `P0` (in `buildStatic()` and `panel()`) | 1400 | 68 | 60 |
| Nameplate; model line; rule | y 104; 140; 166, 440 wide | 112; 148; 172, 944 wide | 60; removed; removed |
| Lamps y (x `P0` + 20, 272, 366); labels y | 206; 214 | 232; 240 | 46 at `P0` + 480, 732, 826; 54, labels at `P0` + 508, 640, 754, 848 |
| Readout window, top band; rows | 250, 256; 290 + 58 i | 1262, 1268; 1302 + 58 i | 852, 858; 892 + 58 i |
| `KNOBS` FREQ, INTENSITY (x, y, r, label y) | 1508, 584, 72, 482; 1752, 584, 56, 482 | 700, 1384, 72, 1282; 900, 1384, 56, 1282 | 660, 970, 64, 876; 880, 970, 56, 876 |
| X GAIN, Y GAIN | 1508 and 1752, 790, 34, 722 | 700 and 900, 1700, 34, 1632 | removed with their `knob()` calls |
| AUDIO OUT rule; label; tagline; jacks; jack labels | 862; 906; `P0` + 150, 906; 968; 978 | 1500, 944 wide; 1610; `P0`, 1650; 1740; 1750 | removed |

  - 9:16, rendered at every beat's widest moment and through the power-off (sweep x 143–937, knot y 481–1039, SIGNAL
    at peak wobble x 156–926, y 680–840): Signature whole, readout text to y 1433, words under 2.4 units left of
    x 950; nameplate, lamps, X/Y GAIN and AUDIO OUT in the bands are dressing. Words to read go on the screen.
  - 1:1, rendered at every beat and through the power-off: nameplate and lamps above the screen; readout, FREQ and
    INTENSITY below. It drops the model line, X/Y GAIN and AUDIO OUT, and the look survives without them.

## Boundaries
- **Distinct from:** `vector-arcade` is a multi-colour arcade attract mode on bare black, strokes redrawn at past
  instants with flicker, game graphics; oscilloscope is one green trace of a sampled X–Y signal in an instrument,
  heard as sound. `terminal` types raster text; `sci-fi-interface` is an ice-blue HUD, `3blue1brown` smooth maths,
  `single-line` ink on paper; `retro-desktop`, `teletext`, `synthwave` and `glitch` are raster screens.
- **Poor fit:** real data with axes (`data-visualization`, `infographic`); text-heavy processes (`terminal`);
  equations (`3blue1brown`); long copy (`kinetic-typography`); characters who act (`clay`, `flash-cartoon`).
- **Do not:** copy real instrument makers' names, logos or panels, or pass the film off as a real measurement; give
  the trace a second colour, scanlines or fills; set type on the screen; score it with sound unrelated to the signal.

## Technical notes
- `render.json` is `{ "signal": "xy.f32" }`: no GPU flag, no `schedule`; all code is in anim.html, with no WebGL or
  vendored libraries. 300 frames take about 15 s on one page of an Apple-silicon laptop.
- Frames are a pure function of t although persistence looks back: `buildSignal()` integrates the whole signal once in
  `window.ready` (its accumulators are the only history), and each `phosphor(t)` rebuilds the afterglow from it, never
  from an earlier frame. Static layers use `rng(12)` and `rng(7)`; the spot jitter follows the sample index.
- One leak: `knob()` sets `lineCap`, `lineWidth`, `strokeStyle` and a gradient `fillStyle` outside
  `save()`/`restore()`. The next frame's FREQ knurling inherits the round cap (up to 13 levels); the leftover gradient
  fill makes the readout glow rasterize up to 4 levels differently (contract.md's gradient quirk), so review.md's cmp
  test fails as shipped. Wrap the body of `knob()` in `ctx.save()` … `ctx.restore()` before the baseline run; frames
  are then identical (tested at 0.5, 4.2, 6.5 and 9.3 s).
- Hard-coded outside `W`/`H`: canvas tag, `CX`, `CY`, `P0` (twice), the strip's y literals, `KNOBS`, the graticule's
  ±5 divisions (table above). `window.NOGLARE` is a debug switch.
