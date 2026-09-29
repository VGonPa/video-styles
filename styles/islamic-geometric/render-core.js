// islamic-geometric · renderer (loaded by anim.html after the geometry is built)
// ── palette: zellige glazes ──
const C = {
  cob: [28, 58, 140], cobD: [18, 36, 92], tur: [24, 148, 150], wht: [240, 236, 224], och: [208, 150, 48],
  bis: [226, 212, 186], grout: [238, 232, 218], edge: [64, 56, 56], ink: [44, 38, 72], con: [170, 82, 54],
  wall: [232, 222, 202], vous: [226, 214, 192],
};
const col8 = f => { const n = f.v.length, a = f.area; if (n === 6) return 'cob'; if (n === 16) return 'och'; if (n === 8) return 'wht'; if (n === 4 && a > 230) return 'tur'; return 'wht'; };
const col10 = f => { const n = f.v.length, a = f.area; if (n === 20) return 'och'; if (n === 10) return 'och'; if (n === 6) return 'tur'; if (n === 4 && a > 300) return 'wht'; return 'cob'; };

function prepFaces(F, colf, seed) {
  const R = rng(seed), out = [];
  for (const f of F.faces) {
    if (f.area <= 0 || f.area > PER * PER) continue;
    let cx = 0, cy = 0, a2 = 0;
    for (let i = 0; i < f.v.length; i++) { const p = f.v[i], q = f.v[(i + 1) % f.v.length], cr = p[0] * q[1] - q[0] * p[1]; a2 += cr; cx += (p[0] + q[0]) * cr; cy += (p[1] + q[1]) * cr; }
    cx /= 3 * a2; cy /= 3 * a2;
    const path = new Path2D(); f.v.forEach((p, i) => i ? path.lineTo(p[0], p[1]) : path.moveTo(p[0], p[1])); path.closePath();
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (const p of f.v) { x0 = Math.min(x0, p[0]); y0 = Math.min(y0, p[1]); x1 = Math.max(x1, p[0]); y1 = Math.max(y1, p[1]); }
    const key = colf(f), jit = 0.93 + 0.12 * R(), warm = (R() - .5) * 10;
    const base = C[key].map((v, i) => v * jit + (i === 0 ? warm : i === 2 ? -warm : 0));
    out.push({ path, cx, cy, d: Math.hypot(cx, cy), x0, y0, x1, y1, key, base, r: R(), glint: R() < 0.07 });
  }
  return out;
}
const T8 = prepFaces(F8, col8, 8), T10 = prepFaces(F10, col10, 10);
{ const OP = new Path2D(); archPts0(0).forEach((p, i) => i ? OP.lineTo(p[0], p[1]) : OP.moveTo(p[0], p[1])); for (const f of T8) { f.glint = f.glint && ctx.isPointInPath(OP, f.cx, f.cy) && f.d > RM + 14 && Math.hypot(f.cx, f.cy) > 0; } }
const edges8 = new Path2D(); for (const [a, b] of F8.edges) { edges8.moveTo(a[0], a[1]); edges8.lineTo(b[0], b[1]); }
{ const R = rng(81); for (const s of segs8) { const m = Math.hypot(s.a[0], s.a[1]); s.ti = 2.05 + 0.85 * Math.min(m, 330) / 250 + 0.08 * R() + (s.tag.length > 1 ? 0.3 : 0); } }
for (const f of T8) f.tg = 3.0 + 1.3 * Math.pow(f.d / 250, 0.9) + 0.12 * f.r;

// ── arch geometry (world) ──
function archPts0(g) { return archPts(g); }
function archPts(g) {
  const a = ARCH.a + g, r = ARCH.r + g, c = ARCH.c, ys = ARCH.ys, hh = Math.sqrt(r * r - c * c), be = Math.atan2(hh, c), L = [];
  L.push([-a, ARCH.bot]);
  for (let i = 0; i <= 48; i++) { const th = Math.PI + be * i / 48; L.push([c + r * Math.cos(th), ys + r * Math.sin(th)]); }
  const Rr = L.slice(0, -1).reverse().map(p => [-p[0], p[1]]);
  return L.concat(Rr);
}
const polyPath = (pts, path = new Path2D()) => { pts.forEach((p, i) => i ? path.lineTo(p[0], p[1]) : path.moveTo(p[0], p[1])); path.closePath(); return path; };
const OPEN = archPts(0), OPENP = polyPath(OPEN), BANDO = archPts(ARCH.band), BANDOP = polyPath(BANDO);
const rectPts = (x0, y0, x1, y1) => [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];
const ALFI = rectPts(-ALF.x, ALF.top, ALF.x, ALF.bot), ALFO = rectPts(-ALF.x - ALF.w, ALF.top - ALF.w, ALF.x + ALF.w, ALF.bot + ALF.w);

// ── textures ──
const PLASTER = mk(W, H);
{
  const g = PLASTER.getContext('2d'), R = rng(5);
  g.fillStyle = rgb(C.wall); g.fillRect(0, 0, W, H);
  for (let i = 0; i < 1400; i++) {
    const x = R() * W, y = R() * H, r = 12 + R() * 90, lt = R() < .5;
    const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, lt ? 'rgba(255,250,240,0.045)' : 'rgba(120,96,70,0.014)'); gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gr; g.fillRect(x - r, y - r, 2 * r, 2 * r);
  }
  const id = g.getImageData(0, 0, W, H), d = id.data;
  for (let i = 0; i < d.length; i += 4) { const n = (R() - .5) * 14; d[i] += n; d[i + 1] += n; d[i + 2] += n * .9; }
  g.putImageData(id, 0, 0);
  const vg = g.createRadialGradient(W / 2, H / 2, 300, W / 2, H / 2, 1200); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(60,40,20,0.16)');
  g.fillStyle = vg; g.fillRect(0, 0, W, H);
}

// ── camera ──
function cam(t) {
  const u = smoother(seg(t, 4.3, 6.45));
  const s0 = (4.8 - 0.35 * sstep(seg(t, 0, 4.6))) * (1 + 0.04 * sstep(seg(t, 3.8, 4.35))), s1 = 1 + 0.03 * sstep(seg(t, 6.45, 10));
  return { s: Math.exp(lerp(Math.log(s0), Math.log(s1), u)), x: lerp(960, 1330, u), y: lerp(540, 590, u) };
}
const setCam = K => ctx.setTransform(K.s, 0, 0, K.s, K.x, K.y);
const inView = (f, K, rot) => {
  if (rot) return true;
  const x0 = f.x0 * K.s + K.x, x1 = f.x1 * K.s + K.x, y0 = f.y0 * K.s + K.y, y1 = f.y1 * K.s + K.y;
  return x1 > -4 && x0 < W + 4 && y1 > -4 && y0 < H + 4;
};

// ── light sweep (screen space) ──
const SWEEP = [0.94, -0.34];
const sweepAt = (t, sx, sy) => { const u = seg(t, 8.35, 9.5); if (u <= 0 || u >= 1) return 0; const pos = lerp(700, 2350, sstep(u)); const pr = sx * SWEEP[0] + sy * SWEEP[1] + 250; return Math.exp(-Math.pow((pr - pos) / 150, 2)) * Math.sin(Math.PI * u); };

// ── one tile ──
function tile(f, K, t, k, lift, strap) {
  ctx.save();
  if (k !== 1) { ctx.translate(f.cx, f.cy); ctx.scale(k, k); ctx.translate(-f.cx, -f.cy); }
  const sx = f.cx * K.s + K.x, sy = f.cy * K.s + K.y;
  const sw = sweepAt(t, sx, sy);
  const c = mix(f.base, [255, 252, 240], clamp(lift + sw * 0.45));
  ctx.fillStyle = rgb(c); ctx.fill(f.path);
  const g = ctx.createLinearGradient(f.x0, f.y0, f.x1, f.y1);
  g.addColorStop(0, `rgba(255,255,250,${0.26 + 0.2 * sw})`); g.addColorStop(0.42, 'rgba(255,255,255,0)'); g.addColorStop(0.75, 'rgba(0,0,20,0)'); g.addColorStop(1, 'rgba(0,0,20,0.16)');
  ctx.fillStyle = g; ctx.fill(f.path);
  if (strap) {
    ctx.strokeStyle = rgb(C.edge, .8); ctx.lineWidth = strap + 1.3 / K.s; ctx.stroke(f.path);
    ctx.strokeStyle = rgb(C.grout); ctx.lineWidth = strap; ctx.stroke(f.path);
  }
  ctx.restore();
}
const strapW = t => 4.2 * smoother(seg(t, 3.25, 4.4));

// ── the 8-fold field ──
function drawField(t, K) {
  const wS = strapW(t);
  for (const f of T8) {
    if (t < f.tg || !inView(f, K)) continue;
    const u = seg(t, f.tg, f.tg + 0.45);
    tile(f, K, t, lerp(0.5, 1, backOut(u, 2.4)), 0.3 * Math.pow(1 - u, 2), 0);
  }
  // lines: ink while being drawn, then a white grout strap with dark cut edges
  const inkC = mix(C.ink, C.edge, smoother(seg(t, 3.3, 4.3)));
  ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  let path;
  if (t < 3.92) {
    path = new Path2D();
    for (const s of segs8) { if (t < s.ti) continue; const u = eOut(seg(t, s.ti, s.ti + 0.32)); path.moveTo(s.a[0], s.a[1]); path.lineTo(lerp(s.a[0], s.b[0], u), lerp(s.a[1], s.b[1], u)); }
  } else path = edges8;
  ctx.strokeStyle = rgb(inkC, 0.9); ctx.lineWidth = wS + 2.4 / K.s; ctx.stroke(path);
  if (wS > 0.05) { ctx.strokeStyle = rgb(C.grout); ctx.lineWidth = wS; ctx.stroke(path); }
}

// ── construction: compass circle, diameters, two squares, octagon, lattice ──
const LAT = [];   // tiling edges with a start time
{
  const seen = new Set();
  for (const p of polys8) for (let k = 0; k < p.length; k++) {
    const a = p[k], b = p[(k + 1) % p.length], mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, kk = Math.round(mx) + ',' + Math.round(my);
    if (seen.has(kk)) continue; seen.add(kk); const d = Math.hypot(mx, my); if (d > 420) continue;
    LAT.push({ a, b, ti: 1.95 + 0.75 * d / 300, d });
  }
}
function lineP(a, b, u) { ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(lerp(a[0], b[0], u), lerp(a[1], b[1], u)); ctx.stroke(); }
function drawConstruction(t, K) {
  const fade = 1 - smoother(seg(t, 3.5, 4.5)); if (fade <= 0) return;
  const px = 1 / K.s; ctx.lineCap = 'round';
  ctx.strokeStyle = rgb(C.con, 0.55 * fade); ctx.lineWidth = 1.5 * px;
  for (const e of LAT) { if (t < e.ti) continue; const u = eOut(seg(t, e.ti, e.ti + 0.4)); const m = [(e.a[0] + e.b[0]) / 2, (e.a[1] + e.b[1]) / 2]; lineP(m, e.a, u); lineP(m, e.b, u); }
  ctx.strokeStyle = rgb(C.con, 0.8 * fade); ctx.lineWidth = 2 * px;
  // circle
  const cu = seg(t, 0.5, 1.3), a0 = -2.4, RC = PER / 2, pt = k => [RC * Math.cos(k * Math.PI / 4), RC * Math.sin(k * Math.PI / 4)];
  if (cu > 0) { ctx.beginPath(); ctx.arc(0, 0, RC, a0, a0 + TAU * smoother(cu)); ctx.stroke(); }
  // diameters: eight equal divisions
  for (let k = 0; k < 4; k++) {
    const u = eOut(seg(t, 1.2 + 0.07 * k, 1.55 + 0.07 * k)); if (u <= 0) continue;
    const a = k * Math.PI / 4, L = RC * 1.18, e = [Math.cos(a) * L, Math.sin(a) * L];
    lineP([0, 0], e, u); lineP([0, 0], [-e[0], -e[1]], u);
  }
  // two squares (the eight-point star), then every third point joined: the lines the pattern follows
  for (let q = 0; q < 2; q++) for (let k = 0; k < 4; k++) {
    const u = eOut(seg(t, 1.45 + 0.14 * q + 0.04 * k, 1.75 + 0.14 * q + 0.04 * k)); if (u <= 0) continue;
    lineP(pt(q + 2 * k), pt(q + 2 * k + 2), u);
  }
  ctx.strokeStyle = rgb(C.con, 0.95 * fade); ctx.lineWidth = 2.6 * px;
  for (let k = 0; k < 8; k++) {
    const u = eOut(seg(t, 1.75 + 0.045 * k, 2.1 + 0.045 * k)); if (u <= 0) continue;
    const a = pt(k), b = pt(k + 3), e = [lerp(a[0], b[0], -0.12), lerp(a[1], b[1], -0.12)], f = [lerp(a[0], b[0], 1.12), lerp(a[1], b[1], 1.12)];
    lineP(e, f, u);
  }
  // compass pricks
  ctx.fillStyle = rgb(C.con, 0.9 * fade);
  const dotA = seg(t, 0.5, 0.6); if (dotA > 0) { ctx.beginPath(); ctx.arc(0, 0, 3.2 * px * dotA, 0, TAU); ctx.fill(); }
  for (let k = 0; k < 8; k++) { const u = seg(t, 1.25 + 0.04 * k, 1.35 + 0.04 * k); if (u <= 0) continue; const a = k * Math.PI / 4; ctx.beginPath(); ctx.arc(PER / 2 * Math.cos(a), PER / 2 * Math.sin(a), 3.4 * px * backOut(u), 0, TAU); ctx.fill(); }
}
function drawCompass(t, K) {
  const inU = eOut(seg(t, 0.05, 0.5)), outU = eIn(seg(t, 1.3, 1.75)); if (outU >= 1) return;
  const cu = smoother(seg(t, 0.5, 1.3)), ang = -2.4 + TAU * cu, px = 1 / K.s;
  const RC = PER / 2, tip = [RC * Math.cos(ang), RC * Math.sin(ang)], mid = [tip[0] / 2, tip[1] / 2];
  const L = RC * 1.02, h = Math.sqrt(L * L - RC * RC / 4), nrm = [-Math.sin(ang), Math.cos(ang)];
  const off = [(1 - inU) * 160 + outU * 190, -(1 - inU) * 120 - outU * 160];
  const Hn = [mid[0] - nrm[0] * h, mid[1] - nrm[1] * h];
  const needle = [0, 0];
  ctx.save(); ctx.translate(off[0], off[1]); ctx.globalAlpha = inU * (1 - outU);
  const draw = (sh) => {
    const dx = sh ? 7 * px : 0, dy = sh ? 11 * px : 0;
    ctx.save(); ctx.translate(dx, dy); ctx.lineCap = 'round';
    const leg = (a, b, w0, w1, col) => { const dir = [b[0] - a[0], b[1] - a[1]], l = Math.hypot(...dir), n = [-dir[1] / l, dir[0] / l];
      ctx.beginPath(); ctx.moveTo(a[0] + n[0] * w0, a[1] + n[1] * w0); ctx.lineTo(b[0] + n[0] * w1, b[1] + n[1] * w1); ctx.lineTo(b[0] - n[0] * w1, b[1] - n[1] * w1); ctx.lineTo(a[0] - n[0] * w0, a[1] - n[1] * w0); ctx.closePath(); ctx.fillStyle = col; ctx.fill(); };
    const brass = sh ? 'rgba(60,40,20,0.22)' : '#b58d45', dark = sh ? 'rgba(60,40,20,0)' : '#6e5226';
    const hub = [Hn[0] - nrm[0] * 6, Hn[1] - nrm[1] * 6];
    leg(Hn, needle, 3.4, 0.9, brass); leg(Hn, tip, 3.4, 1.6, brass);
    if (!sh) { leg([lerp(Hn[0], tip[0], .78), lerp(Hn[1], tip[1], .78)], tip, 1.7, 0.6, '#3a3634'); leg([lerp(Hn[0], needle[0], .86), lerp(Hn[1], needle[1], .86)], needle, 1.0, 0.25, '#555'); }
    ctx.fillStyle = brass; ctx.beginPath(); ctx.arc(Hn[0], Hn[1], 5.2, 0, TAU); ctx.fill();
    leg(Hn, hub, 1.6, 1.3, brass); ctx.beginPath(); ctx.arc(hub[0], hub[1], 2.6, 0, TAU); ctx.fill();
    if (!sh) { ctx.strokeStyle = dark; ctx.lineWidth = 0.5; ctx.beginPath(); ctx.arc(Hn[0], Hn[1], 5.2, 0, TAU); ctx.stroke();
      ctx.fillStyle = '#e8cf8e'; ctx.beginPath(); ctx.arc(Hn[0] - 1.4, Hn[1] - 1.6, 1.8, 0, TAU); ctx.fill(); }
    ctx.restore();
  };
  draw(true); draw(false);
  ctx.restore();
}

// ── arch frame: voussoirs, spandrels, alfiz ──
function drawFrame(t, K) {
  // panel shadow on the wall
  ctx.save(); ctx.shadowColor = 'rgba(50,30,10,0.35)'; ctx.shadowBlur = 30 * K.s; ctx.shadowOffsetX = 8 * K.s; ctx.shadowOffsetY = 12 * K.s;
  ctx.fillStyle = rgb(C.och); ctx.fill(polyPath(ALFO)); ctx.restore();
  // alfiz band: ochre with a chain of white lozenges and cobalt dots
  const band = polyPath(ALFO); polyPath(ALFI, band);
  ctx.fillStyle = rgb(C.och); ctx.fill(band, 'evenodd');
  ctx.save(); ctx.clip(band, 'evenodd');
  const ring = [[-ALF.x - ALF.w / 2, ALF.top - ALF.w / 2], [ALF.x + ALF.w / 2, ALF.top - ALF.w / 2], [ALF.x + ALF.w / 2, ALF.bot + ALF.w / 2], [-ALF.x - ALF.w / 2, ALF.bot + ALF.w / 2]];
  for (let e = 0; e < 4; e++) {
    const a = ring[e], b = ring[(e + 1) % 4], L = Math.hypot(b[0] - a[0], b[1] - a[1]), n = Math.round(L / 26), ux = (b[0] - a[0]) / L, uy = (b[1] - a[1]) / L;
    for (let i = 0; i < n; i++) {
      const x = a[0] + ux * (i + .5) * L / n, y = a[1] + uy * (i + .5) * L / n, r = 9;
      ctx.fillStyle = rgb(C.wht); ctx.beginPath(); ctx.moveTo(x - r, y); ctx.lineTo(x, y - r); ctx.lineTo(x + r, y); ctx.lineTo(x, y + r); ctx.closePath(); ctx.fill();
      ctx.fillStyle = rgb(C.cob); ctx.beginPath(); ctx.arc(x, y, 3.2, 0, TAU); ctx.fill();
    }
  }
  ctx.restore();
  ctx.strokeStyle = rgb(C.edge, .7); ctx.lineWidth = 1.2; ctx.stroke(polyPath(ALFO)); ctx.stroke(polyPath(ALFI));
  // spandrels: cobalt with small white eight-point stars
  const spd = polyPath(ALFI); polyPath(BANDO, spd);
  ctx.fillStyle = rgb(C.cobD); ctx.fill(spd, 'evenodd');
  ctx.save(); ctx.clip(spd, 'evenodd');
  const SP = 44;
  for (let gx = -8; gx <= 8; gx++) for (let gy = -12; gy <= 9; gy++) {
    const x = gx * SP, y = gy * SP + 12, r = 11;
    ctx.fillStyle = rgb(C.wht, 0.92); ctx.beginPath();
    for (let k = 0; k < 16; k++) { const a = k * TAU / 16 + Math.PI / 8, rr = k % 2 ? r * 0.62 : r; k ? ctx.lineTo(x + rr * Math.cos(a), y + rr * Math.sin(a)) : ctx.moveTo(x + rr * Math.cos(a), y + rr * Math.sin(a)); }
    ctx.closePath(); ctx.fill();
    ctx.fillStyle = rgb(C.och); ctx.beginPath(); ctx.arc(x, y, 3, 0, TAU); ctx.fill();
    const x2 = x + SP / 2, y2 = y + SP / 2; ctx.fillStyle = rgb(C.tur); ctx.beginPath(); ctx.moveTo(x2 - 5, y2); ctx.lineTo(x2, y2 - 5); ctx.lineTo(x2 + 5, y2); ctx.lineTo(x2, y2 + 5); ctx.closePath(); ctx.fill();
  }
  ctx.restore();
  // voussoir band: alternating ochre and white wedges round the pointed arch, blocks down the jambs
  const vb = polyPath(BANDO); polyPath(OPEN, vb);
  ctx.save(); ctx.clip(vb, 'evenodd');
  ctx.fillStyle = rgb(C.wht); ctx.fillRect(-400, -700, 800, 1200);
  const r0 = ARCH.r, be = Math.atan2(Math.sqrt(r0 * r0 - ARCH.c * ARCH.c), ARCH.c), NV = 9;
  for (const sd of [-1, 1]) {
    for (let i = 0; i < NV; i++) {
      if (i % 2) continue;
      const th0 = Math.PI + be * i / NV, th1 = Math.PI + be * (i + 1) / NV + (i === NV - 1 ? 0.25 : 0);
      const P = (th, r) => [ARCH.c + r * Math.cos(th), ARCH.ys + r * Math.sin(th)];
      const q = [P(th0, r0 - 5), P(th0, r0 + ARCH.band + 30), P(th1, r0 + ARCH.band + 30), P(th1, r0 - 5)];
      ctx.beginPath(); q.forEach((p, k) => { const x = sd < 0 ? p[0] : -p[0]; k ? ctx.lineTo(x, p[1]) : ctx.moveTo(x, p[1]); }); ctx.closePath();
      ctx.fillStyle = rgb(C.och); ctx.fill();
    }
    for (let y = ARCH.ys, i = 0; y < ARCH.bot; y += 48, i++) if (i % 2 === 0) { ctx.fillStyle = rgb(C.och); ctx.fillRect(sd > 0 ? ARCH.a - 2 : -ARCH.a - ARCH.band - 2, y, ARCH.band + 4, 48); }
  }
  // glaze gloss on the band
  const gg = ctx.createLinearGradient(-300, -500, 300, 400); gg.addColorStop(0, 'rgba(255,255,250,0.18)'); gg.addColorStop(1, 'rgba(0,0,30,0.1)'); ctx.fillStyle = gg; ctx.fillRect(-400, -700, 800, 1200);
  ctx.restore();
  ctx.strokeStyle = rgb(C.cob); ctx.lineWidth = 3; ctx.stroke(polyPath(BANDO)); ctx.stroke(OPENP);
  ctx.strokeStyle = rgb(C.edge, .6); ctx.lineWidth = 1; ctx.stroke(polyPath(archPts(ARCH.band + 1.5))); ctx.stroke(polyPath(archPts(-1.5)));
}

// ── medallion: the 8-fold rosette turns into a 10-fold one ──
const MT0 = 6.95;
function drawMedallionContents(t, K) {
  const t0 = MT0, rot = (Math.PI / 4) * smoother(seg(t, t0, 8.5));
  const wS = strapW(t);
  ctx.fillStyle = rgb(C.cobD); ctx.beginPath(); ctx.arc(0, 0, RM, 0, TAU); ctx.fill();
  ctx.save(); ctx.rotate(rot);
  for (const f of T8) {
    if (f.d > RM + 60) continue;
    const ts = t0 + 0.55 * f.d / RM, k = 1 - smoother(seg(t, ts, ts + 0.45)); if (k <= 0.01) continue;
    tile(f, K, t, k, 0, wS);
  }
  ctx.restore();
  ctx.save(); ctx.rotate(rot - Math.PI / 4);
  for (const f of T10) {
    const ts = t0 + 0.3 + 0.55 * f.d / RM, u = seg(t, ts, ts + 0.55); if (u <= 0) continue;
    tile(f, K, t, lerp(0.2, 1, backOut(u, 2.2)), 0.55 * Math.pow(1 - u, 2), wS);
  }
  ctx.restore();
}
function drawRing(t, K) {
  const u = smoother(seg(t, 6.45, 6.95)); if (u <= 0) return;
  const a0 = -Math.PI / 2;
  ctx.lineCap = 'butt';
  ctx.strokeStyle = rgb(C.edge, .7); ctx.lineWidth = 13; ctx.beginPath(); ctx.arc(0, 0, RM + 4, a0, a0 + TAU * u); ctx.stroke();
  ctx.strokeStyle = rgb(C.och); ctx.lineWidth = 11; ctx.beginPath(); ctx.arc(0, 0, RM + 4, a0, a0 + TAU * u); ctx.stroke();
  ctx.strokeStyle = rgb(C.wht); ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(0, 0, RM + 4, a0, a0 + TAU * u); ctx.stroke();
  if (u < 1) { const a = a0 + TAU * u; ctx.fillStyle = 'rgba(255,248,220,0.9)'; ctx.beginPath(); ctx.arc((RM + 4) * Math.cos(a), (RM + 4) * Math.sin(a), 5, 0, TAU); ctx.fill(); }
}

// ── captions ──
function drawText(t) {
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  const X = 140;
  const letters = (str, x, y, font, col, t0, st, sp) => {
    ctx.font = font; ctx.letterSpacing = sp || '0px'; let cx = x;
    for (let i = 0; i < str.length; i++) {
      const ch = str[i], w = ctx.measureText(ch).width, u = eOut(seg(t, t0 + i * st, t0 + i * st + 0.5));
      if (u > 0) { ctx.fillStyle = rgb(col, u); ctx.fillText(ch, cx, y + 26 * (1 - u)); }
      cx += w;
    }
    ctx.letterSpacing = '0px';
  };
  letters('COMPASS · STRAIGHTEDGE · CLAY', X, 356, '30px "Marcellus SC"', [146, 96, 28], 5.6, 0.018, '5px');
  letters('The Pattern', X, 492, '124px Marcellus', C.cobD, 5.75, 0.035);
  letters('Without End', X, 626, '124px Marcellus', C.cobD, 5.95, 0.035);
  // divider: a rule with an eight-point star
  const du = eOut(seg(t, 6.3, 6.9));
  if (du > 0) {
    ctx.strokeStyle = rgb([158, 108, 36], du); ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(X, 682); ctx.lineTo(X + 250 * du, 682); ctx.moveTo(X + 310, 682); ctx.lineTo(X + 310 + 250 * du, 682); ctx.stroke();
    const sx = X + 280, sy = 682; ctx.fillStyle = rgb(C.och, du); ctx.save(); ctx.translate(sx, sy); ctx.rotate((1 - du) * 1.5);
    for (let q = 0; q < 2; q++) { ctx.save(); ctx.rotate(q * Math.PI / 4); ctx.fillRect(-10, -10, 20, 20); ctx.restore(); }
    ctx.fillStyle = rgb(C.cob, du); ctx.beginPath(); ctx.arc(0, 0, 4, 0, TAU); ctx.fill(); ctx.restore();
  }
  // subtitle: "Eight" becomes "Ten" as the medallion turns
  ctx.font = '44px Marcellus';
  const su = eOut(seg(t, 6.45, 7.0)), sw = smoother(seg(t, 7.55, 8.0));
  const rest = ' points from a single circle.';
  const col = [78, 62, 52];
  for (const [word, a, dy] of [['Eight', 1 - sw, -30 * sw], ['Ten', sw, 30 * (1 - sw)]]) {
    if (a <= 0) continue;
    const w = ctx.measureText(word).width;
    ctx.fillStyle = rgb(word === 'Ten' ? [168, 104, 26] : col, su * a); ctx.fillText(word, X, 762 + dy + 20 * (1 - su));
    if (word === 'Eight') ctx._w8 = w; else ctx._w10 = w;
  }
  const wx = lerp(ctx.measureText('Eight').width, ctx.measureText('Ten').width, sw);
  ctx.fillStyle = rgb(col, su); ctx.fillText(rest, X + wx, 762 + 20 * (1 - su));
}

// ── frame ──
function frame(t) {
  const K = cam(t);
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.drawImage(PLASTER, 0, 0);
  setCam(K);
  if (t > 4.45) drawFrame(t, K);
  // the panel
  ctx.save(); ctx.clip(OPENP);
  ctx.fillStyle = rgb(C.bis, 0.55); ctx.fill(OPENP);
  drawConstruction(t, K);
  if (t >= 6.45) {   // field outside the medallion stays; inside it turns
    ctx.save(); const hole = new Path2D(OPENP); hole.moveTo(RM, 0); hole.arc(0, 0, RM, 0, TAU, true); ctx.clip(hole, 'evenodd'); drawField(t, K); ctx.restore();
    ctx.save(); const cp = new Path2D(); cp.arc(0, 0, RM, 0, TAU); ctx.clip(cp);
    if (t < MT0) drawField(t, K); else drawMedallionContents(t, K);
    ctx.restore();
  } else drawField(t, K);
  ctx.restore();
  drawRing(t, K);
  drawCompass(t, K);
  // glints as the light passes
  if (t > 8.3 && t < 9.6) {
    for (const f of T8.concat(T10)) {
      if (!f.glint) continue; const sx = f.cx * K.s + K.x, sy = f.cy * K.s + K.y;
      const g = sweepAt(t, sx, sy); if (g < 0.25) continue;
      const inside = true;
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = `rgba(255,252,235,${0.8 * g})`;
      const r = 14 * g; ctx.beginPath(); ctx.moveTo(sx - r, sy); ctx.lineTo(sx, sy - 2); ctx.lineTo(sx + r, sy); ctx.lineTo(sx, sy + 2); ctx.closePath(); ctx.fill();
      ctx.beginPath(); ctx.moveTo(sx, sy - r); ctx.lineTo(sx + 2, sy); ctx.lineTo(sx, sy + r); ctx.lineTo(sx - 2, sy); ctx.closePath(); ctx.fill();
      setCam(K);
    }
  }
  if (t > 5.5) drawText(t);
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  const fin = seg(t, 0, 0.35), fo = smoother(seg(t, 9.35, 10));
  const blk = Math.max(1 - fin, fo);
  if (blk > 0) { ctx.fillStyle = `rgba(14,10,8,${blk})`; ctx.fillRect(0, 0, W, H); }
}
window.draw = ({ t }) => { frame(t); return cv.toDataURL('image/jpeg', 0.92).split(',')[1]; };
window.ready = document.fonts.load('124px Marcellus').then(() => document.fonts.load('30px "Marcellus SC"')).then(() => document.fonts.ready);
window.events = () => {
  const ev = [];
  ev.push({ k: 'compass', t: 0.5, d: 0.8 });
  for (let k = 0; k < 4; k++) ev.push({ k: 'line', t: 1.2 + 0.07 * k, v: 0 });
  for (let q = 0; q < 2; q++) for (let k = 0; k < 4; k++) ev.push({ k: 'line', t: 1.5 + 0.2 * q + 0.05 * k, v: 1 });
  const bins = new Map(), add = (k, tt) => { const b = Math.round(tt * 60); const kk = k + b; bins.set(kk, { k, t: b / 60, v: (bins.get(kk)?.v || 0) + 1 }); };
  for (const s of segs8) if (Math.hypot(s.a[0], s.a[1]) < 300) add('ink', s.ti);
  const K0 = cam(3.5);
  for (const f of T8) { const K = cam(f.tg); if (f.tg < 6.3 && Math.abs(f.cx * K.s + K.x - 960) < 1000 && Math.abs(f.cy * K.s + K.y - 540) < 560) add('tile', f.tg + 0.12); }
  for (const f of T10) add('tile', MT0 + 0.3 + 0.55 * f.d / RM + 0.2);
  ev.push(...bins.values());
  ev.push({ k: 'whoosh', t: 4.2, d: 2.3 }, { k: 'ring', t: 6.45, d: 0.5 }, { k: 'spin', t: 6.9, d: 1.5 }, { k: 'phrase', t: 5.7, v: 0 }, { k: 'shimmer', t: 8.35, d: 1.1 }, { k: 'chord', t: 8.45 });
  return ev;
};
