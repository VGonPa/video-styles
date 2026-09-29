# events.json → audio.wav (48 kHz stereo, 10 s)
# city-pop bed (electric-piano maj7 chords, round synth bass, soft brushed hats), engine drone with
# palm pass-by whooshes, flare shimmer, wind in the hair, iris zips, night-city hum, title brass sting + chime.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(85)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); p = 0.0
    for i in range(len(x)): p = (1 - a) * x[i] + a * p; y[i] = p
    return y
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def epiano(f, d):
    t = tt(d); mod = np.sin(2 * np.pi * f * 14 * t) * 1.2 * np.exp(-t / .12)
    s = np.sin(2 * np.pi * f * t + mod) + .25 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / .4)
    return s * np.exp(-t / 1.1) * np.minimum(1, t / .004)
def bass(f, d):
    t = tt(d); s = np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / .08)
    return s * np.exp(-t / .35) * np.minimum(1, t / .003)
def hat():
    t = tt(.08); return band(rs.standard_normal(len(t)), 6000, 14000) * np.exp(-t / .018)
def whoosh(d, lo=200, hi=2600):
    t = tt(d); x = rs.standard_normal(len(t)); fc = lo + hi * np.sin(np.pi * t / d) ** 2
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); p = 0.0
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y / (np.abs(y).max() + 1e-9) * np.sin(np.pi * t / d) ** 1.5
# ── city-pop bed: 100 bpm, Fmaj7 · Em7 · Dm7 · Cmaj7/E, one chord per bar (2.4 s)
beat = 0.6
prog = [[53, 57, 60, 64, 69], [52, 55, 59, 62, 67], [50, 53, 57, 60, 65], [52, 55, 60, 64, 71]]
roots = [41, 40, 38, 40]
for b in range(4):
    t0 = .35 + b * 4 * beat
    for rep, off in enumerate([0, 2.5 * beat]):
        for i, m in enumerate(prog[b]): add(epiano(nt(m), 2.0), t0 + off + i * .012, .045 * (1 if rep == 0 else .7), -.3 + i * .15)
    for k, (off, oc) in enumerate([(0, 0), (1.5, 12), (2, 0), (3, 7), (3.5, 12)]):
        add(bass(nt(roots[b] + oc), .5), t0 + off * beat, .16)
    for k in range(8): add(hat(), t0 + k * beat / 2 + (.02 if k % 2 else 0), .05 if k % 2 else .03, .35)
# ── engine drone (shot A), low-passed saw with held-cel wobble
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'engine':
        d = e['d']; t = tt(d); f = 72 + 6 * np.sin(2 * np.pi * .4 * t)
        ph = np.cumsum(f) / SR; saw = 2 * (ph % 1) - 1
        s = lp(saw + .5 * np.sign(np.sin(2 * np.pi * ph * .5)), 500) * np.minimum(1, t / .3) * np.minimum(1, (d - t) / .15)
        add(s, te, .16)
    elif k == 'pass': add(whoosh(.6, 300, 3000), te, .22, rs.uniform(-.5, .5))
    elif k == 'flare':
        t = tt(.6); s = sum(np.sin(2 * np.pi * nt(m) * t) for m in [84, 88, 91, 96]) * np.minimum(1, t / .4) * np.exp(-np.maximum(0, t - .35) / .1)
        add(s, te, .03); add(whoosh(.5, 800, 5000), te + .1, .12)
    elif k == 'wind':
        d = e['d']; t = tt(d); x = band(rs.standard_normal(len(t)), 250, 2400)
        am = .6 + .4 * np.abs(np.sin(2 * np.pi * 1.1 * t) * np.sin(2 * np.pi * .37 * t))
        add(x / np.abs(x).max() * am * np.minimum(1, t / .3) * np.minimum(1, (d - t) / .3), te, .09, -.2)
    elif k == 'iris':
        t = tt(.45); f = 500 + 1800 * (1 - t / .45) if e.get('v') else 400 + 1800 * t / .45
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / .45); add(s, te, .05); add(whoosh(.45, 400, 3500), te, .1)
    elif k == 'city':
        d = e['d']; t = tt(d); x = lp(rs.standard_normal(len(t)), 300); x /= np.abs(x).max()
        add(x * np.minimum(1, t / .5) * .8, te, .06)
    elif k == 'sting':
        for i, m in enumerate([60, 64, 67, 71, 74, 79]):
            t = tt(2.2); f = nt(m); ph = np.cumsum(f * (1 + .004 * np.sin(2 * np.pi * 5.5 * t))) / SR
            saw = 2 * (ph % 1) - 1; s = lp(saw, 1800) * np.minimum(1, t / .03) * np.exp(-t / .9)
            add(s, te + i * .03, .05, -.4 + i * .16)
        add(bass(nt(36), 1.2), te, .22)
        t = tt(.3); add(band(rs.standard_normal(len(t)), 80, 400) * np.exp(-t / .05), te, .25)
    elif k == 'glint':
        for i, m in enumerate([96, 100, 103, 108]):
            t = tt(1.0); add(np.sin(2 * np.pi * nt(m) * t) * np.exp(-t / .35), te + i * .05, .04, .3)
fi = int(.4 * SR); fo = int(.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * .85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
