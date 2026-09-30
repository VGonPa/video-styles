# events.json → audio.wav · projector tick (24/sec, faint), 1 kHz "2-pop", silent-film piano motifs, splice bumps,
# engine cough + radial-engine spin-up, frameshift clatter, run-out flapping and projector wind-down. Band-limited like optical sound.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); out = np.zeros(N)
rs = np.random.default_rng(3)
def add(sig, t, g=1.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0: out[i:i + n] += sig[:n] * g
def click(g=1.0, f=1800, d=0.004):
    n = int(0.02 * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * tt) * np.exp(-tt / d) + 0.5 * np.sin(2 * np.pi * 180 * tt) * np.exp(-tt / 0.008)) * g
def thump(f=70, d=0.05, dur=0.25):
    n = int(dur * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * f * tt * (1 - 0.3 * tt / dur)) * np.exp(-tt / d)
def burst(dur, d, lp=0.5):
    n = int(dur * SR); tt = np.arange(n) / SR; z = rs.normal(0, 1, n)
    for _ in range(3): z = lp * z + (1 - lp) * np.roll(z, 1)
    return z * np.exp(-tt / d)
def piano(freq, dur=2.2):
    n = int(dur * SR); tt = np.arange(n) / SR; s = np.zeros(n)
    for h, a in enumerate([1, 0.5, 0.28, 0.16, 0.1, 0.06], 1):
        s += a * np.sin(2 * np.pi * freq * h * (1 + 0.0004 * h * h) * tt) * np.exp(-tt * (1.3 + h * 0.7))
    return s * np.minimum(1, tt / 0.004)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
ev = json.load(open('events.json'))
run = next(e for e in ev if e['k'] == 'runout')
t = 0.12
while t < run['t']:  # projector: irregularly spaced, faint click
    add(click(0.05 + 0.02 * rs.random(), 1500 + 400 * rs.random()), t); t += 1 / 24 + rs.normal(0, 0.0015)
for e in ev:
    k, t = e['k'], e['t']
    if k == 'pop': n = int(SR / 30); add(np.sin(2 * np.pi * 1000 * np.arange(n) / SR), t, 0.35)
    elif k == 'motif':  # a brisk, rising newsreel fanfare on the piano
        for m, dt in [(67, 0), (72, 0.22), (76, 0.44), (79, 0.66), (77, 1.05), (76, 1.3)]: add(piano(nt(m)), t + dt, 0.18)
        add(piano(nt(48), 3), t, 0.16); add(piano(nt(55), 3), t + 0.66, 0.12)
    elif k == 'splice': add(thump(90, 0.03, 0.12), t, 0.3); add(click(0.3, 1200, 0.005), t)
    elif k == 'cough':  # engine catches for one bang, then dies back
        add(thump(55, 0.08, 0.4), t, 0.55); add(burst(0.3, 0.07, 0.6), t, 0.3)
        add(thump(60, 0.05, 0.3), t + 0.16, 0.25)
    elif k == 'engine':  # radial engine: firing pulses from a slow chug up to a steady roar
        a, b, end = e['a'], e['b'], e['e']
        tt = a
        while tt < end:
            u = min(1, max(0, (tt - a) / (b - a)))
            rate = 5 + 50 * u * u
            g = (0.18 + 0.2 * u) * min(1, (end - tt) / 0.05)
            add(thump(48 + 30 * u, 0.012 + 0.02 * (1 - u), 0.06), tt, g); add(burst(0.03, 0.008, 0.3), tt, g * 0.5)
            tt += 1 / rate * (1 + rs.normal(0, 0.03))
        # propeller whoosh: noise swelling with the spin-up
        n = int((end - a) * SR); ts = np.arange(n) / SR + a
        env = np.clip((ts - a) / (b - a), 0, 1) ** 2 * np.clip((end - ts) / 0.05, 0, 1)
        z = rs.normal(0, 1, n); z = np.convolve(z, np.ones(24) / 24, mode='same')
        add(z * env * (1 + 0.3 * np.sin(2 * np.pi * 36 * ts)), a, 0.5)
    elif k == 'slip':
        for i in range(7): add(click(0.25, 900, 0.006), t + i * 0.032)
    elif k == 'chord':
        for i, m in enumerate([62, 66, 69, 74]): add(piano(nt(m), 2.5), t + i * 0.06, 0.14)
        add(piano(nt(38), 3), t, 0.18)
    elif k == 'low':  # closing cadence
        for i, m in enumerate([60, 64, 67, 72]): add(piano(nt(m), 2.2), t + i * 0.09, 0.15)
        add(piano(nt(36), 2.5), t, 0.2)
    elif k == 'runout':  # loose film tail slapping the reel, slowing as the motor winds down
        tt, end = t, e['e'] - 0.1
        while tt < end:
            u = (tt - t) / (end - t)
            add(click(0.3 * (1 - 0.7 * u), 700 + 300 * rs.random(), 0.007), tt)
            tt += 1 / (24 - 14 * u)
        n = int((end - t) * SR); ts = np.arange(n) / SR
        add(np.sin(2 * np.pi * np.cumsum(120 - 70 * ts / ts[-1]) / SR) * (1 - ts / ts[-1]), t, 0.06)
# legacy optical audio: band limited
def onepole(x, fc, hp=False):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); p = 0.0
    for i in range(len(x)): p = (1 - a) * x[i] + a * p; y[i] = p
    return x - y if hp else y
out = onepole(onepole(out, 4200), 90, hp=True)
fade = np.ones(N); fade[-int(0.25 * SR):] = np.linspace(1, 0, int(0.25 * SR)); out *= fade
out = np.tanh(out * 1.3) * 0.85
pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes()); w.close()
print('audio.wav ok')
