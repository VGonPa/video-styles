# events.json → audio.wav (48 kHz stereo, 10 s)
# agitprop poster sound design, all synthesized: a marching snare/kick bed, heavy paper-and-wood slams for every
# shape that lands, a distorted brass "megaphone blast" per shouted word, whooshes for flying blocks, a tearing
# rip for the red wedge, a gear ratchet, radio beeps from the tower, a swell for the circle wipe and a final boom.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(39)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def env(n, a, r):
    t = np.arange(n) / SR; d = n / SR; return np.minimum(1, t / max(a, 1e-4)) * np.clip((d - t) / max(r, 1e-4), 0, 1)
def saw(f, d, vib=0.0):
    t = tt(d); ph = np.cumsum(f * (1 + vib * np.sin(2 * np.pi * 5.5 * t))) / SR; return 2 * (ph % 1) - 1
def kick(d=0.3, f0=110, f1=42):
    t = tt(d); f = f1 + (f0 - f1) * np.exp(-t / 0.035); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (d * 0.35))
def snare(d=0.16):
    t = tt(d); n = band(rs.standard_normal(len(t)), 1200, 9000) * np.exp(-t / 0.045)
    return n + 0.4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.03)
def slam(v):
    t = tt(0.45); body = kick(0.45, 95, 38) * (0.8 + 0.4 * v)
    slap = band(rs.standard_normal(len(t)), 300, 5000) * np.exp(-t / 0.018)
    wood = np.sin(2 * np.pi * 240 * t) * np.exp(-t / 0.04)
    return body + 0.6 * slap + 0.25 * wood
def whoosh(d, v):
    n = rs.standard_normal(int(d * SR)); u = np.linspace(0, 1, len(n))
    x = band(n, 400, 2200 + 3000 * v) * np.sin(np.pi * u) ** 2 * u; return x / (np.abs(x).max() + 1e-9)
ev = json.load(open('events.json'))
# march bed at 120 bpm: kick on the beat, snare on the off-beat, with a small roll before the wedge
for i in range(19):
    tb = 0.12 + i * 0.5
    if tb > 9.3: break
    add(kick(0.25, 90, 45), tb, 0.22)
    add(snare(), tb + 0.25, 0.08, 0.2)
for j in range(6): add(snare(0.08), 2.95 + j * 0.045, 0.04 + j * 0.01, -0.2)
for e in ev:
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'slam':
        add(slam(v), te, 0.30 + 0.35 * v, rs.uniform(-.25, .25))
    elif k == 'shout':
        d = 0.55; base = 98 if v == 0 else 131
        x = sum(saw(base * m, d, 0.012) * g for m, g in [(1, 1), (1.5, .7), (2, .55), (3, .3)])
        x = band(x, 450, 3600); x = np.tanh(x * 3.0) * env(len(x), 0.02, 0.22)
        x *= 1 + 0.35 * np.sin(2 * np.pi * 27 * tt(d))     # megaphone buzz
        add(x / (np.abs(x).max() + 1e-9), te - 0.02, 0.30 + 0.08 * v)
    elif k == 'whoosh':
        add(whoosh(0.32, v), te - 0.05, 0.10 + 0.08 * v, rs.uniform(-.4, .4))
    elif k == 'rip':
        d = e['d'] + 0.1; n = rs.standard_normal(int(d * SR))
        crackle = (rs.random(len(n)) < 0.02) * rs.standard_normal(len(n)) * 4
        x = band(n + crackle, 700, 7000) * np.linspace(0.3, 1, len(n)) * env(len(n), 0.02, 0.15)
        add(x / (np.abs(x).max() + 1e-9), te, 0.22, -0.3)
        add(whoosh(0.4, 1.0), te + e['d'] - 0.3, 0.2, 0.3)
    elif k == 'gear':
        for j in range(9):
            c = band(rs.standard_normal(int(0.03 * SR)), 1500, 6000) * np.exp(-tt(0.03) / 0.006)
            add(c, te + 0.05 + j * 0.045, 0.10, -0.5)
    elif k == 'beep':
        for j, f in enumerate([1180, 1180, 880]):
            b = np.sin(2 * np.pi * f * tt(0.06)) * env(int(0.06 * SR), 0.004, 0.02); add(b, te + j * 0.09, 0.035, 0.55)
    elif k == 'swell':
        d = e['d'] + 0.2; t = tt(d)
        x = sum(np.sin(2 * np.pi * f * t * (1 + 0.5 * t / d)) for f in (110, 165, 220)) * (t / d) ** 2 * env(len(t), 0.05, 0.1)
        add(x / 3, te, 0.16); add(whoosh(d, 0.8), te, 0.10)
    elif k == 'boom':
        t = tt(1.8); x = kick(1.8, 70, 30) + 0.3 * band(rs.standard_normal(len(t)), 60, 400) * np.exp(-t / 0.4)
        add(x, te, 0.5)
fi = int(0.02 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.2) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
