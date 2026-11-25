"""Reel e storie del 26 nov 2026. Reel: budget contro consuntivo, la routine del mese in 3 passi.
Grafici illustrativi, senza valori.
Uso: python3 contenuti_2026_11_26.py preview|full|storie
"""
import sys, os, subprocess
from PIL import Image
import render2 as r
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, card, pill, pr, ease
from reels import Hd, header, T, pillL, tick, typed, stamp, cta, frame, W, H, FPS, MX, B, I, S
import contenuti_2026_11_22_23 as c

MEDIA = c.MEDIA
DAY = "2026-11-26"
TMP = "/home/claude/reel"
TP = "budget 2027"
NAME = "budget_ogni_mese"
PASSI = [("Chiudi", "il mese, a data fissa"), ("Confronta", "budget e consuntivo"),
         ("Decidi", "chi fa cosa, entro quando")]
MESI = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]


# ---------------------------------------------------------------- reel
def v1(fr, t):
    header(fr, TP, 1, 4)
    Hd(fr, t, [[("Tieni vivo il budget", B)], [("tutto l'anno,", B)], [("in ", B), ("3 passi.", I)]], size=86)

    def k(d):
        card(d, MX, 800, 900, 560, "budget 2027 · dodici controlli", "illustrativo")
        for i, m in enumerate(MESI):
            x = MX + 50 + (i % 4) * 205
            y = 910 + (i // 4) * 140
            on = pr(t, 0.8 + i * 0.13, 0.1) > 0
            d.rounded_rectangle([x, y, x + 185, y + 110], 18, fill=SOFT, outline=NAVY, width=3)
            T(d, (x + 22, y + 55), m, "MONOB", 30, NAVY)
            tick(d, x + 112, y + 55, on, 50, ORANGE if i == 0 else NAVY)
    fr.layer(k, pr(t, 0.45), rise=70)


def v2(fr, t):
    header(fr, TP, 2, 4)
    Hd(fr, t, [[("Chiudi, confronta,", B)], [("poi ", B), ("decidi.", I)]], size=92)
    for i, (nm, q) in enumerate(PASSI):
        st, y = 0.6 + i * 0.75, 700 + i * 250

        def dr(d, i=i, nm=nm, q=q, st=st, y=y):
            card(d, MX, y, 900, 220, f"passo {i + 1}", f"0{i + 1}", ORANGE if i == 0 else NAVY)
            tick(d, MX + 40, y + 146, pr(t, st + 0.45, 0.1) > 0, 56, ORANGE)
            T(d, (MX + 125, y + 146), nm, "M800", 44, NAVY)
            T(d, (MX + 405, y + 146), q, "M600", 32, GREY, maxw=470)
        fr.layer(dr, pr(t, st), rise=70)


def v3(fr, t):
    header(fr, TP, 3, 4)
    Hd(fr, t, [[("L'AI prepara.", B)], [("Tu ", B), ("decidi.", I)]], size=96)

    def k(d):
        card(d, MX, 700, 900, 660, "budget e consuntivo", "illustrativo")
        x0, y0, w, h = MX + 60, 800, 780, 170
        d.line([x0, y0 + h, x0 + w, y0 + h], fill=SOFT, width=4)
        bud = [0.30, 0.42, 0.54, 0.66, 0.80, 0.94]
        con = [0.30, 0.34, 0.60, 0.44, 0.66, 0.56]
        for pts, col, st in ((bud, NAVY, 0.6), (con, ORANGE, 1.0)):
            q = pr(t, st, 0.7)
            n = len(pts) - 1
            xy = []
            for j in range(n + 1):
                if j / n <= q + 1e-6:
                    xy.append((x0 + w * j / n, y0 + h - h * pts[j]))
            if 0 < q < 1:
                j = int(q * n)
                f = q * n - j
                if j < n:
                    xy.append((x0 + w * (j + f) / n, y0 + h - h * (pts[j] + (pts[j + 1] - pts[j]) * f)))
            if len(xy) > 1:
                d.line(xy, fill=col, width=8, joint="curve")
        if t > 1.5:
            pillL(d, x0, y0 + h + 45, "budget", NAVY)
            pillL(d, x0 + 200, y0 + h + 45, "consuntivo", ORANGE)
        for i, s in enumerate(["carica il consuntivo del mese", "evidenzia le righe fuori soglia",
                               "prepara la pagina per la riunione"]):
            yy = 1090 + i * 80
            if pr(t, 1.7 + i * 0.3, 0.1) > 0:
                tick(d, MX + 50, yy, True, 48, NAVY)
                T(d, (MX + 125, yy), s, "M600", 36, NAVY, maxw=740)
        if t > 2.7:
            T(d, (MX + 450, 1318), "le azioni le decide chi firma", "MONO", 28, GREY, "mm")
    fr.layer(k, pr(t, 0.45), rise=70)


REEL = [(v1, 3.2), (v2, 3.8), (v3, 3.6),
        (cta(TP, 4, 4, "CONTROLLO", ["Ti mando la guida gratuita", "sul controllo di gestione."]), 3.6)]


# ---------------------------------------------------------------- storie
def s1(d, y):
    card(d, MX, y, 900, 540, "budget degli acquisti", "budget 2027")
    c.rows_check(d, y, ["parti dal budget delle vendite", "aggiungi la scorta che vuoi tenere",
                        "togli quella che hai già"], step=110, size=38)
    T(d, (MX + 450, y + 480), "quello che resta è da comprare", "MONO", 28, GREY, "mm")


def s2(d, y):
    card(d, MX, y, 900, 580, "ogni settimana", "tre indicatori")
    c.rows_pill(d, y, (("margine", "quanto resta sul venduto", NAVY), ("cassa", "il saldo previsto", ORANGE),
                       ("scaduto", "quanto non hai incassato", NAVY)), w=280)
    T(d, (MX + 450, y + 520), "pochi numeri, sempre gli stessi", "MONO", 28, GREY, "mm")


def s3(d, y):
    card(d, MX, y, 900, 540, "budget e consuntivo", "oggi sul profilo")
    for i, (nm, q) in enumerate(PASSI):
        yy = y + 150 + i * 105
        d.text((MX + 50, yy), f"0{i + 1}", font=F("MONOB", 34), fill=ORANGE, anchor="lm")
        T(d, (MX + 130, yy), nm, "M800", 38, NAVY)
        T(d, (MX + 390, yy), q, "M600", 30, GREY, maxw=470)
    T(d, (MX + 450, y + 480), "oggi sul profilo: il reel", "MONO", 28, GREY, "mm")


def s4(d, y):
    card(d, MX, y, 900, 580, "rata del finanziamento", "budget di cassa")
    c.rows_pill(d, y, (("interessi", "vanno nel conto economico", NAVY), ("capitale", "esce solo dalla cassa", ORANGE),
                       ("data", "il mese in cui paghi", NAVY)), w=280)
    T(d, (MX + 450, y + 520), "per questo utile e cassa non coincidono", "MONO", 28, GREY, "mm")


def s5(d, y):
    card(d, MX, y, 900, 560, "cassa a 13 settimane", "tesoreria")
    c.rows_check(d, y, ["incassi attesi, settimana per settimana", "uscite già note",
                        "il saldo più basso del periodo"], step=110, size=36)
    T(d, (MX + 450, y + 480), "la guida gratuita è nella libreria", "MONO", 28, GREY, "mm")
    T(d, (MX + 450, y + 522), "controlia.it/libreria", "MONOB", 28, ORANGE, "mm")


def storie():
    c.story(DAY, 1, "budget 2027", [[("Gli acquisti", B)], [("seguono ", B), ("le vendite.", I)]], s1)
    c.story(DAY, 2, "controllo di gestione", [[("Tre indicatori,", B)], [("ogni ", B), ("settimana.", I)]], s2)
    c.story(DAY, 3, "budget 2027", [[("Il budget si guarda", B)], [("ogni ", B), ("mese.", I)]], s3)
    c.story(DAY, 4, "budget 2027", [[("La rata non è", B)], [("tutta ", B), ("costo.", I)]], s4)
    c.story(DAY, 5, "tesoreria", [[("Guarda la cassa", B)], [("a ", B), ("13 settimane.", I)]], s5)
    ims = [Image.open(os.path.join(MEDIA, DAY, f"storia_{i}.png")).resize((432, 768)) for i in range(1, 6)]
    sh = Image.new("RGB", (432 * 5, 768))
    for i, im in enumerate(ims):
        sh.paste(im, (432 * i, 0))
    sh.save(os.path.join(TMP, "sheet_storie_26.png"))


if __name__ == "__main__":
    mode = sys.argv[1]
    os.makedirs(TMP, exist_ok=True)
    out_dir = os.path.join(MEDIA, DAY)
    os.makedirs(out_dir, exist_ok=True)
    if mode == "storie":
        storie()
    elif mode == "preview":
        ims = [frame(REEL, i, d - 0.3).resize((540, 960)) for i, (_, d) in enumerate(REEL)]
        ims.append(frame(REEL, 0, 1.6).resize((540, 960)))
        sh = Image.new("RGB", (540 * len(ims), 960))
        for i, im in enumerate(ims):
            sh.paste(im, (540 * i, 0))
        sh.save(os.path.join(TMP, f"sheet_{NAME}.png"))
    else:
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
