import sys, os, math, subprocess
from PIL import Image, ImageDraw, ImageFont

S = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(os.path.dirname(S), "fonts")
W, H, FPS = 1080, 1920, 30
PAPER, LINE = (245, 242, 234), (226, 221, 209)
NAVY, ORANGE, WHITE = (0, 43, 92), (255, 107, 0), (255, 255, 255)
GREY, SOFT = (122, 135, 153), (232, 236, 242)
MX = 90
_fc = {}


def F(name, size):
    k = (name, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(os.path.join(FD, name + ".ttf"), size)
    return _fc[k]


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def pr(t, start, dur=0.4):
    return ease((t - start) / dur)


# ---------- paper background ----------
BG = Image.new("RGB", (W, H), PAPER)
_b = ImageDraw.Draw(BG)
for x in range(0, W, 36):
    _b.line([x, 0, x, H], fill=LINE, width=1)
for y in range(0, H, 36):
    _b.line([0, y, W, y], fill=LINE, width=1)


class Frame:
    def __init__(self):
        self.img = BG.copy().convert("RGBA")

    def layer(self, draw_fn, p=1.0, rise=50, dx=0):
        """draw_fn(d) draws at full opacity; composited with alpha p and a rise."""
        if p <= 0:
            return
        ly = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw_fn(ImageDraw.Draw(ly))
        if p < 1:
            ly.putalpha(ly.getchannel("A").point(lambda v: int(v * p)))
        self.img.alpha_composite(ly, (0, 0)) if p >= 1 and not dx else self._off(ly, int(dx * (1 - p)), int(rise * (1 - p)))

    def _off(self, ly, ox, oy):
        base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        base.paste(ly, (ox, oy))
        self.img.alpha_composite(base)


# ---------- building blocks ----------
def rich(d, x, y, segs, size, center=False):
    """segs: [(text, 'b'|'i')]; y is the baseline."""
    fonts = {"b": (F("M800", size), NAVY), "i": (F("PFI", int(size * 1.08)), ORANGE)}
    if center:
        x = (W - sum(fonts[s][0].getlength(tx) for tx, s in segs)) / 2
    for tx, s in segs:
        f, c = fonts[s]
        d.text((x, y), tx, font=f, fill=c, anchor="ls")
        x += f.getlength(tx)


def header(fr, topic, n):
    def dr(d):
        f = F("MONO", 30)
        d.text((MX, 215), "// ", font=f, fill=GREY)
        d.text((MX + f.getlength("// "), 215), f"0{n}", font=F("MONOB", 30), fill=ORANGE)
        d.text((MX + f.getlength("// 0n "), 215), f"· {topic}", font=f, fill=GREY)
        d.text((W - MX, 215), f"{n}/5", font=f, fill=GREY, anchor="ra")
    fr.layer(dr)


def pill(d, xr, cy, s, color=ORANGE, size=26):
    f = F("MONOB", size)
    w = f.getlength(s) + 32
    d.rounded_rectangle([xr - w, cy - 22, xr, cy + 22], 22, fill=color)
    d.text((xr - w / 2, cy), s, font=f, fill=WHITE, anchor="mm")
    return w


def card(d, x, y, w, h, title, tag=None, tagc=ORANGE):
    d.rounded_rectangle([x + 10, y + 12, x + w + 10, y + h + 12], 26, fill=(0, 43, 92, 46))
    d.rounded_rectangle([x, y, x + w, y + h], 26, fill=WHITE, outline=NAVY, width=4)
    for i, c in enumerate((ORANGE, NAVY, GREY)):
        d.ellipse([x + 28 + i * 26, y + 30, x + 44 + i * 26, y + 46], fill=c)
    d.text((x + 120, y + 38), title, font=F("MONOB", 28), fill=NAVY, anchor="lm")
    if tag:
        pill(d, x + w - 24, y + 38, tag, tagc)
    d.line([x + 4, y + 74, x + w - 4, y + 74], fill=SOFT, width=3)


def wordmark(d, cx, y, size):
    f = F("M900", size)
    w1, w2 = f.getlength("Control"), f.getlength("IA")
    x = cx - (w1 + w2) / 2
    d.text((x, y), "Control", font=f, fill=NAVY)
    d.text((x + w1, y), "IA", font=f, fill=ORANGE)


# ---------- scenes ----------
def s1(fr, t):
    header(fr, "fine mese", 1)
    fr.layer(lambda d: rich(d, MX, 400, [("Il tuo ufficio", "b")], 84), pr(t, 0.05))
    fr.layer(lambda d: rich(d, MX, 500, [("amministrativo", "b")], 84), pr(t, 0.2))
    fr.layer(lambda d: rich(d, MX, 600, [("rincorre i dati", "b")], 84), pr(t, 0.35))
    fr.layer(lambda d: rich(d, MX, 700, [("invece di ", "b"), ("leggerli?", "i")], 84), pr(t, 0.5))

    rows = ["estratti conto", "scadenziario", "report direzione"]

    def a(d):
        card(d, MX, 820, 640, 450, "chiusura mese", "3 aperti")
        for i, s in enumerate(rows):
            y = 950 + i * 100
            if pr(t, 1.1 + i * 0.3, 0.2) <= 0:
                continue
            d.rounded_rectangle([MX + 36, y - 22, MX + 80, y + 22], 8, outline=NAVY, width=4)
            d.text((MX + 104, y), s, font=F("M600", 36), fill=NAVY, anchor="lm")
            pill(d, MX + 610, y, "da fare", GREY, 22)
    fr.layer(a, pr(t, 0.8))

    def b(d):
        card(d, 520, 1210, 470, 330, "report", "in ritardo")
        cx, cy, r = 640, 1400, 78
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=8)
        ang = t * 2.4
        d.line([cx, cy, cx + math.sin(ang) * 52, cy - math.cos(ang) * 52], fill=ORANGE, width=8)
        d.line([cx, cy, cx, cy - 38], fill=NAVY, width=8)
        for i, wd in enumerate((200, 150, 180)):
            d.rounded_rectangle([760, 1350 + i * 44, 760 + wd, 1368 + i * 44], 9, fill=SOFT)
    fr.layer(b, pr(t, 1.7), rise=70)


def s2(fr, t):
    header(fr, "nasce", 2)
    fr.layer(lambda d: rich(d, MX, 420, [("L'AI entra nella tua", "b")], 80), pr(t, 0.05))
    fr.layer(lambda d: rich(d, MX, 520, [("amministrazione", "b")], 80), pr(t, 0.2))
    fr.layer(lambda d: rich(d, MX, 620, [("e ", "b"), ("finanza.", "i")], 80), pr(t, 0.35))

    def c(d):
        card(d, MX, 780, 900, 620, "AI 4 Finance", "nuovo")
        d.text((MX + 60, 900), "AI 4", font=F("M900", 190), fill=NAVY)
        d.text((MX + 60, 1305), "Finance", font=F("PFI", 210), fill=ORANGE, anchor="ls")
        p = pr(t, 1.0, 0.6)
        d.rectangle([MX + 60, 1335, MX + 60 + int(780 * p), 1345], fill=NAVY)
    fr.layer(c, pr(t, 0.6), rise=80)
    fr.layer(lambda d: d.text((W // 2, 1480), "per imprenditori · CFO · responsabili amministrativi",
                              font=F("MONO", 28), fill=GREY, anchor="ma"), pr(t, 1.3), rise=30)


def s3(fr, t):
    header(fr, "come funziona", 3)
    fr.layer(lambda d: rich(d, MX, 400, [("Formazione +", "b")], 80), pr(t, 0.05))
    fr.layer(lambda d: rich(d, MX, 500, [("implementazione", "b")], 80), pr(t, 0.2))
    fr.layer(lambda d: rich(d, MX, 600, [("su 4 ", "b"), ("processi.", "i")], 80), pr(t, 0.35))
    cw, ch = 430, 400
    spots = [(MX, 700), (560, 700), (MX, 1140), (560, 1140)]
    names = ["Tesoreria e cash flow", "Crediti e solleciti", "Reporting e controllo", "Governance AI Act e GDPR"]
    tags = ["01", "02", "03", "04"]

    def body(d, i, x, y, q):
        ix, iy, iw = x + 36, y + 110, cw - 72
        if i == 0:
            pts = [(0, 150), (60, 120), (120, 135), (180, 80), (240, 95), (300, 40), (358, 20)]
            n = max(2, int(1 + q * (len(pts) - 1)))
            d.line([(ix + a, iy + b) for a, b in pts[:n]], fill=ORANGE, width=9, joint="curve")
            d.line([ix, iy + 170, ix + iw, iy + 170], fill=SOFT, width=4)
        elif i == 1:
            for r, (lab, c) in enumerate((("sollecito", ORANGE), ("incassato", NAVY), ("sollecito", ORANGE))):
                yy = iy + 22 + r * 60
                d.rounded_rectangle([ix, yy - 9, ix + 150, yy + 9], 9, fill=SOFT)
                if q > r / 3:
                    pill(d, ix + iw, yy, lab, c, 20)
        elif i == 2:
            for b_, hh in enumerate((70, 110, 90, 160)):
                bx = ix + 20 + b_ * 88
                d.rounded_rectangle([bx, iy + 175 - hh * q, bx + 58, iy + 175], 10,
                                    fill=ORANGE if b_ == 3 else NAVY)
        else:
            for r, lab in enumerate(("AI Act", "GDPR")):
                yy = iy + 40 + r * 84
                d.rounded_rectangle([ix, yy - 26, ix + 52, yy + 26], 10, fill=ORANGE if q > 0.3 + r * 0.3 else SOFT)
                if q > 0.3 + r * 0.3:
                    d.line([ix + 12, yy, ix + 22, yy + 12, ix + 40, yy - 12], fill=WHITE, width=7)
                d.text((ix + 76, yy), lab, font=F("M800", 40), fill=NAVY, anchor="lm")

    for i, (x, y) in enumerate(spots):
        st = 0.8 + i * 0.75

        def dr(d, i=i, x=x, y=y, st=st):
            card(d, x, y, cw, ch, "processo", tags[i])
            body(d, i, x, y, pr(t, st + 0.25, 0.7))
            f = F("M800", 25)
            d.text((x + 36, y + ch - 52), names[i], font=f, fill=NAVY, anchor="lm")
        fr.layer(dr, pr(t, st), rise=70)


def s4(fr, t):
    header(fr, "la metrica", 4)
    fr.layer(lambda d: rich(d, MX, 410, [("Un solo numero:", "b")], 84), pr(t, 0.05))
    fr.layer(lambda d: rich(d, MX, 515, [("le ore ", "b"), ("restituite", "i")], 84), pr(t, 0.2))
    fr.layer(lambda d: rich(d, MX, 620, [("al tuo team.", "b")], 84), pr(t, 0.35))

    def c(d):
        card(d, 170, 760, 740, 720, "tempo restituito", "ogni mese")
        cx, cy, r = W // 2, 1150, 230
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=SOFT, width=30)
        sweep = ease((t - 0.8) / 1.8) * 290
        d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + sweep, fill=ORANGE, width=30)
        ang = math.radians(-90 + sweep)
        d.line([cx, cy, cx + math.cos(ang) * 150, cy + math.sin(ang) * 150], fill=NAVY, width=16)
        d.line([cx, cy, cx, cy - 100], fill=NAVY, width=16)
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=ORANGE)
    fr.layer(c, pr(t, 0.6), rise=80)


def s5(fr, t):
    header(fr, "il prossimo passo", 5)
    fr.layer(lambda d: rich(d, 0, 430, [("Commenta", "b")], 120, center=True), pr(t, 0.05))
    fr.layer(lambda d: rich(d, 0, 590, [("FINANCE", "i")], 150, center=True), pr(t, 0.25))

    def a(d):
        card(d, MX, 700, 900, 250, "commenti")
        d.ellipse([MX + 40, 800, MX + 130, 890], fill=SOFT, outline=NAVY, width=4)
        d.rounded_rectangle([MX + 160, 800, MX + 860, 890], 45, outline=NAVY, width=4)
        word = "FINANCE"[: int(max(0, t - 1.0) / 0.09)]
        f = F("M800", 46)
        d.text((MX + 200, 845), word, font=f, fill=NAVY, anchor="lm")
        if int(t * 3) % 2 == 0:
            cx = MX + 204 + f.getlength(word)
            d.rectangle([cx, 822, cx + 5, 868], fill=ORANGE)
    fr.layer(a, pr(t, 0.6), rise=70)

    def b(d):
        card(d, MX, 1000, 900, 330, "DM", "ControlIA", NAVY)
        d.rounded_rectangle([MX + 40, 1110, MX + 800, 1290], 36, fill=ORANGE)
        d.text((MX + 80, 1166), "Da quale processo partire", font=F("M800", 42), fill=WHITE, anchor="lm")
        d.text((MX + 80, 1232), "nella tua azienda.", font=F("M800", 42), fill=WHITE, anchor="lm")
    fr.layer(b, pr(t, 1.9), rise=70)
    fr.layer(lambda d: wordmark(d, W // 2, 1400, 84), pr(t, 2.4), rise=30)
    fr.layer(lambda d: d.text((W // 2, 1512), "L'Intelligenza del Controllo", font=F("M600", 38),
                              fill=GREY, anchor="ma"), pr(t, 2.6), rise=30)


SCENES = [(s1, 3.6), (s2, 3.0), (s3, 5.4), (s4, 3.2), (s5, 4.4)]
PAPER_RGBA = BG.convert("RGBA")


def frame(i, t):
    fn, dur = SCENES[i]
    fr = Frame()
    fn(fr, t)
    img = fr.img
    if i < len(SCENES) - 1 and t > dur - 0.2:
        img = Image.blend(img, PAPER_RGBA, 1 - max(0.0, (dur - t) / 0.2))
    return img.convert("RGB")


if __name__ == "__main__":
    if sys.argv[1] == "preview":
        for i, (_, dur) in enumerate(SCENES):
            frame(i, dur - 0.35).save(os.path.join(S, f"p{i+1}.png"))
    else:
        files = []
        for i, (_, dur) in enumerate(SCENES):
            tmp, out = os.path.join(S, f"t2_{i}.mp4"), os.path.join(S, f"sc2_{i}.mp4")
            p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                  "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18",
                                  "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
            for k in range(round(dur * FPS)):
                p.stdin.write(frame(i, k / FPS).tobytes())
            p.stdin.close()
            assert p.wait() == 0
            os.replace(tmp, out)
            files.append(out)
        with open(os.path.join(S, "list2.txt"), "w") as f:
            for x in files:
                f.write(f"file '{x}'\n")
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i",
                               os.path.join(S, "list2.txt"), "-c", "copy", os.path.join(S, "joined2.mp4")])
        print("done")
