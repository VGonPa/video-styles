# events.json → audio.wav (48 kHz stereo, 10 s)
# typewriter keys, push-pin taps, paper slaps/rustle, felt-tip marker squeaks, dashed-pen scratches,
# red-string twangs, zoom whooshes, projector hum + soft pad bed, closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(11)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def key():
    t = tt(0.06); n = band(rs.standard_normal(len(t)), 1800, 7000) * np.exp(-t / 0.004)
    body = np.sin(2 * np.pi * (160 + 40 * rs.random()) * t) * np.exp(-t / 0.012)
    return 0.55 * n / (np.abs(n).max() + 1e-9) + 0.5 * body
def pin():
    t = tt(0.25); f = 240 * np.exp(-t * 18) + 110; ph = 2 * np.pi * np.cumsum(f) / SR
    thump = np.sin(ph) * np.exp(-t / 0.035)
    click = band(rs.standard_normal(len(t)), 2500, 9000) * np.exp(-t / 0.0025)
    return thump + 0.5 * click / (np.abs(click).max() + 1e-9)
def slap():
    t = tt(0.35); n = band(rs.standard_normal(len(t)), 300, 5000) * np.exp(-t / 0.035)
    return 0.8 * n / (np.abs(n).max() + 1e-9) + 0.6 * np.sin(2 * np.pi * 85 * t) * np.exp(-t / 0.05)
def rustle(d=0.45):
    t = tt(d); n = band(rs.standard_normal(len(t)), 900, 7000)
    am = np.abs(band(rs.standard_normal(len(t)), 5, 40)); am /= am.max() + 1e-9
    return n / (np.abs(n).max() + 1e-9) * am * np.sin(np.pi * t / d) ** 0.7
def marker(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 1500, 5000)
    squeak = np.sin(2 * np.pi * np.cumsum(2400 + 500 * np.sin(2 * np.pi * 7 * t)) / SR) * 0.15
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.5 * (0.7 + 0.3 * np.sin(2 * np.pi * 11 * t))
    s = (n / (np.abs(n).max() + 1e-9) + squeak) * env; return s
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 200 + 2600 * np.sin(np.pi * t / d) ** 2
    a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y / (np.abs(y).max() + 1e-9) * np.sin(np.pi * t / d) ** 1.5
def twang(f):
    n = int(0.7 * SR); P = int(SR / f); buf = rs.uniform(-1, 1, P); out = np.zeros(n)
    for i in range(n): out[i] = buf[i % P]; buf[i % P] = 0.5 * (buf[i % P] + buf[(i + 1) % P]) * 0.994
    return out * np.exp(-np.arange(n) / SR / 0.25)
def tone(freq, d, att=0.4, rel=1.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in [(1, 1), (2, .3), (3, .12)])
    env = np.minimum(1, t / att) * np.minimum(1, (d - t) / rel); return s * env
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
# bed: projector hum + soft pad (A minor), swelling into the end
t = np.arange(N) / SR
hum = (np.sin(2 * np.pi * 50 * t) + .4 * np.sin(2 * np.pi * 100 * t) + .15 * np.sin(2 * np.pi * 150 * t)) * (1 + .3 * np.sin(2 * np.pi * 24 * t))
bedenv = np.clip(t / 0.8, 0, 1)
L += hum * 0.012 * bedenv; R += hum * 0.012 * bedenv
room = band(rs.standard_normal(N), 200, 3000); room /= np.abs(room).max(); L += room * .006; R += np.roll(room, 777) * .006
for m, g, p in [(45, .05, -.3), (52, .035, .3), (57, .025, 0)]:
    s = tone(nt(m), 9.6, 1.5, 1.2) * (1 + .15 * np.sin(2 * np.pi * .25 * np.arange(int(9.6 * SR)) / SR)); add(s, 0.3, g, p)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'key': add(key(), te + rs.uniform(0, .008), 0.16 * (0.8 + .4 * rs.random()), rs.uniform(-.2, .2))
    elif k == 'pin': add(pin(), te, 0.5 * v)
    elif k == 'slap': add(slap(), te, 0.4 * v); add(rustle(0.3), te + 0.02, 0.06)
    elif k == 'rustle': add(rustle(0.5), te, 0.12, .4)
    elif k == 'marker': add(marker(e['d']), te, 0.05)
    elif k == 'pen':
        d = e['d']; nd = 14
        for i in range(nd): add(marker(d / nd * 0.6), te + d * (1 - (1 - i / nd) ** 1.0) , 0.035)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.22)
    elif k == 'twang': add(twang(e['f']), te, 0.18, rs.uniform(-.3, .3))
    elif k == 'burn': add(whoosh(1.2), 0.0, 0.12)
    elif k == 'chord':
        for i, m in enumerate([57, 60, 64, 69, 72]): add(tone(nt(m), 2.0, 0.08 + i * .03, 1.2), te + i * 0.04, 0.03)
        add(tone(nt(33), 2.0, .1, 1.3), te, 0.06)
# master: fade in/out, soft limiter
fi = int(0.25 * SR); fo = int(0.8 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
