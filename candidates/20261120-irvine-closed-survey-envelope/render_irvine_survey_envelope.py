"""Read exact closed Irvine survey OBJ and compare neutral massing in Blender."""
import bpy,sys,math,collections,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from pathlib import Path
coarse,fine,old,out=map(Path,sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.read_factory_settings(use_empty=True)
def im(p):
 bef=set(bpy.context.scene.objects)
 bpy.ops.wm.obj_import(filepath=str(p),forward_axis='Y',up_axis='Z')
 objs=[x for x in bpy.context.scene.objects if x not in bef and x.type=='MESH']
 o,=objs;return o
def audit(o):
 m=o.data;assert not m.validate(verbose=True,clean_customdata=False)
 fs=[tuple(f.vertices) for f in m.polygons]
 vv=[o.matrix_world@v.co for v in m.vertices]
 edges=collections.defaultdict(list)
 for a,b,c in fs:
  for i,j in ((a,b),(b,c),(c,a)):edges[tuple(sorted((i,j)))].append((i,j))
 assert all(len(v)==2 and v[0]==v[1][::-1] for v in edges.values())
 assert min(f.area for f in m.polygons)>5e-9
 tree=BVHTree.FromPolygons(vv,fs,all_triangles=True,epsilon=1e-8)
 bad=[(i,j) for i,j in tree.overlap(tree) if j>i and set(fs[i]).isdisjoint(fs[j])]
 assert not bad,bad[:20]
 return dict(vertices=len(vv),triangles=len(fs),paired_edges=len(edges),
  disjoint_triangle_intersections=len(bad),min_face_area_m2=min(f.area for f in m.polygons),
  local_extent=[list(map(min,zip(*vv))),list(map(max,zip(*vv)))])
ob=im(coarse); fit=audit(ob); finer=im(fine); check=audit(finer); finer.hide_render=True
assert len(ob.data.polygons)==10964 and len(finer.data.polygons)==40654
(out/'blender-readback.json').write_text(json.dumps({'0.64m':fit,'0.32m':check},indent=2)+'\n'); print('BLENDER_READBACK',fit,check,flush=True)
bef=set(bpy.context.scene.objects);bpy.ops.import_scene.fbx(filepath=str(old),use_image_search=False)
oldobjs=[x for x in bpy.context.scene.objects if x not in bef and x.type=='MESH'];assert oldobjs
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=c;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=c;p.inputs['Roughness'].default_value=.73
 return m
brick=mat('city outline proxy, not facade',(.39,.44,.49,1)); r0=mat('lower returns',(.14,.41,.51,1));r1=mat('upper returns',(.22,.56,.57,1)); prior=mat('old massing only',(.45,.47,.51,1))
for m in (brick,r0,r1):ob.data.materials.append(m)
num=int((out/'roof-face-count.txt').read_text())
for f in ob.data.polygons:
 z=sum(ob.data.vertices[i].co.z for i in f.vertices)/3
 f.material_index=(2 if z>34 else 1) if f.index<num else 0
for o in oldobjs:
 o.data.materials.clear();o.data.materials.append(prior)
 for f in o.data.polygons:f.material_index=0
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=12;sc.cycles.use_denoising=False
sc.render.threads_mode='FIXED';sc.render.threads=2
sc.render.resolution_x=710;sc.render.resolution_y=575;sc.render.resolution_percentage=100
sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
sc.world=bpy.data.worlds.new('Neutral');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.72
def sun(n,amt,e):
 d=bpy.data.lights.new(n,type='SUN');d.energy=amt;d.angle=.08;o=bpy.data.objects.new(n,d);sc.collection.objects.link(o);o.rotation_euler=e
sun('Sun',2.3,(.56,-.49,-.7))
sun('Fill',1.5,(-.64,.44,.4))
c=bpy.data.cameras.new('Same scale diagnostic');c.type='ORTHO';c.ortho_scale=94
cam=bpy.data.objects.new('Model coordinate frame',c);sc.collection.objects.link(cam);sc.camera=cam
for label,p,t in [('street',(66,-99,66),(0,0,26)),('north',(-54,102,62),(0,0,27))]:
 cam.location=Vector(p);cam.rotation_euler=(Vector(t)-cam.location).to_track_quat('-Z','Y').to_euler()
 for tag in ['candidate','old_trial']:
  ob.hide_render=(tag!='candidate')
  for o in oldobjs:o.hide_render=(tag=='candidate')
  sc.render.filepath=str(out/(tag+'-'+label+'.png'));bpy.ops.render.render(write_still=True)

