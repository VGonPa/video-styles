# events.json → audio.wav (48 kHz stereo, 10 s). All synthesized, no samples.
# Storytime-channel sound design: a bouncy plucked-ukulele loop under the confident start, a soft pop
# for the character and every thought bubble, tiny ticks as words appear, a smug "ding", a pan sizzle,
# sniff and "huh?" blips, a record scratch + two whoosh snap-zooms and a low "dun-DUN" sting, a harp
# glissando into and out of the flashback, a detuned music-box whistle tune inside it, spaghetti rattling
# into a dry pot, piercing smoke-alarm beeps, a two-note "womp womp", and a slide-whistle iris out.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(76)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def env(d, att=0.004, dec=0.2):
    t = tt(d); return np.minimum(1, t / att) * np.exp(-t / dec) * np.minimum(1, (d - t) / 0.01)
def pluck(f, d=0.5, dec=0.18, bright=0.5):
    t = tt(d); s = np.sin(2 * np.pi * f * t) + bright * 0.5 * np.sin(4 * np.pi * f * t) * np.exp(-t / 0.05) + bright * 0.25 * np.sin(6 * np.pi * f * t) * np.exp(-t / 0.03)
    return s * env(d, 0.002, dec)
def bell(f, d=0.9, dec=0.35, det=0.0):
    t = tt(d); return (np.sin(2 * np.pi * f * (1 + det) * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.1)) * env(d, 0.002, dec)
def sine_sweep(f0, f1, d, dec=None, curve=1.0):
    t = tt(d); k = (t / d) ** curve; f = f0 * (f1 / f0) ** k; ph = 2 * np.pi * np.cumsum(f) / SR
    e = np.exp(-t / dec) if dec else np.minimum(1, (d - t) / 0.03)
    return np.sin(ph) * e * np.minimum(1, t / 0.004)
def lp(x, a):  # one-pole low-pass
    y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)): acc += a * (x[i] - acc); y[i] = acc
    return y
def noise(d): return rs.uniform(-1, 1, int(d * SR))
def bandnoise(d, a_lo, a_hi):
    n = noise(d); return lp(n, a_hi) - lp(n, a_lo)
ev = json.load(open('events.json'))
T = {}
for e in ev: T.setdefault(e['k'], e['t'])
# ── bouncy ukulele loop (C–G–Am–F, 120 bpm, 8ths) until the record scratch ──
e8 = 0.25
prog = [[60, 64, 67, 72], [59, 62, 67, 71], [57, 60, 64, 69], [57, 60, 65, 69]]
pat = [0, 2, 1, 3, 2, 1, 3, 2]
tb = 0.15; k = 0
while tb < T['scratch']:
    ch = prog[(k // 8) % 4]; m = ch[pat[k % 8]]
    g = 0.07 if tb < T['cut'] else 0.05
    add(pluck(nt(m), 0.4, 0.14, 0.7), tb, g * min(1, (T['scratch'] - tb) / 0.05), 0.25 * np.sin(k))
    if k % 4 == 0: add(pluck(nt(ch[0] - 24), 0.5, 0.2, 0.2), tb, 0.12)
    if k % 2 == 1: add(bandnoise(0.03, 0.2, 0.9) * env(0.03, 0.001, 0.008), tb, 0.03, -0.2)
    tb += e8; k += 1
# ── flashback music box: a whistled little tune, slightly detuned ──
tune = [72, 76, 79, 76, 77, 74, 72, 71, 72]
for i, m in enumerate(tune):
    ts = T['memory'] + i * 0.16
    if ts > T['harpDown']: break
    add(bell(nt(m + 12), 0.7, 0.3, 0.004), ts, 0.035, 0.3); add(bell(nt(m), 0.7, 0.3, -0.003), ts, 0.03, -0.3)
    t = tt(0.15); wf = nt(m + 12) * (1 + 0.012 * np.sin(2 * np.pi * 6 * t)); add(np.sin(2 * np.pi * np.cumsum(wf) / SR) * env(0.15, 0.02, 0.2), ts, 0.025)
# ── soft ending plucks (sheepish, sparse) ──
for i, m in enumerate([67, 64, 62, 60, 59, 60]):
    ts = T['womp'] + 0.9 + i * 0.3
    if ts < T['irisClose'] + 0.2: add(pluck(nt(m), 0.6, 0.25, 0.4), ts, 0.045, 0.2 * np.sin(i))
# ── one-shots ──
for e in ev:
    k_, te = e['k'], e['t']
    if k_ == 'pop': add(sine_sweep(300, 900, 0.09, dec=0.05), te, 0.28)
    elif k_ == 'bubble': add(sine_sweep(500, 1200, 0.07, dec=0.035), te, 0.14, 0.2)
    elif k_ == 'word': add(bandnoise(0.02, 0.3, 0.95) * env(0.02, 0.001, 0.006), te, 0.035, 0.1)
    elif k_ == 'scribble':
        d = 0.35; s = bandnoise(d, 0.15, 0.7) * (0.6 + 0.4 * np.sin(2 * np.pi * 14 * tt(d))) * np.minimum(1, (d - tt(d)) / 0.05)
        add(s, te + 0.2, 0.05, -0.4)
    elif k_ == 'ding':
        for i, m in enumerate([88, 95]): add(bell(nt(m), 0.8, 0.3), te + i * 0.07, 0.07, 0.3)
    elif k_ == 'cut': add(bandnoise(0.12, 0.05, 0.4) * env(0.12, 0.005, 0.04), te, 0.08)
    elif k_ == 'sizzle':
        d = T['harpUp'] - te + 0.3; s = bandnoise(d, 0.35, 0.95)
        crack = (rs.random(len(s)) < 0.0009).astype(float); crack = lp(crack, 0.5) * 40
        e_ = np.minimum(1, tt(d) / 0.4) * np.minimum(1, (d - tt(d)) / 0.3) * (0.6 + 0.4 * np.minimum(1, tt(d) / 1.2))
        add((s * 0.5 + crack * s) * e_, te, 0.05, 0.4)
    elif k_ == 'sniff':
        for i in range(2): add(bandnoise(0.1, 0.2, 0.7) * np.sin(np.pi * tt(0.1) / 0.1), te + i * 0.17, 0.08, 0.1)
    elif k_ == 'huh': add(sine_sweep(420, 640, 0.18) * 0.8, te, 0.07); add(sine_sweep(840, 1280, 0.18), te, 0.02)
    elif k_ == 'gasp':
        add(bandnoise(0.2, 0.1, 0.6) * np.sin(np.pi * tt(0.2) / 0.2) ** 0.5, te, 0.1); add(sine_sweep(700, 1500, 0.12, dec=0.06), te + 0.02, 0.06)
    elif k_ == 'scratch':
        d = 0.3; t = tt(d); f = 300 + 900 * np.abs(np.sin(2 * np.pi * 5.5 * t)); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 + bandnoise(d, 0.1, 0.8) * 0.8
        add(s * np.minimum(1, (d - t) / 0.05), te - 0.12, 0.12)
    elif k_ == 'zoom':
        d = 0.16; t = tt(d); add(bandnoise(d, 0.05, 0.6) * (t / d) ** 2 * np.minimum(1, (d - t) / 0.01), te - d + 0.03, 0.22, -0.1)
        add(noise(0.05) * env(0.05, 0.001, 0.015), te, 0.12)
    elif k_ == 'sting':
        for i, m in enumerate([38, 37]):
            d = 0.5 if i else 0.25; t = tt(d); s = np.sign(np.sin(2 * np.pi * nt(m) * t)) * 0.5 + np.sin(2 * np.pi * nt(m) * t)
            add(lp(s, 0.08) * env(d, 0.005, 0.3 if i else 0.15), te + i * 0.26, 0.28)
    elif k_ == 'shake':
        for i in range(6): add(bandnoise(0.04, 0.3, 0.9) * env(0.04, 0.001, 0.01), te + i * 0.07, 0.05, (-1) ** i * 0.4)
    elif k_ in ('harpUp', 'harpDown'):
        ms = [60, 62, 64, 67, 69, 72, 74, 76, 79, 81, 84, 86, 88, 91]
        if k_ == 'harpDown': ms = ms[::-1]
        for i, m in enumerate(ms): add(pluck(nt(m), 0.9, 0.35, 0.3), te + i * 0.026, 0.05, -0.5 + i / len(ms))
    elif k_ == 'rattle':
        r2 = np.random.default_rng(5)
        for i in range(14):
            ts = te + 0.1 + i * 0.05 + r2.random() * 0.03; f = 2500 + r2.random() * 2500
            add(np.sin(2 * np.pi * f * tt(0.05)) * env(0.05, 0.001, 0.01) + 0.5 * bandnoise(0.05, 0.4, 0.95) * env(0.05, 0.001, 0.006), ts, 0.04, 0.4)
    elif k_ == 'beep':
        d = 0.15; t = tt(d); s = np.sign(np.sin(2 * np.pi * 3150 * t)) * 0.5 + np.sin(2 * np.pi * 3150 * t) * 0.5
        add(lp(s, 0.5) * np.minimum(1, t / 0.003) * np.minimum(1, (d - t) / 0.004), te, 0.11)
    elif k_ == 'womp':
        for i, (m0, m1) in enumerate([(58, 57), (55, 51)]):
            d = 0.32 if i == 0 else 0.6; t = tt(d); f = nt(m0) * (nt(m1) / nt(m0)) ** (t / d)
            ph = 2 * np.pi * np.cumsum(f * (1 + 0.01 * np.sin(2 * np.pi * 5 * t))) / SR
            s = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)
            add(lp(s, 0.12) * env(d, 0.03, d * 0.9), te + 0.1 + i * 0.36, 0.11)
    elif k_ == 'iris':
        d = T['irisClose'] - te + 0.3; add(sine_sweep(1500, 700, d, curve=1.2) * np.minimum(1, tt(d) / 0.05), te, 0.035)
    elif k_ == 'irisClose':
        add(sine_sweep(900, 180, 0.3, dec=0.2), te, 0.07); add(sine_sweep(160, 70, 0.15, dec=0.08), te + 0.28, 0.2)
# master: fade in/out, soft limiter
fi = int(0.03 * SR); fo = int(0.25 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.8) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
