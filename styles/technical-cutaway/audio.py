# events.json -> audio.wav (48 kHz stereo, 10 s). Everything is synthesized (no samples):
# a clean explainer bed (soft pad + plucked 8th-note arpeggio, D major), an air whoosh as the
# wheel turns in, a glassy shimmer when the housing goes x-ray, filtered slides + detent clicks as
# each part leaves the axle, soft UI ticks for the callouts, a 3-phase electric hum that swells
# while the coils fire, metal clunks as the parts seat home, a rising spin whir and a closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
WL = np.zeros(N); WR = np.zeros(N); wet = (WL, WR)
rs = np.random.default_rng(80)
def add(sig, t, g=1.0, pan=0.0, dst=None):
    i = int(t * SR); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    l, r = (L, R) if dst is None else dst
    l[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; r[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def lp1(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); p = 0.0
    for i in range(len(x)): p = (1 - a) * x[i] + a * p; y[i] = p
    return y
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def noise(d): return rs.standard_normal(int(d * SR))
def pluck(m, d=0.7, vel=0.5):
    f = nt(m); t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 6) + 0.3 * np.sin(4 * np.pi * f * t) * np.exp(-t * 12) + 0.08 * np.sin(6 * np.pi * f * t) * np.exp(-t * 20)
    return s * np.minimum(1, t / 0.003) * np.minimum(1, (d - t) / 0.05) * vel
def pad(ms, d, att=0.8, rel=1.2):
    t = tt(d); s = np.zeros_like(t)
    for m in ms:
        for det in (-0.07, 0.0, 0.06):
            f = nt(m) * 2 ** (det / 12); s += np.sin(2 * np.pi * f * t + rs.uniform(0, 6.28)) + 0.12 * np.sin(4 * np.pi * f * t)
    return s * np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1) / (3 * len(ms))
def whoosh(d, lo=200, hi=2500, peak=0.5):
    t = tt(d); x = noise(d); out = np.zeros_like(t); seg = 2400
    for k in range(0, len(t), seg):
        u = k / len(t); c = lo * (hi / lo) ** np.sin(np.pi * min(1.0, u / (2 * peak)))
        blk = x[k:k + seg * 2]; y = band(blk, c * 0.6, c * 1.6)[:seg]; out[k:k + len(y)] += y
    out /= np.abs(out).max() + 1e-9
    return out * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5
def click(f=3200, d=0.03):
    t = tt(d); return band(noise(d), f * 0.6, f * 1.6) * np.exp(-t * 180) + 0.4 * np.sin(2 * np.pi * f * 0.5 * t) * np.exp(-t * 120)
def clunk(f=140):
    t = tt(0.35)
    body = np.sin(2 * np.pi * f * t) * np.exp(-t * 22) + 0.5 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 30)
    ring = 0.18 * np.sin(2 * np.pi * f * 9.1 * t) * np.exp(-t * 14) + 0.12 * np.sin(2 * np.pi * f * 13.4 * t) * np.exp(-t * 18)
    return body + ring + 0.35 * band(noise(0.35), 1500, 6000) * np.exp(-t * 90)
def shimmer(d=1.2):
    t = tt(d); s = np.zeros_like(t)
    for k, m in enumerate([86, 90, 93, 97, 98]):
        s += np.sin(2 * np.pi * nt(m) * t + k) * np.exp(-np.maximum(0, t - k * 0.06) * 3) * (t > k * 0.06)
    return s * np.minimum(1, t / 0.01) / 5 + 0.25 * whoosh(d, 2000, 9000, 0.4)

# --- music bed: 110 bpm, D major, gentle 8th-note arpeggio over a pad
B = 60 / 110 / 2
CH = [(0.0, [50, 57, 62, 64, 66, 69]), (2.18, [47, 54, 59, 62, 66, 69]), (4.36, [43, 50, 55, 59, 62, 66]), (6.54, [45, 52, 57, 62, 64, 69]), (8.3, [50, 57, 62, 66, 69, 74])]
for ci, (t0, ch) in enumerate(CH):
    t1 = CH[ci + 1][0] if ci + 1 < len(CH) else 9.6
    add(pad(ch[1:5], t1 - t0 + 0.9, 0.6, 1.0), t0, 0.07, 0.0, wet)
    add(pluck(ch[0] - 12, 1.4, 0.8), t0, 0.14, 0.0, wet)
    pat = [2, 3, 4, 5, 4, 3, 5, 4]
    k = 0; tb = t0 + B
    while tb < t1 - 0.05 and tb < 9.2:
        add(pluck(ch[pat[k % 8]] + 12, 0.5, 0.5), tb, 0.05 * (1.2 if k % 4 == 0 else 1.0), -0.3 + 0.6 * ((k * 3) % 5) / 4, wet)
        k += 1; tb += B
for j, m in enumerate([74, 78, 81, 86]): add(pluck(m, 2.2, 0.5), 8.35 + j * 0.07, 0.07, -0.2 + 0.15 * j, wet)

for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'whoosh': add(whoosh(1.7, 180, 2200, 0.35), te, 0.2, 0.4)
    elif k == 'ghost': add(shimmer(1.3), te, 0.12, 0.1, wet)
    elif k == 'slide':
        i = e['i']; pan = [0.6, -0.6, 0.35, -0.3, 0.15][i]
        add(whoosh(0.55, 500 + 150 * i, 3500, 0.3), te, 0.09, pan); add(click(2600 + 300 * i), te + 0.02, 0.08, pan)
        add(click(1800, 0.04), te + 0.62, 0.05, pan)
    elif k == 'tick': add(pluck(86 + [0, 2, 4, 7, 9, 12][e['i']], 0.25, 0.6), te, 0.05, -0.4 + 0.16 * e['i'], wet); add(click(5000, 0.02), te, 0.04, 0)
    elif k == 'hum':
        d = e['d']; t = tt(d); env = np.minimum(1, t / 0.35) * np.clip((d - t) / 0.45, 0, 1)
        f = 55 + 35 * np.clip(t / d, 0, 1)                        # pitch rises as the rotor speeds up
        ph = 2 * np.pi * np.cumsum(f) / SR
        s = sum(np.sin(n * ph + p0) / n for n in range(1, 12) for p0 in [0])  # buzzy saw
        trem = 0.75 + 0.25 * np.sin(3 * ph / 7)                   # 3-phase beat
        s = band(s * trem, 40, 2400)
        s /= np.abs(s).max() + 1e-9
        add(s * env, te, 0.12, 0.0)
    elif k == 'clunk': add(clunk(120 + 25 * e['i']), te, 0.16, [0.6, -0.6, 0.35, -0.3, 0.15][e['i']])
    elif k == 'spin':
        d = 2.1; t = tt(d); f = 120 + 520 * (t / d) ** 1.4; ph = 2 * np.pi * np.cumsum(f) / SR
        s = band(noise(d), 300, 5000) * (0.5 + 0.5 * np.sin(ph * 0.25)) * 0.5 + 0.3 * np.sin(ph)
        add(s * np.minimum(1, t / 0.6) * np.clip((d - t) / 0.9, 0, 1), te, 0.06, 0.2)
    elif k == 'end': add(pad([62, 66, 69, 74], 1.7, 0.3, 1.2), te + 0.05, 0.08, 0.0, wet)

ir_t = tt(1.6); M = 1 << int(np.ceil(np.log2(N + len(ir_t))))
for dry_ch, wet_ch, seed in ((L, WL, 1), (R, WR, 2)):
    ir = np.random.default_rng(seed).standard_normal(len(ir_t)) * np.exp(-ir_t / 0.35); ir = lp1(ir, 7000); ir /= np.sqrt(np.sum(ir ** 2))
    rev = np.fft.irfft(np.fft.rfft(wet_ch, M) * np.fft.rfft(ir, M), M)[:N]
    dry_ch += wet_ch * 0.85 + rev * 0.22
fi = int(0.03 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); pk = np.abs(st).max(); st = np.tanh(st / pk * 1.3) * 0.75
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok, peak before norm', round(float(pk), 3))
