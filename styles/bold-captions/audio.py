# events.json → audio.wav (48 kHz stereo, 10 s)
# a soft lo-fi bed (pad chords, muted kick, quiet hats) ducked under every emphasis, word pops, sub-boom hits on
# highlighted words, whooshes into cutaways, fast clock ticks + an alarm ring, a riser into SCROLLING, swipe-up
# whooshes with finger flicks, cartoon boings for the icons and a closing chime.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(46)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def sweep(f): return np.sin(2 * np.pi * np.cumsum(f) / SR)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)

def pop():
    t = tt(0.09); return sweep(1100 * np.exp(-t * 55) + 320) * np.exp(-t / 0.022) + 0.25 * norm(band(rs.standard_normal(len(t)), 2000, 9000)) * np.exp(-t / 0.004)
def hit(v):
    t = tt(0.9); sub = sweep(95 * np.exp(-t * 7) + 42) * np.exp(-t / (0.16 + 0.1 * v))
    snap = norm(band(rs.standard_normal(len(t)), 1200, 11000)) * np.exp(-t / 0.012)
    body = norm(band(rs.standard_normal(len(t)), 150, 1200)) * np.exp(-t / 0.05)
    return sub * 1.0 + snap * 0.45 + body * 0.25
def whoosh(d, lo=300, hi=5000):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = lo + (hi - lo) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
def tick(hi):
    t = tt(0.03); return sweep(np.full(len(t), 3400.0 if hi else 2600.0)) * np.exp(-t / 0.004) + 0.4 * norm(band(rs.standard_normal(len(t)), 3000, 12000)) * np.exp(-t / 0.002)
def ring(d):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * f * t) for f, a in [(2150, 1), (2610, .7), (3900, .3), (5300, .15)])
    return s * (0.55 + 0.45 * np.sign(np.sin(2 * np.pi * 24 * t))) * np.minimum(1, (d - t) / 0.12)
def riser(d):
    t = tt(d); u = t / d; tone = sweep(220 + 700 * u ** 2) * 0.5 + sweep(330 + 1050 * u ** 2) * 0.25
    nz = norm(band(rs.standard_normal(len(t)), 2000, 10000)) * 0.25
    return (tone + nz) * u ** 2.2
def flick():
    t = tt(0.07); return norm(band(rs.standard_normal(len(t)), 1500, 7000)) * np.sin(np.pi * t / 0.07) ** 2
def boing():
    t = tt(0.4); f = 260 + 380 * (1 - np.exp(-t * 18)) + 40 * np.sin(2 * np.pi * 18 * t) * np.exp(-t * 5)
    return sweep(f) * np.exp(-t / 0.13) * np.minimum(1, t / 0.004)
def tone(freq, d, att=0.01, rel=1.0, harm=((1, 1), (2, .45), (3, .2), (4.2, .12))):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) * np.exp(-t * h * 1.5) for h, a in harm)
    return s * np.minimum(1, t / att) * np.minimum(1, (d - t) / rel)
def thump():
    t = tt(0.25); return sweep(70 * np.exp(-t * 10) + 40) * np.exp(-t / 0.06)

def bed(d):
    out = np.zeros(int(d * SR)); t = np.arange(len(out)) / SR; BEAT = 0.6
    chords = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 65]]
    for ci in range(int(d / 2.4) + 1):
        t0 = ci * 2.4; i0 = int(t0 * SR); n = min(int(2.5 * SR), len(out) - i0)
        if n <= 0: break
        tc = np.arange(n) / SR; env = np.minimum(1, tc / 0.25) * np.minimum(1, (2.5 - tc) / 0.35)
        for m in chords[ci % 4]:
            f = nt(m); out[i0:i0 + n] += (np.sin(2 * np.pi * f * tc) + 0.3 * np.sin(2 * np.pi * 2 * f * tc + 1)) * env * 0.08
        f = nt(chords[ci % 4][0] - 24); out[i0:i0 + n] += np.sin(2 * np.pi * f * tc) * env * 0.22
    for k in range(int(d / BEAT) + 1):
        i0 = int(k * BEAT * SR); kick = thump() * 0.5; n = min(len(kick), len(out) - i0)
        if n > 0: out[i0:i0 + n] += kick[:n]
        hh = norm(band(rs.standard_normal(int(0.03 * SR)), 6000, 14000)) * np.exp(-tt(0.03) / 0.008) * 0.07
        i1 = int((k * BEAT + BEAT / 2) * SR); n = min(len(hh), len(out) - i1)
        if n > 0: out[i1:i1 + n] += hh[:n]
    return out * np.minimum(1, t / 0.4)

ev = json.load(open('events.json'))
duck = np.ones(N)
for e in ev:
    if e['k'] == 'hit':
        i = int(e['t'] * SR); n = min(int(0.45 * SR), N - i); u = np.arange(n) / n; duck[i:i + n] = np.minimum(duck[i:i + n], 0.35 + 0.65 * u ** 1.5)
for e in ev:
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'bed':
        b = bed(e['d']); i = int(te * SR); n = min(len(b), N - i); b = b[:n] * duck[i:i + n]; add(b, te, 0.5, 0); add(np.roll(b, 300), te, 0.12, .6)
    elif k == 'pop': add(pop(), te, 0.16, rs.uniform(-.2, .2))
    elif k == 'hit': add(hit(v), te, 0.55 * v)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.3, -.3)
    elif k == 'swipe': add(whoosh(e['d'], 800, 7000), te, 0.28, .25)
    elif k == 'tick':
        for j in range(int(e['d'] / 0.085)): add(tick(j % 2 == 0), te + j * 0.085, 0.07, .15)
    elif k == 'ring': add(ring(e['d']), te, 0.07, -.1)
    elif k == 'cut': add(thump(), te, 0.25)
    elif k == 'riser': add(riser(e['d']), te, 0.13)
    elif k == 'flicks':
        for j in range(int(e['d'] / 0.22)): add(flick(), te + j * 0.22, 0.06, .3)
    elif k == 'boing': add(boing(), te, 0.2, rs.uniform(-.3, .3))
    elif k == 'ding':
        for i, m in enumerate([76, 79, 84, 88]): add(tone(nt(m), 1.1, 0.005, 0.8), te + i * 0.03, 0.05)
fi = int(0.1 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
