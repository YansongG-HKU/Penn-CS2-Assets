D='/workspace/penn_campus/FisherFineArts'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
# Fisher Fine Arts Library (Frank Furness, 1888-91). NRHP 72001154: original plan ~140x80 ft (42.7x24.4 m),
# apse radius 38.7 ft (11.8 m), stair tower ~95 ft. Red sandstone base, red brick + terracotta. Front (34th St/College Green side) = -Y.
LX,LY=32.0,24.0
def wallblock(x0,x1,y0,y1,zt,zbase=4.0):
    boxr(x0-0.15,x1+0.15,y0-0.15,y1+0.15,0,zbase,'Limestone')
    boxr(x0-0.28,x1+0.28,y0-0.28,y1+0.28,0,0.8,'Granite')
    boxr(x0,x1,y0,y1,zbase,zt,'Brick')
    for (z0,z1) in ((zbase,zbase+0.4),(zt-0.9,zt)): boxr(x0-0.04,x1+0.04,y0-0.04,y1+0.04,z0,z1,'LimeDark')
def gable(x0,x1,y0,y1,ze,h,axis='Y'):
    if axis=='Y':
        xc=(x0+x1)/2; prism([(x0-0.4,ze),(x1+0.4,ze),(xc,ze+h)],y0-0.4,y1+0.4,'Roof')
    else:
        yc=(y0+y1)/2; prism([(y0-0.4,ze),(y1+0.4,ze),(yc,ze+h)],-(x1+0.4),-(x0-0.4),'Roof',Matrix.Rotation(pi/2,4,'Z'))
# main reading-room hall
wallblock(-14,8,-6,10,18.0); gable(-14,8,-6,10,18.0,7.0,'X')
# stacks wing (east)
wallblock(8,27,-2,12,13.0); gable(8,27,-2,12,13.0,4.0,'X')
# stair tower
TX0,TX1,TY0,TY1=6.0,14.0,-12.0,-4.0; ZT=33.0
wallblock(TX0,TX1,TY0,TY1,ZT,6.0)
boxr(TX0-0.3,TX1+0.3,TY0-0.3,TY1+0.3,ZT,ZT+0.6,'LimeDark')
for i in range(5):
    for (xa,ya,xb,yb) in ((TX0-0.3,TY0-0.3,TX1+0.3,TY0+0.4),(TX0-0.3,TY1-0.4,TX1+0.3,TY1+0.3)):
        x=xa+0.4+i*(xb-xa-0.8)/4; boxr(x-0.45,x+0.45,ya,yb,ZT+0.6,ZT+2.0,'LimeDark')
    for (xa,xb) in ((TX0-0.3,TX0+0.4),(TX1-0.4,TX1+0.3)):
        y=TY0+0.6+i*(TY1-TY0-1.2)/4; boxr(xa,xb,y-0.45,y+0.45,ZT+0.6,ZT+2.0,'LimeDark')
boxr(TX0+0.6,TX0+2.4,TY0+0.6,TY0+2.4,ZT,ZT+4.5,'Brick'); boxr(TX0+0.4,TX0+2.6,TY0+0.4,TY0+2.6,ZT+4.5,ZT+5.0,'LimeDark')
# rotunda (apse) to the west: rusticated drum + brick upper drum + conical roof
CX,CY=-14.0,2.0; R=11.8
lathe((CX,CY,0),[(R+1.6,0),(R+1.6,6.5)],40,'Limestone'); lathe((CX,CY,6.5),[(R+1.9,0),(R+1.9,0.45)],40,'Copper')
lathe((CX,CY,0),[(R,0),(R,17.0)],40,'Brick'); lathe((CX,CY,10.5),[(R+0.05,0),(R+0.05,0.4)],40,'LimeDark')
lathe((CX,CY,17.0),[(R+0.4,0),(R+0.4,0.5)],40,'LimeDark')
lathe((CX,CY,17.5),[(R+0.5,0),(0.6,7.5),(0.0,7.6)],40,'Roof')
# entrance porch (arched, gabled) east of tower
PX0,PX1,PY0,PY1=15.0,24.0,-11.0,-2.0
wallblock(PX0,PX1,PY0,PY1,9.0,3.0); prism([(PX0-0.4,9.0),(PX1+0.4,9.0),((PX0+PX1)/2,13.5)],PY0-0.4,PY0+3.0,'Roof',frame((0,0,0),0))
Fp=frame(((PX0+PX1)/2,PY0,0),pi)
prism([(-4.9,9.0),(4.9,9.0),(0,13.5)],-0.01,0.25,'Brick',Fp)
archwin(Fp,0,0.6,4.6,6.8,'Limestone',k=14)
# facades
Ff=frame((-3,-6,0),pi); Fb=frame((-3,10,0),0); Fs=frame((17.5,-2,0),pi); Fsb=frame((17.5,12,0),0); Fse=frame((27,5,0),-pi/2)
for x in (-8.5,-5,-1.5,2,5.5):
    window(Ff,x,1.2,1.2,2.0,None,0.15,'LimeDark'); archwin(Ff,x,5.5,2.0,7.5,'Limestone',k=10); window(Ff,x,14.0,1.4,2.2,None,0,'LimeDark')
for x in (-8.5,-5,-1.5,2,5.5):
    window(Fb,x,1.2,1.2,2.0,None,0.15,'LimeDark'); archwin(Fb,x,5.5,2.0,7.5,'Limestone',k=10)
for F in (Fs,Fsb):
    for x in (-6,-2,2,6): window(F,x,1.2,1.2,2.0,None,0.15,'LimeDark'); window(F,x,5.0,1.6,2.6,None,0,'LimeDark'); window(F,x,9.0,1.6,2.4,None,0,'LimeDark')
for x in (-4.5,0,4.5): window(Fse,x,5.0,1.6,2.6,None,0,'LimeDark'); window(Fse,x,9.0,1.6,2.4,None,0,'LimeDark')
Ftf=frame(((TX0+TX1)/2,TY0,0),pi); Fte=frame((TX1,(TY0+TY1)/2,0),-pi/2); Ftw=frame((TX0,(TY0+TY1)/2,0),pi/2)
for F in (Ftf,Fte,Ftw):
    window(F,0,7.5,1.3,2.2,None,0,'LimeDark'); window(F,0,12.5,1.3,2.2,None,0,'LimeDark'); archwin(F,0,18.5,1.6,3.6,'Limestone',k=8); window(F,-1.6,26.5,0.9,1.6,None,0,'LimeDark'); window(F,1.6,26.5,0.9,1.6,None,0,'LimeDark')
# rotunda windows: arched upper ring + small base windows (west half only)
for a in np.linspace(pi*0.55,pi*1.45,7):
    F=frame((CX+(R+0.05)*math.cos(a),CY+(R+0.05)*math.sin(a),0),a-pi/2); archwin(F,0,11.6,1.8,3.0,'Limestone',k=8)
    F2=frame((CX+(R+1.65)*math.cos(a),CY+(R+1.65)*math.sin(a),0),a-pi/2); window(F2,0,1.4,1.2,1.6,None,0,'LimeDark')
# rotunda gabled dormers + finials (photo), terracotta frieze band
for a in np.linspace(pi*0.6,pi*1.4,5):
    F=frame((CX+(R-0.6)*math.cos(a),CY+(R-0.6)*math.sin(a),0),a-pi/2)
    boxr(-1.6,1.6,-1.5,0.9,16.8,20.0,'Brick',F); prism([(-1.9,20.0),(1.9,20.0),(0,22.4)],-1.7,1.1,'Brick',F)
    prism([(-2.05,19.9),(2.05,19.9),(0,22.6)],0.9,1.15,'LimeDark',F)
    gothwin(F,0,17.5,1.1,2.0,'Limestone',k=5,frm='Iron')
    cyl((0,1.0,22.45),0.18,1.0,8,'Copper',F); cyl((0,1.0,23.4),0.07,0.7,6,'Copper',F)
lathe((CX,CY,15.6),[(R+0.08,0),(R+0.08,0.35)],40,'Carve')
boxr(-14.05,8.05,-6.05,10.05,16.3,16.6,'Carve')
for (x,y) in ((-14,-6),(8,-6),(-14,10),(8,10)): cyl((x,y,18.0),0.3,2.2,8,'LimeDark'); cyl((x,y,20.2),0.12,0.8,6,'Copper')
# site: brick paving plaza + flat lawn
boxr(-LX,LX,-LY,LY,-0.05,0.0,'Paving')
boxr(-30,-4,-22.5,-16,0,0.06,'Granite'); boxr(-29.8,-4.2,-22.3,-16.2,0,0.08,'Lawn')
boxr(28,31.5,-20,20,0,0.06,'Granite'); boxr(28.2,31.3,-19.8,19.8,0,0.08,'Lawn')
finalize(D)
