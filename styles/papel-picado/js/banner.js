// banner.js · cut tissue-paper banners: baked once (mask of cuts → base + backlit versions), drawn per frame as a
// row-sliced sheet so it can unroll, swing toward the viewer, ripple in the wind and catch light through the paper.

// ---------- cut motifs (drawn as holes, then small bridges painted back in paper) ----------
function petal(g, cx, cy, a, r0, r1, wd) {
  // teardrop from r0 to r1 along angle a
  const ca = Math.cos(a), sa = Math.sin(a), px = -sa, py = ca;
  const x0 = cx + ca * r0, y0 = cy + sa * r0, x1 = cx + ca * r1, y1 = cy + sa * r1, m = (r0 + r1) / 2;
  g.moveTo(x0, y0);
  g.quadraticCurveTo(cx + ca * m + px * wd, cy + sa * m + py * wd, x1, y1);
  g.quadraticCurveTo(cx + ca * m - px * wd, cy + sa * m - py * wd, x0, y0);
}
function diamond(g, x, y, rx, ry) { g.moveTo(x, y - ry); g.lineTo(x + rx, y); g.lineTo(x, y + ry); g.lineTo(x - rx, y); g.closePath(); }
function dot(g, x, y, r) { g.moveTo(x + r, y); g.arc(x, y, r, 0, TAU); }

function motifFlower(g, cx, cy, R, paint) {
  g.beginPath(); for (let i = 0; i < 10; i++) petal(g, cx, cy, i / 10 * TAU - Math.PI / 2, R * 0.3, R * 0.98, R * 0.19); g.fill();
  g.beginPath(); for (let i = 0; i < 10; i++) petal(g, cx, cy, (i + 0.5) / 10 * TAU - Math.PI / 2, R * 0.34, R * 0.62, R * 0.07); paint(); g.fill(); g.globalCompositeOperation = 'destination-out';
  g.beginPath(); dot(g, cx, cy, R * 0.2); g.fill();
  g.beginPath(); for (let i = 0; i < 12; i++) { const a = i / 12 * TAU; dot(g, cx + Math.cos(a) * R * 0.1, cy + Math.sin(a) * R * 0.1, R * 0.028); } paint(); g.fill(); g.globalCompositeOperation = 'destination-out';
  // leaves under the bloom
  g.beginPath(); petal(g, cx - R * 0.08, cy + R * 1.02, Math.PI * 0.82, 0, R * 0.62, R * 0.17); petal(g, cx + R * 0.08, cy + R * 1.02, Math.PI * 0.18, 0, R * 0.62, R * 0.17); g.fill();
}
function motifBird(g, cx, cy, R, paint) {
  // a songbird in profile facing left: body, head, beak, raised wing, long split tail
  g.beginPath();
  g.moveTo(cx - R * 0.78, cy - R * 0.28); // beak tip
  g.lineTo(cx - R * 0.55, cy - R * 0.36);
  g.bezierCurveTo(cx - R * 0.5, cy - R * 0.66, cx - R * 0.12, cy - R * 0.68, cx - R * 0.08, cy - R * 0.36);
  g.bezierCurveTo(cx + R * 0.25, cy - R * 0.2, cx + R * 0.45, cy - R * 0.05, cx + R * 0.62, cy + R * 0.02);
  g.lineTo(cx + R * 1.02, cy - R * 0.22); g.lineTo(cx + R * 0.9, cy + R * 0.08); g.lineTo(cx + R * 1.06, cy + R * 0.16); g.lineTo(cx + R * 0.6, cy + R * 0.2);
  g.bezierCurveTo(cx + R * 0.3, cy + R * 0.42, cx - R * 0.2, cy + R * 0.42, cx - R * 0.42, cy + R * 0.1);
  g.bezierCurveTo(cx - R * 0.55, cy - R * 0.08, cx - R * 0.6, cy - R * 0.18, cx - R * 0.55, cy - R * 0.2);
  g.lineTo(cx - R * 0.78, cy - R * 0.28); g.closePath(); g.fill();
  // paint back: eye ring, wing feathers (bridges keep the cut together), tail stripes
  paint();
  g.beginPath(); dot(g, cx - R * 0.4, cy - R * 0.42, R * 0.07); g.fill();
  g.lineWidth = R * 0.045; g.lineCap = 'round';
  g.beginPath(); g.moveTo(cx - R * 0.25, cy - R * 0.08); g.bezierCurveTo(cx, cy - R * 0.62, cx + R * 0.32, cy - R * 0.7, cx + R * 0.44, cy - R * 0.6); g.stroke();
  for (let i = 0; i < 4; i++) { g.beginPath(); g.moveTo(cx - R * 0.18 + i * R * 0.13, cy + R * 0.05 - i * R * 0.02); g.quadraticCurveTo(cx + i * R * 0.12, cy - R * 0.2, cx + R * 0.1 + i * R * 0.12, cy - R * 0.5 + i * R * 0.05); g.stroke(); }
  g.beginPath(); g.moveTo(cx + R * 0.62, cy + R * 0.08); g.lineTo(cx + R * 0.95, cy - R * 0.08); g.moveTo(cx + R * 0.62, cy + R * 0.14); g.lineTo(cx + R * 0.96, cy + R * 0.14); g.stroke();
  g.globalCompositeOperation = 'destination-out';
  g.beginPath(); dot(g, cx - R * 0.4, cy - R * 0.42, R * 0.03); g.fill();
  // branch + leaves under the bird
  g.lineWidth = R * 0.07; g.beginPath(); g.moveTo(cx - R * 0.95, cy + R * 0.62); g.quadraticCurveTo(cx, cy + R * 0.45, cx + R * 0.9, cy + R * 0.66); g.stroke();
  g.beginPath(); for (let i = 0; i < 5; i++) { const x = cx - R * 0.72 + i * R * 0.38; petal(g, x, cy + R * 0.56, i % 2 ? Math.PI * 0.35 : Math.PI * 0.62, R * 0.04, R * 0.36, R * 0.1); } g.fill();
}
function motifStar(g, cx, cy, R, paint) {
  // eight-point geometric rosette with a ring of wedges
  g.beginPath(); for (let i = 0; i < 16; i++) { const a = i / 16 * TAU - Math.PI / 2, r = i % 2 ? R * 0.42 : R * 0.98; i ? g.lineTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r) : g.moveTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r); } g.closePath(); g.fill();
  paint();
  g.beginPath(); for (let i = 0; i < 16; i++) { const a = i / 16 * TAU - Math.PI / 2, r = i % 2 ? R * 0.3 : R * 0.7; i ? g.lineTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r) : g.moveTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r); } g.closePath(); g.fill();
  g.lineWidth = R * 0.04; g.beginPath(); for (let i = 0; i < 8; i++) { const a = i / 8 * TAU - Math.PI / 2; g.moveTo(cx, cy); g.lineTo(cx + Math.cos(a) * R, cy + Math.sin(a) * R); } g.stroke();
  g.globalCompositeOperation = 'destination-out';
  g.beginPath(); for (let i = 0; i < 8; i++) petal(g, cx, cy, (i + 0.5) / 8 * TAU - Math.PI / 2, R * 0.08, R * 0.26, R * 0.06); g.fill();
  g.beginPath(); for (let i = 0; i < 8; i++) { const a = (i + 0.5) / 8 * TAU - Math.PI / 2; diamond(g, cx + Math.cos(a) * R * 0.72, cy + Math.sin(a) * R * 0.72, R * 0.05, R * 0.05); } paint(); g.fill(); g.globalCompositeOperation = 'destination-out';
  g.beginPath(); for (let i = 0; i < 24; i++) { const a = i / 24 * TAU; dot(g, cx + Math.cos(a) * R * 1.12, cy + Math.sin(a) * R * 1.12, R * 0.04); } g.fill();
}
function motifSun(g, cx, cy, R, paint) {
  // round marigold-like bloom: two rings of teardrops around a lattice heart
  g.beginPath(); for (let i = 0; i < 16; i++) petal(g, cx, cy, i / 16 * TAU, R * 0.6, R * 1.0, R * 0.11); g.fill();
  g.beginPath(); for (let i = 0; i < 12; i++) petal(g, cx, cy, (i + 0.5) / 12 * TAU, R * 0.24, R * 0.52, R * 0.1); g.fill();
  g.beginPath(); for (let i = 0; i < 6; i++) { const a = i / 6 * TAU; diamond(g, cx + Math.cos(a) * R * 0.1, cy + Math.sin(a) * R * 0.1, R * 0.045, R * 0.045); } dot(g, cx, cy, R * 0.04); g.fill();
}
const MOTIFS = [motifFlower, motifBird, motifStar, motifSun];

function shade(hex, k) { const n = parseInt(hex.slice(1), 16); const f = v => Math.round(v * k); return `rgb(${f(n >> 16)},${f(n >> 8 & 255)},${f(n & 255)})`; }
// ---------- the sheet ----------
// returns { base, lit, w, h } — w×h pixels, hem at the top
function bakeBanner(w, h, col, motif, seed, letter) {
  const rnd = mulberry(seed * 7919 + 13);
  const M = mk(w, h), g = M.getContext('2d');
  const hem = Math.round(h * 0.075), fr = h * 0.14; // bottom fringe depth
  // outline: rectangle with a scalloped / zig-zag bottom edge
  g.fillStyle = '#000'; g.beginPath(); g.moveTo(0, 0); g.lineTo(w, 0); g.lineTo(w, h - fr);
  const nS = letter ? 7 : 8, sw = w / nS, zig = (seed % 2 === 0) && !letter;
  for (let i = nS - 1; i >= 0; i--) {
    const x0 = (i + 1) * sw, x1 = i * sw;
    if (zig) { g.lineTo(x0 - sw / 2, h - 2); g.lineTo(x1, h - fr); }
    else g.bezierCurveTo(x0 - sw * 0.05, h - fr * 0.1, x1 + sw * 0.05, h - fr * 0.1, x1, h - fr);
  }
  g.closePath(); g.fill();
  g.globalCompositeOperation = 'destination-out'; g.fillStyle = '#000'; g.strokeStyle = '#000';
  const paint = () => { g.globalCompositeOperation = 'source-over'; };
  const bw = w * 0.07, top = hem + h * 0.035, bot = h - fr - h * 0.03; // border margin
  // row of little cuts along the fringe and a frame of dots/diamonds
  g.beginPath(); for (let i = 0; i < nS; i++) { const x = (i + 0.5) * sw; zig ? diamond(g, x, h - fr * 0.55, sw * 0.12, fr * 0.2) : dot(g, x, h - fr * 0.62, sw * 0.12); } g.fill();
  const fx0 = bw, fx1 = w - bw, fy0 = top, fy1 = bot;
  g.beginPath(); const nx = 9, ny = Math.round(9 * (fy1 - fy0) / (fx1 - fx0));
  for (let i = 0; i <= nx; i++) { const x = lerp(fx0, fx1, i / nx); diamond(g, x, fy0, w * 0.018, w * 0.026); diamond(g, x, fy1, w * 0.018, w * 0.026); }
  for (let j = 1; j < ny; j++) { const y = lerp(fy0, fy1, j / ny); diamond(g, fx0, y, w * 0.026, w * 0.018); diamond(g, fx1, y, w * 0.026, w * 0.018); }
  g.fill();
  // inner frame slit (thin cut line with bridges)
  g.lineWidth = w * 0.011;
  const ix0 = fx0 + w * 0.05, ix1 = fx1 - w * 0.05, iy0 = fy0 + w * 0.05, iy1 = fy1 - w * 0.05;
  for (const [ax, ay, bx, by] of [[ix0, iy0, ix1, iy0], [ix1, iy0, ix1, iy1], [ix1, iy1, ix0, iy1], [ix0, iy1, ix0, iy0]]) {
    const n = 5; for (let k = 0; k < n; k++) { const u0 = k / n + 0.02, u1 = (k + 1) / n - 0.02; g.beginPath(); g.moveTo(lerp(ax, bx, u0), lerp(ay, by, u0)); g.lineTo(lerp(ax, bx, u1), lerp(ay, by, u1)); g.stroke(); }
  }
  const cx = w / 2, cy = (iy0 + iy1) / 2, R = Math.min(ix1 - ix0, iy1 - iy0) * 0.42;
  if (letter) {
    // one bold letter cut through the paper, with little corner flowers
    let fs = (iy1 - iy0) * 0.74; g.font = `${fs}px ${FT}`;
    const mw = g.measureText(letter).width; if (mw > (ix1 - ix0) * 0.82) { fs *= (ix1 - ix0) * 0.82 / mw; g.font = `${fs}px ${FT}`; }
    g.textAlign = 'center'; g.textBaseline = 'alphabetic';
    const m = g.measureText(letter), asc = m.actualBoundingBoxAscent, dsc = m.actualBoundingBoxDescent;
    g.fillText(letter, cx, cy + (asc - dsc) / 2);
    const cr = w * 0.07;
    for (const [x, y] of [[ix0 + cr * 1.2, iy0 + cr * 1.2], [ix1 - cr * 1.2, iy0 + cr * 1.2], [ix0 + cr * 1.2, iy1 - cr * 1.2], [ix1 - cr * 1.2, iy1 - cr * 1.2]]) {
      g.beginPath(); for (let i = 0; i < 6; i++) petal(g, x, y, i / 6 * TAU, cr * 0.22, cr, cr * 0.28); g.fill();
    }
  } else {
    MOTIFS[motif](g, cx, cy - R * (motif === 0 ? 0.18 : 0), R, paint);
    g.globalCompositeOperation = 'destination-out';
    // scatter of tiny cuts in the corners
    const cr = w * 0.06;
    for (const [x, y] of [[ix0 + cr, iy0 + cr], [ix1 - cr, iy0 + cr], [ix0 + cr, iy1 - cr], [ix1 - cr, iy1 - cr]]) {
      g.beginPath(); for (let i = 0; i < 4; i++) petal(g, x, y, i / 4 * TAU + Math.PI / 4, cr * 0.18, cr * 0.95, cr * 0.26); g.fill();
    }
  }
  g.globalCompositeOperation = 'source-over';
  // two versions: the paper in room light and the paper with a lamp behind it
  const make = (fill, lit) => {
    const C = mk(w, h), c = C.getContext('2d');
    c.drawImage(M, 0, 0); c.globalCompositeOperation = 'source-in'; c.fillStyle = fill; c.fillRect(0, 0, w, h);
    c.globalCompositeOperation = 'source-atop';
    // tissue: soft mottling plus short crinkles at random angles
    const r2 = mulberry(seed * 31 + 3);
    for (let i = 0; i < 40; i++) {
      const x = r2() * w, y = r2() * h, rad = 20 + r2() * 60, lightB = r2() < 0.5;
      const gr = c.createRadialGradient(x, y, 0, x, y, rad);
      gr.addColorStop(0, lightB ? `rgba(255,255,255,${lit ? 0.1 : 0.07})` : `rgba(50,0,40,${lit ? 0.05 : 0.08})`); gr.addColorStop(1, 'rgba(0,0,0,0)');
      c.fillStyle = gr; c.fillRect(x - rad, y - rad, rad * 2, rad * 2);
    }
    for (let i = 0; i < 70; i++) {
      c.strokeStyle = r2() < 0.5 ? `rgba(255,255,255,${lit ? 0.14 : 0.08})` : `rgba(50,0,40,${lit ? 0.06 : 0.1})`;
      c.lineWidth = 0.7 + r2() * 0.8; const x = r2() * w, y = r2() * h, a = (r2() - 0.5) * 1.2 + (r2() < 0.3 ? 1.57 : 0), l = 8 + r2() * 26;
      c.beginPath(); c.moveTo(x, y); c.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); c.lineTo(x + Math.cos(a + 0.5) * l * 1.6, y + Math.sin(a + 0.5) * l * 1.6); c.stroke();
    }
    // fold creases from cutting the folded stack: centre vertical, one horizontal
    c.strokeStyle = lit ? 'rgba(255,255,255,0.22)' : 'rgba(40,0,30,0.16)'; c.lineWidth = 1.6;
    c.beginPath(); c.moveTo(w / 2 + 1, hem); c.lineTo(w / 2 - 1, h); c.moveTo(0, h * 0.52); c.lineTo(w, h * 0.5); c.stroke();
    // doubled hem folded over the string
    c.fillStyle = lit ? 'rgba(255,255,255,0.12)' : 'rgba(40,0,30,0.22)'; c.fillRect(0, 0, w, hem);
    c.fillStyle = lit ? 'rgba(255,255,255,0.35)' : 'rgba(255,255,255,0.18)'; c.fillRect(0, hem - 2, w, 2);
    if (lit) { // light blooms through the centre of the sheet
      const gr = c.createRadialGradient(w / 2, h * 0.5, 0, w / 2, h * 0.5, h * 0.62);
      gr.addColorStop(0, 'rgba(255,245,200,0.28)'); gr.addColorStop(1, 'rgba(255,250,220,0)'); c.fillStyle = gr; c.fillRect(0, 0, w, h);
    }
    return C;
  };
  return { base: make(col.c, false), lit: make(col.l, true), w, h, col, dark: shade(col.c, 0.55), rnd: rnd() };
}

// draw a banner hanging from (x, y). st = { s: scale, rot, len: 0..1 unroll, stretch, swing, sway, ripple, ph, wt, lit, alpha }
// The sheet is assembled upright in two scratch canvases (paper, backlit paper) so row seams never double up;
// the backlit copy is masked by a per-row gradient, then the whole sheet is composited once with its translucency.
const ROWS = 34;
let SC1, SC2;
function drawBanner(g, B, x, y, st) {
  const { w, h } = B, s = st.s, len = clamp(st.len);
  if (len <= 0.001) return;
  const SW = Math.ceil(w + h * 0.9), SH = Math.ceil(h * 1.08) + 4, ox = SW / 2;
  if (!SC1 || SC1.width < SW || SC1.height < SH) { SC1 = mk(Math.max(SW, 520), Math.max(SH, 380)); SC2 = mk(SC1.width, SC1.height); }
  const a = SC1.getContext('2d'), b = SC2.getContext('2d');
  a.clearRect(0, 0, SW + 2, SH + 2); b.clearRect(0, 0, SW + 2, SH + 2);
  const vis = len * h, rows = Math.max(3, Math.ceil(ROWS * len));
  let yy = 2, xx = ox;
  const hem = h * 0.075, Ls = [];
  for (let i = 0; i < rows; i++) {
    const a0 = i / rows * vis, dh = vis / rows, v = (a0 + dh / 2) / h;
    // top rows are pinned in the hem, lower rows swing toward the viewer and ripple sideways
    const pin = clamp((a0 - hem) / (h * 0.25));
    const th = pin * (st.swing * (0.4 + v) + st.ripple * 0.35 * Math.sin(v * 5.5 - st.wt * 1.7 + st.ph));
    const lat = pin * (st.sway * v * 0.9 + st.ripple * 0.18 * Math.sin(v * 7 - st.wt * 2.3 + st.ph * 1.3));
    const fy = Math.cos(th), sx = 1 - pin * 0.05 * Math.abs(Math.sin(st.wt * 1.3 + st.ph + v * 3)) * st.ripple;
    const ddy = dh * fy, dx = xx - w * sx / 2;
    a.drawImage(B.base, 0, a0, w, dh + 0.5, dx, yy, w * sx, ddy + 1);
    b.drawImage(B.lit, 0, a0, w, dh + 0.5, dx, yy, w * sx, ddy + 1);
    Ls.push([yy + ddy / 2, clamp(st.lit + 0.45 * Math.sin(th) + 0.1)]);
    yy += ddy; xx += dh * Math.sin(lat) * 0.9;
  }
  const gr = b.createLinearGradient(0, 0, 0, yy + 2);
  for (const [py, L] of Ls) gr.addColorStop(clamp(py / (yy + 2)), `rgba(0,0,0,${L})`);
  b.globalCompositeOperation = 'destination-in'; b.fillStyle = gr; b.fillRect(0, 0, SW, yy + 2); b.globalCompositeOperation = 'source-over';
  a.drawImage(SC2, 0, 0);
  g.save(); g.translate(x, y); g.rotate(st.rot); g.scale(s, s * (st.stretch || 1));
  g.globalAlpha = st.alpha; g.drawImage(SC1, 0, 0, SW, yy + 2, -ox, -2, SW, yy + 2); g.globalAlpha = 1;
  // paper still rolled up at the bottom while unfurling
  if (len < 0.995) {
    const ry = yy - 2, rx = xx - ox, rr = h * 0.035 * (1 - len * 0.6);
    const cg = g.createLinearGradient(0, ry - rr, 0, ry + rr);
    cg.addColorStop(0, B.dark); cg.addColorStop(0.45, B.col.l); cg.addColorStop(1, B.dark);
    g.fillStyle = cg; g.beginPath(); g.ellipse(rx, ry, w / 2 + 2, rr, 0, 0, TAU); g.fill();
  }
  g.restore();
}
