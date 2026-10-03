# Medieval Tapestry (`bayeux-tapestry`)

A long embroidered linen frieze in the manner of the Bayeux Tapestry: laid-and-couched wool in eight dyed
colours, stem-stitch outlines, Latin-style captions and a border of beasts. The strip unrolls from a roller and
pans past. Earnest, naive, chronicle-like.

**Reference film:** a lord prepares to sail, crosses the sea and feasts · `styles/bayeux-tapestry/`

## Signature
- Linen ground with visible weave (`bakeLinenTile()`), figures in flat laid wool with dark stem-stitch outlines.
- A caption in stitched capitals across the top band ("HERE LORD EDRIC MAKES READY TO SAIL").
- The strip unrolls from a wooden roller (`roller()`) and the camera pans along it.

## Palette
| Role | Colour | In code |
|---|---|---|
| linen | `#e2d5b8` | `COL.linen` in `js/lib.js` |
| terracotta wool | `#a9563b` | `COL.terra` |
| mustard wool | `#c8993f` | `COL.mustard` |
| sage | `#8a966b` | `COL.sage` |
| dark green | `#3d4a31` | `COL.greenD` |
| outline blue | `#2c3548` | `COL.blueD` |
| knot shadow | `rgba(45,28,12,0.3)` | `knot()` |
| lit and shaded wool | `shade(h, k)` | `shade()` |

- Eight dyed wools only (`COL`); shading is a lighter or darker version of the same wool (`shade(h, k)`), never a new hue.

## Typography and copy
- No fonts: captions are stitched from vector glyphs (`GLY`) by `caption(text, x, y, u, cols, seed)` and drawn by `drawCaption()`.
- Copy: "HERE … AND HERE …" chronicle voice, capitals only, A–Z and a few signs; about 34 characters per caption.

## Texture and finish
- Laid wool: `bakeWool()` tile blended with `'overlay'` inside each shape (`laid(c, poly, col, ang)`).
- Couching lines across the laid wool every few pixels.

## Shapes, line and figures
- People are built by `human(c, x, y, o)` from `leg()`, `arm()`, `head()`; horses by `horse()`.
- Profiles, almond eyes, no perspective; ground line at `GY`.

## Composition and camera
- A 5400 × 840 strip (`SW`, `SH`) with top and bottom border bands (`MAIN0`, `MAIN1`); the camera pans `CAM0` → `CAM1`.
- 9:16: show a taller slice and scroll vertically through stacked registers.

## Motion
- Limbs move in a stepped, puppet-like way (`walkPose(ph, amp)`); figures do not squash.
- The pan is slow and even; captions stitch in.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0.15–1.75 | the strip unrolls | `T.unroll`, `{ k: 'unroll', d }` |
| 0.7–2.35 | first caption | `T.cap1`, `CAP1` |
| 5.4–8.0 | the feast is served | `T.serve`, `diners(c, t)` |
| 8.3–9.5 | roll up | `T.rollup`, `{ k: 'thunk' }` |

## Sound
- Cues: `unroll` (d), `rollup` (d), `thunk`, plus the scene's own.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| wool fill | `js/lib.js` → `laid()` | `laid(c, poly, col, ang = 90, o)` | as is |
| outlined piece | `js/lib.js` → `piece()` | `piece(c, poly, col, ang, ol = COL.blueD, w)` | as is |
| stem stitch | `stem()` | `stem(c, pts, col, w = 4.4, u, L)` | as is |
| people | `js/figures.js` → `human()` | `human(c, x, y, { s, upper, hose })` | as is |
| captions | `caption()`, `drawCaption()`, `GLY` | | as is |
| strip and timeline | `js/scene.js` → `bakeStrip()`, `T`, `frame(t)` | | replace |

## Adapting
- **New subject:** keep the wool kit and figures; compose new scenes on the strip.
- **Length:** a longer strip (`SW`) and a slower pan.
- **Other formats:** see Composition.

## Boundaries
- **Distinct from:** `illuminated-manuscript` (gold and vellum), `greek-pottery`.
- **Poor fit:** modern products; use `editorial-illustration`.
- **Do not:** reproduce real tapestry scenes.

## Technical notes
- Canvas 2D; code in `js/lib.js`, `js/figures.js`, `js/scene.js`; `anim.html` only loads them.
- No `fonts/`.
