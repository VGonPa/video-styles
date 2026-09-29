// cave-painting: small deterministic helpers (seeded RNG, easing, 1D noise, smooth closed paths)
'use strict';
const W = 1920, H = 1080;
function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, k) => a + (b - a) * k;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eio = k => k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
const eo = k => 1 - Math.pow(1 - k, 3);
const ei = k => k * k * k;
const eback = k => { const c = 1.9; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
// smooth 1D value noise, deterministic
const N1 = (() => { const r = rng(4242), v = Array.from({ length: 512 }, r); return x => { const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f); return lerp(v[((i % 512) + 512) % 512], v[(((i + 1) % 512) + 512) % 512], u); }; })();
// closed Catmull-Rom spline through points → current path
function smoothClosed(ctx, P) {
  const n = P.length; ctx.moveTo(P[0][0], P[0][1]);
  for (let i = 0; i < n; i++) {
    const p0 = P[(i - 1 + n) % n], p1 = P[i], p2 = P[(i + 1) % n], p3 = P[(i + 2) % n];
    ctx.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]);
  }
  ctx.closePath();
}
// open Catmull-Rom spline
function smoothOpen(ctx, P) {
  const n = P.length; ctx.moveTo(P[0][0], P[0][1]);
  for (let i = 0; i < n - 1; i++) {
    const p0 = P[Math.max(0, i - 1)], p1 = P[i], p2 = P[i + 1], p3 = P[Math.min(n - 1, i + 2)];
    ctx.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]);
  }
}
// tapered stroke along an open polyline: widths per point → filled polygon + round joints
function taper(ctx, P, Wd) {
  const L = [], R = [];
  for (let i = 0; i < P.length; i++) {
    const a = P[Math.max(0, i - 1)], b = P[Math.min(P.length - 1, i + 1)];
    let dx = b[0] - a[0], dy = b[1] - a[1]; const l = Math.hypot(dx, dy) || 1; dx /= l; dy /= l;
    L.push([P[i][0] - dy * Wd[i] / 2, P[i][1] + dx * Wd[i] / 2]); R.push([P[i][0] + dy * Wd[i] / 2, P[i][1] - dx * Wd[i] / 2]);
  }
  ctx.beginPath(); ctx.moveTo(L[0][0], L[0][1]); for (const p of L.slice(1)) ctx.lineTo(p[0], p[1]);
  for (const p of R.reverse()) ctx.lineTo(p[0], p[1]); ctx.closePath(); ctx.fill();
  for (let i = 0; i < P.length; i++) { ctx.beginPath(); ctx.arc(P[i][0], P[i][1], Wd[i] / 2, 0, 7); ctx.fill(); }
}
