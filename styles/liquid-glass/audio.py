# events.json → audio.wav (48 kHz stereo, 10 s), all synthesized.
# A soft D-major pad that follows the scene changes (I → vi → IV → I), glassy water-drop plips when the drop
# lands and the droplets condense/merge, airy risers into each morph, a glass "bloom" (low thump + bell
# partials) when the liquid snaps into a new shape, a three-note chime for the mark, small glass taps for
# the staggered letters, a bubble pop when the pill pinches off and sparkling shimmers for the light sweeps.
# Everything runs through a synthetic stereo reverb.
import json, wave
import numpy as np

SR, DUR = 48000, 10.0
N = int(SR * DUR)
dry = np.zeros((2, N)); wet = np.zeros((2, N))
rs = np.random.default_rng(183)


def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)


def add(sig, t, g=1.0, pan=0.0, send=0.3):
    i = int(round(t * SR)); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    gl, gr = np.sqrt(0.5 - pan / 2) * 1.414, np.sqrt(0.5 + pan / 2) * 1.414
    for ch, gg in ((0, gl), (1, gr)):
        dry[ch, i:i + n] += sig[:n] * g * gg * (1 - send * 0.5)
        wet[ch, i:i + n] += sig[:n] * g * gg * send


def lowpass(x, fc):
    # one-pole low-pass; fc may be an array (time-varying cutoff)
    fc = np.broadcast_to(np.asarray(fc, float), x.shape)
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); s = 0.0
    for k in range(len(x)):
        s += a[k] * (x[k] - s); y[k] = s
    return y


def bell(f, d=1.6, bright=1.0):
    t = tt(d); s = np.zeros(len(t))
    for r, a, dec in ((1.0, 1.0, 1.0), (2.76, 0.45 * bright, 0.45), (5.40, 0.22 * bright, 0.25), (8.93, 0.10 * bright, 0.14)):
        if f * r < SR / 2.2:
            s += a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / (d * 0.32 * dec))
    return s * np.minimum(1, t / 0.002)


def plip(f0, f1, d=0.12, sweep=0.04):
    # water drop: a quick upward pitch glide
    t = tt(d); f = f1 + (f0 - f1) * np.exp(-t / sweep)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (d / 3.2)) * np.minimum(1, t / 0.0015)


def thump(f0=110, f1=48, d=0.35):
    t = tt(d); f = f1 + (f0 - f1) * np.exp(-t / 0.05)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (d / 4)) * np.minimum(1, t / 0.003)


def whoosh(d, f0, f1, rise=True):
    t = tt(d); u = t / d
    fc = f0 * (f1 / f0) ** u
    n = lowpass(rs.standard_normal(len(t)), fc) - lowpass(rs.standard_normal(len(t)), fc * 0.35) * 0.6
    env = (u ** 2.2 if rise else np.sin(np.pi * u) ** 1.5) * np.minimum(1, (1 - u) / 0.04 + 0.0001)
    return norm(n) * env


def pad_note(f, d, att=0.7, rel=0.9, det=0.0):
    t = tt(d); s = np.zeros(len(t))
    for k in range(1, 7):
        for dc in (-4 + det, 4 + det):
            s += np.sin(2 * np.pi * f * k * (1 + dc / 1200 * 1.0) * t + k * 0.7) / (k ** 1.6)
    env = np.minimum(1, t / att) * np.minimum(1, (d - t) / rel)
    return s * np.clip(env, 0, 1)


data = json.load(open('events.json'))
CH = {'I': [50, 57, 64, 66, 69], 'vi': [47, 54, 57, 62, 64], 'IV': [43, 50, 57, 59, 66], 'I2': [50, 57, 64, 66, 69, 74]}
chords = data['chords']
for k, (t0, name) in enumerate(chords):
    t1 = chords[k + 1][0] if k + 1 < len(chords) else DUR
    notes = CH['I2'] if (name == 'I' and k > 0) else CH[name]
    d = t1 - t0 + 1.0
    for j, m in enumerate(notes):
        g = 0.012 if m < 52 else 0.014
        add(pad_note(hz(m), d, att=0.9 if k == 0 else 0.45, det=1.5), max(0, t0 - 0.25), g, pan=(j / (len(notes) - 1) - 0.5) * 0.7, send=0.45)

# air bed
air = norm(lowpass(rs.standard_normal(N), 9000) - lowpass(rs.standard_normal(N), 3500))
tline = np.arange(N) / SR
air *= 0.5 + 0.5 * np.sin(2 * np.pi * 0.11 * tline)
dry[0] += air * 0.006; dry[1] += np.roll(air, 3000) * 0.006

SCALE = [74, 76, 78, 81, 83, 86, 88, 90, 93, 95, 98]
for e in data['ev']:
    k, t = e['k'], e['t']
    if k == 'drip':
        add(bell(hz(98), 0.5, 0.5), t, 0.035, 0.0, 0.6)
    elif k == 'fall':
        add(whoosh(0.5, 2500, 500, rise=False), t, 0.05, 0.0, 0.3)
    elif k == 'land':
        add(plip(420, 1250, 0.16, 0.035), t, 0.22, 0.0, 0.35)
        add(thump(120, 52, 0.4), t, 0.19, 0.0, 0.1)
        add(bell(hz(74), 1.8, 0.7), t + 0.01, 0.05, 0.0, 0.6)
    elif k == 'bead':
        add(plip(700, 1500, 0.10, 0.025), t, 0.12, e.get('pan', 0), 0.45)
    elif k == 'merge':
        add(plip(260, 560, 0.18, 0.05), t, 0.22, e.get('pan', 0), 0.35)
        add(thump(90, 50, 0.3), t, 0.10, e.get('pan', 0), 0.1)
    elif k == 'riser':
        add(whoosh(e['d'], 300, 5000, rise=True), t, 0.06, 0.0, 0.4)
    elif k == 'morph':
        v = e.get('v', 1.0)
        add(thump(95, 45, 0.5), t, 0.20 * v, 0.0, 0.12)
        for j, m in enumerate((74, 81, 86)):
            add(bell(hz(m), 2.2, 0.8), t + j * 0.012, 0.05 * v, (j - 1) * 0.35, 0.6)
    elif k == 'chime':
        for j, m in enumerate((86, 90, 93)):
            add(bell(hz(m), 2.4, 0.9), t + j * 0.07, 0.06, (j - 1) * 0.4, 0.6)
    elif k == 'tap':
        v = e.get('v', 1.0); m = SCALE[e['i'] % len(SCALE)] + (0 if v >= 1 else 12)
        add(bell(hz(m), 0.6, 0.6), t, 0.032 * v, (e['i'] / 10 - 0.35) * 0.8, 0.55)
    elif k == 'pop':
        add(plip(380, 980, 0.12, 0.03), t, 0.20, 0.0, 0.35)
        add(bell(hz(81), 1.4, 0.6), t + 0.02, 0.04, 0.0, 0.6)
    elif k == 'shimmer':
        d = e['d']
        for j in range(14):
            tj = t + d * j / 14 + rs.uniform(0, d / 14)
            add(bell(hz(SCALE[rs.integers(4, len(SCALE))] + 12), 0.4, 0.3), tj, 0.010 + 0.008 * np.sin(np.pi * j / 13), rs.uniform(-0.7, 0.7), 0.7)
        add(whoosh(d, 3000, 9000, rise=False), t, 0.018, 0.0, 0.5)

# synthetic stereo reverb: decaying filtered noise, convolved by FFT
L_ir = int(2.4 * SR); ti = np.arange(L_ir) / SR
irs = []
for ch in range(2):
    n = rs.standard_normal(L_ir) * np.exp(-ti / 0.55)
    n = np.convolve(n, np.ones(6) / 6, mode='same')
    n[:int(0.012 * SR)] = 0
    irs.append(n / np.sqrt((n ** 2).sum()))
M = 1 << int(np.ceil(np.log2(N + L_ir)))
out = np.zeros((2, N))
for ch in range(2):
    rv = np.fft.irfft(np.fft.rfft(wet[ch], M) * np.fft.rfft(irs[ch], M), M)[:N]
    out[ch] = dry[ch] + rv * 0.9

# master: high-pass below ~35 Hz, fade in, fade out with the picture, soft limiter
fr = np.fft.rfftfreq(N, 1 / SR); hp = np.clip((fr - 20) / 25, 0, 1) ** 2
for ch in range(2): out[ch] = np.fft.irfft(np.fft.rfft(out[ch]) * hp, N)
fi = int(0.25 * SR); out[:, :fi] *= np.linspace(0, 1, fi)
f0 = data.get('fadeOut', 9.15)
u = np.clip((tline - f0) / (DUR - 0.03 - f0), 0, 1); out *= 1 - u * u * (3 - 2 * u)
out = np.tanh(out * 1.6) / np.tanh(1.6) * 0.85
pk = np.abs(out).max(); out *= min(1.0, 0.89 / (pk + 1e-9))
pcm = (np.clip(out.T, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok, peak', round(float(np.abs(out).max()), 3))
