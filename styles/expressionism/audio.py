# events.json → audio.wav (48 kHz stereo, 10 s)
# Colour as sound, after Kandinsky's pairing of colours and instruments: yellow is a trumpet, light blue
# a flute, dark blue a cello over an organ, red a tuba with a drum, green a calm violin, violet a
# bassoon, orange a bell (pink a celesta, black a woodblock). Every shape that appears or lets go of
# the landscape sounds in its own colour, panned where it is on screen. A timpani walks the 120 BPM
# beat on D and A; the brush whips across the stereo field with each slash; the morph rises as a
# dissonant string cluster with a cymbal swell, the title lands on timpani, tam-tam and a tense chord
# (tritone, major seventh, minor ninth) that opens out into bare fifths, and everything fades with the
# picture.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(143)
TAU = 2 * np.pi
t = np.arange(N) / SR
def tt(d): return np.arange(int(d * SR)) / SR
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def norm(x): return x / (np.abs(x).max() + 1e-9)
def ramp(x, a, b): return np.clip((x - a) / (b - a), 0, 1)
def smooth(k): return k * k * (3 - 2 * k)
def add(sig, at, g=1.0, pan=0.0):
    i = int(round(at * SR)); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    p = np.asarray(pan, float)
    p = p[:n] if p.ndim else p
    L[i:i + n] += sig[:n] * g * np.cos((p + 1) * np.pi / 4) * 1.414
    R[i:i + n] += sig[:n] * g * np.sin((p + 1) * np.pi / 4) * 1.414
def band(x, lo, hi):      # soft band-pass in the frequency domain
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4) / (1 + (f / hi) ** 4)
    return np.fft.irfft(X, len(x))
def noise(d, lo, hi): return norm(band(rs.standard_normal(int(d * SR)), lo, hi))
def sweep(x, f0, f1, q=3.0):  # state-variable band-pass whose centre glides from f0 to f1 (short signals)
    fc = np.geomspace(f0, f1, len(x)); y = np.empty_like(x); lo = bp = 0.0
    for i in range(len(x)):
        f = 2 * np.sin(np.pi * fc[i] / SR); hp = x[i] - lo - bp / q; bp += f * hp; lo += f * bp; y[i] = bp
    return y
def partials(f0, d, amps, vib=0.0, vrate=5.5, vdelay=0.2, scoop=0.0, bend=0.0, fmax=11000, seed=0):
    tb = tt(d); r = np.random.default_rng(seed)
    v = vib * np.sin(TAU * vrate * tb + r.random() * 6) * smooth(np.clip(tb / max(vdelay, 1e-3), 0, 1))
    f = f0 * (1 + v - scoop * np.exp(-tb / 0.05)) * 2 ** (bend * smooth(np.clip(tb / d, 0, 1)) / 12)
    ph = TAU * np.cumsum(f) / SR; out = np.zeros(len(tb))
    for n, a in enumerate(amps, 1):
        if n * f0 > fmax: break
        if a: out += a * np.sin(n * ph + r.random() * 6)
    return out
def shape(d, a, r, dec=None):
    tb = tt(d); e = smooth(np.clip(tb / a, 0, 1)) * np.clip((d - tb) / r, 0, 1)
    return e * (np.exp(-tb / dec) if dec else 1)

# ── the colour instruments ──
def trumpet(m, d, seed=0, bend=0.0):
    f0 = hz(m); H = int(10000 // f0)
    amps = [(1 / n ** 0.8) * (1 + 1.8 * np.exp(-((n * f0 - 1400) / 650) ** 2)) for n in range(1, H + 1)]
    tb = tt(d)
    return norm(partials(f0, d, amps, vib=0.004, vrate=5.8, vdelay=0.25, scoop=0.03, bend=bend, seed=seed)) * shape(d, 0.02, 0.08) * (0.65 + 0.35 * np.exp(-tb / 0.08))
def flute(m, d, seed=0, bend=0.0):
    f0 = hz(m); x = norm(partials(f0, d, [1, 0.18, 0.06, 0.02], vib=0.006, vrate=5.0, vdelay=0.15, bend=bend, seed=seed))
    return (x + 0.12 * noise(d, f0 * 0.8, f0 * 3)) * shape(d, 0.07, 0.12)
def cello(m, d, seed=0, bend=0.0, att=0.12):
    f0 = hz(m); H = int(4200 // f0)
    x = norm(partials(f0, d, [1 / n ** 1.05 for n in range(1, H + 1)], vib=0.004, vrate=5.3, vdelay=0.2, bend=bend, seed=seed))
    org = norm(partials(f0 / 2, d, [0.6, 0.35, 0, 0.2], bend=bend, seed=seed + 1))
    return (x + 0.45 * org) * shape(d, att, 0.2)
def tuba(m, d, seed=0, bend=0.0):
    f0 = hz(m); tb = tt(d)
    x = norm(partials(f0, d, [1 / n ** 1.6 for n in range(1, 9)], scoop=0.04, bend=bend, seed=seed)) * shape(d, 0.03, 0.1)
    thump = np.sin(TAU * 52 * tb * (1 + 0.5 * np.exp(-tb / 0.03))) * np.exp(-tb / 0.12)
    return x + 0.6 * thump
def violin(m, d, seed=0, bend=0.0):
    f0 = hz(m); H = int(7000 // f0)
    return norm(partials(f0, d, [1 / n ** 1.1 for n in range(1, H + 1)], vib=0.006, vrate=6.0, vdelay=0.2, bend=bend, seed=seed)) * shape(d, 0.09, 0.15)
def bassoon(m, d, seed=0, bend=0.0):
    f0 = hz(m); H = int(5000 // f0)
    amps = [(1 if n % 2 else 0.35) / n * (1 + 1.4 * np.exp(-((n * f0 - 520) / 260) ** 2)) for n in range(1, H + 1)]
    return norm(partials(f0, d, amps, vib=0.003, vrate=5.0, bend=bend, seed=seed)) * shape(d, 0.045, 0.1)
def bell(m, d, seed=0, bend=0.0):
    f0 = hz(m) * 2 ** (bend / 12); tb = tt(d); r = np.random.default_rng(seed)
    s = sum(a * np.sin(TAU * f0 * k * tb + r.random() * 6) * np.exp(-tb / dc) for k, a, dc in [(1, 1, 1.6), (2.0, 0.5, 1.0), (2.76, 0.4, 0.7), (4.07, 0.25, 0.45), (5.4, 0.15, 0.3), (6.9, 0.08, 0.2)])
    return s * np.minimum(1, tb / 0.002) * np.clip((d - tb) / 0.05, 0, 1)
def celesta(m, d, seed=0, bend=0.0):
    f0 = hz(m) * 2 ** (bend / 12); tb = tt(d)
    s = np.sin(TAU * f0 * tb) * np.exp(-tb / 0.6) + 0.3 * np.sin(TAU * 4 * f0 * tb) * np.exp(-tb / 0.1)
    return s * np.minimum(1, tb / 0.002) * np.clip((d - tb) / 0.05, 0, 1)
def wood(f=950, d=0.14):
    tb = tt(d)
    return (np.sin(TAU * f * tb) * np.exp(-tb / 0.025) + 0.5 * np.sin(TAU * f * 2.6 * tb) * np.exp(-tb / 0.012) + 0.3 * noise(d, 1500, 6000) * np.exp(-tb / 0.004))
VOICE = {'yellow': trumpet, 'lemon': trumpet, 'cobalt': flute, 'ultra': cello, 'prussian': cello, 'vermilion': tuba, 'crimson': tuba,
         'acid': violin, 'emerald': violin, 'violet': bassoon, 'orange': bell, 'pink': celesta}
NOTE = {'yellow': 74, 'lemon': 79, 'cobalt': 81, 'ultra': 43, 'prussian': 50, 'vermilion': 38, 'crimson': 41, 'acid': 69, 'emerald': 64,
        'violet': 46, 'orange': 86, 'pink': 89}
GAIN = {trumpet: 0.07, flute: 0.07, cello: 0.08, tuba: 0.1, violin: 0.06, bassoon: 0.07, bell: 0.05, celesta: 0.05}
def colour(c, d, at, pan, v=1.0, m=None, bend=0.0, seed=0):
    if c == 'black':
        for j in range(3): add(wood(700 + 180 * j), at + 0.035 * j, 0.06 * v, pan)
        return
    fn = VOICE[c]; add(fn(NOTE[c] if m is None else m, d, seed=seed, bend=bend), at, GAIN[fn] * v, pan)

# ── percussion ──
def timp(m, d=1.3, hard=1.0):
    f0 = hz(m); tb = tt(d)
    f = f0 * (1 + 0.06 * np.exp(-tb / 0.04))
    ph = TAU * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-tb / 0.55) + 0.5 * np.sin(1.5 * ph) * np.exp(-tb / 0.3) + 0.25 * np.sin(1.99 * ph) * np.exp(-tb / 0.2)
    return (s + 0.35 * hard * noise(d, 80, 1600) * np.exp(-tb / 0.02)) * np.minimum(1, tb / 0.002)
def tick(d=0.05): tb = tt(d); return noise(d, 5000, 14000) * np.exp(-tb / 0.012)

ev = json.load(open('events.json'))
get = lambda k: [e for e in ev if e['k'] == k]
ti = get('title')[0]['t']; close = get('close')[0]; sw = get('swell')[0]

for e in get('beat'):
    if e['t'] >= ti - 0.01 and e['t'] < ti + 0.01: continue        # the title hit replaces this beat
    add(timp(38 if e['i'] % 2 == 0 else 33, hard=e['v']), e['t'], 0.2 * e['v'], 0)
for e in get('tick'): add(tick(), e['t'], 0.05 * (0.6 + 0.4 * e['v']), 0.35 if int(e['t'] * 4) % 2 else -0.35)

# the brush: bristles dragging in at the edge and ink drops landing, then a whip and a string scrape travelling across
for e in get('brush'):
    tb = tt(e['d'] + 0.04); drag = noise(len(tb) / SR, 900, 6500) * (0.6 + 0.4 * rs.standard_normal(len(tb)).clip(-1, 1))
    add(drag * (0.15 + 0.85 * (tb / tb[-1]) ** 1.5), e['t'], 0.16, e['pan'])
for e in get('drop'):
    tb = tt(0.12); f = 1300 * np.exp(-tb / 0.03) + 380
    plop = np.sin(TAU * np.cumsum(f) / SR) * np.exp(-tb / 0.03) + 0.4 * noise(0.12, 2000, 9000) * np.exp(-tb / 0.004)
    add(plop, e['t'], 0.11 * (0.5 + 0.5 * e['v']), e['pan'])
for e in get('whip'):
    d = e['d'] + 0.25; tb = tt(d); x = rs.standard_normal(len(tb))
    wh = norm(sweep(x, 350, 7000, 2.5)) * np.minimum(1, tb / 0.01) * np.exp(-np.maximum(0, tb - e['d']) / 0.06)
    scrape = norm(band(partials(98 * (1 + 0.02 * rs.random()), d, [1 / n for n in range(1, 40)]) * (1 + 0.6 * rs.standard_normal(len(tb))), 700, 3500)) * np.exp(-tb / 0.18)
    p = e['from'] + (e['to'] - e['from']) * np.clip(tb / e['d'], 0, 1)
    add(wh, e['t'], 0.2 * e['v'], p); add(scrape, e['t'] + 0.02, 0.07 * e['v'], p)
# contours and hatches being drawn: dry scratches
for e in get('ink') + get('hatch'):
    n = int(e['d'] * 28)
    for j in range(n):
        d = 0.06; tb = tt(d); add(noise(d, 1800, 9000) * np.exp(-tb / 0.018), e['t'] + e['d'] * j / n + rs.uniform(0, 0.01), 0.04, e['pan'] + rs.uniform(-0.4, 0.4))

# colour floods: a swelling chord in the field's instrument
CHORD = {'yellow': [69, 74, 78], 'acid': [62, 69, 74], 'emerald': [57, 64]}
for e in get('flood'):
    for j, m in enumerate(CHORD[e['c']]):
        colour(e['c'], e['d'] + 0.5, e['t'] + 0.02 * j, e['pan'] + 0.3 * (j - 1), v=0.8, m=m, seed=j)
    tb = tt(e['d'] + 0.2); add(noise(len(tb) / SR, 600, 5000) * smooth(np.clip(tb / e['d'], 0, 1)) * np.exp(-np.maximum(0, tb - e['d']) / 0.08), e['t'], 0.03, e['pan'])
# shapes popping in: their colour's note
for e in get('pop'): colour(e['c'], 0.55 if e['c'] not in ('orange', 'pink') else 1.4, e['t'], e['pan'], v=e['v'] * 1.2)
# mountains rise: a glide up into the note
for e in get('rise'): colour(e['c'], 0.9, e['t'], e['pan'], v=e['v'] * 1.3, m=NOTE[e['c']] - 5, bend=5)
# a field swaps hue for one beat: a stab in the new colour
for e in get('swap'):
    for j, m in enumerate([NOTE[e['c']], NOTE[e['c']] + 7]): colour(e['c'], 0.45, e['t'] + 0.015 * j, 0.25 * (j - 0.5), v=0.9, m=m)
# the sun's rings: a faint glass ping
for e in get('ring'):
    d = 0.9; tb = tt(d); add(np.sin(TAU * hz(93) * tb) * np.exp(-tb / 0.35) * np.minimum(1, tb / 0.003), e['t'] + 0.03, 0.012, e['pan'])

# ── the transformation: each shape lets go with a bent note; a string cluster and a cymbal swell ──
for j, e in enumerate(get('morph')): colour(e['c'], 0.7, e['t'], e['pan'], v=0.75, bend=1.5 if j % 2 else -1.0, seed=10 + j)
d = sw['d']; tb = tt(d); cl = np.zeros(len(tb))
for j, m in enumerate([62, 63, 64, 66, 67, 69, 70]):
    cl += partials(hz(m), d, [1 / n ** 1.15 for n in range(1, 16)], vib=0.006, vrate=5.6 + 0.3 * j, vdelay=0.1, bend=1.0, seed=30 + j)
trem = 1 - 0.35 * (0.5 + 0.5 * np.sin(TAU * (9 + 5 * tb / d) * tb))
cl = norm(cl) * trem * (tb / d) ** 2.2 * np.clip((d - tb) / 0.006, 0, 1)
add(cl, sw['t'], 0.11, -0.15); add(np.roll(cl, 300), sw['t'], 0.08, 0.3)
cym = noise(d, 3500, 15000) * (tb / d) ** 3 * np.clip((d - tb) / 0.006, 0, 1)
add(cym, sw['t'], 0.07, 0.1)
for e in get('windup'):                          # the inhale before the slam
    tb = tt(e['d']); add(noise(e['d'], 300, 3000) * (tb / e['d']) ** 2.5 * np.clip((e['d'] - tb) / 0.005, 0, 1), e['t'], 0.06, 0)
for e in get('mark'):
    if e['kind'] == 'hatch':
        for j in range(5): tb = tt(0.05); add(noise(0.05, 2500, 9000) * np.exp(-tb / 0.012), e['t'] + 0.04 * j, 0.05, e['pan'])
    else: add(flute(81 if e['i'] == 1 else 76, 0.5, bend=-3), e['t'], 0.05, e['pan'])
# the colour clouds bloom: a soft, slow swell in each cloud's own instrument
for j, e in enumerate(get('cloud')):
    tb = tt(1.4); add(VOICE[e['c']](NOTE[e['c']] - 12 if e['c'] in ('lemon', 'cobalt', 'pink') else NOTE[e['c']], 1.4, seed=70 + j) * np.sin(np.pi * tb / 1.4) ** 2, e['t'], GAIN[VOICE[e['c']]] * 0.5, e['pan'])

# ── the title: timpani, tam-tam and a tense chord that opens into bare fifths ──
add(timp(38, 2.5), ti, 0.42, 0); add(timp(26, 2.5, 0.5), ti, 0.3, 0)
tb = tt(3.5); r = np.random.default_rng(7); tam = np.zeros(len(tb))
for j in range(60):
    f = r.uniform(180, 3600); tam += np.sin(TAU * f * tb + r.random() * 6) * np.exp(-tb / r.uniform(0.5, 2.0)) / np.sqrt(f / 180)
tam = norm(tam) * smooth(np.clip(tb / 0.08, 0, 1)) + 0.3 * noise(3.5, 200, 6000) * np.exp(-tb / 0.12)
add(tam, ti, 0.1, 0.1)
hold = DUR - ti
tense = np.zeros((2, int(hold * SR))); openc = np.zeros_like(tense)
tense_env = 1 - smooth(ramp(tt(hold), 0.35, 1.0)); open_env = smooth(ramp(tt(hold), 0.45, 1.0))
for j, (m, fn, p) in enumerate([(50, cello, -0.3), (56, violin, 0.3), (61, violin, -0.2), (63, trumpet, 0.25), (69, violin, 0.0)]):
    s = fn(m, hold, seed=40 + j) * tense_env; tense[0] += s * np.cos((p + 1) * np.pi / 4); tense[1] += s * np.sin((p + 1) * np.pi / 4)
for j, (m, fn, p) in enumerate([(38, cello, 0.0), (50, cello, -0.3), (57, violin, 0.3), (62, violin, -0.2), (69, flute, 0.25), (76, flute, -0.1)]):
    s = fn(m, hold, seed=50 + j) * open_env; openc[0] += s * np.cos((p + 1) * np.pi / 4); openc[1] += s * np.sin((p + 1) * np.pi / 4)
chord = tense * 0.6 + openc * 0.5
chord *= 0.12 / (np.abs(chord).max() + 1e-9)
i0 = int(ti * SR); L[i0:i0 + chord.shape[1]] += chord[0][:N - i0]; R[i0:i0 + chord.shape[1]] += chord[1][:N - i0]
su = get('sub')[0]['t']
for j, m in enumerate([74, 81, 86]): add(bell(m, 2.2), su + 0.07 * j, 0.035, -0.3 + 0.3 * j)

# ── a small hall, then the fade with the picture ──
def ir(seed, d=1.8):
    r = np.random.default_rng(seed); tb = tt(d); x = r.standard_normal(len(tb)) * np.exp(-tb / 0.45)
    x = band(x, 120, 7000); x[:int(0.018 * SR)] = 0
    return x / np.sqrt((x ** 2).sum())
def conv(x, h):
    n = 1 << int(np.ceil(np.log2(len(x) + len(h))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[:len(x)]
outL = L + conv(L, ir(11)) * 0.3; outR = R + conv(R, ir(12)) * 0.3
master = smooth(ramp(t, 0, 0.04)) * (1 - smooth(ramp(t, close['t'] + 0.05, DUR - 0.02)))
st = np.stack([outL * master, outR * master], 1)
st = np.tanh(st / (np.abs(st).max() + 1e-9) * 1.5) / np.tanh(1.5)
st *= 0.89 / (np.abs(st).max() + 1e-9)                                       # peak about -1 dBFS
st[-int(0.02 * SR):] = 0
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
