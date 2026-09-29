# events.json → audio.wav (48 kHz stereo, 10 s)
# An evening plaza: murmur and crickets, string-light filaments ticking on, tissue banners rustling as they unroll
# with a soft flap, a gust of wind, and a little marimba-and-plucked-strings waltz in C that climbs with the tilt,
# sounds a note for each cut-paper letter, sparkles with the twinkling lamps and settles on a last chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(106)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        pan = float(np.clip(pan, -1, 1))
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)

def marimba(f, d=0.9):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 5) + 0.35 * np.sin(2 * np.pi * f * 3.93 * t) * np.exp(-t * 18) + 0.12 * np.sin(2 * np.pi * f * 9.2 * t) * np.exp(-t * 40)
    return s * np.minimum(1, t / 0.0015)
def pluck(f, d=1.0, bright=0.5):
    n = int(d * SR); p = max(2, int(SR / f)); buf = rs.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]; j = (i + 1) % p; buf[i % p] = (0.5 + bright * 0.0) * (buf[i % p] + buf[j]) * 0.996
    return band(out, 80, 6000) * np.minimum(1, np.arange(n) / 25)
def rustle(d, lo=1200, hi=7000, crackle=0.6):
    t = tt(d); x = band(rs.standard_normal(len(t)), lo, hi)
    am = np.abs(band(rs.standard_normal(len(t)), 2, 25)); am /= am.max() + 1e-9
    cr = np.zeros(len(t)); idx = rs.integers(0, len(t), int(d * 90)); cr[idx] = rs.uniform(-1, 1, len(idx)); cr = band(cr, 1500, 9000)
    return (norm(x) * am + norm(cr) * crackle) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.8
def flap():
    t = tt(0.14); return (np.sin(2 * np.pi * (140 + 90 * np.exp(-t * 30)) * t) * np.exp(-t / 0.025) * 0.6 + band(rs.standard_normal(len(t)), 300, 2500) * np.exp(-t / 0.02))
def tick():
    t = tt(0.05); return band(rs.standard_normal(len(t)), 2500, 9000) * np.exp(-t / 0.004) + np.sin(2 * np.pi * 3200 * t) * np.exp(-t / 0.01) * 0.3
def whoosh(d, lo=200, hi=2500):
    t = tt(d); x = band(rs.standard_normal(len(t)), lo, hi); env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.6
    am = 0.6 + 0.4 * np.abs(band(rs.standard_normal(len(t)), 0.5, 4)) / 0.02; am = np.clip(am / am.max(), 0.3, 1)
    return norm(x) * env * am
def bell(f, d=1.2):
    t = tt(d); return (np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 7)) * np.exp(-t * 3.5)
def pad(fs, d):
    t = tt(d); s = sum(np.sin(2 * np.pi * f * t + k) + 0.3 * np.sin(4 * np.pi * f * t) for k, f in enumerate(fs))
    return s / len(fs) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2

ev = json.load(open('events.json'))
T = np.arange(N) / SR
# plaza ambience: murmur + crickets
mur = norm(band(rs.standard_normal(N), 180, 1100)) * (0.7 + 0.3 * np.abs(band(rs.standard_normal(N), 0.3, 3)) / 0.004).clip(0, 1.4)
L += mur * 0.012; R += np.roll(mur, 2311) * 0.012
for k in range(2):
    ph = rs.uniform(0, 1); f0 = 4300 + k * 600; puls = (np.sin(2 * np.pi * (2.6 + k * 0.7) * T + ph * 6) > 0.55) * (np.sin(2 * np.pi * 38 * T) > 0)
    cri = np.sin(2 * np.pi * f0 * T) * puls; cri = band(cri, 3000, 7000)
    (L if k == 0 else R)[:] += cri * 0.004

# waltz in C, 3/4 at 132 bpm: bass on 1, plucked chord on 2 and 3
BEAT = 60 / 132; START = 0.45
CH = [('C', 48, [60, 64, 67]), ('G', 43, [59, 62, 65, 67]), ('C', 48, [60, 64, 67]), ('F', 41, [60, 65, 69]), ('C', 48, [60, 64, 67]), ('G', 43, [59, 62, 65, 67]), ('C', 48, [60, 64, 67])]
end_t = next(e['t'] for e in ev if e['k'] == 'end')
for b, (_, bass, ch) in enumerate(CH):
    t0 = START + b * 3 * BEAT
    if t0 > end_t + 0.3: break
    add(pluck(nt(bass), 1.2), t0, 0.16, -0.2)
    for beat in (1, 2):
        tb = t0 + beat * BEAT
        if tb > end_t + 0.1: break
        for j, m in enumerate(ch): add(pluck(nt(m), 0.6), tb + j * 0.008, 0.045, 0.25)
# marimba melody (gentle, leaves room for the title notes)
MEL = [(0, 67), (1, 72), (2, 76), (3, 74), (4, 71), (5, 67), (6, 69), (7, 72), (8, 77), (9, 76), (10, 72), (11, 67)]
for k, m in MEL:
    t0 = START + 3 * BEAT + k * BEAT * 1.5
    if t0 > 5.8: break
    add(marimba(nt(m)), t0, 0.08, 0.1 * np.sin(k))
pan_of = lambda e: e.get('pan', 0.0)
PENTA = [72, 74, 76, 79, 81, 84, 86, 88]
for e in ev:
    k, te = e['k'], e['t']
    if k == 'bulb': add(tick(), te, 0.05, pan_of(e) * 0.8)
    elif k == 'unfurl':
        s = e['s']; add(rustle(0.55, 1000 if s > 1 else 1600, 7000), te, 0.03 + 0.04 * s, pan_of(e) * 0.85); add(flap(), te + 0.6, 0.05 * s + 0.02, pan_of(e) * 0.85)
    elif k == 'gust':
        add(whoosh(2.3, 150, 2200), te, 0.09, -0.3); add(rustle(2.0, 1500, 8000, 0.9), te + 0.4, 0.06, 0.2)
    elif k == 'glow': add(pad([nt(60), nt(64), nt(67), nt(72)], 1.8), te, 0.05, 0.0)
    elif k == 'tilt':
        add(whoosh(e['d'], 300, 3500), te, 0.05, 0.0)
        for i, m in enumerate([60, 62, 64, 67, 69, 72, 74, 76]): add(marimba(nt(m), 0.6), te + 0.2 + i * 0.14, 0.06, -0.6 + i * 0.17)
    elif k == 'title':
        add(rustle(0.45, 1300, 7000), te, 0.05, pan_of(e)); add(flap(), te + 0.55, 0.06, pan_of(e))
        add(marimba(nt(PENTA[e['i']]), 1.0), te + 0.55, 0.1, pan_of(e) * 0.7)
    elif k == 'caption':
        for i, m in enumerate([72, 76, 79]): add(bell(nt(m + 12), 1.4), te + i * 0.09, 0.03, -0.2 + i * 0.2)
    elif k == 'twinkle':
        for i in range(10): add(bell(nt([84, 88, 91, 93, 96][i % 5]), 0.9), te + i * 0.09, 0.022, -0.9 + i * 0.2)
    elif k == 'end':
        for i, m in enumerate([48, 60, 64, 67, 72]): add(pluck(nt(m), 1.6), te + i * 0.02, 0.1 if m == 48 else 0.05, 0.0)
        for i in range(10): add(marimba(nt(72 + (i % 2) * 4), 0.5), te + 0.1 + i * 0.07, 0.03 * (1 - i / 12), 0.2)
fi = int(0.12 * SR); fo = int(1.0 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.6
st = np.stack([L, R], 1); st = np.tanh(st * 3.0) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
