D='/workspace/penn_campus/QuadCleemann'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Cleemann House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602417: PCA 28.1 x 10.7 m
from numpy import arange

ZE=jblock(-14.05,14.05,-5.35,5.35,4,chim=((-11.55, 0.0), (11.55, 0.0)),win_front=[-12.05, -8.85, -5.65, -2.45, 0.75, 3.95, 7.15, 10.35],win_back=[-12.05, -8.85, -5.65, -2.45, 0.75, 3.95, 7.15, 10.35],win_side=[-2.85, 0.35],dorm_front=(-9.37, 0.0, 9.37),dorm_back=(-9.37, 0.0, 9.37),)
Fe=frame((0,-5.35,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-5.35-0.9-0.9*i,-5.35-0.0,0,0.6-0.2*i,'Granite')

paving(16,12)

finalize(D)
