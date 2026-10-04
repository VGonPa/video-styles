# 80s Anime (`anime-80s`)

Intro.

**Reference film:** demo · `styles/anime-80s/`

## Signature
None.

## Palette
| Role | Colour | In code |
|---|---|---|
| ink | `#2a1328` | `P.ink` |
| sky pink | `#e2657c` | `P.skyPink` |


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
| cel fill | `common.js` → `celShape(g, build, fill, line, lw)` | | as is |
| shot A | `shotA.js` → `initA()`, `drawA(g, t)` | | replace |
| held cels | `cel(t, fps)` | fps 12 = on twos | as is |


## Adapting
None.

## Boundaries
None.

## Technical notes
None.
