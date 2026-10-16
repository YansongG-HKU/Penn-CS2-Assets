D='/workspace/penn_campus/QuadMcClelland'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# McClelland House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 3 floors.
# OSM way 320602420: PCA 45.6 x 18.8 m (~624 m2); ground-floor arcade lounge
from numpy import arange

ZE=jblock(-22.8,22.8,-9.4,9.4,3,chim=((-19, 0), (19, 0)),win_front=[-20.8, -17.4, -14.0, -10.6, -7.2, -3.8, -0.4, 3.0, 6.4, 9.8, 13.2, 16.6, 20.0],win_back=[-20.8, -17.4, -14.0, -10.6, -7.2, -3.8, -0.4, 3.0, 6.4, 9.8, 13.2, 16.6, 20.0],win_side=[-6.9, -3.7, -0.5, 2.7, 5.9],dorm_front=(-15, 0, 15),dorm_back=(-15, 0, 15),arch_front=[-20.8, -17.4, -14.0, -10.6, -7.2, -3.8, -0.4, 3.0, 6.4, 9.8, 13.2, 16.6, 20.0])
Fe=frame((0,-9.4,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-9.4-0.9-0.9*i,-9.4-0.0,0,0.6-0.2*i,'Granite')

paving(24,12)

finalize(D)
