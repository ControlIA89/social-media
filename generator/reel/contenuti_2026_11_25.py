"""Carosello e storie del 25 nov 2026. Carosello: budget 2027 in tre scenari (4 passi).
Grafici illustrativi, senza valori.
Uso: python3 contenuti_2026_11_25.py [prefisso_fogli_di_controllo]"""
import os, sys
from PIL import Image
import render2 as r
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, card
import contenuti_2026_11_22_23 as c
from contenuti_2026_11_22_23 import (canvas, save, head, headline, story, rows_pill, rows_check,
                                     passo, T, tick, MEDIA, W, MX, B, I)

DAY = "2026-11-25"
N = 6
NAME = "carosello_tre_scenari"
PASSI = ["Scegli i driver che contano", "Scrivi lo scenario base",
         "Aggiungi prudente e ambizioso", "Decidi prima cosa fai"]


def slide(n, topic, draw):
    bg, ly, d = canvas(1350)
    head(d, 80, topic, n, N)
    draw(d)
    if n < N:
        d.text((MX, 1240), "scorri >>", font=F("MONOB", 28), fill=ORANGE)
    save(bg, ly, DAY, f"{NAME}_{n}.png", 1350 - 190)


def fan(d, x, y, w, h, labels=True):
    """Tre linee che partono dallo stesso punto: illustrativo, senza valori."""
    d.line([x, y + h, x + w - 190, y + h], fill=SOFT, width=4)
    x1 = x + w - 200
    start = (x, y + h * 0.62)
    for end, col, wd, lab in ((0.08, GREY, 6, "ambizioso"), (0.38, NAVY, 9, "base"), (0.80, ORANGE, 6, "prudente")):
        pts = [(start[0] + (x1 - x) * k / 20, start[1] + (y + h * end - start[1]) * (k / 20) ** 1.5) for k in range(21)]
        d.line(pts, fill=col, width=wd, joint="curve")
        ex, ey = pts[-1]
        d.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=col)
        if labels:
            T(d, (ex + 26, ey), lab, "MONOB", 26, col)
    d.ellipse([start[0] - 12, start[1] - 12, start[0] + 12, start[1] + 12], fill=NAVY)


def k1(d):
    y = headline(d, 290, [[("Budget 2027:", B)], [("tre scenari,", I)], [("non uno.", B)]], 96)
    card(d, MX, y + 10, 900, 440, "risultato 2027 · tre scenari", "illustrativo")
    fan(d, MX + 60, y + 120, 780, 230)
    T(d, (MX + 450, y + 405), "stessi driver, tre risultati", "MONO", 28, GREY, "mm")


def k6(d):
    y = headline(d, 300, [[("L'AI ", B), ("ricalcola.", I)], [("Tu decidi.", B)]], 92)
    card(d, MX, y + 10, 900, 300, "cosa chiedo all'AI", "scenari")
    for k, s in enumerate(["Ricalcola i tre scenari dai driver", "Mostrami dove la cassa non regge",
                           "Segnala le ipotesi incoerenti"]):
        yy = y + 135 + k * 62
        tick(d, MX + 50, yy, True, 44, ORANGE if k == 0 else NAVY)
        T(d, (MX + 120, yy), s, "M600", 34, NAVY, maxw=740)
    y2 = y + 360
    r.rich(d, MX, y2 + 70, [("Commenta ", B), ("BUDGET.", I)], 80)
    d.rounded_rectangle([MX, y2 + 120, MX + 900, y2 + 220], 30, fill=ORANGE)
    T(d, (MX + 40, y2 + 170), "Ti mando la guida sulla cassa a 13 settimane.", "M800", 38, WHITE, maxw=820)


# ---------------------------------------------------------------- storie
def s1(d, y):
    card(d, MX, y, 900, 560, "budget delle vendite", "budget 2027")
    rows_pill(d, y, (("clienti attivi", "quanto riconfermi", NAVY), ("clienti a rischio", "cosa puoi perdere", ORANGE),
                     ("clienti nuovi", "quanti, e da quando", NAVY)), w=390)
    T(d, (MX + 450, y + 510), "il totale viene dopo, non prima", "MONO", 28, GREY, "mm")


def s2(d, y):
    card(d, MX, y, 900, 540, "prima di usare un'analisi", "AI")
    rows_check(d, y, ["il totale torna con la contabilità", "le righe ci sono tutte", "i segni sono giusti"],
               step=110, size=36)
    T(d, (MX + 450, y + 485), "tre controlli, poi leggi il commento", "MONO", 28, GREY, "mm")


def s3(d, y):
    card(d, MX, y, 900, 560, "tre scenari", "oggi sul profilo")
    for i, s in enumerate(PASSI):
        yy = y + 140 + i * 90
        d.text((MX + 50, yy), f"0{i + 1}", font=F("MONOB", 32), fill=ORANGE, anchor="lm")
        T(d, (MX + 130, yy), s, "M600", 36, NAVY, maxw=720)
    T(d, (MX + 450, y + 510), "il carosello di oggi", "MONO", 28, GREY, "mm")


def s4(d, y):
    card(d, MX, y, 900, 560, "revisione in corso d'anno", "budget 2027")
    rows_pill(d, y, (("budget", "l'impegno di inizio anno", NAVY), ("forecast", "dove stai andando davvero", ORANGE)),
              w=300, step=140)
    T(d, (MX + 450, y + 480), "tienili tutti e due: il confronto serve", "MONO", 28, GREY, "mm")


def s5(d, y):
    card(d, MX, y, 900, 560, "crediti verso clienti", "tesoreria")
    rows_pill(d, y, (("prima", "promemoria della scadenza", NAVY), ("alla scadenza", "verifica dell'incasso", NAVY),
                     ("dopo", "sollecito, poi telefonata", ORANGE)), w=330)
    T(d, (MX + 450, y + 510), "guide gratuite: controlia.it/libreria", "MONO", 28, GREY, "mm")


if __name__ == "__main__":
    slide(1, "budget 2027", k1)
    slide(2, "passo 1", passo("01", [[("Scegli i driver", B)], [("che ", B), ("contano.", I)]],
                              ["Due o tre, non venti.", "Volumi, prezzi, tempi di incasso."]))
    slide(3, "passo 2", passo("02", [[("Scrivi lo", B)], [("scenario ", B), ("base.", I)]],
                              ["È quello su cui ti impegni.", "Ogni ipotesi con un nome e una data."]))
    slide(4, "passo 3", passo("03", [[("Aggiungi prudente", B)], [("e ", B), ("ambizioso.", I)]],
                              ["Cambi solo i driver, non il foglio.", "Stessa struttura, tre risultati."]))
    slide(5, "passo 4", passo("04", [[("Decidi prima", B)], [("cosa ", B), ("fai.", I)]],
                              ["Se va peggio: cosa rinvii, cosa tagli.", "Scrivi la soglia che fa scattare la scelta."]))
    slide(6, "il prossimo passo", k6)
    story(DAY, 1, "budget 2027", [[("Il budget vendite", B)], [("parte dai ", B), ("clienti.", I)]], s1)
    story(DAY, 2, "AI per la finanza", [[("Prima di fidarti,", B)], [("controlla i ", B), ("totali.", I)]], s2)
    story(DAY, 3, "budget 2027", [[("Tre scenari,", B)], [("non ", B), ("uno.", I)]], s3)
    story(DAY, 4, "budget 2027", [[("Il forecast non", B)], [("riscrive il ", B), ("budget.", I)]], s4)
    story(DAY, 5, "tesoreria e crediti", [[("Il sollecito parte", B)], [("prima della ", B), ("scadenza.", I)]], s5)

    if len(sys.argv) > 1:
        for pref, names in (("s", [f"storia_{i}.png" for i in range(1, 6)]),
                            ("c", [f"{NAME}_{i}.png" for i in range(1, N + 1)])):
            ims = [Image.open(os.path.join(MEDIA, DAY, n)) for n in names]
            ims = [im.resize((432, int(432 * im.height / im.width))) for im in ims]
            sh = Image.new("RGB", (432 * len(ims), max(i.height for i in ims)), "white")
            for i, im in enumerate(ims):
                sh.paste(im, (432 * i, 0))
            sh.save(f"{sys.argv[1]}_{pref}.png")
