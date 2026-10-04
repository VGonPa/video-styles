# Kinetic Typography (`kinetic-typography`)

A short line of copy performed word by word on warm paper: the words are the only actors. They drop, squash, stretch,
stack and swing on the beat, then lock up into a typeset phrase closed by a red full stop. It comes from
motion-graphics quote and title animation; the mood is playful, sure of itself and editorial.

**Reference film:** "Start before you're ready.": "Start" drops in and stretches, three words stack and swing into a column, a thin "ready" types itself in and doubts itself with a "?", "Start" shoves it off and the phrase rebuilds into a lockup with a red full stop, then crushes out · `styles/kinetic-typography/`

## Signature
- **S1 Only words on paper:** near-black words on cream paper with static grain and a warm vignette; no images,
  icons, rules or boxes. The one shape that is not a letter is the red full stop at the end.
- **S2 Contrast inside one phrase:** a heavy Bricolage Grotesque 800 hero word at 300 px, Instrument Serif italic for
  the soft connector, Bricolage 460 for the rest, later a thin 240 word: each word has its own voice.
- **S3 Words are bodies:** the hero drops in stretched tall, squashes on landing, stretches like rubber (38 % wider)
  and nods as the others arrive; every arrival overshoots (`backOut()`) and rings (`ring()`).
- **S4 One word per beat:** words land on a 120 bpm grid (0.5 s), each on a kick or a wooden knock.
- **S5 The phrase moves as a group:** by 2.95 s the stack swings 90° into a vertical column. Below about 6.5 s the
  swing is the first style beat to go; the lockup rise is then the only group move.

## Palette
| Role | Colour | In code |
|---|---|---|
| Paper, before grain and vignette | `#ebe5d7` | `PAPER_TONE` (unused), `buildPaper()` base |
| Ink: every word (doubting letters at 0.9 alpha, the "?" at 0.55) | `#15130f` | `INK` |
| The full stop, the only accent | `#d8402f` | `RED`, `redDot()` |
| Vignette, 0 to 0.16 alpha towards the corners | 60, 45, 25 | `buildPaper()` |

- Flat ink; colour never changes. Red appears once, as punctuation, at the very end.

## Typography and copy
- **Fonts.** Bricolage Grotesque (`GRO`; `fonts/BricolageGrotesque-normal-200-800-latin.woff2`,
  `fonts/BricolageGrotesque-normal-200-800-latin-ext.woff2`) is variable: any weight from 200 to 800 draws, so weight
  can animate. Instrument Serif (`SER`; `fonts/InstrumentSerif-italic-400-latin.woff2`,
  `fonts/InstrumentSerif-italic-400-latin-ext.woff2`) is italic 400 only.
- **Presets** in `F`, set by `setType()` and measured by `textWidth()`: `F.start` hero, 800, 300 px, letter-spacing
  −12 px; `F.before` serif italic 170 px; `F.youre` 460, 180 px, −5 px; `F.thin` 240, 250 px, −2 px. The lockup line
  sits at 165 px (`layout()` scales the serif by 165/170, the others by 165/180), its last word bold 800 at −6 px; the
  hero is scaled 1.12 there. Positions come from measured widths, so new copy reflows.
- **Glyphs** (woff2 cmaps): Latin and Latin Extended; no Vietnamese, Greek or Cyrillic; the serif lacks ± ½ ¼ ¾.
  Add letters beyond U+00FF (ğ ş ł ę ő ř…) to `needs` in `boot()`: until the latin-ext file loads, `layout()` measures
  them in a fallback face (fits and lockup slightly off). á é ñ ü are in the main file.
- **Copy:** one sentence of up to four words, one slot each, each slot a voice: the hero (loudest, 7 letters or
  fewer), a soft connector, a medium word, and a last word, the doubting word, that arrives thin (letter by letter
  when there is a doubt beat) and turns bold in the lockup before the red full stop. Any part of speech fits (the
  demo's hero is a verb). A longer hero fits below its partners' 170–180 px in 9:16 (9 letters: 161 px; "Publish"
  keeps 214) and loses the loudest voice: give long words the medium or last slot. 9:16 stack rows are not fitted:
  connector ≤ 12 characters, medium ≤ 10. Three words (tested, 16:9, "Ship it anyway."): delete the you're `partner()`
  call and its width and gap in `layout()`, park `T.youre` and `T.you` at 99. Five or more words become two phrases. A
  hero with a descender (g j p q y) sits on the connector's ascenders in the stack and column (tested: "Begin" over
  "before" in 16:9): set `SLOT.start` to −225 and keep `T.stack` ≤ `T.before` − 0.2.
- **Reading time:** the demo brings one new word per 0.5 s beat. A new word needs about 0.4 s before the next new
  one, or the finished phrase must then hold at least 0.35 s a word (the lockup can assemble at 0.2–0.25 s a word).
  The doubting word types over about 1 s at uneven gaps (0.12, 0.12, 0.43, 0.30 s): doubt is told by rhythm.
- **Characters per line**, from `measureText` on lowercase sentences, spaces counted (capitals run about 20 % wider):

| Preset and size | em per character | 16:9, 1680 px | 9:16, 820 px centred on 540 |
|---|---|---|---|
| serif italic 170 | 0.35–0.37 | 26 | 12 |
| medium 460 at 180 | 0.40–0.42 | 22 | 10 |
| bold 800 at 180 | 0.42–0.44 | 21 | 10 |
| thin 240 at 250 | 0.41–0.43 | 15 | 7 |
| lockup row, mixed, 165 | 0.39 ("before you're ready." is 1294 px) | about 25, then the fit | about 10–13 by letters, then the fit |

- **Fits.** The hero must survive the stretch (1.39× wide), the column (0.72 × its width, standing up) and, in 16:9,
  the push row: fit it to 760 px in 16:9 and 640 px in 9:16 (`Start` is 620 at 300 px), the doubting word to 600 px.
  Lockup rows get a factor too (9:16 below; 16:9 tested with "Experiment without anyone's permission."); under
  about 0.6 (a 9:16 row of about 1,370 px, roughly 19 characters) split the copy. HERO and DOUBT are your strings:
```js
const fitSize = (str, spec, maxW) => Math.min(spec.size, spec.size * maxW / textWidth(str, spec));
// first lines of layout(): F.start.size = fitSize(HERO, F.start, 760); F.start.ls = -0.04 * F.start.size;
//                          F.thin.size = fitSize(DOUBT, F.thin, 600);
// 16:9 layout(), after total: const kr = Math.min(1, 1680 / total); let cursor = W / 2 - total * kr / 2;
//   place(): x: cursor + w * kr / 2, s: s * kr, cursor += w * kr; the gaps and the 12 times kr;
//   dot y: row + 165 * 0.35 * kr - dotR - 1
```

## Texture and finish
- `buildPaper()` runs once in `boot()` into `PAPER`, an `OffscreenCanvas` the size of the frame: the paper tone plus
  seeded noise of ±4.5 levels (`stream(20)`, blue at 0.9 of it), then a radial vignette from radius 300 to 1150.
  `frame()` draws it first every frame (a full repaint); it never refreshes: no flicker, weave or light leaks.
- Ink is flat: no shadow, outline, blur, glow or motion trail. Alpha moves only in the first third or so of an
  entrance (`unit()` of 2.5–4 × progress) and in the exit.

## Shapes, line and figures
- Type is the only drawing. Each word is one call of `word(str, o, p)`: preset o, pose p = { x, y, r, s, sx, sy, a,
  col, base }, pivoting on the word's visual centre (baseline 0.35 × size below y), so turns and squashes happen
  around the middle of the word; `inGroup(g, lx, ly)` places a word inside a moving group pose. Character is weight
  plus behaviour: bold is sure (fast, shoves), thin unsure (trembles, leans away, shrinks 5 %), the serif is soft.
- A new "object" is a word or punctuation mark from the two fonts, given a body: the "?" (serif italic, tilted 12°,
  wobbling ±8°), the full stop (`redDot()`, an `arc()` of radius 21), a digit, an ampersand. No icons or arrows.

## Composition and camera
- No camera: the frame never pans, zooms or shakes; only words move, one focus at a time, on mostly bare paper.
  16:9: the stack at (960, 560) with rows `SLOT` −205, 10, 205; the column at (330, 540), turned −90° at 0.72
  (`stackGroup()`); the doubting word centred on `READY_X0` 1190, baseline 560; `PUSH` (470, 540, 0.84); `CENTER`
  (960, 540, 1.05); lockup: hero at (960, 420), line at y 700 with 46 px gaps (ink x 318–1607, y 298–790). Keep
  `CENTER.y` = `PUSH.y` in every format, and in 9:16 and 1:1 `CENTER.x` = `PUSH.x` too; otherwise the hero jumps at
  `T.up` (16:9) or waits on the middle row while the connector swings through it (9:16, 1:1).
- 9:16 (1080 × 1920; every shot rendered). The push row needs the hero, its run-up and a 574 px doubting word side by
  side, which 1080 px cannot hold, so the film turns vertical: stack in the middle, column on top, the doubting word
  below it, the hero dropping onto it from above, the lockup in three rows, each fitted to 820 px:
```js
// canvas width="1080" height="1920"; W = 1080, H = 1920
// stackGroup(): x: 540, y: mix(860, 600, cubicInOut(p))  (r and s unchanged)   colGroup(): g.y -= q * 950 (flies up)
// startSolo(): const y = mix(-260, 860, fall * fall); x: 540; slot y: mix(y, 860 + SLOT.start, u)
const PUSH = { x: 540, y: 790, s: 0.84 }, CENTER = { x: 540, y: 790, s: 1.05 };  // the hero recoils up and waits there
let LOCK, READY_X0 = 540, READY_Y0 = 1250, READY_W = 700, READY_TOP = 168, PUSH_HALF = 88;
const contactY = () => READY_Y0 - READY_TOP - 8 - PUSH_HALF;               // replaces contactX
// startFree(), pull-back and dash: P.y += -70 * back * (1 - dash) + dash * (contactY() - PUSH.y);  swap sx and sy
// startFree(), after the hit: P.y = mix(contactY(), CENTER.y, backOut(c, 1.6)) replaces the statement
//   P.x = mix(contactX(), CENTER.x, backOut(c, 1.6)); keep P.s = mix(PUSH.s, CENTER.s, cubicOut(c)); swap sx, sy
// readyWord(): cy = READY_Y0; the shove: edge = S.y + PUSH_HALF * S.s / PUSH.s;
//   cy = Math.max(cy + 1500 * cubicIn(p) + 420 * p, edge + 8 + READY_TOP); rot += 38 * cubicIn(p) * DEG; cx += 90 * p;
// redDot(): shrink towards (W / 2, H / 2) instead of (960, 540)
function layout() {
  F.start.size = fitSize(HERO, F.start, 640); F.start.ls = -0.04 * F.start.size; F.thin.size = fitSize(DOUBT, F.thin, 600);   // Fits; 640 in 9:16 and 1:1
  const kB = 165 / 170, kG = 165 / 180, gap = 46, dotR = 21, boldReady = { ...F.youre, w: 800, ls: -6 };
  const wB = textWidth('before', F.before) * kB, wY = textWidth("you're", F.youre) * kG, wR = textWidth('ready', boldReady) * kG;
  const kr = Math.min(1, 820 / (wB + gap + wY)), kd = Math.min(1, 820 / (wR + 12 + 2 * dotR));   // fit each row
  LOCK = { start: { x: W / 2, y: 700, s: 1.12 } };
  let x = W / 2 - (wB + gap + wY) * kr / 2;
  LOCK.before = { x: x + wB * kr / 2, y: 960, s: kB * kr }; x += (wB + gap) * kr;
  LOCK.youre = { x: x + wY * kr / 2, y: 960, s: kG * kr };
  x = W / 2 - (wR + 12 + 2 * dotR) * kd / 2;
  LOCK.ready = { x: x + wR * kd / 2, y: 1160, s: kG * kd };
  LOCK.dot = { x: x + (wR + 12) * kd + dotR, y: 1160 + 165 * 0.35 * kd - dotR - 1, r: dotR };
  READY_W = textWidth('ready', F.thin);
  READY_TOP = (setType(F.thin), g2d.measureText('ready').actualBoundingBoxAscent);
  PUSH_HALF = 0.35 * F.start.size * PUSH.s;      // the hero's baseline below its pivot
}
```
- 9:16 measured (S1–S5 whole from 1.0 to 2.95 s): ink within x 107–985 (past 950 only at the stretch peak and the
  "?"), y 366–1330 until the shove; lockups x 128–950 with the demo, stand-in, long English, Spanish and Polish copy.
  The paper below y 1330 is bare by design, as above and below the 16:9 lockup: grain and vignette are the ground.
- 1:1 (1080 × 1080; the 9:16 code with 860 → 540 in `stackGroup()` and in `startSolo()`'s landing and slot, the
  column at y 330 scaled 0.6 (`stackGroup()` 600 → 330, 0.72 → 0.6), `PUSH.y` and `CENTER.y` 420, READY_Y0 860, lockup
  rows at 380, 640 and 840). Ink within x 107–982, y 136–930 until "ready" leaves.

## Motion
- Easing: `backOut(k, pull)` for every arrival, pull 1.25–3 (light elements pull harder: the "?" 2, the dot 3);
  `quintOut` for long slides, `cubicInOut` for group moves, `cubicIn` for anything leaving.
- Springs: `ring(t, t0, hz, damp)` at 2.5–3.2 Hz, damping 6–9 (the column's itch 7 Hz), added to sx and sy with
  opposite signs. `ring()` alone never reaches zero (the demo is strictly still only from 8.4 s): cut each spring
  after two cycles, at a zero crossing (tested: no jump; the dot settles at `T.dot` + 0.6, its 1.3 px bounce kept):
```js
  const dt = t - t0;
  if (dt >= 2 / hz) return 0;   // the added line in ring()
```
- Words move whole. Only the doubting word goes letter by letter: each letter rises 70 px with `backOut()` 1.1, then
  all tremble (sines of 17 and 29.3 rad/s, up to ±4.5° and ±5 px) while the word sways (1.7 Hz, ±3.2°) and leans away.
- The exit crushes words left to right 0.09 s apart, 0.36 s each (`exitMod()`); the lockup arrives on half-beats; the
  last word ramps its weight 300 → 800 over 0.4 s. Never: scale-pop entrances for words (they drop, rise, swing or
  slide in), fades as the main entrance, typewriter lines, camera moves, colour changes.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.4 | Bare paper; "Start" falls from above, stretched tall, and lands mid-frame on the first kick | `T.land`, `startSolo()` |
| 0.4–1.3 | Squash ring; rubber stretch 0.9–1.12 | `T.stretch` |
| 1.3–2.2 | Start rises to the top row; "before" (serif) and "you're" rise in under it, Start nods | `T.stack`, `T.before`, `T.youre`, `partner()` |
| 2.4–2.95 | The stack swings −90° into a column on the left, shrinking to 0.72 | `T.rot0`, `T.rot1`, `stackGroup()` |
| 3.11–4.46 | The doubting word "ready" types in letter by letter with ticks; the beat stops | `T.rd`, `readyWord()` |
| 4.1–5.1 | It trembles; "?" at 4.45, it leans back; Start itches (4.62); the column drops out | `T.wob0`, `T.q`, `T.itch`, `T.colOut`, `colGroup()` |
| 5.0–5.65 | Start breaks loose upright, pulls back, dashes and shoves "ready" off right | `T.free0`, `T.free1`, `T.hit`, `startFree()` |
| 5.65–6.53 | The beat returns; Start slides to centre, then rises into the lockup | `T.settle`, `T.up`, `LOCK` |
| 6.31–7.75 | "before" swings in from the left, "you're" from below, bold "ready" from the right; the dot pops 7.35 | `T.bef`, `T.you`, `T.ready`, `T.dot`, `redDot()` |
| 7.75–8.6 | Lockup held; strictly still only from 8.4 s (0.2 s): the dot's tail and the "ready" spring still change pixels | |
| 8.6–9.45 | Crush exit left to right; the dot shrinks to centre and fades; bare paper 9.45–9.5 | `T.out`, `T.end`, `exitMod()` |

- Reusable: the drop-and-stretch entrance, stacking a word per beat, the group swing, the doubt beat and the shove
  (for a phrase with a turn), the lockup on half-beats, the red full stop, the crush exit. The words are plot.
- Ending fix (tested): the two-cycle `ring()` cut, `T.stack` 1.25, `T.out` 8.85, `T.end` 9.7, the tink at `T.out` +
  0.45, audio.py `DUR` 10.0 and `fo` 0.3 s, build.sh `DUR=10`: held 8.0–8.85 s. Also change `word()`'s `translate(0, py)` to `translate(0, py * s)`, or a word
  whose s is not 1 jumps 0.35 × size × (1 − s) as the exit starts (Start: 12.6 px).
- Review keys: KEYS=1.0,2.6,4.6,5.62,8.3,9.15 with the ending fix (stretch peak, swing, doubt, contact, lockup, crush).

## Sound
audio.py reads `events.json` (`{t, k, v, d}`) into wooden percussion on a 120 bpm pulse, 48 kHz stereo, `DUR` 9.5.
- `beat` (`v` 0–11): a kick, a shaker 0.25 s later and a bass note from a 12-note line (MIDI 43–52) picked by `v`.
  `knock`: a 330 Hz wood block plus a kick (landing, hit, the last word's lockup). `wood` (`v` 0–2): blocks at 620,
  740, 880 Hz panned −0.3, 0.3, 0 (stack and lockup arrivals). `stretch`: a rubbery pitch bend, 0.45 s.
- `tick` (`v`): a click at 1500 + 180 × `v` Hz, one per letter. `tremble` (`v` mod 3): faint clicks. `soft`: an E5
  tone under the "?". `rattle`: five clicks 45 ms apart (the itch). `whoosh` (`d`): swept noise lasting `d`. `swish`:
  a 0.5 s whoosh (the exit). `pop`: the dot. `tink`: A4, E5, A5 chimes, 1.2 s, the closing sound.
- Fixed in audio.py: room tone; the lockup chord (A3 C4 E4 A4, 2.2 s) at 7.15, the demo's `T.ready` (move it with
  your lockup); the shaker 0.25 s after each `beat`, half the demo's beat (0.2 s on a 0.4 s grid); a 0.1 s fade-in
  and a 0.6 s fade-out (`fi`, `fo`). Fixed in anim.html: the beats list in
  `window.events` (0.4–2.9 and 5.65–8.15 s) and the tremble loop (9 cues from `T.wob0` + 0.12, every 0.16 s):
  re-time both, ending the trembles before `T.hit`. Every other cue follows `T`.
- The demo buries its `tink` (emitted at `T.out` + 0.8, it peaks at 0.003). Emit it at `T.out` + 0.45, as the dot
  starts to shrink, and keep `DUR` = `T.out` + 1.15 with `fo` 0.3 s: peak 0.117, 67 % of the chime heard.
- No cue is looked up by name; unknown kinds and cues outside 0 to `DUR` drop silently. Breaks (tested): `beat` `v`
  ≥ 12 or `wood` `v` ≥ 3 (IndexError), a fractional `v` on either (TypeError), a `whoosh` without `d` (KeyError) or
  under one sample (ValueError). Pans are constants within ±0.5 (no NaN); any `DUR` works; past 12 beats use `v % 12`.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Paper | `anim.html` → `buildPaper` | built once in `boot()` into `PAPER`; drawn first in `frame()` | as is |
| Type presets | `F`, `setType()`, `textWidth()` | fam, w (weight), size, ls (letter-spacing px), it (italic) | as is; fit hero and doubting word |
| Word drawer | `anim.html` → `word` | `word(str, o, p)`: preset, pose { x, y, r, s, sx, sy, a, col, base } | adapt: `translate(0, py * s)` |
| Easing and springs | `backOut()`, `ring()`, `quintOut`, `cubicIn`, `cubicOut`, `cubicInOut`, `span()`, `mix()` | `backOut(k, pull)`; `ring(t, t0, hz, damp)` decaying sine from t0 | adapt: two-cycle cut in `ring()` |
| Group poses | `inGroup()`, `mixPose()`, `stackGroup()`, `colGroup()` | `inGroup(g, lx, ly)`: offset inside a pose { x, y, r, s } | as is; poses per format |
| Hero choreography | `startSolo()`, `startFree()`, `startWord()` | drop, stretch, stack slot; break loose, push, rise | adapt (9:16: vertical shove) |
| Partner words | `partner()` | `partner(t, key, str, o, tIn, lock, tBack, ex, idx)`: stack entry at tIn, lockup swing at tBack | as is; new strings |
| Doubting word | `readyWord()`, `RD` | one `T.rd` time per letter; thin, then bold from `T.ready` | adapt: new word, letter times |
| Exit | `exitMod()` | `exitMod(P, ex, i)`: crush onto the baseline, i × 0.09 s stagger | as is |
| Full stop | `redDot()` | pops at `T.dot`, shrinks to centre after `T.out` | as is; centre per format |
| Lockup | `layout()`, `LOCK` | measured widths into poses, once in `boot()` | adapt: row fits, rows per format |
| Timeline and cues | `T`, `window.events` | | replace; tink at `T.out` + 0.45 |

## Adapting
- **Style vs demo plot:** always the style: paper, ink, the red full stop, the type cast, words as bodies, a word per
  beat, the group swing (dropped only below 6.5 s), the lockup and crush exit, the wooden percussion. Plot: the phrase
  and its meaning. The doubt beat and the shove serve a phrase with a turn (one word hesitates and is overruled);
  without one, go from the swing to the lockup (the 6.5 s plan). The demo's "ready?" is plot. Any regrouping is a
  transformation: the swing, a shove, thin turning bold, the rebuild.
- **New subject (stand-in rendered in 16:9 and 9:16: "Publish before it's perfect."; long copy as in Fits):** replace
  the strings in `startWord()`, `frame()`, `RD`, `readyWord()` and `layout()`, and add letters beyond U+00FF to
  `needs`. What follows the copy: the fits and one `T.rd` time per letter (with five, "perfect" showed only
  "perfe"). The "?" and `contactX` follow measured widths; `SLOT`, `PUSH` and `CENTER` stayed.
- **Length:** up to about 12 s, stretch the doubt and the hold (11.75 s plan below); a doubt (first letter to
  shove) past about 4 s or a still lockup past about 1.5 s goes dead. Past 12 s, one project per phrase (8 s or
  6.5 s plan), joined with ffmpeg's concat demuxer. Untested as MP4: frames match at the join (bare paper) and the
  joined audio passes check_audio, with a 0.35 s near-silent breath and the bass line restarting.
- **Shorter:**
  - Opening: no visual fade-in; the hero lands at 0.3–0.4 s, S1–S4 read by 1.4 s (1.15 s on a 0.4 s grid), S5 by
    2.95 s (2.45 s).
  - Ending cost: after the dot lands, 0.6 s to settle (with the `ring()` cut), 0.8 s held, 0.85 s exit. The lockup,
    the title card, costs at least 2.2 s from the hero's rise to the exit, plus the exit.
  - Cutting order: first the doubt and the shove (optional; the 6.5 s plan keeps S1–S5), then below 6.5 s the stack
    and the swing (the 4 s plan drops S5); never the landing, the lockup or the exit.
  - Re-time `T` only (move durations stay, nothing drifts on film time) and park dropped beats at 99. Keep
    `T.settle` + 0.1 ≤ `T.up`; `T.bef` and `T.you` at least 0.66 s after `T.colOut` (else a partner vanishes);
    `T.free0` ≥ `T.colOut` + 0.22 and, with the short-plan `startWord()`, `T.up` ≥ `T.colOut` + 0.25 (sooner, the hero
    leaves the column through its partners); `T.stack` ≤ `T.before` − 0.15 (the demo's 0.1 s hides the top of the rising connector under the hero for
    two frames).
  - Every plan rendered in 16:9, 9:16 and 1:1 with no shared ink between words in any frame; holds are
    frames identical to the page with `T.out` and `T.end` moved 90 s later (99 and 99.85); each passed events.mjs,
    audio.py and `python3 <skill>/scripts/check_audio.py audio.wav 8` (6.5, 4.25, 11.75):
```
all: ring() two-cycle cut; word() pivot fix; tink at T.out + 0.45; audio.py fo = int(0.3 * SR), lockup chord at T.ready
  (was 7.15), DUR = T.out + 1.15, shaker at te + 0.2 on the 0.4 s grid (8, 6.5, 4 s); build.sh DUR the same
8 s, every scene, opening on a 0.4 s grid:
  T = { land: 0.35, stretch: 0.75, stack: 1.0, before: 1.15, youre: 1.55, rot0: 1.95, rot1: 2.45,
  rd: [2.55, 2.65, 2.75, 2.95, 3.1], wob0: 3.05, q: 3.35, itch: 3.5, colOut: 3.53, free0: 3.75, free1: 4.05, hit: 4.25,
  settle: 4.5, up: 4.65, bef: 4.85, you: 5.05, ready: 5.25, dot: 5.45, out: 6.85, end: 7.7 }
  beats [0.35, 0.75, 1.15, 1.55, 1.95, 2.35, 4.25, 4.65, 5.05, 5.45, 5.85, 6.25]; 7 trembles; rot0 whoosh d 0.5
  DUR 8.0 (peak 0.684); held 24 frames, 6.067 to the first exit frame 6.867: the minimum (no later T.dot, no earlier T.out)
6.5 s, all of S1-S5, no doubt or shove; startWord below:
  T = { land: 0.35, stretch: 0.75, stack: 1.0, before: 1.15, youre: 1.55, rot0: 1.95, rot1: 2.45, rd: [99, 99, 99, 99, 99],
  wob0: 99, q: 99, itch: 99, colOut: 2.6, free0: 99, free1: 99.4, hit: 99.6, settle: 99.8, up: 2.85, bef: 3.35,
  you: 3.55, ready: 3.75, dot: 3.95, out: 5.35, end: 6.2 }
  beats every 0.4 s from 0.35 to 4.75 (12); rot0 whoosh d 0.5; DUR 6.5 (peak 0.685); held 24 frames, 4.567-5.367: the minimum
4 s, drops S5 and the stack (landing, stretch, lockup); startWord below; delete the two stack wood cues (T.before, T.youre):
  T = { land: 0.3, stretch: 0.6, stack: 99, before: 0.86, youre: 1.06, rot0: 99, rot1: 99.5, rd: [99, 99, 99, 99, 99],
  wob0: 99, q: 99, itch: 99, colOut: 99, free0: 99, free1: 99.4, hit: 99.6, settle: 99.8, up: 0.75, bef: 1.1,
  you: 1.3, ready: 1.5, dot: 1.7, out: 3.1, end: 3.95 }
  (before and youre sit 0.24 s ahead of bef and you, so partner() skips the stack; up 0.75 lifts the hero clear of "before")
  beats [0.3, 0.7, 1.1, 1.5, 1.9, 2.3, 2.7]; DUR 4.25 (peak 0.688); held 2.30-3.1 (0.83 s)
11.75 s, longer doubt and hold: T = { land: 0.4, stretch: 0.9, stack: 1.25, before: 1.4, youre: 1.9, rot0: 2.4,
  rot1: 2.95, rd: [3.15, 3.35, 3.55, 4.25, 4.75], wob0: 4.7, q: 5.6, itch: 6.12, colOut: 6.28, free0: 6.5, free1: 6.92,
  hit: 7.15, settle: 7.5, up: 7.65, bef: 8.15, you: 8.4, ready: 8.65, dot: 8.9, out: 10.6, end: 11.45 }
  beats [0.4, 0.9, 1.4, 1.9, 2.4, 2.9, 7.15, 7.65, 8.15, 8.65, 9.15, 9.65]; 14 trembles; DUR 11.75 (peak 0.693); held 9.5-10.6
function startWord(t, ex) {   // 6.5 s and 4 s plans: the hero goes from the column (or its landing) into the lockup
  const A = t < T.rot0 ? startSolo(t) : inGroup(stackGroup(t), 0, SLOT.start);
  const P = { ...A, ...mixPose(A, { ...LOCK.start, r: 0 }, backOut(span(t, T.up, T.up + 0.38), 1.3)) };
  exitMod(P, ex, 0); word('Start', F.start, P);
}
```
- **Other formats:** poses as in Composition (vertical shove, three lockup rows); timing, cues and ending fix as 16:9.

## Boundaries
- **Distinct from:** `bold-captions` puts 1–3 uppercase Montserrat Black words with outlines and coloured highlights
  over a presenter, popping in place; here the phrase is the whole picture, in contrasting families on paper, and
  words travel, collide and regroup. `swiss-style` snaps type to a grid poster and holds still; `split-flap` flips
  characters in place; `glitch` corrupts a slammed title; `title-sequence` sets credits among cut-paper bars;
  `stencil-street`, `constructivism`, `chat-story` and `terminal` put text in an image or an interface.
- **Poor fit:** anything that needs pictures (`kurzgesagt`, `editorial-illustration`), steps or many words
  (`whiteboard`, `infographic`), numbers (`data-visualization`), captions over footage (`bold-captions`), product
  screens (`product-ui`).
- **Do not:** add images, icons, lines, boxes or a second accent colour; use the red for anything but the one full
  stop; move the camera; blur, glow or shadow; type whole lines letter by letter; put more than four words in a phrase.

## Technical notes
- No render.json, vendored library or GPU: canvas 2D with the fonts in fonts/ through fonts.css. `DUR` in anim.html
  is unused (the timeline ends at `T.end`; build.sh's and audio.py's `DUR` set the length). Sizes hard-coded outside
  `W`/`H`: the canvas tag, the pose numbers the 9:16 block changes, and 700 and 420 in `layout()`.
- Deterministic: `stream()` seeds the grain (20) and the tremble-cue jitter (7), audio.py's `default_rng(20)` runs in
  cue order; the determinism test passes on the demo, the 9:16 version and the stand-in. `layout()` runs once in
  `boot()` and sets `LOCK`, `READY_W` and `PUSH_HALF`: set any fitted size before it.
- `readyWord()` letters, the "?" and `redDot()` assign `globalAlpha` instead of multiplying it: a scene fade done
  with `globalAlpha` would not reach them.
