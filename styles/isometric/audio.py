# events.json → audio.wav (48 kHz stereo, 10 s)
# the original clip's toy-synth palette (pop, blip, bloop, thud, tick, clack, boing, chime) plus
# little engine buzz, conveyor rumble, tape zip, scanner sweep, doorbell and a soft whoosh; warm pad bed.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(7)
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
def gen(k, e):
    f = e.get('f', 0)
    if k == 'pop': return sweep(f, f * 0.45, 0.09, 0.03)
    if k == 'blip': return sweep(f, f, 0.12, 0.035)
    if k == 'bloop': return sweep(f, f * 2.4, 0.16, 0.06)
    if k == 'bloopdn': return sweep(f, f * 0.4, 0.2, 0.07)
    if k == 'thud': return sweep(f, f * 0.6, 0.3, 0.09)
    if k == 'clack': return sweep(f, f * 0.7, 0.05, 0.012, lambda x: np.sign(np.sin(x)) * 0.5)
    if k == 'chime':
        n = int(SR * 1.4); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.5 * t) + 0.25 * np.sin(2 * np.pi * f * 2.01 * t)) / 1.75 * env(n, 0.4)
    if k == 'boing':
        n = int(SR * 0.35); t = np.arange(n) / SR
        fr = f * (1 + 0.6 * np.exp(-t * 9) * np.sin(2 * np.pi * 14 * t)); return np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(n, 0.12)
    if k == 'zip':
        d = e['d']; t = tt(d); x = band(rs.standard_normal(len(t)), 1500, 7000); am = 0.6 + 0.4 * np.sign(np.sin(2 * np.pi * (60 + 80 * t / d) * t))
        return x / np.abs(x).max() * am * np.sin(np.pi * t / d) ** 0.4 * 0.6
    if k == 'scan':
        d = 0.3; t = tt(d); fr = 900 + 1800 * t / d; return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * t / d) * 0.5
    if k == 'ding':
        out = np.zeros(int(SR * 1.6))
        for off, fr in [(0, 1319), (0.28, 1047)]:
            n = int(SR * 1.2); t = np.arange(n) / SR; s = (np.sin(2 * np.pi * fr * t) + 0.3 * np.sin(2 * np.pi * fr * 2.76 * t) * np.exp(-t / 0.08)) * env(n, 0.45)
            i = int(off * SR); out[i:i + n] += s[:len(out) - i]
        return out
    if k == 'engine':  # small toy motor: buzzy low tone with a quick putter, rises and falls with speed
        d = e['d']; t = tt(d); sp = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.7
        fr = f * (1 + 0.5 * sp); ph = 2 * np.pi * np.cumsum(fr) / SR
        s = (np.sign(np.sin(ph)) * 0.3 + np.sin(ph * 2) * 0.4) * (0.75 + 0.25 * np.sin(2 * np.pi * 22 * t))
        return band(s, 40, 1400) * (0.35 + 0.65 * sp) * np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.15)
    if k == 'belt':
        d = e['d']; t = tt(d); x = band(rs.standard_normal(len(t)), 80, 500) * 0.5
        rattle = np.sign(np.sin(2 * np.pi * 10 * t)) * np.exp(-((t * 10) % 1) / 0.08) * 0.15
        return (x / np.abs(x).max() + rattle * band(rs.standard_normal(len(t)), 1500, 4000)) * np.minimum(1, t / 0.08) * np.minimum(1, (d - t) / 0.1) * 0.5
    if k == 'whoosh':
        d = e['d']; t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
        a = np.exp(-2 * np.pi * (200 + 1800 * np.sin(np.pi * t / d) ** 2) / SR)
        for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
        return y / (np.abs(y).max() + 1e-9) * np.sin(np.pi * t / d) ** 1.5
    raise ValueError(k)
# bed: warm pad (C major 6/9), gentle swell into the title
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR
for m, g, p in [(48, .03, -.3), (55, .022, .3), (64, .016, 0), (69, .012, .2)]:
    s = sum(a * np.sin(2 * np.pi * nt(m) * h * t) for h, a in [(1, 1), (2, .25)]) * (1 + .15 * np.sin(2 * np.pi * .3 * t))
    swell = np.clip(t / 1.2, 0, 1) * (0.8 + 0.5 * np.clip((t - 7.8) / 1.0, 0, 1)); add(s * swell, 0, g, p)
pans = {'engine': 0, 'belt': .2, 'scan': .25, 'ding': .3}
for e in json.load(open('events.json')):
    k, v = e['k'], e.get('v', 0.3)
    add(gen(k, e), e['t'], v, pans.get(k, rs.uniform(-.35, .35)))
fi = int(0.2 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
