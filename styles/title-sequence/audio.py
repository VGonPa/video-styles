# events.json → audio.wav (48 kHz stereo, 10 s)
# 120 BPM cool-jazz title cue, all synthesized: plucked walking bass, swung ride cymbal, finger snaps on 2 & 4,
# muted brass stabs, bongos under the staircase, plus paper foley (bar slams, letter snips, strip rip, whooshes).
# The band drops out for the keyhole "break" (7.0–7.5 s) and hits back on the figure/ground flip.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(111)
BEAT = 0.5
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def lp1(x, fc):
    a = np.exp(-2 * np.pi * np.asarray(fc, float) / SR) * np.ones(len(x)); y = np.zeros_like(x); p = 0.0
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y
# ── band ──
def bass(m, d=0.48):
    f = nt(m); t = tt(d); s = np.sin(2 * np.pi * f * t) + .5 * np.sin(4 * np.pi * f * t) * np.exp(-t / .05) + .2 * np.sin(6 * np.pi * f * t) * np.exp(-t / .03)
    thump = band(rs.standard_normal(len(t)), 60, 900) * np.exp(-t / .008)
    return (s * np.exp(-t / .22) * np.minimum(1, (d - t) / .03) + .25 * norm(thump))
def ride(acc=1.0):
    t = tt(0.9); n = band(rs.standard_normal(len(t)), 5000, 14000)
    bell = sum(np.sin(2 * np.pi * f * t) for f in (3150, 4270, 5890)) * .08
    return (norm(n) * .8 + bell) * np.exp(-t / (.16 + .1 * acc))
def snap():
    t = tt(0.08); n = band(rs.standard_normal(len(t)), 1200, 6000); return norm(n) * np.exp(-t / .012)
def bongo(f):
    t = tt(0.3); fr = f * (1 + .5 * np.exp(-t / .01)); s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / .09)
    return s + .3 * norm(band(rs.standard_normal(len(t)), 1500, 5000)) * np.exp(-t / .004)
def brass(ms, d=0.9, bright=1.0):
    t = tt(d); s = np.zeros(len(t))
    for m in ms:
        f = nt(m) * (1 + .002 * rs.standard_normal()); ph = 2 * np.pi * f * t + rs.random() * 6
        s += sum(np.sin(k * ph) / k * (1 if k < 4 else .6) for k in range(1, 12))
    env = np.minimum(1, t / .012) * (np.exp(-t / .12) * .7 + .3 * np.exp(-t / (d * .5))) * np.minimum(1, (d - t) / .08)
    fc = 500 + 3500 * bright * np.exp(-t / .09)
    return norm(lp1(s * env, fc))
# ── paper foley ──
def slam():
    t = tt(0.3); n = band(rs.standard_normal(len(t)), 250, 4500) * np.exp(-t / .03)
    return .8 * norm(n) + .7 * np.sin(2 * np.pi * (70 + 60 * np.exp(-t / .02)) * t) * np.exp(-t / .07)
def snip():
    t = tt(0.05); return norm(band(rs.standard_normal(len(t)), 2500, 9000)) * np.exp(-t / .006)
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); fc = 250 + 2400 * np.sin(np.pi * t / d) ** 2
    return norm(lp1(x, fc)) * np.sin(np.pi * t / d) ** 1.5
def rip(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 700, 6000); am = np.abs(band(rs.standard_normal(len(t)), 20, 120)); am = norm(am)
    return norm(n) * am * np.minimum(1, t / .02) * np.minimum(1, (d - t) / .05)

ev = json.load(open('events.json'))
BREAK = (7.0, 7.5); END = 9.8
walk = [38, 41, 43, 44, 45, 48, 47, 46, 45, 41, 40, 39, 38, 41, 43, 45, 46, 45, 44, 38]
for b in range(20):
    tb = b * BEAT
    if tb < 0.2 or tb >= END or BREAK[0] <= tb < BREAK[1]: continue
    add(bass(walk[b]), tb, 0.34, -.15)
    add(ride(1.0 if b % 2 == 0 else .6), tb, 0.05, .35)                    # ride on the beat …
    if tb + BEAT * 2 / 3 < BREAK[0] or tb >= BREAK[1]: add(ride(.4), tb + BEAT * 2 / 3, 0.03, .35)   # … and the swung "and"
    if b % 2 == 1: add(snap(), tb, 0.16, -.4)
bongo_f = [196, 220, 247, 262, 294, 330, 392]
for e in ev:
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'slam': add(slam(), te, 0.42 * v, rs.uniform(-.2, .2)); add(brass([50, 57], .25, .6), te, 0.05 * v)
    elif k == 'snip': add(snip(), te + rs.uniform(0, .006), 0.07, rs.uniform(-.3, .3))
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.16, rs.uniform(-.3, .3))
    elif k == 'rip': add(rip(e['d']), te, 0.16, -.3)
    elif k == 'bongo': add(bongo(bongo_f[int(v)]), te, 0.3, -.3 + .1 * v)
    elif k == 'stab':
        if v >= 1:   # title: full minor-9 stab, bass octave and a crash that rings under the title card
            add(brass([50, 53, 57, 60, 64], 1.4, 1.0), te, 0.2); add(bass(26, 1.6), te, 0.4); add(ride(3.0), te, 0.07)
        else: add(brass([49, 52, 56, 59], .6, .8), te, 0.16); add(bass(37, .5), te, 0.3)
# brass punctuation on the credits
for tb, ch in [(1.0, [53, 57, 60]), (2.3, [50, 53, 57, 62]), (4.25, [52, 55, 58]), (6.45, [50, 55, 58, 62])]:
    add(brass(ch, .35, .7), tb, 0.09)
# last bass note + cymbal tail after the shutters close
add(bass(26, 1.2), END - .05, 0.3); add(ride(2.5), END - .05, 0.05)
fi = int(0.15 * SR); fo = int(0.35 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
