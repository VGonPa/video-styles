# events.json → audio.wav (48 kHz stereo, 10 s)
# office room tone (HVAC air + fluorescent hum), distant keyboards that fall silent for the beat,
# paper slides, soft panel "prints", balloon pops, pointer taps on the whiteboard, a wall clock
# ticking through the pause, a felt-marker strike, and a dry two-note marimba sign-off.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(85)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def key():
    t = tt(0.05); n = band(rs.standard_normal(len(t)), 1500, 6000) * np.exp(-t / 0.004)
    return 0.6 * norm(n) + 0.4 * np.sin(2 * np.pi * (190 + 50 * rs.random()) * t) * np.exp(-t / 0.01)
def slide(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 500, 6000)
    am = np.abs(band(rs.standard_normal(len(t)), 3, 30)); am = norm(am) * 0.5 + 0.5
    return norm(n) * am * np.sin(np.pi * t / d) ** 1.2
def printp():  # soft paper "thup" as a panel appears
    t = tt(0.18); n = band(rs.standard_normal(len(t)), 200, 3000) * np.exp(-t / 0.02)
    return 0.6 * norm(n) + 0.5 * np.sin(2 * np.pi * 95 * t) * np.exp(-t / 0.04)
def pop():
    t = tt(0.12); f = 520 * np.exp(-t * 30) + 300; ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.03) + 0.2 * norm(band(rs.standard_normal(len(t)), 2000, 8000)) * np.exp(-t / 0.004)
def tap():  # pointer tip on a whiteboard
    t = tt(0.08); n = band(rs.standard_normal(len(t)), 1200, 7000) * np.exp(-t / 0.003)
    return 0.7 * norm(n) + 0.5 * np.sin(2 * np.pi * 820 * t) * np.exp(-t / 0.012)
def tick():
    t = tt(0.05); n = band(rs.standard_normal(len(t)), 2500, 9000) * np.exp(-t / 0.002)
    return norm(n) + 0.3 * np.sin(2 * np.pi * 3100 * t) * np.exp(-t / 0.006)
def marker(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 1400, 5200)
    squeak = np.sin(2 * np.pi * np.cumsum(2100 + 400 * np.sin(2 * np.pi * 5 * t)) / SR) * 0.25
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.4 * (0.75 + 0.25 * np.sin(2 * np.pi * 9 * t))
    return (norm(n) + squeak) * env
def mallet(f, d=1.6):
    t = tt(d); s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t / 0.05)
    return s * np.exp(-t / 0.45) * np.minimum(1, t / 0.004)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
# bed: HVAC air + faint fluorescent hum
t = np.arange(N) / SR
air = norm(band(rs.standard_normal(N), 60, 900)); air2 = norm(band(rs.standard_normal(N), 60, 900))
hum = np.sin(2 * np.pi * 120 * t) + 0.3 * np.sin(2 * np.pi * 240 * t)
L += air * 0.030 + hum * 0.004; R += air2 * 0.030 + hum * 0.004
ev = json.load(open('events.json'))
# distant keyboards: busy office until the question lands (3.55 s), then silence for the beat
kt = 0.35
while kt < 3.5:
    add(key(), kt, 0.05 * (0.6 + 0.8 * rs.random()), rs.uniform(-0.7, 0.7)); kt += rs.uniform(0.06, 0.22) + (0.35 if rs.random() < 0.12 else 0)
kt = 8.1
while kt < 9.4:   # Friday: one keyboard only
    add(key(), kt, 0.035, -0.5); kt += rs.uniform(0.12, 0.35)
for e in ev:
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'slide': add(slide(e['d']), te, 0.22 * v, 0.2)
    elif k == 'panel': add(printp(), te, 0.28)
    elif k == 'pop': add(pop(), te, 0.16)
    elif k == 'tap': add(tap(), te, 0.09, -0.3)
    elif k == 'tick': add(tick(), te, 0.07, -0.1)
    elif k == 'marker': add(marker(e['d']), te, 0.10, 0.3)
    elif k == 'chord':
        add(mallet(nt(69)), te, 0.10, -0.15); add(mallet(nt(64)), te + 0.22, 0.10, 0.15)
fi = int(0.25 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.9) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
