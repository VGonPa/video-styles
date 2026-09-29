# events.json → audio.wav (48 kHz stereo, 10 s), all synthesized
# snappy panel pops, soft lettering ticks, wand swishes, a twinkle, a big POOF (noise burst + low thump),
# a fizz of smoke, then an awkward beat of crickets, a sweat-drop plip and a tiny eye tick.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(91)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def nrm(x): return x / (np.abs(x).max() + 1e-9)
def noise(d, lo, hi): return nrm(band(rs.standard_normal(int(d * SR)), lo, hi))
def sweep(f0, f1, d, curve=1.0):
    t = tt(d); f = f0 + (f1 - f0) * (t / d) ** curve; return np.sin(2 * np.pi * np.cumsum(f) / SR)
def snap(v=1):   # a dry paper "pop": short noise click + a quick pitched knock
    t = tt(.09); return (noise(.09, 1200, 7000) * np.exp(-t / .006) * .7 + sweep(520, 180, .09) * np.exp(-t / .022)) * v
def blip():
    t = tt(.05); return sweep(1500, 1100, .05) * np.exp(-t / .012)
def swish(v=1):
    d = .26; t = tt(d); n = noise(d, 600, 5000); f = np.sin(np.pi * t / d) ** 2
    return band(n * f, 800 + 0 * v, 6000) * (.6 + .4 * v)
def chirp():     # little cheerful two-note "ta-da" from the assistant's wave
    out = np.zeros(int(.3 * SR))
    for k, (f, t0) in enumerate([(880, 0), (1175, .11)]):
        t = tt(.16); s = np.sin(2 * np.pi * f * t) * np.exp(-t / .05); i = int(t0 * SR); out[i:i + len(s)] += s
    return out
def twinkle():
    out = np.zeros(int(.8 * SR))
    for k, f in enumerate([1568, 2093, 2637, 3136, 4186]):
        t = tt(.5); s = (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 2.01 * t)) * np.exp(-t / .12); i = int(k * .055 * SR); out[i:i + len(s)] += s * (1 - k * .1)
    return out
def poof():
    d = .9; t = tt(d); n = noise(d, 150, 4000) * np.exp(-t / .16) * np.minimum(1, t / .004)
    thump = sweep(140, 45, .35) * np.exp(-tt(.35) / .1); out = n.copy(); out[:len(thump)] += thump * 1.4
    return out
def hiss(d):
    t = tt(d); return noise(d, 3000, 9000) * np.exp(-t / (d * .45)) * np.minimum(1, t / .05)
def crickets(d):
    out = np.zeros(int(d * SR)); t0 = 0.05
    while t0 < d - .2:
        for k in range(3):   # a chirp = 3 fast pulses of a 4.6 kHz tone
            t = tt(.028); s = np.sin(2 * np.pi * 4600 * t) * np.sin(np.pi * t / .028) ** 2; i = int((t0 + k * .036) * SR); out[i:i + len(s)] += s
        t0 += .42
    return out
def drip():
    t = tt(.12); return sweep(700, 1700, .12, .5) * np.exp(-t / .035)
def tick():
    t = tt(.03); return noise(.03, 2500, 9000) * np.exp(-t / .004)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'snap': add(snap(v), te, .35, rs.uniform(-.3, .3))
    elif k == 'blip': add(blip(), te, .08, 0)
    elif k == 'swish': add(swish(v), te, .16 * v, -.2)
    elif k == 'giggle': add(chirp(), te, .06, .3)
    elif k == 'twinkle': add(twinkle(), te, .05, .2)
    elif k == 'poof': add(poof(), te, .7, .1)
    elif k == 'hiss': add(hiss(e['d']), te, .05, .15)
    elif k == 'crickets': add(crickets(e['d']), te, .035, .45)
    elif k == 'drip': add(drip(), te, .09, -.2)
    elif k == 'tick': add(tick(), te, .12, 0)
# faint room tone so the silence beat is "silent" but never digital zero
L += noise(DUR, 80, 900) * .004; R += noise(DUR, 80, 900) * .004
fi = int(.05 * SR); fo = int(.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.6) * .9
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
