# events.json → audio.wav (48 kHz stereo, 10 s)
# A viol consort holds a drone in D that moves with the painting: an open fifth while the panel is
# constructed, D minor as the glazes go on, the bright Dorian G major for the gold, A major with its
# leading note under the title, and a Picardy D major to close. Over it: a plucked lute
# (Karplus-Strong) that runs up the transversals and gilds each letter, a stylus scratch for every
# construction line, a charcoal whisper for the sinopia, loaded-brush swishes for the underpainting
# and airy ones for the glazes, papery ticks as the gold leaf lands, a bell-bright shimmer for the
# raking glint, ratchet clicks and a small ring as the armillary sphere turns and settles.
# Everything sits in the reverb of a stone loggia and fades with the panel.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(137)
t = np.arange(N) / SR
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def add(sig, at, g=1.0, pan=0.0):
    i = int(round(at * SR)); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    pan = float(np.clip(pan, -1, 1))
    L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi, edge=0.15):   # FFT band-pass with soft shoulders
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    g = np.clip((f - lo * (1 - edge)) / (lo * edge * 2 + 1e-9), 0, 1) * np.clip((hi * (1 + edge) - f) / (hi * edge * 2 + 1e-9), 0, 1)
    return np.fft.irfft(X * g, len(x))
def env(n, a, d):   # attack seconds, exponential decay time constant
    x = np.arange(n) / SR; return np.minimum(1, x / max(a, 1e-4)) * np.exp(-x / d)

ev = json.load(open('events.json'))
get = lambda k: [e for e in ev if e['k'] == k]
one = lambda k: get(k)[0]

# ── the viol consort: bowed additive voices, a little vibrato and bow noise, chords that cross-fade ──
def viol(f0, seed):
    r = np.random.default_rng(seed)
    vib = 1 + 0.004 * np.sin(2 * np.pi * (4.6 + r.random()) * t + r.random() * 6) * np.clip((t - 0.5) / 1.2, 0, 1)
    ph = 2 * np.pi * np.cumsum(f0 * vib) / SR
    out = np.zeros(N)
    for n in range(1, int(5000 / f0)):
        fn = n * f0; a = (1 / n ** 1.15) * (1 + 1.2 * np.exp(-((fn - 1100) / 500) ** 2))   # a nasal body resonance
        out += a * np.sin(n * ph + r.random() * 6)
    return out / 3
light = one('light'); push = one('push'); title0 = get('letter')[0]['t']; glow = one('glow')['t']; close = one('close')['t']
CHORDS = [   # (start, midi notes)
    (one('vp')['t'], [38, 45]), (one('glaze')['t'], [38, 45, 53, 57]), (push['t'], [43, 50, 59, 62]),
    (title0 - 0.05, [45, 52, 57, 61]), (glow, [38, 45, 50, 54, 57]),
]
ends = [c[0] for c in CHORDS[1:]] + [DUR + 1]
consort = np.zeros((2, N)); cache = {}
for k, ((t0, notes), t1) in enumerate(zip(CHORDS, ends)):
    e = np.clip((t - t0) / (0.9 if k == 0 else 0.45), 0, 1) ** 1.4 * np.clip((t1 + 0.35 - t) / 0.45, 0, 1)
    for j, m in enumerate(notes):
        if m not in cache: cache[m] = viol(nt(m), m)
        pan = (j / max(1, len(notes) - 1) - 0.5) * 0.7
        g = (0.9 if m < 48 else 0.55) * e
        consort[0] += cache[m] * g * np.sqrt(0.5 - pan / 2); consort[1] += cache[m] * g * np.sqrt(0.5 + pan / 2)
# the key light opens the consort's tone: dark until the light, brighter after
dark = np.stack([band(c, 50, 700) for c in consort]); bright = np.stack([band(c, 50, 3200) for c in consort])
k_light = np.clip((t - light['t']) / light['d'], 0, 1)
consort = dark * (1 - k_light) + bright * k_light
fade = np.clip((DUR - 0.05 - t) / 0.9, 0, 1) ** 1.5
consort *= 0.06 / (np.abs(consort).max() + 1e-9) * fade
L += consort[0]; R += consort[1]

# ── the lute: Karplus-Strong strings with a small wooden body ──
BODY = sum(a * np.sin(2 * np.pi * f * tt(0.05)) * np.exp(-tt(0.05) / d) for f, a, d in [(110, 1.0, 0.012), (240, 0.7, 0.008), (520, 0.35, 0.005)])
def lute(f, d=1.6, bright=0.5):
    n = int(d * SR); P = max(2, int(round(SR / f))); damp = 0.997 if f < 300 else 0.994
    z = np.zeros(n + P + 2)
    burst = rs.standard_normal(P * 4); z[1:P + 1] = band(burst, 40, min(2500 + 5000 * bright, f * 12))[:P]
    for s in range(P + 1, n + P + 2, P):
        e = min(s + P, n + P + 2)
        z[s:e] = 0.5 * damp * (z[s - P:e - P] + z[s - P - 1:e - P - 1])
    y = z[1:n + 1]; y = y + 0.25 * np.convolve(y, BODY)[:n] / np.abs(BODY).sum()
    return norm(y) * np.minimum(1, np.arange(n) / 30)
def strum(at, notes, g, spread=0.022, pan=0.0):
    for j, m in enumerate(notes): add(lute(nt(m), 2.6, 0.4), at + j * spread, g, pan + (j - len(notes) / 2) * 0.08)

vp = one('vp')['t']
strum(vp + 0.02, [50, 57], 0.07)
# a run up the D Dorian scale as the transversals step forward
for e, m in zip(get('step'), [62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81]):
    add(lute(nt(m), 1.0, 0.6), e['t'] + 0.03, 0.045, -0.5 + e['i'] / 11)
# each gilded letter a plucked note, rising to the title's last letter
for e, m in zip(get('letter'), [57, 61, 64, 66, 69, 71, 73, 74, 76, 78, 81]):
    add(lute(nt(m), 1.5, 0.55), e['t'], 0.055, -0.45 + e['i'] * 0.09)
strum(one('motto')['t'] + 0.05, [52, 57, 61, 64], 0.06, 0.035)
strum(glow + 0.05, [50, 57, 62, 66, 69], 0.075, 0.03)
strum(close - 0.05, [38, 45, 50, 54], 0.055, 0.04)

# ── the construction: a stylus scratching each line into the gesso, a tick at each check point ──
def scratch(d, bright=1.0):
    n = int(d * SR); x = rs.standard_normal(n)
    grit = np.repeat(rs.random(n // 120 + 1), 120)[:n] ** 3
    y = band(x * (0.35 + grit), 2200 * bright, 9000)
    e = np.minimum(1, np.arange(n) / (0.01 * SR)) * np.clip((n - np.arange(n)) / (0.03 * SR), 0, 1)
    return norm(y) * e
for e in get('line'): add(scratch(e['d'] * 0.9), e['t'], 0.007, -0.6 + e['i'] / 25 * 1.2)
for e in get('step'): add(scratch(e['d'] * 0.8, 0.8), e['t'], 0.005, 0.3)
dg = one('diag'); add(scratch(dg['d']), dg['t'], 0.01, 0.4)
for e in get('tick'):
    s = np.sin(2 * np.pi * 4200 * tt(0.04)) * np.exp(-tt(0.04) / 0.006); add(s, e['t'], 0.02, 0.2)
# the sinopia: a dry charcoal whisper while the figure and the loggia are drawn
sn = one('sinopia'); n = int(sn['d'] * SR)
x = band(rs.standard_normal(n), 1400, 6000); am = np.interp(np.arange(n), np.linspace(0, n, 40), rs.random(40)) ** 2
add(norm(x) * am * np.sin(np.pi * np.arange(n) / n) ** 0.5, sn['t'], 0.03, 0.15)

# ── the brushes: loaded swishes for the underpainting, airy ones for the glazes ──
def swish(d, lo, hi, a=0.02, dec=0.11):
    n = int(d * SR); x = rs.standard_normal(n)
    drag = 0.6 + 0.4 * np.interp(np.arange(n), np.linspace(0, n, 12), rs.random(12))
    return norm(band(x, lo, hi)) * env(n, a, dec) * drag
for e in get('brush'): add(swish(0.4, 260, 2600), e['t'] + rs.uniform(0, 0.03), 0.04 * min(1.6, np.sqrt(e['v']) / 2.2), e['pan'] * 0.7)
for e in get('wash'): add(swish(0.6, 1200, 7500, 0.06, 0.2), e['t'] + rs.uniform(0, 0.04), 0.022 * min(1.6, np.sqrt(e['v']) / 2.2), e['pan'] * 0.7)

# ── gold: the bole dabbed on, leaf landing in squares, a raking shimmer ──
bo = one('bole'); add(swish(bo['d'] + 0.2, 150, 900, 0.05, 0.25), bo['t'], 0.03, -0.2)
for e in get('leaf'):
    for _ in range(min(4, 1 + e['v'] // 6)):
        f = rs.uniform(3000, 7000); n = int(0.02 * SR)
        s = band(rs.standard_normal(n), f * 0.7, f * 1.3) * env(n, 0.0005, 0.004)
        add(norm(s), e['t'] + rs.uniform(0, 1 / 30), 0.012 * min(2, np.sqrt(e['v']) / 3), rs.uniform(-0.8, 0.8))
def bellnote(f, d, bright=1.0):
    x = tt(d); s = np.zeros(len(x))
    for ratio, a, dec in [(1, 0.6, 1.6), (2.0, 0.35, 1.0), (2.76, 0.3 * bright, 0.6), (5.4, 0.15 * bright, 0.25), (8.9, 0.06 * bright, 0.12)]:
        s += a * np.sin(2 * np.pi * f * ratio * x + rs.random() * 6) * np.exp(-x / dec)
    return s * np.minimum(1, x / 0.002)
gl = one('glint')
for i, m in enumerate([86, 89, 93, 91, 98, 96, 93, 101, 98]):
    add(bellnote(nt(m), 2.2), gl['t'] + 0.05 + i * gl['d'] * 0.1, 0.018, -0.8 + 1.6 * i / 8)
n = int(gl['d'] * SR); sh = sum(np.sin(2 * np.pi * f * tt(gl['d']) + rs.random() * 6) for f in [2349, 2352, 2793, 3136, 3522, 3527])
add(sh * np.sin(np.pi * np.arange(n) / n) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * tt(gl['d']))), gl['t'], 0.006, 0)
add(bellnote(nt(81), 3.0, 0.6), glow, 0.03, -0.1)

# ── the sphere: a breath of air on the push, the fingertip's brush, ratchet clicks, a small ring ──
n = int(push['d'] * SR); add(norm(band(rs.standard_normal(n), 80, 500)) * np.sin(np.pi * np.arange(n) / n) ** 2, push['t'], 0.03, 0.1)
tu = one('turn'); add(swish(0.35, 500, 3000, 0.08, 0.1), tu['t'] + 0.25, 0.03, -0.1)
for e in get('click'):
    n = int(0.03 * SR); s = sum(np.sin(2 * np.pi * f * tt(0.03)) * np.exp(-tt(0.03) / dd) for f, dd in [(3400, 0.004), (5200, 0.003), (7100, 0.002)])
    add(s + 0.3 * band(rs.standard_normal(n), 2000, 9000) * env(n, 0.0003, 0.002), e['t'], 0.03 * (1 if e['v'] > 0 else 0.6), -0.25)
st = one('settle')['t']; x = tt(2.2)
ring = sum(a * np.sin(2 * np.pi * 880 * r_ * x + rs.random() * 6) * np.exp(-x / d) for r_, a, d in [(1, 0.6, 1.2), (2.41, 0.4, 0.7), (3.93, 0.25, 0.45), (5.62, 0.12, 0.25)])
add(ring * np.minimum(1, x / 0.003), st, 0.03, -0.25)

# ── the loggia: a faint air bed and a stone-room reverb ──
room = band(rs.standard_normal(N), 60, 700); room = norm(room) * 0.004 * np.clip(t / 0.4, 0, 1) * fade
L += room; R += np.roll(room, 7919)
def ir(seed, d=2.4):
    r = np.random.default_rng(seed); x = tt(d)
    y = r.standard_normal(len(x)) * np.exp(-x / 0.55)
    y = band(y, 150, 6500) * (1 - 0.5 * np.clip(x / d, 0, 1)); y[:int(0.014 * SR)] = 0
    return y / np.sqrt((y ** 2).sum())
def conv(x, h):
    n = 1 << int(np.ceil(np.log2(len(x) + len(h))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[:len(x)]
wetL, wetR = conv(L, ir(11)), conv(R, ir(12))
outL = L * 0.82 + wetL * 0.42; outR = R * 0.82 + wetR * 0.42
# sound and light die together: from the close the whole mix sinks over the last ~0.9 s
master = np.ones(N); k = t >= close; master[k] = (1 - np.clip((t[k] - close) / (DUR - close - 0.02), 0, 1)) ** 1.6
def highpass(x, fc=28):   # no DC or sub-bass rumble
    X = np.fft.rfft(x - x.mean()); f = np.fft.rfftfreq(len(x), 1 / SR); X *= np.clip((f - fc * 0.6) / (fc * 0.4), 0, 1); return np.fft.irfft(X, len(x))
outL, outR = highpass(outL) * master, highpass(outR) * master
fi = int(0.03 * SR)
for ch in (outL, outR): ch[:fi] *= np.linspace(0, 1, fi)
st2 = np.stack([outL, outR], 1); st2 = st2 / (np.abs(st2).max() + 1e-9) * 0.9
st2 = np.tanh(st2 * 1.25) / np.tanh(1.25) * 0.89
pcm = (np.clip(st2, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st2).max().round(3))
