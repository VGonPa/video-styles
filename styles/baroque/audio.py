# events.json → audio.wav (48 kHz stereo, 10 s), all of it synthesised here.
# D minor, a small Baroque band in a stone room: the beam stutters on with the soft knock of a shutter and
# an organ pedal fades in under it; a rope creaks through its pulley while the curtain dips and is hauled
# up in a rush of velvet, a timpani stroke lands as the swag arrives and the bullion tassels chime; strings
# and a harpsichord continuo walk i–iv–VI–V while the light crosses the still life, with sand trickling in
# the hourglass. The silk flutters at the corner, draws breath, and is thrown: a whoosh that follows it
# across the stereo field over a rising string run. The title lands on a harpsichord flourish and a drum
# stroke, the gilding glints, and the light irises down on a cadence (iv6–V7–I, with a Picardy third)
# that dies away with the picture. Everything sits in a synthetic stone-hall reverb.
import json, wave
import numpy as np

SR, DUR = 48000, 10.0
N = int(SR * DUR)
t = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(138)

ev = json.load(open('events.json'))
one = lambda k: next(e for e in ev if e['k'] == k)
every = lambda k: [e for e in ev if e['k'] == k]
nt = lambda m: 440.0 * 2 ** ((m - 69) / 12)


def tt(d):
    return np.arange(int(d * SR)) / SR


def add(sig, at, g=1.0, pan=0.0):
    """Mix a mono signal (or a per-sample pan array) in at time `at`, equal-power panned."""
    i = int(round(at * SR))
    if i < 0:
        sig = sig[-i:]; pan = pan[-i:] if np.ndim(pan) else pan; i = 0
    n = min(len(sig), N - i)
    if n <= 0:
        return
    p = np.clip(pan[:n] if np.ndim(pan) else pan, -1, 1)
    a = (p + 1) * np.pi / 4
    L[i:i + n] += sig[:n] * g * np.cos(a) * 1.4142
    R[i:i + n] += sig[:n] * g * np.sin(a) * 1.4142


def peak(x):
    return x / (np.abs(x).max() + 1e-12)


def fft_band(x, lo, hi, order=4):
    """Zero-phase band-pass with Butterworth-shaped skirts."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR) + 1e-3
    g = 1 / (1 + (lo / f) ** (2 * order)) / (1 + (f / hi) ** (2 * order))
    return np.fft.irfft(X * g, len(x))


def moving_band(x, fc, bw):
    """Time-varying Gaussian band-pass (centre fc[n], width bw[n] in Hz), by short-time FFT overlap-add."""
    n, M = len(x), 2048
    hop, win = M // 4, np.hanning(M)
    pad = np.concatenate([np.zeros(M), x, np.zeros(M)])
    out = np.zeros(len(pad)); norm = np.zeros(len(pad))
    f = np.fft.rfftfreq(M, 1 / SR)
    for s in range(0, len(pad) - M, hop):
        c = min(n - 1, max(0, s + M // 2 - M))
        G = np.exp(-0.5 * ((f - fc[c]) / bw[c]) ** 2)
        out[s:s + M] += np.fft.irfft(np.fft.rfft(pad[s:s + M] * win) * G, M) * win
        norm[s:s + M] += win ** 2
    return (out / np.maximum(norm, 1e-6))[M:M + n]


def adsr(n, att, rel):
    x = np.arange(n) / SR
    d = n / SR
    e = np.clip(x / max(att, 1e-4), 0, 1) ** 1.6
    return e * np.clip((d - x) / max(rel, 1e-4), 0, 1) ** 1.3


# ── instruments ──
def string_voice(f0, d, att, rel, seed, bright=1.0):
    """One bowed voice: band-limited saw with delayed vibrato, slight bow noise."""
    r = np.random.default_rng(seed); x = tt(d)
    vib = 1 + 0.0042 * np.sin(2 * np.pi * (5.2 + 0.6 * r.random()) * x + r.random() * 6) * np.clip((x - 0.25) / 0.5, 0, 1)
    ph = 2 * np.pi * np.cumsum(f0 * vib) / SR + r.random() * 6
    s = np.zeros(len(x))
    for k in range(1, min(28, int(6000 / f0)) + 1):
        s += np.sin(k * ph) / k * np.exp(-k * f0 / (2600 * bright))
    s += 0.02 * fft_band(r.standard_normal(len(x)), 800, 5000)
    return s * adsr(len(x), att, rel)


def strings(notes, t0, t1, g, att=0.35, rel=0.5, bright=1.0, swell=None):
    """A string section on a chord from t0 to t1 (+release): three desks per note, spread in the field."""
    d = t1 - t0 + rel
    for i, m in enumerate(notes):
        for desk in range(3):
            v = string_voice(nt(m) * 2 ** ((desk - 1) * 6 / 1200), d, att, rel, seed=int(m * 7 + desk * 131 + t0 * 10), bright=bright)
            if swell is not None: v *= swell(tt(d))
            pan = -0.55 + 1.1 * (i + 0.33 * desk) / max(1, len(notes))
            add(v, t0, g / np.sqrt(len(notes)), pan)


def organ(m, t0, d, g, pan=0.0, att=0.5, rel=0.8):
    """A flue rank: diapason with octave and fifteenth, a breath of wind."""
    x = tt(d + rel); f = nt(m); s = np.zeros(len(x))
    for k, a in [(1, 1.0), (2, 0.55), (3, 0.22), (4, 0.25), (6, 0.08), (8, 0.06)]:
        s += a * np.sin(2 * np.pi * f * k * x * (1 + 0.0004 * k) + k)
    s += 0.01 * fft_band(rs.standard_normal(len(x)), 200, 2000)
    e = np.clip(x / att, 0, 1) ** 2 * np.clip((d + rel - x) / rel, 0, 1)
    add(s * e, t0, g, pan)


def harpsichord(m, at, g, pan=0.0, d=None):
    """A plucked 8' choir: two strings a hair apart, quill click, partials dying faster as they rise."""
    f = nt(m); d = d or min(3.2, 1.2 + 260 / f); x = tt(d); s = np.zeros(len(x))
    for st, det in ((0, 0.0), (1, 0.9)):
        ff = f * 2 ** (det / 1200)
        for k in range(1, min(40, int(9000 / ff)) + 1):
            a = abs(np.sin(np.pi * k * 0.12)) / k ** 0.75
            tau = d * 0.55 / (1 + 0.22 * k)
            s += a * np.sin(2 * np.pi * ff * k * np.sqrt(1 + 1.2e-4 * k * k) * x + rs.random() * 6) * np.exp(-x / tau)
    click = fft_band(rs.standard_normal(len(x)), 2500, 9000) * np.exp(-x / 0.004) * 0.25
    s = s / 2 + click
    s *= np.minimum(1, x / 0.0015)
    add(s, at, g, pan)


def timpani(m, at, g, pan=0.0):
    f = nt(m); x = tt(2.6)
    glide = 1 + 0.035 * np.exp(-x / 0.06)
    s = np.zeros(len(x))
    for ratio, a, dec in [(1, 1.0, 1.5), (1.504, 0.55, 0.9), (1.742, 0.35, 0.7), (2.0, 0.28, 0.55), (2.245, 0.16, 0.45), (2.494, 0.12, 0.35)]:
        s += a * np.sin(2 * np.pi * np.cumsum(f * ratio * glide) / SR + rs.random() * 6) * np.exp(-x / dec)
    felt = fft_band(rs.standard_normal(len(x)), 30, 500) * np.exp(-x / 0.018)
    s = s + 0.6 * peak(felt) + 0.5 * np.sin(2 * np.pi * 44 * x) * np.exp(-x / 0.25)
    add(s * np.minimum(1, x / 0.002), at, g, pan)


def tink(f, at, g, pan=0.0, d=1.6):
    """A small gilt chime: inharmonic bell partials."""
    x = tt(d); s = np.zeros(len(x))
    for ratio, a, dec in [(1, 1, 0.9), (2.76, 0.45, 0.35), (5.4, 0.25, 0.15), (8.93, 0.12, 0.08)]:
        s += a * np.sin(2 * np.pi * f * ratio * x + rs.random() * 6) * np.exp(-x / (dec * d / 1.6))
    add(s * np.minimum(1, x / 0.001), at, g, pan)


def knock(at, g, pan=0.0, f=420):
    """A wooden shutter knock: a damped pair of body modes over a click."""
    x = tt(0.25)
    s = np.sin(2 * np.pi * f * x) * np.exp(-x / 0.03) + 0.6 * np.sin(2 * np.pi * f * 2.3 * x) * np.exp(-x / 0.015)
    s += 0.4 * fft_band(rs.standard_normal(len(x)), 1000, 6000) * np.exp(-x / 0.003)
    add(s, at, g, pan)


# ── the beam stutters on ──
for e in every('flick'):
    knock(e['t'], 0.3 * e['v'], -0.6, f=380 + 120 * e['v'])
    air = fft_band(rs.standard_normal(int(0.4 * SR)), 150, 1400) * np.exp(-tt(0.4) / 0.09) * np.minimum(1, tt(0.4) / 0.01)
    add(air, e['t'], 0.2 * e['v'], -0.5)
beam = one('beam')
knock(beam['t'], 0.22, -0.6, f=520)
x = tt(2.2); sh = moving_band(rs.standard_normal(len(x)), 2500 + 3500 * np.clip(x / 0.5, 0, 1), 900 + 0 * x)
add(sh * np.clip(x / 0.3, 0, 1) * np.exp(-np.clip(x - 0.3, 0, None) / 0.5), beam['t'], 0.05, -0.35)

# the organ pedal: an open fifth on D, from the light coming on to the cadence
cad = one('cadence')['t']; title = one('title')['t']
organ(38, beam['t'], cad - beam['t'], 0.07, -0.15, att=1.0, rel=0.6)
organ(45, beam['t'] + 0.3, cad - beam['t'] - 0.3, 0.045, 0.2, att=1.2, rel=0.6)

# ── the curtain: a dip, a creaking haul, the swag arrives on a drum stroke, the tassels chime ──
lift = one('lift'); a0, a1 = lift['t'], lift['t'] + lift['d']
lc = np.array(lift['curve'])                                            # curtain height, every 1/100 s from a0
lp = np.interp(t, a0 + np.arange(len(lc)) / 100, lc, left=0, right=lc[-1])
speed = np.abs(np.gradient(lp) * SR)                                    # how fast it is being hauled
sp = speed / speed.max()
velvet = moving_band(rs.standard_normal(N), 250 + 900 * sp, 260 + 500 * sp) * sp ** 1.2
add(velvet, 0, 0.5, 0.25)
# rope through the pulley: stick-slip pulses whose rate follows the haul
creak = np.zeros(N); tc = a0 - 0.05; rr = np.random.default_rng(7)
while tc < a1 + 1.4:
    i = int(tc * SR); v = sp[i] + (0.25 if tc < a1 + 0.05 else 0)
    if v > 0.05:
        x = tt(0.05)
        pulse = (np.sin(2 * np.pi * 310 * x) + 0.5 * np.sin(2 * np.pi * 870 * x) + 0.25 * np.sin(2 * np.pi * 1630 * x)) * np.exp(-x / 0.008)
        n = min(len(pulse), N - i); creak[i:i + n] += pulse[:n] * (0.4 + 0.6 * rr.random()) * min(1, v)
    tc += 1 / (16 + 55 * v) * (0.7 + 0.6 * rr.random())
add(creak, 0, 0.09, 0.55)
arrive = one('arrive')['t']; settle = one('settle')['t']; reveal = one('reveal')['t']
timpani(38, arrive, 0.34, 0.1)
for k, (f, dt, p) in enumerate([(1568, 0.0, 0.5), (2093, 0.07, 0.75), (1760, 0.16, 0.3), (2349, 0.26, 0.85), (1976, 0.4, 0.6)]):
    tink(f, settle - 0.1 + dt, 0.035 * (1 - 0.12 * k), p, d=0.9)

# ── the still life: strings and harpsichord continuo walk i–iv–VI–V while the light turns ──
turn = one('turn'); silk = one('silk'); throw = silk['throw']
t_iv, t_VI, t_V = turn['t'], turn['t'] + turn['d'] * 0.5, turn['t'] + turn['d'] * 0.88
chords = [((50, 53, 57, 62), reveal - 0.1, t_iv), ((50, 55, 58, 62), t_iv, t_VI), ((46, 53, 58, 62), t_VI, t_V), ((45, 52, 57, 61), t_V, throw)]
for k, (ch, c0, c1) in enumerate(chords):
    strings(ch, c0, c1 + 0.15, 0.05 + 0.006 * k, att=0.6 if k == 0 else 0.35, rel=0.45)
    for j, m in enumerate(sorted(ch)):
        harpsichord(m - 12 if j == 0 else m, c0 + 0.02 + 0.035 * j, 0.06, -0.3 + 0.2 * j)
    # a passing figure in the continuo halfway through each chord
    mid = (c0 + c1) / 2
    for j, m in enumerate([ch[3] + 12, ch[2] + 12, ch[1] + 12]):
        harpsichord(m, mid + 0.12 * j, 0.03, 0.35)
# sand in the hourglass while the light is on it
x = tt(2.4); grains = (rs.random(len(x)) < 0.012) * rs.standard_normal(len(x))
sand = fft_band(grains, 3000, 11000) * np.clip(x / 0.6, 0, 1) * np.clip((2.4 - x) / 0.8, 0, 1)
add(sand, reveal + 0.3, 0.18, -0.7)

# ── the silk: a flutter at the corner, a breath in, the throw across the field over a string run ──
path = np.array(silk['path'], dtype=float)
pt, px, pv, pc = path[:, 0], path[:, 1], path[:, 3], path[:, 4]
on = np.interp(t, pt, np.minimum(1, pc / 120), left=0, right=0)
vel = np.interp(t, pt, np.minimum(1.2, pv / 2600), left=0, right=0)
pan = np.interp(t, pt, 2 * px - 1, left=-1, right=1)
flutter = 1 + 0.45 * np.sin(2 * np.pi * 13 * t + 2 * np.sin(2 * np.pi * 3.1 * t)) * np.clip(1 - vel, 0.2, 1)
whoosh = moving_band(rs.standard_normal(N), 380 + 2300 * vel, 300 + 1500 * vel) * (0.12 + vel) ** 1.3 * on * flutter
add(whoosh, 0, 0.5, pan)
silky = moving_band(rs.standard_normal(N), 5200 + 2500 * vel, 1800 + 0 * vel) * vel ** 1.5 * on
add(silky, 0, 0.12, pan)
# the breath in before the throw: a reversed swell
x = tt(throw - silk['t'] - 0.15)
inhale = moving_band(rs.standard_normal(len(x)), 600 + 1800 * (x / x[-1]) ** 2, 500 + 0 * x) * (x / x[-1]) ** 3
add(inhale, silk['t'] + 0.15, 0.25, -0.6)
# a tirata: the strings rush up the D harmonic minor scale from A to the A two octaves above
scale = [57, 58, 61, 62, 64, 65, 67, 69, 70, 73, 74, 76, 77, 79, 81]
run_d = title - throw - 0.05
for j, m in enumerate(scale):
    at = throw + run_d * (j / len(scale)) ** 1.15
    v = string_voice(nt(m), 0.22, 0.012, 0.12, seed=900 + j, bright=1.3)
    add(v, at, 0.045 + 0.003 * j, -0.6 + 1.2 * j / len(scale))
strings((45, 52, 55, 61, 64), throw, title, 0.07, att=0.25, rel=0.3, bright=1.2, swell=lambda x: 0.6 + 0.4 * np.clip(x / 0.6, 0, 1))

# ── the title: a harpsichord flourish over a drum stroke and the strings on D minor; the gilding glints ──
timpani(38, title, 0.3, 0.0)
timpani(33, title + 0.02, 0.1, -0.2)
for j, m in enumerate([62, 65, 69, 74, 77, 81, 86, 81, 86]):
    harpsichord(m, title + 0.055 * j, 0.075 if j < 7 else 0.05, -0.4 + 0.1 * j)
t_iv6, t_V7 = cad - 0.75, cad - 0.35
strings((50, 57, 62, 65, 69), title, t_iv6, 0.075, att=0.08, rel=0.35, bright=1.15)
strings((46, 55, 62, 67), t_iv6, t_V7, 0.06, att=0.1, rel=0.25)
strings((45, 55, 61, 64, 67), t_V7, cad, 0.065, att=0.08, rel=0.2)
for c0, ch in [(t_iv6, (43, 58, 62, 67)), (t_V7, (33, 57, 61, 64, 67))]:
    for j, m in enumerate(ch):
        harpsichord(m, c0 + 0.03 * j, 0.05, -0.2 + 0.1 * j)
glint = one('glint')
for k, (f, p) in enumerate([(1175, -0.5), (1760, -0.25), (1397, 0.0), (2349, 0.2), (1760, 0.4), (2794, 0.6)]):
    tink(f, glint['t'] + 0.1 + 0.29 * k + 0.05 * rs.random(), 0.022, p, d=1.4)

# ── the iris: a roll into the cadence on D major, dying with the fade ──
out = one('out'); o0, o1 = out['t'], out['t'] + out['d']
for k in range(12):
    timpani(33, t_V7 + k * (cad - t_V7) / 12, 0.018 + 0.006 * k, -0.1)
timpani(38, cad, 0.26, 0.05)
fade = np.clip((DUR - 0.02 - t) / (DUR - 0.02 - o0), 0, 1) ** 1.6     # the room falls quiet with the picture
cadd = DUR - cad
for j, m in enumerate((38, 50, 57, 62, 66, 69, 74)):
    harpsichord(m, cad + 0.045 * j, 0.06, -0.3 + 0.1 * j, d=cadd)
strings((50, 57, 62, 66, 69, 74), cad, DUR - 0.3, 0.085, att=0.12, rel=0.3, bright=1.1,
        swell=lambda x: np.clip(1 - x / (DUR - cad) * 0.25, 0, 1))
organ(38, cad, DUR - cad - 0.4, 0.06, -0.1, att=0.05, rel=0.4)
organ(50, cad, DUR - cad - 0.4, 0.04, 0.15, att=0.1, rel=0.4)
organ(57, cad, DUR - cad - 0.4, 0.03, 0.3, att=0.1, rel=0.4)
organ(66, cad, DUR - cad - 0.4, 0.022, -0.3, att=0.15, rel=0.4)

# ── the room: a stone-hall reverb (decorrelated noise tails, highs dying first) ──
ir_n = int(2.6 * SR); xi = np.arange(ir_n) / SR
wet = []
for ch, src in enumerate((L, R)):
    r = np.random.default_rng(50 + ch)
    lo = fft_band(r.standard_normal(ir_n), 20, 1500) * np.exp(-xi / 0.42)
    hi = fft_band(r.standard_normal(ir_n), 1500, 12000) * np.exp(-xi / 0.2)
    ir = (lo + 0.6 * hi) * np.clip((xi - 0.018) / 0.01, 0, 1)
    ir /= np.sqrt((ir ** 2).sum())
    M = 1 << int(np.ceil(np.log2(N + ir_n)))
    wet.append(np.fft.irfft(np.fft.rfft(src, M) * np.fft.rfft(ir, M), M)[:N])
L = L + 0.32 * wet[0]; R = R + 0.32 * wet[1]

# ── master: the fade, no rumble or DC, peak at -1 dBFS ──
L *= np.where(t > o0, fade, 1); R *= np.where(t > o0, fade, 1)
L = fft_band(L, 28, 20000); R = fft_band(R, 28, 20000)
edge = np.clip(t / 0.01, 0, 1) * np.clip((DUR - t) / 0.05, 0, 1)
L *= edge; R *= edge
L -= L.mean(); R -= R.mean()
g = 10 ** (-1 / 20) / max(np.abs(L).max(), np.abs(R).max())
st = (np.stack([L, R], 1) * g * 32767).round().astype(np.int16)
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
