# events.json → audio.wav (48 kHz stereo, 10 s)
# fine-nib pen on paper, steam hiss, soft air whooshes for each morph, bird chirps, sunrise swell with glass chimes,
# a warm morning pad (F major) and a closing piano-like chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(8)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def pen(d):
    # nib scratch: band noise with a slow grain and small stroke accents
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 2200, 8000))
    grain = np.abs(band(rs.standard_normal(len(t)), 8, 60)); grain = 0.55 + 0.45 * norm(grain)
    env = np.minimum(1, t / 0.08) * np.minimum(1, (d - t) / 0.2)
    return n * grain * env
def hiss(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 3000, 11000)); return n * np.sin(np.pi * t / d) ** 2
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 180 + 1600 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.6
def chirp(v=1.0):
    out = np.zeros(int(0.5 * SR)); o = 0
    for k in range(3 if v > .6 else 2):
        d = 0.05 + 0.02 * rs.random(); t = tt(d)
        f = 3200 + 1600 * np.sin(np.pi * t / d) + 300 * rs.random()
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 1.5
        out[o:o + len(s)] += s; o += len(s) + int((0.03 + 0.03 * rs.random()) * SR)
    return out
def tone(freq, d, att=0.4, rel=1.0, parts=((1, 1), (2, .3), (3, .12))):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in parts)
    env = np.minimum(1, t / att) * np.minimum(1, np.maximum(0, (d - t)) / rel); return s * env
def pluck(freq, d=2.4):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) * np.exp(-t * (1.6 + h * 0.9)) for h, a in [(1, 1), (2, .45), (3, .2), (4, .1)])
    return s * np.minimum(1, t / 0.004)
def chime(freq):
    t = tt(2.0); return (np.sin(2 * np.pi * freq * t) + .3 * np.sin(2 * np.pi * freq * 2.76 * t)) * np.exp(-t * 2.2) * np.minimum(1, t / 0.003)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR
room = norm(band(rs.standard_normal(N), 150, 2500)); L += room * .004; R += np.roll(room, 911) * .004
# morning pad: F major, slowly swelling toward the sunrise
for m, g, p in [(53, .045, -.3), (60, .03, .3), (65, .022, 0), (69, .016, .2)]:
    d = 9.6; s = tone(nt(m), d, 2.0, 1.4) * (1 + .12 * np.sin(2 * np.pi * .2 * tt(d)))
    s *= 0.6 + 0.4 * np.clip((tt(d) - 5.0) / 2.0, 0, 1); add(s, 0.3, g, p)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'pen': add(pen(e['d']), te, 0.05, -.1)
    elif k == 'steam': add(hiss(1.0), te, 0.025, .1)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.13, rs.uniform(-.2, .2))
    elif k == 'chirp': add(chirp(v), te, 0.05 * v, .35)
    elif k == 'sun':
        add(tone(nt(77), 2.6, 1.2, 1.2) + tone(nt(81), 2.6, 1.3, 1.2), te, 0.02)
        for i, m in enumerate([84, 88, 91, 96]): add(chime(nt(m)), te + 0.5 + i * 0.16, 0.035, -.3 + i * .2)
    elif k == 'chord':
        for i, m in enumerate([41, 53, 60, 65, 69, 72]): add(pluck(nt(m)), te + i * 0.035, 0.07 if m < 50 else 0.05, -.2 + i * .08)
    elif k == 'retract': add(pen(e['d']) * np.linspace(1, 0.3, int(e['d'] * SR)), te, 0.025, .1)
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.8 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 3.2) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
