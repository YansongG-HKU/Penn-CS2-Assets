"""Replay only the verified per-texel Irvine slate patch in a clean trial copy."""
import hashlib,json,shutil,struct,sys,zipfile
from pathlib import Path
from PIL import Image
d=Path(__file__).resolve().parent
src,out=map(Path,sys.argv[1:]); m=json.loads((d/'manifest.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
if out.exists() or not src.is_dir():raise ValueError('Supply an existing Irvine trial folder and a new output folder')
for n,h in m['inputs_sha256'].items():
 if sha((src/n).read_bytes())!=h:raise ValueError('Pinned trial file not matched: '+n)
patch=d/'slate-texels.zip'
if sha(patch.read_bytes())!=m['archive_sha256']:raise ValueError('Invalid patch archive')
shutil.copytree(src,out)
with zipfile.ZipFile(patch) as z:
 a=z.read('indices.u32le')
 if len(a)!=4*m['target_texels']:raise ValueError('Wrong texel count')
 idx=[t[0] for t in struct.iter_unpack('<I',a)]
 if idx!=sorted(set(idx)) or not all(j<1024**2 for j in idx):raise ValueError('Invalid texel indices')
 for name,record in m['maps'].items():
  dest=out/name; before=Image.open(dest); assert before.size==(1024,1024)
  buf=bytearray(before.convert('RGBA').tobytes()); p=z.read(record['patch'])
  if len(p)!=4*m['target_texels']:raise ValueError('Wrong number of patch RGBA values')
  for j,i in enumerate(idx):buf[i*4:i*4+4]=p[j*4:j*4+4]
  if sha(buf)!=record['output_rgba_sha256']:raise ValueError('Wrong reconstructed texture')
  Image.frombytes('RGBA',(1024,1024),bytes(buf)).convert(before.mode).save(dest,optimize=False,**{k:v for k,v in before.info.items() if k in ('exif','dpi','icc_profile')})
  if sha(Image.open(dest).convert('RGBA').tobytes())!=record['output_rgba_sha256']:raise ValueError('Decoded texture changed')
  print(name,sha(dest.read_bytes()))
