# events.json → audio.wav (48 kHz stereo, 10 s)
# dry, wooden sound for a painting that assembles itself: short slides and knocks as the bars lock,
# brush swipes for the colour planes, a low glide for the rebalance, then a boogie-woogie walking bass
# and piano stabs while the squares hop along the avenues, plucked notes for the words and a final chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(121)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def knock(f0=520, dec=0.03):
    # woodblock: two inharmonic partials + a click
    t = tt(0.2); s = np.sin(2 * np.pi * f0 * t) * np.exp(-t / dec) + 0.5 * np.sin(2 * np.pi * f0 * 2.76 * t) * np.exp(-t / (dec * 0.5))
    c = norm(band(rs.standard_normal(len(t)), 2000, 9000)) * np.exp(-t / 0.002)
    return s + 0.3 * c
def slide(d, lo=600, hi=4000):
    t = tt(d); x = norm(band(rs.standard_normal(len(t)), lo, hi)); env = (t / d) ** 1.5 * np.minimum(1, (d - t) / 0.02)
    return x * env
def swipe(d):
    # bristle swish: noise with a moving one-pole lowpass
    t = tt(d + 0.08); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 500 + 3500 * np.clip(t / d, 0, 1); a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    env = np.minimum(1, t / 0.015) * np.exp(-np.maximum(0, t - d) / 0.03)
    return norm(y) * env
def pluck(freq, d=0.6, bright=1.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) * np.exp(-t / (0.35 / h ** (0.6 * bright))) for h, a in [(1, 1), (2, .5), (3, .25), (4, .12), (5, .06)])
    return s * np.minimum(1, t / 0.003)
def glide(f0, f1, d):
    t = tt(d); f = f0 + (f1 - f0) * (0.5 - 0.5 * np.cos(np.pi * t / d)); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.sin(np.pi * t / d) ** 0.7
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 200 + 2200 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
t = np.arange(N) / SR
room = norm(band(rs.standard_normal(N), 120, 1800)); L += room * .003; R += np.roll(room, 777) * .003
# boogie-woogie walking bass in C (one note per hop, eighth notes)
BASS = [36, 40, 43, 45, 46, 45, 43, 40]
STAB = {0: [60, 64, 70], 6: [60, 64, 70], 8: [65, 69, 75], 14: [65, 69, 75]}
ev = json.load(open('events.json'))
for e in ev:
    k, te = e['k'], e['t']; d = e.get('d', 0.3); v = e.get('v', 1.0)
    if k == 'slide': add(slide(d), te, 0.05 * v, -0.3 if e.get('o') == 'v' else 0.3)
    elif k == 'lock': add(knock(), te, 0.22 * v, rs.uniform(-.3, .3)); add(knock(180, 0.05), te, 0.12 * v)
    elif k == 'tick': add(knock(rs.choice([620, 700, 780]), 0.02), te, 0.06, rs.uniform(-.6, .6))
    elif k == 'wipe': add(swipe(d), te, 0.11 * v, rs.uniform(-.2, .2))
    elif k == 'shift': add(glide(nt(43), nt(48), d), te, 0.07); add(slide(d, 200, 1200), te, 0.03)
    elif k == 'whoosh': add(whoosh(d), te, 0.09 * v)
    elif k == 'hop':
        n = e['n']; g = min(1, n / 4) * 0.8 + 0.2
        add(pluck(nt(BASS[n % 8]), 0.3, 0.6), te, 0.16 * g)
        add(knock(1400, 0.008), te, 0.02 * g, 0.4 if n % 2 else -0.4)
        if n % 16 in STAB:
            for m in STAB[n % 16]: add(pluck(nt(m), 0.25, 1.4), te + 0.004, 0.04 * g, 0.2)
    elif k == 'pop': add(pluck(nt(e['n']), 0.9), te, 0.09, rs.uniform(-.3, .3)); add(knock(900, 0.012), te, 0.05)
    elif k == 'chord':
        for i, m in enumerate([48, 60, 64, 67, 72, 76]): add(pluck(nt(m), 1.6, 0.8), te + i * 0.025, 0.05)
# master: fade in/out, soft limiter
fi = int(0.1 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.8) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
