# events.json -> audio.wav (48 kHz stereo, 10 s)
# 1940s radio-serial feel: vinyl crackle, a tremolo organ bed in D minor, balloon pops, paper page turn,
# whooshes, an electric zap, woodblock caption ticks, logo thuds and a brassy "TO BE CONTINUED!" stab.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(57)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def nrm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def pop():
    t = tt(0.12); f = 900 * np.exp(-t * 40) + 260; ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.03) + 0.35 * nrm(band(rs.standard_normal(len(t)), 1500, 6000)) * np.exp(-t / 0.004)
def tick():
    t = tt(0.09); return (np.sin(2 * np.pi * 1250 * t) + .5 * np.sin(2 * np.pi * 2600 * t)) * np.exp(-t / 0.012)
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 250 + 2400 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return nrm(y) * np.sin(np.pi * t / d) ** 1.5
def zap():
    t = tt(0.5); buzz = np.sign(np.sin(2 * np.pi * (110 + 40 * np.sin(2 * np.pi * 23 * t)) * t))
    cr = band(rs.standard_normal(len(t)), 2000, 9000) * (rs.random(len(t)) < .08)
    return (0.5 * buzz + nrm(cr)) * np.exp(-t / 0.18) * (0.6 + 0.4 * (np.sin(2 * np.pi * 31 * t) > 0))
def page(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 700, 8000)
    am = np.abs(band(rs.standard_normal(len(t)), 4, 30)); am = nrm(am)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** .6
    flap = np.zeros(len(t)); i = int(len(t) * .8); tf = tt(0.2)
    fl = nrm(band(rs.standard_normal(len(tf)), 150, 2500)) * np.exp(-tf / 0.05); flap[i:i + len(tf)] = fl[:len(flap) - i]
    return nrm(n) * am * env * .8 + flap * .9
def thud(v):
    t = tt(0.3); f = 140 * np.exp(-t * 14) + 48; ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.07) + 0.3 * nrm(band(rs.standard_normal(len(t)), 200, 2500)) * np.exp(-t / 0.01)
def snag():
    t = tt(0.4); f = 180 + 60 * np.exp(-t * 20); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12)
    return s * (1 + .4 * np.sin(2 * np.pi * 38 * t)) + 0.6 * nrm(band(rs.standard_normal(len(t)), 800, 5000)) * np.exp(-t / 0.015)
def brass(freq, d, att=0.03, rel=0.9):
    t = tt(d); vib = 1 + 0.006 * np.sin(2 * np.pi * 5.5 * t) * np.clip(t / .3, 0, 1)
    ph = 2 * np.pi * np.cumsum(freq * vib) / SR
    s = sum(np.sin(ph * h) / h ** 1.1 for h in range(1, 9))
    env = np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1) * (0.8 + 0.2 * np.exp(-t / .15))
    return s * env
def organ(freq, d, att=0.3, rel=0.6):
    t = tt(d); s = np.sin(2 * np.pi * freq * t) + .5 * np.sin(4 * np.pi * freq * t) + .25 * np.sin(6 * np.pi * freq * t)
    trem = 1 + .25 * np.sin(2 * np.pi * 6 * t)
    return s * trem * np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1)
t = np.arange(N) / SR
# vinyl / old radio crackle + hiss
crk = np.zeros(N); idx = rs.integers(0, N, 900); crk[idx] = rs.uniform(-1, 1, 900) * rs.random(900) ** 2
crk = band(crk, 800, 9000); hiss = band(rs.standard_normal(N), 3000, 10000)
L += nrm(crk) * .05 + nrm(hiss) * .006; R += np.roll(nrm(crk), 311) * .05 + nrm(hiss) * .006
# organ bed: Dm - Bb - Gm - A (tension) under page 1; splash rises
chords = [(0.2, [50, 57, 62, 65]), (1.7, [46, 53, 58, 62]), (3.2, [43, 55, 58, 62]), (4.6, [45, 52, 57, 61]), (6.1, [45, 52, 57, 61, 64])]
for i, (t0, ns) in enumerate(chords):
    d = (chords[i + 1][0] - t0 + .35) if i + 1 < len(chords) else 1.3
    for m in ns: add(organ(nt(m), d, .25, .4), t0, .028, (m - 55) / 30)
# splash: D major, brighter, swelling to the stab
for m in [50, 57, 62, 66, 69]: add(organ(nt(m), 2.3, .5, .5), 6.9, .03, (m - 60) / 30)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'pop': add(pop(), te, .32, rs.uniform(-.3, .3))
    elif k == 'tick': add(tick(), te, .12, rs.uniform(-.2, .2))
    elif k == 'whoosh': add(whoosh(e['d']), te, .16)
    elif k == 'swish': add(whoosh(0.55), te - .1, .34, .3)
    elif k == 'zap': add(zap(), te, .16, .4)
    elif k == 'page': add(page(e['d']), te, .3, -.2)
    elif k == 'thud': add(thud(v), te, .3 * v, rs.uniform(-.25, .25))
    elif k == 'snag': add(snag(), te, .3, .15)
    elif k == 'stab':
        for i, m in enumerate([62, 66, 69, 74]): add(brass(nt(m), 1.0, .02, .7), te + i * .012, .05)
        add(brass(nt(38), 1.0, .02, .7), te, .07); add(thud(1), te, .35)
        for i, m in enumerate([62, 66, 69, 74, 78]): add(brass(nt(m), 0.95, .03, .8), te + .35 + i * .01, .05)
        add(brass(nt(38), 0.95, .03, .8), te + .35, .07)
fi = int(0.2 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
