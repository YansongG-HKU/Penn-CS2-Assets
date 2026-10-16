D='/workspace/penn_campus/QuadLeidy'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Leidy House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602394: PCA 23.4 x 15.7 m
from numpy import arange

ZE=jblock(-11.7,11.7,-7.85,7.85,4,chim=((-9.2, 0.0), (9.2, 0.0)),win_front=[-9.7, -6.5, -3.3, -0.1, 3.1, 6.3, 9.5],win_back=[-9.7, -6.5, -3.3, -0.1, 3.1, 6.3, 9.5],win_side=[-5.35, -2.15, 1.05, 4.25],dorm_front=(-5.85, 5.85),dorm_back=(-5.85, 5.85),)
Fe=frame((0,-7.85,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-7.85-0.9-0.9*i,-7.85-0.0,0,0.6-0.2*i,'Granite')

paving(16,12)

finalize(D)
