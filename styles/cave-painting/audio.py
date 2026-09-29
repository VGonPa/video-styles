# events.json → audio.wav (48 kHz stereo, 10 s), all synthesized:
# cave room tone + torch roar/crackle, flint sparks, ignition whoosh, frame-drum hoofbeats with cave echo,
# pigment spray breaths, soft brush dabs, a breathy bone-flute line, water drips, and a dimming drone.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR)
dry = np.zeros((N, 2)); wet = np.zeros((N, 2))
rs = np.random.default_rng(103)
tt = lambda d: np.arange(int(d * SR)) / SR
def add(sig, t, g=1.0, pan=0.0, send=0.35):
    i = int(t * SR); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    l, r = np.sqrt(0.5 - pan / 2) * 1.414, np.sqrt(0.5 + pan / 2) * 1.414
    for bus, gg in ((dry, 1 - send * 0.5), (wet, send)):
        bus[i:i + n, 0] += sig[:n] * g * gg * l; bus[i:i + n, 1] += sig[:n] * g * gg * r
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def nrm(x): return x / (np.abs(x).max() + 1e-9)
def seg(t, a, b): return np.clip((t - a) / (b - a), 0, 1)

t = np.arange(N) / SR
flame = (1 - (1 - seg(t, 0.62, 1.7)) ** 3) * (1 - 0.76 * seg(t, 8.7, 9.85))
# room tone and torch roar
room = nrm(band(rs.standard_normal(N), 40, 400)); dry[:, 0] += room * 0.02; dry[:, 1] += np.roll(room, 911) * 0.02
roar = nrm(band(rs.standard_normal(N), 90, 700)) * (0.8 + 0.4 * nrm(band(rs.standard_normal(N), 2, 12)))
dry[:, 0] += roar * 0.05 * flame; dry[:, 1] += np.roll(roar, 313) * 0.05 * flame
# crackle: sparse pops, denser when the flame is strong
def pop():
    d = tt(0.012 + rs.random() * 0.02); return nrm(band(rs.standard_normal(len(d)), 1500, 9000)) * np.exp(-d / 0.003)
tc = 0.7
while tc < 9.8:
    k = np.interp(tc, t, flame)
    if k > 0.05: add(pop(), tc, 0.12 * k * (0.4 + rs.random()), rs.uniform(-.5, .5), 0.15)
    tc += rs.exponential(1 / 14)
def spark():
    d = tt(0.5); click = nrm(band(rs.standard_normal(len(d)), 2000, 12000)) * np.exp(-d / 0.004)
    ring = np.sin(2 * np.pi * 3150 * d) * np.exp(-d / 0.08) * 0.25 + np.sin(2 * np.pi * 4720 * d) * np.exp(-d / 0.05) * 0.15
    return click + ring
def whoosh(d):
    x = tt(d); s = nrm(band(rs.standard_normal(len(x)), 150, 2500)) * np.sin(np.pi * np.clip(x / d, 0, 1)) ** 1.3
    return s + np.sin(2 * np.pi * (70 - 30 * x / d) * x) * np.exp(-x / 0.25) * 0.8
def drum(f0=95, dec=0.22):
    x = tt(0.6); ph = 2 * np.pi * np.cumsum(f0 * (0.65 + 0.35 * np.exp(-x * 30))) / SR
    return np.sin(ph) * np.exp(-x / dec) + nrm(band(rs.standard_normal(len(x)), 200, 2500)) * np.exp(-x / 0.015) * 0.35
def spray():
    x = tt(0.45); env = np.minimum(1, x / 0.03) * np.exp(-x / 0.14)
    return nrm(band(rs.standard_normal(len(x)), 700, 7000)) * env
def dab():
    x = tt(0.09); return nrm(band(rs.standard_normal(len(x)), 250, 2200)) * np.exp(-x / 0.02)
def flute(m, d):
    f = 440 * 2 ** ((m - 69) / 12); x = tt(d)
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.2 * x) * np.clip(x / 0.4, 0, 1)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    tone = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)
    breath = nrm(band(rs.standard_normal(len(x)), f * 0.8, f * 4)) * 0.22
    env = np.minimum(1, x / 0.18) * np.minimum(1, (d - x) / 0.5) ** 1.5
    return (tone + breath) * env
def drip():
    x = tt(0.2); f = 900 + 1400 * np.exp(-x * 40); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / 0.03)
for td in (2.1, 5.2, 7.9): add(drip(), td, 0.08, rs.uniform(-.7, .7), 0.8)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'spark': add(spark(), te, 0.35, -0.4, 0.4)
    elif k == 'ignite': add(whoosh(0.9), te - 0.1, 0.35, -0.3, 0.3)
    elif k == 'hoof': add(drum(90 + rs.uniform(-8, 8), 0.16), te + rs.uniform(0, 0.01), 0.3 * v, rs.uniform(-.25, .25), 0.45)
    elif k == 'freeze': add(drum(62, 0.5), te, 0.55, 0, 0.6); add(drum(124, 0.2), te + 0.01, 0.2, 0, 0.5)
    elif k == 'puff': add(spray(), te, 0.28, 0.35, 0.4)
    elif k == 'dab': add(dab(), te, 0.1 * v, rs.uniform(-.3, .1), 0.3)
    elif k == 'flute': add(flute(e['m'], e['d']), te, 0.07, 0.15, 0.7)
    elif k == 'dim':
        x = tt(1.3); add(np.sin(2 * np.pi * (55 - 8 * x / 1.3) * x) * np.minimum(1, x / 0.3) * (1 - x / 1.3), te, 0.12, 0, 0.5)
# cave reverb: exponentially decaying noise impulse response (≈1.8 s), FFT convolution
ir_t = tt(1.8); M = N + len(ir_t)
for ch in (0, 1):
    ir = rs.standard_normal(len(ir_t)) * np.exp(-ir_t / 0.45); ir[:int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR)); ir /= np.sqrt((ir ** 2).sum())
    y = np.fft.irfft(np.fft.rfft(wet[:, ch], M) * np.fft.rfft(ir, M), M)[:N]
    dry[:, ch] += y * 0.9
fi, fo = int(0.2 * SR), int(0.7 * SR)
dry[:fi] *= np.linspace(0, 1, fi)[:, None]; dry[-fo:] *= (np.linspace(1, 0, fo) ** 1.5)[:, None]
st = np.tanh(dry * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
