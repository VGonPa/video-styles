# events.json → audio.wav (48 kHz stereo, 10 s)
# paper slides and cardboard taps, snow-crunch footsteps, pull-tab rustle, glassy moonrise, star bells,
# lamp clicks with warm chimes, title-card whoosh + word pops, winter wind + soft D-major pad, music-box close.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(9)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def rustle(d=0.45, lo=900, hi=7000):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), lo, hi))
    am = np.abs(band(rs.standard_normal(len(t)), 5, 40)); am /= am.max() + 1e-9
    return n * am * np.sin(np.pi * t / d) ** 0.7
def tap(f=140):
    t = tt(0.25); ph = 2 * np.pi * np.cumsum(f * np.exp(-t * 6) + f * .4) / SR
    return np.sin(ph) * np.exp(-t / 0.04) + 0.35 * norm(band(rs.standard_normal(len(t)), 1500, 6000)) * np.exp(-t / 0.004)
def crunch():
    t = tt(0.11); n = norm(band(rs.standard_normal(len(t)), 1200, 7000))
    grains = (rs.random(len(t)) < 0.012) * rs.standard_normal(len(t)) * 3
    return (n * 0.5 + grains) * np.exp(-t / 0.035) * np.minimum(1, t / 0.006)
def bell(f, d=1.2):
    t = tt(d); return (np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.15) + .2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / 0.06)) * np.exp(-t / (d * .35)) * np.minimum(1, t / 0.002)
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    a = np.exp(-2 * np.pi * (200 + 2400 * np.sin(np.pi * t / d) ** 2) / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
def tone(freq, d, att=0.4, rel=1.0, harm=((1, 1), (2, .3), (3, .12))):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in harm)
    return s * np.minimum(1, t / att) * np.minimum(1, (d - t) / rel)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR
# bed: winter wind (slowly breathing filtered noise) + a soft D-major pad that cools into the night
wind = band(rs.standard_normal(N), 150, 1400); wind = norm(wind) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.17 * t + 1) ** 2)
L += wind * 0.03; R += np.roll(wind, 2400) * 0.03
for m, g, p in [(50, .05, -.3), (57, .035, .3), (62, .025, 0), (66, .018, .2)]:
    add(tone(nt(m), 9.7, 1.8, 1.4) * (1 + .12 * np.sin(2 * np.pi * .21 * tt(9.7))), 0.2, g, p)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'slide': add(rustle(0.5), te, 0.10 * v, rs.uniform(-.3, .3))
    elif k == 'tap': add(tap(e.get('f', 140)), te, 0.28 * v)
    elif k == 'step': add(crunch(), te + rs.uniform(0, .01), 0.10 * v * (0.8 + .4 * rs.random()), rs.uniform(-.25, .25))
    elif k == 'tab': add(rustle(e['d'], 500, 6000), te, 0.16, .4); add(whoosh(e['d']), te, 0.06, .3)
    elif k == 'moon':
        for i, m in enumerate([74, 78, 81, 86]): add(tone(nt(m), 1.8, 0.5, 1.0, ((1, 1), (2, .15))), te + i * .12, 0.012, .5)
    elif k == 'star': add(bell(e['f'], 1.0), te, 0.035, rs.uniform(-.6, .6))
    elif k == 'sniff':
        for i in range(2): add(rustle(0.08, 3000, 9000), te + i * .13, 0.05)
    elif k == 'rustle': add(rustle(e['d'], 600, 5000), te, 0.07, .15)
    elif k == 'light': add(tap(900) * .3, te, 0.12); add(bell(e['f'], 1.4), te + .01, 0.045, -.3)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.14)
    elif k == 'pop': add(tap(e['f']), te, 0.16); add(rustle(0.06, 2000, 8000), te, 0.03)
    elif k == 'chord':
        for i, m in enumerate([74, 78, 81, 86, 90]): add(bell(nt(m), 2.2), te + i * 0.09, 0.05, -.4 + i * .2)
        add(tone(nt(38), 2.2, .15, 1.4), te, 0.05)
fi = int(0.3 * SR); fo = int(0.8 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
