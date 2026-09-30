# events.json → audio.wav (48 kHz stereo, 9.5 s)
# wooden knocks and blocks on a 120 bpm pulse (soft kick + shaker); the pulse drops out while
# "ready" hesitates (thin nervous ticks, trembling), returns with the shove; whooshes, rubber stretch, pop, closing tink.
import json, wave, numpy as np
SR, DUR = 48000, 9.5
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(20)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def env(t, a, dec): return np.minimum(1, t / a) * np.exp(-t / dec)
def wood(f, dec=0.03):   # wooden block: two partials + a short click
    t = tt(0.3); return (np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * f * 2.76 * t) * env(t, 0.0005, dec * 0.4)) * env(t, 0.0008, dec) \
        + 0.15 * rs.standard_normal(len(t)) * env(t, 0.0002, 0.002)
def kick():
    t = tt(0.4); f = 110 * np.exp(-t * 22) + 48; return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(t, 0.002, 0.12)
def shaker():
    t = tt(0.08); n = band(rs.standard_normal(len(t)), 5000, 11000); return n / (np.abs(n).max() + 1e-9) * env(t, 0.004, 0.018)
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    a = np.exp(-2 * np.pi * (200 + 2400 * np.sin(np.pi * t / d) ** 2) / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y / (np.abs(y).max() + 1e-9) * np.sin(np.pi * t / d) ** 1.5
def stretch():   # rubbery pitch bend up and back
    t = tt(0.45); f = 180 + 160 * np.sin(np.pi * np.clip(t / 0.3, 0, 1)) + 20 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 6)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR); s = np.tanh(2.5 * s) * np.sin(np.pi * np.clip(t / 0.45, 0, 1)) ** 0.8; return s
def pop():
    t = tt(0.2); f = 900 * np.exp(-t * 30) + 380; return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(t, 0.001, 0.04)
def tone(freq, d, att, rel):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in [(1, 1), (2, .25), (3, .08)])
    return s * np.minimum(1, t / att) * np.minimum(1, np.maximum(0, d - t) / rel)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
# room tone
room = band(rs.standard_normal(N), 150, 2500); room /= np.abs(room).max(); L += room * .004; R += np.roll(room, 911) * .004
ev = json.load(open('events.json'))
for e in ev:
    k, te, v = e['k'], e['t'], e.get('v', 0)
    if k == 'beat':
        add(kick(), te, 0.34); add(shaker(), te + 0.25, 0.05, 0.3)   # kick on the beat, shaker on the off-beat
        bass = [45, 45, 48, 48, 50, 43, 45, 45, 48, 52, 45, 45][v]; add(tone(nt(bass), 0.42, 0.01, 0.2), te, 0.09)
    elif k == 'knock': add(wood(330, 0.06), te, 0.32); add(kick(), te, 0.2)
    elif k == 'wood': add(wood([620, 740, 880][v], 0.035), te, 0.2, [-.3, .3, 0][v])
    elif k == 'stretch': add(stretch(), te, 0.09)
    elif k == 'tick': add(wood(1500 + 180 * v, 0.012), te, 0.07, 0.35)
    elif k == 'tremble': add(wood(2100 + 300 * (v % 3), 0.006), te, 0.025, 0.4 - 0.1 * (v % 3))
    elif k == 'soft': add(tone(nt(76), 0.6, 0.05, 0.4), te, 0.025, 0.5)
    elif k == 'rattle':
        for i in range(5): add(wood(900 + 60 * i, 0.01), te + i * 0.045, 0.05, -0.5)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.16)
    elif k == 'pop': add(pop(), te, 0.2)
    elif k == 'swish': add(whoosh(0.5), te, 0.1)
    elif k == 'tink':
        for i, m in enumerate([69, 76, 81]): add(tone(nt(m), 1.2, 0.004, 0.9), te + i * 0.05, 0.035)
# lockup chord pad under the hold
for i, m in enumerate([57, 60, 64, 69]): add(tone(nt(m), 2.2, 0.3, 1.2), 7.15 + i * 0.03, 0.022)
fi = int(0.1 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
