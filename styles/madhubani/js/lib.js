// lib.js · helpers, pigments, paper, polyline tools and the stroke-by-stroke op renderer (deterministic, seeded)
const TAU = Math.PI * 2;
const W = 1920, H = 1080;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eOut = u => 1 - Math.pow(1 - u, 3);
const eIn = u => u * u * u;
const eInOut = u => u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
const eSine = u => 0.5 - 0.5 * Math.cos(Math.PI * u);
const eBack = u => { const c = 2.0; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
function mulberry(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function mk(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }

// Mithila pigments: turmeric, indigo, vermilion, leaf green, marigold, pink, lamp-black on handmade paper
const C = {
  paper: '#f3e3be', paperD: '#e2cc9e', ink: '#1c130e',
  yel: '#eeb21e', yelL: '#f7d774', org: '#ec7a1f',
  ind: '#26358a', indL: '#5d73c2', water: '#bccbe8',
  ver: '#d8371d', verD: '#a3230e', pink: '#e2477d', pinkL: '#f4a7c3',
  grn: '#3b8a3a', grnD: '#236126', grnL: '#8fc24f',
  brown: '#8a3f1b', white: '#fbf4e2',
};
const FT = 'Yatra One';

// ── polylines ──
function bez(p0, p1, p2, p3, n = 24) {
  const o = [];
  for (let i = 0; i <= n; i++) { const u = i / n, v = 1 - u;
    o.push([v * v * v * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u * u * u * p3[0], v * v * v * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u * u * u * p3[1]]); }
  return o;
}
function ell(cx, cy, rx, ry, n = 48, a0 = 0, a1 = TAU) { const o = []; for (let i = 0; i <= n; i++) { const a = lerp(a0, a1, i / n); o.push([cx + Math.cos(a) * rx, cy + Math.sin(a) * ry]); } return o; }
function plen(p) { let L = 0; for (let i = 1; i < p.length; i++) L += Math.hypot(p[i][0] - p[i - 1][0], p[i][1] - p[i - 1][1]); return L; }
function toPath(p, closed) { const q = new Path2D(); q.moveTo(p[0][0], p[0][1]); for (let i = 1; i < p.length; i++) q.lineTo(p[i][0], p[i][1]); if (closed) q.closePath(); return q; }
function bbox(p) { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (const [x, y] of p) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); } return { x0, y0, x1, y1 }; }
function resample(p, step) {   // evenly spaced points (for a hand wobble that doesn't depend on vertex density)
  const o = [p[0]]; let acc = 0;
  for (let i = 1; i < p.length; i++) {
    const [ax, ay] = p[i - 1], [bx, by] = p[i], l = Math.hypot(bx - ax, by - ay); let d = step - acc;
    while (d <= l) { o.push([ax + (bx - ax) * d / l, ay + (by - ay) * d / l]); d += step; }
    acc = l - (d - step);
  }
  o.push(p[p.length - 1]); return o;
}
// static hand wobble along the normal (low frequency, seeded, never boils)
function wob(p, amp, seed, step = 6) {
  const q = resample(p, step), r = mulberry(seed), f1 = 0.02 + r() * 0.02, f2 = 0.07 + r() * 0.05, ph1 = r() * TAU, ph2 = r() * TAU;
  let s = 0;
  return q.map((pt, i) => {
    const a = q[Math.max(0, i - 1)], b = q[Math.min(q.length - 1, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1;
    if (i) s += Math.hypot(pt[0] - q[i - 1][0], pt[1] - q[i - 1][1]);
    const o = amp * (0.7 * Math.sin(s * f1 + ph1) + 0.3 * Math.sin(s * f2 + ph2));
    return [pt[0] - dy / l * o, pt[1] + dx / l * o];
  });
}
const mapP = (p, M) => M ? p.map(M) : p;

// ── ops: every motif is a list of timed strokes; u = local progress 0…1 ──
// line   {k:'line', p, w, c, closed}           — traced with a travelling pen
// dbl    {k:'dbl', p, w, gap, gc, closed}      — the Madhubani double outline (ink / colour / ink)
// fill   {k:'fill', p, c, a, sp}               — brushed in, parallel strokes one after another (bharni)
// hatch  {k:'hatch', p, c, a, sp, lw}          — fine parallel line fill (kachni), line by line
// scales {k:'scales', p, r, c, lw, dir}        — fish-scale arcs, column by column
// dots   {k:'dots', d:[[x,y,r]], c}            — dots dabbed one by one
// pop    {k:'pop', p, c, o:[x,y], edge}        — small solid shape that springs in
function strokeDash(g, path, L, u) { if (u < 1) g.setLineDash([L * u + 0.01, L * 2 + 10]); g.stroke(path); if (u < 1) g.setLineDash([]); }
function linesIn(b, a, sp) {   // parallel segments covering box b at angle a
  const cx = (b.x0 + b.x1) / 2, cy = (b.y0 + b.y1) / 2, R = Math.hypot(b.x1 - b.x0, b.y1 - b.y0) / 2 + 4;
  const dx = Math.cos(a), dy = Math.sin(a), nx = -dy, ny = dx, o = [];
  for (let s = -R + sp / 2; s <= R; s += sp) o.push([[cx + nx * s - dx * R, cy + ny * s - dy * R], [cx + nx * s + dx * R, cy + ny * s + dy * R]]);
  return o;
}
function prepOp(o) {
  if (o.p) { o.L = plen(o.p) * 1.08; o.b = bbox(o.p); }
  if (o.k === 'fill') o.ln = linesIn(o.b, o.a ?? 0.6, o.sp ?? 9);
  if (o.k === 'hatch') o.ln = linesIn(o.b, o.a ?? 0.8, o.sp ?? 7);
  if (o.k === 'scales') {   // arcs bulge toward the tail; columns ordered head → tail
    const b = o.b, r = o.r, dir = o.dir ?? 1, a0 = dir > 0 ? Math.PI / 2 : -Math.PI / 2; o.arcs = [];
    let col = 0;
    for (let x = dir > 0 ? b.x1 + r : b.x0 - r; dir > 0 ? x > b.x0 - r : x < b.x1 + r; x -= dir * r * 1.15, col++)
      for (let y = b.y0 - r + (col % 2) * r; y < b.y1 + r; y += 2 * r) o.arcs.push(ell(x, y, r, r, 10, a0, a0 + Math.PI));
  }
  if (o.k === 'dots') o.n = o.d.length;
  if (o.k === 'pop') o.o = o.o || [(o.b.x0 + o.b.x1) / 2, (o.b.y0 + o.b.y1) / 2];
  return o;
}
function drawOp(g, o, u, M) {
  g.lineCap = 'round'; g.lineJoin = 'round';
  switch (o.k) {
    case 'line': { const P = toPath(mapP(o.p, M), o.closed && u >= 1); g.strokeStyle = o.c || C.ink; g.lineWidth = o.w; strokeDash(g, P, o.L, u); break; }
    case 'dbl': { const P = toPath(mapP(o.p, M), o.closed && u >= 1); g.strokeStyle = C.ink; g.lineWidth = o.w; strokeDash(g, P, o.L, u);
      g.strokeStyle = o.gc; g.lineWidth = o.gap; strokeDash(g, P, o.L, clamp(u * 1.04 - 0.04)); break; }
    case 'fill': { const P = toPath(mapP(o.p, M), true);
      if (u >= 1) { g.fillStyle = o.c; g.fill(P); break; }
      g.save(); g.clip(P); g.strokeStyle = o.c; g.lineWidth = (o.sp ?? 9) * 1.9; const n = o.ln.length;
      for (let i = 0; i < n; i++) { const v = clamp((u * (n + 2) - i) / 2); if (v <= 0) break; const s = mapP(o.ln[i], M), L = Math.hypot(s[1][0] - s[0][0], s[1][1] - s[0][1]);
        const q = new Path2D(); q.moveTo(...s[0]); q.lineTo(...s[1]); strokeDash(g, q, L, v); }
      g.restore(); break; }
    case 'hatch': { const P = toPath(mapP(o.p, M), true); g.save(); g.clip(P); g.strokeStyle = o.c || C.ink; g.lineWidth = o.lw ?? 1.6; const n = o.ln.length;
      for (let i = 0; i < n; i++) { const v = clamp(u * (n + 1) - i); if (v <= 0) break; const s = mapP(o.ln[i], M), L = Math.hypot(s[1][0] - s[0][0], s[1][1] - s[0][1]);
        const q = new Path2D(); q.moveTo(...s[0]); q.lineTo(...s[1]); strokeDash(g, q, L, eOut(v)); }
      g.restore(); break; }
    case 'scales': { const P = toPath(mapP(o.p, M), true); g.save(); g.clip(P); g.strokeStyle = o.c || C.ink; g.lineWidth = o.lw ?? 1.8; const n = o.arcs.length, m = Math.floor(u * n);
      const q = new Path2D(); for (let i = 0; i < m; i++) { const a = mapP(o.arcs[i], M); q.moveTo(...a[0]); for (let j = 1; j < a.length; j++) q.lineTo(...a[j]); }
      g.stroke(q); g.restore(); break; }
    case 'dots': { g.fillStyle = o.c || C.ink; const n = o.n, f = u * n;
      for (let i = 0; i < n && i < f; i++) { const s = eBack(clamp(f - i)); const [x, y, r] = M ? [...M(o.d[i]), o.d[i][2]] : o.d[i]; g.beginPath(); g.arc(x, y, Math.max(0.01, r * s), 0, TAU); g.fill(); }
      break; }
    case 'pop': { const s = eBack(u); if (s <= 0.001) break; g.save(); const [ox, oy] = M ? M(o.o) : o.o; g.translate(ox, oy); g.scale(s, s); g.translate(-ox, -oy);
      const P = toPath(mapP(o.p, M), true); g.fillStyle = o.c; g.fill(P); if (o.edge) { g.strokeStyle = C.ink; g.lineWidth = o.edge; g.stroke(P); } g.restore(); break; }
  }
}
// motif = ops placed on a local time axis [0…dur]; drawn at local time lt
function drawMotif(g, ops, lt, M) { for (const o of ops) { const u = seg(lt, o.t0, o.t1); if (u > 0) drawOp(g, o, u, M); } }
function prep(ops) { ops.forEach(prepOp); return ops; }

// ── handmade paper: warm, blotchy, fibrous; grain is baked once ──
let PAPER, GRAIN;
function bakePaper() {
  PAPER = mk(W, H); const g = PAPER.getContext('2d'), r = mulberry(105);
  g.fillStyle = C.paper; g.fillRect(0, 0, W, H);
  for (let i = 0; i < 90; i++) {
    const x = r() * W, y = r() * H, rad = 60 + r() * 280, dark = r() < 0.3, gr = g.createRadialGradient(x, y, 0, x, y, rad);
    gr.addColorStop(0, dark ? `rgba(214,168,98,${0.02 + r() * 0.04})` : `rgba(255,248,226,${0.03 + r() * 0.05})`); gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gr; g.fillRect(x - rad, y - rad, rad * 2, rad * 2);
  }
  for (let i = 0; i < 2600; i++) { g.strokeStyle = `rgba(140,100,50,${0.03 + r() * 0.06})`; g.lineWidth = 0.6 + r() * 0.6; const x = r() * W, y = r() * H, a = r() * TAU, l = 3 + r() * 14;
    g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + Math.cos(a + 0.5) * l * 0.5, y + Math.sin(a + 0.5) * l * 0.5, x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke(); }
  for (let i = 0; i < 260; i++) { g.fillStyle = `rgba(120,80,40,${0.06 + r() * 0.1})`; g.beginPath(); g.arc(r() * W, r() * H, 0.6 + r() * 1.4, 0, TAU); g.fill(); }
  GRAIN = mk(W, H); const q = GRAIN.getContext('2d'), rr = mulberry(7), id = q.createImageData(W, H), d = id.data;
  for (let i = 0; i < d.length; i += 4) { const v = 240 + rr() * 15; d[i] = v; d[i + 1] = v - 2; d[i + 2] = v - 6; d[i + 3] = 255; }
  q.putImageData(id, 0, 0);
  // soft vignette baked into grain so it survives the camera move
  const vg = q.createRadialGradient(W / 2, H / 2, 520, W / 2, H / 2, 1180); vg.addColorStop(0, 'rgba(255,255,255,0)'); vg.addColorStop(1, 'rgba(170,110,50,0.26)');
  q.fillStyle = vg; q.fillRect(0, 0, W, H);
}
