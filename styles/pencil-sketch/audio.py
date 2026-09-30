# events.json → audio.wav (48 kHz stereo, 10 s)
# graphite on paper: every stroke is a pencil scratch (tooth-grain noise), hatching flicks, handwriting
# with letter-rate pressure, a quiet room, and a paper rustle as the page corner lifts.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(10)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def norm(x): return x / (np.abs(x).max() + 1e-9)
def tt(d): return np.arange(int(d * SR)) / SR
# one long graphite bed, sliced per stroke: bright scratch + low drag, modulated by paper-tooth grain
BL = 4 * SR
hi = norm(band(rs.standard_normal(BL), 2200, 9000))
lo = norm(band(rs.standard_normal(BL), 350, 1400))
grain = np.abs(band(rs.standard_normal(BL), 30, 260)); grain = 0.35 + 0.65 * norm(grain)
BED = (hi * 0.8 + lo * 0.35) * grain
def scratch(d, sharp=False):
    n = max(int(d * SR), int(0.03 * SR)); o = rs.integers(0, BL - n); s = BED[o:o + n].copy()
    t = np.arange(n) / SR; a = 0.004 if sharp else 0.012; r = 0.012 if sharp else 0.03
    env = np.minimum(1, t / a) * np.minimum(1, (n / SR - t) / r)
    env *= 0.75 + 0.25 * np.sin(np.pi * np.clip(t / (n / SR), 0, 1))          # pressure peaks mid-stroke
    return s * np.clip(env, 0, 1)
def write(d):
    s = scratch(d); t = np.arange(len(s)) / SR
    pulse = 0.35 + 0.65 * np.abs(np.sin(2 * np.pi * (4.5 + 0.6 * np.sin(2 * np.pi * 1.3 * t)) * t)) ** 1.5   # letters
    return s * pulse
def rustle(d):
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 700, 8000))
    am = norm(np.abs(band(rs.standard_normal(len(t)), 4, 35)))
    body = norm(band(rs.standard_normal(len(t)), 120, 600)) * 0.5
    return (n * am + body * am) * np.sin(np.pi * t / d) ** 0.8
# room: very quiet air + a faint low hum of the desk lamp
t = np.arange(N) / SR
room = norm(band(rs.standard_normal(N), 80, 2500)); L += room * .004; R += np.roll(room, 911) * .004
hum = np.sin(2 * np.pi * 60 * t) * .003; L += hum; R += hum
for e in json.load(open('events.json')):
    k, te, v, p = e['k'], e['t'], e.get('v', 1.0), e.get('p', 0.0)
    if k == 'scr':
        d = e['d']; add(scratch(d, sharp=d < 0.13), te + rs.uniform(0, .006), 0.11 * v * (0.8 + .4 * rs.random()), p)
    elif k == 'write': add(write(e['d']), te, 0.16 * min(1.2, v), p)
    elif k == 'lift':
        add(rustle(e["d"] + 0.3), te - 0.05, 0.13, .45)
        tk = tt(0.05); add(norm(band(rs.standard_normal(len(tk)), 1500, 6000)) * np.exp(-tk / 0.008), te, 0.12, .5)   # corner leaves the page
# master: fade in/out, soft limiter
fi = int(0.3 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 5.0) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3), 'rms', np.sqrt((st ** 2).mean()).round(4))
