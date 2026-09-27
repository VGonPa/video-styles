# events.json → audio.wav (48 kHz stereo, 10 s)
# newsroom sound design: paper slides, letterpress type clacks, highlighter squeak, felt-pen scratch,
# spinning-paper whoosh + flutter, page-landing thud, rubber-stamp thump, scissor snips, paper lift,
# low printing-press pulse + documentary pad bed, closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(27)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def nrm(x): return x / (np.abs(x).max() + 1e-9)
def lp(x, fc):
    a = np.exp(-2 * np.pi * np.broadcast_to(fc, x.shape) / SR); y = np.zeros_like(x); p = 0.0
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y
def clack():                                   # letterpress / linotype matrix drop
    t = tt(0.09); f0 = 900 + 500 * rs.random()
    click = nrm(band(rs.standard_normal(len(t)), 2200, 9000)) * np.exp(-t / 0.003)
    ring = (np.sin(2 * np.pi * f0 * t) + .5 * np.sin(2 * np.pi * f0 * 2.7 * t)) * np.exp(-t / 0.012)
    body = np.sin(2 * np.pi * (110 + 30 * rs.random()) * t) * np.exp(-t / 0.025)
    return 0.6 * click + 0.25 * ring + 0.55 * body
def rustle(d=0.45, lo=900, hi=7000):
    t = tt(d); n = nrm(band(rs.standard_normal(len(t)), lo, hi))
    am = np.abs(band(rs.standard_normal(len(t)), 4, 35)); am /= am.max() + 1e-9
    return n * am * np.sin(np.pi * t / d) ** 0.7
def slide(d):                                  # paper sliding / camera glide air
    t = tt(d); x = rs.standard_normal(len(t)); fc = 300 + 1600 * np.sin(np.pi * t / d) ** 2
    return nrm(lp(x, fc)) * np.sin(np.pi * t / d) ** 1.6
def marker(d):
    t = tt(d); n = nrm(band(rs.standard_normal(len(t)), 1400, 5200))
    squeak = np.sin(2 * np.pi * np.cumsum(2300 + 400 * np.sin(2 * np.pi * 6 * t)) / SR) * 0.18
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.5 * (0.75 + 0.25 * np.sin(2 * np.pi * 9 * t))
    return (n + squeak) * env
def pen(d):                                    # felt pen circling: scratchy, faster modulation
    t = tt(d); n = nrm(band(rs.standard_normal(len(t)), 2000, 8000))
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.4 * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 7 * t)))
    return n * env
def whoosh(d, peak=.5):
    t = tt(d); x = rs.standard_normal(len(t)); u = t / d
    env = np.where(u < peak, (u / peak) ** 2, ((1 - u) / (1 - peak)) ** 1.5)
    return nrm(lp(x, 250 + 3500 * env)) * env
def flutter(d):                                # paper flapping as it spins
    t = tt(d); u = t / d; rate = 22 - 14 * np.abs(u - .45) * 2
    ph = 2 * np.pi * np.cumsum(rate) / SR
    n = nrm(band(rs.standard_normal(len(t)), 600, 6000))
    return n * (0.5 + 0.5 * np.sin(ph)) ** 3 * np.sin(np.pi * u) ** .8
def thud(g=1.0):
    t = tt(0.5); f = 60 + 90 * np.exp(-t * 30); low = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.09)
    slap = nrm(band(rs.standard_normal(len(t)), 400, 6000)) * np.exp(-t / 0.02)
    return g * (low + 0.5 * slap)
def stamp():
    t = tt(0.6); f = 55 + 120 * np.exp(-t * 40); low = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.11)
    knock = nrm(band(rs.standard_normal(len(t)), 150, 2500)) * np.exp(-t / 0.018)
    rub = nrm(band(rs.standard_normal(len(t)), 300, 3000)) * np.exp(-((t - .03) / .04) ** 2) * .3
    return low * 1.1 + 0.6 * knock + rub
def snip():
    t = tt(0.12); a = nrm(band(rs.standard_normal(len(t)), 3000, 11000)) * np.exp(-t / 0.004)
    b = nrm(band(rs.standard_normal(len(t)), 1500, 6000)) * np.exp(-np.maximum(t - .035, 0) / .006) * (t > .035)
    ring = np.sin(2 * np.pi * 3100 * t) * np.exp(-t / .02) * .2
    return a * .7 + b * .8 + ring
def tone(freq, d, att=0.4, rel=1.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in [(1, 1), (2, .28), (3, .1), (4, .04)])
    env = np.minimum(1, t / att) * np.minimum(1, np.maximum(d - t, 0) / rel); return s * env
nt = lambda m: 440 * 2 ** ((m - 69) / 12)

t = np.arange(N) / SR
# bed: room tone, low press pulse (fades out for the second edition), D-minor documentary pad
room = nrm(band(rs.standard_normal(N), 150, 2500)); L += room * .006; R += np.roll(room, 911) * .006
press = np.zeros(N); beat = 60 / 112
for k in range(int(DUR / beat) + 1):
    tb = k * beat; i = int(tb * SR); tl = tt(0.25)
    hit = np.sin(2 * np.pi * (70 + 25 * np.exp(-tl * 40)) * tl) * np.exp(-tl / 0.06) + .25 * nrm(band(rs.standard_normal(len(tl)), 200, 1200)) * np.exp(-tl / .03)
    if k % 2: hit *= .55
    n = min(len(hit), N - i)
    if n > 0: press[i:i + n] += hit[:n]
penv = np.clip(t / 1.2, 0, 1) * (1 - 0.6 * np.clip((t - 4.2) / 1.0, 0, 1))
L += press * .05 * penv; R += press * .05 * penv
for m, g, p in [(38, .05, -.3), (45, .035, .3), (50, .025, 0), (53, .018, -.15)]:
    s = tone(nt(m), 9.7, 1.8, 1.4) * (1 + .12 * np.sin(2 * np.pi * .2 * tt(9.7))); add(s, 0.2, g, p)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'clack': add(clack(), te + rs.uniform(0, .006), 0.2 * v * (0.8 + .4 * rs.random()), rs.uniform(-.35, .35))
    elif k == 'glide': add(slide(e['d']), te, 0.07, rs.uniform(-.2, .2)); add(rustle(e['d'] * .8, 1200, 6000), te + .1, 0.03)
    elif k == 'marker': add(marker(e['d']), te, 0.07, .15)
    elif k == 'pen': add(pen(e['d']), te, 0.06, -.1)
    elif k == 'spin':
        d = e['d']; add(whoosh(d, .42), te, 0.3); add(flutter(d), te, 0.12, .2)
    elif k == 'thud': add(thud(v), te, 0.45); add(rustle(0.35), te + .01, 0.08)
    elif k == 'air': add(whoosh(0.14, .8), te, 0.12)
    elif k == 'stamp': add(stamp(), te, 0.6)
    elif k == 'snip': add(snip(), te, 0.16, rs.uniform(.1, .4))
    elif k == 'lift': add(rustle(0.6, 700, 6000), te, 0.12, .3); add(whoosh(0.5, .3), te, 0.05)
    elif k == 'chord':
        for i, m in enumerate([50, 57, 62, 65, 69]): add(tone(nt(m), 2.0, 0.1 + i * .05, 1.3), te + i * 0.06, 0.028)
        add(tone(nt(26), 2.0, .15, 1.4), te, 0.06)
# master: fade in/out, soft limiter
fi = int(0.3 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
