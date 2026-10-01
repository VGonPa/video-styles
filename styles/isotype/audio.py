# events.json → audio.wav (48 kHz stereo, 10 s)
# letterpress/print-shop palette: wooden-type tocks tuned per row as symbols are counted out,
# paper flicks when a symbol flips, a soft toy-car purr for each car queueing, small stops,
# a paper swish for the regroup, a bell chord for the finding, a quiet warm pad underneath.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(120)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def env(t, a, dec): return np.minimum(1, t / a) * np.exp(-t / dec)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def tock(f, dec=0.06):   # wooden type block: tuned bar + click
    t = tt(0.4)
    s = np.sin(2 * np.pi * f * t) * env(t, 0.001, dec) + 0.3 * np.sin(2 * np.pi * f * 3.93 * t) * env(t, 0.0005, dec * 0.25)
    return s + 0.12 * band(rs.standard_normal(len(t)), 2000, 9000) * env(t, 0.0002, 0.003)
def stamp():
    t = tt(0.5); f = 120 * np.exp(-t * 25) + 55
    thud = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(t, 0.002, 0.09)
    n = band(rs.standard_normal(len(t)), 300, 4000) * env(t, 0.001, 0.03)
    return thud + 0.35 * n / (np.abs(n).max() + 1e-9)
def flick():
    t = tt(0.12); n = band(rs.standard_normal(len(t)), 2500, 9000)
    return n / (np.abs(n).max() + 1e-9) * np.sin(np.pi * t / 0.12) ** 2 * (1 + np.sin(2 * np.pi * 60 * t)) * 0.5
def purr(d):   # tiny engine: low buzz with a rising then falling pitch
    t = tt(d); x = t / d; f = 70 + 45 * np.sin(np.pi * x)
    ph = 2 * np.pi * np.cumsum(f) / SR; s = np.sign(np.sin(ph)) * 0.4 + np.sin(ph)
    s = band(s, 40, 900) + 0.3 * band(rs.standard_normal(len(t)), 200, 1200)
    return s / (np.abs(s).max() + 1e-9) * np.sin(np.pi * np.clip(x, 0, 1)) ** 1.2
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    a = np.exp(-2 * np.pi * (250 + 2600 * np.sin(np.pi * t / d) ** 2) / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y / (np.abs(y).max() + 1e-9) * np.sin(np.pi * t / d) ** 1.5
def bell(f, d=2.2):
    t = tt(d); return sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (d * 0.35 / h ** 0.5)) for h, a in [(1, 1), (2.01, .35), (3.02, .15), (4.1, .06)]) * np.minimum(1, t / 0.004)
def tone(freq, d, att=0.4, rel=1.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in [(1, 1), (2, .25), (3, .08)])
    return s * np.minimum(1, t / att) * np.minimum(1, (d - t) / rel)
# bed: room tone + warm pad (F major), a little swell as the finding lands
t = np.arange(N) / SR
room = band(rs.standard_normal(N), 150, 2500); room /= np.abs(room).max(); L += room * .005; R += np.roll(room, 911) * .005
for m, g, p in [(41, .04, -.3), (48, .03, .3), (57, .02, 0), (53, .02, .1)]:
    s = tone(nt(m), 9.5, 1.5, 1.4) * (1 + .12 * np.sin(2 * np.pi * .2 * tt(9.5))); add(s, 0.2, g, p)
ROWSCALE = [[67, 69, 72, 74, 76, 79], [64, 67, 69, 72, 74], [60, 62, 64, 67, 69, 72], [57, 60, 62, 64, 67, 69, 72, 74, 76, 79, 81]]
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 0)
    if k == 'pop':
        sc = ROWSCALE[v]; m = sc[min(e.get('i', 0), len(sc) - 1)] if 'i' in e else 72
        add(tock(nt(m)), te + 0.03, 0.16, -0.5 + e.get('i', 3) * 0.09)
    elif k == 'tick': add(tock(nt(84 + v % 5), 0.025), te, 0.07, rs.uniform(-.3, .3))
    elif k == 'stamp': add(stamp(), te, 0.4 * v)
    elif k == 'flip': add(flick(), te, 0.12, rs.uniform(-.2, .2))
    elif k == 'drive': add(purr(e['d']), te, 0.07, 0.3)
    elif k == 'park': add(tock(nt(57), 0.03), te, 0.1, -0.1)
    elif k == 'swish': add(whoosh(e['d']), te, 0.16)
    elif k == 'chime':
        for i, m in enumerate([65, 69, 72, 77]): add(bell(nt(m)), te + i * 0.05, 0.05, -.2 + i * .13)
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.0) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
