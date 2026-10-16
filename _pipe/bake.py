import bpy,numpy as np,math,time,sys
from mathutils import Vector
import os
D=os.environ['BD']; S=D+'/src'; os.makedirs(S,exist_ok=True)
RES=int(sys.argv[-1]) if sys.argv[-1].isdigit() else 4096
rng=np.random.default_rng(7)
def fnoise(N,sig,sy=None,seed=0):
    r=np.random.default_rng(seed); f=np.fft.fft2(r.normal(size=(N,N)))
    ky=np.fft.fftfreq(N)[:,None]; kx=np.fft.fftfreq(N)[None,:]; sy=sy or sig
    g=np.exp(-(kx**2)*(sig**2)*20-(ky**2)*(sy**2)*20); n=np.real(np.fft.ifft2(f*g)); return (n-n.mean())/(n.std()+1e-9)
def blocks(N,rows,minw,maxw,bev,seed,cols_fixed=None):
    r=np.random.default_rng(seed); h=np.ones((N,N)); idv=np.zeros((N,N)); rh=N//rows
    yy=np.arange(rh); dy=np.minimum(yy,rh-1-yy)
    for ro in range(rows):
        x=r.integers(0,N) if cols_fixed is None else (ro%2)*cols_fixed//2; ws=[]
        while sum(ws)<N:
            ws.append(cols_fixed if cols_fixed else int(r.integers(minw,maxw)))
        ws[-1]-=sum(ws)-N
        for w in ws:
            if w<=0: continue
            cols=np.arange(x,x+w)%N; xx=np.arange(w); dx=np.minimum(xx,w-1-xx)
            d=np.minimum(dy[:,None],dx[None,:]); h[ro*rh:(ro+1)*rh][:,cols]=np.clip(d/bev,0,1)
            idv[ro*rh:(ro+1)*rh][:,cols]=r.normal(); x+=w
    return h,idv
def save(name,arr,N):
    a=np.clip(arr,0,1)
    if a.ndim==2: a=np.stack([a]*3,-1)
    rgba=np.concatenate([a,np.ones((N,N,1))],-1)[::-1]
    im=bpy.data.images.new(name,N,N); im.pixels.foreach_set(rgba.astype(np.float32).ravel()); im.filepath_raw=S+'/'+name+'.png'; im.file_format='PNG'; im.save(); return im
N=1024
def tex(name,base,var,rows,minw,maxw,bev,seed,joint=0.55,streak=0.0,speck=0.0,cf=None,nz=0.3):
    h,idv=blocks(N,rows,minw,maxw,bev,seed,cf) if rows else (np.ones((N,N)),np.zeros((N,N)))
    n1=fnoise(N,30,seed=seed+1); n2=fnoise(N,3,seed=seed+2); col=np.array(base)[None,None,:]*np.ones((N,N,3))
    m=1+var*idv[...,None]*0.5+nz*(0.06*n1[...,None]+0.03*n2[...,None])
    if streak: m+= -streak*np.clip(fnoise(N,4,60,seed+3),0,None)[...,None]
    if speck: m+= speck*np.random.default_rng(seed).normal(size=(N,N,1))
    col=col*m; col=col*(joint+(1-joint)*np.clip(h*3,0,1))[...,None]
    save(name+'_col',col,N); save(name+'_h',h*0.85+0.15*(0.5+0.1*n2),N)
tex('lime',(0.82,0.76,0.64),0.05,8,190,380,5,1,0.66,0.0,0.01)
tex('limed',(0.81,0.75,0.63),0.035,4,300,700,4,2,0.74,0.0,0.01)
tex('rust',(0.62,0.62,0.61),0.05,5,280,500,14,3,0.6,0.0,0.05)
tex('gran',(0.64,0.64,0.63),0.0,0,1,2,1,4,1,0,0.05)
tex('pave',(0.70,0.69,0.66),0.05,4,0,0,4,5,0.7,0,0.03,cf=256)
def brick(name,base,hdr,seed):
    r=np.random.default_rng(seed); rows=16; rh=N/rows; y=np.arange(N); row=(y//rh).astype(int); fy=(y%rh)
    col=np.zeros((N,N,3)); h=np.zeros((N,N)); U=N/4.0
    for ro in range(rows):
        off=(ro%2)*U*0.375; xs=[]; x=-U+off
        while x<N+U:
            xs.append((x,x+U*0.625,0)); xs.append((x+U*0.625,x+U,1)); x+=U
        ys=slice(int(ro*rh),int((ro+1)*rh)); yy=np.arange(ys.start,ys.stop)-ro*rh; dy=np.minimum(yy,rh-1-yy)
        for (x0,x1,hd) in xs:
            xa=np.arange(int(np.floor(x0)),int(np.floor(x1)))
            if len(xa)==0: continue
            cols=xa%N; dx=np.minimum(xa-x0,x1-1-xa); d=np.minimum(dy[:,None],dx[None,:])
            c=np.array(hdr if hd else base)*(1+0.07*r.normal())
            hh=np.clip(d/3.0,0,1); h[ys][:,cols]=hh; col[ys][:,cols]=c*hh[...,None]+np.array((0.62,0.6,0.56))*(1-hh[...,None])
    n1=fnoise(N,3,seed=seed+2); mc=col.reshape(-1,3).mean(0); col=0.85*mc[None,None,:]+0.15*col; col=col*(1+0.03*fnoise(N,40,seed=seed+5)[...,None]); h=0.6+0.4*h; save(name+'_col',col,N); save(name+'_h',h*0.85+0.15*(0.5+0.1*n1),N)
_bc=tuple(float(x) for x in os.environ.get('BRICKCOL','0.36,0.17,0.10').split(','))
brick('brick',_bc,tuple(c*0.55 for c in _bc),21)
tex('iron',tuple(float(x) for x in os.environ.get('IRONCOL','0.035,0.035,0.035').split(',')),0.0,0,1,2,1,22,1,0,0.02)
tex('copper',(0.22,0.42,0.34),0.0,0,1,2,1,23,1,0,0.08)
tex('dome',(0.70,0.70,0.68),0.03,10,200,420,4,6,0.78,0.0,0.01)
tex('roof',tuple(float(x) for x in os.environ.get('ROOFCOL','0.20,0.26,0.24').split(',')),0.02,1,0,0,5,7,0.8,0,0.02,cf=128)
tex('bronze',(0.24,0.16,0.09),0.0,0,1,2,1,8,1,0,0.03)
tex('leaf',(0.10,0.20,0.06),0.0,0,1,2,1,24,1,0,0.30,nz=1.2)
tex('lawn',(0.20,0.33,0.12),0.0,0,1,2,1,9,1,0,0.25)
tex('carve',tuple(float(x) for x in os.environ.get('CARVECOL','0.55,0.50,0.42').split(',')),0.0,0,1,2,1,10,1,0,0.04)
tex('lampt',(0.95,0.93,0.86),0.0,0,1,2,1,11,1,0,0.0)
tex('glass',(0.06,0.08,0.10),0.0,0,1,2,1,12,1,0,0.02)
bpy.ops.wm.open_mainfile(filepath=D+'/work_geo.blend')
ob=bpy.data.objects['Bld']
# name: tile, tile size m, rough, metal, emit, bumpstr
P={'Limestone':('lime',4.8,.85,0,None,.5),'LimeDark':('limed',4.8,.8,0,None,.4),'Rustic':('rust',4.8,.7,0,None,1.0),
'Granite':('gran',3,.55,0,None,.2),'Paving':('pave',4.8,.8,0,None,.6),'Dome':('dome',4.8,.75,0,None,.5),'Roof':('roof',4.8,.5,.4,None,.4),
'Bronze':('bronze',2,.45,.85,None,.1),'Lawn':('lawn',2,.95,0,None,.3),'Hedge':('leaf',0.8,.9,0,None,1.2),'Brick':('brick',1.28,.85,0,None,.8),'Iron':('iron',2,.5,float(os.environ.get('IRONMET','.7')),None,.1),'Copper':('copper',2,.6,.3,None,.2),'Carve':('carve',2,.9,0,None,.1),'Lamp':('lampt',2,.3,0,(1,.85,.6),0),
'Statue':('bronze',1,.65,.2,None,.1),'Win':('glass',2,.08,0,(1,.72,.42),0),'Gls':('glass',2,.08,0,(1,.8,.55),0)}
for m in ob.data.materials:
    t,sz,ro,me,em,bs=P[m.name]; m.use_nodes=True; nt=m.node_tree; nd=nt.nodes; L=nt.links
    pb=nd['Principled BSDF']; tc=nd.new('ShaderNodeTexCoord'); mp=nd.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value=(1/sz,)*3
    L.new(tc.outputs['Object'],mp.inputs['Vector'])
    ic=nd.new('ShaderNodeTexImage'); ic.image=bpy.data.images.load(S+'/'+t+'_col.png'); ic.projection='BOX'; ic.projection_blend=0.15
    ih=nd.new('ShaderNodeTexImage'); ih.image=bpy.data.images.load(S+'/'+t+'_h.png'); ih.image.colorspace_settings.name='Non-Color'; ih.projection='BOX'; ih.projection_blend=0.15
    for i in (ic,ih): L.new(mp.outputs[0],i.inputs[0])
    L.new(ic.outputs[0],pb.inputs['Base Color']); bu=nd.new('ShaderNodeBump'); bu.inputs['Strength'].default_value=bs; bu.inputs['Distance'].default_value=0.03
    L.new(ih.outputs[0],bu.inputs['Height']); L.new(bu.outputs[0],pb.inputs['Normal'])
    pb.inputs['Roughness'].default_value=ro; pb.inputs['Metallic'].default_value=me; pb.inputs['Emission Strength'].default_value=1.0
    if m.name=='Statue':
        uvn=nd.new('ShaderNodeUVMap'); uvn.uv_map='ScanUV'; at=nd.new('ShaderNodeAttribute'); at.attribute_name='scantex'
        ims=[]
        for k in range(3):
            t_=nd.new('ShaderNodeTexImage'); t_.image=bpy.data.images.load(D+f'/alma_src/textures/texture{k}_{k}.jpeg'); L.new(uvn.outputs[0],t_.inputs[0]); ims.append(t_)
        c1=nd.new('ShaderNodeMath'); c1.operation='GREATER_THAN'; c1.inputs[1].default_value=0.5; L.new(at.outputs['Fac'],c1.inputs[0])
        c2=nd.new('ShaderNodeMath'); c2.operation='GREATER_THAN'; c2.inputs[1].default_value=1.5; L.new(at.outputs['Fac'],c2.inputs[0])
        m1=nd.new('ShaderNodeMix'); m1.data_type='RGBA'; L.new(c1.outputs[0],m1.inputs[0]); L.new(ims[0].outputs[0],m1.inputs[6]); L.new(ims[1].outputs[0],m1.inputs[7])
        m2=nd.new('ShaderNodeMix'); m2.data_type='RGBA'; L.new(c2.outputs[0],m2.inputs[0]); L.new(m1.outputs[2],m2.inputs[6]); L.new(ims[2].outputs[0],m2.inputs[7])
        bw=nd.new('ShaderNodeRGBToBW'); L.new(m2.outputs[2],bw.inputs[0])
        rp=nd.new('ShaderNodeValToRGB'); e=rp.color_ramp.elements
        e[0].position=0.0; e[0].color=(0.04,0.026,0.014,1); e[1].position=0.45; e[1].color=(0.13,0.085,0.04,1)
        L.new(bw.outputs[0],rp.inputs[0])
        nz=nd.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value=7; nz.inputs['Detail'].default_value=6
        mr=nd.new('ShaderNodeMapRange'); L.new(nz.outputs[0],mr.inputs[0]); mr.inputs[1].default_value=0.66; mr.inputs[2].default_value=0.8; mr.inputs[4].default_value=0.22
        mx=nd.new('ShaderNodeMix'); mx.data_type='RGBA'; L.new(mr.outputs[0],mx.inputs[0]); L.new(rp.outputs[0],mx.inputs[6]); mx.inputs[7].default_value=(0.09,0.17,0.13,1)
        gp=nd.new('ShaderNodeNewGeometry'); pr=nd.new('ShaderNodeValToRGB'); q=pr.color_ramp.elements
        q[0].position=0.40; q[0].color=(0.035,0.023,0.012,1); q[1].position=0.60; q[1].color=(0.11,0.072,0.034,1)
        L.new(gp.outputs['Pointiness'],pr.inputs[0]); L.new(pr.outputs[0],pb.inputs['Base Color'])
    m['emit']=em or (0,0,0); m['metal']=me
    CM={'Limestone':(1,0,0),'LimeDark':(1,0,0),'Carve':(1,0,0),'Dome':(1,0,0),'Brick':(0,1,0),'Rustic':(0,1,0),'Granite':(0,1,0),'Paving':(0,1,0),'Roof':(0,0,1)}
    m['cm']=CM.get(m.name,(0,0,0)); m['snow']=0.0 if m.name in ('Roof','Paving','Lawn','Dome','Granite') else 1.0
ob.data.uv_layers.active=ob.data.uv_layers['UVMap']
# split Win out (CS2 window grid UVs later, not in atlas)
import bmesh
names=[m.name for m in ob.data.materials]
wi=names.index('Win')
win=ob.copy(); win.data=ob.data.copy(); win.name='WinTmp'; bpy.context.scene.collection.objects.link(win)
for o,keep in ((ob,False),(win,True)):
    b=bmesh.new(); b.from_mesh(o.data); bmesh.ops.delete(b,geom=[f for f in b.faces if (f.material_index==wi)!=keep],context='FACES'); b.to_mesh(o.data); b.free()
# smooth shading with sharp edges > 35 deg
b=bmesh.new(); b.from_mesh(ob.data)
for f in b.faces: f.smooth=True
for e in b.edges:
    stf=[f for f in e.link_faces if names[f.material_index]=='Statue']
    e.smooth = (len(e.link_faces)==2 and e.calc_face_angle(3.14)<math.radians(60)) if (stf and len(stf)==len(e.link_faces)) else not (len(e.link_faces)!=2 or e.calc_face_angle(3.14)>math.radians(35))
b.to_mesh(ob.data); b.free()
# UV: smart project non-preUV faces, normalize to metres, priority scale, pack
pre=ob.data.attributes['preuv'].data
bpy.context.view_layer.objects.active=ob; ob.select_set(True)
for k,p_ in enumerate(ob.data.polygons): p_.select=(pre[k].value==0)
bpy.ops.object.mode_set(mode='EDIT'); bpy.context.tool_settings.mesh_select_mode=(False,False,True)
t0=time.time(); bpy.ops.object.mode_set(mode='OBJECT')
_sel=[p_.select for p_ in ob.data.polygons]
for _mi in range(len(ob.data.materials)):
    for k,p_ in enumerate(ob.data.polygons): p_.select=_sel[k] and p_.material_index==_mi
    if not any(p_.select for p_ in ob.data.polygons): continue
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.uv.smart_project(angle_limit=math.radians(60),island_margin=0.001,area_weight=0.0,correct_aspect=True,scale_to_bounds=False); bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.object.mode_set(mode='OBJECT'); print('SMART',time.time()-t0,flush=True)
b=bmesh.new(); b.from_mesh(ob.data); uv=b.loops.layers.uv['UVMap']; pl=b.faces.layers.int['preuv']
def uva(f):
    l=f.loops; a=0.0
    for k in range(1,len(l)-1):
        p0,p1,p2=l[0][uv].uv,l[k][uv].uv,l[k+1][uv].uv; a+=abs((p1-p0).cross(p2-p0))/2
    return a
KK={}
for _mi in range(len(names)):
    A3=sum(f.calc_area() for f in b.faces if f[pl]==0 and f.material_index==_mi); A2=sum(uva(f) for f in b.faces if f[pl]==0 and f.material_index==_mi); KK[_mi]=math.sqrt(A3/max(A2,1e-9))
PR={'Statue':3.0,'Limestone':1.3,'LimeDark':1.2,'Carve':1.2,'Dome':0.8,'Bronze':1.0,'Lamp':0.5,'Rustic':0.7,'Granite':0.45,'Paving':0.22,'Lawn':0.2,'Hedge':0.6,'Roof':0.3,'Gls':0.6,'Brick':0.55,'Iron':0.8,'Copper':0.8}
for f in b.faces:
    sc_=PR[names[f.material_index]]*(KK[f.material_index] if f[pl]==0 else 1.0)
    for l in f.loops: l[uv].uv=l[uv].uv*sc_
b.to_mesh(ob.data); b.free()
SI=names.index('Statue') if 'Statue' in names else -99; t0=time.time()
def packsel(isstat,margin,smart=False):
    for p_ in ob.data.polygons: p_.select=((p_.material_index==SI)==isstat)
    bpy.ops.object.mode_set(mode='EDIT')
    if smart: bpy.ops.uv.smart_project(angle_limit=math.radians(70),island_margin=0.02,area_weight=0.0,scale_to_bounds=True)
    bpy.ops.uv.select_all(action='SELECT')
    bpy.ops.uv.pack_islands(udim_source='CLOSEST_UDIM',rotate=True,margin=margin,shape_method='CONVEX')
    bpy.ops.object.mode_set(mode='OBJECT')
HAS_ST=any(p_.material_index==SI for p_ in ob.data.polygons)
if HAS_ST: packsel(True,0.008,True)
packsel(False,0.0015)
b=bmesh.new(); b.from_mesh(ob.data); uv=b.loops.layers.uv['UVMap']
for f in b.faces:
    st_=f.material_index==SI
    for l in f.loops:
        u,v=l[uv].uv
        l[uv].uv=((0.885+0.11*u) if st_ else (0.875*u if HAS_ST else u), v)
b.to_mesh(ob.data); b.free()
print('PACK',time.time()-t0,flush=True)
b=bmesh.new(); b.from_mesh(ob.data); uv=b.loops.layers.uv['UVMap']
def uva2(f):
    l=f.loops; a=0.0
    for k in range(1,len(l)-1):
        p0,p1,p2=l[0][uv].uv,l[k][uv].uv,l[k+1][uv].uv; a+=abs((p1-p0).cross(p2-p0))/2
    return a
TH=(1.5/RES)**2; bad=[f for f in b.faces if uva2(f)<TH]; fixed=0
for f in bad:
    for lp in f.loops:
        for f2 in lp.vert.link_faces:
            if f2 is f or uva2(f2)<TH: continue
            c=sum((l2[uv].uv for l2 in f2.loops),Vector((0,0)))/len(f2.loops)
            for l3 in f.loops: l3[uv].uv=c.copy()
            fixed+=1; break
        else: continue
        break
print('DEGEN',len(bad),'fixed',fixed,flush=True)
# audit: thin sliver faces (<2.5 px wide in UV) of uniform-colour materials (sashes, mullions, door panels, lamps) bleed the
# neighbouring island's colour (white/pale lines on dark bronze). Collapse their UVs onto the centre of the largest island face of the same material.
UNI=[n for n in ('Bronze','Iron','Copper','Lamp','Carve') if n in names]
def _w(f):
    a=uva2(f); L=max(((f.loops[i][uv].uv-f.loops[i-1][uv].uv).length for i in range(len(f.loops))),default=0)
    return (2 if len(f.loops)==3 else 1)*a/max(L,1e-12)*RES
_anc={}
for f in b.faces:
    n=names[f.material_index]
    if n in UNI:
        a=uva2(f)
        if a>_anc.get(n,(0,None))[0]: _anc[n]=(a,f)
thin=0
for f in b.faces:
    n=names[f.material_index]
    if n in UNI and n in _anc and f is not _anc[n][1] and _w(f)<2.5:
        af=_anc[n][1]; c=sum((l2[uv].uv for l2 in af.loops),Vector((0,0)))/len(af.loops)
        for l3 in f.loops: l3[uv].uv=c.copy()
        thin+=1
print('THIN collapsed',thin,flush=True)
b.to_mesh(ob.data); b.free()
ob.data.uv_layers[0].name='UVMap'
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.render.threads_mode='FIXED'; sc.render.threads=8
sc.render.bake.margin=3; sc.render.bake.margin_type='EXTEND'
def target(name,noncolor=True,res=RES):
    im=bpy.data.images.new(name,res,res,alpha=False)
    if noncolor: im.colorspace_settings.name='Non-Color'
    for m in ob.data.materials:
        n=m.node_tree.nodes.get('BAKE') or m.node_tree.nodes.new('ShaderNodeTexImage'); n.name='BAKE'; n.image=im; m.node_tree.nodes.active=n
    return im
def setemit(kind):
    for m in ob.data.materials:
        pb=m.node_tree.nodes['Principled BSDF']; v=m['metal']; e=list(m['emit'])
        q=m['snow']; c=list(m['cm'])
        pb.inputs['Emission Color'].default_value={'metal':(v,v,v,1),'emit':(*e,1),'cm':(*c,1),'snow':(q,q,q,1),'smask':((1,1,1,1) if m.name=='Statue' else (0,0,0,1))}.get(kind,(0,0,0,1))
def bake(t,name,nc=True,**k):
    im=target(name,nc); t0=time.time(); bpy.ops.object.bake(type=t,**k); print('BAKED',name,time.time()-t0,flush=True)
    a=np.empty(RES*RES*4,np.float32); im.pixels.foreach_get(a); np.save(S+'/'+name+'.npy',a.reshape(RES,RES,4)[...,:3].astype(np.float16))
win.select_set(False); ob.select_set(True); bpy.context.view_layer.objects.active=ob
setemit('none'); sc.cycles.samples=1
sc.cycles.samples=int(os.environ.get('BAKE_AA','12')); bake('DIFFUSE','b_col',False,pass_filter={'COLOR'})
bake('ROUGHNESS','b_rough')
bake('NORMAL','b_nrm',normal_space='TANGENT'); sc.cycles.samples=1
setemit('metal'); bake('EMIT','b_metal'); setemit('emit'); bake('EMIT','b_emit',False); setemit('cm'); bake('EMIT','b_cm'); setemit('snow'); bake('EMIT','b_snow'); setemit('smask'); bake('EMIT','b_smask'); setemit('none')
sc.cycles.samples=24; sc.world=bpy.data.worlds.new('w') if not sc.world else sc.world
bake('AO','b_ao')
bpy.ops.wm.save_as_mainfile(filepath=D+'/work_baked.blend')
