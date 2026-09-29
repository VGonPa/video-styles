# events.json -> audio.wav (48 kHz stereo, 10 s)
# Quiet, well-mannered sound for an opinion page, all synthesized: a soft Rhodes-like pad in D,
# each landing notification a small marimba note (climbing a pentatonic scale), felt footsteps as he
# backs away, a woody seesaw creak on every tilt, a hollow thunk when the phone slams down, a breathy
# whoosh for the catapult, a glassy shimmer while the metaphor morphs, a brass-pan ting when he lands,
# a low bell when the single dot outweighs him, a clock ticking under the punchline, and the
# two-note notification chime when the count quietly ticks over to 2.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(64)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def marimba(f, d=0.9):
    t = tt(d); return (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.28) + 0.35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t / 0.04)
                       + 0.15 * np.sin(2 * np.pi * f * 10 * t) * np.exp(-t / 0.01)) * np.minimum(1, t / 0.002)
def bell(f, d=3.0, tau=1.1):
    t = tt(d); x = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / (tau * k)) for a, r, k in [(1, 1, 1), (.5, 2.01, .6), (.35, 2.76, .45), (.2, 4.07, .3), (.12, 5.4, .2)])
    return x * np.minimum(1, t / 0.003)
def felt():
    t = tt(0.09); return norm(band(rs.standard_normal(len(t)), 120, 900)) * np.exp(-t / 0.018)
def creak(d=0.35, f0=180):
    t = tt(d); f = f0 + 40 * np.sin(2 * np.pi * 3 * t); ph = np.cumsum(f) / SR
    pulses = (np.sin(2 * np.pi * ph) > 0.97).astype(float)
    x = band(pulses + 0.2 * rs.standard_normal(len(t)), 300, 2600)
    return norm(x) * np.sin(np.pi * t / d) ** 1.5
def thunk():
    t = tt(0.6); f = 70 + 90 * np.exp(-t * 25); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.16) + 0.4 * norm(band(rs.standard_normal(len(t)), 200, 1800)) * np.exp(-t / 0.03)
def whoosh(d=0.8):
    t = tt(d); n = rs.standard_normal(len(t)); out = np.zeros(len(t)); k = 2400
    for i in range(0, len(t), k):
        c = 400 + 2600 * np.sin(np.pi * i / len(t)); out[i:i + k] = band(n[i:i + k], c * 0.6, c * 1.4)
    return norm(out) * np.sin(np.pi * t / d) ** 2
def shimmer(d=1.0):
    x = np.zeros(int(d * SR))
    for j, m in enumerate([74, 78, 81, 86, 90, 93]):
        s = bell(nt(m), d - j * 0.13, 0.35) * 0.4; i = int(j * 0.13 * SR); x[i:i + len(s)] += s[:len(x) - i]
    return x
def tick():
    t = tt(0.04); return norm(band(rs.standard_normal(len(t)), 2500, 7000)) * np.exp(-t / 0.004)
# pad bed: D maj9, slow swell, drifting to G maj7 after the morph
tg = np.arange(N) / SR
def chord(ms, a, b):
    x = sum(np.sin(2 * np.pi * nt(m) * tg + 0.3 * np.sin(2 * np.pi * 0.2 * tg)) for m in ms) / len(ms)
    env = np.clip((tg - a) / 0.8, 0, 1) * np.clip((b - tg) / 0.8, 0, 1); return x * env
pad = chord([50, 57, 62, 66, 69, 76], 0.0, 5.4) + chord([43, 55, 59, 62, 66, 71], 4.9, 10.4)
L += pad * 0.05; R += np.roll(pad, 300) * 0.05
PENT = [74, 76, 78, 81, 83, 86]
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'land':
        add(marimba(nt(PENT[e['v'] % 6])), te, 0.22, 0.35); add(creak(0.4, 150 + 20 * e['v']), te + 0.05, 0.05, 0.1)
    elif k == 'slam':
        add(thunk(), te + 0.06, 0.4, 0.2); add(marimba(nt(62)), te, 0.25, 0.3); add(creak(0.5, 120), te, 0.08)
    elif k == 'step': add(felt(), te, 0.12, -0.2)
    elif k == 'whoosh': add(whoosh(0.9), te, 0.14, -0.2)
    elif k == 'morph': add(shimmer(1.1), te, 0.16)
    elif k == 'fuse': add(marimba(nt(69), 0.6), te, 0.12, 0.4)
    elif k == 'pan': add(bell(nt(81), 1.2, 0.3), te, 0.09, -0.4); add(felt(), te, 0.2, -0.4)
    elif k == 'dong': add(bell(nt(38), 3.5, 1.4), te, 0.32, 0.35); add(thunk(), te, 0.2, 0.35)
    elif k == 'ding': add(bell(nt(83), 1.2, 0.35), te, 0.16, 0.4); add(bell(nt(88), 1.4, 0.4), te + 0.14, 0.16, 0.4)
    elif k == 'tick': add(tick(), te, 0.05, 0.1 if round(te * 2) % 2 else -0.1)
fi = int(0.1 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.4) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
