D='/workspace/penn_campus/QuadFoerderer'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Foerderer House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602392: PCA 24.0 x 12.0 m
from numpy import arange

ZE=jblock(-12.0,12.0,-6.0,6.0,4,chim=((-9.5, 0.0), (9.5, 0.0)),win_front=[-10.0, -6.8, -3.6, -0.4, 2.8, 6.0, 9.2],win_back=[-10.0, -6.8, -3.6, -0.4, 2.8, 6.0, 9.2],win_side=[-3.5, -0.3, 2.9],dorm_front=(-6.0, 6.0),dorm_back=(-6.0, 6.0),)
Fe=frame((0,-6.0,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-6.0-0.9-0.9*i,-6.0-0.0,0,0.6-0.2*i,'Granite')

paving(16,12)

finalize(D)
