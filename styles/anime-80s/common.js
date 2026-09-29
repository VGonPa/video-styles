// ── anime-80s · shared helpers: math, seeded rng, palette, cel/paint primitives, film finish ──
const W = 1920, H = 1080, DUR = 10.0, TAU = Math.PI * 2;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eOut = u => 1 - Math.pow(1 - u, 3);
const eIn = u => u * u * u;
const eInOut = u => u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
const sstep = u => u * u * (3 - 2 * u);
const eBack = u => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(u - 1, 3) + c1 * Math.pow(u - 1, 2); };
const bump = (t, a, b) => Math.sin(Math.PI * seg(t, a, b));
const cel = (t, fps = 12) => Math.floor(t * fps + 1e-6) / fps;      // held-cel time (animation on 2s/3s)
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const mk = (w = W, h = H) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
const hx = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
const rgba = (c, a = 1) => { c = typeof c === 'string' ? hx(c) : c; return `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a})`; };
const mixc = (a, b, u) => { a = typeof a === 'string' ? hx(a) : a; b = typeof b === 'string' ? hx(b) : b; return [lerp(a[0], b[0], u), lerp(a[1], b[1], u), lerp(a[2], b[2], u)]; };

// 80s cel palette: amber / magenta / dusty teal, plum ink line
const P = {
  ink: '#2a1328', skyTop: '#2c2455', skyMid: '#7c3a7a', skyPink: '#e2657c', skyAmber: '#f6a45a', skyGlow: '#ffdb9c',
  sun: '#fff3c8', sunRim: '#ffb46a', cloudShade: '#6c3a70', cloudMid: '#b44f80', cloudLit: '#f79a72', cloudHot: '#ffd08c',
  sea0: '#3a6e80', sea1: '#244a62', sea2: '#172f48', teal: '#4f8c95', tealDk: '#2d5563',
  red: '#d42a3e', redDk: '#8c1a3c', redHi: '#ff7a64', chrome: '#ffe6c4',
  night0: '#0d0c26', night1: '#1f1846', night2: '#3b2458',
};

// cel fill + ink line for a path builder fn(g)
function celShape(g, build, fill, line = P.ink, lw = 3) {
  g.beginPath(); build(g); g.fillStyle = fill; g.fill();
  if (line) { g.lineWidth = lw; g.strokeStyle = line; g.lineJoin = 'round'; g.lineCap = 'round'; g.stroke(); }
}
// clipped shade/highlight inside a previously built path
function celClip(g, build, inner) { g.save(); g.beginPath(); build(g); g.clip(); inner(g); g.restore(); }

// painted brush dabs (hand-painted background texture)
function dabs(g, R, n, x0, y0, x1, y1, cols, len = 40, wid = 8, ang = 0, alpha = .18, angJ = .25) {
  for (let i = 0; i < n; i++) {
    const x = lerp(x0, x1, R()), y = lerp(y0, y1, R());
    g.save(); g.translate(x, y); g.rotate(ang + (R() - .5) * angJ);
    g.globalAlpha = alpha * (.4 + .6 * R()); g.fillStyle = cols[(R() * cols.length) | 0];
    const l = len * (.5 + R()), w = wid * (.5 + R());
    g.beginPath(); g.ellipse(0, 0, l / 2, w / 2, 0, 0, TAU); g.fill(); g.restore();
  }
  g.globalAlpha = 1;
}

// cel-shaded cumulus bank lit from below (sunset): shade body, lit underside rim, hot core, brushy dabs
function cloudBank(g, R, cx, cy, wid, hgt, lit = 1, cols = {}) {
  const puffs = [], fb = cy + hgt * .12;
  const n = Math.round(wid / 48);
  for (let i = 0; i < n; i++) {
    const u = i / (n - 1), x = cx - wid / 2 + u * wid + (R() - .5) * 30;
    const prof = Math.sin(Math.PI * (.08 + u * .84)) ** .8;
    const r = hgt * (.22 + R() * .18) * (.55 + .45 * prof);
    puffs.push([x, fb - r * .7 - prof * hgt * .35 * (.6 + .4 * R()), r]);
  }
  for (let i = 0; i < n * .8; i++) { const [x, y, r] = puffs[1 + ((R() * (n - 2)) | 0)]; const rr = r * (.6 + .35 * R()); puffs.push([x + (R() - .5) * r * 1.2, y - r * (.35 + .5 * R()), rr]); }
  const body = gg => { for (const [x, y, r] of puffs) { gg.moveTo(x + r, y); gg.arc(x, y, r, 0, TAU); } gg.rect(cx - wid / 2 - 10, cy - 2, wid + 20, 0); };
  const flatBase = cy + hgt * .12;
  g.save(); g.beginPath(); g.rect(cx - wid, 0, wid * 2, flatBase); g.clip();
  g.beginPath(); body(g); g.fillStyle = cols.shade || P.cloudShade; g.fill();
  g.save(); g.beginPath(); body(g); g.clip();
  // mid tone band and lit underside, offset toward the low sun
  g.beginPath(); for (const [x, y, r] of puffs) { g.moveTo(x + r * .95, y + r * .32); g.arc(x, y + r * .32, r * .95, 0, TAU); }
  g.fillStyle = cols.mid || P.cloudMid; g.fill();
  g.globalAlpha = lit;
  g.beginPath(); g.rect(cx - wid, flatBase - hgt * .3, wid * 2, hgt);
  g.fillStyle = cols.lit || P.cloudLit; g.fill();
  g.beginPath(); g.rect(cx - wid, flatBase - hgt * .1, wid * 2, hgt);
  g.fillStyle = cols.hot || P.cloudHot; g.fill();
  g.globalAlpha = 1;
  dabs(g, R, wid * .5, cx - wid / 2, cy - hgt, cx + wid / 2, flatBase, [cols.shade || P.cloudShade, cols.mid || P.cloudMid, cols.lit || P.cloudLit], 60, 10, 0, .12, .3);
  g.restore(); g.restore();
}

// film finish: color bleed, bloom, grain, dust, vignette
const FX = {};
function initFX() {
  const R = rng(99);
  FX.grain = [];
  for (let k = 0; k < 6; k++) {
    const c = mk(960, 540), g = c.getContext('2d'), id = g.createImageData(960, 540), d = id.data;
    for (let i = 0; i < d.length; i += 4) { const v = 128 + (R() + R() + R() - 1.5) * 90; d[i] = d[i + 1] = d[i + 2] = v; d[i + 3] = 255; }
    g.putImageData(id, 0, 0); FX.grain.push(c);
  }
  const v = mk(), g = v.getContext('2d');
  const rg = g.createRadialGradient(W / 2, H / 2, H * .35, W / 2, H / 2, H * 1.05);
  rg.addColorStop(0, 'rgba(20,6,24,0)'); rg.addColorStop(1, 'rgba(20,6,24,.55)');
  g.fillStyle = rg; g.fillRect(0, 0, W, H); FX.vig = v;
  FX.small = mk(480, 270); FX.small2 = mk(480, 270); FX.bleed = mk();
}
function finish(out, src, t, o = {}) {
  const g = out.getContext('2d');
  const tc = cel(t, 12), R = rng(1 + Math.round(tc * 12) * 7919);
  // gate weave (held at 12 fps like the projected cels)
  const wx = (R() - .5) * 2.4, wy = (R() - .5) * 2.4;
  g.fillStyle = '#000'; g.fillRect(0, 0, W, H);
  g.drawImage(src, wx - 2, wy - 2, W + 4, H + 4);
  // colour bleed: warm channel smears right a few px
  const b = FX.bleed.getContext('2d');
  b.globalCompositeOperation = 'copy'; b.drawImage(out, 0, 0);
  b.globalCompositeOperation = 'multiply'; b.fillStyle = '#ff5a3c'; b.fillRect(0, 0, W, H);
  b.globalCompositeOperation = 'source-over';
  g.globalCompositeOperation = 'lighten'; g.globalAlpha = .35; g.drawImage(FX.bleed, 5, 0); g.globalAlpha = 1;
  // bloom
  const s = FX.small.getContext('2d'), s2 = FX.small2.getContext('2d');
  s.globalCompositeOperation = 'copy'; s.filter = 'none'; s.drawImage(out, 0, 0, 480, 270);
  s2.globalCompositeOperation = 'copy'; s2.filter = 'blur(10px) brightness(1.1)'; s2.drawImage(FX.small, 0, 0); s2.filter = 'none';
  g.globalCompositeOperation = 'screen'; g.globalAlpha = o.bloom ?? .32; g.drawImage(FX.small2, 0, 0, W, H);
  // grain (refreshed at 12 fps) + vignette
  g.globalCompositeOperation = 'overlay'; g.globalAlpha = o.grain ?? .16;
  const gi = Math.round(tc * 12) % FX.grain.length;
  g.drawImage(FX.grain[gi], (gi * 37) % 20 - 20, 0, W + 20, H);
  g.globalCompositeOperation = 'source-over'; g.globalAlpha = 1;
  g.drawImage(FX.vig, 0, 0);
  // dust and hair specks on the cel
  const nd = (R() * 4) | 0;
  for (let i = 0; i < nd; i++) {
    g.fillStyle = R() < .5 ? 'rgba(255,245,225,.55)' : 'rgba(25,8,20,.5)';
    const x = R() * W, y = R() * H;
    if (R() < .7) { g.beginPath(); g.arc(x, y, 1 + R() * 2.5, 0, TAU); g.fill(); }
    else { g.strokeStyle = g.fillStyle; g.lineWidth = 1.2; g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + 20 * R(), y + 14, x + 30 * (R() - .3), y + 26 * R()); g.stroke(); }
  }
  if (o.fade > 0) { g.fillStyle = `rgba(0,0,0,${o.fade})`; g.fillRect(0, 0, W, H); }
}

// lens flare: streak + ghosts along the axis through screen centre
function flare(g, x, y, k, col = [255, 190, 120]) {
  if (k <= 0) return;
  g.save(); g.globalCompositeOperation = 'lighter';
  let rg = g.createRadialGradient(x, y, 0, x, y, 260 * k);
  rg.addColorStop(0, rgba([255, 250, 230], .9 * k)); rg.addColorStop(.25, rgba(col, .35 * k)); rg.addColorStop(1, rgba(col, 0));
  g.fillStyle = rg; g.fillRect(x - 300, y - 300, 600, 600);
  const sg = g.createLinearGradient(x - 900, 0, x + 900, 0);
  sg.addColorStop(0, rgba(col, 0)); sg.addColorStop(.5, rgba([255, 235, 210], .55 * k)); sg.addColorStop(1, rgba(col, 0));
  g.fillStyle = sg; g.fillRect(x - 900, y - 3 * k, 1800, 6 * k);
  const dx = W / 2 - x, dy = H / 2 - y;
  const ghosts = [[.5, 38, [120, 220, 210]], [.8, 22, [255, 120, 180]], [1.25, 64, [255, 180, 110]], [1.6, 30, [140, 200, 255]], [1.9, 90, [255, 110, 160]]];
  for (const [f, r, c] of ghosts) {
    const gx = x + dx * f * 2, gy = y + dy * f * 2;
    const q = g.createRadialGradient(gx, gy, r * .6, gx, gy, r);
    q.addColorStop(0, rgba(c, .10 * k)); q.addColorStop(.85, rgba(c, .16 * k)); q.addColorStop(1, rgba(c, 0));
    g.fillStyle = q; g.beginPath(); g.arc(gx, gy, r, 0, TAU); g.fill();
  }
  g.restore();
}
