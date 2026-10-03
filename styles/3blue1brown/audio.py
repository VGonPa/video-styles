# events.json -> audio.wav (48 kHz stereo, 10 s), every sound synthesised.
# A calm, contemplative piano-and-pad cue in D major, in the spirit of a math-explainer score:
# low notes as the plane opens, single notes for the basis vectors, soft glints while formulas are
# written, a rising Gmaj9 arpeggio under the matrix transformation, a dominant as the terms fold
# into 3, and a D major resolution with a bell when the 3 lands in the parallelogram.
import json
import wave

import numpy as np

SR, DUR = 48000, 10.0
N = int(SR * DUR)
L = np.zeros(N)
R = np.zeros(N)
rng = np.random.default_rng(1729)


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def place(sig, t, gain=1.0, pan=0.0):
    i = int(round(t * SR))
    n = min(len(sig), N - i)
    if n <= 0 or i < 0:
        return
    L[i:i + n] += sig[:n] * gain * np.sqrt((1 - pan) / 2) * 1.414
    R[i:i + n] += sig[:n] * gain * np.sqrt((1 + pan) / 2) * 1.414


def piano(midi, dur=2.6, vel=1.0):
    """Two slightly detuned strings of inharmonic partials, a fast attack and a felt-hammer thump."""
    f0 = hz(midi)
    t = np.arange(int(dur * SR)) / SR
    tau0 = np.clip(1.5 * (220.0 / f0) ** 0.4, 0.35, 3.0)
    out = np.zeros_like(t)
    for detune in (-0.0006, 0.0006):
        for n in range(1, 9):
            fn = n * f0 * np.sqrt(1 + 0.00035 * n * n) * (1 + detune)
            if fn > 15000:
                break
            amp = (1.0 / n ** 1.25) * (0.55 + 0.45 * vel) ** (n - 1)
            out += amp * np.sin(2 * np.pi * fn * t + n * 0.7) * np.exp(-t * (1 + 0.55 * (n - 1)) / tau0)
    out *= np.minimum(1, t / 0.004)
    out *= np.minimum(1, np.maximum(0, (dur - t) / 0.25))
    thump = rng.standard_normal(int(0.012 * SR)) * np.exp(-np.arange(int(0.012 * SR)) / (0.002 * SR))
    out[:len(thump)] += 0.08 * np.convolve(thump, np.ones(12) / 12, 'same')
    return out / 4.0 * vel


def bell(midi, dur=2.4):
    f0 = hz(midi)
    t = np.arange(int(dur * SR)) / SR
    s = sum(a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t / d)
            for r, a, d in [(1, 1.0, 1.1), (2.76, 0.32, 0.45), (5.40, 0.14, 0.22), (8.93, 0.05, 0.12)])
    return s * np.minimum(1, t / 0.003) * np.minimum(1, np.maximum(0, (dur - t) / 0.3)) / 1.5


def pad(midis, t0, t1, gain, attack=0.9, release=0.9):
    """Soft sine-and-octave chord with slow swells, slightly spread across the stereo field."""
    n = int((t1 - t0 + release) * SR)
    t = np.arange(n) / SR
    env = np.minimum(1, t / attack) * np.clip((t1 - t0 + release - t) / release, 0, 1)
    for j, m in enumerate(midis):
        f = hz(m)
        wob = 1 + 0.002 * np.sin(2 * np.pi * (0.13 + 0.05 * j) * t)
        s = np.sin(2 * np.pi * f * t * wob) + 0.18 * np.sin(4 * np.pi * f * t) + 0.06 * np.sin(6 * np.pi * f * t)
        place(s * env, t0, gain, pan=-0.5 + j / max(1, len(midis) - 1))


def breath(t0, dur, gain):
    """A very soft band-limited noise swell (air moving as the plane transforms)."""
    n = int(dur * SR)
    x = rng.standard_normal(n)
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    spec *= np.exp(-((np.log(f + 1) - np.log(900)) ** 2) / 0.9)
    y = np.fft.irfft(spec, n)
    y /= np.abs(y).max() + 1e-9
    y *= np.sin(np.pi * np.arange(n) / n) ** 2
    place(y, t0, gain, -0.2)
    place(np.roll(y, 777), t0, gain * 0.9, 0.2)


ev = json.load(open('events.json'))
when = {e['k']: e for e in ev}
apply_t, apply_d = when['apply']['t'], when['apply']['d']

# harmonic bed: Dmaj9 -> Gmaj9 under the transformation -> Em7 under the derivation -> A -> D
glyphs = [e for e in ev if e['k'] == 'glyph']
det_t = min(e['t'] for e in glyphs if e['t'] > apply_t)    # first glyph of det(A) = ...
pad([50, 57, 64, 66], 0.10, apply_t, 0.020, attack=1.4)
pad([43, 50, 59, 66], apply_t, det_t, 0.022, attack=0.8)
pad([52, 59, 62, 67], det_t, when['morph']['t'], 0.019, attack=0.6)
pad([45, 52, 61, 64], when['morph']['t'], when['copy']['t'], 0.019, attack=0.4)
pad([50, 57, 62, 66, 69], when['copy']['t'], 9.6, 0.022, attack=0.7, release=0.8)

for e in ev:
    k, t = e['k'], e['t']
    if k == 'open':
        place(piano(38, 3.5, 0.7), t, 0.55, -0.1)
        place(piano(45, 3.2, 0.6), t + 0.35, 0.35, 0.1)
    elif k == 'vector':
        place(piano([69, 74][e['v']], 2.4, 0.8), t, 0.42, [-0.25, 0.25][e['v']])
    elif k == 'label':
        place(bell([78, 81, 76][e['v']], 1.8), t + 0.05, 0.10, [-0.35, 0.35, 0.0][e['v']])
    elif k == 'square':
        place(piano(66, 2.6, 0.7), t, 0.32, 0.0)
        place(piano(62, 2.6, 0.6), t + 0.02, 0.22, -0.1)
    elif k == 'glyph' and e['v'] % 2 == 0:
        if t < apply_t:
            notes = [74, 76, 78, 81]                       # matrix being written: Dmaj9 glints
        else:
            notes = [71, 74, 76, 79, 83, 79, 76]           # derivation being written: Em7 glints
        m = notes[(e['v'] // 2) % len(notes)]
        place(piano(m, 1.4, 0.45), t + 0.06, 0.13, rng.uniform(-0.4, 0.4))
    elif k == 'pulse':
        place(piano(43, 3.0, 0.75), t, 0.45, 0.0)
    elif k == 'apply':
        breath(t, e['d'] + 0.3, 0.018)
        arp = [55, 59, 62, 66, 69, 71, 74, 78]
        for j, m in enumerate(arp):                      # spaced like the eased motion: dense mid-way
            u = (j + 0.5) / len(arp)
            s = u - np.sin(2 * np.pi * u) / (2 * np.pi) * 0.6
            place(piano(m, 2.2, 0.55 + 0.04 * j), t + 0.05 + s * e['d'], 0.20 + 0.01 * j, -0.5 + j / 7)
    elif k == 'morph':
        place(piano(45, 2.8, 0.7), t, 0.40, -0.1)
        place(piano(61, 2.4, 0.6), t + 0.03, 0.22, 0.1)
        place(piano(64, 2.4, 0.6), t + 0.06, 0.20, 0.2)
    elif k == 'copy':
        for j, m in enumerate([76, 78, 81]):
            place(piano(m, 1.6, 0.55), t + 0.08 + j * 0.17, 0.16, -0.2 + 0.2 * j)
        land = t + e['d']
        for j, m in enumerate([38, 50, 57, 66, 74]):
            place(piano(m, 3.4, 0.8), land + j * 0.025, [0.42, 0.32, 0.26, 0.22, 0.2][j], -0.3 + 0.15 * j)
        place(bell(81, 2.6), land + 0.04, 0.12, 0.25)
    elif k == 'box':
        place(bell(86, 1.6), t + 0.1, 0.05, -0.3)
        place(bell(90, 1.4), t + 0.3, 0.035, 0.3)

# a small room: stereo exponentially decaying noise as the impulse response, convolved by FFT
ir_n = int(1.6 * SR)
ti = np.arange(ir_n) / SR
irL = rng.standard_normal(ir_n) * np.exp(-ti / 0.38)
irR = rng.standard_normal(ir_n) * np.exp(-ti / 0.38)
for ir in (irL, irR):
    sp = np.fft.rfft(ir)
    sp *= 1 / (1 + (np.fft.rfftfreq(ir_n, 1 / SR) / 4500) ** 2)
    ir[:] = np.fft.irfft(sp, ir_n)
    ir /= np.sqrt((ir ** 2).sum())
size = 1 << int(np.ceil(np.log2(N + ir_n)))
wetL = np.fft.irfft(np.fft.rfft(L, size) * np.fft.rfft(irL, size), size)[:N]
wetR = np.fft.irfft(np.fft.rfft(R, size) * np.fft.rfft(irR, size), size)[:N]
L = L + 0.30 * wetL
R = R + 0.30 * wetR

# open from silence and fade out with the picture (9.3 -> 10.0 s)
fade_in = int(0.08 * SR)
out_t = when['out']['t']
for ch in (L, R):
    ch[:fade_in] *= np.linspace(0, 1, fade_in)
    tail = np.arange(N) / SR
    ch *= np.clip(1 - (tail - out_t) / (DUR - out_t), 0, 1) ** 1.6
mix = np.stack([L, R], 1)
# master: the dense low pad made the mix hot (-13.5 LUFS at 0.78); 0.45 sits near -18 LUFS like the rest of the catalog
mix = np.tanh(mix / (np.abs(mix).max() + 1e-9) * 1.2) * 0.45
pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('audio.wav ok', round(float(np.abs(mix).max()), 3))
