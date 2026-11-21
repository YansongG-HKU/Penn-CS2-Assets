"""Export geometry-only survey shell FBX and check exact topology/dimensions after clean import."""
import bpy,sys,json,hashlib,collections
from pathlib import Path
from mathutils.bvhtree import BVHTree
d=Path(sys.argv[sys.argv.index('--')+1]).resolve()
OBJ=d/'Fisher-Fine-Arts-survey-envelope.obj'
FBX=d/'Fisher-Fine-Arts-geometry-reference.fbx'
def clear():bpy.ops.wm.read_factory_settings(use_empty=True)
def read():return next(o for o in bpy.context.scene.objects if o.type=='MESH')
def detail(o):
 m=o.data; m.calc_loop_triangles()
 a=[o.matrix_world@v.co for v in m.vertices]; f=[tuple(t.vertices) for t in m.loop_triangles]
 es=collections.defaultdict(list)
 for p in f:
  for x,y in zip(p,p[1:]+p[:1]): es[min(x,y),max(x,y)].append((x,y))
 assert all(len(e)==2 and e[0]==e[1][::-1] for e in es.values())
 return a,f,len(es),[list(map(min,zip(*a))),list(map(max,zip(*a)))]
clear()
bpy.ops.wm.obj_import(filepath=str(OBJ),forward_axis='Y',up_axis='Z')
o=read();v0,f0,e0,b0=detail(o);o.name='Fisher_Fine_Arts_Geometry_Reference_No_Game_Materials'
o.select_set(True)
bpy.ops.export_scene.fbx(filepath=str(FBX),use_selection=True,object_types={'MESH'},axis_forward='-Z',axis_up='Y',
  global_scale=1.,apply_scale_options='FBX_SCALE_NONE',use_mesh_modifiers=False,mesh_smooth_type='OFF',
  use_custom_props=False,bake_anim=False,path_mode='STRIP',add_leaf_bones=False)
clear()
bpy.ops.import_scene.fbx(filepath=str(FBX),use_image_search=False)
o=read();v1,f1,e1,b1=detail(o)
assert len(v0)==len(v1) and f0==f1 and e0==e1
worst=max((a-b).length for a,b in zip(v0,v1)); assert worst<1.e-4
tree=BVHTree.FromPolygons(v1,f1,all_triangles=True,epsilon=1e-7)
bad=[(i,j) for i,j in tree.overlap(tree) if i<j and set(f1[i]).isdisjoint(f1[j])]
assert not bad,bad[:10]
report={'FBX_file':FBX.name,'FBX_sha256':hashlib.sha256(FBX.read_bytes()).hexdigest(),'verts':len(v1),'triangles':len(f1),'oriented_edge_pairs':e1,
   'maximum_roundtrip_displacement_m':worst,'nonadjacent_triangle_pairs':len(bad),'UV':'none - reference only', 'game_materials':False}
(d/'geometry-fbx-readback.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
