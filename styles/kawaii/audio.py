# events.json → audio.wav (48 kHz stereo, 10 s)
# music-box melody over soft plucked bass, bubbly pops for sticker letters, boing hops and soft pats,
# yawns, twinkly chimes, a shimmer + whoosh for the sparkle-burst wipe, hand claps, a "yay" chord,
# confetti tinkles, a closing iris swoop and a final bell.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(68)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def sweep(f0, f1, d, shape=2.0):
    t = tt(d); f = f0 + (f1 - f0) * (t / d) ** (1 / shape); return np.sin(2 * np.pi * np.cumsum(f) / SR), t
def bell(f, d=1.2, dec=.35):                     # music-box / glockenspiel tine
    t = tt(d); s = np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / .08) + .15 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / .03)
    return s * np.exp(-t / dec) * np.minimum(1, t / .002)
def pluck(f, d=.5):
    t = tt(d); s = np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t); return s * np.exp(-t / .12) * np.minimum(1, t / .004)
def pop(f=600):
    s, t = sweep(f * .6, f * 1.8, .09, 1.0); return s * np.exp(-t / .03) * np.minimum(1, t / .002)
def boing(v):
    s, t = sweep(180, 520 + 200 * v, .22, 1.6); vib = 1 + .08 * np.sin(2 * np.pi * 28 * t); return s * vib * np.exp(-t / .09) * np.minimum(1, t / .004)
def pat():
    t = tt(.08); n = band(rs.standard_normal(len(t)), 150, 1400) * np.exp(-t / .012); b = np.sin(2 * np.pi * 110 * t) * np.exp(-t / .03)
    return .6 * n / (np.abs(n).max() + 1e-9) + .6 * b
def yawn():
    t = tt(.5); f = 330 - 120 * (t / .5); s = np.sin(2 * np.pi * np.cumsum(f) / SR) + .3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return s * np.sin(np.pi * t / .5) ** 1.5 * (1 + .1 * np.sin(2 * np.pi * 6 * t))
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    a = np.exp(-2 * np.pi * (300 + 3500 * (t / d) ** 1.5) / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y / (np.abs(y).max() + 1e-9) * np.sin(np.pi * t / d) ** 1.2
def clap():
    out = np.zeros(int(.25 * SR))
    for k, dt in enumerate([0, .008, .017]):
        t = tt(.2); n = band(rs.standard_normal(len(t)), 900, 6000) * np.exp(-t / (.012 if k < 2 else .05)); i = int(dt * SR); out[i:i + len(n)] += n[:len(out) - i]
    return out / (np.abs(out).max() + 1e-9)
# ── music bed: 120 bpm, C major, music box + plucked bass ──
bpm = 120; b = 60 / bpm
melA = [(0, 76), (1, 79), (1.5, 81), (2, 79), (3, 76), (3.5, 74), (4, 72), (5, 74), (5.5, 76), (6, 79), (7, 74)]
melB = [(0, 84), (.5, 83), (1, 81), (1.5, 79), (2, 81), (3, 84), (4, 86), (4.5, 84), (5, 81), (5.5, 79), (6, 81), (6.5, 84), (7, 88), (8, 84), (8.5, 86), (9, 88)]
for bt, m in melA: add(bell(nt(m), 1.0, .3), .45 + bt * b, .07, .15)
for bt, m in melB: add(bell(nt(m), 1.0, .28), 4.6 + bt * b, .075, -.15)
bass = [48, 48, 45, 45, 41, 41, 43, 43] * 3
for k in range(19):
    tb = .45 + k * b
    if tb > 9.4: break
    if 3.8 < tb < 4.55: continue
    add(pluck(nt(bass[k % len(bass)] - (0 if tb < 4.5 else 0))), tb, .09)
    add(pluck(nt(bass[k % len(bass)] + 7), .3), tb + b / 2, .035)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'pop': add(pop(nt(72 + [0, 2, 4, 7, 9, 12, 14, 16, 19, 21, 24, 26, 28, 31][e['n'] % 14])), te, .22 * min(v, 1.2), rs.uniform(-.4, .4))
    elif k == 'boing': add(boing(v), te, .09 * (.5 + v * .6), rs.uniform(-.3, .3))
    elif k == 'pat': add(pat(), te, .12 * min(1, .4 + v))
    elif k == 'yawn': add(yawn(), te, .05, rs.uniform(-.3, .3))
    elif k == 'chime':
        for i, m in enumerate([88, 91, 96]): add(bell(nt(m), .8, .2), te + i * .05, .05, rs.uniform(-.5, .5))
    elif k == 'unpop':
        for i in range(8): add(pop(nt(84 - i * 2)), te + i * .03, .08, -.5 + i * .14)
    elif k == 'shimmer':
        for i in range(12): add(bell(nt(84 + (i * 5) % 17), .5, .12), te + i * .03, .03, rs.uniform(-.7, .7))
    elif k == 'whoosh': add(whoosh(e['d']), te, .25)
    elif k == 'sparkle':
        for i, m in enumerate([96, 100, 103, 108]): add(bell(nt(m), .9, .25), te + i * .045, .05, (i - 1.5) * .3)
    elif k == 'clap': add(clap(), te, .35); add(bell(nt(91), .6, .2), te, .05)
    elif k == 'yay':
        for i, m in enumerate([60, 64, 67, 72, 76, 79]): add(bell(nt(m), 1.6, .6), te + i * .025, .06)
    elif k == 'tink': add(bell(nt(rs.choice([96, 98, 100, 103, 105])), .4, .08), te, .025, rs.uniform(-.8, .8))
    elif k == 'iris': s, t = sweep(900, 260, e['d'], .6); add(s * np.sin(np.pi * t / e['d']) * .5 + whoosh(e['d']) * .4, te, .12)
    elif k == 'ding':
        for i, m in enumerate([72, 79, 84, 88]): add(bell(nt(m), 1.8, .7), te + i * .06, .07)
fi = int(.05 * SR); fo = int(.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.1) * .85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
