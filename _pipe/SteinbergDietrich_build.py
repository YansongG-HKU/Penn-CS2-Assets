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
# ribbon + punched windows
for xc in (-45,-30,0,30,45):
    F=frame((xc,YF,0),pi)
    for z in (1.2,5.5,9.5,13.5):
        for x in (-8,-4,0,4,8): window(F,x,z,2.2,2.6,None,0.1,'LimeDark')
for x in np.arange(-50,51,4.5):
    for z in (1.2,5.5,9.5,13.5): window(Fb,x,z,2.0,2.6,None,0.1,'LimeDark')
door(frame((0,YF,0),pi),0,3.0,3.2,0.8,None,y=0.15)
boxr(-LX,LX,-LY,LY,-0.05,0,'Paving')
boxr(-55,55,-38,-33,0,0.06,'Granite'); boxr(-54.5,54.5,-37.5,-33.5,0,0.08,'Lawn')
finalize(D)
