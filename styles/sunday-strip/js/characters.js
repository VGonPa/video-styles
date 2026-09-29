// ── characters.js · Juniper (a girl, original), Mortimer (her stuffed owl), broccoli, props ──
const SKIN = '#f6d0ad', SKIN_D = '#e2a883', HAIR = '#b4532c', HAIR_D = '#8e3f22', TEAL = '#4a8b95', CREAM = '#f4ecd6';
const PANTS = '#52709f', SHOE = '#963a2b', BOW = '#d4432f', BLUSH = '#ee8f80';
const OWL = '#9a6c45', OWL_D = '#7a5234', OWL_BELLY = '#e3c793', OWL_FACE = '#f0dcb2', BEAK = '#d9973a';
const BROC = '#5f9a3f', BROC_D = '#3f7430', BROC_L = '#9cc26a', STALK = '#b9d08a';

// capsule polygon between two points (rounded ends)
function capsule(a, b, w1, w2 = w1, n = 8) {
  const ang = Math.atan2(b[1] - a[1], b[0] - a[0]), o = [];
  for (let i = 0; i <= n; i++) { const q = ang - Math.PI / 2 - i / n * Math.PI; o.push([a[0] + Math.cos(q) * w1 / 2, a[1] + Math.sin(q) * w1 / 2]); }
  for (let i = 0; i <= n; i++) { const q = ang + Math.PI / 2 - i / n * Math.PI; o.push([b[0] + Math.cos(q) * w2 / 2, b[1] + Math.sin(q) * w2 / 2]); }
  return o;
}
function part(pts, col, lw = 3.4, o = {}) { wash(pts, col, { base: '#fbf7ec', ...o }); inkShape(pts, lw, { seed: o.seed ?? (pts[0][0] + pts[0][1]) * 0.013, parts: o.parts }); }
function partRaw(pts, col, lw = 3.4, o = {}) { wash(pts, col, { ...o, raw: true }); brush(pts.concat([pts[0]]), lw, { raw: true, ta: .03, tb: .03, seed: o.seed ?? 2 }); }

// hands: small, simple, readable (palm + thumb + finger creases or an index finger)
function hand(x, y, ang, sz, mode = 'fist', side = 1) {
  const c = Math.cos(ang), s = Math.sin(ang), px = -s * side, py = c * side;
  const P = (u, v) => [x + c * u * sz + px * v * sz, y + s * u * sz + py * v * sz];
  if (mode === 'point') {
    part(capsule(P(0.25, 0.12), P(1.25, 0.12), sz * 0.26, sz * 0.22), SKIN, 2.8, { seed: 5 });
  }
  if (mode === 'flat') {
    const pal = []; for (let i = 0; i < 12; i++) { const a = i / 12 * TAU; pal.push(P(0.35 + Math.cos(a) * 0.55, Math.sin(a) * 0.3)); }
    part(pal, SKIN, 2.8, { seed: 6 });
    part(capsule(P(0.1, -0.28), P(0.5, -0.46), sz * 0.2, sz * 0.18), SKIN, 2.6, { seed: 7 });
    brush([P(0.62, -0.05), P(0.86, -0.04)], 2, { seed: 3 }); brush([P(0.62, 0.12), P(0.84, 0.13)], 2, { seed: 4 });
    return;
  }
  const pal = circ(...P(0.3, 0), sz * 0.44, sz * 0.4, 12, 0.08, 11);
  part(pal, SKIN, 2.8, { seed: 8 });
  part(capsule(P(0.2, -0.36), P(0.6, -0.34), sz * 0.22, sz * 0.2), SKIN, 2.6, { seed: 9 });   // thumb
  if (mode === 'fist') { brush([P(0.55, 0.05), P(0.72, 0.1)], 2.2, { seed: 1 }); brush([P(0.5, 0.22), P(0.66, 0.28)], 2.2, { seed: 2 }); }
  else { brush([P(0.5, 0.25), P(0.66, 0.3)], 2.2, { seed: 2 }); }
}
function fork(a, b, floret) {
  const ang = Math.atan2(b[1] - a[1], b[0] - a[0]), c = Math.cos(ang), s = Math.sin(ang);
  part(capsule(a, b, 9, 7), '#c9ccd0', 2.4, { seed: 12, gran: 0.2 });
  const base = [b[0] + c * 4, b[1] + s * 4];
  for (let k = -1.5; k <= 1.5; k++) { const o = [-s * k * 7, c * k * 7]; brush([[base[0] + o[0], base[1] + o[1]], [base[0] + o[0] + c * 34, base[1] + o[1] + s * 34]], 3.2, { seed: 20 + k }); }
  if (floret) broccoli(base[0] + c * 30, base[1] + s * 30, floret, 5, { ang: ang + Math.PI / 2 });
}

// a broccoli floret (and, much larger, a broccoli tree). origin at stalk base, grows along -y (rotated by o.ang)
function broccoli(x, y, s, seed = 1, o = {}) {
  const R = rng(seed * 97 + 3);
  ctx.save(); ctx.translate(x, y); ctx.rotate(o.ang || 0); ctx.scale(s, s);
  const lw = (o.lw || 3) / Math.sqrt(s) * (o.lwk || 1);
  // stalk with two branching arms
  const st = [[-13, 0], [13, 0], [11, -34], [30, -58], [22, -64], [4, -46], [-4, -46], [-22, -66], [-30, -58], [-11, -34]];
  part(st, o.stalk || STALK, lw, { seed: seed + 0.3, gran: 0.35, ...(o.base ? { base: o.base } : {}) });
  brush([[0, -6], [1, -38]], lw * 0.6, { seed: seed });
  // crown: scalloped cloud
  const cx = 0, cy = -84, rx = 54, ry = 40, nb = o.bumps || 11, cr0 = [];
  for (let i = 0; i < 64; i++) {
    const a = Math.PI * 0.62 + i / 64 * TAU;
    const k = 0.84 + 0.16 * Math.sqrt(Math.abs(Math.sin((a + seed) * nb / 2)));
    cr0.push([cx + Math.cos(a) * rx * k, cy + Math.sin(a) * ry * k * (Math.sin(a) > 0 ? 0.75 : 1)]);
  }
  wash(cr0, o.col || BROC, { raw: true, gran: 0.6, edge: 0.7 });
  // shaded underside + lit top (wet-in-wet)
  glaze(cr0, lgrad(0, cy - ry, 0, cy + ry, [[0, 'rgba(255,255,255,0)'], [1, o.dark || BROC_D]]), 0.55, true);
  softBlob(cx - 14, cy - 18, 26, o.light || BROC_L, 0.45);
  // floret buds: small scallop arcs inside
  const nd = o.detail ?? 16;
  for (let i = 0; i < nd; i++) {
    const a = R() * TAU, rr = Math.sqrt(R()) * 0.72, bx = cx + Math.cos(a) * rx * rr, by = cy + Math.sin(a) * ry * rr * 0.9, r = 5 + R() * 6;
    brush([[bx - r, by], [bx - r * 0.5, by - r * 0.8], [bx + r * 0.4, by - r * 0.8], [bx + r, by]], lw * 0.45, { seed: seed + i, col: o.budInk || INK, a: 0.75 });
  }
  brush(cr0.concat(cr0.slice(0, 3)), lw, { raw: true, ta: 0.03, tb: 0.03, seed: seed + 1.1 });
  ctx.restore();
}

// Mortimer, the stuffed owl (reality: felt, buttons, stitches). origin: bottom centre
function owlPlush(x, y, s, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(o.tilt || 0);
  const lw = 3.2 / Math.sqrt(s);
  part([[-12, 0], [-34, 8], [-36, -6]], '#c98a3a', lw * 0.8, { seed: 1 }); part([[12, 0], [34, 8], [36, -6]], '#c98a3a', lw * 0.8, { seed: 2 });
  const body = [[0, -150], [40, -146], [62, -122], [70, -72], [66, -26], [46, -4], [0, 2], [-46, -4], [-66, -26], [-70, -72], [-62, -122], [-40, -146]];
  part([[-38, -140], [-60, -182], [-14, -150]], OWL_D, lw, { seed: 3 }); part([[38, -140], [60, -182], [14, -150]], OWL_D, lw, { seed: 4 });
  part(body, OWL, lw, { seed: 5, gran: 0.7 });
  glaze(body, lgrad(-70, 0, 70, 0, [[0, 'rgba(255,255,255,0)'], [0.6, 'rgba(255,255,255,0)'], [1, OWL_D]]), 0.6);
  part([[-60, -104], [-84, -62], [-74, -18], [-54, -34], [-50, -80]], OWL_D, lw, { seed: 6 });
  part([[60, -104], [84, -62], [74, -18], [54, -34], [50, -80]], OWL_D, lw, { seed: 7 });
  const belly = circ(0, -48, 40, 42, 16, 0.04, 3); part(belly, OWL_BELLY, lw * 0.8, { seed: 8 });
  for (let r = 0; r < 3; r++) for (let c = -1; c <= 1; c++) { if (r === 2 && c) continue; const bx = c * 20 + (r % 2 ? 10 : 0) * 0, by = -66 + r * 20; brush([[bx - 8, by - 3], [bx, by + 4], [bx + 8, by - 3]], lw * 0.55, { seed: r * 3 + c }); }
  // stitches: dashed seam round the belly and down the crown
  ctx.save(); ctx.strokeStyle = INK; ctx.lineWidth = 1.6; ctx.setLineDash([5, 6]); tracePts(cr(circ(0, -48, 47, 49, 16, 0, 3), true, 4), true); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(0, -150); ctx.lineTo(0, -132); ctx.stroke(); ctx.restore();
  part(circ(-22, -110, 26, 25, 14, 0.05, 4), OWL_FACE, lw * 0.8, { seed: 9 }); part(circ(22, -110, 26, 25, 14, 0.05, 5), OWL_FACE, lw * 0.8, { seed: 10 });
  for (const ex of [-22, 22]) {   // button eyes, two thread holes, a glint
    ctx.fillStyle = INK; ctx.beginPath(); ctx.arc(ex, -110, 13, 0, TAU); ctx.fill();
    ctx.fillStyle = '#4b4540'; ctx.beginPath(); ctx.arc(ex, -110, 9, 0, TAU); ctx.fill();
    ctx.fillStyle = INK; ctx.beginPath(); ctx.arc(ex - 3, -110, 1.8, 0, TAU); ctx.arc(ex + 3, -110, 1.8, 0, TAU); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,0.85)'; ctx.beginPath(); ctx.ellipse(ex - 6, -116, 3, 2, -0.6, 0, TAU); ctx.fill();
  }
  part([[-9, -94], [9, -94], [0, -76]], BEAK, lw * 0.8, { seed: 11 });
  ctx.restore();
}

// Juniper, side view facing right, seated. origin = hip. o: {x,y,s,arm:'rest'|'lecture'|'fork', eye:'open'|'smug'|'wide'|'down', mouth, headRot, floret}
function girlSide(o) {
  ctx.save(); ctx.translate(o.x, o.y); ctx.scale(o.s, o.s);
  const lw = 3.6;
  // far leg (behind, a touch darker)
  ctx.save(); ctx.translate(-14, -5);
  part([[-10, -18], [60, -17], [100, -13], [112, 6], [102, 24], [60, 21], [0, 21]], '#435d88', lw, { seed: 1 });
  part([[84, 8], [111, 7], [107, 60], [105, 90], [86, 90], [84, 50]], '#435d88', lw, { seed: 2 });
  part([[82, 88], [107, 86], [131, 94], [135, 108], [82, 110]], '#7e2f23', lw, { seed: 3 });
  ctx.restore();
  // far arm (just a hand on the table for 'rest' / 'lecture')
  // torso: striped shirt
  const shirt = [[-30, 12], [-35, -40], [-30, -100], [-14, -134], [18, -142], [42, -124], [50, -80], [48, -30], [42, 10], [5, 16]];
  wash(shirt, CREAM, { gran: 0.3 });
  ctx.save(); tracePts(cr(shirt, true, 6), true); ctx.clip();
  for (let k = 0; k < 8; k++) { const yy = -136 + k * 21; wash([[-50, yy], [70, yy - 4], [70, yy + 9], [-50, yy + 13]], TEAL, { gran: 0.4, edge: 0.3, off: [0, 0] }); }
  ctx.restore();
  inkShape(shirt, lw, { seed: 4 });
  // near leg: thigh, knee, shin, shoe
  part([[-10, -18], [60, -17], [100, -13], [112, 6], [102, 24], [60, 21], [0, 21]], PANTS, lw, { seed: 5 });
  part([[84, 8], [111, 7], [107, 60], [105, 90], [86, 90], [84, 50]], PANTS, lw, { seed: 6 });
  brush([[92, 88], [104, 88]], 2, { seed: 1 });
  part([[82, 88], [107, 86], [131, 94], [135, 108], [82, 110]], SHOE, lw, { seed: 7 });
  // head group (neck pivot)
  ctx.save(); ctx.translate(15, -150); ctx.rotate(o.headRot || 0); ctx.translate(-15, 150);
  part([[2, -168], [28, -170], [30, -130], [4, -128]], SKIN, lw, { seed: 8 });
  const pig = [[-44, -252], [-80, -270], [-104, -262], [-104, -234], [-82, -220], [-46, -222]];
  part(pig, HAIR, lw, { seed: 9 });
  brush([[-58, -246], [-94, -250]], 1.8, { seed: 2, col: HAIR_D }); brush([[-60, -234], [-92, -238]], 1.8, { seed: 3, col: HAIR_D });
  const head = [[0, -284], [40, -282], [66, -266], [76, -246], [80, -236], [97, -224], [92, -213], [81, -210], [83, -200], [79, -191], [72, -180], [54, -166], [30, -160], [4, -166], [-24, -180], [-40, -204], [-44, -236], [-32, -266]];
  part(head, SKIN, lw, { seed: 10 });
  glaze(head, lgrad(-40, 0, 90, 0, [[0, SKIN_D], [0.45, 'rgba(255,255,255,0)']]), 0.5);
  softBlob(52, -198, 17, BLUSH, 0.35);
  const hair = [[-8, -298], [36, -296], [66, -278], [80, -256], [70, -250], [62, -262], [48, -254], [36, -262], [22, -250], [8, -246], [-2, -226], [-8, -200], [-20, -176], [-40, -188], [-52, -222], [-46, -264], [-28, -288]];
  part(hair, HAIR, lw, { seed: 11 });
  glaze(hair, lgrad(0, -300, 0, -180, [[0, 'rgba(255,255,255,0)'], [1, HAIR_D]]), 0.5);
  brush([[10, -286], [26, -262]], 1.8, { seed: 5, col: HAIR_D }); brush([[-20, -280], [-26, -240]], 1.8, { seed: 6, col: HAIR_D });
  // bow
  part([[-48, -246], [-66, -274], [-38, -270]], BOW, 3, { seed: 12 }); part([[-48, -246], [-70, -224], [-40, -226]], BOW, 3, { seed: 13 });
  part(circ(-48, -246, 7, 7, 8, 0, 2), BOW, 2.6, { seed: 14 });
  // ear
  part([[6, -224], [-6, -232], [-14, -216], [-8, -200], [6, -204]], SKIN, 3, { seed: 15 });
  brush([[0, -222], [-6, -214], [0, -208]], 1.8, { seed: 7 });
  // eye + brow
  const ex = 60 + (o.eyeDX || 0), ey = -232 + (o.eyeDY || 0);
  const e = o.eye || 'open';
  if (e === 'smug') { brush([[ex - 9, ey], [ex, ey + 5], [ex + 9, ey + 1]], 3.4, { seed: 8 }); brush([[ex - 10, ey - 20], [ex + 10, ey - 24]], 3, { seed: 9 }); }
  else if (e === 'blink') { brush([[ex - 8, ey + 2], [ex + 8, ey + 2]], 3.4, { seed: 8 }); brush([[ex - 10, ey - 18], [ex + 10, ey - 19]], 3, { seed: 9 }); }
  else {
    const big = e === 'wide' ? 1.35 : 1;
    ctx.fillStyle = INK; ctx.beginPath(); ctx.ellipse(ex, ey, 5.2 * big, 8.5 * big, 0, 0, TAU); ctx.fill();
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(ex + 1.5, ey - 3, 1.6 * big, 0, TAU); ctx.fill();
    if (e === 'wide') brush([[ex - 10, ey - 26], [ex + 1, ey - 31], [ex + 11, ey - 27]], 3, { seed: 9 });
    else if (e === 'down') brush([[ex - 10, ey - 17], [ex + 11, ey - 14]], 3.2, { seed: 9 });
    else brush([[ex - 10, ey - 20], [ex + 10, ey - 21]], 3, { seed: 9 });
  }
  const m = o.mouth || 'flat';
  if (m === 'flat') brush([[70, -193], [80, -194]], 2.6, { seed: 10 });
  if (m === 'smug') brush([[66, -196], [74, -191], [82, -196]], 2.6, { seed: 10 });
  if (m === 'talk') { part([[70, -198], [82, -199], [80, -188], [72, -189]], '#7a2e25', 2.2, { seed: 16, gran: 0 }); }
  if (m === 'wobble') brush([[68, -192], [72, -195], [76, -191], [81, -194]], 2.4, { seed: 10 });
  ctx.restore();
  // near arm
  const S = [14, -118];
  const pose = { rest: [[66, -66], [122, -74], 0.05, 'flat'], lecture: [[60, -66], [72, -146], -1.45, 'point'], fork: [[66, -66], [112, -110], -0.9, 'fist'] }[o.arm || 'rest'];
  const [E, Wr, ha, hm] = pose; const Wr2 = o.wrist ? [Wr[0] + o.wrist[0], Wr[1] + o.wrist[1]] : Wr;
  if (o.arm === 'fork') fork([Wr2[0] - 6, Wr2[1] + 10], [Wr2[0] + 22 + (o.forkDX || 0), Wr2[1] - 52], o.floret);
  part(capsule(E, Wr2, 23, 20), SKIN, lw, { seed: 17 });
  part(capsule(S, [lerp(S[0], E[0], 0.5), lerp(S[1], E[1], 0.5)], 40, 32), CREAM, lw, { seed: 18 });
  ctx.save(); tracePts(cr(capsule(S, [lerp(S[0], E[0], 0.5), lerp(S[1], E[1], 0.5)], 40, 32), true, 6), true); ctx.clip();
  for (let k = 0; k < 4; k++) { const yy = -138 + k * 21; wash([[-20, yy], [80, yy - 4], [80, yy + 9], [-20, yy + 13]], TEAL, { gran: 0.4, edge: 0.3, off: [0, 0] }); }
  ctx.restore(); inkShape(capsule(S, [lerp(S[0], E[0], 0.5), lerp(S[1], E[1], 0.5)], 40, 32), lw, { seed: 19 });
  brush([E, [E[0] - 4, E[1] + 5]], 2.2, { seed: 3 });   // elbow crease
  hand(Wr2[0], Wr2[1], ha, 30, hm, 1);
  ctx.restore();
}

// Juniper close-up, front 3/4, suspicious squint at the broccoli. panel-local coords (600 x 720). sq: 0..1
function girlClose(sq, look, t) {
  ctx.save(); ctx.translate(-34, 6);
  const lw = 4.4;
  const shirt = [[-40, 730], [0, 650], [120, 588], [220, 570], [320, 570], [420, 588], [540, 650], [600, 730]];
  wash(shirt, CREAM, { gran: 0.3 });
  ctx.save(); tracePts(cr(shirt, true, 6), true); ctx.clip();
  for (let k = 0; k < 6; k++) { const yy = 580 + k * 30; wash([[-60, yy], [640, yy - 6], [640, yy + 13], [-60, yy + 19]], TEAL, { gran: 0.4, edge: 0.3, off: [0, 0] }); }
  ctx.restore(); inkShape(shirt, lw, { seed: 2 });
  part([[222, 480], [318, 480], [326, 590], [214, 590]], SKIN, lw, { seed: 3 });
  brush([[212, 588], [270, 612], [328, 588]], lw, { seed: 4 });
  ctx.save(); ctx.translate(270, 0); ctx.scale(0.9, 1); ctx.translate(-270, 0);
  // pigtails + bows
  part([[98, 250], [42, 226], [10, 258], [18, 312], [60, 322], [100, 300]], HAIR, lw, { seed: 5 });
  part([[442, 250], [498, 226], [530, 258], [522, 312], [480, 322], [440, 300]], HAIR, lw, { seed: 6 });
  part(circ(88, 350, 26, 40, 12, 0.05, 1), SKIN, lw, { seed: 7 }); part(circ(452, 350, 26, 40, 12, 0.05, 2), SKIN, lw, { seed: 8 });
  const face = [[270, 168], [382, 190], [440, 258], [452, 350], [430, 440], [372, 506], [270, 530], [168, 506], [110, 440], [88, 350], [100, 258], [158, 190]];
  part(face, SKIN, lw, { seed: 9 });
  glaze(face, lgrad(80, 0, 460, 0, [[0, SKIN_D], [0.35, 'rgba(255,255,255,0)'], [0.85, 'rgba(255,255,255,0)'], [1, SKIN_D]]), 0.45);
  softBlob(170, 440, 34, BLUSH, 0.32); softBlob(372, 440, 34, BLUSH, 0.32);
  const hair = [[90, 300], [95, 220], [150, 150], [230, 116], [320, 116], [400, 150], [455, 220], [455, 300], [432, 268], [412, 236], [386, 262], [360, 230], [330, 258], [300, 226], [270, 254], [240, 224], [210, 254], [180, 226], [150, 260], [126, 236], [108, 274]];
  part(hair, HAIR, lw, { seed: 10 });
  glaze(hair, lgrad(0, 110, 0, 300, [[0, 'rgba(255,255,255,0)'], [1, HAIR_D]]), 0.45);
  for (const [a, b] of [[[200, 140], [230, 200]], [[300, 130], [290, 196]], [[380, 160], [360, 214]], [[150, 180], [140, 230]]]) brush([a, b], 2.2, { seed: a[0], col: HAIR_D });
  for (const bx of [96, 444]) { part([[bx, 262], [bx - 28, 234], [bx - 26, 286]], BOW, 3.4, { seed: bx }); part([[bx, 262], [bx + 28, 236], [bx + 26, 288]], BOW, 3.4, { seed: bx + 1 }); part(circ(bx, 262, 9, 9, 8, 0, 3), BOW, 3, { seed: bx + 2 }); }
  // eyes: dots under lowering lids
  const blink = 0;
  for (const [ex, side] of [[205, -1], [335, 1]]) {
    const ry = lerp(15, 5, sq), dx = look[0], dy = look[1];
    ctx.fillStyle = INK; ctx.beginPath(); ctx.ellipse(ex + dx, 362 + dy + sq * 5, 9, ry, 0, 0, TAU); ctx.fill();
    if (sq < 0.7) { ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(ex + dx + 3, 356 + dy + sq * 5, 2.4, 0, TAU); ctx.fill(); }
    const inner = side < 0 ? 1 : -1;  // inner corner (towards the nose) sits lower: suspicion
    const yl = 362 - ry - 3 + sq * 5;
    brush([[ex - 26 * inner, yl - 2 - sq * 2], [ex, yl - 1], [ex + 26 * inner, yl + sq * 8]], 5.2, { seed: ex, ta: .1, tb: .3 });
    if (sq > 0.3) brush([[ex - 20, 362 + ry + 5 + sq * 5], [ex + 20, 362 + ry + 3 + sq * 5]], 2.4, { seed: ex + 1, a: sq });
    // brow
    brush([[ex - 30 * inner, 314 - sq * 6], [ex + 26 * inner, 316 + sq * 20]], 5.6, { seed: ex + 2 });
  }
  brush([[262, 392], [278, 410], [262, 418]], 3.2, { seed: 11 });
  brush([[240, 466 + sq * 2], [256, 462], [270, 465 - sq * 2], [286, 461], [300, 467 + sq * 3]], 3.4, { seed: 12 });
  ctx.restore(); ctx.restore();
  // her fist and fork, broccoli held up for inspection (foreground)
  const rot = Math.sin(t * 2.2) * 0.05 * (1 - sq);
  part(capsule([660, 800], [512, 640], 84, 72), SKIN, lw, { seed: 13 });
  ctx.save(); ctx.translate(495, 610); ctx.rotate(rot); ctx.translate(-495, -610);
  fork([495, 640], [478, 470], 1.25);
  ctx.restore();
  hand(506, 616, -1.75, 96, 'fist', -1);
}

function plate(x, y, s, florets) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  part([[-80, 0], [-64, 14], [64, 14], [80, 0]], '#dfe6ea', 3, { seed: 1 });
  const top = circ(0, 0, 118, 16, 22, 0, 2); part(top, '#f7f7f2', 3.2, { seed: 2, gran: 0.2 });
  ctx.save(); tracePts(cr(circ(0, 0, 118, 16, 22, 0, 2), true, 5), true); ctx.clip();
  ctx.strokeStyle = '#6f9fc4'; ctx.lineWidth = 6; ctx.globalAlpha = 0.6; ctx.beginPath(); ctx.ellipse(2, 1, 104, 12, 0, 0, TAU); ctx.stroke(); ctx.restore();
  ctx.restore();
  for (const [dx, a, k, sd] of florets) broccoli(x + dx * s, y + 2 * s, 0.42 * s * k, sd, { ang: a, detail: 6 });
}
function milk(x, y, s) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  wash([[-26, -110], [26, -110], [22, 0], [-22, 0]], '#dfe9ef', { gran: 0.2, a: 0.8, base: '#fbf7ec' });
  wash([[-24.5, -82], [24.5, -82], [22, -2], [-22, -2]], '#fbfbf5', { gran: 0.15, off: [0, 0] });
  glaze([[-24.5, -82], [24.5, -82], [22, -2], [-22, -2]], lgrad(-25, 0, 25, 0, [[0, '#c9d6e0'], [0.4, 'rgba(255,255,255,0)'], [1, '#c9d6e0']]), 0.6);
  brush([[-26, -110], [-22, 0]], 3, { seed: 5 }); brush([[26, -110], [22, 0]], 3, { seed: 6 });
  brush(cr(circ(0, -110, 26, 6, 12, 0, 2), true, 4).concat([[26, -110]]), 2.4, { raw: true, seed: 7, ta: .02, tb: .02 });
  brush(cr(circ(0, -82, 24.5, 5, 12, 0, 3), true, 4).slice(0, 25), 2, { raw: true, seed: 8, ta: .05, tb: .05 });
  brush([[-22, 0], [0, 4], [22, 0]], 3, { seed: 9 });
  brush([[-15, -100], [-13, -18]], 4, { col: '#ffffff', seed: 4, a: 0.9 });
  ctx.restore();
}
