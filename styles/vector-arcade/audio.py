# events.json → audio.wav (48 kHz stereo, 10 s)
# early-80s arcade board sounds, all synthesized: CRT power-on thump, title "zaps" as strokes land, planet sweep,
# warp riser through the web, two-note heartbeat bass, square-wave laser pews, noise-burst explosions (three sizes),
# thrust rumble, the big ship explosion, a falling GAME OVER arpeggio, initials blips + confirm chime,
# INSERT COIN chirps and the power-off down-sweep. A faint transformer hum sits under everything.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(36)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); p = 0.0
    for i in range(len(x)): p = (1 - a) * x[i] + a * p; y[i] = p
    return y
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def sq(ph): return np.sign(np.sin(ph)) * 0.8 + 0.2 * np.sin(ph)
def sweep(f0, f1, d, wave='sq', curve=1.0):
    t = tt(d); u = (t / d) ** curve; f = f0 * (f1 / f0) ** u; ph = 2 * np.pi * np.cumsum(f) / SR
    return sq(ph) if wave == 'sq' else np.sin(ph)
def env(n, a, r):
    t = np.arange(n) / SR; d = n / SR; return np.minimum(1, t / max(a, 1e-4)) * np.clip((d - t) / max(r, 1e-4), 0, 1)
def noise_boom(d, fc0, fc1):
    t = tt(d); x = rs.standard_normal(len(t)); fc = fc0 * (fc1 / fc0) ** (t / d)
    y = np.zeros_like(x); p = 0.0; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    y /= np.abs(y).max() + 1e-9
    # 'crackle' of a digital noise generator: sample-and-hold
    hold = np.repeat(rs.standard_normal(len(t) // 40 + 1), 40)[:len(t)]
    return (0.8 * y + 0.2 * lp(hold, 1800) / 2) * np.exp(-t / (d * 0.33))
# bed: faint transformer hum + high-voltage whine from power-on to power-off
t = np.arange(N) / SR
hum = (np.sin(2 * np.pi * 60 * t) + .5 * np.sin(2 * np.pi * 120 * t) + .2 * np.sin(2 * np.pi * 180 * t))
bed = np.clip(t / 0.3, 0, 1) * np.clip((9.55 - t) / 0.3, 0, 1)
L += hum * 0.010 * bed; R += hum * 0.010 * bed
whine = np.sin(2 * np.pi * 7800 * t) * 0.0025 * bed; L += whine; R += whine
ev = json.load(open('events.json'))
for e in ev:
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'on':
        s = sweep(40, 90, 0.35, 'sin') * env(int(.35 * SR), .005, .3); add(s, te, 0.5)
        c = band(rs.standard_normal(int(.05 * SR)), 1500, 9000) * np.exp(-tt(.05) / .006); add(c, te, 0.25)
    elif k == 'zap':
        f0 = 1800 + 900 * v; s = sweep(f0, f0 * 0.35, 0.07, 'sq', 0.6) * env(int(.07 * SR), .002, .05)
        add(lp(s, 5000), te, 0.07, rs.uniform(-.5, .5))
    elif k == 'planet':
        s = sweep(180, 900, 0.7, 'sin', 1.4) * env(int(.7 * SR), .05, .3) * (1 + .5 * np.sin(2 * np.pi * 14 * tt(.7))); add(s, te, 0.12, -.4)
    elif k == 'swell':
        for m, g in [(220, 1), (330, .6), (440, .4)]:
            s = sweep(m, m, 0.8, 'sq') * env(int(.8 * SR), .15, .5); add(lp(s, 1600), te, 0.035 * g)
    elif k == 'warp':
        d = e['d']; s = sweep(70, 1400, d, 'sq', 2.2) * env(int(d * SR), .2, .08)
        n = band(rs.standard_normal(int(d * SR)), 300, 6000) * np.linspace(0.1, 1, int(d * SR)) ** 2 * env(int(d * SR), .1, .08)
        add(lp(s, 3000), te, 0.10); add(n, te, 0.05)
    elif k == 'flash':
        add(noise_boom(0.6, 6000, 300), te, 0.22)
    elif k == 'fire':
        s = sweep(2600, 500, 0.12, 'sq', 0.5) * env(int(.12 * SR), .001, .08); add(lp(s, 7000), te, 0.09, rs.uniform(-.2, .2))
    elif k == 'boom':
        d = [0.7, 0.5, 0.35][int(v)]; add(noise_boom(d, [900, 1500, 2600][int(v)], 120), te, [0.5, 0.38, 0.28][int(v)], rs.uniform(-.3, .3))
    elif k == 'beat':
        f = 55 if v else 49; s = sweep(f, f, 0.14, 'sq') * env(int(.14 * SR), .003, .09); add(lp(s, 400), te, 0.35)
    elif k == 'thrust':
        d = e['d']; n = lp(rs.standard_normal(int(d * SR)), 280) * env(int(d * SR), .05, .15)
        n *= 1 + .4 * np.sign(np.sin(2 * np.pi * 30 * tt(d))); add(n / (np.abs(n).max() + 1e-9), te, 0.2)
    elif k == 'shipboom':
        add(noise_boom(1.6, 1200, 60), te, 0.8); add(sweep(120, 30, 1.0, 'sin') * env(int(SR), .002, .8), te, 0.5)
    elif k == 'over':
        for i, f in enumerate([784, 659, 523, 392, 262]):
            s = sweep(f, f, 0.16, 'sq') * env(int(.16 * SR), .004, .1); add(lp(s, 3000), te + i * 0.11, 0.07)
    elif k == 'tick':
        s = sweep(1200, 1200, 0.03, 'sq') * env(int(.03 * SR), .001, .02); add(s, te, 0.04)
    elif k == 'blip':
        s = sweep(1560, 1560, 0.035, 'sq') * env(int(.035 * SR), .001, .02); add(lp(s, 5000), te, 0.06)
    elif k == 'confirm':
        for i, f in enumerate([1047, 1319, 1568, 2093]):
            s = sweep(f, f, 0.09, 'sq') * env(int(.09 * SR), .002, .06); add(lp(s, 5000), te + i * 0.06, 0.06)
    elif k == 'coin':
        s = np.concatenate([sweep(988, 988, .07, 'sq'), sweep(1319, 1319, .16, 'sq')]); s *= env(len(s), .003, .1); add(lp(s, 4000), te, 0.05)
    elif k == 'off':
        s = sweep(900, 40, 0.55, 'sin', 0.5) * env(int(.55 * SR), .005, .3); add(s, te, 0.22)
        c = band(rs.standard_normal(int(.08 * SR)), 800, 8000) * np.exp(-tt(.08) / .01); add(c, te + 0.4, 0.12)
fi = int(0.02 * SR); fo = int(0.3 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
