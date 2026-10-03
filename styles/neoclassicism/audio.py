# events.json → audio.wav (48 kHz stereo, 9.6 s)
# Civic calm: a bowed-string and flue-pipe pad walks a plain cadence (I in the portico, IV in the relief,
# V7 in the frieze, home to I at the end). Stone tocks land with the steps, the columns (panned where
# they stand) and the entablature; the pediment shuts with a drier clack; a chisel taps each letter.
# Laurel leaves rustle and glint, a stylus whispers while the contour drawings appear, the mouldings
# slide in on stone, the relief rises on a low warm swell under an airy raking sweep, the wreath lifts on
# a breath of air and a rising chime, and each emblem settles with a muted knock and a bell.
# The pad, the stone hits and the rest are built as separate stems: the hits sit about 6 dB over the
# pad, everything goes through a synthetic hall, and the mix is set to -14 LUFS (BS.1770) with peaks
# held under -1.5 dBFS. It fades out with the picture.
import json, wave, numpy as np

SR, DUR = 48000, 9.6
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(139)
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
PAD, HITS, FX = (np.zeros((2, N)) for _ in range(3))


def seg(d):
    return np.arange(int(d * SR)) / SR


def place(stem, x, at, gain=1.0, pan=0.0):
    i0 = int(round(at * SR))
    if i0 >= N:
        return
    if i0 < 0:
        x, i0 = x[-i0:], 0
    n = min(len(x), N - i0)
    a = (np.clip(pan, -1, 1) + 1) * np.pi / 4      # equal-power pan
    stem[0, i0:i0 + n] += x[:n] * gain * np.cos(a)
    stem[1, i0:i0 + n] += x[:n] * gain * np.sin(a)


def bandpass(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def peak(x):
    return x / (np.max(np.abs(x)) + 1e-12)


def one_pole(x, cutoff):
    # time-varying one-pole low-pass; cutoff may be an array
    c = np.broadcast_to(np.asarray(cutoff, float), x.shape)
    k = 1 - np.exp(-2 * np.pi * c / SR)
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += k[i] * (x[i] - acc); y[i] = acc
    return y


ev = json.load(open('events.json'))
of = lambda kind: [e for e in ev if e['k'] == kind]

# ── the pad: four chords, each voice a soft bowed tone plus a quiet flue pipe an octave up ──
CHORDS = [[41, 53, 57, 60, 65],          # I   F
          [46, 53, 58, 62, 65],          # IV  B-flat
          [48, 52, 58, 60, 64],          # V7  C
          [41, 53, 57, 60, 65, 69]]      # I   F, with the third on top
LEVEL = [0.72, 0.85, 0.9, 1.35]          # the pad grows a little through the film; the cadence speaks up
pads = sorted(of('pad'), key=lambda e: e['t'])
end = of('end')[0]
fade_t, fade_d = end['t'], end['d']


def bowed(f0, seed):
    r = np.random.default_rng(seed)
    vib = 1 + 0.0028 * np.sin(2 * np.pi * (4.6 + 0.5 * r.random()) * t + r.random() * 6)
    drift = 1 + 0.0012 * np.sin(2 * np.pi * 0.21 * t + r.random() * 6)
    ph = 2 * np.pi * np.cumsum(f0 * vib * drift) / SR
    out = np.zeros(N)
    for h in range(1, 14):
        if f0 * h > 5000:
            break
        out += np.sin(h * ph + r.random() * 6) * (1 / h) * np.exp(-h / 5.5)
    pipe = 0.35 * np.sin(2 * ph + 1.3) + 0.12 * np.sin(4 * ph + 0.4)
    return out + pipe


for i, e in enumerate(pads):
    t0 = e['t']; t1 = pads[i + 1]['t'] if i + 1 < len(pads) else DUR
    a_in = 0.9 if i == 0 else 0.4
    env = np.clip((t - t0 + (0 if i == 0 else 0.12)) / a_in, 0, 1) ** 1.6
    if i + 1 < len(pads):
        env *= 1 - np.clip((t - t1 + 0.1) / 0.45, 0, 1)
    if i == 0:
        env *= 0.6 + 0.4 * np.clip((t - 0.8) / 2.0, 0, 1)
    notes = CHORDS[e['c']]
    for j, m in enumerate(notes):
        v = bowed(hz(m), 31 * i + j) * env * (1.0 if m < 50 else 0.62) * LEVEL[i]
        p = (j / (len(notes) - 1) - 0.5) * 0.7
        PAD[0] += v * np.cos((p + 1) * np.pi / 4); PAD[1] += v * np.sin((p + 1) * np.pi / 4)


# ── stone ──
def tock(v):
    d = seg(0.6)
    f = 62 + 70 * np.exp(-d / 0.025)                  # the thud drops in pitch as it lands
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-d / (0.11 + 0.05 * v))
    knock = sum(a * np.sin(2 * np.pi * fr * d + rng.random() * 6) * np.exp(-d / dc)
                for fr, a, dc in [(205, 0.5, 0.05), (348, 0.35, 0.035), (560, 0.22, 0.022), (910, 0.12, 0.014)])
    grit = peak(bandpass(rng.standard_normal(len(d)), 700, 6000)) * np.exp(-d / 0.03)
    crumbs = np.zeros(len(d))
    for c in rng.uniform(0.01, 0.12, 6):
        i = int(c * SR); k = np.arange(min(200, len(d) - i))
        crumbs[i:i + len(k)] += rng.choice([-1, 1]) * np.exp(-k / 18) * rng.uniform(0.2, 0.6)
    return (body * 1.0 + knock * 0.55 + grit * 0.22 + crumbs * 0.12) * np.minimum(1, d / 0.0012)


def clack():
    d = seg(0.5)
    knock = sum(a * np.sin(2 * np.pi * fr * d + rng.random() * 6) * np.exp(-d / dc)
                for fr, a, dc in [(410, 0.6, 0.045), (690, 0.45, 0.03), (1130, 0.3, 0.02), (1720, 0.18, 0.012)])
    low = np.sin(2 * np.pi * 95 * d) * np.exp(-d / 0.09)
    grit = peak(bandpass(rng.standard_normal(len(d)), 1500, 9000)) * np.exp(-d / 0.02)
    return (knock + 0.6 * low + 0.25 * grit) * np.minimum(1, d / 0.0008)


def chisel():
    d = seg(0.22)
    ring = sum(a * np.sin(2 * np.pi * fr * d + rng.random() * 6) * np.exp(-d / dc)
               for fr, a, dc in [(2730, 0.5, 0.05), (4120, 0.35, 0.035), (5960, 0.22, 0.02)])
    tick = peak(bandpass(rng.standard_normal(len(d)), 3000, 12000)) * np.exp(-d / 0.004)
    chip = peak(bandpass(rng.standard_normal(len(d)), 900, 5000)) * np.exp(-d / 0.018)
    return ring * 0.5 + tick * 0.6 + chip * 0.25


onsets = []                                            # where the hits are, for the balance below
for e in of('tock'):
    place(HITS, peak(tock(e['v'])), e['t'] - 0.004, 0.16 * e['v'] ** 0.8, e['pan'] * 0.8); onsets.append(e['t'])
for e in of('clack'):
    place(HITS, peak(clack()), e['t'] - 0.003, 0.14, 0); onsets.append(e['t'])
for e in of('chisel'):
    v = e.get('v', 1.0)
    place(HITS, peak(chisel()), e['t'], 0.05 * v, e['pan'] * 0.9)
    place(HITS, peak(chisel()), e['t'] + 0.045, 0.028 * v, e['pan'] * 0.9)       # the mallet's echo tap


# ── laurel: a dry rustle and a couple of glints per leaf pair ──
def rustle(d=0.25):
    x = seg(d)
    n = bandpass(rng.standard_normal(len(x)), 3500, 11000)
    flutter = 0.6 + 0.4 * np.sin(2 * np.pi * rng.uniform(25, 40) * x) ** 2
    return peak(n) * flutter * np.sin(np.pi * np.clip(x / d, 0, 1)) ** 2


def glint(f):
    x = seg(0.5)
    return (np.sin(2 * np.pi * f * x) + 0.3 * np.sin(2 * np.pi * f * 2.01 * x)) * np.exp(-x / 0.12) * np.minimum(1, x / 0.002)


GLINT = [hz(m) for m in (77, 81, 84, 89, 93)]           # F A C F A, inside the chord
for k, e in enumerate(of('leaf')):
    v = e.get('v', 1)
    place(FX, rustle(), e['t'], 0.02 * v, -0.4 if k % 2 else 0.4)
    place(FX, glint(GLINT[k % len(GLINT)]), e['t'] + 0.03, 0.012 * v, 0.5 if k % 2 else -0.5)

# ── the gilt rule draws outward: a faint shimmer that widens from the centre to both sides ──
for e in of('rule'):
    x = seg(e['d'] + 0.3); u = np.clip(x / e['d'], 0, 1)
    env = np.sin(np.pi * np.clip(x / (e['d'] + 0.3), 0, 1)) ** 2
    for s in (-1, 1):
        n = peak(bandpass(rng.standard_normal(len(x)), 2500, 9000)) * env
        place(FX, n * np.cos(np.pi / 4 * (1 - u)), e['t'], 0.012, s * u * 0.8)
        place(FX, n * np.sin(np.pi / 4 * (1 - u)) * 0.7, e['t'], 0.012, 0)

# ── contour drawings appear: a stylus whisper; mouldings slide in and out on stone ──
for e in of('draw'):
    x = seg(e['d']); u = x / e['d']
    n = peak(bandpass(rng.standard_normal(len(x)), 1800, 7000))
    strokes = 0.55 + 0.45 * np.sin(2 * np.pi * 7.5 * x) ** 2
    place(FX, n * strokes * np.sin(np.pi * u) ** 1.5, e['t'], 0.016, 0)
for e in of('slide'):
    x = seg(e['d'] + 0.15); u = np.clip(x / e['d'], 0, 1)
    n = peak(one_pole(bandpass(rng.standard_normal(len(x)), 120, 3000), 900))
    place(FX, n * np.sin(np.pi * u) ** 1.2, e['t'], 0.05, 0)

# ── the relief rises: a low warm swell; the raking light: air walking left → right ──
for e in of('swell'):
    x = seg(e['d'] + 0.8); u = x / (e['d'] + 0.8)
    n = one_pole(rng.standard_normal(len(x)), 120 + 700 * np.sin(np.pi * u) ** 2)
    tone = np.sin(2 * np.pi * hz(34) * x) + 0.5 * np.sin(2 * np.pi * hz(46) * x)
    env = np.sin(np.pi * np.clip(u * 1.1, 0, 1)) ** 2
    place(FX, (peak(n) * 0.6 + tone * 0.5) * env, e['t'], 0.07, 0)
for e in of('sweep'):
    x = seg(e['d']); u = x / e['d']
    n = peak(one_pole(bandpass(rng.standard_normal(len(x)), 800, 9000), 1200 + 5000 * np.sin(np.pi * u) ** 2))
    env = np.sin(np.pi * u) ** 1.6
    i0 = int(e['t'] * SR); m = min(len(x), N - i0); a = (2 * u - 1 + 1) * np.pi / 4
    FX[0, i0:i0 + m] += (n * env * 0.03 * np.cos(a))[:m]; FX[1, i0:i0 + m] += (n * env * 0.03 * np.sin(a))[:m]

# ── camera moves: a breath of air ──
for e in of('air'):
    x = seg(e['d'] + 0.3); u = np.clip(x / e['d'], 0, 1)
    shape = u ** 2 * np.exp(-np.maximum(x - e['d'], 0) / 0.08) if e['up'] else np.sin(np.pi * u) ** 2
    n = peak(one_pole(rng.standard_normal(len(x)), 300 + 2500 * shape))
    place(FX, n * shape, e['t'], 0.04, 0)

# ── the wreath lifts: a rising chime and a rustle at the top ──
for e in of('lift'):
    x = seg(e['d'] + 0.6); u = np.clip(x / e['d'], 0, 1)
    n = peak(one_pole(bandpass(rng.standard_normal(len(x)), 300, 8000), 600 + 3500 * u))
    place(FX, n * np.sin(np.pi * np.clip(x / (e['d'] + 0.3), 0, 1)) ** 2, e['t'], 0.03, 0)
    for k, m in enumerate([65, 69, 72, 77, 81]):
        place(FX, glint(hz(m)), e['t'] + 0.08 + k * e['d'] * 0.16, 0.022, -0.5 + 0.25 * k)
    place(FX, rustle(0.4), e['t'] + e['d'] * 0.7, 0.03, 0)


# ── emblems: a muted stone settle and a warm chime; the lamp catches with a soft breath ──
def bell(f, d=2.5):
    x = seg(d)
    s = sum(a * np.sin(2 * np.pi * f * r * x + rng.random() * 6) * np.exp(-x / dc)
            for r, a, dc in [(1, 0.6, 1.4), (2.0, 0.3, 0.8), (2.76, 0.14, 0.45), (5.4, 0.05, 0.2)])
    return s * np.minimum(1, x / 0.003)


for e in of('emblem'):
    place(HITS, peak(tock(0.4)), e['t'], 0.06, e['pan'] * 0.7); onsets.append(e['t'])
    place(FX, bell(hz(72 if e['pan'] == 0 else 67)), e['t'] + 0.05, 0.03, e['pan'] * 0.7)
for e in of('flame'):
    x = seg(0.9)
    n = peak(one_pole(rng.standard_normal(len(x)), 400 + 1600 * np.exp(-x / 0.25)))
    crack = np.zeros(len(x))
    for c in rng.uniform(0.05, 0.6, 7):
        i = int(c * SR); k = np.arange(min(150, len(x) - i))
        crack[i:i + len(k)] += rng.choice([-1, 1]) * np.exp(-k / 12) * rng.uniform(0.2, 0.8)
    place(FX, n * np.clip(x / 0.12, 0, 1) * np.exp(-x / 0.35) + 0.2 * crack, e['t'], 0.04, 0)

# the final cadence: a low warm bell under the last chord
cad = [e for e in of('pad') if e['c'] == 3][0]['t']
for m, gn, p in [(41, 0.06, 0), (53, 0.036, -0.3), (57, 0.026, 0.3), (65, 0.018, 0)]:
    place(PAD, bell(hz(m), 3.5), cad + 0.02, gn, p)

# a quiet room bed
bed = peak(bandpass(rng.standard_normal(N), 50, 700)) * 0.004 * np.clip(t / 0.6, 0, 1)
FX[0] += bed; FX[1] += np.roll(bed, 4801)


# ── balance: each hit's 100 ms RMS about 6 dB over the pad around it ──
def rms(x):
    return np.sqrt(np.mean(x ** 2) + 1e-20)


ratios = []
for o in onsets:
    i0 = int(o * SR); w = slice(max(0, i0 - int(0.01 * SR)), min(N, i0 + int(0.1 * SR)))
    pw = slice(max(0, i0 - int(0.4 * SR)), min(N, i0 + int(0.4 * SR)))
    ratios.append(rms(HITS[:, w]) / rms(PAD[:, pw]))
hit_gain = 10 ** (6 / 20) / np.median(ratios)
mix = PAD + HITS * hit_gain + FX * hit_gain ** 0.5 * 3.2       # the effects sit roughly 8-20 dB under the pad


# ── the hall ──
def hall(seed, d=2.6):
    r = np.random.default_rng(seed); x = seg(d)
    h = r.standard_normal(len(x)) * np.exp(-x / 0.62)
    h = bandpass(h, 150, 6500) * (1 - 0.5 * x / d)
    h[:int(0.022 * SR)] = 0
    return h / np.sqrt(np.sum(h ** 2))


def convolve(x, h):
    n = 1 << int(np.ceil(np.log2(len(x) + len(h))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[:len(x)]


out = np.stack([mix[0] * 0.82 + convolve(mix[0], hall(5)) * 0.5, mix[1] * 0.82 + convolve(mix[1], hall(6)) * 0.5])
fade = 1 - np.clip((t - fade_t) / fade_d, 0, 1) ** 1.3
fade[:int(0.03 * SR)] *= np.linspace(0, 1, int(0.03 * SR))
out *= fade


# ── loudness (ITU-R BS.1770: K-weighting, 400 ms blocks, absolute and relative gates) ──
def k_weight(x):
    n = 1 << int(np.ceil(np.log2(len(x) + SR)))
    z = np.exp(-1j * 2 * np.pi * np.fft.rfftfreq(n, 1 / SR) / SR)
    H = np.ones_like(z)
    for b, a in [([1.53512485958697, -2.69169618940638, 1.19839281085285], [1, -1.69065929318241, 0.73248077421585]),
                 ([1.0, -2.0, 1.0], [1, -1.99004745483398, 0.99007225036621])]:
        H *= (b[0] + b[1] * z + b[2] * z * z) / (a[0] + a[1] * z + a[2] * z * z)
    return np.fft.irfft(np.fft.rfft(x, n) * H, n)[:len(x)]


def lufs(st):
    kw = np.stack([k_weight(ch) for ch in st])
    blk, hop = int(0.4 * SR), int(0.1 * SR)
    z = np.array([np.mean(kw[:, i:i + blk] ** 2, axis=1).sum() for i in range(0, N - blk + 1, hop)])
    l = -0.691 + 10 * np.log10(z + 1e-20)
    z = z[l > -70]
    rel = -0.691 + 10 * np.log10(z.mean()) - 10
    z = z[-0.691 + 10 * np.log10(z) > rel]
    return -0.691 + 10 * np.log10(z.mean())


def limit(st, ceiling):
    # look-ahead peak limiter: the gain dips just before a peak and recovers over about 60 ms
    need = np.minimum(1, ceiling / (np.max(np.abs(st), axis=0) + 1e-12))
    w = int(0.003 * SR)
    need = np.min(np.lib.stride_tricks.sliding_window_view(np.pad(need, (0, w), constant_values=1), w + 1), axis=1)
    gain = np.empty(N); gcur = 1.0; rel = 1 - np.exp(-1 / (0.06 * SR))
    for i in range(N):
        gcur = need[i] if need[i] < gcur else gcur + (need[i] - gcur) * rel
        gain[i] = gcur
    return st * gain


CEIL = 10 ** (-1.6 / 20)
for _ in range(3):
    out *= 10 ** ((-14 - lufs(out)) / 20)
    out = limit(out, CEIL)
pk = np.max(np.abs(out))
print(f'audio.wav  {lufs(out):.1f} LUFS  peak {20 * np.log10(pk):.1f} dBFS  hits +6 dB gain x{hit_gain:.2f}')
pcm = (np.clip(out.T, -1, 1) * 32767).astype('<i2')
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
