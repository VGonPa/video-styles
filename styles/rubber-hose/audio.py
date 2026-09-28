# events.json → audio.wav (48 kHz stereo, 10 s)
# Jaunty honky-tonk ragtime piano (stride bass "oom-pah" + syncopated melody, 120 bpm) that stops dead on the gag,
# slide whistle (falling cube / spring back up), wood-block BONK + jaw-harp BOING, star tings, shake rattle,
# tap-shoe clicks, plop, title thuds — all through a narrow optical-soundtrack band with projector rattle and crackle.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(41)
BEAT = 0.5
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def norm(x): return x / (np.abs(x).max() + 1e-9)

# ── honky-tonk piano: inharmonic partials, two detuned strings, hammer knock, damper release ──
def piano(m, dur, vel=1.0):
    f0 = nt(m); t = tt(dur + 0.6); s = np.zeros(len(t))
    for det in (-5, 6):                                         # cents: the out-of-tune saloon upright
        f = f0 * 2 ** (det / 1200)
        for k in range(1, 9):
            fk = f * k * np.sqrt(1 + 0.0004 * k * k)
            if fk > 9000: break
            s += (1 / k ** 1.15) * np.sin(2 * np.pi * fk * t + k) * np.exp(-t * (1.1 + 0.55 * k + f0 / 900))
    s *= 0.5
    ham = band(rs.standard_normal(len(t)), 300, 3000) * np.exp(-t / 0.006)
    s += 0.25 * norm(ham) * vel
    rel = np.where(t > dur, np.exp(-(t - dur) * 14), 1.0)
    att = np.minimum(1, t / 0.002)
    return s * rel * att * vel

def slide(f0, f1, d, curve=1.0):
    t = tt(d); u = (t / d) ** curve
    f = f0 * (f1 / f0) ** u * (1 + 0.018 * np.sin(2 * np.pi * 6 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.05 * np.sin(3 * ph)
    breath = band(rs.standard_normal(len(t)), 1500, 5000) * 0.06
    env = np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.05)
    return (s + breath) * env
def bonk():
    t = tt(0.3)
    s = np.sin(2 * np.pi * 540 * t) * np.exp(-t / 0.05) + 0.6 * np.sin(2 * np.pi * 1320 * t) * np.exp(-t / 0.02)
    s += 0.9 * np.sin(2 * np.pi * (140 * np.exp(-t * 6) + 60) * t) * np.exp(-t / 0.08)
    s += 0.5 * norm(band(rs.standard_normal(len(t)), 1500, 8000)) * np.exp(-t / 0.004)
    return s
def boing():
    t = tt(1.1); f = 150 * (1 + 0.45 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 2.2)) * (1 + 0.25 * np.exp(-t * 6))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.55 * np.sin(2 * ph) + 0.35 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph)
    return s * np.exp(-t / 0.4) * np.minimum(1, t / 0.005)
def ting(f=2600):
    t = tt(0.5); return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 20)) * np.exp(-t / 0.14)
def block(f):
    t = tt(0.06); return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.012) + 0.3 * norm(band(rs.standard_normal(len(t)), 2000, 7000)) * np.exp(-t / 0.003)
def tap():
    t = tt(0.08); c = norm(band(rs.standard_normal(len(t)), 2200, 8000)) * np.exp(-t / 0.006)
    return c + 0.5 * np.sin(2 * np.pi * 380 * t) * np.exp(-t / 0.015)
def thud():
    t = tt(0.25); return np.sin(2 * np.pi * (90 * np.exp(-t * 10) + 70) * t) * np.exp(-t / 0.06) + 0.25 * norm(band(rs.standard_normal(len(t)), 200, 1500)) * np.exp(-t / 0.01)
def pop():
    t = tt(0.12); f = 500 + 900 * np.exp(-t * 40); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.03)
def plop():
    t = tt(0.4); f = 950 * np.exp(-t * 18) + 160
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.07)
    s += 0.35 * norm(band(rs.standard_normal(len(t)), 800, 5000)) * np.exp(-t / 0.05) * np.minimum(1, t / 0.01)
    return s
def swish(d):
    t = tt(d); x = band(rs.standard_normal(len(t)), 400, 3000); return norm(x) * np.sin(np.pi * t / d) ** 2

# ── music: stride bass on the beat, chord on the off-beat, syncopated right hand ──
CH = {'C': ([36, 43], [55, 60, 64]), 'A7': ([45, 40], [55, 61, 64]), 'D7': ([38, 45], [54, 57, 60]),
      'G7': ([43, 38], [53, 59, 62]), 'F': ([41, 36], [53, 57, 60])}
bar_map = {}                                                     # beat index → chord
for b in range(0, 6): bar_map[b] = 'C'
bar_map.update({6: 'A7', 7: 'A7', 8: 'D7', 9: 'D7', 10: 'G7', 13: 'G7', 14: 'C', 16: 'F', 17: 'G7', 18: 'C'})
for b, ch in bar_map.items():
    bass, chord = CH[ch]
    tb = b * BEAT
    if b in (14, 18):                                            # ta-da / final: full two-hand chord, rolled
        for i, m in enumerate([bass[0] - 12 + 12, bass[0] + 12] + chord + [chord[-1] + 12]):
            add(piano(m, 1.6 if b == 18 else 0.9, 0.9), tb + i * 0.018, 0.22, -0.3 + i * 0.1)
        continue
    add(piano(bass[b % 2], 0.22, 1.0), tb, 0.30, -0.25)          # oom
    add(piano(bass[b % 2] - 12, 0.22, 0.6), tb, 0.16, -0.25)
    if b not in (10, 13):
        for m in chord: add(piano(m, 0.12, 0.7), tb + BEAT / 2, 0.13, 0.1)   # pah
MEL = [(0.5, 67, .5), (1, 69, .25), (1.25, 72, .5), (1.75, 76, .25), (2, 74, .5), (2.5, 72, .25), (2.75, 69, .5),
       (3.25, 67, .75), (4, 64, .25), (4.25, 67, .25), (4.5, 72, 1.0),
       (6, 76, .25), (6.25, 77, .25), (6.5, 76, .5), (7, 73, .25), (7.25, 76, .5), (7.75, 79, .25),
       (8, 78, .25), (8.25, 74, .25), (8.5, 78, .5), (9, 81, .5), (9.5, 78, .25), (9.75, 74, .25),
       (10, 79, .25),
       (13, 71, .25), (13.25, 74, .25), (13.5, 77, .25), (13.75, 79, .25), (14, 84, 1.0),
       (16, 81, .5), (16.5, 77, .25), (16.75, 81, .25), (17, 79, .5), (17.5, 77, .25), (17.75, 74, .25), (18, 84, 1.4)]
for b, m, d in MEL:
    add(piano(m, d * BEAT * 0.9, 0.9), b * BEAT, 0.20, 0.25)
    add(piano(m - 12, d * BEAT * 0.9, 0.5), b * BEAT, 0.08, 0.25)   # octave doubling, ragtime style

for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'thud': add(thud(), te, 0.35 * v, rs.uniform(-.3, .3))
    elif k == 'pop': add(pop(), te, 0.18 * v, rs.uniform(-.2, .2))
    elif k == 'tap': add(tap(), te, 0.22 * v, 0.1 if int(te * 4) % 2 else -0.1)
    elif k == 'fall': add(slide(1900, 480, e['d'], 0.8), te, 0.16)
    elif k == 'rise': add(slide(420, 1700, e['d'], 1.3), te, 0.16)
    elif k == 'bonk': add(bonk(), te, 0.45)
    elif k == 'boing': add(boing(), te, 0.28)
    elif k == 'ting': add(ting(2400 + 500 * rs.random()), te, 0.10 * v, rs.uniform(-.5, .5))
    elif k == 'shake':
        for i in range(int(e['d'] * 24)): add(block(700 if i % 2 else 900), te + i / 24, 0.22, -0.4 if i % 2 else 0.4)
    elif k == 'plop': add(plop(), te, 0.35)
    elif k == 'swish': add(swish(e['d']), te, 0.035)

# ── optical soundtrack character: band-limit, projector rattle, crackle, hiss ──
L = band(L, 110, 6500); R = band(R, 110, 6500)
t = np.arange(N) / SR
rattle = band(rs.standard_normal(N), 800, 4000) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 24 * t))) * 0.006
hiss = band(rs.standard_normal(N), 2000, 7000) * 0.004
crk = np.zeros(N); idx = rs.integers(0, N - 200, 90)
for i in idx: crk[i:i + 40] += rs.uniform(-1, 1) * np.exp(-np.arange(40) / 6) * rs.uniform(.02, .08)
L += rattle + hiss + crk; R += rattle + np.roll(hiss, 911) + crk
fi = int(0.3 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.5) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
