# events.json → audio.wav (48 kHz stereo, 10 s)
# Belle Epoque salon: a soft string pad in D major / lydian colours, harp arpeggios as the frame draws,
# glassy celesta ticks for the mosaic tiles, a breathy swell as the lily blooms, an airy whoosh on the pull-back,
# a glass clink + pour for the bottle, feather swishes, a chime on the title, a final harp and bell chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(1900)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def bell(f, d=2.2):
    t = tt(d); s = np.zeros_like(t)
    for r, a, dec in [(1, 1, .9), (2.0, .5, .6), (2.76, .35, .4), (5.4, .2, .18), (8.9, .08, .08)]:
        s += a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / dec)
    return s * np.minimum(1, t / .002)
def pluck(f, d=1.2, bright=.5):
    t = tt(d); s = sum((bright ** (h - 1)) * np.sin(2 * np.pi * f * h * t) * np.exp(-t * (2.5 + h * 1.2)) for h in range(1, 6))
    return s * np.minimum(1, t / .003)
def harp(notes, t0, d, g):
    for i, m in enumerate(notes): add(pluck(nt(m), 1.4, .45), t0 + d * i / len(notes), g * (0.8 + .2 * i / len(notes)), -0.5 + i / len(notes))
def shimmer(d):
    t = tt(d); s = np.zeros_like(t)
    for f in [2637, 3136, 3520, 4186, 4699]:
        s += np.sin(2 * np.pi * f * t + rs.uniform(0, 6)) * (0.5 + 0.5 * np.sin(2 * np.pi * rs.uniform(5, 9) * t))
    return s / 5 * np.sin(np.pi * t / d) ** 2
def whoosh(d, lo=200, hi=2800):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = lo + hi * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
def click():
    t = tt(.08); n = band(rs.standard_normal(len(t)), 2000, 9000) * np.exp(-t / .003)
    return norm(n) + .6 * np.sin(2 * np.pi * 900 * t) * np.exp(-t / .01)
def door(d):
    t = tt(d); rum = band(rs.standard_normal(len(t)), 40, 260); rum = norm(rum)
    roll = np.sin(2 * np.pi * np.cumsum(28 + 10 * np.sin(np.pi * t / d)) / SR) ** 9   # roller ticks
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** .6
    return (rum * .8 + .25 * band(roll, 200, 3000)) * env
def thud(f=70, d=.5):
    t = tt(d); ph = 2 * np.pi * np.cumsum(f * (1 + 1.5 * np.exp(-t * 30))) / SR
    return np.sin(ph) * np.exp(-t / .12) + .3 * norm(band(rs.standard_normal(len(t)), 100, 1500)) * np.exp(-t / .02)
def gong(f=180, d=3.0):
    t = tt(d); s = np.zeros_like(t)
    for r, a, dec in [(1, 1, 1.4), (1.52, .6, 1.0), (2.31, .45, .8), (3.07, .3, .5), (4.2, .2, .35)]:
        s += a * np.sin(2 * np.pi * f * r * t + 2 * np.sin(2 * np.pi * 3 * t) * .1) * np.exp(-t / dec)
    return s * np.minimum(1, t / .004)
def glint():
    t = tt(.6); return (np.sin(2 * np.pi * 4186 * t) + .6 * np.sin(2 * np.pi * 6272 * t)) * np.exp(-t / .12) * np.minimum(1, t / .002)
def swell(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 3000, 12000)); return n * (t / d) ** 3
def pad(ms, d, att, rel):
    t = tt(d); s = np.zeros_like(t)
    for m in ms:
        f = nt(m)
        for det in (-.0025, .0025):
            s += (np.sin(2 * np.pi * f * (1 + det) * t) + .25 * np.sin(4 * np.pi * f * (1 + det) * t) + .1 * np.sin(6 * np.pi * f * t))
    s /= len(ms) * 2
    env = np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1)
    return s * env * (1 + .12 * np.sin(2 * np.pi * 4.5 * t))
def celesta(f, d=1.4):
    t = tt(d); s = np.sin(2 * np.pi * f * t) * np.exp(-t / .45) + .35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t / .12)
    return s * np.minimum(1, t / .002)
def breath(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 500, 5000)); return n * np.sin(np.pi * t / d) ** 2
def clink():
    t = tt(1.2); s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / dec) for f, a, dec in [(2350, 1, .35), (3710, .6, .22), (5120, .35, .12), (6980, .2, .07)])
    return s * np.minimum(1, t / .001)
def pour(d):
    t = tt(d); x = band(rs.standard_normal(len(t)), 300, 2400); bub = np.zeros_like(t)
    for k in range(int(d * 14)):
        i = int(rs.uniform(0, len(t) - 2400)); tb = tt(.05); f = rs.uniform(500, 1100)
        bub[i:i + len(tb)] += np.sin(2 * np.pi * np.cumsum(f * (1 + 2 * tb / .05)) / SR) * np.exp(-tb / .015)
    return (norm(x) * .35 + bub * .5) * np.sin(np.pi * t / d) ** .7
# ── bed: Dmaj9 → Bm11 → Gmaj7#11 → A6sus → Dmaj9 (final)
chords = [(0.1, 2.6, [50, 57, 61, 64, 66]), (2.5, 2.2, [47, 54, 57, 61, 64]), (4.5, 2.6, [43, 50, 54, 61, 66]),
          (7.0, 2.0, [45, 52, 57, 59, 64]), (8.8, 1.3, [38, 50, 57, 61, 64, 66])]
for t0, d, ms in chords: add(pad(ms, d + .6, .6, .8), t0, .085)
room = norm(band(rs.standard_normal(N), 150, 2500)); L += room * .003; R += np.roll(room, 911) * .003
D9 = [62, 66, 69, 73, 74, 76, 78, 81, 85, 86, 88, 90]
tick_notes = [86, 88, 90, 93, 95, 97, 98]
ti = 0
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'tick': add(celesta(nt(tick_notes[ti % len(tick_notes)] - 12)), te, .05 * e.get('v', 1), -.6 + 1.2 * ((ti * 5) % 7) / 6); ti += 1
    elif k == 'swell': add(shimmer(e['d']), te, .04)
    elif k == 'harp': harp(D9[:e['n']], te, e['d'], .085)
    elif k == 'grow': add(breath(e['d']), te, .035, -.2)
    elif k == 'bloom': add(swell(.5), te, .05); add(breath(1.2), te + .1, .05); add(bell(nt(81), 2.6), te + .55, .06); add(bell(nt(85), 2.6), te + .62, .04, .3)
    elif k == 'pluck': add(pluck(nt(88 if e.get('f') else 85), 1.0, .3), te, .07, -.3 if e.get('f') else .3)
    elif k == 'whoosh': add(whoosh(e['d'], 150, 1800), te, .14)
    elif k == 'glass': add(clink(), te, .07, .1); add(clink(), te + .11, .035, -.2)
    elif k == 'pour': add(pour(e['d']), te, .09)
    elif k == 'bloom2': add(breath(1.0), te, .04, -.5); add(breath(1.0), te + .08, .04, .5); add(celesta(nt(90)), te + .4, .05, -.5); add(celesta(nt(93)), te + .5, .05, .5)
    elif k == 'fwip': add(whoosh(.28, 900, 5000), te, .06, rs.uniform(-.7, .7))
    elif k == 'reveal': add(swell(.4), te - .35, .05); add(bell(nt(74), 3.0), te, .08); add(bell(nt(81), 3.0), te + .06, .05)
    elif k == 'chime': add(bell(nt(86)), te, .07, .15); add(bell(nt(90)), te + .1, .04, -.15)
    elif k == 'gleam': add(swell(.35), te - .3, .04); add(shimmer(.8), te, .05, .3); add(glint(), te + .3, .04, .4)
    elif k == 'final': harp([62, 66, 69, 74, 78, 81, 86], te - .4, .8, .07); add(bell(nt(74), 3.0), te + .45, .07); add(bell(nt(78), 3.0), te + .5, .04, .3)
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.0) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
