# events.json -> audio.wav (48 kHz stereo, 10 s). Everything is synthesized (no samples):
# a bouncy pluck + soft marimba bed in F major (116 bpm), water-drop "bloops" for the pops,
# rubbery squeaks for the bumps, a balloon-inflate hiss with a rising pitch, a soft button
# thunk + springy boing on the press, tiny rubber taps for confetti bounces, ascending
# bloops for the title letters, and a warm closing chord. Light FFT-convolution reverb.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
WL = np.zeros(N); WR = np.zeros(N); wet = (WL, WR)
rs = np.random.default_rng(52)
def add(sig, t, g=1.0, pan=0.0, dst=None):
    i = int(t * SR); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    l, r = (L, R) if dst is None else dst
    l[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; r[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def noise(d): return rs.standard_normal(int(d * SR))
def sweep(f0, f1, d, curve=1.0):
    t = tt(d); f = f0 * (f1 / f0) ** ((t / d) ** curve); return np.sin(2 * np.pi * np.cumsum(f) / SR)
def bloop(f=520, d=0.16, up=2.2):
    """water-drop pop: fast upward pitch glide with a soft decay"""
    t = tt(d); f_ = f * (1 + (up - 1) * (1 - np.exp(-t * 38)))
    return np.sin(2 * np.pi * np.cumsum(f_) / SR) * np.exp(-t * 22) * np.minimum(1, t / 0.002)
def squeak(f=700, d=0.22):
    """rubbery squeak: vibrato FM tone with a pitch bend"""
    t = tt(d); f_ = f * (1 + 0.35 * np.sin(np.pi * t / d)) * (1 + 0.04 * np.sin(2 * np.pi * 38 * t))
    ph = 2 * np.pi * np.cumsum(f_) / SR
    return np.sin(ph + 0.9 * np.sin(2 * ph)) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.7
def boing(f=180, d=0.55):
    t = tt(d); f_ = f * (1 + 0.5 * np.exp(-t * 7) * np.cos(2 * np.pi * 9 * t))
    return np.sin(2 * np.pi * np.cumsum(f_) / SR) * np.exp(-t * 6) * np.minimum(1, t / 0.003)
def thunk():
    t = tt(0.3); return np.sin(2 * np.pi * 110 * t * (1 + 0.8 * np.exp(-t * 40))) * np.exp(-t * 20) + 0.3 * band(noise(0.3), 300, 2500) * np.exp(-t * 70)
def tap(f=900):
    t = tt(0.06); return np.sin(2 * np.pi * f * t * (1 + 0.5 * np.exp(-t * 90))) * np.exp(-t * 70)
def pluck(m, d=0.6, vel=0.6):
    f = nt(m); t = tt(d); s = np.zeros_like(t)
    for n in range(1, 7): s += (1 / n ** 1.4) * np.sin(2 * np.pi * n * f * t) * np.exp(-t * (5 + 3 * n))
    return s * np.minimum(1, t / 0.002) * np.minimum(1, (d - t) / 0.04) * vel
def marimba(m, d=0.9, vel=0.6):
    f = nt(m); t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 4) + 0.3 * np.sin(2 * np.pi * f * 3.99 * t) * np.exp(-t * 14)
    return s * np.minimum(1, t / 0.0015) * np.minimum(1, (d - t) / 0.04) * vel
def pad(ms, d, att=0.8, rel=1.5):
    t = tt(d); s = np.zeros_like(t)
    for m in ms:
        for det in (-0.07, 0.0, 0.06): s += np.sin(2 * np.pi * nt(m) * 2 ** (det / 12) * t + rs.uniform(0, 6.28))
    return s * np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1) / (3 * len(ms))

# --- music bed: F major, 116 bpm, bouncy off-beat plucks + marimba bass
B = 60 / 116
CH = {'F': [65, 69, 72], 'Dm': [62, 65, 69], 'Bb': [62, 65, 70], 'C': [64, 67, 72]}
prog = ['F', 'Dm', 'Bb', 'C', 'F', 'Dm', 'Bb', 'C', 'F']
for bi, c in enumerate(prog):
    b0 = 0.3 + bi * 2 * B
    if b0 > 9.0: break
    bass = CH[c][0] - 24 if c != 'C' else 48
    add(marimba(bass, 0.9, 0.9), b0, 0.2, 0.0, wet); add(marimba(bass + 7, 0.6, 0.7), b0 + B, 0.13, 0.0, wet)
    for k in range(4):
        tk = b0 + (k + 0.5) * B / 2
        if tk > 9.2: continue
        for j, m in enumerate(CH[c]): add(pluck(m + 12, 0.35, 0.5), tk + j * 0.008, 0.05, -0.2 + 0.2 * j, wet)
mel = [(0.3, 77), (0.8, 81), (1.3, 84), (2.3, 81), (3.4, 82), (3.9, 81), (4.4, 77), (5.5, 79), (6.6, 81), (7.1, 84), (7.6, 86), (8.1, 84), (8.6, 89)]
for t0, m in mel: add(marimba(m, 0.8, 0.5), t0, 0.08, 0.25, wet)

letters = 0
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'pop': add(bloop(430 + 70 * e['i'], 0.18), te + 0.02, 0.26, [-0.5, -0.2, 0.2, 0.5, -0.05, 0.05][e['i'] % 6], wet)
    elif k == 'bump': add(squeak(620 if e['pan'] < 0 else 760, 0.2), te, 0.14, e['pan']); add(boing(150, 0.4), te, 0.16, e['pan'])
    elif k == 'swoosh':
        x = band(noise(0.8), 500, 5000) * np.sin(np.pi * np.clip(tt(0.8) / 0.8, 0, 1)) ** 2; add(x / np.abs(x).max(), te, 0.07, 0)
    elif k == 'inflate':
        d = 0.9; t = tt(d); h = band(noise(d), 1500, 9000) * np.sin(np.pi * t / d) ** 1.5
        add(h / np.abs(h).max(), te, 0.06, 0); add(sweep(160, 420, d, 0.8) * np.sin(np.pi * t / d) ** 0.6 * 0.6, te, 0.12, 0, wet)
    elif k == 'slide':
        x = band(noise(0.7), 800, 4000) * np.sin(np.pi * np.clip(tt(0.7) / 0.7, 0, 1)) ** 2; add(x / np.abs(x).max(), te, 0.05, 0.4)
    elif k == 'press': add(thunk(), te - 0.02, 0.3, 0.05)
    elif k == 'release':
        add(boing(210, 0.6), te, 0.22, 0); add(bloop(700, 0.2, 2.6), te + 0.03, 0.2, 0, wet)
        for j in range(10): add(tap(1800 + 260 * j), te + 0.05 + 0.035 * j, 0.05, rs.uniform(-0.7, 0.7), wet)
    elif k == 'boing': add(tap(rs.uniform(500, 1100)), te, min(0.07, 0.015 * e['imp']), e['pan'])
    elif k == 'letter':
        m = [72, 74, 76, 77, 79, 81, 83, 84][letters % 8] + 12 * (letters // 8)
        add(bloop(nt(m) * 0.55, 0.12, 1.8), te + 0.02, 0.1, -0.5 + letters * 0.06, wet); letters += 1
    elif k == 'wave':
        for j in range(8): add(squeak(900 + 90 * j, 0.09), te + j * 0.05, 0.035, -0.5 + j * 0.14)
    elif k == 'out': add(pad([65, 69, 72, 77], 1.6, 0.3, 1.2), te - 0.2, 0.09, 0, wet); add(bloop(400, 0.3, 1.6), te + 0.3, 0.1, 0, wet)

# light room reverb on the wet bus
ir_t = tt(1.2); M = 1 << int(np.ceil(np.log2(N + len(ir_t))))
for dry_ch, wet_ch, seed in ((L, WL, 1), (R, WR, 2)):
    ir = np.random.default_rng(seed).standard_normal(len(ir_t)) * np.exp(-ir_t / 0.25); ir = band(ir, 100, 7000); ir /= np.sqrt(np.sum(ir ** 2))
    rev = np.fft.irfft(np.fft.rfft(wet_ch, M) * np.fft.rfft(ir, M), M)[:N]
    dry_ch += wet_ch * 0.85 + rev * 0.22
fi = int(0.03 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); pk = np.abs(st).max(); st = np.tanh(st / pk * 1.3) * 0.75
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok, peak before norm', round(float(pk), 3))
