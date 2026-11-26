"""Blender exact import, orientation/self-intersection QA, and compare old mass vs survey."""
from pathlib import Path
import bpy,sys,collections,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
new,old,out=map(Path,sys.argv[sys.argv.index('--')+1:]);out.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath=str(new),forward_axis='Y',up_axis='Z')
o,=[x for x in bpy.context.scene.objects if x.type=='MESH']
m=o.data; assert not m.validate(verbose=True,clean_customdata=False)
vv=[o.matrix_world@v.co for v in m.vertices]; ff=[tuple(p.vertices) for p in m.polygons]
assert all(len(f)==3 for f in ff) and min(p.area for p in m.polygons)>1e-6
E=collections.defaultdict(list)
for f in ff:
 for a,b in zip(f,f[1:]+f[:1]):E[tuple(sorted((a,b)))].append((a,b))
assert all(len(es)==2 and es[0]==es[1][::-1] for es in E.values())
tree=BVHTree.FromPolygons(vv,ff,all_triangles=True,epsilon=1e-7)
disjoint=[(a,b) for a,b in tree.overlap(tree) if a<b and set(ff[a]).isdisjoint(ff[b])]
assert not disjoint,disjoint
vol=sum(vv[a].dot(vv[b].cross(vv[c])) for a,b,c in ff)/6;assert vol>20000
summary={'candidate':{'verts':len(vv),'tris':len(ff),'oriented_two_face_edges':len(E),'disjoint_intersections':len(disjoint),
  'min_face_area_m2':min(p.area for p in m.polygons),'volume_m3':vol,'xyz_bounds_m':[list(map(op,zip(*vv))) for op in (min,max)]}}
bpy.ops.import_scene.fbx(filepath=str(old),use_image_search=False)
oo,=[x for x in bpy.context.scene.objects if x.type=='MESH' and x is not o]
mm=oo.data; mm.calc_loop_triangles()
vv0=[oo.matrix_world@v.co for v in mm.vertices];assert len(mm.loop_triangles)==52
summary['old_topology_repaired_LOD2']={'verts':len(vv0),'tris':len(mm.loop_triangles),'xyz_bounds_with_lot_plane_m':[list(map(op,zip(*vv0))) for op in (min,max)]}
(out/'blender-readback.json').write_text(json.dumps(summary,indent=2)+'\n')
print('READBACK',summary,flush=True)
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.67
 return m
wall=mat('Wall approximation',(.42,.49,.56))
low=mat('Measured lower roof',(.089,.34,.47))
upper=mat('East upper roof',(.09,.52,.50))
faceold=mat('mid grey',(.46,.47,.48))
for material in (wall,low,upper):m.materials.append(material)
highest=max(z.z for z in vv)
for p in m.polygons:
 p.material_index=(2 if p.normal.z>.9 and p.center.z>24.9 else 1 if p.normal.z>.9 else 0)
mm.materials.clear();mm.materials.append(faceold)
sc=bpy.context.scene;sc.render.engine='CYCLES'
sc.cycles.device='CPU';sc.cycles.use_denoising=False;sc.cycles.samples=18
sc.render.threads_mode='FIXED';sc.render.threads=2;sc.render.resolution_x=970;sc.render.resolution_y=620
sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
sc.world=bpy.data.worlds.new('Background');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.9
bpy.ops.mesh.primitive_plane_add(size=260,location=(0,0,-.01));bpy.context.object.data.materials.append(mat('Neutral sample plane',(.3,.35,.39)))
for nm,rot,e in [('Key',(.28,-.45,-.52),2.15),('Fill',(-.61,.31,.54),.8)]:
 s=bpy.data.lights.new(nm,type='SUN');s.energy=e;s.angle=.16
 ob=bpy.data.objects.new(nm,s);sc.collection.objects.link(ob);ob.rotation_euler=rot
ca=bpy.data.cameras.new('QA');ca.type='ORTHO';ca.ortho_scale=180
co=bpy.data.objects.new('Camera',ca);sc.collection.objects.link(co);sc.camera=co
for n,cam in [('aerial',(4,-73,158)),('south',(30,-198,95))]:
 co.location=cam;co.rotation_euler=(Vector((0,0,10))-co.location).to_track_quat('-Z','Y').to_euler()
 for label in ('old','survey'):
  o.hide_render=label!='survey';oo.hide_render=label!='old'
  if label=='old' and n=='south':continue
  sc.render.filepath=str(out/(n+'-'+label+'.png'));bpy.ops.render.render(write_still=True)
