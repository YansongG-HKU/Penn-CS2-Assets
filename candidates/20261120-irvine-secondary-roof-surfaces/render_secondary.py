"""Reimport exact secondary components and render them against the pinned central roof."""
from pathlib import Path
import bpy,collections,json,sys
from mathutils import Vector
sec,central,out=map(Path,sys.argv[sys.argv.index('--')+1:]);out.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath=str(sec),forward_axis='Y',up_axis='Z')
objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
assert len(objects)==6
summary={}
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=c;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=c;p.inputs['Roughness'].default_value=.73
 return m
M=[mat('New surveyed inset decks',(.12,.51,.43,1)),mat('New surveyed outer slate geometry',(.14,.35,.61,1)),
   mat('Previously fitted main roof',(.36,.41,.47,1))]
for o in objects:
 m=o.data
 assert not m.validate(verbose=True,clean_customdata=False)
 e=collections.defaultdict(list)
 for f in m.polygons:
  assert f.normal.z>0.25 and f.area>0
  x=list(f.vertices); assert len(x)==3
  for j,k in zip(x,x[1:]+x[:1]):e[tuple(sorted((j,k)))].append((j,k))
 assert all(len(x)==1 or (len(x)==2 and x[0]==x[1][::-1]) for x in e.values())
 m.materials.append(M['hip' in o.name]); summary[o.name]={'vertices':len(m.vertices),'faces':len(m.polygons),'boundary':sum(len(v)==1 for v in e.values()),'two_face_edges':sum(len(v)==2 for v in e.values())}
bpy.ops.wm.obj_import(filepath=str(central),forward_axis='Y',up_axis='Z')
main,=[o for o in bpy.context.scene.objects if o.type=='MESH' and o not in objects]
assert len(main.data.polygons)==64
main.data.materials.append(M[2])
# Verify it really has the same local XY frame and expected height separation.
W=lambda o:[o.matrix_world@v.co for v in o.data.vertices]
assert max(max(abs(p.x),abs(p.y)) for p in W(main))<8.9
assert min(p.z for p in W(main))>37 and all(max(p.z for p in W(o))<29 for o in objects)
(out/'blender-readback.json').write_text(json.dumps(summary,indent=2)+'\n')
print('BLENDER_COMPONENT_READBACK',json.dumps(summary),flush=True)
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=12;sc.cycles.use_denoising=False
sc.render.threads_mode='FIXED';sc.render.threads=2
sc.render.resolution_x=750;sc.render.resolution_y=540;sc.render.resolution_percentage=100
sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
sc.world=bpy.data.worlds.new('Neutral');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.75
sun=bpy.data.lights.new('Top Sun',type='SUN');sun.energy=2.6;u=bpy.data.objects.new('Top Sun',sun);sc.collection.objects.link(u);u.rotation_euler=(.55,-.48,-.7)
c=bpy.data.cameras.new('Model coordinate frame');c.type='ORTHO';c.ortho_scale=60
cam=bpy.data.objects.new('Model coordinate frame',c);sc.collection.objects.link(cam);sc.camera=cam
for label,campos in {'oblique':(46,-75,78),'plan':(0,0,105)}.items():
 aim=Vector((0,-3,32)) if label=='oblique' else Vector((0,-6,25))
 cam.location=Vector(campos if label=='oblique' else (0,-6,105))
 cam.rotation_euler=(aim-cam.location).to_track_quat('-Z','Y').to_euler()
 sc.render.filepath=str(out/(label+'.png'));bpy.ops.render.render(write_still=True)

