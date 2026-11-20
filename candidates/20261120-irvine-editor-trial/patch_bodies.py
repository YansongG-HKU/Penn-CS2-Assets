"""Normalize only the expected Irvine body FBX map paths; preserve all geometry."""
import json,hashlib,sys
from pathlib import Path
from io_scene_fbx import parse_fbx,encode_bin
d,ref,far,dst=map(Path,sys.argv[sys.argv.index('--')+1:])
sys.path.insert(0,str(d))
from portable_penn_lod2 import clone,snapshot,normalize
stem='NA_IrvineAuditorium_7x7'
digest=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
R={}
for m in ('','_LOD1','_LOD2'):
 name=stem+m+'.fbx';src=far if m=='_LOD2' else ref/name
 r,v=parse_fbx.parse(str(src)); changes=[]
 wanted={f'{stem}{m if m=="_LOD2" else ""}_{n}.png' for n in ('BaseColor','Normal','Emissive')}
 normalize(r,wanted,changes)
 if len(changes)!=6 or {n for _,n in changes}!=wanted:raise ValueError((src,changes))
 q=dst/name
 assert not q.exists()
 with encode_bin.FBXElem.enable_multithreading_cm():payload=clone(r)
 encode_bin.write(str(q),payload,v)
 rr,w=parse_fbx.parse(str(q))
 assert w==v and snapshot(rr)==snapshot(r)
 R[name]={'source_sha256':digest(src),'output_sha256':digest(q),'path_fields':changes}
print(R)
(dst.parent/'body-paths.json').write_text(json.dumps(R,indent=2)+'\n')
