"""Storie Instagram del 16 novembre 2026 (1080x1920). Uso: python3 storie_2026_11_16.py [foglio_di_controllo.png]"""
import os, sys
from PIL import Image, ImageDraw
import render2 as r
import reels
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, PAPER, LINE, card, pill

OUT = os.path.join(os.path.dirname(os.path.dirname(r.S)), "media", "2026-11-16")
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
    card(d, MX, y, 900, 560, "budget delle vendite", "tre leve")
    for i, (s, sub, c) in enumerate((("prezzo", "a quanto vendi", NAVY), ("volumi", "quanto vendi", NAVY),
                                     ("mix", "cosa vendi di più", ORANGE))):
        yy = y + 170 + i * 135
        d.rounded_rectangle([MX + 50, yy - 50, MX + 330, yy + 50], 22, fill=c)
        reels.T(d, (MX + 190, yy), s, "M800", 46, WHITE, "mm")
        reels.T(d, (MX + 370, yy), sub, "M600", 40, NAVY, maxw=480)
        if i < 2:
            reels.T(d, (MX + 190, yy + 68), "×", "M800", 44, GREY, "mm")


def st2(d, y):
    cw = 435
    for k, (title, tag, c, rows) in enumerate((("fissi", "ci sono sempre", NAVY, ["affitti", "personale", "canoni"]),
                                               ("variabili", "con le vendite", ORANGE, ["materiali", "trasporti", "provvigioni"]))):
        x = MX + k * (cw + 30)
        card(d, x, y, cw, 520, title, None)
        reels.T(d, (x + 40, y + 122), tag, "MONOB", 26, c)
        for i, s in enumerate(rows):
            yy = y + 220 + i * 105
            d.ellipse([x + 44, yy - 12, x + 68, yy + 12], fill=c)
            reels.T(d, (x + 96, yy), s, "M800", 42, NAVY, maxw=310)


def st3(d, y):
    card(d, MX, y, 900, 520, "dal documento all'incasso", "illustrativo")
    xs = [MX + 60 + i * 200 for i in range(4)]
    for i, m in enumerate(("gen", "feb", "mar", "apr")):
        on = i in (0, 3)
        d.rounded_rectangle([xs[i], y + 150, xs[i] + 180, y + 270], 20, fill=(ORANGE if i == 3 else NAVY) if on else SOFT)
        reels.T(d, (xs[i] + 90, y + 210), m, "M800", 44, WHITE if on else GREY, "mm")
    d.line([xs[0] + 90, y + 310, xs[0] + 90, y + 345, xs[3] + 90, y + 345, xs[3] + 90, y + 310], fill=GREY, width=6)
    reels.T(d, (xs[0], y + 410), "fatturi", "M800", 42, NAVY)
    reels.T(d, (xs[3] + 180, y + 410), "incassi", "M800", 42, ORANGE, "rm")
    reels.T(d, (W // 2, y + 470), "in mezzo paghi fornitori e stipendi", "MONO", 28, GREY, "mm")


def st4(d, y):
    card(d, MX, y, 900, 500, "domande da fare", "sempre")
    for i, s in enumerate(["Su quali dati ti basi?", "Cosa cambia se sbaglio?", "Quale dato manca?"]):
        yy = y + 160 + i * 120
        check(d, MX + 50, yy)
        reels.T(d, (MX + 136, yy), s, "M600", 42, NAVY, maxw=720)


def st5(d, y):
    card(d, MX, y, 900, 600, "errore tipico", "illustrativo")
    yb = y + 480
    d.line([MX + 50, yb, MX + 850, yb], fill=SOFT, width=6)
    hs = (150, 230, 180, 270)
    for g, (lab, c, extra) in enumerate((("2026", NAVY, 0), ("2027", ORANGE, 18))):
        x0 = MX + 80 + g * 410
        for k, hh in enumerate(hs):
            bx = x0 + k * 82
            d.rounded_rectangle([bx, yb - hh - extra, bx + 60, yb], 10, fill=c)
        reels.T(d, (x0 + 153, yb + 55), lab, "M800", 40, NAVY, "mm")
    reels.T(d, (MX + 450, y + 150), "stessa forma, un po' più alto", "MONO", 28, GREY, "mm")


story(1, "budget 2027", [[("Il budget delle", B)], [("vendite parte", B)], [("da ", B), ("tre leve.", I)]], st1)
story(2, "controllo di gestione", [[("Costi fissi", B)], [("o variabili?", B)], [("Separali.", I)]], st2)
story(3, "budget 2027", [[("Budget di cassa:", B)], [("conta ", B), ("quando", I)], [("incassi.", B)]], st3)
story(4, "AI per la finanza", [[("All'AI chiedi", B)], [("le ipotesi,", B)], [("non ", B), ("il numero.", I)]], st4)
story(5, "budget 2027", [[("Il 2027 non è", B)], [("il 2026 con", B)], [("un ", B), ("ritocco.", I)]], st5)

if len(sys.argv) > 1:
    ims = [Image.open(os.path.join(OUT, f"storia_{i}.png")) for i in range(1, 6)]
    sh = Image.new("RGB", (540 * 5, 960), "white")
    for i, im in enumerate(ims):
        sh.paste(im.resize((540, 960)), (540 * i, 0))
    sh.save(sys.argv[1])
