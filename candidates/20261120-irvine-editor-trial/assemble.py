"""Create a deterministic Irvine import ZIP, verify and extract it into a fresh directory."""
import json,hashlib,sys,zipfile
from pathlib import Path
root,archive,extract=map(Path,sys.argv[1:])
assert not archive.exists() and not extract.exists()
A=root/'IrvineAuditorium'; stem='NA_IrvineAuditorium_7x7'
expected={stem+s+'.fbx' for s in ('','_LOD1','_LOD2','_Win','_LOD1_Win')}|{'settings.json'}|{stem+s+'_'+n+'.png' for s in ('','_LOD2') for n in ('BaseColor','Normal','MaskMap','ControlMask','Emissive')}
assert {q.name for q in A.iterdir()}==expected
digest=lambda b:hashlib.sha256(b).hexdigest()
H={'IrvineAuditorium/'+n:digest((A/n).read_bytes()) for n in sorted(expected)}
(root/'SHA256SUMS.txt').write_text(''.join(h+'  '+p+'\n' for p,h in H.items()))
N=sorted(set(H)|{'README.txt','SHA256SUMS.txt'})
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name in N:
  info=zipfile.ZipInfo(name,(2026,11,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
  info.external_attr=0o644<<16
  z.writestr(info,(root/name).read_bytes(),compresslevel=9)
with zipfile.ZipFile(archive) as z:
 assert z.namelist()==N and not z.testzip()
 for f in N:
  b=z.read(f); p=extract/f;p.parent.mkdir(parents=True,exist_ok=True)
  if f in H:assert digest(b)==H[f]
  p.write_bytes(b)
R={'archive_sha256':digest(archive.read_bytes()),'bytes':archive.stat().st_size,'payload_files':len(H),'manifest':H,'crc_and_payload_checks':'passed'}
(root/'package.json').write_text(json.dumps(R,indent=2)+'\n')
print(R['bytes'],R['archive_sha256'],R['payload_files'])
