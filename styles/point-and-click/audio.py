# events.json → audio.wav (48 kHz stereo, 10 s)
# Early-90s sound-card style: 2-operator FM synthesis (like the OPL chips of the era) for a jaunty
# 6/8 tavern shanty and a quiet moonlit coda, plus synthesized ambience and effects: harbour surf and
# gulls, door creak, footsteps (boards / sand), parrot squawks, pickup chime, fish-lever clunk,
# stone-door rumble, iris sweeps, beach surf, paper rustle. No samples.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR)
L = np.zeros(N); Rr = np.zeros(N)
rs = np.random.RandomState(7)
nt = lambda m: 440.0 * 2 ** ((m - 69) / 12)

def put(sig, t, g=1.0, pan=0.0):
    i = int(round(t * SR)); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    L[i:i + n] += sig[:n] * g * (1 - pan) ** 0.5 * 1.0; Rr[i:i + n] += sig[:n] * g * (1 + pan) ** 0.5 * 1.0

def tt(d): return np.arange(int(d * SR)) / SR
def adsr(n, a=0.005, d=0.1, s=0.6, r=0.05):
    t = np.arange(n) / SR; e = np.minimum(1, t / max(a, 1e-4)); e = e * (s + (1 - s) * np.exp(-np.maximum(0, t - a) / d))
    rl = min(n, int(r * SR)); e[-rl:] *= np.linspace(1, 0, rl); return e
def fm(f, d, ratio=1.0, idx=2.0, idx_dec=0.3, fb=0.0):
    t = tt(d); I = idx * np.exp(-t / idx_dec) if idx_dec else idx
    ph = 2 * np.pi * np.cumsum(np.broadcast_to(np.asarray(f, float), t.shape)) / SR
    return np.sin(ph + I * np.sin(ph * ratio + fb * np.sin(ph * ratio)))
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    m = 1 / (1 + (lo / np.maximum(f, 1)) ** 4) / (1 + (f / hi) ** 4); return np.fft.irfft(X * m, len(x))
def noise(d): return rs.uniform(-1, 1, int(d * SR))

EV = json.load(open('events.json'))
ev = lambda k, s=None: [e for e in EV if e['k'] == k and (s is None or e.get('s') == s)]

# ── harbour ambience (0 → cut): surf swell + two gulls ──
a = ev('amb', 'harbour')[0]; d = a['e'] - a['t'] + 0.03; t = tt(d)
surf = band(noise(d), 120, 1500) * (0.55 + 0.45 * np.sin(2 * np.pi * t / 2.6 + 1.2)) * 0.9
e = np.ones(len(t)); e[:int(0.3 * SR)] = np.linspace(0, 1, int(0.3 * SR)); e[-int(0.03 * SR):] = np.linspace(1, 0, int(0.03 * SR))
put(surf * e, a['t'], 0.16, -0.2); put(band(noise(d), 60, 300) * e, a['t'], 0.12, 0.2)
for g0, p in [(0.25, 0.5), (0.72, -0.4)]:
    gd = 0.32; gt = tt(gd); f = 1500 + 700 * np.sin(np.pi * gt / gd) - 500 * gt / gd
    s = fm(f, gd, 2.0, 1.2, 0) * np.sin(np.pi * gt / gd) ** 1.5; put(s, g0, 0.035, p); put(s[: len(s) // 2], g0 + 0.36, 0.028, p)

# ── tavern shanty (6/8, D minor, eighth = 1/6 s), OPL-style voices ──
m = ev('music', 'tavern')[0]; T0, TE = m['t'], m['e']; E8 = 1 / 6
mel = [(69, 2), (74, 1), (74, 2), (76, 1), (77, 2), (76, 1), (74, 2), (69, 1), (70, 2), (69, 1), (67, 2), (64, 1), (65, 2), (67, 1), (69, 3),
       (69, 2), (74, 1), (74, 2), (76, 1), (77, 1), (79, 1), (77, 1), (76, 2), (72, 1), (74, 6)]
chords = [[62, 65, 69], [62, 65, 69], [62, 67, 70], [61, 64, 69], [62, 65, 69], [60, 64, 67], [62, 65, 69]]
roots = [50, 50, 43, 45, 50, 48, 50]
def mgain(t0):  # music fades out under the iris
    return 1.0 if t0 < TE - 0.5 else max(0.0, (TE - t0) / 0.5)
tq = T0 + 0.05
for n, ln in mel:
    if tq >= TE: break
    d = ln * E8 * 0.92; s = fm(nt(n), d, 1.0, 2.4, 0.08, 0.3) * adsr(int(d * SR), 0.004, 0.12, 0.35, 0.03)
    s += 0.35 * fm(nt(n) * 2.003, d, 1.0, 0.8, 0.05) * adsr(int(d * SR), 0.004, 0.06, 0.1, 0.03)
    put(s, tq, 0.10 * mgain(tq), 0.15); tq += ln * E8
for b in range(7):
    tb = T0 + 0.05 + b * 1.0
    if tb >= TE: break
    for k, (off, note) in enumerate([(0, roots[b]), (3, roots[b] + 7)]):
        tn = tb + off * E8; d = 0.3
        if tn < TE: put(fm(nt(note), d, 0.5, 3.0, 0.1) * adsr(int(d * SR), 0.003, 0.1, 0.4, 0.04), tn, 0.16 * mgain(tn), -0.1)
    for off in (1, 2, 4, 5):
        tn = tb + off * E8
        if tn >= TE: continue
        d = 0.13; s = sum(fm(nt(c) * (1 + 0.002 * j), d, 2.0, 1.2, 0.06) for j, c in enumerate(chords[b])) / 3
        put(s * adsr(int(d * SR), 0.006, 0.05, 0.4, 0.03), tn, 0.07 * mgain(tn), -0.3)
    for off in (0, 3):
        tn = tb + off * E8
        if tn < TE: put(band(noise(0.05), 2000, 9000) * adsr(int(0.05 * SR), 0.001, 0.015, 0, 0.01), tn, 0.03 * mgain(tn), 0.3)

# ── moonlit coda (beach): FM celesta arpeggio resolving to D major, over sustained pad ──
m = ev('music', 'beach')[0]; B0 = m['t']
arp = [62, 69, 74, 77, 81, 77, 74, 69, 67, 70, 74, 79, 78, 74, 69, 66]
for i, n in enumerate(arp):
    tn = B0 + i * 0.13; d = 0.9
    put(fm(nt(n), d, 3.5, 1.6, 0.12) * adsr(int(d * SR), 0.003, 0.35, 0.0, 0.1), tn, 0.05 * (1 - 0.3 * (i / 16)), 0.4 * np.sin(i))
for i, ch in enumerate([[50, 57, 62, 65], [55, 62, 67, 70], [50, 57, 62, 66, 69]]):
    tn = B0 + i * 0.7; d = 2.3 - i * 0.6 if i < 2 else 10 - tn
    s = sum(fm(nt(c), d, 1.0, 0.6, 0) * (1 + 0 * j) for j, c in enumerate(ch)) / len(ch)
    env = adsr(int(d * SR), 0.25, 1.0, 0.8, 0.5); put(s * env, tn, 0.07, 0)

# ── beach ambience ──
a = ev('amb', 'beach')[0]; d = a['e'] - a['t']; t = tt(d)
sw = 0.5 + 0.5 * np.sin(2 * np.pi * (t / 2.2) - 1.2) ** 2
e = np.minimum(1, t / 0.35)
put(band(noise(d), 300, 5000) * sw * e, a['t'], 0.10, 0.2); put(band(noise(d), 50, 400) * e, a['t'], 0.14, -0.2)
for k in range(10):
    tc = a['t'] + 0.3 + k * 0.23 + rs.uniform(0, 0.05)
    put(np.sin(2 * np.pi * 4700 * tt(0.03)) * adsr(int(0.03 * SR), 0.002, 0.01, 0, 0.01), tc, 0.006, 0.6)

# ── effects ──
for e in EV:
    k, t0 = e['k'], e['t']
    if k == 'click':
        put(fm(1320, 0.025, 1.0, 1.0, 0.01) * adsr(int(0.025 * SR), 0.001, 0.01, 0, 0.01), t0, 0.03)
    elif k == 'step':
        if e['s'] == 'wood':
            d = 0.08; s = band(noise(d), 80, 900) * adsr(int(d * SR), 0.001, 0.018, 0, 0.02) + 0.6 * np.sin(2 * np.pi * 110 * tt(d)) * np.exp(-tt(d) / 0.02)
            put(s, t0, 0.10, -0.1)
        else:
            d = 0.12; put(band(noise(d), 800, 6000) * adsr(int(d * SR), 0.01, 0.04, 0, 0.03), t0, 0.05)
    elif k == 'door':
        d = 0.42; tq = tt(d); f = 330 + 90 * np.sin(2 * np.pi * 7 * tq) * np.exp(-tq * 2) + 60 * tq
        put(fm(f, d, 1.51, 4 + 2 * np.sin(2 * np.pi * 23 * tq), 0) * adsr(int(d * SR), 0.03, 0.25, 0.5, 0.08), t0, 0.035, 0.3)
        put(band(noise(0.03), 1500, 6000) * adsr(int(0.03 * SR), 0.001, 0.008, 0, 0.01), t0 - 0.04, 0.08, 0.3)
    elif k == 'squawk':
        d = 0.2; tq = tt(d); f = 1100 + 900 * np.sin(np.pi * tq / d) ** 0.7
        s = fm(f, d, 1.01, 5.0, 0, 0.8) * adsr(int(d * SR), 0.005, 0.08, 0.6, 0.04) + 0.3 * band(noise(d), 1500, 5000) * adsr(int(d * SR), 0.002, 0.04, 0.2, 0.03)
        put(s, t0 - 0.1, 0.05, 0.55)
    elif k == 'pick':
        for i, n in enumerate([81, 86, 90]): d = 0.35; put(fm(nt(n), d, 3.5, 2.0, 0.08) * adsr(int(d * SR), 0.002, 0.12, 0, 0.05), t0 + i * 0.06, 0.05)
    elif k == 'inv':
        for i, n in enumerate([86, 93]): d = 0.3; put(fm(nt(n), d, 2.0, 1.5, 0.05) * adsr(int(d * SR), 0.002, 0.1, 0, 0.05), t0 + i * 0.08, 0.045)
    elif k == 'clunk':
        d = 0.25; put(np.sin(2 * np.pi * (90 * np.exp(-tt(d) * 6) + 50) * tt(d)) * np.exp(-tt(d) / 0.07), t0, 0.22)
        put(fm(620, 0.12, 1.41, 6, 0.03) * adsr(int(0.12 * SR), 0.001, 0.03, 0, 0.03), t0, 0.06)
    elif k == 'rumble':
        d = e['e'] - t0 + 0.1; tq = tt(d)
        s = band(noise(d), 30, 260) * (0.7 + 0.3 * np.sign(np.sin(2 * np.pi * 20 * tq))) + 0.5 * np.sin(2 * np.pi * 46 * tq)
        put(s * adsr(len(tq), 0.04, 1, 1, 0.1), t0, 0.22)
        put(band(noise(d), 1000, 4000) * adsr(len(tq), 0.1, 0.2, 0.3, 0.1), t0, 0.03)
    elif k == 'thud':
        d = 0.35; put(np.sin(2 * np.pi * (70 * np.exp(-tt(d) * 5) + 35) * tt(d)) * np.exp(-tt(d) / 0.1), t0, 0.28); put(band(noise(d), 100, 1200) * np.exp(-tt(d) / 0.05), t0, 0.1)
    elif k in ('iris', 'irisopen'):
        d = 0.4; tq = tt(d); f = (300 + 900 * tq / d) if k == 'irisopen' else (1200 - 900 * tq / d)
        put(fm(f, d, 0.5, 1.0, 0) * np.sin(np.pi * tq / d) ** 2, t0, 0.025)
    elif k == 'paper':
        for j in range(4): put(band(noise(0.05), 2000, 9000) * adsr(int(0.05 * SR), 0.003, 0.015, 0, 0.02), t0 + j * 0.045 + rs.uniform(0, 0.02), 0.05, -0.2)

# master: soft clip, fades
st = np.stack([L, Rr], 1)
fi, fo = int(0.03 * SR), int(0.45 * SR)
st[:fi] *= np.linspace(0, 1, fi)[:, None]; st[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
st = np.tanh(st * 1.8) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
