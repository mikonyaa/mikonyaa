"""Hero 2: Xcode. ProfileView.swift on the left, the live canvas on the right showing the
profile as an iPhone app. The selected line of code and the selected element in the
preview move together, the way Xcode links them. One 16-second loop, no filters."""
from __future__ import annotations

import chibi
import data as gh
import wall
from desktop import menubar
from kit import (EASE, FG, FG2, FG3, Clock, Doc, app_icon, esc, f1, f3, shadow, squircle, text, tw, traffic)

W, H, HZ = 1200, 760, 640
T = 16.0
KW, TY, PT, ST, NU, PL, CM, FN = "#ff7ab2", "#dabaff", "#9ef1dd", "#ff8170", "#d9c97c", "#e6e6e6", "#7f8c98", "#67b7a4"


def code_lines(d):
    fol = f"{d['followers']}"
    return [
        [("import", KW), (" SwiftUI", PL)],
        [],
        [("struct", KW), (" ProfileView", "#5dd8ff"), (": ", PL), ("View", TY), (" {", PL)],
        [("    let", KW), (" miko = ", PL), ("Developer", PT), (".", PL), ("miko", FN)],
        [],
        [("    var", KW), (" body: ", PL), ("some", KW), (" View", TY), (" {", PL)],
        [("        NavigationStack", TY), (" {", PL)],
        [("            List", TY), (" {", PL)],
        [("                Header", PT), ("(name: ", PL), ('"miko"', ST), (",", PL)],
        [("                       role: ", PL), ('"Software, tools & side projects"', ST), (",", PL)],
        [("                       city: ", PL), ('"Astana, Kazakhstan"', ST), (")", PL)],
        [("                Stats", PT), ("(stars: ", PL), (str(d["stars"]), NU), (", followers: ", PL), (fol, NU), (", repos: ", PL), (str(d["repo_count"]), NU), (")", PL)],
        [("                Section", TY), ("(", PL), ('"Projects"', ST), (") {", PL)],
        [("                    ForEach", TY), ("(miko.", PL), ("projects", FN), (") { project ", PL), ("in", KW)],
        [("                        ProjectRow", PT), ("(project)", PL)],
        [("                    }", PL)],
        [("                }", PL)],
        [("            }", PL)],
        [("            .", PL), ("navigationTitle", FN), ("(", PL), ('"miko"', ST), (")", PL)],
        [("        }", PL)],
        [("        .", PL), ("tabBar", FN), ("(.", PL), ("liquidGlass", FN), (")", PL)],
        [("    }", PL)],
        [("}", PL)],
    ]


def toolbar(D, C, x, y, w):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="52" fill="#2a2a2e"/>', traffic(x + 20, y + 26),
           f'<path d="M{x} {y+52}H{x+w}" stroke="#000" stroke-opacity="0.5"/>']
    # sidebar toggle, run, stop
    bx = x + 100
    out.append(f'<rect x="{bx}" y="{y+18}" width="18" height="15" rx="3" stroke="#bdbdc2" stroke-width="1.4"/><path d="M{bx+6} {y+18}V{y+33}" stroke="#bdbdc2" stroke-width="1.4"/>')
    out.append(f'<path d="M{bx+52} {y+17} L{bx+66} {y+26} L{bx+52} {y+35}Z" fill="#e5e5ea"/>'
               f'<rect x="{bx+86}" y="{y+19}" width="13" height="13" rx="2" fill="#7c7c82"/>')
    # scheme
    sx = bx + 124
    out.append(f'<rect x="{sx}" y="{y+13}" width="216" height="26" rx="7" fill="#3a3a40" opacity="0.7"/>'
               + app_icon(D, "swift", sx + 7, y + 17, 18)
               + text(sx + 32, y + 30.5, "miko", 12.5, FG, "sans", 600) + text(sx + 66, y + 30.5, "›", 12.5, FG3, "sans", 600)
               + f'<rect x="{sx+80}" y="{y+19}" width="9" height="14" rx="2.2" stroke="#d1d1d6" stroke-width="1.3"/>'
               + text(sx + 96, y + 30.5, "iPhone 18 Pro", 12.5, FG, "sans", 500))
    # activity view: Building… → Build Succeeded
    ax, aw = x + w / 2 - 60, 330
    out.append(f'<rect x="{f1(ax)}" y="{y+12}" width="{aw}" height="28" rx="7" fill="#1c1c1f" stroke="#fff" stroke-opacity="0.08"/>')
    out.append(f'<g>{C.ease("opacity", [(0, 1), (2.2, 1), (2.5, 0), (T - 0.4, 0), (T - 0.1, 1)])}'
               + text(ax + 14, y + 30, "miko", 12.5, FG, "sans", 600) + text(ax + 52, y + 30, "Building miko…", 12.5, FG2, "sans", 500)
               + f'<rect x="{f1(ax+180)}" y="{y+23}" width="130" height="5" rx="2.5" fill="#3a3a40"/>'
               f'<rect x="{f1(ax+180)}" y="{y+23}" width="0" height="5" rx="2.5" fill="#0a84ff">'
               + C.ease("width", [(0, 0), (0.3, 0), (2.1, 130), (T, 130)]) + '</rect></g>')
    out.append(f'<g opacity="0">{C.ease("opacity", [(0, 0), (2.3, 0), (2.6, 1), (T - 0.4, 1), (T - 0.1, 0)])}'
               + text(ax + 14, y + 30, "miko", 12.5, FG, "sans", 600)
               + text(ax + 52, y + 30, "Build Succeeded", 12.5, FG2, "sans", 500)
               + f'<circle cx="{f1(ax+165)}" cy="{y+26}" r="6" fill="#30d158"/><path d="M{f1(ax+162)} {y+26} l2.2 2.2 l4 -4.4" stroke="#fff" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
               + text(ax + aw - 14, y + 30, "Today at 09:41", 12.5, FG3, "sans", 500, "end") + '</g>')
    # right buttons
    rx = x + w - 30
    out.append(f'<path d="M{rx-7} {y+26}h14M{rx} {y+19}v14" stroke="#bdbdc2" stroke-width="1.6" stroke-linecap="round"/>'
               f'<rect x="{rx-44}" y="{y+19}" width="16" height="14" rx="3" stroke="#bdbdc2" stroke-width="1.4"/><path d="M{rx-34} {y+19}V{y+33}" stroke="#bdbdc2" stroke-width="1.4"/>')
    return "".join(out)


def navigator(D, x, y, w, h):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#222226"/>', f'<path d="M{x+w} {y}V{y+h}" stroke="#000" stroke-opacity="0.5"/>']
    # navigator tabs
    for i in range(7):
        ix = x + 18 + i * 27
        col = "#0a84ff" if i == 0 else "#8e8e93"
        out.append(f'<rect x="{ix}" y="{y+11}" width="13" height="11" rx="2" stroke="{col}" stroke-width="1.4"/>' if i == 0 else
                   f'<circle cx="{ix+6}" cy="{y+16.5}" r="5" stroke="{col}" stroke-width="1.3" opacity="0.8"/>')
    out.append(f'<path d="M{x} {y+32}H{x+w}" stroke="#000" stroke-opacity="0.4"/>')
    rows = [(0, "proj", "miko", False), (1, "folder", "Sources", False), (2, "swift", "ProfileView.swift", True),
            (2, "swift", "ProjectRow.swift", False), (2, "swift", "Stats.swift", False), (2, "swift", "Developer.swift", False),
            (1, "folder", "Packages", False), (2, "pkg", "LiquidGlassTabBars", False), (2, "pkg", "AdaptiveAppShell", False),
            (1, "folder", "Resources", False), (2, "assets", "Assets.xcassets", False), (1, "test", "mikoTests", False)]
    for i, (lvl, kind, name, sel) in enumerate(rows):
        ry = y + 52 + i * 24
        ix = x + 14 + lvl * 16
        if sel:
            out.append(f'<rect x="{x+8}" y="{ry-15}" width="{w-16}" height="22" rx="5" fill="#0a5bd8"/>')
        if lvl < 2 and kind == "folder":
            out.append(f'<path d="M{ix-8} {ry-7} l3.5 3.5 l3.5 -3.5" stroke="#8e8e93" stroke-width="1.3" fill="none" stroke-linecap="round"/>')
        gx = ix + 2
        if kind == "swift":
            out.append(f'<rect x="{gx}" y="{ry-12}" width="13" height="15" rx="2.5" fill="#ff7a3d"/><path d="M{gx+3} {ry-6} q4 4 8 -1" stroke="#fff" stroke-width="1.4" fill="none"/>')
        elif kind == "folder":
            out.append(f'<path d="M{gx} {ry-11} h5 l2 2 h7 v10 h-14z" fill="#5aa7f0"/>')
        elif kind == "proj":
            out.append(f'<rect x="{gx}" y="{ry-12}" width="14" height="15" rx="3" fill="#2f74e8"/><path d="M{gx+4} {ry-7} h6 M{gx+4} {ry-4} h6 M{gx+4} {ry-1} h4" stroke="#fff" stroke-width="1.2"/>')
        elif kind == "pkg":
            out.append(f'<path d="M{gx+7} {ry-13} l7 3.5 v8 l-7 3.5 l-7 -3.5 v-8z" fill="#c69460"/><path d="M{gx} {ry-9.5} l7 3.5 l7 -3.5 M{gx+7} {ry-6} v9" stroke="#7a5530" stroke-width="1"/>')
        elif kind == "assets":
            out.append(f'<rect x="{gx}" y="{ry-12}" width="14" height="14" rx="3" fill="#5ac8fa"/><circle cx="{gx+7}" cy="{ry-5}" r="3" fill="#fff"/>')
        else:
            out.append(f'<path d="M{gx} {ry-11} h5 l2 2 h7 v10 h-14z" fill="#8e8e93"/>')
        out.append(text(gx + 20, ry, name, 12.5, "#ffffff" if sel else "#d1d1d6", "sans", 600 if lvl == 0 else 500))
    # filter field
    out.append(f'<path d="M{x} {y+h-34}H{x+w}" stroke="#000" stroke-opacity="0.4"/>'
               f'<rect x="{x+10}" y="{y+h-26}" width="{w-20}" height="20" rx="6" fill="#2e2e33"/>' + text(x + 30, y + h - 12, "Filter", 11.5, FG3, "sans", 500)
               + f'<circle cx="{x+21}" cy="{y+h-16.5}" r="3.5" stroke="#8e8e93" stroke-width="1.2"/>')
    return "".join(out)


def editor(D, C, d, x, y, w, h, sel_steps):
    lines = code_lines(d)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#1f1f24"/>']
    # tab + jump bar
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="28" fill="#2a2a2e"/><path d="M{x} {y+28}H{x+w}" stroke="#000" stroke-opacity="0.4"/>'
               f'<rect x="{x+8}" y="{y+4}" width="170" height="21" rx="5" fill="#3a3a40"/>'
               f'<rect x="{x+18}" y="{y+8}" width="11" height="13" rx="2" fill="#ff7a3d"/>' + text(x + 36, y + 19, "ProfileView.swift", 12, FG, "sans", 600))
    jb = ["miko", "Sources", "ProfileView.swift", "body"]
    jx = x + 14
    for i, part in enumerate(jb):
        out.append(text(jx, y + 46, part, 11.5, FG2 if i < 3 else FG, "sans", 500))
        jx += tw(part, 11.5, weight=500) + 8
        if i < 3:
            out.append(text(jx - 2, y + 46, "›", 11.5, FG3, "sans", 500))
            jx += 10
    out.append(f'<path d="M{x} {y+54}H{x+w}" stroke="#000" stroke-opacity="0.35"/>')
    fs, lh = 12.4, 19.2
    top = y + 76
    gut = x + 40
    # current-line highlight, moves with the selection
    ys = [(t, round(top + (ln - 1) * lh - 14, 1), round(n * lh, 1)) for t, ln, n, *_ in sel_steps]
    out.append(f'<rect x="{x}" y="{ys[0][1]}" width="{w}" height="{ys[0][2]}" fill="#2f3b52" opacity="0.85">'
               + C.ease("y", [(t, v) for t, v, _ in ys]) + C.ease("height", [(t, v) for t, _, v in ys]) + '</rect>')
    for i, toks in enumerate(lines):
        ly = top + i * lh
        out.append(text(gut - 10, ly, str(i + 1), 11, "#5a5a63", "mono", 400, "end"))
        if toks:
            spans = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in toks)
            out.append(f'<text x="{gut+6}" y="{f1(ly)}" class="mono" font-size="{fs}" xml:space="preserve">{spans}</text>')
    # caret at the end of the selected line
    cx_vals = []
    for t, ln, n, *_ in sel_steps:
        L = sum(len(s) for s, _ in lines[ln - 1])
        cx_vals.append((t, round(gut + 6 + L * fs * 0.602 + 2, 1), round(top + (ln - 1) * lh - 11.5, 1)))
    out.append(f'<rect x="{cx_vals[0][1]}" y="{cx_vals[0][2]}" width="1.6" height="15" fill="#fff">'
               + C.ease("x", [(t, v) for t, v, _ in cx_vals]) + C.ease("y", [(t, v) for t, _, v in cx_vals])
               + '<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.45;0.5;0.95;1" dur="1.1s" repeatCount="indefinite"/></rect>')
    # minimap strip
    mx = x + w - 52
    out.append(f'<rect x="{mx}" y="{y+56}" width="1" height="{h-56}" fill="#000" opacity="0.35"/>')
    for i, toks in enumerate(lines):
        ox = mx + 8
        for s, c in toks:
            ln_ = len(s.rstrip())
            lead = len(s) - len(s.lstrip())
            if ln_ - lead > 0:
                out.append(f'<rect x="{f1(ox+lead*0.9)}" y="{f1(y+64+i*3.4)}" width="{f1((ln_-lead)*0.9)}" height="2" fill="{c}" opacity="0.55"/>')
            ox += len(s) * 0.9
    return "".join(out)


def phone_screen(D, C, d, sx, sy, sw, sh, sel_steps):
    p = D.p
    out = [f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="34" fill="#000"/>']
    D.adddef(f'<clipPath id="{p}-scr"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="34"/></clipPath>')
    s = []
    # status bar + island
    s.append(text(sx + 30, sy + 24, "9:41", 13, FG, "sans", 700))
    s.append(f'<rect x="{sx+sw/2-38}" y="{sy+9}" width="76" height="22" rx="11" fill="#000" stroke="#1c1c1e"/>')
    s.append(f'<g transform="translate({sx+sw-62} {sy+15})" fill="#fff"><rect x="0" y="6" width="3" height="4" rx="1"/><rect x="4.5" y="4" width="3" height="6" rx="1"/>'
             f'<rect x="9" y="2" width="3" height="8" rx="1"/><rect x="22" y="1" width="20" height="10" rx="3" fill="none" stroke="#fff" stroke-opacity="0.6"/>'
             f'<rect x="24" y="3" width="14" height="6" rx="1.5"/></g>')
    # large title + avatar
    s.append(text(sx + 18, sy + 86, "miko", 32, FG, "sans", 800, extra=' letter-spacing="-0.6"'))
    s.append(text(sx + 18, sy + 106, "Software, tools & side projects", 11.5, "#98989f", "sans", 500))
    s.append(f'<g transform="translate({sx+18} {sy+114})"><path d="M5 0 a5 5 0 0 1 5 5 c0 4 -5 9 -5 9 s-5 -5 -5 -9 a5 5 0 0 1 5 -5z" fill="#0a84ff"/>'
             f'<circle cx="5" cy="5" r="1.8" fill="#000"/></g>' + text(sx + 34, sy + 126, "Astana, Kazakhstan", 11.5, "#d1d1d6", "sans", 500))
    acx, acy, ar = sx + sw - 40, sy + 62, 22
    D.adddef(f'<clipPath id="{p}-pav"><circle cx="{acx}" cy="{acy}" r="{ar}"/></clipPath>',
             f'<linearGradient id="{p}-pavbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fb4ff"/><stop offset="1" stop-color="#ff9fb0"/></linearGradient>')
    s.append(f'<circle cx="{acx}" cy="{acy}" r="{ar}" fill="url(#{p}-pavbg)"/><g clip-path="url(#{p}-pav)">{chibi.bust(acx, acy-1, 0.31, p+"pa", smile="open")}</g>')
    # stats
    stats = [(str(d["stars"]), "Stars"), (f"{d['followers']/1000:.1f}k", "Followers"), (str(d["repo_count"]), "Repos")]
    pw = (sw - 36 - 16) / 3
    for i, (v, k) in enumerate(stats):
        px = sx + 18 + i * (pw + 8)
        s.append(f'<rect x="{f1(px)}" y="{sy+142}" width="{f1(pw)}" height="52" rx="14" fill="#1c1c1e"/>'
                 + text(px + pw / 2, sy + 166, v, 17, FG, "sans tnum", 700, "middle") + text(px + pw / 2, sy + 183, k, 10.5, "#8e8e93", "sans", 500, "middle"))
    # projects list
    s.append(text(sx + 30, sy + 220, "PROJECTS", 10.5, "#8e8e93", "sans", 600, extra=' letter-spacing="0.6"'))
    rows = [("templates", "Apple Design Templates", "SwiftUI templates"), ("tabbar", "Liquid Glass Tab Bars", "Floating tab bars"),
            ("shell", "Adaptive App Shell", "iPhone · iPad shell"), ("resize", "ResizeLint", "Swift static analysis")]
    by = {r["name"]: r for r in d["repos"]}
    repo = {"templates": "Apple-Design-Templates", "tabbar": "LiquidGlassTabBars", "shell": "AdaptiveAppShell", "resize": "ResizeLint"}
    ly0, rh = sy + 228, 48
    s.append(f'<rect x="{sx+14}" y="{ly0}" width="{sw-28}" height="{rh*len(rows)}" rx="14" fill="#1c1c1e"/>')
    for i, (k, name, sub) in enumerate(rows):
        ry = ly0 + i * rh
        stars = by.get(repo[k], {}).get('stars', 0)
        s.append(app_icon(D, k, sx + 26, ry + 10, 28) + text(sx + 64, ry + 23, name, 12, FG, "sans", 600)
                 + text(sx + 64, ry + 38, f"{sub} · ★ {stars}", 10.5, "#8e8e93", "sans", 500)
                 + f'<path d="M{sx+sw-30} {ry+21} l4 4 l-4 4" stroke="#5a5a5f" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
        if i < len(rows) - 1:
            s.append(f'<path d="M{sx+64} {ry+rh}H{sx+sw-14}" stroke="#38383a"/>')
    # floating glass tab bar
    tbx, tby, tbw, tbh = sx + 16, sy + sh - 74, sw - 32, 54
    s.append(f'<rect x="{tbx}" y="{tby+4}" width="{tbw}" height="{tbh}" rx="27" fill="#000" opacity="0.4"/>'
             f'<rect x="{tbx}" y="{tby}" width="{tbw}" height="{tbh}" rx="27" fill="#2c2c30" opacity="0.92"/>'
             f'<rect x="{tbx+0.5}" y="{tby+0.5}" width="{tbw-1}" height="{tbh-1}" rx="26.5" stroke="#fff" stroke-opacity="0.18"/>')
    tabs = ["Profile", "Projects", "Stats", "Settings"]
    tw_ = (tbw - 8) / 4
    pill_x = [(0, tbx + 4), (11.6, tbx + 4), (12.2, tbx + 4 + tw_), (13.4, tbx + 4 + tw_), (14.0, tbx + 4 + 2 * tw_),
              (15.0, tbx + 4 + 2 * tw_), (15.6, tbx + 4)]
    s.append(f'<rect x="{tbx+4}" y="{tby+4}" width="{f1(tw_)}" height="{tbh-8}" rx="23" fill="#fff" opacity="0.14">'
             + C.ease("x", [(t, round(v, 1)) for t, v in pill_x]) + '</rect>')
    glyphs = ["M-5 -2 a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0 M-8 9 q8 -8 16 0", "M-7 -6 h14 v12 h-14z M-7 -2 h14",
              "M-7 6 v-4 M-2 6 v-9 M3 6 v-6 M8 6 v-12", "M0 -7 a7 7 0 1 0 0.1 0 M0 -3 a3 3 0 1 0 0.1 0"]
    for i, (lab, g) in enumerate(zip(tabs, glyphs)):
        cx = tbx + 4 + tw_ * i + tw_ / 2
        s.append(f'<path d="{g}" transform="translate({f1(cx)} {tby+20})" stroke="#fff" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                 + text(cx, tby + 43, lab, 9.5, "#e5e5ea", "sans", 600, "middle"))
    s.append(f'<rect x="{sx+sw/2-50}" y="{sy+sh-9}" width="100" height="4" rx="2" fill="#fff" opacity="0.8"/>')
    out.append(f'<g clip-path="url(#{p}-scr)">{"".join(s)}</g>')
    # Xcode canvas selection: a blue outline that follows the selected code line
    boxes = []
    for t, ln, n, (bx, by_, bw, bh) in sel_steps:
        boxes.append((t, sx + bx, sy + by_, bw, bh))
    out.append(f'<rect x="{f1(boxes[0][1])}" y="{f1(boxes[0][2])}" width="{boxes[0][3]}" height="{boxes[0][4]}" rx="8" stroke="#0a84ff" stroke-width="2" fill="#0a84ff" fill-opacity="0.08">'
               + C.ease("x", [(t, round(x_, 1)) for t, x_, *_ in boxes]) + C.ease("y", [(t, round(y_, 1)) for t, _, y_, *_ in boxes])
               + C.ease("width", [(t, w_) for t, _, _, w_, _ in boxes]) + C.ease("height", [(t, h_) for t, *_, h_ in boxes]) + '</rect>')
    return "".join(out)


def xcode(d):
    D = Doc(W, H, "xc", r=14)
    C = Clock(T)
    D.add(wall.wallpaper(D, W, H, HZ, "night", seed=11, sun_x=0.5))
    D.add(menubar(D, d, app="Xcode", items=("File", "Edit", "View", "Find", "Navigate", "Editor", "Product", "Debug", "Window", "Help")))
    x, y, w, h = 22, 42, W - 44, H - 42 - 22
    D.adddef(f'<clipPath id="xc-win"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/></clipPath>')
    D.add(shadow(x, y, w, h, 12))
    nav_w, can_w = 200, 376
    ed_x, ed_w = x + nav_w, w - nav_w - can_w
    cv_x = x + w - can_w
    body_y, body_h = y + 52, h - 52
    sw, sh = 252, 540
    sx, sy = cv_x + (can_w - sw) / 2, body_y + 54
    # selection steps: (time, first line, n lines, preview box in screen coords)
    steps = [(0.0, 9, 3, (8, 34, sw - 16, 102)), (2.6, 9, 3, (8, 34, sw - 16, 102)), (3.2, 12, 1, (12, 138, sw - 24, 60)),
             (5.8, 12, 1, (12, 138, sw - 24, 60)), (6.4, 13, 4, (10, 206, sw - 20, 222)), (9.6, 13, 4, (10, 206, sw - 20, 222)),
             (10.2, 21, 1, (12, sh - 78, sw - 24, 62)), (15.4, 21, 1, (12, sh - 78, sw - 24, 62)), (15.95, 9, 3, (8, 34, sw - 16, 102))]
    inner = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#1f1f24"/>',
             toolbar(D, C, x, y, w),
             navigator(D, x, body_y, nav_w, body_h),
             editor(D, C, d, ed_x, body_y, ed_w, body_h, steps),
             f'<rect x="{cv_x}" y="{body_y}" width="{can_w}" height="{body_h}" fill="#2b2b30"/>'
             f'<path d="M{cv_x} {body_y}V{y+h}" stroke="#000" stroke-opacity="0.5"/>']
    # canvas dots + preview pill
    dots = "".join(f'<circle cx="{cv_x+12+i*24}" cy="{body_y+12+j*24}" r="0.9" fill="#fff" opacity="0.07"/>'
                   for i in range(16) for j in range(int(body_h / 24)))
    inner.append(dots)
    inner.append(f'<rect x="{cv_x+can_w/2-70}" y="{body_y+14}" width="140" height="26" rx="13" fill="#3a3a40"/>'
                 f'<circle cx="{cv_x+can_w/2-52}" cy="{body_y+27}" r="4" fill="#30d158"><animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/></circle>'
                 + text(cv_x + can_w / 2 + 6, body_y + 31.5, "ProfileView · Live", 12, FG, "sans", 600, "middle"))
    # phone
    inner.append(f'<rect x="{sx-9}" y="{sy-9}" width="{sw+18}" height="{sh+18}" rx="43" fill="#000" opacity="0.45" transform="translate(0 10)"/>'
                 f'<rect x="{sx-9}" y="{sy-9}" width="{sw+18}" height="{sh+18}" rx="43" fill="#1a1a1c" stroke="#5a5a60" stroke-width="2"/>')
    inner.append(phone_screen(D, C, d, sx, sy, sw, sh, steps))
    # canvas bottom bar
    inner.append(f'<rect x="{cv_x}" y="{y+h-34}" width="{can_w}" height="34" fill="#252529"/>'
                 + text(cv_x + 16, y + h - 12, "▶︎  ⧉  ⚙︎", 12, "#8e8e93", "sans", 500) + text(cv_x + can_w - 16, y + h - 12, "75%", 12, "#8e8e93", "sans tnum", 600, "end"))
    D.add(f'<g clip-path="url(#xc-win)">{"".join(inner)}</g>'
          f'<rect x="{x+0.5}" y="{y+0.5}" width="{w-1}" height="{h-1}" rx="11.5" stroke="#fff" stroke-opacity="0.14"/>'
          f'<rect x="{x-0.5}" y="{y-0.5}" width="{w+1}" height="{h+1}" rx="12.5" stroke="#000" stroke-opacity="0.6"/>')
    return D.svg(title="miko in Xcode", desc="Xcode with ProfileView.swift and a live iPhone preview of miko's profile: stats, projects and a floating tab bar.")
