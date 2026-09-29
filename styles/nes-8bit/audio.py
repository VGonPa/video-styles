# events.json → audio.wav (48 kHz stereo, 10 s)
# Chiptune in the style of a third-generation console sound chip: two pulse channels
# (12.5 / 25 / 50 % duty), a 4-bit stepped triangle bass and a 15-bit LFSR noise channel.
# Title jingle, stage theme, boss theme, "level clear" fanfare + sound effects (jump, coffee pickup,
# hit, boss drop/thud, HP fill ticks, email volley, power-up, stomp, explosions, flag, tally blips).
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR)
MIX = np.zeros(N)
nt = lambda m: 440.0 * 2 ** ((m - 69) / 12)

def put(sig, t, g=1.0):
    i = int(round(t * SR)); n = min(len(sig), N - i)
    if n > 0 and i >= 0: MIX[i:i + n] += sig[:n] * g

def pulse(freq, d, duty=0.5):
    f = np.broadcast_to(np.asarray(freq, float), (int(d * SR),))
    ph = np.cumsum(f) / SR
    return np.where(ph % 1.0 < duty, 1.0, -1.0)

def tri(freq, d):
    f = np.broadcast_to(np.asarray(freq, float), (int(d * SR),))
    ph = np.cumsum(f) / SR % 1.0
    x = 1 - 4 * np.abs(ph - 0.5)          # -1..1
    return np.round((x + 1) * 7.5) / 7.5 - 1  # 16 steps, like the hardware sequencer

# 15-bit LFSR noise
reg, seq = 1, np.zeros(32767)
for i in range(32767):
    b = (reg ^ (reg >> 1)) & 1; reg = (reg >> 1) | (b << 14); seq[i] = 1.0 if reg & 1 else -1.0
def noise(rate, d):
    n = int(d * SR); idx = (np.floor(np.arange(n) / SR * rate).astype(int)) % 32767
    return seq[idx]

def env(n, a=0.002, dec=None, sus=1.0, d=None):
    t = np.arange(n) / SR; e = np.minimum(1, t / a) if a > 0 else np.ones(n)
    if dec: e = e * (sus + (1 - sus) * np.exp(-t / dec))
    return np.round(e * 15) / 15             # 4-bit volume steps

def note(ch, m, d, g, duty=0.5, dec=0.12, sus=0.45):
    if m is None: return None
    f = nt(m); n = int(d * SR)
    s = pulse(f, d, duty) if ch == 'p' else tri(f, d)
    e = env(n, 0.003, dec, sus) if ch == 'p' else np.ones(n)
    rel = min(n, int(0.012 * SR)); e[-rel:] *= np.linspace(1, 0, rel)
    return s * e * g

def seqplay(t0, step, notes, ch, g, duty=0.5, t_end=99, gate=0.9, dec=0.12, sus=0.45):
    t = t0
    for m in notes:
        ln = 1
        if isinstance(m, tuple): m, ln = m
        if t >= t_end: break
        d = min(step * ln * gate, t_end - t)
        s = note(ch, m, d, g, duty, dec, sus)
        if s is not None: put(s, t)
        t += step * ln

def hat(t, g=0.05): n = noise(28000, 0.03); put(n * env(len(n), 0.001, 0.008, 0), t, g)
def snare(t, g=0.09): n = noise(9000, 0.12); put(n * env(len(n), 0.001, 0.035, 0), t, g)
def kick(t, g=0.2): d = 0.09; f = 180 * np.exp(-np.arange(int(d * SR)) / SR * 40) + 45; put(tri(f, d) * env(int(d * SR), 0.001, 0.04, 0), t, g)

EV = json.load(open('events.json'))
mus = [e for e in EV if e['k'] in ('music', 'stop', 'fanfare')]

# ── title jingle (C major arpeggio up into a held C) ──
T = next(e['t'] for e in EV if e['k'] == 'music' and e['s'] == 'title')
seqplay(T, 0.075, [72, 76, 79, 84, 79, 84, 88, None, (91, 4)], 'p', 0.11, 0.25, dec=0.1, sus=0.5)
seqplay(T, 0.075, [60, 64, 67, 72, 67, 72, 76, None, (79, 4)], 'p', 0.06, 0.125)
put(tri(nt(48), 0.8) * np.linspace(1, 0.6, int(0.8 * SR)), T, 0.2)

# ── stage theme: 150 bpm, eighth = 0.2 s ──
L0 = next(e['t'] for e in EV if e['k'] == 'music' and e['s'] == 'level')
LEND = next(e['t'] for e in EV if e['k'] == 'stop')
E8 = 0.2
lead = [76, 79, 84, 79, 81, 79, 76, 72, 74, 76, 77, 79, (81, 2), (79, 2), 76, 79, 84, 86, (88, 4)]
bass = [48, 60, 48, 60, 53, 65, 53, 65, 55, 67, 55, 67, 48, 60, 48, 60, 53, 65, 55, 67, 48, 60, 48, 60]
chords = [[60, 64, 67], [65, 69, 72], [67, 71, 74], [60, 64, 67], [65, 69, 72], [67, 71, 74]]
seqplay(L0, E8, lead, 'p', 0.10, 0.25, LEND)
seqplay(L0, E8, bass, 't', 0.22, t_end=LEND, gate=0.8)
arp = [c[i % 3] for c in chords for i in range(8)]
seqplay(L0, E8 / 2, arp, 'p', 0.035, 0.125, LEND, dec=0.05, sus=0.2)
k = 0; t = L0
while t < LEND - 0.01:
    hat(t); (snare if k % 4 == 2 else kick if k % 4 == 0 else (lambda *_: None))(t); t += E8; k += 1

# ── boss theme: 16th = 0.075 s, A minor, driving ──
B0 = next(e['t'] for e in EV if e['k'] == 'music' and e['s'] == 'boss')
BEND = [e['t'] for e in EV if e['k'] == 'stop'][1]
S16 = 0.075
blead = [69, 69, 72, 69, 75, 74, 72, 69, 69, 69, 72, 69, 76, 75, 74, 72] * 2
seqplay(B0, S16, blead, 'p', 0.09, 0.5, BEND, gate=0.7, dec=0.06, sus=0.5)
seqplay(B0, S16, [45, 57] * 16, 't', 0.22, t_end=BEND, gate=0.7)
k = 0; t = B0
while t < BEND - 0.01:
    hat(t, 0.04); (snare(t) if k % 8 == 4 else kick(t) if k % 8 == 0 else None); t += S16; k += 1

# ── level clear fanfare ──
FF = next(e['t'] for e in EV if e['k'] == 'fanfare')
seqplay(FF, 0.09, [67, 72, 76, 79, 84, 88, (91, 3), (88, 3), (91, 8)], 'p', 0.11, 0.25, dec=0.2, sus=0.55)
seqplay(FF, 0.09, [64, 67, 72, 76, 79, 84, (88, 3), (84, 3), (88, 8)], 'p', 0.05, 0.125, dec=0.2, sus=0.5)
seqplay(FF, 0.09, [48, 55, 60, 55, 48, 55, (60, 3), (55, 3), (48, 8)], 't', 0.24, gate=0.95)
snare(FF + 0.54, 0.06); snare(FF + 0.81, 0.08)

# ── sound effects ──
def sweep(f0, f1, d, duty=0.5, curve=1.0):
    n = int(d * SR); s = np.linspace(0, 1, n) ** curve; return pulse(f0 + (f1 - f0) * s, d, duty)
for e in EV:
    k, t = e['k'], e['t']
    if k == 'start':
        for i, m in enumerate([84, 91, 96]): put(pulse(nt(m), 0.06, 0.5) * env(int(0.06 * SR), 0.002, 0.03, 0.3), t + i * 0.06, 0.1)
    elif k == 'jump':
        s = sweep(260, 900, 0.16, 0.5, 0.6); put(s * env(len(s), 0.002, 0.1, 0.3), t, 0.09)
    elif k == 'coin':
        put(pulse(nt(83), 0.06, 0.25) * 1.0, t, 0.08); s = pulse(nt(88), 0.3, 0.25); put(s * env(len(s), 0.002, 0.09, 0), t + 0.06, 0.1)
    elif k == 'hurt':
        d = 0.42; n = int(d * SR); tt = np.arange(n) / SR
        s = pulse((900 - 700 * tt / d) * (1 + 0.06 * np.sign(np.sin(2 * np.pi * 24 * tt))), d, 0.5); put(s * env(n, 0.002, 0.25, 0.2), t, 0.1)
    elif k == 'drop':
        s = sweep(1600, 260, 0.35, 0.125); put(s * env(len(s), 0.002, 0.3, 0.5), t, 0.08)
    elif k == 'thud':
        n = noise(1800, 0.45); put(n * env(len(n), 0.001, 0.12, 0), t, 0.16)
        d = 0.3; f = 140 * np.exp(-np.arange(int(d * SR)) / SR * 9) + 30; put(tri(f, d) * env(int(d * SR), 0.001, 0.15, 0), t, 0.3)
    elif k in ('tick', 'tickd'):
        put(pulse(1400 if k == 'tick' else 700, 0.02, 0.5), t, 0.06)
    elif k == 'shoot':
        s = sweep(700, 250, 0.08, 0.25); put(s * env(len(s), 0.001, 0.05, 0), t, 0.07); hat(t, 0.05)
    elif k == 'pop':
        n = noise(14000, 0.1); put(n * env(len(n), 0.001, 0.03, 0), t, 0.08)
    elif k == 'power':
        for i, m in enumerate([72, 76, 79, 84, 88, 91, 96]): put(pulse(nt(m), 0.04, 0.125), t + i * 0.035, 0.07)
    elif k == 'stomp':
        s = sweep(200, 1000, 0.1, 0.5); put(s * env(len(s), 0.001, 0.06, 0), t, 0.1); n = noise(5000, 0.12); put(n * env(len(n), 0.001, 0.04, 0), t, 0.1)
    elif k == 'boom':
        n = noise(2600, 0.3); put(n * env(len(n), 0.001, 0.08, 0), t, 0.11)
    elif k == 'rise':
        for i in range(8): put(pulse(nt(60 + i * 2), 0.025, 0.25), t + i * 0.031, 0.06)
    elif k == 'flag':
        s = sweep(400, 1600, 0.23, 0.125, 1.5); put(s * env(len(s), 0.002, 0.3, 0.6), t, 0.07)
    elif k == 'tally':
        put(pulse(1760, 0.025, 0.5), t, 0.05)

# master: DC-block high-pass (~90 Hz) + gentle low-pass, like the console's output stage; fades
y = np.zeros(N); a = np.exp(-2 * np.pi * 90 / SR); px = py = 0.0
b = np.exp(-2 * np.pi * 12000 / SR); lp = 0.0
for i in range(N):
    x = MIX[i]; py = a * (py + x - px); px = x; lp = (1 - b) * py + b * lp; y[i] = lp
fi, fo = int(0.05 * SR), int(0.5 * SR)
y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo)
y = np.tanh(y * 1.6) * 0.75
st = np.stack([y, y], 1)
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
