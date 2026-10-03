"""events.json -> audio.wav (48 kHz stereo, 10 s). Everything is synthesised; nothing is sampled.

A slow glass pad in D (it opens up when the wordmark lands) under small liquid and glass sounds
cued by the picture: a whoosh and a water-drop "bloop" as the bead glides in and lands, two
bloops as it splits, a gulp as the three melt into the switch, a rising three-note glass
arpeggio as the lens selects Focus, Flow and Rest, bubbles as the switch pours into the
wordmark, a bell chord on the title and a shimmer for the glint.
"""
import json
import wave

import numpy as np

SR, DUR = 48000, 10.0
N = int(SR * DUR)
rng = np.random.default_rng(183)
dry = np.zeros((N, 2))
wet = np.zeros((N, 2))          # reverb send


def tt(d):
    return np.arange(int(d * SR)) / SR


def note(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def put(sig, t, gain=1.0, pan=0.0, send=0.3):
    """Mix a mono signal in at time t. pan: -1 left .. 1 right (a number, or one value per sample)."""
    i = int(round(t * SR))
    if i >= N or i + len(sig) <= 0:
        return
    j = max(0, -i)
    i = max(0, i)
    n = min(len(sig) - j, N - i)
    pan = np.broadcast_to(np.asarray(pan, float), sig.shape)[j:j + n]
    stereo = sig[j:j + n, None] * gain * np.stack([np.sqrt(0.5 - pan / 2), np.sqrt(0.5 + pan / 2)], 1) * 1.414
    dry[i:i + n] += stereo
    wet[i:i + n] += stereo * send


def band(x, lo, hi):
    """Brick-wall band-pass by FFT, with soft shoulders."""
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    spec *= np.clip((f - lo) / (0.25 * lo + 1), 0, 1) * np.clip((hi - f) / (0.25 * hi), 0, 1)
    return np.fft.irfft(spec, len(x))


def noise(d, lo, hi):
    x = band(rng.standard_normal(int(d * SR)), lo, hi)
    return x / (np.abs(x).max() + 1e-9)


def bloop(f0, f1, d=0.16, rise=0.05):
    """Water drop: a sine whose pitch flicks from f0 to f1, then rings briefly."""
    t = tt(d)
    f = f0 + (f1 - f0) * (1 - np.exp(-t / rise))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (d * 0.3)) * np.minimum(1, t / 0.003)


def glass(f, d=1.6, bright=1.0):
    """Struck glass: a few inharmonic partials, the high ones dying first."""
    t = tt(d)
    out = np.zeros_like(t)
    for ratio, amp, decay in ((1, 1, 0.42), (2.76, 0.42 * bright, 0.16), (5.4, 0.2 * bright, 0.07), (8.9, 0.1 * bright, 0.035)):
        if f * ratio < SR / 2.2:
            out += amp * np.sin(2 * np.pi * f * ratio * t + ratio) * np.exp(-t / (d * decay))
    return out * np.minimum(1, t / 0.002)


def whoosh(d, lo, hi, peak=0.5):
    """Air moving past: band-passed noise that swells to `peak` of its length and falls away."""
    t = tt(d) / d
    env = np.where(t < peak, (t / peak) ** 2, ((1 - t) / (1 - peak)) ** 1.5)
    return noise(d, lo, hi) * env


events = json.load(open('events.json'))
when = {e['k']: e['t'] for e in events}          # first cue of each kind is overwritten by later ones; fine for one-offs
t_title, t_fade = when['title'], when['fade']
time = np.arange(N) / SR

# ---- pad: detuned sines on a D major add-9 chord; upper voices arrive with the wordmark ----
swell = np.clip(time / 1.6, 0, 1) ** 1.5
opened = np.clip((time - (t_title - 0.5)) / 1.2, 0, 1)
for midi, gain, late in ((38, 0.5, 0), (45, 0.36, 0), (50, 0.3, 0), (54, 0.22, 0), (57, 0.18, 0), (64, 0.12, 0),
                         (66, 0.13, 1), (69, 0.11, 1), (76, 0.07, 1)):
    env = swell * (opened if late else 0.75 + 0.25 * opened)
    for k, (detune, phase) in enumerate(((-0.07, 0.4), (0.06, 2.1))):
        f = note(midi + detune)
        breath = 1 + 0.22 * np.sin(2 * np.pi * (0.09 + 0.013 * (midi % 7)) * time + midi + k)
        voice = np.sin(2 * np.pi * f * time + phase) * gain * 0.06 * env * breath
        dry[:, k] += voice
        wet[:, k] += voice * 0.5
# a thread of air high above it, like the curtains themselves
air = noise(DUR, 3500, 9000) * 0.012 * swell * (1 + 0.5 * np.sin(2 * np.pi * 0.17 * time))
air2 = noise(DUR, 3500, 9000) * 0.012 * swell * (1 + 0.5 * np.sin(2 * np.pi * 0.13 * time + 1))
dry[:, 0] += air
dry[:, 1] += air2

# ---- cues ----
ARPEGGIO = (74, 78, 81)                           # D5, F#5, A5: one note per mode
slides = 0
for e in events:
    k, t = e['k'], e['t']
    if k == 'glide':
        sig = whoosh(e['d'], 500, 4200, 0.7)
        put(sig, t, 0.13, np.linspace(-0.9, 0.0, len(sig)), 0.4)
    elif k == 'land':
        put(bloop(300, 880), t, 0.3, 0.0, 0.5)
        put(glass(note(86), 1.2, 0.6), t + 0.02, 0.05, 0.1, 0.9)
    elif k == 'split':
        put(bloop(520, 260, 0.2, 0.08), t, 0.22, 0.0, 0.4)           # the stretch before the beads part
    elif k == 'bead':
        pan = -0.6 if e['i'] == 0 else 0.6
        put(bloop(420 + 120 * e['i'], 1150 + 250 * e['i'], 0.14, 0.035), t, 0.2, pan, 0.5)
        put(glass(note(81 + 5 * e['i']), 1.0, 0.5), t, 0.035, pan, 0.9)
    elif k == 'merge':
        put(bloop(700, 240, 0.3, 0.1), t, 0.26, 0.0, 0.4)
        d = tt(0.5)
        put(np.sin(2 * np.pi * np.cumsum(48 + 60 * np.exp(-d * 14)) / SR) * np.exp(-d / 0.16), t + 0.05, 0.3, 0.0, 0.1)
        put(whoosh(0.4, 400, 3000, 0.4), t, 0.07, 0.0, 0.4)
    elif k == 'label':
        d = tt(0.05)
        put(np.sin(2 * np.pi * note(93 + 2 * e['i']) * d) * np.exp(-d / 0.012), t + 0.1, 0.03, (e['i'] - 1) * 0.6, 0.6)
    elif k == 'select':
        pan = (e['i'] - 1) * 0.55
        put(glass(note(ARPEGGIO[e['i']]), 1.8), t, 0.11, pan, 0.8)
        put(glass(note(ARPEGGIO[e['i']] - 12), 1.4, 0.3), t, 0.05, pan, 0.6)
        put(bloop(500, 900, 0.09, 0.03), t, 0.07, pan, 0.3)
    elif k == 'slide':
        sig = whoosh(0.36, 900, 6000, 0.55)
        start = -0.55 + 0.55 * slides                               # each slide travels one mode to the right
        slides += 1
        put(sig, t, 0.07, np.linspace(start, start + 0.55, len(sig)), 0.4)
    elif k == 'clear':
        d = tt(0.3)
        put(noise(0.3, 1200, 7000) * (d / 0.3) ** 2.5, t, 0.05, 0.3, 0.5)
    elif k == 'morph':
        sig = whoosh(e['d'], 250, 5200, 0.8)
        put(sig, t, 0.13, np.linspace(-0.3, 0.3, len(sig)), 0.5)
        for j in range(4):                                             # one bubble per blob, then a run of small ones
            put(bloop(260 + 70 * j, 620 + 130 * j, 0.15, 0.05), t + 0.03 + 0.06 * j, 0.15, -0.5 + 0.33 * j, 0.5)
        for j in range(9):
            at = t + 0.3 + (e['d'] - 0.3) * (j / 9) ** 0.8
            put(bloop(500 + 110 * j, 1000 + 190 * j, 0.09, 0.025), at, 0.05 + 0.006 * j, rng.uniform(-0.6, 0.6), 0.6)
    elif k == 'title':
        d = tt(1.6)
        put(np.sin(2 * np.pi * np.cumsum(36.7 + 50 * np.exp(-d * 11)) / SR) * np.exp(-d / 0.5), t, 0.3, 0.0, 0.12)
        for j, (midi, gain) in enumerate(((62, 0.10), (69, 0.09), (74, 0.09), (78, 0.08), (81, 0.06), (88, 0.045))):
            put(glass(note(midi), 3.0, 0.8), t + 0.018 * j, gain, (-0.5, 0.4, -0.2, 0.3, -0.35, 0.5)[j], 0.9)
    elif k == 'glint':
        d = tt(e['d'])
        env = np.sin(np.pi * d / e['d']) ** 2
        sig = sum(np.sin(2 * np.pi * note(m) * (1 + 0.002 * np.sin(2 * np.pi * 5 * d)) * d + m) for m in (93, 98, 100, 102, 105)) / 5
        put(sig * env, t, 0.035, np.linspace(-0.6, 0.6, len(d)), 0.9)
        put(noise(e['d'], 6000, 13000) * env, t, 0.02, np.linspace(-0.6, 0.6, len(d)), 0.6)

# ---- reverb: each channel through its own decaying-noise room ----
mix = dry.copy()
for ch in range(2):
    ir = rng.standard_normal(int(2.0 * SR)) * np.exp(-tt(2.0) / 0.48)
    ir = band(ir, 180, 8500)
    ir /= np.sqrt((ir ** 2).sum())
    n = N + len(ir) - 1
    mix[:, ch] += np.fft.irfft(np.fft.rfft(wet[:, ch], n) * np.fft.rfft(ir, n), n)[:N] * 0.55

# ---- master: fade with the picture, soft clip, leave headroom ----
fade = np.clip(time / 0.04, 0, 1) * (1 - np.clip((time - t_fade) / (DUR - 0.03 - t_fade), 0, 1)) ** 1.6
mix *= fade[:, None]
mix = np.tanh(mix * 1.5)
mix *= 0.84 / np.abs(mix).max()
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('audio.wav', f'peak {np.abs(mix).max():.2f}', f'rms {np.sqrt((mix ** 2).mean()):.3f}')
