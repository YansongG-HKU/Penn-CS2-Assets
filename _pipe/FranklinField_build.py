D='/workspace/penn_campus/FranklinField'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
# Franklin Field. OSM way 665447049: PCA 219.7 x 149.9 m ~27635 m2. Classic U-shaped brick stadium bowl + upper deck.
# Exterior shell only; flat field paving (no turf 3D). Lot 28x19 (224x152). Front (open south end) = -Y.
LX,LY=112.0,76.0
# field plane
boxr(-55,55,-60,60,-0.02,0.0,'Paving')
# lower bowl: three sides (U open to -Y)
def stand(x0,x1,y0,y1,z0,z1):
    boxr(x0,x1,y0,y1,z0,z1,'Brick')
    boxr(x0-0.05,x1+0.05,y0-0.05,y1+0.05,z1-0.6,z1,'LimeDark')
# west / east / north stands
stand(-100,-58,-55,55,0,12); stand(58,100,-55,55,0,12); stand(-100,100,55,72,0,14)
# upper deck setback
stand(-98,-62,-50,50,12,22); stand(62,98,-50,50,12,22); stand(-98,98,58,70,14,24)
# arched exterior colonnade on long sides (street face)
for F,xs in ((frame((-100,0,0),pi/2),np.arange(-45,46,8)),(frame((100,0,0),-pi/2),np.arange(-45,46,8)),(frame((0,72,0),0),np.arange(-85,86,8))):
    for x in xs:
        archwin(F,x,1.5,5.5,7.5,'Limestone',k=8)
        window(F,x,12.5,3.5,4.0,None,0.1,'LimeDark')
# scoreboard mass at open end (south)
boxr(-18,18,-70,-58,0,18,'Brick'); boxr(-16,16,-69,-59,10,16,'Iron')
boxr(-LX,LX,-LY,LY,-0.05,0,'Paving')
# plaza strips
boxr(-105,105,-74,-70,0,0.05,'Granite')
finalize(D)
