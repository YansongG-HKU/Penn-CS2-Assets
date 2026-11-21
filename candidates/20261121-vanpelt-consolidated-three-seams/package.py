from pathlib import Path
import zipfile,hashlib,json
D=Path(__file__).resolve().parent
out=D/'Van-Pelt-Library-LOD2-consolidated-trial.zip'; Q=D/'fresh'
files={str(p.relative_to(D)):p for x in ('assets','editable') for p in (D/x).rglob('*') if p.is_file()}
assert sum(Path(n).suffix=='.fbx' for n in files)==5 and sum(Path(n).suffix=='.png' for n in files)==10
for n in ('README.md','area-receipt.json','stage-receipt.json','offline-readback.json','repair-receipt.json','readback.json'):files[n]=D/n
with zipfile.ZipFile(out,'x',zipfile.ZIP_DEFLATED) as z:
 for n,p in sorted(files.items()):z.write(p,n)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 z.extractall(Q)
 assert all((Q/n).read_bytes()==p.read_bytes() for n,p in files.items())
print(out.stat().st_size,hashlib.sha256(out.read_bytes()).hexdigest(),len(files))
