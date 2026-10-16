D='/workspace/penn_campus/QuadBaldwinW'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# BaldwinW House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602390: PCA 16.9 x 16.9 m
from numpy import arange

ZE=jblock(-8.45,8.45,-8.45,8.45,4,chim=((6.25, 0.0),),win_front=[-6.45, -3.25, -0.05, 3.15, 6.35],win_back=[-6.45, -3.25, -0.05, 3.15, 6.35],win_side=[-5.95, -2.75, 0.45, 3.65],dorm_front=(-4.22, 4.22),dorm_back=(-4.22, 4.22),)
Fe=frame((0,-8.45,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-8.45-0.9-0.9*i,-8.45-0.0,0,0.6-0.2*i,'Granite')

paving(12,12)

finalize(D)
