// lib.js · helpers, pigments, paper, gold flecks and small sprites — all deterministic, seeded
const TAU = Math.PI * 2;
const W = 1920, H = 1080;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eOut = u => 1 - Math.pow(1 - u, 3);
const eIn = u => u * u * u;
const eInOut = u => u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
const eSine = u => 0.5 - 0.5 * Math.cos(Math.PI * u);
const eBack = u => { const c = 2.2; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
function mulberry(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const hash = n => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
function mk(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
function rr(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }

// opaque mineral pigments of a Safavid atelier
const COL = {
  ink: '#2b1a12', inkS: '#4d3222',
  lapis: '#1f3d98', lapisD: '#13286a', lapisL: '#5d80d2', azure: '#8fb3e6',
  verm: '#d9442b', vermD: '#a42c19', rose: '#e8909d', roseD: '#c25f72', pinkL: '#f6c7cc',
  emer: '#2f8a57', emerD: '#1d5f3c', emerL: '#6fb46e', sage: '#9cc27a', cyp: '#1d4f38', cypL: '#3f7f55',
  ground: '#6aa55c', groundD: '#528f4a', groundL: '#8cc06f',
  turq: '#35a9a4', turqD: '#1f7a78', lilac: '#a88ccc', lilacD: '#7a62a3', ochre: '#dca544', ochreD: '#b07a26',
  ivory: '#f5ecd6', white: '#fdf9ef', buff: '#e8d3a8', buffD: '#c9ad7a', brown: '#6b3d22', brownD: '#452413',
  paper: '#efe2c2', water: '#9cc0dc', waterD: '#5f88b4',
  g0: '#fff3b6', g1: '#f2cf66', g2: '#d19f34', g3: '#8f6317', g4: '#5c3d0c',
};
const FT = 'Amiri';

// ── painting rectangle and the border band ──
const P = { x: 150, y: 94, w: 1620, h: 892 };              // the painting
const BO = { x: 100, y: 44, w: 1720, h: 992 };             // outer edge of the border band
const BI = { x: 132, y: 76, w: 1656, h: 928 };             // inner edge of the border band
const clipP = g => { g.beginPath(); g.rect(P.x, P.y, P.w, P.h); g.clip(); };

// ── margin paper: warm buff with zar-afshan (sprinkled gold) flecks ──
let PAPER;
function bakePaper() {
  PAPER = mk(W, H); const g = PAPER.getContext('2d'), r = mulberry(11);
  g.fillStyle = COL.paper; g.fillRect(0, 0, W, H);
  for (let i = 0; i < 70; i++) {
    const x = r() * W, y = r() * H, rad = 80 + r() * 260, dark = r() < 0.5;
    const gr = g.createRadialGradient(x, y, 0, x, y, rad);
    gr.addColorStop(0, dark ? `rgba(180,140,80,${0.04 + r() * 0.05})` : `rgba(255,251,236,${0.08 + r() * 0.08})`); gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gr; g.fillRect(x - rad, y - rad, rad * 2, rad * 2);
  }
  // burnished paper fibres
  for (let i = 0; i < 1600; i++) { g.strokeStyle = `rgba(150,110,60,${0.03 + r() * 0.05})`; g.lineWidth = 0.7; const x = r() * W, y = r() * H, a = r() * TAU, l = 4 + r() * 12; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke(); }
  // gold flecks: irregular flakes, denser near the outer edge
  FLECKS = [];
  for (let i = 0; i < 900; i++) {
    let x = r() * W, y = r() * H;
    if (x > BO.x - 6 && x < BO.x + BO.w + 6 && y > BO.y - 6 && y < BO.y + BO.h + 6) continue;   // margin only
    const s = 1.2 + r() * r() * 5.5; flake(g, x, y, s, r);
    if (s > 3.2) FLECKS.push({ x, y, s, ph: r() });
  }
  // soft edge darkening
  const vg = g.createRadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1150);
  vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(110,70,30,0.22)'); g.fillStyle = vg; g.fillRect(0, 0, W, H);
}
let FLECKS = [];
function flake(g, x, y, s, r) {
  g.beginPath(); const n = 5 + Math.floor(r() * 3), a0 = r() * TAU;
  for (let k = 0; k < n; k++) { const a = a0 + k / n * TAU, d = s * (0.5 + r() * 0.7); k ? g.lineTo(x + Math.cos(a) * d, y + Math.sin(a) * d) : g.moveTo(x + Math.cos(a) * d, y + Math.sin(a) * d); }
  g.closePath(); const gr = g.createLinearGradient(x - s, y - s, x + s, y + s); gr.addColorStop(0, COL.g0); gr.addColorStop(0.5, COL.g1); gr.addColorStop(1, COL.g3);
  g.fillStyle = gr; g.fill();
}

// static grain multiplied over everything so the paint sits in the paper
let GRAIN;
function bakeGrain() {
  GRAIN = mk(W, H); const g = GRAIN.getContext('2d'), r = mulberry(5);
  const id = g.createImageData(W, H), d = id.data;
  for (let i = 0; i < d.length; i += 4) { const v = 238 + r() * 17; d[i] = v; d[i + 1] = v - 2; d[i + 2] = v - 7; d[i + 3] = 255; }
  g.putImageData(id, 0, 0);
}

// gold fill for a path (burnished leaf)
function goldFill(g, x, y, w, h) {
  const gr = g.createLinearGradient(x, y, x + w * 0.7, y + h);
  gr.addColorStop(0, COL.g1); gr.addColorStop(0.3, COL.g0); gr.addColorStop(0.5, COL.g2); gr.addColorStop(0.75, COL.g1); gr.addColorStop(1, COL.g3);
  return gr;
}

// ── sprites (drawn once, stamped many times) ──
const SPR = {};
function sprite(size, fn) { const c = mk(size, size), g = c.getContext('2d'); g.translate(size / 2, size / 2); fn(g, size / 2); return c; }
function bakeSprites() {
  const blossom = (petal, edge, heart) => sprite(40, (g, R) => {
    for (let k = 0; k < 5; k++) {
      g.save(); g.rotate(k / 5 * TAU); g.beginPath(); g.ellipse(0, -R * 0.48, R * 0.34, R * 0.46, 0, 0, TAU);
      g.fillStyle = petal; g.fill(); g.lineWidth = 1.2; g.strokeStyle = edge; g.stroke(); g.restore();
    }
    g.beginPath(); g.arc(0, 0, R * 0.2, 0, TAU); g.fillStyle = heart; g.fill();
    for (let k = 0; k < 5; k++) { const a = k / 5 * TAU + 0.6; g.fillStyle = COL.vermD; g.beginPath(); g.arc(Math.cos(a) * R * 0.28, Math.sin(a) * R * 0.28, 1.3, 0, TAU); g.fill(); }
  });
  SPR.bW = blossom(COL.white, 'rgba(190,120,130,0.9)', COL.ochre);
  SPR.bP = blossom(COL.pinkL, 'rgba(180,80,100,0.9)', COL.verm);
  SPR.bR = blossom(COL.rose, 'rgba(140,40,60,0.9)', COL.g1);
  SPR.bud = sprite(16, (g, R) => { g.beginPath(); g.ellipse(0, 0, R * 0.45, R * 0.62, 0, 0, TAU); g.fillStyle = COL.vermD; g.fill(); g.beginPath(); g.ellipse(0, -R * 0.1, R * 0.28, R * 0.38, 0, 0, TAU); g.fillStyle = COL.rose; g.fill(); });
  SPR.petal = sprite(20, (g, R) => { g.beginPath(); g.ellipse(0, 0, R * 0.42, R * 0.8, 0, 0, TAU); g.fillStyle = COL.white; g.fill(); g.lineWidth = 1; g.strokeStyle = 'rgba(200,110,125,0.9)'; g.stroke(); });
  SPR.petalP = sprite(20, (g, R) => { g.beginPath(); g.ellipse(0, 0, R * 0.42, R * 0.8, 0, 0, TAU); g.fillStyle = COL.pinkL; g.fill(); g.lineWidth = 1; g.strokeStyle = 'rgba(180,80,100,0.9)'; g.stroke(); });
  const rose = (c1, c2) => sprite(44, (g, R) => {
    g.beginPath(); g.arc(0, 0, R * 0.82, 0, TAU); g.fillStyle = c2; g.fill();
    for (let k = 0; k < 7; k++) { const a = k / 7 * TAU; g.beginPath(); g.arc(Math.cos(a) * R * 0.5, Math.sin(a) * R * 0.5, R * 0.36, 0, TAU); g.fillStyle = c1; g.fill(); g.lineWidth = 1.2; g.strokeStyle = c2; g.stroke(); }
    g.beginPath(); g.arc(0, 0, R * 0.42, 0, TAU); g.fillStyle = c1; g.fill(); g.strokeStyle = c2; g.lineWidth = 1.4; g.stroke();
    g.beginPath(); for (let a = 0; a < 9; a += 0.2) { const d = a * R * 0.04; g.lineTo(Math.cos(a) * d, Math.sin(a) * d); } g.strokeStyle = c2; g.lineWidth = 1.2; g.stroke();
  });
  SPR.roseR = rose(COL.verm, COL.vermD); SPR.roseP = rose(COL.rose, COL.roseD); SPR.roseW = rose(COL.white, '#c9a0a0');
}
