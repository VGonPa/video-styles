// ── shot B (3.75 – 6.6 s): close-up of the driver in profile, hair streaming, sun behind ──
const B = { OX: 860, OY: 340, S: 1.07, HZ: 790, SUNX: 380 };
function initB() {
  const R = rng(1986);
  B.sky = paintSky(W + 300, B.HZ + 10, B.HZ, B.SUNX + 150, R);
  B.clouds = paintClouds(W + 600, R, [[300, 520, 860, 280, 1], [1150, 400, 720, 230, .85], [1900, 560, 900, 300, 1], [2400, 280, 600, 190, .7]]);
  const sc = mk(W + 600, 300), s = sc.getContext('2d');
  const sg = s.createLinearGradient(0, 0, 0, 300); sg.addColorStop(0, '#e08a86'); sg.addColorStop(.15, P.sea0); sg.addColorStop(1, P.sea1);
  s.fillStyle = sg; s.fillRect(0, 0, sc.width, 300);
  for (let i = 0; i < 700; i++) { const y = Math.pow(R(), 1.4) * 300, sz = .4 + y / 300;
    s.globalAlpha = .35; s.fillStyle = R() < .5 ? P.teal : (R() < .5 ? '#e0708a' : P.tealDk); s.beginPath(); s.ellipse(R() * sc.width, y, (30 + R() * 70) * sz, 2 + 2 * sz, 0, 0, TAU); s.fill(); }
  s.globalAlpha = 1; B.sea = sc;
  const pf = { trunk: '#3a2240', lit: '#d0706a', leaf: '#2e2a4a', leafDk: '#1e1a34', line: '#140a18' };
  B.palm = paintPalm(R, 1400, .3, pf);
  // passing guardrail smear band at the bottom of the sea
  const rc = mk(W, 60), r = rc.getContext('2d');
  for (let i = 0; i < 90; i++) { r.fillStyle = rgba(R() < .5 ? '#b8b0c8' : '#6a5a80', .5); r.fillRect(R() * W, 10 + R() * 30, 100 + R() * 300, 3 + R() * 6); }
  B.rail = rc;
  // eye position on screen for the iris
}
function drawB(g, t) {
  const tc = cel(t, 12), lt = t - 3.75;
  const cam = lt * 900;
  g.drawImage(B.sky, -150 - lt * 12, 0);
  flare(g, B.SUNX, B.HZ - 30, .55);
  g.drawImage(B.clouds, -300 - lt * 30, 0);
  g.drawImage(B.sea, -((lt * 80) % 600), B.HZ);
  const R = rng(900 + Math.round(tc * 12));
  for (let i = 0; i < 40; i++) { const y = B.HZ + 6 + Math.pow(R(), 1.3) * 230, sp = 30 + (y - B.HZ) * 1.2;
    const x = B.SUNX + (R() - .5) * sp * 2, l = 14 + R() * 60 * (1 - (y - B.HZ) / 300);
    g.fillStyle = R() < .6 ? 'rgba(255,235,180,.9)' : 'rgba(255,150,130,.8)'; g.fillRect(x - l / 2, y, l, 2 + (y - B.HZ) / 60); }
  g.drawImage(B.rail, -((cam * 1.3) % W), 930); g.drawImage(B.rail, W - ((cam * 1.3) % W), 930);
  // background palms sweep right→left behind her (smeared)
  const pp = cam * 2.2, psp = 3400;
  for (let k = Math.floor(pp / psp) - 1; k < Math.floor(pp / psp) + 2; k++) {
    const x = k * psp - pp + 2600; if (x < -1600 || x > W + 1600) continue;
    for (let j = 3; j >= 0; j--) { g.globalAlpha = j ? .18 : 1; g.drawImage(B.palm.c, x - B.palm.ax + j * 70, 1250 - B.palm.ay); }
    g.globalAlpha = 1;
  }
  // driver: held-cel bob and a slow push-in
  const z = 1 + .03 * eInOut(seg(lt, 0, 2.85));
  const bob = Math.sin(tc * 19) * 3;
  const blink = (t > 4.55 && t < 4.72) ? 1 : 0;
  const smile = eOut(seg(tc, 5.2, 5.6));
  B.eyeX = W / 2 + (B.OX + 124 * B.S - W / 2) * z; B.eyeY = H / 2 + (B.OY + bob - 6 * B.S - H / 2) * z;
  g.save(); g.translate(W / 2, H / 2); g.scale(z, z); g.translate(-W / 2, -H / 2);
  g.translate(B.OX, B.OY + bob); g.scale(B.S, B.S);
  drawDriver(g, tc, { lw: 3.6, blink, smile, arm: { elbow: [10, 600], hand: [335, 468], wheel: [296, 300, 410, 700], fistRot: -.25 } });
  g.restore();
  // windshield A-pillar + glass edge + door top in front of everything
  g.save();
  g.fillStyle = 'rgba(120,200,210,.12)'; g.beginPath(); g.moveTo(1800, 1080); g.lineTo(1520, 380); g.lineTo(1920, 380); g.lineTo(1920, 1080); g.fill();
  g.lineCap = 'round'; g.strokeStyle = P.ink; g.lineWidth = 34; g.beginPath(); g.moveTo(1800, 1090); g.lineTo(1520, 380); g.stroke();
  g.strokeStyle = '#c8c6d8'; g.lineWidth = 26; g.stroke();
  g.strokeStyle = '#ffe4c0'; g.lineWidth = 6; g.beginPath(); g.moveTo(1790, 1080); g.lineTo(1512, 384); g.stroke();
  g.restore();
  const door = gg => { gg.moveTo(-20, 1040); gg.quadraticCurveTo(900, 1020, 1940, 1030); gg.lineTo(1940, 1100); gg.lineTo(-20, 1100); gg.closePath(); };
  celShape(g, door, P.red, P.ink, 4);
  celClip(g, door, gg => { gg.fillStyle = P.redHi; gg.fillRect(0, 1030, W, 10); gg.fillStyle = 'rgba(255,245,230,.9)'; gg.beginPath(); gg.moveTo(1100, 1034); gg.lineTo(1260, 1032); gg.lineTo(1230, 1060); gg.lineTo(1080, 1062); gg.fill(); });
  // eye sparkle at the smile
  const sp = bump(t, 5.55, 5.95);
  if (sp > 0) { const x = B.eyeX + 8 * z, y = B.eyeY - 14; g.save(); g.globalCompositeOperation = 'lighter'; g.fillStyle = `rgba(255,255,240,${sp})`;
    g.translate(x, y); g.rotate(sp * .6); for (let i = 0; i < 4; i++) { g.rotate(Math.PI / 2); g.beginPath(); g.moveTo(0, 0); g.lineTo(5, 0); g.lineTo(0, 40 * sp); g.lineTo(-5, 0); g.fill(); } g.restore(); }
}
