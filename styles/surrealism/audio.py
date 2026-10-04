# events.json → audio.wav (48 kHz stereo)
# Cold daylight on an empty plain: a quiet, slowly beating drone of open fifths that sits above the
# low end and swells only under the title, a glassy overtone haze above it and a thin wind. The pocket watch ticks on the second (a dry click with a
# small steel ring), panned where the watch sits; it stiffens with a faint creak, then melts on a
# soft glide that sags in pitch, slows its vibrato and settles with a muffled thump. The bird shadow's
# wing beats are feathery breaths of filtered noise and its slide away is a whoosh that runs off to the
# right. The far walker's feet land as soft distant thuds. The title's shadow arrives on a low swell,
# the letters on a single soft clock chime, the caption on a glassy shimmer, and the tail decays into
# the fade. Everything is synthesised with numpy; the mix goes through a synthetic open-air space and
# is set to about -14 LUFS (K-weighted, gated) with peaks held under -1.5 dBFS. The bed stays low under the
# first two beats so the ticks, the glide and the wing beats carry them, which gives the mix its range.
import json, wave, numpy as np

SR = 48000
ev = json.load(open('events.json'))
DUR = max(e['t'] + e.get('d', 0) for e in ev)
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(145)
note = lambda m: 440.0 * 2 ** ((m - 69) / 12)
BED, FX = np.zeros((2, N)), np.zeros((2, N))
cues = lambda kind: [e for e in ev if e['k'] == kind]


def span(d):
    return np.arange(int(d * SR)) / SR


def put(bus, x, at, gain=1.0, pan=0.0):
    """add mono x into a stereo bus at time `at`, equal-power panned"""
    i = int(round(at * SR))
    if i < 0:
        x, i = x[-i:], 0
    n = min(len(x), N - i)
    if n <= 0:
        return
    th = (np.clip(pan, -1, 1) + 1) * np.pi / 4
    bus[0, i:i + n] += x[:n] * gain * np.cos(th)
    bus[1, i:i + n] += x[:n] * gain * np.sin(th)


def band(x, lo, hi):
    F = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    F *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4) / (1 + (f / hi) ** 4)
    return np.fft.irfft(F, len(x))


def norm1(x):
    return x / (np.max(np.abs(x)) + 1e-12)


def lowpass_sweep(x, fc):
    """one-pole low-pass whose cutoff (Hz, an array) moves over time"""
    a = 1 - np.exp(-2 * np.pi * np.asarray(fc, float) / SR)
    a = np.broadcast_to(a, x.shape)
    y = np.empty_like(x); z = 0.0
    for i in range(len(x)):
        z += a[i] * (x[i] - z); y[i] = z
    return y


# ── the drone: open fifths on D, each voice a few slightly detuned partials that beat slowly. It is
# held low through the watch and the bird and rises under the title ──
fade_in = np.clip(t / 1.2, 0, 1) ** 1.5
swell_at = np.interp(t, [0, 3.0, 5.6, 6.6, 7.6, DUR], [0.42, 0.42, 0.6, 0.85, 1.0, 1.0])
fade_in = fade_in * swell_at
for m, g, p in [(38, 0.16, -0.2), (45, 0.30, 0.25), (50, 0.34, -0.05), (57, 0.20, 0.35)]:
    f0 = note(m)
    v = np.zeros(N)
    for k, amp in [(1, 1.0), (2, 0.42), (3, 0.2), (4, 0.09), (5, 0.05)]:
        for det in (-0.6, 0.6):
            v += amp * np.sin(2 * np.pi * (f0 * k + det * k * 0.5) * t + rng.random() * 6)
    swell = 0.8 + 0.2 * np.sin(2 * np.pi * (0.07 + 0.03 * rng.random()) * t + rng.random() * 6)
    put(BED, v * swell * fade_in, 0, g * 0.045, p)
# a glassy haze of high partials, very quiet, slowly breathing
for m, p in [(74, -0.5), (81, 0.5), (86, 0.0)]:
    trem = 0.55 + 0.45 * np.sin(2 * np.pi * (0.11 + 0.05 * rng.random()) * t + rng.random() * 6)
    put(BED, np.sin(2 * np.pi * note(m) * t) * trem * fade_in, 0, 0.0055, p)
# thin wind over the plain
wind = band(lowpass_sweep(rng.standard_normal(N), 700 + 500 * np.sin(2 * np.pi * 0.09 * t) ** 2), 170, 2400)
put(BED, norm1(wind) * fade_in, 0, 0.026, -0.3)
put(BED, norm1(np.roll(wind, 9001)) * fade_in, 0, 0.026, 0.3)


# ── the watch ──
def tick(v):
    d = span(0.16)
    click = norm1(band(rng.standard_normal(len(d)), 2500, 11000)) * np.exp(-d / 0.0035)
    ring = sum(a * np.sin(2 * np.pi * f * d + rng.random() * 6) * np.exp(-d / dc)
               for f, a, dc in [(3150, 0.5, 0.025), (4870, 0.32, 0.016), (7300, 0.18, 0.01)])
    body = np.sin(2 * np.pi * 900 * d) * np.exp(-d / 0.008)
    return (click * 0.9 + ring * 0.45 + body * 0.25) * v


for e in cues('tick'):
    put(FX, tick(e['v']), e['t'], 0.24, e['pan'])
    put(FX, tick(e['v'] * 0.35), e['t'] + 0.11, 0.24, e['pan'])        # the escapement's soft second beat

for e in cues('creak'):                 # the stiffening: a thin tense tone that bends up and holds
    d = span(e['d'] + 0.1); u = np.clip(d / e['d'], 0, 1)
    f = 1650 + 140 * np.minimum(u / 0.3, 1)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    grain = norm1(band(rng.standard_normal(len(d)), 1500, 4000)) * (0.5 + 0.5 * np.sin(2 * np.pi * 31 * d))
    env = np.sin(np.pi * np.clip(d / (e['d'] + 0.1), 0, 1)) ** 2
    put(FX, (tone * 0.5 + grain * 0.3) * env, e['t'], 0.018, -0.05)

for e in cues('melt'):                  # the soft fold: a glide that sags, its vibrato slowing like wax
    d = span(e['d'] + 0.9); u = np.clip(d / e['d'], 0, 1)
    sag = u * u * (3 - 2 * u)
    f = note(69) * 2 ** (-(sag * 14 + 1.2 * np.clip((d - e['d']) / 0.9, 0, 1)) / 12)
    vib = 1 + 0.012 * np.sin(2 * np.pi * np.cumsum(5.5 - 4.0 * sag) / SR)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    voice = np.sin(ph) + 0.35 * np.sin(2 * ph + 0.4) + 0.12 * np.sin(3 * ph + 1.1)
    env = np.clip(d / 0.25, 0, 1) * np.exp(-np.maximum(d - e['d'], 0) / 0.35)
    put(FX, voice * env, e['t'], 0.075, -0.1)
    goo = lowpass_sweep(rng.standard_normal(len(d)), 900 - 700 * sag)  # a viscous low breath under it
    put(FX, norm1(goo) * env, e['t'], 0.03, 0.05)

for e in cues('settle'):                # the flap meets the stone, muffled, and sways
    d = span(0.9)
    f = 70 + 50 * np.exp(-d / 0.03)
    thump = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-d / 0.12)
    put(FX, band(thump, 90, 2000), e['t'], 0.1, -0.1)
    sway = np.sin(2 * np.pi * note(55) * d) * np.exp(-d / 0.45) * (0.5 + 0.5 * np.cos(2 * np.pi * d / 0.62))
    put(FX, sway, e['t'] + 0.05, 0.02, -0.1)

# ── the camera: a breath of air under each long move ──
for e in cues('air'):
    d = span(e['d']); u = d / e['d']
    shape = np.sin(np.pi * u) ** 2
    n = lowpass_sweep(rng.standard_normal(len(d)), 250 + 1400 * shape)
    put(FX, norm1(n) * shape, e['t'], 0.03, -0.25)
    put(FX, norm1(np.roll(n, 4000)) * shape, e['t'], 0.03, 0.25)


# ── the bird shadow: feathery wing beats, then a whoosh that leaves to the right ──
def wingbeat():
    d = span(0.32)
    n = band(rng.standard_normal(len(d)), 450, 3200)
    env = np.exp(-((d - 0.08) / 0.045) ** 2) + 0.6 * np.exp(-((d - 0.17) / 0.06) ** 2)
    return norm1(n) * env


for e in cues('wing'):
    put(FX, wingbeat(), e['t'] - 0.08, 0.12 * e['v'], e['pan'])
for e in cues('glide'):
    d = span(e['d']); u = d / e['d']
    n = lowpass_sweep(band(rng.standard_normal(len(d)), 200, 6000), 500 + 3500 * u)
    env = np.clip(u / 0.25, 0, 1) * (1 - u) ** 1.5
    pans = e['pan0'] + (e['pan1'] - e['pan0']) * u
    th = (pans + 1) * np.pi / 4
    i = int(e['t'] * SR); m = min(len(d), N - i)
    FX[0, i:i + m] += (norm1(n) * env * 0.06 * np.cos(th))[:m]
    FX[1, i:i + m] += (norm1(n) * env * 0.06 * np.sin(th))[:m]


# ── the far walker: faint, distant footfalls, more knock than thud ──
def footfall():
    d = span(0.5)
    f = 140 + 60 * np.exp(-d / 0.03)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-d / 0.07)
    scuff = norm1(band(rng.standard_normal(len(d)), 300, 1800)) * np.exp(-d / 0.02)
    return lowpass_sweep(body + 0.3 * scuff, 900)


for e in cues('stride'):
    put(FX, footfall(), e['t'], 0.035 * e['v'], e['pan'] * 0.8)


# ── the title ──
def bell(f, d=3.6):
    x = span(d)
    s = sum(a * np.sin(2 * np.pi * f * r * x + rng.random() * 6) * np.exp(-x / dc)
            for r, a, dc in [(0.5, 0.35, 2.2), (1.0, 0.6, 1.6), (1.19, 0.22, 0.9), (2.0, 0.28, 0.8), (2.74, 0.12, 0.4), (4.1, 0.05, 0.18)])
    return s * np.clip(x / 0.004, 0, 1)


for e in cues('shadow'):                # the shadow arrives on a low swell
    d = span(e['d'] + 1.6); u = np.clip(d / (e['d'] + 0.3), 0, 1)
    env = np.sin(np.pi / 2 * u) ** 2 * np.exp(-np.maximum(d - e['d'] - 0.3, 0) / 0.6)
    tone = np.sin(2 * np.pi * note(38) * d) + 0.5 * np.sin(2 * np.pi * note(50) * d + 0.3)
    hush = lowpass_sweep(rng.standard_normal(len(d)), 180 + 500 * u)
    put(FX, (tone * 0.7 + norm1(hush) * 0.5) * env, e['t'], 0.07, 0)
for e in cues('chime'):                 # the letters: one soft clock chime
    put(FX, bell(note(74)), e['t'], 0.1, -0.1)
    put(FX, bell(note(62), 4.2), e['t'] + 0.01, 0.075, 0.1)
for e in cues('shimmer'):               # the caption: a glassy shimmer
    d = span(1.8)
    s = sum(np.sin(2 * np.pi * note(m) * d + rng.random() * 6) * (0.6 + 0.4 * np.sin(2 * np.pi * (6 + k) * d)) for k, m in enumerate([86, 90, 93, 98]))
    env = np.clip(d / 0.3, 0, 1) * np.exp(-d / 0.7)
    put(FX, s * env, e['t'], 0.006, 0.2)


# ── space: a long, airy, decorrelated tail ──
def space(seed, d=3.2):
    r = np.random.default_rng(seed); x = span(d)
    h = band(r.standard_normal(len(x)), 120, 7000) * np.exp(-x / 0.8)
    h[:int(0.03 * SR)] = 0
    return h / np.sqrt(np.sum(h ** 2))


def conv(x, h):
    n = 1 << int(np.ceil(np.log2(len(x) + len(h))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[:len(x)]


dry = BED + FX
mix = np.stack([dry[0] * 0.85 + conv(dry[0], space(1)) * 0.42, dry[1] * 0.85 + conv(dry[1], space(2)) * 0.42])
end = cues('end')[0]
mix *= 1 - np.clip((t - end['t']) / end['d'], 0, 1) ** 1.4
mix[:, :int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))


# ── loudness: K-weighting as a frequency response, 400 ms blocks, absolute + relative gates ──
def kweight(x):
    n = 1 << int(np.ceil(np.log2(len(x))))
    f = np.fft.rfftfreq(n, 1 / SR)
    shelf = 10 ** (4.0 / 20 * (1 / (1 + (1500 / np.maximum(f, 1)) ** 2)))   # +4 dB above ~1.5 kHz
    hp = 1 / np.sqrt(1 + (38 / np.maximum(f, 1e-3)) ** 4)                     # second-order high-pass near 38 Hz
    return np.fft.irfft(np.fft.rfft(x, n) * shelf * hp, n)[:len(x)]


def loudness(st):
    k = np.stack([kweight(c) for c in st])
    blk, hop = int(0.4 * SR), int(0.1 * SR)
    p = np.array([np.mean(k[:, i:i + blk] ** 2, axis=1).sum() for i in range(0, k.shape[1] - blk, hop)])
    lv = -0.691 + 10 * np.log10(p + 1e-20)
    p = p[lv > -70]
    gate = -0.691 + 10 * np.log10(p.mean()) - 10
    p = p[-0.691 + 10 * np.log10(p) > gate]
    return -0.691 + 10 * np.log10(p.mean())


def soft_limit(st, ceil):
    """gain that dips a few ms ahead of any peak over `ceil` and recovers over ~80 ms"""
    need = np.minimum(1, ceil / (np.max(np.abs(st), axis=0) + 1e-12))
    B = int(0.004 * SR)
    blocks = np.concatenate([need, np.ones((-len(need)) % B)]).reshape(-1, B).min(axis=1)
    need = np.repeat(np.minimum(blocks, np.append(blocks[1:], 1.0)), B)[:len(need)]   # this block or the next
    g = np.empty(len(need)); cur = 1.0; rel = 1 - np.exp(-1 / (0.08 * SR))
    for i in range(len(need)):
        cur = need[i] if need[i] < cur else cur + (need[i] - cur) * rel
        g[i] = cur
    w = np.hanning(97); w /= w.sum()
    g = np.minimum(g, np.convolve(g, w, mode='same'))                              # round off the attack
    return st * g


CEIL = 10 ** (-1.6 / 20)
for _ in range(3):
    mix *= 10 ** ((-14 - loudness(mix)) / 20)
    mix = soft_limit(mix, CEIL)
print(f'audio.wav  {DUR:.2f} s  {loudness(mix):.1f} LUFS  peak {20 * np.log10(np.max(np.abs(mix))):.1f} dBFS')
pcm = (np.clip(mix.T, -1, 1) * 32767).astype('<i2')
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
