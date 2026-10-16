import bpy,bmesh,numpy as np,math,os,sys,json
from mathutils import Vector
D=os.environ['BD']; A=os.environ['AN']; OUT=D+'/lodcheck'; os.makedirs(OUT,exist_ok=True)
sc=bpy.context.scene
def stats(o):
    b=bmesh.new(); b.from_mesh(o.data); b.verts.ensure_lookup_table()
    bnd=sum(1 for e in b.edges if e.is_boundary); nm=sum(1 for e in b.edges if len(e.link_faces)>2)
    zero=sum(1 for f in b.faces if f.calc_area()<1e-7); loose=sum(1 for v in b.verts if not v.link_faces)
    wind=0
    for e in b.edges:
        if len(e.link_faces)==2:
            l1,l2=e.link_loops
            if l1.vert==l2.vert: wind+=1
    # components
    comp=[-1]*len(b.verts); nc=0
    for v in b.verts:
        if comp[v.index]>=0: continue
        st=[v]; comp[v.index]=nc
        while st:
            x=st.pop()
            for e in x.link_edges:
                y=e.other_vert(x)
                if comp[y.index]<0: comp[y.index]=nc; st.append(y)
        nc+=1
    co=np.array([v.co[:] for v in b.verts]); cid=np.array(comp)
    mn=np.full((nc,3),1e9); mx=np.full((nc,3),-1e9)
    np.minimum.at(mn,cid,co); np.maximum.at(mx,cid,co)
    # closed comps with negative volume -> flipped
    vol=np.zeros(nc); closed=np.ones(nc,bool)
    for e in b.edges:
        if e.is_boundary or len(e.link_faces)>2: closed[cid[e.verts[0].index]]=False
    for f in b.faces:
        p=[l.vert.co for l in f.loops]
        for k in range(1,len(p)-1): vol[cid[f.loops[0].vert.index]]+=p[0].dot(p[k].cross(p[k+1]))/6
    flipped=int(((vol<-1e-6)&closed).sum())
    e=0.05; floating=0
    for i in range(nc):
        ov=np.all((mn-e<=mx[i])&(mx+e>=mn[i]),axis=1); ov[i]=False
        if not ov.any(): floating+=1
    b.free()
    return dict(tris=sum(len(p.vertices)-2 for p in o.data.polygons),boundary_edges=bnd,nonmanifold_edges=nm,zero_area=zero,loose_verts=loose,bad_winding=wind,components=nc,flipped_closed=flipped,floating=floating)
groups={'LOD0':[A+'_Base',A+'_Win',A+'_Gls'],'LOD1':[A+'_LOD1_Base',A+'_LOD1_Win',A+'_LOD1_Gls'],'LOD2':[A+'_LOD2_Base']}
res={}
for g,ns in groups.items():
    for n in ns:
        o=bpy.data.objects.get(n)
        if o and len(o.data.polygons): res[n]=stats(o)
json.dump(res,open(OUT+'/mesh_checks.json','w'),indent=1); print('CHECKS',json.dumps(res),flush=True)
if 'nostat' in sys.argv: pass
# ---- renders ----
for g,ns in groups.items():
    for n in ns:
        o=bpy.data.objects.get(n)
        if o: o.location.x=0
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=16; sc.cycles.use_denoising=True
sc.render.resolution_x=640; sc.render.resolution_y=400; sc.render.threads_mode='FIXED'; sc.render.threads=8
sc.view_settings.view_transform='AgX'; sc.view_settings.exposure=-1.3
w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; nt=w.node_tree; sky=nt.nodes.new('ShaderNodeTexSky'); sky.sky_type='NISHITA'; sky.sun_elevation=math.radians(35); sky.sun_rotation=math.radians(200)
nt.links.new(sky.outputs[0],nt.nodes['Background'].inputs[0]); nt.nodes['Background'].inputs[1].default_value=0.35
for o in sc.objects:
    if o.type=='MESH' and o.name not in sum(groups.values(),[]): o.hide_render=True
bpy.ops.mesh.primitive_plane_add(size=2000,location=(0,0,-0.08)); gp=bpy.context.object
cam=bpy.data.objects.new('cam',bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera=cam
o0=bpy.data.objects[A+'_Base']; dx,dy,dz=o0.dimensions; S=max(dx,dy)
views={'front':((-0.25*S,-1.25*S,0.35*S),35),'back':((0.25*S,1.25*S,0.35*S),35),'aerial':((0.9*S,-0.9*S,1.0*S),35)}
dist={'LOD0':1.0,'LOD1':1.0,'LOD2':1.0}
files={}
for vn,(loc,lens) in views.items():
    for g,ns in groups.items():
        for g2,ns2 in groups.items():
            for n in ns2:
                o=bpy.data.objects.get(n)
                if o: o.hide_render=(g2!=g)
        L=Vector(loc)*dist[g]; tgt=Vector((0,0,dz*0.35)); cam.location=L+tgt*0; cam.data.lens=lens
        cam.rotation_euler=(tgt-L).to_track_quat('-Z','Y').to_euler()
        f=f'{OUT}/_{vn}_{g}.png'; sc.render.filepath=f; bpy.ops.render.render(write_still=True); files[(vn,g)]=f
# composite
for vn in views:
    ims=[]
    for g in groups:
        im=bpy.data.images.load(files[(vn,g)]); a=np.array(im.pixels[:]).reshape(400,640,4); ims.append(a)
    row=np.concatenate(ims,1); W=row.shape[1]
    out=bpy.data.images.new('c',W,400,alpha=True); out.pixels.foreach_set(row.ravel().astype(np.float32)); out.filepath_raw=f'{D}/lod_compare_{vn}.png'; out.file_format='PNG'; out.save()
print('LODDONE',flush=True)
