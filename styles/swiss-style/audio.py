# events.json → audio.wav (48 kHz stereo, 10 s)
# grid ticks, a mechanical counter clatter, a whoosh as the numeral shrinks, vibraphone pings as the rings
# close, slug-snap clicks as type lands on the baseline, then a dry 120 bpm pulse playing a tone row
# (kick, hat, vibraphone) that resolves into a soft chord and fades with the picture.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(1959)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def wood(f):
    t = tt(0.09); return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.012) + 0.3 * norm(band(rs.standard_normal(len(t)), 2000, 8000)) * np.exp(-t / 0.002)
def tick():
    t = tt(0.03); return norm(band(rs.standard_normal(len(t)), 2500, 9000)) * np.exp(-t / 0.003) + 0.4 * np.sin(2 * np.pi * 1800 * t) * np.exp(-t / 0.004)
def clunk():
    t = tt(0.2); f = 150 * np.exp(-t * 20) + 70
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.04) + 0.6 * np.pad(tick(), (0, len(t) - len(tick())))
def snap():
    t = tt(0.05); n = norm(band(rs.standard_normal(len(t)), 1200, 10000)) * np.exp(-t / 0.0035)
    return n + 0.5 * np.sin(2 * np.pi * 420 * t) * np.exp(-t / 0.008)
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 300 + 3000 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
def swipe(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 600, 4000)); return n * np.sin(np.pi * t / d) ** 2
def kick():
    t = tt(0.35); f = 120 * np.exp(-t * 28) + 48
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.09)
def hat():
    t = tt(0.06); return norm(band(rs.standard_normal(len(t)), 6000, 14000)) * np.exp(-t / 0.012)
def vib(f, d=1.6):
    t = tt(d); trem = 1 + 0.25 * np.sin(2 * np.pi * 5.5 * t)
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / 0.05)
    return s * np.exp(-t / 0.55) * trem * np.minimum(1, t / 0.002)
def pizz(f):
    t = tt(0.6); return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(4 * np.pi * f * t)) * np.exp(-t / 0.16) * np.minimum(1, t / 0.004)
room = band(rs.standard_normal(N), 150, 2500); room = norm(room)
L += room * .004; R += np.roll(room, 911) * .004
ROW = [64, 67, 63, 70, 66, 61, 68, 71, 65, 62, 69, 72]   # a twelve-tone row for the pulse
PING = [72, 74, 77, 79, 81, 84, 86]
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'swipe': add(swipe(e['d']), te, 0.05 * v, -0.3)
    elif k == 'col': add(wood(900 + 500 * v), te, 0.10, -0.7 + 1.4 * v)
    elif k == 'tick': add(tick(), te, 0.07 * v, rs.uniform(-.3, .3))
    elif k == 'clunk': add(clunk(), te, 0.28 * v)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.16)
    elif k == 'thump': add(kick(), te, 0.45); add(vib(nt(60), 2.0), te, 0.10)
    elif k == 'ping': add(vib(nt(PING[e['n']]), 1.4), te, 0.07, -0.4 + 0.12 * e['n'])
    elif k == 'snap': add(snap(), te, 0.20 * v, rs.uniform(-.25, .25))
    elif k == 'beat':
        n = e['n']; add(kick(), te, 0.42 if e['acc'] else 0.28); add(hat(), te + 0.25, 0.05, 0.3)
        add(vib(nt(ROW[n % 12]), 1.2), te, 0.10, -0.25 + 0.5 * (n % 2)); add(pizz(nt(ROW[n % 12] - 24)), te, 0.12)
    elif k == 'chord':
        for i, m in enumerate([60, 64, 67, 71, 74]): add(vib(nt(m), 2.2), te + i * 0.025, 0.07, -0.3 + 0.15 * i)
        add(pizz(nt(36)), te, 0.2); add(kick(), te, 0.3)
fi = int(0.05 * SR); fo = int(0.75 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
