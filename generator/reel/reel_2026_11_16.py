"""Reel del 16 novembre 2026: Budget 2027 in 5 passi (1080x1920, senza audio).
Uso: python3 reel_2026_11_16.py preview <cartella>   -> un fotogramma per scena
     python3 reel_2026_11_16.py full                 -> mp4 e copertina in media/2026-11-16/"""
import os, sys, subprocess
from PIL import Image
import render2 as r
import reels
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, card, pill, pr
from reels import Hd, header, T, pillL, tick, stamp, back, frame, B, I, W, H, FPS, MX

OUT = os.path.join(os.path.dirname(os.path.dirname(r.S)), "media", "2026-11-16")
TP, TOT = "budget 2027", 7


def s1(fr, t):
    header(fr, TP, 1, TOT)
    Hd(fr, t, [[("Budget 2027:", B)], [("non partire", B)], [("da ", B), ("Excel.", I)]])

    def c(d):
        card(d, MX, 780, 900, 520, "budget_2027.xlsx", "vuoto", GREY)
        for i in range(20):
            cx, cy = MX + 45 + (i % 5) * 162, 890 + (i // 5) * 92
            d.rectangle([cx, cy, cx + 152, cy + 80], fill=WHITE, outline=SOFT, width=3)
            if i < int(max(0, t - 0.9) * 9):
                T(d, (cx + 76, cy + 40), "?", "M800", 44, GREY, "mm")
    fr.layer(c, pr(t, 0.6), rise=70)
    stamp(fr, 540, 1300, "PRIMA I DRIVER", pr(t, 2.3, 0.25), -6)


def step(n, lines, title, tag, body):
    def sc(fr, t):
        header(fr, TP, n + 1, TOT)
        q = pr(t, 0.0, 0.3)
        fr.layer(lambda d: d.text((MX, 470), f"0{n}", font=F("PFI", int(250 * back(q))), fill=ORANGE, anchor="ls"), q, rise=0)
        Hd(fr, t, lines, 600, 80, 0.15)

        def c(d):
            card(d, MX, 780, 900, 620, title, tag)
            body(d, t)
        fr.layer(c, pr(t, 0.45), rise=70)
    return sc


def k1(d, t):
    labs = ["volumi", "prezzi", "mix di prodotto", "persone", "tempi di incasso"]
    for i, s in enumerate(labs):
        yy = 925 + i * 92
        tick(d, MX + 50, yy, t > 0.9 + i * 0.3, 56)
        T(d, (MX + 136, yy), s, "M600", 42, NAVY)


def k2(d, t):
    d.line([MX + 50, 1330, MX + 850, 1330], fill=SOFT, width=5)
    for i, (lab, hh) in enumerate((("linea A", 300), ("linea B", 210), ("linea C", 150), ("nuova", 90))):
        q = pr(t, 0.8 + i * 0.22, 0.6)
        bx = MX + 80 + i * 195
        d.rounded_rectangle([bx, 1330 - max(16, hh * q), bx + 130, 1330], 14, fill=ORANGE if i == 3 else NAVY)
        T(d, (bx + 65, 1365), lab, "MONOB", 26, NAVY, "mm")
    T(d, (MX + 50, 900), "prezzo × volumi, linea per linea", "MONO", 30, GREY)


def k3(d, t):
    for k, (ttl, c, rows) in enumerate((("fissi", NAVY, ["affitti", "personale", "canoni"]),
                                        ("variabili", ORANGE, ["materiali", "trasporti", "provvigioni"]))):
        x = MX + 40 + k * 420
        q = pr(t, 0.8 + k * 0.5, 0.3)
        if q <= 0:
            continue
        d.rounded_rectangle([x, 880, x + 390, 960], 20, fill=c)
        T(d, (x + 195, 920), ttl, "M800", 40, WHITE, "mm")
        for i, s in enumerate(rows):
            if pr(t, 1.0 + k * 0.5 + i * 0.2, 0.1) > 0:
                yy = 1050 + i * 115
                d.ellipse([x + 16, yy - 12, x + 40, yy + 12], fill=c)
                T(d, (x + 64, yy), s, "M600", 40, NAVY, maxw=320)


def k4(d, t):
    x0, x1, y0 = MX + 50, MX + 850, 1110
    d.line([x0, y0, x1, y0], fill=SOFT, width=5)
    T(d, (x1, y0 - 28), "zero", "MONO", 26, GREY, "rm")
    pts = [(0, -120), (130, -60), (260, 40), (400, 110), (540, 30), (670, -90), (800, -170)]
    q = pr(t, 0.8, 1.3)
    n = max(2, int(1 + q * (len(pts) - 1)))
    d.line([(x0 + a, y0 + b) for a, b in pts[:n]], fill=NAVY, width=10, joint="curve")
    if n >= 4:
        a, b = pts[3]
        d.ellipse([x0 + a - 20, y0 + b - 20, x0 + a + 20, y0 + b + 20], fill=ORANGE)
        T(d, (x0 + a, y0 + b + 62), "qui serve liquidità", "M800", 32, NAVY, "mm")
    for i, m in enumerate(("gen", "mar", "mag", "lug", "set", "nov")):
        T(d, (x0 + 40 + i * 144, 1362), m, "MONOB", 26, GREY, "mm")


def k5(d, t):
    d.line([MX + 50, 1340, MX + 850, 1340], fill=SOFT, width=5)
    series = [("spinto", GREY, [(0, 330), (170, 270), (340, 200), (510, 120), (640, 50)]),
              ("base", ORANGE, [(0, 330), (170, 300), (340, 260), (510, 215), (640, 180)]),
              ("prudente", NAVY, [(0, 330), (170, 330), (340, 325), (510, 315), (640, 310)])]
    for i, (lab, c, pts) in enumerate(series):
        q = pr(t, 0.8 + i * 0.35, 0.8)
        if q <= 0:
            continue
        n = max(2, int(1 + q * (len(pts) - 1)))
        d.line([(MX + 50 + a, 900 + b) for a, b in pts[:n]], fill=c, width=10, joint="curve")
        if q >= 1:
            pill(d, MX + 870, 900 + pts[-1][1], lab, c, 22)


def s7(fr, t):
    header(fr, TP, 7, TOT)
    Hd(fr, t, [[("L'AI prepara", B)], [("i numeri.", B)], [("Tu ", B), ("firmi.", I)]])
    rows = [("raccolta dati", "AI"), ("ipotesi", "AI"), ("controlli", "AI"), ("decisione", "tu")]

    def c(d):
        card(d, MX, 780, 900, 560, "chi fa cosa", "budget 2027", NAVY)
        for i, (s, who) in enumerate(rows):
            if pr(t, 0.9 + i * 0.35, 0.1) <= 0:
                continue
            yy = 910 + i * 105
            tick(d, MX + 50, yy, True, 56, ORANGE if who == "tu" else NAVY)
            T(d, (MX + 136, yy), s, "M800" if who == "tu" else "M600", 44, NAVY)
            pill(d, MX + 860, yy, who, ORANGE if who == "tu" else GREY, 28)
    fr.layer(c, pr(t, 0.6), rise=70)
    stamp(fr, 560, 1395, "FIRMA TUA", pr(t, 2.6, 0.25), 6)


REEL = [(s1, 3.4),
        (step(1, [[("Scegli", B)], [("i ", B), ("driver", I)]], "driver", "pochi", k1), 3.0),
        (step(2, [[("Budget delle", B)], [("vendite", I)]], "ricavi", "illustrativo", k2), 2.8),
        (step(3, [[("Budget dei", B)], [("costi", I)]], "costi", "separati", k3), 2.8),
        (step(4, [[("Budget di", B)], [("cassa", I)]], "cassa mese per mese", "illustrativo", k4), 3.0),
        (step(5, [[("Tre", B)], [("scenari", I)]], "scenari", "illustrativo", k5), 2.8),
        (s7, 4.0)]
NAME = "budget_2027_5_passi"

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        os.makedirs(sys.argv[2], exist_ok=True)
        for i, (_, dur) in enumerate(REEL):
            frame(REEL, i, dur - 0.3).save(os.path.join(sys.argv[2], f"scena_{i+1}.png"))
            frame(REEL, i, dur * 0.45).resize((540, 960)).save(os.path.join(sys.argv[2], f"meta_{i+1}.png"))
    else:
        os.makedirs(OUT, exist_ok=True)
        tmpd = sys.argv[2]
        os.makedirs(tmpd, exist_ok=True)
        files = []
        for i, (_, dur) in enumerate(REEL):
            out = os.path.join(tmpd, f"s_{i}.mp4")
            p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                  "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18",
                                  "-preset", "veryfast", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
            for k in range(round(dur * FPS)):
                p.stdin.write(frame(REEL, i, k / FPS).tobytes())
            p.stdin.close()
            assert p.wait() == 0
            files.append(out)
        lst = os.path.join(tmpd, "lista.txt")
        with open(lst, "w") as f:
            for x in files:
                f.write(f"file '{x}'\n")
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                               "-c", "copy", "-movflags", "+faststart", os.path.join(OUT, f"reel_{NAME}.mp4")])
        frame(REEL, 0, REEL[0][1] - 0.3).save(os.path.join(OUT, f"cover_{NAME}.png"))
        print("fatto", sum(d for _, d in REEL))
