# events.json → audio.wav (48 kHz stereo, 10 s)
# bristle swishes as strokes land, night wind + faint crickets, a soft nocturne pad, celesta-like star bells,
# warm lamp tinks, a low swell under the camera push, one long brush drag for the title, closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(1889)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def bristle(d, lo=700, hi=4200):
    # loaded brush dragged across canvas: band noise with a rough, fluttering amplitude
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), lo, hi))
    am = np.abs(band(rs.standard_normal(len(t)), 20, 90)); am = .55 + .45 * norm(am)
    env = np.minimum(1, t / (d * .18)) * (1 - t / d) ** 1.4
    return n * am * env
def bell(f, d=1.6):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (d * k)) for h, a, k in [(1, 1, .45), (2.76, .35, .18), (5.4, .12, .08)])
    return s * np.minimum(1, t / .004)
def tone(freq, d, att=0.4, rel=1.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in [(1, 1), (2, .25), (3, .08)])
    env = np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1); return s * env
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR
# bed: night wind (slow filtered noise) + crickets + a soft D-major nocturne pad that swells with the push
wind = norm(band(rs.standard_normal(N), 120, 900)) * (.6 + .4 * np.sin(2 * np.pi * .13 * t + 1)) * np.clip(t / 1.5, 0, 1)
L += wind * .03; R += np.roll(wind, 2400) * .03
for k in range(26):
    tc = 0.8 + k * 0.33 + rs.uniform(0, .12); pan = rs.choice([-.7, .7])
    for j in range(3):
        d = .035; s = np.sin(2 * np.pi * 4300 * tt(d)) * np.sin(np.pi * tt(d) / d) ** 2
        add(s, tc + j * .06, .006, pan)
for m, g, p, a in [(50, .05, -.3, 2.0), (57, .035, .3, 2.4), (62, .03, 0, 2.8), (66, .022, -.2, 3.2), (69, .018, .2, 3.6)]:
    s = tone(nt(m), 9.2 - a * .3, a, 1.4) * (1 + .12 * np.sin(2 * np.pi * .21 * tt(9.2 - a * .3))); add(s, .3 + a * .3, g, p)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'brush': add(bristle(.16 + .1 * rs.random()), te + rs.uniform(0, .03), .05 + .13 * v, rs.uniform(-.5, .5))
    elif k == 'lamp': add(bell(1320 + rs.uniform(-30, 30), .35), te, .025 * v, rs.uniform(-.4, .2))
    elif k == 'star': add(bell(e['f'], 1.8), te, .05 * v, rs.uniform(-.6, .6))
    elif k == 'push':
        d = e['d']; x = norm(band(rs.standard_normal(int(d * SR)), 60, 500)); tl = tt(d)
        add(x * np.sin(np.pi * tl / d) ** 2, te, .06); add(tone(nt(38), d, d * .5, d * .4), te, .05)
    elif k == 'title': add(bristle(e['d'] + .2, 500, 3500), te, .16, -.3)
    elif k == 'sign': add(bristle(e['d'] + .1, 900, 5000), te, .1, .5)
    elif k == 'chord':
        for i, m in enumerate([62, 66, 69, 74, 78]): add(bell(nt(m), 2.2), te + i * .05, .03, -.4 + i * .2)
        add(tone(nt(38), 1.6, .1, 1.2), te, .05)
# master: fade in/out, soft limiter
fi = int(0.3 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
