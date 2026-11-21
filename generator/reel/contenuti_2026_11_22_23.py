"""Immagine singola e storie del 22 nov 2026; carosello e storie del 23 nov 2026.
Uso: python3 contenuti_2026_11_22_23.py [prefisso_fogli_di_controllo]"""
import os, sys
from PIL import Image, ImageDraw
import render2 as r
import reels
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, PAPER, LINE, card, pill

MEDIA = os.path.join(os.path.dirname(os.path.dirname(r.S)), "media")
W, MX = 1080, 90
B, I = "b", "i"
T = reels.T
tick = reels.tick


def canvas(h):
    bg = Image.new("RGB", (W, h), PAPER)
    b = ImageDraw.Draw(bg)
    for x in range(0, W, 36):
        b.line([x, 0, x, h], fill=LINE)
    for y in range(0, h, 36):
        b.line([0, y, W, y], fill=LINE)
    ly = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    return bg.convert("RGBA"), ly, ImageDraw.Draw(ly)


def save(bg, ly, day, name, logo_y):
    os.makedirs(os.path.join(MEDIA, day), exist_ok=True)
    bg.alpha_composite(ly)
    bg.alpha_composite(reels.LOGO, (W - MX - 328, logo_y))
    bg.convert("RGB").save(os.path.join(MEDIA, day, name))


def head(d, y, topic, n, tot):
    f = F("MONO", 30)
    d.text((MX, y), "// ", font=f, fill=GREY)
    d.text((MX + f.getlength("// "), y), f"0{n}", font=F("MONOB", 30), fill=ORANGE)
    d.text((MX + f.getlength("// 0n "), y), f"· {topic}", font=f, fill=GREY)
    if tot:
        d.text((W - MX, y), f"{n}/{tot}", font=f, fill=GREY, anchor="ra")


def seg_w(segs, size):
    return sum((F("M800", size) if s == "b" else F("PFI", int(size * 1.08))).getlength(t) for t, s in segs)


def headline(d, y, lines, size=88):
    while max(seg_w(l, size) for l in lines) > W - 2 * MX:
        size -= 2
    for i, l in enumerate(lines):
        r.rich(d, MX, y + i * int(size * 1.2), l, size)
    return y + len(lines) * int(size * 1.2)


def story(day, n, topic, lines, body):
    bg, ly, d = canvas(1920)
    head(d, 270, topic, n, 5)
    y = headline(d, 460, lines)
    body(d, y + 40)
    save(bg, ly, day, f"storia_{n}.png", 1920 - 390)


def rows_pill(d, y, items, w=350, step=125):
    for i, (s, sub, c) in enumerate(items):
        yy = y + 170 + i * step
        d.rounded_rectangle([MX + 50, yy - 46, MX + 50 + w, yy + 46], 22, fill=c)
        T(d, (MX + 50 + w // 2, yy), s, "M800", 40, WHITE, "mm", maxw=w - 30)
        T(d, (MX + 90 + w, yy), sub, "M600", 36, NAVY, maxw=800 - w - 40)


def rows_check(d, y, items, step=105, size=38, first=ORANGE):
    for i, s in enumerate(items):
        yy = y + 150 + i * step
        tick(d, MX + 50, yy, True, 50, first if i == 0 else NAVY)
        T(d, (MX + 130, yy), s, "M600", size, NAVY, maxw=730)


# =====================================================================
# 22 NOVEMBRE
# =====================================================================
D22 = "2026-11-22"
DOMANDE = ["Quanto vendo?", "A che prezzo?", "Quanto mi costa farlo?", "Quante persone servono?",
           "Quando incasso?", "E se va peggio?"]


def post22():
    bg, ly, d = canvas(1350)
    head(d, 80, "budget 2027", 1, 0)
    y = headline(d, 270, [[("Il budget 2027", B)], [("risponde a ", B), ("sei domande.", I)]])
    card(d, MX, y + 10, 900, 560, "budget 2027 · una pagina", "checklist")
    for i, s in enumerate(DOMANDE):
        yy = y + 135 + i * 80
        d.text((MX + 50, yy), f"0{i + 1}", font=F("MONOB", 34), fill=ORANGE, anchor="lm")
        T(d, (MX + 130, yy), s, "M800", 40, NAVY, maxw=700)
    T(d, (MX, y + 630), "Se manca una risposta, il budget non è pronto.", "M600", 36, GREY, maxw=880)
    save(bg, ly, D22, "immagine_sei_domande.png", 1350 - 190)


def s22_1(d, y):
    card(d, MX, y, 900, 600, "il budget completo", "budget 2027")
    rows_pill(d, y, (("conto economico", "se guadagni", NAVY), ("cassa", "se ce la fai a pagare", ORANGE),
                     ("patrimonio", "cosa resta in azienda", NAVY)), w=400)
    T(d, (MX + 450, y + 535), "il conto economico da solo non basta", "MONO", 28, GREY, "mm")


def s22_2(d, y):
    card(d, MX, y, 900, 520, "prima di caricare il file", "AI")
    rows_check(d, y, ["a cosa serve l'analisi", "da dove vengono i dati", "quali controlli fare"])
    T(d, (MX + 450, y + 470), "il contesto vale più del prompt", "MONO", 28, GREY, "mm")


def s22_3(d, y):
    card(d, MX, y, 900, 660, "sei domande", "oggi sul profilo")
    for i, s in enumerate(DOMANDE):
        yy = y + 135 + i * 76
        d.text((MX + 50, yy), f"0{i + 1}", font=F("MONOB", 32), fill=ORANGE, anchor="lm")
        T(d, (MX + 130, yy), s, "M600", 36, NAVY, maxw=700)
    T(d, (MX + 450, y + 615), "il post di oggi, in una pagina", "MONO", 28, GREY, "mm")


def s22_4(d, y):
    card(d, MX, y, 900, 560, "incassi", "budget di cassa")
    rows_pill(d, y, (("in fattura", "i termini concordati", NAVY), ("in banca", "quando arrivano davvero", ORANGE)),
              w=330, step=140)
    T(d, (MX + 450, y + 480), "nel budget di cassa usa la seconda", "MONO", 28, GREY, "mm")


def s22_5(d, y):
    card(d, MX, y, 900, 520, "chat", "nuovo reel")
    d.rounded_rectangle([MX + 40, y + 110, MX + 860, y + 250], 36, fill=SOFT)
    T(d, (MX + 76, y + 150), "Prepara il budget 2027 mese per mese,", "M600", 34, NAVY, maxw=760)
    T(d, (MX + 76, y + 206), "partendo dal consuntivo.", "M600", 34, NAVY, maxw=760)
    d.rounded_rectangle([MX + 40, y + 300, MX + 860, y + 392], 20, fill=SOFT)
    d.rounded_rectangle([MX + 62, y + 316, MX + 122, y + 376], 10, fill=ORANGE)
    T(d, (MX + 92, y + 346), "xls", "MONOB", 20, WHITE, "mm")
    T(d, (MX + 150, y + 346), "budget_2027.xlsx", "M600", 36, NAVY)
    T(d, (MX + 450, y + 465), "oggi sul profilo: il reel", "MONO", 28, GREY, "mm")


# =====================================================================
# 23 NOVEMBRE
# =====================================================================
D23 = "2026-11-23"
N = 6
PASSI = ["Parti dal saldo di inizio anno", "Porta i ricavi sui giorni di incasso",
         "Metti ogni uscita nel suo mese", "Cerca il punto più basso"]


def slide(n, topic, draw):
    bg, ly, d = canvas(1350)
    head(d, 80, topic, n, N)
    draw(d)
    if n < N:
        d.text((MX, 1240), "scorri >>", font=F("MONOB", 28), fill=ORANGE)
    save(bg, ly, D23, f"carosello_budget_cassa_{n}.png", 1350 - 190)


def curve(d, x, y, w, h, low_mark=True):
    pts = [0.55, 0.62, 0.48, 0.35, 0.28, 0.12, 0.22, 0.40, 0.52, 0.45, 0.60, 0.70]
    P = [(x + i * w / 11, y + h - p * h) for i, p in enumerate(pts)]
    d.line([x, y + h, x + w, y + h], fill=SOFT, width=4)
    d.line(P, fill=NAVY, width=8, joint="curve")
    if low_mark:
        lx, lyy = P[5]
        d.ellipse([lx - 16, lyy - 16, lx + 16, lyy + 16], fill=ORANGE)
        d.line([lx, lyy + 20, lx, y + h], fill=ORANGE, width=3)


def k1(d):
    y = headline(d, 290, [[("Budget di cassa", B)], [("in ", B), ("4 passi.", I)]], 96)
    card(d, MX, y + 10, 900, 520, "saldo di cassa per mese", "illustrativo")
    curve(d, MX + 60, y + 130, 780, 300)
    T(d, (MX + 450, y + 480), "il mese più basso è quello da guardare", "MONO", 28, GREY, "mm")


def passo(num, lines, body):
    def f(d):
        d.text((MX, 470), num, font=F("PFI", 280), fill=ORANGE, anchor="ls")
        y = headline(d, 640, lines, 80)
        card(d, MX, y + 20, 900, 300, "come lo faccio", "metodo", NAVY)
        T(d, (MX + 50, y + 155), body[0], "M600", 38, GREY, maxw=800)
        T(d, (MX + 50, y + 235), body[1], "M800", 38, NAVY, maxw=800)
    return f


def k6(d):
    y = headline(d, 300, [[("L'AI ", B), ("controlla.", I)], [("Tu decidi.", B)]], 92)
    card(d, MX, y + 10, 900, 300, "controlli con l'AI", "budget di cassa")
    for k, s in enumerate(["Ogni ricavo ha il suo incasso?", "Ogni investimento ha il suo pagamento?",
                           "Il saldo minimo regge?"]):
        yy = y + 135 + k * 62
        tick(d, MX + 50, yy, True, 44, ORANGE if k == 0 else NAVY)
        T(d, (MX + 120, yy), s, "M600", 34, NAVY, maxw=740)
    y2 = y + 360
    r.rich(d, MX, y2 + 70, [("Commenta ", B), ("BUDGET.", I)], 80)
    d.rounded_rectangle([MX, y2 + 120, MX + 900, y2 + 220], 30, fill=ORANGE)
    T(d, (MX + 40, y2 + 170), "Ti mando la guida sulla cassa a 13 settimane.", "M800", 38, WHITE, maxw=820)


def s23_1(d, y):
    card(d, MX, y, 900, 560, "saldo di cassa per mese", "illustrativo")
    curve(d, MX + 60, y + 120, 780, 300)
    T(d, (MX + 450, y + 490), "conta il punto più basso, non dicembre", "MONO", 28, GREY, "mm")


def s23_2(d, y):
    card(d, MX, y, 900, 560, "prima del budget", "controllo")
    rows_pill(d, y, (("piano dei conti", "uguale al consuntivo", NAVY), ("centri di costo", "gli stessi di oggi", NAVY),
                     ("confronto", "possibile ogni mese", ORANGE)), w=380)
    T(d, (MX + 450, y + 510), "se le voci cambiano, il confronto salta", "MONO", 28, GREY, "mm")


def s23_3(d, y):
    card(d, MX, y, 900, 560, "budget di cassa", "oggi sul profilo")
    for i, s in enumerate(PASSI):
        yy = y + 140 + i * 90
        d.text((MX + 50, yy), f"0{i + 1}", font=F("MONOB", 32), fill=ORANGE, anchor="lm")
        T(d, (MX + 130, yy), s, "M600", 36, NAVY, maxw=720)
    T(d, (MX + 450, y + 510), "il carosello di oggi", "MONO", 28, GREY, "mm")


def s23_4(d, y):
    card(d, MX, y, 900, 560, "incoerenze da cercare", "AI")
    rows_check(d, y, ["ricavi in crescita, personale fermo", "incassi più veloci dei termini",
                      "investimenti senza pagamento"], step=110, size=36)
    T(d, (MX + 450, y + 500), "chiedi all'AI di trovarle, poi decidi tu", "MONO", 28, GREY, "mm")


def s23_5(d, y):
    card(d, MX, y, 900, 560, "Excel + Claude", "nuovo reel")
    for i in range(6):
        for j in range(5):
            fill = ORANGE if (i, j) == (3, 3) else (SOFT if i == 0 or j == 0 else WHITE)
            d.rectangle([MX + 40 + j * 70, y + 110 + i * 60, MX + 107 + j * 70, y + 167 + i * 60], fill=fill,
                        outline=(214, 220, 230))
    d.rounded_rectangle([MX + 430, y + 100, MX + 860, y + 470], 20, fill=SOFT, outline=NAVY, width=3)
    T(d, (MX + 460, y + 140), "Claude", "MONOB", 26, ORANGE)
    T(d, (MX + 460, y + 200), "Perché il margine", "M600", 30, NAVY)
    T(d, (MX + 460, y + 245), "di marzo scende?", "M600", 30, NAVY)
    T(d, (MX + 450, y + 515), "oggi sul profilo: il reel", "MONO", 28, GREY, "mm")


if __name__ == "__main__":
    post22()
    story(D22, 1, "budget 2027", [[("Il budget sta", B)], [("in ", B), ("tre prospetti.", I)]], s22_1)
    story(D22, 2, "AI per la finanza", [[("All'AI dai il", B)], [("contesto,", I), (" non", B)], [("solo il file.", B)]], s22_2)
    story(D22, 3, "budget 2027", [[("Sei domande,", B)], [("una ", B), ("pagina.", I)]], s22_3)
    story(D22, 4, "tesoreria", [[("Nel budget conta", B)], [("quando ", B), ("incassi.", I)]], s22_4)
    story(D22, 5, "Claude in pratica", [[("Il foglio del budget,", B)], [("pronto in ", B), ("chat.", I)]], s22_5)

    slide(1, "budget 2027", k1)
    slide(2, "passo 1", passo("01", [[("Parti dal saldo", B)], [("di ", B), ("inizio anno.", I)]],
                              ["Non lo sai ancora: stimalo.", "Saldo di oggi più i movimenti fino a dicembre."]))
    slide(3, "passo 2", passo("02", [[("Porta i ricavi sui", B)], [("giorni di ", B), ("incasso.", I)]],
                              ["Una fattura di marzo può entrare a maggio.", "Usa i tempi reali, cliente per cliente."]))
    slide(4, "passo 3", passo("03", [[("Ogni uscita", B)], [("nel suo ", B), ("mese.", I)]],
                              ["Fornitori, stipendi, imposte, rate.", "Tredicesime e investimenti a parte."]))
    slide(5, "passo 4", passo("04", [[("Cerca il punto", B)], [("più ", B), ("basso.", I)]],
                              ["Il saldo di fine anno inganna.", "Il mese peggiore ti dice se serve fido."]))
    slide(6, "il prossimo passo", k6)
    story(D23, 1, "budget 2027", [[("Il saldo che conta", B)], [("è il più ", B), ("basso.", I)]], s23_1)
    story(D23, 2, "controllo di gestione", [[("Prima del budget,", B)], [("il ", B), ("piano dei conti.", I)]], s23_2)
    story(D23, 3, "budget 2027", [[("Budget di cassa", B)], [("in ", B), ("4 passi.", I)]], s23_3)
    story(D23, 4, "AI per la finanza", [[("Chiedi all'AI", B)], [("le ", B), ("incoerenze.", I)]], s23_4)
    story(D23, 5, "Claude in pratica", [[("Chiedi al tuo Excel", B)], [("perché il margine", B)], [("scende.", I)]], s23_5)

    if len(sys.argv) > 1:
        sets = (("22", D22, ["immagine_sei_domande.png"] + [f"storia_{i}.png" for i in range(1, 6)]),
                ("23s", D23, [f"storia_{i}.png" for i in range(1, 6)]),
                ("23c", D23, [f"carosello_budget_cassa_{i}.png" for i in range(1, N + 1)]))
        for pref, day, names in sets:
            ims = [Image.open(os.path.join(MEDIA, day, n)) for n in names]
            ims = [im.resize((432, int(432 * im.height / im.width))) for im in ims]
            sh = Image.new("RGB", (432 * len(ims), max(i.height for i in ims)), "white")
            for i, im in enumerate(ims):
                sh.paste(im, (432 * i, 0))
            sh.save(f"{sys.argv[1]}_{pref}.png")
