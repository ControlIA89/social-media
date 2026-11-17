"""Storie Instagram del 18 novembre 2026 (1080x1920). Uso: python3 storie_2026_11_18.py [foglio_di_controllo.png]"""
import os, sys
from PIL import Image, ImageDraw
import render2 as r
import reels
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, PAPER, LINE, card, pill

OUT = os.path.join(os.path.dirname(os.path.dirname(r.S)), "media", "2026-11-18")
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


def rows_pill(d, y, items, w=350, step=125):
    for i, (s, sub, c) in enumerate(items):
        yy = y + 170 + i * step
        d.rounded_rectangle([MX + 50, yy - 46, MX + 50 + w, yy + 46], 22, fill=c)
        reels.T(d, (MX + 50 + w // 2, yy), s, "M800", 40, WHITE, "mm")
        reels.T(d, (MX + 90 + w, yy), sub, "M600", 38, NAVY, maxw=800 - w - 40)


def rows_check(d, y, items):
    for i, s in enumerate(items):
        yy = y + 160 + i * 110
        check(d, MX + 50, yy)
        reels.T(d, (MX + 136, yy), s, "M600", 42, NAVY, maxw=720)


def st1(d, y):
    card(d, MX, y, 900, 650, "chi porta i numeri", "budget 2027")
    rows_pill(d, y, (("vendite", "volumi e prezzi", ORANGE), ("acquisti", "costi dei materiali", NAVY),
                     ("produzione", "capacità e tempi", NAVY), ("personale", "organico e ingressi", NAVY)), step=112)
    reels.T(d, (MX + 450, y + 590), "l'amministrazione mette insieme", "MONO", 28, GREY, "mm")


def st2(d, y):
    card(d, MX, y, 900, 620, "registro delle ipotesi", "tre righe")
    rows_check(d, y, ["cosa ho ipotizzato", "chi l'ha deciso", "quando, e su quale dato"])
    d.rounded_rectangle([MX + 50, y + 470, MX + 850, y + 570], 22, fill=NAVY)
    reels.T(d, (MX + 450, y + 520), "a marzo saprai ancora il perché", "M800", 38, WHITE, "mm")


def st3(d, y):
    card(d, MX, y, 900, 600, "fine riunione", "nuovo reel")
    rows_pill(d, y, (("decisione", "cosa abbiamo deciso", ORANGE), ("responsabile", "chi lo fa", NAVY),
                     ("scadenza", "entro quando", NAVY)), w=370)
    reels.T(d, (MX + 450, y + 535), "oggi sul profilo: il reel sul verbale", "MONO", 28, GREY, "mm")


def st4(d, y):
    card(d, MX, y, 900, 650, "budget del personale", "per persona")
    rows_check(d, y, ["chi c'è oggi", "chi entra, e da che mese", "chi esce", "aumenti già previsti"])
    reels.T(d, (MX + 450, y + 588), "prima le persone, poi la somma", "MONO", 28, GREY, "mm")


def st5(d, y):
    card(d, MX, y, 900, 600, "scostamento", "illustrativo")
    for i, (s, w, c) in enumerate((("prezzo", 430, ORANGE), ("volume", 300, NAVY), ("mix", 180, NAVY))):
        yy = y + 170 + i * 120
        reels.T(d, (MX + 50, yy), s, "M800", 42, NAVY)
        d.rounded_rectangle([MX + 270, yy - 34, MX + 270 + w, yy + 34], 18, fill=c)
    reels.T(d, (MX + 450, y + 535), "tre cause, tre decisioni diverse", "MONO", 28, GREY, "mm")


story(1, "budget 2027", [[("Il budget non", B)], [("lo scrive ", B), ("solo", I)], [("l'amministrazione.", B)]], st1)
story(2, "budget 2027", [[("Ogni ipotesi", B)], [("ha un ", B), ("nome", I)], [("e una data.", B)]], st2)
story(3, "budget 2027", [[("La riunione di", B)], [("budget finisce", B)], [("con ", B), ("tre cose.", I)]], st3)
story(4, "budget 2027", [[("Il costo del", B)], [("personale si fa", B)], [("per ", B), ("persona.", I)]], st4)
story(5, "controllo di gestione", [[("Lo scostamento", B)], [("va ", B), ("spiegato,", I)], [("non solo letto.", B)]], st5)

if len(sys.argv) > 1:
    ims = [Image.open(os.path.join(OUT, f"storia_{i}.png")) for i in range(1, 6)]
    sh = Image.new("RGB", (540 * 5, 960), "white")
    for i, im in enumerate(ims):
        sh.paste(im.resize((540, 960)), (540 * i, 0))
    sh.save(sys.argv[1])
