# events.json → audio.wav (48 kHz stereo, 10 s)
# craft-knife scratches through paper, chips ticking down, sheet unfolding (rustle + crinkle), soft paper slaps,
# water shimmer for the koi, wooden lantern knocks, and a sparse plucked-zither line on the D major pentatonic
# with a glissando at the unfold and a closing arpeggio. Everything is synthesized; nothing is sampled.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(23)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(max(1, int(d * SR))) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def scratch(d):   # blade dragging through paper: grainy high noise with a stick-slip flutter
    d = max(d, 0.03); t = tt(d); n = norm(band(rs.standard_normal(len(t)), 2200, 9000))
    grain = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * (70 + 40 * rs.random()) * t + rs.random() * 6))
    env = np.minimum(1, t / 0.006) * np.minimum(1, (d - t) / 0.012 + 0.02)
    return n * grain * env
def tick():
    t = tt(0.03); return norm(band(rs.standard_normal(len(t)), 1200, 5000)) * np.exp(-t / 0.005)
def flutter(d=0.5):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 600, 5000))
    am = np.abs(np.sin(2 * np.pi * 13 * t + rs.random() * 3)) ** 3
    return n * am * np.sin(np.pi * t / d) ** 0.8
def rustle(d=0.6):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 700, 8000))
    am = np.abs(band(rs.standard_normal(len(t)), 4, 45)); am = norm(am)
    crk = np.zeros(len(t))
    for _ in range(int(d * 40)): i = rs.integers(0, len(t) - 400); crk[i:i + 300] += norm(band(rs.standard_normal(300), 2500, 9000)) * np.exp(-np.arange(300) / 50) * rs.random()
    return (n * am + 0.6 * crk) * np.sin(np.pi * t / d) ** 0.6
def slap(v=1.0):
    t = tt(0.3); n = norm(band(rs.standard_normal(len(t)), 250, 4500)) * np.exp(-t / 0.03)
    return 0.8 * n + 0.7 * v * np.sin(2 * np.pi * 90 * t) * np.exp(-t / 0.045)
def knock():   # wooden cap of the lantern against its cord
    t = tt(0.35); s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / dcy) for f, a, dcy in [(420, 1, .05), (1130, .4, .025), (2230, .15, .012)])
    return s + 0.3 * norm(band(rs.standard_normal(len(t)), 1500, 6000)) * np.exp(-t / 0.004)
def water(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 300, 2500)); env = np.sin(np.pi * t / d) ** 1.5
    s = n * env * 0.5
    for _ in range(9):   # little bubble plinks
        t0 = rs.random() * d * 0.85; f0 = 900 + rs.random() * 1400; b = tt(0.08); ph = 2 * np.pi * np.cumsum(f0 * (1 + 1.5 * b / 0.08)) / SR
        blip = np.sin(ph) * np.exp(-b / 0.02); i = int(t0 * SR); s[i:i + len(b)] += blip[:len(s) - i] * 0.35
    return s
def pluck(f, d=2.2, bright=0.5):   # Karplus-Strong zither string
    n = int(d * SR); P = max(2, int(SR / f)); buf = rs.uniform(-1, 1, P); buf = buf - buf.mean(); out = np.zeros(n)
    a = 0.5 + bright * 0.49
    for i in range(n): out[i] = buf[i % P]; buf[i % P] = (a * buf[i % P] + (1 - a) * buf[(i + 1) % P]) * 0.9985
    t = tt(d); out *= np.minimum(1, (d - t) / 0.3)
    return out + 0.25 * np.sin(2 * np.pi * f * t) * np.exp(-t / 0.6)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
PENTA = [62, 64, 66, 69, 71, 74, 76, 78, 81, 83, 86]   # D major pentatonic
# bed: a quiet drone (D + A) with slow tremolo
t = np.arange(N) / SR
drone = (np.sin(2 * np.pi * nt(50) * t) + .5 * np.sin(2 * np.pi * nt(57) * t) + .2 * np.sin(2 * np.pi * nt(62) * t)) * (1 + .2 * np.sin(2 * np.pi * .3 * t))
denv = np.clip(t / 1.5, 0, 1) * (0.6 + 0.4 * np.clip((t - 4) / 2, 0, 1))
L += drone * 0.018 * denv; R += drone * 0.018 * denv
room = norm(band(rs.standard_normal(N), 150, 2500)); L += room * .004; R += np.roll(room, 911) * .004
# melody: sparse plucks
for tm, m, g in [(0.35, 62, .16), (1.25, 69, .09), (2.05, 66, .09), (2.75, 71, .08),
                 (4.5, 74, .12), (5.1, 76, .10), (5.7, 78, .10), (6.3, 76, .09), (6.9, 71, .09), (7.6, 74, .11), (8.2, 69, .09), (8.75, 71, .09)]:
    add(pluck(nt(m), 2.4), tm, g, rs.uniform(-.35, .35))
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'cut': add(scratch(e['d']), te, 0.05 + 0.05 * v, rs.uniform(-.25, .35))
    elif k == 'drop':
        add(tick(), te + 0.02, 0.05 + 0.08 * v, rs.uniform(-.3, .3))
        if v > 0.2: add(flutter(0.6), te, 0.12 * v, .3)
    elif k == 'land': add(slap(v), te, 0.22 * v); add(rustle(0.25), te, 0.05)
    elif k == 'unfold':
        add(rustle(e['d'] + 0.2), te, 0.16, -.2)
        for i, m in enumerate(PENTA[:9]): add(pluck(nt(m), 1.8, .6), te + 0.08 + i * 0.07, 0.07 + 0.005 * i, -.4 + i * 0.1)
    elif k == 'swish': add(water(e['d']), te, 0.10, .1); add(water(1.2), te + 1.6, 0.07, -.2)
    elif k == 'lift': add(rustle(0.4), te, 0.06, .2)
    elif k == 'lantern': add(knock(), te, 0.16, -.5 if te < 7.7 else .5); add(rustle(0.3), te + 0.03, 0.04)
    elif k == 'banner': add(rustle(0.45), te, 0.12); add(slap(0.5), te + 0.42, 0.1)
    elif k == 'whoosh':
        d = e['d']; tw = tt(d); n = norm(band(rs.standard_normal(len(tw)), 200, 2200)) * np.sin(np.pi * tw / d) ** 2; add(n, te, 0.05)
    elif k == 'chord':
        for i, m in enumerate([50, 62, 66, 69, 74, 78, 81]): add(pluck(nt(m), 2.2, .45), te + i * 0.06, 0.1 if m > 50 else 0.14, -.3 + i * .1)
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 3.4) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
