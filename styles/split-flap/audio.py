# events.json → audio.wav (48 kHz stereo, 10 s)
# split-flap clatter: every flap landing is a short plastic tick + wooden body knock (panned by board position),
# heavier knocks for the wide status flaps, tiny ticks for the header clock; relay/motor hum while the drums spin,
# concourse room tone, zoom whooshes, a three-note terminal chime before the headline and a warm closing tone.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(48)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def flap(size=1.0):
    t = tt(0.05)
    tick = norm(band(rs.standard_normal(len(t)), 2200, 9000)) * np.exp(-t / 0.0016)
    f = (1300 + 500 * rs.random()) / size
    body = np.sin(2 * np.pi * f * t) * np.exp(-t / (0.006 * size))
    knock = np.sin(2 * np.pi * (180 / size) * t) * np.exp(-t / (0.01 * size))
    return 0.8 * tick + 0.35 * body + 0.3 * knock * size
V_MAIN = [flap(1.0) for _ in range(12)]; V_STAT = [flap(1.9) for _ in range(6)]; V_CLK = [flap(0.8) for _ in range(4)]
def whoosh(d):
    t = tt(d); x = rs.standard_normal(len(t)); y = np.zeros_like(x); p = 0.0
    fc = 150 + 1800 * np.sin(np.pi * t / d) ** 2; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
def bell(freq, d):
    t = tt(d); s = np.zeros_like(t)
    for h, a, dec in [(1, 1, 1.4), (2.0, .35, .7), (3.01, .18, .4), (4.2, .08, .25)]: s += a * np.sin(2 * np.pi * freq * h * t) * np.exp(-t / dec)
    return s * np.minimum(1, t / 0.004)
def tone(freq, d, att=0.3, rel=1.2):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in [(1, 1), (2, .25), (3, .08)])
    return s * np.minimum(1, t / att) * np.minimum(1, (d - t) / rel)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
ev = json.load(open('events.json'))
t = np.arange(N) / SR
# room tone: soft concourse air
room = norm(band(rs.standard_normal(N), 80, 1800)); L += room * .012; R += np.roll(room, 5311) * .012
# motor/relay hum follows the flap density
dens = np.zeros(N)
for e in ev:
    if e['k'] == 'flap': i = int(e['t'] * SR); dens[i:i + 1] += 1
kern = np.hanning(int(0.12 * SR)); dens = np.convolve(dens, kern / kern.sum() * SR / 400, 'same'); dens = np.clip(dens, 0, 1.2)
hum = (np.sin(2 * np.pi * 100 * t) + .5 * np.sin(2 * np.pi * 200 * t) + .25 * np.sin(2 * np.pi * 300 * t))
hum = hum + 0.3 * norm(band(rs.standard_normal(N), 300, 900))
L += hum * dens * 0.02; R += hum * dens * 0.02
for e in ev:
    k, te = e['k'], e['t']; pan = e.get('pan', 0.0)
    te += rs.uniform(0, 0.004)
    if k == 'flap': add(V_MAIN[rs.integers(12)], te, 0.075 * (0.7 + 0.6 * rs.random()), pan)
    elif k == 'sflap': add(V_STAT[rs.integers(6)], te, 0.2, pan)
    elif k == 'cflap': add(V_CLK[rs.integers(4)], te, 0.14, 0.5)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.09)
    elif k == 'chime':
        for i, m in enumerate([76, 72, 79]): add(bell(nt(m), 2.2), te + i * 0.26, 0.09, [-.2, .2, 0][i])
    elif k == 'tone':
        for i, m in enumerate([48, 55, 60, 64, 67]): add(tone(nt(m), 1.8, 0.1 + i * .04, 1.1), te + i * 0.03, 0.035 if m > 50 else 0.06)
    elif k == 'power':
        tp = tt(0.5); add(np.sin(2 * np.pi * np.cumsum(40 + 80 * tp / 0.5) / SR) * np.sin(np.pi * tp / 0.5), te, 0.05)
fi = int(0.05 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', len(ev), 'events, peak', np.abs(st).max().round(3), 'rms', np.sqrt((st ** 2).mean()).round(3))
