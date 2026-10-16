D='/workspace/penn_campus/QuadMcKean'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# McKean House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602389: PCA 33.5 x 22.6 m
from numpy import arange

ZE=jblock(-16.75,16.75,-11.3,11.3,4,chim=((-14.25, 0.0), (14.25, 0.0)),win_front=[-14.75, -11.55, -8.35, -5.15, -1.95, 1.25, 4.45, 7.65, 10.85, 14.05],win_back=[-14.75, -11.55, -8.35, -5.15, -1.95, 1.25, 4.45, 7.65, 10.85, 14.05],win_side=[-8.8, -5.6, -2.4, 0.8, 4.0, 7.2],dorm_front=(-11.17, -0.0, 11.17),dorm_back=(-11.17, -0.0, 11.17),)
Fe=frame((0,-11.3,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-11.3-0.9-0.9*i,-11.3-0.0,0,0.6-0.2*i,'Granite')

paving(20,16)

finalize(D)
