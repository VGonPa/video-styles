# events.json → audio.wav (48 kHz stereo, 10 s)
# A soft tanpura-like drone (Sa–Pa with a buzzing bridge) under plucked-string phrases in a pentatonic
# (Bhupali-like) scale; the nib scratches every double outline, brushes lay in the colour, water laps in the pond,
# small wooden taps and plucks mark leaves, blossoms and fillers, wings flutter, parrots chirp as they land,
# the sun's smile gets a little bell run and the clip resolves on a low pluck.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(105)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i); pan = float(np.clip(pan, -1, 1))
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
SA = 62   # D
SCALE = [0, 2, 4, 7, 9, 12, 14, 16, 19, 21, 24]   # Sa Re Ga Pa Dha (major pentatonic)
def deg(i, o=0): return SA + SCALE[i % len(SCALE)] + 12 * o

def pluck(f, d=1.2, bright=0.5):
    n = int(d * SR); p = max(2, int(SR / f)); buf = rs.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]; j = (i + 1) % p; buf[i % p] = (0.5 + bright * 0.004) * (buf[i % p] + buf[j]) * 0.996
    # sympathetic shimmer
    t = np.arange(n) / SR; out += 0.15 * np.sin(2 * np.pi * f * 2.003 * t) * np.exp(-t * 2.5)
    return band(out, 80, 7000) * np.minimum(1, np.arange(n) / 25)
def tanpura(f, d):
    t = tt(d); out = np.zeros(len(t))
    for k in range(1, 14):
        out += np.sin(2 * np.pi * f * k * t + rs.uniform(0, 6)) * (1 / k ** 0.9) * (1 + 0.5 * np.sin(2 * np.pi * (0.3 + 0.07 * k) * t + k))
    return norm(out)
def rustle(d, lo=700, hi=4500):
    t = tt(d); x = band(rs.standard_normal(len(t)), lo, hi); am = np.abs(band(rs.standard_normal(len(t)), 1, 16)); am /= am.max() + 1e-9
    return norm(x) * am * np.sin(np.pi * np.clip(t / d, 0, 1))
def nib(d):
    t = tt(d); x = band(rs.standard_normal(len(t)), 2200, 8000) * (0.55 + 0.45 * np.sin(2 * np.pi * 6 * t + rs.uniform(0, 6)) ** 2)
    return norm(x) * np.sin(np.pi * t / d) ** 0.6
def tok(f=700):
    t = tt(0.09); return np.sin(2 * np.pi * f * t * (1 + 0.4 * np.exp(-t * 60))) * np.exp(-t / 0.018) + band(rs.standard_normal(len(t)), 1500, 5000) * np.exp(-t / 0.004) * 0.4
def bell(f, d=1.2):
    t = tt(d); return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 5) + 0.2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 9)) * np.exp(-t * 3.2)
def chirp():
    out = np.zeros(int(0.45 * SR)); o = 0
    for k in range(rs.integers(2, 4)):
        d = 0.045 + rs.uniform(0, 0.04); t = tt(d); f0 = rs.uniform(2600, 3600); f1 = f0 * rs.uniform(1.25, 1.7)
        f = f0 + (f1 - f0) * np.sin(np.pi * t / d); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 2
        i = int(o * SR); out[i:i + len(s)] += s[:len(out) - i]; o += d + rs.uniform(0.03, 0.06)
    return out
def flutter(d):
    t = tt(d); x = band(rs.standard_normal(len(t)), 300, 2500); am = np.clip(np.sin(2 * np.pi * 11 * t), 0, 1) ** 3
    return norm(x) * am * np.sin(np.pi * t / d)
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); out = np.zeros(len(t)); segs = 12
    for s in range(segs):
        a, b = int(s * len(t) / segs), int((s + 1) * len(t) / segs); fc = 300 + 1500 * np.sin(np.pi * (s + 0.5) / segs)
        out[a:b] = band(x, fc * 0.5, fc * 1.6)[a:b]
    return out * np.sin(np.pi * t / d) ** 1.5

ev = json.load(open('events.json'))
# drone: Sa and Pa, entering softly and staying under everything
dr = tanpura(nt(SA - 24), DUR) * 0.6 + tanpura(nt(SA - 17), DUR) * 0.4
env = np.clip(np.arange(N) / SR / 1.2, 0, 1)
L += dr * env * 0.03; R += np.roll(dr, 997) * env * 0.03
# pond water from the first waves onward
wt = next(e['t'] for e in ev if e['k'] == 'water')
w = band(rs.standard_normal(N), 300, 3500); bub = np.zeros(N); idx = rs.integers(int(wt * SR), N, 500); bub[idx] = rs.uniform(0.3, 1, len(idx)); bub = band(bub, 600, 2600)
ta = np.arange(N) / SR; wenv = np.clip((ta - wt) / 0.8, 0, 1) * (1 - 0.45 * np.clip((ta - 3.0) / 1.2, 0, 1))
water = (norm(w) * 0.4 + norm(bub)) * wenv
L += water * 0.016; R += np.roll(water, 411) * 0.016
# opening phrase and the growing-tree phrase
for i, (d, t0) in enumerate([(0, 0.05), (2, 0.3), (3, 0.55), (4, 0.8), (3, 1.2), (2, 1.45)]): add(pluck(nt(deg(d, 0)), 1.5), t0, 0.16, -0.4 + i * 0.12)
for i, (d, t0) in enumerate([(3, 2.9), (4, 3.2), (5, 3.5), (6, 3.8), (7, 4.15), (6, 4.5), (5, 4.8), (4, 5.2)]): add(pluck(nt(deg(d, 0)), 1.4), t0, 0.12, 0.3 - i * 0.08)
pops = 0; ticks = 0
for e in ev:
    k, te = e['k'], e['t']; pan = e.get('pan', 0.0)
    if k == 'pen': add(nib(min(1.6, e['d'])), te, 0.045, rs.uniform(-0.3, 0.3))
    elif k == 'brush': add(rustle(e['d'], 500, 3000), te, 0.06, rs.uniform(-0.4, 0.4))
    elif k == 'hatch': add(nib(e['d']) * 0.8, te, 0.035, rs.uniform(-0.4, 0.4))
    elif k == 'plip': add(tok(1100), te, 0.05, 0.0)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.08, 0.0)
    elif k == 'grow': add(rustle(e['d'], 250, 1800), te, 0.03, rs.uniform(-0.5, 0.5))
    elif k == 'pop':
        pops += 1
        if pops % 3 == 0: add(tok(rs.uniform(600, 900)), te, 0.035, pan)
    elif k == 'bloom': add(pluck(nt(deg(int(rs.integers(5, 10)), 0)), 0.5, 1.0), te, 0.05, pan)
    elif k == 'rays':
        for i in range(6): add(tok(900 + i * 80), te + i * e['d'] / 6, 0.03, rs.uniform(-0.5, 0.5))
    elif k == 'dots':
        for i in range(8): add(tok(1400 + rs.uniform(-100, 200)), te + i * e['d'] / 8, 0.02, rs.uniform(-0.3, 0.3))
    elif k == 'flap': add(flutter(e['d']), te, 0.05, pan)
    elif k == 'land': add(chirp(), te, 0.05, pan); add(tok(500), te, 0.03, pan)
    elif k == 'tick':
        ticks += 1
        if ticks % 5 == 0: add(tok(rs.uniform(1200, 1800)), te, 0.018, pan)
    elif k == 'title':
        for i, d in enumerate([0, 2, 4, 5, 7]): add(pluck(nt(deg(d, 0)), 1.3), te + i * 0.12, 0.11, -0.2 + i * 0.1)
    elif k == 'smile':
        for i, d in enumerate([5, 7, 9]): add(bell(nt(deg(d, 1)), 1.2), te + i * 0.1, 0.035, -0.6)
    elif k == 'wake': add(bell(nt(deg(4, 1)), 1.4), te, 0.03, 0.6)
    elif k == 'peacock': add(chirp(), te, 0.03, -0.6); add(chirp(), te + 0.2, 0.03, 0.6)
    elif k == 'end':
        for i, d in enumerate([7, 4, 3, 2, 0]): add(pluck(nt(deg(d, 0)), 2.0), te + i * 0.16, 0.13, 0.3 - i * 0.15)
        add(pluck(nt(SA - 12), 2.4), te + 0.85, 0.16, 0.0); add(bell(nt(deg(5, 1)), 1.6), te + 0.85, 0.03, 0.0)
fi = int(0.05 * SR); fo = int(1.0 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.6
st = np.stack([L, R], 1); st = np.tanh(st * 4.2) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
