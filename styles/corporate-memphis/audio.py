# events.json → audio.wav (48 kHz stereo, 9.5 s)
# Upbeat "corporate ukulele" bed, all synthesised: a plucked nylon-string ukulele strumming the island pattern
# (C | G | Am | F | C, 120 bpm), a round sine bass, finger snaps on the backbeat in the first scene and claps in
# the second, a marimba-like plucked arpeggio once the laptop opens, then the cue sounds read from events.json:
# pops, boings on landings, a rubbery stretch, the pencil whoosh and skid, the puzzle click and chime, the bubble
# inflating, UI ticks, the high-five slap and sparkle, key clicks for the tagline and a final strummed chord.
import json, wave, numpy as np
SR, DUR = 48000, 9.5
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(142)
BEAT = 0.5


def add(sig, t, g=1.0, pan=0.0):
    i = int(round(t * SR)); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414
        R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414


def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def tt(d): return np.arange(int(d * SR)) / SR
def nt(m): return 440 * 2 ** ((m - 69) / 12)
def norm(x): return x / (np.abs(x).max() + 1e-9)
def noise(d, lo, hi): return norm(band(rs.standard_normal(int(d * SR)), lo, hi))


# ── instruments ──
def uke(m, dur=0.9, vel=1.0):
    """plucked nylon string: harmonics with faster decay up the series, pluck-position comb, finger noise"""
    f = nt(m); t = tt(dur); s = np.zeros(len(t))
    for k in range(1, 12):
        fk = f * k * (1 + 0.0007 * k * k)
        if fk > 12000: break
        s += np.sin(np.pi * k * 0.17) / k ** 1.05 * np.sin(2 * np.pi * fk * t + k * 0.7) * np.exp(-t * (2.6 + 1.9 * k))
    s += 0.18 * noise(dur, 1500, 6000) * np.exp(-t / 0.006)
    return s * np.minimum(1, t / 0.0015) * vel


def strum(notes, t0, down=True, vel=1.0, dur=0.8):
    seq = notes if down else notes[::-1]
    for i, m in enumerate(seq):
        add(uke(m, dur, vel * (1 if down else 0.7)), t0 + i * (0.011 if down else 0.008), 0.17, -0.25 + 0.17 * i)


def bass(m, dur):
    f = nt(m); t = tt(dur + 0.15)
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t) + 0.08 * np.sin(6 * np.pi * f * t)
    env = np.minimum(1, t / 0.008) * np.exp(-t * 2.2) * np.where(t > dur, np.exp(-(t - dur) * 30), 1)
    return s * env


def marimba(m, vel=1.0):
    f = nt(m); t = tt(0.6)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 7) + 0.35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 22)
    s += 0.12 * np.sin(2 * np.pi * f * 9.9 * t) * np.exp(-t * 50)
    return s * np.minimum(1, t / 0.002) * vel


def bell(m, d=1.4):
    f = nt(m); t = tt(d)
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2) + 0.5 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6)
         + 0.28 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 11) + 0.15 * np.sin(2 * np.pi * f * 8.9 * t) * np.exp(-t * 18))
    return s * np.minimum(1, t / 0.001)


def snap():
    t = tt(0.12)
    s = noise(0.12, 1800, 9000) * np.exp(-t / 0.007) + 0.5 * np.sin(2 * np.pi * 2100 * t) * np.exp(-t / 0.012)
    return s


def clap():
    t = tt(0.25); s = np.zeros(len(t)); nz = noise(0.25, 700, 5000)
    for k, dt in enumerate((0, 0.009, 0.019)):
        i = int(dt * SR); env = np.exp(-(t[: len(t) - i]) / (0.006 if k < 2 else 0.05))
        s[i:] += nz[: len(t) - i] * env * (0.7 if k < 2 else 1.0)
    return s


def kick():
    t = tt(0.3); f = 50 + 70 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 12)


# ── sound effects ──
def pop(m=76):
    t = tt(0.16); f = nt(m) * (1 + 1.6 * np.exp(-t * 60))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.035) + 0.3 * noise(0.16, 2000, 8000) * np.exp(-t / 0.002)


def boing(f0=170, d=0.7):
    t = tt(d); f = f0 * (1 + 0.5 * np.exp(-t * 9)) * (1 + 0.08 * np.sin(2 * np.pi * 11 * t) * np.exp(-t * 3))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)) * np.exp(-t / 0.18) * np.minimum(1, t / 0.004)


def whoosh(d, f0=500, f1=2500):
    t = tt(d); x = rs.standard_normal(len(t)); out = np.zeros(len(t)); n = 8
    for k in range(n):                                    # crude swept band: crossfade bands
        a, b = int(k * len(t) / n), int((k + 1) * len(t) / n)
        fc = f0 * (f1 / f0) ** ((k + .5) / n)
        out[a:b] = band(x, fc * 0.6, fc * 1.6)[a:b]
    return norm(out) * np.sin(np.pi * t / d) ** 2


def skid(d):
    t = tt(d); x = noise(d, 900, 3500) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 38 * t)))
    return x * np.sin(np.pi * t / d) ** 0.7


def thunk():
    t = tt(0.25)
    return np.sin(2 * np.pi * (70 + 60 * np.exp(-t * 25)) * t) * np.exp(-t / 0.06) + 0.25 * noise(0.25, 200, 1500) * np.exp(-t / 0.01)


def stretch(d):
    t = tt(d); u = t / d; f = 260 * (2.6 ** u) * (1 + 0.035 * np.sin(2 * np.pi * 7 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + 0.25 * np.sin(2 * ph)) * np.sin(np.pi * u) ** 1.5


def twang():
    t = tt(0.5); f = 140 * (1 + 0.6 * np.exp(-t * 18))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + 0.6 * np.sin(3 * ph) * np.exp(-t * 12)) * np.exp(-t / 0.12)


def click():
    t = tt(0.08)
    return noise(0.08, 3000, 10000) * np.exp(-t / 0.003) + 0.8 * np.sin(2 * np.pi * 900 * t) * np.exp(-t / 0.015)


def blip(m):
    t = tt(0.09); return np.sin(2 * np.pi * nt(m) * t) * np.exp(-t / 0.025) * np.minimum(1, t / 0.002)


def inflate(d):
    t = tt(d); u = t / d; f = 180 * (4.5 ** (u ** 1.4))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (0.6 * np.sin(ph) + 0.2 * np.sin(2 * ph)) * u ** 1.2 + 0.7 * whoosh(d, 300, 4000) * u


def key():
    t = tt(0.05)
    return noise(0.05, 2500, 9000) * np.exp(-t / 0.0025) + 0.4 * np.sin(2 * np.pi * 1700 * t) * np.exp(-t / 0.006)


# ── music: island strum (D . D U . U D U) over C | G | Am | F | C ──
CH = {'C': [67, 60, 64, 72], 'G': [67, 62, 67, 71], 'Am': [69, 60, 64, 69], 'F': [69, 60, 65, 69]}
ROOT = {'C': 36, 'G': 43, 'Am': 45, 'F': 41}
PROG = ['C', 'G', 'Am', 'F']
PAT = [(0, True), (2, True), (3, False), (5, False), (6, True), (7, False)]
END = 8.64                                               # the final chord lands as the tagline completes
for bar in range(5):
    ch = PROG[bar % 4] if bar < 4 else 'C'
    t0 = bar * 2.0
    for e8, down in PAT:
        te = t0 + e8 * 0.25
        if te >= END - 0.02 or te < 0.05: continue
        strum(CH[ch], te, down, 0.95 if e8 in (0, 6) else 0.8, 0.55 if not down else 0.75)
    for b in (0, 2):                                      # bass on beats 1 and 3, with an eighth pickup
        tb = t0 + b * BEAT
        if tb < END - 0.02: add(bass(ROOT[ch], 0.42), tb, 0.25, -0.05)
        if tb + 0.75 < END - 0.02 and b == 2: add(bass(ROOT[ch] + 7, 0.2), tb + 0.75, 0.16, -0.05)
    for b in range(4):
        tb = t0 + b * BEAT
        if tb >= END - 0.02: continue
        if b in (0, 2) and tb > 0.4: add(kick(), tb, 0.15)
        if b in (1, 3):
            if tb < 4.0: add(snap(), tb, 0.2, 0.35 if b == 1 else -0.35)
            else: add(clap(), tb, 0.24, 0.15 if b == 1 else -0.15)
# plucked arpeggio once the laptop is open (bars 3 and 4, last half of bar 5 left to the chord)
ARP = {'Am': [69, 72, 76, 79, 76, 72, 76, 81], 'F': [69, 72, 77, 81, 77, 72, 77, 84], 'C': [72, 76, 79, 84]}
for bar, ch in ((2, 'Am'), (3, 'F'), (4, 'C')):
    for i, m in enumerate(ARP[ch]):
        te = bar * 2.0 + i * 0.25 + (0.125 if i % 2 else 0)
        if 4.1 < te < END - 0.05: add(marimba(m, 0.8 + 0.2 * (i % 2 == 0)), te, 0.11, 0.3 if i % 2 else -0.2)

# ── cues ──
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'bloom': add(norm(band(rs.standard_normal(int(0.5 * SR)), 80, 700)) * np.sin(np.pi * tt(0.5) / 0.5) ** 2, te, 0.12)
    elif k == 'pop': add(pop(e.get('n', 76)), te, 0.24 * v, rs.uniform(-.3, .3))
    elif k == 'boing': add(boing(), te, 0.34 * v, -0.1)
    elif k == 'whoosh': add(whoosh(e['d'], 400, 2200), te, 0.09 * v, 0.4)
    elif k == 'skid': add(skid(e['d']), te, 0.07, 0.4)
    elif k == 'thunk': add(thunk(), te, 0.34, 0.3)
    elif k == 'stretch': add(stretch(e['d']), te, 0.09, 0.2)
    elif k == 'snap': add(snap(), te, 0.3, 0.2)
    elif k == 'twang': add(twang(), te, 0.22, 0.35)
    elif k == 'click': add(click(), te, 0.34, -0.2)
    elif k == 'chime':
        for i, d in enumerate((0, 4, 7)): add(bell(e['n'] + d, 1.2), te + i * 0.045, 0.085, -0.3 + 0.3 * i)
    elif k == 'clap': add(clap(), te, 0.3 * v, rs.uniform(-.3, .3))
    elif k == 'blip': add(blip(e['n']), te, 0.13, 0.3)
    elif k == 'inflate': add(inflate(e['d']), te, 0.16)
    elif k == 'tick': add(blip(e['n']), te, 0.13, 0.1); add(click(), te, 0.065, 0.1)
    elif k == 'spring': add(boing(230, 0.5), te - 0.02, 0.22, -0.3); add(stretch(0.3), te, 0.07, -0.3)
    elif k == 'five':
        add(clap(), te, 0.4, 0.1); add(noise(0.25, 300, 2500) * np.exp(-tt(0.25) / 0.01), te, 0.24, 0.1)
        for i, m in enumerate((84, 88, 91, 96)): add(bell(m, 1.0), te + 0.02 + i * 0.05, 0.08, -0.3 + 0.2 * i)
    elif k == 'key': add(key(), te, 0.12 * v, rs.uniform(-.2, .2))
    elif k == 'chord':
        strum([60, 64, 67, 72], te, True, 1.0, 1.6); strum([67, 72, 76, 79], te + 0.05, True, 0.8, 1.6)
        add(bass(36, 1.2), te, 0.4); add(bell(84, 1.6), te + 0.06, 0.09, 0.2); add(bell(91, 1.6), te + 0.1, 0.06, -0.2)

# ── master: gentle bus compression, fades with the picture ──
st = np.stack([L, R], 1)
t = np.arange(N) / SR
fade = np.clip(t / 0.08, 0, 1) * np.where(t > 9.1, np.clip((9.5 - t) / 0.4, 0, 1) ** 1.5, 1)
st *= fade[:, None]
st = np.tanh(st * 1.25) * 0.88
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
