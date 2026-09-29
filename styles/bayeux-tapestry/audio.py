# events.json → audio.wav (48 kHz stereo, 10 s)
# linen rustle and a wooden rod rumble as the strip unrolls and rolls up, needle punctures and thread draws while each
# caption is stitched, soft hoof clops on earth, the sea washing under the ships with timber creaks, a frame drum and
# cup knocks at the feast, over a quiet two-note fiddle drone and plucked-harp phrases in D dorian.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(98)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)

def rustle(d):   # linen sliding over a roll
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 700, 7000))
    am = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * 3.1 * t + rs.uniform(0, 6))) ** 2
    rum = norm(band(rs.standard_normal(len(t)), 60, 300)) * 0.6
    return (n * am + rum) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.8
def harp(f, d=2.0, bright=0.5):   # Karplus-Strong plucked string
    n = int(d * SR); p = max(2, int(SR / f)); buf = rs.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]; j = (i + 1) % p
        buf[i % p] = 0.5 * (buf[i % p] + buf[j]) * (0.993 + 0.005 * bright)
    return out * np.minimum(1, np.arange(n) / 60)
def drone(d, f0):   # bowed, slightly buzzy fiddle drone
    t = tt(d); ph = 2 * np.pi * f0 * t + 0.02 * np.sin(2 * np.pi * 5 * t)
    s = sum(np.sin(k * ph) / k ** 1.3 for k in range(1, 9))
    s = band(s, 70, 2500) * (1 + 0.1 * np.sin(2 * np.pi * 0.35 * t)); env = np.clip(t / 1.5, 0, 1) * np.clip((d - t) / 1.2, 0, 1)
    return norm(s) * env
def prick():   # needle through linen
    t = tt(0.03); return band(rs.standard_normal(len(t)), 2500, 12000) * np.exp(-t / 0.004)
def draw_thread(d=0.28):   # thread pulled through: rising hiss
    t = tt(d); n = band(rs.standard_normal(len(t)), 1800, 9000); return norm(n) * np.sin(np.pi * t / d) ** 2 * (0.5 + t / d)
def clop():
    t = tt(0.12); return np.sin(2 * np.pi * (180 + 90 * np.exp(-t * 40)) * t) * np.exp(-t / 0.025) + 0.4 * band(rs.standard_normal(len(t)), 300, 2500) * np.exp(-t / 0.01)
def creak(d=0.5):
    t = tt(d); f = 140 + 40 * np.sin(2 * np.pi * 1.3 * t) + 8 * rs.standard_normal(len(t)).cumsum() / np.sqrt(len(t))
    ph = 2 * np.pi * np.cumsum(f) / SR; s = np.sign(np.sin(ph)) * (0.6 + 0.4 * rs.random(len(t)))
    return norm(band(s, 200, 2600)) * np.sin(np.pi * t / d) ** 1.5
def drum():   # frame drum
    t = tt(0.4); return np.sin(2 * np.pi * (95 + 30 * np.exp(-t * 25)) * t) * np.exp(-t / 0.13) + 0.25 * band(rs.standard_normal(len(t)), 150, 1500) * np.exp(-t / 0.02)
def knock():   # wooden cup set down / raised together
    t = tt(0.2); s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / dd) for f, dd in [(620, 0.05), (1180, 0.03), (1730, 0.02)])
    return s + 0.3 * band(rs.standard_normal(len(t)), 800, 5000) * np.exp(-t / 0.008)
def thunk():
    t = tt(0.35); return np.sin(2 * np.pi * (110 + 50 * np.exp(-t * 30)) * t) * np.exp(-t / 0.08) + 0.3 * band(rs.standard_normal(len(t)), 200, 1800) * np.exp(-t / 0.02)

ev = json.load(open('events.json'))
t = np.arange(N) / SR
# drone bed D3 + A3
add(drone(9.6, nt(50)), 0.2, 0.045, -0.2); add(drone(9.0, nt(57)), 0.8, 0.03, 0.25)
# sea: swells under the crossing, drifting left→right with the camera
sea = [e for e in ev if e['k'] == 'sea'][0]; s0, s1 = sea['t'], sea['t'] + sea['d']
wa = norm(band(rs.standard_normal(N), 150, 1400)); wb = norm(band(rs.standard_normal(N), 150, 1400))
sw = (0.6 + 0.4 * np.sin(2 * np.pi * 0.42 * t)) * np.clip((t - s0) / 0.9, 0, 1) * np.clip((s1 - t) / 0.9, 0, 1) * 0.07
pn = np.clip((t - s0) / (s1 - s0), 0, 1)
L += wa * sw * (1.1 - pn * 0.6); R += wb * sw * (0.5 + pn * 0.6)
tunes = [[62, 65, 69, 67, 69, 72, 69], [69, 67, 65, 64, 62, 64, 65], [74, 72, 69, 71, 72, 69, 74]]
ci = 0
for e in ev:
    k, te = e['k'], e['t']
    if k in ('unroll', 'rollup'): add(rustle(e['d'] + 0.2), te, 0.12, 0.5 if k == 'unroll' else -0.2)
    elif k == 'thunk': add(thunk(), te - 0.05, 0.3, -0.5)
    elif k == 'cap':
        d = e['d']; n = int(d * 11)
        for i in range(n): add(prick(), te + i / 11 + rs.uniform(-0.015, 0.015), 0.07, 0.35)
        for i in range(int(d / 0.42)): add(draw_thread(), te + 0.2 + i * 0.42, 0.035, 0.45)
        tn = tunes[ci % 3]; ci += 1
        for i, m in enumerate(tn): add(harp(nt(m), 1.8), te + i * d / len(tn), 0.12, -0.35 + i * 0.1)
    elif k == 'pull': add(draw_thread(0.45), te, 0.05, 0.55)
    elif k == 'hoof': add(clop(), te, 0.05 * np.clip((3.2 - te) / 1.2, 0, 1), -0.1 - te * 0.15)
    elif k == 'point': add(harp(nt(57), 2.0), te, 0.1, -0.4)
    elif k == 'creak': add(creak(0.55), te, 0.035, 0.1)
    elif k == 'toast': add(knock(), te, 0.09, -0.3 + 0.2 * (te - 7.3)); add(harp(nt([69, 72, 74, 77][min(3, int(round((te - 7.45) / 0.25)))]), 1.5), te, 0.07, 0.2)
    elif k == 'serve': add(knock(), te, 0.05, -0.5)
    elif k == 'fade':
        for i, m in enumerate([69, 67, 65, 64, 62]): add(harp(nt(m), 2.4), te - 0.6 + i * 0.16, 0.11, 0.3 - i * 0.15)
        add(harp(nt(50), 2.6), te + 0.25, 0.14, 0.0)
# frame drum through the feast
for i, tb in enumerate(np.arange(6.6, 9.0, 0.3)):
    add(drum(), tb, (0.12 if i % 4 == 0 else 0.06) * np.clip((9.0 - tb) / 0.8, 0, 1), -0.05)
fi = int(0.25 * SR); fo = int(0.9 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.6
st = np.stack([L, R], 1); st = np.tanh(st * 2.2) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
