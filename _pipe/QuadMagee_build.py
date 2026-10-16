D='/workspace/penn_campus/QuadMagee'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Magee House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602416: PCA 27.9 x 17.4 m
from numpy import arange

ZE=jblock(-13.95,13.95,-8.7,8.7,4,chim=((-11.45, 0.0), (11.45, 0.0)),win_front=[-11.95, -8.75, -5.55, -2.35, 0.85, 4.05, 7.25, 10.45],win_back=[-11.95, -8.75, -5.55, -2.35, 0.85, 4.05, 7.25, 10.45],win_side=[-6.2, -3.0, 0.2, 3.4],dorm_front=(-9.3, -0.0, 9.3),dorm_back=(-9.3, -0.0, 9.3),)
Fe=frame((0,-8.7,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-8.7-0.9-0.9*i,-8.7-0.0,0,0.6-0.2*i,'Granite')

paving(16,12)

finalize(D)
