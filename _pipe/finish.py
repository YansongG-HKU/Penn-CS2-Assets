import bpy,bmesh,numpy as np,math,json,os,random
from mathutils import Vector,Matrix
D=os.environ['BD']; S=D+'/src'; A=os.environ['AN']; R=4096; R2=1024
bpy.ops.wm.open_mainfile(filepath=D+'/work_baked.blend')
sc=bpy.context.scene; hi=bpy.data.objects['Bld']; wtmp=bpy.data.objects['WinTmp']
def ld(n): return np.load(S+'/'+n+'.npy').astype(np.float32)
def savepng(name,rgb,a=None,nc=True):
    r=rgb.shape[0]; a=np.ones((r,r,1)) if a is None else a[...,None]
    im=bpy.data.images.new(name,r,r,alpha=True)
    if nc: im.colorspace_settings.name='Non-Color'
    im.pixels.foreach_set(np.concatenate([np.clip(rgb,0,1),a],-1).astype(np.float32).ravel())
    im.filepath_raw=D+'/'+name+'.png'; im.file_format='PNG'; im.save()
def pullpush(a,valid):
    imgs=[a*valid[...,None]]; ws=[valid.astype(np.float32)]
    while imgs[-1].shape[0]>1:
        i=imgs[-1]; w=ws[-1]; h=i.shape[0]//2
        iw=i.reshape(h,2,h,2,-1).sum((1,3)); ww=w.reshape(h,2,h,2).sum((1,3))
        imgs.append(np.where(ww[...,None]>0,iw/np.maximum(ww,1e-6)[...,None],0)); ws.append((ww>0).astype(np.float32))
    out=imgs[-1]
    for k in range(len(imgs)-2,-1,-1):
        up=np.repeat(np.repeat(out,2,0),2,1); w=ws[k][...,None]
        out=np.where(w>0, imgs[k]/np.maximum(w,1e-6) if k>0 else a, up)
    return out
def compose(pf,tag):
    ld0=globals()['ld']; _c=ld0(pf+'col'); _v=(_c.max(-1)>0.004)
    def ldf(n,_v=_v): return pullpush(ld0(n),_v)
    ld_=ldf
    ld=ld_
    col=ld(pf+'col'); ao=ld(pf+'ao')[...,:1]; r=col.shape[0]
    if os.path.exists(S+'/'+pf+'smask.npy'): ao=np.where(ld(pf+'smask')[...,:1]>0.5,1.0,ao)
    savepng(tag+'_BaseColor',col*(0.66+0.34*ao),nc=False); nr=ld(pf+'nrm')
    if os.path.exists(S+'/'+pf+'smask.npy'):
        mk=ld(pf+'smask')[...,:1]>0.5; nr=np.where(mk,np.array([0.5,0.5,1.0],np.float32),nr)
    savepng(tag+'_Normal',nr)
    z=np.zeros((r,r)); savepng(tag+'_MaskMap',np.stack([ld(pf+'metal')[...,0],z,z],-1),1-ld(pf+'rough')[...,0])
    cm=ld(pf+'cm'); cm=(cm>0.5).astype(np.float32); savepng(tag+'_ControlMask',cm,(ld(pf+'snow')[...,0]>0.5).astype(np.float32))
    savepng(tag+'_Emissive',ld(pf+'emit'),nc=False)
compose('b_',A)
# ---------- LOD2: massing + portico silhouette ----------
bm=bmesh.new()
def boxr(x0,x1,y0,y1,z0,z1):
    bmesh.ops.create_cube(bm,size=1,matrix=Matrix.Translation(((x0+x1)/2,(y0+y1)/2,(z0+z1)/2))@Matrix.Diagonal((x1-x0,y1-y0,z1-z0,1)))
def wedge(x0,x1,y0,y1,z0,z1):
    v=[bm.verts.new(p) for p in [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y1,z1),(x1,y1,z1)]]
    for f in [(0,3,2,1),(0,1,5,4),(1,2,5),(0,4,3),(3,4,5,2)]: bm.faces.new([v[i] for i in f])
def cyl(x,y,z,r,h,n): bmesh.ops.create_cone(bm,cap_ends=True,segments=n,radius1=r,radius2=r*0.9,depth=h,matrix=Matrix.Translation((x,y,z+h/2)))
exec(open(D+'/lod2.py').read())
bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
me=bpy.data.meshes.new(A+'_LOD2_Base'); bm.to_mesh(me); bm.free()
lo2=bpy.data.objects.new(A+'_LOD2_Base',me); sc.collection.objects.link(lo2)
bpy.ops.object.select_all(action='DESELECT'); bpy.context.view_layer.objects.active=lo2; lo2.select_set(True)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(60),island_margin=0.004,area_weight=0.0); bpy.ops.uv.pack_islands(rotate=True,margin=0.004)
bpy.ops.object.mode_set(mode='OBJECT')
ml=bpy.data.materials.new('l2bake'); ml.use_nodes=True; me.materials.append(ml)
bn=ml.node_tree.nodes.new('ShaderNodeTexImage'); ml.node_tree.nodes.active=bn
for o in (hi,wtmp): o.select_set(True)
lo2.select_set(True); bpy.context.view_layer.objects.active=lo2
bk=sc.render.bake; bk.use_selected_to_active=True; bk.cage_extrusion=0.6; bk.max_ray_distance=4.0; bk.margin=4
def setemit(kind):
    for m in hi.data.materials:
        pb=m.node_tree.nodes['Principled BSDF']; v=m['metal']; e=list(m['emit']); q=m['snow']; c=list(m['cm'])
        pb.inputs['Emission Color'].default_value={'metal':(v,v,v,1),'emit':(*e,1),'cm':(*c,1),'snow':(q,q,q,1)}.get(kind,(0,0,0,1))
def bake2(t,name,nc=True,**k):
    im=bpy.data.images.new(name,R2,R2)
    if nc: im.colorspace_settings.name='Non-Color'
    bn.image=im; bpy.ops.object.bake(type=t,**k)
    a=np.empty(R2*R2*4,np.float32); im.pixels.foreach_get(a); np.save(S+'/'+name+'.npy',a.reshape(R2,R2,4)[...,:3].astype(np.float16))
sc.cycles.samples=1; setemit('none')
bake2('DIFFUSE','l2_col',False,pass_filter={'COLOR'}); bake2('ROUGHNESS','l2_rough'); bake2('NORMAL','l2_nrm',normal_space='TANGENT')
for kd in ('metal','emit','cm','snow'): setemit(kd); bake2('EMIT','l2_'+kd,kd=='emit')
_rm=float(os.environ.get('LOD2_RMIN','0')); _mm=float(os.environ.get('LOD2_MMAX','1'))
if _rm>0 or _mm<1:
    _r=np.load(S+'/l2_rough.npy').astype(np.float32); np.save(S+'/l2_rough.npy',np.maximum(_r,_rm).astype(np.float16))
    _m=np.load(S+'/l2_metal.npy').astype(np.float32); np.save(S+'/l2_metal.npy',np.minimum(_m,_mm).astype(np.float16)); print('LOD2CLAMP',_rm,_mm,flush=True)
setemit('none'); sc.cycles.samples=16; bk.use_selected_to_active=False; bake2('AO','l2_ao')
compose('l2_',A+'_LOD2')
# ---------- final materials ----------
def final_mat(name,tag):
    m=bpy.data.materials.new(name); m.use_nodes=True; nd=m.node_tree.nodes; L=m.node_tree.links; pb=nd['Principled BSDF']
    def img(suf,nc=True):
        n=nd.new('ShaderNodeTexImage'); n.image=bpy.data.images.load(D+'/'+tag+suf+'.png',check_existing=True)
        if nc: n.image.colorspace_settings.name='Non-Color'
        return n
    c=img('_BaseColor',False); L.new(c.outputs[0],pb.inputs['Base Color'])
    n=img('_Normal'); nm=nd.new('ShaderNodeNormalMap'); L.new(n.outputs[0],nm.inputs['Color']); L.new(nm.outputs[0],pb.inputs['Normal'])
    mk=img('_MaskMap'); sp=nd.new('ShaderNodeSeparateColor'); L.new(mk.outputs[0],sp.inputs[0]); L.new(sp.outputs[0],pb.inputs['Metallic'])
    iv=nd.new('ShaderNodeMath'); iv.operation='SUBTRACT'; iv.inputs[0].default_value=1; L.new(mk.outputs['Alpha'],iv.inputs[1]); L.new(iv.outputs[0],pb.inputs['Roughness'])
    e=img('_Emissive',False); L.new(e.outputs[0],pb.inputs['Emission Color']); pb.inputs['Emission Strength'].default_value=0.0
    return m
def win_mat(name):
    m=bpy.data.materials.new(name); m.use_nodes=True; pb=m.node_tree.nodes['Principled BSDF']
    pb.inputs['Base Color'].default_value=(0.03,0.04,0.05,1); pb.inputs['Roughness'].default_value=0.05; pb.inputs['Metallic'].default_value=0.3
    pb.inputs['Emission Color'].default_value=(1,0.72,0.42,1); pb.inputs['Emission Strength'].default_value=0.0; return m
MB=final_mat(A+'_Base',A); MW=win_mat(A+'_Win'); MG=final_mat(A+'_Gls',A)
names=[m.name for m in hi.data.materials]
def part(src,objname,keep,mat):
    o=src.copy(); o.data=src.data.copy(); o.name=objname; o.data.name=objname; sc.collection.objects.link(o)
    b=bmesh.new(); b.from_mesh(o.data)
    bmesh.ops.delete(b,geom=[f for f in b.faces if names[f.material_index] not in keep],context='FACES')
    for f in b.faces: f.material_index=0
    b.to_mesh(o.data); b.free(); o.data.materials.clear(); o.data.materials.append(mat); return o
base=part(hi,A+'_Base',[n for n in names if n not in('Win','Gls')],MB); gls=part(hi,A+'_Gls',['Gls'],MG)
win=part(wtmp,A+'_Win',['Win'],MW)
for o in (base,gls,win,lo2):
    if 'ScanUV' in o.data.uv_layers: o.data.uv_layers.remove(o.data.uv_layers['ScanUV'])
# CS2 window UV grid (5x5 cells, per CS2-Exporter-for-Blender)
random.seed(3); me=win.data; uvl=me.uv_layers[0].data; polys=list(me.polygons); random.shuffle(polys)
grid=[[[] for _ in range(5)] for _ in range(5)]
for p in polys:
    ci=random.randint(0,24); grid[4-ci//5][ci%5].append(p)
for r in range(5):
    for c in range(5):
        cell=grid[r][c]; n=len(cell)
        if not n: continue
        sub=math.ceil(n**0.5); ss=0.2/sub*0.98; ou=c*0.2+(0.2/sub)*0.01; ov=r*0.2+(0.2/sub)*0.01
        for k,f in enumerate(cell):
            nrm=f.normal.normalized(); tg=-nrm.cross(Vector((0,0,1))); tg=tg.normalized() if tg.length>1e-6 else Vector((1,0,0))
            pts=[Vector((me.vertices[me.loops[i].vertex_index].co.dot(tg),me.vertices[me.loops[i].vertex_index].co.z)) for i in range(f.loop_start,f.loop_start+f.loop_total)]
            mnx=min(q.x for q in pts); mny=min(q.y for q in pts); sx=max(q.x for q in pts)-mnx; sy=max(q.y for q in pts)-mny
            e=ss*0.95; ex,ey=(e,e*sy/sx) if sx>sy else (e*sx/max(sy,1e-9),e)
            u0=ou+(k%sub)*ss+ss*0.025; v0=ov+(k//sub)*ss+ss*0.025
            for j,q in enumerate(pts): uvl[f.loop_start+j].uv=(u0+(q.x-mnx)/max(sx,1e-9)*ex, v0+(q.y-mny)/max(sy,1e-9)*ey)
lo2.data.materials.clear(); lo2.data.materials.append(final_mat(A+'_LOD2_Base',A+'_LOD2'))
bpy.data.objects.remove(hi); bpy.data.objects.remove(wtmp)
# ---------- LOD1: remove tagged micro-detail, dissolve flute valleys, decimate statue only ----------
def cp(o,n):
    c=o.copy(); c.data=o.data.copy(); c.name=n; c.data.name=n; sc.collection.objects.link(c); return c
l1=cp(base,A+'_LOD1_Base'); l1w=cp(win,A+'_LOD1_Win'); l1g=cp(gls,A+'_LOD1_Gls')
for o,mm in ((l1,MB),(l1w,MW),(l1g,MG)): o.data.materials.clear(); o.data.materials.append(mm)
b=bmesh.new(); b.from_mesh(l1.data); dl=b.faces.layers.int['drop']; vl=b.verts.layers.int['valley']
_K=lambda e: frozenset(tuple(round(c,4) for c in v.co) for v in e.verts)
_b0=set(_K(e) for e in b.edges if e.is_boundary)
_df=[f for f in b.faces if f[dl]==1]
if os.environ.get('SAFEDROP'):  # only drop detail whose edges are all shared with other drop faces (no new holes)
    _df=[f for f in _df if all(all(g[dl]==1 for g in e.link_faces) for e in f.edges)]
bmesh.ops.delete(b,geom=_df,context='FACES')
_nb=[e for e in b.edges if e.is_boundary and _K(e) not in _b0]
if _nb: r=bmesh.ops.holes_fill(b,edges=_nb,sides=64); print('HOLEFILL',len(_nb),len(r['faces']),flush=True)
_nb2=[e for e in b.edges if e.is_boundary and _K(e) not in _b0]
if _nb2: r=bmesh.ops.holes_fill(b,edges=_nb2,sides=0); print('HOLEFILL2',len(_nb2),len(r['faces']),flush=True)
_vv=[v for v in b.verts if v[vl]==1]; _tm={}
for v in _vv:
    t=Vector((0,0,1)).cross(v.normal)
    for e in v.link_edges:
        u=e.other_vert(v)
        if u[vl]==0 and abs(u.co.z-v.co.z)<1e-3 and (u.co-v.co).dot(t)>0 and u not in _tm: _tm[v]=u; break
print('BND_PREWELD',sum(e.is_boundary for e in b.edges),flush=True)
bmesh.ops.weld_verts(b,targetmap=_tm); print('WELD',len(_vv),len(_tm),flush=True)
print('BND_POSTWELD',sum(e.is_boundary for e in b.edges),flush=True)
b.to_mesh(l1.data); b.free()
def tris(o): return sum(len(p.vertices)-2 for p in o.data.polygons)
for o in (base,l1,lo2):
    for p in o.data.polygons: p.use_smooth=True
info={o.name:tris(o) for o in (base,win,gls,l1,l1w,l1g,lo2)}
dims={o.name:tuple(round(v,2) for v in o.dimensions) for o in (base,lo2)}; print('TRIS',info,'DIMS',dims,flush=True)
json.dump({'tris':info,'dims':dims},open(S+'/stats.json','w'))
# ---------- export ----------
def exp(objs,fn):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active=objs[0]
    bpy.ops.export_scene.fbx(filepath=fn,use_selection=True,object_types={'MESH'},axis_forward='-Z',axis_up='Y',apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',bake_space_transform=True,use_triangles=True,mesh_smooth_type='FACE',use_tspace=True,path_mode='STRIP',embed_textures=False,add_leaf_bones=False)
exp([base,win,gls],D+'/'+A+'.fbx'); exp([l1,l1w,l1g],D+'/'+A+'_LOD1.fbx'); exp([lo2],D+'/'+A+'_LOD2.fbx')
os.makedirs(D+'/split_fbx',exist_ok=True)
for o,fn in ((base,A),(win,A+'_Win'),(gls,A+'_Gls'),(l1,A+'_LOD1'),(l1w,A+'_LOD1_Win'),(l1g,A+'_LOD1_Gls'),(lo2,A+'_LOD2')): exp([o],D+'/split_fbx/'+fn+'.fbx')
sh={f'{A}_LOD1_{s}.png':f'{A}_{s}.png' for s in ('BaseColor','Normal','MaskMap','ControlMask','Emissive')}
json.dump({'sharedAssets':sh},open(D+'/settings.json','w'),indent=2)
for o in (l1,l1w,l1g): o.location.x=130
lo2.location.x=250
for o in (l1,l1w,l1g,lo2): o.hide_render=True
bpy.ops.wm.save_as_mainfile(filepath=D+'/'+A+'.blend')
