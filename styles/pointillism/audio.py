# events.json → audio.wav (48 kHz stereo, 10 s)
# soft brush dabs (a patter that follows how many dots land per frame), river lapping and a summer-park air bed,
# a warm string-pad in F major, airy pull-out swell, birdsong chirps, celesta notes for the title words,
# a rising shimmer as the dabs lift off, closing chord.
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
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
DABS = []
for k in range(12):                                  # a small bank of bristle taps
    t = tt(0.05); n = band(rs.standard_normal(len(t)), 700 + 300 * rs.random(), 4200) * np.exp(-t / (0.006 + 0.004 * rs.random()))
    body = np.sin(2 * np.pi * (220 + 120 * rs.random()) * t) * np.exp(-t / 0.01)
    DABS.append(0.7 * n / (np.abs(n).max() + 1e-9) + 0.25 * body)
def tone(freq, d, att=0.4, rel=1.0, harm=((1, 1), (2, .25), (3, .08))):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in harm)
    env = np.minimum(1, t / att) * np.minimum(1, np.maximum(0, d - t) / rel); return s * env
def celesta(freq, d=1.6):
    t = tt(d); s = np.sin(2 * np.pi * freq * t) + .35 * np.sin(2 * np.pi * freq * 4 * t) * np.exp(-t / .08) + .2 * np.sin(2 * np.pi * freq * 2 * t)
    return s * np.exp(-t / .5) * np.minimum(1, t / .003)
def chirp(f0, f1, d):
    t = tt(d); f = f0 + (f1 - f0) * (t / d) ** .7; ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph + 1.5 * np.sin(2 * np.pi * 38 * t)) * np.sin(np.pi * t / d) ** 2
def bird():
    out = np.zeros(int(0.7 * SR)); p = 0.0
    for k in range(3 + int(rs.random() * 3)):
        f0 = 3200 + 1600 * rs.random(); s = chirp(f0, f0 * (1.25 + .3 * rs.random()), 0.05 + 0.05 * rs.random()); i = int(p * SR)
        out[i:i + len(s)] += s[:len(out) - i]; p += 0.08 + 0.06 * rs.random()
    return out
# beds: river lapping (slow-modulated low noise), light breeze, F-major pad swelling with the reveal
t = np.arange(N) / SR
lap = band(rs.standard_normal(N), 120, 900); lap /= np.abs(lap).max()
lapam = 0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * t) * np.sin(2 * np.pi * 0.23 * t + 1)
air = band(rs.standard_normal(N), 1500, 7000); air /= np.abs(air).max()
bed = np.clip(t / 1.2, 0, 1)
L += (lap * lapam * 0.05 + air * 0.008) * bed; R += (np.roll(lap, 4321) * lapam * 0.05 + np.roll(air, 999) * 0.008) * bed
for m, g, p, t0 in [(53, .045, -.25, 0.2), (60, .03, .25, 0.6), (65, .022, 0, 1.0), (69, .018, .3, 3.2), (72, .012, -.3, 4.4)]:
    d = 9.6 - t0; s = tone(nt(m), d, 1.6, 1.4) * (1 + .12 * np.sin(2 * np.pi * .3 * tt(d))); add(s, t0, g, p)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'dab':
        n = int(min(4, np.ceil(np.sqrt(v) / 6)))
        for j in range(n):
            add(DABS[int(rs.integers(len(DABS)))], te + rs.uniform(0, 1 / 30), 0.05 * (0.6 + .6 * rs.random()) * min(1, .4 + v / 150), rs.uniform(-.6, .6))
    elif k == 'air':
        d = e['d']; s = band(rs.standard_normal(int(d * SR)), 300, 2500); s /= np.abs(s).max()
        add(s * np.sin(np.pi * tt(d) / d) ** 2, te, 0.06)
    elif k == 'note':
        for j, m in enumerate([[77, 81], [84], [81, 86], [89, 84]][int(v)]): add(celesta(nt(m)), te + j * .05, 0.07, -.3 + .2 * v)
    elif k == 'sub':
        for j, m in enumerate([72, 77, 81]): add(celesta(nt(m), 2.0), te + j * .09, 0.04, .2)
    elif k == 'bird':
        add(bird(), te, 0.035, rs.uniform(-.7, .7))
    elif k == 'lift':
        for j in range(26): add(DABS[j % len(DABS)], te + j * 0.042 + rs.uniform(0, .02), 0.04, rs.uniform(-.7, .7))
        for j, m in enumerate([89, 86, 84, 81, 77]): add(celesta(nt(m), 1.4), te + .1 + j * .17, 0.03, .4 - j * .2)
    elif k == 'chord':
        for i, m in enumerate([53, 60, 65, 69, 72, 77]): add(tone(nt(m), 1.25, 0.12 + i * .02, 1.0), te + i * .035, 0.028)
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.5) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
