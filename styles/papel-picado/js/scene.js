// scene.js · a town plaza at dusk: strings of papel picado unfurl, a gust sets them fluttering, lamps shine through
// the tissue, marigold petals drift down, then the view tilts up to a string of cut-paper letters: ¡FIESTA!
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const DUR = 10, CAMMAX = 900;
const TL = { lightsOn: [0.15, 1.1], tilt: [4.85, 7.05], gust: 3.15, glow: [4.0, 5.2], title0: 6.35, caption: 7.85, twinkle: 8.2, end: [9.0, 10] };
const TITLE = ['¡', 'F', 'I', 'E', 'S', 'T', 'A', '!'], CAPTION = 'A NIGHT OF CUT PAPER & LIGHT';
const FTITLE = `100px ${FT}`, FCAP = `600 34px '${FC}'`;

// ---------- camera & wind ----------
const cam = t => CAMMAX * eInOut(seg(t, TL.tilt[0], TL.tilt[1])) - 22 * Math.sin(Math.PI * seg(t, TL.tilt[0] - 0.35, TL.tilt[0] + 0.25)) * (t < TL.tilt[0] + 0.25 ? 1 : 0);
const windRaw = t => 0.22 + 0.85 * Math.exp(-Math.pow((t - 4.05) / 0.75, 2)) + 0.22 * seg(t, 5.5, 7) + 0.08 * vnoise(t * 1.3, 3);
const WT = []; { let a = 0; for (let i = 0; i <= DUR * 120 + 240; i++) { WT.push(a); a += (1.6 + 2.6 * windRaw(i / 120)) / 120; } }
const windPhase = t => { const f = clamp(t, 0, DUR + 1.9) * 120, i = Math.floor(f); return lerp(WT[i], WT[i + 1], f - i); };

// ---------- strings of banners and strings of lights ----------
const catY = (S, x) => { const u = (x - S.xm) / S.half; return S.y + S.sag * (1 - u * u); };
const catSlope = (S, x) => -2 * S.sag * (x - S.xm) / (S.half * S.half);
const BSTR = [
  { id: 'far', par: 0.62, y: 392, sag: 34, xm: 960, half: 1100, s: 0.42, n: 17, t0: 0.5, gap: 0.065, off: 0 },
  { id: 'mid', par: 0.88, y: 178, sag: 62, xm: 900, half: 1150, s: 0.7, n: 11, t0: 0.8, gap: 0.085, off: 3 },
  { id: 'near', par: 1.3, y: -215, sag: 165, xm: 980, half: 1100, s: 1.22, n: 6, t0: 1.3, gap: 0.13, off: 5 },
];
const TSTR = { id: 'title', par: 1.0, y: -CAMMAX + 205, sag: 56, xm: 960, half: 1120, s: 1.0 };
const LSTR = [
  { par: 0.45, y: 560, sag: 60, xm: 960, half: 1150, n: 26, r: 3.2, g: 0.6, x0: -40, x1: 1960 },
  { par: 0.45, y: 610, sag: 34, xm: 420, half: 700, n: 14, r: 2.6, g: 0.5, x0: -60, x1: 900 },
  { par: 0.78, y: 318, sag: 64, xm: 980, half: 1100, n: 22, r: 4.4, g: 0.8, x0: -40, x1: 1960 },
  { par: 1.0, y: -CAMMAX + 112, sag: 46, xm: 960, half: 1100, n: 22, r: 4.8, g: 0.85, x0: -40, x1: 1960 },
  { par: 1.0, y: -CAMMAX + 790, sag: 44, xm: 960, half: 1100, n: 24, r: 5, g: 0.9, x0: -40, x1: 1960 },
];
let BANNERS = [], TITLEB = [], BULBS = [];
function initStrings() {
  let seed = 1;
  for (const S of BSTR) {
    const span = 2000 / S.n;
    for (let i = 0; i < S.n; i++) {
      const x = -20 + (i + 0.5) * span + (hash(seed * 3.1) - 0.5) * span * 0.08;
      const col = PAPER[(i * 3 + S.off) % PAPER.length];
      BANNERS.push({ S, x, B: bakeBanner(230, 300, col, (i + S.off) % 4, seed), ph: hash(seed * 9.7) * TAU, t0: S.t0 + i * S.gap + hash(seed) * 0.05, seed });
      seed++;
    }
  }
  const tc = [0, 1, 2, 3, 4, 5, 6, 0];
  for (let i = 0; i < TITLE.length; i++) {
    const x = 960 + (i - 3.5) * 226;
    TITLEB.push({ S: TSTR, x, B: bakeBanner(206, 300, PAPER[tc[i]], 0, 100 + i, TITLE[i]), ph: hash(200 + i) * TAU, t0: TL.title0 + i * 0.11, seed: 100 + i, i });
  }
  let k = 0;
  for (const L of LSTR) for (let i = 0; i < L.n; i++) {
    const x = lerp(L.x0, L.x1, (i + 0.5) / L.n);
    BULBS.push({ L, x, k: k++, on: lerp(TL.lightsOn[0], TL.lightsOn[1], clamp((x + 40) / 2000)) + hash(k * 1.7) * 0.25 + (L.par > 0.9 ? 4.4 : 0) });
  }
}

// ---------- baked layers ----------
let SKY, TOWN, GLOW, AMBER, GRAIN, VIG, PETALS = [], PSPR = [];
const SKYH = H + Math.round(CAMMAX * 0.4);
function bakeSky() {
  SKY = mk(W, SKYH); const g = SKY.getContext('2d');
  const gr = g.createLinearGradient(0, 0, 0, SKYH);
  [[0, '#0b0a26'], [0.22, '#1d1646'], [0.38, '#3b2263'], [0.48, '#6e2f74'], [0.56, '#b24876'], [0.63, '#e67c56'], [0.7, '#f6ae62'], [1, '#fcd08a']].forEach(([o, c]) => gr.addColorStop(o, c));
  g.fillStyle = gr; g.fillRect(0, 0, W, SKYH);
  // thin dusk clouds catching the last light
  const r = mulberry(77);
  for (let i = 0; i < 26; i++) {
    const y = SKYH * (0.55 + r() * 0.3), x = r() * W, w = 200 + r() * 500;
    const cg = g.createLinearGradient(0, y - 8, 0, y + 8); cg.addColorStop(0, 'rgba(255,170,150,0)'); cg.addColorStop(0.5, `rgba(255,${150 + r() * 50 | 0},140,${0.08 + r() * 0.12})`); cg.addColorStop(1, 'rgba(255,170,150,0)');
    g.fillStyle = cg; g.beginPath(); g.ellipse(x, y, w, 5 + r() * 7, 0, 0, TAU); g.fill();
  }
}
const STARS = []; { const r = mulberry(5); for (let i = 0; i < 140; i++) STARS.push({ x: r() * W, y: r() * SKYH * 0.5, s: 0.6 + r() * 1.6, ph: r() * TAU, f: 0.5 + r() * 2 }); }

function bakeTown() {
  TOWN = mk(W, H); const g = TOWN.getContext('2d'); const r = mulberry(11);
  // distant rooftops in violet haze
  g.fillStyle = '#4a2a5e';
  let x = -20; g.beginPath(); g.moveTo(-20, H);
  while (x < W + 40) { const w = 60 + r() * 140, y = 640 + r() * 50; g.lineTo(x, y); g.lineTo(x + w, y); if (r() < 0.25) { g.lineTo(x + w, y - 26); g.lineTo(x + w + 30, y - 26); g.lineTo(x + w + 30, y); x += 30; } x += w; }
  g.lineTo(W + 40, H); g.closePath(); g.fill();
  const win = (x, y, w, h, a) => { const gg = g.createLinearGradient(0, y, 0, y + h); gg.addColorStop(0, `rgba(255,196,110,${a})`); gg.addColorStop(1, `rgba(255,140,60,${a})`); g.fillStyle = gg; g.fillRect(x, y, w, h); };
  for (let i = 0; i < 40; i++) if (r() < 0.5) win(r() * W, 660 + r() * 60, 6, 9, 0.35);
  // two arcaded colonial facades framing the plaza
  const facade = (x0, x1, top, col, seed) => {
    const rr = mulberry(seed);
    const fg = g.createLinearGradient(0, top, 0, 1000); fg.addColorStop(0, col); fg.addColorStop(1, '#1c0f25'); g.fillStyle = fg;
    g.beginPath(); g.moveTo(x0, 1000); g.lineTo(x0, top);
    // stepped parapet
    const n = Math.round((x1 - x0) / 120);
    for (let i = 0; i < n; i++) { const a = lerp(x0, x1, i / n), b = lerp(x0, x1, (i + 1) / n); g.lineTo(a, top); g.lineTo(a + (b - a) * 0.3, top); g.quadraticCurveTo((a + b) / 2, top - 22, a + (b - a) * 0.7, top); g.lineTo(b, top); }
    g.lineTo(x1, 1000); g.closePath(); g.fill();
    g.fillStyle = 'rgba(0,0,0,0.25)'; g.fillRect(x0, top + 28, x1 - x0, 6);
    // upper floor: tall shuttered windows and iron balconies
    const bays = Math.round((x1 - x0) / 118);
    for (let i = 0; i < bays; i++) {
      const cx = lerp(x0, x1, (i + 0.5) / bays), wy = top + 70, lit = rr() < 0.72;
      win(cx - 20, wy, 40, 86, lit ? 0.9 : 0.12);
      g.fillStyle = 'rgba(30,12,30,0.8)'; g.fillRect(cx - 1.5, wy, 3, 86); g.fillRect(cx - 20, wy + 30, 40, 2.5);
      g.fillStyle = '#1a0c20'; g.fillRect(cx - 30, wy - 8, 60, 8); g.fillRect(cx - 34, wy + 86, 68, 6);
      g.strokeStyle = '#1a0c20'; g.lineWidth = 2; g.strokeRect(cx - 32, wy + 62, 64, 24);
      g.beginPath(); for (let k = 1; k < 8; k++) { g.moveTo(cx - 32 + k * 8, wy + 62); g.lineTo(cx - 32 + k * 8, wy + 86); } g.stroke();
    }
    // ground-floor arcade (portales) glowing from the shops inside
    const ay = top + 190, arcs = Math.round((x1 - x0) / 106);
    g.fillStyle = 'rgba(20,8,24,0.55)'; g.fillRect(x0, ay - 8, x1 - x0, 8);
    for (let i = 0; i < arcs; i++) {
      const a = lerp(x0, x1, i / arcs) + 12, b = lerp(x0, x1, (i + 1) / arcs) - 12, m = (a + b) / 2, rad = (b - a) / 2;
      const ag = g.createLinearGradient(0, ay, 0, 1000); ag.addColorStop(0, 'rgba(255,170,90,0.55)'); ag.addColorStop(1, 'rgba(255,120,60,0.95)');
      g.fillStyle = ag; g.beginPath(); g.moveTo(a, 1000); g.lineTo(a, ay + rad); g.arc(m, ay + rad, rad, Math.PI, 0); g.lineTo(b, 1000); g.closePath(); g.fill();
      g.fillStyle = 'rgba(60,20,40,0.5)'; g.fillRect(m - rad * 0.55, ay + rad + 40, rad * 1.1, 1000 - ay - rad - 40);
    }
  };
  facade(-30, 660, 620, '#3a1f45', 21);
  facade(1270, 1960, 596, '#43203f', 22);
  // trimmed laurel trees flanking the bandstand
  const tree = (cx, cy, R) => {
    g.fillStyle = '#1a0f22'; g.fillRect(cx - 9, cy, 18, 1000 - cy);
    g.fillStyle = '#23142e'; g.beginPath(); for (let i = 0; i < 9; i++) { const a = i / 9 * TAU; g.moveTo(cx + Math.cos(a) * R * 0.55 + R * 0.5, cy - R * 0.45 + Math.sin(a) * R * 0.4); g.arc(cx + Math.cos(a) * R * 0.55, cy - R * 0.45 + Math.sin(a) * R * 0.4, R * 0.5, 0, TAU); } g.fill();
    const hg = g.createRadialGradient(cx, cy + 10, 0, cx, cy, R * 1.1); hg.addColorStop(0, 'rgba(255,150,80,0.22)'); hg.addColorStop(1, 'rgba(255,150,80,0)'); g.fillStyle = hg; g.fillRect(cx - R * 1.2, cy - R * 1.2, R * 2.4, R * 2.4);
  };
  tree(720, 820, 120); tree(1210, 812, 112); tree(470, 850, 90); tree(1480, 846, 92);
  // the bandstand (kiosco): platform, slim columns, railing, ogee roof with a ball finial
  const kx = 960;
  const kg = g.createRadialGradient(kx, 880, 10, kx, 880, 260); kg.addColorStop(0, 'rgba(255,190,110,0.55)'); kg.addColorStop(1, 'rgba(255,150,80,0)'); g.fillStyle = kg; g.fillRect(kx - 300, 640, 600, 380);
  g.fillStyle = '#1d0f24';
  g.fillRect(kx - 205, 928, 410, 44); g.fillRect(kx - 222, 918, 444, 12);
  for (let i = 0; i < 6; i++) { const cx = kx - 175 + i * 70; g.fillRect(cx - 4, 772, 8, 150); }
  g.fillRect(kx - 190, 872, 380, 5); g.fillRect(kx - 190, 912, 380, 5);
  for (let i = 0; i < 26; i++) g.fillRect(kx - 188 + i * 14.8, 876, 3, 38);
  g.beginPath(); g.moveTo(kx - 232, 780); g.lineTo(kx + 232, 780); g.lineTo(kx + 214, 764);
  g.bezierCurveTo(kx + 150, 750, kx + 60, 720, kx + 26, 672); g.lineTo(kx - 26, 672); g.bezierCurveTo(kx - 60, 720, kx - 150, 750, kx - 214, 764); g.closePath(); g.fill();
  g.fillRect(kx - 4, 640, 8, 34); g.beginPath(); g.arc(kx, 636, 11, 0, TAU); g.fill();
  g.fillStyle = 'rgba(255,190,110,0.55)'; for (let i = 0; i < 16; i++) { g.beginPath(); g.arc(kx - 216 + i * 28.8, 786, 3.2, 0, TAU); g.fill(); }
  // plaza paving in warm light
  const pg = g.createLinearGradient(0, 968, 0, H); pg.addColorStop(0, '#5a2d3e'); pg.addColorStop(1, '#2a1426'); g.fillStyle = pg; g.fillRect(0, 968, W, H - 968);
  g.strokeStyle = 'rgba(255,170,110,0.12)'; g.lineWidth = 1.5;
  for (let i = -12; i <= 12; i++) { g.beginPath(); g.moveTo(960 + i * 40, 968); g.lineTo(960 + i * 260, H); g.stroke(); }
  for (let j = 0; j < 5; j++) { const y = 968 + Math.pow(j / 5, 1.6) * 112 + 6; g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); }
  const lg = g.createRadialGradient(960, 990, 0, 960, 990, 700); lg.addColorStop(0, 'rgba(255,170,90,0.35)'); lg.addColorStop(1, 'rgba(255,170,90,0)'); g.fillStyle = lg; g.fillRect(0, 968, W, H - 968);
}
function bakeSprites() {
  GLOW = mk(128, 128); { const g = GLOW.getContext('2d'); const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(255,236,190,1)'); gr.addColorStop(0.12, 'rgba(255,214,140,0.7)'); gr.addColorStop(0.4, 'rgba(255,160,70,0.18)'); gr.addColorStop(1, 'rgba(255,140,60,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); }
  AMBER = mk(128, 128); { const g = AMBER.getContext('2d'); const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(255,190,80,1)'); gr.addColorStop(0.5, 'rgba(255,140,40,0.55)'); gr.addColorStop(1, 'rgba(255,110,30,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); }
  // marigold petals: small ruffled wedges in orange and gold
  const cols = [['#ff9a1f', '#ffc24a'], ['#f47a12', '#ffb03a'], ['#ffb81f', '#ffe07a'], ['#e8600e', '#ff9a3a']];
  for (let k = 0; k < 8; k++) {
    const c = mk(48, 48), g = c.getContext('2d'), r = mulberry(300 + k), [a, b] = cols[k % 4];
    g.translate(24, 24); g.rotate(r() * TAU);
    const gr = g.createLinearGradient(-14, 0, 14, 0); gr.addColorStop(0, a); gr.addColorStop(1, b); g.fillStyle = gr;
    g.beginPath(); g.moveTo(0, 16);
    const n = 5 + (r() * 3 | 0); for (let i = 0; i <= n; i++) { const an = Math.PI + i / n * Math.PI, rr = 12 + r() * 5; g.lineTo(Math.cos(an) * rr * 0.9, Math.sin(an) * rr - 2); }
    g.closePath(); g.fill();
    g.strokeStyle = 'rgba(150,50,0,0.35)'; g.lineWidth = 1; for (let i = -1; i <= 1; i++) { g.beginPath(); g.moveTo(0, 14); g.lineTo(i * 6, -8); g.stroke(); }
    PSPR.push(c);
  }
  // static film grain + vignette
  GRAIN = mk(W / 2, H / 2); { const g = GRAIN.getContext('2d'), im = g.createImageData(W / 2, H / 2), r = mulberry(9); for (let i = 0; i < im.data.length; i += 4) { const v = r() * 255; im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 16; } g.putImageData(im, 0, 0); }
  VIG = mk(W, H); { const g = VIG.getContext('2d'); const gr = g.createRadialGradient(W / 2, H * 0.48, H * 0.35, W / 2, H / 2, H * 1.05); gr.addColorStop(0, 'rgba(10,4,20,0)'); gr.addColorStop(1, 'rgba(10,4,20,0.55)'); g.fillStyle = gr; g.fillRect(0, 0, W, H); }
}
function initPetals() {
  const r = mulberry(41);
  for (let i = 0; i < 190; i++) {
    const gust = i < 70; // a burst loosened by the gust, then a steady drift
    const t0 = gust ? 3.25 + r() * 1.9 : 2.2 + r() * 7.6;
    const near = r() < 0.3;
    PETALS.push({ t0, x0: -150 + r() * 1900, par: near ? 1.35 : 0.8 + r() * 0.35, s: near ? 1.1 + r() * 0.6 : 0.55 + r() * 0.45, v: 120 + r() * 110, dr: 50 + r() * 130, sw: 20 + r() * 40, f: 0.8 + r() * 1.6, spin: 2 + r() * 5, ph: r() * TAU, k: i % 8, near });
  }
}

// ---------- per-frame ----------
const bulbLevel = (b, t) => {
  const on = eOut(seg(t, b.on, b.on + 0.18)), flick = on < 1 && on > 0 ? 0.6 + 0.4 * Math.sin(t * 90 + b.k) : 1;
  const breathe = 0.88 + 0.12 * Math.sin(t * 2.3 + b.k * 1.3);
  const flare = 0.55 * Math.exp(-Math.pow((t - 4.55) / 0.45, 2)) * (b.L.par < 0.9 ? 1 : 0);
  const wave = 0.9 * Math.exp(-Math.pow((t - TL.twinkle - b.x / 1900 * 0.9) / 0.12, 2)) * (b.L.par >= 1 ? 1 : 0);
  const spark = hash(b.k * 3.3 + Math.floor(t * 7)) > 0.93 ? 0.35 : 0;
  const out = 1 - eIn(seg(t, TL.end[0] + 0.2 + (1 - b.x / 1920) * 0.4, DUR - 0.1)) * 0.9;
  return on * flick * (breathe + flare + wave + spark * seg(t, 7, 8)) * out;
};
function drawLights(g, L, t, c) {
  const dy = c * L.par;
  if (L.y + dy > H + 100 || L.y + L.sag + dy < -100) return;
  g.strokeStyle = 'rgba(20,10,20,0.85)'; g.lineWidth = 1.6 * (L.par + 0.3); g.beginPath();
  for (let x = L.x0 - 40; x <= L.x1 + 40; x += 20) { const y = catY(L, x) + dy; x === L.x0 - 40 ? g.moveTo(x, y) : g.lineTo(x, y); } g.stroke();
  const bl = BULBS.filter(b => b.L === L);
  for (const b of bl) {
    const y = catY(L, b.x) + dy + L.r * 1.6, lv = bulbLevel(b, t);
    g.fillStyle = '#2a1a1e'; g.fillRect(b.x - L.r * 0.5, y - L.r * 2.2, L.r, L.r * 1.2);
    g.fillStyle = `rgb(${lerp(90, 255, clamp(lv)) | 0},${lerp(60, 238, clamp(lv)) | 0},${lerp(50, 196, clamp(lv)) | 0})`;
    g.beginPath(); g.ellipse(b.x, y, L.r * 0.8, L.r, 0, 0, TAU); g.fill();
  }
  g.globalCompositeOperation = 'lighter';
  for (const b of bl) { const y = catY(L, b.x) + dy + L.r * 1.6, lv = bulbLevel(b, t); if (lv < 0.02) continue; const R = L.r * 12 * (0.7 + 0.5 * lv); g.globalAlpha = clamp(lv * L.g, 0, 1); g.drawImage(GLOW, b.x - R, y - R, R * 2, R * 2); }
  g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';
}
function bannerState(bn, t, c, extraLit) {
  const S = bn.S, u = seg(t, bn.t0, bn.t0 + 0.62), after = t - (bn.t0 + 0.62);
  const len = eOut(u);
  const stretch = after > 0 ? 1 + 0.06 * Math.exp(-after * 5) * Math.sin(after * 17) : 1;
  const tw = t - bn.x / 1900 * 0.55; // the gust travels left to right
  const Wd = windRaw(tw), wp = windPhase(tw) + bn.ph;
  const kick = after > 0 ? 0.5 * Math.exp(-after * 3.2) * Math.sin(after * 9) : 0.25 * u;
  const swing = kick + Wd * (0.42 + 0.3 * Math.sin(wp * 0.8 + bn.ph)) + 0.05 * Math.sin(wp * 2.1);
  const sway = Wd * 0.28 * Math.sin(wp * 0.6 + bn.ph * 2) + 0.05 * Math.sin(wp * 1.3);
  const ripple = 0.18 + Wd * 0.75;
  const glow = 0.5 * Math.exp(-Math.pow((t - 4.6) / 0.55, 2));
  return { s: S.s, rot: Math.atan(catSlope(S, bn.x)) * 0.8 + 0.03 * Math.sin(wp * 0.9), len, stretch, swing, sway, ripple, ph: bn.ph, wt: wp, lit: 0.08 + glow * (S.par < 1.2 ? 1 : 0.6) + extraLit, alpha: 0.9 };
}
function nearLit(x, y, par, t, c) {
  let s = 0;
  for (const b of BULBS) { if (b.L.par >= par || b.L.par < par - 0.4) continue; const by = catY(b.L, b.x) + c * b.L.par, d2 = (b.x - x) ** 2 + (by - y) ** 2; s += Math.exp(-d2 / 9000) * bulbLevel(b, t); }
  return clamp(s * 0.6, 0, 0.7);
}
function drawString(g, S, list, t, c, extra) {
  const dy = c * S.par;
  if (S.y + dy > H + 60 || S.y + S.sag + dy + 420 * S.s < -60) return;
  g.strokeStyle = 'rgba(245,230,210,0.75)'; g.lineWidth = 1.4 * S.s + 0.6; g.beginPath();
  for (let x = -60; x <= 1980; x += 20) { const y = catY(S, x) + dy; x === -60 ? g.moveTo(x, y) : g.lineTo(x, y); } g.stroke();
  for (const bn of list) {
    const y = catY(S, bn.x) + dy - 3 * S.s;
    const st = bannerState(bn, t, c, (extra ? extra(bn, t) : 0) + nearLit(bn.x, y + 150 * S.s, S.par, t, c));
    drawBanner(g, bn.B, bn.x, y, st);
  }
}
function drawPetals(g, t, c, near) {
  for (const p of PETALS) {
    if (p.near !== near) continue; const a = t - p.t0; if (a < 0) continue;
    const c0 = cam(p.t0);
    const y = -40 - c0 * p.par + p.v * a + c * p.par; if (y > H + 40) continue;
    const x = p.x0 + p.dr * a + p.sw * Math.sin(a * p.f + p.ph) + 60 * (windRaw(t) - 0.22) * a * 0.5;
    const sp = PSPR[p.k], sc = p.s, fl = Math.cos(a * p.spin + p.ph);
    g.save(); g.translate(x, y); g.rotate(a * p.spin * 0.4 + p.ph); g.scale(sc * (0.25 + 0.75 * Math.abs(fl)), sc);
    g.globalAlpha = (fl > 0 ? 1 : 0.8) * clamp(a * 3); g.drawImage(sp, -24, -24); g.restore();
  }
  g.globalAlpha = 1;
}
function drawCaption(g, t, c) {
  const u = seg(t, TL.caption, TL.caption + 0.8); if (u <= 0) return;
  const y = TSTR.y + c + 452 - 14 * (1 - eOut(u));
  g.save(); g.globalAlpha = eOut(u) * (1 - seg(t, TL.end[0] + 0.3, DUR - 0.15));
  g.font = FCAP; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = '#ffe9c4';
  g.letterSpacing = '9px'; g.shadowColor = 'rgba(255,150,70,0.55)'; g.shadowBlur = 16;
  g.fillText(CAPTION, 960, y); g.shadowBlur = 0;
  const w = g.measureText(CAPTION).width / 2 + 30, wl = 110 * eOut(seg(t, TL.caption + 0.2, TL.caption + 1));
  g.strokeStyle = '#ffc27a'; g.lineWidth = 2;
  g.beginPath(); g.moveTo(960 - w, y); g.lineTo(960 - w - wl, y); g.moveTo(960 + w, y); g.lineTo(960 + w + wl, y); g.stroke();
  g.fillStyle = '#ffc27a'; for (const sx of [-1, 1]) { g.beginPath(); diamond(g, 960 + sx * (w + wl + 12), y, 7, 7); g.fill(); }
  g.restore();
}
function drawFrame(t) {
  const g = ctx, c = cam(t);
  g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';
  g.drawImage(SKY, 0, -(SKYH - H) + c * 0.4);
  for (const s of STARS) { const y = s.y - (SKYH - H) + c * 0.4; if (y < -5 || y > H) continue; const a = (0.25 + 0.3 * seg(y, 600, 0)) * (0.6 + 0.4 * Math.sin(t * s.f + s.ph)) * seg(t, 0.5, 2.5); g.fillStyle = `rgba(255,240,220,${a})`; g.fillRect(s.x, y, s.s, s.s); }
  g.drawImage(TOWN, 0, c * 0.45);
  drawLights(g, LSTR[0], t, c); drawLights(g, LSTR[1], t, c);
  drawString(g, BSTR[0], BANNERS.filter(b => b.S === BSTR[0]), t, c);
  drawLights(g, LSTR[2], t, c);
  drawString(g, BSTR[1], BANNERS.filter(b => b.S === BSTR[1]), t, c);
  drawLights(g, LSTR[3], t, c); drawLights(g, LSTR[4], t, c);
  // lamps behind the title string: once the letters hang, warm light pours through the cut letters
  g.globalCompositeOperation = 'lighter';
  for (const bn of TITLEB) {
    const k = 0.1 * seg(t, bn.t0 + 0.3, bn.t0 + 1.1) + 0.55 * Math.exp(-Math.pow((t - TL.twinkle - bn.x / 1900 * 0.9) / 0.2, 2));
    const out = 1 - seg(t, TL.end[0] + 0.2, DUR - 0.2); if (k * out < 0.01) continue;
    const y = catY(TSTR, bn.x) + c + 160, R = 150; g.globalAlpha = clamp(k * out); g.drawImage(AMBER, bn.x - R, y - R, R * 2, R * 2);
  }
  g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';
  // letters: a travelling shimmer of light through each sheet as the lamps twinkle
  drawString(g, TSTR, TITLEB, t, c, (bn, t) => 0.25 * seg(t, bn.t0 + 0.4, bn.t0 + 1.2) + 0.55 * Math.exp(-Math.pow((t - TL.twinkle - bn.x / 1900 * 0.9) / 0.16, 2)));
  drawPetals(g, t, c, false);
  drawCaption(g, t, c);
  drawString(g, BSTR[2], BANNERS.filter(b => b.S === BSTR[2]), t, c);
  drawPetals(g, t, c, true);
  g.drawImage(VIG, 0, 0); g.drawImage(GRAIN, 0, 0, W, H);
  // open from dusk darkness, close by dimming to night
  const dark = Math.max(1 - eOut(seg(t, 0, 0.9)), eInOut(seg(t, TL.end[0] + 0.1, DUR - 0.08)));
  if (dark > 0) { g.fillStyle = `rgba(6,3,14,${dark})`; g.fillRect(0, 0, W, H); }
}
window.events = () => {
  const ev = [];
  for (const b of BULBS) if (b.L.par < 0.9) ev.push({ k: 'bulb', t: b.on, pan: (b.x - 960) / 960 });
  for (const bn of BANNERS) ev.push({ k: 'unfurl', t: bn.t0, pan: (bn.x - 960) / 960, s: bn.S.s });
  ev.push({ k: 'gust', t: TL.gust }, { k: 'glow', t: 4.3 }, { k: 'tilt', t: TL.tilt[0], d: TL.tilt[1] - TL.tilt[0] });
  for (const bn of TITLEB) ev.push({ k: 'title', t: bn.t0, pan: (bn.x - 960) / 960, i: bn.i });
  ev.push({ k: 'caption', t: TL.caption }, { k: 'twinkle', t: TL.twinkle }, { k: 'end', t: TL.end[0] });
  return ev.sort((a, b) => a.t - b.t);
};
window.ready = (async () => {
  await document.fonts.load(FTITLE, TITLE.join('')); await document.fonts.load(FCAP, CAPTION); await document.fonts.ready;
  bakeSky(); bakeTown(); bakeSprites(); initStrings(); initPetals();
})();
window.draw = ({ t }) => { drawFrame(t); return cv.toDataURL('image/jpeg', 0.92).split(',')[1]; };
