# events.json -> audio.wav (48 kHz stereo, 9.6 s), all of it synthesised here with numpy.
# A breezy hillside meadow above a river bend. Wind moves through the grass, the river murmurs below
# and grasshoppers trill. The thin washes go down as broad wet sweeps of the brush, then the canvas
# fills to a flurry of bristle dabs that follow the strokes across the frame. Swallows twitter as they
# cross; a gust swells from left to right, hisses through the meadow and snaps the washing on the line.
# The cloud shadow comes in as a low, cool E minor ninth; as the sun breaks out low a harp glissando
# climbs D lydian across the stereo field with the repainting wave and opens onto a warm D major ninth.
# The title is dabbed on in softer brushwork, the subtitle gets two bell notes over a G major ninth on
# a D pedal, and the picture dissolves into light on a high, airy D chord that thins away.
import json
import wave

import numpy as np

SR, DUR = 48000, 9.6
N = int(SR * DUR)
DRY_L, DRY_R = np.zeros(N), np.zeros(N)
WET_L, WET_R = np.zeros(N), np.zeros(N)
rng = np.random.default_rng(141)

cues = json.load(open('events.json'))
of = lambda k: [c for c in cues if c['k'] == k]
first = lambda k: of(k)[0]
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)


def secs(d):
    return np.arange(int(round(d * SR))) / SR


def smooth(a, b, x):
    k = np.clip((x - a) / (b - a), 0, 1)
    return k * k * (3 - 2 * k)


def put(sig, at, gain=1.0, pan=0.0, wet=0.25):
    """Mix a mono signal in at `at` seconds, equal-power panned (pan may be a per-sample array)."""
    i = int(round(at * SR))
    if i < 0:
        sig = sig[-i:]
        pan = pan[-i:] if np.ndim(pan) else pan
        i = 0
    n = min(len(sig), N - i)
    if n <= 0:
        return
    p = np.clip(pan[:n] if np.ndim(pan) else pan, -1, 1)
    th = (p + 1) * np.pi / 4
    left, right = sig[:n] * gain * np.cos(th) * 1.414, sig[:n] * gain * np.sin(th) * 1.414
    DRY_L[i:i + n] += left; DRY_R[i:i + n] += right
    WET_L[i:i + n] += left * wet; WET_R[i:i + n] += right * wet


def band(x, lo=None, hi=None, order=2):
    """Zero-phase band-pass with Butterworth-like skirts, done in the frequency domain."""
    X = np.fft.rfft(x)
    f = np.maximum(np.fft.rfftfreq(len(x), 1 / SR), 1e-3)
    g = np.ones_like(f)
    if lo:
        g /= np.sqrt(1 + (lo / f) ** (2 * order))
    if hi:
        g /= np.sqrt(1 + (f / hi) ** (2 * order))
    return np.fft.irfft(X * g, len(x))


def unit(x):
    return x / (np.abs(x).max() + 1e-12)


def gliding_band(x, centre, width):
    """Band-pass whose centre and width (Hz, one value per sample) drift over time: short-time FFT, overlap-add."""
    M, hop = 4096, 1024
    win = np.hanning(M)
    padded = np.concatenate([np.zeros(M), x, np.zeros(M)])
    out, norm = np.zeros(len(padded)), np.zeros(len(padded))
    f = np.fft.rfftfreq(M, 1 / SR)
    for s in range(0, len(padded) - M, hop):
        c = int(np.clip(s + M // 2 - M, 0, len(x) - 1))
        g = np.exp(-0.5 * ((f - centre[c]) / width[c]) ** 2)
        out[s:s + M] += np.fft.irfft(np.fft.rfft(padded[s:s + M] * win) * g, M) * win
        norm[s:s + M] += win ** 2
    return (out / np.maximum(norm, 1e-6))[M:M + len(x)]


# ── voices ──
def harp(m, seed, ring=None):
    """A plucked gut string: partials set by the pluck point, upper ones dying first, a little stretch."""
    r = np.random.default_rng(seed)
    f = hz(m)
    d = ring or min(2.6, 0.9 + 260 / f)
    x = secs(d)
    s = np.zeros(len(x))
    for k in range(1, min(14, int(7000 / f)) + 1):
        amp = abs(np.sin(np.pi * k * 0.21)) / k ** 0.9
        tau = d * 0.42 / (1 + 0.45 * (k - 1))
        s += amp * np.sin(2 * np.pi * f * k * (1 + 2.5e-4 * k * k) * x + r.random() * 6) * np.exp(-x / tau)
    s += 0.04 * band(r.standard_normal(len(x)), 1500, 6000) * np.exp(-x / 0.004)
    return unit(s * np.minimum(1, x / 0.0025))


def piano(m, seed, d=3.0):
    """A soft felt hammer: two strings a hair apart, a quick first decay into a long tail."""
    r = np.random.default_rng(seed)
    f = hz(m)
    x = secs(d)
    s = np.zeros(len(x))
    for det in (-0.7, 0.7):
        ff = f * 2 ** (det / 1200)
        for k in range(1, min(10, int(5000 / f)) + 1):
            amp = 1 / k ** 1.6
            s += amp * np.sin(2 * np.pi * ff * k * (1 + 3e-4 * k * k) * x + r.random() * 6) * np.exp(-x / (1.4 / (1 + 0.5 * k)))
    env = 0.55 * np.exp(-x / 0.35) + 0.45 * np.exp(-x / 2.2)
    return unit(s * env * np.minimum(1, x / 0.006))


def pad(m, d, att, rel, seed, bright=1400):
    """Three slightly detuned additive saws through a soft low-pass: a quiet string/organ wash."""
    r = np.random.default_rng(seed)
    f = hz(m)
    x = secs(d + rel)
    s = np.zeros(len(x))
    for det in (-5, 0, 6):
        ff = f * 2 ** (det / 1200)
        ph = r.random() * 6
        for k in range(1, min(24, int(4000 / ff)) + 1):
            s += np.sin(2 * np.pi * ff * k * x + ph * k) / k / (1 + (ff * k / bright) ** 2)
    env = smooth(0, att, x) * (1 - smooth(d, d + rel, x))
    return unit(s) * env


def bell(m, seed, d=2.2):
    """A celesta-like bar: near-harmonic partials with a bright, quick top."""
    r = np.random.default_rng(seed)
    f = hz(m)
    x = secs(d)
    s = np.zeros(len(x))
    for ratio, amp, tau in ((1, 1, 0.9), (2.0, 0.3, 0.4), (3.01, 0.12, 0.18), (4.17, 0.08, 0.08)):
        s += amp * np.sin(2 * np.pi * f * ratio * x + r.random() * 6) * np.exp(-x / tau)
    return unit(s * np.minimum(1, x / 0.002))


def dab(d, lo, hi, seed):
    """One brush mark on canvas: rough bristle noise and a soft felt bump of the brush landing."""
    r = np.random.default_rng(seed)
    x = secs(d)
    hiss = band(r.standard_normal(len(x)), lo, hi)
    grain = 0.55 + 0.45 * unit(np.abs(band(r.standard_normal(len(x)), 30, 260)))
    env = (1 - np.exp(-x / 0.004)) * np.exp(-x / (d * 0.35))
    bump = band(r.standard_normal(len(x)), 90, 380) * np.exp(-x / 0.012)
    return unit(hiss) * grain * env + 0.35 * unit(bump)


def sweep(d, seed):
    """A broad wet brush drawn across the ground: soft, low, swelling and dying with the stroke."""
    r = np.random.default_rng(seed)
    x = secs(d)
    k = x / d
    s = band(r.standard_normal(len(x)), 220, 2200) * (0.7 + 0.3 * unit(np.abs(band(r.standard_normal(len(x)), 8, 40))))
    return unit(s) * np.sin(np.pi * k) ** 1.5


def twitter(seed):
    """A swallow's call: a quick run of thin rising 'vit' notes."""
    r = np.random.default_rng(seed)
    parts = []
    for _ in range(r.integers(3, 6)):
        d = r.uniform(0.025, 0.045)
        x = secs(d)
        f = r.uniform(3400, 4200) + r.uniform(1500, 2600) * x / d + 220 * np.sin(2 * np.pi * 70 * x)
        parts.append(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * x / d) ** 2)
        parts.append(np.zeros(int(r.uniform(0.03, 0.06) * SR)))
    return np.concatenate(parts)


# ── the meadow: wind in the grass, the river murmuring below, a few grasshoppers ──
t = np.arange(N) / SR
life = smooth(0.2, 1.2, t) * (1 - smooth(8.7, 9.55, t))
for side, seed in ((-0.5, 1), (0.5, 2)):
    r = np.random.default_rng(seed)
    swell = 0.5 + 0.5 * unit(band(r.standard_normal(N), 0.2, 1.6))
    grass = unit(band(r.standard_normal(N), 1600, 7000)) * swell
    put(grass * life, 0, 0.045, side, wet=0.15)
    murmur = unit(band(r.standard_normal(N), 160, 700)) * (0.6 + 0.4 * unit(band(r.standard_normal(N), 0.3, 3)))
    put(murmur * life, 0, 0.055, side * 0.6, wet=0.2)
for k in range(7):
    at = 1.4 + k * 1.05 + rng.uniform(0, 0.4)
    d = rng.uniform(0.35, 0.7)
    x = secs(d)
    trill = np.sin(2 * np.pi * rng.uniform(4800, 6200) * x) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * rng.uniform(22, 30) * x)))
    put(band(trill, 3000, 9000) * np.sin(np.pi * x / d), at, 0.016, rng.uniform(-0.8, 0.8), wet=0.3)

# ── the ébauche: broad wet sweeps of the brush ──
for i, c in enumerate(of('wash')):
    put(sweep(max(0.12, c['d']), 3000 + i), c['t'], 0.026 + 0.016 * c['v'], c['p'] * 0.8, wet=0.2)

# ── the broken strokes: a flurry of dabs, as many and as strong as the strokes landing in each 1/15 s ──
for i, c in enumerate(of('dab')):
    grains = 1 + int(round(5 * c['v']))
    for g in range(grains):
        d = 0.04 + 0.12 * c['v'] * rng.random()
        at = c['t'] + rng.random() / 15
        put(dab(d, 1100, 6500, 1000 + i * 8 + g), at, 0.08 + 0.15 * c['v'], np.clip(c['p'] + rng.uniform(-0.3, 0.3), -1, 1), wet=0.1)

# ── swallows twittering as they cross ──
for i, c in enumerate(of('swallow')):
    for j in range(2):
        at = c['t'] - 0.25 + 0.45 * j
        put(twitter(300 + 10 * i + j), at, 0.075, np.clip(c['dir'] * (-0.6 + 0.9 * (j + 0.5) / 2), -1, 1), wet=0.4)

# ── the gust: wind swelling across the field, the meadow hissing, the washing snapping on the line ──
g = first('gust')
x = secs(g['d'])
k = x / g['d']
env = smooth(0, 0.35, k) * (1 - smooth(0.45, 1.0, k))
wind = gliding_band(rng.standard_normal(len(x)), 320 + 700 * np.sin(np.pi * k) ** 2, 180 + 380 * np.sin(np.pi * k))
put(unit(wind) * env, g['t'], 0.11, -0.9 + 1.8 * k, wet=0.2)
hiss = np.zeros(len(x))
for _ in range(1100):
    j = int(rng.beta(2.2, 2.8) * len(x))
    n = int(rng.uniform(0.002, 0.007) * SR)
    if j + n < len(x):
        hiss[j:j + n] += rng.standard_normal(n) * np.hanning(n) * rng.uniform(0.3, 1)
put(unit(band(hiss, 2000, 9000)) * env, g['t'] + 0.15, 0.06, -0.7 + 1.4 * k, wet=0.25)
ln = first('linen')
curve = np.array(ln['curve'])
lt_ = ln['t'] + np.arange(len(curve)) * ln['step']
vel = np.abs(np.gradient(curve)) / ln['step']
v = np.interp(t, lt_, vel / vel.max(), left=0, right=0)
flap = unit(band(rng.standard_normal(N), 300, 2600)) * (0.45 + 0.55 * np.abs(np.sin(2 * np.pi * 15 * t + 2 * np.sin(2 * np.pi * 3 * t))))
put(flap * v ** 1.5, 0, 0.07, ln['p'], wet=0.25)
peak_t = lt_[int(np.argmax(curve))]
snap = band(rng.standard_normal(int(0.08 * SR)), 600, 4000) * np.exp(-secs(0.08) / 0.012)
put(unit(snap), peak_t - 0.02, 0.05, ln['p'], wet=0.3)

# ── the cloud shadow: a low, cool E minor ninth that swells and gives way to the light ──
s = first('shadow')
for i, m in enumerate((40, 47, 54, 55, 62)):
    put(pad(m, 0.75, 0.45, 0.55, 400 + i, bright=900), s['t'], 0.045, -0.5 + 0.25 * i, wet=0.45)

# ── the sun breaks out: a harp glissando up D lydian across the field, onto a warm D major ninth ──
lt = first('light')
scale = [62, 64, 66, 68, 69, 71, 73]
notes = [o * 12 + n for o in (0, 1, 2) for n in scale][:19]
for i, m in enumerate(notes):
    k = i / (len(notes) - 1)
    put(harp(m, 500 + i), lt['t'] + lt['d'] * k ** 0.9, 0.042 * (0.75 + 0.25 * k), -0.8 + 1.6 * k, wet=0.5)
bloom = lt['t'] + lt['d'] + 0.03
for i, m in enumerate((38, 45, 52, 54, 61)):
    put(piano(m, 600 + i), bloom + 0.018 * i, 0.05, -0.4 + 0.2 * i, wet=0.4)
    put(pad(m, 1.1, 0.25, 0.9, 620 + i), bloom, 0.03, -0.4 + 0.2 * i, wet=0.5)
put(harp(81, 640, ring=2.4), bloom + 0.1, 0.035, 0.5, wet=0.6)

# ── the title, dabbed on in softer, lower brushwork ──
for i, c in enumerate(of('tdab')):
    for gi in range(1 + int(round(3 * c['v']))):
        put(dab(0.035 + 0.05 * rng.random(), 700, 4200, 2000 + i * 8 + gi), c['t'] + rng.random() / 15, 0.035 + 0.06 * c['v'],
            np.clip(c['p'], -1, 1), wet=0.15)

# ── the subtitle: two bell notes over a G major ninth on a D pedal, held while the picture holds ──
sub = first('sub')
for i, m in enumerate((38, 43, 50, 54, 57, 62)):
    put(piano(m, 700 + i, d=3.2), sub['t'] + 0.02 * i, 0.05, -0.45 + 0.18 * i, wet=0.45)
    put(pad(m, 1.0, 0.4, 0.9, 720 + i, bright=1100), sub['t'], 0.025, -0.45 + 0.18 * i, wet=0.5)
put(bell(78, 760), sub['t'] + 0.08, 0.04, -0.2, wet=0.55)
put(bell(81, 761), sub['t'] + 0.34, 0.035, 0.25, wet=0.55)

# ── into the light: an airy high D chord swells with the haze, a few harp notes drift down, all thins away ──
gl_ = first('glow')
end = first('end')['t']
rise = gl_['t'] - 0.45                     # the airy chord is already sounding when the light starts to take the picture
for i, m in enumerate((62, 69, 74, 76, 78, 81)):
    put(pad(m, end - rise - 0.6, 0.5, 0.6, 900 + i, bright=2600), rise, 0.024, -0.5 + 0.2 * i, wet=0.6)
for i, m in enumerate((38, 45)):
    put(pad(m, end - rise - 0.6, 0.4, 0.6, 920 + i, bright=700), rise, 0.03, -0.2 + 0.4 * i, wet=0.5)
x = secs(end - rise)
air = gliding_band(rng.standard_normal(len(x)), 2500 + 4000 * x / x[-1], 900 + 1200 * x / x[-1])
put(unit(air) * smooth(0, 0.6, x), rise, 0.03, 0.3, wet=0.5)
for i, m in enumerate((86, 81, 78, 74)):
    put(harp(m, 940 + i), rise + 0.1 + 0.18 * i, 0.028 * (1 - 0.12 * i), 0.5 - 0.25 * i, wet=0.65)


# ── a soft room: decaying noise, brighter early and darker late, different per ear ──
def room(seed, d=2.0):
    r = np.random.default_rng(seed)
    x = secs(d)
    n = r.standard_normal(len(x))
    ir = 0.4 * n * np.exp(-x / 0.25) + band(n, None, 2600) * np.exp(-x / 0.6)
    ir *= smooth(0, 0.015, x)
    return ir / np.sqrt(np.sum(ir ** 2))


def convolve(x, ir):
    n = 1 << int(np.ceil(np.log2(len(x) + len(ir))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[:len(x)]


left = DRY_L + 0.55 * convolve(WET_L, room(11))
right = DRY_R + 0.55 * convolve(WET_R, room(12))
out = np.stack([left, right], 1)
out *= 0.89 / (np.abs(out).max() + 1e-9)
# the master fade follows the picture into the light: a raised cosine from the glow cue, near silence by ~9.4 s
k = np.clip((t - gl_['t']) / (9.45 - gl_['t']), 0, 1)
out *= (smooth(0, 0.02, t) * 0.5 * (1 + np.cos(np.pi * k)))[:, None]
pcm = (np.clip(out, -1, 1) * 32767).astype('<i2')
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
