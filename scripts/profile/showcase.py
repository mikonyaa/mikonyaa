"""Stack (what I build with), How I work (three habits, each with proof) and the Xcode console footer."""
from __future__ import annotations

import chibi
from extras import _node_icon
from kit import EASE, FG, FG2, FG3, Clock, Doc, app_icon, esc, f1, f3, icon, squircle, text, tw, traffic

CARD, LINE = "#16161b", "#ffffff"


def tile(x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{CARD}"/>'
            f'<rect x="{x+0.5}" y="{y+0.5}" width="{w-1}" height="{h-1}" rx="21.5" stroke="#fff" stroke-opacity="0.09"/>')


def head(D, kind, x, y, title, sub, glyph=None):
    ic = _node_icon(D, kind, x, y, 38) if glyph is None else glyph
    return ic + text(x + 52, y + 17, title, 19, FG, "sans", 700, extra=' letter-spacing="-0.2"') + text(x + 52, y + 36, sub, 13.5, FG2, "sans", 500)


def chips(items, x, y, maxw, fs=12.5):
    out, cx, cy = [], x, y
    for label, col in items:
        w = tw(label, fs, weight=600) + (30 if col else 20)
        if cx + w > x + maxw:
            cx, cy = x, cy + 34
        out.append(f'<rect x="{f1(cx)}" y="{cy}" width="{f1(w)}" height="27" rx="13.5" fill="#24242b" stroke="#fff" stroke-opacity="0.06"/>')
        if col:
            out.append(f'<circle cx="{f1(cx+13)}" cy="{cy+13.5}" r="4" fill="{col}"/>')
        out.append(text(cx + (23 if col else 10), cy + 18, label, fs, "#d1d1d6", "sans", 600))
        cx += w + 8
    return "".join(out)


def _lang_icon(D, name, x, y, s):
    cols = {"Swift": ("#ffa257", "#f23e2a"), "Python": ("#4b8bbe", "#2b5b84"), "TypeScript": ("#4a90e2", "#2f66c4"),
            "Objective-C": ("#7d8596", "#3c414c"), "SQL": ("#5d8fd1", "#2a4f86")}[name]
    gid = f"{D.p}-li-{name[:3]}"
    D.once(gid, f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{cols[0]}"/><stop offset="1" stop-color="{cols[1]}"/></linearGradient>')
    d = squircle(x, y, s)
    out = f'<path d="{d}" fill="url(#{gid})"/><path d="{d}" stroke="#fff" stroke-opacity="0.2"/>'
    if name == "Swift":
        out += icon("swift", x + s * 0.2, y + s * 0.2, s * 0.6, "#fff")
    elif name == "Python":
        out += icon("python", x + s * 0.2, y + s * 0.2, s * 0.6, "#fff")
    elif name == "TypeScript":
        out += text(x + s * 0.9, y + s * 0.86, "TS", s * 0.44, "#fff", "sans", 800, "end")
    elif name == "Objective-C":
        out += text(x + s / 2, y + s * 0.68, "{ }", s * 0.46, "#fff", "mono", 700, "middle")
    else:
        k = s / 40
        out += (f'<path d="M-8 -7 a8 3 0 1 0 16 0 a8 3 0 1 0 -16 0 M-8 -7 v14 a8 3 0 0 0 16 0 v-14 M-8 0 a8 3 0 0 0 16 0" '
                f'transform="translate({f1(x+s/2)} {f1(y+s/2)}) scale({f3(k)})" stroke="#fff" stroke-width="2.2" fill="none"/>')
    return out


# ------------------------------------------------------------------ device minis for the Apple tile

def _ipad(D, C, x, y):
    w, h = 196, 140
    sel = C.ease("y", [(0, y + 30), (2.0, y + 30), (2.4, y + 50), (4.4, y + 50), (4.8, y + 70), (6.8, y + 70), (7.2, y + 30)])
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#050507" stroke="#3a3a40" stroke-width="1.4"/>'
            f'<rect x="{x+6}" y="{y+6}" width="{w-12}" height="{h-12}" rx="9" fill="#17171c"/>'
            f'<rect x="{x+6}" y="{y+6}" width="58" height="{h-12}" rx="9" fill="#202027"/>'
            f'<rect x="{x+10}" y="{y+30}" width="50" height="16" rx="5" fill="#0a84ff">{sel}</rect>'
            + "".join(f'<rect x="{x+15}" y="{y+36+i*20}" width="{30-i*4}" height="4" rx="2" fill="#fff" opacity="0.8"/>' for i in range(4))
            + "".join(f'<rect x="{x+72+(i%3)*38}" y="{y+16+(i//3)*56}" width="32" height="48" rx="6" fill="#2a2a33"/>' for i in range(6)))


def _mac(D, C, x, y):
    w, h = 236, 146
    drop = C.ease("opacity", [(0, 0), (1.0, 0), (1.3, 1), (5.4, 1), (5.7, 0)])
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#050507" stroke="#3a3a40" stroke-width="1.4"/>'
            f'<rect x="{x+6}" y="{y+6}" width="{w-12}" height="{h-12}" rx="5" fill="#1b2140"/>'
            f'<rect x="{x+6}" y="{y+6}" width="{w-12}" height="11" fill="#000" opacity="0.35"/>'
            + "".join(f'<rect x="{x+14+i*18}" y="{y+10}" width="12" height="3" rx="1.5" fill="#fff" opacity="0.7"/>' for i in range(4))
            + f'<rect x="{x+w-48}" y="{y+8}" width="12" height="7" rx="2" fill="#fff" opacity="0.95"/>'
            f'<g opacity="0">{drop}<rect x="{x+w-104}" y="{y+20}" width="92" height="66" rx="7" fill="#26262d" stroke="#fff" stroke-opacity="0.15"/>'
            + "".join(f'<rect x="{x+w-96}" y="{y+30+i*16}" width="{60-i*10}" height="4" rx="2" fill="#fff" opacity="0.75"/>' for i in range(3))
            + f'<rect x="{x+w-100}" y="{y+42}" width="84" height="14" rx="4" fill="#0a84ff" opacity="0.6"/></g>'
            f'<rect x="{x+20}" y="{y+34}" width="110" height="80" rx="7" fill="#26262d" stroke="#fff" stroke-opacity="0.1"/>'
            + "".join(f'<rect x="{x+30}" y="{y+52+i*14}" width="{80-i*14}" height="4" rx="2" fill="#fff" opacity="0.45"/>' for i in range(4))
            + f'<path d="M{x-14} {y+h} h{w+28} l-10 9 h{-(w+8)}z" fill="#3a3a42"/><rect x="{x+w/2-22}" y="{y+h}" width="44" height="3" rx="1.5" fill="#1d1d22"/>')


def _iphone(D, C, x, y):
    w, h = 84, 172
    iw = C.ease("width", [(0, 30), (2.6, 30), (3.0, 72), (5.6, 72), (6.0, 30)])
    ix = C.ease("x", [(0, x + 27), (2.6, x + 27), (3.0, x + 6), (5.6, x + 6), (6.0, x + 27)])
    ih = C.ease("height", [(0, 10), (2.6, 10), (3.0, 34), (5.6, 34), (6.0, 10)])
    la = C.ease("opacity", [(0, 0), (2.9, 0), (3.1, 1), (5.4, 1), (5.6, 0)])
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="17" fill="#050507" stroke="#3a3a40" stroke-width="1.4"/>'
            f'<rect x="{x+4}" y="{y+4}" width="{w-8}" height="{h-8}" rx="13" fill="#17171c"/>'
            + "".join(f'<rect x="{x+12}" y="{y+56+i*24}" width="{w-24}" height="18" rx="5" fill="#2a2a33"/>' for i in range(4))
            + f'<rect x="{x+27}" y="{y+8}" width="30" height="10" rx="5" fill="#000">{ix}{iw}{ih}</rect>'
            f'<g opacity="0">{la}<circle cx="{x+16}" cy="{y+25}" r="5" fill="#30d158"/>'
            f'<rect x="{x+26}" y="{y+21}" width="26" height="3.5" rx="1.75" fill="#fff" opacity="0.85"/><rect x="{x+26}" y="{y+28}" width="18" height="3" rx="1.5" fill="#fff" opacity="0.5"/>'
            f'<text x="{x+71}" y="{y+29}" class="sans tnum" font-size="8" font-weight="700" fill="#30d158" text-anchor="end">2:31</text></g>'
            f'<rect x="{x+w/2-16}" y="{y+h-10}" width="32" height="3" rx="1.5" fill="#fff" opacity="0.6"/>')


def _watch(D, C, x, y):
    cx, cy, r = x + 30, y + 44, 17
    circ = 2 * 3.14159 * r
    off = C.ease("stroke-dashoffset", [(0, round(circ, 1)), (0.6, round(circ, 1)), (2.6, round(circ * 0.28, 1)), (6.6, round(circ * 0.28, 1)), (7.4, round(circ, 1))])
    return (f'<rect x="{x+14}" y="{y}" width="32" height="14" rx="4" fill="#2a2a30"/><rect x="{x+14}" y="{y+74}" width="32" height="14" rx="4" fill="#2a2a30"/>'
            f'<rect x="{x}" y="{y+10}" width="60" height="68" rx="16" fill="#050507" stroke="#3a3a40" stroke-width="1.4"/>'
            f'<rect x="{x+60}" y="{y+30}" width="4" height="12" rx="2" fill="#3a3a40"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="#3a1414" stroke-width="5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="#ff375f" stroke-width="5" stroke-linecap="round" stroke-dasharray="{f1(circ)}" '
            f'stroke-dashoffset="{f1(circ)}" transform="rotate(-90 {cx} {cy})">{off}</circle>')


def _vision(D, C, x, y):
    flo = C.ease_t("translate", [(0, "0 0"), (3.6, "0 -5"), (7.2, "0 0")])
    return (f'<g>{flo}<rect x="{x}" y="{y}" width="104" height="72" rx="14" fill="#ffffff" opacity="0.13"/>'
            f'<rect x="{x+0.5}" y="{y+0.5}" width="103" height="71" rx="13.5" stroke="#fff" stroke-opacity="0.35"/>'
            + "".join(f'<rect x="{x+10+(i%3)*30}" y="{y+12+(i//3)*28}" width="24" height="22" rx="5" fill="#fff" opacity="0.22"/>' for i in range(6))
            + f'<rect x="{x+36}" y="{y+80}" width="32" height="5" rx="2.5" fill="#fff" opacity="0.5"/></g>'
            f'<path d="M{x+18} {y+120} q34 -18 68 0 q-6 18 -22 16 q-12 -8 -24 0 q-16 2 -22 -16z" fill="#2a2a30" stroke="#55555c"/>')


# ------------------------------------------------------------------ Stack

def stack(d):
    W, H = 1200, 1180
    D = Doc(W, H, "sk", r=0, border=False)
    C = Clock(8.0)
    # languages strip
    D.add(tile(0, 0, W, 76))
    D.add(text(28, 44, "Languages", 15, FG2, "sans", 700))
    x = 140
    for name in ("Swift", "Python", "TypeScript", "Objective-C", "SQL"):
        D.add(_lang_icon(D, name, x, 19, 38) + text(x + 50, 44, name, 17, FG, "sans", 700))
        x += 50 + tw(name, 17, weight=700) + 36
    y0 = 92
    # Apple platforms
    ax, aw, ah = 0, 744, 392
    D.add(tile(ax, y0, aw, ah))
    apple = (f'<path d="M0 -6 C-3 -10 -12 -10 -12 -1 C-12 8 -5 14 -2 14 C0 14 1 13 3 13 C5 13 6 14 8 14 C11 14 14 9 15 5 '
             f'C11 3 10 -3 14 -6 C12 -9 9 -10 6 -10 C3 -10 2 -8 0 -8Z M2 -11 C2 -15 5 -18 8 -18 C8 -14 5 -11 2 -11Z" fill="#fff"/>')
    gl = (f'<path d="{squircle(ax+24, y0+24, 38)}" fill="#2c2c33"/><path d="{squircle(ax+24, y0+24, 38)}" stroke="#fff" stroke-opacity="0.2"/>'
          f'<g transform="translate({ax+42} {y0+45}) scale(0.95)">{apple}</g>')
    D.add(head(D, "", ax + 24, y0 + 24, "Apple platforms", "Native apps in Swift for every Apple device", glyph=gl))
    dy = y0 + 104
    D.add(_ipad(D, C, ax + 26, dy + 20) + _mac(D, C, ax + 240, dy + 6) + _iphone(D, C, ax + 504, dy - 8) + _watch(D, C, ax + 612, dy + 40))
    for lab, cx in (("iPadOS", ax + 124), ("macOS", ax + 358), ("iOS", ax + 546), ("watchOS", ax + 642)):
        D.add(text(cx, dy + 186, lab, 12, FG3, "sans", 600, "middle"))
    D.add(chips([("SwiftUI", "#0a84ff"), ("UIKit", "#0a84ff"), ("Liquid Glass", "#64d2ff"), ("WidgetKit", "#30d158"), ("ActivityKit", "#30d158"),
                 ("MenuBarExtra", "#8e8e93"), ("NavigationSplitView", "#8e8e93"), ("visionOS", "#bf5af2")],
                ax + 24, y0 + ah - 86, aw - 48))
    # Backend
    bx, bw = 760, W - 760
    D.add(tile(bx, y0, bw, ah))
    D.add(head(D, "fastapi", bx + 24, y0 + 24, "Backend", "APIs and services in Python and Swift"))
    code = [
        ("main.py", "fastapi", [[("@app", "#d9c97c"), (".get(", "#e5e5ea"), ('"/projects"', "#ff8170"), (")", "#e5e5ea")],
                               [("async def ", "#ff7ab2"), ("projects", "#67b7a4"), ("(limit: ", "#e5e5ea"), ("int", "#dabaff"), (" = ", "#e5e5ea"), ("10", "#d9c97c"), ("):", "#e5e5ea")],
                               [("    return await ", "#ff7ab2"), ("db.fetch(limit)", "#e5e5ea")]]),
        ("routes.swift", "vapor", [[("app", "#e5e5ea"), (".get(", "#e5e5ea"), ('"projects"', "#ff8170"), (") { req ", "#e5e5ea"), ("async throws in", "#ff7ab2")],
                                   [("    try await ", "#ff7ab2"), ("Project", "#9ef1dd"), (".query(on: req.db).all()", "#e5e5ea")],
                                   [("}", "#e5e5ea")]]),
    ]
    cy = y0 + 86
    for fname, kind, lines in code:
        D.add(f'<rect x="{bx+24}" y="{cy}" width="{bw-48}" height="96" rx="12" fill="#0d0d10" stroke="#fff" stroke-opacity="0.07"/>'
              + _node_icon(D, kind, bx + 36, cy + 10, 18) + text(bx + 62, cy + 23.5, fname, 12, FG2, "mono", 600)
              + text(bx + bw - 38, cy + 23.5, "FastAPI" if kind == "fastapi" else "Vapor", 11.5, FG3, "sans", 600, "end"))
        for i, toks in enumerate(lines):
            sp = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in toks)
            D.add(f'<text x="{bx+38}" y="{cy+48+i*17}" class="mono" font-size="11.5" xml:space="preserve">{sp}</text>')
        cy += 106
    resp = [("GET", "/projects", "200 OK", "18 ms", "#64d2ff"), ("POST", "/checks", "201 Created", "24 ms", "#bf9cff")]
    for i, (m, path, st, ms, col) in enumerate(resp):
        vis = (C.ease("opacity", [(0, 1), (3.6, 1), (3.8, 0), (7.85, 0), (8.0, 1)]) if i == 0 else
               C.ease("opacity", [(0, 0), (3.85, 0), (4.05, 1), (7.6, 1), (7.8, 0)]))
        D.add(f'<g opacity="{1 if i == 0 else 0}">{vis}<circle cx="{bx+32}" cy="{cy+12}" r="4" fill="#30d158"/>'
              f'<text x="{bx+44}" y="{cy+16.5}" class="mono" font-size="12.5" xml:space="preserve"><tspan fill="{col}">{m}</tspan>'
              f'<tspan fill="#e5e5ea"> {path}</tspan><tspan fill="#30d158">  {st}</tspan><tspan fill="{FG3}"> · {ms}</tspan></text></g>')
    D.add(chips([("FastAPI", "#14b8a6"), ("Vapor", "#a77bff"), ("REST", None), ("JSON", None)], bx + 24, y0 + ah - 52, bw - 48))
    # second row: Web · Testing · Data
    y1 = y0 + ah + 16
    rh = 340
    wx_, ww_ = 0, 392
    D.add(tile(wx_, y1, ww_, rh))
    react = (f'<circle cx="0" cy="0" r="2.6" fill="#fff"/>' + "".join(
        f'<ellipse cx="0" cy="0" rx="10" ry="4" stroke="#fff" stroke-width="1.5" fill="none" transform="rotate({a})"/>' for a in (0, 60, 120)))
    rgl = (f'<path d="{squircle(wx_+24, y1+24, 38)}" fill="#20232a"/><path d="{squircle(wx_+24, y1+24, 38)}" stroke="#fff" stroke-opacity="0.2"/>'
           f'<g transform="translate({wx_+43} {y1+43}) scale(1.2)">{react.replace("#fff", "#61dafb")}</g>')
    D.add(head(D, "", wx_ + 24, y1 + 24, "Web", "Fast, accessible front ends", glyph=rgl))
    bx0, by0, bw0, bh0 = wx_ + 24, y1 + 86, ww_ - 48, 166
    D.add(f'<rect x="{bx0}" y="{by0}" width="{bw0}" height="{bh0}" rx="12" fill="#f5f5f7"/>'
          f'<path d="M{bx0} {by0+12}a12 12 0 0 1 12 -12H{bx0+bw0-12}a12 12 0 0 1 12 12V{by0+28}H{bx0}Z" fill="#e3e3e8"/>'
          + "".join(f'<circle cx="{bx0+14+i*12}" cy="{by0+14}" r="4" fill="{c}"/>' for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")))
          + f'<rect x="{bx0+58}" y="{by0+7}" width="{bw0-80}" height="14" rx="7" fill="#fff"/>' + text(bx0 + 68, by0 + 17.5, "localhost:5173", 9.5, "#6e6e73", "mono", 500))
    D.add(f'<rect x="{bx0+14}" y="{by0+40}" width="80" height="8" rx="4" fill="#1d1d1f"/><rect x="{bx0+bw0-60}" y="{by0+38}" width="46" height="14" rx="7" fill="#0a84ff"/>')
    cards_ = [("#ff9f0a", "#ff375f"), ("#5ac8fa", "#5856d6"), ("#30d158", "#0a84ff")]
    cwid = (bw0 - 28 - 16) / 3
    for k, (a, b) in enumerate(cards_):
        gid = f"{D.p}-wc{k}"
        D.adddef(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')
        cxk = bx0 + 14 + k * (cwid + 8)
        D.add(f'<rect x="{f1(cxk)}" y="{by0+62}" width="{f1(cwid)}" height="70" rx="10" fill="url(#{gid})"/>'
              f'<rect x="{f1(cxk+8)}" y="{by0+114}" width="{f1(cwid*0.5)}" height="5" rx="2.5" fill="#fff" opacity="0.9"/>')
    # a hot-module update: the middle card changes, a toast confirms it
    gid = f"{D.p}-wcx"
    D.adddef(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#bf5af2"/><stop offset="1" stop-color="#ff375f"/></linearGradient>')
    cxm = bx0 + 14 + (cwid + 8)
    D.add(f'<rect x="{f1(cxm)}" y="{by0+62}" width="{f1(cwid)}" height="70" rx="10" fill="url(#{gid})" opacity="0">'
          + C.ease("opacity", [(0, 0), (3.0, 0), (3.3, 1), (7.4, 1), (7.8, 0)]) + '</rect>')
    D.add(f'<g opacity="0">{C.ease("opacity", [(0, 0), (2.9, 0), (3.1, 1), (5.6, 1), (5.9, 0)])}'
          f'<rect x="{bx0+bw0-206}" y="{by0+bh0-34}" width="196" height="24" rx="8" fill="#1d1d1f"/>'
          + text(bx0 + bw0 - 197, by0 + bh0 - 18, "[vite] hmr update /src/App.tsx", 9.5, "#30d158", "mono", 500) + '</g>')
    D.add(chips([("React", "#61dafb"), ("Next.js", "#ffffff"), ("Vite", "#bd34fe"), ("Tailwind CSS", "#38bdf8"), ("Motion", "#ffd60a")],
                wx_ + 24, y1 + rh - 74, ww_ - 48))
    # Testing
    tx_, tw_ = 408, 392
    D.add(tile(tx_, y1, tw_, rh))
    D.add(head(D, "cli", tx_ + 24, y1 + 24, "Testing", "Checks that catch problems early"))
    term = [(0.3, [("$ ", FG3), ("npx playwright test", "#e5e5ea")]), (0.9, [("✓ ", "#30d158"), ("end-to-end suite passed", FG2)]),
            (1.8, [("$ ", FG3), ("npx vitest run", "#e5e5ea")]), (2.4, [("✓ ", "#30d158"), ("unit tests passed", FG2)]),
            (3.3, [("$ ", FG3), ("axe audit", "#e5e5ea")]), (3.9, [("✓ ", "#30d158"), ("0 accessibility violations", FG2)]),
            (4.8, [("$ ", FG3), ("resizelint Sources/", "#e5e5ea")]), (5.4, [("RL001 ", "#ff9f0a"), ("Toolbar.swift:42", FG2)])]
    D.add(f'<rect x="{tx_+24}" y="{y1+86}" width="{tw_-48}" height="166" rx="12" fill="#0d0d10" stroke="#fff" stroke-opacity="0.07"/>')
    for i, (t, spans) in enumerate(term):
        sp = "".join(f'<tspan fill="{c}">{esc(s_)}</tspan>' for s_, c in spans)
        D.add(f'<g opacity="0">{C.show(t, 7.6, fade=0.12)}<text x="{tx_+40}" y="{y1+110+i*19}" class="mono" font-size="11.5" xml:space="preserve">{sp}</text></g>')
    D.add(chips([("Playwright", "#2ead33"), ("Vitest", "#729b1b"), ("axe-core", "#663399"), ("XCTest", "#ff9f0a")],
                tx_ + 24, y1 + rh - 74, tw_ - 48))
    # Data
    dx_, dw_ = 816, W - 816
    D.add(tile(dx_, y1, dw_, rh))
    D.add(head(D, "postgresql", dx_ + 24, y1 + 24, "Data", "Relational, local and embedded"))
    D.add(f'<rect x="{dx_+24}" y="{y1+86}" width="{dw_-48}" height="166" rx="12" fill="#0d0d10" stroke="#fff" stroke-opacity="0.07"/>'
          f'<text x="{dx_+40}" y="{y1+112}" class="mono" font-size="11.5" xml:space="preserve"><tspan fill="#ff7ab2">SELECT</tspan><tspan fill="#e5e5ea"> name, stars </tspan>'
          f'<tspan fill="#ff7ab2">FROM</tspan><tspan fill="#e5e5ea"> repos</tspan></text>'
          f'<text x="{dx_+40}" y="{y1+130}" class="mono" font-size="11.5" xml:space="preserve"><tspan fill="#ff7ab2">ORDER BY</tspan><tspan fill="#e5e5ea"> stars </tspan>'
          f'<tspan fill="#ff7ab2">DESC LIMIT</tspan><tspan fill="#d9c97c"> 3</tspan><tspan fill="#e5e5ea">;</tspan></text>'
          f'<path d="M{dx_+40} {y1+144}H{dx_+dw_-40}" stroke="#fff" stroke-opacity="0.1"/>')
    top3 = sorted([r for r in d["repos"] if r["name"].lower() != d["login"].lower()], key=lambda r: -r["stars"])[:3]
    for i, r in enumerate(top3):
        ry = y1 + 168 + i * 24
        nm = r["name"] if len(r["name"]) <= 24 else r["name"][:23] + "…"
        D.add(f'<g opacity="0">{C.show(1.0 + i * 0.35, 7.6, fade=0.15)}'
              f'<rect x="{dx_+34}" y="{ry-16}" width="{dw_-68}" height="22" rx="5" fill="#fff" opacity="{0.04 if i % 2 == 0 else 0}"/>'
              + text(dx_ + 42, ry, nm, 11.5, "#e5e5ea", "mono", 500) + text(dx_ + dw_ - 44, ry, f"{r['stars']}", 11.5, "#d9c97c", "mono", 600, "end") + '</g>')
    D.add(f'<g opacity="0">{C.show(2.3, 7.6, fade=0.15)}' + text(dx_ + 42, y1 + 240, "3 rows · 2 ms", 11, FG3, "mono", 500) + '</g>')
    D.add(chips([("PostgreSQL", "#336791"), ("MySQL", "#f29111"), ("SQLite", "#0f80cc")], dx_ + 24, y1 + rh - 74, dw_ - 48))
    # third row: Swift tooling · Ship
    y2 = y1 + rh + 16
    rh2 = 316
    sx2, sw2 = 0, 592
    D.add(tile(sx2, y2, sw2, rh2))
    D.add(head(D, "", sx2 + 24, y2 + 24, "Swift tooling", "Static analysis, CLIs and project generation",
               glyph=_lang_icon(D, "Swift", sx2 + 24, y2 + 24, 38)))
    code_ = [[("import ", "#ff7ab2"), ("SwiftSyntax", "#e5e5ea")],
             [("final class ", "#ff7ab2"), ("FixedFrameRule", "#5dd8ff"), (": ", "#e5e5ea"), ("SyntaxVisitor", "#dabaff"), (" {", "#e5e5ea")],
             [("  override func ", "#ff7ab2"), ("visit", "#67b7a4"), ("(_ node: ", "#e5e5ea"), ("FunctionCallExprSyntax", "#dabaff"), (")", "#e5e5ea")],
             [("      -> ", "#e5e5ea"), ("SyntaxVisitorContinueKind", "#dabaff"), (" {", "#e5e5ea")],
             [("    if ", "#ff7ab2"), ("node.isFixedWidthFrame { report(.", "#e5e5ea"), ("rl001", "#67b7a4"), (", node) }", "#e5e5ea")],
             [("    return ", "#ff7ab2"), (".visitChildren", "#67b7a4")],
             [("  }", "#e5e5ea")], [("}", "#e5e5ea")]]
    D.add(f'<rect x="{sx2+24}" y="{y2+86}" width="{sw2-48}" height="176" rx="12" fill="#0d0d10" stroke="#fff" stroke-opacity="0.07"/>'
          + text(sx2 + 40, y2 + 106, "Rules/FixedFrameRule.swift", 11, FG3, "mono", 600))
    for i, toks in enumerate(code_):
        sp = "".join(f'<tspan fill="{c}">{esc(s_)}</tspan>' for s_, c in toks)
        D.add(f'<text x="{sx2+40}" y="{y2+128+i*16.5}" class="mono" font-size="11.5" xml:space="preserve">{sp}</text>')
    D.add(f'<rect x="{sx2+40}" y="{y2+128+4*16.5-12}" width="{sw2-80}" height="16" rx="3" fill="#ff9f0a" opacity="0">'
          + C.ease("opacity", [(0, 0), (1.0, 0), (1.3, 0.16), (5.6, 0.16), (6.0, 0)]) + '</rect>')
    D.add(chips([("SwiftSyntax", "#ff7a3d"), ("ArgumentParser", "#ff7a3d"), ("Yams", "#8e8e93"), ("XcodeGen", "#0a84ff"),
                 ("Swift Package Manager", "#ff7a3d"), ("Xcode", "#0a84ff")], sx2 + 24, y2 + rh2 - 42, sw2 - 48)
          if False else chips([("SwiftSyntax", "#ff7a3d"), ("ArgumentParser", "#ff7a3d"), ("XcodeGen", "#0a84ff"),
                               ("SwiftPM", "#ff7a3d"), ("Xcode", "#0a84ff")], sx2 + 24, y2 + rh2 - 42, sw2 - 48))
    # Ship
    sx_, sw_ = 608, W - 608
    D.add(tile(sx_, y2, sw_, rh2))
    D.add(head(D, "githubactions", sx_ + 24, y2 + 24, "Ship", "From commit to release"))
    steps = [("git", "git push", "main"), ("githubactions", "GitHub Actions", "build · test · lint"), ("docker", "Docker", "image ready"),
             ("cli", "Homebrew tap", "brew install resizelint")]
    for i, (k, t1, t2) in enumerate(steps):
        sy = y2 + 90 + i * 44
        t0 = 0.5 + i * 1.1
        D.add(_node_icon(D, k, sx_ + 24, sy, 28) + text(sx_ + 64, sy + 13, t1, 13.5, FG, "sans", 700) + text(sx_ + 64, sy + 28, t2, 11.5, FG3, "mono", 500))
        if i < len(steps) - 1:
            D.add(f'<path d="M{sx_+38} {sy+31} v11" stroke="#fff" stroke-opacity="0.2" stroke-width="2"/>')
        ck = sx_ + sw_ - 40
        D.add(f'<circle cx="{ck}" cy="{sy+14}" r="9" stroke="#3a3a42" stroke-width="2"/>'
              f'<circle cx="{ck}" cy="{sy+14}" r="9" fill="#30d158" opacity="0">{C.ease("opacity", [(0, 0), (t0, 0), (t0 + 0.3, 1), (7.4, 1), (7.8, 0)])}</circle>'
              f'<path d="M{ck-4} {sy+14} l3 3 l5 -6" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" opacity="0">'
              f'{C.ease("opacity", [(0, 0), (t0, 0), (t0 + 0.3, 1), (7.4, 1), (7.8, 0)])}</path>')
    D.add(chips([("Git", "#f05033"), ("GitHub Actions", "#2088ff"), ("Docker", "#2496ed"), ("Homebrew", "#fbb040"), ("AI workflows", "#bf5af2")],
                sx_ + 24, y2 + rh2 - 42, sw_ - 48))
    return D.svg(title="Stack", desc="Languages: Swift, Python, TypeScript, Objective-C, SQL. Apple platforms: SwiftUI, UIKit, Liquid Glass, WidgetKit, ActivityKit, "
                                     "MenuBarExtra. Backend: FastAPI and Vapor. Web: React, Next.js, Vite, Tailwind CSS. Testing: Playwright, Vitest, axe-core, XCTest. "
                                     "Data: PostgreSQL, MySQL, SQLite. Swift tooling: SwiftSyntax, ArgumentParser, XcodeGen. Ship: Git, GitHub Actions, Docker, Homebrew.")


# ------------------------------------------------------------------ How I work

def principles(d):
    W, H = 1200, 360
    D = Doc(W, H, "hw", r=0, border=False)
    C = Clock(8.0)
    tw3 = (W - 32) / 3
    items = [
        ("Native first", "SwiftUI apps that feel at home on", "iPhone, iPad, Mac, Watch and Vision Pro."),
        ("Catch it before users do", "Static analysis and CI checks for the", "bugs that slip through review."),
        ("Automate the second time", "If I do something twice, it becomes a", "script. This README redraws itself."),
    ]
    for i, (title, l1, l2) in enumerate(items):
        x = i * (tw3 + 16)
        D.add(tile(x, 0, tw3, H))
        D.add(text(x + 26, 46, f"0{i+1}", 13, FG3, "mono", 600) + text(x + 26, H - 78, title, 21, FG, "sans", 700, extra=' letter-spacing="-0.3"')
              + text(x + 26, H - 52, l1, 14, FG2, "sans", 500) + text(x + 26, H - 32, l2, 14, FG2, "sans", 500))
        sx, sy, sw, sh = x + 26, 64, tw3 - 52, 176
        D.add(f'<rect x="{f1(sx)}" y="{sy}" width="{f1(sw)}" height="{sh}" rx="14" fill="#0d0d10" stroke="#fff" stroke-opacity="0.07"/>')
        cx = sx + sw / 2
        if i == 0:
            # a floating glass tab bar with a sliding selection
            for k, (a, b) in enumerate((("#ff9f0a", "#ff375f"), ("#5ac8fa", "#5856d6"), ("#30d158", "#0a84ff"))):
                gid = f"{D.p}-n{k}"
                D.adddef(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')
                D.add(f'<rect x="{f1(sx+16+k*((sw-40)/3+4))}" y="{sy+16}" width="{f1((sw-40)/3)}" height="74" rx="10" fill="url(#{gid})" opacity="0.5"/>')
            bw_, bh_ = sw - 60, 50
            bx_, by_ = sx + 30, sy + sh - 66
            tw_ = (bw_ - 8) / 4
            D.add(f'<rect x="{f1(bx_)}" y="{by_+4}" width="{f1(bw_)}" height="{bh_}" rx="25" fill="#000" opacity="0.4"/>'
                  f'<rect x="{f1(bx_)}" y="{by_}" width="{f1(bw_)}" height="{bh_}" rx="25" fill="#2a2a30" opacity="0.92"/>'
                  f'<rect x="{f1(bx_)}" y="{by_}" width="{f1(bw_)}" height="{bh_}" rx="25" stroke="#fff" stroke-opacity="0.25"/>')
            px = [round(bx_ + 4 + tw_ * k, 1) for k in range(4)]
            D.add(f'<rect x="{px[0]}" y="{by_+4}" width="{f1(tw_)}" height="{bh_-8}" rx="21" fill="#fff" opacity="0.16">'
                  + C.ease("x", [(0, px[0]), (1.2, px[0]), (1.6, px[1]), (3.2, px[1]), (3.6, px[2]), (5.2, px[2]), (5.6, px[3]), (7.2, px[3]), (7.6, px[0])]) + '</rect>')
            for k in range(4):
                D.add(f'<circle cx="{f1(px[k]+tw_/2)}" cy="{by_+19}" r="6" stroke="#fff" stroke-width="1.6"/>'
                      f'<rect x="{f1(px[k]+tw_/2-12)}" y="{by_+32}" width="24" height="4" rx="2" fill="#fff" opacity="0.7"/>')
        elif i == 1:
            checks = [("resizelint", "RL001 fixed width", 0.6), ("fontwitness", "fallback font", 1.6), ("tests", "", 2.6)]
            for k, (nm, issue, t0) in enumerate(checks):
                ry = sy + 26 + k * 46
                D.add(f'<rect x="{f1(sx+16)}" y="{ry}" width="{f1(sw-32)}" height="36" rx="9" fill="#1c1c23"/>'
                      + text(sx + 30, ry + 23, nm, 13, "#e5e5ea", "mono", 600))
                if issue:
                    fail = C.ease("opacity", [(0, 0), (t0, 0), (t0 + 0.2, 1), (t0 + 1.6, 1), (t0 + 1.9, 0)])
                    D.add(f'<g opacity="0">{fail}' + text(sx + sw - 54, ry + 23, issue, 11.5, "#ff9f0a", "mono", 500, "end")
                          + f'<circle cx="{f1(sx+sw-34)}" cy="{ry+18}" r="9" fill="#ff453a"/><path d="M{f1(sx+sw-37.5)} {ry+14.5} l7 7 M{f1(sx+sw-30.5)} {ry+14.5} l-7 7" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/></g>')
                ok_at = t0 + (1.9 if issue else 0.3)
                ok = C.ease("opacity", [(0, 0), (ok_at, 0), (ok_at + 0.25, 1), (7.4, 1), (7.8, 0)])
                D.add(f'<g opacity="0">{ok}' + text(sx + sw - 54, ry + 23, "passed", 11.5, "#30d158", "mono", 500, "end")
                      + f'<circle cx="{f1(sx+sw-34)}" cy="{ry+18}" r="9" fill="#30d158"/><path d="M{f1(sx+sw-38.5)} {ry+18} l3 3 l6 -6" stroke="#fff" stroke-width="1.8" fill="none" stroke-linecap="round"/></g>')
        else:
            # a looping arrow around "profile.yml", runs twice a day
            r = 54
            ccx, ccy = cx, sy + sh / 2
            D.add(f'<circle cx="{f1(ccx)}" cy="{f1(ccy)}" r="{r}" stroke="#fff" stroke-opacity="0.08" stroke-width="8"/>'
                  f'<g><animateTransform attributeName="transform" type="rotate" values="0 {f1(ccx)} {f1(ccy)};360 {f1(ccx)} {f1(ccy)}" dur="8s" repeatCount="indefinite"/>'
                  f'<path d="M{f1(ccx)} {f1(ccy-r)} A{r} {r} 0 1 1 {f1(ccx-r*0.87)} {f1(ccy-r*0.5)}" stroke="#30d158" stroke-width="8" fill="none" stroke-linecap="round"/>'
                  f'<path d="M{f1(ccx-r*0.87-9)} {f1(ccy-r*0.5-1)} l9 -11 l5 13z" fill="#30d158"/></g>'
                  + text(ccx, ccy - 2, "profile.yml", 13, FG, "mono", 700, "middle") + text(ccx, ccy + 16, "2× a day", 11.5, FG3, "mono", 500, "middle"))
            D.add(text(sx + 16, sy + 26, "cron", 11, FG3, "mono", 500) + text(sx + sw - 16, sy + 26, "17 3,15 * * *", 11, "#d9c97c", "mono", 500, "end"))
    return D.svg(title="How I work", desc="Native first; catch it before users do; automate the second time.")


# ------------------------------------------------------------------ Xcode console footer, Miko sitting on top

def console(d):
    W, H = 1200, 420
    top = 186
    D = Doc(W, H, "cs", r=0, border=False)
    C = Clock(12.0)
    p = D.p
    D.adddef(f'<clipPath id="{p}-win"><rect x="0" y="{top}" width="{W}" height="{H-top}" rx="16"/></clipPath>')
    D.add(f'<g clip-path="url(#{p}-win)"><rect x="0" y="{top}" width="{W}" height="{H-top}" fill="#1f1f24"/>'
          f'<rect x="0" y="{top}" width="{W}" height="34" fill="#2a2a2e"/><path d="M0 {top+34}H{W}" stroke="#000" stroke-opacity="0.45"/></g>'
          f'<rect x="0.5" y="{top+0.5}" width="{W-1}" height="{H-top-1}" rx="15.5" stroke="#fff" stroke-opacity="0.1"/>')
    # debug bar
    D.add(f'<path d="M22 {top+12} l5 5 l5 -5" stroke="#bdbdc2" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
          f'<path d="M50 {top+11} v12 M54 {top+11} l8 6 l-8 6z" stroke="#bdbdc2" stroke-width="1.5" fill="none" stroke-linejoin="round"/>'
          + text(84, top + 22, "miko", 12, FG2, "sans", 600) + text(118, top + 22, "›", 12, FG3, "sans", 600) + text(130, top + 22, "Thread 1", 12, FG2, "sans", 600)
          + f'<rect x="{W-220}" y="{top+8}" width="200" height="19" rx="6" fill="#1c1c1f"/>' + text(W - 206, top + 21.5, "All Output", 11.5, FG2, "sans", 600)
          + f'<path d="M{W-34} {top+15} l3.5 3.5 l3.5 -3.5" stroke="#8e8e93" stroke-width="1.4" fill="none"/>')
    lines = [
        (0.4, [("▶ ", "#30d158"), ("visitor.scroll(to: .bottom)", "#e5e5ea")]),
        (1.2, [("// it was supposed to be a quick stop.", "#7f8c98")]),
        (2.4, [("(lldb) ", "#8e8e93"), ("po miko.contacts", "#e5e5ea")]),
        (3.0, [("▿ 2 elements", "#e5e5ea")]),
        (3.3, [('  - "t.me/mikonyaa"', "#ff8170")]),
        (3.6, [('  - "dev.miko@icloud.com"', "#ff8170")]),
        (4.8, [("Thanks for stopping by. ", "#e5e5ea"), ("Program ended with exit code: 0", "#8e8e93")]),
    ]
    for i, (t, spans) in enumerate(lines):
        sp = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in spans)
        D.add(f'<g opacity="0">{C.show(t, 11.4, fade=0.12)}<text x="28" y="{top+66+i*24}" class="mono" font-size="14" xml:space="preserve">{sp}</text></g>')
    # caret after the last line
    D.add(f'<rect x="28" y="{top+66+7*24-13}" width="8" height="16" fill="#e5e5ea" opacity="0.8">'
          f'<animate attributeName="opacity" values="0.8;0.8;0;0;0.8" keyTimes="0;0.45;0.5;0.95;1" dur="1.1s" repeatCount="indefinite"/></rect>')
    # Miko sits on the window's top edge, legs over the console
    s = 0.86
    hx = W - 420
    hy = top - 130 * s + 4
    D.add(f'<ellipse cx="{hx}" cy="{top+3}" rx="64" ry="6" fill="#000" opacity="0.3"/>' + chibi.sitting(hx, hy, s, p + "me"))
    return D.svg(title="Thanks for stopping by", desc="An Xcode console: visitor.scroll(to: .bottom); it was supposed to be a quick stop; "
                                                      "po miko.contacts lists t.me/mikonyaa and dev.miko@icloud.com. Miko sits on top of the window with a laptop.")
