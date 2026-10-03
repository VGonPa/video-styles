# events.json -> audio.wav (48 kHz stereo, 10 s), numpy only, every sound synthesised.
# A 120 BPM diner twist in C: kick on the beats, handclaps on 2 and 4, an upright-ish walking bass and short
# square-wave organ stabs on the off-beats, over I-IV-V-I. Each ink plate that slams onto the paper is a
# printing-press thunk (a low thud and a metallic clack); the cherry's bounce is a spring boing; every grid cell
# that pops in is a bubbly pitch-drop "pop" panned where the cell lands; each diagonal re-ink ripple runs up a
# marimba as it crosses the grid; the camera's pull-backs are short downward air sweeps and the dive into the
# dots is a rising whoosh. The title lands on a brass chord stab with a crash, the key plate thunks, and a held
# organ-and-brass chord fades out with the picture.
import json, wave
import numpy as np

SR, DUR = 48000, 10.0
N = int(SR * DUR)
OUT = np.zeros((2, N))
RNG = np.random.default_rng(146)
TAU = 2 * np.pi


def secs(d):
    return np.arange(int(round(d * SR))) / SR


def midi(m):
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def place(sig, at, gain=1.0, pan=0.0):
    """Mix a mono signal in at time `at` with an equal-power pan; pan may be a number or a per-sample array."""
    i0 = int(round(at * SR))
    if i0 >= N or len(sig) == 0:
        return
    s = sig
    if i0 < 0:
        s, i0 = s[-i0:], 0
    n = min(len(s), N - i0)
    p = np.clip(np.asarray(pan, dtype=float), -1.0, 1.0)      # clamp: the law below stays real and finite
    if p.ndim:
        p = p[:n]
    ang = (p + 1.0) * np.pi / 4.0
    OUT[0, i0:i0 + n] += s[:n] * gain * np.cos(ang)
    OUT[1, i0:i0 + n] += s[:n] * gain * np.sin(ang)


def env(d, att=0.002, dec=0.1, rel=0.01):
    """Attack, exponential decay, and a short release so nothing clicks at the end."""
    tb = secs(d)
    e = np.minimum(1.0, tb / max(att, 1e-4)) * np.exp(-tb / dec)
    tail = np.clip((d - tb) / max(rel, 1e-4), 0.0, 1.0)
    return e * tail


def bandpass(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1.0 / SR)
    X *= 1.0 / (1.0 + (lo / np.maximum(f, 1.0)) ** 4) / (1.0 + (f / hi) ** 4)
    return np.fft.irfft(X, len(x))


def hiss(d, lo, hi):
    x = bandpass(RNG.standard_normal(max(16, int(round(d * SR)))), lo, hi)
    return x / (np.abs(x).max() + 1e-9)


def glide(f, d):
    """A sine whose frequency follows the array (or constant) f over d seconds."""
    tb = secs(d)
    f = np.broadcast_to(np.asarray(f, dtype=float), tb.shape)
    return np.sin(TAU * np.cumsum(f) / SR)


# ── drums ──
def kick(d=0.32):
    tb = secs(d)
    body = glide(46 + 95 * np.exp(-tb / 0.035), d) * env(d, 0.001, 0.16, 0.02)
    return body + 0.25 * hiss(d, 1500, 6000) * env(d, 0.0005, 0.004, 0.002)


def clap(d=0.28):
    tb = secs(d)
    x = hiss(d, 900, 5200)
    e = np.zeros_like(tb)
    for j, off in enumerate([0.0, 0.011, 0.022, 0.031]):      # a few hands slightly apart, then the room
        u = tb - off
        e += np.where(u >= 0, np.exp(-np.maximum(u, 0) / (0.007 if j < 3 else 0.09)), 0.0) * (0.8 if j < 3 else 1.0)
    return x * e * np.clip((d - tb) / 0.02, 0, 1)


def hat(d=0.06):
    return hiss(d, 7000, 16000) * env(d, 0.0005, 0.014, 0.01)


def crash(d=2.4):
    tb = secs(d)
    metal = np.zeros_like(tb)
    r = np.random.default_rng(9)
    for _ in range(40):
        f = r.uniform(3000, 11000)
        metal += np.sin(TAU * f * tb + r.uniform(0, TAU)) * np.exp(-tb / r.uniform(0.3, 1.2))
    metal /= np.abs(metal).max() + 1e-9
    return (0.7 * hiss(d, 4000, 15000) + 0.3 * metal) * env(d, 0.002, 0.7, 0.05)


# ── pitched voices ──
def bass(m, d=0.42):
    f = midi(m)
    tb = secs(d)
    s = glide(f, d) + 0.35 * np.sin(2 * TAU * f * tb) + 0.12 * np.sin(3 * TAU * f * tb)
    thump = 0.4 * hiss(d, 60, 400) * env(d, 0.001, 0.012, 0.005)
    return (s * env(d, 0.004, 0.22, 0.04) + thump)


def organ(ms, d=0.16, bright=1.0):
    """A thin, buzzy combo organ: band-limited squares with a quick vibrato, all notes together."""
    tb = secs(d)
    out = np.zeros_like(tb)
    for j, m in enumerate(ms):
        f = midi(m) * (1 + 0.004 * np.sin(TAU * 6.2 * tb + j))
        ph = TAU * np.cumsum(f) / SR
        for h in range(1, 12, 2):
            if h * midi(m) > 9000:
                break
            out += np.sin(h * ph) / h * (bright if h > 1 else 1.0)
    return out / max(1, len(ms)) * env(d, 0.004, 0.5, 0.03)


def brass(ms, d, stab=True):
    """Sawtooth-ish partials with a bright attack that mellows: a brassy chord."""
    tb = secs(d)
    out = np.zeros_like(tb)
    r = np.random.default_rng(len(ms) * 7 + int(d * 10))
    bright = 0.35 + 0.65 * np.exp(-tb / (0.12 if stab else 0.6))
    for m in ms:
        f = midi(m) * (1 - 0.012 * np.exp(-tb / 0.03))           # the lip comes up to pitch
        ph = TAU * np.cumsum(f) / SR + r.uniform(0, TAU)
        for h in range(1, 16):
            if h * midi(m) > 10000:
                break
            out += np.sin(h * ph) / h * bright ** (h - 1)
    out /= len(ms)
    return out * (env(d, 0.012, 0.35, 0.05) if stab else np.minimum(1, tb / 0.08) * np.clip((d - tb) / 0.3, 0, 1))


def marimba(m, d=0.3):
    f = midi(m)
    tb = secs(d)
    return (np.sin(TAU * f * tb) * np.exp(-tb / 0.11) + 0.35 * np.sin(TAU * 3.93 * f * tb) * np.exp(-tb / 0.025)) * np.minimum(1, tb / 0.001)


def vibes(m, d=1.6):
    f = midi(m)
    tb = secs(d)
    trem = 1 - 0.3 * (0.5 + 0.5 * np.sin(TAU * 5.5 * tb))
    return (np.sin(TAU * f * tb) + 0.2 * np.sin(TAU * 4 * f * tb) * np.exp(-tb / 0.2)) * env(d, 0.002, 0.7, 0.1) * trem


# ── effects ──
def thunk(heavy=1.0):
    """The press: a felt-padded thud under a metal-on-metal clack."""
    d = 0.5
    tb = secs(d)
    thud = glide(38 + 70 * np.exp(-tb / 0.05), d) * env(d, 0.001, 0.13, 0.03)
    clack = np.zeros_like(tb)
    for f, a, dc in [(1180, 1.0, 0.03), (2310, 0.7, 0.022), (3725, 0.5, 0.016), (5480, 0.3, 0.01)]:
        clack += a * np.sin(TAU * f * tb) * np.exp(-tb / dc)
    clack += 0.6 * hiss(d, 1800, 7000) * np.exp(-tb / 0.006)
    return heavy * thud + 0.55 * clack


def pop(row=1):
    d = 0.14
    tb = secs(d)
    f0 = 880 + 120 * (3 - row)
    s = glide(f0 * np.exp(-tb / 0.03) + 240, d) * env(d, 0.001, 0.045, 0.01)
    return s + 0.15 * hiss(d, 2500, 8000) * np.exp(-tb / 0.003)


def boing(d=0.5, f0=260, depth=0.45):
    tb = secs(d)
    f = f0 * (1 + depth * np.sin(TAU * 11 * tb) * np.exp(-tb / 0.18))
    return glide(f, d) * env(d, 0.003, 0.2, 0.05)


def air(d, f0, f1, rise=True):
    """Noise through a band-pass whose centre glides from f0 to f1 (a whoosh), shaped to swell or fall."""
    n = int(round(d * SR))
    x = RNG.standard_normal(n)
    fc = np.geomspace(f0, f1, n)
    y = np.empty(n)
    lo = bp = 0.0
    q = 2.2
    for i in range(n):                                          # state-variable filter, one sample at a time
        g = 2 * np.sin(np.pi * min(fc[i], SR / 6) / SR)
        hp = x[i] - lo - bp / q
        bp += g * hp
        lo += g * bp
        y[i] = bp
    y /= np.abs(y).max() + 1e-9
    k = np.linspace(0, 1, n)
    shape = k ** 2.2 * np.clip((1 - k) / 0.04, 0, 1) if rise else np.sin(np.pi * k) ** 1.5
    return y * shape


# ── the cue list ──
EV = json.load(open('events.json'))
def cues(k):
    return [e for e in EV if e['k'] == k]
T_TITLE = cues('title')[0]['t']
T_CLOSE = cues('close')[0]['t']
DIVE = cues('dive')[0]

# the groove: I (C) - IV (F) - V (G) - I (C), one bar per four beats from 0.25
BARS = [[48, 52, 55, 57], [53, 57, 60, 62], [55, 59, 62, 64], [48, 52, 55, 57]]
CHORDS = [[60, 64, 67], [60, 65, 69], [59, 62, 67], [60, 64, 67]]
for e in cues('beat'):
    t, i = e['t'], e['i']
    if t >= T_TITLE - 0.01:
        continue                                                # the title hit takes over
    bar, beat = divmod(i, 4)
    in_dive = DIVE['t'] + 0.1 < t < T_TITLE
    if not in_dive:
        place(kick(), t, 0.55)
        place(bass(BARS[min(bar, 3)][beat] - 12), t, 0.3, -0.1)
    if i >= 4 and beat % 2 == 1 and not in_dive:
        place(clap(), t, 0.22, 0.05)
    if i >= 4 and not in_dive:                                 # twist off-beats: a hat and an organ stab
        place(hat(), t + 0.25, 0.08, 0.35)
        place(organ(CHORDS[min(bar, 3)], 0.17), t + 0.25, 0.09, -0.25)
    elif i < 4:
        place(hat(), t + 0.25, 0.05, 0.35)
# a clap fill into the title, under the whoosh
for j, dt in enumerate([0.375, 0.25, 0.125]):
    place(clap(0.2), T_TITLE - dt, 0.12 + 0.05 * j, 0.0)

# the four plates slam onto the paper (the key plate, last, hits hardest)
for e in cues('plate'):
    place(thunk(1.3 if e['ink'] == 'k' else 1.0), e['t'] - 0.004, 0.42 if e['ink'] == 'k' else 0.32, {'y': -0.25, 'm': 0.25, 'c': -0.1, 'k': 0.0}[e['ink']])
# the cherry: a big bounce on the hero, then the two cherries' hop
for e in cues('bounce'):
    place(boing(0.55, 300, 0.5), e['t'] - 0.25, 0.14, e['pan'])
for e in cues('hop'):
    place(boing(0.4, 380, 0.35), e['t'] - 0.22, 0.08, e['pan'])
# cells popping in
for e in cues('pop'):
    place(pop(e.get('row', 1)), e['t'] - 0.01, 0.16 if e['t'] < 4.5 else 0.09, e['pan'])
# re-ink ripples: each wave of swaps runs up the marimba in the order it crosses the grid
SCALE = [72, 74, 76, 79, 81, 84, 86, 88, 91, 93, 96]
waves = {}
for e in cues('swap'):
    waves.setdefault(int((e['t'] - 0.25) / 0.5), []).append(e)    # grouped by the beat that launched them
for w in waves.values():
    w.sort(key=lambda e: e['t'])
    for j, e in enumerate(w):
        step = round(j / max(1, len(w) - 1) * (len(SCALE) - 1))
        place(marimba(SCALE[step], 0.3), e['t'], 0.05 if len(w) > 8 else 0.08, e['pan'])
# camera pull-backs: short falling air; the dive: a long rising whoosh with a climbing tone
for e in cues('zoom'):
    place(air(e['d'] + 0.1, 5000, 700, rise=False), e['t'], 0.07, 0.0)
d = DIVE['d'] + 0.15
place(air(d, 250, 7000, rise=True), DIVE['t'], 0.36, 0.0)
tb = secs(d)
riser = glide(220 * 2 ** (2.5 * (tb / d) ** 1.6), d) * (tb / d) ** 2 * np.clip((d - tb) / 0.03, 0, 1)
place(riser, DIVE['t'], 0.08, 0.0)

# the title: a brass stab and a crash on the beat, the key plate's thunk, then a held chord that fades with the picture
place(kick(0.5), T_TITLE, 0.6)
place(bass(36, 1.2), T_TITLE, 0.3)
place(brass([48, 55, 60, 64, 67, 72], 0.7, stab=True), T_TITLE, 0.3, -0.1)
place(crash(2.6), T_TITLE, 0.16, 0.2)
for e in cues('tkey'):
    place(thunk(1.1), e['t'] - 0.004, 0.3, 0.0)
hold = DUR - (T_TITLE + 0.15)
pad = brass([48, 55, 64, 69, 74], hold, stab=False) * 0.6 + organ([60, 64, 67, 69, 74], hold, bright=0.6) * np.minimum(1, secs(hold) / 0.4) * 0.5
place(pad, T_TITLE + 0.15, 0.22, 0.0)
for e in cues('sub'):
    for j, m in enumerate([76, 81, 88]):
        place(vibes(m, 1.5), e['t'] + 0.06 * j, 0.05, -0.3 + 0.3 * j)

# ── a little room, the fade with the picture, and the master ──
def room(seed, d=1.2):
    r = np.random.default_rng(seed)
    tb = secs(d)
    h = bandpass(r.standard_normal(len(tb)) * np.exp(-tb / 0.28), 150, 8000)
    h[:int(0.012 * SR)] = 0
    return h / np.sqrt((h ** 2).sum())
def convolve(x, h):
    n = 1 << int(np.ceil(np.log2(len(x) + len(h))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[:len(x)]
wet = np.stack([convolve(OUT[0], room(1)), convolve(OUT[1], room(2))])
mixd = OUT + 0.22 * wet
tt = np.arange(N) / SR
k = np.clip((tt - T_CLOSE) / 0.32, 0, 1)                         # the picture fades over 0.3 s from the close cue
mixd *= np.minimum(1, tt / 0.01) * (1 - k * k * (3 - 2 * k))
peak = np.abs(mixd).max() + 1e-9
mixd = np.tanh(mixd / peak * 1.4) / np.tanh(1.4)
mixd *= 0.89 / (np.abs(mixd).max() + 1e-9)                       # about -1 dBFS
mixd[:, -int(0.02 * SR):] = 0
assert np.isfinite(mixd).all()
pcm = (np.clip(mixd.T, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb')
w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', round(float(np.abs(mixd).max()), 3))
