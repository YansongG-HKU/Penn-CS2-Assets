"""Read binary FBX polygons without altering assets, inventory exact indexed polygon failures."""
from pathlib import Path
import zipfile,sys,tempfile,types,json
from collections import Counter
mod=types.ModuleType('io_scene_fbx');mod.__path__=['/usr/share/blender/scripts/addons_core/io_scene_fbx'];sys.modules[mod.__name__]=mod
from io_scene_fbx import parse_fbx
def scan(f):
 root,ver=parse_fbx.parse(str(f)); rv=[]
 for ob in root.elems:
  if ob.id!=b'Objects':continue
  for g in ob.elems:
   if g.id!=b'Geometry' or g.props[2]!=b'Mesh':continue
   ix=next(e for e in g.elems if e.id==b'PolygonVertexIndex').props[0]; ar=[]; hs={}; st=Counter(); st['triangles']=0
   for i in ix:
    if i>=0: ar.append(i); continue
    ar.append(-i-1); n=len(ar); st['polygons']+=1; st['triangles']+=n-2; k=tuple(sorted(ar))
    if len(set(ar))!=n: st['repeated_index_faces']+=1
    j=ar.index(min(ar)); or0=tuple(ar[j:]+ar[:j])
    if k in hs:
     st['same_index_duplicate_excess']+=1
     st['same_cyclic' if hs[k]==or0 else 'other_cyclic']+=1
    else: hs[k]=or0
    ar.clear()
   rv.append(dict(st))
 return rv
if __name__=='__main__':
 z=zipfile.ZipFile(sys.argv[1]); out={}
 with tempfile.TemporaryDirectory() as tmp:
  f=Path(tmp)/'payload.fbx'
  for n in z.namelist():
   if not n.lower().endswith('.fbx'):continue
   f.write_bytes(z.read(n))
   try:out[n]=scan(f)
   except Exception as e:out[n]=str(e)
 Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n')
 for n,v in out.items():
  if isinstance(v,str) or any(x.get('same_index_duplicate_excess') or x.get('repeated_index_faces') for x in v):print(n,v)
 print('Files',len(out))
