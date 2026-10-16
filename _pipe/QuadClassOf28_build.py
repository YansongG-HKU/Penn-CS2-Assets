D='/workspace/penn_campus/QuadClassOf28'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# ClassOf28 House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602396: PCA 21.4 x 16.2 m
from numpy import arange

ZE=jblock(-10.7,10.7,-8.1,8.1,4,chim=((-8.2, 0.0), (8.2, 0.0)),win_front=[-8.7, -5.5, -2.3, 0.9, 4.1, 7.3],win_back=[-8.7, -5.5, -2.3, 0.9, 4.1, 7.3],win_side=[-5.6, -2.4, 0.8, 4.0],dorm_front=(-5.35, 5.35),dorm_back=(-5.35, 5.35),)
Fe=frame((0,-8.1,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-8.1-0.9-0.9*i,-8.1-0.0,0,0.6-0.2*i,'Granite')

paving(12,12)

finalize(D)
