# events.json → audio.wav (48 kHz stereo, 10 s)
# lightbox click and hum, sand sprinkle and pour hiss (granular crackle), fingertip scratches on glass,
# dab taps, wing flutters, a soft rush as the head pours in, a palm swish, a warm pad with a few bell notes.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(19)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def grains(d, rate, lo=2500, hi=11000):
    # sparse clicks of falling grains, each a tiny filtered impulse
    n = int(d * SR); x = np.zeros(n); k = rs.poisson(rate * d)
    idx = rs.integers(0, n, k); x[idx] = rs.uniform(-1, 1, k) * rs.uniform(0.2, 1, k)
    return norm(band(x, lo, hi))
def hiss(d, lo, hi, att=0.15, rel=0.3):
    t = tt(d); x = norm(band(rs.standard_normal(len(t)), lo, hi))
    am = 0.7 + 0.3 * norm(band(rs.standard_normal(len(t)), 2, 12))
    return x * am * np.minimum(1, t / att) * np.minimum(1, (d - t) / rel)
def scratch(d, v=1.0):
    t = tt(d); x = norm(band(rs.standard_normal(len(t)), 700, 3200))
    am = np.abs(norm(band(rs.standard_normal(len(t)), 20, 90))) ** 0.6
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.4
    return x * am * env * v
def tap():
    t = tt(0.09); return norm(band(rs.standard_normal(len(t)), 300, 2500)) * np.exp(-t / 0.012) + 0.4 * np.sin(2 * np.pi * 180 * t) * np.exp(-t / 0.02)
def flutter():
    out = np.zeros(int(0.32 * SR))
    for i in range(4):
        t = tt(0.05); b = norm(band(rs.standard_normal(len(t)), 250, 1800)) * np.sin(np.pi * t / 0.05)
        j = int((i * 0.07 + rs.uniform(0, 0.01)) * SR); out[j:j + len(b)] += b * (1 - i * 0.18)
    return out
def swish(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 300 + 3200 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.2
def tone(freq, d, att=0.4, rel=1.0, harm=((1, 1), (2, .25), (3, .08))):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in harm)
    return s * np.minimum(1, t / att) * np.minimum(1, (d - t) / rel)
def bell(freq, d=2.2):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) * np.exp(-t / (0.9 / h ** 0.7)) for h, a in [(1, 1), (2.01, .35), (3.02, .12), (4.17, .05)])
    return s * np.minimum(1, t / 0.004)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR
# lightbox hum, room tone and a slow pad (D, modal) that opens up toward the face
on = np.clip(t / 0.5, 0, 1)
hum = (np.sin(2 * np.pi * 100 * t) + .3 * np.sin(2 * np.pi * 200 * t)) * on
L += hum * 0.006; R += hum * 0.006
room = norm(band(rs.standard_normal(N), 150, 2500)); L += room * .004; R += np.roll(room, 911) * .004
for m, g, p, t0, d in [(50, .05, -.3, 0.2, 9.4), (57, .035, .3, 0.4, 9.2), (62, .022, 0, 2.2, 7.4), (66, .016, -.2, 5.4, 4.2)]:
    s = tone(nt(m), d, 1.6, 1.4) * (1 + .12 * np.sin(2 * np.pi * .3 * tt(d))); add(s, t0, g, p)
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']; d = e.get('d', 0.3); v = e.get('v', 1.0)
    if k == 'light':
        c = tt(0.05); add(norm(band(rs.standard_normal(len(c)), 1000, 6000)) * np.exp(-c / 0.006), te, 0.12)
    elif k == 'sprinkle':
        add(grains(d, 2600) * np.sin(np.pi * tt(d) / d) ** 0.5, te, 0.1, -0.4); add(hiss(d, 4000, 12000), te, 0.03, -0.2)
    elif k == 'pour':
        pan = np.linspace(-0.7, 0.7, 8)
        for i in range(8): add(hiss(d / 8 + 0.12, 1200, 9000, 0.05, 0.08), te + i * d / 8, 0.06, pan[i])
        add(grains(d, 5000, 1500, 9000) * np.minimum(1, (d - tt(d)) / 0.3), te, 0.12)
        add(hiss(d, 80, 400), te, 0.05)
    elif k == 'carve': add(scratch(max(d, 0.08), v), te, 0.07, rs.uniform(-.4, .1))
    elif k == 'dab': add(tap(), te, 0.1, rs.uniform(-.4, 0)); add(grains(0.12, 300), te, 0.05)
    elif k == 'flap': add(flutter(), te, 0.05, rs.uniform(-.3, .5))
    elif k == 'settle': add(tap(), te, 0.03, 0.3)
    elif k == 'whoosh': add(swish(d + 0.3), te - 0.1, 0.12, 0.3); add(grains(d, 1800), te, 0.06, 0.3)
    elif k == 'write':
        n = int(d / 0.11)
        for i in range(n): add(scratch(0.09 + 0.04 * rs.random(), 0.8), te + i * d / n, 0.08, -0.4)
    elif k == 'wipe': add(swish(d + 0.2), te, 0.3, 0); add(grains(d, 4000, 1500, 9000) * np.linspace(0.3, 1, int(d * SR)), te, 0.12)
    elif k == 'bell': add(bell(nt(e['n'] + 12)), te, 0.05, rs.uniform(-.3, .3))
    elif k == 'chord':
        for i, m in enumerate([62, 66, 69, 74, 78]): add(tone(nt(m), 1.5, 0.1 + i * .04, 0.9), te + i * 0.05, 0.022)
        add(tone(nt(38), 1.5, .15, 1.0), te, 0.05)
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.0) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
