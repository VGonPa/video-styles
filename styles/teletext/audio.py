# events.json → audio.wav (48 kHz stereo, 10 s)
# easy-listening electric-piano bed (the kind that played under teletext pages), CRT power-on thump + static,
# remote-control clicks, soft data ticks as rows arrive, header-search flutter, temperature blips, CRT switch-off zap.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(118)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def epiano(f, d):
    t = tt(d); mod = np.sin(2 * np.pi * f * 1.0 * t) * (1.6 * np.exp(-t / 0.25) + 0.25)
    s = np.sin(2 * np.pi * f * t + mod) + 0.25 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / 0.4)
    return s * np.exp(-t / 1.1) * np.minimum(1, t / 0.004) * np.minimum(1, (d - t) / 0.08)
def bass(f, d):
    t = tt(d); s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    return s * np.exp(-t / 0.6) * np.minimum(1, t / 0.006) * np.minimum(1, (d - t) / 0.05)
def click(bright=1.0):
    t = tt(0.03); n = band(rs.standard_normal(len(t)), 1500, 9000) * np.exp(-t / 0.0022)
    b = np.sin(2 * np.pi * 900 * t) * np.exp(-t / 0.004)
    return (n / (np.abs(n).max() + 1e-9) + 0.4 * b) * bright
def tick():
    t = tt(0.012); return np.sin(2 * np.pi * 3200 * t) * np.exp(-t / 0.0018)
def blip(f):
    t = tt(0.11); return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.035) * np.minimum(1, t / 0.002)
# music bed: 96 bpm, Fmaj7 | Em7 | Dm7 | G7sus-G7 (two bars per chord would be too slow; one chord per bar)
beat = 60 / 96; bar = 4 * beat
prog = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [55, 59, 62, 65]]
roots = [41, 40, 38, 43]
t0 = 0.25; k = 0; tb = t0
while tb < 9.6:
    ch = prog[k % 4]
    for hit, dur in [(0, 1.4), (1.5, 0.45), (2.5, 1.3)]:
        for j, m in enumerate(ch): add(epiano(nt(m + 12), dur * beat + 0.3), tb + hit * beat + j * 0.012, 0.028, -0.25 + j * 0.17)
    add(bass(nt(roots[k % 4]), 1.8 * beat), tb, 0.10); add(bass(nt(roots[k % 4] + 7), 0.9 * beat), tb + 2.5 * beat, 0.07)
    for h in range(8):                                    # soft brushed hats
        n = band(rs.standard_normal(int(0.05 * SR)), 5000, 12000) * np.exp(-tt(0.05) / (0.012 if h % 2 else 0.02))
        add(n, tb + h * beat / 2, 0.012 if h % 2 else 0.02, 0.3)
    tb += bar; k += 1
# room tone: mains hum + a whisper of line whine
t = np.arange(N) / SR
hum = np.sin(2 * np.pi * 50 * t) + .35 * np.sin(2 * np.pi * 100 * t) + .12 * np.sin(2 * np.pi * 150 * t)
L += hum * 0.006; R += hum * 0.006
wh = np.sin(2 * np.pi * 15625 * t) * 0.0025; L += wh; R += wh
for e in json.load(open('events.json')):
    kk, te, v = e['k'], e['t'], e.get('v', 1.0)
    if kk == 'on':
        tq = tt(0.6); thump = np.sin(2 * np.pi * (70 + 60 * np.exp(-tq * 20)) * tq) * np.exp(-tq / 0.12)
        st = band(rs.standard_normal(len(tq)), 800, 9000) * np.exp(-tq / 0.18)
        add(thump, te, 0.5); add(st / (np.abs(st).max() + 1e-9), te, 0.08)
    elif kk == 'key': add(click(v), te, 0.35, 0.15)
    elif kk == 'search':
        d = e['d']; tq = tt(d); fl = band(rs.standard_normal(len(tq)), 2000, 6000) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 30 * tq)))
        add(fl / (np.abs(fl).max() + 1e-9) * np.sin(np.pi * tq / d) ** 0.5, te, 0.018)
    elif kk == 'load':
        for r in range(24): add(tick(), te + r * e['d'] / 24, 0.035 * (0.7 + 0.3 * rs.random()), rs.uniform(-.4, .4))
    elif kk == 'blip': add(blip(nt(76 + [0, 3, 5, 7, 10][int(v)])), te, 0.07, -0.3 + 0.15 * v)
    elif kk == 'off':
        # music and hum die with the tube, then the collapse zap and relay click
        i0 = int(te * SR); ramp = np.clip(1 - (np.arange(N - i0) / SR) / 0.35, 0, 1); L[i0:] *= ramp; R[i0:] *= ramp
        tq = tt(0.5); f = 1800 * np.exp(-tq * 9) + 60; zap = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tq / 0.15)
        add(zap, te, 0.14); add(click(), te + 0.02, 0.25)
fi = int(0.05 * SR); fo = int(0.3 * SR)
for c in (L, R): c[:fi] *= np.linspace(0, 1, fi); c[-fo:] *= np.linspace(1, 0, fo)
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
