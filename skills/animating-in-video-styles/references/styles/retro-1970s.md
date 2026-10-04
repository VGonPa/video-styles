# 1970s Retro (`retro-1970s`)

A 1970s TV title sequence on a warm-up CRT: earth-tone sets under a sunburst, a stripe ribbon, chunky shadowed serif
titles and cartoon props bouncing on a funk beat. Broadcast, not film. Cheerful, homely, groovy.

**Reference film:** titles for an invented TV cooking show: four vegetables drop onto a counter, bounce on the beat
and hop into a striped enamel pot under "SUNDAY KITCHEN"; a crash zoom into the soup, a stripe-ring iris, and a lemon
cake lands under "Tonight: Lemon Cake" · `styles/retro-1970s/`

## Signature
- A CRT picture: it opens from a bright horizontal line (0–0.55 s, `switchOn()`), then stays inside a rounded dark
  bezel with vignette, 3 px RGB fringes, scanlines, coarse moving grain and a warm cast (`compose()`).
- Cream ground with a slowly turning sunburst of 14 tan wedges (`C.cream2`, darker than the cream; paler on scene 2's
  mustard) centred on the subject (`rays()`).
- The four-colour stripe motif (mustard, orange, rust, dark brown: `STRIPES`) as a ribbon that runs in along the
  counter and turns up the left side round a 250 px corner (0.55–1.92 s, `rainbow()`); the same bands wrap the pot.
- Round props with even 6–7 px brown outlines and flat fills, landing with squash and bouncing on a 0.5 s beat
  (from 1.0 s, `vegPose()`); a channel bug pops in top right at 0.8–1.2 s (`ident()`).
- From 1.45 s a heavy cream serif title pops in letter by letter, each letter rising, rocking upright and
  overshooting, with three offset shadow copies in orange, rust and brown (`poppedTitle()`).

## Palette
| Role | Colour | In code |
|---|---|---|
| Ground, title faces, highlights, mushroom stem, frosting | `#F3E3C3` | `C.cream` |
| Sunburst wedges, cake plate | `#E9D2A8` | `C.cream2` |
| Outlines, title strokes, the bug's frame | `#3A2216` | `C.brown` |
| Dark stripe, nearest title shadow, pot inner wall, mushroom cap | `#6E3B1F` | `C.brown2` |
| Rust stripe, soup, second shadow, schedule line, kicker shadow | `#C2501F` | `C.rust` |
| Orange stripe, pot body, carrot, farthest shadow, bubbles | `#E8862B` | `C.orange` |
| Mustard stripe, scene 2 ground, onion, sponge | `#EDB53A` | `C.mustard` |
| Leaves; tomato; lemon slices | `#7D7B2E`; `#D4452A`; `#F7D55C` | `C.olive`, `C.tomato`, `C.lemon` |
| Steam core; ground shadows; side shade | `#FFF6E6`; `rgba(58,34,22,0.3)`; `rgba(58,34,22,0.18)` | `steam()`, `potBack()`, `potFront()` |
| Warm cast (soft-light over everything) | `rgba(200,120,50,0.25)` | `compose()` |
| Flicker wash, refreshed at 15 fps | `rgba(255,235,200,${0.025 + 0.02 * rand()})` | `compose()` |
| Scanline rows; vignette edge; bezel | `rgba(40,20,10,0.16)`; `rgba(20,8,0,0.62)`; `#0b0604` | `scanlines()`, `tubeMask()` |
| Switch-on surround and glow; closing fade | `#060302`, `#fff4e0`; `rgba(11,6,4,${dark})` | `switchOn()`, `compose()` |

- Flat fills from `C`, outlined in `C.brown`; light and shade are a translucent cream highlight and a brown side
  band. No gradients on objects, no teal, blue or neon. The faded look is the finish, not desaturation.

## Typography and copy
- `fonts/` (Latin and Latin Extended each, `fonts.css`): Fraunces 900 for titles and the bug's numeral, Shrikhand for
  the "Tonight:" kicker, Monoton (inline capitals) for the schedule line, Fredoka 700 for the bug's label.
- `poppedTitle(x, text, cx, baseY, size, spec)`, centred: each glyph is drawn as orange, rust and brown2 copies offset
  down-right by 3, 2 and 1 × `depth` (each also stroked at 0.11 × size, which fattens it), then a brown stroke and a
  cream fill. `spec.at(i)` is letter i's progress, from `stagger(t, t0, step, dur)` (demo 0.07 s apart, 0.5 s each):
  it rises 0.45 × size (`eOut3`), turns upright from ±0.25 rad (alternating), scales by `eBack(k, 2.0)` (13 %
  overshoot) and fades in over its first third. SUNDAY 135 px, depth 7, track 8; KITCHEN 185 px, depth 9, track 10.
- `lensTitle(x, text, cx, baseY, size, k)`: three outline ghosts (brown2, rust, orange) shrink from 2–2.65× onto the
  line while the solid title lands with `eBack(main, 1.5)`; settled at about 0.97 of `k` (the orange ghost fades until
  `k` = 1). The kicker (inline in `cakeScene()`): Shrikhand 96 px, a rust copy 7 px down-right, 12 px brown stroke,
  cream face, dropping in with `eBack(drop, 1.6)`. Schedule line: Monoton 46 px, rust, tracking closing 34 → 12 px.
- Ink widths, shadows included: SUNDAY 643 px (107 a capital at 135 px), KITCHEN 976 px (140 at 185 px), "Lemon Cake"
  1105 px at 190 px (110 a character; 1150 by the end of the push-in), the schedule line 800 px for 19 characters:
  16:9 holds about 10 capitals a line at 185 px; the 9:16 stack holds 7 at the KITCHEN size (220) and about 10 at the
  SUNDAY size (160) inside the right 12 % band (8 at 160 spans x 224–870, tested). Longer copy takes a second line or
  a smaller size.
- Copy is a TV listing: a show name of one or two words in capitals, one word a line; a schedule line in capitals; a
  mixed-case kicker ("Tonight:") and an episode title in title case. Invent the channel and show.
- Glyphs: Latin and Latin Extended; no Greek or Cyrillic (Fraunces falls back to a system serif, tested). Add every
  new string to `sample` in `prepare()`: a Latin Extended letter missing there draws in a fallback face on a page's
  first frame (tested with Ş and Ğ).

## Texture and finish
`compose(t)` paints the scene into `sx`, then builds the picture on `ctx`:
- `trackingSlip()`: inside the `SLIPS` windows (0.62 s for 0.1 s, `S2` + 0.02 for 0.12, 7.9 for 0.08) three bands,
  20–110 px tall, slide up to ±35 px, reseeded every frame: TV interference, not gate weave.
- `misregister()`: R, G and B (`SPLIT`, `planes`) added back with red 3 px left, blue 3 px right and 1 px down (9 px
  during a slip). Then `SCAN` multiplied (a 4 px period, two rows darkened, built once by `scanlines()`).
- Grain: six 960 × 540 noise tiles (`noiseTile()`, `GRAIN`) drawn at 3960 × 2280, so about 4 px a grain, overlay at
  0.2; tile and offset change at 15 fps, and the same random draw sets the flicker wash.
- The warm cast and flicker; `switchOn()` before 0.6 s; `TUBE` (`tubeMask()`: radial vignette, the bezel outside an
  inset rounded rectangle of radius 70, a faint top glare); the closing fade. Nothing else: no gate weave, dust,
  scratches, splices, halation or film burn: that is film, not broadcast.

## Shapes, line and figures
- `outline(x, w)`: `C.brown`, round joins and caps; 6 px by default, 7 for pot and cake bodies, 5 for leaves and
  lemons, 4 for inner lines, 3 for splash drops. Every object is a closed, curvy silhouette (ellipses, quadratic and
  bezier curves) in one fill; details are brown strokes or cream dots; leaves come from `leaf()` (olive).
- Props have their origin at the bottom centre and stand on `GROUND` over a soft shadow ellipse (`vegShadow()`).
  Demo sizes: tomato 140 × 120, carrot 80 × 190, mushroom 168 wide, onion 140 × 178, pot 450 (582 with handles) × 170,
  cake 500 × 260. Containers get the stripe bands clipped inside them (`potFront()`), a cream highlight bar and a
  60 px brown side shade.
- Small kit: `twinkle()` (four-point star, 5 px brown stroke, cream); for soup, `steam()` (wavy strokes, brown2 under
  a cream core), `splash()` (droplets) and the bubbles in `potBack()`.
- A new object belongs when it is rounded and chunky, 120–200 px tall at 16:9 scale, outlined at 6–7 px, filled from
  `C`, over a floor shadow, and moves with squash and stretch; small props stop at detail strokes or cream dots and at
  most one cream highlight (the tomato), large bodies add a 60–70 px brown side band (pot, cake). No people in the
  demo, and none tested: tell the story with props.

## Composition and camera
- 16:9 kitchen: `POT` centred at x 1020, rim 740, `GROUND` 910; vegetables at x 520, 680 and 1370, 1540; the title
  centred at x 1040 (baselines 200, 378; schedule line 446); the bug at (1700, 132); the sunburst on the pot (1020,
  760). The ribbon (`BEND` x 470, y 735, r 250; `LANES` ±23, ±69: 47 px stripes 46 px apart) enters from x 2060 along
  y 892–1078, under the props' feet, and rises (lane centres x 151–289) out of the top. Scene 2, centred on x 960:
  `CAKE` top 640, bottom 900, stand to 1004 on a four-stripe tablecloth from y 948; kicker y 150, title baseline 420;
  twinkles in the corners. Keep what must be read 40 px inside the bezel.
- Camera: `kitchenCamera()` is a zoom lens on the pot: a pull-back from 1.75× (0.25–1.5 s, `eOut3`) and a crash zoom
  of about 42× (`ZOOM_IN` to `S2` + 0.2, `eIn3`) that recentres the soup at (`W`/2, 0.55 `H`). Scene 2 pushes in from
  1 to 1.05 (`eInOut`, `S2` to `DUR`). No pans, cuts or shake.
- 9:16 and 1:1 recompose as a stack (bug, title, props on the counter, ground); the kitchen is drawn through one
  extra scale so its world coordinates stay those of 16:9. Every value was rendered (1:1 after `//`):

```js
canvas width="1080" height="1920"; W = 1080, H = 1920          // 1080 x 1080
const STAGE = { s: 0.65, x: -103, y: 878.5 };                  // y 308.5: pot at screen x 560, GROUND at 1470 / 900
// kitchenCamera(): zoom = STAGE.s * settle * Math.exp(3.75 * eIn3(crash)); const rx = STAGE.s * fx + STAGE.x,
//   ry = STAGE.s * fy + STAGE.y; return [zoom, lerp(rx, W / 2, centre) - fx * zoom, lerp(ry, 0.55 * H, centre) - fy * zoom];
BEND.x 528; lanePath() lineTo(BEND.x - r, -1500), laneLength's + 160 -> + 1500     // -700, + 700
VEG x 505, 666, 1412, 1643 (screen 225, 330, 815, 965); vegPose() drop from land - 0.5, GROUND - 2600 * (1 - u * u)   // 1600
poppedTitle SUNDAY (989, -182, 160), KITCHEN (989, 41, 220); Monoton 50px at (989, 125)   // y -82, 133; 218
kitchen twinkles [520, -420, 40], [1497, -367, 34], [760, 390, 30]   // [466, -182, 40], [1635, 249, 34], [543, 387, 30]
ident() cx 790, cy 350: clear of the top 15 % and right 12 % bands, so not in the corner   // 905, 100
CAKE { x: 540, top: 1150, bot: 1410, rx: 250 }; cake() lerp(-1700, ...), lemons - 1300 * (1 - u * u)   // top 640, bot 900; -900, 700
cakeScene(): push centre (540, 1150), rays (540, 1150, ...)  // (540, 600), (540, 640)
tablecloth: 14 stripes [C.cream, C.orange, C.rust, C.brown2][i % 4] at y 1458 + 36 * i   // the 4 of 16:9
kicker translate(540, lerp(-100, 560, ...)); lensTitle(x, 'Lemon Cake', 540, 830, 128, ...)   // 215; (540, 430, 140)
cake twinkles [130, 700, 36], [960, 690, 30], [900, 960, 22], [170, 980, 24]   // [100, 470, 36], [980, 590, 30], [860, 250, 22], [150, 760, 24]
iris(): R0 = lerp(0, 1600, u)                                 // 1500
tubeMask(): radii 0.35 * Math.min(W, H), 1.05 * Math.min(W, H); grain drawImage(tile, gx, gy, 3960, 2280)   // same
```
- Both take fixes F1–F4 (Adapting); F3 is needed: in the stack the falling lemons cross the kicker. 9:16 lands
  (scene 2 at 8.5 s): bug x 650–930, y 290–410; SUNDAY KITCHEN x 176–920, y 680–933; schedule line to y 968; kicker
  x 310–784, y 472–586; "Lemon Cake" x 155–954 (the last 27 px are shadow), y 706–853. Once titles are up, bare
  sunburst stays under 18 % of the rows in 9:16 (below the ribbon; above the bug in scene 2) and under 6 % in 1:1.
  While the set fills it reaches 62 % in 9:16 and 57 % in 1:1 (0.5–0.8 s, against 44 % in 16:9), and 36–40 % in scene
  2 before its titles (5.3–6.3 s): accepted because the rays lead to the pot; keep a new opening as short. The iris
  needs 1600 to cover the 9:16 corners; with `W` and `H` swapped the grain stretches into vertical streaks and the
  vignette misses the sides, hence the last line.
- Stand-in (9:16): a tall stockpot (`POT` rim 520, rx 150) and a cake 460 tall (`CAKE` top 950, rx 190).
  Subject-dependent: the hop's arc (`vegPose()`'s 215, about 0.75 × (`GROUND` − rim) + 90; at 215 the props clipped
  through the stockpot's wall, 430 cleared it), the episode title's baseline (190 px or more above the subject: kicker
  520, title 760), the twinkles (off the title and the hop arcs), the camera focus (`kitchenCamera()`'s 800: the
  subject's middle), the lemons' spread (inside `CAKE` rx).

## Motion
- Easing: `eOut3` for arrivals (switch-on, pull-back, letter rise, schedule line), `eIn3` for the crash zoom,
  `eInOut` for the ribbon, iris, push-in and fades, `eBack(k, s)` for every pop (letters 2.0, bug 2.2, twinkles 1.9,
  kicker 1.6, lens title 1.5). Drops fall with gravity. Smooth 30 fps; only the grain steps (15 fps).
- Bounce (`vegPose()`): a 120 px parabola per `BEAT` (0.5 s, the music's beat), squash 16 % at each contact plus 14 %
  on the first landing, 7 % stretch at the top, a small rock. Hop: a 0.45 s arc (`JUMP_D`), shrinking to 0.72 and
  turning 1.6 rad, behind the pot's front from halfway, a splash at 55 %. Heavy landings ring with a damped spring
  (cake 14 %, lemons 18 %).
- Ambient, on film time, allowed through the final hold: the sunburst's turn (0.06 and −0.08 rad/s), steam, soup
  bubbles, the twinkles' 12–14 % pulse, the scene 2 push-in, grain, flicker and tracking slips. All else is action.
- Never: held drawings or limited animation, camera shake, hard cuts (sets change by crash zoom and stripe iris), glow
  or neon, 3D, desaturated or monochrome frames.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.6 | The picture opens from a bright line (wide by 0.2, tall 0.18–0.55, glow gone by 0.6); slip 0.62–0.72 | `switchOn()`, `SLIPS` |
| 0.25–1.5 | Zoom-lens pull-back from 1.75× on the steaming pot; sunburst turning throughout | `kitchenCamera()`, `rays()` |
| 0.55–1.92 | The four stripes run in, 0.09 s apart, 1.1 s each | `rainbow()`, `BEND`, `LANES` |
| 0.6–1.75 | Vegetables drop (0.4 s), land at 1.0, 1.25, 1.5, 1.75 and bounce on the beat; the bug pops 0.8–1.2 | `VEG`, `vegPose()`, `ident()` |
| 1.45–2.77 | SUNDAY, then KITCHEN from 1.85, letter by letter | `poppedTitle()`, `stagger` |
| 2.55–3.4 | Schedule line 2.75–3.35; three twinkles pop | `kitchenScene()`, `twinkles()` |
| 3.0–4.45 | One hop every 0.25 s into the pot, splashes; steam bursts at 4.25 | `vegPose()`, `splash()`, `steam()` |
| 4.3–4.82 | Crash zoom into the soup; steam and splashes clear first (4.25–4.42) | `ZOOM_IN`, `kitchenCamera()` |
| 4.57–5.22 | Stripe-ring iris opens from the soup onto scene 2; slip 4.64–4.76 | `iris()`, `S2` |
| 4.95–5.3 | The cake drops onto its stand and wobbles | `cake()`, `CAKE` |
| 5.2–6.5 | Lemon slices land at 5.5, 5.75, 6.0; kicker drops 5.55–6.0; leaf sprig 6.2–6.5 | `lemonSlice()`, `cakeScene()`, `leafSprig()` |
| 6.0–6.73 | "Lemon Cake" arrives through the lens | `lensTitle()` |
| 6.7–7.45 | Four twinkles pop in | `twinkles()` |
| 7.53–9.12 | Hold, 1.59 s measured (slip at 7.9; the push-in continues) | `cakeScene()` |
| 9.12–9.96 | Fade to dark brown | `compose()` |

- A set opens on something already moving, fills by beats on the music's grid (props landing, letters popping),
  plays one action (the hops), and leaves by crash zoom and iris; beats are 0.25–0.5 s, a set about 4.5 s.
- Demo faults (fixes under Adapting): the tomato hops through the carrot (3.07–3.2 s); the third lemon falls behind
  the kicker (5.83–5.87); the twinkle at (1560, 330) touches KITCHEN's N. Soup bubbles balloon into large rings in the
  crash zoom (left as is: it reads as a close-up of the soup). Fast falls and the crash zoom pass under the bug for 1–5
  frames: it is a broadcast overlay on top of everything; never rest text or props under it.
- `KEYS=0.3,2.9,3.6,4.5,4.9,6.4,8.5`: switch-on, the kitchen card, hops, crash zoom, iris, lens title, end card.

## Sound
audio.py reads events.json (cues with a time `t`, kind `k` and value `v`), synthesizes 48 kHz stereo, `DUR` 10.0, and
passes the mix through a TV-speaker band-pass (150–7000 Hz) and tanh.
- Music, written at fixed times: a funk groove at `BPM` 120 from 0.5 s (kick, hats, `BASSLINE`, clav `STABS`, bars
  alternating F and B flat), faded in 0.4–0.7 s, ducked by a Gaussian around 4.55 s (the crash zoom); the master
  fades on `(9.98 - tm) / 0.86`. The demo's landings and bounces sit on this grid. A new length re-times 9.98 and 0.86,
  the duck's 4.55 (one per crash zoom, or none), 0.4 and the groove's 0.5.
- Cue kinds (`v` defaults to 0): `on` (set switching on), `ident` (two blips, right), `land` (boing, pitch 220 +
  140 v; v 0–1 pan left, 2 and up right), `bounce` (blip, 300 + 60 v), `hop` (rising sweep), `plop` (falling tone and
  noise), `pop` (letter, 520 + 45 v, pan (v − 5) / 8), `whoosh` (0.55 s rising noise into a crash zoom), `iris` (saw
  sweep), `thump` (heavy landing), `ding` (bell, v 0, 1, 2 = E, G, B), `chime` (four-note arpeggio, 1.8 s, the title).
- The film's cue list derives `land`, `bounce` (one per beat), `hop` and `plop` from its prop rows; the `pop` times
  are literals there: re-time them with the title. No cue is looked up by name, so audio.py plays any subset.
- What breaks it (tested): `pop` with v outside −3…13 pushes the pan past ±1; the band-pass spreads the NaN over that
  whole channel, silent for the entire film while audio.py prints "ok" (check_audio.py fails it). `ding` takes v 0, 1
  or 2 only: 3 and up or −4 and below raise IndexError, −2 or −3 silence the right channel. Unknown kinds and cues
  before 0 or past `DUR` drop silently. Any `DUR` works (6.3333 tested), but past 10 the fixed fade leaves silence
  after 9.98 s (check_audio.py only prints a note) and below it the track ends without a fade.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Maths, easing, random | `anim.html` → `seg`, `anim.html` → `rng` | `seg(t, t0, t1)`, `lerp`, `clamp`, `eOut3`, `eIn3`, `eInOut`, `eBack(k, s)`, `rng(seed)` | as is |
| Palette and stripes | `anim.html` → `C`, `anim.html` → `STRIPES` | colour names as in Palette | as is |
| CRT finish | `compose()`, `misregister()`, `trackingSlip()`, `switchOn()`, `tubeMask()`, `scanlines()`, `noiseTile()` | built in `prepare()`; `SLIPS` rows [start, length] | as is; slips, fade and sizes per film |
| Sunburst | `anim.html` → `rays` | `rays(x, cx, cy, spin, alpha)`: 14 wedges reaching 2400 px | as is |
| Stripe ribbon | `rainbow()`, `lanePath()`, `laneLength`, `BEND`, `LANES` | `rainbow(x, t, start)` | adapt the path per set |
| Titles | `poppedTitle()`, `stagger`, `lensTitle()` | `poppedTitle(x, text, cx, baseY, size, { at, depth, track })`; `lensTitle(x, text, cx, baseY, size, k)` | as is |
| Bug | `anim.html` → `ident` | `ident(x, t)`: centre, label and numeral inside | adapt: own name and number |
| Prop kit and twinkles | `outline()`, `leaf()`, `vegShadow()`, `drawVeg()`, `steam()`, `splash()`, `twinkles()` | `drawVeg(x, v, P)` draws `v.f` at pose P; `twinkles(x, t, [[x, y, r, t0]...], wobble, rate)` | as is, plus the `steam()` line in Technical notes; soup pieces only for soup |
| Bounce and hop | `vegPose()`, `VEG`, `BEAT`, `JUMP_D`, `GROUND` | rows `{ f, x, land, jump, tilt }`; jump − land must be whole `BEAT`s or the prop snaps to the floor | adapt |
| Zoom lens and iris | `kitchenCamera()`, `iris()`, `ZOOM_IN`, `S2`, `paintScene()` | | adapt focus and times |
| Demo subjects | `tomato()`, `carrot()`, `mushroom()`, `onion()`, `potBack()`, `potFront()`, `POT`, `cake()`, `CAKE`, `lemonSlice()`, `leafSprig()` | | replace |
| Scenes, timeline, cues | `kitchenScene()`, `cakeScene()`, `soundCues()` | | replace |
| Sounds | `audio.py` | cue kinds in Sound | as is; music times and `DUR` |

## Adapting
- **Style vs demo plot:** the style is everything in Signature, plus the zoom-lens moves and the funk groove through a
  TV speaker. Plot: the kitchen, vegetables, pot, cake, lemons and copy. Transformations: props hopping into a
  container, a crash zoom and stripe iris onto a new set, an object dropping onto a stand and being decorated.
- **New subject:** keep the finish, sunburst, ribbon and title kit; write new props (origin bottom centre) and
  `VEG`-style rows. Traps: times are literals in each drawer and again in `soundCues()`; `vegPose()` starts a hop from
  the floor, so jump − land must be whole beats; the hop arc must clear the container's rim (stand-in above); several
  drawers assign `globalAlpha` (Technical notes). The steam, the bubbles in `potBack()`, `splash()` and the `plop` cue
  belong to a pot of soup: drop them for a dry container (tested with a toy drum: the 6 s plan then settles when the
  last prop vanishes, 4.167 s, held 1.38 s). Fixes for the demo's faults, tested:
  - F1, the inner prop hops first: tomato `land` 1.25, `jump` 3.25; carrot 1.0 and 3.0.
  - F2, the KITCHEN twinkle at (1590, 330): keep each twinkle's centre 1.15 r + 3 px from letters and hop arcs.
  - F3, the kicker waits for the lemons: its `seg(t, 5.55, 6.0)` becomes seg(t, 6.0, 6.45), the title's
    `seg(t, 6.0, 6.75)` becomes seg(t, 6.3, 7.05), scene 2 twinkles 0.3 s later, `chime` at 6.3. The film then settles
    at 7.767 (1.35 s held).
  - F4, damped motion tapers to exactly zero: multiply the cake's squash by (1 − seg(land, 0, 1)), the lemons' wobble
    by (1 − seg(l, 0, 0.8)), the steam burst by (1 − seg(t, plopAt + 0.25, plopAt + 0.6)). The steam taper is what
    lets an ending in the kitchen hold: without it the 6 s and 4 s plans hold under 0.6 s.
- **Length:** past 10 s add sets, each entered by crash zoom and iris (about 4.5 s: props land 1.2, title 1.3, an
  action 1.2, the zoom 0.5), or more props on the beat; a bouncing set with no new event tires after about 3 s.
  Untested past 10 s. `iris()` draws `cakeScene()` by name and `paintScene()` has two hard-wired phases: for a third
  set, pass `iris()` the incoming scene's drawer and add a phase per set. In audio.py set `DUR`, one duck per crash
  zoom and the closing fade (14 s tested); the groove loops to `DUR`.
- **Shorter:** from 10 s to about 8 s keep every beat: cut the final hold to 0.9 s and the fade to 0.5 s, then run
  the action clock uniformly faster (up to 1.2×: letters and bounces at 0.42 s still read), with the tempo scaled to
  match so bounces stay on the beat; between 6 and 8 s take the 6 s plan and add bounce cycles (7 s below). Under 6 s
  cut whole scenes: scene 2 first (crash zoom, iris, cake, kicker, lens title), then bounce cycles (one before the
  hop); keep switch-on, ribbon, props, popped title and the hops into the container (the transformation). The
  signature is complete when the title lands: 2.77 s, 2.2 s after the 0.55 s switch-on (4 s plan: at 1.9 s, 1.35 s
  after it). A popped two-line title costs 1.32 s (0.95 at stagger 0.05, 0.4 s a letter); a kicker and lens title
  1.03 s, 1.77 s with twinkles (F3 times); the lens title alone 0.73 s; then 0.8 s of hold. Re-time actions only, with
  ambient motion on a second clock. Tested in 16:9 and 9:16 (4 s also 1:1), holds measured as in Film grammar,
  soundtracks through check_audio.py:

```js
let AMB = 0, ACT = t => t;               // compose(t): AMB = t; paintScene(ACT(t)); ...
// on AMB: rays(.., 0.06 * AMB, ..) and (.., -0.08 * AMB, ..), steam(x, AMB, ..), potBack(x, AMB),
//   the twinkle pulse Math.sin(rate * (AMB - t0)), the push seg(AMB, <scene 2 start>, <film end>)
// 8 s, all beats, F1-F4: ACT = t => 1.2 * t; push seg(AMB, S2 / 1.2, 8); SLIPS [[0.62 / 1.2, 0.1], [(S2 + 0.02) / 1.2, 0.12]];
//   fade seg(t, 7.46, 7.96); cues t / 1.2. audio.py DUR 8.0, BPM 144, groove from 0.5 / 1.2, fade-in 0.4 / 1.2,
//   duck 4.55 / 1.2, master (7.98 - tm) / 0.52. Settled 6.467, held 0.99 s; peak 0.617.
// 6 s, the kitchen alone, F1, F2, F4: ZOOM_IN 99, S2 99.32; fade seg(t, 5.55, 5.96); drop the whoosh, iris, thump,
//   ding and scene 2 chime cues; chime at the last plop + 0.25 (4.25). audio.py DUR 6.0, no duck,
//   master (5.98 - tm) / 0.43. Settled 4.6, held 0.95 s; peak 0.611.
// 7 s (9:16 tested): the 6 s plan with every VEG jump + 0.5 (one more bounce), fade seg(t, 6.55, 6.96);
//   audio.py DUR 7.0, master (6.98 - tm) / 0.43. Settled 5.1, held 1.45 s; peak 0.537.
// 4 s, as 6 s plus: audio.py DUR 4.0; VEG land/jump carrot 0.75/1.25, tomato 0.875/1.375, mushroom 1.0/1.5,
//   onion 1.125/1.625; pull seg(t, 0.2, 1.1); rainbow(x, t, 0.45); stagger(t, 0.95, 0.05, 0.4) and (t, 1.2, 0.05, 0.4);
//   schedule line seg(t, 1.9, 2.3); kitchen twinkles at 1.9, 2.0, 2.1; pops 1.0 + 0.05 n, 1.25 + 0.05 n; fade seg(t, 3.62, 3.96);
//   master (3.98 - tm) / 0.36. Settled 2.5, held 1.12 s; peak 0.517.
```
- **Other formats:** values in Composition and camera. Not carried over: a wider row of props (the 9:16 counter fits
  four at 0.65, no more) and anything entering from the top, which crosses the title band.

## Boundaries
- **Distinct from:** `mid-century` (1950s limited animation: teal among the mustards, dry-brush and crayon fills,
  off-register blocks, angular figures held on twos, no CRT); `synthwave` (also a CRT power-on, scanlines, RGB split,
  grain and tracking glitches, but neon magenta and cyan on dark, chrome type, a perspective grid); `teletext` (8-colour
  character mosaics on a CRT, no drawn props); `weather-tv` (1990s bevelled blue map, gradient icons, clean video);
  `anime-80s` (painted cel sunsets, film flare, 12 fps figures); `documentary-16mm` (black-and-white film with gate
  weave, scratches and splices); `vhs-camcorder` (1990s home video on a VCR).
- **Poor fit:** data and numbers (`data-visualization`), long text (`kinetic-typography`), sombre or serious stories
  (`dark-documentary`), interface walkthroughs (`product-ui`), news urgency (`newspaper`).
- **Do not:** reproduce a real 1970s brand's logo, packaging, product or lettering, a real channel's ident or numeral
  styling, or a real show's titles; invent the channel, show and products, as the demo does.

## Technical notes
- No render.json and no vendor folder: Canvas 2D, no GPU; anim.html, fonts.css and eight woff2 files. 300 frames
  render in about 20 s on one page. Grain, bubbles, splashes and slips come from the seeded `rng()`, audio.py's noise
  from `np.random.default_rng(13)`. But `outline()` leaves stroke colour, width, join and cap set on the scene
  context, and `steam()`, drawn before any outline, inherits `lineJoin`: a kitchen frame drawn first on a page has
  mitred steam and fails the determinism test (50 dB at 4.2 s). In `steam()`, after `x.lineCap = 'round'` add
  x.lineJoin = 'round' (tested: identical at 0.31, 4.2 and 8.5 s). New drawers set every stroke property they use.
- `potBack()` (bubbles), `twinkle()`, `steam()`, `rays()`, `ident()`, `lensTitle()` and the schedule line assign
  `globalAlpha` instead of multiplying it, so a scene faded by `globalAlpha` leaves them opaque; `poppedTitle()` and
  `splash()` multiply. Multiply and restore in new drawers.
- Sizes a 9:16 version must change: the canvas tag; the grain's draw size in `compose()` and `tubeMask()`'s radii,
  which follow `W` and `H` and stretch or shrink when they swap; and literal layout everywhere. The 9:16 block lists
  each one.
