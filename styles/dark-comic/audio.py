# events.json → audio.wav (48 kHz stereo, 10 s)
# Rain on a city roof (hiss + patter), distant traffic rumble, a low minor drone, a close thunder
# crack with a rolling tail, the panel cracking and bursting into glass, soft paper thumps as the
# 9-panel grid inks in, typewriter keys and a bell for each caption, a slow swell for the push into
# the window and a last low muted piano-like note. All synthesized.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(60)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
t = np.arange(N) / SR
# rain bed: broadband hiss + random droplet patter, both channels decorrelated
hissL = norm(band(rs.standard_normal(N), 1500, 12000)); hissR = norm(band(rs.standard_normal(N), 1500, 12000))
pat = np.zeros(N); idx = rs.integers(0, N - 400, 5200)
for i in idx: pat[i] += rs.uniform(-1, 1)
pat = norm(band(pat, 2500, 11000))
env = np.clip(t / 0.5, 0, 1) * (1 - 0.35 * np.clip((t - 9.0) / 1.0, 0, 1))
L += (hissL * 0.030 + pat * 0.05) * env; R += (hissR * 0.030 + np.roll(pat, 1777) * 0.05) * env
# distant traffic / city rumble
rum = norm(band(rs.standard_normal(N), 30, 160)); L += rum * 0.05 * env; R += np.roll(rum, 3001) * 0.05 * env
# low drone: minor pad (D, F, A) slowly swelling
for f, g in [(73.4, 0.030), (87.3, 0.018), (110.0, 0.016), (146.8, 0.008)]:
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.13 * t + f)
    s = np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 0.5 * t)) * lfo * np.clip(t / 2.0, 0, 1)
    L += s * g; R += np.sin(2 * np.pi * f * 1.003 * t) * lfo * np.clip(t / 2.0, 0, 1) * g
def thunder(v):
    d = 3.2; x = tt(d); crack = norm(band(rs.standard_normal(len(x)), 800, 9000)) * np.exp(-x / 0.05)
    roll = norm(band(rs.standard_normal(len(x)), 25, 400)); am = np.abs(band(rs.standard_normal(len(x)), 1, 9)); am /= am.max() + 1e-9
    roll *= am * np.exp(-x / 1.1) * np.minimum(1, x / 0.08)
    return (crack * 0.7 + roll * 1.3) * v
def key():
    x = tt(0.06); c = norm(band(rs.standard_normal(len(x)), 1200, 7000)) * np.exp(-x / 0.006)
    thock = np.sin(2 * np.pi * 180 * x) * np.exp(-x / 0.012)
    return c * 0.8 + thock * 0.5
def ding():
    x = tt(1.2); return (np.sin(2 * np.pi * 2093 * x) + 0.4 * np.sin(2 * np.pi * 5230 * x) * np.exp(-x / 0.1)) * np.exp(-x / 0.35)
def crackle(d=0.3):
    x = tt(d); out = np.zeros(len(x))
    for i in range(24):
        j = int(rs.uniform(0, d * 0.9) * SR); k = tt(0.02); tick = norm(band(rs.standard_normal(len(k)), 3000, 14000)) * np.exp(-k / 0.002)
        out[j:j + len(k)] += tick[:len(out) - j] * rs.uniform(.4, 1)
    return out
def shatter():
    d = 1.4; x = tt(d); burst = norm(band(rs.standard_normal(len(x)), 1500, 14000)) * np.exp(-x / 0.08)
    body = norm(band(rs.standard_normal(len(x)), 80, 900)) * np.exp(-x / 0.06)
    tink = np.zeros(len(x))
    for i in range(46):
        f = rs.uniform(2500, 7500); s0 = rs.uniform(0.02, 1.0) ** 1.6; j = int(s0 * SR); k = tt(0.12)
        s = np.sin(2 * np.pi * f * k) * np.exp(-k / 0.025) * rs.uniform(.2, .7)
        tink[j:j + len(k)] += s[:len(tink) - j]
    return burst * 0.9 + body * 0.6 + tink * 0.6
def thump():
    x = tt(0.14); return np.sin(2 * np.pi * (90 * np.exp(-x * 12) + 50) * x) * np.exp(-x / 0.04) + 0.25 * norm(band(rs.standard_normal(len(x)), 400, 3000)) * np.exp(-x / 0.01)
def swell(d):
    x = tt(d); s = norm(band(rs.standard_normal(len(x)), 200, 1400)) * np.sin(np.pi * x / d) ** 2
    return s + 0.5 * np.sin(2 * np.pi * 55 * x) * np.sin(np.pi * x / d) ** 2
def note(f, d=2.4):
    x = tt(d); s = sum(np.sin(2 * np.pi * f * h * x) * np.exp(-x / (0.9 / h)) / h for h in (1, 2, 3, 4))
    return s * np.minimum(1, x / 0.004)
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'key': add(key(), te, 0.16, rs.uniform(-.25, .25))
    elif k == 'space': add(key(), te, 0.10, 0.1)
    elif k == 'ding': add(ding(), te, 0.05, 0.3)
    elif k == 'thunder': add(thunder(e['v']), te, 0.55, -0.2)
    elif k == 'crack': add(crackle(0.28), te, 0.30)
    elif k == 'shatter': add(shatter(), te, 0.45)
    elif k == 'thump': add(thump(), te, 0.10, rs.uniform(-.4, .4))
    elif k == 'push': add(swell(e['d']), te, 0.10)
    elif k == 'end':
        add(note(73.4), te, 0.16, -0.1); add(note(110.0), te + 0.12, 0.08, 0.1); add(note(174.6), te + 0.24, 0.05, 0.15)
fi = int(0.2 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.2) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
