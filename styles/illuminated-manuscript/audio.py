# events.json → audio.wav (48 kHz stereo, 10 s)
# quill scratching each line, soft leaf-laying rustles and a glassy shimmer for each gilding and shine,
# leaf-pop ticks as the vines grow, a crackling oven, a slithering snail, the rabbit's little fanfare,
# a helm clanking to the ground, a page-turn swoosh, soft hops, and a plucked lute (Karplus-Strong) to open and close.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(97)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)

def lute(f, d=1.8, bright=0.3):
    n = int(d * SR); p = max(2, int(SR / f)); buf = rs.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]; j = (i + 1) % p
        buf[i % p] = 0.5 * (buf[i % p] + buf[j]) * (0.990 + 0.006 * bright)
    return band(out, 80, 5000) * np.minimum(1, np.arange(n) / 40)
def scratch(d, n):   # quill on vellum: filtered noise pulsed per letter stroke
    t = tt(d); x = band(rs.standard_normal(len(t)), 2200, 8000)
    rate = max(6, n / max(d, 0.05)) * 1.3; am = (0.35 + 0.65 * np.abs(np.sin(np.pi * rate * t + rs.uniform(0, 3)))) ** 2
    am *= 0.7 + 0.3 * band(rs.standard_normal(len(t)), 1, 30) / 0.02 * 0.02
    return norm(x) * am * np.clip(t / 0.02, 0, 1) * np.clip((d - t) / 0.03, 0, 1)
def rustle(d, lo=900, hi=5000):
    t = tt(d); x = band(rs.standard_normal(len(t)), lo, hi); am = band(rs.standard_normal(len(t)), 1, 18); am = np.abs(am) / (np.abs(am).max() + 1e-9)
    return norm(x) * am * np.sin(np.pi * np.clip(t / d, 0, 1))
def shimmer(d=1.2, base=1568):
    t = tt(d); out = np.zeros(len(t))
    for k, (m, dl) in enumerate([(1, 0), (1.5, 0.06), (2, 0.12), (2.52, 0.18), (3, 0.24)]):
        tk = np.clip(t - dl, 0, None); out += np.sin(2 * np.pi * base * m * tk) * np.exp(-tk * 4) * (t >= dl) * (0.9 ** k)
    return out * 0.5
def tick():
    t = tt(0.04); return np.sin(2 * np.pi * 2600 * t) * np.exp(-t / 0.006) + 0.5 * band(rs.standard_normal(len(t)), 3000, 9000) * np.exp(-t / 0.004)
def crackle(d, dens=40):
    t = tt(d); k = np.zeros(len(t)); idx = rs.integers(0, len(t), int(dens * d)); k[idx] = rs.uniform(0.2, 1, len(idx))
    k = band(k, 900, 9000); hiss = band(rs.standard_normal(len(t)), 200, 1200) * 0.15
    return (norm(k) + hiss) * np.clip(t / 0.4, 0, 1) * np.clip((d - t) / 0.4, 0, 1)
def slither(d):
    t = tt(d); x = band(rs.standard_normal(len(t)), 250, 1500) * (0.6 + 0.4 * np.sin(2 * np.pi * 2.5 * t)); return norm(x) * np.sin(np.pi * t / d)
def brass(f, d, vib=5.5):
    t = tt(d); ph = 2 * np.pi * f * t + 0.08 * np.sin(2 * np.pi * vib * t) * np.clip(t / 0.15, 0, 1) * 6
    s = sum(np.sin(k * ph) / k ** 1.1 for k in range(1, 9)); s = band(s, 150, 4200)
    env = np.clip(t / 0.03, 0, 1) * np.clip((d - t) / 0.05, 0, 1); return norm(s) * env
def slide_whistle(d=0.3, f0=1500, f1=380):
    t = tt(d); f = f0 * (f1 / f0) ** (t / d); ph = 2 * np.pi * np.cumsum(f) / SR; return np.sin(ph) * np.sin(np.pi * t / d) ** 0.5
def clank():
    t = tt(0.5); out = np.zeros(len(t))
    for f, dcy in [(820, 0.12), (1370, 0.09), (2210, 0.07), (3380, 0.05)]: out += np.sin(2 * np.pi * f * t) * np.exp(-t / dcy)
    return out * 0.4 + band(rs.standard_normal(len(t)), 1500, 8000) * np.exp(-t / 0.01)
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); out = np.zeros(len(t)); seg = len(t) // 10
    for k in range(10):
        a, b = k * seg, (k + 1) * seg; lo = 300 + 250 * np.sin(np.pi * k / 9) * 4; out[a:b] = band(x, lo, lo + 2200)[a:b]
    flutter = 0.75 + 0.25 * np.sin(2 * np.pi * 22 * t)
    return norm(out) * np.sin(np.pi * t / d) ** 1.5 * flutter
def thud(f=90, d=0.2):
    t = tt(d); return np.sin(2 * np.pi * (f + 50 * np.exp(-t * 30)) * t) * np.exp(-t / 0.05) + 0.3 * band(rs.standard_normal(len(t)), 200, 1500) * np.exp(-t / 0.012)

ev = json.load(open('events.json'))
t = np.arange(N) / SR
room = norm(band(rs.standard_normal(N), 60, 700)); L += room * 0.008; R += np.roll(room, 999) * 0.008
# opening lute: a quiet D-dorian arpeggio
for i, m in enumerate([50, 57, 62, 65, 69]): add(lute(nt(m), 2.4), 0.25 + i * 0.16, 0.16, -0.4 + i * 0.2)
fire_t = next(e['t'] for e in ev if e['k'] == 'fire'); lift_t = next(e['t'] for e in ev if e['k'] == 'lift')
add(crackle(lift_t + 0.4 - fire_t), fire_t, 0.03, 0.45)
for e in ev:
    k, te = e['k'], e['t']
    if k == 'write':
        pan = -0.35 if te < 4.2 else (0.3 if te < 6 else 0.35)
        add(scratch(e['d'], e['n']), te, 0.055 if not e['red'] else 0.05, pan)
    elif k == 'gild': add(rustle(e['d'] + 0.2, 1500, 7000), te, 0.05, -0.3 if te < 2.5 else 0.3); add(shimmer(1.0, 1318), te + e['d'] * 0.6, 0.035, 0.0)
    elif k == 'shine': add(shimmer(1.4, 1976), te, 0.05, -0.2 if te < 2.8 else 0.3)
    elif k == 'vine':
        add(rustle(e['d'], 600, 3500), te, 0.03, -0.5 if te < 2.2 else 0.5)
        for q in np.sort(rs.uniform(te + 0.2, te + e['d'], 12)): add(tick(), q, 0.025, (-0.6 if te < 2.2 else 0.6) + rs.uniform(-0.2, 0.2))
    elif k == 'paint':
        for q in np.linspace(te, te + e['d'] - 0.15, 5): add(rustle(0.25, 500, 3000), q, 0.035, 0.35)
    elif k == 'snail': add(slither(e['d']), te, 0.05, 0.1)
    elif k == 'trumpet':
        for m, dt, dd in [(67, 0, 0.1), (67, 0.11, 0.08), (72, 0.2, 0.1), (76, 0.31, 0.24)]: add(brass(nt(m), dd), te + dt, 0.07, 0.45)
    elif k == 'retreat': add(slide_whistle(), te, 0.03, 0.15)
    elif k == 'clank': add(clank(), te, 0.07, 0.2); add(clank(), te + 0.18, 0.03, 0.22)
    elif k == 'lift': add(rustle(0.3, 2000, 9000), te, 0.06, 0.4)
    elif k == 'turn': add(whoosh(e['d'] + 0.1), te, 0.12, 0.0)
    elif k == 'land': add(thud(70, 0.3), te, 0.12, -0.3); add(rustle(0.2, 1500, 6000), te, 0.04, -0.3)
    elif k == 'hop': add(thud(130, 0.14), te, 0.05, 0.3)
    elif k == 'grab': add(lute(nt(81), 0.8, 0.8), te, 0.05, 0.3)
    elif k == 'end':
        for i, m in enumerate([74, 72, 69, 65, 62]): add(lute(nt(m), 2.2), te + i * 0.17, 0.14, 0.4 - i * 0.18)
        add(lute(nt(50), 2.6), te + 0.9, 0.16, 0.0); add(lute(nt(57), 2.4), te + 0.93, 0.1, 0.1)
fi = int(0.15 * SR); fo = int(0.8 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.6
st = np.stack([L, R], 1); st = np.tanh(st * 4.0) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
