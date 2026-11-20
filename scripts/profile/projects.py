"""Project cards: each one shows a small, working-looking piece of the project's UI.
600 x 400, dark, one gentle loop per card (8 s), no filters."""
from __future__ import annotations

from kit import EASE, FG, FG2, FG3, Clock, Doc, app_icon, esc, f1, f3, squircle, text, tw

CW, CH = 600, 400
SX, SY, SW, SH = 16, 16, 568, 248
T = 8.0

PROJECTS = [
    dict(key="apple-design-templates", repo="Apple-Design-Templates", icon="templates", tint="#2f6bff", lang=("Swift", "#F05138"),
         title="Apple Design Templates", kind="SwiftUI templates for Apple platforms",
         desc="Curated templates for polished Apple-platform interfaces."),
    dict(key="liquid-glass-tab-bars", repo="LiquidGlassTabBars", icon="tabbar", tint="#7b4dff", lang=("Swift", "#F05138"),
         title="Liquid Glass Tab Bars", kind="Native, floating and morphing tab bars",
         desc="Three tab bar patterns for SwiftUI, accessibility built in."),
    dict(key="adaptive-app-shell", repo="AdaptiveAppShell", icon="shell", tint="#0fb5a6", lang=("Swift", "#F05138"),
         title="Adaptive App Shell", kind="iPhone tabs, iPad sidebar and inspector",
         desc="Per-tab navigation, deep links and an optional inspector."),
    dict(key="menu-bar-command-kit", repo="MacMenuBarCommandKit", icon="menubar", tint="#8a93a8", lang=("Swift", "#F05138"),
         title="Menu Bar Command Kit", kind="A macOS menu bar app with a command palette",
         desc="Menu bar controls, settings and keyboard-first command search."),
    dict(key="resizelint", repo="ResizeLint", icon="resize", tint="#22c55e", lang=("Swift", "#F05138"),
         title="ResizeLint", kind="Static analysis for resizable Swift apps",
         desc="Finds layout code that breaks when a window is resized."),
    dict(key="fontwitness", repo="fontwitness", icon="fonts", tint="#ff8a3d", lang=("TypeScript", "#3178c6"),
         title="FontWitness", kind="Typography checks for Chromium",
         desc="Shows the fonts that actually rendered; fails CI on a fallback."),
]


def _stage(D, tint):
    p = D.p
    D.adddef(f'<radialGradient id="{p}-glow" cx="0.5" cy="0.35" r="0.7"><stop offset="0" stop-color="{tint}" stop-opacity="0.38"/>'
             f'<stop offset="1" stop-color="{tint}" stop-opacity="0"/></radialGradient>',
             f'<clipPath id="{p}-st"><rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="16"/></clipPath>')
    dots = "".join(f'<circle cx="{SX+14+i*22}" cy="{SY+14+j*22}" r="0.9" fill="#fff" opacity="0.06"/>' for i in range(26) for j in range(11))
    return (f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="16" fill="#0d0d11"/>'
            f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="16" fill="url(#{p}-glow)"/>{dots}')


def bar(x, y, w, h=5, c="#fff", op=0.25, r=None):
    return f'<rect x="{f1(x)}" y="{f1(y)}" width="{f1(w)}" height="{h}" rx="{r if r is not None else h/2}" fill="{c}" opacity="{op}"/>'


def phone(x, y, w, h, inner, r=18):
    return (f'<rect x="{x}" y="{y+5}" width="{w}" height="{h}" rx="{r}" fill="#000" opacity="0.4"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#050507" stroke="#3a3a40" stroke-width="1.5"/>'
            f'<rect x="{x+4}" y="{y+4}" width="{w-8}" height="{h-8}" rx="{r-4}" fill="#16161b"/>{inner}'
            f'<rect x="{x+w/2-14}" y="{y+8}" width="28" height="8" rx="4" fill="#000"/>')


# ------------------------------------------------------------------ previews

def p_templates(D, C):
    out = []
    pw, ph = 104, 212
    xs = [SX + 40 + i * 128 for i in range(4)]
    y0 = SY + 22
    screens = []
    # onboarding
    x = xs[0]
    D.adddef(f'<linearGradient id="{D.p}-ob" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5ac8fa"/><stop offset="1" stop-color="#5856d6"/></linearGradient>')
    screens.append(f'<rect x="{x+30}" y="{y0+44}" width="44" height="44" rx="12" fill="url(#{D.p}-ob)"/>'
                   + bar(x + 22, y0 + 102, 60, 7, "#fff", 0.85) + bar(x + 16, y0 + 116, 72, 4) + bar(x + 24, y0 + 125, 56, 4)
                   + "".join(f'<circle cx="{x+44+i*8}" cy="{y0+160}" r="2.4" fill="#fff" opacity="{0.9 if i == 0 else 0.3}"/>' for i in range(3))
                   + f'<rect x="{x+14}" y="{y0+174}" width="76" height="20" rx="10" fill="#0a84ff"/>' + bar(x + 36, y0 + 182, 32, 4, "#fff", 0.9))
    # settings
    x = xs[1]
    rows = ""
    for i, c in enumerate(("#ff9f0a", "#30d158", "#0a84ff", "#ff375f", "#bf5af2")):
        ry = y0 + 46 + i * 26
        on = i in (1, 2)
        rows += (f'<rect x="{x+14}" y="{ry}" width="14" height="14" rx="4" fill="{c}"/>' + bar(x + 34, ry + 5, 30, 4, "#fff", 0.5)
                 + f'<rect x="{x+70}" y="{ry+1}" width="22" height="13" rx="6.5" fill="{"#30d158" if on else "#3a3a3c"}"/>'
                 f'<circle cx="{x+(85 if on else 77)}" cy="{ry+7.5}" r="5" fill="#fff"/>')
    screens.append(bar(x + 14, y0 + 26, 50, 8, "#fff", 0.9) + f'<rect x="{x+8}" y="{y0+38}" width="{pw-16}" height="134" rx="10" fill="#22222a"/>' + rows)
    # paywall
    x = xs[2]
    D.adddef(f'<linearGradient id="{D.p}-pw" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff9f0a"/><stop offset="1" stop-color="#ff375f"/></linearGradient>')
    plans = "".join(f'<rect x="{x+12}" y="{y0+110+i*26}" width="80" height="20" rx="7" fill="#22222a" stroke="{"#0a84ff" if i == 1 else "#3a3a40"}" stroke-width="1.3"/>'
                    + bar(x + 20, y0 + 118 + i * 26, 30, 4, "#fff", 0.6) + bar(x + 70, y0 + 118 + i * 26, 14, 4, "#fff", 0.4) for i in range(2))
    screens.append(f'<rect x="{x+10}" y="{y0+26}" width="84" height="74" rx="12" fill="url(#{D.p}-pw)"/>'
                   + f'<path d="M{x+52} {y0+44} l5 10 l11 1.5 l-8 7.5 l2 11 l-10 -5.3 l-10 5.3 l2 -11 l-8 -7.5 l11 -1.5z" fill="#fff" opacity="0.95"/>'
                   + plans + f'<rect x="{x+12}" y="{y0+170}" width="80" height="22" rx="11" fill="#fff"/>' + bar(x + 34, y0 + 179, 36, 4, "#000", 0.7))
    # widgets
    x = xs[3]
    tiles = [("#5ac8fa", "#007aff"), ("#ffd60a", "#ff9f0a"), ("#30d158", "#00a86b"), ("#bf5af2", "#5e5ce6")]
    tl = ""
    for i, (a, b) in enumerate(tiles):
        gid = f"{D.p}-wd{i}"
        D.adddef(f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')
        tx, ty = x + 12 + (i % 2) * 42, y0 + 30 + (i // 2) * 42
        tl += f'<rect x="{tx}" y="{ty}" width="38" height="38" rx="10" fill="url(#{gid})"/>' + bar(tx + 6, ty + 26, 18, 4, "#fff", 0.85)
    tl += f'<rect x="{x+12}" y="{y0+118}" width="80" height="58" rx="12" fill="#22222a"/>'
    tl += "".join(f'<rect x="{x+20+i*12}" y="{y0+164-hh}" width="7" height="{hh}" rx="2" fill="#30d158" opacity="0.85"/>' for i, hh in enumerate((14, 26, 20, 34, 28, 38)))
    screens.append(tl)
    for i, (x, sc) in enumerate(zip(xs, screens)):
        t0 = i * 2.0
        lift = C.ease_t("translate", [(0, "0 0"), (t0, "0 0"), (t0 + 0.45, "0 -8"), (t0 + 1.75, "0 -8"), (t0 + 2.2, "0 0")])
        ring = C.ease("opacity", [(0, 0), (t0, 0), (t0 + 0.45, 1), (t0 + 1.75, 1), (t0 + 2.2, 0)])
        out.append(f'<g>{lift}{phone(x, y0, pw, ph, sc)}'
                   f'<rect x="{x-4}" y="{y0-4}" width="{pw+8}" height="{ph+8}" rx="22" stroke="#4d8dff" stroke-width="2.2" opacity="0">{ring}</rect></g>')
    return "".join(out)


def p_tabbar(D, C):
    p = D.p
    out = []
    # content behind the bar: a feed of colourful cards
    cols = [("#ff9f0a", "#ff375f"), ("#5ac8fa", "#5856d6"), ("#30d158", "#0a84ff"), ("#bf5af2", "#ff375f"), ("#ffd60a", "#30d158"), ("#64d2ff", "#bf5af2")]
    for i, (a, b) in enumerate(cols):
        gid = f"{p}-fc{i}"
        D.adddef(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')
        cx, cy = SX + 34 + (i % 3) * 170, SY + 24 + (i // 3) * 104
        out.append(f'<rect x="{cx}" y="{cy}" width="156" height="92" rx="14" fill="url(#{gid})" opacity="0.55"/>'
                   + bar(cx + 12, cy + 64, 70, 6, "#fff", 0.8) + bar(cx + 12, cy + 76, 44, 4, "#fff", 0.5))
    # dim lower part, like content scrolling under the bar
    D.adddef(f'<linearGradient id="{p}-fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d0d11" stop-opacity="0"/><stop offset="1" stop-color="#0d0d11" stop-opacity="0.9"/></linearGradient>')
    out.append(f'<rect x="{SX}" y="{SY+120}" width="{SW}" height="{SH-120}" fill="url(#{p}-fade)"/>')
    # floating glass bar that morphs into a compact pill and back
    bw, bh = 340, 64
    bx, by = SX + (SW - bw) / 2, SY + SH - bh - 22
    cbx, cbw = SX + SW / 2 - 110, 150
    x_anim = C.ease("x", [(0, bx), (5.0, bx), (5.5, cbx), (6.9, cbx), (7.45, bx)])
    w_anim = C.ease("width", [(0, bw), (5.0, bw), (5.5, cbw), (6.9, cbw), (7.45, bw)])
    out.append(f'<rect x="{bx}" y="{by+5}" width="{bw}" height="{bh}" rx="32" fill="#000" opacity="0.45">{x_anim}{w_anim}</rect>'
               f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="32" fill="#2a2a30" opacity="0.88">{x_anim}{w_anim}</rect>'
               f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="32" fill="#fff" opacity="0.06">{x_anim}{w_anim}</rect>'
               f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="32" stroke="#fff" stroke-opacity="0.28">{x_anim}{w_anim}</rect>')
    tw_ = (bw - 10) / 4
    tabs = [("Home", "M-7 1 L0 -6 L7 1 M-5 -1 V7 H5 V-1"), ("Library", "M-7 -6 h14 v13 h-14z M-7 -2 h14"),
            ("Stats", "M-7 7 v-5 M-2 7 v-10 M3 7 v-7 M8 7 v-13"), ("Profile", "M-5 -2 a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0 M-8 9 q8 -8 16 0")]
    # selection pill: Home → Library → Stats → (compact) → Home
    px = [bx + 5 + tw_ * i for i in range(4)]
    pill_x = C.ease("x", [(0, px[0]), (1.0, px[0]), (1.5, px[1]), (2.6, px[1]), (3.1, px[2]), (4.4, px[2]), (4.9, px[0]),
                          (5.0, px[0]), (5.5, cbx + 5), (6.9, cbx + 5), (7.45, px[0])])
    pill_w = C.ease("width", [(0, tw_), (1.0, tw_), (1.25, tw_ * 1.35), (1.5, tw_), (2.6, tw_), (2.85, tw_ * 1.35), (3.1, tw_),
                              (4.4, tw_), (4.65, tw_ * 1.5), (4.9, tw_), (5.0, tw_), (5.5, cbw - 10), (6.9, cbw - 10), (7.45, tw_)])
    out.append(f'<rect x="{px[0]}" y="{by+5}" width="{tw_}" height="{bh-10}" rx="27" fill="#fff" opacity="0.16">{pill_x}{pill_w}</rect>')
    icons_vis = C.ease("opacity", [(0, 1), (5.0, 1), (5.25, 0), (7.1, 0), (7.45, 1)])
    ic = []
    for i, (lab, g) in enumerate(tabs):
        cx = bx + 5 + tw_ * i + tw_ / 2
        ic.append(f'<path d="{g}" transform="translate({f1(cx)} {by+24})" stroke="#fff" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                  + text(cx, by + 50, lab, 11, "#e5e5ea", "sans", 600, "middle"))
    out.append(f'<g>{icons_vis}{"".join(ic)}</g>')
    comp = C.ease("opacity", [(0, 0), (5.3, 0), (5.6, 1), (6.8, 1), (7.1, 0)])
    out.append(f'<g opacity="0">{comp}<path d="{tabs[0][1]}" transform="translate({f1(cbx+38)} {by+32})" stroke="#fff" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
               + text(cbx + 58, by + 37, "Home", 13, FG, "sans", 600) +
               f'<circle cx="{f1(cbx+cbw+42)}" cy="{by+32}" r="30" fill="#2a2a30" stroke="#fff" stroke-opacity="0.28"/>'
               f'<circle cx="{f1(cbx+cbw+40)}" cy="{by+30}" r="7" stroke="#fff" stroke-width="1.8"/><path d="M{f1(cbx+cbw+45)} {by+35} l5 5" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/></g>')
    # labels for the three styles
    lab = C.ease("opacity", [(0, 1), (4.9, 1), (5.1, 0), (7.3, 0), (7.5, 1)])
    chip = lambda s: (f'<rect x="{SX+14}" y="{SY+14}" width="{tw(s, 12, True)+24}" height="24" rx="12" fill="#000" opacity="0.55"/>'
                      + text(SX + 26, SY + 30, s, 12, "#e5e5ea", "mono", 500))
    out.append(f'<g>{lab}{chip(".floating")}</g>')
    out.append(f'<g opacity="0">{C.ease("opacity", [(0, 0), (5.2, 0), (5.4, 1), (7.0, 1), (7.2, 0)])}{chip(".morphing")}</g>')
    return "".join(out)


def p_shell(D, C):
    out = []
    # iPad (landscape)
    ix, iy, iw, ih = SX + 30, SY + 26, 340, 200
    out.append(f'<rect x="{ix}" y="{iy+5}" width="{iw}" height="{ih}" rx="18" fill="#000" opacity="0.4"/>'
               f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="18" fill="#050507" stroke="#3a3a40" stroke-width="1.5"/>'
               f'<rect x="{ix+7}" y="{iy+7}" width="{iw-14}" height="{ih-14}" rx="12" fill="#16161b"/>')
    sbw = 92
    out.append(f'<rect x="{ix+7}" y="{iy+7}" width="{sbw}" height="{ih-14}" rx="12" fill="#1f1f26"/>' + bar(ix + 18, iy + 20, 40, 7, "#fff", 0.85))
    items = ["Inbox", "Today", "Projects", "Archive"]
    sel_y = [iy + 34 + i * 24 for i in range(4)]
    sel = C.ease("y", [(0, sel_y[0]), (1.6, sel_y[0]), (2.0, sel_y[1]), (3.6, sel_y[1]), (4.0, sel_y[2]), (5.6, sel_y[2]), (6.0, sel_y[3]), (7.4, sel_y[3]), (7.8, sel_y[0])])
    out.append(f'<rect x="{ix+12}" y="{sel_y[0]}" width="{sbw-10}" height="20" rx="6" fill="#0a84ff">{sel}</rect>')
    for i, it in enumerate(items):
        out.append(f'<circle cx="{ix+22}" cy="{sel_y[i]+10}" r="3.5" fill="#fff" opacity="0.8"/>' + text(ix + 31, sel_y[i] + 14, it, 10.5, "#f2f2f7", "sans", 600))
    # content grid
    cx0 = ix + 7 + sbw + 10
    for r in range(3):
        for c in range(3):
            gx, gy = cx0 + c * 46, iy + 18 + r * 58
            out.append(f'<rect x="{gx}" y="{gy}" width="40" height="50" rx="7" fill="#2a2a33"/>' + bar(gx + 6, gy + 34, 22, 4, "#fff", 0.4))
    # inspector slides in and out
    insp = C.ease_t("translate", [(0, "0 0"), (2.8, "0 0"), (3.3, "90 0"), (5.2, "90 0"), (5.7, "0 0")])
    D.adddef(f'<clipPath id="{D.p}-ipad"><rect x="{ix+7}" y="{iy+7}" width="{iw-14}" height="{ih-14}" rx="12"/></clipPath>')
    out.append(f'<g clip-path="url(#{D.p}-ipad)"><g>{insp}<rect x="{ix+iw-7-88}" y="{iy+7}" width="88" height="{ih-14}" fill="#23232b"/>'
               f'<path d="M{ix+iw-7-88} {iy+7}V{iy+ih-7}" stroke="#000" stroke-opacity="0.5"/>'
               + bar(ix + iw - 86, iy + 22, 44, 6, "#fff", 0.8) + "".join(bar(ix + iw - 86, iy + 40 + k * 16, 66 - (k % 2) * 18, 4) for k in range(6))
               + f'<rect x="{ix+iw-86}" y="{iy+ih-40}" width="70" height="20" rx="6" fill="#0a84ff" opacity="0.85"/></g></g>')
    # iPhone (compact): same app as tabs
    px, py, pw, ph = SX + 410, SY + 18, 112, 214
    inner = (bar(px + 14, py + 30, 48, 8, "#fff", 0.9) + "".join(
        f'<rect x="{px+12}" y="{py+48+k*34}" width="{pw-24}" height="28" rx="8" fill="#2a2a33"/>' + bar(px + 20, py + 60 + k * 34, 40, 4, "#fff", 0.45)
        for k in range(4)))
    tabx = [px + 14 + i * 22 for i in range(4)]
    tsel = C.ease("x", [(0, tabx[0]), (1.6, tabx[0]), (2.0, tabx[1]), (3.6, tabx[1]), (4.0, tabx[2]), (5.6, tabx[2]), (6.0, tabx[3]), (7.4, tabx[3]), (7.8, tabx[0])])
    inner += (f'<rect x="{px+10}" y="{py+ph-40}" width="{pw-20}" height="26" rx="13" fill="#2a2a30" stroke="#fff" stroke-opacity="0.2"/>'
              f'<rect x="{tabx[0]}" y="{py+ph-37}" width="20" height="20" rx="10" fill="#0a84ff">{tsel}</rect>'
              + "".join(f'<circle cx="{tx+10}" cy="{py+ph-27}" r="3" fill="#fff"/>' for tx in tabx))
    out.append(phone(px, py, pw, ph, inner, r=20))
    out.append(text(ix + iw / 2, SY + SH - 8, "regular · sidebar + inspector", 11, FG3, "mono", 500, "middle")
               + text(px + pw / 2, SY + SH - 8, "compact · tabs", 11, FG3, "mono", 500, "middle"))
    return "".join(out)


def p_menubar(D, C):
    out = []
    # menu bar strip
    my = SY + 14
    out.append(f'<rect x="{SX+14}" y="{my}" width="{SW-28}" height="26" rx="8" fill="#1d1d24"/>'
               + text(SX + 30, my + 17.5, "Finder", 12, FG, "sans", 700) + text(SX + 84, my + 17.5, "File   Edit   View   Go", 12, "#d1d1d6", "sans", 500))
    ix = SX + SW - 150
    out.append(f'<rect x="{ix-11}" y="{my+3}" width="24" height="20" rx="5" fill="#fff" opacity="0.18"/>'
               + text(ix + 1, my + 18, "⌘", 13, FG, "sans", 700, "middle") + text(SX + SW - 28, my + 17.5, "Sat 09:41", 12, FG, "sans", 600, "end"))
    # dropdown under the status item
    dx, dy, dw, dh = ix - 160, my + 32, 206, 178
    rows = [("Run checks", "⌘R", "#30d158"), ("Open dashboard", "⌘D", "#0a84ff"), ("Quick note", "⌘N", "#ff9f0a"), ("Settings…", "⌘,", "#8e8e93")]
    drop = (f'<rect x="{dx}" y="{dy+4}" width="{dw}" height="{dh}" rx="12" fill="#000" opacity="0.4"/>'
            f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="12" fill="#26262d" stroke="#fff" stroke-opacity="0.14"/>'
            + text(dx + 14, dy + 24, "Command Kit", 12.5, FG, "sans", 700)
            + f'<rect x="{dx+dw-46}" y="{dy+12}" width="32" height="18" rx="9" fill="#30d158"/><circle cx="{dx+dw-23}" cy="{dy+21}" r="7" fill="#fff"/>'
            + f'<path d="M{dx+10} {dy+38}H{dx+dw-10}" stroke="#fff" stroke-opacity="0.1"/>')
    hy = [dy + 46 + i * 30 for i in range(4)]
    drop += f'<rect x="{dx+6}" y="{hy[0]}" width="{dw-12}" height="26" rx="6" fill="#0a84ff">' + C.ease("y", [(0, hy[0]), (1.2, hy[0]), (1.5, hy[1]), (2.6, hy[1]), (2.9, hy[2]), (3.9, hy[2]), (4.2, hy[0])]) + '</rect>'
    for i, (lab, key, col) in enumerate(rows):
        drop += (f'<circle cx="{dx+20}" cy="{hy[i]+13}" r="5" fill="{col}"/>' + text(dx + 32, hy[i] + 17.5, lab, 12, FG, "sans", 500)
                 + text(dx + dw - 14, hy[i] + 17.5, key, 12, "#c7c7cc", "sans", 500, "end"))
    out.append(f'<g>{C.ease("opacity", [(0, 1), (4.6, 1), (4.9, 0), (7.6, 0), (7.9, 1)])}{drop}</g>')
    # command palette appears while the dropdown closes
    cx, cy, cw, chh = SX + 70, SY + 58, 300, 170
    pal = (f'<rect x="{cx}" y="{cy+6}" width="{cw}" height="{chh}" rx="14" fill="#000" opacity="0.45"/>'
           f'<rect x="{cx}" y="{cy}" width="{cw}" height="{chh}" rx="14" fill="#26262d" stroke="#fff" stroke-opacity="0.16"/>'
           f'<circle cx="{cx+22}" cy="{cy+24}" r="6" stroke="#c7c7cc" stroke-width="1.7"/><path d="M{cx+26.5} {cy+28.5} l5 5" stroke="#c7c7cc" stroke-width="1.7" stroke-linecap="round"/>')
    q = "deploy"
    qw = len(q) * 15 * 0.55
    D.adddef(f'<clipPath id="{D.p}-q"><rect x="{cx+40}" y="{cy+10}" height="24" width="0">'
             f'<animate attributeName="width" values="0;0;{f1(qw*0.17)};{f1(qw*0.34)};{f1(qw*0.5)};{f1(qw*0.67)};{f1(qw*0.84)};{f1(qw+2)};{f1(qw+2)};0" '
             f'keyTimes="0;{f3(4.9/T)};{f3(5.05/T)};{f3(5.2/T)};{f3(5.35/T)};{f3(5.5/T)};{f3(5.65/T)};{f3(5.8/T)};{f3(7.6/T)};1" calcMode="discrete" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>')
    pal += f'<text x="{cx+40}" y="{cy+29}" class="sans" font-size="15" fill="{FG}" clip-path="url(#{D.p}-q)">{q}</text>'
    pal += f'<path d="M{cx} {cy+44}H{cx+cw}" stroke="#fff" stroke-opacity="0.1"/>'
    res = [("Deploy to staging", "↵"), ("Deploy to production", "⌘↵"), ("Deploy log", "")]
    ry = [cy + 52 + i * 34 for i in range(3)]
    pal += f'<rect x="{cx+8}" y="{ry[0]}" width="{cw-16}" height="30" rx="7" fill="#0a84ff">' + C.ease("y", [(0, ry[0]), (6.4, ry[0]), (6.7, ry[1]), (7.6, ry[1]), (7.8, ry[0])]) + '</rect>'
    for i, (lab, key) in enumerate(res):
        pal += (f'<rect x="{cx+18}" y="{ry[i]+7}" width="16" height="16" rx="4" fill="#3a3a44"/>' + text(cx + 44, ry[i] + 20, lab, 12.5, FG, "sans", 500)
                + text(cx + cw - 20, ry[i] + 20, key, 12, "#e5e5ea", "sans", 500, "end"))
    out.append(f'<g opacity="0">{C.ease("opacity", [(0, 0), (4.7, 0), (5.0, 1), (7.6, 1), (7.9, 0)])}{pal}</g>')
    return "".join(out)


def p_resize(D, C):
    out = []
    # a window whose width breathes; at narrow widths the fixed-width toolbar overflows
    wx, wy, wh = SX + 26, SY + 30, 186
    wide, narrow = 300, 176
    wa = C.ease("width", [(0, wide), (1.2, wide), (2.6, narrow), (4.6, narrow), (6.0, wide)])
    D.adddef(f'<clipPath id="{D.p}-rw"><rect x="{wx}" y="{wy}" width="{wide}" height="{wh}" rx="12">{wa}</rect></clipPath>')
    out.append(f'<rect x="{wx}" y="{wy+5}" width="{wide}" height="{wh}" rx="12" fill="#000" opacity="0.4">{wa}</rect>'
               f'<rect x="{wx}" y="{wy}" width="{wide}" height="{wh}" rx="12" fill="#1f1f26" stroke="#fff" stroke-opacity="0.15">{wa}</rect>')
    inner = ("".join(f'<circle cx="{wx+16+i*14}" cy="{wy+15}" r="4.5" fill="{c}"/>' for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")))
             + f'<path d="M{wx} {wy+30}H{wx+wide}" stroke="#000" stroke-opacity="0.5"/>'
             + f'<rect x="{wx+12}" y="{wy+42}" width="120" height="26" rx="7" fill="#0a84ff"/>' + bar(wx + 26, wy + 53, 64, 5, "#fff", 0.9)
             + f'<rect x="{wx+140}" y="{wy+42}" width="120" height="26" rx="7" fill="#3a3a44"/>' + bar(wx + 154, wy + 53, 60, 5, "#fff", 0.6)
             + "".join(bar(wx + 12, wy + 84 + k * 16, 200 - (k % 3) * 40, 5) for k in range(5)))
    out.append(f'<g clip-path="url(#{D.p}-rw)">{inner}</g>')
    # red overflow marker + resize handle
    warn = C.ease("opacity", [(0, 0), (2.2, 0), (2.5, 1), (4.7, 1), (5.0, 0)])
    out.append(f'<g opacity="0">{warn}<rect x="{wx+140}" y="{wy+40}" width="124" height="30" rx="8" stroke="#ff453a" stroke-width="2" stroke-dasharray="5 4"/>'
               f'<path d="M{wx+narrow+6} {wy+34} l10 18 h-20z" fill="#ff9f0a"/><path d="M{wx+narrow+6} {wy+40} v6" stroke="#000" stroke-width="2" stroke-linecap="round"/></g>')
    handle_x = C.ease("x", [(0, wx + wide - 3), (1.2, wx + wide - 3), (2.6, wx + narrow - 3), (4.6, wx + narrow - 3), (6.0, wx + wide - 3)])
    out.append(f'<rect x="{wx+wide-3}" y="{wy+wh/2-22}" width="6" height="44" rx="3" fill="#fff" opacity="0.7">{handle_x}</rect>')
    # terminal with the finding
    tx, ty, tww, th = SX + 340, SY + 30, 212, 186
    out.append(f'<rect x="{tx}" y="{ty+5}" width="{tww}" height="{th}" rx="12" fill="#000" opacity="0.4"/>'
               f'<rect x="{tx}" y="{ty}" width="{tww}" height="{th}" rx="12" fill="#121216" stroke="#fff" stroke-opacity="0.15"/>'
               + "".join(f'<circle cx="{tx+16+i*14}" cy="{ty+15}" r="4.5" fill="{c}" opacity="0.8"/>' for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840"))))
    lines = [("$ resizelint Sources/", "#e5e5ea", 0.4), ("Toolbar.swift:42:9", "#8e8e93", 1.2), ("RL001 fixed width", "#ff9f0a", 2.5),
             ("  breaks below 260pt", "#ff9f0a", 2.6), ("fix: .frame(maxWidth:", "#30d158", 3.6), ("       .infinity)", "#30d158", 3.7), ("1 finding · 0.18s", "#8e8e93", 4.6)]
    for i, (s, c, t0) in enumerate(lines):
        out.append(f'<g opacity="0">{C.show(t0, 7.6)}' + text(tx + 14, ty + 50 + i * 19, s, 11.5, c, "mono", 500) + '</g>')
    return "".join(out)


def p_fonts(D, C):
    out = []
    bx, by, bw, bh = SX + 24, SY + 26, 300, 196
    out.append(f'<rect x="{bx}" y="{by+5}" width="{bw}" height="{bh}" rx="12" fill="#000" opacity="0.4"/>'
               f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="12" fill="#f5f5f7"/>'
               f'<path d="M{bx} {by+30}H{bx+bw}" stroke="#d1d1d6"/>'
               + "".join(f'<circle cx="{bx+16+i*14}" cy="{by+15}" r="4.5" fill="{c}"/>' for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")))
               + f'<rect x="{bx+64}" y="{by+7}" width="{bw-80}" height="16" rx="8" fill="#e5e5ea"/>' + text(bx + 76, by + 19, "example.com/pricing", 9.5, "#6e6e73", "sans", 500))
    bad = C.ease("opacity", [(0, 1), (3.6, 1), (4.0, 0), (7.4, 0), (7.8, 1)])
    good = C.ease("opacity", [(0, 0), (3.6, 0), (4.0, 1), (7.4, 1), (7.8, 0)])
    out.append(f'<g>{bad}<text x="{bx+20}" y="{by+82}" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="700" fill="#1d1d1f">Ship the type</text>'
               f'<text x="{bx+20}" y="{by+116}" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="700" fill="#1d1d1f">you meant.</text></g>')
    out.append(f'<g opacity="0">{good}<text x="{bx+20}" y="{by+82}" font-family="Georgia, \'Times New Roman\', serif" font-size="32" font-weight="700" fill="#1d1d1f" letter-spacing="-0.5">Ship the type</text>'
               f'<text x="{bx+20}" y="{by+116}" font-family="Georgia, \'Times New Roman\', serif" font-size="32" font-weight="700" fill="#1d1d1f" font-style="italic">you meant.</text></g>')
    out.append(bar(bx + 20, by + 140, 220, 6, "#1d1d1f", 0.18) + bar(bx + 20, by + 154, 180, 6, "#1d1d1f", 0.18)
               + f'<rect x="{bx+20}" y="{by+168}" width="92" height="18" rx="9" fill="#1d1d1f"/>')
    # audit panel
    ax, ay, aw, ah = SX + 344, SY + 26, 200, 196
    out.append(f'<rect x="{ax}" y="{ay+5}" width="{aw}" height="{ah}" rx="12" fill="#000" opacity="0.4"/>'
               f'<rect x="{ax}" y="{ay}" width="{aw}" height="{ah}" rx="12" fill="#1f1f26" stroke="#fff" stroke-opacity="0.15"/>'
               + text(ax + 14, ay + 24, "fontwitness audit", 11.5, "#e5e5ea", "mono", 600)
               + f'<path d="M{ax} {ay+36}H{ax+aw}" stroke="#fff" stroke-opacity="0.1"/>'
               + text(ax + 14, ay + 58, "expected", 10.5, FG3, "mono", 500) + text(ax + 14, ay + 76, "Georgia 700", 12.5, FG, "sans", 600)
               + text(ax + 14, ay + 104, "rendered", 10.5, FG3, "mono", 500))
    out.append(f'<g>{bad}' + text(ax + 14, ay + 122, "Arial (fallback)", 12.5, "#ff6b61", "sans", 600)
               + f'<circle cx="{ax+aw-24}" cy="{ay+117}" r="9" fill="#ff453a"/><path d="M{ax+aw-28} {ay+113} l8 8 M{ax+aw-20} {ay+113} l-8 8" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>'
               + f'<rect x="{ax+14}" y="{ay+150}" width="{aw-28}" height="28" rx="8" fill="#ff453a" opacity="0.18" stroke="#ff453a" stroke-opacity="0.6"/>'
               + text(ax + aw / 2, ay + 168.5, "CI · failed", 12, "#ff6b61", "sans", 700, "middle") + '</g>')
    out.append(f'<g opacity="0">{good}' + text(ax + 14, ay + 122, "Georgia 700", 12.5, "#4cd964", "sans", 600)
               + f'<circle cx="{ax+aw-24}" cy="{ay+117}" r="9" fill="#30d158"/><path d="M{ax+aw-28.5} {ay+117} l3 3 l6 -6" stroke="#fff" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
               + f'<rect x="{ax+14}" y="{ay+150}" width="{aw-28}" height="28" rx="8" fill="#30d158" opacity="0.18" stroke="#30d158" stroke-opacity="0.6"/>'
               + text(ax + aw / 2, ay + 168.5, "CI · passed", 12, "#4cd964", "sans", 700, "middle") + '</g>')
    return "".join(out)


PREVIEW = {"templates": p_templates, "tabbar": p_tabbar, "shell": p_shell, "menubar": p_menubar, "resize": p_resize, "fonts": p_fonts}


def card(proj, repo):
    D = Doc(CW, CH, "pc" + proj["icon"][:4], r=24, bg="#141418")
    C = Clock(T)
    p = D.p
    D.adddef(f'<linearGradient id="{p}-bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1b21"/><stop offset="1" stop-color="#121215"/></linearGradient>')
    D.add(f'<rect width="{CW}" height="{CH}" fill="url(#{p}-bg)"/>')
    D.add(_stage(D, proj["tint"]))
    D.add(f'<g clip-path="url(#{p}-st)">{PREVIEW[proj["icon"]](D, C)}</g>')
    D.add(f'<rect x="{SX+0.5}" y="{SY+0.5}" width="{SW-1}" height="{SH-1}" rx="15.5" stroke="#fff" stroke-opacity="0.08"/>')
    by = SY + SH + 22
    D.add(app_icon(D, proj["icon"], 26, by, 54))
    D.add(text(96, by + 24, proj["title"], 22, FG, "sans", 700, extra=' letter-spacing="-0.3"'))
    D.add(text(96, by + 47, proj["kind"], 14.5, FG2, "sans", 500))
    D.add(text(26, by + 92, proj["desc"], 15, "#c7c7cc", "sans", 500))
    stars = repo.get("stars", 0)
    lang, lc = proj["lang"]
    meta = f"★ {stars}"
    mw = tw(meta, 13, weight=600) + 22
    mx = CW - 26 - mw
    D.add(f'<rect x="{f1(mx)}" y="{by+6}" width="{f1(mw)}" height="26" rx="13" fill="#26262d" stroke="#fff" stroke-opacity="0.1"/>'
          + text(mx + mw / 2, by + 23.5, meta, 13, "#ffd60a" if stars >= 5 else FG2, "sans tnum", 700, "middle"))
    lw = tw(lang, 13, weight=600) + 34
    lx = mx - 8 - lw
    D.add(f'<rect x="{f1(lx)}" y="{by+6}" width="{f1(lw)}" height="26" rx="13" fill="#26262d" stroke="#fff" stroke-opacity="0.1"/>'
          f'<circle cx="{f1(lx+14)}" cy="{by+19}" r="4.5" fill="{lc}"/>' + text(lx + 24, by + 23.5, lang, 13, FG2, "sans", 600))
    return D.svg(title=proj["title"], desc=f'{proj["title"]}: {proj["desc"]}')
