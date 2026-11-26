import bpy,sys,collections,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
old,new,d=map(Path,sys.argv[sys.argv.index('--')+1:]); d.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
def load(path):
 b=set(bpy.context.scene.objects)
 bpy.ops.wm.obj_import(filepath=str(path),forward_axis='Y',up_axis='Z')
 o,=[x for x in bpy.context.scene.objects if x not in b and x.type=='MESH']
 return o
def check(o):
 m=o.data;assert not m.validate()
 V=[o.matrix_world@v.co for v in m.vertices];F=[tuple(p.vertices) for p in m.polygons]
 E=collections.defaultdict(list)
 assert all(len(f)==3 for f in F) and min(p.area for p in m.polygons)>1e-6
 for f in F:
  for i,j in zip(f,f[1:]+f[:1]):E[tuple(sorted((i,j)))].append((i,j))
 assert all(len(p)==2 and p[0]==p[1][::-1] for p in E.values())
 tree=BVHTree.FromPolygons(V,F,all_triangles=True,epsilon=1e-7)
 bad=[(a,b) for a,b in tree.overlap(tree) if a<b and set(F[a]).isdisjoint(F[b])]
 assert not bad,bad[:5]
 return dict(verts=len(V),triangles=len(F),oriented_edges=len(E),nonadjacent_triangle_intersections=len(bad),min_face_area_m2=min(x.area for x in m.polygons),
  bounds=[list(map(x,zip(*V))) for x in (min,max)])
a,b=load(old),load(new)
ra,rb=check(a),check(b)
assert ra['bounds']==rb['bounds'] and rb['triangles']>ra['triangles']
(d/'blender-readback.json').write_text(json.dumps({'old_survey':ra,'raised_surface_candidate':rb},indent=2)+'\n')
def mat(n,col):
 m=bpy.data.materials.new(n);m.diffuse_color=(*col,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=.63
 return m
wall=mat('Walls not detailed',(.43,.46,.50)); low=mat('Base roof zones',(.085,.31,.39)); hi=mat('Previously measured cap',(.12,.45,.51)); change=mat('Seven added surveyed roof surfaces',(.83,.46,.15))
for o in (a,b):
 for m in (wall,low,hi,change):o.data.materials.append(m)
 for p in o.data.polygons:
  zz=p.center.z+19.331369165057666
  p.material_index=(3 if o==b and p.normal.z>.9 and p.center.x>9.5 and 46.31<zz<46.89 else 2 if p.normal.z>.9 and zz>43.3 else 1 if p.normal.z>.9 else 0)
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.use_denoising=False;sc.cycles.samples=22;sc.render.threads_mode='FIXED';sc.render.threads=2
sc.render.resolution_x=950;sc.render.resolution_y=630;sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
sc.world=bpy.data.worlds.new('Moderate studio');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.75
for n,e,r in [('Key',2.2,(.35,-.43,-.59)),('Fill',.85,(-.55,.40,.64))]:
 l=bpy.data.lights.new(n,'SUN');l.energy=e;l.angle=.17;o=bpy.data.objects.new(n,l);sc.collection.objects.link(o);o.rotation_euler=r
cam=bpy.data.cameras.new('Matched scale');cam.type='ORTHO';cam.ortho_scale=67
co=bpy.data.objects.new('Camera',cam);sc.collection.objects.link(co);sc.camera=co
co.location=Vector((37,-26,109));co.rotation_euler=(Vector((34,0,24))-co.location).to_track_quat('-Z','Y').to_euler()
for tag,obj in [('east-old',a),('east-refined',b)]:
 a.hide_render=a!=obj;b.hide_render=b!=obj
 sc.render.filepath=str(d/(tag+'.png'));bpy.ops.render.render(write_still=True)
