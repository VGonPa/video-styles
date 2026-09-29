// History Comedy: timeline, per-frame drawing, audio events (loaded by anim.html)
// 0.0 map + two kings argue → 2.7 zoom into the map, armies sail, BONK on the island → 5.3 smash
// cut to a shocked face → 6.5 "37 years later…" card → 7.3 the two old kings still on the island,
// punchline → 9.5 fade to parchment.
const T = { exit: 2.62, zoom: [2.7, 3.35], bump: 4.2, face: 5.3, shock: 5.44, card: 6.5, isle: 7.3, fade: [9.45, 9.98] };
let MAPC, PARCH, GRAIN;

const talk = (t, t0, d) => { if (t < t0 || t > t0 + d) return 0; const v = Math.sin((t - t0) * TAU * 5.5); return v > 0 ? 0.35 + 0.65 * v : 0; };
const pop = (t, t0, d = 0.32) => eob(seg(t, t0, t0 + d), 2.6);

// speech bubble: tip (tx,ty) points at the speaker; box centred at (tx+dx, ty-dy-h/2)
function bubble(g, t, t0, t1, tx, ty, lines, dx, dy = 46, sz = 60) {
  if (t < t0 || t > t1 + 0.12) return;
  const k = t > t1 ? 1 - seg(t, t1, t1 + 0.12) : pop(t, t0, 0.3);
  if (k <= 0) return;
  g.save(); g.font = `${sz}px "Patrick Hand"`;
  const lh = sz * 1.08, w = Math.max(...lines.map(l => g.measureText(l).width)) + sz * 1.0, h = lines.length * lh + sz * 0.62;
  const bx = tx + dx, by = ty - dy - h / 2;
  g.translate(tx, ty); g.scale(k, k); g.translate(-tx, -ty);
  g.lineJoin = 'round'; g.lineWidth = 6; g.strokeStyle = INK; g.fillStyle = '#fffdf5';
  const r = 30, x0 = bx - w / 2, y0 = by - h / 2;
  const box = () => { g.beginPath(); g.roundRect(x0, y0, w, h, r); };
  const tail = () => { const bx0 = clamp(tx, x0 + 50, x0 + w - 90); g.beginPath(); g.moveTo(bx0, y0 + h - 4); g.quadraticCurveTo(bx0 + 10, y0 + h + dy * 0.5, tx, ty); g.quadraticCurveTo(bx0 + 30, y0 + h + dy * 0.3, bx0 + 54, y0 + h - 4); g.closePath(); };
  g.save(); g.translate(7, 8); g.fillStyle = 'rgba(60,35,15,0.22)'; box(); g.fill(); tail(); g.fill(); g.restore();
  tail(); g.fill(); g.stroke(); box(); g.fill(); g.stroke(); tail(); g.fill();
  g.fillStyle = INK; g.textAlign = 'center'; g.textBaseline = 'middle';
  lines.forEach((l, i) => g.fillText(l, bx, y0 + sz * 0.31 + lh * (i + 0.5) + 2));
  g.restore();
}
// subtitle caption at the bottom (hard cut in with a small rise, like a lower-third subtitle)
const CAPS = [
  [0.25, 2.66, '1412. Two kings. One very small island.'],
  [3.15, 4.2, 'Both invasions set sail on the same morning.'],
  [4.25, 5.28, 'The island is 40 metres wide.'],
  [5.5, 6.48, 'Nobody had a plan B.'],
  [8.75, 9.95, 'The goats were never consulted.'],
];
function captions(g, t) {
  for (const [a, b, s] of CAPS) {
    if (t < a || t > b) continue;
    const k = eout(seg(t, a, a + 0.14)), fo = t > T.fade[0] ? 1 - seg(t, T.fade[0], T.fade[1] - 0.1) : 1;
    g.save(); g.globalAlpha = k * fo; g.font = '900 54px Nunito'; g.textAlign = 'center'; g.textBaseline = 'alphabetic'; g.letterSpacing = '0.5px';
    const y = 1022 + (1 - k) * 14;
    g.lineJoin = 'round'; g.lineWidth = 13; g.strokeStyle = 'rgba(30,20,14,0.96)'; g.strokeText(s, W / 2, y);
    g.fillStyle = '#fff6dc'; g.fillText(s, W / 2, y); g.restore();
  }
}

// ── scene 1+2: the map ──
const bz = (a, c, b, u) => [(1 - u) * (1 - u) * a[0] + 2 * (1 - u) * u * c[0] + u * u * b[0], (1 - u) * (1 - u) * a[1] + 2 * (1 - u) * u * c[1] + u * u * b[1]];
const ARMY = [
  { from: [640, 660], c: [800, 700], to: [925, 590], col: COL.red, dk: COL.redDk, n: '12,000', side: -1, t0: 3.05, a0: 3.2 },
  { from: [1300, 468], c: [1130, 430], to: [995, 590], col: COL.pur, dk: COL.purDk, n: '12,001', side: 1, t0: 3.14, a0: 3.28 },
];
const MARCH = [3.55, 4.2], HOPS = 4;
function armyU(t) { const u = seg(t, MARCH[0], MARCH[1]) * HOPS, k = Math.min(F(u), HOPS - 1), fr = Math.min(1, u - k); return [(k + eio(fr)) / HOPS, fr, u >= HOPS]; }
function arrow(g, A, rev) {
  if (rev <= 0) return;
  const N = 48, pts = []; for (let i = 0; i <= N * rev; i++) pts.push(bz(A.from, A.c, A.to, i / N));
  const end = bz(A.from, A.c, A.to, rev); pts.push(end);
  const pr = bz(A.from, A.c, A.to, Math.max(0, rev - 0.04)), ang = Math.atan2(end[1] - pr[1], end[0] - pr[0]);
  g.lineCap = 'round'; g.lineJoin = 'round';
  const line = () => { g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); };
  const head = () => { g.beginPath(); g.moveTo(end[0] + Math.cos(ang) * 22, end[1] + Math.sin(ang) * 22); g.lineTo(end[0] + Math.cos(ang + 2.3) * 22, end[1] + Math.sin(ang + 2.3) * 22); g.lineTo(end[0] + Math.cos(ang - 2.3) * 22, end[1] + Math.sin(ang - 2.3) * 22); g.closePath(); };
  line(); g.strokeStyle = INK; g.lineWidth = 17; g.stroke(); g.strokeStyle = A.col; g.lineWidth = 10; g.stroke();
  head(); g.fillStyle = A.col; g.lineWidth = 3.5; g.strokeStyle = INK; g.fill(); g.stroke();
}
function blob(g, x, y, r, A, sx, sy, t) {
  g.save(); g.translate(x, y); g.scale(sx, sy); g.lineJoin = 'round';
  g.beginPath(); for (let i = 0; i <= 40; i++) { const a = i / 40 * TAU, rr = r * (1 + 0.07 * Math.sin(3 * a + A.side) + 0.05 * Math.sin(5 * a + t * 3 * A.side)); const px = Math.cos(a) * rr * 1.18, py = Math.sin(a) * rr * 0.9; i ? g.lineTo(px, py) : g.moveTo(px, py); } g.closePath();
  g.save(); g.translate(3, 4); g.fillStyle = 'rgba(40,30,20,0.25)'; g.fill(); g.restore();
  g.fillStyle = A.col; g.fill(); g.strokeStyle = INK; g.lineWidth = 3.2; g.stroke();
  g.save(); g.clip(); g.fillStyle = 'rgba(255,255,255,0.18)'; g.beginPath(); g.ellipse(-r * 0.3, -r * 0.45, r * 0.8, r * 0.35, -0.2, 0, TAU); g.fill(); g.restore();
  // flag
  const fx = -A.side * r * 0.55, fy = -r * 0.75;
  g.beginPath(); g.moveTo(fx, fy + 6); g.lineTo(fx, fy - 40); g.lineWidth = 3; g.stroke();
  const wv = Math.sin(t * 9 + A.side) * 3;
  g.beginPath(); g.moveTo(fx, fy - 40); g.quadraticCurveTo(fx - A.side * 12, fy - 36 + wv, fx - A.side * 26, fy - 33); g.lineTo(fx, fy - 24); g.closePath(); g.fillStyle = A.dk; g.fill(); g.lineWidth = 2.5; g.stroke();
  g.font = '900 19px Nunito'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.lineWidth = 5; g.strokeStyle = INK; g.strokeText(A.n, 0, 3); g.fillStyle = '#fffaf0'; g.fillText(A.n, 0, 3);
  g.restore();
}
function star(g, x, y, r, a) { g.beginPath(); for (let i = 0; i < 10; i++) { const rr = i % 2 ? r * 0.45 : r, q = a + i * PI / 5; g.lineTo(x + Math.cos(q) * rr, y + Math.sin(q) * rr); } g.closePath(); }
function sceneMap(g, t) {
  const zk = eio(seg(t, T.zoom[0], T.zoom[1])), z = lerp(1, 2.1, zk), cx = 960, cy = lerp(540, 578, zk);
  const db = t - T.bump, shake = db > 0 && db < 0.3 ? (1 - db / 0.3) * 9 : 0;
  const shx = shake * Math.sin(db * 90), shy = shake * Math.cos(db * 77);
  g.setTransform(z, 0, 0, z, 960 - cx * z + shx, 540 - cy * z + shy);
  g.drawImage(MAPC, 0, 0, W, H);
  // goats on the island (tiny); they hop at the bump
  const gh = db > 0 ? Math.sin(PI * seg(t, T.bump, T.bump + 0.36)) * 14 : 0;
  goat(g, 932, 536 - gh, 0.19, 1, { graze: 0.6 + 0.4 * Math.sin(t * 2) }); goat(g, 960, 528 - gh * 1.3, 0.19, -1, { hop: gh > 0 }); goat(g, 990, 538 - gh, 0.19, -1, { graze: 1 });
  // armies
  for (const A of ARMY) {
    if (t < A.t0) continue;
    arrow(g, A, eout(seg(t, A.a0, A.a0 + 0.38)));
    const [u, fr, done] = armyU(t); let [x, y] = bz(A.from, A.c, A.to, u); let sx = 1, sy = 1;
    if (!done && t > MARCH[0]) { y -= Math.sin(PI * fr) * 10; const q = Math.sin(PI * fr); sx = 1 - 0.08 * q; sy = 1 + 0.1 * q; }
    if (db > 0) { const e = Math.exp(-db * 7), w = Math.cos(db * 26); sx = 1 - 0.26 * e * w; sy = 1 + 0.2 * e * w; x += A.side * 16 * (1 - Math.exp(-db * 9)); x += A.side * 10 * e * (w < 0 ? -w : 0) * 0; }
    const pk = pop(t, A.t0, 0.3); blob(g, x, y, 34, A, sx * pk, sy * pk, t);
  }
  // BONK
  if (db > 0 && db < 1.1) {
    const k = pop(t, T.bump, 0.25), fo = 1 - seg(t, T.bump + 0.8, T.bump + 1.1);
    g.save(); g.globalAlpha = fo; g.lineJoin = 'round';
    for (let i = 0; i < 4; i++) { const a = db * 4 + i * TAU / 4, rx = 60 * k, sx0 = 960 + Math.cos(a) * rx, sy0 = 548 + Math.sin(a) * rx * 0.35 - 30;
      star(g, sx0, sy0, 9, a * 2); g.fillStyle = COL.gold; g.fill(); g.strokeStyle = INK; g.lineWidth = 2.5; g.stroke(); }
    g.translate(960, 676); g.scale(k, k); g.rotate(-0.08);
    star(g, 0, 0, 58, 0.3); g.fillStyle = '#fff4cf'; g.fill(); g.strokeStyle = INK; g.lineWidth = 3.5; g.stroke();
    g.font = '40px "Patrick Hand"'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = COL.redDk; g.fillText('BONK!', 0, 2);
    g.restore();
  }
  g.setTransform(1, 0, 0, 1, 0, 0);
  // the kings (scene 1), standing on their own kingdoms
  if (t < T.exit + 0.4) {
    const ex = ein(seg(t, T.exit, T.exit + 0.32)) * 720 - Math.sin(PI * seg(t, T.exit - 0.1, T.exit + 0.06)) * 18;
    const pH = pop(t, 0.12, 0.34), pO = pop(t, 0.28, 0.34);
    const hT = talk(t, 0.8, 0.7), oT = talk(t, 1.62, 0.8);
    const pointing = eob(seg(t, 0.72, 0.9)) * (1 - eio(seg(t, 1.9, 2.1)));
    const shrug = eob(seg(t, 1.55, 1.75));
    const blinkH = (t > 1.95 && t < 2.03), blinkO = (t > 0.55 && t < 0.62) || (t > 2.3 && t < 2.37);
    king(g, 'humbert', { x: 330, y: 960 + ex, s: 1.32 * (0.4 + 0.6 * pH), sy: pH / (0.4 + 0.6 * pH), f: 1, mouth: hT, brow: t > 1.6 ? -1 : -0.3, blink: blinkH,
      armF: [lerp(0.3, 1.45, pointing), lerp(0.9, 0.55, pointing)], armB: [-0.25, -1.0], bob: Math.sin(t * 5) * 1.5, lean: -0.03 * pointing, crownTilt: -0.05 });
    king(g, 'osric', { x: 1590, y: 960 + ex, s: 1.32 * (0.4 + 0.6 * pO), sy: pO / (0.4 + 0.6 * pO), f: -1, mouth: oT, brow: t < 1.55 ? 0.8 : 0.4, smile: 0.2, blink: blinkO,
      armF: [lerp(0.15, 0.7, shrug), lerp(0.8, 1.5, shrug)], armB: [lerp(-0.15, 0.4, shrug), lerp(-0.6, 1.6, shrug)], bob: Math.sin(t * 5 + 2) * 1.5, crownTilt: 0.06 });
    bubble(g, t, 0.75, T.exit - 0.02, 480, 420, ['Nubb is ours.', 'No cap.'], 170, 40);
    bubble(g, t, 1.55, T.exit - 0.02, 1440, 420, ['Bro. It’s a rock', 'with goats.'], -200, 40);
  }
}

// ── scene 3: the shocked face ──
function sceneFace(g, t) {
  const lt = t - T.face;
  g.drawImage(PARCH, 0, 0);
  const punch = 1 + 0.28 * (1 - eob(seg(t, T.face, T.face + 0.2), 1.8)) + 0.07 * seg(t, T.face, T.card), ang = lt * 0.18;
  // radial burst
  g.save(); g.globalCompositeOperation = 'multiply'; g.translate(960, 470);
  for (let i = 0; i < 18; i++) { const a0 = ang + i * TAU / 18; g.beginPath(); g.moveTo(0, 0); g.arc(0, 0, 1500, a0, a0 + TAU / 36); g.closePath(); g.fillStyle = i % 2 ? '#f1c4a2' : '#e79a7e'; g.fill(); }
  g.restore();
  g.save(); g.translate(960, 560); g.scale(punch, punch); g.translate(-960, -560); g.lineJoin = 'round'; g.lineCap = 'round';
  // shoulders, collar, neck (the body is under the head: not a floating head)
  const K = KINGS.humbert;
  g.save(); g.translate(0, 44);
  g.beginPath(); g.moveTo(420, 1120); g.bezierCurveTo(430, 880, 560, 820, 760, 810); g.lineTo(1160, 810); g.bezierCurveTo(1360, 820, 1490, 880, 1500, 1120); g.closePath();
  g.fillStyle = K.robe; g.fill(); g.strokeStyle = INK; g.lineWidth = 10; g.stroke();
  g.beginPath(); g.rect(885, 740, 140, 90); g.fillStyle = COL.skinSh; g.fill(); g.stroke();
  g.beginPath(); g.moveTo(560, 900); g.quadraticCurveTo(580, 800, 800, 796); g.lineTo(1120, 796); g.quadraticCurveTo(1350, 800, 1370, 900); g.quadraticCurveTo(960, 960, 560, 900); g.closePath();
  g.fillStyle = COL.ermine; g.fill(); g.stroke();
  g.fillStyle = INK; for (const [x, y] of [[650, 880], [760, 900], [880, 908], [1010, 910], [1130, 900], [1250, 884], [720, 840], [1200, 840]]) { g.beginPath(); g.moveTo(x, y - 14); g.lineTo(x + 8, y + 8); g.lineTo(x - 8, y + 8); g.closePath(); g.fill(); }
  g.restore();
  const sk = eob(seg(t, T.shock, T.shock + 0.16), 2.4), jit = sk > 0.5 ? Math.sin(t * 70) * 3 : 0;
  g.save(); g.translate(930 + jit, 540); head(g, 'humbert', 272, { shock: sk, mouth: 0, smile: 0.5 }); g.restore();
  g.save(); g.translate(942 + jit, 540 - 210 - 16 * sk); g.scale(2.8, 2.8); g.rotate(-0.04 - 0.1 * sk); crown(g, 'tall', 0, 0, 1, 0); g.restore();
  // sweat drop
  if (t > 5.75) { const k = seg(t, 5.75, 6.4), y = 390 + eio(k) * 90;
    g.beginPath(); g.moveTo(790, y - 60); g.quadraticCurveTo(822, y - 8, 790, y + 10); g.quadraticCurveTo(758, y - 8, 790, y - 60); g.fillStyle = '#bfe3ee'; g.fill(); g.lineWidth = 6; g.strokeStyle = INK; g.stroke(); }
  // shock lines
  if (sk > 0.3) { g.strokeStyle = INK; g.lineWidth = 10; for (const [a, r0] of [[-2.4, 380], [-2.0, 400], [-1.1, 400], [-0.7, 380]]) { const L = 50 + 10 * Math.sin(t * 30 + a); g.beginPath(); g.moveTo(930 + Math.cos(a) * r0, 540 + Math.sin(a) * r0); g.lineTo(930 + Math.cos(a) * (r0 + L), 540 + Math.sin(a) * (r0 + L)); g.stroke(); } }
  g.restore();
}

// ── scene 4: "37 years later…" ──
function sceneCard(g, t) {
  g.drawImage(PARCH, 0, 0);
  g.save(); g.globalCompositeOperation = 'multiply'; g.fillStyle = '#d9bf8f'; g.fillRect(0, 0, W, H); g.restore();
  const k = eout(seg(t, T.card + 0.04, T.card + 0.4));
  g.save(); g.beginPath(); g.rect(0, 0, 330 + k * 1300, H); g.clip();
  g.font = 'italic 150px "IM Fell English"'; g.textAlign = 'center'; g.textBaseline = 'alphabetic'; g.fillStyle = INK; g.fillText('37 years later…', 960, 575); g.restore();
  // hourglass flips over, then sand runs
  const hk = eob(seg(t, T.card + 0.02, T.card + 0.34), 1.6), sand = seg(t, T.card + 0.3, T.isle);
  g.save(); g.translate(960, 320); g.scale(1.35, 1.35); g.rotate(PI * hk); g.lineJoin = 'round'; g.strokeStyle = INK; g.lineWidth = 6;
  const glass = () => { g.beginPath(); g.moveTo(-44, -70); g.lineTo(44, -70); g.quadraticCurveTo(40, -18, 6, 0); g.quadraticCurveTo(40, 18, 44, 70); g.lineTo(-44, 70); g.quadraticCurveTo(-40, 18, -6, 0); g.quadraticCurveTo(-40, -18, -44, -70); g.closePath(); };
  glass(); g.fillStyle = 'rgba(255,252,240,0.55)'; g.fill();
  g.save(); glass(); g.clip(); g.fillStyle = COL.gold;
  // before the flip the sand is all in the bottom bulb (local +y); after, that bulb is on top and drains
  const full = hk < 0.5 ? 1 : 1 - 0.35 * sand, other = hk < 0.5 ? 0 : 0.35 * sand;
  if (hk < 0.5) g.fillRect(-50, 70 - 62 * full, 100, 62 * full); else g.fillRect(-50, 6, 100, 62 * full);
  if (other > 0) { g.fillRect(-50, -70, 100, 62 * other); if (hk > 0.95) g.fillRect(-2.5, -70 + 62 * other, 5, 70 - 62 * other); }
  g.restore(); glass(); g.stroke();
  for (const y of [-78, 78]) { g.beginPath(); g.roundRect(-60, y - 9, 120, 18, 6); g.fillStyle = '#9a6a3a'; g.fill(); g.stroke(); }
  g.restore();
  const fl = eio(seg(t, T.card + 0.25, T.card + 0.6));
  if (fl > 0) { g.save(); g.strokeStyle = INK; g.lineWidth = 4; g.lineCap = 'round'; g.beginPath();
    for (let i = 0; i <= 60 * fl; i++) { const u = i / 60, x = 700 + u * 520, y = 640 + Math.sin(u * TAU * 1.5) * 10 * Math.sin(u * PI); i ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke();
    g.beginPath(); g.arc(960, 640, 7 * fl, 0, TAU); g.fillStyle = INK; g.fill(); g.restore(); }
}

// ── scene 5: the old kings, still on the island ──
function sceneIsle(g, t) {
  const lt = t - T.isle, zz = 1 + 0.035 * seg(t, T.isle, 10);
  g.save(); g.translate(960, 600); g.scale(zz, zz); g.translate(-960, -600);
  g.drawImage(PARCH, 0, 0);
  g.save(); g.globalCompositeOperation = 'multiply';
  const sky = g.createLinearGradient(0, 0, 0, 700); sky.addColorStop(0, '#dce8e4'); sky.addColorStop(1, '#fbf1dc'); g.fillStyle = sky; g.fillRect(0, 0, W, 700);
  // distant home coasts on the horizon
  g.fillStyle = COL.redLand; g.beginPath(); g.moveTo(-20, 700); g.lineTo(-20, 610); g.quadraticCurveTo(120, 590, 250, 640); g.quadraticCurveTo(320, 670, 380, 700); g.fill();
  g.fillStyle = COL.purLand; g.beginPath(); g.moveTo(1940, 700); g.lineTo(1940, 600); g.quadraticCurveTo(1780, 596, 1680, 640); g.quadraticCurveTo(1600, 676, 1530, 700); g.fill();
  g.restore(); g.globalAlpha = 0.75; g.fillStyle = COL.sea; g.fillRect(0, 700, W, 400); g.globalAlpha = 1;
  g.strokeStyle = INK; g.lineWidth = 3; g.globalAlpha = 0.6; g.beginPath(); g.moveTo(0, 700); g.lineTo(W, 700); g.stroke(); g.globalAlpha = 1;
  // clouds
  for (const [x, y, s] of [[420, 230, 1], [1480, 180, 0.8], [980, 120, 0.6]]) { const dx = lt * 12 * s; g.save(); g.translate(x + dx, y); g.scale(s, s);
    g.beginPath(); g.arc(-60, 10, 44, PI * 0.5, PI * 1.5); g.arc(0, -16, 58, PI, 0); g.arc(64, 8, 42, PI * 1.4, PI * 0.5); g.closePath(); g.fillStyle = '#fbf3de'; g.fill(); g.lineWidth = 4; g.strokeStyle = 'rgba(53,37,27,0.6)'; g.stroke(); g.restore(); }
  // waves
  g.strokeStyle = 'rgba(50,95,105,0.55)'; g.lineWidth = 4; g.lineCap = 'round';
  for (let i = 0; i < 16; i++) { const r = hash(i, 3, 2), x = (hash(i, 1, 2) * 2100 + lt * 20 * (0.5 + r)) % 2100 - 90, y = 740 + hash(i, 2, 2) * 320; if (Math.abs(x - 960) < 640 && y < 900) continue;
    g.beginPath(); g.moveTo(x - 24, y); g.quadraticCurveTo(x - 12, y - 12, x, y); g.quadraticCurveTo(x + 12, y - 12, x + 24, y); g.stroke(); }
  // island
  g.save(); g.lineJoin = 'round';
  g.beginPath(); g.ellipse(960, 830, 600, 105, 0, 0, TAU); g.fillStyle = 'rgba(50,95,105,0.25)'; g.fill();
  g.beginPath(); g.moveTo(380, 830); g.bezierCurveTo(420, 740, 600, 720, 960, 716); g.bezierCurveTo(1320, 720, 1500, 740, 1540, 830); g.bezierCurveTo(1300, 880, 620, 880, 380, 830); g.closePath();
  g.fillStyle = COL.sand; g.fill(); g.strokeStyle = INK; g.lineWidth = 6; g.stroke();
  g.beginPath(); g.moveTo(440, 800); g.bezierCurveTo(480, 740, 640, 728, 960, 724); g.bezierCurveTo(1280, 728, 1440, 740, 1480, 800); g.bezierCurveTo(1200, 790, 700, 790, 440, 800); g.closePath();
  g.fillStyle = COL.grass; g.fill(); g.lineWidth = 5; g.stroke(); g.restore();
  // shared signpost with both flags
  g.save(); g.lineJoin = 'round'; g.strokeStyle = INK; g.lineWidth = 5;
  g.beginPath(); g.rect(954, 560, 14, 200); g.fillStyle = '#9a6a3a'; g.fill(); g.stroke();
  const wv = Math.sin(t * 4) * 5;
  g.beginPath(); g.moveTo(961, 480); g.lineTo(961, 562); g.stroke();
  g.beginPath(); g.moveTo(961, 482); g.quadraticCurveTo(930, 486 + wv, 900, 484); g.lineTo(914, 500); g.lineTo(900, 516); g.quadraticCurveTo(930, 516 - wv, 961, 512); g.closePath(); g.fillStyle = COL.red; g.fill(); g.lineWidth = 4; g.stroke();
  g.beginPath(); g.moveTo(961, 482); g.quadraticCurveTo(992, 486 - wv, 1022, 484); g.lineTo(1008, 500); g.lineTo(1022, 516); g.quadraticCurveTo(992, 516 + wv, 961, 512); g.closePath(); g.fillStyle = COL.pur; g.fill(); g.stroke();
  g.beginPath(); g.roundRect(876, 574, 170, 70, 8); g.fillStyle = '#c99a5e'; g.fill(); g.lineWidth = 5; g.stroke();
  g.font = '44px "IM Fell English SC"'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = INK; g.fillText('Nubb', 961, 610); g.restore();
  // goats (they multiplied)
  const GO = [[760, 812, 0.95, 1, 0], [890, 842, 1.0, -1, 1], [1050, 848, 1.05, 1, 2], [1170, 806, 0.9, -1, 3], [965, 790, 0.8, 1, 4]];
  for (const [x, y, s, f, i] of GO) { const gz = i === 2 ? (t > 9.0 ? 1 - eio(seg(t, 9.0, 9.2)) : 1) * (0.6 + 0.4 * Math.sin(t * 2.2)) : (i % 2 ? 0.5 + 0.5 * Math.sin(t * 1.7 + i) : 0);
    goat(g, x, y, s, f, { graze: Math.max(0, gz), blink: i === 2 && t > 9.45 && t < 9.52 }); }
  // the kings, old now
  const oT = talk(t, 7.52, 1.05), hT = talk(t, 8.3, 0.7);
  const br = Math.sin(t * 2.6) * 1.5;
  king(g, 'humbert', { x: 560, y: 790, s: 1.22, f: 1, old: true, lean: 0.13, mouth: hT, brow: t > 8.25 ? -0.8 : 0.1, sleepy: t < 8.25, blink: t > 7.9 && t < 7.97,
    armF: [0.75, 0.55], armB: [-0.1, 0.9], cane: true, caneY: 0, bob: br, crownTilt: -0.14, crownDx: -6, headTilt: 0.05 });
  king(g, 'osric', { x: 1360, y: 790, s: 1.22, f: -1, old: true, lean: 0.13, mouth: oT, brow: 0.5, smile: 0.25, blink: t > 8.9 && t < 8.97,
    armF: [0.75, 0.55], armB: [-0.1, 0.9], cane: true, caneY: 0, bob: Math.sin(t * 2.6 + 1.3) * 1.5, crownTilt: 0.18, headTilt: 0.04 });
  bubble(g, t, 7.45, 9.4, 1330, 350, ['So… joint custody', 'of the goats?'], 170, 40);
  bubble(g, t, 8.2, 9.4, 590, 350, ['Fine. But I get', 'weekends.'], -170, 40);
  g.restore();
}

function render(t) {
  const g = ctx; g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';
  if (t < T.face) sceneMap(g, t); else if (t < T.card) sceneFace(g, t); else if (t < T.isle) sceneCard(g, t); else sceneIsle(g, t);
  g.setTransform(1, 0, 0, 1, 0, 0);
  captions(g, t);
  // opening: parchment unrolls into view; ending: fade back to bare parchment
  if (t < 0.2) { g.globalAlpha = 1 - eout(t / 0.2); g.drawImage(PARCH, 0, 0); g.globalAlpha = 1; }
  if (t > T.fade[0]) { g.globalAlpha = eio(seg(t, T.fade[0], T.fade[1])); g.drawImage(PARCH, 0, 0); g.globalAlpha = 1; }
  g.drawImage(GRAIN, 0, 0);
}

window.ready = (async () => {
  await Promise.all(['60px "Patrick Hand"', '900 54px Nunito', '40px "IM Fell English SC"', 'italic 40px "IM Fell English"'].map(f => document.fonts.load(f)));
  await document.fonts.ready;
  PARCH = parchment(W, H, 3); MAPC = buildMap(); GRAIN = grainLayer();
})();
window.draw = ({ t }) => { render(t); return cv.toDataURL('image/jpeg', 0.92).split(',')[1]; };
window.events = () => {
  const E = [];
  E.push({ k: 'music', s: 'jig', t: 0.05, e: T.face }, { k: 'music', s: 'coda', t: T.isle + 0.05, e: 10 });
  E.push({ k: 'pop', t: 0.12 }, { k: 'pop', t: 0.28, p: 0.6 });
  for (const b of [0.75, 1.55, 7.45, 8.2]) E.push({ k: 'bubble', t: b });
  E.push({ k: 'babble', t: 0.8, e: 1.5, v: 'h' }, { k: 'babble', t: 1.62, e: 2.42, v: 'o' }, { k: 'babble', t: 7.52, e: 8.57, v: 'o', old: 1 }, { k: 'babble', t: 8.3, e: 9.0, v: 'h', old: 1 });
  E.push({ k: 'drop', t: T.exit }, { k: 'whoosh', t: T.zoom[0] });
  for (const A of ARMY) E.push({ k: 'pop', t: A.t0, p: A.side * 0.5 }, { k: 'draw', t: A.a0, p: A.side * 0.5 });
  for (let i = 0; i < HOPS; i++) E.push({ k: 'drum', t: MARCH[0] + i * (MARCH[1] - MARCH[0]) / HOPS + 0.06 });
  E.push({ k: 'bonk', t: T.bump }, { k: 'bleat', t: T.bump + 0.06, p: 0 });
  E.push({ k: 'cut', t: T.face }, { k: 'sting', t: T.shock });
  E.push({ k: 'card', t: T.card }, { k: 'cut', t: T.isle }, { k: 'sea', t: T.isle, e: 10 }, { k: 'bleat', t: 9.18, p: 0.1 });
  return E.sort((a, b) => a.t - b.t);
};
