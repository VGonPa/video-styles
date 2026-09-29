# events.json → audio.wav (48 kHz stereo, 10 s)
# dark drone bed, sub booms on titles, glassy shimmer, cold wind over the terrain, sonar pings,
# the thin "signal" tone with vibrato, soft UI ticks, typewriter keys + carriage returns,
# felt-marker redaction swipes, a dive whoosh into the black bar, closing low chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(78)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def boom():
    t = tt(3.0); f = 34 + 40 * np.exp(-t * 6); ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t / 1.1) * np.minimum(1, t / .01)
    return s + 0.25 * norm(band(rs.standard_normal(len(t)), 40, 400)) * np.exp(-t / .25)
def shimmer():
    t = tt(2.2); s = sum(np.sin(2 * np.pi * f * t + p) * a for f, a, p in [(1568, .5, 0), (2093, .35, 1), (2637, .25, 2), (3136, .15, .5)])
    return s * np.minimum(1, t / .6) * np.exp(-t / .9)
def wind(d):
    t = tt(d); s = norm(band(rs.standard_normal(len(t)), 150, 900)); am = 0.6 + 0.4 * np.sin(2 * np.pi * .35 * t + 1)
    return s * am * np.sin(np.pi * t / d) ** 1.2
def ping():
    t = tt(1.8); s = np.sin(2 * np.pi * 1318 * t) * np.exp(-t / .35) + .3 * np.sin(2 * np.pi * 2636 * t) * np.exp(-t / .15)
    return s * np.minimum(1, t / .003)
def signal(d):
    t = tt(d); f = 1420 + 14 * np.sin(2 * np.pi * 5.5 * t) + 30 * np.sin(2 * np.pi * .7 * t); ph = 2 * np.pi * np.cumsum(f) / SR
    am = (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t) ** 2) * np.minimum(1, t / .25) * np.minimum(1, (d - t) / .4)
    return np.sin(ph) * am + .15 * norm(band(rs.standard_normal(len(t)), 1200, 1700)) * am
def tick():
    t = tt(.02); return norm(band(rs.standard_normal(len(t)), 4000, 12000)) * np.exp(-t / .0015) + .4 * np.sin(2 * np.pi * 3200 * t) * np.exp(-t / .003)
def key():
    t = tt(0.07); n = norm(band(rs.standard_normal(len(t)), 1500, 7000)) * np.exp(-t / .004)
    return 0.6 * n + 0.5 * np.sin(2 * np.pi * (150 + 40 * rs.random()) * t) * np.exp(-t / .014)
def ret():
    t = tt(.25); z = norm(band(rs.standard_normal(len(t)), 800, 5000)) * np.exp(-t / .05) * .5
    return z + .5 * np.sin(2 * np.pi * 2400 * t) * np.exp(-t / .06)
def bar(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 700, 3500)); env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** .6
    return n * env * (0.8 + 0.2 * np.sin(2 * np.pi * 13 * t))
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 150 + 3200 * (t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * (t / d) ** 1.5
def slide():
    t = tt(.6); return norm(band(rs.standard_normal(len(t)), 400, 2500)) * np.sin(np.pi * t / .6) ** 2
def tone(freq, d, att=0.4, rel=1.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in [(1, 1), (2, .25), (3, .08)])
    return s * np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1)
t = np.arange(N) / SR
# bed: low drone (D minor cluster), slow beating, rises gently; room hiss
for m, g, p in [(38, .06, -.2), (45, .04, .2), (50, .025, 0), (53, .015, .3)]:
    s = tone(nt(m) * (1 + .002 * (m % 3)), 9.8, 1.2, 1.5) * (1 + .2 * np.sin(2 * np.pi * .18 * np.arange(int(9.8 * SR)) / SR + m))
    add(s, 0.1, g, p)
hiss = norm(band(rs.standard_normal(N), 2000, 9000)); L += hiss * .004; R += np.roll(hiss, 911) * .004
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'boom': add(boom(), te, .32 * v)
    elif k == 'shimmer': add(shimmer(), te, .035, .2)
    elif k == 'wind': add(wind(e['d']), te, .05, -.3)
    elif k == 'ping': add(ping(), te, .07 * v, .35)
    elif k == 'signal': add(signal(e['d']), te, .045, .1)
    elif k == 'tick': add(tick(), te, .05, rs.uniform(-.4, .4))
    elif k == 'key': add(key(), te + rs.uniform(0, .006), .13 * (0.8 + .4 * rs.random()), rs.uniform(-.2, .2))
    elif k == 'ret': add(ret(), te, .06, .3)
    elif k == 'bar': add(bar(e['d']), te, .09)
    elif k == 'whoosh': add(whoosh(e['d']), te, .2)
    elif k == 'thud': add(boom()[:SR // 2] * np.exp(-tt(.5) / .12), te, .25)
    elif k == 'slide': add(slide(), te, .06)
    elif k == 'chord':
        for i, m in enumerate([50, 57, 62, 65, 69]): add(tone(nt(m), 1.4, .15 + i * .05, .8), te + i * .05, .03)
fi = int(0.3 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
