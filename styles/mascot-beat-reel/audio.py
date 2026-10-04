# events.json -> audio.wav (48 kHz stereo, 10 s). Synthesized only, nothing sampled.
# A tight 120 bpm toy-pop groove: kick on every beat, clap on 2 and 4, closed hats on 8ths, a
# bouncy octave-jumping synth bass (C - Am - F - G, then a C add9 to finish). Every label landing
# gets a stamp hit (low thump + noise slap) and each cut a short whoosh. Foley follows the picture:
# propeller whirr, slide-whistle drop and boing, a bulb blip and two bright dings; wooden knocks on
# the nail; pan sizzle, tosses and soft flops; balloon squeaks and a pop-burst into confetti; a toy
# horn with water slosh and steam puffs; a plonk per hat, a cymbal swell into the final chord, and a
# ring-out under the fade.
import json
import wave

import numpy as np

SR, DUR = 48000, 10.0
N = int(SR * DUR)
BEAT = 0.5
L = np.zeros(N); R = np.zeros(N)             # dry bus
RL = np.zeros(N); RR = np.zeros(N)           # reverb send
rng = np.random.default_rng(150)
ev = json.load(open('events.json'))


def put(sig, t, g=1.0, pan=0.0, send=0.0):
    """Mix a mono signal at time t; pan clamped to [-1, 1] before the constant-power law."""
    i = int(round(t * SR))
    if i >= N:
        return
    if i < 0:
        sig = sig[-i:]; i = 0
    n = min(len(sig), N - i)
    if n <= 0:
        return
    p = float(np.clip(pan, -1.0, 1.0))
    gl, gr = np.cos((p + 1) * np.pi / 4), np.sin((p + 1) * np.pi / 4)
    s = sig[:n] * g
    L[i:i + n] += s * gl; R[i:i + n] += s * gr
    if send:
        RL[i:i + n] += s * gl * send; RR[i:i + n] += s * gr * send


def ts(d): return np.arange(int(d * SR)) / SR
def midi(m): return 440.0 * 2 ** ((m - 69) / 12)
def osc(freq_curve): return 2 * np.pi * np.cumsum(freq_curve) / SR
def adsr(d, a=0.004, r=0.04):
    x = ts(d); return np.minimum(1, x / max(a, 1e-4)) * np.clip((d - x) / max(r, 1e-4), 0, 1)
def noise(d): return rng.standard_normal(int(d * SR))
def bandpass(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))
def lowpass1(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); acc = 0.0
    for k in range(len(x)):
        acc = (1 - a) * x[k] + a * acc; y[k] = acc
    return y
def norm(x): return x / (np.abs(x).max() + 1e-9)


# ------------------------------------------------------------------ instruments
def kick(d=0.32):
    x = ts(d); f = 48 + 110 * np.exp(-x * 38)
    return np.sin(osc(f)) * np.exp(-x * 9) * adsr(d, 0.001, 0.05) + 0.25 * norm(bandpass(noise(d), 1500, 6000)) * np.exp(-x * 160)
def clap(d=0.22):
    x = ts(d); env = np.zeros_like(x)
    for k, off in enumerate((0, 0.011, 0.022)):
        env += (x >= off) * np.exp(-np.maximum(0, x - off) * (140 if k < 2 else 26))
    return norm(bandpass(noise(d), 900, 5200)) * env
def hat(d=0.05, open_=False):
    x = ts(d); return norm(bandpass(noise(d), 7000, 15000)) * np.exp(-x * (28 if open_ else 95))
def bass(m, d=0.22):
    x = ts(d); f = midi(m) * (1 + 0.012 * np.exp(-x * 30))
    ph = osc(f)
    raw = np.sign(np.sin(ph)) * 0.45 + np.sin(ph) * 0.7 + 0.25 * np.sin(2 * ph)
    return lowpass1(raw, 1500) * adsr(d, 0.003, 0.05) * np.exp(-x * 3)
def thump(f0=95, d=0.35):
    x = ts(d); return np.sin(osc(f0 * (0.5 + 0.9 * np.exp(-x * 30)))) * np.exp(-x * 10) * adsr(d, 0.001, 0.05)
def slap(d=0.09, lo=1200, hi=7000):
    x = ts(d); return norm(bandpass(noise(d), lo, hi)) * np.exp(-x * 55)
def whoosh(d, lo, hi, rise=True):
    x = ts(d); env = (x / d) ** 2 if rise else (1 - x / d) ** 2
    return norm(bandpass(noise(d), lo, hi)) * env * adsr(d, 0.01, 0.02)
def blip(f0, f1, d, shape='sine'):
    x = ts(d); f = f0 * (f1 / f0) ** (x / d); ph = osc(f)
    w = np.sin(ph) if shape == 'sine' else 0.6 * np.sign(np.sin(ph)) + 0.4 * np.sin(ph)
    return w * adsr(d, 0.002, min(0.04, d / 2))
def boing(f, d=0.45):
    x = ts(d); fm = f * (1 + 0.5 * np.exp(-x * 8) * np.sin(2 * np.pi * 12 * x))
    return np.sin(osc(fm)) * np.exp(-x * 6) * adsr(d, 0.002, 0.06)
def plonk(f, d=0.4):
    x = ts(d); s = np.sin(2 * np.pi * f * x) * np.exp(-x * 14) + 0.5 * np.sin(2 * np.pi * f * 2.76 * x) * np.exp(-x * 30)
    return s * adsr(d, 0.001, 0.05)
def chord_pad(notes, d, bright=6):
    x = ts(d); s = np.zeros_like(x)
    for m in notes:
        for det in (-0.06, 0.0, 0.07):
            f = midi(m) * 2 ** (det / 12); ph0 = rng.uniform(0, 2 * np.pi)
            for h in range(1, bright + 1):
                s += np.sin(2 * np.pi * f * h * x + ph0 * h) / h ** 1.2
    return s / (3 * len(notes) * 2.5)


# ------------------------------------------------------------------ groove
BASSLINE = [48, 48, 45, 45, 41, 41, 43, 43]         # one root per beat pair: C C Am Am F F G G (bars of 2 s)
for e in ev:
    if e['k'] != 'beat':
        continue
    t, n = e['t'], e['n']
    if t > 9.0 + 1e-6:
        continue                                     # ring-out: the groove stops on the final chord
    put(kick(), t, 0.95)
    if n % 4 in (1, 3):
        put(clap(), t, 0.42, 0.12, send=0.25)
    for k in range(2):                               # 8th-note hats, the off-beat a little more open
        put(hat(0.07 if k else 0.04, open_=bool(k)), t + k * BEAT / 2, 0.16 if k else 0.11, 0.35)
    if t < 9.0:
        root = BASSLINE[(n // 2) % 8] if t < 8.0 else 48
        put(bass(root - 12), t, 0.36, -0.05)                 # root on the beat
        put(bass(root, 0.16), t + BEAT / 2, 0.24, 0.05)      # octave on the off-beat: the bounce

# ------------------------------------------------------------------ cues
def bell(f, d=1.1):
    x = ts(d)
    s = sum(a * np.sin(2 * np.pi * f * r * x) * np.exp(-x * k) for r, k, a in ((1, 3.5, 1), (2.76, 7, 0.4), (5.4, 13, 0.18)))
    return s * adsr(d, 0.001, 0.05)
def squeak(f0, f1, d=0.2):
    x = ts(d); f = (f0 + (f1 - f0) * np.sqrt(x / d)) * (1 + 0.03 * np.sin(2 * np.pi * 26 * x)); ph = osc(f)
    return (np.sin(ph) + 0.35 * np.sin(2 * ph)) * adsr(d, 0.01, 0.05)
for e in ev:
    k, t, pan = e['k'], e['t'], e.get('pan', 0.0)
    if k == 'stamp':
        put(thump(), t, 0.85); put(slap(), t, 0.32, 0.0, send=0.3)
    elif k == 'sub':
        put(blip(1800, 2400, 0.05), t, 0.08, -0.2)
    elif k == 'cut':
        put(whoosh(0.22, 2500, 9000), t - 0.22, 0.12, 0.0, send=0.2)
    elif k == 'whirr':                                   # propeller: buzzy band noise chopped at the blade rate
        d = e['d']; x = ts(d); rate = 30 + 16 * np.clip((x - 1.0) * 4, 0, 1)
        chop = 0.55 + 0.45 * np.sin(2 * np.pi * np.cumsum(rate) / SR)
        put(norm(bandpass(noise(d), 350, 1600)) * chop * adsr(d, 0.3, 0.1), t, 0.05, pan)
    elif k == 'fall':
        put(blip(1500, 520, 0.48) * 0.8, t + 0.01, 0.16, pan, send=0.3)       # slide whistle down
    elif k == 'land':
        put(boing(150), t, 0.4, pan, send=0.2)
    elif k == 'bulb':
        put(blip(420, 950, 0.12), t + 0.02, 0.18, pan, send=0.2)
    elif k == 'ding':
        put(bell([1318.5, 1568.0][e['i']]), t, 0.3, pan, send=0.45)
    elif k == 'swing':
        put(whoosh(0.14, 600, 4500), t, 0.14, pan)
    elif k == 'knock':                                   # wood knock + a bright tink off the nail head
        x = ts(0.16)
        wood = norm(bandpass(noise(0.16), 450, 1400)) * np.exp(-x * 45) + 0.8 * np.sin(2 * np.pi * 190 * x) * np.exp(-x * 30)
        put(wood, t, 0.55, pan, send=0.2)
        put(sum(np.sin(2 * np.pi * f * ts(0.25)) * np.exp(-ts(0.25) * 22) for f in (2350, 3580)) * 0.5, t, 0.12, pan + 0.1, send=0.3)
    elif k == 'sizzle':                                  # pan hiss with a sprinkle of crackles
        d = e['d']; x = ts(d); hiss = norm(bandpass(noise(d), 3000, 11000)) * (0.7 + 0.3 * np.sin(2 * np.pi * 3 * x))
        crack = np.zeros(len(x))
        for j in rng.integers(0, len(x) - 200, 70):
            crack[j:j + 120] += rng.uniform(0.3, 1) * np.exp(-np.arange(120) / 18)
        put((hiss * 0.6 + bandpass(crack * rng.standard_normal(len(x)), 2000, 9000) * 2) * adsr(d, 0.05, 0.1), t, 0.07, pan)
    elif k == 'toss':
        put(whoosh(0.18, 900, 5000), t - 0.04, 0.1, pan)
    elif k == 'flop':                                    # soft batter flop: low thud + short wet slap
        put(thump(105, 0.2), t, 0.45, pan); put(slap(0.06, 300, 1800), t, 0.25, pan)
    elif k == 'butter':
        put(blip(900, 1500, 0.07), t, 0.12, pan, send=0.2)
    elif k == 'squeak':
        put(squeak(620 + 90 * e['i'], 980 + 120 * e['i']), t, 0.2, pan, send=0.25)
    elif k == 'burst':                                   # four overlapping pops
        for j in range(4):
            put(slap(0.08, 800, 12000) + 0.6 * thump(160, 0.08), t + 0.008 * j, 0.42, pan + (j - 1.5) * 0.25, send=0.3)
    elif k == 'confetti':
        for j in range(18):
            put(blip(5000 + 3000 * rng.random(), 6200, 0.02), t + 0.04 + 0.45 * rng.random(), 0.05, rng.uniform(-0.6, 0.9), send=0.4)
    elif k == 'hop':
        put(blip(260, 700, 0.2), t, 0.16, pan, send=0.2)
    elif k == 'slosh':
        d = 0.7 if e.get('big') else 0.45
        x = ts(d); wob = 0.6 + 0.4 * np.sin(2 * np.pi * 7 * x)
        put(norm(bandpass(noise(d), 250, 2200)) * np.sin(np.pi * x / d) ** 1.5 * wob, t, 0.22 if e.get('big') else 0.14, pan, send=0.3)
    elif k == 'horn':
        d = 0.42; x = ts(d)
        tone = sum(np.sign(np.sin(osc(midi(m) * (1 + 0.006 * np.sin(2 * np.pi * 6 * x))))) for m in (64, 68))
        put(lowpass1(tone, 1400) * adsr(d, 0.02, 0.08), t, 0.2, pan, send=0.3)
    elif k == 'puff':
        d = 0.3 if e.get('small') else 0.45; x = ts(d)
        put(norm(bandpass(noise(d), 500, 3000)) * np.exp(-x * 7) * adsr(d, 0.01, 0.05), t, 0.12 if e.get('small') else 0.2, pan, send=0.2)
    elif k == 'plonk':
        put(plonk(midi([67, 71, 74, 79][e['i']])), t, 0.36, pan + [-0.25, 0.15, -0.1, 0.2][e['i']], send=0.25)
        put(thump(140, 0.12), t, 0.25, pan)
    elif k == 'swell':
        put(whoosh(e['d'], 3000, 14000) * 0.9, t, 0.16, 0.0, send=0.4)
    elif k == 'chord':
        d = DUR - t
        pad = chord_pad([48, 60, 64, 67, 74], d) * adsr(d, 0.004, 0.05) * np.exp(-ts(d) * 1.1)
        put(pad, t, 0.62, 0.0, send=0.45)
        x = ts(d); crash = norm(bandpass(noise(d), 3500, 16000)) * np.exp(-x * 2.6)
        put(crash, t, 0.17, -0.1, send=0.35)
        put(thump(70, 0.5), t, 0.8)

# ------------------------------------------------------------------ reverb (a short plate: decaying noise IR)
irn = int(1.1 * SR); x = np.arange(irn) / SR
ir = rng.standard_normal(irn) * np.exp(-x * 5.5); ir[: int(0.012 * SR)] = 0
ir = bandpass(ir, 200, 9000); ir /= np.sqrt((ir ** 2).sum())
def conv(a):
    m = len(a) + irn; fa = np.fft.rfft(a, m); fb = np.fft.rfft(ir, m)
    return np.fft.irfft(fa * fb, m)[: len(a)]
L += 0.5 * conv(RL); R += 0.5 * conv(RR)

# ------------------------------------------------------------------ master: fade-out tail, soft clip, -1 dBFS peak
fade = next(e for e in ev if e['k'] == 'fade')
tt = np.arange(N) / SR
tail = np.clip(1 - (tt - fade['t']) / fade['d'], 0, 1) ** 1.5
tail = np.where(tt < fade['t'], 1.0, 0.35 + 0.65 * tail)       # ring-out keeps going under the picture fade
tail[-int(0.04 * SR):] *= np.linspace(1, 0, int(0.04 * SR))
st = np.stack([L, R]) * tail
st = np.tanh(st * 1.2) / np.tanh(1.2)
st *= 10 ** (-1 / 20) / np.abs(st).max()
assert np.isfinite(st).all(), 'NaN in mix'
assert (np.abs(st[0]).max() > 0.1) and (np.abs(st[1]).max() > 0.1), 'a channel is silent'
pcm = (np.clip(st.T, -1, 1) * 32767).astype('<i2')
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
