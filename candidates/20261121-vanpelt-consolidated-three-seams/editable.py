from pathlib import Path
import bpy,sys,json,hashlib
D=Path(sys.argv[-2]).resolve(); mode=sys.argv[-1]
A=D/'assets/VanPeltLibrary';F=D/'editable/VanPelt-LOD2-editable.blend'
p=A/'NA_VanPeltLibrary_18x6_LOD2.fbx'
if mode=='save':
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False)
 o,=[o for o in bpy.context.scene.objects if o.type=='MESH']
 for i in bpy.data.images:
  if i.source=='FILE':
   name=Path(i.filepath).name; assert (A/name).is_file();i.filepath='//../assets/VanPeltLibrary/'+name
 F.parent.mkdir(exist_ok=False)
 bpy.context.preferences.filepaths.save_version=0
 bpy.ops.wm.save_as_mainfile(filepath=str(F),relative_remap=False,compress=True)
bpy.ops.wm.open_mainfile(filepath=str(F),use_scripts=False)
o,=[o for o in bpy.context.scene.objects if o.type=='MESH'];m=o.data;m.calc_loop_triangles()
assert len(m.loop_triangles)==52 and len(m.vertices)==28 and m.uv_layers.active
seen={}
for i in bpy.data.images:
 if i.source=='FILE':
  p=Path(bpy.path.abspath(i.filepath)).resolve()
  assert i.filepath.startswith('//') and p.parent==A and p.is_file()
  assert len(i.pixels)>0;seen[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
assert len(seen)==3
print('EDITABLE_PASS',F.name,seen)
