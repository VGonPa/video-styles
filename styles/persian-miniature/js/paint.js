// paint.js · the painted layers of the miniature, baked once (sky, ground, court, pavilion, trees, plants, border)
const LAY = {};          // name → { c: canvas, bb: [x,y,w,h], dabs, t0, t1, dir }
const SITES = { bloss: [], roses: [] };   // dynamic blossoms (drawn per frame) and rose heads
const HZ = x => 300 + 14 * Math.sin(x * 0.0061 + 0.4) + 8 * Math.sin(x * 0.019 + 1.3) - 70 * Math.exp(-Math.pow((x - 230) / 150, 2)) - 26 * Math.exp(-Math.pow((x - 1230) / 110, 2));
const PATH = { y0: 836, y1: 928, x1: 1300 };   // foreground walk
const POOL = { x: 740, y: 548, w: 320, h: 136 }, JET = { x: 900, y: 616 };
const CHAN = { x: 886, w: 28, y0: 330, y1: 836 };
const PAV = { x: 1350, x1: 1742, top: 384, floor: 850, arch: { x: 1446, w: 188, top: 612, spring: 690 } };

function layer(name, bb, t0, t1, dir, fn, clip = clipP) {
  const c = mk(W, H), g = c.getContext('2d'); g.save(); clip(g); fn(g); g.restore();
  LAY[name] = { c, bb, t0, t1, dir, dabs: dabs(bb, t0, t1, dir, name.length * 31 + bb[0]) };
}
// brush dabs used to reveal a layer as if painted in, in a direction with some scatter
function dabs(bb, t0, t1, dir, seed) {
  const r = mulberry(seed), out = [], sp = 44; const [x, y, w, h] = bb;
  for (let yy = y - sp / 2; yy < y + h + sp; yy += sp) for (let xx = x - sp / 2; xx < x + w + sp; xx += sp) {
    const px = xx + (r() - 0.5) * sp * 0.9, py = yy + (r() - 0.5) * sp * 0.9;
    let o = dir === 'down' ? (py - y) / h : dir === 'up' ? 1 - (py - y) / h : dir === 'left' ? 1 - (px - x) / w : dir === 'out' ? Math.hypot((px - x - w / 2) / w, (py - y - h / 2) / h) * 1.4 : (px - x) / w;
    o = clamp(o); const ts = t0 + (t1 - t0 - 0.28) * (0.78 * o + 0.22 * r());
    out.push({ x: px, y: py, r: sp * (1.0 + r() * 0.5), ts, d: 0.2 + r() * 0.12, sq: 0.42 + r() * 0.22, a: (r() - 0.5) * 0.5 });
  }
  return out.sort((a, b) => a.ts - b.ts);
}

// ── sky: burnished gold with Chinese cloud bands ──
function paintSky(g) {
  const r = mulberry(21);
  const sg = g.createLinearGradient(0, P.y, 0, 330); sg.addColorStop(0, '#d9a53a'); sg.addColorStop(0.45, '#eec65e'); sg.addColorStop(1, '#d49c34');
  g.fillStyle = sg; g.fillRect(P.x, P.y, P.w, 320);
  // burnish: broad soft sheen + leaf seams + punched tooling dots
  for (let i = 0; i < 9; i++) { const x = P.x + r() * P.w, y = P.y + r() * 200, rad = 120 + r() * 200; const gr = g.createRadialGradient(x, y, 0, x, y, rad); gr.addColorStop(0, `rgba(255,246,200,${0.12 + r() * 0.12})`); gr.addColorStop(1, 'rgba(255,246,200,0)'); g.fillStyle = gr; g.fillRect(x - rad, y - rad, rad * 2, rad * 2); }
  for (let x = P.x + r() * 60; x < P.x + P.w; x += 70 + r() * 40) { g.fillStyle = 'rgba(150,100,30,0.10)'; g.fillRect(x, P.y, 1.2, 240); }
  for (let y = P.y + 50; y < 300; y += 64) { g.fillStyle = 'rgba(150,100,30,0.08)'; g.fillRect(P.x, y + r() * 20, P.w, 1.2); }
  for (let i = 0; i < 2200; i++) { g.fillStyle = r() < 0.5 ? `rgba(130,85,20,${0.10 + r() * 0.12})` : `rgba(255,250,215,${0.2 + r() * 0.2})`; g.beginPath(); g.arc(P.x + r() * P.w, P.y + r() * 240, 0.6 + r() * 0.8, 0, TAU); g.fill(); }
  const cloud = (x, y, s, flip) => {
    g.save(); g.translate(x, y); g.scale(s * (flip ? -1 : 1), s);
    g.beginPath(); g.moveTo(-120, 10);
    g.bezierCurveTo(-100, -20, -60, -24, -40, -6); g.bezierCurveTo(-30, -34, 10, -40, 24, -12); g.bezierCurveTo(40, -30, 80, -26, 86, 0);
    g.bezierCurveTo(110, -4, 130, 10, 118, 20); g.bezierCurveTo(100, 30, 60, 22, 40, 16); g.bezierCurveTo(10, 30, -30, 30, -50, 18); g.bezierCurveTo(-80, 30, -110, 26, -120, 10); g.closePath();
    g.fillStyle = COL.white; g.fill(); g.lineWidth = 2.4 / s; g.strokeStyle = COL.lapisL; g.stroke();
    g.lineWidth = 1.6 / s; g.strokeStyle = COL.lapis;
    for (const [cx, cy, rad] of [[-62, 4, 12], [4, -4, 14], [64, 4, 11]]) { g.beginPath(); for (let a = 0; a < 9; a += 0.2) g.lineTo(cx + Math.cos(a + 2) * rad * a / 9, cy + Math.sin(a + 2) * rad * a / 9); g.stroke(); }
    // trailing ribbon tail
    g.beginPath(); g.moveTo(118, 20); g.bezierCurveTo(150, 30, 170, 10, 196, 16); g.bezierCurveTo(174, 22, 156, 40, 116, 26); g.fillStyle = COL.white; g.fill(); g.stroke();
    g.restore();
  };
  cloud(440, 150, 0.8, false); cloud(1420, 138, 0.8, true); cloud(1640, 226, 0.6, false); cloud(260, 250, 0.5, true);
}

// ── ground: tilted green plane up to a high horizon, rocky outcrops, scattered tufts ──
function tuft(g, x, y, s, r) {
  g.strokeStyle = r() < 0.5 ? COL.emerD : COL.emer; g.lineWidth = 1.3;
  for (let k = -3; k <= 3; k++) { g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + k * 2 * s, y - 6 * s, x + k * 3.4 * s, y - (8 + (3 - Math.abs(k)) * 2.2) * s); g.stroke(); }
  const fl = r();
  if (fl < 0.3) { g.fillStyle = [COL.verm, COL.white, COL.lapisL, COL.ochre][Math.floor(r() * 4)]; for (let k = -1; k <= 1; k++) { g.beginPath(); g.arc(x + k * 5 * s, y - (12 + (k ? 0 : 3)) * s, 2.2 * s, 0, TAU); g.fill(); } }
}
function rocks(g, x, y, w, h, cols, seed) {
  const r = mulberry(seed);
  for (let i = 0; i < 14; i++) {
    const cx = x + r() * w, cy = y + h * (0.2 + r() * 0.8), rw = 26 + r() * 40, rh = 22 + r() * 30, c = cols[i % cols.length];
    g.beginPath(); const n = 9;
    for (let k = 0; k <= n; k++) { const a = Math.PI + k / n * Math.PI; const bump = 1 + 0.18 * Math.sin(k * 2.7 + i); g.lineTo(cx + Math.cos(a) * rw * bump, cy + Math.sin(a) * rh * bump); }
    g.closePath(); g.fillStyle = c; g.fill();
    g.save(); g.clip(); const sh = g.createLinearGradient(0, cy - rh, 0, cy); sh.addColorStop(0, 'rgba(255,255,255,0.25)'); sh.addColorStop(1, 'rgba(40,20,60,0.22)'); g.fillStyle = sh; g.fillRect(cx - rw * 1.3, cy - rh * 1.3, rw * 2.6, rh * 1.4);
    g.strokeStyle = 'rgba(40,25,50,0.35)'; g.lineWidth = 1; for (let q = 1; q <= 3; q++) { g.beginPath(); g.ellipse(cx + (r() - 0.5) * rw * 0.6, cy + 2, rw * (1 - q * 0.22), rh * (1 - q * 0.22), 0, Math.PI * 1.05, Math.PI * 1.95); g.stroke(); } g.restore();
    g.lineWidth = 1.6; g.strokeStyle = 'rgba(40,25,50,0.6)'; g.stroke();
    g.strokeStyle = 'rgba(255,255,255,0.45)'; g.lineWidth = 1.2; g.beginPath(); g.arc(cx - rw * 0.2, cy - rh * 0.3, rw * 0.35, Math.PI * 1.1, Math.PI * 1.7); g.stroke();
    g.strokeStyle = 'rgba(40,25,50,0.35)'; g.beginPath(); g.arc(cx + rw * 0.2, cy - rh * 0.1, rw * 0.3, Math.PI * 1.2, Math.PI * 1.9); g.stroke();
  }
}
function paintGround(g) {
  const r = mulberry(33);
  g.beginPath(); g.moveTo(P.x, P.y + P.h); for (let x = P.x; x <= P.x + P.w; x += 6) g.lineTo(x, HZ(x)); g.lineTo(P.x + P.w, P.y + P.h); g.closePath();
  const gr = g.createLinearGradient(0, 240, 0, P.y + P.h); gr.addColorStop(0, COL.groundL); gr.addColorStop(0.35, COL.ground); gr.addColorStop(1, COL.groundD);
  g.fillStyle = gr; g.fill();
  g.save(); g.clip();
  for (let i = 0; i < 2600; i++) { g.fillStyle = `rgba(${r() < 0.5 ? '30,80,40' : '200,235,160'},${0.05 + r() * 0.08})`; g.beginPath(); g.arc(P.x + r() * P.w, 220 + r() * 780, 1 + r() * 2.5, 0, TAU); g.fill(); }
  g.restore();
  g.lineWidth = 2.2; g.strokeStyle = COL.emerD; g.beginPath(); for (let x = P.x; x <= P.x + P.w; x += 6) g.lineTo(x, HZ(x)); g.stroke();
  rocks(g, P.x - 20, 190, 330, 90, [COL.lilac, COL.rose, COL.azure, COL.ochre], 4);
  rocks(g, 1160, 262, 170, 50, [COL.azure, COL.lilac, COL.pinkL], 8);
  // horizon shrubs
  for (let x = P.x + 8; x < P.x + P.w; x += 34 + r() * 30) { const y = HZ(x) + 3; g.fillStyle = r() < 0.5 ? COL.emer : COL.emerD; g.beginPath(); g.ellipse(x, y - 7, 11 + r() * 8, 9, 0, Math.PI, 0); g.fill(); }
  g.save(); g.beginPath(); for (let x = P.x; x <= P.x + P.w; x += 6) g.lineTo(x, HZ(x) + 4); g.lineTo(P.x + P.w, P.y + P.h); g.lineTo(P.x, P.y + P.h); g.closePath(); g.clip();
  g.lineWidth = 1; g.lineCap = 'round';
  for (let i = 0; i < 16000; i++) { const x = P.x + r() * P.w, y = 200 + r() * 800, l = 3 + r() * 4, a = -Math.PI / 2 + (r() - 0.5) * 0.9; g.strokeStyle = r() < 0.55 ? `rgba(30,90,45,${0.18 + r() * 0.2})` : `rgba(190,230,150,${0.16 + r() * 0.2})`; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke(); }
  g.restore();
  for (let i = 0; i < 330; i++) { const x = P.x + 10 + r() * (P.w - 20), y = 320 + r() * 660; if (y > HZ(x) + 16) tuft(g, x, y, 0.75 + r() * 0.5, r); }
}

// ── court: brick walk, pool, channels ──
function paintCourt(g) {
  const r = mulberry(44);
  // brick walk with herringbone
  const px0 = P.x, px1 = PATH.x1 + 40, y0 = PATH.y0, y1 = PATH.y1;
  g.fillStyle = COL.buff; g.fillRect(px0, y0, px1 - px0, y1 - y0);
  g.save(); g.beginPath(); g.rect(px0, y0 + 8, px1 - px0, y1 - y0 - 16); g.clip();
  g.strokeStyle = 'rgba(150,100,55,0.75)'; g.lineWidth = 1.3;
  for (let x = px0 - 100; x < px1 + 100; x += 26) for (let y = y0; y < y1 + 26; y += 26) {
    const o = ((x / 26) | 0) % 2 ? 13 : 0; g.beginPath(); g.moveTo(x, y + o); g.lineTo(x + 13, y + o + 13); g.lineTo(x + 26, y + o); g.stroke();
  }
  for (let i = 0; i < 300; i++) { g.fillStyle = `rgba(${r() < 0.5 ? '170,110,60' : '255,245,220'},${0.1 + r() * 0.15})`; g.fillRect(px0 + r() * (px1 - px0), y0 + r() * (y1 - y0), 4 + r() * 8, 2); }
  g.restore();
  for (const [y, c, lw] of [[y0 + 2, COL.verm, 3], [y0 + 7, COL.lapis, 2.5], [y1 - 7, COL.lapis, 2.5], [y1 - 2, COL.verm, 3]]) { g.strokeStyle = c; g.lineWidth = lw; g.beginPath(); g.moveTo(px0, y); g.lineTo(px1, y); g.stroke(); }
  // channel (up to the horizon, down to the walk)
  const water = (x, y, w, h, ang) => {
    g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip();
    g.fillStyle = COL.water; g.fillRect(x, y, w, h);
    g.strokeStyle = 'rgba(40,70,130,0.55)'; g.lineWidth = 1.4;
    if (ang) { for (let yy = y; yy < y + h + 10; yy += 9) { g.beginPath(); for (let xx = x; xx <= x + w; xx += 3) g.lineTo(xx, yy + Math.sin(xx * 0.5) * 2.2); g.stroke(); } }
    else for (let xx = x - 10; xx < x + w + 10; xx += 9) { g.beginPath(); for (let yy = y; yy <= y + h; yy += 3) g.lineTo(xx + Math.sin(yy * 0.35 + xx) * 2.2, yy); g.stroke(); }
    g.restore();
  };
  const stone = (x, y, w, h, b) => {
    g.fillStyle = COL.ivory; g.fillRect(x - b, y - b, w + 2 * b, h + 2 * b);
    g.strokeStyle = COL.lapis; g.lineWidth = 2; g.strokeRect(x - b + 3, y - b + 3, w + 2 * b - 6, h + 2 * b - 6);
    g.strokeStyle = COL.verm; g.lineWidth = 1.4; g.strokeRect(x - 2, y - 2, w + 4, h + 4);
    // little diamond border on the rim
    g.fillStyle = COL.turqD; const st = 16;
    for (let xx = x - b + 12; xx < x + w + b - 8; xx += st) for (const yy of [y - b / 2 - 1, y + h + b / 2 + 1]) { g.beginPath(); g.moveTo(xx, yy - 3.5); g.lineTo(xx + 3.5, yy); g.lineTo(xx, yy + 3.5); g.lineTo(xx - 3.5, yy); g.fill(); }
  };
  stone(CHAN.x, HZ(CHAN.x + 14) + 18, CHAN.w, POOL.y - HZ(CHAN.x + 14) - 18, 7); water(CHAN.x, HZ(CHAN.x + 14) + 18, CHAN.w, POOL.y - HZ(CHAN.x + 14) - 12, false);
  stone(CHAN.x, POOL.y + POOL.h, CHAN.w, PATH.y0 - POOL.y - POOL.h - 20, 7); water(CHAN.x, POOL.y + POOL.h - 4, CHAN.w, PATH.y0 - POOL.y - POOL.h - 16, false);
  stone(POOL.x, POOL.y, POOL.w, POOL.h, 14); water(POOL.x, POOL.y, POOL.w, POOL.h, true);
  // fountain basin: a lobed stone cup at the centre
  g.save(); g.translate(JET.x, JET.y);
  g.beginPath(); for (let k = 0; k <= 64; k++) { const a = k / 64 * TAU, rd = 26 + 4 * Math.cos(a * 8); g.lineTo(Math.cos(a) * rd, Math.sin(a) * rd * 0.62); } g.closePath();
  g.fillStyle = COL.ivory; g.fill(); g.strokeStyle = COL.inkS; g.lineWidth = 1.6; g.stroke();
  g.beginPath(); g.ellipse(0, 0, 16, 9, 0, 0, TAU); g.fillStyle = COL.azure; g.fill(); g.stroke();
  g.restore();
}

// ── pavilion: tiled kiosk with an iwan arch, upper talar, parapet and canopy ──
function hexTiles(g, x, y, w, h, s, c1, c2, line) {
  g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip(); g.fillStyle = c2; g.fillRect(x, y, w, h);
  const dy = s * Math.sqrt(3) / 2;
  for (let j = -1; j * dy < h + dy; j++) for (let i = -1; i * s * 1.5 < w + s; i++) {
    const cx = x + i * s * 1.5, cy = y + j * dy * 2 + (i % 2 ? dy : 0);
    g.beginPath(); for (let k = 0; k < 6; k++) { const a = k / 6 * TAU; g.lineTo(cx + Math.cos(a) * s * 0.86, cy + Math.sin(a) * s * 0.86); } g.closePath();
    g.fillStyle = c1; g.fill(); g.strokeStyle = line; g.lineWidth = 1.2; g.stroke();
    g.beginPath(); g.arc(cx, cy, s * 0.22, 0, TAU); g.fillStyle = line; g.fill();
  }
  g.restore();
}
function starLattice(g, x, y, w, h, s, bg, fg) {
  g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip(); g.fillStyle = bg; g.fillRect(x, y, w, h);
  g.strokeStyle = fg; g.lineWidth = 1.4;
  for (let j = -1; j * s < h + s; j++) for (let i = -1; i * s < w + s; i++) {
    const cx = x + i * s + (j % 2 ? s / 2 : 0), cy = y + j * s;
    g.beginPath(); for (let k = 0; k < 16; k++) { const a = k / 16 * TAU, d = k % 2 ? s * 0.18 : s * 0.4; g.lineTo(cx + Math.cos(a) * d, cy + Math.sin(a) * d); } g.closePath(); g.stroke();
  }
  g.restore();
}
function archPath(g, x, w, top, spring, bottom) {
  const cx = x + w / 2;
  g.beginPath(); g.moveTo(x, bottom); g.lineTo(x, spring);
  g.bezierCurveTo(x, spring - (spring - top) * 0.6, cx - w * 0.12, top + 10, cx, top);
  g.bezierCurveTo(cx + w * 0.12, top + 10, x + w, spring - (spring - top) * 0.6, x + w, spring);
  g.lineTo(x + w, bottom); g.closePath();
}
function arabesque(g, x, y, w, h, col, seed) {   // gold spandrel filled with a scrolling split-palmette vine
  const r = mulberry(seed); g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip();
  g.strokeStyle = col; g.lineWidth = 1.6;
  for (let k = 0; k < 3; k++) { const cx = x + (k + 0.5) * w / 3, cy = y + h * (0.4 + r() * 0.2), rd = Math.min(w, h) * 0.3;
    g.beginPath(); for (let a = 0; a < 10; a += 0.2) g.lineTo(cx + Math.cos(a) * rd * a / 10, cy + Math.sin(a) * rd * a / 10); g.stroke();
    g.beginPath(); g.ellipse(cx + rd * 0.9, cy - rd * 0.3, 4, 7, 0.6, 0, TAU); g.fillStyle = col; g.fill(); }
  g.restore();
}
function paintPavilion(g) {
  const { x, x1, top, floor, arch } = PAV, w = x1 - x;
  // terrace: a floor band in front of the pavilion, a tiled front face, one step down to the walk
  const tw = P.x + P.w - 1300;
  g.fillStyle = COL.buff; g.fillRect(1300, floor, tw, 24);
  g.strokeStyle = 'rgba(150,100,55,0.7)'; g.lineWidth = 1.1; for (let xx = 1300; xx < P.x + P.w; xx += 30) { g.beginPath(); g.moveTo(xx, floor); g.lineTo(xx - 8, floor + 24); g.stroke(); }
  g.fillStyle = COL.ivory; g.fillRect(1300, floor + 24, tw, 60);
  hexTiles(g, 1306, floor + 32, tw - 6, 46, 11, COL.turq, COL.white, COL.lapisD);
  g.strokeStyle = COL.inkS; g.lineWidth = 1.5; g.strokeRect(1300, floor, tw, 84); g.beginPath(); g.moveTo(1300, floor + 24); g.lineTo(1300 + tw, floor + 24); g.stroke();
  { const sx = 1226, sy = 882; g.fillStyle = COL.buff; g.fillRect(sx, sy, 1300 - sx, PATH.y1 - sy); g.fillStyle = COL.buffD; g.fillRect(sx, sy, 1300 - sx, 5); g.strokeStyle = COL.inkS; g.strokeRect(sx, sy, 1300 - sx, PATH.y1 - sy);
    g.strokeStyle = COL.verm; g.lineWidth = 2; g.beginPath(); g.moveTo(sx + 6, sy + 16); g.lineTo(1294, sy + 16); g.stroke(); }
  // body
  g.fillStyle = COL.ivory; g.fillRect(x, top, w, floor - top);
  g.strokeStyle = COL.inkS; g.lineWidth = 1.8; g.strokeRect(x, top, w, floor - top);
  // tile dado
  hexTiles(g, x + 4, floor - 58, w - 8, 54, 9, COL.lapisL, COL.white, COL.lapisD);
  // side niches with vases
  for (const nx of [x + 18, x1 - 18 - 58]) {
    archPath(g, nx, 58, 640, 676, 776); g.fillStyle = COL.turqD; g.fill(); g.strokeStyle = COL.g3; g.lineWidth = 2; g.stroke();
    g.save(); g.translate(nx + 29, 776); g.fillStyle = COL.white; g.beginPath(); g.moveTo(-9, 0); g.bezierCurveTo(-20, -16, -14, -32, -5, -36); g.lineTo(-5, -44); g.lineTo(5, -44); g.lineTo(5, -36); g.bezierCurveTo(14, -32, 20, -16, 9, 0); g.closePath(); g.fill(); g.strokeStyle = COL.lapis; g.lineWidth = 1.4; g.stroke();
    g.beginPath(); g.moveTo(-12, -18); g.lineTo(12, -18); g.stroke(); g.restore();
    archPath(g, nx, 58, 470, 500, 560); g.fillStyle = COL.lapis; g.fill(); g.strokeStyle = COL.g3; g.stroke();
    starLattice(g, nx + 8, 500, 42, 56, 16, COL.lapis, COL.g1);
  }
  // pishtaq frame around the iwan
  const fx = arch.x - 26, fw = arch.w + 52, fy = arch.top - 34;
  g.fillStyle = COL.lapis; g.fillRect(fx, fy, fw, floor - 58 - fy);
  g.save(); g.beginPath(); g.rect(fx + 6, fy + 6, fw - 12, floor - 58 - fy - 12); g.clip();
  g.fillStyle = COL.white; for (let yy = fy; yy < floor; yy += 14) for (let xx = fx; xx < fx + fw; xx += 14) { if (xx > fx + 12 && xx < fx + fw - 22 && yy > fy + 12) continue; g.beginPath(); g.arc(xx + 7, yy + 7, 2.6, 0, TAU); g.fill(); }
  g.restore();
  // spandrels (gold with arabesque)
  g.fillStyle = goldFill(g, arch.x, fy, arch.w, 90); g.fillRect(arch.x - 12, fy + 14, arch.w + 24, arch.spring - fy - 14);
  arabesque(g, arch.x - 12, fy + 14, arch.w + 24, arch.spring - fy - 14, COL.g4, 3);
  // arch opening: interior lapis, star lattice, carpet on the floor
  archPath(g, arch.x, arch.w, arch.top, arch.spring, floor); g.save(); g.clip();
  starLattice(g, arch.x, arch.top, arch.w, floor - arch.top, 30, COL.lapisD, 'rgba(242,207,102,0.7)');
  // tilted floor + carpet
  g.fillStyle = COL.buff; g.fillRect(arch.x, 772, arch.w, floor - 772);
  const cx0 = arch.x + 18, cw = arch.w - 36, cy0 = 780, ch = floor - cy0 - 4;
  g.fillStyle = COL.lapis; g.fillRect(cx0, cy0, cw, ch); g.fillStyle = COL.verm; g.fillRect(cx0 + 8, cy0 + 7, cw - 16, ch - 14);
  g.fillStyle = COL.g1; g.beginPath(); g.ellipse(cx0 + cw / 2, cy0 + ch / 2, 34, 16, 0, 0, TAU); g.fill(); g.strokeStyle = COL.lapisD; g.lineWidth = 1.5; g.stroke();
  g.fillStyle = COL.white; for (let xx = cx0 + 6; xx < cx0 + cw - 4; xx += 10) { g.fillRect(xx, cy0 + 2, 3, 3); g.fillRect(xx, cy0 + ch - 5, 3, 3); }
  g.restore();
  archPath(g, arch.x, arch.w, arch.top, arch.spring, floor); g.strokeStyle = COL.g3; g.lineWidth = 3; g.stroke(); g.strokeStyle = COL.white; g.lineWidth = 1.2; g.stroke();
  // upper storey: talar with slender columns, red curtains, lattice balustrade
  const uy = top + 44, uh = 190;
  g.fillStyle = COL.turqD; g.fillRect(x + 90, uy, w - 180, uh);
  starLattice(g, x + 90, uy, w - 180, uh, 26, COL.turqD, 'rgba(255,255,255,0.5)');
  for (let i = 0; i < 5; i++) {
    const cx = x + 90 + i * (w - 180) / 4; g.fillStyle = COL.g2; g.fillRect(cx - 4, uy, 8, uh); g.strokeStyle = COL.g4; g.lineWidth = 1; g.strokeRect(cx - 4, uy, 8, uh);
    g.fillStyle = COL.g1; g.fillRect(cx - 8, uy, 16, 8); g.fillRect(cx - 8, uy + uh - 8, 16, 8);
  }
  for (let i = 0; i < 4; i++) {   // curtains swagged at each bay
    const bx = x + 90 + i * (w - 180) / 4 + 6, bw = (w - 180) / 4 - 12;
    g.fillStyle = COL.verm; g.beginPath(); g.moveTo(bx, uy + 8); g.lineTo(bx + bw, uy + 8); g.quadraticCurveTo(bx + bw * 0.5, uy + 70, bx, uy + 8); g.fill();
    g.beginPath(); g.moveTo(bx, uy + 8); g.quadraticCurveTo(bx + 14, uy + 80, bx + 4, uy + 150); g.lineTo(bx, uy + 150); g.fill();
    g.beginPath(); g.moveTo(bx + bw, uy + 8); g.quadraticCurveTo(bx + bw - 14, uy + 80, bx + bw - 4, uy + 150); g.lineTo(bx + bw, uy + 150); g.fill();
    g.strokeStyle = COL.vermD; g.lineWidth = 1.2; g.beginPath(); g.moveTo(bx + 4, uy + 20); g.quadraticCurveTo(bx + bw * 0.5, uy + 56, bx + bw - 4, uy + 20); g.stroke();
  }
  g.fillStyle = COL.ivory; g.fillRect(x + 84, uy + uh - 34, w - 168, 34);
  g.strokeStyle = COL.vermD; g.lineWidth = 1.6; for (let xx = x + 90; xx < x1 - 90; xx += 17) { g.beginPath(); g.moveTo(xx, uy + uh - 30); g.lineTo(xx + 17, uy + uh - 4); g.moveTo(xx + 17, uy + uh - 30); g.lineTo(xx, uy + uh - 4); g.stroke(); }
  g.strokeStyle = COL.inkS; g.lineWidth = 1.4; g.strokeRect(x + 84, uy + uh - 34, w - 168, 34);
  // cornice band between storeys
  g.fillStyle = COL.lapis; g.fillRect(x, uy + uh + 4, w, 20); g.fillStyle = COL.g1; for (let xx = x + 8; xx < x1; xx += 22) { g.beginPath(); g.moveTo(xx, uy + uh + 14); g.lineTo(xx + 6, uy + uh + 8); g.lineTo(xx + 12, uy + uh + 14); g.lineTo(xx + 6, uy + uh + 20); g.fill(); }
  // parapet with stepped merlons
  g.fillStyle = COL.lapis; g.fillRect(x - 6, top, w + 12, 34); g.strokeStyle = COL.g2; g.lineWidth = 2; g.strokeRect(x - 6, top, w + 12, 34);
  g.fillStyle = COL.white; for (let xx = x + 10; xx < x1 - 6; xx += 24) { g.beginPath(); g.arc(xx, top + 17, 5, 0, TAU); g.fill(); }
  for (let xx = x - 6; xx < x1 + 4; xx += 26) { g.fillStyle = COL.ivory; g.beginPath(); g.moveTo(xx, top); g.lineTo(xx, top - 12); g.lineTo(xx + 6, top - 12); g.lineTo(xx + 6, top - 20); g.lineTo(xx + 14, top - 20); g.lineTo(xx + 14, top - 12); g.lineTo(xx + 20, top - 12); g.lineTo(xx + 20, top); g.fill(); g.strokeStyle = COL.inkS; g.lineWidth = 1; g.stroke(); }
  // canopy kiosk on the roof
  const kx = x + w / 2, ky = top - 20;
  g.fillStyle = COL.g2; for (const dx of [-44, 38]) g.fillRect(kx + dx, ky - 56, 6, 56);
  g.fillStyle = COL.verm; g.beginPath(); g.moveTo(kx - 62, ky - 54); g.quadraticCurveTo(kx - 40, ky - 70, kx, ky - 112); g.quadraticCurveTo(kx + 40, ky - 70, kx + 62, ky - 54); g.closePath(); g.fill(); g.strokeStyle = COL.vermD; g.lineWidth = 1.6; g.stroke();
  g.strokeStyle = COL.g1; g.lineWidth = 2; for (let k = -2; k <= 2; k++) { g.beginPath(); g.moveTo(kx + k * 22, ky - 56); g.quadraticCurveTo(kx + k * 9, ky - 80, kx, ky - 110); g.stroke(); }
  g.fillStyle = COL.g1; g.fillRect(kx - 64, ky - 58, 128, 6);
  g.beginPath(); g.arc(kx, ky - 118, 6, 0, TAU); g.fill(); g.fillRect(kx - 1.5, ky - 136, 3, 18);
}

// ── trees ──
function cypress(g, x, base, h, w, seed) {
  const r = mulberry(seed), bend = (r() - 0.5) * 18;
  const pts = []; const n = 40;
  for (let i = 0; i <= n; i++) { const u = i / n, hw = w * Math.pow(Math.sin(Math.PI * Math.min(1, u * 1.08 + 0.02)), 0.8) * (1 - u * 0.55) * 0.5 + 1; pts.push([x + bend * u * u, base - h * u, hw]); }
  g.beginPath(); pts.forEach(([px, py, hw], i) => i ? g.lineTo(px - hw, py) : g.moveTo(px - hw, py)); for (let i = n; i >= 0; i--) g.lineTo(pts[i][0] + pts[i][2], pts[i][1]); g.closePath();
  g.fillStyle = COL.cyp; g.fill(); g.lineWidth = 1.6; g.strokeStyle = '#0f2e20'; g.stroke();
  // feathered foliage: rows of tiny arcs
  g.save(); g.clip(); g.strokeStyle = COL.cypL; g.lineWidth = 1.3;
  for (let i = 2; i < n; i++) { const [px, py, hw] = pts[i]; for (let k = -hw; k < hw; k += 7) { g.beginPath(); g.arc(px + k + (i % 2) * 3.5, py, 4, Math.PI * 0.1, Math.PI * 0.9); g.stroke(); } }
  g.restore();
  g.fillStyle = COL.brownD; g.fillRect(x - 3, base - 4, 6, 10);
}
function almond(g, x, base, seed, grp, h = 210, bloom0 = 0) {
  const r = mulberry(seed);
  const branch = (x0, y0, a, len, wd, depth) => {
    const x1 = x0 + Math.cos(a) * len, y1 = y0 + Math.sin(a) * len, mx = (x0 + x1) / 2 + (r() - 0.5) * len * 0.3, my = (y0 + y1) / 2 + (r() - 0.5) * len * 0.2;
    g.strokeStyle = COL.brownD; g.lineWidth = wd; g.lineCap = 'round'; g.beginPath(); g.moveTo(x0, y0); g.quadraticCurveTo(mx, my, x1, y1); g.stroke();
    if (depth >= 2) for (let k = 0; k < 3; k++) { const u = 0.35 + k * 0.3; const bx = lerp(lerp(x0, mx, u), lerp(mx, x1, u), u), by = lerp(lerp(y0, my, u), lerp(my, y1, u), u); if (r() < 0.55) SITES.bloss.push({ x: bx + (r() - 0.5) * 10, y: by + (r() - 0.5) * 10, s: 0.34 + r() * 0.22, grp, k: r(), pink: r() < 0.45, b0: bloom0 }); }
    if (depth <= 0) { for (let k = 0; k < 2; k++) SITES.bloss.push({ x: x1 + (r() - 0.5) * 16, y: y1 + (r() - 0.5) * 14, s: 0.36 + r() * 0.26, grp, k: r(), pink: r() < 0.45, b0: bloom0 }); return; }
    const nb = depth > 2 ? 2 : 2 + (r() < 0.5 ? 1 : 0);
    for (let k = 0; k < nb; k++) branch(x1, y1, a + (k - (nb - 1) / 2) * (0.55 + r() * 0.3) + (r() - 0.5) * 0.3, len * (0.66 + r() * 0.12), wd * 0.66, depth - 1);
  };
  // trunk: a slightly twisting double stroke
  g.fillStyle = COL.brown; g.beginPath(); g.moveTo(x - 7, base); g.bezierCurveTo(x - 10, base - h * 0.3, x + 8, base - h * 0.35, x - 2, base - h * 0.45); g.lineTo(x + 4, base - h * 0.45); g.bezierCurveTo(x + 14, base - h * 0.32, x - 2, base - h * 0.25, x + 7, base); g.closePath(); g.fill(); g.strokeStyle = COL.brownD; g.lineWidth = 1.4; g.stroke();
  const ty = base - h * 0.44;
  branch(x + 1, ty, -Math.PI / 2 - 0.55, h * 0.3, 7, 4); branch(x + 1, ty, -Math.PI / 2 + 0.5, h * 0.3, 7, 4); branch(x + 1, ty, -Math.PI / 2 + 0.02, h * 0.34, 6, 4);
}
function pomegranate(g, x, base, seed) {
  const r = mulberry(seed);
  g.fillStyle = COL.brown; g.fillRect(x - 5, base - 90, 10, 90); g.strokeStyle = COL.brownD; g.lineWidth = 1.2; g.strokeRect(x - 5, base - 90, 10, 90);
  for (let i = 0; i < 70; i++) {
    const a = r() * TAU, d = Math.sqrt(r()), cx = x + Math.cos(a) * d * 62, cy = base - 140 + Math.sin(a) * d * 52;
    g.save(); g.translate(cx, cy); g.rotate(r() * TAU); g.beginPath(); g.ellipse(0, 0, 11, 5, 0, 0, TAU); g.fillStyle = r() < 0.5 ? COL.emer : COL.emerD; g.fill(); g.strokeStyle = '#123a24'; g.lineWidth = 1; g.stroke(); g.restore();
  }
  for (let i = 0; i < 11; i++) { const a = r() * TAU, d = Math.sqrt(r()) * 0.85; const cx = x + Math.cos(a) * d * 58, cy = base - 140 + Math.sin(a) * d * 46; g.beginPath(); g.arc(cx, cy, 6, 0, TAU); g.fillStyle = COL.verm; g.fill(); g.strokeStyle = COL.vermD; g.stroke(); g.fillStyle = COL.vermD; g.fillRect(cx - 2, cy - 8, 4, 3); }
}
function chinar(g, x, base, seed) {   // plane tree: pale trunk, crown of five-lobed leaves in clusters
  const r = mulberry(seed);
  g.fillStyle = '#cdbb9a'; g.beginPath(); g.moveTo(x - 12, base); g.bezierCurveTo(x - 8, base - 60, x - 14, base - 110, x - 4, base - 150); g.lineTo(x + 6, base - 150); g.bezierCurveTo(x + 12, base - 110, x + 6, base - 60, x + 12, base); g.closePath(); g.fill(); g.strokeStyle = COL.brownD; g.lineWidth = 1.4; g.stroke();
  for (let i = 0; i < 16; i++) { g.fillStyle = 'rgba(120,100,70,0.5)'; g.beginPath(); g.ellipse(x + (r() - 0.5) * 12, base - r() * 140, 3 + r() * 3, 2, 0, 0, TAU); g.fill(); }
  g.strokeStyle = COL.brownD; g.lineWidth = 4; for (const a of [-2.2, -1.6, -0.9]) { g.beginPath(); g.moveTo(x, base - 140); g.lineTo(x + Math.cos(a) * 60, base - 140 + Math.sin(a) * 50); g.stroke(); }
  const leaf = (lx, ly, sz, rot, c) => { g.save(); g.translate(lx, ly); g.rotate(rot); g.beginPath();
    for (let k = 0; k <= 10; k++) { const a = -Math.PI / 2 + (k / 10 - 0.5) * Math.PI * 1.7, d = sz * (k % 2 ? 0.55 : 1); g.lineTo(Math.cos(a) * d, Math.sin(a) * d); } g.closePath();
    g.fillStyle = c; g.fill(); g.strokeStyle = '#123a24'; g.lineWidth = 0.9; g.stroke(); g.restore(); };
  for (let i = 0; i < 150; i++) { const a = r() * TAU, d = Math.sqrt(r()); const lx = x + Math.cos(a) * d * 95, ly = base - 205 + Math.sin(a) * d * 72; leaf(lx, ly, 9 + r() * 4, r() * 1.2 - 0.6, [COL.emer, COL.emerD, COL.cypL, COL.sage][Math.floor(r() * 4)]); }
}
function paintTrees(g) {
  // back row along the horizon
  cypress(g, 318, 318, 290, 52, 1);           // breaks out of the frame, top into the border
  almond(g, 440, 330, 7, 0, 170, 1);
  cypress(g, 540, 318, 200, 40, 2);
  almond(g, 1030, 325, 9, 0, 160, 1);
  pomegranate(g, 1250, 350, 3);
  cypress(g, 1160, 312, 210, 40, 4);
  chinar(g, 236, 552, 17);
  // flanking the pool — these wait for spring
  cypress(g, 690, 530, 250, 44, 5);
  almond(g, 600, 540, 12, 1, 230, 0);
  cypress(g, 1110, 530, 250, 44, 6);
  almond(g, 1196, 540, 14, 2, 230, 0);
  // bottom right, near the terrace
  cypress(g, 1266, 820, 210, 40, 8);
}
function paintPlants(g) {
  const r = mulberry(55);
  // flower bed borders (low trellis)
  const bed = (x, y, w, h, kinds, seed) => {
    const rr2 = mulberry(seed);
    g.strokeStyle = COL.ivory; g.lineWidth = 3; g.strokeRect(x, y, w, h); g.strokeStyle = COL.vermD; g.lineWidth = 1; g.strokeRect(x - 2, y - 2, w + 4, h + 4);
    for (let yy = y + 24; yy < y + h; yy += 30) for (let xx = x + 14; xx < x + w - 6; xx += 26) plant(g, xx + (rr2() - 0.5) * 8, yy, kinds[Math.floor(rr2() * kinds.length)], rr2);
  };
  bed(212, 560, 330, 190, ['tulip', 'iris', 'narc', 'tulip'], 61);
  bed(1340 - 190, 600, 150, 180, ['tulip', 'narc'], 62);
  { const cx = 560, cy = 700, cw = 130, ch = 86;   // a small carpet laid on the grass beside the pool
    g.fillStyle = COL.lapis; g.fillRect(cx, cy, cw, ch); g.fillStyle = COL.verm; g.fillRect(cx + 9, cy + 9, cw - 18, ch - 18);
    g.strokeStyle = COL.g1; g.lineWidth = 1.4; g.strokeRect(cx + 4, cy + 4, cw - 8, ch - 8);
    g.fillStyle = COL.white; for (let x = cx + 6; x < cx + cw - 4; x += 9) { g.fillRect(x, cy + 1.5, 3, 3); g.fillRect(x, cy + ch - 4.5, 3, 3); }
    g.fillStyle = COL.g1; g.beginPath(); g.moveTo(cx + cw / 2, cy + 20); g.lineTo(cx + cw / 2 + 30, cy + ch / 2); g.lineTo(cx + cw / 2, cy + ch - 20); g.lineTo(cx + cw / 2 - 30, cy + ch / 2); g.closePath(); g.fill(); g.strokeStyle = COL.lapisD; g.stroke();
    g.fillStyle = COL.lapisD; g.beginPath(); g.arc(cx + cw / 2, cy + ch / 2, 6, 0, TAU); g.fill();
    for (const [x, c] of [[cx + 22, COL.turq], [cx + cw - 22, COL.g2]]) { g.fillStyle = c; rr(g, x - 16, cy + 12, 32, 20, 8); g.fill(); g.strokeStyle = COL.ink; g.lineWidth = 1.2; g.stroke(); }
  }
  // rose bushes along the walk (heads bloom later)
  for (const [x, grp] of [[250, 3], [470, 3], [700, 3], [1060, 3], [1170, 3]]) {
    const y = PATH.y0 - 6;
    for (let i = 0; i < 30; i++) { const a = Math.PI + r() * Math.PI, d = Math.sqrt(r()); g.save(); g.translate(x + Math.cos(a) * d * 48, y + Math.sin(a) * d * 40); g.rotate(r() * TAU); g.beginPath(); g.ellipse(0, 0, 9, 4.5, 0, 0, TAU); g.fillStyle = r() < 0.5 ? COL.emer : COL.emerD; g.fill(); g.strokeStyle = '#123a24'; g.lineWidth = 0.8; g.stroke(); g.restore(); }
    for (let i = 0; i < 6; i++) { const a = Math.PI * (1.12 + i * 0.15), d = 26 + r() * 10; SITES.roses.push({ x: x + Math.cos(a) * d, y: y + Math.sin(a) * d * 0.9, s: 0.55 + r() * 0.2, k: r(), c: i % 3 }); }
  }
  // foreground strip below the walk
  for (let x = P.x + 10; x < P.x + P.w; x += 30 + r() * 18) plant(g, x, 968 + r() * 12, ['tulip', 'narc', 'grass', 'iris', 'grass'][Math.floor(r() * 5)], r);
}
function plant(g, x, y, kind, r) {
  g.strokeStyle = COL.emerD; g.lineWidth = 1.5; g.lineCap = 'round';
  if (kind === 'grass') { tuft(g, x, y, 1.1, r); return; }
  g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + 2, y - 10, x, y - 20); g.stroke();
  g.fillStyle = COL.emer; for (const s of [-1, 1]) { g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + s * 10, y - 6, x + s * 6, y - 16); g.quadraticCurveTo(x + s * 3, y - 6, x, y); g.fill(); }
  if (kind === 'tulip') { g.fillStyle = r() < 0.6 ? COL.verm : COL.rose; g.beginPath(); g.moveTo(x - 5, y - 26); g.lineTo(x - 5, y - 20); g.quadraticCurveTo(x, y - 16, x + 5, y - 20); g.lineTo(x + 5, y - 26); g.lineTo(x + 2, y - 23); g.lineTo(x, y - 27); g.lineTo(x - 2, y - 23); g.closePath(); g.fill(); g.strokeStyle = COL.vermD; g.lineWidth = 0.8; g.stroke(); }
  else if (kind === 'iris') { g.fillStyle = COL.lilac; for (const s of [-1, 0, 1]) { g.beginPath(); g.ellipse(x + s * 4, y - 23 + Math.abs(s) * 2, 2.6, 5, s * 0.7, 0, TAU); g.fill(); } g.fillStyle = COL.ochre; g.fillRect(x - 1, y - 22, 2, 3); }
  else { g.fillStyle = COL.white; for (let k = 0; k < 6; k++) { const a = k / 6 * TAU; g.beginPath(); g.ellipse(x + Math.cos(a) * 3.5, y - 22 + Math.sin(a) * 3.5, 2.4, 1.6, a, 0, TAU); g.fill(); } g.fillStyle = COL.ochre; g.beginPath(); g.arc(x, y - 22, 1.8, 0, TAU); g.fill(); }
}

// ── border band: lapis ground + a scrolling vine; one "outline" state and one fully gilded state ──
let BAND_O, BAND_G;
function bandPath(g) { g.beginPath(); g.rect(BO.x, BO.y, BO.w, BO.h); g.rect(BI.x, BI.y, BI.w, BI.h); }
function vineAround(g, gilded) {
  const r = mulberry(71), per = [];
  const mid = 16, x0 = BO.x + mid, y0 = BO.y + mid, x1 = BO.x + BO.w - mid, y1 = BO.y + BO.h - mid;
  // walk the centre line of the band, a sine vine with alternating palmettes
  const sides = [[x0, y0, x1, y0], [x1, y0, x1, y1], [x1, y1, x0, y1], [x0, y1, x0, y0]];
  const lw = gilded ? 2.6 : 1.4;
  for (const [ax, ay, bx, by] of sides) {
    const L = Math.hypot(bx - ax, by - ay), ux = (bx - ax) / L, uy = (by - ay) / L, nx = -uy, ny = ux, n = Math.round(L / 64);
    g.beginPath();
    for (let s = 0; s <= L; s += 3) { const o = Math.sin(s / L * n * Math.PI) * 7.5; g.lineTo(ax + ux * s + nx * o, ay + uy * s + ny * o); }
    g.lineWidth = lw; g.strokeStyle = gilded ? COL.g1 : 'rgba(240,205,120,0.55)'; g.stroke();
    for (let k = 0; k < n; k++) {
      const s = (k + 0.5) / n * L, sg = k % 2 ? 1 : -1, px = ax + ux * s + nx * sg * 6, py = ay + uy * s + ny * sg * 6;
      g.save(); g.translate(px, py); g.rotate(Math.atan2(uy, ux) + (sg > 0 ? Math.PI / 2 : -Math.PI / 2));
      g.beginPath(); g.moveTo(0, 0); g.bezierCurveTo(-7, -3, -6, -11, 0, -13); g.bezierCurveTo(6, -11, 7, -3, 0, 0);
      if (gilded) { g.fillStyle = goldFill(g, -7, -13, 14, 13); g.fill(); g.strokeStyle = COL.g4; g.lineWidth = 0.9; g.stroke(); }
      else { g.strokeStyle = 'rgba(240,205,120,0.6)'; g.lineWidth = 1.1; g.stroke(); }
      g.restore();
      // tiny blossoms between palmettes
      const qx = ax + ux * (s + L / n / 2) - nx * sg * 5, qy = ay + uy * (s + L / n / 2) - ny * sg * 5;
      if (k < n - 1) { g.beginPath(); g.arc(qx, qy, gilded ? 3 : 2.5, 0, TAU); if (gilded) { g.fillStyle = COL.white; g.fill(); g.strokeStyle = COL.verm; g.lineWidth = 1; g.stroke(); } else { g.strokeStyle = 'rgba(240,205,120,0.5)'; g.lineWidth = 1; g.stroke(); } }
    }
  }
  // corner rosettes
  for (const [cx, cy] of [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]) {
    g.save(); g.translate(cx, cy);
    for (let k = 0; k < 8; k++) { g.rotate(TAU / 8); g.beginPath(); g.ellipse(0, -8, 3.6, 7, 0, 0, TAU); if (gilded) { g.fillStyle = goldFill(g, -4, -15, 8, 15); g.fill(); g.strokeStyle = COL.g4; g.lineWidth = 0.8; g.stroke(); } else { g.strokeStyle = 'rgba(240,205,120,0.6)'; g.lineWidth = 1; g.stroke(); } }
    g.beginPath(); g.arc(0, 0, 4, 0, TAU); g.fillStyle = gilded ? COL.verm : 'rgba(240,205,120,0.4)'; g.fill(); g.restore();
  }
}
function bakeBand() {
  const mkB = gilded => {
    const c = mk(W, H), g = c.getContext('2d');
    g.save(); bandPath(g); g.clip('evenodd');
    g.fillStyle = COL.lapis; g.fillRect(0, 0, W, H);
    const r = mulberry(81); for (let i = 0; i < 900; i++) { g.fillStyle = `rgba(${r() < 0.5 ? '10,20,60' : '120,150,230'},${0.08 + r() * 0.1})`; g.beginPath(); g.arc(BO.x + r() * BO.w, BO.y + r() * BO.h, 1 + r() * 2, 0, TAU); g.fill(); }
    vineAround(g, gilded); g.restore();
    return c;
  };
  BAND_O = mkB(false); BAND_G = mkB(true);
}

function bakeLayers() {
  const full = [P.x, P.y, P.w, P.h];
  layer('sky', [P.x, P.y, P.w, 260], 1.15, 1.95, 'down', paintSky);
  layer('ground', [P.x, 180, P.w, P.y + P.h - 180], 1.4, 2.3, 'up', paintGround);
  layer('court', [P.x, POOL.y - 240, 1360, P.y + P.h - POOL.y + 240], 1.75, 2.55, 'right', paintCourt);
  layer('pav', [1220, 240, 560, 700], 1.95, 2.8, 'up', paintPavilion);
  layer('trees', [P.x, 20, P.w, 820], 2.15, 3.0, 'out', paintTrees, g => { g.beginPath(); g.rect(P.x, 20, P.w, P.y + P.h - 20); g.clip(); });
  layer('plants', [P.x, 520, P.w, 470], 2.35, 3.1, 'right', paintPlants);
}
