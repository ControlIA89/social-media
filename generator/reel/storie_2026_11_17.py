"""Storie Instagram del 17 novembre 2026 (1080x1920). Uso: python3 storie_2026_11_17.py [foglio_di_controllo.png]"""
import os, sys
from PIL import Image, ImageDraw
import render2 as r
import reels
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, PAPER, LINE, card, pill

OUT = os.path.join(os.path.dirname(os.path.dirname(r.S)), "media", "2026-11-17")
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
    card(d, MX, y, 900, 560, "budget dei costi", "tre famiglie")
    for i, (s, sub, c) in enumerate((("variabili", "seguono i volumi", ORANGE), ("di struttura", "confermi o tagli", NAVY),
                                     ("nuovi", "li decidi adesso", NAVY))):
        yy = y + 170 + i * 135
        d.rounded_rectangle([MX + 50, yy - 50, MX + 400, yy + 50], 22, fill=c)
        reels.T(d, (MX + 225, yy), s, "M800", 44, WHITE, "mm")
        reels.T(d, (MX + 440, yy), sub, "M600", 40, NAVY, maxw=410)


def st2(d, y):
    card(d, MX, y, 900, 600, "budget e consuntivo", "illustrativo")
    x0, x1, yb = MX + 70, MX + 830, y + 470
    d.line([x0, yb, x1, yb], fill=SOFT, width=6)
    n = 6
    xs = [x0 + 30 + i * (x1 - x0 - 60) / (n - 1) for i in range(n)]
    bud = [yb - 110 - i * 34 for i in range(n)]
    con = [bud[0] + 6, bud[1] + 22, bud[2] + 10, bud[3] + 46, bud[4] + 70, bud[5] + 84]
    d.polygon(list(zip(xs[2:], bud[2:])) + list(zip(xs[2:], con[2:]))[::-1], fill=(255, 107, 0, 50))
    for i in range(n - 1):
        for k in range(6):
            if k % 2 == 0:
                a, b2 = k / 6, (k + 1) / 6
                d.line([xs[i] + (xs[i + 1] - xs[i]) * a, bud[i] + (bud[i + 1] - bud[i]) * a,
                        xs[i] + (xs[i + 1] - xs[i]) * b2, bud[i] + (bud[i + 1] - bud[i]) * b2], fill=NAVY, width=8)
    d.line(list(zip(xs, con)), fill=ORANGE, width=10, joint="curve")
    for x, yy in zip(xs, con):
        d.ellipse([x - 13, yy - 13, x + 13, yy + 13], fill=ORANGE)
    reels.T(d, (xs[5] - 10, bud[5] - 44), "budget", "M800", 36, NAVY, "rm")
    reels.T(d, (xs[5] + 20, con[5] + 60), "consuntivo", "M800", 36, ORANGE, "rm")
    reels.T(d, (MX + 450, y + 530), "lo scostamento si guarda ogni mese", "MONO", 28, GREY, "mm")


def st3(d, y):
    card(d, MX, y, 900, 560, "nuovo carosello", "oggi sul profilo")
    for i, s in enumerate(["la chiusura del mese", "il margine per cliente", "il cash flow"]):
        yy = y + 165 + i * 115
        d.rounded_rectangle([MX + 50, yy - 26, MX + 102, yy + 26], 10, outline=NAVY, width=5)
        reels.T(d, (MX + 136, yy), s, "M600", 42, NAVY, maxw=720)
    reels.T(d, (MX + 450, y + 495), "tre controlli da fare sui tuoi numeri", "MONO", 28, GREY, "mm")


def st4(d, y):
    card(d, MX, y, 900, 620, "budget con l'AI", "chi fa cosa")
    for i, s in enumerate(["raccolta dei dati", "controlli di quadratura", "prima bozza delle ipotesi"]):
        yy = y + 160 + i * 110
        check(d, MX + 50, yy)
        reels.T(d, (MX + 136, yy), s, "M600", 42, NAVY, maxw=720)
    d.rounded_rectangle([MX + 50, y + 470, MX + 850, y + 570], 22, fill=NAVY)
    reels.T(d, (MX + 450, y + 520), "la decisione resta a chi firma", "M800", 38, WHITE, "mm")


def st5(d, y):
    card(d, MX, y, 900, 540, "revisione in corso d'anno", "2027")
    for i in range(4):
        x = MX + 60 + i * 200
        d.rounded_rectangle([x, y + 150, x + 180, y + 270], 20, fill=ORANGE if i == 0 else NAVY)
        reels.T(d, (x + 90, y + 210), f"T{i + 1}", "M800", 46, WHITE, "mm")
        check(d, x + 64, y + 330)
    reels.T(d, (MX + 450, y + 420), "a ogni trimestre: cosa è cambiato?", "M600", 38, NAVY, "mm")
    reels.T(d, (MX + 450, y + 480), "ipotesi, prezzi, costi, cassa", "MONO", 28, GREY, "mm")


story(1, "budget 2027", [[("Il budget dei", B)], [("costi: tre", B)], [("famiglie.", I)]], st1)
story(2, "budget 2027", [[("Il budget serve", B)], [("se lo ", B), ("confronti", I)], [("ogni mese.", B)]], st2)
story(3, "controllo di gestione", [[("3 segnali che", B)], [("il controllo è", B)], [("in ritardo.", I)]], st3)
story(4, "budget 2027", [[("Nel budget,", B)], [("cosa ", B), ("delego", I)], [("all'AI.", B)]], st4)
story(5, "budget 2027", [[("Il budget non", B)], [("va chiuso in un", B)], [("cassetto.", I)]], st5)

if len(sys.argv) > 1:
    ims = [Image.open(os.path.join(OUT, f"storia_{i}.png")) for i in range(1, 6)]
    sh = Image.new("RGB", (540 * 5, 960), "white")
    for i, im in enumerate(ims):
        sh.paste(im.resize((540, 960)), (540 * i, 0))
    sh.save(sys.argv[1])
