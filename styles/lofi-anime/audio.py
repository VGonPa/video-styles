# events.json → audio.wav (48 kHz stereo, 10 s)
# rain on the window (hiss bed + glass ticks), lamp click, distant train rumble with rail clacks (pans right → left),
# thunder after the lightning, a sleepy purr, pencil scribbles for the captions, and a warm lo-fi electric-piano
# chord loop with tape wow (Fmaj9 → Em7 → Dm9 → Cmaj9) that starts when the lamp clicks on and fades with the picture.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(30)
t_all = np.arange(N) / SR
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tilt(x, k):   # pink-ish spectral tilt
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= 1 / np.maximum(f, 40) ** k; return np.fft.irfft(X, len(x))
def norm(x): return x / (np.abs(x).max() + 1e-9)
def tt(d): return np.arange(int(d * SR)) / SR
ev = json.load(open('events.json'))
E = {e['k']: e for e in ev}
# ── rain bed ──
rain0 = E['rain']['t']
ramp = 0.3 + 0.7 * np.clip((t_all - rain0) / 2.0, 0, 1) ** 0.8
for ch, seed in ((L, 1), (R, 2)):
    r2 = np.random.default_rng(seed)
    hiss = norm(tilt(band(r2.standard_normal(N), 250, 11000), .45))
    body = norm(band(r2.standard_normal(N), 90, 500))
    am = 1 + .25 * norm(band(r2.standard_normal(N), .3, 3))
    ch += (hiss * .10 + body * .05) * ramp * am
# glass ticks: tiny droplet hits, denser as the rain builds
nt_ = int(260)
for i in range(nt_):
    te = rain0 + rs.random() * (DUR - rain0)
    if rs.random() > 0.35 + 0.65 * np.clip((te - rain0) / 2, 0, 1): continue
    d = tt(.012); f = 2500 + rs.random() * 4000
    s = np.sin(2 * np.pi * f * d) * np.exp(-d / .0022)
    add(s, te, .02 + .03 * rs.random(), rs.uniform(-.8, .8))
# ── tape hiss + music ──
hissT = norm(band(rs.standard_normal(N), 3000, 12000)); L += hissT * .006; R += np.roll(hissT, 999) * .006
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
m0 = E['music']['t']
wow = lambda d: 1 + .0035 * np.sin(2 * np.pi * .55 * d) + .0015 * np.sin(2 * np.pi * 3.1 * d)
def ep(freq, d, dec=1.6):
    t = tt(d); ph = 2 * np.pi * np.cumsum(freq * wow(t + rs.random())) / SR
    s = np.sin(ph) + .28 * np.sin(2 * ph) * np.exp(-t / .25) + .08 * np.sin(3 * ph) * np.exp(-t / .12)
    env = np.minimum(1, t / .012) * (0.35 + .65 * np.exp(-t / dec)) * np.minimum(1, (d - t) / .35)
    return s * env * (1 + .12 * np.sin(2 * np.pi * 4.2 * t))
chords = [[53, 57, 60, 64, 67], [52, 55, 59, 62, 67], [50, 53, 57, 60, 64], [48, 52, 55, 59, 62]]
bass = [29, 28, 26, 24]
for i, (ch, b) in enumerate(zip(chords, bass)):
    tc = m0 + i * 2.0
    for k, m in enumerate(ch): add(ep(nt(m), 2.3), tc + k * .035 + .02 * rs.random(), .045, (k - 2) * .18)
    add(ep(nt(b + 12), 2.1, 1.0), tc, .07)
    add(ep(nt(ch[1] + 12), .9, .5), tc + 1.1, .02, .2)       # soft off-beat restrike
for te, m in [(2.7, 76), (3.35, 72), (4.45, 74), (5.25, 71), (6.55, 69), (7.2, 72), (8.35, 67)]:
    add(ep(nt(m), 1.6, .7), te, .03, .25)
# ── lamp clicks ──
def click(v=1):
    d = tt(.04); n = norm(band(rs.standard_normal(len(d)), 1800, 9000)) * np.exp(-d / .003)
    return (n + .6 * np.sin(2 * np.pi * 1100 * d) * np.exp(-d / .006)) * v
for e in ev:
    if e['k'] == 'click': add(click(e.get('v', 1)), e['t'], .35, .45)
# ── distant train: rumble + rail clacks, right → left ──
tr = E['train']; td = tr['d']; d = tt(td)
rum = norm(band(rs.standard_normal(len(d)), 35, 260)) * np.sin(np.pi * d / td) ** 1.4
clk = np.zeros(len(d))
for k in range(int(td / .42)):
    for off in (0, .085):
        i = int((k * .42 + off) * SR)
        c = norm(band(rs.standard_normal(int(.05 * SR)), 150, 1200)) * np.exp(-tt(.05) / .012)
        clk[i:i + len(c)] += c[:max(0, len(d) - i)]
sig = (rum * .7 + clk * .22) * np.sin(np.pi * d / td) ** 1.2
pan = np.linspace(.7, -.7, len(d))
i0 = int(tr['t'] * SR); n = min(len(d), N - i0)
L[i0:i0 + n] += sig[:n] * .16 * np.sqrt(.5 - pan[:n] / 2) * 1.414; R[i0:i0 + n] += sig[:n] * .16 * np.sqrt(.5 + pan[:n] / 2) * 1.414
# ── lightning crackle + thunder ──
d = tt(.25); add(norm(band(rs.standard_normal(len(d)), 1500, 8000)) * np.exp(-d / .05), E['flash']['t'], .04, .3)
d = tt(3.6); th = norm(band(rs.standard_normal(len(d)), 20, 180))
env = np.minimum(1, d / .15) * np.exp(-d / 1.2) * (1 + .6 * np.sin(2 * np.pi * 1.3 * d + 1) ** 2)
add(th * env, E['thunder']['t'], .42, .2); add(norm(band(rs.standard_normal(len(d)), 150, 900)) * env * np.exp(-d / .5), E['thunder']['t'] + .05, .06, .3)
# ── purr + pencil scribbles ──
d = tt(1.8); pr = norm(band(rs.standard_normal(len(d)), 60, 400)) * (0.5 + .5 * np.sin(2 * np.pi * 26 * d)) * np.sin(np.pi * d / 1.8)
add(pr, E['purr']['t'], .07, -.35)
for e in ev:
    if e['k'] == 'pen':
        d = tt(e['d']); sc = norm(band(rs.standard_normal(len(d)), 2500, 7000)) * np.abs(np.sin(2 * np.pi * 5.5 * d)) ** 2 * np.sin(np.pi * d / e['d'])
        add(sc, e['t'], .018, -.4)
# ── master: music + fx fade with the picture, rain keeps going until the last moment ──
fi = int(.4 * SR); fo = int(.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.5) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
