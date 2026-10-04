# Low-Poly 3D (`low-poly`)

Intro.

**Reference film:** demo · `styles/low-poly/`

## Signature
None.

## Palette
| Role | Colour | In code |
|---|---|---|
| sky top | `#56a6f0` | `PAL.top` |
| gem rim light | `#ff8ad8` | `gemRim` |
| title glow | `#fff1e4` | |


## Typography and copy
None.

## Texture and finish
None.

## Shapes, line and figures
None.

## Composition and camera
None.

## Motion
None.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–1 | title | `T` |

## Sound
None.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| three.js | `vendor/three.min.js` | `THREE.MeshStandardMaterial({ flatShading: true })` | as is |
| palette ramps | `palAt(name, t, out)` | name: `'sun'`, `'top'`… | as is |
| title glow | `octx.filter = 'blur(10px)'` | font `"800 184px 'Outfit'"` | adapt |
| length | `build.sh` | `DUR` | edit |


## Adapting
None.

## Boundaries
None.

## Technical notes
None.
