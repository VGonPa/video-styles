# events.json → audio.wav (48 kHz stereo, 10 s), all synthesized, no samples.
# Saturday-morning cartoon sound design: a bouncy square-wave title jingle, snoring, a twin-bell alarm,
# slide-whistle zips, skid screeches, pot-hop boings, a xylophone chase vamp, a car-horn "take" with a
# cymbal crash, a ta-da, iris "bwoop" and the classic two-note button ending.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(113)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def sweep(f): return np.sin(2 * np.pi * np.cumsum(f) / SR)
def sq(f, duty=.5):
    ph = (np.cumsum(f) / SR) % 1; return np.where(ph < duty, 1.0, -1.0)
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def env(d, a=.005, r=.08):
    t = tt(d); return np.minimum(1, t / a) * np.minimum(1, np.maximum(0, d - t) / r)
def note(m, d, kind='sq', g=1.0):
    t = tt(d); f = np.full(len(t), nt(m)) * (1 + .004 * np.sin(2 * np.pi * 6 * t))
    if kind == 'sq': s = band(sq(f, .3), 60, 5000) * .6 + .4 * sweep(f)
    elif kind == 'xy':  # xylophone: bright partials, fast decay
        s = sum(a * np.sin(2 * np.pi * nt(m) * h * t) * np.exp(-t * k) for h, a, k in [(1, 1, 9), (3.93, .45, 20), (9.3, .2, 40)])
    elif kind == 'bass': s = band(sq(f, .5), 40, 900)
    else: s = sweep(f)
    return s * env(d, .004, min(.06, d * .4)) * g
def noise(d, lo, hi): return norm(band(rs.standard_normal(int(d * SR)), lo, hi))
def boing(f0=160, d=.45):
    t = tt(d); f = f0 * (1 + .45 * np.sin(2 * np.pi * 16 * t) * np.exp(-t * 5)) * (1 + .9 * t / d)
    return sweep(f) * np.exp(-t / (d * .4))
def slide(f0, f1, d):  # slide whistle
    t = tt(d); f = f0 * (f1 / f0) ** (t / d) * (1 + .01 * np.sin(2 * np.pi * 7 * t))
    return (sweep(f) + .15 * sweep(2 * f)) * np.sin(np.pi * t / d) ** .5
def whoosh(d, lo=200, hi=3000):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = lo + hi * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
def bellring(d, g=1.0):  # twin-bell alarm: hammer at 22 Hz alternating two bells
    t = tt(d); out = np.zeros(len(t)); hit = int(SR / 22); k = 0
    for i0 in range(0, len(t), hit):
        f = 2350 if k % 2 else 2780; tl = tt(min(.12, (len(t) - i0) / SR))
        s = (np.sin(2 * np.pi * f * tl) + .5 * np.sin(2 * np.pi * f * 2.7 * tl) + .25 * np.sin(2 * np.pi * f * .5 * tl)) * np.exp(-tl * 30)
        n = min(len(s), len(t) - i0); out[i0:i0 + n] += s[:n]; k += 1
    return norm(out) * np.minimum(1, t / .01) * np.minimum(1, (d - t) / .03) * g
def horn(d=.6):  # "a-OO-ga": two-segment nasal horn
    t = tt(d); f = np.where(t < .18, 190 + 60 * t / .18, 250 - 40 * (t - .18) / (d - .18))
    ph = np.cumsum(f) / SR; saw = 2 * (ph % 1) - 1
    y = band(saw, 300, 1600) + .6 * band(saw, 2000, 3200)
    return norm(y) * np.minimum(1, t / .02) * np.minimum(1, (d - t) / .08)
def crash(d=1.2): t = tt(d); return noise(d, 3000, 14000) * np.exp(-t / .35)

# ---- title jingle (0.1–1.45): bouncy square melody + bass, 168 bpm eighths
e8 = 60 / 168 / 2
mel = [(72, 1), (76, 1), (79, 1), (84, 2), (79, 1), (81, 1), (83, 1), (84, 3)]
tb = .12
for m, n in mel:
    add(note(m, e8 * n * .92, 'sq'), tb, .09, .15); add(note(m - 12, e8 * n * .92, 'xy'), tb, .08, -.2); tb += e8 * n
for i, m in enumerate([48, 55, 52, 55, 53, 55, 48, 43]):
    add(note(m, e8 * .9, 'bass'), .12 + i * e8 * 1.4, .12)
# ---- chase vamp (3.9–5.6): xylophone ostinato + walking bass, 176 bpm sixteenths
s16 = 60 / 176 / 4
riff = [67, 70, 72, 70, 67, 70, 74, 72, 67, 70, 72, 70, 75, 74, 72, 70]
k = 0; tb = 3.92
while tb < 5.5:
    fade = 1 if tb < 5.15 else max(0, 1 - (tb - 5.15) / .35)
    add(note(riff[k % 16], s16 * 1.8, 'xy'), tb, .09 * fade, .3 * np.sin(k))
    if k % 4 == 0: add(note([43, 43, 46, 41][(k // 4) % 4], s16 * 3.5, 'bass'), tb, .14 * fade)
    if k % 2 == 1: add(noise(.03, 5000, 12000) * np.exp(-tt(.03) / .008), tb, .05 * fade, .4)
    k += 1; tb += s16

for e in json.load(open('events.json')):
    k, te, v, d = e['k'], e['t'], e.get('v', 1.0), e.get('d', .3)
    if k == 'sting': add(crash(.8), te, .08); add(boing(120, .5), te, .1)
    elif k == 'plink': add(note(79 + [0, 4, 7, 12][v % 4], .18, 'xy'), te, .06, -.6 + .1 * v)
    elif k == 'pop': t = tt(.1); add(sweep(500 * (1 + 2 * np.exp(-t * 50))) * np.exp(-t / .03), te, .2)
    elif k == 'ribbon': add(slide(500, 1400, .25), te, .06)
    elif k == 'spin': add(whoosh(d, 300, 3500), te, .22); add(slide(1400, 300, d), te, .05)
    elif k == 'snore':
        for i in range(2):
            t = tt(.35); add(norm(band(rs.standard_normal(len(t)), 80, 500)) * np.sin(np.pi * t / .35) * (1 + .5 * sq(np.full(len(t), 32))), te + i * .5, .05)
    elif k == 'ring': add(bellring(d), te, .16 * v, -.25)
    elif k == 'zip': add(slide(400, 2400 * v, .16), te, .11, .3); add(whoosh(.2, 400, 4000), te, .12)
    elif k == 'skid': t = tt(d); add(norm(band(rs.standard_normal(len(t)), 1800, 4200)) * (.6 + .4 * np.sin(2 * np.pi * 40 * t)) * np.exp(-t / (d * .8)), te, .08); add(sweep(np.full(len(t), 1650) * (1 - .15 * t / d)) * np.exp(-t / (d * .7)), te, .05)
    elif k == 'boing': add(boing(150 * v, .5), te, .16)
    elif k == 'gulp': t = tt(.18); add(sweep(300 + 500 * (t / .18) ** 2) * np.sin(np.pi * t / .18), te, .12)
    elif k == 'swish': add(whoosh(.3, 400, 5000), te, .3)
    elif k == 'hop': t = tt(.16); add(sweep(110 * (1 + 1.5 * np.exp(-t * 40))) * np.exp(-t / .05), te, .22); add(boing(260, .22), te, .04)
    elif k == 'toss': add(slide(600, 1500, .35), te, .07, .4)
    elif k == 'clang': t = tt(.5); add(sum(np.sin(2 * np.pi * f * t) for f in (820, 1330, 2210)) * np.exp(-t / .12) / 3, te, .15, .2)
    elif k == 'paper': add(noise(.12, 1500, 8000) * np.exp(-tt(.12) / .04), te, .1); add(slide(700, 1600, .12), te + .02, .05)
    elif k == 'take': add(horn(.6), te, .28); add(horn(.5), te + .62, .16)
    elif k == 'crash': add(crash(1.2), te, .12); t = tt(.3); add(sweep(60 * (1 + 3 * np.exp(-t * 30))) * np.exp(-t / .1), te, .4)
    elif k == 'click': add(noise(.02, 2000, 9000) * np.exp(-tt(.02) / .003), te, .3); add(noise(.02, 2000, 7000) * np.exp(-tt(.02) / .003), te + .05, .18)
    elif k == 'iris': add(slide(900, 180, d), te, .06)
    elif k == 'button':  # "bum-BUM!"
        add(note(55, .14, 'sq'), te, .12); add(note(43, .14, 'bass'), te, .15)
        add(note(60, .5, 'sq'), te + .2, .14); add(note(48, .5, 'bass'), te + .2, .18); add(note(72, .5, 'xy'), te + .2, .08)
# ta-da after the grin
for i, m in enumerate([72, 76, 79, 84]): add(note(m, .4 - i * .03, 'sq'), 6.95 + i * .04, .05, -.3 + .2 * i)

fi = int(0.05 * SR); fo = int(0.35 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo)
st = np.stack([L, R], 1); st = np.tanh(st * 1.2) * 0.9
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
