# events.json → audio.wav (48 kHz stereo, 10 s)
# A low electrical hum under the dark city, swooshes for captions and camera moves, a visor power-up
# chirp, a balloon pop, hologram beeps, a rising electric charge with crackling zaps, the panel border
# cracking, a dive whoosh into a huge sub-bass impact with debris rattle, surge zaps racing outward,
# a rising power-up chord as the city lights, a servo whirr as the hero stands, a flare swell, the logo
# slam, a chrome shimmer and a bright resolving chord. All synthesized.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(61)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def env(x, a, d): return np.minimum(1, x / max(a, 1e-4)) * np.exp(-x / d)
t = np.arange(N) / SR

def drone():
    x = t; e = np.clip(x / 0.6, 0, 1) * (1 - np.clip((x - 4.2) / 0.4, 0, 1)) * 0.9 + 0.1
    s = sum(np.sin(2 * np.pi * f * x) * g for f, g in [(50, 1), (100, .45), (150, .2), (61.7, .35)])
    return s * e * (0.8 + 0.2 * np.sin(2 * np.pi * 0.3 * x))
def swoosh(d=0.35):
    x = tt(d); n = rs.standard_normal(len(x)); w = np.sin(np.pi * x / d) ** 2
    return norm(band(n, 600, 5000)) * w
def whoosh(d):
    x = tt(d); n = norm(band(rs.standard_normal(len(x)), 150, 3000)); return n * np.sin(np.pi * x / d) ** 3
def visor():
    x = tt(0.45); f = 400 + 2600 * (x / 0.45) ** 1.5; ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * 0.6 + np.sign(np.sin(ph * 0.5)) * 0.1) * env(x, 0.01, 0.2)
def pop():
    x = tt(0.12); return np.sin(2 * np.pi * (300 + 900 * np.exp(-x * 40)) * x) * env(x, 0.002, 0.03)
def beep(v):
    x = tt(0.18); return (np.sin(2 * np.pi * 1320 * x) + 0.3 * np.sin(2 * np.pi * 2640 * x)) * env(x, 0.004, 0.06) * v
def charge(d):
    x = tt(d); f = 60 + 240 * (x / d) ** 2; ph = 2 * np.pi * np.cumsum(f) / SR
    buzz = np.sign(np.sin(ph)) * 0.3 + np.sin(ph * 2) * 0.3; hiss = norm(band(rs.standard_normal(len(x)), 2000, 12000)) * 0.4
    return (buzz + hiss * (x / d)) * (x / d) ** 1.2
def zap(v):
    x = tt(0.14); n = norm(band(rs.standard_normal(len(x)), 1500, 14000)); am = (np.sin(2 * np.pi * 120 * x) > 0).astype(float)
    return (n * (0.5 + 0.5 * am) + np.sign(np.sin(2 * np.pi * 180 * x)) * 0.3) * env(x, 0.001, 0.04) * v
def crack():
    x = tt(0.6); c = norm(band(rs.standard_normal(len(x)), 1500, 14000)) * env(x, 0.001, 0.05)
    tink = np.zeros(len(x))
    for i in range(20):
        j = int(rs.uniform(0.01, 0.45) * SR); k = tt(0.08); s = np.sin(2 * np.pi * rs.uniform(3000, 7000) * k) * np.exp(-k / 0.02)
        tink[j:j + len(k)] += s[:len(tink) - j] * rs.uniform(.2, .6)
    return c + tink
def boom():
    x = tt(3.0); sub = np.sin(2 * np.pi * (35 + 90 * np.exp(-x * 6)) * x) * env(x, 0.003, 0.9)
    crack_ = norm(band(rs.standard_normal(len(x)), 500, 10000)) * env(x, 0.001, 0.08)
    rum = norm(band(rs.standard_normal(len(x)), 20, 300)) * env(x, 0.01, 0.8)
    return sub * 1.2 + crack_ * 0.8 + rum * 0.7
def debris():
    x = tt(0.1); return norm(band(rs.standard_normal(len(x)), 300, 4000)) * env(x, 0.001, 0.02)
def powerup(d):
    x = tt(d); e = np.clip(x / (d * 0.8), 0, 1) ** 1.5 * np.minimum(1, (d - x) / 0.3)
    s = 0
    for f in (110, 164.8, 220, 277.2, 329.6):
        fr = f * (1 + 0.5 * x / d); ph = 2 * np.pi * np.cumsum(fr) / SR; s = s + (np.sin(ph) + 0.3 * np.sin(2 * ph)) / 5
    return s * e
def beam():
    x = tt(1.4); f = 880 + 440 * np.minimum(1, x / 0.3); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + 0.4 * np.sin(1.5 * ph)) * env(x, 0.05, 0.5)
def servo(d):
    x = tt(d); f = 220 + 160 * np.sin(np.pi * x / d); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sign(np.sin(ph)) * 0.25 + np.sin(2 * ph) * 0.3) * np.sin(np.pi * x / d) ** 2
def slam():
    x = tt(2.0); return np.sin(2 * np.pi * (45 + 120 * np.exp(-x * 10)) * x) * env(x, 0.002, 0.5) + norm(band(rs.standard_normal(len(x)), 2000, 12000)) * env(x, 0.001, 0.15) * 0.6
def shimmer():
    x = tt(1.2); s = sum(np.sin(2 * np.pi * f * x + i) * np.exp(-x / (0.25 + 0.1 * i)) * np.minimum(1, np.maximum(0, x - i * 0.05) / 0.01) for i, f in enumerate([2093, 2637, 3136, 4186, 5274]))
    return s / 3
def tick():
    x = tt(0.04); return norm(band(rs.standard_normal(len(x)), 3000, 9000)) * env(x, 0.0005, 0.006)
def chord():
    x = tt(2.8); s = 0
    for f, g in [(130.8, 1), (196, .7), (261.6, .6), (329.6, .5), (392, .35), (523.3, .25)]:
        s = s + np.sin(2 * np.pi * f * x) * g + np.sin(2 * np.pi * f * 1.004 * x) * g * 0.5
    return s / 4 * np.minimum(1, x / 0.02) * np.exp(-x / 1.3)

for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'drone': add(drone(), 0, 0.10)
    elif k == 'swoosh': add(swoosh(), te - 0.1, 0.10 * e['v'], -0.3)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.16, 0.2)
    elif k == 'visor': add(visor(), te, 0.10, -0.3)
    elif k == 'pop': add(pop(), te, 0.20, 0.2)
    elif k == 'beep': add(beep(e['v']), te, 0.06, 0.4)
    elif k == 'charge': add(charge(e['d']), te, 0.10)
    elif k == 'zap': add(zap(e['v']), te, 0.16, rs.uniform(-.5, .5))
    elif k == 'crack': add(crack(), te, 0.30, 0.2)
    elif k == 'dive': add(whoosh(0.3), te, 0.25)
    elif k == 'boom': add(boom(), te, 0.60)
    elif k == 'debris': add(debris(), te, 0.12, rs.uniform(-.7, .7))
    elif k == 'powerup': add(powerup(e['d']), te, 0.16)
    elif k == 'beam': add(beam(), te, 0.05, 0.1)
    elif k == 'servo': add(servo(e['d']), te, 0.04)
    elif k == 'flarewipe': add(whoosh(e['d'] + 0.2), te - 0.1, 0.22)
    elif k == 'slam': add(slam(), te - 0.28, 0.40)
    elif k == 'shimmer': add(shimmer(), te, 0.06, 0.3)
    elif k == 'tick': add(tick(), te, 0.05, rs.uniform(-.3, .3))
    elif k == 'chord': add(chord(), te - 0.25, 0.22)
fi = int(0.2 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.0) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
