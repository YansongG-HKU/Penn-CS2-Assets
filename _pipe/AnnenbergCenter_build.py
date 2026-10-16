D='/workspace/penn_campus/AnnenbergCenter'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
# Annenberg Center for the Performing Arts (Vincent G. Kling & Associates, 1971). OSM way 32120984: PCA 79.8 x 69.2 m.
# Brown brick; tall hexagonal tower with glass curtain entrance under metal canopy; lower rectangular wings. Front = -Y.
# Lot 10x9 (80x72).
LX,LY=40.0,36.0
# lower wings
def wing(x0,x1,y0,y1,ze):
    boxr(x0-0.15,x1+0.15,y0-0.15,y1+0.15,0,0.7,'Granite')
    boxr(x0,x1,y0,y1,0,ze,'Brick')
    boxr(x0-0.04,x1+0.04,y0-0.04,y1+0.04,ze-0.4,ze,'LimeDark')
    boxr(x0+0.3,x1-0.3,y0+0.3,y1-0.3,ze,ze+0.35,'Roof')
wing(-38,-8,-30,28,14.0)
wing(8,38,-30,28,14.0)
wing(-8,8,8,32,12.0)   # rear connector
# hexagonal tower (pointy-top hex ≈ regular)
R=11.5; ZH=28.0
lathe((0,-2,0),[(R,0),(R,ZH)],6,'Brick',rot=pi/6)
lathe((0,-2,ZH-0.5),[(R+0.25,0),(R+0.25,0.5)],6,'LimeDark',rot=pi/6)
lathe((0,-2,ZH),[(R+0.4,0),(R*0.55,3.2)],6,'Roof',rot=pi/6)
# entrance glass curtain under metal canopy (front of tower)
Ff=frame((0,-2-R*math.cos(pi/6),0),pi)
for x in (-4,-2,0,2,4):
    window(Ff,x,0.8,1.6,6.5,None,0.1,'LimeDark')
door(Ff,0,2.4,3.2,0.6,None,y=0.15)
# metal canopy
boxr(-7,7,-0.2,3.5,8.5,9.0,'Iron',Ff)
boxr(-7.2,7.2,-0.3,3.7,9.0,9.2,'Copper',Ff)
# tower face windows
for k in range(6):
    a=pi/6+k*pi/3; F=frame((R*0.92*math.cos(a),-2+R*0.92*math.sin(a),0),a-pi/2)
    for z in (4,9,14,19,23.5):
        window(F,0,z,2.2,2.8 if z<20 else 2.2,None,0.1,'LimeDark')
# wing fenestration
for (xc,y0) in ((-23,-30),(23,-30)):
    F=frame((xc,y0,0),pi)
    for x in np.arange(-12,13,3.5):
        for z in (1.5,5.5,9.5): window(F,x,z,2.2,2.6,None,0.1,'LimeDark')
for (xc,y1) in ((-23,28),(23,28)):
    F=frame((xc,y1,0),0)
    for x in np.arange(-12,13,3.5):
        for z in (1.5,5.5,9.5): window(F,x,z,2.2,2.6,None,0.1,'LimeDark')
for (xw,ang) in ((-38,pi/2),(38,-pi/2)):
    F=frame((xw,0,0),ang)
    for x in np.arange(-22,23,3.5):
        for z in (1.5,5.5,9.5): window(F,x,z,2.0,2.6,None,0.1,'LimeDark')
# plaza
boxr(-LX,LX,-LY,LY,-0.05,0,'Paving')
boxr(-36,-10,-35,-31,0,0.06,'Granite'); boxr(-35.7,-10.3,-34.7,-31.3,0,0.08,'Lawn')
boxr(10,36,-35,-31,0,0.06,'Granite'); boxr(10.3,35.7,-34.7,-31.3,0,0.08,'Lawn')
finalize(D)
