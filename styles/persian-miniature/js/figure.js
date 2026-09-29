// figure.js · the gardener: a slender young man in a knee-length qaba, sash, trousers, pointed shoes and a white turban,
// carrying a small blue ewer. Walks to the right; phase is driven by distance so feet do not slide.
const FIG = { L1: 36, L2: 34, foot: 4, cyc: 0 };
FIG.cyc = 4 * (FIG.L1 + FIG.L2) * Math.sin(0.45);   // ground covered per full stride cycle
const SKIN = '#f2d6b6', SKIND = '#c99a78';

function legPose(ph, amp, rest = 0) {
  const th = 0.45 * amp * Math.sin(ph) + rest * (1 - amp);
  const kn = amp * (0.06 + 0.75 * Math.pow(Math.max(0, Math.cos(ph)), 1.6));
  const kx = FIG.L1 * Math.sin(th), ky = FIG.L1 * Math.cos(th);
  const sa = th - kn, ax = kx + FIG.L2 * Math.sin(sa), ay = ky + FIG.L2 * Math.cos(sa);
  // toe lifts while the foot swings forward
  const lift = amp * Math.max(0, Math.cos(ph)) * 0.35;
  return { kx, ky, ax, ay, fa: -lift + Math.max(0, -Math.sin(ph)) * amp * 0.25 * (Math.cos(ph) < 0 ? 1 : 0) };
}
function drawLeg(g, hx, hy, p, near) {
  const trouser = near ? COL.lapisL : '#4768b4', shoe = near ? COL.ochre : COL.ochreD;
  const K = [hx + p.kx, hy + p.ky], A = [hx + p.ax, hy + p.ay];
  g.lineCap = 'round'; g.lineJoin = 'round';
  // outline stroke then fill stroke (tapered: thigh 13, shin 9)
  g.strokeStyle = COL.ink; g.lineWidth = 15; g.beginPath(); g.moveTo(hx, hy); g.lineTo(K[0], K[1]); g.stroke();
  g.lineWidth = 11; g.beginPath(); g.moveTo(K[0], K[1]); g.lineTo(A[0], A[1]); g.stroke();
  g.strokeStyle = trouser; g.lineWidth = 12.4; g.beginPath(); g.moveTo(hx, hy); g.lineTo(K[0], K[1]); g.stroke();
  g.lineWidth = 8.4; g.beginPath(); g.moveTo(K[0], K[1]); g.lineTo(A[0], A[1]); g.stroke();
  // knee crease + ankle cuff
  g.strokeStyle = 'rgba(20,30,70,0.55)'; g.lineWidth = 1.2; g.beginPath(); g.arc(K[0] + 1, K[1], 4, -0.3, 1.6); g.stroke();
  g.strokeStyle = COL.white; g.lineWidth = 2; const cx = A[0] - (A[0] - K[0]) * 0.15, cy = A[1] - (A[1] - K[1]) * 0.15; g.beginPath(); g.moveTo(cx - 4, cy); g.lineTo(cx + 4, cy); g.stroke();
  // pointed shoe with curled toe
  g.save(); g.translate(A[0], A[1]); g.rotate(p.fa);
  g.beginPath(); g.moveTo(-6, -3); g.quadraticCurveTo(-7, 4, -2, 4.5); g.lineTo(13, 4.5); g.quadraticCurveTo(19, 3, 20, -2); g.quadraticCurveTo(16, 0, 11, -1); g.lineTo(3, -4); g.closePath();
  g.fillStyle = shoe; g.fill(); g.strokeStyle = COL.ink; g.lineWidth = 1.4; g.stroke(); g.restore();
}
// arm from shoulder S: upper angle a1 (0 = straight down, + = forward), elbow bend b (+ = forearm forward)
function drawArm(g, sx, sy, a1, b, near, holdEwer, swing) {
  const U = 30, F = 27, E = [sx + U * Math.sin(a1), sy + U * Math.cos(a1)], a2 = a1 + b, Hn = [E[0] + F * Math.sin(a2), E[1] + F * Math.cos(a2)];
  const robe = near ? COL.verm : COL.vermD;
  g.lineCap = 'round';
  g.strokeStyle = COL.ink; g.lineWidth = 13; g.beginPath(); g.moveTo(sx, sy); g.lineTo(E[0], E[1]); g.lineTo(Hn[0], Hn[1]); g.stroke();
  g.strokeStyle = robe; g.lineWidth = 10.4; g.beginPath(); g.moveTo(sx, sy); g.lineTo(E[0], E[1]); g.lineTo(Hn[0], Hn[1]); g.stroke();
  // gold cuff
  const cx = lerp(E[0], Hn[0], 0.86), cy = lerp(E[1], Hn[1], 0.86);
  g.strokeStyle = COL.g1; g.lineWidth = 10.4; g.beginPath(); g.moveTo(lerp(E[0], Hn[0], 0.8), lerp(E[1], Hn[1], 0.8)); g.lineTo(cx, cy); g.stroke();
  // elbow crease
  g.strokeStyle = 'rgba(80,15,5,0.6)'; g.lineWidth = 1.2; g.beginPath(); g.arc(E[0], E[1], 3.5, a1 + 0.6, a1 + 2.2); g.stroke();
  if (holdEwer) {
    // ewer hangs from the hand by its handle, swinging a little
    g.save(); g.translate(Hn[0] + Math.sin(a2) * 3, Hn[1] + Math.cos(a2) * 3); g.rotate(swing);
    g.beginPath(); g.moveTo(-3, 2); g.bezierCurveTo(-14, 8, -15, 26, -6, 32); g.lineTo(8, 32); g.bezierCurveTo(17, 26, 16, 8, 5, 2); g.closePath();
    g.fillStyle = COL.lapisL; g.fill(); g.strokeStyle = COL.lapisD; g.lineWidth = 1.4; g.stroke();
    g.strokeStyle = COL.white; g.lineWidth = 1.2; g.beginPath(); g.moveTo(-10, 16); g.lineTo(12, 16); g.stroke();
    g.beginPath(); g.moveTo(10, 10); g.quadraticCurveTo(22, 6, 24, -2); g.strokeStyle = COL.lapisD; g.lineWidth = 3; g.stroke();   // spout
    g.fillStyle = COL.g1; g.fillRect(-4, -1, 10, 4);
    g.restore();
  }
  // hand: small palm with thumb
  g.save(); g.translate(Hn[0], Hn[1]); g.rotate(-a2);
  g.beginPath(); g.ellipse(0, 3, 3.6, 5.2, 0, 0, TAU); g.fillStyle = SKIN; g.fill(); g.strokeStyle = SKIND; g.lineWidth = 1; g.stroke();
  g.beginPath(); g.ellipse(3, 1, 1.6, 3, -0.5, 0, TAU); g.fill(); g.stroke(); g.restore();
  return Hn;
}
function drawHead(g, x, y, look) {
  g.save(); g.translate(x, y); g.rotate(-look);
  // neck
  g.fillStyle = SKIN; g.fillRect(-4, 4, 9, 12); g.strokeStyle = SKIND; g.lineWidth = 1; g.beginPath(); g.moveTo(5, 6); g.lineTo(5, 15); g.stroke();
  // hair at the nape
  g.fillStyle = COL.ink; g.beginPath(); g.ellipse(-6, 2, 6, 8, 0.2, 0, TAU); g.fill();
  // face in three-quarter view, turned right
  g.beginPath(); g.moveTo(-7, -4); g.bezierCurveTo(-8, 8, -2, 13, 3, 13); g.bezierCurveTo(7, 13, 10, 9, 10, 6);
  g.lineTo(12.5, 2.5); g.lineTo(10, 1.2); g.bezierCurveTo(10.5, -3, 9, -9, 3, -10); g.bezierCurveTo(-3, -10, -7, -8, -7, -4); g.closePath();
  g.fillStyle = SKIN; g.fill(); g.strokeStyle = SKIND; g.lineWidth = 1.2; g.stroke();
  g.fillStyle = COL.ink; g.beginPath(); g.ellipse(6, -1.8, 1.8, 1.1, 0, 0, TAU); g.fill();   // almond eye
  g.strokeStyle = COL.ink; g.lineWidth = 1.1; g.beginPath(); g.moveTo(2.5, -4.5); g.quadraticCurveTo(6, -6.5, 9.5, -4.8); g.stroke();   // arched brow
  g.strokeStyle = '#b5524a'; g.lineWidth = 1.3; g.beginPath(); g.moveTo(6, 8); g.lineTo(9, 7.6); g.stroke();   // mouth
  g.strokeStyle = SKIND; g.lineWidth = 1; g.beginPath(); g.arc(-2, 1, 2.6, -1.2, 1.4); g.stroke();   // ear
  g.fillStyle = COL.ink; g.beginPath(); g.moveTo(-7, -4); g.quadraticCurveTo(-4, 2, -1, 1); g.lineTo(-1, -6); g.fill();   // sideburn
  // white turban: wrapped folds, a gold pin and a dark aigrette plume
  g.beginPath(); g.moveTo(-10, -4); g.bezierCurveTo(-14, -20, -2, -27, 6, -25); g.bezierCurveTo(14, -23, 16, -12, 11, -5); g.bezierCurveTo(4, -9, -4, -8, -10, -4); g.closePath();
  g.fillStyle = COL.white; g.fill(); g.strokeStyle = '#8f8a80'; g.lineWidth = 1.2; g.stroke();
  g.strokeStyle = '#b4ada0'; g.lineWidth = 1;
  for (let k = 0; k < 3; k++) { g.beginPath(); g.moveTo(-10 + k * 2, -7 - k * 5); g.quadraticCurveTo(2, -14 - k * 5, 12, -8 - k * 5); g.stroke(); }
  g.fillStyle = COL.g1; g.beginPath(); g.arc(8, -17, 2.4, 0, TAU); g.fill(); g.strokeStyle = COL.g4; g.lineWidth = 0.8; g.stroke();
  g.strokeStyle = COL.ink; g.lineWidth = 1.6; g.beginPath(); g.moveTo(8, -18); g.quadraticCurveTo(12, -28, 18, -32); g.stroke();
  g.lineWidth = 1; for (let k = 0; k < 5; k++) { g.beginPath(); g.moveTo(10 + k * 1.5, -21 - k * 2); g.lineTo(14 + k * 1.4, -20 - k * 2.6); g.stroke(); }
  g.restore();
}
// x,y: position of the feet on the ground; ph: stride phase; amp: 0 standing … 1 walking; look: head tilt up
function drawFigure(g, x, y, ph, amp, t, look = 0) {
  const pN = legPose(ph, amp, 0.06), pF = legPose(ph + Math.PI, amp, -0.1);
  const hipY = y - FIG.foot - Math.max(pN.ay, pF.ay);
  const hx = x, hy = hipY, lean = 0.05 * amp;
  const sx = hx + 6 + lean * 50, sy = hy - 50, breath = Math.sin(t * 2.4) * 0.6 * (1 - amp);
  g.save();
  // soft contact shadow (painted miniature: a faint ground wash)
  g.fillStyle = 'rgba(40,40,20,0.14)'; g.beginPath(); g.ellipse(x + 4, y + 1, 26, 4.5, 0, 0, TAU); g.fill();
  // far arm (mostly hidden), far leg
  drawArm(g, sx - 5, sy + 4, 0.35 * amp * Math.sin(ph), 0.35 + 0.2 * amp, false, false, 0);
  drawLeg(g, hx - 2, hy, pF, false);
  drawLeg(g, hx + 2, hy, pN, true);
  // skirt of the qaba, flaring to just above the knees; hem follows the legs
  const kxs = [hx + pN.kx, hx + pF.kx], hemY = hy + 28, hemL = Math.min(...kxs) - 13, hemR = Math.max(...kxs) + 11;
  g.beginPath(); g.moveTo(hx - 12, hy - 8); g.lineTo(hx + 13, hy - 8);
  g.quadraticCurveTo(hemR + 2, hy + 10, hemR, hemY - 1); g.quadraticCurveTo((hemL + hemR) / 2, hemY + 4, hemL, hemY);
  g.quadraticCurveTo(hemL + 2, hy + 8, hx - 12, hy - 8); g.closePath();
  g.fillStyle = COL.verm; g.fill(); g.strokeStyle = COL.ink; g.lineWidth = 1.6; g.stroke();
  g.strokeStyle = COL.g1; g.lineWidth = 2.4; g.beginPath(); g.moveTo(hemR, hemY - 3); g.quadraticCurveTo((hemL + hemR) / 2, hemY + 1, hemL + 1, hemY - 2.5); g.stroke();
  g.strokeStyle = COL.vermD; g.lineWidth = 1.2; g.beginPath(); g.moveTo(hx + 2, hy - 6); g.lineTo(lerp(hemL, hemR, 0.55), hemY - 2); g.stroke();
  // torso (fitted), slight forward lean
  g.beginPath(); g.moveTo(hx - 11, hy - 8); g.lineTo(hx + 12, hy - 8); g.quadraticCurveTo(sx + 14, sy + 24, sx + 10, sy + 2 - breath);
  g.quadraticCurveTo(sx - 2, sy - 5 - breath, sx - 15, sy + 1 - breath); g.quadraticCurveTo(hx - 15, hy - 30, hx - 11, hy - 8); g.closePath();
  g.fillStyle = COL.verm; g.fill(); g.strokeStyle = COL.ink; g.lineWidth = 1.6; g.stroke();
  // gold floral dots on the robe
  g.fillStyle = COL.g1; for (const [dx, dy] of [[-4, -26], [5, -38], [-6, -44], [4, -18], [-2, 10], [8, 16], [-8, 20]]) { g.beginPath(); g.arc(hx + dx + (dy < 0 ? lean * (-dy) : 0), hy + dy, 1.6, 0, TAU); g.fill(); }
  // crossover front edge + white collar
  g.strokeStyle = COL.g1; g.lineWidth = 2; g.beginPath(); g.moveTo(sx + 6, sy + 4); g.quadraticCurveTo(hx + 8, hy - 28, hx + 11, hy - 9); g.stroke();
  g.fillStyle = COL.white; g.beginPath(); g.moveTo(sx - 3, sy - 3); g.lineTo(sx + 8, sy + 1); g.lineTo(sx + 4, sy + 8); g.closePath(); g.fill();
  // sash with a hanging end
  g.fillStyle = COL.ochre; g.beginPath(); g.moveTo(hx - 12, hy - 14); g.lineTo(hx + 13, hy - 14); g.lineTo(hx + 13, hy - 6); g.lineTo(hx - 12, hy - 6); g.closePath(); g.fill(); g.strokeStyle = COL.ochreD; g.lineWidth = 1.2; g.stroke();
  const sw = Math.sin(ph * 2) * 2 * amp;
  g.fillStyle = COL.ochre; g.beginPath(); g.moveTo(hx - 6, hy - 8); g.lineTo(hx - 12 - sw, hy + 16); g.lineTo(hx - 6 - sw, hy + 18); g.lineTo(hx - 1, hy - 7); g.closePath(); g.fill(); g.stroke();
  // head
  drawHead(g, sx - 1, sy - 16 - breath, look);
  // near arm holding the ewer, swinging opposite the near leg
  const a1 = -0.34 * amp * Math.sin(ph) + 0.06, b = 0.28 + 0.12 * amp * Math.max(0, -Math.sin(ph));
  drawArm(g, sx + 2, sy + 5, a1, b, true, true, -a1 * 0.8 + Math.sin(ph + 0.8) * 0.08 * amp);
  g.restore();
}
