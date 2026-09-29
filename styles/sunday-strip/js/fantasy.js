// ── fantasy.js · the imagination tier: lush, more rendered watercolor of the late Cretaceous ──
// scene space is 1920 x 1080; the page panel shows its central band, the full-frame expansion reveals the rest.
let F_SKY, F_FAR, F_MID, F_NEAR, F_FORE;
const FM = 60;   // bake margin for parallax

function tree(x, y, s, seed, tint) {
  // a broccoli tree: tall pale trunk, forked, crowned by an enormous floret
  const lw = tint.lw ?? 3;
  const h = tint.h ?? (70 + hash(seed) * 50);
  if (h > 0) { const tr = [[x - 15 * s, y], [x + 15 * s, y], [x + 11 * s, y - h * s - 4], [x - 11 * s, y - h * s - 4]]; part(tr, tint.stalk, lw, { seed, gran: 0.4, base: tint.dark }); glaze(tr, lgrad(x - 15 * s, 0, x + 15 * s, 0, [[0, 'rgba(255,255,255,0)'], [1, tint.dark]]), 0.6); }
  broccoli(x, y - (h - 8) * s, s, seed, { col: tint.col, dark: tint.dark, light: tint.light, stalk: tint.stalk, base: tint.dark, detail: tint.detail ?? 18, lwk: tint.lwk ?? 1, budInk: tint.bud, bumps: 9 + Math.floor(hash(seed + 3) * 5) });
}
function fern(x, y, len, ang, col, seed, side = 1) {
  // a cycad / fern frond: curved rachis with tapering leaflets
  const R = rng(seed), p = [];
  for (let i = 0; i <= 12; i++) { const u = i / 12, a = ang + side * u * 0.7; p.push([x + Math.cos(a) * len * u, y + Math.sin(a) * len * u - Math.sin(u * Math.PI) * len * 0.12]); }
  for (let i = 1; i < 12; i++) {
    const [px, py] = p[i], u = i / 12, l = len * 0.22 * (1 - u * 0.7), a0 = Math.atan2(p[i + 1][1] - py, p[i + 1][0] - px);
    for (const sd of [-1, 1]) {
      const a = a0 + sd * (1.0 + R() * 0.2), tx = px + Math.cos(a) * l, ty = py + Math.sin(a) * l + l * 0.25;
      const lf = [[px, py], [lerp(px, tx, 0.5) + Math.cos(a + 1.57) * l * 0.12, lerp(py, ty, 0.5) + Math.sin(a + 1.57) * l * 0.12], [tx, ty], [lerp(px, tx, 0.5) - Math.cos(a + 1.57) * l * 0.1, lerp(py, ty, 0.5) - Math.sin(a + 1.57) * l * 0.1]];
      wash(lf, col, { gran: 0.3, edge: 0.6, off: [0, 0] });
      brush([[px, py], [tx, ty]], 1.8, { seed: seed + i + sd, a: 0.8 });
    }
  }
  brush(p, 3.2, { seed, ta: 0.05, tb: 0.5 });
}
function buildFantasy() {
  const BW = W + 2 * FM, BH = H + 2 * FM;
  F_SKY = bake(BW, BH, (w, h) => {
    ctx.fillStyle = lgrad(0, 0, 0, h, [[0, '#1f5f8f'], [0.3, '#4f9dba'], [0.5, '#bfe0d0'], [0.6, '#f4d596'], [0.72, '#f3a867'], [1, '#e0874f']]); ctx.fillRect(0, 0, w, h);
    ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = 0.25; ctx.drawImage(GRAN, 0, 0, 1024, 1024, 0, 0, w, h); ctx.restore();
    softBlob(900 + FM, 200 + FM, 260, '#fff4c8', 0.55); softBlob(900 + FM, 200 + FM, 110, '#fffbe6', 0.9);
    wash(circ(900 + FM, 200 + FM, 78, 78, 20, 0.03, 4), '#fff6d0', { gran: 0.2, edge: 0.4, off: [0, 0] });
    const R = rng(12);
    for (let i = 0; i < 14; i++) { const cx = R() * w, cy = 120 + R() * 360, rx = 120 + R() * 260; wash(circ(cx, cy, rx, 22 + R() * 30, 16, 0.3, i), i % 3 ? '#fbe7c6' : '#c9dde3', { gran: 0.4, edge: 0.35, a: 0.5, off: [0, 0] }); }
    paperGrain(w, h, 0.8);
  });
  F_FAR = bake(BW, BH, (w, h) => {
    ctx.translate(FM, FM);
    // distant ranges in cool, granulating blue-violet
    const ridge = (y0, amp, col, seed, a) => { const R = rng(seed), p = [[-FM, H + FM]]; for (let x = -FM; x <= W + FM; x += 60) p.push([x, y0 - amp * (0.5 + 0.5 * Math.sin(x * 0.004 + seed)) - R() * amp * 0.3]); p.push([W + FM, H + FM]); wash(p, col, { raw: true, gran: 0.7, edge: 0.6, a, off: [0, 0] }); };
    ridge(600, 90, '#9aa6c9', 3, 0.75);
    // volcano
    const vol = [[1040, 660], [1250, 440], [1330, 350], [1360, 342], [1400, 342], [1430, 352], [1520, 450], [1760, 660]];
    wash(vol, '#8a86b0', { gran: 0.8, edge: 0.7, off: [0, 0] });
    glaze(vol, lgrad(1200, 0, 1700, 0, [[0, 'rgba(255,255,255,0)'], [1, '#5e5a8a']]), 0.6);
    brush([[1250, 440], [1330, 350], [1360, 342]], 2.4, { seed: 4, a: 0.6 }); brush([[1400, 342], [1430, 352], [1520, 450]], 2.4, { seed: 5, a: 0.6 });
    for (let i = 0; i < 6; i++) brush([[1340 + i * 12, 360], [1300 + i * 30 - 60, 520 + i * 20]], 1.6, { seed: 30 + i, a: 0.35 });
    softBlob(1380, 346, 50, '#f5874a', 0.55);
    ridge(660, 70, '#8fb3a6', 7, 0.8);
  });
  F_MID = bake(BW, BH, (w, h) => {
    ctx.translate(FM, FM);
    const hazy = { col: '#6fa488', dark: '#4a7f78', light: '#c4e0b0', stalk: '#6f9a80', detail: 5, lw: 1.6, lwk: 0.5, bud: '#3f6660', h: 0 };
    const hazy2 = { col: '#5e9a62', dark: '#3a6f55', light: '#b8dc92', stalk: '#7fa56e', detail: 8, lw: 2, lwk: 0.6, bud: '#2f5a44', h: 10 };
    const R = rng(21);
    for (let i = 0; i < 30; i++) tree(-60 + i * 70 + R() * 40, 640 + R() * 14, 1.1 + R() * 0.4, 100 + i, hazy);
    for (let i = 0; i < 20; i++) tree(-40 + i * 104 + R() * 50, 700 + R() * 16, 1.5 + R() * 0.5, 140 + i, hazy2);
    // mid ground meadow
    const g = [[-FM, 700], [300, 690], [700, 712], [1100, 700], [1500, 716], [W + FM, 700], [W + FM, H + FM], [-FM, H + FM]];
    wash(g, '#a9c46e', { gran: 0.7, edge: 0.5, off: [0, 0] });
    glaze(g, lgrad(0, 700, 0, 900, [[0, 'rgba(255,255,255,0)'], [1, '#6e9a4a']]), 0.6);
    const lush = { col: '#4f9a34', dark: '#1f5c24', light: '#b3e070', stalk: '#8fb35e', detail: 16, lw: 2.8, lwk: 0.8, bud: INK, h: 26 };
    const pos = [[1080, 800, 1.9], [1290, 780, 1.6], [1480, 812, 2.2], [1680, 790, 1.8], [100, 790, 1.9], [290, 772, 1.5], [-40, 800, 2.2]];
    pos.forEach(([x, y, s], i) => tree(x, y, s, 200 + i, lush));
  });
  F_NEAR = bake(BW, BH, (w, h) => {
    ctx.translate(FM, FM);
    // the ridge the Tyrannosaurus stands on
    const rg = [[-FM, 860], [200, 846], [520, 836], [860, 842], [1180, 870], [1500, 910], [W + FM, 940], [W + FM, H + FM], [-FM, H + FM]];
    wash(rg, '#b3b861', { gran: 0.8, edge: 0.6, off: [0, 0] });
    glaze(rg, lgrad(0, 840, 0, 1080, [[0, 'rgba(255,255,255,0)'], [1, '#6d6a2e']]), 0.75);
    softBlob(700, 950, 380, '#d9c77a', 0.35);
    brush(rg.slice(0, 7), 3.4, { seed: 8, ta: 0.02, tb: 0.1 });
    const R = rng(33);
    for (let i = 0; i < 60; i++) { const x = R() * W, y = 870 + R() * 200; brush([[x, y], [x + 20 + R() * 30, y + 2]], 1.6, { seed: i, a: 0.5 }); }
    for (let i = 0; i < 40; i++) { const x = R() * W, y = 880 + R() * 180, c = ['#e0533c', '#f2c14a', '#f7f0e0', '#c46ab0'][i % 4]; for (let k = 0; k < 4; k++) wash(circ(x + (k % 2) * 9, y + (k >> 1) * 8, 6, 5, 8, 0.2, i * 4 + k), c, { gran: 0.2, edge: 0.4, off: [0, 0] }); ctx.fillStyle = '#6d4a1e'; ctx.beginPath(); ctx.arc(x + 4, y + 4, 2.5, 0, TAU); ctx.fill(); }
    for (let i = 0; i < 18; i++) fern(R() * W, 900 + R() * 160, 70 + R() * 60, -1.2 - R() * 0.8, '#5d8a36', 400 + i, R() < 0.5 ? 1 : -1);
    for (let i = 0; i < 26; i++) { const x = R() * W, y = 850 + R() * 40; brush([[x, y + 10], [x + (R() - 0.5) * 16, y - 18 - R() * 16]], 2, { seed: i + 99, col: '#4d6b2a' }); }
  });
  F_FORE = bake(BW, BH, (w, h) => {
    ctx.translate(FM, FM);
    fern(-30, 1100, 420, -1.2, '#3f7a3a', 5, 1); fern(40, 1110, 360, -0.75, '#4f8c3e', 6, 1); fern(-60, 960, 300, -0.35, '#2f6532', 7, 1);
    fern(1960, 1100, 440, -1.95, '#3f7a3a', 8, -1); fern(1900, 1120, 380, -2.4, '#4f8c3e', 9, -1); fern(1990, 980, 300, -2.8, '#2f6532', 10, -1);
    tree(1790, 1150, 3.2, 301, { col: '#4d9234', dark: '#1f5a24', light: '#a7d46c', stalk: '#9fbf6a', detail: 22, lw: 3.4, lwk: 1, bud: INK, h: 120 });
  });
}

// ── the Tyrannosaurus (it is Juniper: note the red bow and her teal stripes). origin = hip, facing right
const REX = '#6f9447', REX_D = '#3f6431', REX_BELLY = '#e2cf8a';
function rex(x, y, s, st) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const lw = 4.4;
  const breath = Math.sin(st.t * 3.2) * 0.012;
  // far leg (darker, a step ahead)
  ctx.save(); ctx.translate(70, -12);
  const LEG = [[-60, -196], [72, -204], [112, -122], [74, -20], [26, 108], [50, 166], [112, 178], [128, 198], [8, 204], [-20, 150], [-44, 96], [-34, 10], [-92, -102]];
  part(LEG, '#4f7439', lw, { seed: 1 });
  ctx.restore();
  // tail sway: bend the tail points
  const sw = Math.sin(st.t * 1.6) * 14;
  const body = [[-600, -40 + sw], [-430, -112 + sw * 0.6], [-260, -188 + sw * 0.25], [-120, -236], [20, -256], [150, -252], [240, -234], [300, -214], [330, -168], [306, -118], [236, -70], [124, -40], [20, -38], [-60, -66], [-200, -92 + sw * 0.25], [-380, -76 + sw * 0.6], [-560, -32 + sw]];
  ctx.save(); ctx.scale(1, 1 + breath);
  part(body, REX, lw, { seed: 5, gran: 0.8 });
  glaze(body, lgrad(0, -260, 0, -30, [[0, 'rgba(255,255,255,0)'], [0.55, 'rgba(255,255,255,0)'], [1, REX_D]]), 0.55);
  // belly
  wash([[330, -168], [306, -118], [236, -70], [124, -40], [20, -38], [60, -70], [180, -96], [270, -140]], REX_BELLY, { gran: 0.4, a: 0.8 });
  // Juniper's stripes, down the back
  ctx.save(); tracePts(cr(body, true, 6), true); ctx.clip();
  for (let k = 0; k < 9; k++) { const bx = -470 + k * 88, top = k < 5 ? -150 + (4 - k) * -20 : -250; const tp = [[bx, top - 60], [bx + 30, top - 60], [bx + 20 + 8, top + 50], [bx + 4, top + 56]];
    wash(tp.map(([a, b]) => [a, b + (k < 3 ? 40 + (2 - k) * 34 : 0)]), '#3f8a93', { gran: 0.5, edge: 0.4, a: 0.75, off: [0, 0] }); }
  ctx.restore();
  // scales and ink texture
  const R = rng(55);
  for (let i = 0; i < 70; i++) { const px = -420 + R() * 700, py = -220 + R() * 160; if (py > -60 - (px + 400) * 0.02) continue; brush([[px, py], [px + 6, py - 4], [px + 12, py]], 1.6, { seed: i, a: 0.55 }); }
  brush([[-300, -130], [-120, -150], [60, -140]], 1.8, { seed: 9, a: 0.4 });
  ctx.restore();
  // near leg: one organic outline, drumstick thigh to toes
  part(LEG, REX, lw, { seed: 6, gran: 0.8 });
  glaze(LEG, lgrad(-90, -200, 120, 100, [[0, 'rgba(255,255,255,0)'], [1, REX_D]]), 0.55);
  brush([[-40, -160], [20, -120], [60, -60]], 1.8, { seed: 11, a: 0.5 }); brush([[-20, -180], [40, -150]], 1.6, { seed: 12, a: 0.4 });
  brush([[-30, 40], [-10, 80]], 1.8, { seed: 31, a: 0.5 }); brush([[30, 170], [40, 190]], 1.6, { seed: 32, a: 0.5 });
  for (const cx of [120, 94, 68]) part([[cx, 190], [cx + 22, 199], [cx, 206]], '#f1ead4', 2.4, { seed: cx });
  // tiny arm (two claws)
  part(capsule([272, -142], [302, -98], 22, 16), REX, 3.4, { seed: 10 }); part(capsule([302, -98], [336, -112], 15, 12), REX, 3.2, { seed: 11 });
  for (const d of [-5, 5]) brush([[336, -112 + d], [350, -104 + d]], 2.6, { seed: d });
  // head + neck, rotating at the neck; lower jaw hinged
  ctx.save(); ctx.translate(270, -210); ctx.rotate(st.head); ctx.translate(-270, 210);
  const jawA = st.jaw;
  const up = [[150, -252], [240, -264], [330, -326], [400, -356], [480, -354], [560, -338], [612, -318], [620, -292], [594, -282], [470, -276], [440, -270], [420, -248], [364, -206], [306, -150], [230, -150]];
  // mouth interior + teeth (visible when open)
  const piv = [436, -272], rot = (p) => { const c = Math.cos(jawA), sn = Math.sin(jawA); const dx = p[0] - piv[0], dy = p[1] - piv[1]; return [piv[0] + dx * c - dy * sn, piv[1] + dx * sn + dy * c]; };
  const jaw = [[436, -278], [592, -282], [588, -262], [522, -244], [452, -238], [418, -252]].map(rot);
  if (jawA > 0.02) {
    wash([[440, -276], [600, -284], rot([592, -282]), rot([450, -262])], '#8c2f2a', { gran: 0.3, off: [0, 0] });
    for (let k = 0; k < 7; k++) { const tx = 474 + k * 18; part([[tx, -280], [tx + 10, -280], [tx + 5, -262]], '#fbf5e4', 1.6, { seed: k }); const b = rot([tx + 4, -281]); part([b, [b[0] + 10, b[1]], [b[0] + 5, b[1] - 16]], '#fbf5e4', 1.6, { seed: k + 9 }); }
    wash([rot([470, -266]), rot([560, -270]), rot([540, -256]), rot([480, -254])], '#d06a66', { gran: 0.2, off: [0, 0], a: 0.8 });
  }
  part(jaw, REX, lw, { seed: 12 });
  wash(jaw.slice(2), REX_BELLY, { gran: 0.3, a: 0.6 });
  wash(up, REX, { base: '#fbf7ec', gran: 0.8 });
  brush(cr(up, true, 7).slice(0, 13 * 7 + 1), lw, { raw: true, ta: 0.12, tb: 0.1, seed: 13 });
  glaze(up, lgrad(0, -360, 0, -150, [[0, 'rgba(255,255,255,0)'], [0.6, 'rgba(255,255,255,0)'], [1, REX_D]]), 0.5);
  wash([[306, -150], [364, -206], [420, -248], [440, -270], [400, -230], [340, -170]], REX_BELLY, { gran: 0.4, a: 0.7 });
  // eye with a fierce brow, nostril, cheek wrinkles
  part(circ(474, -322, 12, 10, 10, 0, 3), '#f3c540', 2.6, { seed: 14 });
  ctx.fillStyle = INK; ctx.beginPath(); ctx.ellipse(476, -322, 3, 8, 0, 0, TAU); ctx.fill();
  brush([[446, -336], [478, -344], [506, -334]], 6, { seed: 15, ta: .1, tb: .2 });
  brush([[590, -320], [600, -318]], 4, { seed: 16 });
  for (let k = 0; k < 3; k++) brush([[390 + k * 16, -300], [398 + k * 16, -284]], 1.8, { seed: 17 + k, a: 0.6 });
  for (let k = 0; k < 4; k++) brush([[250 + k * 26, -260 + k * 10], [262 + k * 26, -230 + k * 12]], 1.6, { seed: 20 + k, a: 0.5 });
  // Juniper's red bow, knotted between the crests
  part([[400, -352], [372, -388], [362, -352]], BOW, 3, { seed: 21 }); part([[400, -352], [428, -392], [440, -356]], BOW, 3, { seed: 22 });
  part(circ(400, -354, 9, 8, 8, 0, 2), BOW, 2.8, { seed: 23 });
  ctx.restore();
  ctx.restore();
}

// Mortimer, alive: a great horned owl gliding over the forest (front-below view, wings spread)
function owlFly(x, y, s, flap, bank) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(bank); ctx.scale(s, s);
  const f = flap;
  for (const sd of [-1, 1]) {
    const wing = [[-26, -34], [-110, -80 - f * 46], [-210, -74 - f * 80], [-272, -44 - f * 96], [-252, -18 - f * 82], [-226, 0 - f * 70], [-196, 12 - f * 54], [-160, 22 - f * 38], [-118, 30 - f * 22], [-70, 34 - f * 8], [-24, 24]].map(([a, b]) => [a * sd, b]);
    for (let k = 0; k < 4; k++) { const P = [lerp(wing[2][0], wing[5][0], k / 3), lerp(wing[2][1], wing[5][1], k / 3)]; part(capsule(P, [P[0] - sd * (46 - k * 6), P[1] + 6 + k * 12 - f * 14]), '#8a5a2e', 2.4, { seed: 50 + k * sd }); }
    part(wing, '#a9763f', 3.4, { seed: 30 + sd, gran: 0.8 });
    wash(wing.slice(0, 3).concat([[wing[8][0], wing[8][1] - 10], [wing[10][0], wing[10][1] - 12]]), '#e2c08a', { gran: 0.5, a: 0.6, off: [0, 4] });
    glaze(wing, lgrad(0, -80, 0, 40, [[0, 'rgba(255,255,255,0)'], [1, '#6b4424']]), 0.5);
    for (let k = 1; k < 5; k++) { const a = wing[k + 4], b = [lerp(a[0], -20 * sd, 0.35), lerp(a[1], -34, 0.35)]; brush([a, b], 1.8, { seed: k * sd, a: 0.7 }); }
    for (let k = 0; k < 4; k++) brush([[sd * (70 + k * 44), -40 - f * (10 + k * 18)], [sd * (90 + k * 44), -30 - f * (12 + k * 18)]], 3, { seed: k + 40, col: '#5e3b20', a: 0.8 });
  }
  const body = circ(0, 10, 40, 62, 16, 0.04, 2); part(body, '#c99a5e', 3.4, { seed: 1 });
  for (let r = 0; r < 4; r++) for (let c = -1; c <= 1; c++) brush([[c * 16 - 6, -8 + r * 18], [c * 16, -2 + r * 18], [c * 16 + 6, -8 + r * 18]], 2, { seed: r * 3 + c, col: '#6b4424' });
  part([[-30, -80], [-40, -118], [-10, -92]], '#7d5230', 3, { seed: 2 }); part([[30, -80], [40, -118], [10, -92]], '#7d5230', 3, { seed: 3 });
  part(circ(0, -62, 40, 36, 16, 0.03, 3), '#a9763f', 3.4, { seed: 4 });
  part(circ(-15, -60, 17, 16, 12, 0, 1), '#e3a863', 2.4, { seed: 5 }); part(circ(15, -60, 17, 16, 12, 0, 2), '#e3a863', 2.4, { seed: 6 });
  for (const ex of [-15, 15]) { ctx.fillStyle = '#f2b72c'; ctx.beginPath(); ctx.arc(ex, -60, 9, 0, TAU); ctx.fill(); ctx.fillStyle = INK; ctx.beginPath(); ctx.arc(ex, -60, 5, 0, TAU); ctx.fill(); ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(ex + 2, -63, 1.6, 0, TAU); ctx.fill(); }
  part([[-6, -48], [6, -48], [0, -34]], '#3a2c20', 2, { seed: 7 });
  for (const sd of [-1, 1]) part([[sd * 10, 66], [sd * 20, 84], [sd * 4, 80]], '#6b4424', 2.4, { seed: 8 + sd });
  ctx.restore();
}
function ptero(x, y, s, f) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = '#5c5a82'; ctx.globalAlpha = 0.8;
  ctx.beginPath(); ctx.moveTo(-60, -f * 18); ctx.quadraticCurveTo(-26, -8 - f * 6, 0, 0); ctx.quadraticCurveTo(26, -8 - f * 6, 60, -f * 18); ctx.quadraticCurveTo(24, 4, 6, 6); ctx.lineTo(18, 2); ctx.lineTo(4, -4); ctx.quadraticCurveTo(-24, 4, -60, -f * 18); ctx.fill();
  ctx.restore();
}
function captionBox(x, y, w, lines, a) {
  if (a <= 0) return;
  ctx.save(); ctx.globalAlpha = clamp(a * 2); ctx.translate(0, (1 - eOut(clamp(a))) * -18);
  const h = 30 + lines.length * 42;
  wash([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], '#f6e7bd', { raw: true, gran: 0.3, edge: 0.4, off: [0, 0], a: 1 });
  inkRect(x, y, w, h, 3.6, 77);
  ctx.fillStyle = INK; ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic'; ctx.font = 'italic 36px "IM Fell English"';
  lines.forEach((l, i) => ctx.fillText(l, x + 24, y + 50 + i * 42));
  ctx.restore();
}
function roarBurst(x, y, u) {
  if (u <= 0) return;
  const k = backOut(clamp(u / 0.35), 2.4), pts = [];
  for (let i = 0; i < 26; i++) { const a = i / 26 * TAU, r = (i % 2 ? 150 : 210) * (1 + 0.12 * Math.sin(i * 2.7)); pts.push([Math.cos(a) * r * 1.35, Math.sin(a) * r * 0.62]); }
  ctx.save(); ctx.translate(x, y); ctx.rotate(-0.06); ctx.scale(k, k);
  ctx.fillStyle = '#fffbe8'; tracePts(pts, true); ctx.fill();
  wash(pts, '#f7d774', { raw: true, gran: 0.4, a: 0.55, off: [0, 0] });
  brush(pts.concat([pts[0]]), 4.4, { raw: true, ta: .02, tb: .02, seed: 3 });
  ctx.fillStyle = INK; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '112px "Caveat Brush"';
  ctx.fillText('RRROOAAR!', 0, 6);
  ctx.restore();
}

// the scene, drawn in scene space (1920 x 1080); t is scene time
function fantasyScene(t) {
  const p = seg(t, T.fan[0], T.snap);      // slow push-in / parallax
  const lay = (img, depth) => { ctx.save(); const sc = 1 + p * 0.05 * depth; ctx.translate(960, 540); ctx.scale(sc, sc); ctx.translate(-960 - p * 30 * depth, -540); ctx.drawImage(img, -FM, -FM); ctx.restore(); };
  lay(F_SKY, 0.2);
  // volcanic smoke drifting
  ctx.save(); const sc = 1 + p * 0.05 * 0.45; ctx.translate(960, 540); ctx.scale(sc, sc); ctx.translate(-960 - p * 13, -540);
  for (let i = 0; i < 10; i++) { const u = ((t * 0.12 + i / 10) % 1); softBlob(1380 + u * 180 + Math.sin(i * 3) * 20, 330 - u * 260, 40 + u * 90, i % 2 ? '#8b86a6' : '#a7a0b8', 0.45 * (1 - u)); }
  ctx.restore();
  lay(F_FAR, 0.45);
  // pterosaurs, far away
  const st = stp(t);
  for (let i = 0; i < 3; i++) { const u = st * 0.05 + i * 0.13; ptero(1000 + i * 150 - st * 40 - i * 30, 420 + i * 36 + Math.sin(st * 2 + i) * 8, 0.45 - i * 0.08, Math.sin(st * 7 + i * 2)); }
  lay(F_MID, 0.8);
  lay(F_NEAR, 1.1);
  // the Tyrannosaurus: survey, anticipation (head dips), ROAR
  ctx.save(); const sN = 1 + p * 0.05 * 1.1; ctx.translate(960, 540); ctx.scale(sN, sN); ctx.translate(-960 - p * 33, -540);
  const dip = eInOut(seg(st, T.roar - 0.45, T.roar - 0.05)), rise = eOut(seg(st, T.roar - 0.05, T.roar + 0.2));
  const head = -0.04 + 0.05 * Math.sin(st * 1.3) * (1 - dip) + 0.12 * dip - 0.3 * rise;
  const jaw = 0.06 * dip + 0.5 * rise;
  const shake = st > T.roar ? Math.sin(st * 60) * 3 * (1 - seg(st, T.roar, T.snap)) : 0;
  ctx.save(); ctx.globalAlpha = 0.35; ctx.fillStyle = rgrad(760, 850, 10, 300, [[0, '#3d3a20'], [1, 'rgba(61,58,32,0)']]); ctx.beginPath(); ctx.ellipse(760, 850, 330, 26, 0, 0, TAU); ctx.fill(); ctx.restore();
  rex(680 + shake, 652, 0.75, { t: st, head, jaw });
  ctx.restore();
  lay(F_FORE, 1.5);
  // Mortimer glides across, wingbeats then a long glide
  const ou = seg(t, T.fan[0], T.snap + 0.4), ox = lerp(1880, 1080, ou), oy = 250 - Math.sin(ou * Math.PI) * 40;
  const gl = seg(st, 4.8, 5.4), beat = Math.sin(st * 11) * lerp(1, 0.22, gl) - 0.12 * gl;
  owlFly(ox, oy + beat * 8, 0.7, beat, -0.08 + beat * 0.03);
  captionBox(64, 184, 600, ['The late Cretaceous. A lone', 'Tyrannosaurus surveys an', 'ancient forest of greens.'], seg(t, T.cap, T.cap + 0.35));
  roarBurst(1470, 590, seg(t, T.roar, T.roar + 0.5));
}
// in the page panel (page-local coords): the central band of the scene
function drawFantasyPanel(t, pw, ph) {
  const k = pw / W; ctx.save(); ctx.translate(pw / 2, ph / 2); ctx.scale(k, k); ctx.translate(-960, -540);
  fantasyScene(Math.min(t, T.snap - 0.3)); ctx.restore();
}
// expanding to full frame (screen coords)
function drawFantasyFull(t, r, ex, cam) {
  const [x, y, pw, ph] = PAN.fan, c0 = toScr(cam, x + pw / 2, y + ph / 2), k0 = pw / W * cam[2];
  const kk = lerp(k0, 1.0, ex), cx = lerp(c0[0], 960, ex), cy = lerp(c0[1], 540, ex);
  ctx.save(); ctx.beginPath(); ctx.rect(r[0], r[1], r[2] - r[0], r[3] - r[1]); ctx.clip();
  ctx.translate(cx, cy); ctx.scale(kk, kk); ctx.translate(-960, -540);
  fantasyScene(t);
  ctx.restore();
  // the panel's ink frame rides the expansion out past the screen edge
  if (ex < 1) { ctx.save(); ctx.globalAlpha = 1; inkRect(r[0], r[1], r[2] - r[0], r[3] - r[1], 5.5 * lerp(cam[2], 1.6, ex), 5); ctx.restore(); }
}
