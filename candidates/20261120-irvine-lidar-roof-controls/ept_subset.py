"""Filter remote official EPT hierarchies and fetch small local point nodes only."""
import argparse,concurrent.futures,hashlib,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('uri');p.add_argument('directory',type=Path)
p.add_argument('region',type=float,nargs=6);p.add_argument('--depth',type=int,default=10);p.add_argument('--download',action='store_true');a=p.parse_args()
o=a.directory;o.mkdir(exist_ok=True,parents=True); h=o/'index-cache';h.mkdir(exist_ok=True)
def get(url,d,limit):
 if not d.exists():
  tmp=d.with_suffix(d.suffix+'.partial')
  subprocess.run(['curl','-fLsS','--max-time','18','--max-filesize',str(limit),url,'-o',str(tmp)],check=True)
  tmp.replace(d)
 assert 0<d.stat().st_size<=limit
get(a.uri+'/ept.json',h/'ept.json',100000)
m=json.loads((h/'ept.json').read_text()); b=m['bounds']; H={}
def overlap(k):
 d,*p=map(int,k.split('-')); f=[(b[i+3]-b[i])/(2**d) for i in range(3)]
 s=[b[i]+p[i]*f[i] for i in range(3)];t=[s[i]+f[i] for i in range(3)]
 return d<=a.depth and not any(s[i]>a.region[i+3] or t[i]<a.region[i] for i in range(3))
def walk(k):
 q=h/(k+'.json');get(a.uri+'/ept-hierarchy/'+q.name,q,300000)
 for n,i in json.loads(q.read_text()).items():
  if not overlap(n):continue
  if i<0:
   assert n!=k;walk(n)
  else:H[n]=i
walk('0-0-0-0')
assert len(H)<160, len(H)
p=o/'ept-hierarchy';p.mkdir(exist_ok=True)
(p/'0-0-0-0.json').write_text(json.dumps(dict(sorted(H.items())))+'\n')
m['points']=sum(H.values())
(o/'ept.json').write_text(json.dumps(m,indent=2)+'\n')
b=o/'ept-data';b.mkdir(exist_ok=True)
print('selected nodes',len(H),'total node points before XY',m['points'],'max node points',max(H.values()),flush=True)
if a.download:
 assert sum(H.values())<2500000
 def fetch(k):
  q=b/(k+'.laz');get(a.uri+'/ept-data/'+q.name,q,2000000);return [k,q.stat().st_size,hashlib.sha256(q.read_bytes()).hexdigest()]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rec=list(pool.map(fetch,[k for k,n in H.items() if n>0]))
 (o/'receipts.json').write_text(json.dumps(dict(url=a.uri,region=a.region,requested_depth=a.depth,selected=rec),indent=2)+'\n')
 print('downloaded bytes',sum(x[1] for x in rec),flush=True)
