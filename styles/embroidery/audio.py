# events.json → audio.wav (48 kHz stereo, 10 s)
# thread drawn through cloth (soft filtered swishes), needle pricks, French-knot pops, tension-screw ratchet,
# fabric snapping taut, wooden hoop knocks, camera whooshes, a quiet music-box melody over a warm pad, closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(55)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def nz(x): return x / (np.abs(x).max() + 1e-9)
# pre-made noise banks (fast)
PULLS = [nz(band(rs.standard_normal(int(.5 * SR)), lo, hi)) for lo, hi in [(1400, 5200), (1800, 6500), (1100, 4200), (2200, 7500)]]
def pull(d):
    d = float(np.clip(d * .9, .05, .4)); t = tt(d); src = PULLS[rs.integers(4)]; o = rs.integers(0, len(src) - len(t))
    env = np.sin(np.pi * t / d) ** 1.6 * (1 + .5 * np.sin(2 * np.pi * 60 * t))
    prick = np.zeros_like(t); k = int(.004 * SR); prick[:k] = nz(band(rs.standard_normal(k * 4), 4000, 12000))[:k] * np.exp(-np.arange(k) / (k / 4))
    return src[o:o + len(t)] * env * .8 + prick * .5
def knot():
    t = tt(.09); f = 420 * np.exp(-t * 30) + 160; ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / .02) + .25 * nz(band(rs.standard_normal(len(t)), 2000, 8000)) * np.exp(-t / .004)
def click():
    t = tt(.03); return nz(band(rs.standard_normal(len(t)), 3000, 9000)) * np.exp(-t / .0025) + .4 * np.sin(2 * np.pi * 1850 * t) * np.exp(-t / .006)
def snap():
    t = tt(.35); return .9 * np.sin(2 * np.pi * 95 * t) * np.exp(-t / .05) + .7 * nz(band(rs.standard_normal(len(t)), 300, 4000)) * np.exp(-t / .03)
def knock(g=1.0):
    t = tt(.4); s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / dd) for f, a, dd in [(176, 1, .09), (410, .6, .05), (770, .35, .03), (1330, .2, .015)])
    return s * g + .3 * nz(band(rs.standard_normal(len(t)), 800, 5000)) * np.exp(-t / .006)
def rustle(d=.6):
    t = tt(d); n = nz(band(rs.standard_normal(len(t)), 700, 6000)); am = nz(np.abs(band(rs.standard_normal(len(t)), 4, 30)))
    return n * am * np.sin(np.pi * t / d) ** .8
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    a = np.exp(-2 * np.pi * (180 + 2200 * np.sin(np.pi * t / d) ** 2) / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return nz(y) * np.sin(np.pi * t / d) ** 1.5
def tone(freq, d, att=.4, rel=1.0, harm=((1, 1), (2, .25), (3, .08))):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in harm)
    return s * np.minimum(1, t / att) * np.minimum(1, np.maximum(0, (d - t) / rel))
def mbox(freq, d=1.6):   # music-box tine: bright partials, fast decay
    t = tt(d); return (np.sin(2 * np.pi * freq * t) + .35 * np.sin(2 * np.pi * freq * 3.9 * t) * np.exp(-t / .08) + .15 * np.sin(2 * np.pi * freq * 6.8 * t) * np.exp(-t / .03)) * np.exp(-t / .55) * np.minimum(1, t / .002)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR
room = nz(band(rs.standard_normal(N), 150, 2500)); L += room * .005; R += np.roll(room, 911) * .005
# pad: F major, gentle swell
for m, g, p in [(41, .05, -.3), (48, .03, .3), (53, .025, 0), (57, .018, .2)]:
    add(tone(nt(m), 9.4, 1.8, 1.4) * (1 + .12 * np.sin(2 * np.pi * .2 * tt(9.4))), .4, g, p)
# music-box melody (sparse, patient)
mel = [(0.9, 72), (1.5, 76), (2.1, 79), (2.7, 77), (3.3, 76), (3.9, 72), (4.5, 74), (5.7, 76), (6.3, 79), (6.9, 81), (7.5, 79), (8.1, 77), (8.7, 76), (9.05, 72)]
for tm, m in mel: add(mbox(nt(m)), tm, .05, rs.uniform(-.3, .3))
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'pull': add(pull(e['d']), te, .045 * e.get('v', 1), rs.uniform(-.35, .35))
    elif k == 'knot': add(knot(), te, .12, rs.uniform(-.3, .3))
    elif k == 'click': add(click(), te, .12, .25)
    elif k == 'snap': add(snap(), te, .35)
    elif k == 'lift': add(knock(.6), te, .25, -.2); add(rustle(.7), te + .05, .08, -.3)
    elif k == 'knock': add(knock(), te, .4, .1); add(rustle(.35), te, .06, .2)
    elif k == 'whoosh': add(whoosh(e['d']), te, .16)
    elif k == 'chord':
        for i, m in enumerate([53, 60, 65, 69, 72, 77]): add(tone(nt(m), 2.2, .06 + i * .03, 1.4), te + i * .05, .025)
        add(mbox(nt(84), 1.8), te + .3, .04)
fi = int(.3 * SR); fo = int(.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.tanh(np.stack([L, R], 1) * 1.5) * .8
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(st, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
