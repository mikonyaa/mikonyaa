"""Shared drawing kit for the miko.os profile: text, squircles, app icons, macOS window chrome,
and a small timeline helper for looping SMIL sequences. No SVG filters anywhere: blur filters
make browsers repaint every frame and the animation stutters."""
from __future__ import annotations

import os
import re
from xml.sax.saxutils import escape as _esc

SANS = "-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'SF Pro Display', 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'SF Mono', ui-monospace, Menlo, 'JetBrains Mono', 'Cascadia Mono', Consolas, 'DejaVu Sans Mono', monospace"
MONO_ADV = 0.602
FG, FG2, FG3 = "#f5f5f7", "#a1a1aa", "#6e6e78"
EASE = "0.42 0 0.58 1"
OUT = "0.16 1 0.3 1"
HERE = os.path.dirname(os.path.abspath(__file__))


def esc(s):
    return _esc(str(s), {'"': "&quot;"})


def f1(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def f3(v):
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return s or "0"


def text(x, y, s, size=14, fill=FG, family="sans", weight=400, anchor="start", extra=""):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    w = f' font-weight="{weight}"' if weight != 400 else ""
    return f'<text x="{f1(x)}" y="{f1(y)}" class="{family}" font-size="{f1(size)}"{w} fill="{fill}"{a}{extra}>{esc(s)}</text>'


def tw(s, size, mono=False, weight=400):
    if mono:
        return len(s) * size * MONO_ADV
    w = 0.0
    for ch in s:
        w += (0.27 if ch in "il.,:;|!' ·" else 0.35 if ch in "fjrt()-/" else 0.86 if ch in "mwMW" else
              0.66 if (ch.isupper() or ch.isdigit()) else 0.55)
    return w * size * (1 + max(0, weight - 400) / 1600)


def squircle(x, y, s, h=None, rk=0.225):
    """Continuous-corner rounded rectangle (Apple style)."""
    h = s if h is None else h
    r = min(s, h) * rk
    k = r * 1.28
    return (f"M{f1(x+k)} {f1(y)}H{f1(x+s-k)}C{f1(x+s-k*0.18)} {f1(y)} {f1(x+s)} {f1(y+k*0.18)} {f1(x+s)} {f1(y+k)}"
            f"V{f1(y+h-k)}C{f1(x+s)} {f1(y+h-k*0.18)} {f1(x+s-k*0.18)} {f1(y+h)} {f1(x+s-k)} {f1(y+h)}"
            f"H{f1(x+k)}C{f1(x+k*0.18)} {f1(y+h)} {f1(x)} {f1(y+h-k*0.18)} {f1(x)} {f1(y+h-k)}"
            f"V{f1(y+k)}C{f1(x)} {f1(y+k*0.18)} {f1(x+k*0.18)} {f1(y)} {f1(x+k)} {f1(y)}Z")


def icon(name, x, y, size, color):
    raw = open(os.path.join(HERE, "icons", f"{name}.svg"), encoding="utf-8").read()
    vb = re.search(r'viewBox="([^"]+)"', raw).group(1)
    inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", raw, flags=re.S)
    inner = re.sub(r"<title>.*?</title>", "", inner)
    inner = re.sub(r'\sfill="[^"]*"', "", inner)
    vx, vy, vw, _ = [float(v) for v in vb.split()]
    k = size / vw
    return f'<g transform="translate({f1(x)} {f1(y)}) scale({f3(k)}) translate({f3(-vx)} {f3(-vy)})" fill="{color}">{inner}</g>'


class Doc:
    def __init__(self, w, h, p, r=16, bg=None, border=True):
        self.w, self.h, self.p, self.r, self.border = w, h, p, r, border
        self.defs = [f'<clipPath id="{p}-clip"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>']
        self._ids = set()
        self.body = [f'<g clip-path="url(#{p}-clip)">'] + ([f'<rect width="{w}" height="{h}" fill="{bg}"/>'] if bg else [])

    def add(self, *x):
        self.body.extend(x)

    def adddef(self, *x):
        self.defs.extend(x)

    def once(self, key, d):
        if key not in self._ids:
            self._ids.add(key)
            self.defs.append(d)

    def svg(self, title="", desc=""):
        b = list(self.body) + ["</g>"]
        if self.border:
            b.append(f'<rect x="0.5" y="0.5" width="{self.w-1}" height="{self.h-1}" rx="{self.r-0.5}" fill="none" stroke="#ffffff" stroke-opacity="0.1"/>')
        css = f".sans{{font-family:{SANS}}}.mono{{font-family:{MONO}}}.tnum{{font-variant-numeric:tabular-nums}}"
        t = f"<title>{esc(title)}</title>" if title else ""
        d = f"<desc>{esc(desc)}</desc>" if desc else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
                f'role="img" fill="none">{t}{d}<style>{css}</style><defs>{"".join(self.defs)}</defs>{"".join(b)}</svg>')


# ------------------------------------------------------------------ timeline (one looping clock)

class Clock:
    """Everything in a scene loops on one period T, so sequences stay in sync."""

    def __init__(self, T):
        self.T = T

    def k(self, t):
        return max(0.0, min(1.0, t / self.T))

    def show(self, t_on, t_off=None, fade=0.0):
        """Opacity: hidden, appears at t_on, hides at t_off (default: just before the loop ends)."""
        t_off = self.T - 0.35 if t_off is None else t_off
        a, b = self.k(t_on), self.k(t_on + max(fade, 0.001))
        c, e = self.k(t_off), self.k(t_off + 0.3)
        return (f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{f3(a)};{f3(b)};{f3(c)};{f3(e)};1" '
                f'dur="{self.T}s" repeatCount="indefinite"/>')

    def type_clip(self, cid, x, y, h, text_w, t0, n, cps=16, t_off=None):
        """clipPath whose rect grows one character at a time: a typed command."""
        t_off = self.T - 0.35 if t_off is None else t_off
        step = text_w / max(1, n)
        vals, kts = ["0"], ["0"]
        for i in range(n + 1):
            vals.append(f1(i * step + (2 if i == n else 0)))
            kts.append(f3(self.k(t0 + i / cps)))
        vals += [f1(text_w + 2), "0"]
        kts += [f3(self.k(t_off)), "1"]
        # remove duplicate keyTimes (discrete mode tolerates equal times, but keep it strictly increasing)
        return (f'<clipPath id="{cid}"><rect x="{f1(x)}" y="{f1(y)}" height="{f1(h)}" width="0">'
                f'<animate attributeName="width" values="{";".join(vals)}" keyTimes="{";".join(kts)}" calcMode="discrete" '
                f'dur="{self.T}s" repeatCount="indefinite"/></rect></clipPath>'), t0 + n / cps

    def ease(self, attr, pairs, extra=""):
        """Smooth (spline) animation through (t, value) pairs inside the loop."""
        pairs = sorted(pairs)
        if pairs[0][0] > 0:
            pairs = [(0, pairs[0][1])] + pairs
        if pairs[-1][0] < self.T:
            pairs = pairs + [(self.T, pairs[-1][1])]
        vals = ";".join(str(v) for _, v in pairs)
        kts = ";".join(f3(self.k(t)) for t, _ in pairs)
        spl = ";".join([EASE] * (len(pairs) - 1))
        return (f'<animate attributeName="{attr}" values="{vals}" keyTimes="{kts}" calcMode="spline" keySplines="{spl}" '
                f'dur="{self.T}s" repeatCount="indefinite"{extra}/>')

    def ease_t(self, typ, pairs):
        pairs = sorted(pairs)
        if pairs[0][0] > 0:
            pairs = [(0, pairs[0][1])] + pairs
        if pairs[-1][0] < self.T:
            pairs = pairs + [(self.T, pairs[-1][1])]
        vals = ";".join(str(v) for _, v in pairs)
        kts = ";".join(f3(self.k(t)) for t, _ in pairs)
        spl = ";".join([EASE] * (len(pairs) - 1))
        return (f'<animateTransform attributeName="transform" type="{typ}" values="{vals}" keyTimes="{kts}" calcMode="spline" '
                f'keySplines="{spl}" dur="{self.T}s" repeatCount="indefinite" additive="sum"/>')


# ------------------------------------------------------------------ window chrome

def traffic(x, y, r=6.2):
    out = []
    for i, (c, edge) in enumerate((("#ff5f57", "#e0443e"), ("#febc2e", "#dea123"), ("#28c840", "#1aab29"))):
        cx = x + i * (r * 2 + 8)
        out.append(f'<circle cx="{f1(cx)}" cy="{f1(y)}" r="{r}" fill="{c}"/><circle cx="{f1(cx)}" cy="{f1(y)}" r="{r-0.5}" stroke="{edge}" stroke-width="1"/>'
                   f'<ellipse cx="{f1(cx)}" cy="{f1(y-r*0.45)}" rx="{f1(r*0.55)}" ry="{f1(r*0.3)}" fill="#fff" opacity="0.28"/>')
    return "".join(out)


def shadow(x, y, w, h, r=12, strength=1.0):
    """A soft drop shadow out of a few stacked translucent rounded rects (cheap to paint)."""
    out = []
    steps = [(g, 4 + g * 0.9, 0.022) for g in (26, 22, 18, 15, 12, 9, 7, 5, 3, 1.5)]
    for i, (grow, dy, op) in enumerate(steps):
        out.append(f'<rect x="{f1(x-grow)}" y="{f1(y-grow+dy)}" width="{f1(w+2*grow)}" height="{f1(h+2*grow)}" rx="{f1(r+grow)}" '
                   f'fill="#000" opacity="{f3(op*strength)}"/>')
    return "".join(out)


def window(doc, x, y, w, h, title="", fill="#1e1e22", alpha=0.94, bar=38, bar_fill=None, r=12):
    """Window with a soft shadow, a slightly translucent body and a hairline highlight."""
    gid = f"{doc.p}-winhl"
    doc.once(gid, f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.07"/>'
                  f'<stop offset="0.25" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    out = [shadow(x, y, w, h, r),
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" opacity="{alpha}"/>']
    if bar_fill:
        out.append(f'<path d="M{x} {y+bar}V{y+r}a{r} {r} 0 0 1 {r} -{r}H{x+w-r}a{r} {r} 0 0 1 {r} {r}V{y+bar}Z" fill="{bar_fill}"/>')
    out += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#{gid})"/>',
            f'<rect x="{x+0.5}" y="{y+0.5}" width="{w-1}" height="{h-1}" rx="{r-0.5}" stroke="#fff" stroke-opacity="0.13"/>',
            f'<rect x="{x-0.5}" y="{y-0.5}" width="{w+1}" height="{h+1}" rx="{r+0.5}" stroke="#000" stroke-opacity="0.55"/>',
            traffic(x + 20, y + bar / 2)]
    if bar:
        out.append(f'<path d="M{x} {y+bar}H{x+w}" stroke="#000" stroke-opacity="0.35"/>')
    if title:
        out.append(text(x + w / 2, y + bar / 2 + 4.5, title, 13, "#c7c7cc", "sans", 600, "middle"))
    return "".join(out)


# ------------------------------------------------------------------ app icons

APP = {
    "finder": ("#8fd0ff", "#1e6fe8"), "terminal": ("#4a4d55", "#141519"), "xcode": ("#5ab4ff", "#1550c8"),
    "swift": ("#ffa257", "#f23e2a"), "templates": ("#62b0ff", "#2457e6"), "tabbar": ("#caa8ff", "#6b46d6"),
    "shell": ("#4fe0cd", "#0e8590"), "menubar": ("#6a7080", "#25282f"), "resize": ("#6ee59a", "#139a4d"),
    "fonts": ("#ffbb62", "#f05a2a"), "github": ("#3a3a40", "#121214"), "messages": ("#7af07f", "#1fb33a"),
    "safari": ("#ffffff", "#d9dde6"), "settings": ("#b7bcc6", "#5d626d"),
}


def _glyph(kind, cx, cy, s):
    w = "#ffffff"
    k = s / 100
    T = f'transform="translate({f1(cx-50*k)} {f1(cy-50*k)}) scale({f3(k)})"'
    st = lambda d, sw=6, c=w: f'<path d="{d}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" fill="none" {T}/>'
    fl = lambda d, c=w, op=1: f'<path d="{d}" fill="{c}" opacity="{op}" {T}/>'
    if kind == "templates":
        return fl("M28 37 L50 26 L72 37 L50 48Z") + st("M28 50 L50 61 L72 50") + st("M28 62 L50 73 L72 62")
    if kind == "tabbar":
        return (fl("M20 56 a12 12 0 0 1 12 -12 h36 a12 12 0 0 1 12 12 a12 12 0 0 1 -12 12 h-36 a12 12 0 0 1 -12 -12z", w, 0.35)
                + fl("M24 56 a8 8 0 0 1 8 -8 h14 a8 8 0 0 1 8 8 a8 8 0 0 1 -8 8 h-14 a8 8 0 0 1 -8 -8z")
                + fl("M60 52 h12 v8 h-12z", w, 0.8) + st("M30 32 h40", 5))
    if kind == "shell":
        return (st("M24 30 h52 a6 6 0 0 1 6 6 v28 a6 6 0 0 1 -6 6 h-52 a6 6 0 0 1 -6 -6 v-28 a6 6 0 0 1 6 -6z", 5)
                + st("M38 30 V70", 5) + fl("M64 36 h10 v28 h-10z", w, 0.75))
    if kind == "menubar":
        return st("M38 38 a6 6 0 1 1 6 -6 v36 a6 6 0 1 1 -6 -6 h24 a6 6 0 1 1 -6 6 v-36 a6 6 0 1 1 6 6z", 5.5)
    if kind == "resize":
        return st("M22 50 H78") + st("M33 39 L22 50 L33 61") + st("M67 39 L78 50 L67 61") + st("M14 30 V70", 5) + st("M86 30 V70", 5)
    if kind == "fonts":
        return (f'<text x="{f1(cx-4*k)}" y="{f1(cy+14*k)}" text-anchor="middle" font-family="Georgia, \'Times New Roman\', serif" '
                f'font-size="{f1(48*k)}" font-weight="700" fill="{w}">Aa</text>' + st("M70 66 a8 8 0 1 1 0.1 0 M76 72 l8 8", 4.5))
    if kind == "terminal":
        return st("M28 38 L42 50 L28 62") + st("M48 64 H70")
    if kind == "swift":
        return icon("swift", cx - 30 * k, cy - 30 * k, 60 * k, w)
    if kind == "github":
        return icon("github", cx - 30 * k, cy - 30 * k, 60 * k, "#ffffff")
    if kind == "xcode":
        return (fl("M26 66 L58 34 L66 42 L34 74Z", "#e8f1ff") + fl("M54 26 h18 a4 4 0 0 1 4 4 v8 h-10 l-6 -6z", "#ffffff")
                + st("M30 30 h40 M30 30 v40", 2.5, "#ffffff"))
    if kind == "messages":
        return fl("M50 24 C72 24 84 36 84 50 C84 64 72 76 50 76 C45 76 40 75 36 73 L22 80 L26 67 C19 62 16 56 16 50 C16 36 28 24 50 24Z")
    if kind == "finder":
        return (fl("M50 18 h28 a10 10 0 0 1 10 10 v44 a10 10 0 0 1 -10 10 h-28z", "#dceeff", 0.95)
                + f'<path d="M50 18 C46 34 44 46 46 58 L54 58" stroke="#0b2f6b" stroke-width="4" fill="none" stroke-linecap="round" {T}/>'
                + fl("M34 38 h4 v8 h-4z M64 38 h4 v8 h-4z", "#0b2f6b")
                + f'<path d="M32 66 Q50 76 68 66" stroke="#0b2f6b" stroke-width="4" fill="none" stroke-linecap="round" {T}/>')
    if kind == "safari":
        return (f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(36*k)}" fill="#1f7cf5"/>'
                + fl("M50 20 L56 50 L50 80 L44 50Z", "#ff3b30") + fl("M50 50 L56 50 L50 80 L44 50Z", "#ffffff"))
    if kind == "settings":
        return (f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(26*k)}" stroke="#2c2f36" stroke-width="{f1(10*k)}" stroke-dasharray="{f1(6*k)} {f1(4*k)}"/>'
                f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(14*k)}" fill="#e6e8ee"/>')
    return ""


def app_icon(doc, kind, x, y, s):
    a, b = APP[kind]
    gid = f"{doc.p}-ai-{kind}"
    doc.once(gid, f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')
    doc.once(f"{doc.p}-gloss", f'<linearGradient id="{doc.p}-gloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.32"/>'
                               f'<stop offset="0.45" stop-color="#fff" stop-opacity="0.04"/><stop offset="1" stop-color="#000" stop-opacity="0.08"/></linearGradient>')
    d = squircle(x, y, s)
    return (f'<path d="{d}" transform="translate(0 {f1(s*0.05)})" fill="#000" opacity="0.28"/>'
            f'<path d="{d}" fill="url(#{gid})"/><path d="{d}" fill="url(#{doc.p}-gloss)"/>'
            f'<path d="{d}" stroke="#fff" stroke-opacity="0.22" stroke-width="1"/>' + _glyph(kind, x + s / 2, y + s / 2, s))
