import bpy,json,sys,hashlib
from pathlib import Path
inp,out=map(Path,sys.argv[sys.argv.index('--')+1:]);data={}
for f in sorted(inp.glob('*.fbx')):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.fbx(filepath=str(f))
 arr=[]
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH':continue
  me=ob.data;me.calc_loop_triangles()
  arr.append(dict(name=ob.name, co=[list(ob.matrix_world@v.co) for v in me.vertices],tri=[[t.polygon_index,*t.vertices] for t in me.loop_triangles],poly=[list(p.vertices) for p in me.polygons]))
 assert arr,f
 data[f.stem]=dict(sha256=hashlib.sha256(f.read_bytes()).hexdigest(),meshes=arr)
out.write_text(json.dumps(data,separators=(',',':'))+'\n')
