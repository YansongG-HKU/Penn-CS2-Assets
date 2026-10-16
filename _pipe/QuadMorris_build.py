D='/workspace/penn_campus/QuadMorris'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Morris House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602418: PCA 30.7 x 19.7 m
from numpy import arange

ZE=jblock(-15.35,15.35,-9.85,9.85,4,chim=((-12.85, 0.0), (12.85, 0.0)),win_front=[-13.35, -10.15, -6.95, -3.75, -0.55, 2.65, 5.85, 9.05, 12.25],win_back=[-13.35, -10.15, -6.95, -3.75, -0.55, 2.65, 5.85, 9.05, 12.25],win_side=[-7.35, -4.15, -0.95, 2.25, 5.45],dorm_front=(-10.23, -0.0, 10.23),dorm_back=(-10.23, -0.0, 10.23),)
Fe=frame((0,-9.85,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-9.85-0.9-0.9*i,-9.85-0.0,0,0.6-0.2*i,'Granite')

paving(16,16)

finalize(D)
