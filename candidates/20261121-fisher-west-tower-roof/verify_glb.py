"""Check the self-contained GLB preview matches the authoritative standalone OBJ geometry."""
import collections,hashlib,json,math,sys,bpy
from pathlib import Path
d=Path(sys.argv[sys.argv.index('--')+1]).resolve()
glb=d/'Fisher-west-tower-crown-review.glb'
def audit(import_fn):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 import_fn()
 verts=[];pos={};fs=[]
 for o in bpy.context.scene.objects:
  if o.type!='MESH':continue
  m=o.data; m.calc_loop_triangles()
  W=[o.matrix_world@p.co for p in m.vertices]
  ids=[]
  for pp in W:
   k=tuple(round(q,4) for q in pp)
   if k not in pos:pos[k]=len(verts);verts.append(k)
   ids.append(k)
  fs.extend(tuple(ids[i] for i in f.vertices) for f in m.loop_triangles)
 return collections.Counter(tuple(sorted(a)) for a in fs),len(verts),len(fs)
a,i,j=audit(lambda:bpy.ops.wm.obj_import(filepath=str(d/'Fisher-west-tower-crown-geometry.obj'),forward_axis='Y',up_axis='Z'))
b,k,l=audit(lambda:bpy.ops.import_scene.gltf(filepath=str(glb)))
assert i==k==510 and j==l==1020
# At 0.1 mm rounding a handful of near-halfway coordinates can land on adjacent bins, so
# independently compare nearest point and triangle centroids rather than assume text serialization identity.
if a!=b:
 pa={v for t in a for v in t}; pb={v for t in b for v in t}; mm={p:min(pa,key=lambda q:math.dist(p,q)) for p in pb}
 assert len(set(mm.values()))==510 and max(math.dist(p,q) for p,q in mm.items())<=.00011
 b=collections.Counter({tuple(sorted(mm[x] for x in t)):n for t,n in b.items()});assert a==b
r={'format':'GLB','sha256':hashlib.sha256(glb.read_bytes()).hexdigest(),'triangles':l,'position_welded_vertices':k,'same_triangles_as_obj_after_small_serialization_tolerance':True}
(d/'glb-readback.json').write_text(json.dumps(r,indent=2)+'\n')
