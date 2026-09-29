// scene.js · "How the Harvest Came": a papyrus unrolls into three registers, one per Egyptian season.
// I · The Flood (the river rises, the sun comes up, ducks lift off the papyrus; the water falls back and leaves black silt)
// II · The Growing (a plough team and a sower walk in procession; shoots come up behind them)
// III · The Harvest (reapers with sickles, bearers carry baskets to the granary heap). Deterministic in t.
const cv = document.getElementById('c'), MAIN = cv.getContext('2d');
const DUR = 10.0, STEP = 12, stp = t => Math.floor(t * STEP + 1e-4) / STEP;
const PAINT = mk(1920, 1080), PX = PAINT.getContext('2d');
const FONT = "'Marcellus SC'";

// ── layout ──
const BOX = { x0: 100, y0: 66, x1: 1820, y1: 1016, b: 18 };
const IN = { x0: 118, x1: 1802 };
const REG = [{ y0: 222, y1: 476 }, { y0: 484, y1: 738 }, { y0: 746, y1: 998 }];
const PANEL_X1 = 262, SCN_X0 = 268;
// ── timeline ──
const T = {
  open: [0.15, 1.05], title: [0.85, 1.75],
  roll: [[1.35, 2.3], [2.6, 3.55], [3.85, 4.8]],
  sun: [1.75, 3.7], flood: [2.05, 3.2], recede: [3.55, 4.45], ducks: [2.55, 4.5],
  team: [2.8, 8.9], reap: [4.0, 9.4], bear: [4.1, 7.5], tip: [7.55, 8.25],
  cap2: 4.6, cap3: 8.45, end: [8.25, 9.0], fade: [9.3, 10.0],
};

// ── static paint: block border, register dividers, panel frames (baked once) ──
let STATIC;
function bakeStatic() {
  STATIC = mk(1920, 1080); X = STATIC.getContext('2d');
  const { x0, y0, x1, y1, b } = BOX, cols = [COL.blue, COL.red, COL.green, COL.ochre];
  const run = (ax, ay, len, horiz, k0) => {
    let p = 0, k = k0;
    while (p < len) {
      const L = Math.min(34, len - p);
      X.fillStyle = cols[k % 4]; horiz ? X.fillRect(ax + p, ay, L, b) : X.fillRect(ax, ay + p, b, L);
      X.fillStyle = COL.white; horiz ? X.fillRect(ax + p + L - 5, ay, 5, b) : X.fillRect(ax, ay + p + L - 5, b, 5);
      X.fillStyle = COL.ink; horiz ? X.fillRect(ax + p + L - 6, ay, 1.6, b) : X.fillRect(ax, ay + p + L - 6, b, 1.6);
      p += L; k++;
    }
  };
  run(x0, y0, x1 - x0, true, 0); run(x0, y1 - b, x1 - x0, true, 2); run(x0, y0 + b, y1 - y0 - 2 * b, false, 1); run(x1 - b, y0 + b, y1 - y0 - 2 * b, false, 3);
  X.strokeStyle = COL.ink; X.lineWidth = 2.4; X.strokeRect(x0, y0, x1 - x0, y1 - y0); X.strokeRect(x0 + b, y0 + b, x1 - x0 - 2 * b, y1 - y0 - 2 * b);
  // register dividers: black / red / black
  const div = y => { X.fillStyle = COL.ink; X.fillRect(IN.x0, y, IN.x1 - IN.x0, 2.2); X.fillStyle = COL.red; X.fillRect(IN.x0, y + 2.2, IN.x1 - IN.x0, 3.6); X.fillStyle = COL.ink; X.fillRect(IN.x0, y + 5.8, IN.x1 - IN.x0, 2.2); };
  div(214); div(476); div(738);
  X = PX;
}

// ── roll: a rolled-up strip of papyrus (cylinder) ──
function drawRoll(ctx, x, y0, y1, w) {
  const g = ctx.createLinearGradient(x - w / 2, 0, x + w / 2, 0);
  g.addColorStop(0, '#7d5a2c'); g.addColorStop(0.28, '#e3cc98'); g.addColorStop(0.45, '#f4e4bb'); g.addColorStop(0.8, '#b48c52'); g.addColorStop(1, '#6b4a22');
  ctx.save();
  ctx.fillStyle = 'rgba(30,18,6,0.28)'; ctx.fillRect(x + w / 2, y0 + 4, 16, y1 - y0);   // cast shadow
  ctx.fillStyle = g; ctx.fillRect(x - w / 2, y0, w, y1 - y0);
  ctx.globalCompositeOperation = 'multiply'; ctx.drawImage(FIB, x - w / 2, y0, w, y1 - y0, x - w / 2, y0, w, y1 - y0); ctx.globalCompositeOperation = 'source-over';
  for (const yy of [y0, y1]) {   // spiral ends
    ctx.beginPath(); ctx.ellipse(x, yy, w / 2, w * 0.16, 0, 0, TAU); ctx.fillStyle = '#d9bf88'; ctx.fill(); ctx.strokeStyle = 'rgba(70,45,15,0.8)'; ctx.lineWidth = 1.2; ctx.stroke();
    for (let k = 1; k < 4; k++) { ctx.beginPath(); ctx.ellipse(x + k * 0.8, yy, w / 2 * (1 - k * 0.22), w * 0.16 * (1 - k * 0.22), 0, 0, TAU); ctx.stroke(); }
  }
  ctx.strokeStyle = 'rgba(60,38,12,0.7)'; ctx.lineWidth = 1.2; ctx.strokeRect(x - w / 2, y0, w, y1 - y0);
  ctx.restore();
}
function rollX(t, i) {
  const [a, b] = T.roll[i], u = eInOut(seg(t, a, b));
  return IN.x0 + 16 + (IN.x1 + 40 - IN.x0) * u - 10 * Math.sin(Math.PI * seg(t, a - 0.28, a + 0.04));
}

// ── text helpers ──
function txt(s, x, y, size, col, a = 1, align = 'center', ls = 0.04) {
  X.save(); X.globalAlpha *= a; X.font = `${size}px ${FONT}`; X.fillStyle = col; X.textAlign = align; X.textBaseline = 'alphabetic';
  if ('letterSpacing' in X) X.letterSpacing = `${(ls * size).toFixed(1)}px`;
  X.fillText(s, x, y); X.restore();
}
function fitSize(s, size, maxW) { X.font = `${size}px ${FONT}`; const w = X.measureText(s).width * (1 + 0.04); return w > maxW ? size * maxW / w : size; }
function staggerText(s, x, y, size, col, t, t0, per, align = 'center') {   // letters rise in one by one with a slight overshoot
  X.save(); X.font = `${size}px ${FONT}`; const sp = size * 0.06; if ('letterSpacing' in X) X.letterSpacing = '0px';
  const ws = [...s].map(ch => X.measureText(ch).width + sp), W = ws.reduce((a, b) => a + b, 0) - sp;
  let cx = align === 'center' ? x - W / 2 : x;
  [...s].forEach((ch, i) => {
    const u = seg(t, t0 + i * per, t0 + i * per + 0.32);
    if (u > 0 && ch !== ' ') { X.globalAlpha = clamp(u * 2.5); X.fillStyle = col; X.textAlign = 'left';
      X.save(); X.translate(cx + ws[i] / 2, y); const sc = 0.6 + 0.4 * eBack(u); X.scale(sc, sc); X.fillText(ch, -ws[i] / 2 + sp / 2, (1 - eOut(u)) * size * 0.35); X.restore(); }
    cx += ws[i];
  });
  X.restore();
}
function speech(x, y, lines, a) {   // workers' remarks, as tomb captions: short lines between thin red column rules
  if (a <= 0) return;
  X.save(); X.globalAlpha = a; X.font = `21px ${FONT}`;
  const w = Math.max(...lines.map(l => X.measureText(l).width)) + 24, h = lines.length * 25 + 10;
  const yy = y + (1 - eOut(a)) * 8;
  X.fillStyle = COL.red; X.fillRect(x - w / 2, yy - h, 2.5, h); X.fillRect(x + w / 2 - 2.5, yy - h, 2.5, h);
  lines.forEach((l, i) => txt(l, x, yy - h + 27 + i * 25, 21, COL.ink, 1, 'center', 0.03));
  X.restore();
}

// ── caption panel at the left of each register ──
const PANELS = [['I', 'THE FLOOD', ['THE RIVER', 'ROSE']], ['II', 'THE GROWING', ['THE SEED', 'WAS SOWN']], ['III', 'THE HARVEST', ['THE GRAIN', 'WAS', 'GATHERED']]];
function panel(i) {
  const r = REG[i], [num, season, lines] = PANELS[i], cx = (IN.x0 + PANEL_X1) / 2;
  X.fillStyle = COL.ink; X.fillRect(PANEL_X1, r.y0, 2.2, r.y1 - r.y0); X.fillStyle = COL.red; X.fillRect(PANEL_X1 + 2.2, r.y0, 3.6, r.y1 - r.y0);
  txt(num, cx, r.y0 + 52, 44, COL.red);
  txt(season, cx, r.y0 + 84, fitSize(season, 19, 126), COL.red);
  X.fillStyle = COL.ink; X.fillRect(cx - 40, r.y0 + 98, 80, 2);
  const n = lines.length, sz = Math.min(...lines.map(l => fitSize(l, 25, 128)));
  lines.forEach((l, k) => txt(l, cx, r.y0 + 142 + k * 31 + (3 - n) * 12, sz, COL.ink));
}

// ══ I · the flood ══
const R1 = { land0: 400, land1: 432, water0: 432, base: 476 };
const PAPY = (() => { const r = mulberry(11), a = []; for (let i = 0; i < 17; i++) a.push({ x: 1360 + i * 25 + r() * 14, h: 118 + r() * 50, lean: (r() - 0.5) * 0.35, ph: r() * TAU }); return a; })();
function reg1(t) {
  const ts = stp(t);
  const fk = eOut(seg(t, ...T.flood)) * (1 - eInOut(seg(t, ...T.recede)));
  const silt = seg(t, T.recede[0] + 0.15, T.recede[1]);
  const wTop = R1.water0 - 96 * fk;
  // sun disc rising behind the land (plain disc)
  const su = eOut(seg(t, ...T.sun)) - 0.28 * eInOut(seg(t, T.end[0] + 0.2, DUR)), sy = lerp(R1.land0 + 60, 300, su), sx = 790;
  X.save(); X.beginPath(); X.rect(SCN_X0, REG[0].y0, 1600, R1.land0 - REG[0].y0); X.clip();
  X.beginPath(); X.arc(sx, sy, 62, 0, TAU); paint(COL.gold, 2.4);
  X.beginPath(); X.arc(sx, sy, 50, 0, TAU); paint(COL.red, 2.4);
  X.restore();
  // land: dry ochre → wet black silt left by the water
  const landCol = silt < 1 ? COL.ochre : COL.silt;
  poly([[SCN_X0, R1.land0], [1330, R1.land0], [1352, R1.land1], [SCN_X0, R1.land1]]); paint(COL.ochre);
  if (silt > 0) { X.save(); X.beginPath(); const sw = lerp(SCN_X0, 1360, eInOut(silt)); X.rect(SCN_X0, R1.land0 - 4, sw - SCN_X0, 40); X.clip();
    poly([[SCN_X0, R1.land0], [1330, R1.land0], [1352, R1.land1], [SCN_X0, R1.land1]]); paint(COL.silt);
    X.strokeStyle = 'rgba(160,190,210,0.55)'; X.lineWidth = 2; for (let k = 0; k < 9; k++) { const gx = 320 + k * 115 + hash(k) * 40; X.beginPath(); X.moveTo(gx, 412 + (k % 3) * 6); X.lineTo(gx + 26, 412 + (k % 3) * 6); X.stroke(); }
    X.restore(); }
  palm(372, R1.land0 + 2, 132, Math.sin(ts * 1.6) * 2.5);
  palm(1215, R1.land0 + 2, 118, Math.sin(ts * 1.6 + 1) * 2.5);
  // papyrus thicket
  for (const p of PAPY) papyrusPlant(p.x, 440, p.h, p.lean, Math.sin(ts * 2.1 + p.ph) * 3);
  // the Nile: flat blue with zig-zag water lines, flowing
  X.beginPath(); X.rect(SCN_X0, wTop, IN.x1 - SCN_X0, R1.base - wTop); paint(COL.blue, 0);
  X.save(); X.beginPath(); X.rect(SCN_X0, wTop, IN.x1 - SCN_X0, R1.base - wTop); X.clip();
  const fl = (ts * 34) % 28;
  X.strokeStyle = COL.ink; X.lineWidth = 2; X.lineJoin = 'miter';
  for (let y = R1.base - 9, row = 0; y > wTop + 4; y -= 15, row++) {
    X.beginPath(); const off = fl + (row % 2) * 14;
    for (let x = SCN_X0 - 28 + off, k = 0; x < IN.x1 + 28; x += 14, k++) X.lineTo(x, y + (k % 2 ? -4.5 : 4.5));
    X.stroke();
  }
  for (const [fx, fy, dx, s] of [[520, 458, 1, 1.25], [980, 452, -1, 1.1], [1500, 460, 1, 1.2]]) fish(fx + dx * ts * 24, fy - 30 * fk, s, dx, ts * 9);
  X.restore();
  line([SCN_X0, wTop], [IN.x1, wTop], 2.4);
  // ducks lift off the thicket as the water comes up, and cross the register
  const dt = seg(t, ...T.ducks);
  if (dt > 0 && dt < 1) for (let k = 0; k < 3; k++) {
    const u = clamp(dt * 1.25 - k * 0.1), e = eIn(Math.min(u, 0.25) / 0.25) * 0.25 + Math.max(0, u - 0.25);
    const x = lerp(1500 + k * 70, 150, e), y = lerp(300 + k * 14, 262 + k * 30, eOut(u)) - Math.sin(u * 8 + k) * 6;
    duck(x, y, 2.3, Math.cos(ts * 22 + k * 2.1), -1);
  }
}

// ══ II · the growing ══
const G2 = 712, H2 = 178, U2 = H2 / 19, S2 = 6, OXS = 8.2;
const teamX = t => 820 + 84 * clamp(stp(t) - T.team[0], 0, T.team[1] - T.team[0]);
const shareX = t => teamX(t) - 232;
function sownAt(x) { const x0 = shareX(0); if (x < x0) return -10; return T.team[0] + (x - x0) / 84; }
function reg2(t) {
  const ts = stp(t), xT = teamX(t), d = xT - 820;
  // soil, furrows behind the plough, shoots coming up
  X.beginPath(); X.rect(SCN_X0, G2, IN.x1 - SCN_X0, REG[1].y1 - G2); paint(COL.silt, 0); line([SCN_X0, G2], [IN.x1, G2], 2.4);
  const sx = shareX(t);
  X.strokeStyle = 'rgba(0,0,0,0.55)'; X.lineWidth = 1.6;
  for (let k = 0; k < 3; k++) { X.beginPath(); for (let x = SCN_X0; x < sx; x += 20) { X.moveTo(x, G2 + 7 + k * 7); X.lineTo(x + 12, G2 + 5 + k * 7); } X.stroke(); }
  for (let x = SCN_X0 + 8, i = 0; x < 1800; x += 17, i++) {
    const g = eOut(seg(ts, sownAt(x) + 0.35, sownAt(x) + 1.4)); if (g <= 0) continue;
    const h = (18 + hash(i) * 14) * g, xx = x + (hash(i + 3) - 0.5) * 6;
    X.strokeStyle = COL.greenD; X.lineWidth = 2.6; X.lineCap = 'round';
    X.beginPath(); X.moveTo(xx, G2); X.quadraticCurveTo(xx - 2, G2 - h * 0.6, xx - 6 * g, G2 - h); X.stroke();
    X.beginPath(); X.moveTo(xx + 1, G2); X.quadraticCurveTo(xx + 3, G2 - h * 0.5, xx + 7 * g, G2 - h * 0.8); X.strokeStyle = COL.green; X.stroke();
  }
  // shade tree with a water jar, at the end of the field
  const tx = 1700;
  X.beginPath(); X.moveTo(tx - 10, G2); X.lineTo(tx - 7, G2 - 120); X.lineTo(tx + 7, G2 - 120); X.lineTo(tx + 10, G2); X.closePath(); paint(COL.brown);
  smooth([[tx - 80, G2 - 130], [tx - 70, G2 - 196], [tx - 20, G2 - 222], [tx + 40, G2 - 218], [tx + 82, G2 - 180], [tx + 78, G2 - 128], [tx + 20, G2 - 108], [tx - 40, G2 - 110]]); paint(COL.green);
  X.fillStyle = COL.greenD; for (let k = 0; k < 26; k++) { X.beginPath(); X.ellipse(tx - 62 + hash(k) * 128, G2 - 200 + hash(k + 40) * 82, 5, 8, hash(k + 7) * 3, 0, TAU); X.fill(); }
  X.fillStyle = COL.red; for (let k = 0; k < 7; k++) { X.beginPath(); X.arc(tx - 50 + hash(k + 90) * 100, G2 - 190 + hash(k + 60) * 60, 4, 0, TAU); X.fill(); }
  X.beginPath(); X.moveTo(tx - 48, G2); X.lineTo(tx - 44, G2 - 10); X.lineTo(tx - 24, G2 - 10); X.lineTo(tx - 20, G2); paint(COL.brown, 2);
  smooth([[tx - 44, G2 - 10], [tx - 50, G2 - 40], [tx - 42, G2 - 64], [tx - 26, G2 - 64], [tx - 18, G2 - 40], [tx - 24, G2 - 10]]); paint(COL.red, 2.2);
  line([tx - 44, G2 - 58], [tx - 24, G2 - 58], 2);
  // plough team: two oxen, the ard, the ploughman
  const oph = d / (3.2 * OXS / 0.6) ;
  ox({ x: xT + 44, y: G2 - 5, s: OXS, col: '#8e4a2a', ph: oph + 0.25, headDip: 0.05 });
  const px = xT - 300, pph = d * 0.6 / (S2 * U2);
  const yoke = [xT + 6.6 * OXS + 12, G2 - 12.6 * OXS];
  const share = [sx, G2 + 3], heel = [sx - 26, G2 - 4];
  const hF = [px + 4.4 * U2, G2 - 9.2 * U2], hB = [px + 3.6 * U2, G2 - 9.0 * U2];
  X.lineCap = 'round';
  X.strokeStyle = COL.ink; X.lineWidth = 9; X.beginPath(); X.moveTo(heel[0], heel[1]); X.lineTo(yoke[0], yoke[1]); X.stroke();
  X.strokeStyle = COL.brown; X.lineWidth = 5.5; X.stroke();
  for (const h of [hB, hF]) { X.beginPath(); X.moveTo(share[0], share[1]); X.lineTo(h[0] + 6, h[1]); X.strokeStyle = COL.ink; X.lineWidth = 8; X.stroke(); X.strokeStyle = COL.brown; X.lineWidth = 4.5; X.stroke(); }
  poly([[heel[0], heel[1]], [share[0] + 18, share[1]], [share[0], share[1] - 12]]); paint(COL.ochreD, 2);
  ox({ x: xT, y: G2, s: OXS, col: COL.white, patches: true, ph: oph, headDip: 0 });
  X.save(); X.translate(yoke[0], yoke[1]); X.rotate(-0.05); poly([[-40, -4], [80, -4], [82, 5], [-40, 5]]); paint(COL.ochreD, 2.2); X.restore();
  const wf = walkFeet(pph, S2);
  human({ x: px, y: G2, H: H2, lean: 0.28, bob: -Math.abs(Math.sin(pph * TAU)) * 0.25, fB: wf.B, fF: wf.F,
    hB: [4.4 - 0.8, -9.0], hF: [4.4, -9.2], fistB: true, fistF: true, eB: 1, eF: 1 });
  // the sower walks ahead, casting seed from a bag
  const wx = xT + 250, wph = d * 0.6 / (S2 * U2) + 0.3, wfs = walkFeet(wph, S2);
  const cyc = ((wph * 1) % 1 + 1) % 1, throwA = Math.sin(cyc * TAU);
  const hand = [lerp(-1.5, 5.2, (throwA + 1) / 2), lerp(-8, -14.5, (throwA + 1) / 2)];
  human({ x: wx, y: G2, H: H2, lean: 0.06, bob: -Math.abs(Math.sin(wph * TAU)) * 0.25, fB: wfs.B, fF: wfs.F, hB: [-1.6, -8.6], hF: hand, fistB: true, eB: -1, eF: 1,
    propB: (w, a) => { X.save(); X.translate(w[0], w[1] + 1.8); smooth([[-1.4, -1.2], [1.4, -1.2], [1.9, 1.4], [0, 2.4], [-1.9, 1.4]]); paint(COL.white, LW * 0.9); X.restore(); } });
  // seeds: each cast (one per stride) throws a small spray that falls ahead
  for (let k = -2; k < 60; k++) {
    const cast = T.team[0] + (k + 0.1 - 0.3) * (S2 * U2) / (0.6 * 84); const el = ts - cast;
    if (el < 0 || el > 0.55) continue;
    const ox0 = teamX(cast) + 250 + 4.5 * U2, oy0 = G2 - 14 * U2;
    for (let s = 0; s < 7; s++) { const vx = 90 + hash(k * 13 + s) * 160, vy = -60 - hash(k * 7 + s) * 90;
      const x = ox0 + vx * el, y = Math.min(G2 - 2, oy0 + vy * el + 900 * el * el);
      X.beginPath(); X.ellipse(x, y, 2.6, 1.8, 0.5, 0, TAU); X.fillStyle = COL.ochre; X.fill(); X.strokeStyle = COL.ink; X.lineWidth = 0.8; X.stroke(); }
  }
  speech(px + 200, G2 - 150, ['PULL STEADY,', 'MY BEAUTIES.'], seg(t, T.cap2, T.cap2 + 0.35));
}

// ══ III · the harvest ══
const G3 = 972, H3 = 160, U3 = H3 / 19;
const WHEAT = (() => { const r = mulberry(33), a = []; for (let x = 280; x < 905; x += 7 + r() * 4) a.push({ x, h: 136 + r() * 34, lean: (r() - 0.5) * 0.1, ph: r() * TAU }); return a; })();
const CHOP = 0.8; let POUR = [0, 0];
function reaperX(t, i) { const x0 = [440, 690][i], n = Math.max(0, (stp(t) - T.reap[0] - i * 0.3) / CHOP); return x0 + 17 * (Math.floor(n) + eInOut(clamp((n % 1 - 0.75) / 0.25))); }
function reg3(t) {
  const ts = stp(t);
  X.beginPath(); X.rect(SCN_X0, G3, IN.x1 - SCN_X0, REG[2].y1 - G3); paint('#7a5530', 0); line([SCN_X0, G3], [IN.x1, G3], 2.4);
  const ra = [reaperX(t, 0), reaperX(t, 1)];
  for (const w of WHEAT) {
    const who = w.x < 640 ? 0 : 1, cut = w.x < ra[who] + 30 && w.x > [300, 640][who] - 999 * 0;
    wheatStalk(w.x, G3, w.h, w.lean + Math.sin(ts * 2 + w.ph) * 0.02, cut && w.x > (who ? 640 : 282) - 1 ? true : false);
  }
  // sheaves left behind the reapers
  for (let i = 0; i < 2; i++) { const x0 = [296, 650][i]; for (let x = x0 + 14; x < ra[i] - 50; x += 62) sheaf(x, G3); }
  for (let i = 0; i < 2; i++) {
    const n = Math.max(0, (ts - T.reap[0] - i * 0.3) / CHOP), q = n % 1;
    const up = q < 0.45 ? eOut(q / 0.45) : q < 0.62 ? 1 - eIn((q - 0.45) / 0.17) : 0;
    human({ x: ra[i], y: G3, H: H3, lean: 0.3, fB: [-2.4, 0], fF: [2.8, 0], hipX: -0.3,
      hB: [5.9, -12.8], hF: [lerp(8.1, 7.7, up), lerp(-11.0, -14.8, up)], fistB: true, fistF: true, eB: 1, eF: 1,
      propF: (w, a) => sickle(w, a, lerp(0.15, -0.55, up)) });
  }
  // bearers walk to the granary heap
  const b1 = { x0: 1070, x1: 1440 }, b2 = { x0: 820, x1: 1180 };
  const walk = (b, t0, t1) => b.x0 + (b.x1 - b.x0) * clamp((ts - t0) / (t1 - t0));
  const x1 = walk(b1, T.bear[0], T.bear[1]), x2 = walk(b2, T.bear[0], T.bear[1] + 0.8);
  const tip = eInOut(seg(t, ...T.tip)), tipBack = eInOut(seg(t, T.tip[1] + 0.25, T.tip[1] + 0.8));
  const hk = eOut(seg(t, T.tip[0] + 0.25, T.tip[1] + 0.1)) + 0.06 * Math.sin(Math.PI * seg(t, T.tip[1] + 0.05, T.tip[1] + 0.45));
  heap(1650, G3, 290, 78 + 30 * hk);
  const bearer = (x, female, phOff, tipK, backK) => {
    const ph = (x - (female ? b1.x0 : b2.x0)) * 0.6 / (S2 * U3) + phOff, wf = walkFeet(ph, S2);
    const still = female && ts >= T.bear[1];
    const fB = still ? [-2.2, 0] : wf.B, fF = still ? [2.6, 0] : wf.F;
    const k = tipK * (1 - backK);
    const top = [x + 0.72 * U3, G3 - 20.4 * U3];
    const bc = [lerp(top[0], x + 7.6 * U3, eOut(k)), lerp(top[1], G3 - 14.2 * U3, eIn(k))], ang = lerp(0, 1.25, k);
    const W = (lx, ly) => [bc[0] + lx * Math.cos(ang) - ly * Math.sin(ang), bc[1] + lx * Math.sin(ang) + ly * Math.cos(ang)];
    const toU = p => [(p[0] - x) / U3, (p[1] - G3) / U3];
    const grip = toU(W(-24, -8)), grip2 = toU(W(20, -4));
    human({ x, y: G3, H: H3, female, collar: female, skin: female ? COL.skinW : COL.skinM, bob: still ? 0 : -Math.abs(Math.sin(ph * TAU)) * 0.25,
      fB, fF, hB: k > 0.02 ? grip : [-0.9, -20.6], hF: k > 0.02 ? grip2 : [1.5 + Math.sin(ph * TAU) * 0.5, -8.4], eB: -1, eF: 1, fistB: true, fistF: k > 0.02 });
    if (female) POUR = W(29, -30);
    X.save(); X.translate(bc[0], bc[1]); X.rotate(ang); basket([0, 0], 58, 30, 1 - clamp((tipK - 0.5) * 2) * (1 - backK) - backK); X.restore();
  };
  bearer(x2, false, 0.4, 0, 0);
  bearer(x1, true, 0, tip, tipBack);
  if (tip > 0.45 && ts < T.tip[1] + 0.25) for (let s = 0; s < 40; s++) { const q = (ts * 2.2 + s / 40) % 1, fall = G3 - 48 - POUR[1];   // grain pouring from the rim
    const x = POUR[0] + q * 26 + (hash(s) - 0.5) * 14 * q, y = POUR[1] + q * fall;
    X.beginPath(); X.ellipse(x, y, 2.6, 1.8, 0.4, 0, TAU); X.fillStyle = COL.gold; X.fill(); X.strokeStyle = COL.ink; X.lineWidth = 0.8; X.stroke(); }
  speech(1690, G3 - 150, ['ONE MORE BASKET,', 'THEN BEER.'], seg(t, T.cap3 - 1.6, T.cap3 - 1.25));
}
function sheaf(x, y) {   // an upright bound sheaf
  X.save(); X.translate(x, y);
  for (let k = -3; k <= 3; k++) { X.beginPath(); X.moveTo(k * 3.2, 0); X.quadraticCurveTo(k * 0.6, -26, k * 3.6, -52); X.strokeStyle = COL.ochreD; X.lineWidth = 2.4; X.stroke(); }
  for (let k = -3; k <= 3; k++) wheatEar(k * 3.6, -52, k * 0.09, 1);
  X.beginPath(); X.ellipse(0, -24, 7, 3.2, 0, 0, TAU); paint(COL.red, 1.6);
  X.restore();
}

// ══ title band ══
function titleBand(t) {
  const cx = 960, cy = 149, w = 800, h = 98, r = h / 2;
  const draw = seg(t, T.title[0], T.title[0] + 0.55), fill = seg(t, T.title[0] + 0.3, T.title[0] + 0.7);
  if (draw <= 0) return;
  const path = (inset) => { X.beginPath(); X.moveTo(cx - w / 2 + r, cy - h / 2 + inset); X.lineTo(cx + w / 2 - r, cy - h / 2 + inset); X.arc(cx + w / 2 - r, cy, r - inset, -Math.PI / 2, Math.PI / 2);
    X.lineTo(cx - w / 2 + r, cy + h / 2 - inset); X.arc(cx - w / 2 + r, cy, r - inset, Math.PI / 2, Math.PI * 1.5); X.closePath(); };
  X.save(); X.globalAlpha = fill; path(0); X.fillStyle = COL.gold; X.fill(); X.restore();
  const per = 2 * (w - 2 * r) + TAU * r;
  X.save(); X.setLineDash([per * eInOut(draw), per]); path(0); X.strokeStyle = COL.ink; X.lineWidth = 5; X.stroke();
  X.setLineDash([per * eInOut(draw), per]); path(9); X.lineWidth = 2; X.stroke(); X.restore();
  // the tie bar at the end of the ring
  const bu = eBack(seg(t, T.title[0] + 0.45, T.title[0] + 0.75));
  if (bu > 0) { X.save(); X.translate(cx + w / 2 + 5, cy); X.scale(1, bu); X.fillStyle = COL.ink; X.fillRect(-5, -h / 2 + 4, 10, h - 8); X.restore(); }
  staggerText('HOW THE HARVEST CAME', cx - 10, cy + 17, 50, COL.blueD, t, T.title[0] + 0.45, 0.03);
  // side notes in red: a rosette, and two lines
  const la = seg(t, T.title[0] + 0.7, T.title[0] + 1.1);
  txt('A RECORD OF', 400, 138, 25, COL.red, la); txt('THREE SEASONS', 400, 172, 25, COL.red, la);
  rosette(196, 149, 22, eBack(la)); rosette(1724, 149, 22, eBack(seg(t, T.end[0] + 0.6, T.end[1] + 0.2)));
  staggerText('AND SO, EACH YEAR,', 1548, 138, 25, COL.red, t, T.end[0], 0.022);
  staggerText('IT CAME AGAIN.', 1548, 172, 25, COL.red, t, T.end[0] + 0.38, 0.022);
}
function rosette(x, y, r, k) {
  if (k <= 0) return; X.save(); X.translate(x, y); X.scale(k, k);
  for (let i = 0; i < 8; i++) { X.save(); X.rotate(i * TAU / 8); X.beginPath(); X.ellipse(0, -r * 0.55, r * 0.22, r * 0.45, 0, 0, TAU); paint(i % 2 ? COL.blue : COL.green, 1.6); X.restore(); }
  X.beginPath(); X.arc(0, 0, r * 0.26, 0, TAU); paint(COL.gold, 1.6); X.restore();
}

// ══ frame ══
function frame(t) {
  X = PX; PX.clearRect(0, 0, 1920, 1080);
  PX.drawImage(STATIC, 0, 0);
  titleBand(t);
  const regs = [reg1, reg2, reg3];
  for (let i = 0; i < 3; i++) {
    const rx = rollX(t, i), r = REG[i];
    if (rx <= IN.x0 + 17) continue;
    X.save(); X.beginPath(); X.rect(IN.x0, r.y0, Math.min(rx, IN.x1) - IN.x0, r.y1 - r.y0); X.clip();
    panel(i); X.save(); X.beginPath(); X.rect(SCN_X0 + 6, r.y0, IN.x1 - SCN_X0 - 6, r.y1 - r.y0); X.clip(); regs[i](t); X.restore();
    X.restore();
  }
  const c = MAIN;
  c.drawImage(TABLE, 0, 0);
  // the sheet opens between two rollers
  const o = eInOut(seg(t, ...T.open)) + 0.012 * Math.sin(Math.PI * seg(t, T.open[1] - 0.1, T.open[1] + 0.25));
  const half = lerp(26, 960 - SX0 + 4, o), lx = 960 - half, rxx = 960 + half;
  c.save(); c.beginPath(); c.rect(lx, 0, rxx - lx, 1080); c.clip();
  c.fillStyle = 'rgba(0,0,0,0.35)'; c.fillRect(SX0 + 10, SY0 + 12, SX1 - SX0, SY1 - SY0);   // sheet shadow on the table
  c.drawImage(SHEET, 0, 0);
  c.globalAlpha = 0.95; c.drawImage(PAINT, 0, 0); c.globalAlpha = 1;
  c.globalCompositeOperation = 'multiply'; c.globalAlpha = 0.7; c.drawImage(FIB, SX0, SY0, SX1 - SX0, SY1 - SY0, SX0, SY0, SX1 - SX0, SY1 - SY0); c.globalAlpha = 1; c.globalCompositeOperation = 'source-over';
  // register rolls still waiting / unrolling
  for (let i = 0; i < 3; i++) { const rx = rollX(t, i), r = REG[i]; if (rx < IN.x1 + 30) drawRoll(c, rx, r.y0 - 5, r.y1 + 5, lerp(34, 22, seg(rx, IN.x0, IN.x1))); }
  c.restore();
  drawRoll(c, lx, SY0 - 12, SY1 + 12, 46); drawRoll(c, rxx, SY0 - 12, SY1 + 12, 46);
  // gentle fade in and out
  const fi = 1 - seg(t, 0, 0.35), fo = eInOut(seg(t, ...T.fade));
  const a = Math.max(fi * 0.9, fo);
  if (a > 0) { c.fillStyle = `rgba(12,8,4,${a})`; c.fillRect(0, 0, 1920, 1080); }
}

window.draw = ({ t }) => { frame(t); return cv.toDataURL('image/jpeg', 0.92).split(',')[1]; };
window.events = () => {
  const ev = [{ k: 'open', t: T.open[0], d: T.open[1] - T.open[0] }, { k: 'ring', t: T.title[0] }, { k: 'title', t: T.title[0] + 0.45 }];
  T.roll.forEach(([a, b]) => ev.push({ k: 'roll', t: a, d: b - a }));
  ev.push({ k: 'sun', t: T.sun[0], d: T.sun[1] - T.sun[0] }, { k: 'flood', t: T.flood[0], d: T.recede[1] - T.flood[0] }, { k: 'ducks', t: T.ducks[0] + 0.05 });
  for (let tt = T.team[0]; tt < T.team[1]; tt += (3.2 * OXS / 0.6) / 84 / 2) ev.push({ k: 'hoof', t: +tt.toFixed(3) });
  for (let i = 0; i < 2; i++) for (let n = 0; ; n++) { const tt = T.reap[0] + i * 0.3 + (n + 0.55) * CHOP; if (tt > 9.3) break; ev.push({ k: 'chop', t: +tt.toFixed(3) }); }
  ev.push({ k: 'pour', t: T.tip[0] + 0.3, d: 0.6 }, { k: 'cap', t: T.cap2 }, { k: 'cap', t: T.cap3 - 1.6 }, { k: 'end', t: T.end[0] }, { k: 'fade', t: T.fade[0] });
  return ev.sort((a, b) => a.t - b.t);
};
window.ready = (async () => { await document.fonts.load(`50px ${FONT}`); await document.fonts.ready; bakePapyrus(); bakeTable(); bakeStatic(); X = PX; })();
