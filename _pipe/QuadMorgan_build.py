D='/workspace/penn_campus/QuadMorgan'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Morgan House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602409: PCA 25.0 x 12.1 m
from numpy import arange

ZE=jblock(-12.5,12.5,-6.05,6.05,4,chim=((-10.0, 0.0), (10.0, 0.0)),win_front=[-10.5, -7.3, -4.1, -0.9, 2.3, 5.5, 8.7],win_back=[-10.5, -7.3, -4.1, -0.9, 2.3, 5.5, 8.7],win_side=[-3.55, -0.35, 2.85],dorm_front=(-6.25, 6.25),dorm_back=(-6.25, 6.25),)
Fe=frame((0,-6.05,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-6.05-0.9-0.9*i,-6.05-0.0,0,0.6-0.2*i,'Granite')

paving(16,12)

finalize(D)
