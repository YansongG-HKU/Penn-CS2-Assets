"""Independently check byte-exported OBJ triangles against each whole held scan."""
import gzip,json,sys
from pathlib import Path
from collections import defaultdict
import hashlib
import numpy as np
out=Path(sys.argv[1]); raw=out/'Irvine-secondary-roof-surfaces.obj'
rep=json.loads((out/'secondary-roof-evidence.json').read_text()); assert hashlib.sha256(raw.read_bytes()).hexdigest()==rep['obj_sha256']
p=Path(sys.argv[2]); assert hashlib.sha256(p.read_bytes()).hexdigest()==rep['source_csv_gz_sha256']
with gzip.open(p,'rt') as g: a=np.unique(np.loadtxt(g,delimiter=',',skiprows=1,usecols=range(6)),axis=0)
b=a[np.isin(a[:,4],[19,20])&(a[:,3]==1)&(a[:,5]==1)]
L=(b[:,:2]-rep['utm_origin'])@np.column_stack((rep['E_axis_utm'],rep['N_axis_utm']))
V=[]; F=defaultdict(list); k=''
for line in raw.read_text().splitlines():
 sp=line.split()
 if sp[0]=='o':k=sp[1]
 if sp[0]=='v':V.append([float(i) for i in sp[1:]])
 if sp[0]=='f':F[k].append([int(i)-1 for i in sp[1:]])
V=np.array(V); D={}
for k,faces in F.items():
 h=np.full(len(L),np.nan)
 for f in faces:
  q=V[f]; A=np.column_stack((q[1,:2]-q[0,:2],q[2,:2]-q[0,:2]))
  assert np.linalg.det(A)>1e-7
  uv=(L-q[0,:2])@np.linalg.inv(A).T
  w=np.c_[1-uv.sum(1),uv]; seen=w.min(1)>=-1e-7
  hit=w[seen]@q[:,2]+rep['reference_zero_navd88_m']
  prev=h[seen]; ok=np.isfinite(prev)
  assert np.all(abs(hit[ok]-prev[ok])<2e-5)
  h[seen]=hit
 d={}
 for i in [19,20]:
  j=np.isfinite(h)&(b[:,4]==i); err=abs(h[j]-b[j,2])
  d[str(i)]=[len(err),*np.quantile(err,[.5,.9,.95]).round(5).tolist(),float(np.mean(err<.5))]
  assert len(err)>100 and float(np.quantile(err,.9))<.32 and float(np.mean(err<.5))>.96
 D[k]=d
print(json.dumps(D,indent=2))
(out/'triangle-holdout.json').write_text(json.dumps(D,indent=2)+'\n')

