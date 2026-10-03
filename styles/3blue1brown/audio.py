# events.json → audio.wav (48 kHz stereo, 10 s), everything synthesised with numpy.
# 3blue1brown: a quiet piano-like pad under the whole clip, a felt pluck for every Write glyph and
# every tick label, a swish for the Creates, a whoosh for the sweep and the camera pan, a soft tone
# whose pitch follows sin θ while the curve is traced, a shimmer for the flash, and a fade-out.
import json
import wave

import numpy as np

SR, DUR = 48000, 10.0
TAU = 2 * np.pi
N = int(SR * DUR)
L = np.zeros(N)
R = np.zeros(N)
rng = np.random.default_rng(3141)


def tt(d):
    return np.arange(int(d * SR)) / SR


def smooth(u):
    u = np.clip(u, 0, 1)
    return u * u * u * (u * (u * 6 - 15) + 10)


def put(sig, t, gain=1.0, pan=0.0):
    """Mix sig into both channels at time t; pan runs from -1 (left) to +1 (right)."""
    i = max(0, int(t * SR))
    n = min(len(sig), N - i)
    if n <= 0:
        return
    L[i:i + n] += sig[:n] * gain * np.sqrt(0.5 - pan / 2) * 1.414
    R[i:i + n] += sig[:n] * gain * np.sqrt(0.5 + pan / 2) * 1.414


def band(x, lo, hi):
    """Brick-wall band-pass by FFT, normalised to unit peak."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    y = np.fft.irfft(X, len(x))
    return y / (np.abs(y).max() + 1e-9)


def pluck(freq, d=1.6, bright=1.0):
    """Felt-piano pluck: a handful of partials with faster decay the higher they sit."""
    t = tt(d)
    out = np.zeros_like(t)
    for k in range(1, 7):
        amp = bright ** (k - 1) / k ** 1.25
        out += amp * np.sin(TAU * freq * k * t) * np.exp(-t * (2.2 + 1.6 * k))
    return out * np.minimum(1, t / 0.004)


def pad_note(freq, d, attack=0.5, release=0.6):
    """A slow, warm pad voice: two detuned sines plus a quiet octave, soft edges."""
    t = tt(d)
    v = (np.sin(TAU * freq * t) + np.sin(TAU * freq * 1.003 * t + 0.7)
         + 0.35 * np.sin(TAU * freq * 2 * t) + 0.12 * np.sin(TAU * freq * 3 * t))
    e = np.minimum(1, t / attack) * np.minimum(1, (d - t) / release)
    return v * np.clip(e, 0, 1) / 2.5


def whoosh(d, lo, hi, peak=0.5):
    """Band-limited noise with a hump envelope that peaks at the given fraction of d."""
    t = tt(d)
    x = band(rng.standard_normal(len(t)), lo, hi)
    e = np.exp(-((t / d - peak) / 0.28) ** 2)
    return x * e


def swish(d, f0, f1):
    """A rising filtered-noise sweep plus a faint sine glide: Create()."""
    t = tt(d)
    parts = 8
    out = np.zeros_like(t)
    for k in range(parts):
        a, b = k / parts, (k + 1) / parts
        seg = (t / d >= a) & (t / d < b)
        c = f0 * (f1 / f0) ** ((a + b) / 2)
        x = band(rng.standard_normal(len(t)), c * 0.7, c * 1.4)
        out += x * seg
    e = np.sin(np.pi * t / d) ** 0.7
    glide = np.sin(TAU * np.cumsum(f0 / 4 * (f1 / f0) ** (t / d)) / SR) * 0.35
    return (out * 0.8 + glide) * e


def note(name):
    names = {'C': -9, 'D': -7, 'E': -5, 'F': -4, 'G': -2, 'A': 0, 'B': 2}
    n = names[name[0]] + 12 * (int(name[-1]) - 4)
    if '#' in name:
        n += 1
    return 440.0 * 2 ** (n / 12)


ev = json.load(open('events.json'))
by = {}
for e in ev:
    by.setdefault(e['k'], []).append(e)

# --- the pad: four chords, crossfaded at the scene beats ---------------------------------------
beats = [0.0, by['spin'][0]['t'], by['pan'][0]['t'], by['trace'][0]['t'], by['flash'][0]['t'], DUR + 1]
chords = [['A2', 'E3', 'A3', 'C4', 'E4'], ['F2', 'C3', 'F3', 'A3', 'C4'],
          ['C3', 'G3', 'C4', 'E4', 'G4'], ['G2', 'D3', 'G3', 'B3', 'D4'], ['A2', 'E3', 'A3', 'C4', 'E4']]
for i, ch in enumerate(chords):
    t0, t1 = beats[i], min(beats[i + 1] + 0.5, DUR)
    for j, n in enumerate(ch):
        put(pad_note(note(n), t1 - t0, attack=0.9 if i else 1.6, release=0.7), t0,
            0.030 / (1 + 0.25 * j), pan=(j - 2) * 0.15)

# --- cues --------------------------------------------------------------------------------------
t = tt(1.2)
plane_swell = (np.sin(TAU * 110 * t) * np.minimum(1, t / 0.7) * np.minimum(1, (1.2 - t) / 0.3)
               + 0.5 * band(rng.standard_normal(len(t)), 200, 1200) * np.sin(np.pi * t / 1.2))
put(plane_swell, by['plane'][0]['t'], 0.08)

for e in by.get('circle', []):
    put(swish(e['d'], 500, 2400), e['t'], 0.10, pan=-0.1)

scale = ['A4', 'C5', 'D5', 'E5', 'G5', 'A5', 'C6']
for e in by.get('glyph', []):
    step = int(round(e['v'] * (len(scale) - 1)))
    put(pluck(note(scale[step]), 1.4, 0.8), e['t'], 0.10, pan=-0.3 + 0.6 * e['v'])

for e in by.get('pop', []):
    t = tt(0.12)
    f = 320 * 2 ** (np.minimum(t / 0.06, 1) * 1.0)
    put(np.sin(TAU * np.cumsum(f) / SR) * np.exp(-t * 28) * np.minimum(1, t / 0.002), e['t'], 0.16)

for e in by.get('spin', []):
    d = e['d']
    t = tt(d)
    # the whoosh follows the angular speed of the smooth sweep: silent at both ends, loud mid-way
    u = t / d
    speed = 30 * u * u * (1 - u) * (1 - u)
    x = band(rng.standard_normal(len(t)), 250, 1800)
    put(x * speed ** 1.5 * 0.5, e['t'], 0.07)
    put(np.sin(TAU * np.cumsum(220 + 180 * speed) / SR) * speed * 0.4, e['t'], 0.05)

for e in by.get('show', []):
    put(pluck(note('E5'), 0.9, 0.6), e['t'], 0.05, pan=0.2)

for e in by.get('pan', []):
    put(whoosh(e['d'], 150, 1400, peak=0.45), e['t'], 0.09, pan=-0.3)

for e in by.get('move', []):
    put(whoosh(e['d'], 900, 4000, peak=0.5), e['t'], 0.035, pan=0.2)
    put(pluck(note('E5'), 1.2, 0.7), e['t'] + e['d'], 0.07, pan=0.3)

for e in by.get('axis', []):
    t = tt(e['d'])
    scratch = band(rng.standard_normal(len(t)), 1500, 6000) * (0.6 + 0.4 * np.sin(TAU * 11 * t))
    put(scratch * np.sin(np.pi * t / e['d']) ** 0.8, e['t'], 0.035, pan=0.4)

tick_notes = ['D5', 'E5', 'G5', 'A5']
for i, e in enumerate(by.get('tick', [])):
    put(pluck(note(tick_notes[i % 4]), 1.2, 0.7), e['t'], 0.06, pan=0.15 + 0.2 * e['v'])

for e in by.get('trace', []):
    d = e['d']
    t = tt(d + 0.4)
    u = np.clip(t / d, 0, 1)
    theta = TAU * (0.72 * u + 0.28 * smooth(u))
    f = note('D4') * 2 ** (0.75 * np.sin(theta))
    ph = TAU * np.cumsum(f) / SR
    tone = np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    env = np.minimum(1, t / 0.25) * np.clip((d + 0.4 - t) / 0.4, 0, 1)
    put(tone * env, e['t'], 0.075, pan=0.35)

for e in by.get('flash', []):
    t = tt(e['d'] + 0.6)
    bell = sum(np.sin(TAU * f * t) * np.exp(-t * k) for f, k in ((1760, 4), (2637, 5), (3520, 7)))
    sparkle = band(rng.standard_normal(len(t)), 5000, 12000) * np.exp(-t * 6)
    put((bell * 0.5 + sparkle * 0.5) * np.minimum(1, t / 0.01), e['t'], 0.05, pan=0.3)
    put(pluck(note('A5'), 1.5, 0.6), e['t'], 0.06, pan=0.2)

# --- master: edge fades, the closing fade-out, gentle soft-clip -------------------------------
end = by['end'][0]
fi = int(0.02 * SR)
fo_start = int(end['t'] * SR)
for ch in (L, R):
    ch[:fi] *= np.linspace(0, 1, fi)
    ch[fo_start:] *= np.clip(1 - (np.arange(N - fo_start) / SR) / end['d'], 0, 1)
mix = np.stack([L, R], 1)
mix = np.tanh(mix * 2.4) * 0.85
pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('audio.wav ok, peak', round(float(np.abs(mix).max()), 3))
