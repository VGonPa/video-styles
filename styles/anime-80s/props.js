// ── anime-80s · props: palm tree, sports car (side + rear), driver profile ──

// palm tree cel painted to its own canvas. lit: rim colour from the low sun
function paintPalm(R, h, lean, cols) {
  const c = mk(Math.round(h * 1.3), Math.round(h * 1.15)), g = c.getContext('2d');
  const bx = c.width * .5 - lean * h * .15, by = c.height - 4;
  const tx = c.width * .5 + lean * h * .25, ty = c.height - h;
  const pt = u => [lerp(bx, tx, u) + Math.sin(u * Math.PI) * lean * h * .12, lerp(by, ty, u)];
  // trunk
  const w0 = h * .045, w1 = h * .026;
  g.beginPath();
  for (let i = 0; i <= 20; i++) { const u = i / 20, [x, y] = pt(u); const w = lerp(w0, w1, u); i ? g.lineTo(x - w, y) : g.moveTo(x - w, y); }
  for (let i = 20; i >= 0; i--) { const u = i / 20, [x, y] = pt(u); const w = lerp(w0, w1, u); g.lineTo(x + w, y); }
  g.closePath(); g.fillStyle = cols.trunk; g.fill(); g.lineWidth = Math.max(1.5, h * .004); g.strokeStyle = cols.line; g.stroke();
  // trunk rings + lit edge
  g.save(); g.clip();
  for (let i = 0; i <= 20; i++) { const u = i / 20, [x, y] = pt(u); const w = lerp(w0, w1, u); g.fillStyle = cols.lit; g.fillRect(x - w, y - 2, w * .55, h * .02); }
  g.strokeStyle = cols.line; g.globalAlpha = .5; g.lineWidth = Math.max(1, h * .003);
  for (let u = .04; u < 1; u += .045) { const [x, y] = pt(u); const w = lerp(w0, w1, u); g.beginPath(); g.moveTo(x - w, y); g.quadraticCurveTo(x, y + w * .5, x + w, y - 2); g.stroke(); }
  g.restore(); g.globalAlpha = 1;
  // fronds
  const nf = 9;
  const frond = (a, len, droop, col, shade) => {
    const sp = [];
    for (let i = 0; i <= 14; i++) { const u = i / 14; const ang = a + droop * u * u * Math.sign(Math.cos(a) || 1); sp.push([tx + Math.cos(a) * len * u + Math.cos(ang) * len * u * .1, ty + Math.sin(a) * len * u * .9 + droop * len * u * u * .55]); }
    // leaflets as a jagged tapered blade
    g.beginPath();
    for (let i = 0; i <= 14; i++) { const [x, y] = sp[i]; const w = h * .07 * Math.sin(Math.PI * Math.min(1, i / 14 * 1.15)) * (i % 2 ? 1 : .55); i ? g.lineTo(x, y - w) : g.moveTo(x, y); }
    for (let i = 14; i >= 0; i--) { const [x, y] = sp[i]; const w = h * .06 * Math.sin(Math.PI * Math.min(1, i / 14 * 1.15)) * (i % 2 ? .55 : 1); g.lineTo(x, y + w); }
    g.closePath(); g.fillStyle = col; g.fill(); g.lineWidth = Math.max(1.2, h * .0035); g.strokeStyle = cols.line; g.stroke();
    g.beginPath(); g.moveTo(sp[0][0], sp[0][1]); for (const [x, y] of sp) g.lineTo(x, y); g.strokeStyle = shade; g.lineWidth = Math.max(1, h * .004); g.stroke();
  };
  for (let k = 0; k < nf; k++) {
    const a = -Math.PI / 2 + (k / (nf - 1) - .5) * Math.PI * 1.55 + (R() - .5) * .2;
    const back = k % 2 === 0;
    frond(a, h * (.36 + R() * .12), .9 + R() * .5, back ? cols.leafDk : cols.leaf, back ? cols.line : cols.lit);
  }
  g.beginPath(); g.arc(tx, ty, h * .03, 0, TAU); g.fillStyle = cols.trunk; g.fill();
  return { c, ax: bx, ay: by };
}

// ── original wedge sports car, side view, facing right. origin = centre of the road contact line
function carSidePath(g) {
  g.moveTo(-322, -40);
  g.lineTo(-326, -104); g.lineTo(-300, -118); g.lineTo(-292, -106);     // tail + ducktail spoiler
  g.lineTo(-150, -102);                                                  // rear deck
  g.lineTo(-150, -98); g.lineTo(-20, -98);                              // open cockpit door line
  g.lineTo(80, -100); g.quadraticCurveTo(250, -86, 318, -66);            // long hood
  g.quadraticCurveTo(334, -60, 330, -40);                                // nose
  g.lineTo(330, -26); g.lineTo(262, -24);
  g.arc(205, -46, 60, -.3, Math.PI + .3, true);                         // front wheel arch
  g.lineTo(-146, -24);
  g.arc(-205, -46, 60, -.3, Math.PI + .3, true);                        // rear wheel arch
  g.lineTo(-322, -26); g.closePath();
}
function wheel(g, x, y, r, rot, night) {
  g.beginPath(); g.arc(x, y, r, 0, TAU); g.fillStyle = '#1c1020'; g.fill(); g.lineWidth = 3; g.strokeStyle = P.ink; g.stroke();
  g.beginPath(); g.arc(x, y, r * .62, 0, TAU); g.fillStyle = night ? '#4a4a70' : '#8f98a8'; g.fill(); g.stroke();
  g.save(); g.translate(x, y); g.rotate(rot); g.fillStyle = night ? '#2a2a48' : '#5c6478';
  for (let i = 0; i < 5; i++) { g.rotate(TAU / 5); g.beginPath(); g.moveTo(-r * .09, r * .12); g.lineTo(-r * .16, r * .55); g.lineTo(r * .16, r * .55); g.lineTo(r * .09, r * .12); g.fill(); }
  g.restore();
  g.beginPath(); g.arc(x, y, r * .14, 0, TAU); g.fillStyle = '#d8dce8'; g.fill();
  g.beginPath(); g.arc(x - r * .22, y - r * .25, r * .42, Math.PI * 1.05, Math.PI * 1.45); g.strokeStyle = 'rgba(255,240,220,.8)'; g.lineWidth = 3; g.stroke();
}
function drawCarSide(g, x, y, tc, driver) {
  g.save(); g.translate(x, y);
  // shadow
  g.fillStyle = 'rgba(30,10,40,.45)'; g.beginPath(); g.ellipse(0, -6, 360, 16, 0, 0, TAU); g.fill();
  // windshield (behind driver) + steering wheel
  g.beginPath(); g.moveTo(80, -100); g.lineTo(-8, -160); g.lineTo(-18, -156); g.lineTo(58, -100); g.closePath();
  g.fillStyle = 'rgba(120,200,210,.35)'; g.fill(); g.lineWidth = 3; g.strokeStyle = P.ink; g.stroke();
  if (driver) driver(g);
  // body
  celShape(g, carSidePath, P.red, P.ink, 3.5);
  celClip(g, carSidePath, gg => {
    gg.fillStyle = P.redDk; gg.fillRect(-340, -64, 700, 60);                          // lower cel shade
    gg.fillStyle = P.redHi; gg.fillRect(-340, -97, 700, 10);                           // sunset reflection band
    gg.fillStyle = '#ffc070'; gg.fillRect(-340, -89, 700, 4);
    gg.fillStyle = 'rgba(255,245,230,.95)';                                             // glossy glints
    gg.beginPath(); gg.moveTo(120, -97); gg.lineTo(190, -93); gg.lineTo(150, -76); gg.lineTo(96, -79); gg.fill();
    gg.beginPath(); gg.moveTo(-110, -94); gg.lineTo(-70, -94); gg.lineTo(-96, -76); gg.lineTo(-124, -76); gg.fill();
    gg.fillStyle = 'rgba(255,245,230,.5)'; gg.fillRect(-300, -104, 140, 3);
  });
  // body crease, door seam, side intake, lights
  g.strokeStyle = P.ink; g.lineWidth = 2.5;
  g.beginPath(); g.moveTo(-318, -66); g.lineTo(326, -62); g.stroke();
  g.beginPath(); g.moveTo(-40, -97); g.lineTo(-46, -30); g.moveTo(96, -99); g.lineTo(100, -30); g.stroke();
  g.fillStyle = '#2a0e22'; g.beginPath(); g.moveTo(-132, -60); g.lineTo(-70, -60); g.lineTo(-80, -44); g.lineTo(-126, -44); g.closePath(); g.fill();
  g.fillStyle = '#ffb040'; g.fillRect(300, -58, 24, 8); g.strokeRect(300, -58, 24, 8);
  g.fillStyle = '#ff3040'; g.fillRect(-326, -92, 12, 26); g.strokeRect(-326, -92, 12, 26);
  g.fillStyle = '#1c1020'; g.fillRect(-330, -30, 664, 8);
  const rot = -tc * 14;
  wheel(g, -205, -46, 50, rot); wheel(g, 205, -46, 50, rot);
  g.restore();
}

// ── driver, profile facing right. local units: ear ≈ (0,0), crown y=-200, chin y=156
function skinPath(g) {
  g.moveTo(-40, -150);
  g.bezierCurveTo(40, -200, 120, -160, 140, -80);
  g.bezierCurveTo(146, -55, 150, -40, 147, -22);
  g.bezierCurveTo(144, -10, 150, 5, 162, 22);
  g.lineTo(184, 50);
  g.bezierCurveTo(178, 58, 168, 62, 158, 62);
  g.bezierCurveTo(160, 70, 168, 78, 166, 84);
  g.bezierCurveTo(160, 88, 154, 90, 152, 93);
  g.bezierCurveTo(158, 97, 162, 103, 157, 108);
  g.bezierCurveTo(150, 114, 144, 116, 146, 124);
  g.bezierCurveTo(150, 134, 154, 146, 146, 156);
  g.bezierCurveTo(130, 170, 100, 172, 80, 168);
  g.bezierCurveTo(76, 210, 80, 250, 88, 310);
  g.lineTo(-34, 310);
  g.bezierCurveTo(-28, 250, -24, 200, -30, 140);
  g.bezierCurveTo(-60, 60, -70, -60, -40, -150); g.closePath();
}
function hairCapPath(g) {
  g.moveTo(134, -98);
  g.bezierCurveTo(152, -165, 62, -222, -40, -204);
  g.bezierCurveTo(-134, -186, -156, -62, -124, 40);
  g.bezierCurveTo(-112, 92, -84, 130, -46, 150);
  g.bezierCurveTo(-34, 96, -18, 64, -8, 40);
  g.bezierCurveTo(4, 8, 26, -18, 52, -34);
  g.bezierCurveTo(88, -52, 118, -64, 134, -98); g.closePath();
}
// streaming strands: centre line from anchor, flowing to -x with a travelling wave (held cels)
function strand(g, ax, ay, len, wid, ph, tc, amp, lift, col, hi, lw) {
  const n = 18, pts = [];
  for (let i = 0; i <= n; i++) {
    const s = i / n;
    const wv = Math.sin(TAU * (s * 1.3 - tc * 2.2) + ph) * amp * Math.pow(s, 1.2);
    pts.push([ax - len * s, ay - lift * s + wv + 40 * s * s]);
  }
  const edge = (sign) => { const out = [];
    for (let i = 0; i <= n; i++) { const s = i / n, a = pts[Math.max(0, i - 1)], b = pts[Math.min(n, i + 1)];
      const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1; const w = wid * Math.pow(1 - s, .8) * (0.6 + .4 * Math.sin(Math.PI * Math.min(1, s * 3 + .3)));
      out.push([pts[i][0] - dy / L * w * sign, pts[i][1] + dx / L * w * sign]); } return out; };
  const e1 = edge(1), e2 = edge(-1);
  g.beginPath(); g.moveTo(e1[0][0], e1[0][1]); for (const p of e1) g.lineTo(p[0], p[1]); for (let i = n; i >= 0; i--) g.lineTo(e2[i][0], e2[i][1]); g.closePath();
  g.fillStyle = col; g.fill(); g.lineWidth = lw; g.strokeStyle = P.ink; g.lineJoin = 'round'; g.stroke();
  if (hi) { g.beginPath(); for (let i = 2; i <= n * .6; i++) { const p = e1[i], q = pts[i]; const x = lerp(p[0], q[0], .45), y = lerp(p[1], q[1], .45); i === 2 ? g.moveTo(x, y) : g.lineTo(x, y); }
    g.strokeStyle = hi; g.lineWidth = wid * .22; g.lineCap = 'round'; g.stroke(); }
}
// main flowing hair mass: crown → pointed locks trailing to -x, travelling wave on held cels
function hairMass(g, tc, lw) {
  const wave = (x, y, ph) => { const s = clamp(-x / 680); return [x, y + Math.sin(TAU * (s * 1.1 - tc * 2.2) + ph) * 34 * Math.pow(s, 1.3)]; };
  const locks = [[-640, -175], [-700, -110], [-610, -40], [-690, 20], [-560, 90], [-470, 140]];
  const vals = [[-430, -135], [-470, -70], [-450, -5], [-420, 60], [-360, 115]];
  const pts = [[-10, -206], [-160, -214], [-330, -196]];
  locks.forEach((p, i) => { pts.push(p); if (vals[i]) pts.push(vals[i]); });
  pts.push([-300, 150], [-150, 150], [-46, 150]);
  const W_ = pts.map((p, i) => wave(p[0], p[1], i * .35));
  const path = gg => { gg.moveTo(W_[0][0], W_[0][1]);
    for (let i = 1; i < W_.length; i++) { const a = W_[i - 1], b = W_[i]; const isTip = locks.some(l => l[0] === pts[i][0]);
      if (isTip) gg.quadraticCurveTo(lerp(a[0], b[0], .5), lerp(a[1], b[1], .5) - 14, b[0], b[1]); else gg.quadraticCurveTo(lerp(a[0], b[0], .6), lerp(a[1], b[1], .5) + 10, b[0], b[1]); }
    gg.lineTo(40, 40); gg.closePath(); };
  celShape(g, path, HAIR.base, P.ink, lw);
  celClip(g, path, gg => {
    gg.fillStyle = '#2a1842'; gg.beginPath(); gg.moveTo(-60, 80); for (let x = -60; x >= -720; x -= 40) { const p = wave(x, 60 + (-x) * .02, 2); gg.lineTo(p[0], p[1]); } gg.lineTo(-720, 300); gg.lineTo(-60, 300); gg.fill();
    // gloss streaks following the flow
    for (const [y0, ph, w] of [[-170, 0, 16], [-100, 1.1, 12], [-30, 2.2, 10]]) {
      gg.beginPath(); for (let x = -140; x >= -520; x -= 20) { const p = wave(x, y0 + (x + 140) * -.02, ph); x === -140 ? gg.moveTo(p[0], p[1]) : gg.lineTo(p[0], p[1]); }
      gg.strokeStyle = HAIR.hi; gg.lineWidth = w; gg.lineCap = 'round'; gg.stroke(); }
    gg.beginPath(); for (let x = -40; x >= -700; x -= 20) { const p = wave(x, -212 + (-x) * .05, 0); x === -40 ? gg.moveTo(p[0], p[1]) : gg.lineTo(p[0], p[1]); }
    gg.strokeStyle = HAIR.rim; gg.lineWidth = 14; gg.stroke();
  });
  // inner lock separation lines
  g.strokeStyle = P.ink; g.lineWidth = lw * .7;
  for (const [y0, ph] of [[-140, .4], [-60, 1.4], [20, 2.5], [90, 3.1]]) { g.beginPath(); for (let x = -120; x >= -400; x -= 20) { const p = wave(x, y0 + (x + 120) * -.03, ph); x === -120 ? g.moveTo(p[0], p[1]) : g.lineTo(p[0], p[1]); } g.stroke(); }
}
const HAIR = { base: '#3b2358', mid: '#5a3478', hi: '#c78ad0', rim: '#ffb070' };
const STRANDS = (() => { const R = rng(4242), a = [];
  for (let i = 0; i < 5; i++) { const u = i / 4; a.push({ ax: lerp(-60, -118, Math.sin(u * Math.PI)) + (u > .5 ? 30 * (u - .5) : 0), ay: lerp(-175, 120, u), len: 480 + R() * 260, wid: 14 + R() * 8, ph: R() * TAU, amp: 26 + R() * 30, lift: 40 - u * 120 + (R() - .5) * 60, back: i % 3 === 1 }); }
  return a; })();
function drawDriver(g, tc, o = {}) {
  const blink = o.blink || 0, smile = o.smile || 0, lw = o.lw || 3.4;
  for (const s of STRANDS) if (s.back) strand(g, s.ax - 40, s.ay + 30, s.len * .9, s.wid, s.ph + 1.3, tc, s.amp, s.lift, '#2a1842', null, lw);
  hairMass(g, tc, lw);
  // torso: 80s padded jacket
  const jacket = gg => { gg.moveTo(82, 252); gg.bezierCurveTo(150, 290, 200, 330, 230, 420); gg.lineTo(260, 700); gg.lineTo(-240, 700); gg.lineTo(-230, 420);
    gg.bezierCurveTo(-226, 350, -200, 318, -150, 296); gg.bezierCurveTo(-100, 280, -50, 262, -30, 240); gg.closePath(); };
  const skin = '#ffd6bc', skinSh = '#e08a8a', skinLit = '#ffe9c8';
  celShape(g, skinPath, skin, P.ink, lw);
  celClip(g, skinPath, gg => {
    gg.beginPath(); gg.moveTo(80, 168); gg.bezierCurveTo(60, 150, 30, 130, 8, 96); gg.lineTo(-70, 100); gg.lineTo(-70, 320); gg.lineTo(100, 320); gg.closePath();
    gg.fillStyle = skinSh; gg.fill();
    gg.fillStyle = skinLit; gg.beginPath(); gg.ellipse(150, -70, 14, 60, -.1, 0, TAU); gg.fill();
  });
  celShape(g, jacket, '#efe4ee', P.ink, lw);
  celClip(g, jacket, gg => {
    gg.fillStyle = '#9d86b8'; gg.beginPath(); gg.moveTo(-240, 300); gg.lineTo(-40, 300); gg.bezierCurveTo(-10, 420, 20, 560, 40, 720); gg.lineTo(-260, 720); gg.fill();
    gg.fillStyle = '#ffc890'; gg.fillRect(214, 300, 60, 420);
  });
  // collar / lapel + shirt vee
  g.fillStyle = '#4f8c95'; g.beginPath(); g.moveTo(80, 250); g.bezierCurveTo(110, 270, 130, 285, 146, 300); g.lineTo(96, 380); g.bezierCurveTo(60, 330, 20, 290, -26, 244); g.quadraticCurveTo(30, 262, 80, 250); g.closePath(); g.fill(); g.lineWidth = lw; g.strokeStyle = P.ink; g.stroke();
  g.beginPath(); g.moveTo(-30, 242); g.bezierCurveTo(0, 300, 30, 330, 96, 380); g.stroke();
  // arm: upper arm (sleeve), elbow, pushed-up sleeve, forearm, fist on the wheel
  const arm = o.arm;
  if (arm) {
    const [sx, sy] = [-120, 360], [ex, ey] = arm.elbow, [hx_, hy] = arm.hand;
    const tube = (x0, y0, x1, y1, w0, w1, fill) => { const a = Math.atan2(y1 - y0, x1 - x0), nx = -Math.sin(a), ny = Math.cos(a);
      const bld = gg => { gg.moveTo(x0 + nx * w0, y0 + ny * w0); gg.lineTo(x1 + nx * w1, y1 + ny * w1); gg.arc(x1, y1, w1, a + Math.PI / 2, a - Math.PI / 2, true); gg.lineTo(x0 - nx * w0, y0 - ny * w0); gg.arc(x0, y0, w0, a - Math.PI / 2, a + Math.PI / 2, true); gg.closePath(); };
      celShape(g, bld, fill, P.ink, lw); return bld; };
    const ua = tube(sx, sy, ex, ey, 70, 54, '#e6d8e6');
    celClip(g, ua, gg => { const a = Math.atan2(ey - sy, ex - sx), nx = -Math.sin(a), ny = Math.cos(a);
      gg.fillStyle = '#9d86b8'; gg.beginPath(); gg.moveTo(sx + nx * 20, sy + ny * 20); gg.lineTo(ex + nx * 14, ey + ny * 14); gg.lineTo(ex + nx * 90, ey + ny * 90); gg.lineTo(sx + nx * 110, sy + ny * 110); gg.fill();
      gg.fillStyle = '#ffc890'; gg.beginPath(); gg.moveTo(sx - nx * 58, sy - ny * 58); gg.lineTo(ex - nx * 44, ey - ny * 44); gg.lineTo(ex - nx * 90, ey - ny * 90); gg.lineTo(sx - nx * 110, sy - ny * 110); gg.fill(); });
    g.lineWidth = lw * 1.4; g.strokeStyle = P.ink; g.beginPath(); ua(g); g.stroke();
    tube(ex, ey, hx_, hy, 34, 28, skin);
    // pushed-up sleeve cuff at the elbow
    { const a = Math.atan2(hy - ey, hx_ - ex), nx = -Math.sin(a), ny = Math.cos(a), cx0 = ex + Math.cos(a) * 30, cy0 = ey + Math.sin(a) * 30;
      celShape(g, gg => { gg.moveTo(ex + nx * 58, ey + ny * 58); gg.lineTo(cx0 + nx * 44, cy0 + ny * 44); gg.lineTo(cx0 - nx * 44, cy0 - ny * 44); gg.lineTo(ex - nx * 58, ey - ny * 58); gg.closePath(); }, '#efe4ee', P.ink, lw);
      g.beginPath(); g.moveTo(lerp(ex, cx0, .5) + nx * 50, lerp(ey, cy0, .5) + ny * 50); g.lineTo(lerp(ex, cx0, .5) - nx * 50, lerp(ey, cy0, .5) - ny * 50); g.strokeStyle = '#9d86b8'; g.lineWidth = lw; g.stroke(); }
    // steering wheel rim (edge-on) then fist wrapped over it
    const [w0x, w0y, w1x, w1y] = arm.wheel;
    g.lineCap = 'round'; g.strokeStyle = P.ink; g.lineWidth = 50; g.beginPath(); g.moveTo(w0x, w0y); g.lineTo(w1x, w1y); g.stroke();
    g.strokeStyle = '#2b2233'; g.lineWidth = 43; g.stroke();
    g.strokeStyle = 'rgba(255,190,140,.8)'; g.lineWidth = 6; g.beginPath(); g.moveTo(w0x - 12, w0y + 4); g.lineTo(w1x - 12, w1y + 4); g.stroke();
    g.save(); g.translate(hx_, hy); g.rotate(arm.fistRot || 0);
    const fist = gg => { gg.moveTo(-40, -34); gg.bezierCurveTo(-10, -52, 40, -50, 62, -30); gg.bezierCurveTo(78, -12, 78, 30, 60, 46); gg.bezierCurveTo(30, 62, -20, 58, -44, 36); gg.bezierCurveTo(-58, 12, -56, -20, -40, -34); gg.closePath(); };
    celShape(g, fist, skin, P.ink, lw);
    celClip(g, fist, gg => { gg.fillStyle = skinSh; gg.fillRect(-60, 20, 140, 60); });
    g.strokeStyle = P.ink; g.lineWidth = lw * .8;
    for (let i = 0; i < 3; i++) { const y = -22 + i * 20; g.beginPath(); g.moveTo(34, y); g.quadraticCurveTo(58, y + 6, 70, y + 12); g.stroke(); }  // finger splits
    g.beginPath(); g.moveTo(-30, -30); g.bezierCurveTo(0, -46, 30, -40, 44, -26); g.stroke();                                               // thumb over the rim
    g.beginPath(); g.moveTo(40, -24); g.quadraticCurveTo(46, -16, 40, -10); g.stroke();
    g.restore();
  }
  // ear + hoop earring
  celShape(g, gg => { gg.moveTo(8, 18); gg.bezierCurveTo(-4, 0, -24, 10, -20, 44); gg.bezierCurveTo(-18, 70, 0, 82, 12, 72); gg.closePath(); }, skin, P.ink, lw * .8);
  g.beginPath(); g.moveTo(-4, 34); g.quadraticCurveTo(-12, 46, -4, 60); g.strokeStyle = skinSh; g.lineWidth = lw * .8; g.stroke();
  g.beginPath(); g.ellipse(2, 104, 13, 22, .15, 0, TAU); g.strokeStyle = '#ffc24a'; g.lineWidth = lw * 1.6; g.stroke();
  // hair cap + front strands
  celShape(g, hairCapPath, HAIR.base, null);
  g.save(); g.beginPath(); g.rect(-75, -400, 600, 700); g.clip(); g.beginPath(); hairCapPath(g); g.lineWidth = lw; g.strokeStyle = P.ink; g.lineJoin = 'round'; g.stroke(); g.restore();
  celClip(g, hairCapPath, gg => {
    gg.fillStyle = HAIR.mid; gg.beginPath(); gg.ellipse(40, -150, 110, 40, -.15, 0, TAU); gg.fill();
    // glossy highlight band (the classic angel ring), zig-zag lower edge
    gg.fillStyle = HAIR.hi; gg.beginPath(); gg.moveTo(-70, -178); gg.quadraticCurveTo(20, -205, 100, -160);
    for (let i = 0; i < 7; i++) { const u = i / 6; gg.lineTo(lerp(100, -70, u), lerp(-160, -178, u) + (i % 2 ? 16 : 0) + 12); }
    gg.closePath(); gg.fill();
  });
  for (const s of STRANDS) if (!s.back) strand(g, s.ax, s.ay, s.len, s.wid, s.ph, tc, s.amp, s.lift, s.ay > 0 ? HAIR.base : HAIR.mid, s.ay < 40 ? HAIR.hi : HAIR.rim, lw);
  // bangs blown back
  const wob = Math.sin(TAU * tc * 3) * 5;
  celShape(g, gg => { gg.moveTo(134, -98); gg.bezierCurveTo(146, -120, 110, -150, 70, -160); gg.bezierCurveTo(100, -130, 120, -110, 118 + wob, -70); gg.closePath(); }, HAIR.base, P.ink, lw * .9);
  celShape(g, gg => { gg.moveTo(92, -150); gg.bezierCurveTo(60, -120, 50, -80, 44 - wob, -40); gg.bezierCurveTo(70, -80, 90, -110, 128, -118); gg.closePath(); }, HAIR.mid, P.ink, lw * .9);
  // face details
  if (o.detail !== false) {
    g.lineCap = 'round'; g.lineJoin = 'round';
    g.strokeStyle = P.ink; g.lineWidth = lw * .9; g.beginPath(); g.moveTo(100, -58); g.quadraticCurveTo(125, -64, 146, -50); g.stroke();   // brow
    if (blink > .5) {
      g.lineWidth = lw * 1.4; g.beginPath(); g.moveTo(102, -8); g.quadraticCurveTo(122, 4, 140, -2); g.stroke();
      g.lineWidth = lw; g.beginPath(); g.moveTo(104, -6); g.lineTo(92, -14); g.stroke();
    } else {
      g.save(); g.translate(120, -6); g.scale(1.22, 1.22); g.translate(-120, 6);
      // eye (profile wedge): white, big teal iris with twin highlights, heavy upper lash line
      const eye = gg => { gg.moveTo(100, -26); gg.quadraticCurveTo(124, -32, 142, -14); gg.quadraticCurveTo(138, 4, 132, 10); gg.quadraticCurveTo(116, 14, 106, 8); gg.closePath(); };
      celShape(g, eye, '#fff8f2', null);
      celClip(g, eye, gg => {
        gg.fillStyle = '#1f4a5c'; gg.beginPath(); gg.ellipse(127, -6, 12, 22, 0, 0, TAU); gg.fill();
        gg.fillStyle = '#4fb0b4'; gg.beginPath(); gg.ellipse(127, 2, 9, 12, 0, 0, TAU); gg.fill();
        gg.fillStyle = '#10222e'; gg.beginPath(); gg.ellipse(128, -8, 5, 11, 0, 0, TAU); gg.fill();
        gg.fillStyle = '#fff'; gg.beginPath(); gg.ellipse(131, -16, 4, 6, .3, 0, TAU); gg.fill(); gg.beginPath(); gg.arc(123, 6, 2.5, 0, TAU); gg.fill();
        gg.fillStyle = 'rgba(160,110,190,.45)'; gg.fillRect(96, -32, 50, 12);
      });
      g.lineWidth = lw * 1.8; g.beginPath(); g.moveTo(98, -24); g.quadraticCurveTo(124, -34, 143, -14); g.stroke();
      g.lineWidth = lw * 1.1; g.beginPath(); g.moveTo(100, -24); g.lineTo(86, -34); g.moveTo(104, -27); g.lineTo(94, -40); g.stroke();
      g.lineWidth = lw * .7; g.beginPath(); g.moveTo(108, 9); g.quadraticCurveTo(120, 14, 131, 10); g.stroke();
      g.restore();
    }
    // nostril, lips, blush hatching
    g.lineWidth = lw * .7; g.beginPath(); g.moveTo(166, 52); g.quadraticCurveTo(170, 56, 166, 58); g.stroke();
    g.lineWidth = lw * .9; g.beginPath(); g.moveTo(152, 93); g.quadraticCurveTo(142, 92 - smile * 8, 136, 88 - smile * 10); g.stroke();
    g.fillStyle = '#e8707e'; g.beginPath(); g.moveTo(152, 94); g.bezierCurveTo(158, 97, 161, 103, 156, 107); g.quadraticCurveTo(150, 102, 152, 94); g.fill();
    g.strokeStyle = '#ee7f8e'; g.lineWidth = lw * .8;
    for (let i = 0; i < 4; i++) { g.beginPath(); g.moveTo(92 + i * 11, 36); g.lineTo(84 + i * 11, 50); g.stroke(); }
  }
}
