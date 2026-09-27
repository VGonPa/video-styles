# events.json → audio.wav (48 kHz stereo, 10 s)
# A short synthwave cue at 100 bpm (Am – F – C – G): detuned-saw pad, rolling 16th-note bass, gated-reverb snare,
# four-on-the-floor kick and a plucked arpeggio, all entering on the chrome-logo slam (bar 2 downbeat, 3.0 s).
# SFX from events.json: CRT power on/off, laser zaps and wipes, the slam impact, star-glint tings, light-sweep shimmer,
# neon ignition buzz and flicker, typing blips and road whooshes for the passing palms.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(1986)
BEAT, M0 = 0.6, 0.6
def add(sig, t, g=1.0, pan=0.0):
    i = int(round(t * SR)); j = max(0, -i); i = max(0, i); n = min(len(sig) - j, N - i)
    if n > 0:
        s = sig[j:j + n] * g
        L[i:i + n] += s * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += s * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def lp(x, fc):  # gentle spectral low-pass (1-pole-ish rolloff)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X /= np.sqrt(1 + (f / fc) ** 4); return np.fft.irfft(X, len(x))
def conv(x, h):
    n = len(x) + len(h) - 1; return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
saw = lambda f, t, ph=0: 2 * ((f * t + ph) % 1) - 1
def env(t, a, d, s=0.0, rel=None):
    e = np.minimum(1, t / max(a, 1e-4)) * (s + (1 - s) * np.exp(-np.maximum(t - a, 0) / d))
    if rel: e *= np.clip((t[-1] - t) / rel, 0, 1)
    return e

# ── music ──
CH = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62], [57, 60, 64]]   # Am F C G (Am tail)
ROOT = [45, 41, 36, 43, 45]
bar = lambda k: M0 + k * 4 * BEAT
def pad(notes, d, cut):
    t = tt(d); s = np.zeros_like(t)
    for m in notes:
        for dt, ph in [(-0.09, 0.1), (0.0, 0.5), (0.1, 0.8)]:
            s += saw(nt(m + 12) * 2 ** (dt / 12), t, ph)
    s = lp(s, cut) * env(t, 0.35, 99, 1, 0.35)
    return s / 9
for k in range(4):
    add(pad(CH[k], 4 * BEAT + 0.3, 1500 if k else 900), bar(k) - (0.4 if k == 0 else 0), 0.16 if k else 0.12, 0)
add(pad(CH[4], 1.6, 900), bar(4), 0.1)
t0 = np.arange(N) / SR
def bassnote(m, d, cut):
    t = tt(d); s = saw(nt(m), t) + 0.5 * saw(nt(m) * 1.004, t, .3) + 0.6 * np.sin(2 * np.pi * nt(m) / 2 * t)
    return lp(s, cut) * env(t, 0.004, 0.09, 0.35) * np.clip((d - t) / 0.01, 0, 1)
for k in range(4):
    for i in range(16):
        tb = bar(k) + i * BEAT / 4
        if tb > 9.35: break
        m = ROOT[k] + (12 if i % 2 else 0)
        pre = k == 0
        add(bassnote(m, BEAT / 4 * 0.9, 380 + 200 * i / 16 if pre else 900), tb, 0.07 if pre else 0.2, 0)
def kick():
    t = tt(0.4); f = 45 + 110 * np.exp(-t * 35); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.13) * 1.0
IR = rs.standard_normal(int(0.32 * SR)) * np.exp(-tt(0.32) / 0.2); IR[int(0.28 * SR):] *= np.linspace(1, 0, len(IR) - int(0.28 * SR))
def snare():
    t = tt(0.2); s = 0.8 * band(rs.standard_normal(len(t)), 900, 9000) * np.exp(-t / 0.05) + 0.5 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.04)
    wet = conv(s, IR * 0.04); wet[:len(s)] += s * 0.6; return norm(wet)
def hat(o=False):
    t = tt(0.12 if o else 0.05); return norm(band(rs.standard_normal(len(t)), 7000, 16000)) * np.exp(-t / (0.04 if o else 0.012))
KICK, SNARE = kick(), snare()
for b in range(4, 16):
    tb = M0 + b * BEAT
    if tb > 9.3: break
    add(KICK, tb, 0.45)
    if b % 2 == 1: add(SNARE, tb, 0.22, 0.05)
    add(hat(), tb + BEAT / 2, 0.05, 0.3); add(hat(), tb + BEAT / 4, 0.025, -0.3); add(hat(), tb + 3 * BEAT / 4, 0.025, -0.3)
def pluck(f):
    t = tt(0.3); s = (saw(f, t) + 0.5 * np.sign(np.sin(2 * np.pi * f * 2 * t))) ; return lp(s, 2600) * np.exp(-t / 0.08) * np.minimum(1, t / 0.002)
for k in (2, 3):
    notes = CH[k] + [CH[k][0] + 12]
    for i in range(16):
        tb = bar(k) + i * BEAT / 4
        if tb > 9.3: break
        add(pluck(nt(notes[[0, 1, 2, 3, 2, 1, 0, 2][i % 8]] + 12)), tb, 0.05, 0.5 * np.sin(i))
        add(pluck(nt(notes[[0, 1, 2, 3, 2, 1, 0, 2][i % 8]] + 12)), tb + 0.3, 0.018, -0.5 * np.sin(i))   # dotted-eighth echo

# ── SFX ──
def sweep(f0, f1, d, wave_='sin'):
    t = tt(d); f = f0 * (f1 / f0) ** (t / d); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) if wave_ == 'sin' else np.sign(np.sin(ph)) * .5)
def whoosh(d, rev=False):
    t = tt(d); x = rs.standard_normal(len(t)); e = np.sin(np.pi * t / d) ** 2 if not rev else (t / d) ** 3
    return norm(band(x, 300, 5000)) * e
def ting(f):
    t = tt(1.0); return sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t * k) for h, a, k in [(1, 1, 4), (2.76, .4, 7), (5.4, .2, 11)])
def shimmer():
    d = 0.9; t = tt(d); s = np.zeros_like(t)
    for i in range(16):
        f = 3000 + 4000 * rs.random(); k = int(rs.uniform(0, .55) * SR); tl = t[:len(t) - k]; g = np.zeros_like(t); g[k:] = np.sin(2 * np.pi * f * tl) * np.exp(-tl / .1); s += g
    return s * np.sin(np.pi * t / d)
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'crton':
        add(sweep(60, 14000, 0.35) * np.exp(-tt(0.35) / 0.2), te, 0.03); t = tt(0.25); add(np.sin(2 * np.pi * 70 * t) * np.exp(-t / .06), te, 0.3)
        add(norm(band(rs.standard_normal(int(0.4 * SR)), 2000, 9000)) * np.exp(-tt(0.4) / .12), te, 0.05)
    elif k == 'zap': add(sweep(2400, 500, 0.18) * np.exp(-tt(0.18) / .06), te, 0.08, -.2); add(sweep(3000, 700, 0.18) * np.exp(-tt(0.18) / .06), te + .06, 0.05, .2)
    elif k == 'charge': add(sweep(200, 1800, 0.32, 'sq') * (tt(0.32) / .32) ** 2, te, 0.06); add(whoosh(0.32, True), te, 0.12)
    elif k == 'laser':
        add(sweep(3200, 180, 0.45) * np.exp(-tt(0.45) / .2), te, 0.12, -.3); add(sweep(2900, 160, 0.45) * np.exp(-tt(0.45) / .2), te + .02, 0.12, .3)
        add(whoosh(0.45), te, 0.1)
    elif k == 'fall': add(whoosh(0.22, True), te, 0.3)
    elif k == 'slam':
        t = tt(1.2); sub = np.sin(2 * np.pi * np.cumsum(38 + 90 * np.exp(-t * 18)) / SR) * np.exp(-t / .35)
        crash = norm(band(rs.standard_normal(len(t)), 3000, 15000)) * np.exp(-t / .5)
        add(sub, te, 0.7); add(crash, te, 0.1, -.2); add(np.roll(crash, 480), te + .01, 0.08, .2); add(SNARE, te, 0.35)
        add(pad([57, 64, 69, 72], 1.6, 3000) * np.exp(-tt(1.6) / .9), te, 0.2)
    elif k == 'glint': add(ting(2637 if rs.random() < .5 else 3136), te + .08, 0.05, rs.uniform(-.4, .4))
    elif k == 'sweep': add(shimmer(), te, 0.04, .2)
    elif k == 'neon':
        d = 1.1; t = tt(d); buzz = lp(saw(120, t) + .5 * saw(240, t), 2500)
        gate = np.array([1 if rs.random() < .35 + .6 * min(1, x / 0.5) else 0.1 for x in t[::1600]]).repeat(1600)[:len(t)]
        add(buzz * gate * np.exp(-np.maximum(t - .5, 0) / .25), te, 0.035, .2)
        add(norm(band(rs.standard_normal(len(t)), 3000, 12000)) * gate * 0.3 * np.exp(-t / .4), te, 0.03)
    elif k == 'flickoff':
        d = .4; t = tt(d); gate = (rs.random(int(d * 30) + 1) < .5).astype(float).repeat(1600)[:len(t)]
        add(lp(saw(120, t), 2000) * gate * (1 - t / d), te, 0.04, .2)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.1)
    elif k == 'laser2': add(sweep(600, 2600, 0.4) * np.sin(np.pi * tt(0.4) / .4), te, 0.04); add(whoosh(0.4), te, 0.05)
    elif k == 'tick': t = tt(0.04); add(np.sign(np.sin(2 * np.pi * 1760 * t)) * np.exp(-t / .01), te, 0.025, rs.uniform(-.3, .3))
    elif k == 'pass': add(whoosh(0.35), te, 0.07 * e.get('v', 1), e['pan'])
    elif k == 'crtoff':
        add(sweep(9000, 80, 0.5) * np.exp(-tt(0.5) / .25), te, 0.03); t = tt(0.3); add(np.sin(2 * np.pi * 55 * t) * np.exp(-t / .08), te + .38, 0.25)
        add(norm(band(rs.standard_normal(int(0.25 * SR)), 1500, 8000)) * np.exp(-tt(0.25) / .05), te + .4, 0.06)

# ── master ──
fi = int(0.05 * SR); fo = int(0.35 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 2
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
