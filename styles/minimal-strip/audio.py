# events.json → audio.wav (48 kHz stereo, 10 s)
# a quiet afternoon in a park: soft breeze and far-off birds, fine-nib pen scratches as each panel
# border is drawn, soft paper ticks for balloons, a dry leaf tumbling and settling, a small sigh,
# a few sparse felt-piano notes for the punchline, the paper sliding away, and a last soft chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(89)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def pen(d):   # fine nib on paper: filtered noise with a scratchy, stroke-by-stroke envelope
    t = tt(d); n = band(rs.standard_normal(len(t)), 2500, 9000)
    am = np.abs(band(rs.standard_normal(len(t)), 6, 40)); am = norm(am) * 0.7 + 0.3
    return norm(n) * am * np.sin(np.pi * t / d) ** 0.6
def tick():   # soft paper tick for a balloon
    t = tt(0.09); n = band(rs.standard_normal(len(t)), 800, 5000) * np.exp(-t / 0.008)
    return 0.6 * norm(n) + 0.4 * np.sin(2 * np.pi * 660 * t) * np.exp(-t / 0.02)
def rustle(d):  # a dry leaf tumbling: sparse crackles
    t = tt(d); out = np.zeros(len(t)); k = 0.0
    while k < d - 0.03:
        c = band(rs.standard_normal(int(0.03 * SR)), 1800, 8000) * np.exp(-np.arange(int(0.03 * SR)) / SR / 0.005)
        i = int(k * SR); out[i:i + len(c)] += norm(c) * (0.3 + 0.7 * rs.random()); k += rs.uniform(0.05, 0.16)
    return out * np.sin(np.pi * t / d) ** 0.5
def land():
    t = tt(0.06); return norm(band(rs.standard_normal(len(t)), 1500, 7000)) * np.exp(-t / 0.01)
def sigh(d):  # breathy exhale: band-limited noise, a slow swell and long release
    t = tt(d); n = band(rs.standard_normal(len(t)), 300, 2400)
    env = np.minimum(1, t / 0.25) ** 1.5 * np.exp(-np.maximum(0, t - 0.35) / 0.35)
    return norm(n) * env
def slide(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 400, 5000)
    return norm(n) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5
def piano(f, d=2.4):  # soft felt piano: few harmonics, slight inharmonicity, fast attack, long decay
    t = tt(d); s = np.zeros(len(t))
    for h, a in [(1, 1.0), (2, 0.35), (3, 0.12), (4, 0.05)]:
        s += a * np.sin(2 * np.pi * f * h * (1 + 0.0004 * h * h) * t) * np.exp(-t / (0.9 / h ** 0.6))
    return s * np.minimum(1, t / 0.006)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
# bed: soft breeze + two distant birds
t = np.arange(N) / SR
air = norm(band(rs.standard_normal(N), 80, 1200)); air2 = norm(band(rs.standard_normal(N), 80, 1200))
sw = 0.75 + 0.25 * np.sin(2 * np.pi * 0.13 * t + 1.0)
L += air * 0.022 * sw; R += air2 * 0.022 * sw
def bird(f0):
    tb = tt(0.16); f = f0 * (1 + 0.25 * np.sin(np.pi * tb / 0.16)); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.sin(np.pi * tb / 0.16) ** 2
for bt, bf, bp in [(1.4, 3300, -0.6), (1.62, 3600, -0.6), (6.3, 3100, 0.7), (6.5, 3450, 0.7)]:
    add(bird(bf), bt, 0.012, bp)
ev = json.load(open('events.json'))
for e in ev:
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'pen': add(pen(e['d']), te, 0.05 * v, -0.2)
    elif k == 'pop': add(tick(), te, 0.10)
    elif k == 'leaf': add(rustle(e['d']), te, 0.05 * v, 0.2)
    elif k == 'land': add(land(), te, 0.06 * v, 0.1)
    elif k == 'sigh': add(sigh(e['d']), te, 0.07, -0.2)
    elif k == 'slide': add(slide(e['d']), te, 0.10, -0.3)
    elif k == 'note':
        for i, m in enumerate(e['n']): add(piano(nt(m)), te + i * 0.28, 0.07, 0.1 * (i - 0.5))
    elif k == 'chord':
        for i, m in enumerate([60, 64, 67, 71]): add(piano(nt(m), 3.0), te + i * 0.07, 0.055, -0.3 + 0.2 * i)
fi = int(0.2 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 3.2) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
