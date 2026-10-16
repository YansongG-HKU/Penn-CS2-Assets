import bpy,math,sys
from mathutils import Vector
import os,json
D=os.environ['BD']; A=os.environ['AN']; CF=json.load(open(D+'/cams.json'))
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=int(sys.argv[-1]); sc.cycles.use_denoising=True
sc.render.resolution_x=1280; sc.render.resolution_y=720; sc.render.threads_mode='FIXED'; sc.render.threads=8
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'; sc.view_settings.exposure=-1.3
def gm(n,c,r):
    m=bpy.data.materials.new(n); m.use_nodes=True; p=m.node_tree.nodes['Principled BSDF']; p.inputs['Base Color'].default_value=(*c,1); p.inputs['Roughness'].default_value=r; return m
LX,LY=CF['lot']
for (x0,x1,y0,y1,z,mat) in [(-400,400,-400,400,-0.06,gm('grass',(0.05,0.11,0.03),0.95)),(-300,300,-LY-14,-LY-2,-0.04,gm('road',(0.06,0.06,0.065),0.9)),(-300,300,-LY-2,-LY,-0.03,gm('walk',(0.35,0.33,0.30),0.8))]:
    bpy.ops.mesh.primitive_plane_add(location=((x0+x1)/2,(y0+y1)/2,z)); o=bpy.context.object; o.scale=((x1-x0)/2,(y1-y0)/2,1); o.data.materials.append(mat)
w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; nt=w.node_tree; sky=nt.nodes.new('ShaderNodeTexSky'); sky.sky_type='NISHITA'
nt.links.new(sky.outputs[0],nt.nodes['Background'].inputs[0])
def setsun(elev,az,strength,sky_str):
    sky.sun_elevation=math.radians(elev); sky.sun_rotation=math.radians(az); sky.sun_size=math.radians(1.0); nt.nodes['Background'].inputs[1].default_value=sky_str
bpy.ops.object.camera_add(); cam=bpy.context.object; sc.camera=cam
def shot(name,loc,tgt,lens):
    cam.location=loc; cam.data.lens=lens; cam.rotation_euler=(Vector(tgt)-Vector(loc)).to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=D+'/'+name; bpy.ops.render.render(write_still=True)
setsun(32,200,1,0.35)
for n,(loc,tgt,lens) in CF['day'].items(): shot(n,loc,tgt,lens)
setsun(-6,200,1,0.02); sc.view_settings.exposure=0.0
for n in (A+'_Base',A+'_Win',A+'_Gls'): bpy.data.materials[n].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=6.0
bpy.ops.object.light_add(type='SUN',rotation=(math.radians(35),0,math.radians(150))); l=bpy.context.object.data; l.energy=0.06; l.color=(0.6,0.7,1.0)
for (loc,rot,en,sz) in CF['nightlights']:
    bpy.ops.object.light_add(type='AREA',location=loc,rotation=[math.radians(a) for a in rot]); a=bpy.context.object.data; a.energy=en; a.size=sz; a.color=(1,0.85,0.65)
loc,tgt,lens=CF['night']; shot('render_04_night.png',loc,tgt,lens)
