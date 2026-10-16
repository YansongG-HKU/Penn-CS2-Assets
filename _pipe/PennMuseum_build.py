D='/workspace/penn_campus/PennMuseum'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
# Penn Museum. OSM rel 5231601: PCA 164.9 x 114.0 m ~10128 m2. Brick Romanesque/Byzantine; white stone portal; rotunda.
# Simplified massing. Lot 21x15 (168x120). Front=-Y.
LX,LY=84.0,60.0
# main front wings
boxr(-70,70,-40,-10,0,0.8,'Granite'); boxr(-70,70,-40,-10,0.8,12.0,'Brick')
boxr(-70,70,-40,-10,11.2,12.0,'LimeDark')
# central pavilion
boxr(-14,14,-48,-10,0,16.0,'Brick')
prism([(-14.5,16.0),(14.5,16.0),(0,24.0)],-48.2,-10,'Brick')
prism([(-15,16.0),(15,16.0),(0,24.5)],-48.5,-45.5,'Roof')
# white stone portal
Ff=frame((0,-48,0),pi)
boxr(-6,6,0,1.2,2.0,10.5,'Limestone',Ff)
door(Ff,0,3.2,4.0,2.2,None,y=0.2)
box((0,0.5,10.5),(4.5,0.8,3.5),'Limestone',Ff)  # relief panel
# stairs
for i in range(8): boxr(-10+0.4*i,10-0.4*i,-55+0.7*i,-48,0,0.22*(i+1),'Brick')
# arched upper windows on wings
for x in list(np.arange(-60,61,6.0)):
    if abs(x)<16: continue
    window(frame((0,-40,0),pi),x,2.0,2.4,2.6,None,0.1,'LimeDark')
    archwin(frame((0,-40,0),pi),x,7.0,2.8,3.8,'Limestone',k=8)
# rear rotunda
lathe((0,25,0),[(28,0),(28,18)],32,'Brick')
lathe((0,25,18),[(28.4,0),(28.4,0.5)],32,'LimeDark')
lathe((0,25,18.5),[(28.8,0),(8,12),(0.5,12.5)],32,'Roof')
# connector
boxr(-40,40,-10,25,0,14.0,'Brick')
boxr(-LX,LX,-LY,LY,-0.05,0,'Paving')
boxr(-65,65,-58,-49,0,0.06,'Granite'); boxr(-64.5,64.5,-57.5,-49.5,0,0.08,'Lawn')
# reflection pool as flat paving (no water mesh needed — dark paving)
boxr(-12,12,-58,-52,-0.02,0.02,'Granite')
finalize(D)
