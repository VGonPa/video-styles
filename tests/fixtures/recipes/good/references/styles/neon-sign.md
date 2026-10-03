# Neon Sign (`neon-sign`)

Glass neon tubes on a wet brick wall at night: script and block letters strike, buzz, flicker and reflect in a
puddle. Moody and urban.

**Reference film:** a diner sign lights word by word, a letter faults, then the power is cut · `styles/neon-sign/`

## Signature
- Dark brick wall (`buildTextures()`), tubes with a white-hot core, coloured body and a wide glow.
- Tubes strike on with a flicker (`strike(t, t0, seed)`).
- A wet-ground reflection below the horizon (`HORIZON`, `REFL_K`).

## Palette
| Role | Colour | In code |
|---|---|---|
| pink tube body | `255,45,150` | `COL.pink.body` |
| pink core | `255,226,242` | `COL.pink.core` |
| cyan tube body | `30,215,255` | `COL.cyan.body` |
| amber glow | `255,135,10` | `COL.amber.glow` |
| mortar | `#5c554e` | `buildTextures()` |
| bricks | `hsl(${h},${s}%,${l}%)` | `buildTextures()`: h 6–18, s 30–52, l 22–35 |

- Light is additive: glow layers are blurred copies at lower resolution (`LB`, `GA`, `GB2`, `GC`).

## Typography and copy
- Letters are Hershey centrelines turned into tubes (`place()`, `chaikin()`, `resample()`), not fonts.
- One or two words per sign, lower case script or caps.

## Texture and finish
- Brick albedo baked once at 2× (`BS = 2`); wet sheen and puddle (`puddle`).

## Shapes, line and figures
- Tube width 6–10 px (`w` in `place(key, cx, top, sc, color, w, group, smooth)`).

## Composition and camera
- Sign centred above the horizon; a slow push (`camera(t)`).

## Motion
- Strikes stagger by 0.1 s per letter; faults (`FAULTS`) flicker at 60 Hz steps.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–1 | pen writes the script | `T_PEN0`, `T_PEN1`, `penX(t)` |
| 4.3 | "served" strikes | `SERVED` |
| end | power cut | `T_CUT`, `cut(t, delay)` |

## Sound
- Cues: `pen` (d), `strike` (v 0.5–1), `tick` (v), `crackle` (d), `cut`.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| tube geometry | `place()` | `place(key, cx, top, sc, color, w, group, smooth)` | adapt: new words |
| tube drawing | `strokeTube(c, tb, frac, width, style)` | | as is |
| brick wall | `buildTextures()` | | as is |
| faults | `faulty(t)`, `FAULTS` | | adapt |

## Adapting
- **New subject:** new words through `place()`; keep the wall and glow.
- **Length:** add strikes and faults.
- **Other formats:** stack words vertically.

## Boundaries
- **Distinct from:** `synthwave`, `vaporwave`.
- **Poor fit:** long text; use `kinetic-typography`.
- **Do not:** copy real brand signs.

## Technical notes
- `render.json` `{ "gpu": "full" }` (GPU raster, not WebGL).
