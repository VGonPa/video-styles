# events.json → audio.wav (48 kHz stereo, 9.5 s)
# tiny jazzy synth jingle: FM electric-piano chord on every cut, walking-ish bass plucks, swung hi-hat,
# marimba blips for each word, plus doodle SFX (chomp, boing, plop, pop, ding, whoosh) and a final cadence.
import json, wave, numpy as np
SR, DUR = 48000, 9.5
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(75)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def epiano(f, d, bright=1.0):
    t = tt(d); idx = (1.6 * bright) * np.exp(-t / 0.18)
    s = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t)) + 0.25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.3)
    return s * np.exp(-t / (0.45 + 0.2 * bright)) * np.minimum(1, t / 0.004) * np.minimum(1, (d - t) / 0.05)
def chord(notes, t0, d=0.7, g=0.05, bright=1.0, spread=0.012):
    for k, m in enumerate(notes): add(epiano(nt(m), d, bright), t0 + k * spread, g, -0.4 + 0.8 * k / max(1, len(notes) - 1))
def bass(m, t0, d=0.5, g=0.22):
    t = tt(d); f = nt(m); s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t / 0.06)
    add(s * np.exp(-t / 0.22) * np.minimum(1, t / 0.003) * np.minimum(1, (d - t) / 0.04), t0, g)
def marimba(f, g, t0, pan):
    t = tt(0.22); s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.07) + 0.3 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / 0.012)
    add(s * np.minimum(1, t / 0.002), t0, g, pan)
def hat(t0, g):
    t = tt(0.05); n = band(rs.standard_normal(len(t)), 7000, 16000) * np.exp(-t / 0.012); add(n / (np.abs(n).max() + 1e-9), t0, g, 0.3)
def noise_burst(d, lo, hi, tau):
    t = tt(d); n = band(rs.standard_normal(len(t)), lo, hi) * np.exp(-t / tau); return n / (np.abs(n).max() + 1e-9)
def glide(f0, f1, d, tau, shape='sine'):
    t = tt(d); f = f0 * (f1 / f0) ** (t / d); ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) if shape == 'sine' else np.sign(np.sin(ph)) * 0.5
    return s * np.exp(-t / tau) * np.minimum(1, t / 0.002)
def bell(f, d=1.6):
    t = tt(d); return np.sin(2 * np.pi * f * t + 2.2 * np.exp(-t / 0.4) * np.sin(2 * np.pi * f * 3.5 * t)) * np.exp(-t / 0.6) * np.minimum(1, t / 0.002)

# one jazzy chord per cut (F major, with a couple of chromatic side-steps)
PROG = [([53, 57, 60, 64, 67], 41), ([50, 53, 57, 60, 64], 38), ([55, 58, 62, 65, 69], 43), ([48, 52, 58, 62, 69], 36),
        ([57, 61, 65, 67, 72], 45), ([50, 53, 57, 60, 64], 38), ([58, 62, 65, 69, 72], 46), ([57, 60, 64, 65, 69], 45),
        ([56, 60, 63, 67, 70], 44), ([55, 58, 62, 65, 69], 43), ([61, 65, 68, 72, 79], 49), ([48, 53, 55, 58, 62], 36)]
ev = json.load(open('events.json'))
cuts = sorted([(e['t'], e['i']) for e in ev if e['k'] == 'cut'])
def chord_at(t):
    c = 0
    for tc, i in cuts:
        if tc <= t + 1e-6: c = i
    return PROG[c]
# swung hi-hat bed (≈150 bpm), stops before the ending
beat = 60 / 150
for b in range(int(8.6 / beat)):
    hat(b * beat, 0.035); hat(b * beat + beat * 0.66, 0.02)
for e in ev:
    k, te = e['k'], e['t']
    if k == 'cut':
        notes, root = PROG[e['i']]
        if e['i'] < 11: chord(notes, te, 0.75, 0.05); bass(root, te)
        else: chord(notes, te, 0.3, 0.04); bass(root, te, 0.3)
    elif k == 'word':
        notes, _ = chord_at(te); m = notes[e['j'] % len(notes)] + 24
        marimba(nt(m), 0.1, te, -0.3 + 0.15 * (e['j'] % 5))
    elif k == 'stab': chord([n + 12 for n in chord_at(te)[0][1:]], te, 0.25, 0.03, 1.6, 0.0)
    elif k == 'pop': add(glide(900 + 400 * rs.random(), 300, 0.09, 0.03), te, 0.14, rs.uniform(-.6, .6)); add(noise_burst(0.02, 2000, 8000, 0.003), te, 0.05)
    elif k == 'chomp':
        for j, dt in enumerate([0, 0.07]): add(noise_burst(0.08, 300, 4000, 0.02), te + dt, 0.35); add(glide(180, 90, 0.08, 0.03), te + dt, 0.3)
    elif k == 'boing':
        t = tt(0.3); f = 220 * (1 + 0.8 * np.exp(-t / 0.05)) * (1 + 0.04 * np.sin(2 * np.pi * 14 * t)); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12)
        add(s, te, 0.12, rs.uniform(-.3, .3))
    elif k == 'whirl':
        t = tt(e['d']); f = 300 * 2 ** (2.5 * t / e['d']); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 22 * t)) * np.sin(np.pi * t / e['d'])
        add(s, te, 0.06)
    elif k == 'ding': add(bell(nt(84)), te, 0.1, 0.2); add(bell(nt(91), 0.8), te + 0.06, 0.05, 0.2)
    elif k == 'step': add(noise_burst(0.04, 200, 2500, 0.008), te, 0.08, -0.4)
    elif k == 'plop': add(glide(250, 1100, 0.12, 0.05), te, 0.2, rs.uniform(-.3, .3)); add(noise_burst(0.1, 800, 5000, 0.02), te + 0.01, 0.05)
    elif k == 'clunk': add(glide(140, 70, 0.2, 0.06), te, 0.35); add(bell(nt(96), 0.3), te, 0.04)
    elif k == 'whoosh':
        d = e['d'] + 0.1; t = tt(d); n = band(rs.standard_normal(len(t)), 300, 6000); n /= np.abs(n).max()
        add(n * (t / d) ** 2 * np.minimum(1, (d - t) / 0.03), te, 0.25)
    elif k == 'blip': add(glide(nt(84 + rs.integers(0, 3) * 4), nt(84), 0.06, 0.03, 'square'), te, 0.05, rs.uniform(-.7, .7))
    elif k == 'end':
        fin = [53, 57, 60, 64, 67, 72]
        for j, m in enumerate(fin): add(epiano(nt(m), 1.2, 0.7), te + 0.32 + j * 0.045, 0.05, -0.5 + j * 0.2)
        bass(29, te + 0.32, 1.1, 0.26)
    elif k == 'bell': add(bell(nt(89), 1.2), te, 0.07, 0.1)
# master: tiny fade-in, gentle fade-out on the last 0.35 s, soft limiter
fi = int(0.02 * SR); fo = int(0.35 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.0) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
