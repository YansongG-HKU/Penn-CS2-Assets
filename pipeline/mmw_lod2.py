import math; pi=math.pi
def _hip(x0,x1,y0,y1,z0,z1):
    if x1-x0>=y1-y0:
        r=(y1-y0)/2; ym=(y0+y1)/2; a=min(r*0.95,(x1-x0)/2-0.1)
        P=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0+a,ym,z1),(x1-a,ym,z1)]; Fs=[(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4),(3,2,1,0)]
    else:
        r=(x1-x0)/2; xm=(x0+x1)/2; a=min(r*0.95,(y1-y0)/2-0.1)
        P=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(xm,y0+a,z1),(xm,y1-a,z1)]; Fs=[(0,1,4),(1,2,5,4),(2,3,5),(3,0,4,5),(3,2,1,0)]
    v=[bm.verts.new(p) for p in P]
    for f in Fs: bm.faces.new([v[i] for i in f])
def _ex(pts,z0,z1):
    a=[bm.verts.new((x,y,z0)) for x,y in pts]; b=[bm.verts.new((x,y,z1)) for x,y in pts]; n=len(pts)
    bm.faces.new(a[::-1]); bm.faces.new(b)
    for i in range(n): bm.faces.new((a[i],a[(i+1)%n],b[(i+1)%n],b[i]))
boxr(-LOTX/2,LOTX/2,-LOTY/2,LOTY/2,-0.05,0)
for x0,x1,y0,y1 in BL:
    y0+=SHIFTY; y1+=SHIFTY
    boxr(x0-0.15,x1+0.15,y0-0.15,y1+0.15,0,ZC+0.8); _hip(x0-0.5,x1+0.5,y0-0.5,y1+0.5,ZC+0.8,ZR)
if AP:
    cx,cy,rx,ry=AP; cy+=SHIFTY; N=8
    _ex([(cx+(rx+0.15)*math.cos(pi*k/N),cy+(ry+0.15)*math.sin(pi*k/N)) for k in range(N+1)],0,ZA)
    _ex([(cx+(rx+0.9)*0.6*math.cos(pi*k/N),cy+(ry+0.9)*0.6*math.sin(pi*k/N)) for k in range(N+1)],ZA,ZA+(ZAR-ZA)*0.75)

_B=[(a,b,c+SHIFTY,d+SHIFTY) for a,b,c,d in BL]; x0,x1,y0,y1=_B[ENT]; XA=x0; XB=x1
_o=[b for i,b in enumerate(_B) if i!=ENT and b[2]<y0-0.5]
for b in _o:
    if b[1]>x0 and b[0]<(x0+x1)/2: XA=max(XA,b[1])
    if b[0]<x1 and b[1]>(x0+x1)/2: XB=min(XB,b[0])
YT=max([b[2] for b in _o]+[y0-6.0]); xc=(XA+XB)/2
if not globals().get('NOTERRACE'):
    boxr(XA,XB,YT,y0,0,ZT+1.0)
    _v=[bm.verts.new(p) for p in [(XA+1.0,YT-3.4,0),(XB-1.0,YT-3.4,0),(XB-1.0,YT,0),(XA+1.0,YT,0),(xc+1.5,YT-3.4,ZT),(xc+1.5,YT,ZT),(xc-1.5,YT-3.4,ZT),(xc-1.5,YT,ZT)]]
    for f in [(3,2,1,0),(0,1,4,6),(1,2,5,4),(2,3,7,5),(3,0,6,7),(6,4,5,7)]: bm.faces.new([_v[i] for i in f])
