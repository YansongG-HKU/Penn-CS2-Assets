D='/workspace/penn_campus/QuadBaldwinE'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# BaldwinE House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602391: PCA 14.9 x 13.5 m
from numpy import arange

ZE=jblock(-7.45,7.45,-6.75,6.75,4,chim=((5.25, 0.0),),win_front=[-5.45, -2.25, 0.95, 4.15],win_back=[-5.45, -2.25, 0.95, 4.15],win_side=[-4.25, -1.05, 2.15],dorm_front=(0.0,),dorm_back=(0.0,),)
Fe=frame((0,-6.75,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-6.75-0.9-0.9*i,-6.75-0.0,0,0.6-0.2*i,'Granite')

paving(12,12)

finalize(D)
