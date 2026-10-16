D='/workspace/penn_campus/QuadWarwick'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Warwick House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602421: PCA 30.0 x 14.0 m
from numpy import arange

ZE=jblock(-15.0,15.0,-7.0,7.0,4,chim=((-12.5, 0.0), (12.5, 0.0)),win_front=[-13.0, -9.8, -6.6, -3.4, -0.2, 3.0, 6.2, 9.4, 12.6],win_back=[-13.0, -9.8, -6.6, -3.4, -0.2, 3.0, 6.2, 9.4, 12.6],win_side=[-4.5, -1.3, 1.9],dorm_front=(-10.0, 0.0, 10.0),dorm_back=(-10.0, 0.0, 10.0),)
Fe=frame((0,-7.0,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-7.0-0.9-0.9*i,-7.0-0.0,0,0.6-0.2*i,'Granite')

paving(16,12)

finalize(D)
