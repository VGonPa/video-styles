# events.json → audio.wav (48 kHz stereo, 9.8 s) — hud: clean sine blips and ring ticks, two-tone caution beeps,
# rising "ok" chirps, RCS thruster puffs, fold whoosh + scan sweep, contact thud, clamp clunks, completion bell,
# a cabin hum bed that winds down with the power-down.
import json, wave, numpy as np
SR, DUR = 48000, 9.8
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(18)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def env(t, a, dec): return np.minimum(1, t / a) * np.exp(-t / dec)
def sine(f, d, a=0.002, dec=0.05): t = tt(d); return np.sin(2 * np.pi * f * t) * env(t, a, dec)
def norm(x): return x / (np.abs(x).max() + 1e-9)
def puff(d=0.32):     # RCS thruster: short hiss burst with a soft attack
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 700, 6000)); return n * np.minimum(1, t / 0.01) * np.exp(-t / 0.07)
def whoosh(d, lo=200, hi=2400):
    t = tt(d); X = np.fft.rfft(rs.standard_normal(len(t))); f = np.fft.rfftfreq(len(t), 1 / SR)
    out = np.zeros(len(t)); k = 8; w = len(t) // k
    for j in range(k):   # piecewise band sweep
        fc = lo + (hi - lo) * np.sin(np.pi * (j + 0.5) / k) ** 2
        Y = X.copy(); Y[(f < fc * 0.5) | (f > fc * 1.6)] = 0; y = np.fft.irfft(Y, len(t)); out[j * w:(j + 1) * w] = y[j * w:(j + 1) * w]
    return norm(out) * np.sin(np.pi * t / d) ** 1.5
def thud():
    t = tt(0.6); f = 120 * np.exp(-t * 9) + 45; ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.12) + 0.3 * norm(band(rs.standard_normal(len(t)), 100, 1500)) * np.exp(-t / 0.03)
def clunk():
    t = tt(0.3); m = np.sin(2 * np.pi * 310 * t) * np.exp(-t / 0.05) + 0.5 * np.sin(2 * np.pi * 740 * t) * np.exp(-t / 0.03)
    return m + 0.6 * norm(band(rs.standard_normal(len(t)), 1500, 8000)) * np.exp(-t / 0.004)
# bed: low cabin hum + faint air, fades in with the boot, winds down (pitch falls) with the power-down
t = np.arange(N) / SR; off0, off1 = 8.85, 9.5
drop = np.clip((t - off0) / (off1 - off0), 0, 1)
fr = 55 * (1 - 0.6 * drop ** 1.5); ph = 2 * np.pi * np.cumsum(fr) / SR
hum = (np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.12 * np.sin(3 * ph)) * np.clip(t / 0.8, 0, 1) * (1 - drop) ** 1.2
L += hum * 0.03; R += hum * 0.03
air = norm(band(rs.standard_normal(N), 300, 2500)) * np.clip(t / 1.0, 0, 1) * (1 - drop); L += air * 0.004; R += np.roll(air, 999) * 0.004
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'tick': add(sine(3200, 0.03, 0.0005, 0.004), te, 0.10, rs.uniform(-.3, .3))
    elif k == 'blip': add(sine(2093, 0.2, 0.002, 0.035), te, 0.10, -0.4); add(sine(2637, 0.2, 0.002, 0.04), te + 0.05, 0.08, -0.4)
    elif k == 'warn':
        for j in range(2): add(sine(740, 0.16, 0.004, 0.07), te + j * 0.16, 0.10, 0.35); add(sine(587, 0.16, 0.004, 0.07), te + j * 0.16 + 0.08, 0.09, 0.35)
    elif k == 'beep': add(sine(740, 0.12, 0.004, 0.04), te, 0.035, 0.35)
    elif k == 'ok':
        for j, f in enumerate([1175, 1568]): add(sine(f, 0.25, 0.002, 0.06), te + j * 0.06, 0.08, 0.35)
    elif k == 'rcs': add(puff(), te, 0.16, rs.uniform(-.5, .5))
    elif k == 'ping': add(sine(1396, 1.0, 0.003, 0.28) + 0.3 * sine(2793, 1.0, 0.003, 0.2), te, 0.10)
    elif k == 'sweep': add(whoosh(0.8), te, 0.12); add(sine(82, 0.6, 0.01, 0.18), te, 0.25)
    elif k == 'scan':
        d = 0.6; tt_ = tt(d); s = np.sin(2 * np.pi * np.cumsum(900 + 1400 * tt_ / d) / SR) * np.sin(np.pi * tt_ / d) ** 2; add(s, te, 0.025, 0.2)
    elif k == 'thud': add(thud(), te, 0.45)
    elif k == 'clunk': add(clunk(), te, 0.22, rs.uniform(-.3, .3))
    elif k == 'chime':
        for j, f in enumerate([1318.5, 1975.5, 2637]): add(sine(f, 1.4, 0.003, 0.4), te + j * 0.07, 0.07)
    elif k == 'down':
        d = 0.7; tt_ = tt(d); s = np.sin(2 * np.pi * np.cumsum(1400 * np.exp(-tt_ * 4) + 60) / SR) * np.exp(-tt_ / 0.3); add(s, te, 0.07)
# master: fades, soft limiter
fi = int(0.2 * SR); fo = int(0.4 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
