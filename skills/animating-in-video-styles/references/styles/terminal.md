# Terminal (`terminal`)

A command-line session on a green-phosphor CRT: a shell prompt, commands typed key by key, logs and ASCII progress
bars streaming line by line, an error, its fix and a success, then an ASCII picture before the tube powers off. It
draws on 1980s video terminals and Unix shells; the mood is deadpan and technical, showing what happens behind the
scenes with a wink.

**Reference film:** an invented coffee machine is deployed from a shell: boot log, `brew deploy --strength=strong`,
four progress bars, "ERROR: milk not found", oat milk added, a retry succeeds, the screen rolls clear into an ASCII
mug that fills with dithered coffee, a caption types, the cursor blinks, the CRT powers off · `styles/terminal/`

## Signature
- **S1 A CRT tube:** black bezel around a round-cornered glass, dark green radial glass, vignette, a faint reflection
  top left, scanlines every 4 px, grain, flicker and a slow rolling band; the picture opens from a bright centre line
  at power-on (0–0.42 s) and is never edge to edge.
- **S2 One phosphor, one monospace grid:** JetBrains Mono 32 px on fixed 19.2 × 52 px cells, in four greens (dim,
  normal, bright bold, inverse), with bloom; no other hue anywhere, errors included.
- **S3 A prompt and a typed command:** an invented user@host:~$ prompt ("dev@kitchen:~$" in the demo) and a block
  cursor; the command appears key by key (about 32 characters a second, pauses after spaces), the cursor steady from
  the first key to Enter, blinking about once a second at a waiting prompt; phosphor trails ghost behind every change.
- **S4 Output as whole lines:** a banner at 0.44 s and `[ OK ]` boot lines from 0.54 s, then ASCII progress bars
  (filled and dithered cells in brackets, a percentage and a | / - \ spinner) from 2.2 s. Text pops in whole; it
  never fades, slides or scales.
- Later signature moves: the error as an inverse flash with a slice glitch, an inverse SUCCESS, the roll-up clear,
  an ASCII picture card, the power-off to a dot.

## Palette
| Role | Colour | In code |
|---|---|---|
| Normal text, filled bar cells, SUCCESS box, cursor | `#8ef7aa` | `C.n` |
| Dim text: prompt path, banner, secondary info, brackets, empty and dithered cells | `#3d9a5b` | `C.d` |
| Bright text (bold 700): typed commands, values, OK, the caption; the error box | `#eafff0` | `C.b` |
| Ink of inverse text (dark text on a lit box) | `#041209` | `C.bg` |
| Glass, centre → 0.6 → edge | `#07170d`, `#041009`, `#010402` | `BG` in `setup()` |
| Power line; rolling band (0.035 alpha); additive washes; after-glow dot; glass reflection (0.045 alpha) | 140,255,170; 120,255,160; 150,255,180; 245,255,248; 210,255,225 | `LINE`, `drawTube()`, `frameAt()`, `DOT`, `VIG` |
| Bezel, vignette (to 0.62), scanlines (0.30 and 0.12) | `#000`, 0,0,0 | `VIG`, `SCAN` |

- Colour is a text style per run: 'n', 'd', 'b', 'i' (inverse) and 'e' (error), set in each line's segments. Hierarchy
  is brightness and weight, never hue: an error is an inverse block, not red. Everything glows through the bloom.

## Typography and copy
- **Font:** JetBrains Mono (`MONO`), 400 for 'n' and 'd', 700 for 'b', 'i' and 'e'
  (`fonts/JetBrainsMono-normal-400-latin.woff2`, `fonts/JetBrainsMono-normal-700-latin.woff2`, `latin-ext` twins).
  `FS` 32, `LH` 52, `CW` 19.2 measured from "M" in `setup()` (overwriting `let CW = 16.8, COLS = 96`); `cell()`
  draws each glyph alone in its cell.
- **Glyphs:** ASCII, Latin-1 (° · » ³ é ñ ü), Latin Extended (ğ ş ł), ↑ ↓ • … – —; box drawing, → ←, ✓ ✗, braille,
  ▶ ■ ● and ▓ fall back to another face. `cell()` paints █ ░ ▒ as rectangles and dither, so bars join. Add latin-ext
  letters to `glyphProbe` in the `window.ready` chain, or early frames may draw them in a fallback face.
- **Voice:** an invented shell, lowercase and terse: a user@host:~$ prompt, long flags, `[ OK ]` lines (`OKL()`),
  "» " for progress, "ERROR:", "hint:", "x … exit 1"; values and units joined by "  ·  ". The joke is played straight.
  Invent the tool and the OS banner (brewOS 3.1 in the demo); Boundaries says what must never be typed.
- **Limits (FS 32), measured with a ruler render:**

| Format | Grid used | Columns | Rows | A typed command after the 15-cell prompt |
|---|---|---|---|---|
| 16:9 | `X0` 140, `Y0` 118 | 85 (the tube shows 90) | 16 (18 fit, the last two in the vignette) | 70 |
| 9:16 | `X0` 72, `Y0` 300 | 45 clear of the right 12 % (48 fit the tube) | 21 (y 300–1392) | 30 |
| 1:1 | `X0` 72, `Y0` 96 | 45 (48 fit) | 17 (an 18th in the bezel shadow) | 30 |

- Nothing wraps: shorten a long line, shorten the prompt ("kim@roof:~$" is 12 cells) or split output with a
  two-space indent. Bar labels up to 13 characters in 16:9, 12 in 9:16 and 1:1 (`barLine()` pads to 14 or 13);
  `[ OK ]` names up to 12 (`OKL()` pads to 13). The caption is one line, typed at 0.016 s a character: up to 85, 43
  and 48 characters (9:16 centres it on all 48 columns, so 44 reach the right 12 %).

## Texture and finish
- Built once in `setup()`: `BG`, `SCAN` (1.5 px at 0.30 and 0.8 px at 0.12 black every 4 px), `VIG` (black outside
  a rect inset 34 × 30 px, radius 90, blurred 18 px; vignette from radius 380 to 1180; reflection at (560, 230)), four
  512 px green grain tiles in `NOISE` (seeded `rng`), `LINE`, `DOT` and the dither patterns `dith` (6 px tiles).
- Per frame, `drawPhosphor()` paints the screen into `TEXT` over three past copies (`TRAILS`: 0.04, 0.08, 0.12 s
  back at 0.30, 0.17, 0.10 alpha), skipped whenever `layout` changes (a scroll or clear would smear lines).
  `drawTube()` lays glass, the rolling band (320 px, period 5.6 s), `TEXT`, blurred downsamples `GLOW_A` (quarter
  size, 0.55) and `GLOW_B` (eighth, 0.45), grain tile `fi % 4` at 0.045 and a 0.03–0.065 black flicker; `frameAt()`
  squashes it for power on/off, adds glitch and flashes, then `SCAN` and `VIG`. Trails add 0.12 s to every change.

## Shapes, line and figures
- Everything is a character in a cell: no lines, vectors, images, people or icons. Bars are `BAR` cells: a dim
  bracket, filled █ cells (a 28 px band at 0.82 alpha, the leading cell bright while filling), dithered ░ cells (dim,
  same band), then the percentage and spinner, ending in "100%" and a bright value (`barLine()`).
- Inverse runs ('i', 'e') get a lit box 4 px wider than the text each side and 10 px shorter than the line.
- The card is pure ASCII line art (in the demo a mug, `CUPART`: . - | / \ ' ~), 9 rows by 35, in 'n' (its ~ row 'd'),
  its newest row bright while it draws. Its ▒ fill (full-cell dither, dim) rises a row at a time; on the label row two
  9-cell runs from `c0` + 3 and `c0` + 20 stop one cell short of STRONG: move them for another label (up to 22 fit).
  The demo's three steam wisps of "(" and ")" step at 8 fps above it.
- A new object belongs when it is ASCII line art on the grid: outline characters only, one cell per character, no
  diagonal smoothing, filled with ▒ runs between its outline's ends, labelled in capitals on a clear row. Its
  height follows from `r0` + rows + 1 < `ROWS` − 1 (the caption above the prompt row): with something above the art
  (`r0` ≥ 3), up to 10 rows in 16:9, 11 in 1:1 and 15 in 9:16; with nothing above (`r0` 0), 13, 14 and 18.

## Composition and camera
- No camera; the picture moves only when squashed for power on/off. Text is top-left in the grid (`X0`, `Y0`), the
  newest line lowest; past `ROWS` lines each new line jumps the screen up a row. Focus: the newest line and cursor.
- The card is centred: columns from `COLS` and `CUPW`, top row `r0` 3 (in the demo, steam rows `r0` − 3 to − 1), the
  caption on row `r0` + 10, the final prompt on row `ROWS` − 1.
- A terminal fills from the top. With the demo's three `[ OK ]` lines the bare glass stays over a fifth of the
  frame until about 4 s in every format (43 % at 1.5 s in 9:16); grain and scanlines are not content. Boot with
  twelve `[ OK ]` lines 0.035 s apart from 0.475 s, a blank at 0.895, P1 0.96: the prompt lands on row 14 and the
  glass is under a fifth from 0.97 s in all formats, but for the clear and card build (7.50–8.20 s; 9:16 7.53–7.97).
  The 4, 5 and 8 s plans stream them 0.015 s apart from 0.46 (blank 0.64, P1 0.70): under a fifth from 0.70 s (ten
  lines leave 24 % in 9:16 until 1.6 s). Never fill the glass with boxes or art. In 9:16 and 1:1 every tested frame
  after the prompt passes (largest empty area 13–21 %). In 16:9 the ragged right leaves 27–48 % of the glass empty
  beside the log and 29 % beside the end card, as in the original. A 16:9 reviewer may flag it.
- 9:16 and 1:1, rendered at every beat; only these lines change, everything else follows `W`/`H`:

```js
// canvas width="1080" height="1920"; W = 1080, H = 1920          // 1:1: height="1080", H = 1080
const X0 = 72, Y0 = 300;  const ROWS = 21;                        // 1:1: X0 = 72, Y0 = 96; ROWS = 17
const BAR = 14;           // and label.padEnd(14) -> label.padEnd(13) in barLine(): bar lines 45 cells
// deploy line: drop ' -> counter-01' (52 -> 38 cells); every other demo line already fits 45
// cup scene in screenAt(): r0 = 4 (9:16); 1:1 keeps r0 = 3
// boot log: twelve OKL() lines (bullet above), each at most 45 cells
```
- 9:16 measured: key text in x 72–936, y 300–1392 (clear of all three bands); card rows y 352–1392, caption row
  1028–1080. S1–S2 whole from 0.44 s, S3 whenever a prompt is last, S4 from 2.1 s (in the card, art and dither).
  Unchanged and right in 9:16: the reflection (top glare), the vignette radii (same half-diagonal), the band (same
  5.6 s crossing, so no faster to the eye). 1:1 end card y 105–975, largest bare band 11.7 % (16:9 10.2 %).

## Motion
- Stepped, not eased: characters, lines and rows appear whole on frame boundaries; no tweened position, scale or
  fade on text. Easing exists only in bar fills (`eOut`), the roll-up and power-off (`eIn`) and the picture opening.
- **Typing:** `typeTimes()` gives each key 0.017 + 0.02 × `hash` s, plus 0.04 s after a space (29 characters in
  0.87 s). The cursor (19.2 × 44 px, `C.n`) is steady from a command's first key to its Enter (0.14 s after the last
  key). Whenever a prompt is the last line otherwise, it blinks on `Math.floor(t * 1.9)`: 0.53 s on, 0.53 s off,
  phase from t = 0 (a pause over 0.3 s inside a command would also make it blink). No cursor while output streams.
  Do not type faster: the demo is already several times human speed, and the keys would merge into a buzz.
- **Output:** whole lines, the first 0.06–0.08 s after Enter, then 0.08–0.12 s apart; bars fill over 0.22–0.42 s
  with 0.04 s gaps, the spinner turning 14 steps a second; the caption types at 0.016 s a character, silently. A
  boot log is a dump and streams faster: 0.035 s a line in the 10 s block, 0.015 s in the 4–8 s plans (two lines a
  frame, under the warm flash), so the prompt lands by P1.
- **Error:** the 'e' run alternates bright text and an inverse bright box every 1/12 s for 0.5 s, then stays inverse;
  `drawGlitch()` shoves up to seven 12–82 px slices of the picture ±60 px, fading over 0.34 s, with a green wash.
- **Clear:** the screen jumps up row by row, accelerating, `ROWS` + 1 rows in 0.22 s (`ROLL` to `CUP`).
- **Power** (`tubeAt()`): on, a centre line (0.1 s) opens into the picture by 0.42 s, a flash fades by 0.7, text
  from 0.40; off at `OFF`, a squash to a line (0.17 s), a dot (`OFF` + 0.19 to + 0.36) fading to `DUR` − 0.15. Keep
  `OFF` ≤ `DUR` − 0.6 (demo − 0.65); past `DUR` − 0.51 the dot stays lit to the last frame.
- Ambient, allowed through holds: the blinking cursor (a loop with no end state: the idle prompt is the settled
  state of a terminal), steam wisps, grain, flicker and the rolling band; they stay on film time. Actions: typing,
  lines, bars and spinner, rows, fill, steam fading in, caption, glitch, and the 0.12 s trail after each.
- Never: smooth scrolling, text fading or sliding, motion blur, camera moves, overshoot, a second colour.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.70 | Power-on: centre line, the picture opens by 0.42, warm flash fades | `tubeAt()` |
| 0.44–0.80 | Boot log: banner, three `[ OK ]` lines, a blank line | `L()`, `OKL()` |
| 0.96–2.03 | Prompt; the command typed 1.02–1.89; Enter 2.03 | `promptLine()`, `CMDS`, `typeTimes()`, `ENT` |
| 2.10–3.65 | Deploy line; four bars, the fourth stalls at 30 % | `STEPS1`, `barLine()` |
| 3.75–4.09 | ERROR flashes inverse, slice glitch; hint 3.87, failure 3.97 | `ERR`, `drawGlitch()` |
| 4.36–6.16 | Fix typed 4.42–5.18 (Enter 5.32, first scroll 5.36, OK line 5.40); retry typed 5.42–6.02, Enter 6.16 | `CMDS`, `E3` |
| 6.22–7.02 | Resume line, two bars | `STEPS2` |
| 7.12–7.42 | Inverse SUCCESS line, prompt 7.22, cursor blinking | `OK` |
| 7.42–8.04 | Roll-up clear to 7.64; the ASCII mug drawn from 7.72, 0.035 s a row | `ROLL`, `CUP`, `CUPART`, `CUP_ROW` |
| 8.00–8.51 | Coffee rises in four steps to 8.44, steam fades in from 8.04, caption 8.06–8.51, prompt 8.26 | `CAPTION`, `PROMPT_END` |
| 8.63–9.35 | Held (0.72 s) | |
| 9.35–10 | Power-off: line 9.52, dot 9.71, fade to 9.85, black | `OFF`, `tubeAt()` |

- No cuts: a new line, a scroll, the clear or the power-off hands over; beats run 0.3–1.2 s; every beat is reusable.
- Ending: the caption's last letter lands at 8.51 and its trail clears at 8.63, so the final state holds 0.72 s,
  short of 0.8. Tested fix (16:9, 9:16, 1:1): `ROLL` = `OK` + 0.25 and `CAPTION` = `CUP` + 0.36: held 8.533–9.35 s.
- KEYS=1.5,2.5,3.8,7.15,7.58,8.8,9.45 (typing with trails, bar filling, error and glitch, full screen and SUCCESS,
  roll-up, end card, power-off squash); with the ending fix, 7.5 for the roll-up and 8.7 for the card.

## Sound
audio.py turns `events.json` (`{t, k}` cues, some with `v` or `d`) into 48 kHz stereo, `DUR` 10.0, with a 0.02 s
fade-in, a 0.3 s fade-out and a tanh limiter; no music:
- `key` (one per keystroke, `v` 0.6–1.0 sets the level; a 6 ms random delay, pan ±0.15), `enter` (a thunk), `tick`
  (one per output line after 0.4 s and per card row: the demo's mug, `CUPART`), `blip` (`v` = step / steps, pitch
  900 + 700 `v` Hz; `round(fill × 10)` per bar), `error` (two square-wave buzzes and a noise burst, 0.66 s), `success`
  (three chimes), `roll` (a 0.22 s whirr), `hiss` (steam, `d` long), `on` (thump at 0.02), `off` (falling whine).
- The bed (`hum` at 60, 120, 180 Hz and `room` noise) ramps in at fixed 0.05–0.45 s (power-on at 0.02) and out
  from `off` − 0.1 to + 0.2; audio.py finds `off` by name. Besides the end fades, every other sound follows cues.
- A new scene gets `key` and `enter` from `window.events` (from `TT` and `ENT`) and a `tick` per non-prompt `LOG` line
  after 0.4 s; emit `blip` per bar step, `error` and `success` at those lines, `roll` at a clear, `on` and `off`.
  `hiss` (`CUP` + 0.3, `d` = `OFF` − `CUP` − 0.3) is the demo mug's steam: send it only for steam, wind or the like.
- Breaks (tested): no `off` (StopIteration); `hiss` without `d` (KeyError) or with `d` under 1/48000 s (ValueError),
  even past `DUR`, so drop it with the card; `DUR` under 0.3 s. Pans are fixed (no NaN), a large `v` only gets
  louder, unknown kinds and cues outside 0–`DUR` are skipped; fractional `DUR` works (7.33 tested).

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Helpers | `anim.html` → `seg` | `seg(t, a, b)`, `clamp`, `lerp`, `eOut`, `eIn`, `hash(n)`, `rng`, `mk(w, h)` | as is |
| Grid and colours | `MONO`, `FS`, `LH`, `X0`, `Y0`, `CW`, `COLS`, `ROWS`, `C` | `CW` and `COLS` measured in `setup()` | as is; per format |
| Typing | `anim.html` → `typeTimes` | `typeTimes(str, t0, seed)`: key times | as is |
| Line log | `LOG`, `L()`, `OKL()`, `promptLine()`, `PROMPT` | `L(t, segs, p)`: a line from t; segs are [text, style] runs or a function of t; p marks a prompt | replace lines; keep time order |
| Commands | `CMDS`, `TT`, `ENT`, `E1`, `E2`, `E3` | [text, start] rows; Enter 0.14 s after the last key | replace; timing block below |
| Progress bars | `barLine()`, `BAR`, `STEPS1`, `STEPS2`, `spin` | `barLine([label, a, b, fill, suf], fail)` | adapt: the fail text is a literal " 30%  stalled"; the demo marks the fourth step as failing |
| Screen builder | `anim.html` → `screenAt` | runs {r, c, s, st} and the cursor, from t | adapt the card scene |
| Cells and CRT finish | `cell()`, `paintText()`, `dith`, `setup()`, `drawPhosphor()`, `TRAILS`, `layout`, `downsample()`, `drawTube()`, `frameAt()` | block glyphs as rects; layers built once, composed per frame | as is |
| Glitch, power on/off | `drawGlitch()`, `tubeAt()` | 0.34 s from `ERR`; `OFF`, `DUR` | as is |
| Picture card | `CUPART`, `CUPW`, `CUP_ROW`, card branch of `screenAt()` | `r0`, fill runs, steam columns `c0` + 9 + 7 w, caption string | replace the art and caption; re-place the fill and steam |
| Timeline and cues | `ERR`, `OK`, `ROLL`, `CUP`, `CAPTION`, `PROMPT_END`, `OFF`, `window.events` | | re-time |
| Sounds | `audio.py` → `add` | `key()`, `enter()`, `tick()`, `beep()`, `square()`, `band()`, `env()` | as is; `DUR` |

## Adapting
- **Style vs demo plot:** style: the tube and finish, the green grid, typed commands with cursor and trails,
  whole-line output, `[ OK ]` lines, bars, error flash and glitch, inverse SUCCESS, the clear into an ASCII card with
  caption and idle prompt, power on/off, the key sounds. Plot: coffee, brewOS, the milk, the mug. Transformations:
  failure to fix to success, a bar completing, the clear into the picture.
- **New subject:** rewrite `PROMPT`, `CMDS`, the `L()` lines (in time order: the log is drawn in push order), the
  steps, `CUPART`, its label and the caption. This block replaces the demo's `CMDS` … `OFF` lines; the prompt lines
  L(0.96, …), L(4.36, …), L(5.36, …) become L(P1, …), L(P2, …), L(P3, …), and `screenAt()` takes const cap = CAP. It
  reproduces the demo from the retry on (the fix types 0.06 s earlier, so the retry prompt follows its output line)
  with the ending fix: HELD 25. Change the copy and the hold changes: trust HELD.

```js
const CMDS = [['brew deploy --strength=strong', 0], ['brew add milk --type=oat', 0], ['brew deploy --retry', 0]];
const TT = [], ENT = [];
function typeCmd(k, t0) {                              // types command k from t0; returns its Enter time
  CMDS[k][1] = t0; TT[k] = typeTimes(CMDS[k][0], t0, k * 11 + 1);
  ENT[k] = TT[k][TT[k].length - 1] + 0.14; return ENT[k];
}
const P1 = 0.96, E1 = typeCmd(0, P1 + 0.06);
const ERR = E1 + 1.72;                                  // after the last STEPS1 bar ends
const P2 = ERR + 0.55, E2 = typeCmd(1, P2 + 0.06);
const P3 = E2 + 0.10, E3 = typeCmd(2, P3 + 0.06);       // after the fix's output line (E2 + 0.08)
const OK = E3 + 0.96;                                   // after the last STEPS2 bar ends
const ROLL = OK + 0.25, CUP = ROLL + 0.22;
const CAPTION = CUP + 0.36, PROMPT_END = CUP + 0.62;
const CAP = 'order #042 is live  ·  enjoy';
const SETTLE = Math.max(CUP + 0.80, CAPTION + 0.016 * CAP.length, PROMPT_END) + 0.12;   // card done, trail included
const OFF = 9.35;                                       // DUR - 0.65; or derive it:
// const OFF = Math.ceil((SETTLE + 0.84) * 30) / 30;    // then DUR = OFF + 0.65, rounded up
const HELD = Math.ceil(OFF * 30) - Math.ceil(SETTLE * 30);   // frames held before the power-off
if (HELD < 24) console.error(`final hold ${HELD} frames: cut copy or gaps, or raise OFF and DUR`);
```
- Replace the demo's STEPS1.forEach line (after `barLine()`) with STEPS1.forEach((s, i) => L(s[1], barLine(s, i ===
  STEPS1.length - 1))); so that the last bar fails. The 8 s plan's three bars need it.
- HELD matched the measured hold in every build. New copy within the limits (commands of 28, 29, 27 characters, a
  41-character caption) gave HELD 10, measured 10, and render.mjs printed the error; with the derived OFF (9.867) and
  `DUR` 10.52 in all three places it held 25 frames and check_audio passed.
- Stand-in (16:9, 9:16): a balloon launch, prompt "kim@roof:~$", 22 lines, a bar failing at 18 % (text from `fill`),
  a 12-row balloon (`CUPW` 21, `r0` 0 and 3) with wind marks for steam, a 31-character caption. Grid, finish and cues
  needed no change; the art, fill rows, label gap, steam loop and caption row did.
- **Length:** add beats (a command and its output, more bars), not holds: a held card tires after about 1.5 s
  (the 14 s plan below holds 1.43 s).
  Typing costs about 0.03 s a character and 0.04 s a space: 45 characters take 1.4 s, a seventh of a 10 s film (9:16
  and 1:1 allow 30 after the prompt). Set `DUR` in anim.html, audio.py and build.sh; audio.py needs nothing else.
- **Shorter:** costs: typing as above, Enter + 0.14; a bar 0.20–0.42 s; error to prompt 0.5–0.6 s; SUCCESS to clear
  0.25 s; SETTLE (`CUP` + 0.93 with the demo caption), 24 frames held, a 0.5 s power-off, `OFF` = `DUR` − 0.65: the
  card costs about 2 s from `ROLL`. The fade-in is the 0.42 s power-on; S1–S2 read at 0.44, S3 at the first key.
  - Down to about 6 s keep every scene and cut copy and steps; under 6 s cut whole beats: the error, fix and retry
    first (park `ERR` at 99), then the bars and SUCCESS (park `OK` at 99), never the typed command, the card or the
    power-off. Removing the card instead leaves a mostly bare 9:16 frame and needs the `hiss` cue deleted.
  - Each plan uses the block; HELD matched the measured hold in 16:9, 9:16 and 1:1 (14 s: 16:9, 9:16) and
    `python3 <skill>/scripts/check_audio.py audio.wav 8` passed (5, 4, 14). Commands are the demo's: replace "brew"
    with your tool. Held times are for the demo's copy.
  - The 4 and 5 s plans have no slack and the 8 s plan five frames. Typing time depends only on a command's length
    and its spaces, so a command as long as the demo's, with as many spaces, keeps the plan's times ("sluice run"
    for "brew serve" held 24). Each extra character costs about 0.027 s and each extra space 0.04 s more. A caption
    up to 27 characters ends before the fill and costs nothing; each character beyond costs 0.016 s. Tested in 9:16:
    an 8-letter tool with a 41-character caption held 17, 16 and 15 frames (8, 5, 4 s), and 23, 22 and 22 with a
    27-character caption. In 4–5 s, keep command 1 to 10 and 20 characters and the caption to 27.
```
8 s, every scene: boot 12 lines at 0.46 + 0.015 k, blank 0.64; P1 0.70; ERR = E1 + 1.00; P2 = ERR + 0.50;
  OK = E3 + 0.48; OFF 7.35; commands 2-3 'brew add milk', 'brew retry'; STEPS1 grind [E1 + 0.14, E1 + 0.40],
  pull shot [E1 + 0.44, E1 + 0.70], steam milk fails [E1 + 0.74, E1 + 0.92]; STEPS2 steam milk [E3 + 0.12,
  E3 + 0.40]. HELD 29 (6.400-7.35 s)
5 s, no error: boot as 8 s; P1 0.70; command 1 'brew deploy --strong'; ERR = 99; OK = E1 + 0.66; STEPS1 grind
  [E1 + 0.12, E1 + 0.34], pull shot [E1 + 0.38, E1 + 0.58], none failing: STEPS1.forEach(s => L(s[1], barLine(s)));
  STEPS2 = []; OFF 4.35. HELD 24 (3.567-4.35 s)
4 s, command to card: as 5 s with command 1 'brew serve', STEPS1 = [], OK = 99, ROLL = E1 + 0.20, OFF 3.35
  (the deploy line shows 0.13 s, then the clear). HELD 24 (2.567-3.35 s)
14 s: boot of 12 lines as in Composition; P1 1.10; P2 = ERR + 0.95; P3 = E2 + 0.30; a fourth command
  'brew status --all' with P4 = OK + 0.10, E4 = typeCmd(3, OK + 1.06); L(P4, promptLine(3), true) in place of
  L(OK + 0.1, PROMPT, true), then six status lines at E4 + 0.07 + 0.10 k and L(E4 + 0.80, PROMPT, true);
  ROLL = E4 + 1.20; OFF 13.35. HELD 43 (11.933-13.35 s)
```
- **Other formats:** the Composition block on any plan; timing, cues and holds are unchanged (mug `r0` 4 in 9:16).

## Boundaries
- **Distinct from:** `sci-fi-interface`, an ice-blue HUD of reticles, radar and amber cautions in Chakra Petch with
  Martian Mono data; `oscilloscope`, one beam trace inside a modelled instrument, heard as the sound; `vector-arcade`,
  stroke-font capitals and wireframes in three phosphors, no raster; `dither-1bit`, a whole scene in two inks;
  `teletext`, a 40 × 25 page in eight colours with mosaic blocks; `ascii-art`, a dense colour image from a glyph ramp;
  `retro-desktop`, a windowed GUI; `glitch`, corruption as the subject. The CRT power-on/off and phosphor finish are
  shared with those CRT styles; the terminal reads by its grid, prompt, typed command and whole-line log.
- **Poor fit:** pictures of the real world (`kurzgesagt`), charts with axes (`data-visualization`), modern app
  screens (`product-ui`), characters and feelings (`storytime`), a slogan as type (`kinetic-typography`).
- **Do not:** add a second hue (red errors, amber warnings), GUI windows, icons or images; smooth-scroll or fade
  text. Never type a real CLI's name (brew, git, npm, docker, kubectl, apt, pip, curl, ssh, aws…): the demo's brew is
  Homebrew's command and survives only as the reference's pun; name the tool after the subject (lampctl, sluice). No
  real hostnames, IPs, tokens, passwords or keys, and no real product's banner or prompt: use 192.0.2.x and
  example.com, which are reserved for documentation (RFC 5737, RFC 2606) and reach no one, and mask secrets.

## Technical notes
- Canvas 2D, no render.json, vendored library or GPU; about 0.07 s a still on one worker. Deterministic (`rng` 17,
  `hash`, audio.py's `default_rng(17)` in cue order): the test passes on the demo, the 9:16 version and the stand-in.
- `DUR` in anim.html is used (the dot fades until `DUR` − 0.15). Literal times outside the timing block: the card's
  0.08, 0.36, 0.8, 0.3 and 0.7 s offsets from `CUP` in `screenAt()`, the error flash's 0.5 s, the glitch's 0.34 s.
- `paintText()` assigns `globalAlpha` (the trail alpha) inside `save()`/`restore()`: to fade text, scale the alpha
  it is given rather than setting `globalAlpha` around it. The trails double the steam wisps in some frames (known).
