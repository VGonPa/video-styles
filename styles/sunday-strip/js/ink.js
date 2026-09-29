// ── ink.js · brush-ink strokes, watercolor washes, paper textures (all deterministic) ──
const W = 1920, H = 1080, TAU = Math.PI * 2;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eInOut = u => u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
const eOut = u => 1 - Math.pow(1 - u, 3);
const eIn = u => u * u * u;
const backOut = (u, c = 1.7) => u >= 1 ? 1 : 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2);
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const mk = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
const hash = (x) => { const s = Math.sin(x * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const vnoise = x => { const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f); return lerp(hash(i), hash(i + 1), u); };

const INK = '#1e1a17';
let ctx;                       // current target context (switched for offscreen baking)
const useCtx = c => { const p = ctx; ctx = c; return p; };

// Catmull-Rom densify
function cr(pts, closed, n = 7) {
  const out = [], L = pts.length, m = closed ? L : L - 1;
  const P = i => closed ? pts[(i + L) % L] : pts[clamp(i, 0, L - 1)];
  for (let i = 0; i < m; i++) {
    const p0 = P(i - 1), p1 = P(i), p2 = P(i + 1), p3 = P(i + 2);
    for (let k = 0; k < n; k++) {
      const u = k / n, u2 = u * u, u3 = u2 * u;
      out.push([
        0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * u + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * u2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * u3),
        0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * u + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * u2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * u3)]);
    }
  }
  if (!closed) out.push(pts[L - 1]);
  return out;
}
function tracePts(p, closed) { ctx.beginPath(); ctx.moveTo(p[0][0], p[0][1]); for (let i = 1; i < p.length; i++) ctx.lineTo(p[i][0], p[i][1]); if (closed) ctx.closePath(); }
// transform a point list: translate + scale + rotate about origin
const xf = (pts, x, y, s = 1, r = 0, fx = 1) => { const c = Math.cos(r), sn = Math.sin(r); return pts.map(([a, b]) => { a *= fx; return [x + s * (a * c - b * sn), y + s * (a * sn + b * c)]; }); };
const circ = (x, y, rx, ry = rx, n = 14, wob = 0, seed = 1) => { const R = rng(seed), o = []; for (let i = 0; i < n; i++) { const a = i / n * TAU, k = 1 + wob * (R() - .5); o.push([x + Math.cos(a) * rx * k, y + Math.sin(a) * ry * k]); } return o; };

// tapered brush stroke along a polyline (smoothed)
function brush(pts, w = 4, o = {}) {
  const closed = !!o.closed, p = o.raw ? pts : cr(pts, closed, o.n || 7);
  if (p.length < 2) return;
  const seed = o.seed ?? (pts[0][0] * 0.37 + pts[0][1] * 0.11);
  const ta = o.ta ?? 0.18, tb = o.tb ?? 0.22, col = o.col || INK;
  const len = [0]; for (let i = 1; i < p.length; i++) len.push(len[i - 1] + Math.hypot(p[i][0] - p[i - 1][0], p[i][1] - p[i - 1][1]));
  const Lt = len[len.length - 1] || 1, Lp = [], Rp = [];
  for (let i = 0; i < p.length; i++) {
    const a = p[Math.max(0, i - 1)], b = p[Math.min(p.length - 1, i + 1)];
    let dx = b[0] - a[0], dy = b[1] - a[1]; const d = Math.hypot(dx, dy) || 1; dx /= d; dy /= d;
    const u = len[i] / Lt;
    let prof = closed ? 0.78 + 0.22 * Math.sin(u * TAU * 1.5 + seed) : Math.pow(clamp(u / ta), 0.55) * Math.pow(clamp((1 - u) / tb), 0.6);
    prof = Math.max(prof, closed ? 0 : 0.1);
    const ww = w * prof * (0.82 + 0.36 * vnoise(len[i] * 0.025 + seed * 3.1)) / 2;
    Lp.push([p[i][0] - dy * ww, p[i][1] + dx * ww]); Rp.push([p[i][0] + dy * ww, p[i][1] - dx * ww]);
  }
  ctx.save(); ctx.fillStyle = col; if (o.a != null) ctx.globalAlpha *= o.a;
  if (closed) { tracePts(Lp, true); ctx.moveTo(Rp[0][0], Rp[0][1]); for (let i = Rp.length - 1; i >= 0; i--) ctx.lineTo(Rp[i][0], Rp[i][1]); ctx.closePath(); ctx.fill('evenodd'); }
  else { ctx.beginPath(); ctx.moveTo(Lp[0][0], Lp[0][1]); for (const q of Lp) ctx.lineTo(q[0], q[1]); for (let i = Rp.length - 1; i >= 0; i--) ctx.lineTo(Rp[i][0], Rp[i][1]); ctx.closePath(); ctx.fill(); }
  ctx.restore();
}
// a closed outline drawn as two or three overlapping brush strokes (never a mechanical uniform line)
function inkShape(pts, w = 4, o = {}) {
  const p = cr(pts, true, o.n || 7), n = p.length;
  const seed = o.seed ?? 1, R = rng(Math.floor(seed * 1000) + 7), k0 = Math.floor(R() * n);
  const parts = o.parts || 2; const overlap = Math.floor(n * 0.06);
  for (let j = 0; j < parts; j++) {
    const a = k0 + Math.floor(j * n / parts), b = k0 + Math.floor((j + 1) * n / parts) + overlap;
    const sp = []; for (let i = a; i <= b; i++) sp.push(p[i % n]);
    brush(sp, w, { raw: true, ta: 0.08, tb: 0.12, seed: seed + j * 1.7, col: o.col });
  }
}
// ── watercolor ──
let GRAN, PAPER_T, BLOOM;
function bbox(p) { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (const [x, y] of p) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); } return [x0, y0, x1 - x0, y1 - y0]; }
// wash: transparent pigment fill, granulation, darker drying edge; slightly off-register from the ink
function wash(pts, col, o = {}) {
  const p = o.raw ? pts : cr(pts, true, 6), off = o.off || [4, 3];
  ctx.save();
  if (o.base) { tracePts(p, true); ctx.fillStyle = o.base; ctx.fill(); }
  ctx.translate(off[0], off[1]);
  tracePts(p, true); ctx.globalAlpha = o.a ?? 0.9; ctx.fillStyle = col; ctx.fill();
  const [bx, by, bw, bh] = bbox(p);
  if ((o.gran ?? 0.65) > 0 && bw > 2 && bh > 2) {
    ctx.save(); ctx.clip(); ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = o.gran ?? 0.65;
    const R = rng(Math.floor(bx * 13 + by * 7) | 0), sx = R() * 500, sy = R() * 500, sc = o.gs || 1;
    ctx.drawImage(GRAN, sx, sy, Math.min(512, bw / sc), Math.min(512, bh / sc), bx, by, bw, bh);
    ctx.restore();
  }
  if ((o.edge ?? 0.6) > 0) {
    tracePts(p, true); ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = (o.edge ?? 0.6) * 0.6;
    ctx.strokeStyle = col; ctx.lineWidth = o.ew || 4.2; ctx.lineJoin = 'round'; ctx.stroke();
  }
  ctx.restore();
}
// wash clipped glaze: gradient shading inside a shape (for form and depth)
function glaze(pts, grad, a = 0.5, raw) {
  const p = raw ? pts : cr(pts, true, 6);
  ctx.save(); tracePts(p, true); ctx.clip(); ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = a; ctx.fillStyle = grad;
  const [bx, by, bw, bh] = bbox(p); ctx.fillRect(bx - 4, by - 4, bw + 8, bh + 8); ctx.restore();
}
const lgrad = (x0, y0, x1, y1, stops) => { const g = ctx.createLinearGradient(x0, y0, x1, y1); stops.forEach(([o, c]) => g.addColorStop(o, c)); return g; };
const rgrad = (x, y, r0, r1, stops) => { const g = ctx.createRadialGradient(x, y, r0, x, y, r1); stops.forEach(([o, c]) => g.addColorStop(o, c)); return g; };
// loose wet-in-wet blob (soft edge, used for skies, foliage glow, cheek blush)
const hexA = (h, a) => { const n = parseInt(h.slice(1), 16); return `rgba(${n >> 16},${n >> 8 & 255},${n & 255},${a})`; };
function softBlob(x, y, r, col, a = 0.4) {
  ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = rgrad(x, y, 0, r, [[0, col], [0.35, col], [1, hexA(col, 0)]]);
  ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill(); ctx.restore();
}

function buildInkTextures() {
  // granulation: clustered pigment specks + low-frequency pooling, grey on white (multiply)
  GRAN = mk(1024, 1024); { const g = GRAN.getContext('2d'); const R = rng(88);
    g.fillStyle = '#fff'; g.fillRect(0, 0, 1024, 1024);
    for (let i = 0; i < 260; i++) { const x = R() * 1024, y = R() * 1024, r = 40 + R() * 160; g.fillStyle = rgradOn(g, x, y, r, `rgba(140,128,115,${0.1 + R() * 0.18})`); g.fillRect(x - r, y - r, 2 * r, 2 * r); }
    for (let i = 0; i < 26000; i++) { const x = R() * 1024, y = R() * 1024; g.fillStyle = `rgba(90,80,70,${0.05 + R() * 0.16})`; g.fillRect(x, y, 1 + R() * 1.6, 1 + R() * 1.6); }
    // back-run blooms: pale rings
    for (let i = 0; i < 40; i++) { const x = R() * 1024, y = R() * 1024, r = 20 + R() * 70; g.strokeStyle = `rgba(120,110,100,${0.08 + R() * 0.08})`; g.lineWidth = 2 + R() * 3; g.beginPath(); for (let k = 0; k <= 24; k++) { const a = k / 24 * TAU, rr = r * (1 + 0.25 * Math.sin(a * 3 + i)); k ? g.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr) : g.moveTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr); } g.stroke(); }
  }
  // cold-press paper: soft tooth + fibres, multiplied over everything
  PAPER_T = mk(1024, 1024); { const g = PAPER_T.getContext('2d'); const R = rng(9);
    g.fillStyle = '#fff'; g.fillRect(0, 0, 1024, 1024);
    const id = g.getImageData(0, 0, 1024, 1024), d = id.data;
    // tooth: sum of two value-noise octaves, wrapped
    const N = 64, grid = []; for (let i = 0; i < N * N; i++) grid.push(R());
    const G = (x, y) => grid[((y % N + N) % N) * N + ((x % N + N) % N)];
    const vn = (x, y) => { const xi = Math.floor(x), yi = Math.floor(y), fx = x - xi, fy = y - yi, ux = fx * fx * (3 - 2 * fx), uy = fy * fy * (3 - 2 * fy);
      return lerp(lerp(G(xi, yi), G(xi + 1, yi), ux), lerp(G(xi, yi + 1), G(xi + 1, yi + 1), ux), uy); };
    for (let y = 0; y < 1024; y++) for (let x = 0; x < 1024; x++) {
      const v = vn(x / 16, y / 16) * 0.6 + vn(x / 6, y / 6) * 0.4, sp = R();
      const k = 246 - v * 16 - (sp < 0.02 ? 14 : 0), i = (y * 1024 + x) * 4; d[i] = k + 2; d[i + 1] = k; d[i + 2] = k - 5; d[i + 3] = 255;
    }
    g.putImageData(id, 0, 0);
    for (let i = 0; i < 500; i++) { const x = R() * 1024, y = R() * 1024, a = R() * TAU, l = 6 + R() * 16; g.strokeStyle = `rgba(160,145,120,${0.12 + R() * 0.15})`; g.lineWidth = 0.8; g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + Math.cos(a) * l * .5 + 3, y + Math.sin(a) * l * .5, x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke(); }
  }
}
function rgradOn(g, x, y, r, col) { const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, col); gr.addColorStop(1, 'rgba(0,0,0,0)'); return gr; }

// hand-drawn balloon: slightly irregular ellipse, brush outline, tail, uppercase hand lettering
function balloon(cx, cy, lines, tail, pop = 1, o = {}) {
  if (pop <= 0) return;
  const fs = o.fs || 34, lh = fs * 1.12;
  ctx.save(); ctx.font = `${fs}px "Patrick Hand"`;
  const ry = lines.length * lh / 2 + fs * 0.85; let rx = 0;
  lines.forEach((l, i) => { const y = Math.abs((i - (lines.length - 1) / 2) * lh) + lh * 0.45; rx = Math.max(rx, (ctx.measureText(l).width / 2 + fs * 0.45) / Math.sqrt(Math.max(0.2, 1 - (y / ry) ** 2))); });
  const k = backOut(clamp(pop), 2.2);
  ctx.translate(cx, cy); ctx.scale(lerp(0.3, 1, k), lerp(0.3, 1, k)); ctx.globalAlpha = clamp(pop * 3);
  const pts = []; for (let i = 0; i < 28; i++) { const a = i / 28 * TAU; const w = 1 + 0.018 * Math.sin(a * 3 + cx); pts.push([Math.cos(a) * rx * w, Math.sin(a) * ry * w]); }
  const [tx, ty] = [tail[0] - cx, tail[1] - cy];
  // tail as a curved wedge joined to the ellipse
  const ang = Math.atan2(ty / ry, tx / rx), bx = Math.cos(ang) * rx * 0.92, by = Math.sin(ang) * ry * 0.92, pa = ang + Math.PI / 2, tw2 = Math.min(rx, ry) * 0.28;
  const t1 = [bx + Math.cos(pa) * tw2, by + Math.sin(pa) * tw2], t2 = [bx - Math.cos(pa) * tw2, by - Math.sin(pa) * tw2];
  const mid = [(bx + tx) / 2 + Math.cos(pa) * tw2 * 0.4, (by + ty) / 2 + Math.sin(pa) * tw2 * 0.4];
  ctx.fillStyle = o.fill || '#fffdf6';
  tracePts(cr(pts, true, 5), true); ctx.fill();
  ctx.beginPath(); ctx.moveTo(t1[0], t1[1]); ctx.quadraticCurveTo(mid[0], mid[1], tx, ty); ctx.quadraticCurveTo(mid[0] - Math.cos(pa) * tw2 * 0.3, mid[1] - Math.sin(pa) * tw2 * 0.3, t2[0], t2[1]); ctx.closePath(); ctx.fill();
  if (!o.offPanel) {
    brush([t1, mid, [tx, ty]], 3.6, { ta: 0.05, tb: 0.4, seed: 3 }); brush([t2, [mid[0] - Math.cos(pa) * tw2 * .3, mid[1] - Math.sin(pa) * tw2 * .3], [tx, ty]], 3.6, { ta: 0.05, tb: 0.4, seed: 4 });
  }
  // outline, leaving the tail mouth open
  const p = cr(pts, true, 5); const n = p.length; const ia = Math.round(((ang % TAU + TAU) % TAU) / TAU * n);
  const gap = Math.max(2, Math.round(n * tw2 / (Math.PI * (rx + ry)) * 0.9));
  const arc = []; for (let i = ia + gap; i <= ia + n - gap; i++) arc.push(p[i % n]);
  brush(arc, 3.8, { raw: true, ta: 0.04, tb: 0.04, seed: cx * 0.01 });
  if (o.offPanel) { brush([t1, mid, [tx, ty]], 3.6, { ta: 0.05, tb: 0.01, seed: 3 }); brush([t2, [mid[0] - Math.cos(pa) * tw2 * .3, mid[1] - Math.sin(pa) * tw2 * .3], [tx, ty]], 3.6, { ta: 0.05, tb: 0.01, seed: 4 }); }
  ctx.fillStyle = INK; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  lines.forEach((l, i) => ctx.fillText(l, 0, (i - (lines.length - 1) / 2) * lh + fs * 0.04));
  ctx.restore();
}
