# events.json → audio.wav (48 kHz stereo, 10 s)
# 16-bit console sound set, all synthesized: pulse/triangle/noise channels.
# Clock bell, encounter sting + swirl sweep, battle loop (triangle bass, pulse arpeggio, noise hats),
# menu blips, text blips, slash/hit/crunch noise, spell sparkle, stamp thud, boss dissolve rumble,
# original victory fanfare, EXP ticks, level-up jingle, learned chime.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(71)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def pulse(f, d, duty=0.5, att=0.003, dec=None, vib=0.0):
    t = tt(d); ff = f * (1 + vib * np.sin(2 * np.pi * 6 * t)) if np.isscalar(f) else f
    ph = np.cumsum(np.broadcast_to(ff, t.shape)) / SR
    s = np.where((ph % 1) < duty, 1.0, -1.0)
    env = np.minimum(1, t / att) * (np.exp(-t / dec) if dec else np.minimum(1, (d - t) / 0.01))
    return s * env
def tri(f, d, dec=None):
    t = tt(d); ph = (f * t) % 1; s = 4 * np.abs(ph - 0.5) - 1
    env = np.minimum(1, t / 0.003) * (np.exp(-t / dec) if dec else np.minimum(1, (d - t) / 0.01))
    return s * env
def noise(d, dec=0.05, hold=7):
    # sample-and-hold noise = NES-ish noise channel; hold sets the "pitch"
    n = int(d * SR); v = rs.uniform(-1, 1, n // hold + 2); s = np.repeat(v, hold)[:n]
    return s * np.exp(-tt(d) / dec)
def sweep(f0, f1, d, duty=0.5, dec=None):
    t = tt(d); f = f0 * (f1 / f0) ** (t / d); ph = np.cumsum(f) / SR
    s = np.where((ph % 1) < duty, 1.0, -1.0)
    env = np.exp(-t / dec) if dec else np.minimum(1, (d - t) / 0.02)
    return s * env * np.minimum(1, t / 0.003)
def noise_sweep(d, h0, h1, dec):
    n = int(d * SR); out = np.zeros(n); i = 0
    while i < n:
        h = int(h0 + (h1 - h0) * i / n); out[i:i + h] = rs.uniform(-1, 1); i += max(1, h)
    return out * np.exp(-tt(d) / dec)
ev = json.load(open('events.json'))
T = {e['k']: e['t'] for e in ev}
# ── battle loop (A minor, 150 bpm, 8ths) from the reveal until the boss dissolves ──
t0, t1 = T['bgm'], T['die']
e8 = 60 / 150 / 2
bass = [45, 45, 57, 45, 48, 45, 50, 52, 45, 45, 57, 45, 53, 52, 50, 47]
arp = [69, 72, 76, 72, 69, 72, 77, 72, 68, 71, 76, 71, 68, 71, 74, 71]
k = 0
while t0 + k * e8 < t1:
    ts = t0 + k * e8; fadeg = min(1.0, (t1 - ts) / 0.3)
    add(tri(nt(bass[k % 16] - 12 + 12), e8 * 0.95), ts, 0.16 * fadeg)
    add(pulse(nt(arp[k % 16]), e8 * 0.8, 0.25, dec=0.08), ts, 0.035 * fadeg, 0.3)
    if k % 2 == 1: add(noise(0.05, 0.012, 2), ts, 0.05 * fadeg, -0.2)
    if k % 4 == 0: add(noise(0.12, 0.04, 20) + sweep(160, 50, 0.12, dec=0.05), ts, 0.10 * fadeg)
    k += 1
# ── one-shots ──
for e in ev:
    k_, te, v = e['k'], e['t'], e.get('v', 0)
    if k_ == 'bell':
        for i, m in enumerate([84, 79]): add(tri(nt(m), 0.6, dec=0.25) + 0.4 * pulse(nt(m + 12), 0.6, 0.5, dec=0.12), te + i * 0.02, 0.10)
    elif k_ == 'alert': add(sweep(600, 1800, 0.12, 0.5, dec=0.08), te, 0.08)
    elif k_ == 'encounter':
        for i in range(3): add(sweep(1600, 200, 0.05, 0.5), te + i * 0.053, 0.07, (-1) ** i * 0.3)
    elif k_ == 'swirl':
        for i in range(16): add(pulse(nt(60 + i * 2), 0.03, 0.25, dec=0.02), te + i * 0.021, 0.06, np.sin(i) * 0.5)
        add(noise_sweep(0.36, 30, 2, 0.3), te, 0.05)
    elif k_ == 'open': add(pulse(nt(84), 0.03, 0.5, dec=0.015), te, 0.05)
    elif k_ == 'blip': add(pulse(nt(76 if v == 0 else 88), 0.018, 0.5 if v == 0 else 0.25, dec=0.01), te, 0.035 if v == 0 else 0.03, 0.1)
    elif k_ == 'move': add(pulse(nt(88), 0.03, 0.25, dec=0.012), te, 0.06)
    elif k_ == 'select': add(pulse(nt(84), 0.04, 0.5, dec=0.02), te, 0.06); add(pulse(nt(91), 0.06, 0.5, dec=0.03), te + 0.04, 0.06)
    elif k_ == 'step': add(noise(0.04, 0.01, 6), te, 0.08)
    elif k_ == 'slash': add(noise_sweep(0.18, 1, 8, 0.07), te, 0.16, -0.3)
    elif k_ == 'hit': add(noise(0.2, 0.06, 12) + sweep(220, 60, 0.2, dec=0.07), te, 0.15, -0.3)
    elif k_ == 'charge': add(sweep(120, 700, 0.3, 0.125) * np.linspace(0.3, 1, int(0.3 * SR)), te, 0.06, -0.3)
    elif k_ == 'wave':
        t = tt(0.22); f = 400 + 250 * np.sin(2 * np.pi * 28 * t); add(pulse(f, 0.22, 0.5) * np.linspace(1, 0.4, len(t)), te, 0.05)
    elif k_ == 'crunch': add(noise(0.4, 0.12, 16) + 0.6 * sweep(160, 40, 0.4, dec=0.12), te, 0.18, 0.3)
    elif k_ == 'cast':
        for i, m in enumerate([72, 76, 79, 84, 88, 91, 96, 100]): add(pulse(nt(m), 0.08, 0.125, dec=0.05), te + i * 0.028, 0.045, 0.3 - i * 0.06)
    elif k_ == 'stamp': add(noise(0.3, 0.07, 24) + 1.2 * sweep(140, 45, 0.3, dec=0.1), te, 0.22)
    elif k_ == 'bighit': add(noise(0.5, 0.15, 10), te, 0.14); add(sweep(900, 80, 0.4, 0.5, dec=0.15), te, 0.05)
    elif k_ == 'die':
        d = T['fanfare'] - te + 0.05
        add(noise_sweep(d, 6, 40, d * 0.7) , te, 0.14)
        add(sweep(500, 50, d, 0.5) * np.linspace(1, 0, int(d * SR)), te, 0.05)
    elif k_ == 'tick': add(pulse(nt(96), 0.015, 0.5, dec=0.008), te, 0.03)
    elif k_ == 'levelup':
        for i, m in enumerate([72, 76, 79, 84, 79, 84, 88]): add(pulse(nt(m), 0.1, 0.25, dec=0.07), te + i * 0.05, 0.05)
    elif k_ == 'stat': add(pulse(nt(79 + v * 2), 0.05, 0.5, dec=0.03), te, 0.045)
    elif k_ == 'learn':
        for i, m in enumerate([72, 76, 79, 83, 88]): add(tri(nt(m), 1.2, dec=0.5) + 0.25 * pulse(nt(m), 1.2, 0.25, dec=0.3), te + i * 0.05, 0.05, (i - 2) * 0.15)
# ── original victory fanfare (C major) + calm afterglow arpeggio ──
tf = T['fanfare']; q = 0.1
mel = [(72, 1), (76, 1), (79, 1), (84, 3), (83, 1), (79, 1), (81, 1), (84, 5)]
tb = tf
for m, l in mel:
    add(pulse(nt(m), q * l * 0.95, 0.25, dec=0.06 + 0.12 * l), tb, 0.07); add(pulse(nt(m - 12), q * l * 0.95, 0.5, dec=0.05 + 0.1 * l), tb, 0.03, 0.3)
    tb += q * l
for i, m in enumerate([48, 55, 48, 53, 55, 48]): add(tri(nt(m), 0.28), tf + i * 0.24, 0.14)
ta = tf + 1.5; i = 0
chords = [[60, 64, 67, 72], [57, 60, 64, 69], [53, 57, 60, 65], [55, 59, 62, 67]]
while ta < DUR:
    c = chords[(i // 8) % 4]; add(pulse(nt(c[i % 4] + 12), 0.14, 0.25, dec=0.1), ta, 0.022, np.sin(i) * 0.4)
    if i % 4 == 0: add(tri(nt(c[0] - 12), 0.5), ta, 0.09)
    ta += 0.12; i += 1
# master: fade in/out, soft limiter
fi = int(0.05 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.2) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
