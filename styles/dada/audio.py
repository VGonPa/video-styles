# events.json → audio.wav (48 kHz stereo, 10 s)
# a cabaret upright plays a tidy oom-pah under the orderly front page; giant shears snip across it,
# the page tears and flutters away, and the piano lid slams. Cut-outs slap onto the board, the gear
# lands with a clank and ratchets as it turns, a slide whistle tips the hat and drops the D, and the
# tune comes back "in error": the same notes, shuffled and out of tune. A rubber stamp thumps, a horn
# honks once, and the room fades out.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(130)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def noise(d, lo, hi): return norm(band(rs.standard_normal(int(d * SR)), lo, hi))
def lowpass_sweep(x, fc):
    y = np.zeros_like(x); p = 0.0; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y
def glide(f0, f1, d, vib=0.0):
    # sine whose pitch slides from f0 to f1 (slide whistle), optional vibrato
    t = tt(d); f = f0 * (f1 / f0) ** (t / d) * (1 + vib * np.sin(2 * np.pi * 7 * t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.05)

# ── upright piano: two slightly detuned strings, stretched partials, hammer knock ──
def piano(f, d=1.2, det=0.0015):
    t = tt(d); s = np.zeros(len(t))
    for h, a in [(1, 1), (2, .55), (3, .32), (4, .2), (5, .12), (6, .07)]:
        fh = f * h * np.sqrt(1 + 0.0004 * h * h)
        for k in (1 + det, 1 - det): s += a * np.sin(2 * np.pi * fh * k * t) * np.exp(-t * (1.6 + 0.9 * h))
    knock = noise(0.03, 800, 5000) * np.exp(-tt(0.03) / 0.005)
    s[:len(knock)] += knock * 0.3
    return s * np.minimum(1, t / 0.003)
def chord(fs, d=0.5, det=0.0015): return sum(piano(f, d, det) for f in fs) / len(fs)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
BEAT = 60 / 138
# in order: two bars of oom-pah-pah in C, then G
for bar, (bass, ch) in enumerate([(48, [64, 67, 72]), (43, [62, 67, 71])]):
    t0 = 0.15 + bar * 3 * BEAT
    add(piano(hz(bass), 1.0), t0, 0.075, -0.2)
    for k in (1, 2): add(chord([hz(m) for m in ch], 0.45), t0 + k * BEAT, 0.045, 0.25)
add(piano(hz(48), 0.6), 0.15 + 6 * BEAT, 0.065, -0.2)
# in error: the same notes, wrong order, wrong tuning, wrong time
notes = [64, 67, 72, 43, 62, 71, 48, 67, 64, 72, 62, 43]; rs.shuffle(notes)
te = 3.25
for m in notes:
    if te > 8.0: break
    add(piano(hz(m) * 2 ** (rs.uniform(-40, 40) / 1200), 0.7, 0.004), te, 0.05 if m > 55 else 0.065, rs.uniform(-.5, .5))
    te += BEAT * rs.choice([0.5, 1, 1, 1.5, 2])

# ── foley ──
def snip():
    # two blades meeting: bright ringing contact plus a short shear of paper
    t = tt(0.12); ring = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / 0.02) for f in (3150, 4870, 6230)) / 3
    shear = noise(0.12, 1800, 9000) * np.exp(-t / 0.025)
    return ring * 0.6 + shear * 0.8
def swish(d):
    t = tt(d); y = lowpass_sweep(rs.standard_normal(len(t)), 200 + 2400 * np.sin(np.pi * t / d) ** 2)
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
def rip():
    t = tt(0.45); cr = (rs.random(len(t)) < 0.15) * rs.standard_normal(len(t))
    x = norm(band(cr + 0.4 * rs.standard_normal(len(t)), 900, 9000)) * np.minimum(1, t / 0.008) * np.exp(-t / 0.14)
    thump = np.sin(2 * np.pi * 70 * t) * np.exp(-t / 0.06)
    return x + thump * 0.7
def flutter(d):
    t = tt(d); am = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * (22 - 8 * t / d) * t))
    return noise(d, 300, 3500) * am * np.exp(-t / (d * 0.45))
def slap(v=1.0):
    t = tt(0.22); n = noise(0.22, 400, 7000) * np.exp(-t / 0.018)
    thump = np.sin(2 * np.pi * (95 + 40 * np.exp(-t / 0.01)) * t) * np.exp(-t / 0.05)
    return (n * 0.8 + thump * 0.7) * v
def clank():
    # cast gear dropped on the board: inharmonic ring over a paper slap
    t = tt(0.7); out = 0.6 * sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / dcy) for f, a, dcy in [(410, 1, .3), (1130, .6, .2), (1870, .45, .12), (2655, .3, .08)])
    s = slap(0.8); out[:len(s)] += s
    return out
def thud():
    t = tt(0.3); return np.sin(2 * np.pi * (70 + 30 * np.exp(-t / 0.02)) * t) * np.exp(-t / 0.08) + noise(0.3, 200, 1500) * np.exp(-t / 0.03) * 0.4
def tick():
    t = tt(0.03); return (np.sin(2 * np.pi * 2400 * t) * 0.6 + noise(0.03, 2000, 8000) * 0.5) * np.exp(-t / 0.005)
def blink():
    t = tt(0.05); return np.sin(2 * np.pi * (1800 - 9000 * t) * t) * np.exp(-t / 0.012)
def stamp():
    t = tt(0.8); boom = np.sin(2 * np.pi * (48 + 60 * np.exp(-t / 0.03)) * t) * np.exp(-t / 0.18)
    knock = noise(0.8, 250, 1600) * np.exp(-t / 0.035)
    return boom * 1.1 + knock * 0.9
def honk(d=0.45):
    # bulb horn: buzzy reed at a fixed pitch, nasal band, a squeeze in the envelope
    t = tt(d); f = 330 * (1 + 0.02 * np.sin(2 * np.pi * 6 * t)); ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sign(np.sin(ph)) * 0.6 + np.sin(2 * ph) * 0.4
    x = band(x, 250, 3000); env = np.minimum(1, t / 0.04) * np.minimum(1, (d - t) / 0.12)
    return norm(x) * env
# room: low murmur of a small hall
t = np.arange(N) / SR
room = norm(band(rs.standard_normal(N), 60, 500)) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.21 * t))
L += room * 0.012; R += np.roll(room, 3100) * 0.012

for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'slide': add(swish(e['d']), te, 0.12, 0.6)
    elif k == 'snip': add(snip(), te, 0.2 * v, rs.uniform(-.3, .3))
    elif k == 'swish': add(swish(e['d']), te, 0.13, rs.uniform(-.4, .4))
    elif k == 'rip':
        add(rip(), te, 0.3)
        add(chord([hz(m) for m in (36, 37, 43, 44, 49, 50)], 1.2, 0.006), te + 0.02, 0.16, 0)   # the lid slams
    elif k == 'flutter': add(flutter(e['d']), te, 0.12, 0.2)
    elif k == 'slap': add(slap(v), te, 0.22, rs.uniform(-.35, .35))
    elif k == 'clank': add(clank(), te, 0.2, -0.3)
    elif k == 'thud': add(thud(), te, 0.25, -0.3)
    elif k == 'hop': add(slap(0.4), te, 0.12 * v, 0.3)
    elif k == 'fall': add(glide(1500, 380, e['d'], 0.01), te, 0.05, 0.25)
    elif k == 'drop': add(glide(1900, 900, e['d']), te, 0.045, 0.1)
    elif k == 'blink': add(blink(), te, 0.06, -0.3)
    elif k == 'whistle': add(glide(620, 1250, e['d'], 0.008) if e.get('up') else glide(1250, 620, e['d'], 0.008), te, 0.05, -0.3)
    elif k == 'tick': add(tick(), te, 0.05, -0.35)
    elif k == 'stamp':
        add(stamp(), te, 0.4, 0.05)
        add(chord([hz(m) for m in (36, 43, 48, 55, 60, 61)], 1.6, 0.005), te + 0.01, 0.16, 0)
        add(honk(), te + 0.42, 0.11, 0.35)
# master: fade in/out, soft limiter
fi = int(0.35 * SR); fo = int(0.65 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.6) * 0.9
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
