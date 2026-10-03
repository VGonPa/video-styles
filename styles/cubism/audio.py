# events.json -> audio.wav (48 kHz stereo, 9.6 s), all of it synthesised here with numpy.
# A quiet studio. Charcoal scratches as the guitar is drawn and a soft brush as its planes fill; then
# every cut line snaps on with a dry scratch and every facet that locks into its new view plucks one
# Karplus-Strong string, so the fracture plays an arpeggio down the Andalusian cadence (A minor, G, F,
# E). Each pasted paper is snipped, slides in and settles with a soft thump on a low A, G, F and, for the
# title's sheet, E; the stencil title is dabbed on with a dry brush, and an E major chord is strummed under
# it and rings into the fade.
import json
import wave

import numpy as np

SR, DUR = 48000, 9.6
N = int(SR * DUR)
DRY = np.zeros((2, N))
WET = np.zeros((2, N))
GTR = np.zeros((2, N))          # plucked strings go through the guitar body before the mix
rng = np.random.default_rng(144)

cues = json.load(open('events.json'))
of = lambda k: [c for c in cues if c['k'] == k]
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)


def secs(d):
    return np.arange(int(round(d * SR))) / SR


def ramp(a, b, x):
    k = np.clip((x - a) / (b - a), 0, 1)
    return k * k * (3 - 2 * k)


def place(bus, sig, at, gain=1.0, pan=0.0, wet=None):
    """Add a mono signal at `at` seconds, equal-power panned (pan may vary per sample)."""
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
    s = sig[:n] * gain
    bus[0, i:i + n] += s * np.cos(th) * 1.414
    bus[1, i:i + n] += s * np.sin(th) * 1.414
    if wet:
        WET[0, i:i + n] += s * np.cos(th) * 1.414 * wet
        WET[1, i:i + n] += s * np.sin(th) * 1.414 * wet


def bandpass(x, lo=None, hi=None, order=2):
    """Zero-phase filter with Butterworth-shaped skirts, applied in the frequency domain."""
    X = np.fft.rfft(x)
    f = np.maximum(np.fft.rfftfreq(len(x), 1 / SR), 1e-3)
    g = np.ones_like(f)
    if lo:
        g /= np.sqrt(1 + (lo / f) ** (2 * order))
    if hi:
        g /= np.sqrt(1 + (f / hi) ** (2 * order))
    return np.fft.irfft(X * g, len(x))


def norm(x):
    return x / (np.abs(x).max() + 1e-12)


# ── voices ──
def pluck(m, seed, t60=None, bright=0.55, d=None, lean=0.5):
    """Karplus-Strong string. The delay line is filled with a soft noise burst shaped by the pluck
    point; each pass blends neighbouring samples (the string's loss) and is scaled to give t60.
    `lean` is the blend weight: 0.5 is the classic average, smaller keeps the upper partials ringing longer."""
    r = np.random.default_rng(seed)
    f = hz(m)
    t60 = t60 or float(np.clip(3.2 - 0.0042 * f, 1.2, 2.9))
    d = d or t60 * 0.9
    n = int(d * SR)
    P = max(2, int(round(SR / f - lean)))      # the two-point blend adds `lean` samples of delay
    rho = 10 ** (-3 / (t60 * SR / (P + lean)))
    exc = r.uniform(-1, 1, P)
    k = max(1, int(round((1 - bright) * 7)))
    exc = np.convolve(exc, np.ones(k) / k, mode='same')
    exc = exc - np.roll(exc, int(P * 0.19))    # plucked a fifth of the way along the string
    exc -= exc.mean()
    y = np.zeros(n + P + 1)
    y[1:P + 1] = exc
    i = P + 1
    while i < len(y):                           # a whole period at a time: it only reads the past
        j = min(i + P, len(y))
        y[i:j] = rho * ((1 - lean) * y[i - P:j - P] + lean * y[i - P - 1:j - P - 1])
        i = j
    out = y[P + 1:]
    x = np.arange(len(out)) / SR
    out = out * np.minimum(1, x / 0.0015) * (1 - ramp(d - 0.25, d, x))
    return norm(out)


def body_ir():
    """A small wooden box: a few damped low resonances under a quick bright knock."""
    x = secs(0.35)
    ir = np.zeros(len(x))
    ir[0] = 1.0
    for f, g, tau in ((102, 0.8, 0.06), (196, 0.6, 0.05), (232, 0.45, 0.04), (395, 0.35, 0.025), (590, 0.2, 0.015)):
        ir += g * 2 / (tau * SR) * np.sin(2 * np.pi * f * x) * np.exp(-x / tau)   # g: gain at the resonance
    return ir


def scratch(d, seed, lo=1700, hi=7500, snap=False):
    """Charcoal dragged over primed canvas: band-passed noise broken into grains by the weave."""
    r = np.random.default_rng(seed)
    x = secs(max(0.05, d))
    hiss = bandpass(r.standard_normal(len(x)), lo, hi)
    grain = np.zeros(len(x))
    j = 0
    while j < len(x):                           # little catches of the stick on the threads
        n = int(r.uniform(0.003, 0.012) * SR)
        grain[j:j + n] += r.uniform(0.3, 1.0) * np.hanning(min(n, len(x) - j))
        j += int(r.uniform(0.002, 0.01) * SR)
    k = x / x[-1]
    env = (np.exp(-k * 3) * 0.7 + 0.3) if snap else np.sin(np.pi * np.clip(k, 0, 1)) ** 0.6
    env *= np.minimum(1, x / 0.004)
    return norm(hiss * (0.35 + grain) * env)


def swish(d, seed):
    """A soft flat brush laying a plane of colour."""
    r = np.random.default_rng(seed)
    x = secs(d)
    s = bandpass(r.standard_normal(len(x)), 350, 2600)
    s *= 0.7 + 0.3 * norm(np.abs(bandpass(r.standard_normal(len(x)), 6, 30)))
    return norm(s) * np.sin(np.pi * x / d) ** 1.4


def snip(seed):
    """Scissors closing: the blades' crisp shear, two small metal rings and a click as they meet."""
    r = np.random.default_rng(seed)
    x = secs(0.12)
    shear = bandpass(r.standard_normal(len(x)), 2500, 11000) * np.exp(-x / 0.018) * ramp(0, 0.004, x)
    ring = sum(a * np.sin(2 * np.pi * f * x + r.random() * 6) * np.exp(-x / tau)
               for f, a, tau in ((3150, 0.5, 0.03), (5230, 0.35, 0.02), (7400, 0.2, 0.012)))
    click = np.zeros(len(x))
    c0 = int(0.045 * SR)
    click[c0:c0 + 240] = bandpass(r.standard_normal(240), 900, 6000) * np.hanning(240) * 2.2
    return norm(shear + 0.25 * ring + click)


def slide(d, seed):
    """A sheet of paper skimming the canvas."""
    r = np.random.default_rng(seed)
    x = secs(d)
    k = x / d
    s = bandpass(r.standard_normal(len(x)), 700, 4200)
    s *= 0.6 + 0.4 * norm(np.abs(bandpass(r.standard_normal(len(x)), 15, 70)))
    return norm(s) * ramp(0, 0.3, k) * (1 - ramp(0.75, 1.0, k))


def thump(seed):
    """Paper settling flat: a soft low bump and a short papery flap."""
    r = np.random.default_rng(seed)
    x = secs(0.25)
    low = np.sin(2 * np.pi * (78 + 30 * np.exp(-x / 0.02)) * x) * np.exp(-x / 0.05)
    flap = bandpass(r.standard_normal(len(x)), 250, 1600) * np.exp(-x / 0.03)
    return norm(low + 0.45 * norm(flap))


def dab(seed, d=0.05):
    """A stiff dry brush tapped through a stencil: a soft pat and a bristly rasp."""
    r = np.random.default_rng(seed)
    x = secs(d)
    pat = bandpass(r.standard_normal(len(x)), 120, 700) * np.exp(-x / 0.008)
    rasp = bandpass(r.standard_normal(len(x)), 1200, 5500) * np.exp(-x / (d * 0.3)) * ramp(0, 0.002, x)
    return norm(0.8 * norm(pat) + norm(rasp))


# ── room tone: a faint, slightly moving hush ──
t = np.arange(N) / SR
life = ramp(0.0, 0.5, t) * (1 - ramp(9.0, 9.58, t))
for ch, seed in ((-0.6, 1), (0.6, 2)):
    r = np.random.default_rng(seed)
    hush = norm(bandpass(r.standard_normal(N), 90, 1800)) * (0.75 + 0.25 * norm(bandpass(r.standard_normal(N), 0.1, 0.8)))
    place(DRY, hush * life, 0, 0.016, ch)

# ── the drawing: charcoal scratches, then soft brushes as the planes fill ──
for i, c in enumerate(of('scratch')):
    place(DRY, scratch(c['d'], 100 + i), c['t'], 0.17 * (0.6 + 0.4 * c['v']), c['p'] * 0.7, wet=0.12)
for i, c in enumerate(of('fill')):
    place(DRY, swish(c['d'], 200 + i), c['t'], 0.1, c['p'] * 0.6, wet=0.2)

# ── the fracture: a dry snap of charcoal per cut, a plucked string per facet that locks ──
for i, c in enumerate(of('cut')):
    place(DRY, scratch(c['d'] + 0.04, 300 + i, 2200, 8000, snap=True), c['t'], 0.1 * (0.6 + 0.4 * c['v']), c['p'] * 0.8, wet=0.1)
CHORDS = [(45, 52, 57, 60, 64, 69), (43, 50, 55, 59, 62, 67), (41, 48, 53, 57, 60, 65), (40, 47, 52, 56, 59, 64)]
ORDER = (0, 2, 3, 4, 5, 3)                       # bass, then up through the chord and back a step
for c in of('lock'):
    i = c['i']
    if i < 24:
        chord = CHORDS[min(3, i // 6)]
        m = chord[ORDER[i % 6]]
    else:                                        # the extra facets ring the top of whichever chord is sounding
        m = CHORDS[int(np.clip((c['t'] - 1.72 + 1e-3) // 0.72, 0, 3))][5]
    bass = i < 24 and i % 6 == 0
    place(GTR, pluck(m, 400 + i, bright=0.5 if bass else 0.62), c['t'], 0.17 if bass else 0.12, c['p'] * 0.55, wet=0.3)

# ── papier collé: snip, slide, thump, and the cadence starts again low: A, G, F, and E for the title's sheet ──
for i, c in enumerate(of('snip')):
    place(DRY, snip(500 + i), c['t'], 0.1, c['p'] * 0.6, wet=0.12)
for i, c in enumerate(of('slide')):
    sig = slide(max(0.1, c['d']), 600 + i)
    place(DRY, sig, c['t'], 0.09, np.linspace(c['p'], c['p1'], len(sig)), wet=0.15)
LOW = {'wood': (45, 52), 'blue': (43, 50), 'news': (41, 48), 'sheet': (40, 47)}
for i, c in enumerate(of('land')):
    place(DRY, thump(700 + i), c['t'], 0.12, c['p'] * 0.5, wet=0.15)
    for j, m in enumerate(LOW[c['kind']]):
        place(GTR, pluck(m, 720 + 4 * i + j, t60=2.6, bright=0.45), c['t'] + 0.012 * j, 0.11, -0.2 + 0.4 * j, wet=0.35)

# ── the title: a dry brush dabbed through the stencil, as fast as the paint builds up ──
for i, c in enumerate(of('dabs')):
    count = int(70 * c['v']) + 10
    for k in range(count):
        u = rng.beta(1.6, 1.6)                   # densest mid-way, like the ease of the build-up
        place(DRY, dab(800 + 97 * i + k, rng.uniform(0.035, 0.06)), c['t'] + u * c['d'], 0.11 * (0.55 + 0.45 * c['v']) * rng.uniform(0.6, 1),
              np.clip(c['p'] + rng.uniform(-0.25, 0.25), -1, 1), wet=0.12)

# ── the final chord: E major strummed down, ringing into the fade ──
st = of('strum')[0]
for j, m in enumerate((40, 47, 52, 56, 59, 64)):
    place(GTR, pluck(m, 900 + j, t60=7.5, bright=0.6, d=9.6 - st['t'], lean=0.1), st['t'] + 0.024 * j, 0.15, -0.5 + 0.2 * j, wet=0.45)
place(DRY, scratch(0.12, 950, 900, 4000, snap=True), st['t'] - 0.01, 0.025, 0.1, wet=0.2)


# ── mix: strings through the body, a small room on the wet send, gentle master fade ──
def room(seed, d=1.3):
    r = np.random.default_rng(seed)
    x = secs(d)
    n = r.standard_normal(len(x))
    ir = 0.5 * n * np.exp(-x / 0.12) + bandpass(n, None, 3000) * np.exp(-x / 0.4)
    ir *= ramp(0, 0.012, x)
    return ir / np.sqrt(np.sum(ir ** 2))


def convolve(x, ir):
    n = 1 << int(np.ceil(np.log2(len(x) + len(ir))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[:len(x)]


B = body_ir()
mix = DRY + np.stack([convolve(GTR[0], B), convolve(GTR[1], B)])
mix += 0.5 * np.stack([convolve(WET[0], room(11)), convolve(WET[1], room(12))])
fade = of('fade')[0]
k = np.clip((t - fade['t']) / (9.58 - fade['t']), 0, 1)
mix *= (ramp(0, 0.01, t) * 0.5 * (1 + np.cos(np.pi * k)))[None, :]
mix *= 0.8 / (np.abs(mix).max() + 1e-9)          # peaks at about -1.9 dBFS
pcm = (np.clip(mix.T, -1, 1) * 32767).astype('<i2')
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
