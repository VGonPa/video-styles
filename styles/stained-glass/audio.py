# events.json → audio.wav (48 kHz stereo, 10 s)
# a glass-and-stone score: a cool pre-dawn air bed that warms into a sustained pad as the sun rises,
# a glass clink for every piece set in the window (pitched by group), a spinning whoosh + chime chord as the
# petal ring opens, a rising swell into the push through the glass, a bright shimmer on the gold flash,
# soft taps as the title's glass letters drop in and bell tones as each one lights, a falling tail at the end.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(45)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def clink(f, d=.9):   # struck glass: inharmonic partials, fast decay, a tick of noise on the attack
    t = tt(d); s = sum(a * np.sin(2 * np.pi * f * k * t + rs.uniform(0, 6)) * np.exp(-t / dd) for k, a, dd in [(1, 1, .28), (2.32, .55, .16), (4.25, .3, .08), (6.7, .15, .04)])
    s += band(rs.standard_normal(len(t)), 3000, 12000) * np.exp(-t / .004) * .6
    return norm(s) * np.minimum(1, t * 3000)
def bell(f, d=2.2):
    t = tt(d); return norm(sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t / dd) for k, a, dd in [(1, 1, .9), (2.0, .35, .5), (3.01, .15, .25), (5.4, .06, .1)]))
def sweep(d, lo0, hi0, lo1, hi1, env):
    t = tt(d); x = rs.standard_normal(len(t)); out = np.zeros_like(x); K = 12; sl = len(t) // K + 1
    for k in range(K):
        a, b = k * sl, min(len(t), (k + 1) * sl); u = k / (K - 1); out[a:b] = band(x, lo0 + (lo1 - lo0) * u, hi0 + (hi1 - hi0) * u)[a:b]
    return norm(out) * env(t / d)
def pad(ms, d, att=.8):
    t = tt(d); s = sum(np.sin(2 * np.pi * nt(m) * t * (1 + dt)) for m in ms for dt in (-.002, .002)) / (2 * len(ms))
    return s * np.minimum(1, t / att) * np.minimum(1, (d - t) / .9)
t = np.arange(N) / SR
# bed: cool air before dawn, warming into a pad on A major as the sun rises
air = norm(band(rs.standard_normal(N), 250, 2200)) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 4.1) ** 2)
L += air * .012; R += np.roll(air, 900) * .012
dr = sum(a * np.sin(2 * np.pi * nt(m) * t + ph) for m, a, ph in [(33, .5, 0), (40, .3, 1), (45, .2, 2)])
L += dr * .035; R += dr * .035
ev = json.load(open('events.json'))
GP = {'hill': [64, 66, 69], 'sun': [76, 81], 'river': [73], 'wedge': [69, 71, 73, 76, 78, 81], 'petal': [81, 83, 85, 88], 'spandrel': [85, 88], 'band': [88, 90, 93], 'jewel': [93, 95, 97]}
for e in ev:
    k, te = e['k'], e['t']
    if k == 'clink':
        m = GP.get(e['g'], [81]); m = m[rs.integers(len(m))]; add(clink(nt(m)), te, .11, rs.uniform(-.6, .6))
    elif k == 'spin':
        add(sweep(1.1, 300, 1500, 1200, 7000, lambda u: np.sin(np.pi * u) ** 1.5), te, .12, -.3)
    elif k == 'chord':
        ms = [69, 73, 76, 81, 85] if e['n'] == 0 else [57, 64, 69, 73, 76, 81]
        for i, m in enumerate(ms): add(bell(nt(m), 2.6), te + i * .05, .045, -.5 + i * .22)
    elif k == 'swell':
        add(pad([57, 64, 69, 73], 2.4, 1.4), te, .5)
    elif k == 'rise':
        add(sweep(.95, 100, 600, 600, 6000, lambda u: u ** 2.2), te, .2)
        add(pad([69, 76, 81], .95, .7), te, .25)
    elif k == 'flash':
        add(sweep(1.6, 2000, 9000, 1500, 6000, lambda u: np.minimum(1, u * 30) * np.exp(-u * 3)), te, .1)
        for i, m in enumerate([88, 93, 97, 100]): add(bell(nt(m), 1.6), te + i * .04, .03, -.3 + i * .2)
        add(pad([45, 57, 64, 69, 73], 3.6, .25), te + .05, .45)
    elif k == 'tick': add(clink(nt(90 + (e['i'] % 3) * 2), .4), te, .05, -.6 + e['i'] * .1)
    elif k == 'bell':
        sc = [69, 71, 73, 76, 78, 81, 83, 85, 88, 90, 93, 95]; add(bell(nt(sc[e['i']]), 1.8), te, .05, -.6 + e['i'] * .1)
    elif k == 'chime':
        for i, m in enumerate([81, 85, 88]): add(bell(nt(m), 2.2), te + i * .12, .035, .2)
    elif k == 'fall': add(sweep(.9, 200, 3000, 60, 500, lambda u: np.sin(np.pi * u) * (1 - u)), te, .04)
# stone hall: a longer exponential-noise reverb
ir = rs.standard_normal(int(2.4 * SR)) * np.exp(-np.arange(int(2.4 * SR)) / SR / .6); ir = band(ir, 150, 7000); ir /= np.abs(ir).sum() ** .5 * 16
def conv(x):
    n = len(x) + len(ir); F = 1 << (n - 1).bit_length(); return np.fft.irfft(np.fft.rfft(x, F) * np.fft.rfft(ir, F), F)[:len(x)]
L, R = L + conv(L) * .55, R + conv(np.roll(R, 240)) * .55
fi = int(0.3 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.6) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
