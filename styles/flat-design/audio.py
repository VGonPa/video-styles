# events.json → audio.wav (48 kHz stereo, 9.5 s) for flat-design.
# A bright 2014 product-video bed at 120 bpm: plucked ukulele-style strums over I–vi–IV–V–I (C Am F G C),
# a low marimba bass, soft claps and a shaker; on top, the picture's cues: marimba-and-bloop pops for every
# shape that lands (pitches snapped to the chord of the moment), typing ticks, a whoosh for the circle wipe,
# low thuds as the hills land, smoke puffs, a rocket rumble that rises with the climb, glockenspiel twinkles
# for the stars, panel swooshes, a button click and a final major chord. Everything is synthesised.
import json, wave, numpy as np

SR, DUR, BPM = 48000, 9.5, 120.0
BEAT = 60.0 / BPM
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(141)
nt = lambda m: 440.0 * 2 ** ((m - 69) / 12)
tt = lambda d: np.arange(int(d * SR)) / SR


def add(sig, t, g=1.0, pan=0.0):
    i = int(round(t * SR)); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414
        R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414


def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def norm(x): return x / (np.abs(x).max() + 1e-9)


def env_ar(t, a, d): return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


# ── instruments ──
def marimba(f, d=1.0, bright=1.0):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t) * env_ar(t, .002, .32)
    s += .32 * bright * np.sin(2 * np.pi * f * 3.93 * t) * env_ar(t, .001, .05)
    s += .10 * bright * np.sin(2 * np.pi * f * 9.2 * t) * env_ar(t, .001, .015)
    s += .25 * band(rs.standard_normal(len(t)), 800, 5000) * np.exp(-t / .003)
    return s


def pluck(f, d=1.4, bright=1.0):        # plucked nylon string: decaying harmonics, the higher ones die first
    t = tt(d); s = np.zeros_like(t)
    for k in range(1, 14):
        if f * k > 12000: break
        s += (1.0 / k ** 1.0) * bright ** (k - 1) * np.sin(2 * np.pi * f * k * t + rs.uniform(0, 6.28)) * np.exp(-t / (0.55 / k ** 0.8))
    s *= np.minimum(1, t / .003)
    s += .15 * band(rs.standard_normal(len(t)), 2000, 7000) * np.exp(-t / .004)
    return s


def glock(f, d=1.2):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) * env_ar(t, .001, .45) + .35 * np.sin(2 * np.pi * f * 2.76 * t) * env_ar(t, .001, .12)
            + .12 * np.sin(2 * np.pi * f * 5.4 * t) * env_ar(t, .001, .04))


def bloop(f=520, d=.16):                 # the UI "pop": a quick upward pitch flick
    t = tt(d); fr = f * (0.55 + 0.45 * (1 - np.exp(-t / .012)))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * env_ar(t, .001, .045)


def tick(v=1.0):
    t = tt(.04)
    return v * (band(rs.standard_normal(len(t)), 2500, 9000) * np.exp(-t / .0025) + .4 * np.sin(2 * np.pi * 3200 * t) * np.exp(-t / .006))


def noise_sweep(d, f0, f1, env, width=1.6):
    t = tt(d); x = rs.standard_normal(len(t)); out = np.zeros_like(x); K = 14; sl = len(t) // K + 1
    for k in range(K):
        a, b = k * sl, min(len(t), (k + 1) * sl); u = (k + .5) / K; fc = f0 * (f1 / f0) ** u
        out[a:b] = band(x, fc / width, fc * width)[a:b]
    return norm(out) * env(t / d)


def thud(f=70, d=.5):
    t = tt(d); fr = f * (1 + 1.2 * np.exp(-t / .03))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * env_ar(t, .002, .12) + .3 * band(rs.standard_normal(len(t)), 60, 600) * np.exp(-t / .03)


def clap():
    t = tt(.25); n = band(rs.standard_normal(len(t)), 900, 5000); e = np.zeros_like(t)
    for k, o in enumerate((0, .009, .019)): e += (t >= o) * np.exp(-np.maximum(0, t - o) / (.006 if k < 2 else .07))
    return n * e


def shaker():
    t = tt(.07); return band(rs.standard_normal(len(t)), 5000, 12000) * env_ar(t, .012, .018)


# ── harmony: I–vi–IV–V–I, one chord per 4/4 bar (2 s) ──
CHORDS = [(0.0, 'C'), (2.0, 'Am'), (4.0, 'F'), (6.0, 'G'), (8.0, 'C')]
UKE = {'C': [67, 60, 64, 72], 'Am': [69, 60, 64, 69], 'F': [69, 60, 65, 69], 'G': [67, 62, 67, 71]}
ROOT = {'C': 48, 'Am': 45, 'F': 41, 'G': 43}
PCS = {'C': {0, 4, 7}, 'Am': {9, 0, 4}, 'F': {5, 9, 0}, 'G': {7, 11, 2}}


def chord_at(t):
    c = CHORDS[0][1]
    for t0, name in CHORDS:
        if t >= t0 - .06: c = name
    return c


def snap(m, t):                          # nearest chord tone, so every UI note sits in the harmony
    pcs = PCS[chord_at(t)]
    for d in (0, -1, 1, -2, 2):
        if (m + d) % 12 in pcs: return m + d
    return m


def strum(notes, t, v=1.0, up=False, pan=0.0):
    seq = notes[::-1] if up else notes
    for i, m in enumerate(seq):
        add(pluck(nt(m), 1.1, .9) * v, t + i * (.008 if up else .012), .1, pan + (i - 1.5) * .08)


# ── the bed ──
PATTERN = [(0, 1.0, False), (1, .7, False), (1.5, .55, True), (2.5, .55, True), (3, .8, False), (3.5, .5, True)]
for bar in range(5):
    t0 = bar * 4 * BEAT
    if t0 >= 8.0: break
    name = chord_at(t0 + .1)
    for b, v, up in PATTERN:
        tb = t0 + b * BEAT
        if tb < .45: continue                                     # bar 1 enters after the first pop
        strum(UKE[name], tb, v, up, -.15)
    for b in (0, 2):
        tb = t0 + b * BEAT
        if tb >= .4: add(marimba(nt(ROOT[name]), 1.1, .5), tb, .2, .1)
    if bar >= 1:
        for b in (1, 3): add(clap(), t0 + b * BEAT, .11, .2)
        for k in range(8): add(shaker(), t0 + k * BEAT / 2 + .01, .07 * (1 if k % 2 else .6), .35)

# ── the picture's cues ──
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'pop':
        m = snap(e['n'], te)
        add(marimba(nt(m), .9), te, .26 * v, rs.uniform(-.3, .3)); add(bloop(nt(m) / 2), te, .2 * v)
    elif k == 'blip':
        add(bloop(nt(snap(e['n'], te)) / 2, .12), te, .16 * v, rs.uniform(-.4, .4))
    elif k == 'tick': add(tick(), te, .07 * v, rs.uniform(-.25, .25))
    elif k == 'whoosh': add(noise_sweep(e['d'], 300, 5000, lambda u: np.sin(np.pi * u) ** 1.5), te, .22, .2)
    elif k == 'thud': add(thud(nt(snap(e['n'], te)) / 2 if e['n'] > 45 else 60), te, .34)
    elif k == 'rise':
        t = tt(e['d'] + .1); fr = 300 + 900 * np.clip(t / e['d'], 0, 1) ** 1.5
        add(np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.minimum(1, t / .02) * np.exp(-np.maximum(0, t - e['d']) / .04), te, .06)
    elif k == 'puff':
        for i in range(6): add(noise_sweep(.45, 900, 300, lambda u: (1 - u) ** 2 * np.minimum(1, u * 30)), te + i * .035, .07, (-1) ** i * .4)
    elif k == 'launch':
        add(thud(42, 1.2), te, .45); add(noise_sweep(.9, 2500, 400, lambda u: np.exp(-u * 3) * np.minimum(1, u * 40)), te, .22)
    elif k == 'rumble':
        d = e['d']; t = tt(d); x = rs.standard_normal(len(t)); u = t / d
        low = band(x, 30, 260); mid = band(x, 200, 1500)
        sw = np.minimum(1, u / .08) * (1 - np.clip((u - .82) / .18, 0, 1)) ** 2
        rumble = norm(low) * (.7 + .3 * u) + .4 * norm(mid) * u ** 1.5 + .35 * np.sin(2 * np.pi * (45 + 25 * u) * t)
        add(rumble * sw, te, .2)
    elif k == 'twinkle':
        m = snap(e['n'], te); add(glock(nt(m)), te, .11, rs.uniform(-.6, .6))
    elif k == 'zoom': add(noise_sweep(.5, 400, 7000, lambda u: u ** 2 * (1 - u) * 6), te, .2, 0)
    elif k == 'swoosh':
        add(noise_sweep(.34, 600, 3500, lambda u: np.sin(np.pi * u) ** 2), te, .17 * v, .5 - .3 * (1 - v) * 5)
    elif k == 'swish': add(noise_sweep(.3, 1500, 4500, lambda u: np.sin(np.pi * u) ** 2), te, .09)
    elif k == 'slide': add(noise_sweep(.3, 800, 2500, lambda u: np.sin(np.pi * u) ** 2), te, .07)
    elif k == 'click':
        c = tick(1.0); add(c + .6 * thud(180, .04)[:len(c)], te, .3); add(tick(.7), te + .11, .2)
    elif k == 'chord':
        for i, m in enumerate([60, 64, 67, 72]): add(pluck(nt(m), 1.6, .8), te + i * .014, .13, -.3 + i * .2)
        for m in (36, 48): add(marimba(nt(m), 1.4, .4), te, .3)
        for i, m in enumerate([72, 76, 79]): add(marimba(nt(m), 1.2), te + .02 * i, .14, -.3 + .3 * i)
        for i, m in enumerate([84, 88, 91, 96]): add(glock(nt(m), 1.4), te + .06 + .07 * i, .07, -.4 + .27 * i)

# fades, gentle bus glue, write
fi, fo = int(.02 * SR), int(.5 * SR)
for ch in (L, R):
    ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.6
st = np.stack([L, R], 1)
st = np.tanh(st * 1.25) * .84
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', round(float(np.abs(st).max()), 3), round(float(np.sqrt((st ** 2).mean())), 4))
