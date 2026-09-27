# events.json → audio.wav (48 kHz stereo, 10 s)
# 1920s gala palette: warm maj7/9 pad with a slow tremolo, harp glissandi, bell chimes, glass shimmers on the line work,
# a latch click + rolling elevator doors, whooshes, pinstripe panels meeting, a metallic stamp on the seal, glints.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(1925)
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
# ── bed: Ebmaj7 → Cm9 → Abmaj7(#11) → Bb13sus → Ebmaj9 on the seal
chords = [(0.2, 2.6, [51, 58, 62, 67, 70]), (2.45, 2.3, [48, 55, 58, 62, 63]), (4.5, 3.1, [44, 51, 55, 60, 62]),
          (7.4, 1.35, [46, 53, 56, 60, 63]), (8.55, 1.45, [39, 51, 58, 62, 65, 67])]
for t0, d, ms in chords: add(pad(ms, d + .5, .5, .7), t0, .09)
t = np.arange(N) / SR
room = norm(band(rs.standard_normal(N), 150, 2500)); L += room * .004; R += np.roll(room, 911) * .004
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'shimmer': add(shimmer(e['d']), te, .05, rs.uniform(-.4, .4))
    elif k == 'chime': add(bell(nt(79 if e.get('f', 0) == 0 else 84)), te, .12, .1); add(bell(nt(86)), te + .09, .06, -.2)
    elif k == 'gleam': add(swell(.35), te - .3, .05); add(shimmer(.7), te, .06, .3); add(glint(), te + .25, .05, .4)
    elif k == 'click': add(click(), te, .25)
    elif k == 'door':
        d = e['d']; add(door(d), te, .5, -.5); add(door(d), te + .02, .5, .5)
    elif k == 'whoosh': add(whoosh(e['d']), te, .18)
    elif k == 'harp': harp([63, 67, 70, 74, 75, 79, 82, 86, 87, 91][:e['n']], te, e['d'], .09)
    elif k == 'reveal': add(swell(.4), te - .35, .06); add(bell(nt(75), 3.0), te, .08); add(bell(nt(82), 3.0), te + .05, .05)
    elif k == 'pluck': add(pluck(nt(87), 1.0, .3), te, .08, rs.uniform(-.5, .5))
    elif k == 'glint': add(glint(), te, .07, rs.uniform(-.3, .3))
    elif k == 'meet': add(thud(90, .4), te, .3); add(bell(nt(91), .8), te, .03)
    elif k == 'rise': add(swell(.16), te, .08)
    elif k == 'stamp': add(thud(55, .7), te, .6); add(gong(155, 2.4), te, .12); add(bell(nt(87), 2.5), te + .02, .06)
    elif k == 'tick': add(pluck(nt(96), .3, .2), te, .04 * e.get('v', 1))
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
