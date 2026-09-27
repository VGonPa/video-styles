# events.json → audio.wav (48 kHz stereo, 10 s) · mid-90s PC foley:
# CRT degauss thunk + whine, startup chime, mouse clicks, keyboard clacks, hard-disk chatter, floppy stepper grind,
# error "ding" bells (a cascading storm), menu ticks, power-relay thunk, CRT power-off zap, soft closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(95)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def nrm(x): return x / (np.abs(x).max() + 1e-9)
def click(v=1.0):
    t = tt(0.03); n = nrm(band(rs.standard_normal(len(t)), 2000, 9000)) * np.exp(-t / 0.0015)
    return n + 0.4 * np.sin(2 * np.pi * 1400 * t) * np.exp(-t / 0.004)
def key(kind='key'):
    d = 0.09 if kind == 'key' else 0.14; t = tt(d)
    f0 = {'key': 190, 'space': 120, 'enter': 140}[kind] + 30 * rs.random()
    n = nrm(band(rs.standard_normal(len(t)), 1200, 6500)) * np.exp(-t / 0.005)
    body = np.sin(2 * np.pi * f0 * t) * np.exp(-t / 0.02)
    rel = np.zeros_like(t); j = int(0.045 * SR * (1.4 if kind != 'key' else 1)); m = min(len(t) - j, int(.01 * SR))
    if m > 0: rel[j:j + m] = nrm(band(rs.standard_normal(m), 2500, 8000)) * np.exp(-np.arange(m) / SR / 0.002) * 0.35
    return 0.6 * n + 0.55 * body + rel
def hdd(d):
    t = tt(d); s = np.zeros_like(t); k = 0.0
    while k < d - 0.02:
        i = int(k * SR); c = nrm(band(rs.standard_normal(int(.012 * SR)), 800, 5000)) * np.exp(-np.arange(int(.012 * SR)) / SR / .002)
        s[i:i + len(c)] += c[:len(s) - i] * (0.5 + 0.5 * rs.random()); k += 0.018 + 0.05 * rs.random()
    whirr = np.sin(2 * np.pi * 180 * t) * 0.08 * np.sin(np.pi * t / d)
    return s + whirr
def floppy(d):
    t = tt(d); s = np.zeros_like(t)
    # stepper motor: buzzy steps whose pitch hops around
    k = 0.0
    while k < d - 0.05:
        L_ = 0.06 + 0.12 * rs.random(); f = rs.choice([95, 120, 150, 190, 240]); i = int(k * SR); tl = tt(L_)
        ph = (f * tl) % 1.0; buzz = (np.where(ph < .3, 1.0, -.4)) * np.minimum(1, tl / .004) * np.minimum(1, (L_ - tl) / .01)
        s[i:i + len(tl)] += buzz[:len(s) - i] * 0.5; k += L_ + 0.03 * rs.random()
    grind = nrm(band(rs.standard_normal(len(t)), 300, 2500)) * (0.25 + 0.15 * np.sin(2 * np.pi * 5 * t))
    return (s + grind * 0.4) * np.minimum(1, t / .03) * np.minimum(1, (d - t) / .05)
def bell(f, d=0.7):
    t = tt(d); mod = np.sin(2 * np.pi * f * 1.41 * t) * 1.3 * np.exp(-t / 0.2)
    return np.sin(2 * np.pi * f * t + mod) * np.exp(-t / 0.22) * np.minimum(1, t / .002)
def ding(v, p):
    d = bell(880 * v, 0.7); d2 = bell(660 * v, 0.7)
    s = np.zeros(int(0.8 * SR)); s[:len(d)] += d; j = int(0.07 * SR); s[j:j + len(d2)] += d2[:len(s) - j] * 0.9
    return s
def tone(freq, d, att=0.4, rel=1.0, harm=((1, 1), (2, .3), (3, .1))):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in harm)
    env = np.minimum(1, t / att) * np.minimum(1, np.maximum(0, d - t) / rel); return s * env
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
ev = json.load(open('events.json'))
T_black = next(e['t'] for e in ev if e['k'] == 'thunk'); T_off = next(e['t'] for e in ev if e['k'] == 'crt_off')
# bed: PC fan + faint mains hum until the relay thunk; CRT hum until power-off
t = np.arange(N) / SR
fan = band(rs.standard_normal(N), 60, 900); fan = nrm(fan) * (1 + .1 * np.sin(2 * np.pi * 31 * t))
fenv = np.clip(t / 0.3, 0, 1) * np.clip((T_black + .25 - t) / .35, 0, 1)
L += fan * 0.035 * fenv; R += np.roll(fan, 911) * 0.035 * fenv
hum = (np.sin(2 * np.pi * 60 * t) + .35 * np.sin(2 * np.pi * 120 * t)) * np.clip(t / .2, 0, 1) * np.clip((T_off + .15 - t) / .2, 0, 1)
L += hum * 0.012; R += hum * 0.012
for e in ev:
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'click': add(click(), te, 0.2 * v, .15)
    elif k in ('key', 'space', 'enter'): add(key(k), te + rs.uniform(0, .006), 0.2 * v * (0.8 + .4 * rs.random()), rs.uniform(-.25, .25))
    elif k == 'hdd': add(hdd(e['d']), te, 0.12, -.2)
    elif k == 'floppy': add(floppy(e['d']), te, 0.16, -.3)
    elif k == 'ding': add(ding(v if v != 1 else 1.0, e.get('p', 0)), te, 0.16 if v == 1 else 0.11, max(-.7, min(.7, e.get('p', 0))))
    elif k == 'tick': add(click(), te, 0.07)
    elif k == 'crt_on':
        d = tt(0.9); thump = np.sin(2 * np.pi * (70 * np.exp(-d * 3) + 40) * d) * np.exp(-d / .18)
        buzz = np.sign(np.sin(2 * np.pi * 60 * d)) * np.exp(-d / .25) * 0.3
        whine = np.sin(2 * np.pi * (2000 + 5000 * np.minimum(1, d / .5)) * d) * 0.02 * np.exp(-d / .6)
        add(thump + buzz + whine + nrm(band(rs.standard_normal(len(d)), 500, 6000)) * np.exp(-d / .05) * .5, te + .02, 0.35)
    elif k == 'chime':
        for i, (m, dl) in enumerate([(63, 0), (70, .12), (75, .24), (79, .36), (82, .5)]):
            add(tone(nt(m), 1.9 - dl, 0.03, 1.1, ((1, 1), (2, .25), (4, .08))), te + dl, 0.05, (i - 2) * .2)
        add(tone(nt(39), 2.0, .2, 1.2), te, 0.07); add(tone(nt(51), 2.0, .3, 1.2), te + .1, 0.04)
    elif k == 'thunk':
        d = tt(0.4); add(np.sin(2 * np.pi * (90 * np.exp(-d * 8) + 45) * d) * np.exp(-d / .08) + nrm(band(rs.standard_normal(len(d)), 200, 3000)) * np.exp(-d / .02) * .4, te, 0.35)
    elif k == 'crt_off':
        d = tt(0.45); f = 6000 * np.exp(-d * 9) + 200; ph = 2 * np.pi * np.cumsum(f) / SR
        add(np.sin(ph) * np.exp(-d / .15) * .25 + nrm(band(rs.standard_normal(len(d)), 1000, 8000)) * np.exp(-d / .03) * .5, te, 0.22)
    elif k == 'end':
        for i, m in enumerate([60, 64, 67, 72]): add(tone(nt(m), 1.0, 0.05 + i * .03, 0.7), te + i * .05, 0.035, (i - 1.5) * .2)
        add(tone(nt(48), 1.0, .08, .8), te, 0.05)
# master: fades + soft limiter
fi = int(0.02 * SR); fo = int(0.35 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.5) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
