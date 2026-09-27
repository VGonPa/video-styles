# events.json → audio.wav (48 kHz stereo, 10 s)
# a shadow-theatre score: warm drone + night air, harp melody (Karplus-Strong), paper snips for the title pieces,
# a leafy rustle for the foliage wipe, celesta chime for the moon, soft wing flutter, a page swish,
# felt footsteps, the lantern's metal tink, a soft flare and a harp chord, then a falling line into a reverb tail.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(42)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def harp(f, d=2.4, bright=0.5):
    n = int(d * SR); P = max(2, int(SR / f)); buf = band(rs.uniform(-1, 1, P * 4), 0, 2000 + 6000 * bright)[:P]; out = np.zeros(n)
    for i in range(n): out[i] = buf[i % P]; buf[i % P] = 0.5 * (buf[i % P] + buf[(i + 1) % P]) * 0.998
    t = np.arange(n) / SR; return norm(out) * np.exp(-t / 1.1) * np.minimum(1, t * 400)
def snip():
    t = tt(.09); return norm(band(rs.standard_normal(len(t)), 2500, 9000) * np.exp(-t / .008) + .5 * np.sin(2 * np.pi * 3100 * t) * np.exp(-t / .01))
def step():
    t = tt(.18); return norm(band(rs.standard_normal(len(t)), 90, 900) * np.exp(-t / .025) + .6 * np.sin(2 * np.pi * 110 * t) * np.exp(-t / .03))
def bell(f, d=2.5):
    t = tt(d); return norm(sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t / (dd)) for k, a, dd in [(1, 1, .9), (2.76, .4, .35), (5.4, .2, .15), (8.9, .08, .08)]))
def sweep(d, lo0, hi0, lo1, hi1, env):
    t = tt(d); x = rs.standard_normal(len(t)); out = np.zeros_like(x); K = 10; sl = len(t) // K + 1
    for k in range(K):
        a, b = k * sl, min(len(t), (k + 1) * sl); u = k / (K - 1); out[a:b] = band(x, lo0 + (lo1 - lo0) * u, hi0 + (hi1 - hi0) * u)[a:b]
    return norm(out) * env(t / d)
t = np.arange(N) / SR
# bed: drone on D + A with slow swell, and a breath of night air
dr = sum(a * np.sin(2 * np.pi * nt(m) * t + ph) for m, a, ph in [(38, .5, 0), (45, .35, 1), (50, .2, 2), (57, .08, .5)])
sw = 0.6 + 0.4 * np.sin(2 * np.pi * t / 5.5) ** 2
L += dr * sw * .045; R += dr * sw * .045
for ch in (L, R): ch += norm(band(rs.standard_normal(N), 200, 1800)) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 3.7 + rs.uniform(0, 6))) * .012
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'harp': m = e['n']; add(harp(nt(m), bright=.3 if m < 56 else .6), te, (0.2 if m < 56 else 0.15), (m - 64) / 30)
    elif k == 'snip': add(snip(), te, .1 * v, rs.uniform(-.4, .4))
    elif k == 'iris': add(sweep(.9, 100, 800, 300, 3000, lambda u: np.sin(np.pi * u) ** 2), te, .1)
    elif k == 'shimmer':
        for i, m in enumerate([81, 86, 90, 93]): add(bell(nt(m), 1.5), te + i * .08, .04, -.3 + i * .2)
    elif k == 'rustle':
        d = e['d']; s = sweep(d, 1500, 7000, 800, 5000, lambda u: np.sin(np.pi * u) ** 1.2)
        s *= 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 23 * tt(d)[:len(s)] + rs.uniform(0, 3)))
        n = len(s); pan = np.linspace(.8, -.8, n); i = int(te * SR); m = min(n, N - i)
        L[i:i + m] += s[:m] * .16 * np.sqrt(.5 - pan[:m] / 2) * 1.414; R[i:i + m] += s[:m] * .16 * np.sqrt(.5 + pan[:m] / 2) * 1.414
    elif k == 'moon':
        for i, m in enumerate([74, 78, 81, 86]): add(bell(nt(m)), te + i * .22, .05, .5)
    elif k == 'wings':
        d = e['d']; tw = tt(d); s = norm(band(rs.standard_normal(len(tw)), 300, 2500)) * np.maximum(0, np.sin(2 * np.pi * 5.5 * tw)) ** 3 * np.sin(np.pi * tw / d)
        n = len(s); pan = np.linspace(.7, -.7, n); i = int(te * SR); m = min(n, N - i)
        L[i:i + m] += s[:m] * .05 * np.sqrt(.5 - pan[:m] / 2) * 1.414; R[i:i + m] += s[:m] * .05 * np.sqrt(.5 + pan[:m] / 2) * 1.414
    elif k == 'page':
        d = e['d']; add(sweep(d, 600, 5000, 300, 2500, lambda u: np.sin(np.pi * u) ** .8), te, .14, .3)
        add(step(), te + d * .9, .12, -.3)
    elif k == 'step': add(step(), te, .08 * v, rs.uniform(-.2, .2))
    elif k == 'tink': add(bell(1320, 1.2) * .7 + bell(1980, 1.2) * .3, te, .06, .3)
    elif k == 'flare':
        add(sweep(1.1, 60, 400, 100, 1600, lambda u: np.minimum(1, u * 6) * np.exp(-u * 2.2)), te, .22, .2)
        for i, m in enumerate([86, 90, 93, 98]): add(bell(nt(m), 1.8), te + .12 + i * .05, .03, -.2 + i * .15)
    elif k == 'chord':
        for i, m in enumerate([50, 62, 66, 69, 74, 78]): add(harp(nt(m), 3.0, .6), te + i * .06, .13, -.4 + i * .16)
    elif k == 'fall': add(sweep(1.2, 200, 3000, 60, 600, lambda u: np.sin(np.pi * u) * (1 - u)), te, .05)
# a little room: exponential-noise reverb
ir = rs.standard_normal(int(1.8 * SR)) * np.exp(-np.arange(int(1.8 * SR)) / SR / .45); ir = band(ir, 150, 6000); ir /= np.abs(ir).sum() ** .5 * 18
def conv(x):
    n = len(x) + len(ir); F = 1 << (n - 1).bit_length(); return np.fft.irfft(np.fft.rfft(x, F) * np.fft.rfft(ir, F), F)[:len(x)]
L, R = L + conv(L) * .5, R + conv(R) * .5
fi = int(0.25 * SR); fo = int(0.8 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.6) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
