"""Swift Playgrounds: a page called "Ship It". A for loop walks Miko across a small isometric island,
picks up three gems and toggles the switch; the current line is highlighted as the code runs."""
from __future__ import annotations

import random

import chibi
from kit import FG, FG2, FG3, MONO_ADV, Clock, Doc, esc, f1, text, traffic, tw


def _pop(ax, ay, inner, C, t0, t_off=None, start=0.4):
    """Scale `inner` up from (ax, ay) at t0 with a small overshoot."""
    T = C.T
    t_off = T - 0.6 if t_off is None else t_off
    s = [(0, start), (t0, start), (t0 + 0.22, 1.07), (t0 + 0.36, 1), (t_off, 1), (t_off + 0.3, start)]
    o = [(0, 0), (t0, 0), (t0 + 0.12, 1), (t_off, 1), (t_off + 0.3, 0)]
    sv = [(t, f"{v} {v}") for t, v in s]
    return (f'<g opacity="0">{C.ease("opacity", o)}<g transform="translate({f1(ax)} {f1(ay)})"><g>{C.ease_t("scale", sv)}'
            f'<g transform="translate({f1(-ax)} {f1(-ay)})">{inner}</g></g></g></g>')


HW, HH, SH = 54, 27, 30          # iso tile half-width, half-height, side height


def _iso(ox, oy, c, r, lvl=0):
    return ox + (c - r) * HW, oy + (c + r) * HH - lvl * SH


def _block(x, y, top="#7ed957", lip="#5fbf3c", left="#b9824f", right="#93623a", lip_h=7):
    t = f"M{f1(x)} {f1(y-HH)} L{f1(x+HW)} {f1(y)} L{f1(x)} {f1(y+HH)} L{f1(x-HW)} {f1(y)}Z"
    lf = f"M{f1(x-HW)} {f1(y)} L{f1(x)} {f1(y+HH)} L{f1(x)} {f1(y+HH+SH)} L{f1(x-HW)} {f1(y+SH)}Z"
    rt = f"M{f1(x)} {f1(y+HH)} L{f1(x+HW)} {f1(y)} L{f1(x+HW)} {f1(y+SH)} L{f1(x)} {f1(y+HH+SH)}Z"
    lipl = f"M{f1(x-HW)} {f1(y)} L{f1(x)} {f1(y+HH)} L{f1(x)} {f1(y+HH+lip_h)} L{f1(x-HW)} {f1(y+lip_h)}Z"
    lipr = f"M{f1(x)} {f1(y+HH)} L{f1(x+HW)} {f1(y)} L{f1(x+HW)} {f1(y+lip_h)} L{f1(x)} {f1(y+HH+lip_h)}Z"
    return (f'<path d="{lf}" fill="{left}"/><path d="{rt}" fill="{right}"/>'
            + (f'<path d="{lipl}" fill="{lip}"/><path d="{lipr}" fill="{lip}" opacity="0.85"/>' if lip_h else "")
            + f'<path d="{t}" fill="{top}"/>'
            f'<path d="M{f1(x-HW)} {f1(y)} L{f1(x)} {f1(y-HH)} L{f1(x+HW)} {f1(y)}" stroke="#fff" stroke-opacity="0.35" stroke-width="1.5" fill="none"/>'
            f'<path d="M{f1(x)} {f1(y+HH)} V{f1(y+HH+SH)}" stroke="#000" stroke-opacity="0.12"/>')


def _gem(x, y, s=1.0):
    k = s
    return (f'<path d="M{x} {f1(y-17*k)} L{f1(x+12*k)} {y} L{x} {f1(y+17*k)} L{f1(x-12*k)} {y}Z" fill="#e0349f"/>'
            f'<path d="M{x} {f1(y-17*k)} L{f1(x-12*k)} {y} L{x} {f1(y+3*k)}Z" fill="#ff8fe0"/>'
            f'<path d="M{x} {f1(y-17*k)} L{f1(x+12*k)} {y} L{x} {f1(y+3*k)}Z" fill="#ff5cc6"/>'
            f'<path d="M{f1(x-12*k)} {y} L{x} {f1(y+17*k)} L{x} {f1(y+3*k)}Z" fill="#c21f86"/>'
            f'<path d="M{f1(x-5*k)} {f1(y-8*k)} L{f1(x-1*k)} {f1(y-12*k)}" stroke="#fff" stroke-width="{f1(2*k)}" stroke-linecap="round" opacity="0.85"/>')


def _tree(x, y):
    return (f'<ellipse cx="{x+4}" cy="{y+2}" rx="20" ry="9" fill="#000" opacity="0.15"/>'
            f'<path d="M{x-4} {y} v-26 h8 v26z" fill="#8a5a36"/>'
            f'<circle cx="{x}" cy="{y-46}" r="25" fill="#3f9a3a"/><circle cx="{x-11}" cy="{y-36}" r="17" fill="#4fb046"/>'
            f'<circle cx="{x+10}" cy="{y-56}" r="14" fill="#5cc451"/><circle cx="{x-6}" cy="{y-58}" r="8" fill="#7ad86a" opacity="0.8"/>')


def playground(d):
    W, H = 1200, 640
    T = 15.4
    D = Doc(W, H, "pg", r=16, bg="#1c1c1e")
    C = Clock(T)
    p = D.p
    # toolbar
    D.add(f'<rect width="{W}" height="56" fill="#2a2a2d"/><path d="M0 56H{W}" stroke="#000" stroke-opacity="0.5"/>' + traffic(26, 28)
          + f'<rect x="92" y="19" width="22" height="18" rx="4" stroke="#a1a1aa" stroke-width="1.6"/><path d="M100 19v18" stroke="#a1a1aa" stroke-width="1.6"/>'
          + text(W / 2, 33, "Ship It", 15, FG, "sans", 700, "middle")
          + "".join(f'<circle cx="{W-60+i*9}" cy="28" r="1.8" fill="#a1a1aa"/>' for i in range(3)))
    # ---------------- code pane
    LX, LW = 0, 562
    D.add(f'<rect x="{LX}" y="56" width="{LW}" height="{H-56}" fill="#1f1f22"/><path d="M{LW} 56V{H}" stroke="#000" stroke-opacity="0.5"/>')
    D.add(f'<rect x="24" y="78" width="{LW-48}" height="62" rx="12" fill="#2a2a2f"/>' + _gem(52, 109, 0.85)
          + text(74, 104, "Goal", 15, FG, "sans", 800) + text(74, 126, "Collect every gem, then toggle the switch.", 15, FG2, "sans", 500))
    code = [[("// Walk the path, grab every gem.", "#6c7986")],
            [("for", "#fc5fa3"), (" step ", "#f5f5f7"), ("in", "#fc5fa3"), (" ", "#fff"), ("1", "#d0bf69"), ("...", "#f5f5f7"), ("3", "#d0bf69"), (" {", "#f5f5f7")],
            [("    moveForward", "#67b7a4"), ("()", "#f5f5f7")],
            [("    collectGem", "#67b7a4"), ("()", "#f5f5f7")],
            [("    turnRight", "#67b7a4"), ("()", "#f5f5f7")],
            [("    moveForward", "#67b7a4"), ("()", "#f5f5f7")],
            [("    turnLeft", "#67b7a4"), ("()", "#f5f5f7")],
            [("}", "#f5f5f7")],
            [("toggleSwitch", "#67b7a4"), ("()", "#f5f5f7")]]
    CS, LH, CY0, CX = 20, 42, 194, 78
    line_y = lambda i: CY0 + i * LH
    # current-line highlight (moves while the code runs)
    t = 1.05
    seq = []
    pos = [(0, 0)]
    path = [(0.0, 0, 0)]
    turns = []
    gems_t = []
    for it in range(3):
        seq.append((t, 1)); t += 0.32
        seq.append((t, 2)); c0, r0 = pos[-1]; c1, r1 = c0 + 1, r0; path += [(t, c0, r0), (t + 0.8, c1, r1)]; pos.append((c1, r1)); t += 0.8
        seq.append((t, 3)); gems_t.append(t + 0.12); t += 0.55
        seq.append((t, 4)); turns.append((t, 1)); t += 0.45
        seq.append((t, 5)); c0, r0 = pos[-1]; c1, r1 = c0, r0 + 1; path += [(t, c0, r0), (t + 0.8, c1, r1)]; pos.append((c1, r1)); t += 0.8
        seq.append((t, 6)); turns.append((t, -1)); t += 0.45
    seq.append((t, 8)); t_sw = t + 0.2; t += 0.6
    t_end = t
    hy = [(0, line_y(1) - 28)]
    for k, (ts, ln) in enumerate(seq):
        y_ = line_y(ln) - 28
        hy += [(ts, hy[-1][1]), (ts + 0.12, y_)]
    hl_op = C.ease("opacity", [(0, 0), (1.0, 0), (1.1, 1), (t_end, 1), (t_end + 0.3, 0)])
    D.add(f'<g opacity="0">{hl_op}<rect x="16" y="{line_y(1)-28}" width="{LW-32}" height="39" rx="8" fill="#ffd60a" opacity="0.14">{C.ease("y", hy)}</rect>'
          f'<rect x="16" y="{line_y(1)-28}" width="4" height="39" rx="2" fill="#ffd60a">{C.ease("y", hy)}</rect></g>')
    for i, toks in enumerate(code):
        D.add(text(46, line_y(i), str(i + 1), 14, FG3, "mono", 500, "end"))
        x = CX
        parts = []
        for s_, col in toks:
            parts.append(f'<tspan fill="{col}">{esc(s_)}</tspan>')
            x += len(s_) * CS * MONO_ADV
        D.add(f'<text x="{CX}" y="{line_y(i)}" class="mono" font-size="{CS}" xml:space="preserve">{"".join(parts)}</text>')
    # shortcut bar
    D.add(f'<path d="M0 {H-72}H{LW}" stroke="#fff" stroke-opacity="0.06"/>')
    sx = 22
    for lab in ("moveForward()", "turnLeft()", "collectGem()", "toggleSwitch()"):
        w_ = tw(lab, 14, mono=True) + 22
        D.add(f'<rect x="{f1(sx)}" y="{H-54}" width="{f1(w_)}" height="34" rx="9" fill="#2c2c31" stroke="#fff" stroke-opacity="0.08"/>'
              + text(sx + 11, H - 32, lab, 14, "#67b7a4", "mono", 500))
        sx += w_ + 9
    # ---------------- live view
    VX, VY, VW, VH = 574, 68, 614, 560
    D.adddef(f'<clipPath id="{p}-lv"><rect x="{VX}" y="{VY}" width="{VW}" height="{VH}" rx="14"/></clipPath>',
             f'<linearGradient id="{p}-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5ec4f5"/><stop offset="0.7" stop-color="#b8ecff"/>'
             f'<stop offset="1" stop-color="#d9f6ff"/></linearGradient>',
             f'<linearGradient id="{p}-water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2fa7ea"/><stop offset="1" stop-color="#1f7fc7"/></linearGradient>')
    L = [f'<rect x="{VX}" y="{VY}" width="{VW}" height="{VH}" fill="url(#{p}-sky)"/>']
    rng = random.Random(9)
    for cx_, cy_, s_ in ((660, 118, 1.0), (1080, 150, 0.8), (930, 96, 0.6)):
        L.append(f'<g opacity="0.9"><animateTransform attributeName="transform" type="translate" values="0 0;24 0;0 0" dur="{18+s_*6:.0f}s" repeatCount="indefinite"/>'
                 f'<ellipse cx="{cx_}" cy="{cy_}" rx="{f1(46*s_)}" ry="{f1(14*s_)}" fill="#fff"/><circle cx="{f1(cx_-12*s_)}" cy="{f1(cy_-10*s_)}" r="{f1(18*s_)}" fill="#fff"/>'
                 f'<circle cx="{f1(cx_+14*s_)}" cy="{f1(cy_-6*s_)}" r="{f1(14*s_)}" fill="#fff"/></g>')
    ox, oy = 880, 232
    # water plane under the island
    wx, wy = _iso(ox, oy, 2, 2)
    wd = f"M{wx} {wy-HH*7+SH} L{wx+HW*7} {wy+SH} L{wx} {wy+HH*7+SH} L{wx-HW*7} {wy+SH}Z"
    L.append(f'<path d="{wd}" fill="url(#{p}-water)"/>')
    for k in range(9):
        a, b = rng.uniform(-5, 5), rng.uniform(-4, 4)
        x1, y1 = _iso(ox, oy, 2 + a, 2 + b)
        L.append(f'<path d="M{f1(x1-14)} {f1(y1+SH+4)} q7 -4 14 0 q7 4 14 0" stroke="#bfe9ff" stroke-width="2" fill="none" stroke-linecap="round" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0.8;0" dur="{rng.uniform(2.4, 3.6):.1f}s" begin="{rng.uniform(0, 3):.1f}s" repeatCount="indefinite"/></path>')
    holes = {(0, 4), (4, 4), (0, 3)}
    raised = {(4, 0)}
    trees = {(4, 2), (1, 3)}
    gems = [(1, 0), (2, 1), (3, 2)]
    sw = (3, 3)
    for dep in range(9):
        for c in range(5):
            r = dep - c
            if not 0 <= r < 5 or (c, r) in holes:
                continue
            x, y = _iso(ox, oy, c, r)
            if (c, r) in raised:
                L.append(_block(x, y, "#c7ccd6", "#c7ccd6", "#9aa1b0", "#7d8495", lip_h=0))
                L.append(_block(x, y - SH, "#d9dee8", "#d9dee8", "#aab1c0", "#8a91a2", lip_h=0))
            else:
                L.append(_block(x, y))
            if (c, r) in trees:
                L.append(_tree(x + 4, y + 4))
    # switch
    sx_, sy_ = _iso(ox, oy, *sw)
    plate = f"M{sx_} {sy_-13} L{sx_+26} {sy_} L{sx_} {sy_+13} L{sx_-26} {sy_}Z"
    inner = f"M{sx_} {sy_-7} L{sx_+14} {sy_} L{sx_} {sy_+7} L{sx_-14} {sy_}Z"
    L.append(f'<path d="{plate}" fill="#3b3f4c"/><path d="{plate}" stroke="#20232b" stroke-width="2" fill="none"/><path d="{inner}" fill="#5a6070"/>'
             f'<g opacity="0">{C.ease("opacity", [(0, 0), (t_sw, 0), (t_sw + 0.15, 1), (T - 0.35, 1), (T - 0.1, 0)])}'
             f'<ellipse cx="{sx_}" cy="{sy_}" rx="44" ry="22" fill="#ffe066" opacity="0.45"/><path d="{inner}" fill="#ffe066"/>'
             f'<path d="M{sx_} {sy_-9} V{sy_-60}" stroke="#fff3b0" stroke-width="10" opacity="0.35" stroke-linecap="round"/></g>')
    # gems
    for k, (gc, gr) in enumerate(gems):
        gx, gy = _iso(ox, oy, gc, gr)
        tg = gems_t[k]
        L.append(f'<ellipse cx="{gx}" cy="{gy}" rx="12" ry="5" fill="#000" opacity="0.18">'
                 + C.ease("opacity", [(0, 0), (0.3, 0.18), (tg, 0.18), (tg + 0.15, 0)]) + '</ellipse>')
        spin = ('<animateTransform attributeName="transform" type="scale" values="1 1;0.5 1;1 1" dur="1.8s" repeatCount="indefinite" '
                'calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>')
        bob = ('<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="2.2s" repeatCount="indefinite" '
               f'begin="{k*0.4}s" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>')
        col = (C.ease("opacity", [(0, 0), (0.3, 1), (tg, 1), (tg + 0.35, 0)])
               + C.ease_t("translate", [(0, "0 0"), (tg, "0 0"), (tg + 0.35, "0 -34")]))
        L.append(f'<g opacity="0">{col}<g transform="translate({gx} {gy-30})"><g>{bob}<g>{spin}{_gem(0, 0, 1.15)}</g></g></g></g>')
        # sparkle
        sp = "".join(f'<path d="M{f1(gx+dx)} {f1(gy-30+dy-6)} L{f1(gx+dx+1.6)} {f1(gy-30+dy-1.6)} L{f1(gx+dx+6)} {f1(gy-30+dy)} L{f1(gx+dx+1.6)} {f1(gy-30+dy+1.6)} '
                     f'L{f1(gx+dx)} {f1(gy-30+dy+6)} L{f1(gx+dx-1.6)} {f1(gy-30+dy+1.6)} L{f1(gx+dx-6)} {f1(gy-30+dy)} L{f1(gx+dx-1.6)} {f1(gy-30+dy-1.6)}Z" fill="#fff"/>'
                     for dx, dy in ((-22, -14), (20, -20), (24, 12), (-18, 16)))
        L.append(f'<g opacity="0">{C.ease("opacity", [(0, 0), (tg + 0.05, 0), (tg + 0.15, 1), (tg + 0.55, 0)])}{sp}</g>')
    # Miko walks the path
    s = 0.39
    foot = 176 * s
    tr = []
    for (ta, ca, ra), (tb, cb, rb) in zip(path[1::2], path[2::2]):
        xa, ya = _iso(ox, oy, ca, ra)
        xb, yb = _iso(ox, oy, cb, rb)
        tr += [(ta, f"{f1(xa)} {f1(ya)}"), (ta + (tb - ta) / 2, f"{f1((xa+xb)/2)} {f1((ya+yb)/2-12)}"), (tb, f"{f1(xb)} {f1(yb)}")]
    x0, y0 = _iso(ox, oy, 0, 0)
    tr = [(0, f"{f1(x0)} {f1(y0)}")] + tr
    rot = [(0, "0")]
    for ts, sd in turns:
        rot += [(ts, "0"), (ts + 0.2, f"{12*sd}"), (ts + 0.42, "0")]
    cel = [(0, "0"), (t_sw - 0.1, "0"), (t_sw + 0.1, "-12"), (t_sw + 0.3, "0"), (t_end + 0.6, "0"), (t_end + 0.8, "-16"), (t_end + 1.0, "0")]
    vis = C.ease("opacity", [(0, 0), (0.25, 1), (T - 0.45, 1), (T - 0.15, 0)])
    L.append(f'<g opacity="0">{vis}<g>{C.ease_t("translate", tr)}'
             f'<ellipse cx="0" cy="2" rx="22" ry="8" fill="#000" opacity="0.2"/>'
             f'<g>{C.ease_t("rotate", rot)}<g>{C.ease_t("translate", [(t, f"0 {v}") for t, v in cel])}'
             f'{chibi.standing(0, -foot, s, p + "m", smile="open")}</g></g></g></g>')
    # gem counter
    gcx, gcy = VX + VW - 112, VY + 20
    cnt = [f'<rect x="{gcx}" y="{gcy}" width="92" height="40" rx="20" fill="#000" opacity="0.28"/>' + _gem(gcx + 24, gcy + 20, 0.72)]
    marks = [0.0] + gems_t
    for k in range(4):
        a, b = marks[k], (marks[k + 1] if k < 3 else T - 0.3)
        op = ([(0, 1 if k == 0 else 0)] + ([(a, 0), (a + 0.05, 1)] if k else []) + [(b, 1), (b + 0.05, 0)]
              + ([(T - 0.3, 0), (T - 0.25, 1)] if k == 0 else []))
        cnt.append(f'<g opacity="{1 if k == 0 else 0}">{C.ease("opacity", sorted(op))}{text(gcx + 44, gcy + 26.5, f"{k}/3", 17, "#fff", "sans", 800)}</g>')
    L.append("".join(cnt))
    # success banner + confetti
    t_ok = t_end + 0.4
    ban = (f'<rect x="{VX+VW/2-170}" y="{VY+28}" width="340" height="74" rx="18" fill="#fff" opacity="0.96"/>'
           + text(VX + VW / 2, VY + 60, "You did it!", 20, "#1c1c1e", "sans", 800, "middle")
           + text(VX + VW / 2, VY + 84, "Every gem collected, switch on.", 14, "#55555c", "sans", 600, "middle"))
    L.append(_pop(VX + VW / 2, VY + 64, ban, C, t_ok, t_off=T - 0.75))
    conf = []
    cols = ["#ff375f", "#ffd60a", "#30d158", "#0a84ff", "#bf5af2", "#ff9f0a"]
    for k in range(26):
        cx_ = VX + 40 + rng.random() * (VW - 80)
        dy = rng.uniform(300, 480)
        t0 = t_ok + rng.uniform(0, 0.5)
        sp = rng.uniform(0.6, 1.1)
        conf.append(f'<g opacity="0">{C.ease("opacity", [(0, 0), (t0, 0), (t0 + 0.05, 1), (t0 + 2.2, 1), (t0 + 2.6, 0)])}'
                    f'<g>{C.ease_t("translate", [(0, f"{f1(cx_)} {VY-10}"), (t0, f"{f1(cx_)} {VY-10}"), (t0 + 2.6, f"{f1(cx_+rng.uniform(-40, 40))} {f1(VY-10+dy)}")])}'
                    f'<rect x="-4" y="-2.5" width="8" height="5" rx="1" fill="{cols[k % 6]}">'
                    f'<animateTransform attributeName="transform" type="rotate" values="0;360" dur="{sp:.2f}s" repeatCount="indefinite"/></rect></g></g>')
    L.append("".join(conf))
    # Run My Code button + pointer
    bw, bh = 150, 42
    bx, by = VX + VW - bw - 20, VY + VH - bh - 20
    lab = lambda s_, ic: ic + text(bx + 44, by + 27, s_, 15, "#fff", "sans", 700)
    play = f'<path d="M{bx+20} {by+13} l13 8 l-13 8z" fill="#fff"/>'
    stop = f'<rect x="{bx+20}" y="{by+14}" width="13" height="13" rx="2.5" fill="#fff"/>'
    run_on = [(0, 0), (0.78, 0), (0.83, 1), (t_end + 0.2, 1), (t_end + 0.25, 0)]
    L.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="{bh/2}" fill="#0a84ff"/>'
             f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="{bh/2}" fill="#ff453a" opacity="0">{C.ease("opacity", run_on)}</rect>'
             f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="{bh/2}" fill="#000" opacity="0">{C.ease("opacity", [(0, 0), (0.62, 0), (0.68, 0.25), (0.82, 0)])}</rect>'
             f'<g>{C.ease("opacity", [(0, 1), (0.78, 1), (0.83, 0), (t_end + 0.2, 0), (t_end + 0.25, 1)])}{lab("Run My Code", play)}</g>'
             f'<g opacity="0">{C.ease("opacity", run_on)}{lab("Stop", stop)}</g>')
    ptr = [(0, f"{bx+bw*0.62} {VY+VH+30}"), (0.2, f"{bx+bw*0.62} {VY+VH+30}"), (0.6, f"{bx+bw*0.62} {by+bh*0.6}"), (0.95, f"{bx+bw*0.62} {by+bh*0.6}"),
           (1.6, f"{bx+bw+40} {VY+VH+40}")]
    clk = [(0, "1"), (0.62, "1"), (0.68, "0.85"), (0.8, "1")]
    L.append(f'<g>{C.ease_t("translate", ptr)}<g>{C.ease_t("scale", clk)}'
             '<path d="M0 0 L0 17.5 L4.4 13.4 L7.4 20.2 L10.2 19 L7.3 12.4 L13 12.2Z" fill="#000" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/></g></g>')
    D.add(f'<g clip-path="url(#{p}-lv)">{"".join(L)}</g>'
          f'<rect x="{VX+0.5}" y="{VY+0.5}" width="{VW-1}" height="{VH-1}" rx="14" stroke="#fff" stroke-opacity="0.12"/>')
    return D.svg(title="Swift Playgrounds", desc="A Swift Playgrounds page called Ship It: a for loop moves Miko across an island, "
                                                 "collects three gems and toggles the switch.")
