// cave-painting: "The first story ever told"
// Pipeline per frame: paint layer (2D, screen space) → WebGL2 limestone shader (procedural relief, normal-mapped
// torchlight, pigment soaking into the rock grain) → 2D overlay (flame, embers, pigment puff) → JPEG.
'use strict';
const DUR = 10;
const out = document.getElementById('c'), octx = out.getContext('2d');
const paint = Object.assign(document.createElement('canvas'), { width: W, height: H }), pctx = paint.getContext('2d');
const glc = Object.assign(document.createElement('canvas'), { width: W, height: H });
const gl = glc.getContext('webgl2', { preserveDrawingBuffer: true, antialias: false, alpha: false });

// ---------- timeline ----------
const CAM_END = 1300;
const camX = t => CAM_END * eio(seg(t, 2.0, 5.7));
const RUN0 = 2.5, RUN1 = 5.7;                       // herd gallops between these times
const PUFFS = [6.05, 6.4, 6.75];                     // hand-stencil spray puffs
const TITLE0 = 7.05, SUB0 = 8.05, DIM0 = 8.7, FADE0 = 9.25, FADE1 = 9.85;
const HAND = { x: 2770, y: 440 };                    // world position of the hand stencil
const TITLE = { x: 1980, y: 875, w: 1000 };           // world position (center/baseline) of the painted title
const AUROCHS = { kind: 'aurochs', x: 660, y: 440, s: 270, dir: -1, fill: PIG.red, shade: 0.42, ghosts: 0.3, farDx: 0.13 };
const DOTS = Array.from({ length: 7 }, (_, i) => [1210 + i * 38 + (i % 2) * 6, 250 + Math.sin(i * 1.3) * 10, 13 + (i % 3) * 2]);
const HERD = [
  { kind: 'horse', x: 1640, y: 300, s: 140, fill: PIG.red, shade: 0.5, lag: 0.0, off: 0 },
  { kind: 'horse', x: 2090, y: 370, s: 162, fill: PIG.yel, shade: 0.55, lag: 0.12, off: 1 },
  { kind: 'deer', x: 1880, y: 570, s: 132, fill: PIG.red, shade: 0.35, lag: 0.25, off: 2 },
  { kind: 'horse', x: 1480, y: 610, s: 128, fill: PIG.brown, shade: 0.45, lag: 0.18, off: 3 },
  { kind: 'deer', x: 2330, y: 620, s: 124, fill: PIG.yel, shade: 0.4, lag: 0.08, off: 1 },
];
const RUN_DIST = 320;

function flicker(t) {
  return 0.84 + 0.07 * Math.sin(6.28 * 6.1 * t) + 0.05 * Math.sin(6.28 * 11.3 * t + 1.3) + 0.14 * (N1(t * 14) - 0.5) + 0.1 * (N1(t * 5 + 30) - 0.5);
}
function light(t) {
  const ign = eo(seg(t, 0.62, 1.7));
  const spark = Math.max(0, 1 - Math.abs(t - 0.36) / 0.05) * 0.35 + Math.max(0, 1 - Math.abs(t - 0.48) / 0.05) * 0.45;
  const dim = lerp(1, 0.24, eio(seg(t, DIM0, FADE1)));
  let lx = lerp(330, 560, eio(seg(t, 0.6, 2.0)));
  lx = lerp(lx, 920, eio(seg(t, 2.0, 5.2)));
  lx = lerp(lx, 1250, eio(seg(t, 5.3, 6.2)));
  const jit = ign * 7;
  return { x: lx + jit * (N1(t * 9 + 5) - 0.5), y: 700 + jit * (N1(t * 8 + 50) - 0.5), z: 470, R: lerp(330, 1050, eo(seg(t, 0.6, 2.6))),
    I: (ign * flicker(t) + spark * (1 - ign)) * dim, flame: ign * dim, sparkI: spark * (1 - ign) };
}
const fadeOut = t => 1 - eio(seg(t, FADE0, FADE1));

// ---------- hand stencil (precomputed: spray dots around a hand mask, three puff layers) ----------
const HS = 820;
function handPath(c) {
  // left hand pressed flat, fingers slightly spread; wrist fades out of the spray below
  c.beginPath(); smoothClosed(c, [[-78, 96], [-88, 30], [-84, -34], [-58, -62], [0, -70], [58, -60], [84, -30], [90, 26], [80, 70], [56, 104]]); c.fill();
  c.beginPath(); smoothClosed(c, [[-64, 80], [-68, 170], [-62, 240], [54, 240], [60, 170], [62, 84]]); c.fill();
  const finger = (bx, by, ang, len, w) => {
    const a = ang * Math.PI / 180, k = 0.05;
    const m = [bx + Math.sin(a) * len * 0.52, by - Math.cos(a) * len * 0.52], e = [bx + Math.sin(a + k) * len, by - Math.cos(a + k) * len];
    taper(c, [[bx, by], m, e], [w, w * 0.94, w * 0.82]);
  };
  finger(-66, -40, -22, 100, 34); finger(-28, -58, -8, 134, 38); finger(12, -62, 3, 148, 39); finger(52, -52, 14, 130, 37);
  finger(70, 58, 54, 118, 46); taper(c, [[40, 70], [70, 58]], [60, 46]);
}
const stencil = [0, 1, 2].map(k => {
  const cv = Object.assign(document.createElement('canvas'), { width: HS, height: HS }), c = cv.getContext('2d'), r = rng(900 + k * 17);
  c.translate(HS / 2, HS / 2);
  const hz = c.createRadialGradient(0, -20, 20, 0, -20, 320); hz.addColorStop(0, rgba(PIG.red, 0.3)); hz.addColorStop(0.55, rgba(PIG.red, 0.16)); hz.addColorStop(1, rgba(PIG.red, 0));
  c.fillStyle = hz; c.fillRect(-HS / 2, -HS / 2, HS, HS);
  for (let i = 0; i < 15000; i++) {
    const ang = r() * 6.2832, rad = 190 * Math.sqrt(-2 * Math.log(1 - r() * 0.999)) * (0.75 + 0.5 * N1(ang * 3 + k * 7));
    const x = Math.cos(ang) * rad * 1.05, y = Math.sin(ang) * rad * 0.9 - 25;
    if (y > 120 && r() < clamp((y - 120) / 140)) continue;
    const s = 0.8 + r() * r() * 3.5; c.fillStyle = rgba(PIG.red, 0.18 + r() * 0.3); c.beginPath(); c.arc(x, y, s, 0, 7); c.fill();
  }
  // denser pigment hugging the hand's edge (where the spray hit the fingers), then the hand itself masks the rock
  c.save(); c.filter = 'blur(16px)'; c.globalAlpha = 0.4; c.fillStyle = rgba(PIG.red, 1); c.translate(0, -8); c.scale(1.08, 1.05); handPath(c); c.restore();
  c.globalCompositeOperation = 'destination-out'; c.shadowColor = '#000'; c.shadowBlur = 3; c.fillStyle = '#000'; handPath(c);
  return cv;
});

// ---------- title ----------
const TITLE_TXT = 'THE FIRST STORY EVER TOLD', SUB_TXT = 'told in ochre and charcoal, by firelight';
let titleSize = 140, letters = [];
function layoutTitle() {
  pctx.font = `700 ${titleSize}px 'Amatic SC'`; const w = pctx.measureText(TITLE_TXT).width;
  titleSize = Math.floor(titleSize * TITLE.w / w); pctx.font = `700 ${titleSize}px 'Amatic SC'`;
  let x = TITLE.x - pctx.measureText(TITLE_TXT).width / 2;
  letters = [...TITLE_TXT].map((ch, i) => { const o = { ch, x, i }; x += pctx.measureText(ch).width; return o; });
}

// ---------- paint layer ----------
function drawPaint(t) {
  const cx = camX(t);
  pctx.setTransform(1, 0, 0, 1, 0, 0); pctx.clearRect(0, 0, W, H); pctx.translate(-cx, 0);
  // decorative red dots (a sign row, no meaning implied)
  for (const [x, y, r] of DOTS) { pctx.fillStyle = rgba(PIG.red, 0.85); pctx.beginPath(); pctx.ellipse(x, y, r, r * 0.9, 0.3, 0, 7); pctx.fill(); }
  // the aurochs: flip-book legs start stepping once the flame is up
  const ph = t < 1.25 ? 0 : Math.floor(t * 8);
  drawAnimal(pctx, { ...AUROCHS, phase: ph, amp: 0.6 });
  // the herd
  for (const a of HERD) {
    const k = seg(t, RUN0 + a.lag * 0.5, RUN1 - 0.25 + a.lag);
    const dx = -RUN_DIST * (1 - eo(k)) * (1 + a.lag * 0.4);
    const running = t > RUN0 + a.lag * 0.5 && k < 1;
    const bob = running ? Math.sin((Math.floor(t * 10) + a.off) * Math.PI / 2) * 6 : 0;
    drawAnimal(pctx, { ...a, x: a.x + dx, y: a.y - bob, dir: 1, phase: running ? Math.floor(t * 10) + a.off : 0, amp: 1, ghosts: running ? 0.14 : 0.3 * eo(seg(t, RUN1 - 0.3 + a.lag, RUN1 + 0.3 + a.lag)) + 0.02 });
  }
  // hand stencil
  PUFFS.forEach((p, k) => { const a = eo(seg(t, p, p + 0.3)); if (a > 0) { pctx.globalAlpha = a; pctx.drawImage(stencil[k], HAND.x - HS / 2, HAND.y - HS / 2); pctx.globalAlpha = 1; } });
  // painted title, letter by letter (each letter soaks in with a small double dab)
  pctx.font = `700 ${titleSize}px 'Amatic SC'`; pctx.textBaseline = 'alphabetic';
  for (const L of letters) {
    const a = eo(seg(t, TITLE0 + L.i * 0.042, TITLE0 + L.i * 0.042 + 0.28)); if (a <= 0 || L.ch === ' ') continue;
    pctx.fillStyle = rgba([132, 38, 22], a); pctx.strokeStyle = rgba([132, 38, 22], a); pctx.lineWidth = 6; pctx.lineJoin = 'round'; pctx.fillText(L.ch, L.x, TITLE.y); pctx.strokeText(L.ch, L.x, TITLE.y);
    pctx.fillStyle = rgba(PIG.red, 0.4 * a); pctx.fillText(L.ch, L.x + 3, TITLE.y - 2.5);
  }
  const sa = eo(seg(t, SUB0, SUB0 + 0.6));
  if (sa > 0) { pctx.font = `700 ${Math.round(titleSize * 0.44)}px 'Amatic SC'`; pctx.textAlign = 'center'; pctx.fillStyle = rgba(PIG.char, 0.85 * sa); pctx.fillText(SUB_TXT, TITLE.x, TITLE.y + titleSize * 0.52); pctx.textAlign = 'left'; }
}

// ---------- WebGL limestone ----------
const VS = `#version 300 es
in vec2 p; void main(){ gl_Position = vec4(p,0.,1.); }`;
const FS = `#version 300 es
precision highp float;
uniform sampler2D uPaint; uniform vec2 uRes; uniform float uCam; uniform vec3 uL; uniform float uI; uniform float uG; uniform float uFade; uniform vec2 uF; uniform float uR;
out vec4 o;
uint hsh(uvec2 v){ v = v*1664525u+1013904223u; v.x += v.y*1664525u; v.y += v.x*1664525u; v ^= v>>16u; v.x += v.y*1664525u; v.y += v.x*1664525u; v ^= v>>16u; return v.x^v.y; }
float h2(vec2 i){ return float(hsh(uvec2(ivec2(i)+ivec2(60000)))&0xffffffu)/16777215.0; }
float vn(vec2 p){ vec2 i=floor(p), f=fract(p); vec2 u=f*f*(3.-2.*f);
  return mix(mix(h2(i),h2(i+vec2(1,0)),u.x),mix(h2(i+vec2(0,1)),h2(i+vec2(1,1)),u.x),u.y); }
float fbm(vec2 p){ float s=0., a=.5; for(int k=0;k<5;k++){ s+=a*vn(p); p=p*2.03+vec2(17.1,9.7); a*=.5; } return s/.97; }
float vedge(vec2 p){
  vec2 i=floor(p), f=fract(p); float d1=8., d2=8.;
  for(int y=-1;y<=1;y++) for(int x=-1;x<=1;x++){ vec2 g=vec2(x,y); vec2 o=vec2(h2(i+g), h2(i+g+vec2(31.,17.)));
    vec2 r=g+o-f; float d=dot(r,r); if(d<d1){ d2=d1; d1=d; } else if(d<d2) d2=d; }
  return sqrt(d2)-sqrt(d1);
}
float crackF(vec2 w){
  vec2 q = w + 22.*vec2(fbm(w/70.+2.)-.5, fbm(w/70.+8.)-.5);
  float c = (1.-smoothstep(.3, 1.8, vedge(vec2(q.x/520., q.y/340.))*200.)) * smoothstep(.56,.64,fbm(w/420.+7.));
  c = max(c, .6*(1.-smoothstep(.2, 1.1, vedge(q/150.+9.)*75.)) * smoothstep(.66,.72,fbm(w/260.+21.)));
  return c;
}
float height(vec2 w){
  float h = fbm(w/640.)*1.0 + fbm(w/160.+3.1)*0.42 + fbm(w/40.)*0.1 + vn(w/7.)*0.015;
  return h - crackF(w)*0.05;
}
void main(){
  vec2 fc = gl_FragCoord.xy; vec2 s = vec2(fc.x, uRes.y-fc.y); vec2 w = s + vec2(uCam,0.);
  float e = 1.5, HS = 95.;
  float h = height(w);
  float hx = height(w+vec2(e,0.)) - height(w-vec2(e,0.)), hy = height(w+vec2(0.,e)) - height(w-vec2(0.,e));
  vec3 n = normalize(vec3(-hx*HS/(2.*e), -hy*HS/(2.*e), 1.));
  float cr = crackF(w);
  // limestone albedo: cream/grey, ochre iron staining, white calcite curtains, darker hollows and cracks
  float m1 = fbm(w/260.+20.);
  vec3 alb = mix(vec3(.76,.68,.56), vec3(.6,.575,.53), smoothstep(.35,.7,m1));
  alb = mix(alb, vec3(.72,.5,.33), .55*smoothstep(.5,.78,fbm(w/190.+40.)));
  alb = mix(alb, vec3(.88,.85,.78), .6*smoothstep(.62,.8,fbm(vec2(w.x/45., w.y/520.)+60.)));
  alb *= mix(.78, 1.08, smoothstep(.2,.9,h)) * (1.-cr*.55);
  alb *= .9 + .2*vn(w/3.);
  // pigment: soaks into the grain, skips pores and cracks
  vec4 pc = texture(uPaint, fc/uRes);
  float grain = smoothstep(.22,.72, vn(w/2.2)*.45 + fbm(w/11.)*.75);
  float a = pc.a * mix(.62, 1., grain) * (1.-cr*.6) * mix(.86,1.,smoothstep(.3,.8,fbm(w/70.+90.)));
  alb = mix(alb, pc.rgb, min(1., a*1.02));
  // torchlight
  vec3 P = vec3(s, h*HS);
  vec3 Ld = uL - P; float d = length(Ld); Ld /= d;
  float att = uI / (1. + pow(d/uR, 2.));
  float dif = max(dot(n, Ld), 0.);
  vec3 lc = vec3(1., .6, .3);
  vec3 col = alb * lc * (dif*att*2.1 + att*.12) + alb*vec3(.012,.013,.02);
  float glint = step(.992, h2(floor(w/2.))) * (1.-a);
  vec3 Hh = normalize(Ld + vec3(0,0,1)); col += lc * pow(max(dot(n,Hh),0.),50.) * att * (.06 + glint*1.6);
  col += lc * uI * .06 * exp(-length(uF - s)/420.);
  col = 1. - exp(-col*1.25);
  vec2 uv = fc/uRes; col *= 1. - .45*pow(clamp(length((uv-.5)*vec2(1.,.85))*1.35,0.,1.), 2.4);
  col += (h2(fc + vec2(uG*131., uG*57.)) - .5) * .03;
  o = vec4(col*uFade, 1.);
}`;
function sh(type, src) { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; }
const prog = gl.createProgram(); gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(prog);
if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
gl.useProgram(prog);
const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
const loc = gl.getAttribLocation(prog, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
const tex = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tex);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
const U = n => gl.getUniformLocation(prog, n);
gl.viewport(0, 0, W, H);

// ---------- overlay: flame, embers, pigment puff ----------
const fcv = Object.assign(document.createElement('canvas'), { width: W, height: H }), fctx = fcv.getContext('2d');
function drawFlame(c0, L, t) {
  let c = c0;
  if (L.sparkI > 0.02) { // flint sparks before the torch catches
    const r = rng(77 + Math.floor(t * 30));
    c.globalCompositeOperation = 'lighter';
    for (let i = 0; i < 14; i++) { const a = -Math.PI / 2 + (r() - 0.5) * 2.2, d = 20 + r() * 120 * L.sparkI;
      c.fillStyle = `rgba(255,${180 + r() * 60 | 0},90,${L.sparkI})`; c.beginPath(); c.arc(330 + Math.cos(a) * d, 1000 + Math.sin(a) * d, 2 + r() * 2, 0, 7); c.fill(); }
    c.globalCompositeOperation = 'source-over';
  }
  const f = L.flame * (0.85 + 0.25 * (flicker(t) - 0.84));
  if (f <= 0.01) return;
  const bx = L.x, by = 1150 - (1 - f) * 70, hgt = 400 * f;
  c.save(); c.globalCompositeOperation = 'lighter';
  const g = c.createRadialGradient(bx, by - hgt * 0.4, 0, bx, by - hgt * 0.4, 420 * f);
  g.addColorStop(0, `rgba(255,150,60,${0.28 * f})`); g.addColorStop(1, 'rgba(255,120,40,0)'); c.fillStyle = g; c.fillRect(bx - 500, by - 700, 1000, 700);
  c.restore(); c = fctx; c.clearRect(bx - 400, 0, 800, H); c.save(); c.globalCompositeOperation = 'lighter';
  const tongues = [[1, 1, [240, 80, 25], 0.42], [0.72, 0.8, [255, 140, 40], 0.4], [0.45, 0.55, [255, 205, 110], 0.42], [0.22, 0.3, [255, 240, 200], 0.5]];
  for (let j = 0; j < 3; j++) {
    const ox = (j - 1) * 34 * f, hj = hgt * (j === 1 ? 1 : 0.72 + 0.2 * N1(t * 6 + j * 9));
    for (const [ws, hs, col, al] of tongues) {
      const w = 62 * f * ws, h = hj * hs, sway = (N1(t * 7 + j * 3) - 0.5) * 50 * f, sway2 = (N1(t * 11 + j * 5 + 20) - 0.5) * 30 * f;
      const gg = c.createLinearGradient(0, by, 0, by - h);
      gg.addColorStop(0, `rgba(${col[0]},${col[1]},${col[2]},${al * f})`); gg.addColorStop(1, `rgba(${col[0]},${col[1] * 0.6 | 0},${col[2] * 0.4 | 0},0)`);
      c.fillStyle = gg; c.beginPath(); c.moveTo(bx + ox - w, by);
      c.bezierCurveTo(bx + ox - w * 1.1, by - h * 0.45, bx + ox + sway2 - w * 0.4, by - h * 0.7, bx + ox + sway, by - h);
      c.bezierCurveTo(bx + ox + sway2 + w * 0.4, by - h * 0.7, bx + ox + w * 1.1, by - h * 0.45, bx + ox + w, by); c.fill();
    }
  }
  c.restore(); c = c0; c.save(); c.globalCompositeOperation = 'lighter'; c.filter = 'blur(2.5px)';
  c.drawImage(fcv, bx - 400, 0, 800, H, bx - 400, 0, 800, H); c.filter = 'none';
  // embers: each rises on its own loop, deterministic in t
  for (let i = 0; i < 26; i++) {
    const r = rng(300 + i), per = 1.1 + r() * 1.3, ph = ((t + r() * per) % per) / per, life = Math.sin(Math.PI * ph);
    const x = bx + (r() - 0.5) * 80 + Math.sin(t * (1.5 + r() * 2) + i) * 30 * ph + (r() - 0.5) * 120 * ph, y = by - 60 - ph * (260 + r() * 300);
    c.fillStyle = `rgba(255,${150 + r() * 80 | 0},70,${0.8 * life * f})`; c.beginPath(); c.arc(x, y, 1.4 + r() * 2, 0, 7); c.fill();
  }
  c.restore();
}
function drawPuffs(c, t, L) {
  const hx = HAND.x - camX(t), hy = HAND.y;
  PUFFS.forEach((p, k) => {
    const u = seg(t, p - 0.05, p + 1.1); if (u <= 0 || u >= 1) return;
    const r = rng(500 + k);
    for (let i = 0; i < 34; i++) {
      const a = r() * 6.28, d = (40 + r() * 230) * (0.35 + eo(u) * 0.9), rad = (40 + r() * 70) * (0.6 + u * 1.2);
      const x = hx + Math.cos(a) * d - 30 + u * 40, y = hy + Math.sin(a) * d * 0.8 - u * 60 + 20;
      const al = 0.16 * Math.sin(Math.PI * Math.sqrt(u)) * (0.5 + r()) * Math.min(1, L.I * 1.3);
      const g = c.createRadialGradient(x, y, 0, x, y, rad); g.addColorStop(0, `rgba(196,92,52,${al})`); g.addColorStop(1, 'rgba(196,92,52,0)');
      c.fillStyle = g; c.fillRect(x - rad, y - rad, rad * 2, rad * 2);
    }
  });
}

// ---------- frame ----------
window.draw = ({ t }) => {
  const L = light(t);
  drawPaint(t);
  gl.bindTexture(gl.TEXTURE_2D, tex); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, paint);
  gl.uniform1i(U('uPaint'), 0); gl.uniform2f(U('uRes'), W, H); gl.uniform1f(U('uCam'), camX(t));
  gl.uniform3f(U('uL'), L.x, L.y, L.z); gl.uniform1f(U('uI'), L.I); gl.uniform2f(U('uF'), L.x, 1040); gl.uniform1f(U('uR'), L.R); gl.uniform1f(U('uG'), Math.floor(t * 12) % 64); gl.uniform1f(U('uFade'), fadeOut(t));
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  octx.globalCompositeOperation = 'source-over'; octx.drawImage(glc, 0, 0);
  octx.globalAlpha = fadeOut(t); drawPuffs(octx, t, L); drawFlame(octx, L, t); octx.globalAlpha = 1;
  return out.toDataURL('image/jpeg', 0.92).split(',')[1];
};

// ---------- sound events ----------
window.events = () => {
  const ev = [{ k: 'spark', t: 0.34 }, { k: 'spark', t: 0.46 }, { k: 'ignite', t: 0.6 }];
  for (let n = Math.ceil(RUN0 * 10); n < RUN1 * 10 + 2; n++) ev.push({ k: 'hoof', t: n / 10, v: (n % 4 === 0 ? 1 : n % 2 ? 0.55 : 0.75) * (0.6 + 0.4 * Math.sin(Math.PI * seg(n / 10, RUN0, RUN1 + 0.2))) });
  ev.push({ k: 'freeze', t: RUN1 });
  PUFFS.forEach(p => ev.push({ k: 'puff', t: p - 0.04 }));
  letters.forEach(L => { if (L.ch !== ' ' && L.i % 2 === 0) ev.push({ k: 'dab', t: TITLE0 + L.i * 0.042 }); });
  ev.push({ k: 'dab', t: SUB0, v: 0.6 });
  [[1.4, 62, 1.6], [3.2, 69, 1.2], [4.6, 67, 1.4], [7.1, 64, 1.8], [8.3, 62, 1.6]].forEach(([t, m, d]) => ev.push({ k: 'flute', t, m, d }));
  ev.push({ k: 'dim', t: DIM0 });
  return ev;
};

window.ready = (async () => { await document.fonts.load(`700 140px 'Amatic SC'`); await document.fonts.ready; layoutTitle(); })();
