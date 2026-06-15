#!/usr/bin/env python3
"""HA kiosk dashboard mockup v3 - inspired by Tunet / ha-fusion glassmorphism."""
import math, cairosvg
FONT="DejaVu Sans, Liberation Sans, sans-serif"
W,H=1680,1200
muted="#8794a8"; dim="#62708a"

def rr(x,y,w,h,r,fill,stroke=None,sw=1,op=1.0):
    s=f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" ry="{r}" fill="{fill}" opacity="{op}"'
    if stroke:s+=f' stroke="{stroke}" stroke-width="{sw}"'
    return s+'/>'
def tx(x,y,s,sz,fill,w="normal",a="start",op=1.0,ls=None):
    e=f' letter-spacing="{ls}"' if ls else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{sz}" font-weight="{w}" fill="{fill}" text-anchor="{a}" opacity="{op}"{e}>{s}</text>'
def card(x,y,w,h,r=24):
    return rr(x,y,w,h,r,"url(#glass)",stroke="#ffffff",sw=1.1,op=1)
def arc(cx,cy,r,a0,a1,col,w):
    a0r=math.radians(a0);a1r=math.radians(a1)
    x0=cx+r*math.cos(a0r);y0=cy+r*math.sin(a0r);x1=cx+r*math.cos(a1r);y1=cy+r*math.sin(a1r)
    large=1 if (a1-a0)>180 else 0
    return f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 {large} 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
def spark(pts,x,y,w,h,col,fill=None):
    n=len(pts);mn=min(pts);mx=max(pts);rng=(mx-mn) or 1
    P=[(x+i/(n-1)*w, y+h-(v-mn)/rng*h) for i,v in enumerate(pts)]
    d="M "+" L ".join(f"{px:.1f} {py:.1f}" for px,py in P)
    out=""
    if fill:
        out+=f'<path d="{d} L {x+w:.1f} {y+h:.1f} L {x:.1f} {y+h:.1f} Z" fill="{fill}" opacity="0.9"/>'
    out+=f'<path d="{d}" fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
    return out

DEFS='''<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a141c"/><stop offset="0.5" stop-color="#0a1620"/><stop offset="1" stop-color="#070d14"/></linearGradient>
 <radialGradient id="b1" cx="0.15" cy="0.2" r="0.55"><stop offset="0" stop-color="#1d6a73" stop-opacity="0.45"/><stop offset="1" stop-color="#1d6a73" stop-opacity="0"/></radialGradient>
 <radialGradient id="b2" cx="0.85" cy="0.15" r="0.5"><stop offset="0" stop-color="#3a4f8a" stop-opacity="0.4"/><stop offset="1" stop-color="#3a4f8a" stop-opacity="0"/></radialGradient>
 <radialGradient id="b3" cx="0.7" cy="0.95" r="0.55"><stop offset="0" stop-color="#5a3a7a" stop-opacity="0.38"/><stop offset="1" stop-color="#5a3a7a" stop-opacity="0"/></radialGradient>
 <linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0.085"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.025"/></linearGradient>
 <linearGradient id="amber" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffd27a"/><stop offset="1" stop-color="#ff9e3d"/></linearGradient>
 <linearGradient id="cyan" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7ef0e8"/><stop offset="1" stop-color="#3fb6d6"/></linearGradient>
 <linearGradient id="green" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7ce6a0"/><stop offset="1" stop-color="#3fb56f"/></linearGradient>
 <linearGradient id="lime" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e0f06a"/><stop offset="1" stop-color="#8fd13f"/></linearGradient>
 <linearGradient id="blue" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6fd0ff"/><stop offset="1" stop-color="#3b7bf0"/></linearGradient>
 <linearGradient id="poster" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a4a3a"/><stop offset="0.5" stop-color="#5a4a32"/><stop offset="1" stop-color="#221a14"/></linearGradient>
 <linearGradient id="album" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff8a5b"/><stop offset="0.5" stop-color="#e0556a"/><stop offset="1" stop-color="#7b3fb0"/></linearGradient>
 <linearGradient id="rain" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a6e8a" stop-opacity="0.55"/><stop offset="1" stop-color="#2a6e8a" stop-opacity="0.05"/></linearGradient>
 <linearGradient id="elec" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#caa23a" stop-opacity="0.5"/><stop offset="1" stop-color="#caa23a" stop-opacity="0.02"/></linearGradient>
</defs>'''

P=[]
P.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
P.append(DEFS)
P.append(rr(0,0,W,H,70,"#15171c"))
P.append(rr(10,10,W-20,H-20,62,"#0b0d11",stroke="#2a2d34",sw=2))
P.append(f'<clipPath id="sc"><rect x="44" y="44" width="{W-88}" height="{H-88}" rx="40"/></clipPath>')
P.append('<g clip-path="url(#sc)">')
P.append(rr(44,44,W-88,H-88,40,"url(#bg)"))
for b in ("b1","b2","b3"):
    P.append(f'<rect x="44" y="44" width="{W-88}" height="{H-88}" fill="url(#{b})"/>')
P.append(f'<circle cx="{W/2}" cy="28" r="5" fill="#23262d"/><circle cx="{W/2}" cy="28" r="2" fill="#3a4a6a"/>')

L=84; R=W-84; GW=R-L
# ---------- Header ----------
top=92
P.append(tx(L,top+34,"HJEMME",46,"#e7edf5",w="bold",ls="14"))
P.append(tx(L,top+64,"MANDAG · 15. JUNI",17,muted,ls="3"))
P.append(tx(R,top+44,"19:53",54,"#e7edf5",w="bold",a="end",ls="2"))

# ---------- presence + status chips ----------
cy=top+96
def pill(x,w,h=44,r=22): P.append(rr(x,cy,w,h,r,"url(#glass)",stroke="#ffffff",sw=1.0))
# person 1
x=L
for ini,nm,st,c,home in [("M","Martin","HJEMME","url(#amber)",True),("I","Ingrid","BORTE","url(#purple)" ,False)]:
    w=190
    P.append(rr(x,cy,w,44,22,"url(#glass)",stroke="#ffffff",sw=1.0))
    P.append(f'<circle cx="{x+26}" cy="{cy+22}" r="15" fill="{c if c!="url(#purple)" else "#8b7bf0"}"/>')
    P.append(tx(x+26,cy+28,ini,15,"#0a0f1c",w="bold",a="middle"))
    dotc="#5be08a" if home else "#6b7689"
    P.append(f'<circle cx="{x+38}" cy="{cy+12}" r="5" fill="{dotc}" stroke="#0b1620" stroke-width="2"/>')
    P.append(tx(x+50,cy+20,nm,15,"#e7edf5",w="bold"))
    P.append(tx(x+50,cy+36,st,11,muted,ls="1"))
    x+=w+12
# status pills
for label,val,c in [("Sonos","Spiller","url(#cyan)"),("Elbil","Lader 64%","url(#green)"),("Strøm","135 øre","url(#lime)"),("Inne","23.7°","url(#amber)")]:
    w=150
    P.append(rr(x,cy,w,44,22,"url(#glass)",stroke="#ffffff",sw=1.0))
    P.append(f'<circle cx="{x+22}" cy="{cy+22}" r="6" fill="{c}"/>')
    P.append(tx(x+38,cy+20,label,13,muted))
    P.append(tx(x+38,cy+36,val,14,"#e7edf5",w="bold"))
    x+=w+12

# ---------- tab nav (sub-pages) ----------
ty=cy+62
tabs=["HJEM","LYS","KLIMA","ENERGI","MEDIA","KAMERA"]
tx0=L
for i,t in enumerate(tabs):
    w=22+len(t)*10.5
    if i==0:
        P.append(rr(tx0,ty,w,42,21,"url(#amber)"))
        P.append(tx(tx0+w/2,ty+27,t,15,"#1a1205",w="bold",a="middle",ls="1"))
    else:
        P.append(rr(tx0,ty,w,42,21,"url(#glass)",stroke="#ffffff",sw=1.0))
        P.append(tx(tx0+w/2,ty+27,t,15,"#cdd6e3",w="bold",a="middle",ls="1"))
    tx0+=w+12
# edit/settings on right
for i,lbl in enumerate(["✎","⚙"]):
    P.append(f'<circle cx="{R-18-i*48}" cy="{ty+21}" r="18" fill="url(#glass)" stroke="#ffffff" stroke-width="1"/>')
P.append(tx(R-18,ty+27,"✎",16,"#cdd6e3",a="middle"))
P.append(tx(R-66,ty+28,"⚙",17,"#cdd6e3",a="middle"))

# ============ MASONRY GRID ============
gy=ty+62
gap=22
cw=(GW-3*gap)/4
colx=[L+i*(cw+gap) for i in range(4)]
gridbottom=44+(H-88)-40
# ---- Column A ----
# Vær
x,y=colx[0],gy; ch=286; P.append(card(x,y,cw,ch))
P.append(tx(x+24,y+38,"VÆR · HJEMME",13,muted,ls="2"))
P.append(rr(x+cw-96,y+18,72,28,14,"#ffffff",op=0.07)); P.append(tx(x+cw-60,y+37,"REGN",13,"#9fc3e0",w="bold",a="middle"))
# cloud + rain
P.append(f'<path d="M {x+44} {y+96} q -16 0 -16 -16 q 0 -14 16 -14 q 3 -16 24 -12 q 18 -2 18 16 q 14 0 14 12 q 0 14 -18 14 Z" fill="#9fb0c8"/>')
for rx in range(-2,5):
    P.append(f'<line x1="{x+40+rx*9}" y1="{y+104}" x2="{x+36+rx*9}" y2="{y+116}" stroke="url(#cyan)" stroke-width="2.4" stroke-linecap="round"/>')
P.append(tx(x+cw-24,y+104,"4.1°",44,"#e7edf5",w="bold",a="end"))
# temp graph
P.append(spark([5,4.2,4,4.1,3.6,3.8,4.5,5.2],x+24,y+150,cw-48,46,"url(#cyan)","url(#rain)"))
days=[("Tir","17°"),("Ons","17°"),("Tor","18°"),("Fre","21°")]
for i,(d,t) in enumerate(days):
    dx=x+24+i*((cw-48)/4)+((cw-48)/4)/2
    P.append(tx(dx,y+228,d,13,muted,a="middle"))
    P.append(f'<circle cx="{dx}" cy="{y+246}" r="7" fill="#9fb0c8"/>')
    P.append(tx(dx,y+274,t,15,"#dfe5ef",w="bold",a="middle"))
# Alarm
x,y=colx[0],gy+286+gap; ch=234; P.append(card(x,y,cw,ch))
P.append(f'<circle cx="{x+40}" cy="{y+42}" r="20" fill="none" stroke="url(#green)" stroke-width="3"/>')
P.append(f'<path d="M {x+32} {y+42} l 6 6 l 12 -14" fill="none" stroke="url(#green)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
P.append(tx(x+cw-24,y+34,"FRAKOBLET",13,"#9fc3e0",w="bold",a="end",ls="1"))
P.append(tx(x+24,y+108,"Borte",36,"#e7edf5",w="bold"))
P.append(tx(x+24,y+138,"HUSALARM",13,muted,ls="2"))
P.append(rr(x+24,y+162,cw-48,48,16,"#ffffff",op=0.06))
P.append(tx(x+cw/2,y+192,"Aktiver",17,"#dfe5ef",w="bold",a="middle"))
# Klima Varmtvann
x,y=colx[0],gy+286+234+2*gap; ch=252; P.append(card(x,y,cw,ch))
P.append(f'<rect x="{x+30}" y="{y+24}" width="8" height="20" rx="4" fill="none" stroke="url(#amber)" stroke-width="3"/><circle cx="{x+34}" cy="{y+50}" r="7" fill="url(#amber)"/>')
P.append(tx(x+52,y+40,"Varmtvann",20,"#e7edf5",w="bold"))
P.append(tx(x+cw-24,y+38,"VARMER",13,"#ffce8a",w="bold",a="end",ls="1"))
P.append(tx(x+24,y+118,"22.0°",46,"#e7edf5",w="bold"))
# -/+ row
P.append(rr(x+24,y+150,60,52,16,"#ffffff",op=0.06)); P.append(tx(x+54,y+184,"–",28,"#dfe5ef",a="middle"))
P.append(rr(x+cw-84,y+150,60,52,16,"#ffffff",op=0.06)); P.append(tx(x+cw-54,y+183,"+",26,"#dfe5ef",a="middle"))
P.append(tx(x+cw/2,y+183,"22°",22,"#e7edf5",w="bold",a="middle"))
P.append(tx(x+24,y+232,"Mål 22° · Idle",14,muted))

# ---- Column B ----
# Strøm Nordpool
x,y=colx[1],gy; ch=286; P.append(card(x,y,cw,ch))
P.append(f'<path d="M {x+38} {y+24} L {x+26} {y+46} L {x+36} {y+46} L {x+32} {y+62} L {x+46} {y+40} L {x+36} {y+40} Z" fill="url(#lime)"/>')
P.append(tx(x+56,y+40,"STRØM",13,muted,ls="2"))
P.append(rr(x+cw-100,y+18,76,28,14,"#ffffff",op=0.07)); P.append(tx(x+cw-62,y+37,"NORMAL",12,"#cde0a0",w="bold",a="middle"))
P.append(tx(x+24,y+96,"135",44,"#e7edf5",w="bold")); P.append(tx(x+118,y+96,"øre/kWh",18,muted))
import random
random.seed(3)
pts=[20,18,22,25,30,28,35,60,95,70,45,40,38,42,50,48,55,80,120,90,60,50,45,40]
P.append(spark(pts,x+24,y+126,cw-48,110,"url(#lime)","url(#elec)"))
P.append(tx(x+24,y+264,"I dag · forbruk 18,4 kWh · 101 kr",14,muted))
# Media Sonos
x,y=colx[1],gy+286+gap; ch=234; P.append(card(x,y,cw,ch))
art=ch-48
P.append(rr(x+24,y+24,art,art,16,"url(#album)"))
P.append(f'<circle cx="{x+24+art/2}" cy="{y+24+art/2}" r="{art*0.13}" fill="#0a0f1c" opacity="0.55"/>')
tx0=x+24+art+22
P.append(tx(tx0,y+44,"SONOS · STUE",12,muted,ls="2"))
P.append(tx(tx0,y+82,"Johnny and Mary",22,"#e7edf5",w="bold"))
P.append(tx(tx0,y+108,"Todd Terje",16,muted))
# progress + controls
P.append(rr(tx0,y+136,cw-(tx0-x)-24,6,3,"#ffffff",op=0.14))
P.append(rr(tx0,y+136,(cw-(tx0-x)-24)*0.4,6,3,"url(#cyan)"))
ccx=tx0+ (cw-(tx0-x)-24)/2
cyy=y+186
P.append(f'<path d="M {ccx-54} {cyy-11} L {ccx-66} {cyy} L {ccx-54} {cyy+11} Z" fill="#cfd6e2"/>')
P.append(f'<circle cx="{ccx}" cy="{cyy}" r="22" fill="#fff"/>')
P.append(f'<rect x="{ccx-7}" y="{cyy-10}" width="5" height="20" rx="2" fill="#0a0f1c"/><rect x="{ccx+2}" y="{cyy-10}" width="5" height="20" rx="2" fill="#0a0f1c"/>')
P.append(f'<path d="M {ccx+54} {cyy-11} L {ccx+66} {cyy} L {ccx+54} {cyy+11} Z" fill="#cfd6e2"/>')
# Lys Kjøkken
x,y=colx[1],gy+286+234+2*gap; ch=252; P.append(card(x,y,cw,ch))
P.append(f'<circle cx="{x+38}" cy="{y+36}" r="12" fill="none" stroke="url(#amber)" stroke-width="3"/><rect x="{x+33}" y="{y+45}" width="10" height="6" rx="3" fill="url(#amber)"/>')
P.append(tx(x+58,y+40,"Kjøkken",20,"#e7edf5",w="bold"))
P.append(rr(x+cw-86,y+22,58,30,15,"url(#amber)")); P.append(f'<circle cx="{x+cw-42}" cy="{y+37}" r="11" fill="#fff"/>')
P.append(tx(x+24,y+118,"48",40,"#e7edf5",w="bold")); P.append(tx(x+72,y+118,"%",20,muted))
P.append(rr(x+24,y+150,cw-48,16,8,"#ffffff",op=0.10))
P.append(rr(x+24,y+150,(cw-48)*0.48,16,8,"url(#amber)"))
P.append(f'<circle cx="{x+24+(cw-48)*0.48}" cy="{y+158}" r="13" fill="#fff"/>')
P.append(tx(x+24,y+208,"4 av 4 lamper · varmt lys",14,muted))

# ---- Column C ----
# Elbil-lader gauge
x,y=colx[2],gy; ch=286; P.append(card(x,y,cw,ch))
P.append(tx(x+24,y+38,"ELBIL-LADER",13,muted,ls="2"))
P.append(f'<circle cx="{x+cw-32}" cy="{y+32}" r="7" fill="#5be08a"/>'); P.append(tx(x+cw-46,y+37,"Lader",13,"#9fe0b5",w="bold",a="end"))
gcx,gcy,gr=x+cw/2,y+150,72
P.append(f'<circle cx="{gcx}" cy="{gcy}" r="{gr}" fill="none" stroke="#ffffff" stroke-opacity="0.10" stroke-width="14"/>')
P.append(arc(gcx,gcy,gr,135,135+270*0.64,"url(#green)",14))
P.append(tx(gcx,gcy-2,"64%",34,"#e7edf5",w="bold",a="middle"))
P.append(tx(gcx,gcy+24,"7.4 kW",15,muted,a="middle"))
P.append(tx(x+24,y+262,"1t 20m igjen · +18,4 kWh",14,muted))
# Bil
x,y=colx[2],gy+286+gap; ch=234; P.append(card(x,y,cw,ch))
P.append(f'<path d="M {x+30} {y+44} l 4 -12 q 2 -5 8 -5 l 14 0 q 6 0 8 5 l 4 12 l 0 6 l -38 0 Z" fill="none" stroke="url(#blue)" stroke-width="2.6" stroke-linejoin="round"/><circle cx="{x+34}" cy="{y+50}" r="3.5" fill="url(#blue)"/><circle cx="{x+54}" cy="{y+50}" r="3.5" fill="url(#blue)"/>')
P.append(tx(x+76,y+40,"Nissan Leaf",20,"#e7edf5",w="bold"))
P.append(tx(x+cw-24,y+38,"HJEMME",13,"#9fe0b5",w="bold",a="end",ls="1"))
P.append(tx(x+24,y+110,"71%",40,"#e7edf5",w="bold")); P.append(tx(x+116,y+110,"· 198 km",18,muted))
P.append(rr(x+24,y+130,cw-48,14,7,"#ffffff",op=0.10)); P.append(rr(x+24,y+130,(cw-48)*0.71,14,7,"url(#green)"))
P.append(tx(x+24,y+182,"Frakoblet · kupé 6.3°",14,muted))
# Kamera
x,y=colx[2],gy+286+234+2*gap; ch=252; P.append(card(x,y,cw,ch))
P.append(rr(x+18,y+18,cw-36,ch-72,16,"#10202a"))
P.append(f'<rect x="{x+18}" y="{y+18}" width="{cw-36}" height="{ch-72}" rx="16" fill="url(#b1)" opacity="0.5"/>')
# faux hedge/house
P.append(f'<rect x="{x+18}" y="{y+ch-110}" width="{cw-36}" height="42" fill="#1c3a2a" opacity="0.7"/>')
P.append(f'<rect x="{x+60}" y="{y+70}" width="80" height="60" rx="6" fill="#2a3340" opacity="0.8"/>')
P.append(f'<circle cx="{x+30}" cy="{y+36}" r="5" fill="#ff5b5b"/>'); P.append(tx(x+44,y+41,"LIVE",13,"#ff9a9a",w="bold"))
P.append(tx(x+24,y+ch-26,"Inngang · ingen bevegelse 12m",14,muted))

# ---- Column D ----
# Media TV poster (tall)
x,y=colx[3],gy; ch=392; P.append(card(x,y,cw,ch,r=22))
P.append(rr(x+14,y+14,cw-28,ch-86,16,"url(#poster)"))
# silhouette knight
P.append(f'<circle cx="{x+cw/2}" cy="{y+150}" r="46" fill="#5a5240" opacity="0.6"/>')
P.append(f'<rect x="{x+cw/2-40}" y="{y+196}" width="80" height="90" rx="20" fill="#3a3528" opacity="0.7"/>')
P.append(f'<rect x="{x+14}" y="{y+ch-150}" width="{cw-28}" height="64" fill="#000000" opacity="0.0"/>')
P.append(tx(x+28,y+ch-78,"NÅ SPILLER · TV STUE",12,"#cbb98a",ls="2"))
P.append(tx(x+28,y+ch-50,"A Knight of the",21,"#f2ecd9",w="bold"))
P.append(tx(x+28,y+ch-26,"Seven Kingdoms",21,"#f2ecd9",w="bold"))
# Vifte
x,y=colx[3],gy+392+gap; ch=188; P.append(card(x,y,cw,ch))
P.append(f'<g transform="translate({x+38},{y+38})"><path d="M0 0 q -16 -8 0 -20 q 16 8 0 20 M0 0 q 8 -16 20 0 q -8 16 -20 0 M0 0 q 16 8 0 20 q -16 -8 0 -20 M0 0 q -8 16 -20 0 q 8 -16 20 0Z" fill="url(#cyan)"/><circle r="4" fill="#0a1620"/></g>')
P.append(tx(x+64,y+42,"Vifte kjøkken",19,"#e7edf5",w="bold"))
P.append(tx(x+24,y+108,"88",36,"#e7edf5",w="bold")); P.append(tx(x+66,y+108,"%",18,muted))
P.append(rr(x+24,y+130,cw-48,14,7,"#ffffff",op=0.10)); P.append(rr(x+24,y+130,(cw-48)*0.88,14,7,"url(#cyan)"))
P.append(f'<circle cx="{x+24+(cw-48)*0.88}" cy="{y+137}" r="12" fill="#fff"/>')
# Nyheter
x,y=colx[3],gy+392+188+2*gap; ch=192; P.append(card(x,y,cw,ch))
P.append(f'<rect x="{x+26}" y="{y+24}" width="22" height="22" rx="3" fill="none" stroke="url(#amber)" stroke-width="2.6"/><line x1="{x+31}" y1="{y+31}" x2="{x+43}" y2="{y+31}" stroke="url(#amber)" stroke-width="2.4"/><line x1="{x+31}" y1="{y+37}" x2="{x+43}" y2="{y+37}" stroke="url(#amber)" stroke-width="2.4"/>')
P.append(tx(x+58,y+40,"Nyheter",19,"#e7edf5",w="bold"))
news=[("NRK","Ny ladepark åpner i sentrum","12m"),("VG","Strømprisene faller til helgen","41m")]
for i,(s,h,t) in enumerate(news):
    ny=y+72+i*46
    P.append(tx(x+26,ny+14,s,13,"#ffce8a",w="bold"))
    P.append(tx(x+26,ny+38,h,16,"#dfe5ef"))
    P.append(tx(x+cw-24,ny+14,t,12,dim,a="end"))

P.append('</g>')
P.append(f'<rect x="44" y="44" width="{W-88}" height="120" rx="40" fill="#ffffff" opacity="0.02"/>')
P.append('</svg>')
svg="\n".join(P)
cairosvg.svg2png(bytestring=svg.encode(),write_to="/home/user/pr-ving/mockup/v3_home.png",output_width=1680,output_height=1200)
print("done")
