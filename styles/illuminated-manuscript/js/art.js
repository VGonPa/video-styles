// art.js · vines, initials, rubrication marks, the quill

// ── vine scrolls: hairline stem, spiral tendrils ending in ivy leaves and gold bezants ──
function catmull(pts, step = 4) {
  const out = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
    const len = Math.hypot(p2[0] - p1[0], p2[1] - p1[1]), n = Math.max(2, Math.ceil(len / step));
    for (let k = 0; k < n; k++) {
      const t = k / n, t2 = t * t, t3 = t2 * t;
      out.push([0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
        0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)]);
    }
  }
  out.push(pts[pts.length - 1]); return out;
}
function withLen(pl) { let s = 0; const L = [0]; for (let i = 1; i < pl.length; i++) { s += Math.hypot(pl[i][0] - pl[i - 1][0], pl[i][1] - pl[i - 1][1]); L.push(s); } return { pl, L, len: s }; }
function strokePart(g, P, frac) {   // stroke the first `frac` of a polyline
  if (frac <= 0) return; const lim = P.len * Math.min(1, frac);
  g.beginPath(); g.moveTo(P.pl[0][0], P.pl[0][1]);
  for (let i = 1; i < P.pl.length; i++) {
    if (P.L[i] <= lim) g.lineTo(P.pl[i][0], P.pl[i][1]);
    else { const a = P.L[i - 1], u = (lim - a) / (P.L[i] - a + 1e-9); g.lineTo(lerp(P.pl[i - 1][0], P.pl[i][0], u), lerp(P.pl[i - 1][1], P.pl[i][1], u)); break; }
  }
  g.stroke();
}
function ptAt(P, s) {
  s = clamp(s, 0, P.len); let i = 1; while (i < P.L.length - 1 && P.L[i] < s) i++;
  const a = P.L[i - 1], u = (s - a) / (P.L[i] - a + 1e-9);
  const p = [lerp(P.pl[i - 1][0], P.pl[i][0], u), lerp(P.pl[i - 1][1], P.pl[i][1], u)];
  const ang = Math.atan2(P.pl[i][1] - P.pl[i - 1][1], P.pl[i][0] - P.pl[i - 1][0]); return [p[0], p[1], ang];
}
function ivy(g, s) {   // ivy leaf pointing along +x, stem at origin
  g.beginPath(); g.moveTo(0, 0);
  g.bezierCurveTo(-0.1 * s, -0.5 * s, 0.35 * s, -0.75 * s, 0.5 * s, -0.42 * s);
  g.bezierCurveTo(0.62 * s, -0.3 * s, 0.8 * s, -0.16 * s, 1.05 * s, 0);
  g.bezierCurveTo(0.8 * s, 0.16 * s, 0.62 * s, 0.3 * s, 0.5 * s, 0.42 * s);
  g.bezierCurveTo(0.35 * s, 0.75 * s, -0.1 * s, 0.5 * s, 0, 0); g.closePath();
}
const LEAF_COLS = ['gold', COL.blue, COL.rose, 'gold', COL.green, COL.red];
class Vine {
  constructor(anchors, seed, o = {}) {
    const r = mulberry(seed); this.r = r;
    this.stem = withLen(catmull(anchors, 5));
    this.tend = []; this.buds = [];
    const every = o.every || 58; let side = 1, k = 0;
    for (let s = every * 0.6; s < this.stem.len - 10; s += every * (0.8 + r() * 0.4)) {
      const [x, y, a] = ptAt(this.stem, s); side = -side; k++;
      if (o.side) side = o.side;
      // spiral tendril: curvature grows along it
      const pts = [[x, y]]; let ang = a + side * (0.7 + r() * 0.4), px = x, py = y, curv = 0.012 + r() * 0.01; const n = 16 + (r() * 10 | 0);
      for (let i = 0; i < n; i++) { px += Math.cos(ang) * 4.2; py += Math.sin(ang) * 4.2; ang -= side * curv * 4.2; curv *= 1.1; pts.push([px, py]); }
      const T = withLen(pts); const endA = Math.atan2(pts[n][1] - pts[n - 1][1], pts[n][0] - pts[n - 1][0]);
      const kind = r() < (o.bezant ?? 0.35) ? 'bez' : 'leaf';
      // a leaf part-way along the tendril too (outward side)
      const mid = ptAt(T, T.len * 0.45);
      this.tend.push({ s, T, kind, end: pts[n], endA, col: LEAF_COLS[(k + (seed % 5)) % LEAF_COLS.length], size: (o.leaf || 22) * (0.8 + r() * 0.45),
        mid, midA: mid[2] - side * 1.2, midCol: LEAF_COLS[(k + 2 + seed) % LEAF_COLS.length], hasMid: r() < 0.55, side, seed: seed * 31 + k });
    }
    // gold bezants with hairline sprigs dotted along the stem
    for (let s = every * 0.3; s < this.stem.len; s += every * 0.5 * (0.8 + r() * 0.5)) {
      const [x, y, a] = ptAt(this.stem, s); const sd = r() < 0.5 ? -1 : 1, l = 10 + r() * 12;
      this.buds.push({ s, x, y, bx: x + Math.cos(a + sd * 1.3) * l, by: y + Math.sin(a + sd * 1.3) * l, rad: 3.2 + r() * 2 });
    }
    this.width = o.width || 2.2;
  }
  draw(g, p, sh = -1) {   // p: growth 0..1 ; sh: gold shine phase
    if (p <= 0) return;
    const head = p * (this.stem.len + 120);
    g.lineCap = 'round'; g.lineJoin = 'round';
    g.strokeStyle = COL.ink; g.lineWidth = this.width; strokePart(g, this.stem, head / this.stem.len);
    for (const b of this.buds) {
      const u = clamp((head - b.s) / 40); if (u <= 0) continue;
      g.lineWidth = 1; g.strokeStyle = COL.ink; g.beginPath(); g.moveTo(b.x, b.y); g.lineTo(lerp(b.x, b.bx, u), lerp(b.y, b.by, u)); g.stroke();
      const uu = eBack(clamp((head - b.s - 30) / 50)); if (uu > 0) bezant(g, b.bx, b.by, b.rad * uu, sh);
    }
    for (const d of this.tend) {
      const u = clamp((head - d.s) / (d.T.len + 30)); if (u <= 0) continue;
      g.lineWidth = 1.3; g.strokeStyle = COL.ink; strokePart(g, d.T, u / 0.85);
      if (d.hasMid) { const um = eBack(clamp((u - 0.45) / 0.3)); if (um > 0) leafAt(g, d.mid[0], d.mid[1], d.midA, d.size * 0.75 * um, d.midCol, sh, d.seed + 7); }
      const ue = eBack(clamp((u - 0.8) / 0.2)); if (ue <= 0) continue;
      if (d.kind === 'bez') bezant(g, d.end[0], d.end[1], d.size * 0.3 * ue, sh);
      else leafAt(g, d.end[0], d.end[1], d.endA, d.size * ue, d.col, sh, d.seed);
    }
  }
}
function leafAt(g, x, y, a, s, col, sh, seed) {
  g.save(); g.translate(x, y); g.rotate(a);
  if (col === 'gold') gold(g, gg => ivy(gg, s), [-0.1 * s, -0.8 * s, 1.2 * s, 1.6 * s], 1, sh, seed);
  else { ivy(g, s); g.fillStyle = col; g.fill(); g.strokeStyle = 'rgba(255,250,235,0.8)'; g.lineWidth = 1.1; g.beginPath(); g.moveTo(s * 0.12, 0); g.lineTo(s * 0.75, 0); g.stroke(); }
  ivy(g, s); g.strokeStyle = COL.ink; g.lineWidth = 1.2; g.stroke();
  g.restore();
}
function bezant(g, x, y, rad, sh) {
  if (rad <= 0.3) return;
  gold(g, gg => { gg.beginPath(); gg.arc(x, y, rad, 0, TAU); }, [x - rad, y - rad, rad * 2, rad * 2], 1, sh, (x * 7 + y) | 0);
  g.strokeStyle = COL.ink; g.lineWidth = 0.9; g.beginPath(); g.arc(x, y, rad, 0, TAU); g.stroke();
}

// ── gilded glyph: burnished gold masked by a letterform ──
const _gc = {};
function goldGlyph(g, ch, font, x, y, u, sh, seed) {   // x,y: baseline-left
  if (u <= 0) return;
  g.save(); g.font = font; const m = g.measureText(ch); g.restore();
  const w = Math.ceil(m.width + 40), h = Math.ceil(m.actualBoundingBoxAscent + m.actualBoundingBoxDescent + 40);
  const key = ch + font; const c = _gc[key] || (_gc[key] = mk(w, h)); const q = c.getContext('2d');
  const ox = 20, oy = 20 + m.actualBoundingBoxAscent;
  q.clearRect(0, 0, w, h); q.globalCompositeOperation = 'source-over';
  gold(q, gg => { gg.beginPath(); gg.rect(0, 0, w, h); }, [0, 0, w, h], u, sh, seed);
  q.globalCompositeOperation = 'destination-in'; q.font = font; q.fillStyle = '#000'; q.fillText(ch, ox, oy); q.globalCompositeOperation = 'source-over';
  // shadow of the raised letter, then letter, then contour
  g.save(); g.globalAlpha = 0.35 * clamp(u * 2); g.filter = 'blur(1.5px)'; g.font = font; g.fillStyle = '#3a2208'; g.fillText(ch, x + 2, y + 3); g.restore();
  g.drawImage(c, x - ox, y - oy);
  g.save(); g.font = font; g.lineWidth = 1.6; g.strokeStyle = `rgba(55,30,6,${0.9 * clamp(u * 1.5)})`; g.strokeText(ch, x, y); g.restore();
}

// white penwork filigree over a colored field
function filigree(g, x, y, w, h, seed, col = 'rgba(255,250,238,0.85)') {
  const r = mulberry(seed); g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip();
  g.strokeStyle = col; g.fillStyle = col; g.lineWidth = 1.1;
  for (let i = 0; i < w * h / 900; i++) {
    const cx = x + r() * w, cy = y + r() * h, rad = 5 + r() * 7, a0 = r() * TAU;
    g.beginPath(); for (let k = 0; k <= 20; k++) { const a = a0 + k * 0.32, rr2 = rad * (1 - k / 26); g.lineTo(cx + Math.cos(a) * rr2, cy + Math.sin(a) * rr2); } g.stroke();
    g.beginPath(); g.arc(cx + Math.cos(a0) * rad * 1.5, cy + Math.sin(a0) * rad * 1.5, 1.3, 0, TAU); g.fill();
  }
  g.restore();
}

// line filler: small red stroke with blue dots (fills short line ends)
function lineFiller(g, x0, x1, y) {
  if (x1 - x0 < 24) return;
  g.save(); g.strokeStyle = COL.red; g.lineWidth = 2; g.beginPath();
  for (let x = x0; x <= x1; x += 3) g.lineTo(x, y - 12 + Math.sin((x - x0) * 0.3) * 3.5); g.stroke();
  g.fillStyle = COL.blue; for (let x = x0 + 10; x < x1 - 4; x += 20) { g.beginPath(); g.arc(x, y - 12, 2.4, 0, TAU); g.fill(); }
  g.restore();
}

// ── quill: goose feather, tip at origin, shaft rising up-right ──
let QUILL, QSHAD; const QOX = 40, QOY = 560;
function bakeQuill() {
  const W = 620, H = 620; QUILL = mk(W, H); const g = QUILL.getContext('2d'), r = mulberry(3);
  g.translate(QOX, QOY); g.rotate(-0.95);
  // nib
  g.fillStyle = '#6b5436'; g.beginPath(); g.moveTo(0, 0); g.lineTo(34, -5); g.lineTo(34, 5); g.closePath(); g.fill();
  g.fillStyle = '#1a120c'; g.beginPath(); g.moveTo(0, 0); g.lineTo(12, -2); g.lineTo(12, 2); g.closePath(); g.fill();
  // barrel
  const bar = g.createLinearGradient(0, -6, 0, 6); bar.addColorStop(0, '#f1e6cc'); bar.addColorStop(0.5, '#d8c7a0'); bar.addColorStop(1, '#a8926a');
  g.fillStyle = bar; g.beginPath(); g.moveTo(30, -5); g.lineTo(150, -6); g.lineTo(150, 6); g.lineTo(30, 5); g.closePath(); g.fill();
  // vanes: many barbs, left vane wider
  const L = 640;
  for (let side of [-1, 1]) {
    for (let s = 120; s < L; s += 2.2) {
      const u = (s - 120) / (L - 120), wv = (side < 0 ? 62 : 40) * Math.sin(Math.PI * Math.pow(u, 0.75)) * (1 - 0.25 * u) + 4;
      const gap = hash(s * 0.13 + side) < 0.05 ? 1 : 0;   // a few splits in the vane
      if (gap) continue;
      const shade = 225 + (hash(s + side * 9) - 0.5) * 40 - u * 30;
      g.strokeStyle = `rgba(${shade},${shade - 8},${shade - 25},0.9)`; g.lineWidth = 1.6;
      g.beginPath(); g.moveTo(s, side * 3); g.quadraticCurveTo(s + wv * 0.25, side * wv * 0.6, s + wv * 0.55, side * wv); g.stroke();
    }
  }
  // rachis
  g.strokeStyle = '#c9b88f'; g.lineWidth = 4; g.beginPath(); g.moveTo(140, 0); g.quadraticCurveTo(450, -8, L, -18); g.stroke();
  g.strokeStyle = 'rgba(255,255,245,0.7)'; g.lineWidth = 1.3; g.beginPath(); g.moveTo(140, -1.5); g.quadraticCurveTo(450, -9.5, L, -19); g.stroke();
  // soft downy base
  for (let i = 0; i < 40; i++) { g.strokeStyle = `rgba(245,240,225,${0.3 + r() * 0.4})`; g.lineWidth = 1; g.beginPath(); const s = 130 + r() * 50; g.moveTo(s, 0); g.quadraticCurveTo(s + 10, (r() - 0.5) * 50, s + 20 + r() * 20, (r() - 0.5) * 70); g.stroke(); }
  QSHAD = mk(W, H); const s = QSHAD.getContext('2d'); s.filter = 'blur(7px)'; s.drawImage(QUILL, 0, 0); s.filter = 'none';
  s.globalCompositeOperation = 'source-in'; s.fillStyle = 'rgba(30,15,5,0.45)'; s.fillRect(0, 0, W, H);
}
function drawQuill(g, x, y, lift, rot) {   // screen-space
  g.save(); g.translate(x + 18 + lift * 60, y + 26 + lift * 70); g.rotate(rot); g.globalAlpha = 0.8 - lift * 0.35; g.drawImage(QSHAD, -QOX, -QOY); g.restore();
  g.save(); g.translate(x, y); g.rotate(rot); g.drawImage(QUILL, -QOX, -QOY); g.restore();
}
