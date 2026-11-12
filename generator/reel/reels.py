import sys, os, math, subprocess
from PIL import Image, ImageDraw
import render2 as r
from render2 import F, NAVY, ORANGE, WHITE, GREY, SOFT, card, pill, pr, ease, Frame

S = r.S
W, H, FPS, MX = 1080, 1920, 30, 90
B, I = "b", "i"

# ---------- logo sticker (bottom right) ----------
_lg = Image.open(os.path.join(os.path.dirname(S), "logo.png")).convert("RGBA")
_lg = _lg.resize((280, int(280 * _lg.height / _lg.width)), Image.LANCZOS)
LOGO = Image.new("RGBA", (340, 150), (0, 0, 0, 0))
_d = ImageDraw.Draw(LOGO)
_d.rounded_rectangle([8, 10, 338, 148], 22, fill=(0, 43, 92, 46))
_d.rounded_rectangle([0, 0, 328, 138], 22, fill=WHITE, outline=NAVY, width=4)
LOGO.alpha_composite(_lg, (24, (138 - _lg.height) // 2))


def put_logo(img, y=1530):
    img.alpha_composite(LOGO, (W - MX - 328, y))


# ---------- helpers ----------
def back(x):
    x = max(0.0, min(1.0, x))
    c = 1.70158
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def seg_w(segs, size):
    return sum((F("M800", size) if s == "b" else F("PFI", int(size * 1.08))).getlength(t) for t, s in segs)


def Hd(fr, t, lines, y0=400, size=84, t0=0.05, center=False):
    while max(seg_w(l, size) for l in lines) > W - 2 * MX:
        size -= 2
    step = int(size * 1.2)
    for i, l in enumerate(lines):
        fr.layer(lambda d, l=l, i=i: r.rich(d, MX, y0 + i * step, l, size, center), pr(t, t0 + i * 0.15))
    return y0 + (len(lines) - 1) * step


def header(fr, topic, n, tot):
    def dr(d):
        f = F("MONO", 30)
        d.text((MX, 215), "// ", font=f, fill=GREY)
        d.text((MX + f.getlength("// "), 215), f"0{n}", font=F("MONOB", 30), fill=ORANGE)
        d.text((MX + f.getlength("// 0n "), 215), f"· {topic}", font=f, fill=GREY)
        d.text((W - MX, 215), f"{n}/{tot}", font=f, fill=GREY, anchor="ra")
    fr.layer(dr)


def T(d, xy, s, fname, size, fill, anchor="lm", maxw=None):
    f = F(fname, size)
    while maxw and f.getlength(s) > maxw:
        size -= 1
        f = F(fname, size)
    d.text(xy, s, font=f, fill=fill, anchor=anchor)


def pillL(d, x, cy, s, color=ORANGE, size=24):
    f = F("MONOB", size)
    w = f.getlength(s) + 32
    d.rounded_rectangle([x, cy - 22, x + w, cy + 22], 22, fill=color)
    d.text((x + w / 2, cy), s, font=f, fill=WHITE, anchor="mm")
    return w


def tick(d, x, cy, on, s=52, color=ORANGE):
    if on:
        d.rounded_rectangle([x, cy - s / 2, x + s, cy + s / 2], 10, fill=color)
        d.line([x + s * .22, cy, x + s * .42, cy + s * .22, x + s * .78, cy - s * .22], fill=WHITE, width=7)
    else:
        d.rounded_rectangle([x, cy - s / 2, x + s, cy + s / 2], 10, outline=NAVY, width=5)


def typed(s, t, t0, cps=22):
    return s[: max(0, int((t - t0) * cps))]


def stamp(fr, cx, cy, s, p, ang=8):
    if p <= 0:
        return
    f = F("M900", 92)
    w, h = int(f.getlength(s)) + 90, 170
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([6, 6, w - 6, h - 6], 24, fill=(245, 242, 234, 235), outline=ORANGE, width=12)
    d.text((w / 2, h / 2), s, font=f, fill=ORANGE, anchor="mm")
    sc = 1 + (1 - p) * 0.9
    im = im.resize((int(w * sc), int(h * sc)), Image.LANCZOS).rotate(ang, expand=True, resample=Image.BICUBIC)
    if p < 1:
        im.putalpha(im.getchannel("A").point(lambda v: int(v * p)))
    ly = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ly.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
    fr.img.alpha_composite(ly)


def cta(topic, n, tot, word, msg, lead="Commenta"):
    def sc(fr, t):
        header(fr, topic, n, tot)
        fr.layer(lambda d: r.rich(d, 0, 430, [(lead, B)], 120, True), pr(t, 0.05))
        fr.layer(lambda d: r.rich(d, 0, 590, [(word, I)], 150, True), pr(t, 0.25))

        def a(d):
            card(d, MX, 700, 900, 250, "commenti")
            d.ellipse([MX + 40, 800, MX + 130, 890], fill=SOFT, outline=NAVY, width=4)
            d.rounded_rectangle([MX + 160, 800, MX + 860, 890], 45, outline=NAVY, width=4)
            wd = typed(word, t, 1.0, 11)
            f = F("M800", 46)
            d.text((MX + 200, 845), wd, font=f, fill=NAVY, anchor="lm")
            if int(t * 3) % 2 == 0:
                cx = MX + 204 + f.getlength(wd)
                d.rectangle([cx, 822, cx + 5, 868], fill=ORANGE)
        fr.layer(a, pr(t, 0.6), rise=70)

        def b(d):
            card(d, MX, 1000, 900, 330, "DM", "risposta", NAVY)
            d.rounded_rectangle([MX + 40, 1110, MX + 840, 1290], 36, fill=ORANGE)
            for i, s in enumerate(msg):
                T(d, (MX + 80, 1166 + i * 66), s, "M800", 40, WHITE, maxw=720)
        fr.layer(b, pr(t, 1.9), rise=70)
    return sc


def mini(d, i, x, y, q, w=358):
    """small illustrative visuals, no real data"""
    if i == 0:
        for k, (lab, c) in enumerate((("sollecito", ORANGE), ("incassato", NAVY), ("sollecito", ORANGE))):
            yy = y + 22 + k * 56
            d.rounded_rectangle([x, yy - 9, x + 150, yy + 9], 9, fill=SOFT)
            if q > k / 3:
                pill(d, x + w, yy, lab, c, 20)
    elif i == 1:
        pts = [(0, 140), (60, 110), (120, 125), (180, 70), (240, 85), (300, 35), (358, 15)]
        n = max(2, int(1 + q * (len(pts) - 1)))
        d.line([(x + a, y + b) for a, b in pts[:n]], fill=ORANGE, width=9, joint="curve")
        d.line([x, y + 160, x + w, y + 160], fill=SOFT, width=4)
    elif i == 2:
        for k, (wd, c) in enumerate(((300, NAVY), (220, GREY), (260, NAVY), (120, ORANGE))):
            d.rounded_rectangle([x, y + k * 42, x + wd * q, y + 26 + k * 42], 10, fill=c)
    else:
        for k, (h1, h2) in enumerate(((90, 70), (120, 130), (100, 150))):
            bx = x + 20 + k * 115
            d.rounded_rectangle([bx, y + 160 - h1 * q, bx + 40, y + 160], 8, fill=NAVY)
            d.rounded_rectangle([bx + 46, y + 160 - h2 * q, bx + 86, y + 160], 8, fill=ORANGE)


# =====================================================================
# REEL A - Claude for Finance
# =====================================================================
TA = "Claude for Finance"


def a1(fr, t):
    header(fr, TA, 1, 5)
    Hd(fr, t, [[("Claude for Finance", B)], [("non è una ", B), ("chat.", I)]])

    def c(d):
        card(d, MX, 760, 900, 330, "chat", "ieri")
        d.rounded_rectangle([MX + 40, 870, MX + 760, 970], 40, fill=SOFT)
        T(d, (MX + 80, 920), typed("Riassumimi questo bilancio", t, 0.9), "M600", 40, NAVY)
        d.rounded_rectangle([MX + 140, 1000, MX + 860, 1060], 30, fill=SOFT)
    fr.layer(c, pr(t, 0.6), rise=70)
    stamp(fr, 690, 1090, "NON SOLO", pr(t, 2.2, 0.25))
    fr.layer(lambda d: T(d, (W // 2, 1290), "è un banco di lavoro per chi fa numeri", "MONO", 32, GREY, "mm"),
             pr(t, 2.7), rise=30)


def a2(fr, t):
    header(fr, TA, 2, 5)
    Hd(fr, t, [[("Dentro ci sono", B)], [("tre ", B), ("pezzi.", I)]])
    rows = [("Excel", "Claude dentro Excel", None, "legge, modifica e spiega il foglio"),
            ("connettori", "Dati di mercato collegati", ["S&P Capital IQ", "Morningstar", "PitchBook", "Moody's"], None),
            ("skill", "Skill già pronte", ["DCF", "comparabili", "due diligence", "earnings"], None)]
    for i, (ttl, main, pills, sub) in enumerate(rows):
        st, y = 0.7 + i * 1.3, 640 + i * 270

        def dr(d, i=i, ttl=ttl, main=main, pills=pills, sub=sub, st=st, y=y):
            card(d, MX, y, 900, 240, ttl, f"0{i+1}")
            T(d, (MX + 40, y + 122), main, "M800", 42, NAVY)
            if sub:
                T(d, (MX + 40, y + 188), sub, "M600", 30, GREY)
                k = int(t * 5) % 12
                for c_ in range(12):
                    gx, gy = MX + 660 + (c_ % 4) * 52, y + 96 + (c_ // 4) * 40
                    d.rectangle([gx, gy, gx + 46, gy + 34], fill=ORANGE if c_ == k else SOFT)
            else:
                x = MX + 40
                for k, s in enumerate(pills):
                    if pr(t, st + 0.35 + k * 0.18, 0.15) > 0:
                        x += pillL(d, x, y + 188, s, NAVY if k % 2 else ORANGE, 22) + 12
        fr.layer(dr, pr(t, st), rise=70)


def a3(fr, t):
    header(fr, TA, 3, 5)
    Hd(fr, t, [[("È nato per banche", B)], [("e fondi. E la ", B), ("PMI?", I)]])
    cols = [("banche", "coperto", NAVY, ["DCF", "comparabili", "due diligence"], True),
            ("PMI", "da costruire", ORANGE, ["scadenziario", "cassa", "margini"], False)]
    for i, (ttl, tg, tc, labs, on) in enumerate(cols):
        x = MX + i * 470

        def dr(d, x=x, ttl=ttl, tg=tg, tc=tc, labs=labs, on=on, i=i):
            card(d, x, 700, 430, 460, ttl, tg, tc)
            for k, s in enumerate(labs):
                yy = 840 + k * 105
                tick(d, x + 36, yy, on and pr(t, 1.0 + k * 0.25, 0.1) > 0, color=NAVY)
                T(d, (x + 110, yy), s, "M600", 36, NAVY, maxw=290)
        fr.layer(dr, pr(t, 0.6 + i * 0.5), rise=70)
    fr.layer(lambda d: T(d, (W // 2, 1250), "Le skill pronte non parlano", "M800", 44, NAVY, "mm"), pr(t, 2.2), rise=30)
    fr.layer(lambda d: T(d, (W // 2, 1312), "la lingua della tua azienda.", "M800", 44, NAVY, "mm"), pr(t, 2.35), rise=30)


def a4(fr, t):
    header(fr, TA, 4, 5)
    Hd(fr, t, [[("Stessa logica,", B)], [("sui ", B), ("tuoi", I), (" processi.", B)]])
    names = ["Scadenziario e solleciti", "Previsione di cassa", "Bilancio riclassificato", "Budget vs consuntivo"]
    for i, nm in enumerate(names):
        x, y, st = MX + (i % 2) * 470, 680 + (i // 2) * 400, 0.7 + i * 0.7

        def dr(d, i=i, x=x, y=y, st=st, nm=nm):
            card(d, x, y, 430, 370, "skill", f"0{i+1}")
            mini(d, i, x + 36, y + 105, pr(t, st + 0.25, 0.7))
            T(d, (x + 36, y + 320), nm, "M800", 30, NAVY, maxw=358)
        fr.layer(dr, pr(t, st), rise=70)


REEL_A = [(a1, 3.8), (a2, 5.6), (a3, 4.0), (a4, 4.8),
          (cta(TA, 5, 5, "SKILL", ["Ti scrivo quali skill servono", "alla tua azienda."]), 4.2)]

# =====================================================================
# REEL B - Cos'e' una skill
# =====================================================================
TB = "skill di Claude"


def b1(fr, t):
    header(fr, TB, 1, 5)
    Hd(fr, t, [[("Riscrivi ogni volta", B)], [("lo stesso ", B), ("prompt?", I)]])

    def c(d):
        card(d, MX, 720, 900, 470, "prompt", "3 volte")
        for i, day in enumerate(("lunedì", "martedì", "mercoledì")):
            yy, st = 860 + i * 110, 0.8 + i * 0.6
            if t < st:
                continue
            w = pillL(d, MX + 40, yy, day, NAVY, 24)
            T(d, (MX + 60 + w, yy), typed("Riclassifica il bilancio così...", t, st, 40), "MONO", 32, NAVY)
    fr.layer(c, pr(t, 0.5), rise=70)
    stamp(fr, 690, 1200, "ANCORA?", pr(t, 2.7, 0.25), -7)


def b2(fr, t):
    header(fr, TB, 2, 5)
    Hd(fr, t, [[("Una skill è una", B)], [("procedura", I), (" scritta", B)], [("una volta.", B)]])

    def c(d):
        card(d, MX, 770, 900, 520, "cartella skill", "1 volta")
        for i, (nm, ds) in enumerate((("SKILL.md", "istruzioni"), ("modello.xlsx", "formato"), ("controlli.py", "verifiche"))):
            q = pr(t, 1.0 + i * 0.6, 0.3)
            if q <= 0:
                continue
            yy = 920 + i * 125
            x = MX + 50 + (1 - q) * 60
            d.rounded_rectangle([x, yy - 44, x + 66, yy + 44], 10, fill=WHITE, outline=NAVY, width=5)
            d.polygon([(x + 40, yy - 44), (x + 66, yy - 18), (x + 40, yy - 18)], fill=ORANGE)
            T(d, (x + 96, yy), nm, "MONOB", 42, NAVY)
            pill(d, MX + 860, yy, ds, ORANGE if i == 0 else GREY, 24)
    fr.layer(c, pr(t, 0.7), rise=70)


def b3(fr, t):
    header(fr, TB, 3, 5)
    Hd(fr, t, [[("Dentro ci metti", B)], [("il tuo ", B), ("metodo.", I)]])
    labs = ["Quali dati raccogliere", "Come si calcola", "Quali quadrature fare", "Come consegnare"]
    done = sum(1 for i in range(4) if t > 1.1 + i * 0.7)

    def c(d):
        card(d, MX, 700, 900, 650, "SKILL.md", f"{done}/4")
        for i, s in enumerate(labs):
            yy = 850 + i * 125
            tick(d, MX + 50, yy, i < done, 60)
            T(d, (MX + 140, yy), s, "M600", 44, NAVY)
        d.rounded_rectangle([MX + 50, 1290, MX + 850, 1310], 10, fill=SOFT)
        if done:
            d.rounded_rectangle([MX + 50, 1290, MX + 50 + 200 * done, 1310], 10, fill=ORANGE)
    fr.layer(c, pr(t, 0.6), rise=70)


def b4(fr, t):
    header(fr, TB, 4, 5)
    Hd(fr, t, [[("Stesso lavoro,", B)], [("stesso ", B), ("standard.", I)]])
    for i, nm in enumerate(("cliente A", "cliente B", "cliente C")):
        st, y = 0.7 + i * 0.8, 660 + i * 270

        def dr(d, i=i, st=st, y=y, nm=nm):
            q = pr(t, st + 0.2, 0.7)
            okk = q >= 1
            card(d, MX, y, 900, 240, nm, "quadra" if okk else "in corso", ORANGE if okk else GREY)
            for k, hh in enumerate((60, 95, 75, 115)):
                bx = MX + 50 + k * 58
                d.rounded_rectangle([bx, y + 210 - hh * q, bx + 42, y + 210], 8, fill=ORANGE if k == 3 else NAVY)
            T(d, (MX + 330, y + 130), "Bilancio riclassificato", "M800", 38, NAVY)
            for k in range(3):
                tick(d, MX + 330 + k * 60, y + 190, q >= (k + 1) / 3, 40, NAVY)
        fr.layer(dr, pr(t, st), rise=70)


REEL_B = [(b1, 3.8), (b2, 4.2), (b3, 4.6), (b4, 4.2),
          (cta(TB, 5, 5, "METODO", ["Ti spiego come trasformare", "un tuo report in una skill."]), 4.2)]

# =====================================================================
# REEL C - 5 skill finance
# =====================================================================
TC = "skill finance"


def squares(fr, t, y, t0, size=150):
    gap = (W - 2 * MX - 5 * size) / 4
    for i in range(5):
        q = pr(t, t0 + i * 0.18, 0.3)
        if q <= 0:
            continue
        s = size * back(q)
        cx, cy = MX + size / 2 + i * (size + gap), y + size / 2

        def dr(d, cx=cx, cy=cy, s=s, i=i):
            d.rounded_rectangle([cx - s / 2 + 8, cy - s / 2 + 10, cx + s / 2 + 8, cy + s / 2 + 10], 24, fill=(0, 43, 92, 46))
            d.rounded_rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], 24, fill=ORANGE, outline=NAVY, width=4)
            d.text((cx, cy), str(i + 1), font=F("M900", int(s * 0.55)), fill=WHITE, anchor="mm")
        fr.layer(dr)


def c1(fr, t):
    header(fr, TC, 1, 7)
    Hd(fr, t, [[("5 skill finance", B)], [("che ho costruito", B)], [("con ", B), ("Claude.", I)]])
    squares(fr, t, 760, 0.7)

    def c(d):
        card(d, MX, 1000, 900, 330, "registro skill finance", "5 skill")
        T(d, (MX + 50, 1140), "pianificazione · tesoreria · crediti", "MONO", 34, NAVY)
        T(d, (MX + 50, 1210), "bilancio · controllo · reporting", "MONO", 34, NAVY)
    fr.layer(c, pr(t, 1.7), rise=70)


def item(n, lines, title, body):
    def sc(fr, t):
        header(fr, TC, n + 1, 7)
        q = pr(t, 0.0, 0.3)
        fr.layer(lambda d: d.text((MX, 470), f"0{n}", font=F("PFI", int(250 * back(q))), fill=ORANGE, anchor="ls"), q, rise=0)
        Hd(fr, t, lines, 600, 80, 0.15)

        def c(d):
            card(d, MX, 780, 900, 620, title, f"0{n}")
            body(d, t)
        fr.layer(c, pr(t, 0.45), rise=70)
    return sc


def k1(d, t):
    for i, s in enumerate(("VAN", "TIR", "payback", "DSCR")):
        q = pr(t, 0.8 + i * 0.2, 0.25)
        if q > 0:
            x = MX + 40 + i * 208
            d.rounded_rectangle([x, 890, x + 190, 990], 22, fill=ORANGE if i == 0 else WHITE, outline=NAVY, width=4)
            T(d, (x + 95, 940), s, "M800", 38, WHITE if i == 0 else NAVY, "mm", 160)
    q = pr(t, 1.2, 0.9)
    d.line([MX + 50, 1220, MX + 850, 1220], fill=SOFT, width=5)
    pts = [(0, 300), (130, 330), (260, 290), (400, 220), (540, 150), (680, 90), (800, 40)]
    n = max(2, int(1 + q * (len(pts) - 1)))
    d.line([(MX + 50 + a, 1030 + b) for a, b in pts[:n]], fill=NAVY, width=10, joint="curve")


def k2(d, t):
    for i, (lab, wd) in enumerate((("0-30 gg", 560), ("31-60 gg", 380), ("61-90 gg", 240), ("oltre 90", 170))):
        yy = 920 + i * 115
        T(d, (MX + 50, yy), lab, "MONOB", 32, NAVY)
        q = pr(t, 0.8 + i * 0.2, 0.6)
        d.rounded_rectangle([MX + 260, yy - 26, MX + 260 + max(30, wd * q), yy + 26], 14, fill=ORANGE if i == 3 else NAVY)


def k3(d, t):
    d.line([MX + 50, 1330, MX + 850, 1330], fill=SOFT, width=5)
    series = [("base", NAVY, [(0, 300), (150, 250), (300, 220), (450, 150), (600, 110), (700, 60)]),
              ("prudente", GREY, [(0, 300), (150, 280), (300, 270), (450, 230), (600, 220), (700, 190)]),
              ("stress", ORANGE, [(0, 300), (150, 320), (300, 350), (450, 380), (600, 400), (700, 420)])]
    for i, (lab, c, pts) in enumerate(series):
        q = pr(t, 0.8 + i * 0.35, 0.8)
        if q <= 0:
            continue
        n = max(2, int(1 + q * (len(pts) - 1)))
        d.line([(MX + 50 + a, 900 + b) for a, b in pts[:n]], fill=c, width=10, joint="curve")
        if q >= 1:
            pill(d, MX + 870, 900 + pts[-1][1], lab, c, 22)


def k4(d, t):
    T(d, (MX + 235, 900), "Impieghi", "M800", 34, NAVY, "mm")
    T(d, (MX + 665, 900), "Fonti", "M800", 34, NAVY, "mm")
    blocks = [(0, 940, 190, "Immobilizzazioni", NAVY, WHITE), (0, 1140, 220, "Circolante", SOFT, NAVY),
              (1, 940, 150, "Patrimonio netto", ORANGE, WHITE), (1, 1100, 120, "Debiti finanziari", NAVY, WHITE),
              (1, 1230, 130, "Debiti operativi", SOFT, NAVY)]
    for i, (col, y, h, lab, c, tc) in enumerate(blocks):
        q = pr(t, 0.8 + i * 0.22, 0.25)
        if q <= 0:
            continue
        x = MX + 50 + col * 430
        d.rounded_rectangle([x, y, x + 370, y + h * q], 16, fill=c)
        if q >= 1:
            T(d, (x + 185, y + h / 2), lab, "M800", 30, tc, "mm")


def k5(d, t):
    scan = int(max(0, t - 0.7) * 14)
    for i in range(20):
        cx, cy = MX + 50 + (i % 5) * 162, 890 + (i // 5) * 82
        bad = i == 7 and scan > 7
        d.rectangle([cx, cy, cx + 152, cy + 72], fill=ORANGE if bad else (SOFT if i < scan else WHITE), outline=SOFT, width=3)
        if bad:
            T(d, (cx + 76, cy + 36), "#RIF!", "MONOB", 30, WHITE, "mm")
    x = MX + 50
    for i, s in enumerate(("formule", "quadrature", "etichette")):
        if pr(t, 1.7 + i * 0.2, 0.1) > 0:
            x += pillL(d, x, 1300, s, NAVY, 28) + 16


def c7(fr, t):
    header(fr, TC, 7, 7)
    fr.layer(lambda d: r.rich(d, 0, 460, [("Quale ti serve?", B)], 100, True), pr(t, 0.05))
    fr.layer(lambda d: r.rich(d, 0, 590, [("Commenta il ", B), ("numero.", I)], 84, True), pr(t, 0.25))
    squares(fr, t, 760, 0.6)
    fr.layer(lambda d: T(d, (W // 2, 1040), "ti rispondo in DM con un esempio", "MONO", 34, GREY, "mm"), pr(t, 1.7), rise=30)


REEL_C = [(c1, 3.6),
          (item(1, [[("Business plan di", B)], [("una ", B), ("nuova linea", I)]], "risultato", k1), 2.8),
          (item(2, [[("Aging dei", B)], [("crediti", I)]], "scaduto per fascia", k2), 2.8),
          (item(3, [[("Scenari", B)], [("di ", B), ("cassa", I)]], "tre scenari", k3), 2.8),
          (item(4, [[("Stato patrimoniale", B)], [("riclassificato", I)]], "impieghi e fonti", k4), 2.8),
          (item(5, [[("Revisione del", B)], [("modello ", B), ("Excel", I)]], "controllo", k5), 2.8),
          (c7, 3.6)]

REELS = {"A_claude_for_finance": REEL_A, "B_cosa_e_una_skill": REEL_B, "C_5_skill_finance": REEL_C}


def frame(sc, i, t):
    fn, dur = sc[i]
    fr = Frame()
    fn(fr, t)
    img = fr.img
    if i < len(sc) - 1 and t > dur - 0.2:
        img = Image.blend(img, r.PAPER_RGBA, 1 - max(0.0, (dur - t) / 0.2))
    put_logo(img)
    return img.convert("RGB")


if __name__ == "__main__":
    mode = sys.argv[1]
    for name, sc in REELS.items():
        if len(sys.argv) > 2 and sys.argv[2] not in name:
            continue
        if mode == "preview":
            ims = [frame(sc, i, d - 0.3).resize((360, 640)) for i, (_, d) in enumerate(sc)]
            sh = Image.new("RGB", (360 * len(ims), 640))
            for i, im in enumerate(ims):
                sh.paste(im, (360 * i, 0))
            sh.save(os.path.join(S, f"sheet_{name}.png"))
        else:
            files = []
            for i, (_, dur) in enumerate(sc):
                tmp, out = os.path.join(S, f"t_{name}_{i}.mp4"), os.path.join(S, f"s_{name}_{i}.mp4")
                p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                      "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18",
                                      "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
                for k in range(round(dur * FPS)):
                    p.stdin.write(frame(sc, i, k / FPS).tobytes())
                p.stdin.close()
                assert p.wait() == 0
                os.replace(tmp, out)
                files.append(out)
            lst = os.path.join(S, f"l_{name}.txt")
            with open(lst, "w") as f:
                for x in files:
                    f.write(f"file '{x}'\n")
            os.makedirs("/home/claude/reel", exist_ok=True)
            subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                                   "-c", "copy", f"/home/claude/reel/reel_{name}.mp4"])
            frame(sc, 0, sc[0][1] - 0.3).save(f"/home/claude/reel/cover_{name}.png")
            print("done", name, sum(d for _, d in sc))
