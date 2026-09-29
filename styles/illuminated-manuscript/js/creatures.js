// creatures.js · the snail knight, the trumpeting rabbit, the loaf, and the oven miniature

function inkShape(g, fill, lw = 2) { if (fill) { g.fillStyle = fill; g.fill(); } g.strokeStyle = COL.ink; g.lineWidth = lw; g.stroke(); }
function ell(g, x, y, rx, ry, a = 0) { g.beginPath(); g.ellipse(x, y, rx, ry, a, 0, TAU); }

// ── the snail knight (faces right, origin = front of the foot on the ground line) ──
// st: { ret: 0..1 withdraw, bob: phase, helm: {x,y,a} or null (attached), lance: extra droop }
function snail(g, x, y, s, st) {
  const ret = st.ret || 0, bob = st.bob || 0;
  g.save(); g.translate(x, y); g.scale(s, s); g.lineJoin = 'round'; g.lineCap = 'round';
  const SC = [-62, -50];
  // lance (behind the shell) — tournament lance with red spiral, vamplate, pennant
  g.save(); g.translate(SC[0], SC[1]); g.rotate(-0.12 + (st.lance || 0) + Math.sin(bob * 2) * 0.02);
  g.beginPath(); g.moveTo(-50, -3); g.lineTo(200, -1.5); g.lineTo(200, 1.5); g.lineTo(-50, 4); g.closePath(); inkShape(g, '#e3cf9c', 1.6);
  g.save(); g.clip(); g.strokeStyle = COL.red; g.lineWidth = 4; for (let k = -50; k < 200; k += 16) { g.beginPath(); g.moveTo(k, 5); g.lineTo(k + 8, -5); g.stroke(); } g.restore();
  g.beginPath(); g.moveTo(22, -12); g.lineTo(40, -2); g.lineTo(40, 2); g.lineTo(22, 12); g.closePath(); inkShape(g, '#b9b9b0', 1.5);
  const wv = Math.sin(bob * 3) * 3;
  g.beginPath(); g.moveTo(150, -2); g.lineTo(188, -4 + wv); g.lineTo(176, 5 + wv * 0.5); g.lineTo(190, 14 + wv); g.lineTo(150, 12); g.closePath(); inkShape(g, COL.red, 1.4);
  g.fillStyle = COL.g1; g.beginPath(); g.arc(162, 6, 3, 0, TAU); g.fill();
  g.restore();
  // body (foot + neck + head) — scales into the shell as it withdraws
  const k = 1 - 0.9 * eInOut(ret);
  g.save(); g.translate(SC[0], SC[1]); g.scale(k, k); g.translate(-SC[0], -SC[1]);
  const nb = Math.sin(bob) * 2.5;
  g.beginPath(); g.moveTo(-128, 0); g.quadraticCurveTo(-134, -9, -112, -14); g.lineTo(-28, -16);
  g.quadraticCurveTo(-18, -26 + nb, -12, -44 + nb); g.quadraticCurveTo(-2, -64 + nb, 14, -54 + nb); g.quadraticCurveTo(24, -44 + nb, 18, -28);
  g.quadraticCurveTo(14, -8, 4, 0); g.closePath(); inkShape(g, '#b7b58f', 2);
  g.strokeStyle = 'rgba(80,70,40,0.35)'; g.lineWidth = 1; for (let i = -120; i < -20; i += 12) { g.beginPath(); g.moveTo(i, -3); g.lineTo(i + 6, -11); g.stroke(); }
  // eyestalks (poke through the helm's crown when it is on)
  const es = 1 - 0.8 * clamp(ret * 2);
  for (const [dx, ph] of [[0, 0], [9, 1.3]]) {
    const bx = 2 + dx, by = -60 + nb, tx = bx + 6 + Math.sin(bob * 1.7 + ph) * 4, ty = by - 26 * es;
    g.strokeStyle = COL.ink; g.lineWidth = 2.2; g.beginPath(); g.moveTo(bx, by); g.quadraticCurveTo(bx - 2, (by + ty) / 2, tx, ty); g.stroke();
    ell(g, tx, ty, 3.6, 3.6); inkShape(g, '#2b2518', 1);
  }
  g.restore();
  // shell with spiral, shield
  ell(g, SC[0], SC[1], 46, 44); const sg = g.createRadialGradient(SC[0] - 14, SC[1] - 16, 5, SC[0], SC[1], 48);
  sg.addColorStop(0, '#f0c98c'); sg.addColorStop(0.6, '#cf8c52'); sg.addColorStop(1, '#a8603a'); inkShape(g, sg, 2.2);
  g.strokeStyle = COL.ink; g.lineWidth = 1.8; g.beginPath();
  for (let a = 0; a < TAU * 2.6; a += 0.08) { const rr2 = 42 - a * 2.5; g.lineTo(SC[0] + Math.cos(a + 1.2) * rr2 * 1.02, SC[1] + Math.sin(a + 1.2) * rr2); } g.stroke();
  g.strokeStyle = 'rgba(255,245,215,0.7)'; g.lineWidth = 2; g.beginPath(); g.arc(SC[0] - 6, SC[1] - 6, 36, 3.6, 4.6); g.stroke();
  // heater shield: azure, a loaf or
  g.save(); g.translate(SC[0] + 6, SC[1] + 2); g.rotate(0.1);
  g.beginPath(); g.moveTo(-15, -17); g.lineTo(15, -17); g.lineTo(15, 0); g.quadraticCurveTo(14, 14, 0, 21); g.quadraticCurveTo(-14, 14, -15, 0); g.closePath(); inkShape(g, COL.blue, 1.6);
  ell(g, 0, -1, 8, 5.5); inkShape(g, COL.g1, 1); g.strokeStyle = COL.g3; g.lineWidth = 1; g.beginPath(); g.moveTo(-3, -4); g.lineTo(-1, 2); g.moveTo(2, -4); g.lineTo(4, 2); g.stroke();
  g.restore();
  // great helm: sits on the head, or has fallen (st.helm gives its own pose)
  const hp = st.helm || { x: 4, y: -58 + nb, a: 0 };
  g.save(); g.translate(hp.x, hp.y); g.rotate(hp.a); g.scale(st.helm ? 1 : k, st.helm ? 1 : k);
  g.beginPath(); g.moveTo(-14, 10); g.lineTo(-14, -12); g.quadraticCurveTo(-14, -24, 2, -24); g.quadraticCurveTo(18, -24, 18, -12); g.lineTo(18, 10); g.closePath();
  const hg = g.createLinearGradient(-14, 0, 18, 0); hg.addColorStop(0, '#8d9096'); hg.addColorStop(0.45, '#e4e6e8'); hg.addColorStop(1, '#7c7f85'); inkShape(g, hg, 1.8);
  g.strokeStyle = COL.ink; g.lineWidth = 2.4; g.beginPath(); g.moveTo(-10, -6); g.lineTo(18, -6); g.stroke();
  g.fillStyle = COL.ink; for (let i = 0; i < 3; i++) { g.beginPath(); g.arc(8 + i * 3.5, 4, 1, 0, TAU); g.fill(); }
  g.beginPath(); g.moveTo(-2, -24); g.quadraticCurveTo(-18, -44, -34, -30); g.quadraticCurveTo(-20, -34, -8, -22); g.closePath(); inkShape(g, COL.red, 1.4);
  g.restore();
  g.restore();
}

// ── the rabbit (faces left, origin = ground under the body) ──
// st: { pose: 'trumpet'|'loaf', trA: trumpet angle, blow: 0..1, air: hop 0..1, t }
function rabbit(g, x, y, s, st) {
  const air = st.air || 0, hopUp = Math.sin(Math.PI * air);
  g.save(); g.translate(x, y - hopUp * 34 * s); g.scale(s * (st.dir || 1), s); g.lineJoin = 'round'; g.lineCap = 'round';
  const lean = (st.lean || 0) - hopUp * 0.35;
  const fur = '#b9a07c', furD = '#8a7152', belly = '#f3ead6';
  // hind foot (stretches back when airborne)
  g.save(); g.translate(18, -6); g.rotate(hopUp * 0.7);
  ell(g, 10, 0, 28, 8); inkShape(g, fur, 1.8); g.restore();
  g.save(); g.rotate(lean);
  ell(g, 40, -34, 11, 10); inkShape(g, belly, 1.6);                 // tail
  ell(g, 18, -30, 28, 25, -0.3); inkShape(g, fur, 2);                  // haunch
  g.strokeStyle = furD; g.lineWidth = 1.2; g.beginPath(); g.arc(18, -30, 17, 3.6, 5.2); g.stroke();
  ell(g, 0, -64, 26, 40, 0.12); inkShape(g, fur, 2);                   // body
  ell(g, -12, -62, 13, 28, 0.12); g.fillStyle = belly; g.fill();
  // head
  const puff = (st.blow || 0) * 4;
  g.save(); g.translate(-12, -116);
  // ears
  for (const [a, l, bend] of [[-1.25, 62, 0], [-0.9, 56, 0.35]]) {
    g.save(); g.translate(6, -12); g.rotate(a + Math.sin((st.t || 0) * 5 + a) * 0.04);
    g.beginPath(); g.moveTo(0, -7); g.quadraticCurveTo(l * 0.6, -12, l, -2 + bend * 18); g.quadraticCurveTo(l * 0.6, 12, 0, 7); g.closePath(); inkShape(g, fur, 1.8);
    g.beginPath(); g.moveTo(8, -2); g.quadraticCurveTo(l * 0.6, -5, l - 8, bend * 14); g.quadraticCurveTo(l * 0.6, 5, 8, 2); g.closePath(); g.fillStyle = '#e3a5a0'; g.fill();
    g.restore();
  }
  g.beginPath(); g.moveTo(22, 4); g.quadraticCurveTo(24, -20, 2, -22); g.quadraticCurveTo(-18, -22, -24, -8 - puff * 0.3);
  g.quadraticCurveTo(-32 - puff, 0, -26, 8 + puff * 0.5); g.quadraticCurveTo(-12, 18, 8, 16); g.quadraticCurveTo(20, 14, 22, 4); g.closePath(); inkShape(g, fur, 2);
  ell(g, -8, -8, 3.4, 3.8); g.fillStyle = COL.ink; g.fill(); g.fillStyle = '#fff'; g.beginPath(); g.arc(-9, -9.5, 1.1, 0, TAU); g.fill();
  ell(g, -28 - puff * 0.8, -2, 3, 2.4); g.fillStyle = '#9c5a55'; g.fill();
  g.strokeStyle = 'rgba(40,25,15,0.6)'; g.lineWidth = 0.9; for (const dy of [-2, 3]) { g.beginPath(); g.moveTo(-22, 2); g.lineTo(-40, 2 + dy * 2); g.stroke(); }
  g.restore();
  // forepaws + prop
  if (st.pose === 'trumpet') {
    g.save(); g.translate(-38, -112); g.rotate(st.trA || 0);
    // banner hanging from the tube
    const fl = Math.sin((st.t || 0) * 7) * 3;
    g.beginPath(); g.moveTo(-40, 2); g.lineTo(-86, 2); g.lineTo(-86 + fl * 0.3, 36); g.lineTo(-74, 28 + fl * 0.3); g.lineTo(-63, 36 + fl * 0.2); g.lineTo(-40, 32); g.closePath(); inkShape(g, COL.blue, 1.4);
    g.strokeStyle = COL.g1; g.lineWidth = 2; g.beginPath(); g.moveTo(-44, 7); g.lineTo(-82, 7); g.stroke();
    g.fillStyle = COL.g1; g.beginPath(); g.arc(-62, 18, 4, 0, TAU); g.fill();
    // tube and bell
    const tg = g.createLinearGradient(0, -4, 0, 4); tg.addColorStop(0, COL.g0); tg.addColorStop(0.5, COL.g2); tg.addColorStop(1, COL.g3);
    g.beginPath(); g.moveTo(0, -3); g.lineTo(-104, -3); g.lineTo(-104, 3); g.lineTo(0, 3); g.closePath(); inkShape(g, tg, 1.4);
    g.beginPath(); g.moveTo(-100, -3); g.quadraticCurveTo(-116, -5, -126, -16); g.lineTo(-126, 16); g.quadraticCurveTo(-116, 5, -100, 3); g.closePath(); inkShape(g, tg, 1.6);
    // sound: arcs from the bell
    const b = st.blow || 0;
    if (b > 0) for (let i = 0; i < 3; i++) {
      const ph = ((st.t || 0) * 3.2 + i / 3) % 1; g.strokeStyle = `rgba(184,50,31,${(1 - ph) * b})`; g.lineWidth = 2.2;
      g.beginPath(); g.arc(-126, 0, 12 + ph * 46, Math.PI - 0.6, Math.PI + 0.6); g.stroke();
    }
    g.restore();
    // paw on the tube
    g.save(); g.translate(-38, -112); g.rotate(st.trA || 0); ell(g, -26, 5, 8, 6); inkShape(g, fur, 1.6); g.restore();
    g.beginPath(); g.moveTo(-6, -92); g.quadraticCurveTo(-22, -96, -36 + Math.cos(st.trA || 0) * -26 * 0.3, -106 + Math.sin(st.trA || 0) * -26); g.strokeStyle = COL.ink; g.lineWidth = 9; g.stroke(); g.strokeStyle = fur; g.lineWidth = 6; g.stroke();
  } else if (st.pose === 'loaf') {
    loaf(g, -34, -78, 0.8, -0.2);
    g.beginPath(); g.moveTo(-4, -92); g.quadraticCurveTo(-24, -92, -38, -84); g.strokeStyle = COL.ink; g.lineWidth = 9; g.stroke(); g.strokeStyle = fur; g.lineWidth = 6; g.stroke();
    ell(g, -40, -84, 7, 5.5); inkShape(g, fur, 1.4);
  }
  g.restore(); g.restore();
}

function loaf(g, x, y, s, a = 0) {
  g.save(); g.translate(x, y); g.rotate(a); g.scale(s, s);
  g.beginPath(); g.moveTo(-36, 10); g.quadraticCurveTo(-40, -18, 0, -22); g.quadraticCurveTo(40, -18, 36, 10); g.quadraticCurveTo(0, 16, -36, 10); g.closePath();
  const lg = g.createLinearGradient(0, -22, 0, 14); lg.addColorStop(0, '#e9b262'); lg.addColorStop(0.55, '#c07c34'); lg.addColorStop(1, '#8f5220'); inkShape(g, lg, 2);
  g.strokeStyle = '#f6dca0'; g.lineWidth = 3; for (const dx of [-16, 0, 16]) { g.beginPath(); g.moveTo(dx - 6, -12); g.lineTo(dx + 6, -2); g.stroke(); }
  g.strokeStyle = 'rgba(255,245,215,0.6)'; g.lineWidth = 2; g.beginPath(); g.moveTo(-26, -10); g.quadraticCurveTo(-18, -18, -4, -19); g.stroke();
  g.restore();
}

// grassy ground line of a bas-de-page
function groundLine(g, x0, x1, y, seed, u = 1) {
  const r = mulberry(seed); g.save(); g.strokeStyle = COL.ink; g.lineWidth = 1.6; g.beginPath();
  const xe = lerp(x0, x1, u); for (let x = x0; x <= xe; x += 8) g.lineTo(x, y + Math.sin(x * 0.05) * 2);
  g.stroke();
  for (let x = x0 + 6; x < xe; x += 14 + r() * 16) {
    g.strokeStyle = COL.green; g.lineWidth = 1.6; const h = 6 + r() * 9;
    g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x - 2, y - h * 0.6, x - 5, y - h); g.moveTo(x + 2, y); g.quadraticCurveTo(x + 4, y - h * 0.5, x + 7, y - h * 0.8); g.stroke();
    if (r() < 0.2) { g.fillStyle = r() < 0.5 ? COL.red : COL.blue; g.beginPath(); g.arc(x - 5, y - h - 2, 2.6, 0, TAU); g.fill(); }
  }
  g.restore();
}

// ── the miniature: a domed bread oven before a diapered ground (baked ink + colour layers) ──
const MIN = { x: 110, y: 120, w: 610, h: 470, fr: 14, band: 9 };
MIN.ix = MIN.x + MIN.fr + MIN.band; MIN.iy = MIN.y + MIN.fr + MIN.band; MIN.iw = MIN.w - 2 * (MIN.fr + MIN.band); MIN.ih = MIN.h - 2 * (MIN.fr + MIN.band);
let MINI_INK, MINI_COL;
const OVEN = { x: 350, y: 330, rx: 150, ry: 140, mw: 46, mh: 72 };   // interior coords
function bakeMiniature() {
  const W = MIN.iw, H = MIN.ih;
  const build = (colour) => {
    const c = mk(W, H), g = c.getContext('2d'), r = mulberry(21); g.lineJoin = 'round'; g.lineCap = 'round';
    const F = (f) => colour ? f : null;
    // diaper
    if (colour) {
      g.fillStyle = COL.blueD; g.fillRect(0, 0, W, H); const S = 44;
      g.save(); g.translate(W / 2, 0); g.rotate(Math.PI / 4);
      for (let i = -14; i < 14; i++) for (let j = -14; j < 14; j++) { g.fillStyle = (i + j) & 1 ? '#8e2a22' : '#28478f'; g.fillRect(i * S, j * S, S, S); }
      g.strokeStyle = 'rgba(245,225,170,0.35)'; g.lineWidth = 1.2;
      for (let i = -14; i < 14; i++) { g.beginPath(); g.moveTo(i * S, -14 * S); g.lineTo(i * S, 14 * S); g.moveTo(-14 * S, i * S); g.lineTo(14 * S, i * S); g.stroke(); }
      for (let i = -14; i < 14; i++) for (let j = -14; j < 14; j++) { g.fillStyle = COL.g1; g.beginPath(); g.arc(i * S, j * S, 2.8, 0, TAU); g.fill(); if ((i + j) & 1) { g.fillStyle = 'rgba(255,240,215,0.5)'; g.beginPath(); g.arc(i * S + S / 2, j * S + S / 2, 1.8, 0, TAU); g.fill(); } }
      g.restore();
    }
    // hill
    g.beginPath(); g.moveTo(0, 318); g.bezierCurveTo(120, 280, 260, 300, 380, 302); g.bezierCurveTo(470, 304, 520, 285, W, 296); g.lineTo(W, H); g.lineTo(0, H); g.closePath();
    const hg = g.createLinearGradient(0, 290, 0, H); hg.addColorStop(0, '#5f9a57'); hg.addColorStop(1, '#2f6441'); inkShape(g, F(hg), 2);
    if (colour) for (let i = 0; i < 38; i++) { const x = r() * W, y = 330 + r() * 90; g.strokeStyle = COL.greenD; g.lineWidth = 1.2; g.beginPath(); g.moveTo(x, y); g.lineTo(x - 3, y - 8); g.moveTo(x, y); g.lineTo(x + 3, y - 8); g.stroke(); if (r() < 0.45) { g.fillStyle = r() < 0.5 ? '#fff6e6' : '#d8453a'; g.beginPath(); g.arc(x, y - 10, 3, 0, TAU); g.fill(); } }
    // oven dome (bricks) on a stone plinth
    const O = OVEN;
    g.beginPath(); g.rect(O.x - O.rx - 12, O.y, O.rx * 2 + 24, 26); inkShape(g, F('#a79a86'), 2);
    if (colour) { g.strokeStyle = 'rgba(40,30,20,0.5)'; g.lineWidth = 1; for (let x = O.x - O.rx; x < O.x + O.rx; x += 34) { g.beginPath(); g.moveTo(x, O.y); g.lineTo(x, O.y + 26); g.stroke(); } }
    g.beginPath(); g.ellipse(O.x, O.y, O.rx, O.ry, 0, Math.PI, TAU); g.closePath();
    const og = g.createRadialGradient(O.x - 50, O.y - 90, 10, O.x, O.y - 40, O.rx * 1.2); og.addColorStop(0, '#e79a6c'); og.addColorStop(0.6, '#bd5f3c'); og.addColorStop(1, '#86381f');
    inkShape(g, F(og), 2.4);
    g.save(); g.beginPath(); g.ellipse(O.x, O.y, O.rx, O.ry, 0, Math.PI, TAU); g.closePath(); g.clip();
    g.strokeStyle = colour ? 'rgba(70,25,10,0.55)' : 'rgba(42,27,18,0.5)'; g.lineWidth = 1.3;
    for (let k = 1; k < 7; k++) { const f = k / 7; g.beginPath(); g.ellipse(O.x, O.y, O.rx * (1 - f * 0.08), O.ry * (1 - f) + 2, 0, Math.PI, TAU); g.stroke(); }
    for (let k = 0; k < 7; k++) { const n = 12 - k; for (let i = 0; i < n; i++) { const a = Math.PI + (i + (k % 2) * 0.5) / n * Math.PI, f0 = k / 7, f1 = (k + 1) / 7;
      g.beginPath(); g.moveTo(O.x + Math.cos(a) * O.rx * (1 - f0 * 0.08), O.y + Math.sin(a) * (O.ry * (1 - f0) + 2)); g.lineTo(O.x + Math.cos(a) * O.rx * (1 - f1 * 0.08), O.y + Math.sin(a) * (O.ry * (1 - f1) + 2)); g.stroke(); } }
    if (colour) { g.strokeStyle = 'rgba(255,230,200,0.5)'; g.lineWidth = 5; g.beginPath(); g.ellipse(O.x - 10, O.y, O.rx - 22, O.ry - 22, 0, Math.PI + 0.35, Math.PI + 1.25); g.stroke(); }
    g.restore();
    // vent
    g.beginPath(); g.rect(O.x - 14, O.y - O.ry - 16, 28, 20); inkShape(g, F('#8d7f6c'), 2);
    // mouth
    g.beginPath(); g.moveTo(O.x - O.mw, O.y); g.lineTo(O.x - O.mw, O.y - O.mh + O.mw); g.arc(O.x, O.y - O.mh + O.mw, O.mw, Math.PI, TAU); g.lineTo(O.x + O.mw, O.y); g.closePath();
    inkShape(g, F('#2a110a'), 2.6);
    g.beginPath(); g.moveTo(O.x - O.mw - 8, O.y); g.lineTo(O.x - O.mw - 8, O.y - O.mh + O.mw); g.arc(O.x, O.y - O.mh + O.mw, O.mw + 8, Math.PI, TAU); g.lineTo(O.x + O.mw + 8, O.y);
    g.strokeStyle = colour ? '#e8d6b4' : COL.ink; g.lineWidth = colour ? 5 : 1.4; g.stroke();
    // peel leaning on the dome
    g.save(); g.translate(540, 330); g.rotate(-0.33);
    g.beginPath(); g.rect(-5, -170, 10, 170); inkShape(g, F('#a8773f'), 1.8);
    g.beginPath(); g.moveTo(-22, -170); g.lineTo(22, -170); g.quadraticCurveTo(26, -228, 0, -232); g.quadraticCurveTo(-26, -228, -22, -170); g.closePath(); inkShape(g, F('#c28b4c'), 1.8);
    g.restore();
    // trestle table with loaves
    g.beginPath(); g.moveTo(66, 256); g.lineTo(80, 330); g.moveTo(100, 256); g.lineTo(86, 330); g.moveTo(170, 256); g.lineTo(184, 330); g.moveTo(204, 256); g.lineTo(190, 330);
    g.strokeStyle = colour ? '#6b4526' : COL.ink; g.lineWidth = colour ? 6 : 2; g.stroke(); if (colour) { g.strokeStyle = COL.ink; g.lineWidth = 1.2; g.stroke(); }
    g.beginPath(); g.rect(48, 244, 176, 14); inkShape(g, F('#a8773f'), 1.8);
    if (colour) { loaf(g, 84, 232, 0.72); loaf(g, 136, 230, 0.8); loaf(g, 188, 232, 0.72); }
    else for (const [lx, s] of [[84, 0.72], [136, 0.8], [188, 0.72]]) { g.save(); g.translate(lx, 232); g.scale(s, s); g.beginPath(); g.moveTo(-36, 10); g.quadraticCurveTo(-40, -18, 0, -22); g.quadraticCurveTo(40, -18, 36, 10); g.quadraticCurveTo(0, 16, -36, 10); g.strokeStyle = COL.ink; g.lineWidth = 2.4; g.stroke(); g.restore(); }
    // flour sack
    g.beginPath(); g.moveTo(10, 330); g.quadraticCurveTo(4, 280, 22, 262); g.lineTo(18, 250); g.lineTo(40, 246); g.lineTo(38, 260); g.quadraticCurveTo(58, 280, 50, 330); g.closePath(); inkShape(g, F('#e2d2ac'), 2);
    if (colour) { g.strokeStyle = COL.redD; g.lineWidth = 2.2; g.beginPath(); g.moveTo(18, 258); g.lineTo(40, 256); g.stroke(); }
    return c;
  };
  MINI_INK = build(false); MINI_COL = build(true);
}
// paint-in order: patches (x, y, radius, start) sweeping from the oven outward
const MINI_PATCH = (() => { const r = mulberry(33), out = []; for (let i = 0; i < 70; i++) { const x = r() * MIN.iw, y = r() * MIN.ih; const d = Math.hypot(x - OVEN.x, (y - OVEN.y + 60) * 1.3) / 520; out.push([x, y, 70 + r() * 60, clamp(d + (r() - 0.5) * 0.2)]); } return out; })();
let _mm; function miniature(g, t, T) {   // T: { ink:[a,b], gild:[a,b], col:[a,b], shine: phase }
  const x = MIN.x, y = MIN.y, w = MIN.w, h = MIN.h, ix = MIN.ix, iy = MIN.iy;
  const ui = seg(t, T.ink[0], T.ink[1]), uc = seg(t, T.col[0], T.col[1]), ug = seg(t, T.gild[0], T.gild[1]);
  if (ui <= 0) return;
  // gold frame + coloured band
  const frame = gg => { gg.beginPath(); gg.rect(x, y, w, h); gg.rect(x + MIN.fr, y + MIN.fr, w - 2 * MIN.fr, h - 2 * MIN.fr); };
  if (ug > 0) {
    g.save(); g.beginPath(); g.rect(x, y, w, h); g.rect(x + MIN.fr, y + MIN.fr, w - 2 * MIN.fr, h - 2 * MIN.fr); g.clip('evenodd');
    gold(g, gg => { gg.beginPath(); gg.rect(x, y, w, h); }, [x, y, w, h], ug, T.shine, 5); g.restore();
    g.save(); g.beginPath(); g.rect(x + MIN.fr, y + MIN.fr, w - 2 * MIN.fr, h - 2 * MIN.fr); g.rect(ix, iy, MIN.iw, MIN.ih); g.fillStyle = COL.rose; g.globalAlpha = clamp(ug * 2); g.fill('evenodd'); g.restore();
    g.fillStyle = 'rgba(255,248,235,0.9)'; const n = 60; for (let i = 0; i < n; i++) { const u = i / n, P = u * 2 * (w + h - 4 * MIN.fr); let px, py; const a1 = w - 2 * MIN.fr, b1 = h - 2 * MIN.fr, o = MIN.fr + MIN.band / 2;
      if (P < a1) { px = x + MIN.fr + P; py = y + o; } else if (P < a1 + b1) { px = x + w - o; py = y + MIN.fr + P - a1; } else if (P < 2 * a1 + b1) { px = x + w - MIN.fr - (P - a1 - b1); py = y + h - o; } else { px = x + o; py = y + h - MIN.fr - (P - 2 * a1 - b1); }
      if (ug > u) { g.beginPath(); g.arc(px, py, 1.8, 0, TAU); g.fill(); } }
  }
  g.strokeStyle = COL.ink; g.lineWidth = 1.6; g.globalAlpha = ui; g.strokeRect(x, y, w, h); g.globalAlpha = 1; g.strokeRect(x + MIN.fr, y + MIN.fr, w - 2 * MIN.fr, h - 2 * MIN.fr);
  // underdrawing: wipe down from the top
  g.save(); g.beginPath(); g.rect(ix, iy, MIN.iw, MIN.ih * eInOut(ui)); g.clip(); g.drawImage(MINI_INK, ix, iy); g.restore();
  // colour in soft patches
  if (uc > 0) {
    _mm = _mm || mk(MIN.iw, MIN.ih); const m = _mm.getContext('2d'); m.globalCompositeOperation = 'source-over'; m.clearRect(0, 0, MIN.iw, MIN.ih);
    if (uc >= 1) m.drawImage(MINI_COL, 0, 0);
    else {
      m.fillStyle = '#000';
      for (const [px, py, pr, s0] of MINI_PATCH) { const u = clamp((uc - s0 * 0.7) / 0.3); if (u > 0) { m.beginPath(); m.arc(px, py, pr * eOut(u), 0, TAU); m.fill(); } }
      m.globalCompositeOperation = 'source-in'; m.drawImage(MINI_COL, 0, 0); m.globalCompositeOperation = 'source-over';
    }
    g.drawImage(_mm, ix, iy);
  }
  // live fire in the mouth and smoke from the vent
  const fire = seg(t, T.col[0] + 0.25, T.col[0] + 0.7);
  if (fire > 0) {
    const O = OVEN, ox = ix + O.x, oy = iy + O.y;
    g.save(); g.beginPath(); g.moveTo(ox - O.mw + 3, oy); g.lineTo(ox - O.mw + 3, oy - O.mh + O.mw); g.arc(ox, oy - O.mh + O.mw, O.mw - 3, Math.PI, TAU); g.lineTo(ox + O.mw - 3, oy); g.closePath(); g.clip();
    const tq = Math.floor(t * 12) / 12;   // flicker on twos, like hand-painted cels
    for (let i = 0; i < 6; i++) {
      const fx = ox - 36 + i * 14.5, hgt = (34 + 22 * Math.sin(tq * 9 + i * 2.1) + 10 * Math.sin(tq * 17 + i)) * fire, wd = 11 + (i % 2) * 3;
      for (const [c, k] of [['#c8321e', 1], ['#f08a24', 0.72], ['#fbd65a', 0.42]]) {
        g.fillStyle = c; g.beginPath(); g.moveTo(fx - wd * k, oy); g.quadraticCurveTo(fx - wd * k * 0.9, oy - hgt * k * 0.6, fx + Math.sin(tq * 11 + i) * 4, oy - hgt * k); g.quadraticCurveTo(fx + wd * k * 0.9, oy - hgt * k * 0.6, fx + wd * k, oy); g.fill();
      }
    }
    g.fillStyle = '#6e3a1a'; for (let i = 0; i < 3; i++) { g.save(); g.translate(ox - 22 + i * 22, oy - 4); g.rotate(0.3 - i * 0.3); g.fillRect(-18, -3, 36, 6); g.restore(); }
    g.restore();
    // smoke: a stylised curl rising from the vent
    g.save(); g.beginPath(); g.rect(ix, iy, MIN.iw, MIN.ih); g.clip();
    for (let k = 0; k < 4; k++) {
      const ph = (t * 0.45 + k / 4) % 1, sx = ox + Math.sin(ph * 5 + k) * 14 + ph * 26, sy = oy - O.ry - 20 - ph * 150, rad = 9 + ph * 16;
      g.strokeStyle = `rgba(250,244,232,${0.85 * Math.sin(Math.PI * ph) * fire})`; g.lineWidth = 3.5;
      g.beginPath(); for (let a = 0; a < TAU * 1.3; a += 0.2) { const rr2 = rad * (1 - a / (TAU * 1.6)); g.lineTo(sx + Math.cos(a + ph * 4) * rr2, sy + Math.sin(a + ph * 4) * rr2 * 0.8); } g.stroke();
    }
    g.restore();
  }
  // miniature shine across the whole painting once finished
  if (T.shine >= 0 && T.shine <= 1) {
    g.save(); g.beginPath(); g.rect(ix, iy, MIN.iw, MIN.ih); g.clip(); const cx = lerp(ix - 200, ix + MIN.iw + 200, T.shine);
    const sg = g.createLinearGradient(cx - 90, iy, cx + 90, iy + 120); sg.addColorStop(0, 'rgba(255,250,230,0)'); sg.addColorStop(0.5, 'rgba(255,250,230,0.10)'); sg.addColorStop(1, 'rgba(255,250,230,0)');
    g.fillStyle = sg; g.fillRect(ix, iy, MIN.iw, MIN.ih); g.restore();
  }
}
