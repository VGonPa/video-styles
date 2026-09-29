// Point-and-Click Adventure: timeline, per-frame drawing, audio events (loaded by anim.html)
const T = {
  irisIn: [0, 0.45], walkE: [0, 1.0], xE: [184, 238], doorOpen: [0.55, 0.78], cut1: 1.15,
  walk1: [1.15, 2.0], x1: [30, 92], say1: [2.0, 2.95], say2: [2.95, 3.95],
  step2: [3.95, 4.12], x2: [92, 99], reach: [4.12, 4.3], grab: 4.3, retract: [4.3, 4.48], fly: [4.32, 4.78],
  say3: [4.8, 5.95], walk3: [4.95, 5.6], x3: [99, 138],
  pullUp: [5.62, 5.78], pullDown: [5.78, 5.95], release: [6.05, 6.25], slide: [5.98, 6.5],
  say4: [6.38, 7.1], walk4: [6.4, 7.2], x4: [138, 194], parrotTurn: 6.8,
  irisOut1: [7.02, 7.42], beach: 7.45, irisIn2: [7.45, 7.85],
  walk5: [7.55, 8.4], x5: [38, 96], lift: [8.35, 8.55], say5: [8.55, 9.9], irisOut2: [9.5, 9.92]
};
const CUR = [[0.10, 296, 30], [0.36, 238, 100], [1.15, 238, 100], [1.5, 210, 80], [1.78, 284, 74], [2.4, 284, 74], [2.8, 236, 58], [3.45, 226, 62],
  [3.78, 114, 96], [4.3, 114, 96], [4.62, 158, 90], [5.2, 158, 90], [5.6, 176, 64], [6.05, 182, 68], [6.3, 208, 100], [7.45, 208, 100],
  [7.7, 180, 60], [8.12, SLOT(3)[0], SLOT(3)[1] + 148], [8.5, SLOT(3)[0], SLOT(3)[1] + 148], [8.95, 178, 116], [9.6, 184, 112]];
const CLICKS = [0.4, 1.86, 3.84, 4.7, 6.34, 8.2];
const LABELS = [[0.34, 1.0, 'door'], [1.76, 2.45, 'parrot'], [3.76, 4.35, 'a suspiciously damp map'], [4.78, 5.3, 'stuffed fish'], [6.28, 6.95, 'secret passage'], [8.1, 8.6, 'a suspiciously damp map']];
const FISH = { x: 161, y: 92 };

let BG_EXT, BG_INT, BG_BEACH, STRIP, PANEL, ICONS;
function buildPanel() {  // the bookshelf that is secretly a door
  const P = new Paint(40, 62), r = rng(77), books = [];
  P.rect(0, 0, 40, 62, 'wood', (x, y) => (x < 2 || x > 37 || y < 2) ? 4.6 + (x === 0 || y === 0 ? 2 : 0) : 1.4);
  for (const sy of [19, 39, 59]) P.rect(0, sy, 40, 3, 'wood', (x, y) => y === sy ? 6.4 : 3.2);
  for (const sy of [19, 39, 59]) { let x = 3; while (x < 36) { const w = 3 + F(r() * 3), h = 10 + F(r() * 6), rp = ['red', 'green', 'sea', 'glow', 'plaster', 'red'][F(r() * 6)];
    if (r() < 0.12) { x += 3; continue; } const lean = r() < 0.15 && x < 30;
    for (let y = sy - h; y < sy; y++) for (let i = 0; i < w; i++) { const X = x + i + (lean ? F((sy - y) / 5) : 0); if (X > 36) continue; P.set(X, y, rp, (rp === 'glow' ? 2.4 : 3) + (i === 0 ? 1.6 : 0) + (i === w - 1 ? -1 : 0) + ((y === sy - h + 2) ? 1.8 : 0)); }
    x += w + (lean ? 2 : 0); } }
  P.light(20, 10, 40, 1.2); return P.canvas();
}

// ── helpers ──
const walkX = (t, [a, b], [x0, x1]) => lerp(x0, x1, seg(t, a, b));
const walkPh = (x, x0) => F(((Math.abs(x - x0) / 34) % 1) * 8) / 8;
function curAt(t) { let i = 0; while (i < CUR.length - 1 && CUR[i + 1][0] <= t) i++; if (i >= CUR.length - 1) return CUR[CUR.length - 1].slice(1);
  const [t0, x0, y0] = CUR[i], [t1, x1, y1] = CUR[i + 1], f = eio(seg(t, t0, t1)); return [lerp(x0, x1, f), lerp(y0, y1, f)]; }
const labelAt = t => { for (const [a, b, s] of LABELS) if (t >= a && t < b) return s; return null; };
function iris(cx, cy, r) {
  V.fillStyle = '#000'; r = F(r / 3) * 3;
  for (let y = 0; y < SH; y++) { const dy = y + 0.5 - cy; if (r <= 0 || Math.abs(dy) >= r) { V.fillRect(0, y, VW, 1); continue; } const dx = R(Math.sqrt(r * r - dy * dy));
    V.fillRect(0, y, Math.max(0, R(cx) - dx), 1); V.fillRect(R(cx) + dx, y, VW, 1); }
}
function drawCursor(x, y, hot, click, t) {
  x = R(x); y = R(y); const g = click ? 1 : 2, L = 4, c = hot ? (F(t * 10) % 2 ? '#fcfc80' : '#fcfcfc') : '#fcfcfc';
  const arms = [[x - g - L, y, L, 1], [x + g + 1, y, L, 1], [x, y - g - L, 1, L], [x, y + g + 1, 1, L]];
  V.fillStyle = '#0a0610'; for (const [a, b, w, h] of arms) V.fillRect(a - 1, b - 1, w + 2, h + 2);
  V.fillStyle = c; for (const [a, b, w, h] of arms) V.fillRect(a, b, w, h); if (click) fill(x, y, 1, 1, c);
}
function flame(x, y, t, s, big) {  // flickering flame, colour-cycled per 1/12 s
  const k = F(t * 12), h = hash(k, s, 9); const cs = ['#fff8dc', '#fcd670', '#f09c2e', '#bc5a14'];
  if (big) { fill(x - 1, y + 1, 4, 4, cs[2]); fill(x, y + (h > 0.5 ? 0 : 1), 2, 4, cs[1]); fill(x, y + 3, 2, 1, cs[0]); if (h > 0.7) fill(x + 1, y - 1, 1, 1, cs[1]); }
  else { fill(x, y + 1, 2, 3, cs[2]); fill(x, y + (h > 0.5 ? 0 : 1), 1 + (h > 0.3 ? 1 : 0), 2, cs[1]); fill(x, y + 3, 1, 1, cs[0]); }
}
function drawFish(phi) {
  const cs = Math.cos(phi), sn = Math.sin(phi), px = FISH.x, py = FISH.y, cell = [];
  for (let dy = -14; dy <= 14; dy++) for (let dx = -18; dx <= 18; dx++) { const u = dx * cs + dy * sn, w = -dx * sn + dy * cs; let c = null;
    const hw = 4.8 * Math.sqrt(Math.max(0, 1 - (u / 12.2) ** 2));
    if (Math.abs(u) <= 12 && Math.abs(w) <= hw) c = w < -1.6 ? '#4a6a5a' : w > 1.8 ? '#dcdcc4' : '#8eac9c';
    else if (u > 10 && u < 16 && Math.abs(w) <= (u - 9.5) * 1.05) c = '#4a6a5a';
    else if (u > -4 && u < 4 && w < -3.5 && w > -6.8 + (u + 4) * 0.35) c = '#5e7e6c';
    if (c && Math.abs(u + 6.2) < 0.55 && Math.abs(w) < hw - 0.5) c = '#3a5446';
    if (c && Math.hypot(u + 8.4, w + 1.2) < 1.3) c = '#f4f0e0'; if (c && Math.hypot(u + 8.6, w + 1.2) < 0.7) c = '#101010';
    if (c && Math.abs(u + 11.4) < 1 && Math.abs(w - 1) < 0.7) c = '#2a2020';
    if (c) cell.push([px + dx, py + dy, c]); }
  const occ = new Set(cell.map(([x, y]) => x + ',' + y)); V.fillStyle = '#140a10';
  for (const [x, y] of cell) for (const [a, b] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) if (!occ.has((x + a) + ',' + (y + b))) V.fillRect(x + a, y + b, 1, 1);
  for (const [x, y, c] of cell) fill(x, y, 1, 1, c); fill(px, py, 1, 1, '#f8d470');
}
const fishPhi = t => t < T.pullDown[0] ? 0 : -0.5 * eob(seg(t, T.pullDown[0], T.pullDown[1]));
const fishHead = phi => [FISH.x - 10 * Math.cos(phi), FISH.y - 10 * Math.sin(phi) + 1];

// ── the hero's performance per scene ──
function heroInt(t) {
  const y = 140; let x = T.x1[0], pose;
  if (t < T.walk1[1]) { x = walkX(t, T.walk1, T.x1); pose = walkPose(walkPh(x, T.x1[0])); }
  else if (t < T.step2[0]) { x = T.x1[1]; pose = standPose(); if (t >= T.say1[0] && t < T.say1[1]) { const k = F(t * 7) % 2; pose.talk = k; pose.an = k ? { s: 0.55, f: 1.75 } : { s: 0.4, f: 1.35 }; } }
  else if (t < T.step2[1]) { x = walkX(t, T.step2, T.x2); pose = walkPose(walkPh(x, T.x2[0]) * 0.5); }
  else if (t < T.walk3[0]) { x = T.x2[1]; pose = standPose(); const shx = x, shy = y - 33 - 1, rest = [x + 2, y - 18];
    let f = t < T.grab ? eio(seg(t, T.reach[0], T.reach[1])) : 1 - eio(seg(t, T.retract[0], T.retract[1]));
    if (f > 0) { const tg = [lerp(rest[0], 112, f), lerp(rest[1], 98, f)]; pose.an = ik(shx, shy, tg[0], tg[1], A_UP, A_LO + 1.5); pose.lean = R(f); } }
  else if (t < T.walk3[1]) { x = walkX(t, T.walk3, T.x3); pose = walkPose(walkPh(x, T.x3[0])); }
  else if (t < T.walk4[0]) { x = T.x3[1]; pose = standPose(); const shx = x, shy = y - 34, rest = [x + 2, y - 18], head = fishHead(fishPhi(t));
    let tg = rest; if (t < T.pullUp[1]) { const f = eio(seg(t, T.pullUp[0], T.pullUp[1])); tg = [lerp(rest[0], head[0], f), lerp(rest[1], head[1], f)]; }
    else if (t < T.release[0]) tg = head; else { const f = eio(seg(t, T.release[0], T.release[1])); tg = [lerp(head[0], rest[0], f), lerp(head[1], rest[1], f)]; }
    pose.an = ik(shx, shy, tg[0], tg[1], A_UP, A_LO + 1.5); if (t > T.pullDown[0] && t < T.release[0]) pose.lean = 1; }
  else { x = walkX(t, T.walk4, T.x4); pose = walkPose(walkPh(x, T.x4[0])); }
  const dark = clamp((x - 176) / 18) * 0.6;
  return { x, y, pose, pal: dark > 0 ? tintPal(PAL_INT, '#06060e', dark) : PAL_INT };
}
function heroBeach(t) {
  const y = 138; let x, pose;
  if (t < T.walk5[1]) { x = walkX(t, T.walk5, T.x5); pose = walkPose(walkPh(x, T.x5[0])); }
  else { x = T.x5[1]; pose = standPose(); const f = eio(seg(t, T.lift[0], T.lift[1]));
    pose.an = { s: lerp(0.08, 0.5, f), f: lerp(0.28, 2.0, f) }; pose.af = { s: lerp(-0.05, 0.6, f), f: lerp(0.2, 2.1, f) }; pose.hd = f > 0.5 ? 1 : 0;
    if (t >= T.say5[0]) pose.talk = F(t * 7) % 2 && t < T.say5[0] + 1.0; }
  const dark = clamp((54 - x) / 16) * 0.55;
  return { x, y, pose, pal: dark > 0 ? tintPal(PAL_BEACH, '#6e2a0a', dark) : PAL_BEACH };
}

// ── scenes ──
function sceneExt(t) {
  V.drawImage(BG_EXT, 0, 0);
  for (const g of EXT_GLINTS) { const ph = (t * 2.4 + g.p) % 3; if (ph < 1) fill(g.x, g.y, g.l, 1, col('sky', 8)); else if (ph < 1.6) fill(g.x + 1, g.y, g.l - 1, 1, col('sea', 7)); }
  V.drawImage(textImg('THE DAMP ANCHOR', COL.sign, 1), 240 - R(textImg('THE DAMP ANCHOR', COL.sign, 1).tw / 2) - 1, 44);
  // lantern
  fill(263, 73, 5, 1, '#1c1c2a'); fill(261, 74, 9, 1, '#272738'); fill(261, 75, 9, 9, '#1c1c2a'); fill(262, 75, 7, 8, col('glow', 6 + (hash(F(t * 12), 1, 4) > 0.5 ? 1 : 0))); fill(261, 84, 9, 1, '#272738'); flame(264, 77, t, 2, true);
  // door (hinged left, swings inward)
  const o = eio(seg(t, T.doorOpen[0], T.doorOpen[1])), w = Math.max(3, R(26 * (1 - o)));
  for (let x = 0; x < w; x++) for (let y = 83; y < 124; y++) { const px = x * 26 / w; let c = (F(px) % 6 === 0) ? '#281308' : '#4a2414'; if (o > 0) c = mixHex(c, '#120605', o * 0.6);
    if ((y === 88 || y === 118) && px < 14) c = '#434358'; if (F(px) === 21 && y >= 102 && y <= 104 && o < 0.3) c = '#d8a238'; fill(225 + x, y, 1, 1, c); }
  const x = walkX(t, T.walkE, T.xE), pose = t < T.walkE[1] ? walkPose(walkPh(x, T.xE[0])) : standPose();
  drawHero(pose, x, 128, PAL_EXT);
}
function sceneInt(t) {
  const sh = t >= T.slide[0] && t < T.slide[1] + 0.06 ? (F(t * 24) % 2 ? 1 : -1) : 0;
  V.save(); V.translate(sh, 0);
  V.drawImage(BG_INT, 0, 0);
  V.drawImage(textImg('SOUP:', '#d0d4dc', 1), 104, 45); V.drawImage(textImg('damp', '#d0d4dc', 1), 105, 53);
  flame(149, 23, t, 3, true); flame(255, 83, t, 4, false);
  // secret panel sliding up into the wall, dust
  const so = t < T.slide[0] ? 0 : R(64 * eio(seg(t, T.slide[0], T.slide[1])) + (t < T.slide[1] ? (F(t * 20) % 2) : 0));
  V.save(); V.beginPath(); V.rect(188, 62, 40, 62); V.clip(); if (so < 62) V.drawImage(PANEL, 188, 62 - so); V.restore();
  if (t >= T.slide[0]) for (let i = 0; i < 16; i++) { const t0 = T.slide[0] + hash(i, 1, 5) * 0.6, u = t - t0; if (u < 0 || u > 0.8) continue;
    fill(189 + hash(i, 2, 5) * 38, 62 + u * u * 120 + u * 6, 1, 1, u < 0.4 ? '#9e9eb2' : '#6a6a80'); }
  // puddle, map + drips
  fill(123, 124, 7, 1, '#2a5888'); fill(125, 125, 4, 1, '#1f4474');
  if (t < T.grab) { fill(108, 96, 11, 4, '#d8c68a'); fill(108, 96, 11, 1, '#f0e2aa'); fill(113, 96, 1, 4, '#b09c60'); fill(109, 98, 3, 2, '#6a8ab0'); fill(107, 99, 1, 1, '#6a8ab0'); }
  for (let k = 0; k < 2; k++) { const u = (t * 1.3 + k * 0.5) % 1; if (t < T.grab || u > 0.9) fill(126 + k, 100 + R(u * u * 24), 1, 1 + (u > 0.5 ? 1 : 0), '#86b0cc'); }
  drawFish(fishPhi(t));
  // parrot
  const talking = [T.say2, T.say3, T.say4].some(([a, b]) => t >= a && t < b), open = talking && F(t * 9) % 2 === 0;
  const blink = [1.6, 3.55, 5.35, 7.05].some(b => t >= b && t < b + 0.1), flip = t >= T.parrotTurn;
  V.drawImage(parrotCanvas(open, open ? 1 : 0, blink, flip), 269, 84 - 24);
  // hero
  const h = heroInt(t);
  if (h.x > 180) { V.save(); V.beginPath(); V.rect(0, 0, 228, SH); V.clip(); drawHero(h.pose, h.x, h.y, h.pal); V.restore(); }
  else drawHero(h.pose, h.x, h.y, h.pal);
  V.restore();
  // speech
  if (t >= T.say1[0] && t < T.say1[1]) say(['I seek treasure.'], h.x, 84, COL.hero);
  if (t >= T.say2[0] && t < T.say2[1]) say(['Take a number.'], 262, 56, COL.parrot);
  if (t >= T.say3[0] && t < T.say3[1]) say(['Don\'t pull', 'the fish.'], 262, 56, COL.parrot);
  if (t >= T.say4[0] && t < T.say4[1]) say(['Nobody listens.'], 256, 56, COL.parrot);
}
function sceneBeach(t) {
  V.drawImage(BG_BEACH, 0, 0);
  for (const s of STARS) { const b = Math.sin(t * 4 + s.p * 3); if (b > 0.3) fill(s.x, s.y, 1, 1, '#fbfdff'); if (b > 0.85) { fill(s.x - 1, s.y, 3, 1, '#a8c0e0'); fill(s.x, s.y - 1, 1, 3, '#a8c0e0'); fill(s.x, s.y, 1, 1, '#fbfdff'); } }
  for (let y = 86; y < 112; y += 2) { const w = 3 + (y - 84) * 0.5, x0 = 238 + 2 * Math.sin(t * 3 + y * 0.7) - w / 2 + (((F(t * 6) + y) % 3) - 1), c = col('moon', (y + F(t * 8)) % 3 + 1);
    if (y >= shoreY(R(x0)) - 1) continue; fill(x0, y, R(w * 0.45), 1, c); fill(x0 + R(w * 0.6), y, R(w * 0.4), 1, c); }
  const s = 2.2 * Math.sin(t * 1.9) - 1;
  for (let x = 74; x < VW; x++) { const y = shoreY(x) + R(s + 0.8 * Math.sin(x / 9 + t * 2)); if (hash(x, F(t * 10), 3) > 0.28) fill(x, y, 1, 1, '#c8d8f0'); if (hash(x, F(t * 10), 4) > 0.55) fill(x, y - 2, 1, 1, '#5a8cb4'); }
  const h = heroBeach(t), c = drawHero(h.pose, h.x, h.y, h.pal);
  if (t >= T.lift[0] + 0.1) { const hx = R(h.x - GOX + c.hand[0] + GOX), hy = R(h.y - GOY + c.hand[1] + GOY);
    const pc = mixHex('#d8c68a', '#3a5aa8', 0.35), pd = mixHex('#b09c60', '#3a5aa8', 0.35);
    fill(hx - 3, hy - 11, 15, 12, '#140a10'); fill(hx - 2, hy - 10, 13, 10, pc); fill(hx - 2, hy - 10, 13, 1, mixHex('#f0e2aa', '#3a5aa8', 0.3)); fill(hx + 4, hy - 10, 1, 10, pd);
    fill(hx + 7, hy - 6, 1, 1, '#c83632'); fill(hx + 9, hy - 6, 1, 1, '#c83632'); fill(hx + 8, hy - 5, 1, 1, '#c83632'); fill(hx + 7, hy - 4, 1, 1, '#c83632'); fill(hx + 9, hy - 4, 1, 1, '#c83632');
    fill(hx, hy - 1, 2, 2, mixHex('#eaa878', '#3a5aa8', 0.42)); }
  if (t >= T.say5[0]) say(['It just says:', 'YOU ARE HERE.'], h.x + 4, 84, COL.hero);
}

function render(t) {
  V.fillStyle = '#000'; V.fillRect(0, 0, VW, VH);
  // scene
  V.save(); V.beginPath(); V.rect(0, 0, VW, SH); V.clip();
  if (t < T.cut1) { sceneExt(t); iris(232, 104, 300 * (1 - Math.pow(1 - seg(t, T.irisIn[0], T.irisIn[1]), 2))); }
  else if (t < T.beach) { sceneInt(t); if (t >= T.irisOut1[0]) iris(206, 104, 230 * Math.pow(1 - seg(t, T.irisOut1[0], T.irisOut1[1]), 1.6)); }
  else { sceneBeach(t); if (t < T.irisIn2[1]) iris(40, 112, 340 * (1 - Math.pow(1 - seg(t, T.irisIn2[0], T.irisIn2[1]), 2)));
    if (t >= T.irisOut2[0]) { const h = heroBeach(t); iris(h.x + 2, 108, 240 * Math.pow(1 - seg(t, T.irisOut2[0], T.irisOut2[1]), 1.5)); } }
  V.restore();
  // inventory strip
  V.drawImage(STRIP, 0, SH);
  ['spoon', 'sock', 'card'].forEach((k, i) => { const [x, y] = SLOT(i); V.drawImage(ICONS[k], x - 13, SH + y - 11); });
  if (t >= T.fly[1]) { const u = t - T.fly[1], [x, y] = SLOT(3), b = u < 0.25 ? R(-3 * Math.sin(u / 0.25 * Math.PI)) : 0; V.drawImage(ICONS.map, x - 13, SH + y - 11 + b); }
  const flash = (t >= T.fly[1] && t < T.fly[1] + 0.3) || (t >= 8.2 && t < 8.7);
  if (flash && F(t * 12) % 2 === 0) { const x0 = 14 + 3 * 37; V.strokeStyle = COL.label; V.lineWidth = 1; V.strokeRect(x0 + 0.5, SH + 19.5, 32, 29); }
  const lb = labelAt(t); if (lb) { const im = textImg(lb, COL.label); V.drawImage(im, R(160 - im.tw / 2), SH + 2); }
  // the map flying from the barrel into the inventory
  if (t >= T.fly[0] && t < T.fly[1]) { const f = seg(t, T.fly[0], T.fly[1]), e = eio(f), [sx, sy] = SLOT(3), x = lerp(113, sx, e), y = lerp(97, sy + SH, e) - Math.sin(f * Math.PI) * 34;
    V.drawImage(ICONS.map, R(x - 13), R(y - 11)); }
  // cursor
  if (t >= CUR[0][0] && t < 9.52) { const [cx, cy] = curAt(t), click = CLICKS.some(c => t >= c && t < c + 0.1); drawCursor(cx, cy, !!lb, click, t); }
  // palette-step fades of the whole screen (start and end)
  let lv = 0; if (t < 0.32) lv = 4 - F(t / 0.08); if (t >= 9.62) lv = Math.min(4, 1 + F((t - 9.62) / 0.07));
  if (lv > 0) { V.fillStyle = `rgba(0,0,0,${lv / 4})`; V.fillRect(0, SH, VW, VH - SH); if (lv >= 4) V.fillRect(0, 0, VW, VH); }
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H); ctx.imageSmoothingEnabled = false; ctx.drawImage(VC, OX, OY, VW * SC, VH * SC);
}

window.ready = (async () => {
  await document.fonts.load('8px Tiny5'); await document.fonts.ready;
  BG_EXT = buildExt(); BG_INT = buildInt(); BG_BEACH = buildBeach(); STRIP = buildStrip(); PANEL = buildPanel();
  ICONS = { spoon: itemIcon('spoon'), sock: itemIcon('sock'), card: itemIcon('card'), map: itemIcon('map') };
})();
window.draw = ({ t }) => { render(t); return cv.toDataURL('image/jpeg', 0.92).split(',')[1]; };
window.events = () => {
  const E = [];
  E.push({ k: 'amb', s: 'harbour', t: 0, e: T.cut1 }, { k: 'irisopen', t: 0.02 }, { k: 'door', t: T.doorOpen[0] }, { k: 'music', s: 'tavern', t: T.cut1, e: T.irisOut1[1] });
  CLICKS.forEach(t => E.push({ k: 'click', t }));
  // footsteps: every half walk cycle
  const walks = [[T.walkE, T.xE], [T.walk1, T.x1], [T.step2, T.x2], [T.walk3, T.x3], [T.walk4, T.x4], [T.walk5, T.x5]];
  for (const [tw, xw] of walks) { let last = -1; for (let t = tw[0]; t < tw[1]; t += 1 / 120) { const x = walkX(t, tw, xw), n = F(Math.abs(x - xw[0]) / 17); if (n !== last) { E.push({ k: 'step', t, s: tw === T.walk5 ? 'sand' : 'wood' }); last = n; } } }
  for (const s of [T.say2, T.say3, T.say4]) E.push({ k: 'squawk', t: s[0] });
  E.push({ k: 'pick', t: T.grab }, { k: 'inv', t: T.fly[1] }, { k: 'clunk', t: T.pullDown[0] + 0.1 }, { k: 'rumble', t: T.slide[0], e: T.slide[1] }, { k: 'thud', t: T.slide[1] });
  E.push({ k: 'iris', t: T.irisOut1[0] }, { k: 'irisopen', t: T.irisIn2[0] }, { k: 'amb', s: 'beach', t: T.beach, e: 10 }, { k: 'music', s: 'beach', t: 7.7, e: 10 });
  E.push({ k: 'paper', t: T.lift[0] }, { k: 'iris', t: T.irisOut2[0] });
  return E.sort((a, b) => a.t - b.t);
};
