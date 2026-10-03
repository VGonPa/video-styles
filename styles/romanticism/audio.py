# events.json → audio.wav (48 kHz stereo, 10 s)
# A storm at sea: wind that gusts and whistles, rain hiss, the deep rumble of the swell. Each wave rolls
# in and bursts against the cliff (a low boom, a sheet of spray hissing back down). Strings in D minor
# tremble under it all and swell as the sky holds its breath; the lightning cracks and thunder rolls
# round the bay. A thin shimmer as the crack opens; then, as the cloud tears back, the strings swell into
# D major over a timpani and cymbal roll, the wind drops and a smaller wave breaks beneath it; a harp
# spells out the title over a low chord, and everything fades into a long hall.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(140)
t = np.arange(N) / SR
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def ramp(x, a, b): return np.clip((x - a) / (b - a), 0, 1)
def smooth(k): return k * k * (3 - 2 * k)
def add(sig, at, g=1.0, pan=0.0):
    i = int(at * SR); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def addst(l, r, g=1.0):
    L[:] += l * g; R[:] += r * g
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def noise(d, lo, hi): return norm(band(rs.standard_normal(int(d * SR)), lo, hi))
def slow(d, hz, seed):   # a smooth random curve in [0, 1]
    r = np.random.default_rng(seed); x = band(r.standard_normal(int(d * SR)), 0.05, hz)
    x -= x.min(); return x / (x.max() + 1e-9)
def onepole(x, fc):      # one-pole low-pass with a time-varying cutoff (short signals only)
    fc = np.broadcast_to(fc, x.shape); a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); p = 0.0
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y

ev = json.load(open('events.json'))
get = lambda k: [e for e in ev if e['k'] == k]
brk = get('break')[0]; close = get('close')[0]['t']; gl = get('gloom')[0]['t']; tear = get('tear')[0]
sw0, pk = tear['t'] + 0.35, brk['t'] + 0.65                                # the swell: from just after the crack to the full break
wind_k = 1 - 0.55 * smooth(ramp(t, brk['t'] + 0.6, brk['t'] + 3.2))     # the gale eases once the light is through
rain_k = 1 - smooth(ramp(t, brk['t'] + 0.6, brk['t'] + 2.3))
fade_in = smooth(ramp(t, 0, 0.8))

# ── the storm bed ──
gust = 0.35 + 0.65 * slow(DUR, 0.7, 3)
for ch, seed, pan in ((0, 5, -1), (1, 6, 1)):
    r = np.random.default_rng(seed)
    body = norm(band(r.standard_normal(N), 140, 1500)) * (0.5 + 0.5 * gust)
    air = norm(band(r.standard_normal(N), 1500, 5200)) * gust ** 2
    f = 360 + 240 * slow(DUR, 0.5, seed + 10) + 120 * gust                   # the wind whistling past the headland
    howl = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.3 + 0.7 * slow(DUR, 1.2, seed + 20)) * gust ** 1.5
    howl += 0.5 * np.sin(2 * np.pi * np.cumsum(f * 1.51) / SR) * slow(DUR, 1.0, seed + 30) * gust ** 2
    w = (0.05 * body + 0.02 * air + 0.012 * howl) * wind_k * fade_in
    (L if ch == 0 else R)[:] += w
for ch, seed in ((0, 7), (1, 8)):
    r = np.random.default_rng(seed)
    hiss = norm(band(r.standard_normal(N), 3000, 14000))
    drops = np.zeros(N); idx = r.integers(0, N, 2600); drops[idx] = r.uniform(-1, 1, len(idx))
    drops = norm(band(drops, 1800, 9000))
    (L if ch == 0 else R)[:] += (0.016 * hiss + 0.02 * drops) * rain_k * fade_in
swell_env = 0.5 + 0.5 * slow(DUR, 0.35, 9)
sea = norm(band(rs.standard_normal(N), 25, 240)) * swell_env * (1 - 0.3 * smooth(ramp(t, brk['t'], brk['t'] + 3))) * fade_in
addst(sea, np.roll(sea, 4111), 0.07)

# ── waves against the cliff ──
def swell(v):
    d = 0.85; tb = tt(d); x = rs.standard_normal(len(tb))
    y = norm(onepole(x, 120 + 900 * (tb / d) ** 2)) * (tb / d) ** 1.6
    return y * (0.6 + 0.4 * v)
def crash(v):
    d = 2.6; tb = tt(d)
    f = 52 * (1 + 0.6 * np.exp(-tb / 0.05))
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tb / 0.35)
    thud = noise(d, 30, 320) * np.exp(-tb / 0.4)
    burst = noise(d, 300, 9000) * np.exp(-tb / 0.45) * np.minimum(1, tb / 0.012)
    spray = noise(d, 2200, 12000) * smooth(np.clip((tb - 0.15) / 0.3, 0, 1)) * np.exp(-np.maximum(0, tb - 0.4) / 0.8)
    return (0.9 * boom + 0.6 * thud + 0.75 * burst + 0.35 * spray) * v
for e in get('swell'): add(swell(e['v']), e['t'], 0.09, e['pan'] * 0.7)
for e in get('crash'): add(crash(e['v']), e['t'], 0.25 if e['t'] < sw0 else 0.035, e['pan'] * 0.7)   # the wave under the swell is ducked

# ── lightning and thunder ──
def crack():
    d = 0.5; tb = tt(d)
    snap = noise(d, 1500, 14000) * np.exp(-tb / 0.02)
    rip = np.zeros(len(tb)); idx = rs.integers(0, int(0.12 * SR), 160); rip[idx] = rs.uniform(-1, 1, len(idx))
    rip = norm(band(rip, 800, 9000)) * np.exp(-tb / 0.08)
    return snap + 0.6 * rip
def thunder(d, big):
    tb = tt(d); x = norm(band(rs.standard_normal(len(tb)), 25, 520 if big else 260))
    env = np.zeros(len(tb))
    for c0 in np.sort(rs.uniform(0, d * 0.5, 7 if big else 3)):
        env += np.exp(-np.maximum(0, tb - c0) / rs.uniform(0.25, 0.7)) * (tb > c0) * rs.uniform(0.4, 1)
    env *= np.minimum(1, tb / 0.06) * np.exp(-tb / (1.6 if big else 1.0))
    return x * env / (env.max() + 1e-9)
for e in get('strike'):
    if e['v'] >= 0.4: add(crack(), e['t'], 0.2 * e['v'], e['pan'])
    else: add(thunder(2.4, False), e['t'] + 0.5, 0.12, e['pan'])        # a far flicker: only its rumble arrives
th = get('thunder')[0]; add(thunder(5.0, True), th['t'], 0.34, th['pan'] * 0.6)

# ── strings: D minor, trembling, until the tear; then D major ──
def strings(m, env, trem, seed, bright=1.0):
    r = np.random.default_rng(seed); f0 = nt(m); out = np.zeros(N)
    for det in (-7, 0, 6):
        vib = 1 + 0.003 * np.sin(2 * np.pi * (5.2 + r.random()) * t + r.random() * 6)
        ph = 2 * np.pi * np.cumsum(f0 * 2 ** (det / 1200) * vib) / SR
        for n in range(1, int(min(5200, 2600 * bright) / f0) + 1):
            out += np.sin(n * ph + r.random() * 6) / n ** 1.15
    tr = 1 - trem * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 11.5 * t + r.random() * 6))) * 0.55
    tr = np.convolve(tr, np.ones(240) / 240, 'same')                         # softened bow changes
    return out * env * tr
minor_env = 0.5 * (0.25 + 0.75 * smooth(ramp(t, 0.3, gl + 0.4))) * smooth(ramp(t, 0.1, 1.2)) * (1 - smooth(ramp(t, sw0, sw0 + 0.8)))
major_env = ramp(t, sw0 - 0.1, pk) ** 0.85 * (1 - 0.45 * smooth(ramp(t, pk, pk + 1.6))) * (1 - smooth(ramp(t, close - 0.2, DUR)))
trem_k = 0.4 + 0.6 * smooth(ramp(t, 1.0, gl + 0.3))
orch = np.zeros((2, N))
for k, (m, env, trem, g, pan) in enumerate([
        (38, minor_env, trem_k, 1.0, -0.3), (45, minor_env, trem_k, 0.8, 0.3), (50, minor_env, trem_k, 0.7, -0.15), (53, minor_env, trem_k, 0.55, 0.4), (57, minor_env, trem_k, 0.4, -0.45),
        (38, major_env, 0, 1.0, -0.3), (45, major_env, 0, 0.8, 0.3), (50, major_env, 0, 0.7, -0.1), (54, major_env, 0, 0.6, 0.35), (57, major_env, 0, 0.5, -0.4),
        (62, major_env * smooth(ramp(t, sw0 + 0.2, pk)), 0, 0.42, 0.2), (66, major_env * smooth(ramp(t, sw0 + 0.4, pk + 0.3)), 0, 0.3, -0.2)]):
    v = strings(m, env, trem, seed=40 + k, bright=1.0 if m < 60 else 0.7) * g
    orch[0] += v * np.sqrt(0.5 - pan / 2); orch[1] += v * np.sqrt(0.5 + pan / 2)
orch *= 0.11 / (np.abs(orch).max() + 1e-9)
L += orch[0]; R += orch[1]
# a high line climbing as the lantern is lifted
rz = get('raise')[0]['t']
add(np.sin(2 * np.pi * np.cumsum(nt(69) * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * tt(2.0)))) / SR) * smooth(np.clip(tt(2.0) / 0.8, 0, 1)) * np.exp(-tt(2.0) / 1.2), rz, 0.012, 0.3)

# ── timpani roll at the break, harp and a low chord for the title ──
def drum(f, d=1.4):
    tb = tt(d); s = np.sin(2 * np.pi * f * tb) * np.exp(-tb / 0.5) + 0.4 * np.sin(2 * np.pi * f * 1.5 * tb) * np.exp(-tb / 0.25)
    return (s + 0.3 * noise(d, 60, 900) * np.exp(-tb / 0.03)) * np.minimum(1, tb / 0.002)
nroll = int((pk - sw0) * 17)
for i in range(nroll):
    k = i / nroll; add(drum(nt(38)), sw0 + i / 17 + rs.uniform(-0.006, 0.006), 0.05 * (0.2 + 0.8 * k ** 1.5), rs.uniform(-0.15, 0.15))
add(drum(nt(38), 2.2), pk, 0.13, 0)
# a cymbal rolled up to the break, then let ring
tb = tt(pk - sw0 + 1.8); u = np.clip(tb / (pk - sw0), 0, 1)
cym = noise(len(tb) / SR, 3000, 13000) * (u ** 2.2) * np.where(tb < pk - sw0, 1, np.exp(-(tb - (pk - sw0)) / 0.55))
add(cym, sw0, 0.05, 0.1)
# the crack: a thin rising shimmer
td = tear.get('d', 0.65); tb = tt(td + 0.6)
shim = noise(len(tb) / SR, 2500, 11000) * smooth(np.clip(tb / td, 0, 1)) * np.exp(-np.maximum(0, tb - td) / 0.3)
shim += 0.4 * np.sin(2 * np.pi * nt(93) * tb) * smooth(np.clip(tb / td, 0, 1)) * np.exp(-np.maximum(0, tb - td) / 0.4)
add(shim, tear['t'], 0.02, 0.35)
def harp(f, d=2.4):
    tb = tt(d); s = sum(a * np.sin(2 * np.pi * f * h * tb + rs.random() * 6) * np.exp(-tb / dec) for h, a, dec in [(1, 1, 1.3), (2, .45, .7), (3, .22, .4), (4, .1, .25), (5, .05, .15)])
    return s * np.minimum(1, tb / 0.002)
ti = get('title')[0]
for i, m in enumerate([50, 57, 62, 66, 69, 74, 78, 81, 86, 90, 93][:ti['n']]):
    add(harp(nt(m)), ti['t'] + 0.05 + i * ti['step'], 0.04 * (0.7 if m > 80 else 1), -0.6 + 1.2 * i / max(1, ti['n'] - 1))
add(drum(nt(26), 3.0), ti['t'] + 0.05, 0.06, 0)
sub = get('subtitle')[0]['t']
add(harp(nt(62), 3.0), sub + 0.1, 0.04, -0.2); add(harp(nt(69), 3.0), sub + 0.16, 0.035, 0.2)

# ── a long hall ──
def ir(seed, d=3.0):
    r = np.random.default_rng(seed); tb = tt(d)
    x = r.standard_normal(len(tb)) * np.exp(-tb / 0.75)
    x = band(x, 90, 6500) * (1 - 0.5 * np.clip(tb / d, 0, 1)); x[:int(0.022 * SR)] = 0
    return x / np.sqrt((x ** 2).sum())
def conv(x, h):
    n = 1 << int(np.ceil(np.log2(len(x) + len(h))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[:len(x)]
outL = L * 0.82 + conv(L, ir(11)) * 0.42; outR = R * 0.82 + conv(R, ir(12)) * 0.42
master = smooth(ramp(t, 0, 0.25)) * (1 - smooth(ramp(t, close, DUR)) ** 1.2)
st = np.stack([outL * master, outR * master], 1)
st = np.tanh(st / (np.abs(st).max() + 1e-9) * 1.4) / np.tanh(1.4)
st *= 0.72 / (np.abs(st).max() + 1e-9)                                       # peak -2.9 dBFS: headroom for a mono fold-down
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
