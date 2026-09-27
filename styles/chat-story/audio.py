# events.json → audio.wav (48 kHz stereo, 10 s)
# messenger foley: notification ding, screen tap, keyboard clicks, send swooshes, receive bloops, read tick,
# record blip, a breathy voice-note sigh, heart pop + sparkle, over a soft pluck + pad bed (D major), ending on a chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(47)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
nrm = lambda x: x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def sweep(f0, f1, d, dec):
    t = tt(d); f = f0 * (f1 / f0) ** (t / d); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / dec) * np.minimum(1, t / .002)
def key():
    t = tt(.04); n = nrm(band(rs.standard_normal(len(t)), 1500, 7000)) * np.exp(-t / .004)
    return .6 * n + .5 * np.sin(2 * np.pi * (900 + 300 * rs.random()) * t) * np.exp(-t / .006)
def tap():
    t = tt(.06); return nrm(band(rs.standard_normal(len(t)), 800, 5000)) * np.exp(-t / .006) * .8 + np.sin(2 * np.pi * 420 * t) * np.exp(-t / .015)
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 250 + 2600 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return nrm(y) * np.sin(np.pi * t / d) ** 1.6
def bell(freq, d=1.0):
    t = tt(d); s = np.sin(2 * np.pi * freq * t) + .3 * np.sin(2 * np.pi * freq * 2.76 * t) * np.exp(-t / .1)
    return s * np.exp(-t / (d / 3.5)) * np.minimum(1, t / .003)
def pluck(freq, d=.6):
    t = tt(d); return (np.sin(2 * np.pi * freq * t) + .3 * np.sin(2 * np.pi * freq * 2 * t) * np.exp(-t / .05)) * np.exp(-t / .16) * np.minimum(1, t / .003)
def tone(freq, d, att=.4, rel=1.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in [(1, 1), (2, .2), (3, .06)])
    return s * np.minimum(1, t / att) * np.minimum(1, np.maximum(0, d - t) / rel)
def sigh(d):  # breathy exhale + falling hum, band-limited like a phone speaker
    t = tt(d); env = np.sin(np.pi * np.minimum(1, t / d)) ** .8
    br = nrm(band(rs.standard_normal(len(t)), 500, 3200)) * env * (1 - .5 * t / d)
    f = 210 * (1 - .28 * t / d) * (1 + .02 * np.sin(2 * np.pi * 5 * t))
    hum = sum(a * np.sin(2 * np.pi * np.cumsum(f * h) / SR) for h, a in [(1, 1), (2, .5), (3, .3), (4, .15)])
    hum = band(hum, 150, 3400) * np.minimum(1, np.maximum(0, t - .12) / .15) * env
    return .55 * br + .5 * nrm(hum)
t = np.arange(N) / SR
# bed: soft pad (D add9) + a light pluck figure
for m, g, p in [(50, .04, -.3), (57, .028, .3), (62, .022, 0), (64, .016, -.2)]:
    add(tone(nt(m), 9.6, 1.5, 1.4), .15, g, p)
beat = 60 / 100 / 2; pat = [74, 78, 81, 78, 76, 81, 78, 74]; k = 0; tb = .7
while tb < 9.2:
    add(pluck(nt(pat[k % 8] - (0 if (k // 16) % 2 == 0 else 2))), tb, .035 * (1 if k % 2 == 0 else .65), .3 if k % 2 else -.3); k += 1; tb += beat
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'key': add(key(), te, .16 * v, rs.uniform(-.25, .25))
    elif k == 'tap': add(tap(), te, .28)
    elif k == 'whoosh': add(whoosh(e['d']), te, .12 * v, rs.uniform(-.3, .3))
    elif k == 'slide': add(whoosh(.3), te, .07 * v)
    elif k == 'ding': add(bell(nt(83)), te, .16, .1); add(bell(nt(90)), te + .11, .13, .1)
    elif k == 'recv': add(sweep(520, 880, .12, .04), te, .2, -.2); add(sweep(700, 1200, .1, .03), te + .06, .12, -.2)
    elif k == 'send': add(whoosh(.18), te - .04, .08, .25); add(sweep(700, 1500, .1, .03), te, .18, .25)
    elif k == 'tick': add(sweep(2400, 2600, .03, .006), te, .1)
    elif k == 'blip': add(sweep(880, 880, .08, .03), te, .12); add(sweep(1320, 1320, .08, .03), te + .07, .1)
    elif k == 'sigh': add(sigh(e['d']), te, .22, .15)
    elif k == 'heart':
        add(sweep(300, 1400, .14, .035), te, .3)
        for i, m in enumerate([86, 90, 93, 98]): add(bell(nt(m), .9), te + .05 + i * .06, .07, rs.uniform(-.4, .4))
    elif k == 'chord':
        for i, m in enumerate([50, 57, 62, 66, 69, 74]): add(tone(nt(m), 1.6, .05 + i * .02, 1.1), te + i * .03, .03)
fi = int(.15 * SR); fo = int(.8 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.tanh(np.stack([L, R], 1) * 1.8) * .8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
