# events.json → audio.wav (48 kHz stereo, 10 s)
# A painter's rhythm section. Each Prussian-blue outline lands as a dry brush swish over a soft hand-drum
# beat, the sun's swoosh the deepest; the outlines struck again over the colour come back as a quicker brushed roll. The lay-in is a
# patter of thick wet dabs that thickens as the strokes pour on. A warm A-major organ-and-strings pad
# swells under the day, the sun's rings of light answer with bell shimmer, and a gust hisses through the
# wheat from left to right. At sunset the chord sinks to F-sharp minor seventh over a low swell, the
# afterglow is smeared along the ridge with a warm brushed sigh, and broad night washes sweep in; every
# star ignites as a celesta note from the pentatonic (the big ones lower and longer), placed where it
# shines. The title resolves to A major with a rising harp run under the letters, a soft bell for the
# dates, and all of it fades with the picture into a small warm room.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(142)
t = np.arange(N) / SR
midi = lambda m: 440.0 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def ramp(x, a, b): return np.clip((x - a) / (b - a), 0, 1)
def smooth(k): return k * k * (3 - 2 * k)
def place(sig, at, g=1.0, pan=0.0):
    i = int(round(at * SR)); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    a = (pan + 1) * np.pi / 4                                       # equal-power pan
    L[i:i + n] += sig[:n] * g * np.cos(a) * 1.414; R[i:i + n] += sig[:n] * g * np.sin(a) * 1.414
def bandpass(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def noise(d, lo, hi, r=rs): return norm(bandpass(r.standard_normal(int(d * SR)), lo, hi))
def sweep_bp(x, f0, f1, q=2.5):   # a band-pass whose centre glides from f0 to f1 (state-variable filter)
    fc = np.geomspace(f0, f1, len(x)); y = np.empty_like(x); lo = bp = 0.0
    for i in range(len(x)):
        f = 2 * np.sin(np.pi * fc[i] / SR); hp = x[i] - lo - bp / q; bp += f * hp; lo += f * bp; y[i] = bp
    return y

ev = json.load(open('events.json'))
get = lambda k: [e for e in ev if e['k'] == k]
first = lambda k: get(k)[0]
close = first('close')['t']; sunset = first('sunset'); night = first('night'); title = first('title'); day = first('day')['t']

# ── the room: a faint warm air under everything ──
air = norm(np.cumsum(rs.standard_normal(N))); air = bandpass(air - air.mean(), 30, 900)
air = norm(air) * smooth(ramp(t, 0.0, 0.6))
L += 0.006 * air; R += 0.006 * np.roll(air, 2111)

# ── outlines: a dry brush swish over a hand-drum beat, panned to where the line is drawn ──
def brush(d, f0, f1, grain=1.0):
    tb = tt(d + 0.06); x = rs.standard_normal(len(tb))
    x *= 1 + grain * (rs.random(len(tb)) < 0.04) * 3                  # bristles catching the weave
    y = sweep_bp(x, f0, f1, 1.8)
    env = np.minimum(1, tb / 0.012) * np.where(tb < d, 0.75 + 0.25 * np.sin(np.pi * tb / d), np.exp(-(tb - d) / 0.025))
    return norm(y) * env
def drum(f, d=0.5, click=0.25):
    tb = tt(d); ph = 2 * np.pi * np.cumsum(f * (1 + 0.5 * np.exp(-tb / 0.03))) / SR
    body = np.sin(ph) * np.exp(-tb / 0.16) + 0.3 * np.sin(1.6 * ph) * np.exp(-tb / 0.07)
    tap = noise(d, 200, 2500) * np.exp(-tb / 0.012)
    return (body + click * tap) * np.minimum(1, tb / 0.0015)
DRUM = [midi(40), midi(45), midi(43), midi(45)]                   # a steady four-beat figure under the lines
for e in get('contour'):
    i = e['i']
    if e.get('hero'):   # the sun drawn as one swoosh: the loudest beat, a deep drum under a long round brush
        place(brush(e['d'] + 0.1, 900, 4200, 1.2), e['t'], 0.17, e['pan'] * 0.6)
        place(drum(midi(33), 0.9, 0.4), e['t'], 0.26, e['pan'] * 0.3)
        continue
    place(brush(e['d'], 1400 + 200 * (i % 3), 3600 + 300 * (i % 2)), e['t'], 0.12, e['pan'] * 0.8)
    place(drum(DRUM[i % 4], click=0.3 if i % 4 == 0 else 0.18), e['t'], 0.19 if i % 4 == 0 else 0.13, e['pan'] * 0.4)
# struck again over the colour: a quicker brushed roll that builds
rr = get('reassert')
for j, e in enumerate(rr):
    k = j / max(1, len(rr) - 1)
    place(brush(0.12, 2600, 5200, 1.5), e['t'], 0.07 + 0.05 * k, e['pan'] * 0.8)
    place(drum(midi(47 if j % 2 else 45), 0.3, 0.4), e['t'], 0.06 + 0.06 * k, e['pan'] * 0.4)
place(drum(midi(33), 1.2, 0.5), rr[-1]['t'] + 1 / 15, 0.2, 0.0)                    # the downbeat as the picture breathes

# ── the lay-in: thick wet dabs, as many as the strokes landing in each painted frame ──
def dab():
    d = 0.09; tb = tt(d); f = rs.uniform(150, 260)
    plop = np.sin(2 * np.pi * np.cumsum(f * (1 - 0.35 * tb / d)) / SR) * np.exp(-tb / 0.018)
    smear = noise(d, 250, rs.uniform(900, 1600)) * np.exp(-tb / 0.03)
    return (0.6 * plop + smear) * np.minimum(1, tb / 0.002)
for e in get('dabs'):
    count = int(min(7, 1 + e['n'] / 60))
    for _ in range(count):
        place(dab(), e['t'] + rs.uniform(0, 1 / 15), 0.085 * (0.6 + 0.4 * min(1, e['n'] / 300)) * rs.uniform(0.6, 1.0),
              float(np.clip(e['pan'] + rs.uniform(-0.45, 0.45), -1, 1)))

# ── the pad: organ and strings, A major under the day, F♯ minor 7 at sunset, A major add9 for the title ──
def voice(m, env, seed, bright=1.0):
    r = np.random.default_rng(seed); f0 = midi(m); out = np.zeros(N)
    for det in (-6, 0, 5):
        vib = 1 + 0.0025 * np.sin(2 * np.pi * (4.8 + r.random()) * t + r.random() * 6)
        ph = 2 * np.pi * np.cumsum(f0 * 2 ** (det / 1200) * vib) / SR
        for h in range(1, int(min(4800 * bright, 9000) / f0) + 1):
            out += np.sin(h * ph + r.random() * 6) * (h ** -1.25 if h > 1 else 1.0) * (0.55 if h % 2 == 0 else 1.0)
    return out * env
s0, s1 = sunset['t'], sunset['t'] + 1.0
ti = title['t']
day_env = smooth(ramp(t, day, 2.6)) * (0.75 + 0.25 * smooth(ramp(t, 2.6, 3.4))) * (1 - smooth(ramp(t, s0, s1)))
dusk_env = smooth(ramp(t, s0 - 0.2, s1)) * (1 - smooth(ramp(t, ti - 0.1, ti + 0.6)))
home_env = smooth(ramp(t, ti - 0.1, ti + 0.9)) * (1 - smooth(ramp(t, close, DUR)))
pad = np.zeros((2, N))
CHORDS = [(day_env, [45, 52, 57, 61, 64, 69]), (dusk_env, [42, 49, 54, 57, 61, 64]), (home_env, [45, 52, 57, 61, 64, 71])]
for c, (env, notes) in enumerate(CHORDS):
    for j, m in enumerate(notes):
        v = voice(m, env, 50 + 10 * c + j, 0.8 if m > 60 else 1.0) * (1.0 if m < 50 else 0.7 if m < 62 else 0.5)
        p = (-0.5 + j / (len(notes) - 1)) * 0.8
        pad[0] += v * np.cos((p + 1) * np.pi / 4); pad[1] += v * np.sin((p + 1) * np.pi / 4)
pad *= 0.13 / (np.abs(pad).max() + 1e-9)
L += pad[0]; R += pad[1]
# a low swell as the sun goes down
tb = tt(sunset['d'] + 1.4)
swell = (np.sin(2 * np.pi * midi(30) * tb) + 0.5 * noise(len(tb) / SR, 30, 160)) * smooth(np.clip(tb / sunset['d'], 0, 1)) * np.exp(-np.maximum(0, tb - sunset['d']) / 0.5)
place(swell, s0, 0.09, 0.15)

# ── the sun's rings of light: bell shimmer ──
def bell(f, d=2.2):
    tb = tt(d); s = 0
    for ratio, a, dec in [(1, 1, 1.4), (2.0, 0.45, 0.9), (2.76, 0.35, 0.6), (5.4, 0.18, 0.3), (8.9, 0.08, 0.15)]:
        s = s + a * np.sin(2 * np.pi * f * ratio * tb + rs.random() * 6) * np.exp(-tb / dec)
    return s * np.minimum(1, tb / 0.004) * (1 + 0.15 * np.sin(2 * np.pi * 6 * tb))
for j, e in enumerate(get('pulse')):
    place(bell(midi([81, 76, 85][j % 3])), e['t'], 0.065, e['pan'])
    place(bell(midi([88, 83, 93][j % 3]), 1.4), e['t'] + 0.06, 0.025, -e['pan'] * 0.5)

# ── the gust: wind through the wheat, crossing from left to right ──
gu = first('gust'); tb = tt(gu['d'] + 0.6); u = np.clip(tb / gu['d'], 0, 1)
wind = sweep_bp(rs.standard_normal(len(tb)), 350, 1100, 1.2) * np.sin(np.pi * u) ** 1.5
rustle = np.zeros(len(tb)); idx = rs.integers(0, len(tb), 1800); rustle[idx] = rs.uniform(-1, 1, len(idx))
rustle = bandpass(rustle, 2500, 9000) * np.sin(np.pi * u) ** 2
g = norm(wind) * 0.8 + norm(rustle) * 0.5
i0 = int(gu['t'] * SR); n = min(len(g), N - i0); pan = np.clip(-1 + 2 * u[:n], -1, 1) * 0.85
L[i0:i0 + n] += 0.1 * g[:n] * np.cos((pan + 1) * np.pi / 4) * 1.414
R[i0:i0 + n] += 0.1 * g[:n] * np.sin((pan + 1) * np.pi / 4) * 1.414

# ── the afterglow smeared along the ridge: a warm, slow brushed sigh ──
ag = first('afterglow')
place(brush(ag['d'], 300, 900, 0.3), ag['t'], 0.07, 0.15)

# ── night repaints the sky: broad soft washes sweeping in ──
for j in range(7):
    at = night['t'] + j * night['d'] / 7 + rs.uniform(0, 0.05)
    place(brush(0.38, 500 + 60 * j, 1500 + 80 * j, 0.4), at, 0.06, float(np.sin(j * 2.1)) * 0.7)

# ── stars: a celesta note each, from the pentatonic, where the star shines ──
def celesta(f, d=2.0):
    tb = tt(d)
    s = np.sin(2 * np.pi * f * tb) * np.exp(-tb / 0.9) + 0.25 * np.sin(2 * np.pi * 4 * f * tb) * np.exp(-tb / 0.25) \
        + 0.12 * np.sin(2 * np.pi * 2 * f * tb) * np.exp(-tb / 0.5)
    return (s + 0.15 * noise(d, 4000, 12000) * np.exp(-tb / 0.006)) * np.minimum(1, tb / 0.0015)
PENTA = [78, 81, 83, 85, 88, 90, 93, 95, 97]                         # F♯ A B C♯ E, rising through the night
for j, e in enumerate(sorted(get('star'), key=lambda e: e['t'])):
    big = e.get('size', 40) >= 70; mid = e.get('size', 40) >= 45
    m = PENTA[j % len(PENTA)] - (12 if big else 0)
    place(celesta(midi(m), 3.0 if big else 2.0), e['t'], 0.12 if big else 0.1 if mid else 0.08, e['pan'] * 0.85)
    if big: place(bell(midi(m + 7), 2.4), e['t'] + 0.04, 0.03, e['pan'] * 0.6)

# ── the title: a harp run rising under the letters, a brushed flourish, then a soft bell for the dates ──
def harp(f, d=1.8):
    tb = tt(d); s = sum(a * np.sin(2 * np.pi * f * h * tb + rs.random() * 6) * np.exp(-tb / dec) for h, a, dec in [(1, 1, 0.9), (2, 0.4, 0.5), (3, 0.18, 0.3), (4, 0.08, 0.2)])
    return s * np.minimum(1, tb / 0.002)
RUN = [57, 61, 64, 69, 71, 73, 76, 81, 83, 85, 88, 93, 95, 97, 100, 105, 107, 109]
for j, e in enumerate(get('letter')):
    place(harp(midi(RUN[j % len(RUN)])), e['t'] + 0.02, 0.03 * (0.8 if j > 12 else 1.0), e['pan'] * 0.7)
    place(brush(0.08, 2200, 4200, 0.8), e['t'], 0.02, e['pan'] * 0.7)
place(brush(title['end'] - ti, 900, 3000, 0.6), ti, 0.04, 0.0)
place(drum(midi(33), 1.6, 0.3), ti, 0.14, 0.0)
sub = first('subtitle')['t']
place(bell(midi(69), 2.4), sub, 0.04, -0.2); place(bell(midi(76), 2.2), sub + 0.05, 0.03, 0.2)

# ── a small warm room ──
def ir(seed, d=2.0):
    r = np.random.default_rng(seed); tb = tt(d)
    x = r.standard_normal(len(tb)) * np.exp(-tb / 0.42)
    x = bandpass(x, 120, 7000) * (1 - 0.6 * np.clip(tb / d, 0, 1)); x[:int(0.015 * SR)] = 0
    return x / np.sqrt((x ** 2).sum())
def conv(x, h):
    n = 1 << int(np.ceil(np.log2(len(x) + len(h))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[:len(x)]
outL = L * 0.85 + conv(L, ir(21)) * 0.32; outR = R * 0.85 + conv(R, ir(22)) * 0.32
master = smooth(ramp(t, 0, 0.1)) * (1 - smooth(ramp(t, close, DUR)) ** 1.1)
st = np.stack([outL * master, outR * master], 1)
st = np.tanh(st / (np.abs(st).max() + 1e-9) * 1.2) / np.tanh(1.2)
st *= 0.89 / (np.abs(st).max() + 1e-9)                                        # peak about -1 dBFS
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
