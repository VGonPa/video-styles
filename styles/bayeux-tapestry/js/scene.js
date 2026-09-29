// scene.js · the strip, the camera travelling along it, live stitching, rollers and the frame
const cv = document.getElementById('c'), CX = cv.getContext('2d');
const SW = 5400, SH = 840, SY0 = 120, GY = 690;   // strip width/height, strip top on screen, ground line (strip coords)
const MAIN0 = 128, MAIN1 = 712;
let STRIP, BG, LIGHT;

// ── timeline ──
const T = { fadeIn: [0, 0.5], unroll: [0.15, 1.75], cap1: [0.7, 2.35], point: [0.9, 1.5], cap2: [3.7, 4.95], cap3: [6.35, 7.6],
  serve: [5.4, 8.0], toast: [7.1, 7.35, 7.6, 7.85], rollup: [8.3, 9.5], fade: [9.3, 10] };
// camera: eased travel along the strip (velocity ramps up, cruises, ramps down), integrated once
const CAM0 = -70, CAM1 = SW - 1790, CAM = [];
(() => { const n = 3000, v = t => eSine(seg(t, 1.5, 2.7)) * (1 - eSine(seg(t, 6.9, 8.1))); let a = 0; CAM.push(0);
  for (let i = 1; i <= n; i++) { a += (v((i - 0.5) / 300)) / 300; CAM.push(a); } const k = (CAM1 - CAM0) / a; for (let i = 0; i <= n; i++) CAM[i] = CAM0 + CAM[i] * k; })();
const camX = t => { const f = clamp(t, 0, 10) * 300, i = Math.min(2999, Math.floor(f)); return lerp(CAM[i], CAM[i + 1], f - i); };

// captions (centred on their scenes)
const CAPCOL = [COL.blueD, COL.terraD, COL.greenD];
function capAt(text, cx, seed) { const w = caption(text, 0, 0, 7.4, CAPCOL, seed); return caption(text, cx - (w.x1 - 11) / 2, 146, 7.4, CAPCOL, seed); }
const CAP1 = capAt('HERE LORD EDRIC MAKES READY TO SAIL', 880, 5);
const CAP2 = capAt('AND HERE THEY CROSS THE SEA', 2790, 7);
const CAP3 = capAt('HERE THEY FEAST, AND ALL ARE GLAD', 4655, 9);

// ── bake: wall, linen strip with borders and static pieces ──
function bakeBG() {
  BG = mk(1920, 1080); const g = BG.getContext('2d'), r = mulberry(21);
  g.fillStyle = '#2b231d'; g.fillRect(0, 0, 1920, 1080);
  for (let i = 0; i < 900; i++) { const x = r() * 1920, y = r() * 1080, rad = 10 + r() * 60; const gg = g.createRadialGradient(x, y, 0, x, y, rad);
    gg.addColorStop(0, `rgba(${r() < 0.5 ? '70,58,46' : '18,14,11'},${0.12 + r() * 0.12})`); gg.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gg; g.fillRect(x - rad, y - rad, rad * 2, rad * 2); }
  const sp = g.createRadialGradient(960, 520, 100, 960, 540, 1150); sp.addColorStop(0, 'rgba(255,220,170,0.10)'); sp.addColorStop(1, 'rgba(0,0,0,0.55)');
  g.fillStyle = sp; g.fillRect(0, 0, 1920, 1080);
  LIGHT = mk(1920, 1080); const l = LIGHT.getContext('2d');
  const lg = l.createRadialGradient(900, 470, 250, 960, 540, 1250); lg.addColorStop(0, 'rgba(255,238,205,0.10)'); lg.addColorStop(0.6, 'rgba(0,0,0,0)'); lg.addColorStop(1, 'rgba(10,6,2,0.42)');
  l.fillStyle = lg; l.fillRect(0, 0, 1920, 1080);
}
function bakeStrip() {
  STRIP = mk(SW, SH); const c = STRIP.getContext('2d'), r = mulberry(98);
  // cloth with slightly wavy long edges
  const top = [], bot = []; for (let x = 0; x <= SW; x += 30) { top.push([x, 2 + r() * 3 + Math.sin(x / 400) * 1.5]); bot.push([x, SH - 2 - r() * 3 + Math.sin(x / 350) * 1.5]); }
  const cloth = top.concat(bot.reverse());
  LINEN_PAT = c.createPattern(LINEN_TILE, 'repeat');
  c.save(); c.clip(pathOf(cloth)); c.fillStyle = LINEN_PAT; c.fillRect(0, 0, SW, SH);
  for (let i = 0; i < 140; i++) { const x = r() * SW, y = r() * SH, rad = 60 + r() * 260; const g = c.createRadialGradient(x, y, 0, x, y, rad);
    g.addColorStop(0, r() < 0.7 ? 'rgba(150,110,55,0.08)' : 'rgba(255,248,228,0.08)'); g.addColorStop(1, 'rgba(0,0,0,0)'); c.fillStyle = g; c.fillRect(x - rad, y - rad, rad * 2, rad * 2); }
  for (const [y0, y1] of [[0, 34], [SH, SH - 34]]) { const g = c.createLinearGradient(0, y0, 0, y1); g.addColorStop(0, 'rgba(120,85,40,0.28)'); g.addColorStop(1, 'rgba(120,85,40,0)'); c.fillStyle = g; c.fillRect(0, Math.min(y0, y1), SW, 34); }
  c.restore();
  // hems: a folded edge held with running stitches
  for (const y of [9, SH - 9]) { c.save(); c.setLineDash([7, 6]); c.strokeStyle = 'rgba(120,92,52,0.7)'; c.lineWidth = 2; c.beginPath(); c.moveTo(0, y); c.lineTo(SW, y); c.stroke(); c.restore();
    c.fillStyle = 'rgba(90,65,30,0.10)'; c.fillRect(0, y < SH / 2 ? 0 : SH - 16, SW, 16); }
  // register lines
  for (const y of [18, MAIN0, MAIN1, 822]) { stem(c, [[4, y], [SW - 4, y]], COL.blueD, 4.2, 1, 10); }
  stem(c, [[4, MAIN0 - 7], [SW - 4, MAIN0 - 7]], COL.terra, 3, 1, 9); stem(c, [[4, MAIN1 + 7], [SW - 4, MAIN1 + 7]], COL.terra, 3, 1, 9);
  // borders: slanted bars with paired creatures between them
  const pal = [[COL.terra, COL.mustard], [COL.sage, COL.terraD], [COL.blue, COL.mustardL], [COL.mustard, COL.green], [COL.blueL, COL.terra]];
  for (const [y0, y1, sd] of [[18, MAIN0 - 7, 0], [MAIN1 + 7, 822, 1]]) {
    const H = y1 - y0;
    for (let i = 0, x = 40; x < SW; x += 180, i++) {
      const bc = [COL.mustard, COL.sage, COL.terra, COL.blueL][(i + sd) % 4];
      piece(c, [[x, y1 - 3], [x + 16, y1 - 3], [x + 16 + H * 0.42, y0 + 3], [x + H * 0.42, y0 + 3]], bc, 90 - 23, COL.blueD, 3, { gap: 16 });
      const k = (i * 3 + sd * 2) % 5, [c1, c2] = pal[k], cx = x + 100, gy = y1 - 8, type = (i + sd) % 3;
      if (type === 0) bird(c, cx, gy, 1.02, c1, c2, (i + sd) % 2 === 1);
      else if (type === 1) beast(c, cx - 4, gy, 1.0, c1, c2, (i + sd) % 2 === 0);
      else bird(c, cx, gy, 0.95, c2, c1, (i + sd) % 2 === 0);
    }
  }
  // scene furniture
  hall(c, 110, GY);
  ground(c, 30, 1630, GY + 4); ground(c, 3700, SW - 20, GY + 4);
  tree(c, 1590, GY + 4, 0.95, {});
  tree(c, 3770, GY + 4, 0.95, { b: COL.green, t: COL.terraD, l1: COL.terra, l2: COL.sage });
  tree(c, 5330, GY + 4, 0.7, { b: COL.sage, t: COL.mustard, l1: COL.green, l2: COL.terra });
  canopy(c, 4070, 5250, GY);
  // the left end is sewn to a rod: a darker binding band
  c.fillStyle = 'rgba(80,55,25,0.18)'; c.fillRect(0, 0, 18, SH); c.fillRect(SW - 18, 0, 18, SH);
}

// ── live pieces ──
function drinkHorn(c, wr, b) {
  const d = [Math.sin(b), Math.cos(b)], p = [d[1], -d[0]], P = (t, n) => [wr[0] + d[0] * t + p[0] * n, wr[1] + d[1] * t + p[1] * n];
  const H = cr([P(8, -10), P(2, -24), P(-14, -30), P(-22, -26), P(-6, -12), P(4, -2)], true, 3);
  piece(c, H, COL.mustardL, 0, COL.blueD, 3, { bars: false });
  stem(c, [P(-14, -30), P(-22, -26)], COL.terraD, 4, 1, 5);
}
function cup(c, wr, b) {
  const x = wr[0] + 8 * Math.sin(b), y = wr[1] + 8 * Math.cos(b) - 8;
  piece(c, [[x - 12, y - 16], [x + 12, y - 16], [x + 7, y], [x + 2, y + 2], [x + 2, y + 10], [x + 8, y + 14], [x - 8, y + 14], [x - 2, y + 10], [x - 2, y + 2], [x - 7, y]], COL.terra, 0, COL.blueD, 3, { bars: false });
}
function platter(c, wr, b) {   // a dish with a roast bird, held level
  const x = wr[0] + 18, y = wr[1] - 6;
  piece(c, cr([[x - 44, y], [x + 44, y], [x + 34, y + 9], [x - 34, y + 9]], true, 2), COL.mustard, 0, COL.blueD, 3, { bars: false });
  piece(c, cr([[x - 30, y - 2], [x - 24, y - 22], [x, y - 30], [x + 22, y - 24], [x + 30, y - 6], [x + 20, y - 1]], true, 3), COL.terra, 20, COL.blueD, 3, { gap: 12 });
  stem(c, [[x - 24, y - 16], [x - 38, y - 30]], COL.blueD, 3.4, 1, 5); stem(c, [[x + 24, y - 14], [x + 36, y - 26]], COL.blueD, 3.4, 1, 5);
  knot(c, x - 39, y - 31, COL.mustardL, 3.2); knot(c, x + 37, y - 27, COL.mustardL, 3.2);
}
function table(c) {
  const ol = COL.blueD, x0 = 4175, x1 = 5145, y = 575;
  // trestles, then a cloth with a scalloped, knotted hem hanging over the board
  for (const tx of [x0 + 70, x1 - 70]) for (const sd of [-1, 1]) piece(c, thick([[tx, y + 40], [tx + sd * 34, GY + 2]], [12, 10]), COL.terraD, 90, ol, 3, { bars: false });
  const F = []; for (let k = 0; k <= 40; k++) { const u = k / 40, xx = lerp(x0, x1, u); F.push([xx, y + 64 + 7 * Math.abs(Math.sin(Math.PI * u * 10))]); }
  const cloth = [[x0, y + 10], [x1, y + 10], ...F.slice().reverse()];
  piece(c, cloth, COL.blueL, 90, ol, 4, { gap: 22 });
  for (let k = 1; k < 20; k++) { const u = k / 20, xx = lerp(x0, x1, u); stem(c, [[xx, y + 14], [xx + 2, y + 36], [xx, y + 60]], COL.blue, 2.8, 1, 8); }
  const hem = F.concat(F.slice().reverse().map(([a, b]) => [a, b - 14]));
  piece(c, hem, COL.terra, 0, ol, 3, { bars: false });
  for (let k = 0.5; k < 20; k += 1) { const u = k / 20; knot(c, lerp(x0, x1, u), y + 62, COL.mustardL, 2.6); }
  piece(c, [[x0 - 16, y - 6], [x1 + 16, y - 6], [x1 + 8, y + 12], [x0 - 8, y + 12]], COL.mustard, 0, ol, 4, { bars: false });
  // food: bowls, loaves, a fish on a dish, a jug
  const loaf = x => piece(c, [[x - 18, y - 6], ...ell(x, y - 6, 18, 16, Math.PI, TAU, 10)], COL.mustardL, 0, ol, 3, { bars: false });
  const bowlUp = (x, cc) => piece(c, [[x - 26, y - 34], [x + 26, y - 34], [x + 18, y - 12], [x + 6, y - 10], [x + 6, y - 6], [x - 6, y - 6], [x - 6, y - 10], [x - 18, y - 12]], cc, 0, ol, 3, { bars: false });
  bowlUp(4250, COL.sage); loaf(4430); bowlUp(4640, COL.terra); loaf(4700);
  fish(c, 4880, y - 22, 1.1, COL.blue, false); piece(c, cr([[4830, y - 8], [4930, y - 8], [4920, y - 2], [4840, y - 2]], true, 2), COL.mustard, 0, ol, 2.6, { bars: false });
  piece(c, cr([[5055, y - 6], [5040, y - 30], [5046, y - 52], [5040, y - 64], [5070, y - 64], [5064, y - 52], [5070, y - 30]], true, 3), COL.green, 90, ol, 3, { bars: false });
  loaf(4990); bowlUp(4535, COL.blueL);
}
// the four guests: seated behind the table (legs hidden by the cloth); horns raised one after another
function diners(c, t) {
  const G = [[4330, false, COL.terra, COL.mustard, COL.blueD, drinkHorn, true], [4545, false, COL.mustard, COL.terra, COL.terraD, cup, false],
             [4770, true, COL.sage, COL.terra, COL.mustard, drinkHorn, true], [4995, true, COL.blueL, COL.mustard, COL.terra, cup, false]];
  G.forEach(([x, flip, tun, hem, hair, hold, beard], i) => {
    const u = eBack(seg(t, T.toast[i], T.toast[i] + 0.5)), sway = Math.sin(t * 3 + i) * 0.03;
    const arms = [[lerp(0.55, 2.55, u) + sway, lerp(0.95, 0.35, u)], [0.35, 1.0]];
    human(c, x, 694 + (u > 0 ? -3 * Math.sin(Math.PI * seg(t, T.toast[i], T.toast[i] + 0.4)) : 0), { flip, tunic: tun, hem, hose: COL.blue, hair, beard, upper: true, arms, hold });
  });
}
function crewman(c, x, y, s, o) { human(c, x, y, Object.assign({ s, upper: true, hose: COL.blue }, o)); }
function ships(c, t) {
  const S = [[2000, 0, true], [2800, 1.7, false]];
  S.forEach(([x0, ph, first]) => {
    const x = x0 + 48 * t, y = 620 + 5 * Math.sin(t * 2.1 + ph + 0.6), rot = 0.022 * Math.sin(t * 2.1 + ph), bill = 0.6 + 0.4 * Math.sin(t * 1.3 + ph);
    if (x < camX(t) - 400 || x > camX(t) + 2350) return;
    ship(c, x, y, { rot, bill, shields: first,
      crew: gun => {
        if (first) {
          crewman(c, -92, gun(-92) + 116, 0.78, { tunic: COL.sage, hem: COL.terra, hair: COL.blueD, arms: [[0.9, 0.6], [0.6, 0.6]] });
          crewman(c, 70, gun(70) + 116, 0.8, { tunic: COL.terra, hem: COL.mustard, hair: COL.mustard, beard: true, arms: [[2.05 + 0.05 * Math.sin(t * 2), 0.12], [0.4, 0.5]], open: true });
        } else {
          horse(c, -60, gun(-60) + 150, { s: 0.9, col: COL.terra, col2: COL.blue, mane: COL.mustard });
          horse(c, 100, gun(100) + 146, { s: 0.9, col: COL.blueL, col2: COL.terra, mane: COL.terraD });
        }
        crewman(c, -196, gun(-196) + 114, 0.78, { tunic: first ? COL.blueL : COL.mustard, hem: COL.terra, hair: COL.terraD, arms: [[1.0, 0.5], [0.8, 0.6]] });
      },
      front: gun => { piece(c, thick([[-150, gun(-196) - 36], [-222, 10], [-230, 44]], [9, 9, 22]), COL.terraD, 20, COL.blueD, 3, { bars: false }); } });
  });
}
function seaAndFish(c, t) {
  if (camX(t) + 1920 < 1600 || camX(t) > 3760) return;
  waves(c, 1655, 3700, [0, 1, 2, 3], t);
  fish(c, 2330 + 30 * t, 674, 1.35, COL.mustard, false); fish(c, 3350 - 22 * t, 698, 1.2, COL.terra, true);
}
function scene1(c, t) {
  if (camX(t) > 1500) return;
  // lord at the hall door points to the sea
  const pu = eBack(seg(t, ...T.point));
  human(c, 630, GY, { s: 1.1, tunic: COL.terra, hem: COL.mustard, hose: COL.blue, hair: COL.mustard, beard: true, arms: [[lerp(0.25, 1.95, pu), lerp(0.3, 0.1, pu)], [-0.1, 0.3]], open: pu > 0.5, legs: [[0.14, 0.04], [-0.1, 0.03]] });
  // groom leads the horse towards the shore
  const gx = 1175 + 24 * t, ph = t * 5.2, wp = walkPose(ph, 0.85);
  const hx = gx - 330;
  horse(c, hx, GY + 1, { s: 1.1, col: COL.blue, col2: COL.terra, mane: COL.mustard, saddle: COL.green, ph: ph * 1.0, walk: 0.8, rein: [(gx - 64 - hx) / 1.1, (-134 + wp.bob) / 1.1] });
  human(c, gx, GY + wp.bob, { s: 1.1, tunic: COL.sage, hem: COL.terra, hose: COL.terra, hair: COL.blueD, legs: wp.legs, arms: [[0.3 * Math.sin(ph + Math.PI), 0.35], [-0.75, 0.3]] });
}
function scene3(c, t) {
  if (camX(t) + 1920 < 3700) return;
  const k = seg(t, ...T.serve), w = 1 - seg(t, T.serve[1] - 0.5, T.serve[1]);
  const sx = 3905 + 110 * eSine(k), ph = t * 5.2, wp = walkPose(ph, 0.8 * w);
  human(c, sx, GY + wp.bob, { s: 1.05, tunic: COL.mustard, hem: COL.green, hose: COL.sage, hair: COL.terraD, legs: wp.legs, arms: [[1.25, 0.35], [1.1, 0.45]], over: platter });
  diners(c, t); table(c);
}

// ── needle and thread ──
function needle(c, h, t, lift) {
  const a = -0.95, dx = Math.cos(a), dy = Math.sin(a), dip = 8 * (0.5 + 0.5 * Math.sin(t * 46)) * (1 - lift);
  const tx = h.x + dx * (dip - 6 + lift * 90), ty = h.y + dy * (dip - 6 + lift * 90), Lq = 150;
  const ex = tx + dx * Lq, ey = ty + dy * Lq;
  c.save();
  // thread from the eye up and out of frame
  const th = new Path2D(); th.moveTo(ex, ey); th.quadraticCurveTo(ex + 120, ey - 40, ex + 260, -60);
  const tb = new Path2D(); tb.moveTo(h.x, h.y); tb.quadraticCurveTo(h.x + 12, h.y - 8, tx + dx * 20, ty + dy * 20);
  c.lineCap = 'round';
  c.strokeStyle = 'rgba(20,12,5,0.25)'; c.lineWidth = 5; c.translate(8, 12); c.stroke(th); c.translate(-8, -12);
  for (const p of lift < 0.5 ? [th, tb] : [th]) { c.strokeStyle = shade(h.col, -0.3); c.lineWidth = 4.2; c.stroke(p); c.strokeStyle = h.col; c.lineWidth = 2.6; c.stroke(p); c.strokeStyle = shade(h.col, 0.35); c.lineWidth = 0.9; c.stroke(p); }
  // shadow, then the steel needle
  const nx = -dy, ny = dx, N = (s, w) => [tx + dx * s + nx * w, ty + dy * s + ny * w];
  const body = [N(0, 0), N(24, 2.6), N(Lq - 10, 3.2), N(Lq, 2), N(Lq + 3, 0), N(Lq, -2), N(Lq - 10, -3.2), N(24, -2.6)];
  c.fillStyle = 'rgba(20,12,5,0.3)'; c.fill(pathOf(tr(body, 10, 14)));
  const g = c.createLinearGradient(...N(0, -3), ...N(0, 3)); g.addColorStop(0, '#8a8d90'); g.addColorStop(0.4, '#f1f1ee'); g.addColorStop(1, '#55585c');
  c.fillStyle = g; c.fill(pathOf(body));
  c.fillStyle = '#2a221c'; c.fill(pathOf([N(Lq - 16, 0.2), N(Lq - 7, 1), N(Lq - 4, 0), N(Lq - 7, -1), N(Lq - 16, -0.2)]));
  c.restore();
}

// ── rollers ──
function roller(c, x, r) {
  const y0 = SY0 - 8, y1 = SY0 + SH + 8;
  c.save();
  const sh = c.createLinearGradient(x + r, 0, x + r + 60, 0); sh.addColorStop(0, 'rgba(8,5,2,0.55)'); sh.addColorStop(1, 'rgba(8,5,2,0)');
  c.fillStyle = sh; c.fillRect(x + r, y0 + 20, 60, y1 - y0);
  // rod ends
  for (const [ya, yb] of [[y0 - 34, y0], [y1, y1 + 34]]) {
    const g = c.createLinearGradient(x - 11, 0, x + 11, 0); g.addColorStop(0, '#3a2414'); g.addColorStop(0.35, '#8a5a32'); g.addColorStop(1, '#2a180c');
    c.fillStyle = g; c.fillRect(x - 11, ya, 22, yb - ya);
    const ky = ya < y0 ? ya : yb; c.beginPath(); c.ellipse(x, ky, 17, 9, 0, 0, TAU); c.fill();
  }
  // wound cloth
  const g = c.createLinearGradient(x - r, 0, x + r, 0);
  g.addColorStop(0, '#6f604a'); g.addColorStop(0.3, '#d8caa9'); g.addColorStop(0.45, '#e6dbc0'); g.addColorStop(0.8, '#9c8c6d'); g.addColorStop(1, '#4e4232');
  c.fillStyle = g; c.fillRect(x - r, y0, 2 * r, y1 - y0);
  // coloured edges of the wound borders showing through
  for (const [yy, cc] of [[SY0 + 18, COL.blueD], [SY0 + MAIN0, COL.blueD], [SY0 + MAIN1, COL.blueD], [SY0 + 822, COL.blueD], [SY0 + MAIN0 - 7, COL.terra], [SY0 + MAIN1 + 7, COL.terra]]) {
    c.fillStyle = cc; c.globalAlpha = 0.45; c.fillRect(x - r, yy - 1.5, 2 * r, 3); c.globalAlpha = 1; }
  c.globalCompositeOperation = 'multiply'; c.fillStyle = g; c.globalAlpha = 0.35; c.fillRect(x - r, y0, 2 * r, y1 - y0); c.globalAlpha = 1; c.globalCompositeOperation = 'source-over';
  for (const yy of [y0, y1]) { c.beginPath(); c.ellipse(x, yy, r, Math.max(3, r * 0.18), 0, 0, TAU); c.fillStyle = '#b9a987'; c.fill();
    c.strokeStyle = 'rgba(80,62,40,0.6)'; c.lineWidth = 1.2; for (let k = 0.3; k < 1; k += 0.18) { c.beginPath(); c.ellipse(x, yy, r * k, Math.max(2, r * 0.18 * k), 0, 0, TAU); c.stroke(); }
    c.fillStyle = '#5a3a20'; c.beginPath(); c.ellipse(x, yy, 11, 3, 0, 0, TAU); c.fill(); }
  c.restore();
}

// ══ frame ══
function frame(t) {
  const c = CX, cam = camX(t);
  c.drawImage(BG, 0, 0);
  // visible part of the strip: left of the unrolling roller at the start, left of the roll-up roller at the end
  const uu = eInOut(seg(t, ...T.unroll)), ru = eInOut(seg(t, ...T.rollup));
  const Ux = lerp(-cam + 58, 2020, uu), Ur = lerp(60, 52, uu);
  const Rx = lerp(SW - cam, 330, ru), Rr = 12 + 50 * Math.sqrt(ru);
  const ax = Math.max(0, -cam), bx = Math.min(1920, SW - cam, t < T.unroll[1] + 0.1 ? Ux : 1e4, t > T.rollup[0] ? Rx : 1e4);
  if (bx > ax) {
    // cast shadow on the wall
    c.fillStyle = 'rgba(8,5,2,0.45)'; c.fillRect(ax + 10, SY0 + 16, bx - ax, SH);
    c.save(); c.beginPath(); c.rect(ax, 0, bx - ax, 1080); c.clip();
    c.drawImage(STRIP, cam + ax, 0, bx - ax, SH, ax, SY0, bx - ax, SH);
    c.save(); c.beginPath(); c.rect(ax, SY0 + MAIN0 + 3, bx - ax, MAIN1 - MAIN0 - 6); c.clip();
    c.translate(-cam, SY0);
    scene1(c, t); ships(c, t); seaAndFish(c, t); scene3(c, t);
    c.restore();
    c.save(); c.translate(-cam, SY0);
    const heads = [];
    for (const [cap, [a, b]] of [[CAP1, T.cap1], [CAP2, T.cap2], [CAP3, T.cap3]]) {
      if (cap.x1 < cam - 50 || cap.x0 > cam + 1970) continue;
      const h = drawCaption(c, cap, seg(t, a, b)); if (h && t < b + 0.45) heads.push([h, seg(t, b, b + 0.45)]);
    }
    for (const [h, lift] of heads) needle(c, h, t, eIn(lift));
    c.restore();
    c.restore();
  }
  // left end rod (sewn to the start of the strip)
  if (-cam > -40) { const x = -cam - 4; c.save(); const g = c.createLinearGradient(x - 10, 0, x + 10, 0); g.addColorStop(0, '#3a2414'); g.addColorStop(0.35, '#8a5a32'); g.addColorStop(1, '#2a180c');
    c.fillStyle = g; c.fillRect(x - 10, SY0 - 40, 20, SH + 80); c.beginPath(); c.ellipse(x, SY0 - 40, 16, 8, 0, 0, TAU); c.ellipse(x, SY0 + SH + 40, 16, 8, 0, 0, TAU); c.fill(); c.restore(); }
  if (t < T.unroll[1] + 0.1 && Ux < 2100) roller(c, Ux + Ur, Ur);
  if (t > T.rollup[0] - 0.01 || SW - cam < 1920) roller(c, (t > T.rollup[0] ? Rx : SW - cam) + Rr * 0.4, t > T.rollup[0] ? Rr : 12);
  c.drawImage(LIGHT, 0, 0);
  const a = Math.max(1 - eOut(seg(t, ...T.fadeIn)), eInOut(seg(t, ...T.fade)));
  if (a > 0) { c.fillStyle = `rgba(10,7,4,${a})`; c.fillRect(0, 0, 1920, 1080); }
}

window.draw = ({ t }) => { frame(t); return cv.toDataURL('image/jpeg', 0.92).split(',')[1]; };
window.events = () => {
  const ev = [{ k: 'unroll', t: T.unroll[0], d: T.unroll[1] - T.unroll[0] }, { k: 'rollup', t: T.rollup[0], d: T.rollup[1] - T.rollup[0] }, { k: 'thunk', t: T.rollup[1] }];
  for (const [cap, [a, b]] of [[CAP1, T.cap1], [CAP2, T.cap2], [CAP3, T.cap3]]) {
    ev.push({ k: 'cap', t: a, d: b - a });
    let acc = 0; for (const s of cap) { ev.push({ k: 'stitch', t: +(a + (b - a) * acc / cap.total).toFixed(3) }); acc += s.len; }
    ev.push({ k: 'pull', t: b });
  }
  for (let tt = 0.3; tt < 3.2; tt += Math.PI / 5.2 / 2) ev.push({ k: 'hoof', t: +tt.toFixed(3) });
  ev.push({ k: 'point', t: T.point[0] + 0.2 }, { k: 'sea', t: 2.9, d: 4.6 }, { k: 'creak', t: 4.2 }, { k: 'creak', t: 5.5 });
  T.toast.forEach(tt => ev.push({ k: 'toast', t: tt + 0.35 }));
  ev.push({ k: 'serve', t: T.serve[1] - 0.2 }, { k: 'fade', t: T.fade[0] });
  return ev.sort((a, b) => a.t - b.t);
};
window.ready = (async () => { bakeWool(); bakeLinenTile(); bakeBG(); bakeStrip(); })();
