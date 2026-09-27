# events.json → audio.wav (48 kHz stereo, 10 s)
# CRT thunk + degauss, terminal chirps, rubber-button clacks, Geiger-counter clicks, radio static + a crackly
# 1950s jingle ("Happy Days in the Bunker", synthesized: vibes, clarinet, pizzicato bass, brushes) that is cut dead
# by the white flash → tinnitus ring → the same tune in full filmstrip fidelity (boing, stamp slams, wink ding,
# card flick, brass ta-daa) → it shrinks back into the wrist speaker → power-down zap.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(114)
EV = json.load(open('events.json'))
first = lambda k: next(e for e in EV if e['k'] == k)
T_ON, T_FLASH, T_OFF = first('on')['t'], first('flash')['t'], first('off')['t']
MUS = first('music'); T_ZOOM = MUS['z']

def add(sig, t, g=1.0, pan=0.0):
    i = int(round(t * SR)); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def norm(x): return x / (np.abs(x).max() + 1e-9)
def tt(d): return np.arange(int(d * SR)) / SR
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def sweep(f0, f1, d, shape=1.0):
    t = tt(d); f = f0 + (f1 - f0) * (t / d) ** shape; return np.sin(2 * np.pi * np.cumsum(f) / SR)

# ── one-shots ──
def click(bright=1.0):
    t = tt(0.03); n = band(rs.standard_normal(len(t)), 1500, 9000) * np.exp(-t / 0.002)
    return norm(n) * bright + 0.4 * np.sin(2 * np.pi * 900 * t) * np.exp(-t / 0.004)
def geiger():
    t = tt(0.012); n = rs.standard_normal(len(t)) * np.exp(-t / 0.0006)
    return norm(band(n, 1800, 12000)) + 0.3 * np.sin(2 * np.pi * 3100 * t) * np.exp(-t / 0.0015)
def clack():
    t = tt(0.09); n = band(rs.standard_normal(len(t)), 600, 4500) * np.exp(-t / 0.008)
    return 0.8 * norm(n) + 0.6 * np.sin(2 * np.pi * 170 * t) * np.exp(-t / 0.02)
def beep(f, d, sq=True):
    t = tt(d); s = np.sign(np.sin(2 * np.pi * f * t)) if sq else np.sin(2 * np.pi * f * t)
    s = band(s, 200, 5000) if sq else s
    return s * np.minimum(1, t / 0.003) * np.minimum(1, (d - t) / 0.01)
def crt_on():
    t = tt(1.1)
    thunk = np.sin(2 * np.pi * (55 + 30 * np.exp(-t * 20)) * t) * np.exp(-t / 0.08)
    degauss = np.sin(2 * np.pi * 100 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 50 * t)) * np.exp(-t / 0.35)
    crackle = band(rs.standard_normal(len(t)), 2000, 9000) * np.exp(-t / 0.05)
    whine = sweep(4000, 7800, 1.1, 0.3) * np.minimum(1, t / 0.3) * np.exp(-t / 0.6) * 0.08
    return thunk * 0.9 + degauss * 0.5 + 0.35 * norm(crackle) + whine
def crt_off():
    t = tt(0.6)
    zap = sweep(1400, 60, 0.6, 0.35) * np.exp(-t / 0.18)
    thunk = np.sin(2 * np.pi * 50 * t) * np.exp(-t / 0.1)
    fizz = band(rs.standard_normal(len(t)), 3000, 9000) * np.exp(-t / 0.12)
    return 0.5 * zap + 0.6 * thunk + 0.15 * norm(fizz)
def whoosh(d, lo=200, hi=2600, rev=False):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    env = np.sin(np.pi * t / d) ** 1.5 if not rev else (t / d) ** 2 * np.minimum(1, (d - t) / 0.05)
    fc = lo + (hi - lo) * env; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * env
def boing():
    t = tt(0.55); f = 180 + 420 * (1 - np.exp(-t * 9)) + 60 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 3)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return s * np.exp(-t / 0.22) * np.minimum(1, t / 0.01)
def slam():
    t = tt(0.4); body = np.sin(2 * np.pi * (70 + 60 * np.exp(-t * 30)) * t) * np.exp(-t / 0.09)
    n = band(rs.standard_normal(len(t)), 150, 3000) * np.exp(-t / 0.03)
    wood = np.sin(2 * np.pi * 820 * t) * np.exp(-t / 0.03)
    return body + 0.5 * norm(n) + 0.25 * wood
def bell(f, d=1.4):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (0.5 / h ** 0.5)) for h, a in [(1, 1), (2.76, .45), (5.4, .2), (8.9, .08)])
    return s * np.minimum(1, t / 0.002)
def flick():
    t = tt(0.3); n = band(rs.standard_normal(len(t)), 800, 7000)
    am = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * (40 - 60 * t) * t)); return norm(n) * am * np.exp(-t / 0.08)
def pen(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 1500, 6000); am = 0.6 + 0.4 * np.sin(2 * np.pi * 13 * t)
    return norm(n) * am * np.sin(np.pi * t / d) ** 0.6
def brass(freqs, d):
    t = tt(d); s = np.zeros(len(t))
    for f in freqs:
        ph = 2 * np.pi * f * t + 0.15 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t / 0.3)
        s += sum(np.sin(h * ph) / h ** 0.9 for h in range(1, 9))
    s = band(s, 150, 4500)
    return norm(s) * np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.12) ** 1.5
def static(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 300, 6000)
    wh = sweep(3000, 900, d, 0.7) * 0.25 + sweep(1800, 2600, d) * 0.12
    return (norm(n) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 9 * t))) + wh) * np.minimum(1, (d - t) / 0.03)
def crackle(d, rate=30):
    out = np.zeros(int(d * SR)); k = int(rate * d)
    for p in rs.integers(0, len(out) - 200, k): out[p:p + 60] += rs.standard_normal(60) * np.exp(-np.arange(60) / 8) * rs.uniform(0.2, 1)
    return out

# ── "Happy Days in the Bunker" (150 bpm) ──
BEAT = 0.4
MEL = [(0, 76, .5), (.5, 79, .5), (1, 84, 1), (2, 81, .5), (2.5, 79, .5), (3, 76, 1), (4, 77, .5), (4.5, 81, .5), (5, 79, .5), (5.5, 76, .5),
       (6, 74, 1), (7, 67, 1), (8, 76, .5), (8.5, 79, .5), (9, 84, 1), (10, 86, .5), (10.5, 84, .5), (11, 81, 1), (12, 79, .5), (12.5, 76, .5), (13, 74, .5), (13.5, 76, .5), (14, 72, 2)]
CH = [48, 45, 41, 43, 48, 41, 43, 48]  # C Am F G C F G C (2 beats each)
def vib(f, d):
    t = tt(d + 0.6); s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / 0.08)
    return s * np.exp(-t / 0.7) * (1 + 0.25 * np.sin(2 * np.pi * 6 * t)) * np.minimum(1, t / 0.003)
def clar(f, d):
    t = tt(d); s = sum(np.sin(2 * np.pi * f * h * t) / h for h in (1, 3, 5, 7))
    return s * np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.05)
def pizz(f):
    t = tt(0.5); return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(4 * np.pi * f * t)) * np.exp(-t / 0.16) * np.minimum(1, t / 0.004)
def brush():
    t = tt(0.12); return norm(band(rs.standard_normal(len(t)), 2000, 9000)) * np.exp(-t / 0.035)
def tune(d, beats=16):
    buf = np.zeros(int((d + 1) * SR))
    def put(sig, tb, g):
        i = int(tb * BEAT * SR); n = min(len(sig), len(buf) - i)
        if n > 0: buf[i:i + n] += sig[:n] * g
    for b, m, du in MEL:
        if b * BEAT < d: put(vib(nt(m), du * BEAT), b, 0.30); put(clar(nt(m - 12), du * BEAT * 0.9), b, 0.10)
    for i, root in enumerate(CH):
        third = 3 if root == 45 else 4
        for k in range(4):  # pizzicato bass: root / fifth
            b = i * 2 + k * 0.5
            if b * BEAT < d: put(pizz(nt(root + (7 if k % 2 else 0))), b, 0.30 if k % 2 == 0 else 0.18)
        for k in range(2):  # vibes comp on the off-beats
            b = i * 2 + k + 0.5
            if b * BEAT < d:
                for iv in (12, 12 + third, 19): put(vib(nt(root + iv), 0.15) * 0.5, b, 0.06)
    for b in np.arange(0, beats, 0.5):
        if b * BEAT < d: put(brush(), b, 0.08 if b % 1 else (0.14 if b % 2 == 1 else 0.05))
    return buf[:int(d * SR)]
def radioize(x, amt=1.0):
    y = band(x, 380, 2900); y = np.tanh(y * 2.2) / 1.2
    return (1 - amt) * x + amt * y

# ── beds ──
t = np.arange(N) / SR
hum = (np.sin(2 * np.pi * 60 * t) + .5 * np.sin(2 * np.pi * 120 * t) + .2 * np.sin(2 * np.pi * 180 * t))
hum_env = np.clip((t - T_ON) / 0.3, 0, 1) * (t < T_FLASH) + np.clip((t - T_ZOOM) / 0.4, 0, 1) * (t > T_ZOOM) * np.clip((T_OFF + 0.2 - t) / 0.2, 0, 1)
L += hum * 0.012 * hum_env; R += hum * 0.012 * hum_env
room = band(rs.standard_normal(N), 150, 2500); room = norm(room); L += room * .004; R += np.roll(room, 911) * .004
# filmstrip projector clatter (poster section): 24 Hz shutter ticks + crackle
pst = MUS['t']; pd = T_ZOOM + 0.4 - pst
proj = np.zeros(int(pd * SR)); tick = band(rs.standard_normal(200), 1200, 6000) * np.exp(-np.arange(200) / 30)
for k in range(int(pd * 24)): i = int(k / 24 * SR); proj[i:i + 200] += tick[:len(proj[i:i + 200])] * (0.6 + 0.4 * (k % 2))
proj = proj * np.minimum(1, np.arange(len(proj)) / SR / 0.2) * np.clip((len(proj) / SR - np.arange(len(proj)) / SR) / 0.4, 0, 1)
add(proj, pst, 0.05, -0.2); add(crackle(pd, 18), pst, 0.08, 0.2)

for e in EV:
    k, te = e['k'], e['t']
    if k == 'geiger': add(geiger(), te, 0.22 * rs.uniform(0.6, 1.0), rs.uniform(0.3, 0.6))
    elif k == 'toggle': add(click(), te, 0.25, 0.5); add(click(0.6), te + 0.018, 0.15, 0.5)
    elif k == 'on': add(crt_on(), te, 0.42)
    elif k == 'chirp': add(beep(1000 + 90 * e['v'], 0.04), te, 0.07)
    elif k == 'tab': add(clack(), te - 0.02, 0.35, -0.1); add(beep(880, 0.035), te + 0.02, 0.06)
    elif k == 'type':
        for j in range(int(e['d'] * 32)): add(click(0.5), te + j / 32 + rs.uniform(0, .006), 0.06)
    elif k == 'tick': add(click(), te, 0.12); add(beep(1500, 0.02, False), te, 0.05)
    elif k == 'error': add(beep(220, 0.1), te, 0.06); add(beep(180, 0.12), te + 0.12, 0.06)
    elif k == 'blip': s = np.sin(2 * np.pi * 1760 * tt(0.2)) * np.exp(-tt(0.2) / 0.05); add(s, te, 0.05, 0.2)
    elif k == 'knob':
        for j in range(9): add(click(0.4), te + j * e['d'] / 9, 0.08, 0.5)
    elif k == 'static': add(static(e['d']), te, 0.07, 0.3)
    elif k == 'jingle':
        d = e['d']; m = radioize(tune(d)); m = m + crackle(d, 60) * 0.25 + band(rs.standard_normal(len(m)), 1000, 5000) * 0.02
        m *= np.minimum(1, tt(d) / 0.04); add(m, te, 0.40, 0.3)  # hard cut at the flash
    elif k == 'flash':
        r = tt(1.6); ring = np.sin(2 * np.pi * 4186 * r) * np.exp(-r / 0.5) * np.minimum(1, r / 0.05)
        add(ring, te + 0.02, 0.035)
        sw = whoosh(0.3, 300, 5000, rev=True); add(sw, te - 0.3, 0.12)
    elif k == 'music':
        d = e['d']; m = tune(d); mr = radioize(m); u = np.clip((tt(d) + te - T_ZOOM) / 0.45, 0, 1)
        m = m * (1 - u) + mr * u * 0.9
        m *= np.minimum(1, tt(d) / 0.03) * np.clip((te + d - (tt(d) + te)) / 0.05, 0, 1)
        add(m, te, 0.42)
    elif k == 'pop': add(boing(), te, 0.25); add(whoosh(0.25, 400, 3000), te - 0.12, 0.08)
    elif k == 'slam': add(slam(), te, 0.5)
    elif k == 'swish': add(whoosh(0.28, 500, 4000), te, 0.12, 0.3)
    elif k == 'ding': add(bell(2637), te, 0.12, -0.2); add(bell(3951, 0.8), te + 0.06, 0.06, -0.2)
    elif k == 'pen': add(pen(e['d']), te, 0.08, 0.3)
    elif k == 'flip': add(flick(), te, 0.25, 0.4); add(whoosh(0.35, 400, 3500), te, 0.08, 0.4)
    elif k == 'fanfare':
        add(brass([nt(60), nt(64), nt(67)], 0.13), te - 0.14, 0.16, 0.2)
        add(brass([nt(60), nt(64), nt(67), nt(72)], 0.75), te, 0.2, 0.2); add(bell(2093, 1.0), te, 0.05, 0.2)
    elif k == 'whoosh': add(whoosh(e['d'], 300, 3000, rev=True), te, 0.12)
    elif k == 'off': add(crt_off(), te, 0.4)

# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.35 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.5) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
