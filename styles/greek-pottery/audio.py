# events.json -> audio.wav (48 kHz stereo, 10 s), all synthesized
# plucked lyre (Karplus-Strong) motif in E Dorian over a soft reed drone, ratchet spins and clay "tock" locks for
# the bands, soft footfalls and hollow hoof clops, a whoosh for the rollout, an owl's two-note hoot,
# brush swishes for the painted letters, leafy rustle for the laurel, and a final lyre strum.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(94)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def pluck(f, d=1.6, bright=0.5):
    n = int(d * SR); P = max(2, int(SR / f)); buf = rs.uniform(-1, 1, P)
    buf = band(np.concatenate([buf] * 4), 60, 2000 + 5000 * bright)[:P]
    out = np.zeros(n); b = buf.copy(); idx = 0
    for i in range(n):
        out[i] = b[idx]; nxt = (idx + 1) % P; b[idx] = 0.5 * (b[idx] + b[nxt]) * 0.9965; idx = nxt
    body = np.sin(2 * np.pi * f * tt(d)) * np.exp(-tt(d) / 0.5) * 0.15
    return norm(out + body) * np.exp(-tt(d) / (d * 0.55))
def knock(f=900, d=0.12, dec=0.018):
    t = tt(d); n = band(rs.standard_normal(len(t)), f * .6, f * 1.8) * np.exp(-t / dec)
    return norm(n) * 0.7 + np.sin(2 * np.pi * f * .35 * t) * np.exp(-t / (dec * 1.4)) * 0.6
def thud():
    t = tt(0.14); s = np.sin(2 * np.pi * (70 + 60 * np.exp(-t * 40)) * t) * np.exp(-t / 0.035)
    n = band(rs.standard_normal(len(t)), 200, 1800) * np.exp(-t / 0.012)
    return s + 0.35 * norm(n)
def swish(d, lo=1800, hi=7000):
    t = tt(d); n = band(rs.standard_normal(len(t)), lo, hi); env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.2 * np.exp(-t / d * 1.2)
    return norm(n) * env
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 180 + 2200 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.6
def hoot():
    out = np.zeros(int(1.0 * SR))
    for t0, f, d in [(0, 392, .28), (.38, 370, .42)]:
        t = tt(d); v = 1 + 0.012 * np.sin(2 * np.pi * 6 * t); ph = 2 * np.pi * np.cumsum(f * v) / SR
        env = np.minimum(1, t / .05) * np.exp(-np.maximum(0, t - .08) / (d * .5))
        s = (np.sin(ph) + 0.15 * np.sin(2 * ph)) * env + 0.03 * band(rs.standard_normal(len(t)), 300, 1500) * env
        i = int(t0 * SR); out[i:i + len(s)] += s
    return out
def rustle(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 1500, 8000)
    am = np.abs(band(rs.standard_normal(len(t)), 8, 50)); am = am / (am.max() + 1e-9)
    return norm(n) * am * np.sin(np.pi * t / d) ** .8
def ratchet(d, rate0=26, rate1=6):
    out = np.zeros(int((d + .2) * SR)); t = 0.0
    while t < d:
        u = t / d; r = rate0 + (rate1 - rate0) * u; k = knock(1800 + 600 * rs.random(), .04, .004) * (1 - .6 * u)
        i = int(t * SR); out[i:i + len(k)] += k[:len(out) - i]; t += 1 / r
    return out
t = np.arange(N) / SR
# drone: soft reed on E2 + B2, slow breathing, swelling a little at the rollout
for f, g, p in [(nt(40), .04, -.2), (nt(47), .025, .25), (nt(52), .012, 0)]:
    ph = 2 * np.pi * f * t; s = np.sin(ph) + .35 * np.sin(2 * ph) + .18 * np.sin(3 * ph) + .08 * np.sin(5 * ph)
    env = np.clip(t / 1.2, 0, 1) * (1 + .15 * np.sin(2 * np.pi * .2 * t + p)) * (1 + .4 * np.exp(-((t - 6.2) / 1.2) ** 2))
    L += s * g * env * (1 - p * .5); R += s * g * env * (1 + p * .5)
# turntable rumble while the vase turns
rum = band(rs.standard_normal(N), 30, 160); rum = norm(rum) * np.clip(t / .8, 0, 1) * np.clip((5.4 - t) / .8, 0, 1)
L += rum * .05; R += rum * .05
# lyre motif (E Dorian): a patient arpeggio that stops when the runner wins
motif = [52, 59, 64, 62, 59, 57, 59, 64, 66, 64, 62, 59, 57, 55, 57, 59]
for i, m in enumerate(motif):
    te = 0.55 + i * 0.42
    if te > 7.0: break
    add(pluck(nt(m), 1.6, .45), te, 0.12 * (0.85 + .3 * rs.random()), (-.3 if i % 2 else .3))
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'spin': add(ratchet(e['d']), te, 0.07 * v, rs.uniform(-.4, .4))
    elif k == 'lock': add(knock(700, .16, .03), te, 0.35 * v, rs.uniform(-.2, .2))
    elif k == 'step': add(thud(), te, 0.16 * v, e.get('p', 0))
    elif k == 'hoof': add(knock(520 + 120 * rs.random(), .08, .012), te, 0.05 * v, -.35)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.2)
    elif k == 'hoot': add(hoot(), te, 0.11, -.35)
    elif k == 'wreath': add(rustle(0.7), te, 0.06, -.3)
    elif k == 'grow': add(rustle(e['d']), te, 0.05, .2)
    elif k == 'brush': add(swish(0.13), te, 0.07, rs.uniform(-.2, .4))
    elif k == 'chord':
        for i, m in enumerate([40, 47, 52, 55, 59, 64]): add(pluck(nt(m), 2.2, .6), te + i * 0.035, 0.1, -.3 + i * .12)
# master: fade in/out, soft limiter
fi = int(0.3 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.82
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
