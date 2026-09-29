// picture-book · characters: Fern the fox (side view, facing right) and Bear (sitting, three-quarter left), the blue button.
const C = {
  paper: '#f3ead8', ink: '#4a3426', fox: '#cf7440', foxD: '#9c5231', sock: '#5d3d2e', cream: '#f6e9d0',
  bear: '#8a5d40', bearL: '#c99a6c', bearD: '#5e3d2b', vest: '#b3593f', blue: '#5b84ad', blueD: '#3d5f85',
  pink: '#e39a8a', dark: '#3a2a22',
};

function drawButton(g, x, y, r, rot = 0, seed = 1) {
  g.save(); g.translate(x, y); g.rotate(rot);
  const p = ell(0, 0, r, r);
  paint(g, p, C.blue, seed, { edge: r * 0.28, edgeA: 0.5, mottle: 0.3, streak: 0.3, tsc: 0.4 });
  g.save(); g.globalAlpha = 0.35; g.strokeStyle = C.blueD; g.lineWidth = r * 0.14; g.beginPath(); g.arc(0, 0, r * 0.72, 0, TAU); g.stroke(); g.restore();
  g.fillStyle = rgba('#f6ecd6', 0.92); for (const [a, b] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) { g.beginPath(); g.arc(a * r * 0.24, b * r * 0.24, r * 0.12, 0, TAU); g.fill(); }
  g.fillStyle = 'rgba(255,250,235,0.45)'; g.beginPath(); g.ellipse(-r * 0.38, -r * 0.45, r * 0.28, r * 0.14, -0.6, 0, TAU); g.fill();
  pencil(g, p, { w: Math.max(1.5, r * 0.12), a: 0.7, seed: seed + 2 });
  g.restore();
}

// ── fox ──
function foxPose(P) {
  const cr = P.crouch ?? 0, walk = P.walk ?? 0;
  const bob = -walk * Math.abs(Math.sin(P.ph ?? 0)) * 6 + (P.breathe ?? 0) * 2.2 + (P.squash ?? 0) * 8;
  const by = -92 + cr * 52 + bob;
  const hu = P.headUp ?? 1;
  const neck = [lerp(76, 70, hu), lerp(-40, by - 26, hu)];
  const ang = lerp(0.42, -0.06, hu) + (P.headAng ?? 0);
  return { by, neck, ang };
}
function foxMouthLocal(P) { const { neck, ang } = foxPose(P); const c = Math.cos(ang), s = Math.sin(ang);
  return [neck[0] + c * 70 - s * 12, neck[1] + s * 70 + c * 12]; }

function foxLeg(g, hip, foot, back, seed, far) {
  const kx = (hip[0] + foot[0]) / 2 + (back ? -9 : 4), ky = (hip[1] + foot[1]) / 2;
  const cen = sampleSpline([hip, [kx, ky], foot], 9);
  const up = poly(ribbon(cen, [15, 14, 13, 11.5, 10, 9, 8.5, 8, 7.5]));
  const col = far ? shade(C.fox, 0.8) : C.fox;
  paint(g, up, col, seed, { edge: 5 });
  const low = poly(ribbon(cen.slice(4), [10.2, 9.4, 8.8, 8.4, 8]));
  paint(g, low, far ? shade(C.sock, 0.85) : C.sock, seed + 1, { edge: 3, mottle: 0.3 });
  const paw = ell(foot[0] + 5, foot[1] - 4, 11, 6.5);
  paint(g, paw, far ? shade(C.sock, 0.85) : C.sock, seed + 2, { edge: 3, mottle: 0.3 });
  pencil(g, up, { w: 2.4, a: 0.55, seed });
}

function drawFox(g, x, y, s, P) {
  const { by, neck, ang } = foxPose(P);
  const cr = P.crouch ?? 0, walk = P.walk ?? 0, ph = P.ph ?? 0;
  g.save(); g.translate(x, y); g.scale(s, s);
  // soft contact shadow
  g.save(); g.fillStyle = 'rgba(70,50,30,0.16)'; g.beginPath(); g.ellipse(0, 2, 120 + cr * 30, 10, 0, 0, TAU); g.fill(); g.restore();
  const legs = (far) => {
    const defs = far ? [[-40, 12, Math.PI, true], [62, 10, 0, false]] : [[-54, 16, 0, true], [48, 14, Math.PI, false]];
    for (const [hx, hy, off, back] of defs) {
      const a = Math.sin(ph + off) * 0.48 * walk, lift = Math.max(0, Math.cos(ph + off)) * 15 * walk;
      const hip = [hx, by + hy], L = -hip[1];
      const tuck = cr * (back ? 18 : 30);
      const foot = [hx + Math.sin(a) * L + tuck, -lift - (far ? 3 : 0)];
      foxLeg(g, hip, foot, back, 100 + hx | 0, far);
    }
  };
  legs(true);
  // tail (behind the body once it has swung up past the rump, in front while wrapped round her)
  const tw = P.tail ?? 1, wag = P.wag ?? 0;
  const up = [[-84, by - 10], [-130, by - 32], [-176, by - 44], [-216, by - 36], [-244, by - 14]];
  const wr = [[-84, by + 4], [-104, by + 30], [-50, by + 38], [30, by + 36], [100, by + 26]];
  const base = up[0];
  const ctr = up.map((p, i) => { const q = [lerp(wr[i][0], p[0], tw), lerp(wr[i][1], p[1], tw)];
    const a = wag * (i / 4), dx = q[0] - base[0], dy = q[1] - base[1];
    return [base[0] + dx * Math.cos(a) - dy * Math.sin(a), base[1] + dx * Math.sin(a) + dy * Math.cos(a)]; });
  const drawTail = () => {
  const cs = sampleSpline(ctr, 22), wf = u => 8 + 30 * Math.pow(Math.sin(Math.PI * Math.pow(u, 0.8)), 0.75);
  const tail = poly(ribbon(cs, cs.map((_, i) => wf(i / 21))));
  paint(g, tail, C.fox, 31, { edge: 9 });
  g.save(); g.clip(tail);
  const tipI = 16; const tip = poly(ribbon(cs.slice(tipI), cs.slice(tipI).map((_, i) => wf((i + tipI) / 21) + 6)));
  paint(g, tip, C.cream, 32, { edge: 4, mottle: 0.2 });
  g.restore();
  hatch(g, tail, 33, { box: [-260, by - 80, 130, by + 60], sp: 12, ang: -0.5, len: 20, a: 0.22 });
  pencil(g, tail, { w: 3, seed: 34 });
  };
  if (tw > 0.5) drawTail();
  // body
  const B = [[-92, 4], [-84, -26], [-50, -40], [0, -37], [44, -44], [78, -30], [94, -6], [84, 22], [50, 36], [0, 38], [-50, 40], [-84, 28]].map(([a, b]) => [a, b + by]);
  const body = blob(B);
  paint(g, body, C.fox, 21, { edge: 10 });
  g.save(); g.clip(body);
  paint(g, blob([[56, by - 18], [100, by - 12], [96, by + 34], [48, by + 44], [36, by + 12]]), C.cream, 22, { edge: 5, mottle: 0.25 });
  paint(g, blob([[-70, by + 28], [0, by + 26], [60, by + 30], [60, by + 60], [-70, by + 60]]), shade(C.fox, 1.1), 23, { edge: 0, mottle: 0.25 });
  g.restore();
  hatch(g, body, 24, { box: [-100, by - 10, 70, by + 40], sp: 11, ang: -1.0, len: 22, a: 0.28 });
  pencil(g, body, { w: 3, seed: 25 });
  legs(false);
  if (tw <= 0.5) drawTail();
  // head
  g.save(); g.translate(neck[0], neck[1]); g.rotate(ang);
  const perk = P.perk ?? 1;
  const ear = (dx, dy, far) => {
    g.save(); g.translate(10 + dx, -38 + dy); g.rotate((1 - perk) * -0.55 + (far ? -0.12 : 0)); g.translate(-10, 38);
    const e = blob([[-10, -34], [-1, -66], [7, -90], [18, -66], [30, -36]]);
    paint(g, e, far ? C.foxD : C.fox, far ? 41 : 42, { edge: 5 });
    paint(g, blob([[0, -42], [7, -78], [18, -46]]), far ? shade(C.sock, 0.8) : C.sock, 43, { edge: 2, mottle: 0.2 });
    pencil(g, e, { w: 2.6, seed: 44 });
    g.restore();
  };
  ear(-20, 4, true);
  const head = blob([[-24, -6], [-18, -34], [4, -46], [30, -40], [54, -24], [76, -12], [90, -5], [86, 5], [64, 11], [36, 19], [8, 20], [-16, 12]]);
  paint(g, head, C.fox, 45, { edge: 8 });
  g.save(); g.clip(head);
  paint(g, blob([[-8, 15], [14, 3], [40, -1], [66, -3], [92, 1], [92, 26], [20, 32], [-12, 28]]), C.cream, 46, { edge: 4, mottle: 0.2 });
  g.restore();
  pencil(g, head, { w: 3, seed: 47 });
  ear(0, 0, false);
  // nose, eye, mouth
  g.fillStyle = C.dark; g.beginPath(); g.ellipse(87, -5, 7.5, 6, 0.2, 0, TAU); g.fill();
  const eo = P.eye ?? 1;
  if (eo > 0.25) {
    g.fillStyle = C.dark; g.beginPath(); g.ellipse(40, -21, 5, 6.5 * clamp(eo), 0, 0, TAU); g.fill();
    g.fillStyle = 'rgba(255,248,230,0.9)'; g.beginPath(); g.arc(41.8, -23.5, 1.7, 0, TAU); g.fill();
  } else {
    const p = new Path2D(); p.moveTo(33, -21); p.quadraticCurveTo(40, -15, 48, -21); pencil(g, p, { w: 2.8, seed: 48, a: 0.95 });
  }
  const m = new Path2D(); m.moveTo(84, 5); m.quadraticCurveTo(74, 10, 64, 8); pencil(g, m, { w: 2, seed: 49, a: 0.6 });
  // cheek blush
  g.fillStyle = rgba(C.pink, 0.28); g.beginPath(); g.ellipse(34, -4, 10, 6, 0, 0, TAU); g.fill();
  if (P.button) drawButton(g, 70, 12, 13, 0.3, 61);
  g.restore();
  g.restore();
}

// ── bear ──
function drawBear(g, x, y, s, P) {
  const hp = P.happy ?? 0, br = P.breathe ?? 0;
  g.save(); g.translate(x, y); g.scale(s, s);
  g.save(); g.fillStyle = 'rgba(60,40,25,0.18)'; g.beginPath(); g.ellipse(0, 2, 170, 14, 0, 0, TAU); g.fill(); g.restore();
  g.save(); g.translate(0, 0); g.scale(1 + br * 0.006, 1 - br * 0.004);
  const body = blob([[-122, -40], [-130, -120], [-110, -200], [-72, -250], [0, -264], [70, -252], [110, -200], [130, -120], [122, -40], [60, -10], [-60, -10]]);
  paint(g, body, C.bear, 71, { edge: 12 });
  g.save(); g.clip(body);
  paint(g, blob([[-42, -262], [42, -262], [30, -96], [-30, -96]]), C.bearL, 72, { edge: 4, mottle: 0.3 });
  const vl = blob([[-150, -96], [-150, -290], [-40, -290], [-7, -172], [-7, -96]], 0.35);
  const vr = blob([[7, -96], [7, -172], [40, -290], [150, -290], [150, -96]], 0.35);
  paint(g, vl, C.vest, 73, { edge: 8 }); paint(g, vr, shade(C.vest, 0.9), 74, { edge: 8 });
  pencil(g, vl, { w: 2.6, seed: 75, a: 0.6 }); pencil(g, vr, { w: 2.6, seed: 76, a: 0.6 });
  g.restore();
  hatch(g, body, 77, { box: [-140, -130, 140, -10], sp: 12, ang: -0.9, len: 24, a: 0.25 });
  pencil(g, body, { w: 3.2, seed: 78 });
  // buttons (the middle one is missing - loose thread cross)
  drawButton(g, -26, -206, 13, 0.2, 81);
  if (P.button) { const sc = P.btnScale ?? 1; g.save(); g.translate(-20, -163); g.scale(sc, sc); drawButton(g, 0, 0, 13, -0.3, 82); g.restore(); }
  else { const th = new Path2D(); th.moveTo(-27, -170); th.lineTo(-13, -156); th.moveTo(-13, -170); th.lineTo(-27, -156); th.moveTo(-20, -163); th.quadraticCurveTo(-10, -150, -16, -140); pencil(g, th, { w: 2, seed: 83, a: 0.7 }); }
  drawButton(g, -20, -120, 13, 0.5, 84);
  // feet
  for (const sx of [-1, 1]) {
    const f = ell(sx * 80, -30, 56, 34, sx * 0.12);
    paint(g, f, C.bear, 90 + sx, { edge: 8 });
    paint(g, ell(sx * 88, -32, 30, 21, sx * 0.12), C.bearL, 92 + sx, { edge: 4, mottle: 0.3 });
    for (const k of [-1, 0, 1]) { g.fillStyle = rgba(C.bearL, 0.95); g.beginPath(); g.ellipse(sx * 88 + k * 16, -58, 6, 5, 0, 0, TAU); g.fill(); }
    pencil(g, f, { w: 3, seed: 94 + sx });
  }
  // arms: hang along the sides, paws curled in on the tummy
  for (const sx of [-1, 1]) {
    const pts = [[66, -250], [100, -242], [122, -205], [126, -160], [112, -118], [90, -94], [60, -94], [50, -116], [76, -136], [88, -172], [80, -215]].map(([a, b]) => [a * sx, b]);
    const ap = blob(pts), wv = sx < 0 ? (P.wave ?? 0) : 0;
    g.save(); if (wv) { g.translate(-80, -228); g.rotate(wv); g.translate(80, 228); }
    paint(g, ap, shade(C.bear, 0.95), 96 + sx, { edge: 9 });
    paint(g, ell(sx * 74, -106, 20, 14, sx * 0.3), shade(C.bearL, 0.95), 98 + sx, { edge: 4, mottle: 0.3 });
    pencil(g, ap, { w: 2.8, seed: 99 + sx, a: 0.75 });
    g.restore();
  }
  g.restore();
  // head
  g.save(); g.translate(-8, -300 + br * 1.5); g.rotate(P.tilt ?? 0);
  for (const [ex, ey] of [[-64, -66], [60, -70]]) {
    const e = ell(ex, ey, 31, 29); paint(g, e, C.bear, 101 + ex, { edge: 8 });
    paint(g, ell(ex, ey + 2, 16, 14), C.bearL, 103, { edge: 3, mottle: 0.3 }); pencil(g, e, { w: 2.8, seed: 104 });
  }
  const head = wob(0, 0, 94, 84, 5, 0.035, 12);
  paint(g, head, C.bear, 105, { edge: 12 });
  const mz = ell(-26, 22, 46, 33, -0.05); paint(g, mz, C.bearL, 106, { edge: 6, mottle: 0.3 });
  pencil(g, head, { w: 3.2, seed: 107 }); pencil(g, mz, { w: 2.2, seed: 108, a: 0.55 });
  g.fillStyle = C.dark; g.beginPath(); g.ellipse(-32, 7, 16, 11, 0, 0, TAU); g.fill();
  g.fillStyle = 'rgba(255,248,230,0.5)'; g.beginPath(); g.ellipse(-37, 3, 5, 2.5, -0.3, 0, TAU); g.fill();
  const mo = new Path2D(); mo.moveTo(-32, 17); mo.lineTo(-32, 28);
  const cv = lerp(-5, 10, hp); mo.moveTo(-52, 32 - cv * 0.3); mo.quadraticCurveTo(-42, 30 + cv, -32, 28); mo.quadraticCurveTo(-22, 30 + cv, -12, 32 - cv * 0.3);
  pencil(g, mo, { w: 2.6, seed: 109, a: 0.9 });
  const ec = P.eyesClosed ?? 0;
  for (const [ex, ey] of [[-62, -20], [12, -24]]) {
    if (hp > 0.5 || ec > 0.5) {
      const p = new Path2D(); if (ec > 0.5) { p.moveTo(ex - 9, ey); p.quadraticCurveTo(ex, ey + 7, ex + 9, ey); } else { p.moveTo(ex - 9, ey + 3); p.quadraticCurveTo(ex, ey - 8, ex + 9, ey + 3); }
      pencil(g, p, { w: 3, seed: 110, a: 0.95 });
    } else {
      const bl = P.blink ?? 1;
      g.fillStyle = C.dark; g.beginPath(); g.ellipse(ex, ey, 7, 8 * bl, 0, 0, TAU); g.fill();
      g.fillStyle = 'rgba(255,248,230,0.9)'; g.beginPath(); g.arc(ex + 2, ey - 3, 2, 0, TAU); g.fill();
      // worried brows fade as he cheers up
      const b = new Path2D(); const dir = ex < -20 ? -1 : 1; b.moveTo(ex - 11, ey - 18 - dir * 4); b.lineTo(ex + 11, ey - 18 + dir * 4);
      pencil(g, b, { w: 2.4, seed: 111, a: 0.7 * (1 - hp) });
    }
  }
  g.fillStyle = rgba(C.pink, 0.15 + hp * 0.3);
  for (const [cx, cy] of [[-80, 12], [26, 8]]) { g.beginPath(); g.ellipse(cx, cy, 15, 9, 0, 0, TAU); g.fill(); }
  g.restore();
  g.restore();
}

function sparkle(g, x, y, r, a) {
  if (a <= 0) return;
  g.save(); g.translate(x, y); g.globalAlpha = a; g.fillStyle = '#fff8e6';
  g.beginPath(); for (let i = 0; i < 8; i++) { const rr = i % 2 ? r * 0.22 : r; const an = i / 8 * TAU - Math.PI / 2; g.lineTo(Math.cos(an) * rr, Math.sin(an) * rr); } g.closePath(); g.fill();
  g.globalAlpha = a * 0.8; g.strokeStyle = '#e8b85c'; g.lineWidth = 1.5; g.stroke();
  g.restore();
}
