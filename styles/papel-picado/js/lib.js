// lib.js · helpers, palette, seeded noise — all deterministic
const TAU = Math.PI * 2;
const W = 1920, H = 1080;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eOut = u => 1 - Math.pow(1 - u, 3);
const eIn = u => u * u * u;
const eInOut = u => u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
const eSine = u => 0.5 - 0.5 * Math.cos(Math.PI * u);
// damped spring settle: 0 → 1 with overshoot
const spring = (u, k = 3.2, z = 4.2) => u <= 0 ? 0 : 1 - Math.exp(-z * u) * Math.cos(k * TAU * u * 0.5);
function mulberry(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const hash = n => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
function mk(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
// smooth 1D value noise
function vnoise(x, s = 0) { const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f); return lerp(hash(i + s * 57.3), hash(i + 1 + s * 57.3), u) * 2 - 1; }

// tissue-paper colours (base, lit), plus the dusk plaza
const PAPER = [
  { n: 'pink', c: '#e8337f', l: '#ff5eaa' },
  { n: 'orange', c: '#f26a1b', l: '#ff9d3a' },
  { n: 'turq', c: '#14a9b5', l: '#3ee6ea' },
  { n: 'yellow', c: '#f5c61c', l: '#ffe84e' },
  { n: 'green', c: '#35b04a', l: '#6fe85e' },
  { n: 'purple', c: '#8e3fc0', l: '#b870f5' },
  { n: 'red', c: '#e0273a', l: '#ff5a52' },
];
const FT = 'Bungee', FC = 'Josefin Sans';
