#!/usr/bin/env python3
"""Check the soundtrack audio.py wrote: length, peak, and whether it is silent or ends early.

  python3 scripts/check_audio.py my-project/audio.wav [seconds]

Most styles' audio.py print only "audio.wav ok", even when a NaN (from a pan pushed past ±1, a zero-length ramp
or a division by zero) has turned the whole mix into silence or a constant value. This reads the file itself.
Pass the film's length to also check that the file is that long. Exits 1 when the track is silent, constant,
or the wrong length. Needs Python 3.8+ and NumPy.
"""

import sys
import wave

import numpy as np


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    path = sys.argv[1]
    try:
        with wave.open(path, "rb") as w:
            rate, channels, width = w.getframerate(), w.getnchannels(), w.getsampwidth()
            raw = w.readframes(w.getnframes())
    except (OSError, wave.Error) as err:
        sys.exit(f"cannot read {path}: {err}")
    if width != 2:
        sys.exit(f"{path}: expected 16-bit PCM, found {8 * width}-bit")
    pcm = np.frombuffer(raw, dtype="<i2").reshape(-1, channels).astype(np.float64) / 32767
    seconds = len(pcm) / rate
    level = np.abs(pcm).max(axis=1)
    peak = float(level.max()) if len(level) else 0.0
    loud = np.nonzero(level > 0.001)[0]
    last = (loud[-1] + 1) / rate if len(loud) else 0.0
    print(f"{path}: {seconds:.2f} s, {channels} ch, {rate} Hz, peak {peak:.3f}, last sound at {last:.2f} s")

    problems = []
    ends = [((np.nonzero(np.abs(pcm[:, c]) > 0.001)[0][-1:] + 1) / rate).sum() for c in range(channels)]
    if channels > 1 and peak >= 0.001 and max(ends) - min(ends) > max(1.0, 0.25 * seconds):
        quiet = "LR"[int(np.argmin(ends))] if channels == 2 else str(int(np.argmin(ends)))
        problems.append(f"channel {quiet} goes silent at {min(ends):.2f} s while another sounds to {max(ends):.2f} s: "
                        "a NaN in that channel usually causes this")
    if channels > 1 and peak >= 0.001:
        # A NaN in one cue zeroes that channel exactly (astype int16) for the cue's length while the other plays on.
        block = int(rate * 0.05)
        n = len(pcm) // block
        if n:
            blocks = np.abs(pcm[: n * block]).reshape(n, block, channels)
            dead = (blocks.max(axis=1) == 0) & (blocks.max(axis=(1, 2)) > 0.01)[:, None]
            hits = np.nonzero(dead.any(axis=1))[0]
            if len(hits) >= 2:
                c = "LR"[int(np.nonzero(dead[hits[0]])[0][0])] if channels == 2 else "?"
                problems.append(f"channel {c} is exactly silent at {hits[0] * block / rate:.2f} s while the other "
                                "plays: a NaN in one cue (a pan past ±1) usually causes this")
    if peak < 0.001:
        problems.append("silent: a NaN in the mix (a pan past ±1, a zero-length ramp) usually causes this")
    elif len(pcm) > 1 and float(pcm.std(axis=0).max()) < 1e-6:
        problems.append("constant value, not sound: a NaN in the mix usually causes this")
    if len(sys.argv) == 3:
        want = float(sys.argv[2])
        if abs(seconds - want) > 0.05:
            problems.append(f"length {seconds:.2f} s, expected {want:.2f} s: set DUR in audio.py")
        elif peak >= 0.001 and last < want - 1.5:
            print(f"note: nothing sounds after {last:.2f} s of {want:.2f} s; check that the score covers the film")
    for p in problems:
        print("FAIL", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
