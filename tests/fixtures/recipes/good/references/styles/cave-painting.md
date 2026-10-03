# Cave Painting (`cave-painting`)

Intro.

**Reference film:** demo · `styles/cave-painting/`

## Signature
None.

## Palette
| Role | Colour | In code |
|---|---|---|
| red ochre | `#9a3a22` | `PIG.red` in `js/animals.js` |
| charcoal | `#231a15` | `PIG.char` |


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
| animals | `js/animals.js` → `drawAnimal(ctx, a)` | `a.kind`, `a.fill`, `a.shade` | adapt |
| tapered stroke | `js/lib.js` → `taper(ctx, P, Wd)` | P: points, Wd: widths | as is |
| timeline | `js/scene.js` → `HERD`, `flicker(t)` | | replace |


## Adapting
None.

## Boundaries
None.

## Technical notes
None.
