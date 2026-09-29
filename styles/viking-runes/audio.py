# events.json → audio.wav (48 kHz stereo, 10 s)
# chisel taps on granite (iron ping + stone crack), grit scrape while the band is cut, torch crackle and fjord wind bed,
# ember chimes as each rune hands over its letter (D minor pentatonic), stone thuds as letters land,
# a low drone swell, a wind gust on the pull-back and a distant horn call for the ending.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(96)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def tap(v):
    t = tt(0.35); f0 = 2900 + 500 * rs.random()
    ping = sum(a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t / d) for r, a, d in [(1, 1, .06), (1.51, .5, .04), (2.37, .3, .025)])
    crack = norm(band(rs.standard_normal(len(t)), 700, 6000)) * np.exp(-t / 0.008)
    thud = np.sin(2 * np.pi * 140 * t) * np.exp(-t / 0.02)
    return (0.35 * ping + 0.9 * crack + 0.5 * thud) * v
def grit(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 1500, 8000))
    am = np.abs(band(rs.standard_normal(len(t)), 8, 60)); am = norm(am)
    return n * am * np.minimum(1, t / .1) * np.minimum(1, (d - t) / .2)
def bell(f, d=2.2):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * f * r * t + r) * np.exp(-t / (d * dd)) for r, a, dd in [(1, 1, .5), (2.01, .4, .3), (2.76, .25, .2), (5.4, .1, .08)])
    return s * np.minimum(1, t / .004)
def land():
    t = tt(0.4); f = 90 * np.exp(-t * 6) + 50; ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.07) + 0.3 * norm(band(rs.standard_normal(len(t)), 200, 2000)) * np.exp(-t / 0.03)
def wind(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 250 + 900 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.4
def horn(f, d):
    t = tt(d); vib = 1 + .004 * np.sin(2 * np.pi * 5 * t) * np.minimum(1, t / .8)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    s = sum(np.sin(k * ph) / k ** 1.3 for k in range(1, 9))
    env = np.minimum(1, t / .5) * np.minimum(1, (d - t) / 1.2)
    return band(s * env, 60, 1800)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR
# bed: fjord wind, torch crackle, low D drone
bed = band(rs.standard_normal(N), 80, 900); bed = norm(bed) * (0.6 + 0.4 * np.sin(2 * np.pi * .13 * t + 1) ** 2)
L += bed * .035; R += np.roll(bed, 4000) * .035
for k in range(150):
    tc = rs.uniform(0, DUR); c = norm(band(rs.standard_normal(int(.02 * SR)), 1200, 9000)) * np.exp(-tt(.02) / .003)
    add(c, tc, .05 + .08 * rs.random() ** 2, .45)
fire = band(rs.standard_normal(N), 150, 1200); L += norm(fire) * .012; R += norm(fire) * .02
for m, g, p in [(38, .05, -.2), (45, .03, .2), (50, .02, 0)]:
    add(horn(nt(m), 9.7) * .5 + np.sin(2 * np.pi * nt(m) * tt(9.7)) * np.minimum(1, tt(9.7) / 2) * np.minimum(1, (9.7 - tt(9.7)) / 1.5), 0.2, g, p)
PENTA = [62, 65, 67, 69, 72, 74, 77, 79, 81, 84]
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'tap': add(tap(v), te + rs.uniform(0, .006), 0.22 * (0.8 + .4 * rs.random()), rs.uniform(-.3, .3))
    elif k == 'scrape': add(grit(e['d']), te, 0.05, -.1)
    elif k == 'glint': add(bell(nt(86), 1.6), te, 0.05, .2)
    elif k == 'chime': add(bell(nt(PENTA[e['i'] % len(PENTA)]), 2.0), te, 0.07, -.4 + .8 * e['i'] / 10)
    elif k == 'land': add(land(), te, 0.28)
    elif k == 'swell':
        for i, m in enumerate([50, 57, 62, 65, 69]): add(horn(nt(m), 2.6) * .6, te + i * .05, 0.03, (i - 2) * .2)
    elif k == 'wind': add(wind(e['d']), te, 0.16, .3)
    elif k == 'horn': add(horn(nt(50), 2.2), te, 0.07, -.3); add(horn(nt(57), 1.6), te + .9, 0.05, -.3)
# master: fade in/out, soft limiter
fi = int(0.3 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.5) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
