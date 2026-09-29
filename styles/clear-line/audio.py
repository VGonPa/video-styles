# events.json → audio.wav (48 kHz stereo, 10 s)
# harbour bed (soft surf + distant gulls), a little two-stroke scooter putter that follows the chase,
# kite flutter, balloon pops, a pen scratching the route on the map, page-turn whooshes for the camera
# moves, a brake squeal, a dachshund yip, a bright catch chime, and a light pizzicato adventure tune
# that resolves on a closing chord as the page is revealed. All synthesized.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(59)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def pop():
    t = tt(0.12); f = 560 * np.exp(-t * 30) + 260; ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.03) + 0.3 * norm(band(rs.standard_normal(len(t)), 1500, 6000)) * np.exp(-t / 0.004)
def whoosh(d, f0=200, f1=1800):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = f0 + (f1 - f0) * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
def scratch(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 2200, 7000))
    return n * np.sin(np.pi * t / d) ** .4 * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 11 * t)))
def flutter(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 300, 2500))
    am = 0.5 + 0.5 * np.sin(2 * np.pi * (14 + 3 * np.sin(2 * np.pi * .7 * t)) * t)
    return n * am * np.minimum(1, t / .3) * np.minimum(1, (d - t) / .4)
def mallet(freq, d=0.9):
    t = tt(d); s = np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.3) + 0.25 * np.sin(2 * np.pi * freq * 3.99 * t) * np.exp(-t / 0.05)
    return s * np.minimum(1, t / 0.002)
def pluck(freq, d=0.6):
    n = int(d * SR); P = int(SR / freq); buf = rs.uniform(-1, 1, P); out = np.zeros(n)
    for i in range(n): out[i] = buf[i % P]; buf[i % P] = 0.5 * (buf[i % P] + buf[(i + 1) % P]) * 0.994
    return out * np.exp(-np.arange(n) / SR / 0.25)
def gull():
    t = tt(0.55); out = np.zeros(len(t))
    for j, (a, b) in enumerate([(0, .22), (.26, .5)]):
        m = (t >= a) & (t < b); u = (t[m] - a) / (b - a)
        f = 1900 - 700 * u + 300 * np.sin(np.pi * u); ph = 2 * np.pi * np.cumsum(f) / SR
        out[m] = (np.sin(ph) + .3 * np.sin(2 * ph)) * np.sin(np.pi * u) ** .6 * (1 - .3 * j)
    return out
def yip():
    t = tt(0.16); f = 900 + 500 * np.sin(np.pi * t / .16); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + .5 * np.sin(2 * ph) + .25 * np.sin(3 * ph)) * np.sin(np.pi * t / .16) ** .7
def squeal(d):
    t = tt(d); f = 2300 - 400 * t / d; ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * .4 + norm(band(rs.standard_normal(len(t)), 1500, 5000)) * .6) * np.sin(np.pi * t / d) ** .8
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR
# harbour bed: slow surf swells
surf = norm(band(rs.standard_normal(N), 150, 1400)); sw = 0.55 + 0.45 * np.sin(2 * np.pi * t / 3.1) ** 2
L += surf * sw * 0.020; R += np.roll(surf, 1777) * (0.55 + 0.45 * np.cos(2 * np.pi * t / 3.4) ** 2) * 0.020
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'engine':
        d = e['d']; tl = tt(d); tg = te + tl
        rpm = 38 + 6 * np.sin(2 * np.pi * tl / 2.7)
        rpm = np.where(tg > 7.0, 38 * np.clip(1 - (tg - 7.0) / 0.7, 0.35, 1), rpm)
        ph = 2 * np.pi * np.cumsum(rpm) / SR
        pulse = np.clip(np.sin(ph), 0, 1) ** 6
        body = band(pulse + 0.2 * rs.standard_normal(len(tl)) * pulse, 60, 1800)
        env = np.minimum(1, tl / .4) * np.clip((te + d - tg) / .5, 0, 1)
        env = env * np.where((tg > 3.2) & (tg < 5.6), 0.45, 1.0)          # quieter under the map
        add(norm(body) * env, te, 0.10, -0.05)
    elif k == 'flutter': add(flutter(e['d']), te, 0.035, 0.3)
    elif k == 'pop': add(pop(), te, 0.26 * v, rs.uniform(-.2, .2))
    elif k == 'bark': add(yip(), te, 0.18, 0.25); add(yip(), te + .2, 0.14, 0.25)
    elif k == 'gull': add(gull(), te, 0.05, rs.uniform(-.6, .6))
    elif k == 'whoosh': add(whoosh(e['d'], 180, 1600), te, 0.13)
    elif k == 'pen':
        d = e['d']
        for i in range(10): add(scratch(d / 10 * .7), te + d * i / 10, 0.05, -0.3 + .06 * i)
    elif k == 'brake': add(squeal(e['d']), te + .1, 0.05, 0.1)
    elif k == 'catch':
        for i, m in enumerate([84, 88, 91]): add(mallet(nt(m), .8), te + i * .05, 0.07, .2)
    elif k == 'chord':
        for i, m in enumerate([60, 64, 67, 72, 76]): add(mallet(nt(m + 12), 1.0), te + i * 0.07, 0.05, -0.3 + i * 0.15)
        add(pluck(nt(36), 1.0), te, 0.16); add(pluck(nt(48), 1.0), te, 0.10)
# pizzicato adventure tune (F major, 138 bpm, eighths); thins out under the map, resolves at 9.0
B = 60 / 138 / 2
mel = [72, None, 74, 76, None, 77, 76, 74, 72, None, 69, 72, None, 74, 72, None,
       77, None, 76, 74, None, 76, 77, 79, 81, None, 79, 77, 76, None, 74, None]
bass = [41, 48, 45, 48, 43, 50, 46, 50]
for i in range(int(8.9 / B)):
    tb = 0.35 + i * B
    if tb > 8.9: break
    g = 0.45 if 3.3 < tb < 5.5 else 1.0
    m = mel[i % len(mel)]
    if m and i % 1 == 0: add(pluck(nt(m), .35), tb, 0.07 * g, 0.25)
    if i % 2 == 0: add(pluck(nt(bass[(i // 4) % len(bass)]), .5), tb, 0.14 * g, -0.2)
fi = int(0.2 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 3.0) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
