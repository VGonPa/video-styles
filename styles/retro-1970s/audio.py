# events.json → audio.wav (48 kHz stereo, 10 s) · 70s TV kitchen: TV-on beep, a 120 bpm funk groove
# (kick, hats, bass, clavinet-ish stabs), vegetable boings, letter pops, soup plops, zoom whoosh,
# iris sweep, cake thump, lemon dings, title chime; old TV speaker band-pass; fades with the picture.
import json, wave, numpy as np
SR, DUR, BPM = 48000, 10.0, 120
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(13)
BEAT = 60 / BPM
tm = np.arange(N) / SR
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def sweep(f0, f1, d, dec, shape='sine'):
    t = tt(d); f = f0 * (f1 / f0) ** (t / d); ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) if shape == 'sine' else (2 * ((ph / (2 * np.pi)) % 1) - 1)
    return s * np.minimum(1, t / 0.003) * np.exp(-t / dec)
def kick():
    t = tt(0.3); f = 50 + 110 * np.exp(-t * 30); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.09)
def hat(d=0.04, dec=0.01):
    t = tt(d); n = band(rs.standard_normal(len(t)), 6000, 14000)
    return n / (np.abs(n).max() + 1e-9) * np.exp(-t / dec)
def bass(f, d):
    t = tt(d); s = np.zeros(len(t))
    for h in range(1, 7): s += np.sin(2 * np.pi * f * h * t) / h * (0.8 ** h)
    return s * np.minimum(1, t / 0.005) * np.exp(-t / 0.18) * np.minimum(1, (d - t) / 0.02)
def clav(freqs, d=0.16):
    t = tt(d); s = np.zeros(len(t))
    for f in freqs:
        for h in range(1, 6): s += np.sign(np.sin(2 * np.pi * f * h * t)) * 0.12 / h
    return band(s, 500, 3200) * np.minimum(1, t / 0.002) * np.exp(-t / 0.05)

# ── groove from 0.5 s on the picture's beat grid (bars alternate F / Bb) ──
music = np.zeros(N)
def madd(sig, t, g):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0: music[i:i + n] += sig[:n] * g
BASSLINE = [(0, 1.0), (0.75, 1.0), (1.5, 1.5), (2.0, 4 / 3), (2.75, 4 / 3), (3.5, 9 / 8)]  # (beat offset, ratio to root)
STABS = [0.5, 1.5, 2.75, 3.25]
bar, b = 4 * BEAT, 0
while 0.5 + b * bar < DUR:
    base = 0.5 + b * bar
    for k in range(4):
        madd(kick(), base + k * BEAT, 0.5)
        madd(hat(), base + k * BEAT + BEAT / 2, 0.12)
        madd(hat(0.1, 0.03), base + k * BEAT + BEAT * 0.75, 0.05)
    root = 87.31 if b % 2 == 0 else 116.54
    for off, r in BASSLINE: madd(bass(root * r, 0.22), base + off * BEAT, 0.35)
    chord = [349.23, 440.0, 523.25, 659.25] if b % 2 == 0 else [466.16, 587.33, 698.46]
    for off in STABS: madd(clav(chord), base + off * BEAT, 0.16)
    b += 1
# music comes in after the TV switches on and ducks under the crash zoom
music *= np.clip((tm - 0.4) / 0.3, 0, 1) * (1 - 0.7 * np.exp(-((tm - 4.55) / 0.18) ** 2))
add(music, 0, 1.0)

ev = json.load(open('events.json'))
for e in sorted(ev, key=lambda e: e['t']):
    k, t, v = e['k'], e['t'], e.get('v', 0)
    side = -0.5 if v < 2 else 0.5
    if k == 'on': add(sweep(180, 900, 0.18, 0.08), t, 0.35); add(sweep(1200, 1200, 0.12, 0.05), t + 0.16, 0.12)
    elif k == 'ident': add(sweep(660, 1320, 0.12, 0.05), t, 0.12, 0.6); add(sweep(990, 990, 0.2, 0.08), t + 0.1, 0.1, 0.6)
    elif k == 'land':  # cartoon boing
        x = tt(0.35); f = 220 + 140 * v + 60 * np.sin(2 * np.pi * 14 * x) * np.exp(-x / 0.15)
        add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / 0.12), t, 0.22, side)
    elif k == 'bounce': add(sweep(300 + 60 * v, 520 + 60 * v, 0.06, 0.03), t, 0.05, side)
    elif k == 'hop': add(sweep(300, 900, 0.18, 0.1), t, 0.12, side)
    elif k == 'plop':
        x = tt(0.25); f = 900 * np.exp(-x * 14) + 180
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / 0.06)
        n = band(rs.standard_normal(len(x)), 800, 5000) * np.exp(-x / 0.05)
        add(s + 0.3 * n / (np.abs(n).max() + 1e-9), t, 0.3, side * 0.6)
    elif k == 'pop': f = 520 + 45 * v; add(sweep(f * 0.6, f * 1.4, 0.09, 0.03), t, 0.2, (v - 5) / 8)
    elif k == 'whoosh':  # rising band-passed noise into the crash zoom
        d = 0.55; x = tt(d); n = rs.standard_normal(len(x)); s = np.zeros(len(x)); ch = 1200
        for i in range(0, len(x), ch):
            u = i / len(x); s[i:i + ch] = band(n[i:i + ch], 300 + 3000 * u, 1200 + 6000 * u)
        add(s / (np.abs(s).max() + 1e-9) * (x / d) ** 1.5, t, 0.35)
    elif k == 'iris': add(sweep(250, 1400, 0.5, 0.35, 'saw') * 0.4, t, 0.14)
    elif k == 'thump': add(kick(), t, 0.5); add(sweep(180, 90, 0.3, 0.1), t, 0.25)
    elif k == 'ding':
        f = [1318.5, 1567.98, 1975.5][v]; x = tt(0.6)
        add((np.sin(2 * np.pi * f * x) + 0.3 * np.sin(2 * np.pi * 2.76 * f * x)) * np.exp(-x / 0.18), t, 0.1, (v - 1) * 0.5)
    elif k == 'chime':
        n = int(1.8 * SR); x = np.arange(n) / SR; s = np.zeros(n)
        for j, f in enumerate([523.25, 659.25, 783.99, 1046.5]):
            o = int(j * 0.07 * SR); xx = x[:n - o]; vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * xx)
            s[o:] += (np.sin(2 * np.pi * f * vib * xx) + 0.3 * np.sin(4 * np.pi * f * xx)) * np.exp(-xx / 0.55)
        add(s * np.minimum(1, x / 0.01), t, 0.14)

# old TV speaker: band-pass + soft limiting; the fade matches the picture's soft fade
out = np.stack([band(L, 150, 7000), band(R, 150, 7000)])
out = np.tanh(out * 1.3) * 0.8
out *= np.clip((9.98 - tm) / 0.86, 0, 1) ** 1.5
pcm = (np.clip(out.T, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok')
