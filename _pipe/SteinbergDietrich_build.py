D='/workspace/penn_campus/SteinbergDietrich'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
# Steinberg-Dietrich Hall (Wharton). OSM way 51469702: PCA 127.4 x 78.5 m ~4980 m2. Modern brick/concrete academic.
# Lot 16x10 (128x80). Front (Locust Walk)=-Y.
LX,LY=64.0,40.0; XW,YF,YB=58.0,-32.0,32.0
ZB=4.2; ZC=18.0; ZTOP=22.0
boxr(-XW,XW,YF,YB,0,0.5,'Granite')
# E-shaped: main bar + three fingers south
boxr(-XW,XW,YF+12,YB,0,ZC,'Brick')
for (x0,x1) in ((-XW,-XW+28),(-14,14),(XW-28,XW)):
    boxr(x0,x1,YF,YF+14,0,ZC,'Brick')
for o in (0.04,):
    boxr(-XW-o,XW+o,YF+12-o,YB+o,ZB,ZB+0.35,'LimeDark')
    boxr(-XW-o,XW+o,YF+12-o,YB+o,ZC-0.7,ZC,'LimeDark')
boxr(-XW+1,XW-1,YF+13,YB-1,ZC,ZTOP,'Roof')
for (x0,x1) in ((-XW,-XW+28),(-14,14),(XW-28,XW)):
    boxr(x0+0.5,x1-0.5,YF+0.5,YF+13.5,ZC,ZTOP-1,'Roof')
Ff=frame((0,YF,0),pi); Fb=frame((0,YB,0),0)
# v2 (real photos Commons 'The Wharton School - UPenn 20240528'): dark brown brick, no white trim;
# 1983 Steinberg entry = chamfered brick bay with tall mullioned glazing, stone name panel, wide stairs; vertical window bands.
YP=YF-4.0
boxr(-7,7,YP,YF+1,0,ZC,'Brick')
for q in (-1,1): box((q*8.6,YF-1.6,0),(4.6,4.6,ZC),'Brick',rz=pi/4)
boxr(-7.2,7.2,YP-0.1,YF,ZC-0.6,ZC,'LimeDark')
Fp=frame((0,YP,0),pi)
window(Fp,0,6.6,8.0,8.0,None,0.1,'Brick')
box((0,0.12,4.6),(6.4,0.24,1.3),'Limestone',Fp)
door(Fp,0,5.0,3.0,1.0,None,y=0.1)
for i in range(5): boxr(-9-0.9*i,9+0.9*i,YP-1.0-0.9*i,YP,0,1.0-0.2*i,'Granite')
# side bays: tall vertical glazed slots
for q in (-1,1):
    for z in (2.0,8.0): window(frame((q*11.6,YF-1.6,0),pi+q*pi/4),0,z,1.4,5.0,None,0.1,'Brick')
# vertical window bands on wings (punched, brick sills)
for xc in (-44,44):
    F=frame((xc,YF,0),pi)
    for z in (1.2,5.5,9.5,13.5):
        for x in (-9,-6,-3,3,6,9): window(F,x,z,1.6,3.0,None,0.1,'Brick')
for x in np.arange(-50,51,4.5):
    if not (16<abs(x)<28): continue
    F=frame((x,YF+12,0),pi)
    for z in (5.5,9.5,13.5): window(F,0,z,1.6,3.0,None,0.1,'Brick')
for x in np.arange(-50,51,4.5):
    for z in (1.2,5.5,9.5,13.5): window(Fb,x,z,1.6,3.0,None,0.1,'Brick')
boxr(-LX,LX,-LY,LY,-0.05,0,'Paving')
boxr(-55,55,-38,-33,0,0.06,'Granite'); boxr(-54.5,54.5,-37.5,-33.5,0,0.08,'Lawn')
finalize(D)
