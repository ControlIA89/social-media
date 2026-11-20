"""Carosello (1080x1350, 7 slide) e storie (1080x1920) del 21 novembre 2026.
Uso: python3 storie_2026_11_21.py [foglio_di_controllo_prefisso]"""
import os, sys
from PIL import Image, ImageDraw
import render2 as r
import reels
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, PAPER, LINE, card, pill

OUT = os.path.join(os.path.dirname(os.path.dirname(r.S)), "media", "2026-11-21")
os.makedirs(OUT, exist_ok=True)
W, MX = 1080, 90
B, I = "b", "i"


def canvas(h):
    bg = Image.new("RGB", (W, h), PAPER)
    b = ImageDraw.Draw(bg)
    for x in range(0, W, 36):
        b.line([x, 0, x, h], fill=LINE)
    for y in range(0, h, 36):
        b.line([0, y, W, y], fill=LINE)
    ly = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    return bg.convert("RGBA"), ly, ImageDraw.Draw(ly)


def save(bg, ly, name, logo_y):
    bg.alpha_composite(ly)
    bg.alpha_composite(reels.LOGO, (W - MX - 328, logo_y))
    bg.convert("RGB").save(os.path.join(OUT, name))


def head(d, y, topic, n, tot):
    f = F("MONO", 30)
    d.text((MX, y), "// ", font=f, fill=GREY)
    d.text((MX + f.getlength("// "), y), f"0{n}", font=F("MONOB", 30), fill=ORANGE)
    d.text((MX + f.getlength("// 0n "), y), f"· {topic}", font=f, fill=GREY)
    d.text((W - MX, y), f"{n}/{tot}", font=f, fill=GREY, anchor="ra")


def seg_w(segs, size):
    return sum((F("M800", size) if s == "b" else F("PFI", int(size * 1.08))).getlength(t) for t, s in segs)


def headline(d, y, lines, size=88):
    while max(seg_w(l, size) for l in lines) > W - 2 * MX:
        size -= 2
    for i, l in enumerate(lines):
        r.rich(d, MX, y + i * int(size * 1.2), l, size)
    return y + len(lines) * int(size * 1.2)


T = reels.T

# ---------------- CAROSELLO ----------------
N = 7


def slide(n, topic, draw):
    bg, ly, d = canvas(1350)
    head(d, 80, topic, n, N)
    draw(d)
    if n < N:
        d.text((MX, 1240), "scorri >>", font=F("MONOB", 28), fill=ORANGE)
    save(bg, ly, f"carosello_errori_budget_{n}.png", 1350 - 190)


ERR = ["Copi il 2026 e aggiungi una %", "Lo scrive solo l'amministrazione", "Niente budget di cassa",
       "Un solo scenario", "Lo chiudi in un cassetto"]


def c1(d):
    y = headline(d, 290, [[("5 errori che rendono", B)], [("il budget 2027", B)], [("inutile a ", B), ("marzo.", I)]])
    card(d, MX, y + 10, 900, 480, "budget 2027", "da evitare")
    for i in range(5):
        yy = y + 130 + i * 74
        d.rounded_rectangle([MX + 50, yy - 26, MX + 102, yy + 26], 10, outline=NAVY, width=5)
        d.text((MX + 130, yy), f"errore {i + 1}", font=F("MONO", 36), fill=NAVY, anchor="lm")
        pill(d, MX + 850, yy, "?", GREY, 22)


def err(num, lines, body):
    def f(d):
        d.text((MX, 470), num, font=F("PFI", 280), fill=ORANGE, anchor="ls")
        y = headline(d, 640, lines, 84)
        card(d, MX, y + 20, 900, 300, "come lo eviti", "metodo", NAVY)
        T(d, (MX + 50, y + 155), body[0], "M600", 40, GREY, maxw=800)
        T(d, (MX + 50, y + 235), body[1], "M800", 40, NAVY, maxw=800)
    return f


def c7(d):
    y = headline(d, 300, [[("L'AI ", B), ("prepara.", I)], [("Tu decidi.", B)]], 92)
    card(d, MX, y + 10, 900, 300, "dove entra l'AI", "budget 2027")
    for k, s in enumerate(["Raccoglie i dati del consuntivo.", "Scrive le ipotesi.", "Controlla la coerenza."]):
        yy = y + 135 + k * 62
        reels.tick(d, MX + 50, yy, True, 44, ORANGE if k == 0 else NAVY)
        T(d, (MX + 120, yy), s, "M600", 36, NAVY, maxw=740)
    y2 = y + 360
    r.rich(d, MX, y2 + 70, [("Commenta ", B), ("BUDGET.", I)], 80)
    d.rounded_rectangle([MX, y2 + 120, MX + 900, y2 + 220], 30, fill=ORANGE)
    T(d, (MX + 40, y2 + 170), "Ti mando la traccia dei cinque passi.", "M800", 40, WHITE, maxw=820)


slide(1, "budget 2027", c1)
slide(2, "errore 1", err("01", [[("Copi il 2026 e", B)], [("aggiungi una ", B), ("%.", I)]],
                         ["Ripeti gli errori dell'anno prima.", "Parti dai driver: volumi, prezzi, persone."]))
slide(3, "errore 2", err("02", [[("Lo scrive solo", B)], [("l'", B), ("amministrazione.", I)]],
                         ["Vendite e produzione sanno cosa cambia.", "Ogni ipotesi ha un nome e una data."]))
slide(4, "errore 3", err("03", [[("Niente budget", B)], [("di ", B), ("cassa.", I)]],
                         ["L'utile non è cassa.", "Conta quando incassi e quando paghi."]))
slide(5, "errore 4", err("04", [[("Un solo", B)], [("scenario.", I)]],
                         ["È una scommessa, non un piano.", "Prepara base, prudente e spinto."]))
slide(6, "errore 5", err("05", [[("Lo chiudi in un", B)], [("cassetto.", I)]],
                         ["Senza confronto, il budget invecchia.", "Budget contro consuntivo, ogni mese."]))
slide(7, "il prossimo passo", c7)


# ---------------- STORIE ----------------
def story(n, topic, lines, body):
    bg, ly, d = canvas(1920)
    head(d, 270, topic, n, 5)
    y = headline(d, 460, lines)
    body(d, y + 40)
    save(bg, ly, f"storia_{n}.png", 1920 - 390)


def rows_pill(d, y, items, w=350, step=125):
    for i, (s, sub, c) in enumerate(items):
        yy = y + 170 + i * step
        d.rounded_rectangle([MX + 50, yy - 46, MX + 50 + w, yy + 46], 22, fill=c)
        T(d, (MX + 50 + w // 2, yy), s, "M800", 40, WHITE, "mm", maxw=w - 30)
        T(d, (MX + 90 + w, yy), sub, "M600", 38, NAVY, maxw=800 - w - 40)


def st1(d, y):
    card(d, MX, y, 900, 600, "prima del budget", "budget 2027")
    rows_pill(d, y, (("consuntivo", "dati chiusi a ottobre", NAVY), ("stima", "novembre e dicembre", ORANGE),
                     ("base", "il punto di partenza 2027", NAVY)), w=330)
    T(d, (MX + 450, y + 535), "parti da un 2026 credibile", "MONO", 28, GREY, "mm")


def st2(d, y):
    card(d, MX, y, 900, 640, "margine per cliente", "illustrativo")
    for i, (s, w, c) in enumerate((("cliente A", 520, NAVY), ("cliente B", 400, NAVY), ("cliente C", 260, NAVY),
                                   ("cliente D", 90, ORANGE))):
        yy = y + 160 + i * 100
        T(d, (MX + 50, yy), s, "M800", 38, NAVY)
        d.rounded_rectangle([MX + 290, yy - 32, MX + 290 + w, yy + 32], 16, fill=c)
    T(d, (MX + 450, y + 560), "guardalo prima di fare il listino 2027", "MONO", 28, GREY, "mm")


def st3(d, y):
    card(d, MX, y, 900, 650, "5 errori del budget", "nuovo carosello")
    for i, s in enumerate(ERR):
        yy = y + 140 + i * 88
        reels.tick(d, MX + 50, yy, True, 48, ORANGE if i == 0 else NAVY)
        T(d, (MX + 125, yy), s, "M600", 36, NAVY, maxw=730)
    T(d, (MX + 450, y + 600), "oggi sul profilo: il carosello", "MONO", 28, GREY, "mm")


def st4(d, y):
    card(d, MX, y, 900, 600, "budget di cassa", "budget 2027")
    rows_pill(d, y, (("imposte", "segna i mesi in cui escono", ORANGE), ("tredicesime", "si pagano a dicembre", NAVY),
                     ("IVA", "segui le liquidazioni", NAVY)), w=330)
    T(d, (MX + 450, y + 535), "i mesi pesanti si vedono prima", "MONO", 28, GREY, "mm")


def st5(d, y):
    card(d, MX, y, 900, 620, "progetto Claude", "nuovo reel")
    for k, (nm, col) in enumerate((("consuntivo_2026.xlsx", NAVY), ("driver_2027.docx", ORANGE),
                                   ("istruzioni del progetto", NAVY))):
        yy = y + 120 + k * 120
        d.rounded_rectangle([MX + 40, yy, MX + 860, yy + 92], 20, fill=SOFT)
        d.rounded_rectangle([MX + 62, yy + 16, MX + 122, yy + 76], 10, fill=col)
        T(d, (MX + 150, yy + 46), nm, "M600", 36, NAVY, maxw=680)
    T(d, (MX + 450, y + 560), "oggi sul profilo: il reel sui progetti", "MONO", 28, GREY, "mm")


story(1, "budget 2027", [[("Prima del budget,", B)], [("chiudi bene", B)], [("il 2026.", I)]], st1)
story(2, "controllo di gestione", [[("Non tutti i clienti", B)], [("ti fanno ", B), ("guadagnare.", I)]], st2)
story(3, "budget 2027", [[("5 errori che", B)], [("rendono inutile", B)], [("il ", B), ("budget.", I)]], st3)
story(4, "budget 2027", [[("In cassa ci sono", B)], [("mesi ", B), ("pesanti.", I)]], st4)
story(5, "Claude in pratica", [[("Spieghi il budget", B)], [("a Claude ", B), ("una volta.", I)]], st5)

if len(sys.argv) > 1:
    for pref, names, size in (("st", [f"storia_{i}.png" for i in range(1, 6)], (432, 768)),
                              ("ca", [f"carosello_errori_budget_{i}.png" for i in range(1, N + 1)], (432, 540))):
        ims = [Image.open(os.path.join(OUT, n)).resize(size) for n in names]
        sh = Image.new("RGB", (size[0] * len(ims), size[1]), "white")
        for i, im in enumerate(ims):
            sh.paste(im, (size[0] * i, 0))
        sh.save(f"{sys.argv[1]}_{pref}.png")
