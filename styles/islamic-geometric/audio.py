# events.json → audio.wav (48 kHz stereo, 10 s)
# a compass point scratching plaster, pencil strokes for the construction lines, fine pen ticks as the
# pattern inks in (binned per 1/60 s), glazed-tile clinks as the tiles are set, an airy rise under the
# pull-back, a scribed ring, a turning whoosh, plucked-string phrases in a Hijaz-flavoured mode on D,
# a glassy shimmer for the raking light and a closing chord over a soft low drone.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(102)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def scratch(d, lo=1800, hi=7000, grain=38):
    t = tt(d); x = norm(band(rs.standard_normal(len(t)), lo, hi))
    am = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * grain * t + 3 * np.sin(2 * np.pi * 3 * t)))
    return x * am * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.6
def tick():
    t = tt(0.02); return norm(band(rs.standard_normal(len(t)), 2500, 9000)) * np.exp(-t / 0.0018)
TICKS = [tick() for _ in range(16)]
def clink():
    t = tt(0.35); f0 = 2300 + 1800 * rs.random()
    s = sum(a * np.sin(2 * np.pi * f0 * h * t + rs.random() * 6) * np.exp(-t / (dcy / h)) for h, a, dcy in [(1, 1, .06), (2.32, .5, .05), (3.9, .25, .03)])
    n = norm(band(rs.standard_normal(len(t)), 3000, 11000)) * np.exp(-t / 0.0015)
    th = np.sin(2 * np.pi * (320 + 120 * rs.random()) * t) * np.exp(-t / 0.008)
    return 0.45 * s + 0.35 * n + 0.25 * th
CLINKS = [clink() for _ in range(20)]
def pluck(f, d=2.0, bright=0.6):
    n = int(d * SR); P = int(SR / f); buf = rs.uniform(-1, 1, P) * np.hanning(P) ** bright; out = np.zeros(n)
    for i in range(n): out[i] = buf[i % P]; buf[i % P] = 0.5 * (buf[i % P] + buf[(i + 1) % P]) * 0.996
    return out * np.minimum(1, np.arange(n) / 60)
def whoosh(d, lo=250, hi=1800):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = lo + hi * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 2
def bell(f, d=1.4):
    t = tt(d); return sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (0.45 / h)) for h, a in [(1, 1), (2.76, .35), (5.4, .15)]) * np.minimum(1, t / 0.002)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR
# low drone on D with a slow swell once the tiles glaze
dr = sum(a * np.sin(2 * np.pi * nt(m) * t + ph) for m, a, ph in [(38, 1, 0), (45, .5, 1), (50, .3, 2), (57, .12, .5)]) * (1 + 0.12 * np.sin(2 * np.pi * 0.25 * t))
L += dr * np.clip((t - 2.6) / 3.0, 0, 1) * 0.02; R += dr * np.clip((t - 2.6) / 3.0, 0, 1) * 0.02
room = norm(band(rs.standard_normal(N), 200, 3000)); L += room * 0.004; R += np.roll(room, 777) * 0.004
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'compass': add(scratch(e['d'], 1500, 6000, 30), te, 0.05, 0.1)
    elif k == 'line': add(scratch(0.3, 2500, 8000, 55), te, 0.035, rs.uniform(-.4, .4))
    elif k == 'ink':
        c = e['v']; n = int(min(c, 4)); g = 0.05 * min(1.0, np.sqrt(c) / 2.5) / np.sqrt(max(1, n))
        for j in range(n): add(TICKS[rs.integers(16)], te + rs.uniform(0, 1 / 60), g, rs.uniform(-.6, .6))
    elif k == 'tile':
        c = e['v']; n = int(min(c, 4)); g = 0.075 * min(1.0, np.sqrt(c) / 3) / np.sqrt(max(1, n))
        for j in range(n): add(CLINKS[rs.integers(20)], te + rs.uniform(0, 1 / 60), g * (0.7 + 0.6 * rs.random()), rs.uniform(-.6, .6))
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.08)
    elif k == 'ring': add(scratch(e['d'], 1200, 5000, 24), te, 0.04, 0.3)
    elif k == 'spin': add(whoosh(e['d'], 400, 2600), te, 0.06, -0.2)
    elif k == 'phrase':
        for i, m in enumerate([62, 63, 66, 67, 69]): add(pluck(nt(m)), te + i * 0.17, 0.13, -0.3 + 0.15 * i)
    elif k == 'shimmer':
        for i in range(12): add(bell(nt(rs.choice([86, 87, 90, 91, 93, 98]))), te + e['d'] * i / 12 + rs.uniform(0, 0.06), 0.022, -0.8 + 1.6 * i / 11)
    elif k == 'chord':
        for i, m in enumerate([50, 57, 62, 66, 69, 74]): add(pluck(nt(m), 1.5, 0.35), te + i * 0.05, 0.12, -0.4 + 0.16 * i)
fi = int(0.2 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 3.0) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
