# events.json → audio.wav (48 kHz stereo, 10 s)
# explainer-channel sound design: light marimba/pluck bed (120 bpm), cartoon pops, swishes and whooshes for pans,
# UI blips for counters, dings for highlighted pictograms, paper flips, drawer slide, zoom riser, soft Zzz, charge-up, end chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(29)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def sweep(f0, f1, d, curve=1.0):
    t = tt(d); f = f0 + (f1 - f0) * (t / d) ** curve; return np.sin(2 * np.pi * np.cumsum(f) / SR), t
def pop(v=1.0):
    s, t = sweep(260 * (0.8 + 0.4 * v), 900, 0.09, 0.6); return s * np.exp(-t / 0.03) * np.minimum(1, t / 0.002)
def blip(f):
    t = tt(0.07); return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * np.exp(-t / 0.02)
def tick(f):
    t = tt(0.12); s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.03); c = norm(band(rs.standard_normal(len(t)), 2000, 8000)) * np.exp(-t / 0.003)
    return s + 0.3 * c
def marimba(f, d=0.6):
    t = tt(d); return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / 0.03)) * np.exp(-t / 0.18) * np.minimum(1, t / 0.003)
def ding(f):
    t = tt(0.9); s = sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (0.35 / h)) for h, a in [(1, 1), (2.76, .35), (5.4, .12)]); return s * np.minimum(1, t / 0.002)
def noise_sweep(d, lo, hi, shape=1.5):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = lo + (hi - lo) * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** shape
def riser(d):
    t = tt(d); n = noise_sweep(d, 300, 4000, 0.8) * (t / d) ** 1.5
    s, _ = sweep(180, 900, d, 2.0); return n + 0.25 * s * (t / d) ** 2
def thud():
    s, t = sweep(140, 55, 0.25); return s * np.exp(-t / 0.08)
def flip():
    t = tt(0.08); return norm(band(rs.standard_normal(len(t)), 1500, 7000)) * np.exp(-t / 0.015) * np.minimum(1, t / 0.004)
def drawer():
    t = tt(0.3); n = norm(band(rs.standard_normal(len(t)), 150, 1500)) * np.sin(np.pi * t / 0.3) ** 0.6
    k = np.zeros_like(t); k[int(0.27 * SR):] = np.exp(-(t[int(0.27 * SR):] - 0.27) / 0.02); return 0.6 * n + 0.8 * k * np.sin(2 * np.pi * 120 * t)
def yawn():
    t = tt(0.75); f = 330 - 120 * (t / 0.75) + 30 * np.sin(np.pi * t / 0.75); ph = 2 * np.pi * np.cumsum(f) / SR
    v = sum(np.sin(ph * h) / h for h in range(1, 6)); env = np.sin(np.pi * t / 0.75) ** 1.2
    return band(v, 200, 1800) * env
def zzz():
    t = tt(0.55); s = np.sin(2 * np.pi * (180 + 10 * np.sin(2 * np.pi * 5 * t)) * t) * np.sin(np.pi * t / 0.55) ** 2
    return s + 0.2 * norm(band(rs.standard_normal(len(t)), 300, 1200)) * np.sin(np.pi * t / 0.55) ** 2
def charge(d):
    t = tt(d); f = 300 * 2 ** (1.6 * t / d); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + 0.3 * np.sin(2 * ph)) * (0.3 + 0.7 * t / d) * np.minimum(1, (d - t) / 0.05) * (0.8 + 0.2 * np.sin(2 * np.pi * 14 * t))
def tone(freq, d, att=0.05, rel=1.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in [(1, 1), (2, .25), (3, .08)])
    return s * np.minimum(1, t / att) * np.minimum(1, (d - t) / rel)

# music bed: 120 bpm, C – Am – F – G marimba arpeggios; after the whip to night, a soft pad
BEAT = 0.5; chords = [[60, 64, 67, 72], [57, 60, 64, 69], [53, 57, 60, 65], [55, 59, 62, 67]]
for b in range(16):
    tb = 0.1 + b * BEAT; ch = chords[(b // 2) % 4]
    if tb > 7.9: break
    add(marimba(nt(ch[0] - 12), 0.5), tb, 0.08, -0.2)
    for k in range(2): add(marimba(nt(ch[1 + (b + k) % 3]), 0.4), tb + k * BEAT / 2, 0.045, 0.25 * (1 if k else -1))
for m, g in [(48, .03), (55, .022), (64, .018), (67, .014)]: add(tone(nt(m), 1.9, 0.4, 1.2), 8.1, g)
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'pop': add(pop(e.get('v', 1)), te, 0.35 * e.get('v', 1))
    elif k == 'swish': add(noise_sweep(e['d'], 800, 6000), te, 0.09, -0.3)
    elif k == 'whoosh': add(noise_sweep(e['d'], 300, 3500, 1.2), te, 0.2)
    elif k == 'blip': add(blip(e['f']), te, 0.14 * e.get('v', 1))
    elif k == 'low': add(blip(330), te, 0.2); add(blip(330), te + 0.14, 0.2)
    elif k == 'step': add(tick(160), te, 0.12, rs.uniform(-.2, .2))
    elif k == 'tick': add(tick(e['f']), te, 0.14, rs.uniform(-.4, .4))
    elif k == 'ding': add(ding(nt(76 + [0, 4, 7][e['n']])), te, 0.12)
    elif k == 'thud': add(thud(), te, 0.4)
    elif k == 'riser': add(riser(e['d']), te, 0.2)
    elif k == 'drawer': add(drawer(), te, 0.28)
    elif k == 'flip': add(flip(), te + rs.uniform(0, 0.02), 0.1, rs.uniform(-.6, .6))
    elif k == 'yawn': add(yawn(), te, 0.16)
    elif k == 'zzz': add(zzz(), te, 0.06)
    elif k == 'charge': add(charge(e['d']), te, 0.07)
    elif k == 'chord':
        for i, m in enumerate([72, 76, 79, 84]): add(ding(nt(m)), te + i * 0.05, 0.07)
        for m in [48, 60, 64, 67]: add(tone(nt(m), 1.1, 0.02, 0.9), te, 0.035)
# master: fade in/out, soft limiter
fi = int(0.05 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
