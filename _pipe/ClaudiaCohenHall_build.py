D='/workspace/penn_campus/ClaudiaCohenHall'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
# Claudia Cohen Hall (ex-Logan Hall; Thomas W. Richards 1874; VSBA renovation). OSM way 51367397: PCA 49.5 x 34.7 m.
# Collegiate / Victorian Gothic brick with stone trim; Perelman Quad. Front=-Y. Lot 7x5 (56x40).
LX,LY=28.0,20.0; XW,YF,YB=22.0,-14.0,14.0
ZB=4.0; ZC=16.5; ZTOP=22.0
boxr(-XW-0.2,XW+0.2,YF-0.2,YB+0.2,0,0.7,'Granite')
boxr(-XW,XW,YF,YB,0,ZB,'Rustic'); boxr(-XW,XW,YF,YB,ZB,ZC,'Brick')
for (a,b) in ((ZB,ZB+0.4),(ZC-0.9,ZC)): boxr(-XW-0.04,XW+0.04,YF-0.04,YB+0.04,a,b,'LimeDark')
# centre pavilion projection
boxr(-7,7,YF-3.5,YF+0.2,0,ZC,'Brick'); boxr(-7.05,7.05,YF-3.55,YF+0.25,ZC-0.9,ZC,'LimeDark')
# gables on ends + centre
def groof(x0,x1,y0,y1,ze,h,axis='Y'):
    if axis=='Y':
        xc=(x0+x1)/2; prism([(x0-0.3,ze),(x1+0.3,ze),(xc,ze+h)],y0-0.2,y1+0.2,'Roof')
    else:
        yc=(y0+y1)/2; prism([(y0-0.3,ze),(y1+0.3,ze),(yc,ze+h)],-(x1+0.2),-(x0-0.2),'Roof',Matrix.Rotation(pi/2,4,'Z'))
groof(-XW,XW,YF,YB,ZC,5.5,'X')
groof(-7,7,YF-3.5,YF+1,ZC,6.5,'Y')
Ff=frame((0,YF-3.5,0),pi); Fb=frame((0,YB,0),0); Fm=frame((0,YF,0),pi)
door(Ff,0,2.4,3.2,0.9,None,y=0.12)
UP=[(ZB+0.8,1.5,2.4),(ZB+4.5,1.5,2.4),(ZB+8.2,1.4,2.2),(ZB+11.8,1.3,2.0)]
for x in (-16,-11,-5.5,5.5,11,16):
    for z,w,h in UP: window(Fm,x,z,w,h,None,0,'LimeDark')
for x in (-4.5,-1.5,1.5,4.5):
    for z,w,h in UP: window(Ff,x,z,w,h,None,0,'LimeDark')
for x in (-16,-11,-5.5,0,5.5,11,16):
    for z,w,h in UP: window(Fb,x,z,w,h,None,0,'LimeDark')
for F in (frame((-XW,(YF+YB)/2,0),pi/2),frame((XW,(YF+YB)/2,0),-pi/2)):
    for x in (-8,-4,0,4,8):
        for z,w,h in UP: window(F,x,z,w,h,None,0,'LimeDark')
boxr(-LX,LX,-LY,LY,-0.05,0,'Paving')
boxr(-24,24,-19,-14.5,0,0.06,'Granite'); boxr(-23.7,23.7,-18.7,-14.8,0,0.08,'Lawn')
finalize(D)
