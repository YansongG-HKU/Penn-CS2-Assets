from pathlib import Path
import zipfile,hashlib,json
D=Path(__file__).resolve().parent; T=D/'stage'; A=D.parent/'import-selection.json'; Q=D/'fresh'; out=D/'Irvine-LOD2-consolidated-baseline-seam-patch.zip'
payload={str(p.relative_to(T)):p for p in T.rglob('*') if p.is_file()}
assert len(payload)==6 and sum(p.suffix=='.png' for p in payload.values())==5
S=D.parent/'irvine-input/IrvineAuditorium/textures'
for p in payload.values():
 if p.suffix=='.png':assert p.read_bytes()==(S/p.name).read_bytes()
H={n:hashlib.sha256(p.read_bytes()).hexdigest() for n,p in payload.items()}
with zipfile.ZipFile(out,'x',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for n,p in sorted(payload.items()):z.write(p,n)
 for n in ('README.md','repair-receipt.json','readback.json'):z.write(D/n,n)
 z.write(A,A.name)
 z.writestr('payload-sha256.json',json.dumps(H,indent=2)+'\n')
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 z.extractall(Q)
 for n,h in H.items():assert hashlib.sha256((Q/n).read_bytes()).hexdigest()==h
print(out.stat().st_size,hashlib.sha256(out.read_bytes()).hexdigest())
