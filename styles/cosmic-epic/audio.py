# events.json -> audio.wav (48 kHz stereo, 10 s). Everything is synthesized (no samples):
# a slow D-minor drone bed with a sub hum, a glassy shimmer as the star clears the planet's limb,
# a rising riser while the star swells, a reversed "inhale" as it collapses, a deep sub-bass
# supernova boom with a crackling tail, soft ticks as the timeline counter races ahead, a high
# airy pad as the stars go out, and one low bell for the final title. FFT-convolution hall reverb.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N); WL = np.zeros(N); WR = np.zeros(N); wet = (WL, WR)
rs = np.random.default_rng(79)
def add(sig, t, g=1.0, pan=0.0, dst=None):
    i = int(t * SR); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    l, r = (L, R) if dst is None else dst
    l[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; r[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def pad(ms, d, att, rel, bright=0.2):
    t = tt(d); s = np.zeros_like(t)
    for m in ms:
        for det in (-0.08, 0.0, 0.07):
            f = nt(m) * 2 ** (det / 12); ph = rs.uniform(0, 6.28)
            s += np.sin(2 * np.pi * f * t + ph) + bright * np.sin(4 * np.pi * f * t + ph) + bright * 0.4 * np.sin(6 * np.pi * f * t)
    return s * np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1) / (3 * len(ms))
def tick(v):
    t = tt(0.06); f = 2600 if v < 1 else 1500
    return (np.sin(2 * np.pi * f * t) * 0.6 + band(rs.standard_normal(len(t)), 2000, 9000) * 0.25) * np.exp(-t / 0.008)
def shimmer(d):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * nt(m) * t + rs.uniform(0, 6)) for m, a in [(86, .5), (89, .35), (93, .35), (98, .2), (101, .12)])
    return s * np.minimum(1, t / (d * 0.35)) * np.clip((d - t) / (d * 0.6), 0, 1) * (0.8 + 0.2 * np.sin(2 * np.pi * 6.3 * t))
def riser(d):
    t = tt(d); k = t / d; f = 110 * 2 ** (2.2 * k ** 1.6)
    ph = 2 * np.pi * np.cumsum(f) / SR; s = sum(np.sin(ph * h * (1 + 0.003 * h)) / h for h in range(1, 7))
    nz = band(rs.standard_normal(len(t)), 300, 6000) * 0.15 * k
    return (s * 0.5 + nz) * k ** 2.2 * np.clip((d - t) / 0.08, 0, 1)
def inhale(d):
    t = tt(d); x = band(rs.standard_normal(len(t)), 200, 8000); x /= np.abs(x).max()
    return x * (t / d) ** 3.5 * np.clip((d - t) / 0.03, 0, 1)
def boom(d=4.5):
    t = tt(d); f = 26 + 44 * np.exp(-t / 0.35); ph = 2 * np.pi * np.cumsum(f) / SR
    sub = np.sin(ph) * np.exp(-t / 1.3) * np.minimum(1, t / 0.004)
    nz = band(rs.standard_normal(len(t)), 30, 1800); nz /= np.abs(nz).max()
    body = nz * np.exp(-t / 0.7) * 0.8
    crack = band(rs.standard_normal(len(t)), 1500, 9000) * (rs.random(len(t)) < 0.004) * 6 * np.exp(-t / 1.6)
    return sub * 1.0 + body + crack * 0.25
def bell(m, d=2.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * nt(m) * r * t) * np.exp(-t / (d * 0.45 / r ** 0.5)) for r, a in [(1, 1), (2.0, .4), (2.76, .25), (5.4, .1)])
    return s * np.minimum(1, t / 0.01)

# drone bed: D minor, swelling to the burst, then a hollow fifth that thins to nothing
add(pad([38, 45, 50, 53], 5.4, att=2.5, rel=0.3, bright=0.25), 0.0, 0.22, -0.1, wet)
add(pad([26, 38], 5.3, att=1.5, rel=0.2, bright=0.05), 0.0, 0.26, 0.0)
add(pad([38, 45, 57, 62, 64], 3.2, att=0.8, rel=2.2, bright=0.15), 5.2, 0.14, 0.1, wet)
add(pad([81, 86, 88, 93], 3.2, att=0.9, rel=2.0, bright=0.0), 5.6, 0.06, 0.2, wet)
ev = json.load(open('events.json'))
for e in ev:
    k, te = e['k'], e['t']
    if k == 'tick': add(tick(e['v']), te, 0.14 * e['v'], rs.uniform(-0.3, 0.3), None); add(tick(e['v']), te, 0.05, 0, wet)
    elif k == 'emerge': add(shimmer(2.6), te - 0.35, 0.12, 0.25, wet)
    elif k == 'swell': add(riser(1.4), te + 0.05, 0.13, -0.05, wet)
    elif k == 'collapse': TB = next(x['t'] for x in ev if x['k'] == 'burst'); add(inhale(TB - te), te, 0.3, 0.0, wet)
    elif k == 'burst': add(boom(), te, 0.7, 0.0); add(boom(), te, 0.3, 0.0, wet)
    elif k == 'title': add(bell(38, 2.2), te, 0.45, -0.05, wet); add(bell(45, 2.2), te + 0.02, 0.25, 0.1, wet); add(bell(74, 1.6), te + 0.7, 0.1, 0.2, wet)
# hall: decaying stereo noise IR (~3.5 s), FFT convolution
ir_t = tt(3.5); M = 1 << int(np.ceil(np.log2(N + len(ir_t))))
for dry, w_, seed in ((L, WL, 1), (R, WR, 2)):
    ir = np.random.default_rng(seed).standard_normal(len(ir_t)) * np.exp(-ir_t / 0.9); ir = band(ir, 40, 7000); ir /= np.sqrt(np.sum(ir ** 2))
    rev = np.fft.irfft(np.fft.rfft(w_, M) * np.fft.rfft(ir, M), M)[:N]
    dry += w_ * 0.6 + rev * 0.45
fi = int(0.4 * SR); fo = int(0.8 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); pk = np.abs(st).max(); st = np.tanh(st / pk * 1.3) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok, peak before norm', round(float(pk), 3))
