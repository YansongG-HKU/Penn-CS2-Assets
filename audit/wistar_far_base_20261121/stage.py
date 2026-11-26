from pathlib import Path
import zipfile,json,hashlib
D=Path(__file__).resolve().parent;ROOT=D.parent/'cs2-penn-portable';z=zipfile.ZipFile(next((ROOT/'library').glob('*.zip')))
f='NA_WistarInstitute_17x8_LOD2.fbx';A=f'WistarInstitute/fbx/split/{f}'; raw=json.loads((D/'raw.json').read_text());names=[p for p in z.namelist() if p.startswith('WistarInstitute/textures/') and '_LOD2_' in p]
assert len(names)==5
for mode in ('old','fresh'):
 for name in sorted(names+[A]):
  p=D/mode/name;p.parent.mkdir(exist_ok=True,parents=True)
  p.write_bytes((D/'new'/f).read_bytes() if name==A and mode=='fresh' else z.read(name))
 if mode=='old':assert hashlib.sha256((D/mode/A).read_bytes()).hexdigest()==raw['source_sha256']
print(D/'fresh'/A)
