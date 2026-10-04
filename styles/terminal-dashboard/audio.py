# events.json -> audio.wav (48 kHz stereo, 10.4 s), every sound synthesised here with numpy.
# Calm and sober: a quiet low pad with a breath of air under the whole film; a mechanical click per typed
# key (Enter heavier); soft staggered blips as the panels draw; a very quiet tick per log line, panned by
# where the line ends; state cues (passed: a soft high blip, rerouted: a two-note dip and lift, stopped:
# a low dull blip); a soft digital thunk on each layout switch; a rising sine glide under each growing
# cost bar; and a warm chord under the banner that rings into the fade.
import json
import wave

import numpy as np

RATE, LENGTH = 48000, 10.4
NS = int(RATE * LENGTH)
DRY = np.zeros((2, NS))
SEND = np.zeros((2, NS))
TIME = np.arange(NS) / RATE
CUES = json.load(open('events.json'))


def cues(kind):
    return [c for c in CUES if c['k'] == kind]


def midi(m):
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def clock(d):
    return np.arange(max(1, int(d * RATE))) / RATE


def ramp(x, a, b):
    """0 before a, 1 after b, a raised-cosine step between."""
    u = np.clip((x - a) / max(b - a, 1e-9), 0.0, 1.0)
    return 0.5 - 0.5 * np.cos(np.pi * u)


def norm(x):
    peak = np.max(np.abs(x))
    return x / peak if peak > 0 else x


def mix_in(sig, at, gain, pan=0.0, send=0.1):
    """Add a mono voice at `at` seconds. Pan is clamped to [-1, 1] and mapped with a constant-power law."""
    pan = float(np.clip(np.nan_to_num(pan), -1.0, 1.0))
    start = int(round(at * RATE))
    if start < 0:
        sig, start = sig[-start:], 0
    n = min(len(sig), NS - start)
    if n <= 0:
        return
    a = (pan + 1.0) * np.pi / 4.0
    v = sig[:n] * gain
    for ch, k in ((0, np.cos(a)), (1, np.sin(a))):
        DRY[ch, start:start + n] += v * k * np.sqrt(2.0)
        SEND[ch, start:start + n] += v * k * np.sqrt(2.0) * send


def tone_filter(x, low=None, high=None, slope=6.0):
    """Spectral band shaping: logistic roll-offs in octaves below `low` and above `high`."""
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1.0 / RATE)
    oct_ = np.log2(np.maximum(f, 1.0))
    gain = np.ones_like(f)
    if low:
        gain *= 1.0 / (1.0 + np.exp(-slope * (oct_ - np.log2(low))))
    if high:
        gain *= 1.0 / (1.0 + np.exp(slope * (oct_ - np.log2(high))))
    return np.fft.irfft(spec * gain, len(x))


def hiss(n, seed):
    return np.random.default_rng(seed).uniform(-1.0, 1.0, n)


def sweep_phase(freq):
    return 2.0 * np.pi * np.cumsum(freq) / RATE


# ── voices ──────────────────────────────────────────────────────────────────────────────────────
def key_click(seed, heavy=False):
    """A mechanical switch: a bright snap, a short plastic body resonance, and for Enter a low bottom-out."""
    rng = np.random.default_rng(seed)
    x = clock(0.16 if heavy else 0.07)
    snap = tone_filter(hiss(len(x), seed), 2500, 11000) * np.exp(-x / 0.0025)
    body_f = rng.uniform(1700, 2300) * (0.75 if heavy else 1.0)
    body = np.sin(2 * np.pi * body_f * x + rng.uniform(0, 6)) * np.exp(-x / 0.009) * 0.45
    out = snap + body
    if heavy:
        out += np.sin(sweep_phase(110 + 140 * np.exp(-x / 0.012))) * np.exp(-x / 0.045) * 0.9
        out += tone_filter(hiss(len(x), seed + 9), 300, 2500) * np.exp(-x / 0.02) * 0.3
    return norm(out) * ramp(x, 0, 0.0008)


def blip(freq, dur=0.12, seed=0):
    x = clock(dur)
    s = np.sin(2 * np.pi * freq * x) + 0.18 * np.sin(2 * np.pi * freq * 2.01 * x)
    return norm(s) * ramp(x, 0, 0.003) * np.exp(-x / (dur * 0.32))


def log_tick(seed):
    x = clock(0.03)
    s = 0.6 * np.sin(2 * np.pi * 4200 * x) + tone_filter(hiss(len(x), seed), 3000, 9000)
    return norm(s) * np.exp(-x / 0.004)


def passed_cue():
    return blip(midi(91), 0.18) * 0.7 + np.pad(blip(midi(98), 0.16), (int(0.05 * RATE), 0))[:int(0.18 * RATE)] * 0.45


def reroute_cue():
    """Two notes: the first sags a whole tone, the second lifts a fourth above where it began."""
    d = 0.11
    x = clock(d)
    f1 = midi(81) * 2 ** (-2 / 12 * ramp(x, 0, d))
    n1 = np.sin(sweep_phase(f1)) * ramp(x, 0, 0.004) * np.exp(-x / 0.06)
    n2 = blip(midi(86), 0.2)
    out = np.zeros(int(0.32 * RATE))
    out[:len(n1)] += n1
    j = int(0.12 * RATE)
    out[j:j + len(n2)] += n2[:len(out) - j]
    return norm(out)


def stopped_cue():
    x = clock(0.26)
    s = np.sin(2 * np.pi * midi(52) * x) + 0.3 * np.sin(2 * np.pi * midi(52) * 3 * x) * np.exp(-x / 0.02)
    return norm(tone_filter(s, None, 900, 4.0)) * ramp(x, 0, 0.004) * np.exp(-x / 0.07)


def thunk(seed):
    """A soft digital thunk: a dropping sine, a muted click and a puff of low noise."""
    x = clock(0.22)
    body = np.sin(sweep_phase(70 + 160 * np.exp(-x / 0.018))) * np.exp(-x / 0.07)
    click = tone_filter(hiss(len(x), seed), 1200, 5000) * np.exp(-x / 0.003) * 0.25
    puff = tone_filter(hiss(len(x), seed + 1), 150, 900) * np.exp(-x / 0.03) * 0.3
    return norm(body + click + puff) * ramp(x, 0, 0.001)


def glide(d, m0, m1):
    """A rising sine glide with a quiet octave, eased like the bar it sits under, ending softly."""
    x = clock(d + 0.12)
    u = np.clip(x / d, 0, 1)
    f = midi(m0) * (midi(m1) / midi(m0)) ** (1 - (1 - u) ** 3)
    ph = sweep_phase(f)
    s = np.sin(ph) + 0.22 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    return norm(s) * ramp(x, 0, 0.03) * (1 - ramp(x, d - 0.02, d + 0.12))


def pad_voice(m, d, seed, detune=0.004):
    """Three slightly detuned sines with a slow beat; soft and round."""
    rng = np.random.default_rng(seed)
    x = clock(d)
    f = midi(m)
    s = sum(np.sin(2 * np.pi * f * (1 + k * detune) * x + rng.uniform(0, 6)) for k in (-1, 0, 1))
    s += 0.12 * np.sin(2 * np.pi * 2 * f * x + rng.uniform(0, 6))
    return s / 3.0


def warm_note(m, d, seed):
    """A warm electric-piano-like note: a few harmonics that soften as it rings."""
    rng = np.random.default_rng(seed)
    x = clock(d)
    f = midi(m)
    s = np.zeros(len(x))
    for h, (amp, tau) in enumerate(((1.0, 3.5), (0.35, 1.2), (0.12, 0.5), (0.05, 0.25)), start=1):
        s += amp * np.sin(2 * np.pi * f * h * x + rng.uniform(0, 6)) * np.exp(-x / tau)
    return norm(s) * ramp(x, 0, 0.012)


# ── the bed: a low pad (D, A, E, A) and a breath of air, swelling in and out with the picture ──
bed = cues('bed')[0]
env = ramp(TIME, bed['t'], bed['t'] + 1.6) * (1 - ramp(TIME, bed['end'] - 0.8, bed['end']))
swell = 0.85 + 0.15 * np.sin(2 * np.pi * TIME / 7.0 - 1.2)
pad = sum(pad_voice(m, LENGTH, 30 + i) * a for i, (m, a) in enumerate(((38, 1.0), (45, 0.7), (52, 0.45), (57, 0.3))))
pad = tone_filter(pad, 40, 1400, 3.0)
air = tone_filter(hiss(NS, 7), 1500, 7000, 2.0) * 0.03
for ch, ph in ((0, 0.0), (1, 1.7)):
    wob = 1 + 0.08 * np.sin(2 * np.pi * TIME / 3.3 + ph)
    DRY[ch] += (pad * 0.045 + air * wob) * env * swell
    SEND[ch] += pad * 0.015 * env

# ── keys ──
for i, c in enumerate(cues('key')):
    mix_in(key_click(100 + i), c['t'], 0.2 * (0.85 + 0.3 * np.random.default_rng(i).random()), c['p'], 0.05)
for c in cues('enter'):
    mix_in(key_click(190, heavy=True), c['t'], 0.32, c['p'], 0.08)

# ── the screen drawing ──
for i, c in enumerate(cues('blip')):
    mix_in(blip(midi(c['m']), 0.1), c['t'], 0.07, c['p'], 0.25)
for i, c in enumerate(cues('tick')):
    mix_in(log_tick(300 + i), c['t'], 0.045, c['p'], 0.1)
for c in cues('pass'):
    mix_in(passed_cue(), c['t'], 0.08, c['p'], 0.3)
for c in cues('reroute'):
    mix_in(reroute_cue(), c['t'], 0.1, c['p'], 0.3)
for c in cues('stop'):
    mix_in(stopped_cue(), c['t'], 0.16, c['p'], 0.2)
for i, c in enumerate(cues('thunk')):
    mix_in(thunk(400 + i), c['t'], 0.3, 0.0, 0.15)
for c in cues('glide'):
    mix_in(glide(c['d'], c['m0'], c['m1']), c['t'], 0.07, c['p'], 0.35)

# ── the banner chord: D major add 9 and 6, rolled, ringing into the fade ──
for c in cues('chord'):
    for j, m in enumerate((50, 57, 62, 66, 69, 71, 76)):
        mix_in(warm_note(m, LENGTH - c['t'], 500 + j), c['t'] + 0.022 * j, 0.06 if j else 0.075, -0.5 + j / 6.0, 0.45)


# ── a small soft room on the send, master fade, peak normalised under -1 dBFS ──
def room(seed, d=1.6):
    x = clock(d)
    taps = hiss(len(x), seed) * np.exp(-x / 0.35)
    ir = tone_filter(taps, 200, 5000, 3.0) * ramp(x, 0, 0.006)
    return ir / np.sqrt(np.sum(ir ** 2))


def fft_convolve(a, b):
    n = 1 << int(np.ceil(np.log2(len(a) + len(b))))
    return np.fft.irfft(np.fft.rfft(a, n) * np.fft.rfft(b, n), n)[:len(a)]


out = DRY + 0.4 * np.stack([fft_convolve(SEND[0], room(21)), fft_convolve(SEND[1], room(22))])
fade = cues('fade')[0]
out *= (ramp(TIME, 0, 0.02) * (1 - ramp(TIME, fade['t'], LENGTH - 0.01)))[None, :]
out = np.nan_to_num(out)
out *= 10 ** (-1.5 / 20) / (np.max(np.abs(out)) + 1e-12)
pcm = (np.clip(out.T, -1.0, 1.0) * 32767).astype('<i2')
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(RATE)
    w.writeframes(pcm.tobytes())
