"""Sottofondo di musica classica per i reel, suonato da zero (nessuna registrazione di terzi).
Brani di pubblico dominio: Bach (1722), Pachelbel (ca. 1680), Satie (1888).
Uso: python3 musica_classica.py <bach|satie|pachelbel> <durata_secondi> <file_uscita.wav>
"""
import sys
import numpy as np
import soundfile as sf

SR = 48000
brano, dur, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
n = int(SR * (dur + 2.5))
L = np.zeros(n)
R = np.zeros(n)
rng = np.random.default_rng(11)
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def m(name):
    """'F#4' -> numero MIDI"""
    p = NOTE[name[0]]
    rest = name[1:]
    if rest[0] in "#b":
        p += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    return 12 * (int(rest) + 1) + p


def hz(k):
    return 440 * 2 ** ((k - 69) / 12)


def place(sig, at, gain=1.0, pan=0.5):
    i = int(at * SR)
    if i >= n or i < 0:
        return
    j = min(n, i + len(sig))
    L[i:j] += sig[: j - i] * gain * (1 - pan)
    R[i:j] += sig[: j - i] * gain * pan


def piano(k, length=4.0, soft=1.0):
    x = np.arange(int(SR * length)) / SR
    f = hz(k)
    tau = 1.9 * 2 ** ((60 - k) / 30)
    s = np.zeros_like(x)
    for h in range(1, 8):
        fh = f * h * (1 + 0.0004 * h * h)
        if fh > 9000:
            break
        s += np.sin(2 * np.pi * fh * x + rng.uniform(0, 6.28)) * np.exp(-x / (tau / h ** 0.7)) / h ** (1.6 * soft)
    return s * (1 - np.exp(-x * 400))


def archi(k, length):
    x = np.arange(int(SR * (length + 0.6))) / SR
    f = hz(k) * (1 + 0.003 * np.sin(2 * np.pi * 5.2 * x) * np.clip(x / 0.5, 0, 1))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = sum(np.sin(h * ph) / h ** 1.7 for h in range(1, 7))
    env = np.clip(x / 0.25, 0, 1) * np.clip((length + 0.6 - x) / 0.6, 0, 1)
    return s * env


def pan_of(k):
    return float(np.clip(0.5 + (k - 60) / 90, 0.25, 0.75))


def hum():
    return rng.uniform(-0.008, 0.008)


if brano == "bach":
    # Preludio in do maggiore BWV 846: ogni battuta ripete due volte la stessa figura di otto note
    bars = ["C4 E4 G4 C5 E5", "C4 D4 A4 D5 F5", "B3 D4 G4 D5 F5", "C4 E4 G4 C5 E5", "C4 E4 A4 E5 A5",
            "C4 D4 F#4 A4 D5", "B3 D4 G4 D5 G5", "B3 C4 E4 G4 C5", "A3 C4 E4 G4 C5", "D3 A3 D4 F#4 C5",
            "G3 B3 D4 G4 B4", "G3 Bb3 E4 G4 C#5", "F3 A3 D4 A4 D5", "F3 Ab3 D4 F4 B4", "E3 G3 C4 G4 C5",
            "E3 F3 A3 C4 F4", "D3 F3 A3 C4 F4", "G2 D3 G3 B3 F4", "C3 E3 G3 C4 E4"]
    st = 0.21
    t, b = 0.3, 0
    while t < dur:
        k = [m(x) for x in bars[b % len(bars)].split()]
        for half in range(2):
            fig = [k[0], k[1], k[2], k[3], k[4], k[2], k[3], k[4]]
            for i, note in enumerate(fig):
                g = (0.5 if i == 0 else 0.34 if i == 1 else 0.3) * rng.uniform(0.9, 1.08)
                place(piano(note, 3.0 if i < 2 else 1.6), t + (half * 8 + i) * st + hum(), g, pan_of(note))
        t += 16 * st
        b += 1

elif brano == "satie":
    # Gymnopédie n. 1: basso sul primo tempo, accordo sul secondo, melodia sopra
    beat = 0.84
    acc = [("G2", "B3 D4 F#4"), ("D2", "A3 C#4 F#4")]
    mel = [(None, 1), ("F#5", 1), ("A5", 1), ("G5", 1), ("F#5", 1), ("C#5", 1), ("B4", 1), ("C#5", 1), ("D5", 1),
           ("A4", 3), ("F#4", 6)]
    t, b = 0.3, 0
    while t < dur:
        bass, ch = acc[b % 2]
        place(piano(m(bass), 5.0), t + hum(), 0.55, 0.45)
        for x in ch.split():
            place(piano(m(x), 4.0, 1.15), t + beat + hum(), 0.26, pan_of(m(x)))
        t += 3 * beat
        b += 1
    t = 0.3 + 2 * 3 * beat          # due battute di introduzione, poi la melodia
    i = 0
    while t < dur:
        note, ln = mel[i % len(mel)]
        if note:
            place(piano(m(note), 2.5 + ln, 0.9), t + hum(), 0.5, 0.6)
        t += ln * beat
        i += 1

elif brano == "pachelbel":
    # Canone in re: otto accordi, basso pizzicato, archi tenuti e la prima voce del canone
    step = 1.62
    prog = [("D3", "F#4 A4 D5", "F#5"), ("A2", "E4 A4 C#5", "E5"), ("B2", "D4 F#4 B4", "D5"),
            ("F#2", "C#4 F#4 A4", "C#5"), ("G2", "D4 G4 B4", "B4"), ("D2", "D4 F#4 A4", "A4"),
            ("G2", "D4 G4 B4", "B4"), ("A2", "E4 A4 C#5", "C#5")]
    t, b = 0.3, 0
    while t < dur:
        bass, ch, top = prog[b % 8]
        place(piano(m(bass), 2.5), t, 0.5, 0.5)
        place(piano(m(bass) + 12, 1.5), t + step / 2, 0.22, 0.5)
        for x in ch.split():
            place(archi(m(x), step), t, 0.075, pan_of(m(x)))
        if b >= 2:
            place(archi(m(top), step), t, 0.16, 0.62)
        t += step
        b += 1
else:
    sys.exit("brano sconosciuto: usa bach, satie o pachelbel")

# riverbero morbido da sala
ir_t = np.arange(int(SR * 1.6)) / SR
x = np.stack([L, R], 1)
wet = np.zeros_like(x)
for c in range(2):
    ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t / 0.45)
    ir = np.convolve(ir, np.ones(24) / 24, mode="same")
    N = 1 << int(np.ceil(np.log2(n + len(ir))))
    wet[:, c] = np.fft.irfft(np.fft.rfft(x[:, c], N) * np.fft.rfft(ir, N), N)[:n]
wet /= np.abs(wet).max() + 1e-9
x = x / (np.abs(x).max() + 1e-9) * 0.8 + wet * 0.28
x = x[: int(SR * dur)]
tt = np.arange(len(x)) / SR
x *= (np.clip(tt / 0.4, 0, 1) * np.clip((dur - tt) / 2.2, 0, 1))[:, None]
x /= np.abs(x).max() * 1.25
sf.write(out, x, SR)
