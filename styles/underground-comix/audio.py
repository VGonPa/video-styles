# events.json -> audio.wav (48 kHz stereo, 10 s)
# A 120 bpm late-60s groove, all synthesized: kick on every one of Mel's steps, snare backbeat,
# tambourine-ish hats, a round bass line and a fuzz-guitar riff (detuned saws through a hard tanh
# clip) that gets a wah sweep once the sky turns psychedelic. Rubbery squish before the sun bursts,
# a reverse-swell into a crash, wood-block ticks as the title letters land, drip bloops, and a held
# fuzz power chord with vibrato as the camera pulls back to the comic page, then a soft thud.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(62)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def saw(f, t): return 2 * ((f * t) % 1) - 1
def kick():
    t = tt(0.35); f = 45 + 110 * np.exp(-t * 28); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.12) + 0.3 * norm(band(rs.standard_normal(len(t)), 1000, 5000)) * np.exp(-t / 0.004)
def snare():
    t = tt(0.25); n = norm(band(rs.standard_normal(len(t)), 900, 7000))
    return n * np.exp(-t / 0.07) * 0.8 + np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.5
def hat(open_=False):
    t = tt(0.2 if open_ else 0.06); n = norm(band(rs.standard_normal(len(t)), 6000, 14000))
    return n * np.exp(-t / (0.07 if open_ else 0.015))
def crash():
    t = tt(2.2); n = norm(band(rs.standard_normal(len(t)), 3000, 15000)); return n * np.exp(-t / 0.7)
def fuzz(freq, d, vib=0.0):
    t = tt(d); f = freq * (1 + vib * 0.012 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t / 0.4))
    ph = np.cumsum(f) / SR
    x = (2 * (ph % 1) - 1) + (2 * ((ph * 1.006) % 1) - 1) + 0.5 * np.sin(2 * np.pi * ph * 0.5)
    y = np.tanh(x * 7.0)
    env = np.minimum(1, t / 0.006) * np.minimum(1, (d - t) / 0.03)
    return band(y, 80, 4200) * env
def bass(freq, d):
    t = tt(d); x = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(4 * np.pi * freq * t)
    return np.tanh(1.5 * x) * np.exp(-t / 0.45) * np.minimum(1, t / 0.005) * np.minimum(1, (d - t) / 0.02)
def block(freq):
    t = tt(0.12); return np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.025)
def bloop():
    t = tt(0.22); f = 300 + 900 * np.sin(np.pi * np.minimum(1, t / 0.12)) * np.exp(-t * 6); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.sin(np.pi * t / 0.22) ** 0.6
def pop():
    t = tt(0.12); f = 600 * np.exp(-t * 30) + 250; ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.03)
def squish():
    t = tt(0.5); f = 420 * np.exp(-t * 3) + 80 + 40 * np.sin(2 * np.pi * 22 * t); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(3 * np.sin(ph)) * np.sin(np.pi * t / 0.5) ** 0.8
def swell(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 500, 9000)); return n * (t / d) ** 3
def whoosh(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 200, 2500)); return n * np.sin(np.pi * t / d) ** 2

B = 0.5; E8 = 0.25
bus_g = np.zeros(N)                                   # guitar bus (wah later)
def addg(sig, t0, g):
    i = int(t0 * SR); n = min(len(sig), N - i)
    if n > 0: bus_g[i:i + n] += sig[:n] * g
# riff: E minor pentatonic, one bar of eighths (2 s), repeated; the last bar lands on a held chord
riff = [40, None, 40, 43, 45, None, 46, 45, 43, 40, None, 38, 40, None, 43, None]
bassl = [28, 28, 31, 33, 28, 28, 26, 26]
for i in range(int(8.0 / E8)):
    tb = 0.25 + i * E8
    if tb >= 8.25: break
    m = riff[i % 16]
    g = 0.45 if tb < 2.25 else (0.7 if tb < 4.25 else 1.0)
    if m is not None: addg(fuzz(nt(m + 12), E8 * 0.92), tb, 0.10 * g)
    if i % 2 == 0: add(bass(nt(bassl[(i // 2) % 8]), B * 0.95), tb, 0.30, -0.1)
# held power chord E-B-E with vibrato
for m in (40, 47, 52): addg(fuzz(nt(m + 12), 1.7, vib=1.0) * np.exp(-tt(1.7) / 0.9), 8.25, 0.075)
# wah on the guitar bus from the burst on (state-variable band-pass, swept to the beat)
tg = np.arange(N) / SR
fc = 500 + 1600 * (0.5 + 0.5 * np.sin(2 * np.pi * 1.0 * (tg - 0.25)))
fcoef = 2 * np.sin(np.pi * np.clip(fc, 100, 6000) / SR); q = 0.35
low = band_ = 0.0; wah = np.zeros(N)
x = bus_g
for i in range(int(4.15 * SR), N):
    hp = x[i] - low - q * band_; band_ += fcoef[i] * hp; low += fcoef[i] * band_; wah[i] = band_
mix = np.clip((tg - 4.15) / 0.3, 0, 1) * 0.75
guitar = x * (1 - mix) + wah * mix * 2.2
L += guitar * 1.0; R += np.roll(guitar, 480) * 0.9       # little stereo spread
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'step':
        n = round((te - 0.25) / B)
        add(kick(), te, 0.55)
        if n % 2 == 1: add(snare(), te, 0.28, 0.1)
        add(hat(n % 4 == 3), te + 0.25, 0.07, 0.35); add(hat(), te, 0.05, 0.35)
    elif k == 'pop': add(pop(), te, 0.22 * e.get('v', 1))
    elif k == 'squish': add(squish(), te, 0.16, 0.2)
    elif k == 'burst': add(swell(0.5), te - 0.5, 0.18); add(crash(), te, 0.22); add(kick(), te, 0.4)
    elif k == 'tick': add(block(900 + 60 * e['v']), te, 0.09, -0.4 + 0.06 * e['v'])
    elif k == 'drip': add(bloop(), te, 0.09, rs.uniform(-.5, .5))
    elif k == 'pull': add(whoosh(0.9), te, 0.12); add(crash(), te, 0.12)
    elif k == 'thud': add(kick(), te, 0.45); add(block(180), te, 0.2)
fi = int(0.15 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.6) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
