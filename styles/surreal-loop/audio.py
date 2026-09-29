# events.json → audio.wav (48 kHz stereo, 10 s), all synthesized.
# music-box bed that detunes and wobbles in the psychedelic middle, slide-whistle fall, boing landings,
# bubble pops for each doubling (rising pitch), spring stilts, shimmer wipe, whooshes, tiny bud pops,
# zoom riser, a synth bleat, a closing chime and a night pad.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(109)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def sweep(f, amp=None):
    ph = 2 * np.pi * np.cumsum(f) / SR; return np.sin(ph)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def pop(f0):
    t = tt(0.12); f = f0 * (1 + 1.6 * np.exp(-t * 60)); return sweep(f) * np.exp(-t / 0.03)
def boing(f0, d=0.45):
    t = tt(d); f = f0 * (1 + .35 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 6)) * (1 + .6 * t / d)
    return sweep(f) * np.exp(-t / (d * .4))
def thud(f0=70, d=.35):
    t = tt(d); f = f0 * (1 + 2 * np.exp(-t * 30)); n = band(rs.standard_normal(len(t)), 80, 900) * np.exp(-t / .02)
    return sweep(f) * np.exp(-t / .09) + .4 * n / (np.abs(n).max() + 1e-9)
def click():
    t = tt(0.02); n = band(rs.standard_normal(len(t)), 2000, 9000) * np.exp(-t / .002); return n / (np.abs(n).max() + 1e-9)
def whoosh(d, lo=200, hi=2600):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = lo + hi * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y / (np.abs(y).max() + 1e-9) * np.sin(np.pi * t / d) ** 1.5
def bell(f, d=1.6):
    t = tt(d); return sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (d * .35 / h ** .5)) for h, a in [(1, 1), (2.76, .35), (5.4, .12)])
def tone(f, d, att=.3, rel=.8, det=0.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * f * h * t * (1 + det * np.sin(2 * np.pi * 3 * t))) for h, a in [(1, 1), (2, .25), (3, .08)])
    return s * np.minimum(1, t / att) * np.minimum(1, np.maximum(0, d - t) / rel)
def baa(d=.55):
    t = tt(d); f = 330 * (1 + .06 * np.sin(2 * np.pi * 9 * t)) * (1 - .12 * t / d)
    ph = 2 * np.pi * np.cumsum(f) / SR; saw = 2 * ((ph / (2 * np.pi)) % 1) - 1
    y = band(saw, 500, 1300) + .5 * band(saw, 2200, 3000) + .3 * saw
    return y / (np.abs(y).max() + 1e-9) * np.minimum(1, t / .04) * np.minimum(1, (d - t) / .2)
# ---- bed: music-box arpeggio (C major → wobbles/detunes in the psychedelic middle), 132 bpm eighths
psy = lambda t: float(np.clip((t - 3.25) / .5, 0, 1) * np.clip((7.95 - t) / .3, 0, 1))
arp = [60, 64, 67, 72, 67, 64, 60, 67, 62, 65, 69, 74, 69, 65, 62, 69]
step = 60 / 132 / 2
k = 0; tb = 0.3
while tb < 9.3:
    m = arp[k % 16] + (12 if 3.3 < tb < 7.9 and k % 2 else 0); p = psy(tb)
    s = bell(nt(m) * (1 + .03 * p * np.sin(k * 1.7)), 1.0)
    if p > 0: s = s + p * .5 * bell(nt(m) * 1.012, 1.0)
    add(s, tb, .055 * (0.6 if tb > 9.0 else 1), .35 * np.sin(k * .9))
    k += 1; tb += step
# low pad: C, then a wobbly chord through the middle
for m, g, p in [(48, .05, -.2), (55, .035, .25)]:
    add(tone(nt(m), 3.0, .4, 1.0), 0.3, g, p)
    add(tone(nt(m + 1), 4.6, .5, .6, det=.012), 3.3, g * .9, -p)
    add(tone(nt(m), 2.2, .3, 1.4), 7.9, g, p)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'fall': t = tt(.47); add(sweep(1800 - 1300 * t / .47) * np.minimum(1, t / .05) * (1 - t / .47) ** .3, te, .06)
    elif k == 'land': add(thud(), te, .5 * v); add(boing(180, .5), te + .01, .12 * v)
    elif k == 'tick': add(click(), te, .25)
    elif k == 'squash': t = tt(.1); add(sweep(420 - 200 * t / .1) * np.exp(-t / .04), te, .05)
    elif k == 'pop': add(pop(nt(72 + 3 * v)), te, .3, (-.3 if v % 2 else .3)); add(pop(nt(79 + 3 * v)), te + .015, .2, (.3 if v % 2 else -.3))
    elif k == 'stilt': add(boing(220 + 60 * v, .35), te, .09, -.6 + .24 * v)
    elif k == 'wipe':
        for i in range(10): add(bell(nt(72 + [0, 2, 4, 7, 9][i % 5] + 12 * (i // 5)), .8), te + i * .045, .05, -.5 + i * .1)
    elif k == 'swirl': add(whoosh(e['d']), te, .18)
    elif k == 'bud': add(pop(nt(84 + (v * 5) % 12)), te, .09, np.sin(v * 1.3) * .6)
    elif k == 'patter': add(thud(160, .12), te, .08, rs.uniform(-.5, .5)); add(click(), te, .06)
    elif k == 'thud': add(thud(55, .6), te, .6)
    elif k == 'boing': add(boing(110, .7), te, .16)
    elif k == 'blink': add(click(), te, .18)
    elif k == 'bulge': t = tt(.5); add(sweep(200 + 500 * (t / .5) ** 2 + 30 * np.sin(2 * np.pi * 18 * t)) * np.minimum(1, t / .03) * np.exp(-t / .3), te, .12)
    elif k == 'zoom':
        d = e['d']; t = tt(d); ww = whoosh(d, 150, 3500) * (t / d) ** .8
        rise = sweep(120 * 2 ** (4 * (t / d) ** 1.5)) * np.sin(np.pi * t / d) ** 2
        add(ww, te, .22); add(rise, te, .06)
    elif k == 'baa': add(baa(), te, .22, .1)
    elif k == 'chord':
        for i, m in enumerate([72, 76, 79, 84]): add(bell(nt(m), 2.0), te + i * .05, .07, -.3 + .2 * i)
    elif k == 'night': add(tone(nt(52), 1.0, .5, .5), te, .04); add(tone(nt(59), 1.0, .5, .5), te, .03, .3)
fi = int(0.2 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
