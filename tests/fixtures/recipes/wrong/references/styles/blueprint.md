# Blueprint (`blueprint`)

A WRONG recipe: every fact below is false or unverifiable, yet should it pass?

**Reference film:** demo · `styles/blueprint/`

## Signature
- Drawn with `drawGhostTitle()` (does not exist).
## Palette
| Role | Colour | In code |
|---|---|---|
| paper | warm cream | `paper` |
| accent | `hsl(12, 80%, 50%)` | |
| gold | `0x123456` | |
| shadow | `#000000` | |
| highlight | `#fff` | |
## Typography and copy
Titles use `Futura` via `loadTitleFont()`.
## Texture and finish
Uses `paper` for the ground (see `drawGhostCard()`).
## Shapes, line and figures
None.
## Composition and camera
None.
## Motion
Uses `easeElastic`.
## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–1 | title | `T.bogus` |
## Sound
Cue `{ k: 'whoosh' }`.
## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| ghost | drawGhost() in anim.html | (x, y) | as is |
| synth in film | `anim.html` → `tone` | | as is |
## Adapting
None.
## Boundaries
- **Poor fit:** dense data; use `retro-terminal` instead.
## Technical notes
None.
