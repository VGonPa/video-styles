// motifs.js · fish, leaves, flowers, parrots, peacocks, sun and moon as timed stroke lists (local coordinates)
const S = (k, t0, t1, o) => Object.assign({ k, t0, t1 }, o);
const R2 = n => Math.round(n * 100) / 100;

// band of a lengthwise body between xa and xb (top edge −hw, bottom edge +hw), boundary curves bulge by ba/bb
function bodyBand(hw, xa, xb, ba = 0, bb = 0, n = 18) {
  const p = [];
  for (let i = 0; i <= n; i++) { const x = lerp(xa, xb, i / n); p.push([x, -hw(x)]); }
  for (let i = 1; i < 10; i++) { const y = lerp(-hw(xb), hw(xb), i / 10), q = y / (hw(xb) || 1); p.push([xb + bb * (1 - q * q), y]); }
  for (let i = n; i >= 0; i--) { const x = lerp(xa, xb, i / n); p.push([x, hw(x)]); }
  for (let i = 1; i < 10; i++) { const y = lerp(hw(xa), -hw(xa), i / 10), q = y / (hw(xa) || 1); p.push([xa + ba * (1 - q * q), y]); }
  return p;
}
function gillArc(hw, x, b, n = 14) { const p = []; for (let i = 0; i <= n; i++) { const y = lerp(-hw(x), hw(x), i / n) * 0.96, q = y / hw(x); p.push([x + b * (1 - q * q), y]); } return p; }

// ── fish (head toward +x); pal = {head, body, band, tail, fin, gap} ──
function makeFish(pal, seed) {
  const xt = -95, xn = 125, HW = 50;
  const hw = x => { const s = clamp((x - xt) / (xn - xt)); return HW * Math.pow(Math.sin(Math.PI * (0.05 + 0.9 * Math.pow(s, 0.8))), 0.72); };
  const top = [], bot = [];
  for (let i = 0; i <= 40; i++) { const x = lerp(xt, xn, i / 40); top.push([x, -hw(x)]); bot.push([x, hw(x)]); }
  const nose = ell(xn, 0, 9, hw(xn), 10, -Math.PI / 2, Math.PI / 2);
  const outline = [...top, ...nose.slice(1, -1), ...bot.reverse()];
  const r0 = hw(xt);
  const tail = [[xt + 4, -r0], ...bez([xt + 4, -r0], [xt - 20, -r0 - 10], [xt - 48, -40], [xt - 66, -56], 10).slice(1),
    ...bez([xt - 66, -56], [xt - 50, -28], [xt - 42, -10], [xt - 40, 0], 8).slice(1), ...bez([xt - 40, 0], [xt - 42, 10], [xt - 50, 28], [xt - 66, 56], 8).slice(1),
    ...bez([xt - 66, 56], [xt - 48, 40], [xt - 20, r0 + 10], [xt + 4, r0], 10).slice(1)];
  const fin = [[-8, -hw(-8) + 3], ...bez([-8, -hw(-8)], [8, -hw(8) - 30], [34, -hw(34) - 32], [56, -hw(56) + 3], 16).slice(1)];
  const finTop = [...fin, ...[]];
  const vfin = [[8, hw(8) - 2], ...bez([8, hw(8)], [14, hw(14) + 18], [30, hw(30) + 20], [42, hw(42) - 2], 12).slice(1)];
  const head = bodyBand(hw, 64, xn + 8, -13, 0), body = bodyBand(hw, -18, 64, -10, -13), band = bodyBand(hw, xt - 2, -18, 0, -10);
  const w = (p, a = 1.6, s = seed) => wob(p, a, s, 5);
  const ops = [
    // brushed colour (bharni)
    S('fill', 0.95, 1.35, { p: tail, c: pal.tail, a: 0.2, sp: 8 }),
    S('fill', 1.0, 1.3, { p: fin, c: pal.fin, a: -0.4, sp: 7 }),
    S('fill', 1.05, 1.3, { p: vfin, c: pal.fin, a: 0.4, sp: 7 }),
    S('fill', 0.85, 1.25, { p: head, c: pal.head, a: 1.2, sp: 9 }),
    S('fill', 0.95, 1.45, { p: body, c: pal.body, a: 1.3, sp: 9 }),
    S('fill', 1.1, 1.5, { p: band, c: pal.band, a: 1.4, sp: 9 }),
    // fine line patterns (kachni)
    S('scales', 1.45, 2.1, { p: body, r: 11, lw: 2.2, dir: 1 }),
    S('hatch', 1.55, 2.05, { p: band, a: Math.PI / 2 + 0.12, sp: 9, lw: 2.2 }),
    S('hatch', 1.65, 2.15, { p: tail, a: 0.05, sp: 7, lw: 1.7 }),
    S('hatch', 1.7, 2.05, { p: fin, a: 1.9, sp: 7, lw: 1.6 }),
    S('hatch', 1.75, 2.05, { p: vfin, a: 1.2, sp: 7, lw: 1.6 }),
    S('dots', 1.6, 2.1, { d: Array.from({ length: 9 }, (_, i) => [74 + i * 5.6, -hw(74 + i * 5.6) * 0.62 + 2, 2.4]).concat(Array.from({ length: 8 }, (_, i) => [74 + i * 5.6, hw(74 + i * 5.6) * 0.6, 2.4])) }),
    // double outlines
    S('dbl', 0.45, 0.95, { p: w(tail, 1.2, seed + 3), w: 7, gap: 2.6, gc: pal.gap, closed: true }),
    S('dbl', 0.6, 1.0, { p: w(fin, 1, seed + 4), w: 6, gap: 2.2, gc: pal.gap }),
    S('dbl', 0.65, 1.0, { p: w(vfin, 1, seed + 5), w: 6, gap: 2.2, gc: pal.gap }),
    S('dbl', 0, 0.8, { p: w(outline, 1.8), w: 8, gap: 3, gc: pal.gap, closed: true }),
    S('dbl', 0.7, 0.95, { p: gillArc(hw, 64, -13), w: 6, gap: 2.2, gc: pal.gap }),
    S('line', 0.8, 1.0, { p: gillArc(hw, 55, -11), w: 2.4 }),
    S('line', 0.85, 1.05, { p: bez([xn + 7, 7], [xn - 2, 12], [xn - 10, 12], [xn - 16, 9], 8), w: 3 }),
    // big almond eye
    S('pop', 0.55, 0.8, { p: ell(98, -9, 17, 13, 30), c: C.white, edge: 3.2, o: [98, -9] }),
    S('pop', 0.75, 0.95, { p: ell(100, -9, 7.5, 7.5, 20), c: C.ink, o: [100, -9] }),
    S('pop', 0.9, 1.05, { p: ell(102, -11.5, 2.4, 2.4, 10), c: C.white, o: [102, -11.5] }),
    S('line', 0.7, 0.95, { p: bez([80, -24], [90, -31], [106, -31], [116, -22], 10), w: 2.6 }),
  ];
  return { ops: prep(ops), hw, xt, xn };
}

// ── leaf (base at origin, points to +x) ──
function makeLeaf(len, wid, seed, cA = C.grn, cB = C.grnL) {
  const top = [], bot = [];
  for (let i = 0; i <= 18; i++) { const x = len * i / 18, h = wid * Math.pow(Math.sin(Math.PI * Math.pow(i / 18, 0.9)), 0.85); top.push([x, -h]); bot.push([x, h]); }
  const out = [...top, ...bot.slice(0, -1).reverse()];
  const upper = [...top, [0, 0]], lower = [...bot, [0, 0]];
  return prep([
    S('fill', 0.12, 0.4, { p: upper, c: cA, a: 0.9, sp: 6 }),
    S('fill', 0.18, 0.45, { p: lower, c: cB, a: -0.9, sp: 6 }),
    S('hatch', 0.38, 0.7, { p: upper, a: -0.75, sp: 6.5, lw: 1.3 }),
    S('dbl', 0, 0.32, { p: wob(out, 0.8, seed, 4), w: 5, gap: 1.8, gc: C.yel, closed: true }),
    S('line', 0.25, 0.45, { p: [[2, 0], [len * 0.94, 0]], w: 2 }),
  ]);
}
// ── round flower (centre at origin) ──
function makeFlower(r, petal, heart, seed) {
  const ops = [], n = 8;
  for (let k = 0; k < n; k++) { const a = k / n * TAU, cx = Math.cos(a) * r * 0.62, cy = Math.sin(a) * r * 0.62;
    const p = ell(0, 0, r * 0.42, r * 0.26, 16).map(([x, y]) => [cx + x * Math.cos(a) - y * Math.sin(a), cy + x * Math.sin(a) + y * Math.cos(a)]);
    ops.push(S('pop', k * 0.04, k * 0.04 + 0.22, { p, c: petal, edge: 1.8, o: [cx, cy] })); }
  ops.push(S('pop', 0.3, 0.5, { p: ell(0, 0, r * 0.36, r * 0.36, 20), c: heart, edge: 2.2, o: [0, 0] }));
  ops.push(S('dots', 0.45, 0.7, { d: Array.from({ length: 6 }, (_, k) => [Math.cos(k / 6 * TAU) * r * 0.18, Math.sin(k / 6 * TAU) * r * 0.18, 1.6]).concat([[0, 0, 2.2]]) }));
  return prep(ops);
}
// small five-petal filler flower and other space-fillers (no empty space)
function makeFiller(kind, s, seed) {
  const r = mulberry(seed), ops = [];
  if (kind === 0) {   // five-petal flower
    const c = [C.ver, C.pink, C.org, C.ind][Math.floor(r() * 4)];
    for (let k = 0; k < 5; k++) { const a = k / 5 * TAU - Math.PI / 2, cx = Math.cos(a) * s * 0.5, cy = Math.sin(a) * s * 0.5;
      ops.push(S('pop', k * 0.05, k * 0.05 + 0.25, { p: ell(cx, cy, s * 0.42, s * 0.42, 14), c, edge: 1.4, o: [cx, cy] })); }
    ops.push(S('pop', 0.25, 0.45, { p: ell(0, 0, s * 0.3, s * 0.3, 12), c: C.yel, edge: 1.4, o: [0, 0] }));
  } else if (kind === 1) {   // dot triangle
    const d = []; for (let i = 0; i < 3; i++) for (let j = 0; j <= i; j++) d.push([(j - i / 2) * s * 0.55, (i - 1) * s * 0.5, s * 0.14]);
    ops.push(S('dots', 0, 0.5, { d }));
  } else if (kind === 2) {   // sprig: a curl with two leaves
    const stem = bez([0, s], [s * 0.4, s * 0.3], [-s * 0.5, -s * 0.3], [0, -s], 14);
    ops.push(S('line', 0, 0.35, { p: stem, w: 2.2 }));
    for (const [u, sd] of [[0.35, 1], [0.65, -1]]) { const [x, y] = stem[Math.round(u * 14)];
      const lf = ell(0, 0, s * 0.42, s * 0.18, 14).map(([a, b]) => [x + sd * (a + s * 0.4), y + b - s * 0.1]);
      ops.push(S('pop', 0.25 + u * 0.3, 0.5 + u * 0.3, { p: lf, c: C.grn, edge: 1.4, o: [x, y] })); }
  } else {   // spiral curl
    const p = []; for (let a = 0; a < 3.2 * Math.PI; a += 0.2) { const d = s * 0.08 * a; p.push([Math.cos(a) * d, Math.sin(a) * d]); }
    ops.push(S('line', 0, 0.5, { p, w: 2.2, c: [C.ind, C.ver][Math.floor(r() * 2)] }));
  }
  return prep(ops);
}

// ── parrot (feet at origin, faces +x). Wing drawn separately so it can flap ──
function makeParrot(body, seed) {
  const bodyP = ell(-2, -24, 27, 15, 30).map(([x, y]) => { const a = -0.5, dx = x + 2, dy = y + 24; return [-2 + dx * Math.cos(a) - dy * Math.sin(a), -24 + dx * Math.sin(a) + dy * Math.cos(a)]; });
  const tail = [[-18, -18], [-66, 8], [-70, 16], [-58, 16], [-14, -8]];
  const beak = [...bez([28, -46], [40, -48], [44, -38], [37, -30], 8), [31, -36]];
  const ops = prep([
    S('pop', 0, 0.01, { p: tail, c: body, edge: 0 }),
    S('hatch', 0, 0.01, { p: tail, a: 0.4, sp: 5, lw: 1.3 }),
    S('pop', 0, 0.01, { p: bodyP, c: body, edge: 0 }),
    S('pop', 0, 0.01, { p: ell(20, -42, 13, 12, 24), c: body, edge: 0 }),
    S('dbl', 0, 0.01, { p: wob(tail, 0.6, seed), w: 4.5, gap: 1.6, gc: C.yel, closed: true }),
    S('dbl', 0, 0.01, { p: wob(bodyP, 0.6, seed + 1), w: 4.5, gap: 1.6, gc: C.yel, closed: true }),
    S('dbl', 0, 0.01, { p: ell(20, -42, 13, 12, 24, -2.3, 2.4), w: 4.5, gap: 1.6, gc: C.yel }),
    S('line', 0, 0.01, { p: ell(20, -42, 13, 12, 12, 1.6, 2.9), w: 3, c: C.ver }),
    S('pop', 0, 0.01, { p: beak, c: C.ver, edge: 2.2 }),
    S('pop', 0, 0.01, { p: ell(23, -45, 5, 4.5, 14), c: C.white, edge: 2 }),
    S('pop', 0, 0.01, { p: ell(24, -45, 2.3, 2.3, 10), c: C.ink }),
  ]);
  const wing = prep([
    S('pop', 0, 0.01, { p: [[0, 0], ...bez([0, 0], [-10, -12], [-34, -10], [-44, 4], 10), ...bez([-44, 4], [-30, 8], [-12, 8], [0, 0], 10)], c: C.yel, edge: 0 }),
    S('scales', 0, 0.01, { p: [[0, 0], ...bez([0, 0], [-10, -12], [-34, -10], [-44, 4], 10), ...bez([-44, 4], [-30, 8], [-12, 8], [0, 0], 10)], r: 5, lw: 1.3, dir: 1 }),
    S('dbl', 0, 0.01, { p: [[0, 0], ...bez([0, 0], [-10, -12], [-34, -10], [-44, 4], 10), ...bez([-44, 4], [-30, 8], [-12, 8], [0, 0], 10)], w: 4, gap: 1.4, gc: C.ver, closed: true }),
  ]);
  const legs = prep([S('line', 0, 0.01, { p: [[-4, -12], [-2, 0]], w: 2.6, c: C.org }), S('line', 0, 0.01, { p: [[4, -11], [6, 0]], w: 2.6, c: C.org })]);
  return { ops, wing, legs, shoulder: [8, -30] };
}

// ── peacock (feet at origin, faces +x) ──
function tube(cl, w0, w1) {   // outline of a tapered tube along centreline cl
  const L = [], Rr = [];
  for (let i = 0; i < cl.length; i++) { const a = cl[Math.max(0, i - 1)], b = cl[Math.min(cl.length - 1, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1, w = lerp(w0, w1, i / (cl.length - 1)) / 2;
    L.push([cl[i][0] - dy / l * w, cl[i][1] + dx / l * w]); Rr.push([cl[i][0] + dy / l * w, cl[i][1] - dx / l * w]); }
  return [...L, ...Rr.reverse()];
}
function makePeacock(seed, gc) {
  const rot = (p, a, cx, cy) => p.map(([x, y]) => { const dx = x - cx, dy = y - cy; return [cx + dx * Math.cos(a) - dy * Math.sin(a), cy + dx * Math.sin(a) + dy * Math.cos(a)]; });
  const body = rot(ell(0, -150, 50, 66, 40), 0.35, 0, -150);
  const neckCl = bez([18, -196], [44, -240], [14, -268], [50, -300], 20), neck = tube(neckCl, 34, 18);
  const train = [...bez([-34, -176], [-110, -214], [-220, -186], [-290, -96], 18), ...bez([-290, -96], [-300, -40], [-250, -4], [-190, -8], 12).slice(1),
    ...bez([-190, -8], [-120, -30], [-70, -70], [-30, -112], 12).slice(1)];
  const plumeEnds = [[-238, -168], [-268, -128], [-282, -80], [-266, -36], [-222, -16]];
  const wing = rot([[30, -178], ...bez([30, -178], [0, -196], [-50, -160], [-62, -112], 12), ...bez([-62, -112], [-30, -118], [10, -140], [30, -178], 12)], 0, 0, 0);
  const d = []; { const r = mulberry(seed); for (let y = -205; y < -90; y += 13) for (let x = -50; x < 55; x += 13) { const px = x + ((y / 13) % 2 ? 6 : 0), py = y; const dx = px, dy = py + 150, ca = Math.cos(-0.35), sa = Math.sin(-0.35), lx = dx * ca - dy * sa, ly = dx * sa + dy * ca; if ((lx / 44) ** 2 + (ly / 60) ** 2 < 1) d.push([px, py, 2.6]); } }
  const ops = [
    S('fill', 0.35, 0.8, { p: train, c: C.grn, a: 0.5, sp: 10 }),
    S('hatch', 0.75, 1.3, { p: train, a: -0.5, sp: 8, lw: 1.5 }),
  ];
  plumeEnds.forEach(([x, y], i) => {
    const t = 0.5 + i * 0.1;
    ops.push(S('line', t, t + 0.3, { p: bez([-40, -130], [lerp(-40, x, 0.4), lerp(-130, y, 0.2) - 10], [lerp(-40, x, 0.8), y], [x, y], 12), w: 3 }));
    ops.push(S('pop', t + 0.25, t + 0.5, { p: ell(x, y, 22, 17, 24), c: C.yel, edge: 2.4, o: [x, y] }));
    ops.push(S('pop', t + 0.32, t + 0.55, { p: ell(x + 2, y, 14, 11, 20), c: C.ver, edge: 1.8, o: [x, y] }));
    ops.push(S('pop', t + 0.4, t + 0.6, { p: ell(x + 3, y, 7, 6, 16), c: C.ind, edge: 1.2, o: [x, y] }));
  });
  ops.push(
    S('fill', 0.4, 0.8, { p: body, c: C.ind, a: 1.0, sp: 10 }),
    S('dots', 0.8, 1.3, { d, c: C.white }),
    S('fill', 0.7, 1.0, { p: wing, c: C.yel, a: -0.6, sp: 8 }),
    S('scales', 0.95, 1.4, { p: wing, r: 7, lw: 1.6, dir: 1 }),
    S('dbl', 0.6, 0.95, { p: wob(wing, 0.8, seed + 2), w: 5, gap: 1.8, gc: C.ver, closed: true }),
    S('dbl', 0, 0.55, { p: wob(train, 1.4, seed + 3), w: 7, gap: 2.6, gc, closed: true }),
    S('dbl', 0.1, 0.55, { p: wob(body, 1.0, seed + 4), w: 7, gap: 2.6, gc, closed: true }),
    S('line', 0.55, 0.8, { p: [[-8, -92], [-12, 0]], w: 8 }), S('line', 0.6, 0.85, { p: [[12, -90], [18, 0]], w: 8 }),
    S('line', 0.8, 0.95, { p: [[-26, 0], [-12, 0], [4, 0]], w: 6.5 }), S('line', 0.85, 1.0, { p: [[4, 0], [18, 0], [34, 0]], w: 6.5 }),
    S('line', 0.55, 0.8, { p: [[-8, -92], [-12, 0]], w: 4.5, c: C.org }), S('line', 0.6, 0.85, { p: [[12, -90], [18, 0]], w: 4.5, c: C.org }),
    S('line', 0.8, 0.95, { p: [[-26, 0], [-12, 0], [4, 0]], w: 3.4, c: C.org }), S('line', 0.85, 1.0, { p: [[4, 0], [18, 0], [34, 0]], w: 3.4, c: C.org }),
  );
  const headOps = [
    S('fill', 0.5, 0.85, { p: neck, c: C.ind, a: 0.2, sp: 8 }),
    S('scales', 0.85, 1.3, { p: neck, r: 6, c: C.white, lw: 1.5, dir: 1 }),
    S('dbl', 0.2, 0.6, { p: wob(neck, 0.7, seed + 5), w: 6, gap: 2.2, gc, closed: true }),
    S('pop', 0.55, 0.75, { p: [[62, -312], [88, -302], [62, -294]], c: C.org, edge: 2.2, o: [62, -303] }),
    S('pop', 0.5, 0.7, { p: ell(52, -304, 16, 15, 24), c: C.ind, edge: 3, o: [52, -304] }),
    S('pop', 0.7, 0.85, { p: ell(56, -306, 7, 5, 16), c: C.white, edge: 1.6, o: [56, -306] }),
    S('pop', 0.8, 0.9, { p: ell(57, -306, 2.6, 2.6, 10), c: C.ink, o: [57, -306] }),
  ];
  [[34, -352], [46, -358], [58, -352]].forEach(([x, y], i) => {
    headOps.push(S('line', 0.75 + i * 0.05, 0.95 + i * 0.05, { p: [[48, -318], [x, y]], w: 2.4 }));
    headOps.push(S('pop', 0.9 + i * 0.05, 1.05 + i * 0.05, { p: ell(x, y, 5.5, 5.5, 12), c: C.ver, edge: 1.6, o: [x, y] }));
  });
  return { ops: prep(ops), head: prep(headOps), pivot: [18, -196] };
}

// ── sun (face at origin) — mouth and eyes are drawn live so it can smile ──
function makeSun(seed) {
  const ops = [], R = 86;
  for (let k = 0; k < 18; k++) { const a = k / 18 * TAU - Math.PI / 2, a1 = a - 0.16, a2 = a + 0.16, r0 = 100, r1 = k % 2 ? 140 : 156;
    const p = [[Math.cos(a1) * r0, Math.sin(a1) * r0], [Math.cos(a) * r1, Math.sin(a) * r1], [Math.cos(a2) * r0, Math.sin(a2) * r0]];
    ops.push(S('pop', 0.55 + k * 0.035, 0.8 + k * 0.035, { p, c: k % 2 ? C.org : C.ver, edge: 2.4, o: [Math.cos(a) * r0, Math.sin(a) * r0] })); }
  ops.push(S('fill', 0.2, 0.6, { p: ell(0, 0, R, R, 60), c: C.yel, a: 0.8, sp: 10 }));
  ops.push(S('dots', 0.95, 1.4, { d: Array.from({ length: 30 }, (_, k) => [Math.cos(k / 30 * TAU) * (R + 1), Math.sin(k / 30 * TAU) * (R + 1), 2.2]), c: C.ver }));
  ops.push(S('dbl', 0, 0.55, { p: wob(ell(0, 0, R, R, 80), 1.2, seed), w: 8, gap: 3, gc: C.ver, closed: true }));
  ops.push(S('dbl', 0.15, 0.6, { p: ell(0, 0, 96, 96, 80), w: 5, gap: 1.6, gc: C.yel, closed: true }));
  // brows and a long Mithila nose
  ops.push(S('line', 0.5, 0.7, { p: bez([-50, -30], [-40, -44], [-18, -44], [-6, -32], 10), w: 3.4 }));
  ops.push(S('line', 0.5, 0.7, { p: bez([50, -30], [40, -44], [18, -44], [6, -32], 10), w: 3.4 }));
  ops.push(S('line', 0.6, 0.85, { p: bez([-4, -30], [-8, 0], [-14, 12], [-2, 16], 12), w: 3.2 }));
  ops.push(S('pop', 0.8, 1.0, { p: ell(-44, 22, 11, 7, 16), c: C.pink, o: [-44, 22] }), S('pop', 0.85, 1.05, { p: ell(44, 22, 11, 7, 16), c: C.pink, o: [44, 22] }));
  return prep(ops);
}
function sunFace(g, sm, blink, lt) {   // sm 0 → 1 smile, blink 0 → 1 closed
  if (lt < 0.7) return; const a = clamp((lt - 0.7) / 0.25);
  g.globalAlpha = a; g.lineCap = 'round'; g.lineJoin = 'round';
  for (const sx of [-1, 1]) {   // almond eyes
    const cx = sx * 27, cy = -18, rw = 17, rh = 9 * (1 - blink * 0.85) * (1 - sm * 0.25);
    g.beginPath(); g.moveTo(cx - rw, cy); g.quadraticCurveTo(cx, cy - rh * 2, cx + rw, cy); g.quadraticCurveTo(cx, cy + rh * 1.2, cx - rw, cy); g.closePath();
    g.fillStyle = C.white; g.fill(); g.strokeStyle = C.ink; g.lineWidth = 3; g.stroke();
    if (blink < 0.6) { g.save(); g.clip(); g.fillStyle = C.ink; g.beginPath(); g.arc(cx + sx * 2, cy - 1, 6, 0, TAU); g.fill(); g.restore(); }
    g.beginPath(); g.moveTo(cx + sx * rw, cy); g.lineTo(cx + sx * (rw + 9), cy - 3); g.stroke();   // Mithila eye tail
  }
  // lips: upper and lower, the corners lift with the smile
  const lift = 11 * sm, w = 22 + 5 * sm, y0 = 40;
  g.beginPath(); g.moveTo(-w, y0 - lift); g.quadraticCurveTo(-8, y0 - 9, 0, y0 - 5); g.quadraticCurveTo(8, y0 - 9, w, y0 - lift);
  g.quadraticCurveTo(0, y0 + 13 + sm * 6, -w, y0 - lift); g.closePath(); g.fillStyle = C.ver; g.fill(); g.strokeStyle = C.ink; g.lineWidth = 2.8; g.stroke();
  g.beginPath(); g.moveTo(-w + 2, y0 - lift); g.quadraticCurveTo(0, y0 + 2 + sm * 7, w - 2, y0 - lift); g.lineWidth = 2; g.stroke();
  g.globalAlpha = 1;
}
// ── moon: pale face with an indigo crescent; star ring ──
function makeMoon(seed) {
  const R = 80, ops = [];
  const cres = [...ell(0, 0, R, R, 40, -Math.PI / 2, Math.PI / 2), ...ell(-26, 0, R * 0.92, R, 40, Math.PI / 2 - 0.02, -Math.PI / 2 + 0.02).slice(1)];
  const cresIn = [...ell(0, 0, R, R, 30, -1.1, 1.1), ...ell(-26, 0, R * 0.92, R, 30, 1.1, -1.1).reverse().reverse()];
  ops.push(S('fill', 0.2, 0.55, { p: ell(0, 0, R, R, 60), c: C.white, a: 0.8, sp: 10 }));
  ops.push(S('fill', 0.45, 0.75, { p: cres, c: C.indL, a: 1.3, sp: 7 }));
  ops.push(S('hatch', 0.7, 1.1, { p: cres, a: 1.1, sp: 6, lw: 1.5 }));
  ops.push(S('dbl', 0, 0.5, { p: wob(ell(0, 0, R, R, 80), 1.2, seed), w: 8, gap: 3, gc: C.ind, closed: true }));
  ops.push(S('dbl', 0.4, 0.75, { p: ell(-26, 0, R * 0.92, R, 40, Math.PI / 2 - 0.02, -Math.PI / 2 + 0.02), w: 5, gap: 1.6, gc: C.ind }));
  ops.push(S('line', 0.55, 0.8, { p: bez([-6, -34], [-10, -4], [-16, 8], [-4, 12], 12), w: 3 }));
  ops.push(S('line', 0.5, 0.7, { p: bez([-50, -34], [-40, -44], [-22, -42], [-12, -32], 10), w: 3 }));
  ops.push(S('pop', 0.8, 1.0, { p: ell(-46, 16, 9, 6, 14), c: C.pinkL, o: [-46, 16] }));
  for (let k = 0; k < 12; k++) { const a = k / 12 * TAU, x = Math.cos(a) * 120, y = Math.sin(a) * 120, s = k % 2 ? 9 : 13, p = [];
    for (let j = 0; j < 8; j++) { const b = j / 8 * TAU - Math.PI / 2, d = j % 2 ? s * 0.38 : s; p.push([x + Math.cos(b) * d, y + Math.sin(b) * d]); }
    ops.push(S('pop', 0.6 + k * 0.04, 0.85 + k * 0.04, { p, c: k % 2 ? C.yel : C.white, edge: 2, o: [x, y] })); }
  return prep(ops);
}
function moonFace(g, open, lt) {
  if (lt < 0.6) return; g.globalAlpha = clamp((lt - 0.6) / 0.25); g.lineCap = 'round'; g.strokeStyle = C.ink; g.lineWidth = 3;
  const cx = -30, cy = -18, rw = 15, rh = 8 * open;
  if (open > 0.05) { g.beginPath(); g.moveTo(cx - rw, cy); g.quadraticCurveTo(cx, cy - rh * 2, cx + rw, cy); g.quadraticCurveTo(cx, cy + rh, cx - rw, cy); g.closePath(); g.fillStyle = C.white; g.fill(); g.stroke();
    g.save(); g.clip(); g.fillStyle = C.ink; g.beginPath(); g.arc(cx - 3, cy - 1, 5.5, 0, TAU); g.fill(); g.restore(); }
  else { g.beginPath(); g.moveTo(cx - rw, cy); g.quadraticCurveTo(cx, cy + 9, cx + rw, cy); g.stroke(); for (let i = 0; i < 4; i++) { const x = cx - 10 + i * 7; g.beginPath(); g.moveTo(x, cy + 5); g.lineTo(x - 1, cy + 11); g.stroke(); } }
  g.beginPath(); g.moveTo(cx - rw, cy); g.lineTo(cx - rw - 8, cy - 3); g.stroke();
  g.beginPath(); g.moveTo(-34, 34); g.quadraticCurveTo(-24, 28, -12, 32); g.quadraticCurveTo(-24, 44, -34, 34); g.closePath(); g.fillStyle = C.ver; g.fill(); g.lineWidth = 2.4; g.stroke();
  g.globalAlpha = 1;
}
