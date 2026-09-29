// ── saturday-cartoon · shared helpers, the two characters and their props ──────────────────────────
// Everything is flat vector: bright fills, one cel-shadow tone, thick INK outline with round joins.
const W = 1920, H = 1080, DUR = 10.0, TAU = Math.PI * 2;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const sstep = (a, b, x) => { const u = seg(x, a, b); return u * u * (3 - 2 * u); };
const eOut = u => 1 - Math.pow(1 - clamp(u), 3);
const eIn = u => Math.pow(clamp(u), 3);
const eIO = u => { u = clamp(u); return u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2; };
const eBack = (u, k = 2.2) => { u = clamp(u); return 1 + (k + 1) * Math.pow(u - 1, 3) + k * Math.pow(u - 1, 2); };
const eElastic = u => { u = clamp(u); return u === 0 || u === 1 ? u : Math.pow(2, -8 * u) * Math.sin((u * 10 - .75) * TAU / 3) + 1; };
// damped wobble after an impact at time t0 (0 before t0)
const wob = (t, t0, f = 9, d = 7) => t < t0 ? 0 : Math.exp(-(t - t0) * d) * Math.sin((t - t0) * f * TAU);
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const mixHex = (a, b, u) => { const pa = parseInt(a.slice(1), 16), pb = parseInt(b.slice(1), 16), k = clamp(u);
  const ch = sh => Math.round(lerp((pa >> sh) & 255, (pb >> sh) & 255, k)); return `rgb(${ch(16)},${ch(8)},${ch(0)})`; };
const mk = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
const DISPLAY = '"Rammetto One"', ROUND = '"Sniglet"';
const INK = '#1b1030', LW = 9;

// fill + ink stroke of the current path
function fs(c, fill, lw = LW) {
  if (fill) { c.fillStyle = fill; c.fill(); }
  if (lw) { c.lineWidth = lw; c.strokeStyle = INK; c.lineJoin = 'round'; c.lineCap = 'round'; c.stroke(); }
}
function ell(c, x, y, rx, ry, fill, lw = LW, rot = 0) { c.beginPath(); c.ellipse(x, y, Math.max(.1, rx), Math.max(.1, ry), rot, 0, TAU); fs(c, fill, lw); }
// a limb: ink stroke under a colored stroke (so the outline is automatic)
function tube(c, pts, w, fill, lw = LW) {
  c.lineCap = 'round'; c.lineJoin = 'round';
  const path = () => { c.beginPath(); c.moveTo(pts[0][0], pts[0][1]);
    if (pts.length === 3) c.quadraticCurveTo(pts[1][0], pts[1][1], pts[2][0], pts[2][1]);
    else for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); };
  path(); c.strokeStyle = INK; c.lineWidth = w + lw * 2; c.stroke();
  path(); c.strokeStyle = fill; c.lineWidth = w; c.stroke();
}
function bez(p0, p1, p2, p3, u) { const v = 1 - u;
  return [v * v * v * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u * u * u * p3[0],
          v * v * v * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u * u * u * p3[1]]; }

/* ================================================================ SQUIRREL
 * "Nuts": hyper, orange, huge conjoined eyes, buck teeth, an S-curve tail twice his size.
 * Local units: feet on (0,0), facing +x, head top ≈ -300, tail top ≈ -330.
 * o: {x,y,s,dir,sq,lean,legs:'stand'|'run'|'skid',ph,arm:'down'|'hold'|'up'|'show'|'wave',
 *     look:[x,y],blink,wink,wide,mouth:'grin'|'o'|'gulp'|'yell',tail,item(c)} */
const FUR = '#ff7a1a', FUR_D = '#d6501c', FUR_L = '#ffa24a', CREAM = '#ffe6ad', NOSE = '#3a1426', PINK = '#ff8fb0';
function drawSquirrel(c, o) {
  const s = o.s || 1, dir = o.dir || 1, sq = o.sq || 1, ph = o.ph || 0;
  c.save(); c.translate(o.x, o.y); c.rotate((o.lean || 0) * dir); c.scale(dir * s / Math.sqrt(sq), s * sq);
  // ---- tail: chain of overlapping puffs along an S-curve (outline pass, fill pass, highlight pass)
  const tw = o.tail || 0;
  const P0 = [-30, -70], P1 = [-190, -40], P2 = [-250, -250], P3 = [-120, -330];
  const tp = [];
  for (let i = 0; i <= 22; i++) { const u = i / 22; const p = bez(P0, P1, P2, P3, u);
    const r = 26 + 40 * Math.pow(Math.sin(Math.PI * Math.min(1, u * 1.05)), .6) + (u > .9 ? 8 : 0);
    tp.push([p[0] + Math.sin(tw + u * 3.2) * 26 * u * u, p[1] + Math.cos(tw * .7 + u * 2) * 8 * u, r]); }
  const curl = [tp[22][0] + 30 + Math.sin(tw + 3.2) * 10, tp[22][1] + 34, 34];
  c.fillStyle = INK; for (const [x, y, r] of [...tp, curl]) { c.beginPath(); c.arc(x, y, r + LW, 0, TAU); c.fill(); }
  c.fillStyle = FUR_D; for (const [x, y, r] of [...tp, curl]) { c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill(); }
  c.fillStyle = FUR; for (const [x, y, r] of [...tp, curl]) { c.beginPath(); c.arc(x + 6, y - 6, r * .78, 0, TAU); c.fill(); }
  c.fillStyle = FUR_L; for (let i = 6; i < 22; i += 3) { const [x, y, r] = tp[i]; c.beginPath(); c.ellipse(x + 10, y - 14, r * .3, r * .16, -.6, 0, TAU); c.fill(); }
  // ---- legs
  const legs = o.legs || 'stand';
  if (legs === 'run') {
    // the classic cartoon "wheel" run: a blur loop with feet caught mid-spin
    c.save(); c.globalAlpha = .9; c.strokeStyle = INK; c.lineWidth = 5; c.lineCap = 'round';
    for (let k = 0; k < 3; k++) { c.beginPath(); c.ellipse(8, -40, 62 - k * 12, 34 - k * 7, 0, ph + k * 1.4, ph + k * 1.4 + 2.2); c.stroke(); }
    c.restore();
    for (let i = 0; i < 2; i++) { const a = ph * 1 + i * Math.PI; const fx = 8 + Math.cos(a) * 52, fy = -40 + Math.sin(a) * 30;
      tube(c, [[0, -78], [fx * .5, (fy - 78) / 2 + 6], [fx, fy]], 20, i ? FUR_D : FUR);
      ell(c, fx + 14, fy + 4, 28, 12, i ? FUR_D : FUR, 7, Math.sin(a) * .4); }
  } else if (legs === 'skid') {
    tube(c, [[-10, -70], [30, -40], [70, -10]], 22, FUR_D); ell(c, 88, -10, 30, 12, FUR_D, 7, -.3);
    tube(c, [[10, -70], [44, -44], [92, -14]], 22, FUR); ell(c, 110, -14, 30, 12, FUR, 7, -.3);
  } else {
    const hop = o.hop || 0;
    tube(c, [[-18, -70], [-14, -38], [-12, -14 - hop]], 22, FUR_D); ell(c, 2, -10 - hop, 30, 12, FUR_D, 7);
    tube(c, [[22, -70], [26, -38], [28, -14]], 22, FUR); ell(c, 44, -10, 30, 12, FUR, 7);
  }
  // ---- far arm
  const arm = o.arm || 'down';
  const handPos = { down: [52, -110], hold: [96, -170], up: [-6, -330], show: [120, -214], wave: [70, -320] }[arm];
  const farHand = arm === 'show' ? [104, -196] : arm === 'hold' ? [80, -176] : arm === 'up' ? [18, -318] : [-30, -120];
  tube(c, [[-10, -168], [(farHand[0] - 10) / 2, (farHand[1] - 168) / 2 - 10], farHand], 17, FUR_D);
  ell(c, farHand[0], farHand[1], 15, 15, FUR_D, 7);
  // ---- body + belly
  c.beginPath(); c.ellipse(0, -122, 58, 76, 0, 0, TAU); fs(c, FUR);
  c.beginPath(); c.ellipse(-20, -118, 26, 58, 0, 0, TAU); c.fillStyle = FUR_D; c.globalAlpha = .45; c.fill(); c.globalAlpha = 1;
  c.beginPath(); c.ellipse(20, -112, 32, 52, 0, 0, TAU); fs(c, CREAM, 5);
  const nearArm = () => {
    if (o.item) { c.save(); c.translate(handPos[0], handPos[1]); c.scale(dir, 1); c.scale(1 / s, 1 / s); c.scale(Math.sqrt(sq), 1 / sq); o.item(c); c.restore(); }
    tube(c, [[20, -170], [(handPos[0] + 20) / 2 + (arm === 'up' ? 22 : 0), (handPos[1] - 170) / 2 + 12], handPos], 17, FUR);
    ell(c, handPos[0], handPos[1], 16, 16, FUR, 7);
  };
  if (arm === 'up' || arm === 'wave') nearArm();
  // ---- ears (behind head)
  for (const [bx, lean] of [[-18, -.25], [30, .15]]) {
    c.save(); c.translate(bx, -270); c.rotate(lean);
    c.beginPath(); c.moveTo(-24, 10); c.quadraticCurveTo(-14, -52, 4, -74); c.quadraticCurveTo(18, -40, 24, 8); c.closePath(); fs(c, FUR);
    c.beginPath(); c.moveTo(-10, 0); c.quadraticCurveTo(-4, -36, 4, -50); c.quadraticCurveTo(12, -26, 12, 2); c.closePath(); c.fillStyle = PINK; c.fill();
    c.beginPath(); c.moveTo(4, -72); c.lineTo(-6, -92); c.moveTo(4, -72); c.lineTo(12, -94); c.strokeStyle = INK; c.lineWidth = 6; c.stroke();
    c.restore();
  }
  // ---- head
  c.beginPath(); c.arc(18, -222, 64, 0, TAU); fs(c, FUR);
  c.beginPath(); c.arc(-2, -212, 44, Math.PI * .55, Math.PI * 1.35); c.lineWidth = 16; c.strokeStyle = FUR_D; c.globalAlpha = .5; c.stroke(); c.globalAlpha = 1;
  c.beginPath(); c.ellipse(56, -196, 40, 30, 0, 0, TAU); fs(c, CREAM, 6);
  // eyes: two tall conjoined ovals
  const wide = o.wide || 0, lk = o.look || [0, 0];
  const erx = 19 * (1 + wide * .45), ery = 28 * (1 + wide * .5);
  for (const [ex, isR] of [[30, 0], [66, 1]]) {
    const ey = -250 - wide * 10;
    c.beginPath(); c.ellipse(ex, ey, erx, ery, 0, 0, TAU); fs(c, '#ffffff', 6);
    const bl = isR && o.wink != null ? Math.max(o.blink || 0, o.wink) : (o.blink || 0);
    const pr = 8 * (1 - wide * .45);
    c.beginPath(); c.ellipse(ex + 4 + lk[0] * 8, ey + 4 + lk[1] * 10, pr, pr * 1.35, 0, 0, TAU); c.fillStyle = INK; c.fill();
    c.beginPath(); c.arc(ex + 1 + lk[0] * 8, ey - 2 + lk[1] * 10, pr * .35, 0, TAU); c.fillStyle = '#fff'; c.fill();
    if (bl > 0) {
      c.save(); c.beginPath(); c.ellipse(ex, ey, erx + 1, ery + 1, 0, 0, TAU); c.clip();
      c.fillStyle = FUR; c.fillRect(ex - 30, ey - ery - 2, 60, (ery * 2 + 4) * bl); c.restore();
      c.beginPath(); c.ellipse(ex, ey, erx, ery, 0, 0, TAU); fs(c, null, 6);
      if (bl > .9) { c.beginPath(); c.moveTo(ex - erx, ey + 4); c.quadraticCurveTo(ex, ey + 18, ex + erx, ey + 4); fs(c, null, 6); }
    }
  }
  // nose, mouth, teeth
  ell(c, 92, -210, 12, 9, NOSE, 4);
  const mouth = o.mouth || 'grin';
  if (mouth === 'o' || mouth === 'yell') {
    const big = mouth === 'yell' ? 1.6 : 1;
    c.beginPath(); c.ellipse(70, -180, 13 * big, 15 * big, 0, 0, TAU); fs(c, '#5a0f2a', 5);
    c.fillStyle = '#fff'; c.fillRect(64, -180 - 15 * big, 12, 9);
  } else if (mouth === 'gulp') {
    c.beginPath(); c.moveTo(48, -184); for (let i = 1; i <= 6; i++) c.lineTo(48 + i * 7, -184 + (i % 2 ? -5 : 5)); fs(c, null, 5);
    c.fillStyle = '#fff'; c.beginPath(); c.rect(72, -182, 16, 16); fs(c, '#fff', 4);
  } else {
    c.beginPath(); c.moveTo(40, -190); c.quadraticCurveTo(66, -168, 94, -192); fs(c, null, 6);
    c.beginPath(); c.rect(68, -187, 18, 22); fs(c, '#fff', 4);
    c.beginPath(); c.moveTo(77, -187); c.lineTo(77, -166); fs(c, null, 3);
  }
  // ---- held item + near arm (item drawn at the near hand, un-mirrored)
  if (arm !== 'up' && arm !== 'wave') nearArm();
  c.restore();
}

/* ================================================================ CACTUS
 * "Thorns": grumpy saguaro in a terracotta pot, heavy unibrow, a pink flower that pops on the take.
 * Local units: pot bottom on (0,0), pot top at -150, body ≈ 300 tall above that.
 * o: {x,y,s,sq,lean,open(0..1),anger,take,jaw,grin,spines,arms:'rest'|'up'|'fist',armPh,red,look:[x,y],flower} */
const CAC = '#43c254', CAC_D = '#2a9446', CAC_L = '#8fe777', POT = '#ea7a3e', POT_D = '#b9522b', RIM = '#f6a261';
const SPINES = (() => { const r = rng(77), a = []; for (let i = 0; i < 26; i++) a.push([r() * 2 - 1, .06 + r() * .86, r()]); return a; })();
function drawCactus(c, o) {
  const s = o.s || 1, sq = o.sq || 1, take = o.take || 0, jaw = o.jaw || 0, grin = o.grin || 0, anger = o.anger || 0;
  c.save(); c.translate(o.x, o.y); c.rotate(o.lean || 0); c.scale(s / Math.sqrt(sq), s * sq);
  const bw = 74 * (1 + take * .08), bh = 300 * (1 + jaw * .12), top = -150 - bh;
  const spl = 12 + (o.spines || 0) * 34, red = o.red || 0;
  // anger rises like a thermometer: solid red fills the body from the pot up (no muddy color mixing)
  const REDB = '#ff4a3d', REDD = '#c9262e', lvl = -150 - bh * 1.1 * red;
  const armCol = A => (red > 0 && lvl < A[0][1] - 20) ? REDB : CAC;
  // ---- arms (behind body)
  const ap = o.armPh || 0, arms = o.arms || 'rest';
  const armL = arms === 'up' ? [[-50, -290], [-150, -330 + Math.sin(ap) * 20], [-160, -470 + Math.cos(ap) * 20]]
             : arms === 'fist' ? [[-50, -270], [-140, -260], [-150, -350 + Math.sin(ap) * 16]]
             : [[-50, -280], [-128, -284], [-130, -370]];
  const armR = arms === 'up' ? [[50, -250], [150, -300 + Math.cos(ap) * 20], [150, -450 + Math.sin(ap) * 20]]
             : arms === 'fist' ? [[50, -236], [134, -232], [140, -318 + Math.cos(ap) * 16]]
             : [[50, -232], [122, -236], [124, -316]];
  for (const A of [armL, armR]) {
    const ac = armCol(A);
    tube(c, A, 56, ac);
    c.save(); c.globalAlpha = .55; c.lineCap = 'round'; c.strokeStyle = ac === CAC ? CAC_D : REDD; c.lineWidth = 5;
    c.beginPath(); c.moveTo(A[0][0], A[0][1]); c.quadraticCurveTo(A[1][0], A[1][1], A[2][0], A[2][1]); c.stroke(); c.restore();
    // spines on the arm tip
    const [ex, ey] = A[2];
    c.strokeStyle = INK; c.lineWidth = 3.5; c.beginPath();
    for (const a of [-2.2, -1.57, -.9]) { const len = spl * .8; c.moveTo(ex + Math.cos(a) * 30, ey + Math.sin(a) * 30); c.lineTo(ex + Math.cos(a) * (30 + len), ey + Math.sin(a) * (30 + len)); }
    c.stroke();
    if (arms === 'fist') ell(c, ex, ey - 6, 34, 30, ac);
  }
  // ---- body
  const body = () => { c.beginPath(); c.moveTo(-bw, -140); c.lineTo(-bw, top + bw); c.arc(0, top + bw, bw, Math.PI, 0); c.lineTo(bw, -140); c.closePath(); };
  body(); fs(c, CAC);
  c.save(); body(); c.clip();
  c.fillStyle = CAC_D; c.globalAlpha = .55; c.fillRect(-bw, top, bw * .45, bh + 20);
  c.globalAlpha = .6; c.fillStyle = CAC_L; c.beginPath(); c.ellipse(bw * .42, top + bw + 40, 14, 70, 0, 0, TAU); c.fill();
  c.globalAlpha = 1; c.strokeStyle = CAC_D; c.lineWidth = 5;
  const ribs = () => { for (const rx of [-.45, 0, .45]) { c.beginPath(); c.moveTo(rx * bw, -140); c.quadraticCurveTo(rx * bw * 1.12, top + bh * .4, rx * bw * .75, top + 18); c.stroke(); } };
  ribs();
  if (red > 0) { c.beginPath(); c.rect(-bw - 5, lvl, bw * 2 + 10, -130 - lvl); c.clip();
    c.fillStyle = REDB; c.fillRect(-bw - 5, lvl, bw * 2 + 10, -130 - lvl);
    c.fillStyle = REDD; c.globalAlpha = .55; c.fillRect(-bw, top, bw * .45, bh + 20); c.globalAlpha = 1;
    c.strokeStyle = REDD; ribs(); c.fillStyle = '#ffb09a'; c.fillRect(-bw - 5, lvl, bw * 2 + 10, 7); }
  c.restore();
  body(); fs(c, null);
  // spines around the silhouette (they shoot out on the take)
  c.strokeStyle = INK; c.lineWidth = 3.5; c.lineCap = 'round'; c.beginPath();
  for (const [sx, sy, k] of SPINES) {
    const side = sx < 0 ? -1 : 1, y = -150 - bh * sy;
    if (Math.abs(sx) > .35) { c.moveTo(side * bw, y); c.lineTo(side * (bw + spl * (.7 + k * .6)), y - spl * .35); }
    else if (take < .01) { const x = sx * bw * 1.5; c.moveTo(x - 5, y + 6); c.lineTo(x, y); c.lineTo(x + 6, y + 6); }
  }
  const ta = [-2.5, -2.0, -1.57, -1.1, -.6];
  for (const a of ta) { c.moveTo(Math.cos(a) * bw, top + bw + Math.sin(a) * bw); c.lineTo(Math.cos(a) * (bw + spl), top + bw + Math.sin(a) * (bw + spl)); }
  c.stroke();
  // flower on the head (springs up on the take)
  const fl = o.flower || 0;
  if (fl > 0 || true) {
    const fy = top + 6 - fl * 40;
    if (fl > 0) { c.beginPath(); c.moveTo(0, top + 4); c.lineTo(0, fy); fs(c, null, 6); c.beginPath(); c.moveTo(0, top + 4); c.lineTo(0, fy); c.strokeStyle = CAC; c.lineWidth = 2; c.stroke(); }
    const pr = 13 + fl * 6;
    for (let i = 0; i < 5; i++) { const a = i / 5 * TAU - Math.PI / 2 + fl * 1.2; ell(c, Math.cos(a) * pr, fy + Math.sin(a) * pr, pr * .8, pr * .55, '#ff5fa8', 5, a); }
    ell(c, 0, fy, pr * .55, pr * .55, '#ffd23f', 5);
  }
  // ---- face
  const fy = top + bw + 70 - take * 30;
  const open = o.open == null ? 1 : o.open, lk = o.look || [0, 0];
  const erx = 23 * (1 + take * 1.25), ery = 25 * (1 + take * 1.7);
  for (const side of [-1, 1]) {
    const ex = side * (27 + take * 26), ey = fy - take * 26;
    if (open < .05) { c.beginPath(); c.moveTo(ex - 18, ey + 2); c.quadraticCurveTo(ex, ey + 12, ex + 18, ey + 2); fs(c, null, 6); continue; }
    c.beginPath(); c.ellipse(ex, ey, erx, ery, 0, 0, TAU); fs(c, '#fff', 6);
    const pr = 8 * (1 - take * .5);
    c.beginPath(); c.arc(ex + lk[0] * 9, ey + 6 + lk[1] * 8, pr, 0, TAU); c.fillStyle = INK; c.fill();
    // heavy lid: flat line = grumpy
    const lid = (1 - open) * .9 + anger * .25 * (1 - take);
    if (lid > 0) {
      c.save(); c.beginPath(); c.ellipse(ex, ey, erx + 1, ery + 1, 0, 0, TAU); c.clip();
      c.fillStyle = (red > 0 && lvl < ey - ery) ? REDD : CAC_D; c.fillRect(ex - 40, ey - ery - 2, 80, (ery * 2 + 4) * lid); c.restore();
      c.beginPath(); c.moveTo(ex - erx + 2, ey - ery + (ery * 2) * lid); c.lineTo(ex + erx - 2, ey - ery + (ery * 2) * lid); fs(c, null, 6);
      c.beginPath(); c.ellipse(ex, ey, erx, ery, 0, 0, TAU); fs(c, null, 6);
    }
  }
  // unibrow: thick, angled down to the middle when angry, flies up on the take
  const by = Math.max(top + 30, fy - 36 - take * 70), dip = anger * 22 - take * 26 - grin * 10;
  c.beginPath(); c.moveTo(-62 - take * 20, by - 6); c.quadraticCurveTo(0, by + dip + 8, 62 + take * 20, by - 6);
  c.lineTo(62 + take * 20, by - 20); c.quadraticCurveTo(0, by + dip - 10, -62 - take * 20, by - 20); c.closePath(); fs(c, '#27123a', 4);
  // mouth: frown / jaw-drop / grin
  const my = fy + 52;
  if (jaw > .02) {
    const mh = 30 + jaw * 250, mw = 38 + jaw * 20;
    c.beginPath(); c.moveTo(-mw, my); c.quadraticCurveTo(0, my - 14, mw, my); c.lineTo(mw * .9, my + mh); c.quadraticCurveTo(0, my + mh + 30, -mw * .9, my + mh); c.closePath(); fs(c, '#5a0f2a', 6);
    c.save(); c.clip(); c.fillStyle = '#fff'; c.fillRect(-mw, my - 14, mw * 2, 22);
    c.fillStyle = '#ff5f7e'; c.beginPath(); c.ellipse(0, my + mh + 6, mw * .75, 34, 0, 0, TAU); c.fill(); c.restore();
    c.beginPath(); c.moveTo(-mw, my); c.quadraticCurveTo(0, my - 14, mw, my); c.lineTo(mw * .9, my + mh); c.quadraticCurveTo(0, my + mh + 30, -mw * .9, my + mh); c.closePath(); fs(c, null, 6);
  } else if (grin > .02) {
    const gw = 30 + grin * 30, gh = 8 + grin * 38;
    c.beginPath(); c.moveTo(-gw, my - 6); c.quadraticCurveTo(0, my + gh * 1.6, gw, my - 6); c.quadraticCurveTo(0, my + 4, -gw, my - 6); c.closePath(); fs(c, '#5a0f2a', 6);
    c.save(); c.clip(); c.fillStyle = '#fff'; c.fillRect(-gw, my - 10, gw * 2, 16 + grin * 4); c.restore();
    c.beginPath(); c.moveTo(-gw, my - 6); c.quadraticCurveTo(0, my + gh * 1.6, gw, my - 6); c.quadraticCurveTo(0, my + 4, -gw, my - 6); c.closePath(); fs(c, null, 6);
  } else {
    const k = o.sleep ? 0 : 1;
    c.beginPath(); c.moveTo(-26, my + 8 * k); c.quadraticCurveTo(0, my - 10 * k + (1 - k) * 8, 26, my + 8 * k); fs(c, null, 7);
  }
  // ---- pot (in front of the body's base)
  c.beginPath(); c.moveTo(-112, -140); c.lineTo(-86, 0); c.lineTo(86, 0); c.lineTo(112, -140); c.closePath(); fs(c, POT);
  c.save(); c.clip(); c.fillStyle = POT_D; c.globalAlpha = .5; c.fillRect(-120, -140, 70, 150); c.globalAlpha = 1; c.restore();
  c.beginPath(); c.moveTo(-112, -140); c.lineTo(-86, 0); c.lineTo(86, 0); c.lineTo(112, -140); c.closePath(); fs(c, null);
  c.beginPath(); c.roundRect(-130, -172, 260, 44, 10); fs(c, RIM);
  c.beginPath(); c.moveTo(-100, -150); c.lineTo(80, -150); c.strokeStyle = '#fff'; c.globalAlpha = .45; c.lineWidth = 6; c.stroke(); c.globalAlpha = 1;
  c.restore();
}

/* ================================================================ ALARM CLOCK
 * twin-bell, red, face reads 7:00.  ring 0..1 = shake + hammer + vibration arcs. */
function drawClock(c, x, y, s, ring, t, rot = 0, snooze = 0) {
  c.save(); c.translate(x, y);
  const jit = ring * Math.sin(t * TAU * 22) * .11, hop = ring * Math.abs(Math.sin(t * TAU * 11)) * 10;
  c.rotate(rot + jit); c.translate(0, -hop); c.scale(s, s);
  // legs
  tube(c, [[-34, -30], [-50, 0]], 12, '#8a2a3a', 6); tube(c, [[34, -30], [50, 0]], 12, '#8a2a3a', 6);
  // bells + handle + hammer
  for (const side of [-1, 1]) { c.save(); c.translate(side * 44, -118); c.rotate(side * .55);
    c.beginPath(); c.arc(0, 0, 32, Math.PI, 0); c.lineTo(34, 6); c.lineTo(-34, 6); c.closePath(); fs(c, '#ffd23f', 7);
    c.beginPath(); c.arc(-10, -10, 8, 0, TAU); c.fillStyle = '#fff6b0'; c.fill(); c.restore(); }
  c.beginPath(); c.moveTo(0, -126); c.lineTo(0, -160 + snooze * 12); fs(c, null, 7);
  c.beginPath(); c.roundRect(-16, -170 + snooze * 12, 32, 16, 6); fs(c, '#ff3b4f', 6); // snooze button
  const hm = ring * Math.sin(t * TAU * 22) * 22;
  tube(c, [[0, -104], [hm, -142]], 7, '#555', 5); ell(c, hm, -144, 10, 10, '#777', 5);
  // body + face
  ell(c, 0, -70, 64, 64, '#ff3b4f');
  c.beginPath(); c.arc(-18, -88, 36, Math.PI * 1.05, Math.PI * 1.55); c.strokeStyle = '#ff9aa6'; c.lineWidth = 9; c.lineCap = 'round'; c.stroke();
  ell(c, 0, -70, 47, 47, '#fffaf0', 6);
  c.strokeStyle = INK; c.lineWidth = 4;
  for (let i = 0; i < 12; i++) { const a = i / 12 * TAU; const r0 = i % 3 ? 38 : 34; c.beginPath(); c.moveTo(Math.cos(a) * r0, -70 + Math.sin(a) * r0); c.lineTo(Math.cos(a) * 42, -70 + Math.sin(a) * 42); c.stroke(); }
  tube(c, [[0, -70], [0, -104]], 4, INK, 0); tube(c, [[0, -70], [-12, -48]], 7, INK, 0);
  ell(c, 0, -70, 5, 5, INK, 0);
  c.restore();
  // vibration arcs
  if (ring > .05) {
    c.save(); c.translate(x, y - hop); c.strokeStyle = INK; c.lineCap = 'round'; c.lineWidth = 6 * s;
    for (const side of [-1, 1]) for (let k = 0; k < 3; k++) {
      const r = (95 + k * 26 + ((t * 9) % 1) * 12) * s; c.globalAlpha = ring * (1 - k * .25);
      c.beginPath(); c.arc(0, -120 * s, r, side > 0 ? -.55 : Math.PI - .35, side > 0 ? .35 : Math.PI + .55); c.stroke(); }
    c.restore();
  }
}

/* ================================================================ CALENDAR PAGE (the punchline) */
function drawCalendar(c, s = 1) {
  c.save(); c.scale(s, s);
  c.beginPath(); c.roundRect(-190, -150, 380, 250, 14); fs(c, '#fffdf3');
  c.save(); c.beginPath(); c.roundRect(-190, -150, 380, 250, 14); c.clip(); c.fillStyle = '#ff3b4f'; c.fillRect(-200, -160, 400, 76); c.restore();
  c.beginPath(); c.roundRect(-190, -150, 380, 250, 14); fs(c, null);
  c.beginPath(); c.moveTo(-190, -84); c.lineTo(190, -84); fs(c, null, 6);
  for (const rx of [-110, 110]) { ell(c, rx, -150, 12, 12, '#cfd3dc', 6); }
  c.fillStyle = '#fff'; c.font = `800 34px ${ROUND}`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('TODAY IS', 0, -116);
  c.font = `52px ${DISPLAY}`; c.lineWidth = 10; c.strokeStyle = INK; c.lineJoin = 'round';
  c.strokeText('SATURDAY', 0, 8); c.fillStyle = '#2f7cff'; c.fillText('SATURDAY', 0, 8);
  c.font = `800 22px ${ROUND}`; c.fillStyle = INK; c.fillText('no alarms · just cartoons', 0, 66);
  c.restore();
}

/* ================================================================ SFX lettering with a jagged burst */
function burst(c, x, y, r0, r1, n, fill, rot = 0, seed = 1) {
  const r = rng(seed); c.beginPath();
  for (let i = 0; i < n * 2; i++) { const a = rot + i / (n * 2) * TAU, rr = i % 2 ? r0 * (.85 + r() * .2) : r1 * (.85 + r() * .3);
    const px = x + Math.cos(a) * rr, py = y + Math.sin(a) * rr * .72; i ? c.lineTo(px, py) : c.moveTo(px, py); }
  c.closePath(); fs(c, fill, 8);
}
function sfx(c, text, x, y, size, pop, rot, fill, bfill, seed = 3) {
  if (pop <= 0) return;
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(pop, pop);
  c.font = `${size}px ${DISPLAY}`; c.textAlign = 'center'; c.textBaseline = 'middle';
  const w = c.measureText(text).width;
  if (bfill) burst(c, 0, 0, w * .5 + size * .12, w * .5 + size * .5, 12, bfill, 0, seed);
  c.lineJoin = 'round';
  for (let k = 7; k >= 1; k--) { c.fillStyle = INK; c.fillText(text, k * 1.6, k * 1.6); }
  c.lineWidth = size * .16; c.strokeStyle = INK; c.strokeText(text, 0, 0);
  c.fillStyle = fill; c.fillText(text, 0, 0);
  c.restore();
}
