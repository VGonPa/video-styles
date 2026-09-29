// ── kawaii · a "Good morning!" breakfast routine with chibi food friends ───────────────────────────
// Mint morning over a pink gingham table: the title pops in letter by letter, four sleepy breakfast
// characters (a rice ball, a toast slice, a strawberry milk carton, a sunny egg) hop in with squash and
// stretch, stretch and wake with sparkles, wiggle → a sparkle-burst wipe to a butter-yellow sunburst →
// two pairs high-five, each friend launches a sticker letter to spell "YAY!", heart confetti rains →
// a heart iris closes on the group → "Have a sweet day!" hold.
const W = 1920, H = 1080, TAU = Math.PI * 2;
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eOut = u => 1 - Math.pow(1 - u, 3);
const eIn = u => u * u * u;
const eInOut = u => u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
const eBack = (u, s = 2.2) => { const c3 = s + 1; return 1 + c3 * Math.pow(u - 1, 3) + s * Math.pow(u - 1, 2); };
const bell = u => (u <= 0 || u >= 1) ? 0 : Math.sin(Math.PI * u);
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const mk = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };

// ── palette ──
const INK = '#5a3940', WHITE = '#ffffff', SHADOW = 'rgba(96,56,86,.16)';
const MINT = '#c6efdc', MINT_D = '#9fdcc3', PEACH = '#ffc9a8', LAV = '#d9c9f7', LAV_D = '#bca6ee', BUTTER = '#fff0b3', PINK = '#ffb3c9', PINK_D = '#ff8fb0';
const DISP = '"Mochiy Pop One"', ROUND = '"Sniglet"';
const OUT = 7, BOR = 15, Y0 = 905, S = 1.08;

// ── timeline ──
const T = { fadeIn: [0, .35], title0: .3, titleOut: 3.4, wipe: [3.9, 4.55], hf1: 4.95, hf2: 5.3, yay: 5.95, iris: [8.55, 9.3], heart: 9.3, fadeOut: [9.65, 10] };

// ── helpers: paths ──
function roundPoly(pts, r) {
  const p = new Path2D(), n = pts.length;
  const m = [(pts[n - 1][0] + pts[0][0]) / 2, (pts[n - 1][1] + pts[0][1]) / 2]; p.moveTo(m[0], m[1]);
  for (let i = 0; i < n; i++) { const a = pts[i], b = pts[(i + 1) % n]; p.arcTo(a[0], a[1], b[0], b[1], r); }
  p.closePath(); return p;
}
function rrect(x, y, w, h, r) { const p = new Path2D(); p.roundRect(x, y, w, h, r); return p; }
function ellipse(x, y, rx, ry, rot = 0) { const p = new Path2D(); p.ellipse(x, y, rx, ry, rot, 0, TAU); return p; }
function heartPath(cx, cy, s) {              // s = half-width
  const p = new Path2D(); const k = s / 16;
  for (let i = 0; i <= 80; i++) { const a = i / 80 * TAU; const x = 16 * Math.pow(Math.sin(a), 3); const y = -(13 * Math.cos(a) - 5 * Math.cos(2 * a) - 2 * Math.cos(3 * a) - Math.cos(4 * a));
    i ? p.lineTo(cx + x * k, cy + y * k + s * .1) : p.moveTo(cx + x * k, cy + y * k + s * .1); }
  p.closePath(); return p;
}
function sparklePath(cx, cy, r, rot = 0, pinch = .22) {
  const p = new Path2D();
  for (let i = 0; i < 4; i++) {
    const a = rot + i * TAU / 4, b = a + TAU / 8, a2 = a + TAU / 4;
    const x0 = cx + Math.cos(a) * r, y0 = cy + Math.sin(a) * r, cxp = cx + Math.cos(b) * r * pinch, cyp = cy + Math.sin(b) * r * pinch;
    if (!i) p.moveTo(x0, y0); p.quadraticCurveTo(cxp, cyp, cx + Math.cos(a2) * r, cy + Math.sin(a2) * r);
  }
  p.closePath(); return p;
}
function starPath(cx, cy, r, rot = 0, inner = .5, n = 5) {
  const p = new Path2D();
  for (let i = 0; i < n * 2; i++) { const a = rot - Math.PI / 2 + i * Math.PI / n, rr = i % 2 ? r * inner : r; i ? p.lineTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr) : p.moveTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr); }
  p.closePath(); return p;
}
// sticker drawing: 'shadow' / 'white' passes build the union silhouette border, 'ink' draws fill + outline
let MODE = 'ink';
function shape(path, fill, outline = true) {
  if (MODE === 'ink') { ctx.fillStyle = fill; ctx.fill(path); if (outline) { ctx.lineWidth = OUT; ctx.strokeStyle = INK; ctx.lineJoin = 'round'; ctx.stroke(path); } return; }
  ctx.fillStyle = ctx.strokeStyle = MODE === 'white' ? WHITE : SHADOW; ctx.lineJoin = 'round'; ctx.lineWidth = OUT + 2 * BOR; ctx.fill(path); ctx.stroke(path);
}
function detail(fn) { if (MODE === 'ink') fn(); }
function stroked(path, w, col) {         // tube (arm / straw)
  ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  if (MODE !== 'ink') { ctx.strokeStyle = MODE === 'white' ? WHITE : SHADOW; ctx.lineWidth = w + OUT + 2 * BOR; ctx.stroke(path); return; }
  ctx.strokeStyle = INK; ctx.lineWidth = w + OUT; ctx.stroke(path); ctx.strokeStyle = col; ctx.lineWidth = w - OUT; ctx.stroke(path);
}
function sticker(draw, dx = 7, dy = 11) {       // run a draw fn in the three passes
  ctx.save(); ctx.translate(dx, dy); MODE = 'shadow'; draw(); ctx.restore();
  MODE = 'white'; draw(); MODE = 'ink'; draw();
}

// ── faces ──
function face(fx, fy, ex, bx, P, sc = 1) {
  ctx.save(); ctx.translate(fx, fy); ctx.scale(sc, sc);
  const lx = P.look ? P.look[0] : 0, ly = P.look ? P.look[1] : 0;
  // blush
  ctx.fillStyle = 'rgba(255,128,160,.55)';
  for (const s of [-1, 1]) { ctx.beginPath(); ctx.ellipse(s * bx, 22, 19, 11, 0, 0, TAU); ctx.fill(); }
  ctx.strokeStyle = 'rgba(255,255,255,.8)'; ctx.lineWidth = 2.5; ctx.lineCap = 'round';
  for (const s of [-1, 1]) for (const d of [-6, 1, 8]) { ctx.beginPath(); ctx.moveTo(s * bx + d, 18); ctx.lineTo(s * bx + d - 3, 25); ctx.stroke(); }
  // eyes
  ctx.fillStyle = INK; ctx.strokeStyle = INK; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  const blink = P.blink || 0;
  for (const s of [-1, 1]) {
    const x = s * ex + lx, y = ly;
    if (P.eyes === 'sleep') { ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(x, y - 4, 11, .25 * Math.PI, .75 * Math.PI); ctx.stroke(); }
    else if (P.eyes === 'happy') { ctx.lineWidth = 7; ctx.beginPath(); ctx.arc(x, y + 6, 12, 1.15 * Math.PI, 1.85 * Math.PI); ctx.stroke(); }
    else {
      const big = P.eyes === 'wow' ? 1.35 : 1, ry = 15 * big * (1 - .9 * blink), rx = 12 * big;
      if (ry < 3) { ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(x - 10, y); ctx.lineTo(x + 10, y); ctx.stroke(); continue; }
      ctx.beginPath(); ctx.ellipse(x, y, rx, ry, 0, 0, TAU); ctx.fill();
      ctx.fillStyle = WHITE; ctx.beginPath(); ctx.arc(x + 4 * big, y - 5 * big * (1 - blink), 4.6 * big, 0, TAU); ctx.fill();
      if (big > 1) { ctx.beginPath(); ctx.arc(x - 5, y + 7, 2.6, 0, TAU); ctx.fill(); }
      ctx.fillStyle = INK;
    }
  }
  // mouth
  const m = P.mouth || 'smile'; ctx.lineWidth = 5.5;
  if (m === 'smile') { ctx.beginPath(); ctx.arc(0, 12, 9, .15 * Math.PI, .85 * Math.PI); ctx.stroke(); }
  else if (m === 'w') { ctx.beginPath(); ctx.arc(-6.5, 14, 6.5, .1 * Math.PI, .95 * Math.PI); ctx.moveTo(13, 14.5); ctx.arc(6.5, 14, 6.5, .05 * Math.PI, .9 * Math.PI); ctx.stroke(); }
  else if (m === 'yawn') { ctx.fillStyle = '#b24a5c'; ctx.beginPath(); ctx.ellipse(0, 20, 8, 11 * (P.mo || 1), 0, 0, TAU); ctx.fill(); ctx.stroke(); }
  else if (m === 'flat') { ctx.beginPath(); ctx.moveTo(-6, 16); ctx.lineTo(6, 16); ctx.stroke(); }
  else if (m === 'open') {
    ctx.fillStyle = '#b24a5c'; ctx.beginPath(); ctx.moveTo(-15, 10); ctx.quadraticCurveTo(0, 12, 15, 10); ctx.quadraticCurveTo(14, 34, 0, 34); ctx.quadraticCurveTo(-14, 34, -15, 10); ctx.closePath(); ctx.fill();
    ctx.save(); ctx.clip(); ctx.fillStyle = '#ff8ea4'; ctx.beginPath(); ctx.ellipse(0, 34, 10, 8, 0, 0, TAU); ctx.fill(); ctx.restore(); ctx.stroke();
  }
  ctx.restore();
}

// ── characters (local coords: feet at y = 0, unscaled) ──
const armPath = (x, y, a, side, len = 46) => { const p = new Path2D(); p.moveTo(x, y); p.lineTo(x + side * Math.cos(a) * len, y - Math.sin(a) * len); return p; };
function limbs(P, sh, col, footX, aw = 30) {
  for (const s of [-1, 1]) shape(ellipse(s * footX, -6, 25, 15), col);
  stroked(armPath(-sh[0], sh[1], P.armL, -1), aw, col);
  stroked(armPath(sh[0], sh[1], P.armR, 1), aw, col);
}
const ONI_BODY = roundPoly([[0, -250], [-158, -8], [158, -8]], 64);
const ONI_NORI = rrect(-64, -80, 128, 78, 12);
function drawOnigiri(P) {
  limbs(P, [100, -62], '#fffaf0', 50);
  shape(ONI_BODY, '#fffaf0');
  detail(() => {
    ctx.save(); ctx.clip(ONI_BODY); ctx.fillStyle = '#f1e7d4';
    for (const [x, y, r] of [[-52, -168, .5], [44, -182, -.4], [-86, -54, .2], [92, -60, -.3], [8, -212, .1], [70, -110, .7], [-78, -104, -.6]]) { ctx.beginPath(); ctx.ellipse(x, y, 9, 5, r, 0, TAU); ctx.fill(); }
    ctx.restore();
    shape(ONI_NORI, '#34433e');
    ctx.strokeStyle = 'rgba(255,255,255,.22)'; ctx.lineWidth = 5; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(-46, -64); ctx.lineTo(-46, -22); ctx.stroke();
    face(0, -140, 33, 60, P);
  });
}
const TOAST_BODY = (() => { const p = new Path2D(); p.moveTo(0, 0); p.lineTo(-88, 0); p.quadraticCurveTo(-110, 0, -110, -22); p.lineTo(-112, -172); p.bezierCurveTo(-168, -182, -162, -290, -62, -290); p.quadraticCurveTo(0, -304, 62, -290); p.bezierCurveTo(162, -290, 168, -182, 112, -172); p.lineTo(110, -22); p.quadraticCurveTo(110, 0, 88, 0); p.closePath(); return p; })();
const TOAST_IN = (() => { const p = new Path2D(); const m = new DOMMatrix().translate(0, -146).scale(.8, .8).translate(0, 146); p.addPath(TOAST_BODY, m); return p; })();
function drawToast(P) {
  limbs(P, [104, -108], '#e8a45e', 46);
  shape(TOAST_BODY, '#e8a45e');
  detail(() => {
    ctx.fillStyle = '#ffe4a9'; ctx.fill(TOAST_IN); ctx.strokeStyle = '#d99250'; ctx.lineWidth = 3; ctx.stroke(TOAST_IN);
    ctx.fillStyle = '#f3d08e'; for (const [x, y] of [[-60, -60], [52, -48], [-20, -36], [70, -200], [-74, -214]]) { ctx.beginPath(); ctx.arc(x, y, 4, 0, TAU); ctx.fill(); }
  });
  ctx.save(); ctx.translate(40, -244); ctx.rotate(-.14 + (P.butter || 0)); shape(rrect(-36, -24, 72, 46, 12), '#fff3a1');
  detail(() => { ctx.strokeStyle = WHITE; ctx.lineWidth = 5; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(-22, -12); ctx.lineTo(-6, -12); ctx.stroke(); }); ctx.restore();
  detail(() => face(0, -150, 34, 64, P));
}
const MILK_ROOF = (() => { const p = new Path2D(); p.moveTo(-94, -234); p.lineTo(-62, -308); p.lineTo(62, -308); p.lineTo(94, -234); p.closePath(); return p; })();
const MILK_FIN = rrect(-68, -330, 136, 26, 7), MILK_BODY = rrect(-98, -238, 196, 238, 22), MILK_LABEL = rrect(-72, -104, 144, 82, 18);
function drawMilk(P) {
  const st = new Path2D(); st.moveTo(30, -318); st.lineTo(40, -390); st.lineTo(80, -414);
  stroked(st, 22, '#cdb6fa');
  limbs(P, [92, -122], '#ffb6cc', 44);
  shape(MILK_FIN, '#ffd6e3'); shape(MILK_ROOF, '#fff1f6'); shape(MILK_BODY, '#ffb6cc');
  detail(() => {
    ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = 7; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(-76, -214); ctx.lineTo(-76, -130); ctx.stroke();
    shape(MILK_LABEL, '#fffafc');
    // tiny strawberry
    ctx.save(); ctx.translate(-42, -62); ctx.scale(.85, .85); const sb = new Path2D(); sb.moveTo(0, 22); sb.bezierCurveTo(-26, 4, -22, -16, 0, -14); sb.bezierCurveTo(22, -16, 26, 4, 0, 22); sb.closePath();
    ctx.fillStyle = '#ff6f8f'; ctx.fill(sb); ctx.lineWidth = 4; ctx.strokeStyle = INK; ctx.stroke(sb);
    ctx.fillStyle = '#7fd3a8'; ctx.beginPath(); ctx.ellipse(-6, -16, 8, 4, -.4, 0, TAU); ctx.ellipse(6, -16, 8, 4, .4, 0, TAU); ctx.fill();
    ctx.fillStyle = '#fff4b0'; for (const [x, y] of [[-6, -4], [6, -2], [0, 8]]) { ctx.beginPath(); ctx.arc(x, y, 2, 0, TAU); ctx.fill(); } ctx.restore();
    ctx.fillStyle = '#e45f88'; ctx.font = `800 29px ${ROUND}`; ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic'; ctx.fillText('milk', 22, -52);
    face(0, -172, 32, 62, P);
  });
}
const EGG_BODY = (() => { const p = new Path2D(); for (let i = 0; i <= 96; i++) { const a = i / 96 * TAU, r = 1 + .055 * Math.sin(3 * a + .6) + .035 * Math.sin(5 * a + 2.1);
  const x = Math.cos(a) * 172 * r, y = -98 + Math.sin(a) * 96 * r; i ? p.lineTo(x, y) : p.moveTo(x, y); } p.closePath(); return p; })();
const EGG_YOLK = ellipse(6, -116, 76, 74);
function drawEgg(P) {
  limbs(P, [150, -84], '#fffdf7', 54, 28);
  shape(EGG_BODY, '#fffdf7');
  shape(EGG_YOLK, '#ffc63f');
  detail(() => { ctx.strokeStyle = 'rgba(255,255,255,.85)'; ctx.lineWidth = 8; ctx.lineCap = 'round'; ctx.beginPath(); ctx.arc(6, -116, 56, 1.15 * Math.PI, 1.45 * Math.PI); ctx.stroke();
    face(6, -124, 27, 49, P, .95); });
}
const CHARS = [
  { draw: drawOnigiri, x: 310, top: 250, sh: [100, -62], from: -1, s: 1.12, hops: 3 },
  { draw: drawToast, x: 745, top: 300, sh: [104, -108], from: -1, s: .8, hops: 4 },
  { draw: drawMilk, x: 1180, top: 330, sh: [92, -122], from: 1, s: .95, hops: 4 },
  { draw: drawEgg, x: 1610, top: 200, sh: [150, -84], from: 1, s: 1.26, hops: 3 },
];

// ── motion: jumps, squash springs, arms, eyes ──
const HOP = .28;
for (const [i, C] of CHARS.entries()) {
  C.jumps = []; const x0 = C.x + C.from * (C.hops * 250 + 60);
  for (let k = 0; k < C.hops; k++) C.jumps.push({ t0: C.s + k * HOP, d: HOP, h: 105, x0: lerp(x0, C.x, k / C.hops), x1: lerp(x0, C.x, (k + 1) / C.hops), tilt: -C.from * .12, sq: .22 });
  C.wake = [2.5, 2.72, 2.61, 2.83][i];
  C.jumps.push({ t0: C.wake + .08, d: .3, h: 55, tilt: 0, sq: .18 });                 // wake-up pop
  C.jumps.push({ t0: 4.5 + i * .06, d: .32, h: 70, tilt: 0, sq: .2 });                  // "wow" after the wipe
  const pair = i < 2 ? T.hf1 : T.hf2, inward = (i % 2 === 0) ? 1 : -1;
  C.inward = inward; C.hf = pair;
  C.jumps.push({ t0: pair, d: .42, h: 150, dx: inward * 22, tilt: inward * .16, sq: .26, pre: .16 });
  C.yay = T.yay + i * .2;
  C.jumps.push({ t0: C.yay, d: .36, h: 95, tilt: 0, sq: .22, pre: .12 });
  for (let k = 0; k < 4; k++) C.jumps.push({ t0: 6.95 + k * .42 + (i % 2) * .21, d: .3, h: 48 + (k % 2) * 16, tilt: (i % 2 ? -1 : 1) * .06, sq: .16 });
  C.jumps.push({ t0: 8.72 + i * .05, d: .34, h: 60, tilt: 0, sq: .18 });
}
function pose(C, t) {
  const P = { x: C.x, lift: 0, sx: 1, sy: 1, rot: 0, armL: -.85, armR: -.85, eyes: 'open', mouth: 'smile', blink: 0, look: [0, 0] };
  if (t < C.jumps[0].t0) P.x = C.jumps[0].x0;
  let sq = 0;
  for (const J of C.jumps) {
    const u = (t - J.t0) / J.d;
    if (J.pre && u < 0 && u > -J.pre / J.d) sq += .16 * bell(1 + u * J.d / J.pre);             // anticipation crouch
    if (u >= 0 && u < 1) {
      P.lift = J.h * 4 * u * (1 - u);
      if (J.x0 !== undefined) P.x = lerp(J.x0, J.x1, u);
      if (J.dx) P.x += J.dx * bell(u);
      P.rot += J.tilt * bell(u);
      sq -= .1 * Math.cos(TAU * u) * (J.h / 120);                                           // stretch at takeoff / landing, round at apex
    }
    if (u >= 1) { const tau = t - J.t0 - J.d; if (tau < 1) sq += J.sq * Math.exp(-tau * 9) * Math.cos(tau * 24); }
    if (J.x1 !== undefined && u >= 1) P.x = J.x1;
  }
  P.sy = 1 - sq; P.sx = 1 + sq * .85;
  // phase logic
  if (t < C.wake) {
    P.eyes = 'sleep'; P.mouth = 'flat';
    const st0 = C.wake - .6, su = seg(t, st0, C.wake - .05);
    if (su > 0) { const b = Math.sin(Math.PI * Math.min(1, su * 1.1)); P.armL = P.armR = lerp(-.85, 1.35, eInOut(Math.min(1, su * 2))); P.sy *= 1 + .1 * b; P.sx *= 1 - .07 * b; P.mouth = 'yawn'; P.mo = .6 + .6 * b; P.rot += .05 * Math.sin(su * TAU); }
    else { P.rot += .03 * Math.sin(t * 5 + C.x); }
  } else {
    const au = seg(t, C.wake, C.wake + .35); P.armL = P.armR = lerp(1.35, -.6, eOut(au));
    P.mouth = t < C.wake + .5 ? 'open' : 'w'; P.eyes = t < C.wake + .5 ? 'wow' : 'open';
  }
  // wiggle
  const wg = seg(t, 3.15, 3.35) * (1 - seg(t, 3.7, 3.85));
  if (wg > 0) { P.rot += .1 * wg * Math.sin(TAU * 3.2 * (t - 3.15) + C.x * .01); P.armL = -.6 + .5 * wg * Math.sin(TAU * 3.2 * (t - 3.15)); P.armR = -.6 - .5 * wg * Math.sin(TAU * 3.2 * (t - 3.15)); }
  // wipe: look up in awe
  if (t >= 3.85 && t < 4.75) { P.eyes = 'wow'; P.mouth = 'open'; P.look = [0, -5 * seg(t, 3.85, 4)]; P.armL = P.armR = lerp(-.6, .5, eOut(seg(t, 3.9, 4.1))); }
  if (t >= 4.75) { P.eyes = 'open'; P.mouth = 'w'; }
  // high-five
  const hu = seg(t, C.hf - .25, C.hf + .1) * (1 - seg(t, C.hf + .45, C.hf + .7));
  if (t > C.hf - .25 && t < C.hf + .7) { if (C.inward > 0) P.armR = lerp(-.6, .75, eOut(hu)); else P.armL = lerp(-.6, .75, eOut(hu)); }
  if (t > C.hf + .1 && t < C.hf + .6) { P.eyes = 'happy'; P.mouth = 'open'; }
  // YAY
  if (t > C.yay - .1 && t < C.yay + .55) { const u = seg(t, C.yay - .1, C.yay + .12) * (1 - seg(t, C.yay + .35, C.yay + .55)); P.armL = P.armR = lerp(-.6, 1.25, eOut(u)); P.eyes = 'happy'; P.mouth = 'open'; }
  // celebration
  if (t > 6.9) { const u = seg(t, 6.9, 7.1); const w = Math.sin(TAU * 2.4 * (t - 6.9) + C.x * .004); P.armL = lerp(P.armL, 1.05 + .35 * w, u); P.armR = lerp(P.armR, 1.05 - .35 * w, u); P.eyes = (Math.floor((t - 6.9) / .84 + (C.x > 900 ? .5 : 0)) % 2) ? 'happy' : 'open'; P.mouth = 'open'; }
  if (t > 8.6) { P.eyes = 'happy'; P.mouth = 'w'; }
  // blinks
  for (const b of [1.95, 3.55, 5.72, 7.35, 8.2]) { const u = (t - b - (C.x % 7) * .02) / .16; if (u > 0 && u < 1 && P.eyes === 'open') P.blink = bell(u); }
  // butter wobble
  P.butter = .08 * Math.sin(t * 9) * clamp(P.lift / 60);
  return P;
}
function drawChar(C, t) {
  const P = pose(C, t);
  if (P.x < -300 || P.x > W + 300) return P;
  // ground shadow
  const sh = 1 - clamp(P.lift / 260) * .5;
  ctx.fillStyle = 'rgba(150,70,100,.18)'; ctx.beginPath(); ctx.ellipse(P.x + 6, Y0 + 6, 150 * S * sh * (C.draw === drawEgg ? 1.15 : .9), 22 * sh, 0, 0, TAU); ctx.fill();
  ctx.save(); ctx.translate(P.x, Y0 - P.lift); ctx.rotate(P.rot); ctx.scale(S * P.sx, S * P.sy);
  sticker(() => C.draw(P));
  ctx.restore();
  return P;
}

// ── backgrounds (precomputed) ──
let DOTS_A, DOTS_B, DOTS_C, GING_A, GING_B;
function dotTile(bg, dot, r, sp, heart) {
  const c = mk(sp * 2, sp * 2), x = c.getContext('2d'); x.fillStyle = bg; x.fillRect(0, 0, c.width, c.height); x.fillStyle = dot;
  for (const [px, py] of [[sp / 2, sp / 2], [sp * 1.5, sp * 1.5]]) { if (heart) x.fill(heartPath(px, py, r)); else { x.beginPath(); x.arc(px, py, r, 0, TAU); x.fill(); } }
  for (const [px, py] of [[sp * 1.5, sp / 2], [sp / 2, sp * 1.5]]) { x.save(); x.translate(px, py); x.rotate(.2); x.fill(sparklePath(0, 0, r * .9, 0, .3)); x.restore(); }
  return c;
}
function gingham(c1, c2, bg) {
  const c = mk(W, H - Y0 + 140), x = c.getContext('2d'), sq = 44;
  x.fillStyle = bg; x.fillRect(0, 0, c.width, c.height);
  x.globalAlpha = .55; x.fillStyle = c1;
  for (let i = 0; i * sq < c.width; i += 2) x.fillRect(i * sq, 0, sq, c.height);
  for (let j = 0; j * sq < c.height; j += 2) x.fillRect(0, j * sq, c.width, sq);
  x.globalAlpha = .5; x.fillStyle = c2;
  for (let i = 0; i * sq < c.width; i += 2) for (let j = 0; j * sq < c.height; j += 2) x.fillRect(i * sq, j * sq, sq, sq);
  x.globalAlpha = 1; return c;
}
function table(G, rim, t) {
  const top = Y0 - 70;
  const p = new Path2D(); p.moveTo(-10, H + 10); p.lineTo(-10, top + 20);
  const n = 22; for (let i = 0; i <= n; i++) { const x0 = -10 + i * (W + 20) / n; p.lineTo(x0, top + 20); }
  p.lineTo(W + 10, H + 10); p.closePath();
  // scalloped edge
  const sc = new Path2D(); sc.moveTo(-10, top + 20);
  for (let i = 0; i < n; i++) { const xa = -10 + i * (W + 20) / n, xb = xa + (W + 20) / n; sc.quadraticCurveTo((xa + xb) / 2, top - 10, xb, top + 20); }
  sc.lineTo(W + 10, H + 10); sc.lineTo(-10, H + 10); sc.closePath();
  ctx.save(); ctx.fillStyle = SHADOW; ctx.translate(0, -8); ctx.fill(sc); ctx.restore();
  ctx.save(); ctx.clip(sc); ctx.drawImage(G, 0, top - 30); ctx.restore();
  ctx.lineWidth = 6; ctx.strokeStyle = rim; ctx.stroke(sc);
}
function bgA(t) {
  const sp = 110, off = (t * 22) % (sp * 2);
  ctx.save(); ctx.translate(-off, -off * .5); ctx.fillStyle = ctx.createPattern(DOTS_A, 'repeat'); ctx.fillRect(0, 0, W + sp * 4, H + sp * 4); ctx.restore();
  // sun (sleepy → awake)
  const sy = lerp(330, 190, eOut(seg(t, 0, 1.4))), awake = t > 2.62;
  ctx.save(); ctx.translate(205, sy); ctx.rotate(t * .35);
  sticker(() => { for (let i = 0; i < 10; i++) { ctx.save(); ctx.rotate(i * TAU / 10); shape(rrect(-13, -138, 26, 40, 13), '#ffcf6b'); ctx.restore(); } shape(ellipse(0, 0, 92, 92), '#ffdf7e'); }, 5, 8);
  ctx.restore();
  ctx.save(); ctx.translate(205, sy); face(0, -8, 30, 52, { eyes: awake ? 'happy' : 'sleep', mouth: awake ? 'open' : 'flat' }, 1.1); ctx.restore();
  // cloud
  const cx = 1700 - t * 14, cy = 175 + 6 * Math.sin(t * 2);
  ctx.save(); ctx.translate(cx, cy);
  const cl = new Path2D(); for (const [x, y, r] of [[-80, 20, 52], [-20, -18, 70], [55, -2, 60], [100, 28, 42], [10, 36, 50], [-100, 40, 30]]) cl.moveTo(x + r, y), cl.arc(x, y, r, 0, TAU);
  sticker(() => shape(cl, '#ffffff', false), 5, 8);
  ctx.lineWidth = OUT; ctx.strokeStyle = INK; ctx.stroke(cl); ctx.fillStyle = '#fff'; ctx.fill(cl);
  face(0, 8, 26, 50, { eyes: 'happy', mouth: 'smile' }, .9); ctx.restore();
  table(GING_A, '#ff9fbd', t);
}
function bgB(t) {
  ctx.fillStyle = BUTTER; ctx.fillRect(0, 0, W, H);
  // sunburst rays
  ctx.save(); ctx.translate(960, 560); ctx.rotate(t * .18); ctx.fillStyle = '#ffe08f';
  for (let i = 0; i < 16; i++) { ctx.beginPath(); ctx.moveTo(0, 0); ctx.arc(0, 0, 1500, i * TAU / 16, (i + .5) * TAU / 16); ctx.closePath(); ctx.fill(); }
  ctx.restore();
  const sp = 120, off = (t * 18) % (sp * 2);
  ctx.save(); ctx.globalAlpha = .7; ctx.translate(-off, off * .5 - sp * 2); ctx.fillStyle = ctx.createPattern(DOTS_B, 'repeat'); ctx.fillRect(0, 0, W + sp * 4, H + sp * 4); ctx.restore();
  table(GING_B, '#8fd9bd', t);
}

// ── sticker text ──
function stickerText(str, x, y, size, fill, font = DISP, sc = 1, rot = 0) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc);
  ctx.font = `${font === DISP ? '' : '800 '}${size}px ${font}`; ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic'; ctx.lineJoin = 'round'; ctx.wordSpacing = `${Math.round(size * .2)}px`;
  const b = size * .15;
  ctx.fillStyle = ctx.strokeStyle = SHADOW; ctx.lineWidth = b * 2 + 10; ctx.strokeText(str, 7, 11); ctx.fillText(str, 7, 11);
  ctx.strokeStyle = WHITE; ctx.lineWidth = b * 2 + 10; ctx.strokeText(str, 0, 0);
  ctx.strokeStyle = INK; ctx.lineWidth = font === DISP ? size * .075 + 4 : size * .04 + 3; ctx.strokeText(str, 0, 0);
  ctx.fillStyle = fill; ctx.fillText(str, 0, 0);
  ctx.restore();
}
const TITLE = 'Good morning!', TCOL = ['#ff9ec0', '#ffe27a', '#bda7f7', '#ffb892'];
let TW = [];
function drawTitle(t) {
  ctx.font = `128px ${DISP}`; let x = 960 - TW.reduce((a, b) => a + b, 0) / 2, ci = 0;
  for (let k = 0; k < TITLE.length; k++) {
    const ch = TITLE[k], w = TW[k]; if (ch === ' ') { x += w; continue; }
    const t0 = T.title0 + k * .055, u = seg(t, t0, t0 + .42), uo = seg(t, T.titleOut + k * .025, T.titleOut + k * .025 + .28);
    const sc = eBack(u, 2.6) * (1 - eIn(uo)); if (sc > .01) {
      const bob = 7 * Math.sin(TAU * 1.1 * t - k * .55) * seg(t, t0 + .4, t0 + .7);
      stickerText(ch, x + w / 2, 320 + bob - 26 * (1 - u) - 40 * uo, 128, TCOL[ci % 4], DISP, sc, (1 - u) * -.35 + .04 * Math.sin(t * 3 + k));
    }
    x += w; ci++;
  }
}
// ── YAY letters ──
const YAY = [['Y', '#ff9ec0'], ['A', '#8fe0c0'], ['Y', '#bda7f7'], ['!', '#ffb38a']];
function drawYay(t, Ps) {
  for (let i = 0; i < 4; i++) {
    const C = CHARS[i], t0 = C.yay + .06; if (t < t0) continue;
    const u = seg(t, t0, t0 + .5);
    const sx = C.x, sy = Y0 - C.top * S, tx = lerp(C.x, 960 + (i - 1.5) * 330, .55), ty = 385;
    const k = eBack(u, 1.6), x = lerp(sx, tx, eOut(u)), y = lerp(sy, ty, k) - 60 * bell(Math.min(1, u * 1.3));
    const bob = 9 * Math.sin(TAU * 1.2 * (t - 6.6) - i * .9) * seg(t, 6.7, 7);
    stickerText(YAY[i][0], x, y + bob, 250, YAY[i][1], DISP, lerp(.2, 1, eBack(seg(t, t0, t0 + .35), 2.4)), (1 - u) * .5 * (i % 2 ? 1 : -1) + .05 * Math.sin(t * 2.5 + i));
  }
}
// ── sparkles and confetti ──
function sparkle(x, y, r, rot, col, a = 1) {
  if (r < .5 || a <= 0) return; ctx.save(); ctx.globalAlpha = a; const p = sparklePath(x, y, r, rot);
  ctx.lineJoin = 'round'; ctx.strokeStyle = WHITE; ctx.lineWidth = Math.max(4, r * .28); ctx.stroke(p); ctx.fillStyle = col; ctx.fill(p); ctx.lineWidth = Math.max(2, r * .09); ctx.strokeStyle = INK; ctx.stroke(p); ctx.restore();
}
function burst(x, y, t0, t, n, R, seed, cols) {
  const u = (t - t0) / .55; if (u < 0 || u > 1) return; const r = rng(seed);
  for (let i = 0; i < n; i++) { const a = i / n * TAU + r() * .5, d = R * eOut(u) * (.7 + r() * .5), s = (14 + r() * 14) * bell(Math.min(1, u * 1.4 + .15));
    sparkle(x + Math.cos(a) * d, y + Math.sin(a) * d, s, u * 2 + i, cols[i % cols.length]); }
}
const HEARTS = (() => { const r = rng(77), a = [], cols = ['#ff8fb0', '#ffb3c9', '#c9b3f7', '#8fe0c0', '#ffd27a', '#ff9e8a'];
  for (let i = 0; i < 70; i++) a.push({ x: r() * (W + 200) - 100, t0: 6.45 + r() * 1.8, v: 230 + r() * 200, s: 16 + r() * 22, ph: r() * TAU, w: 3 + r() * 4, sw: 30 + r() * 50, col: cols[i % cols.length], rot: (r() - .5) * .8 });
  return a; })();
function confetti(t) {
  for (const h of HEARTS) {
    const dt = t - h.t0; if (dt < 0) continue; const y = -60 + dt * h.v; if (y > H + 60) continue;
    const x = h.x + h.sw * Math.sin(dt * 2.2 + h.ph), flip = Math.cos(dt * h.w + h.ph);
    ctx.save(); ctx.translate(x, y); ctx.rotate(h.rot + .4 * Math.sin(dt * 1.7 + h.ph)); ctx.scale(Math.max(.12, Math.abs(flip)), 1);
    const p = heartPath(0, 0, h.s); ctx.fillStyle = WHITE; ctx.lineWidth = 8; ctx.lineJoin = 'round'; ctx.strokeStyle = WHITE; ctx.stroke(p);
    ctx.fillStyle = h.col; ctx.fill(p); if (flip < 0) { ctx.fillStyle = 'rgba(90,57,64,.15)'; ctx.fill(p); } ctx.lineWidth = 3; ctx.strokeStyle = INK; ctx.stroke(p); ctx.restore();
  }
}
function zzz(t) {
  for (const [i, C] of CHARS.entries()) {
    for (let k = 0; k < 3; k++) {
      const t0 = 1.55 + i * .12 + k * .28, u = seg(t, t0, t0 + .9); if (u <= 0 || u >= 1 || t > C.wake - .1) continue;
      const P = pose(C, t), x = P.x + 70 + 40 * u + 10 * Math.sin(u * 8), y = Y0 - P.lift - C.top * S - 10 - 90 * u;
      ctx.save(); ctx.globalAlpha = bell(u) ** .5; stickerText('z', x, y, 40 + k * 10, LAV_D, ROUND, 1, -.2); ctx.restore();
    }
  }
}

// ── render ──
function render(t) {
  const wu = seg(t, ...T.wipe);
  if (wu < 1) bgA(t);
  if (wu > 0) {                                   // sparkle-burst wipe
    const R = 60 + 4300 * Math.pow(wu, 2.2), rot = wu * 1.2, p = sparklePath(960, 520, R, rot, .3);
    ctx.save(); ctx.clip(p); bgB(t); ctx.restore();
    if (wu < 1) { ctx.save(); ctx.lineJoin = 'round'; ctx.lineWidth = 36; ctx.strokeStyle = WHITE; ctx.stroke(p); ctx.lineWidth = 12; ctx.strokeStyle = LAV_D; ctx.stroke(p); ctx.restore(); }
  }
  // gathering sparkle before the wipe
  const g = seg(t, 3.55, 3.95); if (g > 0 && wu < .2) sparkle(960, 520, 90 * eBack(g, 2) * (1 - seg(t, 3.9, 4.05)) + 1, t * 3, '#fff6c2');
  burst(960, 520, 3.92, t, 14, 900, 5, ['#ffe27a', '#ff9ec0', '#bda7f7', '#8fe0c0']);
  if (t < 4.2) drawTitle(t);
  zzz(t);
  const Ps = CHARS.map(C => drawChar(C, t));
  for (const [i, C] of CHARS.entries()) burst(Ps[i].x, Y0 - C.top * S - 30, C.wake, t, 5, 110, 20 + i, ['#ffe27a', '#ffffff', '#ff9ec0']);
  // high-five claps
  for (const [a, b, t0] of [[0, 1, T.hf1], [2, 3, T.hf2]]) {
    const tc = t0 + .2, u = seg(t, tc, tc + .4); if (u <= 0 || u >= 1) continue;
    const x = (CHARS[a].x + CHARS[b].x) / 2, y = Y0 - 150 - 115 * S;
    ctx.save(); const s = 70 * eBack(seg(t, tc, tc + .15), 3) * (1 - eIn(seg(t, tc + .25, tc + .4)));
    const p = starPath(x, y, s, u * .6, .5, 8); ctx.lineJoin = 'round'; ctx.strokeStyle = WHITE; ctx.lineWidth = 14; ctx.stroke(p); ctx.fillStyle = '#fff3a1'; ctx.fill(p); ctx.lineWidth = 5; ctx.strokeStyle = INK; ctx.stroke(p); ctx.restore();
    burst(x, y, tc, t, 8, 150, 40 + a, ['#ff9ec0', '#8fe0c0', '#bda7f7', '#ffe27a']);
    const hu = seg(t, tc, tc + .6); for (let k = 0; k < 3; k++) { const hx = x + (k - 1) * 50, hy = y - 40 - 120 * hu - k * 10; ctx.save(); ctx.globalAlpha = 1 - hu; ctx.translate(hx, hy); const hp = heartPath(0, 0, 18); ctx.fillStyle = PINK_D; ctx.strokeStyle = WHITE; ctx.lineWidth = 7; ctx.stroke(hp); ctx.fill(hp); ctx.restore(); }
  }
  drawYay(t, Ps);
  confetti(t);
  // heart iris
  const iu = seg(t, ...T.iris);
  if (iu > 0) {
    const R = lerp(1500, 0, eInOut(iu)), cx = 960, cy = lerp(640, 560, iu);
    const hp = heartPath(cx, cy, R);
    ctx.save(); const outside = new Path2D(); outside.rect(0, 0, W, H); outside.addPath(hp);
    ctx.clip(outside, 'evenodd');
    const sp = 110, off = (t * 22) % (sp * 2);
    ctx.save(); ctx.translate(-off, -off * .5); ctx.fillStyle = ctx.createPattern(DOTS_C, 'repeat'); ctx.fillRect(0, 0, W + sp * 4, H + sp * 4); ctx.restore();
    ctx.restore();
    if (R > 2) { ctx.save(); ctx.lineJoin = 'round'; ctx.lineWidth = 30; ctx.strokeStyle = WHITE; ctx.stroke(hp); ctx.lineWidth = 9; ctx.strokeStyle = INK; ctx.stroke(hp); ctx.restore(); }
  }
  // final heart + caption
  const fu = seg(t, T.heart, T.heart + .45);
  if (fu > 0) {
    const beat = 1 + .06 * bell(((t - T.heart - .5) / .5) % 1 * (t > T.heart + .5 ? 1 : 0));
    const s = 165 * eBack(fu, 2.6) * beat;
    ctx.save(); ctx.translate(960, 440); ctx.rotate(.05 * Math.sin(t * 3));
    ctx.save(); ctx.translate(7, 11); MODE = 'shadow'; shape(heartPath(0, 0, s), PINK_D); ctx.restore(); MODE = 'white'; shape(heartPath(0, 0, s), PINK_D); MODE = 'ink'; shape(heartPath(0, 0, s), '#ff8fb0');
    ctx.fillStyle = 'rgba(255,255,255,.75)'; ctx.beginPath(); ctx.ellipse(-s * .42, -s * .3, s * .14, s * .08, -.6, 0, TAU); ctx.fill();
    face(0, -s * .12, 34, 58, { eyes: 'happy', mouth: 'w' }, s / 120);
    ctx.restore();
    burst(960, 440, T.heart + .05, t, 10, 260, 9, ['#ffe27a', '#8fe0c0', '#ffffff', '#bda7f7']);
    const cu = seg(t, T.heart + .2, T.heart + .6);
    if (cu > 0) stickerText('Have a sweet day!', 960, 800 + 30 * (1 - eOut(cu)), 84, '#fff3a1', DISP, eBack(cu, 1.8), 0);
  }
  // fade in / out (to cream)
  const f = Math.max(1 - eOut(seg(t, ...T.fadeIn)), eInOut(seg(t, ...T.fadeOut)));
  if (f > 0) { ctx.fillStyle = `rgba(255,250,240,${f})`; ctx.fillRect(0, 0, W, H); }
}

window.ready = (async () => {
  await Promise.all([`128px ${DISP}`, `800 40px ${ROUND}`].map(f => document.fonts.load(f, 'Good morning! YAY Have a sweet day milk z')));
  await document.fonts.ready;
  DOTS_A = dotTile(MINT, '#e2f8ee', 11, 110, false);
  DOTS_B = dotTile('rgba(0,0,0,0)', '#fff8d8', 12, 120, true);
  DOTS_C = dotTile(LAV, '#ebe2fb', 12, 110, true);
  GING_A = gingham('#ffc2d4', '#ff9fbd', '#fff5f8');
  GING_B = gingham('#bff0dc', '#8fdcc0', '#f6fffa');
  ctx.font = `128px ${DISP}`; TW = [...TITLE].map(c => ctx.measureText(c).width + (c === ' ' ? 10 : 4));
  render(0);
})();
window.draw = ({ t }) => { render(t); return cv.toDataURL('image/jpeg', 0.92).split(',')[1]; };
window.events = () => {
  const ev = [{ t: 0, k: 'music' }];
  let ci = 0; for (let k = 0; k < TITLE.length; k++) { if (TITLE[k] !== ' ') ev.push({ t: T.title0 + k * .055 + .08, k: 'pop', n: ci++ }); }
  for (const C of CHARS) for (const J of C.jumps) { if (J.t0 > 9.5) continue; ev.push({ t: J.t0, k: 'boing', v: J.h / 150 }); ev.push({ t: J.t0 + J.d, k: 'pat', v: J.h / 150 }); }
  for (const C of CHARS) ev.push({ t: C.wake, k: 'chime' }), ev.push({ t: C.wake - .55, k: 'yawn' });
  ev.push({ t: T.titleOut, k: 'unpop' }, { t: 3.55, k: 'shimmer' }, { t: T.wipe[0], k: 'whoosh', d: .7 }, { t: 3.95, k: 'sparkle' });
  ev.push({ t: T.hf1 + .2, k: 'clap' }, { t: T.hf2 + .2, k: 'clap' });
  CHARS.forEach((C, i) => ev.push({ t: C.yay + .08, k: 'pop', n: 6 + i * 2, v: 1.3 }));
  ev.push({ t: T.yay + .75, k: 'yay' });
  for (const h of HEARTS.slice(0, 26)) ev.push({ t: h.t0 + .3, k: 'tink' });
  ev.push({ t: T.iris[0], k: 'iris', d: .75 }, { t: T.heart + .05, k: 'ding' }, { t: T.heart + .3, k: 'sparkle' });
  return ev.sort((a, b) => a.t - b.t);
};
