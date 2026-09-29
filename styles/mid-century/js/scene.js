// scene.js · "The Modern Way": a gentleman walks through an abstract city of rectangles, tips his hat,
// a starburst wipes to the title card. Limited animation: characters held on twos, cels slide on ones.
const cv = document.getElementById('c'); g = cv.getContext('2d');
const TL = { walkEnd: 4.1, tip: 4.42, burst: 4.86, title: 5.55, hatBack: 7.9, exit: 8.35, fade: 9.2 };
const GY = 925, FY = 1000, MS = 1.45, SPEED = 470, X0 = -300, CYC = 290 * MS;
const manWX = t => X0 + SPEED * Math.min(t, TL.walkEnd);
const camX = t => Math.max(0, manWX(t) - 700);

// ---- city ----
let NEAR = [], FAR = [], PROPS = [];
function initCity() {
  const r = mulberry(1950); let x = -260; const cols = ['mustard', 'teal', 'grey', 'oliveL', 'mustard', 'tealD', 'olive'];
  let i = 0;
  while (x < 3200) {
    const w = 170 + r() * 190, h = 260 + r() * 330, col = cols[(i * 3 + (r() * 2 | 0)) % cols.length];
    NEAR.push({ x, w, h, col, win: r() * 3 | 0, roof: r() * 3 | 0, seed: (r() * 1e6) | 0, i, ant: r() < 0.4 });
    x += w + (r() < 0.35 ? 30 + r() * 90 : -10); i++;
  }
  x = -300; i = 0;
  while (x < 2600) { const w = 140 + r() * 220, h = 420 + r() * 300; FAR.push({ x, w, h, i, col: r() < 0.5 ? 'sky' : 'cream', seed: (r() * 1e6) | 0 }); x += w * (0.6 + r() * 0.5); i++; }
  // foreground props: lollipop trees and a lamp post
  PROPS = [{ k: 'tree', x: 380 }, { k: 'lamp', x: 1150 }, { k: 'tree', x: 1900 }, { k: 'lamp', x: 2500 }, { k: 'tree', x: 3000 }];
}
function drawFar(t, cam) {
  const off = cam * 0.35;
  for (const b of FAR) {
    const x = b.x - off; if (x > W + 50 || x + b.w < -50) continue;
    const up = eBack(seg(onN(t, 2), 0.05 + b.i * 0.05, 0.6 + b.i * 0.05), 1.4);
    const y = GY - b.h * up;
    g.save(); g.translate(x, y);
    fill(rect(10, 10, b.w, b.h * up + 10), b.col, 0.9);
    // "a few lines for a city": outline only, drawn off-register from the pale block
    lineP([0, b.h * up, 0, 0, b.w, 0, b.w, b.h * up], 2.4, 0.45);
    const r = mulberry(b.seed);
    for (let k = 0; k < 4; k++) { const yy = 40 + k * 60 + r() * 20; if (yy > b.h * up - 40) break; lineP([18 + r() * 20, yy, b.w - 20 - r() * 30, yy], 1.8, 0.28); }
    g.restore();
  }
}
function drawBuilding(b, x, t) {
  const rise = eBack(seg(onN(t, 2), 0.1 + b.i * 0.07, 0.62 + b.i * 0.07), 1.9);
  if (rise <= 0) return;
  const h = b.h * rise;
  g.save(); g.beginPath(); g.rect(x - 60, -200, b.w + 120, GY + 200); g.clip();
  g.translate(x, GY - h);
  const r = mulberry(b.seed);
  let body;
  if (b.roof === 1) body = poly([0, 30, b.w, 0, b.w, h + 20, 0, h + 20], 3, b.seed);
  else if (b.roof === 2) body = poly([0, 0, b.w * 0.55, 0, b.w * 0.55, -40, b.w, -40, b.w, h + 20, 0, h + 20], 3, b.seed);
  else body = poly([0, 0, b.w, 0, b.w, h + 20, 0, h + 20], 3, b.seed);
  g.save(); g.translate(REG[0] + 2, REG[1] - 2); fill(body, b.col); g.restore();
  line(body, 3, 0.75);
  // windows: grid of cream slots / vertical crayon strokes / horizontal bands, printed off-register
  const dark = b.col === 'tealD' || b.col === 'olive';
  const wc = dark ? 'mustard' : 'white';
  if (b.win === 0) {
    const nx = Math.max(2, Math.floor((b.w - 40) / 46)), ny = Math.floor((h - 90) / 62);
    for (let j = 0; j < ny; j++) for (let k = 0; k < nx; k++) {
      if (r() < 0.18) continue;
      const wx = 22 + k * ((b.w - 44) / nx), wy = 60 + j * 62;
      g.save(); g.translate(-5, 4); fill(rect(wx, wy, 24, 34), r() < 0.2 ? 'orange' : wc); g.restore();
      lineP([wx, wy, wx + 24, wy, wx + 24, wy + 34], 2, 0.55);
    }
  } else if (b.win === 1) {
    for (let k = 26; k < b.w - 20; k += 28) lineP([k, 60, k + 2, h - 30], 3, 0.6);
    g.save(); g.translate(-6, 0); fill(rect(20, h - 110, 40, 90), 'ink'); g.restore();
  } else {
    for (let yy = 56; yy < h - 60; yy += 70) { g.save(); g.translate(6, -3); fill(rect(16, yy, b.w - 32, 22), wc, 0.95); g.restore(); lineP([14, yy + 26, b.w - 18, yy + 26], 2, 0.5); }
  }
  if (b.ant) { const ax = b.w * 0.3; lineP([ax, 0, ax, -80], 3, 0.8); lineP([ax - 26, -60, ax + 26, -60], 2.4, 0.8); lineP([ax - 16, -76, ax + 16, -76], 2.4, 0.8); }
  g.restore();
}
function drawProp(p, x, t) {
  const up = eBack(seg(onN(t, 2), 0.5 + p.x / 3000, 0.95 + p.x / 3000), 2.4);
  if (up <= 0) return;
  g.save(); g.translate(x, GY + 20); g.scale(1, up);
  if (p.k === 'tree') {
    lineP([0, 0, 0, -230], 6, 0.9); lineP([0, -150, 30, -185], 4, 0.9);
    g.save(); g.translate(8, -6); fill(ellipse(0, -300, 72, 100, 0.12), 'olive'); g.restore();
    line(ellipse(0, -300, 72, 100, 0.12), 3, 0.7);
    for (let k = 0; k < 5; k++) lineP([-30 + k * 14, -340 + k * 22, -8 + k * 14, -330 + k * 22], 2.4, 0.5);
  } else {
    lineP([0, 0, 0, -420, 40, -440], 6, 0.9);
    const shade = poly([22, -448, 78, -434, 70, -418, 30, -426]);
    fill(shade, 'mustard'); line(shade, 2.6, 0.8);
  }
  g.restore();
}
function drawCar(t, cam) {
  // slides in from the right, poses (squash + hold), then zips off left
  const tin = 1.75, tpose = 2.25, tout = 3.05;
  if (t < tin || t > tout + 0.5) return;
  const u = onN(t, 2);
  let sx;
  if (u < tpose) sx = lerp(W + 260, 1450, eBack(seg(u, tin, tpose), 1.6));
  else if (u < tout) sx = 1450;
  else sx = lerp(1450, -500, eIn(seg(u, tout, tout + 0.42)));
  const squash = u > tpose && u < tpose + 0.3 ? Math.sin(seg(u, tpose, tpose + 0.3) * Math.PI) * 0.06 : 0;
  const ant = u > tout - 0.18 && u < tout ? -0.05 : 0; // anticipation lean before the dash
  g.save(); g.translate(sx, GY + 6); g.scale(1.35 * (1 + squash), 1.35 * (1 - squash)); g.transform(1, 0, ant * 3, 1, 0, 0);
  const body = poly([-170, -40, -120, -44, -80, -92, 50, -96, 110, -50, 170, -44, 176, -6, -176, -6], 3, 5);
  const fin = poly([130, -48, 190, -86, 176, -44]);
  const glass = poly([-66, -84, 38, -88, 80, -52, -84, -48]);
  g.save(); g.translate(REG[0], REG[1]); fill(fin, 'teal'); fill(body, 'teal'); g.restore();
  fill(glass, 'white'); line(body, 3, 0.85); line(fin, 2.6, 0.8);
  lineP([-20, -86, -24, -48], 2.4, 0.7);
  fill(poly([-176, -26, 176, -26, 176, -16, -176, -16]), 'mustard');
  for (const wx of [-104, 108]) { g.fillStyle = C.ink; g.beginPath(); g.arc(wx, -4, 26, 0, TAU); g.fill(); g.fillStyle = C.white; g.beginPath(); g.arc(wx, -4, 9, 0, TAU); g.fill(); }
  g.restore();
  // speed lines as it leaves
  if (u > tout) { const k = seg(u, tout, tout + 0.35); for (let i = 0; i < 4; i++) lineP([sx + 200 + i * 20, GY - 90 + i * 22, sx + 200 + 260 * k + i * 30, GY - 90 + i * 22], 3, 0.7 * (1 - seg(u, tout + 0.3, tout + 0.5))); }
}
function drawSun(t) {
  const u = onN(t, 3), k = eBack(seg(u, 0.35, 0.9), 2);
  if (k <= 0) return;
  g.save(); g.translate(1560, 210); g.scale(k, k); g.rotate(Math.floor(t * 4) * 0.12);
  g.save(); g.translate(6, -4); fill(burst(0, 0, 118, 64, 14), 'orange'); g.restore();
  line(burst(0, 0, 118, 64, 14), 2.4, 0.5);
  fill(ellipse(0, 0, 50, 50), 'mustard');
  g.restore();
}
function drawClouds(t) {
  for (const [x0, y, s, rot, v] of [[300, 180, 1.2, -0.1, 18], [980, 120, 0.9, 0.18, 30], [1900, 300, 1.0, -0.2, 22]]) {
    const x = ((x0 - t * v - camX(t) * 0.12) % 2300 + 2300) % 2300 - 200;
    const b = boomerang(x, y, s, rot);
    g.save(); g.translate(5, -4); fill(b, 'white', 0.9); g.restore(); line(boomerang(x, y, s, rot), 2.4, 0.45);
  }
}
function manPose(t) {
  const u = onN(t, 2);
  if (u < TL.walkEnd) return walkPose(((manWX(u) - X0) / CYC) % 1);
  const st = STAND();
  if (u < TL.tip) { // stop: little rock back (anticipation), settle forward
    const k = seg(u, TL.walkEnd, TL.tip); const p = blendPose(walkPose(((manWX(TL.walkEnd) - X0) / CYC) % 1), st, eOut(seg(k, 0, 0.5)));
    p.lean = -0.07 * Math.sin(k * Math.PI); return p;
  }
  const tip = { ...st, arms: [{ sh: 2.0, el: 1.14 }, st.arms[1]], hatLift: 6, hatX: 9, hatTilt: -0.1, lean: 0.04, headTilt: 0.05 };
  const k = eBack(seg(u, TL.tip, TL.tip + 0.2), 2);
  return blendPose(st, tip, k);
}
function scene1(t) {
  const cam = camX(t);
  g.fillStyle = C.cream; g.fillRect(0, 0, W, H);
  drawSun(t); drawClouds(t);
  drawFar(t, cam);
  for (const b of NEAR) { const x = b.x - cam; if (x > W + 60 || x + b.w < -60) continue; drawBuilding(b, x, t); }
  // street: a single wobbly crayon line, a flat warm band, painted dashes
  g.save(); g.translate(0, GY); fill(rect(-10, 0, W + 20, H - GY), 'sky'); g.restore();
  lineP([-10, GY + 2, W + 10, GY - 2], 4, 0.9);
  // kerb: a second crayon line and a flat olive strip; the gentleman walks on the near pavement
  g.save(); g.translate(0, GY + 30); fill(rect(-10, 0, W + 20, 14), 'oliveL'); g.restore(); lineP([-10, GY + 30, W + 10, GY + 32], 3, 0.8);
  for (let k = 0; k < 12; k++) { const x = ((k * 190 - cam) % 2280 + 2280) % 2280 - 190; lineP([x, GY + 46, x - 30, H + 10], 2, 0.3); }
  for (const p of PROPS) { const x = p.x - cam; if (x < -200 || x > W + 200) continue; drawProp(p, x, t); }
  drawCar(t, cam);
  const mx = onN(manWX(t), 1) - cam;
  drawMan(Math.round(manWX(onN(t, 2)) - camX(onN(t, 2))), FY - 170 * MS, MS, manPose(t));
}

// ---- title card ----
const TITLE_A = 'THE', TITLE_B = 'MODERN', TITLE_C = 'WAY';
const SUB = 'in which a gentleman goes somewhere, stylishly.';
const CREDIT = 'A JUNIPER STUDIO CARTOON';
let LET = [];
function initTitle() {
  g.font = `190px "${FT}"`; let x = 190; const r = mulberry(55);
  for (const [i, ch] of [...TITLE_B].entries()) { const w = g.measureText(ch).width; LET.push({ ch, x, y: 560, size: 190, rot: (r() - 0.5) * 0.09, dy: (r() - 0.5) * 16, t0: TL.title + 0.28 + i * 0.09, col: 'ink', sh: i % 2 ? 'orange' : 'teal' }); x += w - 6; }
  g.font = `250px "${FT}"`; x = 260;
  for (const [i, ch] of [...TITLE_C].entries()) { const w = g.measureText(ch).width; LET.push({ ch, x, y: 800, size: 250, rot: (r() - 0.5) * 0.12, dy: (r() - 0.5) * 20, t0: TL.title + 0.95 + i * 0.13, col: ['orange', 'teal', 'white'][i], sh: 'ink', big: true }); x += w + 4; }
}
function drawLetter(L, t) {
  const u = onN(t, 2), k = seg(u, L.t0, L.t0 + 0.34); if (k <= 0) return;
  const e = eBack(k, 2.4);
  g.save(); g.translate(L.x + (1 - e) * -260, L.y + L.dy + (1 - e) * 120); g.rotate(L.rot + (1 - e) * -0.5);
  g.font = `${L.size}px "${FT}"`; g.textBaseline = 'alphabetic';
  // off-register second colour behind the letter
  g.fillStyle = TEX[L.sh] ? pat(L.sh) : L.sh; g.fillText(L.ch, 9, 7);
  g.fillStyle = pat(L.col); g.fillText(L.ch, 0, 0);
  g.restore();
}
function sparkles(t, ts) {
  const pts = [[1110, 250, 34], [150, 205, 22], [1260, 700, 26], [990, 110, 18], [1770, 860, 30], [990, 900, 20]];
  pts.forEach(([x, y, r], i) => { const k = eBack(seg(onN(t, 3), ts + 0.9 + i * 0.12, ts + 1.2 + i * 0.12), 2.5); if (k <= 0) return; const tw = 0.8 + 0.25 * ((Math.floor(t * 5) + i) % 2); sparkle(x, y, r * k * tw, 0.2 * i); });
}
function manPose2(t) {
  const st = STAND(), u = onN(t, 2);
  const tip = { ...st, arms: [{ sh: 2.0, el: 1.14 }, st.arms[1]], hatLift: 6, hatX: 9, hatTilt: -0.1, lean: 0.04, headTilt: 0.05 };
  if (u < TL.hatBack) return tip;
  if (u < TL.exit) return blendPose(tip, st, eBack(seg(u, TL.hatBack, TL.hatBack + 0.2), 1.5));
  return walkPose(((u - TL.exit) * SPEED * 1.25 / (290 * 1.42) + 0.25) % 1);
}
function scene2(t) {
  const ts = TL.burst + 0.2;
  g.fillStyle = C.cream; g.fillRect(0, 0, W, H);
  // big colour blocks slide in and settle, each printed a little off its crayon frame
  const sl = (a, d = 0.4) => eBack(seg(onN(t, 2), a, a + d), 1.8);
  let k = sl(ts + 0.05);
  g.save(); g.translate((1 - k) * -900, 0); g.rotate(-0.025);
  fill(rect(120, 300, 1010, 560), 'mustard'); lineP([104, 318, 1112, 290, 1122, 846], 3, 0.7);
  g.restore();
  k = sl(ts + 0.15);
  g.save(); g.translate(1520, 470); g.scale(k, k); fill(ellipse(8, -6, 330, 330), 'teal'); line(ellipse(0, 0, 330, 330), 3, 0.6); g.restore();
  k = sl(ts + 0.25);
  g.save(); g.translate(0, (1 - k) * 300); fill(poly([-20, 980, 1940, 930, 1940, 1100, -20, 1100]), 'olive'); lineP([-20, 976, 1940, 926], 3, 0.8); g.restore();
  // boomerangs glide in on their own cels
  [[1270, 180, 1.5, 0.3, 'orange'], [640, 130, 0.85, -0.12, 'tealD'], [1800, 120, 0.9, 2.6, 'mustard']].forEach(([x, y, s, rot, c], i) => {
    const kk = sl(ts + 0.35 + i * 0.12, 0.5); if (kk <= 0) return;
    const b = boomerang(x + (1 - kk) * 700, y, s, rot + (1 - kk) * 1.5); g.save(); g.translate(5, -4); fill(b, c); g.restore(); line(boomerang(x + (1 - kk) * 700, y, s, rot + (1 - kk) * 1.5), 2.4, 0.6);
  });
  // small credit + THE
  const ka = seg(onN(t, 2), TL.title, TL.title + 0.3);
  if (ka > 0) {
    g.globalAlpha = ka; g.font = `700 30px "${FC}"`; g.fillStyle = C.ink; g.textBaseline = 'alphabetic';
    if (g.letterSpacing !== undefined) g.letterSpacing = '9px'; g.fillText(CREDIT, 196, 250); if (g.letterSpacing !== undefined) g.letterSpacing = '0px';
    g.globalAlpha = 1;
    const e = eBack(ka, 2); g.save(); g.translate(200, 372 + (1 - e) * -60); g.rotate(-0.05);
    g.font = `92px "${FT}"`; g.fillStyle = pat('ink'); g.fillText(TITLE_A, 7, 5); g.fillStyle = pat('white'); g.fillText(TITLE_A, 0, 0); g.restore();
  }
  for (const L of LET) drawLetter(L, t);
  // script subtitle writes on left to right
  const ks = seg(t, TL.title + 1.7, TL.title + 2.6);
  if (ks > 0) {
    g.save(); g.font = `66px "${FS}"`; const w = g.measureText(SUB).width; g.beginPath(); g.rect(190, 830, (w + 40) * eOut(ks) + 10, 130); g.clip();
    g.fillStyle = pat('ink'); g.fillText(SUB, 210, 912); g.restore();
  }
  sparkles(t, ts);
  // the gentleman, larger, on the right: holds the hat tip, puts it back, strolls off
  const k2 = sl(ts + 0.3, 0.45); const mS = 1.42;
  let mx = 1500 + (1 - k2) * 700; if (t > TL.exit) mx += (onN(t, 2) - TL.exit) * SPEED * 1.25;
  drawMan(mx, 950 - 170 * mS, mS, manPose2(t));
}

// ---- transition: starburst from the hat ----
function hatScreen() { const ht = TL.tip + 0.3; return [manWX(ht) - camX(ht) + 20 * MS, FY - 170 * MS - 250 * MS]; }
function drawFrame(t) {
  const tb = TL.burst, [hx, hy] = hatScreen();
  const R = (t0) => 2600 * eIn(seg(t, t0, t0 + 0.5)) + 40 * eOut(seg(t, t0, t0 + 0.12));
  if (t < tb + 0.2 + 0.5) scene1(t);
  const rings = [[tb, 'mustard'], [tb + 0.1, 'orange'], [tb + 0.2, null]];
  for (const [t0, col] of rings) {
    if (t < t0) continue; const r = R(t0); if (r < 1) continue;
    const rot = Math.floor(t * 10) * 0.07;
    const p = burst(hx, hy, r, r * 0.62, 16, rot);
    if (col) { g.save(); g.translate(0, 0); fill(p, col); line(p, 4, 0.8); g.restore(); }
    else { g.save(); g.clip(p); scene2(t); g.restore(); if (r < 2400) line(p, 5, 0.9); }
  }
  g.globalCompositeOperation = 'multiply'; g.drawImage(PAPER, 0, 0); g.globalCompositeOperation = 'source-over';
  // open from cream paper, close to cream paper
  const a = Math.max(1 - eOut(seg(t, 0, 0.35)), eInOut(seg(t, TL.fade, DUR - 0.1)));
  if (a > 0) { g.globalAlpha = a; g.fillStyle = C.paper; g.fillRect(0, 0, W, H); g.drawImage(PAPER, 0, 0); g.globalAlpha = 1; }
}
window.events = () => {
  const ev = [];
  // footsteps: each contact of the walk cycle (phase 0 and 0.5)
  for (let n = 0; ; n++) { const tt = (n + 0.5) * CYC / 2 / SPEED; if (tt > TL.walkEnd) break; if (manWX(tt) > -120) ev.push({ k: 'step', t: tt, n }); }
  for (const b of NEAR) { const x = b.x; if (x > W) continue; ev.push({ k: 'rise', t: 0.1 + b.i * 0.07 + 0.3, pan: (x + b.w / 2 - 960) / 960 }); }
  ev.push({ k: 'sun', t: 0.6 }, { k: 'carIn', t: 1.75 }, { k: 'honk', t: 2.5 }, { k: 'carOut', t: 3.05 }, { k: 'stop', t: TL.walkEnd }, { k: 'tip', t: TL.tip }, { k: 'burst', t: TL.burst });
  for (const L of LET) ev.push({ k: L.big ? 'bigLetter' : 'letter', t: L.t0 + 0.22, pan: (L.x - 960) / 960 });
  for (let tt = TL.exit + 0.05; tt < DUR - 0.4; tt += 145 * 1.42 / (SPEED * 1.25)) ev.push({ k: 'step', t: tt, n: 99, soft: 1 });
  ev.push({ k: 'the', t: TL.title + 0.2 }, { k: 'script', t: TL.title + 1.7 }, { k: 'hatBack', t: TL.hatBack }, { k: 'exit', t: TL.exit }, { k: 'end', t: TL.fade - 0.25 });
  return ev.sort((a, b) => a.t - b.t);
};
window.ready = (async () => {
  await document.fonts.load(`190px "${FT}"`, TITLE_A + TITLE_B + TITLE_C); await document.fonts.load(`66px "${FS}"`, SUB); await document.fonts.load(`700 30px "${FC}"`, CREDIT); await document.fonts.ready;
  bakeTextures(); initCity(); initTitle();
})();
window.draw = ({ t }) => { drawFrame(t); return cv.toDataURL('image/jpeg', 0.92).split(',')[1]; };
