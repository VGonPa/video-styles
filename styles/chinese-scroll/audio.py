# events.json → audio.wav (48 kHz stereo, 10 s)
# silk rustle while the scroll unrolls, a river-and-wind bed, plucked qin notes (Karplus-Strong, D pentatonic)
# following the journey, a sail filling, the waterfall swelling as it passes, distant crane calls, lamp flickers and
# a warm swell as it lights, a small bell for the boat lantern, the roller knocking on the table, the seal's soft thud.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(99)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def qin(f, d=3.2):
    n = int(d * SR); p = int(SR / f); buf = rs.uniform(-1, 1, p); buf = band(np.concatenate([buf] * 4), 60, 5000)[:p]
    out = np.zeros(n); b = buf.copy()
    for i in range(n):
        j = i % p; out[i] = b[j]; b[j] = 0.4985 * (b[j] + b[(j + 1) % p])
    t = tt(d); body = np.sin(2 * np.pi * f * t) * np.exp(-t / 1.4) * .35
    return norm(out + body) * np.minimum(1, t / .003) * np.minimum(1, (d - t) / .4)
def rustle(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 1800, 9000))
    am = norm(np.abs(band(rs.standard_normal(len(t)), 3, 30))) ** 1.5
    rum = norm(band(rs.standard_normal(len(t)), 60, 300)) * .5
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** .7
    return (n * am * .8 + rum) * env
def whoosh(d, lo, hi):
    t = tt(d); return norm(band(rs.standard_normal(len(t)), lo, hi)) * np.sin(np.pi * t / d) ** 2
def crane(v):
    out = np.zeros(int(1.4 * SR))
    for k, st in enumerate([0, .38, .62]):
        d = .3 if k else .42; t = tt(d); f = (820 if k != 1 else 980) * (1 + .06 * np.sin(np.pi * t / d))
        ph = 2 * np.pi * np.cumsum(f) / SR; s = sum(np.sin(h * ph) / h ** 1.2 for h in range(1, 7))
        s = band(s * np.sin(np.pi * t / d) ** .6, 400, 5000); i = int(st * SR); out[i:i + len(s)] += s
    return norm(out) * v
def bell(f, d=2.4):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * f * r * t + r) * np.exp(-t / (d * dd)) for r, a, dd in [(1, 1, .5), (2.01, .4, .3), (2.76, .25, .2), (5.4, .1, .08)])
    return s * np.minimum(1, t / .004)
def knock(f=180):
    t = tt(.25); return np.sin(2 * np.pi * f * t) * np.exp(-t / .03) + .4 * norm(band(rs.standard_normal(len(t)), 300, 3000)) * np.exp(-t / .01)
t = np.arange(N) / SR
# bed: river lapping + soft wind
water = norm(band(rs.standard_normal(N), 150, 1400)) * (0.6 + 0.4 * np.sin(2 * np.pi * .21 * t) ** 2)
L += water * .03; R += np.roll(water, 7000) * .03
wind = norm(band(rs.standard_normal(N), 300, 2200)) * (0.5 + 0.5 * np.sin(2 * np.pi * .08 * t + 2) ** 2)
L += wind * .012; R += np.roll(wind, 3000) * .012
# low drone on D and A
for m, g in [(38, .03), (45, .018)]:
    d = 9.6; tq = tt(d); add(np.sin(2 * np.pi * nt(m) * tq) * np.minimum(1, tq / 2) * np.minimum(1, (d - tq) / 1.5), .2, g)
PENTA = [62, 64, 66, 69, 71, 74, 76, 78]
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'rustle': add(rustle(e['d']), te, .09, .25)
    elif k == 'qin': add(qin(nt(PENTA[e['i'] % len(PENTA)] - 12)), te, .2, -.3 + .6 * (e['i'] % 4) / 3)
    elif k == 'sail': add(whoosh(1.2, 200, 1500), te, .07, .1)
    elif k == 'falls': add(whoosh(e['d'], 500, 4000), te, .05, -.2)
    elif k == 'crane': add(crane(v), te, .05, .4)
    elif k == 'flick': add(knock(900) * .3, te, .05)
    elif k == 'glow':
        for i, m in enumerate([62, 69, 74, 78]): add(bell(nt(m), 2.6), te + i * .06, .025, (i - 1.5) * .2)
    elif k == 'bell': add(bell(nt(86), 1.8), te, .04, .3)
    elif k == 'knock': add(knock(160), te, .25, -.4)
    elif k == 'stamp': add(knock(90), te, .35, -.3)
fi = int(0.4 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.5) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
