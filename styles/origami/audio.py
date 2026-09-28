# events.json -> audio.wav (48 kHz stereo, 10 s). Everything is synthesized (no samples):
# paper rustle swishes for every fold, a crisp press "tk" plus a kalimba note as each crease is set
# (the notes climb a pentatonic scale fold by fold), soft air whooshes for the wing beats, a rising
# breath for the take-off, a quiet water bed with droplets for the pleated sea, a flutter as the boat
# unfolds and a warm kalimba chord + pad under the title. FFT-convolution room reverb on the music bus.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
WL = np.zeros(N); WR = np.zeros(N); wet = (WL, WR)
rs = np.random.default_rng(56)
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
def norm(x): return x / (np.abs(x).max() + 1e-9)

def kalimba(m, d=1.6, vel=0.6):
    f = nt(m); t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 2.6) + 0.28 * np.sin(2 * np.pi * f * 5.95 * t) * np.exp(-t * 14) \
        + 0.12 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t * 5)
    return s * np.minimum(1, t / 0.0015) * vel
def rustle(d=0.35, lo=1800, hi=9000, grit=0.5):
    """paper swish: band noise with a swelling envelope + sparse crackle grains"""
    t = tt(d); x = norm(band(noise(d), lo, hi))
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.4
    am = 0.6 + 0.4 * np.abs(band(noise(d), 4, 40)) * 3
    cr = np.zeros_like(t)
    for _ in range(int(d * 60 * grit)):
        i = rs.integers(0, len(t) - 400); k = tt(0.006); cr[i:i + len(k)] += rs.uniform(-1, 1) * np.exp(-k * 900)
    return (x * np.minimum(am, 1.4) * 0.8 + band(cr, 1500, 12000) * 2.5) * env
def press():
    """crease being set: a crisp tick with a short scrape"""
    t = tt(0.09); x = norm(band(noise(0.09), 2500, 11000)) * np.exp(-t * 70)
    return x + 0.5 * np.sin(2 * np.pi * 180 * t) * np.exp(-t * 60)
def whoosh(d, lo=150, hi=1400):
    t = tt(d); x = norm(band(noise(d), lo, hi)); return x * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
def thump():
    t = tt(0.25); return np.sin(2 * np.pi * 70 * t * (1 + 0.5 * np.exp(-t * 30))) * np.exp(-t * 22) + 0.3 * norm(band(noise(0.25), 400, 3000)) * np.exp(-t * 35)
def drop(f=1400):
    t = tt(0.12); return np.sin(2 * np.pi * np.cumsum(f * (1 + 1.2 * np.exp(-t * 40))) / SR) * np.exp(-t * 38)
def pad(ms, d, att=0.8, rel=1.2):
    t = tt(d); s = np.zeros_like(t)
    for m in ms:
        for det in (-0.07, 0.0, 0.06): s += np.sin(2 * np.pi * nt(m) * 2 ** (det / 12) * t + rs.uniform(0, 6.28))
    return s * np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1) / (3 * len(ms))

# D major pentatonic, one note per crease, climbing
PENTA = [62, 64, 66, 69, 71, 74, 76, 78, 81, 83, 86, 88, 90, 93, 95]
ev = json.load(open('events.json'))
nc = 0
for e in ev:
    k, te = e['k'], e['t']
    if k == 'land': add(thump(), te, 0.35, 0); add(rustle(0.3, 800, 6000, 0.2), te - 0.1, 0.10, -0.1)
    elif k == 'fold': add(rustle(max(0.25, e['d'] * 0.8)), te + 0.02, 0.13, -0.3 + 0.6 * ((e['i'] * 7) % 5) / 4)
    elif k == 'crease':
        add(press(), te, 0.22, 0.1)
        m = PENTA[min(nc, len(PENTA) - 1)] if nc < 9 else PENTA[(nc - 9) % 6 + 2]
        add(kalimba(m, 1.6, 0.6), te, 0.16, -0.25 + 0.5 * (nc % 3) / 2, wet); nc += 1
    elif k == 'stand': add(thump(), te + 0.3, 0.12, 0.2); add(rustle(0.3, 1200, 7000, 0.3), te, 0.10, 0.2)
    elif k == 'open':
        add(whoosh(0.5, 300, 2500), te, 0.12, 0.1)
        for j, m in enumerate([74, 78, 81]): add(kalimba(m, 1.8, 0.5), te + 0.12 + j * 0.07, 0.10, -0.2 + 0.2 * j, wet)
    elif k == 'flap': add(whoosh(0.2, 120, 900 + 100 * e['i']), te, 0.22 * (1 - 0.12 * e['i']), 0.2 + 0.1 * e['i'])
    elif k == 'takeoff': add(whoosh(1.1, 200, 3200) * np.linspace(0.3, 1, int(1.1 * SR)), te, 0.14, 0.4)
    elif k == 'water':
        d = 9.6 - te; t = tt(d); bed = norm(band(noise(d), 200, 2200)); bed *= (0.55 + 0.45 * np.sin(2 * np.pi * 0.9 * t) ** 2)
        bed *= np.minimum(1, t / 0.6) * np.clip((d - t) / 1.4, 0, 1)
        add(bed, te, 0.06, -0.2); add(np.roll(bed, 9000), te, 0.05, 0.25)
        for j in range(9): add(drop(1100 + 500 * rs.random()), te + 0.4 + j * 0.23 + 0.08 * rs.random(), 0.05, rs.uniform(-0.6, 0.6), wet)
    elif k == 'standboat': add(rustle(0.3, 1200, 7000, 0.3), te - 0.2, 0.10, 0.0)
    elif k == 'splash': add(norm(band(noise(0.4), 300, 3500)) * np.exp(-tt(0.4) * 9), te, 0.10, 0)
    elif k == 'unfold': add(rustle(0.3, 1500, 10000, 0.8), te, 0.12, -0.3 + 0.12 * e['i'])
    elif k == 'flatten': add(thump(), te, 0.10, 0); add(press(), te + 0.02, 0.12, 0)
    elif k == 'word':
        chord = [[62, 69], [66, 74], [69, 78], [74, 81]][e['i']]
        for j, m in enumerate(chord): add(kalimba(m, 2.2, 0.55), te + j * 0.03, 0.13, -0.3 + 0.2 * e['i'], wet)
        if e['i'] == 3: add(pad([50, 57, 62, 66, 69], 1.9, 0.5, 1.2), te, 0.08, 0, wet)
# soft underscore: a low kalimba ostinato through the folding
for j, bt in enumerate(np.arange(0.5, 8.6, 0.625)):
    m = [50, 57, 54, 57][j % 4] + (5 if 4.6 < bt < 7.5 and j % 4 == 0 else 0)
    add(kalimba(m, 1.2, 0.5), bt, 0.07, -0.1, wet)

ir_t = tt(1.6); M = 1 << int(np.ceil(np.log2(N + len(ir_t))))
for dry_ch, wet_ch, seed in ((L, WL, 1), (R, WR, 2)):
    ir = np.random.default_rng(seed).standard_normal(len(ir_t)) * np.exp(-ir_t / 0.35); ir = band(ir, 20, 7000); ir /= np.sqrt(np.sum(ir ** 2))
    rev = np.fft.irfft(np.fft.rfft(wet_ch, M) * np.fft.rfft(ir, M), M)[:N]
    dry_ch += wet_ch * 0.85 + rev * 0.3
fi = int(0.03 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); pk = np.abs(st).max(); st = np.tanh(st / pk * 1.2) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok, peak before norm', round(float(pk), 3))
