# events.json → audio.wav (48 kHz stereo, 9.5 s): a lo-fi cosy bed on a 100 bpm grid.
# Kalimba motif + soft pad chords (F maj7 → D m7 → B♭ maj7 → C6 → F maj9), dusty kick/snare/hat, vinyl crackle;
# confetti pops, a watering-can trickle, a growing "bwoop", the leaf whoosh (left → right), bicycle ticking,
# a two-strike bike bell, a soft brake, the parcel "boop", the iris swish, a cardboard thud, the notification
# ding and a final warm chord. Everything is synthesised; nothing is sampled.
import json, wave, numpy as np
SR, DUR = 48000, 9.5
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(143)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def env_ad(t, a, d): return np.minimum(1, t / a) * np.exp(-np.maximum(0, t - a) / d)
def kal(f, d=1.6):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / .9) + .3 * np.sin(2 * np.pi * 2.01 * f * t) * np.exp(-t / .22) \
        + .22 * np.sin(2 * np.pi * 5.93 * f * t) * np.exp(-t / .05)
    s += .15 * band(rs.standard_normal(len(t)), 1500, 7000) * np.exp(-t / .004)
    return s * np.minimum(1, t / .002)
def pad(notes, d):
    t = tt(d); s = np.zeros_like(t)
    for m in notes:
        f = nt(m)
        for k in range(1, 6):
            for det in (-.0025, .0025):
                s += np.sin(2 * np.pi * f * k * (1 + det) * t + k) / (k * k)
    e = np.minimum(1, t / .5) * np.minimum(1, (d - t) / .7)
    return s * e * (1 + .12 * np.sin(2 * np.pi * .7 * t))
def bass(f, d=.55):
    t = tt(d); return (np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t)) * env_ad(t, .008, .28)
def kick():
    t = tt(.35); f = 48 + 70 * np.exp(-t * 28); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .16)
def snare():
    t = tt(.25); return .6 * band(rs.standard_normal(len(t)), 900, 6000) * np.exp(-t / .07) + .4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / .05)
def hat():
    t = tt(.06); return band(rs.standard_normal(len(t)), 6000, 12000) * np.exp(-t / .018)
def pop(f):
    t = tt(.12); return np.sin(2 * np.pi * np.cumsum(f * (1.6 - .6 * np.minimum(1, t / .05))) / SR) * np.exp(-t / .03)
def trickle(d):
    t = tt(d); x = band(rs.standard_normal(len(t)), 1800, 7000)
    am = np.abs(band(rs.standard_normal(len(t)), 2, 30)); am = am / (am.max() + 1e-9)
    s = norm(x) * (.35 + .65 * am) * np.minimum(1, t / .08) * np.minimum(1, (d - t) / .15)
    for _ in range(int(d * 26)):   # droplet blips
        t0 = rs.uniform(0, d - .05); f0 = rs.uniform(1300, 3200); i0 = int(t0 * SR); tb = tt(.04)
        b = np.sin(2 * np.pi * np.cumsum(f0 * (1 + 1.2 * tb / .04)) / SR) * np.exp(-tb / .01)
        s[i0:i0 + len(b)] += .5 * b[:len(s) - i0]
    return s
def bwoop(d):
    t = tt(d); f = 260 * 2 ** (1.6 * (t / d) ** .8) * (1 + .03 * np.sin(2 * np.pi * 7 * t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** .6
def sweep(d, f0, f1, f2, q=.5):
    t = tt(d); x = rs.standard_normal(len(t)); out = np.zeros_like(x); K = 14; n = len(t) // K + 1
    for k in range(K):
        u = k / (K - 1); fc = f0 * (f1 / f0) ** (2 * u) if u < .5 else f1 * (f2 / f1) ** (2 * u - 1)
        a, b = k * n, min(len(t), (k + 1) * n); out[a:b] = band(x, fc * (1 - q), fc * (1 + q))[a:b]
    return norm(out) * np.sin(np.pi * t / d) ** 1.4
def click():
    t = tt(.012); return band(rs.standard_normal(len(t)), 2500, 8000) * np.exp(-t / .002)
def bell(f=1980):
    t = tt(1.2); s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / dd) for r, a, dd in [(1, 1, .7), (2.76, .5, .3), (5.4, .25, .12), (8.93, .12, .06)])
    return s * (1 + .3 * np.sin(2 * np.pi * 28 * t) * np.exp(-t / .3)) * np.minimum(1, t / .001)
def boop():
    t = tt(.25); f = 260 + 520 * np.minimum(1, t / .12); return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_ad(t, .005, .08)
def thud():
    t = tt(.4); f = 55 + 40 * np.exp(-t * 20)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .12) + .5 * band(rs.standard_normal(len(t)), 200, 1600) * np.exp(-t / .035)
def ding(f):
    t = tt(1.3); return (np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t) * np.exp(-t / .2)) * env_ad(t, .002, .55)
# bed: chords on 2.4 s bars from 0.2 s, bass on beats 1 and 3, vinyl crackle + hiss
BARS = [(.2, [53, 57, 60, 64], 41), (2.6, [50, 57, 60, 65], 38), (5.0, [58, 62, 65, 69], 34), (7.4, [55, 60, 64, 69], 36)]
for i, (t0, notes, root) in enumerate(BARS):
    d = (BARS[i + 1][0] if i + 1 < len(BARS) else 8.6) - t0 + .5
    add(norm(pad(notes, d)), t0 - .15, .055, (-.2, .2, -.1, .1)[i])
    for b in (0, 1.2):
        if t0 + b < 8.6: add(bass(nt(root + 12)), t0 + b, .16)
hiss = band(rs.standard_normal(N), 3000, 9000); L += norm(hiss) * .006; R += norm(np.roll(hiss, 977)) * .006
for _ in range(70):
    i = rs.integers(0, N - 400); c = band(rs.standard_normal(400), 800, 6000) * np.exp(-np.arange(400) / 60)
    (L if rs.random() < .5 else R)[i:i + 400] += c * rs.uniform(.01, .03)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'kal': add(kal(nt(e['n'])), te, .2, float(np.clip((e['n'] - 75) / 14, -.5, .5)))
    elif k == 'kick': add(kick(), te, .32)
    elif k == 'snare': add(snare(), te, .09)
    elif k == 'hat': add(hat(), te, .05 * v, .25)
    elif k == 'pop': add(pop(rs.uniform(500, 900)), te, .07 * v, rs.uniform(-.6, .6))
    elif k == 'water': add(trickle(e['d']), te, .09, .1)
    elif k == 'grow': add(bwoop(e['d']), te, .14, .05)
    elif k == 'whoosh':
        s = sweep(e['d'], 250, 2200, 500); n = len(s); pan = np.linspace(-.8, .8, n)
        i = int(te * SR); m = min(n, N - i); L[i:i + m] += s[:m] * .3 * np.sqrt(.5 - pan[:m] / 2) * 1.414; R[i:i + m] += s[:m] * .3 * np.sqrt(.5 + pan[:m] / 2) * 1.414
    elif k == 'tick':
        t = te; d = e['d']
        while t < te + d:
            u = (t - te) / d; rate = 11 * (1 - .75 * max(0, (u - .82) / .18))
            add(click(), t, .06 * min(1, (t - te) / .3), .1); t += 1 / max(2, rate)
    elif k == 'bell': add(bell(), te, .16 * v, .3)
    elif k == 'brake':
        t = tt(e['d']); s = band(rs.standard_normal(len(t)), 2000, 6000) * np.sin(np.pi * t / e['d']) ** 2
        s += .4 * np.sin(2 * np.pi * (2700 + 60 * np.sin(2 * np.pi * 9 * t)) * t) * np.sin(np.pi * t / e['d']) ** 3
        add(norm(s), te, .045, .2)
    elif k == 'boop': add(boop(), te, .2)
    elif k == 'swish': add(sweep(e['d'], 400, 3000, 700, .4), te, .16)
    elif k == 'thud': add(thud(), te, .4)
    elif k == 'ding': add(ding(nt(88)), te, .17, .15); add(ding(nt(93)), te + .13, .17, .15)
    elif k == 'chord':
        for i, m in enumerate([53, 57, 64, 67, 72, 76]): add(kal(nt(m), 2.2), te + i * .06, .14, -.4 + i * .16)
        add(norm(pad([53, 57, 64, 67, 72], DUR - te + .2)), te - .1, .07)
fi = int(.15 * SR); fo = int(.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.6
st = np.stack([L, R], 1); st = np.tanh(st * 1.25) * .82
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
