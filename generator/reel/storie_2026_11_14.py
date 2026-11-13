"""Storie Instagram del 14 novembre 2026 (1080x1920). Uso: python3 storie_2026_11_14.py"""
import os
from PIL import Image, ImageDraw
import render2 as r
import reels
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, PAPER, LINE, card, pill

OUT = os.path.join(os.path.dirname(os.path.dirname(r.S)), "media", "2026-11-14")
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
    card(d, MX, y, 900, 500, "sabato mattina", "10 minuti")
    for i, s in enumerate(["Cosa ho incassato?", "Cosa è uscito?", "Cosa scade lunedì?"]):
        yy = y + 160 + i * 120
        check(d, MX + 50, yy)
        d.text((MX + 136, yy), s, font=F("M600", 42), fill=NAVY, anchor="lm")


def st2(d, y):
    card(d, MX, y, 900, 600, "skill", "procedura")
    for i, s in enumerate(["Quali dati raccogliere", "Come si calcola", "Quali quadrature fare", "Come si consegna"]):
        yy = y + 160 + i * 115
        d.rounded_rectangle([MX + 50, yy - 40, MX + 130, yy + 40], 18, fill=ORANGE if i == 0 else NAVY)
        d.text((MX + 90, yy), str(i + 1), font=F("M900", 44), fill=WHITE, anchor="mm")
        d.text((MX + 160, yy), s, font=F("M600", 42), fill=NAVY, anchor="lm")


def st3(d, y):
    cw = 435
    for k, (title, tag, c, rows) in enumerate((("AI", "prepara", ORANGE, ["raccoglie", "riconcilia", "segnala"]),
                                               ("tu", "decidi", NAVY, ["verifichi", "scegli", "firmi"]))):
        x = MX + k * (cw + 30)
        card(d, x, y, cw, 520, title, tag, c)
        for i, s in enumerate(rows):
            yy = y + 170 + i * 120
            d.ellipse([x + 44, yy - 12, x + 68, yy + 12], fill=c)
            d.text((x + 96, yy), s, font=F("M800", 44), fill=NAVY, anchor="lm")


def st4(d, y):
    card(d, MX, y, 900, 620, "budget 2027", "da lunedì")
    steps = ["Driver", "Vendite", "Costi", "Cassa"]
    for i, s in enumerate(steps):
        yy = y + 160 + i * 120
        d.rounded_rectangle([MX + 50, yy - 44, MX + 50 + 420 + i * 110, yy + 44], 22,
                            fill=ORANGE if i == 3 else SOFT)
        d.text((MX + 86, yy), s, font=F("M800", 44), fill=WHITE if i == 3 else NAVY, anchor="lm")
        if i < 3:
            ax = MX + 110
            d.line([ax, yy + 48, ax, yy + 72], fill=NAVY, width=6)
            d.polygon([(ax - 12, yy + 64), (ax + 12, yy + 64), (ax, yy + 78)], fill=NAVY)


def st5(d, y):
    card(d, MX, y, 900, 560, "utile e cassa", "illustrativo")
    for i, (lab, wd, c) in enumerate((("Utile", 620, NAVY), ("Cassa", 300, ORANGE))):
        yy = y + 150 + i * 130
        d.text((MX + 50, yy), lab, font=F("M800", 40), fill=NAVY, anchor="lm")
        d.rounded_rectangle([MX + 50, yy + 34, MX + 50 + wd, yy + 66], 16, fill=c)
    d.text((MX + 50, y + 430), "In mezzo: crediti da incassare,", font=F("M600", 38), fill=GREY, anchor="lm")
    d.text((MX + 50, y + 486), "scorte, rate, imposte.", font=F("M600", 38), fill=GREY, anchor="lm")


story(1, "controllo di gestione", [[("Tre domande", B)], [("sui numeri della", B)], [("settimana.", I)]], st1)
story(2, "Claude in pratica", [[("Prima del prompt,", B)], [("scrivi la", B)], [("procedura.", I)]], st2)
story(3, "AI per la finanza", [[("L'AI prepara.", B)], [("Tu ", B), ("firmi.", I)]], st3)
story(4, "stagione del budget", [[("Il budget parte", B)], [("dai driver,", B)], [("non dai ", B), ("numeri.", I)]], st4)
story(5, "controllo di gestione", [[("L'utile", B)], [("non è ", B), ("cassa.", I)]], st5)

ims = [Image.open(os.path.join(OUT, f"storia_{i}.png")) for i in range(1, 6)]
sh = Image.new("RGB", (540 * 5, 960), "white")
for i, im in enumerate(ims):
    sh.paste(im.resize((540, 960)), (540 * i, 0))
sh.save("/tmp/claude-0/-home-claude/95b1d4ce-a0ac-585c-b646-d0f24d564b21/scratchpad/sheet.png")
