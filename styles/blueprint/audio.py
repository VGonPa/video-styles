# events.json → audio.wav (48 kHz stereo, 10 s)
# drafting-pen scratches, fine-liner strokes, hatching rasps, arrowhead ticks, soft stencil keys,
# camera whoosh, metal parts sliding apart, balloon taps, quiet room tone + cool pad, closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(7)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def scratch(d, lo=2500, hi=9000, grain=90):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), lo, hi))
    am = 0.6 + 0.4 * norm(np.abs(band(rs.standard_normal(len(t)), 10, grain)))
    env = np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.05).clip(0)
    return n * am * env
def tick():
    t = tt(0.03); return norm(band(rs.standard_normal(len(t)), 3000, 10000)) * np.exp(-t / 0.003)
def key():
    t = tt(0.05); n = norm(band(rs.standard_normal(len(t)), 1500, 6000)) * np.exp(-t / 0.004)
    return 0.6 * n + 0.4 * np.sin(2 * np.pi * (220 + 60 * rs.random()) * t) * np.exp(-t / 0.01)
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    a = np.exp(-2 * np.pi * (200 + 2200 * np.sin(np.pi * t / d) ** 2) / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
def slide(d):
    t = tt(d); s = norm(band(rs.standard_normal(len(t)), 600, 3500)) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    ring = np.sin(2 * np.pi * 1850 * t) * np.exp(-np.maximum(t - d * 0.9, 0) / 0.08) * (t > d * 0.9)
    return s + 0.25 * ring
def tap(f):
    t = tt(0.2); s = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2.7 * t)) * np.exp(-t / 0.04)
    c = tick(); s[:len(c)] += 0.3 * c; return s
def tone(freq, d, att=0.4, rel=1.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in [(1, 1), (2, .25), (3, .08)])
    return s * np.minimum(1, t / att) * np.minimum(1, (d - t) / rel)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
# bed: room tone + soft D-major-ish pad
t = np.arange(N) / SR
room = norm(band(rs.standard_normal(N), 150, 2500)); L += room * .005; R += np.roll(room, 911) * .005
for m, g, p in [(38, .045, -.3), (45, .03, .3), (54, .018, 0), (57, .014, .2)]:
    s = tone(nt(m), 9.7, 1.8, 1.4) * (1 + .12 * np.sin(2 * np.pi * .2 * np.arange(int(9.7 * SR)) / SR)); add(s, 0.2, g, p)
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'scribe': add(scratch(e['d']), te, 0.07, rs.uniform(-.3, .3))
    elif k == 'pen': add(scratch(e['d'], 4000, 11000, 40), te, 0.035, rs.uniform(-.4, .4))
    elif k == 'hatch':
        d = e['d']; n = max(3, int(d * 22))
        for i in range(n): add(scratch(0.035, 3000, 9000), te + d * i / n, 0.05, rs.uniform(-.3, .3))
    elif k == 'tick': add(tick(), te, 0.12, rs.uniform(-.3, .3))
    elif k == 'key': add(key(), te + rs.uniform(0, .01), 0.1 * (0.8 + .4 * rs.random()), rs.uniform(-.25, .25))
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.18)
    elif k == 'slide': add(slide(e['d']), te, 0.05 + 0.07 * e.get('v', 1), rs.uniform(-.4, .4))
    elif k == 'pop': add(tap(nt(79 + [0, 2, 4, 7, 9, 12, 14, 16][int(e['v']) % 8])), te, 0.12, -0.5 + e['v'] / 7)
    elif k == 'chord':
        for i, m in enumerate([62, 66, 69, 74, 78]): add(tone(nt(m), 1.6, 0.06 + i * .03, 1.0), te + i * 0.05, 0.03)
        add(tone(nt(38), 1.6, .1, 1.1), te, 0.06)
fi = int(0.25 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.tanh(np.stack([L, R], 1) * 1.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
