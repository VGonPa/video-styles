# Oscilloscope (`oscilloscope`)

A vintage X–Y vector monitor whose green phosphor trace draws Lissajous figures, a wireframe cube and a word,
and whose soundtrack is the very signal that deflects the beam. Precise, nerdy, hypnotic.

**Reference film:** a scope warms up, sweeps, plays Lissajous chords, draws a cube and parks the beam · `styles/oscilloscope/`

## Signature
- The instrument front panel (graticule, knobs, readouts) fills the frame; the screen glows green.
- A single bright beam with decaying phosphor afterglow and bloom (`phosphor(t)`, `compose()`).
- What you see is what you hear: the left channel is X and the right channel is Y.

## Palette
| Role | Colour | In code |
|---|---|---|
| phosphor (red channel) | `255 * (c * 0.30 + hot * 0.62 + glow * 0.16)` | `compose()` |
| phosphor (green channel) | `255 * (g + hot * 0.1)` | `compose()` |
| readout label | `#5fdc8c` | `panel(t)` |
| readout value | `#b8ffd0` | `panel(t)` |
| lamp green | `[110, 255, 150]` | `lamp()` |
| lamp red | `[255, 120, 60]` | `lamp()` |
| screw metal | `#8d9294` → `#2c3032` | `screw()` |

- The trace colour is computed per pixel from beam energy (`E`), halo and bloom; white-hot where the beam dwells.

## Typography and copy
- `'Barlow Condensed'` (`FONT`) for the panel legends; `'IBM Plex Mono'` (`MONO`) at 30 px for the readouts.
- Copy is instrument labels in caps: "CH1 X", "RATIO", at most 12 characters.

## Texture and finish
- Phosphor energy integrated over the recent past of the signal (`decayAt(t)`), blurred by `boxBlur()` into a halo and bloom.
- Static layers baked once in `buildStatic()`: `FRONT`, `GRAT`, `GLARE`.

## Shapes, line and figures
- Only the beam draws: paths are tables built by `makePath(pts, wts)` and sampled by `pathAt(P, f, out)`.
- Text on screen is drawn by the beam from `GLYPHS` strokes.

## Composition and camera
- Locked-off camera; the screen sits left (`SX`, `SY`, `SW`, `SH`), the panel right.
- 9:16: stack the screen above the panel.

## Motion
- The beam moves at audio rate (`SR = 48000`); the camera never moves.
- Knobs ease with `eBack` and `eInOut`.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0.08 | power lamp | `T.lamp` |
| 0.22 | beam appears | `T.beam` |
| 1.05–2.15 | time base spins up | `T.spin0`, `T.spin1` |
| 2.62–3.3 | the FREQ knob turns | `T.knob0`, `T.knob1` |
| end | beam parked on a dot | `T.dot` |

## Sound
- There are no cues: `window.signal()` returns the X,Y samples, events.mjs writes `xy.f32` (`render.json` `signal`), and audio.py filters it (`dc_block()`, `onepole_lp()`) and normalises to −8.5 dBFS.
- To change the sound, change `buildSignal()`; audio.py stays as is.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| signal | `anim.html` → `buildSignal()` | 48 kHz X,Y in `SXa`, `SYa` | adapt: new figures |
| phosphor | `phosphor(t)`, `compose()` | `GAIN`, `expoAt(t)`, `decayAt(t)` | as is |
| vector paths | `makePath(pts, wts)`, `pathAt(P, f, out)` | | as is |
| front panel | `buildStatic()`, `panel(t)`, `KNOBS` | | adapt: labels |
| audio | `audio.py` | `dc_block(x, fc)`, `onepole_lp(x, fc)` | as is |

## Adapting
- **New subject:** draw new figures as paths in the signal; keep the phosphor and the panel.
- **Length:** `NS = SR * DUR` sizes the signal; audio length follows it.
- **Other formats:** the phosphor buffer is `SW × SH`; resize it with the screen.

## Boundaries
- **Distinct from:** `terminal` (text console), `sci-fi-interface` (HUD).
- **Poor fit:** characters and stories; use `retro-desktop`.
- **Do not:** add sound that is not the signal.

## Technical notes
- Canvas 2D with `ImageData` per frame; heavy CPU per frame (about 3 minutes for 10 s).
- `render.json` is `{ "signal": "xy.f32" }`.
