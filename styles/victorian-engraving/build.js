// ── builders: every asset is engraved once at load time ──────────────────────────────────────────
const A = {};

function buildSky() {                                   // parallax sky (moves at 0.6× camera)
  const P = newPart(0, 0, SKW, 860, { seed: 3, s: 6.5 });
  region(P, rect(0, 0, SKW, 860), lin(0, 0, 0, 840, [[0, .62], [.5, .3], [1, .08]]), { a: 90, wob: .28, xk: 0, lw: 0,
    tint: g => { const gr = g.createLinearGradient(0, 0, 0, 840); gr.addColorStop(0, '#7f98a2'); gr.addColorStop(.55, '#cfc3a4'); gr.addColorStop(1, '#eab27c'); return gr; } });
  const r = rng(77), clouds = [[260, 200, 1.1], [860, 110, .8], [1380, 250, 1.25], [1960, 140, .9], [2380, 300, 1], [620, 470, .7], [1700, 480, .6]];
  for (const [cx, cy, sc] of clouds) {
    const p = new Path2D(), lumps = [];
    for (let k = 0; k < 9; k++) { const u = k / 8 - .5; lumps.push([cx + u * 360 * sc, cy - (1 - 4 * u * u) * 55 * sc - r() * 30 * sc, (48 + r() * 42) * sc * (1.1 - Math.abs(u))]); }
    lumps.push([cx, cy + 10 * sc, 90 * sc]);
    for (const [a, b, rr] of lumps) { p.moveTo(a + rr, b); p.arc(a, b, rr, 0, TAU); }
    const flat = rect(cx - 260 * sc, cy - 400, 520 * sc, 400 + 38 * sc);
    for (const [a, b, rr] of lumps) inkStroke(P, circ(a, b, rr), 5, flat);
    engrave(P, g => { g.save(); g.clip(flat); g.fillStyle = fillOf(g, lin(0, cy - 140 * sc, 0, cy + 40 * sc, [[0, .02], [.6, .1], [1, .38]])); g.fill(p); g.restore(); }, { a: 15, s: 5.5, wob: .5, xk: .6, seed: cx });
    tintFill(P, p, '#f6ead3', flat);
    inkStroke(P, `M ${cx - 250 * sc} ${cy + 38 * sc} L ${cx + 250 * sc} ${cy + 38 * sc}`, 2.4);
  }
  for (let k = 0; k < 7; k++) { const bx = 300 + r() * 1900, by = 330 + r() * 180, s = 7 + r() * 6;   // distant birds
    inkStroke(P, `M ${bx - s} ${by - s * .4} Q ${bx - s * .4} ${by - s * .7} ${bx} ${by} Q ${bx + s * .4} ${by - s * .7} ${bx + s} ${by - s * .4}`, 1.8); }
  A.sky = finish(P, { bare: true, ta: .85 });
}

function buildGround() {                                 // skyline + marble floor, world coords
  const P = newPart(0, 560, WW, H, { seed: 5, s: 5.5 });
  const r = rng(19), sk = new Path2D(); let bx = -20; sk.moveTo(-20, 812);
  while (bx < WW + 40) {
    const w = 60 + r() * 120, h = 50 + r() * 120, top = 812 - h, kind = r();
    sk.lineTo(bx, top);
    if (kind < .25) { sk.lineTo(bx + w / 2, top - 45); sk.lineTo(bx + w, top); }
    else if (kind < .38) { sk.lineTo(bx + w * .2, top); sk.arc(bx + w / 2, top, w * .3, Math.PI, 0); sk.lineTo(bx + w * .5, top - w * .3 - 30); sk.lineTo(bx + w * .5 + 1, top - w * .3); sk.lineTo(bx + w, top); }
    else if (kind < .55) { sk.lineTo(bx + w * .6, top); sk.lineTo(bx + w * .6, top - 110 - r() * 60); sk.lineTo(bx + w * .6 + 22, top - 110 - r() * 60); sk.lineTo(bx + w * .6 + 22, top); sk.lineTo(bx + w, top); }
    else { sk.lineTo(bx + w * .3, top); sk.lineTo(bx + w * .3, top - 26); sk.lineTo(bx + w * .3 + 16, top - 26); sk.lineTo(bx + w * .3 + 16, top); sk.lineTo(bx + w, top); }
    sk.lineTo(bx + w, 812 - (50 + r() * 60)); bx += w;
  }
  sk.lineTo(WW + 40, 812); sk.closePath();
  region(P, sk, lin(0, 600, 0, 812, [[0, .28], [1, .48]]), { a: 90, s: 4.6, wob: .1, lw: 2, tint: '#a39c93' });
  // checkered marble floor in one-point perspective
  const VX = 1460, VY = 520, rows = [], R = 9;
  for (let j = 0; j <= R; j++) rows.push(810 + 270 * Math.pow(j / R, 1.55));
  const X = (xb, y) => VX + (xb - VX) * (y - VY) / (H - VY);
  const tiles = [];
  for (let j = 0; j < R; j++) for (let i = -14; i < 14; i++) {
    const xa = VX + i * 230, xb2 = xa + 230, y0 = rows[j], y1 = rows[j + 1];
    tiles.push([poly([[X(xa, y0), y0], [X(xb2, y0), y0], [X(xb2, y1), y1], [X(xa, y1), y1]]), (i + j) & 1]);
  }
  engrave(P, g => { for (const [q, d] of tiles) { g.fillStyle = gray(d ? .56 : .1); g.fill(q); } g.fillStyle = 'rgba(0,0,0,0)'; }, { a: 90, s: 5, wob: .06, xk: .5 });
  for (const [q, d] of tiles) tintFill(P, q, d ? '#79685a' : '#efe4cf');
  for (const [q] of tiles) inkStroke(P, q, 1.4);
  inkStroke(P, `M 0 811 L ${WW} 811`, 3);
  A.ground = finish(P, { bare: true, ta: .85 });
}

// ── the Chairman (head facing right; local origin = centre of head) ──
const HEAD = new Path2D('M -70 250 L -70 225 C -80 170 -120 120 -135 60 C -155 -20 -140 -120 -80 -160 C -30 -190 60 -185 100 -140 C 125 -110 132 -80 134 -52 C 136 -40 142 -32 138 -24 C 134 -16 136 -10 142 0 L 188 52 C 194 60 188 70 176 70 C 166 70 158 66 150 68 C 144 72 142 78 146 86 C 150 92 150 100 144 104 C 150 110 148 118 140 120 C 134 124 134 130 140 138 C 146 150 140 168 118 172 C 96 178 80 182 66 190 C 54 198 50 212 52 250 Z');
const CUT = (() => { const r = rng(4), pts = []; for (let i = 0; i <= 19; i++) pts.push([-175 + i * 20, -78 + (i & 1 ? 9 : -9) + (r() - .5) * 6]); return pts; })();
const BELOW = poly([...CUT, [300, 700], [-400, 700]]);
const ABOVE = poly([...CUT, [300, -500], [-400, -500]]);
const PIVOT = [-150, -80];

function buildChair() {
  const P = newPart(-330, -110, 290, 660, { seed: 9, s: 6.2 });
  // coat
  region(P, 'M -60 250 C -120 262 -200 285 -250 330 C -290 372 -300 440 -305 660 L 250 660 C 250 560 245 470 225 410 C 205 350 160 300 110 285 C 90 300 60 300 40 290 L -60 280 Z',
    lin(-300, 0, 250, 0, [[0, .86], [.6, .62], [1, .7]]), { a: 78, wob: .3, tint: '#3d4250' });
  region(P, 'M 62 318 C 100 334 140 356 160 384 C 190 430 200 520 205 660 L 105 660 C 100 560 88 450 58 372 Z', lin(60, 0, 205, 0, [[0, .55], [1, .3]]), { a: 100, s: 5, tint: '#c1923c' });
  for (let k = 0; k < 5; k++) { const by = 405 + k * 52, bx = 108 + k * 9; inkFill(P, circ(bx, by, 7)); inkFill(P, circ(bx - 2, by - 2, 2.5), '#e8d9b8'); }
  inkStroke(P, 'M 120 470 C 150 500 180 505 205 492', 3);                                         // watch chain
  for (let k = 0; k < 9; k++) inkFill(P, circ(122 + k * 10, 473 + Math.sin(k / 8 * Math.PI) * 28, 3.4));
  region(P, 'M 110 285 C 150 312 176 352 186 402 L 160 424 C 146 376 116 330 72 304 Z', .62, { a: 60, s: 5, tint: '#2f3340' });  // lapel
  region(P, 'M -40 282 C -90 300 -120 330 -140 380 L -110 400 C -95 350 -70 318 -30 298 Z', .75, { a: 60, s: 5, tint: '#2f3340' });
  inkStroke(P, 'M -250 330 C -236 420 -228 520 -226 660', 2.6);
  inkStroke(P, 'M -150 420 C -120 460 -60 470 -20 455', 1.6); inkStroke(P, 'M -200 520 C -150 550 -80 555 -30 540', 1.6);
  // neck + collar + cravat
  region(P, 'M -70 200 L 52 200 L 52 262 L -70 262 Z', lin(-70, 0, 52, 0, [[0, .45], [1, .2]]), { a: 100, st: .9, lk: .5, tint: '#eab998', lw: 0 });
  region(P, 'M -62 228 L 58 222 C 70 238 76 256 72 272 L 106 286 C 92 296 70 298 54 292 L -44 286 C -58 268 -64 248 -62 228 Z', lin(0, 222, 0, 296, [[0, .05], [1, .22]]), { a: 0, s: 5, tint: '#f7f2e6' });
  region(P, 'M 42 262 C 74 262 104 280 108 302 C 112 332 96 360 72 374 C 62 352 46 332 30 312 C 30 292 34 274 42 262 Z', rad(70, 300, 5, 70, [[0, .3], [1, .7]]), { ring: [70, 300], s: 5, tint: '#7b3656' });
  inkFill(P, circ(78, 304, 8), '#f5ecdc'); inkStroke(P, circ(78, 304, 8), 2);
  // lower head (below the hinge cut)
  region(P, HEAD, rad(70, -10, 20, 250, [[0, .06], [.55, .22], [1, .6]], 110, -30), { a: 112, st: 1, lk: .45, xk: .5, clip: BELOW, tint: '#efc4a0' });
  tintFill(P, circ(78, 30, 48), 'rgba(222,120,100,.45)', BELOW);
  // whiskers (mutton chops) + moustache
  const hair = { a: 72, s: 4.2, wob: .9, xk: .4, lw: 2.2, tint: '#b3aca0' };
  region(P, 'M 18 -30 C 44 -14 58 12 70 42 C 84 72 100 88 120 96 C 106 122 84 150 58 160 C 28 168 6 150 -2 120 C -8 92 -4 66 6 44 C 14 24 10 -6 18 -30 Z', lin(0, -30, 0, 160, [[0, .3], [1, .5]]), hair);
  for (let k = 0; k < 9; k++) { const y0 = -10 + k * 17, x0 = 12 + k * 5; inkStroke(P, `M ${x0} ${y0} C ${x0 + 14} ${y0 + 8} ${x0 + 20} ${y0 + 22} ${x0 + 12} ${y0 + 30}`, 1.6); }
  region(P, 'M 142 70 C 156 76 166 86 172 96 C 184 98 196 90 202 76 C 206 92 198 110 178 112 C 160 116 140 114 120 106 C 108 100 100 92 96 82 C 112 84 130 80 142 70 Z', .62, { ...hair, a: 20 });
  // ear
  region(P, 'M -12 -24 C 20 -34 36 -2 28 30 C 22 56 6 64 -3 52 C -9 42 -3 32 -9 22 C -15 10 -20 -12 -12 -24 Z', rad(6, 12, 4, 50, [[0, .12], [1, .42]]), { a: 100, st: 1, lk: .4, xk: .5, tint: '#e7b08e' });
  inkStroke(P, 'M 2 -10 C 18 -8 22 16 12 32', 2); inkStroke(P, 'M 6 4 C 10 8 10 16 6 20', 1.6);
  // eye, brow, wrinkles, monocle
  region(P, 'M 70 -48 C 90 -64 120 -60 138 -44 C 124 -46 110 -44 96 -40 C 86 -38 76 -40 70 -48 Z', .75, { a: 20, s: 4, wob: .6, lw: 2, tint: '#9d978f', clip: BELOW });
  inkFill(P, 'M 100 -30 C 104 -33 110 -31 111 -25 C 106 -24 101 -25 100 -30 Z');
  inkStroke(P, 'M 76 -26 C 88 -35 104 -34 116 -23', 4.2); inkStroke(P, 'M 82 -35 C 94 -41 106 -39 114 -32', 1.8);
  inkStroke(P, 'M 86 -14 C 96 -10 106 -12 114 -18', 1.8); inkStroke(P, 'M 88 -4 C 98 0 108 -2 116 -8', 1.4);
  inkStroke(P, 'M 142 18 C 128 40 124 60 132 76', 2); inkStroke(P, 'M 150 68 C 156 62 164 62 170 66', 2);
  inkStroke(P, 'M 72 160 C 92 170 110 168 124 160', 1.8); inkStroke(P, 'M 124 118 C 132 116 138 118 142 121', 1.8);
  const mono = circ(101, -24, 27);
  tintFill(P, mono, 'rgba(210,225,220,.55)');
  inkStroke(P, mono, 5.5); inkStroke(P, 'M 84 -38 C 90 -44 100 -46 108 -44', 2, null, '#fff8e8');
  inkStroke(P, 'M 96 3 C 70 60 30 110 20 170 C 14 210 30 250 56 300', 1.6); inkStroke(P, 'M 96 3 C 70 60 30 110 20 170 C 14 210 30 250 56 300', 1.2, null, '#c9a55a');
  // the hinge (brass) at the back of the cut
  inkFill(P, circ(PIVOT[0] + 6, PIVOT[1] + 8, 9), '#b89245'); inkStroke(P, circ(PIVOT[0] + 6, PIVOT[1] + 8, 9), 2.2);
  inkStroke(P, poly(CUT.concat([...CUT].reverse())), 2.8, HEAD);
  A.chair = finish(P, { seed: 9 });
}

function buildLid() {
  const P = newPart(-205, -385, 225, -40, { seed: 12, s: 6.2 });
  region(P, HEAD, rad(70, -60, 20, 220, [[0, .06], [.6, .2], [1, .55]], 100, -100), { a: 112, st: 1, lk: .45, xk: .5, clip: ABOVE, tint: '#efc4a0' });
  inkStroke(P, 'M 56 -112 C 88 -120 110 -114 126 -102', 1.6); inkStroke(P, 'M 46 -96 C 82 -102 108 -96 128 -86', 1.6);
  inkStroke(P, poly(CUT.concat([...CUT].reverse())), 2.8, HEAD);
  // top hat
  const crown = 'M -124 -150 C -128 -240 -136 -320 -140 -362 C -40 -376 60 -376 150 -362 C 142 -320 134 -240 128 -150 Z';
  region(P, crown, lin(-140, 0, 150, 0, [[0, .92], [.36, .5], [.5, .78], [1, .95]]), { a: 0, s: 4.6, wob: .12, tint: '#2e2b31' });
  region(P, crown, lin(0, -198, 0, -152, [[0, .7], [1, .7]]), { a: 0, s: 4.6, clip: rect(-200, -198, 400, 46), tint: '#6d2a26', lw: 2 });
  inkStroke(P, 'M -140 -362 C -60 -350 60 -350 150 -362', 2.2);
  region(P, 'M -182 -150 C -130 -170 70 -172 176 -154 C 190 -151 192 -140 180 -136 C 70 -152 -110 -152 -176 -134 C -190 -134 -194 -146 -182 -150 Z', .8, { a: 0, s: 4.4, tint: '#2e2b31' });
  inkStroke(P, 'M -90 -330 C -94 -260 -98 -210 -98 -165', 3, null, 'rgba(250,240,220,.55)');
  const F = finish(P, { seed: 12 });
  F.ox += PIVOT[0]; F.oy += PIVOT[1];
  A.lid = F;
}

function buildCavity() {
  const P = newPart(-170, -125, 180, -40, { seed: 14 });
  region(P, ell(2, -80, 158, 30), rad(2, -90, 10, 150, [[0, 1], [1, .7]]), { ring: [2, -60], s: 4, tint: '#5b3a33', lw: 3 });
  inkStroke(P, 'M -140 -86 C -60 -104 80 -104 150 -86', 2.4, null, '#8a5b4e');
  A.cavity = finish(P, { bare: true });
}

function buildDesk() {
  const P = newPart(90, 700, 890, H + 10, { seed: 21, s: 5.5 });
  region(P, 'M 128 800 L 852 800 L 852 1090 L 128 1090 Z', lin(128, 0, 852, 0, [[0, .62], [.5, .45], [1, .7]]), { a: 90, wob: 1.1, s: 5, tint: '#8a5a34' });
  for (const px of [150, 610]) {
    region(P, rect(px, 830, 220, 220), lin(0, 830, 0, 1050, [[0, .7], [1, .5]]), { a: 90, wob: 1.3, s: 4.6, tint: '#7b4f2e', lw: 3 });
    inkStroke(P, rect(px + 14, 844, 192, 192), 1.6, null, '#e9d6b0');
  }
  region(P, rect(398, 850, 184, 60), lin(0, 850, 0, 910, [[0, .15], [1, .45]]), { a: 90, s: 4, tint: '#cfa857', lw: 2.4 });
  inkText(P, 'THE CHAIR', 490, 891, `30px ${SC}`, { ls: 2 });
  region(P, 'M 112 770 L 868 770 L 884 804 L 96 804 Z', lin(0, 770, 0, 804, [[0, .3], [1, .6]]), { a: 90, s: 4.5, tint: '#56713f' });
  // bell, inkwell + quill, papers
  region(P, 'M 770 772 C 770 742 830 742 830 772 Z', lin(770, 0, 830, 0, [[0, .6], [.4, .15], [1, .7]]), { a: 0, s: 4, tint: '#c9a24f' });
  region(P, rect(760, 770, 80, 6), .6, { a: 90, s: 4, lw: 1.8 }); inkFill(P, circ(800, 738, 7), '#c9a24f'); inkStroke(P, circ(800, 738, 7), 2);
  region(P, 'M 200 772 L 206 740 L 254 740 L 260 772 Z', lin(200, 0, 260, 0, [[0, .85], [1, .5]]), { a: 0, s: 4, tint: '#39424a' });
  region(P, 'M 236 742 C 260 700 300 660 346 640 C 330 668 300 700 250 742 Z', lin(236, 740, 346, 640, [[0, .1], [1, .35]]), { a: -40, s: 3.6, wob: .4, lw: 1.8, tint: '#efe8da' });
  inkStroke(P, 'M 240 746 C 270 706 310 670 346 640', 1.4);
  region(P, 'M 560 770 L 700 764 L 712 774 L 572 780 Z', .08, { a: 0, s: 4, lw: 1.8, tint: '#f1e7d2' });
  A.desk = finish(P, { seed: 21 });
}
