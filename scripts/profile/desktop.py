"""Hero 1: miko.os. A macOS desktop over Astana at dusk: an About window with Miko,
a terminal that types, widgets fed by GitHub data, a notification and a dock that
magnifies smoothly under the pointer. One 20-second loop, no filters."""
from __future__ import annotations

import datetime as dt
import math

import chibi
import data as gh
import wall
from kit import (EASE, FG, FG2, FG3, Clock, Doc, app_icon, esc, f1, f3, shadow, squircle, text, tw, window)

W, H, HZ = 1200, 760, 600
T = 20.0
GREEN = ["#2a2a31", "#0e4429", "#006d32", "#26a641", "#39d353"]


def menubar(D, d, app="Terminal", items=("Shell", "Edit", "View", "Window", "Help")):
    out = [f'<rect width="{W}" height="28" fill="#05060f" opacity="0.38"/>',
           f'<circle cx="22" cy="14" r="8" fill="#fff"/>'
           f'<path d="M17.6 18 V11.6 L20 14.8 L22 11.6 L24 14.8 L26.4 11.6 V18" stroke="#11131c" stroke-width="1.7" fill="none" stroke-linejoin="round" stroke-linecap="round"/>',
           text(42, 18.5, app, 13.5, FG, "sans", 700)]
    x = 42 + tw(app, 13.5, weight=700) + 20
    for it in items:
        out.append(text(x, 18.5, it, 13.5, FG, "sans", 500))
        x += tw(it, 13.5, weight=500) + 20
    day = dt.date.fromisoformat(d["generated"])
    stamp = f"{day.strftime('%a %d %b')}  09:41"
    out.append(text(W - 16, 18.5, stamp, 13.5, FG, "sans", 500, "end"))
    rx = W - 16 - tw(stamp, 13.5, weight=500) - 20
    out.append(  # control centre, battery, wi-fi
        f'<g transform="translate({f1(rx-16)} 8)" fill="#fff"><rect x="0" y="0" width="16" height="5" rx="2.5"/><rect x="0" y="7" width="16" height="5" rx="2.5" opacity="0.85"/>'
        f'<circle cx="4" cy="2.5" r="1.6" fill="#000" opacity="0.5"/><circle cx="12" cy="9.5" r="1.6" fill="#000" opacity="0.5"/></g>'
        f'<g transform="translate({f1(rx-54)} 8)"><rect x="0.5" y="0.5" width="22" height="11" rx="3" stroke="#fff" stroke-opacity="0.9"/>'
        f'<rect x="2.5" y="2.5" width="15" height="7" rx="1.5" fill="#fff"/><path d="M24.5 4.5v3" stroke="#fff" stroke-linecap="round"/></g>'
        f'<g transform="translate({f1(rx-84)} 7)" stroke="#fff" stroke-width="1.7" fill="none" stroke-linecap="round">'
        f'<path d="M1 5 Q9 -1.5 17 5"/><path d="M4 8.2 Q9 4 14 8.2"/><circle cx="9" cy="11.6" r="1.3" fill="#fff" stroke="none"/></g>')
    return "".join(out)


def about(D, d, x, y, w, h):
    out = [window(D, x, y, w, h, bar=36, fill="#202024", alpha=0.95)]
    cx, cy, r = x + w / 2, y + 36 + 82, 68
    p = D.p
    D.adddef(f'<clipPath id="{p}-av"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>',
             f'<linearGradient id="{p}-avbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fb4ff"/>'
             f'<stop offset="0.55" stop-color="#b48df0"/><stop offset="1" stop-color="#ff9fb0"/></linearGradient>')
    out.append(f'<circle cx="{cx}" cy="{cy+3}" r="{r+2}" fill="#000" opacity="0.35"/>'
               f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{p}-avbg)"/>'
               f'<g clip-path="url(#{p}-av)"><circle cx="{cx-34}" cy="{cy-36}" r="10" fill="#fff" opacity="0.25"/>'
               f'<circle cx="{cx+40}" cy="{cy-30}" r="5" fill="#fff" opacity="0.25"/>'
               + chibi.bust(cx, cy - 4, 0.94, f"{p}me", smile="open") + '</g>'
               f'<circle cx="{cx}" cy="{cy}" r="{r-0.5}" stroke="#fff" stroke-opacity="0.35" stroke-width="1.5"/>')
    out.append(text(cx, cy + r + 40, "miko", 30, FG, "sans", 700, "middle", ' letter-spacing="-0.4"'))
    out.append(text(cx, cy + r + 62, "Software, tools, and side projects", 13.5, FG2, "sans", 500, "middle"))
    rows = [("Location", "Astana, Kazakhstan"), ("Focus", "native apps · dev tools · CI"),
            ("Stack", "Swift · Python · TypeScript"), ("GitHub", f"{d['stars']} stars · {d['followers']:,} followers")]
    ry = cy + r + 96
    for i, (k, v) in enumerate(rows):
        out.append(text(x + 118, ry + i * 21, k, 12.5, FG3, "sans", 600, "end") + text(x + 130, ry + i * 21, v, 12.5, "#e5e5ea", "sans", 500))
    by = y + h - 46
    for i, (label, primary) in enumerate((("More Info…", False), ("GitHub ↗", True))):
        bw = 104
        bx = cx - bw - 5 if i == 0 else cx + 5
        out.append(f'<rect x="{f1(bx)}" y="{by}" width="{bw}" height="26" rx="7" fill="{"#0a84ff" if primary else "#3a3a40"}" '
                   f'stroke="#fff" stroke-opacity="{0.25 if primary else 0.1}"/>' + text(bx + bw / 2, by + 17.5, label, 12.5, FG, "sans", 600, "middle"))
    return "".join(out)


def terminal(D, C, x, y, w, h):
    p = D.p
    out = [window(D, x, y, w, h, "miko — -zsh — 80×24", fill="#141418", alpha=0.95, bar=34)]
    fs, lh = 12.5, 18.6
    adv = fs * 0.602
    x0, y0 = x + 16, y + 34 + 22
    prompt = [("~/dev", "#64d2ff"), (" ", FG), ("main", "#bf9cff"), (" ❯ ", "#30d158")]
    pw = sum(len(s) for s, _ in prompt) * adv
    script = [
        ("cmd", "whoami", 0.5), ("out", [("miko · software, tools & side projects", FG2)], None),
        ("cmd", "ls ~/projects", 2.0), ("out", [("ResizeLint  FontWitness  AdaptiveAppShell", "#6cb6ff")], None),
        ("out", [("LiquidGlassTabBars  MenuBarCommandKit  skillparcel", "#6cb6ff")], None),
        ("cmd", "swift build -c release", 4.0), ("bar", None, None), ("out", [("✓ ", "#30d158"), ("Build complete! ", "#30d158"), ("(2.31s)", FG3)], None),
        ("cmd", "git push", 9.3), ("out", [("To github.com:mikonyaa/ResizeLint.git", FG2)], None),
        ("out", [("   a3f9c12..e81b04d  ", FG3), ("main -> main", "#e5e5ea")], None),
    ]
    t = 0.0
    cursor_steps = []  # (time, x, y)
    for i, (kind, body, t_start) in enumerate(script):
        ly = y0 + i * lh
        if kind == "cmd":
            t = t_start
            spans = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in prompt)
            out.append(f'<g opacity="0">{C.show(t-0.25)}<text x="{f1(x0)}" y="{f1(ly)}" class="mono" font-size="{fs}" xml:space="preserve">{spans}</text></g>')
            cid = f"{p}-ty{i}"
            clip, t_end = C.type_clip(cid, x0 + pw, ly - fs, fs + 5, len(body) * adv, t, len(body), cps=15)
            D.adddef(clip)
            out.append(f'<text x="{f1(x0+pw)}" y="{f1(ly)}" class="mono" font-size="{fs}" fill="{FG}" clip-path="url(#{cid})">{esc(body)}</text>')
            for k in range(len(body) + 1):
                cursor_steps.append((t - 0.25 if k == 0 else t + k / 15, x0 + pw + k * adv, ly))
            t = t_end + 0.35
        elif kind == "out":
            spans = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in body)
            out.append(f'<g opacity="0">{C.show(t)}<text x="{f1(x0)}" y="{f1(ly)}" class="mono" font-size="{fs}" xml:space="preserve">{spans}</text></g>')
            t += 0.22
        elif kind == "bar":
            t_b0, t_b1 = t, t + 2.2
            bx, bw = x0 + 33 * adv, w - 32 - 33 * adv - 52
            gid = f"{p}-pb"
            D.adddef(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0a84ff"/><stop offset="1" stop-color="#64d2ff"/></linearGradient>')
            fill = (f'<rect x="{f1(bx)}" y="{f1(ly-9)}" width="0" height="9" rx="4.5" fill="url(#{gid})">'
                    + C.ease("width", [(t_b0, 0), (t_b0 + 0.6, round(bw * 0.35, 1)), (t_b0 + 1.4, round(bw * 0.72, 1)), (t_b1, round(bw, 1)), (T - 0.35, round(bw, 1)), (T - 0.05, 0)])
                    + '</rect>')
            out.append(f'<g opacity="0">{C.show(t)}'
                       f'<text x="{f1(x0)}" y="{f1(ly)}" class="mono" font-size="{fs}" fill="{FG2}">Compiling ResizeLint (42 files)</text>'
                       f'<rect x="{f1(bx)}" y="{f1(ly-9)}" width="{f1(bw)}" height="9" rx="4.5" fill="#2c2c33"/>{fill}'
                       f'<text x="{f1(bx+bw+10)}" y="{f1(ly)}" class="mono" font-size="{fs}" fill="{FG3}">42/42</text></g>')
            t = t_b1 + 0.25
            cursor_steps.append((t_b0, x0, ly + lh * 2))
    # cursor: hops along with the typing, blinks while idle
    vals_x, vals_y, kts = [], [], []
    for (tt, cx_, cy_) in sorted(cursor_steps):
        kts.append(C.k(tt)); vals_x.append(f1(cx_)); vals_y.append(f1(cy_ - fs + 1.5))
    kts[0] = 0.0
    kt = ";".join(f3(k) for k in kts)
    out.append(f'<g opacity="0">{C.show(0.25)}<rect x="{vals_x[0]}" y="{vals_y[0]}" width="{f1(adv)}" height="{fs+2}" fill="#e5e5ea" opacity="0.85">'
               f'<animate attributeName="x" values="{";".join(vals_x)}" keyTimes="{kt}" calcMode="discrete" dur="{T}s" repeatCount="indefinite"/>'
               f'<animate attributeName="y" values="{";".join(vals_y)}" keyTimes="{kt}" calcMode="discrete" dur="{T}s" repeatCount="indefinite"/>'
               f'<animate attributeName="opacity" values="0.85;0.85;0.1;0.85" keyTimes="0;0.45;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect></g>')
    return "".join(out)


def widget(x, y, w, h):
    return (shadow(x, y, w, h, 18, 0.6) + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#1b1b21" opacity="0.9"/>'
            f'<rect x="{x+0.5}" y="{y+0.5}" width="{w-1}" height="{h-1}" rx="17.5" stroke="#fff" stroke-opacity="0.12"/>')


def widgets(D, d, x, y):
    out = []
    c = d["contrib"]
    wk = c["weeks"][-17:]
    lv, _ = gh._levels(c["weeks"])
    out.append(widget(x, y, 240, 122))
    out.append(text(x + 14, y + 22, "Contributions", 12.5, FG, "sans", 700) + text(x + 226, y + 22, f"{c['total']:,} this year", 11.5, FG3, "sans", 600, "end"))
    cs, gp = 9, 3
    gx, gy = x + 16, y + 32
    last = None
    for wi, week in enumerate(wk):
        for (day, n, wd) in week:
            cx_, cy_ = gx + wi * (cs + gp), gy + wd * (cs + gp)
            out.append(f'<rect x="{cx_}" y="{cy_}" width="{cs}" height="{cs}" rx="2.4" fill="{GREEN[lv(n)]}"/>')
            last = (cx_, cy_)
    if last:
        out.append(f'<rect x="{last[0]-1.5}" y="{last[1]-1.5}" width="{cs+3}" height="{cs+3}" rx="3.4" stroke="#39d353" stroke-width="1.4" fill="none">'
                   f'<animate attributeName="opacity" values="1;0.2;1" dur="2.2s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="{EASE};{EASE}"/></rect>')
    # stars
    sx = x + 252
    out.append(widget(sx, y, 90, 122))
    star = "M0 -11 L3.2 -3.6 L11.4 -3.6 L4.8 1.4 L7.2 9.4 L0 4.6 L-7.2 9.4 L-4.8 1.4 L-11.4 -3.6 L-3.2 -3.6Z"
    D.adddef(f'<linearGradient id="{D.p}-star" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe066"/><stop offset="1" stop-color="#ff9f0a"/></linearGradient>')
    out.append(f'<path d="{star}" transform="translate({sx+26} {y+30})" fill="url(#{D.p}-star)"/>'
               + text(sx + 14, y + 82, str(d["stars"]), 36, FG, "sans tnum", 700, extra=' letter-spacing="-1"')
               + text(sx + 14, y + 104, "stars", 12, FG3, "sans", 600))
    # languages ring
    lx = sx + 100
    out.append(widget(lx, y, 88, 122))
    shares = gh.language_shares(d["repos"], top=3)
    cols = {"TypeScript": "#3b82f6", "Swift": "#ff7a3d", "Python": "#ffd43b", "JavaScript": "#f7df1e", "Other": "#8e8e93"}
    rcx, rcy, rr = lx + 44, y + 52, 26
    circ = 2 * math.pi * rr
    acc = 0.0
    out.append(f'<circle cx="{rcx}" cy="{rcy}" r="{rr}" stroke="#2c2c33" stroke-width="8"/>')
    for i, (name, s) in enumerate(shares):
        seg = max(0.0, s * circ - 2.5)
        out.append(f'<circle cx="{rcx}" cy="{rcy}" r="{rr}" stroke="{cols.get(name, "#8e8e93")}" stroke-width="8" fill="none" '
                   f'stroke-dasharray="{f1(seg)} {f1(circ)}" stroke-dashoffset="{f1(-acc*circ)}" transform="rotate(-90 {rcx} {rcy})" stroke-linecap="round"/>')
        acc += s
    top = shares[0]
    out.append(text(rcx, rcy + 5, f"{top[1]*100:.0f}%", 14, FG, "sans tnum", 700, "middle")
               + text(rcx, y + 106, top[0], 11.5, FG3, "sans", 600, "middle"))
    return "".join(out)


def notification(D, C, x, y, w):
    h = 62
    body = (shadow(x, y, w, h, 16, 0.7) + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#26262c" opacity="0.96"/>'
            f'<rect x="{x+0.5}" y="{y+0.5}" width="{w-1}" height="{h-1}" rx="15.5" stroke="#fff" stroke-opacity="0.14"/>'
            + app_icon(D, "github", x + 12, y + 13, 36)
            + text(x + 60, y + 27, "GitHub Actions", 13, FG, "sans", 700) + text(x + w - 14, y + 27, "now", 11.5, FG3, "sans", 500, "end")
            + text(x + 60, y + 46, "profile.yml · numbers redrawn ✓", 12.5, "#d1d1d6", "sans", 500))
    slide = C.ease_t("translate", [(0, f"{w+40} 0"), (11.2, f"{w+40} 0"), (11.75, "0 0"), (16.4, "0 0"), (16.95, f"{w+40} 0")])
    return f'<g>{slide}{body}</g>'


DOCK = ["finder", "terminal", "xcode", "swift", "templates", "tabbar", "shell", "menubar", "resize", "fonts", "|", "github"]


def dock(D, C):
    """Dock + pointer. Positions are sampled every 50 ms while the pointer is near the dock and
    interpolated linearly, so the magnification is smooth and stays in sync with the pointer."""
    s0, gap = 50, 10
    n_icons = sum(1 for k in DOCK if k != "|")
    sep_w = 18
    base_w = n_icons * s0 + (n_icons - 1) * gap + sep_w
    dock_y, dock_h = H - 72, 62
    dock_x = (W - base_w) / 2 - 12
    icon_bottom = dock_y + 6 + s0

    def layout(cursor_x, m):
        sizes = []
        for k in DOCK:
            sizes.append(sep_w if k == "|" else s0)
        # base centres
        xs, x = [], dock_x + 12
        for s in sizes:
            xs.append(x + s / 2)
            x += s + (gap if s == s0 else 0)
        scale = []
        for k, cx in zip(DOCK, xs):
            if k == "|":
                scale.append(1.0)
                continue
            dist = abs(cx - cursor_x)
            f = max(0.0, 1 - dist / 130)
            scale.append(1 + 0.5 * m * (0.5 - 0.5 * math.cos(math.pi * f)))
        widths = [(s0 * sc if k != "|" else sep_w) for k, sc in zip(DOCK, scale)]
        extra = sum(widths) - sum(sizes)
        # anchor: grow outward from the pointer so icons under it don't slide away
        x = dock_x + 12 - extra * ((cursor_x - (dock_x + 12)) / base_w if m > 0 else 0.5)
        centres = []
        for k, wdt in zip(DOCK, widths):
            centres.append(x + wdt / 2)
            x += wdt + (gap if k != "|" else 0)
        left = centres[0] - widths[0] / 2 - 12
        right = centres[-1] + widths[-1] / 2 + 12
        return centres, scale, (left, right)

    # pointer path: (t, x, y)
    gx_icon = None
    c0, _, _ = layout(0, 0)
    gi = DOCK.index("github")
    gx_icon = c0[gi]
    path = [(0, 610, 470), (11.4, 610, 470), (12.6, c0[0] - 10, icon_bottom - 22), (15.4, gx_icon, icon_bottom - 24),
            (16.2, gx_icon, icon_bottom - 24), (17.6, 650, 500), (T, 610, 470)]

    def ease(u):
        return u * u * (3 - 2 * u)

    def pointer(t):
        for (ta, xa, ya), (tb, xb, yb) in zip(path, path[1:]):
            if ta <= t <= tb:
                u = 0 if tb == ta else ease((t - ta) / (tb - ta))
                return xa + (xb - xa) * u, ya + (yb - ya) * u
        return path[-1][1], path[-1][2]

    def mag(t, py):
        return max(0.0, min(1.0, (py - (dock_y - 60)) / 50))

    ts = [0.0, 11.4] + [11.4 + i * 0.05 for i in range(1, int((18.0 - 11.4) / 0.05))] + [18.0, T]
    ts = sorted(set(round(t, 3) for t in ts))
    frames = []
    for t in ts:
        px, py = pointer(t)
        cs, sc, lr = layout(px, mag(t, py))
        frames.append((t, px, py, cs, sc, lr))
    kt = ";".join(f3(C.k(t)) for t, *_ in frames)
    bx_v = ";".join(f1(fr[5][0]) for fr in frames)
    bw_v = ";".join(f1(fr[5][1] - fr[5][0]) for fr in frames)
    anim = (f'<animate attributeName="x" values="{bx_v}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/>'
            f'<animate attributeName="width" values="{bw_v}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/>')
    out = [f'<rect x="{f1(dock_x)}" y="{dock_y+6}" width="{f1(base_w+24)}" height="{dock_h}" rx="24" fill="#000" opacity="0.18">{anim}</rect>',
           f'<rect x="{f1(dock_x)}" y="{dock_y}" width="{f1(base_w+24)}" height="{dock_h}" rx="22" fill="#2a2a38" opacity="0.62">{anim}</rect>'
           f'<rect x="{f1(dock_x)}" y="{dock_y}" width="{f1(base_w+24)}" height="{dock_h}" rx="22" fill="#ffffff" opacity="0.1">{anim}</rect>'
           f'<rect x="{f1(dock_x)}" y="{dock_y}" width="{f1(base_w+24)}" height="{dock_h}" rx="22" stroke="#fff" stroke-opacity="0.3">{anim}</rect>']
    running = {"finder", "terminal", "xcode"}
    for i, k in enumerate(DOCK):
        if k == "|":
            sx_v = ";".join(f1(fr[3][i]) for fr in frames)
            out.append(f'<rect x="{f1(frames[0][3][i])}" y="{dock_y+12}" width="1" height="{dock_h-24}" fill="#fff" opacity="0.3">'
                       f'<animate attributeName="x" values="{sx_v}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></rect>')
            continue
        tr = ";".join(f"{f1(fr[3][i])} {icon_bottom}" for fr in frames)
        scv = ";".join(f3(fr[4][i]) for fr in frames)
        inner = app_icon(D, k, -s0 / 2, -s0, s0)
        if k == "github":
            inner = (f'<g>{C.ease_t("translate", [(0, "0 0"), (16.25, "0 0"), (16.55, "0 -24"), (16.85, "0 0"), (17.1, "0 -10"), (17.35, "0 0")])}{inner}</g>')
        out.append(f'<g transform="translate({f1(frames[0][3][i])} {icon_bottom})">'
                   f'<animateTransform attributeName="transform" type="translate" values="{tr}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/>'
                   f'<animateTransform attributeName="transform" type="scale" values="{scv}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite" additive="sum"/>'
                   f'{inner}</g>')
        dot_x = ";".join(f1(fr[3][i]) for fr in frames)
        if k in running or k == "github":
            extra = "" if k in running else C.show(16.4)
            op = "1" if k in running else "0"
            out.append(f'<circle cx="{f1(frames[0][3][i])}" cy="{dock_y+dock_h-5}" r="2" fill="#fff" opacity="{op}">{extra}'
                       f'<animate attributeName="cx" values="{dot_x}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></circle>')
    # pointer
    pv = ";".join(f"{f1(fr[1])} {f1(fr[2])}" for fr in frames)
    arrow = ('<path d="M0 0 L0 17.5 L4.4 13.4 L7.4 20.2 L10.2 19 L7.3 12.4 L13 12.2Z" fill="#000" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/>')
    click = C.ease_t("scale", [(0, 1), (16.15, 1), (16.25, 0.86), (16.4, 1)])
    out.append(f'<g transform="translate(610 470)"><animateTransform attributeName="transform" type="translate" values="{pv}" keyTimes="{kt}" '
               f'dur="{T}s" repeatCount="indefinite"/><g>{click}{arrow}</g></g>')
    return "".join(out)


def desktop(d):
    D = Doc(W, H, "os", r=14)
    C = Clock(T)
    D.add(wall.wallpaper(D, W, H, HZ, "dusk", sun_x=0.47))
    D.add(menubar(D, d))
    D.add(about(D, d, 36, 52, 356, 404))
    D.add(terminal(D, C, 726, 52, 438, 262))
    D.add(widgets(D, d, 726, 332))
    D.add(notification(D, C, W - 16 - 320, 38, 320))
    D.add(dock(D, C))
    return D.svg(title="miko.os", desc="A macOS desktop over Astana at dusk: About miko, a terminal running swift build and git push, "
                                       "contribution, star and language widgets, and a dock of projects.")
