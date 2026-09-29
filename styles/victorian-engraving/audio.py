# events.json → audio.wav (48 kHz stereo, 10 s), fully synthesized
# a pompous little oom-pah march (tuba + off-beat band chords + piccolo), which stops dead before the stomp;
# rope creaks, card flips, a harrumph, a hinge squeak, wing flutters, the stomp + glass tinkle, crane ratchets,
# engine chuffs, a whistle, the cannon, a brass fanfare and a closing chord under the iris.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(23)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def nrm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def brass(f, d, att=.02, rel=.08, bright=1.0, vib=0.0):
    t = tt(d); ph = 2 * np.pi * np.cumsum(f * (1 + vib * np.sin(2 * np.pi * 5.5 * t))) / SR
    s = sum((1 / h) ** (1.3 / bright) * np.sin(h * ph) for h in range(1, 9))
    env = np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1); return s * env
def pluck(f, d=.18):
    t = tt(d); s = sum((.6 ** h) * np.sin(2 * np.pi * f * (h + 1) * t) for h in range(5)); return s * np.exp(-t / .06)
def noise(d, lo, hi): return nrm(band(rs.standard_normal(int(d * SR)), lo, hi))
def sweep(f0, f1, d, harm=4):
    t = tt(d); f = np.geomspace(f0, f1, len(t)); ph = 2 * np.pi * np.cumsum(f) / SR
    return sum(np.sin(h * ph) / h for h in range(1, harm + 1)) * np.sin(np.pi * t / d) ** .5
def thump(f0=110, d=.4, dec=.08):
    t = tt(d); f = f0 * np.exp(-t * 6) + f0 * .4; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / dec)
# ── the march (F major, 120 bpm), bars as root/fifth; stops before the stomp, resumes for the engine ──
beat = .5
prog = [(41, [53, 57, 60]), (36, [52, 55, 58]), (41, [53, 57, 60]), (36, [52, 55, 60])]
mel = [(0, 77, .25), (.5, 81, .25), (1, 84, .5), (2, 81, .25), (2.5, 79, .25), (3, 76, .5), (4, 77, .25), (4.5, 79, .25), (5, 81, .25), (5.5, 82, .25), (6, 84, .75)]
def march(t0, t1, g=1.0):
    k = 0; t = t0
    while t < t1 - .05:
        root, ch = prog[(k // 2) % 4]
        add(brass(nt(root if k % 2 == 0 else root + 7), .34, .015, .1, .7), t, .16 * g)
        for m in ch: add(pluck(nt(m)), t + beat / 2, .035 * g, (m - 55) / 20)
        t += beat; k += 1
    for (b, m, d) in mel:
        tm = t0 + .25 + b * beat
        if tm + d < t1: add(brass(nt(m), d * beat * 1.6, .01, .05, 1.6, .004), tm, .028 * g, .25)
march(0.45, 4.72)
march(6.3, 8.3, .8)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'rope': add(sweep(180, 140, .35, 6) * noise(.35, 300, 3000) * .5 + sweep(180, 140, .35, 6) * .3, te, .06, -.3)
    elif k == 'thud': add(thump(90, .4, .06), te, .5 * v); add(noise(.1, 200, 2500) * np.exp(-tt(.1) / .02), te, .12)
    elif k == 'whoosh':
        d = e['d']; n = noise(d, 300, 4000) * np.sin(np.pi * tt(d) / d) ** 2; add(n, te, .12)
    elif k == 'flip': add(noise(.12, 800, 6000) * np.exp(-tt(.12) / .03), te, .12); add(noise(.1, 800, 6000) * np.exp(-tt(.1) / .02), te + .12, .1)
    elif k == 'harrumph':
        add(brass(nt(38), .16, .02, .06, .5), te, .22); add(brass(nt(43), .22, .02, .1, .5, .01), te + .2, .26)
    elif k == 'rattle':
        for i in range(3): add(noise(.03, 1500, 7000) * np.exp(-tt(.03) / .006), te + i * .067, .2)
    elif k == 'hinge': add(sweep(620, 1100, .3, 3), te, .06, -.2); add(sweep(900, 700, .15, 3), te + .28, .04, -.2)
    elif k == 'pop': add(thump(520, .12, .02), te, .18, rs.uniform(-.4, .4))
    elif k == 'flutter':
        d = e['d']; t = tt(d); am = (np.sin(2 * np.pi * 7.5 * t) > 0) * np.exp(-t / d * .8)
        add(noise(d, 700, 5000) * am, te, .035, rs.uniform(-.5, .5))
    elif k == 'shimmer':
        for i, m in enumerate([84, 88, 91, 96, 100]):
            t = tt(1.2); add(np.sin(2 * np.pi * nt(m) * t) * np.exp(-t / .35), te + i * .07, .05, .3)
    elif k == 'descend':
        d = e['d']; t = tt(d); f = 60 + 40 * t / d; add(np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / d) ** 2 + noise(d, 60, 400) * (t / d) ** 2 * .6, te, .25)
    elif k == 'stomp':
        add(thump(70, 1.0, .22), te, 1.0); add(noise(.5, 40, 900) * np.exp(-tt(.5) / .09), te, .6)
        add(noise(.25, 1500, 8000) * np.exp(-tt(.25) / .03), te, .25)
    elif k == 'tinkle':
        for i in range(9):
            t = tt(.4); f = 2600 + rs.random() * 3000; add(np.sin(2 * np.pi * f * t) * np.exp(-t / .07), te + .03 + rs.random() * .3, .05, rs.uniform(-.6, .6))
    elif k == 'ratchet':
        d = e['d']; n = int(d * 22)
        for i in range(n): add(noise(.02, 2000, 7000) * np.exp(-tt(.02) / .004), te + i * d / n, .09, .2)
    elif k == 'clank': add(pluck(310, .4) + pluck(470, .4) * .6, te, .2 * v); add(noise(.08, 1500, 6000) * np.exp(-tt(.08) / .015), te, .15 * v)
    elif k == 'trolley':
        d = e['d']; t = tt(d); add(noise(d, 80, 700) * np.sin(np.pi * t / d) * (1 + .5 * np.sin(2 * np.pi * 9 * t)), te, .12, .3)
        for i in range(int(d * 8)): add(noise(.02, 1500, 5000) * np.exp(-tt(.02) / .005), te + i / 8, .06, .3)
    elif k == 'gulp': add(sweep(300, 90, .25, 2), te, .25); add(thump(160, .3, .05), te + .1, .3)
    elif k == 'chug':
        d = e['d']
        for i in range(int(d / .1)): add(noise(.09, 150, 2500) * np.exp(-tt(.09) / .025), te + i * .1, .2, .35); add(pluck(200 + (i % 2) * 60, .12), te + i * .1 + .05, .08, .35)
    elif k == 'whistle':
        t = tt(.35); add((np.sin(2 * np.pi * 1180 * t) + .5 * np.sin(2 * np.pi * 1400 * t)) * np.minimum(1, t / .03) * np.clip((.35 - t) / .1, 0, 1) + noise(.35, 1000, 3000) * .2, te, .07, .4)
    elif k == 'boom':
        add(thump(55, 1.4, .35), te, .9, .1); add(noise(1.0, 30, 1500) * np.exp(-tt(1.0) / .18), te, .7, .1)
        add(noise(.1, 2000, 9000) * np.exp(-tt(.1) / .01), te, .3)
    elif k == 'unfurl':
        t = tt(.35); add(noise(.35, 500, 6000) * (np.sin(2 * np.pi * 18 * t) > -.2) * np.sin(np.pi * t / .35), te, .14)
    elif k == 'fanfare':
        for i, (m, dt) in enumerate([(65, 0), (69, .09), (72, .18), (77, .3)]):
            add(brass(nt(m), .9 - dt, .02, .4, 1.4, .006), te + dt, .05, (i - 1.5) / 4)
        add(brass(nt(41), .9, .02, .4, .8), te + .3, .12)
    elif k == 'pip': add(thump(900, .08, .015), te, .1, .3)
    elif k == 'puff': add(noise(.3, 200, 3000) * np.exp(-tt(.3) / .08), te, .07, .4)
    elif k == 'close':
        for m in [53, 57, 60, 65]: add(brass(nt(m), .62, .06, .3, .9, .004), te, .04)
        add(brass(nt(29), .62, .06, .3, .6), te, .1)
fi = int(0.2 * SR); fo = int(0.35 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
