// picture-book · helpers: math, seeded RNG, tileable noise, gouache + colored-pencil painting, paper textures.
const W = 1920, H = 1080, TAU = Math.PI * 2;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eInOut = u => u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
const eSine = u => 0.5 - 0.5 * Math.cos(Math.PI * clamp(u));
const eOut = u => 1 - Math.pow(1 - clamp(u), 3);
const eIn = u => clamp(u) ** 3;
const eBack = (u, s = 1.9) => { u = clamp(u) - 1; return 1 + (s + 1) * u * u * u + s * u * u; };
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const mk = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };

// ── colour helpers ──
function hex(c) { const n = parseInt(c.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
function shade(c, k, warm = 0) { const [r, g, b] = hex(c); const f = v => Math.round(clamp(v * k, 0, 255));
  return `rgb(${f(r + warm)},${f(g)},${f(b - warm)})`; }
function rgba(c, a) { const [r, g, b] = hex(c); return `rgba(${r},${g},${b},${a})`; }

// ── tileable value noise / fBm on a size×size torus ──
function tileNoise(size, cells, seed) {
  const r = rng(seed), g = new Float32Array(cells * cells); for (let i = 0; i < g.length; i++) g[i] = r();
  const out = new Float32Array(size * size), sm = u => u * u * (3 - 2 * u);
  for (let y = 0; y < size; y++) { const fy = y / size * cells, iy = Math.floor(fy), ty = sm(fy - iy), y0 = iy % cells, y1 = (iy + 1) % cells;
    for (let x = 0; x < size; x++) { const fx = x / size * cells, ix = Math.floor(fx), tx = sm(fx - ix), x0 = ix % cells, x1 = (ix + 1) % cells;
      const a = g[y0 * cells + x0], b = g[y0 * cells + x1], c = g[y1 * cells + x0], d = g[y1 * cells + x1];
      out[y * size + x] = (a + (b - a) * tx) + ((c + (d - c) * tx) - (a + (b - a) * tx)) * ty; } }
  return out;
}
function fbm(size, seed, base, oct) {
  const acc = new Float32Array(size * size); let amp = 1, tot = 0;
  for (let o = 0; o < oct; o++) { const n = tileNoise(size, base << o, seed + o * 17); for (let i = 0; i < acc.length; i++) acc[i] += n[i] * amp; tot += amp; amp *= 0.5; }
  for (let i = 0; i < acc.length; i++) acc[i] /= tot; return acc;
}
function alphaCanvas(size, f, rgb) {           // canvas of one colour whose alpha = f(i) (0..1)
  const c = mk(size, size), x = c.getContext('2d'), im = x.createImageData(size, size), d = im.data;
  for (let i = 0; i < size * size; i++) { d[i * 4] = rgb[0]; d[i * 4 + 1] = rgb[1]; d[i * 4 + 2] = rgb[2]; d[i * 4 + 3] = clamp(f(i)) * 255; }
  x.putImageData(im, 0, 0); return c;
}

// ── textures (built once in initTextures) ──
const TX = {};
function initTextures() {
  const S = 512;
  const a = fbm(S, 11, 4, 5), b = fbm(S, 29, 32, 3);
  const n = a.map((v, i) => 0.62 * v + 0.38 * b[i]);
  const k = 2.6;
  TX.dark = alphaCanvas(S, i => (n[i] - 0.5) * k, [70, 38, 20]);      // pigment pooling blotches
  TX.light = alphaCanvas(S, i => (0.5 - n[i]) * k, [255, 247, 228]);  // thin, chalky passages
  // granulation: fine pigment specks settling in the paper tooth
  const r = rng(7);
  TX.gran = alphaCanvas(S, i => { const v = r(); return v > 0.83 ? (v - 0.83) * 3.2 * (0.4 + b[i]) : 0; }, [60, 34, 22]);
  // dry-brush streaks (light) - horizontal-ish strokes
  const st = mk(S, S), sx = st.getContext('2d'), r2 = rng(3);
  for (let i = 0; i < 260; i++) { const y = r2() * S, x = r2() * S, L = 40 + r2() * 160, ang = (r2() - 0.5) * 0.35;
    sx.strokeStyle = `rgba(255,248,230,${0.04 + r2() * 0.10})`; sx.lineWidth = 1 + r2() * 4; sx.lineCap = 'round';
    for (const dx of [0, -S, S]) for (const dy of [0, -S, S]) { sx.beginPath(); sx.moveTo(x + dx, y + dy); sx.lineTo(x + dx + Math.cos(ang) * L, y + dy + Math.sin(ang) * L); sx.stroke(); } }
  TX.streak = st;
  // colored-pencil grain for strokes
  const r3 = rng(5), p = fbm(256, 41, 64, 2);
  TX.pencil = alphaCanvas(256, i => { const v = r3(); return (v < 0.22 ? 0 : 0.35 + v * 0.65) * (0.55 + p[i] * 0.8); }, [58, 36, 26]);
  TX.pencilLight = alphaCanvas(256, i => { const v = r3(); return (v < 0.3 ? 0 : 0.3 + v * 0.7); }, [255, 244, 222]);
  const cx = mk(1, 1).getContext('2d');
  TX.P = {}; for (const key of ['dark', 'light', 'gran', 'streak', 'pencil', 'pencilLight']) TX.P[key] = cx.createPattern(TX[key], 'repeat');
}
// pattern at an offset (texture sticks to the object's local frame, varied per seed)
function pat(key, seed, sc = 1) { const p = TX.P[key]; const r = rng(seed * 31 + 7);
  p.setTransform(new DOMMatrix().translate(r() * 512, r() * 512).scale(sc)); return p; }

// ── shapes ──
// closed Catmull-Rom spline through pts → Path2D
function blob(pts, tension = 1) {
  const p = new Path2D(), n = pts.length;
  p.moveTo(pts[0][0], pts[0][1]);
  for (let i = 0; i < n; i++) { const p0 = pts[(i - 1 + n) % n], p1 = pts[i], p2 = pts[(i + 1) % n], p3 = pts[(i + 2) % n];
    p.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6 * tension, p1[1] + (p2[1] - p0[1]) / 6 * tension, p2[0] - (p3[0] - p1[0]) / 6 * tension, p2[1] - (p3[1] - p1[1]) / 6 * tension, p2[0], p2[1]); }
  p.closePath(); return p;
}
function openSpline(pts) {        // open Catmull-Rom as Path2D
  const p = new Path2D(), n = pts.length; p.moveTo(pts[0][0], pts[0][1]);
  for (let i = 0; i < n - 1; i++) { const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(n - 1, i + 2)];
    p.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]); }
  return p;
}
function ell(x, y, rx, ry, rot = 0) { const p = new Path2D(); p.ellipse(x, y, rx, ry, rot, 0, TAU); return p; }
function poly(pts) { const p = new Path2D(); p.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) p.lineTo(pts[i][0], pts[i][1]); p.closePath(); return p; }
// wobbly organic circle-ish blob
function wob(cx, cy, rx, ry, seed, amt = 0.08, n = 10) { const r = rng(seed), pts = [];
  for (let i = 0; i < n; i++) { const a = i / n * TAU + r() * 0.2; const k = 1 + (r() - 0.5) * 2 * amt; pts.push([cx + Math.cos(a) * rx * k, cy + Math.sin(a) * ry * k]); }
  return blob(pts); }
// polyline with per-sample half-width → closed outline (for tails, legs, stems)
function ribbon(center, widths) {
  const L = [], R = [], n = center.length;
  for (let i = 0; i < n; i++) { const a = center[Math.max(0, i - 1)], b = center[Math.min(n - 1, i + 1)];
    let dx = b[0] - a[0], dy = b[1] - a[1]; const m = Math.hypot(dx, dy) || 1; dx /= m; dy /= m;
    L.push([center[i][0] - dy * widths[i], center[i][1] + dx * widths[i]]); R.push([center[i][0] + dy * widths[i], center[i][1] - dx * widths[i]]); }
  return L.concat(R.reverse());
}
function sampleSpline(pts, m) {   // sample open Catmull-Rom into m points
  const n = pts.length, out = [];
  for (let j = 0; j < m; j++) { const u = j / (m - 1) * (n - 1), i = Math.min(n - 2, Math.floor(u)), t = u - i;
    const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(n - 1, i + 2)];
    const f = k => 0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t * t + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t * t * t);
    out.push([f(0), f(1)]); }
  return out;
}

// ── gouache fill: flat body colour, pooled darker edge, mottling, granulation, dry-brush light ──
function paint(g, path, color, seed, o = {}) {
  g.save();
  g.fillStyle = color; g.fill(path);
  g.clip(path);
  const big = 6000;
  g.globalAlpha = o.mottle ?? 0.42; g.fillStyle = pat('dark', seed, o.tsc ?? 1); g.fillRect(-big, -big, 2 * big, 2 * big);
  g.globalAlpha = o.lightA ?? 0.38; g.fillStyle = pat('light', seed + 3, o.tsc ?? 1); g.fillRect(-big, -big, 2 * big, 2 * big);
  g.globalAlpha = o.gran ?? 0.5; g.fillStyle = pat('gran', seed + 5); g.fillRect(-big, -big, 2 * big, 2 * big);
  g.globalAlpha = o.streak ?? 0.6; g.fillStyle = pat('streak', seed + 9, o.ssc ?? 1); g.fillRect(-big, -big, 2 * big, 2 * big);
  if (o.edge !== 0) { g.globalAlpha = o.edgeA ?? 0.32; g.strokeStyle = shade(color, 0.62); g.lineWidth = o.edge ?? 9; g.stroke(path); }
  g.restore();
}
// colored-pencil outline: two grainy passes, slightly offset, never perfectly closed
function pencil(g, path, o = {}) {
  g.save(); g.lineJoin = 'round'; g.lineCap = 'round';
  g.strokeStyle = o.light ? pat('pencilLight', o.seed ?? 1) : pat('pencil', o.seed ?? 1);
  const w = o.w ?? 3;
  g.globalAlpha = o.a ?? 0.85; g.lineWidth = w; g.stroke(path);
  g.globalAlpha = (o.a ?? 0.85) * 0.55; g.translate(o.dx ?? 1.2, o.dy ?? -0.9); g.lineWidth = w * 0.7; g.stroke(path);
  g.restore();
}
// colored-pencil hatching inside a path (shading), direction ang
function hatch(g, path, seed, o = {}) {
  const r = rng(seed); g.save(); g.clip(path); g.lineCap = 'round';
  g.strokeStyle = o.light ? pat('pencilLight', seed) : pat('pencil', seed);
  g.globalAlpha = o.a ?? 0.35; g.lineWidth = o.w ?? 2;
  const [x0, y0, x1, y1] = o.box, sp = o.sp ?? 9, ang = o.ang ?? -0.9, L = o.len ?? 26;
  for (let y = y0; y < y1; y += sp) for (let x = x0; x < x1; x += sp * 1.4) {
    const jx = x + (r() - 0.5) * sp, jy = y + (r() - 0.5) * sp, l = L * (0.6 + r() * 0.6);
    g.beginPath(); g.moveTo(jx, jy); g.lineTo(jx + Math.cos(ang) * l, jy + Math.sin(ang) * l); g.stroke(); }
  g.restore();
}
