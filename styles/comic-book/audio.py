# events.json → audio.wav · comic: panel 'clicks', robot motor + beeps, whoosh, POW thump, happy boops, sparkles, bell
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); out = np.zeros(N)
rs = np.random.default_rng(16)
def add(sig, t, g=1.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0: out[i:i + n] += sig[:n] * g
def tt(d): return np.arange(int(d * SR)) / SR
def sweep(f0, f1, d, dec, vib=0):
    x = tt(d); f = f0 * (f1 / f0) ** (x / d) * (1 + vib * np.sin(2 * np.pi * 14 * x) * np.exp(-x * 4))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / dec) * np.minimum(1, x / 0.003)
def wood(f):
    x = tt(0.12); return (np.sin(2 * np.pi * f * x) + 0.5 * np.sin(2 * np.pi * f * 2.7 * x)) * np.exp(-x / 0.025)
def bell(f):
    x = tt(1.6); return sum(a * np.sin(2 * np.pi * f * m * x) * np.exp(-x * (1.5 + m)) for m, a in [(1, 1), (2.76, 0.5), (5.4, 0.25)])
def lp(sig, a):  # one-pole low-pass
    y = np.zeros_like(sig); acc = 0.0
    for i, v in enumerate(sig): acc += a * (v - acc); y[i] = acc
    return y
def motor(d, f0, f1):  # buzzy sawtooth motor, rising pitch
    x = tt(d); f = np.linspace(f0, f1, len(x)); ph = np.cumsum(f) / SR
    saw = 2 * (ph % 1) - 1; env = np.minimum(1, x / 0.05) * np.minimum(1, (d - x) / 0.12)
    return lp(saw, 0.25) * env * (1 + 0.3 * np.sin(2 * np.pi * 31 * x))
def square(f, d):
    x = tt(d); return np.sign(np.sin(2 * np.pi * f * x)) * np.minimum(1, (d - x) / 0.01) * 0.5
def noise(d): return rs.standard_normal(int(d * SR))
def whoosh(d):
    x = tt(d); env = np.sin(np.pi * x / d) ** 2
    a = np.linspace(0.02, 0.25, len(x)) ** 1.0
    y = np.zeros(len(x)); acc = 0.0; n = noise(d)
    for i in range(len(x)): acc += a[i] * (n[i] - acc); y[i] = acc
    return y * env * 2.5
for e in json.load(open('events.json')):
    k, t = e['k'], e['t']
    if k == 'paper': add(wood(1400) * 0.4, t, 0.25)
    elif k == 'vroom': add(motor(0.65, 90, 170), t, 0.22)
    elif k == 'vroom2': add(motor(0.45, 110, 210), t, 0.22)
    elif k == 'bonk': add(sweep(420, 180, 0.18, 0.06), t, 0.45); add(wood(700), t, 0.35)
    elif k == 'beep':
        for j, f in enumerate([1200, 1500, 1200]): add(square(f, 0.07), t + j * 0.1, 0.12)
        add(lp(noise(0.12), 0.6) * np.exp(-tt(0.12) / 0.05), t + 0.32, 0.25)
    elif k == 'whoosh': add(whoosh(0.7), t, 0.5)
    elif k == 'boing': add(sweep(180, 520, 0.35, 0.18, vib=0.25), t, 0.3)
    elif k == 'pow':
        add(sweep(160, 45, 0.35, 0.12), t, 0.9); add(lp(noise(0.25), 0.3) * np.exp(-tt(0.25) / 0.06), t, 0.6); add(wood(2200), t, 0.3)
    elif k == 'boop':
        add(sweep(600, 900, 0.1, 0.08), t, 0.14); add(sweep(900, 1350, 0.12, 0.1), t + 0.13, 0.14)
    elif k == 'sweep':
        for j in range(5): add(whoosh(0.18) * 0.5, t + j * 0.18, 0.25)
    elif k == 'sparkle':
        for j, f in enumerate([2640, 3520, 3960]): add(bell(f) * 0.6, t + j * 0.05, 0.05)
    elif k == 'ding': add(bell(1320), t, 0.18); add(bell(1760), t + 0.12, 0.12)
    elif k == 'beepq': add(square(900, 0.08), t, 0.1); add(sweep(900, 1500, 0.16, 0.2) * 0.5, t + 0.12, 0.16)
out = np.tanh(out * 1.3) * 0.85
pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes()); w.close()
print('audio.wav ok')
