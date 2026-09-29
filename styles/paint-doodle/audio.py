# events.json -> audio.wav (48 kHz stereo, 9.6 s)
# Desktop-doodle foley: mouse clicks, text-tool pops, mouse-scribble scratches, stiff cut-out slides,
# bonks and thuds, a bucket-fill "bloop", a tiny square-wave fanfare, zoom stabs, chair squeaks.
import json, wave, numpy as np
SR, DUR = 48000, 9.6
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(82)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
nrm = lambda x: x / (np.abs(x).max() + 1e-9)
def click():
    t = tt(0.05); a = nrm(band(rs.standard_normal(len(t)), 2000, 9000)) * np.exp(-t / 0.002)
    b = nrm(band(rs.standard_normal(len(t)), 1500, 7000)) * np.exp(-(t - 0.025).clip(0) / 0.002) * (t > 0.025)
    return a + 0.6 * b
def pop(f=520):
    t = tt(0.12); fr = f * (1 + 0.8 * np.exp(-t / 0.01)); return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.035)
def scribble(d):
    t = tt(d); n = nrm(band(rs.standard_normal(len(t)), 1200, 6000))
    am = 0.5 + 0.5 * np.sin(2 * np.pi * 9 * t) ** 2; return n * am * np.sin(np.pi * t / d) ** 0.4
def slide(d):
    t = tt(d); n = nrm(band(rs.standard_normal(len(t)), 300, 2500)); return n * np.sin(np.pi * t / d) ** 2
def thud():
    t = tt(0.3); fr = 140 * np.exp(-t * 12) + 55
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.06) + 0.3 * nrm(band(rs.standard_normal(len(t)), 100, 1500)) * np.exp(-t / 0.02)
def bonk():
    t = tt(0.25); return (np.sin(2 * np.pi * 330 * t) + 0.5 * np.sin(2 * np.pi * 811 * t)) * np.exp(-t / 0.05)
def bloop():
    t = tt(0.35); fr = 300 + 900 * (t / 0.35) ** 0.6; return np.sign(np.sin(2 * np.pi * np.cumsum(fr) / SR)) * 0.4 * np.exp(-t / 0.15)
def square(f, d):
    t = tt(d); s = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + 0.5 * np.sin(2 * np.pi * f * t)
    return s * np.minimum(1, t / 0.005) * np.exp(-t / (d * 0.8))
def stab():
    t = tt(0.3); s = sum(np.sign(np.sin(2 * np.pi * f * t)) for f in (98, 116.5, 146.8)) / 3
    return s * np.exp(-t / 0.12)
def squeak(f):
    t = tt(0.16); fr = f * (1 + 0.25 * np.sin(np.pi * t / 0.16)); s = np.sin(2 * np.pi * np.cumsum(fr) / SR)
    s += 0.3 * np.sin(2 * 2 * np.pi * np.cumsum(fr) / SR); return s * np.sin(np.pi * t / 0.16) ** 1.5
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
# quiet room tone so the silences are not digital-dead
room = nrm(band(rs.standard_normal(N), 150, 2500)); L += room * .004; R += np.roll(room, 911) * .004
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'pop': add(pop(520 + 60 * rs.random()), te, 0.22 * v, rs.uniform(-.2, .2)); add(click(), te - 0.01, 0.12)
    elif k == 'click': add(click(), te, 0.35)
    elif k == 'scribble': add(scribble(e['d']), te, 0.07, -.2)
    elif k == 'stamp': add(thud(), te, 0.25); add(click(), te, 0.1)
    elif k == 'slide': add(slide(e['d']), te, 0.08)
    elif k == 'thud': add(thud(), te, 0.45)
    elif k == 'bonk': add(bonk(), te, 0.16 * v)
    elif k == 'fill': add(bloop(), te, 0.16)
    elif k == 'cut': add(click(), te, 0.08)
    elif k == 'fanfare':
        for i, (m, d) in enumerate([(67, .09), (67, .09), (72, .3)]): add(square(nt(m), d), te + [0, .1, .2][i], 0.07)
    elif k == 'zoom': add(stab(), te, 0.22)
    elif k == 'squeak': add(squeak(1500 + 180 * (v % 2)), te, 0.1, (-.4 if v % 2 else .4))
    elif k == 'end':
        for i, m in enumerate([72, 67, 64, 60]): add(square(nt(m), .22), te + i * .09, 0.05)
fi = int(0.05 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
