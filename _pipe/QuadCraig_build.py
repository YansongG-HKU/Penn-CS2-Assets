D='/workspace/penn_campus/QuadCraig'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Craig House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602403: PCA 20.3 x 17.5 m
from numpy import arange

ZE=jblock(-10.15,10.15,-8.75,8.75,4,chim=((-7.65, 0.0), (7.65, 0.0)),win_front=[-8.15, -4.95, -1.75, 1.45, 4.65, 7.85],win_back=[-8.15, -4.95, -1.75, 1.45, 4.65, 7.85],win_side=[-6.25, -3.05, 0.15, 3.35],dorm_front=(-5.08, 5.08),dorm_back=(-5.08, 5.08),)
Fe=frame((0,-8.75,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-8.75-0.9-0.9*i,-8.75-0.0,0,0.6-0.2*i,'Granite')

paving(12,12)

finalize(D)
