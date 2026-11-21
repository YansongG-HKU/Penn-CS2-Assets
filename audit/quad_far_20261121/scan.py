"""Readback screening of positive-area overlaps (not general mesh intersection)."""
from collections import Counter,defaultdict
from pathlib import Path
from scipy.spatial import cKDTree
from osgeo import ogr
from itertools import combinations
import numpy as np
import sys,json
D=Path(__file__).resolve().parent
E=1e-5;MIN=1e-5
def polygon(x):
 r=ogr.Geometry(ogr.wkbLinearRing)
 for a,b in x:r.AddPoint_2D(float(a),float(b))
 r.CloseRings();p=ogr.Geometry(ogr.wkbPolygon);p.AddGeometry(r);return p
def orientation(q,pp):
 uv=np.eye(3)[np.argmin(np.abs(q))]
 u=np.cross(q,uv);u/=np.linalg.norm(u);return np.array([u,np.cross(q,u)])
def components(pairs,n):
 lab=list(range(n))
 def find(a):
  while lab[a]!=a:a=lab[a]
  return a
 for a,b in sorted(pairs):
  a,b=find(a),find(b);lab[max(a,b)]=min(a,b)
 return [find(i) for i in range(n)]
def topo(index,tri):
 edges=defaultdict(list)
 for i,r in enumerate(tri):
  v=[index[j] for j in r]
  for a,b in zip(v,v[1:]+v[:1]):edges[tuple(sorted((a,b)))].append((i,1 if a<b else -1))
 hist=Counter(map(len,edges.values()))
 return dict(edge_incidence=dict(hist), winding_disagree=sum(len(v)==2 and sum(y for _,y in v)!=0 for v in edges.values()),
  incidence_gt2=[dict(edge=list(k),faces=[i for i,_ in v]) for k,v in edges.items() if len(v)>2])
def audit(asset):
 coords=[];idx=[];ref=[]
 for m in asset['meshes']:
  for f,a,b,c in m['tri']:idx.append([len(coords)+a,len(coords)+b,len(coords)+c]);ref.append([m['name'],f])
  coords.extend(m['co'])
 v=np.asarray(coords);t=v[idx]; n=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);m=np.linalg.norm(n,axis=1); alive=m>1e-12
 n[alive]/=m[alive,None];lo=t.min(axis=1);hi=t.max(axis=1);hits=[]
 for i in range(len(t)):
  if not alive[i]:continue
  mask=alive[i+1:] & np.all(hi[i]+E>=lo[i+1:],axis=1) & np.all(hi[i+1:]+E>=lo[i],axis=1)
  for j in np.flatnonzero(mask)+i+1:
   c=float(n[i]@n[j]); 
   if abs(c)<0.999999999:continue
   d1=float(np.max(np.abs((t[j]-t[i,0])@n[i])));d2=float(np.max(np.abs((t[i]-t[j,0])@n[j])))
   if max(d1,d2)>E:continue
   area=[]
   for k in (i,j):
    uv=orientation(n[k],t[k,0]);p,q=(polygon((t[h]-t[k,0])@uv.T) for h in (i,j))
    if not p.Intersects(q):break
    g=p.Intersection(q); area.append(g.GetArea() if g.GetDimension()==2 else 0.)
   if len(area)!=2 or min(area)<=MIN:continue
   hits.append(dict(tri=[i,int(j)],faces=[ref[i],ref[j]],direction='same' if c>0 else 'opposed',area_m2=area,plane_deviation_m=[d1,d2],centroid_a_m=t[i].mean(axis=0).tolist(),centroid_b_m=t[j].mean(axis=0).tolist()))
 pairs=cKDTree(v).query_pairs(E);labels=components(pairs,len(v))
 for perm in set(labels):
  q=v[np.asarray(labels)==perm];assert np.linalg.norm(q-q[0],axis=1).max()<=E+1e-12
 return dict(sha256=asset['sha256'],vertices=len(v),triangles=len(t),degenerate=int(sum(~alive)),coordinates_weldable_pairs=len(pairs),indexed=topo(list(range(len(v))),idx),position=topo(labels,idx),hits=hits,
  pair_counts=Counter(r['direction'] for r in hits),pairwise_area_m2={k:sum(min(r['area_m2']) for r in hits if r['direction']==k) for k in ('same','opposed')})
tag=sys.argv[1] if len(sys.argv)>1 else ""
out={k:audit(v) for k,v in json.loads((D/(tag+'world.json')).read_text()).items()}
(D/(tag+'screen.json')).write_text(json.dumps(dict(plane_tolerance_m=E,minimum_positive_area_m2=MIN, assets=out),indent=2)+'\n')
for a,r in out.items():
 print(a,r['triangles'],r['indexed']['edge_incidence'],r['position']['edge_incidence'],r['pair_counts'],{k:round(v,7) for k,v in r['pairwise_area_m2'].items()})
