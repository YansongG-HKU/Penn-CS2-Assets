D='/workspace/penn_campus/QuadAshhurst'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Ashhurst House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602415: PCA 22.3 x 14.3 m
from numpy import arange

ZE=jblock(-11.15,11.15,-7.15,7.15,4,chim=((-8.65, 0.0), (8.65, 0.0)),win_front=[-9.15, -5.95, -2.75, 0.45, 3.65, 6.85],win_back=[-9.15, -5.95, -2.75, 0.45, 3.65, 6.85],win_side=[-4.65, -1.45, 1.75],dorm_front=(-5.58, 5.58),dorm_back=(-5.58, 5.58),)
Fe=frame((0,-7.15,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-7.15-0.9-0.9*i,-7.15-0.0,0,0.6-0.2*i,'Granite')

paving(12,12)

finalize(D)
