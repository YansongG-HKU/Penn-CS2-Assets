from pathlib import Path
import shutil,bpy,sys,json,hashlib,math
D=Path(sys.argv[-1]).resolve()
S=D/'assets'; C=D/'clean'
shutil.copytree(S,C)
receipt=json.loads((D/'stage-receipt.json').read_text())
data={}
for n,a in receipt['controls'].items():
 f=C/n; images={}; models={}
 for name,info in a['fbx'].items():
  bpy.ops.wm.read_factory_settings(use_empty=True)
  p=f/name
  assert hashlib.sha256(p.read_bytes()).hexdigest()==info['trial_sha256']
  bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False)
  o,=[m for m in bpy.context.scene.objects if m.type=='MESH'];m=o.data;m.calc_loop_triangles()
  assert m.uv_layers.active and len(m.loop_triangles)==info['triangles']
  assert all(math.isfinite(z) for v in m.vertices for z in o.matrix_world@v.co)
  maprow={}
  for im in bpy.data.images:
   if im.source=='FILE':
    q=Path(bpy.path.abspath(im.filepath)).resolve();assert q.parent==f and q.name in a['png'];im.reload()
    assert len(im.pixels)>0
    maprow[q.name]=list(im.size)
  if not (p.stem.endswith('_Win') or p.stem.endswith('_Gls')):
   assert set(k.rsplit('_',1)[-1] for k in maprow)=={'BaseColor.png','Normal.png','Emissive.png'},(p,maprow)
  models[name]={'triangles':len(m.loop_triangles),'bound_images':maprow}
 bpy.ops.wm.read_factory_settings(use_empty=True)
 for name,sha in a['png'].items():
  p=f/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==sha
  im=bpy.data.images.load(str(p),check_existing=False);assert len(im.pixels)>0
  images[name]=list(im.size);bpy.data.images.remove(im)
 assert hashlib.sha256((f/'settings.json').read_bytes()).hexdigest()==a['settings_sha256']
 data[n]={'models':models,'decoded_all_png':images}
(D/'offline-readback.json').write_text(json.dumps({'controls':data,'game_editor_ran':False,'not_proof_of_visual_quality':True},indent=2)+'\n')
print('CLEAN_OFFLINE_STAGING_OK',[(n,len(x['models']),len(x['decoded_all_png'])) for n,x in data.items()])
