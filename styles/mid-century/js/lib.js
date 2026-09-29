// lib.js · helpers, palette, baked dry-brush / crayon / paper textures — all deterministic
const TAU = Math.PI * 2;
const W = 1920, H = 1080, DUR = 10;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eOut = u => 1 - Math.pow(1 - u, 3);
const eIn = u => u * u * u;
const eInOut = u => u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
// back-out: overshoot then settle
const eBack = (u, s = 2.2) => { u = clamp(u); const c = s + 1; return 1 + c * Math.pow(u - 1, 3) + s * Math.pow(u - 1, 2); };
// damped spring 0 → 1 with a bounce
const spring = (u, f = 2.2, z = 5) => u <= 0 ? 0 : u >= 3 ? 1 : 1 - Math.exp(-z * u) * Math.cos(f * TAU * u * 0.5);
// limited animation: hold each drawing for n frames of 30 fps ("on twos", "on threes")
const onN = (t, n = 2) => Math.floor(t * 30 / n) * n / 30;
function mulberry(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const hash = n => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
function mk(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }

// 1950s palette: mustard, teal, burnt orange, olive, cream, charcoal
const C = {
  cream: '#efe3c4', paper: '#f3e9cf', mustard: '#d9a42b', teal: '#2f8f8a', tealD: '#1f625f', orange: '#d0602a',
  olive: '#7d7c35', oliveL: '#a9a45a', ink: '#2a2622', skin: '#eeb98f', rose: '#c94a3a', sky: '#e6d7ad', grey: '#9c9582', white: '#f7f0dc',
};
const FT = 'Bowlby One SC', FS = 'Yellowtail', FC = 'Josefin Sans';

// ---- baked textures ----
const TEX = {}; // colour → CanvasPattern with dry-brush streaks
let PAPER, CRAYON;
function hexRgb(h) { const n = parseInt(h.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
function mix(a, b, u) { const A = hexRgb(a), B = hexRgb(b); return `rgb(${A.map((v, i) => Math.round(lerp(v, B[i], u))).join(',')})`; }
function bakeBrush(col, seed, STR = 1) {
  const S = 768, c = mk(S, S), g = c.getContext('2d'), r = mulberry(seed);
  g.fillStyle = col; g.fillRect(0, 0, S, S);
  // big soft mottling first (uneven paint load)
  for (let i = 0; i < 40; i++) {
    const x = r() * S, y = r() * S, rad = 60 + r() * 160, lt = r() < 0.5;
    const gr = g.createRadialGradient(x, y, 0, x, y, rad);
    gr.addColorStop(0, lt ? 'rgba(255,248,225,0.07)' : 'rgba(40,25,10,0.05)'); gr.addColorStop(1, 'rgba(0,0,0,0)');
    for (const ox of [-S, 0, S]) for (const oy of [-S, 0, S]) { g.save(); g.translate(ox, oy); g.fillStyle = gr; g.fillRect(x - rad, y - rad, rad * 2, rad * 2); g.restore(); }
  }
  // dry-brush strokes: bundles of broken parallel bristle lines on a slight diagonal
  for (let i = 0; i < 170; i++) {
    const x0 = r() * S, y0 = r() * S, len = 120 + r() * 420, ang = -0.16 + (r() - 0.5) * 0.12, n = 5 + (r() * 12 | 0), wd = 14 + r() * 30;
    const light = r() < 0.7, a = (light ? 0.05 + r() * 0.13 : 0.03 + r() * 0.06) * STR;
    g.strokeStyle = light ? `rgba(250,242,218,${a})` : `rgba(35,22,12,${a})`;
    for (let b = 0; b < n; b++) {
      const off = (b / n - 0.5) * wd, lw = 0.8 + r() * 2.2; g.lineWidth = lw;
      let d = r() * 20; const ex = Math.cos(ang), ey = Math.sin(ang), nx = -ey, ny = ex;
      while (d < len) {
        const dl = 8 + r() * 60, gap = 2 + r() * 14 * (d / len + 0.2);
        const ax = x0 + ex * d + nx * off, ay = y0 + ey * d + ny * off;
        for (const ox of [-S, 0, S]) for (const oy of [-S, 0, S]) { g.beginPath(); g.moveTo(ax + ox, ay + oy); g.lineTo(ax + ex * dl + ox, ay + ey * dl + oy); g.stroke(); }
        d += dl + gap;
      }
    }
  }
  // tooth of the paper catching the pigment
  const id = g.getImageData(0, 0, S, S), p = id.data;
  for (let i = 0; i < p.length; i += 4) { const v = (r() - 0.5) * 10; p[i] += v; p[i + 1] += v; p[i + 2] += v; }
  g.putImageData(id, 0, 0);
  return c;
}
function bakeTextures() {
  let s = 11;
  for (const k of ['mustard', 'teal', 'tealD', 'orange', 'olive', 'oliveL', 'ink', 'skin', 'rose', 'sky', 'grey', 'white', 'cream']) {
    const cnv = bakeBrush(C[k], s++ * 97, k === 'skin' || k === 'cream' || k === 'white' ? 0.55 : k === 'mustard' || k === 'ink' ? 0.75 : 1); TEX[k] = cnv;
  }
  // paper: cream with fibres and speckle (static, laid over everything with multiply)
  PAPER = mk(W, H); const g = PAPER.getContext('2d'), r = mulberry(7);
  g.fillStyle = '#ffffff'; g.fillRect(0, 0, W, H);
  const id = g.getImageData(0, 0, W, H), p = id.data;
  for (let i = 0; i < p.length; i += 4) { const v = 255 - Math.abs(r() - 0.5) * 26 - (r() < 0.004 ? 40 : 0); p[i] = v; p[i + 1] = v - 2; p[i + 2] = v - 8; }
  g.putImageData(id, 0, 0);
  g.strokeStyle = 'rgba(120,95,60,0.07)';
  for (let i = 0; i < 1400; i++) { const x = r() * W, y = r() * H, a = r() * TAU, l = 6 + r() * 26; g.lineWidth = 0.6 + r(); g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + Math.cos(a + 1) * l * 0.5, y + Math.sin(a + 1) * l * 0.5, x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke(); }
  const vg = g.createRadialGradient(W / 2, H / 2, H * 0.45, W / 2, H / 2, H * 1.05);
  vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(70,45,20,0.22)'); g.fillStyle = vg; g.fillRect(0, 0, W, H);
  // crayon line texture: charcoal with a waxy broken tooth
  CRAYON = mk(512, 512); const cg = CRAYON.getContext('2d'); const cid = cg.createImageData(512, 512), cp = cid.data; const rr = mulberry(33);
  for (let i = 0; i < cp.length; i += 4) { cp[i] = 42; cp[i + 1] = 37; cp[i + 2] = 33; cp[i + 3] = rr() < 0.2 ? 60 + rr() * 80 : 205 + rr() * 50; }
  cg.putImageData(cid, 0, 0);
}
let g; // main context, set in scene
const PAT = {};
function pat(k) { if (!PAT[k]) PAT[k] = g.createPattern(k === 'crayon' ? CRAYON : TEX[k], 'repeat'); return PAT[k]; }

// ---- drawing primitives ----
// polygon from flat [x,y,...] list; slight static wobble on edges (hand-cut) via seeded midpoints
function poly(pts, wob = 0, seed = 1) {
  const p = new Path2D(); const n = pts.length / 2; const r = mulberry(seed);
  for (let i = 0; i < n; i++) {
    const x = pts[i * 2], y = pts[i * 2 + 1];
    if (i === 0) p.moveTo(x, y); else p.lineTo(x, y);
    if (wob) { const j = (i + 1) % n, x2 = pts[j * 2], y2 = pts[j * 2 + 1], mx = (x + x2) / 2, my = (y + y2) / 2, l = Math.hypot(x2 - x, y2 - y);
      if (l > 40) { const nx = -(y2 - y) / l, ny = (x2 - x) / l, d = (r() - 0.5) * wob; p.lineTo(mx + nx * d, my + ny * d); } }
  }
  p.closePath(); return p;
}
// textured flat fill (texture follows the current transform, so it rides with a sliding cel)
function fill(path, k, a = 1) { g.globalAlpha = a; g.fillStyle = TEX[k] ? pat(k) : k; g.fill(path); g.globalAlpha = 1; }
// crayon line
function line(path, w = 4, a = 0.92) { g.globalAlpha = a; g.strokeStyle = pat('crayon'); g.lineWidth = w; g.lineCap = 'round'; g.lineJoin = 'round'; g.stroke(path); g.globalAlpha = 1; }
function lineP(pts, w = 4, a = 0.92, closed = false) { const p = new Path2D(); p.moveTo(pts[0], pts[1]); for (let i = 2; i < pts.length; i += 2) p.lineTo(pts[i], pts[i + 1]); if (closed) p.closePath(); line(p, w, a); }
function rect(x, y, w, h) { return poly([x, y, x + w, y, x + w, y + h, x, y + h], 0); }
function ellipse(x, y, rx, ry, rot = 0) { const p = new Path2D(); p.ellipse(x, y, rx, ry, rot, 0, TAU); return p; }
// starburst: n spikes, alternating radii
function burst(x, y, r1, r2, n, rot = 0) { const pts = []; for (let i = 0; i < n * 2; i++) { const a = rot + i / (n * 2) * TAU, r = i % 2 ? r2 : r1; pts.push(x + Math.cos(a) * r, y + Math.sin(a) * r); } return poly(pts); }
// boomerang (the 1950s laminate shape)
function boomerang(x, y, s, rot) {
  const p = new Path2D(); const m = new DOMMatrix().translate(x, y).rotate(rot * 180 / Math.PI).scale(s);
  const q = new Path2D(); q.moveTo(-100, 10); q.quadraticCurveTo(-60, -40, 0, -18); q.quadraticCurveTo(60, -40, 100, 16); q.quadraticCurveTo(70, -5, 0, 14); q.quadraticCurveTo(-55, 0, -100, 10); q.closePath();
  p.addPath(q, m); return p;
}
// atomic sparkle: four-point star with dots on the tips
function sparkle(x, y, r, rot, col = C.ink) {
  g.save(); g.translate(x, y); g.rotate(rot); g.fillStyle = col;
  g.beginPath(); for (let i = 0; i < 8; i++) { const a = i / 8 * TAU, rr = i % 2 ? r * 0.16 : r; g.lineTo(Math.cos(a) * rr, Math.sin(a) * rr); } g.closePath(); g.fill();
  g.restore();
}
