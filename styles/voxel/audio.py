# events.json -> audio.wav (48 kHz stereo, 10 s). Everything is synthesized (no samples):
# a soft wind bed and the hiss of the waterfall, day birdsong that gives way to crickets at dusk,
# a calm, sparse felt-piano theme (Fmaj7 - Am7 - Cmaj7 - G) in a small room reverb,
# pickaxe ticks and a gravel crunch for the boulder, a material-specific "thock" for every placed
# block (stone, wood, glass, clay, lantern), pixel UI blips for the step cards and title letters,
# a warm swell as the lanterns light, a whoosh for the pull-back and a closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
WL = np.zeros(N); WR = np.zeros(N); wet = (WL, WR)
rs = np.random.default_rng(72)
def add(sig, t, g=1.0, pan=0.0, dst=None):
    i = int(t * SR); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    l, r = (L, R) if dst is None else dst
    l[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; r[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def noise(d): return rs.standard_normal(int(d * SR))
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def env(t, a, d): return np.minimum(1, t / a) * np.exp(-t / d)
def piano(m, d=2.6, vel=0.5):
    """felt piano: few inharmonic partials, soft hammer, gentle decay"""
    f = nt(m); t = tt(d); s = np.zeros_like(t)
    for n, (a, dec) in enumerate([(1, 1.4), (0.45, 0.8), (0.22, 0.45), (0.1, 0.3), (0.05, 0.2)], 1):
        s += a * np.sin(2 * np.pi * f * n * np.sqrt(1 + 0.0004 * n * n) * t + rs.uniform(0, 6.28)) * np.exp(-t / dec)
    s += 0.05 * band(noise(d), 200, 2000) * np.exp(-t / 0.01)
    return s * np.minimum(1, t / 0.006) * np.minimum(1, (d - t) / 0.2) * vel
def pad(ms, d, att=1.0, rel=1.4):
    t = tt(d); s = np.zeros_like(t)
    for m in ms:
        for det in (-0.07, 0.0, 0.06):
            s += np.sin(2 * np.pi * nt(m) * 2 ** (det / 12) * t + rs.uniform(0, 6.28))
    return s * np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1) / (3 * len(ms))
def square(f, d, duty=0.5):
    t = tt(d); return np.where((t * f) % 1 < duty, 1.0, -1.0)
def blip(m, d=0.07):
    t = tt(d); return square(nt(m), d, 0.25) * np.exp(-t / 0.03) * np.minimum(1, t / 0.002)
def thock(kind):
    """block placement: short body resonance + filtered click, per material"""
    if kind in ('cobble', 'mossy'):
        d = 0.14; t = tt(d); f0 = rs.uniform(105, 135)
        return (0.8 * np.sin(2 * np.pi * f0 * t) * np.exp(-t / 0.03) + 0.9 * band(noise(d), 350, 2400) * np.exp(-t / 0.018))
    if kind in ('planks', 'log'):
        d = 0.16; t = tt(d); f0 = rs.uniform(210, 260) * (0.85 if kind == 'log' else 1)
        return (np.sin(2 * np.pi * f0 * t) * np.exp(-t / 0.045) + 0.35 * np.sin(2 * np.pi * f0 * 2.3 * t) * np.exp(-t / 0.02)
                + 0.5 * band(noise(d), 800, 3500) * np.exp(-t / 0.008))
    if kind == 'glass':
        d = 0.35; t = tt(d); f0 = rs.uniform(2400, 2800)
        return 0.5 * (np.sin(2 * np.pi * f0 * t) + 0.6 * np.sin(2 * np.pi * f0 * 1.51 * t)) * np.exp(-t / 0.07) + 0.4 * band(noise(d), 1500, 6000) * np.exp(-t / 0.006)
    if kind == 'roof':
        d = 0.12; t = tt(d); f0 = rs.uniform(380, 460)
        return np.sin(2 * np.pi * f0 * t) * np.exp(-t / 0.025) + 0.6 * band(noise(d), 700, 3000) * np.exp(-t / 0.012)
    d = 0.4; t = tt(d)   # lantern: metal clink
    return 0.6 * (np.sin(2 * np.pi * 1850 * t) + 0.5 * np.sin(2 * np.pi * 2930 * t)) * np.exp(-t / 0.09) + 0.6 * np.sin(2 * np.pi * 160 * t) * np.exp(-t / 0.03)
def pick_hit():
    d = 0.18; t = tt(d)
    return (0.8 * band(noise(d), 1500, 6000) * np.exp(-t / 0.012) + 0.7 * np.sin(2 * np.pi * 170 * t) * np.exp(-t / 0.035)
            + 0.3 * band(noise(d), 300, 1200) * np.exp(-t / 0.04))
def crunch():
    d = 0.7; out = np.zeros(int(d * SR))
    for k in range(26):   # gravel grains
        g = pick_hit() * rs.uniform(0.2, 0.7); i = int(rs.uniform(0, 0.35) ** 1.6 * SR); n = min(len(g), len(out) - i); out[i:i + n] += g[:n]
    t = tt(d); out += 0.9 * np.sin(2 * np.pi * 85 * t) * np.exp(-t / 0.08)
    return out
def whoosh(d, lo=250, hi=2600):
    t = tt(d); x = noise(d); out = np.zeros_like(t); seg = 2400
    for k in range(0, len(t), seg):
        u = k / len(t); c = lo * (hi / lo) ** np.sin(np.pi * min(1.0, u))
        y = band(x[k:k + seg * 2], c * 0.6, c * 1.6)[:seg]; out[k:k + len(y)] += y
    out /= np.abs(out).max() + 1e-9
    return out * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5
def chirp(pan):
    out = np.zeros(int(0.5 * SR)); st = 0.0
    for k in range(rs.integers(2, 5)):
        d = rs.uniform(0.04, 0.08); t = tt(d); f = rs.uniform(3200, 4600) + rs.uniform(-1500, 1500) * (t / d)
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d); i = int(st * SR); out[i:i + len(s)] += s; st += d + rs.uniform(0.02, 0.07)
    return out
def cricket():
    d = 0.35; t = tt(d); am = (np.sin(2 * np.pi * 32 * t) > 0.3).astype(float)
    return np.sin(2 * np.pi * 4300 * t) * am * np.sin(np.pi * t / d)

tv = tt(DUR)
dusk = np.clip((tv - 5.0) / 3.0, 0, 1)
# wind bed and waterfall hiss (the fall gets louder as the camera pulls back to reveal it)
wind = np.cumsum(noise(DUR)); wind -= np.convolve(wind, np.ones(3000) / 3000, 'same'); wind = band(wind, 80, 1200); wind /= np.abs(wind).max()
add(wind * (0.6 + 0.4 * np.sin(2 * np.pi * tv / 4.1) ** 2), 0, 0.10, -0.2)
fall = band(noise(DUR), 500, 7000); fall /= np.abs(fall).max()
add(fall * (0.35 + 0.65 * np.clip((tv - 7.3) / 1.8, 0, 1)) * (0.8 + 0.2 * np.sin(2 * np.pi * tv * 0.7)), 0, 0.05, 0.35)
# birds by day, crickets at dusk
for tb, pn in [(0.4, -0.5), (1.2, 0.4), (2.6, -0.3), (3.3, 0.6), (4.4, -0.6), (5.1, 0.3)]: add(chirp(pn), tb, 0.035, pn)
for k in range(24):
    tc = 6.3 + k * 0.15 + rs.uniform(0, 0.06)
    if tc < 9.6: add(cricket(), tc, 0.012 * min(1, (tc - 6.3) / 1.2), 0.5 if k % 2 else -0.45)

# music: F major felt piano, 72 bpm, sparse arpeggios over a slow pad
B = 60 / 72
bars = [(0.3, [53, 60, 64, 69, 72]), (0.3 + 4 * B * 0.62, [57, 64, 67, 72, 76]), (0.3 + 8 * B * 0.62, [48, 55, 64, 67, 71]), (0.3 + 12 * B * 0.62, [55, 62, 67, 71, 74])]
for b0, ch in bars:
    add(piano(ch[0] - 12, 3.2, 0.5), b0, 0.16, -0.1, wet)
    for j, m in enumerate([ch[1], ch[2], ch[3], ch[4], ch[3]]):
        tn = b0 + j * B * 0.5
        if tn < 9.3: add(piano(m, 2.4, 0.42 - 0.04 * j), tn, 0.10, -0.3 + 0.15 * j, wet)
mel = [(1.35, 81), (2.4, 79), (3.0, 76), (4.3, 77), (5.2, 76), (5.75, 72), (6.9, 74), (7.6, 71)]
for tm, m in mel: add(piano(m, 2.4, 0.36), tm, 0.10, 0.25, wet)
add(pad([53, 60, 64, 69], 4.5, 1.8, 2.0), 0.2, 0.045, 0.0, wet)
add(pad([48, 55, 64, 67], 4.5, 1.5, 2.2), 4.2, 0.045, 0.0, wet)

letters = 0
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'card': add(blip(84, 0.06), te, 0.05, -0.5); add(blip(91, 0.07), te + 0.055, 0.045, -0.5)
    elif k == 'hit': add(pick_hit(), te, 0.28, 0.0)
    elif k == 'break': add(crunch(), te, 0.30, 0.0); add(blip(64, 0.1) * 0.5, te + 0.04, 0.03, 0)
    elif k == 'place': add(thock(e['m']), te, {'glass': 0.10, 'lantern': 0.16}.get(e['m'], 0.13), float(rs.uniform(-0.35, 0.35)))
    elif k == 'glow':
        add(pad([65, 69, 72, 76], 3.2, 0.8, 1.8), te, 0.07, 0.1, wet)
        for j, m in enumerate([84, 88, 91, 96]): add(piano(m, 1.8, 0.3), te + 0.12 * j, 0.06, 0.3, wet)
    elif k == 'pull': add(whoosh(1.8), te, 0.16, 0.2)
    elif k == 'letter': add(blip(72 + [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19][letters % 12], 0.08), te, 0.035, -0.4 + letters * 0.07); letters += 1
    elif k == 'sub': add(piano(77, 2.5, 0.4), te, 0.08, 0, wet); add(piano(84, 2.5, 0.3), te + 0.06, 0.06, 0, wet)
    elif k == 'end':
        for j, m in enumerate([41, 53, 60, 65, 69, 72]): add(piano(m, 1.6, 0.35), te - 0.35 + j * 0.03, 0.08, -0.2 + 0.08 * j, wet)

# room reverb on the music bus
ir_t = tt(2.2); M = 1 << int(np.ceil(np.log2(N + len(ir_t))))
for dry_ch, wet_ch, seed in ((L, WL, 1), (R, WR, 2)):
    ir = np.random.default_rng(seed).standard_normal(len(ir_t)) * np.exp(-ir_t / 0.55); ir = band(ir, 60, 6000); ir /= np.sqrt(np.sum(ir ** 2))
    rev = np.fft.irfft(np.fft.rfft(wet_ch, M) * np.fft.rfft(ir, M), M)[:N]
    dry_ch += wet_ch * 0.8 + rev * 0.35
fi = int(0.05 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); pk = np.abs(st).max(); st = np.tanh(st / pk * 1.3) * 0.75
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok, peak before norm', round(float(pk), 3))
