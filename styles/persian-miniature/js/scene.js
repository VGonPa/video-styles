// scene.js · timeline, reveal, living garden (fountain, birds, blossoms), the walk, border gilding, events
const cv = document.getElementById('c'), X = cv.getContext('2d');
const TMP = mk(W, H), TG = TMP.getContext('2d');
let STATIC;   // all painted layers composited, used once every layer is fully painted
const TL = {
  fadeIn: [0, 0.5], rule: [0.25, 1.15], band: [0.5, 1.45],
  jet: 2.45, title: [2.85, 3.75], appear: [2.55, 2.95], walk: [2.95, 7.45],
  bloom2: [7.15, 7.75], bloom1: [7.45, 8.1], roses: [7.25, 8.15], look: [7.45, 8.1],
  caption: [7.8, 8.55], gild: [7.7, 8.95], twinkle: [8.8, 9.6], fadeOut: [9.35, 10.0],
};
const WALK = { x0: 780, x1: 1510 };
const TITLE = 'The Garden of Patience', CAPTION = 'He who waits in the garden is never late for spring.';
const FTITLE = `700 46px ${FT}`, FCAP = `italic 400 31px ${FT}`;

// ── walk kinematics: trapezoidal speed profile, distance-driven stride ──
function walkU(t) {
  const [a, b] = TL.walk, u = seg(t, a, b), r = 0.16;   // ramp fraction at each end
  const area = 1 - r;   // integral of the unit trapezoid
  const d = u < r ? u * u / (2 * r) : u > 1 - r ? (1 - r) - (1 - u) * (1 - u) / (2 * r) : r / 2 + (u - r);
  const sp = u < r ? u / r : u > 1 - r ? (1 - u) / r : 1;
  return { d: clamp(d / area), sp: (t > a && t < b) ? sp : 0 };
}
const groundAt = x => 900 - 18 * eSine(seg(x, 1212, 1240)) - 18 * eSine(seg(x, 1288, 1314));
function figState(t) {
  const w = walkU(t), x = lerp(WALK.x0, WALK.x1, w.d), ph = (x - WALK.x0) / FIG.cyc * TAU;
  return { x, y: groundAt(x), ph, amp: Math.min(1, w.sp * 1.15) };
}

// ── reveal helpers ──
function drawRevealed(L, t) {
  if (t >= L.t1) { X.drawImage(L.c, 0, 0); return; }
  if (t <= L.t0) return;
  TG.setTransform(1, 0, 0, 1, 0, 0); TG.globalCompositeOperation = 'source-over'; TG.clearRect(0, 0, W, H);
  TG.fillStyle = '#000';
  for (const d of L.dabs) {
    if (d.ts > t) break;
    const u = eOut(clamp((t - d.ts) / d.d)); TG.beginPath(); TG.ellipse(d.x, d.y, d.r * u, d.r * u * d.sq, d.a, 0, TAU); TG.fill();
  }
  TG.globalCompositeOperation = 'source-in'; TG.drawImage(L.c, 0, 0); TG.globalCompositeOperation = 'source-over';
  X.drawImage(TMP, 0, 0);
}
function wedge(g, th) {   // two-way sweep from the top centre, half-angle th (0…π)
  g.beginPath(); g.moveTo(960, 540); g.arc(960, 540, 3000, -Math.PI / 2 - th, -Math.PI / 2 + th); g.closePath();
}
function bandPoint(a) {   // point on the band's centre line in direction a from the centre
  const hw = BO.w / 2 - 16, hh = BO.h / 2 - 16, dx = Math.cos(a), dy = Math.sin(a);
  const s = Math.min(Math.abs(dx) > 1e-6 ? hw / Math.abs(dx) : 1e9, Math.abs(dy) > 1e-6 ? hh / Math.abs(dy) : 1e9);
  return [960 + dx * s, 540 + dy * s];
}
// rulings (jadval): traced from the top centre around both ways
function rulePath(g, R, u) {
  const { x, y, w, h } = R, per = 2 * (w + h), L = u * per / 2;
  const pts = [[x + w / 2, y], [x + w, y], [x + w, y + h], [x + w / 2, y + h]], pts2 = [[x + w / 2, y], [x, y], [x, y + h], [x + w / 2, y + h]];
  for (const ps of [pts, pts2]) {
    g.beginPath(); g.moveTo(...ps[0]); let rem = L;
    for (let i = 1; i < ps.length && rem > 0; i++) { const [ax, ay] = ps[i - 1], [bx, by] = ps[i], l = Math.hypot(bx - ax, by - ay), f = Math.min(1, rem / l); g.lineTo(ax + (bx - ax) * f, ay + (by - ay) * f); rem -= l; }
    g.stroke();
  }
}
function drawRulings(t) {
  const u = eInOut(seg(t, ...TL.rule)); if (u <= 0) return;
  X.lineCap = 'square';
  const lines = [[P, 0, COL.g2, 4], [P, -6, COL.verm, 1.6], [P, -10, COL.lapis, 2], [BI, 0, COL.g2, 2.4], [BO, 0, COL.g2, 2.4], [BO, 6, COL.lapis, 1.4]];
  for (const [R, o, c, lw] of lines) { X.strokeStyle = c; X.lineWidth = lw; rulePath(X, { x: R.x + o, y: R.y + o, w: R.w - 2 * o, h: R.h - 2 * o }, u); }
}

// ── the living garden ──
function bloomTime(s) {
  if (s.b0) return 2.35 + (s.y - 150) / 250 * 0.5 + s.k * 0.25;
  const [a, b] = s.grp === 2 ? TL.bloom2 : TL.bloom1; return a + (b - a - 0.3) * (s.k * 0.6 + 0.4 * seg(Math.abs(s.x - (s.grp === 2 ? 1196 : 600)), 0, 110));
}
function drawBlossoms(t) {
  for (const s of SITES.bloss) {
    const tb = bloomTime(s), u = seg(t, tb, tb + 0.34);
    if (!s.b0 && u < 1 && t > 2.7) { const bu = (1 - eOut(u)) * (0.55 + 0.45 * eSine(seg(t, 3.0, 7.1))); if (bu > 0.02) { const z = 12 * s.s * bu; X.drawImage(SPR.bud, s.x - z / 2, s.y - z / 2, z, z); } }
    if (u <= 0) continue;
    const z = 38 * s.s * eBack(u), img = s.pink ? SPR.bP : SPR.bW;
    X.save(); X.translate(s.x, s.y); X.rotate(s.k * 6 + (1 - u) * 1.2); X.drawImage(img, -z / 2, -z / 2, z, z); X.restore();
  }
}
function drawRoses(t) {
  const [a, b] = TL.roses;
  for (const s of SITES.roses) {
    const tb = a + (b - a - 0.3) * (0.75 * seg(1300 - s.x, 0, 1200) + 0.25 * s.k), u = seg(t, tb, tb + 0.32);
    const img = [SPR.roseR, SPR.roseP, SPR.roseW][s.c];
    if (t > 2.9 && u < 1) { const z = 12 * s.s * (1 - u); X.drawImage(SPR.bud, s.x - z / 2, s.y - z / 2, z, z); }
    if (u <= 0) continue;
    const z = 40 * s.s * eBack(u); X.save(); X.translate(s.x, s.y); X.rotate(s.k * 5 + (1 - u) * 1.5); X.drawImage(img, -z / 2, -z / 2, z, z); X.restore();
  }
}
let PETALS = [];
function initPetals() {
  const r = mulberry(91);
  const src = SITES.bloss;
  for (let i = 0; i < 150; i++) {
    const s = src[Math.floor(r() * src.length)], tb = bloomTime(s) + 0.3;
    const ts = tb + r() * (9.6 - tb) * (s.b0 ? 1 : 0.9);
    if (!s.b0 && r() < 0.35) continue;
    PETALS.push({ s, ts, vx: 18 + r() * 26, vy: 30 + r() * 22, ph: r() * TAU, sp: 1.5 + r() * 2, rot: r() * TAU, sz: 8 + r() * 5, pink: s.pink });
  }
}
function drawPetals(t) {
  X.save(); X.beginPath(); X.rect(P.x, P.y, P.w, P.h); X.clip();
  for (const p of PETALS) {
    const a = t - p.ts; if (a < 0 || a > 5) continue;
    const x = p.s.x + p.vx * a + 14 * Math.sin(a * p.sp + p.ph), y = p.s.y + p.vy * a + 4 * Math.sin(a * p.sp * 2 + p.ph);
    const al = clamp(a / 0.2) * clamp((5 - a) / 0.8);
    X.globalAlpha = al; X.save(); X.translate(x, y); X.rotate(p.rot + a * 2.2); X.scale(1, 0.55 + 0.45 * Math.cos(a * p.sp * 1.3 + p.ph));
    X.drawImage(p.pink ? SPR.petalP : SPR.petal, -p.sz / 2, -p.sz / 2, p.sz, p.sz); X.restore();
  }
  X.globalAlpha = 1; X.restore();
}
function drawWater(t) {
  if (t < LAY.court.t0 + 0.5) return;
  const al = seg(t, LAY.court.t0 + 0.5, LAY.court.t1);
  X.save(); X.globalAlpha = al;
  // flowing highlights in the channels
  const top = HZ(CHAN.x + 14) + 18;
  for (const [y0, y1] of [[top, POOL.y], [POOL.y + POOL.h, PATH.y0 - 20]]) {
    X.save(); X.beginPath(); X.rect(CHAN.x, y0, CHAN.w, y1 - y0); X.clip();
    X.strokeStyle = 'rgba(255,255,255,0.8)'; X.lineWidth = 2; X.lineCap = 'round';
    for (let k = 0; k < 12; k++) { const yy = y0 + ((k * 37 + t * 60) % (y1 - y0 + 40)) - 20, xx = CHAN.x + 6 + (k * 11) % (CHAN.w - 12); X.beginPath(); X.moveTo(xx, yy); X.quadraticCurveTo(xx + 3, yy + 6, xx, yy + 12); X.stroke(); }
    X.restore();
  }
  // pool: ripples from the jet + drifting glints
  X.save(); X.beginPath(); X.rect(POOL.x, POOL.y, POOL.w, POOL.h); X.clip();
  const jt = seg(t, TL.jet, TL.jet + 0.6);
  for (let k = 0; k < 4; k++) { const ph = ((t - TL.jet) * 0.55 + k / 4) % 1; if (t < TL.jet + k * 0.45) continue; X.strokeStyle = `rgba(255,255,255,${0.55 * (1 - ph)})`; X.lineWidth = 1.6; X.beginPath(); X.ellipse(JET.x, JET.y, 34 + ph * 120, (34 + ph * 120) * 0.42, 0, 0, TAU); X.stroke(); }
  X.fillStyle = 'rgba(255,255,255,0.75)';
  for (let k = 0; k < 14; k++) { const x = POOL.x + ((k * 97 + t * 14) % POOL.w), y = POOL.y + 12 + (k * 41) % (POOL.h - 24), f = 0.5 + 0.5 * Math.sin(t * 3 + k); X.globalAlpha = al * f * 0.8; X.fillRect(x, y, 8, 1.6); }
  X.restore(); X.globalAlpha = al;
  // the jet: rises with overshoot, then plays
  if (jt > 0) {
    const hj = 74 * eBack(jt) * (1 + 0.05 * Math.sin(t * 9));
    X.lineCap = 'round';
    X.strokeStyle = 'rgba(210,230,250,0.9)'; X.lineWidth = 6; X.beginPath(); X.moveTo(JET.x, JET.y); X.lineTo(JET.x, JET.y - hj); X.stroke();
    X.strokeStyle = COL.white; X.lineWidth = 2.4; X.beginPath(); X.moveTo(JET.x, JET.y); X.lineTo(JET.x, JET.y - hj); X.stroke();
    // falling arcs of droplets
    for (let s = -1; s <= 1; s += 2) for (let k = 0; k < 3; k++) {
      const reach = (26 + k * 20) * jt, apex = JET.y - hj;
      X.strokeStyle = 'rgba(255,255,255,0.55)'; X.lineWidth = 1.6; X.beginPath();
      for (let q = 0; q <= 1.001; q += 0.1) { const x = JET.x + s * reach * q, y = apex + (JET.y - 6 - apex + k * 4) * q * q; q ? X.lineTo(x, y) : X.moveTo(x, y); } X.stroke();
      X.fillStyle = COL.white;
      for (let d = 0; d < 4; d++) { const q = ((t * 1.3 + d / 4 + k * 0.17) % 1); const x = JET.x + s * reach * q, y = apex + (JET.y - 6 - apex + k * 4) * q * q; X.beginPath(); X.arc(x, y, 2.2, 0, TAU); X.fill(); }
    }
    // crown spray
    for (let d = 0; d < 7; d++) { const a = -Math.PI / 2 + (d - 3) * 0.35, q = (t * 2 + d * 0.13) % 1, rd = 8 + q * 14; X.globalAlpha = al * (1 - q); X.beginPath(); X.arc(JET.x + Math.cos(a) * rd, JET.y - hj + Math.sin(a) * rd * 0.6 + q * 10, 1.8, 0, TAU); X.fill(); }
  }
  X.restore();
}
// birds: white doves crossing the gold sky, wings beating
const BIRDS = [
  { t0: 3.3, t1: 7.6, y: 236, amp: 16, s: 1.3, ph: 0.0, f: 4.2 },
  { t0: 3.55, t1: 7.9, y: 214, amp: 10, s: 1.1, ph: 1.9, f: 4.8 },
  { t0: 4.1, t1: 8.6, y: 250, amp: 14, s: 1.05, ph: 3.1, f: 4.5 },
];
function drawBird(g, x, y, s, flap, dir) {
  g.save(); g.translate(x, y); g.scale(s * dir, s);
  const wy = Math.sin(flap) * 16;
  g.fillStyle = COL.white; g.strokeStyle = COL.inkS; g.lineWidth = 1.4;
  // far wing
  g.beginPath(); g.moveTo(-2, -2); g.quadraticCurveTo(-8, -8 - wy * 0.6, -18, -12 - wy); g.quadraticCurveTo(-8, -2, 4, 0); g.closePath(); g.fillStyle = '#e6e0d2'; g.fill(); g.stroke();
  // body + tail + head
  g.fillStyle = COL.white;
  g.beginPath(); g.moveTo(-22, 2); g.lineTo(-30, -2); g.lineTo(-29, 6); g.closePath(); g.fill(); g.stroke();
  g.beginPath(); g.ellipse(-4, 1, 16, 6.5, -0.05, 0, TAU); g.fill(); g.stroke();
  g.beginPath(); g.arc(12, -3, 5, 0, TAU); g.fill(); g.stroke();
  g.fillStyle = COL.ochreD; g.beginPath(); g.moveTo(16.5, -3.5); g.lineTo(22, -2); g.lineTo(16.5, -1); g.fill();
  g.fillStyle = COL.ink; g.beginPath(); g.arc(13.5, -4, 1.1, 0, TAU); g.fill();
  // near wing
  g.fillStyle = COL.white; g.beginPath(); g.moveTo(-6, 0); g.quadraticCurveTo(-4, -10 - wy, -14, -22 - wy * 1.2); g.quadraticCurveTo(0, -12 - wy * 0.5, 6, -1); g.closePath(); g.fill(); g.stroke();
  g.strokeStyle = 'rgba(80,60,40,0.5)'; g.lineWidth = 1; for (let k = 0; k < 3; k++) { g.beginPath(); g.moveTo(-4 + k * 3, -2); g.lineTo(-10 + k * 3, -14 - wy * (0.8 - k * 0.2)); g.stroke(); }
  g.restore();
}
function drawBirds(t) {
  X.save(); X.beginPath(); X.rect(P.x, P.y, P.w, P.h); X.clip();
  for (const b of BIRDS) {
    const u = seg(t, b.t0, b.t1); if (u <= 0 || u >= 1) continue;
    const x = lerp(P.x - 40, P.x + P.w + 40, u), y = b.y + b.amp * Math.sin(u * 5 + b.ph) - 20 * Math.sin(u * Math.PI) - 100 * Math.exp(-Math.pow((x - 330) / 230, 2));
    drawBird(X, x, y, b.s, t * b.f * TAU / 2 + b.ph, 1);
  }
  X.restore();
}

// a hoopoe perched on the plane tree: pecks, looks about, raises its crest when the garden blooms
function drawHoopoe(t) {
  const a = seg(t, 2.9, 3.2); if (a <= 0) return;
  const x = 262, y = 286, peck = Math.max(0, Math.sin((t - 3.4) * 2.6)) ** 8 * (t > 3.4 ? 1 : 0), crest = eBack(seg(t, 4.6, 4.9)) * (1 - seg(t, 5.8, 6.2)) + eBack(seg(t, 7.2, 7.5));
  X.save(); X.globalAlpha = a; X.translate(x, y);
  X.lineJoin = 'round'; X.strokeStyle = COL.ink; X.lineWidth = 1.3;
  // tail + legs
  X.fillStyle = COL.ink; X.beginPath(); X.moveTo(-14, -2); X.lineTo(-30, 4); X.lineTo(-28, 10); X.lineTo(-12, 4); X.closePath(); X.fill();
  X.fillStyle = COL.white; X.fillRect(-26, 5, 6, 2);
  X.strokeStyle = COL.inkS; X.beginPath(); X.moveTo(-2, 8); X.lineTo(-4, 16); X.moveTo(3, 8); X.lineTo(3, 16); X.stroke();
  // body
  X.fillStyle = '#e3a06a'; X.beginPath(); X.ellipse(-2, 0, 15, 9, -0.15, 0, TAU); X.fill(); X.strokeStyle = COL.ink; X.stroke();
  // barred wing
  X.save(); X.beginPath(); X.ellipse(-6, -1, 11, 6.5, -0.2, 0, TAU); X.clip(); X.fillStyle = COL.ink; X.fillRect(-18, -8, 24, 16);
  X.fillStyle = COL.white; for (let k = 0; k < 4; k++) X.fillRect(-15 + k * 5, -8, 2.2, 16); X.restore();
  // head, pecking
  X.save(); X.translate(10, -6); X.rotate(0.9 * peck);
  X.fillStyle = '#e3a06a'; X.beginPath(); X.arc(0, 0, 6, 0, TAU); X.fill(); X.strokeStyle = COL.ink; X.stroke();
  X.strokeStyle = COL.inkS; X.lineWidth = 1.8; X.beginPath(); X.moveTo(5, 0); X.quadraticCurveTo(13, 1, 18, 5); X.stroke();
  X.fillStyle = COL.ink; X.beginPath(); X.arc(2, -1.5, 1.2, 0, TAU); X.fill();
  // crest: a fan of black-tipped feathers
  const cr = 0.25 + 0.75 * clamp(crest);
  for (let k = 0; k < 6; k++) { const an = -Math.PI / 2 - 0.9 * cr + k * 0.33 * cr - 0.5 * (1 - cr), l = 9 + 5 * cr; X.strokeStyle = '#e3a06a'; X.lineWidth = 3; X.beginPath(); X.moveTo(-1, -3); X.lineTo(-1 + Math.cos(an) * l, -3 + Math.sin(an) * l); X.stroke(); X.strokeStyle = COL.ink; X.lineWidth = 3; X.beginPath(); X.moveTo(-1 + Math.cos(an) * l * 0.8, -3 + Math.sin(an) * l * 0.8); X.lineTo(-1 + Math.cos(an) * l, -3 + Math.sin(an) * l); X.stroke(); }
  X.restore(); X.restore();
}
// ── cartouches ──
function cartouche(cx, cy, w, h, u) {
  if (u <= 0) return;
  const x = cx - w / 2, y = cy - h / 2, k = eOut(u);
  X.save(); X.globalAlpha = clamp(u * 3);
  // illuminated cloud-band corners (gold triangles with lapis dots) outside the panel ends
  for (const sx of [-1, 1]) {
    X.fillStyle = goldFill(X, cx + sx * w / 2, y, 30, h); X.beginPath(); X.moveTo(cx + sx * w / 2, y + 4); X.lineTo(cx + sx * (w / 2 + 30 * k), cy); X.lineTo(cx + sx * w / 2, y + h - 4); X.closePath(); X.fill();
    X.strokeStyle = COL.g4; X.lineWidth = 1.2; X.stroke(); X.fillStyle = COL.lapis; X.beginPath(); X.arc(cx + sx * (w / 2 + 10 * k), cy, 3.4, 0, TAU); X.fill();
  }
  X.fillStyle = COL.ivory; X.fillRect(x, y, w, h);
  X.strokeStyle = COL.g2; X.lineWidth = 4; X.strokeRect(x + 2, y + 2, w - 4, h - 4);
  X.strokeStyle = COL.lapis; X.lineWidth = 1.5; X.strokeRect(x + 7, y + 7, w - 14, h - 14);
  X.strokeStyle = COL.inkS; X.lineWidth = 1.2; X.strokeRect(x, y, w, h);
  X.restore();
}
function writeText(txt, font, cx, y, u, color) {
  if (u <= 0) return;
  X.font = font; const w = X.measureText(txt).width, x0 = cx - w / 2, edge = x0 + (w + 60) * u;
  X.save(); const gr = X.createLinearGradient(edge - 60, 0, edge, 0); gr.addColorStop(0, color); gr.addColorStop(1, 'rgba(0,0,0,0)');
  X.fillStyle = gr; X.textBaseline = 'alphabetic'; X.fillText(txt, x0, y); X.restore();
}

// ── gilding of the border band with a travelling glint ──
function drawBand(t) {
  const ub = eInOut(seg(t, ...TL.band));
  if (ub > 0) { X.save(); wedge(X, ub * Math.PI * 1.001); X.clip(); X.drawImage(BAND_O, 0, 0); X.restore(); }
  const ug = eInOut(seg(t, ...TL.gild));
  if (ug > 0) { X.save(); wedge(X, ug * Math.PI * 1.001); X.clip(); X.drawImage(BAND_G, 0, 0); X.restore(); }
}
function glint(x, y, s, a) {
  if (a <= 0) return;
  X.save(); X.globalCompositeOperation = 'lighter'; X.globalAlpha = a;
  const gr = X.createRadialGradient(x, y, 0, x, y, 70 * s); gr.addColorStop(0, 'rgba(255,245,200,0.8)'); gr.addColorStop(0.18, 'rgba(255,220,130,0.25)'); gr.addColorStop(1, 'rgba(255,200,100,0)');
  X.fillStyle = gr; X.fillRect(x - 70 * s, y - 70 * s, 140 * s, 140 * s);
  X.strokeStyle = 'rgba(255,250,225,0.9)'; X.lineWidth = 1.6; X.beginPath(); X.moveTo(x - 30 * s, y); X.lineTo(x + 30 * s, y); X.moveTo(x, y - 30 * s); X.lineTo(x, y + 30 * s); X.stroke();
  X.restore();
}

// ── frame ──
function drawFrame(t) {
  X.setTransform(1, 0, 0, 1, 0, 0); X.fillStyle = '#1a0f08'; X.fillRect(0, 0, W, H);
  const z = 1 + 0.028 * eSine(clamp(t / 10));
  X.setTransform(z, 0, 0, z, 960 * (1 - z), 560 * (1 - z));
  X.drawImage(PAPER, 0, 0);
  drawBand(t);
  drawRulings(t);
  // painting
  if (t >= LAY.plants.t1) X.drawImage(STATIC, 0, 0);
  else for (const k of ['sky', 'ground', 'court', 'pav', 'trees', 'plants']) drawRevealed(LAY[k], t);
  drawWater(t);
  drawBlossoms(t); drawRoses(t);
  drawBirds(t); drawHoopoe(t);
  // the gardener
  const fa = eOut(seg(t, ...TL.appear));
  if (fa > 0) {
    const f = figState(t), look = 0.22 * eInOut(seg(t, ...TL.look)) - 0.1 * eInOut(seg(t, 9.0, 9.6));
    X.save(); X.globalAlpha = fa; X.beginPath(); X.rect(P.x, P.y, P.w, P.h); X.clip(); drawFigure(X, f.x, f.y, f.ph, f.amp, t, look); X.restore();
  }
  drawPetals(t);
  // title cartouche and closing caption
  const ut = seg(t, ...TL.title);
  cartouche(960, 158, 560, 76, eOut(seg(ut, 0, 0.45)));
  writeText(TITLE, FTITLE, 960, 172, eInOut(seg(ut, 0.3, 1)), COL.lapisD);
  const uc = seg(t, ...TL.caption);
  cartouche(960, 952, 820, 52, eOut(seg(uc, 0, 0.4)));
  writeText(CAPTION, FCAP, 960, 962, eInOut(seg(uc, 0.25, 1)), COL.ink);
  // gold flecks twinkle once the border is gilded
  for (const f of FLECKS) { const tw = seg(t, TL.twinkle[0] + f.ph * 0.5, TL.twinkle[0] + f.ph * 0.5 + 0.35); if (tw > 0 && tw < 1 && f.ph < 0.45) glint(f.x, f.y, 0.22 * f.s / 4, Math.sin(Math.PI * tw) * 0.9); }
  // glints riding the gilding fronts
  const ug = seg(t, ...TL.gild);
  if (ug > 0 && ug < 1) { const th = eInOut(ug) * Math.PI, a = Math.sin(Math.PI * ug); for (const s of [-1, 1]) { const [x, y] = bandPoint(-Math.PI / 2 + s * th); glint(x, y, 0.7, a); } }
  X.globalCompositeOperation = 'multiply'; X.drawImage(GRAIN, 0, 0); X.globalCompositeOperation = 'source-over';
  X.setTransform(1, 0, 0, 1, 0, 0);
  const fade = 1 - seg(t, ...TL.fadeIn) + eIn(seg(t, ...TL.fadeOut));
  if (fade > 0) { X.fillStyle = `rgba(20,12,6,${clamp(fade)})`; X.fillRect(0, 0, W, H); }
}

// ── events for the sound design ──
window.events = () => {
  const ev = [{ k: 'rule', t: TL.rule[0] }, { k: 'band', t: TL.band[0], d: TL.band[1] - TL.band[0] }];
  for (const k of ['sky', 'ground', 'court', 'pav', 'trees', 'plants']) ev.push({ k: 'paint', t: LAY[k].t0, d: LAY[k].t1 - LAY[k].t0 });
  ev.push({ k: 'jet', t: TL.jet }, { k: 'title', t: TL.title[0] + 0.25, d: 0.65 });
  let last = 0; for (let t = TL.walk[0]; t < TL.walk[1] + 0.2; t += 1 / 120) { const f = figState(t), n = Math.floor(f.ph / Math.PI + 0.5); if (n > last) { last = n; ev.push({ k: 'step', t, a: f.amp, stone: f.x > 1214 }); } }
  for (const b of BIRDS) for (let t = b.t0 + 0.4; t < b.t1 - 0.4; t += 1.1 + (b.ph % 0.5)) ev.push({ k: 'chirp', t, pan: (seg(t, b.t0, b.t1) * 2 - 1) * 0.8 });
  for (const s of SITES.bloss) if (!s.b0) ev.push({ k: 'pop', t: bloomTime(s), pan: (s.x - 960) / 960 });
  ev.push({ k: 'caption', t: TL.caption[0] + 0.2, d: 0.6 }, { k: 'gild', t: TL.gild[0], d: TL.gild[1] - TL.gild[0] }, { k: 'twinkle', t: TL.twinkle[0] }, { k: 'end', t: 9.2 });
  return ev.sort((a, b) => a.t - b.t);
};

window.ready = (async () => {
  await document.fonts.load(FTITLE, TITLE); await document.fonts.load(FCAP, CAPTION); await document.fonts.ready;
  bakePaper(); bakeGrain(); bakeSprites(); bakeLayers(); bakeBand(); initPetals();
  STATIC = mk(W, H); const g = STATIC.getContext('2d'); for (const k of ['sky', 'ground', 'court', 'pav', 'trees', 'plants']) g.drawImage(LAY[k].c, 0, 0);
})();
window.draw = ({ t }) => { drawFrame(t); return cv.toDataURL('image/jpeg', 0.92).split(',')[1]; };
