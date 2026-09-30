# events.json → audio.wav (48 kHz stereo, 10 s)
# chalk scratches for lines and handwriting, chalk taps for counted cells, board knocks for totals,
# eraser thud + felt rubbing, a soft dust puff, quiet classroom room tone.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(6)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def chalk(d):
    # gritty scratch: band noise gated by random grain pulses, faint squeak, soft attack/release
    t = tt(d + 0.03); n = norm(band(rs.standard_normal(len(t)), 1400, 7500))
    grit = np.abs(band(rs.standard_normal(len(t)), 30, 140)); grit = norm(grit) ** 1.6
    sq = np.sin(2 * np.pi * np.cumsum(3100 + 400 * np.sin(2 * np.pi * 5 * t)) / SR) * 0.06
    env = np.minimum(1, t / 0.008) * np.clip((d + 0.03 - t) / 0.03, 0, 1)
    return (n * (0.35 + 0.65 * grit) + sq) * env
def write(d, n):
    # handwriting: one short scratch per letter with tiny pauses between
    out = np.zeros(int((d + 0.05) * SR)); n = max(1, n)
    for i in range(n):
        s = chalk(d / n * (0.55 + 0.3 * rs.random())); j = int(i * d / n * SR)
        m = min(len(s), len(out) - j); out[j:j + m] += s[:m] * (0.7 + 0.3 * rs.random())
    return out
def tap():
    t = tt(0.05); c = norm(band(rs.standard_normal(len(t)), 2000, 9000)) * np.exp(-t / 0.004)
    return c + 0.5 * np.sin(2 * np.pi * (850 + 150 * rs.random()) * t) * np.exp(-t / 0.01)
def knock():
    t = tt(0.3); f = 180 * np.exp(-t * 10) + 120
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05) + 0.3 * norm(band(rs.standard_normal(len(t)), 1500, 6000)) * np.exp(-t / 0.006)
def thud():
    t = tt(0.35); return np.sin(2 * np.pi * 85 * t) * np.exp(-t / 0.06) + 0.5 * norm(band(rs.standard_normal(len(t)), 200, 2500)) * np.exp(-t / 0.03)
def erase(d):
    # felt rubbing: low band noise, loud on each up/down pass, quiet at the turns
    t = tt(d); n = norm(band(rs.standard_normal(len(t)), 150, 1800)) + 0.3 * norm(band(rs.standard_normal(len(t)), 2500, 6000))
    passes = np.abs(np.sin(np.pi * 4.5 * t / d)) ** 0.6
    return n * (0.25 + 0.75 * passes) * np.minimum(1, t / 0.02) * np.clip((d - t) / 0.06, 0, 1)
def puff():
    t = tt(0.9); n = norm(band(rs.standard_normal(len(t)), 250, 3500))
    return n * np.minimum(1, t / 0.02) * np.exp(-t / 0.22)
# bed: quiet classroom room tone (no music, as on a real board)
t = np.arange(N) / SR
room = norm(band(rs.standard_normal(N), 80, 1200)); L += room * .01; R += np.roll(room, 911) * .01
hum = np.sin(2 * np.pi * 60 * t) + .3 * np.sin(2 * np.pi * 120 * t); L += hum * .004; R += hum * .004
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'chalk': add(chalk(e['d']), te, 0.16 * e.get('v', 1), rs.uniform(-.25, .25))
    elif k == 'write': add(write(e['d'], e['n']), te, 0.17, rs.uniform(-.2, .2))
    elif k == 'tap': add(tap(), te, 0.13, rs.uniform(-.3, .1))
    elif k == 'ding': add(knock(), te, 0.35, -.15)
    elif k == 'thud': add(thud(), te, 0.4, -.3)
    elif k == 'erase': add(erase(e['d']), te, 0.3, -.3)
    elif k == 'puff': add(puff(), te, 0.3, .35); add(tap(), te - 0.01, 0.2, .35)
# master: fade in/out, soft limiter
fi = int(0.2 * SR); fo = int(0.6 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 2.0) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
