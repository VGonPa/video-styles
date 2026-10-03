# Magazine Cartoon (`magazine-cartoon`)

A single-panel gag cartoon printed on the page of an invented weekly magazine, in the tradition of the urbane
magazine cartoon: an economical dip-pen line, a grey wash, well-dressed adults in a sparse urban interior, and one
italic caption in quotation marks set under the panel. The cartoon draws itself stroke by stroke, the wash blooms,
and after a beat the caption fades in and one character reacts with the smallest possible gesture. The picture
plays it straight; the wit is all in the caption, and it is dry, literate and unhurried.

**Reference film:** two cartoons in *The Lamplight Review*: a couple before a huge, ornately framed blank canvas ("Apparently it sold before he could ruin it."), then, after a page turn, a woman with a martini telling a man with a tumbler "We met ironically, but it's become rather sincere." while he takes a slow sip · `styles/magazine-cartoon/`

## Signature
- A cream magazine page, complete as soon as the 0.3 s fade-up from blank paper ends: the magazine's name and a date in tracked capitals over a thin rule, a ruled panel centred below with wide paper margins, an italic page number at the foot.
- Inside the panel a cartoon draws itself at constant speed with a tapering, slightly wobbly dip-pen line: the speaker first, then the listener (both figures by 1.1 s), then a sparse setting of a few props (by 2.15 s).
- Monochrome: a mottled grey wash blooms region by region after the line, one solid-black mass (her bob and dress) inks in, and a small italic signature appears in the panel's lower right. No colour anywhere.
- Well-dressed adults in strict profile, standing still in an everyday urban interior, each drawn with a few dozen lines: long-nosed profiles, closed or half-lidded eyes, plain suits and dresses.
- After a beat (0.8 s after the line is finished) one line of italic caption in curly quotes starts to fade in, centred under the panel, at 2.95 s.

## Palette
| Role | Colour | In code |
|---|---|---|
| Ink: every line, solid black and all type | `#171513` | `INK` |
| Solid-black mottle (hair, dress, bow tie) | `23, 21, 19` | `inkPat` in `buildTextures()` |
| Grey wash, at alpha `tone` | `92, 90, 88` | `WASH`, `washPat` |
| Paper: page, fades, every margin | `[245 + k, 240 + k, 228 + k * .9, 255]` | `paperC` in `buildTextures()` |
| Lit windows punched out of a wash | `#f5f0e4` | `PAPER` |
| Paper fibres | `rgba(120,100,80,…)` | `buildTextures()` |
| Paper vignette at the edges | `rgba(90,70,40,.10)` | `buildTextures()` |
| Running-head rule | `rgba(23,21,19,.85)` | `buildPage()` |
| Panel border | `rgba(23,21,19,.9)` | `buildPage()` |
| Spine shadow down the left edge | `rgba(60,45,25,.22)` | `buildPage()` |
| Shadow cast by the turning page | `rgba(40,30,15,…)` | `pageTurn()` |
| Gloss and shade on the turning page | `255,250,235`, `30,22,12` | `pageTurn()` |

- One ink and one grey. Tone comes only from the wash's alpha (`tone` 0.14–0.75 in `WASHR()`) and from solid blacks; never colour, gradients on figures, or hatching for shade.
- Washes are translucent and fill the authored region exactly, while the pen line on top wobbles, so line and wash disagree slightly at the edges, as in real pen and wash. Overlapping washes darken.

## Typography and copy
- One family, EB Garamond (`SERIF`), from `fonts/EBGaramond-latin.woff2` (roman, weights 400–800) and `fonts/EBGaramond-Italic-latin.woff2`, declared in `fonts.css`; `window.ready` loads `italic 52px` and `500 21px` before building textures.
- Caption: italic 52 px in `INK`, centred on x 960, baseline `PY + PH + 92` (876). It fades in over 0.5 s with `eOut()` while rising 10 px and stays until the page turns. Nothing types on.
- Running head (`buildPage()`): weight 500 at 21 px with `letterSpacing` 5 px, written in capitals, the magazine's name flush left at x 110 and the date flush right at 1810, baseline 40, over a 1.4 px rule at y 50.
- Folio: italic 24 px centred at (960, 1052); odd numbers (47, then 49 after the turn), as right-hand pages are.
- Signature: italic 26 px, right-aligned at `PX + PW - 26`, `PY + PH - 22`, inside the panel; it fades in as the line finishes.
- Measure: at 52 px a caption runs about 18.5 px per character (`CAP1`, 45 characters with its quotes, is 822 px; `CAP2`, 52, is 967 px; ten Ws are 555 px). In 16:9 keep it on one line inside the panel's 1100 px, about 55 characters. 9:16: at most two lines of 800 px (about 43 characters), broken by hand at a phrase boundary. 1:1: at most two lines of 900 px. Positions in Composition.
- Form: one sentence (two short ones at most) of 5–12 words (the demo's are 8 and 8; every word past 8 costs 0.25 s of screen time, see Film grammar), in curly quotes (“ ” and ’) with the full stop inside, sentence case, no attribution. It is spoken by one figure in the picture; the other listens with closed or half-lidded eyes and supplies the reaction. The viewer learns who speaks from the drawing order (speaker first) and the reaction, since the demo's open-mouth tick reads as a smile (see Shapes).
- Voice: deadpan and well read, the register of a dinner party overheard ("Apparently", "rather"). No exclamation marks, no puns (a stock phrase made literal counts: “It was the least we could do, so we did it.”), no capitals or italics for stress, no slang, sound effects or emoji. The speaker is calm and never knows they are funny.
- How the demo's gags work (mechanisms, not templates):
  - Museum, the model: the picture shows a blank canvas framed and roped off like a masterpiece; the man relays it as ordinary art-market news. Its reading goes past the stock "you're only paying for the name" and "less is more": the market bought the painter's name before his work could lower its price, so the painter is the only threat to his own painting. "Before he could ruin it" is what does that.
  - The museum caption points at what the picture shows with a pronoun ("it") and never names it. Naming what is visible ("this blank canvas") explains the joke.
  - It opens on a sentence adverb because "Apparently" does work: it marks hearsay, which lets the speaker pass the absurd on as news. Open on an adverb only when it does such work; "[Adverb], [statement]" is not the house shape.
  - Party, not a model: “We met ironically, but it’s become rather sincere.” is a quip. It fails the cover test below (it would work under any couple, and the picture shows nothing odd). It is the demo's line, not a pattern for a new caption.
- Tests before you keep a caption:
  - Cover the picture: the caption alone should be incomplete (what sold? who is "he"?); merely flat is not enough, because a flat line usually stays flat under the picture. Cover the caption: the picture alone should be odd but unexplained. A caption that works without the picture is a quip pasted under a drawing; a picture that is already the joke makes the caption redundant. A caption that is merely true of the picture adds nothing, however dry: “Less is more, darling.” under the canvas, or any line that only explains how the odd thing got there.
  - Take the oddity out: picture the same scene without it (the museum couple before an ordinary painting). If the caption is still a joke there, it does not depend on the picture and is a quip. A caption that depends on the picture goes flat without the oddity: before an ordinary painting the museum line is mere gallery gossip about a painter who overworks. The party caption fails this: its picture has nothing odd, and the line is as funny under any couple.
  - Say its figurative reading as one plain sentence about people (museum: "the market bought his name before his work could lower its price"). If you cannot, the caption is decoration. If that sentence is what everyone already says about the subject, the caption is a cliché in costume.
  - First write down the two or three things people always say about the subject (modern art: "my kid could paint that", "but is it art?"; marriage: "opposites attract"; therapy: "and how does that make you feel?"). List them also for what your figurative sentence is about when that differs from the brief: a coffee-machine caption whose reading is about parents and money must not restate what people say about parents and money. The caption may not be one of them, nor mean one of them. Turning a stock line around is allowed when the figurative sentence is new ("parents now fear the habits they used to nag for" turns "kids never read"); restating one with new nouns is not.
  - Every example in this recipe is a mould, frame included: "Apparently it [verb]ed before he could [verb] it." or "We [verb]ed [adverb], but it's become rather [adjective]." with new words is still the demo, and so is any caption turning on "X, but it's become Y". If your caption can be made from any example here by swapping any of its words, the opening adverb and the pronouns included ("Evidently it closed before anyone could review it." is the museum line), write another: the sentence's shape is the mould.
- A second example, to show range, not to refill: two parents stand at their teenager's door; he lies on his bed reading a paperback. The mother: “We’re giving it a week before we call anyone.” Covered, the picture is odd but unexplained (why are they watching him read?) and the caption is incomplete (giving what a week? call whom?). Figurative reading: "parents now fear the habits they used to nag for". It applies the vocabulary of a worrying symptom to a virtue. "We're giving it a [time] before we [verb]" with new words is a refill.
- Off-voice captions for the museum panel: “My kid could paint that!” (the stock line, shouted); “Ten million dollars for a blank canvas?” (names what is shown and says the joke aloud); “It’s called Untitled. Get it?” (explains itself); “Talk about a blank cheque.” (a pun on an idiom); “Less is more, darling.” (a proverb: true of the picture, adds nothing).
- Brands and messages: the cartoon observes; it does not sell. Put the product into the picture's situation and keep the caption a social observation, or make the brand the magazine's name in the running head. No call to action, URL or hashtag in the caption.
- Names are invented: the magazine (never a real one), the date and the cartoonist. The name and date are written once each in `buildPage()`; the signature `'Ashby'` three times (two `cartoon()` calls in `window.draw` and one in `pageTurn()`).
- Longer copy: cut it. A cartoon carries one line; a second idea becomes a second cartoon on the next page. Never smaller type, a second caption, or a balloon.
- Glyphs: Latin subsets (Latin-1, Œ and œ, curly quotes, dashes, ellipsis, €, ™). Western European accents work; Polish, Czech, Greek or Cyrillic need other font files.

## Texture and finish
- `paperC` (built once in `buildTextures()` by `noiseCanvas()`, seed 3): value noise in three octaves (64, 24 and 8 px lattices) shading the paper a few levels either way, 900 faint fibre strokes and a radial vignette from 500 to 1250 px. Static: nothing flickers.
- `washPat`: a 512 px tile of `WASH` grey whose alpha is noise around 0.55, so every wash is mottled like watercolour. `cartoon()` fills each region at its `tone`, then strokes its outline 5 px wide, clipped inside the region, at 35 % of that, so pigment seems to pool at the edges.
- `inkPat`: a 256 px tile of near-black at alpha about 0.9 ± 0.15; solid blacks are brushed ink, not flat fills.
- `buildPage()` paints each page once (cached in `pages`): paper, running head, rule, folio, the 1.6 px panel border and a 70 px shadow along the spine.
- The opening and closing fades lay `paperC` over the frame: the film starts and ends on blank paper, never on black.
- The page turn is the only light effect: shading and a soft gloss across the bending page, and a shadow on the page beneath.

## Shapes, line and figures
- Every line is an open stroke, `S(d, w)`, from an SVG path string (any path command; it is measured through the hidden `<svg>` path `sp`). `buildScene()` samples it every 2.2 px, adds a slow wobble of 0.55–1.05 px, tapers it in over 7 px and out over 16 px, and sets a half-width of 1.28 × `w` × a per-stroke pressure (0.8–1.15) with a gentle swell. Author clean geometry; the wobble is added, so never add jitter of your own.
- Weights (`w`): 1 for outlines; 0.8–0.9 for secondary outlines (ears, hands, glasses, inner frames); 0.6–0.7 for features (eye, mouth, brow, spectacles); 0.35–0.5 for small detail (floor lines, fringe, label text, pocket marks); 1.5 only for the heavy rope. The weight does not scale with `XF.s`, so a figure at 1.2× keeps the same pen.
- Outlines need not close: the demo's jacket front, back and hem are separate strokes. `crD()` turns a point list into a smooth path; `limb()` strokes both edges of a tapered tube and returns its outline for a wash.
- No occlusion: washes are translucent, fills and lines draw over everything, and nothing hides anything. Break background lines by hand where a figure stands (the museum's wall line stops at x 719 and resumes at 809 behind the man), keep props from overlapping figures, and keep animated limbs short: the demo's sip shows its forearm crossing the chest outlines.
- Figures: strict profile (authored facing left, mirrored with `XF.a` −1), tall and still, heads about 1/5.5 of the height (the man is about 442 authored px tall). A long nose line, one short arc for an eye (closed or half-lidded, the deadpan look), a one-tick mouth (slightly open for the speaker), a small loop for an ear, hands as closed loops round a prop, legs as two strokes with a knee crease, shoes as loops, clothes as a few strokes (lapel, collar, pocket, buttons as 1 px ticks). Hair is a solid-black mass, a grey wash or a bald crown line.
- Seated or reclining figures (a chair, a couch, a bed) are not in the kit: build thighs and shins with `limb()`, break the seat's lines by hand where the body rests on it, and wash the body and the seat as separate regions that do not overlap, or their tones add into a dark box.
- Expressions are single marks: a brow, an eyelid, a mouth. A reacting feature must sit on bare skin with room above it: the demo's raised brow climbs into her black bob and all but vanishes (compare 3.5 s and 4.05 s at full size).
- The speaker's "open" mouth in `manFace()` (with `open`) is a 9 px tick at `w` 0.6 that curves up and reads as a closed smile; drawn at `w` 0.8 it still does (rendered at 4.05 s). To make the speaker unmistakable, draw an open mouth: a small closed outline under the nose (about 9 × 4 authored px, a D or an oval), stroked at `w` 0.5–0.6 and filled with `FILL()`. Rendered, it reads as speech; like every fill it appears only near the draw's end.
- Settings are suggested by three to five props with no ceiling and no perspective except a floor line: a frame and a wall label, stanchions and rope, a doorway; a sofa, a print, a lamp, a window with a skyline. Under each figure and stanchion goes a flat grey ellipse of shadow (tone 0.2–0.22).
- A new object: one to three outline strokes at `w` 1 (or 0.8–0.9), interior detail at 0.35–0.6, one wash region at tone 0.2–0.5 blooming after the line, a floor shadow if it stands. Give each cartoon one solid-black mass (`FILL()` with `INK`) for contrast: a dress, hair, a bow tie, a cat.

## Composition and camera
- 16:9 page: the panel `PX` 410, `PY` 64, `PW` 1100 × `PH` 720 (about 3 : 2), centred with 410 px of paper on each side, hanging 14 px under the running-head rule; caption baseline 92 px below the panel; folio near the foot. The wide margins are the look: this is a printed page, not a full-bleed frame.
- In the panel: an eye-level, side-on stage. The wall meets the floor at about 0.78 of the panel height (y 560), drawn as a heavy stroke under a thin 0.35 one 12 px above; the floor is two or three loose short strokes. Feet stand at about 0.9 (y 645–657), heads near 0.16–0.22: the figures fill about three quarters of the panel height.
- The pair stands side by side in profile (museum: on the right, both facing the canvas, about 40 px apart; party: in the middle, facing each other, about 90 px apart, props on both sides). The blank canvas takes 44 % of the panel width, because its emptiness is the joke.
- No camera. The page never moves, zooms or cuts; the only movement of the frame is the page turn.
- 9:16 (1080 × 1920), rendered with both demo scenes restaged, the page turn and the fades:
  - Canvas and `W`/`H` 1080 × 1920; a square panel `PX` 60, `PY` 300, `PW` 960, `PH` 960. Running head at baseline `PY - 24` from `PX` to `PX + PW`, rule at `PY - 14` with width `PW`: small print in the top band. Folio at `W / 2`, `H - 28`.
  - Caption centred on `W / 2` at `PY + PH + 92` (1352), a second line 62 px lower (1414), both above the bottom 25 % band; one line of 822 px (`CAP1`) reached x 951, the edge of the right 12 % band, so keep lines under 800 px.
  - The bottom band (y 1440–1920) holds only the page's paper and the folio: low in detail but textured, as the 16:9 side margins are, and it is the band Reels, Shorts and TikTok cover. Keep `paperC` full frame (it is built at `W` × `H` in `buildTextures()`); never fill the band flat. The signature sits in the right band; it is small print.
  - Recompose rather than scale. Rendered museum values: the setting under `XF = { a: 1, s: .87, e: 0, f: 147 }` (wall line at 634, 0.66 of the panel; the painting at x 103–525, y 224–516), the figures under `XF = { a: 1, s: 1.45, e: -480, f: -57 }` (about two thirds of the panel height, feet at 880), the doorway pushed out of the panel, and the wall lines re-broken round the new figure positions. The figures' `e` can range from about −480 (the man's jacket clears the wall label) to −435 (the woman's shadow stays inside the panel); re-break the wall lines for whatever you choose. Party: the woman at `{ a: -1, s: 1.45, e: 1767, f: -70 }`, the man at `{ a: 1, s: 1.45, e: -440, f: -57 }`, the window block shifted 80 px right so it clears the man.
  - Furniture that stands in the room (a counter, a table, a lamp) has its base near the figures' feet, as the demo's lamp and stanchions do (bases at y 598–604, between the wall line at 560 and the feet at 645). In 9:16 these values put 246 px between the wall line and the feet (85 px in 16:9): a counter drawn at the figures' scale with its base on the wall line rose to their shoulders and read as a high cabinet; with its base at y 850 its top met their waists (rendered). Things on the wall (a painting, a cabinet, a window) are unaffected.
  - With those values the square panel's top fifth is empty wall (the painting starts at 224, the heads at 236). Let a prop reach into it: two picture lights hung from the top border over the painting (rods to y 150, shades to 180) and a pendant lamp over the party couple (rod to 120, shade to 162) filled it in a render; a tall window, door or picture rising into it works too.
  - Those figure values assume standing adults. A low stand-in (a long dog at 1.2×, then 1.5×) left the upper right of the square panel empty; what fixed it: the subject in front of the props with its feet at 0.97 (y 930), the props larger and lower (`s` 0.95, wall line at 0.73), and a tall prop up to the wall line on the side the subject leaves free (a doorway at x 840–935). Keep the signature corner (about 130 × 60 px at the panel's lower right) clear; the dog's hindquarters crowded it.
- 1:1 (1080 × 1080), rendered: keep the 16:9 scene and scale it through the base transform in `cartoon()` (`translate(PX, PY)` followed by `scale(PW / 1100)`); `PX` 60, `PY` 120, `PW` 960, `PH` 628; running head, rule and folio as in 9:16; caption at `PY + PH + 92` with lines under 900 px (`CAP2`, 967 px, needs two). Line weights thin by the same 0.87; they still read.
- For two-line captions, replace the caption's single `fillText` in `cartoon()`:

```js
cap.split('\n').forEach((ln, i) => c.fillText(ln, W / 2, PY + PH + 92 + 62 * i + 10 * (1 - eOut(cu))));
```

## Motion
- The pen: `cartoon()` maps `seg(t, D[0], D[1])` linearly onto the strokes in authored order, with no easing; each stroke's share of the time is its length plus a 60 px pen lift, and it grows sample by sample (`poly()`). Demo speed: about 10,900 px a second in scene 1 (114 strokes, 13,250 px of line, 20,090 with lifts, in 1.85 s) and 14,300 in scene 2. These are authored lengths, measured by `sp.getTotalLength()` before `XF` scales the points, so a figure at `XF.s` 1.45 (the 9:16 values) covers 1.45 times more screen at the same number.
- 14,300 is the demo's fastest scene, not a tested limit. At that speed the pen advances about 477 px a frame, so most strokes (median 62 px) appear within one frame; what a viewer sees is how long each figure takes: 0.30–0.45 s in the demo (scene 2's speaker is the fastest, 9 frames), 0.27–0.41 s in the short plans under Adapting. Keep every figure at about 0.27 s (8 frames) or more, the shortest the tested plans used without the draw losing its order, and shorten a draw by trimming props, not by speeding the pen.
- Order is part of the joke: speaker, listener, then the setting. The scene-1 man is complete at 0.76 s, both figures at 1.08 s; the props take the second half of the draw.
- Wash regions bloom with `eOut()` over 0.38 s from `tw` + the region's `delay` (0–0.25) + 0.03 s × (index mod 5). Solid blacks fade in with `eOut()` from 0.2 s before the draw ends to 0.15 s after; the signature from 0.05 s before to 0.25 s after.
- One reaction per cartoon, by the listener, 0.5–0.75 s after the caption: scene 1's brow pops with `backOut()` (overshoot 1.6) over 0.3 s, rotating −7° and rising 9 px, and settles to 65 % with `eIO2()` 1.1–1.4 s later; scene 2's sip, an `eIO2()` two-bone reach in `groupsFor()`, takes 0.42 s up, holds 0.36 s and takes 0.34 s down, the wrist tilting the glass. Scene 2 also lifts the speaker's brow at the same time (`brow2`: 6° and 4.5 px over 0.25 s, returning over 0.3 s from 0.8 s after it began); a new film can drop it.
- The page turn rotates the page on its spine in perspective with a slight bend, `eInOut()` over 0.8 s; the next cartoon starts drawing 0.08 s before it ends.
- Fades: `eOut()` over 0–0.3 s from paper, `eIO2()` over `T.out` back to it. Everything runs smoothly at 30 fps; the wobble is baked once, so lines never boil.
- Never: a camera move or zoom, a figure walking or moving more than one gesture, squash and stretch, speed lines, balloons, type-on text, colour, a bouncing caption.

## Film grammar
| Time (s) | What happens | In code |
|---|---|---|
| 0–0.3 | Page fades up from blank paper: running head, rule, empty panel, folio 47 | `window.draw`, `buildPage()` |
| 0.3–1.08 | The speaker draws (face, crown, spectacles, suit, arm, legs), then the woman | `T.d1`, `buildScene()`, `cartoon()` |
| 1.08–2.15 | The setting: frame, label, stanchions and rope, wall line, floor strokes, doorway | `T.d1` |
| 1.95–2.4 | Solid blacks ink in; signature fades in | `cartoon()` |
| 2.1–2.85 | Grey wash blooms region by region | `T.w1` |
| 2.95–3.45 | The beat ends: caption 1 fades in under the panel | `T.c1`, `CAP1` |
| 3.7–4.0 | The listener's brow lifts; it settles at 4.8–5.1 | `T.brow`, `groupsFor()` |
| 5.0–5.8 | The page turns on its spine to page 49 | `T.turn`, `pageTurn()` |
| 5.72–7.3 | Cartoon 2 draws: the speaker (now the woman), the man, the room (figures by 6.4) | `T.d2` |
| 7.25–7.95 | Wash; the lit windows are paper fills | `T.w2` |
| 7.95–8.45 | Caption 2 fades in | `T.c2`, `CAP2` |
| 8.45–8.7 | The speaker's brow lifts; it returns at 9.25–9.55 | `groupsFor()` |
| 8.5–9.62 | The listener's slow sip, glass at his lips 8.92–9.28 | `T.sip` |
| 9.55–10 | Fade to blank paper | `T.out` |

- A cartoon is one beat of about 4.5–5 s: draw (1.6–1.9 s), wash (0.7 s, overlapping the draw's end), a beat of silence (0.8 s after the line ends), caption, reaction 0.5–0.75 s later, a hold, then the page turn (0.8 s) hands over to the next.
- Reading pace: caption 1 is readable from 2.95 to the turn at 5.0, about 4 words a second for its 8 words; caption 2 has only 1.6 s before the fade, which is too short. A caption needs about 0.25 s per word, never less than 2 s, from its start to anything that removes it (a turn or the fade): 8 words 2 s, 10 words 2.5 s, 12 words 3 s. The reaction and the still hold fall inside that time: the viewer reads the line, then looks back at the picture it depends on.
- The demo never holds still at the end: the sip finishes at 9.62, inside the fade. A new film ends with nothing moving for at least 0.8 s before the fade.
- Reusable patterns: the page, the self-drawing panel, the wash bloom, the beat, the caption, one small reaction, the page turn, the paper fades. The museum, the party, the couples, the canvas, the drinks and both captions are one-off demo content.
- Review keys: render the original and your film with KEYS at the first reaction (4.05 in the demo), the turn at mid-page (5.4) and the sip with caption 2 (9.0); the default thirds (3.33, 6.67) catch neither reaction. In your own film add one key inside the final still hold, just before `T.out`.

## Sound
- audio.py reads a list of cues `{k, t, …}` and synthesizes everything with NumPy at 48 kHz stereo, `DUR` 10.0. Unknown kinds are skipped silently.
- Bed: a quiet room tone (band-passed noise at 0.012, the right channel delayed), written for the whole of `DUR` regardless of cues.
- Cue kinds and their fields:
  - `pen` {t, d}: a dip-pen scratch lasting `d` (at least 0.04 s), gain 0.035, panned at random within ±0.2. `window.events` sends one per stroke longer than 40 px, timed from the draw window, so short strokes are silent.
  - `wash` {t}: two soft brush swishes, 0.55 s and then 0.4 s a quarter-second later.
  - `beat` {t}: the punchline sting, a dry two-note double bass (55 Hz, then 41.2 Hz 0.2 s later), sent 0.05 s after each caption starts.
  - `turn` {t, d}: a paper flip with a slowing flutter over `d` (the demo sends the turn's length plus 0.1 s, starting 0.05 s early).
  - `party` {t, d}: a cocktail-party murmur over `d` with 0.8 s in and 0.6 s out, spread across the stereo field.
  - `step` {t}: a soft footstep, panned right; `clink` {t}: ice in a tumbler, two inharmonic strikes; `sip` {t}: a faint 0.3 s sip.
- Limits: `pen`, `turn` and `party` read `d` without a default, so a cue without it stops audio.py with a KeyError; a `d` of zero stops `turn` and `party` with a ValueError (an empty FFT), while `pen` clamps it. Every pan is fixed or random within ±0.5 and no cue field reaches it, so no value gives NaN; a cue past `DUR` is dropped silently.
- audio.py looks up no cue by name and runs with any subset, even none. A new film should send `pen` per stroke (automatic from the scenes), `wash` at each wash start, `beat` with each caption, `turn` with each page turn, and `party` for a crowded room; `step`, `clink` and `sip` only when the picture has footsteps or a glass. The demo's eyebrow has no sound: keep reactions silent or quieter than the caption sting.
- Nothing is written at fixed times in audio.py except the master: a 0.2 s fade-in, a 0.5 s fade-out at `DUR` and a tanh limiter. The fixed times live in `window.events`: `step` at 0.9 and 1.6 s and `party` at 5.3 s for 4.7 s; everything else follows `T`.

## Reuse map
| Piece | Where | Call / key params | Reuse |
|---|---|---|---|
| Paper, wash and ink textures | `anim.html` → `buildTextures` | built once in `window.ready`: `paperC`, `washPat`, `inkPat` from `noiseCanvas()` | as is |
| Magazine page | `buildPage()` | `buildPage(num)`: paper, running head, rule, folio `num`, panel border, spine shadow; cached in `pages` | adapt: magazine name, date, positions for 9:16 and 1:1 |
| Scene authoring | `newScene()`, `S()`, `WASHR()`, `FILL()`, `P()` | `S(d, w)` a pen stroke; `WASHR(d, tone, delay, rule)` a wash region; `FILL(d, col, rule)` a solid black (`INK`) or paper fill; `XF` (`a` mirror, `s` scale, `e`/`f` offsets) and `GRP` (animated group name) apply to the calls after them; `P(x, y)` gives an authored point under `XF` | as is |
| Path helpers | `crD()`, `limb()` | `crD(pts)` smooth path through points; `limb(pts, w0, w1, sides)` tapered tube: strokes its edges, returns its outline for `WASHR()` | as is |
| Pen line | `buildScene()` | `buildScene(sc, seed)` samples, wobbles, tapers and times every stroke; call once per scene in `window.ready` | as is |
| Cartoon renderer | `cartoon()` | `cartoon(c, sc, t, D, tw, tc, cap, sign)`: context, scene, draw window, wash start, caption time, caption, signature | as is; adapt the caption for two lines |
| Animated parts | `groupsFor()`, `rotAbout()` | one branch per scene (`sc === SC1`, else) returning a matrix per `GRP` name; pivots taken with `P()` into `CUR.bp`, `CUR.piv` | adapt: a branch per new scene |
| Figures | `manFace()`, `manNeck()`, `manSuit()`, `manLegs()`, `womanFace()`, `womanBody()`, `womanClutchArm()`, `womanMartiniArm()` | authored facing left at fixed coordinates (feet near y 645 and 652); place and mirror with `XF`; `manSuit(tone, delay)`, `womanBody(tone, delay, dressFill)` | adapt or replace |
| Page turn | `pageTurn()` | `pageTurn(u)`, u 0–1; caches the outgoing page once in `pg1`, from `pages` 47 and `SC1` at `T.turn` start | adapt: outgoing page, scene and caption; one cache per turn |
| Scenes, timeline, copy | `SC1`, `SC2`, `T`, `CAP1`, `CAP2` | | replace |
| Cues | `window.events` | `pen` per stroke from `T.d1`/`T.d2`, the rest from `T` except the literal `step` and `party` times; it also sends two cues audio.py ignores | adapt |

## Adapting
- **Style vs demo plot:**
  - Always the style: the magazine page with its running head, rule, folio and spine shadow; the ruled panel in wide paper margins; the dip-pen line drawing itself, speaker first; grey wash and one solid black; the signature in the panel's corner; the beat, then the quoted italic caption under the panel; one small reaction; the page turn between cartoons; fades from and to paper.
  - Demo plot, to replace: the museum and the party, both couples, the blank canvas, the drinks, the brow and the sip as particular gestures, both captions, *The Lamplight Review*, the date, folios 47 and 49, `'Ashby'`.
  - The transformation in a new film is the blank page becoming a finished cartoon and the caption changing how it reads, then the page turn to the next one; a single-cartoon film counts the draw-in plus the reaction.
- **New subject:** write the caption first and test it (Typography and copy), then draw the one picture it needs: who speaks, who listens, the odd thing in plain view, three to five props. Author new scenes with `S()`, `WASHR()` and `FILL()` under `XF`, tag the reacting part with `GRP`, add its branch to `groupsFor()`, and rename the magazine, date and cartoonist. Traps: break background lines behind figures; all solid blacks fade in together near the draw's end, wherever their outline came; `pageTurn()` and `window.events` name `SC1` and `SC2` directly; grep for decimal seconds after moving `T` (the `step` and `party` cues).
- **Length:** past 10 s add cartoons, one per page and about 4.5–5 s each: three in 15 s, four in 20. Beyond four the identical rhythm turns predictable; vary who speaks and what the reaction is, and let one cartoon hold longer. Each needs its scene and `buildScene()` call, a page from `buildPage()` with the next odd folio, a `groupsFor()` branch, a caption and a branch in `window.draw`. `pg1` caches only one outgoing page, so key the cache by turn or a second turn shows the first page again. In audio.py change only `DUR` (the bed and master follow it) and send `party` per crowded scene. Rendering grows linearly and is cheap.
- **Shorter:** a cartoon cannot be compressed much: the beat, the caption's reading time and the final hold are the joke. Two cartoons need about 9 s; at 8 s and below use one cartoon. Both plans were rendered (contact stills) and audio.py run:
  - 9 s, two cartoons, the demo's scenes untrimmed: `T.d1` 0.15–1.7 (12,960 px a second; the man takes 0.38 s, the woman 0.27 s), `T.w1` 1.65, `T.c1` 2.1, `T.brow` 2.6 (its settle at 3.7–4.0 ends before the turn), `T.turn` 4.1–4.8 (0.7 s, the demo's 0.8 shortened), `T.d2` 4.72–6.3 (the demo's 14,320; the woman takes 0.30 s, the man 0.38 s), `T.w2` 6.25, `T.c2` 6.7, `T.out` 8.7–9.0; drop the sip (`T.sip` past the end) and the second brow's return (delete the return factor of `brow2` in `groupsFor()`; scene 2's only gesture is then the speaker's `brow2`, against the listener rule in Motion: in your own film give that 0.25 s gesture to the listener), and send `party` at 4.6 for 4.4 s. Each 8-word caption gets 2.0 s; the second brow peaks at 7.45 and the frame is still for 1.25 s.
  - 4 s, one cartoon, scene 1 trimmed to about 14,700 px with lifts: cut the doorway and the picture beyond it, the frame's inner edge with its four mitre strokes, the two thin frame rules and the four thin skirting lines, and run the wall stroke that ends at x 1000 on to 1100. The frame still reads, its wash band marking the inner edge. Then fade 0–0.3, `T.d1` 0.1–1.3 (12,260 px a second; the man takes 0.41 s, the woman 0.29 s), `T.w1` 1.25, `T.c1` 1.7, `T.brow` 2.2 with no settle (delete the settle term in the scene-1 branch of `groupsFor()`), `T.out` 3.7–4.0, the other `T` entries past the end, no `party` cue. The caption gets 2.0 s, the reaction peaks at 2.5 and the frame is still for 1.2 s. This fits a caption of 8 words. A longer one must start earlier, so each extra word takes 0.25 s from the draw; the final hold cannot give it, because the hold lies inside the caption's time and grows when the caption starts earlier. Nine words is the most a 4 s film holds (rendered: the wall label, floor strokes, thin rope, the stanchions' second poles and two wall-line pieces also cut, `T.d1` 0.1–1.05, `T.c1` 1.45, `T.brow` 1.95; the caption gets 2.25 s and the hold 1.43 s, but the pen runs at 13,200 px a second and the woman takes 0.26 s, at the figure minimum). For a longer caption, lengthen the film. The page is there as the 0.3 s fade-in ends, with the pen already drawing; the whole signature is on screen by 2.2 s, 1.9 s after the fade-in.
  - Between 6 and 8 s use one cartoon and spend the extra time on a slower, untrimmed draw (up to the demo's 1.85 s), a longer caption hold and the reaction's settle. What goes first as the film shrinks: the second cartoon and its turn, then long gestures (the 1.1 s sip), then props; never the beat or the caption's reading time. Minimums from both plans: a beat of 0.4 s counted from the last pen stroke (in both plans the caption fades in over the last 0.3 s of the wash bloom, which reads fine; never start the caption while the pen is still drawing), 0.25 s per word and at least 2 s from a caption's start to anything that removes it, a still final hold of 0.8 s, and a pen no faster than the demo's 14,300 px a second with no figure under about 0.27 s. There is no title card to cut: the running head names the magazine at no cost in time.
  - A dropped cartoon can stay in the code: with its times past the end, `window.draw` never calls `pageTurn()` and its cues fall past `DUR`, where audio.py drops them. Set `DUR` in audio.py to the new length.
- **Other formats:** the page furniture and the 1:1 scene rescale directly (values in Composition). 9:16 needs the scene recomposed for a square panel and the caption broken into two lines; the figures, gestures and page turn stay inside the panel to the last frame. In `pageTurn()` replace the vertical centre `540 - 540 * s` with `H / 2 - H / 2 * s` for 9:16; 1:1 keeps 540.

## Boundaries
- **Distinct from:** `single-panel-absurd` (rural, animal and laboratory absurdity on a desk-calendar page, grey-green washes, a typed caption: the joke is the premise, not a social observation); `comic-strip` (four panels with balloons, a setup and a silent beat); `editorial-illustration` (colour, a visual metaphor and a headline, no gag caption); `minimal-strip` (trembling pen, four panels, gentle philosophy); `ink-wash` (sumi-e brush and colour washes, poetic, no caption).
- **Poor fit:** a joke that needs a setup and several beats or dialogue (`comic-strip`); workplace satire with buzzwords (`office-strip`); charts and numbers (`stick-webcomic`); action (`comic-book`); colour or brand palettes (`editorial-illustration`); animal or nature absurdity (`single-panel-absurd`); step-by-step explanation (`whiteboard`).
- **Do not:** copy a real magazine's name, masthead, typography, cartoonists, signatures or recurring characters, or write the name of the magazine that inspired the style anywhere visible. No colour, balloons, slapstick, puns or exclamation marks; never caption what the picture already shows.

## Technical notes
- No `render.json` and no `vendor/`: plain canvas 2D, no GPU. The film is `anim.html` with `fonts.css` and two fonts. Keep the hidden `<svg id="sv">` element: `buildScene()` measures every stroke through its path `sp`.
- Fast: 300 frames render in about 7 s at one worker (measured), events.mjs takes 0.6 s and audio.py 0.2 s, so a full build.sh is mostly the x264 `-preset slow` encode and the GIF. `window.ready` builds the full-frame paper noise pixel by pixel in JavaScript.
- Deterministic seeds: `buildScene()` seeds its wobble with `rng(101)` and `rng(202)`, textures use seeds 3, 5, 7 and 11.
- The first gradient fill on the main canvas (the turn's shadow in `pageTurn()`) changes how every later wash pattern fill is drawn, so a frame drawn after a turn frame differs from the same frame drawn alone (up to 15 levels in wash areas, PSNR about 54 dB) and the determinism test fails. Fix: one transparent gradient fill on `ctx` at the end of `window.ready`, after the pages are built:

```js
{ const g = ctx.createLinearGradient(0, 0, 10, 0); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); }
```

  With it every test frame matches exactly (rendered: 8.0 s alone and after 5.4 s, 9.0 s alone and after four earlier times, 2.6 s alone and in a run); wash areas shift by up to about 15 levels against the original, which does not show.
- Sizes hard-coded outside `W`/`H`: the canvas tag; `110`, `1810` and `1700` (running head and rule) and `960` and `1052` (folio) in `buildPage()`; `960` (caption x) in `cartoon()`; `540` (vertical centre) in `pageTurn()`; the vignette radii 500 and 1250, left unchanged in both rendered formats (9:16 has the same half-diagonal as 16:9; in 1:1 the corners darken to about 0.035 instead of 0.08, which still looked right). `PX`, `PY`, `PW`, `PH` drive the border, clip, signature and caption height, so a new panel moves those together.
- `groupsFor()` treats every scene that is not `SC1` as scene 2; `pageTurn()` hard-codes page 47, `SC1`, `T.d1`, `T.w1`, `T.c1`, `CAP1` and the signature for its cached image.
