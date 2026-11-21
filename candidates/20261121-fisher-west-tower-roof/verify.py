"""Reimport the tower slice; measure held rays and optional isolated visible opening."""
import bpy,collections,sys,math,json,statistics,hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from pathlib import Path
d,legacy=(Path(a).resolve() for a in sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.read_factory_settings(use_empty=True)
def imp(p):
 s=set(bpy.context.scene.objects)
 bpy.ops.wm.obj_import(filepath=str(p),forward_axis='Y',up_axis='Z')
 o,=[o for o in bpy.context.scene.objects if o not in s and o.type=='MESH'];return o
ob=imp(d/'Fisher-west-tower-crown-geometry.obj')
base=imp(legacy)
def mesh(o):
 m=o.data
 v=[o.matrix_world@p.co for p in m.vertices];f=[tuple(p.vertices) for p in m.polygons]
 assert all(len(p)==3 for p in f)
 return v,f,BVHTree.FromPolygons(v,f,all_triangles=True,epsilon=1.e-7)
v,f,t=mesh(ob);_,_,t0=mesh(base)
E=collections.defaultdict(list)
for a in f:
 for x,y in zip(a,a[1:]+a[:1]):E[min(x,y),max(x,y)].append((x,y))
assert all(len(a)==2 and a[0]==a[1][::-1] for a in E.values())
bad=[(i,j) for i,j in t.overlap(t) if i<j and set(f[i]).isdisjoint(f[j])]
assert not bad and len(v)==510 and len(f)==1020 and len(E)==1530
vol=sum(v[i].dot(v[j].cross(v[k])) for i,j,k in f)/6
assert 160<vol<390,vol
cal=json.loads((d/'calibration.json').read_text()); fit=json.loads((d/'build.json').read_text()); a=math.radians(cal['rotation_local_deg'])
def xy(u,v):
 return (u*math.cos(a)-v*math.sin(a),u*math.sin(a)+v*math.cos(a))
def check_line(tr,u,v):
 x,y=xy(u,v); q=tr.ray_cast(Vector((x,y,100)),Vector((0,0,-1)))[0];return None if q is None else q.z+17.1
def compare(rows):
 vals=[]; prior=[]; g0=[]
 for x,y,z in rows:
  u=check_line(t,x,y); p=check_line(t0,x,y)
  if u is not None: vals.append(abs(u-z));prior.append(abs(p-z));g0.append(u)
 assert len(vals)>5
 quant=lambda a:[statistics.median(a),statistics.quantiles(a,n=100,method='inclusive')[89],statistics.quantiles(a,n=100,method='inclusive')[94]]
 return {'in_n':len(rows),'matched_new_ray_n':len(vals),'old_abs_p50_p90_p95_on_matched_subset':quant(prior),'new_abs_p50_p90_p95_on_matched_subset':quant(vals),'min_max_new_return_navd88':(min(g0),max(g0))}
samples=json.loads((d/'held-tower.json').read_text())
core=compare(samples['roof']);assert core['matched_new_ray_n']==417 and core['new_abs_p50_p90_p95_on_matched_subset'][1]<.15
high=compare(samples['upper'])
lower=compare([l for a in samples['lower'].values() for l in a])
p=fit['upper_cap_hole_extents_xy_in_rotated_frame']
assert check_line(t,(p[0]+p[1])/2,(p[2]+p[3])/2) is None
native={'distinct_vertices':len(v),'triangles':len(f),'paired_edges':len(E),'non_adjacent_pairs':len(bad),'signed_volume_isolated_reference_m3':vol,
'provisional_through_cut_ray_passed':True,'gated_inner_roof_holdout':core,
'upper_filtered_height_holdout':high,'lower_crest_filtered_height_holdout':lower,'materials_only_for_reference':[m.name for m in ob.data.materials]}
(d/'blender-readback.json').write_text(json.dumps(native,indent=2)+'\n');print(json.dumps(native),flush=True)
base.hide_render=True
for X in ob.data.materials:
 X.use_nodes=True; p=X.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.75
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=29;sc.cycles.use_denoising=False
sc.render.threads_mode='FIXED';sc.render.threads=2;sc.render.resolution_x=680;sc.render.resolution_y=455;sc.render.resolution_percentage=100
sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA';sc.world=bpy.data.worlds.new('Neutral');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
for en,e in [(2.0,(.58,-.53,-.5)),(1.1,(-.55,.28,.72))]:
 l=bpy.data.lights.new('Sun','SUN');l.energy=en;l.angle=.1; lo=bpy.data.objects.new('Sun',l);sc.collection.objects.link(lo);lo.rotation_euler=e
cc=bpy.data.cameras.new('Camera');cc.type='ORTHO';cc.ortho_scale=19.
co=bpy.data.objects.new('Roof study',cc);sc.collection.objects.link(co);sc.camera=co
T=Vector((-9.5,7.1,29.2))
for k,p in [('west',(-22,15,12)),('aerial',(-13,-6,32))]:
 cc.ortho_scale=22.5 if k=='west' else 25.0
 co.location=T+Vector(p);co.rotation_euler=(T-co.location).to_track_quat('-Z','Y').to_euler()
 sc.render.filepath=str(d/(k+'.png'));bpy.ops.render.render(write_still=True)
# Export a self-contained inspection GLB; the OBJ/MTL is the evidence geometry.
bpy.ops.object.select_all(action='DESELECT');ob.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(d/'Fisher-west-tower-crown-review.glb'),export_format='GLB',use_selection=True,export_animations=False,export_cameras=False,export_lights=False)
