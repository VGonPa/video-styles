# events.json → audio.wav (48 kHz stereo, 10 s)
# A santur-like struck-string arpeggio in a Shur-flavoured mode (with a quarter-flat second) opens and closes the clip,
# a reed-flute (ney-like) phrase accompanies the walk, the pen traces the rulings, brushes lay in each colour,
# the fountain bubbles, doves chirp, soft slippers tap the brick walk, blossoms open on tiny plucks, and the gilding shimmers.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(101)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
# Shur on D: D, E half-flat, F, G, A, Bb, C, D
SHUR = [62, 63.5, 65, 67, 69, 70, 72, 74, 75.5, 77, 79]

def santur(f, d=1.6, bright=0.6):
    # struck string pair (slightly detuned) with a hammer transient
    t = tt(d); out = np.zeros(len(t))
    for det in (1.0, 1.0035):
        for k in range(1, 7):
            out += np.sin(2 * np.pi * f * det * k * t) * np.exp(-t * (2.2 + k * 1.3 / bright)) / k ** 1.2
    out += band(rs.standard_normal(len(t)), 2000, 9000) * np.exp(-t / 0.004) * 0.6
    return norm(out) * np.minimum(1, t / 0.002)
def tar(f, d=1.4):
    n = int(d * SR); p = max(2, int(SR / f)); buf = rs.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]; j = (i + 1) % p; buf[i % p] = 0.5 * (buf[i % p] + buf[j]) * 0.995
    return band(out, 90, 5000) * np.minimum(1, np.arange(n) / 30)
def ney(f, d, vib=5.0):
    t = tt(d); ph = 2 * np.pi * np.cumsum(f * (1 + 0.006 * np.sin(2 * np.pi * vib * t) * np.clip(t / 0.3, 0, 1))) / SR
    tone = np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    breath = band(rs.standard_normal(len(t)), 900, 4500) * 0.35
    env = np.clip(t / 0.12, 0, 1) * np.clip((d - t) / 0.18, 0, 1)
    return (tone * 0.8 + breath) * env
def rustle(d, lo=900, hi=5000):
    t = tt(d); x = band(rs.standard_normal(len(t)), lo, hi); am = band(rs.standard_normal(len(t)), 1, 14); am = np.abs(am) / (np.abs(am).max() + 1e-9)
    return norm(x) * am * np.sin(np.pi * np.clip(t / d, 0, 1))
def pen(d):
    t = tt(d); x = band(rs.standard_normal(len(t)), 2500, 8000) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t) ** 2)
    return norm(x) * np.sin(np.pi * t / d) ** 0.7
def shimmer(d=1.2, base=1568):
    t = tt(d); out = np.zeros(len(t))
    for k, (m, dl) in enumerate([(1, 0), (1.5, 0.07), (2, 0.14), (2.52, 0.21), (3, 0.28), (4, 0.36)]):
        tk = np.clip(t - dl, 0, None); out += np.sin(2 * np.pi * base * m * tk) * np.exp(-tk * 3.5) * (t >= dl) * (0.88 ** k)
    return out * 0.5
def chirp():
    out = np.zeros(int(0.5 * SR)); o = 0
    for k in range(rs.integers(2, 4)):
        d = 0.05 + rs.uniform(0, 0.04); t = tt(d); f0 = rs.uniform(2800, 3800); f1 = f0 * rs.uniform(1.2, 1.6)
        f = f0 + (f1 - f0) * np.sin(np.pi * t / d); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 2
        i = int(o * SR); out[i:i + len(s)] += s[:len(out) - i]; o += d + rs.uniform(0.03, 0.07)
    return out
def tap(bright=False):
    t = tt(0.12); f = 160 if bright else 110
    return np.sin(2 * np.pi * (f + 60 * np.exp(-t * 40)) * t) * np.exp(-t / 0.03) + band(rs.standard_normal(len(t)), 600, 3000 if bright else 1800) * np.exp(-t / 0.012) * 0.6
def bell(f, d=1.0):
    t = tt(d); return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6)) * np.exp(-t * 4)

ev = json.load(open('events.json'))
room = norm(band(rs.standard_normal(N), 80, 600)); L += room * 0.006; R += np.roll(room, 1777) * 0.006
# fountain: bubbling water from the jet onward
jet = next(e['t'] for e in ev if e['k'] == 'jet')
w = band(rs.standard_normal(N), 400, 5000); bub = np.zeros(N); idx = rs.integers(int(jet * SR), N, 900); bub[idx] = rs.uniform(0.3, 1, len(idx)); bub = band(bub, 700, 3500)
tt_all = np.arange(N) / SR; wenv = np.clip((tt_all - jet) / 0.6, 0, 1) * (0.7 + 0.3 * np.abs(band(rs.standard_normal(N), 0.5, 6)) / 0.01 * 0.01)
water = (norm(w) * 0.6 + norm(bub)) * wenv
L += water * 0.022; R += np.roll(water, 311) * 0.02
# opening santur arpeggio
for i, m in enumerate([62, 69, 74, 72, 70, 69]): add(santur(nt(m), 1.8), 0.15 + i * 0.13, 0.12, -0.5 + i * 0.18)
# ney phrase during the walk
for m, t0, d in [(62, 3.1, 0.9), (65, 3.95, 0.55), (63.5, 4.45, 0.5), (65, 4.9, 0.45), (67, 5.3, 0.9), (65, 6.15, 0.5), (63.5, 6.6, 0.55), (62, 7.1, 1.3)]:
    add(ney(nt(m), d + 0.1), t0, 0.07, -0.15)
pops = 0
for e in ev:
    k, te = e['k'], e['t']
    if k == 'rule': add(pen(0.9), te, 0.05, -0.2)
    elif k == 'band': add(rustle(e['d'], 1500, 7000), te, 0.045, 0.2); add(shimmer(1.2, 1175), te + 0.4, 0.025, 0.0)
    elif k == 'paint': add(rustle(e['d'], 500, 3200), te, 0.05, rs.uniform(-0.5, 0.5))
    elif k == 'jet': add(rustle(0.5, 800, 6000), te, 0.05, 0.0)
    elif k == 'title':
        for i, m in enumerate([62, 65, 67, 69]): add(tar(nt(m - 12), 1.3), te + i * 0.16, 0.10, -0.1 + i * 0.07)
    elif k == 'step': add(tap(e['stone']), te, 0.10 * max(0.4, e['a']), (te - 5.2) * 0.15)
    elif k == 'chirp': add(chirp(), te, 0.035, e['pan'])
    elif k == 'pop':
        pops += 1
        if pops % 4 == 0: add(santur(nt(SHUR[rs.integers(4, len(SHUR))] + 12), 0.5, 1.0), te, 0.035, e['pan'])
    elif k == 'caption':
        for i, m in enumerate([69, 67, 65, 63.5, 62]): add(tar(nt(m - 12), 1.4), te + i * 0.15, 0.09, 0.1 - i * 0.05)
    elif k == 'gild': add(rustle(e['d'], 3000, 9000), te, 0.03, 0.0); add(shimmer(1.6, 1568), te + 0.2, 0.04, -0.3); add(shimmer(1.6, 1976), te + 0.7, 0.035, 0.3)
    elif k == 'twinkle':
        for i in range(6): add(bell(nt(SHUR[rs.integers(5, len(SHUR))] + 12), 0.9), te + i * 0.11, 0.025, rs.uniform(-0.8, 0.8))
    elif k == 'end':
        for i, m in enumerate([74, 69, 65, 62]): add(santur(nt(m), 2.2), te + i * 0.14, 0.11, 0.4 - i * 0.25)
        add(santur(nt(50), 2.4), te + 0.6, 0.12, 0.0)
fi = int(0.1 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.6
st = np.stack([L, R], 1); st = np.tanh(st * 3.5) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
