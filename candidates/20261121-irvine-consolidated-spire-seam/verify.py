"""Clean exact readback: local buried opposed caps, winding, UV, normals, silhouette-ray parity."""
from pathlib import Path
import bpy,sys,collections,json,math,hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
old,new,report,render=(Path(x).resolve() for x in sys.argv[sys.argv.index('--')+1:])
R={}
def load(p,expected):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False)
 o,=[x for x in bpy.context.scene.objects if x.type=='MESH'];m=o.data; m.calc_loop_triangles()
 assert not m.validate(verbose=True,clean_customdata=False)
 v=[o.matrix_world @ k.co for k in m.vertices]
 A=[];F=[tuple(q.vertices) for q in m.loop_triangles]
 assert len(F)==expected
 for f in m.polygons:
  A.append((tuple(tuple(v[i]) for i in f.vertices),tuple(tuple(m.uv_layers.active.data[i].uv) for i in f.loop_indices),
   tuple(tuple((o.matrix_world.to_3x3()@m.corner_normals[i].vector).normalized()) for i in f.loop_indices),f.use_smooth,f.material_index))
 caps=[i for i,f in enumerate(A) if all(abs(w[2]-40.5)<9e-6 for w in f[0])]
 E=collections.defaultdict(list)
 for f in F:
  for i,j in zip(f,f[1:]+f[:1]):E[min(i,j),max(i,j)].append((i,j))
 if expected==96:
  assert len(E)==144 and all(len(x)==2 and x[0]==x[1][::-1] for x in E.values()) and not caps
 else: assert caps==[36,41]
 ims={}
 for im in bpy.data.images:
  if im.source!='FILE':continue
  x=Path(bpy.path.abspath(im.filepath)).resolve();assert x.parent==p.parent.parent.parent/'textures' and x.is_file(),x
  im.reload(); assert len(im.pixels)>0 and list(im.size)==[1024]*2
  ims[x.name]=hashlib.sha256(x.read_bytes()).hexdigest()
 assert set(ims)==set(p.stem+'_'+k+'.png' for k in ('BaseColor','Normal','Emissive'))
 return o,v,F,A,caps,ims
a,v,f,A,ac,ai=load(old,108);B0=BVHTree.FromPolygons(v,f,all_triangles=True)
a,v1,f1,A1,bc,bi=load(new,96);B1=BVHTree.FromPolygons(v1,f1,all_triangles=True)
assert [x for i,x in enumerate(A) if i not in ac]==A1 and ai==bi
extent=lambda v:[tuple(map(k,zip(*v))) for k in (min,max)]
assert extent(v)==extent(v1); results={}
def hit(T,o,d):
 return T.ray_cast(o,d,400)[0]
outside_max=0.; num=0
for k,source in enumerate(((1,0,0),(0,1,0),(0,0,1),(1,-1,.28),(-.7,-1,.61))):
 d=Vector(source).normalized(); X=d.cross(Vector((0,0,1)))
 if X.length<.01:X=Vector((1,0,0))
 X.normalize();Y=d.cross(X).normalized()
 Z=Vector((0,0,25)); n=0
 for i in range(-26,27):
  for j in range(-25,26):
   start=Z+X*(i*1.78+.117)+Y*(j*1.67+.093)+d*170
   f0=hit(B0,start,-d); f1=hit(B1,start,-d)
   assert (f0 is None)==(f1 is None)
   if f0 is not None:
    delta=(f0-f1).length; assert delta<.00004, (k,delta);outside_max=max(outside_max,delta);n+=1
 results[str(k)]=n;num+=(53*51)
inner={}
for k,z,axis in [('lower_inside',40.49,(0,0,1)),('upper_inside',40.51,(0,0,-1))]:
 oldhits=[];newhits=[]
 for i in range(-6,7):
  for j in range(-6,7):
   xy=(i*.109+.002,j*.109+.003,z)
   s=hit(B0,Vector(xy),Vector(axis));t=hit(B1,Vector(xy),Vector(axis)); assert s and t
   assert abs(s.z-40.5)<.00004 and abs(t.z-40.5)>.75
   oldhits.append(s.z);newhits.append(t.z)
 inner[k]={'sample_count':len(oldhits),'old_hit_z_range':[min(oldhits),max(oldhits)],'new_hit_z_range':[min(newhits),max(newhits)]}
report.write_text(json.dumps({'bounding_box_m':extent(v),'mesh_raw_108_to_96_reread':True,'retained_polygons_exact':40,'closed_oriented_tri_edges':144,
 'seam_z_m':40.5,'missing_coplanar_polygons_after':0,'ordinal_silhouette_hit_samples_per_view':results,'outside_ray_trials':num,
 'max_first_surface_shift_m':outside_max,'exposed_images_same':bi,'interior_rays':inner},indent=2)+'\n')
if __import__("os").environ.get("NO_RENDER")=="1": raise SystemExit(0)
# One reference image from exact post-repair mesh, original baked color only.
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=7;sc.cycles.use_denoising=False
sc.render.threads_mode='FIXED';sc.render.threads=2;sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
sc.render.resolution_x=630;sc.render.resolution_y=535;sc.render.resolution_percentage=100
sc.view_settings.view_transform='Standard'
mat=bpy.data.materials.new('diagnostic original color');mat.use_nodes=True;N=mat.node_tree.nodes;N.clear()
t=N.new('ShaderNodeTexImage');t.image=next(i for i in bpy.data.images if i.filepath.endswith('BaseColor.png'))
e=N.new('ShaderNodeEmission');o=N.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(t.outputs['Color'],e.inputs[0]);mat.node_tree.links.new(e.outputs[0],o.inputs[0]);a.data.materials[0]=mat
cam0=bpy.data.cameras.new('fixed camera');cam0.type='ORTHO';cam0.ortho_scale=94
cam=bpy.data.objects.new('fixed camera',cam0);sc.collection.objects.link(cam);sc.camera=cam
cam.location=(100,-138,69);q=Vector((0,0,24));cam.rotation_euler=(q-cam.location).to_track_quat('-Z','Y').to_euler()
sc.render.filepath=str(render);bpy.ops.render.render(write_still=True)
print(report.read_text())
