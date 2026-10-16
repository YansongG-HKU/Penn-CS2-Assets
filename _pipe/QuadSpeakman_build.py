D='/workspace/penn_campus/QuadSpeakman'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# Speakman House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. 4 floors.
# OSM way 320602397: PCA 51.2 x 17.5 m (~698 m2)
from numpy import arange

ZE=jblock(-25.6,25.6,-8.75,8.75,4,chim=((-22.1, 0), (0, 0), (22.1, 0)),win_front=[-23.6, -20.4, -17.2, -14.0, -10.8, -7.6, -4.4, -1.2, 2.0, 5.2, 8.4, 11.6, 14.8, 18.0, 21.2],win_back=[-23.6, -20.4, -17.2, -14.0, -10.8, -7.6, -4.4, -1.2, 2.0, 5.2, 8.4, 11.6, 14.8, 18.0, 21.2],win_side=[-6.25, -3.05, 0.15, 3.35],dorm_front=(-18, -6, 6, 18),dorm_back=(-18, -6, 6, 18),)
Fe=frame((0,-8.75,0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,-8.75-0.9-0.9*i,-8.75-0.0,0,0.6-0.2*i,'Granite')

paving(28,12)

finalize(D)
