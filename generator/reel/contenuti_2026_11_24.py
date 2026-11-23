"""Reel e storie del 24 nov 2026. Reel: ricavi sotto budget, tre domande (prezzo, volume, mix).
Grafici illustrativi, senza valori.
Uso: python3 contenuti_2026_11_24.py preview|full|storie
"""
import sys, os, subprocess
from PIL import Image
import render2 as r
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, card, pill, pr, ease
from reels import Hd, header, T, pillL, tick, typed, stamp, cta, frame, W, H, FPS, MX, B, I, S
import contenuti_2026_11_22_23 as c

MEDIA = c.MEDIA
DAY = "2026-11-24"
TMP = "/home/claude/reel"
TP = "budget 2027"
NAME = "scostamento_3_domande"
DOM = [("Prezzo", "Hai venduto a meno?"), ("Volume", "Hai venduto meno pezzi?"),
       ("Mix", "Hai venduto prodotti diversi?")]


# ---------------------------------------------------------------- reel
def v1(fr, t):
    header(fr, TP, 1, 4)
    Hd(fr, t, [[("Ricavi sotto budget?", B)], [("Trova il perché", B)], [("in ", B), ("3 domande.", I)]], size=88)

    def k(d):
        card(d, MX, 800, 900, 560, "ricavi · budget e consuntivo", "illustrativo")
        base = 1290
        d.line([MX + 60, base, MX + 840, base], fill=SOFT, width=4)
        q1, q2 = pr(t, 0.7, 0.6), pr(t, 1.0, 0.6)
        d.rounded_rectangle([MX + 170, base - 340 * q1, MX + 370, base], 14, fill=NAVY)
        d.rounded_rectangle([MX + 500, base - 215 * q2, MX + 700, base], 14, fill=ORANGE)
        T(d, (MX + 270, base + 36), "budget", "MONOB", 28, NAVY, "mm")
        T(d, (MX + 600, base + 36), "consuntivo", "MONOB", 28, ORANGE, "mm")
        if t > 1.7:
            for x in range(MX + 380, MX + 720, 26):
                d.line([x, base - 340, x + 13, base - 340], fill=GREY, width=4)
            d.line([MX + 740, base - 340, MX + 740, base - 215], fill=NAVY, width=5)
            T(d, (MX + 790, base - 278), "?", "M900", 90, ORANGE, "mm")
    fr.layer(k, pr(t, 0.45), rise=70)


def v2(fr, t):
    header(fr, TP, 2, 4)
    Hd(fr, t, [[("Prezzo, volume", B)], [("o ", B), ("mix?", I)]], size=96)
    for i, (nm, q) in enumerate(DOM):
        st, y = 0.6 + i * 0.75, 700 + i * 250

        def dr(d, i=i, nm=nm, q=q, st=st, y=y):
            card(d, MX, y, 900, 220, f"domanda {i + 1}", f"0{i + 1}", ORANGE if i == 0 else NAVY)
            tick(d, MX + 40, y + 146, pr(t, st + 0.45, 0.1) > 0, 56, ORANGE)
            T(d, (MX + 125, y + 146), nm, "M800", 46, NAVY)
            T(d, (MX + 330, y + 146), q, "M600", 34, GREY, maxw=540)
        fr.layer(dr, pr(t, st), rise=70)


def v3(fr, t):
    header(fr, TP, 3, 4)
    Hd(fr, t, [[("L'AI scompone.", B)], [("Tu ", B), ("spieghi.", I)]], size=96)

    def k(d):
        card(d, MX, 700, 900, 640, "lo scostamento, a pezzi", "illustrativo")
        x0, y0 = MX + 50, 820
        segs = [(300, NAVY, "prezzo"), (330, ORANGE, "volume"), (170, GREY, "mix")]
        x = x0
        for i, (wd, col, lab) in enumerate(segs):
            q = pr(t, 0.7 + i * 0.4, 0.4)
            if q > 0:
                d.rounded_rectangle([x, y0, x + wd * q - 8, y0 + 80], 14, fill=col)
                if q >= 1:
                    T(d, (x + wd / 2 - 4, y0 + 40), lab, "MONOB", 26, WHITE, "mm")
            x += wd
        for i, s in enumerate(["scompone lo scostamento", "trova le righe che pesano", "scrive la bozza del commento"]):
            yy = 990 + i * 90
            if pr(t, 1.7 + i * 0.3, 0.1) > 0:
                tick(d, MX + 50, yy, True, 50, NAVY)
                T(d, (MX + 130, yy), s, "M600", 38, NAVY, maxw=730)
        if t > 2.7:
            T(d, (MX + 450, 1290), "la causa la confermi tu", "MONO", 28, GREY, "mm")
    fr.layer(k, pr(t, 0.45), rise=70)


REEL = [(v1, 3.2), (v2, 3.8), (v3, 3.6),
        (cta(TP, 4, 4, "CONTROLLO", ["Ti mando la guida gratuita", "sul controllo di gestione."]), 3.6)]


# ---------------------------------------------------------------- storie
def s1(d, y):
    card(d, MX, y, 900, 540, "prima del budget", "prezzi 2027")
    c.rows_check(d, y, ["quali prezzi aumenti", "da quale mese", "per quali clienti"], step=110, size=40)
    T(d, (MX + 450, y + 480), "il prezzo è un'ipotesi, non un risultato", "MONO", 28, GREY, "mm")


def s2(d, y):
    card(d, MX, y, 900, 580, "report del mese", "una pagina")
    c.rows_pill(d, y, (("numeri", "pochi, sempre gli stessi", NAVY), ("scostamenti", "solo quelli che pesano", ORANGE),
                       ("azioni", "chi fa cosa, entro quando", NAVY)), w=300)
    T(d, (MX + 450, y + 520), "il dettaglio va in allegato", "MONO", 28, GREY, "mm")


def s3(d, y):
    card(d, MX, y, 900, 540, "ricavi sotto budget", "oggi sul profilo")
    for i, (nm, q) in enumerate(DOM):
        yy = y + 150 + i * 105
        d.text((MX + 50, yy), f"0{i + 1}", font=F("MONOB", 34), fill=ORANGE, anchor="lm")
        T(d, (MX + 130, yy), nm, "M800", 40, NAVY)
        T(d, (MX + 320, yy), q, "M600", 32, GREY, maxw=530)
    T(d, (MX + 450, y + 480), "oggi sul profilo: il reel", "MONO", 28, GREY, "mm")


def s4(d, y):
    card(d, MX, y, 900, 580, "tre colonne", "budget flessibile")
    c.rows_pill(d, y, (("budget", "sui volumi previsti", NAVY), ("flessibile", "ricalcolato sui volumi reali", ORANGE),
                       ("consuntivo", "quello che è successo", NAVY)), w=290)
    T(d, (MX + 450, y + 520), "così vedi se hai speso di più o prodotto di più", "MONO", 28, GREY, "mm", maxw=820)


def s5(d, y):
    card(d, MX, y, 900, 580, "AI 4 Finance", "ControlIA", NAVY)
    c.rows_check(d, y, ["il report del mese lo prepara l'AI", "gli scostamenti arrivano in bozza",
                        "il tuo team rilegge e firma"], step=110, size=36)
    T(d, (MX + 450, y + 480), "la metrica: ore restituite al team", "MONO", 28, GREY, "mm")
    T(d, (MX + 450, y + 528), "scrivimi FINANCE in DM", "MONOB", 28, ORANGE, "mm")


def storie():
    c.story(DAY, 1, "budget 2027", [[("Il listino 2027", B)], [("si decide ", B), ("prima", I)], [("del budget.", B)]], s1)
    c.story(DAY, 2, "controllo di gestione", [[("Il report mensile", B)], [("sta in ", B), ("una pagina.", I)]], s2)
    c.story(DAY, 3, "budget 2027", [[("Sotto budget?", B)], [("Tre ", B), ("domande.", I)]], s3)
    c.story(DAY, 4, "budget 2027", [[("Confronta a parità", B)], [("di ", B), ("volumi.", I)]], s4)
    c.story(DAY, 5, "ControlIA", [[("Reporting e controllo,", B)], [("con ", B), ("l'AI.", I)]], s5)
    ims = [Image.open(os.path.join(MEDIA, DAY, f"storia_{i}.png")).resize((432, 768)) for i in range(1, 6)]
    sh = Image.new("RGB", (432 * 5, 768))
    for i, im in enumerate(ims):
        sh.paste(im, (432 * i, 0))
    sh.save(os.path.join(TMP, "sheet_storie_24.png"))


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
