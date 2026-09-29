# events.json → audio.wav (48 kHz stereo, 10 s)
# A small cool-jazz combo for a 1950s cartoon: walking upright bass locked to the gentleman's footsteps, brushes on
# the snare and a swung ride, vibraphone stabs as buildings pop up, a two-tone car horn, a woodblock when he stops,
# a muted-horn "ta-da" for the hat tip, an upward glissando and cymbal for the starburst, a vibraphone arpeggio for the
# title letters, horn stabs on WAY, then the bass walks him off and the band lands on a soft Fmaj9.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(110)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        pan = float(np.clip(pan, -1, 1))
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)

def bass(f, d=0.6):
    t = tt(d); env = np.exp(-t * 5.5) * np.minimum(1, t / 0.004)
    s = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(4 * np.pi * f * t) * np.exp(-t * 9) + 0.2 * np.sin(6 * np.pi * f * t) * np.exp(-t * 14)
    thump = band(rs.standard_normal(len(t)), 60, 400) * np.exp(-t / 0.012) * 0.6
    return s * env + thump
def vibe(f, d=1.4, trem=5.5):
    t = tt(d); s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 12) + 0.08 * np.sin(2 * np.pi * f * 10 * t) * np.exp(-t * 30)
    return s * np.exp(-t * 2.2) * (1 - 0.35 * (0.5 + 0.5 * np.sin(2 * np.pi * trem * t))) * np.minimum(1, t / 0.002)
def horn(f, d=0.45, wah=1.0):
    # muted trumpet: additive saw with a closing lowpass-like rolloff
    t = tt(d); s = np.zeros(len(t)); vib = 1 + 0.006 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t / 0.2)
    for h in range(1, 14):
        cut = 900 + 2200 * wah * np.exp(-t * 6) ; amp = 1 / h * np.exp(-(h * f / cut) ** 2)
        s += amp * np.sin(2 * np.pi * f * h * t * vib)
    env = np.minimum(1, t / 0.02) * np.exp(-t * 2) * np.minimum(1, (d - t) / 0.05)
    return s * env
def brush(d=0.18):
    t = tt(d); return band(rs.standard_normal(len(t)), 2000, 11000) * np.exp(-t / 0.05) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.3
def ride(d=0.9):
    t = tt(d); s = sum(np.sign(np.sin(2 * np.pi * f * t)) for f in [587, 845, 1127, 1467, 1823, 2491])
    return band(s, 3500, 14000) * np.exp(-t * 4.5) * np.minimum(1, t / 0.001)
def woodblock(f=900):
    t = tt(0.12); return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.018) + 0.4 * np.sin(2 * np.pi * f * 2.7 * t) * np.exp(-t / 0.008)
def step(soft=0):
    t = tt(0.09); return band(rs.standard_normal(len(t)), 150, 1800 if not soft else 1200) * np.exp(-t / 0.014)
def honk():
    t = tt(0.32); out = np.zeros(len(t))
    for f in (392, 494):
        s = np.zeros(len(t))
        for h in range(1, 9): s += np.sin(2 * np.pi * f * h * t) / h * (1 if h % 2 else 0.5)
        out += s
    return out * np.minimum(1, t / 0.01) * np.minimum(1, (0.32 - t) / 0.04)
def whoosh(d, lo=300, hi=3000):
    t = tt(d); return norm(band(rs.standard_normal(len(t)), lo, hi)) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5

ev = json.load(open('events.json'))
steps = [e for e in ev if e['k'] == 'step']
# walking bass: one note per footstep, a ii–V–I–VI walk in F with chromatic approaches
WALK = [43, 46, 48, 49, 48, 46, 45, 43, 41, 45, 48, 50, 51, 50, 48, 46, 45]
for i, e in enumerate([s for s in steps if not s.get('soft')]):
    add(bass(nt(WALK[i % len(WALK)])), e['t'], 0.34, -0.15); add(step(), e['t'], 0.06, 0.1)
EXIT = [41, 43, 45, 46, 48, 50, 52, 53]
end_t = next(e['t'] for e in ev if e['k'] == 'end')
for i, e in enumerate([s for s in steps if s.get('soft')]):
    if e['t'] < end_t - 0.05: add(bass(nt(EXIT[i % len(EXIT)])), e['t'], 0.28, -0.15)
    add(step(1), e['t'], 0.045, 0.3)
# swung ride + brushes during the walk and the exit
def swing(t0, t1, beat):
    b = t0; k = 0
    while b < t1:
        add(ride(), b, 0.022, 0.45); add(brush(0.22), b + beat * 0.02, 0.035, -0.3)
        if k % 2 == 1: add(ride(0.5), b + beat * 0.66, 0.014, 0.45)
        b += beat; k += 1
first = steps[0]['t'] if steps else 0.3
walk_steps = [s['t'] for s in steps if not s.get('soft')]
beat = walk_steps[1] - walk_steps[0] if len(walk_steps) > 1 else 0.45
swing(first, 4.05, beat)
exit_steps = [s['t'] for s in steps if s.get('soft')]
if len(exit_steps) > 1: swing(exit_steps[0], 9.2, exit_steps[1] - exit_steps[0])
VIB = [65, 69, 72, 76, 79, 77, 74, 72, 69, 67, 72, 76]
ri = 0
for e in ev:
    k, te, pan = e['k'], e['t'], e.get('pan', 0.0)
    if k == 'rise':
        add(vibe(nt(VIB[ri % len(VIB)]), 1.0), te, 0.05, pan * 0.8); add(woodblock(700 + 90 * (ri % 5)), te, 0.03, pan * 0.8); ri += 1
    elif k == 'sun':
        for i, m in enumerate([77, 81, 84, 88]): add(vibe(nt(m), 1.2), te + i * 0.06, 0.04, 0.6)
    elif k == 'carIn': add(whoosh(0.55, 200, 2500), te, 0.07, 0.7)
    elif k == 'honk': add(honk(), te, 0.05, 0.4); add(honk(), te + 0.22, 0.04, 0.4)
    elif k == 'carOut': add(whoosh(0.6, 300, 4000), te, 0.09, -0.3)
    elif k == 'stop': add(woodblock(820), te, 0.1, 0.0); add(woodblock(620), te + 0.12, 0.08, 0.0)
    elif k == 'tip':
        add(horn(nt(72), 0.18), te, 0.05, 0.1); add(horn(nt(77), 0.55), te + 0.2, 0.06, 0.1)
        for m in (65, 69, 72, 76): add(vibe(nt(m), 1.2), te + 0.2, 0.03, -0.2)
    elif k == 'burst':
        for i in range(14): add(vibe(nt(60 + [0, 2, 4, 5, 7, 9, 11][i % 7] + 12 * (i // 7)), 0.5), te + i * 0.028, 0.04, -0.7 + i * 0.1)
        add(whoosh(0.7, 500, 6000), te, 0.07, 0.0); add(ride(2.2), te + 0.4, 0.07, 0.0); add(ride(2.2), te + 0.42, 0.05, -0.4)
        add(bass(nt(41), 1.5), te + 0.4, 0.4, 0.0)
    elif k == 'the': add(vibe(nt(72), 1.2), te, 0.05, -0.4)
    elif k == 'letter':
        idx = sum(1 for x in ev if x['k'] == 'letter' and x['t'] < te)
        add(vibe(nt([65, 69, 72, 76, 79, 81][idx % 6]), 1.3), te, 0.055, pan * 0.7); add(brush(0.12), te, 0.03, pan * 0.7)
    elif k == 'bigLetter':
        idx = sum(1 for x in ev if x['k'] == 'bigLetter' and x['t'] < te)
        for m in [[53, 57, 64], [55, 58, 65], [57, 60, 67, 72]][idx % 3]: add(horn(nt(m + 12), 0.34 if idx < 2 else 0.9, 0.8), te, 0.035, pan * 0.6)
        add(bass(nt([41, 43, 45][idx % 3]), 0.7), te, 0.3, 0.0)
    elif k == 'script':
        for i in range(9): add(vibe(nt([84, 88][i % 2]), 0.5, 7), te + i * 0.1, 0.018, 0.2 + 0.05 * i)
    elif k == 'hatBack': add(woodblock(980), te, 0.07, 0.4)
    elif k == 'end':
        for i, m in enumerate([41, 57, 64, 67, 69, 72]):
            add((bass if m < 50 else vibe)(nt(m), 2.2 if m >= 50 else 1.8), te + i * 0.05, 0.3 if m < 50 else 0.05, -0.3 + i * 0.12)
        add(ride(2.5), te, 0.03, 0.4)
fi = int(0.05 * SR); fo = int(1.0 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.6
st = np.stack([L, R], 1); st = np.tanh(st * 2.2) * 0.85
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
