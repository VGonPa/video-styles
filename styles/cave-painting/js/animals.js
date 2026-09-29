// cave-painting: profile animals in the Paleolithic manner (unit space: tail at -x, head at +x, y down).
// Ochre body wash, charcoal contour, dark legs with superimposed "flip-book" leg positions.
'use strict';
const PIG = { red: [154, 58, 34], yel: [201, 145, 58], char: [35, 26, 21], brown: [110, 56, 32] };
const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;

const SHAPES = {
  horse: {
    body: [[-0.78, -0.2], [-0.62, -0.31], [-0.3, -0.27], [-0.05, -0.25], [0.22, -0.33], [0.42, -0.5], [0.6, -0.68], [0.72, -0.76], [0.8, -0.72],
      [0.9, -0.58], [1.0, -0.43], [0.99, -0.33], [0.86, -0.33], [0.72, -0.34], [0.62, -0.24], [0.57, -0.02], [0.42, 0.12], [0.1, 0.2], [-0.25, 0.18], [-0.52, 0.1], [-0.72, 0.02], [-0.84, -0.08]],
    front: [0.44, 0.06], hind: [-0.56, 0.02], l1: 0.3, l2: 0.3, lw: [0.13, 0.085, 0.06],
    extra(ctx, s) {
      // erect mane: short charcoal hatches along the neck crest
      ctx.fillStyle = rgba(PIG.char, 0.9);
      for (let i = 0; i <= 11; i++) { const k = i / 11, x = lerp(0.2, 0.74, k), y = lerp(-0.34, -0.78, k) - 0.03 * Math.sin(k * 3);
        taper(ctx, [[x, y + 0.04], [x - 0.03, y - 0.07]], [0.05, 0.02]); }
      // tail
      ctx.fillStyle = rgba(PIG.char, 0.85); taper(ctx, [[-0.76, -0.2], [-0.95, -0.12], [-1.05, 0.05], [-1.08, 0.25]], [0.08, 0.11, 0.08, 0.02]);
      // eye + ear
      ctx.beginPath(); ctx.arc(0.8, -0.6, 0.025, 0, 7); ctx.fill();
      taper(ctx, [[0.73, -0.74], [0.7, -0.86]], [0.06, 0.015]);
    }
  },
  aurochs: {
    body: [[-0.82, -0.22], [-0.66, -0.3], [-0.35, -0.3], [-0.05, -0.36], [0.2, -0.5], [0.38, -0.55], [0.56, -0.47], [0.7, -0.37], [0.8, -0.3],
      [0.92, -0.16], [1.0, 0.0], [0.98, 0.08], [0.88, 0.08], [0.76, 0.06], [0.66, 0.16], [0.58, 0.3], [0.4, 0.3], [0.1, 0.26], [-0.25, 0.24], [-0.52, 0.2], [-0.7, 0.1], [-0.84, -0.06]],
    front: [0.42, 0.24], hind: [-0.6, 0.14], l1: 0.25, l2: 0.24, lw: [0.09, 0.06, 0.045],
    extra(ctx, s) {
      ctx.fillStyle = rgba(PIG.char, 0.92);
      // lyre horns sweeping forward and up
      taper(ctx, [[0.78, -0.33], [0.84, -0.46], [0.94, -0.56], [1.06, -0.58], [1.14, -0.52]], [0.06, 0.05, 0.04, 0.026, 0.01]);
      taper(ctx, [[0.72, -0.37], [0.74, -0.5], [0.82, -0.62], [0.93, -0.67], [1.02, -0.64]], [0.05, 0.045, 0.035, 0.022, 0.01]);
      ctx.beginPath(); ctx.arc(0.84, -0.14, 0.02, 0, 7); ctx.fill();
      taper(ctx, [[-0.86, -0.2], [-0.98, -0.1], [-1.02, 0.1], [-1.0, 0.3]], [0.05, 0.04, 0.03, 0.06]);
    }
  },
  deer: {
    body: [[-0.74, -0.26], [-0.84, -0.36], [-0.7, -0.33], [-0.4, -0.27], [-0.05, -0.26], [0.28, -0.31], [0.45, -0.45], [0.58, -0.66], [0.66, -0.8],
      [0.78, -0.8], [0.9, -0.72], [0.99, -0.67], [0.96, -0.6], [0.8, -0.6], [0.66, -0.48], [0.58, -0.22], [0.48, 0.0], [0.28, 0.08], [-0.1, 0.1], [-0.45, 0.06], [-0.68, -0.04], [-0.78, -0.15]],
    front: [0.42, 0.0], hind: [-0.56, -0.02], l1: 0.34, l2: 0.38, lw: [0.1, 0.06, 0.04],
    extra(ctx, s) {
      ctx.fillStyle = rgba(PIG.char, 0.92);
      // branching antlers
      const beam = [[0.7, -0.8], [0.62, -0.98], [0.5, -1.14], [0.36, -1.26], [0.2, -1.32]];
      taper(ctx, beam, [0.045, 0.04, 0.034, 0.026, 0.012]);
      for (const [i, dx, dy] of [[1, 0.14, -0.1], [2, 0.12, -0.16], [3, 0.08, -0.18], [2, -0.04, 0.1]]) {
        const b = beam[i]; taper(ctx, [b, [b[0] + dx * 0.6, b[1] + dy * 0.7], [b[0] + dx, b[1] + dy]], [0.03, 0.02, 0.008]);
      }
      taper(ctx, [[0.66, -0.82], [0.56, -0.9]], [0.05, 0.015]);
      ctx.beginPath(); ctx.arc(0.82, -0.72, 0.02, 0, 7); ctx.fill();
    }
  }
};
// four flip-book gait drawings: [front a1, a2, hind a1, a2] (radians from vertical, + = toward head)
const GAIT = [[1.0, 1.3, -1.0, -1.35], [0.35, -0.25, -0.3, 0.35], [-0.05, -1.15, 0.65, 0.05], [-0.45, -0.3, 0.25, -0.5]];
function legPts(root, a1, a2, l1, l2) {
  const k = [root[0] + l1 * Math.sin(a1), root[1] + l1 * Math.cos(a1)], h = [k[0] + l2 * Math.sin(a2), k[1] + l2 * Math.cos(a2)];
  return [root, k, h, [h[0] + 0.035 * Math.cos(a2), h[1] - 0.02]];
}
function poseAt(p, amp) {
  const i = Math.floor(p) % 4, f = p - Math.floor(p), a = GAIT[i], b = GAIT[(i + 1) % 4];
  return a.map((v, j) => lerp(v, b[j], f) * amp);
}
function drawLegs(ctx, sh, pose, alpha, dxRoot, dark) {
  ctx.fillStyle = rgba(dark ? [22, 16, 13] : PIG.char, alpha);
  const [w0, w1, w2] = sh.lw;
  const F = legPts([sh.front[0] + dxRoot, sh.front[1]], pose[0], pose[1], sh.l1, sh.l2);
  const Hh = legPts([sh.hind[0] + dxRoot, sh.hind[1]], pose[2], pose[3], sh.l1 * 1.05, sh.l2);
  taper(ctx, F, [w0, w1, w2, w2 * 0.6]); taper(ctx, Hh, [w0 * 1.15, w1, w2, w2 * 0.6]);
}
// a: {kind, x, y, s, dir, fill, shade, alpha, phase, amp, ghosts}
function drawAnimal(ctx, a) {
  const sh = SHAPES[a.kind];
  ctx.save(); ctx.translate(a.x, a.y); ctx.scale(a.s * a.dir, a.s); ctx.globalAlpha = a.alpha ?? 1;
  const amp = a.amp ?? 1, near = poseAt(a.phase, amp), far = poseAt(a.phase + 0.5, amp);
  // far legs behind the body
  drawLegs(ctx, sh, far, 0.8, a.farDx ?? 0.07, true);
  // body wash
  ctx.beginPath(); smoothClosed(ctx, sh.body); ctx.fillStyle = rgba(a.fill, 0.88); ctx.fill();
  ctx.save(); ctx.clip();
  // bichrome shading: charcoal along the back/head, lighter belly (as in Magdalenian painting)
  const g = ctx.createLinearGradient(0, -0.8, 0, 0.25); g.addColorStop(0, rgba(PIG.char, a.shade)); g.addColorStop(0.55, rgba(PIG.char, a.shade * 0.25)); g.addColorStop(1, rgba([226, 196, 150], 0.18));
  ctx.fillStyle = g; ctx.fillRect(-1.2, -1.2, 2.4, 2.4);
  if (a.kind === 'aurochs') { const r = ctx.createRadialGradient(0.85, -0.12, 0.02, 0.85, -0.12, 0.4); r.addColorStop(0, rgba(PIG.char, 0.8)); r.addColorStop(1, rgba(PIG.char, 0)); ctx.fillStyle = r; ctx.fillRect(0.3, -0.8, 1, 1.2); }
  ctx.restore();
  // charcoal contour, drawn twice slightly offset like a re-traced line
  ctx.strokeStyle = rgba(PIG.char, 0.85); ctx.lineJoin = 'round';
  for (const [ox, oy, lw] of [[0, 0, 5.5], [0.006, -0.005, 2.5]]) { ctx.save(); ctx.translate(ox, oy); ctx.lineWidth = lw / a.s; ctx.beginPath(); smoothClosed(ctx, sh.body); ctx.stroke(); ctx.restore(); }
  // superimposed ghost legs (the flip-book), then the active drawing
  if (a.ghosts) for (let k = 0; k < 4; k++) drawLegs(ctx, sh, GAIT[k].map(v => v * amp), a.ghosts, 0, false);
  drawLegs(ctx, sh, near, 0.95, 0, false);
  sh.extra(ctx, a.s);
  ctx.restore();
}
