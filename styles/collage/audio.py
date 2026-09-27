# events.json → audio.wav (48 kHz stereo, 10 s)
# paper slaps, masking-tape rips, stapler, paperclip, scissor snips, crayon + marker scribbles, a long paper tear,
# digital pixel blips (the only "clean" sounds), a kraft sheet sliding, over a soft plucked lo-fi loop and room tone.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(25)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
nz = lambda s: s / (np.abs(s).max() + 1e-9)
def slap(v=1.0):
    t = tt(0.3); n = band(rs.standard_normal(len(t)), 250, 6000) * np.exp(-t / 0.022)
    thud = np.sin(2 * np.pi * (70 + 40 * np.exp(-t * 30)) * t) * np.exp(-t / 0.045)
    return 0.8 * nz(n) + 0.7 * v * thud
def tape():
    d = 0.16; t = tt(d); n = band(rs.standard_normal(len(t)), 1500, 9000)
    crk = (rs.random(len(t)) < 0.012) * rs.standard_normal(len(t)) * 3
    env = np.sin(np.pi * t / d) ** 0.6
    return nz(n + band(crk, 800, 8000)) * env
def staple():
    t = tt(0.25); click = band(rs.standard_normal(len(t)), 2000, 10000) * np.exp(-t / 0.003)
    ping = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / 0.05) * a for f, a in [(3200, .4), (4750, .25), (6100, .15)])
    thunk = np.sin(2 * np.pi * 120 * t) * np.exp(-t / 0.03)
    return nz(click) * .8 + ping + thunk * .6
def clip():
    t = tt(0.12); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t / 0.02) * a for f, a in [(2600, .6), (5300, .3)]) + nz(band(rs.standard_normal(len(t)), 3000, 9000)) * np.exp(-t / 0.002) * .5
def snip():
    t = tt(0.2); c = nz(band(rs.standard_normal(len(t)), 2500, 11000)) * np.exp(-t / 0.004)
    ring = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / 0.035) * a for f, a in [(4100, .3), (6900, .18)])
    swish = nz(band(rs.standard_normal(len(t)), 3000, 8000)) * np.exp(-((t - 0.02) / 0.02) ** 2) * .4
    return c + ring + swish
def crayon(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 300, 2600)
    am = 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 9 * t + rs.random() * 3))
    grit = band((rs.random(len(t)) < 0.02) * rs.standard_normal(len(t)), 500, 4000) * 2
    return nz(n + grit) * am * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.4
def marker(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 1500, 5000)
    squeak = np.sin(2 * np.pi * np.cumsum(2300 + 400 * np.sin(2 * np.pi * 6 * t)) / SR) * 0.12
    return (nz(n) + squeak) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.5
def rip(d):
    t = tt(d); base = band(rs.standard_normal(len(t)), 500, 7000)
    dens = 0.02 + 0.08 * np.sin(np.pi * t / d)
    crk = band((rs.random(len(t)) < dens) * rs.standard_normal(len(t)) * 4, 300, 9000)
    env = np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.08) * (0.6 + 0.4 * np.abs(band(rs.standard_normal(len(t)), 8, 40)) / 0.05).clip(0, 1.4)
    return nz(0.5 * nz(base) + nz(crk)) * env
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 300 + 2200 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return nz(y) * np.sin(np.pi * t / d) ** 1.5
def blip(f):
    t = tt(0.07); s = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sin(2 * np.pi * f * t) * 0.5
    return s * np.exp(-t / 0.018) * np.minimum(1, t / 0.002)
def slide(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 400, 5000)
    am = np.abs(band(rs.standard_normal(len(t)), 4, 30)); am = am / (am.max() + 1e-9)
    return nz(n) * (0.5 + 0.5 * am) * np.sin(np.pi * t / d) ** 0.8
def pluck(f, d=1.6, bright=0.5):
    n = int(d * SR); P = max(2, int(SR / f)); buf = rs.uniform(-1, 1, P); out = np.zeros(n)
    for i in range(n): out[i] = buf[i % P]; buf[i % P] = (bright * buf[i % P] + (1 - bright) * buf[(i + 1) % P]) * 0.996
    return band(out, 80, 5000) * np.minimum(1, np.arange(n) / 60)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
# bed: room tone + gentle plucked loop (F major / D minor), 96 bpm eighths
t = np.arange(N) / SR
room = band(rs.standard_normal(N), 150, 2500); room = nz(room); L += room * .007; R += np.roll(room, 911) * .007
beat = 60 / 96 / 2
prog = [[53, 57, 60, 64], [50, 57, 60, 65], [46, 53, 58, 62], [48, 55, 60, 64]]
k = 0; tb = 0.35
while tb < 9.4:
    ch = prog[int(tb / (beat * 8)) % 4]; note = ch[[0, 2, 1, 3, 2, 1, 3, 2][k % 8]] + 12 * (k % 8 == 3)
    add(pluck(nt(note), 1.2, 0.5), tb + rs.uniform(0, .01), 0.05 * (1.1 if k % 4 == 0 else .8), (-.3 if k % 2 else .3))
    if k % 8 == 0: add(pluck(nt(ch[0] - 12), 1.8, 0.6), tb, 0.08, 0)
    k += 1; tb += beat
for e in json.load(open('events.json')):
    k_, te, v = e['k'], e['t'], e.get('v', 1.0)
    pan = rs.uniform(-.35, .35)
    if k_ == 'slap': add(slap(v), te, 0.38 * v + .1, pan)
    elif k_ == 'tape': add(tape(), te, 0.13, pan)
    elif k_ == 'staple': add(staple(), te, 0.3, .3)
    elif k_ == 'clip': add(clip(), te, 0.18, -.4)
    elif k_ == 'snip': add(snip(), te, 0.28, .35)
    elif k_ == 'crayon': add(crayon(e['d']), te, 0.12, pan)
    elif k_ == 'marker': add(marker(e['d']), te, 0.06, pan)
    elif k_ == 'rip': add(rip(e['d']), te, 0.42, 0); add(rip(e['d'] * .8), te + .05, 0.18, .5)
    elif k_ == 'whoosh': add(whoosh(e['d']), te, 0.2)
    elif k_ == 'blip': add(blip(e['f']), te, 0.07, rs.uniform(-.5, .5))
    elif k_ == 'slide': add(slide(e['d']), te, 0.25); add(slap(.6), te + e['d'], 0.25)
    elif k_ == 'chord':
        for i, m in enumerate([53, 57, 60, 65, 69]): add(pluck(nt(m), 2.2, .5), te + i * 0.05, 0.07, (i - 2) * .15)
fi = int(0.2 * SR); fo = int(0.6 * SR)
for c in (L, R): c[:fi] *= np.linspace(0, 1, fi); c[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.82
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
