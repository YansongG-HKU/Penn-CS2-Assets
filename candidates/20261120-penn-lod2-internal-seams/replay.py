"""Extract only the expected patch members and verify exact candidate outputs."""
import json,shutil,sys,tempfile,zipfile
from pathlib import Path
import model_delta
base,out=map(Path,sys.argv[1:])
p=Path(__file__).resolve().parent
rows=json.loads((p/'manifest.json').read_text())
wanted={r['patch'] for r in rows}
if len(wanted)!=34:raise ValueError('Unexpected manifest count')
with tempfile.TemporaryDirectory() as tmp:
 d=Path(tmp);shutil.copyfile(p/'manifest.json',d/'manifest.json')
 for z in sorted(p.glob('patches-*.zip')):
  with zipfile.ZipFile(z) as f:
   for info in f.infolist():
    if info.filename not in wanted or not (0<info.file_size<=65536):raise ValueError('Unexpected patch member')
    (d/info.filename).write_bytes(f.read(info))
    wanted.remove(info.filename)
 if wanted:raise ValueError('Missing patch files')
 sys.argv=[sys.argv[0],'apply',str(base),str(out),str(d)]
 model_delta.main()
