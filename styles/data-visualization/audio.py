# events.json → audio.wav (48 kHz stereo, 10 s)
# editorial data sound: soft marimba-like plucks per data point (pitch follows the value), a counter
# ratchet for "×3", woody ticks for bars, paper-slide whooshes on scroll, a quiet pad and a closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(19)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def env(t, a, dec): return np.minimum(1, t / a) * np.exp(-t / dec)
def pluck(f, d=0.4, dec=0.07):
    t = tt(d); return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / 0.02)) * env(t, 0.002, dec)
def tick(f):
    t = tt(0.15); n = band(rs.standard_normal(len(t)), 1500, 6000) * np.exp(-t / 0.003)
    return pluck(f, 0.15, 0.035) + 0.25 * n / (np.abs(n).max() + 1e-9)
def ratchet():
    t = tt(0.05); n = band(rs.standard_normal(len(t)), 2500, 9000) * np.exp(-t / 0.004)
    return n / (np.abs(n).max() + 1e-9) + 0.4 * np.sin(2 * np.pi * 1400 * t) * np.exp(-t / 0.01)
def slide(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 300 + 1800 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y / (np.abs(y).max() + 1e-9) * np.sin(np.pi * t / d) ** 1.5
def tone(freq, d, att=0.4, rel=1.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in [(1, 1), (2, .25), (3, .08)])
    return s * np.minimum(1, t / att) * np.minimum(1, np.maximum(d - t, 0) / rel)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
# bed: quiet room + soft C major pad
room = band(rs.standard_normal(N), 150, 2500); room /= np.abs(room).max(); L += room * .004; R += np.roll(room, 911) * .004
for m, g, p in [(48, .035, -.3), (55, .025, .3), (64, .015, 0)]:
    add(tone(nt(m), 9.4, 1.5, 1.5), 0.2, g, p)
PENT = [60, 62, 64, 67, 69, 72, 74, 76, 79, 81, 84]
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 0.5)
    if k == 'dot': add(pluck(nt(PENT[min(len(PENT) - 1, int(v * 12))])), te, 0.09, (v - 0.5) * 0.6)
    elif k == 'tock': add(pluck(nt(55), 0.6, 0.14) + 0.4 * pluck(nt(67), 0.6, 0.1), te, 0.14)
    elif k == 'count': add(ratchet(), te, 0.05 + 0.03 * v, 0.2); add(pluck(nt(72 + int(v * 7)), 0.2, 0.03), te, 0.035)
    elif k == 'tick': add(tick(nt(69)), te, 0.1, -0.1)
    elif k == 'tickLo': add(tick(nt(57)), te, 0.09, 0.1)
    elif k == 'slide': add(slide(e['d']), te, 0.07)
    elif k == 'soft':
        for i, m in enumerate([60, 64, 67, 72]): add(tone(nt(m), 1.8, 0.05 + i * .03, 1.2), te + i * 0.07, 0.03)
        add(tone(nt(36), 1.8, .1, 1.3), te, 0.05)
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.6) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
