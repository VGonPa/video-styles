# events.json → audio.wav (48 kHz stereo, 10 s), all synthesized
# pen scribbles, footsteps/thuds, whooshes, sword swishes, metallic clangs + shatter, star twinkles/chimes,
# rubbery ramp "boing", bar creak, stretch squeak, pop, fist-bump tap, light percussive bed, closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(81)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def nrm(x): return x / (np.abs(x).max() + 1e-9)
def noise(d, lo, hi): return nrm(band(rs.standard_normal(int(d * SR)), lo, hi))
def pen(d):
    t = tt(d); n = noise(d, 1800, 6500); am = np.abs(band(rs.standard_normal(len(t)), 8, 45)); am = nrm(am)
    return n * (.4 + .6 * am) * np.minimum(1, t / .02) * np.minimum(1, (d - t) / .03)
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 300 + 2400 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return nrm(y) * np.sin(np.pi * t / d) ** 1.5
def swish():
    d = .16; t = tt(d); return noise(d, 2500, 9000) * np.sin(np.pi * t / d) ** 2 * np.exp(-t / .09)
def step(v):
    t = tt(.08); return (np.sin(2 * np.pi * (140 + 30 * rs.random()) * t) * np.exp(-t / .018) + .5 * noise(.08, 400, 3000) * np.exp(-t / .008)) * v
def thud():
    t = tt(.3); f = 110 * np.exp(-t * 9) + 50
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .07) + .4 * noise(.3, 200, 2500) * np.exp(-t / .02)
def skid(d):
    t = tt(d); return noise(d, 700, 5000) * np.exp(-t / (d * .6)) * np.minimum(1, t / .01)
def clang(big):
    d = 1.4 if big else .9; t = tt(d); s = np.zeros_like(t)
    for f, a, dec in [(523, 1, .5), (1187, .7, .35), (1812, .5, .25), (2633, .4, .18), (3410, .3, .12), (777, .5, .45)]:
        s += a * np.sin(2 * np.pi * f * (1.0 if not big else .82) * t + rs.random() * 6) * np.exp(-t / (dec * (1.4 if big else 1)))
    hit = noise(d, 1500, 12000) * np.exp(-t / .01)
    low = np.sin(2 * np.pi * 70 * t) * np.exp(-t / .12) * (1.2 if big else .4)
    return nrm(s) * .8 + hit * .7 + low
def shatter():
    out = np.zeros(int(.7 * SR))
    for k in range(14):
        i = int(rs.uniform(0, .5) * SR); f = rs.uniform(2500, 6000); t = tt(.12)
        g = np.sin(2 * np.pi * f * t) * np.exp(-t / .025) * rs.uniform(.3, 1); n = min(len(g), len(out) - i); out[i:i + n] += g[:n]
    return out
def chime(f, d=.8, dec=.25):
    t = tt(d); return sum(a * np.sin(2 * np.pi * f * h * t) for h, a in [(1, 1), (2.01, .35), (3.02, .15)]) * np.exp(-t / dec) * np.minimum(1, t / .003)
def boing(v=1):
    d = .45; t = tt(d); f = 180 + 140 * np.exp(-t * 6) * np.cos(t * 50)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .15) * v
def zip_(d):
    t = tt(d); f = 500 + 2200 * t / d; return (np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * .25 + noise(d, 2000, 8000) * .5) * np.minimum(1, (d - t) / .02 + .2)
def creak():
    d = .3; t = tt(d); f = 260 + 60 * np.sin(t * 20); return np.sin(2 * np.pi * np.cumsum(f) / SR) * (np.sin(2 * np.pi * 38 * t) > 0) * np.sin(np.pi * t / d)
def stretch(d):
    t = tt(d); f = 300 + 500 * t / d + 20 * np.sin(t * 90); return np.sin(2 * np.pi * np.cumsum(f) / SR) * (.6 + .4 * np.sin(t * 60)) * np.minimum(1, t / .03)
def pop():
    t = tt(.2); f = 900 * np.exp(-t * 25) + 200; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .05) + .4 * noise(.2, 1000, 8000) * np.exp(-t / .01)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def tone(freq, d, att=.02, rel=.6):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in [(1, 1), (2, .25), (3, .08)]); return s * np.minimum(1, t / att) * np.minimum(1, (d - t) / rel)
# light bed: soft plucked bass pulse (C major) through the action, dropping out for the impacts
t = np.arange(N) / SR
for i, beat in enumerate(np.arange(1.15, 8.6, .375)):
    if abs(beat - 4.7) < .2 or abs(beat - 5.8) < .3: continue
    m = [36, 36, 43, 41][i % 4]; add(tone(nt(m), .3, .005, .25) * np.exp(-tt(.3) / .12), beat, .07)
    add(noise(.04, 6000, 12000) * np.exp(-tt(.04) / .01), beat + .1875, .02)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0); pan = rs.uniform(-.25, .25)
    if k == 'pen': add(pen(e['d']), te, .09, pan)
    elif k == 'step': add(step(v), te, .16, pan)
    elif k == 'thud': add(thud(), te, .35 * v, pan)
    elif k == 'whoosh': add(whoosh(e['d']), te, .16, pan)
    elif k == 'swish': add(swish(), te, .22, pan)
    elif k == 'skid': add(skid(e['d']), te, .12, pan)
    elif k == 'clang': add(clang(v > 1.2), te, .32 * min(v, 1.3), 0)
    elif k == 'shatter': add(shatter(), te, .12)
    elif k == 'twinkle':
        for j, m in enumerate([84, 88, 91, 96]): add(chime(nt(m)), te + j * .05, .06, .3)
    elif k == 'tink': add(chime(nt(91), .4, .08), te, .08 * v, .2)
    elif k == 'ting': add(chime(nt(96), .7, .2), te, .08 * v, pan)
    elif k == 'blip': add(chime(nt(79 if v > .9 else 83), .25, .05), te, .08)
    elif k == 'boing': add(boing(v), te, .18)
    elif k == 'zip': add(zip_(e['d']), te, .06)
    elif k == 'creak': add(creak(), te, .06)
    elif k == 'stretch': add(stretch(e['d']), te, .07)
    elif k == 'pop': add(pop(), te, .35)
    elif k == 'descend':
        for j, m in enumerate([96, 91, 88, 84, 79]): add(chime(nt(m), .6, .2), te + j * .15, .05, .2 - j * .1)
    elif k == 'rise':
        for j, m in enumerate([72, 76, 79, 84]): add(chime(nt(m), .6, .2), te + j * .09, .05)
    elif k == 'flare': add(whoosh(.5), te - .1, .12); add(chime(nt(84), 1.5, .5), te, .08); add(chime(nt(91), 1.5, .5), te + .02, .06)
    elif k == 'sparkle': add(chime(nt(int(rs.choice([84, 86, 88, 91, 93, 96]))), .35, .08), te, .03 * v * 2, rs.uniform(-.7, .7))
    elif k == 'tap': add(step(1), te, .3); add(chime(nt(88), .5, .12), te, .05)
    elif k == 'chord':
        for j, m in enumerate([60, 64, 67, 72, 76]): add(tone(nt(m), 1.6, .03 + j * .02, 1.0), te + j * .03, .045)
        add(tone(nt(36), 1.6, .02, 1.0), te, .08)
fi = int(.05 * SR); fo = int(.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * .85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
