# events.json -> audio.wav (48 kHz stereo, 10.0 s), synthesised here with numpy; no samples, no beat.
# A quiet room: a low bed of filtered air under everything. Paper burnish as each tone group lays in, a wire
# creak as the crow crouches, a soft whoosh on each downstroke and a low hum while the wire wobbles; a paper
# swell through the ink and again through the paper; cloth fluttering with the breeze on the balcony; at dusk
# a warm two-sine drone, one glockenspiel note as the title lands and a felt marker for the swipe. The whole
# mix is set to about -18 LUFS with its true peak under -1 dBFS and falls to silence by the last frame.
import json
import wave

import numpy as np

SR, DUR = 48000, 10.0
N = int(SR * DUR)
T = np.arange(N) / SR
DRY = np.zeros((2, N))
SEND = np.zeros((2, N))
cues = json.load(open('events.json'))


def cue(kind):
    return [c for c in cues if c['k'] == kind]


def seconds(d):
    return np.arange(max(1, int(round(d * SR)))) / SR


def smoothstep(a, b, x):
    k = np.clip((x - a) / (b - a), 0.0, 1.0)
    return k * k * (3 - 2 * k)


def normed(x):
    return x / (np.max(np.abs(x)) + 1e-12)


def hiss(n, seed):
    return np.random.default_rng(seed).standard_normal(n)


def bandpass(x, lo=None, hi=None, slope=2):
    """Shape a signal's spectrum with gentle Butterworth-like skirts (zero phase, via the FFT)."""
    spec = np.fft.rfft(x)
    f = np.maximum(np.fft.rfftfreq(len(x), 1 / SR), 1e-3)
    gain = np.ones_like(f)
    if lo:
        gain *= 1 / np.sqrt(1 + (lo / f) ** (2 * slope))
    if hi:
        gain *= 1 / np.sqrt(1 + (f / hi) ** (2 * slope))
    return np.fft.irfft(spec * gain, len(x))


def mix_in(sig, at, gain, pan=0.0, wet=0.2):
    """Add a mono voice at `at` seconds, equal-power panned (-1 left .. 1 right), with some of it sent to the room."""
    start = int(round(at * SR))
    if start < 0:
        sig, start = sig[-start:], 0
    n = min(len(sig), N - start)
    if n <= 0:
        return
    angle = (np.clip(pan, -1, 1) + 1) * np.pi / 4
    for ch, g in enumerate((np.cos(angle), np.sin(angle))):
        DRY[ch, start:start + n] += sig[:n] * gain * g * np.sqrt(2)
        SEND[ch, start:start + n] += sig[:n] * gain * g * np.sqrt(2) * wet


def grain_rub(n, seed, rate=(18, 46)):
    """A slow random tremble, like a burnisher catching on the tooth of the paper."""
    r = np.random.default_rng(seed)
    out = np.zeros(n)
    i = 0
    while i < n:
        w = int(SR / r.uniform(*rate))
        out[i:i + w] += r.uniform(0.35, 1.0) * np.hanning(min(w, n - i))
        i += int(w * r.uniform(0.45, 0.8))
    return out


# ---- voices
def burnish(d, seed, bright=1.0, rising=True):
    x = seconds(d + 0.08)
    body = bandpass(hiss(len(x), seed), 1400 * bright, 6500 * bright)
    env = smoothstep(0, 0.05, x) * (1 - smoothstep(d * 0.55, d + 0.08, x))
    if not rising:
        env = env[::-1]
    return normed(body * (0.35 + grain_rub(len(x), seed + 1))) * env


def creak(d, seed):
    x = seconds(d)
    tone = np.sin(2 * np.pi * (210 + 30 * x / d) * x) * 0.4 + bandpass(hiss(len(x), seed), 300, 1100)
    return normed(tone * grain_rub(len(x), seed + 2, (9, 20))) * np.sin(np.pi * x / d) ** 2


def whoosh(d, seed):
    """Air pushed by a wing: noise in a band sweeping up, a soft low push under it."""
    x = seconds(d + 0.12)
    src = hiss(len(x), seed)
    lo = bandpass(src, 350, 1100)
    hi = bandpass(src, 1100, 3200)
    k = np.clip(x / (d + 0.12), 0, 1)
    air = lo * (1 - k) + hi * k * 0.6
    push = np.sin(2 * np.pi * 95 * x) * np.exp(-x / 0.05) * 0.5
    env = smoothstep(0, 0.035, x) * np.exp(-np.maximum(0, x - 0.04) / (d * 0.55))
    return normed(air + push) * env


def thrum(d, hz, seed):
    """The wire's low hum, pulsing with its wobble and dying with it."""
    x = seconds(d)
    wobble = np.abs(np.cos(2 * np.pi * hz * x)) * np.exp(-x / 0.42)
    tone = np.sin(2 * np.pi * 62 * x) + 0.35 * np.sin(2 * np.pi * 124 * x + 0.4) + 0.12 * bandpass(hiss(len(x), seed), 80, 260)
    return normed(tone) * wobble * smoothstep(0, 0.01, x)


def swell(d, seed, dark):
    x = seconds(d + 0.45)
    lo, hi = (260, 2400) if dark else (1100, 7600)
    body = bandpass(hiss(len(x), seed), lo, hi)
    env = smoothstep(0, d * 0.7, x) * (1 - smoothstep(d * 0.7, d + 0.45, x))
    return normed(body * (0.6 + 0.4 * grain_rub(len(x), seed + 3, (6, 14)))) * env


def bell(seed):
    """One soft glockenspiel bar: a bright fundamental with the bar's stretched overtones dying fast."""
    x = seconds(2.4)
    f0 = 1318.5                                   # E6
    tone = (np.sin(2 * np.pi * f0 * x) * np.exp(-x / 0.9)
            + 0.32 * np.sin(2 * np.pi * f0 * 2.76 * x + 0.7) * np.exp(-x / 0.22)
            + 0.12 * np.sin(2 * np.pi * f0 * 5.40 * x + 1.9) * np.exp(-x / 0.08)
            + 0.22 * np.sin(2 * np.pi * f0 / 2 * x) * np.exp(-x / 1.3))
    knock = bandpass(hiss(len(x), seed), 2500, 9000) * np.exp(-x / 0.004) * 0.06
    return normed(tone + knock) * smoothstep(0, 0.003, x)


def marker(d, seed):
    """A felt tip dragged across paper: a soft, steady fsss with a little drag in it."""
    x = seconds(d + 0.06)
    body = bandpass(hiss(len(x), seed), 2200, 7000)
    drag = 0.75 + 0.25 * grain_rub(len(x), seed + 4, (30, 70))
    env = smoothstep(0, 0.03, x) * (1 - smoothstep(d - 0.02, d + 0.06, x))
    return normed(body * drag) * env


# ---- the bed: a low, slowly breathing air under everything
bed = cue('bed')[0]
air = np.stack([bandpass(hiss(N, 11), 30, 240), bandpass(hiss(N, 12), 30, 240)])
air += 0.35 * np.stack([bandpass(hiss(N, 13), 240, 900), bandpass(hiss(N, 14), 240, 900)])
air /= np.max(np.abs(air)) + 1e-12
breathe = 0.8 + 0.2 * np.sin(2 * np.pi * 0.17 * T + 0.5)
DRY += air * breathe * 0.07 * smoothstep(0, 0.6, T)

# ---- the lane
for i, c in enumerate(cue('lay')):
    mix_in(burnish(c['d'], 100 + i, 1.0 if c['t'] < 5 else 0.85), c['t'], 0.16 * c['v'], c['p'], 0.25)
for c in cue('creak'):
    mix_in(creak(c['d'], 200), c['t'], 0.05, c['p'], 0.2)
for i, c in enumerate(cue('wing')):
    mix_in(whoosh(c['d'], 300 + i), c['t'], 0.24 * c['v'], c['p'], 0.3)
for c in cue('thrum'):
    mix_in(thrum(c['d'], c['hz'], 400), c['t'], 0.1, c['p'], 0.15)

# ---- the transitions and the balcony
for i, c in enumerate(cue('swell')):
    mix_in(swell(c['d'], 500 + i, c['dark']), c['t'] - 0.1, 0.17 if c['dark'] else 0.12, 0.0, 0.35)
for c in cue('cloth'):
    env = np.interp(T, c['t'] + np.arange(len(c['env'])) / c['rate'], c['env'], left=0, right=0)
    flap = 0.55 + 0.45 * grain_rub(N, 610, (7, 13))
    for ch, seed in ((0, 620), (1, 621)):
        cloth = bandpass(hiss(N, seed), 220, 2600)
        cloth /= np.max(np.abs(cloth)) + 1e-12
        DRY[ch] += cloth * flap * env * 0.11 * smoothstep(c['t'], c['t'] + 0.25, T)

# ---- dusk: the drone, the bell, the marker, the tones going home
drone = cue('drone')[0]
x = T - drone['t']
hum = (np.sin(2 * np.pi * 73.42 * T) + 0.8 * np.sin(2 * np.pi * 110.0 * T + 0.6)
       + 0.18 * np.sin(2 * np.pi * 146.83 * T + 1.1) + 0.1 * np.sin(2 * np.pi * 220.4 * T))
hum *= (0.85 + 0.15 * np.sin(2 * np.pi * 0.31 * T)) * smoothstep(0, 1.1, x) * (x > 0)
DRY += np.stack([hum, np.roll(hum, 96)]) * 0.035
for c in cue('bell'):
    mix_in(bell(700), c['t'], 0.11, c['p'], 0.5)
for c in cue('marker'):
    m = marker(c['d'], 800)
    pans = np.linspace(c['p0'], c['p1'], len(m))
    start = int(round(c['t'] * SR))
    angle = (pans + 1) * np.pi / 4
    n = min(len(m), N - start)
    for ch, g in enumerate((np.cos(angle), np.sin(angle))):
        DRY[ch, start:start + n] += (m * g * np.sqrt(2) * 0.13)[:n]
        SEND[ch, start:start + n] += (m * g * np.sqrt(2) * 0.13 * 0.2)[:n]
for c in cue('unlay'):
    mix_in(burnish(c['d'], 900, 0.8, rising=False), c['t'], 0.1, 0.0, 0.4)


# ---- a small room on the send
def room(seed, d=1.2):
    x = seconds(d)
    ir = hiss(len(x), seed) * np.exp(-x / 0.28) * smoothstep(0, 0.012, x)
    ir = bandpass(ir, 120, 5000)
    return ir / np.sqrt(np.sum(ir ** 2))


def convolve(sig, ir):
    n = 1 << int(np.ceil(np.log2(len(sig) + len(ir))))
    return np.fft.irfft(np.fft.rfft(sig, n) * np.fft.rfft(ir, n), n)[:len(sig)]


out = DRY + 0.3 * np.stack([convolve(SEND[0], room(31)), convolve(SEND[1], room(32))])

# ---- everything falls away to silence by the last frame; 10 ms fades at both ends
fade = cue('fade')[0]
k = np.clip((T - fade['t']) / (fade['end'] - 0.04 - fade['t']), 0, 1)
out *= (0.5 + 0.5 * np.cos(np.pi * k)) ** 1.5
out *= smoothstep(0, 0.01, T) * (1 - smoothstep(DUR - 0.01, DUR, T))
out = np.nan_to_num(out)


# ---- loudness: BS.1770 K-weighting in the frequency domain, gated blocks, then a true-peak check
def biquad_response(b, a, w):
    z = np.exp(-1j * w)
    return (b[0] + b[1] * z + b[2] * z * z) / (a[0] + a[1] * z + a[2] * z * z)


def k_weight(sig):
    w = 2 * np.pi * np.fft.rfftfreq(len(sig), 1 / SR) / SR
    shelf = biquad_response([1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585], w)
    high = biquad_response([1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621], w)
    return np.fft.irfft(np.fft.rfft(sig) * shelf * high, len(sig))


def lufs(st):
    weighted = np.stack([k_weight(c) for c in st])
    block, hop = int(0.4 * SR), int(0.1 * SR)
    power = np.array([np.sum(np.mean(weighted[:, i:i + block] ** 2, axis=1)) for i in range(0, N - block + 1, hop)])
    loud = -0.691 + 10 * np.log10(power + 1e-20)
    gated = power[loud > -70]
    rel = -0.691 + 10 * np.log10(np.mean(gated)) - 10
    return -0.691 + 10 * np.log10(np.mean(power[(loud > -70) & (loud > rel)]))


def true_peak(st):
    return max(np.max(np.abs(np.fft.irfft(np.fft.rfft(c), 4 * len(c)))) * 4 for c in st)


TARGET = -18.0
out *= 10 ** ((TARGET - lufs(out)) / 20)
ceiling = 10 ** (-1.6 / 20)
if true_peak(out) > ceiling:
    # a slow, look-ahead gain ride on the few peaks that would cross the ceiling, then level again
    need = np.minimum(1.0, ceiling / np.maximum(np.max(np.abs(out), axis=0), 1e-9))
    win = int(0.012 * SR)
    held = np.array([np.min(need[max(0, i - win):i + 2 * win]) for i in range(0, N, win)])
    out *= np.interp(np.arange(N), np.arange(0, N, win), held)
    out *= min(1.0, ceiling / true_peak(out))
print(f'audio: {lufs(out):.1f} LUFS, true peak {20 * np.log10(true_peak(out)):.1f} dBFS')
pcm = (np.clip(out.T, -1, 1) * 32767).astype('<i2')
with wave.open('audio.wav', 'wb') as f:
    f.setnchannels(2)
    f.setsampwidth(2)
    f.setframerate(SR)
    f.writeframes(pcm.tobytes())
