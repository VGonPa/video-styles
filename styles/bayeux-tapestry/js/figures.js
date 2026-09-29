// figures.js · profile figures, horse, ship, border creatures, trees and halls, all built from laid wool + stem-stitch outlines
// All figures face right in local coords (flip mirrors them); y = 0 is the ground line.

// ── a person in profile: knee-length tunic, cross-gartered hose, unfilled linen face ──
const HIP_Y = -135;
function legPts([a, k], dx) {
  const h = [dx, HIP_Y], kn = [h[0] + 66 * Math.sin(a), h[1] + 66 * Math.cos(a)], b = a - k;
  return [h, kn, [kn[0] + 62 * Math.sin(b), kn[1] + 62 * Math.cos(b)], b];
}
function armPts([a, e], sh) {
  const el = [sh[0] + 48 * Math.sin(a), sh[1] + 48 * Math.cos(a)], b = a + e;
  return [sh, el, [el[0] + 42 * Math.sin(b), el[1] + 42 * Math.cos(b)], b];
}
function handPoly(w, b, open) {
  const d = [Math.sin(b), Math.cos(b)], p = [d[1], -d[0]];
  const P = (t, n) => [w[0] + d[0] * t + p[0] * n, w[1] + d[1] * t + p[1] * n];
  return cr(open ? [P(-2, 5.5), P(5, 7), P(9, 12), P(12, 11), P(11, 5), P(19, 4), P(21, 0), P(18, -4.5), P(8, -6), P(-2, -5.5)]
                 : [P(-2, 5.5), P(6, 8), P(11, 8.5), P(12, 5), P(16, 3), P(17, -2), P(13, -6), P(5, -6.5), P(-2, -5.5)], true, 3);
}
function leg(c, L, col, ol) {
  const [h, kn, an, b] = L;
  const P = thick([h, kn, an], [24, 15, 11]);
  piece(c, P, col, 90 - (b * 180 / Math.PI), ol, 3.6, { gap: 17 });
  // cross-gartering on the shin
  const nx = Math.cos(b), ny = -Math.sin(b), dx = Math.sin(b), dy = Math.cos(b);
  for (const f of [0.22, 0.47, 0.72]) {
    const cx = kn[0] + (an[0] - kn[0]) * f, cy = kn[1] + (an[1] - kn[1]) * f, w = 7.2 - f * 2;
    stem(c, [[cx - nx * w - dx * 6, cy - ny * w - dy * 6], [cx + nx * w + dx * 6, cy + ny * w + dy * 6]], COL.mustardL, 2.6, 1, 6);
  }
  const sh = [[-7, -9], [6, -10], [23, 1], [22, 7], [-8, 7]].map(([x, y]) => [an[0] + x, an[1] + y]);
  piece(c, cr(sh, true, 3), COL.blueD, 0, shade(COL.blueD, -0.3), 3, { bars: false });
}
function arm(c, A, col, ol, o = {}) {
  const [s, el, wr, b] = A;
  piece(c, thick([s, el, wr], [21, 16, 13]), col, 90 - (b * 180 / Math.PI), ol, 3.6, { gap: 16 });
  if (o.hold) o.hold(c, wr, b);
  bareP(c, handPoly(wr, b, o.open), ol, 3);
  if (o.over) o.over(c, wr, b);
}
function head(c, hc, o) {
  const H = [[-13, 20], [-21, 8], [-23, -6], [-17, -19], [-5, -26], [8, -25], [17, -17], [20, -8], [21, -3], [28, 6], [27, 8.5], [21, 10], [21.5, 13], [19.5, 15], [21, 17.5], [19.5, 22], [14, 26], [6, 26]];
  c.save(); c.translate(hc[0], hc[1]); c.scale(1.14, 1.14); hc = [0, 0];
  const P = cr(H.map(([x, y]) => [hc[0] + x, hc[1] + y]), true, 4);
  bareP(c, P, o.ol, 3.8);
  const hair = o.hood ? [[19, -11], [10, -25], [-6, -30], [-20, -21], [-26, -4], [-22, 14], [-14, 24], [-8, 14], [-5, -2], [4, -11], [16, -8]]
                      : [[16, -15], [8, -24], [-6, -27], [-19, -19], [-24, -4], [-21, 10], [-14, 18], [-9, 8], [-6, -2], [1, -10], [11, -13]];
  piece(c, cr(hair.map(([x, y]) => [hc[0] + x, hc[1] + y]), true, 3), o.hair, o.hood ? 90 : 10, o.ol, 3.2, { gap: 14 });
  stem(c, [[hc[0] + 11, hc[1] - 5], [hc[0] + 15.5, hc[1] - 4.5]], o.ol, 4, 1, 5);   // eye
  stem(c, ell(hc[0] - 3, hc[1] + 3, 3.5, 5, -1.6, 1.8, 6), o.ol, 2.6, 1, 5);          // ear
  if (o.beard) piece(c, cr([[14, 12], [21, 16], [20, 23], [13, 27], [3, 25], [-8, 17], [-4, 10], [6, 16]].map(([x, y]) => [hc[0] + x, hc[1] + y]), true, 3), o.hair, 90, o.ol, 3, { bars: false });
  else stem(c, [[hc[0] + 22, hc[1] + 11], [hc[0] + 16, hc[1] + 13], [hc[0] + 11, hc[1] + 12]], o.hair, 3, 1, 5);   // moustache
  c.restore();
}
// o: { s, flip, tunic, hem, hose, hair, beard, hood, legs:[front,back] [thighAngle, kneeBend], arms:[front,back] [shoulderAngle, elbowBend], hold, over, open, upper }
function human(c, x, y, o) {
  const s = o.s || 1, ol = o.ol || COL.blueD; c.save(); c.translate(x, y); c.scale(o.flip ? -s : s, s);
  const legs = o.legs || [[0.1, 0.04], [-0.1, 0.04]], arms = o.arms || [[0.15, 0.25], [-0.12, 0.2]];
  const shF = [7, -203], shB = [-3, -205];
  arm(c, armPts(arms[1], shB), shade(o.tunic, -0.18), ol, { hold: o.holdB, over: o.overB, open: o.openB });
  if (!o.upper) { leg(c, legPts(legs[1], -6), shade(o.hose, -0.2), ol); leg(c, legPts(legs[0], 5), o.hose, ol); }
  bareP(c, [[-7, -205], [-8, -232], [11, -234], [10, -208]], ol, 3.4);   // neck
  const T = cr([[-7, -214], [-19, -205], [-23, -182], [-18, -150], [-25, -122], [-35, -91], [-6, -86], [20, -88], [36, -94], [26, -122], [19, -151], [23, -180], [17, -207], [7, -216]], true, 4);
  piece(c, T, o.tunic, 90, ol, 4, { gap: 18 });
  const hem = cr([[-30, -107], [-35, -91], [-6, -86], [20, -88], [36, -94], [31, -109], [0, -102]], true, 4);
  piece(c, hem, o.hem || COL.mustard, 0, ol, 3, { bars: false });
  for (let i = 0; i < 6; i++) knot(c, -24 + i * 10.5, -96 + (i > 2 ? -1 : 0), ol, 2);
  stem(c, [[-19, -150], [0, -147], [19, -151]], o.hem || COL.mustard, 4, 1, 7);   // belt
  piece(c, cr([[-8, -214], [0, -210], [9, -214], [11, -206], [0, -202], [-10, -207]], true, 3), o.hem || COL.mustard, 0, ol, 2.6, { bars: false });   // collar
  head(c, [7, -254], { ol, hair: o.hair || COL.terraD, beard: o.beard, hood: o.hood });
  arm(c, armPts(arms[0], shF), o.tunic, ol, { hold: o.hold, over: o.over, open: o.open });
  c.restore();
}
function walkPose(ph, amp = 1) {
  const s = Math.sin(ph), s2 = Math.sin(ph + Math.PI);
  return { legs: [[0.36 * s * amp, 0.08 + 0.42 * Math.max(0, Math.sin(ph + 1.1)) * amp], [0.36 * s2 * amp, 0.08 + 0.42 * Math.max(0, Math.sin(ph + 1.1 + Math.PI)) * amp]],
           bob: -3 * Math.abs(Math.cos(ph)) * amp };
}

// ── horse: long body, arched neck, slim legs; far legs in a second wool (as on the frieze) ──
const HORSE = cr([[42, -166], [-20, -157], [-80, -166], [-110, -150], [-114, -118], [-100, -98], [-70, -90], [0, -86], [50, -92], [80, -103], [96, -128],
  [108, -156], [128, -186], [148, -180], [168, -170], [184, -174], [188, -186], [180, -200], [156, -232], [142, -238], [138, -260], [128, -242], [116, -236], [96, -214], [70, -186]], true, 5);
function horseLeg(c, top, a, k, col, ol) {
  const kn = [top[0] + 46 * Math.sin(a), top[1] + 46 * Math.cos(a)], b = a - k, an = [kn[0] + 44 * Math.sin(b), kn[1] + 44 * Math.cos(b)];
  piece(c, thick([top, kn, an], [26, 13, 9]), col, 90 - b * 57.3, ol, 3.2, { gap: 16 });
  const hf = [[-5, -3], [7, -3], [10, 7], [-6, 7]].map(([x, y]) => [an[0] + x * Math.cos(b) + y * Math.sin(b) * 0.3, an[1] + y]);
  piece(c, hf, COL.blueD, 0, shade(COL.blueD, -0.3), 2.6, { bars: false });
}
function horse(c, x, y, o) {
  const s = o.s || 1, ol = o.ol || COL.blueD, ph = o.ph || 0, amp = o.walk || 0;
  c.save(); c.translate(x, y); c.scale(o.flip ? -s : s, s);
  const lg = i => { const p = ph + [0, Math.PI, Math.PI * 0.5, Math.PI * 1.5][i]; return [0.3 * Math.sin(p) * amp, (0.1 + 0.55 * Math.max(0, Math.sin(p + 1.2))) * amp]; };
  // far legs
  let q = lg(1); horseLeg(c, [60, -104], q[0] + 0.04, q[1], o.col2, ol);
  q = lg(3); horseLeg(c, [-86, -108], q[0] - 0.12, q[1] - 0.2, o.col2, ol);
  // tail
  for (let i = 0; i < 4; i++) stem(c, cr([[-110, -150], [-128 - i * 3, -130], [-134 - i * 4, -95], [-126 - i * 5, -58 + i * 6]], false, 5), i % 2 ? o.mane : shade(o.mane, -0.2), 5, 1, 8);
  piece(c, HORSE, o.col, 8, ol, 4.2, { gap: 20 });
  // mane along the crest
  const crest = cr([[136, -246], [116, -234], [95, -212], [70, -184], [44, -165], [62, -170], [92, -196], [112, -216], [132, -232]], true, 3);
  piece(c, crest, o.mane, 60, ol, 3, { bars: false });
  // saddle cloth
  if (o.saddle) piece(c, cr([[-30, -162], [30, -168], [36, -130], [-26, -122]], true, 3), o.saddle, 90, ol, 3.2);
  knot(c, 150, -220, ol, 3.4);                                     // eye
  stem(c, ell(178, -186, 4, 3, -2.5, 1.5, 5), ol, 2.4, 1, 4);    // nostril
  // bridle and reins
  stem(c, [[136, -236], [154, -204], [172, -178]], COL.terraD, 3.2, 1, 6);
  stem(c, [[156, -208], [178, -196], [184, -184]], COL.terraD, 3, 1, 6);
  if (o.rein) stem(c, cr([[174, -180], [(174 + o.rein[0]) / 2, Math.max(-180, o.rein[1]) + 26], o.rein], false, 6), COL.terraD, 3, 1, 7);
  q = lg(0); horseLeg(c, [72, -102], q[0], q[1], o.col, ol);
  q = lg(2); horseLeg(c, [-78, -106], q[0] - 0.12, q[1] - 0.2, o.col, ol);
  c.restore();
}

// ── longship: coloured strakes, dragon prow, striped square sail ──
function ship(c, x, y, o) {
  const ol = COL.blueD; c.save(); c.translate(x, y); c.rotate(o.rot || 0);
  const gun = xx => -64 + 8 * (1 - (xx / 245) ** 2), keel = xx => 14 - 56 * Math.pow(Math.abs(xx) / 250, 2.4);
  // mast, sail, rigging
  const bill = o.bill || 0;
  stem(c, [[4, -372], [272, -132]], COL.greenD, 3, 1, 8); stem(c, [[4, -372], [-262, -122]], COL.greenD, 3, 1, 8);
  piece(c, thick([[0, gun(0)], [0, -372]], [12, 9]), COL.terraD, 90, ol, 3);
  const top = -342, bot = -176, xl = -118, xr = 124;
  const edgeR = u => [xr + bill * Math.sin(Math.PI * u) * 34, lerp(top, bot, u)], edgeL = u => [xl + bill * Math.sin(Math.PI * u) * 14, lerp(top, bot, u)];
  const cols = [COL.terra, COL.mustard, COL.blueL, COL.sage, COL.terra, COL.mustard];
  for (let i = 0; i < 6; i++) {
    const f0 = i / 6, f1 = (i + 1) / 6, P = [];
    for (let k = 0; k <= 8; k++) { const u = k / 8, L = edgeL(u), R = edgeR(u); P.push([lerp(L[0], R[0], f0), lerp(L[1], R[1], f0) + Math.sin(Math.PI * f0) * 10 * u]); }
    for (let k = 8; k >= 0; k--) { const u = k / 8, L = edgeL(u), R = edgeR(u); P.push([lerp(L[0], R[0], f1), lerp(L[1], R[1], f1) + Math.sin(Math.PI * f1) * 10 * u]); }
    laid(c, P, cols[i], 90, { gap: 22, shadow: i === 0 });
  }
  const SP = []; for (let k = 0; k <= 8; k++) SP.push(edgeL(k / 8)); for (let k = 0; k <= 12; k++) { const f = k / 12; const L = edgeL(1), R = edgeR(1); SP.push([lerp(L[0], R[0], f), lerp(L[1], R[1], f) + Math.sin(Math.PI * f) * 10]); } for (let k = 8; k >= 0; k--) SP.push(edgeR(k / 8));
  outline(c, SP, ol, 4);
  stem(c, [[xl - 12, top], [xr + 14, top]], COL.terraD, 6, 1, 9);   // yard
  // crew and cargo (behind the hull)
  if (o.crew) o.crew(gun);
  // posts: stern curl and dragon prow
  piece(c, thick(cr([[-232, -58], [-262, -86], [-284, -128], [-290, -164], [-276, -186], [-258, -180], [-262, -164]], false, 5), u => 22 - 12 * u), COL.mustard, 30, ol, 3.4, { gap: 15 });
  piece(c, thick(cr([[232, -58], [262, -92], [280, -140], [286, -178]], false, 5), u => 22 - 8 * u), COL.mustard, 150, ol, 3.4, { gap: 15 });
  const dh = cr([[276, -176], [282, -200], [298, -214], [318, -210], [336, -200], [322, -194], [334, -186], [316, -186], [300, -180], [296, -168]], true, 3);
  piece(c, dh, COL.terra, 0, ol, 3.4, { bars: false });
  piece(c, [[286, -204], [282, -226], [296, -212]], COL.mustardL, 0, ol, 2.6, { bars: false });   // horn
  knot(c, 306, -202, ol, 2.8);
  // hull strakes
  const HP = []; for (let k = 0; k <= 30; k++) { const xx = -245 + 490 * k / 30; HP.push([xx, gun(xx)]); } for (let k = 30; k >= 0; k--) { const xx = -245 + 490 * k / 30; HP.push([xx, keel(xx)]); }
  const sc = [COL.terra, COL.mustard, COL.blue, COL.sage];
  for (let i = 0; i < 4; i++) {
    const P = [];
    for (let k = 0; k <= 30; k++) { const xx = -245 + 490 * k / 30; P.push([xx, lerp(gun(xx), keel(xx), i / 4)]); }
    for (let k = 30; k >= 0; k--) { const xx = -245 + 490 * k / 30; P.push([xx, lerp(gun(xx), keel(xx), (i + 1) / 4) + 0.5]); }
    laid(c, P, sc[i], 0, { gap: 24, shadow: i === 3 });
    if (i) { const L = []; for (let k = 0; k <= 30; k++) { const xx = -245 + 490 * k / 30; L.push([xx, lerp(gun(xx), keel(xx), i / 4)]); } stem(c, L, ol, 2.6, 1, 8); }
  }
  outline(c, HP, ol, 4.4);
  // shields along the rail
  if (o.shields) for (let xx = -180, i = 0; xx <= 180; xx += 34, i++) {
    const cc = [COL.mustard, COL.terra, COL.blueL][i % 3], sp = ell(xx, gun(xx) - 2, 15, 15, 0, TAU, 20);
    piece(c, sp, cc, 90, ol, 3, { bars: false }); knot(c, xx, gun(xx) - 2, ol, 3.4);
  }
  if (o.front) o.front(gun);
  c.restore();
}

// ── sea: wave bands with stitched crests ──
function waveY(x, row, t) { return 600 + row * 30 + 7 * Math.sin(x / 26 - t * 2.4 + row * 1.7) + 4 * Math.sin(x / 71 + t * 1.1 + row); }
function waves(c, x0, x1, rows, t) {
  const cols = [COL.blueL, COL.sage, COL.blue, COL.green, COL.blueD];
  for (const row of rows) {
    const top = [], bot = [], xa = x0 + (3 - row) * 16, xb = x1 - (3 - row) * 12;
    for (let x = xa; x <= xb; x += 16) { top.push([x, waveY(x, row, t)]); bot.push([x, waveY(x, row + 1, t) + 2]); }
    laid(c, top.concat(bot.reverse()), cols[row], 0, { gap: 26, shadow: false });
    stem(c, top, row % 2 ? COL.blueD : COL.greenD, 4, 1, 9);
  }
}
function fish(c, x, y, s, col, flip) {
  c.save(); c.translate(x, y); c.scale(flip ? -s : s, s);
  const B = cr([[-26, 0], [-8, -12], [14, -10], [28, 0], [14, 9], [-8, 10]], true, 4);
  piece(c, [[-24, 0], [-40, -12], [-37, 0], [-40, 12]], shade(col, -0.2), 0, COL.blueD, 2.6, { bars: false });
  piece(c, B, col, 0, COL.blueD, 3, { bars: false }); knot(c, 17, -3, COL.blueD, 2); stem(c, [[5, -9], [2, 0], [5, 8]], COL.blueD, 2.4, 1, 5);
  c.restore();
}

// ── border creatures ──
function bird(c, x, y, s, col, col2, flip) {
  const ol = COL.blueD; c.save(); c.translate(x, y); c.scale(flip ? -s : s, s);
  stem(c, [[-4, -22], [-7, -2], [-12, 0]], ol, 2.6, 1, 5); stem(c, [[6, -22], [6, -2], [11, 0]], ol, 2.6, 1, 5);
  piece(c, cr([[-24, -30], [-46, -50], [-40, -30], [-48, -18]], true, 2), col2, 30, ol, 2.8, { bars: false });   // tail
  piece(c, cr([[-28, -32], [-10, -48], [16, -46], [26, -56], [30, -70], [40, -70], [46, -66], [38, -62], [34, -48], [26, -30], [6, -20], [-18, -22]], true, 3), col, 0, ol, 3.2, { gap: 15 });
  piece(c, cr([[-18, -34], [2, -46], [16, -40], [4, -30]], true, 3), col2, 0, ol, 2.6, { bars: false });   // wing
  knot(c, 36, -65, ol, 2);
  c.restore();
}
function beast(c, x, y, s, col, col2, flip) {
  const ol = COL.blueD; c.save(); c.translate(x, y); c.scale(flip ? -s : s, s);
  const lg = (p, a, cc) => piece(c, thick([p, [p[0] + 18 * Math.sin(a), p[1] + 18], [p[0] + 18 * Math.sin(a) + 2, -1]], [11, 7, 6]), cc, 90, ol, 2.6, { bars: false });
  lg([-26, -30], -0.3, col2); lg([22, -30], 0.3, col2);
  stem(c, cr([[-36, -40], [-50, -52], [-44, -74], [-30, -76]], false, 4), col2, 4, 1, 6);   // tail curling over
  piece(c, cr([[-30, -76], [-24, -84], [-34, -84]], true, 2), col2, 0, ol, 2.4, { bars: false });
  piece(c, cr([[-38, -34], [-32, -52], [0, -50], [24, -56], [36, -44], [30, -28], [0, -26], [-30, -24]], true, 3), col, 0, ol, 3.2, { gap: 15 });
  piece(c, cr([[22, -50], [26, -70], [38, -76], [50, -70], [54, -60], [44, -52], [34, -46]], true, 3), col2, 70, ol, 3, { bars: false });   // maned head
  piece(c, [[34, -74], [38, -86], [44, -76]], col, 0, ol, 2.4, { bars: false });
  knot(c, 45, -65, ol, 2);
  lg([-30, -30], 0.2, col); lg([26, -30], -0.2, col);
  c.restore();
}

// ── scene furniture ──
function tree(c, x, y, s, o = {}) {
  const ol = COL.blueD; c.save(); c.translate(x, y); c.scale(s, s);
  const br = [
    [[0, -150], [-40, -190], [-90, -170], [-100, -230], [-60, -262]],
    [[0, -150], [40, -190], [90, -170], [100, -230], [60, -262]],
    [[0, -220], [-30, -270], [-10, -310], [26, -300], [30, -340]],
    [[0, -220], [30, -270], [10, -310], [-26, -300], [-30, -340]],
    [[0, -100], [-50, -110], [-60, -80], [-90, -95]],
    [[0, -100], [50, -110], [60, -80], [90, -95]],
  ];
  const lf = [[-60, -262], [60, -262], [30, -340], [-30, -340], [-90, -95], [90, -95]];
  for (const b of br) piece(c, thick(cr(b, false, 5), u => 16 - 8 * u), o.b || COL.sage, 90, ol, 3, { bars: false });
  piece(c, thick([[0, 0], [0, -120], [0, -236]], [34, 22, 12]), o.t || COL.terra, 90, ol, 3.6, { gap: 18 });
  lf.forEach(([lx, ly], i) => {
    c.save(); c.translate(lx, ly); c.rotate([-0.6, 0.6, 0.2, -0.2, -1.6, 1.6][i]);
    const L = cr([[0, 6], [-22, -8], [-24, -30], [-10, -40], [-6, -52], [0, -46], [6, -52], [10, -40], [24, -30], [22, -8]], true, 3);
    piece(c, L, i % 2 ? (o.l1 || COL.mustard) : (o.l2 || COL.green), 90, ol, 3, { bars: false });
    stem(c, [[0, 2], [0, -40]], ol, 2.4, 1, 6);
    c.restore();
  });
  c.restore();
}
function tiles(c, x0, x1, y0, y1, col) {   // rows of stitched roof scales
  for (let y = y0 + 12, r = 0; y < y1; y += 14, r++) {
    const pts = []; for (let x = x0 + (r % 2) * 9; x < x1; x += 18) pts.push(...ell(x + 9, y - 6, 9, 7, Math.PI, 0, 5));
    stem(c, pts.filter(p => p[0] > x0 && p[0] < x1), col, 2.6, 1, 6);
  }
}
function hall(c, x, y) {   // arcaded hall with a scale-tiled roof and a small turret
  const ol = COL.blueD; c.save(); c.translate(x, y);
  const X = [0, 130, 260, 390];
  piece(c, [[-20, 0], [410, 0], [410, 14], [-20, 14]], COL.terraD, 0, ol, 3, { bars: false });
  piece(c, cr([[-18, -330], [410, -330], [410, -284], [-18, -284]], true, 1), COL.blueL, 0, ol, 3.4);
  for (let i = 0; i < 3; i++) {
    const a = X[i], b = X[i + 1], m = (a + b) / 2;
    const wall = [[a, -284], [b, -284], [b, -250], ...ell(m, -250, (b - a) / 2 - 8, 56, 0, -Math.PI, 12), [a, -250]];
    piece(c, wall, COL.blueL, 0, ol, 3, { bars: false });
    stem(c, ell(m, -250, (b - a) / 2 - 8, 56, 0, -Math.PI, 14), COL.terra, 5, 1, 8);
  }
  X.forEach(xx => { piece(c, [[xx - 8, 0], [xx + 8, 0], [xx + 7, -250], [xx - 7, -250]], COL.mustard, 90, ol, 3, { gap: 16 });
    piece(c, [[xx - 14, -250], [xx + 14, -250], [xx + 10, -262], [xx - 10, -262]], COL.terra, 0, ol, 2.8, { bars: false }); });
  const roof = [[-40, -330], [430, -330], [390, -410], [0, -410]];
  piece(c, roof, COL.terra, 0, ol, 4); tiles(c, -30, 420, -410, -332, COL.terraD);
  // turret with a domed cap
  piece(c, [[160, -410], [230, -410], [230, -452], [160, -452]], COL.sage, 90, ol, 3.4);
  stem(c, ell(195, -432, 9, 12, 0, TAU, 12), ol, 3, 1, 6);
  piece(c, [[150, -452], ...ell(195, -452, 45, 34, Math.PI, TAU, 12), [240, -452]], COL.mustard, 0, ol, 3.4);
  knot(c, 195, -492, COL.terraD, 6);
  // beast-head finials at the roof ends
  for (const [fx, fl] of [[-40, 1], [430, -1]]) {
    const H = cr([[0, 0], [-8 * fl, -20], [-2 * fl, -34], [12 * fl, -30], [22 * fl, -34], [14 * fl, -24], [8 * fl, -10]], true, 3).map(([a, b]) => [fx + a, -330 + b]);
    piece(c, H, COL.mustard, 0, ol, 2.8, { bars: false });
  }
  c.restore();
}
function canopy(c, x0, x1, y) {   // feast hall: two columns and a tiled roof over the table
  const ol = COL.blueD;
  for (const xx of [x0 + 20, x1 - 20]) {
    piece(c, [[xx - 10, y], [xx + 10, y], [xx + 9, y - 380], [xx - 9, y - 380]], COL.sage, 90, ol, 3.2, { gap: 16 });
    piece(c, [[xx - 18, y - 380], [xx + 18, y - 380], [xx + 13, y - 394], [xx - 13, y - 394]], COL.terra, 0, ol, 2.8, { bars: false });
    piece(c, [[xx - 16, y], [xx + 16, y], [xx + 12, y - 12], [xx - 12, y - 12]], COL.terra, 0, ol, 2.8, { bars: false });
  }
  const mid = (x0 + x1) / 2;
  const R = [[x0 - 20, y - 394], [x1 + 20, y - 394], [x1 - 30, y - 440], [mid + 60, y - 452], [mid - 60, y - 452], [x0 + 30, y - 440]];
  piece(c, R, COL.terra, 0, ol, 4); tiles(c, x0, x1, y - 450, y - 396, COL.terraD);
  piece(c, [[mid - 50, y - 450], ...ell(mid, y - 450, 50, 36, Math.PI, TAU, 12), [mid + 50, y - 450]], COL.mustard, 0, ol, 3.4);
  knot(c, mid, y - 492, COL.terraD, 6);
  stem(c, [[x0 + 30, y - 382], [x1 - 30, y - 382]], COL.mustard, 5, 1, 9);
}
function ground(c, x0, x1, y, col = COL.greenD) {
  const pts = []; for (let x = x0; x <= x1; x += 14) pts.push([x, y + 3 * Math.sin(x / 47) + 2 * Math.sin(x / 13)]);
  stem(c, pts, col, 4.4, 1, 9);
}
