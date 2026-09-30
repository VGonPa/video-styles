# events.json → audio.wav (48 kHz stereo, 10 s)
# clay stop-motion foley: squishes, plops, pats, tin clinks, water trickle + drips, soft footsteps,
# rubbery stretch and boing, petal/letter pops, a warm kalimba bed and a closing chime.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(12)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def env(n, a=0.002, d=0.08): t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def sweep(f0, f1, ms, d, harm=0.0):
    n = int(SR * ms / 1000); t = np.arange(n) / SR; f = f0 * (f1 / f0) ** (t / (ms / 1000))
    ph = 2 * np.pi * np.cumsum(f) / SR; return (np.sin(ph) + harm * np.sin(2 * ph)) * env(n, 0.002, d)
def noise(d, lo, hi, dec):
    t = tt(d); n = band(rs.standard_normal(len(t)), lo, hi) * np.exp(-t / dec); return n / (np.abs(n).max() + 1e-9)
def mix(*xs):
    o = np.zeros(max(len(x) for x in xs))
    for x in xs: o[:len(x)] += x
    return o
def squish(f): return mix(sweep(f, f * 1.6, 140, 0.06, 0.35), 0.25 * noise(0.14, 300, 2500, 0.04))
def plop(f): return sweep(f, f * .32, 110, 0.045, 0.15)
def pop(f): return sweep(f, f * 2.2, 60, 0.03, 0.2)
def pat(): return mix(0.8 * sweep(150, 70, 90, 0.03), 0.4 * noise(0.08, 200, 1800, 0.02))
def clink():
    t = tt(0.5); s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, a, d in [(1870, 1, .12), (2950, .6, .08), (4410, .35, .05)])
    return s + 0.3 * noise(0.5, 3000, 9000, 0.004)
def step(): return mix(0.9 * sweep(110, 60, 120, 0.04, 0.2), 0.3 * noise(0.1, 150, 1200, 0.02))
def drip(f): return sweep(f, f * 1.9, 45, 0.02)
def trickle(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 1200, 6000)
    am = np.abs(band(rs.standard_normal(len(t)), 8, 60)); am /= am.max() + 1e-9
    return n / (np.abs(n).max() + 1e-9) * am * np.sin(np.pi * t / d) ** 0.5
def boing():
    t = tt(0.45); f = 180 + 140 * np.exp(-t * 6) * np.cos(2 * np.pi * 9 * t); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.18)
def stretch(d):
    t = tt(d); f = 520 * (0.45 ** (t / d)) * (1 + 0.04 * np.sin(2 * np.pi * 7 * t)); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.sin(np.pi * t / d) ** 0.6 + 0.15 * noise(d, 200, 1500, d)
def kalimba(f, d=1.2):
    t = tt(d); return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / 0.05)) * np.exp(-t / 0.45) * np.minimum(1, t / 0.003)
def chime(f):
    t = tt(2.2); return sum(np.sin(2 * np.pi * f * k * t) * np.exp(-t / (0.9 / k)) / k for k in (1, 2, 3, 4.2)) * np.minimum(1, t / 0.004)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
# bed: quiet room tone + a gentle kalimba ostinato (C major pentatonic)
room = band(rs.standard_normal(N), 150, 2500); room /= np.abs(room).max(); L += room * .004; R += np.roll(room, 911) * .004
mel = [72, 76, 79, 76, 74, 79, 81, 79, 72, 76, 79, 84, 81, 79, 76, 74]
for i, m in enumerate(mel):
    te = 0.5 + i * 0.5
    if te > 8.9: break
    add(kalimba(nt(m)), te, 0.05, -.25 if i % 2 else .25)
    if i % 4 == 0: add(kalimba(nt(m - 24), 1.8), te, 0.06)
for e in json.load(open('events.json')):
    k, te, v, f = e['k'], e['t'], e.get('v', 1.0), e.get('f', 0)
    if k == 'lamp': add(noise(0.05, 1500, 8000, 0.006), te, 0.12)
    elif k == 'squish': add(squish(f), te, 0.35 * v, rs.uniform(-.2, .2))
    elif k == 'plop': add(plop(f), te, 0.45 * v, .2)
    elif k == 'pat': add(pat(), te, 0.4, .2)
    elif k == 'clink': add(clink(), te, 0.12 * v, .15)
    elif k == 'pour':
        add(trickle(e['d']), te, 0.08, .25)
        for j in range(int(e['d'] * 14)): add(drip(rs.uniform(900, 1700)), te + j / 14 + rs.uniform(0, .03), 0.12, rs.uniform(0, .4))
    elif k == 'step': add(step(), te, 0.4, -.2)
    elif k == 'pop': add(pop(f), te, 0.3 * v, rs.uniform(-.3, .3))
    elif k == 'boing': add(boing(), te, 0.22, -.2)
    elif k == 'stretch': add(stretch(e['d']), te, 0.16, .1)
    elif k == 'chime':
        for i, m in enumerate([72, 76, 79, 84]): add(chime(nt(m)), te + i * 0.06, 0.06)
# light room echo, master fades, soft limiter
for ch in (L, R):
    src = ch.copy()
    for dl, g in ((0.043, .18), (0.071, .12), (0.113, .07)): k = int(dl * SR); ch[k:] += src[:-k] * g
fi = int(0.2 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
