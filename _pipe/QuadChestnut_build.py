D='/workspace/penn_campus/QuadChestnut'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Chestnut House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602399: PCA 17.5 x 16.5 m
from numpy import arange

ZE=jblock(-8.75,8.75,-8.25,8.25,4,chim=((6.55, 0.0),),win_front=[-6.75, -3.55, -0.35, 2.85, 6.05],win_back=[-6.75, -3.55, -0.35, 2.85, 6.05],win_side=[-5.75, -2.55, 0.65, 3.85],dorm_front=(-4.38, 4.38),dorm_back=(-4.38, 4.38),)
Fe=frame((0,-8.25,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-8.25-0.9-0.9*i,-8.25-0.0,0,0.6-0.2*i,'Granite')

paving(12,12)

finalize(D)
