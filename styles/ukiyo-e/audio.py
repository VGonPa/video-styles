# events.json → audio.wav (48 kHz stereo, 10 s). Everything is synthesised; nothing is sampled.
# Print one: four soft baren presses, open sea, a koto figure that tightens into a trill as the wave
# rears, a rising rumble and the crash. Print two: quiet lapping water, a breathy bamboo-flute line,
# koto notes under the title, a wooden clack and drum for the seal, and a last open chord.
import json, wave
import numpy as np

SR, DUR = 48000, 10.0
N = int(SR * DUR)
MIX = np.zeros((N, 2))
rs = np.random.default_rng(38)


def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def hz(n): return 440.0 * 2 ** ((n - 69) / 12)
def noise(n): return rs.standard_normal(n)


def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (lo / np.maximum(f, 1e-6)) ** 6) / (1 + (f / hi) ** 6)   # soft-edged band-pass
    return np.fft.irfft(X, len(x))


def add(sig, t, g=1.0, pan=0.0):
    """Mono signal at time t; pan -1 (left) .. 1 (right), equal power."""
    i = int(t * SR); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    MIX[i:i + n, 0] += sig[:n] * g * np.cos((pan + 1) * np.pi / 4) * 1.414
    MIX[i:i + n, 1] += sig[:n] * g * np.sin((pan + 1) * np.pi / 4) * 1.414


def add_wide(make, t, g):
    """Two independent takes of a noise texture, one per ear."""
    for ch in (0, 1):
        sig = make(); i = int(t * SR); n = min(len(sig), N - i)
        if n > 0: MIX[i:i + n, ch] += sig[:n] * g


def koto(n, d=2.4):
    """Plucked string (Karplus-Strong), resampled to the exact pitch, with a plectrum tick."""
    f = hz(n); period = int(round(SR / f)); total = int(d * SR)
    cur = rs.uniform(-1, 1, period); cur = 0.5 * (cur + np.roll(cur, 1)); cur -= cur.mean()
    blocks = []
    for _ in range(total // period + 2):
        blocks.append(cur); cur = 0.5 * (cur + np.roll(cur, 1)) * 0.9965
    raw = np.concatenate(blocks)
    out = np.interp(np.arange(total) * (period * f / SR), np.arange(len(raw)), raw)
    t = tt(d)[:total]
    tick = band(noise(total), 1800, 7000) * np.exp(-t / 0.004) * 0.5
    return (norm(out) + tick) * np.minimum(1, (d - t) / 0.25)


def flute(n, d):
    """Bamboo flute: the note is scooped up from below, breath noise rides on it, vibrato arrives late."""
    t = tt(d); f = hz(n)
    scoop = 2 ** (-0.7 / 12 * np.exp(-t / 0.08))
    vib = 1 + 0.007 * np.sin(2 * np.pi * 4.7 * t) * np.clip((t - 0.6) / 0.9, 0, 1)
    ph = 2 * np.pi * np.cumsum(f * scoop * vib) / SR
    tone = np.sin(ph) + 0.30 * np.sin(2 * ph) + 0.11 * np.sin(3 * ph) + 0.04 * np.sin(4 * ph)
    breath = norm(band(noise(len(t)), f * 0.9, f * 4)) * (0.22 + 0.9 * np.exp(-t / 0.07)) + 0.05 * norm(band(noise(len(t)), 3000, 8000))
    env = np.minimum(1, t / 0.16) * np.minimum(1, (d - t) / 0.7) * (0.72 + 0.28 * np.sin(np.pi * t / d))
    return (0.8 * tone + 0.3 * breath) * env


def press():
    """The baren rubbing a block down: a soft padded thud and a breath of paper."""
    t = tt(0.32)
    body = np.sin(2 * np.pi * np.cumsum(58 + 34 * np.exp(-t / 0.03)) / SR) * np.exp(-t / 0.055)
    rub = norm(band(noise(len(t)), 500, 4500)) * np.exp(-t / 0.05) * np.minimum(1, t / 0.006)
    return body + 0.3 * rub


def surf(d, lo, hi, rate, depth, phase):
    """Rolling water: band-limited noise breathing at `rate` Hz."""
    t = tt(d)
    am = 1 - depth + depth * (0.5 + 0.5 * np.sin(2 * np.pi * rate * t + phase)) ** 1.5
    return norm(band(noise(len(t)), lo, hi)) * am * np.minimum(1, t / 0.5) * np.minimum(1, (d - t) / 0.6)


def swell(d):
    t = tt(d); k = t / d
    return norm(band(noise(len(t)), 38, 380)) * k ** 2.2 + 0.45 * norm(band(noise(len(t)), 300, 1600)) * k ** 3.2


def crash():
    """The wave falling: a low thump, then a wall of water whose top fizzes on as foam."""
    t = tt(3.0); n = len(t); a = np.minimum(1, t / 0.07)
    low = norm(band(noise(n), 45, 300)) * np.exp(-t / 0.5)
    mid = norm(band(noise(n), 300, 2600)) * np.exp(-t / 0.65)
    fizz = norm(band(noise(n), 2600, 9500)) * np.exp(-t / 1.0) * (0.75 + 0.25 * np.abs(band(noise(n), 6, 30)) * 6)
    thump = np.sin(2 * np.pi * np.cumsum(38 + 26 * np.exp(-t / 0.09)) / SR) * np.exp(-t / 0.3)
    return a * (0.9 * low + 0.8 * mid + 0.42 * fizz) + 0.9 * thump


def stamp():
    """Seal: wooden clappers and a small drum under them."""
    t = tt(0.7)
    clack = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / dcy) for f, a, dcy in ((1180, 1, .022), (2090, .6, .016), (3340, .3, .009)))
    clack += 0.5 * norm(band(noise(len(t)), 2000, 9000)) * np.exp(-t / 0.003)
    drum = np.sin(2 * np.pi * np.cumsum(60 + 40 * np.exp(-t / 0.035)) / SR) * np.exp(-t / 0.2)
    return 0.7 * clack + drum


for e in json.load(open('events.json')):
    k, t0, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'press': add(press(), t0, 0.30 * v, rs.uniform(-.2, .2))
    elif k == 'sea':
        add_wide(lambda: surf(e['d'], 160, 2400, 0.42, 0.6, rs.uniform(0, 6)), t0, 0.11)
        add_wide(lambda: surf(e['d'], 2400, 7500, 0.42, 0.8, rs.uniform(0, 6)), t0, 0.03)
    elif k == 'calm':
        add_wide(lambda: surf(e['d'], 200, 1700, 0.3, 0.7, rs.uniform(0, 6)), t0, 0.04)
    elif k == 'swell': add_wide(lambda: swell(e['d']), t0, 0.34)
    elif k == 'crash': add_wide(crash, t0, 0.62)
    elif k == 'koto':
        n = e['n']; add(koto(n), t0, 0.2 * v, np.clip((n - 66) / 14, -.5, .5))
    elif k == 'flute': add(flute(e['n'], e['d']), t0, 0.085, -0.15)
    elif k == 'stamp': add(stamp(), t0, 0.24, -0.1)

# a small wooden room: exponentially decaying noise as the impulse response, a different one per ear
out = np.zeros_like(MIX)
for ch in (0, 1):
    ti = tt(1.5); ir = band(noise(len(ti)), 250, 6000) * np.exp(-ti / 0.32); ir /= np.sqrt((ir ** 2).sum())
    wet = np.fft.irfft(np.fft.rfft(MIX[:, ch], N + len(ir)) * np.fft.rfft(ir, N + len(ir)), N + len(ir))[:N]
    out[:, ch] = MIX[:, ch] + 0.2 * wet
fi, fo = int(0.12 * SR), int(0.75 * SR)
out[:fi] *= np.linspace(0, 1, fi)[:, None]
out[-fo:] *= (np.linspace(1, 0, fo) ** 1.6)[:, None]
out = np.tanh(out / np.abs(out).max() * 1.25) / np.tanh(1.25) * 0.89
pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('audio.wav ok', 'peak', np.abs(out).max().round(3), 'rms', np.sqrt((out ** 2).mean()).round(3))
