D='/workspace/penn_campus/QuadLippincott'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Lippincott House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602408: PCA 17.1 x 16.1 m
from numpy import arange

ZE=jblock(-8.55,8.55,-8.05,8.05,4,chim=((6.35, 0.0),),win_front=[-6.55, -3.35, -0.15, 3.05, 6.25],win_back=[-6.55, -3.35, -0.15, 3.05, 6.25],win_side=[-5.55, -2.35, 0.85, 4.05],dorm_front=(-4.28, 4.28),dorm_back=(-4.28, 4.28),)
Fe=frame((0,-8.05,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-8.05-0.9-0.9*i,-8.05-0.0,0,0.6-0.2*i,'Granite')

paving(12,12)

finalize(D)
