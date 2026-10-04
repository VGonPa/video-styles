# Absurd Webcomic (`absurd-webcomic`)

A loud, flat-colour webcomic gag: chunky characters with thick dark outlines, deadpan first-person captions,
and one tiny annoyance that escalates into a cosmic overreaction before snapping back to fake calm. It draws
on the long-form humour webcomics of the 2010s: the joke is in the gap between the caption's composure and
the picture's hysteria.

**Reference film:** "How I feel when the Wi-Fi drops for one second": a goat sipping coffee loses Wi-Fi,
screams so loudly it is audible from orbit, and ends in a wrecked room insisting "I'm a very calm person." ·
`styles/absurd-webcomic/`

## Signature
- A white caption box with a hard offset shadow in the top-left, in heavy rounded capitals, popping in
  with overshoot within the first half second (`captionBox()`, `T.title`).
- Saturated flat colour with no gradients on the characters: a mustard wall with darker stripes (`C.wall`,
  `C.wallD`), a cream goat in a green sweater, every shape outlined 7 px in near-black (`OL`, `INK`).
- An iris opening from black onto the character's face (`iris(t, cam)`).
- A calm, self-satisfied character (closed ^ ^ eyes, steaming mug) set up for the reversal.

## Palette
| Role | Colour | In code |
|---|---|---|
| outline ink | `#1a1320` | `INK` |
| wall | `#ffd447` | `C.wall` |
| wall stripes | `#f2b92c` | `C.wallD` |
| rage background | `#ff3b2f` | `C.red` |
| rage rays | `#ff8c1a` | `C.ray` |
| goat | `#fbf5e8` | `C.goat` |
| goat shade | `#eadfca` | `C.goatS` |
| sweater | `#3dbb63` | `C.sweater` |
| iris (eyes) | `#ffc81f` | `C.iris` |
| inside of the mouth | `#6b0f22` | `C.mouth` |
| mug | `#ff5d8f` | `C.mug` |
| desk | `#e0873e` | `C.desk` |
| space | `#1b1747` | `C.space` |
| earth, land | `#2f8cff`, `#43d17a` | `C.earth`, `C.land` |
| narwhal | `#8aa9ff` | `C.narw` |
| caption yellow | `#fff6a8` | `captionBox()` |
| scream letters | `#ffe23d`, `#fff27a` | `screamText(t)` |
| iris black | `#120d18` | `iris(t, cam)` |

- Flat fills inside thick outlines: `fs(fill, lw = OL, stroke = INK)` fills and strokes every closed path.
  Shading, where it exists, is one flat darker tone (`C.goatS`, `C.sweaterD`), never a gradient.
- Gradients appear only in backgrounds the character looks at: the window sky and the laptop video.
- The rage beat swaps the whole room for `C.red` with rotating `C.ray` wedges, the comic shorthand for
  "losing it".

## Typography and copy
- Two faces: `'Titan One'` (`FT`, `fonts/TitanOne-400-latin.woff2`) for the title card and the giant
  scream; `'Gochi Hand'` (`FH`, `fonts/GochiHand-400-latin.woff2`) for captions and speech bubbles.
- Caption boxes: `captionBox(txt, x, y, p, rot, size, maxW, bg = '#fff', font = FH)` wraps with
  `wrapText(txt, font, maxW)`, adds a 10–12 px hard shadow in `INK`, tilts by `rot` (about ±0.02 rad) and
  pops with `eOutBack`. Sizes 50–60 px.
- Speech bubbles: `bubble(txt, x, y, p, tail, size = 62)` is an ellipse with a wedge tail pointing at the
  speaker. It does not wrap: keep a bubble under about 25 characters at 60–70 px, or split it into two
  bubbles.
- The scream is `SCREAM` ("NOOOOOO!") at 190 px, laid out letter by letter from widths measured in
  `window.ready` (`SCW`), each letter outlined 26 px, jittering and arced; the letters later fall off one by
  one.
- Voice: first-person, deadpan, past tense, with a timestamp ("7:02 AM. Coffee. Birdsong. Inner peace.",
  "Then the Wi-Fi dropped. For one second."). The title is a "How I feel when…" premise in capitals; the
  punchline is a calm lie ("I'm a very calm person."). Parenthetical asides land the absurd scale
  ("(Audible from orbit.)").
- Copy per beat: one caption of 4–9 words. A 900 px caption holds about 40 characters per line at 50 px;
  the 1800 px title holds about 48 capitals at 50 px. Longer copy becomes another caption beat.
- Latin-1 glyphs only (`-latin.woff2` subsets).

## Texture and finish
- None: clean digital flat colour, no paper, grain or halftone. The finish is the outline weight.
- Motion lines and shock rings do the work of texture: the speed ring of yellow strokes in `drawRays(t)`,
  the expanding shockwaves around the planet in `drawSpace(t)`.
- `impactFlash(t)` gives a two-frame white then yellow-burst flash at the smash.

## Shapes, line and figures
- Uniform 7 px outlines (`OL`); limbs are constant-width outlined tubes (`tube(pts, w, col, lw = OL)`), horns
  and tusks tapered polygons along a cubic (`taper(p0, p1, p2, p3, w0, w1, n)`), which also returns a point
  function for decorating along them.
- Characters are big-headed, round and rubbery: the goat's head is 390 px tall on a small body; eyes are
  huge ellipses with yellow irises and a horizontal goat pupil; expression comes from parameters, not new
  drawings: `bulge`, `brow`, `open`, `pupil`, `rage`, `lidL`, `lidR` in `goatAt(t)`.
- Overreaction kit on the face: bloodshot bulging eyes, a mouth that opens to fill the frame (`mouth(g)`
  with teeth, tongue and uvula), steam from the ears (`steamPuffs(g)`), an anger mark (`veins(g)`), sweat,
  and in the aftermath singed fur (`frazzle(g)`) and a smoking horn (`smoke(x, y, g)`).
- Props are simple rounded rectangles and ellipses (`rrect()`, `ell()`), outlined the same way.
- A new character: round silhouette, oversized head and eyes, flat fills, the same `OL` outline, and a face
  driven by the same parameters.

## Composition and camera
- One continuous camera in room coordinates: `KEYS` lists time, x, y, zoom and an easing; `camAt(t)`
  interpolates zoom in log space so pushes feel even.
- The room is 1920 × 1080 with the goat right of centre (`GX`, `GY`), the laptop left (`LAP`), the window
  top right (`WIN`); captions sit top-left, bubbles near the speaker.
- The big move zooms out of the room into a tiny house window on a planet (`HW`, scale `S`): `render(t)`
  draws the room inside the house window when the view leaves the room.
- Screen shake (`shakeAt(t)`) decays from 26 px after the scream.
- 9:16: put the character in the lower two thirds and captions in the upper third; bubbles need the
  tail recomputed; the zoom-to-planet works unchanged because it is centred.

## Motion
- Pops: every caption and bubble scales in with `eOutBack` (overshoot 2.2) and leaves by scaling to zero.
- Camera moves use `eInOut` and `eSm`; the smash zoom uses `eIn` then `eOut`.
- Jitter is stepped: `jit(t, fps, k)` holds a random offset per frame at 15–30 fps, so trembling reads
  as hand-animated, and it stays deterministic.
- Timing is comic: a long calm hold, a slow push-in, a whip, a held beat (the twitching eye), then the
  smash; the reversal is instant and the calm is held again at the end.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.55 | iris opens on the goat | `iris(t, cam)` |
| 0.35 | title caption pops | `T.title` |
| 0.75 | caption "7:02 AM…" | `T.cap1` |
| 2.2–2.5 | push into the laptop | `T.push`, `T.onScreen` |
| 2.56–2.8 | Wi-Fi bars drop one by one | `T.bar1`, `T.bar2`, `T.bar3`, `T.drop`, `wifi()` |
| 2.95–3.45 | whip to the face, twitch, inhale | `T.whip`, `T.face`, `T.inhale` |
| 3.45 | smash: flash, rays, scream | `T.boom`, `impactFlash(t)`, `screamText(t)` |
| 4.9–5.65 | pull out to the planet | `T.out0`, `T.out1` |
| 5.8–6.3 | narwhal: "It's back." | `T.narw`, `narwhal(t)`, `T.back` |
| 6.4 | scream letters fall | `T.fall` |
| 6.9–7.45 | dive back into the wrecked room | `T.in0`, `T.in1` |
| 7.65–8.85 | "7:03 AM.", calm bubble, sip | `T.cap3`, `T.bub`, `T.sip` |
| 9.2–9.86 | iris closes with a bounce | `T.iris0`, `T.iris3` |

- Structure: setup (calm), trigger, escalation, absurd scale, punchline, deadpan aftermath. Each beat is
  announced by one caption or one bubble.
- Reusable: the iris in and out, caption pops, the smash cut, the zoom to absurd scale, the aftermath with
  props still wrecked. The goat, the Wi-Fi and the narwhal are demo content.

## Sound
- All synthesized in audio.py: `pluck(f, d, dec)` for the calm tune, `tweet()`, `slurp(d)`, `whoosh(d, up)`,
  `blip(f, d)`, `err()`, `plink(f)`, `inhale(d)`, `boom()`, `crash()`, a formant-filtered `scream(d)`,
  `bell(f, d)`, blip `talk(d)`, `woodblock(f)`, `thump()`, `slide(d, f0, f1)` and `pop()`.
- Cues: `iris`, `tweet`, `pop` (`v`, loudness), `sip` (`d`), `whoosh` (`d`), `down` (`v` = 0, 1 or 2, one
  per Wi-Fi bar), `error`, `twitch`, `inhale` (`d`), `boom`, `scream` (`d`), `crash`, `zoomout` (`d`), `ding`,
  `talk` (`d`), `bonk` (`v`, letter index for a falling scale), `zoomin` (`d`), `land`, `irisclose`, `plink`.
- Not cue-driven: the calm plucked `tune(t0, t1, trans, g)` plays at 0.1–2.52 s and 7.55–9.6 s, the
  tape-stop at 2.5 s, and the scream is muffled from 4.9 s by a hard-coded time. Move these with the
  timeline.
- A new film should emit `pop` for every caption, `talk` for every bubble (`d` = reading time), `whoosh`
  for camera moves and `boom` plus `scream` at the smash.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| fill and outline | `anim.html` → `fs()` | `fs(fill, lw = OL, stroke = INK)` | as is |
| shapes | `anim.html` → `ell()` | `ell(x, y, rx, ry, r)`, `rrect(x, y, w, h, r)` | as is |
| outlined tube | `anim.html` → `tube()` | `tube(pts, w, col, lw = OL)` | as is |
| tapered stroke | `anim.html` → `taper()` | `taper(p0, p1, p2, p3, w0, w1, n = 24)` | as is |
| stepped jitter | `anim.html` → `jit` | `jit(t, fps, k)`, seeded by `hash(a, b)` | as is |
| caption box | `anim.html` → `captionBox()` | `captionBox(txt, x, y, p, rot, size, maxW, bg, font)` | as is |
| speech bubble | `anim.html` → `bubble()` | `bubble(txt, x, y, p, tail, size = 62)` | as is |
| scream letters | `anim.html` → `screamText()` | `SCREAM`, `SCW` | adapt: new shout |
| smash | `anim.html` → `drawRays()` | `impactFlash(t)` | as is |
| iris | `anim.html` → `iris()` | `iris(t, cam)` | as is |
| camera | `anim.html` → `camAt()` | `KEYS` rows [t, x, y, zoom, easing], `shakeAt(t)` | adapt: new keys |
| goat | `anim.html` → `drawGoat()` | `drawGoat(g)` with the pose from `goatAt(t)` | replace or adapt |
| room, space, narwhal | `drawRoom()`, `drawSpace()`, `narwhal()` | | replace |
| timeline and copy | `anim.html` → `T`, `render()` | | replace |
| cues | `anim.html` → `window.events` | | replace |
| sound kit | `audio.py` → `whoosh()` | `boom()`, `scream(d)`, `talk(d)`, `pop()` | as is |

## Adapting
- **New subject:** find the tiny annoyance, the absurd escalation and the calm lie. Keep the caption voice,
  the smash and the aftermath; replace the goat with an original character built the same way.
- **Length:** each extra escalation step costs about 1.5 s (caption, reaction, sound). Past 20 s stack
  two escalations before the smash rather than a longer calm opening; one smash per film.
- **Other formats:** see Composition. Captions wrap automatically (`maxW`); bubbles and the scream do not,
  so shorten them for 9:16.

## Boundaries
- **Distinct from:** `relatable-webcomic` (gentle, pastel, no explosions), `stick-webcomic` (stick
  figures), `single-panel-absurd` (one still panel, no camera).
- **Poor fit:** serious or sensitive topics, and data; use `editorial-illustration` or `infographic`.
- **Do not:** copy The Oatmeal's characters, its lettering or its recurring jokes; invent the character and
  the gag. Never mock real people or brands.

## Technical notes
- Canvas 2D only, no `render.json`; renders 10 s in about a minute.
- All randomness is seeded: `rng(seed)` for stars and cracks, `hash(a, b)` for jitter keyed to
  `Math.floor(t * fps)`.
- `ctx.roundRect()` is used for every rounded rectangle; it needs a current Chromium.
- Hard-coded sizes: `W`, `H`, `GX`, `GY`, `LAP`, `WIN`, `HW`, the camera centre 960, 540 in `render()`,
  `toScreen()` and `KEYS`, and the scream baseline at 960.
- `eOutElastic` is defined but unused.
