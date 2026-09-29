# events.json → audio.wav (48 kHz stereo, 10 s)
# leather-and-gesso creaks as the screenfold opens and shuts, soft taps for the footprints, two-tone
# slit-drum knocks for the date cartouches, a seed-rattle swell for the sunrise, wing whooshes, soft paw
# thuds, a clay-flute (ocarina-like) line on a pentatonic scale with a two-voice greeting at the
# crossing, brush swishes for the caption and a low frame-drum thump when the codex closes.
# Everything is synthesized; nothing is sampled.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(104)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(max(1, int(d * SR))) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def creak(d):      # stiff hide bending: slow stick-slip grains + low body
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 300, 3500))
    rate = 18 + 30 * t / d; ph = 2 * np.pi * np.cumsum(rate) / SR
    am = np.abs(np.sin(ph)) ** 6
    body = np.sin(2 * np.pi * (140 + 40 * t / d) * t) * am
    return (0.8 * n * am + 0.3 * body) * np.sin(np.pi * t / d) ** 0.7
def slap(v=1.0):
    t = tt(0.3); n = norm(band(rs.standard_normal(len(t)), 200, 3500)) * np.exp(-t / 0.025)
    return 0.8 * n + 0.8 * v * np.sin(2 * np.pi * 85 * t) * np.exp(-t / 0.05)
def tap(v=0):
    t = tt(0.08); f = 700 if v else 820
    return norm(band(rs.standard_normal(len(t)), 500, 3000)) * np.exp(-t / 0.008) + 0.6 * np.sin(2 * np.pi * f * t) * np.exp(-t / 0.012)
def knock(f):      # slit drum tongue
    t = tt(0.6); s = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / dcy) for m, a, dcy in [(1, 1, .16), (2.7, .35, .05), (5.1, .12, .02)])
    return s + 0.25 * norm(band(rs.standard_normal(len(t)), 1200, 5000)) * np.exp(-t / 0.004)
def rattle(d, grow=True):   # seed rattle: dense tiny clicks, swelling
    t = tt(d); out = np.zeros(len(t)); n = int(d * 260)
    for _ in range(n):
        i = rs.integers(0, len(t) - 600); c = norm(band(rs.standard_normal(600), 3000, 11000)) * np.exp(-np.arange(600) / 60)
        out[i:i + 600] += c * rs.random()
    env = (t / d) ** 1.5 if grow else np.sin(np.pi * t / d)
    return out * env * np.minimum(1, (d - t) / 0.08)
def flute(f, d, vib=5.0, breath=0.18):   # clay flute: near-sine + breath, soft attack, vibrato
    t = tt(d); fm = f * (1 + 0.006 * np.sin(2 * np.pi * vib * t) * np.clip(t / 0.25, 0, 1))
    ph = 2 * np.pi * np.cumsum(fm) / SR
    tone = np.sin(ph) + 0.12 * np.sin(2 * ph) + 0.05 * np.sin(3 * ph)
    b = norm(band(rs.standard_normal(len(t)), f * 0.8, f * 3)) * breath
    env = np.minimum(1, t / 0.06) * np.minimum(1, (d - t) / 0.15)
    return (tone + b) * env
def whoosh(d, lo=200, hi=1800):
    t = tt(d); return norm(band(rs.standard_normal(len(t)), lo, hi)) * np.sin(np.pi * t / d) ** 2
def thud(v=1.0):
    t = tt(0.25); return (np.sin(2 * np.pi * (70 + 40 * np.exp(-t / 0.02)) * t) * np.exp(-t / 0.06) + 0.3 * norm(band(rs.standard_normal(len(t)), 100, 800)) * np.exp(-t / 0.02)) * v
def drum(f=62):
    t = tt(1.2); fm = f * (1 + 0.4 * np.exp(-t / 0.03)); ph = 2 * np.pi * np.cumsum(fm) / SR
    return np.sin(ph) * np.exp(-t / 0.35) + 0.25 * norm(band(rs.standard_normal(len(t)), 80, 1200)) * np.exp(-t / 0.03)
def brush(d):
    t = tt(d); return norm(band(rs.standard_normal(len(t)), 1500, 7000)) * np.sin(np.pi * t / d) ** 1.2 * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t) ** 2)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
# bed: soft room air + a very quiet low hum
t = np.arange(N) / SR
room = norm(band(rs.standard_normal(N), 120, 1800)); L += room * .004; R += np.roll(room, 777) * .004
hum = (np.sin(2 * np.pi * nt(45) * t) + .4 * np.sin(2 * np.pi * nt(52) * t)) * np.clip(t / 2, 0, 1) * np.clip((9.8 - t) / 1.2, 0, 1)
L += hum * .012; R += hum * .012
# clay-flute line (A minor pentatonic)
for tm, m, d, g in [(0.45, 69, 0.9, .07), (1.4, 72, 0.5, .06), (1.95, 74, 0.8, .06), (2.9, 76, 0.5, .05), (3.45, 74, 0.5, .05), (3.95, 79, 1.2, .07),
                    (5.3, 81, 0.6, .06), (5.95, 79, 0.4, .05), (7.35, 76, 0.5, .06), (7.9, 74, 0.5, .05), (8.45, 72, 0.6, .05), (9.05, 69, 0.9, .06)]:
    add(flute(nt(m), d), tm, g, rs.uniform(-.3, .3))
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'unfold': add(creak(e['d']), te, 0.14, .2); add(slap(0.7), te + e['d'] - 0.05, 0.18, .1)
    elif k == 'fold': add(creak(e['d']), te, 0.12, -.1); add(slap(0.5), te + e['d'] - 0.05, 0.12)
    elif k == 'close': add(drum(58), te, 0.35); add(slap(1.0), te, 0.18)
    elif k == 'step': add(tap(e['v']), te, 0.10, -.25 if e['v'] else .25)
    elif k == 'sign': add(knock(330), te, 0.16, -.2); add(knock(247), te + 0.16, 0.14, .2)
    elif k == 'sun': add(rattle(e['d']), te, 0.10, .3)
    elif k == 'rays': add(rattle(0.5, False), te, 0.12, .35); add(knock(440), te + 0.05, 0.08, .3)
    elif k == 'flap': add(whoosh(0.3, 250, 1600), te, 0.10, .1)
    elif k == 'pad': add(thud(0.8), te, 0.10, -.2)
    elif k == 'greet':
        for i, (m, d) in enumerate([(62, 0.22), (64, 0.22), (67, 0.45)]): add(flute(nt(m), d, 4), te + i * 0.2, 0.08, -.35)
    elif k == 'greet2':
        for i, (m, d) in enumerate([(79, 0.12), (81, 0.12), (79, 0.12), (84, 0.4)]): add(flute(nt(m), d, 7, 0.25), te + 0.3 + i * 0.1, 0.06, .35)
    elif k == 'brush': add(brush(e['d']), te, 0.05, .1)
    elif k == 'land': add(whoosh(0.4, 300, 2500), te - 0.25, 0.12); add(tap(1), te, 0.12)
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 3.0) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
