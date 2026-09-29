// lib.js · helpers, palette and the baked papyrus textures (all deterministic, seeded)
const TAU = Math.PI * 2;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eOut = u => 1 - Math.pow(1 - u, 3);
const eIn = u => u * u * u;
const eInOut = u => u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
const eBack = u => { const c = 1.9; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
function mulberry(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const hash = n => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
function mk(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }

// mineral palette (as painted on papyrus)
const COL = {
  ink: '#1c1713', red: '#a53a22', redD: '#8a2e1b', skinM: '#a4492b', skinW: '#d9a24e',
  ochre: '#d6a23f', ochreD: '#b9822c', gold: '#e2b44f', blue: '#2e5f93', blueL: '#5b8fbf', blueD: '#1f4570',
  green: '#4c8a67', greenL: '#78ad7c', greenD: '#2f6649', white: '#efe6cf', brown: '#6d4228', silt: '#3a2a1f',
  pap: '#e8d4a2',
};

// ── papyrus: two crossed layers of pith strips, sheet joins, blotches, frayed edge ──
let SHEET, FIB, SX0 = 60, SX1 = 1860, SY0 = 34, SY1 = 1046;
function bakePapyrus() {
  const W = 1920, H = 1080, r = mulberry(95);
  const base = mk(W, H), b = base.getContext('2d');
  b.fillStyle = COL.pap; b.fillRect(0, 0, W, H);
  // broad warm blotches
  for (let i = 0; i < 70; i++) {
    const x = r() * W, y = r() * H, rad = 80 + r() * 260, dark = r() < 0.6;
    const g = b.createRadialGradient(x, y, 0, x, y, rad);
    g.addColorStop(0, dark ? 'rgba(160,110,50,0.10)' : 'rgba(255,245,215,0.12)'); g.addColorStop(1, 'rgba(0,0,0,0)');
    b.fillStyle = g; b.fillRect(x - rad, y - rad, rad * 2, rad * 2);
  }
  // fiber layer (grayscale, multiplied over paint too)
  const fib = mk(W, H), f = fib.getContext('2d');
  f.fillStyle = '#fff'; f.fillRect(0, 0, W, H);
  const strips = (horiz) => {
    const L = horiz ? H : W; let p = 0;
    while (p < L) {
      const w = 7 + r() * 16, shade = r();
      const a = horiz ? 0.04 + shade * 0.06 : 0.012 + shade * 0.02;
      f.fillStyle = `rgba(120,85,40,${a})`;
      horiz ? f.fillRect(0, p, W, w) : f.fillRect(p, 0, w, H);
      // strip edges: fine darker lines
      f.strokeStyle = `rgba(95,62,25,${horiz ? 0.06 + r() * 0.1 : 0.02 + r() * 0.04})`; f.lineWidth = 0.7 + r() * 0.7;
      f.beginPath();
      if (horiz) { f.moveTo(0, p + r()); for (let x = 0; x <= W; x += 60) f.lineTo(x, p + (r() - 0.5) * 1.6); }
      else { f.moveTo(p, 0); for (let y = 0; y <= H; y += 60) f.lineTo(p + (r() - 0.5) * 1.6, y); }
      f.stroke();
      // fibers inside the strip
      const nf = horiz ? 3 + (r() * 6 | 0) : 1;
      for (let k = 0; k < nf; k++) {
        const q = p + r() * w; f.strokeStyle = `rgba(${r() < 0.5 ? '90,60,25' : '255,250,235'},${0.06 + r() * 0.1})`; f.lineWidth = 0.6 + r() * 0.9;
        f.beginPath(); const s0 = r() * (horiz ? W : H), len = 100 + r() * 600;
        if (horiz) { f.moveTo(s0, q); f.lineTo(s0 + len, q + (r() - 0.5) * 2); } else { f.moveTo(q, s0); f.lineTo(q + (r() - 0.5) * 2, s0 + len); }
        f.stroke();
      }
      p += w;
    }
  };
  strips(true); strips(false);
  // sheet joins (kollemata): slightly darker overlapping bands
  for (let x = SX0 + 330; x < SX1; x += 452) { f.fillStyle = 'rgba(130,90,40,0.10)'; f.fillRect(x, 0, 22, H); f.fillStyle = 'rgba(100,65,25,0.14)'; f.fillRect(x + 21, 0, 1.5, H); }
  // speckles
  for (let i = 0; i < 2600; i++) { f.fillStyle = `rgba(80,50,20,${0.08 + r() * 0.25})`; const s = 0.6 + r() * 1.8; f.fillRect(r() * W, r() * H, s, s * (0.5 + r())); }
  b.globalCompositeOperation = 'multiply'; b.drawImage(fib, 0, 0); b.globalCompositeOperation = 'source-over';
  FIB = fib;
  // cut the sheet: frayed top/bottom, straight-ish sides, darker aged rim
  SHEET = mk(W, H); const s = SHEET.getContext('2d');
  const edge = (y0, dir) => { const pts = []; for (let x = SX0; x <= SX1; x += 9) pts.push([x, y0 + dir * (r() * 5 + (r() < 0.06 ? r() * 12 : 0))]); return pts; };
  const top = edge(SY0, 1), bot = edge(SY1, -1).reverse();
  s.beginPath(); top.forEach((p, i) => i ? s.lineTo(p[0], p[1]) : s.moveTo(p[0], p[1])); bot.forEach(p => s.lineTo(p[0], p[1])); s.closePath();
  s.save(); s.clip(); s.drawImage(base, 0, 0);
  const rim = (x0, y0, x1, y1) => { const g = s.createLinearGradient(x0, y0, x1, y1); g.addColorStop(0, 'rgba(120,70,25,0.30)'); g.addColorStop(1, 'rgba(120,70,25,0)'); return g; };
  s.fillStyle = rim(0, SY0, 0, SY0 + 40); s.fillRect(0, 0, W, SY0 + 40);
  s.fillStyle = rim(0, SY1, 0, SY1 - 40); s.fillRect(0, SY1 - 40, W, 60);
  s.fillStyle = rim(SX0, 0, SX0 + 40, 0); s.fillRect(SX0, 0, 40, H);
  s.fillStyle = rim(SX1, 0, SX1 - 40, 0); s.fillRect(SX1 - 40, 0, 40, H);
  s.restore();
}

// dark linen/wood table behind the sheet
let TABLE;
function bakeTable() {
  TABLE = mk(1920, 1080); const c = TABLE.getContext('2d'), r = mulberry(7);
  c.fillStyle = '#2a1c12'; c.fillRect(0, 0, 1920, 1080);
  for (let y = 0; y < 1080; y += 2) { c.fillStyle = `rgba(${r() < 0.5 ? '0,0,0' : '90,60,35'},${r() * 0.12})`; c.fillRect(0, y, 1920, 2); }
  for (let i = 0; i < 40; i++) { c.strokeStyle = `rgba(0,0,0,${0.1 + r() * 0.15})`; c.lineWidth = 1 + r() * 2; c.beginPath(); const y = r() * 1080; c.moveTo(0, y); c.bezierCurveTo(600, y + (r() - 0.5) * 40, 1300, y + (r() - 0.5) * 40, 1920, y + (r() - 0.5) * 30); c.stroke(); }
  const g = c.createRadialGradient(960, 540, 300, 960, 540, 1150); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,0.6)'); c.fillStyle = g; c.fillRect(0, 0, 1920, 1080);
}

// ── ink helpers: slightly wobbly painted outlines ──
let X, LW = 2.6; // current context, default outline width
function poly(pts, close = true) { X.beginPath(); X.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) X.lineTo(pts[i][0], pts[i][1]); if (close) X.closePath(); }
function smooth(pts, close = true) {   // quadratic through midpoints
  const n = pts.length; X.beginPath();
  if (close) {
    const m0 = [(pts[n - 1][0] + pts[0][0]) / 2, (pts[n - 1][1] + pts[0][1]) / 2]; X.moveTo(m0[0], m0[1]);
    for (let i = 0; i < n; i++) { const p = pts[i], q = pts[(i + 1) % n]; X.quadraticCurveTo(p[0], p[1], (p[0] + q[0]) / 2, (p[1] + q[1]) / 2); }
    X.closePath();
  } else {
    X.moveTo(pts[0][0], pts[0][1]);
    for (let i = 1; i < n - 1; i++) { const p = pts[i], q = pts[i + 1]; X.quadraticCurveTo(p[0], p[1], (p[0] + q[0]) / 2, (p[1] + q[1]) / 2); }
    X.lineTo(pts[n - 1][0], pts[n - 1][1]);
  }
}
function paint(fill, lw = LW, stroke = COL.ink) { if (fill) { X.fillStyle = fill; X.fill(); } if (lw) { X.strokeStyle = stroke; X.lineWidth = lw; X.lineJoin = 'round'; X.lineCap = 'round'; X.stroke(); } }
function line(a, b, lw = LW, c = COL.ink) { X.beginPath(); X.moveTo(a[0], a[1]); X.lineTo(b[0], b[1]); X.strokeStyle = c; X.lineWidth = lw; X.lineCap = 'round'; X.stroke(); }
// tapered limb outline along a polyline with per-point half widths
function limb(pts, ws, fill, lw = LW) {
  const L = [], R = [];
  for (let i = 0; i < pts.length; i++) {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
    let dx = b[0] - a[0], dy = b[1] - a[1]; const d = Math.hypot(dx, dy) || 1; dx /= d; dy /= d;
    L.push([pts[i][0] - dy * ws[i], pts[i][1] + dx * ws[i]]); R.push([pts[i][0] + dy * ws[i], pts[i][1] - dx * ws[i]]);
  }
  const e0 = pts[0], e1 = pts[pts.length - 1];
  X.beginPath(); X.moveTo(L[0][0], L[0][1]);
  for (let i = 1; i < L.length; i++) X.lineTo(L[i][0], L[i][1]);
  X.arc(e1[0], e1[1], ws[ws.length - 1], Math.atan2(L[L.length - 1][1] - e1[1], L[L.length - 1][0] - e1[0]), Math.atan2(R[R.length - 1][1] - e1[1], R[R.length - 1][0] - e1[0]), true);
  for (let i = R.length - 1; i >= 0; i--) X.lineTo(R[i][0], R[i][1]);
  X.arc(e0[0], e0[1], ws[0], Math.atan2(R[0][1] - e0[1], R[0][0] - e0[0]), Math.atan2(L[0][1] - e0[1], L[0][0] - e0[0]), true);
  X.closePath(); paint(fill, lw);
}
// two-bone IK: returns middle joint; bend = +1/-1 picks the side
function ik(a, c, l1, l2, bend) {
  let dx = c[0] - a[0], dy = c[1] - a[1], d = Math.hypot(dx, dy);
  const dm = Math.min(d, l1 + l2 - 0.01); const ux = dx / (d || 1), uy = dy / (d || 1);
  const x = (l1 * l1 - l2 * l2 + dm * dm) / (2 * dm), h = Math.sqrt(Math.max(0, l1 * l1 - x * x));
  return [a[0] + ux * x - uy * h * bend, a[1] + uy * x + ux * h * bend];
}
const add2 = (a, b, k = 1) => [a[0] + b[0] * k, a[1] + b[1] * k];
