# xy.f32 → audio.wav (48 kHz stereo, 10 s). The soundtrack is the deflection signal itself: left = X, right = Y.
# What you hear is what the beam draws: the time base spinning up out of the subsonic range, the trace's pitch rising
# with the FREQ knob, the Lissajous chords (3:4 = a fourth, 2:3 = a fifth), the 110 Hz buzz of the cube and the
# word, and silence once the beam is parked on the dot. Only gentle conditioning is applied: a DC blocker (the beam's
# resting offset is inaudible anyway), a soft low-pass to take the edge off the vector paths' corners, a short
# fade at both ends, and a peak normalisation to about -8.5 dBFS.
import wave, numpy as np
SR = 48000
xy = np.fromfile('xy.f32', dtype=np.float32).astype(np.float64).reshape(-1, 2)
def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); p = 0.0
    for i in range(len(x)): p = (1 - a) * x[i] + a * p; y[i] = p
    return y
def dc_block(x, fc=18.0):
    r = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); px = py = 0.0
    for i in range(len(x)): py = x[i] - px + r * py; px = x[i]; y[i] = py
    return y
out = []
for ch in (xy[:, 0], xy[:, 1]):
    s = dc_block(ch)
    s = onepole_lp(onepole_lp(s, 3000), 3000)
    out.append(s)
L, R = out
n = len(L); t = np.arange(n) / SR
fade = np.clip(t / 0.03, 0, 1) * np.clip((n / SR - t) / 0.08, 0, 1)
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max()) + 1e-9
g = 10 ** (-8.5 / 20) / peak
st = np.stack([L * g, R * g], 1)
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(st, -1, 1) * 32767).astype('<i2').tobytes())
print('audio: peak %.1f dBFS, rms L %.1f R %.1f dBFS' % (20 * np.log10(np.abs(st).max()), 20 * np.log10(np.sqrt((st[:, 0] ** 2).mean())), 20 * np.log10(np.sqrt((st[:, 1] ** 2).mean()))))
