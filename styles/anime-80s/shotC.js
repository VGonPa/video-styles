// ── shot C (6.6 – 10 s): night city, the car pulls away down the boulevard; "MIDNIGHT COAST" title card ──
const C = { VX: 960, VY: 610, F: 470 };
const projX = (X, z) => C.VX + X * C.F / z, projY = (Y, z) => C.VY + Y * C.F / z;   // Y = height below eye (camera 1 unit high)
function initC() {
  const R = rng(1987);
  // sky + moon + skyline painted once
  const c = mk(), g = c.getContext('2d');
  const lg = g.createLinearGradient(0, 0, 0, C.VY);
  lg.addColorStop(0, P.night0); lg.addColorStop(.6, P.night1); lg.addColorStop(.88, P.night2); lg.addColorStop(1, '#8a3a6a');
  g.fillStyle = lg; g.fillRect(0, 0, W, H);
  for (let i = 0; i < 900; i++) { const y = R() * C.VY; g.globalAlpha = .1; g.fillStyle = R() < .5 ? '#3a3070' : '#140f30'; g.beginPath(); g.ellipse(R() * W, y, 60 + R() * 140, 3 + R() * 4, 0, 0, TAU); g.fill(); }
  g.globalAlpha = 1;
  for (let i = 0; i < 90; i++) { g.fillStyle = `rgba(255,240,220,${.3 + R() * .6})`; g.beginPath(); g.arc(R() * W, R() * 380, R() * 1.8 + .5, 0, TAU); g.fill(); }
  let rg = g.createRadialGradient(1640, 130, 40, 1640, 130, 230); rg.addColorStop(0, 'rgba(200,220,255,.35)'); rg.addColorStop(1, 'rgba(120,120,220,0)');
  g.fillStyle = rg; g.fillRect(1300, 0, 620, 420);
  g.beginPath(); g.arc(1640, 130, 58, 0, TAU); g.fillStyle = '#f4ecd8'; g.fill();
  g.save(); g.beginPath(); g.arc(1640, 130, 58, 0, TAU); g.clip(); g.fillStyle = '#c9c0d8'; g.beginPath(); g.arc(1674, 114, 58, 0, TAU); g.fill(); g.restore();
  g.fillStyle = 'rgba(80,60,140,.8)'; g.beginPath(); g.ellipse(1690, 158, 150, 8, 0, 0, TAU); g.fill();
  // skyline: far layer (violet) and near layer (indigo) with window grids and neon bars
  const skyline = (n, y0, hMin, hMax, col, lit, far) => {
    let x = -20;
    while (x < W + 20) { const bw = (far ? 40 : 70) + R() * (far ? 70 : 120), dc = Math.abs(x + bw / 2 - C.VX) / W;
      const bh = hMin + R() * (hMax - hMin) * (1 - dc * .9);
      g.fillStyle = col; g.fillRect(x, y0 - bh, bw, bh + 4);
      if (R() < .3) { g.fillRect(x + bw * .3, y0 - bh - 30, bw * .4, 30); g.fillStyle = '#ff4060'; g.fillRect(x + bw * .5 - 2, y0 - bh - 44, 4, 14); }
      g.fillStyle = rgba('#8fe0e0', .25); g.fillRect(x, y0 - bh, 3, bh);
      for (let wy = y0 - bh + 8; wy < y0 - 6; wy += far ? 10 : 14) for (let wx = x + 5; wx < x + bw - 6; wx += far ? 8 : 12)
        if (R() < lit) { g.fillStyle = R() < .7 ? '#ffd27a' : (R() < .5 ? '#9ff0e8' : '#ff8fb8'); g.fillRect(wx, wy, far ? 3 : 5, far ? 4 : 6); }
      if (!far && R() < .35) { const ny = y0 - bh * (.3 + R() * .5); g.fillStyle = R() < .5 ? '#ff4fa0' : '#4ff0e0'; g.fillRect(x + 6, ny, bw - 12, 7); g.globalAlpha = .25; g.fillRect(x, ny - 8, bw, 23); g.globalAlpha = 1; }
      x += bw + (far ? 2 : R() * 20); }
  };
  skyline(0, C.VY + 2, 60, 330, '#3a2c68', .22, true);
  skyline(0, C.VY + 4, 30, 200, '#221a48', .3, false);
  // road surface
  g.fillStyle = '#1a1430'; g.beginPath(); g.moveTo(0, C.VY); g.lineTo(W, C.VY); g.lineTo(W, H); g.lineTo(0, H); g.fill();
  g.fillStyle = '#2a2046'; g.beginPath(); g.moveTo(C.VX - 4, C.VY); g.lineTo(C.VX + 4, C.VY); g.lineTo(projX(3.4, 1), H); g.lineTo(projX(-3.4, 1), H); g.fill();
  // city glow reflected on the wet asphalt
  for (let i = 0; i < 160; i++) { const x = R() * W, y = C.VY + 10 + Math.pow(R(), .7) * (H - C.VY);
    g.fillStyle = rgba(R() < .5 ? '#ff5fa0' : (R() < .5 ? '#ffc070' : '#60e0e0'), .08 + R() * .1); g.fillRect(x, y, 3 + R() * 5, 20 + R() * 80); }
  // kerbs
  g.strokeStyle = '#6a5a9a'; g.lineWidth = 4; for (const s of [-1, 1]) { g.beginPath(); g.moveTo(C.VX + s * 4, C.VY); g.lineTo(projX(s * 3.4, 1), H); g.stroke(); }
  C.bg = c;
  // title art
  initTitle(R);
}
function drawCarRear(g, x, y, s, tc) {
  g.save(); g.translate(x, y); g.scale(s, s);
  // taillight glow on the road
  g.save(); g.globalCompositeOperation = 'lighter';
  for (const sx of [-190, 190]) { const q = g.createLinearGradient(0, 0, 0, 420); q.addColorStop(0, 'rgba(255,60,80,.45)'); q.addColorStop(1, 'rgba(255,60,80,0)'); g.fillStyle = q; g.fillRect(sx - 60, 0, 120, 420); }
  g.restore();
  g.fillStyle = 'rgba(0,0,0,.5)'; g.beginPath(); g.ellipse(0, 0, 330, 22, 0, 0, TAU); g.fill();
  // tyres
  g.fillStyle = '#120a18'; for (const sx of [-1, 1]) { g.fillRect(sx * 290 - (sx > 0 ? 70 : 0), -74, 70, 74); }
  // windshield frame beyond the cabin
  g.lineJoin = 'round'; g.strokeStyle = P.ink; g.lineWidth = 12; g.beginPath(); g.moveTo(-235, -150); g.lineTo(-205, -250); g.lineTo(205, -250); g.lineTo(235, -150); g.stroke();
  g.strokeStyle = '#8c8ab0'; g.lineWidth = 7; g.stroke();
  g.fillStyle = 'rgba(120,180,220,.14)'; g.beginPath(); g.moveTo(-235, -150); g.lineTo(-205, -250); g.lineTo(205, -250); g.lineTo(235, -150); g.fill();
  // passenger headrest
  celShape(g, gg => { gg.moveTo(40, -150); gg.lineTo(46, -212); gg.quadraticCurveTo(95, -228, 144, -212); gg.lineTo(150, -150); gg.closePath(); }, '#3a2448', P.ink, 5);
  // driver from behind: shoulders (jacket), neck, head, hair fluttering out sideways (held cels)
  celShape(g, gg => { gg.moveTo(-200, -140); gg.quadraticCurveTo(-196, -200, -150, -206); gg.lineTo(-40, -206); gg.quadraticCurveTo(4, -200, 8, -140); gg.closePath(); }, '#d8cce0', P.ink, 5);
  g.fillStyle = '#8a76a8'; g.fillRect(-200, -170, 40, 30); g.fillRect(-32, -170, 40, 30);
  // neck
  g.fillStyle = '#e8a898'; g.fillRect(-116, -222, 40, 24); g.strokeStyle = P.ink; g.lineWidth = 4; g.strokeRect(-116, -222, 40, 24);
  // hair seen from behind: a mass lifted and whipped up by the wind, pointed locks (held cels)
  const k = Math.round(tc * 12) % 4, wv = [[0, 0], [8, -6], [2, -12], [-6, -4]][k];
  const hp = gg => { gg.moveTo(-150, -252);
    gg.bezierCurveTo(-152, -322, -40, -322, -42, -252);
    gg.quadraticCurveTo(-30, -214, -34, -180 + wv[1] * .3);
    gg.lineTo(-58, -198); gg.lineTo(-76, -170 - wv[1] * .4); gg.lineTo(-98, -194); gg.lineTo(-124, -168 + wv[1] * .5); gg.lineTo(-144, -198);
    gg.quadraticCurveTo(-170, -186, -206 + wv[0], -188 + wv[1]); gg.lineTo(-172, -214);
    gg.quadraticCurveTo(-200, -222, -238 + wv[0], -238 + wv[1]); gg.quadraticCurveTo(-190, -240, -150, -252); gg.closePath(); };
  celShape(g, hp, '#3b2358', P.ink, 5);
  celClip(g, hp, gg => { gg.fillStyle = '#5a3478'; gg.beginPath(); gg.ellipse(-110, -290, 50, 26, -.2, 0, TAU); gg.fill();
    gg.strokeStyle = '#c78ad0'; gg.lineWidth = 8; gg.lineCap = 'round'; gg.beginPath(); gg.moveTo(-132, -286); gg.quadraticCurveTo(-100, -304, -64, -290); gg.stroke(); });
  g.strokeStyle = P.ink; g.lineWidth = 3; g.beginPath(); g.moveTo(-96, -262); g.quadraticCurveTo(-92, -226, -98, -196); g.moveTo(-124, -258); g.quadraticCurveTo(-140, -224, -172, -214); g.moveTo(-66, -262); g.quadraticCurveTo(-56, -226, -58, -198); g.stroke();

  // body
  const body = gg => { gg.moveTo(-300, -40); gg.lineTo(-300, -118); gg.lineTo(-270, -150); gg.lineTo(270, -150); gg.lineTo(300, -118); gg.lineTo(300, -40); gg.quadraticCurveTo(0, -30, -300, -40); gg.closePath(); };
  celShape(g, body, '#b02240', P.ink, 6);
  celClip(g, body, gg => {
    gg.fillStyle = '#6a1236'; gg.fillRect(-310, -72, 620, 50);
    gg.fillStyle = 'rgba(160,230,240,.55)'; gg.fillRect(-270, -150, 540, 5);     // city light on the deck edge
    gg.fillStyle = 'rgba(255,120,190,.35)'; gg.fillRect(-270, -140, 540, 8);
  });
  // tail-light band: louvered, glowing
  g.fillStyle = '#1a0612'; g.fillRect(-286, -114, 572, 40); g.strokeStyle = P.ink; g.lineWidth = 4; g.strokeRect(-286, -114, 572, 40);
  g.save(); g.globalCompositeOperation = 'lighter';
  for (let i = 0; i < 18; i++) { if (i >= 7 && i <= 10) continue; const lx = -280 + i * 31.5; g.fillStyle = '#ff2a44'; g.fillRect(lx, -108, 25, 28); g.fillStyle = 'rgba(255,200,200,.8)'; g.fillRect(lx, -108, 25, 5); }
  for (const sx of [-180, 180]) { const q = g.createRadialGradient(sx, -94, 10, sx, -94, 190); q.addColorStop(0, 'rgba(255,60,90,.55)'); q.addColorStop(1, 'rgba(255,40,80,0)'); g.fillStyle = q; g.fillRect(sx - 200, -290, 400, 400); }
  g.restore();
  // plate + exhausts
  g.fillStyle = '#e8e2d0'; g.fillRect(-60, -70, 120, 34); g.strokeStyle = P.ink; g.lineWidth = 3; g.strokeRect(-60, -70, 120, 34);
  g.fillStyle = '#2a2040'; g.font = '600 26px "Barlow Condensed"'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('MC 85', 0, -52);
  g.fillStyle = '#8a8aa8'; for (const sx of [-230, 200]) { g.beginPath(); g.ellipse(sx + 15, -34, 16, 8, 0, 0, TAU); g.fill(); g.stroke(); }
  g.restore();
}
function drawC(g, t) {
  const tc = cel(t, 12), lt = t - 6.6;
  const camZ = lt * 9;                      // camera travel (street lamps / dashes)
  const drift = 30 * eInOut(seg(lt, 0, 3.4)); // slow tilt up toward the title
  g.save(); g.translate(0, drift);
  g.drawImage(C.bg, 0, 0); g.drawImage(C.bg, 0, H - 40, W, 40, 0, H - 40, W, 80);
  // lane dashes
  g.fillStyle = '#cfc4e0';
  for (let k = 0; k < 40; k++) { const z0 = 1.2 * k - (camZ % 1.2) + .3, z1 = z0 + .5; if (z0 < .25) continue;
    const y0 = projY(1, z0), y1 = projY(1, z1), w0 = .05 * C.F / z0, w1 = .05 * C.F / z1;
    g.beginPath(); g.moveTo(C.VX - w0, y0); g.lineTo(C.VX + w0, y0); g.lineTo(C.VX + w1, y1); g.lineTo(C.VX - w1, y1); g.fill(); }
  // street lamps on both sides passing toward the viewer
  for (let k = 0; k < 14; k++) { const z = 3 * k - (camZ % 3) + .9; if (z < .7) continue;
    for (const s of [-1, 1]) { const X = s * 4.4, xb = projX(X, z), yb = projY(1, z), yt = projY(-2.2, z), arm = s * -.9 * C.F / z;
      g.strokeStyle = '#140d26'; g.lineWidth = Math.max(1.5, 24 / z); g.beginPath(); g.moveTo(xb, yb); g.lineTo(xb, yt); g.lineTo(xb + arm, yt + 4 / z); g.stroke();
      g.save(); g.globalCompositeOperation = 'lighter'; const r = 90 / z;
      const q = g.createRadialGradient(xb + arm, yt + 10 / z, 1, xb + arm, yt + 10 / z, r * 2.4); q.addColorStop(0, 'rgba(255,220,150,.9)'); q.addColorStop(.25, 'rgba(255,160,90,.35)'); q.addColorStop(1, 'rgba(255,120,80,0)');
      g.fillStyle = q; g.fillRect(xb + arm - r * 2.4, yt + 10 / z - r * 2.4, r * 4.8, r * 4.8);
      g.fillStyle = 'rgba(255,190,120,.12)'; g.fillRect(xb + arm - r * .5, yb - 4, r, 200 / z); g.restore(); } }
  // car recedes (held at 12 fps), slight lane sway
  const zc = lerp(1.45, 5.2, eIn(seg(tc, 6.6, 9.9)) * .6 + seg(tc, 6.6, 9.9) * .4);
  const s = 1.9 / zc * C.F / 600, cx = C.VX + Math.sin(tc * 2.2) * 30 / zc;
  C.irisX = cx; C.irisY = projY(1, zc) - 94 * s + drift;
  drawCarRear(g, cx, projY(1, zc), s, tc);
  g.restore();
  drawTitle(g, t);
}
// ── title card ──
const TT = { words: 'MIDNIGHT COAST', y: 300, size: 160 };
function initTitle(R) {
  const g = mk(10, 10).getContext('2d'); g.font = `400 ${TT.size}px "Russo One"`;
  TT.letters = []; const gap = 6;
  let tw = 0; const ws = [...TT.words].map(ch => { const w = ch === ' ' ? TT.size * .32 : g.measureText(ch).width; tw += w + gap; return w; });
  let x = -tw / 2;
  [...TT.words].forEach((ch, i) => {
    if (ch !== ' ') {
      const pad = 60, c = mk(Math.ceil(ws[i] + pad * 2 + 40), TT.size + pad * 2), q = c.getContext('2d');
      q.font = g.font; q.textBaseline = 'alphabetic'; q.lineJoin = 'round';
      const bx = pad + 20, by = pad + TT.size * .86;
      q.setTransform(1, 0, -.2, 1, TT.size * .18, 0);
      // deep extrude
      for (let d = 18; d > 0; d -= 2) { q.fillStyle = d > 12 ? '#130a2c' : '#2a1a5c'; q.fillText(ch, bx + d * .55, by + d); }
      q.lineWidth = 16; q.strokeStyle = '#130a2c'; q.strokeText(ch, bx, by);
      const fg = q.createLinearGradient(0, pad, 0, pad + TT.size);
      fg.addColorStop(0, '#fff6d8'); fg.addColorStop(.38, '#ffd070'); fg.addColorStop(.52, '#ff8a4a'); fg.addColorStop(.53, '#ff4f8a'); fg.addColorStop(1, '#b02a8a');
      q.fillStyle = fg; q.fillText(ch, bx, by);
      // horizontal speed cuts through the lower half
      q.globalCompositeOperation = 'destination-out';
      for (const [yy, hh] of [[.66, 5], [.76, 7], [.86, 9]]) q.fillRect(0, pad + TT.size * yy, c.width, hh);
      q.globalCompositeOperation = 'source-atop';
      q.fillStyle = 'rgba(255,255,255,.85)'; q.fillRect(0, pad + TT.size * .12, c.width, 8);
      q.globalCompositeOperation = 'source-over';
      q.lineWidth = 3; q.strokeStyle = 'rgba(255,250,235,.9)'; q.strokeText(ch, bx - 2, by - 2);
      TT.letters.push({ c, x: x - bx, i: TT.letters.length, w: ws[i] });
    }
    x += ws[i] + gap;
  });
}
function drawTitle(g, t) {
  const lt = t - 7.7; if (lt < 0) return;
  const tc = cel(lt, 12);
  // magenta slab behind the tagline slides in
  const bar = eOut(seg(lt, .55, .9));
  if (bar > 0) {
    g.save(); g.translate(W / 2, TT.y + 150); g.transform(1, 0, -.2, 1, 0, 0);
    g.fillStyle = '#ff4f8a'; g.fillRect(-470 * bar, -26, 940 * bar, 52); g.fillStyle = '#130a2c'; g.fillRect(-470 * bar + 10, 30, 940 * bar, 8);
    g.restore();
    g.save(); g.globalAlpha = seg(lt, .75, 1.0); g.fillStyle = '#fff4e4'; g.font = 'italic 600 38px "Barlow Condensed"'; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.fillText('EPISODE 01  ·  AFTER THE SUN GOES DOWN', W / 2, TT.y + 152); g.restore();
  }
  // letters slam in, staggered, on held cels with overshoot
  for (const L of TT.letters) {
    const u = seg(tc, L.i * .045, L.i * .045 + .3); if (u <= 0) continue;
    const sc = u < 1 ? lerp(2.2, 1, eBack(u)) : 1, a = clamp(u * 3);
    g.save(); g.globalAlpha = a; g.translate(W / 2 + L.x + L.c.width / 2, TT.y); g.scale(sc, sc);
    g.drawImage(L.c, -L.c.width / 2, -L.c.height / 2 - 20); g.restore();
  }
  // glint star sweeping across the logo + lens flare pop
  const gs = seg(lt, .9, 1.5);
  if (gs > 0 && gs < 1) { const x = lerp(W / 2 - 700, W / 2 + 700, eInOut(gs)), y = TT.y - 70;
    g.save(); g.globalCompositeOperation = 'lighter'; const k = Math.sin(Math.PI * gs);
    g.fillStyle = `rgba(255,255,245,${k})`; g.translate(x, y);
    for (let i = 0; i < 4; i++) { g.rotate(Math.PI / 2); g.beginPath(); g.moveTo(0, 0); g.lineTo(7, 0); g.lineTo(0, 90 * k); g.lineTo(-7, 0); g.fill(); }
    g.restore(); flare(g, x, y, k * .8, [255, 150, 200]); }
}
