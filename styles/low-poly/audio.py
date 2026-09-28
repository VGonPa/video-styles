# events.json -> audio.wav (48 kHz stereo, 10 s). Everything is synthesized (no samples):
# an airy high-altitude wind bed, a soft kalimba + marimba arpeggio over a warm pad that mellows at dusk,
# the windmill's blades whooshing past, a hiss as the balloon inflates and burner roars at lift-off,
# glockenspiel tinks as the windows light, a rising reverse swell as the island shrinks, a crystal
# chime + thump when it snaps into the gem, glints, marimba pops for the title letters.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
WL = np.zeros(N); WR = np.zeros(N); wet = (WL, WR)
rs = np.random.default_rng(51)
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
def kalimba(m, d=1.4, vel=0.6):
    f = nt(m); t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 3.0) + 0.25 * np.sin(2 * np.pi * f * 5.02 * t) * np.exp(-t * 16) \
        + 0.1 * np.sin(2 * np.pi * f * 7.1 * t) * np.exp(-t * 30)
    return s * np.minimum(1, t / 0.002) * np.minimum(1, (d - t) / 0.05) * vel
def marimba(m, d=1.0, vel=0.6):
    f = nt(m); t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2) + 0.35 * np.sin(2 * np.pi * f * 3.99 * t) * np.exp(-t * 11) + 0.12 * np.sin(2 * np.pi * f * 9.9 * t) * np.exp(-t * 30)
    return s * np.minimum(1, t / 0.0015) * np.minimum(1, (d - t) / 0.05) * vel
def glock(m, d=1.6, vel=0.5):
    f = nt(m); t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 2.0) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 5) + 0.2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 9)
    return s * np.minimum(1, t / 0.001) * vel
def pad(ms, d, att=1.0, rel=1.2):
    t = tt(d); s = np.zeros_like(t)
    for m in ms:
        for det in (-0.07, 0.0, 0.06):
            f = nt(m) * 2 ** (det / 12); s += np.sin(2 * np.pi * f * t + rs.uniform(0, 6.28)) + 0.12 * np.sin(4 * np.pi * f * t)
    return s * np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1) / (3 * len(ms))
def whoosh(d, lo=300, hi=3000, peak=0.5):
    t = tt(d); x = noise(d); out = np.zeros_like(t); seg = 2400
    for k in range(0, len(t), seg):
        u = k / len(t); c = lo * (hi / lo) ** np.sin(np.pi * min(1.0, u / (2 * peak)))
        blk = x[k:k + seg * 2]; y = band(blk, c * 0.6, c * 1.6)[:seg]; out[k:k + len(y)] += y
    out /= np.abs(out).max() + 1e-9
    return out * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5
def pop(f=600, d=0.09):
    t = tt(d); return np.sin(2 * np.pi * f * t * (1 + 0.6 * np.exp(-t * 60))) * np.exp(-t * 45)
def roar(d):
    t = tt(d); x = band(noise(d), 60, 900); x /= np.abs(x).max() + 1e-9
    return x * np.minimum(1, t / 0.05) * np.clip((d - t) / 0.25, 0, 1) * (1 + 0.3 * np.sin(2 * np.pi * 23 * t))

# --- wind bed: slowly breathing band-limited noise, decorrelated L/R
for pan, seed_shift in ((-0.5, 0), (0.5, 17000)):
    w = band(noise(DUR), 180, 1400); w /= np.abs(w).max()
    env = 0.55 + 0.45 * np.sin(2 * np.pi * tt(DUR) / 4.1 + seed_shift) ** 2
    add(w * env, 0, 0.07, pan)

# --- music: D major, 96 bpm, kalimba arpeggio; mellows into Bm / A at dusk, resolves to D on the gem
B = 60 / 96 / 2   # eighth note
CH = [(0.0, [62, 66, 69, 74], 50), (2.5, [67, 71, 74, 79], 43), (5.0, [59, 62, 66, 71], 47), (6.9, [57, 61, 64, 69], 45)]
ARP = [0, 1, 2, 3, 2, 1, 2, 3]
for k, (t0, ch, bass) in enumerate(CH):
    t1 = CH[k + 1][0] if k + 1 < len(CH) else 7.7
    n = 0; t = t0 + 0.25
    while t < t1 - 0.05:
        m = ch[ARP[n % 8]] + (12 if n % 8 == 3 else 0)
        add(kalimba(m, 1.3, 0.55 if n % 2 == 0 else 0.4), t, 0.08 * (0.8 if t > 5 else 1), -0.3 + 0.6 * ((n % 4) / 3), wet)
        n += 1; t += B
    add(pad(ch, t1 - t0 + 1.0, 0.8, 1.0), t0, 0.05, 0.0, wet)
    add(marimba(bass, 1.6, 0.7), t0 + 0.25, 0.1, 0.0, wet)
# gem resolution: bright D chord with high shimmer
# (gem chord is added with the gem event below)

# windmill blades: a soft whoosh each time a blade passes the top (angle = 1.2 t + 0.15 t^2)
t = tt(DUR); ang = 1.2 * t + 0.15 * t * t
passes = np.where(np.diff(np.floor(ang / (np.pi / 2))) > 0)[0] / SR
for k, tp in enumerate(passes):
    if tp > 7.1: break
    add(whoosh(0.35, 250, 900, 0.5), tp, 0.05, 0.35)

let_n = 0
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'rise': add(whoosh(1.4, 200, 1500, 0.7), te, 0.12, 0)
    elif k == 'inflate': add(band(noise(1.2), 2000, 7000) * np.sin(np.pi * tt(1.2) / 1.2) ** 2, te, 0.035, -0.3)
    elif k == 'burn': add(roar(e['d']), te, 0.16, -0.35)
    elif k == 'lift':
        tl = tt(1.4); f = 300 * 2 ** (tl / 1.4 * 0.6); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tl / 1.4) ** 2
        add(s, te, 0.035, -0.2, wet)
    elif k == 'win': add(glock(86 + [0, 4, 7][e['i']], 1.6, 0.5), te, 0.06, 0.3 - 0.15 * e['i'], wet)
    elif k == 'shrink':
        d = 0.85; tl = tt(d); x = band(noise(d), 400, 6000) * (tl / d) ** 2.5
        add(x / (np.abs(x).max() + 1e-9), te, 0.12, 0)
        f = 220 * 2 ** (tl / d * 2); add(np.sin(2 * np.pi * np.cumsum(f) / SR) * (tl / d) ** 2, te, 0.05, 0, wet)
    elif k == 'gem':
        tl = tt(0.5); add(np.sin(2 * np.pi * 55 * tl) * np.exp(-tl * 9), te, 0.3, 0); add(pad([62, 69, 74, 78, 81], 2.2, 0.05, 1.6), te, 0.07, 0.0, wet)
        for j, m in enumerate([86, 90, 93, 98, 102]): add(glock(m, 2.0, 0.5), te + j * 0.025, 0.07, -0.4 + 0.2 * j, wet)
        add(band(noise(0.8), 5000, 12000) * np.exp(-tt(0.8) * 5), te, 0.05, 0.2)
    elif k == 'glint': add(glock(105, 0.9, 0.4), te, 0.04, 0.3, wet); add(glock(110, 0.7, 0.3), te + 0.04, 0.03, 0.4, wet)
    elif k == 'letter':
        m = [74, 76, 78, 81, 83, 86, 88, 90][let_n % 8]
        add(marimba(m, 0.6, 0.5), te + 0.03, 0.08, -0.4 + let_n * 0.11, wet); add(pop(520 + 40 * let_n, 0.06), te, 0.04, 0); let_n += 1
    elif k == 'sub': add(whoosh(0.7, 900, 4000), te, 0.045, 0.1)

# room reverb on the music bus
ir_t = tt(2.0); M = 1 << int(np.ceil(np.log2(N + len(ir_t))))
for dry_ch, wet_ch, seed in ((L, WL, 1), (R, WR, 2)):
    ir = np.random.default_rng(seed).standard_normal(len(ir_t)) * np.exp(-ir_t / 0.5); ir = lp1(ir, 6500); ir /= np.sqrt(np.sum(ir ** 2))
    rev = np.fft.irfft(np.fft.rfft(wet_ch, M) * np.fft.rfft(ir, M), M)[:N]
    dry_ch += wet_ch * 0.85 + rev * 0.3
fi = int(0.05 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); pk = np.abs(st).max(); st = np.tanh(st / pk * 1.3) * 0.75
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok, peak before norm', round(float(pk), 3))
