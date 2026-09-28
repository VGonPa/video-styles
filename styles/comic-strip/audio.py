# events.json → audio.wav (48 kHz stereo, 10 s)
# newsprint rustle, brush-pen scratches for the title, ruled-pen strokes for each panel border,
# soft balloon pops, a leaf rustle on the shrug, the to-do list unrolling, a clock ticking through
# the silent beat, a gentle push-in swell, a wry two-note pluck on the punchline, the strip sliding
# off the page and a small closing chord. All synthesized.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(58)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def rustle(d=0.45, lo=900, hi=7000):
    t = tt(d); n = band(rs.standard_normal(len(t)), lo, hi)
    am = np.abs(band(rs.standard_normal(len(t)), 5, 40)); am /= am.max() + 1e-9
    return norm(n) * am * np.sin(np.pi * t / d) ** 0.7
def scratch(d, lo=2000, hi=6500, grain=True):
    # pen nib on newsprint: band noise with fibre "catches"
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), lo, hi))
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.4
    if grain: env *= 0.65 + 0.35 * np.abs(np.sin(2 * np.pi * (23 + 9 * rs.random()) * t + rs.random() * 6))
    return n * env
def pop():
    t = tt(0.12); f = 520 * np.exp(-t * 30) + 240; ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t / 0.03)
    click = norm(band(rs.standard_normal(len(t)), 1500, 6000)) * np.exp(-t / 0.004)
    return body + 0.35 * click
def tick(hi=True):
    t = tt(0.05); n = norm(band(rs.standard_normal(len(t)), 2500 if hi else 1600, 8000)) * np.exp(-t / 0.006)
    return n + 0.4 * np.sin(2 * np.pi * (1800 if hi else 1400) * t) * np.exp(-t / 0.01)
def whoosh(d, f0=200, f1=1800):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = f0 + (f1 - f0) * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
def mallet(freq, d=0.9):
    t = tt(d); s = np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.28) + 0.25 * np.sin(2 * np.pi * freq * 3.99 * t) * np.exp(-t / 0.05)
    return s * np.minimum(1, t / 0.002)
def pluck(freq, d=0.8):  # plucked string (Karplus-Strong)
    n = int(d * SR); P = int(SR / freq); buf = rs.uniform(-1, 1, P); out = np.zeros(n)
    for i in range(n): out[i] = buf[i % P]; buf[i % P] = 0.5 * (buf[i % P] + buf[(i + 1) % P]) * 0.996
    return out * np.exp(-np.arange(n) / SR / 0.35)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
# bed: quiet room tone (a morning kitchen), fades in
t = np.arange(N) / SR
room = norm(band(rs.standard_normal(N), 120, 1800)); env = np.clip(t / 0.6, 0, 1)
L += room * 0.010 * env; R += np.roll(room, 911) * 0.010 * env
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'rustle': add(rustle(0.7, 500, 6000), te, 0.20, -0.2)
    elif k == 'pen':
        d = e['d']; n = 6
        for i in range(n): add(scratch(d / n * 0.8, 1800, 6000), te + d * i / n + rs.uniform(0, .02), 0.07, rs.uniform(-.3, .3))
    elif k == 'rule':
        d = e['d']
        for i in range(4): add(scratch(d / 4 * 0.9, 2500, 7500), te + d * i / 4, 0.05, -0.4 + i * 0.25)
    elif k == 'pop': add(pop(), te, 0.28 * v, rs.uniform(-.2, .2))
    elif k == 'leaf': add(rustle(0.35, 2000, 9000), te, 0.07, 0.3)
    elif k == 'unroll':
        d = e['d']; add(rustle(d, 700, 6000), te, 0.12, 0.1)
        for i in range(9): add(tick(False), te + d * (i / 9) ** 0.7, 0.04, 0.1)
    elif k == 'clock':
        for i in range(4): add(tick(i % 2 == 0), te + i * 0.5, 0.06, 0.35)
    elif k == 'push': add(whoosh(e['d'], 120, 900), te, 0.10)
    elif k == 'pluck':
        add(pluck(nt(55)), te, 0.22, -0.1); add(pluck(nt(60)), te + 0.22, 0.22, 0.1)
        add(mallet(nt(79)), te + 0.22, 0.04)
    elif k == 'slide': add(whoosh(e['d'], 300, 2600), te, 0.16); add(rustle(0.5, 600, 5000), te + 0.05, 0.10)
    elif k == 'chord':
        for i, m in enumerate([60, 64, 67, 72]): add(mallet(nt(m + 12), 1.0), te + i * 0.06, 0.05, -0.3 + i * 0.2)
        add(pluck(nt(36), 1.0), te, 0.12)
# a soft walking bass under the setup; it drops out for the silent beat and returns after the punchline
BEAT = 0.6; line = [36, 40, 43, 45, 41, 45, 48]
for i, m in enumerate(line):
    add(pluck(nt(m), 0.7), 0.5 + i * BEAT, 0.16, -0.15)
for i, m in enumerate([43, 47, 48]):
    add(pluck(nt(m), 0.7), 7.95 + i * BEAT, 0.13, -0.15)
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 3.0) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
