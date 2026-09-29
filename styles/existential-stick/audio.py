# events.json → audio.wav (48 kHz stereo, 10 s), all synthesized:
# projector flutter + hiss, pencil scratches for vignette borders and captions, soft footsteps, a paper slide
# for the split, music-box notes for each memory, a sea swell, a rising rattle into the colour burst (a
# detuned chord + crash that cuts to sudden silence), a bus that rumbles in, sighs its brakes and pulls away,
# and a quiet closing chord.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR)
dry = np.zeros((N, 2)); wet = np.zeros((N, 2))
rs = np.random.default_rng(108)
tt = lambda d: np.arange(int(d * SR)) / SR
def add(sig, t, g=1.0, pan=0.0, send=0.3):
    i = int(t * SR); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    l, r = np.sqrt(0.5 - pan / 2) * 1.414, np.sqrt(0.5 + pan / 2) * 1.414
    for bus, gg in ((dry, 1 - send * 0.5), (wet, send)):
        bus[i:i + n, 0] += sig[:n] * g * gg * l; bus[i:i + n, 1] += sig[:n] * g * gg * r
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def nrm(x): return x / (np.abs(x).max() + 1e-9)
def seg(t, a, b): return np.clip((t - a) / (b - a), 0, 1)
t = np.arange(N) / SR
ev = json.load(open('events.json'))
burst = next(e for e in ev if e['k'] == 'burst'); b0, b1 = burst['t'], burst['t'] + burst['d']
# projector bed: 24 Hz shutter flutter over filtered hiss, ducked to silence during the burst's aftermath
bed_env = seg(t, 0.0, 0.4) * (1 - 0.85 * seg(t, b0 - 0.1, b0))
bed_env = bed_env + 0.85 * seg(t, b1 + 0.25, b1 + 1.0) * (t > b1)
bed_env = np.clip(bed_env, 0, 1) * (1 - seg(t, 9.3, 10.0))
hiss = nrm(band(rs.standard_normal(N), 1500, 9000)); flut = 0.75 + 0.25 * np.sign(np.sin(2 * np.pi * 24 * t))
dry[:, 0] += hiss * 0.012 * bed_env * flut; dry[:, 1] += np.roll(hiss, 2000) * 0.012 * bed_env * flut
mot = nrm(band(rs.standard_normal(N), 60, 260)); dry[:, 0] += mot * 0.02 * bed_env; dry[:, 1] += mot * 0.02 * bed_env
for k in range(int(DUR * 24)):
    tc = k / 24; e = np.interp(tc, t, bed_env)
    if e > 0.05: add(nrm(band(rs.standard_normal(240), 800, 5000)) * np.exp(-np.arange(240) / 40), tc, 0.02 * e, 0, 0)
def scratch(d, lo=1800, hi=7000):
    x = tt(d); s = nrm(band(rs.standard_normal(len(x)), lo, hi))
    env = (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * (7 + 3 * rs.random()) * x))) * np.minimum(1, x / 0.02) * np.minimum(1, (d - x) / 0.05)
    return s * env
def step(v):
    x = tt(0.09); return nrm(band(rs.standard_normal(len(x)), 120, 1400)) * np.exp(-x / 0.018) + np.sin(2 * np.pi * 85 * x) * np.exp(-x / 0.03) * 0.6
def slide(d):
    x = tt(d); return nrm(band(rs.standard_normal(len(x)), 400, 4000)) * np.sin(np.pi * x / d) ** 1.5
def note(m, d=1.8, bright=1.0):
    f = 440 * 2 ** ((m - 69) / 12); x = tt(d)
    s = np.sin(2 * np.pi * f * x) + 0.35 * bright * np.sin(2 * np.pi * 2 * f * x) * np.exp(-x / 0.3) + 0.12 * bright * np.sin(2 * np.pi * 3.01 * f * x) * np.exp(-x / 0.15)
    return s * np.minimum(1, x / 0.004) * np.exp(-x / (d * 0.35))
for e in ev:
    k, te = e['k'], e['t']
    if k == 'pen': add(scratch(e['d']), te, 0.07, -0.2, 0.15)
    elif k == 'scribble': add(scratch(e['d'], 2500, 8000), te, 0.035, 0.2, 0.1)
    elif k == 'step': add(step(e['v']), te, 0.16 * e['v'], -0.3 + 0.4 * te / 2.5, 0.2)
    elif k == 'settle': add(step(1) * 0.6, te + 0.05, 0.1, 0.1, 0.2)
    elif k == 'whoosh': add(slide(0.5), te, 0.06, 0, 0.3)
    elif k == 'mem': add(note(e['m']), te, 0.12, (e['m'] - 72) / 10, 0.6); add(note(e['m'] + 12, 1.2, 0.5), te + 0.12, 0.04, 0.3, 0.7)
    elif k == 'sea':
        x = tt(1.2); add(nrm(band(rs.standard_normal(len(x)), 200, 1800)) * np.sin(np.pi * x / 1.2) ** 2, te, 0.05, -0.4, 0.4)
    elif k == 'rattle':
        d = b0 - te; x = tt(d); s = nrm(band(rs.standard_normal(len(x)), 300, 6000)) * (x / d) ** 1.5 * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 30 * x)))
        add(s, te, 0.16, 0, 0.2)
    elif k == 'burst':
        d = e['d']; x = tt(d)
        ch = sum(np.sin(2 * np.pi * f * (1 + dt) * x) for f in (220, 277.2, 329.6, 440, 554.4, 659.3) for dt in (-0.004, 0.004))
        ch = ch / 12 * (0.4 + 0.6 * seg(x, 0, d))
        crash = nrm(band(rs.standard_normal(len(x)), 800, 12000)) * np.exp(-x / 0.35)
        sh = nrm(band(rs.standard_normal(len(x)), 3000, 11000)) * (0.5 + 0.5 * np.sin(2 * np.pi * 6 * x)) * seg(x, 0, d)
        sig = (ch * 0.9 + crash * 0.6 + sh * 0.25) * np.minimum(1, (d - x) / 0.012)
        add(sig, te, 0.32, 0, 0.35)
    elif k == 'bus':
        a, bb, c = e['a'], e['b'], e['c']; d = c - te + 0.6; x = tt(d); tx = te + x
        env = seg(tx, te, a) * 0.8 + 0.2 * ((tx >= a) & (tx < bb)) + seg(tx, bb, bb + 0.1) * (tx >= bb) * 0.8
        env = np.clip(env, 0, 1) * (1 - seg(tx, c, c + 0.6))
        f0 = 48 + 14 * seg(tx, bb, c)
        ph = 2 * np.pi * np.cumsum(f0) / SR
        rum = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph)) * 0.5 + nrm(band(rs.standard_normal(len(x)), 60, 500)) * 0.5
        pan = np.interp(tx, [te, a, bb, c], [0.8, 0.0, 0.0, -0.8])
        i = int(te * SR); n = min(len(x), N - i)
        dry[i:i + n, 0] += (rum * env * 0.22 * np.sqrt(0.5 - pan / 2) * 1.414)[:n]; dry[i:i + n, 1] += (rum * env * 0.22 * np.sqrt(0.5 + pan / 2) * 1.414)[:n]
        y = tt(0.6); add(nrm(band(rs.standard_normal(len(y)), 2500, 9000)) * np.exp(-y / 0.22) * np.minimum(1, y / 0.03), a - 0.05, 0.08, 0.05, 0.3)
        add(np.sin(2 * np.pi * 2100 * tt(0.25)) * np.exp(-tt(0.25) / 0.08), a - 0.12, 0.02, 0.1, 0.3)
    elif k == 'chord':
        for j, m in enumerate((57, 64, 68, 71, 76)): add(note(m, 2.4, 0.6), te + j * 0.06, 0.07, -0.3 + j * 0.15, 0.7)
ir_t = tt(1.4); M = N + len(ir_t)
for ch in (0, 1):
    ir = rs.standard_normal(len(ir_t)) * np.exp(-ir_t / 0.35); ir[:int(0.01 * SR)] *= np.linspace(0, 1, int(0.01 * SR)); ir /= np.sqrt((ir ** 2).sum())
    y = np.fft.irfft(np.fft.rfft(wet[:, ch], M) * np.fft.rfft(ir, M), M)[:N]
    dry[:, ch] += y * 0.8
fi, fo = int(0.15 * SR), int(0.6 * SR)
dry[:fi] *= np.linspace(0, 1, fi)[:, None]; dry[-fo:] *= (np.linspace(1, 0, fo) ** 1.5)[:, None]
st = np.tanh(dry * 2.4) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
