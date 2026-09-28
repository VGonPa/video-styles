# events.json → audio.wav (48 kHz stereo, 10 s)
# Ambient generative score: a slow A-minor drone that swells out of silence, an airy noise wash and a cloud of tiny
# sine grains whose loudness/density follow the particles' mean speed (the 'speed' curve exported by anim.html).
# SFX from events.json: glassy FM chimes as each letter of EMERGE locks in, a left→right shimmer for the wave, a
# reverse swell for the inhale, a sub-drop + crash for the burst, a wide chord bloom for the galaxy, an accelerating
# riser for the collapse and a bell + boom for the singularity flash, then everything decays into a reverb tail.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N); VL = np.zeros(N); VR = np.zeros(N)   # dry bus + reverb send
rs = np.random.default_rng(49)
def add(sig, t, g=1.0, pan=0.0, send=0.35):
    i = int(round(t * SR)); j = max(0, -i); i = max(0, i); n = min(len(sig) - j, N - i)
    if n <= 0: return
    s = sig[j:j + n] * g; gl, gr = np.sqrt(0.5 - pan / 2) * 1.414, np.sqrt(0.5 + pan / 2) * 1.414
    L[i:i + n] += s * gl; R[i:i + n] += s * gr; VL[i:i + n] += s * gl * send; VR[i:i + n] += s * gr * send
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def conv(x, h):
    n = len(x) + len(h) - 1; return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[:len(x)]
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
ev = json.load(open('events.json'))
spd = np.array(next(e['v'] for e in ev if e['k'] == 'speed'), float)
t0 = np.arange(N) / SR
S = np.interp(t0, np.arange(len(spd)) / 30, spd)            # mean |v| (px/s) at audio rate
act = np.clip(S / 600, 0, 1.5)                                # activity 0..1.5

# ── drone: detuned sines, slow swell, dies after the flash ──
dr_env = np.clip(t0 / 1.8, 0, 1) ** 2 * np.where(t0 < 9.05, 1, np.exp(-(t0 - 9.05) / 0.25))
for m, g in [(33, .5), (40, .35), (45, .3), (48, .16), (52, .12)]:
    for dt, ph in [(-0.06, 0.3), (0.05, 1.7)]:
        f = nt(m + dt); L += np.sin(2 * np.pi * f * t0 + ph) * g * 0.05 * dr_env * (1 + 0.3 * np.sin(2 * np.pi * 0.13 * t0 + m))
        R += np.sin(2 * np.pi * f * 1.001 * t0 + ph + 0.7) * g * 0.05 * dr_env * (1 + 0.3 * np.sin(2 * np.pi * 0.11 * t0 + m + 1))
# ── airy wash following speed ──
wash = band(rs.standard_normal(N), 500, 5000); wash2 = band(rs.standard_normal(N), 500, 5000)
we = (0.012 + 0.05 * act) * np.clip(t0 / 1.0, 0, 1) * np.where(t0 < 9.1, 1, np.exp(-(t0 - 9.1) / 0.15))
L += norm(wash) * we; R += norm(wash2) * we
# ── particle grains: density and brightness follow activity ──
for k in range(1400):
    tg = rs.uniform(0.15, 9.1); a = float(np.interp(tg, t0[::480], act[::480]))
    if rs.random() > 0.12 + 0.6 * min(a, 1): continue
    f = rs.choice([nt(m) for m in (81, 84, 86, 88, 91, 93, 96, 98)]) * (1 + 0.003 * rs.standard_normal())
    d = 0.05 + 0.06 * rs.random(); t = tt(d)
    add(np.sin(2 * np.pi * f * t) * np.sin(np.pi * t / d) ** 2, tg, 0.006 + 0.01 * min(a, 1.2), rs.uniform(-0.9, 0.9), 0.6)

def bell(f, d=2.2, idx=2.0, ratio=3.5):
    t = tt(d); e = np.exp(-t / (d * 0.28)) * np.minimum(1, t / 0.004)
    return np.sin(2 * np.pi * f * t + idx * np.exp(-t / 0.3) * np.sin(2 * np.pi * f * ratio * t)) * e
def sweep(f0, f1, d, shape=1.0):
    t = tt(d); f = f0 * (f1 / f0) ** ((t / d) ** shape); return np.sin(2 * np.pi * np.cumsum(f) / SR)
CHIME = [69, 72, 74, 76, 79, 81]
for e in ev:
    k, te = e['k'], e['t']
    if k == 'lock':
        i = e['i']; add(bell(nt(CHIME[i] + 12), 1.6, 1.4, 2.0), te, 0.06, -0.7 + 0.28 * i, 0.7)
        add(bell(nt(CHIME[i]), 1.8, 0.6, 1.0), te, 0.04, -0.7 + 0.28 * i, 0.5)
    elif k == 'wave':
        d = 0.95; t = tt(d); s = np.zeros_like(t)
        for j in range(24):
            f = nt(rs.choice([88, 91, 93, 96, 100])); o = int(rs.uniform(0, 0.7) * SR); tl = t[:len(t) - o]
            g = np.zeros_like(t); g[o:] = np.sin(2 * np.pi * f * tl) * np.exp(-tl / 0.09); s += g
        s *= np.sin(np.pi * t / d)
        for j, pan in enumerate(np.linspace(-0.8, 0.8, 6)):
            seg = s.copy(); m = np.zeros_like(t); a, b = int(j / 6 * len(t)), int((j + 1) / 6 * len(t)); m[a:b] = 1
            add(seg * m, te, 0.035, pan, 0.8)
    elif k == 'inhale':
        d = 0.36; t = tt(d); env = (t / d) ** 2.5
        add(norm(band(rs.standard_normal(len(t)), 800, 7000)) * env, te, 0.12, 0, 0.3)
        add(sweep(220, 660, d, 2) * env, te, 0.05)
    elif k == 'burst':
        t = tt(1.6); sub = np.sin(2 * np.pi * np.cumsum(34 + 110 * np.exp(-t * 16)) / SR) * np.exp(-t / 0.45)
        crash = norm(band(rs.standard_normal(len(t)), 1500, 14000)) * np.exp(-t / 0.35)
        add(sub, te, 0.55, 0, 0.1); add(crash, te, 0.1, -0.35, 0.8); add(np.roll(crash, 700), te, 0.08, 0.35, 0.8)
        for m in (69, 76, 81, 88): add(bell(nt(m), 2.4, 1.2, 1.5), te + 0.02, 0.025, rs.uniform(-.6, .6), 0.9)
    elif k == 'galaxy':
        d = 3.4; t = tt(d); env = np.clip(t / 0.9, 0, 1) * np.clip((d - t) / 1.0, 0, 1)
        for m, pan in [(53, -0.5), (57, 0.5), (60, -0.2), (64, 0.3), (69, 0), (72, -0.6)]:
            s = sum(np.sin(2 * np.pi * nt(m) * (1 + dt) * t + dt * 900) for dt in (-0.002, 0, 0.0025)) / 3
            add(s * env * (1 + 0.25 * np.sin(2 * np.pi * 0.7 * t + m)), te, 0.022, pan, 0.6)
    elif k == 'collapse':
        d = 9.05 - te; t = tt(d); env = (t / d) ** 2.2
        trem = 0.6 + 0.4 * np.sin(2 * np.pi * np.cumsum(3 + 22 * (t / d) ** 2) / SR)
        add(sweep(110, 1320, d, 2.0) * env * trem, te, 0.06, 0, 0.5)
        add(sweep(165, 1980, d, 2.0) * env * trem, te, 0.03, 0.3, 0.5)
        add(norm(band(rs.standard_normal(len(t)), 2000, 12000)) * env, te, 0.05, -0.2, 0.6)
    elif k == 'flash':
        t = tt(1.4); add(np.sin(2 * np.pi * np.cumsum(30 + 70 * np.exp(-t * 12)) / SR) * np.exp(-t / 0.3), te, 0.5, 0, 0.2)
        for m, g in [(81, .08), (88, .05), (93, .04), (69, .06)]: add(bell(nt(m), 2.6, 1.0, 2.76), te, g, rs.uniform(-.3, .3), 1.0)

# ── reverb (stereo noise IRs) + master ──
for bus, out in ((VL, L), (VR, R)):
    ir = rs.standard_normal(int(1.8 * SR)) * np.exp(-tt(1.8) / 0.5); ir = band(ir, 200, 9000); ir /= np.sqrt((ir ** 2).sum())
    out += conv(bus, ir) * 0.5
fi = int(0.05 * SR); fo = int(0.3 * SR)
st = np.stack([L, R], 1); st[:fi] *= np.linspace(0, 1, fi)[:, None]; st[-fo:] *= (np.linspace(1, 0, fo) ** 2)[:, None]
st = np.tanh(st * 1.6) * 0.8
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
