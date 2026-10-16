D='/workspace/penn_campus/QuadWilson'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Wilson House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602410: PCA 18.6 x 14.7 m
from numpy import arange

ZE=jblock(-9.3,9.3,-7.35,7.35,4,chim=((7.1, 0.0),),win_front=[-7.3, -4.1, -0.9, 2.3, 5.5],win_back=[-7.3, -4.1, -0.9, 2.3, 5.5],win_side=[-4.85, -1.65, 1.55, 4.75],dorm_front=(-4.65, 4.65),dorm_back=(-4.65, 4.65),)
Fe=frame((0,-7.35,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-7.35-0.9-0.9*i,-7.35-0.0,0,0.6-0.2*i,'Granite')

paving(12,12)

finalize(D)
