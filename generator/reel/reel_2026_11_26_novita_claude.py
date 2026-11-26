"""Due reel sulle novità di Claude lette per chi fa finanza (26 e 28 nov 2026, ore 18:30), richiesti da Emanuele il 26 nov.
Fonti ufficiali lette il 26 nov 2026: claude.com/resources/articles/sheets-whiteboards-data (10 nov 2026) e
support.claude.com release notes (voci del 6 e 24 nov 2026). Dati e nomi illustrativi.
Uso: python3 reel_2026_11_26_novita_claude.py preview|full [sheets|novita]
"""
import sys, os, subprocess
from PIL import Image
import render2 as r
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, card, pill, pr
from reels import Hd, header, T, pillL, tick, typed, stamp, cta, frame, W, H, FPS, MX, B, I, S

MEDIA = os.path.join(os.path.dirname(os.path.dirname(S)), "media")
TMP = "/home/claude/reel"
TP = "novità di Claude"


def riga(d, y, lab, txt, col=NAVY, w=250):
    d.rounded_rectangle([MX + 40, y - 40, MX + 40 + w, y + 40], 16, fill=col)
    T(d, (MX + 40 + w / 2, y), lab, "M800", 32, WHITE, "mm")
    T(d, (MX + 70 + w, y), txt, "M600", 34, NAVY, maxw=820 - w - 40)


# =====================================================================
# 1. CLAUDE SHEETS (giovedì 26)
# =====================================================================
def a1(fr, t):
    header(fr, TP, 1, 4)
    Hd(fr, t, [[("Il foglio lo costruisce", B)], [("Claude, ", B), ("con te.", I)]], size=88)

    def c(d):
        card(d, MX, 720, 900, 520, "chat", "Claude Sheets · beta")
        d.rounded_rectangle([MX + 40, 830, MX + 860, 990], 36, fill=SOFT)
        s = typed("Prepara il budget costi 2027, mese per mese", t, 0.7, 26)
        T(d, (MX + 80, 880), s[:24], "M600", 38, NAVY)
        T(d, (MX + 80, 940), s[24:].strip(), "M600", 38, NAVY)
        if t > 2.3:
            d.rounded_rectangle([MX + 40, 1040, MX + 560, 1180], 24, fill=NAVY)
            T(d, (MX + 80, 1110), "budget_costi_2027", "MONOB", 34, WHITE)
            T(d, (MX + 720, 1110), "esempio", "MONO", 28, GREY, "mm")
    fr.layer(c, pr(t, 0.45), rise=70)


def a2(fr, t):
    header(fr, TP, 2, 4)
    Hd(fr, t, [[("Schede, formule,", B)], [("menu ", B), ("a tendina.", I)]], size=92)

    def c(d):
        card(d, MX, 700, 900, 660, "foglio · esempio", "illustrativo")
        x0, y0, cw, ch = MX + 40, 800, 205, 66
        for rr in range(5):
            for cc in range(4):
                q = pr(t, 0.6 + (rr * 4 + cc) * 0.05, 0.1)
                if q <= 0:
                    continue
                x, y = x0 + cc * cw, y0 + rr * ch
                head = rr == 0 or cc == 0
                d.rectangle([x, y, x + cw - 6, y + ch - 6], fill=SOFT if head else WHITE, outline=GREY, width=2)
                if rr == 0 and cc > 0:
                    T(d, (x + cw / 2 - 3, y + ch / 2 - 3), ["gen", "feb", "mar"][cc - 1], "MONOB", 26, NAVY, "mm")
                elif cc == 0 and rr > 0:
                    T(d, (x + 14, y + ch / 2 - 3), ["personale", "affitti", "servizi", "totale"][rr - 1], "MONO", 24, NAVY)
                elif rr == 4:
                    T(d, (x + cw / 2 - 3, y + ch / 2 - 3), "=SOMMA", "MONOB", 24, ORANGE, "mm")
                else:
                    d.rounded_rectangle([x + 50, y + 22, x + cw - 56, y + 38], 8, fill=SOFT)
        if t > 1.8:
            d.rounded_rectangle([x0, 1140, x0 + 170, 1190], 14, fill=NAVY)
            T(d, (x0 + 85, 1165), "costi", "MONOB", 24, WHITE, "mm")
            d.rounded_rectangle([x0 + 185, 1140, x0 + 355, 1190], 14, fill=SOFT)
            T(d, (x0 + 270, 1165), "ricavi", "MONOB", 24, NAVY, "mm")
            d.rounded_rectangle([x0 + 370, 1140, x0 + 540, 1190], 14, fill=SOFT)
            T(d, (x0 + 455, 1165), "cassa", "MONOB", 24, NAVY, "mm")
        if t > 2.3:
            tick(d, MX + 50, 1270, True, 48, ORANGE)
            T(d, (MX + 125, 1270), "le modifiche restano evidenziate", "M600", 36, NAVY, maxw=740)
    fr.layer(c, pr(t, 0.45), rise=70)


def a3(fr, t):
    header(fr, TP, 3, 4)
    Hd(fr, t, [[("Cosa sapere", B)], [("prima ", B), ("di usarlo.", I)]], size=92)

    def c(d):
        card(d, MX, 700, 900, 600, "Claude Sheets", "limiti noti", NAVY)
        rows = [("beta", "sui piani a pagamento", ORANGE), ("funzioni", "semplici, per ora", NAVY),
                ("export", "in .xlsx o CSV", NAVY)]
        for i, (lab, txt, col) in enumerate(rows):
            if pr(t, 0.7 + i * 0.45, 0.1) > 0:
                riga(d, 850 + i * 125, lab, txt, col)
        if t > 2.3:
            T(d, (MX + 450, 1240), "i numeri li controlli tu", "MONO", 28, GREY, "mm")
    fr.layer(c, pr(t, 0.45), rise=70)


SHEETS = [(a1, 3.4), (a2, 3.8), (a3, 3.4),
          (cta(TP, 4, 4, "FINANCE", ["Ti indico le guide gratuite", "da cui partire."]), 3.6)]


# =====================================================================
# 2. TRE NOVITÀ DI NOVEMBRE (sabato 28)
# =====================================================================
NEWS = [("File e app collegate", "invii e salvi file nelle app", "beta"),
        ("Tag di progetto", "la spesa per codice di costo", "beta"),
        ("Claude Sheets", "il foglio costruito in chat", "beta")]


def b1(fr, t):
    header(fr, TP, 1, 4)
    Hd(fr, t, [[("3 novità di Claude", B)], [("per chi fa ", B), ("finanza.", I)]], size=90)

    def c(d):
        card(d, MX, 720, 900, 520, "novembre 2026", "in breve")
        for i, (nm, _, _) in enumerate(NEWS):
            if pr(t, 0.7 + i * 0.4, 0.1) <= 0:
                continue
            yy = 860 + i * 120
            d.text((MX + 50, yy), f"0{i + 1}", font=F("MONOB", 38), fill=ORANGE, anchor="lm")
            T(d, (MX + 140, yy), nm, "M800", 44, NAVY, maxw=720)
    fr.layer(c, pr(t, 0.45), rise=70)


def news_card(d, y, n, nm, txt, lim, h=290):
    card(d, MX, y, 900, h, f"novità {n}", "beta")
    T(d, (MX + 40, y + 125), nm, "M800", 44, NAVY, maxw=820)
    T(d, (MX + 40, y + 185), txt, "M600", 34, NAVY, maxw=820)
    T(d, (MX + 40, y + 240), lim, "MONO", 26, GREY, maxw=820)


def b2(fr, t):
    header(fr, TP, 2, 4)
    Hd(fr, t, [[("Meno copia", B)], [("e ", B), ("incolla.", I)]], size=96)
    fr.layer(lambda d: news_card(d, 690, 1, NEWS[0][0], NEWS[0][1], "Pro, Max, Ultra · rilascio graduale"),
             pr(t, 0.5), rise=70)
    fr.layer(lambda d: news_card(d, 1020, 2, NEWS[1][0], NEWS[1][1], "organizzazioni Enterprise idonee"),
             pr(t, 1.5), rise=70)


def b3(fr, t):
    header(fr, TP, 3, 4)
    Hd(fr, t, [[("E un foglio", B)], [("costruito ", B), ("in chat.", I)]], size=92)
    fr.layer(lambda d: news_card(d, 690, 3, NEWS[2][0], NEWS[2][1], "piani a pagamento · funzioni semplici"),
             pr(t, 0.5), rise=70)

    def c(d):
        card(d, MX, 1020, 900, 300, "prima di usarle", "metodo", NAVY)
        for i, s in enumerate(["controlla piano e stato beta", "decidi quali dati possono entrare"]):
            if pr(t, 1.6 + i * 0.4, 0.1) > 0:
                tick(d, MX + 50, 1150 + i * 85, True, 48, ORANGE if i == 0 else NAVY)
                T(d, (MX + 125, 1150 + i * 85), s, "M600", 36, NAVY, maxw=740)
    fr.layer(c, pr(t, 1.3), rise=70)


NOVITA = [(b1, 3.2), (b2, 3.8), (b3, 3.8),
          (cta(TP, 4, 4, "FINANCE", ["Ti indico le guide gratuite", "da cui partire."]), 3.6)]

REELS = {"sheets": (SHEETS, "2026-11-26", "claude_sheets"), "novita": (NOVITA, "2026-11-28", "novita_claude_novembre")}


def render(REEL, day, NAME):
    out_dir = os.path.join(MEDIA, day)
    os.makedirs(out_dir, exist_ok=True)
    files = []
    for i, (_, dur) in enumerate(REEL):
        out = os.path.join(TMP, f"s_{NAME}_{i}.mp4")
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                              "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18",
                              "-preset", "veryfast", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for k in range(round(dur * FPS)):
            p.stdin.write(frame(REEL, i, k / FPS).tobytes())
        p.stdin.close()
        assert p.wait() == 0
        files.append(out)
    lst = os.path.join(TMP, f"l_{NAME}.txt")
    with open(lst, "w") as f:
        for x in files:
            f.write(f"file '{x}'\n")
    muto = os.path.join(TMP, f"muto_{NAME}.mp4")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                           "-c", "copy", muto])
    dur = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                   "csv=p=0", muto]).decode().strip()
    wav = os.path.join(TMP, f"musica_{NAME}.wav")
    subprocess.check_call([sys.executable, os.path.join(S, "musica_classica.py"), "bach", dur, wav])
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", muto, "-i", wav, "-filter_complex",
                           "[1:a]lowpass=f=7000,highpass=f=40,loudnorm=I=-19:TP=-2[a]", "-map", "0:v",
                           "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
                           os.path.join(out_dir, f"reel_{NAME}_bach.mp4")])
    frame(REEL, 0, REEL[0][1] - 0.3).save(os.path.join(out_dir, f"cover_{NAME}.png"))
    for x in files + [lst, muto, wav]:
        os.remove(x)
    print("done", NAME, dur)


if __name__ == "__main__":
    mode = sys.argv[1]
    os.makedirs(TMP, exist_ok=True)
    for key in ([sys.argv[2]] if len(sys.argv) > 2 else list(REELS)):
        REEL, day, NAME = REELS[key]
        if mode == "preview":
            ims = [frame(REEL, i, d - 0.3).resize((540, 960)) for i, (_, d) in enumerate(REEL)]
            sh = Image.new("RGB", (540 * len(ims), 960))
            for i, im in enumerate(ims):
                sh.paste(im, (540 * i, 0))
            sh.save(os.path.join(TMP, f"sheet_{NAME}.png"))
        else:
            render(REEL, day, NAME)
