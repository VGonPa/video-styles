# events.json → audio.wav (48 kHz stereo, 10 s). Everything synthesized, no samples.
# Cartoon-history-explainer sound: a plucked Karplus-Strong lute jig under the map, mumbled
# "character voices" for each speech bubble, pops, a slide-whistle exit, a whoosh for the zoom,
# war-drum hops, a wooden BONK, a goat bleat, the dramatic "dun dun duuun" sting on the shocked
# face (the jig stops dead on the cut), an hourglass clink + harp run for "37 years later…",
# then a slow, older coda over gentle surf.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR)
L = np.zeros(N); Rr = np.zeros(N)
rs = np.random.RandomState(11)
nt = lambda m: 440.0 * 2 ** ((m - 69) / 12)

def put(sig, t, g=1.0, pan=0.0):
    i = int(round(t * SR)); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    L[i:i + n] += sig[:n] * g * (1 - pan) ** 0.5; Rr[i:i + n] += sig[:n] * g * (1 + pan) ** 0.5

def tt(d): return np.arange(int(d * SR)) / SR
def env(n, a=0.005, r=0.05):
    e = np.ones(n); na, nr = min(n, max(1, int(a * SR))), min(n, max(1, int(r * SR)))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr)
    return e
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    m = 1 / (1 + (lo / np.maximum(f, 1)) ** 4) / (1 + (f / hi) ** 4); return np.fft.irfft(X * m, len(x))
def noise(d): return rs.uniform(-1, 1, int(d * SR))
def ks(f, d, bright=0.5, decay=0.996):
    """Karplus-Strong plucked string."""
    n = int(d * SR); p = max(2, int(SR / f)); buf = rs.uniform(-1, 1, p)
    buf = band(np.concatenate([buf, np.zeros(p)]), 50, 1500 + 6000 * bright)[:p]
    out = np.zeros(n)
    for i in range(0, n, p):
        k = min(p, n - i); out[i:i + k] = buf[:k]
        buf = decay * 0.5 * (buf + np.roll(buf, 1))
    return out * env(n, 0.001, 0.03)
def fm(f, d, ratio=1.0, idx=2.0, idx_dec=0.3):
    t = tt(d); I = idx * np.exp(-t / idx_dec) if idx_dec else idx
    ph = 2 * np.pi * np.cumsum(np.broadcast_to(np.asarray(f, float), t.shape)) / SR
    return np.sin(ph + I * np.sin(ph * ratio))

EV = json.load(open('events.json'))
ev = lambda k, s=None: [e for e in EV if e['k'] == k and (s is None or e.get('s') == s)]

# ── the jig (D major 6/8, eighth = 0.155 s): lute melody + bass, stops dead at the cut ──
m = ev('music', 'jig')[0]; T0, TE = m['t'], m['e']; E8 = 0.155
mel = [(74, 1), (73, 1), (74, 1), (76, 2), (74, 1), (71, 1), (69, 1), (71, 1), (74, 3),
       (78, 1), (76, 1), (74, 1), (73, 2), (71, 1), (69, 2), (66, 1), (69, 3),
       (74, 1), (73, 1), (74, 1), (76, 2), (78, 1), (79, 1), (78, 1), (76, 1), (74, 3),
       (73, 1), (74, 1), (76, 1), (78, 2), (76, 1), (74, 6)]
tq = T0
for n, ln in mel:
    if tq >= TE - 0.02: break
    d = min(ln * E8 + 0.35, TE - tq); put(ks(nt(n), d, 0.6, 0.997), tq, 0.16, 0.2); tq += ln * E8
bass = [50, 57, 50, 57, 55, 57, 50, 45]
for b in range(40):
    tb = T0 + b * 3 * E8
    if tb >= TE - 0.02: break
    d = min(0.5, TE - tb); put(ks(nt(bass[b % 8] - 12), d, 0.3, 0.995), tb, 0.2, -0.25)
    for off in (1, 2):
        tn = tb + off * E8
        if tn < TE - 0.02: put(ks(nt([62, 66, 69][off]), min(0.25, TE - tn), 0.4, 0.99), tn, 0.05, -0.1)

# ── coda: slow, older, over surf (D major, ends on the tonic) ──
m = ev('music', 'coda')[0]; C0 = m['t']
coda = [(62, 0.0), (66, 0.32), (69, 0.64), (74, 1.1), (73, 1.5), (71, 1.72), (69, 2.0), (66, 2.35), (62, 2.7)]
for n, o in coda:
    tn = C0 + o
    if tn < 9.9: put(ks(nt(n), 10 - tn, 0.45, 0.9985), tn, 0.12, 0.15)
for n, o in [(38, 0.0), (45, 1.1), (38, 2.0)]:
    put(ks(nt(n), 10 - (C0 + o), 0.25, 0.999), C0 + o, 0.16, -0.2)
a = ev('sea')[0]; d = 10 - a['t']; t = tt(d)
sw = 0.55 + 0.45 * np.sin(2 * np.pi * t / 2.4 - 1.0) ** 2
put(band(noise(d), 250, 3500) * sw * np.minimum(1, t / 0.3), a['t'], 0.05, 0.25); put(band(noise(d), 60, 300) * np.minimum(1, t / 0.3), a['t'], 0.06, -0.2)

# ── voices: mumbled syllables at the mouth-flap rate (5.5 Hz), per-character timbre ──
for e in ev('babble'):
    t0, t1, v, old = e['t'], e['e'], e['v'], e.get('old', 0)
    base = (150 if v == 'h' else 230) * (0.92 if old else 1.0)
    rate = 5.5; k = 0; ts = t0
    while ts < t1 - 0.05:
        d = 0.13 if not old else 0.15
        tq = tt(d); contour = 1 + 0.18 * np.sin(k * 2.1) + 0.12 * np.sin(np.pi * tq / d)
        vib = 1 + (0.03 if old else 0.008) * np.sin(2 * np.pi * (6.5 if old else 5) * tq)
        f = base * contour * vib
        ratio = 2.0 if v == 'h' else 3.0
        s = fm(f, d, ratio, 2.2 if v == 'h' else 3.0, 0.06) * np.sin(np.pi * tq / d) ** 1.3
        s = band(s, 120, 2600 if v == 'h' else 3600)
        put(s, ts, 0.13, -0.35 if v == 'h' else 0.35); ts += 1 / rate; k += 1

# ── effects ──
for e in EV:
    k, t0 = e['k'], e['t']; p = e.get('p', 0.0)
    if k == 'pop':
        d = 0.09; tq = tt(d); f = 300 + 1400 * (tq / d) ** 0.6
        put(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tq / 0.03), t0, 0.16, p)
    elif k == 'bubble':
        d = 0.07; tq = tt(d); f = 700 + 900 * tq / d
        put(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tq / 0.02), t0, 0.12, 0)
        put(band(noise(0.02), 3000, 9000) * np.exp(-tt(0.02) / 0.004), t0, 0.06, 0)
    elif k == 'drop':  # slide whistle down
        d = 0.42; tq = tt(d); f = 1500 * np.exp(-tq * 3.2) + 250
        s = np.sin(2 * np.pi * np.cumsum(f * (1 + 0.01 * np.sin(2 * np.pi * 9 * tq))) / SR) * env(len(tq), 0.02, 0.1)
        put(s, t0, 0.07, 0)
    elif k == 'whoosh':
        d = 0.65; tq = tt(d); x = noise(d)
        lo = band(x, 150, 900); hi = band(x, 900, 4000); mix = np.sin(np.pi * tq / d)
        put((lo * (1 - tq / d) + hi * (tq / d)) * mix ** 2, t0, 0.22, 0)
    elif k == 'draw':  # marker on paper
        d = 0.36; tq = tt(d); s = band(noise(d), 1800, 5000) * (0.6 + 0.4 * np.sin(2 * np.pi * 14 * tq)) * env(len(tq), 0.02, 0.08)
        put(s, t0, 0.06, p)
    elif k == 'drum':
        d = 0.35; tq = tt(d)
        s = np.sin(2 * np.pi * np.cumsum(90 * np.exp(-tq * 8) + 55) / SR) * np.exp(-tq / 0.12) + 0.35 * band(noise(d), 200, 2000) * np.exp(-tq / 0.03)
        put(s, t0, 0.3, 0)
    elif k == 'bonk':
        d = 0.6; tq = tt(d)
        s = fm(520 * np.exp(-tq * 1.2), d, 1.41, 3.0, 0.08) * np.exp(-tq / 0.16)
        s += 0.9 * np.sin(2 * np.pi * np.cumsum(140 * np.exp(-tq * 6) + 60) / SR) * np.exp(-tq / 0.1)
        put(s, t0, 0.32, 0)
        for j, n in enumerate([88, 91, 95]):  # little cartoon stars
            put(fm(nt(n), 0.3, 3.5, 1.5, 0.06) * np.exp(-tt(0.3) / 0.08), t0 + 0.12 + j * 0.07, 0.035, 0.3 * (j - 1))
    elif k == 'bleat':
        d = 0.42; tq = tt(d); f = 520 * (1 + 0.06 * np.sin(2 * np.pi * 7.5 * tq)) * (1 - 0.1 * tq / d)
        s = fm(f, d, 1.0, 2.5, 0) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 7.5 * tq))) * env(len(tq), 0.02, 0.12)
        put(band(s, 300, 3500), t0, 0.07, p)
    elif k == 'cut':
        put(band(noise(0.03), 1500, 8000) * np.exp(-tt(0.03) / 0.006), t0, 0.14, 0)
    elif k == 'sting':  # dun dun duuun
        for j, (n, o, d) in enumerate([(43, 0.0, 0.16), (43, 0.17, 0.16), (39, 0.36, 0.7)]):
            tq = tt(d); f = nt(n)
            saw = sum(np.sin(2 * np.pi * f * h * tq) / h for h in range(1, 12))
            lo_ = band(saw, 60, 700); s = (lo_ + (band(saw, 60, 2400) - lo_) * np.exp(-tq / 0.2)) * env(len(tq), 0.012, 0.12 if j < 2 else 0.3)
            s += 0.5 * np.sin(2 * np.pi * f / 2 * tq) * env(len(tq), 0.01, 0.1)
            put(s, e['t'] + o, 0.2, 0)
        tq = tt(0.8); put(np.sin(2 * np.pi * 45 * tq) * np.exp(-tq / 0.3), e['t'], 0.2, 0)
    elif k == 'card':
        put(fm(2400, 0.4, 2.76, 1.5, 0.05) * np.exp(-tt(0.4) / 0.08), t0 + 0.2, 0.04, 0.2)  # glass clink
        for j, n in enumerate([62, 66, 69, 74, 78, 81, 86]):
            put(ks(nt(n), 0.9, 0.7, 0.997), t0 + 0.05 + j * 0.05, 0.08, -0.5 + j / 6)

st = np.stack([L, Rr], 1)
fi, fo = int(0.02 * SR), int(0.5 * SR)
st[:fi] *= np.linspace(0, 1, fi)[:, None]; st[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
st = np.tanh(st * 1.6) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
