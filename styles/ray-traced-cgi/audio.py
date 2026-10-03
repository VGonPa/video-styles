# events.json -> audio.wav (48 kHz stereo, 10 s). Everything is synthesised (no samples), in the
# manner of an early-90s workstation demo: keyboard clicks while the trace command is typed, soft
# square-wave bleeps for each band of scanlines, a warm detuned-saw pad (Juno-like) moving
# D maj9 -> G maj7 -> A6 -> B m7 -> D maj9, two-operator FM bells (DX7-like) on each bounce of the
# chrome ball (descending, softer as it settles) with a quiet FM arpeggio under the dolly, a
# band-passed noise whoosh for the dive into the mirror, an ascending FM pluck as each letter rises,
# a high shimmer for the lens flare and a final bell chord that rings out under the fade.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N); WL = np.zeros(N); WR = np.zeros(N); wet = (WL, WR)
rs = np.random.default_rng(140)
nt = lambda m: 440.0 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(d * SR)) / SR
def add(sig, t, g=1.0, pan=0.0, dst=None):
    i = int(round(t * SR)); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    l, r = (L, R) if dst is None else dst
    l[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; r[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def both(sig, t, g, pan, send):
    add(sig, t, g, pan); add(sig, t, g * send, pan, wet)
def lowpass(x, fc, q=0.0):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    H = 1 / np.sqrt(1 + (f / fc) ** 4)                        # 2-pole-ish magnitude response
    if q: H *= 1 + q * np.exp(-((f - fc) / (0.25 * fc)) ** 2)  # gentle resonance bump
    return np.fft.irfft(X * H, len(x))
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))

# ---- instruments
def click(lo=1800, hi=9000, d=0.012):
    t = tt(d); return band(rs.standard_normal(len(t)), lo, hi) * np.exp(-t / 0.0025)
def bleep(m, d=0.085, bright=7):
    t = tt(d); f = nt(m)
    sq = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 2 * bright, 2))
    return lowpass(sq, 2600) * np.minimum(1, t / 0.004) * np.exp(-t / 0.05) * 0.6
def saw_voice(f, t):
    ph = (f * t + rs.uniform()) % 1.0; return 2 * ph - 1
def pad(ms, d, att, rel, cut0=700, cut1=2200, det=(-0.11, 0.0, 0.09)):
    t = tt(d); s = np.zeros_like(t)
    for m in ms:
        for c in det: s += saw_voice(nt(m) * 2 ** (c / 12), t)
    s /= len(ms) * len(det)
    dark, bright = lowpass(s, cut0, 0.4), lowpass(s, cut1, 0.4)
    k = np.clip(t / max(d, 1e-3), 0, 1)
    out = dark * (1 - k) + bright * k                          # the filter opens across the chord
    return out * np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1)
def fm(m, d, ratio=3.5, index=4.0, decay=1.1, idecay=0.35):
    t = tt(d); f = nt(m)
    I = index * np.exp(-t / idecay) + 0.4
    s = np.sin(2 * np.pi * f * t + I * np.sin(2 * np.pi * f * ratio * t))
    return s * np.minimum(1, t / 0.002) * np.exp(-t / decay)
def epiano(m, d=0.6):
    t = tt(d); f = nt(m)
    s = np.sin(2 * np.pi * f * t + 1.3 * np.exp(-t / 0.15) * np.sin(2 * np.pi * f * t))
    return s * np.minimum(1, t / 0.003) * np.exp(-t / 0.28)
def thump(s):
    t = tt(0.35); f = 48 + 70 * np.exp(-t / 0.04); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.09) * np.minimum(1, t / 0.002)
def whoosh(d):
    t = tt(d + 0.45); k = np.clip(t / d, 0, 1)
    x = rs.standard_normal(len(t)); out = np.zeros_like(t)
    # sweep a band-pass by crossfading a few fixed bands (FFT filters are static)
    centres = [250, 500, 1000, 2000, 4000]
    pos = k * (len(centres) - 1)
    for j, c in enumerate(centres):
        w = np.clip(1 - np.abs(pos - j), 0, 1); out += band(x, c / 1.6, c * 1.6) * w
    env = k ** 2.2 * np.where(t < d, 1, np.exp(-(t - d) / 0.12))
    return out / np.abs(out).max() * env
def shimmer(d):
    t = tt(d + 0.8)
    s = sum(a * np.sin(2 * np.pi * nt(m) * t + rs.uniform(0, 6)) for m, a in [(93, .5), (98, .38), (100, .3), (105, .2), (110, .1)])
    sparkle = band(rs.standard_normal(len(t)), 6000, 12000) * 0.25
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5
    tail = np.where(t > d * 0.5, np.exp(-(t - d * 0.5) / 0.5), 1)
    return (s + sparkle) * np.maximum(env, 0) * tail * (0.75 + 0.25 * np.sin(2 * np.pi * 9 * t))

# ---- pad bed (chords follow the picture)
both(pad([50, 57, 61, 64, 66], 2.25, att=0.9, rel=0.25, cut0=500, cut1=1300), 1.15, 0.24, 0.0, 0.5)   # D maj9 under the trace
both(pad([43, 50, 54, 59, 62], 1.45, att=0.12, rel=0.2), 3.25, 0.17, -0.05, 0.5)                       # G maj7: playback
both(pad([45, 52, 54, 61, 64], 1.35, att=0.15, rel=0.2), 4.62, 0.17, 0.05, 0.5)                        # A6
both(pad([47, 54, 57, 62, 66], 1.4, att=0.2, rel=0.12, cut0=900, cut1=3800), 5.9, 0.17, 0.0, 0.6)      # B m7, opening into the dive
both(pad([38, 50, 57, 64, 66, 73], 2.75, att=0.06, rel=0.6, cut0=1800, cut1=1100), 7.25, 0.2, 0.0, 0.7)  # D maj9 for the logo

# ---- cues
ev = json.load(open('events.json'))
BAND_NOTES = [74, 78, 81, 86, 81, 78, 76, 79, 83, 86, 88, 90]
ARP = {3.25: [67, 71, 74, 78], 4.62: [69, 73, 76, 78]}
BELLS = [86, 81, 78, 74, 69, 66]
PLUCK = [74, 78, 81, 85, 86]
for e in ev:
    k, te = e['k'], e['t']
    if k == 'key': both(click(), te, 0.22, rs.uniform(-0.25, 0.25), 0.15)
    elif k == 'enter': both(click(600, 5000, 0.03), te, 0.3, 0.0, 0.2)
    elif k == 'line': both(bleep(93, 0.04, 3), te, 0.06, 0.15, 0.3)
    elif k == 'band': both(bleep(BAND_NOTES[e['i'] % 12]), te, 0.2, -0.25 if e['i'] % 2 else 0.25, 0.35)
    elif k == 'done': both(bleep(81, 0.07), te, 0.15, 0.0, 0.4); both(bleep(86, 0.14), te + 0.09, 0.15, 0.0, 0.4)
    elif k == 'lift':
        t = tt(0.3); f = 220 * 2 ** (t / 0.3 * 1.2)
        both(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.3) ** 2, te, 0.05, 0.0, 0.5)
    elif k == 'bounce':
        s = e['s']; m = BELLS[min(e['i'], len(BELLS) - 1)]
        both(fm(m, 2.2, decay=0.9 + 0.4 * s), te, 0.2 * (0.35 + 0.65 * s), 0.1, 0.5)
        both(thump(s), te, 0.26 * s, 0.0, 0.1)
    elif k == 'breath': both(whoosh(0.3)[::-1][: int(0.3 * SR)], te, 0.05, 0.0, 0.4)
    elif k == 'dive': both(whoosh(e['d']), te, 0.32, 0.0, 0.5)
    elif k == 'cut': both(thump(1.0), te, 0.35, 0.0, 0.3); both(fm(74, 2.5, ratio=2.0, index=2.0, decay=1.3), te, 0.07, 0.0, 0.8)
    elif k == 'letter': both(fm(PLUCK[e['i']], 1.4, ratio=1.0, index=2.5, decay=0.45, idecay=0.08), te, 0.13, -0.5 + 0.25 * e['i'], 0.5)
    elif k == 'chord':
        for j, (m, g) in enumerate([(62, .16), (69, .12), (74, .11), (78, .09), (81, .08), (88, .05)]):
            both(fm(m, 2.6, ratio=3.5, index=2.5, decay=1.4), te + 0.012 * j, g, -0.3 + 0.12 * j, 0.7)
    elif k == 'flare':
        sh = shimmer(e['d']); n = len(sh); pan = np.linspace(-0.6, 0.6, n)
        i0 = int(te * SR); n = min(n, N - i0)
        for dst, g in (((L, R), 0.07), (wet, 0.09)):
            dst[0][i0:i0 + n] += sh[:n] * g * np.sqrt(0.5 - pan[:n] / 2) * 1.414
            dst[1][i0:i0 + n] += sh[:n] * g * np.sqrt(0.5 + pan[:n] / 2) * 1.414
# quiet FM arpeggio under the playback and dolly
for t0, notes in ARP.items():
    for j in range(7):
        both(epiano(notes[j % 4] + 12 * (j // 4)), t0 + 0.07 + 0.2 * j, 0.045, -0.3 if j % 2 else 0.3, 0.5)

# ---- hall: decaying stereo noise IR (~2.6 s), FFT convolution
ir_t = tt(2.6); M = 1 << int(np.ceil(np.log2(N + len(ir_t))))
for dry, w_, seed in ((L, WL, 1), (R, WR, 2)):
    ir = np.random.default_rng(seed).standard_normal(len(ir_t)) * np.exp(-ir_t / 0.7); ir = band(ir, 60, 8000); ir /= np.sqrt(np.sum(ir ** 2))
    rev = np.fft.irfft(np.fft.rfft(w_, M) * np.fft.rfft(ir, M), M)[:N]
    dry += w_ * 0.5 + rev * 0.5
# master: tiny fade in, fade out with the picture (9.3 -> 10 s)
fi = int(0.02 * SR); fo0 = int(9.3 * SR)
for ch in (L, R):
    ch[:fi] *= np.linspace(0, 1, fi)
    ch[fo0:] *= np.linspace(1, 0, N - fo0) ** 1.6
st = np.stack([L, R], 1); pk = np.abs(st).max(); st = np.tanh(st / pk * 1.2) * 0.84
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok, peak before norm', round(float(pk), 3))
