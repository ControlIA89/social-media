"""Carosello e storie del 27 nov 2026. Carosello: budget dei costi 2027 in 4 passi.
Grafici illustrativi, senza valori.
Uso: python3 contenuti_2026_11_27.py [prefisso_fogli_di_controllo]"""
import os, sys
from PIL import Image
import render2 as r
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, card
from contenuti_2026_11_22_23 import (canvas, save, head, headline, story, rows_pill, rows_check,
                                     passo, T, tick, MEDIA, W, MX, B, I)

DAY = "2026-11-27"
N = 6
NAME = "carosello_budget_costi"
PASSI = ["Separa fissi e variabili", "Lega i variabili alle vendite",
         "Rivedi i fissi, uno per uno", "Dai a ogni voce un responsabile"]


def slide(n, topic, draw):
    bg, ly, d = canvas(1350)
    head(d, 80, topic, n, N)
    draw(d)
    if n < N:
        d.text((MX, 1240), "scorri >>", font=F("MONOB", 28), fill=ORANGE)
    save(bg, ly, DAY, f"{NAME}_{n}.png", 1350 - 190)


def k1(d):
    y = headline(d, 290, [[("Budget dei costi:", B)], [("non copiare", I)], [("il 2026.", B)]], 96)
    card(d, MX, y + 10, 900, 440, "costi 2027 · tre famiglie", "illustrativo")
    x0, yb, bw = MX + 90, y + 345, 150
    d.line([MX + 60, yb, MX + 840, yb], fill=SOFT, width=4)
    for i, (h, col, lab) in enumerate(((135, NAVY, "fissi"), (175, ORANGE, "variabili"), (100, GREY, "personale"))):
        x = x0 + i * 255
        d.rounded_rectangle([x, yb - h, x + bw, yb], 14, fill=col)
        T(d, (x + bw // 2, yb + 38), lab, "MONOB", 26, col, "mm")
    T(d, (MX + 450, y + 120), "ogni famiglia si costruisce in modo diverso", "MONO", 26, GREY, "mm")


def k6(d):
    y = headline(d, 300, [[("L'AI ", B), ("raccoglie.", I)], [("Tu decidi.", B)]], 92)
    card(d, MX, y + 10, 900, 300, "cosa chiedo all'AI", "budget dei costi")
    for k, s in enumerate(["Raggruppa i costi 2026 per famiglia", "Elenca contratti e scadenze",
                           "Segnala le voci senza responsabile"]):
        yy = y + 135 + k * 62
        tick(d, MX + 50, yy, True, 44, ORANGE if k == 0 else NAVY)
        T(d, (MX + 120, yy), s, "M600", 34, NAVY, maxw=740)
    y2 = y + 360
    r.rich(d, MX, y2 + 70, [("Commenta ", B), ("BUDGET.", I)], 80)
    d.rounded_rectangle([MX, y2 + 120, MX + 900, y2 + 220], 30, fill=ORANGE)
    T(d, (MX + 40, y2 + 170), "Ti mando la guida gratuita da cui partire.", "M800", 38, WHITE, maxw=820)


# ---------------------------------------------------------------- storie
def s1(d, y):
    card(d, MX, y, 900, 540, "prima di chiudere il budget", "budget 2027")
    rows_check(d, y, ["chiedi i listini 2027 ai fornitori", "controlla i contratti che si rinnovano",
                      "segna da che mese parte l'aumento"], step=110, size=36)
    T(d, (MX + 450, y + 485), "un aumento scoperto a marzo è già costo", "MONO", 28, GREY, "mm")


def s2(d, y):
    card(d, MX, y, 900, 560, "costi indiretti", "controllo di gestione")
    rows_pill(d, y, (("scegli", "un criterio che si spiega", NAVY), ("scrivi", "come lo calcoli", NAVY),
                     ("tieni", "lo stesso tutto l'anno", ORANGE)), w=260)
    T(d, (MX + 450, y + 510), "se cambi criterio, cambi il margine", "MONO", 28, GREY, "mm")


def s3(d, y):
    card(d, MX, y, 900, 560, "budget dei costi", "oggi sul profilo")
    for i, s in enumerate(PASSI):
        yy = y + 140 + i * 90
        d.text((MX + 50, yy), f"0{i + 1}", font=F("MONOB", 32), fill=ORANGE, anchor="lm")
        T(d, (MX + 130, yy), s, "M600", 36, NAVY, maxw=720)
    T(d, (MX + 450, y + 510), "il carosello di oggi", "MONO", 28, GREY, "mm")


def s4(d, y):
    card(d, MX, y, 900, 560, "centri di costo", "controllo di gestione")
    rows_pill(d, y, (("chi", "un nome per ogni centro", NAVY), ("cosa", "i costi che può governare", NAVY),
                     ("quando", "il confronto, ogni mese", ORANGE)), w=260)
    T(d, (MX + 450, y + 510), "un costo senza nome non lo guarda nessuno", "MONO", 28, GREY, "mm")


def s5(d, y):
    card(d, MX, y, 900, 540, "prima di usare l'AI sui numeri", "AI")
    rows_check(d, y, ["anagrafiche senza doppioni", "piano dei conti stabile", "mesi chiusi a data fissa"],
               step=110, size=36)
    T(d, (MX + 450, y + 485), "guide gratuite: controlia.it/libreria", "MONO", 28, GREY, "mm")


if __name__ == "__main__":
    slide(1, "budget 2027", k1)
    slide(2, "passo 1", passo("01", [[("Separa fissi", B)], [("e ", B), ("variabili.", I)]],
                              ["Si muovono in modo diverso.", "Un solo aumento su tutto non regge."]))
    slide(3, "passo 2", passo("02", [[("Lega i variabili", B)], [("alle ", B), ("vendite.", I)]],
                              ["Seguono volumi e mix del budget vendite.", "Se cambiano le vendite, cambiano loro."]))
    slide(4, "passo 3", passo("03", [[("Rivedi i fissi,", B)], [("uno ", B), ("per uno.", I)]],
                              ["Affitti, canoni, utenze, consulenze.", "Per ogni contratto: scadenza e aumenti."]))
    slide(5, "passo 4", passo("04", [[("Ogni voce ha un", B)], [("responsabile.", I)]],
                              ["Un nome per ogni voce che pesa.", "È chi spiega lo scostamento, ogni mese."]))
    slide(6, "il prossimo passo", k6)
    story(DAY, 1, "budget 2027", [[("Gli aumenti si", B)], [("chiedono ", B), ("adesso.", I)]], s1)
    story(DAY, 2, "controllo di gestione", [[("Costi indiretti:", B)], [("un criterio, ", B), ("sempre.", I)]], s2)
    story(DAY, 3, "budget 2027", [[("Budget dei costi", B)], [("in ", B), ("4 passi.", I)]], s3)
    story(DAY, 4, "controllo di gestione", [[("Un centro di costo,", B)], [("un ", B), ("responsabile.", I)]], s4)
    story(DAY, 5, "AI per la finanza", [[("Prima dell'AI,", B)], [("i dati ", B), ("in ordine.", I)]], s5)

    if len(sys.argv) > 1:
        for pref, names in (("s", [f"storia_{i}.png" for i in range(1, 6)]),
                            ("c", [f"{NAME}_{i}.png" for i in range(1, N + 1)])):
            ims = [Image.open(os.path.join(MEDIA, DAY, n)) for n in names]
            ims = [im.resize((540, int(540 * im.height / im.width))) for im in ims]
            sh = Image.new("RGB", (540 * 3, max(i.height for i in ims) * ((len(ims) + 2) // 3)), "white")
            for i, im in enumerate(ims):
                sh.paste(im, (540 * (i % 3), (i // 3) * im.height))
            sh.save(f"{sys.argv[1]}_{pref}.png")
