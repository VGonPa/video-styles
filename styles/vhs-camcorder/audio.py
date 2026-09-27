# events.json → audio.wav (48 kHz stereo, 10 s)
# Two layers:
#  • the TAPE: a mono camcorder soundtrack in tape time τ (garden ambience, birds, a tinny boombox tune, the candle blow,
#    party popper + horn, claps, two barks, mic handling) — read back through τ(t) from anim.html, so FF/REW really scrub
#    it (pitched-up chatter, reversed squeal), with wow & flutter and a camcorder-mic band limit;
#  • the DECK: button clunks, drum spin-up, transport whine in FF/REW, tape hiss, TV static when the tape breaks up.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR)
rs = np.random.default_rng(1996)
E = json.load(open('events.json'))
TB, TJ = E['TB'], E['TJ']
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)

# ── tape soundtrack, τ ∈ [-1, 11] ──────────────────────────────────────────────────────────
T0, TL = -1.0, 12.0
M = np.zeros(int(TL * SR))
def put(sig, tau, g=1.0):
    i = int((tau - T0) * SR); n = min(len(sig), len(M) - i)
    if n > 0 and i >= 0: M[i:i + n] += sig[:n] * g
tm = np.arange(len(M)) / SR + T0
# garden air: soft wind + distant traffic hush
air = band(rs.standard_normal(len(M)), 80, 2500); air = norm(air) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.23 * tm) ** 2)
M += air * 0.05
def chirp():
    d = 0.05 + rs.random() * 0.07; t = tt(d); f0 = 2600 + rs.random() * 2200
    f = f0 + 900 * np.sin(np.pi * t / d) * (1 if rs.random() < .5 else -1) + 300 * np.sin(2 * np.pi * 45 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 2
tb = -0.8
while tb < 10.5:
    for k in range(int(2 + rs.random() * 3)): put(chirp(), tb + k * (0.09 + rs.random() * 0.05), 0.05 + rs.random() * 0.04)
    tb += 0.5 + rs.random() * 0.9
# boombox tune in the next room of the garden: toy-piano arpeggios I–vi–IV–V (original), tinny + band-limited
def bell(freq, d=0.45):
    t = tt(d); s = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 3.01 * t) * np.exp(-t / 0.05) + 0.2 * np.sin(2 * np.pi * freq * 2 * t)
    return s * np.exp(-t / 0.18) * np.minimum(1, t / 0.004)
prog = [[60, 64, 67, 72], [57, 60, 64, 69], [53, 57, 60, 65], [55, 59, 62, 67]]
beat = 0.3; tb = -0.6; bar = 0
while tb < 11:
    ch = prog[bar % 4]
    for k, m in enumerate([ch[0], ch[1], ch[2], ch[3], ch[2], ch[1], ch[0] + 12, ch[2]]):
        put(bell(nt(m + 12)), tb + k * beat / 2, 0.05)
    put(bell(nt(ch[0] - 12), 0.9), tb, 0.06)
    tb += beat * 4; bar += 1
# the blow: a breath across the candles, flames fluttering
t = tt(0.55); put(norm(band(rs.standard_normal(len(t)), 250, 3500)) * np.sin(np.pi * t / 0.55) ** 1.5, TB - 0.2, 0.35)
# party popper at TJ, horn right after
t = tt(0.3); pop = norm(band(rs.standard_normal(len(t)), 400, 9000)) * np.exp(-t / 0.018) + 0.6 * np.sin(2 * np.pi * 120 * t) * np.exp(-t / 0.03)
put(pop, TJ - 0.02, 0.55)
t = tt(0.7); fh = 330 + 90 * np.minimum(1, t / 0.15) + 8 * np.sin(2 * np.pi * 7 * t); ph = np.cumsum(fh) / SR
horn = (2 * (ph % 1) - 1); horn = band(horn, 200, 4000) * np.minimum(1, t / 0.03) * np.minimum(1, (0.7 - t) / 0.08)
put(horn, TJ + 0.12, 0.12)
# claps (three pairs of hands, loose timing)
for h in range(3):
    tc = TJ + 0.25 + rs.random() * 0.1
    while tc < TJ + 1.9:
        t = tt(0.05); c = norm(band(rs.standard_normal(len(t)), 800, 6000)) * np.exp(-t / 0.008)
        put(c, tc, 0.13 * (0.7 + 0.3 * rs.random())); tc += 0.17 + rs.random() * 0.06
# barks
def bark():
    t = tt(0.2); f = 520 * np.exp(-t * 3) + 260; ph = np.cumsum(f) / SR
    src = sum(np.sin(2 * np.pi * ph * h) / h for h in range(1, 14))
    noise = band(rs.standard_normal(len(t)), 500, 4000) * 0.4
    env = np.minimum(1, t / 0.008) * np.exp(-t / 0.07)
    return band((src + noise) * env, 250, 3800)
put(norm(bark()), TJ + 0.08, 0.45); put(norm(bark()), TJ + 0.68, 0.35)
# mic handling bumps during the zoom (thumb on the rocker)
for tz in (1.5, 3.3, 4.75):
    t = tt(0.12); put(norm(band(rs.standard_normal(len(t)), 40, 400)) * np.exp(-t / 0.03), tz, 0.18)
M = band(M, 90, 7500)                                   # camcorder mic / linear-track band limit

# ── read the tape through τ(t) ─────────────────────────────────────────────────────────────
tA = np.arange(N) / SR
tau = np.interp(tA, np.arange(len(E['tau'])) / 500, E['tau'])
wow = 0.0012 * np.sin(2 * np.pi * 0.55 * tA) + 0.0004 * np.sin(2 * np.pi * 6.3 * tA)   # wow & flutter (seconds of tape)
pos = (tau + wow - T0) * SR
tape = np.interp(pos, np.arange(len(M)), M)
seg = lambda a, b: np.clip((tA - a) / (b - a), 0, 1)
def mode_gain():
    g = np.zeros(N)
    for t0, t1, m, v in E['segs']:
        k = (tA >= t0) & (tA < t1)
        g[k] = {'blue': 0, 'lock': 1, 'play': 1, 'ff': 0.5, 'rew': 0.5, 'snow': 1, 'end': 0}[m]
    return g
tg = mode_gain() * seg(0.62, 0.9) * (1 - seg(8.3, 8.55))
tg = np.convolve(tg, np.ones(480) / 480, 'same')
out = tape * tg

# ── deck sounds ────────────────────────────────────────────────────────────────────────────
L = out.copy(); R = out.copy()
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def clunk():
    t = tt(0.25); thump = np.sin(2 * np.pi * (90 * np.exp(-t * 10) + 55) * t) * np.exp(-t / 0.04)
    c1 = norm(band(rs.standard_normal(len(t)), 1500, 8000)) * np.exp(-t / 0.003)
    c2 = np.roll(norm(band(rs.standard_normal(len(t)), 900, 5000)) * np.exp(-t / 0.006), int(0.035 * SR))
    rat = norm(band(rs.standard_normal(len(t)), 600, 3000)) * np.exp(-t / 0.05) * 0.2
    return thump * 0.8 + c1 * 0.6 + c2 * 0.45 + rat
for e in E['ev']:
    if e['k'] in ('clunk', 'stop'): add(clunk(), e['t'], 0.5)
# drum spin-up + running hum
t = tt(0.9); f = 60 + 840 * (1 - np.exp(-t / 0.25)); spin = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / 0.05) * (1 - np.clip((t - 0.5) / 0.4, 0, 1))
add(spin, 0.14, 0.03)
run = (np.sin(2 * np.pi * 29.97 * tA) + 0.5 * np.sin(2 * np.pi * 59.94 * tA) + 0.2 * np.sin(2 * np.pi * 899 * tA)) * seg(0.3, 0.7) * (1 - seg(9.0, 9.05))
L += run * 0.008; R += run * 0.008
# transport whine (FF up, REW slightly lower) + tape rush
for (a, b, f0) in [(4.6, 5.2, 1500), (6.8, 7.75, 1200)]:
    d = b - a + 0.15; t = tt(d); f = f0 * (0.6 + 0.4 * np.minimum(1, t / 0.12)) * (1 + 0.1 * t / d)
    env = np.minimum(1, t / 0.08) * np.minimum(1, (d - t) / 0.1)
    wh = (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(2 * np.pi * np.cumsum(f * 2.02) / SR)) * env
    rush = norm(band(rs.standard_normal(len(t)), 1500, 9000)) * env
    add(wh, a, 0.035, -0.2); add(rush, a, 0.05, 0.2)
# tape hiss while the heads are on tape
hiss = norm(band(rs.standard_normal(N), 2500, 14000)); hg = seg(0.62, 0.7) * (1 - seg(9.0, 9.03))
L += hiss * hg * 0.022; R += np.roll(hiss, 999) * hg * 0.022
# tape breaks up → TV static
st = norm(band(rs.standard_normal(N), 150, 11000)) * (1 + 0.25 * np.sin(2 * np.pi * 59.94 * tA))
sg = seg(8.3, 8.6) * (1 - seg(8.98, 9.02))
L += st * sg * 0.3; R += np.roll(st, 1777) * sg * 0.3
# faint power hum on the blue screen, gone with the fade
blue = np.sin(2 * np.pi * 60 * tA) * (seg(9.02, 9.2) * (1 - seg(9.55, 9.95)) + (seg(0.1, 0.15) * (1 - seg(0.6, 0.64))))
L += blue * 0.006; R += blue * 0.006

# master: fade in/out, soft limiter
fi = int(0.05 * SR); fo = int(0.45 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
stt = np.stack([L, R], 1); stt = np.tanh(stt * 1.5) * 0.8
pcm = (np.clip(stt, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(stt).max().round(3))
