"""Independent Blender readback with closed topology, ray/UV comparisons, actual color render."""
from pathlib import Path
import bpy,sys,collections,json,math,hashlib,os
from mathutils import Vector
from mathutils.bvhtree import BVHTree
old,new,report,render=(Path(x).resolve() for x in sys.argv[sys.argv.index('--')+1:])
def load(p,want):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False)
 o,=[x for x in bpy.context.scene.objects if x.type=='MESH'];m=o.data;m.calc_loop_triangles()
 assert not m.validate(verbose=True,clean_customdata=False)
 v=[o.matrix_world@k.co for k in m.vertices]
 uv=[m.uv_layers.active.data[i].uv.copy() for i in range(len(m.loops))]
 N=[(o.matrix_world.to_3x3()@m.corner_normals[i].vector).normalized() for i in range(len(m.loops))]
 F=[tuple(t.vertices) for t in m.loop_triangles]; UL=[tuple(uv[i] for i in t.loops) for t in m.loop_triangles]
 A=[([tuple(v[i]) for i in f.vertices], [list(uv[i]) for i in f.loop_indices],[list(N[i]) for i in f.loop_indices],f.use_smooth,f.material_index) for f in m.polygons]
 E=collections.defaultdict(list)
 for a in F:
  for i,j in zip(a,a[1:]+a[:1]):E[min(i,j),max(i,j)].append((i,j))
 assert len(F)==want
 if want==52:
  assert len(E)==78 and all(len(v)==2 and v[0]==v[1][::-1] for v in E.values())
 ims={}
 for im in bpy.data.images:
  if im.source=='FILE':
   x=Path(bpy.path.abspath(im.filepath)).resolve();assert x.parent==(p.parent.parent.parent/'textures' if p.parent.name=='split' else p.parent) and x.is_file(),x
   im.reload(); assert len(im.pixels)>0 and list(im.size)==[1024]*2
   ims[x.name]=hashlib.sha256(x.read_bytes()).hexdigest()
 assert len(ims)==3
 return o,v,F,UL,A,ims
a,v,f,u,A,ai=load(old,48);B0=BVHTree.FromPolygons(v,f,all_triangles=True)
a,w,g,uu,AA,bi=load(new,52);B1=BVHTree.FromPolygons(w,g,all_triangles=True)
ext=lambda v:[tuple(map(q,zip(*v))) for q in (min,max)]
assert ext(v)==ext(w) and ai==bi and len(AA)==26
D=[x for i,x in enumerate(A) if i not in {5,10,11,16,17,22}]
assert len(D)==18 and all(a[1:]==b[1:] for a,b in zip(D,AA[:18]))
corner_shift=max(math.dist(x,y) for a,b in zip(D,AA[:18]) for x,y in zip(a[0],b[0]))
assert corner_shift<=6e-6
def pull(B,V,F,U,origin,dir):
 q,_,i,_=B.ray_cast(origin,dir,500.)
 if q is None:return q,None
 f=F[i];a,b,c=[V[k] for k in f]; sub=lambda u,v:tuple(float(i)-float(j) for i,j in zip(u,v));ab=sub(b,a);ac=sub(c,a);ap=sub(q,a)
 # Compute in double precision without accumulating Vector single-precision dot roundoff on skinny triangles.
 dot=lambda a,b:sum(float(x)*float(y) for x,y in zip(a,b))
 A,B,C=dot(ab,ab),dot(ab,ac),dot(ac,ac);D,E=dot(ap,ab),dot(ap,ac)
 d=A*C-B*B;assert d>0
 s=(C*D-B*E)/d;t=(A*E-B*D)/d
 row=U[i]
 uv=tuple(float(row[0][j])*(1-s-t)+float(row[1][j])*s+float(row[2][j])*t for j in (0,1))
 return q,uv
def cmp(o,d):
 p,tu=pull(B0,v,f,u,o,d);q,tv=pull(B1,w,g,uu,o,d)
 assert (p is None)==(q is None)
 if p is None:return None
 return math.dist(p,q),math.dist(tu,tv)
out=[]; stats={}
for ss in [(1,0,0),(0,1,0),(0,0,1),(1,-1,.28),(-.7,-1,.61)]:
 d=Vector(ss).normalized();H=d.cross(Vector((0,0,1)))
 if H.length<.01:H=Vector((1,0,0))
 H.normalize();Q=d.cross(H).normalized()
 C=Vector((0,0,14))
 trial=[]
 for i in range(-40,41):
  for j in range(-40,41):
   z=C+d*215+H*(i*2.10+.123)+Q*(j*1.43+.357)
   h0=cmp(z,-d)
   if h0 is not None:trial.append(h0)
 out.extend(trial);stats[str(ss)]={'hits':len(trial),'trials':81*81}
# Confirm visible ledges independently with dense systematic samples of the original top-side field.
ledges={}
for Z,ext0,ext1 in [(0,(-72,72,-24,24),(-68,68,-16,18)),(22,(-68,68,-16,18),(-66.5,66.5,-15,17))]:
 xa,xb,ya,yb=ext0;xa1,xb1,ya1,yb1=ext1
 ray=[]
 for i in range(145):
  for j in range(115):
   X=xa+(i+.319)/145*(xb-xa);Y=ya+(j+.169)/115*(yb-ya)
   if X<xa1-.005 or X>xb1+.005 or Y<ya1-.005 or Y>yb1+.005:
    z=Vector((X,Y,Z+.2));d=Vector((0,0,-1))
    p,_=pull(B0,v,f,u,z,d);assert p and abs(p.z-Z)<3e-5
    ray.append(cmp(z,d))
 assert all(x is not None for x in ray)
 ledges[str(Z)]={'samples':len(ray),'max_xyz_m':max(x for x,y in ray),'max_UV_norm':max(y for x,y in ray)}
max_shift=max(x for x,y in out); maxuv=max(y for x,y in out)
assert max_shift<.00009 and maxuv<.00005,(max_shift,maxuv)
assert max(x['max_UV_norm'] for x in ledges.values())<.000004,ledges
inside={}
for z in (-.025,4.77,21.9):
 p0,p1=[],[]
 for x in range(-60,61,10):
  for y in range(-12,13,3):
   p=Vector((x+.13,y+.31,z));d=Vector((0,0,1))
   a0,_=pull(B0,v,f,u,p,d);a1,_=pull(B1,w,g,uu,p,d);assert a0 and a1
   assert abs(a1.z-28)<2e-5
   p0.append(a0.z);p1.append(a1.z)
 inside[str(z)]={'samples':len(p0),'before':[min(p0),max(p0)],'after':[min(p1),max(p1)]}
planes={str(z):{k:[w[0] for w in ff if max(abs(t[2]-z) for t in w[0])<1e-5] for k,ff in [('before',A),('after',AA)]} for z in (0,4.8,22)}
report.write_text(json.dumps({'body_count_old_new':[48,52],'triangulated_pair_edges':78,'aabb_m':ext(w),
 'visible_ray_results':stats,'visible_ray_max_shift_m':max_shift,'visible_ray_max_uv_delta':maxuv,'retained_18_corner_max_shift_m':corner_shift,
 'ledge_results':ledges,'interior_first_obstruction':inside,'reread_polygons_on_planes':planes,'original_images_sha256':bi},indent=2)+'\n')
print('READBACK',max_shift,maxuv,ledges,inside)
if os.environ.get('NO_RENDER')=='1':raise SystemExit(0)
# Use the same baked color on the exact rebuilt FBX; not a game or PBR render.
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=7;sc.cycles.use_denoising=False
sc.render.threads_mode='FIXED';sc.render.threads=2;sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
sc.render.resolution_x=690;sc.render.resolution_y=465;sc.render.resolution_percentage=100;sc.view_settings.view_transform='Standard'
mat=bpy.data.materials.new('color only');mat.use_nodes=True;N=mat.node_tree.nodes;N.clear()
t=N.new('ShaderNodeTexImage');t.image=next(i for i in bpy.data.images if i.filepath.endswith('BaseColor.png'))
e=N.new('ShaderNodeEmission');o=N.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(t.outputs['Color'],e.inputs[0]);mat.node_tree.links.new(e.outputs[0],o.inputs[0]);a.data.materials[0]=mat
ca=bpy.data.cameras.new('fixed');ca.type='ORTHO';ca.ortho_scale=160;c=bpy.data.objects.new('fixed',ca);sc.collection.objects.link(c);sc.camera=c;c.location=(75,-147,91)
c.rotation_euler=(Vector((0,0,12))-c.location).to_track_quat('-Z','Y').to_euler()
sc.render.filepath=str(render);bpy.ops.render.render(write_still=True)
