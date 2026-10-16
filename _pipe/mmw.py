# Shared McKim-Mead-White brick+limestone builder (Schermerhorn / Havemeyer).
# Needs: BL (blocks x0,x1,y0,y1), AP (apse cx,cy,rx,ry,dir -> +Y), ZT,ZC,ZR, ENT (entrance block idx), LOTX,LOTY, SHIFTY
def inside(px,py,skip=-1,m=0.05):
    for i,(x0,x1,y0,y1) in enumerate(BL):
        if i!=skip and x0-m<px<x1+m and y0-m<py<y1+m: return True
    if not AP: return False
    cx,cy,rx,ry=AP
    if ((px-cx)/(rx+m))**2+((py-cy)/(ry+m))**2<1 and py>cy-m: return True
    return False
def cor(F,x0,x1,z,p=1.0,m='LimeDark'):
    boxr(x0,x1,0,0.25*p,z,z+0.3,m,F); boxr(x0-0.1,x1+0.1,0,0.55*p,z+0.3,z+0.5,m,F); boxr(x0-0.2,x1+0.2,0,p,z+0.5,z+0.8,m,F)
    n=int((x1-x0)/1.1); DROPF[0]=True
    for k in range(n+1): box((x0+k*(x1-x0)/n,0.6*p,z+0.5),(0.25,0.5*p,0.12),m,F)
    DROPF[0]=False
def hip(x0,x1,y0,y1,z0,z1):
    if x1-x0>=y1-y0:
        r=(y1-y0)/2; ym=(y0+y1)/2; a=min(r*0.95,(x1-x0)/2-0.1)
        P=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0+a,ym,z1),(x1-a,ym,z1)]; Fs=[(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4),(3,2,1,0)]
    else:
        r=(x1-x0)/2; xm=(x0+x1)/2; a=min(r*0.95,(y1-y0)/2-0.1)
        P=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(xm,y0+a,z1),(xm,y1-a,z1)]; Fs=[(0,1,4),(1,2,5,4),(2,3,5),(3,0,4,5),(3,2,1,0)]
    v=[bm.verts.new(p) for p in P]; n0=len(bm.faces)
    for f in Fs: bm.faces.new([v[i] for i in f])
    tag(n0,'Roof')
def extr(pts,z0,z1,m):
    n0=len(bm.faces); a=[bm.verts.new((x,y,z0)) for x,y in pts]; b=[bm.verts.new((x,y,z1)) for x,y in pts]; n=len(pts)
    fs=[bm.faces.new(a[::-1]),bm.faces.new(b)]
    for i in range(n): fs.append(bm.faces.new((a[i],a[(i+1)%n],b[(i+1)%n],b[i])))
    bmesh.ops.recalc_face_normals(bm,faces=fs); tag(n0,m)
BL=[(x0,x1,y0+SHIFTY,y1+SHIFTY) for x0,x1,y0,y1 in BL]; AP=(AP[0],AP[1]+SHIFTY,AP[2],AP[3]) if AP else None
UPS=[]; z=ZT+5.6
while z+2.1<ZC-1.6: UPS.append(z); z+=FLH
# audit: snap belt course ZB into the gap between window rows (above lintel, below next sill) so it never crosses glass
_g=[(u+2.6, n-0.32) for u,n in zip(UPS,UPS[1:])]
if _g: ZB=min(_g,key=lambda g:abs((g[0]+g[1])/2-ZB)); ZB=(ZB[0]+ZB[1])/2-0.275
# massing
for i,(x0,x1,y0,y1) in enumerate(BL):
    boxr(x0-0.15,x1+0.15,y0-0.15,y1+0.15,0,ZT,'Rustic'); boxr(x0-0.3,x1+0.3,y0-0.3,y1+0.3,0,0.9,'Granite')
    DROPF[0]=True
    for zz in np.arange(1.4,ZT-0.3,0.65): boxr(x0-0.17,x1+0.17,y0-0.17,y1+0.17,zz,zz+0.05,'LimeDark')
    DROPF[0]=False
    boxr(x0,x1,y0,y1,ZT,ZC,'Brick')
    for (z0,z1,o) in ((ZT,ZT+0.45,0.04),(ZB+0.15,ZB+0.40,0.04),(ZC-1.1,ZC,0.04)): boxr(x0-o,x1+o,y0-o,y1+o,z0,z1,'LimeDark' if z1-z0<1 else 'Limestone')
    hip(x0-0.5,x1+0.5,y0-0.5,y1+0.5,ZC+0.8,ZR)
if AP:
    # apse (semi-ellipse toward +Y), lower roof
    cx,cy,rx,ry=AP; N=14
    ell=lambda r,e:[(cx+(rx+e)*math.cos(pi*k/N),cy+(ry+e)*math.sin(pi*k/N)) for k in range(N+1)]
    extr(ell(0,0.15),0,ZT,'Rustic'); extr(ell(0,0),ZT,ZA,'Brick'); extr(ell(0,0.2),ZT,ZT+0.6,'LimeDark'); extr(ell(0,0.12),ZA-1.0,ZA,'Limestone')
    for k in range(5):
        t=k/5.0; t2=(k+1)/5.0; s0=math.cos(t*pi/2); s1=math.cos(t2*pi/2)
        extr([(cx+(rx+0.9)*s0*math.cos(pi*j/N),cy+(ry+0.9)*s0*math.sin(pi*j/N)) for j in range(N+1)],ZA+(ZAR-ZA)*math.sin(t*pi/2),ZA+(ZAR-ZA)*math.sin(t2*pi/2)+0.01,'Roof') if False else None
    lv=[bm.verts.new((cx+(rx+0.9)*math.cos(pi*j/N),cy+(ry+0.9)*math.sin(pi*j/N),ZA)) for j in range(N+1)]
    mv=[bm.verts.new((cx+(rx+0.9)*0.6*math.cos(pi*j/N),cy+(ry+0.9)*0.6*math.sin(pi*j/N),ZA+(ZAR-ZA)*0.75)) for j in range(N+1)]
    tp=bm.verts.new((cx,cy,ZAR)); c0=bm.verts.new((cx,cy,ZA)); n0=len(bm.faces)
    for j in range(N):
        bm.faces.new((lv[j],lv[j+1],mv[j+1],mv[j])); bm.faces.new((mv[j],mv[j+1],tp))
    bm.faces.new([c0]+lv[::-1]); bm.faces.new((c0,lv[0],mv[0],tp)); bm.faces.new((c0,tp,mv[N],lv[N]))
    fs=newf(n0); bmesh.ops.recalc_face_normals(bm,faces=fs); tag(n0,'Roof')
    for j in range(1,N,2):
        a=pi*j/N; px=cx+rx*math.cos(a); py=cy+ry*math.sin(a)
        nx,ny=math.cos(a)/rx,math.sin(a)/ry; l=math.hypot(nx,ny); nx/=l; ny/=l
        if inside(px+nx*0.6,py+ny*0.6,m=0.4): continue
        F=frame((px,py,0),math.atan2(-nx,ny))
        window(F,0,1.5,1.0,1.7,None,0.18,'LimeDark'); window(F,0,4.2,1.0,1.7,None,0.18,'LimeDark')
        archwin(F,0,ZT+1.1,1.6,ZA-ZT-3.0)

# facades
def facade(i,side):
    x0,x1,y0,y1=BL[i]
    if side=='S': o=((x0+x1)/2,y0); ang=pi; L=x1-x0
    elif side=='N': o=((x0+x1)/2,y1); ang=0; L=x1-x0
    elif side=='E': o=(x1,(y0+y1)/2); ang=-pi/2; L=y1-y0
    else: o=(x0,(y0+y1)/2); ang=pi/2; L=y1-y0
    F=frame((o[0],o[1],0),ang); cor(F,-L/2,L/2,ZC,1.1)
    n=int((L-3.0)/BAY)+1; xs=[(k-(n-1)/2)*BAY for k in range(n)]
    def wp(x):
        p=F@Vector((x,1.2,0)); return inside(p.x,p.y,skip=i)
    ent=(i==ENT and side=='S')
    for x in xs:
        if wp(x) or wp(x-1.3) or wp(x+1.3): continue
        door_bay=ent and abs(x)<BAY*1.2
        bsk=any(lo<x<hi for (bi,bs,lo,hi) in globals().get('BSKIP',[]) if bi==i and bs==side)
        if not ent and not bsk and ZT>3:
            for zz in (1.5,4.2): window(F,x,zz,1.2,1.7,None,0.18,'LimeDark')
        if not door_bay: window(F,x,ZT+1.1,1.5,3.1,'cor',0,'LimeDark')
        for zz in UPS:
            if door_bay and zz<(ZT+8.5 if abs(x)<0.1 else ZB+0.3): continue
            h=2.1
            window(F,x,zz,1.4,h,None,0,'LimeDark')
        if 'ATTIC' in globals() and not (door_bay and abs(x)>0.1):
            az,ah=ATTIC
            ah2=min(ah,(ZC-1.15)-az) if az+ah>ZC-1.1 else ah
            if ah2>=0.8: window(F,x,az,1.4,ah2,None,0,'LimeDark')
    # quoins at both ends
    DROPF[0]=True
    for e in (-1,1):
        if wp(e*(L/2+0.6)): continue
        for k,zz in enumerate(np.arange(ZT+0.6,ZC-1.2,0.6)):
            a=1.0 if k%2==0 else 0.6
            box((e*(L/2-a/2),0.035,zz),(a,0.07,0.5),'LimeDark',F)
    DROPF[0]=False
    return F,L
FS={}
for i in range(len(BL)):
    for s in 'SNEW': FS[(i,s)]=facade(i,s)
# entrance (campus level = ZT) on front (S) of block ENT
F,L=FS[(ENT,'S')]
for x in (-3.2,3.2): pilaster(F,x,ZT+0.6,ZB-0.2,0.9,0.25)
archwin(F,0,ZT+5.4,3.2,1.61,'Limestone'); door(F,0,2.6,4.2,ZT,None,y=0.0)
box((0,0.3,ZT+7.2),(0.7,0.6,0.9),'Limestone',F)
for q in (-1,1):
    for zz in UPS: window(F,q*BAY*0.0+q*5.6,zz,1.4,2.1,None,0,'LimeDark') if False else None
# campus terrace in the recess + lateral stair flights
x0,x1,y0,y1=BL[ENT]; XA=max(b[1] for b in BL if b[1]<=x0+0.5) if any(b[1]<=x0+0.5 for b in BL) else x0
XA=x0; XB=x1
for b in BL:
    if b is not BL[ENT] and b[2]<y0-0.5:
        if b[1]>x0 and b[0]<(x0+x1)/2: XA=max(XA,b[1])
        if b[0]<x1 and b[1]>(x0+x1)/2: XB=min(XB,b[0])
YT=max([b[2] for b in BL if b is not BL[ENT] and b[2]<y0-0.5]+[y0-6.0])
xc=(XA+XB)/2
if not globals().get('NOTERRACE'):
    boxr(XA,XB,YT,y0-0.15,0,ZT-0.05,'Rustic'); boxr(XA,XB,YT,y0-0.15,ZT-0.05,ZT,'Paving')
    NS=int(ZT/0.17); ri=ZT/NS; tr=min(0.28,((XB-XA)/2-2.0)/NS); W=3.0
    for s in (-1,1):
        for k in range(NS):
            xa=xc+s*(1.5+k*tr); xb=xc+s*(1.5+(k+1)*tr)
            boxr(min(xa,xb),max(xa,xb),YT-W,YT,0,ZT-k*ri,'Granite')
        xe=1.5+NS*tr; pts=[(xc+s*1.5,0),(xc+s*xe,0),(xc+s*xe,0.9),(xc+s*1.5,ZT+0.9)]
        if s<0: pts=pts[::-1]
        prism(pts,YT-W-0.4,YT-W,'LimeDark')
        boxr(min(xc+s*1.6,xc+s*((XB-XA)/2)),max(xc+s*1.6,xc+s*((XB-XA)/2)),YT,YT+0.45,ZT,ZT+1.0,'LimeDark')
    boxr(xc-1.5,xc+1.5,YT-W,YT,0,ZT,'Granite')
else:
    YT=y0-0.2; NS=max(1,int(ZT/0.16))
    for k in range(NS): boxr(-2.4,2.4,y0-0.15-(NS-k)*0.32,y0-0.15,k*ZT/NS,(k+1)*ZT/NS,'Granite')
boxr(-LOTX/2,LOTX/2,-LOTY/2,LOTY/2,-0.05,0.0,'Paving')
LZ=0.0 if globals().get('NOTERRACE') else ZT
for s in (-1,1):
    x=xc+s*(3.9 if globals().get('NOTERRACE') else 2.0); y=YT+1.0 if not globals().get('NOTERRACE') else y0-1.2
    lathe((x,y,LZ),[(0.3,0),(0.3,0.4),(0.18,0.6),(0.1,1.0),(0.08,2.6),(0.22,2.75),(0.08,2.85)],12,'Bronze')
    lathe((x,y,LZ+2.85),[(0.18,0),(0.22,0.2),(0.18,0.5)],10,'Gls'); lathe((x,y,LZ+3.35),[(0.26,0),(0.04,0.3)],10,'Bronze')
    cyl((x,y,LZ+2.84),0.05,0.52,6,'Bronze')
exec(EXTRA) if 'EXTRA' in globals() else None
finalize(D)
