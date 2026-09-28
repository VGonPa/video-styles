# events.json -> audio.wav (48 kHz stereo, 10 s)
# wind + surf bed, cold drone, lamp ignition, beam swells each revolution, ship foghorn,
# lightning crack + thunder roll, rain, a 1-bit square-wave title motif, lantern blinks, closing fade.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(53)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def norm(x): return x / (np.abs(x).max() + 1e-9)
def tt(d): return np.arange(int(d * SR)) / SR
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR
# --- bed: wind (slowly moving band noise) + surf swells synced to the wave period + low drone
wind = norm(band(rs.standard_normal(N), 250, 1400)) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.13 * t + 1))
surfA = norm(band(rs.standard_normal(N), 60, 700)); surfB = norm(band(rs.standard_normal(N), 60, 700))
swell = np.clip(np.sin(2 * np.pi * t / 2.9), 0, 1) ** 2; swell2 = np.clip(np.sin(2 * np.pi * t / 2.9 + 2.2), 0, 1) ** 2
bed_env = np.clip(t / 1.2, 0, 1)
L += (wind * 0.035 + surfA * swell * 0.09 + surfB * swell2 * 0.04) * bed_env
R += (np.roll(wind, 911) * 0.035 + surfA * swell * 0.05 + surfB * swell2 * 0.08) * bed_env
drone = sum(a * np.sin(2 * np.pi * nt(m) * t + p) for m, a, p in [(38, 1, 0), (45, .5, 1), (50, .25, 2)])
drone *= np.clip((t - 0.3) / 2.0, 0, 1) * (1 + 0.2 * np.sin(2 * np.pi * 0.2 * t))
L += drone * 0.03; R += drone * 0.03
def ignite():
    d = tt(0.6); click = norm(band(rs.standard_normal(len(d)), 1500, 8000)) * np.exp(-d / 0.004)
    buzz = np.sign(np.sin(2 * np.pi * 120 * d)) * 0.3 * np.exp(-d / 0.25) * (d > 0.05)
    whoomp = np.sin(2 * np.pi * (70 + 60 * np.exp(-d * 8)) * d) * np.exp(-d / 0.2)
    return click * 0.6 + band(buzz, 100, 2500) + whoomp * 0.7
def sweep(v):
    d = tt(1.6); env = np.sin(np.pi * d / 1.6) ** 2
    s = norm(band(rs.standard_normal(len(d)), 120, 900)) * 0.6 + np.sin(2 * np.pi * 55 * d) * 0.7 + np.sin(2 * np.pi * 82.5 * d) * 0.3
    return s * env * v
def horn(d=1.5):
    x = tt(d); f = 98 * (1 + 0.004 * np.sin(2 * np.pi * 5 * x))
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = sum(np.sin(k * ph) / k for k in range(1, 14)) + 0.5 * sum(np.sin(k * ph * 1.5) / k for k in range(1, 8))
    env = np.minimum(1, x / 0.18) * np.minimum(1, (d - x) / 0.5)
    return band(saw * env, 40, 900)
def crack():
    d = tt(0.5); n = norm(band(rs.standard_normal(len(d)), 900, 12000)) * np.exp(-d / 0.05)
    n2 = norm(band(rs.standard_normal(len(d)), 200, 4000)) * np.exp(-d / 0.12) * (rs.random(len(d)) > 0.6)
    return n + 0.5 * n2
def thunder():
    d = tt(3.4); n = norm(band(rs.standard_normal(len(d)), 25, 260))
    am = norm(np.abs(band(rs.standard_normal(len(d)), 1, 9))) * 0.7 + 0.3
    return n * am * np.minimum(1, d / 0.08) * np.exp(-d / 1.1)
def square(f, d, duty=0.5):
    x = tt(d); s = np.where((x * f) % 1 < duty, 1.0, -1.0); env = np.minimum(1, x / 0.005) * np.exp(-x / (d * 0.45)); return s * env
def ping(f):
    d = tt(0.35); return np.sin(2 * np.pi * f * d) * np.exp(-d / 0.08) + 0.3 * np.sin(2 * np.pi * f * 2.01 * d) * np.exp(-d / 0.04)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'ignite': add(ignite(), te, 0.3, 0.5)
    elif k == 'sweep': add(sweep(v), te - 0.8, 0.12, 0.3)
    elif k == 'horn': add(horn(), te, 0.16 * v, -0.4)
    elif k == 'strike': add(crack(), te, 0.5, -0.1)
    elif k == 'thunder': add(thunder(), te, 0.55); add(thunder(), te + 0.25, 0.3, 0.3)
    elif k == 'rain':
        n = N - int(te * SR); x = np.arange(n) / SR
        r = norm(band(rs.standard_normal(n), 2500, 11000)) * np.minimum(1, x / 0.6)
        L[-n:] += r * 0.03; R[-n:] += np.roll(r, 333) * 0.03
    elif k == 'title':  # 1-bit motif: square-wave arpeggio in D minor, a low octave underneath
        for i, m in enumerate([62, 65, 69, 74, 72]):
            add(band(square(nt(m), 0.9, 0.25), 80, 5000), te + i * 0.19, 0.022, (-0.3 + 0.15 * i))
        add(band(square(nt(38), 2.4, 0.5), 40, 1200), te, 0.02)
    elif k == 'blink': add(ping(1318), te, 0.05, -0.5)
    elif k == 'fade':
        d = tt(1.6); f = nt(62) * np.exp(-d * 0.35); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-d / 0.7)
        add(s, te, 0.05, 0.4)
# master: fade in/out, soft limiter
fi = int(0.4 * SR); fo = int(1.0 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
