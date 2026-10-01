# events.json → audio.wav (48 kHz stereo, 10 s)
# a back street at dusk: distant traffic bed, the stencil sliding onto brick, masking tape slapped down,
# the rattle of the mixing ball, spray-can hiss swelling and easing with each pass, tape ripped off,
# board peeled from the wall, a small glass "tink" when the bulb is revealed, a whoosh as the camera pulls back.
import json, wave, numpy as np
SR, DUR = 48000, 10.0
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(125)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(sig), N - i)
    if n > 0 and i >= 0:
        L[i:i + n] += sig[:n] * g * np.sqrt(0.5 - pan / 2) * 1.414; R[i:i + n] += sig[:n] * g * np.sqrt(0.5 + pan / 2) * 1.414
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tt(d): return np.arange(int(d * SR)) / SR
def norm(x): return x / (np.abs(x).max() + 1e-9)
def lowpass_sweep(x, fc):
    y = np.zeros_like(x); p = 0.0; a = np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y
def slide(d):
    # board dragged over brick: rough low-mid noise with grainy amplitude
    t = tt(d); x = norm(band(rs.standard_normal(len(t)), 250, 3500))
    am = np.abs(band(rs.standard_normal(len(t)), 20, 90)); am = norm(am)
    return x * (0.5 + 0.5 * am) * np.sin(np.pi * t / d) ** 0.8
def tape():
    t = tt(0.16); n = norm(band(rs.standard_normal(len(t)), 600, 6000)) * np.exp(-t / 0.018)
    thump = np.sin(2 * np.pi * 120 * t) * np.exp(-t / 0.03)
    return n * 0.8 + thump * 0.6
def rip():
    # tape tearing: dense crackle burst
    t = tt(0.2); cr = (rs.random(len(t)) < 0.12) * rs.standard_normal(len(t))
    x = norm(band(cr + 0.3 * rs.standard_normal(len(t)), 1500, 9000))
    return x * np.minimum(1, t / 0.01) * np.exp(-t / 0.07)
def rattle(d):
    # mixing ball knocking inside the can, ~13 knocks per second
    out = np.zeros(int(d * SR) + SR // 5); k = 0.0
    while k < d:
        t = tt(0.05); f = 2600 + rs.uniform(-300, 300)
        clk = (np.sin(2 * np.pi * f * t) + 0.6 * np.sin(2 * np.pi * f * 1.52 * t)) * np.exp(-t / 0.006)
        clk += 0.5 * norm(band(rs.standard_normal(len(t)), 3000, 9000)) * np.exp(-t / 0.002)
        i = int(k * SR); out[i:i + len(t)] += clk * (0.7 + 0.3 * rs.random()); k += 1 / 13 + rs.uniform(-0.008, 0.008)
    return out
def hiss(d, ink):
    # pressurised spray: bright noise, quick attack, row-by-row swell, sputter at release
    t = tt(d + 0.12); x = rs.standard_normal(len(t))
    lo, hi = (2200, 11000) if ink == 'k' else (1800, 9500)
    x = norm(band(x, lo, hi)) + 0.25 * norm(band(rs.standard_normal(len(t)), 400, 1500))
    rows = 9 if d > 1.0 else 4
    sw = 0.75 + 0.25 * np.abs(np.sin(np.pi * rows * t / d))
    env = np.minimum(1, t / 0.025) * np.where(t < d, 1.0, np.exp(-(t - d) / 0.03)) * sw
    return x * env
def peel(d):
    t = tt(d); cr = (rs.random(len(t)) < 0.03) * rs.standard_normal(len(t)) * 3
    x = norm(band(rs.standard_normal(len(t)) * 0.4 + cr, 500, 7000))
    sweep = lowpass_sweep(rs.standard_normal(len(t)), 300 + 3000 * (t / d))
    return (x * 0.7 + norm(sweep) * 0.5) * np.sin(np.pi * t / d) ** 0.6
def whoosh(d):
    t = tt(d); y = lowpass_sweep(rs.standard_normal(len(t)), 150 + 1800 * np.sin(np.pi * t / d) ** 2)
    return norm(y) * np.sin(np.pi * t / d) ** 1.5
def ping(f):
    t = tt(1.4); s = sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (0.5 / h ** 0.5)) for h, a in [(1, 1), (2.76, .35), (5.4, .15)])
    return s * np.minimum(1, t / 0.002)
# bed: distant traffic rumble + air, swelling a touch at the end
t = np.arange(N) / SR
rum = norm(band(rs.standard_normal(N), 30, 220)) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.13 * t))
air = norm(band(rs.standard_normal(N), 300, 2500))
L += rum * 0.05 + air * 0.006; R += np.roll(rum, 2400) * 0.05 + np.roll(air, 999) * 0.006
car = norm(band(rs.standard_normal(int(3.0 * SR)), 80, 900)) * np.sin(np.pi * tt(3.0) / 3.0) ** 2
add(car, 5.6, 0.035, 0.6)
for e in json.load(open('events.json')):
    k, te, v = e['k'], e['t'], e.get('v', 1.0)
    if k == 'slide': add(slide(e['d']), te, 0.09 * v, -0.2)
    elif k == 'tape': add(tape(), te, 0.18, rs.uniform(-.4, .4))
    elif k == 'rip': add(rip(), te, 0.16, rs.uniform(-.4, .4))
    elif k == 'rattle': add(rattle(e['d']), te, 0.12, 0.3)
    elif k == 'hiss': add(hiss(e['d'], e['ink']), te, 0.13, 0.15)
    elif k == 'peel': add(peel(e['d']), te, 0.16 * v, -0.15)
    elif k == 'whoosh': add(whoosh(e['d']), te, 0.12)
    elif k == 'ping': add(ping(e['f']), te, 0.05 * v, 0.2)
# master: fade in/out, soft limiter
fi = int(0.3 * SR); fo = int(0.7 * SR)
for ch in (L, R): ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L, R], 1); st = np.tanh(st * 3.4) * 0.9
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio.wav ok', np.abs(st).max().round(3))
