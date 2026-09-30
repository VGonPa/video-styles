# events.json → audio.wav (48 kHz stereo, 9.6 s)
# dry, mechanical poster sounds: grid ticks, type clacks, shape pops/thuds/bloops, a rolling circle,
# the lamp switch click and light-on hum, paper swishes for the bars, a closing major chord.
import json, wave, numpy as np
SR, DUR = 48000, 9.6
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(3)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def tt(d): return np.arange(int(d * SR)) / SR
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def env(n, dec): t = np.arange(n) / SR; return np.minimum(1, t / 0.004) * np.exp(-t / dec)
def sweep(f0, f1, d, dec, shape=np.sin):
    n = int(SR * d); t = np.arange(n) / SR; f = f0 * (f1 / f0) ** (t / d); ph = 2 * np.pi * np.cumsum(f) / SR
    return shape(ph) * env(n, dec)
def gen(e):
    k, f = e['k'], e.get('f')
    if k == 'pop': return sweep(f, f * 0.45, 0.09, 0.03)
    if k == 'blip': return sweep(f, f, 0.12, 0.035)
    if k == 'bloop': return sweep(f, f * 2.4, 0.16, 0.06)
    if k == 'bloopdn': return sweep(f, f * 0.4, 0.2, 0.07)
    if k == 'thud': return sweep(f, f * 0.6, 0.3, 0.09)
    if k == 'tick': return sweep(f, f, 0.03, 0.006)
    if k == 'clack': return sweep(f, f * 0.7, 0.05, 0.012, lambda x: np.sign(np.sin(x)) * 0.5)
    if k == 'chime':
        t = tt(0.9); return (np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*f*1.5*t) + 0.25*np.sin(2*np.pi*f*2.01*t)) / 1.75 * env(len(t), 0.28)
    if k == 'click':  # switch: sharp snap + small body
        t = tt(0.08); n = band(rs.standard_normal(len(t)), 2000, 9000) * np.exp(-t / 0.003)
        return n / (np.abs(n).max() + 1e-9) * 0.8 + sweep(420, 300, 0.08, 0.015)
    if k == 'on':  # light on: soft thump + filament hum that settles
        t = tt(1.4); hum = sum(a * np.sin(2 * np.pi * 100 * h * t) for h, a in [(1, 1), (2, .5), (3, .25)])
        out = hum * 0.18 * np.minimum(1, t / 0.02) * np.exp(-t / 0.5); th = sweep(90, 55, 0.4, 0.12); out[:len(th)] += th * 0.9
        return out
    if k == 'roll':  # circle rolling along the baseline
        d = e['d']; t = tt(d); n = band(rs.standard_normal(len(t)), 150, 900)
        am = 0.6 + 0.4 * np.sin(2 * np.pi * 9 * t) ** 2
        return n / (np.abs(n).max() + 1e-9) * am * np.sin(np.pi * t / d) ** 0.8 * 0.35
    if k == 'swish':
        d = e['d']; t = tt(d); n = band(rs.standard_normal(len(t)), 1200, 7000)
        return n / (np.abs(n).max() + 1e-9) * np.sin(np.pi * t / d) ** 2 * 0.6
    if k == 'chord':
        out = np.zeros(int(2.2 * SR)); t = tt(2.2)
        for i, m in enumerate([60, 64, 67, 72]):
            fr = 440 * 2 ** ((m - 69) / 12); s = np.sin(2 * np.pi * fr * t) + 0.3 * np.sin(4 * np.pi * fr * t)
            out += s * np.minimum(1, t / (0.01 + i * 0.03)) * np.exp(-t / 0.9) * 0.3
        return out
    raise ValueError(k)
for e in json.load(open('events.json')):
    pan = {'clack': rs.uniform(-.3, .3), 'tick': rs.uniform(-.2, .2)}.get(e['k'], 0.0)
    add(gen(e), e['t'], e.get('v', 0.5), pan)
fo = int(0.5 * SR)
for ch in (L, R): ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.tanh(np.stack([L, R], 1) * 1.1) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
