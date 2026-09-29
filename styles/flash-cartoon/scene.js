// flash-cartoon · scenes, timeline and render (loaded after the symbol library in anim.html)
let LOADBG, STAGEBG, RAYS;

// ── precomputed backgrounds ──
function buildLoadBg() {
  const c = mk(W, H), x = c.getContext('2d');
  x.fillStyle = radial(x, W / 2, H * .45, 40, 1250, [[0, '#4a3a9e'], [.45, '#2a2166'], [1, '#0e0b2a']]); x.fillRect(0, 0, W, H);
  // faint dot grid, the kind of "tech" backdrop every preloader had
  x.fillStyle = 'rgba(255,255,255,.06)';
  for (let yy = 30; yy < H; yy += 48) for (let xx = 30 + (yy / 48 % 2) * 24; xx < W; xx += 48) { x.beginPath(); x.arc(xx, yy, 3, 0, TAU); x.fill(); }
  return c;
}
function buildStageBg() {
  const c = mk(W, H), x = c.getContext('2d');
  x.fillStyle = radial(x, 960, 560, 30, 1250, [[0, '#fff58a'], [.28, '#ffc234'], [.6, '#ff6a3d'], [1, '#c81f6a']]); x.fillRect(0, 0, W, H);
  return c;
}
function buildRays() {
  const S = 2600, c = mk(S, S), x = c.getContext('2d'), n = 18;
  x.translate(S / 2, S / 2); x.fillStyle = 'rgba(255,255,255,.17)';
  for (let i = 0; i < n; i++) { const a = i / n * TAU; x.beginPath(); x.moveTo(0, 0); x.arc(0, 0, S * .72, a, a + TAU / n / 2); x.closePath(); x.fill(); }
  return c;
}

// ── small reusable symbols ──
function star(x, cx, cy, r, rot, a = 1) {
  x.save(); x.globalAlpha *= a; x.translate(cx, cy); x.rotate(rot); x.beginPath();
  for (let i = 0; i < 10; i++) { const rr = i % 2 ? r * .45 : r, aa = -Math.PI / 2 + i * Math.PI / 5; i ? x.lineTo(Math.cos(aa) * rr, Math.sin(aa) * rr) : x.moveTo(Math.cos(aa) * rr, Math.sin(aa) * rr); }
  x.closePath(); x.fillStyle = radial(x, -r * .2, -r * .3, 1, r * 1.1, [[0, '#fffbd0'], [.5, '#ffe23a'], [1, '#ffaa12']]); x.fill(); strokeUniform(x, 6);
  x.restore();
}
function note(x, cx, cy, s, rot, a) {
  x.save(); x.globalAlpha *= a; x.translate(cx, cy); x.rotate(rot); x.scale(s, s);
  x.beginPath(); x.ellipse(-14, 30, 20, 14, -.4, 0, TAU); x.moveTo(2, 28); x.lineTo(2, -38); x.quadraticCurveTo(26, -28, 30, -6); x.quadraticCurveTo(20, -18, 8, -18); x.lineTo(8, 28); x.closePath();
  x.fillStyle = '#fff'; x.fill(); strokeUniform(x, 6);
  x.restore();
}
function cursor(x, cx, cy, down) {
  x.save(); x.translate(cx, cy); const s = down ? 1.18 : 1.3; x.scale(s, s);
  x.beginPath(); x.moveTo(0, 0); x.lineTo(0, 46); x.lineTo(11, 36); x.lineTo(19, 55); x.lineTo(27, 51); x.lineTo(19, 33); x.lineTo(33, 33); x.closePath();
  x.fillStyle = '#fff'; x.fill(); strokeUniform(x, 4, '#000');
  x.restore();
}
function outlinedText(x, s, px, py, size, fill, lw = 14, font = TITAN) {
  x.font = `${size}px ${font}`; x.textAlign = 'center'; x.textBaseline = 'middle'; x.lineJoin = 'round';
  x.lineWidth = lw; x.strokeStyle = INK; x.strokeText(s, px, py); x.fillStyle = fill; x.fillText(s, px, py);
}
function puff(x, cx, cy, u) {
  // dust puff, drawn frame-by-frame on 12 fps: three drawings
  const f = Math.min(2, Math.floor(u * 3));
  const r = [26, 40, 30][f], a = [1, .8, .45][f], d = [30, 70, 105][f];
  x.save(); x.globalAlpha = a; x.fillStyle = '#fff';
  for (const s of [-1, 1]) { x.beginPath(); x.arc(cx + s * (100 + d), cy - 10 - f * 8, r, 0, TAU); x.fill(); strokeUniform(x, 5);
    x.beginPath(); x.arc(cx + s * (150 + d * 1.2), cy - 4 - f * 4, r * .6, 0, TAU); x.fill(); strokeUniform(x, 5); }
  x.restore();
}

// ── loader + PRESS PLAY ──
const PCT = track([[.25, 0, 'out'], [.42, 11, 'hold'], [.66, 11, 'out'], [.8, 34, 'hold'], [1.04, 34, 'out'], [1.2, 67, 'hold'], [1.42, 67, 'out'], [1.5, 69, 'hold'], [1.68, 69, 'out'], [1.9, 100]]);
const PLAYC = [960, 500];
const playScale = track([[T.playIn, 0, 'back'], [T.playIn + .38, 1, 'hold'], [T.click - .04, 1, 'out'], [T.click + .04, .88, 'back'], [T.click + .2, 1.02]]);
const curX = track([[2.3, 1560, 'io'], [2.7, 1000]]), curY = track([[2.3, 1120, 'io'], [2.7, 540]]);
function drawLoader(t) {
  const x = ctx;
  x.drawImage(LOADBG, 0, 0);
  const out = seg(t, T.loadOut, T.loadOut + .28), ea = EASE.in(out);
  if (out < 1) {
    x.save(); x.globalAlpha = 1 - out;
    // studio ident
    const ly = 300 - ea * 120;
    outlinedText(x, 'SQUISHWORKS', 960, ly, 124, linear(x, 0, ly - 60, 0, ly + 60, [[0, '#fff27a'], [.5, '#ffc02e'], [1, '#ff7a1f']]), 18);
    x.font = `400 34px ${PIX}`; x.fillStyle = '#c8bff5'; x.textAlign = 'center'; x.fillText('A  VERY  IMPORTANT  CARTOON', 960, ly + 104);
    // loading bar
    const pct = Math.round(PCT(t)), bx = 580, by = 590, bw = 760, bh = 66, fw = bw * pct / 100;
    x.save(); x.translate(960, by + bh / 2); x.scale(1, 1 - ea); x.translate(-960, -(by + bh / 2));
    rrect(x, bx, by, bw, bh, 33); x.fillStyle = '#140f33'; x.fill();
    if (fw > 0) {
      x.save(); rrect(x, bx, by, bw, bh, 33); x.clip();
      x.fillStyle = linear(x, 0, by, 0, by + bh, [[0, '#d6ff7e'], [.5, '#7fe02c'], [1, '#3a9a12']]); x.fillRect(bx, by, fw, bh);
      x.beginPath(); x.rect(bx, by, fw, bh); x.clip();
      x.fillStyle = 'rgba(255,255,255,.22)'; const off = (t * 120) % 70;
      for (let s = bx - 140 + off; s < bx + fw + 70; s += 70) { x.beginPath(); x.moveTo(s, by + bh); x.lineTo(s + 34, by + bh); x.lineTo(s + 34 + 50, by); x.lineTo(s + 50, by); x.closePath(); x.fill(); }
      x.fillStyle = 'rgba(255,255,255,.4)'; rrect(x, bx + 14, by + 8, Math.max(0, fw - 28), 16, 8); x.fill();
      const flash = t > T.full ? Math.max(0, 1 - (t - T.full) / .12) : 0;
      if (flash) { x.fillStyle = `rgba(255,255,255,${flash})`; x.fillRect(bx, by, bw, bh); }
      x.restore();
    }
    rrect(x, bx, by, bw, bh, 33); strokeUniform(x, 7, '#fff');
    x.restore();
    // spinning loader icon: the hero symbol itself, reused at small scale
    const iconA = 1 - ea;
    x.save(); x.globalAlpha *= iconA;
    gloop(x, { x: 500, y: 655, s: .3, sx: 1, sy: 1, spin: -t * 5, armL: -.9, armR: -.9, mouth: 'o', look: [0, 0] });
    x.restore();
    x.font = `700 46px ${PIX}`; x.fillStyle = '#fff'; x.textAlign = 'center'; x.textBaseline = 'middle';
    const dots = '...'.slice(0, 1 + Math.floor(t * 4) % 3);
    x.fillText(pct >= 100 ? 'LOADED!' : `LOADING${dots.padEnd(3, ' ')} ${String(pct).padStart(2, ' ')}%`, 960, 730);
    x.restore();
  }
  if (t >= T.playIn) drawPlay(t);
}
function drawPlay(t) {
  const x = ctx, s = playScale(t), hover = t > 2.66;
  const [cx, cy] = PLAYC;
  x.save(); x.translate(cx, cy); x.scale(s, s);
  // drop shadow
  x.beginPath(); x.arc(8, 14, 180, 0, TAU); x.fillStyle = 'rgba(0,0,0,.35)'; x.fill();
  x.beginPath(); x.arc(0, 0, 180, 0, TAU);
  const pressed = t > T.click - .04 && t < T.click + .12;
  x.fillStyle = radial(x, -50, -70, 10, 240, pressed ? [[0, '#ffd08a'], [.5, '#ff7a1f'], [1, '#c2410a']] : hover ? [[0, '#fff2a8'], [.5, '#ffb23a'], [1, '#e2561a']] : [[0, '#ffe07a'], [.5, '#ff9a2a'], [1, '#d64c12']]);
  x.fill(); strokeUniform(x, 8);
  x.beginPath(); x.ellipse(-40, -95, 105, 46, -.15, 0, TAU); x.fillStyle = 'rgba(255,255,255,.45)'; x.fill();
  x.beginPath(); x.moveTo(-50, -80); x.lineTo(92, 0); x.lineTo(-50, 80); x.closePath(); x.fillStyle = '#fff'; x.fill(); strokeUniform(x, 8);
  x.restore();
  // label bobbing, pops in with a small delay (stagger)
  const la = seg(t, T.playIn + .16, T.playIn + .46), ls = EASE.back(la);
  if (la > 0) {
    x.save(); x.globalAlpha *= 1 - seg(t, T.click + .04, T.reveal + .08); x.translate(960, 780 + Math.sin(t * 7) * 8); x.scale(ls, ls);
    outlinedText(x, 'PRESS PLAY', 0, 0, 84, '#fff', 16);
    x.restore();
  }
  if (t > 2.3) cursor(x, curX(t), curY(t), pressed);
}

// ── stage ──
function bounceY(t, a, b, h) { const u = seg(t, a, b); return -h * Math.sin(Math.PI * u); }
function impulse(t, L, amp) { if (t < L) return 0; const d = t - L; return amp * Math.exp(-d * 8) * Math.cos(d * 26); }
const B = BEAT;
const HOPS = [[B(0) + .1, B(1), 960, 790, 150, -1], [B(1) + .1, B(2), 790, 1130, 170, 1], [B(2) + .1, B(3), 1130, 960, 130, -1]];
const CROUCH = [B(4), B(4) + .25], JUMP = [B(4) + .25, T.pose];
const LANDS = [T.land, B(1), B(2), B(3), T.pose];
const armLT = track([[3.2, .9, 'none'], [T.land, .9, 'out'], [B(0) + .2, -.95, 'io'], [B(0) + .3, -.95, 'io'], [B(1), 1.0, 'io'], [B(1) + .3, -.8, 'io'], [B(2), -.8, 'io'], [B(2) + .3, 1.1, 'io'], [B(3), 1.1, 'io'],
  [B(4), .6, 'out'], [CROUCH[1], -1.15, 'back'], [JUMP[0] + .15, .15, 'io'], [JUMP[1] - .08, .15, 'back'], [T.pose + .12, 1.15, 'hold'], [B(7) - .05, 1.15, 'io'], [B(7) + .25, -.95, 'io'], [7.5, -.95, 'back'], [7.75, -.15, 'hold'], [8.05, -.15, 'io'], [8.3, -.9]]);
const armRT = track([[3.2, .9, 'none'], [T.land, .9, 'out'], [B(0) + .2, -.95, 'io'], [B(0) + .3, -.95, 'io'], [B(1), -.8, 'io'], [B(1) + .3, 1.0, 'io'], [B(2), 1.0, 'io'], [B(2) + .3, 1.1, 'io'], [B(3), 1.1, 'io'],
  [B(4), .6, 'out'], [CROUCH[1], -1.15, 'back'], [JUMP[0] + .15, .15, 'io'], [JUMP[1] - .08, .15, 'back'], [T.pose + .12, 1.15, 'hold'], [B(7) - .05, 1.15, 'io'], [B(7) + .25, -.95, 'io'], [7.5, -.95, 'back'], [7.75, -.15, 'hold'], [8.05, -.15, 'io'], [8.3, -.9]]);
const GROUND = 930;
function heroParams(t) {
  const p = { x: 960, y: GROUND, s: 1.1, sx: 1, sy: 1, rot: 0, spin: 0, wob: 0, armL: armLT(t), armR: armRT(t), mouth: 'smile', eyes: 'open', look: [0, 0] };
  // drop in (ease-in fall, stretched)
  if (t < T.land) { const u = seg(t, T.drop, T.land); p.y = GROUND - 1300 * (1 - EASE.in(u)); p.sy = 1.18; p.sx = .88; p.eyes = 'wide'; p.mouth = 'o'; p.look = [0, 1]; }
  for (const [a, b, x0, x1, h, dir] of HOPS) {
    if (t >= a - .1 && t < a) { const u = seg(t, a - .1, a); p.sy *= 1 - .14 * Math.sin(Math.PI * u * .5); p.x = x0; }
    if (t >= a && t < b) { const u = seg(t, a, b); p.x = lerp(x0, x1, EASE.io(u)); p.y = GROUND + bounceY(t, a, b, h); p.rot = dir * .2 * Math.sin(Math.PI * u); p.sy *= 1 + .12 * Math.cos(Math.PI * u) ** 2; p.look = [dir, -.3]; p.mouth = 'grin'; }
    if (t >= b) p.x = x1;
  }
  // wiggle: fast lean + body wobble, face swaps drawings on 6 fps
  if (t >= B(3) && t < B(4)) { const u = seg(t, B(3), B(4)), env = Math.sin(Math.PI * u);
    p.rot = .17 * Math.sin((t - B(3)) * TAU * 4) * env; p.wob = 26 * Math.sin((t - B(3)) * TAU * 4 + 1) * env;
    p.armL = .35 + .7 * Math.sin((t - B(3)) * TAU * 4); p.armR = .35 - .7 * Math.sin((t - B(3)) * TAU * 4);
    p.mouth = Math.floor(t * 6) % 2 ? 'o' : 'grin'; p.eyes = Math.floor(t * 6) % 2 ? 'happy' : 'open'; }
  // crouch (anticipation) → spin jump → land on the downbeat
  if (t >= CROUCH[0] && t < CROUCH[1]) { const u = EASE.out(seg(t, CROUCH[0], CROUCH[1])); p.sy = 1 - .3 * u; p.sx = 1 + .22 * u; p.eyes = 'shut'; p.mouth = 'smile'; }
  if (t >= JUMP[0] && t < JUMP[1]) { const u = seg(t, JUMP[0], JUMP[1]); p.y = GROUND - 400 * Math.sin(Math.PI * u); p.spin = TAU * EASE.io(u); p.sy = 1 + .1 * Math.cos(Math.PI * u) ** 2; p.sx = 1 / p.sy; p.mouth = 'o'; p.eyes = 'wide'; }
  // landing squash impulses (scale bounce)
  for (const L of LANDS) { const k = L === T.pose ? .34 : .24; const im = impulse(t, L, k); p.sy *= 1 - im; p.sx *= 1 + im * .8; }
  if (t >= T.pose && t < B(7)) { p.mouth = 'open'; p.eyes = 'happy'; }
  if (t >= B(7)) { p.mouth = 'smile'; p.look = [0, 0]; }
  // talking: mouth drawings swap on 8 fps
  if (t >= T.bubble + .05 && t < T.bubble + .8) p.mouth = ['talk', 'smile', 'o', 'talk', 'smile'][Math.floor(t * 8) % 5];
  // blinks (2-frame drawings)
  for (const bt of [4.3, 7.5]) if (t >= bt && t < bt + .1) p.eyes = 'shut';
  if (t >= WINK[0] + .03 && t < WINK[1]) { p.wink = true; p.mouth = 'grin'; }
  return p;
}
function drawCrowd(t) {
  const tints = ['pink', 'cyan', 'tang', 'grape', 'cyan', 'pink', 'tang'];
  for (let i = 0; i < 7; i++) {
    const a = T.land + .05 + i * .06, u = seg(t, a, a + .35);
    if (u <= 0) continue;
    const cx = 170 + i * 263, bob = t > a + .35 ? -22 * Math.abs(Math.sin(Math.PI * (t - T.land) / T.beat)) : 0;
    const y = 1150 + bob + (1 - EASE.back(u)) * 230;
    const lean = .08 * Math.sin(Math.PI * (t - T.land) / T.beat) * (i % 2 ? 1 : -1);
    const cheer = t > T.pose && t < B(7) + .2;
    gloop(ctx, { x: cx, y, s: .55, sx: 1, sy: 1, rot: lean, armL: cheer ? 1.1 : .5 + .3 * Math.sin(t * 9 + i), armR: cheer ? 1.1 : .5 - .3 * Math.sin(t * 9 + i), tint: tints[i], mouth: cheer ? 'open' : 'smile', eyes: cheer ? 'happy' : 'open', look: [clamp((heroX - cx) / 600, -1, 1), -1] });
  }
}
let heroX = 960;
function drawNotes(t) {
  if (t < T.land + .2) return;
  for (let i = 0; i < 8; i++) {
    const per = 1.6, ph = (t - T.land - .2 + i * per / 8) / per; if (ph < 0) continue;
    const u = ph % 1, cyc = Math.floor(ph), side = i % 2 ? 1 : -1;
    if (t - T.land - .2 < 0) continue;
    const cx = 960 + side * (470 + ((i * 97 + cyc * 53) % 230)) + Math.sin(u * TAU) * 30;
    const cy = 900 - u * 620;
    note(ctx, cx, cy, .9 + (i % 3) * .2, .3 * Math.sin(u * TAU + i), Math.sin(Math.PI * u) * .9);
  }
}
function drawBurst(t) {
  const u = seg(t, T.pose, T.pose + .75); if (u <= 0 || u >= 1) return;
  const c = [heroX, GROUND - 180];
  for (let i = 0; i < 8; i++) {
    const a = i / 8 * TAU + .2, d = 170 + 260 * EASE.out(u), s = EASE.back(seg(u, 0, .35)) * (1 - seg(u, .7, 1));
    star(ctx, c[0] + Math.cos(a) * d, c[1] + Math.sin(a) * d * .8, 38 * s + .01, u * 4 + i, 1);
  }
}
function drawBubble(t) {
  const u = seg(t, T.bubble, T.bubble + .3); if (u <= 0 || t > T.bubbleOut + .12) return;
  const s = EASE.back(u) * (1 - EASE.in(seg(t, T.bubbleOut, T.bubbleOut + .12))), x = ctx, bx = 1330, by = 300, bh = 200;
  x.font = `62px ${TITAN}`; const bw = x.measureText("That's my one move.").width + 150;
  const tip = [heroX + 120, GROUND - 330];
  x.save(); x.translate(tip[0], tip[1]); x.scale(s, s); x.translate(-tip[0], -tip[1]);
  x.beginPath(); x.ellipse(bx, by, bw / 2, bh / 2, 0, 0, TAU);
  x.moveTo(bx - 170, by + 60); x.quadraticCurveTo(bx - 190, by + 150, tip[0], tip[1]); x.quadraticCurveTo(bx - 110, by + 120, bx - 90, by + 86);
  x.fillStyle = '#fff'; x.fill(); strokeUniform(x, 8);
  x.beginPath(); x.ellipse(bx, by, bw / 2 - 4, bh / 2 - 4, 0, 0, TAU); x.fillStyle = '#fff'; x.fill();
  x.font = `62px ${TITAN}`; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = INK; x.fillText("That's my one move.", bx, by + 4);
  x.restore();
}
const raysRot = t => t * .22;
function drawStage(t) {
  const x = ctx;
  x.drawImage(STAGEBG, 0, 0);
  x.save(); x.translate(960, 560); x.rotate(raysRot(t)); x.drawImage(RAYS, -RAYS.width / 2, -RAYS.height / 2); x.restore();
  // stage disc
  x.beginPath(); x.ellipse(960, GROUND + 30, 760, 120, 0, 0, TAU); x.fillStyle = linear(x, 0, GROUND - 90, 0, GROUND + 150, [[0, '#a65cf0'], [.5, '#6a24b8'], [1, '#3e1277']]); x.fill(); strokeUniform(x, 8);
  x.beginPath(); x.ellipse(960, GROUND + 6, 690, 82, 0, 0, TAU); x.fillStyle = 'rgba(255,255,255,.14)'; x.fill();
  drawNotes(t);
  const p = heroParams(t); heroX = p.x;
  // contact shadow shrinks as the hero leaves the floor
  const hgt = clamp((GROUND - p.y) / 500);
  x.beginPath(); x.ellipse(p.x, GROUND + 4, 150 * (1 - .5 * hgt), 26 * (1 - .5 * hgt), 0, 0, TAU); x.fillStyle = `rgba(40,0,70,${.45 * (1 - .6 * hgt)})`; x.fill();
  for (const L of LANDS) { const u = seg(t, L, L + .25); if (u > 0 && u < 1) puff(x, HOPX(L), GROUND + 8, u); }
  gloop(x, p);
  drawBurst(t);
  drawBubble(t);
  drawCrowd(t);
  drawBanner(t);
}
const banY = track([[3.4, -170, 'elastic'], [4.3, 110, 'hold'], [6.95, 110, 'back'], [7.25, -190]]);
const banR = track([[3.4, -.25, 'elastic'], [4.3, 0]]);
function drawBanner(t) {
  if (t < 3.4 || t > 7.25) return;
  const x = ctx, y = banY(t), txt = "GLOOP'S BIG DANCE";
  x.save(); x.translate(960, y); x.rotate(banR(t));
  x.font = `72px ${TITAN}`; const w = x.measureText(txt).width + 120, h = 116;
  // ribbon tails (reused symbol, mirrored)
  for (const sd of [-1, 1]) {
    x.save(); x.scale(sd, 1);
    x.beginPath(); x.moveTo(w / 2 - 40, -h / 2 + 26); x.lineTo(w / 2 + 110, -h / 2 + 26); x.lineTo(w / 2 + 70, 22); x.lineTo(w / 2 + 110, h / 2 + 22); x.lineTo(w / 2 - 40, h / 2 + 22); x.closePath();
    x.fillStyle = '#b8175e'; x.fill(); strokeUniform(x, 7); x.restore();
  }
  rrect(x, -w / 2, -h / 2, w, h, 26);
  x.fillStyle = linear(x, 0, -h / 2, 0, h / 2, [[0, '#ff8cc6'], [.5, '#ff3f93'], [1, '#d01f6c']]); x.fill(); strokeUniform(x, 8);
  rrect(x, -w / 2 + 20, -h / 2 + 10, w - 40, 30, 15); x.fillStyle = 'rgba(255,255,255,.35)'; x.fill();
  outlinedText(x, txt, 0, 6, 72, '#fff', 14);
  x.restore();
}
const HOPX = L => L < B(1) ? 960 : L < B(2) ? 790 : L < B(3) ? 1130 : 960;

// ── cartoon iris-out on the hero's face, with the classic hold + wink ──
const WINK = [T.irisA + .3, T.irisB - .15];
const irisR = track([[T.irisA, 1500, 'io'], [WINK[0], 190, 'hold'], [WINK[1], 190, 'in'], [T.irisB, 0]]);
function drawIris(t) {
  const r = irisR(t), x = ctx, c = [heroX, GROUND - 190];
  x.save(); x.beginPath(); x.rect(0, 0, W, H); x.arc(c[0], c[1], Math.max(0, r), 0, TAU, true); x.fillStyle = '#0a0616'; x.fill('evenodd');
  if (r > 0) { x.beginPath(); x.arc(c[0], c[1], r, 0, TAU); strokeUniform(x, 8, '#0a0616'); }
  x.restore();
  const wu = seg(t, WINK[0] + .03, WINK[0] + .2);
  if (wu > 0 && t < WINK[1]) star(x, c[0] + 150, c[1] - 120, 30 * EASE.back(wu) + .01, wu * 2, 1);
}

// ── REPLAY? end screen ──
const repS = track([[T.endIn + .06, 0, 'back'], [T.endIn + .42, 1, 'hold'], [T.hover - .02, 1, 'back'], [T.hover + .2, 1.06]]);
const cur2X = track([[9.05, 520, 'io'], [T.hover, 800]]), cur2Y = track([[9.05, 1150, 'io'], [T.hover, 600]]);
function drawReplay(t) {
  const x = ctx;
  x.drawImage(LOADBG, 0, 0);
  const s = repS(t), hov = t >= T.hover - .02, cx = 960, cy = 540;
  // the hero symbol pops up from behind the button (drawn first so the button hides its feet)
  const pu = seg(t, T.endIn + .3, T.endIn + .65);
  if (pu > 0) gloop(x, { x: 1200, y: 470 + (1 - EASE.back(pu)) * 200 - (t > T.endIn + .65 ? 8 * Math.abs(Math.sin((t - T.endIn) * 7)) : 0), s: .5, sx: 1, sy: 1, rot: -.08, armL: .2, armR: 1.1, mouth: 'grin', eyes: t > 9.3 && t < 9.4 ? 'shut' : 'open', look: [-.6, .4], armsBehind: true });
  x.save(); x.translate(cx, cy); x.scale(s, s);
  rrect(x, -380 + 10, -95 + 16, 760, 190, 95); x.fillStyle = 'rgba(0,0,0,.4)'; x.fill();
  rrect(x, -380, -95, 760, 190, 95);
  x.fillStyle = linear(x, 0, -95, 0, 95, hov ? [[0, '#fff2a8'], [.45, '#ffb23a'], [1, '#e2561a']] : [[0, '#ffe07a'], [.45, '#ff9a2a'], [1, '#d64c12']]); x.fill(); strokeUniform(x, 8);
  rrect(x, -335, -80, 670, 62, 31); x.fillStyle = 'rgba(255,255,255,.42)'; x.fill();
  // circular arrow icon
  x.beginPath(); x.arc(-295, 4, 42, -.4, Math.PI * 1.45); x.lineWidth = 20; x.strokeStyle = INK; x.lineCap = 'round'; x.stroke(); x.lineWidth = 11; x.strokeStyle = '#fff'; x.stroke();
  x.save(); x.translate(-295 + Math.cos(-.4) * 42, 4 + Math.sin(-.4) * 42); x.rotate(-.4 + Math.PI / 2 - .3);
  x.beginPath(); x.moveTo(-20, -10); x.lineTo(20, -10); x.lineTo(0, 22); x.closePath(); x.fillStyle = '#fff'; x.fill(); strokeUniform(x, 6); x.restore();
  outlinedText(x, 'REPLAY?', 82, 8, 112, '#fff', 16);
  x.restore();
  const su = seg(t, T.endIn + .4, T.endIn + .6);
  if (su > 0) { x.save(); x.globalAlpha = su; x.font = `400 40px ${PIX}`; x.fillStyle = '#d9d2ff'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText("(IT'S THE SAME MOVE)", 960, 740 + (1 - EASE.out(su)) * 30); x.restore(); }
  if (t > 9.05) cursor(x, cur2X(t), cur2Y(t), false);
}

// ── master render ──
function render(t) {
  const x = ctx; x.setTransform(1, 0, 0, 1, 0, 0); x.globalAlpha = 1;
  if (t < T.irisB + .02) {
    if (t < T.revealEnd) drawLoader(t);
    if (t >= T.reveal) {
      const u = seg(t, T.reveal, T.revealEnd), r = 180 * playScale(t) + 1500 * EASE.in(u);
      x.save(); if (u < 1) { x.beginPath(); x.arc(PLAYC[0], PLAYC[1], r, 0, TAU); x.clip(); }
      drawStage(t); x.restore();
      if (u < 1) { x.beginPath(); x.arc(PLAYC[0], PLAYC[1], r, 0, TAU); strokeUniform(x, 22 * (1 - u) + 4, '#fff'); }
    }
    if (t >= T.irisA) drawIris(t);
  } else x.fillStyle = '#0a0616', x.fillRect(0, 0, W, H);
  if (t >= T.endIn) { const a = seg(t, T.endIn, T.endIn + .1); x.save(); x.globalAlpha = a; drawReplay(t); x.restore(); }
  const fade = Math.max(1 - seg(t, 0, T.loadA), seg(t, T.fadeA, T.fadeB));
  if (fade > 0) { x.fillStyle = `rgba(5,3,12,${EASE.io(fade)})`; x.fillRect(0, 0, W, H); }
}

window.ready = (async () => {
  await Promise.all([`100px ${TITAN}`, `400 40px ${PIX}`, `700 40px ${PIX}`].map(f => document.fonts.load(f, "SQUISHWORKS LOADING... 100% PRESS PLAY REPLAY? That's my one move. (IT'S THE SAME MOVE) A VERY IMPORTANT CARTOON")));
  await document.fonts.ready;
  LOADBG = buildLoadBg(); STAGEBG = buildStageBg(); RAYS = buildRays();
  render(0);
})();
window.draw = ({ t }) => { render(t); return cv.toDataURL('image/jpeg', 0.92).split(',')[1]; };
// audio cue list (read by events.mjs → events.json → audio.py)
window.events = () => {
  const ev = [];
  for (const k of [.42, .8, 1.2, 1.5, 1.9]) ev.push({ t: k - .1, k: 'blip', v: k === 1.9 ? 1 : .6 });
  ev.push({ t: T.full, k: 'ding' });
  ev.push({ t: T.playIn, k: 'pop', v: 1 }, { t: T.playIn + .16, k: 'pop', v: .6 });
  ev.push({ t: T.click, k: 'click' }, { t: T.reveal, k: 'whoosh', d: .5 });
  ev.push({ t: T.drop, k: 'fall', d: T.land - T.drop });
  for (const L of LANDS) ev.push({ t: L, k: 'boing', v: L === T.pose ? 1 : L === T.land ? .9 : .6 });
  for (let i = 0; i < 7; i++) ev.push({ t: T.land + .05 + i * .06, k: 'pop', v: .35 });
  ev.push({ t: CROUCH[1], k: 'whoosh', d: JUMP[1] - JUMP[0] });
  ev.push({ t: T.pose, k: 'sparkle' });
  ev.push({ t: T.land, k: 'music', beat: T.beat, bars: 1.75 });
  ev.push({ t: T.bubble, k: 'pop', v: .8 }, { t: T.bubble + .05, k: 'gibber', d: .75 });
  ev.push({ t: T.irisA, k: 'iris' }, { t: WINK[0] + .03, k: 'ting' }, { t: WINK[1], k: 'iris2' });
  ev.push({ t: T.endIn + .06, k: 'pop', v: 1 }, { t: T.endIn + .3, k: 'boing', v: .4 }, { t: T.endIn + .06, k: 'jingle' });
  ev.push({ t: T.hover, k: 'hover' });
  return ev.sort((a, b) => a.t - b.t);
};
