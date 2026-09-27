# events.json → audio.wav (48 kHz stereo, 10 s)
# sea ambience bed (surf swells), hyoshigi clappers, baren rubbing, koto plucks (in-scale), wooden tocks,
# a rumbling rise, the crash (noise burst + taiko), falling spray hiss, the seal thud and a closing koto chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(38)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def clack():
    t = tt(0.25); s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, d in [(1450, .03), (2380, .02), (3600, .012)])
    return norm(s + 0.6 * band(rs.standard_normal(len(t)), 1500, 8000) * np.exp(-t / .004))
def tock(f=520):
    t = tt(0.2); return norm(np.sin(2 * np.pi * f * t) * np.exp(-t / .04) + .5 * np.sin(2 * np.pi * f * 2.7 * t) * np.exp(-t / .015) + .3 * band(rs.standard_normal(len(t)), 800, 5000) * np.exp(-t / .003))
def rub(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 600, 6000); am = 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 7 * t))
    return norm(n) * am * np.sin(np.pi * t / d) ** 0.8
def koto(f, d=2.2):
    n = int(d * SR); P = int(SR / f); buf = rs.uniform(-1, 1, P) * np.hanning(P); out = np.zeros(n)
    for i in range(n): out[i] = buf[i % P]; buf[i % P] = 0.5 * (buf[i % P] + buf[(i + 1) % P]) * 0.9965
    t = np.arange(n) / SR; bend = 1 + 0.0 * t
    return norm(out) * np.exp(-t / 0.9)
def taiko():
    t = tt(1.4); f = 95 * np.exp(-t * 3) + 55; ph = 2 * np.pi * np.cumsum(f) / SR
    return norm(np.sin(ph) * np.exp(-t / .35) + .4 * band(rs.standard_normal(len(t)), 60, 900) * np.exp(-t / .05))
def noise_sweep(d, lo0, hi0, lo1, hi1, env):
    t = tt(d); x = rs.standard_normal(len(t)); out = np.zeros_like(x); K = 8; seglen = len(t) // K + 1
    for k in range(K):
        a, b = k * seglen, min(len(t), (k + 1) * seglen); u = k / (K - 1)
        out[a:b] = band(x, lo0 + (lo1 - lo0) * u, hi0 + (hi1 - hi0) * u)[a:b]
    return norm(out) * env(t / d)
# bed: surf — band-limited noise with slow swells, stereo-decorrelated
t = np.arange(N) / SR
for ch, sh in ((L, 0), (R, 1.3)):
    s = band(rs.standard_normal(N), 120, 2400); sw = 0.55 + 0.45 * np.sin(2 * np.pi * (t / 3.1) + sh) ** 2
    ch += norm(s) * sw * 0.05
low = band(rs.standard_normal(N), 30, 180); L += norm(low) * 0.05; R += norm(low) * 0.05
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'clack': add(clack(), te, 0.35 * v, -.2); add(clack(), te + 0.045, 0.22 * v, .2)
    elif k == 'rub': add(rub(e['d']), te, 0.08, -.3 + .6 * (te > .5))
    elif k == 'tock': add(tock(), te, 0.25 * v, -.4)
    elif k == 'koto': add(koto(nt(e['n'])), te, 0.2, rs.uniform(-.35, .35))
    elif k == 'rise': d = e['d']; add(noise_sweep(d, 40, 300, 100, 2500, lambda u: u ** 2.2), te, 0.32)
    elif k == 'crash': add(noise_sweep(1.6, 200, 9000, 80, 2500, lambda u: np.exp(-u * 3.2) * np.minimum(1, u * 40)), te, 0.6)
    elif k == 'taiko': add(taiko(), te, 0.55)
    elif k == 'splash':
        d = e['d']; add(noise_sweep(d, 2000, 11000, 3000, 12000, lambda u: np.exp(-u * 2.5)), te, 0.12, .2)
        for i in range(14): add(tock(1800 + rs.uniform(0, 1500)) * 0.5, te + rs.uniform(0, d * .8), 0.03, rs.uniform(-.6, .6))
    elif k == 'seal':
        add(taiko() * 0.4 + np.pad(tock(260), (0, int(1.4 * SR) - int(0.2 * SR))), te, 0.35)
    elif k == 'chord':
        for i, m in enumerate([52, 57, 59, 64, 69]): add(koto(nt(m), 2.0), te + 0.1 + i * 0.07, 0.14, -.4 + i * .2)
fi = int(0.2 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.5) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
