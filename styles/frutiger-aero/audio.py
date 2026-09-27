# events.json → audio.wav (48 kHz stereo, 10 s)
# cheerful 2006-era UI sound design: a bright major pad + glassy startup arpeggio, jelly "boings" for the icons,
# marimba plucks for the words, bubble bloops and pops, a water-drop plop + splash for the transition,
# messenger blips for the chat bubbles, a button click, shimmer on each sunbeam and a closing bell chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(33)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def bell(f, d=1.2, dec=0.35):
    t = tt(d); s = np.zeros_like(t)
    for h, a, k in [(1, 1, 1), (2.0, .3, 1.6), (3.0, .12, 2.4), (4.2, .06, 3.4)]:
        s += a * np.sin(2 * np.pi * f * h * t + h) * np.exp(-t * k / dec)
    return s * np.minimum(1, t / 0.003)
def marimba(f):
    t = tt(0.6); s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.16) + 0.35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t / 0.03)
    return s * np.minimum(1, t / 0.002)
def boing(f):
    t = tt(0.5); fm = f * (1 + 0.18 * np.exp(-t * 7) * np.sin(2 * np.pi * 11 * t)) * (1 + 0.5 * np.exp(-t * 30))
    ph = 2 * np.pi * np.cumsum(fm) / SR
    return (np.sin(ph) + 0.25 * np.sin(2 * ph)) * np.exp(-t / 0.16) * np.minimum(1, t / 0.003)
def bloop(f=520):
    t = tt(0.25); fr = f * (0.7 + 1.4 * (1 - np.exp(-t * 28))); ph = 2 * np.pi * np.cumsum(fr) / SR
    return np.sin(ph) * np.exp(-t / 0.06) * np.minimum(1, t / 0.003)
def pop():
    t = tt(0.06); fr = 1400 + 2600 * (1 - np.exp(-t * 90)); ph = 2 * np.pi * np.cumsum(fr) / SR
    return np.sin(ph) * np.exp(-t / 0.012) + 0.3 * norm(band(rs.standard_normal(len(t)), 3000, 10000)) * np.exp(-t / 0.003)
def whoosh(d, down=False):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    env = np.sin(np.pi * t / d) ** 1.4
    fc = (3200 - 2600 * t / d) if down else 250 + 3000 * env
    a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * env
def fall():
    t = tt(0.3); fr = 1800 - 1100 * t / 0.3; ph = 2 * np.pi * np.cumsum(fr) / SR
    return np.sin(ph) * np.sin(np.pi * t / 0.3) ** 2
def plop():
    t = tt(0.5); fr = 180 + 900 * (1 - np.exp(-t * 18)); ph = 2 * np.pi * np.cumsum(fr) / SR
    thump = np.sin(2 * np.pi * (70 + 90 * np.exp(-t * 25)) * t) * np.exp(-t / 0.08)
    return 0.8 * np.sin(ph) * np.exp(-t / 0.09) + 0.7 * thump
def splash():
    d = 0.9; t = tt(d); n = norm(band(rs.standard_normal(len(t)), 600, 9000)) * np.exp(-t / 0.18) * np.minimum(1, t / 0.004)
    s = n * 0.7
    for i in range(12):
        k = int(rs.uniform(0.05, 0.6) * SR); b = bloop(rs.uniform(900, 2600)); m = min(len(b), len(t) - k)
        s[k:k + m] += 0.25 * b[:m]
    return s
def shimmer():
    d = 1.1; t = tt(d); s = np.zeros_like(t)
    for i in range(16):
        f = 2400 + 3600 * rs.random(); t0 = rs.uniform(0, 0.7); k = int(t0 * SR)
        g = np.zeros_like(t); tl = t[:len(t) - k]; g[k:] = np.sin(2 * np.pi * f * tl) * np.exp(-tl / 0.12)
        s += g * rs.uniform(.3, 1)
    return s * np.sin(np.pi * t / d) ** .5
def swell(d):
    t = tt(d); f = 330 * 2 ** (t / d * 0.9); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + .3 * np.sin(2 * ph)) * np.sin(np.pi * t / d) ** 2
def tick(f):
    t = tt(0.08); return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.018) + 0.3 * np.sin(2 * np.pi * f * 2.7 * t) * np.exp(-t / 0.006)
def msg(f):
    s = np.zeros(int(0.35 * SR)); a = bell(f, 0.2, 0.08); b = bell(f * 1.5, 0.25, 0.1)
    s[:len(a)] += a; k = int(0.08 * SR); s[k:k + len(b)] += b[:len(s) - k]; return s
def click():
    t = tt(0.08)
    c = lambda: norm(band(rs.standard_normal(len(t)), 1500, 9000)) * np.exp(-t / 0.002) + 0.5 * np.sin(2 * np.pi * 1200 * t) * np.exp(-t / 0.012)
    s = c(); s2 = np.zeros_like(s); k = int(0.05 * SR); s2[k:] = c()[:len(s) - k] * 0.6
    return s + s2
def pad(freq, d, att, rel):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t + h) for h, a in [(1, 1), (2, .22), (3, .08), (4, .03)])
    s *= 1 + 0.15 * np.sin(2 * np.pi * 0.4 * t)
    return s * np.minimum(1, t / att) * np.minimum(1, np.maximum(d - t, 0) / rel)
# bed: bright pad, A section in C major, B section lifts to F → G → C
for m, g, p in [(48, .045, -.2), (55, .03, .25), (64, .02, -.3), (67, .016, .3), (71, .01, 0)]:
    add(pad(nt(m), 3.9, 1.0, 0.6), 0.0, g, p)
for (t0, d, chord) in [(3.6, 2.0, [53, 60, 65, 69, 72]), (5.5, 1.9, [55, 62, 67, 71, 74]), (7.3, 2.7, [48, 55, 64, 67, 72, 74])]:
    for i, m in enumerate(chord): add(pad(nt(m), d + .4, .35, .6), t0, [.045, .03, .02, .016, .012, .01][i], (i - 2) * .15)
air = norm(band(rs.standard_normal(N), 2500, 9000)); tA = np.arange(N) / SR
L += air * .003; R += np.roll(air, 1999) * .003
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'intro':
        for i, m in enumerate([72, 76, 79, 84, 88]): add(bell(nt(m), 1.6, .5), te + 0.08 + i * 0.07, 0.05, (i - 2) * .2)
    elif k == 'fall': add(fall(), te, 0.04 * v, rs.uniform(-.3, .3))
    elif k == 'boing': add(boing(e['f']), te, 0.2, (e['f'] - 500) / 400)
    elif k == 'pluck': add(marimba(e['f']), te, 0.16, (e['f'] - 980) / 500)
    elif k == 'shimmer': add(shimmer(), te, 0.04, .2)
    elif k == 'bloop': add(bloop(e['f']), te, 0.24, rs.uniform(-.3, .3))
    elif k == 'pop': add(pop(), te, 0.09 * v, rs.uniform(-.5, .5))
    elif k == 'whoosh': add(whoosh(e['d'], True), te, 0.12)
    elif k == 'plop': add(plop(), te, 0.38)
    elif k == 'splash': add(splash(), te, 0.2, 0)
    elif k == 'swell': add(swell(e['d']), te, 0.03, .3)
    elif k == 'tick': add(tick(e['f']), te, 0.07, -.3)
    elif k == 'msg': add(msg(e['f']), te, 0.13, .35)
    elif k == 'click': add(click(), te, 0.22, -.25)
    elif k == 'chord':
        for i, m in enumerate([72, 76, 79, 83, 86, 91]): add(bell(nt(m), 2.6, 0.9), te + i * 0.06, 0.05, (i - 2.5) * .15)
# master: fade in/out, soft limiter
fi = int(0.15 * SR); fo = int(0.8 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
