D='/workspace/penn_campus/CollegeHall'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
# College Hall, University of Pennsylvania (Thomas W. Richards, 1871-73). Victorian Gothic.
# OSM way 51367353: oriented PCA envelope ~84.1 x 51.6 m, polygon area ~2319 m2 (c) OSM contributors, ODbL.
# 6 floors, 110266 sq ft (Penn Facilities / Wikipedia). Green serpentine + sandstone trim; end towers removed.
# Front (College Green / Woodland Walk) = -Y. Lot 11x7 cells (88 x 56 m). Asset NA_CollegeHall_11x7.
LOTX,LOTY=44.0,28.0
# plan (half-open intervals as boxr): three pavilions + recessed connectors
# west pavilion / connector / centre / connector / east pavilion
WP=(-40.0,-25.5,-16.5,12.5)
WC=(-25.5,-10.0,-9.5,9.0)
CP=(-10.0,10.0,-19.5,15.5)
EC=(10.0,25.5,-9.5,9.0)
EP=(25.5,40.0,-16.5,12.5)
BLOCKS=[WP,WC,CP,EC,EP]
ZBASE=4.2; ZB=12.2; ZC=21.6; ZA=22.4; ZTOP=29.5
def cor(F,x0,x1,z,p=1.0,dent=True,m='LimeDark'):
    boxr(x0,x1,0,0.22*p,z,z+0.28,m,F); boxr(x0-0.08,x1+0.08,0,0.5*p,z+0.28,z+0.48,m,F)
    boxr(x0-0.18,x1+0.18,0,p,z+0.48,z+0.78,m,F)
    if dent:
        n=max(1,int((x1-x0)/0.45)); DROPF[0]=True
        for k in range(n+1): box((x0+k*(x1-x0)/n,0.32*p,z+0.3),(0.14,0.14,0.14),m,F)
        n=max(1,int((x1-x0)/1.05))
        for k in range(n+1): box((x0+k*(x1-x0)/n,0.55*p,z+0.48),(0.22,0.45*p,0.1),m,F)
        DROPF[0]=False
def buttress(cx,cy,sx,sy,z0,z1):
    # corner buttress (Gothic veneer), drop-friendly
    DROPF[0]=True
    for k,z in enumerate(np.arange(z0,z1-0.4,0.55)):
        a=1.15 if k%2==0 else 0.75
        boxr(min(cx,cx-sx*a),max(cx,cx-sx*a),min(cy,cy+sy*0.08),max(cy,cy+sy*0.08),z,z+0.48,'LimeDark')
        boxr(min(cx,cx+sx*0.08),max(cx,cx+sx*0.08),min(cy,cy-sy*(1.7-a)),max(cy,cy-sy*(1.7-a)),z,z+0.48,'LimeDark')
    DROPF[0]=False
def mansard(x0,x1,y0,y1,zc,zt):
    o=0.45; z0=zc+0.75; ins=2.4
    P=[(x0-o,y0-o,z0),(x1+o,y0-o,z0),(x1+o,y1+o,z0),(x0-o,y1+o,z0),(x0-o+ins,y0-o+ins,zt-0.6),(x1+o-ins,y0-o+ins,zt-0.6),(x1+o-ins,y1+o-ins,zt-0.6),(x0-o+ins,y1+o-ins,zt-0.6)]
    v=[bm.verts.new(p) for p in P]; n0=len(bm.faces)
    for f in [(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7),(3,2,1,0)]: bm.faces.new([v[i] for i in f])
    tag(n0,'Roof')
    boxr(x0-o+ins,x1+o-ins,y0-o+ins,y1+o-ins,zt-0.6,zt-0.45,'Copper')
    boxr(x0-o-0.05,x1+o+0.05,y0-o-0.05,y1+o+0.05,z0-0.05,z0+0.12,'Copper')
def dormer(F,x,z0):
    boxr(x-1.2,x+1.2,-2.2,0.0,z0,z0+3.4,'Brick',F)
    prism([(x-1.45,z0+3.4),(x+1.45,z0+3.4),(x,z0+4.9)],-2.2,0.15,'Roof',F)
    gothwin(F,x,z0+0.4,1.3,2.6,'Limestone',k=8)
def block(x0,x1,y0,y1,zcorn=ZC,zridge=ZTOP,hip=True):
    # schist base + granite plinth
    boxr(x0-0.14,x1+0.14,y0-0.14,y1+0.14,0,ZBASE,'Rustic')
    boxr(x0-0.28,x1+0.28,y0-0.28,y1+0.28,0,0.85,'Granite')
    DROPF[0]=True
    for z in np.arange(1.35,ZBASE-0.25,0.58):
        boxr(x0-0.16,x1+0.16,y0-0.16,y1+0.16,z,z+0.05,'LimeDark')
    DROPF[0]=False
    # serpentine body (Brick + green BRICKCOL)
    boxr(x0,x1,y0,y1,ZBASE,zcorn,'Brick')
    # flush belts (o<=0.04) — gaps between window rows
    for (z0,z1,o) in ((ZBASE,ZBASE+0.45,0.04),(ZB+0.12,ZB+0.38,0.04),(zcorn-1.05,zcorn,0.04)):
        boxr(x0-o,x1+o,y0-o,y1+o,z0,z1,'LimeDark' if z1-z0<1.0 else 'Limestone')
    mansard(x0,x1,y0,y1,zcorn,zridge)
    # corner buttresses
    for (cx,cy,sx,sy) in ((x1,y0,1,-1),(x0,y0,-1,-1),(x1,y1,1,1),(x0,y1,-1,1)):
        buttress(cx,cy,sx,sy,ZBASE+0.5,zcorn-1.2)
for B in BLOCKS:
    x0,x1,y0,y1=B
    zridge = ZTOP if B is CP else (ZTOP-1.4 if B in (WP,EP) else ZTOP-2.2)
    zcorn = ZC if B is CP else (ZC-0.6 if B in (WP,EP) else ZC-1.2)
    block(x0,x1,y0,y1,zcorn=zcorn,zridge=zridge)
# facade frames
Ff=frame((0,CP[2],0),pi)          # front (-Y)
Fb=frame((0,CP[3],0),0)            # back (+Y)
# pavilion front frames
Fwf=frame(((WP[0]+WP[1])/2,WP[2],0),pi)
Fef=frame(((EP[0]+EP[1])/2,EP[2],0),pi)
Fwb=frame(((WP[0]+WP[1])/2,WP[3],0),0)
Feb=frame(((EP[0]+EP[1])/2,EP[3],0),0)
# connector fronts (recessed)
Fcfw=frame(((WC[0]+WC[1])/2,WC[2],0),pi)
Fcfe=frame(((EC[0]+EC[1])/2,EC[2],0),pi)
Fcbw=frame(((WC[0]+WC[1])/2,WC[3],0),0)
Fcbe=frame(((EC[0]+EC[1])/2,EC[3],0),0)
# end walls
Fw=frame((WP[0],(WP[2]+WP[3])/2,0),pi/2)
Fe=frame((EP[1],(EP[2]+EP[3])/2,0),-pi/2)
# cornices on major fronts
for F,h,zc in ((Ff,10.0,ZC),(Fb,10.0,ZC),(Fwf,7.25,ZC-0.6),(Fef,7.25,ZC-0.6),
               (Fwb,7.25,ZC-0.6),(Feb,7.25,ZC-0.6),(Fcfw,7.75,ZC-1.2),(Fcfe,7.75,ZC-1.2),
               (Fcbw,7.75,ZC-1.2),(Fcbe,7.75,ZC-1.2)):
    cor(F,-h,h,zc,1.05)
cor(Fw,-14.5,14.5,ZC-0.6,1.0); cor(Fe,-14.5,14.5,ZC-0.6,1.0)
# ---- fenestration ----
# rows clear of belts: base 1.4-3.6; mid 5.0-10.8; upper 12.8-16.8; attic 17.6-20.4
UP=[(13.0,4.0,None),(17.8,2.2,None)]
def bay(F,x,tall_base=False,skip=False):
    if skip: return
    if tall_base:
        window(F,x,1.2,1.35,2.8,None,0.12,'LimeDark')
    else:
        window(F,x,1.35,1.2,2.4,None,0.12,'LimeDark')
    gothwin(F,x,5.0,1.45,6.0,'Limestone',k=8)
    gothwin(F,x,13.0,1.35,4.2,'Limestone',k=8)
    window(F,x,18.4,1.15,1.7,None,0,'LimeDark')
# centre pavilion front: 5 bays + central door
CX=[-7.2,-3.6,0.0,3.6,7.2]
for x in CX:
    if abs(x)<0.1: continue
    bay(Ff,x,tall_base=True)
# Gothic arched windows at second storey flanking entrance
for x in (-5.4,5.4):
    gothwin(Ff,x,5.0,2.0,3.4,'Limestone',k=10)
# centre entrance portico
door(Ff,0,2.8,3.8,0.9,None,y=0.14)
# portico piers + shallow canopy
for x in (-2.4,2.4):
    box((x,0.55,0.9),(0.7,1.0,3.6),'Limestone',Ff)
boxr(-3.2,3.2,0.2,1.2,4.5,4.85,'Limestone',Ff)
boxr(-3.5,3.5,0.15,1.35,4.85,5.15,'LimeDark',Ff)
# pointed niche above door
gothwin(Ff,0,5.2,2.2,3.6,'Limestone',k=10)
# centre back
for x in [-7.2,-3.6,-0.0,3.6,7.2]:
    bay(Fb,x)
# end pavilion fronts
for F in (Fwf,Fef):
    for x in (-5.0,-1.7,1.7,5.0):
        bay(F,x,tall_base=True)
for F in (Fwb,Feb):
    for x in (-5.0,-1.7,1.7,5.0):
        bay(F,x)
# connector fronts (shallower)
for F in (Fcfw,Fcfe,Fcbw,Fcbe):
    for x in (-5.5,-1.8,1.8,5.5):
        bay(F,x)
# end walls
for F in (Fw,Fe):
    for x in (-10.5,-6.5,-2.2,2.2,6.5,10.5):
        bay(F,x)
# side returns of centre pavilion (east/west faces of centre block)
Fce=frame((CP[1],(CP[2]+CP[3])/2,0),-pi/2)
Fcw=frame((CP[0],(CP[2]+CP[3])/2,0),pi/2)
for F in (Fce,Fcw):
    for x in (-12.0,-7.0,-2.0,2.0,7.0,12.0):
        bay(F,x)
# pavilion side returns toward connectors (visible steps)
for (xwall,y0,y1,ang) in ((WP[1],WP[2],WP[3],-pi/2),(EP[0],EP[2],EP[3],pi/2)):
    F=frame((xwall,(y0+y1)/2,0),ang)
    for x in (-10.0,-5.0,0.0,5.0,10.0):
        bay(F,x)
# lamps at main entrance
for sx in (-1,1):
    x=sx*4.2; y=CP[2]-2.4
    lathe((x,y,0),[(0.32,0),(0.32,0.35),(0.2,0.55),(0.16,0.95),(0.08,1.25),(0.07,2.5),(0.22,2.65),(0.26,2.8),(0.06,2.9)],12,'Bronze')
    lathe((x,y,2.9),[(0.18,0),(0.22,0.2),(0.18,0.45)],10,'Gls')
    cyl((x,y,2.85),0.035,0.55,8,'Bronze')
    lathe((x,y,3.35),[(0.26,0),(0.05,0.28)],10,'Bronze')
# ---- site: paving + flat lawn (College Green) ----
boxr(-LOTX,LOTX,-LOTY,LOTY,-0.05,0.0,'Paving')
# front lawn toward College Green
boxr(-36,36,-27.5,-20.2,0,0.06,'Granite')
boxr(-35.7,35.7,-27.2,-20.5,0.0,0.08,'Lawn')
# side lawns
boxr(-43.5,-40.5,-16,12,0,0.06,'Granite'); boxr(-43.3,-40.7,-15.8,11.8,0.0,0.08,'Lawn')
boxr(40.5,43.5,-16,12,0,0.06,'Granite'); boxr(40.7,43.3,-15.8,11.8,0.0,0.08,'Lawn')
# rear strip
boxr(-36,36,16.2,27.0,0,0.06,'Granite'); boxr(-35.7,35.7,16.5,26.7,0.0,0.08,'Lawn')
# walk to front door
boxr(-2.8,2.8,-20.0,-19.5,0.0,0.04,'Paving')
boxr(-2.5,2.5,-19.5,CP[2]-0.2,0.0,0.05,'Paving')
# mansard dormers (photo: gabled dormers with pointed windows)
for (F,xs,zc) in ((Ff,(-6,6),ZC),(Fb,(-6,0,6),ZC),(Fwf,(-3.5,3.5),ZC-0.6),(Fef,(-3.5,3.5),ZC-0.6),(Fwb,(-3.5,3.5),ZC-0.6),(Feb,(-3.5,3.5),ZC-0.6)):
    for x in xs: dormer(F,x,zc+0.78)
# coloured stone banding (red-brown sandstone), flush, in gaps between window rows
for B in BLOCKS:
    x0,x1,y0,y1=B
    for (za,zb) in ((11.55,11.8),):
        boxr(x0-0.02,x1+0.02,y0-0.02,y1+0.02,za,zb,'Carve')
# corner turrets with spires (outer pavilion corners + centre front)
def turret(cx,cy,z0,s=1.1,h=4.2,sp=5.5):
    boxr(cx-s,cx+s,cy-s,cy+s,z0,z0+h,'Brick'); boxr(cx-s-0.12,cx+s+0.12,cy-s-0.12,cy+s+0.12,z0+h,z0+h+0.3,'LimeDark')
    pyramid(cx,cy,z0+h+0.3,s+0.1,sp,'Carve'); cyl((cx,cy,z0+h+0.3+sp-0.4),0.06,1.6,6,'Iron')
for (cx,cy,zc) in ((WP[0],WP[2],ZC-0.6),(WP[0],WP[3],ZC-0.6),(EP[1],EP[2],ZC-0.6),(EP[1],EP[3],ZC-0.6),(CP[0],CP[2],ZC),(CP[1],CP[2],ZC)):
    turret(cx,cy,zc-0.4)
# central front spire tower over portico
boxr(-2.2,2.2,CP[2]-0.3,CP[2]+3.2,ZC-0.4,ZC+6.0,'Brick'); prism([(-2.6,ZC+6.0),(2.6,ZC+6.0),(0,ZC+8.6)],CP[2]-0.5,CP[2]+3.4,'Roof')
gothwin(Ff,0,ZC+0.9,1.4,3.6,'Limestone',k=6)
pyramid(0,CP[2]+1.45,ZC+8.2,1.0,6.5,'Carve')
finalize(D)
