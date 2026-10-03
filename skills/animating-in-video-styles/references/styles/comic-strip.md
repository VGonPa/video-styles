# Newspaper Comic Strip (`comic-strip`)

A classic four-panel daily strip in black brush ink on warm newsprint, cut from a real-looking newspaper page.
An odd pair (a straight character and an unexpectedly wise one, the wit) trade a setup, a doubt, a silent beat and an
understated punchline. The humour is editorial: dry, literate and quiet, never slapstick.

**Reference film:** "Potted Wisdom": a houseplant tells its owner the day's plan is to lean toward the window, and after a silent beat over the owner's endless to-do list delivers "Ambition is overrated. *Direction* isn't." · `styles/comic-strip/`

## Signature
- A cream newsprint page with greeked text columns above and below a double-ruled band: the strip sits on a newspaper page, never on a blank background.
- A hand-lettered title (lettering only, no box or ribbon) inks itself in left to right, with a script byline on the right and a tiny date and © syndicate line under the strip.
- Panels are ruled on one at a time with a brush border; panel 1 holds two characters side by side at a counter, turned toward each other, in black ink, spot blacks and dot tone, with no colour.
- Rounded balloons of hand-lettered capitals pop in reading order, tails aimed at the speaker and stopping above the head.
- Characters move only in small poses stepped on twos (a blink, mouth flaps, a raised brow); everything else is still.

## Palette
| Role | Colour | In code |
|---|---|---|
| Ink: every line, spot black, dot and letter | `#171411` | `INK` |
| Newsprint page and every figure's fill | `#efe8d7` | `PAPER` |
| Whiter paper: balloons, window, to-do list | `#f4eee0` | `PAPER_HI` |
| Veil that turns dot tone into mid-grey | `rgba(239,232,215,0.35)` | `counter()`; 0.18 in `panel3bg()`, 0.25 in `panel4()` |
| Sunbeam cut through the toned wall | `rgba(244,238,224,0.93)` | `panel4()` |
| Greeked columns on the page | `rgba(40,34,28,0.14)` | `buildTextures()` |
| Double rules framing the strip band | `rgba(40,34,28,0.35)` | `buildTextures()` |
| Paper fibres, dark and light | `rgba(120,100,70,…)`, `rgba(255,255,248,…)` | `buildTextures()` |
| Vignette at the page edge | `rgba(110,90,55,0.16)` | `buildTextures()` |

- Two inks only: a warm near-black and cream paper. Inside the strip, grey exists only as dot tone under a paper veil, so the art reads as printed, not painted; no gradients on figures and no accent colour.
- `PAPER_HI` marks things whiter than the page (balloons, paper props, window glass) so balloons lift off the art.

## Typography and copy
- Three faces, one role each, all in `fonts.css`:
  - `TITLE` = `"Caveat Brush"` (`fonts/CaveatBrush-400-latin.woff2`): the strip title in mixed case, 84 px above panel 1, followed by a small inked emblem from the subject (a leaf); 138 px on the end card with a hand-inked underline.
  - `SIGN` = `"Caveat"` at weight 600 (`fonts/Caveat-600-latin.woff2`): the byline "by M. Ashby" at 36 px, top right of the strip, and the signature "Ashby" at 30 px in the last panel's lower-left corner, where strip cartoonists sign.
  - `LETTER` = `"Patrick Hand SC"` (`fonts/PatrickHandSC-400-latin.woff2`): every balloon at `FS` 27 px with `LH` 30 px leading, centred; small print at 20 px (date, syndicate), 17 px ("TO DO") and the end-card teaser at 36 px.
- Balloon copy is all capitals, as in hand lettering. Patrick Hand SC is a small-caps face, so lowercase would come out as small caps.
- Stress: wrap one word of a balloon line in asterisks (`'*WHOLE* PLAN?'`); `drawLine()` fakes a bold by stroking that word with a 1.5 px ink outline. Use at most one per balloon, on the word the joke turns on.
- `balloon()` takes lines you break by hand and sizes its oval to the widest one; nothing wraps. Measured at 27 px a line runs about 11.5 px per character ("ENORMOUS. I PLAN TO", 19 characters, is 221 px). The balloon is the widest line plus 60 px wide and lines × 30 + 40 px tall.
- Horizontal room in a 440 px panel, checked with `measureLine()` (character counts are a first guess; wide letters cost more: "MOMENTUM, MOMENTUM." is 19 characters and 251 px, 19 Ws are 316 px). A balloon is clipped to the panel, so its centre x needs half its width (widest line / 2 + 30 px) plus about 4 px of room on both sides. At the demo's positions that is about 175 px of text for the first speaker (centre x 118; "REPORT, CLAUDIUS?", 198 px, is cut) and about 240 px for the reply (centre x 290); a lone balloon across the top can take about 22 characters. Three lines per balloon, two balloons per panel.
- Vertical room: the centre y needs half the balloon's height (lines × 15 + 20 px) times 1.12 for the pop's overshoot; the demo's y 66 suits two lines, three lines need y 75 or more.
- 9:16 budgets: the right-column panels (2 and 4) must keep balloons within the first 365 scene px (see Composition), which cuts the horizontal room to about 180 px of text for a reply beside the first speaker (centre x 245), about 270 px for the punchline at centre x 200, and about 300 px for any balloon there. Write to these limits when the film is for 9:16.
- Strip title: Caveat Brush at 84 px runs about 33 px per character. Measure it with `ctx.measureText`: it must stay under about 435 px to clear the emblem at `SX` + 452 ("Two on a Ledge", 437 px, touches it; "Mammoth Women", 13 characters but 519 px, is cut by the 510 px clip in `drawStrip()`). The emblem does not follow the title: for any title, set its x to `SX` + 2 + the measured width + about 23 px (the demo's spacing), and for a title over about 435 px widen the 510 px clip to match.
- End card: at 138 px (about 54 px per character) the title is 1.64 times its 84 px width, and `endCard()` allows 740 px centred on `W / 2` + 70, so a title under 435 px at 84 px fits. The underline is a fixed 600 px: shorten it for a title much under 600 px at 138 px ("Still Life" is 416 px).
- Teaser at 36 px: about 15.5 px per character ("TOMORROW: BASIL ON PATIENCE.", 28 characters, 438 px); keep it under 740 px, about 45 average characters.
- Budget: 3–8 words per balloon (2–5 in an 8 s film; see Shorter), about 11 per dialogue panel, about 30 for the whole strip, and a punchline of six words or fewer. Longer copy: cut it, or split it across a second strip (see Length); never shrink `FS` or add a fifth panel.
- Text enters with its container: the title wipes on as if inked, the byline and credits fade in, and balloon text fades in during the balloon's pop. Nothing types on letter by letter, and balloons stay until the strip leaves.
- Voice: witty, understated and intelligent, a line an educated adult would enjoy. No slapstick: nobody falls, spills, collides or is hit; the silent panel's image is a still exaggeration (a list too long for the frame), not an accident. No sound-effect lettering and no exclamation marks. No puns: a sound-alike ("LEAF IT TO ME") and a stock idiom made literal ("KEEP MY CHIN UP", "I'M ROOTING FOR YOU") both count. The double meaning comes from one plain word used once (*DIRECTION*); a word repeated in two senses ("FOLLOWERS. I *FOLLOW*.") draws attention to itself, so it counts as a pun too.
- How the joke works: every line the wit says is literally true of what it is (a plant does lean toward light, and has for millions of years) and, read as advice, quietly judges the straight character; the wit stays calm and turns out to be right (a small, slow plant in the demo; any object or animal with a literal nature to draw on will do, as long as it can stand beside the straight character at the counter). The straight character only asks (lines end in "?"); the wit only states, in statements ending in full stops.
- Gag shape: panel 1, a plain question and a calm answer that makes something tiny the wit does sound momentous (the demo: a plan, "ENORMOUS. I PLAN TO LEAN TOWARD THE WINDOW."; the bust example below: a night's report); panel 2, the doubt ("THAT'S THE *WHOLE* PLAN?") and an unruffled justification drawn from the wit's nature (its great age is one source, the demo's and the natural one when the brief makes the wit old; what it has never needed is another, as in the bust's "I'VE NEVER NEEDED A CHAIR."; what it gets without trying is a third); panel 3, no words, one still image of the straight character's situation that the punchline will judge (the demo: a to-do list too long for its panel); panel 4, one or two short statements, six words at most, turned by the stressed word ("AMBITION IS OVERRATED. *DIRECTION* ISN'T."), true of the wit literally and of the straight character figuratively. The punchline should work without panel 3 and land harder with it.
- A second example, the same shape on another subject (a museum guard and a marble bust): "ANYTHING TO REPORT, CLAUDIUS?" / "ONE MORE NIGHT WITHOUT MOVING."; "YOU DON'T GET *BORED*?" / "I'VE NEVER NEEDED A CHAIR."; the guard slumped over his phone; "EMPIRES FALL. *POSTURE* LASTS." (figurative reading: "one quiet night and he has lost his bearing"; the empires appear only in panel 4).
- The beats and the tests are the reusable part; the demo's theme (busyness) and its lines are not. Write new lines rather than refilling "BIG DAY AHEAD…?", "THAT'S THE *WHOLE* PLAN?", "IT'S WORKED FOR…" or "… IS OVERRATED. *…* ISN'T."; the frame counts, not only the words: "X IS [anything]. *Y* ISN'T.", "[ADJECTIVE]. I PLAN TO …" and a "what are your plans" question are still the demo's lines with new nouns. The bust's punchline is a second example, not a second frame: "[NOUNS] [VERB]. *[NOUN]* [VERB]." with new words ("MARATHONS LOOM. *STEPS* LAND.", "MEDALS SHINE. *HOLES* BREATHE.") is a refill too. Test: if your line can be made from any example in this recipe by swapping its nouns and verbs, write another.
- Start from the literal fact about the wit in plain words, then cut it to six words around the stressed word. Other shapes on the bust, to show the range, not to fill: a tally, "NINE EMPERORS. ONE *POSE*."; one fragment with the stressed word first, "*UPRIGHT* SINCE BEFORE ROME FELL.".
- What keeps the punchline from being a slogan (two parallel sentences are aphorism-shaped, and the demo's line read alone would fit a mug):
  - Its stressed word names something the wit is literally doing, announced in panel 1 and visible in panel 4: *DIRECTION* is the lean toward the window. Read alone the line is a platitude; in the strip it means two things.
  - It deflates: something big (ambition) loses to something small the wit literally does (direction). It never promises, encourages or instructs. "Small" means modest, not a smaller piece of the big thing: "lines, not pages" or "steps, not the marathon" is the stock "one step at a time". Direction beats ambition by being a different kind of thing.
  - The wit never says "you" and never states the moral; the reader makes the link to the straight character.
  - In panel 4 the straight character has no balloon and reacts only with his face (the demo: eyes closed, a small smile). Any reply, even a question, explains the joke.
  - Before writing panels 2 and 4, write down the two or three things people always say about your subject (running: one step at a time; travel: wherever you go, there you are); none of the wit's lines may be one of them. Then say its figurative reading as one plain sentence about the straight character, using only what panels 1–3 show (the demo: "he is busy without a direction"). If you cannot, the line is decoration ("*HOLES* BREATHE" needs a note to mean "rest"). If the sentence is your subject's stock advice (running: one step at a time) or repeats what panels 1–2 already said, the punchline is a proverb in costume (the stressed word's literal meaning is announced in panel 1; the figurative sentence must be new in panel 4). Keep the literal truth and aim the judgement where panels 1–3 pointed but did not say: the demo names ambition only in panel 4.
- Off-voice punchlines for the same strip: "LEAF IT TO ME!" (pun, exclamation); "FOLLOW YOUR LIGHT AND YOU'LL ALWAYS GROW." (a promise to "you": a slogan); "SPEED IS OVERRATED. *TIMING* ISN'T." (the demo's frame with new nouns, and nothing the plant does: a mug line); "MAYBE YOU NEED A WINDOW." (says the judgement aloud); the owner replying "SO I SHOULD FOCUS?" (explains it).
- Credits are invented: a cartoonist (initial and surname), a syndicate in capitals after ©, a month-day date ("9-28"). The end card repeats the title and adds a dry next-day teaser, "TOMORROW: BASIL ON PATIENCE.", not a call to action. A brand or message belongs in the title or the end card; in the punchline only if it can be said as dry wit. If the brief needs a call to action or a URL, set it as one plain line of 20 px `LETTER` small print under the teaser, inside the end card's clip, like the credits; keep the teaser itself dry. The cartoonist's name is written twice, in the byline in `drawStrip()` and in the signature inside `panel4()`, and the title twice, in `drawStrip()` and `endCard()`. A rewritten last panel keeps the signature in its lower-left corner.
- Glyphs: the fonts are Latin subsets (Latin-1 plus curly quotes, dashes, €). Western European accents work; Polish, Czech, Greek or Cyrillic need other font files.

## Texture and finish
- `PAGE`, built once in `buildTextures()` and drawn under the camera, is the newspaper: `PAPER` fill, 34 soft light and dark blotches, 12,000 short paper fibres, greeked columns (grey bars 6.5 px tall every 15 px, thin column rules, a greeked headline block), the double rules above and below the strip band, and a warm vignette. It is `PM` (300 px) larger than the frame on every side so camera moves and the slide never show an edge.
- Panels have no fill of their own: the page shows through them, so the greeked bands and rules must stay outside the panel grid.
- Dot tone: `TONE` is a pattern from a 10 × 10 tile with two dots of 1.55 px radius, a 45° screen. `tone()` lays it, and a paper veil at 0.18–0.35 lightens it to grey. It lives in world space, so the dots enlarge on the push-in like a magnified print.
- Spot blacks balance every panel: hair, mug, soil, two of the five leaves (the `STEMS` rows whose last value is 1), sweater stripes. Give each new character or prop at least one.
- Screen-space finish after everything: `SPECK` composited with `lighten` at 0.55 knocks paper-coloured specks into solid blacks (dry-brush and press breakup) without touching the paper; `GRAIN` multiplies a fine static noise. Both are built once and never refreshed, which keeps the encode clean.
- The opening fades up from flat paper over 0.3 s; the close only veils to 30 % so the end card stays readable.

## Shapes, line and figures
- One line quality: `inkPts()` fills a polygon along the path whose width wobbles slowly (about ±14 % and ±8 %) and tapers at both ends like brush pressure; `taper: false` gives round caps for ruled lines. Of the figure linework, only `tube()` limbs use a plain stroke.
- Weights at 1×: panel borders 5.2 px, heads and torsos 5, most outlines 4–4.5, balloons 4, eyes, brows and mouths 3–4, hatching and small detail 1.6–2.6.
- `shape()` fills with paper (or `INK` for spot blacks) and then inks the outline, so overlaps occlude cleanly. Draw back to front.
- `ink()` understands absolute `M`, `L`, `C`, `Q` and `Z` only; any other command letter is dropped and its numbers are misread, so convert arcs and relative paths first. Draw each figure around a local origin (the owner at the bottom-centre of his torso, the plant at the bottom-centre of its pot) and place it with `x`, `y` and `s`.
- The wobble is seeded from the path string (`hashS()`), so static lines never shimmer while a path rebuilt from the stepped time boils slightly as it moves, on twos.
- Figures: a large round head (`ell()` 58 × 66), tall dot eyes, a C-shaped nose, ears that drop to one as the head turns, a spot-black hair mass with two cowlick strokes, a striped sweater (ink bands clipped to the torso), ellipse hands with one or two knuckle strokes, `tube()` arms. The head, eyes, nose, ears, hands and arms are the style; the hair shape, cowlicks and sweater are the owner's. Give a new character its own hair and clothes, keeping one spot-black mass (a ponytail, a bun) and one banded or spot-black garment. The demo never draws legs: crop figures at the counter or the border as daily strips do, or build legs as jointed `tube()` limbs.
- Facing is a number `f` from −1 to 1 that slides eyes, nose and mouth across the head and shifts the hair back: a three-quarter turn without a second drawing.
- Expression from few marks: one brow raised (`brow`, sceptical), inner ends up (`worry`), closed arcs (`closed`, content), half-lidded eyes (the plant's serenity), and `mouth` set to `talk`, `flat`, `wave` or the default smile.
- A non-human speaker gets the same marks on its simplest surface: the plant's face is on its pot.
- Form shadow is two to four parallel hatch strokes on one side (the pot's right flank); depth and walls are dot tone.
- Sets are minimal: a counter drawn as a heavy and a thin rule with tone below (`counter()`). The demo's last panel adds a window with a sun and a cloud because its punchline is about leaning toward it. To add an object: paper fill, a 4–5 px tapered outline, one spot-black or toned area, a few hatch strokes; no outline-less shapes.

## Composition and camera
- Four equal panels, `PW` 440 × `PH` 480, `GUT` 20 px apart, from `SX` 50 at `PY` 300: the strip spans 1820 px with 50 px margins, and `PX()` gives a panel's left edge.
- The title above panel 1, byline flush right; date and syndicate line below. The page's double rules and greeked columns bracket the band, so the strip reads as a newspaper clipping.
- Inside a panel: side-on and at eye level, a counter line at about 0.9 of the panel height, the two characters side by side at it, turned toward each other. The owner is cropped at the chest by the bottom border (his origin sits below it); the wit stands at about 0.7 of the width. At the demo's placement the owner fills about x 0–245 of the panel from his shoulders (y ≈ 380) down. A wit under about 120 px tall standing on the counter at 0.9 has its face at his shoulder height: keep the face right of x 250, or raise the counter to about 0.8 of `PH`.
- Balloons sit above the heads in reading order: the first speaker's top left, the reply lower right and overlapping it. They are clipped to the panel, so keep each one inside.
- Each panel shifts the shot slightly (the plant is 15 % larger in panel 2); the silent panel isolates one centred figure on full tone; the punchline panel restages (window set, the pair swapped sides) to mark the turn, and to put the punchline's literal meaning on screen: the plant visibly leans toward the window it planned to lean toward.
- One deliberate frame break per strip: `panel3list()` draws outside the panel clip, so the list unrolls over the border onto the page.
- 2D camera from `camera()`, applied as a world transform in `window.draw`: an opening settle from 1.035× to 1×, a push to 2.02× centred on panel 4 (the panel then fills about 90 % of the frame height), a slow creep while holding, a pull back. The camera never cuts between panels.
- Other formats: the demo shows only 16:9. The values below were rendered in a scratch copy (stills of the opening, the silent panel, the push and the end card); four panels in a row at 1080 px would be about 230 px wide, too narrow for 27 px lettering, so both use a 2 × 2 grid read in Z order.
- 9:16 (1080 × 1920), rendered:
  - Grid: scale 1.09 (panels about 480 × 523, grid 980 × 1066 with `SX` about 50), grid top `PY` 400, so the 84 px title's top sits just under the top 15 % band. Panel origins (50.4, 400), (550.0, 400), (50.4, 943.2), (550.0, 943.2).
  - Page: three greeked columns above the title rules and below the credits. Keep the page's offsets from the grid: double rules at `PY` − 74 and − 68 and at the grid bottom + 82 and + 87; greeked bands from y 34 to `PY` − 86 and from the grid bottom + 108 to `H` − 10.
  - Balloons: keep every balloon left of about 950 px, outside the right 12 % that review.md keeps clear. In panels 2 and 4 (the right column, x 550–1030) that means within the first 365 scene px of the panel (rendered with the panel-2 reply at centre x 245 and the punchline at 200).
  - Push: 2.02× on panel 4, which fills the width and keeps its balloon clear of the right band. The lower half of panel 2 (scene y over about 300) stays in view above panel 4: keep panel 2's balloons and tails above that line.
  - Small print: the byline and syndicate line, flush with the grid's right edge, and the credits under the grid fall in the bands; they are small print.
  - Frame break: the bottom row ends at y 1466, so a break out of panel 3's bottom border lands in the bottom 25 % band (the demo's list, at `todoList()`'s full `len` of 240, reaches y 1650). End any frame break within about 40 scene px (45 frame px) of panel 3's bottom border, by about y 1510 (rendered); for the demo's list that is `len` capped near 110; a break out of panel 3's left border has the 50 px side margin, and its top and right borders face panels 1 and 4 (see Style vs demo plot).
- 1:1 (1080 × 1080): scale 0.91 (panels about 400 × 437, grid 821 × 894 with `SX` about 130), grid top `PY` 112, the title at 64 px with its clip, emblem offset and baseline, and the byline (27 px), scaled by 64/84. With about 35 px left above and below, the greeked columns go in the side margins, each beside a double vertical rule. Push about 2.2× to fill the height as 2.02× does in 16:9. The panel-3 list unrolled to 240 scene px runs off the frame bottom; cap it near 120.
- To build the grid, keep `PW`/`PH` at 440 × 480 as the scene's coordinate space (`counter()`, `panel3bg()` and `panel4()` draw in it) and replace `PX(i)`/`PY` with a per-panel origin. `PY` assumes one row in `drawStrip()` (the panels, the translate before `panel3list()`, the balloon loop, and the title, byline and credits, which hang off `SX`, `PY`, `PH` and the 1820 strip width), in `panelBorder()` and in `camera()`'s push target. Put the title and byline above the top row and the credits under the bottom row. Draw each panel, its border and its balloons through one scale, and move the page's rules and greeked bands (built in `buildTextures()` at fixed y) with the grid.

## Motion
- Easing: `eOut()` for entrances (panel contents, borders, the list unroll, a brow raise), `eInOut()` for the camera push and pull (the opening settle uses `eOut()`), the title and end-card wipes and the head turn, `eIn()` for the strip accelerating away, and `backOut()` overshoot only for balloon pops and the end-card emblem.
- Characters run on twos: their pose functions take `stp()` of the time, stepped at `STEP` 15 fps (the to-do list's unroll is also computed from `stp()`), while the camera, borders, balloons and wipes move at the full 30 fps. Choppy characters against a smooth camera are part of the look.
- A panel enters as its border is ruled clockwise from the top left over 0.3 s (`panelBorder()`), while its contents fade in and rise 8 px into place.
- A balloon pops from its centre over 0.28 s with overshoot; its text fades in from about a quarter of the way through the pop.
- Talking: the mouth toggles open and shut every 0.13 s for 0.4–0.6 s after its balloon pops. Blinks are single 0.1 s closures at staggered times, about one per panel. A reaction starts just before the line it reacts to (the owner's brow rises 0.15 s before his question).
- Secondary motion stays tiny: coffee steam wiggles, the plant sways, the owner bobs 1.5 px.
- Exit: the whole strip anticipates 26 px to the right, then slides about 2200 px off to the left with `eIn()`; the end card wipes on behind it.
- Never: squash and stretch, camera shake, panels flying in, speed lines, colour, or smooth tweened character moves. The one exception is panel 4's slow lean (`le`, from unstepped `t`), a drift that rides the camera creep; compute every other pose from `stp()`.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.3 | Paper fades up; the camera settles from 1.035× over 1.4 s | `window.draw`, `camera()` |
| 0.15–0.75 | Title and leaf emblem ink on left to right | `T.title`, `drawStrip()` |
| 0.6–0.95 | Byline, date and syndicate line fade in | `T.byline` |
| 0.70 | Panel 1 ruled; owner and plant at the counter | `T.p`, `panel1()` |
| 1.15, 1.80 | Question balloon, then the calm answer | `T.b`, `BALLOONS` |
| 2.70 | Panel 2 ruled | `T.p`, `panel2()` |
| 3.00, 3.62 | The doubt, then the justification; the plant shrugs 3.55–4.05 | `T.b`, `panel2()` |
| 4.80 | Panel 3 ruled: silent beat on full tone | `panel3()` |
| 5.15–5.80 | The to-do list unrolls past the bottom border | `panel3list()` |
| 5.85–6.05 | The owner turns to camera, worried | `p3state()` |
| 6.55–7.35 | Panel 4 ruled as the camera pushes in on it | `T.push`, `camera()` |
| 7.55 | Punchline balloon pops; hold and slow creep until 8.65 | `T.b`, `panel4()` |
| 8.65–9.15 | Camera pulls back to the whole strip | `T.pull` |
| 8.8–9.4 | Strip anticipates, then slides off left | `T.slide` |
| 9.2–9.65 | End card wipes on: emblem pops, title, underline, teaser | `T.end`, `endCard()` |
| 9.8–10 | Paper veil to 30 % | `window.draw` |

- Review keys: render the original and your film with KEYS at the punchline hold (pop + 0.5 s; 8.05 in the demo) and on the held end card (9.7 in the demo); the default thirds miss both.
- Beat lengths: about 2 s per dialogue panel (the first balloon 0.3–0.45 s after the border, the reply about 0.6 s later), a 1.75 s silent panel, and at least 1 s of hold on the punchline.
- Reading pace: panels 1–2 hold 23 words (about 130 characters) between the first pop at 1.15 s and the push at 6.55 s, which takes them out of frame: about 4 words a second, with the 1.75 s silent panel as catch-up. Treat that as the ceiling; with no silent panel or more words, add time between balloons.
- The demo's end card is complete at about 9.6 s, only about 0.2 s before the veil starts; in a new film hold it at least 1 s (0.8 s in a film under 10 s; see Shorter).
- Reusable patterns: the inked title and credits, panels ruled one by one, pop-in balloons, the wordless beat panel, the push-in on the punchline, the slide-off, and the "TOMORROW:" end card. The houseplant, the owner, the mug, the to-do list and its lines are one-off demo content.
- Order inside a panel: border, then contents, then the first balloon, then the reply. The camera moves only for the punchline.

## Sound
- audio.py reads a list of cues `{k, t, …}` and synthesizes every sound with NumPy; unknown kinds are skipped silently, so check the spelling.
- Bed: quiet room tone (band-passed noise at 0.010) fading in over 0.6 s, sized from `DUR`, so it stretches with the film.
- Cue kinds and their fields:
  - `rustle` {t}: a 0.7 s newsprint rustle at the start.
  - `pen` {t, d}: six brush-pen scratches spread over `d`, for the title wipe and the end card.
  - `rule` {t, d}: one cue per panel border; each plays four ruled-pen scratches over `d` (one per side), panned left to right (the demo sends `d` 0.3 per border).
  - `pop` {t, v}: a soft balloon pop at gain 0.28 × `v`; one per balloon, `v` 1.2 for the punchline.
  - `leaf` {t}: a short high rustle for the plant's shrug.
  - `unroll` {t, d}: a paper rustle over `d` with nine accelerating ticks.
  - `clock` {t}: four ticks 0.5 s apart (1.5 s first to last); the handler ignores `d`. For a silent panel under 1.75 s change the tick count or spacing in audio.py so no tick lands on the push (rendered: three ticks 0.4 s apart, with the cue sent 0.1 s after the silent panel's border, in a 1.05 s panel; three 0.3 s apart in a 1.0 s one); for a longer one send another `clock` 2 s later.
  - `push` {t, d}: a low whoosh with the camera push.
  - `pluck` {t}: the punchline sting, two plucked notes (G then C, 0.22 s apart) and a soft high mallet, sent 0.05 s after the punchline pops.
  - `slide` {t, d}: a bright whoosh and rustle as the strip leaves.
  - `chord` {t}: a rolled C-major mallet chord over a low C under the end card.
- Limits: `pen`, `rule`, `unroll`, `push` and `slide` read `d` without a default, so leaving it out stops audio.py with a KeyError, and a `d` of zero or less stops it with a ValueError (an empty buffer). Every pan is fixed or drawn at random within ±0.4 (`pen` ±0.3, `pop` ±0.2) and no cue field reaches one, so no value turns the track to NaN; a large `v` only saturates the limiter, and a cue past `DUR` is dropped silently.
- audio.py looks up no cue by name and runs with any subset. A new strip should still send a `rule` per panel, a `pop` per balloon, `pen` for inked titles, `clock` during a silent panel, `push` with the camera, `pluck` on the punchline, and `slide` and `chord` at the exit. `leaf` and `unroll` suit any small rustle or paper move; drop them otherwise.
- Written at fixed times, not from cues: a walking bass of seven plucks from 0.5 s, `BEAT` 0.6 s apart (to 4.1 s), silent through the beat panel, then three plucks at 7.95, 8.55 and 9.15 s after the punchline. Re-time both runs from the new timeline: the setup bass ends before the silent panel, the return starts about 0.4 s after the punchline pop.
- Master: a 0.2 s fade-in, a 0.5 s fade-out at `DUR`, a tanh soft limiter.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Newspaper page, dot tone, grain and specks | `anim.html` → `buildTextures` | built once in `window.ready`; `PAGE` under the camera, `SPECK` and `GRAIN` over the frame | as is; adapt the greeked bands and rules if the strip moves |
| Dot tone | `tone()` | `tone(d)`: a path string or `[x, y, w, h]`; follow with a paper veil | as is |
| Brush stroke | `inkPts()` | `inkPts(P, w, o)`: points, width; `o.closed`, `o.taper`, `o.t0`/`o.t1` taper lengths, `o.upto` drawn fraction, `o.seed`, `o.color` | as is |
| Path inking | `ink()`, `shape()`, `fillD()` | `ink(d, w, o)` inks a path string; `shape(d, w, c)` fills with `c` then inks | as is |
| Geometry helpers | `ell()`, `dot()`, `tube()` | `ell(cx, cy, rx, ry)` returns a path string; `dot(x, y, rx, ry)`; `tube(d, w, lw)` outlined limb | as is |
| Balloon | `balloon()` | `balloon(cx, cy, lines, tip, u, o)`: centre, hand-broken lines, tail tip, pop progress; `o.tailW`, `o.bend` | as is |
| Lettering | `drawLine()`, `measureLine()` | `FS`, `LH`, `LETTER`; asterisks around a word stress it | as is |
| Ruled panel border | `panelBorder()` | `panelBorder(i, u)`: panel index, progress 0–1 | as is |
| Strip layout | `SX`, `PW`, `PH`, `GUT`, `PY`, `PX()` | | adapt for panel count and format |
| Strip assembly | `drawStrip()` | title wipe, credits, clipped panels from `PANELS`, balloons from `BALLOONS` | adapt: title text, emblem, credits |
| Camera | `camera()` | push target `PX(3)`, `T.push`, `T.pull` | adapt the target panel |
| Counter set | `counter()` | `counter(y, x0, toneBelow)` | as is |
| Owner | `owner()` | `owner(o)`: `x`, `y`, `s`, `f`, `rot`, `tilt`, `bob`, `blink`, `closed`, `down`, `brow`, `worry`, `mouth`, `arms`, `steam` | adapt or replace |
| Plant | `plant()`, `STEMS` | `plant(o)`: `x`, `y`, `s`, `lean`, `shrug`, `sway`, `look`, `blink`, `talk`, `brow`; the mouth is always a smile unless `talk`, and the `smile` callers pass is ignored | replace |
| Scenes and copy | `panel1()`…`panel4()`, `panel3list()`, `todoList()`, `BALLOONS`, `T` | `BALLOONS` row: panel, pop time, x, y, lines, tail tip | replace |
| End card | `endCard()` | wipe, title, teaser; the emblem is the wit itself, `plant()` at 0.82 beside the title, popping with `backOut()` and blinking at 9.8 s | adapt text; draw the new wit as the emblem |
| Cues | `window.events` | `rule` from `T.p`, `pop` from `BALLOONS`, the rest from `T`; only `rustle` (0.02 s) and `leaf` (3.55 s) are literal times; the durations sent with `unroll` (0.65), `slide` (0.5) and the end-card `pen` (0.45) are literals too, so change them when those beats change length (`clock`'s 1.5 is ignored) | adapt |

## Adapting
- **Style vs demo plot:**
  - Always the style: the newspaper page (greeked columns, double rules, vignette); the inked title with a small emblem of the wit, the byline, date and © line; panels ruled one at a time; the brush line, spot blacks and veiled dot tone; balloons popping in reading order; characters on twos; the four beats (setup, doubt, silent panel, punchline); one frame break; the push-in on the punchline; the slide-off and the "TOMORROW:" end card (a film under about 7 s drops the slide-off and end card first; see Shorter).
  - Demo plot, to replace: the plant and its lean; the owner's mug (built into `owner()`'s default arms); the to-do list; busyness; and the window in panel 4, which is there only because the plant leans toward it.
  - The punchline panel's restage shows what the new stressed word literally refers to (for the bust's *POSTURE*: the bust upright on its plinth beside the guard slumped in his chair). A window nothing refers to is demo residue.
  - The silent panel's still exaggeration and the frame break need not be one object, nor something that unrolls. Anything in the silent panel crossing a border counts: an elbow, a prop, the wit itself. Break the silent panel's bottom border, as the demo does, or in a 2 × 2 grid its left (outer) border: its other borders face a neighbouring panel across the 20 px gutter (panels 2 and 4 in 16:9; panel 1 above and panel 4 to the right in 9:16 and 1:1), and `panel4()`'s toned wall paints over anything that crosses into panel 4 (rendered in the 9:16 grid: a shape reaching 42 scene px past panel 3's right border (about 24 px into panel 4) shows cut and greyed at the edge of the pushed punchline, while one past its left border sits cleanly in the margin). Draw the crossing part after the panel, outside its clip, as `drawStrip()` draws `panel3list()`.
  - The transformation is the restage plus the push-in; the strip needs no other event.
- **New subject:** keep the odd pair (one straight, one calmly wise), the four beats, the inked title and credits, and the slide-off end card. Invent the title, cartoonist and syndicate. Rewrite `BALLOONS`, `T` and the panel functions; draw new characters with `shape()`, `ink()` and `tube()` and give them the owner's parameters (facing, blink, brow, mouth) so they can act on twos. Trap: many times are literals inside panel functions and `events()` (the shrug at 3.55, the turn at 5.85, blinks, the `leaf` cue), so grep for decimal seconds after moving `T`. Blinks and other short windows are tested against `stp()` time, a multiple of 1/15 s: a window that holds no multiple of 1/15 s never fires.
- **Length:** a strip carries about 10 s. For 20–30 s chain strips: slide one off and rule the next on the same page, putting the end card only after the last; or add a second tier of panels and pan down to it. Each strip needs its own setup, silent beat and punchline; three in a row is the limit before the push-in turns predictable, so in a middle strip skip the push or push on the silent panel instead. In audio.py set `DUR` and repeat both bass runs for each strip; in anim.html `DUR` is unused, so change `T`, the closing fade's literal 9.8–10 s in `window.draw` and the emblem's blink time. Render time grows linearly.
- **Shorter:** the four beats are the joke, so down to about 6 s keep all four panels and shorten holds and copy rather than cutting a panel; cut words, not reading time. Both plans below were rendered at 1080 × 1920 on the 9:16 grid (contact sheets, key stills and an audio.py run):
  - 8 s: title 0.1–0.55 s; panels ruled at 0.40, 1.90, 3.40 and 4.45 s (1.5 s per dialogue panel, a 1.05 s silent panel); inside the silent panel the frame-break move runs from 0.2 to 0.65 s after its border and the reaction ends about 0.2 s before the push; balloons at 0.80 and 1.35, 2.25 and 2.80 s; the push 4.45–5.05 s and the punchline popping at 5.20 s, held to the pull at 6.20–6.55 s; the slide 6.30–6.80 s overlapping the end-card wipe 6.60–6.95 s; the end card held to the veil at 7.8–8.0 s. Copy: 14 words in panels 1–2 (balloons of 2–5 words) and a five-word punchline, under 4 words a second.
  - 6 s: drop the pull, the slide-off and the end card, and end on the pushed punchline: panels at 0.30, 1.55, 2.80 and 3.80 s; balloons at 0.65 and 1.10, 1.85 and 2.30 s; a 1.0 s silent panel; the push 3.80–4.35 s; the punchline at 4.50 s held to the end under the last 0.2 s of veil. Copy: about 9 words in panels 1–2 (balloons of 2–3 words). Move `T.pull`, `T.slide` and `T.end` past the film's end: the camera then holds, the strip stays, `endCard()` draws nothing, and audio.py drops their cues silently.
  - Drop the end card first (with its slide and hold it costs about 1.5 s), then the pull-back; never the silent panel or the push-in, which are the joke's timing. The title inks on from 0.1 s and the credits from about 0.4 s and the first balloon by about 0.8 s, so a short film loses none of the signature. Under about 6 s four panels cannot be read: use magazine-cartoon (one panel, one caption).
  - Re-time in anim.html `T`, the veil's literal 9.8–10 s in `window.draw` and the literal pose, blink and cue times (see New subject); in audio.py `DUR`, the setup bass (rendered: six plucks 0.5 s apart from 0.3 s at 8 s, five 0.45 s apart at 6 s, both ending before the silent panel), the return about 0.4 s after the punchline pop, and `clock` (see Sound).
- **Other formats:** the 2 × 2 grid in Composition keeps the scenes and their balloons unchanged under one scale, except the 9:16 right-column balloons (see Composition). Restack the end card, because its emblem-beside-title row is about 1000 px wide and its y values are fixed: rendered at both sizes, the emblem's origin at `W / 2`, `H / 2` − 60, the title centred on `W / 2` with its baseline at `H / 2` + 80, the underline 600 px wide centred on `W / 2` (− 300 to + 300) at + 110, the teaser at + 156, and the wipe clip 760 × 240 px from `W / 2` − 380, `H / 2` − 40, which leaves room for a call-to-action line about 34 px under the teaser. The emblem pops by scaling about its origin, so draw the new wit around its base. The plant at 0.82 spans about 200 px wide and 265 px tall above that origin; scale a squat wit to a similar width. Take the camera's resting focus and the vignette radii from `W` and `H` too (500 and 1250 are 0.26 and 0.65 of the frame's long side, 1920 in 16:9 and 9:16).

## Boundaries
- **Distinct from:** `comic-book` (colour, action, sound-effect lettering and a camera that dives into each panel); `minimal-strip` (thin trembling pen, white space, soft flat colour); `office-strip` (flat muted office colour, clean uniform line, three panels); `sunday-strip` (watercolour washes, several tiers); `magazine-cartoon` (one panel with a caption underneath, grey wash).
- **Poor fit:** action and heroics (`comic-book`); charts and numbers (`stick-webcomic`); a single one-liner with no setup (`magazine-cartoon`); colour or brand palettes (`office-strip`); long narration (`clear-line`); a film under about 6 s (`magazine-cartoon`).
- **Do not:** reproduce a real strip's cast, title lettering, cartoonist or syndicate; every name in the credits is invented. No colour, no sound-effect lettering, no slapstick. Do not caption what the art already shows; the silent panel carries the joke's contrast without words.

## Technical notes
- No `render.json` and no `vendor/`: plain canvas 2D, no GPU needed. The film is `anim.html` with `fonts.css` and three fonts in `fonts/`; 300 frames render in about 15–25 s at two workers; a full build.sh takes about 1.5 minutes, most of it the x264 `-preset slow` encode and the GIF.
- Deterministic: textures use `rng(58)`; the to-do list's squiggles re-seed `rng(7)` on every draw; line wobble is seeded from each path string.
- `window.ready` loads the three fonts before building textures; a new face needs a matching `document.fonts.load` there.
- Sizes hard-coded outside `W`/`H`: `1820` (strip width) in the greeked columns, the page rules, and the byline and syndicate positions; the rule rows at 226, 232, 862 and 867 and the greeked bands at 34–214 and 888–1070; `960` and `540` in the camera transform in `window.draw` and in `camera()`'s resting focus, whose `fy` starts at 528; the title clip width 510 and emblem offset `SX` + 452 in `drawStrip()`; the vignette radii 500 and 1250; the slide distance 2200: keep it in every format, since with `eIn()` a shorter slide leaves the strip over the end-card wipe; it must also exceed the strip's right edge (1870 in the demo, about 1031 in 9:16); the end card's offsets around `W / 2` and its absolute y values (clip 380–700, title baseline 560, underline 590, teaser 636, emblem 652), which put it in the top third of a 1920-tall frame.
