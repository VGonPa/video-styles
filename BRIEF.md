# Style catalog — a short showcase clip for each animation style

This is an English adaptation of the [original Turkish production brief](https://github.com/yasinozmeen/animasyon-stil-katalogu/blob/main/BRIEF.md). The original project was made for Yasin’s Turkish speaking-practice site and YouTube channel, irticalen.

Create a complete 8–10 second short film for each style. Each film should show that style at its best. There is no shared story: choose a subject that demonstrates the style’s strengths. A small idea from the irticalen world can help (a speech bubble, countdown, topic wheel, microphone, improvised speech, or words), but it is optional.

The viewer should recognize the style within three seconds. Show its signature texture, motion, color, typography, and transitions clearly.

## Quality bar

- Aim for studio-quality work: one focus, deliberate composition, smooth and meaningful motion (anticipation, overshoot, and stagger), and at least one scene transformation or transition.
- Show the strongest version of the style without relying on clichés.
- Draw human figures carefully, especially proportions and hands, or tell the story without figures when the style permits.
- Use English for visible text. Choose fonts that include every required character. Do not use stock images, photos of real people, or third-party brand logos.
- Give each clip its own beginning and ending. Avoid an abrupt cut on the final frame.

## Technical contract

- Put each style in its own directory under `styles/<slug>/`. Its `anim.html` must draw on a 1920 × 1080 canvas. `window.draw({t})` returns the frame at time `t` as base64 JPEG data from `toDataURL('image/jpeg', 0.92)`. `window.ready` waits for fonts and textures. Render the final video as H.264, 30 fps, yuv420p, CRF 18.
- Use the style’s `render.mjs` or the root `render_example.mjs` as a frame renderer. Render at most two browser pages in parallel if memory is constrained. Store intermediate frames as JPEG and remove them after encoding.
- Generate expensive textures, grain, and blur effects once in an offscreen canvas rather than on every frame.
- Audio is optional. If a clip has no sound, add a silent stereo AAC track so the catalog can concatenate all clips. Short synthesized clicks, pops, beeps, or chalk-like sounds are suitable where needed.
- Check each clip with a contact sheet and at least one full-resolution frame from a key moment. Make at least one correction pass.

## Per-style report

For each style, record its slug, the clip’s subject in one sentence, the style features it shows, any known defects, and the output path.
