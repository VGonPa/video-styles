// scene.js · layout, the four pages, the page turn, quill choreography, camera, events
const cv = document.getElementById('c'), X = cv.getContext('2d');
const BODY = `600 41px ${FB}`, LH = 55;
const TIT = `700 62px ${FT}`, HEAD = `800 46px ${FB}`, FINAL = `700 44px ${FB}`;
const mctx = mk(4, 4).getContext('2d');
const wid = (s, f) => { mctx.font = f; return mctx.measureText(s).width; };

// ── text flow: words → justified lines over column slots ──
// markup: ^word = red, ~word = blue, ¶ = pilcrow (alternating blue/red)
function flow(text, slots, font) {
  const paras = text.split('|').map(p => p.trim().split(/\s+/));
  const sp = wid(' ', font), lines = []; let si = 0, pil = 0;
  for (let pi = 0; pi < paras.length; pi++) {
    const words = paras[pi].map(w => {
      let c = COL.ink, s = w;
      if (w === '¶') c = (pil++ % 2) ? COL.red : COL.blue; else if (w[0] === '^') { c = COL.red; s = w.slice(1); } else if (w[0] === '~') { c = COL.blue; s = w.slice(1); }
      return { s, c, w: wid(s, font) };
    });
    let i = 0;
    while (i < words.length) {
      if (si >= slots.length) { console.error('text overflow:', words.slice(i).map(w => w.s).join(' ')); return lines; }
      const sl = slots[si++]; let j = i, used = 0;
      while (j < words.length && used + (j > i ? sp : 0) + words[j].w <= sl.w) { used += (j > i ? sp : 0) + words[j].w; j++; }
      if (j === i) j = i + 1;
      const last = j >= words.length, row = words.slice(i, j), nat = row.reduce((a, w) => a + w.w, 0);
      let gap = (!last && row.length > 1) ? (sl.w - nat) / (row.length - 1) : sp; if (gap > sp * 2.6) gap = sp * 1.3;
      let x = 0; const ws = row.map(w => { const o = { ...w, x }; x += w.w + gap; return o; });
      const rag = gap < (sl.w - nat) / Math.max(1, row.length - 1) - 0.5; lines.push({ x: sl.x, y: sl.y, w: (last || rag) ? x - gap : sl.w, full: sl.w, words: ws, font, last });
      i = j;
    }
  }
  return lines;
}
const slotsCol = (x, w, y0, n, ind = 0, dx = 0) => Array.from({ length: n }, (_, i) => ({ x: x + (i < ind ? dx : 0), y: y0 + i * LH, w: w - (i < ind ? dx : 0) }));
const centred = (s, font, cx, y, c = COL.red) => { const w = wid(s, font); return { x: cx - w / 2, y, w, full: w, words: [{ s, c, x: 0, w }], font, last: true }; };

// ── page content ──
const PAGES = {};
function layout() {
  // A · verso: title, gilded T, two columns
  const A = PAGES.A = { side: 'L' };
  A.title = [centred('A Most Excellent', TIT, 475, 180), centred('Recipe for Bread', TIT, 475, 250)];
  A.ini = { x: 64, y: 292, s: 172 };
  A.lines = flow('ake of the finest flour three good measures, a pinch of salt, and water as warm as a summer brook. Stir in the ^barm, which is yeast, and mix it well together. | ¶ ^Knead it with vigour the length of a long ballad, then let it rest under linen beside the hearth until it be risen twice over.',
    [...slotsCol(150, 305, 330, 9, 3, 104), ...slotsCol(495, 305, 330, 9)], BODY);
  A.vines = [new Vine([[74, 466], [90, 560], [98, 660], [88, 760], [96, 850], [128, 912], [260, 918], [420, 910], [580, 918], [720, 910], [812, 914]], 11, { every: 56 }),
    new Vine([[70, 292], [82, 220], [96, 150], [130, 104], [200, 84], [236, 80]], 12, { every: 46, leaf: 18 })];
  // B · recto: miniature, caption, bas-de-page joust
  const B = PAGES.B = { side: 'R' };
  B.cap = [(() => { const l = centred('Of the Oven, and of its Fire', HEAD, 430, 662); l.words.unshift({ s: '¶', c: COL.blue, x: -34, w: 26 }); return l; })()];
  B.vine = new Vine([[808, 100], [796, 220], [806, 360], [794, 500], [806, 640], [796, 780], [806, 900]], 13, { every: 56 });
  // C · verso (back of the leaf): rubric, pen-flourished W
  const C = PAGES.C = { side: 'L' };
  C.head = [centred('Of the Shaping', HEAD, 475, 180)];
  C.lines = flow('hen it be risen, punch it down as one who hath been sorely wronged, then shape it into round loaves and score each with a sharp knife. | ¶ Let them rise once more beneath the linen, for bread, like a scholar, is much improved by a second rest. | ¶ ^Meanwhile heat the oven until a sprinkle of flour upon its floor doth brown in the time it takes to say so.',
    [...slotsCol(150, 305, 280, 11, 3, 138), ...slotsCol(495, 305, 280, 11)], BODY);
  C.vine = new Vine([[96, 420], [88, 560], [98, 700], [90, 840], [140, 915], [320, 912], [470, 918]], 17, { every: 60, leaf: 20, bezant: 0.5 });
  // D · recto: rubric, gilded S, columns, the warning, the theft
  const D = PAGES.D = { side: 'R' };
  D.head = [centred('Of the Baking', HEAD, 415, 180)];
  D.ini = { x: 88, y: 236, s: 138 };
  D.lines = flow('et the loaves upon the hot stone and bake them until the crust be golden and doth sing when tapped beneath. | ¶ Let them cool, if thou canst bear to wait.',
    [...slotsCol(90, 305, 270, 6, 3, 146), ...slotsCol(435, 305, 270, 6)], BODY);
  D.final = [centred('Item: guard thy loaf from rabbits.', FINAL, 415, 612)];
  D.vine = new Vine([[808, 100], [798, 240], [806, 380], [794, 520], [806, 660], [798, 800], [806, 905]], 19, { every: 60 });
}

// ── writing schedule: each line gets a time slot, sized by its width ──
const WR = [];   // { page, line, t0, t1 }
function schedule(page, lines, ta, tb, gap = 0.035) {
  const W = lines.reduce((a, l) => a + l.w, 0), v = W / (tb - ta - gap * (lines.length - 1));
  let t = ta; for (const l of lines) { const d = l.w / v; WR.push({ page, line: l, t0: t, t1: t + d }); l.t0 = t; l.t1 = t + d; t += d + gap; }
}
const TL = {
  fadeIn: [0, 0.7], title: [0.55, 1.45], body: [1.5, 4.1],
  iniInk: [1.25, 1.6], iniGild: [1.45, 2.05], iniShine: [2.05, 2.6], vineA: [1.7, 3.2],
  mini: { ink: [2.3, 3.0], gild: [2.8, 3.3], col: [3.0, 3.9], shine0: 3.9 }, vineB: [2.5, 3.7],
  cap: [4.28, 4.68], droll: [3.5, 4.1],
  march: [4.45, 5.15], raise: [4.95, 5.2], blow: [5.2, 5.75], retreat: [5.32, 5.62],
  lift: [5.8, 6.08], turn: [6.08, 6.95], settle: [6.95, 7.25],
  dHead: [7.15, 7.42], dBody: [7.48, 8.42], dIni: [7.4, 7.9], dShine: [7.95, 8.45], dFinal: [8.5, 9.05],
  hopIn: [7.95, 8.42], grab: 8.45, hopOut: [8.5, 9.35], snailD: [8.1, 9.8],
  fadeOut: [9.35, 10.0],
};
function buildSchedule() {
  schedule('A', PAGES.A.title, ...TL.title, 0.07);
  schedule('A', PAGES.A.lines, ...TL.body);
  schedule('B', PAGES.B.cap, ...TL.cap);
  schedule('D', PAGES.D.head, ...TL.dHead);
  schedule('D', PAGES.D.lines, ...TL.dBody);
  schedule('D', PAGES.D.final, ...TL.dFinal);
}

// draw a (partly) written line; p = reveal 0..1
function drawLine(g, l, p) {
  if (p <= 0) return;
  g.save(); if (p < 1) { g.beginPath(); g.rect(l.x - 40, l.y - 80, 40 + l.w * p, 120); g.clip(); }
  g.font = l.font; g.textBaseline = 'alphabetic';
  for (const w of l.words) { g.fillStyle = w.c; g.fillText(w.s, l.x + w.x, l.y); }
  g.restore();
  // wet ink glint just behind the pen
  if (p < 1) { g.save(); g.fillStyle = 'rgba(40,20,10,0.25)'; g.beginPath(); g.arc(l.x + l.w * p, l.y + 2, 2.4, 0, TAU); g.fill(); g.restore(); }
  if (p >= 1 && l.last && l.full - l.w > 30 && l.font === BODY) lineFiller(g, l.x + l.w + 10, l.x + l.full, l.y);
}
const linesP = (lines, t) => { for (const l of lines) drawLine(PG, l, seg(t, l.t0, l.t1)); };
function ruling(g, x0, x1, y0, n, cols) {
  g.strokeStyle = 'rgba(150,110,80,0.16)'; g.lineWidth = 1;
  for (const [a, b] of cols) { g.beginPath(); g.moveTo(a, y0 - 60); g.lineTo(a, y0 + n * LH); g.moveTo(b, y0 - 60); g.lineTo(b, y0 + n * LH); g.stroke(); }
  for (let i = 0; i < n; i++) { g.beginPath(); g.moveTo(x0 - 10, y0 + i * LH + 1); g.lineTo(x1 + 10, y0 + i * LH + 1); g.stroke(); }
}

// panel initial: gold frame, blue field with white filigree, burnished gold letter
function panelInitial(g, ch, P, t, ink, gild, shine, seed, fsize) {
  const ui = seg(t, ...ink), ug = seg(t, ...gild), sh = seg(t, ...shine), { x, y, s } = P;
  if (ui <= 0) return;
  const fr = Math.round(s * 0.07);
  if (ug > 0) {
    g.save(); g.globalAlpha = clamp(ug * 3);
    g.fillStyle = COL.blue; g.fillRect(x + fr, y + fr, s - 2 * fr, s - 2 * fr);
    g.fillStyle = COL.rose; g.fillRect(x + fr, y + fr, s - 2 * fr, (s - 2 * fr) * 0.5); g.globalAlpha = 1;
    // rose top half / blue bottom, split on a gentle curve like a quartered field
    g.save(); g.beginPath(); g.rect(x + fr, y + fr, s - 2 * fr, s - 2 * fr); g.clip();
    g.fillStyle = COL.blue; g.beginPath(); g.moveTo(x, y + s * 0.5); g.quadraticCurveTo(x + s * 0.5, y + s * 0.38, x + s, y + s * 0.5); g.lineTo(x + s, y + s); g.lineTo(x, y + s); g.closePath(); g.fill();
    g.restore();
    g.globalAlpha = clamp(ug * 2 - 0.5); filigree(g, x + fr, y + fr, s - 2 * fr, s - 2 * fr, seed); g.restore();
    const frame = gg => { gg.beginPath(); gg.rect(x, y, s, s); gg.rect(x + fr, y + fr, s - 2 * fr, s - 2 * fr); };
    g.save(); g.beginPath(); frame(g); g.clip('evenodd'); gold(g, gg => { gg.beginPath(); gg.rect(x, y, s, s); }, [x, y, s, s], ug, sh > 0 && sh < 1 ? sh : -1, seed); g.restore();
  }
  // letter: ink outline first, then gilded
  const font = `700 ${fsize}px ${FT}`; g.save(); g.font = font; const m = g.measureText(ch); g.restore();
  const lx = x + (s - m.width) / 2, ly = y + s * 0.5 + (m.actualBoundingBoxAscent - m.actualBoundingBoxDescent) / 2;
  if (ug < 1) { g.save(); g.font = font; g.lineWidth = 2; g.strokeStyle = `rgba(42,27,18,${ui})`; g.setLineDash([900 * ui, 900]); g.strokeText(ch, lx, ly); g.restore(); }
  goldGlyph(g, ch, font, lx, ly, clamp((ug - 0.15) / 0.85), sh > 0 && sh < 1 ? lerp(-0.2, 1.1, sh) : -1, seed + 3);
  g.strokeStyle = `rgba(42,27,18,${ui})`; g.lineWidth = 1.6; g.strokeRect(x, y, s, s); if (ug > 0) g.strokeRect(x + fr, y + fr, s - 2 * fr, s - 2 * fr);
}
// a vertical border bar (blue & rose segments, white hairlines), grows with u
function borderBar(g, x, y0, y1, u, horiz) {
  if (u <= 0) return; const L = (y1 - y0) * u;
  g.save(); if (horiz) { g.translate(y0, x); g.rotate(-Math.PI / 2); g.translate(-y0, -x); g.scale(1, 1); }
  for (let y = y0, k = 0; y < y0 + L; y += 46, k++) { g.fillStyle = k % 2 ? COL.rose : COL.blue; g.fillRect(x, y, 10, Math.min(46, y0 + L - y)); }
  g.strokeStyle = 'rgba(255,250,238,0.85)'; g.lineWidth = 1; g.beginPath(); g.moveTo(x + 5, y0); g.lineTo(x + 5, y0 + L); g.stroke();
  g.strokeStyle = COL.ink; g.lineWidth = 1.2; g.strokeRect(x, y0, 10, L);
  g.restore();
}

// ── page renderers (page coords) ──
let PG; const PC = {}, VEL = {}, TOOTH = {};
function beginPage(k) { const c = PC[k] || (PC[k] = mk(PW, PH)); PG = c.getContext('2d'); PG.globalCompositeOperation = 'source-over'; PG.drawImage(VEL[k], 0, 0); return c; }
function endPage(k) { PG.globalCompositeOperation = 'multiply'; PG.drawImage(TOOTH[k], 0, 0); PG.globalCompositeOperation = 'source-over'; return PC[k]; }
function pageA(t) {
  const A = PAGES.A; beginPage('A'); const g = PG;
  ruling(g, 150, 800, 330, 9, [[150, 455], [495, 800]]);
  const vu = seg(t, ...TL.vineA), sh = seg(t, 2.6, 3.4), sh2 = seg(t, 3.2, 4.0);
  borderBar(g, 118, 466, 886, eInOut(seg(t, 1.65, 2.5)));
  if (seg(t, 2.3, 3.0) > 0) { g.save(); g.fillStyle = COL.blue; g.fillRect(120, 886, 690 * eInOut(seg(t, 2.3, 3.0)), 10); g.fillStyle = COL.rose; for (let x = 166; x < 120 + 690 * eInOut(seg(t, 2.3, 3.0)) - 10; x += 92) g.fillRect(x, 886, 46, 10); g.strokeStyle = COL.ink; g.lineWidth = 1.2; g.strokeRect(120, 886, 690 * eInOut(seg(t, 2.3, 3.0)), 10); g.restore(); }
  for (const v of A.vines) v.draw(g, eOut(vu), sh > 0 && sh < 1 ? sh : (sh2 > 0 && sh2 < 1 ? sh2 : -1));
  linesP(A.title, t); linesP(A.lines, t);
  panelInitial(g, 'T', A.ini, t, TL.iniInk, TL.iniGild, TL.iniShine, 41, 158);
  // a second, gentler glint on the initial as the page settles
  const g2 = seg(t, 4.4, 4.95); if (g2 > 0 && g2 < 1) panelInitial(g, 'T', A.ini, t, TL.iniInk, TL.iniGild, [4.4, 4.95], 41, 158);
  return endPage('A');
}
function drollB(t) {   // snail knight vs trumpeting rabbit, bottom of page B
  const g = PG, reveal = seg(t, ...TL.droll);
  if (reveal <= 0) return;
  g.save(); if (reveal < 1) { g.beginPath(); g.rect(80, 700, 680 * eInOut(reveal), 240); g.clip(); }
  groundLine(g, 96, 740, 905, 5);
  const mu = eInOut(seg(t, ...TL.march)), ret = seg(t, ...TL.retreat), sx = lerp(190, 318, mu) - ret * 10;
  const helm = ret > 0 ? (() => { const f = seg(t, TL.retreat[0], TL.retreat[0] + 0.3), b = seg(t, TL.retreat[0] + 0.3, TL.retreat[0] + 0.5);
    return { x: 4 + f * 30 + b * 8, y: lerp(-58, -11, eIn(f)) - Math.sin(Math.PI * b) * 8, a: f * 1.2 + b * 0.35 }; })() : null;
  snail(g, sx, 905, 0.92, { ret: eOut(ret), bob: t * 7 * (1 - ret), helm, lance: 0.3 * eOut(ret) });
  const raise = eBack(seg(t, ...TL.raise)), blow = seg(t, ...TL.blow);
  rabbit(g, 640, 905, 0.95, { pose: 'trumpet', trA: lerp(-0.85, 0.08, raise) + Math.sin(t * 40) * 0.015 * (blow > 0 && blow < 1), blow: blow > 0 && blow < 1 ? Math.sin(Math.PI * blow) ** 0.3 : 0, t, lean: -0.06 * Math.sin(Math.PI * blow) });
  g.restore();
}
function pageB(t) {
  const B = PAGES.B; beginPage('B'); const g = PG;
  B.vine.draw(g, eOut(seg(t, ...TL.vineB)), seg(t, 3.9, 4.6) || -1);
  const mT = TL.mini, msh = seg(t, mT.shine0, mT.shine0 + 0.7);
  miniature(g, t, { ink: mT.ink, gild: mT.gild, col: mT.col, shine: msh > 0 && msh < 1 ? msh : -1 });
  linesP(B.cap, t);
  drollB(t);
  return endPage('B');
}
function pageC() {
  const C = PAGES.C; beginPage('C'); const g = PG;
  ruling(g, 150, 800, 280, 11, [[150, 455], [495, 800]]);
  C.vine.draw(g, 1, -1);
  linesP(C.head, 99); linesP(C.lines, 99);
  // pen-flourished W: red letter, blue hairline flourish running down the margin
  g.save(); g.font = `700 150px ${FT}`; g.fillStyle = COL.red; g.fillText('W', 150, 392); g.restore();
  g.save(); g.strokeStyle = COL.blue; g.lineWidth = 1.3; const r = mulberry(8);
  for (let y = 262; y < 400; y += 16) { g.beginPath(); g.arc(134, y, 5, -1.6, 1.6); g.stroke(); }
  for (let x = 150; x < 270; x += 16) { g.beginPath(); g.arc(x, 250, 5, Math.PI, TAU); g.stroke(); }
  g.beginPath(); for (let a = 0; a < 12; a += 0.2) g.lineTo(134 - Math.cos(a) * a * 1.6, 250 - Math.sin(a) * a * 1.6); g.stroke();
  g.beginPath(); for (let y = 400; y < 860; y += 4) g.lineTo(134 + Math.sin(y * 0.09) * 5, y); g.stroke();
  for (let y = 420; y < 860; y += 30 + r() * 12) { g.beginPath(); for (let a = 0; a < 9; a += 0.3) g.lineTo(134 + (r() < 2 ? -1 : 1) * (6 + a * 1.4) * Math.cos(a) * 0.9, y + a * 1.4 * Math.sin(a)); g.stroke(); }
  g.restore();
  return endPage('C');
}
function pageD(t) {
  const D = PAGES.D; beginPage('D'); const g = PG;
  ruling(g, 90, 740, 270, 6, [[90, 395], [435, 740]]);
  D.vine.draw(g, 1, seg(t, 8.9, 9.6) || -1);
  linesP(D.head, t); linesP(D.lines, t); linesP(D.final, t);
  panelInitial(g, 'S', D.ini, t, [7.25, 7.45], TL.dIni, TL.dShine, 57, 128);
  groundLine(g, 60, 800, 905, 9);
  // the loaf, the thief, the pursuer
  const hin = seg(t, ...TL.hopIn), hout = seg(t, ...TL.hopOut), has = t >= TL.grab;
  if (!has) loaf(g, 430, 896, 1.05);
  const sn = eInOut(seg(t, ...TL.snailD)); if (t > TL.snailD[0]) snail(g, lerp(-10, 190, sn), 905, 0.8, { bob: t * 6 });
  if (hin > 0) {
    let rx, air, dir = 1, pose = 'none';
    if (t < TL.grab) { rx = lerp(40, 470, hin); air = (hin * 2) % 1; }
    else if (hout <= 0) { rx = 470; air = 0; pose = 'loaf'; }
    else { rx = lerp(470, 770, eInOut(hout)); air = hout < 0.92 ? (hout * 3.2) % 1 : 0; pose = 'loaf'; }
    if (t >= TL.grab) dir = -1;
    rabbit(g, rx, 905, 0.8, { pose, air, dir, t });
  }
  return endPage('D');
}

// ── page turn: leaf B/C hinged at the gutter, bent & projected in strips ──
const HX = 960, TOP = 50, CY = 540, DCAM = 2300, NS = 110;
let LF, LB;
function leafAngle(t) {
  const l = eOut(seg(t, ...TL.lift)), u = eInOut(seg(t, ...TL.turn));
  return { th: 0.16 * l + (Math.PI - 0.16) * u, curl: 0.55 * l * (1 - u) };
}
function leafGeom(t) {
  const { th, curl } = leafAngle(t); const P = [[0, 0, th]]; let x = 0, z = 0;
  const settle = seg(t, ...TL.settle), bounce = settle > 0 ? -0.05 * Math.sin(Math.PI * settle) : 0;
  for (let i = 1; i <= NS; i++) {
    const u = i / NS, ph = clamp(th + (0.85 * Math.sin(th) + curl) * u * u + bounce * u * u, 0, Math.PI);
    x += Math.cos(ph) * PW / NS; z += Math.sin(ph) * PW / NS; P.push([x, z, ph]);
  }
  return P;
}
function drawLeaf(g, t, front, back) {
  const P = leafGeom(t), k = 1 - Math.sin(leafAngle(t).th);
  // leaf canvases with gutter shading fading as the leaf lifts
  LF = LF || mk(PW, PH); LB = LB || mk(PW, PH);
  let q = LF.getContext('2d'); q.drawImage(front, 0, 0); q.globalAlpha = k; q.drawImage(GUT_R, 0, 0); q.globalAlpha = 1;
  q = LB.getContext('2d'); q.drawImage(back, 0, 0); q.globalAlpha = Math.max(0, -Math.cos(leafAngle(t).th)) * k; q.drawImage(GUT_L, 0, 0); q.globalAlpha = 1;
  // cast shadow on the pages below (light from the upper left)
  g.save(); g.beginPath(); g.rect(80, TOP, 1760, PH); g.clip(); g.filter = 'blur(14px)';
  const sa = 0.4 * Math.sin(leafAngle(t).th);
  g.fillStyle = `rgba(30,15,5,${sa})`; g.beginPath(); g.moveTo(HX, TOP + 10);
  for (const [x, z] of P) g.lineTo(HX + x + z * 0.32, TOP + 10 + z * 0.05);
  for (let i = P.length - 1; i >= 0; i--) g.lineTo(HX + P[i][0] + P[i][1] * 0.32, TOP + PH - 6 + P[i][1] * 0.02);
  g.closePath(); g.fill(); g.filter = 'none'; g.restore();
  // strips
  const sw = PW / NS;
  for (let i = 0; i < NS; i++) {
    const [xa, za] = P[i], [xb, zb, ph] = P[i + 1];
    const sa2 = DCAM / (DCAM - za), sb = DCAM / (DCAM - zb), sm = (sa2 + sb) / 2;
    const Xa = HX + xa * sa2, Xb = HX + xb * sb, top = CY + (TOP - CY) * sm, hh = PH * sm;
    const shade = Math.sin(ph);
    if (Xb >= Xa) {
      g.drawImage(LF, i * sw, 0, sw, PH, Xa, top, Xb - Xa + 0.9, hh);
      g.fillStyle = `rgba(40,22,8,${0.3 * shade * (ph < 1.2 ? 0.7 : 1)})`; g.fillRect(Xa, top, Xb - Xa, hh);
      const hi = 0.16 * Math.exp(-(((ph - 0.9) / 0.25) ** 2)); if (hi > 0.01) { g.fillStyle = `rgba(255,248,228,${hi})`; g.fillRect(Xa, top, Xb - Xa, hh); }
    } else {
      g.drawImage(LB, PW - (i + 1) * sw, 0, sw, PH, Xb, top, Xa - Xb + 0.9, hh);
      g.fillStyle = `rgba(40,22,8,${0.34 * shade})`; g.fillRect(Xb, top, Xa - Xb, hh);
    }
  }
  // edge line at the free edge for thickness
  const [xe, ze] = P[NS], se = DCAM / (DCAM - ze); g.strokeStyle = 'rgba(120,90,55,0.6)'; g.lineWidth = 1.5;
  g.beginPath(); g.moveTo(HX + xe * se, CY + (TOP - CY) * se); g.lineTo(HX + xe * se, CY + (TOP - CY) * se + PH * se); g.stroke();
}

// ── quill choreography (spread coords) ──
const ORIG = { A: [80, 50], B: [960, 50], C: [80, 50], D: [960, 50] };
function quillAt(t) {
  const W = WR; const sp = (w, p) => { const o = ORIG[w.page], l = w.line, n = l.words.reduce((a, q) => a + q.s.length, 0);
    return [o[0] + l.x + l.w * p, o[1] + l.y - 4 - Math.abs(Math.sin(p * n * Math.PI)) * 7, 0]; };
  const OFF = [[2150, 820], [2150, 380]];
  const firstD = W.findIndex(w => w.page === 'D'), lastB = W.findIndex(w => w.page === 'B');
  const ent = [[0.15, W[0]], [6.85, W[firstD]]], ex = [[W[lastB].t1, W[lastB]], [W[W.length - 1].t1, W[W.length - 1]]];
  for (const [t0, w] of ent) if (t >= t0 && t < w.t0) { const u = eOut(seg(t, t0, w.t0)), a = sp(w, 0); return [lerp(OFF[0][0], a[0], u), lerp(OFF[0][1], a[1], u), 1 - u]; }
  for (const [t0, w] of ex) if (t >= t0 && t < t0 + 0.55) { const u = eIn(seg(t, t0, t0 + 0.55)), a = sp(w, 1); return [lerp(a[0], OFF[1][0], u), lerp(a[1], OFF[1][1], u), u]; }
  for (let i = 0; i < W.length; i++) {
    const w = W[i];
    if (t >= w.t0 && t <= w.t1) return sp(w, seg(t, w.t0, w.t1));
    const nx = W[i + 1];
    if (nx && t > w.t1 && t < nx.t0 && nx.page === w.page || nx && t > w.t1 && t < nx.t0 && w.page === 'A' && nx.page === 'B') {
      const u = eInOut(seg(t, w.t1, nx.t0)), a = sp(w, 1), b = sp(nx, 0), lift = Math.sin(Math.PI * u);
      return [lerp(a[0], b[0], u), lerp(a[1], b[1], u) - lift * 26, lift * 0.6];
    }
  }
  return null;
}

// ── frame ──
function frame(t) {
  const g = X; g.setTransform(1, 0, 0, 1, 0, 0);
  const s = 1.0 + 0.04 * eSine(clamp(t / 10)), fx = lerp(935, 985, eSine(seg(t, 3.2, 7.6)));
  g.setTransform(s, 0, 0, s, 960 - fx * s, 540 - 540 * s);
  g.fillStyle = '#140b06'; g.fillRect(-200, -200, 2400, 1500); g.drawImage(DESK, 0, 0);
  const inTurn = t >= TL.lift[0] && t < TL.settle[1];
  const turned = t >= TL.turn[1];
  // left page: A until the leaf lands, then C; right page: B until the lift, then D
  g.drawImage(turned ? PC.C : pageA(t), 80, TOP);
  g.drawImage(t < TL.lift[0] ? pageB(t) : pageD(t), 960, TOP);
  g.drawImage(GUT_L, 80, TOP); g.drawImage(GUT_R, 960, TOP);
  if (inTurn && !(t >= TL.turn[1])) drawLeaf(g, t, pageB(t), PC.C);
  else if (inTurn) drawLeaf(g, t, pageB(t), PC.C);
  // fold crease
  g.fillStyle = 'rgba(40,22,10,0.5)'; g.fillRect(958.5, TOP, 3, PH);
  // quill
  const q = quillAt(t); if (q) drawQuill(g, q[0], q[1], q[2], -0.04 + Math.sin(t * 3.1) * 0.03 - q[2] * 0.06);
  // candle-light: warm breathing vignette + fade in/out
  g.setTransform(1, 0, 0, 1, 0, 0);
  const vg = g.createRadialGradient(900, 470, 380, 960, 540, 1250), fl = 0.03 * Math.sin(t * 5.3) + 0.02 * Math.sin(t * 8.9);
  vg.addColorStop(0, 'rgba(255,200,120,0.04)'); vg.addColorStop(0.6, `rgba(20,8,0,${0.1 + fl})`); vg.addColorStop(1, `rgba(10,4,0,${0.55 + fl})`);
  g.fillStyle = vg; g.fillRect(0, 0, 1920, 1080);
  const dark = 1 - eOut(seg(t, ...TL.fadeIn)) + eInOut(seg(t, ...TL.fadeOut));
  if (dark > 0) { g.fillStyle = `rgba(8,4,2,${clamp(dark)})`; g.fillRect(0, 0, 1920, 1080); }
}

window.draw = ({ t }) => { frame(t); return cv.toDataURL('image/jpeg', 0.92).split(',')[1]; };
window.events = () => {
  const ev = [];
  for (const w of WR) ev.push({ k: 'write', t: +w.t0.toFixed(3), d: +(w.t1 - w.t0).toFixed(3), red: w.line.words[0].c === COL.red, n: w.line.words.reduce((a, q) => a + q.s.length, 0) });
  ev.push({ k: 'gild', t: TL.iniGild[0], d: TL.iniGild[1] - TL.iniGild[0] }, { k: 'shine', t: TL.iniShine[0] }, { k: 'vine', t: TL.vineA[0], d: TL.vineA[1] - TL.vineA[0] });
  ev.push({ k: 'vine', t: TL.vineB[0], d: TL.vineB[1] - TL.vineB[0] }, { k: 'gild', t: TL.mini.gild[0], d: 0.5 }, { k: 'paint', t: TL.mini.col[0], d: TL.mini.col[1] - TL.mini.col[0] });
  ev.push({ k: 'fire', t: TL.mini.col[0] + 0.3 }, { k: 'shine', t: TL.mini.shine0 });
  ev.push({ k: 'snail', t: TL.march[0], d: TL.march[1] - TL.march[0] }, { k: 'trumpet', t: TL.blow[0], d: TL.blow[1] - TL.blow[0] }, { k: 'retreat', t: TL.retreat[0] }, { k: 'clank', t: TL.retreat[0] + 0.3 });
  ev.push({ k: 'lift', t: TL.lift[0] }, { k: 'turn', t: TL.turn[0], d: TL.turn[1] - TL.turn[0] }, { k: 'land', t: TL.turn[1] });
  ev.push({ k: 'gild', t: TL.dIni[0], d: TL.dIni[1] - TL.dIni[0] }, { k: 'shine', t: TL.dShine[0] });
  for (let h = 0; h < 2; h++) ev.push({ k: 'hop', t: TL.hopIn[0] + (h + 1) * (TL.hopIn[1] - TL.hopIn[0]) / 2 });
  ev.push({ k: 'grab', t: TL.grab });
  for (let h = 0; h < 3; h++) ev.push({ k: 'hop', t: TL.hopOut[0] + (h + 1) / 3.2 * (TL.hopOut[1] - TL.hopOut[0]) });
  ev.push({ k: 'end', t: 9.1 });
  return ev;
};
window.ready = (async () => {
  await document.fonts.load(BODY); await document.fonts.load(TIT); await document.fonts.load(HEAD); await document.fonts.ready;
  bakeDesk(); bakeGutters(); bakeQuill(); bakeMiniature();
  VEL.A = bakeVellum(101, 'L'); VEL.B = bakeVellum(102, 'R'); VEL.C = bakeVellum(103, 'L'); VEL.D = bakeVellum(104, 'R');
  for (const k of 'ABCD') TOOTH[k] = bakeTooth(200 + k.charCodeAt(0));
  layout(); buildSchedule(); pageC();
})();
