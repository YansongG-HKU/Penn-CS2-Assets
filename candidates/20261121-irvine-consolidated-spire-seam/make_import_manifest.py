"""Verified archive inventory: exclude only exact zero-vertex/polygon glass stubs; no source edits."""
import json,collections,sys,zipfile,hashlib,tempfile
from pathlib import Path
D=Path(__file__).parent; sys.path.insert(0,str(D.parent/'cs2-portable-audit'))
from scan import parse_fbx
F,=list((D/'library').glob('*.zip'))
inventory=json.loads((D/'exact-index-audit.json').read_text())
assert len(inventory)==637 and all(isinstance(v,list) and len(v)>0 for v in inventory.values())
assert all(not g.get('same_index_duplicate_excess') and not g.get('repeated_index_faces') for v in inventory.values() for g in v)
source_paths={k:v for k,v in inventory.items() if '/fbx/split/' in k}
assert len(source_paths)==322
S=zipfile.ZipFile(F); one=lambda x,k:next(y for y in x.elems if y.id==k)
A=collections.defaultdict(lambda:{'keep':[],'skip_only_for_import':[]})
with tempfile.TemporaryDirectory() as td:
 p=Path(td)/'geo.fbx'
 for k,group in sorted(source_paths.items()):
  raw=S.read(k)
  assert len(group)==1
  entry={'path':k,'triangles':group[0]['triangles'],'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
  stem=k.split('/')[0]
  if entry['triangles']==0:
   assert k.endswith('_Gls.fbx')
   p.write_bytes(raw); f,_=parse_fbx.parse(str(p));g=one(one(f,b'Objects'),b'Geometry')
   assert not one(g,b'Vertices').props[0] and not one(g,b'PolygonVertexIndex').props[0]
   entry['reason']='exact zero vertices and zero polygon indices, not a glass surface'
   A[stem]['skip_only_for_import'].append(entry)
  else:A[stem]['keep'].append(entry)
assert len(A)==46
with F.open('rb') as fh: archive=hashlib.file_digest(fh,'sha256').hexdigest()
skip=sum(len(v['skip_only_for_import']) for v in A.values())
assert skip==90
m={'archive_filename':F.name,'archive_sha256':archive,'all_fbx_scanned':637,'standard_split_fbx_scanned':322,'indexed_duplicate_excess':0,'standard_split_nonempty_entries':322-skip,
 'standard_split_empty_glass_omitted_from_import_list_only':skip,'scope':'This identifies only exact same-index and exactly empty geometry. Keep original files. Geometric overlap, accurate shape and CS2 Editor remain independent gates.',
 'by_asset':dict(A)}
(D/'import-selection.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print('Empty only',skip,'kept',322-skip,'nonempty glass',[[t['path'] for t in p['keep'] if t['path'].endswith('_Gls.fbx')] for p in A.values() if not p['skip_only_for_import']])
