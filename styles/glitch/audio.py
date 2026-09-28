# events.json → audio.wav (48 kHz stereo, 10 s)
# 120 bpm digital bed (minor pad → searching sine → major pad), beat kicks, bitcrushed glitch hits that also crush the bed,
# real audio freezes (the mix itself stutters exactly where the picture freezes), data chirps, pixel-sort sweep,
# datamosh smear, lock-on chord, power-down glitch out into silence.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(54)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def crush(x, bits=4, hold=8):
    y = np.repeat(x[::hold], hold)[:len(x)]; q = 2 ** bits; return np.round(y * q) / q
def sq(f, t): return np.sign(np.sin(2 * np.pi * f * t))
def saw(f, t): return 2 * ((f * t) % 1) - 1
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def kick(v=1):
    t = tt(0.3); f = 45 + 110 * np.exp(-t * 28); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.11) * v + 0.3 * band(rs.standard_normal(len(t)), 2000, 8000) * np.exp(-t / 0.003)
def hat():
    t = tt(0.04); return band(rs.standard_normal(len(t)), 6000, 14000) * np.exp(-t / 0.008)
def hit(d, v):
    t = tt(max(0.06, d)); n = rs.standard_normal(len(t)); ch = sq(180 + 1400 * rs.random() * np.exp(-t * 12), t)
    gate = (np.floor(t * (40 + 60 * rs.random())) % 2 == 0).astype(float) * 0.6 + 0.4
    s = crush(0.6 * n + 0.5 * ch, 3, 6 + int(rs.random() * 20)) * gate * np.exp(-t / (d * 0.6 + .02))
    thump = np.sin(2 * np.pi * np.cumsum(60 + 200 * np.exp(-t * 40)) / SR) * np.exp(-t / 0.08)
    return (s * 0.7 + thump * 0.8 * v)
def blip(f, v=1):
    t = tt(0.05); return crush(sq(f, t) * np.exp(-t / 0.015), 3, 4) * v
def chirp():
    t = tt(0.14); f = np.where(np.floor(t * 90) % 2 == 0, 1200, 2400); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sign(np.sin(ph)) * np.exp(-t / 0.08) * 0.5
def tone(freq, d, att=0.2, rel=0.5, kind='sin'):
    t = tt(d)
    s = np.sin(2 * np.pi * freq * t) + (0.25 * saw(freq * 1.003, t) if kind == 'saw' else 0.2 * np.sin(4 * np.pi * freq * t))
    env = np.minimum(1, t / att) * np.minimum(1, np.maximum(0, (d - t) / rel)); return s * env
def sweep(d):
    t = tt(d); u = t / d; f = 2400 * np.abs(1 - 2 * u) ** 1.5 + 90; ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sign(np.sin(ph)) * 0.4 + 0.6 * band(rs.standard_normal(len(t)), 300, 9000) * np.sin(np.pi * u) ** 2
    return crush(s * np.sin(np.pi * u) ** 0.7, 4, 8)
def ping():
    t = tt(1.2); s = np.sin(2 * np.pi * 1760 * t) * np.exp(-t / 0.18)
    return s + 0.4 * np.roll(s, int(0.21 * SR)) * (np.arange(len(t)) > 0.21 * SR)
def smear(d):
    t = tt(d); u = t / d; out = np.zeros(len(t))
    for k, m in enumerate([45, 52, 57, 64]):
        f = nt(m) * (1 - 0.35 * u) * (1 + 0.004 * k); out += saw(f, t) * 0.25
    hold = (4 + 40 * u ** 1.5).astype(int)
    idx = np.arange(len(t)); idx = idx - idx % np.maximum(1, hold); out = out[idx]
    return band(out, 40, 6000) * np.minimum(1, t / 0.15) * np.minimum(1, (d - t) / 0.05)
def powerdown():
    t = tt(0.85); f = 900 * np.exp(-t * 4.5) + 30; ph = 2 * np.pi * np.cumsum(f) / SR
    s = crush(np.sign(np.sin(ph)) * 0.5 + 0.4 * rs.standard_normal(len(t)) * np.exp(-t * 3), 3, 10)
    return s * np.exp(-t / 0.3) * (np.floor(t * 30) % 3 != 2)
# bed ────────────────────────────────────────────
t = np.arange(N) / SR
bed = np.zeros(N)
def pad(notes, t0, t1, g, kind='saw'):
    s = sum(tone(nt(m), t1 - t0, 0.25, 0.25, kind) for m in notes) * g
    i = int(t0 * SR); bed[i:i + len(s)] += s[:N - i]
pad([45, 57, 60, 64], 0.8, 3.4, 0.05)                    # A minor, the live feed
pad([81], 3.9, 6.3, 0.03, 'sin')                           # thin searching tone
bed[int(3.9 * SR):int(6.3 * SR)] *= 1 + 0.4 * np.sin(2 * np.pi * 7 * t[int(3.9 * SR):int(6.3 * SR)])
pad([45, 57, 61, 64, 69], 7.4, 9.05, 0.05)                 # A major, locked
ev = json.load(open('events.json'))
for e in ev:                                               # every glitch burst also crushes the bed underneath
    if e['k'] == 'hit':
        i0, i1 = int(e['t'] * SR), int((e['t'] + e['d']) * SR); bed[i0:i1] = crush(bed[i0:i1] * 1.4, 3, 24)
L += bed; R += bed
hats = [b + 0.25 for b in np.arange(1.0, 6.2, 0.5)] + [b + 0.25 for b in np.arange(7.5, 8.8, 0.5)]
for h in hats: add(hat(), h, 0.08, 0.3)
for e in ev:
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'kick': add(kick(), te, 0.5 * v)
    elif k == 'hit': add(hit(e['d'], v), te, 0.30 * (0.5 + v), rs.uniform(-.4, .4))
    elif k == 'boot': add(chirp(), te, 0.2 * v, rs.uniform(-.3, .3)); add(blip(3000), te, 0.1)
    elif k == 'blip': add(blip(e['f']), te, 0.13 * v, rs.uniform(-.2, .2))
    elif k == 'sort': add(sweep(e['d']), te, 0.22)
    elif k == 'chan': add(blip(1500), te, 0.12); add(blip(2250), te + 0.05, 0.1)
    elif k == 'ping': add(ping(), te, 0.16, 0.3)
    elif k == 'mosh': add(smear(e['d']), te, 0.35)
    elif k == 'lock':
        for i, m in enumerate([69, 73, 76, 81]): add(tone(nt(m), 1.3, 0.005, 0.9, 'sin') * np.exp(-tt(1.3) / 0.6), te + i * 0.045, 0.07)
        add(kick(), te, 0.55)
    elif k == 'bar': add(blip(e['f']), te, 0.08)
    elif k == 'out': add(powerdown(), te, 0.35)
# freezes: the mix itself sticks on a 1/15 s slice, in lockstep with the picture
def freeze(t0, t1, srcs):
    L0, R0 = L.copy(), R.copy(); sl = int(SR / 15)
    for j, i in enumerate(range(int(t0 * SR), int(t1 * SR), sl)):
        s = int(srcs[j % len(srcs)] * SR); n = min(sl, N - i)
        L[i:i + n] = L0[s:s + n]; R[i:i + n] = R0[s:s + n]
freeze(2.75, 2.88, [2.62]); freeze(2.8833, 3.0, [2.62, 2.70])
freeze(5.80, 5.94, [5.78]); freeze(9.05, 9.16, [9.03])
# master: silence at the very start/end, soft limiter
fo0, fo1 = int(9.3 * SR), int(9.85 * SR)
for ch in (L, R):
    ch[fo0:fo1] *= np.linspace(1, 0, fo1 - fo0) ** 2; ch[fo1:] = 0; ch[:int(0.005 * SR)] *= np.linspace(0, 1, int(0.005 * SR))
st = np.stack([L, R], 1); st = np.tanh(st * 1.3) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
