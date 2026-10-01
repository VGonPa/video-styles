# events.json → audio.wav (48 kHz stereo, 10 s)
# a toy-box score: soft plucked-string melody (Karplus-Strong), muffled felt "puffs" as pieces land,
# bird chirps and wing flutters, a wool pluck, wind and pattering rain under the cotton cloud,
# a glassy shimmer for the sun, a rising xylophone run as each rainbow strand is laid, title pops, last chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(127)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def ks(f, d, bright=0.5):
    # Karplus-Strong plucked string
    n = int(d * SR); p = max(2, int(SR / f)); buf = band(rs.standard_normal(p * 4), 50, 3000 + 6000 * bright)[:p]
    out = np.zeros(n); b = buf.copy()
    for i in range(0, n, p):
        k = min(p, n - i); out[i:i + k] = b[:k]; b = 0.996 * 0.5 * (b + np.roll(b, 1))
    return norm(out) * np.exp(-tt(d) / (d * 0.45))
def puff(v=1.0):
    t = tt(0.14); n = norm(band(rs.standard_normal(len(t)), 80, 900)) * np.exp(-t / 0.03)
    return (n * 0.7 + np.sin(2 * np.pi * 95 * t) * np.exp(-t / 0.04) * 0.5) * v
def chirp(v=1.0):
    out = np.zeros(int(0.32 * SR))
    for k, (f0, f1, st) in enumerate([(2600, 3900, 0.0), (3000, 4300, 0.11), (2400, 3600, 0.2)]):
        t = tt(0.07); f = f0 + (f1 - f0) * np.sin(np.pi * t / 0.07); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.07) ** 2
        i = int(st * SR); out[i:i + len(s)] += s
    return out * 0.5 * v
def flap(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 300, 2500))
    am = (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 6 * t))) * np.exp(-((t * 12) % 1) * 5)
    return n * am * np.sin(np.pi * t / d) ** 0.5 * 0.5
def pluck():
    t = tt(0.22); n = norm(band(rs.standard_normal(len(t)), 1200, 6000))
    am = np.abs(band(rs.standard_normal(len(t)), 30, 160)); am = norm(am)
    return n * am * np.exp(-t / 0.07) * 0.6
def wind(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 150, 700))
    return n * np.sin(np.pi * t / d) ** 2 * (0.7 + 0.3 * np.sin(2 * np.pi * 0.7 * t))
def rain(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 1500, 9000))
    return n * np.clip(np.minimum(t / 0.5, (d - t) / 0.6), 0, 1) * 0.18
def pat(v):
    t = tt(0.04); return norm(band(rs.standard_normal(len(t)), 1500, 7000)) * np.exp(-t / 0.006) * (0.25 + 0.2 * v)
def plink(v):
    t = tt(0.25); f = (1300 + 500 * v) * (1 + 0.3 * np.exp(-t * 40)); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05) * 0.3
def bell(f, d=1.2):
    t = tt(d); return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.15)) * np.exp(-t / (d * 0.3))
def shine():
    out = np.zeros(int(1.2 * SR))
    for k, m in enumerate([84, 88, 91, 96]):
        s = bell(hz(m), 0.9) * 0.25; i = int(k * 0.05 * SR); out[i:i + len(s)] += s[:len(out) - i]
    return out
def shake(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 400, 4000))
    return n * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 12 * t))) * 0.35
def pop(f):
    t = tt(0.3); fr = f * (1 + 0.6 * np.exp(-t * 60)); return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.07) * 0.7

ev = json.load(open('events.json'))
for e in ev:
    k, t, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'puff': add(puff(v), t, 0.55)
    elif k in ('land', 'hop'): add(puff(0.8), t, 0.5, 0.2)
    elif k == 'twig': add(puff(1.0), t, 0.6, 0.1); add(pluck(), t, 0.25, 0.1)
    elif k == 'chirp': add(chirp(v), t, 0.35, 0.3)
    elif k == 'flap': add(flap(e['d']), t, 0.4, 0.4)
    elif k == 'pluck': add(pluck(), t, 0.55, -0.3)
    elif k == 'wind': add(wind(e['d']), t, 0.35, -0.2)
    elif k == 'rain': add(rain(e['d']), t, 1.0, 0.0)
    elif k == 'pat': add(pat(v), t, 0.6, rs.uniform(-0.6, 0.6))
    elif k == 'plink': add(plink(v), t, 0.5, 0.5)
    elif k == 'shake': add(shake(e['d']), t, 0.6, -0.2)
    elif k == 'shine': add(shine(), t, 0.6, 0.5)
    elif k == 'note': add(bell(hz([72, 74, 76, 79, 81, 84][e['i']]), 1.0), t, 0.32, -0.5 + e['i'] * 0.2)
    elif k == 'pop': add(pop(e['f']), t, 0.45)
    elif k == 'chord':
        for m in (60, 64, 67, 72, 76): add(ks(hz(m), 2.2, 0.4), t + (m - 60) * 0.006, 0.18)

# gentle plucked melody (C major, 110 bpm) — quieter and minor-tinged under the rain, back for the rainbow
beat = 60 / 110 / 2
mel = [(0.5, 67), (1, 72), (1.5, 76), (2, 74), (2.5, 72), (3, 67), (3.5, 69), (4, 72), (5, 76), (5.5, 79), (6, 77), (6.5, 76), (7, 74),
       (8.5, 72), (9, 76), (9.5, 74), (10, 72), (11, 67), (11.5, 69), (12, 72), (13, 74), (13.5, 72), (14, 71)]
for b, m in mel: add(ks(hz(m), 0.9, 0.5), b * beat, 0.16, 0.15)
for b, m in [(16, 69), (17, 72), (18, 76), (19, 72), (20, 69), (21, 71), (22, 67)]:  # under the cloud: A minor
    add(ks(hz(m), 0.9, 0.3), 3.9 + (b - 16) * beat * 1.5, 0.1, 0.1)
bass = [(0.5, 48), (2.4, 45), (4.3, 41), (6.2, 43), (7.4, 48)]
for t0, m in bass: add(ks(hz(m), 1.6, 0.25), t0, 0.18, -0.15)

fi = int(0.2 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
