# events.json → audio.wav (48 kHz stereo, 10 s)
# ascii-art: every character that settles on the grid is a tiny digital blip (short sine ping on a pentatonic set +
# a breath of filtered noise, panned by column); the opening rain is a soft granular patter; a low fifth drone
# holds the globe, a filtered riser carries the morph, the heart beats with real lub-dub thumps, the dissolve is a
# shimmer of grains, the title lands on a warm bell chord with a bright sweep, and the ending blips step downwards.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(50)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
PENTA = [nt(m) for m in (84, 86, 88, 91, 93, 96, 98, 100)]
def blip(f):
    t = tt(0.035)
    return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.006) * np.minimum(1, t / 0.0008)
BLIPS = [blip(f) for f in PENTA]
TICKS = [norm(band(rs.standard_normal(int(0.02 * SR)), 3000, 11000)) * np.exp(-tt(0.02) / 0.0018) for _ in range(8)]
def whoosh(d, lo=150, hi=2400):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = lo + (hi - lo) * (t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * np.minimum(1, t / d * 1.15) / 1) ** 1.2 * np.minimum(1, (d - t) / 0.08)
def thump(a):
    t = tt(0.4); f = 38 + 34 * np.exp(-t / 0.05)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.11) * np.minimum(1, t / 0.003)
    s += 0.25 * norm(band(rs.standard_normal(len(t)), 60, 400)) * np.exp(-t / 0.02)
    return s * a
def bell(freq, d):
    t = tt(d); s = np.zeros_like(t)
    for h, a, dec in [(1, 1, 1.6), (2.0, .3, .8), (3.01, .12, .45), (4.2, .05, .3)]: s += a * np.sin(2 * np.pi * freq * h * t) * np.exp(-t / dec)
    return s * np.minimum(1, t / 0.006)
ev = json.load(open('events.json'))
t = np.arange(N) / SR
# drone: low fifth, swells in with the globe, darkens for the heart, opens up for the title
env = np.clip((t - 0.6) / 1.6, 0, 1) * np.clip((9.9 - t) / 1.0, 0, 1)
d1 = np.sin(2 * np.pi * nt(36) * t) + 0.5 * np.sin(2 * np.pi * nt(43) * t) + 0.18 * np.sin(2 * np.pi * nt(48) * t + 0.3 * np.sin(2 * np.pi * 0.3 * t))
d2 = np.sin(2 * np.pi * nt(33) * t) + 0.5 * np.sin(2 * np.pi * nt(40) * t) + 0.2 * np.sin(2 * np.pi * nt(45) * t)
mx = np.clip((t - 4.4) / 1.0, 0, 1) * (1 - np.clip((t - 7.6) / 0.8, 0, 1))
drone = (d1 * (1 - mx) + d2 * mx) * env
air = norm(band(rs.standard_normal(N), 200, 3000)) * 0.25 * env
L += drone * 0.028 + air * 0.012; R += np.roll(drone, 240) * 0.028 + np.roll(air, 7919) * 0.012
for e in ev:
    k, te = e['k'], e['t']
    if k == 'tk':
        for j in range(min(e['n'], 7)):
            tj = te + rs.uniform(0, 1 / 30); pan = rs.uniform(-0.8, 0.8)
            add(BLIPS[rs.integers(len(BLIPS))], tj, 0.028, pan); add(TICKS[rs.integers(8)], tj, 0.02, pan)
    elif k == 'rain':
        for j in range(260):
            tj = te + 1.7 * rs.random() ** 1.1; add(TICKS[rs.integers(8)], tj, 0.035 * rs.uniform(0.3, 1), rs.uniform(-0.9, 0.9))
    elif k == 'whoosh':
        add(whoosh(e['d'], 120, 3200), te, 0.12, -0.2)
        tr = tt(e['d']); add(np.sin(2 * np.pi * np.cumsum(220 + 440 * (tr / e['d']) ** 2) / SR) * np.sin(np.pi * tr / e['d']) ** 2, te, 0.02)
    elif k == 'beat':
        add(thump(e['a'] / 0.1), te, 0.5)
    elif k == 'dissolve':
        for j in range(320):
            tj = te + e['d'] * rs.random(); add(BLIPS[rs.integers(len(BLIPS))], tj, 0.016 * rs.uniform(0.4, 1), rs.uniform(-1, 1))
        add(whoosh(e['d'], 800, 6000), te, 0.05, 0.2)
    elif k == 'chord':
        for i, m in enumerate([60, 67, 72, 76, 79]): add(bell(nt(m), 2.6), te + i * 0.045, 0.05 if m > 62 else 0.07, [-.3, .3, -.1, .15, 0][i])
    elif k == 'sweep':
        add(whoosh(e['d'], 2000, 9000), te, 0.035, 0.0)
    elif k == 'fade':
        for i, m in enumerate([96, 93, 91, 88, 86, 84]): add(blip(nt(m)), te + i * 0.08, 0.03, -0.6 + i * 0.24)
fi = int(0.05 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', len(ev), 'events, peak', np.abs(st).max().round(3), 'rms', np.sqrt((st ** 2).mean()).round(3))
