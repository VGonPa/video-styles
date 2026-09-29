// picture-book · the three spreads. Each spread is painted on an SW×SH canvas (two facing pages, gutter at GX).
const SW = 1760, SH = 940, GX = 880;
const P2 = { sage: '#a9b48c', sageL: '#c3c9a3', olive: '#86904f', moss: '#6e7c47', forest: '#55664a', deep: '#3f4f3c',
  bark: '#7b5a44', barkD: '#5b4334', peach: '#f1cfa7', sky: '#ece0c6', sun: '#f4cf7e', rose: '#e2a58e', mush: '#b9553f', fl1: '#e9c46a', fl2: '#e39a8a', fl3: '#f5ecd8' };
const FONT = '"Alegreya"';

// ── painted props ──
function roundTree(g, x, by, h, r, col, seed, o = {}) {
  const rr = rng(seed);
  const trunk = blob([[x - 16, by + 6], [x - 12, by - h * 0.5], [x - 8, by - h], [x + 8, by - h], [x + 12, by - h * 0.5], [x + 20, by + 6]], 0.5);
  paint(g, trunk, o.bark ?? P2.bark, seed, { edge: 6 }); pencil(g, trunk, { w: 2.4, seed, a: o.pa ?? 0.6 });
  // one scalloped canopy with a single pencil contour, shaded in washes (darker underside, light top-left)
  const cy = by - h - r * 0.4, ph = rr() * 6, pts = [];
  for (let i = 0; i < 72; i++) { const a = i / 72 * TAU, rad = r * (0.9 + 0.1 * Math.abs(Math.sin(a * 4.5 + ph))) * (1 + 0.05 * Math.sin(2 * a + ph));
    pts.push([x + Math.cos(a) * rad, cy + Math.sin(a) * rad * 0.88]); }
  const can = blob(pts);
  paint(g, can, col, seed + 1, { edge: 12, mottle: 0.45 });
  g.save(); g.clip(can);
  paint(g, wob(x + r * 0.25, cy + r * 0.62, r * 0.95, r * 0.5, seed + 2, 0.1, 10), shade(col, 0.8), seed + 4, { edge: 0, mottle: 0.35 });
  for (let i = 0; i < 3; i++) paint(g, wob(x - r * 0.35 + i * r * 0.3 + rr() * 10, cy - r * 0.42 + i * r * 0.12, r * 0.26, r * 0.17, seed + 50 + i, 0.12, 8), shade(col, 1.2), seed + 60 + i, { edge: 0, mottle: 0.2 });
  g.restore();
  pencil(g, can, { w: 2.4, seed: seed + 3, a: o.pa ?? 0.55 });
  hatch(g, can, seed + 71, { box: [x - r * 1.2, cy, x + r * 1.2, cy + r], sp: 13, ang: -1.1, len: 22, a: 0.2 });
}
function conifer(g, x, by, h, w, col, seed, o = {}) {
  const tr = poly([[x - 7, by + 4], [x - 5, by - h * 0.2], [x + 5, by - h * 0.2], [x + 7, by + 4]]); paint(g, tr, o.bark ?? P2.barkD, seed, { edge: 3 });
  for (let i = 0; i < 3; i++) { const yb = by - h * 0.15 - i * h * 0.26, ww = w * (1 - i * 0.24), top = yb - h * 0.45;
    const b = blob([[x - ww, yb], [x - ww * 0.35, (yb + top) / 2], [x, top], [x + ww * 0.35, (yb + top) / 2], [x + ww, yb], [x, yb + 10]], 0.7);
    paint(g, b, shade(col, 1 + i * 0.04), seed + i, { edge: 8 }); pencil(g, b, { w: 2, seed, a: o.pa ?? 0.45 }); }
}
function tuft(g, x, by, n, h, col, seed) {
  const r = rng(seed); g.save(); g.lineCap = 'round';
  for (let i = 0; i < n; i++) { const bx = x + (r() - 0.5) * 30, lean = (r() - 0.5) * 0.9, hh = h * (0.6 + r() * 0.5);
    g.strokeStyle = shade(col, 0.85 + r() * 0.3); g.globalAlpha = 0.85; g.lineWidth = 3 + r() * 2.5;
    g.beginPath(); g.moveTo(bx, by); g.quadraticCurveTo(bx + lean * hh * 0.3, by - hh * 0.6, bx + lean * hh, by - hh); g.stroke(); }
  g.restore();
}
function flower(g, x, by, h, col, seed) {
  const r = rng(seed); const st = new Path2D(); st.moveTo(x, by); st.quadraticCurveTo(x + (r() - 0.5) * 16, by - h / 2, x, by - h);
  g.save(); g.strokeStyle = P2.moss; g.lineWidth = 2.6; g.globalAlpha = 0.9; g.stroke(st); g.restore();
  for (let i = 0; i < 5; i++) { const a = i / 5 * TAU; paint(g, ell(x + Math.cos(a) * 7, by - h + Math.sin(a) * 7, 6.5, 5, a), col, seed + i, { edge: 2, mottle: 0.25 }); }
  g.fillStyle = '#c98a3a'; g.beginPath(); g.arc(x, by - h, 4, 0, TAU); g.fill();
}
function mushroom(g, x, by, s, seed) {
  const st = blob([[x - 7 * s, by], [x - 6 * s, by - 24 * s], [x + 6 * s, by - 24 * s], [x + 8 * s, by]], 0.6);
  paint(g, st, P2.fl3, seed, { edge: 3 }); pencil(g, st, { w: 1.8, seed, a: 0.5 });
  const cap = blob([[x - 24 * s, by - 20 * s], [x - 14 * s, by - 38 * s], [x, by - 44 * s], [x + 14 * s, by - 38 * s], [x + 24 * s, by - 20 * s], [x, by - 24 * s]], 0.8);
  paint(g, cap, P2.mush, seed + 1, { edge: 5 }); pencil(g, cap, { w: 2, seed: seed + 1, a: 0.6 });
  g.fillStyle = rgba(P2.fl3, 0.9); for (const [a, b] of [[-10, -32], [4, -38], [12, -28]]) { g.beginPath(); g.arc(x + a * s, by + b * s, 3 * s, 0, TAU); g.fill(); }
}
function hillBand(g, pts, bottom, col, seed, o = {}) {
  const top = pts.map(p => p.slice());
  const path = new Path2D(); const sp = sampleSpline(top, 80); path.moveTo(sp[0][0], bottom);
  for (const p of sp) path.lineTo(p[0], p[1]); path.lineTo(sp[sp.length - 1][0], bottom); path.closePath();
  paint(g, path, col, seed, { edge: o.edge ?? 14, mottle: o.mottle ?? 0.45, ssc: 2 });
  const ln = new Path2D(); ln.moveTo(sp[0][0], sp[0][1]); for (const p of sp) ln.lineTo(p[0], p[1]);
  pencil(g, ln, { w: 2.4, seed, a: o.pa ?? 0.4 });
  return path;
}
function skyRect(g, stops, seed, w = SW) {
  const gr = g.createLinearGradient(0, 0, 0, SH); for (const [o, c] of stops) gr.addColorStop(o, c);
  const p = new Path2D(); p.rect(-20, -20, w + 40, SH + 40);
  paint(g, p, gr, seed, { edge: 0, mottle: 0.12, lightA: 0.5, gran: 0.2, ssc: 2.5, streak: 0.8 });
}

// ── mask where the painting stops and bare paper carries the text (dry, ragged edge) ──
function textMask(pts, seed) {
  const c = mk(SW, SH), g = c.getContext('2d'), r = rng(seed);
  const sp = sampleSpline(pts, 160).map(([x, y], i) => [x + (r() - 0.5) * 9 + Math.sin(i * 0.7) * 3, y + (r() - 0.5) * 9]);
  g.filter = 'blur(2px)'; g.fillStyle = '#000'; g.beginPath(); g.moveTo(-40, -40); for (const p of sp) g.lineTo(p[0], p[1]); g.lineTo(-40, SH * 0.6); g.closePath(); g.fill();
  g.filter = 'none';
  // dry-brush flecks along the edge: paint breaking up into paper tooth
  for (let i = 0; i < 700; i++) { const p = sp[Math.floor(r() * sp.length)]; const d = (r() - 0.35) * 40;
    const k = sp.indexOf(p), q = sp[Math.min(sp.length - 1, k + 1)]; let nx = q[1] - p[1], ny = -(q[0] - p[0]); const m = Math.hypot(nx, ny) || 1;
    g.globalAlpha = 0.3 + r() * 0.7; g.beginPath(); g.ellipse(p[0] + nx / m * d, p[1] + ny / m * d, 1 + r() * 5, 0.8 + r() * 2.5, r() * 3, 0, TAU); g.fill(); }
  return c;
}
const MASK_PTS = [[-40, -40], [850, -40], [835, 90], [810, 220], [740, 330], [610, 400], [420, 430], [220, 440], [60, 430], [-40, 420]];

// ── scene 1: morning meadow ──
const L = {};
function initScenes() {
  L.mask = textMask(MASK_PTS, 3);
  // scene 1 static layers
  L.s1sky = mk(SW, SH); { const g = L.s1sky.getContext('2d');
    skyRect(g, [[0, '#f2d3b4'], [0.4, '#f6e0c4'], [0.68, '#f1e6cc']], 201);
    for (const [x, y, w, s] of [[1080, 150, 150, 1], [1250, 250, 110, 2], [420, 520, 130, 3]]) { const b = wob(x, y, w, w * 0.28, 300 + s, 0.12, 9);
      paint(g, b, '#f8ecd8', 310 + s, { edge: 0, mottle: 0.15, lightA: 0.5 }); } }
  L.s1hills = mk(SW, SH); { const g = L.s1hills.getContext('2d');
    hillBand(g, [[-20, 560], [300, 520], [620, 575], [980, 540], [1320, 585], [1560, 545], [1800, 560]], SH + 20, P2.sageL, 211, { mottle: 0.4 });
    hillBand(g, [[-20, 640], [260, 610], [560, 650], [900, 625], [1200, 660], [1500, 630], [1800, 650]], SH + 20, P2.sage, 212); }
  L.s1ground = mk(SW, SH); { const g = L.s1ground.getContext('2d');
    hillBand(g, [[-20, 720], [300, 700], [700, 735], [1000, 705], [1300, 718], [1560, 700], [1800, 715]], SH + 20, P2.olive, 221, { edge: 16 });
    // soft light path worn through the grass
    const path = blob([[980, 760], [1300, 770], [1560, 790], [1700, 830], [1500, 850], [1200, 820], [960, 800]], 0.8);
    paint(g, path, shade(P2.olive, 1.12), 222, { edge: 0, mottle: 0.3 });
    roundTree(g, 1630, 745, 330, 190, P2.moss, 231);
    // left page: bushes, mushrooms, flowers
    for (const [x, y, r, s] of [[150, 700, 90, 1], [300, 715, 60, 2], [620, 730, 70, 3]]) { const b = wob(x, y, r, r * 0.7, 240 + s, 0.1, 10);
      paint(g, b, P2.forest, 241 + s, { edge: 10 }); pencil(g, b, { w: 2.2, seed: 245, a: 0.5 }); }
    mushroom(g, 420, 800, 1.3, 251); mushroom(g, 470, 812, 0.9, 252); mushroom(g, 1540, 790, 1.0, 253);
    const r = rng(9); for (let i = 0; i < 26; i++) { const x = 40 + r() * 1680, y = 770 + r() * 150; if (Math.abs(x - GX) < 60 || (x > 1000 && x < 1470 && y < 850)) continue;
      flower(g, x, y, 22 + r() * 26, [P2.fl1, P2.fl2, P2.fl3][i % 3], 260 + i); }
    for (let i = 0; i < 40; i++) tuft(g, r() * SW, 740 + r() * 200, 6, 26, P2.moss, 300 + i); }
  L.s1fore = mk(SW, SH); { const g = L.s1fore.getContext('2d'); const r = rng(12);
    for (let i = 0; i < 28; i++) { const x = i / 27 * SW + (r() - 0.5) * 40; tuft(g, x, SH + 8, 9, 50 + r() * 40, P2.moss, 400 + i); } }

  // scene 2 parallax strips (world width WW)
  const WW = 2900;
  L.s2sky = mk(SW, SH); { const g = L.s2sky.getContext('2d'); skyRect(g, [[0, '#d6ddcb'], [0.35, '#e3e2cb'], [0.62, '#ece2c6']], 501);
    for (const [x, y, w, s] of [[1180, 170, 170, 1], [1480, 290, 120, 2], [1010, 330, 90, 3]]) { const b = wob(x, y, w, w * 0.26, 520 + s, 0.12, 9);
      paint(g, b, '#f6eedd', 530 + s, { edge: 0, mottle: 0.12, lightA: 0.5 }); }
    const sun = wob(1620, 150, 58, 58, 540, 0.02, 12); paint(g, sun, '#f3dca0', 541, { edge: 10, edgeA: 0.3, mottle: 0.15 }); }
  L.s2far = mk(WW, SH); { const g = L.s2far.getContext('2d');
    hillBand(g, [[-20, 560], [400, 520], [900, 560], [1400, 525], [1900, 565], [2400, 530], [2920, 550]], SH + 20, '#b9c2a4', 511, { mottle: 0.35, pa: 0.25 });
    const r = rng(21); for (let x = 30; x < WW; x += 70 + r() * 60) conifer(g, x, 600 + r() * 20, 120 + r() * 50, 34 + r() * 12, '#9fae92', 520 + x | 0, { pa: 0.25 }); }
  L.s2mid = mk(WW, SH); { const g = L.s2mid.getContext('2d'); const r = rng(22);
    for (let x = 80; x < WW; x += 230 + r() * 140) { if (r() < 0.5) roundTree(g, x, 700, 120 + r() * 40, 85 + r() * 20, '#7f8f5c', 600 + x | 0, { pa: 0.35 });
      else conifer(g, x, 705, 210 + r() * 40, 60, '#6f8261', 700 + x | 0, { pa: 0.35 }); } }
  L.s2ground = mk(WW, SH); { const g = L.s2ground.getContext('2d');
    hillBand(g, [[-20, 745], [500, 730], [1000, 750], [1500, 735], [2000, 752], [2500, 738], [2920, 745]], SH + 20, P2.olive, 801, { edge: 16 });
    const path = new Path2D(); path.moveTo(-20, 790); path.bezierCurveTo(800, 770, 1600, 800, 2920, 780); path.lineTo(2920, 860); path.bezierCurveTo(1800, 880, 900, 850, -20, 870); path.closePath();
    paint(g, path, '#c8b27f', 802, { edge: 8, mottle: 0.35 }); pencil(g, path, { w: 2, seed: 803, a: 0.35 });
    // a mossy log for Bear to sit by
    const log = blob([[2470, 800], [2480, 760], [2700, 752], [2720, 790], [2700, 812], [2490, 815]], 0.6);
    paint(g, log, P2.bark, 804, { edge: 8 }); pencil(g, log, { w: 2.4, seed: 805, a: 0.6 });
    paint(g, ell(2708, 782, 16, 28), '#c7a47c', 806, { edge: 5 });
    const r = rng(31);
    for (let i = 0; i < 16; i++) { const x = r() * WW, y = 760 + r() * 30; if (Math.abs(x - 2350) < 250) continue; mushroom(g, x, y + 10, 0.7 + r() * 0.5, 810 + i); }
    for (let i = 0; i < 44; i++) { const x = r() * WW, y = 880 + r() * 50; flower(g, x, y, 20 + r() * 26, [P2.fl1, P2.fl2, P2.fl3][i % 3], 830 + i); }
    for (let i = 0; i < 80; i++) tuft(g, r() * WW, 752 + r() * 190, 6, 24, P2.moss, 900 + i); }
  L.s2fore = mk(3600, SH); { const g = L.s2fore.getContext('2d');
    for (const [x, s] of [[150, 1], [700, 2], [1450, 3], [2150, 4], [3100, 5]]) { const r = rng(1000 + s);
      for (let k = 0; k < 7; k++) { const a = -Math.PI / 2 + (k - 3) * 0.32 + (r() - 0.5) * 0.1, len = 150 + r() * 90;
        const cen = []; for (let j = 0; j <= 8; j++) { const u = j / 8; cen.push([x + Math.cos(a) * len * u + u * u * 40 * Math.sign(k - 3), SH + 20 + Math.sin(a) * len * u + u * u * 50]); }
        const fr = poly(ribbon(cen, cen.map((_, j) => 16 * Math.sin(Math.PI * Math.min(1, (j + 1) / 9)) + 2)));
        paint(g, fr, k % 2 ? P2.deep : '#4c5e44', 1010 + s * 10 + k, { edge: 5, mottle: 0.4 }); pencil(g, fr, { w: 2, seed: 1020 + k, a: 0.5 }); } } }

  // scene 3 vignette
  L.s3vig = mk(SW, SH); { const g = L.s3vig.getContext('2d');
    const cx = 440, cy = 470, R = 300; const cl = wob(cx, cy, R, R, 77, 0.02, 18);
    g.save(); g.clip(cl);
    skyRect(g, [[0.15, '#e7b89c'], [0.5, '#efcfa6'], [0.72, '#f3dfb4']], 1101);
    g.fillStyle = rgba('#fff4dc', 0.9); g.beginPath(); g.arc(560, 290, 34, 0, TAU); g.fill(); g.fillStyle = '#ecc39f'; g.beginPath(); g.arc(575, 280, 30, 0, TAU); g.fill();
    for (const [x, y] of [[300, 240], [360, 300], [470, 220], [640, 380], [250, 360]]) sparkle(g, x, y, 7, 0.9);
    hillBand(g, [[100, 600], [300, 575], [500, 600], [800, 580]], 800, P2.sage, 1102);
    hillBand(g, [[100, 690], [300, 670], [500, 682], [800, 668]], 800, P2.olive, 1103);
    conifer(g, 225, 690, 190, 48, P2.forest, 1104); conifer(g, 670, 680, 160, 42, P2.forest, 1105);
    g.restore();
    // ragged painted rim
    g.save(); g.globalAlpha = 0.5; g.strokeStyle = pat('dark', 5); g.lineWidth = 10; g.stroke(cl); g.restore();
    pencil(g, cl, { w: 3, seed: 1106, a: 0.6 });
    // small ornament under "The End"
    const lf = (x, y, a, s) => { g.save(); g.translate(x, y); g.rotate(a); const p = blob([[0, 0], [22 * s, -10 * s], [46 * s, 0], [22 * s, 10 * s]], 0.9); paint(g, p, P2.moss, 1110 + x | 0, { edge: 4 }); pencil(g, p, { w: 1.6, seed: 1111, a: 0.6 }); g.restore(); };
    const stem = new Path2D(); stem.moveTo(1180, 600); stem.quadraticCurveTo(1320, 640, 1460, 600); g.save(); g.strokeStyle = P2.moss; g.lineWidth = 3; g.stroke(stem); g.restore();
    lf(1200, 606, -0.5, 1); lf(1250, 620, 0.3, 0.9); lf(1390, 620, -0.3 + Math.PI, 0.9); lf(1440, 606, 0.5 + Math.PI, 1);
  }
}

// ── text block on bare paper ──
function textBlock(g, t, spec) {
  g.save(); g.textBaseline = 'alphabetic';
  for (const ln of spec) {
    const u = seg(t, ln.t, ln.t + 0.6); if (u <= 0) continue;
    g.globalAlpha = eSine(u); const dy = (1 - eOut(u)) * 10;
    if (ln.cap) { g.font = `700 150px ${FONT}`; g.fillStyle = '#b3593f'; g.fillText(ln.cap, ln.x, ln.y + dy); continue; }
    g.font = `${ln.italic ? 'italic ' : ''}400 ${ln.size ?? 44}px ${FONT}`; g.fillStyle = '#4a3426'; g.fillText(ln.s, ln.x, ln.y + dy);
  }
  g.restore();
}
const TX1 = [
  { cap: 'O', x: 96, y: 218, t: 0.35 },
  { s: 'nce upon a morning, in the', x: 212, y: 150, t: 0.45 },
  { s: 'long grass, a little fox woke up.', x: 212, y: 210, t: 0.6 },
  { s: 'And there, right by her nose,', x: 100, y: 285, t: 1.85 },
  { s: 'was a button, small and blue.', x: 100, y: 345, t: 2.0 },
];
const TX2 = [
  { s: 'She carried it through the woods,', x: 100, y: 150, t: 3.75 },
  { s: 'past ferns and whispering oaks…', x: 100, y: 210, t: 3.9 },
  { s: '“My button!” cried Bear.', x: 100, y: 285, t: 6.25, italic: true },
  { s: '“Thank you, little fox.”', x: 100, y: 345, t: 6.45, italic: true },
];

// ── live scene renderers (g = spread canvas context, IL = illustration scratch canvas) ──
function finishSpread(g, il, t, tx) {
  const x = il.getContext('2d');
  x.globalCompositeOperation = 'destination-out'; x.drawImage(L.mask, 0, 0); x.globalCompositeOperation = 'source-over';
  g.fillStyle = C.paper; g.fillRect(0, 0, SW, SH);
  g.drawImage(il, 0, 0);
  if (tx) textBlock(g, t, tx);
}

function scene1(g, il, t) {
  const x = il.getContext('2d'); x.clearRect(0, 0, SW, SH);
  x.drawImage(L.s1sky, 0, 0);
  // sun rising behind the hills
  const sy = lerp(640, 455, eOut(seg(t, 0, 2.8)));
  const sun = wob(1330, sy, 88, 88, 55, 0.015, 14); paint(x, sun, P2.sun, 55, { edge: 16, edgeA: 0.45, mottle: 0.2, lightA: 0.35 });
  x.save(); x.globalAlpha = 0.22; x.fillStyle = '#fbe3b0'; x.beginPath(); x.arc(1330, sy, 135, 0, TAU); x.fill(); x.globalAlpha = 0.12; x.beginPath(); x.arc(1330, sy, 190, 0, TAU); x.fill(); x.restore();
  x.drawImage(L.s1hills, 0, 0);
  // two birds crossing the sky
  for (const [bx0, by0, sp, ph] of [[980, 250, 150, 0], [1060, 205, 135, 1.7]]) {
    const bx = bx0 + t * sp, by = by0 - t * 12 + Math.sin(t * 3 + ph) * 6, f = Math.sin(t * 13 + ph) * 12;
    const p = new Path2D(); p.moveTo(bx - 16, by - f * 0.6); p.quadraticCurveTo(bx - 7, by - 6 - f * 0.3, bx, by); p.quadraticCurveTo(bx + 7, by - 6 - f * 0.3, bx + 16, by - f * 0.6);
    pencil(x, p, { w: 3, seed: 57, a: 0.8 }); }
  x.drawImage(L.s1ground, 0, 0);
  // fox: sleep → wake (anticipation squash, rise with overshoot) → curious tilt → trot → dip for the button
  const wake = eBack(seg(t, 1.2, 1.7), 1.6), trot = eInOut(seg(t, 2.05, 2.6));
  const dip = Math.sin(Math.PI * seg(t, 2.6, 3.05));
  const P = { crouch: clamp(1 - wake) * 1 + dip * 0.5, headUp: clamp(eBack(seg(t, 1.1, 1.55), 2.2), 0, 1.15), eye: t < 1.2 ? 0 : (Math.abs(t - 1.52) < 0.05 ? 0 : 1),
    tail: eInOut(seg(t, 1.26, 1.5)), perk: t < 1.3 ? 0.2 : eBack(seg(t, 1.3, 1.65), 3), breathe: t < 1.1 ? Math.sin(t * 5.2) : 0,
    squash: Math.sin(Math.PI * seg(t, 0.95, 1.2)) * 0.8, headAng: Math.sin(Math.PI * seg(t, 1.8, 2.05)) * -0.22 + dip * 1.1,
    walk: Math.sin(Math.PI * seg(t, 2.05, 2.6)), wag: Math.sin(t * 7) * 0.12 * seg(t, 1.6, 2.0) };
  const fx = lerp(1100, 1285, trot); P.ph = (fx - 1100) / 100 * TAU;
  const got = t >= 2.83; P.button = got;
  drawFox(x, fx, 792, 1.15, P);
  if (!got) { drawButton(x, 1393, 776, 14, 0.4, 61); sparkle(x, 1403, 764, 22 * Math.sin(Math.PI * seg(t, 1.7, 2.1)), Math.sin(Math.PI * seg(t, 1.7, 2.1))); }
  x.drawImage(L.s1fore, 0, 0);
  finishSpread(g, il, t, TX1);
}

const S2 = { t0: 3.3, t1: 5.5, D: 900, FX: 1000, BX: 1450 };
// eased scroll: half smoothstep + half ease-out → starts gently, glides to a stop
function s2scroll(t) { const u = seg(t, S2.t0, S2.t1); return S2.D * (u * u * (3 - 2 * u) * 0.5 + (1 - Math.pow(1 - u, 2)) * 0.5); }
function scene2(g, il, t) {
  const x = il.getContext('2d'); x.clearRect(0, 0, SW, SH);
  const X = s2scroll(t);
  x.drawImage(L.s2sky, 0, 0);
  x.drawImage(L.s2far, -X * 0.15, 0);
  x.drawImage(L.s2mid, -X * 0.45, 0);
  x.drawImage(L.s2ground, -X, 0);
  // bear by the log
  const bxs = S2.BX + S2.D - X;
  const hand = seg(t, 5.55, 6.35), fly = seg(t, 5.82, 6.22), land = t >= 6.22;
  const hp = eOut(seg(t, 6.25, 6.6));
  drawBear(x, bxs, 812, 0.9, { happy: hp, breathe: Math.sin(t * 2.4), tilt: hp * 0.12 * Math.cos((t - 6.25) * 6) * Math.exp(-(t - 6.25) * 1.5) * (t > 6.25 ? 1 : 0) - hp * 0.05,
    button: land, wave: eBack(seg(t, 6.55, 6.9), 1.4) * (1 - eInOut(seg(t, 7.3, 7.6))) * (2.55 + Math.sin((t - 6.55) * 11) * 0.22), btnScale: land ? eBack(seg(t, 6.22, 6.45), 3) : 1, blink: Math.abs(t - 4.9) < 0.05 ? 0.1 : 1 });
  // fox trotting on the spot while the woods slide past (steps locked to the ground speed)
  const dX = (s2scroll(t + 0.02) - X) / 0.02;
  const toss = Math.sin(Math.PI * seg(t, 5.55, 5.78)) * 0.5 - Math.sin(Math.PI * seg(t, 5.72, 5.95)) * 0.35;
  const P = { walk: clamp(dX / 450), ph: X / 150 * TAU, headAng: toss, button: t < 5.82, tail: 1, perk: 1 + 0.15 * Math.sin(Math.PI * seg(t, 6.25, 6.6)),
    wag: Math.sin(t * 9) * 0.22 * seg(t, 6.2, 6.5) + Math.sin(t * 4) * 0.05, eye: Math.abs(t - 4.3) < 0.05 ? 0 : 1 };
  const s = 0.95, fy = 800;
  drawFox(x, S2.FX, fy, s, P);
  if (fly > 0 && !land) {
    const m = foxMouthLocal({ ...P, headAng: 0 }); const ax = S2.FX + m[0] * s, ay = fy + m[1] * s;
    const bx = bxs - 20 * 0.9, by = 812 - 163 * 0.9; const k = eInOut(fly);
    drawButton(x, lerp(ax, bx, k), lerp(ay, by, k) - Math.sin(Math.PI * k) * 150, 13 * 0.95, k * 9, 61);
  }
  sparkle(x, bxs - 20 * 0.9 + 24, 812 - 163 * 0.9 - 22, 26 * Math.sin(Math.PI * seg(t, 6.22, 6.65)), Math.sin(Math.PI * seg(t, 6.22, 6.65)));
  x.drawImage(L.s2fore, -X * 1.5, 0);
  finishSpread(g, il, t, TX2);
}

function scene3(g, il, t) {
  g.fillStyle = C.paper; g.fillRect(0, 0, SW, SH);
  g.drawImage(L.s3vig, 0, 0);
  // characters inside the vignette: Bear dozing, the fox curled up asleep against him
  g.save(); g.beginPath(); g.arc(440, 470, 296, 0, TAU); g.clip();
  drawBear(g, 515, 698, 0.62, { happy: 1, eyesClosed: 1, breathe: Math.sin(t * 2), button: true });
  drawFox(g, 405, 704, 0.6, { crouch: 1, headUp: 0, eye: 0, tail: 0, perk: 0.3, breathe: Math.sin(t * 4.5) });
  g.restore();
  g.save(); g.textAlign = 'center';
  const u = seg(t, 8.5, 9.0);
  g.globalAlpha = eSine(u); g.font = `italic 400 132px ${FONT}`; g.fillStyle = '#4a3426';
  g.fillText('The End', 1320, 520 + (1 - eOut(u)) * 14);
  g.restore();
}
