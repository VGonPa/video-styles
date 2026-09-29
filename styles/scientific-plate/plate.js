// scientific-plate · scene composition: paper, watercolour tints, labels, reading glass, page turn, plate XV.
// (loaded by anim.html after the specimen generators)
let PAPER14, PAPER15, GRANPAT, VIG, LENS_RIM, LENS_SH, CACHE14 = null, PLATE15, FIGS, FIGS15;

// ── aged paper: tone blotches, fibres, foxing, the intaglio plate-mark and the printed border ──
function buildPaper(seed, plateName) {
  const c = mk(W, H), x = c.getContext('2d'), r = rng(seed);
  x.fillStyle = rgba(PAPERC, 1); x.fillRect(0, 0, W, H);
  const lo = mk(240, 135), lx = lo.getContext('2d'), li = lx.createImageData(240, 135);
  for (let j = 0; j < 135; j++) for (let i = 0; i < 240; i++) { const n = fbm(i / 38, j / 38, seed, 5), m = fbm(i / 9, j / 9, seed + 5, 3);
    const ex = Math.min(i, 239 - i) / 240, ey = Math.min(j, 134 - j) / 135, e = Math.pow(1 - clamp(Math.min(ex * 5.5, ey * 4.5)), 2.2);
    const k = (i + j * 240) * 4, dark = (n - .5) * 34 + (m - .5) * 10 + e * 40;
    li.data[k] = 150; li.data[k + 1] = 112; li.data[k + 2] = 60; li.data[k + 3] = clamp(dark / 80 + .08) * 255; }
  lx.putImageData(li, 0, 0); x.imageSmoothingQuality = 'high'; x.globalAlpha = .55; x.drawImage(lo, 0, 0, W, H); x.globalAlpha = 1;
  // fibres + fine grain
  const id = x.getImageData(0, 0, W, H), d = id.data;
  for (let k = 0, i = 0; k < d.length; k += 4, i++) { const px = i % W, py = (i / W) | 0; const g = (hash2(px, py, seed) - .5) * 9 + (vnoise(px / 2.2, py / 14, seed + 3) - .5) * 6;
    d[k] += g; d[k + 1] += g; d[k + 2] += g * .9; }
  x.putImageData(id, 0, 0);
  // foxing: small rust spots, clustered toward the edges
  for (let i = 0; i < 70; i++) { let px = r() * W, py = r() * H; if (r() < .7) { if (r() < .5) px = r() < .5 ? r() * 190 : W - r() * 190; else py = r() < .5 ? r() * 150 : H - r() * 150; }
    const rr = 1.5 + Math.pow(r(), 3) * 11, g = x.createRadialGradient(px, py, 0, px, py, rr); g.addColorStop(0, `rgba(140,82,36,${.22 + r() * .25})`); g.addColorStop(1, 'rgba(140,82,36,0)');
    x.fillStyle = g; x.beginPath(); x.arc(px, py, rr, 0, TAU); x.fill(); }
  // plate-mark: the pressed rectangle (inside slightly toned, bevel light/shadow)
  const pm = 30; x.fillStyle = 'rgba(120,88,44,0.045)'; x.fillRect(pm, pm, W - 2 * pm, H - 2 * pm);
  x.save(); x.filter = 'blur(1.2px)';
  x.strokeStyle = 'rgba(255,248,230,0.55)'; x.lineWidth = 2; x.beginPath(); x.moveTo(pm + 1, H - pm); x.lineTo(pm + 1, pm + 1); x.lineTo(W - pm, pm + 1); x.stroke();
  x.strokeStyle = 'rgba(90,62,30,0.32)'; x.beginPath(); x.moveTo(W - pm - 1, pm); x.lineTo(W - pm - 1, H - pm - 1); x.lineTo(pm, H - pm - 1); x.stroke();
  x.strokeStyle = 'rgba(90,62,30,0.22)'; x.beginPath(); x.moveTo(pm + 3, H - pm); x.lineTo(pm + 3, pm + 3); x.lineTo(W - pm, pm + 3); x.stroke();
  x.restore();
  // printed border: heavy rule + fine inner rule
  x.strokeStyle = INK; x.globalAlpha = .92; x.lineWidth = 2.6; x.strokeRect(58, 56, W - 116, H - 112); x.lineWidth = .9; x.strokeRect(67, 65, W - 134, H - 130); x.globalAlpha = 1;
  return c;
}
function buildGran() {
  const c = mk(256, 256), x = c.getContext('2d'), r = rng(5), id = x.createImageData(256, 256);
  for (let j = 0; j < 256; j++) for (let i = 0; i < 256; i++) { const n = vnoise(i / 3, j / 3, 9) * .6 + vnoise(i / 11, j / 11, 12) * .4; const k = (i + j * 256) * 4;
    id.data[k] = 70; id.data[k + 1] = 44; id.data[k + 2] = 24; id.data[k + 3] = Math.pow(clamp((n - .45) * 2.2), 1.6) * 150 + (r() < .02 ? 90 : 0); }
  x.putImageData(id, 0, 0); return c;
}
// ── watercolour tint for a static specimen (2× resolution, layered jittered washes, pooled edges, blots) ──
function paintRegion(x, R, seed) {
  const col = R.col, al = R.a || 1, sd = seed * 13 + (R.seed || 0) * 7;
  const jit = L => R.pts.map(([px, py]) => [px + (fbm(px * .03, py * .03, sd + L) - .5) * 6, py + (fbm(px * .03 + 9, py * .03, sd + L + 3) - .5) * 6]);
  const j0 = jit(0);
  for (let L = 0; L < 3; L++) { x.fillStyle = rgba(col, .27 * al); x.fill(polyPath(L ? jit(L) : j0)); }
  x.save(); x.filter = 'blur(2px)'; x.strokeStyle = rgba(col.map(v => v * .72), .3 * al); x.lineWidth = 2.4; x.stroke(polyPath(j0)); x.restore();
  x.save(); x.clip(polyPath(j0)); const r = rng(sd);
  const xs = R.pts.map(p => p[0]), ys = R.pts.map(p => p[1]), bx0 = Math.min(...xs), bx1 = Math.max(...xs), by0 = Math.min(...ys), by1 = Math.max(...ys);
  for (let i = 0; i < 7; i++) { const px = lerp(bx0, bx1, r()), py = lerp(by0, by1, r()), rr = 8 + r() * Math.max(12, (bx1 - bx0) * .35);
    const c2 = R.blot && r() < .6 ? R.blot : (r() < .5 ? col.map(v => v * .85) : [248, 240, 222]);
    const g = x.createRadialGradient(px, py, 0, px, py, rr); g.addColorStop(0, rgba(c2, .2 * al)); g.addColorStop(1, rgba(c2, 0)); x.fillStyle = g; x.fillRect(px - rr, py - rr, 2 * rr, 2 * rr); }
  // light from the upper left: a soft darker pool toward the lower right of each region
  const g = x.createLinearGradient(bx0, by0, bx1, by1); g.addColorStop(0, 'rgba(255,250,236,0.18)'); g.addColorStop(.5, 'rgba(255,250,236,0)'); g.addColorStop(1, rgba(col.map(v => v * .6), .18 * al));
  x.fillStyle = g; x.fillRect(bx0, by0, bx1 - bx0, by1 - by0);
  x.restore();
}
function buildTint(S) {
  const [x0, y0, x1, y1] = S.bbox, s = 2, c = mk(Math.ceil((x1 - x0) * s), Math.ceil((y1 - y0) * s)), x = c.getContext('2d');
  x.setTransform(s, 0, 0, s, -x0 * s, -y0 * s);
  for (const R of S.regions) paintRegion(x, R, S.seed);
  x.setTransform(1, 0, 0, 1, 0, 0); x.globalCompositeOperation = 'source-atop'; x.globalAlpha = .55; x.fillStyle = x.createPattern(GRANC, 'repeat'); x.fillRect(0, 0, c.width, c.height);
  S.tint = c;
  S.wR = Math.max(...[[x0, y0], [x1, y0], [x0, y1], [x1, y1]].map(([px, py]) => Math.hypot(px - S.wash[0], py - S.wash[1]))) * 1.35;
}
let GRANC;
// ── progressive engraving ──
function drawStrokes(c, S, p) {
  if (p <= 0) return; const target = p * S.total; let acc = 0, key = null, path = null;
  c.strokeStyle = INK; c.lineCap = 'round'; c.lineJoin = 'round';
  const flush = () => { if (path) c.stroke(path); path = null; };
  for (const s of S.strokes) {
    if (acc >= target) break; const k = s.w + '|' + s.a;
    if (k !== key) { flush(); key = k; path = new Path2D(); c.lineWidth = s.w; c.globalAlpha = s.a; }
    const rem = target - acc, frac = rem >= s.tl ? 1 : rem / s.tl, lim = frac * s.len; let l = 0;
    path.moveTo(...s.pts[0]);
    for (let i = 1; i < s.pts.length; i++) { const [ax, ay] = s.pts[i - 1], [bx, by] = s.pts[i], sl = Math.hypot(bx - ax, by - ay);
      if (l + sl >= lim) { const u = sl ? (lim - l) / sl : 0; path.lineTo(ax + (bx - ax) * u, ay + (by - ay) * u); break; } path.lineTo(bx, by); l += sl; }
    acc += s.tl;
  }
  flush(); c.globalAlpha = 1;
}
function drawTint(c, S, q) {
  if (q <= 0) return; const [x0, y0, x1, y1] = S.bbox;
  c.save(); if (q < 1) washClip(c, S.wash[0], S.wash[1], S.wR, q, S.seed % 50);
  c.globalCompositeOperation = 'multiply'; c.drawImage(S.tint, x0 + 2, y0 + 1, x1 - x0, y1 - y0); c.restore();
}
// ── inked text: revealed left→right like a fresh impression ──
function inkText(c, str, x, y, font, t0, dur = .45, align = 'center', ls = '0px', alpha = 1) {
  const u = seg(TNOW, t0, t0 + dur); if (u <= 0) return;
  c.save(); c.font = font; c.letterSpacing = ls; c.textAlign = align; c.textBaseline = 'alphabetic';
  const w = c.measureText(str).width, lx = align === 'center' ? x - w / 2 : align === 'right' ? x - w : x;
  if (u < 1) { c.beginPath(); c.rect(lx - 10, y - 80, (w + 20) * eOut(u), 120); c.clip(); }
  c.fillStyle = INK; c.globalAlpha = alpha * (.35 + .65 * clamp(u * 1.6)); c.fillText(str, x, y); c.restore();
}
function figLabel(c, n, name, X, y, t0) {
  c.save(); c.font = `29px ${IT}`; const wN = c.measureText(name).width; c.font = `27px ${SC}`; const wn = c.measureText(n + '. ').width; c.restore();
  const lx = X - (wN + wn) / 2; inkText(c, n + '. ', lx, y, `27px ${SC}`, t0, .2, 'left'); inkText(c, name, lx + wn, y, `29px ${IT}`, t0 + .08, .45, 'left');
}
let TNOW = 0;
function header(c, t0, plate, sub) {
  inkText(c, plate, W / 2, 132, `48px ${SC}`, t0, .3, 'center', '9px');
  const u = eOut(seg(TNOW, t0 + .15, t0 + .55)); if (u > 0) { c.strokeStyle = INK; c.lineWidth = .9; c.globalAlpha = .9;
    for (const [yy, hw] of [[152, 170], [157, 120]]) { c.beginPath(); c.moveTo(W / 2 - hw * u, yy); c.lineTo(W / 2 + hw * u, yy); c.stroke(); } c.globalAlpha = 1; }
  inkText(c, sub, W / 2, 196, `31px ${IT}`, t0 + .2, .5);
}
// ── plate XIV ──
function buildFigs() {
  FIGS = [
    { S: parasol(250, B, 1.12, 101), n: 1, name: 'Parasolia vesperalis', t0: .95, t1: 2.3, w0: 2.1, lt: 2.7 },
    { S: bells(575, B, 1.1, 202), n: 2, name: 'Tintinnabula gregaria', t0: .6, t1: 1.95, w0: 1.8, lt: 2.5 },
    { S: bracket(1360, B, 404), n: 4, name: 'Tabulella annulata', t0: .75, t1: 2.1, w0: 1.95, lt: 2.6 },
    { S: morel(1670, B, 1.12, 505), n: 5, name: 'Favomyces reticulatus', t0: 1.1, t1: 2.45, w0: 2.25, lt: 2.8 },
  ];
  for (const F of FIGS) buildTint(F.S);
  FIGS15 = [
    { S: parasol(470, B + 10, 1.36, 606), n: 6, name: 'Parasolia gigantea' },
    { S: morel(1010, B + 10, 1.2, 707), n: 7, name: 'Favomyces elatus' },
    { S: bells(1420, B + 10, 1.25, 808, [{ bx: -10, tx: -26, ty: -250, tilt: -.14, s: 1.15 }, { bx: 16, tx: 44, ty: -150, tilt: .3, s: .8 }]), n: 8, name: 'Tintinnabula solitaria' },
  ];
  for (const F of FIGS15) buildTint(F.S);
}
const HERO = { t0: .35, t1: 1.75, w0: 1.6, lt: 2.35 };
const LEAD = [{ ch: 'a', x: 772, y: B - 352, t: 3.0 }, { ch: 'b', x: 772, y: B - 250, t: 3.12 }, { ch: 'c', x: 772, y: B - 128, t: 3.24 }];
function heroTargets(hb) {
  const { C, rays } = hb, a = HA; const R = rays[3], j = Math.round((R.C.length - 1) * .5);
  return [[C[0] - 4, C[1] - a * 1.2], [C[0] + a * Math.cos(208 * DEG), C[1] + a * Math.sin(208 * DEG)], [R.L[j][0], R.L[j][1]]];
}
function drawPlate14(c, t) {
  TNOW = t;
  c.drawImage(PAPER14, 0, 0);
  header(c, T.head, 'PLATE XIV.', 'Specimens of Imaginary Fungi.');
  for (const F of FIGS) drawTint(c, F.S, seg(t, F.w0, F.w0 + .85));
  const hb = drawHero(c, t, seg(t, HERO.t0, HERO.t1), seg(t, HERO.w0, HERO.w0 + .85));
  for (const F of FIGS) drawStrokes(c, F.S, eSine(seg(t, F.t0, F.t1)));
  for (const F of FIGS) figLabel(c, F.n, F.name, F.S.cx, B + 62, F.lt);
  figLabel(c, 3, 'Astrocalyx mirabilis', HX, B + 62, HERO.lt);
  // leader letters
  const tg = heroTargets(hb);
  for (const [i, L] of LEAD.entries()) { inkText(c, L.ch, L.x, L.y + 8, `italic 27px ${IT}`, L.t, .2);
    const u = eOut(seg(t, L.t + .1, L.t + .45)); if (u > 0) { const sx = L.x + 13, sy = L.y, [tx, ty] = tg[i];
      c.strokeStyle = INK; c.lineWidth = .9; c.beginPath(); c.moveTo(sx, sy); c.lineTo(lerp(sx, tx, u), lerp(sy, ty, u)); c.stroke(); } }
  inkText(c, 'Fig. 3 is shown closed. It opens only when observed.', W / 2, 936, `italic 30px ${GAR}`, 3.15, .6);
  inkText(c, 'H. Ashgrove del.', 96, 995, `italic 21px ${GAR}`, 3.3, .3, 'left');
  inkText(c, 'E. Quill sculp.', W - 96, 995, `italic 21px ${GAR}`, 3.35, .3, 'right');
  return hb;
}
function buildPlate15() {
  const c = mk(W, H), x = c.getContext('2d'); TNOW = 99;
  x.drawImage(PAPER15, 0, 0);
  header(x, 0, 'PLATE XV.', 'Specimens of Imaginary Fungi, continued.');
  for (const F of FIGS15) { drawTint(x, F.S, 1); }
  for (const F of FIGS15) { drawStrokes(x, F.S, 1); figLabel(x, F.n, F.name, F.S.cx, B + 72, 0); }
  // Fig. 6a — spores, much enlarged, in a ruled roundel
  const rx = 1690, ry = 420, rr = 118; const r = rng(66);
  x.fillStyle = 'rgba(214,190,150,0.35)'; x.beginPath(); x.arc(rx, ry, rr, 0, TAU); x.fill();
  x.strokeStyle = INK; x.lineWidth = 2; x.beginPath(); x.arc(rx, ry, rr, 0, TAU); x.stroke(); x.lineWidth = .8; x.beginPath(); x.arc(rx, ry, rr - 7, 0, TAU); x.stroke();
  for (let i = 0; i < 16; i++) { const a = r() * TAU, d = Math.sqrt(r()) * (rr - 34), px = rx + Math.cos(a) * d, py = ry + Math.sin(a) * d, ro = r() * Math.PI;
    x.save(); x.translate(px, py); x.rotate(ro); x.fillStyle = 'rgba(168,112,70,0.5)'; x.beginPath(); x.ellipse(0, 0, 15, 9, 0, 0, TAU); x.fill();
    x.lineWidth = 1.2; x.stroke(); x.lineWidth = .6; for (let k = -2; k <= 2; k++) { x.beginPath(); x.moveTo(k * 4 + 2, -7); x.lineTo(k * 4 + 3, 7); if (k > -1) x.stroke(); }
    x.beginPath(); x.arc(-4, -2, 2.2, 0, TAU); x.fill(); x.restore(); }
  inkText(x, '6a. Spores, much enlarged.', rx, ry + rr + 44, `italic 27px ${IT}`, 0);
  inkText(x, 'H. Ashgrove del.', 96, 995, `italic 21px ${GAR}`, 0, .3, 'left');
  inkText(x, 'E. Quill sculp.', W - 96, 995, `italic 21px ${GAR}`, 0, .3, 'right');
  return c;
}
// ── reading glass sprites (brass rim + turned-wood handle, and its soft shadow) ──
const LR = 250, MAG = 1.42, HANG = 48 * DEG;
function buildLens() {
  const S = 1100, c = mk(S, S), x = c.getContext('2d'), o = 330;          // lens centre at (o,o) in sprite
  const sh = mk(S, S), y = sh.getContext('2d');
  const handle = (g, fill) => { g.save(); g.translate(o, o); g.rotate(HANG); g.translate(LR + 8, 0);
    g.fillStyle = fill ?? '#000'; if (!fill) { g.fillRect(0, -13, 62, 26); g.beginPath(); g.roundRect(56, -21, 330, 42, 21); g.fill(); g.restore(); return; }
    const gm = g.createLinearGradient(0, -14, 0, 14); gm.addColorStop(0, '#e8c67a'); gm.addColorStop(.45, '#9c7432'); gm.addColorStop(1, '#4e3413');
    g.fillStyle = gm; g.fillRect(0, -12, 64, 24); g.strokeStyle = 'rgba(40,24,8,.8)'; g.lineWidth = 1.5; g.strokeRect(0, -12, 64, 24);
    for (const xx of [16, 30, 46]) { g.beginPath(); g.moveTo(xx, -12); g.lineTo(xx, 12); g.stroke(); }
    const gw = g.createLinearGradient(0, -21, 0, 21); gw.addColorStop(0, '#8a4f2a'); gw.addColorStop(.35, '#5e3016'); gw.addColorStop(1, '#261006');
    g.fillStyle = gw; g.beginPath(); g.roundRect(58, -20, 330, 40, 20); g.fill(); g.stroke();
    g.strokeStyle = 'rgba(255,220,180,.25)'; g.lineWidth = 3; g.beginPath(); g.moveTo(80, -11); g.lineTo(370, -11); g.stroke();
    for (let i = 0; i < 26; i++) { g.strokeStyle = `rgba(20,8,2,${.12 + (i % 3) * .05})`; g.lineWidth = 1; g.beginPath(); g.moveTo(66 + i * 12, -19); g.bezierCurveTo(70 + i * 12, -5, 62 + i * 12, 6, 70 + i * 12, 19); g.stroke(); }
    g.restore(); };
  // shadow
  y.filter = 'blur(16px)'; y.strokeStyle = '#000'; y.lineWidth = 26; y.beginPath(); y.arc(o, o, LR + 4, 0, TAU); y.stroke(); handle(y, null);
  y.fillStyle = 'rgba(0,0,0,.28)'; y.beginPath(); y.arc(o, o, LR - 6, 0, TAU); y.fill();
  // rim
  handle(x, true);
  const gr = x.createLinearGradient(o - LR, o - LR, o + LR, o + LR); gr.addColorStop(0, '#f2d48a'); gr.addColorStop(.35, '#b88a3c'); gr.addColorStop(.6, '#7a5520'); gr.addColorStop(.85, '#c89a48'); gr.addColorStop(1, '#5a3a12');
  x.strokeStyle = gr; x.lineWidth = 22; x.beginPath(); x.arc(o, o, LR + 9, 0, TAU); x.stroke();
  x.strokeStyle = 'rgba(40,24,6,.85)'; x.lineWidth = 1.6; for (const rr of [LR - 2, LR + 20]) { x.beginPath(); x.arc(o, o, rr, 0, TAU); x.stroke(); }
  x.strokeStyle = 'rgba(255,240,200,.55)'; x.lineWidth = 2; x.beginPath(); x.arc(o, o, LR + 13, 200 * DEG, 290 * DEG); x.stroke();
  // glass: highlight crescents
  x.save(); x.beginPath(); x.arc(o, o, LR - 2, 0, TAU); x.clip();
  const gi = x.createRadialGradient(o, o, LR * .55, o, o, LR); gi.addColorStop(0, 'rgba(40,26,10,0)'); gi.addColorStop(1, 'rgba(40,26,10,0.22)'); x.fillStyle = gi; x.fillRect(0, 0, S, S);
  x.filter = 'blur(6px)'; x.strokeStyle = 'rgba(255,252,240,.32)'; x.lineWidth = 16; x.beginPath(); x.arc(o, o, LR - 26, 196 * DEG, 262 * DEG); x.stroke();
  x.strokeStyle = 'rgba(255,252,240,.14)'; x.lineWidth = 8; x.beginPath(); x.arc(o, o, LR - 30, 20 * DEG, 60 * DEG); x.stroke();
  x.restore();
  LENS_RIM = { c, o }; LENS_SH = { c: sh, o };
}
// ── camera and lens paths ──
function camAt(t) {
  const base = 1 + .015 * eSine(seg(t, 0, 3.45)), ia = eInOut(seg(t, ...T.cam)), oa = eInOut(seg(t, ...T.camOut));
  const s = lerp(lerp(base, 1.2, ia), 1, oa), cx = 960, cy = lerp(lerp(540, 610, ia), 540, oa);
  return { s, cx, cy };
}
const toScreen = (cam, [x, y]) => [(x - cam.cx) * cam.s + W / 2, (y - cam.cy) * cam.s + H / 2];
function lensAt(t, cam, hb) {
  const sc = toScreen(cam, [hb.C[0], lerp(hb.C[1], HB - 40, .45)]);
  const a = eInOut(seg(t, ...T.lens)), b = eInOut(seg(t, ...T.lensOut));
  const wob = [14 * Math.sin(t * 1.7), 9 * Math.sin(t * 1.3 + 1)];
  const tg = [sc[0] + wob[0] * seg(t, 4.2, 4.6), sc[1] + wob[1] * seg(t, 4.2, 4.6)];
  const p = [lerp(2320, tg[0], a), lerp(1390, tg[1], a)];
  return [lerp(p[0], 2420, b), lerp(p[1], 170, b)];
}
// ── half-plane helpers for the page turn ──
function clipPoly(poly, f) { const out = []; for (let i = 0; i < poly.length; i++) { const A = poly[i], Bp = poly[(i + 1) % poly.length], da = f(A), db = f(Bp);
  if (da >= 0) out.push(A); if ((da >= 0) !== (db >= 0)) { const u = da / (da - db); out.push([A[0] + (Bp[0] - A[0]) * u, A[1] + (Bp[1] - A[1]) * u]); } } return out; }
function pageTurn(c, t) {
  const u = eInOut(seg(t, ...T.turn)), ang = lerp(34, 8, u) * DEG, nx = Math.cos(ang), ny = Math.sin(ang);
  const Q = [lerp(W + 70, -760, u), lerp(H * .96, H * .38, u)], d = p => (p[0] - Q[0]) * nx + (p[1] - Q[1]) * ny;
  const rect = [[0, 0], [W, 0], [W, H], [0, H]];
  const flat = clipPoly(rect, p => -d(p)), lifted = clipPoly(rect, d);
  const refl = p => { const dd = d(p); return [p[0] - 2 * dd * nx, p[1] - 2 * dd * ny]; };
  const flap = lifted.map(refl);
  const P = pts => { const p = new Path2D(); pts.forEach(([x, y], i) => i ? p.lineTo(x, y) : p.moveTo(x, y)); p.closePath(); return p; };
  c.drawImage(PLATE15, 0, 0);
  if (lifted.length > 2) { // crease shadow falling on the new plate
    c.save(); c.clip(P(lifted)); const g = c.createLinearGradient(Q[0], Q[1], Q[0] + nx * 160, Q[1] + ny * 160);
    g.addColorStop(0, 'rgba(30,18,6,.42)'); g.addColorStop(1, 'rgba(30,18,6,0)'); c.fillStyle = g; c.fillRect(0, 0, W, H); c.restore(); }
  if (flat.length > 2) { c.save(); c.clip(P(flat)); c.drawImage(CACHE14, 0, 0); c.restore(); }
  if (flap.length > 2) {
    const fp = P(flap);
    c.save(); c.shadowColor = 'rgba(30,18,6,.45)'; c.shadowBlur = 36; c.shadowOffsetX = -10 * (1 - u) - 6; c.shadowOffsetY = 12; c.fillStyle = '#d9cba8'; c.fill(fp); c.restore();
    c.save(); c.clip(fp); const k = 2 * (Q[0] * nx + Q[1] * ny);
    c.setTransform(1 - 2 * nx * nx, -2 * nx * ny, -2 * nx * ny, 1 - 2 * ny * ny, k * nx, k * ny);
    c.drawImage(PAPER14, 0, 0); c.globalAlpha = .06; c.drawImage(CACHE14, 0, 0); c.globalAlpha = 1;
    c.setTransform(1, 0, 0, 1, 0, 0);
    const span = 900, g = c.createLinearGradient(Q[0], Q[1], Q[0] - nx * span, Q[1] - ny * span);
    g.addColorStop(0, 'rgba(60,40,16,.34)'); g.addColorStop(.12, 'rgba(255,248,230,.10)'); g.addColorStop(.4, 'rgba(255,248,230,.16)'); g.addColorStop(1, 'rgba(60,40,16,.2)');
    c.fillStyle = g; c.fillRect(0, 0, W, H); c.restore();
    c.strokeStyle = 'rgba(80,58,30,.35)'; c.lineWidth = 1; c.stroke(fp);
  }
}
// ── frame ──
function render(t) {
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  if (t < T.turn[0]) {
    const cam = camAt(t), M = [cam.s, 0, 0, cam.s, W / 2 - cam.cx * cam.s, H / 2 - cam.cy * cam.s];
    ctx.setTransform(...M); const hb = drawPlate14(ctx, t); ctx.setTransform(1, 0, 0, 1, 0, 0);
    if (t > T.lens[0] && t < T.lensOut[1]) {
      const [lx, ly] = lensAt(t, cam, hb);
      ctx.globalAlpha = .75; ctx.drawImage(LENS_SH.c, lx - LENS_SH.o + 26, ly - LENS_SH.o + 34); ctx.globalAlpha = 1;
      ctx.save(); ctx.beginPath(); ctx.arc(lx, ly, LR, 0, TAU); ctx.clip();
      const m = MAG; ctx.setTransform(M[0] * m, 0, 0, M[3] * m, lx + (M[4] - lx) * m, ly + (M[5] - ly) * m);
      drawPlate14(ctx, t); ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.fillStyle = 'rgba(255,246,222,.05)'; ctx.fillRect(lx - LR, ly - LR, 2 * LR, 2 * LR); ctx.restore();
      ctx.drawImage(LENS_RIM.c, lx - LENS_RIM.o, ly - LENS_RIM.o);
    }
  } else if (t < T.turn[1]) {
    if (!CACHE14) { CACHE14 = mk(W, H); drawPlate14(CACHE14.getContext('2d'), T.turn[0]); }
    pageTurn(ctx, t);
  } else {
    const s = 1 + .035 * eSine(seg(t, T.turn[1], 10)); ctx.setTransform(s, 0, 0, s, W / 2 - 960 * s, H / 2 - 540 * s); ctx.drawImage(PLATE15, 0, 0); TNOW = t; inkText(ctx, 'Fig. 7 was drawn from memory; the memory has since been revised.', W / 2, 946, `italic 30px ${GAR}`, 8.45, .9); ctx.setTransform(1, 0, 0, 1, 0, 0);
  }
  ctx.drawImage(VIG, 0, 0);
  const fade = Math.max(1 - eOut(seg(t, ...T.fadeIn)), eInOut(seg(t, ...T.fadeOut)));
  if (fade > 0) { ctx.fillStyle = `rgba(22,15,9,${fade})`; ctx.fillRect(0, 0, W, H); }
}
function buildVig() { const c = mk(W, H), x = c.getContext('2d'); const g = x.createRadialGradient(W / 2, H * .48, H * .45, W / 2, H / 2, H * 1.12);
  g.addColorStop(0, 'rgba(40,24,8,0)'); g.addColorStop(1, 'rgba(40,24,8,.3)'); x.fillStyle = g; x.fillRect(0, 0, W, H); return c; }

window.ready = (async () => {
  await Promise.all([`48px ${SC}`, `29px ${IT}`, `italic 29px ${IT}`, `italic 30px ${GAR}`, `30px ${GAR}`].map(f => document.fonts.load(f, 'PLATE XIV. Specimens of Imaginary Fungi, abc 0123456789')));
  await document.fonts.ready;
  GRANC = buildGran(); GRANPAT = ctx.createPattern(GRANC, 'repeat');
  PAPER14 = buildPaper(3); PAPER15 = buildPaper(8); PAPERPAT = ctx.createPattern(PAPER14, 'no-repeat');
  VIG = buildVig(); buildLens(); buildFigs(); PLATE15 = buildPlate15();
  render(0);
})();
window.draw = ({ t }) => { render(t); return cv.toDataURL('image/jpeg', 0.92).split(',')[1]; };
window.events = () => {
  const ev = [{ t: T.head, k: 'stamp' }, { t: 0, k: 'music' }];
  const all = [...FIGS, { ...HERO, n: 3 }];
  for (const F of all) { ev.push({ t: F.t0, k: 'engrave', d: F.t1 - F.t0 }); ev.push({ t: F.w0, k: 'wash', d: .85 }); ev.push({ t: F.lt, k: 'nib' }, { t: F.lt + .18, k: 'nib', v: .6 }); }
  for (const L of LEAD) ev.push({ t: L.t, k: 'nib', v: .7 }, { t: L.t + .1, k: 'scratch', d: .35 });
  ev.push({ t: 3.15, k: 'scratch', d: .6 });
  ev.push({ t: T.lens[0], k: 'slide', d: .85 }, { t: T.lens[1] - .02, k: 'tink' });
  for (let i = 0; i < NR; i++) ev.push({ t: T.unfold + i * .035 + .12, k: 'creak', v: .6 + (i % 3) * .2 });
  ev.push({ t: T.unfold - .3, k: 'unfold', d: 1.2 }, { t: T.puff, k: 'puff' });
  ev.push({ t: T.lensOut[0], k: 'slide', d: .75 });
  ev.push({ t: T.turn[0], k: 'lift' }, { t: T.turn[0] + .25, k: 'page', d: 1.0 }, { t: T.turn[1] - .08, k: 'settle' }, { t: T.turn[1] + .05, k: 'chord' }, { t: 8.45, k: 'scratch', d: .9 });
  return ev.sort((a, b) => a.t - b.t);
};
