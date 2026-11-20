"""Spotlight (toolbox), Activity (numbers) and Messages (footer)."""
from __future__ import annotations

import datetime as dt
import math

import chibi
import data as gh
import wall
from kit import (EASE, FG, FG2, FG3, Clock, Doc, app_icon, esc, f1, f3, icon, shadow, squircle, text, tw, traffic, window)


# ------------------------------------------------------------------ Spotlight: the toolbox

TOOLS = [
    ("Languages", [("Swift", "swift", ("#ffa257", "#f23e2a"), "Native apps, SwiftUI kits, command-line checks"),
                   ("Python", "python", ("#4b8bbe", "#2b5b84"), "Automation and tooling"),
                   ("TypeScript", "ts", ("#4a90e2", "#2f66c4"), "Web tooling and CI checks")]),
    ("Apple platforms", [("SwiftUI", "swiftui", ("#5ab4ff", "#1550c8"), "iOS, iPadOS, macOS, watchOS, visionOS"),
                         ("Xcode", "xcode", ("#5ab4ff", "#1550c8"), "Previews, Instruments, TestFlight")]),
    ("Workflow and data", [("GitHub Actions", "githubactions", ("#3a3a40", "#121214"), "CI for the profile and the tools"),
                           ("Docker", "docker", ("#3aa0f5", "#1d63c9"), "Reproducible local services"),
                           ("PostgreSQL", "postgresql", ("#4f7fbf", "#2b5085"), "Also MySQL and SQLite")]),
]


def _tool_icon(D, key, cols, x, y, s):
    gid = f"{D.p}-ti-{key}"
    D.once(gid, f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{cols[0]}"/><stop offset="1" stop-color="{cols[1]}"/></linearGradient>')
    d = squircle(x, y, s)
    out = f'<path d="{d}" fill="url(#{gid})"/><path d="{d}" stroke="#fff" stroke-opacity="0.2"/>'
    k = s / 100
    if key == "ts":
        out += text(x + s * 0.92, y + s * 0.86, "TS", s * 0.42, "#fff", "sans", 800, "end")
    elif key == "swiftui":
        out += app_icon(D, "templates", x, y, s)[0:0] + (
            f'<path d="M{f1(x+28*k)} {f1(y+38*k)} L{f1(x+50*k)} {f1(y+26*k)} L{f1(x+72*k)} {f1(y+38*k)} L{f1(x+50*k)} {f1(y+50*k)}Z" fill="#fff"/>'
            f'<path d="M{f1(x+28*k)} {f1(y+52*k)} L{f1(x+50*k)} {f1(y+64*k)} L{f1(x+72*k)} {f1(y+52*k)}" stroke="#fff" stroke-width="{f1(6*k)}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M{f1(x+28*k)} {f1(y+64*k)} L{f1(x+50*k)} {f1(y+76*k)} L{f1(x+72*k)} {f1(y+64*k)}" stroke="#fff" stroke-width="{f1(6*k)}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>')
    elif key == "xcode":
        from kit import _glyph
        out += _glyph("xcode", x + s / 2, y + s / 2, s)
    else:
        name = {"swift": "swift"}.get(key, key)
        out += icon(name, x + s * 0.2, y + s * 0.2, s * 0.6, "#fff")
    return out


def spotlight(d):
    W, H = 1200, 460
    D = Doc(W, H, "sp", r=16)
    C = Clock(15.0)
    D.add(wall.wallpaper(D, W, H, 392, "dusk", seed=5, sun_x=0.5))
    D.add(f'<rect width="{W}" height="{H}" fill="#05060f" opacity="0.3"/>')
    px, py, pw, ph = 150, 32, 900, 396
    D.add(shadow(px, py, pw, ph, 20))
    D.add(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="20" fill="#1e1e24"/>'
          f'<rect x="{px+0.5}" y="{py+0.5}" width="{pw-1}" height="{ph-1}" rx="19.5" stroke="#fff" stroke-opacity="0.16"/>')
    # search field: typed once per loop
    D.add(f'<circle cx="{px+36}" cy="{py+32}" r="10" stroke="#c7c7cc" stroke-width="2.4"/><path d="M{px+43.5} {py+39.5} l7 7" stroke="#c7c7cc" stroke-width="2.4" stroke-linecap="round"/>')
    q = "miko's toolbox"
    qw = tw(q, 24, weight=500)
    clip, _ = C.type_clip(f"{D.p}-q", px + 66, py + 10, 36, qw, 0.3, len(q), cps=18, t_off=14.6)
    D.adddef(clip)
    D.add(f'<text x="{px+66}" y="{py+41}" class="sans" font-size="24" font-weight="500" fill="{FG}" clip-path="url(#{D.p}-q)">{esc(q)}</text>')
    D.add(f'<rect x="{px+pw-96}" y="{py+20}" width="76" height="24" rx="7" fill="#2c2c33"/>' + text(px + pw - 58, py + 37, "⌘ Space", 12, FG3, "sans", 600, "middle"))
    D.add(f'<path d="M{px} {py+64}H{px+pw}" stroke="#fff" stroke-opacity="0.1"/>')
    # list
    lx, lw = px + 12, 360
    D.add(f'<path d="M{px+lw+24} {py+64}V{py+ph}" stroke="#fff" stroke-opacity="0.08"/>')
    rows, y = [], py + 88
    for sec, items in TOOLS:
        D.add(text(lx + 12, y, sec, 11.5, FG3, "sans", 700))
        y += 10
        for name, key, cols, blurb in items:
            rows.append((name, key, cols, blurb, y))
            y += 26
        y += 22
    steps = [0, 1, 2, 3, 5, 7]
    period = 15.0 / len(steps)
    sel_pairs = []
    for i, ri in enumerate(steps):
        t0 = i * period
        sel_pairs += [(t0 + 0.001 if i else 0, rows[ri][4]), (t0 + period - 0.22, rows[ri][4])]
    sel_pairs.append((15.0, rows[steps[0]][4]))
    D.add(f'<rect x="{lx}" y="{rows[0][4]}" width="{lw}" height="25" rx="7" fill="#0a64e0">' + C.ease("y", sel_pairs) + '</rect>')
    kinds = {"Swift": "Language", "Python": "Language", "TypeScript": "Language", "SwiftUI": "Framework", "Xcode": "Developer tool",
             "GitHub Actions": "CI", "Docker": "Containers", "PostgreSQL": "Database"}
    for name, key, cols, blurb, ry in rows:
        D.add(_tool_icon(D, key, cols, lx + 10, ry + 2.5, 20) + text(lx + 42, ry + 17.5, name, 14, FG, "sans", 600)
              + text(lx + lw - 12, ry + 17.5, kinds[name], 12, "#c7c7cc", "sans", 500, "end"))
    # preview pane: one panel per step, crossfading
    shares = dict(gh.language_shares(d["repos"], top=6))
    vx = px + lw + 24
    vw = pw - lw - 24
    for i, ri in enumerate(steps):
        name, key, cols, blurb, _ = rows[ri]
        t0 = i * period
        vis = C.ease("opacity", [(0, 0), (t0 - 0.12, 0), (t0 + 0.1, 1), (t0 + period - 0.2, 1), (t0 + period - 0.05, 0)] if i else
                     [(0, 1), (period - 0.2, 1), (period - 0.05, 0), (15.0 - 0.12, 0), (15.0, 1)])
        cx = vx + vw / 2
        pane = (_tool_icon(D, key, cols, cx - 44, py + 110, 88)
                + text(cx, py + 244, name, 28, FG, "sans", 700, "middle", ' letter-spacing="-0.4"')
                + text(cx, py + 270, blurb, 15, FG2, "sans", 500, "middle"))
        if name in shares:
            s = shares[name]
            bw_ = 300
            pane += (f'<rect x="{f1(cx-bw_/2)}" y="{py+300}" width="{bw_}" height="8" rx="4" fill="#2c2c33"/>'
                     f'<rect x="{f1(cx-bw_/2)}" y="{py+300}" width="{f1(bw_*s)}" height="8" rx="4" fill="{cols[0]}"/>'
                     + text(cx, py + 332, f"{s*100:.0f}% of code across public repos", 12.5, FG3, "sans", 600, "middle"))
        else:
            pane += (f'<rect x="{f1(cx-62)}" y="{py+300}" width="124" height="26" rx="13" fill="#2c2c33"/>'
                     + text(cx, py + 317.5, "in daily use", 12.5, "#d1d1d6", "sans", 600, "middle"))
        D.add(f'<g opacity="{1 if i == 0 else 0}">{vis}{pane}</g>')
    return D.svg(title="Toolbox", desc="Spotlight search for miko's toolbox: Swift, Python, TypeScript, SwiftUI, Xcode, GitHub Actions, Docker, PostgreSQL.")


# ------------------------------------------------------------------ Activity: the numbers

def _smooth(pts, floor=None):
    d = f"M{f1(pts[0][0])} {f1(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[max(0, i - 1)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(len(pts) - 1, i + 2)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        if floor is not None:
            c1 = (c1[0], min(c1[1], floor))
            c2 = (c2[0], min(c2[1], floor))
        d += f" C{f1(c1[0])} {f1(c1[1])} {f1(c2[0])} {f1(c2[1])} {f1(p2[0])} {f1(p2[1])}"
    return d


def activity(d):
    W, H = 1200, 470
    D = Doc(W, H, "ac", r=16, bg="#141418")
    C = Clock(14.0)
    p = D.p
    D.add(f'<rect width="{W}" height="38" fill="#1e1e23"/><path d="M0 38H{W}" stroke="#000" stroke-opacity="0.5"/>' + traffic(22, 19)
          + text(W / 2, 24, "Activity — mikonyaa", 13, "#c7c7cc", "sans", 600, "middle"))
    c = d["contrib"]
    weeks = c["weeks"]
    vals = [sum(n for _, n, _ in wk) for wk in weeks]
    D.add(text(40, 104, f"{c['total']:,}", 46, FG, "sans tnum", 800, extra=' letter-spacing="-1.5"')
          + text(40, 130, "contributions in the last year", 14.5, FG2, "sans", 500))
    last4 = sum(vals[-4:])
    D.add(f'<rect x="{40+tw(f"{c[chr(116)+chr(111)+chr(116)+chr(97)+chr(108)]:,}", 46, weight=800)+16:.0f}" y="76" width="134" height="28" rx="14" fill="#30d158" opacity="0.16"/>'
          + text(40 + tw(f"{c['total']:,}", 46, weight=800) + 83, 95, f"{last4} in 4 weeks", 13, "#4cd964", "sans tnum", 700, "middle"))
    # segmented control
    sx = 560
    D.add(f'<rect x="{sx}" y="72" width="240" height="30" rx="9" fill="#26262d"/><rect x="{sx+162}" y="75" width="75" height="24" rx="7" fill="#45454f"/>')
    for i, lab in enumerate(("Week", "Month", "Year")):
        D.add(text(sx + 40 + i * 80, 92, lab, 13, FG if i == 2 else FG2, "sans", 600, "middle"))
    # chart
    cx0, cx1, cy0, cy1 = 40, 800, 160, 400
    mx = max(vals) or 1
    top = mx * 1.15
    for k in range(5):
        gy = cy1 - (cy1 - cy0) * k / 4
        D.add(f'<path d="M{cx0} {gy}H{cx1}" stroke="#fff" stroke-opacity="{0.12 if k == 0 else 0.06}"/>'
              + text(cx1 + 8, gy + 4, f"{top*k/4:.0f}", 11, FG3, "sans tnum", 500))
    n = len(vals)
    pts = [(cx0 + (cx1 - cx0) * i / (n - 1), cy1 - (cy1 - cy0) * v / top) for i, v in enumerate(vals)]
    line = _smooth(pts, floor=cy1)
    D.adddef(f'<linearGradient id="{p}-ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#30d158" stop-opacity="0.45"/>'
             f'<stop offset="1" stop-color="#30d158" stop-opacity="0"/></linearGradient>',
             f'<clipPath id="{p}-ch"><rect x="{cx0}" y="{cy0-20}" width="{cx1-cx0}" height="{cy1-cy0+20}"/></clipPath>')
    D.add(f'<path d="{line} L{cx1} {cy1} L{cx0} {cy1}Z" fill="url(#{p}-ar)"/>'
          f'<path d="{line}" stroke="#30d158" stroke-width="2.6" fill="none" stroke-linejoin="round"/>')
    seen = set()
    for i, wk in enumerate(weeks):
        day = dt.date.fromisoformat(wk[0][0])
        if day.day <= 7 and (day.year, day.month) not in seen and 0 < i < n - 2:
            seen.add((day.year, day.month))
            D.add(text(pts[i][0], cy1 + 22, day.strftime("%b"), 11.5, FG3, "sans", 600, "middle"))
    # scrubber riding the line
    D.adddef(f'<path id="{p}-ln" d="{line}"/>')
    D.add(f'<g clip-path="url(#{p}-ch)"><g>'
          f'<animateMotion dur="14s" repeatCount="indefinite" calcMode="spline" keyPoints="0;1;1" keyTimes="0;0.9;1" keySplines="{EASE};0 0 1 1">'
          f'<mpath href="#{p}-ln"/></animateMotion>'
          f'<path d="M0 0V400" stroke="#fff" stroke-opacity="0.35" stroke-dasharray="3 4"/>'
          f'<circle r="9" fill="#30d158" opacity="0.25"/><circle r="5" fill="#fff" stroke="#30d158" stroke-width="2.5"/></g></g>')
    # stats column
    longest, current = gh.streaks([(dd, k) for dd, k, _ in c["days"]])
    best = max(c["days"], key=lambda t: t[1])
    rows = [("Commits", f"{c['commits']:,}"), ("Pull requests", f"{c['prs']}"), ("Stars earned", f"{d['stars']}"),
            ("Followers", f"{d['followers']:,}"), ("Longest streak", f"{longest} days"), ("Best day", f"{best[1]}")]
    rx0, rx1 = 860, 1160
    D.add(f'<rect x="{rx0-20}" y="64" width="{rx1-rx0+40}" height="246" rx="14" fill="#1b1b21" stroke="#fff" stroke-opacity="0.07"/>')
    for i, (k, v) in enumerate(rows):
        ry = 98 + i * 36
        D.add(text(rx0, ry, k, 14, FG2, "sans", 500) + text(rx1, ry, v, 15, FG, "sans tnum", 700, "end"))
        if i < len(rows) - 1:
            D.add(f'<path d="M{rx0} {ry+14}H{rx1}" stroke="#fff" stroke-opacity="0.07"/>')
    # languages
    shares = gh.language_shares(d["repos"], top=3)
    cols = {"TypeScript": "#3b82f6", "Swift": "#ff7a3d", "Python": "#ffd43b", "JavaScript": "#f7df1e", "Other": "#636366"}
    D.add(text(rx0 - 20, 344, "Languages", 13, FG, "sans", 700))
    acc = 0.0
    bw = rx1 - rx0 + 40
    for i, (nm, s) in enumerate(shares):
        w = max(2, s * bw - 3)
        D.add(f'<rect x="{f1(rx0-20+acc*bw)}" y="356" width="0" height="10" rx="3" fill="{cols.get(nm, "#636366")}">'
              f'<animate attributeName="width" values="0;{f1(w)};{f1(w)}" keyTimes="0;0.08;1" dur="14s" fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1;0 0 1 1" begin="{0.2+i*0.1:.1f}s"/></rect>')
        acc += s
    lx = rx0 - 20
    for i, (nm, s) in enumerate(shares):
        if nm == "Other":
            continue
        lab = f"{nm} {s*100:.0f}%"
        D.add(f'<circle cx="{f1(lx+5)}" cy="{388}" r="5" fill="{cols.get(nm, "#636366")}"/>' + text(lx + 15, 392.5, lab, 12.5, FG2, "sans", 600))
        lx += tw(lab, 12.5, weight=600) + 30
    D.add(text(W - 24, H - 18, f"updated {d['generated']}", 11.5, FG3, "sans tnum", 500, "end")
          + text(40, H - 18, "weekly contributions · last 12 months", 11.5, FG3, "sans", 500))
    return D.svg(title="Activity", desc=f"{c['total']} contributions in the last year; weekly chart, commits, pull requests, stars, followers, streaks and languages.")


# ------------------------------------------------------------------ Messages: the footer

def messages(d):
    W, H = 1200, 340
    D = Doc(W, H, "ms", r=16, bg="#18181c")
    C = Clock(13.0)
    p = D.p
    sbw = 280
    D.add(f'<rect width="{sbw}" height="{H}" fill="#1f1f24"/><path d="M{sbw} 0V{H}" stroke="#000" stroke-opacity="0.5"/>' + traffic(22, 22)
          + f'<rect x="16" y="46" width="{sbw-32}" height="28" rx="8" fill="#2c2c33"/>' + text(40, 65, "Search", 13, FG3, "sans", 500)
          + f'<circle cx="29" cy="59" r="5" stroke="#8e8e93" stroke-width="1.5"/>')
    # conversation row
    D.adddef(f'<clipPath id="{p}-a1"><circle cx="46" cy="114" r="24"/></clipPath>',
             f'<linearGradient id="{p}-abg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fb4ff"/><stop offset="1" stop-color="#ff9fb0"/></linearGradient>')
    D.add(f'<rect x="10" y="86" width="{sbw-20}" height="58" rx="10" fill="#0a64e0"/>'
          f'<circle cx="46" cy="114" r="24" fill="url(#{p}-abg)"/><g clip-path="url(#{p}-a1)">{chibi.bust(46, 112, 0.33, p+"a1", smile="open")}</g>'
          + text(80, 109, "miko", 14, FG, "sans", 700) + text(sbw - 22, 109, "09:41", 12, "#d1e4ff", "sans", 500, "end")
          + text(80, 128, "thanks for stopping by!", 12.5, "#d1e4ff", "sans", 500))
    for i in range(3):
        y = 162 + i * 58
        D.add(f'<circle cx="46" cy="{y+20}" r="22" fill="#2c2c33"/>' + f'<rect x="80" y="{y+8}" width="{90-i*14}" height="8" rx="4" fill="#3a3a42"/>'
              f'<rect x="80" y="{y+24}" width="{150-i*20}" height="7" rx="3.5" fill="#2e2e35"/>')
    # header
    D.add(f'<rect x="{sbw}" y="0" width="{W-sbw}" height="56" fill="#1d1d22"/><path d="M{sbw} 56H{W}" stroke="#000" stroke-opacity="0.45"/>'
          + text(sbw + (W - sbw) / 2, 26, "miko", 14, FG, "sans", 700, "middle") + text(sbw + (W - sbw) / 2, 44, "Astana, Kazakhstan", 11.5, FG3, "sans", 500, "middle"))
    bubbles = [("in", "hey, thanks for stopping by!", 0.5), ("in", "I build Swift apps and developer tools in Astana.", 1.7),
               ("typing", "", 2.9), ("in", "Say hi on Telegram @mikonyaa or at dev.miko@icloud.com", 4.3), ("out", "hi miko! 👋", 6.6)]
    y = 78
    mx0, mx1 = sbw + 26, W - 26
    for kind, msg, t0 in bubbles:
        if kind == "typing":
            bw, bh = 62, 34
            dots = "".join(f'<circle cx="{mx0+18+i*13}" cy="{y+17}" r="4" fill="#8e8e93">'
                           f'<animate attributeName="opacity" values="0.35;1;0.35" dur="1s" begin="{i*0.18:.2f}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="{EASE};{EASE}"/></circle>' for i in range(3))
            D.add(f'<g opacity="0">{C.ease("opacity", [(0, 0), (t0, 0), (t0 + 0.2, 1), (t0 + 1.2, 1), (t0 + 1.3, 0)])}'
                  f'<rect x="{mx0}" y="{y}" width="{bw}" height="{bh}" rx="17" fill="#2c2c33"/>{dots}</g>')
            continue
        fs = 15
        bw = tw(msg, fs, weight=500) + 30
        bh = 36
        out = kind == "out"
        bx = mx1 - bw if out else mx0
        fill = "#0a84ff" if out else "#2c2c33"
        ox = bx + bw if out else bx
        pop = C.ease_t("scale", [(0, "0.85"), (t0, "0.85"), (t0 + 0.28, "1"), (T_ := 13.0, "1")])
        tail = (f'<path d="M{f1(bx+bw-10)} {y+bh-12} q8 10 16 12 q-12 1 -20 -4z" fill="{fill}"/>' if out else
                f'<path d="M{f1(bx+10)} {y+bh-12} q-8 10 -16 12 q12 1 20 -4z" fill="{fill}"/>')
        body = (f'<rect x="{f1(bx)}" y="{y}" width="{f1(bw)}" height="{bh}" rx="18" fill="{fill}"/>{tail}'
                + text(bx + 15, y + 23.5, msg, fs, "#fff" if out else "#f2f2f7", "sans", 500))
        D.add(f'<g opacity="0">{C.show(t0, 12.4, fade=0.2)}<g transform="translate({f1(ox)} {y+bh})"><g>{pop}'
              f'<g transform="translate({f1(-ox)} {-(y+bh)})">{body}</g></g></g></g>')
        if out:
            D.add(f'<g opacity="0">{C.show(t0 + 0.7, 12.4, fade=0.2)}' + text(mx1, y + bh + 18, "Delivered", 11.5, FG3, "sans", 500, "end") + '</g>')
        y += bh + 10
    # input
    D.add(f'<rect x="{sbw+20}" y="{H-50}" width="{W-sbw-40}" height="32" rx="16" stroke="#3a3a42" fill="#1f1f24"/>'
          + text(sbw + 40, H - 29, "iMessage", 13.5, FG3, "sans", 500))
    return D.svg(title="Say hi", desc="A Messages conversation with miko: thanks for stopping by; say hi on Telegram @mikonyaa or at dev.miko@icloud.com.")
