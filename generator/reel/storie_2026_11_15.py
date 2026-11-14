"""Storie Instagram del 15 novembre 2026 (1080x1920). Uso: python3 storie_2026_11_15.py [foglio_di_controllo.png]"""
import os, sys
from PIL import Image, ImageDraw
import render2 as r
import reels
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, PAPER, LINE, card, pill

OUT = os.path.join(os.path.dirname(os.path.dirname(r.S)), "media", "2026-11-15")
os.makedirs(OUT, exist_ok=True)
W, H, MX = 1080, 1920, 90
B, I = "b", "i"


def seg_w(segs, size):
    return sum((F("M800", size) if s == "b" else F("PFI", int(size * 1.08))).getlength(t) for t, s in segs)


def story(n, topic, lines, body):
    bg = Image.new("RGB", (W, H), PAPER)
    b = ImageDraw.Draw(bg)
    for x in range(0, W, 36):
        b.line([x, 0, x, H], fill=LINE)
    for y in range(0, H, 36):
        b.line([0, y, W, y], fill=LINE)
    bg = bg.convert("RGBA")
    ly = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ly)
    f = F("MONO", 30)
    d.text((MX, 270), "// ", font=f, fill=GREY)
    d.text((MX + f.getlength("// "), 270), f"0{n}", font=F("MONOB", 30), fill=ORANGE)
    d.text((MX + f.getlength("// 0n "), 270), f"· {topic}", font=f, fill=GREY)
    d.text((W - MX, 270), f"{n}/5", font=f, fill=GREY, anchor="ra")
    size = 88
    while max(seg_w(l, size) for l in lines) > W - 2 * MX:
        size -= 2
    for i, l in enumerate(lines):
        r.rich(d, MX, 460 + i * int(size * 1.2), l, size)
    body(d, 460 + len(lines) * int(size * 1.2) + 40)
    bg.alpha_composite(ly)
    bg.alpha_composite(reels.LOGO, (W - MX - 328, H - 390))
    bg.convert("RGB").save(os.path.join(OUT, f"storia_{n}.png"))


def check(d, x, cy, s=52):
    d.rounded_rectangle([x, cy - s // 2, x + s, cy + s // 2], 10, fill=ORANGE)
    d.line([x + 12, cy, x + 22, cy + 12, x + 40, cy - 12], fill=WHITE, width=7)


def st1(d, y):
    card(d, MX, y, 900, 500, "prima di aprire Excel", "domenica")
    for i, s in enumerate(["Consuntivo aggiornato", "Driver scelti", "Chi decide cosa"]):
        yy = y + 160 + i * 120
        check(d, MX + 50, yy)
        d.text((MX + 136, yy), s, font=F("M600", 42), fill=NAVY, anchor="lm")


def st2(d, y):
    card(d, MX, y, 900, 600, "punto di pareggio", "illustrativo")
    x0, x1, yb, yt = MX + 70, MX + 830, y + 520, y + 130
    d.line([x0, yt, x0, yb, x1, yb], fill=SOFT, width=6)
    d.line([x0, yb, x1 - 150, yt + 20], fill=ORANGE, width=10)          # ricavi
    d.line([x0, yb - 170, x1 - 150, yb - 300], fill=NAVY, width=10)     # costi
    # incrocio delle due rette
    rx = (x1 - 150 - x0)
    k_r, k_c = (yb - yt - 20) / rx, 130 / rx
    ix = x0 + 170 / (k_r - k_c)
    iy = yb - k_r * (ix - x0)
    d.ellipse([ix - 22, iy - 22, ix + 22, iy + 22], fill=WHITE, outline=NAVY, width=7)
    d.text((x1, yt + 20), "ricavi", font=F("MONOB", 28), fill=ORANGE, anchor="rm")
    d.text((x1, yb - 300), "costi", font=F("MONOB", 28), fill=NAVY, anchor="rm")
    d.text((ix + 40, iy + 46), "pareggio", font=F("M800", 34), fill=NAVY, anchor="lm")


def st3(d, y):
    cw = 435
    for k, (title, tag, c, rows) in enumerate((("all'AI", "sì", ORANGE, ["importi", "date", "categorie"]),
                                               ("fuori", "no", NAVY, ["nomi", "IBAN", "password"]))):
        x = MX + k * (cw + 30)
        card(d, x, y, cw, 520, title, tag, c)
        for i, s in enumerate(rows):
            yy = y + 170 + i * 120
            d.ellipse([x + 44, yy - 12, x + 68, yy + 12], fill=c)
            d.text((x + 96, yy), s, font=F("M800", 44), fill=NAVY, anchor="lm")


def st4(d, y):
    card(d, MX, y, 900, 500, "quadrature", "sempre")
    for i, s in enumerate(["Il totale è la somma delle righe?", "Il saldo finale torna?", "Da dove viene ogni dato?"]):
        yy = y + 160 + i * 120
        check(d, MX + 50, yy)
        reels.T(d, (MX + 136, yy), s, "M600", 42, NAVY, maxw=720)


def st5(d, y):
    card(d, MX, y, 900, 600, "budget 2027", "illustrativo")
    x0, x1, yb = MX + 70, MX + 560, y + 520
    d.line([x0, y + 130, x0, yb, MX + 830, yb], fill=SOFT, width=6)
    ys = y + 400
    for lab, ye, c in (("spinto", y + 170, GREY), ("base", y + 300, ORANGE), ("prudente", y + 430, NAVY)):
        d.line([x0, ys, x1, ye], fill=c, width=10)
        d.ellipse([x1 - 14, ye - 14, x1 + 14, ye + 14], fill=c)
        d.text((x1 + 40, ye), lab, font=F("M800", 38), fill=NAVY, anchor="lm")


story(1, "stagione del budget", [[("Domani parte", B)], [("il budget ", B), ("2027.", I)]], st1)
story(2, "controllo di gestione", [[("Sai dov'è", B)], [("il tuo punto di", B)], [("pareggio?", I)]], st2)
story(3, "AI per la finanza", [[("Prima di dare", B)], [("i dati all'AI,", B)], [("togli i ", B), ("nomi.", I)]], st3)
story(4, "Claude in pratica", [[("Non chiedere solo", B)], [("il risultato.", B)], [("Chiedi i ", B), ("controlli.", I)]], st4)
story(5, "stagione del budget", [[("Un solo scenario", B)], [("è una", B)], [("scommessa.", I)]], st5)

if len(sys.argv) > 1:
    ims = [Image.open(os.path.join(OUT, f"storia_{i}.png")) for i in range(1, 6)]
    sh = Image.new("RGB", (540 * 5, 960), "white")
    for i, im in enumerate(ims):
        sh.paste(im.resize((540, 960)), (540 * i, 0))
    sh.save(sys.argv[1])
