# events.json → audio.wav (48 kHz stereo, 10 s)
# felt-tip marker squeaks for strokes, quick scribble chirps for handwriting, a soft bee buzz,
# camera whooshes, quiet room tone + warm pad, closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(5)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(max(1, int(d * SR))) / SR
def marker(d):
    d = max(d, 0.03); t = tt(d); n = band(rs.standard_normal(len(t)), 1500, 5500)
    f0 = 2200 + 600 * rs.random()
    squeak = np.sin(2 * np.pi * np.cumsum(f0 + 400 * np.sin(2 * np.pi * (5 + 4 * rs.random()) * t)) / SR) * 0.12
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.5 * (0.7 + 0.3 * np.sin(2 * np.pi * 11 * t))
    return (n / (np.abs(n).max() + 1e-9) + squeak) * env
def tap():
    t = tt(0.04); n = band(rs.standard_normal(len(t)), 800, 6000) * np.exp(-t / 0.004)
    return n / (np.abs(n).max() + 1e-9)
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 200 + 2200 * np.sin(np.pi * t / d) ** 2
    a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y / (np.abs(y).max() + 1e-9) * np.sin(np.pi * t / d) ** 1.5
def buzz(t0):
    # wing drone: buzzy harmonic tone at ~220 Hz, beating with the 7 Hz wing flap, till the end
    t = tt(DUR - t0); f = 218 + 6 * np.sin(2 * np.pi * 0.9 * t) + 3 * np.sin(2 * np.pi * 7.3 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = sum(np.sin(ph * h) / h ** 0.8 for h in range(1, 9))
    s = band(s, 150, 2500); s /= np.abs(s).max() + 1e-9
    env = np.minimum(1, t / 0.5) * (0.75 + 0.25 * np.sin(2 * np.pi * 7 * t))
    return s * env
def tone(freq, d, att=0.4, rel=1.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in [(1, 1), (2, .3), (3, .12)])
    env = np.minimum(1, t / att) * np.minimum(1, (d - t) / rel); return s * env
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR
room = band(rs.standard_normal(N), 200, 3000); room /= np.abs(room).max(); L += room * .005; R += np.roll(room, 777) * .005
for m, g, p in [(53, .03, -.3), (60, .022, .3), (65, .016, 0)]:   # F major pad, warm and light
    s = tone(nt(m), 9.4, 1.5, 1.4) * (1 + .15 * np.sin(2 * np.pi * .25 * tt(9.4))); add(s, 0.3, g, p)
ev = json.load(open('events.json'))
buzzes = [e for e in ev if e['k'] == 'buzz']
for e in ev:
    k, te = e['k'], e['t']
    if k == 'marker':
        add(tap(), te, 0.05, rs.uniform(-.2, .2)); add(marker(e['d']), te, 0.05, rs.uniform(-.25, .25))
    elif k == 'write':
        n = max(1, e['n']); d = e['d']
        for i in range(n): add(marker(d / n * 0.8), te + d * i / n, 0.04, rs.uniform(-.2, .2))
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.14)
    elif k == 'chord':
        for i, m in enumerate([65, 69, 72, 77]): add(tone(nt(m), 1.6, 0.06 + i * .03, 1.0), te + i * 0.05, 0.028)
        add(tone(nt(41), 1.6, .1, 1.1), te, 0.05)
# buzz: first bee on the left, second on the right; the first fades as the camera leaves panel A
b = np.zeros(N)
for j, e in enumerate(buzzes):
    s = buzz(e['t']); i = int(e['t'] * SR); seg = np.zeros(N); seg[i:i + len(s)] = s[:N - i]
    if j == 0: seg *= np.interp(t, [0, 4.5, 5.6, 10], [1, 1, 0.35, 0.35])
    add(seg, 0, 0.022, e['pan'])
# master: fade in/out, soft limiter
fi = int(0.25 * SR); fo = int(0.8 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
