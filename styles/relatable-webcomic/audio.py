# events.json → audio.wav (48 kHz stereo, 10 s), all synthesized
# a soft plucked "ukulele" arpeggio (bright C for the yes, a droopy A minor for the dread, a held breath for the
# buzz, warm C–Fmaj7 for the cosy ending) + paper pops for the panels, pen scribble, phone buzz + message ding,
# twinkly heart chimes, a sigh, clock ticks, a gasp, a camera swoosh, a sip, a heart-iris slide and a last chime.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(92)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def nrm(x): return x / (np.abs(x).max() + 1e-9)
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def noise(d, lo, hi): return nrm(band(rs.standard_normal(int(d * SR)), lo, hi))
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def pluck(f, d=.8, dec=.22):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (dec / h ** .6)) for h, a in [(1, 1), (2, .45), (3, .2), (4, .1)])
    return s * np.minimum(1, t / .004)
def chime(f, d=1.2):
    t = tt(d); return (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-t / .1)) * np.exp(-t / .35) * np.minimum(1, t / .002)
def pop(f0=520):
    t = tt(.14); f = f0 * np.exp(-t * 22) + f0 * .45; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .035) * np.minimum(1, t / .001)
def paper():
    t = tt(.22); p = np.zeros(len(t)); q = pop(260); p[:len(q)] = q
    return noise(.22, 900, 7000) * np.exp(-t / .04) * .5 + p
def click():
    t = tt(.04); return noise(.04, 1500, 9000) * np.exp(-t / .006)
def scribble(d):
    t = tt(d); am = .55 + .45 * np.abs(np.sin(2 * np.pi * 6.5 * t)); return noise(d, 2500, 9000) * am * np.sin(np.pi * t / d) ** .5
def buzz(d):
    t = tt(d); am = (np.sin(2 * np.pi * 11 * t) > -.2).astype(float); x = np.sign(np.sin(2 * np.pi * 165 * t)) * .5 + np.sin(2 * np.pi * 330 * t) * .3
    return band(x, 80, 1600) * am * np.minimum(1, (d - t) / .02)
def slide(d, f0, f1):
    t = tt(d); f = f0 * (f1 / f0) ** (t / d); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / .01) * np.minimum(1, (d - t) / .04)
def sigh(d):
    t = tt(d); x = rs.standard_normal(len(t)); X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR)
    X *= np.exp(-((fr - 900) / 500) ** 2) + .5 * np.exp(-((fr - 2200) / 600) ** 2); y = nrm(np.fft.irfft(X, len(x)))
    return y * np.sin(np.pi * np.minimum(1, t / d)) ** 1.5 * np.exp(-t / d)
def gasp():
    t = tt(.22); x = noise(.22, 1200, 5000); return x * (t / .22) ** 1.2 * np.minimum(1, (.22 - t) / .02)
def swoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0; fc = 300 + 2600 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return nrm(y) * np.sin(np.pi * t / d) ** 1.5
def slurp(d):
    t = tt(d); am = .5 + .5 * np.sin(2 * np.pi * (8 + 4 * t / d) * t); n = rs.standard_normal(len(t))
    X = np.fft.rfft(n); f = np.fft.rfftfreq(len(n), 1 / SR); X *= np.exp(-((f - 1200) / 600) ** 2) + .3 * np.exp(-((f - 2500) / 500) ** 2)
    return nrm(np.fft.irfft(X, len(n))) * am * np.sin(np.pi * t / d) ** .7
def twinkle(t0, g=.05, base=84):
    for j, m in enumerate([0, 4, 7, 12, 16]): add(chime(nt(base + m), .8), t0 + j * .045, g * (1 - j * .1), -.4 + j * .2)

# ── music: plucked arpeggios (8ths at 0.25 s) ──
def arp(t0, t1, chord, g=.07, step=.25, pat=(0, 1, 2, 3, 2, 1)):
    k = 0; t = t0
    while t < t1 - .05:
        m = chord[pat[k % len(pat)]]; add(pluck(nt(m), .9, .25), t, g * (1.0 if k % 2 == 0 else .75), -.2 + .1 * (k % 3)); t += step; k += 1
    add(pluck(nt(chord[0] - 12), 1.4, .45), t0, g * .9, 0)
C, F, Am, Em, G, Fm7 = [60, 64, 67, 72], [60, 65, 69, 72], [57, 64, 69, 72], [55, 64, 67, 71], [55, 62, 67, 71], [60, 64, 65, 69]
arp(.35, 1.4, C); arp(1.4, 2.5, F, .075)
arp(2.55, 3.55, Am, .05, .33); arp(3.55, 4.5, Em, .045, .33)
arp(4.55, 5.45, G, .04, .5, (0, 2))
arp(6.35, 7.35, C, .07); arp(7.35, 8.35, Fm7, .07); arp(8.35, 9.25, C, .06)

ev = json.load(open('events.json'))
for e in ev:
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'scribble': add(scribble(e['d']), te, .05, -.3)
    elif k == 'panel': add(paper(), te, .22, rs.uniform(-.3, .3))
    elif k == 'tick': add(click(), te, .05, -.4)
    elif k == 'buzz': add(buzz(e['d']), te, .06, -.4)
    elif k == 'ding': add(chime(nt(88), 1.0), te, .08, -.3); add(chime(nt(93), 1.0), te + .09, .07, -.3)
    elif k == 'squish': add(slide(.12, 500, 260), te, .05)
    elif k == 'pop': add(pop(620), te, .18 * v, .2)
    elif k == 'hearts': twinkle(te)
    elif k == 'sigh': add(sigh(e['d']), te, .12, .1)
    elif k == 'clock': add(click(), te, .06, .5)
    elif k == 'gasp': add(gasp(), te - .1, .07); add(slide(.18, 700, 1400), te, .04)
    elif k == 'swoosh': add(swoosh(e['d']), te, .12)
    elif k == 'sip': add(slurp(e['d']), te, .06, .1)
    elif k == 'iris': add(slide(e['d'], 1200, 300), te, .025)
    elif k == 'end': add(chime(nt(84), 1.4), te, .1); add(chime(nt(91), 1.4), te + .08, .07, .2); twinkle(te + .15, .03, 91)
fi = int(.01 * SR); fo = int(.35 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.3) * .85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
