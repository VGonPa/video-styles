# events.json → audio.wav (48 kHz stereo, 10 s), all synthesized
# night-street bed (light rain hiss, drips, distant rumble), 120 Hz transformer buzz that follows how much glass is lit,
# electrode strike zaps, a fizzing hiss while the script draws on, relay ticks for the chasing arrow,
# arcing crackles for the faulty letter, a relay clunk + dying whine at the power cut.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(83)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def norm(x): return x / (np.abs(x).max() + 1e-9)
def tt(d): return np.arange(int(d * SR)) / SR
def buzz(t, f0=120.0, nh=14):
    ph = 2 * np.pi * f0 * t + 0.02 * np.sin(2 * np.pi * 0.7 * t)
    return sum((1 / k) * np.sin(k * ph + k * 0.3) for k in range(1, nh + 1))
def strike():
    t = tt(0.22); click = norm(band(rs.standard_normal(len(t)), 2500, 12000)) * np.exp(-t / 0.003)
    z = buzz(t) * np.exp(-t / 0.06) * (0.6 + 0.4 * (rs.random(len(t)) > 0.3))
    ping = np.sin(2 * np.pi * 2900 * t) * np.exp(-t / 0.03) * 0.25
    return 0.7 * click + 0.35 * norm(z) + ping
def tick():
    t = tt(0.05); c = norm(band(rs.standard_normal(len(t)), 1200, 6000)) * np.exp(-t / 0.004)
    return c + 0.4 * np.sin(2 * np.pi * 900 * t) * np.exp(-t / 0.008)
def crackle(d):
    t = tt(d); s = np.zeros(len(t))
    for _ in range(int(d * 70)):
        i = rs.integers(0, len(t) - 400); n = rs.integers(80, 400)
        s[i:i + n] += norm(rs.standard_normal(n)) * np.exp(-np.arange(n) / (n / 4)) * rs.uniform(.3, 1)
    s = band(s, 800, 14000); s += 0.5 * norm(buzz(t, 120, 20)) * (rs.random(len(t)) > 0.5)
    return norm(s)
def fizz(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 3000, 11000)
    am = np.abs(band(rs.standard_normal(len(t)), 8, 60)); am = norm(am)
    s = norm(n) * (0.4 + 0.6 * am) * np.minimum(1, t / 0.08) * np.minimum(1, (d - t) / 0.15)
    return s + 0.25 * norm(buzz(t, 120, 8)) * np.minimum(1, t / 0.2)
def clunk():
    t = tt(0.5); f = 90 * np.exp(-t * 6) + 40; th = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.08)
    c = norm(band(rs.standard_normal(len(t)), 400, 5000)) * np.exp(-t / 0.01)
    return th + 0.6 * c
def whine(d):
    t = tt(d); f = 240 * np.exp(-t * 3.5) + 30
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (d / 3)) + 0.3 * np.sin(2 * np.pi * np.cumsum(f * 2) / SR) * np.exp(-t / (d / 4))
def drip():
    t = tt(0.08); f = 1400 + 900 * np.exp(-t * 60)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.015)

data = json.load(open('events.json'))
t = np.arange(N) / SR
# bed: rain hiss, distant rumble, occasional drips
rain = norm(band(rs.standard_normal(N), 1500, 9000)); rain2 = norm(band(rs.standard_normal(N), 1500, 9000))
L += rain * 0.018; R += rain2 * 0.018
rum = norm(band(rs.standard_normal(N), 30, 140)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.13 * t)); L += rum * 0.03; R += rum * 0.03
for k in range(16): add(drip(), rs.uniform(0.2, 9.4), rs.uniform(.02, .05), rs.uniform(-.8, .8))
# transformer buzz following the lit amount
hum = np.array(data['hum']); env = np.interp(t, np.arange(len(hum)) / 30, hum)
env = np.convolve(env, np.ones(480) / 480, mode='same')                       # 10 ms smoothing
hb = norm(band(buzz(t, 120, 24), 60, 6000)) * np.sqrt(np.clip(env, 0, None))
L += hb * 0.045; R += hb * 0.04
for e in data['ev']:
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'strike': add(strike(), te, 0.22 * v, rs.uniform(-.3, .3))
    elif k == 'tick': add(tick(), te, 0.07 * v, 0.45)
    elif k == 'pen': add(fizz(e['d']), te, 0.08, -.2)
    elif k == 'crackle': add(crackle(e['d']), te, 0.16, -.15)
    elif k == 'cut': add(clunk(), te, 0.6); add(whine(0.8), te + 0.02, 0.05)
# master: fade in/out, soft limiter
fi = int(0.4 * SR); fo = int(1.0 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
