# events.json → audio.wav (48 kHz stereo, 10 s)
# calm liquid sound design: a warm Dmaj9 pad bed with air, water "plips" for drops and melting letters,
# a soft thump + swell for each impact/bloom, gooey low "bloops" as blobs merge, a breath swell for
# "Breathe in.", a long wash for the flood, a warm bell chord for the sphere and an exhale as it dissolves.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(31)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def lp_sweep(x, fc):  # one-pole low-pass with a time-varying cutoff
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); p = 0.0
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y
def plip(f=1.0):  # water drop: sine whose pitch jumps up fast
    t = tt(0.16); fr = 700 * f * (1 + 1.3 * (1 - np.exp(-t * 90))); ph = 2 * np.pi * np.cumsum(fr) / SR
    return np.sin(ph) * np.exp(-t / 0.045) * np.minimum(1, t / 0.002)
def thump():
    t = tt(0.6); return np.sin(2 * np.pi * (60 + 90 * np.exp(-t * 25)) * t) * np.exp(-t / 0.12) * np.minimum(1, t / 0.004)
def bloop(f=1.0):
    t = tt(0.35); fr = f * (170 + 260 * np.exp(-t * 16)); ph = 2 * np.pi * np.cumsum(fr) / SR
    return (np.sin(ph) + 0.25 * np.sin(2 * ph)) * np.exp(-t / 0.09) * np.minimum(1, t / 0.01)
def swell(d, lo=200, hi=2400, shape=1.4, rev=False):
    t = tt(d); env = np.sin(np.pi * t / d) ** shape
    if rev: env = np.exp(-t / (d * 0.35)) * np.minimum(1, t / 0.08)
    x = rs.standard_normal(len(t)); y = lp_sweep(x, lo + (hi - lo) * env)
    return norm(y) * env
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def bell(f, d=2.5, dec=0.8):
    t = tt(d); s = np.zeros_like(t)
    for h, a, k in [(1, 1, 1), (2.0, .25, 1.8), (3.0, .08, 2.6), (4.2, .04, 3.5)]:
        s += a * np.sin(2 * np.pi * f * h * t + h) * np.exp(-t * k / dec)
    return s * np.minimum(1, t / 0.02)
def pad(freq, d, att, rel):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t + h + 0.3 * np.sin(2 * np.pi * 0.2 * t)) for h, a in [(1, 1), (2, .14), (3, .04)])
    s *= 1 + 0.18 * np.sin(2 * np.pi * 0.25 * t)
    return s * np.minimum(1, t / att) * np.minimum(1, np.maximum(d - t, 0) / rel)
def shimmer():
    d = 1.4; t = tt(d); s = np.zeros_like(t)
    for m in [81, 85, 88, 90, 93]:
        t0 = rs.uniform(0, 0.5); k = int(t0 * SR); tl = t[:len(t) - k]
        s[k:] += np.sin(2 * np.pi * nt(m) * tl) * np.exp(-tl / 0.5) * np.minimum(1, tl / 0.03)
    return s
# bed: warm Dmaj9 pad (enters after the first drop blooms) + airy noise
for m, g, p in [(38, .05, -.1), (45, .035, .2), (54, .022, -.3), (61, .016, .3), (64, .014, 0)]:
    add(pad(nt(m), 8.9, 1.6, 1.4), 0.95, g, p)
air = norm(band(rs.standard_normal(N), 1500, 8000)); tA = np.arange(N) / SR
L += air * .005 * np.clip(tA / 1.2, 0, 1); R += np.roll(air, 1733) * .005 * np.clip(tA / 1.2, 0, 1)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'plip': add(plip(e['f']), te, 0.16, rs.uniform(-.2, .2))
    elif k == 'drop': add(thump(), te, 0.4 * v); add(plip(0.8), te, 0.14 * v); add(bloop(1.4), te + .05, 0.08 * v, .2)
    elif k == 'bloom': add(swell(e['d'], 150, 1800, 1.8), te, 0.12)
    elif k == 'flow': add(swell(e['d'], 200, 1500, 1.5), te, 0.08 * v, rs.uniform(-.3, .3))
    elif k == 'goo': add(bloop(e['f']), te, 0.22, rs.uniform(-.3, .3))
    elif k == 'shimmer': add(shimmer(), te, 0.03, .2)
    elif k == 'breath': add(swell(e['d'], 500, 3000, 2.2), te, 0.07)
    elif k == 'flood': add(swell(e['d'], 120, 2200, 1.3), te, 0.14, .3)
    elif k == 'drip': add(plip(e['f'] * 1.2), te, 0.07, (e['f'] - 1.3) * .8)
    elif k == 'swell': add(swell(e['d'], 300, 1200), te, 0.04 * v)
    elif k == 'chord':
        for i, m in enumerate([62, 66, 69, 73, 76]): add(bell(nt(m), 2.6, 0.9), te + i * 0.07, 0.045, (i - 2) * .15)
        add(pad(nt(50), 1.6, .3, 1.0), te, 0.05)
    elif k == 'exhale': add(swell(e['d'], 400, 2000, 1.0, rev=True), te, 0.08)
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.8 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
