# events.json -> audio.wav (48 kHz stereo, 10.08 s), everything synthesised here with numpy.
# A clean 125 BPM ad bed: a soft sub kick on the beats, quiet ticking hats on the eighths and a round bass
# walking D minor, B flat, F, C. Over it the cut-outs: a crisp paper snap on every pop and size snap, a pen
# scratch under each line that draws on, a soft brush for the painted ring and the ink fill, a band-passed
# whoosh on each hard zoom, a small tonal glide under each type morph, a glassy shimmer as the engraving
# turns to plaster, a light riser into the title, and a warm bell-piano chord that rings into the fade.
import json
import wave

import numpy as np

SR, DUR = 48000, 10.08
N = int(SR * DUR)
OUT = np.zeros((2, N))
WET = np.zeros((2, N))
T = np.arange(N) / SR
cues = json.load(open('events.json'))
of = lambda k: [c for c in cues if c['k'] == k]
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)


def span(d):
    return np.arange(max(1, int(round(d * SR)))) / SR


def edge(a, b, x):
    k = np.clip((x - a) / (b - a), 0, 1)
    return k * k * (3 - 2 * k)


def unit(x):
    return x / (np.abs(x).max() + 1e-12)


def place(sig, at, gain=1.0, pan=0.0, wet=0.0):
    """Mix a mono signal in at `at` seconds with an equal-power pan (pan clamped to -1..1)."""
    i = int(round(at * SR))
    if i < 0:
        sig, i = sig[-i:], 0
    n = min(len(sig), N - i)
    if n <= 0:
        return
    th = (np.clip(pan, -1, 1) + 1) * np.pi / 4
    s = sig[:n] * gain
    for ch, g in ((0, np.cos(th)), (1, np.sin(th))):
        OUT[ch, i:i + n] += s * g * 1.414
        WET[ch, i:i + n] += s * g * 1.414 * wet


def band(x, lo=None, hi=None, order=2):
    """Zero-phase Butterworth-shaped band in the frequency domain."""
    X = np.fft.rfft(x)
    f = np.maximum(np.fft.rfftfreq(len(x), 1 / SR), 1e-3)
    g = np.ones_like(f)
    if lo:
        g /= np.sqrt(1 + (lo / f) ** (2 * order))
    if hi:
        g /= np.sqrt(1 + (f / hi) ** (2 * order))
    return np.fft.irfft(X * g, len(x))


def noise(n, seed):
    return np.random.default_rng(seed).standard_normal(n)


# ── voices ──
def kick(seed):
    x = span(0.32)
    f = 46 + 70 * np.exp(-x / 0.03)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / 0.16)
    click = band(noise(len(x), seed), 900, 5000) * np.exp(-x / 0.004) * 0.25
    return unit(body + click) * edge(0, 0.002, x)


def hat(seed, open_=False):
    x = span(0.09 if open_ else 0.04)
    return unit(band(noise(len(x), seed), 7000, 15000) * np.exp(-x / (0.03 if open_ else 0.011)))


def bass(m, d, seed):
    x = span(d)
    f = hz(m)
    s = np.sin(2 * np.pi * f * x) + 0.35 * np.sin(4 * np.pi * f * x + 0.3) + 0.12 * np.sin(6 * np.pi * f * x + 0.9)
    return unit(s) * edge(0, 0.008, x) * np.exp(-x / 0.5) * (1 - edge(d - 0.05, d, x))


def snap(seed, bright=1.0):
    """Paper snapping flat: a crisp crack, a papery flutter and a small low tap."""
    x = span(0.14)
    crack = band(noise(len(x), seed), 1800 * bright, 9000) * np.exp(-x / 0.009)
    flutter = band(noise(len(x), seed + 1), 600, 3500) * np.exp(-x / 0.035) * 0.35
    tap = np.sin(2 * np.pi * (150 + 120 * np.exp(-x / 0.01)) * x) * np.exp(-x / 0.03) * 0.5
    return unit(crack + flutter + tap) * edge(0, 0.0015, x)


def scratch(d, seed):
    """A pen dragged over paper: band-passed noise broken into little catches of the nib."""
    r = np.random.default_rng(seed)
    x = span(max(0.06, d))
    hiss = band(noise(len(x), seed), 2200, 8000)
    grain = np.zeros(len(x))
    j = 0
    while j < len(x):
        n = int(r.uniform(0.004, 0.014) * SR)
        grain[j:j + n] += r.uniform(0.3, 1.0) * np.hanning(min(n, len(x) - j))
        j += int(r.uniform(0.003, 0.011) * SR)
    k = x / x[-1]
    return unit(hiss * (0.3 + grain)) * np.sin(np.pi * k) ** 0.5


def brush(d, seed, lo=500, hi=3200):
    x = span(d)
    s = band(noise(len(x), seed), lo, hi) * (0.7 + 0.3 * unit(np.abs(band(noise(len(x), seed + 3), 8, 40))))
    return unit(s) * np.sin(np.pi * x / x[-1]) ** 1.3


def tick(seed):
    x = span(0.06)
    return unit(band(noise(len(x), seed), 2500, 9000) * np.exp(-x / 0.003) + 0.4 * np.sin(2 * np.pi * 3150 * x) * np.exp(-x / 0.012))


def whoosh(d, seed, up=True):
    """Air through a moving band: a resonant one-pole pair whose centre sweeps with the zoom. A punch-in stops
    dead when the zoom lands; the pull-out trails off."""
    tail = 0.015 if up else 0.12
    x = span(d + tail)
    src = noise(len(x), seed)
    k = np.clip(x / d, 0, 1)
    fc = 280 * (12 ** k) if up else 3200 * (12 ** -k)
    lo = np.zeros(len(x))
    bp = np.zeros(len(x))
    a, b = 0.0, 0.0
    g = 1 - np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)):                       # state-variable style: low and band outputs
        a += g[i] * (src[i] - a - 0.6 * b)
        b += g[i] * a
        lo[i] = b
        bp[i] = a
    env = (k ** 1.6 if up else (1 - k) ** 0.8 * edge(0, 0.03, x)) * (1 - edge(d, d + tail, x))
    return unit(bp * env + 0.3 * lo * env)


def glide(d, m0, m1, seed):
    """A soft sine glide with a quiet fifth above, for the morphs."""
    x = span(d + 0.15)
    k = inout = np.clip(x / d, 0, 1)
    inout = np.where(k < 0.5, 4 * k ** 3, 1 - (2 - 2 * k) ** 3 / 2)
    f = hz(m0) * (hz(m1) / hz(m0)) ** inout
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.3 * np.sin(1.5 * ph) + 0.12 * np.sin(2 * ph)
    return unit(s) * edge(0, 0.04, x) * (1 - edge(d - 0.02, d + 0.15, x))


def shimmer(d, seed):
    r = np.random.default_rng(seed)
    x = span(d + 0.4)
    s = sum(np.sin(2 * np.pi * f * x + r.uniform(0, 6)) * r.uniform(0.4, 1) for f in r.uniform(2400, 6200, 14))
    return unit(s) * edge(0, d * 0.5, x) * np.exp(-np.maximum(0, x - d * 0.5) / 0.18)


def riser(d, seed):
    x = span(d)
    k = x / d
    s = band(noise(len(x), seed), 1500, 9000) * k ** 2.4
    f = hz(55) * 2 ** (2 * k)
    s = unit(s) * 0.6 + 0.4 * np.sin(2 * np.pi * np.cumsum(f) / SR) * k ** 2
    return unit(s) * (1 - edge(d - 0.015, d, x))


def bell_note(m, d, seed):
    """Additive piano-bell: a few slightly stretched partials, the high ones dying first."""
    x = span(d)
    f = hz(m)
    s = np.zeros(len(x))
    for n, (a, tau) in enumerate(((1, 2.6), (0.42, 1.5), (0.22, 0.9), (0.12, 0.55), (0.06, 0.35)), start=1):
        s += a * np.sin(2 * np.pi * f * n * (1 + 0.0007 * n * n) * x) * np.exp(-x / tau)
    hammer = band(noise(len(x), seed), 1000, 6000) * np.exp(-x / 0.006) * 0.08
    return unit(s + hammer) * edge(0, 0.004, x)


# ── the bed ──
bed = of('bed')[0]
BEAT = 60 / bed['bpm']
ROOTS = [38, 34, 41, 36]                          # D, B flat, F, C (bass, one bar each)
duck = np.ones(N)
for w in of('whoosh'):
    duck *= 1 - 0.45 * edge(w['t'] - 0.05, w['t'] + 0.05, T) * (1 - edge(w['t'] + w['d'], w['t'] + w['d'] + 0.12, T))
nb = int(round((bed['end'] - bed['t']) / BEAT))
for i in range(nb):
    tb = bed['t'] + i * BEAT
    place(kick(10 + i), tb, 0.42, 0.0)
    m = ROOTS[(i // 4) % 4]
    place(bass(m, BEAT * 0.9, 20 + i), tb, 0.2 if i % 4 else 0.24, -0.05, 0.05)
    if i % 2 == 1:
        place(bass(m + 12, BEAT * 0.4, 40 + i), tb + BEAT / 2, 0.08, 0.1)
for i in range(int(round((bed['end'] - 1.44) / (BEAT / 2)))):
    th = 1.44 + i * BEAT / 2
    place(hat(100 + i, i % 4 == 3), th, 0.05 if i % 2 == 0 else 0.075, 0.35 if i % 2 else 0.25)
OUT *= duck[None, :]

# ── the cut-outs ──
for i, c in enumerate(of('pop')):
    place(snap(200 + i, 1.0), c['t'], 0.34 * c['v'], c['p'] * 0.7, 0.12)
for i, c in enumerate(of('snap')):
    place(snap(260 + i, 1.3), c['t'], 0.4 * c['v'], c['p'] * 0.7, 0.1)
    place(kick(280 + i)[: int(0.12 * SR)], c['t'], 0.12, 0.0)
place(snap(300, 0.8), of('cut')[0]['t'], 0.3, of('cut')[0]['p'] * 0.6, 0.1)
for i, c in enumerate(of('scratch')):
    place(scratch(c['d'], 400 + i), c['t'], 0.13 * c['v'], c['p'] * 0.7, 0.08)
for i, c in enumerate(of('tick')):
    place(tick(500 + i), c['t'], 0.16 * c['v'], c['p'] * 0.7, 0.15)
for i, c in enumerate(of('brush')):
    place(brush(c['d'], 600 + i), c['t'], 0.14, c['p'] * 0.6, 0.15)
for i, c in enumerate(of('fill')):
    place(brush(c['d'] + 0.06, 650 + i, 250, 1800), c['t'], 0.2, c['p'] * 0.5, 0.2)
for i, c in enumerate(of('whoosh')):
    place(whoosh(c['d'], 700 + i, c['up'] == 1), c['t'], 0.3, c['p'], 0.25)
for i, c in enumerate(of('glide')):
    place(glide(c['d'], c['m0'], c['m1'], 800 + i), c['t'], 0.085, c['p'] * 0.4, 0.4)
for i, c in enumerate(of('shimmer')):
    place(shimmer(c['d'], 850 + i), c['t'], 0.09, c['p'] * 0.5, 0.5)
for i, c in enumerate(of('turn')):
    place(brush(c['d'], 870 + i, 150, 900), c['t'], 0.08, c['p'] * 0.4, 0.2)
for c in of('riser'):
    place(riser(c['d'], 900), c['t'], 0.16, 0.0, 0.2)

# ── the lockup chord: F major with an added ninth, rolled up, ringing into the fade ──
ch = of('chord')[0]
for j, m in enumerate((41, 53, 57, 60, 67, 72)):
    place(bell_note(m, DUR - ch['t'], 950 + j), ch['t'] + 0.018 * j, 0.15 if j else 0.18, -0.45 + 0.18 * j, 0.45)


# ── mix: a small bright room on the send, gentle master fade, peak at -1 dBFS ──
def room(seed, d=1.4):
    x = span(d)
    n = noise(len(x), seed)
    ir = 0.5 * n * np.exp(-x / 0.1) + band(n, None, 4000) * np.exp(-x / 0.45)
    ir *= edge(0, 0.01, x)
    return ir / np.sqrt(np.sum(ir ** 2))


def convolve(x, ir):
    n = 1 << int(np.ceil(np.log2(len(x) + len(ir))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[:len(x)]


mix = OUT + 0.35 * np.stack([convolve(WET[0], room(11)), convolve(WET[1], room(12))])
fade = of('fade')[0]
k = np.clip((T - fade['t']) / (DUR - 0.02 - fade['t']), 0, 1)
mix *= (edge(0, 0.01, T) * 0.5 * (1 + np.cos(np.pi * k)))[None, :]
mix = np.nan_to_num(mix)
mix *= 10 ** (-1.5 / 20) / (np.abs(mix).max() + 1e-9)   # -1.5 dBFS in the wav keeps the AAC decode at or under -1
pcm = (np.clip(mix.T, -1, 1) * 32767).astype('<i2')
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
