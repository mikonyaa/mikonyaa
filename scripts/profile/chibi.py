"""Miko as a vector chibi: fluffy, wavy brown hair, blue hoodie, shorts, sneakers.

All parts are drawn in head-local coordinates (head centre at 0,0; face ~100 wide),
then placed with translate/scale. Poses:
  sitting(x, y, s, pid)   on a ledge with a laptop on the lap; legs swing. Seat line is y + 130*s.
  bust(x, y, s, pid, wave) head and shoulders, optional waving hand.
  desk(x, y, s, pid)      behind a desk, typing on a laptop. Desk top is y + 96*s.
"""
from __future__ import annotations

OL = "#2a1a17"          # outline
SKIN, SKIN2, BLUSH = "#ffdcc4", "#f4b99a", "#ff8f80"
HAIR, HAIR2, HAIR3, HAIR_HI = "#7b4a2d", "#5c3420", "#43241a", "#a8714a"
EYE, IRIS = "#2b1b17", "#6b3f2c"
HOOD, HOOD2, HOOD3, HOOD_HI = "#4167c8", "#2f50a6", "#243f86", "#6c8fe6"
SHORTS, SHORTS2 = "#262d44", "#1b2033"
WHITE, SOLE, LAPTOP, LAPTOP2 = "#f6f7fb", "#c9d0de", "#dfe3ec", "#b9c1d0"
SW = 3.0  # outline width (head-local units)

FACE = "M-50,-4 C-50,-38 -28,-54 0,-54 C28,-54 50,-38 50,-4 C50,24 27,47 0,47 C-27,47 -50,24 -50,-4Z"
BACK_HAIR = ("M-46,6 C-52,14 -60,18 -66,12 C-72,8 -74,-2 -70,-10 C-78,-24 -74,-42 -62,-52 "
             "C-62,-66 -48,-78 -32,-78 C-22,-90 22,-90 32,-78 C48,-78 62,-66 62,-52 "
             "C74,-42 78,-24 70,-10 C74,-2 72,8 66,12 C60,18 52,14 46,6 L28,-4 L-28,-4Z")
FRONT_HAIR = ("M-62,10 C-70,4 -72,-8 -66,-16 C-74,-28 -70,-44 -58,-50 "
              "C-60,-64 -46,-76 -30,-74 C-24,-88 -4,-92 6,-82 C16,-92 38,-88 42,-74 "
              "C58,-76 70,-62 64,-48 C76,-40 76,-22 68,-14 C74,-6 70,6 62,10 "
              "C60,4 56,0 52,-4 C50,-12 46,-17 40,-19 "
              "C43,-11 40,-3 31,-1 C33,-8 29,-14 23,-17 "
              "C24,-8 18,-1 9,0 C11,-8 7,-15 1,-19 "
              "C0,-9 -6,-2 -15,-1 C-13,-9 -17,-15 -23,-18 "
              "C-24,-9 -30,-2 -39,-1 C-38,-8 -42,-13 -47,-15 "
              "C-50,-8 -52,-2 -53,3 C-55,8 -58,10 -62,10Z")
# lighter top sheen and darker inner strands
HAIR_SHEEN = ("M-44,-56 C-34,-68 -16,-74 0,-72 C18,-74 36,-68 46,-56 C34,-60 20,-62 8,-60 "
              "C-8,-63 -28,-61 -44,-56Z")
CURLS = ["M-62,10 C-64,6 -62,2 -58,2", "M62,10 C64,6 62,2 58,2", "M-30,-74 C-26,-70 -20,-70 -16,-74",
         "M6,-82 C10,-78 16,-78 20,-82"]
STRANDS = ["M23,-17 C27,-26 28,-34 25,-42", "M1,-19 C3,-29 2,-38 -2,-46", "M-23,-18 C-24,-28 -28,-36 -34,-42",
           "M40,-19 C46,-28 50,-36 50,-44", "M-47,-15 C-54,-24 -57,-32 -56,-40"]
AHOGE = "M2,-86 C0,-96 8,-102 14,-97"


def _eye(cx, cy, pid, k, blink_dur=5.2, begin=0.0):
    body = (f'<ellipse cx="{cx}" cy="{cy}" rx="7.6" ry="10" fill="{EYE}"/>'
            f'<ellipse cx="{cx}" cy="{cy+2.6}" rx="5.6" ry="6.6" fill="{IRIS}"/>'
            f'<circle cx="{cx+2.6}" cy="{cy-3.6}" r="2.9" fill="#fff"/>'
            f'<circle cx="{cx-2.4}" cy="{cy+4.2}" r="1.3" fill="#fff" opacity="0.85"/>'
            f'<path d="M{cx-9},{cy-1} C{cx-8.4},{cy-13.6} {cx+8.4},{cy-13.6} {cx+9},{cy-1}" stroke="{EYE}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    a = (f'<animateTransform attributeName="transform" type="scale" values="1 1;1 1;1 0.08;1 1;1 1" '
         f'keyTimes="0;0.9;0.93;0.96;1" dur="{blink_dur}s" begin="{begin}s" repeatCount="indefinite"/>')
    return f'<g transform="translate({cx} {cy})"><g>{a}<g transform="translate({-cx} {-cy})">{body}</g></g></g>'


def head(pid, smile="soft", eyes="open"):
    """The head in local coordinates. smile: soft | open | o | flat; eyes: open | closed | happy."""
    mouth = {"soft": '<path d="M-5.5,28 Q0,33 5.5,28" stroke="#7a3b2e" stroke-width="2.4" fill="none" stroke-linecap="round"/>',
             "open": '<path d="M-7,26 Q0,36 7,26 Z" fill="#7a3b2e" stroke="#7a3b2e" stroke-width="1.5" stroke-linejoin="round"/>'
                     '<path d="M-4,30.5 Q0,33.5 4,30.5" fill="#ff8f80"/>',
             "o": '<ellipse cx="0" cy="30" rx="4.6" ry="5.6" fill="#7a3b2e"/><ellipse cx="0" cy="32" rx="2.6" ry="2.2" fill="#ff8f80"/>',
             "flat": '<path d="M-6,29 H6" stroke="#7a3b2e" stroke-width="2.4" stroke-linecap="round"/>'}[smile]
    if eyes == "open":
        eye_svg = _eye(-19, 10, pid, "l") + _eye(19, 10, pid, "r")
    elif eyes == "closed":
        eye_svg = "".join(f'<path d="M{x-8},{10} Q{x},{17} {x+8},{10}" stroke="#2b1b17" stroke-width="2.8" fill="none" stroke-linecap="round"/>' for x in (-19, 19))
    else:  # happy: upside-down arcs
        eye_svg = "".join(f'<path d="M{x-8},{13} Q{x},{3} {x+8},{13}" stroke="#2b1b17" stroke-width="3" fill="none" stroke-linecap="round"/>' for x in (-19, 19))
    return (f'<defs><clipPath id="{pid}-face"><path d="{FACE}"/></clipPath></defs>'
            f'<path d="{BACK_HAIR}" fill="{HAIR2}" stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<path d="M-9,40 h18 v16 h-18z" fill="{SKIN2}"/>'
            f'<path d="{FACE}" fill="{SKIN}" stroke="{OL}" stroke-width="{SW}"/>'
            f'<g clip-path="url(#{pid}-face)"><path d="{FRONT_HAIR}" transform="translate(0 6)" fill="{SKIN2}" opacity="0.75"/></g>'
            f'<ellipse cx="-31" cy="22" rx="8.5" ry="4.6" fill="{BLUSH}" opacity="0.45"/>'
            f'<ellipse cx="31" cy="22" rx="8.5" ry="4.6" fill="{BLUSH}" opacity="0.45"/>'
            + eye_svg +
            f'<path d="M0,17 l-1.2,3.2" stroke="{SKIN2}" stroke-width="2" stroke-linecap="round"/>' + mouth +
            f'<path d="{FRONT_HAIR}" fill="{HAIR}" stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<path d="{HAIR_SHEEN}" fill="{HAIR_HI}" opacity="0.75"/>'
            + "".join(f'<path d="{d}" stroke="{HAIR3}" stroke-width="2.2" fill="none" stroke-linecap="round" opacity="0.6"/>' for d in STRANDS)
            + "".join(f'<path d="{d}" stroke="{HAIR3}" stroke-width="2.4" fill="none" stroke-linecap="round" opacity="0.75"/>' for d in CURLS) +
            f'<path d="{AHOGE}" stroke="{OL}" stroke-width="{SW+3.2}" fill="none" stroke-linecap="round"/>'
            f'<path d="{AHOGE}" stroke="{HAIR}" stroke-width="{SW}" fill="none" stroke-linecap="round"/>')


def _bob(inner, amp=1.6, dur=3.2, begin=0.0):
    return (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 {amp};0 0" dur="{dur}s" '
            f'begin="{begin}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" '
            f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>{inner}</g>')


def _torso():
    return (  # hood behind the neck, torso, collar, strings
        f'<path d="M-30,50 C-34,38 34,38 30,50 L26,60 L-26,60Z" fill="{HOOD3}" stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round"/>'
        f'<path d="M-36,64 C-36,55 -24,50 0,50 C24,50 36,55 36,64 L40,104 C40,112 34,117 26,117 L-26,117 '
        f'C-34,117 -40,112 -40,104Z" fill="{HOOD}" stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round"/>'
        f'<path d="M-22,52 C-14,64 14,64 22,52" fill="none" stroke="{HOOD3}" stroke-width="3" stroke-linecap="round"/>'
        f'<path d="M-36,70 C-30,86 -30,100 -36,112" stroke="{HOOD2}" stroke-width="5" fill="none" opacity="0.7"/>'
        f'<path d="M-7,59 L-8,78 M7,59 L8,78" stroke="{WHITE}" stroke-width="2.6" stroke-linecap="round"/>'
        f'<circle cx="-8" cy="80" r="2.4" fill="{WHITE}"/><circle cx="8" cy="80" r="2.4" fill="{WHITE}"/>')


def _laptop_lap(pid, logo_pulse=True):
    glow = ('<animate attributeName="opacity" values="0.55;1;0.55" dur="3.6s" repeatCount="indefinite"/>' if logo_pulse else "")
    return (f'<path d="M-34,74 h68 a5,5 0 0 1 5,5 v33 h-78 v-33 a5,5 0 0 1 5,-5z" fill="{LAPTOP}" stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<path d="M-29,79 h30 l-12,33 h-18z" fill="#ffffff" opacity="0.35"/>'
            f'<circle cx="0" cy="93" r="5.5" fill="#ffffff" stroke="{LAPTOP2}" stroke-width="1.5">{glow}</circle>'
            f'<path d="M-44,112 h88 a3,3 0 0 1 3,3 v1 a4,4 0 0 1 -4,4 h-86 a4,4 0 0 1 -4,-4 v-1 a3,3 0 0 1 3,-3z" fill="{LAPTOP2}" stroke="{OL}" stroke-width="{SW}"/>')


def _arms_to_laptop():
    sleeve = (lambda sx: f'<path d="M{36*sx},62 C{52*sx},70 {54*sx},92 {46*sx},106 C{42*sx},113 {32*sx},112 {32*sx},104 L{30*sx},76Z" '
                         f'fill="{HOOD}" stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round"/>')
    hand = (lambda sx: f'<ellipse cx="{38*sx}" cy="111" rx="7.5" ry="6" fill="{SKIN}" stroke="{OL}" stroke-width="{SW-0.6}"/>')
    return sleeve(-1) + sleeve(1), hand(-1) + hand(1)


def _leg(sx, swing_begin):
    x0 = 21 * sx
    shoe = (f'<path d="M{x0-11},162 L{x0+9},162 C{x0+15},162 {x0+19},168 {x0+19},173 L{x0+19},176 L{x0-14},176 '
            f'C{x0-16},176 {x0-16},166 {x0-11},162Z" fill="{WHITE}" stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<path d="M{x0-14},172 h33" stroke="{SOLE}" stroke-width="3"/>'
            f'<path d="M{x0-4},166 l8,0" stroke="{HOOD}" stroke-width="3" stroke-linecap="round"/>')
    if sx < 0:
        shoe = f'<g transform="translate({2*x0} 0) scale(-1 1)">{shoe}</g>'
    leg = (f'<path d="M{x0-8},128 L{x0+8},128 L{x0+7},158 L{x0-7},158Z" fill="{SKIN}" stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round"/>'
           f'<path d="M{x0-8},152 h16 v10 h-16z" fill="{WHITE}" stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round"/>' + shoe)
    a = (f'<animateTransform attributeName="transform" type="rotate" values="-7 {x0} 128;9 {x0} 128;-7 {x0} 128" dur="2.4s" '
         f'begin="{swing_begin}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>')
    return f'<g>{a}{leg}</g>'


def _shorts():
    return (f'<path d="M-40,110 L40,110 L42,128 C42,133 38,136 33,136 L5,136 L0,130 L-5,136 L-33,136 C-38,136 -42,133 -42,128Z" '
            f'fill="{SHORTS}" stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<path d="M0,116 L0,130" stroke="{SHORTS2}" stroke-width="2.5"/>')


def sitting(x, y, s, pid):
    """Sits on a ledge (seat at local y=130) with a laptop on the lap."""
    sleeves, hands = _arms_to_laptop()
    body = _leg(-1, 0.0) + _leg(1, 1.2) + _shorts() + _torso() + sleeves + _laptop_lap(pid) + hands
    return (f'<g transform="translate({x:g} {y:g}) scale({s:g})">{body}'
            + _bob(head(pid), amp=1.4, dur=3.4) + '</g>')


def bust(x, y, s, pid, wave=False, smile="open", eyes="open"):
    torso = _torso()
    arm = ""
    if wave:
        palm = (f'<rect x="50" y="14" width="22" height="24" rx="10" fill="{SKIN}" stroke="{OL}" stroke-width="{SW}"/>'
                + "".join(f'<rect x="{fx}" y="{fy}" width="6.4" height="{fh}" rx="3.2" fill="{SKIN}" stroke="{OL}" stroke-width="{SW-0.6}"/>'
                          for fx, fy, fh in ((50.5, 2, 18), (57.2, -1, 20), (63.9, 1, 18), (70.2, 6, 14)))
                + f'<rect x="51" y="12" width="20" height="14" rx="5" fill="{SKIN}"/>'
                + f'<rect x="41" y="20" width="14" height="7" rx="3.5" transform="rotate(-30 48 24)" fill="{SKIN}" stroke="{OL}" stroke-width="{SW-0.6}"/>')
        hand = (f'<g><animateTransform attributeName="transform" type="rotate" values="-10 60 40;16 60 40;-10 60 40" dur="1.2s" '
                f'repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>{palm}</g>')
        arm = (f'<path d="M30,62 C46,64 62,60 70,46 L84,52 C78,72 58,86 34,86Z" fill="{HOOD}" stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round"/>'
               + f'<g transform="translate(14 6)">{hand}</g>')
    left = f'<path d="M-34,62 C-46,70 -48,96 -44,114 L-30,114 L-30,74Z" fill="{HOOD}" stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round"/>'
    return (f'<g transform="translate({x:g} {y:g}) scale({s:g})">{left}{torso}'
            + _bob(head(pid, smile, eyes), amp=1.4, dur=3.0) + f'{arm}</g>')


def desk(x, y, s, pid):
    """Behind a desk (desk top at local y=96), typing on a laptop facing him."""
    sleeves = "".join(
        f'<path d="M{36*sx},62 C{50*sx},68 {54*sx},84 {44*sx},96 L{30*sx},96 L{28*sx},74Z" fill="{HOOD}" stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round"/>'
        for sx in (-1, 1))
    typing = "".join(
        f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -2.4;0 0;0 -1.2;0 0" dur="{0.5+0.13*i}s" repeatCount="indefinite"/>'
        f'<ellipse cx="{30*sx}" cy="94" rx="8" ry="5.5" fill="{SKIN}" stroke="{OL}" stroke-width="{SW-0.6}"/></g>'
        for i, sx in enumerate((-1, 1)))
    lap = (f'<path d="M-36,62 h72 a5,5 0 0 1 5,5 v29 h-82 v-29 a5,5 0 0 1 5,-5z" fill="{LAPTOP}" stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round"/>'
           f'<path d="M-31,67 h30 l-11,29 h-19z" fill="#ffffff" opacity="0.35"/>'
           f'<circle cx="0" cy="80" r="5" fill="#fff" stroke="{LAPTOP2}" stroke-width="1.5"><animate attributeName="opacity" values="0.55;1;0.55" dur="3.6s" repeatCount="indefinite"/></circle>')
    return (f'<g transform="translate({x:g} {y:g}) scale({s:g})">{_torso()}{sleeves}'
            + _bob(head(pid), amp=1.2, dur=3.4) + typing + lap + '</g>')
