# events.json → audio.wav (48 kHz stereo, 10 s), all synthesized
# felt-tip pen strokes, quick lettering scratches, a long marker line with little squeaks at each step,
# a rising whistle for the spike, a soft paper slide for the pan, a mouse tick and a tooltip pop.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(87)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def nrm(x): return x / (np.abs(x).max() + 1e-9)
def noise(d, lo, hi): return nrm(band(rs.standard_normal(int(d * SR)), lo, hi))
def env(t, d, a=.02, r=.04): return np.minimum(1, t / a) * np.clip((d - t) / r, 0, 1)
def pen(d, rate=(6, 30)):
    t = tt(d); n = noise(d, 1500, 6000); am = nrm(np.abs(band(rs.standard_normal(len(t)), *rate)))
    return n * (.35 + .65 * am) * env(t, d)
def write(d):  # lettering: rhythmic short strokes
    t = tt(d); n = noise(d, 2000, 7500); g = (np.sin(2 * np.pi * 11 * t + rs.random() * 6) > -.2).astype(float)
    g = band(g, 0, 60); return n * np.clip(g, 0, 1) * env(t, d, .01, .03)
def marker(d):  # felt marker dragged on a whiteboard: band noise + faint squeaky tone
    t = tt(d); n = noise(d, 900, 4500) * (.7 + .3 * np.sin(2 * np.pi * 3.1 * t))
    f = 1250 + 90 * np.sin(2 * np.pi * .8 * t); sq = np.sin(2 * np.pi * np.cumsum(f) / SR) * .08
    return (n + sq) * env(t, d, .04, .08)
def squeak(v=1):
    d = .12; t = tt(d); f = 1700 + 900 * t / d; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 2 * v
def rise():
    d = .45; t = tt(d); f = 700 * 2 ** (2.2 * t / d); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 1.5 * .5
def slide(d):
    t = tt(d); return noise(d, 250, 2200) * np.sin(np.pi * t / d) ** 2
def tick():
    t = tt(.03); return noise(.03, 2500, 9000) * np.exp(-t / .004)
def pop():
    t = tt(.18); f = 1400 * np.exp(-t * 30) + 500
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .05) * .6
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0); pan = rs.uniform(-.2, .2)
    if k == 'pen': add(pen(e['d']), te, .10 * v, pan)
    elif k == 'write': add(write(e['d']), te, .045, pan)
    elif k == 'marker': add(marker(e['d']), te, .09 * v, .1)
    elif k == 'squeak': add(squeak(v), te, .05, .15)
    elif k == 'rise': add(rise(), te, .09, .3)
    elif k == 'slide': add(slide(e['d']), te, .12, 0)
    elif k == 'tick': add(tick(), te, .12, -.2)
    elif k == 'pop': add(pop(), te, .12, -.2)
# faint room tone so the track never drops to digital silence
L += noise(DUR, 80, 900) * .004; R += noise(DUR, 80, 900) * .004
fi = int(.05 * SR); fo = int(.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 3.4) * .9
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
