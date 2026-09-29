# events.json -> audio.wav (48 kHz stereo, 10 s). Everything is synthesized (no samples):
# a light pizzicato + marimba bed in C major (explainer-friendly, never busy), bubbly "bloop" pops for
# blobs appearing, little ticks for food and labels, munch boops for eating, rubbery bonks for the fight,
# a sad slide-whistle deflate for the blobs that don't make it, rising blips for clones, a clock tick per
# day, a granular "crowd bustle" for the fast-forward generations, a whoosh for the pull-out and a warm
# chime under the final caption. Simple FFT-convolution room reverb on the music bus.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
WL = np.zeros(N); WR = np.zeros(N); wet = (WL, WR)
rs = np.random.default_rng(77)
def add(sig, t, g=1.0, pan=0.0, dst=None):
    i = int(t * SR); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    pan = float(np.clip(pan, -1, 1)); l, r = (L, R) if dst is None else dst
    l[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; r[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def noise(d): return rs.standard_normal(int(d * SR))
def chirp(f0, f1, d, shape=1.0):
    t = tt(d); f = f0 * (f1 / f0) ** ((t / d) ** shape); return np.sin(2 * np.pi * np.cumsum(f) / SR), t
def bloop(f0=380, f1=900, d=0.13):
    s, t = chirp(f0, f1, d, 0.6); return s * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.8
def tick(f=2600, d=0.03):
    t = tt(d); return np.sin(2 * np.pi * f * t) * np.exp(-t * 180) + 0.3 * band(noise(d), 2000, 9000) * np.exp(-t * 300)
def boop(f=300, d=0.11):
    s, t = chirp(f * 1.5, f * 0.8, d); return s * np.exp(-t * 26) * np.minimum(1, t / 0.004)
def munch(f=260):
    return np.concatenate([boop(f, 0.09), np.zeros(int(0.03 * SR)), boop(f * 0.9, 0.09)])
def bonk(f=190):
    s, t = chirp(f * 1.8, f, 0.22, 0.3); return s * np.exp(-t * 16) + 0.25 * band(noise(0.22), 300, 2500) * np.exp(-t * 70)
def puff(d=0.35):
    t = tt(d); x = band(noise(d), 400, 5000); return x / (np.abs(x).max() + 1e-9) * np.exp(-t * 11) * np.minimum(1, t / 0.005)
def swipe(d=0.25):
    t = tt(d); out = np.zeros_like(t); x = noise(d); seg = 1200
    for k in range(0, len(t), seg):
        u = k / len(t); c = 800 * (5000 / 800) ** u; y = band(x[k:k + seg * 2], c * 0.6, c * 1.5)[:seg]; out[k:k + len(y)] += y
    out /= np.abs(out).max() + 1e-9; return out * np.sin(np.pi * t / d) ** 1.4
def slide_down(d=0.55):
    s, t = chirp(700, 170, d, 0.8); vib = 1 + 0.0 * t
    return s * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.5 * vib + 0.15 * band(noise(d), 1500, 6000) * np.exp(-t * 5)
def wobble(d=0.6):
    t = tt(d); f = 900 - 350 * t / d + 40 * np.sin(2 * np.pi * 9 * t); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.5) * np.minimum(1, t / 0.01)
def pluck(m, d=0.5, vel=0.6):
    f = nt(m); t = tt(d); s = np.zeros_like(t)
    for n in range(1, 7): s += (1 / n ** 1.4) * np.sin(2 * np.pi * n * f * t + rs.uniform(0, 6.28)) * np.exp(-t * (7 + 4 * n))
    return s * np.minimum(1, t / 0.002) * vel
def marimba(m, d=0.9, vel=0.6):
    f = nt(m); t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 3.6) + 0.3 * np.sin(2 * np.pi * f * 3.99 * t) * np.exp(-t * 12)
    return s * np.minimum(1, t / 0.0015) * np.minimum(1, (d - t) / 0.05) * vel
def chime(m, d=2.0, vel=0.5):
    f = nt(m); t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 1.6) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 4) + 0.15 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 8)
    return s * np.minimum(1, t / 0.002) * vel
def pad(ms, d, att=0.8, rel=1.2):
    t = tt(d); s = np.zeros_like(t)
    for m in ms:
        for det in (-0.07, 0.0, 0.06): s += np.sin(2 * np.pi * nt(m) * 2 ** (det / 12) * t + rs.uniform(0, 6.28))
    return s * np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1) / (3 * len(ms))
def whoosh(d=1.6):
    t = tt(d); x = noise(d); out = np.zeros_like(t); seg = 2400
    for k in range(0, len(t), seg):
        u = k / len(t); c = 250 * (2400 / 250) ** np.sin(np.pi * min(1.0, u)) ; y = band(x[k:k + seg * 2], c * 0.6, c * 1.6)[:seg]; out[k:k + len(y)] += y
    out /= np.abs(out).max() + 1e-9; return out * np.sin(np.pi * t / d) ** 1.6

# --- music bed: C major, 120 bpm, pizzicato bass + marimba figure; thins out under the sim, resolves at the end
B = 0.5
prog = [(0.35, [48, 55, 64]), (2.35, [45, 52, 60]), (4.35, [41, 48, 57]), (6.35, [43, 50, 59]), (8.35, [48, 55, 64])]
fig = [0, 2, 1, 2, 0, 2, 1, 2]
for b0, ch in prog:
    for k in range(8):
        tk = b0 + k * B * 0.5
        if tk > 9.3: break
        add(pluck(ch[0] if k % 4 == 0 else ch[0] + 12, 0.5, 0.7), tk, 0.13 if k % 4 == 0 else 0.07, -0.1, wet)
    for k, j in enumerate(fig):
        tk = b0 + 0.25 + k * B * 0.5
        if tk > 9.0: break
        add(marimba(ch[j] + 12, 0.7, 0.5), tk, 0.05, 0.25 if k % 2 else -0.2, wet)
add(pad([60, 64, 67, 72], 2.2, 0.6, 1.4), 8.0, 0.06, 0.0, wet)

day_n = 0
for e in json.load(open('events.json')):
    k, te, x = e['k'], e['t'], e.get('x', 0.0) * -0.7      # camera looks toward +z: world +x is screen left
    if k == 'title': add(swipe(0.3), te, 0.05, -0.5); add(chime(79, 1.2, 0.5), te + 0.1, 0.05, -0.4, wet)
    elif k == 'spawn': add(bloop(330 + 60 * rs.uniform(), 820, 0.12), te, 0.14, x)
    elif k == 'food': add(tick(3200, 0.03), te, 0.06, 0.1); add(pluck(84, 0.3, 0.5), te, 0.03, 0.1, wet)
    elif k == 'legend': add(tick(2000, 0.03), te, 0.06, -0.5)
    elif k == 'label': add(tick(2400, 0.035), te, 0.08, x); add(pluck(88, 0.25, 0.4), te, 0.03, x, wet)
    elif k == 'nom': add(munch(240 + 60 * rs.uniform()), te, 0.22, x)
    elif k == 'nib': add(boop(420, 0.07), te, 0.14, x)
    elif k == 'swipe': add(swipe(0.22), te - 0.08, 0.14, x)
    elif k == 'bonk': add(bonk(170 + 30 * rs.uniform()), te, 0.26, x)
    elif k == 'burst': add(puff(0.35), te, 0.16, x); add(bloop(900, 300, 0.1), te, 0.08, x)
    elif k == 'daze': add(wobble(0.6), te, 0.07, x, wet)
    elif k == 'split': add(bloop(420, 1000, 0.1), te, 0.16, x); add(bloop(620, 1400, 0.1), te + 0.08, 0.13, x); add(chime(91, 0.8, 0.4), te + 0.1, 0.03, x, wet)
    elif k == 'deflate': add(slide_down(0.5), te, 0.09, x)
    elif k == 'day':
        if e['g'] > 0: add(tick(1800 + 90 * day_n, 0.04), te, 0.09, 0.55); add(pluck(72 + [0, 2, 4, 5, 7, 9, 11, 12, 14][day_n % 9], 0.35, 0.5), te, 0.035, 0.5, wet); day_n += 1
    elif k == 'bustle':
        n = int(min(28, 6 + e['n'] * 0.3)); d = e['d']
        for j in range(n):
            add(boop(260 + 400 * rs.uniform(), 0.06), te + rs.uniform(0, d), 0.035, rs.uniform(-0.8, 0.8))
        for j in range(int(min(6, e['f']))): add(bonk(260 + 80 * rs.uniform()), te + rs.uniform(0.2, 0.9) * d, 0.05, rs.uniform(-0.7, 0.7))
    elif k == 'births':
        for j in range(int(min(12, e['n'] * 0.5))): add(bloop(500 + 300 * rs.uniform(), 1400, 0.07), te + rs.uniform(0, 0.08), 0.03, rs.uniform(-0.8, 0.8))
    elif k == 'zoom': add(whoosh(1.9), te, 0.12, 0.0)
    elif k == 'cap1': add(chime(76, 1.6, 0.5), te, 0.05, 0, wet); add(chime(72, 1.6, 0.5), te + 0.02, 0.04, 0, wet)
    elif k == 'cap2':
        for j, m in enumerate([72, 76, 79, 84]): add(chime(m, 2.2, 0.5), te + j * 0.06, 0.06, -0.3 + 0.2 * j, wet)
        add(bloop(500, 1200, 0.12), te, 0.08, 0.0)

# room reverb on the music bus
ir_t = tt(1.5); M = 1 << int(np.ceil(np.log2(N + len(ir_t))))
for dry_ch, wet_ch, seed in ((L, WL, 1), (R, WR, 2)):
    ir = np.random.default_rng(seed).standard_normal(len(ir_t)) * np.exp(-ir_t / 0.35); ir = band(ir, 80, 7000); ir /= np.sqrt(np.sum(ir ** 2))
    rev = np.fft.irfft(np.fft.rfft(wet_ch, M) * np.fft.rfft(ir, M), M)[:N]
    dry_ch += wet_ch * 0.85 + rev * 0.28
fi = int(0.03 * SR); fo = int(0.8 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); pk = np.abs(st).max(); st = np.tanh(st / pk * 1.3) * 0.75
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok, peak before norm', round(float(pk), 3))
