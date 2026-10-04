# Generative Particles (`particles`)

A creative-coding study in the tradition of Processing flow-field sketches and shader demos: 40,000 particles drift
through a curl-noise field leaving hairline additive trails on near-black navy, gather into a word, burst into a
galaxy and collapse into one point of light, framed as a lab-notebook entry. Cool, hypnotic and technical.

**Reference film:** a swirling swarm organises into the word EMERGE, bursts into a spiral galaxy, spirals into one
glowing point and fades · `styles/particles/`

## Signature
- A near-black navy frame filled edge to edge with tens of thousands of hairline trails following smooth eddies,
  mostly blue and cyan, with out-of-focus bokeh dots, bloom and a dark vignette, faded up from black over 1 s.
- Colour is speed: slow particles violet and blue, fast ones amber to cream; trails lengthen with speed, so a rush
  toward a target reads as warm streaks and a settled form as a fine violet stipple.
- A small JetBrains Mono lab overlay: study title and spec line top left, phase number and name over a running
  `t = 00.00 s` timer top right, a violet-to-cream velocity bar bottom left, a live `mean |v|` readout bottom right.
- From 1.85 s the swarm streams left to right toward one bold word made only of particles (warm streaks by 2.5 s; the
  word reads from about 3.4 s, whole by 3.9 s); letters overshoot, then settle. Every change of form is particles
  travelling: never a cut, a cross-fade or real type.

## Palette
| Role | Colour | In code |
|---|---|---|
| background, edge → glow just below centre | `vec3(.006,.007,.018)` → `vec3(.030,.026,.068)` | `pComp` (`u_bg`) |
| slowest particles (violet) | `vec3(.46,.30,1.)` | `RAMP`, first stop |
| slow (blue) | `vec3(.18,.46,1.)` | `RAMP` |
| medium (cyan) | `vec3(.10,.86,1.)` | `RAMP` |
| fast (amber) | `vec3(1.,.72,.42)` | `RAMP` |
| fastest (cream) | `vec3(1.,.97,.9)` | `RAMP`, last stop |
| singularity core / inner halo / outer halo | `vec3(1.,.93,.82)`, `vec3(.45,.55,1.)`, `vec3(.5,.3,1.)` | `pComp` (`u_core`) |
| flash halo | `vec3(.55,.62,1.)` | `pComp` (`u_flash`) |
| overlay text, primary / secondary | `rgba(214,224,255,0.82)` / `rgba(160,176,230,0.55)` | `overlay()` |
| velocity legend stops | `#6b33ff`, `#2466ff`, `#1adbff`, `#ffb86b`, `#fff7e6` | `overlay()` |

- All colour is light: particles add (`gl.blendFunc(gl.ONE, gl.ONE)`) into a half-float buffer, dense areas burn
  toward cyan-white, and the tone map `1. - exp(-(c + bg)*1.15)` rolls highlights off. Each vertex takes `ramp(u)` in
  `PVS`, u = (speed / 1400)^0.55; the legend's 2D gradient repeats the ramp's stops: change both together.

## Typography and copy
- Unbounded 700 (`fonts/Unbounded-normal-700-latin.woff2`) is never drawn as text: `textTargets()` fills the word into
  an offscreen mask fitted to 1420 px wide (256 px type for EMERGE, `letterSpacing` 6 px), centred at `TEXT_CY` (−40).
- JetBrains Mono (`fonts/JetBrainsMono-normal-400-latin.woff2`, serving 400–500 in `fonts.css`): 500 at 19 px, 3 px
  tracking, for header and phase label; 400 at 15 px, 1 px tracking, for the rest. The overlay fades in 0.5–1.3 s and
  out 8.9–9.5 s; a phase label fades in over 0.3 s rising 10 px and out over the 0.25 s before the next.
- Voice: a deadpan lab notebook: an invented study title and number, a spec line (count · method · seed), a phase
  number and one noun (CHAOS, FORM…). Copy limits come from 9:16, where the phase label shares the header's row (25 /
  20 px are 18 / 13 px a character): header 30 characters (to x 616), phase label 15 (from x 680), spec line 52 (to
  x 752; the timer starts at x 807).
- The particle word: one word in capitals, fitted to the mask width. Under the wave, 16:9 reads cleanly at 10 letters
  (171 px type) and still at 14 (114 px); 9:16 cleanly at 8 (130 px), thinly at 10 (99 px), not at 14 (66 px). Longer
  copy goes in the overlay. `letterSpacing` stays 6 px as the size shrinks, so
  long words overrun the fit (x 972 in 9:16); 6 × size / 300 px set after the fit kept them inside x 131–944.
- Glyphs: Latin-1, general punctuation, €, ™, ↑ ↓ (`fonts.css`); the mask silently uses a system font for others.

## Texture and finish
- Trails: `K` = 7 one-pixel `gl.LINES` segments per particle through positions `KS` = 2 frames apart (0.47 s),
  fading to the tail; alpha grows with length up to 2.8 px and drops for very fast streaks (`sd`). Always 1 px wide.
- Points: a sprite per particle, depth of field from `coc = clamp(abs(a_p.z)/480., 0., 2.2)`: a 1.9 px Gaussian dot in
  focus, a larger rim-lit disc (bokeh) out of focus, its alpha falling as its area grows.
- Bloom at 480 × 270 and 160 × 90 (`pDown`, 5-tap `pBlur`) added at 0.55 and 0.85 in `pComp`; then tone map, a vignette
  (corners up to 42 % darker) and ±2-level grain new each frame (`u_seed`); a navy glow (`u_bg`) fades in over 0.6 s.
- The core, halos and flash are analytic glows in `pComp` at `W / 2`, `H / 2 + GAL_CY * zc` (`coreAt`, `flashAt`).
  No paper, scanlines, chromatic aberration or lens flare.

## Shapes, line and figures
- Nothing is outlined or filled: every form is particles with trails, from one of two sources:
  - a mask: anything drawn solid white into the offscreen canvas in `textTargets()` (text, a filled path, an image),
    which keeps `NT` random opaque pixels as targets (it needs at least `NT`: New subject);
  - a slot function like `galaxyAt(i, t, o)`: each particle owns a slot (radius, angle, height) that moves with t.
    The galaxy has a 10 % bulge and two logarithmic arms; inner slots turn faster (`gW`).
- Assignment decides the motion: particles sorted by start x (± 260 px noise) meet targets sorted by x, and `del`
  delays each by its target's x, so the word builds left to right; galaxy slots go by distance from the word's centre.
- Particles join a form on a spring: stiffness `42 * w`, damping ratio 0.42 (overshoot), force capped at 9000. The
  flow's pull fades to 12 px/s, which the spring cancels: a settled form holds still (about 0.1 px/s), points only.
- Depth: chaos starts within ±320 px in z, the word flattens to a 5 px spread (`gauss() * 5`). The 6,000 dust
  particles (`i >= NT`) drift at z −700 to 950 as bokeh; in the demo they become the galaxy's halo and collapse with
  it (the held-point plans keep them in the flow: Shorter). The galaxy disc is tilted by `SIN_A` (0.40) and rolled by
  `ROLL` (−0.2 rad). No figures or detailed objects: a form must read as a bold silhouette.

## Composition and camera
- One centred formation about three quarters of the frame wide, a little above centre (`TEXT_CY`), the galaxy 30 px
  below (`GAL_CY`), flow and dust around it. Overlay at 76 px margins: top baselines 88 and 116; bottom, the "velocity"
  label 982, the bar at `ly` 1000, slow/fast and readout 1028; right column right-aligned at 1844.
- Camera: a fixed perspective (focal `F` 2400 px, centred) used only for depth and depth of field. `zoomAt` pushes in
  2.5 % over the film and another 7 % during the collapse (7.5–9.3 s). No orbit, pan or cut.
- Other formats (rendered on the 10 s held-point plan): every shot keeps trails, speed colour, bloom and a whole
  formation (the 9:16 galaxy's outer arms run off both sides, as the demo's reach them); largest empty band 13 %
  (16:9, galaxy), 1 % (9:16, 1:1); 9:16 key text stays inside x 76–950, y 288–1440.

| Value in code | 16:9 demo | 9:16 (1080 × 1920) | 1:1 (1080 × 1080) |
|---|---|---|---|
| `PVS` divisors `960.`, `540.`; `pComp` `1080.-gl_FragCoord.y` | 960, 540; 1080 | 540, 960; 1920 | 540, 540; 1080 |
| `pComp` glow centre `vec2(960.,560.)`, radius `vec2(1150.,760.)`; vignette `vec2(1.,.82)` | as written | 540, 980; 650, 1350; .82, 1 | 540, 560; 650, 760; 1, 1 |
| `RT` bloom sizes (and the `1.6 /`, `0.5 /`, `2.2 /` divisors) | 480 × 270, 160 × 90 | 270 × 480, 90 × 160 | 270 × 270, 90 × 90 |
| `GX`, `GY`, `GX0`, `GY0` | 145, 85, −1440, −840 | 82, 145, −810, −1440 | 82, 82, −810, −810 |
| start cloud (1150, 680); soft walls (1020, 600) in `simulate()` | as written | 730, 1100; 600, 1020 | 730, 680; 600, 600 |
| `NT` of `N` = 40000 (dust = the rest) | 34000 | 22000 (18,000 dust) | 26000 |
| word width: 1420 in `textTargets()`, `+ 710) / 1420` in `del` | 1420 | 820 (148 px type, x 128–945) | 860 |
| `TEXT_CY`, `GAL_CY` | −40, 30 | −60, −60 | −20, 10 |
| galaxy scale, `SIN_A`, `ROLL` | 1, 0.40, −0.2 | 0.72, 0.68, −0.55 | 0.66, 0.55, −0.35 |
| burst radius `d / 700` | 700 | 404 | 424 |
| wave sweep (−900 + 1800 ·); its forces 5200, 2200 | ±900; × 1 | ±520; × 0.6 | ±540; × 0.65 |
| overlay x left / right; top baselines; legend `ly`, readout y | 76 / 1844; 88, 116; 1000, 1028 | 76 / 950; 330, 364; 1380, 1410 | 60 / 1020; 80, 114; 1000, 1028 |
| overlay sizes; legend width `lw` | 19 / 15 px; 240 | 25 / 20 px; 300 | 25 / 20 px; 300 |

- Galaxy scale: multiply `gR[i]` and `gH[i]` where `galaxyAt()` reads them.
- 9:16, why: `NT` 22000 leaves 18,000 dust particles to texture the bottom band (34000 left it 1.2 % lit); the
  steeper tilt and roll fill y 260–1430, where the demo's tilt gives a thin band; the full-strength wave smeared the
  letters. Keep a subject's lowest pixel 50 px above `ly`.

## Motion
- Particles move by physics integrated once in `window.ready`, with no easing curve; every ramp is `sstep()`
  (smoothstep): the flow's grip, each particle's spring weight `w` over 0.75 s, the overlay, the fades.
- Chaos: particles relax toward the flow (250 px/s, rate 2/s; dust 150 and 1.4); walls 60 px outside the frame.
- Assembly: `del` from 1.85 s at the left to 2.90 s at the right, plus up to 0.25 s jitter (last ramp starts 3.15 s);
  arrivals are fast (amber) and overshoot. Wave (4.05–4.95 s): a 90 px band sweeps right, lighting the letters cyan.
- Inhale (5.0–5.35 s): a stiff spring pulls the word in by 7.5 % (anticipation). Burst (5.35 s): a radial kick of up to
  about 1300 px/s, stronger farther out, a 420 px/s clockwise swirl and a scatter in depth.
- Galaxy: from 5.6 s particles spring onto rotating slots (ζ 0.75, velocity-matched), text by 6.15 s, dust by 6.9 s.
  Collapse: from `cDel` (7.55 s at the centre, up to 0.52 s later at the rim) each slot shrinks over 1.05 s on
  `Math.pow(sstep(...), 1.6)`, turning 5.5 rad more; collapsing particles dim (`cw`) so the pile reads as a point.
- Never: camera rotation, bounce in the overlay, or unseeded randomness.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–1.0 | fade up from black (navy glow 0–0.6, overlay 0.5–1.3) | `fadeAt`, `u_bg`, `overlay()` |
| 0–1.85 | chaos: the flow field alone; label 01 CHAOS | `flow()`, `PHASES` |
| 1.85–3.9 | the word assembles left to right; letter chimes 2.47–3.36; 02 FORM from 2.1 | `del`, `letterT` |
| 4.05–4.95 | wave sweeps the word | `waveOn` |
| 5.0–5.35 | inhale | `T_ANT` |
| 5.35 | burst; 03 GALAXY | `T_BURST` |
| 5.6–6.9 | the galaxy forms; chord cue at 5.9 | `T_GAL`, `galaxyAt()` |
| 6.15–7.55 | the galaxy turns | `gW` |
| 7.55–9.1 | collapse spiralling inward; 04 SINGULARITY from 7.65; push-in 7.5–9.3; core glows from 7.9 | `T_CONV`, `cDel`, `zoomAt`, `coreAt` |
| 8.9–9.5 | overlay fades out | `overlay()` |
| 9.05 | flash | `coreAt`, `flashAt` |
| 9.05–9.95 | core decays to 9.9; particles fade 9.15–9.8; glow 9.2–9.95 | `coreAt`, `fadeAt`, `u_bg` |

- One continuous shot; phase labels mark chapters; each hand-over is the particles re-forming; beats of 1.5–2 s.
  Reusable: chaos opening, assembly into a mask, wave, inhale-and-burst, analytic formation, collapse to a point.
- KEYS for contact_sheet.sh: 3.4 (the rush), 4.5 (word under the wave), 5.45 (burst), 7.2 (galaxy), 9.06 (flash), and
  the held final state of the plan you use (10 s: 9.3; 4 s: 3.3).
- The demo's ending never holds: against an end-state copy nothing settles before 9.87 s, after the fade has begun
  (the flash peaks at 9.06 and the core decays at once). Shorter gives a tested 10 s re-timing that holds the point.

## Sound
audio.py reads `events.json` as `{t, k, …}` cues; NumPy synthesizes all (seeded `rs`), 1.8 s reverb, tanh limiter.
- `speed` (required, looked up by name: StopIteration without it): `v` is the `meanV` curve, one value per frame. It
  sets `act` (speed / 600, up to 1.5), which drives an airy noise wash (`we`) and a cloud of tiny high sine grains.
- `lock` with `i`: two FM bells (`bell()`) per letter on `CHIME` (A C D E G A, panned left to right). `wave`: 24 pings
  over 0.95 s, panned left to right. `inhale`: a reverse noise swell and rising `sweep()`. `burst`: sub drop, crash,
  four bells. `galaxy`: a 3.4 s chord. `collapse`: risers up to audio.py's flash time. `flash`: a boom and bells.
- Written at fixed times, not cued: an A-minor drone (`dr_env`: 1.8 s quadratic attack, dying 0.25 s after a written
  9.05); the wash (1 s attack, ending at a written 9.1); grains placed between 0.15 and 9.1 s; the `collapse` riser's
  end (9.05); the master fades over the last 0.3 s. A new flash time replaces 9.05, and it plus 0.05 replaces 9.1.
- Breakers (tested): `lock` without `i` gives KeyError, `i` from 6 IndexError (six `CHIME` notes); with `CHIME`
  extended, `i` = 7 pans past +1 and NaN silences the left channel while audio.py prints "audio.wav ok nan". A `collapse`
  at or after the written flash time gives ValueError in `band()`. Unknown kinds and cues past `DUR` are dropped.
- A new film sends `speed`, a `lock` per letter or part (at most six), `wave`, `inhale`, `burst`, `galaxy` when a
  formation blooms, `collapse` and `flash`. `DUR` may be any length (`int(SR * DUR)` samples).

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Seeded noise, flow, random streams | `anim.html` → `bakeFlow()`, `noise()`, `flow()`, `mulberry()`, `gauss()` | grid `GX` × `GY` × `GT` at 20 px and 0.5 s; `flow(x, y, t)` fills `FL`; one `rnd` stream consumed in a fixed order | as is; resize the grid for formats and lengths; reordering calls reshuffles every later value |
| Simulation | `anim.html` → `simulate()` | step `DT` (`SUBS` 2 per frame); stores every frame in `hist` (Int16, `Q` 0.08 px) and `meanV` | adapt: timeline constants |
| Targets from a mask | `anim.html` → `textTargets()` | draws into a `W` × `H` canvas, keeps `NT` opaque pixels, returns letter `bounds` for the chimes | adapt: word or shape |
| Analytic formation | `anim.html` → `galaxyAt()` | `galaxyAt(i, t, o)` writes the slot into o and returns the collapse progress | adapt or replace |
| Particle renderer | `anim.html` → `renderGL()`, `prog()`, `PVS`, `PFS`, `RAMP` | trails `LV` and points `PV` rebuilt from `hist` each frame | as is (format values in Composition) |
| Bloom and finish | `anim.html` → `tex()`, `pass()`, `texU()`, `RT`, `pDown`, `pBlur`, `pComp` | core light at `u_core`, flash `u_flash`, grain `u_seed` | as is |
| Timeline helpers and cues | `anim.html` → `zoomAt`, `fadeAt`, `coreAt`, `flashAt`, `PHASES`, `window.events` | literal times; `letterT` is each letter's mean `del` + 0.42 | adapt |
| Lab overlay | `anim.html` → `overlay()` | header, spec line, phase labels, timer, legend, readout | adapt: copy, positions |
| Sound | `audio.py` → `bell()`, `sweep()`, `band()` | per-cue handlers, fixed drone and wash | adapt: the fixed times |
| Demo plot | `T_ANT`, `T_BURST`, `T_GAL`, `T_CONV`, `waveOn`, 'EMERGE' | | replace |

## Adapting
- **Style vs demo plot:** the style is the swarm and its finish (flow-field chaos, additive trails coloured by speed,
  depth of field, bloom, vignette, grain on navy), forms reached only by particles travelling, and the lab overlay.
  The plot is the order of forms and their times; any change of form is the transformation (chaos to a word or logo,
  a burst, a chart growing, a collapse to a point).
- **New subject:** replace the word in `textTargets()` (four times; its `k <= 6` loop measures six letter bounds, and
  `simulate()` holds six `letterDel` lists with `while (L < 5 …)`) or draw a filled shape into the mask. The mask needs
  at least `NT` opaque pixels: check the opaque-pixel list's length or lower `NT` to it, or the missing targets are
  NaN, clump at the centre, and audio.py stops with TypeError (20 letters in 9:16: 18,567 pixels for 22,000).
  Stand-in rendered in 9:16: four bars 150 px wide on a 200 px pitch, 300–840 px tall, standing on y 1320, `TEXT_CY`
  −60 (their box centre), built bottom-up; they read from 3.4 s, complete by 4.3. Values tied to the shape:
  - the sort axis in `ord` and `tg` and the `del` formula (x across 1420 px). For the bars: sort particles by −y and
    targets by descending y, and set `del` from the height fraction;
  - `TEXT_CY` is also the centre of the inhale and the burst;
  - the 2.2 in the galaxy ranking is the word's aspect: 0.8 for the bars;
  - the burst radius 700 (450 for the bars);
  - the chimes come from the letters' `bounds`: one per bar (four `lock` cues), and never more than six. For a word
    longer than six letters, set the six bounds at equal sixths of its width (x0 + w · k / 6, k = 1…6) instead of at
    letter edges, so the chimes spread over the whole build (tested with INNOVATION: six chimes 0.80–1.09 s).
- **Ending on a form:** at any length, lift its points as in the 4 s plan's `renderGL()` line, finishing before the
  hold; a settled form is otherwise a dim violet stipple (no trails, slowest colour, little bloom).
- **Length:** past 10 s, raise `DUR` in anim.html (it sets `NF`, the stored frames; past them the film freezes) and
  `GT` (21 slices cover 10 s; `flow()` freezes after them), then audio.py as in Sound. Move on from a settled word
  within about 2 s. A second word (name, then tagline) is untested; it needs a second target set from `textTargets()`
  matched by the particles' first target x, a second `del` from the switch, new chime `bounds`, and the galaxy
  ranking, which reads `tx` and `ty`.
- **Shorter:** re-time the simulation's schedule, never the playback: the flow field and dust stay on film time
  (`flow()` reads t); write the ambient push as `0.025 * t / 10`. Holds are measured by pixels against a twin film:
  - point endings: text particles read the last frame of a simulation run 3 s longer, the core at its held level,
    the push done, the dust on film time; settled means no pixel more than 2 levels off;
  - word endings: right after the targets are assigned in `simulate()`, every text particle gets its target position,
    zero velocity and `del` −10, so the twin carries the same ambient jitter (about 0.1 px/s). Settled means every text
    particle within one `Q` step (0.08 px) of its twin; after that only single-pixel rounding flips (up to about 40
    levels) differ, never streaks.

  Tested plans (contact sheets, check_audio.py). "a + b + c; r" is `del` = a + b · clamp(…) + c · `rnd()` and ramp r,
  the 0.75 in `sstep(del[i], del[i] + 0.75, t)`:

| Literal | demo | 10 s, held point | 8 s, all phases | 6 s, no galaxy | 4 s, word only |
|---|---|---|---|---|---|
| fade in: `fadeAt`, `u_bg`, overlay | 1.0, 0.6, 0.5–1.3 | as demo | 0.8, 0.5, 0.4–1.0 | 0.6, 0.4, 0.3–0.8 | 0.6, 0.4, 0.3–0.8 |
| `del`; ramp | 1.85 + 1.05 + 0.25; 0.75 | as demo | 0.9 + 0.75 + 0.15; 0.6 (9:16: taper, cap) | 0.45 + 0.45 + 0.1; 0.45 (9:16: taper, cap) | 0.35 + 0.4 + 0.1; 0.4, taper, cap, lift |
| wave (`waveOn` and the start in `wx`, cue) | 4.05–4.95 | 3.5–4.4 | none | none | none |
| `T_ANT`, `T_BURST`, `T_GAL` | 5.0, 5.35, 5.6 | 4.4, 4.75, 5.0 | 2.85, 3.2, 3.45 | 1.8, 2.15, 2.4 | 99 (never) |
| ends of the galaxy pull: text 6.15, dust 6.9 (dust: unused while it stays in the flow) | 6.15, 6.9 | 5.55, – | 4.0, – | 2.95, – | – |
| `galaxy` cue; `T_CONV`; flash TF | 5.9; 7.55; 9.05 | 5.3; 6.4; 7.9 | 3.75; 4.35; 5.85 | dropped; 2.4; 3.9 | none (cues dropped) |
| push in `zoomAt` (7.5–9.3) | 7.5–9.3 | 6.35–8.15 | 4.3–6.1 | 2.35–4.15 | none |
| dust kept in the flow | no | yes | yes | yes | – |
| `PHASES` FORM label (2.1) | 2.1 | 2.1 | 0.9 | 0.45; delete the `T_BURST` row and number SINGULARITY 03 (no galaxy; a label at `T_BURST` would peak at half opacity) | 0.35 |
| fade out F0–F1 | particles 9.15–9.8, core to 9.9 | 9.67–9.97 | 7.72–7.98 | 5.72–5.98 | 3.72–3.98 |
| settled, measured | never | 8.733–9.667 | 6.80–7.72 | 4.80–5.72 | 2.733–3.72 |
| audio.py `DUR`; 9.05 → ; 9.1 → | 10; 9.05; 9.1 | 10; 7.9; 7.95 | 8; 5.85; 5.9 | 6; 3.9; 3.95 | 4; 3.72; 3.77 |

```js
// Every plan: the burst fires on the substep that crosses T_BURST, and on the 1/60 s grid rounding can skip it
// (3.2, the 8 s plan's, does). Allow for it; the demo, 10 s and 6 s plans are unchanged:
const burst = t < T_BURST - 1e-6 && t + DT >= T_BURST - 1e-6;   // was: t < T_BURST && t + DT >= T_BURST
// Held point (10, 8, 6 s): keep the dust in the flow to the end with three edits in simulate():
if (t < T_GAL || dust) {                                  // was: if (t < T_GAL || (dust && t < T_GAL)) {
if (t < T_BURST || dust) {                                // the soft walls
cDel[i] = T_CONV + 0.3 + 0.2 * rnd() + 99; del[i] = 99;   // dust never collapses or dims; keeps the rnd() call
// and the timeline (TF = flash, F0–F1 = closing fade, FADE_IN, BG_IN, OV0–OV1 = the fade-in row):
const fadeAt = t => sstep(0, FADE_IN, t) * (1 - sstep(F0, F1, t));
const coreAt = t => (0.35 * sstep(TF - 1.15, TF - 0.05, t) + 2.6 * Math.exp(-Math.pow((t - TF) / 0.11, 2)) * (t < TF ? 0.35 : 1)
  + 0.9 * sstep(TF - 0.1, TF, t) * (1 - 0.6 * sstep(TF, TF + 0.5, t))) * (1 - sstep(F0, F1, t));
const flashAt = t => Math.exp(-Math.pow((t - TF - 0.01) / 0.14, 2));
// u_bg: sstep(0, BG_IN, t) * (1 - sstep(F0 + 0.05, F1, t));
// overlay a: sstep(OV0, OV1, t) * (1 - sstep(F0, F1, t)) in every plan, so the held state keeps the lab frame (the demo
// clears it at the flash). 4 s: coreAt and flashAt return 0; u_bg as above.
// In simulate()'s spring (4 s plan; 8 s and 6 s plans in 9:16), a taper and a raised cap replace k, c and cap (the
// arrival and first overshoot are unchanged):
const zr = sstep(del[i] + 0.4, del[i] + 0.8, t), zeta = 0.42 + 0.28 * zr;
const k = 42 * w * (1 + 0.5 * zr), c = 2 * zeta * Math.sqrt(k) * (1 + 0.3 * (1 - w));
const fm = Math.abs(fx) + Math.abs(fy), cap = 9000 * (1 + 3 * zr);
// In renderGL(), lift the settled word's points; the ramp ends before the hold:
PV[q + 3] = cw * (0.3 + 0.7 * sd) * (i < NT ? 1 + 1.5 * sstep(1.6, 2.4, t) : 1);
```
  - Cut in this order: the wave; the galaxy's hold (0.35 s in the 8 s plan); the galaxy (6 s: the word bursts
    straight into the collapse, `T_CONV` = `T_GAL`); the burst and the point (4 s: end on the word). Shortest
    opening (4 s plan): the assembly starts at 0.35 s, inside the 0.6 s fade-in; the right of the frame stays chaotic
    until about 0.9 s, so about 0.3 s of chaos shows at full brightness.
  - Costs: a point ending takes about 3.6 s from `T_CONV` (1.5 s collapse, about 0.9 s to settle, 0.8 s hold, fade); a
    word settles about 1.5 s after its last ramp ends with the taper and raised cap (2.2 s with the taper alone).
  - Remove the cues of cut beats; pushed past `DUR` they are dropped, except `collapse`, which crashes audio.py.
  - 9:16: the 4 s plan with `del` from 0.3 and a 0.35 spread (the taller cloud travels farther) settles by 2.767
    (0.95 s held); the 10 s plan at 8.767 (0.90 s); 1:1 10 s at 8.733. The 8 s and 6 s plans in 9:16 need the taper
    and raised cap too: without them the taller cloud is still arriving at `T_ANT` and the word reads only during the
    inhale; with them it is whole from 2.4 s (8 s) and 1.6 s (6 s) and crisp from 2.6 s and 1.8 s (the 6 s word is
    sharpest during the inhale, as in 16:9), and the point settles at 6.667 (1.05 s held) and 4.80 (0.92 s).
- **Other formats:** Composition; the settled 9:16 word (x 128–945, y 831–947) and point stay in the safe bands.

## Boundaries
- **Distinct from:** `cosmic-epic` (photoreal deep space, nebulae, planets, timeline titles; here the galaxy is an
  abstract particle formation in a lab frame); `blob-sim` (cute shaded 3D creatures in a rule-based simulation);
  `liquid-motion` (gooey blobs, warm gradients); `oscilloscope`, `vector-arcade` (one beam or vector lines);
  `kinetic-typography` (real type to rhythm); `data-visualization` (readable values; a swarm draws only silhouettes).
- **Poor fit:** copy-heavy messages (`kinetic-typography`, `bold-captions`), readable charts (`data-visualization`),
  space documentaries (`cosmic-epic`), simulated agents (`blob-sim`), warm brands (`liquid-motion`), people
  (untested, and a particle silhouette loses the limbs review.md asks for).
- **Do not:** set the formation as real text or fade in a crisp logo over the swarm; cross-fade or cut between forms;
  add a warm or light background; show two formations at once; use a real brand, study name or seed you cannot invent.

## Technical notes
- No `render.json`: Chromium's default gave WebGL2 through SwiftShader (software) even on a Mac with a GPU.
  `simulate()` takes about 2.1 s per page (`window.simMs`, 0.22 s per second of film), frames 0.15–0.2 s: a 10 s build
  takes about a minute on one worker. `"gpu": "full"` draws a frame in 0.04 s (Apple M2) but changes the image (30 dB
  PSNR against SwiftShader, line rasterisation; same look): keep one backend per film.
- Deterministic as shipped: stills byte-identical alone and after other frames (4.2, 8.5 s) on both backends, so no
  PSNR allowance is needed. Every page and `events.mjs` re-run `simulate()` from t = 0 with the seeded `rnd`.
- Per page: `hist` 7.2 MB per second of film plus 11 MB of `LV`; Int16 clamps positions at ±2,621 px (`Q`). `HALF`
  needs `EXT_color_buffer_float` (else RGBA8 clips the sums). `textTargets()` uses canvas `letterSpacing` (Chromium
  99+). `overlay()` assigns `ctx.globalAlpha` in save/restore: multiply it if you add a 2D fade around it.
- Sizes hard-coded outside `W`/`H`: every literal in the Composition table.
