# events.json → audio.wav (48 kHz stereo, 10 s), all synthesized
# calm plucked morning tune + birds + slurps → tape-stop and Wi-Fi blips → twitch plinks, inhale →
# BOOM + formant-filtered synth scream (muffled as the camera leaves the planet) → narwhal ding + blip talk →
# letter bonks → whoosh back in → the calm tune again, a sip, iris-close slide and a final plink.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(86)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def nrm(x): return x / (np.abs(x).max() + 1e-9)
def noise(d, lo, hi): return nrm(band(rs.standard_normal(int(d * SR)), lo, hi))
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def pluck(f, d=.6, dec=.18):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (dec / h ** .5)) for h, a in [(1, 1), (2, .5), (3, .25), (4, .12)])
    return s * np.minimum(1, t / .003)
def chirp(f0, f1, d):
    t = tt(d); f = f0 + (f1 - f0) * (t / d); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d)
def tweet():
    out = np.zeros(int(.35 * SR))
    for k in range(3):
        c = chirp(3800 + rs.uniform(-300, 300), 2600, .06); i = int(k * .09 * SR); out[i:i + len(c)] += c
    return out
def slurp(d):
    t = tt(d); am = .5 + .5 * np.sin(2 * np.pi * (9 + 5 * t / d) * t); n = rs.standard_normal(len(t))
    X = np.fft.rfft(n); f = np.fft.rfftfreq(len(n), 1 / SR); X *= np.exp(-((f - 1300) / 700) ** 2) + .4 * np.exp(-((f - 2600) / 500) ** 2)
    return nrm(np.fft.irfft(X, len(n))) * am * np.sin(np.pi * t / d) ** .6
def whoosh(d, up=False):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    prog = t / d if up else 1 - t / d
    fc = 250 + 3000 * prog ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    env = np.sin(np.pi * t / d) ** 1.2 if not up else (t / d) ** 2 * np.minimum(1, (d - t) / .03)
    return nrm(y) * env
def blip(f, d=.09):
    t = tt(d); return np.sign(np.sin(2 * np.pi * f * t)) * .5 * np.exp(-t / .05) * np.minimum(1, t / .002)
def err():
    t = tt(.32); return (np.sign(np.sin(2 * np.pi * 150 * t)) * .5 + np.sin(2 * np.pi * 300 * t) * .3) * np.minimum(1, (0.32 - t) / .05)
def plink(f=1760):
    t = tt(.25); return np.sin(2 * np.pi * f * t * (1 + .01 * np.sin(t * 90))) * np.exp(-t / .05)
def inhale(d):
    t = tt(d); n = rs.standard_normal(len(t)); X = np.fft.rfft(n); fr = np.fft.rfftfreq(len(n), 1 / SR); X *= np.exp(-((fr - 1800) / 900) ** 2)
    return nrm(np.fft.irfft(X, len(n))) * (t / d) ** 1.5
def boom():
    t = tt(1.4); f = 90 * np.exp(-t * 4) + 32
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .5) + .8 * noise(1.4, 60, 3000) * np.exp(-t / .12)
def crash():
    t = tt(1.6); return noise(1.6, 3000, 14000) * np.exp(-t / .45) * np.minimum(1, t / .002)
def scream(d):
    t = tt(d); f0 = 205 + 25 * np.sin(2 * np.pi * 5.5 * t) + 18 * np.minimum(1, t / .08) + 6 * rs.standard_normal(len(t)).cumsum() / np.sqrt(len(t)) * 3
    ph = 2 * np.pi * np.cumsum(f0) / SR; saw = sum(np.sin(k * ph) / k for k in range(1, 40))
    x = saw + .35 * rs.standard_normal(len(t))
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR)
    # "OOOO" formants + some rasp
    X *= 1.0 * np.exp(-((fr - 330) / 120) ** 2) + .7 * np.exp(-((fr - 820) / 160) ** 2) + .25 * np.exp(-((fr - 2500) / 400) ** 2) + .05
    y = nrm(np.fft.irfft(X, len(x))); y = np.tanh(y * 3.2)
    env = np.minimum(1, t / .05) * np.minimum(1, (d - t) / .015)
    return y * env
def lowpass(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= 1 / (1 + (f / fc) ** 4); return np.fft.irfft(X, len(x))
def rumble(d):
    t = tt(d); return noise(d, 25, 160) * np.minimum(1, t / .05) * np.minimum(1, (d - t) / .2)
def bell(f, d=1.4):
    t = tt(d); return sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (dec)) for h, a, dec in [(1, 1, .6), (2.76, .5, .25), (5.4, .25, .1), (2, .3, .4)]) * np.minimum(1, t / .002)
def talk(d):
    out = np.zeros(int(d * SR)); k = 0; tt0 = 0.0
    while tt0 < d - .06:
        f = [392, 440, 494, 330, 523][int(rs.integers(0, 5))] * (1.0 if k % 3 else 1.1); b = blip(f, .07) * .6; i = int(tt0 * SR); n = min(len(b), len(out) - i); out[i:i + n] += b[:n]; tt0 += .075 + rs.uniform(0, .03); k += 1
    return out
def woodblock(f):
    t = tt(.18); return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 2.3 * t)) * np.exp(-t / .03)
def thump():
    t = tt(.35); f = 120 * np.exp(-t * 12) + 45; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .1)
def slide(d, f0, f1):
    t = tt(d); f = f0 * (f1 / f0) ** (t / d); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / .02) * np.minimum(1, (d - t) / .05)
def pop():
    t = tt(.12); f = 700 * np.exp(-t * 30) + 300; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .03)
# ── calm morning tune (plucked, F major, a bit of swing) — stops dead at the drop, returns for the deadpan ──
mel = [(0, 72), (.5, 76), (.75, 79), (1.0, 77), (1.5, 76), (2.0, 74), (2.25, 72)]
chords = [(0, [53, 60, 65]), (1.0, [58, 62, 65]), (2.0, [55, 60, 64])]
def tune(t0, t1, trans=0, g=1.0):
    for (tm, m) in mel:
        for rep in (0, 2.5):
            tn = t0 + tm + rep
            if tn < t1: add(pluck(nt(m + trans), .7, .2), tn, .09 * g, .15)
    for (tm, ch) in chords:
        for rep in (0, 2.5):
            tn = t0 + tm + rep
            if tn < t1:
                for j, m in enumerate(ch): add(pluck(nt(m + trans), 1.0, .35), tn + j * .015, .05 * g, -.2)
ev = json.load(open('events.json'))
T = {e['k']: e['t'] for e in ev}
tune(.1, 2.52)
add(slide(.35, 520, 90) * np.linspace(1, .2, int(.35 * SR)), 2.5, .08)          # tape-stop of the tune
tune(7.55, 9.6, 0, .85)
for e in ev:
    k, te, v = e['k'], e['t'], e.get('v', 1.0); pan = rs.uniform(-.3, .3)
    if k == 'tweet': add(tweet(), te, .06, .5)
    elif k == 'pop': add(pop(), te, .18 * v)
    elif k == 'sip': add(slurp(e['d']), te, .08, .15)
    elif k == 'whoosh': add(whoosh(e['d']), te, .14, pan)
    elif k == 'down': add(blip([880, 660, 440][int(v)], .1), te, .07, -.2)
    elif k == 'error': add(err(), te, .09)
    elif k == 'twitch': add(plink(2200 + rs.uniform(-100, 100)), te, .07, .3)
    elif k == 'inhale': add(inhale(e['d']), te, .12)
    elif k == 'boom': add(boom(), te, .5)
    elif k == 'crash': add(crash(), te, .12)
    elif k == 'scream':
        d = e['d']; s = scream(d); lp = lowpass(s, 600); tl = tt(d) + te
        m = np.clip((tl - 4.9) / .75, 0, 1)                                            # muffle as we leave the planet
        mix = s * (1 - m) + lp * m * .8
        add(mix, te, .36); add(mix, te + .012, .1, .6); add(rumble(d), te, .25)
    elif k == 'zoomout': add(whoosh(e['d']), te, .18); add(slide(e['d'], 900, 140), te, .03)
    elif k == 'ding': add(bell(nt(88)), te, .12, .4); add(bell(nt(95)), te + .06, .06, .4)
    elif k == 'talk': add(talk(e['d']), te, .08, .3 if te < 7 else -.1)
    elif k == 'bonk': add(woodblock(nt(72 + [12, 11, 9, 7, 5, 4, 2, 0][int(v) % 8])), te, .1, -.4 + v * .1)
    elif k == 'zoomin': add(whoosh(e['d'], up=True), te, .2)
    elif k == 'land': add(thump(), te, .3)
    elif k == 'iris': add(slide(.4, 300, 900), te, .025)
    elif k == 'irisclose': add(slide(.55, 1100, 260), te, .03)
    elif k == 'plink': add(pluck(nt(84), .8, .25), te, .1); add(pluck(nt(77), .8, .3), te + .08, .07)
fi = int(.02 * SR); fo = int(.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.2) * .9
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
