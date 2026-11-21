"""Independent Blender OBJ readback and common-frame before/after roof massing."""
from pathlib import Path
import collections,json,sys
import bpy
from mathutils import Vector
new,old,out=map(Path,sys.argv[sys.argv.index('--')+1:]);out.mkdir()
def load(which):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 if which=='measured':
  bpy.ops.wm.obj_import(filepath=str(new),forward_axis='Y',up_axis='Z')
  o,=[o for o in bpy.context.scene.objects if o.type=='MESH']
  m=o.data;coords=[o.matrix_world@v.co for v in m.vertices]; E=collections.defaultdict(list)
  for f in m.polygons:
   a=list(f.vertices); assert len(a)==3
   for x,y in zip(a,a[1:]+a[:1]):E[tuple(sorted((x,y)))].append((x,y))
  assert len(coords)==34 and len(m.polygons)==64 and len(E)==96
  assert all(len(p)==2 and p[0]==p[1][::-1] for p in E.values())
  assert min(x.z for x in coords)>37.5 and max(x.z for x in coords)<51
  print('OBJ READBACK',len(coords),len(E),len(m.polygons),flush=True)
  return o
 bpy.ops.import_scene.fbx(filepath=str(old),use_image_search=False)
 o,=[o for o in bpy.context.scene.objects if o.type=='MESH']
 v=[tuple(o.matrix_world@v.co) for v in o.data.vertices]; F=[]
 for f in o.data.polygons:
  ids=list(f.vertices);A=[v[i][2] for i in ids]
  if min(A)>28.999 and 40.49<max(A)<40.51:F.append(ids)
 assert len(F)==16, len(F)
 lo=sorted({i for f in F for i in f});lut={j:i for i,j in enumerate(lo)}
 m=bpy.data.meshes.new('previous roof only');m.from_pydata([v[i] for i in lo],[],[[lut[i] for i in f] for f in F]);m.update()
 b=bpy.data.objects.new('previous roof only',m);bpy.context.scene.collection.objects.link(b);o.hide_render=True
 return b
def material(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=c;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=c;p.inputs['Roughness'].default_value=.68
 return m
for which in ('previous','measured'):
 o=load(which);sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=12;sc.cycles.use_denoising=False
 sc.render.threads_mode='FIXED';sc.render.threads=2
 sc.render.resolution_x=600;sc.render.resolution_y=420;sc.render.resolution_percentage=100
 sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
 a=material('Roof neutral',(0.20,.25,.32,1));o.data.materials.clear();o.data.materials.append(a)
 if which=='measured':
  b=material('Lower hidden cap / diagnostic',(0.16,.17,.20,1));o.data.materials.append(b)
  for f in o.data.polygons:f.material_index=int(f.index>=32)
 world=bpy.data.worlds.new('Daylight reference');sc.world=world;world.use_nodes=True
 world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.64
 sun=bpy.data.lights.new('Top Sun',type='SUN');sun.energy=2.5;u=bpy.data.objects.new('Top Sun',sun);sc.collection.objects.link(u);u.rotation_euler=(.53,-.66,-.35)
 c=bpy.data.cameras.new('Common orthographic frame');c.type='ORTHO';c.ortho_scale=54
 cam=bpy.data.objects.new('Common orthographic frame',c);sc.collection.objects.link(cam);sc.camera=cam
 for label,campos in {'three-quarter':(55,-70,75),'high':(22,-36,115)}.items():
  aim=Vector((0,0,39));cam.location=Vector(campos);cam.rotation_euler=(aim-cam.location).to_track_quat('-Z','Y').to_euler()
  sc.render.filepath=str(out/(which+'-'+label+'.png'));bpy.ops.render.render(write_still=True)
