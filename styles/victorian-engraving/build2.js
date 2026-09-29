// ── builders, part 2: ideas, boot, crane, engine, banner, cards ─────────────────────────────────
function buildWing() {
  const P = newPart(-12, -92, 128, 20, { seed: 31, s: 4.6 });
  const d = 'M 0 0 C 20 -30 60 -72 118 -82 C 110 -68 102 -60 94 -56 C 104 -52 106 -44 102 -38 C 92 -40 82 -36 76 -30 C 82 -26 84 -18 80 -12 C 68 -14 56 -10 48 -4 C 52 0 50 6 44 8 C 28 10 12 8 0 0 Z';
  region(P, d, lin(0, 0, 110, -80, [[0, .45], [1, .08]]), { a: -35, wob: .3, xk: .4, lw: 2.2, tint: '#f6f0e4' });
  for (const q of ['M 8 -6 C 30 -30 60 -54 94 -56', 'M 20 -4 C 40 -18 60 -28 76 -30', 'M 26 2 C 36 -2 44 -4 48 -4', 'M 4 -2 C 26 -40 60 -68 110 -78'])
    inkStroke(P, q, 1.4);
  A.wing = finish(P, { seed: 31, rim: 3 });
}
function gearPath(ro, n, td, ri, hub, spokes) {
  const p = new Path2D(), rb = ro - td;
  for (let k = 0; k < n; k++) {
    const a0 = k / n * TAU, w = TAU / n;
    const pts = [[rb, a0], [ro, a0 + w * .18], [ro, a0 + w * .45], [rb, a0 + w * .63]];
    pts.forEach(([r, a], j) => (k === 0 && j === 0) ? p.moveTo(Math.cos(a) * r, Math.sin(a) * r) : p.lineTo(Math.cos(a) * r, Math.sin(a) * r));
    p.arc(0, 0, rb, a0 + w * .63, a0 + w);
  }
  p.closePath();
  if (spokes) for (let k = 0; k < spokes; k++) {
    const a0 = k / spokes * TAU + .16, a1 = (k + 1) / spokes * TAU - .16;
    p.moveTo(Math.cos(a0) * (hub + 6), Math.sin(a0) * (hub + 6)); p.arc(0, 0, ri, a0, a1); p.arc(0, 0, hub + 6, a1, a0, true); p.closePath();
  } else { p.moveTo(hub, 0); p.arc(0, 0, hub, 0, TAU); }
  return p;
}
function buildGear(ro, n, o = {}) {
  const P = newPart(-ro - 4, -ro - 4, ro + 4, ro + 4, { seed: o.seed || ro, s: o.s || 5 });
  const gp = gearPath(ro, n, o.td || ro * .16, ro * .66, ro * .2, o.spokes || 0);
  region(P, gp, rad(0, 0, ro * .1, ro, [[0, .2], [.6, .35], [1, .62]], -ro * .3, -ro * .3), { ring: [0, 0], s: o.s || 5, rule: 'evenodd', tint: o.tint || '#8e9294', lw: 2.4 });
  inkStroke(P, circ(0, 0, ro * .66), 1.6); inkFill(P, circ(0, 0, ro * .11)); inkStroke(P, circ(0, 0, ro * .2), 2);
  return finish(P, { seed: ro, rim: o.rim ?? 3 });
}
function buildBulb() {
  const P = newPart(-72, -92, 72, 104, { seed: 41, s: 4.6 });
  const glass = region(P, 'M 0 -86 C 52 -86 72 -40 62 -5 C 54 20 32 36 27 56 L -27 56 C -32 36 -54 20 -62 -5 C -72 -40 -52 -86 0 -86 Z',
    rad(0, -20, 5, 85, [[0, .04], [.7, .16], [1, .5]], -24, -48), { ring: [-24, -48], xk: .4, tint: '#f4dd76' });
  inkStroke(P, 'M -12 54 L -9 2 M 12 54 L 9 2', 2); inkStroke(P, 'M -9 2 L -6 -12 L -3 2 L 0 -12 L 3 2 L 6 -12 L 9 2', 1.8);
  inkStroke(P, 'M -40 -60 C -30 -72 -16 -76 -4 -76', 3, null, '#fffaf0');
  region(P, 'M -28 56 L 28 56 L 26 94 L -26 94 Z', lin(-28, 0, 28, 0, [[0, .7], [.4, .25], [1, .75]]), { a: 0, s: 3.6, tint: '#bf9a4e' });
  for (let k = 0; k < 4; k++) inkStroke(P, `M -27 ${64 + k * 8} C -10 ${68 + k * 8} 10 ${68 + k * 8} 27 ${64 + k * 8}`, 1.8);
  region(P, 'M -12 94 L 12 94 L 8 102 L -8 102 Z', .9, { a: 0, s: 3, lw: 1.8 });
  A.bulb = finish(P, { seed: 41, rim: 3 });
}
function buildCup() {
  const P = newPart(-70, -45, 76, 50, { seed: 43, s: 4.4 });
  region(P, ell(0, 36, 64, 11), lin(0, 26, 0, 48, [[0, .1], [1, .45]]), { a: 90, tint: '#e3ebef' });
  region(P, 'M -46 -30 L 46 -30 C 45 10 30 32 0 34 C -30 32 -45 10 -46 -30 Z', lin(-46, 0, 46, 0, [[0, .45], [.35, .06], [1, .5]]), { a: 0, tint: '#e3ebef' });
  tintFill(P, pth('M -45 -18 L 45 -18 L 44 -8 L -44 -8 Z'), '#4a6ea3');
  inkStroke(P, 'M -45 -18 L 45 -18 M -44 -8 L 44 -8', 1.4);
  inkStroke(P, ell(0, -30, 46, 7), 2.2); inkStroke(P, 'M 45 -18 C 70 -22 72 10 40 14', 6);
  A.cup = finish(P, { seed: 43, rim: 3 });
}
function buildWatch() {
  const P = newPart(-56, -72, 56, 56, { seed: 47, s: 4.4 });
  region(P, 'M -8 -48 L -8 -62 L 8 -62 L 8 -48 Z', .5, { a: 0, s: 3, tint: '#c7a458', lw: 2 });
  inkStroke(P, circ(0, -66, 7), 3);
  region(P, circ(0, 0, 48), rad(0, 0, 36, 48, [[0, .3], [1, .7]]), { ring: [0, 0], s: 3.6, tint: '#c7a458' });
  region(P, circ(0, 0, 38), rad(0, 0, 4, 38, [[0, .02], [1, .14]], -12, -12), { ring: [-12, -12], tint: '#f7f0df' });
  for (let k = 0; k < 12; k++) { const a = k / 12 * TAU; inkStroke(P, `M ${Math.cos(a) * 30} ${Math.sin(a) * 30} L ${Math.cos(a) * 35} ${Math.sin(a) * 35}`, k % 3 ? 1.6 : 3); }
  inkStroke(P, 'M 0 0 L 12 -18 M 0 0 L -4 26', 2.6); inkFill(P, circ(0, 0, 3.5));
  A.watch = finish(P, { seed: 47, rim: 3 });
}
function buildSnail() {
  const P = newPart(-72, -80, 96, 34, { seed: 53, s: 4.2 });
  region(P, 'M -64 22 C -40 8 20 6 48 10 C 60 4 68 -10 72 -24 C 76 -30 84 -28 84 -22 C 82 -8 76 6 70 16 C 62 26 30 28 -64 26 Z',
    lin(0, 0, 0, 28, [[0, .14], [1, .4]]), { a: 0, st: 1, lk: .5, tint: '#cdbf9f' });
  inkStroke(P, 'M 74 -20 L 84 -52 M 68 -16 L 70 -48', 2.2); inkFill(P, circ(84, -54, 4)); inkFill(P, circ(70, -50, 4));
  const shell = region(P, circ(-8, -22, 40), rad(-8, -22, 4, 40, [[0, .3], [1, .62]], -20, -34), { ring: [-4, -18], s: 4, tint: '#b87744' });
  const sp = new Path2D(); for (let k = 0; k <= 120; k++) { const a = k / 120 * TAU * 2.6, r = 36 * (1 - k / 138); const px = -6 + Math.cos(a + 1) * r, py = -20 + Math.sin(a + 1) * r; k ? sp.lineTo(px, py) : sp.moveTo(px, py); }
  inkStroke(P, sp, 2.4);
  // a very small top hat: it is, after all, a committee snail
  region(P, 'M 62 -28 L 64 -52 L 86 -54 L 86 -30 Z', .85, { a: 0, s: 3, tint: '#2e2b31', lw: 1.8 });
  region(P, 'M 56 -28 L 92 -31 L 92 -26 L 56 -24 Z', .85, { a: 0, s: 3, tint: '#2e2b31', lw: 1.8 });
  A.snail = finish(P, { seed: 53, rim: 3 });
}
function buildBoot() {                                   // origin = under the ball of the foot, on the sole
  const P = newPart(-255, -1560, 375, 12, { seed: 61, s: 6 });
  region(P, 'M -204 -300 L -214 -1560 L 126 -1560 L 104 -300 C 60 -330 -140 -330 -204 -300 Z', lin(-214, 0, 126, 0, [[0, .62], [.45, .32], [1, .58]]), { a: 0, s: 7, wob: .15, tint: '#777a7f' });
  for (let k = 0; k < 8; k++) inkStroke(P, `M ${-186 + k * 40} -1560 L ${-180 + k * 38} -330`, 1.4, null, 'rgba(250,244,230,.7)');
  inkStroke(P, 'M -150 -380 C -120 -358 -60 -356 -20 -386', 2); inkStroke(P, 'M -40 -430 C 0 -408 50 -408 92 -432', 2); inkStroke(P, 'M -190 -520 C -150 -500 -110 -505 -80 -530', 1.6);
  const boot = 'M -240 0 L -240 -70 C -240 -130 -230 -200 -200 -250 L -176 -318 L 94 -318 C 98 -280 112 -250 144 -222 C 196 -190 270 -178 318 -140 C 360 -104 364 -30 336 0 Z';
  region(P, boot, rad(210, -110, 10, 380, [[0, .2], [.3, .55], [.7, .8], [1, .9]], 240, -150), { a: 20, s: 5, tint: '#3a3236' });
  inkStroke(P, 'M 170 -196 C 232 -170 290 -140 300 -60', 2.4); inkStroke(P, 'M 186 -186 C 240 -162 284 -132 292 -64', 1.2, null, 'rgba(240,230,210,.7)');
  inkStroke(P, 'M 40 -150 C 60 -120 110 -110 150 -128', 1.8); inkStroke(P, 'M -150 -210 C -170 -150 -176 -100 -170 -64', 1.8);
  region(P, 'M -240 0 L -240 -64 L -128 -64 L -118 0 Z', .88, { a: 0, s: 4, tint: '#1f1c1f' });
  region(P, 'M -118 -22 L 346 -22 C 352 -14 348 -4 340 0 L -118 0 Z', .45, { a: 0, s: 4, tint: '#6d5540' });
  for (let k = 0; k < 16; k++) inkStroke(P, `M ${-110 + k * 28} -30 L ${-96 + k * 28} -30`, 2, null, '#e8dcc2');
  region(P, 'M -206 -318 L 96 -318 C 100 -290 108 -262 122 -238 C 60 -252 -60 -242 -198 -226 C -212 -262 -212 -292 -206 -318 Z', lin(0, -318, 0, -226, [[0, .08], [1, .3]]), { a: 90, s: 4.6, tint: '#e9e2d2' });
  for (let k = 0; k < 4; k++) { const by = -304 + k * 22, bx = -120 + k * 2; inkFill(P, circ(bx, by, 6.5)); inkFill(P, circ(bx - 2, by - 2, 2), '#efe4cf'); }
  A.boot = finish(P, { seed: 61 });
}
function buildBurst() {
  const P = newPart(-360, -230, 360, 230, { seed: 67, s: 5 });
  const pts = [], r = rng(8); for (let k = 0; k < 26; k++) { const a = k / 26 * TAU, rr = (k & 1 ? .66 : 1) * (1 - r() * .12); pts.push([Math.cos(a) * 340 * rr, Math.sin(a) * 210 * rr]); }
  region(P, poly(pts), rad(0, 0, 20, 330, [[0, .06], [1, .45]]), { ray: [0, 0, 150], xk: 0, tint: '#f2c24b', lw: 3.4 });
  engText(P, 'SQUASH!', 0, 46, `128px ${FAT}`, { fs: 120, d0: .6, d1: .95, tint: '#b3302a', sh: 5, lw: 2 });
  A.burst = finish(P, { seed: 67 });
}
function buildPuff(seed) {
  const P = newPart(-100, -80, 100, 70, { seed, s: 4.4 }), r = rng(seed), p = new Path2D(), cs = [];
  for (let k = 0; k < 7; k++) { const a = k / 7 * TAU + r(); cs.push([Math.cos(a) * 44, Math.sin(a) * 26 - 6, 30 + r() * 18]); }
  cs.push([0, -4, 46]);
  for (const [a, b, rr] of cs) { p.moveTo(a + rr, b); p.arc(a, b, rr, 0, TAU); }
  for (const [a, b, rr] of cs) inkStroke(P, circ(a, b, rr), 5);
  engrave(P, g => { g.fillStyle = fillOf(g, lin(0, -70, 0, 60, [[0, .03], [1, .4]])); g.fill(p); }, { a: 25, wob: .6 });
  tintFill(P, p, '#efe6d6');
  return finish(P, { seed, rim: 3 });
}
function buildCrane() {
  const P = newPart(930, 40, 2110, 140, { seed: 71, s: 4.6 });
  region(P, rect(940, 60, 1160, 14), .6, { a: 90, tint: '#6a6560' }); region(P, rect(940, 112, 1160, 14), .6, { a: 90, tint: '#6a6560' });
  for (let k = 0; k < 29; k++) { const x0 = 950 + k * 40; inkStroke(P, `M ${x0} 74 L ${x0 + 40} 112 M ${x0 + 40} 74 L ${x0} 112`, 3); }
  for (let k = 0; k < 58; k++) { inkFill(P, circ(946 + k * 20, 67, 2.4)); inkFill(P, circ(946 + k * 20, 119, 2.4)); }
  region(P, rect(930, 50, 26, 86), .7, { a: 0, tint: '#5d5853' }); region(P, rect(2084, 50, 26, 86), .7, { a: 0, tint: '#5d5853' });
  A.crane = finish(P, { seed: 71, rim: 3 });
  const T = newPart(-60, -30, 60, 60, { seed: 73, s: 4 });
  for (const wx of [-32, 32]) { region(T, circ(wx, -14, 14), rad(wx, -14, 2, 14, [[0, .3], [1, .7]]), { ring: [wx, -14], tint: '#6a6560' }); inkFill(T, circ(wx, -14, 3)); }
  region(T, rect(-50, -8, 100, 26), lin(0, -8, 0, 18, [[0, .4], [1, .7]]), { a: 0, tint: '#7a5a3a' });
  for (const rx of [-40, 40]) inkFill(T, circ(rx, 5, 3));
  region(T, circ(0, 36, 18), rad(0, 36, 2, 18, [[0, .3], [1, .7]]), { ring: [0, 36], tint: '#b0904c' }); inkFill(T, circ(0, 36, 4));
  inkStroke(T, 'M -6 18 L -6 30 M 6 18 L 6 30', 3);
  A.trolley = finish(T, { seed: 73, rim: 3 });
  const K = newPart(-40, -50, 44, 80, { seed: 79, s: 3.6 });
  region(K, 'M -22 -44 L 22 -44 L 18 -4 L -18 -4 Z', lin(-22, 0, 22, 0, [[0, .75], [.4, .3], [1, .8]]), { a: 0, tint: '#5f5a55' });
  inkFill(K, circ(0, -30, 6), '#f0e4c9'); inkStroke(K, circ(0, -30, 6), 2);
  region(K, 'M -8 -4 L 8 -4 L 8 30 C 8 52 26 60 34 44 C 38 36 34 28 28 26 L 36 18 C 50 30 50 58 32 70 C 12 82 -8 70 -8 44 Z', lin(-8, 0, 48, 0, [[0, .8], [.4, .35], [1, .75]]), { a: 30, s: 3.4, tint: '#4f4b48' });
  A.hook = finish(K, { seed: 79, rim: 3 });
}
function buildMachine() {                                // world coordinates
  const P = newPart(1770, 180, 2870, 910, { seed: 83, s: 5.5 });
  // gear stand (behind the gears)
  region(P, 'M 2500 575 L 2560 575 L 2610 880 L 2450 880 Z', lin(2450, 0, 2610, 0, [[0, .7], [1, .45]]), { a: 90, tint: '#5e5a56' });
  region(P, 'M 2665 725 L 2715 725 L 2760 880 L 2620 880 Z', lin(2620, 0, 2760, 0, [[0, .7], [1, .45]]), { a: 90, tint: '#5e5a56' });
  region(P, rect(2360, 700, 140, 42), lin(0, 700, 0, 742, [[0, .3], [.5, .1], [1, .6]]), { a: 90, s: 4.4, tint: '#86817a' });
  inkStroke(P, 'M 2366 712 L 2494 712 M 2366 730 L 2494 730', 1.4);
  // chimney
  region(P, rect(2272, 212, 58, 250), lin(2272, 0, 2330, 0, [[0, .75], [.4, .35], [1, .8]]), { a: 0, s: 4.6, tint: '#4d4a48' });
  region(P, 'M 2256 190 L 2346 190 L 2338 216 L 2264 216 Z', .7, { a: 0, s: 4, tint: '#3f3c3a' });
  for (let k = 0; k < 4; k++) inkStroke(P, `M 2272 ${270 + k * 50} L 2330 ${270 + k * 50}`, 2);
  // boiler
  const boil = 'M 1880 850 L 1880 520 C 1880 470 1960 440 2120 440 C 2280 440 2360 470 2360 520 L 2360 850 Z';
  region(P, boil, lin(1880, 0, 2360, 0, [[0, .66], [.35, .12], [.55, .22], [1, .72]]), { a: 0, s: 5, wob: .12, tint: '#6f9c87' });
  for (const by of [560, 700]) { inkStroke(P, `M 1880 ${by} L 2360 ${by}`, 3); for (let k = 0; k < 20; k++) { inkFill(P, circ(1894 + k * 24, by - 9, 3)); inkFill(P, circ(1894 + k * 24, by + 9, 3)); } }
  // hopper (the pancake drops in here)
  region(P, 'M 1832 362 L 2058 362 L 1990 476 L 1940 476 Z', lin(1832, 0, 2058, 0, [[0, .7], [.4, .25], [1, .75]]), { a: 0, s: 4.6, tint: '#b36f3e' });
  region(P, ell(1945, 362, 114, 14), rad(1945, 362, 10, 114, [[0, .95], [1, .75]]), { ring: [1945, 362], s: 4, tint: '#5a3726', lw: 3 });
  for (let k = 0; k < 6; k++) inkFill(P, circ(1850 + k * 38, 380 + Math.abs(k - 2.5) * 3, 3));
  // pressure gauge
  region(P, circ(2000, 626, 66), rad(2000, 626, 50, 66, [[0, .4], [1, .8]]), { ring: [2000, 626], s: 4, tint: '#c7a458' });
  region(P, circ(2000, 626, 54), rad(2000, 626, 4, 54, [[0, .02], [1, .14]], 1980, 606), { ring: [1984, 610], s: 4.4, tint: '#f6efdd' });
  const g = P.tg; g.save(); loc(g, P); g.strokeStyle = '#c23a2e'; g.lineWidth = 12; g.beginPath(); g.arc(2000, 626, 42, deg(-20), deg(40)); g.stroke(); g.restore();
  for (let k = 0; k <= 10; k++) { const a = deg(-220 + k * 26); inkStroke(P, `M ${2000 + Math.cos(a) * 38} ${626 + Math.sin(a) * 38} L ${2000 + Math.cos(a) * 48} ${626 + Math.sin(a) * 48}`, k % 5 ? 1.6 : 3); }
  inkText(P, 'PRESSURE', 2000, 668, `13px ${SC}`, { ls: 1 });
  // plaque
  region(P, 'M 2040 742 L 2336 742 L 2346 752 L 2346 812 L 2336 822 L 2040 822 L 2030 812 L 2030 752 Z', lin(0, 742, 0, 822, [[0, .12], [1, .4]]), { a: 90, s: 4, tint: '#cfa857' });
  inkStroke(P, rect(2042, 752, 292, 60), 1.4);
  inkText(P, 'RESOLUTION ENGINE', 2188, 782, `24px ${SC}`, { ls: .5 });
  inkText(P, 'Patent pending since 1851', 2188, 804, `italic 18px ${SERIF}`);
  // cannon mount on the dome
  region(P, 'M 2130 452 L 2232 452 L 2214 404 L 2148 404 Z', lin(2130, 0, 2232, 0, [[0, .7], [1, .45]]), { a: 90, s: 4, tint: '#6b4a2e' });
  region(P, circ(2180, 440, 40), rad(2180, 440, 30, 40, [[0, .5], [1, .8]]), { ring: [2180, 440], s: 4, tint: '#6b4a2e' });
  for (let k = 0; k < 8; k++) { const a = k / 8 * TAU; inkStroke(P, `M 2180 440 L ${2180 + Math.cos(a) * 32} ${440 + Math.sin(a) * 32}`, 3.4); }
  inkFill(P, circ(2180, 440, 8));
  // plinth
  region(P, rect(1850, 846, 930, 50), lin(0, 846, 0, 896, [[0, .3], [1, .66]]), { a: 90, s: 4.6, wob: .4, tint: '#8c8274' });
  for (let k = 0; k < 7; k++) inkStroke(P, `M ${1980 + k * 130} 846 L ${1972 + k * 130} 896`, 1.6);
  A.machine = finish(P, { seed: 83 });
}
function buildCannon() {
  const P = newPart(-54, -44, 296, 44, { seed: 89, s: 4.4 });
  region(P, 'M 0 -34 L 250 -22 C 262 -22 268 -32 282 -32 L 282 32 C 268 32 262 22 250 22 L 0 34 C -30 34 -46 18 -46 0 C -46 -18 -30 -34 0 -34 Z',
    lin(0, -34, 0, 34, [[0, .8], [.3, .22], [.55, .4], [1, .85]]), { a: 90, s: 4.2, tint: '#9b7442' });
  for (const bx of [36, 150, 246]) inkStroke(P, `M ${bx} ${-34 + bx * .048} L ${bx} ${34 - bx * .048}`, 4);
  inkFill(P, ell(282, 0, 5, 30), '#1c130d');
  A.cannon = finish(P, { seed: 89, rim: 3 });
}
function buildBanner() {
  const P = newPart(-800, -124, 800, 140, { seed: 97, s: 5 });
  const tail = s => `M ${s * 640} -54 L ${s * 790} -30 L ${s * 744} 36 L ${s * 792} 110 L ${s * 640} 96 Z`;
  for (const s of [-1, 1]) {
    region(P, tail(s), lin(s * 640, 0, s * 790, 0, [[0, .75], [1, .4]]), { a: 90, s: 4.4, tint: '#a33229' });
    region(P, `M ${s * 640} 70 L ${s * 640} 96 L ${s * 612} 104 Z`, .9, { a: 0, s: 3, tint: '#6d1f1a' });
  }
  const body = 'M -650 -104 C -320 -118 320 -118 650 -104 L 650 104 C 320 90 -320 90 -650 104 Z';
  region(P, body, lin(-650, 0, 650, 0, [[0, .34], [.07, .1], [.93, .1], [1, .34]]), { a: 90, s: 5, wob: .1, xk: .5, tint: '#f3e3c0' });
  tintFill(P, pth('M -650 -104 C -320 -118 320 -118 650 -104 L 650 -84 C 320 -98 -320 -98 -650 -84 Z M -650 104 C -320 90 320 90 650 104 L 650 84 C 320 70 -320 70 -650 84 Z'), '#a33229');
  inkStroke(P, 'M -650 -84 C -320 -98 320 -98 650 -84 M -650 84 C -320 70 320 70 650 84', 1.8);
  inkText(P, 'RESOLVED:', 0, -30, `50px ${SC}`, { ls: 8 });
  P.g.font = `92px ${SC}`; const w = P.g.measureText('TO FORM A SUB-COMMITTEE').width, fs = Math.min(92, 92 * 1170 / w);
  engText(P, 'TO FORM A SUB-COMMITTEE', 0, 58, `${fs.toFixed(1)}px ${SC}`, { fs, d0: .8, d1: .98, sh: 4, lw: 1.4, s: 4, tint: '#7b1f19' });
  A.banner = finish(P, { seed: 97 });
  const R = newPart(-28, -118, 28, 118, { seed: 101, s: 3.6 });
  region(R, 'M -24 -110 L 24 -110 L 24 110 L -24 110 Z', lin(-24, 0, 24, 0, [[0, .75], [.35, .2], [1, .8]]), { a: 90, tint: '#f0e0bd' });
  inkStroke(R, ell(0, -110, 24, 6), 2); inkStroke(R, 'M -24 -94 L 24 -94 M -24 94 L 24 94', 1.4, null, '#a33229');
  A.roll = finish(R, { seed: 101, rim: 3 });
}
function buildTitle(big, lines) {                        // hanging card; origin = centre
  const P = newPart(-760, -420, 760, 420, { seed: 107, s: 5.5 });
  const card = 'M -730 -380 L 730 -380 L 730 380 L -730 380 Z';
  region(P, card, rad(0, 0, 100, 900, [[0, .06], [1, .22]]), { a: 90, s: 5, wob: .1, xk: 0, tint: '#f1e2c2', lw: 3.4 });
  inkStroke(P, rect(-700, -350, 1400, 700), 5.5); inkStroke(P, rect(-686, -336, 1372, 672), 1.5);
  for (const [cx, cy] of [[-686, -336], [686, -336], [-686, 336], [686, 336]]) {
    const ro = circ(cx, cy, 30); region(P, ro, rad(cx, cy, 2, 30, [[0, .15], [1, .6]]), { ray: [cx, cy, 16], xk: 0, tint: '#b0402f', lw: 3 });
    for (let k = 0; k < 8; k++) { const a = k / 8 * TAU; inkStroke(P, `M ${cx} ${cy} L ${cx + Math.cos(a) * 30} ${cy + Math.sin(a) * 30}`, 1.6); }
    inkFill(P, circ(cx, cy, 7), '#f1e2c2'); inkStroke(P, circ(cx, cy, 7), 2);
  }
  const orn = y => { inkStroke(P, `M -300 ${y} L -24 ${y} M 24 ${y} L 300 ${y}`, 2); inkFill(P, poly([[0, y - 12], [14, y], [0, y + 12], [-14, y]])); inkStroke(P, `M -300 ${y + 6} L -60 ${y + 6} M 60 ${y + 6} L 300 ${y + 6}`, 1); };
  lines(P, orn);
  return finish(P, { seed: 107, rim: 5 });
}
function buildPlaque(txt, seed) {
  const P = newPart(-600, -58, 600, 58, { seed, s: 4.6 });
  const d = 'M -560 -48 L 560 -48 L 590 -18 L 590 18 L 560 48 L -560 48 L -590 18 L -590 -18 Z';
  region(P, d, lin(0, -48, 0, 48, [[0, .08], [1, .28]]), { a: 90, s: 4.6, xk: 0, tint: '#ead7ae', lw: 3 });
  inkStroke(P, 'M -552 -38 L 552 -38 L 578 -12 L 578 12 L 552 38 L -552 38 L -578 12 L -578 -12 Z', 1.4);
  inkText(P, txt, 0, 16, `italic 46px ${SERIF}`);
  return finish(P, { seed, rim: 4 });
}
function composeF(w, h, ox, oy, draw) {                   // assemble already-finished cut-outs into one piece
  const c = mk(w, h), g = c.getContext('2d'); draw(g);
  const sh = mk(w, h), sg = sh.getContext('2d'); sg.filter = 'blur(7px)'; sg.drawImage(recolor(c, '#000'), 0, 0);
  return { img: c, sh, ox, oy };
}
function buildPancake() {
  A.pancake = composeF(420, 90, 210, 45, g => {
    const wd = (sx, rot) => { g.save(); g.translate(210 + sx * 70, 48); g.scale(sx * 1.05, .42); g.rotate(rot); g.drawImage(A.wing.img, -A.wing.ox, -A.wing.oy); g.restore(); };
    wd(-1, .5); wd(1, .5);
    g.save(); g.translate(210, 50); g.rotate(Math.PI / 2); g.scale(.22, 1.6); g.drawImage(A.bulb.img, -A.bulb.ox, -A.bulb.oy); g.restore();
  });
}
