// lib.js · helpers, palette and baked textures (vellum, desk, grain) — all deterministic, seeded
const TAU = Math.PI * 2;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eOut = u => 1 - Math.pow(1 - u, 3);
const eIn = u => u * u * u;
const eInOut = u => u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
const eSine = u => 0.5 - 0.5 * Math.cos(Math.PI * u);
const eBack = u => { const c = 1.9; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
function mulberry(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const hash = n => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
function mk(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }

// pigments of a 14th-century scriptorium
const COL = {
  ink: '#2a1b12', inkS: '#4a3324', red: '#b8321f', redD: '#8e2416', blue: '#2a4f9e', blueD: '#1b336d', blueL: '#6f8fd0',
  rose: '#c9667a', roseD: '#9c4458', green: '#3f7a4a', greenD: '#28573a', greenL: '#7fae6e', white: '#fbf5e6',
  ochre: '#c8913a', brick: '#b5553a', bole: '#8f3a22', vel: '#efe1c1',
  g0: '#fff2b8', g1: '#f1cf6a', g2: '#cf9d34', g3: '#8d6116', g4: '#5a3b0c',
};
const PW = 880, PH = 980;   // one page
const FB = '"Grenze Gotisch"', FT = 'UnifrakturCook';

// ── vellum: warm mottled skin, follicle speckle, hair-side veining, slight cockle; one per page ──
function bakeVellum(seed, side) {   // side: 'L' page (gutter at right) or 'R'
  const c = mk(PW, PH), g = c.getContext('2d'), r = mulberry(seed);
  g.fillStyle = COL.vel; g.fillRect(0, 0, PW, PH);
  for (let i = 0; i < 55; i++) {
    const x = r() * PW, y = r() * PH, rad = 60 + r() * 240, dark = r() < 0.55;
    const gr = g.createRadialGradient(x, y, 0, x, y, rad);
    gr.addColorStop(0, dark ? `rgba(170,125,70,${0.05 + r() * 0.07})` : `rgba(255,250,232,${0.10 + r() * 0.10})`); gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gr; g.fillRect(x - rad, y - rad, rad * 2, rad * 2);
  }
  // faint veins (hair side of the skin)
  for (let i = 0; i < 9; i++) {
    let x = r() * PW, y = r() * PH, a = r() * TAU; g.strokeStyle = `rgba(150,105,60,${0.04 + r() * 0.05})`; g.lineWidth = 1 + r() * 2.2;
    g.beginPath(); g.moveTo(x, y);
    for (let k = 0; k < 30; k++) { a += (r() - 0.5) * 0.5; x += Math.cos(a) * 14; y += Math.sin(a) * 14; g.lineTo(x, y); }
    g.stroke();
  }
  // follicles & specks
  for (let i = 0; i < 2200; i++) { g.fillStyle = `rgba(110,75,40,${0.05 + r() * 0.16})`; const s = 0.5 + r() * 1.5; g.beginPath(); g.ellipse(r() * PW, r() * PH, s, s * (0.6 + r() * 0.6), r() * 3, 0, TAU); g.fill(); }
  for (let i = 0; i < 900; i++) { g.fillStyle = `rgba(255,252,240,${0.10 + r() * 0.2})`; g.fillRect(r() * PW, r() * PH, 1 + r() * 2, 1); }
  // edges darker & slightly foxed; outer edge worn
  const ox = side === 'L' ? 0 : PW, dx = side === 'L' ? 1 : -1;
  let gr = g.createLinearGradient(ox, 0, ox + dx * 90, 0); gr.addColorStop(0, 'rgba(140,95,45,0.28)'); gr.addColorStop(1, 'rgba(140,95,45,0)'); g.fillStyle = gr; g.fillRect(0, 0, PW, PH);
  gr = g.createLinearGradient(0, 0, 0, 70); gr.addColorStop(0, 'rgba(140,95,45,0.22)'); gr.addColorStop(1, 'rgba(140,95,45,0)'); g.fillStyle = gr; g.fillRect(0, 0, PW, 70);
  gr = g.createLinearGradient(0, PH, 0, PH - 80); gr.addColorStop(0, 'rgba(140,95,45,0.26)'); gr.addColorStop(1, 'rgba(140,95,45,0)'); g.fillStyle = gr; g.fillRect(0, PH - 80, PW, 80);
  for (let i = 0; i < 14; i++) {   // foxing near the edges
    const x = side === 'L' ? r() * 120 : PW - r() * 120, y = r() * PH, rad = 6 + r() * 22;
    const f = g.createRadialGradient(x, y, 0, x, y, rad); f.addColorStop(0, 'rgba(150,95,40,0.16)'); f.addColorStop(1, 'rgba(150,95,40,0)'); g.fillStyle = f; g.fillRect(x - rad, y - rad, rad * 2, rad * 2);
  }
  return c;
}

// a grain / tooth layer multiplied over painted content so paint sits in the skin
function bakeTooth(seed) {
  const c = mk(PW, PH), g = c.getContext('2d'), r = mulberry(seed);
  const id = g.createImageData(PW, PH), d = id.data;
  for (let i = 0; i < d.length; i += 4) { const v = 236 + r() * 19; d[i] = v; d[i + 1] = v - 3; d[i + 2] = v - 9; d[i + 3] = 255; }
  g.putImageData(id, 0, 0);
  return c;
}

// ── desk: dark oak with candle-lit falloff; book: leather boards + page-block edges ──
let DESK;
function bakeDesk() {
  const W = 1920, H = 1080, r = mulberry(7);
  DESK = mk(W, H); const g = DESK.getContext('2d');
  g.fillStyle = '#2a1a10'; g.fillRect(0, 0, W, H);
  for (let y = 0; y < H; y += 2) {   // long grain
    const v = 0.5 + 0.5 * Math.sin(y * 0.021 + Math.sin(y * 0.0033) * 4) * Math.sin(y * 0.0071 + 1.3);
    g.fillStyle = `rgba(${70 + v * 40},${42 + v * 24},${22 + v * 10},${0.25 + v * 0.25})`; g.fillRect(0, y, W, 2);
  }
  for (let i = 0; i < 260; i++) {
    const y = r() * H; g.strokeStyle = `rgba(20,10,4,${0.12 + r() * 0.2})`; g.lineWidth = 0.6 + r() * 1.6;
    g.beginPath(); let x = -20, yy = y; g.moveTo(x, yy); while (x < W + 20) { x += 40; yy += (r() - 0.5) * 2.2; g.lineTo(x, yy); } g.stroke();
  }
  const lg = g.createRadialGradient(W * 0.46, H * 0.36, 100, W * 0.5, H * 0.5, 1250);
  lg.addColorStop(0, 'rgba(255,190,110,0.20)'); lg.addColorStop(0.5, 'rgba(0,0,0,0.15)'); lg.addColorStop(1, 'rgba(0,0,0,0.78)');
  g.fillStyle = lg; g.fillRect(0, 0, W, H);
  // leather boards under the page block
  const bx = 80 - 26, by = 50 - 22, bw = 1760 + 52, bh = 980 + 44;
  g.save(); g.shadowColor = 'rgba(0,0,0,0.75)'; g.shadowBlur = 50; g.shadowOffsetY = 18;
  g.fillStyle = '#4a1d14'; rr(g, bx, by, bw, bh, 14); g.fill(); g.restore();
  const lt = g.createLinearGradient(bx, by, bx + bw, by + bh); lt.addColorStop(0, 'rgba(255,170,120,0.10)'); lt.addColorStop(1, 'rgba(0,0,0,0.3)');
  g.fillStyle = lt; rr(g, bx, by, bw, bh, 14); g.fill();
  for (let i = 0; i < 1400; i++) { g.fillStyle = `rgba(${r() < 0.5 ? '20,5,2' : '120,60,40'},${0.1 + r() * 0.15})`; g.fillRect(bx + r() * bw, by + r() * bh, 1.5, 1.5); }
  g.strokeStyle = 'rgba(210,160,80,0.35)'; g.lineWidth = 2; rr(g, bx + 8, by + 8, bw - 16, bh - 16, 10); g.stroke();
  // page-block edges (stacked leaves) peeking at the outer sides
  for (let k = 0; k < 7; k++) {
    g.fillStyle = k % 2 ? '#d9c79f' : '#c9b58b';
    g.fillRect(80 - 3 - k * 2.2, 50 + 4 + k, 3, 980 - 8 - k * 2); g.fillRect(1840 + k * 2.2, 50 + 4 + k, 3, 980 - 8 - k * 2);
    g.fillRect(84, 1030 + k * 1.4, 872, 1.6); g.fillRect(964, 1030 + k * 1.4, 872, 1.6);
  }
}
function rr(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }

// gutter shading for a page lying flat (page coords)
let GUT_L, GUT_R;
function bakeGutters() {
  const mkG = (side) => {
    const c = mk(PW, PH), g = c.getContext('2d'); const x0 = side === 'L' ? PW : 0, dx = side === 'L' ? -1 : 1;
    const gr = g.createLinearGradient(x0, 0, x0 + dx * 170, 0);
    gr.addColorStop(0, 'rgba(60,35,15,0.55)'); gr.addColorStop(0.12, 'rgba(90,55,25,0.30)'); gr.addColorStop(0.45, 'rgba(120,80,40,0.08)'); gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gr; g.fillRect(0, 0, PW, PH);
    // page curvature highlight a little away from the gutter
    const hg = g.createLinearGradient(x0 + dx * 170, 0, x0 + dx * 420, 0);
    hg.addColorStop(0, 'rgba(255,248,225,0)'); hg.addColorStop(0.5, 'rgba(255,248,225,0.10)'); hg.addColorStop(1, 'rgba(255,248,225,0)');
    g.fillStyle = hg; g.fillRect(0, 0, PW, PH);
    return c;
  };
  GUT_L = mkG('L'); GUT_R = mkG('R');
}

// ── burnished gold ──
// paint a gold region: `shape(g)` builds a path. u = laying progress (bole → leaf), sh = shine sweep phase (0..1, <0 none)
function gold(g, shape, bb, u = 1, sh = -1, seed = 1) {
  if (u <= 0) return;
  const [x, y, w, h] = bb, r = mulberry(seed);
  g.save(); shape(g); g.clip();
  // red bole underlayer shows first, then the leaf is laid in a diagonal wipe
  g.fillStyle = COL.bole; g.globalAlpha = clamp(u * 3); g.fillRect(x - 2, y - 2, w + 4, h + 4); g.globalAlpha = 1;
  const lu = clamp((u - 0.25) / 0.75);
  if (lu > 0) {
    g.save(); g.beginPath(); const d = (w + h) * lu * 1.05;
    g.moveTo(x - 4, y - 4); g.lineTo(x - 4 + d, y - 4); g.lineTo(x - 4, y - 4 + d); g.closePath(); g.clip();
    const gr = g.createLinearGradient(x, y, x + w * 0.8, y + h);
    gr.addColorStop(0, COL.g1); gr.addColorStop(0.28, COL.g0); gr.addColorStop(0.48, COL.g2); gr.addColorStop(0.7, COL.g1); gr.addColorStop(1, COL.g3);
    g.fillStyle = gr; g.fillRect(x - 2, y - 2, w + 4, h + 4);
    // leaf seams & burnish streaks
    for (let i = 0; i < 6; i++) { g.fillStyle = `rgba(${r() < 0.5 ? '120,80,20' : '255,245,200'},${0.08 + r() * 0.1})`; g.fillRect(x + r() * w, y - 2, 1 + r() * 3, h + 4); }
    g.restore();
  }
  // shine: bright diagonal band sweeping across
  if (sh >= 0 && sh <= 1) {
    const cx = lerp(x - w * 0.6, x + w * 1.6, sh);
    const sg = g.createLinearGradient(cx - 70, y, cx + 70, y + h * 0.35);
    sg.addColorStop(0, 'rgba(255,255,240,0)'); sg.addColorStop(0.5, 'rgba(255,250,225,0.7)'); sg.addColorStop(1, 'rgba(255,255,240,0)');
    g.globalCompositeOperation = 'lighter'; g.fillStyle = sg; g.fillRect(x - 2, y - 2, w + 4, h + 4); g.globalCompositeOperation = 'source-over';
  }
  g.restore();
  // raised gesso: dark contour below-right, light rim top-left
  if (lu > 0.98) {
    g.save(); g.lineWidth = 1.6; g.strokeStyle = 'rgba(70,40,8,0.85)'; g.translate(0.8, 1.2); shape(g); g.stroke(); g.restore();
    g.save(); g.lineWidth = 1; g.strokeStyle = 'rgba(255,248,210,0.55)'; g.translate(-0.6, -0.8); shape(g); g.stroke(); g.restore();
  }
}
