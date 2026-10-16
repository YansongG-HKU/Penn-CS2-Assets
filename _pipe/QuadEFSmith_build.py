D='/workspace/penn_campus/QuadEFSmith'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# EFSmith House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602411: PCA 23.7 x 14.1 m
from numpy import arange

ZE=jblock(-11.85,11.85,-7.05,7.05,4,chim=((-9.35, 0.0), (9.35, 0.0)),win_front=[-9.85, -6.65, -3.45, -0.25, 2.95, 6.15, 9.35],win_back=[-9.85, -6.65, -3.45, -0.25, 2.95, 6.15, 9.35],win_side=[-4.55, -1.35, 1.85],dorm_front=(-5.92, 5.92),dorm_back=(-5.92, 5.92),)
Fe=frame((0,-7.05,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-7.05-0.9-0.9*i,-7.05-0.0,0,0.6-0.2*i,'Granite')

paving(16,12)

finalize(D)
