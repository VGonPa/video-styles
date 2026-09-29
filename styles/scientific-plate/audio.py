# events.json → audio.wav (48 kHz stereo, 10 s)
# study-room tone + a sparse plucked (harpsichord-like) motif; burin scratches while the specimens engrave,
# soft brush washes, pen-nib ticks, the reading glass sliding and chiming, the earthstar's creaking rays and
# spore puff, a page lifted and turned, a closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(14)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def nrm(x): return x / (np.abs(x).max() + 1e-9)
def pluck(f, d=2.2):
    n = int(d * SR); P = max(2, int(SR / f)); buf = list(rs.uniform(-1, 1, P)); out = np.zeros(n)
    for i in range(n):
        j = i % P; out[i] = buf[j]; buf[j] = 0.5 * (buf[j] + buf[(j + 1) % P]) * 0.9982
    body = np.sin(2 * np.pi * f * 2 * tt(d)) * np.exp(-tt(d) / .25) * .15      # a little quill "tick" brightness
    return (out + body) * np.exp(-np.arange(n) / SR / 0.9)
def burin(d):
    t = tt(d); n = nrm(band(rs.standard_normal(len(t)), 2600, 9000))
    gate = np.zeros(len(t)); i = 0
    while i < len(t):
        l = int(SR * rs.uniform(.05, .16)); g = int(SR * rs.uniform(.01, .05)); e = np.sin(np.pi * np.linspace(0, 1, min(l, len(t) - i))) ** 0.6
        gate[i:i + len(e)] = e * rs.uniform(.5, 1); i += l + g
    rough = 0.6 + 0.4 * np.abs(nrm(band(rs.standard_normal(len(t)), 20, 90)))
    return n * gate * rough
def wash(d):
    t = tt(d); n = nrm(band(rs.standard_normal(len(t)), 300, 2400)); env = np.sin(np.pi * t / d) ** 1.5
    wet = nrm(band(rs.standard_normal(len(t)), 60, 400)) * 0.4
    return (n + wet) * env
def nib():
    t = tt(.05); c = nrm(band(rs.standard_normal(len(t)), 2500, 8000)) * np.exp(-t / .004)
    return c + 0.4 * np.sin(2 * np.pi * 1400 * t) * np.exp(-t / .006)
def scratch(d):
    t = tt(d); n = nrm(band(rs.standard_normal(len(t)), 1800, 6500))
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** .5 * (0.55 + 0.45 * np.sin(2 * np.pi * 9 * t) ** 2)
    return n * env
def whoosh(d, lo=200, hi=2600):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = lo + (hi - lo) * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return nrm(y) * np.sin(np.pi * t / d) ** 1.5
def tink():
    t = tt(1.6); s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / dcy) for f, a, dcy in [(2793, 1, .5), (4186, .5, .35), (6272, .3, .2), (8372, .12, .12)])
    return s * np.minimum(1, t / .002)
def creak():
    t = tt(.12); f = 180 + 120 * rs.random(); s = np.sin(2 * np.pi * f * t) * np.exp(-t / .03)
    k = nrm(band(rs.standard_normal(len(t)), 1200, 5000)) * np.exp(-t / .01)
    return 0.6 * s + 0.5 * k
def puff():
    t = tt(1.2); n = nrm(band(rs.standard_normal(len(t)), 150, 1600)) * np.exp(-t / .22) * np.minimum(1, t / .02)
    sp = np.zeros(len(t))
    for _ in range(40):
        i = int(rs.uniform(.02, 1.0) * SR); l = 200
        if i + l < len(t): sp[i:i + l] += nrm(rs.standard_normal(l)) * np.exp(-np.arange(l) / 30) * rs.uniform(.1, .4)
    return n + band(sp, 3000, 12000) * 2
def rustle(d):
    t = tt(d); n = nrm(band(rs.standard_normal(len(t)), 700, 7000))
    am = np.abs(band(rs.standard_normal(len(t)), 4, 36)); am = am / (am.max() + 1e-9)
    return n * am * np.sin(np.pi * t / d) ** .7
def slap():
    t = tt(.35); n = nrm(band(rs.standard_normal(len(t)), 250, 4000)) * np.exp(-t / .04)
    return 0.8 * n + 0.5 * np.sin(2 * np.pi * 80 * t) * np.exp(-t / .05)
def thump():
    t = tt(.4); f = 120 * np.exp(-t * 10) + 60; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .07) + 0.2 * nrm(band(rs.standard_normal(len(t)), 300, 3000)) * np.exp(-t / .02)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR
# room tone: very soft, warm
room = nrm(band(rs.standard_normal(N), 90, 1800)); L += room * .005; R += np.roll(room, 911) * .005
# plucked motif (D major / Lydian colour), sparse and unhurried
motif = [(0.35, 62), (0.75, 69), (1.15, 74), (1.55, 73), (2.35, 66), (2.75, 69), (3.15, 71), (3.95, 74), (4.55, 76), (4.95, 78), (5.35, 81),
         (6.15, 74), (6.55, 71), (6.95, 69), (7.75, 66)]
for i, (tm, m) in enumerate(motif): add(pluck(nt(m), 2.2), tm, 0.05, (-.3, .3)[i % 2])
for tm, m in [(0.35, 38), (2.35, 43), (4.55, 40), (6.15, 45)]: add(pluck(nt(m), 2.6), tm, 0.06, 0)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'engrave': add(burin(e['d']), te, 0.035, rs.uniform(-.5, .5))
    elif k == 'wash': add(wash(e['d']), te, 0.05, rs.uniform(-.4, .4))
    elif k == 'nib': add(nib(), te, 0.12 * v, rs.uniform(-.3, .3))
    elif k == 'scratch': add(scratch(e['d']), te, 0.03)
    elif k == 'stamp': add(thump(), te, 0.3); add(rustle(.3), te, 0.04)
    elif k == 'slide': add(whoosh(e['d'], 300, 3500), te, 0.12, .3); add(rustle(e['d']), te, 0.03, .3)
    elif k == 'tink': add(tink(), te, 0.05, .1)
    elif k == 'creak': add(creak(), te, 0.07 * v, rs.uniform(-.4, .4))
    elif k == 'unfold': add(whoosh(e['d'], 100, 1400), te, 0.06)
    elif k == 'puff': add(puff(), te, 0.16)
    elif k == 'lift': add(rustle(.4), te, 0.08, .5)
    elif k == 'page': add(whoosh(e['d'], 150, 2200), te, 0.2, -.2); add(rustle(e['d']), te, 0.1, -.2)
    elif k == 'settle': add(slap(), te, 0.2)
    elif k == 'chord':
        for i, m in enumerate([50, 57, 62, 66, 69, 74]): add(pluck(nt(m), 2.4), te + i * 0.045, 0.045)
# master: fade in/out, soft limiter
fi = int(0.3 * SR); fo = int(0.8 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 3.8) * 0.82
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
