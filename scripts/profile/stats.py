"""Activity: what the numbers add up to. Rolling counters, a year of contributions with the
longest streak and the best day marked on it, and the records that come out of it."""
from __future__ import annotations

import datetime as dt

import data as gh
from kit import EASE, FG, FG2, FG3, Clock, Doc, f1, f3, text, traffic, tw

GREEN = ["#202027", "#0e4429", "#006d32", "#26a641", "#39d353"]
OUTQ = "0.16 1 0.3 1"


def odometer(D, x, y, value, fs, delay, color=FG, anchor="start"):
    """Digits roll into place once, like a mechanical counter."""
    p = D.p
    adv, comma = fs * 0.6, fs * 0.28
    width = sum(comma if ch == "," else adv for ch in value)
    if anchor == "end":
        x -= width
    out, cx, k = [], x, 0
    for ch in value:
        if not ch.isdigit():
            out.append(text(cx + (comma if ch == "," else adv) / 2, y, ch, fs, color, "sans", 800, "middle"))
            cx += comma if ch == "," else adv
            continue
        dgt = int(ch)
        lh = fs * 1.1
        cid = f"{p}-od{len(D.defs)}"
        D.adddef(f'<clipPath id="{cid}"><rect x="{f1(cx-1)}" y="{f1(y-fs*0.86)}" width="{f1(adv+2)}" height="{f1(fs*1.08)}"/></clipPath>')
        col = "".join(text(cx + adv / 2, y + i * lh, str(i % 10), fs, color, "sans tnum", 800, "middle") for i in range(20))
        end = -(10 + dgt) * lh
        out.append(f'<g clip-path="url(#{cid})"><g transform="translate(0 {f1(end)})">'
                   f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {f1(end)}" dur="{1.5 + k*0.12:.2f}s" '
                   f'begin="{delay + k*0.06:.2f}s" fill="freeze" calcMode="spline" keySplines="{OUTQ}"/>{col}</g></g>')
        cx += adv
        k += 1
    return "".join(out)


def _streak_run(days):
    best, cur, start, best_span = 0, 0, None, (None, None)
    for d, n, _ in days:
        if n > 0:
            if cur == 0:
                start = d
            cur += 1
            if cur > best:
                best, best_span = cur, (start, d)
        else:
            cur = 0
    return best, best_span


def activity(d):
    W, H = 1200, 660
    D = Doc(W, H, "st", r=16, bg="#141418")
    p = D.p
    c = d["contrib"]
    D.add(f'<rect width="{W}" height="38" fill="#1e1e23"/><path d="M0 38H{W}" stroke="#000" stroke-opacity="0.5"/>' + traffic(22, 19)
          + text(W / 2, 24, "Activity — mikonyaa", 13, "#c7c7cc", "sans", 600, "middle"))
    years = d.get("years") or {}
    all_time = sum(years.values()) or c["total"]
    best_year = max(years.items(), key=lambda kv: kv[1]) if years else None
    cards = [
        (f"{all_time:,}", "contributions on GitHub", f"best year {best_year[0]} · {best_year[1]:,}" if best_year else "all time", "#39d353"),
        (f"{c['total']:,}", "in the last 12 months", f"{c['commits']:,} public commits · {c.get('private', 0):,} private", "#64d2ff"),
        (f"{d['merged_prs']}", "pull requests merged", f"{d.get('prs_total', 0)} opened in total", "#bf5af2"),
        (f"{d.get('contributed_to', 0)}", "other repositories", "contributed to, beyond my own", "#ff9f0a"),
    ]
    cw = (W - 48 - 36) / 4
    for i, (val, lab, sub, col) in enumerate(cards):
        x = 24 + i * (cw + 12)
        D.add(f'<rect x="{f1(x)}" y="58" width="{f1(cw)}" height="132" rx="16" fill="#1b1b21" stroke="#fff" stroke-opacity="0.07"/>'
              f'<rect x="{f1(x+20)}" y="76" width="22" height="4" rx="2" fill="{col}"/>')
        D.add(odometer(D, x + 20, 130, val, 44, 0.2 + i * 0.15))
        D.add(text(x + 20, 156, lab, 14.5, FG, "sans", 600) + text(x + 20, 176, sub, 12.5, FG3, "sans", 500))
    # the year, as a grid
    gx0, gy0 = 24, 206
    D.add(f'<rect x="{gx0}" y="{gy0}" width="{W-48}" height="262" rx="16" fill="#1b1b21" stroke="#fff" stroke-opacity="0.07"/>')
    D.add(text(gx0 + 20, gy0 + 30, "Last 12 months", 15, FG, "sans", 700) + text(gx0 + 140, gy0 + 30, "every square is a day", 12.5, FG3, "sans", 500))
    weeks = c["weeks"]
    counts = sorted(n for wk in weeks for _, n, _ in wk if n > 0) or [1]
    q = [counts[int(len(counts) * f)] for f in (0.25, 0.5, 0.75)]
    lv = lambda n: 0 if n == 0 else 1 + sum(n > t for t in q)
    cs, gp = 15, 4
    n_w = len(weeks)
    ox = gx0 + (W - 48 - n_w * (cs + gp)) / 2 + 14
    oy = gy0 + 58
    pos = {}
    for wi, wk in enumerate(weeks):
        for day, n, wd in wk:
            x, y = ox + wi * (cs + gp), oy + wd * (cs + gp)
            pos[day] = (x, y)
            D.add(f'<rect x="{f1(x)}" y="{f1(y)}" width="{cs}" height="{cs}" rx="3.5" fill="{GREEN[lv(n)]}"/>')
    for wd, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        D.add(text(ox - 10, oy + wd * (cs + gp) + 11, lab, 10.5, FG3, "sans", 500, "end"))
    seen = set()
    for wi, wk in enumerate(weeks):
        day = dt.date.fromisoformat(wk[0][0])
        if day.day <= 7 and (day.year, day.month) not in seen and wi < n_w - 1:
            seen.add((day.year, day.month))
            D.add(text(ox + wi * (cs + gp), oy - 10, day.strftime("%b"), 11, FG3, "sans", 600))
    # longest streak: a bracket under the grid
    longest, (s0, s1) = _streak_run(c["days"])
    if s0 and s0 in pos and s1 in pos:
        x0, x1 = pos[s0][0], pos[s1][0] + cs
        by = oy + 7 * (cs + gp) + 6
        D.add(f'<path d="M{f1(x0)} {by} v6 H{f1(x1)} v-6" stroke="#39d353" stroke-width="1.6" fill="none" opacity="0">'
              f'<animate attributeName="opacity" values="0;1" dur="0.5s" begin="1.6s" fill="freeze"/></path>'
              f'<g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" begin="1.8s" fill="freeze"/>'
              + text((x0 + x1) / 2, by + 24, f"{longest}-day streak", 12.5, "#39d353", "sans", 700, "middle") + '</g>')
    # best day: ring + label
    bd = max(c["days"], key=lambda t: t[1])
    if bd[0] in pos:
        bx, by_ = pos[bd[0]]
        lbl = f"{bd[1]} on {dt.date.fromisoformat(bd[0]).strftime('%b %-d')}"
        lw = tw(lbl, 12, weight=700) + 22
        lx = min(bx + cs / 2 - lw / 2, gx0 + W - 48 - lw - 12)
        ly = gy0 + 14
        D.add(f'<g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" begin="2.2s" fill="freeze"/>'
              f'<rect x="{f1(bx-3)}" y="{f1(by_-3)}" width="{cs+6}" height="{cs+6}" rx="5.5" stroke="#fff" stroke-width="2" fill="none">'
              f'<animate attributeName="opacity" values="1;0.35;1" dur="2s" begin="2.2s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="{EASE};{EASE}"/></rect>'
              f'<path d="M{f1(bx+cs/2)} {f1(by_-4)} V{ly+26}" stroke="#fff" stroke-opacity="0.5" stroke-dasharray="2 3"/>'
              f'<rect x="{f1(lx)}" y="{ly}" width="{f1(lw)}" height="24" rx="12" fill="#fff"/>'
              + text(lx + lw / 2, ly + 16.5, lbl, 12, "#111", "sans", 700, "middle") + '</g>')
    # a light sweep across the grid, once a loop
    D.adddef(f'<linearGradient id="{p}-sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
             f'<stop offset="0.5" stop-color="#fff" stop-opacity="0.09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>',
             f'<clipPath id="{p}-gc"><rect x="{f1(ox-2)}" y="{oy-2}" width="{f1(n_w*(cs+gp)+2)}" height="{7*(cs+gp)+2}"/></clipPath>')
    D.add(f'<g clip-path="url(#{p}-gc)"><rect x="{f1(ox-160)}" y="{oy}" width="140" height="{7*(cs+gp)}" fill="url(#{p}-sw)">'
          f'<animate attributeName="x" values="{f1(ox-160)};{f1(ox+n_w*(cs+gp))};{f1(ox+n_w*(cs+gp))}" keyTimes="0;0.3;1" dur="10s" repeatCount="indefinite" '
          f'calcMode="spline" keySplines="{EASE};0 0 1 1"/></rect></g>')
    # legend
    lx_ = ox + n_w * (cs + gp) - 5 * 19 - 74
    ly_ = oy + 7 * (cs + gp) + 22
    D.add(text(lx_, ly_ + 11, "Less", 11.5, FG3, "sans", 500) + "".join(
        f'<rect x="{f1(lx_+34+i*19)}" y="{ly_}" width="14" height="14" rx="3" fill="{g}"/>' for i, g in enumerate(GREEN))
          + text(lx_ + 34 + 5 * 19 + 4, ly_ + 11, "More", 11.5, FG3, "sans", 500))
    # records
    last = dt.date.fromisoformat(c["days"][-1][0])
    window = [n for day, n, _ in c["days"] if (last - dt.date.fromisoformat(day)).days < 365]
    active = sum(1 for n in window if n > 0)
    by_wd = [0] * 7
    for _, n, wd in c["days"]:
        by_wd[wd] += n
    wd_name = ["Sundays", "Mondays", "Tuesdays", "Wednesdays", "Thursdays", "Fridays", "Saturdays"][by_wd.index(max(by_wd))]
    months = {}
    for day, n, _ in c["days"]:
        months[day[:7]] = months.get(day[:7], 0) + n
    bm = max(months.items(), key=lambda kv: kv[1])
    bm_name = dt.date.fromisoformat(bm[0] + "-01").strftime("%B")
    recs = [(f"{longest} days", "longest streak"), (f"{bd[1]}", "contributions in one day"), (f"{active}", "active days of the last 365"),
            (f"{bm[1]:,}", f"in {bm_name}, the busiest month"), (wd_name, "busiest day of the week")]
    rw = (W - 48 - 4 * 12) / 5
    for i, (v, k) in enumerate(recs):
        x = 24 + i * (rw + 12)
        D.add(f'<rect x="{f1(x)}" y="484" width="{f1(rw)}" height="96" rx="16" fill="#1b1b21" stroke="#fff" stroke-opacity="0.07"/>'
              + text(x + 18, 528, v, 24, FG, "sans tnum", 800, extra=' letter-spacing="-0.4"') + text(x + 18, 556, k, 12.5, FG3, "sans", 600))
    D.add(text(24, H - 34, "From the GitHub API, redrawn twice a day. Private work is counted, never named.", 12, FG3, "sans", 500)
          + text(W - 24, H - 34, f"updated {d['generated']}", 12, FG3, "sans tnum", 500, "end"))
    return D.svg(title="Activity", desc=f"{all_time} contributions on GitHub; {c['total']} in the last 12 months; {d['merged_prs']} pull requests merged; "
                                          f"contributed to {d.get('contributed_to', 0)} other repositories; longest streak {longest} days; best day {bd[1]}.")
