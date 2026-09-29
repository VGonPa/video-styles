// ── timeline + render ───────────────────────────────────────────────────────────────────────────
const T = { titleIn: .45, titleOut: 1.6, harr: 2.0, rattle: 2.3, open: 2.45, glow: 3.9, cap2: 4.3, bootA: 4.35, bootB: 4.65, slam: 71 / 15, hit: 73 / 15,
  rise: 5.35, hookA: 5.5, grab: 5.93, hoist: 6.0, lidShut: 6.0, travel: 6.3, arrive: 7.15, drop: 7.22, gulp: 7.34, boom: 7.7, unfurl: 8.0, unfurlEnd: 8.3,
  land: 9.0, iris: 9.35, irisEnd: 9.9 };
const CAPS = [[1.9, 'Item the First: a Good Idea.'], [T.cap2, 'The Committee examines it closely.'], [6.4, '…and refers it to the proper department.']];
const CHAIR_AT = [470, 330], CS = .85, BULB_AT = [1150, 540], BANNER_AT = [1960, 262], MOUTH = [2062, 166];
// Catmull-Rom through [t, x, y] keys
function path(keys, t) {
  if (t <= keys[0][0]) return [keys[0][1], keys[0][2]];
  for (let i = 0; i < keys.length - 1; i++) if (t <= keys[i + 1][0]) {
    const k0 = keys[Math.max(0, i - 1)], k1 = keys[i], k2 = keys[i + 1], k3 = keys[Math.min(keys.length - 1, i + 2)], u = (t - k1[0]) / (k2[0] - k1[0]);
    const cr = (a, b, c, d) => .5 * (2 * b + (-a + c) * u + (2 * a - 5 * b + 4 * c - d) * u * u + (-a + 3 * b - 3 * c + d) * u * u * u);
    return [cr(k0[1], k1[1], k2[1], k3[1]), cr(k0[2], k1[2], k2[2], k3[2])];
  }
  const l = keys[keys.length - 1]; return [l[1], l[2]];
}
const IDEAS = [
  { f: 'cup', t0: 2.62, ws: .7, wa: [30, -16], keys: [[2.62, 455, 300], [2.85, 430, 185], [3.3, 300, 120], [3.8, 170, 50], [4.3, 40, -140]] },
  { f: 'watch', t0: 2.75, ws: .7, wa: [34, -12], keys: [[2.75, 485, 300], [2.95, 505, 180], [3.4, 640, 105], [3.9, 780, 30], [4.4, 920, -150]] },
  { f: 'cog', t0: 2.88, ws: .62, wa: [34, -4], keys: [[2.88, 470, 300], [3.08, 470, 185], [3.5, 330, 225], [3.9, 230, 160], [4.4, -120, 120]] },
  { f: 'snail', t0: 3.0, ws: .55, wa: [-6, -52], one: 1, keys: [[3.0, 470, 300], [3.25, 580, 210], [3.8, 740, 110], [4.4, 820, 120], [5.2, 950, 150], [6.2, 1300, 120], [7.2, 1750, 110], [8.2, 2150, 90], [8.8, 2242, 118], [T.land, 2250, 124]] },
  { f: 'bulb', t0: 3.12, ws: .92, wa: [40, -26], keys: [[3.12, 470, 300], [3.35, 430, 185], [3.75, 720, 300], [4.15, 1080, 470], [4.4, BULB_AT[0], BULB_AT[1]]] },
];
const flap = (ts, i) => ((stepIx(ts) + i) & 1) ? -.55 : .22;
function drawIdea(I, i, ts) {
  const [px, py] = path(I.keys, ts), F = A[I.f], e = seg(ts, I.t0, I.t0 + .2), sc = .35 + .65 * eOut(e);
  const landed = I.f === 'snail' && ts >= T.land, fa = landed ? .45 : flap(ts, i), tilt = I.f === 'snail' ? -.05 : Math.sin(stepIx(ts) * 1.7 + i) * .06;
  const ws = I.ws * sc, [wx, wy] = I.wa;
  if (!I.one) put(A.wing, px - wx * sc, py + wy * sc, -fa, -ws, ws, .6);
  put(A.wing, px + wx * sc, py + wy * sc, fa, ws, ws, .6);
  put(F, px, py, tilt, sc * (I.f === 'snail' ? .9 : 1), sc * (I.f === 'snail' ? .9 : 1));
}
const bob = ts => ts < T.harr ? 0 : ts < T.harr + .3 ? -.035 * Math.sin(seg(ts, T.harr, T.harr + .3) * Math.PI) : ts < T.open + .15 ? .012 * Math.sin(seg(ts, T.open, T.open + .15) * Math.PI)
  : ts > T.hit + .15 && ts < T.hit + .5 ? .03 * Math.sin(seg(ts, T.hit + .15, T.hit + .5) * Math.PI) : 0;
function lidA(ts) {
  if (ts < T.rattle) return 0;
  if (ts < T.open) return (stepIx(ts) & 1) ? -.06 : -.015;
  if (ts < T.open + .3) return -1.1 * eBack(seg(ts, T.open, T.open + .3));
  if (ts < T.lidShut) return -1.1 + .05 * Math.sin(stepIx(ts) * .9) * (ts < 4.5 ? 1 : 0);
  return -1.1 * (1 - eIn(seg(ts, T.lidShut, T.lidShut + .3)));
}
function footY(ts) {
  if (ts < T.bootA) return -120;
  if (ts < T.bootB) return lerp(-120, 250, eOut(seg(ts, T.bootA, T.bootB)));
  if (ts < T.slam) return lerp(250, 196, eOut(seg(ts, T.bootB, T.slam)));
  if (ts < T.hit) return lerp(196, 880, eIn(seg(ts, T.slam, T.hit)));
  if (ts < T.rise) return 880;
  return lerp(880, -160, eIn(seg(ts, T.rise, T.rise + .45)));
}
function hookY(ts) {
  if (ts < T.hookA) return 190;
  if (ts < T.grab) return lerp(190, 785, eInOut(seg(ts, T.hookA, T.grab - .03)));
  if (ts < T.hoist) return 785;
  if (ts < T.arrive) return lerp(785, 262, eInOut(seg(ts, T.hoist, T.hoist + .35)));
  return lerp(262, 282, eOut(seg(ts, T.arrive, T.drop)));
}
const trolleyX = ts => lerp(BULB_AT[0], 1945, eInOut(seg(ts, T.travel, T.arrive)));
const camX = ts => CAMX * eInOut(seg(ts, 6.25, 7.2));
const swing = ts => ts < T.travel ? 0 : ts < T.arrive ? -.16 * Math.sin(Math.PI * seg(ts, T.travel, T.arrive)) : .1 * Math.sin((ts - T.arrive) * 14) * Math.exp(-(ts - T.arrive) * 5);
const shakeAt = ts => { if (ts < T.hit || ts > T.hit + .34) return [0, 0]; const k = stepIx(ts) - stepIx(T.hit), a = [14, -11, 8, -5, 3, -1][k] || 0; return [a, -a * .6]; };
const mShake = ts => (ts > T.gulp && ts < T.boom + .12) ? ((stepIx(ts) & 1) ? 3.5 : -3.5) : 0;
const gearA = ts => .35 * ts + 5.5 * eInOut(seg(ts, 7.3, 8.3));
const needle = ts => deg(ts < 7.3 ? -206 + 3 * Math.sin(ts * 3) : ts < T.boom ? lerp(-206, 26, eIn(seg(ts, 7.3, T.boom))) + (stepIx(ts) & 1) * 4 : lerp(30, -150, eOut(seg(ts, T.boom + .05, T.boom + .6))));
const PUFFS = [6.55, 6.95, 7.36, 7.47, 7.58, 7.66, 8.2, 8.7, 9.2];

function rope(x0, y0, x1, y1, lw = 4) {
  x.strokeStyle = INK; x.lineWidth = lw; x.lineCap = 'round'; x.beginPath(); x.moveTo(x0, y0); x.lineTo(x1, y1); x.stroke();
  x.strokeStyle = '#c9ad7a'; x.lineWidth = lw * .45; x.setLineDash([5, 6]); x.stroke(); x.setLineDash([]);
}
function world(ts) {
  const cam = camX(ts), [sx, sy] = shakeAt(ts);
  x.save(); x.translate(sx, sy);
  x.drawImage(A.sky.img, -cam * .6, 0);
  x.save(); x.translate(-cam, 0);
  x.drawImage(A.ground.img, 0, 560);
  put(A.crane, 0, 0, 0, 1, 1, .5);
  // ── chairman group ──
  const la = lidA(ts), open = la < -.08;
  x.save(); x.translate(CHAIR_AT[0], 800); x.rotate(bob(ts)); x.translate(0, CHAIR_AT[1] - 800); x.scale(CS, CS);
  if (open) { x.drawImage(A.cavity.img, -A.cavity.ox, -A.cavity.oy); put(A.cog2, 40, -96, ts * 3, 1, 1, 0); }
  x.restore();
  IDEAS.forEach((I, i) => { if (ts >= I.t0 && ts < I.t0 + .16) drawIdea(I, i, ts); });
  x.save(); x.translate(CHAIR_AT[0], 800); x.rotate(bob(ts)); x.translate(0, CHAIR_AT[1] - 800); x.scale(CS, CS);
  put(A.chair, 0, 0); put(A.lid, PIVOT[0], PIVOT[1], la);
  x.restore();
  put(A.desk, 0, 0);
  // ── the Good Idea's glory, and the other ideas ──
  const bulbI = IDEAS[4];
  if (ts >= T.glow && ts < T.hit) {
    const k = eOut(seg(ts, T.glow, T.glow + .25)), [bx, by] = path(bulbI.keys, ts);
    x.save(); x.globalCompositeOperation = 'multiply';
    const gr = x.createRadialGradient(bx, by, 10, bx, by, 260 * k); gr.addColorStop(0, 'rgba(246,206,90,.75)'); gr.addColorStop(1, 'rgba(246,206,90,0)');
    x.fillStyle = gr; x.fillRect(bx - 270, by - 270, 540, 540); x.restore();
    x.strokeStyle = INK; x.lineCap = 'round';
    const rr = stepIx(ts) * .035;
    for (let k2 = 0; k2 < 28; k2++) { const a = k2 / 28 * TAU + rr, l = (k2 & 1 ? 150 : 230) * k; x.lineWidth = k2 & 1 ? 1.4 : 2.4;
      x.beginPath(); x.moveTo(bx + Math.cos(a) * 118, by + Math.sin(a) * 118); x.lineTo(bx + Math.cos(a) * (118 + l * .6), by + Math.sin(a) * (118 + l * .6)); x.stroke(); }
  }
  IDEAS.forEach((I, i) => { if (ts >= I.t0 + .16 && I.f !== 'snail' && (I.f !== 'bulb' || ts < T.hit)) drawIdea(I, i, ts); });
  // ── foot shadow, the boot, dust ──
  const fy = footY(ts);
  if (ts >= T.bootA && ts < T.rise + .45) {
    const k = clamp((fy + 120) / 1000); x.save(); x.globalCompositeOperation = 'multiply'; x.fillStyle = `rgba(40,26,16,${.12 + .35 * k})`;
    x.beginPath(); x.ellipse(1150, 884, 90 + 250 * k, 16 + 24 * k, 0, 0, TAU); x.fill(); x.restore();
  }
  // ── the pancake (the examined idea), the hook, the trolley ──
  const tx = trolleyX(ts), hy = hookY(ts), sw = swing(ts), ht = [tx, hy - 44];
  const hang = (ox, oy) => [ht[0] + ox * Math.cos(sw) - oy * Math.sin(sw), ht[1] + ox * Math.sin(sw) + oy * Math.cos(sw)];
  if (ts >= T.hit && ts < T.grab) put(A.pancake, BULB_AT[0], 866, 0, 1, 1, .8);
  else if (ts >= T.grab && ts < T.drop) { const [px, py] = hang(12, 132); put(A.pancake, px, py, sw + .06, 1, 1, .7); }
  else if (ts >= T.drop && ts < T.gulp) { const [px, py] = hang(12, 132); put(A.pancake, px, lerp(py, 520, eIn(seg(ts, T.drop, T.gulp))), sw, .9, 1, .7); }
  const [rx, ry] = hang(0, 0); rope(tx, 128, rx, ry);
  put(A.hook, ht[0], ht[1] + 44, sw, 1, 1, .6);
  put(A.trolley, tx, 112, 0, 1, 1, .5);
  // ── the Resolution Engine ──
  const ms = mShake(ts); x.save(); x.translate(ms, 0);
  const ga = gearA(ts), gb = -ga * 130 / 105 + .12, pin = [2690 + Math.cos(gb) * 56, 720 + Math.sin(gb) * 56];
  put(A.machine, 0, 0);
  put(A.gearB, 2690, 720, gb, 1, 1, .8);
  put(A.gearA, 2530, 575, ga, 1, 1, .8);
  const chx = pin[0] - Math.sqrt(230 * 230 - (pin[1] - 721) ** 2);
  x.fillStyle = '#6f6a63'; x.strokeStyle = INK; x.lineWidth = 2.4; x.fillRect(chx - 22, 706, 44, 30); x.strokeRect(chx - 22, 706, 44, 30);
  x.lineCap = 'round'; x.lineWidth = 15; x.strokeStyle = INK; x.beginPath(); x.moveTo(chx, 721); x.lineTo(pin[0], pin[1]); x.stroke();
  x.lineWidth = 8; x.strokeStyle = '#9a958c'; x.stroke(); x.lineWidth = 2; x.strokeStyle = '#efe6d2'; x.stroke();
  x.fillStyle = INK; x.beginPath(); x.arc(pin[0], pin[1], 9, 0, TAU); x.fill(); x.beginPath(); x.arc(chx, 721, 7, 0, TAU); x.fill();
  const na = needle(ts); x.strokeStyle = INK; x.lineWidth = 4; x.beginPath(); x.moveTo(2000 - Math.cos(na) * 10, 626 - Math.sin(na) * 10); x.lineTo(2000 + Math.cos(na) * 46, 626 + Math.sin(na) * 46); x.stroke();
  x.fillStyle = INK; x.beginPath(); x.arc(2000, 626, 6, 0, TAU); x.fill();
  const rc = ts >= T.boom ? -28 * (1 - eOut(seg(ts, T.boom + .02, T.boom + .4))) : 0, ca = deg(-115);
  put(A.cannon, 2180 + Math.cos(ca) * rc, 420 + Math.sin(ca) * rc, ca, 1, 1, .8);
  x.restore();
  PUFFS.forEach((p0, i) => { const a = ts - p0; if (a < 0 || a > 1) return; const sc = (.35 + a * .9) * (a > .85 ? (1 - a) / .15 : 1);
    put(A.puffs[i % 3], 2300 + a * 70 + ms, 170 - a * 230, i + stepIx(ts) * .02, sc, sc, .4); });
  // ── the boot (from the heavens) ──
  if (fy > -110) put(A.boot, 1090, fy, 0, 1, 1, 1);
  if (ts >= T.hit && ts < T.hit + .55) { const a = seg(ts, T.hit, T.hit + .55);
    [[-1, 250], [-1, 400], [1, 330], [1, 470]].forEach(([d, o], i) => { const sc = (.35 + .6 * eOut(a)) * (a > .8 ? (1 - a) / .2 : 1); put(A.puffs[i % 3], 1150 + d * (o + a * 120), 860 - a * 40 - i * 6, i, sc, sc * .8, .4); }); }
  if (ts >= T.hit && ts < 5.9) { const a = seg(ts, T.hit, T.hit + .2), sc = (ts < 5.75 ? lerp(.5, 1, eBack(a)) : 1 - eIn(seg(ts, 5.75, 5.9))); if (sc > .01) put(A.burst, 1500, 390, -.08, sc * .92, sc * .92); }
  // ── cannon smoke + the banner ──
  if (ts >= T.boom && ts < T.boom + .75) { const a = seg(ts, T.boom, T.boom + .75);
    if (a < .16) { x.strokeStyle = INK; x.lineWidth = 3; for (let k = 0; k < 14; k++) { const an = ca + (k / 14 - .5) * 1.6; x.beginPath(); x.moveTo(MOUTH[0] + Math.cos(an) * 40, MOUTH[1] + Math.sin(an) * 40); x.lineTo(MOUTH[0] + Math.cos(an) * (80 + (k & 1) * 50), MOUTH[1] + Math.sin(an) * (80 + (k & 1) * 50)); x.stroke(); } }
    for (let k = 0; k < 3; k++) { const sc = (.5 + a * 1.1) * (a > .8 ? (1 - a) / .2 : 1); put(A.puffs[k], MOUTH[0] + (k - 1) * 60 * a - 20 * a, MOUTH[1] - 30 * a - k * 20 * a, k, sc, sc, .4); }
  }
  if (ts >= T.boom + .02 && ts < T.unfurl) { const u = seg(ts, T.boom + .02, T.unfurl);
    put(A.roll, lerp(MOUTH[0], BANNER_AT[0], u), lerp(MOUTH[1], BANNER_AT[1], u) - 70 * Math.sin(Math.PI * u), Math.PI / 2 * (1 - u) + u * 0, 1, 1, .6); }
  if (ts >= T.unfurl) {
    const u = seg(ts, T.unfurl, T.unfurlEnd), hw = 650 * eBack(u), full = ts >= T.unfurlEnd + .06;
    x.save(); x.beginPath(); const cw = full ? 820 : Math.min(hw, 650) + 6; x.rect(BANNER_AT[0] - cw - 20, BANNER_AT[1] - 160, cw * 2 + 40, 320); x.clip();
    put(A.banner, BANNER_AT[0], BANNER_AT[1], 0, 1, 1, 1); x.restore();
    if (!full) for (const s of [-1, 1]) put(A.roll, BANNER_AT[0] + s * Math.min(hw, 660), BANNER_AT[1], 0, 1, 1, .6);
  }
  if (ts >= IDEAS[3].t0 + .16) drawIdea(IDEAS[3], 3, ts);
  x.restore(); x.restore();
}
function render(t) {
  const ts = stp(t);
  x.setTransform(1, 0, 0, 1, 0, 0); x.globalAlpha = 1; x.globalCompositeOperation = 'source-over';
  x.fillStyle = '#1a120b'; x.fillRect(0, 0, W, H);
  world(ts);
  // caption plaque
  let ci = -1; for (let i = 0; i < CAPS.length; i++) if (ts >= CAPS[i][0] - .13) ci = i;
  if (ci >= 0) {
    const tc = CAPS[ci][0], closing = ts < tc, k = closing ? eIn(seg(ts, tc - .13, tc)) : eOut(seg(ts, tc, tc + .15)), idx = closing ? ci - 1 : ci;
    const sy = closing ? 1 - k : (ci === 0 ? eBack(seg(ts, tc, tc + .2)) : k);
    if (idx >= 0 && sy > .02) put(A.plaques[idx], 960, 1004, 0, 1, sy, .8);
  }
  // title card on ropes
  if (ts < T.titleOut + .45) {
    let cy = ts < T.titleIn ? lerp(-520, 520, eBack(seg(ts, 0, T.titleIn))) : 520;
    if (ts >= T.titleOut) cy = ts < T.titleOut + .1 ? 520 + 22 * Math.sin(seg(ts, T.titleOut, T.titleOut + .1) * Math.PI / 2) : lerp(542, -560, eIn(seg(ts, T.titleOut + .1, T.titleOut + .4)));
    const rot = ts < T.titleOut ? .012 * Math.sin(stepIx(ts) * .8) * (1 - seg(ts, 0, 1.2) * .5) : 0;
    for (const s of [-1, 1]) { const ax = 960 + s * 560 * Math.cos(rot) - (-380) * Math.sin(rot) * 0, ay = cy - 380 + s * 560 * Math.sin(rot); rope(ax, ay, 960 + s * 590, -40, 6); }
    put(A.title, 960, cy, rot, 1, 1, 1.2);
  }
  // film: static grain, per-step dust + flicker, vignette, fades, iris
  x.globalCompositeOperation = 'multiply'; x.drawImage(A.vig, 0, 0); x.globalCompositeOperation = 'overlay'; x.globalAlpha = .5; x.drawImage(A.grain, 0, 0); x.globalAlpha = 1; x.globalCompositeOperation = 'source-over';
  const si = stepIx(t), dr = rng(900 + si);
  for (let i = 0, n = Math.floor(dr() * 5); i < n; i++) { x.fillStyle = `rgba(35,22,12,${.35 + dr() * .4})`; x.beginPath(); x.ellipse(dr() * W, dr() * H, 1 + dr() * 2.5, 1 + dr() * 2, dr() * 3, 0, TAU); x.fill(); }
  if (si % 23 === 7) { x.strokeStyle = 'rgba(35,22,12,.3)'; x.lineWidth = 1.2; const hx = dr() * W, hy = dr() * H; x.beginPath(); x.moveTo(hx, hy); x.bezierCurveTo(hx + 25, hy + 30, hx - 18, hy + 60, hx + 12, hy + 96); x.stroke(); }
  x.fillStyle = `rgba(30,18,8,${.03 * dr()})`; x.fillRect(0, 0, W, H);
  if (ts >= T.iris) {
    const u = seg(ts, T.iris, T.irisEnd), cam = camX(ts), [snx, sny] = path(IDEAS[3].keys, ts);
    const cx = lerp(960, snx - cam, eOut(u)), cy = lerp(540, sny, eOut(u)), r = 1250 * Math.pow(1 - eInOut(u), 1.2);
    x.fillStyle = '#140d07'; x.beginPath(); x.rect(0, 0, W, H); if (r > 1) { x.moveTo(cx + r, cy); x.arc(cx, cy, r, 0, TAU); } x.fill('evenodd');
    if (r > 1) { x.strokeStyle = 'rgba(20,13,7,.5)'; x.lineWidth = 10; x.beginPath(); x.arc(cx, cy, r + 3, 0, TAU); x.stroke(); }
  }
  const fade = 1 - seg(ts, 0, .27);
  if (fade > 0) { x.fillStyle = `rgba(20,13,7,${fade})`; x.fillRect(0, 0, W, H); }
}
function buildFilm() {
  A.grain = mk(W, H); const g = A.grain.getContext('2d'), im = g.createImageData(W, H), r = rng(5);
  for (let i = 0; i < W * H; i++) { const v = 128 + (r() - .5) * 46; im.data[i * 4] = im.data[i * 4 + 1] = im.data[i * 4 + 2] = v; im.data[i * 4 + 3] = 255; }
  g.putImageData(im, 0, 0);
  A.vig = mk(W, H); const v = A.vig.getContext('2d'), gr = v.createRadialGradient(W / 2, H / 2, 380, W / 2, H / 2, 1180);
  gr.addColorStop(0, '#fff'); gr.addColorStop(.7, '#e9dcc6'); gr.addColorStop(1, '#8a735a'); v.fillStyle = gr; v.fillRect(0, 0, W, H);
}
window.ready = (async () => {
  await Promise.all([`italic 60px ${SERIF}`, `60px ${SERIF}`, `60px ${SC}`, `60px ${FAT}`].map(f => document.fonts.load(f, 'THE Very Serious COMMITTEE for Good Ideas … SQUASH! 1851 ·')));
  await document.fonts.ready;
  buildSky(); buildGround(); buildChair(); buildLid(); buildCavity(); buildDesk();
  buildWing(); buildBulb(); buildCup(); buildWatch(); buildSnail(); A.cog = buildGear(40, 10, { tint: '#8e9ba1', seed: 3 }); A.cog2 = buildGear(34, 9, { tint: '#b08d47', seed: 4 });
  buildBoot(); buildBurst(); A.puffs = [buildPuff(201), buildPuff(202), buildPuff(203)]; buildCrane(); buildMachine();
  A.gearA = buildGear(130, 18, { spokes: 5, tint: '#b08d47', s: 5.5 }); A.gearB = buildGear(105, 14, { spokes: 4, tint: '#8e9294', s: 5.5 });
  buildCannon(); buildBanner(); buildPancake(); buildFilm();
  A.title = buildTitle(true, (P, orn) => {
    inkText(P, 'MINUTES OF THE WEEKLY SITTING', 0, -262, `38px ${SC}`, { ls: 6 });
    orn(-226);
    inkText(P, 'The Very Serious', 0, -126, `italic 92px ${SERIF}`);
    engText(P, 'COMMITTEE', 0, 72, `200px ${FAT}`, { fs: 190, tint: '#9b2d24', sh: 9 });
    inkText(P, 'for Good Ideas', 0, 184, `italic 88px ${SERIF}`);
    orn(228);
    inkText(P, 'ESTABLISHED 1851  ·  NOTHING YET RESOLVED', 0, 292, `34px ${SC}`, { ls: 4 });
  });
  A.plaques = CAPS.map((c, i) => buildPlaque(c[1], 300 + i));
  render(0);
})();
window.draw = ({ t }) => { render(t); return cv.toDataURL('image/jpeg', 0.92).split(',')[1]; };
window.events = () => {
  const ev = [{ t: .05, k: 'rope' }, { t: T.titleIn - .05, k: 'thud', v: .5 }, { t: T.titleOut, k: 'rope' }, { t: T.titleOut + .1, k: 'whoosh', d: .4 },
    { t: CAPS[0][0], k: 'flip' }, { t: CAPS[1][0], k: 'flip' }, { t: CAPS[2][0], k: 'flip' },
    { t: T.harr, k: 'harrumph' }, { t: T.rattle, k: 'rattle' }, { t: T.open, k: 'hinge' }, { t: T.glow, k: 'shimmer' },
    { t: T.bootA, k: 'descend', d: T.hit - T.bootA }, { t: T.hit, k: 'stomp' }, { t: T.hit + .02, k: 'tinkle' }, { t: T.rise, k: 'whoosh', d: .45 },
    { t: T.hookA, k: 'ratchet', d: T.grab - T.hookA }, { t: T.grab, k: 'clank', v: .6 }, { t: T.hoist, k: 'ratchet', d: .35 }, { t: T.travel, k: 'trolley', d: T.arrive - T.travel },
    { t: T.lidShut + .3, k: 'clank', v: .4 }, { t: T.drop + .02, k: 'gulp' }, { t: T.gulp, k: 'chug', d: T.boom - T.gulp }, { t: 7.5, k: 'whistle' },
    { t: T.boom, k: 'boom' }, { t: T.unfurl, k: 'unfurl' }, { t: T.unfurlEnd, k: 'fanfare' }, { t: T.land, k: 'pip' }, { t: T.iris, k: 'close' }];
  IDEAS.forEach(I => ev.push({ t: I.t0, k: 'pop' }, { t: I.t0 + .05, k: 'flutter', d: I.f === 'snail' ? 1.2 : 1.1 }));
  PUFFS.forEach(p => ev.push({ t: p, k: 'puff' }));
  return ev.sort((a, b) => a.t - b.t);
};
