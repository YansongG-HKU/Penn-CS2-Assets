D='/workspace/penn_campus/IrvineAuditorium'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
# Irvine Auditorium (Horace Trumbauer / Julian Abele, 1926-32; VSBA 1997-2000). OSM way 51469206: PCA 50.5 x 51.5 m.
# Red brick Gothic: octagonal auditorium tower, slate octagonal roof with tall spire, round stair turret, buttresses with
# white stone weatherings, lower slate-roofed wings. Interior tower ~120 ft (VSBA). Front (Spruce St / Penn Commons) = -Y. Lot 7x7.
LX,LY=28.0,28.0
def walls(x0,x1,y0,y1,ze):
    boxr(x0-0.2,x1+0.2,y0-0.2,y1+0.2,0,0.9,'Granite'); boxr(x0,x1,y0,y1,0,ze,'Brick')
    boxr(x0-0.05,x1+0.05,y0-0.05,y1+0.05,ze-0.5,ze,'LimeDark')
def hip(x0,x1,y0,y1,ze,h):
    o=0.4; v=[bm.verts.new(p) for p in [(x0-o,y0-o,ze),(x1+o,y0-o,ze),(x1+o,y1+o,ze),(x0-o,y1+o,ze),((x0+x1)/2,(y0+y1)/2,ze+h)]]
    n0=len(bm.faces)
    for f in [(0,1,4),(1,2,4),(2,3,4),(3,0,4),(3,2,1,0)]: bm.faces.new([v[i] for i in f])
    tag(n0,'Roof')
# lower podium + wings
walls(-25,25,-25,25,12.0); boxr(-25,25,-25,25,12.0,12.1,'Roof')
for (x0,x1,y0,y1) in ((-25,-13,-25,-13),(13,25,-25,-13),(-25,-13,13,25),(13,25,13,25)):
    hip(x0,x1,y0,y1,12.0,5.0)
# octagonal hall
RC=17.0; ap=RC*math.cos(pi/8); ZO=29.0
lathe((0,0,12.0),[(RC,0),(RC,ZO-12.0)],8,'Brick',rot=pi/8)
lathe((0,0,ZO-0.6),[(RC+0.35,0),(RC+0.35,0.6)],8,'LimeDark',rot=pi/8)
lathe((0,0,ZO),[(RC+0.6,0),(5.0,10.5),(1.6,11.5)],8,'Roof',rot=pi/8)
lathe((0,0,ZO+11.5),[(1.6,0),(1.6,2.2),(1.0,2.4),(0.12,16.0)],8,'Copper',rot=pi/8)
# buttresses at octagon corners with stone weatherings
for k in range(8):
    a=pi/8+k*pi/4; ca,sa=math.cos(a),math.sin(a)
    F=frame((RC*ca,RC*sa,0),a-pi/2)
    boxr(-0.8,0.8,-0.5,1.6,12.0,24.5,'Brick',F); boxr(-0.9,0.9,-0.5,1.75,24.5,25.0,'LimeDark',F)
    boxr(-0.6,0.6,-0.5,0.9,25.0,ZO-0.6,'Brick',F); boxr(-0.7,0.7,-0.5,1.05,ZO-0.9,ZO-0.6,'LimeDark',F)
    cyl((0,0.2,ZO),0.35,1.6,8,'Copper',F)
# octagon face windows (paired pointed) + gabled roof dormers on axes
for k in range(8):
    a=k*pi/4; F=frame((ap*math.cos(a),ap*math.sin(a),0),a-pi/2)
    for x in (-2.2,2.2): gothwin(F,x,19.5,1.8,5.6,'Limestone',k=6)
    if k%2==0:
        zb=ZO+1.2; boxr(-1.3,1.3,-2.2,0.4,zb,zb+2.8,'Brick',F); prism([(-1.55,zb+2.8),(1.55,zb+2.8),(0,zb+4.2)],-2.2,0.6,'Roof',F)
        window(F,0,zb+0.6,1.0,1.6,None,0.42,'LimeDark')
# round stair turret with conical slate roof
TX,TY=ap*math.cos(-pi/4)+1.6,ap*math.sin(-pi/4)-1.6
lathe((TX,TY,0),[(2.8,0),(2.8,33.0)],16,'Brick'); lathe((TX,TY,30.5),[(3.0,0),(3.0,0.6)],16,'LimeDark')
lathe((TX,TY,33.0),[(3.2,0),(0.1,6.0)],16,'Roof'); cyl((TX,TY,38.6),0.08,1.8,6,'Copper')
# podium facades
Ff=frame((0,-25,0),pi); Fb=frame((0,25,0),0); Fe=frame((25,0,0),-pi/2); Fw=frame((-25,0,0),pi/2)
for F in (Ff,Fb,Fe,Fw):
    for x in (-20,-16,16,20): window(F,x,1.8,1.4,2.2,None,0.1,'LimeDark'); window(F,x,6.0,1.4,2.4,None,0,'LimeDark'); window(F,x,9.3,1.2,1.6,None,0,'LimeDark')
    for x in (-8,-4,4,8): gothwin(F,x,4.5,1.6,5.0,'Limestone',k=6)
door(Ff,0,3.0,3.8,0.9,None,y=0.14); gothwin(Ff,0,6.0,2.6,4.6,'Limestone',k=6)
for x in (-11.5,11.5):
    for F in (Ff,Fb,Fe,Fw): boxr(x-0.7,x+0.7,0,1.3,0.9,10.5,'Brick',F); boxr(x-0.8,x+0.8,0,1.45,10.5,10.9,'LimeDark',F)
# site
boxr(-LX,LX,-LY,LY,-0.05,0,'Paving')
boxr(-27,-3.5,-27.5,-25.8,0,0.06,'Granite'); boxr(-26.8,-3.7,-27.3,-26.0,0,0.08,'Lawn')
boxr(3.5,27,-27.5,-25.8,0,0.06,'Granite'); boxr(3.7,26.8,-27.3,-26.0,0,0.08,'Lawn')
finalize(D)
