# Reviewing a film

Judge the frames, not the code. After every render, open `_review/sheet.jpg` and both key frames at full size,
next to the original's `_reference/original-sheet.jpg`. If you cannot view images, ask the user to compare
them and tell you what they see; do not skip the review. Write down concrete defects (what, where, at what
time), fix them, render again. Do at least two passes; stop when a fresh look finds nothing worth fixing.

## Does it read as the style?
- The recipe's **Signature** items are on screen within the first 3 seconds.
- Palette, type, texture, line and motion follow the recipe; nothing from a neighbouring style crept in.
- Side by side with the original sheet, a viewer would call it the same style, even though the subject differs.

## Is it a good film?
- One focus at a time and a deliberate composition; the eye knows where to go in every frame.
- Text is readable at full size: nothing clipped, overlapping, too small or too close to the edge. For 9:16
  social formats keep key text out of the top ~15%, the bottom ~25% and the right ~12%, where Reels, Shorts
  and TikTok put captions and buttons.
- Motion has intent: anticipation, overshoot and stagger where the style calls for them, and none where the
  recipe rules them out.
- At least one scene change or transformation.
- A beginning and an ending: open on purpose; close on a settle, fade or final pose, holding the final state
  for at least 0.8 s. Never a hard cut on the last frame.
- People read clearly: a head with a readable profile, neck and shoulders, torso, jointed limbs and hands,
  even as a silhouette. If a figure cannot be drawn well, tell the story with objects or animals.
- The brief lands: the film explains, sells or tells what the user asked for.

## Content rules
- A style "inspired by" a creator borrows the visual language and tone only: never their characters, mascots,
  logos, lettering fonts or signature jokes.
- Cultural styles respect the tradition's visual grammar: no sacred or religious iconography as decoration,
  no invented script pretending to be a real language.
- Real brands, logos, products and people appear only when the user owns or supplies them.

## Technical checks
- The duration ffprobe prints at the end of build.sh matches the plan (see "Duration: three places" in
  contract.md), at 30 fps, with an audio stream.
- Determinism: draw one moment alone and again after other frames, then compare, inside the project folder:
  `node render.mjs _review/det-a 30 0 10 1 4.2`, `node render.mjs _review/det-b 30 0 10 1 0.5,2,4.2`,
  `cmp _review/det-a/t_4.20.jpg _review/det-b/t_4.20.jpg`. The files must be identical (render.mjs draws the
  times in order, so run b reaches 4.2 after other frames). A difference means an unseeded random number, a
  clock or state carried between frames crept in.
- Every character on screen renders in the intended font (missing glyphs show as boxes or a fallback face).
