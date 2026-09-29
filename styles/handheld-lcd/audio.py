# events.json -> audio.wav (48 kHz stereo, 10 s)
# A four-channel handheld sound chip, synthesized: two pulse channels (duty 12.5/25/50 %), a 4-bit wave
# channel and an LFSR noise channel. Plus two non-chip sounds: the power slider click and a faint speaker hiss.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(70)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(d * SR)) / SR
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * (1 - max(0, pan)); R[i:i + n] += sig[:n] * g * (1 + min(0, pan))
def pulse(f, d, duty=0.5, env=None, sweep=None):
    t = tt(d); fr = np.full(len(t), float(f)) if sweep is None else sweep(t)
    ph = np.cumsum(fr) / SR; s = np.where((ph % 1) < duty, 1.0, -1.0)
    # 4-bit style stepped volume envelope
    e = np.ones(len(t)) if env is None else env(t)
    e = np.round(e * 15) / 15
    return s * e
WAVE = np.array([15, 13, 11, 9, 7, 5, 3, 1, 0, 2, 4, 6, 8, 10, 12, 14]) / 7.5 - 1  # triangle-ish 4-bit table
def wavech(f, d, env=None):
    t = tt(d); idx = ((t * f * 16).astype(int)) % 16; s = WAVE[idx]
    e = np.ones(len(t)) if env is None else env(t); return s * e
def lfsr(n, short=False, seed=0x7FFF):
    out = np.empty(n); r = seed
    for i in range(n):
        b = (r ^ (r >> 1)) & 1; r = (r >> 1) | (b << 14)
        if short: r = (r & ~(1 << 6)) | (b << 6)
        out[i] = 1.0 if r & 1 else -1.0
    return out
def noise(d, rate=8000, short=False, env=None):
    t = tt(d); k = max(1, int(d * rate) + 1); base = lfsr(k, short)
    s = base[np.minimum((t * rate).astype(int), k - 1)]
    e = np.ones(len(t)) if env is None else env(t); return s * np.round(e * 15) / 15
dec = lambda tau: (lambda t: np.exp(-t / tau))
def lin(d): return lambda t: np.clip(1 - t / d, 0, 1)

# ---- music (original tunes)
def song(t0, d, name):
    if name == 'puzzle':
        e8 = 0.2
        lead = [74, 77, 81, 77, 79, 77, 74, 72, 74, 77, 79, 81, 84, 81]
        bass = [50, 62, 50, 62, 48, 60, 48, 60, 46, 58, 46, 58, 45, 57]
        harm = [65, 0, 69, 0, 64, 0, 67, 0, 62, 0, 65, 0, 69, 0]
    else:
        e8 = 0.25
        lead = [72, 76, 79, 76, 77, 74, 71, 74]
        bass = [48, 55, 52, 55, 50, 55, 53, 55]
        harm = [0, 64, 0, 67, 0, 65, 0, 62]
    k = 0
    while k * e8 < d - 0.02:
        ts = t0 + k * e8; i = k % len(lead)
        fade = min(1.0, (d - k * e8) / 0.3)
        add(pulse(nt(lead[i]), e8 * 0.9, 0.25, lambda t: 0.9 * np.exp(-t / 0.22)), ts, 0.07 * fade, -0.35)
        add(wavech(nt(bass[i]), e8 * 0.85, lambda t: np.clip(1 - t / (e8 * 0.85), 0, 1) ** 0.3), ts, 0.10 * fade, 0.0)
        if harm[i]: add(pulse(nt(harm[i]), e8 * 0.4, 0.125, lambda t: 0.7 * np.exp(-t / 0.06)), ts, 0.045 * fade, 0.4)
        add(noise(0.03, 20000, True, lin(0.03)), ts, (0.03 if k % 2 else 0.05) * fade, 0.2)
        k += 1

for e in json.load(open('events.json')):
    k, te = e['k'], e['t']
    if k == 'click':
        t = tt(0.07); c = rs.standard_normal(len(t)) * np.exp(-t / 0.004); th = np.sin(2 * np.pi * 140 * t) * np.exp(-t / 0.015)
        add(0.6 * c + 0.8 * th, te, 0.35); add(rs.standard_normal(len(t)) * np.exp(-t / 0.002), te + 0.035, 0.18)
    elif k == 'hum':
        d = 8.72 - te; t = tt(d); h = rs.standard_normal(len(t)); h = np.convolve(h, np.ones(6) / 6, 'same')
        add(h * np.minimum(1, t / 0.2), te, 0.006)
    elif k == 'boot':
        add(pulse(nt(79), 0.06, 0.5, lambda t: 0.8 + 0 * t), te, 0.09, -0.1)
        add(pulse(nt(84), 0.06, 0.5, lambda t: 0.8 + 0 * t), te + 0.06, 0.09, 0.1)
        add(pulse(nt(91), 0.7, 0.25, lambda t: np.exp(-t / 0.22), sweep=lambda t: nt(91) * (1 + 0.004 * np.sin(2 * np.pi * 6 * t))), te + 0.12, 0.11)
        add(pulse(nt(84), 0.6, 0.125, dec(0.18)), te + 0.12, 0.05, 0.3)
    elif k == 'move': add(pulse(1320, 0.03, 0.5, lin(0.03)), te, 0.06, -0.2)
    elif k == 'rot': add(pulse(0, 0.07, 0.5, lin(0.07), sweep=lambda t: 600 + 12000 * t), te, 0.06, 0.2)
    elif k == 'spawn': add(pulse(nt(88), 0.025, 0.25, lin(0.025)), te, 0.03, 0.3)
    elif k == 'lock': add(noise(0.09, 3500, False, dec(0.03)), te, 0.14)
    elif k == 'drop': add(noise(0.14, 9000, False, lin(0.14)), te - 0.06, 0.08); add(pulse(0, 0.08, 0.5, lin(0.08), sweep=lambda t: 900 - 8000 * t), te - 0.07, 0.05)
    elif k == 'clear':
        for i, m in enumerate([72, 76, 79, 84, 88, 91, 96]): add(pulse(nt(m), 0.05, 0.5, lin(0.05)), te + i * 0.045, 0.07, -0.3 + 0.1 * i)
        add(noise(0.4, 12000, False, dec(0.15)), te, 0.05)
    elif k == 'collapse': add(noise(0.25, 1800, False, dec(0.07)), te, 0.2); add(wavech(nt(36), 0.2, dec(0.06)), te, 0.15)
    elif k == 'music': song(te, e['d'], e['song'])
    elif k == 'step': add(noise(0.025, 6000, True, lin(0.025)), te, 0.05, rs.uniform(-0.2, 0.2))
    elif k == 'press': add(pulse(1760, 0.04, 0.5, lin(0.04)), te + 0.01, 0.06)
    elif k == 'dot': add(pulse(nt(81), 0.035, 0.25, lin(0.035)), te, 0.05, 0.1)
    elif k == 'save':
        mel = [(72, 0), (76, .09), (79, .18), (84, .27)]
        for m, dt in mel: add(pulse(nt(m), 0.085 if m != 84 else 0.55, 0.25, (lambda t: 0.9 + 0 * t) if m != 84 else dec(0.25)), te + dt, 0.09, -0.3)
        for m, dt in [(67, 0), (72, .09), (76, .18), (79, .27)]: add(pulse(nt(m), 0.085 if m != 79 else 0.5, 0.125, (lambda t: 0.8 + 0 * t) if m != 79 else dec(0.22)), te + dt, 0.06, 0.35)
        add(wavech(nt(48), 0.36, lin(0.36)), te, 0.1); add(wavech(nt(36), 0.6, dec(0.3)), te + 0.27, 0.12)
    elif k == 'off':
        add(pulse(0, 0.4, 0.5, lin(0.4), sweep=lambda t: 900 * np.exp(-t * 7) + 60), te, 0.06)
        add(noise(0.3, 4000, False, dec(0.1)), te, 0.03)

# output stage: DC blocker + gentle low-pass like a tiny speaker/headphone amp
def onepole(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); p = 0.0
    for i in range(len(x)): p = (1 - a) * x[i] + a * p; y[i] = p
    return y
out = []
for ch in (L, R):
    lp = onepole(ch, 9000); hp = lp - onepole(lp, 40); out.append(hp)
st = np.stack(out, 1)
fo = int(0.5 * SR); st[-fo:] *= np.linspace(1, 0, fo)[:, None]
st = np.tanh(st * 1.6) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
