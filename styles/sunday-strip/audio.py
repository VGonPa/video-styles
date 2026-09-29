# events.json → audio.wav (48 kHz stereo, 10 s)
# newspaper rustle, wet-brush swishes as each panel soaks in (with a soft glockenspiel note), balloon pops,
# then the imagination tier: a warm string swell, Cretaceous air (wind, insects, strange bird calls), a volcanic
# rumble and a big roar. SNAP: everything cuts to a quiet kitchen (room tone, wall-clock ticks), a fork clink,
# and a dry two-note sign-off as the page pulls back.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(88)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def rustle(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 900, 9000)
    am = np.abs(band(rs.standard_normal(len(t)), 4, 40)); am = norm(am) ** 1.5
    return norm(n) * am * np.sin(np.pi * t / d) ** 0.8
def swish(d):   # wet brush dragged over paper
    t = tt(d); n = band(rs.standard_normal(len(t)), 300, 4000)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5
    return norm(n) * env * (0.7 + 0.3 * np.sin(2 * np.pi * 6 * t))
def glock(f, d=1.4):
    t = tt(d); s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.08)
    return s * np.exp(-t / 0.5) * np.minimum(1, t / 0.002)
def pop():
    t = tt(0.12); f = 480 * np.exp(-t * 30) + 280; ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.03)
def pad(d, notes):  # soft string swell (detuned saws, low-passed)
    t = tt(d); s = np.zeros(len(t))
    for m in notes:
        for dt in (-0.12, 0.0, 0.13):
            f = nt(m + dt); s += ((t * f) % 1.0 - 0.5)
    s = band(s, 60, 2400); env = np.clip(t / (d * 0.55), 0, 1) ** 1.6
    return norm(s) * env
def chirp(f0, f1, d):
    t = tt(d); f = np.linspace(f0, f1, len(t)) + 180 * np.sin(2 * np.pi * 28 * t); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.sin(np.pi * t / d) ** 2
def roar(d=1.1):
    t = tt(d); f = 70 + 40 * np.sin(np.pi * t / d) + 8 * np.sin(2 * np.pi * 9 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR; g = np.sign(np.sin(ph)) * 0.5 + np.sin(ph * 2) * 0.3 + np.sin(ph * 3.01) * 0.2
    n = band(rs.standard_normal(len(t)), 150, 2200) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 13 * t)))
    env = np.minimum(1, t / 0.08) * np.exp(-np.maximum(0, t - 0.5) / 0.25)
    return (0.6 * band(g, 40, 1600) + 0.5 * norm(n)) * env
def rumble(d):
    t = tt(d); n = band(rs.standard_normal(len(t)), 25, 120); return norm(n) * np.sin(np.pi * t / d)
def snap():
    t = tt(0.06); n = band(rs.standard_normal(len(t)), 1500, 12000) * np.exp(-t / 0.004)
    return norm(n) + 0.5 * np.sin(2 * np.pi * 1600 * t) * np.exp(-t / 0.01)
def tick():
    t = tt(0.04); n = band(rs.standard_normal(len(t)), 2500, 9000) * np.exp(-t / 0.002)
    return norm(n) + 0.3 * np.sin(2 * np.pi * 3300 * t) * np.exp(-t / 0.005)
def clink():
    t = tt(0.5); s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / dcy) for f, dcy in ((2630, 0.12), (3920, 0.08), (5210, 0.05)))
    return s * np.minimum(1, t / 0.001)
def piano(f, d=2.0):
    t = tt(d); s = sum(np.sin(2 * np.pi * f * k * t) / k ** 1.4 * np.exp(-t * (1.2 + k * 0.6)) for k in range(1, 6))
    return s * np.minimum(1, t / 0.004)

ev = json.load(open('events.json'))
E = {e['k']: e for e in ev}
t_snap = E['snap']['t']
# ambience beds, gated by section
t = np.arange(N) / SR
room = norm(band(rs.standard_normal(N), 80, 900)); room2 = norm(band(rs.standard_normal(N), 80, 900))
fridge = np.sin(2 * np.pi * 58 * t) + 0.4 * np.sin(2 * np.pi * 116 * t)
jf = E['jungle']; j0, j1 = jf['t'], jf['t'] + jf['d']
jgate = np.clip((t - j0) / 0.6, 0, 1) * (t < j1)
kgate = np.where(t < j0, 1.0, 0.0) * np.clip(1 - (t - (j0 - 0.4)) / 0.4, 0, 1) + (t >= t_snap)
wind = norm(band(rs.standard_normal(N), 150, 1400)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.3 * t))
insect = norm(band(rs.standard_normal(N), 5200, 7800)) * (0.5 + 0.5 * np.sin(2 * np.pi * 31 * t)) ** 2
L += room * 0.02 * kgate + fridge * 0.003 * kgate + wind * 0.05 * jgate + insect * 0.012 * jgate
R += room2 * 0.02 * kgate + fridge * 0.003 * kgate + wind[::-1] * 0.05 * jgate + insect * 0.010 * jgate
# Cretaceous birds
bt = j0 + 0.3
while bt < j1 - 0.2:
    f0 = rs.uniform(1400, 2600); add(chirp(f0, f0 * rs.uniform(0.6, 1.4), rs.uniform(0.12, 0.3)), bt, 0.05, rs.uniform(-0.8, 0.8)); bt += rs.uniform(0.25, 0.6)
add(rumble(j1 - j0), j0, 0.10)
# glockenspiel motif, one note per panel as it soaks in (G major, rising)
motif = [67, 71, 74, 79, 76]
wi = 0
for e in ev:
    k, te = e['k'], e['t']
    if k == 'rustle': add(rustle(e['d']), te, 0.10, 0.1)
    elif k == 'wash':
        add(swish(e['d']), te, 0.10, -0.2 + 0.1 * wi)
        add(glock(nt(motif[wi % len(motif)])), te + 0.05, 0.07, -0.3 + 0.15 * wi); wi += 1
    elif k == 'pop': add(pop(), te, 0.14)
    elif k == 'glide': add(swish(e['d']), te, 0.06, 0.3)
    elif k == 'swell':
        p = pad(t_snap - te, [55, 62, 67, 71, 74]); add(p, te, 0.10, 0.0)
    elif k == 'roar': add(roar(), te, 0.34, 0.15)
    elif k == 'snap': add(snap(), te, 0.35, 0.0)
    elif k == 'blink': add(clink(), te + 0.5, 0.05, 0.25)
    elif k == 'chord':
        add(piano(nt(67)), te, 0.12, -0.15); add(piano(nt(71)), te + 0.2, 0.10, 0.1); add(piano(nt(74)), te + 0.4, 0.08, 0.2)
# hard cut: silence everything from the fantasy at the snap (keep the snap itself)
cut = int(t_snap * SR); fade = int(0.012 * SR)
for ch in (L, R):
    ch[cut:cut + fade] *= np.linspace(1, 0, fade); ch[cut + fade:] = 0
# re-add what belongs to the kitchen after the snap
L += room * 0.02 * (t >= t_snap) + fridge * 0.003 * (t >= t_snap); R += room2 * 0.02 * (t >= t_snap) + fridge * 0.003 * (t >= t_snap)
add(snap(), t_snap, 0.35)
for s in np.arange(np.ceil(t_snap * 2) / 2, DUR - 0.2, 0.5): add(tick(), s, 0.05, -0.4)
for e in ev:
    if e['t'] >= t_snap:
        k, te = e['k'], e['t']
        if k == 'wash': add(swish(e['d']), te, 0.10, 0.2); add(glock(nt(76)), te + 0.05, 0.07, 0.2)
        elif k == 'pop': add(pop(), te, 0.14)
        elif k == 'blink': add(clink(), te + 0.5, 0.05, 0.25)
        elif k == 'rustle': add(rustle(e['d']), te, 0.10, 0.1)
        elif k == 'chord': add(piano(nt(67)), te, 0.12, -0.15); add(piano(nt(71)), te + 0.2, 0.10, 0.1); add(piano(nt(74)), te + 0.4, 0.08, 0.2)
fi = int(0.3 * SR); fo = int(0.5 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.4) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
