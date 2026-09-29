# events.json → audio.wav (48 kHz stereo, 10 s)
# A dry, plucked chamber bed (pizzicato + harpsichord-like plucks, all Karplus-Strong), with precise foley:
# a soft air pan, dollhouse hinge creak + thud, light-switch clicks, whip-pan swishes, a desk-bell ding,
# a ceiling drip, umbrella pops, water tinks, a snap-zoom whoosh and a closing plucked chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(112)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def pluck(f, d=0.8, damp=0.996, bright=0.5):
    n = int(d * SR); P = max(2, int(SR / f)); buf = rs.uniform(-1, 1, P) * bright + (1 - bright) * np.sin(np.linspace(0, 2 * np.pi, P))
    out = np.zeros(n); j = 0
    for i in range(n):
        out[i] = buf[j]; nx = (j + 1) % P; buf[j] = 0.5 * (buf[j] + buf[nx]) * damp; j = nx
    return out * np.minimum(1, np.arange(n) / (0.002 * SR))
def whoosh(d, lo=200, hi=2600):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = lo + hi * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
def click():
    t = tt(0.04); n = band(rs.standard_normal(len(t)), 2000, 9000) * np.exp(-t / 0.002)
    return norm(n) + 0.4 * np.sin(2 * np.pi * 900 * t) * np.exp(-t / 0.006)
def creak(d):
    t = tt(d); f = 180 + 60 * np.sin(2 * np.pi * 1.3 * t) + 25 * rs.standard_normal(len(t)).cumsum() / SR * 30
    ph = 2 * np.pi * np.cumsum(f) / SR
    pulses = (np.sin(2 * np.pi * 38 * t) > 0.6).astype(float)
    s = (np.sign(np.sin(ph)) * 0.4 + np.sin(ph * 2)) * (0.4 + 0.6 * pulses)
    return band(s, 200, 3000) * np.sin(np.pi * t / d) ** 0.8
def thud():
    t = tt(0.3); f = 120 * np.exp(-t * 10) + 55
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.06) + 0.3 * norm(band(rs.standard_normal(len(t)), 200, 2000)) * np.exp(-t / 0.02)
def ding(f=1560):
    t = tt(2.0)
    return sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / dd) for m, a, dd in [(1, 1, .9), (2.76, .35, .35), (5.4, .15, .15), (0.5, .12, .6)])
def pop():
    t = tt(0.18); n = band(rs.standard_normal(len(t)), 150, 3500) * np.exp(-t / 0.018)
    thump = np.sin(2 * np.pi * (90 + 200 * np.exp(-t * 40)) * t) * np.exp(-t / 0.03)
    return 0.7 * norm(n) + thump
def tink(f=2600):
    t = tt(0.35); fr = f * (1 + 0.25 * np.exp(-t * 60))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.06) + 0.3 * np.sin(2 * np.pi * f * 2.1 * t) * np.exp(-t / 0.02)
def drip():
    t = tt(0.25); fr = 700 + 1400 * t / 0.25
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-((t - 0.05) / 0.05) ** 2) * 0.6
nt = lambda m: 440 * 2 ** ((m - 69) / 12)

# ── music bed: a jaunty plucked tune in D major, 132 bpm eighths, dry and small ──
beat = 60 / 132 / 2
mel = [74, None, 78, 81, 78, None, 74, None, 76, None, 79, 83, 79, None, 76, None,
       74, 78, 81, 86, 85, None, 81, None, 83, 81, 79, 78, 76, None, 73, None]
bass = [50, 57, 50, 57, 52, 59, 52, 59, 50, 57, 50, 57, 45, 52, 45, 52]
t0 = 0.25
for i in range(34):
    t = t0 + i * beat
    if t > 3.95: break
    m = mel[i % len(mel)]
    if m: add(pluck(nt(m), 0.5, 0.993, 0.7), t, 0.07, 0.25)
    if i % 2 == 0: add(pluck(nt(bass[(i // 2) % len(bass)]), 0.7, 0.995, 0.4), t, 0.08, -0.2)
# card: a held, polite pause (harpsichord arpeggio)
for i, m in enumerate([62, 66, 69, 74, 78]): add(pluck(nt(m), 1.2, 0.997, 0.9), 4.3 + i * 0.06, 0.05, -0.3 + i * 0.15)
# lobby: sparse pizzicato ticks that stop dead for the drip, then resume
for i, m in enumerate([62, None, 69, None, 66, None]):
    if m: add(pluck(nt(m), 0.4, 0.99, 0.6), 5.82 + i * beat, 0.06, 0.1)
for i in range(8):
    t = 7.3 + i * beat
    m = [74, 78, 76, 73, 74, 78, 81, 79][i]
    add(pluck(nt(m), 0.45, 0.992, 0.7), t, 0.06, 0.25)
    if i % 2 == 0: add(pluck(nt([50, 45, 50, 45][i // 2]), 0.6, 0.995, 0.4), t, 0.07, -0.2)
# room tone
room = band(rs.standard_normal(N), 150, 2500); room = norm(room); L += room * .004; R += np.roll(room, 911) * .004

for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'pan': add(whoosh(e['d'], 100, 700), te, 0.05, -0.4)
    elif k == 'creak': add(creak(e['d']), te, 0.05, -0.6); add(creak(e['d']), te + 0.03, 0.05, 0.6)
    elif k == 'thud': add(thud(), te, 0.35)
    elif k == 'click': add(click(), te, 0.25, rs.uniform(-.3, .3))
    elif k == 'whip': add(whoosh(e['d'] + 0.1, 300, 5000), te - 0.05, 0.35, 0.0)
    elif k == 'ding': add(ding(), te, 0.07)
    elif k == 'pop': add(pop(), te, 0.35 * v, rs.uniform(-.25, .25))
    elif k == 'drip': add(drip(), te + 0.45, 0.08)
    elif k == 'swish': add(whoosh(0.22, 400, 3000), te, 0.08, 0.3)
    elif k == 'tink': add(tink(2400 + 500 * rs.random()), te, 0.12 * v, rs.uniform(-.4, .4))
    elif k == 'zoom': add(whoosh(e['d'] + 0.1, 150, 1800), te, 0.25)
    elif k == 'chord':
        for i, m in enumerate([50, 62, 66, 69, 74, 78]): add(pluck(nt(m), 1.6, 0.998, 0.8), te + i * 0.05, 0.07, -0.4 + i * 0.16)
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.6) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
