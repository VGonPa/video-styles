# events.json → audio.wav (48 kHz stereo, 10 s)
# brush-on-paper swishes and leaf flicks, wet washes spreading, a water drop + bloom swell,
# wooden seal presses, soft heron wingbeats, the brush lifting away, sparse plucked-string notes,
# over a quiet room/air bed and a low drone that settles at the end.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(44)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def swish(d):
    d = max(d, .06) + .08; t = tt(d); n = norm(band(rs.standard_normal(len(t)), 700, 6000))
    grain = np.abs(band(rs.standard_normal(len(t)), 20, 180)); grain = 0.55 + 0.45 * norm(grain)
    env = np.minimum(1, t / 0.025) * np.clip((d - t) / (d * 0.55), 0, 1) ** 1.3
    drag = norm(band(rs.standard_normal(len(t)), 150, 600)) * 0.35
    return (n * grain + drag) * env
def flick(d):
    d = max(d, .08) + .05; t = tt(d); n = norm(band(rs.standard_normal(len(t)), 1500, 8000))
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2 * np.exp(-t / (d * 0.6))
    return n * env
def wet(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 180, 1400))
    am = np.abs(band(rs.standard_normal(len(t)), 2, 14)); am = norm(am)
    return n * am * np.sin(np.pi * t / d) ** 0.8
def drop():
    t = tt(0.5); f = 650 + 1300 * (1 - np.exp(-t / 0.018)); ph = 2 * np.pi * np.cumsum(f) / SR
    plip = np.sin(ph) * np.exp(-t / 0.045)
    thump = np.sin(2 * np.pi * 90 * t) * np.exp(-t / 0.05)
    tick = norm(band(rs.standard_normal(len(t)), 2000, 9000)) * np.exp(-t / 0.003)
    return 0.8 * plip + 0.5 * thump + 0.25 * tick
def swell(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 90, 700))
    return n * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
def seal():
    t = tt(0.35); body = np.sin(2 * np.pi * 170 * t) * np.exp(-t / 0.03) + 0.5 * np.sin(2 * np.pi * 310 * t) * np.exp(-t / 0.018)
    click = norm(band(rs.standard_normal(len(t)), 400, 3000)) * np.exp(-t / 0.006)
    return body + 0.5 * click
def wing():
    d = 0.42; t = tt(d); n = norm(band(rs.standard_normal(len(t)), 120, 900))
    return n * np.sin(np.pi * t / d) ** 2.5
def air(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 300 + 1800 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
def pluck(f, d=2.4):
    n = int(d * SR); P = int(SR / f); buf = rs.uniform(-1, 1, P) * np.hanning(P); out = np.zeros(n)
    for i in range(n): out[i] = buf[i % P]; buf[i % P] = 0.5 * (buf[i % P] + buf[(i + 1) % P]) * 0.9965
    t = np.arange(n) / SR
    return norm(out) * np.exp(-t / 0.9) * np.minimum(1, t / 0.002)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def tone(freq, d, att=0.4, rel=1.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in [(1, 1), (2, .25), (3, .08)])
    return s * np.minimum(1, t / att) * np.minimum(1, (d - t) / rel)
# bed: quiet room air + low drone (D, A)
t = np.arange(N) / SR
room = norm(band(rs.standard_normal(N), 120, 2500)); L += room * .007; R += np.roll(room, 911) * .007
for m, g, p in [(38, .05, -.2), (45, .035, .25), (50, .018, 0)]:
    s = tone(nt(m), 9.7, 1.8, 1.4) * (1 + .12 * np.sin(2 * np.pi * .21 * tt(9.7))); add(s, 0.15, g, p)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'swish': add(swish(e['d']), te, 0.16 * v, rs.uniform(-.25, .1))
    elif k == 'flick': add(flick(e['d']), te, 0.1 * v, rs.uniform(-.2, .2))
    elif k == 'wet': add(wet(e['d']), te, 0.07, rs.uniform(-.3, .3))
    elif k == 'drop': add(drop(), te, 0.5, 0.05); add(swell(1.4), te, 0.12)
    elif k == 'seal': add(seal(), te + .03, 0.42, .35)
    elif k == 'wing': add(wing(), te, 0.13, e.get('pan', 0) * .7)
    elif k == 'air': add(air(e['d']), te, 0.14, .4)
    elif k == 'pluck': add(pluck(nt(e['n'])), te, 0.11, rs.uniform(-.3, .3))
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.5) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
