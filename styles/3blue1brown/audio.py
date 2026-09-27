# events.json → audio.wav (48 kHz stereo, 10 s)
# calm, 3b1b-like bed: soft felt-piano notes rising with each odd layer, tiny ticks as squares land,
# a gentle two-note chime for the equation morph, a warm chord when the result is boxed,
# airy swells for the number plane and the matrix warp, and a low resolving note under the fade-out.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(24)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def piano(m, d=2.2, bright=1.0):
    # felt piano: slightly inharmonic partials, upper partials decay faster, soft hammer attack
    t = tt(d); f0 = nt(m); s = np.zeros_like(t)
    for h, a in [(1, 1.0), (2, .42), (3, .2), (4, .1), (5, .05), (6, .025)]:
        fh = f0 * h * np.sqrt(1 + 0.0004 * h * h)
        s += a * bright ** (h - 1) * np.sin(2 * np.pi * fh * t) * np.exp(-t * (1.6 + 1.3 * h))
    att = np.minimum(1, t / 0.006); rel = np.minimum(1, (d - t) / 0.3)
    thump = band(rs.standard_normal(len(t)), 80, 900) * np.exp(-t / 0.01) * 0.04
    return (s * att + thump) * rel
def tick(f=2600):
    t = tt(0.05); return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.006) + 0.3 * band(rs.standard_normal(len(t)), 3000, 9000) * np.exp(-t / 0.003)
def swell(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 300, 2400); n /= np.abs(n).max() + 1e-9
    return n * np.sin(np.pi * t / d) ** 2
def pad(m, d, att=1.5, rel=1.5):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * nt(m) * h * t + h) for h, a in [(1, 1), (2, .25), (3, .08)])
    return s * np.minimum(1, t / att) * np.minimum(1, (d - t) / rel) * (1 + .1 * np.sin(2 * np.pi * .3 * t))
# bed: very quiet sustained pad (C major colour) over the whole clip
for m, g, p in [(48, .03, -.2), (55, .022, .2), (64, .014, 0)]: add(pad(m, 9.8, 1.8, 1.4), 0.1, g, p)
SCALE = [72, 74, 76, 79, 81]            # C5 D5 E5 G5 A5 — one step up per odd layer
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'note':
        n = e['n']; add(piano(SCALE[n], 2.2), te, 0.22, -.3 + .15 * n); add(piano(SCALE[n] - 12, 2.2, .7), te, 0.08, 0)
    elif k == 'tick': add(tick(2400 + 180 * rs.random()), te, 0.018 * e.get('v', 1), rs.uniform(-.4, .4))
    elif k == 'soft': add(piano(60, 2.0, .6), te, 0.12, -.2); add(piano(67, 2.0, .6), te + .08, 0.08, .2)
    elif k == 'morph':
        add(piano(84, 1.8, .8), te + .05, 0.1, -.3); add(piano(88, 1.8, .8), te + e['d'] * .6, 0.1, .3)
    elif k == 'chord':
        for i, m in enumerate([48, 60, 64, 67, 71, 76]): add(piano(m, 3.2, .8), te + i * .035, 0.11 if m > 50 else 0.14, -.4 + i * .16)
    elif k == 'swell': add(swell(e['d']), te, 0.035, rs.uniform(-.2, .2))
    elif k == 'end': add(piano(48, 1.6, .5), te, 0.14); add(piano(55, 1.6, .5), te + .05, 0.08, .2)
# master: short fade-in, fade-out under the visual FadeOut, soft limiter
fi = int(0.2 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
