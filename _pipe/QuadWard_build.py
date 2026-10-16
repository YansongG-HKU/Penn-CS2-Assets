D='/workspace/penn_campus/QuadWard'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Ward House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602400: PCA 23.6 x 23.3 m (~308 m2); corner house
from numpy import arange

ZE=jblock(-11.8,11.8,-11.6,11.6,4,chim=((0, 0),),win_front=[-9.8, -6.6, -3.4, -0.2, 3.0, 6.2, 9.4],win_back=[-9.8, -6.6, -3.4, -0.2, 3.0, 6.2, 9.4],win_side=[-9.1, -5.9, -2.7, 0.5, 3.7, 6.9],dorm_front=(-5, 5),dorm_back=(-5, 5),)
Fe=frame((0,-11.6,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-11.6-0.9-0.9*i,-11.6-0.0,0,0.6-0.2*i,'Granite')
lathe((-11.8,-11.6,0),[(2.6,0),(2.6,ZE+2.0)],8,'Brick')
lathe((-11.8,-11.6,ZE+2.0),[(2.9,0),(2.9,0.4)],8,'Limestone')
lathe((-11.8,-11.6,ZE+2.4),[(2.9,0),(0.1,5.0)],8,'Roof')
paving(16,16)

finalize(D)
