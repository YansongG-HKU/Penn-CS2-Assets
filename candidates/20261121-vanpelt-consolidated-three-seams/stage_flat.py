"""Create one exact staged trial from a single immutable archive and pinned settings."""
import json,hashlib,collections,sys,zipfile
from pathlib import Path
from io_scene_fbx import parse_fbx,encode_bin
D=Path(sys.argv[-1]).resolve(); archive,=list((D.parent/'library').glob('*.zip'))
with archive.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
assert sha=='82c3dc8211489c19ee33b0bade3b8a334165cab5146dd60997c70ced70081b42'
M=json.loads((D.parent/'import-selection.json').read_text())
S=json.loads((D/'settings-pinned.json').read_text())
Z=zipfile.ZipFile(archive)
H={v['path']:v for v in json.loads(Z.read('FILES_SHA256.json'))}
def h(b): return hashlib.sha256(b).hexdigest()
def get(n):
 b=Z.read(n);assert len(b)==H[n]['bytes'] and h(b)==H[n]['sha256']; return b
O=D/'assets';O.mkdir(exist_ok=False); tmp=D/'_one.fbx'; assert not tmp.exists()
meth=dict(zip(b'BCZYILFDRSifdlbc',('add_bool','add_char','add_int8','add_int16','add_int32','add_int64','add_float32','add_float64','add_bytes','add_string','add_int32_array','add_float32_array','add_float64_array','add_int64_array','add_bool_array','add_byte_array')))
def clone(x):
 n=encode_bin.FBXElem(x.id)
 for t,v in zip(x.props_type,x.props):getattr(n,meth[t])(v)
 n.elems=[clone(y) for y in x.elems];return n
view=lambda x:(x.id,bytes(x.props_type),tuple(x.props),tuple(view(a) for a in x.elems))
def loc(x,changes,F):
 if x.id in {b'RelativeFilename',b'FileName',b'Filename'}:
  assert len(x.props)==1 and isinstance(x.props[0],bytes)
  old=x.props[0]
  if old:
   new=old.replace(b'\\',b'/').rsplit(b'/',1)[-1]
   assert new.decode() in F
   changes.append((x,old,new))
   x.props[0]=new
 for a in x.elems:loc(a,changes,F)
receipts={}
try:
 for n in ('VanPeltLibrary',):
  P=O/n;P.mkdir(); q,r=S[n];b=q.encode(); assert hashlib.sha1(f'blob {len(b)}\x00'.encode()+b).hexdigest()==r
  (P/'settings.json').write_bytes(b)
  pngs={}
  for p in Z.namelist():
   if p.startswith(n+'/textures/') and p.endswith('.png'):
    x=get(p); k=Path(p).name; pngs[k]=h(x); (P/k).write_bytes(x)
  assert len(pngs)==10
  alias=json.loads(q)['sharedAssets'];assert len(alias)==5
  assert all(k.replace('_LOD1','')==v and k not in pngs and v in pngs for k,v in alias.items())
  files={}
  for info in M['by_asset'][n]['keep']:
   p=info['path']; blob=get(p);assert h(blob)==info['sha256']
   canonical=h(blob)
   if Path(p).name.endswith('_LOD2.fbx'):
    proof=json.loads((D/'repair-receipt.json').read_text())
    assert proof['source_sha256']==canonical
    blob=(D/'stage'/p).read_bytes(); assert h(blob)==proof['candidate_sha256']
    info={**info,'triangles':52}
   tmp.write_bytes(blob);a,ver=parse_fbx.parse(str(tmp));assert ver==7400
   changes=[];original=view(a);loc(a,changes,pngs)
   dest=P/Path(p).name
   with encode_bin.FBXElem.enable_multithreading_cm():obj=clone(a)
   if changes:encode_bin.write(str(dest),obj,ver)
   else:dest.write_bytes(blob)
   ra,rv=parse_fbx.parse(str(dest));assert rv==ver and view(a)==view(ra)
   for x,old,new in changes:x.props[0]=old
   assert view(a)==original
   files[dest.name]={'canonical_sha256':info['sha256'],'trial_sha256':h(dest.read_bytes()),'triangles':info['triangles'],'version':ver,'image_path_fields_rewritten':len(changes),'source_is_geometry_repair':h(blob)!=canonical,'geometry_stage_sha256':h(blob)}
  receipts[n]={'fbx':files,'png':pngs,'settings_git_blob_sha1':r,'settings_sha256':h(b),'empty_glass_excluded':M['by_asset'][n]['skip_only_for_import']}
finally:
 if tmp.exists():tmp.unlink()
(D/'stage-receipt.json').write_text(json.dumps({'source_sha256':sha,'source_settings_ref':'7e00cba1653a8ef3ee07ebc03fc995e31f065503','controls':receipts,'engine_status':'not_run'},indent=2)+'\n')
print('FILE_STAGE',[(k,len(v['fbx']),len(v['png'])) for k,v in receipts.items()])
