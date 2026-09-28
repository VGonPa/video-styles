# events.json -> audio.wav (48 kHz stereo, 10 s). Everything is synthesized (no samples):
# a soft felt-piano line in D major over a warm pad, graphite scratches while the sketch and the
# caption are drawn, wet-brush washes as each region blooms, a shimmer as the lantern lights,
# and a long ring-out as the memory fades. Simple FFT-convolution room reverb.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(115)
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
def felt(m, d=3.2, vel=0.6):
    """felt piano: slightly inharmonic partials, dull hammer, per-partial decay, soft thump"""
    f = nt(m); t = tt(d); s = np.zeros_like(t); B = 0.00035
    for n in range(1, 9):
        fn = n * f * np.sqrt(1 + B * n * n)
        if fn > 9000: break
        a = (1 / n ** 1.4) * np.exp(-n * (0.35 - 0.2 * vel))
        tau = 2.6 / (1 + 0.55 * n) * (1.0 if m < 70 else 0.75)
        s += a * np.sin(2 * np.pi * fn * t + rs.uniform(0, 6.28)) * np.exp(-t / tau)
    att = np.minimum(1, t / 0.006); rel = np.minimum(1, (d - t) / 0.4)
    thump = band(rs.standard_normal(len(t)), 60, 700) * np.exp(-t / 0.012); thump /= np.abs(thump).max() + 1e-9
    return (s * att * rel + 0.08 * thump) * vel
def pad(ms, d, att=1.6, rel=2.0):
    t = tt(d); s = np.zeros_like(t)
    for m in ms:
        for det in (-0.07, 0.0, 0.06):
            f = nt(m) * 2 ** (det / 12)
            s += np.sin(2 * np.pi * f * t + rs.uniform(0, 6.28)) + 0.18 * np.sin(4 * np.pi * f * t) + 0.06 * np.sin(6 * np.pi * f * t)
    env = np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1)
    return s * env / (3 * len(ms))
def wash(d=1.1):
    """wet brush laid on paper: soft pink-ish noise swoosh with a falling lowpass"""
    t = tt(d); x = np.cumsum(rs.standard_normal(len(t))); x -= np.convolve(x, np.ones(400) / 400, 'same')
    x = band(x, 120, 5000); x /= np.abs(x).max() + 1e-9
    env = np.minimum(1, t / 0.12) * np.exp(-t / (d * 0.45))
    am = 0.75 + 0.25 * np.abs(band(rs.standard_normal(len(t)), 3, 18)) / 0.3
    return x * env * np.clip(am, 0, 1.3)
def pencil(d):
    """graphite on cold-press paper: bursts of bright scratchy noise, one per stroke"""
    t = tt(d); x = band(rs.standard_normal(len(t)), 1800, 9000); x /= np.abs(x).max() + 1e-9
    strokes = np.zeros_like(t); k = 0.0
    while k < d:
        ln = rs.uniform(0.06, 0.2); i0, i1 = int(k * SR), int(min(d, k + ln) * SR)
        if i1 > i0: strokes[i0:i1] = np.sin(np.linspace(0, np.pi, i1 - i0)) ** 0.6 * rs.uniform(0.5, 1.0)
        k += ln + rs.uniform(0.02, 0.09)
    grit = 0.7 + 0.3 * np.sign(np.sin(2 * np.pi * 37 * t + 5 * np.sin(2 * np.pi * 3 * t)))
    return x * strokes * grit * np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.1)
def shimmer(d=2.6):
    t = tt(d); s = sum(np.sin(2 * np.pi * nt(m) * t) * a for m, a in [(86, .5), (90, .35), (93, .3), (98, .15)])
    return s * np.minimum(1, t / 0.9) * np.clip((d - t) / 1.4, 0, 1) * (0.8 + 0.2 * np.sin(2 * np.pi * 5.5 * t))

# dry and wet buses (the piano and pad go through the room)
WL = np.zeros(N); WR = np.zeros(N); wet = (WL, WR)
# pad bed: D (add9) swelling to the glow, softening into G/D as the colour leaves
add(pad([50, 57, 62, 64], 6.6, att=2.2, rel=1.6), 1.2, 0.05, -0.1, wet)
add(pad([43, 55, 62, 66], 4.4, att=1.4, rel=2.6), 6.0, 0.045, 0.1, wet)
# felt piano: one note per bloom, a little rise to the glow, then a falling line as the memory fades
line = [(0.35, 62, .40), (0.35, 50, .30), (1.45, 66, .50), (2.25, 69, .48), (2.95, 74, .46), (3.55, 73, .44),
        (4.30, 62, .38), (4.30, 57, .34), (4.30, 66, .40), (5.00, 76, .46), (5.80, 78, .50), (5.80, 50, .30),
        (6.40, 74, .42), (7.00, 71, .38), (7.60, 69, .36), (8.20, 66, .34), (8.95, 62, .36), (8.95, 50, .26), (8.95, 57, .24)]
for t0, m, v in line:
    add(felt(m, 10.0 - t0 if t0 > 8 else 3.4, v), t0, 0.22, np.clip((m - 64) / 30, -0.4, 0.4), wet)
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'pencil': add(pencil(e['d']), te, 0.035, 0.1)
    elif k == 'wash': add(wash(1.3), te - 0.05, 0.10 * e.get('v', 1), e.get('pan', 0))
    elif k == 'glow': add(shimmer(2.8), te, 0.028, 0.2, wet)
    elif k == 'fade': add(wash(2.4)[::-1] * 0.6, te - 0.3, 0.05, -0.2)
# room: exponentially decaying stereo noise IR (~2.2 s), FFT convolution
ir_t = tt(2.2); M = 1 << int(np.ceil(np.log2(N + len(ir_t))))
for dry_ch, wet_ch, seed in ((L, WL, 1), (R, WR, 2)):
    ir = np.random.default_rng(seed).standard_normal(len(ir_t)) * np.exp(-ir_t / 0.55); ir = lp1(ir, 5000); ir /= np.sqrt(np.sum(ir ** 2))
    rev = np.fft.irfft(np.fft.rfft(wet_ch, M) * np.fft.rfft(ir, M), M)[:N]
    dry_ch += wet_ch * 0.8 + rev * 0.32
# master: gentle warmth, fade in/out, soft limiter
for ch in (L, R): ch[:] = 0.7 * ch + 0.3 * lp1(ch, 3500)
fi = int(0.05 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.6
st = np.stack([L, R], 1); pk = np.abs(st).max(); st = np.tanh(st / pk * 1.2) * 0.72
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok, peak before norm', round(float(pk), 3))
