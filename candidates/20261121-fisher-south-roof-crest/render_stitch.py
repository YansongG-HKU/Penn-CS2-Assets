"""Show exact vended whole shape and standalone strip with an evidence-only material scheme."""
import bpy,sys,json
from pathlib import Path
from mathutils import Vector
d,p=map(lambda x:Path(x).resolve(),sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.read_factory_settings(use_empty=True)
def imp(p):
 o=set(bpy.context.scene.objects);bpy.ops.wm.obj_import(filepath=str(p),forward_axis='Y',up_axis='Z')
 a,=[o0 for o0 in bpy.context.scene.objects if o0 not in o and o0.type=='MESH'];return a
new=imp(d/'Fisher-Fine-Arts-south-strip-corrected-envelope.obj');old=imp(p); st=imp(d/'Fisher-south-raised-roof-strip.obj')
def mat(n,rgb):
 h=bpy.data.materials.new(n);h.diffuse_color=rgb;h.use_nodes=True;pok=h.node_tree.nodes.get('Principled BSDF');pok.inputs['Base Color'].default_value=rgb;pok.inputs['Roughness'].default_value=.76
 return h
g=mat('Unchanged geometry',(.42,.49,.53,1)); h=mat('Repair area highlight',(.07,.41,.52,1)); r=mat('Geometry preview',(.20,.44,.47,1))
N=json.loads((d/'strip-stitch.json').read_text())['retained_exterior_faces']
for o in (new,old,st):
 o.data.materials.clear()
 for m in (g,h,r):o.data.materials.append(m)
 for f in o.data.polygons:f.material_index=2 if o==st else (1 if o==new and f.index>=N else 0)
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=24;sc.cycles.use_denoising=False;sc.render.threads_mode='FIXED';sc.render.threads=2
sc.render.resolution_x=670;sc.render.resolution_y=485;sc.render.resolution_percentage=100;sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
sc.world=bpy.data.worlds.new('Background');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.83
for energy,a in [(2.12,(.63,-.52,-.7)),(.8,(-.51,.35,.63))]:
 l=bpy.data.lights.new('Directional',type='SUN');l.energy=energy;l.angle=.1; lob=bpy.data.objects.new('Directional',l);sc.collection.objects.link(lob);lob.rotation_euler=a
cd=bpy.data.cameras.new('Model QA');cd.type='ORTHO'
cam=bpy.data.objects.new('QA',cd);sc.collection.objects.link(cam);sc.camera=cam
for label,show,T,C,scale in [('stitched-overview',new,(0,0,13),(28,-75,115),87.5),('separate-strip',st,(2,-29.5,16),(24,-40,25),34)]:
 for o in (new,old,st):o.hide_render=(o!=show)
 cd.ortho_scale=scale;cam.location=Vector(C);cam.rotation_euler=(Vector(T)-cam.location).to_track_quat('-Z','Y').to_euler()
 sc.render.filepath=str(d/(label+'.png'));bpy.ops.render.render(write_still=True)
