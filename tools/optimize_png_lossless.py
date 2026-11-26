import pathlib,struct,zlib,hashlib,json,concurrent.futures
import argparse
parser=argparse.ArgumentParser(description="Lossless IDAT-only PNG texture optimization into a separate delta directory")
parser.add_argument("source",type=pathlib.Path)
parser.add_argument("output",type=pathlib.Path)
args=parser.parse_args()
ROOT=args.source.resolve();OUT=args.output.resolve()
if ROOT==OUT or ROOT in OUT.parents or OUT in ROOT.parents:
 parser.error("Source and output must be disjoint directories")
if OUT.exists() and any(OUT.iterdir()):
 parser.error("Output must be empty to prevent stale candidates")
OUT.mkdir(parents=True,exist_ok=True)

def chunks(b):
 pos=8;out=[]
 while pos<len(b):
  n=struct.unpack('>I',b[pos:pos+4])[0];typ=b[pos+4:pos+8];d=b[pos+8:pos+8+n];crc=struct.unpack('>I',b[pos+8+n:pos+12+n])[0];assert zlib.crc32(typ+d)&0xffffffff==crc;out.append((typ,d,b[pos:pos+n+12]));pos+=n+12
 assert pos==len(b);return out
def work(p):
 b=p.read_bytes();assert b[:8]==b'\x89PNG\r\n\x1a\n';cs=chunks(b);raw=zlib.decompress(b''.join(d for t,d,_ in cs if t==b'IDAT'));compressed=zlib.compress(raw,9);new=b[:8];added=False
 for typ,d,full in cs:
  if typ==b'IDAT':
   if not added:new+=struct.pack('>I',len(compressed))+b'IDAT'+compressed+struct.pack('>I',zlib.crc32(b'IDAT'+compressed)&0xffffffff);added=True
  else:new+=full
 nc=chunks(new);assert zlib.decompress(b''.join(d for t,d,_ in nc if t==b'IDAT'))==raw
 assert [(t,d) for t,d,_ in cs if t!=b'IDAT']==[(t,d) for t,d,_ in nc if t!=b'IDAT']
 saved=max(0,len(b)-len(new));rel=str(p.relative_to(ROOT))
 if saved:
  dest=OUT/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(new)
 ihdr=next(d for t,d,_ in cs if t==b'IHDR');w,h,depth,color=struct.unpack('>IIBB',ihdr[:10])
 return {'path':rel,'original_bytes':len(b),'candidate_bytes':len(new) if saved else len(b),'saved_bytes':saved,'width':w,'height':h,'bit_depth':depth,'color_type':color,'scanline_sha256':hashlib.sha256(raw).hexdigest(),'original_sha256':hashlib.sha256(b).hexdigest(),'candidate_sha256':hashlib.sha256(new if saved else b).hexdigest(),'non_IDAT_chunks_preserved':True}
paths=sorted(ROOT.glob('*/textures/*.png'));rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 for r in ex.map(work,paths):
  rows.append(r);(OUT/'texture_audit.json').write_text(json.dumps(rows,indent=2));print('DONE',len(rows),r['saved_bytes'],flush=True)
print('TOTAL',len(rows),sum(x['saved_bytes'] for x in rows),sum(x['saved_bytes']>0 for x in rows),flush=True)
