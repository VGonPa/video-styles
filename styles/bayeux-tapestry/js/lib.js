// lib.js · helpers, wool palette, baked linen/wool textures, stitch primitives and a stitched capital alphabet
// Everything is deterministic (seeded) and depends only on t.
const TAU = Math.PI * 2;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eOut = u => 1 - Math.pow(1 - u, 3);
const eIn = u => u * u * u;
const eInOut = u => u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
const eSine = u => 0.5 - 0.5 * Math.cos(Math.PI * clamp(u));
const eBack = u => { const c = 1.7; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
function mulberry(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const hash = n => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
function mk(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }

// eight dyed wools, as on the old embroidered friezes
const COL = {
  linen: '#e2d5b8', linenD: '#d3c3a1',
  terra: '#a9563b', terraD: '#83402c', mustard: '#c8993f', mustardL: '#d9b565',
  sage: '#8a966b', green: '#5a6a44', greenD: '#3d4a31',
  blueL: '#8e9fa6', blue: '#566b7d', blueD: '#2c3548',
};
const SHC = new Map();
function shade(h, k) {
  const key = h + k; if (SHC.has(key)) return SHC.get(key);
  const n = parseInt(h.slice(1), 16), r = n >> 16, g = n >> 8 & 255, b = n & 255;
  const f = k > 0 ? c => c + (255 - c) * k : c => c * (1 + k);
  const s = `rgb(${f(r) | 0},${f(g) | 0},${f(b) | 0})`; SHC.set(key, s); return s;
}

// ── geometry ──
function ell(cx, cy, rx, ry, a0 = 0, a1 = TAU, n = 28) { const o = []; for (let i = 0; i <= n; i++) { const a = a0 + (a1 - a0) * i / n; o.push([cx + rx * Math.cos(a), cy + ry * Math.sin(a)]); } return o; }
function bez(p0, p1, p2, p3, n = 12) { const o = []; for (let i = 0; i <= n; i++) { const u = i / n, v = 1 - u; o.push([v * v * v * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u * u * u * p3[0], v * v * v * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u * u * u * p3[1]]); } return o; }
function cr(pts, closed = true, n = 6) {   // Catmull-Rom smoothing
  const o = [], m = pts.length, N = closed ? m : m - 1;
  const P = i => closed ? pts[(i + m) % m] : pts[clamp(i, 0, m - 1)];
  for (let i = 0; i < N; i++) {
    const p0 = P(i - 1), p1 = P(i), p2 = P(i + 1), p3 = P(i + 2);
    for (let k = 0; k < n; k++) { const u = k / n, u2 = u * u, u3 = u2 * u;
      o.push([0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * u + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * u2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * u3),
              0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * u + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * u2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * u3)]); }
  }
  if (!closed) o.push(pts[m - 1]);
  return o;
}
function thick(pts, ws) {   // polyline → outline polygon of varying width
  const L = [], R = [], n = pts.length;
  for (let i = 0; i < n; i++) {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)];
    let dx = b[0] - a[0], dy = b[1] - a[1]; const d = Math.hypot(dx, dy) || 1; dx /= d; dy /= d;
    const w = (typeof ws === 'function' ? ws(i / (n - 1)) : ws[i]) / 2;
    L.push([pts[i][0] - dy * w, pts[i][1] + dx * w]); R.push([pts[i][0] + dy * w, pts[i][1] - dx * w]);
  }
  return L.concat(R.reverse());
}
function pathOf(poly, closed = true) { const p = new Path2D(); poly.forEach((q, i) => i ? p.lineTo(q[0], q[1]) : p.moveTo(q[0], q[1])); if (closed) p.closePath(); return p; }
function bbox(poly) { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (const [x, y] of poly) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); } return [x0, y0, x1, y1]; }
const tr = (poly, dx, dy, s = 1, fx = 1) => poly.map(([x, y]) => [dx + x * s * fx, dy + y * s]);

// ── textures ──
let WOOL, LINEN_TILE;
function bakeWool() {   // one tile of laid wool strands (grey around 128, used with 'overlay')
  const S = 96, NR = 28, P = S / NR, c = mk(S, S), g = c.getContext('2d'), im = g.createImageData(S, S), d = im.data, r = mulberry(11);
  const ph = [], am = []; for (let k = 0; k < NR; k++) { ph.push(r() * TAU); am.push(0.4 + r()); }
  for (let y = 0; y < S; y++) {
    const k = Math.floor(y / P), s = y / P - k, ridge = Math.pow(Math.sin(Math.PI * s), 0.8);
    for (let x = 0; x < S; x++) {
      const tw = Math.sin(TAU * (x + s * P * 2.4) / 6 + ph[k]);
      const lf = Math.sin(TAU * x / S * 2 + ph[k]) * am[k];
      const v = clamp(128 + (ridge - 0.62) * 150 + tw * 16 * ridge + lf * 11 + (r() - 0.5) * 22, 0, 255);
      const i = (y * S + x) * 4; d[i] = d[i + 1] = d[i + 2] = v; d[i + 3] = 255;
    }
  }
  g.putImageData(im, 0, 0); WOOL = c;
}
function bakeLinenTile() {   // plain-weave linen, 256 px tile
  const S = 256, c = mk(S, S), g = c.getContext('2d'), r = mulberry(3);
  g.fillStyle = COL.linen; g.fillRect(0, 0, S, S);
  for (let i = 0; i < S; i += 2.56) {
    const a = 0.05 + r() * 0.08, w = 1 + r() * 0.8;
    g.fillStyle = `rgba(120,95,55,${a})`; g.fillRect(i, 0, w, S);
    g.fillStyle = `rgba(110,88,50,${a * 0.9})`; g.fillRect(0, i, S, w);
    g.fillStyle = `rgba(255,250,235,${0.05 + r() * 0.06})`; g.fillRect(i + 1.3, 0, 0.7, S); g.fillRect(0, i + 1.3, S, 0.7);
  }
  for (let i = 0; i < 90; i++) {   // slubs
    const x = r() * S, y = r() * S, hz = r() < 0.5, l = 8 + r() * 30;
    g.fillStyle = `rgba(${r() < 0.5 ? '130,100,60' : '250,244,225'},${0.12 + r() * 0.12})`;
    hz ? g.fillRect(x, y, l, 1.3) : g.fillRect(x, y, 1.3, l);
  }
  LINEN_TILE = c;
}

// ── stitches ──
// laid-and-couched fill: dense parallel strands (angle ang, degrees), held by couching bars with tiny tacks
function laid(c, poly, col, ang = 90, o = {}) {
  const P = pathOf(poly), bb = bbox(poly);
  c.save();
  if (o.shadow !== false) { c.shadowColor = 'rgba(50,32,14,0.42)'; c.shadowBlur = 4; c.shadowOffsetX = 1.6; c.shadowOffsetY = 2.2; }
  c.fillStyle = col; c.fill(P); c.shadowColor = 'transparent';
  c.clip(P);
  const pat = c.createPattern(WOOL, 'repeat');
  pat.setTransform(new DOMMatrix().rotateSelf(ang).translateSelf(hash(bb[0] * 0.13 + bb[1]) * 96, hash(bb[1] * 0.7) * 96));
  c.globalCompositeOperation = 'overlay'; c.fillStyle = pat; c.fillRect(bb[0] - 2, bb[1] - 2, bb[2] - bb[0] + 4, bb[3] - bb[1] + 4);
  c.globalCompositeOperation = 'source-over';
  if (o.bars !== false) {
    const gap = o.gap || 19, a = ang * Math.PI / 180, ca = Math.cos(a), sa = Math.sin(a);
    const cx = (bb[0] + bb[2]) / 2, cy = (bb[1] + bb[3]) / 2, R = Math.hypot(bb[2] - bb[0], bb[3] - bb[1]) / 2 + 4;
    const off = hash(bb[0] * 0.37 + bb[1] * 1.3) * gap, bars = new Path2D();
    for (let d = -R + off; d < R; d += gap) { const px = cx + ca * d, py = cy + sa * d; bars.moveTo(px + sa * R, py - ca * R); bars.lineTo(px - sa * R, py + ca * R); }
    c.lineCap = 'butt';
    c.strokeStyle = 'rgba(40,25,10,0.22)'; c.lineWidth = 4.4; c.stroke(bars);
    c.strokeStyle = shade(col, -0.14); c.lineWidth = 2.8; c.stroke(bars);
    c.strokeStyle = shade(col, 0.22); c.lineWidth = 0.9; c.stroke(bars);
    c.setLineDash([1.8, 6.5]); c.lineDashOffset = off; c.strokeStyle = shade(col, -0.42); c.lineWidth = 4.8; c.stroke(bars); c.setLineDash([]);
  }
  c.restore();
}
// linen-coloured area (faces, hands): the ground shows, only covers what is under it
function bare(c, poly) { c.save(); c.fillStyle = LINEN_PAT || COL.linen; c.fill(pathOf(poly)); c.restore(); }
let LINEN_PAT = null;

// stem stitch along a polyline; u = portion stitched (0..1); returns the needle head [x, y, angle]
function stem(c, pts, col, w = 4.4, u = 1, L = 9) {
  const n = pts.length; if (n < 2 || u <= 0) return null;
  const cum = [0]; for (let i = 1; i < n; i++) cum.push(cum[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  const tot = cum[n - 1] * clamp(u); if (tot <= 0.5) return null;
  let j = 0;
  const at = s => { while (j < n - 2 && cum[j + 1] < s) j++; while (j > 0 && cum[j] > s) j--;
    const l = cum[j + 1] - cum[j] || 1, f = (s - cum[j]) / l, a = pts[j], b = pts[j + 1], tx = (b[0] - a[0]) / l, ty = (b[1] - a[1]) / l;
    return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, tx, ty]; };
  const base = new Path2D(), hi = new Path2D(), o = w * 0.3, step = L * 0.6;
  for (let s = 0; s < tot; s += step) {
    const e = Math.min(s + L, tot), A = at(s), B = at(e), h = at(s + (e - s) * 0.3), g = at(s + (e - s) * 0.78);
    const nx = -A[3], ny = A[2];
    base.moveTo(A[0] + nx * o, A[1] + ny * o); base.lineTo(B[0] - nx * o, B[1] - ny * o);
    hi.moveTo(h[0] + nx * o * 0.2 - 0.5, h[1] + ny * o * 0.2 - 0.6); hi.lineTo(g[0] - nx * o * 0.9 - 0.5, g[1] - ny * o * 0.9 - 0.6);
  }
  c.save(); c.lineCap = 'round';
  c.translate(1.1, 1.5); c.strokeStyle = 'rgba(45,28,12,0.3)'; c.lineWidth = w + 0.6; c.stroke(base); c.translate(-1.1, -1.5);
  c.strokeStyle = shade(col, -0.3); c.lineWidth = w; c.stroke(base);
  c.strokeStyle = col; c.lineWidth = w * 0.6; c.stroke(base);
  c.strokeStyle = shade(col, 0.32); c.lineWidth = w * 0.24; c.stroke(hi);
  c.restore();
  const H = at(tot); return [H[0], H[1], Math.atan2(H[3], H[2])];
}
const outline = (c, poly, col = COL.blueD, w = 4) => stem(c, poly.concat([poly[0], poly[1]]), col, w);
// a filled, outlined piece in one call
function piece(c, poly, col, ang = 90, ol = COL.blueD, w = 4, o) { laid(c, poly, col, ang, o); outline(c, poly, ol, w); }
function bareP(c, poly, ol = COL.blueD, w = 3.6) { bare(c, poly); outline(c, poly, ol, w); }
function knot(c, x, y, col, r = 3) { c.save(); c.fillStyle = 'rgba(45,28,12,0.3)'; c.beginPath(); c.arc(x + 1, y + 1.4, r + 0.5, 0, TAU); c.fill();
  c.fillStyle = shade(col, -0.2); c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill(); c.fillStyle = shade(col, 0.3); c.beginPath(); c.arc(x - r * 0.3, y - r * 0.35, r * 0.4, 0, TAU); c.fill(); c.restore(); }

// ── stitched capitals (single-stroke letters on a 6-unit-tall grid) ──
function A_(cx, cy, rx, ry, a0, a1, n = 10) { const o = []; for (let i = 0; i <= n; i++) { const a = (a0 + (a1 - a0) * i / n) * Math.PI / 180; o.push([cx + rx * Math.cos(a), cy + ry * Math.sin(a)]); } return o; }
const GLY = {
  A: [[[0, 6], [2, 0], [4, 6]], [[0.8, 4], [3.2, 4]]],
  B: [[[0, 6], [0, 0], [2.3, 0], ...A_(2.3, 1.45, 1.35, 1.45, -90, 90).slice(1), [0, 2.9]], [[0, 2.9], [2.5, 2.9], ...A_(2.5, 4.45, 1.5, 1.55, -90, 90).slice(1), [0, 6]]],
  C: [A_(2.4, 3, 2.3, 3, -40, -320, 16)],
  D: [[[0, 0], [0, 6], [1.4, 6], ...A_(1.4, 3, 2.4, 3, 90, -90, 14).slice(1), [0, 0]]],
  E: [[[3.3, 0], [0, 0], [0, 6], [3.3, 6]], [[0, 2.9], [2.5, 2.9]]],
  F: [[[3.3, 0], [0, 0], [0, 6]], [[0, 2.9], [2.5, 2.9]]],
  G: [A_(2.4, 3, 2.3, 3, -40, -360, 16), [[4.7, 3.1], [2.9, 3.1]]],
  H: [[[0, 0], [0, 6]], [[3.5, 0], [3.5, 6]], [[0, 3], [3.5, 3]]],
  I: [[[0, 0], [0, 6]]],
  J: [[[2.4, 0], [2.4, 4.5], ...A_(1.2, 4.5, 1.2, 1.5, 0, 160, 8).slice(1)]],
  K: [[[0, 0], [0, 6]], [[3.3, 0], [0, 3.6]], [[1.1, 2.6], [3.5, 6]]],
  L: [[[0, 0], [0, 6], [3.1, 6]]],
  M: [[[0, 6], [0.3, 0], [2.25, 4.3], [4.2, 0], [4.5, 6]]],
  N: [[[0, 6], [0, 0], [3.6, 6], [3.6, 0]]],
  O: [A_(2.4, 3, 2.4, 3, -90, 270, 20)],
  P: [[[0, 6], [0, 0], [2.3, 0], ...A_(2.3, 1.6, 1.4, 1.6, -90, 90).slice(1), [0, 3.2]]],
  Q: [A_(2.4, 3, 2.4, 3, -90, 270, 20), [[2.8, 4.6], [4.6, 6.6]]],
  R: [[[0, 6], [0, 0], [2.3, 0], ...A_(2.3, 1.6, 1.4, 1.6, -90, 90).slice(1), [0, 3.2]], [[1.7, 3.2], [3.6, 6]]],
  S: [[...A_(2.0, 1.5, 1.8, 1.5, -25, -270, 10), ...A_(2.0, 4.5, 2.0, 1.5, -90, 155, 12).slice(1)]],
  T: [[[0, 0], [4, 0]], [[2, 0], [2, 6]]],
  U: [[[0, 0], [0, 4.2], ...A_(1.8, 4.2, 1.8, 1.8, 180, 0, 10).slice(1), [3.6, 0]]],
  V: [[[0, 0], [2, 6], [4, 0]]],
  W: [[[0, 0], [1.2, 6], [2.4, 1.5], [3.6, 6], [4.8, 0]]],
  X: [[[0, 0], [3.8, 6]], [[3.8, 0], [0, 6]]],
  Y: [[[0, 0], [2, 3], [4, 0]], [[2, 3], [2, 6]]],
  Z: [[[0, 0], [3.6, 0], [0, 6], [3.6, 6]]],
  ',': [[[0.5, 5.3], [0, 7]]],
  '.': [[[0.1, 5.6], [0.5, 6]]],
};
// lay out a caption: strokes in world coords, word colours alternating like the old frieze inscriptions
function caption(text, x, y, u, cols, seed = 1) {
  const r = mulberry(seed), out = []; let cx = x, word = 0;
  for (const ch of text) {
    if (ch === ' ') { cx += 2.5 * u; word++; continue; }
    const g = GLY[ch]; if (!g) continue;
    let w = 0; g.forEach(s => s.forEach(p => w = Math.max(w, p[0])));
    const sl = (r() - 0.5) * 0.05, dy = (r() - 0.5) * 0.5 * u, col = cols[word % cols.length];
    for (const s of g) {
      const pts = s.map(([px, py]) => [cx + (px + (6 - py) * sl) * u + (r() - 0.5) * 0.18 * u, y + dy + py * u + (r() - 0.5) * 0.18 * u]);
      let len = 0; for (let i = 1; i < pts.length; i++) len += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
      out.push({ pts, col, len: Math.max(len, 3) });
    }
    cx += (w + 1.5) * u;
  }
  out.total = out.reduce((a, s) => a + s.len, 0); out.x0 = x; out.x1 = cx;
  return out;
}
// draw a caption stitched up to p (0..1); returns the needle head and the thread colour
function drawCaption(c, cap, p, w = 5.2) {
  if (p <= 0) return null;
  let rem = cap.total * clamp(p), head = null;
  for (const s of cap.strokes || cap) {
    if (rem <= 0) break;
    const u = Math.min(1, rem / s.len); const h = stem(c, s.pts, s.col, w, u, 8); rem -= s.len;
    if (h) head = { x: h[0], y: h[1], a: h[2], col: s.col };
  }
  return head;
}
