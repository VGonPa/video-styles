# events.json → audio.wav (48 kHz stereo, 10 s) · chiptune: pulse/triangle/noise channels
# underwater groove (triangle bass + 12.5% pulse arpeggio), rising pearl chimes, bubble blips, pufferfish warning + inflate,
# chest rattle/open, big-pearl sparkle, fanfare + score tally, mosaic sweeps, map dots/hops and a closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(14)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def env(s, a=60, r=200):
    n = len(s); k = np.arange(n); return s * np.minimum(1, k / a) * np.minimum(1, (n - k) / r)
def sq(freqs, durs, duty=0.5, dec=None):
    parts = []
    for f, d in zip(freqs, durs):
        n = int(d * SR); tt = np.arange(n) / SR
        f = np.full(n, f) if np.isscalar(f) else np.geomspace(f[0], f[1], n)
        ph = np.cumsum(f) / SR % 1.0
        s = np.where(ph < duty, 1.0, -1.0) * (f.max() > 0)
        if dec: s = s * np.exp(-tt / dec)
        parts.append(env(s))
    return np.concatenate(parts)
def tri(f, d, dec=None):
    n = int(d * SR); tt = np.arange(n) / SR
    f = np.full(n, f) if np.isscalar(f) else np.geomspace(f[0], f[1], n)
    ph = np.cumsum(f) / SR % 1.0; s = 4 * np.abs(ph - 0.5) - 1
    s = np.round(s * 8) / 8  # 4-bit stepped triangle like a console wave channel
    if dec: s = s * np.exp(-tt / dec)
    return env(s)
def noise(d, dec, step=8):
    n = int(d * SR); s = np.repeat(rs.choice([-1.0, 1.0], n // step + 1), step)[:n]
    return env(s * np.exp(-np.arange(n) / SR / dec))
def hz(m): return 440 * 2 ** ((m - 69) / 12)

# ── underwater groove until LEVEL CLEAR ──
BPM = 128; E8 = 60 / BPM / 2
prog = [(57, [69, 72, 76]), (53, [69, 72, 77]), (48, [67, 72, 76]), (55, [67, 71, 74])]  # Am F C G
t, k, T_END = 0.45, 0, 6.7
while t < T_END:
    root, ch = prog[(k // 8) % 4]
    fade = min(1, (T_END - t) / 0.4)
    add(tri(hz(root - 12 + (12 if k % 2 else 0)), E8 * 0.9), t, 0.30 * fade)
    for q in range(2):
        add(sq([hz(ch[(k * 2 + q) % 3] + 12)], [E8 * 0.45], 0.125, 0.06), t + q * E8 / 2, 0.035 * fade, 0.35 if q else -0.35)
    if k % 4 == 2: add(noise(0.05, 0.015, 4), t, 0.05 * fade)
    t += E8; k += 1

for e in json.load(open('events.json')):
    k, t = e['k'], e['t']
    if k == 'pearl':
        m = 84 + [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17][e['n']]
        add(sq([hz(m), hz(m + 7)], [0.05, 0.16], 0.25, 0.08), t, 0.13, 0.2)
    elif k == 'bubble':
        for q in range(3): add(sq([(500 + 180 * q, 1500 + 300 * q)], [0.04], 0.5), t + q * 0.07, 0.05, -0.3)
    elif k == 'warn': add(sq([1760, 0, 1760], [0.05, 0.03, 0.08], 0.5), t, 0.1)
    elif k == 'puff': add(sq([(150, 900)], [0.22], 0.25), t, 0.14, 0.3); add(noise(0.25, 0.1, 16), t, 0.07, 0.3)
    elif k == 'deflate': add(sq([(700, 120)], [0.3], 0.25, 0.25), t, 0.09, 0.3)
    elif k == 'rattle': add(noise(0.06, 0.02, 24), t, 0.14, 0.4); add(tri(110, 0.06), t, 0.2, 0.4)
    elif k == 'open':
        add(tri((90, 60), 0.18, 0.08), t, 0.45, 0.4); add(noise(0.2, 0.05, 12), t, 0.12, 0.4)
        add(sq([hz(m) for m in [79, 83, 86, 91]], [0.05] * 4, 0.25, 0.1), t + 0.05, 0.1, 0.4)
    elif k == 'bigpearl':
        add(sq([hz(m) for m in [84, 88, 91, 96, 100]], [0.05, 0.05, 0.05, 0.05, 0.35], 0.5, 0.12), t, 0.12, 0.2)
    elif k == 'fanfare':
        notes = [72, 76, 79, 84, 79, 84, 88]; ds = [0.11, 0.11, 0.11, 0.2, 0.1, 0.12, 0.6]
        add(sq([hz(m) for m in notes], ds, 0.25), t, 0.12); add(sq([hz(m - 12) for m in notes], ds, 0.5), t, 0.05)
        add(tri(hz(43), 0.25), t + 0.46, 0.25); add(tri(hz(48), 0.55), t + 0.66, 0.3)
    elif k == 'tally':
        for q in range(14): add(sq([hz(96)], [0.025], 0.5), t + q * 0.035, 0.05)
    elif k == 'swoosh_in': add(sq([(220, 880)], [0.4], 0.5, 0.3), t, 0.06)
    elif k == 'swoosh_out': add(sq([(880, 180)], [0.35], 0.5, 0.25), t, 0.07)
    elif k == 'card': add(sq([hz(79), hz(84)], [0.06, 0.18], 0.5, 0.1), t, 0.08)
    elif k == 'flag': add(sq([hz(m) for m in [76, 79, 84, 88]], [0.05, 0.05, 0.05, 0.25], 0.25, 0.12), t, 0.1, -0.2)
    elif k == 'dot': add(sq([hz(91)], [0.025], 0.5), t, 0.05, 0.2)
    elif k == 'hop': add(sq([(330, 900)], [0.08], 0.25), t, 0.1, 0.1)
    elif k == 'select':
        add(sq([hz(84), hz(91), hz(96)], [0.06, 0.06, 0.25], 0.5, 0.15), t, 0.09)
        for m, dt in [(60, 0.0), (64, 0.08), (67, 0.16), (72, 0.24)]: add(tri(hz(m), 0.9 - dt, 0.5), t + 0.2 + dt, 0.12)

mx = np.stack([L, R], 1)
mx = np.tanh(mx * 1.1) * 0.85
pcm = (np.clip(mx, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok')
