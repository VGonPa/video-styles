// ── shot A (0 – 3.75 s): wide side-on tracking shot, coastal highway at sunset ──
const A = { HZ: 560, SUNX: 1240, SPEED: 1050 };
function paintSky(w, h, hz, sunx, R) {
  const c = mk(w, h), g = c.getContext('2d');
  const lg = g.createLinearGradient(0, 0, 0, hz);
  lg.addColorStop(0, P.skyTop); lg.addColorStop(.38, P.skyMid); lg.addColorStop(.68, P.skyPink); lg.addColorStop(.88, P.skyAmber); lg.addColorStop(1, P.skyGlow);
  g.fillStyle = lg; g.fillRect(0, 0, w, hz + 4);
  // brushy horizontal paint in the gradient
  for (let i = 0; i < 1400; i++) { const y = R() * hz, u = y / hz;
    const col = u < .4 ? mixc(P.skyTop, P.skyMid, u / .4) : u < .7 ? mixc(P.skyMid, P.skyPink, (u - .4) / .3) : mixc(P.skyPink, P.skyAmber, (u - .7) / .3);
    g.globalAlpha = .12; g.fillStyle = rgba(mixc(col, R() < .5 ? '#ffffff' : '#301040', .12)); g.beginPath(); g.ellipse(R() * w, y, 40 + R() * 120, 3 + R() * 5, 0, 0, TAU); g.fill(); }
  g.globalAlpha = 1;
  // sun halo + disc
  let rg = g.createRadialGradient(sunx, hz - 40, 20, sunx, hz - 40, 520);
  rg.addColorStop(0, 'rgba(255,236,190,.9)'); rg.addColorStop(.3, 'rgba(255,170,110,.35)'); rg.addColorStop(1, 'rgba(255,120,120,0)');
  g.fillStyle = rg; g.fillRect(0, 0, w, hz);
  g.beginPath(); g.arc(sunx, hz - 30, 118, 0, TAU); g.fillStyle = P.sun; g.fill();
  g.beginPath(); g.arc(sunx, hz - 30, 118, 0, TAU); g.lineWidth = 6; g.strokeStyle = 'rgba(255,190,120,.7)'; g.stroke();
  // two thin irregular wisps drifting across the sun
  for (const [dx, dy, len, th, ang] of [[-60, -64, 560, 10, -.035], [90, 8, 380, 6, .02]]) {
    g.save(); g.translate(sunx + dx, hz - 30 + dy); g.rotate(ang);
    g.fillStyle = rgba(mixc(P.cloudMid, P.skyPink, .25), .92);
    g.beginPath(); g.moveTo(-len / 2, 0); g.quadraticCurveTo(-len * .1, -th * 1.4, len / 2, -th * .2); g.quadraticCurveTo(len * .15, th * .9, -len / 2, 0); g.fill();
    g.fillStyle = 'rgba(255,205,150,.85)'; g.beginPath(); g.moveTo(-len * .35, th * .25); g.quadraticCurveTo(0, th * .7, len * .4, th * .05); g.quadraticCurveTo(0, th * .4, -len * .35, th * .25); g.fill();
    g.restore();
  }
  return c;
}
function paintClouds(w, R, list) {
  const c = mk(w, 560), g = c.getContext('2d');
  for (const [x, y, cw, ch, lit] of list) cloudBank(g, R, x, y, cw, ch, lit);
  // high streaky cirrus, magenta with amber belly
  for (let i = 0; i < 14; i++) { const x = R() * w, y = 40 + R() * 180, l = 200 + R() * 400, th = 5 + R() * 6;
    g.save(); g.translate(x, y); g.rotate((R() - .5) * .06);
    g.fillStyle = rgba(P.cloudMid, .6); g.beginPath(); g.moveTo(-l / 2, 0); g.quadraticCurveTo(-l * .1, -th * 1.5, l / 2, -th * .3); g.quadraticCurveTo(l * .2, th, -l / 2, 0); g.fill();
    g.fillStyle = rgba(P.cloudLit, .7); g.beginPath(); g.moveTo(-l * .3, th * .2); g.quadraticCurveTo(l * .05, th * .8, l * .38, 0); g.quadraticCurveTo(0, th * .4, -l * .3, th * .2); g.fill(); g.restore(); }
  return c;
}
function initA() {
  const R = rng(1985);
  A.sky = paintSky(W + 200, A.HZ + 10, A.HZ, A.SUNX + 100, R);
  A.clouds = paintClouds(W + 400, R, [[240, 360, 760, 260, 1], [1000, 250, 640, 200, .85], [1700, 390, 820, 280, 1], [2250, 200, 560, 170, .7]]);
  // distant headland city (dusty teal silhouettes with first lit windows)
  const cc = mk(2600, 260), g = cc.getContext('2d');
  g.fillStyle = '#6a4a7c'; g.beginPath(); g.moveTo(0, 260); g.bezierCurveTo(300, 200, 700, 190, 1100, 230); g.lineTo(1200, 260); g.fill();
  let x = 60;
  while (x < 1000) { const bw = 26 + R() * 50, bh = 40 + R() * 150 * Math.sin(Math.PI * x / 1100) ** .6;
    g.fillStyle = rgba(mixc('#5e5a8a', '#7e5c8a', R())); g.fillRect(x, 230 - bh, bw, bh + 30);
    g.fillStyle = 'rgba(255,190,120,.45)'; g.fillRect(x + bw - 4, 230 - bh, 4, bh);                // sun-lit edge
    for (let wy = 236 - bh; wy < 225; wy += 9) for (let wx = x + 4; wx < x + bw - 6; wx += 8) if (R() < .12) { g.fillStyle = R() < .6 ? '#ffd890' : '#9fe8e0'; g.fillRect(wx, wy, 3, 3); }
    x += bw + R() * 8; }
  g.fillStyle = '#5e5a8a'; g.fillRect(640, 40, 5, 60); g.fillStyle = '#ff5070'; g.beginPath(); g.arc(642, 38, 4, 0, TAU); g.fill();
  A.city = cc;
  // sea painted with horizontal teal strokes, amber/pink sky reflection
  const sc = mk(W + 400, 230), s = sc.getContext('2d');
  const sg = s.createLinearGradient(0, 0, 0, 230); sg.addColorStop(0, '#d8808a'); sg.addColorStop(.12, P.sea0); sg.addColorStop(.6, P.sea1); sg.addColorStop(1, P.sea2);
  s.fillStyle = sg; s.fillRect(0, 0, sc.width, 230);
  for (let i = 0; i < 900; i++) { const y = Math.pow(R(), 1.4) * 230, sz = .3 + y / 230;
    s.globalAlpha = .35; s.fillStyle = R() < .5 ? P.teal : (R() < .5 ? '#e0708a' : P.tealDk); s.beginPath(); s.ellipse(R() * sc.width, y, (20 + R() * 60) * sz, 1.5 + 2 * sz, 0, 0, TAU); s.fill(); }
  s.globalAlpha = 1; A.sea = sc;
  // guardrail tile
  const gc = mk(1920, 90), q = gc.getContext('2d');
  for (let px = 0; px < 1920; px += 160) { q.fillStyle = '#4a3a5e'; q.fillRect(px + 70, 20, 12, 70); q.fillStyle = '#ffb070'; q.fillRect(px + 70, 20, 3, 70); q.strokeStyle = P.ink; q.lineWidth = 2; q.strokeRect(px + 70, 20, 12, 70); }
  q.fillStyle = '#b8b0c8'; q.fillRect(0, 16, 1920, 20); q.fillStyle = '#ffd09a'; q.fillRect(0, 16, 1920, 5); q.fillStyle = '#6a5a80'; q.fillRect(0, 30, 1920, 6);
  q.strokeStyle = P.ink; q.lineWidth = 2.5; q.strokeRect(-5, 16, 1930, 20);
  A.rail = gc;
  // road + verge (static; dashes move per frame)
  const rc = mk(W, H - 780), r = rc.getContext('2d');
  const rg = r.createLinearGradient(0, 0, 0, 180); rg.addColorStop(0, '#6e5a7c'); rg.addColorStop(1, '#4a3a5c');
  r.fillStyle = rg; r.fillRect(0, 0, W, 180);
  dabs(r, R, 600, 0, 0, W, 180, ['#836c8a', '#3e2e50', '#a07a86'], 50, 4, 0, .2, .05);
  r.fillStyle = 'rgba(255,190,130,.35)'; r.fillRect(0, 2, W, 5);
  r.fillStyle = '#2c1a36'; r.fillRect(0, 180, W, 120);
  r.fillStyle = '#3e2548'; r.fillRect(0, 180, W, 10);
  A.road = rc;
  // palms: mid-ground (hazy) and foreground (dark, big)
  const pm = { trunk: '#7a5a80', lit: '#ffb07a', leaf: '#6a6a8e', leafDk: '#4e4a72', line: '#3a2040' };
  A.palmsMid = [0, 1, 2].map(i => paintPalm(R, 260 + i * 40, (R() - .5) * .8, pm));
  const pf = { trunk: '#3a2240', lit: '#c86a6a', leaf: '#2e2a4a', leafDk: '#1e1a34', line: '#140a18' };
  A.palmFg = [paintPalm(R, 1050, .5, pf), paintPalm(R, 980, -.4, pf)];
}
function drawA(g, t) {
  const tc = cel(t, 12);
  const cam = t * A.SPEED;
  // sky (almost locked) + clouds drift
  g.drawImage(A.sky, -100 - cam * .01, 0);
  g.drawImage(A.clouds, -200 - cam * .025, 0);
  g.drawImage(A.city, -120 - cam * .045, A.HZ - 250);
  // sea + sun glitter (glitter is anchored to the sun, re-drawn per held cel)
  g.drawImage(A.sea, -((cam * .09) % 400), A.HZ);
  const R = rng(500 + Math.round(tc * 12));
  for (let i = 0; i < 60; i++) { const y = A.HZ + 6 + Math.pow(R(), 1.3) * 200, sp = 30 + (y - A.HZ) * 1.1;
    const x = A.SUNX + (R() - .5) * sp * 2, l = 10 + R() * 50 * (1 - (y - A.HZ) / 260);
    g.fillStyle = R() < .6 ? 'rgba(255,235,180,.9)' : 'rgba(255,150,130,.8)'; g.fillRect(x - l / 2, y, l, 2 + (y - A.HZ) / 70); }
  // mid palms behind the rail (parallax .35)
  const mp = cam * .35, spacing = 620;
  for (let k = Math.floor(mp / spacing) - 1; k < Math.floor(mp / spacing) + 5; k++) {
    const p = A.palmsMid[((k % 3) + 3) % 3], x = k * spacing - mp + ((k * 137) % 200);
    g.drawImage(p.c, x - p.ax, 790 - p.ay);
  }
  // guardrail
  const rx = -((cam * .85) % 1920);
  g.drawImage(A.rail, rx, 700); g.drawImage(A.rail, rx + 1920, 700);
  g.drawImage(A.road, 0, 780);
  // lane dashes
  g.fillStyle = '#f0e0c8'; const dx = cam % 300;
  for (let x = -dx - 300; x < W + 300; x += 300) { g.beginPath(); g.moveTo(x, 872); g.lineTo(x + 150, 872); g.lineTo(x + 146, 882); g.lineTo(x - 4, 882); g.fill(); }
  // speed streaks on the asphalt (animation on 2s)
  g.fillStyle = 'rgba(255,220,190,.18)';
  for (let i = 0; i < 12; i++) g.fillRect(R() * W, 800 + R() * 150, 120 + R() * 200, 2);
  // car: drifts forward slightly in frame, bob held at 12 fps
  const cx = lerp(820, 1010, eInOut(seg(t, 0, 3.75))) , bob = Math.sin(tc * 23) * 1.5 + (Math.round(tc * 12) % 5 === 0 ? 1.5 : 0);
  g.save(); g.translate(cx, 935 + bob); g.scale(1.22, 1.22);
  drawCarSide(g, 0, 0, tc, gg => {
    gg.save(); gg.beginPath(); gg.rect(-400, -400, 800, 350); gg.clip(); gg.translate(-78, -140 + bob * .3); gg.scale(.2, .2);
    drawDriver(gg, tc, { lw: 11, detail: false, arm: { elbow: [150, 330], hand: [440, 150], wheel: [420, 20, 470, 260] } });
    gg.restore();
  });
  g.restore();
  // foreground palms whip past (parallax 1.9, two-frame smear)
  const fp = cam * 1.9, fsp = 2300;
  for (let k = Math.floor(fp / fsp) - 1; k < Math.floor(fp / fsp) + 2; k++) {
    const p = A.palmFg[((k % 2) + 2) % 2], x = k * fsp - fp + 900;
    if (x < -1500 || x > W + 1500) continue;
    g.globalAlpha = .35; g.drawImage(p.c, x - p.ax + 60, 1180 - p.ay);
    g.globalAlpha = 1; g.drawImage(p.c, x - p.ax, 1180 - p.ay);
  }
}
