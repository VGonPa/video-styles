// scene.js · layout, timeline, camera, the living painting and the audio events
const cv = document.getElementById('c'), X = cv.getContext('2d');
const TL = {
  pond: 0.0, fishA: 0.3, fishB: 0.55, waves: [0.9, 1.9], roots: [1.05, 1.7], grass: [1.35, 4.3],
  border: [1.85, 4.6], zoom: [2.65, 4.1], trunk: [2.85, 3.55], sun: 3.75, moon: 4.0, peaL: 4.15, peaR: 4.35,
  fill: [5.6, 7.0], title: [6.55, 7.45], smile: [7.35, 7.85], wake: [7.8, 8.1], blink: [8.7, 8.95], out: [9.25, 10.0],
};
const ZOOM = { s: 2.9, c: [960, 842] };
const POND = { x0: 640, y0: 700, x1: 1280, y1: 985, r: 26, band: 18 };
const BO = { x0: 24, y0: 22, x1: 1896, y1: 1058 }, BI = { x0: 72, y0: 70, x1: 1848, y1: 1010 };
const SUNP = [262, 262], MOONP = [1656, 252], PSC = 1.15;
const TITLE = 'The Tree That Feeds the Birds', TR = { x0: 486, y0: 90, x1: 1434, y1: 166 };

function rrect(x0, y0, x1, y1, r, n = 6) {
  const p = [], cs = [[x1 - r, y0 + r, -Math.PI / 2], [x1 - r, y1 - r, 0], [x0 + r, y1 - r, Math.PI / 2], [x0 + r, y0 + r, Math.PI]];
  for (const [cx, cy, a] of cs) for (let i = 0; i <= n; i++) { const b = a + i / n * Math.PI / 2; p.push([cx + Math.cos(b) * r, cy + Math.sin(b) * r]); }
  return p;
}
// ── the pond ──
let POND_OPS;
function buildPond() {
  const o = rrect(POND.x0, POND.y0, POND.x1, POND.y1, POND.r, 8), b = POND.band, i = rrect(POND.x0 + b, POND.y0 + b, POND.x1 - b, POND.y1 - b, POND.r - 8, 8);
  const ring = [...o, o[0], i[0], ...i.slice().reverse()];
  const t = TL.pond;
  POND_OPS = prep([
    S('fill', t + 0.3, t + 0.85, { p: i, c: C.water, a: 0.35, sp: 14 }),
    S('fill', t + 0.5, t + 0.95, { p: ring, c: C.yel, a: 0.8, sp: 10 }),
    S('hatch', t + 0.8, t + 1.45, { p: ring, a: 0.85, sp: 8, lw: 1.8 }),
    S('dbl', t, t + 0.75, { p: wob(o, 1.4, 21), w: 9, gap: 3.4, gc: C.ver, closed: true }),
    S('dbl', t + 0.15, t + 0.85, { p: wob(i, 1.2, 22), w: 7, gap: 2.6, gc: C.ver, closed: true }),
  ]);
}
function drawWaves(t) {
  const n = 10, x0 = POND.x0 + 30, x1 = POND.x1 - 30;
  X.lineCap = 'round'; X.strokeStyle = C.ind; X.lineWidth = 2.4;
  for (let k = 0; k < n; k++) {
    const u = seg(t, TL.waves[0] + k * 0.08, TL.waves[0] + k * 0.08 + 0.35); if (u <= 0) continue;
    const y = POND.y0 + 34 + k * 24, ph = t * 1.6 + k * 1.3, xe = lerp(k % 2 ? x1 : x0, k % 2 ? x0 : x1, eOut(u));
    X.beginPath();
    for (let j = 0; j <= 80; j++) { const x = lerp(k % 2 ? x1 : x0, xe, j / 80); const yy = y + 4.5 * Math.sin(x * 0.045 + ph); j ? X.lineTo(x, yy) : X.moveTo(x, yy); }
    X.stroke();
  }
}
// ── fish ──
let FISH;
function buildFish() {
  FISH = [
    { f: makeFish({ head: C.yel, body: C.pink, band: C.yel, tail: C.grn, fin: C.ver, gap: C.ver }, 31), t0: TL.fishA, x: 900, y: 790, dir: 1, fy: 1, ph: 0 },
    { f: makeFish({ head: C.org, body: C.grnL, band: C.yel, tail: C.ind, fin: C.pink, gap: C.yel }, 47), t0: TL.fishB, x: 1022, y: 895, dir: -1, fy: 1, ph: 2.1 },
  ];
}
function fishMap(F, t) {
  const sw = clamp((t - F.t0 - 0.5) / 1.0), A = 9 * sw, ph = t * TAU * 1.25 + F.ph;
  const fx = F.x + 28 * Math.sin(t * 0.85) * sw, fy = F.y + 4 * Math.sin(t * 1.3 + F.ph) * sw, k = 0.85;
  return ([x, y]) => { const w = Math.pow(clamp((105 - x) / 250), 1.7); return [fx + F.dir * x * k, fy + (F.fy * y + A * w * Math.sin(ph - (105 - x) * 0.024)) * k]; };
}
// ── border band: zigzag triangles, double rulings, corner blossoms; drawn from the bottom centre both ways ──
let BORDER;
function halfPath(R, side) {   // bottom centre → corner → up → top centre
  const cx = (R.x0 + R.x1) / 2, x = side < 0 ? R.x0 : R.x1;
  return [[cx, R.y1], [x, R.y1], [x, R.y0], [cx, R.y0]];
}
function perimPos(x, y) {   // 0…1 along a half path for a point on the band (either side)
  const mx = (BO.x0 + BI.x0) / 2, my0 = (BO.y0 + BI.y0) / 2, my1 = (BO.y1 + BI.y1) / 2, hw = 960 - mx, hh = my1 - my0, L = hw * 2 + hh;
  const dx = Math.abs(x - 960);
  if (y > my1 - 30 && dx < hw - 10) return dx / L;
  if (y < my0 + 30 && dx < hw - 10) return (hw + hh + (hw - dx)) / L;
  return (hw + (my1 - y)) / L;
}
function buildBorder() {
  const ops = [], tri = [], r = mulberry(3);
  const band = 48, run = (ax, ay, bx, by, inwardX, inwardY) => {   // triangles along one side
    const len = Math.hypot(bx - ax, by - ay), n = Math.round(len / 46), ux = (bx - ax) / len, uy = (by - ay) / len, st = len / n;
    for (let i = 0; i < n; i++) {
      const p0 = [ax + ux * st * i, ay + uy * st * i], p1 = [ax + ux * st * (i + 1), ay + uy * st * (i + 1)], m = [(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2];
      const up = [p0, p1, [m[0] + inwardX * band, m[1] + inwardY * band]];
      const q0 = [p0[0] + inwardX * band, p0[1] + inwardY * band], q1 = [p1[0] + inwardX * band, p1[1] + inwardY * band];
      const nx = [p1, q1, [p1[0] + ux * st + inwardX * band, p1[1] + uy * st + inwardY * band]];
      tri.push({ p: up, c: C.yel, cen: [m[0] + inwardX * band * 0.33, m[1] + inwardY * band * 0.33] });
      if (i < n - 1) tri.push({ p: [p1, [m[0] + inwardX * band, m[1] + inwardY * band], [m[0] + ux * st + inwardX * band, m[1] + uy * st + inwardY * band]], c: C.ver, cen: [p1[0] + inwardX * band * 0.66, p1[1] + inwardY * band * 0.66] });
    }
  };
  run(BO.x0 + band, BO.y1, BO.x1 - band, BO.y1, 0, -1);
  run(BO.x0 + band, BO.y0, BO.x1 - band, BO.y0, 0, 1);
  run(BO.x0, BO.y0 + band, BO.x0, BO.y1 - band, 1, 0);
  run(BO.x1, BO.y0 + band, BO.x1, BO.y1 - band, -1, 0);
  const [b0, b1] = TL.border, D = b1 - b0;
  for (const T of tri) { const s = perimPos(...T.cen), ts = b0 + s * D * 0.92 + 0.08;
    ops.push(S('pop', ts, ts + 0.3, { p: T.p, c: T.c, edge: 2.2, o: T.cen }));
    if (T.c === C.yel) ops.push(S('dots', ts + 0.15, ts + 0.3, { d: [[T.cen[0], T.cen[1], 3.2]] })); }
  // corner squares with a blossom
  for (const [x, y] of [[BO.x0, BO.y0], [BO.x1 - band, BO.y0], [BO.x0, BO.y1 - band], [BO.x1 - band, BO.y1 - band]]) {
    const ts = b0 + perimPos(x + band / 2, y + band / 2) * D, sq = [[x, y], [x + band, y], [x + band, y + band], [x, y + band]];
    ops.push(S('pop', ts, ts + 0.3, { p: sq, c: C.ind, edge: 2.4 }));
    ops.push(...makeFlower(19, C.ver, C.yel, 5).map(o => Object.assign({}, o, { t0: o.t0 + ts + 0.1, t1: o.t1 + ts + 0.1, p: o.p && o.p.map(([a, b]) => [a + x + band / 2, b + y + band / 2]), o: o.o && [o.o[0] + x + band / 2, o.o[1] + y + band / 2], d: o.d && o.d.map(([a, b, c]) => [a + x + band / 2, b + y + band / 2, c]) })));
  }
  for (const R of [BO, BI]) for (const sd of [-1, 1]) ops.push(S('dbl', b0, b1, { p: wob(halfPath(R, sd), 1.0, 60 + sd + (R === BO ? 0 : 5), 8), w: 8, gap: 3, gc: C.ver }));
  // inner dotted ruling
  const dd = []; for (let x = BI.x0 + 20; x < BI.x1 - 10; x += 22) { dd.push([x, BI.y0 + 12, 2.6]); }
  BORDER = prep(ops);
}
// ground tufts along the bottom edge
let GRASS;
function buildGrass() {
  GRASS = []; const r = mulberry(9);
  for (let x = BI.x0 + 22; x < BI.x1 - 16; x += 26) {
    const u = Math.abs(x - 960) / 900, ts = x > POND.x0 - 30 && x < POND.x1 + 30 ? TL.grass[0] + u * 1.5 : TL.grass[0] + 0.9 + u * 2.1;
    GRASS.push({ x, ts, h: 14 + r() * 8, c: r() < 0.5 ? C.grn : C.grnL, lean: (r() - 0.5) * 0.4 });
  }
}
function drawGrass(t) {
  for (const G of GRASS) { const u = eBack(seg(t, G.ts, G.ts + 0.3)); if (u <= 0) continue;
    const y = 1004, h = G.h * u; X.beginPath(); X.moveTo(G.x - 8, y); X.quadraticCurveTo(G.x - 2 + G.lean * h, y - h * 0.6, G.x + G.lean * h, y - h); X.quadraticCurveTo(G.x + 2 + G.lean * h, y - h * 0.6, G.x + 8, y); X.closePath();
    X.fillStyle = G.c; X.fill(); X.strokeStyle = C.ink; X.lineWidth = 2; X.stroke(); }
}
// ── the tree of life ──
let TREE;
function buildTree() {
  const B = [
    [[944, 566], [860, 548], [700, 580], [556, 478], 30, 10, 0.2],
    [[946, 526], [890, 440], [760, 410], [600, 330], 28, 9, 0.05],
    [[952, 500], [920, 396], [866, 304], [784, 240], 26, 9, 0.3],
    [[960, 490], [964, 410], [956, 330], [960, 272], 26, 9, 0.12],
  ];
  const all = []; B.forEach((b, bi) => { all.push(b); if (bi < 3) all.push([[1920 - b[0][0], b[0][1]], [1920 - b[1][0], b[1][1]], [1920 - b[2][0], b[2][1]], [1920 - b[3][0], b[3][1]], b[4], b[5], b[6] + 0.1]); });
  const r = mulberry(17), br = [], leaves = [], flowers = [];
  const perches = [[0, 0.62], [3, 0.6], [5, 0.62], [2, 0.8]];   // [branch index, param] where the parrots land
  all.forEach((b, i) => {
    const cl = bez(b[0], b[1], b[2], b[3], 40), t0 = TL.trunk[0] + 0.45 + b[6] * 1.0, t1 = t0 + 0.85;
    br.push({ cl, w0: b[4], w1: b[5], t0, t1 });
    const ps = [0.22, 0.32, 0.42, 0.52, 0.62, 0.72, 0.82, 0.92];
    ps.forEach((p, k) => {
      for (const sd of [1, -1]) {
        if (perches.some(([bi, pp]) => bi === i && Math.abs(pp - p) < 0.1) && ((cl[20][1] > cl[40][1]) ? sd === (b[3][0] < 960 ? 1 : -1) : true) && sd === (b[3][0] < 960 ? 1 : -1)) continue;
        const j = Math.round(p * 40), P = cl[j], A = cl[Math.max(0, j - 1)], Bq = cl[Math.min(40, j + 1)], tx = Bq[0] - A[0], ty = Bq[1] - A[1], tl = Math.hypot(tx, ty);
        const nx = -ty / tl * sd, ny = tx / tl * sd, w = lerp(b[4], b[5], p) / 2, ang = Math.atan2(ty / tl * 0.55 + ny, tx / tl * 0.55 + nx);
        const len = 70 + r() * 18;
        leaves.push({ x: P[0] + nx * w * 0.8, y: P[1] + ny * w * 0.8, a: ang + (k % 2 ? 0.1 : -0.1), ops: makeLeaf(len, 19 + r() * 4, 100 + leaves.length, k % 3 === 2 ? C.grnD : C.grn, (k + (sd > 0 ? 1 : 0)) % 2 ? C.grnL : C.yel), ts: t0 + (t1 - t0) * p, ph: r() * TAU, len });
      }
    });
    // a tip leaf and a flower at the tip
    const P = cl[40], A = cl[37], a = Math.atan2(P[1] - A[1], P[0] - A[0]);
    flowers.push({ x: P[0] + Math.cos(a) * 26, y: P[1] + Math.sin(a) * 26, ops: makeFlower(26, i % 2 ? C.pink : C.ver, C.yel, 200 + i), ts: t1 - 0.05, s: 26 });
  });
  // flowers tucked into the gaps of the canopy
  for (const [x, y, rr] of [[730, 470, 26], [850, 400, 24], [1070, 400, 24], [1190, 470, 26], [880, 480, 20], [1040, 480, 20], [690, 370, 22], [1230, 370, 22], [870, 290, 22], [1050, 290, 22], [620, 440, 20], [1300, 440, 20]])
    flowers.push({ x, y, ops: makeFlower(rr, (x + y) % 3 ? C.org : C.pink, C.yel, x), ts: 4.45 + Math.abs(x - 960) / 600 + (600 - y) / 900, s: rr });
  const perch = perches.map(([bi, p]) => { const b = br[bi], j = Math.round(p * 40), P = b.cl[j], w = lerp(b.w0, b.w1, p) / 2; return { x: P[0], y: P[1] - w + 2, face: P[0] < 960 ? 1 : -1 }; });
  const trunk = [...bez([914, 702], [934, 640], [940, 560], [934, 480], 16), ...bez([986, 480], [980, 560], [986, 640], [1006, 702], 16)];
  const roots = [bez([956, 700], [900, 690], [840, 700], [770, 688], 20), bez([964, 700], [1020, 690], [1080, 700], [1150, 688], 20), bez([948, 700], [920, 680], [880, 676], [850, 668], 14), bez([972, 700], [1000, 680], [1040, 676], [1070, 668], 14)];
  const tr = TL.trunk;
  const tcl = bez([960, 700], [957, 620], [963, 540], [960, 462], 40), trunkB = { cl: tcl, w0: 96, w1: 52, t0: TL.trunk[0], t1: TL.trunk[1], trunk: true };
  const bark = prepOp(S('scales', 0, 0.01, { p: tube(tcl, 96, 52), r: 10, lw: 2, dir: 1 }));
  const rootOps = prep(roots.map((p, i) => S('dbl', TL.roots[0] + i * 0.12, TL.roots[0] + i * 0.12 + 0.45, { p, w: 11 - (i > 1 ? 3 : 0), gap: 4.5 - (i > 1 ? 1.5 : 0), gc: C.brown })));
  TREE = { br, leaves, flowers, perch, rootOps, trunk: trunkB, bark };
}
function branchGeom(b, t) {
  const u = seg(t, b.t0, b.t1); if (u <= 0) return null;
  const n = Math.max(2, Math.round((b.trunk ? eInOut(u) : eOut(u)) * 40));
  return { b, cl: b.cl.slice(0, n + 1), n, we: lerp(b.w0, b.w1, n / 40) };
}
function tubeFill(g, extra, cap) {
  X.fill(toPath(tube(g.cl, g.b.w0 + extra, g.we + extra), true));
  if (cap) { const e = g.cl[g.cl.length - 1]; X.beginPath(); X.arc(e[0], e[1], (g.we + extra) / 2, 0, TAU); X.fill(); }
}
function drawTree(t) {
  // one merged silhouette: all ink layers, then all yellow gap layers, then the vermilion bark — junctions stay clean
  const G = [TREE.trunk, ...TREE.br].map(b => branchGeom(b, t)).filter(Boolean);
  X.fillStyle = C.ink; for (const g of G) tubeFill(g, 12, !g.b.trunk);
  X.fillStyle = C.yel; for (const g of G) tubeFill(g, 5.5, !g.b.trunk);
  for (const g of G) {
    X.fillStyle = C.verD; tubeFill(g, 0, !g.b.trunk);
    const P = toPath(tube(g.cl, g.b.w0, g.we), true);
    X.save(); X.clip(P);
    if (g.b.trunk) drawOp(X, TREE.bark, 1);
    else { X.strokeStyle = C.ink; X.lineWidth = 1.8; const cl = g.cl;
      for (let i = 2; i < g.n; i += 2) { const [x, y] = cl[i], [x2, y2] = cl[i + 1] || cl[i], a = Math.atan2(y2 - y, x2 - x) + Math.PI / 2, w = lerp(g.b.w0, g.b.w1, i / 40) / 2;
        X.beginPath(); X.moveTo(x - Math.cos(a - 0.5) * w, y - Math.sin(a - 0.5) * w); X.lineTo(x + Math.cos(a + 0.5) * w * 0.2, y + Math.sin(a + 0.5) * w * 0.2); X.stroke(); } }
    X.restore();
  }
  for (const L of TREE.leaves) { const lt = t - L.ts; if (lt <= 0) continue; const s = eBack(clamp(lt / 0.32)), sway = 0.03 * Math.sin(t * 1.7 + L.ph) * clamp(lt - 0.6);
    X.save(); X.translate(L.x, L.y); X.rotate(L.a + sway); X.scale(s, s); drawMotif(X, L.ops, lt * 1.1); X.restore(); }
  for (const F of TREE.flowers) { const lt = t - F.ts; if (lt <= 0) continue; X.save(); X.translate(F.x, F.y); X.rotate(0.2 * Math.sin(t * 0.8 + F.x) * clamp(lt - 0.8) * 0.3); drawMotif(X, F.ops, lt); X.restore(); }
}
// ── parrots fly in and land ──
let BIRDS;
function buildBirds() {
  const arr = [5.85, 6.1, 6.35, 6.6], from = [[-120, 300], [2040, 180], [2040, 420], [-120, 120]];
  BIRDS = TREE.perch.map((P, i) => ({ P, m: makeParrot(i % 2 ? C.grn : C.grnL, 300 + i), ta: arr[i], tf: arr[i] - 1.0, from: from[i], ph: i * 1.7 }));
}
function drawBird(B, t) {
  if (t < B.tf) return;
  const u = seg(t, B.tf, B.ta), e = 1 - Math.pow(1 - u, 2.2), [fx, fy] = B.from, P = B.P;
  const cx = lerp(fx, P.x, 0.5), cy = Math.min(fy, P.y) - 140;
  let x = (1 - e) * (1 - e) * fx + 2 * (1 - e) * e * cx + e * e * P.x, y = (1 - e) * (1 - e) * fy + 2 * (1 - e) * e * cy + e * e * P.y;
  const flying = u < 1, face = flying ? (P.x > fx ? 1 : -1) : P.face;
  const land = seg(t, B.ta, B.ta + 0.45), bob = u >= 1 ? Math.sin(land * Math.PI) * 7 * (1 - land) + 1.5 * Math.sin((t - B.ta) * 2.2 + B.ph) * clamp((t - B.ta - 0.5) * 2) : 0;
  const wingA = flying ? -0.9 + 0.9 * Math.sin(t * TAU * 5 + B.ph) : -0.12 * Math.sin(land * Math.PI * 2) * (1 - land);
  X.save(); X.translate(x, y + bob); X.scale(face * 1.6, 1.6); if (flying) X.rotate(-0.12 + 0.05 * Math.sin(t * 9));
  if (!flying) drawMotif(X, B.m.legs, 1);
  drawMotif(X, B.m.ops, 1);
  X.save(); X.translate(...B.m.shoulder); X.rotate(wingA); drawMotif(X, B.m.wing, 1); X.restore();
  X.restore();
}
// ── peacocks, sun, moon ──
let PEA, SUN, MOON;
function drawPeacock(Pc, t) {
  const lt = t - Pc.t0; if (lt <= 0) return;
  X.save(); X.translate(Pc.x, 985); X.scale(Pc.face * PSC, PSC);
  drawMotif(X, Pc.m.ops, lt);
  const bob = 0.06 * Math.sin((t - 6.8) * 2.4) * clamp(t - 6.8) + 0.05 * eBack(seg(t, 7.9, 8.3)) * (1 - seg(t, 8.3, 8.9));
  X.translate(...Pc.m.pivot); X.rotate(bob); X.translate(-Pc.m.pivot[0], -Pc.m.pivot[1]);
  drawMotif(X, Pc.m.head, lt); X.restore();
}
// ── space fillers ──
let FILL;
function inPoly(p, [x, y]) { let c = false; for (let i = 0, j = p.length - 1; i < p.length; j = i++) { const [xi, yi] = p[i], [xj, yj] = p[j]; if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c; } return c; }
function buildFillers() {
  const r = mulberry(55), pts = [];   // occupied sample points
  for (const B of TREE.br) for (const q of B.cl) pts.push([q[0], q[1], 24]);
  for (const L of TREE.leaves) for (let k = 0; k <= 4; k++) pts.push([L.x + Math.cos(L.a) * L.len * k / 4, L.y + Math.sin(L.a) * L.len * k / 4, 18]);
  for (const F of TREE.flowers) pts.push([F.x, F.y, F.s + 4]);
  for (const B of BIRDS) pts.push([B.P.x - B.P.face * 14, B.P.y - 40, 70], [B.P.x - B.P.face * 70, B.P.y - 4, 44]);
  const peaPolys = PEA.map(P => [P.m.ops, P.m.head].flat().filter(o => o.p && (o.k === 'fill' || o.k === 'pop')).map(o => o.p.map(([x, y]) => [P.x + P.face * x * PSC, 985 + y * PSC])));
  const free = (x, y, s) => {
    if (x < BI.x0 + 14 + s || x > BI.x1 - 14 - s || y < BI.y0 + 14 + s || y > 978 - s) return false;
    if (Math.hypot(x - SUNP[0], y - SUNP[1]) < 186 + s || Math.hypot(x - MOONP[0], y - MOONP[1]) < 158 + s) return false;
    if (x > TR.x0 - 10 - s && x < TR.x1 + 10 + s && y < TR.y1 + 10 + s) return false;
    if (x > POND.x0 - 10 - s && x < POND.x1 + 10 + s && y > 662 - s) return false;
    if (x > 915 - s && x < 1005 + s && y > 455 - s) return false;
    for (const [px, py, pr] of pts) if (Math.hypot(x - px, y - py) < pr + s) return false;
    for (const polys of peaPolys) for (const p of polys) { if (inPoly(p, [x, y])) return false; for (let i = 0; i < p.length; i += 2) if (Math.hypot(x - p[i][0], y - p[i][1]) < s + 8) return false; }
    return true;
  };
  FILL = [];
  for (let y = 90; y < 990; y += 34) for (let x = 90; x < 1840; x += 34) {
    const jx = x + (r() - 0.5) * 26, jy = y + (r() - 0.5) * 26, s = 14 + r() * 10;
    if (!free(jx, jy, s)) continue;
    if (FILL.some(f => Math.hypot(f.x - jx, f.y - jy) < f.s + s + 10)) continue;
    const kind = r() < 0.5 ? 0 : r() < 0.4 ? 1 : r() < 0.6 ? 2 : 3;
    FILL.push({ x: jx, y: jy, s, ops: makeFiller(kind, s, 900 + FILL.length), ts: TL.fill[0] + (Math.hypot(jx - 960, jy - 560) / 1000) * (TL.fill[1] - TL.fill[0] - 0.4) + r() * 0.15, rot: r() * TAU, kind });
  }
}
// ── title strip ──
let TITLE_OPS;
function buildTitle() {
  const [a] = TL.title, p = [[TR.x0, TR.y0], [TR.x1, TR.y0], [TR.x1, TR.y1], [TR.x0, TR.y1]];
  const ops = [S('fill', a + 0.2, a + 0.55, { p, c: C.yel, a: 1.2, sp: 12 }), S('dbl', a, a + 0.5, { p: wob([[960, TR.y0], [TR.x1, TR.y0], [TR.x1, TR.y1], [TR.x0, TR.y1], [TR.x0, TR.y0], [960, TR.y0]], 1, 88, 8), w: 8, gap: 3, gc: C.ver })];
  for (let k = 0; k < 2; k++) { const x = k ? TR.x1 : TR.x0, sd = k ? 1 : -1;
    for (let j = 0; j < 3; j++) ops.push(S('pop', a + 0.3 + j * 0.06, a + 0.55 + j * 0.06, { p: [[x, TR.y0 + j * 25.3], [x + sd * 24, TR.y0 + j * 25.3 + 12.6], [x, TR.y0 + (j + 1) * 25.3]], c: j % 2 ? C.ind : C.ver, edge: 2 })); }
  const dd = []; for (let x = TR.x0 + 20; x < TR.x1 - 10; x += 21) { dd.push([x, TR.y0 + 12, 2.6]); dd.push([x + 10, TR.y1 - 12, 2.6]); }
  ops.push(S('dots', a + 0.45, a + 0.9, { d: dd, c: C.verD }));
  TITLE_OPS = prep(ops);
}
function drawTitle(t) {
  drawMotif(X, TITLE_OPS, t);
  const [a, b] = TL.title, n = TITLE.length;
  X.font = `400 50px '${FT}'`; X.textBaseline = 'alphabetic'; X.textAlign = 'left';
  const tw = X.measureText(TITLE).width; let x = 960 - tw / 2;
  for (let i = 0; i < n; i++) { const ch = TITLE[i], w = X.measureText(ch).width, ts = a + 0.4 + i / n * 0.55, u = seg(t, ts, ts + 0.22);
    if (u > 0 && ch !== ' ') { const s = eBack(u); X.save(); X.translate(x + w / 2, 145); X.scale(s, s); X.fillStyle = C.ink; X.fillText(ch, -w / 2, 0); X.restore(); }
    x += w; }
}

// ── frame ──
let READY = false;
function camera(t) {
  const u = eInOut(seg(t, ...TL.zoom)), s = Math.exp(lerp(Math.log(ZOOM.s), 0, u));
  const k = (ZOOM.s - s) / (ZOOM.s - 1 || 1), cx = lerp(ZOOM.c[0], 960, k), cy = lerp(ZOOM.c[1], 540, k);
  const push = 1 + 0.035 * eInOut(seg(t, 8.6, 10));
  const S2 = s * push; return [S2, 0, 0, S2, 960 - cx * S2, 540 - cy * S2];
}
function frame(t) {
  X.setTransform(1, 0, 0, 1, 0, 0); X.globalCompositeOperation = 'source-over'; X.globalAlpha = 1;
  X.setTransform(...camera(t));
  X.drawImage(PAPER, 0, 0);
  drawMotif(X, BORDER, t);
  drawGrass(t);
  drawMotif(X, POND_OPS, t);
  drawWaves(t);
  for (const F of FISH) { const lt = t - F.t0; if (lt > 0) drawMotif(X, F.f.ops, lt, fishMap(F, t)); }
  drawMotif(X, TREE.rootOps, t);
  drawTree(t);
  const sl = t - TL.sun; if (sl > 0) { X.save(); X.translate(...SUNP); X.scale(1.15, 1.15); X.rotate(0.015 * Math.sin(t * 0.9)); drawMotif(X, SUN, sl);
    const bl = Math.sin(Math.PI * seg(t, ...TL.blink)); sunFace(X, eBack(seg(t, ...TL.smile)), bl, sl); X.restore(); }
  const ml = t - TL.moon; if (ml > 0) { X.save(); X.translate(...MOONP); X.scale(1.15, 1.15); drawMotif(X, MOON, ml); moonFace(X, eOut(seg(t, ...TL.wake)), ml); X.restore(); }
  for (const P of PEA) drawPeacock(P, t);
  for (const F of FILL) { const lt = t - F.ts; if (lt <= 0) continue; X.save(); X.translate(F.x, F.y); if (F.kind !== 0) X.rotate(F.rot); drawMotif(X, F.ops, lt); X.restore(); }
  for (const B of BIRDS) drawBird(B, t);
  drawTitle(t);
  // paper grain in screen space and the closing fade
  X.setTransform(1, 0, 0, 1, 0, 0);
  X.globalCompositeOperation = 'multiply'; X.drawImage(GRAIN, 0, 0); X.globalCompositeOperation = 'source-over';
  const fo = eInOut(seg(t, ...TL.out)), fi = 1 - seg(t, 0, 0.3);
  if (fo > 0 || fi > 0) { X.globalAlpha = Math.max(fo, fi); X.fillStyle = C.paper; X.fillRect(0, 0, W, H); X.globalAlpha = 1; }
}
window.ready = (async () => {
  await document.fonts.load(`400 44px '${FT}'`); await document.fonts.ready;
  bakePaper(); buildPond(); buildFish(); buildBorder(); buildGrass(); buildTree();
  PEA = [{ m: makePeacock(401, C.yel), x: 452, face: 1, t0: TL.peaL }, { m: makePeacock(402, C.pink), x: 1468, face: -1, t0: TL.peaR }];
  SUN = makeSun(501); MOON = makeMoon(502); buildBirds(); buildFillers(); buildTitle();
  READY = true;
})();
window.draw = ({ t }) => { frame(t); return cv.toDataURL('image/jpeg', 0.92).split(',')[1]; };
// ── events for the sound design ──
window.events = () => {
  const ev = [];
  ev.push({ k: 'pen', t: TL.pond, d: 0.85 }, { k: 'brush', t: TL.pond + 0.35, d: 0.6 }, { k: 'hatch', t: TL.pond + 0.8, d: 0.65 });
  for (const F of FISH) ev.push({ k: 'pen', t: F.t0, d: 0.9 }, { k: 'brush', t: F.t0 + 0.85, d: 0.65 }, { k: 'hatch', t: F.t0 + 1.45, d: 0.7 }, { k: 'plip', t: F.t0 + 0.75 });
  ev.push({ k: 'water', t: TL.waves[0] });
  ev.push({ k: 'pen', t: TL.roots[0], d: 0.7 }, { k: 'pen', t: TL.border[0], d: TL.border[1] - TL.border[0] });
  ev.push({ k: 'whoosh', t: TL.zoom[0], d: TL.zoom[1] - TL.zoom[0] });
  ev.push({ k: 'grow', t: TL.trunk[0], d: 0.8 });
  for (const B of TREE.br) ev.push({ k: 'grow', t: B.t0, d: B.t1 - B.t0 });
  for (const L of TREE.leaves) ev.push({ k: 'pop', t: L.ts, pan: (L.x - 960) / 960 });
  for (const F of TREE.flowers) ev.push({ k: 'bloom', t: F.ts, pan: (F.x - 960) / 960 });
  ev.push({ k: 'pen', t: TL.sun, d: 0.6 }, { k: 'rays', t: TL.sun + 0.55, d: 0.65 }, { k: 'pen', t: TL.moon, d: 0.55 }, { k: 'rays', t: TL.moon + 0.6, d: 0.5 });
  for (const P of PEA) ev.push({ k: 'pen', t: P.t0, d: 0.6 }, { k: 'brush', t: P.t0 + 0.35, d: 0.5 }, { k: 'dots', t: P.t0 + 0.8, d: 0.5 });
  for (const B of BIRDS) ev.push({ k: 'flap', t: B.tf + 0.3, d: 0.7, pan: B.from[0] < 960 ? -0.7 : 0.7 }, { k: 'land', t: B.ta, pan: (B.P.x - 960) / 960 });
  for (const F of FILL) ev.push({ k: 'tick', t: F.ts, pan: (F.x - 960) / 960 });
  ev.push({ k: 'title', t: TL.title[0] + 0.4 }, { k: 'smile', t: TL.smile[0] }, { k: 'wake', t: TL.wake[0] }, { k: 'peacock', t: 7.95 }, { k: 'end', t: 8.9 });
  return ev.sort((a, b) => a.t - b.t);
};
