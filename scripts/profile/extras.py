"""Contacts (linked pills), the Telegram footer, "How I build", Updates and Activity."""
from __future__ import annotations

import datetime as dt
import random

import chibi
import data as gh
from kit import (EASE, FG, FG2, FG3, Clock, Doc, _glyph, app_icon, esc, f1, f3, icon, shadow, squircle, text, tw, traffic)


# ================================================================== contacts

def _shine(D, w, h, r, period=7.0, delay=0.0):
    p = D.p
    D.adddef(f'<linearGradient id="{p}-sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
             f'<stop offset="0.5" stop-color="#fff" stop-opacity="0.13"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>',
             f'<clipPath id="{p}-pc"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>')
    k0, k1 = f3(delay / period), f3((delay + 1.1) / period)
    return (f'<g clip-path="url(#{p}-pc)"><rect x="-120" y="0" width="90" height="{h}" fill="url(#{p}-sh)" transform="skewX(-20)">'
            f'<animate attributeName="x" values="-120;-120;{w+60};{w+60}" keyTimes="0;{k0};{k1};1" dur="{period}s" repeatCount="indefinite" '
            f'calcMode="spline" keySplines="0 0 1 1;{EASE};0 0 1 1"/></rect></g>')


def _tg_glyph(cx, cy, s):
    k = s / 52
    return (f'<g transform="translate({f1(cx)} {f1(cy)}) scale({f3(k)})">'
            f'<g><animateTransform attributeName="transform" type="translate" values="0 0;1.6 -1.6;0 0" dur="2.8s" repeatCount="indefinite" '
            f'calcMode="spline" keyTimes="0;0.5;1" keySplines="{EASE};{EASE}"/>'
            f'<path d="M-13 -1.5 L12 -11.5 C13.3 -12 14.3 -11 14 -9.6 L9.8 10.4 C9.5 11.8 8 12.3 6.9 11.5 L0.6 6.8 L-2.6 9.9 C-3.2 10.5 -4.2 10.2 -4.3 9.4 L-5.2 3.3 L-12.8 0.9 C-14.3 0.4 -14.4 -0.9 -13 -1.5Z" fill="#fff"/>'
            f'<path d="M-5.2 3.3 L8.6 -6.6 L0.6 6.8" fill="#cfe8f7"/></g></g>')


def _mail_glyph(cx, cy, s):
    k = s / 52
    flap = ('<animateTransform attributeName="transform" type="scale" values="1 1;1 1;1 -0.55;1 1;1 1" keyTimes="0;0.55;0.65;0.78;1" '
            'dur="5s" repeatCount="indefinite"/>')
    return (f'<g transform="translate({f1(cx)} {f1(cy)}) scale({f3(k)})">'
            f'<rect x="-14" y="-10" width="28" height="20" rx="4" fill="#fff"/>'
            f'<path d="M-14 9 L-3 0 M14 9 L3 0" stroke="#d6d2ff" stroke-width="1.6"/>'
            f'<g transform="translate(0 -9)"><g>{flap}<path d="M-13 0 L0 10 L13 0" stroke="#7a6cf0" stroke-width="2.2" fill="#f1efff" stroke-linejoin="round"/></g></g></g>')


def _kz_flag(D, x, y, w, h):
    """The flag of Kazakhstan, exactly as published on Wikimedia Commons (public domain), no animation."""
    import os
    import re
    raw = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "flag-kz.svg"), encoding="utf-8").read()
    inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", raw, flags=re.S)
    inner = re.sub(r'id="([A-Z])"', r'id="kz-\1"', inner)
    inner = re.sub(r'xlink:href="#([A-Z])"', r'href="#kz-\1"', inner)
    p = D.p
    r = h * 0.14
    D.adddef(f'<clipPath id="{p}-flag"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r:.1f}"/></clipPath>')
    return (f'<g clip-path="url(#{p}-flag)"><svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 1000 500" preserveAspectRatio="none">{inner}</svg></g>'
            f'<rect x="{x+0.5}" y="{y+0.5}" width="{w-1}" height="{h-1}" rx="{r:.1f}" stroke="#fff" stroke-opacity="0.18"/>')


def contact(kind):
    label, value = {"telegram": ("Telegram", "@mikonyaa"), "email": ("Email", "dev.miko@icloud.com"),
                    "location": ("Based in", "Astana, Kazakhstan")}[kind]
    h = 76
    tx = 96 if kind == "location" else 84
    w = int(tx + max(tw(label, 13, weight=600), tw(value, 19, weight=700)) + 30)
    D = Doc(w, h, f"ct{kind[:3]}", r=h // 2, bg="#17171c", border=False)
    p = D.p
    D.adddef(f'<linearGradient id="{p}-bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22222a"/><stop offset="1" stop-color="#15151a"/></linearGradient>')
    D.add(f'<rect width="{w}" height="{h}" fill="url(#{p}-bg)"/>')
    cx, cy, cr = 38, 38, 26
    if kind == "telegram":
        D.adddef(f'<linearGradient id="{p}-ic" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#41b6ee"/><stop offset="1" stop-color="#1d93d2"/></linearGradient>')
        D.add(f'<circle cx="{cx}" cy="{cy}" r="{cr}" fill="url(#{p}-ic)"/>' + _tg_glyph(cx - 1, cy + 1, 52))
    elif kind == "email":
        D.adddef(f'<linearGradient id="{p}-ic" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a8cff"/><stop offset="1" stop-color="#5f4be0"/></linearGradient>')
        D.add(f'<circle cx="{cx}" cy="{cy}" r="{cr}" fill="url(#{p}-ic)"/>' + _mail_glyph(cx, cy + 1, 52))
    else:
        D.add(_kz_flag(D, 12, 21, 68, 34))
    D.add(text(tx, 32, label, 13, FG2, "sans", 600) + text(tx, 56, value, 19, FG, "sans", 700, extra=' letter-spacing="-0.2"'))
    if kind != "location":
        D.add(_shine(D, w, h, h / 2, delay={"telegram": 0.0, "email": 0.4}[kind]))
    D.add(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{h/2-0.5}" stroke="#fff" stroke-opacity="0.14"/>')
    return D.svg(title=f"{label}: {value}")


# ================================================================== Telegram footer

def telegram(d):
    W, H = 1200, 580
    D = Doc(W, H, "tg", r=16, bg="#0e1621")
    C = Clock(14.0)
    p = D.p
    rng = random.Random(4)
    D.adddef(f'<linearGradient id="{p}-wp" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1c2b4a"/>'
             f'<stop offset="0.5" stop-color="#22243f"/><stop offset="1" stop-color="#2f2246"/></linearGradient>')
    D.add(f'<rect width="{W}" height="{H}" fill="url(#{p}-wp)"/>')
    # doodle wallpaper, like Telegram's chat patterns
    doodles = ["M-6 0 a6 6 0 1 0 12 0 a6 6 0 1 0 -12 0", "M-7 -3 l7 -4 l7 4 v6 l-7 4 l-7 -4z", "M-6 -6 l12 12 M6 -6 l-12 12",
               "M0 -7 l2 5 l5 0 l-4 3 l2 6 l-5 -4 l-5 4 l2 -6 l-4 -3 l5 0z", "M-7 4 l7 -9 l7 9", "M-5 -6 h10 v12 h-10z M-5 -2 h10",
               "M-8 0 q4 -8 8 0 t8 0", "M-4 -7 l-4 7 l4 7 M4 -7 l4 7 l-4 7"]
    dd = []
    for i in range(140):
        x, y = rng.uniform(0, W), rng.uniform(60, H - 56)
        dd.append(f'<path d="{rng.choice(doodles)}" transform="translate({f1(x)} {f1(y)}) rotate({rng.randint(-30, 30)}) scale({rng.uniform(0.9, 1.5):.2f})" '
                  f'stroke="#fff" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    D.add(f'<g opacity="0.05">{"".join(dd)}</g>')
    # header
    D.add(f'<rect width="{W}" height="60" fill="#17212b"/><path d="M0 60H{W}" stroke="#000" stroke-opacity="0.35"/>' + traffic(22, 30)
          + f'<path d="M92 22 l-8 8 l8 8" stroke="#6ab2f2" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    D.adddef(f'<clipPath id="{p}-ha"><circle cx="128" cy="30" r="20"/></clipPath>',
             f'<linearGradient id="{p}-abg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fb4ff"/><stop offset="1" stop-color="#ff9fb0"/></linearGradient>')
    D.add(f'<circle cx="128" cy="30" r="20" fill="url(#{p}-abg)"/><g clip-path="url(#{p}-ha)">{chibi.bust(128, 29, 0.28, p+"h", smile="open")}</g>'
          + text(158, 26, "miko", 15.5, FG, "sans", 700))
    online = C.ease("opacity", [(0, 1), (3.4, 1), (3.5, 0), (5.0, 0), (5.1, 1)])
    typing = C.ease("opacity", [(0, 0), (3.4, 0), (3.5, 1), (5.0, 1), (5.1, 0)])
    D.add(f'<g>{online}' + text(158, 45, "online", 13, "#6ab2f2", "sans", 500) + '</g>'
          f'<g opacity="0">{typing}' + text(158, 45, "typing…", 13, "#6ab2f2", "sans", 500) + '</g>')
    for i, g in enumerate(("M-6 -6 a6 6 0 1 0 0.1 0 M5 5 l5 5", "M-7 -5 q0 -2 2 -2 h2 l2 4 l-2 2 q2 4 6 6 l2 -2 l4 2 v2 q0 2 -2 2 q-14 0 -14 -14z",
                           "M0 -7 v0.1 M0 0 v0.1 M0 7 v0.1")):
        D.add(f'<path d="{g}" transform="translate({W-110+i*40} 30)" stroke="#8b9bab" stroke-width="{3.2 if i == 2 else 1.9}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    # date chip
    D.add(f'<rect x="{W/2-34}" y="74" width="68" height="24" rx="12" fill="#000" opacity="0.28"/>' + text(W / 2, 90.5, "Today", 12.5, "#e8eef4", "sans", 600, "middle"))
    x0, x1 = 300, 900

    def bubble(y, msg, t0, out=False, buttons=None, read_at=None):
        fs = 15.5
        emoji = sum(1 for ch in msg if ord(ch) > 0x2600)
        bw = tw(msg, fs, weight=500) + emoji * fs * 0.75 + (100 if out else 86)
        bh = 40
        bx = x1 - bw if out else x0
        fill = "#2b5278" if out else "#182533"
        tail = (f'<path d="M{f1(bx+bw-8)} {y+bh-14} q6 12 16 14 q-14 2 -22 -6z" fill="{fill}"/>' if out else
                f'<path d="M{f1(bx+8)} {y+bh-14} q-6 12 -16 14 q14 2 22 -6z" fill="{fill}"/>')
        body = (f'<rect x="{f1(bx)}" y="{y}" width="{f1(bw)}" height="{bh}" rx="16" fill="{fill}"/>{tail}'
                + text(bx + 14, y + 25.5, msg, fs, "#f5f7fa", "sans", 500)
                + text(bx + bw - (38 if out else 12), y + 29, "09:41", 11.5, "#7da8d3" if out else "#6d7f8f", "sans", 500, "end"))
        if out:
            body += (f'<path d="M{f1(bx+bw-31)} {y+25} l3 3 l6 -7" stroke="#7da8d3" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
                     f'<path d="M{f1(bx+bw-26)} {y+28} l6 -7" stroke="#7da8d3" stroke-width="1.6" fill="none" stroke-linecap="round" opacity="0">'
                     + C.ease("opacity", [(0, 0), (read_at, 0), (read_at + 0.2, 1), (13.4, 1), (13.6, 0)]) + '</path>')
        if buttons:
            gw = (max(bw, 330) - 6) / len(buttons)
            for i, b in enumerate(buttons):
                gx = bx + i * (gw + 6)
                body += (f'<rect x="{f1(gx)}" y="{y+bh+6}" width="{f1(gw)}" height="36" rx="12" fill="#000" opacity="0.32"/>'
                         + text(gx + gw / 2, y + bh + 29, b, 14, "#ffffff", "sans", 600, "middle"))
        ox = bx + bw if out else bx
        pop = C.ease_t("scale", [(0, "0.9"), (t0, "0.9"), (t0 + 0.25, "1")])
        return (f'<g opacity="0">{C.show(t0, 13.4, fade=0.18)}<g transform="translate({f1(ox)} {y+bh})"><g>{pop}'
                f'<g transform="translate({f1(-ox)} {-(y+bh)})">{body}</g></g></g></g>')

    # sticker: Miko waving on a die-cut white blob
    sx, sy = x0 + 70, 176
    sticker = (f'<ellipse cx="{sx}" cy="{sy+80}" rx="58" ry="8" fill="#000" opacity="0.25"/>'
               f'<path d="M{sx-62} {sy+10} C{sx-66} {sy-50} {sx-30} {sy-80} {sx+4} {sy-78} C{sx+44} {sy-76} {sx+82} {sy-50} {sx+80} {sy+4} '
               f'C{sx+78} {sy+50} {sx+40} {sy+78} {sx} {sy+78} C{sx-36} {sy+78} {sx-60} {sy+50} {sx-62} {sy+10}Z" fill="#fff"/>'
               f'<g transform="translate(0 0)">{chibi.bust(sx, sy - 4, 0.6, p+"st", wave=True, smile="open")}</g>'
               f'<rect x="{sx+46}" y="{sy+58}" width="46" height="20" rx="10" fill="#000" opacity="0.4"/>' + text(sx + 69, sy + 72, "09:41", 11, "#fff", "sans", 500, "middle"))
    D.adddef(f'<clipPath id="{p}-stc"><rect x="{sx-90}" y="{sy-96}" width="200" height="180"/></clipPath>')
    pop = C.ease_t("scale", [(0, "0.6"), (0.4, "0.6"), (0.8, "1.06"), (1.0, "1")])
    D.add(f'<g opacity="0">{C.show(0.4, 13.4, fade=0.2)}<g transform="translate({sx} {sy+78})"><g>{pop}<g transform="translate({-sx} {-(sy+78)})">'
          f'<g clip-path="url(#{p}-stc)">{sticker}</g></g></g></g></g>')
    y = 268
    D.add(bubble(y, "you scrolled all the way down 👀", 1.5))
    D.add(bubble(y + 48, "it was supposed to be a quick stop.", 2.5))
    # typing bubble
    dots = "".join(f'<circle cx="{x0+20+i*12}" cy="{y+96+20}" r="4" fill="#8b9bab"><animate attributeName="opacity" values="0.3;1;0.3" dur="0.9s" '
                   f'begin="{i*0.15:.2f}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="{EASE};{EASE}"/></circle>' for i in range(3))
    D.add(f'<g opacity="0">{C.ease("opacity", [(0, 0), (3.5, 0), (3.7, 1), (4.9, 1), (5.0, 0)])}'
          f'<rect x="{x0}" y="{y+96}" width="64" height="40" rx="16" fill="#182533"/>{dots}</g>')
    D.add(bubble(y + 96, "say hi — I'm one message away", 5.0, buttons=["✈️  Telegram", "✉️  Email"]))
    D.add(bubble(y + 192, "hi miko! 👋", 7.2, out=True, read_at=8.0))
    # input bar
    D.add(f'<rect y="{H-56}" width="{W}" height="56" fill="#17212b"/><path d="M0 {H-56}H{W}" stroke="#000" stroke-opacity="0.3"/>'
          f'<path d="M{x0-6} {H-36} l-7 7 a5 5 0 0 0 7 7 l11 -11 a3.5 3.5 0 0 0 -5 -5 l-10 10" stroke="#8b9bab" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
          + text(x0 + 24, H - 22, "Write a message…", 15, "#6d7f8f", "sans", 500)
          + f'<circle cx="{x1-40}" cy="{H-28}" r="10" stroke="#8b9bab" stroke-width="1.8"/><path d="M{x1-44} {H-25} q4 4 8 0" stroke="#8b9bab" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
          f'<rect x="{x1-8}" y="{H-40}" width="10" height="16" rx="5" stroke="#8b9bab" stroke-width="1.8"/><path d="M{x1-12} {H-26} q8 9 16 0 M{x1-3} {H-17} v4" stroke="#8b9bab" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
    return D.svg(title="Say hi on Telegram", desc="A Telegram chat with miko: you scrolled all the way down; it was supposed to be a quick stop; say hi, I'm one message away.")


# ================================================================== How I build

def _node_icon(D, kind, x, y, s):
    cols = {"ios": ("#5ab4ff", "#1550c8"), "mac": ("#8e94a3", "#3a3e48"), "cli": ("#4a4d55", "#141519"), "vapor": ("#a77bff", "#4b2fd1"),
            "fastapi": ("#14b8a6", "#047a6e"), "postgresql": ("#5d8fd1", "#2a4f86"), "mysql": ("#f2a23a", "#c9670f"),
            "sqlite": ("#3aa0e8", "#0d5f93"), "git": ("#f5664a", "#c4381f"), "githubactions": ("#3a3a40", "#121214"), "docker": ("#45a8ff", "#1d63c9")}[kind]
    gid = f"{D.p}-ni-{kind}"
    D.once(gid, f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{cols[0]}"/><stop offset="1" stop-color="{cols[1]}"/></linearGradient>')
    d = squircle(x, y, s)
    out = f'<path d="{d}" fill="url(#{gid})"/><path d="{d}" stroke="#fff" stroke-opacity="0.2"/>'
    cx, cy, k = x + s / 2, y + s / 2, s / 40
    st = lambda path, sw=2.2: f'<path d="{path}" transform="translate({f1(cx)} {f1(cy)}) scale({f3(k)})" stroke="#fff" stroke-width="{sw}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    if kind == "ios":
        out += st("M-6 -11 h12 a3 3 0 0 1 3 3 v16 a3 3 0 0 1 -3 3 h-12 a3 3 0 0 1 -3 -3 v-16 a3 3 0 0 1 3 -3z M-2 -8 h4")
    elif kind == "mac":
        out += st("M-10 -8 h20 v13 h-20z M-14 8 h28")
    elif kind == "cli":
        out += st("M-9 -5 l5 5 l-5 5 M1 6 h8")
    elif kind == "vapor":
        out += f'<path d="M0 -11 C5 -4 9 1 9 5 a9 9 0 1 1 -18 0 C-9 1 -5 -4 0 -11Z" transform="translate({f1(cx)} {f1(cy+1)}) scale({f3(k)})" fill="#fff"/>'
    elif kind == "fastapi":
        out += st("M0 -11 a11 11 0 1 0 0.1 0", 2.2) + f'<path d="M2 -8 L-5 2 H0 L-2 8 L5 -2 H0Z" transform="translate({f1(cx)} {f1(cy)}) scale({f3(k)})" fill="#fff"/>'
    elif kind == "mysql":
        out += st("M-8 -7 a8 3 0 1 0 16 0 a8 3 0 1 0 -16 0 M-8 -7 v14 a8 3 0 0 0 16 0 v-14 M-8 0 a8 3 0 0 0 16 0")
    else:
        out += icon(kind, x + s * 0.22, y + s * 0.22, s * 0.56, "#fff")
    return out


def stack(d):
    W, H = 1200, 560
    D = Doc(W, H, "hb", r=16, bg="#111115")
    C = Clock(12.0)
    p = D.p
    D.add("".join(f'<circle cx="{14+i*24}" cy="{58+j*24}" r="1" fill="#fff" opacity="0.06"/>' for i in range(50) for j in range(21)))
    D.add(f'<rect width="{W}" height="40" fill="#1b1b21"/><path d="M0 40H{W}" stroke="#000" stroke-opacity="0.5"/>' + traffic(22, 20)
          + text(W / 2, 25, "how-i-build — Freeform", 13, "#c7c7cc", "sans", 600, "middle"))
    nw, nh = 270, 62
    cols_x = {"apps": 60, "api": 465, "data": 870}
    nodes = {
        "ios": ("apps", 92, "iOS & iPadOS", "SwiftUI · UIKit"), "mac": ("apps", 172, "macOS", "SwiftUI · MenuBarExtra"),
        "cli": ("apps", 252, "CLI & CI checks", "Swift · Python · TypeScript"),
        "vapor": ("api", 132, "Vapor", "APIs in Swift"), "fastapi": ("api", 232, "FastAPI", "services in Python"),
        "postgresql": ("data", 92, "PostgreSQL", "relational"), "mysql": ("data", 172, "MySQL", "relational"),
        "sqlite": ("data", 252, "SQLite", "local and embedded"),
    }
    for lane, x in cols_x.items():
        D.add(text(x + 2, 76, {"apps": "APPS", "api": "API", "data": "DATA"}[lane], 11.5, FG3, "sans", 700, extra=' letter-spacing="1.4"'))
    D.add(text(62, 400, "SHIP", 11.5, FG3, "sans", 700, extra=' letter-spacing="1.4"'))
    pos = {k: (cols_x[v[0]], v[1]) for k, v in nodes.items()}
    ship = {"git": (60, 416, "Git", "version control"), "githubactions": (340, 416, "GitHub Actions", "CI and checks"), "docker": (620, 416, "Docker", "containers")}
    sw_, sh_ = 230, 62

    def R(k):
        x, y = pos[k]
        return x + nw, y + nh / 2

    def L(k):
        x, y = pos[k]
        return x, y + nh / 2

    edges = {"e1": ("ios", "vapor"), "e2": ("mac", "vapor"), "e3": ("cli", "fastapi"), "e4": ("vapor", "postgresql"),
             "e5": ("vapor", "mysql"), "e6": ("fastapi", "postgresql"), "e7": ("fastapi", "sqlite")}
    paths = {}
    for eid, (a, b) in edges.items():
        (x0, y0), (x1, y1) = R(a), L(b)
        mx = (x0 + x1) / 2
        paths[eid] = f"M{f1(x0)} {f1(y0)} C{f1(mx)} {f1(y0)} {f1(mx)} {f1(y1)} {f1(x1)} {f1(y1)}"
    gx, gy = ship["git"][0] + sw_, ship["git"][1] + sh_ / 2
    paths["s1"] = f"M{gx} {gy} H{ship['githubactions'][0]}"
    paths["s2"] = f"M{ship['githubactions'][0]+sw_} {gy} H{ship['docker'][0]}"
    dx, dy = ship["docker"][0] + sw_ / 2, ship["docker"][1]
    vx, vy = pos["fastapi"][0] + nw / 2, pos["fastapi"][1] + nh
    paths["s3"] = f"M{dx} {dy} C{dx} {dy-50} {vx} {vy+56} {vx} {vy}"
    for eid, dpath in paths.items():
        D.adddef(f'<path id="{p}-{eid}" d="{dpath}"/>')
        dash = ' stroke-dasharray="4 5"' if eid in ("e5",) else ""
        D.add(f'<path d="{dpath}" stroke="#fff" stroke-opacity="0.16" stroke-width="2" fill="none"{dash}/>')
    D.add(f'<rect x="{f1((R("ios")[0]+L("vapor")[0])/2-46)}" y="{f1((R("ios")[1]+L("vapor")[1])/2-12)}" width="92" height="22" rx="11" fill="#1b1b21" stroke="#fff" stroke-opacity="0.12"/>'
          + text((R("ios")[0] + L("vapor")[0]) / 2, (R("ios")[1] + L("vapor")[1]) / 2 + 3.5, "HTTPS · JSON", 10.5, FG2, "mono", 500, "middle"))
    D.add(f'<rect x="{f1((R("vapor")[0]+L("postgresql")[0])/2-22)}" y="{f1((R("vapor")[1]+L("postgresql")[1])/2-12)}" width="44" height="22" rx="11" fill="#1b1b21" stroke="#fff" stroke-opacity="0.12"/>'
          + text((R("vapor")[0] + L("postgresql")[0]) / 2, (R("vapor")[1] + L("postgresql")[1]) / 2 + 3.5, "SQL", 10.5, FG2, "mono", 500, "middle"))
    mx_, my_ = (dx + vx) / 2, (dy + vy) / 2
    D.add(f'<rect x="{f1(mx_-32)}" y="{f1(my_-11)}" width="64" height="22" rx="11" fill="#1b1b21" stroke="#fff" stroke-opacity="0.12"/>'
          + text(mx_, my_ + 3.5, "deploy", 10.5, FG2, "mono", 500, "middle"))
    flashes = {}

    def packet(eid, t0, t1, rev=False, col="#4da3ff"):
        kp = "1;1;0;0" if rev else "0;0;1;1"
        a, b = f3(C.k(t0)), f3(C.k(t1))
        D.add(f'<g opacity="0">{C.ease("opacity", [(0, 0), (t0 - 0.01, 0), (t0 + 0.05, 1), (t1, 1), (t1 + 0.08, 0)])}'
              f'<animateMotion dur="{C.T}s" repeatCount="indefinite" keyPoints="{kp}" keyTimes="0;{a};{b};1" calcMode="spline" '
              f'keySplines="0 0 1 1;{EASE};0 0 1 1"><mpath href="#{p}-{eid}"/></animateMotion>'
              f'<circle r="10" fill="{col}" opacity="0.22"/><circle r="4.5" fill="{col}"/><circle r="2" fill="#fff"/></g>')

    def flash(key, t):
        flashes.setdefault(key, []).append(t)

    seqs = [(0.3, "e1", "e4", "ios", "vapor", "postgresql"), (4.0, "e3", "e7", "cli", "fastapi", "sqlite"), (6.6, "e2", "e5", "mac", "vapor", "mysql")]
    for t, ea, eb, na, nb, nc in seqs:
        packet(ea, t, t + 0.8); flash(nb, t + 0.8)
        packet(eb, t + 0.85, t + 1.5); flash(nc, t + 1.5)
        packet(eb, t + 1.65, t + 2.3, rev=True, col="#30d158"); flash(nb, t + 2.3)
        packet(ea, t + 2.35, t + 3.1, rev=True, col="#30d158"); flash(na, t + 3.1)
    packet("s1", 9.0, 9.5, col="#ff9f0a"); flash("githubactions", 9.5)
    packet("s2", 9.6, 10.1, col="#ff9f0a"); flash("docker", 10.1)
    packet("s3", 10.2, 11.0, col="#ff9f0a"); flash("fastapi", 11.0); flash("vapor", 11.0)

    def card(key, x, y, w, h, title, sub):
        fl = flashes.get(key, [])
        glow = ""
        if fl:
            pairs = []
            for t in fl:
                pairs += [(t - 0.01, 0), (t + 0.12, 1), (t + 0.9, 0)]
            glow = (f'<rect x="{x-2}" y="{y-2}" width="{w+4}" height="{h+4}" rx="16" stroke="#4da3ff" stroke-width="2" opacity="0">'
                    + C.ease("opacity", [(0, 0)] + pairs) + '</rect>')
        return (f'<rect x="{x}" y="{y+4}" width="{w}" height="{h}" rx="14" fill="#000" opacity="0.35"/>'
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#1c1c23"/>'
                f'<rect x="{x+0.5}" y="{y+0.5}" width="{w-1}" height="{h-1}" rx="13.5" stroke="#fff" stroke-opacity="0.1"/>{glow}'
                + _node_icon(D, key, x + 13, y + 13, 36) + text(x + 62, y + 28, title, 15, FG, "sans", 700)
                + text(x + 62, y + 46, sub, 12.5, FG2, "sans", 500))

    for k, (lane, y, title, sub) in nodes.items():
        x, _ = pos[k]
        D.add(card(k, x, y, nw, nh, title, sub))
    for k, (x, y, title, sub) in ship.items():
        D.add(card(k, x, y, sw_, sh_, title, sub))
    # request log
    lx, ly, lw, lh = 870, 352, 270, 178
    D.add(f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="14" fill="#0b0b0e" stroke="#fff" stroke-opacity="0.1"/>'
          + text(lx + 14, ly + 22, "api.log", 11.5, FG3, "mono", 600)
          + f'<circle cx="{lx+lw-18}" cy="{ly+18}" r="4" fill="#30d158"><animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/></circle>')
    log = [(1.1, [("GET ", "#64d2ff"), ("/v1/projects", "#e5e5ea")]), (1.8, [("  db ", FG3), ("6 rows · 3 ms", FG2)]),
           (3.4, [("200 ", "#30d158"), ("OK · 18 ms", FG2)]), (4.8, [("POST ", "#bf9cff"), ("/checks", "#e5e5ea")]),
           (6.4, [("201 ", "#30d158"), ("Created · 24 ms", FG2)]), (9.5, [("ci ", "#ff9f0a"), ("tests passed", FG2)]),
           (10.1, [("docker ", "#ff9f0a"), ("image built", FG2)]), (11.0, [("deploy ", "#ff9f0a"), ("live ✓", "#30d158")])]
    for i, (t, spans) in enumerate(log):
        sp = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in spans)
        D.add(f'<g opacity="0">{C.show(t, 11.6, fade=0.15)}<text x="{lx+14}" y="{ly+46+i*16.5}" class="mono" font-size="11.5" xml:space="preserve">{sp}</text></g>')
    return D.svg(title="How I build", desc="Apps in SwiftUI talk to APIs in Vapor and FastAPI, backed by PostgreSQL, MySQL and SQLite; Git, GitHub Actions and Docker ship it.")


# ================================================================== Updates (recently pushed)

KIND = {"Apple-Design-Templates": "templates", "LiquidGlassTabBars": "tabbar", "AdaptiveAppShell": "shell",
        "MacMenuBarCommandKit": "menubar", "ResizeLint": "resize", "fontwitness": "fonts", "nativecraft-verify": "xcode",
        "homebrew-tap": "terminal", "LiveActivityDynamicIslandKit": "swift"}


def _ago(iso, today):
    day = dt.date.fromisoformat(iso[:10])
    n = (today - day).days
    if n <= 0:
        return "today"
    if n == 1:
        return "yesterday"
    if n < 7:
        return f"{n} days ago"
    if n < 30:
        return f"{n // 7} week{'s' if n >= 14 else ''} ago"
    m = n // 30
    return f"{m} month{'s' if m > 1 else ''} ago"


def updates(d):
    W, H = 1200, 330
    D = Doc(W, H, "up", r=16, bg="#141418")
    today = dt.date.fromisoformat(d["generated"])
    repos = [r for r in d["repos"] if r.get("pushed") and r["description"] and r["name"].lower() != d["login"].lower()]
    repos.sort(key=lambda r: r["pushed"], reverse=True)
    D.add(text(36, 58, "Updates", 30, FG, "sans", 800, extra=' letter-spacing="-0.6"') + text(36, 82, "Recently pushed repositories", 14, FG2, "sans", 500))
    D.add(f'<rect x="{W-176}" y="38" width="140" height="28" rx="14" fill="#26262d"/><circle cx="{W-158}" cy="52" r="4" fill="#30d158">'
          f'<animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/></circle>' + text(W - 146, 56.5, "updated daily", 12.5, FG2, "sans", 600))
    cw, ch = 548, 98
    for i, r in enumerate(repos[:4]):
        x = 36 + (i % 2) * (cw + 32)
        y = 110 + (i // 2) * (ch + 10)
        kind = KIND.get(r["name"], {"Swift": "swift"}.get(r["language"] or "", "terminal"))
        name = r["name"]
        desc = r["description"].rstrip(".")
        maxw = cw - 96 - 96
        while tw(desc, 13.5, weight=500) > maxw and len(desc) > 8:
            desc = desc[:-2].rstrip(" ,.;:") if not desc.endswith("…") else desc[:-3].rstrip(" ,.;:") + "…"
            if not desc.endswith("…"):
                desc += "…"
        meta = _ago(r["pushed"], today) + (f"  ·  {r['language']}" if r["language"] else "")
        D.add(app_icon(D, kind, x, y + 14, 64)
              + text(x + 82, y + 34, name, 17, FG, "sans", 700, extra=' letter-spacing="-0.2"')
              + text(x + 82, y + 54, meta, 13, FG3, "sans", 500)
              + text(x + 82, y + 76, desc, 13.5, "#c7c7cc", "sans", 500)
              + f'<rect x="{x+cw-78}" y="{y+30}" width="72" height="30" rx="15" fill="#2c2c33"/>' + text(x + cw - 42, y + 50, "OPEN", 13.5, "#0a84ff", "sans", 800, "middle"))
        if i < 2:
            D.add(f'<path d="M{x+82} {y+ch+5}H{x+cw}" stroke="#fff" stroke-opacity="0.08"/>')
    return D.svg(title="Updates", desc="Recently pushed repositories: " + ", ".join(r["name"] for r in repos[:4]) + ".")


# ================================================================== Activity

def _nice(mx):
    for step in (1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500):
        if mx / step <= 4:
            return step, step * (int(mx / step) + 1)
    return 1000, 1000 * (int(mx / 1000) + 1)


def activity(d):
    from panels import _smooth
    W, H = 1200, 500
    D = Doc(W, H, "ac", r=16, bg="#141418")
    C = Clock(14.0)
    p = D.p
    D.add(f'<rect width="{W}" height="38" fill="#1e1e23"/><path d="M0 38H{W}" stroke="#000" stroke-opacity="0.5"/>' + traffic(22, 19)
          + text(W / 2, 24, "Activity — mikonyaa", 13, "#c7c7cc", "sans", 600, "middle"))
    c = d["contrib"]
    D.add(text(40, 104, f"{c['total']:,}", 46, FG, "sans tnum", 800, extra=' letter-spacing="-1.5"')
          + text(40, 130, "contributions in the last 12 months", 14.5, FG2, "sans", 500))
    # what the total is made of (it adds up exactly)
    parts = [("commits", c["commits"], "#30d158"), ("pull requests", c["prs"], "#bf5af2"), ("issues", c["issues"], "#ff9f0a"),
             ("reviews", c["reviews"], "#64d2ff"), ("new repos", c.get("new_repos", 0), "#0a84ff"), ("in private repos", c.get("private", 0), "#636366")]
    known = sum(v for _, v, _ in parts)
    if c["total"] > known:
        parts.append(("other", c["total"] - known, "#3a3a40"))
    parts = [x for x in parts if x[1] > 0]
    bx0, bx1, by = 40, 800, 154
    acc = 0
    for i, (nm, v, col) in enumerate(parts):
        x = bx0 + (bx1 - bx0) * acc / c["total"]
        w = max(2, (bx1 - bx0) * v / c["total"] - 3)
        D.add(f'<rect x="{f1(x)}" y="{by}" width="0" height="10" rx="3" fill="{col}">'
              f'<animate attributeName="width" values="0;{f1(w)}" dur="0.9s" begin="{0.2+i*0.12:.2f}s" fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1"/></rect>')
        acc += v
    lx = bx0
    for nm, v, col in parts:
        lab = f"{v:,} {nm}"
        D.add(f'<circle cx="{f1(lx+5)}" cy="185" r="5" fill="{col}"/>' + text(lx + 15, 189.5, lab, 13, FG2, "sans tnum", 600))
        lx += tw(lab, 13, weight=600) + 32
    # weekly chart
    weeks = c["weeks"]
    vals = [sum(n for _, n, _ in wk) for wk in weeks]
    cx0, cx1, cy0, cy1 = 40, 800, 226, 430
    step, top = _nice(max(vals) or 1)
    k = 0
    while k * step <= top:
        gy = cy1 - (cy1 - cy0) * k * step / top
        D.add(f'<path d="M{cx0} {f1(gy)}H{cx1}" stroke="#fff" stroke-opacity="{0.12 if k == 0 else 0.06}"/>' + text(cx1 + 10, gy + 4, str(k * step), 11, FG3, "sans tnum", 500))
        k += 1
    n = len(vals)
    pts = [(cx0 + (cx1 - cx0) * i / (n - 1), cy1 - (cy1 - cy0) * v / top) for i, v in enumerate(vals)]
    line = _smooth(pts, floor=cy1)
    D.adddef(f'<linearGradient id="{p}-ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#30d158" stop-opacity="0.4"/>'
             f'<stop offset="1" stop-color="#30d158" stop-opacity="0"/></linearGradient>',
             f'<clipPath id="{p}-ch"><rect x="{cx0}" y="{cy0-20}" width="{cx1-cx0}" height="{cy1-cy0+20}"/></clipPath>', f'<path id="{p}-ln" d="{line}"/>')
    D.add(f'<path d="{line} L{cx1} {cy1} L{cx0} {cy1}Z" fill="url(#{p}-ar)"/><path d="{line}" stroke="#30d158" stroke-width="2.4" fill="none" stroke-linejoin="round"/>')
    seen = set()
    for i, wk in enumerate(weeks):
        day = dt.date.fromisoformat(wk[0][0])
        if day.day <= 7 and (day.year, day.month) not in seen and 0 < i < n - 2:
            seen.add((day.year, day.month))
            D.add(text(pts[i][0], cy1 + 22, day.strftime("%b"), 11.5, FG3, "sans", 600, "middle"))
    D.add(f'<g clip-path="url(#{p}-ch)"><g><animateMotion dur="14s" repeatCount="indefinite" calcMode="spline" keyPoints="0;1;1" keyTimes="0;0.9;1" '
          f'keySplines="{EASE};0 0 1 1"><mpath href="#{p}-ln"/></animateMotion>'
          f'<path d="M0 0V400" stroke="#fff" stroke-opacity="0.35" stroke-dasharray="3 4"/><circle r="9" fill="#30d158" opacity="0.25"/>'
          f'<circle r="5" fill="#fff" stroke="#30d158" stroke-width="2.5"/></g></g>')
    # right: most active repositories + streaks
    rx0, rx1 = 870, 1160
    D.add(f'<rect x="{rx0-20}" y="64" width="{rx1-rx0+40}" height="270" rx="14" fill="#1b1b21" stroke="#fff" stroke-opacity="0.07"/>'
          + text(rx0, 94, "Most commits", 14, FG, "sans", 700) + text(rx1, 94, "my repos · 12 months", 12, FG3, "sans", 600, "end"))
    mine = {r["name"] for r in d["repos"]}
    rows = [r for r in c.get("by_repo", []) if r["name"] in mine and r["name"].lower() != d["login"].lower()][:5]
    mx = max([r["commits"] for r in rows] or [1])
    for i, r in enumerate(rows):
        y = 124 + i * 42
        nm = r["name"]
        while tw(nm, 13.5, weight=600) > 200 and len(nm) > 6:
            nm = nm[:-2] + "…" if not nm.endswith("…") else nm[:-2] + "…"
        D.add(f'<circle cx="{rx0+5}" cy="{y-4.5}" r="5" fill="{r.get("color") or "#8e8e93"}"/>' + text(rx0 + 16, y, nm, 13.5, FG, "sans", 600)
              + text(rx1, y, f"{r['commits']}", 13.5, FG, "sans tnum", 700, "end")
              + f'<rect x="{rx0}" y="{y+9}" width="{rx1-rx0}" height="5" rx="2.5" fill="#2c2c33"/>'
              f'<rect x="{rx0}" y="{y+9}" width="0" height="5" rx="2.5" fill="{r.get("color") or "#8e8e93"}" opacity="0.9">'
              f'<animate attributeName="width" values="0;{f1((rx1-rx0)*r["commits"]/mx)}" dur="0.9s" begin="{0.3+i*0.1:.1f}s" fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1"/></rect>')
    longest, current = gh.streaks([(dd, k_) for dd, k_, _ in c["days"]])
    best = max(c["days"], key=lambda t: t[1])
    chips = [(f"{longest} days", "longest streak"), (f"{current} days", "current streak"), (f"{best[1]}", "best day")]
    cw = (rx1 - rx0 + 40 - 16) / 3
    for i, (v, k_) in enumerate(chips):
        x = rx0 - 20 + i * (cw + 8)
        D.add(f'<rect x="{f1(x)}" y="350" width="{f1(cw)}" height="80" rx="14" fill="#1b1b21" stroke="#fff" stroke-opacity="0.07"/>'
              + text(x + cw / 2, 386, v, 20, FG, "sans tnum", 800, "middle") + text(x + cw / 2, 408, k_, 12, FG3, "sans", 600, "middle"))
    D.add(text(40, H - 20, "public data from the GitHub API · private work is counted, never named", 11.5, FG3, "sans", 500)
          + text(W - 24, H - 20, f"updated {d['generated']}", 11.5, FG3, "sans tnum", 500, "end"))
    return D.svg(title="Activity", desc=f"{c['total']} contributions in 12 months: {c['commits']} commits, {c['prs']} pull requests, "
                                          f"{c.get('private', 0)} in private repositories. Weekly chart, most active repositories and streaks.")
