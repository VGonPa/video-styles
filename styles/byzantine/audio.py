# events.json → audio.wav (48 kHz stereo, 10 s)
# A flint spark and the soft breath of each lamp catching; a sung drone (ison) that enters with the icon's
# flame and opens into a wide chord as the apse is revealed; handbells for the four smaller lamps; glassy
# tinks that follow the glints of the gold (panned where they sparkle); an airy shimmer under the raking
# light; a low bell when it crosses the inscription. Everything sits in a long synthetic church reverb.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(1177)
t = np.arange(N) / SR
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def add(sig, at, g=1.0, pan=0.0):
    i = int(at * SR); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def lowpass_sweep(x, fc):
    y = np.zeros_like(x); p = 0.0; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y

ev = json.load(open('events.json'))
get = lambda k: [e for e in ev if e['k'] == k]

# ── the ison: additive voices, harmonics weighted by an "o"/"a" vowel formant envelope ──
FORM = {'o': [(450, 80, 1.0), (800, 90, 0.55), (2830, 140, 0.12)], 'a': [(700, 110, 1.0), (1220, 120, 0.6), (2600, 160, 0.15)]}
def voice(f0, env, vowel='o', seed=0, det=0.0):
    r = np.random.default_rng(seed)
    drift = np.cumsum(r.standard_normal(N)) ; drift = band(drift - drift.mean(), 0.05, 3); drift /= (np.abs(drift).max() + 1e-9)
    vib = 1 + 0.0035 * np.sin(2 * np.pi * (5.1 + 0.4 * r.random()) * t + r.random() * 6) * np.clip((t - 0.6) / 1.5, 0, 1)
    f = f0 * 2 ** (det / 1200) * vib * (1 + 0.0025 * drift)
    ph = 2 * np.pi * np.cumsum(f) / SR
    out = np.zeros(N)
    for n in range(1, int(4200 / f0)):
        w = sum(a * np.exp(-0.5 * ((n * f0 - fc) / bw) ** 2) for fc, bw, a in FORM[vowel]) + 0.02 / n
        out += w / n ** 0.6 * np.sin(n * ph + r.random() * 6)
    return out * env
ign = get('ignite'); t0 = [e['t'] for e in ign if e['v'] == 1][0]
pull = get('pull')[0]; close = get('close')[0]['t']
env_lo = np.clip((t - t0 - 0.2) / 1.6, 0, 1) ** 1.5 * (1 - np.clip((t - close) / 1.0, 0, 1)) ** 1.3
env_hi = np.clip((t - pull['t'] - 0.4) / pull['d'], 0, 1) ** 1.2 * (1 - np.clip((t - close) / 0.9, 0, 1)) ** 1.3
choir = np.zeros((2, N))
for k, (m, vw, env, g, pan) in enumerate([(38, 'o', env_lo, 1.0, -0.2), (38, 'o', env_lo, 0.9, 0.25), (45, 'o', env_lo, 0.6, 0.05),
                                           (50, 'a', env_hi, 0.45, -0.45), (57, 'a', env_hi, 0.35, 0.45), (62, 'o', env_hi, 0.22, -0.1), (65, 'o', env_hi * 0.8, 0.14, 0.3)]):
    v = voice(nt(m), env, vw, seed=k + 3, det=(k % 3 - 1) * 7) * g
    choir[0] += v * np.sqrt(0.5 - pan / 2); choir[1] += v * np.sqrt(0.5 + pan / 2)
choir *= 0.05 / (np.abs(choir).max() + 1e-9) * 2.2
L += choir[0]; R += choir[1]

# ── bells ──
def bell(f, d=5.0, bright=1.0):
    tb = tt(d); s = np.zeros(len(tb))
    for ratio, a, dec in [(0.5, .55, 3.6), (1, .5, 2.8), (1.183, .42, 2.2), (1.506, .22, 1.8), (2.0, .55, 1.5), (2.514, .2 * bright, 0.9), (2.662, .16 * bright, .8), (3.011, .12 * bright, .6), (4.166, .08 * bright, .4)]:
        for dv in (0, 0.7):
            s += a * 0.5 * np.sin(2 * np.pi * (f * ratio + dv) * tb + rs.random() * 6) * np.exp(-tb / dec)
    hit = band(rs.standard_normal(len(tb)), 1500, 9000) * np.exp(-tb / 0.004)
    return (s + 0.4 * norm(hit)) * np.minimum(1, tb / 0.0015)
def handbell(f):
    tb = tt(2.6); s = sum(a * np.sin(2 * np.pi * f * h * tb + rs.random() * 6) * np.exp(-tb / dec) for h, a, dec in [(1, 1, 1.4), (3.0, .35, .5), (5.4, .12, .2), (2.0, .08, .9)])
    return s * np.minimum(1, tb / 0.001)
def spark():
    tb = tt(0.05); return norm(band(rs.standard_normal(len(tb)), 2500, 12000)) * np.exp(-tb / 0.003)
def catch(big):
    d = 0.9 if big else 0.6; tb = tt(d)
    x = rs.standard_normal(len(tb)); fc = 250 + (1400 if big else 900) * np.clip(tb / 0.18, 0, 1) * np.exp(-tb / 0.6)
    y = norm(lowpass_sweep(x, fc)) * np.clip(tb / 0.04, 0, 1) * np.exp(-tb / (0.32 if big else 0.2))
    cr = np.zeros(len(tb))
    for c0 in rs.uniform(0.02, d * 0.6, 9 if big else 5):
        i = int(c0 * SR); k = np.arange(min(240, len(tb) - i)); cr[i:i + len(k)] += rs.choice([-1, 1]) * np.exp(-k / 25.0) * rs.uniform(0.3, 1)
    return y + 0.25 * cr

hb = [74, 77, 81, 72]                                   # D5 F5 A5 C5 for the four smaller lamps
for e in ign:
    add(spark(), e['t'], 0.18, e['pan']); add(spark(), e['t'] + 0.035, 0.1, e['pan'])
    add(catch(e['v'] == 1), e['t'] + 0.11, 0.2 if e['v'] else 0.11, e['pan'])
    if e['v'] == 0:
        add(handbell(nt(hb.pop(0))), e['t'] + 0.15, 0.06, e['pan'])
    else:
        add(bell(nt(50), 5.5, 0.6), e['t'] + 0.18, 0.055, 0)  # a far bell as the icon's flame steadies

# ── glints: glassy tinks where the gold sparkles ──
for e in get('glint'):
    c = e['v']; n = int(min(4, 1 + np.sqrt(c) / 3)); g = min(0.05, 0.006 * np.sqrt(c)) / np.sqrt(n)
    for _ in range(n):
        if rs.random() > 0.55: continue
        f = rs.uniform(2600, 7600); tb = tt(0.12)
        s = (np.sin(2 * np.pi * f * tb) + 0.4 * np.sin(2 * np.pi * f * 2.76 * tb)) * np.exp(-tb / rs.uniform(0.02, 0.06))
        add(s, e['t'] + rs.uniform(0, 1 / 30), g, float(np.clip(e['pan'] + rs.uniform(-0.3, 0.3), -1, 1)))

# ── the raking light: an airy rise and fall, glass bells walking left to right ──
sw = get('sweep')[0]; tb = tt(sw['d']); u = tb / sw['d']
air = band(rs.standard_normal(len(tb)), 1200, 9000); air = norm(lowpass_sweep(air, 1500 + 6000 * np.sin(np.pi * u) ** 2))
x = air * np.sin(np.pi * u) ** 1.5 * 0.05 * 1.414; pe = 2 * u - 1; i0 = int(sw['t'] * SR); n = min(len(x), N - i0)
L[i0:i0 + n] += (x * np.sqrt(0.5 - pe / 2))[:n]; R[i0:i0 + n] += (x * np.sqrt(0.5 + pe / 2))[:n]   # pans with the light
for i, m in enumerate([86, 89, 93, 96, 98, 93, 89, 98, 101]):
    add(handbell(nt(m)), sw['t'] + 0.15 + i * sw['d'] * 0.09, 0.022, -0.85 + 1.7 * i / 8)
add(bell(nt(43), 6.0), get('title')[0]['t'], 0.14, 0)

# ── room: a soft air bed and a long church reverb ──
room = band(rs.standard_normal(N), 60, 900); room = norm(room) * 0.006 * np.clip(t / 0.4, 0, 1)
L += room; R += np.roll(room, 7919)
def ir(seed, d=3.8):
    r = np.random.default_rng(seed); tb = tt(d)
    x = r.standard_normal(len(tb)) * np.exp(-tb / 0.95)
    x = band(x, 120, 7000) * (1 - 0.45 * np.clip(tb / d, 0, 1))
    x[:int(0.018 * SR)] = 0
    return x / np.sqrt((x ** 2).sum())
def conv(x, h):
    n = 1 << int(np.ceil(np.log2(len(x) + len(h))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[:len(x)]
wetL, wetR = conv(L, ir(11)), conv(R, ir(12))
outL = L * 0.8 + wetL * 0.55; outR = R * 0.8 + wetR * 0.55
fi, fo = int(0.05 * SR), int(0.35 * SR)
for ch in (outL, outR): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 2
st = np.stack([outL, outR], 1); st = st / (np.abs(st).max() + 1e-9) * 0.9
st = np.tanh(st * 1.3) / np.tanh(1.3) * 0.88
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
