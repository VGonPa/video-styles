# events.json → audio.wav (48 kHz stereo, 9.5 s)
# bouncy 80s party bed (kick, off-beat hats, square-wave bass line) + synth pops, boings, bloops,
# letter thuds and ticks, pill clacks, confetti crackle, whooshes and a closing chime.
import json, wave, numpy as np
SR, DUR = 48000, 9.5
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(4)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def env(n, dec): t = np.arange(n) / SR; return np.minimum(1, t / 0.004) * np.exp(-t / dec)
def sweep(f0, f1, d, dec, shape=np.sin):
    n = int(SR * d); t = np.arange(n) / SR; f = f0 * (f1 / f0) ** (t / d); ph = 2 * np.pi * np.cumsum(f) / SR
    return shape(ph) * env(n, dec)
sq = lambda x: np.sign(np.sin(x)) * 0.5
def boing(f0):
    t = tt(0.4); f = f0 * (1 + 0.6 * np.exp(-t * 9) * np.sin(2 * np.pi * 14 * t)); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(len(t), 0.14)
def chime(f):
    t = tt(1.4); return (np.sin(2*np.pi*f*t) + .5*np.sin(2*np.pi*f*1.5*t) + .3*np.sin(2*np.pi*f*2.01*t) + .2*np.sin(2*np.pi*f*3*t)) / 2 * env(len(t), 0.45)
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    a = np.exp(-2 * np.pi * (300 + 3000 * np.sin(np.pi * t / d) ** 2) / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y / (np.abs(y).max() + 1e-9) * np.sin(np.pi * t / d) ** 1.5
def crackle():
    t = tt(0.9); out = np.zeros(len(t))
    for _ in range(28):
        i = int(rs.uniform(0, 0.8) * SR); c = band(rs.standard_normal(600), 2500, 9000) * np.exp(-np.arange(600) / SR / 0.002)
        out[i:i + 600] += c * rs.uniform(0.3, 1)
    return out / (np.abs(out).max() + 1e-9) * np.exp(-t / 0.5)
def squeak(d):
    t = tt(d); f = 1500 + 900 * t / d + 120 * np.sin(2 * np.pi * 18 * t); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.sin(np.pi * t / d) ** 0.6
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
# party bed: 124 bpm; starts after the intro pop, ducks under the card reveal, stops before the chime
BPM = 124; beat = 60 / BPM
def kick():
    t = tt(0.25); f = 50 + 110 * np.exp(-t * 30); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.09)
def hat():
    t = tt(0.05); return band(rs.standard_normal(len(t)), 6000, 14000) * np.exp(-t / 0.012)
def bass(m, d):
    t = tt(d); s = sq(2 * np.pi * nt(m) * t) + 0.4 * np.sin(2 * np.pi * nt(m) * t); return band(s * np.exp(-t / 0.18), 30, 1800)
line = [45, 45, 52, 45, 48, 45, 52, 55]   # A, E, C, G bounce
b0 = 0.25; nb = int((8.6 - b0) / beat)
for i in range(nb):
    tb = b0 + i * beat; g = 0.55 if 3.8 < tb < 4.5 else 1.0
    add(kick(), tb, 0.30 * g); add(hat(), tb + beat / 2, 0.05 * g, 0.3)
    add(bass(line[i % 8], beat * 0.9), tb, 0.07 * g, -0.1)
    if i % 2: add(hat(), tb + beat * 0.75, 0.03 * g, -0.3)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0); f = e.get('f', 600); pan = rs.uniform(-.35, .35)
    if k == 'pop': add(sweep(f, f * 0.45, 0.09, 0.03), te, 0.45 * v, pan)
    elif k == 'bloop': add(sweep(f, f * 2.4, 0.18, 0.06), te, 0.35 * v)
    elif k == 'bloopdn': add(sweep(f, f * 0.4, 0.2, 0.07), te, 0.35 * v, pan)
    elif k == 'thud': add(sweep(f, f * 0.6, 0.25, 0.07), te, 0.35 * v)
    elif k == 'tick': add(sweep(f, f, 0.04, 0.008), te, 0.18 * v, pan)
    elif k == 'clack': add(sweep(f, f * 0.7, 0.06, 0.014, sq), te, 0.3 * v)
    elif k == 'boing': add(boing(f), te, 0.45 * v)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.28 * v)
    elif k == 'confetti': add(crackle(), te, 0.18 * v, pan)
    elif k == 'squeak': add(squeak(e['d']), te, 0.05 * v)
    elif k == 'chime':
        for j, m in enumerate([0, 4, 7, 12]): add(chime(f * 2 ** (m / 12)), te + j * 0.06, 0.12, (j - 1.5) * 0.2)
# master: fade in/out, soft limiter
fi = int(0.05 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
