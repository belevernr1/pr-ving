#!/usr/bin/env python3
"""HA kiosk dashboard mockups: full overview + a 'Lys' detail sub-page."""
import math, cairosvg

FONT = "DejaVu Sans, Liberation Sans, sans-serif"
W, H = 1680, 1200
inactive = "#7d889c"

def rr(x,y,w,h,r,fill,stroke=None,sw=1,opacity=1.0):
    s=f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" ry="{r}" fill="{fill}" opacity="{opacity}"'
    if stroke: s+=f' stroke="{stroke}" stroke-width="{sw}"'
    return s+'/>'
def tx(x,y,s,size,fill,weight="normal",anchor="start",opacity=1.0):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" opacity="{opacity}">{s}</text>'
def card(x,y,w,h,r=24):
    return rr(x,y,w,h,r,"url(#cardgrad)",stroke="#ffffff",sw=1.2)
def arc(cx,cy,r,a0,a1,col,w):
    a0r=math.radians(a0);a1r=math.radians(a1)
    x0=cx+r*math.cos(a0r);y0=cy+r*math.sin(a0r)
    x1=cx+r*math.cos(a1r);y1=cy+r*math.sin(a1r)
    large=1 if (a1-a0)>180 else 0
    return f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 {large} 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'

DEFS='''<defs>
 <linearGradient id="screen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1424"/><stop offset="0.5" stop-color="#0a0f1c"/><stop offset="1" stop-color="#05070e"/></linearGradient>
 <radialGradient id="glow1" cx="0.18" cy="0.1" r="0.5"><stop offset="0" stop-color="#2a3f6b" stop-opacity="0.5"/><stop offset="1" stop-color="#2a3f6b" stop-opacity="0"/></radialGradient>
 <radialGradient id="glow2" cx="0.92" cy="0.95" r="0.5"><stop offset="0" stop-color="#5b3f8a" stop-opacity="0.4"/><stop offset="1" stop-color="#5b3f8a" stop-opacity="0"/></radialGradient>
 <linearGradient id="cardgrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0.10"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.035"/></linearGradient>
 <linearGradient id="amber" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffd27a"/><stop offset="1" stop-color="#ff9e3d"/></linearGradient>
 <linearGradient id="cyan" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7ef0e8"/><stop offset="1" stop-color="#3fb6d6"/></linearGradient>
 <linearGradient id="purple" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b69bff"/><stop offset="1" stop-color="#7b62e8"/></linearGradient>
 <linearGradient id="green" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7ce6a0"/><stop offset="1" stop-color="#3fb56f"/></linearGradient>
 <linearGradient id="lime" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d8f06a"/><stop offset="1" stop-color="#8fd13f"/></linearGradient>
 <linearGradient id="carblue" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6fd0ff"/><stop offset="1" stop-color="#3b7bf0"/></linearGradient>
 <linearGradient id="media" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff7a59"/><stop offset="0.5" stop-color="#d6457a"/><stop offset="1" stop-color="#7b3fb0"/></linearGradient>
</defs>'''

def frame_open(parts):
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    parts.append(DEFS)
    parts.append(rr(0,0,W,H,70,"#15171c"))
    parts.append(rr(10,10,W-20,H-20,62,"#0b0d11",stroke="#2a2d34",sw=2))
    parts.append(f'<clipPath id="sc"><rect x="44" y="44" width="{W-88}" height="{H-88}" rx="40"/></clipPath>')
    parts.append('<g clip-path="url(#sc)">')
    parts.append(rr(44,44,W-88,H-88,40,"url(#screen)"))
    parts.append(f'<rect x="44" y="44" width="{W-88}" height="{H-88}" fill="url(#glow1)"/>')
    parts.append(f'<rect x="44" y="44" width="{W-88}" height="{H-88}" fill="url(#glow2)"/>')
    parts.append(f'<circle cx="{W/2}" cy="28" r="5" fill="#23262d"/><circle cx="{W/2}" cy="28" r="2" fill="#3a4a6a"/>')
def frame_close(parts):
    parts.append('</g>')
    parts.append(f'<rect x="44" y="44" width="{W-88}" height="120" rx="40" fill="#ffffff" opacity="0.025"/>')
    parts.append('</svg>')

# ---------- icons ----------
def i_home(cx,cy,col,sw=3.2):
    return f'<path d="M {cx-15} {cy+2} L {cx} {cy-14} L {cx+15} {cy+2} M {cx-10} {cy-2} L {cx-10} {cy+14} L {cx+10} {cy+14} L {cx+10} {cy-2}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
def i_bulb(cx,cy,col):
    return f'<circle cx="{cx}" cy="{cy-3}" r="12" fill="none" stroke="{col}" stroke-width="3"/><rect x="{cx-5}" y="{cy+9}" width="10" height="6" rx="3" fill="{col}"/>'
def i_thermo(cx,cy,col):
    return f'<rect x="{cx-4}" y="{cy-15}" width="8" height="20" rx="4" fill="none" stroke="{col}" stroke-width="3"/><circle cx="{cx}" cy="{cy+9}" r="6.5" fill="{col}"/>'
def i_bolt(cx,cy,col):
    return f'<path d="M {cx+3} {cy-16} L {cx-9} {cy+2} L {cx-1} {cy+2} L {cx-4} {cy+16} L {cx+9} {cy-3} L {cx+1} {cy-3} Z" fill="{col}"/>'
def i_car(cx,cy,col):
    return (f'<path d="M {cx-17} {cy+5} L {cx-13} {cy-6} Q {cx-11} {cy-10} {cx-6} {cy-10} L {cx+6} {cy-10} Q {cx+11} {cy-10} {cx+13} {cy-6} L {cx+17} {cy+5} L {cx+17} {cy+10} L {cx-17} {cy+10} Z" fill="none" stroke="{col}" stroke-width="2.8" stroke-linejoin="round"/>'
            f'<circle cx="{cx-9}" cy="{cy+10}" r="3.5" fill="{col}"/><circle cx="{cx+9}" cy="{cy+10}" r="3.5" fill="{col}"/>')
def i_cam(cx,cy,col):
    return f'<rect x="{cx-14}" y="{cy-8}" width="19" height="16" rx="4" fill="none" stroke="{col}" stroke-width="2.8"/><path d="M {cx+5} {cy-2} L {cx+14} {cy-8} L {cx+14} {cy+8} L {cx+5} {cy+2} Z" fill="{col}"/>'
def i_news(cx,cy,col):
    return (f'<rect x="{cx-13}" y="{cy-13}" width="26" height="26" rx="3" fill="none" stroke="{col}" stroke-width="2.8"/>'
            f'<line x1="{cx-8}" y1="{cy-6}" x2="{cx+8}" y2="{cy-6}" stroke="{col}" stroke-width="2.6"/>'
            f'<line x1="{cx-8}" y1="{cy}" x2="{cx+8}" y2="{cy}" stroke="{col}" stroke-width="2.6"/>'
            f'<line x1="{cx-8}" y1="{cy+6}" x2="{cx+3}" y2="{cy+6}" stroke="{col}" stroke-width="2.6"/>')
def i_sun(cx,cy,r=11):
    out=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#amber)"/>'
    for a in range(0,360,45):
        ar=math.radians(a);x0=cx+(r+4)*math.cos(ar);y0=cy+(r+4)*math.sin(ar);x1=cx+(r+9)*math.cos(ar);y1=cy+(r+9)*math.sin(ar)
        out+=f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="url(#amber)" stroke-width="2.4" stroke-linecap="round"/>'
    return out
def i_cloud(cx,cy,col="#9fb0c8",s=1.0):
    return f'<path d="M {cx-16*s} {cy+8*s} q {-9*s} 0 {-9*s} {-9*s} q 0 {-8*s} {9*s} {-8*s} q {2*s} {-9*s} {14*s} {-7*s} q {10*s} {-1*s} {10*s} {9*s} q {8*s} {0} {8*s} {7*s} q 0 {8*s} {-10*s} {8*s} Z" fill="{col}"/>'
def i_rain(cx,cy):
    return i_cloud(cx,cy-3,"#8aa0c0",0.9)+f'<line x1="{cx-6}" y1="{cy+10}" x2="{cx-8}" y2="{cy+16}" stroke="url(#cyan)" stroke-width="2.6" stroke-linecap="round"/><line x1="{cx+2}" y1="{cy+10}" x2="{cx}" y2="{cy+16}" stroke="url(#cyan)" stroke-width="2.6" stroke-linecap="round"/>'

# ---------- nav rail ----------
def nav_rail(parts, active_idx):
    railX,railY,railW = 84,84,150
    railH = H-88-2*40
    parts.append(rr(railX,railY,railW,railH,28,"url(#cardgrad)",stroke="#ffffff",sw=1.2))
    items=[("Hjem",i_home),("Lys",i_bulb),("Klima",i_thermo),("Energi",i_bolt),("Bil",i_car),("Kamera",i_cam),("Nyheter",i_news)]
    n=len(items)
    top=railY+30; slot=(railH-150)/n
    for idx,(name,icn) in enumerate(items):
        cy=top+slot*idx+slot/2
        if idx==active_idx:
            parts.append(rr(railX+14,cy-slot/2+6,railW-28,slot-12,18,"url(#amber)"))
            col="#1a1205"; lblcol="#1a1205"
        else:
            col=inactive; lblcol="#aab4c4"
        parts.append(icn(railX+railW/2, cy-8, col))
        parts.append(tx(railX+railW/2, cy+24, name, 15, lblcol, weight="bold", anchor="middle"))
    # lock bottom
    lcy=railY+railH-44
    parts.append(f'<rect x="{railX+railW/2-11}" y="{lcy-3}" width="22" height="16" rx="4" fill="#7ef0e8"/>')
    parts.append(f'<path d="M {railX+railW/2-7} {lcy-3} L {railX+railW/2-7} {lcy-10} A 7 7 0 0 1 {railX+railW/2+7} {lcy-10} L {railX+railW/2+7} {lcy-3}" fill="none" stroke="#7ef0e8" stroke-width="2.8"/>')
    parts.append(tx(railX+railW/2, lcy+30, "Kiosk", 13, "#7ef0e8", weight="bold", anchor="middle"))
    return railX+railW+30  # returns main x start

# ================= OVERVIEW =================
def build_overview():
    P=[]; frame_open(P)
    mx0=nav_rail(P,0)
    contentR=44+(W-88)-40
    top=84
    # header
    P.append(tx(mx0,top+44,"God kveld, Martin",42,"#f4f7fc",weight="bold"))
    P.append(tx(mx0,top+82,"Hjemme · 2 av 3 hjemme · alt rolig",21,"#8a94a6"))
    P.append(tx(contentR,top+48,"20:14",48,"#f4f7fc",weight="bold",anchor="end"))
    P.append(tx(contentR,top+80,"Søndag 14. juni",20,"#8a94a6",anchor="end"))

    gx=mx0; gw=contentR-mx0; gap=22
    # ---- week weather strip ----
    ws_y=top+108; ws_h=120
    P.append(card(gx,ws_y,gw,ws_h))
    P.append(tx(gx+26,ws_y+34,"Været denne uka",20,"#f4f7fc",weight="bold"))
    P.append(tx(gx+26,ws_y+34,"",1,"#000"))
    days=[("I dag",i_sun,"16°","9°",True),("Man",i_cloud,"15°","8°",False),("Tir",i_rain,"12°","7°",False),
          ("Ons",i_rain,"11°","6°",False),("Tor",i_cloud,"14°","8°",False),("Fre",i_sun,"18°","10°",False),("Lør",i_sun,"19°","11°",False)]
    colw=(gw-300)/7; startx=gx+286
    for i,(d,icn,hi,lo,now) in enumerate(days):
        dx=startx+i*colw+colw/2
        if now: P.append(rr(dx-colw/2+6,ws_y+14,colw-12,ws_h-28,14,"#ffffff",opacity=0.06))
        P.append(tx(dx,ws_y+34,d,15,"#cfd6e2" if not now else "#ffd27a",weight="bold",anchor="middle"))
        if icn==i_sun: P.append(i_sun(dx,ws_y+62,9))
        elif icn==i_cloud: P.append(i_cloud(dx,ws_y+58))
        else: P.append(i_rain(dx,ws_y+58))
        P.append(tx(dx,ws_y+100,hi,17,"#f4f7fc",weight="bold",anchor="middle"))
        P.append(tx(dx+26,ws_y+100,lo,14,"#7d889c",anchor="middle"))

    # ---- 3-col grid, 2 rows ----
    grid_y=ws_y+ws_h+gap
    cw=(gw-2*gap)/3
    ch=(84+(H-88-40-84)-grid_y-gap)/2 - 78  # leave room for news
    ch=300
    col=[gx, gx+cw+gap, gx+2*(cw+gap)]
    r2=grid_y+ch+gap

    # Card 1: Hvem er hjemme
    x,y=col[0],grid_y; P.append(card(x,y,cw,ch))
    P.append(tx(x+26,y+40,"Hvem er hjemme",22,"#f4f7fc",weight="bold"))
    people=[("M","Martin",True,"url(#amber)"),("I","Ingrid",False,"url(#purple)"),("E","Emma",True,"url(#cyan)")]
    for i,(ini,nm,home,c) in enumerate(people):
        py=y+78+i*68
        P.append(f'<circle cx="{x+50}" cy="{py+10}" r="26" fill="{c}"/>')
        P.append(tx(x+50,py+18,ini,22,"#0a0f1c",weight="bold",anchor="middle"))
        P.append(tx(x+90,py+6,nm,20,"#f4f7fc",weight="bold"))
        dot="#5be08a" if home else "#6b7689"
        P.append(f'<circle cx="{x+96}" cy="{py+24}" r="5" fill="{dot}"/>')
        P.append(tx(x+108,py+30,"Hjemme" if home else "Borte",15,"#9fb0c8"))

    # Card 2: Energi nå
    x,y=col[1],grid_y; P.append(card(x,y,cw,ch))
    P.append(i_bolt(x+40,y+34,"url(#lime)"))
    P.append(tx(x+62,y+40,"Strøm nå",22,"#f4f7fc",weight="bold"))
    P.append(tx(x+26,y+96,"1.8",46,"#f4f7fc",weight="bold"))
    P.append(tx(x+108,y+96,"kW",22,"#9fb0c8"))
    P.append(tx(x+26,y+124,"Nett 1.2 kW · Sol 0.6 kW · 3,1 kr/t",15,"#8a94a6"))
    cons=[("Varmtvann",0.78,"url(#amber)"),("Elbil-lader",0.62,"url(#carblue)"),("Komfyr",0.30,"url(#media)")]
    for i,(nm,frac,c) in enumerate(cons):
        by=y+150+i*44
        P.append(tx(x+26,by+12,nm,15,"#cfd6e2"))
        P.append(rr(x+26,by+18,cw-52,9,5,"#ffffff",opacity=0.10))
        P.append(rr(x+26,by+18,(cw-52)*frac,9,5,c))

    # Card 3: Klima
    x,y=col[2],grid_y; P.append(card(x,y,cw,ch))
    P.append(i_thermo(x+38,y+36,"url(#cyan)"))
    P.append(tx(x+60,y+40,"Klima",22,"#f4f7fc",weight="bold"))
    dcx,dcy,dr=x+cw/2,y+150,68
    P.append(f'<circle cx="{dcx}" cy="{dcy}" r="{dr}" fill="none" stroke="#ffffff" stroke-opacity="0.10" stroke-width="13"/>')
    P.append(arc(dcx,dcy,dr,135,135+270*0.6,"url(#cyan)",13))
    P.append(tx(dcx,dcy+4,"21.5°",34,"#f4f7fc",weight="bold",anchor="middle"))
    P.append(tx(dcx,dcy+30,"Mål 22°",15,"#8a94a6",anchor="middle"))
    P.append(tx(x+26,y+ch-40,"Luft 41% · Stue · Varme på",15,"#8a94a6"))

    # Card 4: Bil
    x,y=col[0],r2; P.append(card(x,y,cw,ch))
    P.append(i_car(x+42,y+36,"url(#carblue)"))
    P.append(tx(x+66,y+42,"Bilen",22,"#f4f7fc",weight="bold"))
    P.append(tx(contentR if False else x+cw-26,y+40,"Låst",15,"#5be08a",weight="bold",anchor="end"))
    # battery
    P.append(tx(x+26,y+108,"312 km",40,"#f4f7fc",weight="bold"))
    P.append(tx(x+26,y+138,"78% batteri · parkert hjemme",16,"#8a94a6"))
    P.append(rr(x+26,y+158,cw-52,16,8,"#ffffff",opacity=0.10))
    P.append(rr(x+26,y+158,(cw-52)*0.78,16,8,"url(#green)"))
    P.append(tx(x+26,y+ch-40,"Klima i bil: av · sist kjørt 09:40",15,"#8a94a6"))

    # Card 5: Elbil-lader
    x,y=col[1],r2; P.append(card(x,y,cw,ch))
    P.append(i_bolt(x+40,y+34,"url(#green)"))
    P.append(tx(x+62,y+40,"Elbil-lader",22,"#f4f7fc",weight="bold"))
    P.append(f'<circle cx="{x+cw-40}" cy="{y+34}" r="7" fill="#5be08a"/>')
    P.append(tx(x+cw-54,y+40,"Lader",15,"#5be08a",weight="bold",anchor="end"))
    dcx,dcy,dr=x+cw/2,y+150,66
    P.append(f'<circle cx="{dcx}" cy="{dcy}" r="{dr}" fill="none" stroke="#ffffff" stroke-opacity="0.10" stroke-width="13"/>')
    P.append(arc(dcx,dcy,dr,135,135+270*0.64,"url(#green)",13))
    P.append(tx(dcx,dcy-2,"64%",32,"#f4f7fc",weight="bold",anchor="middle"))
    P.append(tx(dcx,dcy+24,"7.4 kW",15,"#8a94a6",anchor="middle"))
    P.append(tx(x+26,y+ch-40,"1t 20m igjen · +18,4 kWh i økt",15,"#8a94a6"))

    # Card 6: Kamera
    x,y=col[2],r2; P.append(card(x,y,cw,ch))
    P.append(i_cam(x+40,y+34,"url(#purple)"))
    P.append(tx(x+62,y+40,"Inngang",22,"#f4f7fc",weight="bold"))
    P.append(rr(x+26,y+56,cw-52,ch-130,14,"#10182a",stroke="#ffffff",sw=1))
    # fake night-vision scene
    P.append(f'<circle cx="{x+cw/2}" cy="{y+56+(ch-130)/2}" r="{(ch-130)/2-14}" fill="#16233a" opacity="0.6"/>')
    P.append(f'<circle cx="{x+40}" cy="{y+74}" r="5" fill="#ff5b5b"/>')
    P.append(tx(x+54,y+79,"LIVE",14,"#ff8a8a",weight="bold"))
    P.append(tx(x+26,y+ch-26,"Dør låst · ingen bevegelse 12m",15,"#8a94a6"))

    # ---- News strip ----
    nx=gx; ny=r2+ch+gap; nh=84+(H-88-40)-ny-0
    nh=ny  # placeholder
    ny=r2+ch+gap
    nh=(44+(H-88)-40)-ny
    P.append(card(gx,ny,gw,nh))
    P.append(i_news(gx+44,ny+nh/2,"url(#amber)"))
    P.append(tx(gx+76,ny+34,"Nyheter",20,"#f4f7fc",weight="bold"))
    heads=[("NRK","Lokalt: Ny ladepark åpner i sentrum neste uke","12m"),
           ("VG","Strømprisene faller i Sør-Norge til helgen","41m")]
    hx=gx+76
    for i,(src,h,t) in enumerate(heads):
        hy=ny+30+i*36
        P.append(tx(hx,hy+30,src,15,"#ffb74d",weight="bold"))
        P.append(tx(hx+58,hy+30,h,17,"#dfe5ef"))
        P.append(tx(gx+gw-26,hy+30,t,14,"#7d889c",anchor="end"))
    frame_close(P)
    svg="\n".join(P)
    cairosvg.svg2png(bytestring=svg.encode(),write_to="/home/user/pr-ving/mockup/overview.png",output_width=1680,output_height=1200)

# ================= LIGHTS DETAIL =================
def build_lights():
    P=[]; frame_open(P)
    mx0=nav_rail(P,1)
    contentR=44+(W-88)-40
    top=84
    P.append(tx(mx0,top+44,"Lys",42,"#f4f7fc",weight="bold"))
    P.append(tx(mx0,top+82,"4 rom · 7 lamper på · varmt lys",21,"#8a94a6"))
    # master all off / scenes on right
    P.append(rr(contentR-300,top+18,140,52,16,"#ffffff",opacity=0.06))
    P.append(tx(contentR-230,top+50,"Alt av",18,"#dfe5ef",weight="bold",anchor="middle"))
    P.append(rr(contentR-150,top+18,150,52,16,"url(#amber)"))
    P.append(tx(contentR-75,top+50,"Kveld-scene",17,"#1a1205",weight="bold",anchor="middle"))

    gx=mx0; gw=contentR-mx0; gap=22
    grid_y=top+108
    cw=(gw-gap)/2
    ch=(44+(H-88)-40-grid_y-gap)/2
    rooms=[("Stue",3,72,True),("Kjøkken",2,90,True),("Soverom",1,30,True),("Bad",1,0,False)]
    pos=[(gx,grid_y),(gx+cw+gap,grid_y),(gx,grid_y+ch+gap),(gx+cw+gap,grid_y+ch+gap)]
    for (nm,lamps,bri,on),(x,y) in zip(rooms,pos):
        P.append(card(x,y,cw,ch))
        P.append(i_bulb(x+38,y+40,"url(#amber)" if on else inactive))
        P.append(tx(x+62,y+44,nm,24,"#f4f7fc",weight="bold"))
        P.append(tx(x+62,y+68,f"{lamps} lamper",15,"#8a94a6"))
        # toggle
        tgc="url(#amber)" if on else "#ffffff"
        P.append(rr(x+cw-86,y+24,58,30,15,tgc,opacity=1 if on else 0.12))
        P.append(f'<circle cx="{x+cw-(44 if on else 72)}" cy="{y+39}" r="11" fill="#fff"/>')
        # brightness slider
        sy=y+ch-92
        P.append(tx(x+26,sy-6,"Lysstyrke",15,"#9fb0c8"))
        P.append(tx(x+cw-26,sy-6,f"{bri}%" if on else "Av",15,"#ffb74d" if on else "#7d889c",anchor="end"))
        P.append(rr(x+26,sy+6,cw-52,12,6,"#ffffff",opacity=0.10))
        if on:
            P.append(rr(x+26,sy+6,(cw-52)*bri/100,12,6,"url(#amber)"))
            P.append(f'<circle cx="{x+26+(cw-52)*bri/100}" cy="{sy+12}" r="11" fill="#fff"/>')
        # color temp row
        cy2=y+ch-44
        P.append(tx(x+26,cy2,"Farge",15,"#9fb0c8"))
        sw=44
        cols=["#ffd27a","#fff1d6","#eaf2ff","#bcd2ff"]
        for i,c in enumerate(cols):
            P.append(f'<circle cx="{x+120+i*52}" cy="{cy2-5}" r="14" fill="{c}"/>')
            if i==0 and on: P.append(f'<circle cx="{x+120+i*52}" cy="{cy2-5}" r="18" fill="none" stroke="#ffd27a" stroke-width="2.5"/>')
    frame_close(P)
    svg="\n".join(P)
    cairosvg.svg2png(bytestring=svg.encode(),write_to="/home/user/pr-ving/mockup/lights.png",output_width=1680,output_height=1200)

build_overview()
build_lights()
print("done")
