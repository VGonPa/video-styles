# events.json → audio.wav (48 kHz stereo, 10 s)
# stone tesserae clicking onto the mortar bed (binned per 1/60 s), Karplus-Strong lyre phrases,
# an airy rise under the camera move, water swishes for the dolphins, glass-bell shimmer for the
# light sweep, a quiet fountain courtyard bed and a closing strummed chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(93)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def click(k):
    t = tt(0.045); f0 = 1900 + 1500 * rs.random()
    n = norm(band(rs.standard_normal(len(t)), 1500, 9000)) * np.exp(-t / 0.0022)
    ping = np.sin(2 * np.pi * f0 * t + rs.random() * 6) * np.exp(-t / (0.006 + 0.008 * rs.random()))
    thud = np.sin(2 * np.pi * (180 + 90 * rs.random()) * t) * np.exp(-t / 0.01)
    return 0.7 * n + 0.35 * ping + 0.3 * thud
CLICKS = [click(k) for k in range(24)]
def pluck(f, d=2.2, bright=0.5):
    n = int(d * SR); P = int(SR / f); buf = rs.uniform(-1, 1, P) * np.hanning(P) ** bright; out = np.zeros(n)
    for i in range(n): out[i] = buf[i % P]; buf[i % P] = 0.5 * (buf[i % P] + buf[(i + 1) % P]) * 0.9965
    return out * np.minimum(1, np.arange(n) / 80)
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 250 + 1800 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 2
def swish():
    t = tt(0.9); x = band(rs.standard_normal(len(t)), 400, 3500)
    env = np.sin(np.pi * np.clip(t / 0.9, 0, 1)) ** 1.5 * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t))
    bub = sum(np.sin(2 * np.pi * (500 + 900 * rs.random()) * (1 + 3 * (t - s0).clip(0)) * t) * np.exp(-((t - s0).clip(0)) / 0.02) * (t > s0) for s0 in rs.uniform(0.1, 0.7, 6))
    return norm(x) * env + 0.15 * bub
def bell(f, d=1.6):
    t = tt(d); return sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (0.5 / h)) for h, a in [(1, 1), (2.76, .4), (5.4, .2)]) * np.minimum(1, t / 0.002)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR
# courtyard bed: fountain trickle + warm low drone (D)
fount = band(rs.standard_normal(N), 900, 6000); am = np.abs(band(rs.standard_normal(N), 3, 25)); am = am / am.max()
fount = norm(fount) * (0.4 + 0.6 * am); L += fount * 0.018; R += np.roll(fount, 911) * 0.018
dr = (np.sin(2 * np.pi * nt(38) * t) + 0.5 * np.sin(2 * np.pi * nt(45) * t) + 0.25 * np.sin(2 * np.pi * nt(50) * t)) * (1 + 0.1 * np.sin(2 * np.pi * 0.3 * t))
drenv = np.clip((t - 1.5) / 3.0, 0, 1) * 0.022
L += dr * drenv; R += dr * drenv
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'tick':
        c = e['v']; n = int(min(c, 5)); g = 0.16 * min(1.0, np.sqrt(c) / 3) / np.sqrt(max(1, n)) * (1.0 if c < 40 else 0.8)
        for j in range(n): add(CLICKS[rs.integers(24)], te + rs.uniform(0, 1 / 60), g * (0.7 + 0.6 * rs.random()), rs.uniform(-.5, .5))
    elif k == 'lyre':
        notes = [62, 65, 69, 74] if e['v'] == 0 else [64, 67, 71, 76, 74]
        for i, m in enumerate(notes): add(pluck(nt(m)), te + i * 0.16, 0.16, -0.3 + 0.15 * i)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.09)
    elif k == 'swish': add(swish(), te, 0.07, rs.uniform(-.6, .6))
    elif k == 'glint':
        for i in range(14):
            add(bell(nt(rs.choice([86, 89, 91, 93, 96, 98]))), te + e['d'] * i / 14 + rs.uniform(0, 0.08), 0.03 * (0.6 + 0.4 * rs.random()), -0.8 + 1.6 * i / 13)
    elif k == 'chord':
        for i, m in enumerate([50, 57, 62, 65, 69, 74]): add(pluck(nt(m), 1.4, 0.3), te + i * 0.05, 0.14, -0.4 + 0.16 * i)
fi = int(0.3 * SR); fo = int(0.8 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 3.2) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
