# 8-Bit Console (`nes-8bit`)

A side-scrolling cartridge game of the late 1980s, played back as if captured from a console on a widescreen
TV: a 256 × 240 picture made of 8 × 8 tiles, a fixed 64-colour hardware palette, three-colour sprites and a
four-channel chiptune. Cheerful, punchy and literal; every idea becomes a level, a power-up or a boss.

**Reference film:** "Monday Quest", an office worker runs through Stage 1, dodges emails, drinks coffee,
stomps the boss "THE INBOX" and clears the level into the weekend · `styles/nes-8bit/`

## Signature
- A black title screen whose logo ("MONDAY" / "QUEST") scrolls up into place while the whole palette steps up
  from black in four brightness rows (`FADE`), not a smooth alpha fade.
- Hard square pixels at exactly 4× scale, pillarboxed in black (`SC`, `OX`, `OY`); no anti-aliasing anywhere.
- A blinking "PUSH START" and a legend strip of the game's sprites under the logo.
- The jingle on pulse channels starts at 0.2 s; the picture is silent of any non-palette colour.

## Palette
| Role | Colour | In code |
|---|---|---|
| black (backgrounds, outlines) | `#000000` | `P.k` = `0x0F` |
| white (text, highlights) | `#FCFCFC` | `P.w` = `0x30` |
| office wall cream | `#F0D0B0` | `P.cr` = `0x37` |
| window sky | `#3CBCFC` | `P.sky` = `0x21` |
| hero shirt, boss floor | `#0058F8` | `P.bl` = `0x12` |
| skin | `#FCA044` | `P.sk` = `0x27` |
| wood, flag stripe | `#E45C10` | `P.or` = `0x17` |
| dark wood, coffee | `#881400` | `P.br` = `0x07` |
| red (hearts, boss, badge) | `#F83800` | `P.rd` = `0x16` |
| gold (score pop-ups, flag) | `#F8B800` | `P.gd` = `0x28` |
| plant green | `#00A800` | `P.gn` = `0x1A` |
| light green | `#58D854` | `P.lg` = `0x2A` |
| grey (floor, boss metal) | `#7C7C7C` | `P.gy` = `0x00` |
| light grey | `#BCBCBC` | `P.lgy` = `0x10` |
| light cyan (wainscot, skyline) | `#A4E4FC` | `P.lc` = `0x31` |
| monitor blue | `#0000BC` | `P.db` = `0x02` |

- Every colour is an index into the 64-entry `NESPAL`; `hex(i)` turns an index into its string. Never write a
  hex that is not in `NESPAL`: the fade maps only palette colours and turns anything else black.
- Flat fills only: no gradients, no alpha, no dithering. Sprites use three colours plus transparency.
- The hero's "caffeinated" state cycles through `HPALS`, the console's palette-swap trick.

## Typography and copy
- One face: `'Press Start 2P'` from `fonts/PressStart2P-400-latin.woff2`, loaded in `window.ready` with
  `document.fonts.load('8px "Press Start 2P"')`.
- `textCan(s, ci)` renders a string at 8 px, thresholds the alpha at 110 to hard pixels and tints it with one
  palette index; results are cached in `TX` by string and colour.
- `txt(s, x, y, ci, sc = 1, sh = -1, sho = 1)` draws at integer scale `sc` with an optional one-colour drop
  shadow `sh`; `txtC()` centres on `cx`.
- Upper case only, like the hardware font. At scale 1 a line holds 32 characters (256 / 8); the game uses 22
  ("STAGE 1  THE WORK WEEK"). At scale 2 keep to 14 characters, at scale 3 to 8 ("MONDAY").
- Voice: terse game-speak, HUD labels and shouts: "SCORE", "LIFE", "COFFEE", "CAFFEINATED!", "COMBO x5",
  "LEVEL CLEAR!", "WEEKEND UNLOCKED". Longer copy becomes several screens, never a smaller size.
- Glyphs: Latin-1 only (`©` is used in "© 1989 TINYCART SOFT"); no accents beyond it, no CJK.

## Texture and finish
- None beyond the pixels: no scanlines, no CRT curvature, no grain. The look is the hard 4× upscale with
  `imageSmoothingEnabled = false` on every canvas (`mk(w, h)` sets it).
- The palette fade in `render(t)` reads the virtual screen with `getImageData()`, maps each colour through
  `FADE[fade]` and writes it back; it runs only on fade frames.
- Sprite flicker is a finish too: the hero blinks every other frame while invincible and the email volley
  alternates sprites when more than three share a line.

## Shapes, line and figures
- Everything is axis-aligned `rect()` runs on the 256 × 240 virtual screen `VC`; never `arc()`, strokes or
  rotation. Circles (the wall clock) are two overlapping rectangles.
- Sprites are character grids: `grid(rows, map)` turns rows like `'kwwwwwwk'` and a map from letters to `P`
  colours into a small canvas; `'.'` is transparent. Outlines are one pixel of `P.k`.
- The hero is 18 × 25 and built by `makeHero(pose, pal)` from a skeleton in `POSES`: `fa`, `ba`, `fl`, `bl`
  are three-point arms and legs drawn with a Bresenham `line()`, plus a `HEAD` grid. A head, neck, torso,
  jointed limbs and hands read even at this size.
- Scenery is built from small parametric pieces: `windowPane(x, y)`, `plant(x, y)`, `cooler(x, y)`,
  `wallClock(cx, cy, mins)`, `desk(x0, x1, top, oy, camX)`, `monitor(x, y)`, `floorTiles()`.
- A new object is at most two tiles wide, three colours plus black, with a one-pixel black outline.

## Composition and camera
- The virtual screen is `VW` × `VH` = 256 × 240, drawn at `SC` = 4 into 1024 × 960 and centred with `OX`,
  `OY`; the rest of the frame stays black.
- The top 32 lines are the HUD (`drawHUD(t, room)`): score, lives, coffee count and a clock.
- Play happens on the floor line at y = 208; the camera follows the hero (`camX` clamped to the level width
  `LVLW`) and changes rooms with a full-screen flip scroll, never a cut or a zoom.
- Scene changes between screens slide whole pictures through `BUF_A` and `BUF_B` (title → stage 1).
- 9:16: keep the 4× screen and stack it in the middle (1024 × 960 inside 1080 × 1920), or make the virtual
  screen 256 × 456 and give the extra height to the HUD and a taller level. 1:1 fits the 256 × 240 screen
  with thin bars.

## Motion
- Time is quantised: run cycles step at 12 fps (`F(t * 12) % 3` over `run1`, `run2`, `run3`), sprites
  animate at 4–8 fps, and positions are rounded to whole virtual pixels with `R()`.
- Jumps are parabolas: `jumpY(s, y0, y1, h)`; falls accelerate (`450 * u * u`). No easing curves, no
  overshoot, no squash and stretch.
- Hits use the console idioms: knock-back, a one-second invincibility flicker, screen shake of ±2 px for
  0.3 s when the boss lands.
- Score pop-ups float up 30 px in 0.5 s (`popup(s, x, y, t0, t, ci)`).

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.36 | palette steps up from black | `FADE`, `render(t)` |
| 0.1–0.75 | logo scrolls up into place | `drawTitle(oy, t)` |
| 0.55–1.5 | legend strip, blinking PUSH START | `drawTitle(oy, t)` |
| 1.5–1.95 | vertical scroll from title to stage 1 | `T_SCROLL`, `L0`, `BUF_A`, `BUF_B` |
| 1.95–5.41 | run, jump, collect coffee, dodge emails, get hit | `heroLevelX(t)`, `heroLevelY(t)`, `CUPS`, `LMAIL`, `T_HIT` |
| 5.41–5.91 | flip scroll into the boss room | `T_FLIP`, `T_ROOM` |
| 6.0–6.75 | boss drops, HP bar fills | `bossY(t)`, `T_DROP`, `T_HP` |
| 6.75–7.72 | email volley, power-up, stomp | `BMAIL`, `T_POW`, `J5` |
| 7.95–8.3 | boss explodes | `BOOMS`, `PUFF` |
| 8.3–8.9 | flagpole rises, hero touches it | `drawFlag(x, t, oy)`, `T_POLE`, `T_TOUCH` |
| 8.9–9.45 | LEVEL CLEAR, time-bonus tally | `T_CLEAR`, `T_WKND`, `T_TALLY` |
| 9.5–10 | palette steps down to black | `T_FADE`, `FADE` |

- The film is one play-through: title, a stage, a boss, a clear screen. Each beat is a game event with its
  own sound, and the score in the HUD keeps counting across beats (`score(t)` sums `SCORE_EV`).
- Reusable patterns: title with palette fade, screen scroll, pickup with pop-up, hit with flicker, boss with
  HP bar, clear screen with tally. The office, the emails and THE INBOX are demo content.

## Sound
- audio.py is a small chip emulator: two pulse channels (`pulse(freq, d, duty)`, duty 0.125, 0.25 or 0.5),
  a 16-step triangle bass (`tri(freq, d)`), a 15-bit LFSR noise channel (`noise(rate, d)`) and 4-bit volume
  envelopes (`env(n, a, dec, sus)`). Notes are MIDI numbers converted by `nt(m)`.
- `seqplay(t0, step, notes, ch, g, duty, t_end, gate, dec, sus)` plays a list of notes; a tuple `(m, n)`
  holds a note for `n` steps and `None` is a rest. Drums are `hat()`, `snare()` and `kick()`.
- Music is cued by `music` events with an `s` field: `'title'` (the jingle), `'level'` (the 150 bpm stage
  theme, eighth = 0.2 s) and `'boss'` (A minor, sixteenth = 0.075 s). The first `stop` ends the stage theme,
  the second ends the boss theme, and `fanfare` plays the level-clear fanfare.
- These six music cues are required: audio.py looks each one up with `next()` and raises `StopIteration`
  if one is missing.
- Effects, all with only `k` and `t`: `start`, `jump`, `coin`, `hurt`, `drop`, `thud`, `tick` and `tickd`
  (HP bar up and down, 16 each), `shoot`, `pop`, `power`, `stomp`, `boom`, `rise`, `flag`, `tally`.
- The master is a ~90 Hz DC-blocking high-pass and a 12 kHz low-pass, like the console's output stage, then
  `np.tanh(y * 1.6)` soft clipping; mono, copied to both channels.
- A new scene should emit `jump` for every jump, `coin` for each pickup and `tally` ticks for any counter.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| hardware palette | `anim.html` → `NESPAL` | `hex(i)`; `P` names the 16 used | as is |
| palette fade | `anim.html` → `FADE` | `FADE[1..4]`, applied in `render(t)` | as is |
| canvas helper | `anim.html` → `mk` | `mk(w, h)`: offscreen canvas, smoothing off | as is |
| rectangle | `anim.html` → `rect` | `rect(x, y, w, h, ci)` on the virtual screen | as is |
| grid sprite | `anim.html` → `grid()` | `grid(rows, map)`: letters to palette indices | as is |
| sprite draw | `anim.html` → `spr` | `spr(c, x, y, flip = false)` | as is |
| pixel text | `anim.html` → `txt()` | `txt(s, x, y, ci, sc, sh, sho)`, `txtC(s, cx, y, ci, sc, sh, sho)` | as is |
| hero | `anim.html` → `makeHero()` | `makeHero(pose, pal)` over `POSES` and `HPALS` | adapt: new head grid, new poses |
| explosion | `anim.html` → `puff()` | `PUFF[0..3]` | as is |
| HUD | `anim.html` → `drawHUD()` | `drawHUD(t, room)` | adapt: new labels and counters |
| score pop-up | `anim.html` → `popup()` | `popup(s, x, y, t0, t, ci)` | as is |
| office, boss room, boss | `drawOffice()`, `drawBossRoom()`, `drawBoss()` | | replace |
| timeline | `anim.html` → `T_SCROLL`, `L0`, `T_HIT`, `heroPose()` | | replace |
| cues | `anim.html` → `window.events` | | replace with the new beats |
| chip voices | `audio.py` → `seqplay()` | `seqplay(t0, step, notes, ch, g, …)` | as is |
| themes | `audio.py` | `lead`, `bass`, `chords`, `blead` | adapt: new melodies |

## Adapting
- **New subject:** turn it into a game: the subject is a level, obstacles are enemies, goals are pickups,
  the climax is a boss. Keep the title screen, the palette fade, the HUD and the clear screen.
- **Length:** add stages, each with a scroll in, a short run and one event; past 20 s the stage theme loops
  audibly, so add a second theme or a bridge. Render cost is low (a 256 × 240 picture per frame).
- **Other formats:** 1:1 works with the 4× screen and bars; 9:16 needs a taller virtual screen or a stacked
  layout (see Composition). Never change `SC` to a non-integer: the pixels stop being square.

## Boundaries
- **Distinct from:** `jrpg` (16-bit menus and windows), `voxel` (3D blocks); this style is strictly
  third-generation hardware: 64 colours, 3-colour sprites, chip sound.
- **Poor fit:** dense data or long text; use `infographic` or `terminal`.
- **Do not:** copy real game characters, logos, level layouts or melodies; the publisher on the title
  screen is invented ("TINYCART SOFT").

## Technical notes
- Canvas 2D only, no `render.json`; 10 s render quickly (the virtual screen is small).
- The palette fade costs a `getImageData()` per fade frame only; keep it that way.
- Deterministic: `rng(77)` seeds the explosion bursts, `rng(40 + i)` the boss-room skyline, redrawn each
  frame from the seed. Pickup and burst times are found by stepping time in 1/600 s, not by state.
- Hard-coded sizes: `W`, `H`, `VW`, `VH` and `SC` at the top; levels are laid out in virtual pixels
  (floor at 208, `LVLW` = 448). A 9:16 version changes `W`, `H` and the canvas and recomputes `OX`/`OY`.
- audio.py's `DUR = 10.0` must change with the film; its music is placed by cue times, so it stretches with
  a new timeline.
