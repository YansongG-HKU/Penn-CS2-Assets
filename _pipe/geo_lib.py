import bpy,bmesh,math,random,numpy as np,os
from mathutils import Matrix,Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
bm=bmesh.new()
UVL=bm.loops.layers.uv.new('UVMap'); PRE=bm.faces.layers.int.new('preuv'); DROP=bm.faces.layers.int.new('drop'); VAL=bm.verts.layers.int.new('valley'); SUV=bm.loops.layers.uv.new('ScanUV'); STX=bm.faces.layers.int.new('scantex')
DROPF=[False]
MATS=['Limestone','LimeDark','Rustic','Granite','Paving','Brick','Roof','Bronze','Iron','Copper','Lawn','Hedge','Carve','Lamp','Win','Gls']
MI={n:i for i,n in enumerate(MATS)}
I=Matrix.Identity(4); pi=math.pi
def newf(n0):
    bm.faces.ensure_lookup_table(); return [bm.faces[i] for i in range(n0,len(bm.faces))]
def tag(n0,m):
    fs=newf(n0)
    for f in fs:
        f.material_index=MI[m]
        if DROPF[0]: f[DROP]=1
    return fs
def boxm(M,m):
    n0=len(bm.faces); bmesh.ops.create_cube(bm,size=1,matrix=M); return tag(n0,m)
def box(c,s,m,F=I,rz=0):
    return boxm(F@Matrix.Translation((c[0],c[1],c[2]+s[2]/2))@Matrix.Rotation(rz,4,'Z')@Matrix.Diagonal((s[0],s[1],s[2],1)),m)
def boxr(x0,x1,y0,y1,z0,z1,m,F=I):
    return box(((x0+x1)/2,(y0+y1)/2,z0),(abs(x1-x0),abs(y1-y0),z1-z0),m,F)
AX={'Z':I,'Y':Matrix.Rotation(-pi/2,4,'X'),'X':Matrix.Rotation(pi/2,4,'Y')}
def cyl(c,r,h,seg,m,F=I,r2=None,axis='Z'):
    n0=len(bm.faces)
    M=F@Matrix.Translation(c)@AX[axis]@Matrix.Translation((0,0,h/2))
    bmesh.ops.create_cone(bm,cap_ends=True,cap_tris=False,segments=seg,radius1=r,radius2=(r if r2 is None else r2),depth=h,matrix=M)
    return tag(n0,m)
def lathe(c,prof,seg,m,F=I,closed=False,rot=0.0,radfn=None):
    n0=len(bm.faces); rings=[]
    for (r,z) in prof:
        ring=[]
        for i in range(seg):
            a=2*pi*i/seg+rot; rr=r*(radfn(i) if radfn else 1)
            v=bm.verts.new(F@Vector((c[0]+rr*math.cos(a),c[1]+rr*math.sin(a),c[2]+z)))
            if radfn and radfn(i)<1: v[VAL]=1
            ring.append(v)
        rings.append(ring)
    L=len(rings); vc=[0.0]
    for j in range(1,L+(1 if closed else 0)):
        p0,p1=prof[j-1],prof[j%L]; vc.append(vc[-1]+math.hypot(p1[0]-p0[0],p1[1]-p0[1]))
    rmax=max(p[0] for p in prof); du=2*pi*rmax/seg
    for j in range(L if closed else L-1):
        a,b=rings[j],rings[(j+1)%L]
        for i in range(seg):
            i2=(i+1)%seg
            try: f=bm.faces.new((a[i],a[i2],b[i2],b[i]))
            except ValueError: continue
            f[PRE]=1
            for lp,uv in zip(f.loops,((i*du,vc[j]),((i+1)*du,vc[j]),((i+1)*du,vc[j+1]),(i*du,vc[j+1]))): lp[UVL].uv=uv
    if not closed:
        for ring,rev,r in ((rings[0],True,prof[0][0]),(rings[-1],False,prof[-1][0])):
            if r>1e-4:
                f=bm.faces.new(list(reversed(ring)) if rev else ring); f[PRE]=1
                for k,lp in enumerate(f.loops):
                    idx=ring.index(lp.vert); a_=2*pi*idx/seg; lp[UVL].uv=(r*math.cos(a_)+r,r*math.sin(a_)+r)
    return tag(n0,m)
def torus(c,R,rr,seg,sr,m,F=I,axis='Z'):
    prof=[(R+rr*math.cos(2*pi*k/sr),rr*math.sin(2*pi*k/sr)) for k in range(sr)]
    return lathe((0,0,0),prof,seg,m,F@Matrix.Translation(c)@AX[axis],closed=True)
def prism(pts,y0,y1,m,F=I):
    n0=len(bm.faces)
    a=[bm.verts.new(F@Vector((x,y0,z))) for x,z in pts]; b=[bm.verts.new(F@Vector((x,y1,z))) for x,z in pts]
    n=len(pts); fs=[bm.faces.new(a),bm.faces.new(list(reversed(b)))]
    for i in range(n): fs.append(bm.faces.new((a[i],a[(i+1)%n],b[(i+1)%n],b[i])))
    bmesh.ops.recalc_face_normals(bm,faces=fs); return tag(n0,m)
def poly(pts3,m,F=I,nrm=(0,1,0)):
    n0=len(bm.faces); f=bm.faces.new([bm.verts.new(F@Vector(p)) for p in pts3]); f.normal_update()
    if f.normal.dot(F.to_3x3()@Vector(nrm))<0: f.normal_flip()
    return tag(n0,m)
def frame(o,ang): return Matrix.Translation(o)@Matrix.Rotation(ang,4,'Z')
def column(F,x,y,z0,H=10.67,Dm=1.22):
    bm.faces.ensure_lookup_table(); _n0=len(bm.faces); _column_body(F,x,y,z0,H,Dm); bm.faces.ensure_lookup_table()
    for f in list(bm.faces)[_n0:]: f[DROP]=0
def _column_body(F,x,y,z0,H,Dm):
    r=Dm/2
    box((x,y,z0),(1.38*Dm,1.38*Dm,0.18),'Limestone',F)
    lathe((x,y,z0+0.18),[(0.66*Dm,0),(0.66*Dm,0.08),(0.6*Dm,0.16),(0.55*Dm,0.2),(0.58*Dm,0.26),(0.6*Dm,0.32),(0.53*Dm,0.4),(r*1.02,0.44)],24,'Limestone',F)
    zs=z0+0.62; zt=z0+H-0.72; prof=[]
    for k in range(7):
        t=k/6; prof.append((r*(1-0.14*t**1.6),(zt-zs)*t))
    lathe((x,y,zs),prof,48,'Limestone',F,rot=-pi/2,radfn=lambda i:1.0 if i%2==0 else 0.955)
    lathe((x,y,zt),[(0.88*r,0),(0.95*r,0.06),(1.1*r,0.2),(1.12*r,0.3),(1.0*r,0.38)],24,'Limestone',F)
    zv=zt+0.42
    box((x,y,zt+0.3),(1.55*Dm,0.95*Dm,0.24),'Limestone',F)
    for s in (-1,1):
        cyl((x+s*0.66*Dm,y-0.5*Dm,zv),0.27*Dm,Dm,12,'Limestone',F,axis='Y')
        DROPF[0]=True
        for e in (-1,1):
            yy=y+e*0.51*Dm
            torus((x+s*0.66*Dm,yy,zv),0.18*Dm,0.06*Dm,12,5,'Limestone',F,axis='Y')
            cyl((x+s*0.66*Dm,yy-0.04,zv),0.07*Dm,0.08,8,'Limestone',F,axis='Y')
        DROPF[0]=False
    box((x,y,zt+0.6),(1.42*Dm,1.42*Dm,0.12),'Limestone',F)
SASHM=globals().get('SASHM','Bronze')
def window(F,x,z,w,h,ped=None,y=0.0,frm='LimeDark'):
    # v2 (audit): brick reveals, thin dark sash, stone sill + flat-arch lintel with keystone (MMW campus style)
    # glass/sash proud of belt courses (belts use o<=0.04); avoids white string-courses stacking on panes
    poly([(x-w/2,y+0.06,z),(x+w/2,y+0.06,z),(x+w/2,y+0.06,z+h),(x-w/2,y+0.06,z+h)],'Win',F)
    t=0.12
    box((x-w/2-t/2,y+0.10,z),(t,0.14,h),SASHM,F); box((x+w/2+t/2,y+0.10,z),(t,0.14,h),SASHM,F)
    box((x,y+0.10,z-t),(w+2*t,0.14,t),SASHM,F)
    box((x,y+0.16,z-t-0.18),(w+0.5,0.28,0.18),frm,F)
    box((x,y+0.09,z),(0.09,0.08,h),SASHM,F)
    n=max(1,int(h/1.0)); DROPF[0]=True
    for k in range(1,n+1): box((x,y+0.09,z+k*h/(n+1)),(w,0.08,0.08),SASHM,F)
    for q in (-1,1): box((x+q*w/4,y+0.08,z),(0.07,0.06,h),SASHM,F)
    DROPF[0]=False
    # lintel sits on glass top (box Z = bottom). Keystone starts at lintel top (was z+h-0.05 → 5cm into glass = white tick)
    box((x,y+0.12,z+h),(w+2*t+0.5,0.16,0.45),frm,F)
    zt=z+h+0.45
    if ped in ('tri','seg','cor'):
        box((x,y+0.14,zt),(w+2*t+0.7,0.28,0.3),frm,F)
        box((x,y+0.25,zt+0.3),(w+2*t+1.0,0.5,0.2),frm,F)
        hw=(w+2*t+1.0)/2; zb=zt+0.5
        if ped=='tri': prism([(x-hw,zb),(x+hw,zb),(x,zb+0.24*hw*2)],y,y+0.45,frm,F)
        if ped=='seg':
            pts=[(x-hw,zb)]+[(x+hw*math.cos(a),zb+0.55*hw*math.sin(a)) for a in np.linspace(pi,0,9)][1:-1]+[(x+hw,zb)]
            prism(list(reversed(pts)),y,y+0.45,frm,F)
    else:
        box((x,y+0.14,zt),(0.36,0.26,0.5),frm,F)
def door(F,x,w,h,z,ped='tri',y=0.0):
    box((x,y+0.04,z),(w,0.08,h),'Bronze',F)
    for q in (-1,1):
        DROPF[0]=True
        for k in range(3): box((x+q*w/4,y+0.1,z+0.4+k*h/3.2),(w/2-0.35,0.05,h/3.2-0.4),'Bronze',F)
        DROPF[0]=False
    s=0.5
    box((x-w/2-s/2,y+0.15,z),(s,0.3,h),'LimeDark',F); box((x+w/2+s/2,y+0.15,z),(s,0.3,h),'LimeDark',F)
    box((x,y+0.15,z+h),(w+2*s,0.3,0.7),'LimeDark',F)
    box((x,y+0.3,z+h+0.7),(w+2*s+0.8,0.6,0.3),'LimeDark',F)
    if ped=='tri':
        hw=(w+2*s+0.8)/2; prism([(x-hw,z+h+1.0),(x+hw,z+h+1.0),(x,z+h+1.0+0.45*hw)],y,y+0.5,'LimeDark',F)
def pilaster(F,x,z0,z1,w=1.2,d=0.3,y=0.0):
    box((x,y+d/2+0.05,z0),(w+0.35,d+0.1,0.5),'LimeDark',F)
    box((x,y+d/2,z0+0.5),(w,d,z1-z0-1.1),'Limestone',F)
    box((x,y+d/2+0.06,z1-0.6),(w+0.3,d+0.12,0.6),'LimeDark',F)
    for q in (-1,1): cyl((x+q*w*0.42,y+d+0.12,z1-0.32),0.14,0.0,8,'LimeDark',F,r2=0.14) if False else None
def cornice(F,x0,x1,y0,yf,z,dent=True):
    boxr(x0-0.1,x1+0.1,y0,yf+0.1,ZA,ZF,'LimeDark',F)
    boxr(x0-0.3,x1+0.3,y0,yf+0.3,ZC,ZC+0.25,'LimeDark',F)
    boxr(x0-0.65,x1+0.65,y0,yf+0.65,ZC+0.25,ZC+0.5,'LimeDark',F)
    boxr(x0-0.95,x1+0.95,y0,yf+0.95,ZC+0.5,ZE,'LimeDark',F)
    if dent:
        n=int((x1-x0)/0.5); DROPF[0]=True
        for k in range(n+1): box((x0+k*(x1-x0)/n,yf+0.4,ZC+0.05),(0.2,0.2,0.18),'LimeDark',F)
        DROPF[0]=False
def maketext(body,size):
    cu=bpy.data.curves.new('t','FONT'); cu.body=body; cu.size=size; cu.align_x='CENTER'; cu.resolution_u=2; cu.fill_mode='FRONT'
    to=bpy.data.objects.new('t',cu); bpy.context.scene.collection.objects.link(to); me=to.to_mesh().copy(); bpy.data.objects.remove(to); return me
def addtext(me,M,m):
    n0=len(bm.faces); vs=[bm.verts.new(M@v.co) for v in me.vertices]
    for p in me.polygons:
        try: bm.faces.new([vs[i] for i in p.vertices])
        except ValueError: pass
    fs=tag(n0,m)
    for f in fs:
        f.normal_update()
        if f.normal.dot(M.to_3x3()@Vector((0,0,1)))<0: f.normal_flip()
def text_on(F,body,x,y,z,size,maxw,m='Carve'):
    me=maketext(body,size); wx=max(v.co.x for v in me.vertices)-min(v.co.x for v in me.vertices); sc=min(1.0,maxw/wx)
    DROPF[0]=True; addtext(me,F@Matrix.Translation((x,y,z))@Matrix.Rotation(pi,4,'Z')@Matrix.Rotation(pi/2,4,'X')@Matrix.Diagonal((sc,sc,1,1)),m); DROPF[0]=False
def finalize(D,name='Bld'):
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=0.0005)
    me=bpy.data.meshes.new(name); bm.to_mesh(me)
    ob=bpy.data.objects.new(name,me); bpy.context.scene.collection.objects.link(ob)
    for n in MATS: me.materials.append(bpy.data.materials.new(n))
    import collections
    print('TRIS',sum(len(p.vertices)-2 for p in me.polygons),'per',collections.Counter(MATS[p.material_index] for p in me.polygons),flush=True)
    print('BBOX',[round(min(v.co[i] for v in me.vertices),2) for i in range(3)],[round(max(v.co[i] for v in me.vertices),2) for i in range(3)],flush=True)
    bpy.ops.wm.save_as_mainfile(filepath=D+'/work_geo.blend')

_SR=random.Random(11)
def shrub(x,y,z,r,sq=0.8):
    n0=len(bm.faces); bmesh.ops.create_icosphere(bm,subdivisions=1,radius=r,matrix=Matrix.Translation((x,y,z+r*sq*0.8)))
    fs=newf(n0); vs={v for f in fs for v in f.verts}
    for v in vs:
        d=v.co-Vector((x,y,z+r*sq*0.8)); k=1+_SR.uniform(-0.22,0.22)
        v.co=Vector((x+d.x*k,y+d.y*k,max(z,z+r*sq*0.8+d.z*k*sq)))
    return tag(n0,'Hedge')
def hedge(x0,x1,y0,y1,z,h=0.9):
    L=max(abs(x1-x0),abs(y1-y0)); W=min(abs(x1-x0),abs(y1-y0)); n=max(1,int(L/(W*0.7)))
    for i in range(n+1):
        t=i/max(n,1); x=x0+(x1-x0)*t; y=y0+(y1-y0)*t
        r=W*0.5*_SR.uniform(0.85,1.15); shrub(x+_SR.uniform(-.1,.1),y+_SR.uniform(-.1,.1),z,r,h/(2*r)*_SR.uniform(.85,1.1))

def archwin(F,x,z,w,h,trim='LimeDark',k=12):
    R=w/2; zs=z+h-R
    pts=[(x-R,0.06,z),(x+R,0.06,z)]+[(x+R*math.cos(a),0.06,zs+R*math.sin(a)) for a in np.linspace(0,pi,k+1)]
    pts=[(x-R,0.06,z),(x+R,0.06,z),(x+R,0.06,zs)]+[(x+R*math.cos(a),0.06,zs+R*math.sin(a)) for a in np.linspace(0,pi,k+1)[1:-1]]+[(x-R,0.06,zs)]
    poly(pts,'Win',F)
    t=0.35
    for i in range(k):
        a0,a1=pi*i/k,pi*(i+1)/k
        prism([(x+R*math.cos(a0),zs+R*math.sin(a0)),(x+(R+t)*math.cos(a0),zs+(R+t)*math.sin(a0)),(x+(R+t)*math.cos(a1),zs+(R+t)*math.sin(a1)),(x+R*math.cos(a1),zs+R*math.sin(a1))],0,0.25,trim,F)
    box((x,0.15,zs+R+t-0.1),(0.5,0.3,0.55),trim,F)
    for q in (-1,1): box((x+q*(R+t/2),0.12,z),(t,0.25,h-R),trim,F)
    box((x,0.2,z-0.25),(w+0.9,0.4,0.25),trim,F)
    box((x,0.06,z),(0.08,0.08,h-0.2),'Bronze',F)
    DROPF[0]=True
    for j in range(1,int(h/1.4)): box((x,0.06,z+j*1.4),(w,0.08,0.07),'Bronze',F)
    DROPF[0]=False
