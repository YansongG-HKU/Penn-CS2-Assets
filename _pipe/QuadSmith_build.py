D='/workspace/penn_campus/QuadSmith'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Smith House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602407: PCA 16.6 x 15.9 m
from numpy import arange

ZE=jblock(-8.3,8.3,-7.95,7.95,4,chim=((6.1, 0.0),),win_front=[-6.3, -3.1, 0.1, 3.3],win_back=[-6.3, -3.1, 0.1, 3.3],win_side=[-5.45, -2.25, 0.95, 4.15],dorm_front=(-4.15, 4.15),dorm_back=(-4.15, 4.15),)
Fe=frame((0,-7.95,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-7.95-0.9-0.9*i,-7.95-0.0,0,0.6-0.2*i,'Granite')

paving(12,12)

finalize(D)
