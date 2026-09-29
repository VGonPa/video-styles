# events.json → audio.wav (48 kHz stereo, 10 s)
# papyrus crackle as the sheet and each register unroll, plucked harp (Karplus-Strong) for the cartouche and captions,
# a warm reed drone as the sun comes up, river water under the flood, wing flutter, soft hoof thuds for the plough team,
# sickle swishes, a pour of grain onto the heap, and a closing harp phrase into the fade.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(95)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)

def crackle(d, dens=240):   # dry papyrus: soft hiss + sparse crackles
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 1200, 9000)) * 0.25
    k = np.zeros(len(t)); idx = rs.integers(0, len(t), int(dens * d)); k[idx] = rs.uniform(0.3, 1, len(idx)) * rs.choice([-1, 1], len(idx))
    k = band(k, 800, 12000); env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.7
    return (n + norm(k)) * env
def harp(f, d=2.2, bright=0.5):   # Karplus-Strong plucked string
    n = int(d * SR); p = max(2, int(SR / f)); buf = rs.uniform(-1, 1, p); out = np.zeros(n)
    buf = band(np.concatenate([buf] * 4), 0, 6000)[:p] if p > 8 else buf
    for i in range(n):
        out[i] = buf[i % p]; j = (i + 1) % p
        buf[i % p] = 0.5 * (buf[i % p] + buf[j]) * (0.994 + 0.004 * bright)
    return out * np.minimum(1, np.arange(n) / 60)
def drone(d, f0=110):   # reed-like drone with a slow swell
    t = tt(d); ph = 2 * np.pi * f0 * t; s = np.sign(np.sin(ph)) * 0.3 + np.sin(ph) + 0.4 * np.sin(2 * ph + 0.3) + 0.2 * np.sin(3 * ph)
    s = band(s, 60, 1400) * (1 + 0.08 * np.sin(2 * np.pi * 4.5 * t)); env = np.clip(t / (d * 0.5), 0, 1) ** 1.5 * np.clip((d - t) / 0.8, 0, 1)
    return norm(s) * env
def thud():
    t = tt(0.18); return (np.sin(2 * np.pi * (85 + 40 * np.exp(-t * 30)) * t) * np.exp(-t / 0.05) + 0.3 * band(rs.standard_normal(len(t)), 200, 1200) * np.exp(-t / 0.015))
def swish(d=0.22):
    t = tt(d); n = rs.standard_normal(len(t)); out = np.zeros(len(t)); seg = len(t) // 6
    for k in range(6):
        a, b = k * seg, (k + 1) * seg; lo = 600 + 700 * k; out[a:b] = band(n, lo, lo + 2500)[a:b]
    return norm(out) * np.sin(np.pi * t / d) ** 2
def snip():
    t = tt(0.05); return band(rs.standard_normal(len(t)), 2500, 11000) * np.exp(-t / 0.006)
def flutter(d=0.6):
    t = tt(d); n = band(rs.standard_normal(len(t)), 300, 3000); am = (0.5 + 0.5 * np.sin(2 * np.pi * 14 * t)) ** 3
    return norm(n) * am * np.sin(np.pi * t / d)
def pour(d):
    t = tt(d); out = np.zeros(len(t)); idx = rs.integers(0, len(t), int(1400 * d)); out[idx] = rs.uniform(0.2, 1, len(idx))
    out = band(out, 1500, 9000) + 0.3 * band(rs.standard_normal(len(t)), 400, 3000)
    return norm(out) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.6

ev = json.load(open('events.json'))
E = {}
for e in ev: E.setdefault(e['k'], e)
t = np.arange(N) / SR
# river bed: rises with the flood, settles to a quiet flow
fl = E['flood']; f0, f1 = fl['t'], fl['t'] + fl['d']
water = norm(band(rs.standard_normal(N), 150, 1600)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.7 * t)); water2 = norm(band(rs.standard_normal(N), 150, 1600))
wg = np.clip((t - f0 + 0.4) / 0.8, 0, 1) * (0.05 - 0.03 * np.clip((t - (f1 - 0.6)) / 0.8, 0, 1))
L += water * wg; R += water2 * wg
scale = [62, 64, 67, 69, 71, 74, 76, 79]   # pentatonic on D
for e in ev:
    k, te = e['k'], e['t']
    if k == 'open': add(crackle(e['d'] + 0.2, 300), te, 0.16, 0.0)
    elif k == 'roll': add(crackle(e['d'], 180), te, 0.09, -0.6 + 0.6 * (te > 2) + 0.3 * (te > 3.5))
    elif k == 'ring': add(harp(nt(50), 3.0), te, 0.22, -0.1)
    elif k == 'title':
        for i, m in enumerate([62, 67, 69, 74]): add(harp(nt(m), 2.2), te + i * 0.14, 0.14, -0.3 + i * 0.2)
    elif k == 'sun': add(drone(DUR - te, 73.4), te, 0.06, 0.0); add(drone(DUR - te, 110), te + 0.3, 0.03, 0.2)
    elif k == 'ducks':
        for i in range(4): add(flutter(0.5 + 0.1 * i), te + i * 0.28, 0.06, 0.6 - i * 0.35)
    elif k == 'hoof': add(thud(), te, 0.05, 0.1)
    elif k == 'chop': add(swish(), te, 0.05, -0.45); add(snip(), te + 0.12, 0.06, -0.45)
    elif k == 'pour': add(pour(e['d']), te, 0.08, 0.55)
    elif k == 'cap': add(harp(nt(79), 1.6), te, 0.08, 0.2)
    elif k == 'end':
        for i, m in enumerate([74, 71, 69, 67, 62]): add(harp(nt(m), 2.6), te + i * 0.2, 0.13, 0.4 - i * 0.18)
        add(harp(nt(50), 3.0), te + 1.05, 0.14, 0.0)
fi = int(0.2 * SR); fo = int(0.8 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.6
st = np.stack([L, R], 1); st = np.tanh(st * 2.2) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
