"""Independent Blender readback: closed envelope and correction of upper turret, plus conditioned legacy comparison."""
import bpy,sys,math,collections,json,hashlib,statistics
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
uncorrected,final,old,out=map(Path,sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.read_factory_settings(use_empty=True)
def imp(p):
 previous=set(bpy.context.scene.objects)
 bpy.ops.wm.obj_import(filepath=str(p.resolve()),forward_axis='Y',up_axis='Z')
 o,=[o for o in bpy.context.scene.objects if o not in previous and o.type=='MESH']
 return o
def mesh(o):
 m=o.data
 assert not m.validate(verbose=True,clean_customdata=False)
 vv=[o.matrix_world@v.co for v in m.vertices]
 m.calc_loop_triangles(); ff=[tuple(f.vertices) for f in m.loop_triangles]
 return vv,ff,BVHTree.FromPolygons(vv,ff,all_triangles=True,epsilon=1.e-7)
def audit(o):
 vv,ff,t=mesh(o); E=collections.defaultdict(list)
 for f in ff:
  for x,y in zip(f,f[1:]+f[:1]):E[tuple(sorted((x,y)))].append((x,y))
 assert min(f.area for f in o.data.polygons)>1e-8
 assert all(len(es)==2 and es[0]==es[1][::-1] for es in E.values())
 bad=[(i,j) for i,j in t.overlap(t) if j>i and set(ff[i]).isdisjoint(ff[j])]
 assert not bad,bad[:12]
 vol=sum(vv[i].dot(vv[j].cross(vv[k])) for i,j,k in ff)/6
 assert vol>20000
 return vv,ff,t,{'verts':len(vv),'tris':len(ff),'oriented_two_face_edges':len(E),'non_adjacent_triangle_pairs':0,
  'volume_m3_shell_with_synthetic_base_not_building_volume':vol,
  'bounds':[list(map(min,zip(*vv))),list(map(max,zip(*vv)))], 'min_face_area':min(f.area for f in o.data.polygons)}
ou=imp(uncorrected); ob=imp(final)
A,U,UT,rs=audit(ou); B,V,VT,rf=audit(ob)
assert U==V and len(A)==len(B)==9510
moved=[(i,(q-p).z) for i,(p,q) in enumerate(zip(A,B)) if (q-p).length>1e-6]
assert len(moved)==21 and all((A[i]-B[i]).xy.length<1.e-6 and dz>0 for i,dz in moved)
bef=set(bpy.context.scene.objects)
bpy.ops.import_scene.fbx(filepath=str(old.resolve()),use_image_search=False)
oldobj,=[o for o in bpy.context.scene.objects if o not in bef and o.type=='MESH']
# Old footprint dimensions have the long direction in X and semicircular geometry to the negative X side.
# Rotate -90 degrees to put the apse north. The bounding platform is centered on the City outline bbox only.
oldobj.rotation_euler.z-=math.pi/2
bpy.context.view_layer.update()
OV,OF,OT=mesh(oldobj)
assert len(OF)==336
qs=lambda a:[statistics.median(a),statistics.quantiles(a,n=100,method='inclusive')[89],statistics.quantiles(a,n=100,method='inclusive')[94]]
ls=[];old_valid=[];both_valid=[];detail=[]
for l in (out/'held-sample-local.csv').read_text().splitlines():
 x,y,z=map(float,l.split(',')); org=Vector((x,y,100)); down=Vector((0,0,-1))
 a,b,c=[t.ray_cast(org,down)[0] for t in (UT,VT,OT)]
 assert a is not None and b is not None
 errs=[abs(s.z-z) for s in (a,b)];ls.append(errs)
 if z+17.1>=48:detail.append(errs)
 if c is not None and c.z>2:old_valid.append(abs(c.z-z)); both_valid.append(errs[1])
assert len(ls)==25605 and len(detail)==86
u,v=map(qs,zip(*ls)); d,e=map(qs,zip(*detail));assert e[0]<.2 and e[1]<3.
textures={}
for tag in ['BaseColor','Normal','MaskMap','Emissive','ControlMask']:
 p=old.with_name(old.stem+'_'+tag+'.png').resolve(); im=bpy.data.images.load(str(p),check_existing=False)
 assert im.pixels[0]>=0
 textures[tag]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'dimensions':tuple(im.size)}
data={'legacy_repo_lod2_tag_and_sha256':{'triangles':len(OF),'sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'unchanged_retrieved_texture_maps':textures},
 'legacy_pose_note':'Diagnostic rotation, apse north; central horizontal and fixed z datum, not a game import or exact pose registration.',
 'legacy_comparison':{'valid_lidar_interior_hits_above_ground':len(old_valid),'old_abs_p50_p90_p95_m':qs(old_valid),'new_same_hit_subset_abs_p50_p90_p95_m':qs(both_valid)},
 'original_survey_shell':rs,'final_survey_shell':rf,
 'roof_holdout_all':{'points':len(ls),'initial_abs_p50_p90_p95_m':u,'final_abs_p50_p90_p95_m':v},
 'roof_holdout_above_48_navd88':{'points':len(detail),'initial_abs_p50_p90_p95_m':d,'final_abs_p50_p90_p95_m':e},
 'moved_upper_turret_vertices':len(moved)}
(out/'blender-readback.json').write_text(json.dumps(data,indent=2)+'\n'); print('VERIFIED_SHELL',data,flush=True)
def mat(n,c,r=.71):
 m=bpy.data.materials.new(n);m.diffuse_color=c;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=c;p.inputs['Roughness'].default_value=r
 return m
ob.data.materials.clear()
for m in [mat('City wall outline placeholder',(.44,.44,.42,1)),mat('Roof survey low tier',(.18,.34,.44,1)),
          mat('Roof survey high tier',(.30,.47,.46,1)),mat('Upper North-West turret survey crest',(.82,.41,.18,1))]:
 ob.data.materials.append(m)
num=int((out/'roof-face-count.txt').read_text())
for p in ob.data.polygons:
 x,y,z=p.center
 p.material_index=0 if p.index>=num else 3 if z>31.3 and -11.5<x<-7.5 and 10.5<y<15 else 2 if z>15.5 else 1
oldobj.data.materials.clear();oldobj.data.materials.append(mat('Old geometry silhouette only',(.43,.46,.49,1)))
for p in oldobj.data.polygons:p.material_index=0
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=15;sc.cycles.use_denoising=False
sc.render.threads_mode='FIXED';sc.render.threads=2
sc.render.resolution_x=645;sc.render.resolution_y=525;sc.render.resolution_percentage=100
sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
sc.world=bpy.data.worlds.new('Neutral');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.75
def sun(n,amt,e):
 d=bpy.data.lights.new(n,type='SUN');d.energy=amt;d.angle=.06;o=bpy.data.objects.new(n,d);sc.collection.objects.link(o);o.rotation_euler=e
sun('Main',2.3,(.55,-.63,-.6));sun('Fill',1.05,(-.55,.57,.5))
cam_data=bpy.data.cameras.new('Isometric survey comparison');cam_data.type='ORTHO';cam_data.ortho_scale=85.
c=bpy.data.objects.new('Comparison Camera',cam_data);sc.collection.objects.link(c);sc.camera=c;ou.hide_render=True
for way,C in [('west',(-98,65,63)),('roof',(-38,26,131))]:
 c.location=Vector(C);c.rotation_euler=(Vector((0,0,13))-c.location).to_track_quat('-Z','Y').to_euler()
 for k,show,hide in [('survey',ob,oldobj),('legacy',oldobj,ob)]:
  show.hide_render=False; hide.hide_render=True
  sc.render.filepath=str(out/(f'{k}-{way}.png'));bpy.ops.render.render(write_still=True)
