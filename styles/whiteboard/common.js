// Shared drawing kit for the hand-drawn styles (whiteboard, chalkboard, blueprint, single-line).
// The canonical copy lives in tools/common.js; each of those styles loads an identical copy with
// <script src="common.js">. Everything here is a plain global so anim.html can use it directly.

// Stage: the 1920x1080 canvas every style draws on.
const W = 1920, H = 1080;
const cv = document.getElementById('c');
const ctx = cv.getContext('2d');

// ---- numbers ----
const clamp = (v, lo = 0, hi = 1) => (v < lo ? lo : v > hi ? hi : v);
const lerp = (from, to, k) => from + (to - from) * k;
// Progress of t through the window [start, end], clamped to 0..1.
const seg = (t, start, end) => clamp((t - start) / (end - start));

// ---- easing curves (input and output in 0..1) ----
const ein = k => k * k * k;
const eout = k => 1 - Math.pow(1 - k, 3);
const eio = k => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(2 - 2 * k, 3) / 2);
const eio2 = k => (k < 0.5 ? 2 * k * k : 1 - Math.pow(2 - 2 * k, 2) / 2);
// Overshoots past 1 and settles back; `over` controls how far.
const eback = (k, over = 1.70158) => {
  const d = clamp(k) - 1;
  return 1 + (over + 1) * Math.pow(d, 3) + over * Math.pow(d, 2);
};

// Seeded generator: returns a function yielding floats in [0, 1). 32-bit LCG (Numerical Recipes constants).
function rng(seed) {
  let state = seed >>> 0 || 1;
  return () => {
    state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
    return state / 2 ** 32;
  };
}

// Off-screen canvas of the given size.
function mk(width, height) {
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  return canvas;
}

// ---- fonts ----
// Font files are split by script like the Google Fonts CSS API serves them:
// fonts/<file>-latin.woff2 and fonts/<file>-latin-ext.woff2, each limited to its unicode-range.
const UNICODE_RANGES = {
  'latin': 'U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD',
  'latin-ext': 'U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF',
};
function loadFont(family, file, weight, style = 'normal') {
  const faces = Object.entries(UNICODE_RANGES).map(([subset, unicodeRange]) =>
    new FontFace(family, `url(fonts/${file}-${subset}.woff2)`, { weight: String(weight), style, unicodeRange }));
  faces.forEach(face => document.fonts.add(face));
  return Promise.all(faces.map(face => face.load()));
}

// ---- Path: a stroke sampled into a dense polyline ----
// Points live in `p` as [x, y]; after done(), `cum[i]` is the arc length up to point i and `len` the total.
// Builder methods append points and return the path, so calls chain: P().M(0, 0).L(100, 0).S([...]).

// Bernstein forms of the quadratic and cubic Bezier at parameter k.
const bezier2 = (p0, c, p1, k) => { const j = 1 - k; return j * j * p0 + 2 * j * k * c + k * k * p1; };
const bezier3 = (p0, c0, c1, p1, k) => { const j = 1 - k; return j * j * j * p0 + 3 * j * j * k * c0 + 3 * j * k * k * c1 + k * k * k * p1; };
// Point between a (at knot ta) and b (at knot tb) for knot value t; one step of the Barry-Goldman pyramid.
const knotMix = (a, b, ta, tb, t) => a.map((v, i) => (tb - t) / (tb - ta) * v + (t - ta) / (tb - ta) * b[i]);
const CENTRIPETAL = 0.5;

class Path {
  constructor() { this.p = []; }

  last() { return this.p[this.p.length - 1]; }

  M(x, y) {
    this.p.push([x, y]);
    return this;
  }

  // Straight line, sampled about every 4 px unless `steps` is given.
  L(x, y, steps) {
    const [x0, y0] = this.last();
    const n = steps || Math.max(2, Math.ceil(Math.hypot(x - x0, y - y0) / 4));
    for (let i = 1; i <= n; i++) this.p.push([lerp(x0, x, i / n), lerp(y0, y, i / n)]);
    return this;
  }

  Q(cx, cy, x, y, steps = 30) {
    const [x0, y0] = this.last();
    for (let i = 1; i <= steps; i++) {
      const k = i / steps;
      this.p.push([bezier2(x0, cx, x, k), bezier2(y0, cy, y, k)]);
    }
    return this;
  }

  C(c0x, c0y, c1x, c1y, x, y, steps = 40) {
    const [x0, y0] = this.last();
    for (let i = 1; i <= steps; i++) {
      const k = i / steps;
      this.p.push([bezier3(x0, c0x, c1x, x, k), bezier3(y0, c0y, c1y, y, k)]);
    }
    return this;
  }

  // Elliptical arc from angle `from` to `to`; joins the current end point with a line first.
  A(cx, cy, rx, ry, from, to, steps) {
    const n = steps || Math.max(8, Math.ceil(Math.abs(to - from) * Math.max(rx, ry) / 4));
    for (let i = 0; i <= n; i++) {
      const ang = lerp(from, to, i / n);
      const x = cx + Math.cos(ang) * rx, y = cy + Math.sin(ang) * ry;
      if (i === 0 && this.p.length) this.L(x, y);
      else this.p.push([x, y]);
    }
    return this;
  }

  // Smooth curve through `pts` (centripetal Catmull-Rom), continuing from the current end point.
  S(pts, steps = 16) {
    const knots = this.p.length ? [this.last(), ...pts] : pts;
    if (!this.p.length) this.p.push(knots[0]);
    const last = knots.length - 1;
    const gap = (a, b) => Math.pow(Math.hypot(b[0] - a[0], b[1] - a[1]) || 1e-3, CENTRIPETAL);
    for (let i = 0; i < last; i++) {
      const q0 = knots[Math.max(0, i - 1)], q1 = knots[i], q2 = knots[i + 1], q3 = knots[Math.min(last, i + 2)];
      const k0 = 0, k1 = k0 + gap(q0, q1), k2 = k1 + gap(q1, q2), k3 = k2 + gap(q2, q3);
      for (let s = 1; s <= steps; s++) {
        const t = lerp(k1, k2, s / steps);
        const a1 = knotMix(q0, q1, k0, k1, t), a2 = knotMix(q1, q2, k1, k2, t), a3 = knotMix(q2, q3, k2, k3, t);
        const b1 = knotMix(a1, a2, k0, k2, t), b2 = knotMix(a2, a3, k1, k3, t);
        this.p.push(knotMix(b1, b2, k1, k2, t));
      }
    }
    return this;
  }

  // Hand wobble: displaces each point by two low-frequency sines of its arc length.
  jitter(amp, seed, freq = 0.012) {
    const r = rng(seed);
    const phase = [r() * 9, r() * 9, r() * 9, r() * 9];
    this.done();
    this.p = this.p.map(([x, y], i) => {
      const s = this.cum[i];
      const dx = Math.sin(s * freq + phase[0]) * 0.7 + Math.sin(s * freq * 2.3 + phase[1]) * 0.3;
      const dy = Math.sin(s * freq * 1.1 + phase[2]) * 0.7 + Math.sin(s * freq * 2.7 + phase[3]) * 0.3;
      return [x + amp * dx, y + amp * dy];
    });
    return this.done();
  }

  // Measures the polyline; call after the last builder method.
  done() {
    this.cum = [0];
    for (let i = 1; i < this.p.length; i++) {
      const [ax, ay] = this.p[i - 1], [bx, by] = this.p[i];
      this.cum.push(this.cum[i - 1] + Math.hypot(bx - ax, by - ay));
    }
    this.len = this.cum[this.cum.length - 1];
    return this;
  }

  // Position and heading at arc length s; `i` is the index of the segment's first point.
  at(s) {
    s = clamp(s, 0, this.len);
    let lo = 0, hi = this.cum.length - 1;
    while (hi - lo > 1) {
      const mid = (lo + hi) >> 1;
      if (this.cum[mid] < s) lo = mid; else hi = mid;
    }
    const a = this.p[lo], b = this.p[hi];
    const k = (s - this.cum[lo]) / ((this.cum[hi] - this.cum[lo]) || 1);
    return { x: lerp(a[0], b[0], k), y: lerp(a[1], b[1], k), ang: Math.atan2(b[1] - a[1], b[0] - a[0]), i: lo };
  }

  // Adds the stretch between arc lengths s0 and s1 to the context's current path; returns its end.
  trace(c, s0, s1) {
    if (s1 <= s0) return null;
    const from = this.at(s0), to = this.at(s1);
    c.moveTo(from.x, from.y);
    for (let i = from.i + 1; i <= to.i; i++) c.lineTo(this.p[i][0], this.p[i][1]);
    c.lineTo(to.x, to.y);
    return to;
  }

  // New path with `count` points evenly spaced along this one.
  resample(count) {
    this.done();
    const out = new Path();
    for (let i = 0; i < count; i++) {
      const q = this.at(this.len * i / (count - 1));
      out.p.push([q.x, q.y]);
    }
    return out.done();
  }
}
const P = () => new Path();
