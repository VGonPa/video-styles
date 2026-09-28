# events.json -> audio.wav (48 kHz stereo, 10 s). Everything is synthesized (no samples):
# a sea bed with slow swells, a breezy island ukulele strum + marimba line that mellows at sunset,
# a whoosh and a canvas snap for the gust, gull calls, glockenspiel tinks as the windows light,
# a switch clunk and warm swell for the lamp, wooden pops for the title letters and a cartoon
# "bwoop" for the closing iris. Simple FFT-convolution room reverb on the music bus.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
WL = np.zeros(N); WR = np.zeros(N); wet = (WL, WR)
rs = np.random.default_rng(116)
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
def uke(m, d=1.1, vel=0.6):
    """nylon pluck: bright partials with fast per-partial decay"""
    f = nt(m); t = tt(d); s = np.zeros_like(t)
    for n in range(1, 10):
        if n * f > 10000: break
        s += (1 / n ** 1.1) * np.sin(2 * np.pi * n * f * t * (1 + 0.0004 * n) + rs.uniform(0, 6.28)) * np.exp(-t * (2.2 + 1.4 * n))
    return s * np.minimum(1, t / 0.002) * np.minimum(1, (d - t) / 0.05) * vel
def marimba(m, d=1.0, vel=0.6):
    f = nt(m); t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2) + 0.35 * np.sin(2 * np.pi * f * 3.99 * t) * np.exp(-t * 11) + 0.12 * np.sin(2 * np.pi * f * 9.9 * t) * np.exp(-t * 30)
    return s * np.minimum(1, t / 0.0015) * np.minimum(1, (d - t) / 0.05) * vel
def glock(m, d=1.4, vel=0.5):
    f = nt(m); t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 2.2) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 5) + 0.2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 9)
    return s * np.minimum(1, t / 0.001) * vel
def pad(ms, d, att=1.2, rel=1.5):
    t = tt(d); s = np.zeros_like(t)
    for m in ms:
        for det in (-0.08, 0.0, 0.07):
            f = nt(m) * 2 ** (det / 12); s += np.sin(2 * np.pi * f * t + rs.uniform(0, 6.28)) + 0.15 * np.sin(4 * np.pi * f * t)
    return s * np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1) / (3 * len(ms))
def noise(d): return rs.standard_normal(int(d * SR))
def whoosh(d, lo=300, hi=3000, peak=0.5):
    t = tt(d); x = noise(d); out = np.zeros_like(t); seg = 2400
    for k in range(0, len(t), seg):       # moving band-pass sweep, crossfaded in blocks
        u = k / len(t); c = lo * (hi / lo) ** np.sin(np.pi * min(1.0, u / (2 * peak)))
        blk = x[k:k + seg * 2]; y = band(blk, c * 0.6, c * 1.6)[:seg]; out[k:k + len(y)] += y
    out /= np.abs(out).max() + 1e-9
    return out * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5
def gull(pan=0.0):
    """kee-ow: an FM glide that rises then falls, two or three syllables"""
    out = np.zeros(int(1.3 * SR))
    for k, (st, dd, f0, f1) in enumerate([(0.0, 0.32, 1900, 1250), (0.36, 0.26, 2050, 1300), (0.66, 0.22, 1800, 1200)]):
        t = tt(dd); f = f0 + (f1 - f0) * (t / dd) ** 0.7 + 180 * np.sin(np.pi * t / dd)
        ph = 2 * np.pi * np.cumsum(f) / SR
        s = np.sin(ph + 1.8 * np.sin(ph * 0.5)) * np.sin(np.pi * t / dd) ** 0.6 * (1 - 0.25 * k)
        i = int(st * SR); out[i:i + len(s)] += s
    return band(out, 700, 7000)
def pop(f=600, d=0.09):
    t = tt(d); return np.sin(2 * np.pi * f * t * (1 + 0.6 * np.exp(-t * 60))) * np.exp(-t * 45)
def clunk():
    t = tt(0.25); return (np.sin(2 * np.pi * 95 * t) * np.exp(-t * 28) + 0.4 * band(noise(0.25), 800, 4000) * np.exp(-t * 60))
def snap():
    t = tt(0.3); x = band(noise(0.3), 150, 2500) * np.exp(-t * 22); return x / (np.abs(x).max() + 1e-9) + 0.6 * np.sin(2 * np.pi * 70 * t) * np.exp(-t * 18)

# --- sea bed: slow swells of brown-ish noise
sea = np.cumsum(noise(DUR)); sea -= np.convolve(sea, np.ones(2000) / 2000, 'same'); sea = band(sea, 60, 2200); sea /= np.abs(sea).max()
sw = 0.55 + 0.45 * np.sin(2 * np.pi * tt(DUR) / 3.3) ** 2
add(sea * sw, 0, 0.16, -0.15); add(np.roll(sea, 30000) * (1.1 - sw), 0, 0.12, 0.2)

# --- music: G major island strum, 100 bpm; mellows into Em-C-D-G at sunset
B = 0.6; strum = [0, 1.5, 2, 3, 3.5]            # calypso-ish accents within a bar (beats)
CH = {'G': [55, 59, 62, 67], 'C': [55, 60, 64, 67], 'D': [57, 62, 66, 69], 'Em': [55, 59, 64, 67], 'Am': [57, 60, 64, 69]}
bars = [(0.15, 'G'), (2.55, 'C'), (4.95, 'D'), (7.35, 'G')]
for b0, c in bars:
    for k, bt in enumerate(strum):
        t0 = b0 + bt * B
        if t0 > 9.2: continue
        for j, m in enumerate(CH[c] if k % 2 == 0 else CH[c][::-1]):
            add(uke(m, 0.9, 0.5 if bt % 1 == 0 else 0.35), t0 + j * 0.012, 0.09 * (0.7 if t0 > 6.6 else 1), -0.25, wet)
    add(marimba(CH[c][0] - 12, 1.2, 0.8), b0, 0.16, 0.0, wet)
    add(marimba(CH[c][0] - 12 + 7, 0.8, 0.6), b0 + 2 * B, 0.12, 0.0, wet)
mel = [(0.75, 74), (1.35, 76), (1.95, 79), (2.55, 76), (3.45, 74), (3.75, 72), (4.35, 71), (4.95, 74), (5.85, 78), (6.15, 76),
       (6.75, 74), (7.35, 71), (7.95, 74), (8.55, 79)]
for t0, m in mel: add(marimba(m, 1.0, 0.55), t0, 0.12, 0.25, wet)
add(pad([55, 62, 67, 71], 3.8, 1.4, 1.8), 6.4, 0.05, 0.0, wet)
add(uke(67, 2.0, 0.5), 9.18, 0.10, -0.2, wet); add(uke(71, 2.0, 0.45), 9.2, 0.09, 0.1, wet); add(uke(74, 2.0, 0.45), 9.22, 0.08, 0.2, wet)

win_n = 0; letters = 0
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'iris': add(pop(420, 0.25)[::-1] * 0.5, te + 0.05, 0.10, 0)
    elif k == 'gust': add(whoosh(1.6, 250, 2600), te, 0.22, 0.3); add(snap(), te + 0.3, 0.16, 0.15)
    elif k == 'gull': add(gull(), te, 0.05, e.get('pan', 0))
    elif k == 'win': add(glock(84 + [0, 2, 4, 7, 9, 12, 14, 16][win_n % 8], 1.4, 0.5), te, 0.05, -0.3 + 0.1 * win_n, wet); win_n += 1
    elif k == 'lamp':
        add(clunk(), te, 0.2, 0.1)
        for j, dt in enumerate([0.06, 0.19, 0.31, 0.44]): add(pop(1800 + 200 * j, 0.03), te + dt, 0.03, 0.1)
        add(pad([67, 71, 74, 79], 2.6, 0.6, 1.5), te + 0.35, 0.07, 0.1, wet)
    elif k == 'letter': add(marimba(79 + [0, 2, 4, 5, 7, 9, 11][letters % 7] + 12 * (letters // 7) - 12, 0.5, 0.5), te + 0.02, 0.07, -0.4 + letters * 0.06, wet); add(pop(500 + 30 * letters, 0.07), te, 0.05, 0); letters += 1
    elif k == 'sub': add(whoosh(0.6, 800, 4000), te, 0.05, -0.3)
    elif k == 'irisout':
        t = tt(0.75); f = 900 * (220 / 900) ** (t / 0.75); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.75) ** 0.5
        add(s, te + 0.02, 0.05, 0)
    elif k == 'close': add(pop(260, 0.18), te + 0.17, 0.14, 0)

# room reverb on the music bus
ir_t = tt(1.8); M = 1 << int(np.ceil(np.log2(N + len(ir_t))))
for dry_ch, wet_ch, seed in ((L, WL, 1), (R, WR, 2)):
    ir = np.random.default_rng(seed).standard_normal(len(ir_t)) * np.exp(-ir_t / 0.4); ir = lp1(ir, 6000); ir /= np.sqrt(np.sum(ir ** 2))
    rev = np.fft.irfft(np.fft.rfft(wet_ch, M) * np.fft.rfft(ir, M), M)[:N]
    dry_ch += wet_ch * 0.85 + rev * 0.25
fi = int(0.04 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); pk = np.abs(st).max(); st = np.tanh(st / pk * 1.3) * 0.75
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok, peak before norm', round(float(pk), 3))
