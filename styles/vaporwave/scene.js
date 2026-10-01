// Vaporwave scene layer: 2D scene composition, VHS/glitch post pass, draw loop and audio events.
// Relies on globals from anim.html (timeline T, helpers, renderBust/renderOrb, glc).

const cA = mk(W, H), xA = cA.getContext('2d');
const cB = mk(W, H), xB = cB.getContext('2d');
const cCA = mk(W, H), xCA = cCA.getContext('2d');
const cCB = mk(W, H), xCB = cCB.getContext('2d');
const cWin = mk(460, 250), xWin = cWin.getContext('2d');
const FONT_SERIF = "'DM Serif Display'", FONT_PIX = "'VT323'", FONT_SANS = "'Montserrat'";

// ---------- helpers ----------
const loadImg = src => new Promise(res => { const im = new Image(); im.onload = () => res(im); im.src = src; });
// real low-quality JPEG round trip at reduced size → blocky compression artifacts
async function crunch(src, dst, dw, dh, q, sx = 0, sy = 0, sw = src.width, sh = src.height) {
  const s = mk(dw, dh), c = s.getContext('2d'); c.drawImage(src, sx, sy, sw, sh, 0, 0, dw, dh);
  const im = await loadImg(s.toDataURL('image/jpeg', q)); return im;
}
function vgrad(ctx, y0, y1, stops) { const g = ctx.createLinearGradient(0, y0, 0, y1); stops.forEach(([o, c]) => g.addColorStop(o, c)); return g; }

// ---------- precomputed skies (low-res, JPEG crunched once) ----------
let skyA, skyB;
async function buildSkies() {
  const mkSky = (stops, clouds, seed) => {
    const w = 480, h = 270, c = mk(w, h), x = c.getContext('2d');
    x.fillStyle = vgrad(x, 0, h, stops); x.fillRect(0, 0, w, h);
    const r = rng(seed);
    for (let i = 0; i < clouds.n; i++) {
      const cx = r() * w, cy = clouds.y0 + r() * (clouds.y1 - clouds.y0), rw = 30 + r() * 60, rh = 6 + r() * 10;
      for (let k = 0; k < 5; k++) {
        const g = x.createRadialGradient(cx + (k - 2) * rw * .35, cy - (k % 2) * rh * .6, 0, cx + (k - 2) * rw * .35, cy - (k % 2) * rh * .6, rw * .6);
        g.addColorStop(0, clouds.col); g.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = g;
        x.beginPath(); x.ellipse(cx + (k - 2) * rw * .35, cy - (k % 2) * rh * .6, rw * .6, rh * 1.4, 0, 0, 7); x.fill();
      }
    }
    return c;
  };
  const a = mkSky([[0, '#a896e6'], [.45, '#e7a6dc'], [.72, '#ffc3d6'], [.85, '#ffd9c8'], [1, '#ffe6d6']], { n: 14, y0: 30, y1: 150, col: 'rgba(255,245,252,.55)' }, 7);
  const b = mkSky([[0, '#2a1f5e'], [.35, '#5a3a94'], [.62, '#c867b5'], [.8, '#ff9cb8'], [.9, '#ffc4a8'], [1, '#ffd8b8']], { n: 9, y0: 60, y1: 140, col: 'rgba(255,170,210,.35)' }, 21);
  skyA = await crunch(a, null, 480, 270, 0.32);
  skyB = await crunch(b, null, 480, 270, 0.32);
}

// ---------- perspective checkerboard floor ----------
function drawFloor(ctx, y0, scroll, colA, colB, haze, zmax = 26) {
  const f = 700, h = 1;
  ctx.fillStyle = colA; ctx.fillRect(0, y0, W, H - y0);
  ctx.fillStyle = colB;
  const fr = scroll - Math.floor(scroll), base = Math.floor(scroll);
  ctx.beginPath();
  for (let k = zmax; k >= 0; k--) {
    let zn = k + 1 - fr, zf = k + 2 - fr; if (zn < 0.9) zn = 0.9;
    const syn = y0 + f * h / zn, syf = y0 + f * h / zf;
    const xr = Math.ceil(980 * zn / f) + 1;
    for (let j = -xr; j < xr; j++) {
      if (((j + k + base) & 1) === 0) continue;
      const sx = (X, Z) => 960 + f * X / Z;
      ctx.moveTo(sx(j, zn), syn); ctx.lineTo(sx(j + 1, zn), syn); ctx.lineTo(sx(j + 1, zf), syf); ctx.lineTo(sx(j, zf), syf); ctx.closePath();
    }
  }
  ctx.fill();
  const g = ctx.createLinearGradient(0, y0, 0, y0 + 200);
  g.addColorStop(0, haze); g.addColorStop(1, haze.replace(/[\d.]+\)$/, '0)'));
  ctx.fillStyle = g; ctx.fillRect(0, y0 - 1, W, 201);
}

// ---------- palm tree silhouette ----------
function drawPalm(ctx, x, y, hgt, lean, sway, col, seed) {
  const r = rng(seed);
  const tx = x + lean * hgt + sway * 14, ty = y - hgt;
  const cx = x + lean * hgt * .2, cy = y - hgt * .55;
  const P = u => [(1 - u) * (1 - u) * x + 2 * (1 - u) * u * cx + u * u * tx, (1 - u) * (1 - u) * y + 2 * (1 - u) * u * cy + u * u * ty];
  ctx.fillStyle = col;
  // trunk: one tapered polygon with ring marks
  const N = 24, Lp = [], Rp = [];
  for (let i = 0; i <= N; i++) {
    const u = i / N, [px, py] = P(u), [qx, qy] = P(Math.min(1, u + .01)), [rx, ry] = P(Math.max(0, u - .01));
    const dx = qx - rx, dy = qy - ry, dl = Math.hypot(dx, dy) || 1, w = lerp(30, 15, u);
    const nx = -dy / dl, ny = dx / dl;
    Lp.push([px - nx * w, py - ny * w]); Rp.push([px + nx * w, py + ny * w]);
  }
  ctx.beginPath(); Lp.forEach(([a, b], i) => i ? ctx.lineTo(a, b) : ctx.moveTo(a, b)); [...Rp].reverse().forEach(([a, b]) => ctx.lineTo(a, b)); ctx.closePath(); ctx.fill();
  ctx.strokeStyle = 'rgba(255,255,255,.13)'; ctx.lineWidth = 3;
  for (let i = 1; i < N; i++) { ctx.beginPath(); ctx.moveTo(Lp[i][0], Lp[i][1]); ctx.lineTo(Rp[i][0], Rp[i][1] - 5); ctx.stroke(); }
  // fronds: drooping arcs with leaflets
  const fronds = 9;
  for (let i = 0; i < fronds; i++) {
    const a = -Math.PI / 2 + (i / (fronds - 1) - .5) * 3.4 + (r() - .5) * .2 + sway * .05;
    const L = hgt * (.36 + r() * .12), droop = .75 + r() * .35;
    const pt = u => [tx + Math.cos(a) * L * u, ty + Math.sin(a) * L * u + droop * L * u * u * .55];
    ctx.lineWidth = 7; ctx.strokeStyle = col; ctx.lineCap = 'round';
    ctx.beginPath(); for (let k = 0; k <= 16; k++) { const [px, py] = pt(k / 16); k ? ctx.lineTo(px, py) : ctx.moveTo(px, py); } ctx.stroke();
    ctx.lineWidth = 5;
    for (let k = 2; k <= 15; k++) {
      const u = k / 16, [px, py] = pt(u), [qx, qy] = pt(u + .02), dx = qx - px, dy = qy - py, dl = Math.hypot(dx, dy);
      const nx = -dy / dl, ny = dx / dl, ll = L * .2 * Math.sin(Math.PI * u) + 6;
      for (const s of [-1, 1]) {
        ctx.beginPath(); ctx.moveTo(px, py);
        ctx.quadraticCurveTo(px + nx * s * ll * .6 + dx / dl * ll * .3, py + ny * s * ll * .6 + dy / dl * ll * .3 + 4, px + nx * s * ll + dx / dl * ll * .5, py + ny * s * ll + dy / dl * ll * .5 + ll * .45);
        ctx.stroke();
      }
    }
  }
  ctx.beginPath(); ctx.arc(tx, ty + 4, 16, 0, 7); ctx.fill();
}

// ---------- distant colonnade ----------
function drawColonnade(ctx, x0, x1, yb, hgt, col, n) {
  ctx.fillStyle = col;
  const step = (x1 - x0) / (n - 1), cw = hgt * .11;
  ctx.fillRect(x0 - cw * 2, yb - 12, x1 - x0 + cw * 4, 12);                   // stylobate
  for (let i = 0; i < n; i++) {
    const cx = x0 + i * step, broken = i === 1 || i === n - 2;
    const top = broken ? yb - hgt * .62 : yb - hgt;
    ctx.fillRect(cx - cw / 2, top, cw, yb - 12 - top);
    if (!broken) { ctx.fillRect(cx - cw * .8, top - 10, cw * 1.6, 10); }
    else { ctx.beginPath(); ctx.moveTo(cx - cw / 2, top); ctx.lineTo(cx - cw * .1, top - 16); ctx.lineTo(cx + cw * .2, top - 6); ctx.lineTo(cx + cw / 2, top - 12); ctx.lineTo(cx + cw / 2, top); ctx.fill(); }
  }
  // lintel over the central span only (ruin)
  const ly = yb - hgt - 10;
  ctx.fillRect(x0 + step * 2 - cw, ly - 26, step * (n - 5) + cw * 2, 26);
  ctx.beginPath(); ctx.moveTo(x0 + step * 2 - cw, ly - 26); ctx.lineTo(x0 + step * (n - 1) / 2, ly - 70); ctx.lineTo(x0 + step * (n - 3) + cw, ly - 26); ctx.fill();
}

// ---------- 95-style window ----------
function bevel(ctx, x, y, w, h, inset) {
  const lt = inset ? '#4a3f66' : '#ffffff', dk = inset ? '#ffffff' : '#4a3f66', md = inset ? '#8e86ab' : '#a59dc2';
  ctx.fillStyle = lt; ctx.fillRect(x, y, w, 2); ctx.fillRect(x, y, 2, h);
  ctx.fillStyle = dk; ctx.fillRect(x, y + h - 2, w, 2); ctx.fillRect(x + w - 2, y, 2, h);
  ctx.fillStyle = md; ctx.fillRect(x + 2, y + h - 4, w - 4, 2); ctx.fillRect(x + w - 4, y + 2, 2, h - 4);
}
function drawWindow(ctx, x, y, w, h, title, pop, body) {
  if (pop <= 0) return;
  const s = lerp(.55, 1, backOut(pop, 2.2)), a = clamp(pop * 3);
  ctx.save(); ctx.globalAlpha = a;
  ctx.translate(x + w / 2, y + h / 2); ctx.scale(s, s); ctx.translate(-w / 2, -h / 2);
  ctx.fillStyle = 'rgba(58,30,96,.30)'; ctx.fillRect(12, 12, w, h);             // hard drop shadow
  ctx.fillStyle = '#dcd6ec'; ctx.fillRect(0, 0, w, h); bevel(ctx, 0, 0, w, h, false);
  const g = ctx.createLinearGradient(4, 0, w - 4, 0); g.addColorStop(0, '#6d4fd0'); g.addColorStop(1, '#f48ccd');
  ctx.fillStyle = g; ctx.fillRect(5, 5, w - 10, 34);
  ctx.font = `700 19px ${FONT_SANS}`; ctx.fillStyle = '#fff'; ctx.textBaseline = 'middle'; ctx.textAlign = 'left';
  ctx.fillText(title, 16, 23);
  for (let i = 0; i < 3; i++) {                                                // _ □ x buttons
    const bx = w - 5 - 4 - (3 - i) * 28 + (i === 2 ? 4 : 0), by = 10;
    ctx.fillStyle = '#dcd6ec'; ctx.fillRect(bx, by, 24, 22); bevel(ctx, bx, by, 24, 22, false);
    ctx.strokeStyle = '#2d2446'; ctx.lineWidth = 2.5; ctx.beginPath();
    if (i === 0) { ctx.moveTo(bx + 7, by + 16); ctx.lineTo(bx + 16, by + 16); }
    if (i === 1) { ctx.rect(bx + 6, by + 5, 12, 11); }
    if (i === 2) { ctx.moveTo(bx + 7, by + 6); ctx.lineTo(bx + 17, by + 16); ctx.moveTo(bx + 17, by + 6); ctx.lineTo(bx + 7, by + 16); }
    ctx.stroke();
  }
  body(ctx, 8, 46, w - 16, h - 54);
  ctx.restore();
}
function button(ctx, x, y, w, h, label, pressed, focus) {
  ctx.fillStyle = '#dcd6ec'; ctx.fillRect(x, y, w, h); bevel(ctx, x, y, w, h, pressed);
  ctx.font = `700 20px ${FONT_SANS}`; ctx.fillStyle = '#2d2446'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(label, x + w / 2 + (pressed ? 2 : 0), y + h / 2 + (pressed ? 2 : 0));
  if (focus) { ctx.setLineDash([2, 3]); ctx.strokeStyle = '#2d2446'; ctx.lineWidth = 1.5; ctx.strokeRect(x + 7, y + 7, w - 14, h - 14); ctx.setLineDash([]); }
}
function cursorArrow(ctx, x, y) {
  const pts = [[0, 0], [0, 34], [8, 26], [14, 40], [20, 37], [14, 24], [25, 24]];
  ctx.save(); ctx.translate(x, y); ctx.beginPath(); pts.forEach(([a, b], i) => i ? ctx.lineTo(a, b) : ctx.moveTo(a, b)); ctx.closePath();
  ctx.fillStyle = '#fff'; ctx.fill(); ctx.lineWidth = 2.4; ctx.strokeStyle = '#140c24'; ctx.lineJoin = 'miter'; ctx.stroke(); ctx.restore();
}
function sparkle(ctx, x, y, r, a) {
  if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = '#fff';
  ctx.beginPath(); ctx.moveTo(x, y - r); ctx.quadraticCurveTo(x, y, x + r, y); ctx.quadraticCurveTo(x, y, x, y + r); ctx.quadraticCurveTo(x, y, x - r, y); ctx.quadraticCurveTo(x, y, x, y - r); ctx.fill();
  ctx.restore();
}
function playTri(ctx, x, y, s) { ctx.beginPath(); ctx.moveTo(x, y - s); ctx.lineTo(x + s * 1.5, y); ctx.lineTo(x, y + s); ctx.closePath(); ctx.fill(); }

// ---------- scene A: pastel plaza with the bust and windows ----------
const DLG = { x: 1262, y: 292, w: 470, h: 200 };
const YES2 = { x: DLG.x + 260, y: DLG.y + 140, w: 110, h: 40 };               // the right-hand "Yes" (screen space, no pop scale)
let winOrbImg = null;
async function prepWinOrb(t) {
  const x = xWin; const w = cWin.width, h = cWin.height;
  x.fillStyle = vgrad(x, 0, h, [[0, '#8fe9e0'], [1, '#c7a8f0']]); x.fillRect(0, 0, w, h);
  x.strokeStyle = 'rgba(255,255,255,.55)'; x.lineWidth = 2;
  for (let i = 0; i < 9; i++) { x.beginPath(); x.moveTo(0, 150 + i * i * 4); x.lineTo(w, 150 + i * i * 4); x.stroke(); }
  renderOrb(t * 0.22, 0);
  x.drawImage(glc, ...ORB_SRC, w / 2 - 95, h / 2 - 105 + Math.sin(t * 2) * 6, 190, 190);
  winOrbImg = await crunch(cWin, null, 230, 125, 0.18);
}
function sceneA(t) {
  const ctx = xA; ctx.save();
  const push = 1 + .035 * ease(clamp(t / 5));
  ctx.translate(960, 560); ctx.scale(push, push); ctx.translate(-960 - t * 3, -560);
  ctx.imageSmoothingEnabled = true;
  ctx.drawImage(skyA, -40, -40, W + 80, 700);
  const y0 = 640;
  // pale gradient disc behind the bust
  const dg = ctx.createLinearGradient(0, 180, 0, 640); dg.addColorStop(0, 'rgba(255,255,255,.55)'); dg.addColorStop(1, 'rgba(160,240,232,.55)');
  ctx.fillStyle = dg; ctx.beginPath(); ctx.arc(960, 470, 260, 0, 7); ctx.fill();
  drawColonnade(ctx, 520, 1400, y0 + 2, 150, 'rgba(176,150,222,.85)', 9);
  drawFloor(ctx, y0, t * .45, '#5fd0c7', '#f6effc', 'rgba(255,214,222,1)');
  drawPalm(ctx, 150, 1060, 760, .10, Math.sin(t * 1.3), '#7a4fb0', 3);
  drawPalm(ctx, 1790, 1070, 700, -.12, Math.sin(t * 1.1 + 1), '#7a4fb0', 9);
  // bust shadow + bust
  ctx.fillStyle = 'rgba(40,60,110,.28)'; ctx.beginPath(); ctx.ellipse(975, 1004, 150, 22, 0, 0, 7); ctx.fill();
  const yaw = lerp(-.55, .55, easeInOut(clamp(t / 4.9)));
  renderBust(yaw, 0);
  ctx.drawImage(glc, 960 - 300, 269, 600, 800);
  ctx.restore();

  // ---- screen-space UI (no camera push) ----
  // title: full-width spaced letters popping with overshoot
  ctx.font = `400 84px ${FONT_SERIF}`; ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
  const pitch = 118, n = TITLE.length, x0 = 960 - (n - 1) * pitch / 2;
  let li = 0;
  for (let i = 0; i < n; i++) {
    const ch = TITLE[i]; if (ch === ' ') continue;
    const u = seg(t, T.title0 + li * T.titleStag, T.title0 + li * T.titleStag + T.titleDur); li++;
    if (u <= 0) continue;
    const s = lerp(.4, 1, backOut(u, 2.0)), dy = (1 - easeOut(u)) * 36;
    ctx.save(); ctx.translate(x0 + i * pitch, 160 + dy); ctx.scale(s, s); ctx.globalAlpha = clamp(u * 4);
    ctx.fillStyle = '#5b3aa8'; ctx.fillText(ch, 6, 6);
    ctx.fillStyle = vgrad(ctx, -64, 0, [[0, '#ffffff'], [.5, '#ffc2e6'], [1, '#ff5fb8']]); ctx.fillText(ch, 0, 0);
    ctx.lineWidth = 1.5; ctx.strokeStyle = 'rgba(91,58,168,.6)'; ctx.strokeText(ch, 0, 0);
    ctx.restore();
  }
  // window A: loading memories
  const pA = seg(t, T.winA, T.winA + .38);
  drawWindow(ctx, 88, 330, 500, 250, 'memories.exe', pA, (c, bx, by, bw) => {
    const pr = seg(t, T.prog[0], T.prog[1]);
    c.font = `400 40px ${FONT_PIX}`; c.fillStyle = '#2d2446'; c.textAlign = 'left'; c.textBaseline = 'alphabetic';
    c.fillText(pr < 1 ? 'Loading memories...' : 'Memories loaded.', bx + 16, by + 50);
    c.fillStyle = '#f4f0fb'; c.fillRect(bx + 14, by + 76, bw - 28, 42); bevel(c, bx + 14, by + 76, bw - 28, 42, true);
    const nb = 20, blocks = Math.floor(pr * nb + 1e-6);
    for (let k = 0; k < blocks; k++) { c.fillStyle = k % 2 ? '#3fbdb4' : '#4fcfc5'; c.fillRect(bx + 20 + k * 22, by + 82, 18, 30); }
    c.font = `400 32px ${FONT_PIX}`; c.fillStyle = '#6d4fd0'; c.textAlign = 'right';
    c.fillText(`${Math.round(pr * 100)}%`, bx + bw - 16, by + 158);
    c.textAlign = 'left'; c.fillStyle = '#8e86ab'; c.fillText('est. 1995', bx + 16, by + 158);
  });
  // window B: the rotating orb as a crunchy low-res image
  const pB = seg(t, T.winB, T.winB + .38);
  drawWindow(ctx, 1330, 580, 480, 312, 'orb_final(2).jpg', pB, (c, bx, by, bw, bh) => {
    c.fillStyle = '#fff'; c.fillRect(bx + 4, by + 2, bw - 8, bh - 4); bevel(c, bx + 4, by + 2, bw - 8, bh - 4, true);
    if (winOrbImg) { c.imageSmoothingEnabled = false; c.drawImage(winOrbImg, bx + 6, by + 4, bw - 12, bh - 8); c.imageSmoothingEnabled = true; }
  });
  // dialog C: the only possible answer
  const pC = seg(t, T.dlg, T.dlg + .34);
  const pressed = t >= T.click && t < T.click + .16;
  drawWindow(ctx, DLG.x, DLG.y, DLG.w, DLG.h, 'Question', pC, (c, bx, by) => {
    c.fillStyle = '#6d4fd0'; c.beginPath(); c.arc(bx + 42, by + 46, 26, 0, 7); c.fill();
    c.font = `400 44px ${FONT_PIX}`; c.fillStyle = '#fff'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('?', bx + 42, by + 47);
    c.font = `500 21px ${FONT_SANS}`; c.fillStyle = '#2d2446'; c.textAlign = 'left'; c.textBaseline = 'alphabetic';
    c.fillText('Are you sure you want to', bx + 88, by + 38); c.fillText('feel nostalgic?', bx + 88, by + 66);
    button(c, 120, 140, 110, 40, 'Yes', false, false);
    button(c, 260, 140, 110, 40, 'Yes', pressed, t > T.cursor[1] - .1);
  });
  // cursor glides to the right-hand Yes and clicks
  if (t >= T.cursor[0]) {
    const u = easeInOut(seg(t, T.cursor[0], T.cursor[1]));
    const cx = lerp(1080, YES2.x + 84, u) + Math.sin(u * Math.PI) * 60, cy = lerp(930, YES2.y + 27, u) - Math.sin(u * Math.PI) * 40;
    cursorArrow(ctx, cx, cy + (pressed ? 1 : 0));
  }
  // VCR on-screen display
  ctx.font = `400 64px ${FONT_PIX}`; ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
  if (t > .25 && t < 2.8) {
    ctx.globalAlpha = clamp((2.8 - t) * 4); ctx.fillStyle = 'rgba(40,20,70,.4)'; ctx.fillText('PLAY', 84, 100); playTri(ctx, 222, 83, 18);
    ctx.fillStyle = '#fff'; ctx.fillText('PLAY', 80, 96); playTri(ctx, 218, 79, 18); ctx.globalAlpha = 1;
  }
  ctx.font = `400 46px ${FONT_PIX}`;
  const sec = Math.floor(t);
  const osd = `SP  0:00:${String(sec).padStart(2, '0')}`;
  ctx.fillStyle = 'rgba(40,20,70,.4)'; ctx.fillText(osd, 84, 1034); ctx.fillStyle = '#fff'; ctx.fillText(osd, 80, 1030);
}

// ---------- scene B: dusk plaza, bust in profile, orb, lockup ----------
const STARS = (() => { const r = rng(5); return Array.from({ length: 70 }, () => [r() * W, r() * 360, .6 + r() * 1.8, r() * 6.28]); })();
let plazaW = 0, n95W = 0;
function sceneB(t) {
  const ctx = xB, s = t - T.sceneB; ctx.save();
  const push = 1 + .03 * ease(clamp(s / 5.6));
  ctx.translate(960, 540); ctx.scale(push, push); ctx.translate(-960 + s * 4, -540);
  ctx.drawImage(skyB, -40, -40, W + 80, 680);
  for (const [x, y, r, ph] of STARS) { ctx.globalAlpha = .35 + .35 * Math.sin(t * 2.2 + ph); ctx.fillStyle = '#fff'; ctx.fillRect(x, y, r, r); }
  ctx.globalAlpha = 1;
  const y0 = 600;
  drawFloor(ctx, y0, t * .3, '#3a2a72', '#ff9fd6', 'rgba(255,196,176,1)');
  drawPalm(ctx, 1905, 1090, 760, -.10, Math.sin(t * 1.2), '#1f1540', 4);
  // orb floating over its shadow
  const bob = Math.sin(s * 1.8) * 14;
  ctx.fillStyle = `rgba(20,10,50,${.30 - bob * .005})`; ctx.beginPath(); ctx.ellipse(1650, 760, 130 - bob * 2, 20, 0, 0, 7); ctx.fill();
  renderOrb(t * .2, 1);
  ctx.drawImage(glc, ...ORB_SRC, 1650 - 180, 250 - 180 + bob, 360, 360);
  // bust close-up, near profile, warm key
  renderBust(lerp(1.05, 1.42, easeInOut(clamp(s / 5.6))), 1);
  ctx.drawImage(glc, 250 - 431, 190, 862, 1150);
  ctx.restore();

  // ---- lockup ----
  const cx = 1170, base = 560;
  ctx.font = `italic 400 215px ${FONT_SERIF}`; plazaW = ctx.measureText('PLAZA').width;
  ctx.font = `400 235px ${FONT_PIX}`; n95W = ctx.measureText('95').width;
  const gap = 70, total = plazaW + gap + n95W, lx = cx - total / 2;
  const up = seg(t, T.plaza, T.plaza + .55);
  if (up > 0) {
    const sc = lerp(.86, 1, backOut(up, 1.6)), dy = (1 - easeOut(up)) * 90;
    ctx.save();
    ctx.beginPath(); ctx.rect(0, 0, W, base + 70); ctx.clip();                   // rise from behind a baseline mask
    ctx.translate(lx + plazaW / 2, base - 90 + dy); ctx.scale(sc, sc); ctx.translate(-(lx + plazaW / 2), -(base - 90));
    ctx.font = `italic 400 215px ${FONT_SERIF}`; ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = 'rgba(40,18,84,.85)'; ctx.fillText('PLAZA', lx + 12, base + 12);
    ctx.fillStyle = vgrad(ctx, base - 180, base, [[0, '#ffffff'], [.42, '#ffc6e8'], [.5, '#8a64e0'], [.56, '#b98cf0'], [1, '#9ff5ea']]);
    ctx.fillText('PLAZA', lx, base);
    ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(255,255,255,.85)'; ctx.strokeText('PLAZA', lx, base);
    ctx.restore();
  }
  const p95 = seg(t, T.n95, T.n95 + .42);
  if (p95 > 0) {
    const sc = lerp(.2, 1, backOut(p95, 2.4)), x95 = lx + plazaW + gap + n95W / 2;
    ctx.save(); ctx.translate(x95, base - 85); ctx.scale(sc, sc); ctx.rotate((1 - easeOut(p95)) * -.25);
    ctx.font = `400 235px ${FONT_PIX}`; ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = 'rgba(40,18,84,.85)'; ctx.fillText('95', 11, 90);
    ctx.lineWidth = 12; ctx.strokeStyle = '#3a2470'; ctx.lineJoin = 'round'; ctx.strokeText('95', 0, 80);
    ctx.lineWidth = 6; ctx.strokeStyle = '#ff7fc8'; ctx.strokeText('95', 0, 80);
    ctx.fillStyle = '#86f3e6'; ctx.fillText('95', 0, 80);
    ctx.restore();
  }
  // tagline: title-bar ribbon with full-width spaced letters
  const bar = easeOut(seg(t, T.tagBar, T.tagBar + .35));
  if (bar > 0) {
    const bw = 800 * bar, by = base + 58, bh = 66;
    const g = ctx.createLinearGradient(cx - bw / 2, 0, cx + bw / 2, 0); g.addColorStop(0, '#6d4fd0'); g.addColorStop(1, '#f48ccd');
    ctx.fillStyle = 'rgba(40,18,84,.55)'; ctx.fillRect(cx - bw / 2 + 10, by + 10, bw, bh);
    ctx.fillStyle = g; ctx.fillRect(cx - bw / 2, by, bw, bh);
    ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.fillRect(cx - bw / 2, by, bw, 2);
    ctx.font = `500 40px ${FONT_SANS}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    const pitch = 52, n = TAG.length, x0 = cx - (n - 1) * pitch / 2;
    for (let i = 0; i < n; i++) {
      const u = seg(t, T.tag0 + i * T.tagStag, T.tag0 + i * T.tagStag + .3); if (u <= 0 || TAG[i] === ' ') continue;
      ctx.globalAlpha = u; ctx.fillStyle = '#fff'; ctx.fillText(TAG[i], x0 + i * pitch, by + bh / 2 + 2 + (1 - easeOut(u)) * 14);
    }
    ctx.globalAlpha = 1;
  }
  // sparkles once the lockup has landed
  [[lx + 40, base - 190, 26, 7.55], [lx + plazaW + gap + n95W - 10, base - 200, 20, 7.8], [1560, 120, 30, 7.65], [lx + plazaW * .55, base + 20, 16, 8.0]]
    .forEach(([x, y, r, t0]) => { const u = seg(t, t0, t0 + .6); sparkle(ctx, x, y, r * Math.sin(Math.PI * u) + r * .35 * (u >= 1 ? .6 + .4 * Math.sin(t * 5 + x) : 0), u > 0 ? 1 : 0); });
  // taskbar slides up
  const tb = seg(t, T.taskbar, T.taskbar + .4);
  if (tb > 0) {
    const ty = H - 52 * backOut(tb, 1.4);
    ctx.fillStyle = '#dcd6ec'; ctx.fillRect(0, ty, W, 60); ctx.fillStyle = '#fff'; ctx.fillRect(0, ty + 2, W, 2);
    ctx.fillStyle = '#dcd6ec'; ctx.fillRect(6, ty + 7, 150, 38); bevel(ctx, 6, ty + 7, 150, 38, false);
    const og = ctx.createLinearGradient(0, ty + 14, 0, ty + 38); og.addColorStop(0, '#ff8fcf'); og.addColorStop(1, '#58d6cc');
    ctx.fillStyle = og; ctx.beginPath(); ctx.arc(30, ty + 26, 11, 0, 7); ctx.fill();
    ctx.font = `700 20px ${FONT_SANS}`; ctx.fillStyle = '#2d2446'; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillText('PLAZA', 50, ty + 27);
    ctx.fillStyle = '#dcd6ec'; ctx.fillRect(170, ty + 7, 280, 38); bevel(ctx, 170, ty + 7, 280, 38, true);
    ctx.font = `500 18px ${FONT_SANS}`; ctx.fillStyle = '#2d2446'; ctx.fillText('memories.exe', 186, ty + 27);
    ctx.fillStyle = '#dcd6ec'; ctx.fillRect(W - 150, ty + 7, 144, 38); bevel(ctx, W - 150, ty + 7, 144, 38, true);
    ctx.textAlign = 'center'; ctx.fillText('12:00 AM', W - 78, ty + 27);
  }
}

// ---------- post: VHS softness, chroma bleed, tracking, glitch bands, band-wise crossfade ----------
const out = document.getElementById('out');
const pg = out.getContext('webgl2', { preserveDrawingBuffer: true, antialias: false, premultipliedAlpha: false });
const FS_POST = `#version 300 es
precision highp float;
uniform sampler2D tA,tB,tCA,tCB; uniform vec2 uRes; uniform float uMix,uGl,uT,uFade,uTrack,uFrame;
out vec4 o;
float h1(float n){ return fract(sin(n*127.1)*43758.5453); }
float h2(vec2 p){ return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453); }
vec3 pick(vec2 uv, float sel, float cr){
  vec3 a=mix(texture(tA,uv).rgb,texture(tCA,uv).rgb,cr), b=mix(texture(tB,uv).rgb,texture(tCB,uv).rgb,cr);
  return mix(a,b,sel);
}
vec3 yiq(vec3 c){ return vec3(dot(c,vec3(.299,.587,.114)),dot(c,vec3(.596,-.274,-.322)),dot(c,vec3(.211,-.523,.312))); }
vec3 rgb(vec3 y){ return vec3(y.x+.956*y.y+.621*y.z, y.x-.272*y.y-.647*y.z, y.x-1.106*y.y+1.703*y.z); }
void main(){
  vec2 px=gl_FragCoord.xy; float yt=uRes.y-px.y;
  float off=sin(yt*.013+uT*2.1)*.7+sin(yt*.071+uT*5.3)*.35;
  float bandY=mod(uT*170.,1400.)-160.; float tb=exp(-pow((yt-bandY)/16.,2.))*uTrack;
  off+=tb*34.*(h1(floor(yt/2.)+uFrame)-.5) + tb*10.;
  float bh=mix(22.,64.,step(.5,h1(floor(uFrame/2.)*.37))); float band=floor(yt/bh);
  float hb=h1(band*1.7+floor(uFrame/2.)*13.1);
  float gOn=step(1.-uGl*.5,hb)*step(.001,uGl);
  off+=gOn*(h1(band+uFrame*3.)-.5)*150.*uGl;
  float sel=uMix<=0.?0.:uMix>=1.?1.:step(h1(band*3.3+17.+floor(uFrame/3.)),uMix);
  sel=mix(sel,uMix,.25*(1.-gOn));
  float cr=gOn>0.?1.:clamp(uGl*1.4-.4,0.,1.)*.6;
  vec2 uv=(px+vec2(off,0.))/uRes;
  float ca=(1.6+uGl*16.+tb*6.)/uRes.x;
  vec3 c; c.r=pick(uv+vec2(ca,0.),sel,cr).r; c.g=pick(uv,sel,cr).g; c.b=pick(uv-vec2(ca,0.),sel,cr).b;
  // soft luma, smeared chroma (tape)
  vec3 Y=yiq(c); vec2 iq=vec2(0.); float dx=1./uRes.x;
  for(int k=-3;k<=3;k++){ iq+=yiq(pick(uv+vec2(float(k)*3.5*dx-2.*dx,0.),sel,cr)).yz; }
  Y.yz=mix(Y.yz,iq/7.,.8);
  float yl=(yiq(pick(uv-vec2(dx,0.),sel,cr)).x+yiq(pick(uv+vec2(dx,0.),sel,cr)).x)*.5; Y.x=mix(Y.x,yl,.45);
  c=rgb(Y);
  c*=.94+.06*step(.5,fract(yt/3.));
  c+=(h2(floor(px/2.)+floor(uT*15.)*7.31)-.5)*.045;
  c+=vec3(.9,.95,1.)*tb*.25*h2(px*.37+uFrame);
  vec2 q=px/uRes-.5; c*=1.-.28*dot(q,q)*1.6;
  c=mix(vec3(.07,.04,.12),c,uFade);
  o=vec4(clamp(c,0.,1.),1.);
}`;
const PP = (() => {
  const sh = (type, src) => { const s = pg.createShader(type); pg.shaderSource(s, src); pg.compileShader(s); if (!pg.getShaderParameter(s, pg.COMPILE_STATUS)) throw new Error(pg.getShaderInfoLog(s)); return s; };
  const p = pg.createProgram(); pg.attachShader(p, sh(pg.VERTEX_SHADER, VS)); pg.attachShader(p, sh(pg.FRAGMENT_SHADER, FS_POST)); pg.linkProgram(p);
  if (!pg.getProgramParameter(p, pg.LINK_STATUS)) throw new Error(pg.getProgramInfoLog(p));
  const b = pg.createBuffer(); pg.bindBuffer(pg.ARRAY_BUFFER, b); pg.bufferData(pg.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), pg.STATIC_DRAW);
  const l = pg.getAttribLocation(p, 'p'); pg.enableVertexAttribArray(l); pg.vertexAttribPointer(l, 2, pg.FLOAT, false, 0, 0);
  return p;
})();
const TEX = ['tA', 'tB', 'tCA', 'tCB'].map((n, i) => {
  const tx = pg.createTexture(); pg.activeTexture(pg.TEXTURE0 + i); pg.bindTexture(pg.TEXTURE_2D, tx);
  pg.texParameteri(pg.TEXTURE_2D, pg.TEXTURE_MIN_FILTER, pg.LINEAR); pg.texParameteri(pg.TEXTURE_2D, pg.TEXTURE_MAG_FILTER, pg.LINEAR);
  pg.texParameteri(pg.TEXTURE_2D, pg.TEXTURE_WRAP_S, pg.MIRRORED_REPEAT); pg.texParameteri(pg.TEXTURE_2D, pg.TEXTURE_WRAP_T, pg.CLAMP_TO_EDGE);
  return { n, i, tx };
});
function upload(i, src) { pg.activeTexture(pg.TEXTURE0 + i); pg.bindTexture(pg.TEXTURE_2D, TEX[i].tx); pg.pixelStorei(pg.UNPACK_FLIP_Y_WEBGL, true); pg.texImage2D(pg.TEXTURE_2D, 0, pg.RGBA, pg.RGBA, pg.UNSIGNED_BYTE, src); }

// ---------- envelopes ----------
function glitchAmt(t) { const [a, b, c, d] = T.glitch; return t < a || t > d ? 0 : t < b ? ease(seg(t, a, b)) : t < c ? 1 : 1 - ease(seg(t, c, d)); }
function fadeAmt(t) { return ease(seg(t, T.fadeIn[0], T.fadeIn[1])) * (1 - ease(seg(t, T.fadeOut[0], T.fadeOut[1]))); }
function trackAmt(t) { return .12 + .9 * (1 - seg(t, 0, 1.1)) + .9 * seg(t, T.fadeOut[0], T.fadeOut[1] - .1); }

window.ready = (async () => {
  await document.fonts.load(`400 84px ${FONT_SERIF}`); await document.fonts.load(`italic 400 250px ${FONT_SERIF}`);
  await document.fonts.load(`400 40px ${FONT_PIX}`); await document.fonts.load(`500 20px ${FONT_SANS}`); await document.fonts.load(`700 20px ${FONT_SANS}`);
  await document.fonts.ready;
  await buildSkies();
})();

window.draw = async ({ t }) => {
  const g = glitchAmt(t), mix = seg(t, T.mix[0], T.mix[1]);
  const needA = t < T.mix[1] + .05, needB = t >= T.sceneB;
  if (needA) { await prepWinOrb(t); sceneA(t); }
  if (needB) sceneB(t);
  const srcA = needA ? cA : cB, srcB = needB ? cB : cA;
  upload(0, srcA); upload(1, srcB);
  if (g > 0) {
    const ia = await crunch(srcA, null, 480, 270, 0.06), ib = await crunch(srcB, null, 480, 270, 0.06);
    for (const [x, im] of [[xCA, ia], [xCB, ib]]) { x.imageSmoothingEnabled = false; x.drawImage(im, 0, 0, W, H); }
    upload(2, cCA); upload(3, cCB);
  } else { upload(2, srcA); upload(3, srcB); }
  pg.viewport(0, 0, W, H); pg.useProgram(PP);
  TEX.forEach(({ n, i }) => pg.uniform1i(pg.getUniformLocation(PP, n), i));
  const u = (n, v) => pg.uniform1f(pg.getUniformLocation(PP, n), v);
  pg.uniform2f(pg.getUniformLocation(PP, 'uRes'), W, H);
  u('uMix', mix); u('uGl', g); u('uT', t); u('uFade', fadeAmt(t)); u('uTrack', trackAmt(t)); u('uFrame', Math.round(t * 30));
  pg.drawArrays(pg.TRIANGLES, 0, 3);
  return out.toDataURL('image/jpeg', 0.92).split(',')[1];
};

// audio cue list for audio.py
window.events = () => {
  const ev = [];
  let li = 0; for (const ch of TITLE) { if (ch === ' ') continue; ev.push({ k: 'blip', t: T.title0 + li * T.titleStag + .05, v: li }); li++; }
  ev.push({ k: 'pop', t: T.winA }, { k: 'pop', t: T.winB }, { k: 'pop', t: T.dlg });
  for (let k = 1; k <= 20; k++) ev.push({ k: 'tick', t: lerp(T.prog[0], T.prog[1], k / 20) });
  ev.push({ k: 'ding', t: T.prog[1] + .02 });
  ev.push({ k: 'click', t: T.click });
  ev.push({ k: 'glitch', t: T.glitch[0], d: T.glitch[3] - T.glitch[0] });
  ev.push({ k: 'pop', t: T.taskbar + .05 });
  ev.push({ k: 'swell', t: T.plaza }, { k: 'pop95', t: T.n95 + .05 });
  for (let i = 0; i < TAG.length; i++) if (TAG[i] !== ' ') ev.push({ k: 'blip', t: T.tag0 + i * T.tagStag + .05, v: i + 3 });
  ev.push({ k: 'chime', t: 7.55 });
  ev.push({ k: 'tapestop', t: T.fadeOut[0] });
  return ev;
};
