D='/workspace/penn_campus/QuadButcher'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Butcher House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602398: PCA 35.5 x 14.2 m
from numpy import arange

ZE=jblock(-17.75,17.75,-7.1,7.1,4,chim=((-15.25, 0.0), (15.25, 0.0)),win_front=[-15.75, -12.55, -9.35, -6.15, -2.95, 0.25, 3.45, 6.65, 9.85, 13.05],win_back=[-15.75, -12.55, -9.35, -6.15, -2.95, 0.25, 3.45, 6.65, 9.85, 13.05],win_side=[-4.6, -1.4, 1.8],dorm_front=(-13.31, -4.44, 4.44, 13.31),dorm_back=(-13.31, -4.44, 4.44, 13.31),)
Fe=frame((0,-7.1,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-7.1-0.9-0.9*i,-7.1-0.0,0,0.6-0.2*i,'Granite')

paving(20,12)

finalize(D)
