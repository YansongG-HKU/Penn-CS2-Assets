D='/workspace/penn_campus/QuadBrooks'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Brooks House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602395: PCA 23.1 x 15.8 m
from numpy import arange

ZE=jblock(-11.55,11.55,-7.9,7.9,4,chim=((-9.05, 0.0), (9.05, 0.0)),win_front=[-9.55, -6.35, -3.15, 0.05, 3.25, 6.45],win_back=[-9.55, -6.35, -3.15, 0.05, 3.25, 6.45],win_side=[-5.4, -2.2, 1.0, 4.2],dorm_front=(-5.78, 5.78),dorm_back=(-5.78, 5.78),)
Fe=frame((0,-7.9,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-7.9-0.9-0.9*i,-7.9-0.0,0,0.6-0.2*i,'Granite')

paving(16,12)

finalize(D)
