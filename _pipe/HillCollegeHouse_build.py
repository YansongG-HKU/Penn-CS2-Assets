D='/workspace/penn_campus/HillCollegeHouse'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
# Hill College House (Eero Saarinen, 1958-60). OSM rel 5235124: PCA 78.9 x 45.7 m ~3457 m2.
# Fortress dark brick, 6 floors, atrium court, recessed windows, entry bridge over dry moat (flat paving). Front=-Y. Lot 10x6.
LX,LY=40.0,24.0; XW,YF,YB=36.0,-18.0,18.0; T=8.5
ZB=3.6; ZTOP=22.5
boxr(-XW,XW,YF,YB,0,0.4,'Granite'); boxr(-XW,XW,YF,YB,0.4,ZB,'Brick')
boxr(-XW,XW,YF,YF+T,ZB,ZTOP,'Brick'); boxr(-XW,XW,YB-T,YB,ZB,ZTOP,'Brick')
boxr(-XW,-XW+T,YF+T,YB-T,ZB,ZTOP,'Brick'); boxr(XW-T,XW,YF+T,YB-T,ZB,ZTOP,'Brick')
for (x0,x1,y0,y1) in ((-XW,XW,YF,YF+T),(-XW,XW,YB-T,YB),(-XW,-XW+T,YF+T,YB-T),(XW-T,XW,YF+T,YB-T)):
    boxr(x0,x1,y0,y1,ZTOP,ZTOP+0.45,'Roof')
DROPF[0]=True
for x in np.arange(-XW+1,XW,3.5):
    for y in (YF+0.35,YB-0.35): box((x,y,ZTOP+0.45),(0.12,0.12,1.0),'Iron')
for y in np.arange(YF+2,YB-1,3.5):
    for x in (-XW+0.35,XW-0.35): box((x,y,ZTOP+0.45),(0.12,0.12,1.0),'Iron')
DROPF[0]=False
boxr(-LX,LX,-LY,LY,-0.05,0,'Paving')
boxr(-XW-3.2,XW+3.2,YF-5.2,YF-0.2,-0.3,0.0,'Paving')  # moat
boxr(-3.5,3.5,YF-5.2,YF+0.4,0.0,0.35,'Granite'); boxr(-3.2,3.2,YF-5.0,YF+0.2,0.35,0.5,'LimeDark')
for x in (-3.25,3.25): boxr(x-0.07,x+0.07,YF-5.0,YF,0.5,1.35,'Iron')
Ff=frame((0,YF,0),pi); Fb=frame((0,YB,0),0)
door(Ff,0,2.8,3.4,ZB+0.15,None,y=0.15)
for x in (-6.2,-5.2,5.2,6.2): box((x,0.2,ZB+0.8),(0.35,0.45,ZTOP-ZB-1.2),'Iron',Ff)
UP=[(ZB+1.0,1.5,2.2),(ZB+4.6,1.7,2.3),(ZB+8.4,1.4,2.2),(ZB+12.0,2.0,1.6),(ZB+15.5,1.3,2.3)]
def punch(F,xs):
    for x in xs:
        for z,w,h in UP: window(F,x,z,w,h,None,0.32,'LimeDark')
punch(Ff,[x for x in np.arange(-30,31,4.2) if abs(x)>8])
punch(Fb,[x for x in np.arange(-30,31,4.2) if abs(x)>8])
for F in (frame((-XW,(YF+YB)/2,0),pi/2),frame((XW,(YF+YB)/2,0),-pi/2)):
    punch(F,list(np.arange(-12,13,4.0)))
for F in (frame((0,YF+T,0),0),frame((0,YB-T,0),pi)):
    punch(F,list(np.arange(-18,19,4.5)))
boxr(-38,38,-23.5,-19.8,0,0.06,'Granite'); boxr(-37.7,37.7,-23.2,-20.1,0,0.08,'Lawn')
boxr(-38,38,19.8,23.5,0,0.06,'Granite'); boxr(-37.7,37.7,20.1,23.2,0,0.08,'Lawn')
finalize(D)
