# events.json → audio.wav (48 kHz stereo, 10 s)
# print-shop sounds (drum swishes, registration clacks, roller passes with a mechanical ka-chunk, final lock thunk)
# over a small live-electronics bed (soft kick, off-beat hats, sub bass) and a closing pad as the ink fades.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(26)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def lp_sweep(d, f0, f1, curve):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = f0 + (f1 - f0) * curve(t / d); a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y)
def swish(d):
    t = tt(d); s = lp_sweep(d, 300, 4200, lambda u: np.sin(np.pi * np.clip(u * 1.1, 0, 1)) ** 2)
    return s * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.2
def clack():
    t = tt(0.22); click = norm(band(rs.standard_normal(len(t)), 1500, 8000)) * np.exp(-t / 0.004)
    wood = np.sin(2 * np.pi * 820 * t) * np.exp(-t / 0.018) + .6 * np.sin(2 * np.pi * 1330 * t) * np.exp(-t / 0.012)
    thump = np.sin(2 * np.pi * (120 * np.exp(-t * 20) + 70) * t) * np.exp(-t / 0.05)
    return 0.6 * click + 0.35 * wood + 0.7 * thump
def chunk():
    t = tt(0.16); n = norm(band(rs.standard_normal(len(t)), 200, 2500)) * np.exp(-t / 0.02)
    return n * .7 + np.sin(2 * np.pi * 95 * t) * np.exp(-t / 0.04)
def drum(d):                                        # roller pass: whirr + rhythmic ka-chunks
    t = tt(d + .25); whirr = norm(band(rs.standard_normal(len(t)), 400, 3000))
    am = 0.55 + 0.45 * np.sin(2 * np.pi * 26 * t) ** 2
    env = np.clip(t / 0.05, 0, 1) * np.clip((d + .25 - t) / 0.2, 0, 1)
    s = whirr * am * env * 0.5
    out = s.copy()
    for k in range(4):
        c = chunk(); i = int(k * d / 3.5 * SR); n = min(len(c), len(out) - i); out[i:i + n] += c[:n] * (0.8 if k == 0 else 0.5)
    return out
def kick():
    t = tt(0.4); f = 50 + 110 * np.exp(-t * 28); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.13) + 0.2 * norm(band(rs.standard_normal(len(t)), 2000, 6000)) * np.exp(-t / 0.003)
def hat():
    t = tt(0.07); return norm(band(rs.standard_normal(len(t)), 7000, 15000)) * np.exp(-t / 0.018)
def tone(freq, d, att=0.02, rel=0.3, harm=((1, 1), (2, .25), (3, .08))):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in harm)
    return s * np.minimum(1, t / att) * np.minimum(1, np.maximum(0, d - t) / rel)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
BASS = [38, 38, 41, 43]                             # D, D, F, G (per half bar)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'slide': add(swish(e['d']), te, 0.22 * v, rs.uniform(-.4, .4))
    elif k == 'clack': add(clack(), te, 0.42 * v, rs.uniform(-.2, .2))
    elif k == 'drift':
        d = e['d']; t = tt(d)
        wob = np.sin(2 * np.pi * np.cumsum(nt(62) * (1 - .25 * (t / d) ** 2)) / SR) * np.sin(np.pi * t / d)
        add(wob, te, 0.05, -.2); add(np.sin(2 * np.pi * np.cumsum(nt(69) * (1 - .3 * (t / d) ** 2)) / SR) * np.sin(np.pi * t / d), te + .03, 0.035, .3)
        add(swish(d), te, 0.12)
    elif k == 'drum': add(drum(e['d']), te, 0.28, rs.uniform(-.25, .25))
    elif k == 'lock':
        add(clack(), te, 0.6); add(kick(), te, 0.5)
        for i, m in enumerate([50, 57, 62, 65, 69]): add(tone(nt(m), 2.6, 0.01 + i * .02, 1.6, ((1, 1), (2, .4), (3, .15), (4, .06))), te + i * .03, 0.035, (i - 2) * .2)
    elif k == 'kick':
        add(kick(), te, 0.34 * v)
        add(hat(), te + .25, 0.07 * v, .35)
        bi = int(round(te * 2)) % 4
        add(tone(nt(BASS[bi]), .45, .01, .2, ((1, 1), (2, .5), (3, .2))), te, 0.07 * v)
    elif k == 'outro':
        for i, m in enumerate([50, 57, 62, 64, 69]): add(tone(nt(m), 1.3, .5, .9), te + i * .05, 0.022, (i - 2) * .2)
# faint print-shop room tone
room = norm(band(rs.standard_normal(N), 150, 2000)); L += room * .004; R += np.roll(room, 911) * .004
fi = int(0.2 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
