# events.json → audio.wav (48 kHz stereo, 10 s)
# music-box lullaby in F major, dawn birds, soft paw pats, paper page-turn swishes with a flop,
# a glint "ting", the button's snap into place, and a closing arpeggio.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(84)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def mbox(m, d=1.6, bright=1.0):
    t = tt(d); f = nt(m)
    s = sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (tau)) for h, a, tau in [(1, 1, .9), (2, .28 * bright, .45), (3, .08 * bright, .25), (5.43, .07 * bright, .12)])
    click = band(rs.standard_normal(len(t)), 3000, 9000) * np.exp(-t / 0.002) * 0.06
    return (s + click) * np.minimum(1, t / 0.002)
def chirp(f0, f1, d):
    t = tt(d); f = np.linspace(f0, f1, len(t)); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph + 2 * np.sin(2 * np.pi * 38 * t)) * np.sin(np.pi * t / d) ** 2
def ting(f=2637):
    t = tt(1.0); return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.5 * t) + .25 * np.sin(2 * np.pi * f * 2.76 * t)) * np.exp(-t / 0.28)
def pat():
    t = tt(0.08); n = band(rs.standard_normal(len(t)), 150, 1600) * np.exp(-t / 0.012)
    return 0.6 * n / (np.abs(n).max() + 1e-9) + 0.5 * np.sin(2 * np.pi * 110 * t) * np.exp(-t / 0.02)
def pop():
    t = tt(0.12); f = 900 * np.exp(-t * 30) + 280; ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.03)
def snap():
    t = tt(0.05); n = band(rs.standard_normal(len(t)), 2000, 8000) * np.exp(-t / 0.004)
    return n / (np.abs(n).max() + 1e-9) + 0.4 * np.sin(2 * np.pi * 320 * t) * np.exp(-t / 0.015)
def swish(d):
    # a page leaf: rising papery hiss with flutter, then a soft flop as it lands
    t = tt(d + 0.4); x = rs.standard_normal(len(t))
    y = band(x, 500, 6500); y /= np.abs(y).max() + 1e-9
    u = np.clip(t / d, 0, 1); env = np.sin(np.pi * u) ** 1.2 * (0.75 + 0.25 * np.sin(2 * np.pi * 23 * t)) * (t < d)
    lo = band(x, 80, 500); lo /= np.abs(lo).max() + 1e-9
    flop = lo * np.exp(-np.clip(t - d * 0.92, 0, None) / 0.05) * (t > d * 0.92) * 1.2
    return y * env * 0.6 + flop
def whoosh(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 300, 3000); n /= np.abs(n).max() + 1e-9; return n * np.sin(np.pi * t / d) ** 2
# bed: faint morning room tone
room = band(rs.standard_normal(N), 150, 2500); room /= np.abs(room).max(); L += room * .004; R += np.roll(room, 991) * .004
# music-box lullaby (beat 0.5 s from 0.6 s); bass notes an octave+ below
mel = [72, 77, 76, 72, 74, 72, 69, None, 70, 74, 72, 70, 69, 72, 77, None]
for i, m in enumerate(mel):
    if m: add(mbox(m), 0.6 + i * 0.5, 0.075, 0.15 * np.sin(i))
for i, m in enumerate([53, 50, 46, 53]):
    add(mbox(m, 2.2, 0.6), 0.6 + i * 2.0, 0.05, -0.2); add(mbox(m + 7, 2.0, 0.5), 0.6 + i * 2.0 + 1.0, 0.03, -0.1)
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'bird':
        for j in range(2 + int(rs.random() * 2)): add(chirp(2600 + rs.random() * 600, 3800 + rs.random() * 800, 0.07), te + j * 0.11, 0.035, 0.5)
    elif k == 'wake':
        for j, m in enumerate([81, 84, 89]): add(mbox(m, 1.0, 0.5), te + j * 0.07, 0.035, 0.3)
    elif k == 'glint': add(ting(3136), te, 0.06, 0.4)
    elif k == 'step': add(pat(), te, 0.05, 0.1)
    elif k == 'pick': add(pop(), te, 0.12, 0.3)
    elif k == 'turn': add(swish(e['d']), te, 0.16, 0.25)
    elif k == 'toss': add(whoosh(0.35), te, 0.06, 0.3)
    elif k == 'pop': add(snap(), te, 0.18, 0.35); add(ting(2349), te + 0.01, 0.05, 0.35)
    elif k == 'happy':
        for j, m in enumerate([77, 81, 84]): add(mbox(m, 1.2, 0.6), te + j * 0.06, 0.04, 0.2)
    elif k == 'end':
        for j, m in enumerate([53, 60, 65, 69, 72, 77]): add(mbox(m, 2.4, 0.7), te + j * 0.09, 0.06 if m > 60 else 0.05, -0.3 + j * 0.12)
# master: fade in/out, soft limiter
fi = int(0.3 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.6) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
