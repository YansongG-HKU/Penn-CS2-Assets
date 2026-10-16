D='/workspace/penn_campus/QuadMemorialTower'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
exec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())
# War Memorial Tower (Cope & Stewardson, 1901): gateway tower with three onion-domed towers, red brick with limestone bands/quoins.
# OSM way 320602388: PCA 22.1 x 21.6 m (~267 m2 core)
from numpy import arange

jblock(-11,11,0,10.6,4,chim=((-8,5.3),(8,5.3)),win_back=ar(-9,9,3.0),dorm_back=(-5,5))
# three towers: centre taller
for (x,w,H,r) in ((-7.2,6.0,26.0,2.7),(7.2,6.0,26.0,2.7),(0,8.4,30.0,3.6)):
    y0,y1=-10.8,0.4
    if x!=0: y0,y1=-9.6,0.4
    boxr(x-w/2,x+w/2,y0,y1,0,0.6,'Granite'); boxr(x-w/2,x+w/2,y0,y1,0.6,H,'Brick')
    for z in np.arange(3.6,H-1,3.4): boxr(x-w/2-0.05,x+w/2+0.05,y0-0.05,y1+0.05,z,z+0.3,'Limestone')
    for (xx,s) in ((x-w/2,1),(x+w/2,-1)):
        for z in np.arange(0.6,H-1.0,1.0): box((xx+s*0.45,y0-0.03,z),(0.9 if int(z)%2==0 else 0.5,0.06,0.5),'Limestone')
    # scalloped stone parapet + merlons
    boxr(x-w/2-0.3,x+w/2+0.3,y0-0.3,y1+0.3,H,H+0.5,'LimeDark')
    for k in range(int(w/1.2)+1):
        xm=x-w/2+k*w/int(w/1.2); box((xm,y0-0.15,H+0.5),(0.5,0.3,0.8),'Limestone'); box((xm,y1+0.15,H+0.5),(0.5,0.3,0.8),'Limestone')
    boxr(x-w/2+0.2,x+w/2-0.2,y0+0.2,y1-0.2,H,H+0.9,'Brick')
    onion(x,(y0+y1)/2,H+0.9,r)
    F=frame((x,y0,0),pi)
    for z in np.arange(4.3,H-3.5,3.4):
        if x==0: window(F,-1.6,z,1.5,2.1,None,0.1,'Limestone'); window(F,1.6,z,1.5,2.1,None,0.1,'Limestone')
        else: window(F,0,z,1.5,2.1,None,0.1,'Limestone')
# gateway arch
Fg=frame((0,-10.8,0),pi); door(Fg,0,3.6,4.4,0.6,None,y=0.1)
boxr(-2.6,2.6,-11.1,-10.8,5.0,5.6,'Limestone')
paving(12,12)

finalize(D)
