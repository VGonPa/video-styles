# events.json → audio.wav (48 kHz stereo, 10 s)
# slowed + chopped soft synth pad (detuned saws, low-passed, tape wow, 8th-note chops with stutters, long reverb),
# lazy kick + reverb clap, window bloops, progress ticks, a two-note chime, mouse click, glitch bursts,
# noise swell into the lockup, letter blips on a pentatonic scale, and a final tape stop.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR)
rs = np.random.default_rng(95)
def tt(d): return np.arange(int(d * SR)) / SR
def add(buf, sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        buf[0, i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; buf[1, i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def lowpass(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= 1 / np.sqrt(1 + (f / fc) ** 4); return np.fft.irfft(X, len(x))
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def reverb(x, dec=1.8, seed=3):
    r = np.random.default_rng(seed); n = int(dec * 1.5 * SR); ir = r.standard_normal(n) * np.exp(-np.arange(n) / SR / (dec / 6.9))
    ir = lowpass(ir, 5000); ir /= np.sqrt((ir ** 2).sum())
    L = len(x) + n; F = 1 << (L - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, F) * np.fft.rfft(ir, F), F)[:len(x)]
nt = lambda m: 440 * 2 ** ((m - 69) / 12)

music = np.zeros((2, N)); sfx = np.zeros((2, N))
t = np.arange(N) / SR
# --- pad: slowed chords (≈ -3 semitones feel), each 2.5 s ---
wow = 1 + 0.004 * np.sin(2 * np.pi * 0.55 * t) + 0.0015 * np.sin(2 * np.pi * 3.1 * t)
chords = [[53, 57, 60, 64, 67], [52, 55, 59, 62, 66], [50, 53, 57, 60, 64], [48, 52, 55, 59, 62]]
pad = np.zeros(N)
for ci, ch in enumerate(chords):
    t0 = ci * 2.5; i0 = int(t0 * SR); i1 = min(N, int((t0 + 2.9) * SR)); tl = t[i0:i1] - t0
    env = np.minimum(1, tl / 0.35) * np.minimum(1, (2.9 - tl) / 0.5)
    for m in ch:
        for det in (-0.07, 0.07):
            f = nt(m - 3) * (1 + det / 12)
            ph = 2 * np.pi * np.cumsum(f * wow[i0:i1]) / SR + rs.uniform(0, 6.28)
            saw = 2 * ((ph / (2 * np.pi)) % 1) - 1
            pad[i0:i1] += saw * env * 0.06
pad = lowpass(pad, 1500)
# chop: 8th-note gate at 72 BPM, with stutters repeating the previous slice
beat = 60 / 72; e8 = beat / 2
gate = np.ones(N); chopped = pad.copy()
for k in range(int(DUR / e8) + 1):
    a = int(k * e8 * SR); b = min(N, int((k + 1) * e8 * SR))
    if a >= N: break
    n = b - a; g = np.ones(n); fade = int(0.012 * SR)
    g[:fade] = np.linspace(0, 1, fade)[:n]; g[-fade:] = np.minimum(g[-fade:], np.linspace(1, 0, fade)[-min(n, fade):])
    if k % 2 == 1: g *= 0.72
    gate[a:b] = g
    if k in (5, 13) and a - n >= 0:                               # stutter: replay the previous slice
        chopped[a:b] = pad[a - n:a]
music[0] += chopped * gate; music[1] += np.roll(chopped * gate, 240)
# bass: soft sine roots
for ci, ch in enumerate(chords):
    s = tt(2.5); f = nt(ch[0] - 15)
    add(music, np.sin(2 * np.pi * f * s) * np.minimum(1, s / 0.05) * np.exp(-s / 1.6), ci * 2.5, 0.22)
# lazy drums
def kick():
    s = tt(0.4); f = 50 + 90 * np.exp(-s * 30); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-s / 0.12)
def clap():
    s = tt(0.25); n = band(rs.standard_normal(len(s)), 900, 6000); env = np.exp(-s / 0.05) * (1 + 0.6 * (np.sin(2 * np.pi * 90 * s) > 0) * (s < 0.03))
    return n / np.abs(n).max() * env
drum = np.zeros((2, N))
for k in range(int(DUR / beat)):
    tb = 0.6 + k * beat
    if tb > 9.4: break
    if 4.15 < tb < 5.2: continue                                   # drop out during the glitch
    add(drum, kick(), tb, 0.35)
    if k % 2 == 1: add(drum, clap(), tb, 0.12)
drum[0] += reverb(drum[0], 1.4, 5) * 0.35; drum[1] += reverb(drum[1], 1.4, 6) * 0.35
music += drum
music[0] += reverb(music[0], 2.4, 1) * 0.5; music[1] += reverb(music[1], 2.4, 2) * 0.5
# glitch: music stutters and drops pitch briefly
g0, g1 = int(4.15 * SR), int(5.25 * SR)
seg = music[:, g0:g1].copy(); sl = int(0.09 * SR)
for i in range(0, g1 - g0, sl):
    if (i // sl) % 3 == 1: seg[:, i:i + sl] = music[:, g0 + max(0, i - sl):g0 + max(0, i - sl) + sl][:, :seg[:, i:i + sl].shape[1]]
seg = np.round(seg * 24) / 24                                      # bitcrush
music[:, g0:g1] = seg * 0.8

# --- sfx ---
def bloop(f0=500, f1=900):
    s = tt(0.18); f = f0 + (f1 - f0) * (1 - np.exp(-s * 40)); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-s / 0.05)
def pluck(f):
    s = tt(0.5); return (np.sin(2 * np.pi * f * s) + 0.3 * np.sin(4 * np.pi * f * s)) * np.exp(-s / 0.12) * np.minimum(1, s / 0.004)
def tick():
    s = tt(0.02); return band(rs.standard_normal(len(s)), 2000, 8000) * np.exp(-s / 0.003)
def bell(f, d=1.4):
    s = tt(d); return sum(a * np.sin(2 * np.pi * f * h * s) * np.exp(-s / (d / (1 + h))) for h, a in [(1, 1), (2.76, .35), (5.4, .15)])
penta = [72, 74, 76, 79, 81, 84, 86, 88, 91, 93]
for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'blip': add(sfx, pluck(nt(penta[int(e['v']) % len(penta)])), te, 0.07, (int(e['v']) % 5 - 2) * 0.15)
    elif k == 'pop': add(sfx, bloop(), te, 0.22, rs.uniform(-.3, .3))
    elif k == 'pop95': add(sfx, bloop(700, 1400), te, 0.25); add(sfx, bell(nt(84), 1.0), te, 0.05)
    elif k == 'tick': add(sfx, tick(), te, 0.05, -0.4)
    elif k == 'ding': add(sfx, bell(nt(76)), te, 0.09, -0.3); add(sfx, bell(nt(83)), te + 0.16, 0.09, -0.3)
    elif k == 'click':
        s = tt(0.03); c = band(rs.standard_normal(len(s)), 1500, 9000) * np.exp(-s / 0.004); add(sfx, c, te, 0.3, 0.3); add(sfx, c * 0.6, te + 0.11, 0.3, 0.3)
    elif k == 'glitch':
        d = e['d']
        for j in range(14):
            tj = te + d * rs.random(); s = tt(0.03 + 0.07 * rs.random())
            n = np.round(rs.standard_normal(len(s)) * 3) / 3 * np.sign(np.sin(2 * np.pi * rs.uniform(200, 2000) * s))
            add(sfx, n * np.exp(-s / 0.04), tj, 0.07, rs.uniform(-.6, .6))
    elif k == 'swell':
        s = tt(0.7); n = band(rs.standard_normal(len(s)), 2000, 12000) * (s / 0.7) ** 3
        add(sfx, n / np.abs(n).max(), te - 0.6, 0.12)
        for i, m in enumerate([60, 64, 67, 71, 74]): add(sfx, bell(nt(m), 2.2), te + 0.05 + i * 0.03, 0.035, (i - 2) * 0.2)
    elif k == 'chime':
        for i, m in enumerate([88, 91, 95]): add(sfx, bell(nt(m), 1.0), te + i * 0.12, 0.03, 0.4)
    elif k == 'tapestop': pass
sfx[0] += reverb(sfx[0], 1.6, 7) * 0.3; sfx[1] += reverb(sfx[1], 1.6, 8) * 0.3

mix = music + sfx
# tape stop: from 9.1 s playback speed slides to 0
ts, te_ = 9.1, 10.0; i0 = int(ts * SR)
n = N - i0; u = np.arange(n) / SR / (te_ - ts); speed = np.clip(1 - u, 0, 1) ** 1.3
pos = i0 + np.cumsum(speed)
for ch in range(2): mix[ch, i0:] = np.interp(pos, np.arange(N), mix[ch]) * np.clip(1 - u, 0, 1) ** 0.7
fi = int(0.4 * SR); mix[:, :fi] *= np.linspace(0, 1, fi)
mix = np.tanh(mix * 1.3) * 0.82
pcm = (np.clip(mix.T, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(mix).max().round(3))
