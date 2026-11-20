"""Astana at dusk, drawn as a macOS wallpaper: layered skyline with Bayterek, Khan Shatyr,
Abu Dhabi Plaza, Ak Orda, the Emerald towers and the Pyramid, the Ishim in front.
Static except for a few cheap opacity/translate animations (no filters)."""
from __future__ import annotations

import random

from kit import f1, f3

PALETTES = {
    "dusk": dict(sky=[(0, "#0a0f27"), (0.2, "#18204a"), (0.4, "#33397a"), (0.56, "#6d5596"), (0.68, "#c07299"),
                      (0.75, "#f0977f"), (0.79, "#ffc896")],
                 sun="#ffd6a0", haze="#9c86b6", far="#6b5f9a", mid_top="#4a4682", mid_bot="#2a2852", near="#1b1a36",
                 water_top="#3a2f62", water_bot="#100d24", glow="#ffb37a", stars=0.6),
    "night": dict(sky=[(0, "#060a1c"), (0.3, "#0d1433"), (0.6, "#1c2350"), (0.74, "#3a3470"), (0.79, "#5a467e")],
                  sun="#9a8cff", haze="#4a4680", far="#2f2d62", mid_top="#2a2a5c", mid_bot="#18183a", near="#0f0f26",
                  water_top="#1b1a40", water_bot="#07071a", glow="#8b7bff", stars=1.0),
}


def wallpaper(doc, W, H, hz, mode="dusk", seed=7, sun_x=0.6):
    P = PALETTES[mode]
    p = doc.p
    rng = random.Random(seed)
    stops = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in P["sky"])
    doc.adddef(
        f'<linearGradient id="{p}-sky" x1="0" y1="0" x2="0" y2="{f3(hz/H)}" gradientUnits="objectBoundingBox">{stops}</linearGradient>',
        f'<radialGradient id="{p}-sun"><stop offset="0" stop-color="{P["sun"]}" stop-opacity="0.95"/><stop offset="0.3" stop-color="{P["glow"]}" stop-opacity="0.45"/>'
        f'<stop offset="1" stop-color="{P["glow"]}" stop-opacity="0"/></radialGradient>',
        f'<linearGradient id="{p}-water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["water_top"]}"/><stop offset="1" stop-color="{P["water_bot"]}"/></linearGradient>',
        f'<linearGradient id="{p}-mid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["mid_top"]}"/><stop offset="1" stop-color="{P["mid_bot"]}"/></linearGradient>',
        f'<linearGradient id="{p}-glass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f3a0a8" stop-opacity="0.85"/>'
        f'<stop offset="0.35" stop-color="#7c6fb8"/><stop offset="1" stop-color="#2b2a5a"/></linearGradient>',
        f'<linearGradient id="{p}-trunk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#cfc8e6"/><stop offset="0.55" stop-color="#fbf4ff"/>'
        f'<stop offset="1" stop-color="#f7b8a8"/></linearGradient>',
        f'<radialGradient id="{p}-gold" cx="0.38" cy="0.32" r="0.75"><stop offset="0" stop-color="#fff8d8"/><stop offset="0.35" stop-color="#ffd166"/>'
        f'<stop offset="0.8" stop-color="#d98a1e"/><stop offset="1" stop-color="#9c5a10"/></radialGradient>',
        f'<radialGradient id="{p}-aura"><stop offset="0" stop-color="#ffd27a" stop-opacity="0.55"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>',
        f'<linearGradient id="{p}-tent" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9f3ff" stop-opacity="0.95"/>'
        f'<stop offset="0.55" stop-color="#a9b4e6" stop-opacity="0.9"/><stop offset="1" stop-color="#5d5a9c"/></linearGradient>',
        f'<linearGradient id="{p}-tentglow" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffcf8a" stop-opacity="0.85"/>'
        f'<stop offset="0.6" stop-color="#ffcf8a" stop-opacity="0"/></linearGradient>',
        f'<linearGradient id="{p}-dome" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7fb6ff"/><stop offset="1" stop-color="#1f4c9e"/></linearGradient>',
        f'<linearGradient id="{p}-emerald" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e6a4a0" stop-opacity="0.7"/>'
        f'<stop offset="0.3" stop-color="#3d8a8e"/><stop offset="1" stop-color="#173d4c"/></linearGradient>',
        f'<linearGradient id="{p}-pyr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f2c2a6"/><stop offset="1" stop-color="#5b507e"/></linearGradient>',
        f'<radialGradient id="{p}-lamp"><stop offset="0" stop-color="#ffe2a8" stop-opacity="0.9"/><stop offset="1" stop-color="#ffb35a" stop-opacity="0"/></radialGradient>',
        f'<linearGradient id="{p}-cloud" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a7ab8" stop-opacity="0.0"/>'
        f'<stop offset="0.5" stop-color="#b98bb4" stop-opacity="0.55"/><stop offset="1" stop-color="#ffb59a" stop-opacity="0.8"/></linearGradient>',
    )
    o = [f'<rect width="{W}" height="{hz}" fill="url(#{p}-sky)"/>']
    sx = W * sun_x
    o.append(f'<ellipse cx="{f1(sx)}" cy="{hz}" rx="{f1(W*0.5)}" ry="{f1(hz*0.55)}" fill="url(#{p}-sun)"/>')
    # stars
    for i in range(70):
        x, y = rng.uniform(0, W), rng.uniform(0, hz * 0.42) ** 1.0
        r = rng.choice((0.6, 0.7, 0.9, 1.1))
        op = rng.uniform(0.25, 0.85) * P["stars"] * (1 - y / (hz * 0.5))
        tw = ""
        if i % 9 == 0:
            d = rng.uniform(2.6, 5.2)
            tw = f'<animate attributeName="opacity" values="{f3(op)};{f3(op*0.2)};{f3(op)}" dur="{d:.1f}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>'
        o.append(f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{r}" fill="#fff" opacity="{f3(op)}">{tw}</circle>')
    # clouds: long lit stratus, drifting very slowly
    for i, (cx, cy, w, h) in enumerate(((W*0.18, hz*0.62, 340, 16), (W*0.55, hz*0.52, 420, 14), (W*0.86, hz*0.66, 300, 12),
                                        (W*0.36, hz*0.74, 260, 10), (W*0.74, hz*0.78, 220, 8))):
        shape = (f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="{f1(w/2)}" ry="{f1(h)}" fill="url(#{p}-cloud)"/>'
                 f'<ellipse cx="{f1(cx-w*0.18)}" cy="{f1(cy-h*0.6)}" rx="{f1(w*0.22)}" ry="{f1(h*0.8)}" fill="url(#{p}-cloud)"/>'
                 f'<ellipse cx="{f1(cx+w*0.2)}" cy="{f1(cy+h*0.2)}" rx="{f1(w*0.28)}" ry="{f1(h*0.7)}" fill="url(#{p}-cloud)"/>')
        o.append(f'<g opacity="{0.9 if mode == "dusk" else 0.35}">{shape}</g>')
    city = []
    # far haze
    pts, x = [f"M0 {hz}"], 0
    while x < W:
        w = rng.randint(14, 46)
        h = rng.randint(14, 54)
        pts.append(f"V{hz-h}H{min(W, x+w)}")
        x += w
    city.append(f'<path d="{"".join(pts)}V{hz}Z" fill="{P["haze"]}" opacity="0.5"/>')
    # far blocks with sparse lights
    x = 0
    while x < W:
        w = rng.randint(16, 44)
        h = rng.randint(30, 110)
        city.append(f'<rect x="{x}" y="{hz-h}" width="{w}" height="{h}" fill="{P["far"]}" opacity="0.92"/>')
        if rng.random() < 0.25:
            city.append(f'<path d="M{x+w/2:.0f} {hz-h} v-{rng.randint(8,18)}" stroke="{P["far"]}" stroke-width="1.5"/>')
        for _ in range(int(w * h / 420)):
            wx, wy = x + rng.randint(3, max(3, w - 5)), hz - h + rng.randint(5, max(5, h - 6))
            city.append(f'<rect x="{wx}" y="{wy}" width="2" height="2.5" fill="#ffd9a0" opacity="{rng.uniform(0.25, 0.6):.2f}"/>')
        x += w + rng.randint(0, 6)
    # landmarks (mid layer)
    city.append(_ak_orda(W * 0.21, hz, p))
    city.append(_plaza(W * 0.385, hz, p))
    city.append(_emerald(W * 0.75, hz, p))
    city.append(_pyramid(W * 0.905, hz, p))
    city.append(_khan_shatyr(W * 0.545, hz, p))
    # mid blocks
    x = 0
    keep_out = [(W*0.45, W*0.49)]
    while x < W:
        w = rng.randint(20, 52)
        h = rng.randint(24, 78)
        if not any(a < x + w / 2 < b for a, b in keep_out):
            city.append(f'<rect x="{x}" y="{hz-h}" width="{w}" height="{h}" fill="url(#{p}-mid)"/>'
                        f'<rect x="{x}" y="{hz-h}" width="{w}" height="1.5" fill="#f6a6a0" opacity="0.35"/>')
            for row in range(int(h / 9)):
                for col in range(int(w / 7)):
                    if rng.random() < 0.16:
                        warm = rng.random() < 0.8
                        city.append(f'<rect x="{x+3+col*7}" y="{hz-h+5+row*9}" width="3" height="4" fill="{"#ffd28f" if warm else "#bfe3ff"}" '
                                    f'opacity="{rng.uniform(0.45, 0.95):.2f}"/>')
        x += w + rng.randint(2, 10)
    city.append(_bayterek(W * 0.47, hz, p))
    o.append(f'<g id="{p}-city">{"".join(city)}</g>')
    # embankment, lamps
    o.append(f'<rect y="{hz}" width="{W}" height="{H-hz}" fill="url(#{p}-water)"/>')
    o.append(f'<g opacity="0.22"><use href="#{p}-city" transform="translate(0 {2*hz+6}) scale(1 -1)"/></g>'
             f'<rect y="{hz}" width="{W}" height="{H-hz}" fill="url(#{p}-water)" opacity="0.55"/>')
    o.append(f'<rect y="{hz-3}" width="{W}" height="9" fill="{P["near"]}"/><rect y="{hz-3}" width="{W}" height="1" fill="#ffb98f" opacity="0.35"/>')
    for i in range(int(W / 120) + 1):
        lx = 40 + i * 120
        o.append(f'<path d="M{lx} {hz-3} v-26 q0 -4 6 -4" stroke="{P["near"]}" stroke-width="2.4" fill="none"/>'
                 f'<circle cx="{lx+7}" cy="{hz-32}" r="16" fill="url(#{p}-lamp)" opacity="0.8"/><circle cx="{lx+7}" cy="{hz-31}" r="2.2" fill="#fff1c9"/>'
                 f'<ellipse cx="{lx+7}" cy="{hz+14}" rx="4" ry="10" fill="#ffd28f" opacity="0.18"/>')
    # sun path on the water: shimmering streaks
    for k in range(14):
        y = hz + 10 + k * 9
        w = max(24, 260 - k * 17) * rng.uniform(0.7, 1.1)
        x = sx - w / 2 + rng.uniform(-18, 18)
        op = max(0.08, 0.6 - k * 0.04)
        d = rng.uniform(2.2, 4.4)
        o.append(f'<rect x="{f1(x)}" y="{y}" width="{f1(w)}" height="2" rx="1" fill="{P["sun"]}" opacity="{f3(op)}">'
                 f'<animate attributeName="opacity" values="{f3(op)};{f3(op*0.35)};{f3(op)}" dur="{d:.1f}s" repeatCount="indefinite" '
                 f'calcMode="spline" keyTimes="0;0.5;1" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/></rect>')
    return "".join(o)


def _bayterek(bx, hz, p):
    top = hz - 250          # where the crown starts
    cy = hz - 286           # sphere centre
    trunk = (f"M{bx-15} {hz-8} C{bx-9} {hz-90} {bx-6} {hz-170} {bx-9} {top} L{bx+9} {top} "
             f"C{bx+6} {hz-170} {bx+9} {hz-90} {bx+15} {hz-8}Z")
    lattice = "".join(f'<path d="M{bx-16} {hz-12-i*16} L{bx+16} {hz-28-i*16} M{bx+16} {hz-12-i*16} L{bx-16} {hz-28-i*16}" '
                      f'stroke="#8f88b8" stroke-width="0.8" opacity="0.55"/>' for i in range(15))
    branches = []
    for side in (-1, 1):
        for j, (ox, oy, w) in enumerate(((10, 22, 4.2), (20, 30, 3.4), (28, 40, 2.8))):
            branches.append(f'<path d="M{bx+side*3} {top+2} C{bx+side*(ox*0.5)} {top-6} {bx+side*ox} {top-oy*0.45} {bx+side*(ox+2)} {top-oy}" '
                            f'stroke="url(#{p}-trunk)" stroke-width="{w}" fill="none" stroke-linecap="round"/>')
    aura = (f'<circle cx="{bx}" cy="{cy}" r="74" fill="url(#{p}-aura)"><animate attributeName="opacity" values="0.75;1;0.75" dur="5s" '
            f'repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/></circle>')
    return (f'<g><defs><clipPath id="{p}-tr"><path d="{trunk}"/></clipPath></defs>'
            f'<path d="M{bx-34} {hz} L{bx-26} {hz-10} H{bx+26} L{bx+34} {hz}Z" fill="#3a3666"/>'
            f'<path d="{trunk}" fill="url(#{p}-trunk)"/><g clip-path="url(#{p}-tr)">{lattice}</g>'
            + aura + "".join(branches) +
            f'<circle cx="{bx}" cy="{cy}" r="23" fill="url(#{p}-gold)"/>'
            f'<path d="M{bx-21} {cy+4} Q{bx} {cy+12} {bx+21} {cy+4}" stroke="#a8641a" stroke-width="1" opacity="0.6" fill="none"/>'
            f'<ellipse cx="{bx-8}" cy="{cy-9}" rx="6" ry="4" fill="#fff" opacity="0.65"/>'
            f'<circle cx="{bx}" cy="{cy-24}" r="1.6" fill="#ff5a5a"><animate attributeName="opacity" values="1;0.15;1" dur="2.4s" repeatCount="indefinite"/></circle></g>')


def _khan_shatyr(kx, hz, p):
    ax, ay = kx + 14, hz - 150
    l, r = kx - 82, kx + 78
    shape = f"M{l} {hz} C{l+40} {hz-40} {ax-30} {ay+40} {ax} {ay} C{ax+24} {ay+50} {r-30} {hz-40} {r} {hz}Z"
    mesh = "".join(f'<path d="M{ax} {ay} L{l + (r-l)*i/12:.0f} {hz}" stroke="#ffffff" stroke-width="0.6" opacity="0.35"/>' for i in range(13))
    rings = "".join(f'<path d="M{l} {hz-k*22} Q{(l+r)/2:.0f} {hz-k*22-12} {r} {hz-k*22}" stroke="#ffffff" stroke-width="0.6" opacity="0.3" fill="none"/>' for k in range(1, 7))
    return (f'<g><defs><clipPath id="{p}-ks"><path d="{shape}"/></clipPath></defs>'
            f'<path d="{shape}" fill="url(#{p}-tent)"/><g clip-path="url(#{p}-ks)">{mesh}{rings}'
            f'<rect x="{l}" y="{hz-70}" width="{r-l}" height="70" fill="url(#{p}-tentglow)"/></g>'
            f'<path d="M{ax} {ay} l-3 -26 l4 0z" fill="#e8ecff"/><circle cx="{ax-1}" cy="{ay-27}" r="1.6" fill="#ff5a5a"/></g>')


def _plaza(x, hz, p):
    w, h = 40, 300
    top = hz - h
    shape = f"M{x-w/2} {hz} V{top+30} C{x-w/2} {top+8} {x-6} {top} {x+4} {top-6} C{x+14} {top+6} {x+w/2} {top+20} {x+w/2} {top+40} V{hz}Z"
    lines = "".join(f'<path d="M{x-w/2+k*5} {top+12} V{hz}" stroke="#ffffff" stroke-width="0.5" opacity="0.18"/>' for k in range(1, 8))
    lights = "".join(f'<rect x="{x-w/2+3+(k%6)*6}" y="{top+44+(k*37)%(h-60)}" width="3" height="2" fill="#ffd28f" opacity="0.8"/>' for k in range(22))
    return (f'<g><defs><clipPath id="{p}-pl"><path d="{shape}"/></clipPath></defs><path d="{shape}" fill="url(#{p}-glass)"/>'
            f'<g clip-path="url(#{p}-pl)">{lines}{lights}</g>'
            f'<path d="M{x+4} {top-6} v-22" stroke="#cfc8e6" stroke-width="1.6"/>'
            f'<circle cx="{x+4}" cy="{top-29}" r="1.8" fill="#ff5a5a"><animate attributeName="opacity" values="1;0.15;1" dur="1.8s" repeatCount="indefinite"/></circle>'
            # a second, lower tower of the complex
            f'<path d="M{x+24} {hz} V{top+120} Q{x+36} {top+104} {x+48} {top+120} V{hz}Z" fill="url(#{p}-glass)" opacity="0.9"/></g>')


def _ak_orda(x, hz, p):
    return (f'<g><rect x="{x-62}" y="{hz-54}" width="124" height="54" fill="url(#{p}-mid)"/>'
            + "".join(f'<rect x="{x-56+k*10}" y="{hz-46}" width="4" height="40" fill="#ffd9a6" opacity="0.35"/>' for k in range(12)) +
            f'<rect x="{x-62}" y="{hz-56}" width="124" height="3" fill="#cfc6e8" opacity="0.6"/>'
            f'<rect x="{x-24}" y="{hz-78}" width="48" height="24" fill="#3e3a72"/>'
            f'<path d="M{x-24} {hz-78} C{x-24} {hz-112} {x+24} {hz-112} {x+24} {hz-78}Z" fill="url(#{p}-dome)"/>'
            f'<path d="M{x-12} {hz-100} C{x-6} {hz-108} {x+4} {hz-108} {x+8} {hz-104}" stroke="#fff" stroke-width="1.4" opacity="0.5" fill="none"/>'
            f'<path d="M{x} {hz-104} V{hz-138}" stroke="#ffd166" stroke-width="2"/><circle cx="{x}" cy="{hz-140}" r="3" fill="#ffd166"/></g>')


def _emerald(x, hz, p):
    out = []
    for dx, h, w in ((-34, 150, 30), (0, 196, 34), (38, 126, 28)):
        tx = x + dx
        out.append(f'<path d="M{tx-w/2} {hz} V{hz-h+18} L{tx+w/2} {hz-h} V{hz}Z" fill="url(#{p}-emerald)"/>'
                   + "".join(f'<path d="M{tx-w/2} {hz-h+30+k*14} H{tx+w/2}" stroke="#bff" stroke-width="0.5" opacity="0.18"/>' for k in range(int((h-30)/14))))
    return "<g>" + "".join(out) + "</g>"


def _pyramid(x, hz, p):
    return (f'<g><path d="M{x-74} {hz} L{x} {hz-112} L{x+74} {hz}Z" fill="url(#{p}-pyr)"/>'
            f'<path d="M{x-22} {hz-79} L{x} {hz-112} L{x+22} {hz-79}Z" fill="#ffe2b8" opacity="0.85"/>'
            f'<path d="M{x} {hz-112} L{x} {hz}" stroke="#ffffff" stroke-opacity="0.15"/></g>')
