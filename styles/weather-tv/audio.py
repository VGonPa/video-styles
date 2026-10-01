# events.json → audio.wav (48 kHz stereo, 10 s)
# cheesy 1990s weather bed: FM electric piano (Fmaj9 Em7 Dm9 G13 → Cmaj9), slap-ish synth bass, drum machine
# (kick, gated snare, hats), plus graphics SFX: glint, DVE whoosh, bubbly icon pops, ticks, front sweep,
# radar blips, tab flips, panel thumps.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(8)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
norm = lambda x: x / (np.abs(x).max() + 1e-9)

# ── instruments ──
def ep(f, d=1.6):
    t = tt(d); I = 1.6 * np.exp(-t / .25) + .25
    s = np.sin(2 * np.pi * f * t + I * np.sin(2 * np.pi * f * t)) + .25 * np.sin(2 * np.pi * 14 * f * t) * np.exp(-t / .02)
    return s * np.exp(-t / 1.1) * np.minimum(1, t / .004) * np.minimum(1, (d - t) / .15)
def pad(f, d):
    t = tt(d); s = sum(np.sin(2 * np.pi * f * h * t * (1 + .002 * (h % 2))) / h for h in range(1, 7))
    return s * np.minimum(1, t / .35) * np.minimum(1, (d - t) / .4)
def bass(f, d=.45):
    t = tt(d); I = 2.2 * np.exp(-t / .06)
    s = np.sin(2 * np.pi * f * t + I * np.sin(2 * np.pi * f * 2 * t))
    return s * np.exp(-t / .22) * np.minimum(1, t / .002) * np.minimum(1, (d - t) / .03)
def kick():
    t = tt(.35); f = 50 + 120 * np.exp(-t * 30); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .12)
def snare():
    t = tt(.32); n = band(rs.standard_normal(len(t)), 900, 9000)
    gate = np.where(t < .16, 1.0, np.exp(-(t - .16) / .02))      # 80s/90s gated tail
    return (.7 * norm(n) + .4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / .04)) * gate * (0.35 + .65 * np.exp(-t / .05))
def hat(o=False):
    t = tt(.2 if o else .05); n = band(rs.standard_normal(len(t)), 7000, 15000); return norm(n) * np.exp(-t / (.07 if o else .012))
# ── sfx ──
def pop(f=1.0):
    t = tt(.16); fr = (420 + 900 * (1 - np.exp(-t * 40))) * f
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / .045) * np.minimum(1, t / .003)
def tick():
    t = tt(.03); return norm(band(rs.standard_normal(len(t)), 2500, 9000)) * np.exp(-t / .004)
def lp_noise(d, f0, f1, shape):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = f0 + (f1 - f0) * shape(t / d); a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y)
def whoosh(d): return lp_noise(d, 200, 3200, lambda u: np.sin(np.pi * u) ** 2) * np.sin(np.pi * tt(d) / d) ** 1.5
def sweep(d): t = tt(d); return lp_noise(d, 300, 5000, lambda u: u ** 1.5) * np.sin(np.pi * t / d) ** .8
def blip(v):
    t = tt(.07); return np.sin(2 * np.pi * (1500 if v > .8 else 1180) * t) * np.exp(-t / .025) * np.minimum(1, t / .002)
def thud():
    t = tt(.4); f = 45 + 80 * np.exp(-t * 18); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .14)
def glint():
    out = np.zeros(int(1.2 * SR))
    for i, m in enumerate([84, 88, 91, 96, 100]):
        t = tt(.9); s = np.sin(2 * np.pi * nt(m) * t) * np.exp(-t / .35) * np.minimum(1, t / .002)
        k = int(i * .06 * SR); out[k:k + len(s)] += s
    return out

# ── music bed ──
BEAT = 60 / 108; T0 = 0.25; SIGN = 8.25
CH = [(T0, [53, 57, 60, 64, 67], 41), (T0 + 2 * BEAT, [52, 55, 59, 62], 40), (T0 + 4 * BEAT, [50, 53, 57, 60, 64], 38),
      (T0 + 6 * BEAT, [53, 55, 59, 64], 43), (T0 + 8 * BEAT, [53, 57, 60, 64, 67], 41), (T0 + 10 * BEAT, [52, 55, 59, 62], 40),
      (T0 + 12 * BEAT, [50, 53, 57, 60, 64], 38), (T0 + 13 * BEAT, [53, 55, 59, 64], 43)]
for i, (tc, notes, root) in enumerate(CH):
    te = CH[i + 1][0] if i + 1 < len(CH) else SIGN
    for j, m in enumerate(notes):
        add(ep(nt(m), min(1.8, te - tc + .3)), tc + j * .012, .05, -.4 + .2 * j)
        add(ep(nt(m) * 1.004, min(1.8, te - tc + .3)), tc + .02 + j * .012, .03, .4 - .2 * j)
    add(pad(nt(root + 24), te - tc + .3), tc, .018, 0)
    # bass: root on beats, octave pops on offbeats
    b = tc
    while b < te - .05:
        add(bass(nt(root - 12)), b, .2); add(bass(nt(root), .2), b + BEAT * .5, .09); b += BEAT
# drums until the sign-off
b, k = T0, 0
while b < SIGN - .05:
    if k % 2 == 0: add(kick(), b, .42)
    else: add(snare(), b, .2, .1)
    add(hat(), b + BEAT * .5, .05, .3); add(hat(), b, .035, .3)
    if k % 4 == 3: add(hat(True), b + BEAT * .5, .05, .3)
    b += BEAT; k += 1
# sign-off: Cmaj9 swell + ringing EP + soft crash
for j, m in enumerate([48, 55, 59, 62, 64, 67, 71]):
    add(ep(nt(m), 1.75), SIGN + j * .03, .06, -.3 + .1 * j); add(pad(nt(m), 1.7), SIGN, .012, .2 - .07 * j)
add(bass(nt(36), 1.4), SIGN, .28); add(kick(), SIGN, .4)
cr = tt(1.6); add(norm(band(rs.standard_normal(len(cr)), 4000, 14000)) * np.exp(-cr / .5), SIGN, .06)

# ── sfx from the animation ──
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'glint': add(glint(), te, .05, .3)
    elif k == 'whoosh': add(whoosh(e['d']), te, .2)
    elif k == 'thud': add(thud(), te, .3)
    elif k == 'swipe': add(whoosh(.35), te, .12, -.4)
    elif k == 'pop': add(pop(e.get('f', 1)), te, .2 * v, rs.uniform(-.35, .35))
    elif k == 'tick': add(tick(), te, .08, .2)
    elif k == 'sweep': add(sweep(e['d']), te, .14, -.2)
    elif k == 'blip': add(blip(v), te, .06 * v, .3)
    elif k == 'flip': add(tick(), te, .12); add(tick(), te + .12, .1)
    elif k == 'thump': add(thud(), te, .14)
    elif k == 'chord': pass                       # the sign-off chord is part of the bed above

# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.82
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
