// figures.js · composite-profile people (profile head + frontal eye, frontal shoulders, profile legs), oxen, props
// Human units: u = H/19 (the classic 18-square canon to the hairline); origin at the ground under the hips, facing right, y down.

// walking feet for a stride S (u), phase in [0,1): stance 60 %, swing 40 % with a small lift
function walkFeet(ph, S) {
  const f = p => { p = ((p % 1) + 1) % 1; if (p < 0.6) return [S / 2 - S * (p / 0.6), 0, 0];
    const q = (p - 0.6) / 0.4; return [-S / 2 + S * eInOut(q), -1.1 * Math.sin(Math.PI * q), -0.25 * Math.sin(Math.PI * q)]; };
  return { B: f(ph), F: f(ph + 0.5) };
}

const HEAD_FACE = [[0.55, -1.3], [1.02, -0.8], [1.14, -0.28], [1.1, -0.1], [1.56, 0.42], [1.2, 0.52], [1.28, 0.7], [1.12, 0.8], [1.22, 0.93], [1.02, 1.12], [0.98, 1.3],
  [0.35, 1.34], [-0.25, 0.95], [-0.85, 0.2], [-0.85, -0.9], [-0.2, -1.42]];
const WIG_SHORT = [[1.0, -0.66], [0.96, -1.25], [0.3, -1.68], [-0.62, -1.56], [-1.22, -0.95], [-1.3, 0.1], [-1.02, 0.9], [-0.5, 1.02], [-0.3, 0.4], [0.02, -0.2], [0.55, -0.5]];
const WIG_LONG = [[1.0, -0.66], [0.96, -1.3], [0.3, -1.74], [-0.72, -1.62], [-1.42, -0.9], [-1.62, 0.6], [-1.62, 3.3], [-0.95, 3.55], [-0.62, 1.7], [-0.25, 1.35], [-0.05, 3.25], [0.55, 3.38], [0.45, 1.3], [0.2, 0.35], [0.2, -0.28], [0.58, -0.5]];

function hand(w, ang, flip, fist, skin) {
  X.save(); X.translate(w[0], w[1]); X.rotate(ang); X.scale(1, flip);
  if (fist) {
    smooth([[-0.1, -0.42], [0.6, -0.52], [1.0, -0.25], [1.02, 0.25], [0.7, 0.48], [-0.1, 0.42]]); paint(skin);
    X.beginPath(); X.moveTo(0.35, -0.45); X.quadraticCurveTo(0.75, -0.1, 0.95, -0.05); X.strokeStyle = COL.ink; X.lineWidth = LW * 0.7; X.stroke();
  } else {
    smooth([[-0.1, -0.38], [0.8, -0.44], [1.5, -0.3], [1.62, 0.02], [1.45, 0.3], [0.8, 0.42], [-0.1, 0.4]]); paint(skin);
    smooth([[0.45, -0.36], [0.9, -0.86], [1.18, -0.74], [0.9, -0.3]]); paint(skin, LW * 0.85);
  }
  X.restore();
}

// o: {x,y,H, lean, bob, fB,fF: [x,y,footAngle] (u, ankle-ground pos), hB,hF: [x,y] hand targets (u), eB,eF: elbow side,
//     fistB,fistF, flipB,flipF, skin, female, collar, propB(w,ang), propF(w,ang), onHead(topPoint, dir), headTilt}
function human(o) {
  const u = o.H / 19;
  X.save(); X.translate(o.x, o.y); X.scale(u, u); const LW0 = LW; LW = 2.5 / u;
  const skin = o.skin || COL.skinM, lean = o.lean || 0;
  const dir = [Math.sin(lean), -Math.cos(lean)], p = [Math.cos(lean), Math.sin(lean)];
  const Hc = [o.hipX || 0, -10.2 + (o.bob || 0)];
  const W = add2(Hc, dir, 1.3), S = add2(Hc, dir, 5.9);
  const Sf = add2(add2(S, p, 2.05), dir, -0.62), Sb = add2(add2(S, p, -1.95), dir, -0.62);
  const arm = (sh, hT, e, fist, flip, prop) => {
    const el = ik(sh, hT, 3.9, 3.35, e), w = hT;
    const d = Math.hypot(hT[0] - sh[0], hT[1] - sh[1]); const wr = d > 7.2 ? add2(sh, [(hT[0] - sh[0]) / d, (hT[1] - sh[1]) / d], 7.24) : w;
    limb([sh, el, wr], [0.82, 0.54, 0.38], skin);
    const ang = Math.atan2(wr[1] - el[1], wr[0] - el[0]);
    if (prop) prop(wr, ang);
    hand(wr, ang, flip || 1, fist, skin);
  };
  const leg = (hip, f) => {
    const A = [f[0], f[1] - 0.72];
    const k = ik(hip, A, 5.0, 4.85, -1);
    limb([hip, [lerp(hip[0], k[0], 0.5), lerp(hip[1], k[1], 0.5)], k, [lerp(k[0], A[0], 0.3) - 0.12, lerp(k[1], A[1], 0.3)], A], [1.12, 0.92, 0.6, 0.66, 0.4], skin);
    X.save(); X.translate(A[0], A[1]); X.rotate(f[2] || 0);
    smooth([[-0.5, -0.35], [-0.66, 0.4], [-0.5, 0.72], [2.35, 0.72], [2.5, 0.52], [2.0, 0.2], [0.5, -0.35]]); paint(skin);
    X.restore();
  };
  if (o.propBack) o.propBack();
  if (!o.bFront) arm(Sb, o.hB, o.eB || 1, o.fistB, o.flipB, o.propB);
  leg(add2(Hc, [-0.45, 0.3]), o.fB); leg(add2(Hc, [0.5, 0.3]), o.fF);
  // torso: broad frontal shoulders tapering to the waist, chest in profile on the front edge
  const T = (a, b) => add2(add2(S, p, a), dir, b);
  smooth([T(-2.3, 0.25), T(0, 0.45), T(2.3, 0.25), T(2.75, -0.5), T(2.15, -2.1), T(1.75, -3.3), add2(W, p, 1.3), add2(W, p, -1.3), T(-1.7, -3.2), T(-2.65, -0.6)]);
  paint(skin);
  X.beginPath(); const nip = T(2.0, -2.15); X.arc(nip[0], nip[1], 0.13, 0, TAU); X.fillStyle = COL.ink; X.fill();
  if (!o.female) {   // pleated white kilt
    const hb = [W[0] - 1.9, -7.0], hf = [W[0] + 2.05, -6.9];
    poly([add2(add2(W, p, -1.32), dir, 0.35), add2(add2(W, p, 1.32), dir, 0.35), hf, hb]); paint(COL.white);
    X.save(); poly([add2(add2(W, p, -1.32), dir, 0.35), add2(add2(W, p, 1.32), dir, 0.35), hf, hb]); X.clip();
    X.strokeStyle = 'rgba(28,23,19,0.55)'; X.lineWidth = LW * 0.55;
    for (let i = 1; i <= 4; i++) { X.beginPath(); const a = add2(W, p, 1.1 - i * 0.18); X.moveTo(a[0], a[1]); X.lineTo(hf[0] - i * 0.75, hf[1]); X.stroke(); }
    X.restore();
    line(add2(add2(W, p, -1.32), dir, -0.1), add2(add2(W, p, 1.32), dir, -0.1), LW * 1.3, COL.red);
  } else {           // sheath dress, slightly sheer, from the shoulders to mid-calf
    const hemY = -2.2, hb = [Hc[0] - 1.5, hemY], hf = [Hc[0] + 1.9, hemY];
    X.globalAlpha = 0.86;
    poly([T(-2.2, 0.15), T(2.2, 0.15), T(2.6, -0.55), T(2.05, -2.2), T(1.6, -3.4), add2(W, p, 1.25), [Hc[0] + 1.55, -7.6], hf, hb, [Hc[0] - 1.45, -7.6], add2(W, p, -1.25), T(-1.65, -3.3), T(-2.5, -0.6)]);
    paint(COL.white); X.globalAlpha = 1;
    line([hb[0] + 0.1, hemY], [hf[0] - 0.1, hemY], LW * 1.2, COL.red);
  }
  // neck, head
  const n0 = add2(S, p, 0.15), n1 = add2(S, p, 1.35);
  poly([add2(n0, dir, 0.2), add2(n1, dir, 0.2), add2(add2(S, p, 1.45), dir, 1.5), add2(add2(S, p, 0.25), dir, 1.6)]); paint(skin);
  if (o.collar) {   // broad bead collar: concentric mineral bands
    const c = add2(S, p, 0.75); X.save(); X.translate(c[0], c[1]); X.rotate(lean);
    const bands = [COL.blue, COL.red, COL.green, COL.gold];
    for (let i = bands.length - 1; i >= 0; i--) { X.beginPath(); X.ellipse(0, -0.25, 2.1 + i * 0.35, 0.8 + i * 0.42, 0, 0, Math.PI); X.closePath(); paint(bands[i], LW * 0.7); }
    X.restore();
  }
  const hd = add2(add2(S, dir, 2.5), p, 0.72);
  X.save(); X.translate(hd[0], hd[1]); X.rotate(lean * 0.55 + (o.headTilt || 0));
  poly(HEAD_FACE); paint(skin);
  // eye drawn frontally in the profile head
  smooth([[0.3, 0.0], [0.62, -0.17], [0.94, -0.01], [0.62, 0.11]]); paint(COL.white, LW * 0.75);
  X.beginPath(); X.arc(0.64, -0.03, 0.11, 0, TAU); X.fillStyle = COL.ink; X.fill();
  line([0.3, 0.0], [-0.02, -0.06], LW * 0.9); line([0.3, -0.34], [0.98, -0.32], LW * 0.8);
  if (!o.female) { smooth(WIG_SHORT); paint(COL.ink, LW * 0.6); X.beginPath(); X.ellipse(-0.18, 0.28, 0.26, 0.42, 0.15, 0, TAU); paint(skin, LW * 0.8); }
  else { smooth(WIG_LONG); paint(COL.ink, LW * 0.6); line([0.95, -0.95], [-1.45, -0.55], LW * 1.3, COL.red); }
  X.restore();
  const top = add2(hd, dir, 1.72);
  if (o.bFront) arm(Sb, o.hB, o.eB || 1, o.fistB, o.flipB, o.propB);
  arm(Sf, o.hF, o.eF || 1, o.fistF, o.flipF, o.propF);
  if (o.propTop) o.propTop();
  LW = LW0; X.restore();
  if (o.onHead) o.onHead([o.x + top[0] * u, o.y + top[1] * u], lean);
  return { u, S, hd, W };
}

// ── ox, facing right; units: s px; origin at the ground under the body centre ──
function ox(o) {
  const s = o.s; X.save(); X.translate(o.x, o.y); X.scale(s, s); const LW0 = LW; LW = 2.4 / s;
  const ph = o.ph || 0, col = o.col, bob = Math.sin(ph * TAU * 2) * 0.12;
  const legs = [[3.8, 0.0, -0.1], [-8.0, 0.5, 0], [4.6, 0.5, 1], [-7.2, 0.0, 1]];   // [x, phase offset, near?]
  const drawLeg = (x, off, front) => {
    const q = ((ph + off) % 1 + 1) % 1, sw = q < 0.6 ? 1.6 - 3.2 * (q / 0.6) : -1.6 + 3.2 * eInOut((q - 0.6) / 0.4);
    const lift = q < 0.6 ? 0 : 0.9 * Math.sin(Math.PI * (q - 0.6) / 0.4);
    const top = [x, -7.2 + bob], hoof = [x + sw, -0.55 - lift];
    const knee = front ? [lerp(top[0], hoof[0], 0.5) + 0.3, -3.6 - lift * 0.5] : [lerp(top[0], hoof[0], 0.45) - 0.9, -3.4 - lift * 0.5];
    limb([top, knee, hoof], [1.05, 0.5, 0.38], col);
    poly([[hoof[0] - 0.5, hoof[1] - 0.1], [hoof[0] + 0.55, hoof[1] - 0.1], [hoof[0] + 0.75, hoof[1] + 0.6], [hoof[0] - 0.55, hoof[1] + 0.6]]); paint(COL.ink);
  };
  X.save(); X.globalAlpha = 1; drawLeg(legs[2][0], legs[2][1], true); drawLeg(legs[3][0], legs[3][1], false); X.restore();
  // tail
  X.beginPath(); X.moveTo(-11.0, -11.2 + bob); X.quadraticCurveTo(-12.4, -8, -11.9, -4.6); X.strokeStyle = COL.ink; X.lineWidth = 0.55; X.stroke();
  smooth([[-12.2, -5.2], [-11.4, -5.0], [-11.5, -3.2], [-12.1, -3.0]]); paint(COL.ink, LW * 0.5);
  X.save(); X.translate(0, bob);
  const body = [[-10.2, -12.3], [-4, -12.6], [2.6, -13.7], [6.2, -12.9], [7.4, -9.5], [7.0, -7.3], [5.6, -6.2], [0, -5.8], [-6, -6.1], [-9.2, -6.7], [-11.3, -8.6], [-11.3, -11.2]];
  smooth(body); paint(col);
  if (o.patches) { X.save(); smooth(body); X.clip(); X.fillStyle = COL.ink; for (const [a, b, r1, r2] of [[-6, -10, 2.4, 1.7], [0.5, -11.5, 1.8, 1.4], [-2, -7.2, 1.6, 1.0], [4.5, -9, 1.2, 1.5]]) { X.beginPath(); X.ellipse(a, b, r1, r2, 0.4, 0, TAU); X.fill(); } X.restore(); smooth(body); paint(null); }
  // head, lowered into the yoke
  const hr = o.headDip || 0; X.save(); X.translate(6.6, -12.0); X.rotate(hr);
  smooth([[0.2, -1.2], [2.2, -0.9], [4.4, 1.2], [5.6, 3.6], [5.3, 4.5], [3.9, 4.6], [1.8, 3.0], [0.2, 2.6]]); paint(col);
  X.beginPath(); X.arc(3.4, 0.8, 0.28, 0, TAU); X.fillStyle = COL.ink; X.fill();
  X.beginPath(); X.arc(5.15, 3.9, 0.16, 0, TAU); X.fill();
  smooth([[0.9, -0.3], [-1.5, -0.9], [-1.9, -0.4], [0.6, 0.6]]); paint(col, LW * 0.8);                              // ear
  for (const [dx, sc] of [[0.6, 0.9], [1.4, 1]]) {                                                                   // lyre horns
    X.beginPath(); X.moveTo(dx, -0.8); X.bezierCurveTo(dx - 2.4 * sc, -2.5, dx - 1.8 * sc, -5.2, dx + 0.9 * sc, -5.9);
    X.bezierCurveTo(dx - 0.9 * sc, -4.8, dx - 1.2 * sc, -2.8, dx + 0.9, -0.7); X.closePath(); paint(COL.white, LW * 0.8);
  }
  X.restore();
  X.restore();
  drawLeg(legs[0][0], legs[0][1], true); drawLeg(legs[1][0], legs[1][1], false);
  LW = LW0; X.restore();
}

// ── props ──
function basket(c, w, h, fillK = 1) {   // woven basket with a heap of grain, c = bottom centre
  X.save(); X.translate(c[0], c[1]);
  if (fillK > 0) { X.beginPath(); X.ellipse(0, -h, w * 0.47, h * 0.75 * fillK, 0, Math.PI, 0); paint(COL.gold, LW * 0.8);
    X.fillStyle = COL.ochreD; for (let i = 0; i < 14; i++) { const a = hash(i) * Math.PI, r = hash(i + 9) * 0.85; X.beginPath(); X.arc(-Math.cos(a) * w * 0.42 * r, -h - Math.sin(a) * h * 0.65 * fillK * r, 1.4, 0, TAU); X.fill(); } }
  X.beginPath(); X.moveTo(-w / 2, -h); X.lineTo(w / 2, -h); X.quadraticCurveTo(w * 0.48, 0, 0, 0); X.quadraticCurveTo(-w * 0.48, 0, -w / 2, -h); X.closePath(); paint(COL.ochreD);
  X.save(); X.clip(); X.strokeStyle = 'rgba(28,23,19,0.7)'; X.lineWidth = 1.3;
  for (let x = -w; x < w; x += 9) { X.beginPath(); X.moveTo(x, -h); X.lineTo(x + h, 0); X.stroke(); X.beginPath(); X.moveTo(x, -h); X.lineTo(x - h, 0); X.stroke(); }
  X.restore(); line([-w / 2, -h], [w / 2, -h], 3.2, COL.red);
  X.restore();
}
function wheatStalk(x, y, h, lean, cut, ripe = 1) {
  const tx = x + lean * h, ty = y - h;
  const stem = cut ? h * 0.6 : h;
  X.beginPath(); X.moveTo(x, y); X.quadraticCurveTo(x + lean * stem * 0.3, y - stem * 0.6, x + lean * stem, y - stem);
  X.strokeStyle = ripe > 0.5 ? COL.ochreD : COL.green; X.lineWidth = 2.4; X.stroke();
  if (!cut) wheatEar(tx, ty, lean, ripe);
}
function wheatEar(x, y, lean, ripe = 1) {
  X.save(); X.translate(x, y); X.rotate(Math.atan2(lean, 1));
  X.beginPath(); X.ellipse(0, -9, 4.6, 12, 0, 0, TAU); paint(ripe > 0.5 ? COL.gold : COL.greenL, 1.8);
  X.strokeStyle = COL.ink; X.lineWidth = 1.1;
  for (let k = 0; k < 4; k++) { const yy = -2 - k * 5; X.beginPath(); X.moveTo(-4, yy - 2); X.lineTo(0, yy); X.lineTo(4, yy - 2); X.stroke(); }
  for (let k = -1; k <= 1; k++) { X.beginPath(); X.moveTo(k * 2, -20); X.lineTo(k * 5.5, -31); X.stroke(); }
  X.restore();
}
function sickle(w, ang, raise) {    // wooden sickle with a curved blade set with teeth
  X.save(); X.translate(w[0], w[1]); X.rotate(ang + raise);
  X.beginPath(); X.moveTo(0.3, 0); X.lineTo(-1.4, 0.25); X.strokeStyle = COL.brown; X.lineWidth = 0.6; X.lineCap = 'round'; X.stroke();
  X.beginPath(); X.moveTo(0.4, -0.2); X.bezierCurveTo(1.6, -2.4, 4.0, -2.6, 4.8, -0.4); X.bezierCurveTo(3.8, -1.6, 2.2, -1.4, 0.8, 0.3); X.closePath(); paint(COL.ochre, LW * 0.8);
  X.restore();
}
function papyrusPlant(x, y, h, lean, sway) {
  const tx = x + lean * h + sway, ty = y - h;
  X.beginPath(); X.moveTo(x, y); X.quadraticCurveTo(x + lean * h * 0.4, y - h * 0.5, tx, ty); X.strokeStyle = COL.greenD; X.lineWidth = 3; X.stroke();
  // umbel: an open fan
  X.save(); X.translate(tx, ty); X.rotate(Math.atan2(lean * h + sway, h) * 0.8);
  X.beginPath(); X.moveTo(0, 2); X.lineTo(-19, -26); X.quadraticCurveTo(0, -36, 19, -26); X.closePath(); paint(COL.green, 2);
  X.strokeStyle = COL.greenD; X.lineWidth = 1.2; for (let k = -3; k <= 3; k++) { X.beginPath(); X.moveTo(0, 0); X.lineTo(k * 5.2, -27 - (3 - Math.abs(k))); X.stroke(); }
  X.beginPath(); X.moveTo(-5, -4); X.lineTo(0, 6); X.lineTo(5, -4); X.closePath(); paint(COL.greenD, 1.5);
  X.restore();
}
function palm(x, y, h, sway) {
  X.beginPath(); X.moveTo(x - 7, y); X.quadraticCurveTo(x - 3 + sway * 0.3, y - h * 0.5, x - 4 + sway, y - h); X.lineTo(x + 5 + sway, y - h); X.quadraticCurveTo(x + 8 + sway * 0.3, y - h * 0.5, x + 7, y); X.closePath(); paint(COL.brown, 2);
  X.strokeStyle = COL.ink; X.lineWidth = 1.2; for (let k = 10; k < h - 6; k += 9) { const xx = x + sway * (k / h); X.beginPath(); X.moveTo(xx - 6, y - k); X.lineTo(xx, y - k - 4); X.lineTo(xx + 6, y - k); X.stroke(); }
  const tx = x + sway + 0.5, ty = y - h;
  for (let i = 0; i < 7; i++) {
    const a = -Math.PI + (i + 0.5) / 7 * Math.PI, L = 52 + (i % 2) * 8;
    const ex = tx + Math.cos(a) * L, ey = ty + Math.sin(a) * L * 0.55 + 16;
    X.beginPath(); X.moveTo(tx, ty); X.quadraticCurveTo(tx + Math.cos(a) * L * 0.6, ty + Math.sin(a) * L * 0.6 - 10, ex, ey);
    X.quadraticCurveTo(tx + Math.cos(a) * L * 0.5, ty + Math.sin(a) * L * 0.4 - 2, tx, ty + 4); paint(i % 2 ? COL.green : COL.greenD, 1.6);
  }
  X.fillStyle = COL.red; for (let k = 0; k < 5; k++) { X.beginPath(); X.arc(tx - 8 + k * 4, ty + 10 + (k % 2) * 4, 3.2, 0, TAU); X.fill(); X.strokeStyle = COL.ink; X.lineWidth = 1; X.stroke(); }
}
function duck(x, y, s, flap, dirx = -1) {   // pintail in flight; flap 1 = wings up, -1 = down
  X.save(); X.translate(x, y); X.scale(s * dirx, s);
  const wing = (f, c1, c2, dx) => {
    const ty = -20 * f, tx = -13 + dx;
    const W = [[5 + dx, -1.5], [2 + dx, ty * 0.5 - 1], [tx + 4, ty - 1], [tx, ty], [tx - 2, ty * 0.75], [-5 + dx, ty * 0.25], [-5 + dx, -0.5]];
    smooth(W); paint(c1, 1.5);
    smooth(W.map(([a, b]) => [lerp(1 + dx, a, 0.55), lerp(-1, b, 0.55)])); paint(c2, 1.1);
    X.strokeStyle = COL.ink; X.lineWidth = 0.9;
    for (let k = 1; k <= 3; k++) { const u = k / 4; X.beginPath(); X.moveTo(lerp(tx + 3, -4 + dx, u) * 0.6, lerp(ty, 0, u) * 0.62); X.lineTo(lerp(tx, -5 + dx, u), lerp(ty, ty * 0.25, u)); X.stroke(); }
  };
  wing(flap * 0.9, COL.blueD, COL.greenD, 2.5);                                                        // far wing
  X.beginPath(); X.moveTo(-8, -0.5); X.lineTo(-17, -2); X.lineTo(-15, 1.8); X.closePath(); paint(COL.ink, 1);   // pintail
  X.beginPath(); X.ellipse(0, 0, 9.5, 4.4, -0.05, 0, TAU); paint(COL.white, 1.6);
  X.beginPath(); X.moveTo(7.5, -2); X.quadraticCurveTo(12, -3.6, 15, -3.8); X.lineTo(15.5, -1.2); X.quadraticCurveTo(12, -0.4, 8.5, 2); X.closePath(); paint(COL.green, 1.4);
  X.beginPath(); X.ellipse(17, -3, 3.2, 2.5, 0, 0, TAU); paint(COL.green, 1.4);
  X.beginPath(); X.moveTo(19.6, -3.6); X.lineTo(24, -2.3); X.lineTo(19.8, -1.6); X.closePath(); paint(COL.ochre, 1);
  X.beginPath(); X.arc(17.8, -3.6, 0.7, 0, TAU); X.fillStyle = COL.ink; X.fill();
  wing(flap, COL.blue, COL.ochre, 0);                                                                  // near wing
  X.restore();
}
function fish(x, y, s, dirx, ph) {
  X.save(); X.translate(x, y); X.scale(s * dirx, s);
  const wag = Math.sin(ph) * 1.5;
  X.beginPath(); X.moveTo(-10, 0); X.lineTo(-17, -6 + wag); X.lineTo(-16, 6 + wag); X.closePath(); paint(COL.blueL, 1.6);
  X.beginPath(); X.moveTo(-4, -5); X.lineTo(4, -10); X.lineTo(8, -5); paint(COL.blueL, 1.4);
  X.beginPath(); X.ellipse(0, 0, 12, 6.5, 0, 0, TAU); paint('#9fb9c6', 1.8);
  X.strokeStyle = COL.ink; X.lineWidth = 0.9; for (let k = -1; k <= 1; k++) { X.beginPath(); X.moveTo(-7 + k * 3, -4); X.lineTo(-4 + k * 3, 4); X.stroke(); }
  X.beginPath(); X.arc(7, -1.5, 1.4, 0, TAU); X.fillStyle = COL.ink; X.fill();
  X.restore();
}
function heap(cx, gy, w, h) {    // granary heap of grain
  if (h <= 0.5) return;
  X.beginPath(); X.moveTo(cx - w / 2, gy); X.quadraticCurveTo(cx - w * 0.36, gy - h * 0.9, cx - w * 0.08, gy - h); X.quadraticCurveTo(cx, gy - h * 1.05, cx + w * 0.08, gy - h);
  X.quadraticCurveTo(cx + w * 0.36, gy - h * 0.9, cx + w / 2, gy); X.closePath(); paint(COL.gold);
  X.save(); X.clip(); X.fillStyle = COL.ochreD;
  for (let i = 0; i < 220; i++) { const px = cx + (hash(i * 3.1) - 0.5) * w, py = gy - hash(i * 7.7) * h; X.beginPath(); X.ellipse(px, py, 2.4, 1.5, 0.6, 0, TAU); X.fill(); }
  X.restore();
}
