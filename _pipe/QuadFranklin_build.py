D='/workspace/penn_campus/QuadFranklin'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Franklin House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602393: PCA 24.6 x 15.8 m
from numpy import arange

ZE=jblock(-12.3,12.3,-7.9,7.9,4,chim=((-9.8, 0.0), (9.8, 0.0)),win_front=[-10.3, -7.1, -3.9, -0.7, 2.5, 5.7, 8.9],win_back=[-10.3, -7.1, -3.9, -0.7, 2.5, 5.7, 8.9],win_side=[-5.4, -2.2, 1.0, 4.2],dorm_front=(-6.15, 6.15),dorm_back=(-6.15, 6.15),)
Fe=frame((0,-7.9,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-7.9-0.9-0.9*i,-7.9-0.0,0,0.6-0.2*i,'Granite')

paving(16,12)

finalize(D)
