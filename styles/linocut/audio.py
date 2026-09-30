# events.json → audio.wav (48 kHz stereo, 10 s)
# print-press thumps with a small room, wood-carving creaks while the tree grows, hoof taps,
# wing flutters, sticky brayer roll, paper peel, graphite scratch, one low woody tone under "WILD".
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(11)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def thump(f):   # block pressed onto paper: pitched body + papery slap
    t = tt(0.4); fr = f * 1.9 * np.exp(-t * 30) + f * 0.55; body = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.07)
    slap = band(rs.standard_normal(len(t)), 400, 4500) * np.exp(-t / 0.018)
    return body + 0.35 * norm(slap)
def creak():    # gouge biting into lino: short resonant scrape
    t = tt(0.07); n = band(rs.standard_normal(len(t)), 900 + 600 * rs.random(), 3800) * np.sin(np.pi * t / 0.07) ** 2
    return norm(n) * (0.7 + 0.3 * np.sin(2 * np.pi * 180 * t))
def rustle(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 900, 7000); am = np.abs(band(rs.standard_normal(len(t)), 5, 40)); am /= am.max() + 1e-9
    return norm(n) * am * np.sin(np.pi * t / d) ** 0.7
def hoof():
    t = tt(0.08); return np.sin(2 * np.pi * (520 + 80 * rs.random()) * t) * np.exp(-t / 0.012) + 0.4 * norm(band(rs.standard_normal(len(t)), 2000, 6000)) * np.exp(-t / 0.004)
def flutter(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 300, 2500)); am = np.maximum(0, np.sin(2 * np.pi * (13 + 3 * rs.random()) * t)) ** 3
    return n * am * np.exp(-t / (d * 0.5))
def roll(d):    # brayer: low rumble + tacky ink crackle
    t = tt(d); rum = norm(band(rs.standard_normal(len(t)), 40, 260)); tack = norm(band(rs.standard_normal(len(t)), 2500, 9000)) * (rs.random(len(t)) < 0.02)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.6; return (rum + 0.5 * tack) * env
def peel(d):    # sheet pulled from the inked block: sticky crackle rising, then paper swish
    t = tt(d); crk = band(rs.standard_normal(len(t)), 1500, 8000) * (rs.random(len(t)) < 0.05 + 0.2 * t / d)
    return 0.8 * norm(crk) * np.sin(np.pi * t / d) + 0.6 * rustle(d)
def pencil(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 2500, 9000)); am = 0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 6 * t))
    return n * am * np.sin(np.pi * t / d) ** 0.5
def tone(f, d):   # woody marimba-like note
    t = tt(d); return sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (0.9 / h)) for h, a in [(1, 1), (3.9, .25), (9.2, .06)]) * np.minimum(1, t / 0.004)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'thump': add(thump(e['f']), te, 0.55 * v, rs.uniform(-.15, .15))
    elif k == 'creak': add(creak(), te + rs.uniform(0, .01), 0.10 * v, rs.uniform(-.2, .2))
    elif k == 'rustle': add(rustle(e['d']), te, 0.10, .1)
    elif k == 'hoof': add(hoof(), te, 0.12, .45)
    elif k == 'flutter': add(flutter(e['d']), te, 0.10, rs.uniform(-.4, .4))
    elif k == 'roll': add(roll(e['d']), te, 0.35)
    elif k == 'peel': add(peel(e['d']), te, 0.25 * v, .2)
    elif k == 'pencil': add(pencil(e['d']), te, 0.05, -.4); add(pencil(e['d'] * .7), te + e['d'] * .3, 0.05, .5)
    elif k == 'tone': add(tone(110, 2.5), te, 0.18); add(tone(164.8, 2.3), te + .03, 0.08)
# small room (the old clip's echo) + quiet paper-room floor
dry = np.stack([L, R], 1); wet = dry.copy()
for dl, g in ((0.043, .18), (0.071, .12), (0.113, .07)): k = int(dl * SR); wet[k:] += dry[:-k] * g
room = band(rs.standard_normal(N), 150, 2500); wet[:, 0] += norm(room) * .004; wet[:, 1] += np.roll(norm(room), 999) * .004
fi = int(0.2 * SR); fo = int(0.65 * SR)
wet[:fi] *= np.linspace(0, 1, fi)[:, None]; wet[-fo:] *= (np.linspace(1, 0, fo) ** 1.5)[:, None]
st = np.tanh(wet * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
