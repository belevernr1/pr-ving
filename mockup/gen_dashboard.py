#!/usr/bin/env python3
"""Generates a mockup illustration of a Home Assistant kiosk dashboard on an iPad."""
import cairosvg

FONT = "DejaVu Sans, Liberation Sans, sans-serif"

# Canvas / iPad frame (landscape)
W, H = 1680, 1200

def rrect(x, y, w, h, r, fill, stroke=None, sw=1, opacity=1.0, extra=""):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" ry="{r}" fill="{fill}" opacity="{opacity}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    s += f' {extra}/>'
    return s

def text(x, y, s, size, fill, weight="normal", anchor="start", spacing=None, opacity=1.0):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{ls} opacity="{opacity}">{s}</text>')

def card(x, y, w, h, r=26):
    # glassmorphism-ish card
    return (rrect(x, y, w, h, r, "url(#cardgrad)", stroke="#ffffff", sw=1.2, opacity=1) +
            rrect(x, y, w, h, r, "none", stroke="#ffffff", sw=1.2, opacity=0.0))

parts = []
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')

# ---- defs ----
parts.append('''<defs>
  <linearGradient id="screen" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0d1424"/>
    <stop offset="0.5" stop-color="#0a0f1c"/>
    <stop offset="1" stop-color="#05070e"/>
  </linearGradient>
  <radialGradient id="glow1" cx="0.18" cy="0.12" r="0.5">
    <stop offset="0" stop-color="#2a3f6b" stop-opacity="0.55"/>
    <stop offset="1" stop-color="#2a3f6b" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glow2" cx="0.9" cy="0.95" r="0.5">
    <stop offset="0" stop-color="#5b3f8a" stop-opacity="0.45"/>
    <stop offset="1" stop-color="#5b3f8a" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="cardgrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffffff" stop-opacity="0.10"/>
    <stop offset="1" stop-color="#ffffff" stop-opacity="0.035"/>
  </linearGradient>
  <linearGradient id="amber" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#ffd27a"/>
    <stop offset="1" stop-color="#ff9e3d"/>
  </linearGradient>
  <linearGradient id="amberdim" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#3a2f1e"/>
    <stop offset="1" stop-color="#2a2114"/>
  </linearGradient>
  <linearGradient id="cyan" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#7ef0e8"/>
    <stop offset="1" stop-color="#3fb6d6"/>
  </linearGradient>
  <linearGradient id="purple" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#b69bff"/>
    <stop offset="1" stop-color="#7b62e8"/>
  </linearGradient>
  <linearGradient id="media" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#ff7a59"/>
    <stop offset="0.5" stop-color="#d6457a"/>
    <stop offset="1" stop-color="#7b3fb0"/>
  </linearGradient>
  <linearGradient id="railactive" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffd27a"/>
    <stop offset="1" stop-color="#ff9e3d"/>
  </linearGradient>
</defs>''')

# ---- iPad body ----
parts.append(rrect(0, 0, W, H, 70, "#15171c"))
parts.append(rrect(10, 10, W-20, H-20, 62, "#0b0d11", stroke="#2a2d34", sw=2))
# screen
SX, SY, SW2, SH2 = 44, 44, W-88, H-88
parts.append(f'<clipPath id="screenclip"><rect x="{SX}" y="{SY}" width="{SW2}" height="{SH2}" rx="40"/></clipPath>')
parts.append(f'<g clip-path="url(#screenclip)">')
parts.append(rrect(SX, SY, SW2, SH2, 40, "url(#screen)"))
parts.append(f'<rect x="{SX}" y="{SY}" width="{SW2}" height="{SH2}" fill="url(#glow1)"/>')
parts.append(f'<rect x="{SX}" y="{SY}" width="{SW2}" height="{SH2}" fill="url(#glow2)"/>')

# front camera dot
parts.append(f'<circle cx="{W/2}" cy="28" r="5" fill="#23262d"/>')
parts.append(f'<circle cx="{W/2}" cy="28" r="2" fill="#3a4a6a"/>')

# ===== CONTENT =====
PAD = 40
cx0 = SX + PAD          # 84
cy0 = SY + PAD          # 84
contentR = SX + SW2 - PAD  # right edge

# ---- Left nav rail ----
railX, railY, railW = cx0, cy0, 96
railH = SH2 - 2*PAD
parts.append(rrect(railX, railY, railW, railH, 30, "url(#cardgrad)", stroke="#ffffff", sw=1.2))
# nav icons (drawn simple). active = home
nav_cy = railY + 70
def navslot(cy, active=False):
    out = ""
    if active:
        out += rrect(railX+16, cy-32, railW-32, 64, 20, "url(#railactive)")
    return out, railX+railW/2, cy

# Home (active)
s,_cx,_cy = navslot(nav_cy, True); parts.append(s)
# home icon
parts.append(f'<path d="M {_cx-16} {_cy+2} L {_cx} {_cy-16} L {_cx+16} {_cy+2} M {_cx-11} {_cy-2} L {_cx-11} {_cy+15} L {_cx+11} {_cy+15} L {_cx+11} {_cy-2}" fill="none" stroke="#1a1205" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>')

def icon_bulb(cx, cy, col):
    return (f'<circle cx="{cx}" cy="{cy-3}" r="13" fill="none" stroke="{col}" stroke-width="3.2"/>'
            f'<rect x="{cx-6}" y="{cy+10}" width="12" height="7" rx="3" fill="{col}"/>')
def icon_thermo(cx, cy, col):
    return (f'<rect x="{cx-4}" y="{cy-16}" width="8" height="22" rx="4" fill="none" stroke="{col}" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="{cy+10}" r="7" fill="{col}"/>')
def icon_media(cx, cy, col):
    return f'<path d="M {cx-8} {cy-12} L {cx-8} {cy+12} L {cx+12} {cy} Z" fill="{col}"/>'
def icon_cam(cx, cy, col):
    return (f'<rect x="{cx-14}" y="{cy-9}" width="20" height="18" rx="4" fill="none" stroke="{col}" stroke-width="3"/>'
            f'<path d="M {cx+6} {cy-3} L {cx+15} {cy-9} L {cx+15} {cy+9} L {cx+6} {cy+3} Z" fill="{col}"/>')

inactive = "#7d889c"
for i,(fn) in enumerate([icon_bulb, icon_thermo, icon_media, icon_cam]):
    cy = nav_cy + 96*(i+1)
    parts.append(fn(railX+railW/2, cy, inactive))

# lock at bottom of rail (kiosk indicator)
lockcy = railY + railH - 56
parts.append(f'<circle cx="{railX+railW/2}" cy="{lockcy}" r="26" fill="#1a2336" stroke="#3a4a6a" sw="1"/>')
parts.append(f'<rect x="{railX+railW/2-11}" y="{lockcy-3}" width="22" height="17" rx="4" fill="#7ef0e8"/>')
parts.append(f'<path d="M {railX+railW/2-7} {lockcy-3} L {railX+railW/2-7} {lockcy-10} A 7 7 0 0 1 {railX+railW/2+7} {lockcy-10} L {railX+railW/2+7} {lockcy-3}" fill="none" stroke="#7ef0e8" stroke-width="3"/>')

# ---- Main content area ----
mx0 = railX + railW + 32   # main left
mTop = cy0

# Header
parts.append(text(mx0, mTop+44, "God kveld, Martin", 44, "#f4f7fc", weight="bold"))
parts.append(text(mx0, mTop+84, "Hjemme  ·  Alt er rolig  ·  3 lys på", 22, "#8a94a6"))

# Right header cluster: clock + weather pill
parts.append(text(contentR, mTop+50, "20:06", 52, "#f4f7fc", weight="bold", anchor="end"))
parts.append(text(contentR, mTop+84, "Søndag 14. juni", 22, "#8a94a6", anchor="end"))

# weather pill
wpW = 168
wpX = contentR - 360
parts.append(rrect(wpX, mTop+18, wpW, 66, 22, "url(#cardgrad)", stroke="#ffffff", sw=1.2))
# sun/cloud icon
parts.append(f'<circle cx="{wpX+34}" cy="{mTop+42}" r="13" fill="url(#amber)"/>')
parts.append(f'<path d="M {wpX+30} {mTop+58} q 0 -14 16 -14 q 16 0 16 14 z" fill="#9fb0c8"/>')
parts.append(text(wpX+72, mTop+44, "16°", 30, "#f4f7fc", weight="bold"))
parts.append(text(wpX+72, mTop+70, "Lett skyet", 17, "#8a94a6"))

# ===== Card grid =====
gridTop = mTop + 120
gap = 26
mainW = contentR - mx0

# Layout: left big light card, right column (climate + scenes), bottom media full + status
colL_w = mainW*0.46
colR_x = mx0 + colL_w + gap
colR_w = mainW - colL_w - gap

# --- Big "Stue" light card ---
lc_x, lc_y = mx0, gridTop
lc_w, lc_h = colL_w, 430
parts.append(card(lc_x, lc_y, lc_w, lc_h))
parts.append(text(lc_x+30, lc_y+44, "Stue", 28, "#f4f7fc", weight="bold"))
parts.append(text(lc_x+30, lc_y+72, "3 lamper · varmt lys", 18, "#8a94a6"))
# on toggle
parts.append(rrect(lc_x+lc_w-90, lc_y+24, 60, 32, 16, "url(#amber)"))
parts.append(f'<circle cx="{lc_x+lc_w-44}" cy="{lc_y+40}" r="12" fill="#fff"/>')
# circular dimmer
dcx, dcy, dr = lc_x+lc_w/2, lc_y+232, 96
parts.append(f'<circle cx="{dcx}" cy="{dcy}" r="{dr}" fill="none" stroke="#ffffff" stroke-opacity="0.10" stroke-width="16"/>')
import math
# arc from 135deg to 135+270*0.72
start = 135
sweep = 270*0.72
def arc(cx, cy, r, a0, a1, col, w):
    a0r = math.radians(a0); a1r = math.radians(a1)
    x0 = cx + r*math.cos(a0r); y0 = cy + r*math.sin(a0r)
    x1 = cx + r*math.cos(a1r); y1 = cy + r*math.sin(a1r)
    large = 1 if (a1-a0) > 180 else 0
    return f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 {large} 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
parts.append(arc(dcx, dcy, dr, start, start+sweep, "url(#amber)", 16))
parts.append(text(dcx, dcy+6, "72%", 46, "#f4f7fc", weight="bold", anchor="middle"))
parts.append(text(dcx, dcy+38, "Lysstyrke", 17, "#8a94a6", anchor="middle"))
# three light chips
chipw = (lc_w-60-2*16)/3
for i,(nm,on) in enumerate([("Tak", True),("Sofa", True),("Vindu", False)]):
    chx = lc_x+30 + i*(chipw+16)
    chy = lc_y+lc_h-86
    fill = "url(#amberdim)" if on else "#ffffff"
    op = 1 if on else 0.04
    parts.append(rrect(chx, chy, chipw, 62, 18, fill if on else "#ffffff", opacity=1 if on else 0.05))
    col = "url(#amber)" if on else inactive
    parts.append(icon_bulb(chx+26, chy+30, col))
    parts.append(text(chx+48, chy+30, nm, 18, "#f4f7fc" if on else "#8a94a6", weight="bold"))
    parts.append(text(chx+48, chy+50, "På" if on else "Av", 14, "#ffb74d" if on else "#7d889c"))

# --- Climate card (top right) ---
cl_x, cl_y = colR_x, gridTop
cl_w, cl_h = (colR_w-gap)/2, 200
parts.append(card(cl_x, cl_y, cl_w, cl_h))
parts.append(icon_thermo(cl_x+34, cl_y+44, "url(#cyan)"))
parts.append(text(cl_x+62, cl_y+40, "Klima", 22, "#f4f7fc", weight="bold"))
parts.append(text(cl_x+30, cl_y+108, "21.5°", 52, "#f4f7fc", weight="bold"))
parts.append(text(cl_x+30, cl_y+140, "Mål 22°  ·  Varme", 17, "#8a94a6"))
parts.append(text(cl_x+30, cl_y+172, "Luft 41%  ·  Stue", 16, "#7d889c"))

# --- Camera/door card (top right 2) ---
cam_x = cl_x + cl_w + gap
parts.append(card(cam_x, cl_y, cl_w, cl_h))
parts.append(icon_cam(cam_x+38, cl_y+44, "url(#purple)"))
parts.append(text(cam_x+66, cl_y+40, "Inngang", 22, "#f4f7fc", weight="bold"))
# camera preview block
parts.append(rrect(cam_x+30, cl_y+62, cl_w-60, 80, 14, "#10182a", stroke="#ffffff", sw=1))
parts.append(f'<circle cx="{cam_x+50}" cy="{cl_y+80}" r="5" fill="#ff5b5b"/>')
parts.append(text(cam_x+62, cl_y+85, "LIVE", 14, "#ff8a8a", weight="bold"))
parts.append(text(cam_x+30, cl_y+170, "Dør låst  ·  Ingen bevegelse", 16, "#7d889c"))

# --- Scenes card (right, below climate) ---
sc_x, sc_y = colR_x, gridTop + 200 + gap
sc_w, sc_h = colR_w, 204
parts.append(card(sc_x, sc_y, sc_w, sc_h))
parts.append(text(sc_x+30, sc_y+42, "Scener", 24, "#f4f7fc", weight="bold"))
scenes = [("Kveld","url(#amber)"),("Film","url(#purple)"),("Natt","url(#cyan)"),("Borte","#5a6savedummy")]
scenecols = ["url(#amber)","url(#purple)","url(#cyan)","#6b7689"]
scnames = ["Kveld","Film","Natt","Borte"]
sw_chip = (sc_w-60-3*16)/4
for i in range(4):
    scx = sc_x+30 + i*(sw_chip+16)
    scy = sc_y+64
    parts.append(rrect(scx, scy, sw_chip, sc_h-94, 20, "#ffffff", opacity=0.05))
    # circle accent
    parts.append(f'<circle cx="{scx+sw_chip/2}" cy="{scy+44}" r="22" fill="{scenecols[i]}" opacity="0.9"/>')
    parts.append(text(scx+sw_chip/2, scy+(sc_h-94)-14, scnames[i], 18, "#dfe5ef", weight="bold", anchor="middle"))

# --- Media player (bottom full width) ---
md_x, md_y = mx0, gridTop + 430 + gap
md_w = mainW
md_h = SH2 - 2*PAD - (md_y - cy0)
parts.append(card(md_x, md_y, md_w, md_h))
# album art
art = md_h-48
parts.append(rrect(md_x+24, md_y+24, art, art, 18, "url(#media)"))
parts.append(f'<circle cx="{md_x+24+art/2}" cy="{md_y+24+art/2}" r="{art*0.16}" fill="#0a0f1c" opacity="0.6"/>')
parts.append(f'<circle cx="{md_x+24+art/2}" cy="{md_y+24+art/2}" r="{art*0.05}" fill="#fff" opacity="0.8"/>')
tx = md_x+24+art+28
parts.append(text(tx, md_y+50, "Spiller nå · Sonos Stue", 16, "#8a94a6"))
parts.append(text(tx, md_y+90, "Midnight City", 30, "#f4f7fc", weight="bold"))
parts.append(text(tx, md_y+120, "M83", 20, "#a7b1c2"))
# progress bar
pb_y = md_y+md_h-44
pb_w = md_w - (tx-md_x) - 260
parts.append(rrect(tx, pb_y, pb_w, 7, 4, "#ffffff", opacity=0.12))
parts.append(rrect(tx, pb_y, pb_w*0.46, 7, 4, "url(#cyan)"))
parts.append(f'<circle cx="{tx+pb_w*0.46}" cy="{pb_y+3}" r="8" fill="#fff"/>')
# controls
ctlcx = md_x + md_w - 150
ccy = md_y + md_h/2
parts.append(f'<path d="M {ctlcx-90} {ccy-14} L {ctlcx-104} {ccy} L {ctlcx-90} {ccy+14} M {ctlcx-76} {ccy-14} L {ctlcx-90} {ccy} L {ctlcx-76} {ccy+14}" fill="none" stroke="#cfd6e2" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
parts.append(f'<circle cx="{ctlcx}" cy="{ccy}" r="34" fill="#fff"/>')
parts.append(f'<rect x="{ctlcx-10}" y="{ccy-14}" width="7" height="28" rx="2" fill="#0a0f1c"/>')
parts.append(f'<rect x="{ctlcx+3}" y="{ccy-14}" width="7" height="28" rx="2" fill="#0a0f1c"/>')
parts.append(f'<path d="M {ctlcx+76} {ccy-14} L {ctlcx+90} {ccy} L {ctlcx+76} {ccy+14} M {ctlcx+90} {ccy-14} L {ctlcx+104} {ccy} L {ctlcx+90} {ccy+14}" fill="none" stroke="#cfd6e2" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')

# ---- Kiosk badge (top-right corner overlay) ----
kb_w = 188
kb_x = contentR - kb_w
kb_y = SY + SH2 - 0  # not used

parts.append('</g>')  # end screen clip

# subtle screen reflection top
parts.append(f'<rect x="{SX}" y="{SY}" width="{SW2}" height="{SH2*0.12}" rx="40" fill="#ffffff" opacity="0.025"/>')

parts.append('</svg>')

svg = "\n".join(parts)
with open("/home/user/pr-ving/mockup/dashboard.svg","w") as f:
    f.write(svg)
cairosvg.svg2png(bytestring=svg.encode(), write_to="/home/user/pr-ving/mockup/dashboard.png", output_width=1680, output_height=1200)
print("done")
