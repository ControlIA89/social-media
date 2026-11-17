"""Tre reel brevi sulle novità di Claude (11 nov 2026) lette per chi fa finanza:
Claude Data, Claude Meetings, Claude Whiteboards. Grafici e testi illustrativi, nessun dato reale.
Uso: python3 reel_2026_11_17_claude.py preview|full [nome]
"""
import sys, os, subprocess
from PIL import Image
import render2 as r
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, card, pill, pr
from reels import Hd, header, T, pillL, tick, typed, stamp, cta, frame, W, H, FPS, MX, B, I, S

OUT = "/home/claude/reel"


def arrow(d, x1, y, x2, color=NAVY):
    d.line([x1, y, x2, y], fill=color, width=6)
    d.polygon([(x2, y), (x2 - 16, y - 11), (x2 - 16, y + 11)], fill=color)


def arrow_down(d, x, y1, y2, color=NAVY):
    d.line([x, y1, x, y2], fill=color, width=6)
    d.polygon([(x, y2), (x - 11, y2 - 16), (x + 11, y2 - 16)], fill=color)


# =====================================================================
# DATA
# =====================================================================
TD = "Claude Data"


def d1(fr, t):
    header(fr, TD, 1, 4)
    Hd(fr, t, [[("Ogni numero", B)], [("con la sua ", B), ("fonte.", I)]], size=96)

    def c(d):
        card(d, MX, 720, 900, 560, "cruscotto", "esempio")
        for i, (lab, hh) in enumerate((("ricavi", 190), ("margine", 120), ("cassa", 150))):
            x = MX + 50 + i * 280
            q = pr(t, 0.7 + i * 0.2, 0.5)
            d.rounded_rectangle([x, 830, x + 240, 1100], 18, fill=SOFT)
            d.rounded_rectangle([x + 30, 1070 - hh * q, x + 210, 1070], 12, fill=ORANGE if i == 1 else NAVY)
            T(d, (x + 120, 1150), lab, "MONOB", 30, NAVY, "mm")
        if t > 1.6:
            d.rounded_rectangle([MX + 322, 822, MX + 578, 1108], 22, outline=ORANGE, width=8)
            T(d, (MX + 450, 1225), "da dove viene questo numero?", "M600", 34, GREY, "mm")
    fr.layer(c, pr(t, 0.45), rise=70)


def d2(fr, t):
    header(fr, TD, 2, 4)
    Hd(fr, t, [[("Chiedi in italiano.", B)], [("Risponde con", B)], [("un ", B), ("grafico.", I)]])

    def c(d):
        card(d, MX, 800, 900, 560, "Claude Data", "novità")
        d.rounded_rectangle([MX + 40, 900, MX + 860, 990], 40, fill=SOFT)
        T(d, (MX + 80, 945), typed("Margine per cliente, ultimi 12 mesi", t, 0.7, 26), "M600", 36, NAVY, maxw=760)
        for k, wd in enumerate((620, 480, 390, 250)):
            q = pr(t, 2.0 + k * 0.15, 0.5)
            yy = 1050 + k * 72
            T(d, (MX + 50, yy + 22), f"cliente {'ABCD'[k]}", "MONO", 28, GREY)
            d.rounded_rectangle([MX + 220, yy, MX + 220 + max(20, wd * q), yy + 44], 12, fill=ORANGE if k == 0 else NAVY)
    fr.layer(c, pr(t, 0.5), rise=70)


def d3(fr, t):
    header(fr, TD, 3, 4)
    Hd(fr, t, [[("Clicchi il numero,", B)], [("vedi la ", B), ("query.", I)]])

    def c(d):
        card(d, MX, 700, 900, 400, "dietro il numero", "verificabile")
        for i, s in enumerate(("SELECT cliente,", "  SUM(ricavi - costi)", "FROM vendite", "GROUP BY cliente")):
            if t > 0.7 + i * 0.35:
                T(d, (MX + 50, 830 + i * 62), typed(s, t, 0.7 + i * 0.35, 40), "MONO", 36, NAVY)
    fr.layer(c, pr(t, 0.5), rise=70)

    def n(d):
        card(d, MX, 1150, 900, 250, "per una PMI", "nota", NAVY)
        tick(d, MX + 50, 1275, True, 52, NAVY)
        T(d, (MX + 130, 1275), "Serve un database collegato.", "M800", 38, NAVY, maxw=720)
        T(d, (MX + 130, 1335), "Il lavoro vero è preparare i dati.", "M600", 32, GREY, maxw=720)
    fr.layer(n, pr(t, 2.2), rise=70)


REEL_D = [(d1, 3.0), (d2, 3.6), (d3, 3.8),
          (cta(TD, 4, 4, "FINANCE", ["Ti mando la guida gratuita", "da cui partire."]), 3.6)]

# =====================================================================
# MEETINGS
# =====================================================================
TM = "Claude Meetings"


def m1(fr, t):
    header(fr, TM, 1, 4)
    Hd(fr, t, [[("Esci dalla riunione", B)], [("con le azioni", B)], [("già ", B), ("scritte.", I)]])

    def c(d):
        card(d, MX, 800, 900, 540, "riunione di budget", "in corso")
        names = ["direzione", "vendite", "amministrazione", "Claude"]
        for i, nm in enumerate(names):
            x, y = MX + 40 + (i % 2) * 420, 900 + (i // 2) * 215
            q = pr(t, 0.6 + i * 0.2, 0.3)
            if q <= 0:
                continue
            last = i == 3
            d.rounded_rectangle([x, y, x + 400, y + 195], 20, fill=ORANGE if last else SOFT,
                                outline=NAVY if last else None, width=4)
            d.ellipse([x + 160, y + 30, x + 240, y + 110], fill=WHITE if last else NAVY)
            T(d, (x + 200, y + 155), nm, "MONOB", 28, WHITE if last else NAVY, "mm")
    fr.layer(c, pr(t, 0.45), rise=70)


def m2(fr, t):
    header(fr, TM, 2, 4)
    Hd(fr, t, [[("Claude entra in call", B)], [("e prende ", B), ("nota.", I)]])
    rows = [("decisione", "Rivedere il listino", ORANGE), ("azione", "Aggiornare i costi fissi", NAVY),
            ("chi", "Amministrazione", NAVY), ("quando", "Prima del prossimo incontro", NAVY)]

    def c(d):
        card(d, MX, 700, 900, 640, "note della riunione", "esempio")
        for i, (lab, s, col) in enumerate(rows):
            st = 0.7 + i * 0.55
            if t < st:
                continue
            yy = 850 + i * 125
            pillL(d, MX + 40, yy, lab, col, 24)
            T(d, (MX + 250, yy), typed(s, t, st + 0.1, 36), "M600", 38, NAVY, maxw=600)
    fr.layer(c, pr(t, 0.45), rise=70)


def m3(fr, t):
    header(fr, TM, 3, 4)
    Hd(fr, t, [[("Prima, chiedi", B)], [("il ", B), ("consenso.", I)]])
    labs = ["Tutti d'accordo sulla trascrizione", "Per ora solo su Google Meet", "In beta, piani Team ed Enterprise"]

    def c(d):
        card(d, MX, 700, 900, 520, "da sapere", "beta")
        for i, s in enumerate(labs):
            yy = 850 + i * 130
            tick(d, MX + 50, yy, t > 0.8 + i * 0.5, 60, ORANGE if i == 0 else NAVY)
            T(d, (MX + 140, yy), s, "M600", 38, NAVY, maxw=700)
    fr.layer(c, pr(t, 0.45), rise=70)
    fr.layer(lambda d: T(d, (W // 2, 1310), "Le decisioni restano a chi firma.", "M800", 42, NAVY, "mm"),
             pr(t, 2.4), rise=30)


REEL_M = [(m1, 3.2), (m2, 3.8), (m3, 3.6),
          (cta(TM, 4, 4, "FINANCE", ["Ti mando la guida gratuita", "da cui partire."]), 3.6)]

# =====================================================================
# WHITEBOARDS
# =====================================================================
TW = "Claude Whiteboards"


def w1(fr, t):
    header(fr, TW, 1, 4)
    Hd(fr, t, [[("Il tuo budget", B)], [("su una ", B), ("lavagna.", I)]], size=96)
    notes = [("driver", ORANGE, 0, 0, -4), ("vendite", NAVY, 1, 0, 3), ("costi fissi", NAVY, 2, 0, -2),
             ("personale", NAVY, 0, 1, 3), ("incassi", ORANGE, 1, 1, -3), ("scenari", NAVY, 2, 1, 4)]

    def c(d):
        card(d, MX, 720, 900, 600, "lavagna", "condivisa")
    fr.layer(c, pr(t, 0.45), rise=70)
    for i, (s, col, cx, cy, ang) in enumerate(notes):
        q = pr(t, 0.8 + i * 0.22, 0.3)
        if q <= 0:
            continue
        im = Image.new("RGBA", (250, 190), (0, 0, 0, 0))
        from PIL import ImageDraw
        dd = ImageDraw.Draw(im)
        dd.rounded_rectangle([6, 8, 250, 190], 14, fill=(0, 43, 92, 46))
        dd.rounded_rectangle([0, 0, 242, 180], 14, fill=col)
        f = F("M800", 34)
        dd.text((121, 90), s, font=f, fill=WHITE, anchor="mm")
        im = im.rotate(ang, expand=True, resample=Image.BICUBIC)
        if q < 1:
            im.putalpha(im.getchannel("A").point(lambda v: int(v * q)))
        ly = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ly.paste(im, (MX + 45 + cx * 280, 850 + cy * 220 + int((1 - q) * 40)))
        fr.img.alpha_composite(ly)


def w2(fr, t):
    header(fr, TW, 2, 4)
    Hd(fr, t, [[("Dalla chat", B)], [("alla ", B), ("mappa.", I)]], size=96)
    steps = ["Vendite", "Costi", "Cassa", "Scenari"]

    def c(d):
        card(d, MX, 720, 900, 620, "ciclo del budget", "esempio")
        d.rounded_rectangle([MX + 40, 820, MX + 860, 900], 36, fill=SOFT)
        T(d, (MX + 76, 860), typed("Disegna il ciclo del nostro budget", t, 0.6, 28), "M600", 34, NAVY, maxw=760)
        for i, s in enumerate(steps):
            q = pr(t, 1.9 + i * 0.3, 0.3)
            if q <= 0:
                continue
            col = (i % 2) if i < 2 else (1 - i % 2)
            x, y = MX + 60 + col * 420, 960 + (i // 2) * 190
            d.rounded_rectangle([x, y, x + 360, y + 130], 20, fill=ORANGE if i == 3 else WHITE, outline=NAVY, width=5)
            T(d, (x + 30, y + 65), f"0{i+1}", "MONOB", 30, WHITE if i == 3 else ORANGE)
            T(d, (x + 100, y + 65), s, "M800", 42, WHITE if i == 3 else NAVY)
        if t > 2.3:
            arrow(d, MX + 428, 1025, MX + 474)
        if t > 2.6:
            arrow_down(d, MX + 660, 1096, 1144)
        if t > 2.9:
            d.line([MX + 432, 1215, MX + 474, 1215], fill=NAVY, width=6)
            d.polygon([(MX + 426, 1215), (MX + 442, 1204), (MX + 442, 1226)], fill=NAVY)
    fr.layer(c, pr(t, 0.45), rise=70)


def w3(fr, t):
    header(fr, TW, 3, 4)
    Hd(fr, t, [[("Poi diventa", B)], [("un ", B), ("documento.", I)]], size=96)

    def a(d):
        card(d, MX, 720, 400, 420, "lavagna", "beta", NAVY)
        for k, col in enumerate((ORANGE, NAVY, NAVY, ORANGE)):
            x, y = MX + 50 + (k % 2) * 160, 830 + (k // 2) * 140
            d.rounded_rectangle([x, y, x + 140, y + 115], 12, fill=col)
    fr.layer(a, pr(t, 0.45), rise=70)

    def b(d):
        card(d, MX + 500, 720, 400, 420, "documento")
        for k, wd in enumerate((300, 240, 280, 200, 260)):
            q = pr(t, 1.3 + k * 0.15, 0.4)
            d.rounded_rectangle([MX + 550, 840 + k * 52, MX + 550 + max(16, wd * q), 864 + k * 52], 10,
                                fill=ORANGE if k == 0 else SOFT)
    fr.layer(b, pr(t, 1.0), rise=70)
    if t > 0.9:
        fr.layer(lambda d: arrow(d, MX + 418, 930, MX + 482, ORANGE), pr(t, 0.9, 0.3), rise=0)
    fr.layer(lambda d: T(d, (W // 2, 1250), "Prima il processo. Poi i numeri.", "M800", 44, NAVY, "mm"),
             pr(t, 2.0), rise=30)
    fr.layer(lambda d: T(d, (W // 2, 1320), "novità di Claude, in beta", "MONO", 30, GREY, "mm"), pr(t, 2.2), rise=30)


REEL_W = [(w1, 3.2), (w2, 4.0), (w3, 3.4),
          (cta(TW, 4, 4, "FINANCE", ["Ti mando la guida gratuita", "da cui partire."]), 3.6)]

REELS = {"claude_data": REEL_D, "claude_meetings": REEL_M, "claude_whiteboards": REEL_W}

if __name__ == "__main__":
    mode = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    for name, sc in REELS.items():
        if len(sys.argv) > 2 and sys.argv[2] not in name:
            continue
        if mode == "preview":
            ims = [frame(sc, i, d - 0.3).resize((540, 960)) for i, (_, d) in enumerate(sc)]
            sh = Image.new("RGB", (540 * len(ims), 960))
            for i, im in enumerate(ims):
                sh.paste(im, (540 * i, 0))
            sh.save(os.path.join(OUT, f"sheet_{name}.png"))
        else:
            files = []
            for i, (_, dur) in enumerate(sc):
                tmp, out = os.path.join(OUT, f"t_{name}_{i}.mp4"), os.path.join(OUT, f"s_{name}_{i}.mp4")
                p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                      "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18",
                                      "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
                for k in range(round(dur * FPS)):
                    p.stdin.write(frame(sc, i, k / FPS).tobytes())
                p.stdin.close()
                assert p.wait() == 0
                os.replace(tmp, out)
                files.append(out)
            lst = os.path.join(OUT, f"l_{name}.txt")
            with open(lst, "w") as f:
                for x in files:
                    f.write(f"file '{x}'\n")
            muto = os.path.join(OUT, f"muto_{name}.mp4")
            subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                                   "-c", "copy", muto])
            dur = sum(d for _, d in sc)
            wav = os.path.join(OUT, f"musica_{name}.wav")
            subprocess.check_call([sys.executable, os.path.join(S, "musica_focus.py"), str(dur), wav])
            subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", muto, "-i", wav, "-filter_complex",
                                   "[1:a]lowpass=f=3800,highpass=f=40,loudnorm=I=-20:TP=-2[a]", "-map", "0:v",
                                   "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
                                   os.path.join(OUT, f"reel_{name}.mp4")])
            frame(sc, 0, sc[0][1] - 0.3).save(os.path.join(OUT, f"cover_{name}.png"))
            for x in files + [lst, muto, wav]:
                os.remove(x)
            print("done", name, dur)
