# Cosmic Epic (`cosmic-epic`)

A slow, awe-struck deep-time film rendered in a raymarched WebGL2 shader: a gas giant, a dying star, a
supernova and a sky whose stars go out one by one. Thin, widely tracked titles count the years. Majestic and
melancholic.

**Reference film:** ten billion years compressed into ten seconds, ending in darkness · `styles/cosmic-epic/`

## Signature
- A lit planet limb against a dense star field, with a filmic bloom and lens flare (the `COMP` pass).
- A counter in thin, wide-tracked caps at the bottom centre ("10 BILLION YEARS FROM NOW").
- Everything moves slowly; the camera drifts (`camera(t)`), nothing cuts.

## Palette
| Role | Colour | In code |
|---|---|---|
| nebula teal | `vec3(0.05,0.55,0.62)` | `TEAL` in the `SCENE` shader |
| nebula violet | `VIOLET = vec3(0.34,0.10,0.62)` | `VIOLET` |
| atmosphere rim | `vec3(0.16,0.55,1.0)` | `SCENE` → `atm` |
| title white | `rgba(236,242,255,…)` | `title()` |
| title glow | `rgba(170,205,255,…)` | `title()` → `ctx.shadowColor` |
| supernova flash | `[0.8, 0.9, 1.0]` | `uFcol` |

- Colour lives in linear light inside the shaders and is tone-mapped in `COMP` (`pow(c, vec3(1./2.2))`).
- Never flat fills: every colour is light, with bloom.

## Typography and copy
- `'Montserrat'` at weight 100–300 (`FONT`), all caps, letter-spacing 0.16–0.7 em via `ctx.letterSpacing`.
- Copy is short, declarative, present tense: at most 34 characters per caption line at 24 px.
- Superscripts for powers are built by `title(runs, …)` with `k` (scale) and `up` (raise) per run.

## Texture and finish
- Film grain from `buildGrain()`, offset 12 times a second (`uGOff`).
- Bloom: a 7-level mip chain (`DOWN`, `UP`) added in `COMP` with `uBloomK` (0.16).
- Chromatic aberration at the edges in `COMP`.

## Shapes, line and figures
- No lines and no figures: bodies are spheres raymarched in `SCENE`, stars are GL points (`STARV`).
- A new object must be a lit volume in the shader (a sphere, a ring), never a 2D drawing.

## Composition and camera
- One dominant body off-centre; the star behind it; titles centred low (y 912 and 984).
- The camera interpolates `CAMA` → `CAMB` in `camera(t)`.
- 9:16: move the body to the upper third and the counter to the middle; the shader takes `uRes`.

## Motion
- `sm(a, b, t)` (smoothstep) for every fade; `easeIn3` for the collapse. No overshoot, no bounce.
- Text tracking keeps opening while a title holds.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.9 | fade up from black | `uFade`, `sm(0.0, 0.9, t)` |
| 0.9–3.7 | first caption | `CAPS[0]` |
| 3.3 | the star swells | `T_SWELL`, `{ k: 'swell' }` |
| 4.75 | collapse | `T_COLL` |
| 5.2 | supernova | `TB`, `supernova(t)` |
| 8.05 | final title in darkness | `T_TITLE` |

- Beats are long (2–3 s) and overlap: one caption fades out as the next event starts.

## Sound
- audio.py: a D-minor drone bed (`pad()`), a `shimmer()` when the star clears the limb, a `riser()`, an `inhale()` for the collapse, a `boom()` and a `bell()` for the title, through a convolution hall.
- Cues: `tick` (v 0.7–1, n), `emerge`, `swell`, `collapse`, `burst`, `title`.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| shader programs | `anim.html` → `prog(vs, fs)`, `sh(type, src)` | | as is |
| scene shader | `SCENE` | `uniform vec3 uCam, uR, uU, uF; uniform float uTan, uT` | adapt: new bodies |
| star field | `STARV`, `buildStars()` | `NSTAR` points | as is |
| bloom + grade | `DOWN`, `UP`, `COMP` | `uBloomK`, `uExpo`, `uFade` | as is |
| titles | `title()` | `title(runs, x, y, size, track, alpha, weight, glow)` | as is |
| timeline | `T_SWELL`, `T_COLL`, `TB`, `CAPS`, `counter(t)` | | replace |

## Adapting
- **New subject:** keep the bloom, grain and title system; write new bodies in `SCENE`.
- **Length:** stretch the holds; the counter can run longer.
- **Other formats:** set `W`, `H` and the canvas; the shaders read `uRes`.

## Boundaries
- **Distinct from:** `particles` (abstract), `kurzgesagt` (flat vector space).
- **Poor fit:** jokes, UI, people; use `kurzgesagt`.
- **Do not:** add sci-fi HUD graphics.

## Technical notes
- WebGL2 with `render.json` `{ "gpu": "full", "schedule": "contiguous" }`; slow without a GPU.
- Frames are a pure function of `t` (seeded `mulberry32`), so the contiguous schedule is not needed by new code.
- Hard-coded: `W = 1920, H = 1080`, the title y positions (912, 984, 566, 652).
