"""Read stitched full survey shell independently, compare exact retained faces and independent site rays."""
import sys,collections,statistics,math,csv,json,hashlib,bpy
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
D,prior=map(lambda x:Path(x).resolve(),sys.argv[sys.argv.index('--')+1:])
new=D/'Fisher-Fine-Arts-south-strip-corrected-envelope.obj'
bpy.ops.wm.read_factory_settings(use_empty=True)
def load(f):
 s=set(bpy.context.scene.objects)
 bpy.ops.wm.obj_import(filepath=str(f),forward_axis='Y',up_axis='Z')
 o,=[o for o in bpy.context.scene.objects if o not in s and o.type=='MESH'];m=o.data
 assert not m.validate(verbose=True,clean_customdata=False)
 v=[o.matrix_world@q.co for q in m.vertices]
 ts=[tuple(f.vertices) for f in m.polygons];E=collections.defaultdict(list)
 for f in ts:
  assert len(f)==3
  for a,b in zip(f,f[1:]+f[:1]):E[min(a,b),max(a,b)].append((a,b))
 assert all(len(r)==2 and r[0]==r[1][::-1] for r in E.values())
 T=BVHTree.FromPolygons(v,ts,all_triangles=True,epsilon=0)
 hit=[(i,j) for i,j in T.overlap(T) if i<j and set(ts[i]).isdisjoint(ts[j])]
 assert not hit,hit[:15]
 assert min(t.area for t in m.polygons)>1e-9
 return o,v,ts,T,len(E),[list(map(min,zip(*v))),list(map(max,zip(*v)))]
a,v0,f0,old,e0,b0=load(prior);b,v1,f1,trial,e1,b1=load(new)
step=json.loads((D/'strip-stitch.json').read_text());lo,hi=step['bbox_min_max']; N=step['retained_exterior_faces']
assert b0==b1
def fkeys(v,t):return tuple(tuple(v[i]) for i in t)
# Independently reconstruct preserved rows using the original exact grid membership and pin their vertices.
nrf=int((prior.parent/'roof-face-count.txt').read_text())
orig=[fkeys(v0,r) for j,r in enumerate(f0) if j>=nrf or not all(lo[0]-.000003<=v0[i].x<=hi[0]+.000003 and lo[1]-.000003<=v0[i].y<=hi[1]+.000003 for i in r)]
assert len(orig)==N==18808,(len(orig),N)
assert all(v==fkeys(v1,r) for v,r in zip(orig,f1[:N])) # all vertices bit-exact in Blender float coordinates outside replaced list
before_after=collections.defaultdict(list)
def val(t,x,y):
 h=t.ray_cast(Vector((x,y,100)),Vector((0,0,-1)))[0]
 assert h is not None
 return h.z
def inside(x,y): return lo[0]<=x<=hi[0] and lo[1]<=y<=hi[1]
O=[]
plane=[]
for row in (prior.parent/'held-sample-local.csv').read_text().splitlines():
 x,y,z=map(float,row.split(','))
 z0=val(old,x,y);z1=val(trial,x,y)
 if not inside(x,y):O.append(abs(z0-z1))
 before_after['all_25605'].append((abs(z-z0),abs(z-z1)))
 if inside(x,y):before_after['all_inside_patch'].append((abs(z-z0),abs(z-z1)))
for r in csv.DictReader((D/'strip-held.csv').open()):
 x,y,z=map(float,(r['x'],r['y'],r['z_local']))
 q0,q1=val(old,x,y),val(trial,x,y)
 before_after['measured_strip_subregions'].append((abs(z-q0),abs(z-q1)))
 before_after[r['part']].append((abs(z-q0),abs(z-q1)))
Q=lambda a:[statistics.median(a),statistics.quantiles(a,n=100,method='inclusive')[89],statistics.quantiles(a,n=100,method='inclusive')[94]]
out={k:{'n':len(v),'old_p50_p90_p95_abs_m':Q([a for a,b in v]),'new_p50_p90_p95_abs_m':Q([b for a,b in v])} for k,v in before_after.items()}
res={'before_mesh_v_f_e':[len(v0),len(f0),e0],'new_mesh_v_f_e':[len(v1),len(f1),e1],'outside_part_count_bit_exact_after_blender':len(orig),'unchanged_xyz_bounds':b1,
 'true_closed_edges_and_nonadjacent_intersections_zero':True,'outside_region_rays_n':len(O),'exterior_ray_delta_max_m':max(O),'numbers':out}
(D/'strip-stitch-blender.json').write_text(json.dumps(res,indent=2)+'\n')
print('OUTSIDE',len(O),max(O),'QA',out,flush=True)
assert max(O)<.003
old_q=out['crest']['old_p50_p90_p95_abs_m'];new_q=out['crest']['new_p50_p90_p95_abs_m']
al=out['all_inside_patch'];assert new_q[1]<old_q[1]-.02 and new_q[2]<old_q[2]-.045
assert al['new_p50_p90_p95_abs_m'][1] < al['old_p50_p90_p95_abs_m'][1]+.07 and al['new_p50_p90_p95_abs_m'][2] < al['old_p50_p90_p95_abs_m'][2]+.08,al
# True geometry-only interchange FBX; no planner claims UV/Editor.
dest=D/'Fisher-Fine-Arts-south-strip-corrected-envelope.fbx'
bpy.ops.object.select_all(action='DESELECT'); b.select_set(True); bpy.context.view_layer.objects.active=b
bpy.ops.export_scene.fbx(filepath=str(dest),use_selection=True,object_types={'MESH'},axis_forward='-Z',axis_up='Y',global_scale=1.,
 use_mesh_modifiers=False,mesh_smooth_type='OFF',use_custom_props=False,bake_anim=False,path_mode='STRIP',add_leaf_bones=False)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(dest),use_image_search=False)
o,=[o for o in bpy.context.scene.objects if o.type=='MESH']
V=[o.matrix_world@p.co for p in o.data.vertices];F=[tuple(p.vertices) for p in o.data.polygons]
assert F==f1 and len(V)==len(v1)
maximum=max((a-b).length for a,b in zip(V,v1));assert maximum<.000008,maximum
res['fbx_import_sha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
res['fbx_max_roundtrip_m']=maximum
(D/'strip-stitch-blender.json').write_text(json.dumps(res,indent=2)+'\n')
