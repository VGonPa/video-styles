# events.json → audio.wav (48 kHz stereo, 10 s)
# soft space pad, word pops, a glassy shimmer as the Moon vanishes, zoom whooshes, sea swells that shrink with the tides,
# crickets and tiny footsteps at night, a lantern tinkle, a wobbling "wah" for the axis, icon bloops, closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(21)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def norm(x): return x / (np.abs(x).max() + 1e-9)
def tt(d): return np.arange(int(d * SR)) / SR
def env(t, att, dec): return np.minimum(1, t / att) * np.exp(-t / dec)
def sweep(f0, f1, d, dec, att=0.004):
    t = tt(d); f = f0 * (f1 / f0) ** (t / d); return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(t, att, dec)
def tone(freq, d, att=0.4, rel=1.0, harm=((1, 1), (2, .3), (3, .12))):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in harm)
    return s * np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1)
def bell(f, d=1.2, dec=0.35):
    t = tt(d); return (np.sin(2 * np.pi * f * t) + .45 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / .12) + .25 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / .05)) * env(t, .002, dec)
def noise_swell(d, lo, hi, shape=1.5):
    t = tt(d); return norm(band(rs.standard_normal(len(t)), lo, hi)) * np.sin(np.pi * t / d) ** shape
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    a = np.exp(-2 * np.pi * (250 + 3000 * np.sin(np.pi * t / d) ** 2) / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR
# bed: warm pad (D major add9) that dips at night and swells into the end
bed = np.zeros(N)
for m, g in [(38, .05), (50, .03), (57, .022), (64, .016), (66, .012)]:
    bed += tone(nt(m), DUR, 1.2, 1.0) * g * (1 + .12 * np.sin(2 * np.pi * .3 * t + m))
bed *= 1 - 0.45 * np.clip((t - 5.0) / 0.8, 0, 1) * np.clip((7.2 - t) / 0.5, 0, 1)
L += bed; R += np.roll(bed, 240)
# ocean bed under the coast scenes, loudness following the tidal range
sea = norm(band(rs.standard_normal(N), 120, 1400))
seaEnv = np.clip((t - 2.85) / 0.3, 0, 1) * np.clip((7.3 - t) / 0.4, 0, 1) * (0.35 + 0.65 * np.clip(1 - (t - 3.55) / 1.4, 0, 1))
L += sea * seaEnv * .03; R += np.roll(sea, 999) * seaEnv * .03
# crickets at night
for k in range(26):
    te = 5.45 + k * 0.058 + rs.uniform(0, .03) + (k // 4) * 0.12
    if te > 7.0: break
    c = tone(4300 + rs.uniform(-150, 150), .035, .004, .02, ((1, 1),)) * (0.5 + 0.5 * np.sin(2 * np.pi * 60 * tt(.035)))
    add(c, te, .018, .6 if k % 2 else .4)
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'pop': add(sweep(e['f'], e['f'] * .5, .09, .03), te, .16, rs.uniform(-.25, .25))
    elif k == 'blip': add(sweep(e['f'], e['f'], .12, .035), te, .12, .2)
    elif k == 'rise': add(sweep(90, 160, 1.4, .8, att=.6), te, .22); add(noise_swell(1.4, 200, 1800), te, .05)
    elif k == 'land': add(sweep(120, 70, .35, .1), te, .3)
    elif k == 'suck': add(sweep(300, 1400, .3, .5, att=.25) * np.linspace(0, 1, int(.3 * SR)), te, .12, .4)
    elif k == 'shimmer':
        for i in range(9): add(bell(1400 + i * 260 + rs.uniform(-40, 40), 1.0, .25), te + i * .045, .045, rs.uniform(-.6, .6))
        add(noise_swell(.6, 3000, 9000, 2), te, .05, .4)
    elif k == 'whoosh': add(whoosh(e['d']), te, .25)
    elif k == 'splash': add(noise_swell(.7, 200, 4000, .6) * np.exp(-tt(.7) / .25), te, .18)
    elif k == 'wave': add(noise_swell(1.1, 150, 2200, 2.2), te, .22 * e['v'] + .02, -.3)
    elif k == 'dusk': add(sweep(330, 165, 1.3, .7, att=.3), te, .08)
    elif k == 'step': add(sweep(700, 380, .05, .012), te, .07, .3)
    elif k == 'tinkle': add(bell(2093, 1.0, .3), te, .08, .2); add(bell(2637, 1.0, .3), te + .07, .06, .2)
    elif k == 'wobble':
        d = e['d']; tw = tt(d); f = 180 * (1 + .18 * np.sin(2 * np.pi * tw / .8) * np.minimum(1, tw / .9))
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) + .4 * np.sin(4 * np.pi * np.cumsum(f) / SR)
        add(s * np.minimum(1, tw / .3) * np.clip((d - tw) / .5, 0, 1), te, .07)
    elif k == 'bloop': add(sweep(e['f'], e['f'] * 2.3, .16, .06), te, .2, rs.uniform(-.5, .5))
    elif k == 'chord':
        for i, m in enumerate([62, 66, 69, 74, 76]): add(tone(nt(m), 1.4, .05 + i * .03, 1.0), te + i * .05, .04, (i - 2) * .15)
        add(tone(nt(38), 1.4, .1, 1.0), te, .08)
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
