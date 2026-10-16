D='/workspace/penn_campus/WistarInstitute'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
# Wistar Institute. OSM way 32120133: PCA 130.5 x 62.0 m ~4288 m2.
# Historic orange brick wing + modern glass Fox Tower. Front (Spruce)=-Y. Lot 17x8 (136x64).
LX,LY=68.0,32.0
# historic block (east)
HX0,HX1,HY0,HY1=5,60,-22,22
ZB=3.5; ZC=18.0; ZTOP=20.5
boxr(HX0,HX1,HY0,HY1,0,0.9,'Granite'); boxr(HX0,HX1,HY0,HY1,0.9,ZB,'Rustic')
boxr(HX0,HX1,HY0,HY1,ZB,ZC,'Brick')
for (a,b) in ((ZB,ZB+0.4),(ZC-0.8,ZC)): boxr(HX0-0.04,HX1+0.04,HY0-0.04,HY1+0.04,a,b,'LimeDark')
boxr(HX0+0.5,HX1-0.5,HY0+0.5,HY1-0.5,ZC,ZTOP,'Roof')
# name band
boxr(HX0+8,HX1-8,HY0-0.15,HY0+0.25,ZB+3.8,ZB+4.6,'LimeDark')
# modern glass tower (west)
TX0,TX1=-60,-5
boxr(TX0,TX1,HY0+4,HY1-4,0,32.0,'LimeDark')  # pale frame
# glass curtain as Win grid
Ft=frame(((TX0+TX1)/2,HY0+4,0),pi)
for x in np.arange(-24,25,3.2):
    for z in np.arange(1.5,30,3.4): window(Ft,x,z,2.6,2.8,None,0.08,'LimeDark')
# canopy entrance to modern wing
boxr(-20,-8,HY0-3,HY0+4,8.5,9.2,'Iron')
door(Ft,0,3.0,3.5,0.6,None,y=0.12)
# historic fenestration
Fh=frame(((HX0+HX1)/2,HY0,0),pi); Fhb=frame(((HX0+HX1)/2,HY1,0),0)
for x in np.arange(-22,23,4.0):
    for z,h in ((1.4,2.4),(ZB+1.0,3.0),(ZB+5.5,3.0),(ZB+10.0,2.8),(ZB+14.0,2.4)):
        window(Fh,x,z,2.4,h,None,0.1,'LimeDark'); window(Fhb,x,z,2.4,h,None,0.1,'LimeDark')
boxr(-LX,LX,-LY,LY,-0.05,0,'Paving')
boxr(-60,60,-30,-23,0,0.06,'Granite'); boxr(-59.5,59.5,-29.5,-23.5,0,0.08,'Lawn')
finalize(D)
