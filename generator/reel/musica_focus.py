"""Tappeto musicale "da concentrazione" generato da zero (nessun diritto di terzi).
Uso: python3 musica_focus.py <durata_secondi> <file_uscita.wav>
Stile: lo-fi calmo, 72 bpm, piano elettrico morbido, basso tondo, batteria appena accennata.
"""
import sys
import numpy as np
import soundfile as sf

SR = 48000
dur = float(sys.argv[1])
out = sys.argv[2]
n = int(SR * dur)
t = np.arange(n) / SR
beat = 60 / 72
rng = np.random.default_rng(7)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def place(buf, sig, at, gain=1.0):
    i = int(at * SR)
    if i >= n:
        return
    j = min(n, i + len(sig))
    buf[i:j] += sig[: j - i] * gain


def epiano(m, length=3.2):
    x = np.arange(int(SR * length)) / SR
    f = hz(m)
    body = np.sin(2 * np.pi * f * x) + 0.35 * np.sin(2 * np.pi * 2 * f * x) * np.exp(-x * 3)
    bell = 0.12 * np.sin(2 * np.pi * 4 * f * x) * np.exp(-x * 9)
    env = (1 - np.exp(-x * 220)) * np.exp(-x / 1.5)
    trem = 1 + 0.06 * np.sin(2 * np.pi * 4.5 * x)
    return (body + bell) * env * trem


def bass(m, length=1.4):
    x = np.arange(int(SR * length)) / SR
    f = hz(m)
    return (np.sin(2 * np.pi * f * x) + 0.2 * np.sin(2 * np.pi * 2 * f * x)) * (1 - np.exp(-x * 120)) * np.exp(-x / 0.7)


def kick():
    x = np.arange(int(SR * 0.22)) / SR
    f = 45 + 55 * np.exp(-x * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 16)


def noise_hit(length, decay):
    x = np.arange(int(SR * length)) / SR
    w = rng.standard_normal(len(x))
    w = np.convolve(w, np.ones(6) / 6, mode="same")      # soften the highs
    return w * np.exp(-x * decay)


# Dm9, G13, Cmaj9, Am9: sequenza distesa, senza tensione
chords = [[50, 57, 60, 64, 65], [43, 53, 59, 64, 69], [48, 55, 59, 62, 64], [45, 55, 60, 64, 71]]
L = np.zeros(n)
R = np.zeros(n)
bars = int(dur / (4 * beat)) + 1
for b in range(bars):
    ch = chords[b % len(chords)]
    t0 = b * 4 * beat
    for k, m in enumerate(ch[1:]):
        pan = 0.35 + 0.1 * k
        late = k * 0.018                                   # leggero arpeggio "umano"
        for at, g in ((t0 + late, 0.55), (t0 + 2.5 * beat + late, 0.3)):
            s = epiano(m + 12)
            place(L, s, at, g * (1 - pan))
            place(R, s, at, g * pan)
    for at, g in ((t0, 0.9), (t0 + 2.5 * beat, 0.55)):
        s = bass(ch[0] - 12)
        place(L, s, at, g * 0.5)
        place(R, s, at, g * 0.5)
    for q in range(4):
        at = t0 + q * beat
        if q in (0, 2):
            k_ = kick()
            place(L, k_, at, 0.45)
            place(R, k_, at, 0.45)
        else:
            s = noise_hit(0.12, 28)
            place(L, s, at, 0.10)
            place(R, s, at, 0.10)
        h = noise_hit(0.04, 90)
        place(L, h, at + beat / 2, 0.04)
        place(R, h, at + beat / 2, 0.05)

x = np.stack([L, R], 1)
fade = np.clip(t / 0.8, 0, 1) * np.clip((dur - t) / 2.0, 0, 1)
x *= fade[:, None]
x /= np.abs(x).max() * 1.3
sf.write(out, x, SR)
