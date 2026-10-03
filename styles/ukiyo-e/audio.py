# events.json -> audio.wav (48 kHz stereo, 10 s), all synthesised with numpy.
# A quiet print-shop and sea piece: wooden block knocks and baren rubs while the print is pulled,
# koto-like plucked strings on a hirajoshi-flavoured scale, a rising sea swell, the crash with a
# low drum, plover peeps, a paper rub for the second sheet, the seal press and a ringing bowl.
import json
import wave

import numpy as np

SR, DUR = 48000, 10.0
N = int(SR * DUR)
L = np.zeros(N)
R = np.zeros(N)
noise = np.random.default_rng(183)
BASE = 293.66  # D4


def secs(d):
    return np.arange(int(d * SR)) / SR


def place(sig, t, gain=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= N:
        return
    n = min(len(sig), N - i)
    gl, gr = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i:i + n] += sig[:n] * gain * gl * 1.414
    R[i:i + n] += sig[:n] * gain * gr * 1.414


def bandpass(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def norm(x):
    return x / (np.abs(x).max() + 1e-9)


def koto(n):
    """Plucked string: decaying partials, brighter attack, a small press-bend after the pluck."""
    f0 = BASE * 2 ** (n / 12)
    t = secs(2.6)
    bend = 1 + 0.012 * np.clip((t - 0.18) / 0.12, 0, 1) * np.exp(-np.maximum(t - 0.3, 0) / 0.5)
    phase = 2 * np.pi * f0 * np.cumsum(bend) / SR
    out = np.zeros_like(t)
    for h in range(1, 9):
        amp = (1 / h) * (1.0 if h % 2 else 0.7)
        out += amp * np.sin(h * phase + h * 0.3) * np.exp(-t * (1.2 + 0.9 * h))
    click = bandpass(noise.standard_normal(len(t)), 1500, 7000) * np.exp(-t / 0.006) * 0.25
    return (out / 2.2 + click) * np.minimum(1, t / 0.002)


def tok(f):
    """Wooden block knock: two damped modes and a short noise tap."""
    t = secs(0.35)
    body = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.05) + 0.5 * np.sin(2 * np.pi * f * 2.7 * t) * np.exp(-t / 0.025)
    tap = bandpass(noise.standard_normal(len(t)), 800, 4000) * np.exp(-t / 0.008) * 0.6
    return norm(body + tap)


def rub(d):
    """The baren circling on the back of the sheet: soft papery noise with a slow wobble."""
    t = secs(d)
    x = norm(bandpass(noise.standard_normal(len(t)), 900, 6000))
    wob = 0.55 + 0.45 * np.sin(2 * np.pi * 5.5 * t) ** 2
    return x * wob * np.sin(np.pi * t / d) ** 1.2


def sea_bed(d):
    """Distant surf: low rumble breathing slowly, fading in and out."""
    t = secs(d)
    x = norm(bandpass(noise.standard_normal(len(t)), 60, 700))
    breath = 0.6 + 0.4 * np.sin(2 * np.pi * 0.23 * t - 1.2)
    fade = np.minimum(1, t / 0.8) * np.minimum(1, (d - t) / 1.2)
    return x * breath * fade * 0.3


def swell(d):
    """The wave gathering: band-limited noise opening upward in brightness and level."""
    t = secs(d)
    x = noise.standard_normal(len(t))
    lo = norm(bandpass(x, 80, 500))
    hi = norm(bandpass(x, 500, 3500))
    u = t / d
    return (lo * (0.3 + 0.7 * u) + hi * u ** 2 * 0.8) * u ** 1.4


def crash():
    t = secs(1.8)
    x = noise.standard_normal(len(t))
    body = norm(bandpass(x, 100, 5000)) * np.exp(-t / 0.45)
    low = norm(bandpass(x, 40, 220)) * np.exp(-t / 0.6)
    return body * 0.8 + low * 0.7


def taiko(f):
    t = secs(1.2)
    fr = f * (1 + 0.6 * np.exp(-t / 0.03))
    skin = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.32)
    slap = bandpass(noise.standard_normal(len(t)), 200, 2000) * np.exp(-t / 0.015) * 0.5
    return norm(skin + slap)


def hiss(d):
    t = secs(d)
    return norm(bandpass(noise.standard_normal(len(t)), 3000, 11000)) * np.exp(-t / (d * 0.35)) * np.minimum(1, t / 0.03)


def peep(f):
    """Plover call: a short rising-falling whistle, two notes."""
    out = np.zeros(int(0.32 * SR))
    for k, (dt, a) in enumerate([(0.0, 1.0), (0.14, 0.7)]):
        t = secs(0.11)
        fr = f * (1 + 0.18 * np.sin(np.pi * t / 0.11)) * (1 - 0.05 * k)
        s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * t / 0.11) ** 2
        i = int(dt * SR)
        out[i:i + len(s)] += s * a
    return out


def tick(f):
    t = secs(0.05)
    return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.008)


def stamp():
    """Seal pressed into paper: a dull wooden thock and a soft paper crush."""
    t = secs(0.5)
    thock = np.sin(2 * np.pi * 110 * t) * np.exp(-t / 0.06) + 0.4 * np.sin(2 * np.pi * 260 * t) * np.exp(-t / 0.03)
    crush = bandpass(noise.standard_normal(len(t)), 400, 3000) * np.exp(-t / 0.04) * 0.5
    return norm(thock + crush)


def rin(f):
    """Singing bowl: inharmonic partials with slow beating."""
    t = secs(2.8)
    out = np.zeros_like(t)
    for ratio, amp, dec in [(1, 1, 1.6), (2.71, 0.5, 1.0), (5.12, 0.25, 0.6), (8.4, 0.12, 0.35)]:
        out += amp * np.sin(2 * np.pi * f * ratio * t) * (1 + 0.15 * np.sin(2 * np.pi * 3.1 * t)) * np.exp(-t / dec)
    return out / 1.9 * np.minimum(1, t / 0.004)


GEN = {
    'koto': lambda e: koto(e['n']),
    'tok': lambda e: tok(e['f']),
    'rub': lambda e: rub(e['d']),
    'sea': lambda e: sea_bed(e['d']),
    'swell': lambda e: swell(e['d']),
    'crash': lambda e: crash(),
    'taiko': lambda e: taiko(e['f']),
    'hiss': lambda e: hiss(e['d']),
    'peep': lambda e: peep(e['f']),
    'tick': lambda e: tick(e['f']),
    'stamp': lambda e: stamp(),
    'rin': lambda e: rin(e['f']),
}
PAN = {'peep': lambda: noise.uniform(0.1, 0.6), 'koto': lambda: noise.uniform(-0.35, 0.2),
       'tick': lambda: 0.45, 'crash': lambda: 0.15, 'rub': lambda: noise.uniform(-0.3, 0.3)}

for e in json.load(open('events.json')):
    pan = PAN.get(e['k'], lambda: 0.0)()
    place(GEN[e['k']](e), e['t'], e.get('v', 0.5), pan)

fade = int(0.8 * SR)
for ch in (L, R):
    ch[-fade:] *= np.linspace(1, 0, fade) ** 1.6
mixd = np.stack([L, R], 1)
mixd = np.tanh(mixd / (np.abs(mixd).max() + 1e-9) * 1.3) * 0.85
pcm = (np.clip(mixd, -1, 1) * 32767).astype(np.int16)
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('audio.wav ok', round(float(np.abs(mixd).max()), 3))
