# events.json → audio.wav (48 kHz stereo, 10 s). All synthesized:
# a quiet gallery room tone with two distant footsteps, a dip pen scratching for every stroke,
# a soft brush swish as the wash goes down, a dry two-note double-bass "beat" under each caption,
# a paper page turn, a cocktail-party murmur on the second page, ice clinking in a tumbler.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(63)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def env(t, d, a=.01, r=.05): return np.minimum(1, t / a) * np.clip((d - t) / r, 0, 1)
def scratch(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 2500, 9000))
    grain = 0.5 + 0.5 * np.abs(np.sin(2 * np.pi * (17 + 6 * rs.random()) * t))
    return n * grain * env(t, d, .015, .04)
def swish(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 500, 3500))
    return n * np.sin(np.pi * t / d) ** 2
def bass(f, d=.5):
    t = tt(d); s = np.sin(2 * np.pi * f * t) + .35 * np.sin(4 * np.pi * f * t) + .1 * np.sin(6 * np.pi * f * t)
    return s * np.exp(-t / .16) * np.minimum(1, t / .004)
def step():
    t = tt(.25); return norm(band(rs.standard_normal(len(t)), 80, 900)) * np.exp(-t / .03)
def clink(f):
    t = tt(.6); s = sum(np.sin(2 * np.pi * f * k * t) * np.exp(-t / (.12 / k)) for k in (1, 2.76, 5.4))
    return s * np.minimum(1, t / .001)
def flip(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 300, 6000))
    flutter = 0.55 + 0.45 * np.sin(2 * np.pi * (22 - 10 * t / d) * t) ** 2
    return n * flutter * np.sin(np.pi * t / d) ** 1.2
t = np.arange(N) / SR
room = norm(band(rs.standard_normal(N), 60, 500)) * 0.012
L += room; R += np.roll(room, 3001)
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'pen': add(scratch(max(.04, e['d'])), te, 0.035, rs.uniform(-.2, .2))
    elif k == 'wash': add(swish(.55), te, 0.05, -.1); add(swish(.4), te + .25, 0.035, .15)
    elif k == 'beat': add(bass(55.0), te, 0.22); add(bass(41.2, .7), te + .2, 0.2)
    elif k == 'step': add(step(), te, 0.05, .5)
    elif k == 'turn': add(flip(e['d']), te, 0.16, -.2)
    elif k == 'clink': add(clink(2350 + rs.uniform(-150, 150)), te, 0.05, .25); add(clink(3100), te + .045, 0.03, .25)
    elif k == 'sip': add(norm(band(rs.standard_normal(int(.3 * SR)), 1500, 5000)) * np.sin(np.pi * tt(.3) / .3), te, 0.012, .2)
    elif k in ('room', 'party') and k == 'party':
        d = e['d']; tl = tt(d)
        m = sum(norm(band(rs.standard_normal(len(tl)), lo, hi)) * (0.5 + 0.5 * np.sin(2 * np.pi * r * tl + rs.random() * 6)) ** 2
                for lo, hi, r in [(250, 700, 3.1), (400, 1100, 4.3), (300, 900, 2.2), (600, 1600, 5.1)])
        m = norm(band(m, 200, 1800)) * np.minimum(1, tl / .8) * np.clip((d - tl) / .6, 0, 1)
        add(m, te, 0.03, -.3); add(np.roll(m, 7777), te, 0.03, .3)
fi = int(0.2 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.0) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
