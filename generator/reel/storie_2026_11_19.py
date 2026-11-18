"""Storie Instagram del 19 novembre 2026 (1080x1920). Uso: python3 storie_2026_11_19.py [foglio_di_controllo.png]"""
import os, sys
from PIL import Image, ImageDraw
import render2 as r
import reels
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, PAPER, LINE, card, pill

OUT = os.path.join(os.path.dirname(os.path.dirname(r.S)), "media", "2026-11-19")
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
    card(d, MX, y, 900, 640, "vendite per mese", "illustrativo")
    hs = (120, 150, 210, 240, 270, 230, 180, 70, 220, 280, 300, 190)
    base = y + 480
    for i, (h, m) in enumerate(zip(hs, "GFMAMGLASOND")):
        x = MX + 62 + i * 66
        d.rounded_rectangle([x, base - h, x + 46, base], 10, fill=ORANGE if i == 7 else NAVY)
        reels.T(d, (x + 23, base + 34), m, "MONOB", 26, GREY, "mm")
    reels.T(d, (MX + 450, y + 578), "il budget si distribuisce mese per mese", "MONO", 28, GREY, "mm")


def st2(d, y):
    card(d, MX, y, 900, 600, "budget investimenti", "budget 2027")
    rows_pill(d, y, (("ordine", "quando ti impegni", ORANGE), ("consegna", "quando lo usi", NAVY),
                     ("pagamento", "quando paghi", NAVY)), w=370)
    reels.T(d, (MX + 450, y + 535), "la cassa segue il pagamento", "MONO", 28, GREY, "mm")


def st3(d, y):
    card(d, MX, y, 900, 650, "ciclo del budget", "nuovo reel")
    rows_check(d, y, ["i driver", "vendite e costi", "la cassa", "gli scenari"])
    reels.T(d, (MX + 450, y + 588), "oggi sul profilo: il reel sulla lavagna", "MONO", 28, GREY, "mm")


def st4(d, y):
    card(d, MX, y, 900, 600, "in corso d'anno", "budget 2027")
    rows_pill(d, y, (("marzo", "primo confronto", ORANGE), ("giugno", "revisione", NAVY),
                     ("settembre", "stima di chiusura", NAVY)))
    reels.T(d, (MX + 450, y + 535), "un budget fermo invecchia", "MONO", 28, GREY, "mm")


def st5(d, y):
    card(d, MX, y, 900, 640, "crediti scaduti", "illustrativo")
    for i, (s, w, c) in enumerate((("0-30", 470, NAVY), ("31-60", 330, NAVY), ("61-90", 220, NAVY), ("oltre 90", 140, ORANGE))):
        yy = y + 160 + i * 100
        reels.T(d, (MX + 50, yy), s, "M800", 42, NAVY)
        d.rounded_rectangle([MX + 300, yy - 34, MX + 300 + w, yy + 34], 18, fill=c)
    reels.T(d, (MX + 450, y + 548), "giorni di ritardo", "MONO", 28, GREY, "mm")
    reels.T(d, (MX + 450, y + 590), "ogni fascia, un'azione diversa", "MONO", 28, GREY, "mm")


story(1, "budget 2027", [[("Dodici mesi", B)], [("uguali", I), (" non", B)], [("esistono.", B)]], st1)
story(2, "budget 2027", [[("Un investimento", B)], [("ha ", B), ("tre date.", I)]], st2)
story(3, "budget 2027", [[("Prima il", B)], [("processo,", I)], [("poi i numeri.", B)]], st3)
story(4, "budget 2027", [[("Fissa ora", B)], [("le date della", B)], [("revisione.", I)]], st4)
story(5, "tesoreria e crediti", [[("Lo scaduto", B)], [("si guarda", B)], [("per fasce.", I)]], st5)

if len(sys.argv) > 1:
    ims = [Image.open(os.path.join(OUT, f"storia_{i}.png")) for i in range(1, 6)]
    sh = Image.new("RGB", (540 * 5, 960), "white")
    for i, im in enumerate(ims):
        sh.paste(im.resize((540, 960)), (540 * i, 0))
    sh.save(sys.argv[1])
