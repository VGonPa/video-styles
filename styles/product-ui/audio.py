# events.json → audio.wav (48 kHz stereo, 10 s)
# soft UI foley: cursor clicks, card lift/drop, toggle ticks, counter ticks, pops, airy whooshes on zooms/morphs,
# success chimes, a notification ding, over a light marimba pulse + warm pad (F major), ending on a clean chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(23)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
nrm = lambda x: x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def click(bright=1.0):
    t = tt(0.05); n = nrm(band(rs.standard_normal(len(t)), 2000, 9000)) * np.exp(-t / 0.0022)
    body = np.sin(2 * np.pi * 1800 * bright * t) * np.exp(-t / 0.004)
    return 0.7 * n + 0.4 * body
def tick(f=3200):
    t = tt(0.03); return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.0035) + 0.3 * nrm(band(rs.standard_normal(len(t)), 4000, 10000)) * np.exp(-t / 0.0015)
def thud():
    t = tt(0.22); f = 180 * np.exp(-t * 20) + 70; s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05)
    return s + 0.35 * nrm(band(rs.standard_normal(len(t)), 200, 2500)) * np.exp(-t / 0.012)
def lift():
    t = tt(0.16); f = 500 + 900 * t / 0.16; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.16) ** 2
def pop():
    t = tt(0.14); f = 420 + 1100 * (1 - np.exp(-t * 60)); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.035)
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 300 + 3200 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return nrm(y) * np.sin(np.pi * t / d) ** 1.6
def bell(freq, d=1.2, g=1.0):
    t = tt(d); s = np.sin(2 * np.pi * freq * t) + .35 * np.sin(2 * np.pi * freq * 2.76 * t) * np.exp(-t / .12) + .2 * np.sin(2 * np.pi * freq * 5.4 * t) * np.exp(-t / .05)
    return s * np.exp(-t / (d / 3.5)) * np.minimum(1, t / .003) * g
def chime(v=1.0):
    out = np.zeros(int(1.4 * SR))
    for i, m in enumerate([84, 88, 91]):
        b = bell(nt(m), 1.2); o = int(i * .07 * SR); out[o:o + len(b)] += b[:len(out) - o] * (0.8 - i * .1)
    return out * v
def marimba(freq, d=0.5):
    t = tt(d); return (np.sin(2 * np.pi * freq * t) + .25 * np.sin(2 * np.pi * freq * 4 * t) * np.exp(-t / .02)) * np.exp(-t / .12) * np.minimum(1, t / .002)
def tone(freq, d, att=0.4, rel=1.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in [(1, 1), (2, .25), (3, .08)])
    return s * np.minimum(1, t / att) * np.minimum(1, np.maximum(0, d - t) / rel)
# bed: warm pad (F major 9) + soft marimba pulse at 112 bpm, eighth notes
t = np.arange(N) / SR
for m, g, p in [(53, .045, -.3), (60, .03, .3), (64, .025, 0), (67, .018, -.2)]:
    add(tone(nt(m), 9.7, 1.4, 1.4), 0.2, g, p)
beat = 60 / 112 / 2; pat = [65, 72, 69, 72, 67, 72, 69, 76]
k = 0; tb = 0.9
while tb < 9.1:
    m = pat[k % 8] + (0 if (k // 16) % 2 == 0 else -2); add(marimba(nt(m)), tb, 0.045 * (1.0 if k % 2 == 0 else .7), .25 if k % 2 else -.25); k += 1; tb += beat
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'click': add(click(), te, 0.22 * v, .1)
    elif k == 'tick': add(tick(2600 + 1400 * rs.random()), te, 0.16 * v, rs.uniform(-.2, .2))
    elif k == 'lift': add(lift(), te, 0.05)
    elif k == 'drop': add(thud(), te, 0.35); add(tick(2200), te + .01, .12)
    elif k == 'pop': add(pop(), te, 0.2 * v)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.13 * v, rs.uniform(-.3, .3))
    elif k == 'chime': add(chime(v), te, 0.09)
    elif k == 'roll':
        for i in range(4): add(tick(3000 + 300 * i), te + i * .06, .14)
    elif k == 'ding': add(bell(nt(88), 1.0), te, .1); add(bell(nt(95), 1.0), te + .09, .07)
    elif k == 'chord':
        for i, m in enumerate([53, 60, 65, 69, 72, 76]): add(tone(nt(m), 1.9, 0.05 + i * .02, 1.2), te + i * 0.03, 0.035)
        for i, m in enumerate([77, 81, 84]): add(bell(nt(m), 1.6), te + .15 + i * .08, .04)
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.8) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
