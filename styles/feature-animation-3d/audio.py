# events.json -> audio.wav (48 kHz stereo, 10 s). Everything is synthesized, nothing is sampled.
# A little short-film score in D major (104 bpm): Karplus-Strong pizzicato bass and plucks that
# mickey-mouse the action, a glockenspiel for the star, a slide whistle for its fall, rubber boings
# and thuds for the hops, a string pad that swells as night falls, celesta twinkles for the sky,
# a harp glissando as the star floats up, a sparkle when it parks, and a warm closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR)
dry = [np.zeros(N), np.zeros(N)]; wet = [np.zeros(N), np.zeros(N)]
rs = np.random.default_rng(181)

def add(sig, t, g=1.0, pan=0.0, bus=None):
    i = int(round(t * SR)); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    l, r = bus or dry
    l[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414
    r[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a=0.003, r=0.05):
    t = tt(d); return np.minimum(1, t / a) * np.clip((d - t) / r, 0, 1)
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def glide(f0, f1, d, curve=1.0):
    t = tt(d); f = f0 * (f1 / f0) ** ((t / d) ** curve); return np.sin(2 * np.pi * np.cumsum(f) / SR)

def ks(f, d, damp=0.994, soft=3):
    """Karplus-Strong pluck, computed one period-block at a time"""
    n, P = int(d * SR), max(2, int(round(SR / f)))
    y = np.zeros(n + 1); burst = rs.uniform(-1, 1, P)
    for _ in range(soft): burst = 0.5 * (burst + np.roll(burst, 1))          # softer attack
    y[1:P + 1] = burst
    for s in range(P + 1, n + 1, P):
        e = min(s + P, n + 1); y[s:e] = damp * 0.5 * (y[s - P:e - P] + y[s - P - 1:e - P - 1])
    return y[1:] * env(d, 0.001, 0.04)
def bell(f, d=1.2, ratios=(1, 2.76, 5.4, 8.93), decay=(3.2, 6, 11, 18), amps=(1, 0.42, 0.2, 0.08)):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * k) for r, k, a in zip(ratios, decay, amps))
    return s * env(d, 0.0008, 0.05)
def celesta(f, d=1.0):
    return bell(f, d, ratios=(1, 2, 3.01, 4.2), decay=(4, 7, 12, 20), amps=(1, 0.3, 0.12, 0.05))
def pad(ms, d, att=0.9, rel=1.4, bright=7):
    t = tt(d); s = np.zeros_like(t)
    for m in ms:
        for det in (-0.08, 0.0, 0.07):
            f = nt(m) * 2 ** (det / 12); ph = rs.uniform(0, 6.28)
            for h in range(1, bright + 1): s += np.sin(2 * np.pi * f * h * t + ph * h) / h ** 1.3
    return s * np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1) / (3 * len(ms) * 2.2)
def boing(f, d=0.42):
    t = tt(d); fm = f * (1 + 0.55 * np.exp(-t * 9) * np.cos(2 * np.pi * 11 * t)) * (1 + 0.35 * np.exp(-t * 14))
    ph = 2 * np.pi * np.cumsum(fm) / SR
    return np.sin(ph + 0.7 * np.sin(ph * 2)) * np.exp(-t * 7) * env(d, 0.002, 0.05)
def thud(f=95, d=0.25):
    t = tt(d); return np.sin(2 * np.pi * np.cumsum(f * (1 + 1.4 * np.exp(-t * 35))) / SR) * np.exp(-t * 18) \
        + 0.18 * band(rs.standard_normal(len(t)), 150, 1400) * np.exp(-t * 60)
def bloop(f, d=0.2, up=2.0):
    t = tt(d); fm = f * (1 + (up - 1) * (1 - np.exp(-t * 30)))
    return np.sin(2 * np.pi * np.cumsum(fm) / SR) * np.exp(-t * 16) * env(d, 0.002, 0.03)
def tick(f=3200, d=0.03):
    t = tt(d); return np.sin(2 * np.pi * f * t) * np.exp(-t * 220)
def whoosh(d, lo, hi):
    x = band(rs.standard_normal(int(d * SR)), lo, hi) * np.sin(np.pi * np.clip(tt(d) / d, 0, 1)) ** 2
    return x / (np.abs(x).max() + 1e-9)

# ---------------------------------------------------------------- score
B = 60 / 104
# pizzicato bass, two beats per note through the day, then it hands over to the pad
for k, m in enumerate([50, 45, 47, 42, 43, 50, 52, 45]):
    t0 = 0.6 + 2 * k * B
    if t0 > 6.2: break
    add(ks(nt(m), 0.7, 0.992), t0, 0.34, -0.1, wet)
    add(ks(nt(m + 12), 0.35, 0.985), t0 + B, 0.12, 0.15, wet)
# off-beat plucked chords, light and bouncy, until dusk
CH = [[62, 66, 69], [61, 64, 69], [62, 66, 71], [61, 66, 69], [62, 67, 71], [62, 66, 69], [64, 67, 71], [61, 64, 69]]
for k in range(16):
    t0 = 0.6 + (k + 0.5) * B
    if t0 > 4.4: break
    for j, m in enumerate(CH[k // 2]): add(ks(nt(m + 12), 0.25, 0.97), t0 + 0.006 * j, 0.045, -0.3 + 0.3 * j, wet)
# dusk -> night: string pad
add(pad([55, 59, 62, 66], 1.6, 0.8, 0.6), 4.15, 0.5, 0, wet)           # Gmaj7
add(pad([57, 61, 64, 69], 1.4, 0.5, 0.6), 5.35, 0.52, 0, wet)          # A
add(pad([50, 57, 62, 66, 69], 4.4, 0.7, 1.6), 6.45, 0.58, 0, wet)      # D (add the fifth below)
# night: celesta arpeggio
for k, m in enumerate([74, 78, 81, 86, 81, 78, 74, 78, 81, 85, 88, 85]):
    t0 = 6.5 + k * B / 2
    if t0 > 9.4: break
    add(celesta(nt(m), 1.0), t0, 0.07, -0.4 + 0.07 * k, wet)

# ---------------------------------------------------------------- cues
for e in json.load(open('events.json')):
    k, t, pan = e['k'], e['t'], e.get('pan', 0.0)
    if k == 'wake':
        add(bloop(620, 0.16, 1.7), t, 0.2); add(bloop(880, 0.14, 1.6), t + 0.06, 0.14, 0.1)
        add(celesta(nt(81), 1.2), t, 0.09, 0, wet)
    elif k == 'glance':
        add(tick(2800 + 600 * pan, 0.03), t, 0.12, pan); add(ks(nt(78 + int(3 * pan)), 0.3, 0.98), t, 0.08, pan, wet)
    elif k == 'blink': add(bloop(1500, 0.05, 1.3), t + 0.03, 0.05)
    elif k == 'fall':
        d = 0.42; add(glide(1900, 620, d, 0.9) * env(d, 0.02, 0.06), t, 0.1, 0.35, wet)
    elif k == 'ting': add(bell(nt([81, 85, 88][e['i']])), t, 0.2, 0.25 + 0.1 * e['i'], wet)
    elif k == 'tap': add(bell(nt(93), 0.5), t, 0.05, 0.5, wet)
    elif k == 'pop':
        add(bloop(150 + 40 * e['i'], 0.22, 2.4), t, 0.3, 0.2 + 0.15 * e['i']); add(thud(80, 0.2), t, 0.14, 0.2)
    elif k == 'hop':
        i = e['i']
        if i == 0: add(boing(330, 0.3), t, 0.12, -0.1)
        else:
            add(boing([196, 247, 294][i - 1]), t, 0.2, -0.2 + 0.2 * i)
            add(ks(nt([62, 66, 69][i - 1]), 0.5, 0.99), t, 0.16, -0.1 + 0.15 * i, wet)
    elif k == 'land': add(thud(105 - 8 * e['i'], 0.22), t, 0.28 if e['i'] else 0.14, -0.1 + 0.15 * e['i'])
    elif k == 'dusk': add(whoosh(1.6, 200, 2200), t, 0.035, 0, wet)
    elif k == 'moon':
        d = 1.2; add(glide(140, 70, d, 0.7) * np.sin(np.pi * tt(d) / d) ** 2, t, 0.14, 0.4, wet); add(whoosh(1.0, 300, 1800), t, 0.05, 0.4)
    elif k == 'twinkle': add(celesta(nt(int(rs.choice([86, 88, 90, 93, 95, 98]))), 0.8), t, 0.05, pan, wet)
    elif k == 'toy': add(bell(nt(int(rs.choice([90, 93, 95]))), 0.9), t, 0.045, pan, wet)
    elif k == 'rise':
        for j, m in enumerate([62, 64, 66, 69, 71, 74, 76, 78, 81, 83, 86]): add(ks(nt(m), 0.9, 0.995), t + 0.055 * j, 0.07, -0.2 + 0.05 * j, wet)
    elif k == 'park':
        add(bell(nt(93), 1.6), t, 0.12, 0.3, wet)
        for j in range(6): add(bell(nt(98 + 2 * (j % 3)), 0.5), t + 0.04 + 0.05 * j, 0.03, rs.uniform(-0.2, 0.6), wet)
    elif k == 'happy':
        d = 0.7; s = glide(nt(69), nt(66), d, 0.6); breath = band(rs.standard_normal(int(d * SR)), 400, 2500) * 0.15
        add((s + 0.25 * glide(nt(81), nt(78), d, 0.6) + breath) * np.sin(np.pi * tt(d) / d) ** 1.5, t, 0.07, 0, wet)
    elif k == 'title':
        for j, m in enumerate([62, 66, 69, 74, 78]): add(celesta(nt(m + 12), 1.6), t + 0.09 * j, 0.06, -0.3 + 0.15 * j, wet)

# ---------------------------------------------------------------- room + master
ir_t = tt(1.8); M = 1 << int(np.ceil(np.log2(N + len(ir_t))))
for ch, seed in ((0, 1), (1, 2)):
    ir = np.random.default_rng(seed).standard_normal(len(ir_t)) * np.exp(-ir_t / 0.42); ir = band(ir, 120, 8000); ir /= np.sqrt(np.sum(ir ** 2))
    rev = np.fft.irfft(np.fft.rfft(wet[ch], M) * np.fft.rfft(ir, M), M)[:N]
    dry[ch] += wet[ch] * 0.8 + rev * 0.3
st = np.stack(dry, 1)
fi, fo = int(0.02 * SR), int(0.75 * SR)
st[:fi] *= np.linspace(0, 1, fi)[:, None]; st[-fo:] *= (np.linspace(1, 0, fo) ** 1.6)[:, None]
pk = np.abs(st).max(); st = np.tanh(st / pk * 1.25) * 0.78
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(st, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
print('audio.wav ok, peak before norm', round(float(pk), 3))
