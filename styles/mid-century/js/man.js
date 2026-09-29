// man.js · the gentleman in the hat: flat angular UPA-style figure, profile facing right.
// Local origin = hip joint; ground at y = 170. Colour fills are printed slightly off-register from the crayon line.
const REG = [6, -4];
const THIGH = 82, SHIN = 80;
const COAT = 'orange', COATD = '#8f3d1d', LEGC = C.ink, LEGF = '#5a5048';

function limbPts(ax, ay, a1, l1, a2, l2) { // angles from straight down, positive = forward (+x)
  const kx = ax + Math.sin(a1) * l1, ky = ay + Math.cos(a1) * l1;
  return [ax, ay, kx, ky, kx + Math.sin(a2) * l2, ky + Math.cos(a2) * l2];
}
function taper(x1, y1, x2, y2, w1, w2) {
  const l = Math.hypot(x2 - x1, y2 - y1) || 1, nx = -(y2 - y1) / l, ny = (x2 - x1) / l;
  return poly([x1 + nx * w1, y1 + ny * w1, x2 + nx * w2, y2 + ny * w2, x2 - nx * w2, y2 - ny * w2, x1 - nx * w1, y1 - ny * w1]);
}
function drawLeg(L, far) {
  const [hx, hy, kx, ky, ax, ay] = limbPts(0, 0, L.th, THIGH, L.th - L.kn, SHIN);
  // thin trouser leg: angular crayon stroke with a visible knee
  g.globalAlpha = 1; g.strokeStyle = far ? LEGF : C.ink; g.lineWidth = 13; g.lineJoin = 'miter'; g.lineCap = 'butt';
  const p = new Path2D(); p.moveTo(hx, hy - 8); p.lineTo(kx, ky); p.lineTo(ax, ay); g.stroke(p);
  // pointed shoe (toe up a little when the foot swings)
  const fa = L.foot || 0;
  g.save(); g.translate(ax, ay); g.rotate(fa);
  const shoe = poly([-12, -4, 6, -8, 34, 2, 38, 8, -12, 8]);
  g.fillStyle = far ? LEGF : C.ink; g.fill(shoe);
  g.restore();
}
function drawArm(A, far) {
  const sx = 4, sy = -138;
  const [x0, y0, ex, ey, wx, wy] = limbPts(sx, sy, A.sh, 60, A.sh + A.el, 54);
  const col = far ? COATD : COAT;
  g.save(); g.translate(REG[0], REG[1]);
  fill(taper(x0, y0, ex, ey, 11, 9), far ? COATD : col); fill(taper(ex, ey, wx, wy, 9, 7), far ? COATD : col);
  fill(ellipse(ex, ey, 9, 9), far ? COATD : col);
  g.restore();
  if (!far) lineP([x0 + 8, y0 + 4, ex + 7, ey, wx + 5, wy], 3, 0.8);
  // mitten hand with thumb, along the forearm direction
  const a = Math.atan2(wy - ey, wx - ex);
  g.save(); g.translate(wx, wy); g.rotate(a);
  const hand = poly([-2, -7, 12, -9, 22, -4, 23, 4, 14, 8, 2, 7]);
  const thumb = poly([6, -7, 12, -16, 16, -14, 13, -6]);
  g.fillStyle = far ? '#c78f68' : pat('skin'); g.fill(hand); g.fill(thumb);
  if (!far) { g.save(); g.globalAlpha = 0.8; g.strokeStyle = C.ink; g.lineWidth = 2.2; g.stroke(hand); g.restore(); }
  g.restore();
}
function drawHead(P) {
  g.save(); g.translate(0, -150); g.rotate(P.headTilt || 0);
  // neck
  fill(poly([-6, 4, 7, 4, 8, -18, -5, -18]), 'skin');
  // angular profile: flat back of the head, long wedge nose, small chin
  const head = poly([-20, -16, -25, -52, -16, -76, 16, -79, 22, -62, 48, -42, 26, -38, 22, -24, 8, -14]);
  g.save(); g.translate(REG[0] * 0.6, REG[1] * 0.6); fill(head, 'skin'); g.restore();
  line(head, 3.2, 0.85);
  // ear, eye, brow, a little mouth line
  line(poly([-6, -48, 0, -52, 2, -40, -4, -36]), 2.2, 0.8);
  g.fillStyle = C.ink; g.beginPath(); g.ellipse(14, -54, 3.4, 4.2, 0, 0, TAU); g.fill();
  lineP([6, -63, 20, -65], 3, 0.9); lineP([16, -30, 24, -31], 2.4, 0.8);
  // fedora
  g.save(); g.translate(2 + (P.hatX || 0), -72 - (P.hatLift || 0)); g.rotate(-0.06 + (P.hatTilt || 0));
  const brim = poly([-40, 0, 52, -4, 56, 3, -38, 8]);
  const crown = poly([-24, 1, -20, -34, -4, -40, 20, -38, 28, 0]);
  const band = poly([-23, -4, 27, -4, 27.5, -12, -22, -12]);
  g.save(); g.translate(REG[0] * 0.5, REG[1] * 0.5); fill(crown, 'olive'); g.restore();
  fill(band, 'mustard'); fill(brim, 'ink');
  line(crown, 3, 0.85); lineP([-4, -40, -2, -30], 2.4, 0.7);
  g.restore();
  g.restore();
}
function drawCoat(P) {
  // long angular overcoat: narrow shoulders, flared hem cut on a slant
  const coat = poly([-16, -150, 14, -152, 30, -60, 44, 26, -44, 34, -30, -60], 5, 3);
  g.save(); g.translate(REG[0], REG[1]); fill(coat, COAT); g.restore();
  line(coat, 3.4, 0.85);
  // lapel, pocket slit, three buttons
  lineP([14, -148, 2, -104, 18, -84], 2.6, 0.8);
  lineP([10, -20, 34, -24], 2.6, 0.7);
  g.fillStyle = C.ink; for (let i = 0; i < 3; i++) { g.beginPath(); g.arc(24 + i * 2.5, -70 + i * 26, 3.2, 0, TAU); g.fill(); }
}
// pose: { bob, lean, legs:[near, far]{th,kn,foot}, arms:[near, far]{sh,el}, hatLift, hatTilt, headTilt }
function drawMan(x, y, s, P) {
  g.save(); g.translate(x, y + (P.bob || 0) * s); g.scale(s, s); g.rotate(P.lean || 0);
  // cast shadow: a flat olive dash on the ground
  g.save(); g.rotate(-(P.lean || 0)); g.globalAlpha = 0.28; g.fillStyle = C.ink; g.fillRect(-60, 168 - (P.bob || 0), 130, 7); g.restore(); g.globalAlpha = 1;
  drawArm(P.arms[1], true); drawLeg(P.legs[1], true);
  drawLeg(P.legs[0], false);
  drawCoat(P); drawHead(P);
  drawArm(P.arms[0], false);
  g.restore();
}
// walk cycle, evaluated on a stepped phase (drawings held on twos)
function walkPose(ph) {
  const leg = q => { const a = TAU * q, th = 0.46 * Math.sin(a), sw = Math.cos(a); return { th, kn: 1.05 * Math.max(0, sw) ** 1.4 + 0.08, foot: sw > 0 ? -0.18 * sw : 0.12 * Math.max(0, -Math.sin(a)) }; };
  const arm = q => ({ sh: -0.42 * Math.sin(TAU * q), el: 0.35 + 0.25 * Math.max(0, -Math.sin(TAU * q)) });
  return { bob: -7 * Math.abs(Math.cos(TAU * ph)) + 4, lean: 0.05, legs: [leg(ph), leg(ph + 0.5)], arms: [arm(ph + 0.5), arm(ph)], headTilt: 0.02 * Math.sin(2 * TAU * ph) };
}
const STAND = () => ({ bob: 0, lean: 0, legs: [{ th: 0.14, kn: 0.1, foot: 0 }, { th: -0.1, kn: 0.06, foot: 0 }], arms: [{ sh: 0.08, el: 0.3 }, { sh: -0.08, el: 0.3 }] });
function blendPose(A, B, u) {
  const m = (a, b) => typeof a === 'number' ? lerp(a, b ?? 0, u) : a;
  const o = {}; for (const k of new Set([...Object.keys(A), ...Object.keys(B)])) {
    const a = A[k] ?? 0, b = B[k] ?? 0;
    o[k] = Array.isArray(a) ? a.map((x, i) => { const y = b[i]; const r = {}; for (const kk in x) r[kk] = lerp(x[kk], y[kk] ?? 0, u); return r; }) : m(a, b);
  }
  return o;
}
