D='/workspace/penn_campus/VanPeltLibrary'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
# Van Pelt–Dietrich Library Center (Harbeson, Hough, Livingston & Larson, 1962). OSM way 32120084: PCA 140.7 x 46.7 m.
# Mid-century: brown brick panels between white concrete fins; recessed glazed ground + attic; 10 floors (Penn Facilities),
# photo shows ~5 major storeys. Front (College Green / Locust Walk side) = -Y. Lot 18x6 (144x48).
LX,LY=72.0,24.0
XW,YD,YF=68.0,18.0,-16.0  # main block half-width, back, front
ZB=4.8; ZC=22.0; ZA=26.5; ZTOP=28.0
# plinth / recessed ground glass level
boxr(-XW-0.2,XW+0.2,YF-0.2,YD+0.2,0,0.6,'Granite')
boxr(-XW+1.5,XW-1.5,YF+1.2,YD-1.2,0.6,ZB,'Brick')  # inset brick core
# colonnade of concrete fins (LimeDark) on long facades
FIN=3.3; fins=list(np.arange(-XW+1.0,XW-0.5,FIN))
for x in fins:
    boxr(x-0.35,x+0.35,YF-0.35,YF+0.55,ZB,ZC,'LimeDark')
    boxr(x-0.35,x+0.35,YD-0.55,YD+0.35,ZB,ZC,'LimeDark')
# brick panels between fins
for i in range(len(fins)-1):
    x0,x1=fins[i]+0.35,fins[i+1]-0.35
    if x1-x0<0.5: continue
    boxr(x0,x1,YF,YF+0.4,ZB,ZC,'Brick')
    boxr(x0,x1,YD-0.4,YD,ZB,ZC,'Brick')
# short ends
boxr(-XW, -XW+0.5,YF,YD,ZB,ZC,'Brick'); boxr(XW-0.5,XW,YF,YD,ZB,ZC,'Brick')
for y in np.arange(YF+2,YD-1,3.2):
    boxr(-XW-0.3,-XW+0.55,y-0.3,y+0.3,ZB,ZC,'LimeDark')
    boxr(XW-0.55,XW+0.3,y-0.3,y+0.3,ZB,ZC,'LimeDark')
# recessed attic glazed band
boxr(-XW+1.2,XW-1.2,YF+1.0,YD-1.0,ZC,ZA,'Brick')
boxr(-XW+0.8,XW-0.8,YF+0.6,YD-0.6,ZA,ZTOP,'LimeDark')
# flat roof
boxr(-XW+1.0,XW-1.0,YF+1.0,YD-1.0,ZTOP,ZTOP+0.4,'Roof')
# ground and attic ribbon windows + mid-floor punched windows
Ff=frame((0,YF,0),pi); Fb=frame((0,YD,0),0); Fe=frame((XW,(YF+YD)/2,0),-pi/2); Fw=frame((-XW,(YF+YD)/2,0),pi/2)
for F,xs in ((Ff,fins),(Fb,fins)):
    for x in xs:
        if abs(x)>XW-2: continue
        # three punched windows per bay mid-floors
        for zi,zh in ((ZB+1.2,2.8),(ZB+6.5,2.8),(ZB+11.8,2.8)):
            for dx in (-0.85,0.85):
                window(F,x+dx,zi,0.7,zh,None,0.15,'LimeDark')
        # attic ribbon
        window(F,x,ZC+0.6,2.4,2.8,None,0.15,'LimeDark')
        # ground ribbon
        window(F,x,1.2,2.4,2.8,None,0.15,'LimeDark')
for F in (Fe,Fw):
    for x in np.arange(-12,13,3.2):
        for zi,zh in ((ZB+1.2,2.8),(ZB+6.5,2.8),(ZB+11.8,2.8)):
            window(F,x,zi,1.4,zh,None,0.15,'LimeDark')
        window(F,x,ZC+0.6,1.8,2.8,None,0.15,'LimeDark'); window(F,x,1.2,1.8,2.8,None,0.15,'LimeDark')
# main entrance recess centre front
boxr(-6,6,YF-2.5,YF+0.2,0,ZB+0.2,'Granite')
door(Ff,0,3.2,3.2,0.8,None,y=0.2)
for x in (-3.5,3.5): window(Ff,x,1.0,2.0,2.8,None,0.2,'LimeDark')
# site lawn / paving
boxr(-LX,LX,-LY,LY,-0.05,0,'Paving')
boxr(-60,60,-23,-17.5,0,0.06,'Granite'); boxr(-59.5,59.5,-22.7,-17.8,0,0.08,'Lawn')
boxr(-60,60,19,23.5,0,0.06,'Granite'); boxr(-59.5,59.5,19.3,23.2,0,0.08,'Lawn')
finalize(D)
