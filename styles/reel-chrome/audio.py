# events.json → audio.wav (48 kHz stereo, 9.6 s)
# A low bed (additive saw stacks whose brightness opens with the shot) swells under the title card, ducks at the
# first cut and carries the reel; a sub thump lands on each cut; an air sweep follows the white bar across the
# stereo field; soft tile clicks as the blocks land; a servo rise while the hairlines converge; a bright ping
# (D6 / A6 / D7, echoed left and right) when the reticle locks. Everything is synthesised, nothing is sampled.
import json, wave, numpy as np
SR, DUR = 48000, 9.6
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(129)
def add(sig, t, g=1.0, pan=0.0):
    i = int(round(t * SR)); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        pan = np.clip(pan, -1, 1)
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
norm = lambda x: x / (np.abs(x).max() + 1e-9)
def lowpass(x, fc):
    """One-pole lowpass with a per-sample cutoff."""
    fc = np.broadcast_to(fc, x.shape); a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); p = 0.0
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))

# ── the bed: three chords, each an additive saw stack whose harmonics open with `bright` ──
T = np.arange(N) / SR
T_CUT1, T_CUT2, T_LOCK = 3.2, 6.15, 8.3
level = np.interp(T, [0, .15, 2.9, 3.19, 3.24, 3.9, 6.1, 6.2, 8.2, 8.4, 9.0, 9.6], [0, .05, 1, 1, .42, .6, .6, .5, .66, .72, .5, 0])
bright = np.interp(T, [0, 2.9, 3.2, 6.1, 8.3, 9.6], [1.5, 7.5, 5, 6, 9, 4])
CHORDS = [(0, T_CUT2 + .25, [38, 45, 52, 54, 57]),            # Dadd9 under the title and the sphere
          (T_CUT2 - .1, T_LOCK + .2, [43, 50, 54, 57, 59]),    # Gmaj9 lifts into the drafting field
          (T_LOCK - .05, DUR, [38, 45, 50, 54, 57, 64])]       # resolves to D on the lock
bed = np.zeros(N)
for t0, t1, notes in CHORDS:
    win = np.clip(np.minimum((T - t0) / .25, (t1 - T) / .25), 0, 1)
    for m in notes:
        for det in (-.0025, .0025):
            f = nt(m) * (1 + det); ph = rs.uniform(0, 2 * np.pi)
            for h in range(1, 15):
                if f * h > 9000: break
                bed += win * np.sin(2 * np.pi * f * h * T + ph * h) / h * np.exp(-(h - 1) / bright)
bed = bed / (np.abs(bed).max() + 1e-9) * level * (1 + .06 * np.sin(2 * np.pi * .7 * T))
add(bed, 0, .3)
# slow stereo width: a lightly delayed copy on the right
add(np.concatenate([np.zeros(int(.012 * SR)), bed])[:N] * .5, 0, .12, .8)

# ── sounds ──
def thump():
    t = tt(.7); f = 32 + 85 * np.exp(-t * 22)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .3) * np.minimum(1, t / .002)
    click = np.zeros_like(t); k = int(.004 * SR); click[:k] = np.diff(rs.standard_normal(k + 1)) * np.exp(-np.arange(k) / (k / 4))
    return np.tanh((body + .15 * click) * 1.6)
def tick():
    k = int(.0016 * SR); return np.diff(rs.standard_normal(k + 1)) * np.exp(-np.arange(k) / (k / 3))
def riser(d):
    t = tt(d); u = t / d; x = rs.standard_normal(len(t))
    return norm(lowpass(x, 300 + 5200 * u ** 2)) * u ** 2.2 * np.minimum(1, (d - t) / .02)
def sweep(d, pan):
    t = tt(d); pts = np.array(pan)
    p = np.interp(t, pts[:, 0] - pts[0, 0], pts[:, 1]); speed = np.abs(np.gradient(p)) * SR
    env = np.clip(speed / speed.max(), 0, 1) ** .8 * np.minimum(1, t / .05) * np.minimum(1, (d - t) / .1)
    x = norm(lowpass(rs.standard_normal(len(t)), 900 + 5500 * env)) * env
    return x, p
def shimmer():
    t = tt(1.4); env = np.minimum(1, t / .06) * np.exp(-t / .45)
    s = sum(np.sin(2 * np.pi * nt(m) * t + i) for i, m in enumerate([100, 105, 112])) / 3
    return s * env + .3 * norm(band(rs.standard_normal(len(t)), 7000, 14000)) * env * np.exp(-t / .2)
def glint():
    t = tt(.9); env = np.sin(np.pi * t / .9) ** 2
    return .7 * norm(band(rs.standard_normal(len(t)), 5000, 12000)) * env + .3 * np.sin(2 * np.pi * nt(108) * t) * env
def wipe(d):
    t = tt(d); u = t / d; env = np.sin(np.pi * u) ** 1.2
    return norm(lowpass(rs.standard_normal(len(t)), 5200 - 4300 * u)) * env
def block(f, v):
    t = tt(.12); ff = 700 * f
    tok = np.sin(2 * np.pi * ff * t) * np.exp(-t / .028) + .5 * np.sin(2 * np.pi * ff * 2.71 * t) * np.exp(-t / .012)
    thud = np.sin(2 * np.pi * (110 + 60 * np.exp(-t * 40)) * t) * np.exp(-t / .045)
    k = int(.002 * SR); click = np.zeros_like(t); click[:k] = np.diff(rs.standard_normal(k + 1)) * np.exp(-np.arange(k) / (k / 3))
    return (tok * .6 + thud * .5 * v + click * .25) * np.minimum(1, t / .0008)
def servo(d):
    t = tt(d); u = t / d; f = 220 * 2 ** (u * 1.0)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 + .35 * np.sin(2 * np.pi * 31 * t)) * .5
    air = norm(lowpass(rs.standard_normal(len(t)), 600 + 2400 * u)) * .5
    return (s + air) * np.minimum(1, t / .15) * u ** 1.4 * np.minimum(1, (d - t) / .015)
def ping():
    t = tt(2.6); out = np.zeros_like(t)
    for m, a in [(86, 1), (93, .55), (98, .45)]:
        f = nt(m)
        out += a * (np.sin(2 * np.pi * f * t) * np.exp(-t / 1.1) + .18 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / .25))
    return out * np.minimum(1, t / .002)

for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'thump': add(thump(), te, .6)
    elif k == 'ticks':
        s = te
        while s < te + e['d']: add(tick(), s, .07, rs.uniform(-.5, .5)); s += rs.uniform(.03, .06)
    elif k == 'riser': add(riser(e['d']), te, .22)
    elif k == 'sweep':
        x, p = sweep(e['d'], e['pan']); i = int(te * SR); n = min(len(x), N - i)
        L[i:i + n] += x[:n] * .3 * np.sqrt(.5 - p[:n] / 2) * 1.414; R[i:i + n] += x[:n] * .3 * np.sqrt(.5 + p[:n] / 2) * 1.414
    elif k == 'shimmer': add(shimmer(), te - .1, .06, .1)
    elif k == 'glint': add(glint(), te, .08, .2)
    elif k == 'wipe': add(wipe(e['d']), te, .22)
    elif k == 'block': add(block(e['f'], e['v']), te, .14 * e['v'], e['p'] * .7)
    elif k == 'servo': add(servo(e['d']), te, .07, -.1)
    elif k == 'lock':
        pg = ping(); add(pg, te, .2); add(pg, te + .19, .08, .7); add(pg, te + .38, .045, -.7); add(thump(), te, .22)
    elif k == 'swell': pass                       # the swell is the bed's level curve above

# master: short fade in, fade out with the picture, soft limiter
fi = int(0.02 * SR); fo = int(0.55 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.25) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
