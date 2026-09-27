# events.json → audio.wav (48 kHz stereo, 10 s)
# soft UI sounds: glass drop "plink", airy whooshes, light taps, a toggle click, a liquid "bloop" merge,
# bell-like glass chimes, letter ticks, a shimmer for each light sweep, a soft pad bed and a closing glass chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(22)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def bell(f, d=1.2, dec=0.35):
    t = tt(d); s = np.zeros_like(t)
    for h, a, k in [(1, 1, 1), (2.0, .35, 1.6), (2.76, .22, 2.4), (4.07, .10, 3.4), (5.4, .05, 4.5)]:
        s += a * np.sin(2 * np.pi * f * h * t + h) * np.exp(-t * k / dec)
    return s * np.minimum(1, t / 0.003)
def tap(f):
    t = tt(0.12); body = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.018)
    click = band(rs.standard_normal(len(t)), 3000, 12000) * np.exp(-t / 0.0015)
    return 0.8 * body + 0.25 * norm(click)
def tick():
    t = tt(0.04); return norm(band(rs.standard_normal(len(t)), 4000, 14000)) * np.exp(-t / 0.003) * 0.6 + np.sin(2 * np.pi * 2600 * t) * np.exp(-t / 0.006) * 0.4
def whoosh(d, rev=False):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    env = np.sin(np.pi * t / d) ** 1.6
    if rev: env = (t / d) ** 2.2 * np.exp(-np.maximum(t - d * .9, 0) * 60)
    fc = 250 + 3200 * env
    a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * env
def bloop():
    t = tt(0.32); f = 260 + 700 * np.exp(-t * 22); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.07) * np.minimum(1, t / 0.004)
def click():
    t = tt(0.08)
    c = lambda: norm(band(rs.standard_normal(len(t)), 1500, 9000)) * np.exp(-t / 0.002) + 0.5 * np.sin(2 * np.pi * 1400 * t) * np.exp(-t / 0.01)
    s = c(); s2 = np.zeros_like(s); k = int(0.045 * SR); s2[k:] = c()[:len(s) - k] * 0.6
    return s + s2
def shimmer():
    d = 1.0; t = tt(d); s = np.zeros_like(t)
    for i in range(14):
        f = 2600 + 3800 * rs.random(); t0 = rs.uniform(0, 0.6); k = int(t0 * SR)
        g = np.zeros_like(t); tl = t[:len(t) - k]; g[k:] = np.sin(2 * np.pi * f * tl) * np.exp(-tl / 0.12)
        s += g * rs.uniform(.3, 1)
    return s * np.sin(np.pi * t / d) ** .5
def drop():
    t = tt(0.9); thump = np.sin(2 * np.pi * (90 + 120 * np.exp(-t * 30)) * t) * np.exp(-t / 0.06)
    return 0.6 * thump + bell(1760, 0.9, 0.22) * 0.5
def rise(d):
    t = tt(d); f = 520 * 2 ** (t / d * 0.6); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + .3 * np.sin(2 * ph)) * np.sin(np.pi * t / d) ** 2
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def pad(freq, d, att, rel):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t + h) for h, a in [(1, 1), (2, .18), (3, .06)])
    s *= 1 + 0.2 * np.sin(2 * np.pi * 0.3 * t)
    return s * np.minimum(1, t / att) * np.minimum(1, (d - t) / rel)
# bed: soft Cmaj9 pad + airy noise
for m, g, p in [(48, .05, -.2), (55, .035, .25), (59, .022, -.3), (62, .018, .3), (64, .015, 0)]:
    add(pad(nt(m), 9.8, 1.4, 1.5), 0.1, g, p)
air = norm(band(rs.standard_normal(N), 2000, 9000)); tA = np.arange(N) / SR
L += air * .004 * np.clip(tA / 1.5, 0, 1); R += np.roll(air, 999) * .004 * np.clip(tA / 1.5, 0, 1)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'drop': add(drop(), te, 0.35)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.13 * v, rs.uniform(-.2, .2))
    elif k == 'swish': add(whoosh(0.45), te, 0.12, -.3); add(whoosh(0.4), te + .08, 0.09, .35)
    elif k == 'shimmer': add(shimmer(), te, 0.035, .2)
    elif k == 'tap': add(tap(e['f']), te, 0.2, (e['f'] - 1000) / 900)
    elif k == 'tick': add(tick(), te, 0.035 * v, rs.uniform(-.25, .25))
    elif k == 'rise': add(rise(e['d']), te, 0.025, -.4)
    elif k == 'click': add(click(), te, 0.22, .3)
    elif k == 'chime': add(bell(e['f'], 1.6, 0.45), te, 0.07, rs.uniform(-.2, .2))
    elif k == 'bloop': add(bloop(), te, 0.3, .25)
    elif k == 'suck': add(whoosh(0.4, rev=True), te - .1, 0.16)
    elif k == 'chord':
        for i, m in enumerate([72, 76, 79, 83, 86]): add(bell(nt(m), 2.6, 0.9), te + i * 0.05, 0.05, (i - 2) * .15)
        add(pad(nt(36), 1.9, .05, 1.2), te, 0.07)
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
