D='/workspace/penn_campus/QuadHopkinson'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Hopkinson House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602406: PCA 16.6 x 16.3 m
from numpy import arange

ZE=jblock(-8.3,8.3,-8.15,8.15,4,chim=((6.1, 0.0),),win_front=[-6.3, -3.1, 0.1, 3.3],win_back=[-6.3, -3.1, 0.1, 3.3],win_side=[-5.65, -2.45, 0.75, 3.95],dorm_front=(-4.15, 4.15),dorm_back=(-4.15, 4.15),)
Fe=frame((0,-8.15,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-8.15-0.9-0.9*i,-8.15-0.0,0,0.6-0.2*i,'Granite')

paving(12,12)

finalize(D)
