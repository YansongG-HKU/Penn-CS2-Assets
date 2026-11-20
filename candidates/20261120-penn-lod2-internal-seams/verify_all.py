"""Independently reimport the pinned and repaired LOD2 files and compare retained triangles."""
import bpy,collections,hashlib,json,sys,math
from pathlib import Path
from mathutils import Vector
d,q,report=map(Path,sys.argv[sys.argv.index('--')+1:])
def read(f,remove):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.fbx(filepath=str(f),use_image_search=False)
 o,=[x for x in bpy.context.scene.objects if x.type=='MESH']
 m=o.data; v=[tuple(o.matrix_world@x.co) for x in m.vertices]
 E=collections.defaultdict(list); sig=collections.defaultdict(list)
 r=lambda vec:tuple(round(x,6) for x in vec)
 for p in m.polygons:
  ids=list(p.vertices); assert len(ids)==3
  a,b,c=[Vector(v[i]) for i in ids]; assert ((b-a).cross(c-a)).length>1e-9
  for a,b in zip(ids,ids[1:]+ids[:1]):E[tuple(sorted((a,b)))].append((a,b))
  if p.index in remove:continue
  row=tuple((r(v[m.loops[k].vertex_index]),r(m.uv_layers.active.data[k].uv),
             tuple(m.corner_normals[k].vector)) for k in p.loop_indices)
  rot=min((row[i:]+row[:i] for i in range(3)),key=lambda rr:[(co,uv) for co,uv,n in rr])
  sig[(p.material_index,tuple((co,uv) for co,uv,n in rot))].append(tuple(n for co,uv,n in rot))
 assert all(len(x)==2 and x[0]==x[1][::-1] for x in E.values())
 return len(m.polygons),len(v),len(E),[[fn(x[k] for x in v) for k in range(3)] for fn in (min,max)],sig
R={}
for f in sorted(q.glob('*.fbx')):
 a=d/f.name
 j=json.loads(f.with_name(f.name+'.json').read_text());remove=j['removed_opposite_cap_faces']
 SHA=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
 assert SHA(a)==j['input_sha256'] and SHA(f)==j['output_sha256']
 i,p=read(a,remove),read(f,[])
 assert i[0]-p[0]==len(remove) and i[1]-p[1]==j['welded_vertex_count']
 assert i[3]==p[3] and i[4].keys()==p[4].keys(),f.name
 max_normal=0
 for k,values in i[4].items():
  assert len(values)==len(p[4][k])
  for x,y in zip(sorted(values),sorted(p[4][k])):
   max_normal=max(max_normal,*(math.dist(a,b) for a,b in zip(x,y)))
 assert max_normal<0.0001,(f.name,max_normal)
 R[f.name]={**j,'before_vertices':i[1],'after_vertices':p[1],'after_edges':p[2],
            'bounds_m':p[3],'reimport_retained_corner_position_uv_material_equal_at_6_digits':True,'reimport_max_normal_chord':max_normal}
assert len(R)==34
report.write_text(json.dumps(R,indent=2)+'\n')
print('VERIFIED',len(R),sum(j['old_triangles']-j['new_triangles'] for j in R.values()))
