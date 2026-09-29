# events.json → audio.wav (48 kHz stereo, 10 s)
# Web-toon sound kit, all synthesized: preloader blips + "loaded" ding, button pops and a mouse click, whooshes,
# a cartoon fall whistle, rubbery boings on every landing, sparkle chimes, chipmunk gibberish for the line,
# iris-out swish, and a jaunty 120 BPM chiptune-ish loop (oom-pah bass, offbeat chord plucks, square lead, claps).
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(107)
def add(sig, t, g=1.0, pan=0.0):
    i = int(round(t * SR)); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def sq(f, d, soft=5.0):  # soft square (less harsh than a naive one)
    t = tt(d); ph = 2 * np.pi * np.cumsum(np.broadcast_to(f, t.shape)) / SR; return np.tanh(soft * np.sin(ph))
def tri(f, d):
    t = tt(d); ph = np.cumsum(np.broadcast_to(f, t.shape)) / SR % 1; return 4 * np.abs(ph - .5) - 1
def adsr(d, a=.005, dec=.08, s=.5, r=.05):
    t = tt(d); e = np.where(t < a, t / a, s + (1 - s) * np.exp(-(t - a) / dec)); e *= np.clip((d - t) / r, 0, 1); return e
def blip(f=880, d=.06): return sq(f, d, 3) * adsr(d, .002, .02, .3, .02)
def ding():
    t = tt(1.0); return sum(a * np.sin(2 * np.pi * f * t) for f, a in [(1568, 1), (2352, .4), (3136, .2)]) * np.exp(-t / .25)
def pop(v=1):
    t = tt(.12); f = 380 + 900 * np.exp(-t * 40); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .03)
def click():
    t = tt(.05); n = band(rs.standard_normal(len(t)), 1500, 9000) * np.exp(-t / .004)
    return .8 * norm(n) + .5 * np.sin(2 * np.pi * 1900 * t) * np.exp(-t / .006)
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 300 + 3000 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
def fall(d):  # descending slide whistle
    t = tt(d); f = 1800 * (1 - .65 * t / d); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / .05) * np.minimum(1, (d - t) / .03)
def boing(v=1):
    t = tt(.45); f = 110 + 160 * v + 90 * np.sin(2 * np.pi * 11 * t) * np.exp(-t / .15)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + .35 * np.sin(2 * np.pi * np.cumsum(2 * f) / SR)
    thud = np.sin(2 * np.pi * np.cumsum(90 * np.exp(-t * 20) + 45) / SR) * np.exp(-t / .04)
    return (s * np.exp(-t / .16) * .7 + thud)
def sparkle():
    out = np.zeros(int(1.2 * SR))
    for i, m in enumerate([84, 88, 91, 96, 100, 103]):
        t = tt(.5); s = np.sin(2 * np.pi * nt(m) * t) * np.exp(-t / .12); j = int(i * .055 * SR); out[j:j + len(s)] += s[:len(out) - j]
    return out
def gibber(d):
    out = np.zeros(int(d * SR)); k = 0; t0 = 0.0
    while t0 < d - .06:
        dd = .05 + .05 * rs.random(); f0 = 480 + 360 * rs.random()
        t = tt(dd); f = f0 * (1 + .25 * np.sin(np.pi * t / dd)); s = sq(f, dd, 2.5) * np.sin(np.pi * t / dd) ** .6
        j = int(t0 * SR); out[j:j + len(s)] += s[:len(out) - j]; t0 += dd + .015 + .03 * (k % 3 == 2); k += 1
    return out
def iris():
    t = tt(.35); f = 900 * np.exp(-t * 5) + 200; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .12) * .6 + .4 * whoosh(.35)
def clap():
    t = tt(.15); n = norm(band(rs.standard_normal(len(t)), 900, 5000)); e = np.zeros_like(t)
    for o in (0, .008, .016): e += np.exp(-np.clip(t - o, 0, None) / .012) * (t >= o)
    return n * e * .6 + n * np.exp(-t / .05) * .4
def hat():
    t = tt(.04); return norm(band(rs.standard_normal(len(t)), 6000, 14000)) * np.exp(-t / .008)

def music(t0, beat):
    # 6 beats of loop, then the stab on beat 6 (the ta-da pose)
    e8 = beat / 2
    bass = [36, 43, 36, 43, 41, 43]
    chords = [[60, 64, 67], [60, 64, 67], [60, 64, 67], [59, 62, 67], [60, 65, 69], [59, 62, 67]]
    lead = [76, 79, 81, 79, 76, 72, 74, 76, 79, 77, 76, 74]
    for k in range(6):
        tb = t0 + k * beat
        add(tri(nt(bass[k]), beat * .9) * adsr(beat * .9, .004, .12, .55, .05), tb, .30)
        for i, m in enumerate(chords[k]): add(sq(nt(m), e8 * .7, 2) * adsr(e8 * .7, .003, .04, .2, .03), tb + e8, .045, (-.4, 0, .4)[i])
        if k % 2 == 1: add(clap(), tb, .22, .1)
        add(hat(), tb + e8, .05, -.3); add(hat(), tb, .03, -.3)
    for j, m in enumerate(lead):
        d = e8 * .85; add(sq(nt(m), d, 3) * adsr(d, .004, .06, .45, .03) * (1 + .0 * j), t0 + j * e8, .07, .15)
    ts = t0 + 6 * beat  # stab
    for i, m in enumerate([48, 60, 64, 67, 72, 76]):
        d = 1.1; add(sq(nt(m), d, 2.2) * adsr(d, .004, .25, .15, .4), ts, .06 if m > 50 else .18, (i - 2.5) * .12)
    add(clap(), ts, .25)

def jingle(t0):
    for i, m in enumerate([72, 76, 79, 84]):
        d = .5 if i < 3 else 1.0; add(sq(nt(m), d, 2.5) * adsr(d, .003, .1, .25, .3), t0 + i * .09, .06, (i - 1.5) * .2)
    add(tri(nt(48), 1.0) * adsr(1.0, .004, .3, .3, .4), t0 + .27, .2)

for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'blip': add(blip(700 + 500 * v), te, .12 * v)
    elif k == 'ding': add(ding(), te, .12)
    elif k == 'pop': add(pop(v), te, .28 * v, rs.uniform(-.3, .3))
    elif k == 'click': add(click(), te, .35)
    elif k == 'whoosh': add(whoosh(e['d']), te, .18)
    elif k == 'fall': add(fall(e['d']), te, .08)
    elif k == 'boing': add(boing(v), te, .32 * v + .08)
    elif k == 'sparkle': add(sparkle(), te, .06, .2)
    elif k == 'gibber': add(gibber(e['d']), te, .07)
    elif k in ('iris', 'iris2'): add(iris(), te, .2 if k == 'iris' else .14)
    elif k == 'music': music(te, e['beat'])
    elif k == 'jingle': jingle(te)
    elif k == 'ting': add(ding(), te, .07, .4); add(blip(2400, .04), te, .05, .4)
    elif k == 'hover': add(blip(1320, .05), te, .08)
# master: short fades, soft limiter
fi = int(0.05 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
