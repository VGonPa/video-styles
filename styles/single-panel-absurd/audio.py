# events.json -> audio.wav (48 kHz stereo, 10 s). All synthesized:
# a summer pasture (a lark, crickets), a soft felt-pen scratch for every stroke, a brush swish as the washes
# go down, a small car that slows past the fence and drives off, a cow rising with a dry creak, a pencil tally
# mark, a typewriter for each caption (key strikes, a thumped space bar, the carriage bell), a sheet torn
# off the pad, then wind over the ice, a flipper flap and a penguin's two-note bray.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(90)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def addst(l, r, t, g=1.0):
    i = int(t * SR); n = min(len(l), N - i)
    if n > 0: L[i:i + n] += l[:n] * g; R[i:i + n] += r[:n] * g
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def env(t, d, a=.01, r=.05): return np.minimum(1, t / a) * np.clip((d - t) / r, 0, 1)
def scratch(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 1200, 6000))
    grain = 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * (11 + 5 * rs.random()) * t))
    return n * grain * env(t, d, .02, .04)
def swish(d):
    t = tt(d); return norm(band(rs.standard_normal(len(t)), 400, 3000)) * np.sin(np.pi * t / d) ** 2
def key():
    t = tt(.07); c = norm(band(rs.standard_normal(len(t)), 1500, 7000)) * np.exp(-t / .006)
    th = np.sin(2 * np.pi * (180 + 40 * rs.random()) * t) * np.exp(-t / .012)
    return c * .8 + th * .5
def space():
    t = tt(.09); return norm(band(rs.standard_normal(len(t)), 150, 1500)) * np.exp(-t / .012)
def bell():
    t = tt(1.4); f = 2090
    return sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t / (.5 / k)) for k, a in ((1, 1), (2.41, .45), (3.9, .2))) * np.minimum(1, t / .002)
def car(d):
    # engine hum with doppler-ish pitch and pan following x(t) = u + .82 sin(2 pi u)/(2 pi)
    t = tt(d); u = t / d; f = u + .82 * np.sin(2 * np.pi * u) / (2 * np.pi)
    x = -1.2 + 2.4 * f; v = np.gradient(x, t)
    rpm = 42 + 26 * np.clip(v / 2, 0, 1.5) + 6 * np.sin(2 * np.pi * .7 * t)
    ph = 2 * np.cumsum(np.pi * rpm / SR)
    eng = np.sin(ph) + .5 * np.sin(2 * ph + .3) + .3 * np.sin(3 * ph) + .2 * np.sign(np.sin(ph)) * .3
    tyre = norm(band(rs.standard_normal(len(t)), 300, 2500)) * .35
    s = norm(band(eng, 40, 900)) * .8 + tyre
    near = 1 / (1 + (x * 1.4) ** 2)
    s = s * near * env(t, d, .4, .5)
    pan = np.clip(x, -1, 1)
    return s * np.sqrt(.5 - pan / 2) * 1.414, s * np.sqrt(.5 + pan / 2) * 1.414
def creak(d=.5):
    t = tt(d); f = 110 + 60 * t / d
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (0.5 + 0.5 * (rs.random(len(t)) > .6))
    return norm(band(s, 200, 2500)) * np.sin(np.pi * t / d) ** 2
def rip(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 800, 9000))
    crackle = (rs.random(len(t)) > .93).astype(float); crackle = np.convolve(crackle, np.exp(-np.arange(200) / 30), 'same')
    e = np.minimum(1, t / .03) * np.exp(-t / (d * .35))
    flutter = norm(band(rs.standard_normal(len(t)), 200, 2500)) * np.sin(np.pi * t / d) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 18 * t))
    return (n * .6 + norm(crackle) * .7) * e + flutter * .5
def flap():
    t = tt(.18); return norm(band(rs.standard_normal(len(t)), 300, 2200)) * np.sin(np.pi * t / .18) ** 3
def bray(f0, d):
    t = tt(d); f = f0 * (1 + .08 * np.sin(2 * np.pi * 6 * t)) * (1 - .15 * t / d)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = sum(np.sin(k * ph) / k for k in range(1, 12)) * (1 + .5 * np.sin(2 * np.pi * 34 * t))
    return norm(band(s, 300, 3500)) * env(t, d, .02, .08)
def lark(t0, d):
    t = tt(d); out = np.zeros(len(t)); p = 0
    while p < d - .1:
        n = int(.06 * SR); i = int(p * SR); tl = np.arange(n) / SR; f = 3200 + 900 * rs.random() + 1800 * np.sin(2 * np.pi * (14 + 6 * rs.random()) * tl)
        out[i:i + n] += np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tl / .06) ** 2 * (.5 + .5 * rs.random())
        p += .07 + .09 * rs.random()
    return out
t = np.arange(N) / SR
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'pen': add(scratch(max(.04, e['d'])), te, 0.03, rs.uniform(-.25, .25))
    elif k == 'field':
        d = e['d']; tl = tt(d); fe = np.minimum(1, tl / .6) * np.clip((d - tl) / .4, 0, 1)
        air = norm(band(rs.standard_normal(len(tl)), 80, 700)) * fe
        crk = np.sin(2 * np.pi * 4400 * tl) * (np.sin(2 * np.pi * 32 * tl) > .3) * (np.sin(2 * np.pi * 1.6 * tl) > 0) * fe
        add(air, te, .018, -.2); add(np.roll(air, 4001), te, .018, .2); add(crk, te, .006, .55)
        add(lark(te, 1.6) * fe[:int(1.6 * SR)], te + .4, .012, -.5); add(lark(te, 1.2), te + 3.9, .01, -.4)
    elif k == 'ice':
        d = e['d']; tl = tt(d); fe = np.minimum(1, tl / .8) * np.clip((d - tl) / .6, 0, 1)
        w = norm(band(rs.standard_normal(len(tl)), 150, 1400)) * (0.6 + 0.4 * np.sin(2 * np.pi * .35 * tl) ** 2) * fe
        add(w, te, .045, -.3); add(np.roll(w, 9000), te, .045, .3)
    elif k == 'wash': add(swish(.55), te, 0.05, -.1); add(swish(.45), te + .25, 0.035, .15)
    elif k == 'car': l, r = car(e['d']); addst(l, r, te, .10)
    elif k == 'rise': add(creak(.55), te + .05, .04, -.35); add(swish(.5), te + .1, .03, -.3)
    elif k == 'tally': add(scratch(e['d'] + .05) * 1.4, te, .07, -.2)
    elif k == 'key': add(key(), te, .10 + .03 * rs.random(), rs.uniform(-.15, .15))
    elif k == 'space': add(space(), te, .08)
    elif k == 'bell': add(bell(), te, .06, .3)
    elif k == 'tear': add(rip(e['d'] + .3), te, .16, 0)
    elif k == 'flipper': add(flap(), te, .09, -.2)
    elif k == 'squawk': add(bray(520, .22), te + .12, .05, -.2); add(bray(470, .3), te + .38, .05, -.2)
    elif k == 'squawk2': add(bray(610, .18), te, .02, .6)
fi = int(0.25 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 4.5) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
