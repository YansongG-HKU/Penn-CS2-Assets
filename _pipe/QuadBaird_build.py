D='/workspace/penn_campus/QuadBaird'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Baird House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602404: PCA 16.7 x 16.4 m
from numpy import arange

ZE=jblock(-8.35,8.35,-8.2,8.2,4,chim=((6.15, 0.0),),win_front=[-6.35, -3.15, 0.05, 3.25],win_back=[-6.35, -3.15, 0.05, 3.25],win_side=[-5.7, -2.5, 0.7, 3.9],dorm_front=(-4.17, 4.17),dorm_back=(-4.17, 4.17),)
Fe=frame((0,-8.2,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-8.2-0.9-0.9*i,-8.2-0.0,0,0.6-0.2*i,'Granite')

paving(12,12)

finalize(D)
