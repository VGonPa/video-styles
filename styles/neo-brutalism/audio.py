# events.json → audio.wav (48 kHz stereo, 10 s)
# punchy 120 BPM beat (kick / clap / hats, drops out under the wipe), UI pops, card thuds, button press/release
# clicks, check blips, confetti sparkle burst, whooshes, a bright success chime and a closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(28)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def nz(d, lo, hi): x = band(rs.standard_normal(int(d * SR)), lo, hi); return x / (np.abs(x).max() + 1e-9)
def sweep(f0, f1, d, k=30):
    t = tt(d); f = f1 + (f0 - f1) * np.exp(-t * k); return np.sin(2 * np.pi * np.cumsum(f) / SR), t
def pop(f=1.0):
    s, t = sweep(900 * f, 320 * f, .12, 40); return s * np.exp(-t / .035) + .25 * nz(.12, 2000, 8000) * np.exp(-t / .004)
def kick():
    s, t = sweep(170, 48, .35, 22); return s * np.exp(-t / .12) + .3 * nz(.35, 1000, 5000) * np.exp(-t / .003)
def clap():
    t = tt(.2); e = sum(np.exp(-np.clip(t - o, 0, None) / .006) * (t >= o) for o in (0, .011, .022)) + .6 * np.exp(-t / .05)
    return nz(.2, 900, 6000) * e * .6
def hat(open_=False):
    t = tt(.12); return nz(.12, 7000, 16000) * np.exp(-t / (.03 if open_ else .012))
def thud(v=1):
    s, t = sweep(140, 55, .3, 25); return (s * np.exp(-t / .07) + .5 * nz(.3, 200, 3000) * np.exp(-t / .02)) * v
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 300 + 3500 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y / (np.abs(y).max() + 1e-9) * np.sin(np.pi * t / d) ** 1.5
def swipe(d):
    t = tt(d); return nz(d, 1500, 9000) * np.sin(np.pi * t / d) ** 2 * np.linspace(.4, 1, len(t))
def boing():
    t = tt(.45); f = 260 + 380 * t / .45 + 40 * np.sin(2 * np.pi * 14 * t) * np.exp(-t / .2)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .16)
def click(f=1.0):
    t = tt(.05); return nz(.05, 2500 * f, 10000) * np.exp(-t / .0025) + .5 * np.sin(2 * np.pi * 1800 * f * t) * np.exp(-t / .006)
def press(v=1):
    s, t = sweep(220, 70, .22, 30); return s * np.exp(-t / .05) * v
def tone(freq, d, att=.005, dec=.3, harm=((1, 1), (2, .25), (3, .08))):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in harm); return s * np.minimum(1, t / att) * np.exp(-t / dec)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)

# ── beat: 120 BPM, starts at 0, silent under the wipe (6.25–6.8), ends with the brake ──
BPM = 120; beat = 60 / BPM
for b in range(int(9.2 / beat) + 1):
    tb = b * beat
    if 6.2 <= tb < 6.8 or tb > 9.1: continue
    add(kick(), tb, .5)
    if b % 2 == 1: add(clap(), tb, .28, .1)
    add(hat(), tb + beat / 2, .10, -.3)
    if b % 4 == 3: add(hat(True), tb + beat * .75, .07, .3)
# bass: short plucky root notes on the offbeats (C major-ish, bright)
roots = [36, 36, 41, 43]
for b in range(int(9.0 / beat)):
    tb = b * beat + beat / 2
    if 6.2 <= tb < 6.8: continue
    m = roots[(b // 4) % 4]; add(tone(nt(m), .25, .004, .09, ((1, 1), (2, .5), (3, .2))), tb, .12)

for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'pop': add(pop(e.get('f', 1)), te, .32 * v, rs.uniform(-.3, .3))
    elif k == 'swipe': add(swipe(e['d']), te, .10, .2)
    elif k == 'whoosh': add(whoosh(e['d']), te, .30)
    elif k == 'thud': add(thud(), te, .45 * v, rs.uniform(-.2, .2))
    elif k == 'boing': add(boing(), te, .16, .3)
    elif k == 'tick': add(click(1.2), te, .12)
    elif k == 'press': add(press(), te, .5 * v); add(click(.7), te, .3 * v)
    elif k == 'release': add(click(1.1), te, .25 * v); add(pop(1.6), te + .02, .15 * v)
    elif k == 'check': add(tone(nt(76 + [0, 2, 4, 7][e['f']]), .25, .002, .08, ((1, 1), (2, .3))), te, .13); add(click(1.3), te, .08)
    elif k == 'confetti':
        for i in range(26): add(tone(nt(84 + int(rs.integers(0, 12))), .12, .002, .03), te + rs.uniform(0, .6) ** 1.6, .045, rs.uniform(-.8, .8))
        add(nz(.5, 3000, 12000) * np.exp(-tt(.5) / .15), te, .06)
    elif k == 'chime':
        for i, m in enumerate([72, 76, 79, 84]): add(tone(nt(m), .8, .003, .35), te + i * .06, .09)
    elif k == 'chord':
        for i, m in enumerate([60, 64, 67, 72, 76]): add(tone(nt(m), 2.6, .01 + i * .01, 1.1), te + i * .025, .05)
        add(tone(nt(36), 2.6, .01, 1.0), te, .12)
    elif k == 'brake':
        s, t = sweep(400, 90, .7, 5); add(s * np.exp(-t / .3) * .5 + swipe(.7) * .5, te, .08)
    elif k == 'outro':
        for i, m in enumerate([60, 67, 72, 76, 79]): add(tone(nt(m), 1.3, .03, .6), te + i * .05, .045)

fi = int(.02 * SR); fo = int(.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * .85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
