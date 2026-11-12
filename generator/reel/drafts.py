import os
from PIL import Image, ImageDraw
import render2 as r
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, PAPER, LINE, card, pill

OUT = "/home/claude/bozze"
os.makedirs(OUT, exist_ok=True)
W, MX = 1080, 90


def canvas(h):
    bg = Image.new("RGB", (W, h), PAPER)
    b = ImageDraw.Draw(bg)
    for x in range(0, W, 36):
        b.line([x, 0, x, h], fill=LINE)
    for y in range(0, h, 36):
        b.line([0, y, W, y], fill=LINE)
    ly = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    return bg.convert("RGBA"), ly, ImageDraw.Draw(ly)


def save(bg, ly, name):
    bg.alpha_composite(ly)
    import reels
    bg.alpha_composite(reels.LOGO, (W - MX - 328, bg.height - 390 if bg.height > 1400 else bg.height - 190))
    bg.convert("RGB").save(os.path.join(OUT, name), quality=95)


def header(d, y, topic, n, tot):
    f = F("MONO", 30)
    d.text((MX, y), "// ", font=f, fill=GREY)
    d.text((MX + f.getlength("// "), y), f"0{n}", font=F("MONOB", 30), fill=ORANGE)
    d.text((MX + f.getlength("// 0n "), y), f"· {topic}", font=f, fill=GREY)
    d.text((W - MX, y), f"{n}/{tot}", font=f, fill=GREY, anchor="ra")


def seg_w(segs, size):
    return sum((F("M800", size) if s == "b" else F("PFI", int(size * 1.08))).getlength(t) for t, s in segs)


def headline(d, y, lines, size=88, center=False):
    while max(seg_w(l, size) for l in lines) > W - 2 * MX:
        size -= 2
    for i, l in enumerate(lines):
        r.rich(d, MX, y + i * int(size * 1.2), l, size, center)
    return y + len(lines) * int(size * 1.2)


def footer(d, y):
    pass


B, I = "b", "i"

# ---------------- STORIE 1080x1920 ----------------
def story(n, topic, lines, body):
    bg, ly, d = canvas(1920)
    header(d, 270, topic, n, 5)
    y = headline(d, 460, lines)
    body(d, y + 40)
    footer(d, 1560)
    save(bg, ly, f"storia_{n}.png")


def st1(d, y):
    card(d, MX, y, 900, 430, "sondaggio", "rispondi")
    d.rounded_rectangle([MX + 50, y + 120, MX + 850, y + 240], 60, fill=ORANGE)
    d.text((W // 2, y + 180), "Troppo", font=F("M800", 50), fill=WHITE, anchor="mm")
    d.rounded_rectangle([MX + 50, y + 270, MX + 850, y + 390], 60, outline=NAVY, width=5)
    d.text((W // 2, y + 330), "Il giusto", font=F("M800", 50), fill=NAVY, anchor="mm")


def st2(d, y):
    card(d, MX, y, 900, 500, "conto economico", "per cliente")
    for i, (lab, wd, c) in enumerate((("Ricavi", 560, NAVY), ("Costi diretti", 400, GREY), ("Margine", 160, ORANGE))):
        yy = y + 150 + i * 120
        d.text((MX + 50, yy), lab, font=F("M800", 38), fill=NAVY, anchor="lm")
        d.rounded_rectangle([MX + 50, yy + 34, MX + 50 + wd, yy + 62], 14, fill=c)


def st3(d, y):
    card(d, MX, y, 900, 480, "prompt", "Claude")
    for i, s in enumerate(["Ecco lo scadenziario clienti.", "Ordina per giorni di ritardo",
                           "e scrivi un sollecito per ciascuno,", "in tre toni: gentile, fermo,", "ultimo avviso."]):
        d.text((MX + 50, y + 130 + i * 62), s, font=F("MONO", 36), fill=NAVY)


def st4(d, y):
    card(d, MX, y, 900, 500, "lunedì mattina", "cash flow")
    for i, s in enumerate(["Cosa incasso questa settimana?", "Cosa esce, e quando?", "Dove si apre un buco?"]):
        yy = y + 160 + i * 120
        d.rounded_rectangle([MX + 50, yy - 40, MX + 130, yy + 40], 18, fill=ORANGE)
        d.text((MX + 90, yy), str(i + 1), font=F("M900", 44), fill=WHITE, anchor="mm")
        d.text((MX + 160, yy), s, font=F("M600", 40), fill=NAVY, anchor="lm")


def st5(d, y):
    card(d, MX, y, 900, 560, "AI 4 Finance", "nuovo")
    d.text((MX + 60, y + 100), "AI 4", font=F("M900", 150), fill=NAVY)
    d.text((MX + 60, y + 420), "Finance", font=F("PFI", 170), fill=ORANGE, anchor="ls")
    d.text((MX + 60, y + 490), "tesoreria · crediti · reporting · governance", font=F("MONO", 28), fill=GREY, anchor="lm")


story(1, "domanda del giorno", [[("Quanto tempo passa", B)], [("il tuo ufficio a", B)], [("rincorrere", I), (" i dati?", B)]], st1)
story(2, "controllo di gestione", [[("Il margine non", B)], [("si legge dal", B)], [("fatturato.", I)]], st2)
story(3, "Claude in pratica", [[("Un prompt per il tuo", B)], [("scadenziario.", I)]], st3)
story(4, "AI per la finanza", [[("3 domande da fare", B)], [("all'", B), ("AI", I), (" ogni lunedì.", B)]], st4)
story(5, "novità", [[("Vuoi capire da dove", B)], [("partire? Scrivimi", B)], [("FINANCE", I), (" in DM.", B)]], st5)

# ---------------- CAROSELLO 1080x1350 ----------------
def slide(n, topic, draw):
    bg, ly, d = canvas(1350)
    header(d, 80, topic, n, 5)
    draw(d)
    footer(d, 1240)
    if n < 5:
        d.text((MX, 1240), "scorri >>", font=F("MONOB", 28), fill=ORANGE)
    save(bg, ly, f"post_slide_{n}.png")


def c1(d):
    y = headline(d, 300, [[("3 segnali che il tuo", B)], [("controllo di gestione", B)], [("è ", B), ("in ritardo.", I)]])
    card(d, MX, y + 20, 900, 430, "diagnosi", "3 segnali")
    for i in range(3):
        yy = y + 160 + i * 100
        d.rounded_rectangle([MX + 50, yy - 26, MX + 102, yy + 26], 10, outline=NAVY, width=5)
        d.text((MX + 130, yy), f"segnale {i + 1}", font=F("MONO", 36), fill=NAVY, anchor="lm")
        pill(d, MX + 850, yy, "da verificare", GREY, 22)


def sig(num, lines, body):
    def f(d):
        d.text((MX, 470), num, font=F("PFI", 280), fill=ORANGE, anchor="ls")
        y = headline(d, 640, lines, 84)
        for i, s in enumerate(body):
            d.text((MX, y + 10 + i * 58), s, font=F("M600", 42), fill=GREY)
    return f


def c5(d):
    y = headline(d, 330, [[("Ti riconosci?", B)], [("Scrivimi ", B), ("CONTROLLO", I)], [("in DM.", B)]], 92)
    card(d, MX, y + 20, 900, 300, "DM", "Emanuele", NAVY)
    d.rounded_rectangle([MX + 40, y + 130, MX + 820, y + 280], 36, fill=ORANGE)
    d.text((MX + 80, y + 180), "Guardiamo insieme da dove", font=F("M800", 40), fill=WHITE, anchor="lm")
    d.text((MX + 80, y + 236), "conviene partire.", font=F("M800", 40), fill=WHITE, anchor="lm")


slide(1, "controllo di gestione", c1)
slide(2, "segnale 1", sig("01", [[("Chiudi il mese", B)], [("dopo il ", B), ("20.", I)]],
                         ["Quando i numeri arrivano,", "le decisioni sono già prese."]))
slide(3, "segnale 2", sig("02", [[("Il margine per cliente", B)], [("lo scopri a ", B), ("fine anno.", I)]],
                         ["Sai quanto fatturi.", "Non sai chi ti fa guadagnare."]))
slide(4, "segnale 3", sig("03", [[("Il cash flow lo sa", B)], [("leggere ", B), ("una persona.", I)]],
                         ["Se manca lei, nessuno sa", "cosa succede in cassa."]))
slide(5, "il prossimo passo", c5)

# contact sheets
def sheet(names, th, out):
    ims = [Image.open(os.path.join(OUT, n)) for n in names]
    tw = 432
    s = Image.new("RGB", (tw * len(ims), th), "white")
    for i, im in enumerate(ims):
        s.paste(im.resize((tw, th)), (tw * i, 0))
    s.save(out)


sheet([f"storia_{i}.png" for i in range(1, 6)], 768, os.path.join(r.S, "sh_st.png"))
sheet([f"post_slide_{i}.png" for i in range(1, 6)], 540, os.path.join(r.S, "sh_po.png"))
