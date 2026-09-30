# events.json → audio.wav (48 kHz stereo, 10 s)
# terminal: mechanical key clicks, enter thunks, log ticks, progress blips, error buzz,
# success chime, roll-up whirr, steam hiss, CRT power-on thump / power-off whine, faint flyback hum.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(17)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; y = np.fft.irfft(X, len(x)); return y / (np.abs(y).max() + 1e-9)
def tt(d): return np.arange(int(d * SR)) / SR
def env(t, a, d): return np.minimum(1, t / a) * np.exp(-t / d)
def key():
    t = tt(0.06); return 0.6 * band(rs.standard_normal(len(t)), 1800, 6500) * env(t, 3e-4, 0.006) + 0.5 * np.sin(2 * np.pi * (165 + 30 * rs.random()) * t) * env(t, 1e-3, 0.012)
def enter():
    t = tt(0.1); return 0.7 * band(rs.standard_normal(len(t)), 1200, 5000) * env(t, 3e-4, 0.01) + 0.8 * np.sin(2 * np.pi * 115 * t) * env(t, 1e-3, 0.025)
def tick():
    t = tt(0.02); return band(rs.standard_normal(len(t)), 2500, 8000) * env(t, 2e-4, 0.003)
def beep(f, d, harm=((1, 1), (3, .18), (5, .06))):
    t = tt(d); e = np.minimum(1, t / 0.004) * np.minimum(1, (d - t) / 0.02)
    return sum(a * np.sin(2 * np.pi * f * k * t) for k, a in harm) * e
def square(f, d):
    t = tt(d); e = np.minimum(1, t / 0.005) * np.minimum(1, (d - t) / 0.03)
    return np.tanh(4 * np.sin(2 * np.pi * f * t)) * e * (0.8 + 0.2 * np.sin(2 * np.pi * 30 * t))
# bed: faint 15.7 kHz flyback whine is too harsh; use low mains hum + soft room noise
t = np.arange(N) / SR
hum = (np.sin(2 * np.pi * 60 * t) + .35 * np.sin(2 * np.pi * 120 * t) + .12 * np.sin(2 * np.pi * 180 * t))
bed = np.clip((t - 0.05) / 0.4, 0, 1)
room = band(rs.standard_normal(N), 150, 2500)
ev = json.load(open('events.json'))
off = next(e['t'] for e in ev if e['k'] == 'off')
bed *= np.clip((off + 0.2 - t) / 0.3, 0, 1)
L += (hum * 0.010 + room * 0.004) * bed; R += (hum * 0.010 + np.roll(room, 911) * 0.004) * bed
for e in ev:
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'key': add(key(), te + rs.uniform(0, .006), 0.17 * v, rs.uniform(-.15, .15))
    elif k == 'enter': add(enter(), te, 0.26)
    elif k == 'tick': add(tick(), te, 0.06, rs.uniform(-.3, .3))
    elif k == 'blip': add(beep(900 + 700 * v, 0.018, ((1, 1),)), te, 0.025)
    elif k == 'error':
        add(square(110, 0.32), te, 0.09); add(square(82, 0.32), te + 0.34, 0.09)
        add(band(rs.standard_normal(int(0.3 * SR)), 300, 6000) * np.exp(-tt(0.3) / 0.08), te, 0.08)
    elif k == 'success':
        for i, f in enumerate([880, 1175, 1760]): add(beep(f, 0.12), te + i * 0.09, 0.08)
    elif k == 'roll':
        d = 0.22; n = int(d * SR); x = band(rs.standard_normal(n), 800, 6000)
        am = (np.sin(2 * np.pi * 60 * tt(d)) > 0.3) * np.sin(np.pi * tt(d) / d); add(x * am, te, 0.07)
    elif k == 'hiss':
        d = e['d']; x = band(rs.standard_normal(int(d * SR)), 3000, 11000); tx = tt(d)
        am = np.minimum(1, tx / 0.4) * np.minimum(1, (d - tx) / 0.15) * (0.7 + 0.3 * np.sin(2 * np.pi * 2.3 * tx))
        add(x * am, te, 0.022, -.2); add(np.roll(x, 3001) * am, te, 0.022, .2)
    elif k == 'on':
        tx = tt(0.5); add(np.sin(2 * np.pi * 50 * tx) * env(tx, 0.004, 0.16) + 0.3 * band(rs.standard_normal(len(tx)), 300, 4000) * env(tx, 5e-4, 0.03), te, 0.35)
    elif k == 'off':
        tx = tt(0.5); f = 1000 * np.exp(-tx * 9) + 80
        add(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(tx, 0.003, 0.14) + 0.5 * np.sin(2 * np.pi * 45 * tx) * env(tx, 0.003, 0.12), te, 0.2)
fi = int(0.02 * SR); fo = int(0.3 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo)
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
