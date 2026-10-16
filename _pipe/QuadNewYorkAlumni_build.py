D='/workspace/penn_campus/QuadNewYorkAlumni'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# NewYorkAlumni House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602401: PCA 19.0 x 13.0 m
from numpy import arange

ZE=jblock(-9.5,9.5,-6.5,6.5,4,chim=((7.3, 0.0),),win_front=[-7.5, -4.3, -1.1, 2.1, 5.3],win_back=[-7.5, -4.3, -1.1, 2.1, 5.3],win_side=[-4.0, -0.8, 2.4],dorm_front=(-4.75, 4.75),dorm_back=(-4.75, 4.75),)
Fe=frame((0,-6.5,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-6.5-0.9-0.9*i,-6.5-0.0,0,0.6-0.2*i,'Granite')

paving(12,12)

finalize(D)
