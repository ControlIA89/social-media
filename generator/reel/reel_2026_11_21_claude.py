"""Tre reel sull'uso di Claude per chi fa finanza (21, 22, 23 nov 2026), richiesti da Emanuele il 20 nov.
Progetti, file Excel creati in chat, Claude in Excel. Dati e nomi file illustrativi.
Uso: python3 reel_2026_11_21_claude.py preview|full [nome]
"""
import sys, os, subprocess
from PIL import Image
import render2 as r
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, card, pill, pr
from reels import Hd, header, T, pillL, tick, typed, stamp, cta, frame, W, H, FPS, MX, B, I, S

MEDIA = os.path.join(os.path.dirname(os.path.dirname(S)), "media")
TMP = "/home/claude/reel"
TP = "Claude in pratica"


def file_row(d, x, y, name, col=NAVY, w=820):
    d.rounded_rectangle([x, y, x + w, y + 92], 20, fill=SOFT)
    d.rounded_rectangle([x + 22, y + 16, x + 82, y + 76], 10, fill=col)
    T(d, (x + 52, y + 46), "xls" if name.endswith("xlsx") else "doc", "MONOB", 20, WHITE, "mm")
    T(d, (x + 110, y + 46), name, "M600", 36, NAVY, maxw=w - 140)


# =====================================================================
# 1. PROGETTI (sabato 21)
# =====================================================================
def p1(fr, t):
    header(fr, TP, 1, 4)
    Hd(fr, t, [[("Spieghi il budget", B)], [("a Claude ", B), ("una volta.", I)]], size=92)

    def c(d):
        card(d, MX, 720, 900, 520, "ogni nuova chat", "oggi")
        for k in range(3):
            q = pr(t, 0.7 + k * 0.3, 0.3)
            if q <= 0:
                continue
            yy = 830 + k * 125
            d.rounded_rectangle([MX + 40, yy, MX + 820, yy + 95], 40, fill=SOFT)
            T(d, (MX + 80, yy + 48), "Ti rispiego i nostri driver...", "M600", 36, GREY, maxw=700)
    fr.layer(c, pr(t, 0.45), rise=70)
    stamp(fr, 690, 1150, "BASTA", pr(t, 1.9, 0.25))


def p2(fr, t):
    header(fr, TP, 2, 4)
    Hd(fr, t, [[("Crea un ", B), ("progetto.", I)], [("Carica i documenti.", B)]])
    files = [("consuntivo_2026.xlsx", NAVY), ("driver_2027.docx", ORANGE), ("piano_dei_conti.xlsx", NAVY)]

    def c(d):
        card(d, MX, 700, 900, 560, "progetto · budget 2027", "esempio")
        for k, (nm, col) in enumerate(files):
            q = pr(t, 0.8 + k * 0.4, 0.35)
            if q <= 0:
                continue
            file_row(d, MX + 40 + int((1 - q) * 120), 820 + k * 120, nm, col)
        if t > 2.2:
            T(d, (MX + 450, 1205), "restano lì per ogni chat del progetto", "MONO", 28, GREY, "mm")
    fr.layer(c, pr(t, 0.45), rise=70)


def p3(fr, t):
    header(fr, TP, 3, 4)
    Hd(fr, t, [[("Scrivi le ", B), ("istruzioni.", I)]], size=96)
    rules = ["Usa i nostri driver.", "Separa costi fissi e variabili.", "Scrivi ogni ipotesi."]

    def c(d):
        card(d, MX, 560, 900, 470, "istruzioni del progetto", "una volta")
        for k, s in enumerate(rules):
            st = 0.6 + k * 0.5
            if t < st:
                continue
            yy = 690 + k * 105
            tick(d, MX + 50, yy, True, 52, ORANGE if k == 0 else NAVY)
            T(d, (MX + 130, yy), typed(s, t, st, 34), "M600", 38, NAVY, maxw=720)
    fr.layer(c, pr(t, 0.4), rise=70)

    def n(d):
        card(d, MX, 1080, 900, 300, "da sapere", "limiti", NAVY)
        T(d, (MX + 50, 1200), "Anche sul piano gratuito: max 5 progetti.", "M600", 34, NAVY, maxw=800)
        T(d, (MX + 50, 1275), "Prima di caricare, togli i nomi.", "M800", 36, NAVY, maxw=800)
    fr.layer(n, pr(t, 2.2), rise=70)


REEL_P = [(p1, 3.0), (p2, 3.6), (p3, 3.8),
          (cta(TP, 4, 4, "METODO", ["Ti mando la guida per scrivere", "la tua procedura."]), 3.6)]

# =====================================================================
# 2. FILE EXCEL CREATO IN CHAT (domenica 22)
# =====================================================================
MESI = "GFMAMGLASOND"


def x1(fr, t):
    header(fr, TP, 1, 4)
    Hd(fr, t, [[("Il foglio del budget,", B)], [("pronto in ", B), ("chat.", I)]])

    def c(d):
        card(d, MX, 720, 900, 560, "chat", "esempio")
        d.rounded_rectangle([MX + 40, 820, MX + 860, 960], 36, fill=SOFT)
        s1, s2 = "Prepara il budget 2027 mese per mese,", "partendo dal consuntivo."
        T(d, (MX + 76, 860), typed(s1, t, 0.5, 30), "M600", 34, NAVY, maxw=760)
        T(d, (MX + 76, 916), typed(s2, t, 0.5 + len(s1) / 30, 30), "M600", 34, NAVY, maxw=760)
        if t > 2.3:
            file_row(d, MX + 40, 1020, "budget_2027.xlsx", ORANGE)
            pill(d, MX + 840, 1066, "scarica", NAVY, 22)
    fr.layer(c, pr(t, 0.45), rise=70)


def x2(fr, t):
    header(fr, TP, 2, 4)
    Hd(fr, t, [[("Righe, mesi,", B)], [("formule.", I)]], size=96)

    def c(d):
        card(d, MX, 640, 900, 680, "budget_2027.xlsx", "illustrativo")
        x0, y0, cw = MX + 230, 740, 52
        for j, m in enumerate(MESI):
            T(d, (x0 + j * cw + 23, y0 + 20), m, "MONOB", 24, GREY, "mm")
        rows = ["vendite", "costi var.", "costi fissi", "margine", "cassa"]
        for i, lab in enumerate(rows):
            yy = y0 + 70 + i * 92
            q = pr(t, 0.7 + i * 0.3, 0.6)
            if q <= 0:
                continue
            T(d, (MX + 40, yy + 22), lab, "M800", 30, ORANGE if lab == "margine" else NAVY, maxw=180)
            for j in range(12):
                if j / 12 > q:
                    break
                d.rounded_rectangle([x0 + j * cw, yy, x0 + j * cw + 46, yy + 44], 8,
                                    fill=ORANGE if lab == "margine" else SOFT)
        if t > 2.4:
            T(d, (MX + 450, 1272), "=vendite - costi var. - costi fissi", "MONO", 28, GREY, "mm")
    fr.layer(c, pr(t, 0.4), rise=70)


def x3(fr, t):
    header(fr, TP, 3, 4)
    Hd(fr, t, [[("Le formule", B)], [("le controlli ", B), ("tu.", I)]], size=96)
    labs = ["Su tutti i piani, anche gratuito", "Si attiva nelle impostazioni", "File fino a 30 MB"]

    def c(d):
        card(d, MX, 700, 900, 500, "da sapere", "limiti")
        for k, s in enumerate(labs):
            yy = 840 + k * 125
            tick(d, MX + 50, yy, t > 0.7 + k * 0.45, 58, NAVY)
            T(d, (MX + 140, yy), s, "M600", 38, NAVY, maxw=700)
    fr.layer(c, pr(t, 0.4), rise=70)
    fr.layer(lambda d: T(d, (W // 2, 1290), "Il file è una bozza. La firma è tua.", "M800", 42, NAVY, "mm"),
             pr(t, 2.3), rise=30)


REEL_X = [(x1, 3.4), (x2, 3.6), (x3, 3.6),
          (cta(TP, 4, 4, "BUDGET", ["Ti mando la traccia dei", "cinque passi del budget."]), 3.6)]

# =====================================================================
# 3. CLAUDE IN EXCEL (lunedì 23)
# =====================================================================
def grid(d, x, y, cols, rows, cw=70, rh=56, hi=None):
    for i in range(rows):
        for j in range(cols):
            fill = ORANGE if hi == (i, j) else (SOFT if i == 0 or j == 0 else WHITE)
            d.rectangle([x + j * cw, y + i * rh, x + (j + 1) * cw - 3, y + (i + 1) * rh - 3], fill=fill,
                        outline=(214, 220, 230))


def e1(fr, t):
    header(fr, TP, 1, 4)
    Hd(fr, t, [[("Chiedi al tuo Excel", B)], [("perché il margine", B)], [("scende.", I)]])

    def c(d):
        card(d, MX, 820, 900, 520, "Excel + Claude", "esempio")
        grid(d, MX + 30, 920, 6, 7, 70, 56)

        def side(d=d):
            d.rounded_rectangle([MX + 470, 910, MX + 870, 1310], 20, fill=SOFT, outline=NAVY, width=3)
            T(d, (MX + 500, 950), "Claude", "MONOB", 26, ORANGE)
            d.rounded_rectangle([MX + 495, 990, MX + 850, 1130], 18, fill=WHITE)
            s = "Perché il margine di marzo scende?"
            T(d, (MX + 515, 1030), typed(s[:18], t, 0.9, 26), "M600", 28, NAVY, maxw=320)
            T(d, (MX + 515, 1080), typed(s[18:], t, 0.9 + 18 / 26, 26), "M600", 28, NAVY, maxw=320)
        side()
    fr.layer(c, pr(t, 0.45), rise=70)


def e2(fr, t):
    header(fr, TP, 2, 4)
    Hd(fr, t, [[("Legge il foglio.", B)], [("Ti indica le ", B), ("celle.", I)]])

    def c(d):
        card(d, MX, 700, 900, 620, "Excel + Claude", "esempio")
        hi = (4, 4) if t > 1.0 else None
        grid(d, MX + 30, 800, 6, 8, 70, 56, hi)
        if hi:
            d.rectangle([MX + 30 + 4 * 70 - 4, 800 + 4 * 56 - 4, MX + 30 + 5 * 70 + 1, 800 + 5 * 56 + 1],
                        outline=NAVY, width=5)
        d.rounded_rectangle([MX + 470, 790, MX + 870, 1290], 20, fill=SOFT, outline=NAVY, width=3)
        T(d, (MX + 500, 830), "Claude", "MONOB", 26, ORANGE)
        lines = ["Nella cella D4 i costi", "variabili crescono più", "delle vendite.", "",
                 "Vuoi che aggiunga", "un commento?"]
        for k, s in enumerate(lines):
            st = 1.2 + k * 0.3
            if s and t > st:
                T(d, (MX + 500, 890 + k * 50), typed(s, t, st, 40), "M600", 28, NAVY, maxw=345)
    fr.layer(c, pr(t, 0.4), rise=70)


def e3(fr, t):
    header(fr, TP, 3, 4)
    Hd(fr, t, [[("Prima di ", B), ("provarlo.", I)]], size=96)
    labs = ["È un componente aggiuntivo di Excel", "Serve un piano a pagamento", "Rileggi ogni modifica"]

    def c(d):
        card(d, MX, 580, 900, 500, "da sapere", "limiti")
        for k, s in enumerate(labs):
            yy = 720 + k * 125
            tick(d, MX + 50, yy, t > 0.7 + k * 0.45, 58, ORANGE if k == 2 else NAVY)
            T(d, (MX + 140, yy), s, "M600", 38, NAVY, maxw=700)
    fr.layer(c, pr(t, 0.4), rise=70)
    fr.layer(lambda d: T(d, (W // 2, 1200), "L'AI prepara. Tu firmi.", "M800", 50, NAVY, "mm"), pr(t, 2.3), rise=30)


REEL_E = [(e1, 3.4), (e2, 3.8), (e3, 3.4),
          (cta(TP, 4, 4, "FINANCE", ["Ti mando la guida gratuita", "da cui partire."]), 3.6)]

REELS = {"progetti": (REEL_P, "2026-11-21"), "excel_in_chat": (REEL_X, "2026-11-22"),
         "claude_in_excel": (REEL_E, "2026-11-23")}

if __name__ == "__main__":
    mode = sys.argv[1]
    os.makedirs(TMP, exist_ok=True)
    for name, (sc, day) in REELS.items():
        if len(sys.argv) > 2 and sys.argv[2] not in name:
            continue
        out_dir = os.path.join(MEDIA, day)
        os.makedirs(out_dir, exist_ok=True)
        if mode == "preview":
            ims = [frame(sc, i, d - 0.3).resize((540, 960)) for i, (_, d) in enumerate(sc)]
            sh = Image.new("RGB", (540 * len(ims), 960))
            for i, im in enumerate(ims):
                sh.paste(im, (540 * i, 0))
            sh.save(os.path.join(TMP, f"sheet_{name}.png"))
            continue
        files = []
        for i, (_, dur) in enumerate(sc):
            tmp, out = os.path.join(TMP, f"t_{name}_{i}.mp4"), os.path.join(TMP, f"s_{name}_{i}.mp4")
            p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                  "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18",
                                  "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
            for k in range(round(dur * FPS)):
                p.stdin.write(frame(sc, i, k / FPS).tobytes())
            p.stdin.close()
            assert p.wait() == 0
            os.replace(tmp, out)
            files.append(out)
        lst = os.path.join(TMP, f"l_{name}.txt")
        with open(lst, "w") as f:
            for x in files:
                f.write(f"file '{x}'\n")
        muto = os.path.join(TMP, f"muto_{name}.mp4")
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                               "-c", "copy", muto])
        dur = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                       "csv=p=0", muto]).decode().strip()
        wav = os.path.join(TMP, f"musica_{name}.wav")
        subprocess.check_call([sys.executable, os.path.join(S, "musica_classica.py"), "bach", dur, wav])
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", muto, "-i", wav, "-filter_complex",
                               "[1:a]lowpass=f=7000,highpass=f=40,loudnorm=I=-19:TP=-2[a]", "-map", "0:v",
                               "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
                               os.path.join(out_dir, f"reel_{name}_bach.mp4")])
        frame(sc, 0, sc[0][1] - 0.3).save(os.path.join(out_dir, f"cover_{name}.png"))
        for x in files + [lst, muto, wav]:
            os.remove(x)
        print("done", name, dur)
