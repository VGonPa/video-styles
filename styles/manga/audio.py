# events.json → audio.wav (48 kHz stereo, 10 s)
# panel slams (paper thud), bubble pops, a rising tension drone, heartbeat lub-dubs, the starting gun (crack + boom + tail),
# a sprint whoosh, a page-turn rustle, the tape snap, a crowd roar swell, stopwatch beeps, a bright record sting, closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(43)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def thud(v=1.0):
    t = tt(0.4); f = 150 * np.exp(-t * 14) + 48; body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.08)
    slap = norm(band(rs.standard_normal(len(t)), 400, 6000)) * np.exp(-t / 0.018)
    return body + 0.45 * slap * v
def pop():
    t = tt(0.12); f = 500 + 900 * np.exp(-t * 60); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.03)
def beat():
    out = np.zeros(int(0.5 * SR))
    for off, g in [(0.0, 1.0), (0.17, 0.75)]:
        t = tt(0.25); f = 70 * np.exp(-t * 8) + 38; s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.07) * g
        i = int(off * SR); out[i:i + len(s)] += s
    return out
def drone(d):
    t = tt(d); u = t / d
    s = sum(a * np.sin(2 * np.pi * f * t + p) for f, a, p in [(55, 1, 0), (58.3, .7, 1), (110.5, .35, 2), (164.8, .2, 3)])
    hi = np.sin(2 * np.pi * (880 + 220 * u) * t) * (0.5 + 0.5 * np.sin(2 * np.pi * (6 + 10 * u) * t)) * 0.08
    return (s * 0.5 + hi) * u ** 1.6 * np.minimum(1, (d - t) / 0.03)
def bang():
    t = tt(2.2); crack = norm(band(rs.standard_normal(len(t)), 800, 12000)) * np.exp(-t / 0.012)
    boom = np.sin(2 * np.pi * np.cumsum(90 * np.exp(-t * 6) + 35) / SR) * np.exp(-t / 0.25)
    tail = norm(band(rs.standard_normal(len(t)), 200, 3000)) * np.exp(-t / 0.55) * 0.35
    return crack * 1.0 + boom * 0.9 + tail
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 300 + 3500 * np.sin(np.pi * np.clip(t / d * 1.3, 0, 1)) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.2
def rustle(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 700, 8000))
    am = np.abs(band(rs.standard_normal(len(t)), 4, 35)); am = am / (am.max() + 1e-9)
    return n * (0.3 + am) * np.sin(np.pi * t / d) ** 0.8
def snap():
    t = tt(0.9); crack = norm(band(rs.standard_normal(len(t)), 1500, 14000)) * np.exp(-t / 0.006)
    flutter = norm(band(rs.standard_normal(len(t)), 300, 2500)) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 22 * t))) * np.exp(-t / 0.25) * 0.3
    return crack + flutter + 0.5 * np.sin(2 * np.pi * 70 * t) * np.exp(-t / 0.06)
def crowd(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 250, 3200); n = norm(n)
    am = 0.7 + 0.3 * norm(np.abs(band(rs.standard_normal(len(t)), 1, 8)))
    env = np.minimum(1, t / 0.35) * np.clip(1 - (t - (d - 2.2)) / 2.2, 0, 1) ** 1.2
    return n * np.clip(am, 0, 1.4) * env
def beep():
    out = np.zeros(int(0.3 * SR))
    for off in (0.0, 0.14):
        t = tt(0.07); s = np.sign(np.sin(2 * np.pi * 2400 * t)) * 0.4 * np.minimum(1, (0.07 - t) / 0.005); i = int(off * SR); out[i:i + len(s)] += s
    return band(out, 200, 8000)
def tone(freq, d, att=0.02, rel=1.0, harm=((1, 1), (2, .4), (3, .2), (4, .1))):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in harm)
    return s * np.minimum(1, t / att) * np.minimum(1, (d - t) / rel)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR
room = norm(band(rs.standard_normal(N), 150, 2500)); L += room * .004; R += np.roll(room, 911) * .004
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'slam': add(thud(v), te, 0.5 * v, rs.uniform(-.25, .25))
    elif k == 'pop': add(pop(), te, 0.18)
    elif k == 'beat': add(beat(), te, 0.8)
    elif k == 'drone': add(drone(e['d']), te, 0.12)
    elif k == 'bang': add(bang(), te, 0.9)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.35, -.2)
    elif k == 'flip': add(rustle(e['d']), te, 0.22, .3)
    elif k == 'snap': add(snap(), te, 0.6)
    elif k == 'crowd': add(crowd(e['d']), te, 0.16); add(crowd(e['d']), te + 0.013, 0.1, .5)
    elif k == 'beep': add(beep(), te, 0.12, .2)
    elif k == 'sting':
        for i, m in enumerate([62, 66, 69, 74]): add(tone(nt(m), 1.3, 0.01, 0.9), te + i * 0.02, 0.05)
        add(tone(nt(38), 1.3, 0.01, 1.0), te, 0.08)
    elif k == 'chord':
        for i, m in enumerate([55, 59, 62, 66, 69]): add(tone(nt(m), 1.8, 0.2, 1.4, ((1, 1), (2, .2))), te + i * 0.05, 0.035)
fi = int(0.15 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
