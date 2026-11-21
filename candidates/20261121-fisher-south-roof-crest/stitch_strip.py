"""Substitute the measured strip inside an exact grid seam, with unchanged exterior face coordinates."""
import collections,sys,json,hashlib
from pathlib import Path
import numpy as np
from osgeo import ogr
from geos import tris2,flat
D=Path(__file__).resolve().parent
base=Path(sys.argv[1]); assert hashlib.sha256(base.read_bytes()).hexdigest()=='49393791dbef9a9d7f5aab91b79e96a2203cba7a9c8794ad92ed822d00436db7'
strip=D/'Fisher-south-raised-roof-strip.obj'
def read(p):
 a=[];b=[]
 for ln in p.read_text().splitlines():
  t=ln.split()
  if not t:continue
  if t[0]=='v':a.append([float(k) for k in t[1:]])
  elif t[0]=='f':b.append([int(k)-1 for k in t[1:]])
 return np.asarray(a),np.asarray(b)
V,F=read(base); n=int((base.parent/'roof-face-count.txt').read_text())
sv,sf=read(strip); sf=sf[:8]; assert len(sv)==16
# Keep the better-supported lower south ramp in the full legacy geometry (the standalone study
# still shows the full section). Integrate only the supported crest; leave the mixed-height northern transition untouched.
def poly(P):
 r=ogr.Geometry(ogr.wkbLinearRing)
 for x,y in P:r.AddPoint_2D(x,y)
 r.CloseRings();q=ogr.Geometry(ogr.wkbPolygon);q.AddGeometry(r);return q
cut_s=-29.96
clip=poly([(-10.96,cut_s),(14.97,cut_s),(14.97,-29.50),(-10.96,-29.50)])
pv=[];pf=[];keys={}
def add(pt):
 k=tuple(np.round(pt,7))
 if k not in keys:keys[k]=len(pv);pv.append(k)
 return keys[k]
for row in sf:
 u=sv[row]
 c=poly(u[:,:2]).Intersection(clip)
 if c.IsEmpty():continue
 B=np.linalg.solve(np.c_[u[:,:2],np.ones(3)],u[:,2])
 for t in tris2(c):
  if flat(t)<1e-10:continue
  pf.append([add(p) for p in np.c_[t,np.c_[t,np.ones(3)]@B]])
sv=np.asarray(pv);sf=np.asarray(pf)
B0=np.array([-11.44,-30.16]);B1=np.array([15.60,-29.12])
geom=V[F[:n],:2]
M=((geom>=B0-1e-7)&(geom<=B1+1e-7)).all(axis=(1,2))
assert M.sum()==2*52*2,M.sum()
assert abs(sum(flat(v) for v in geom[M])-np.prod(B1-B0))<1e-7
# A densely pinned intermediate collar retains the real prior heightfield next to ambiguous return
# layers. That protects the old north transition instead of stretching the high plane across it.
triangle_set=V[F[:n][M]]
def oldz(q):
 vals=[]
 for a in triangle_set:
  if (q<a[:,:2].min(axis=0)-1e-7).any() or (q>a[:,:2].max(axis=0)+1e-7).any():continue
  uv=np.linalg.solve((a[1:,:2]-a[0,:2]).T,q-a[0,:2]); ww=np.r_[1-uv.sum(),uv]
  if min(ww)>=-1.e-7:vals.append(float(ww@a[:,2]))
 assert vals and max(vals)-min(vals)<.0002,(q,vals)
 return np.mean(vals)
# Preserve a small pre-existing height contribution near the conditioned, multi-level upper
# returns. One weight for the full panel; do not patch individual validation points.
retained_weight=.10
for i,p in enumerate(sv):sv[i,2]=(1-retained_weight)*p[2]+retained_weight*oldz(p[:2])
xx=np.r_[-11.17,np.round(np.arange(-10.92,15.36,.52),7),15.32]
xs=np.unique(xx)
midxy=np.array([*(zip(xs,np.full(len(xs),-30.08))),*(zip(xs[::-1],np.full(len(xs),-29.36)))])
inter=np.c_[midxy,[oldz(q) for q in midxy]]
def rings(f):
 e=collections.defaultdict(list)
 for r in f:
  rr=tuple(map(int,r))
  for i,j in zip(rr,rr[1:]+rr[:1]):e[min(i,j),max(i,j)].append((i,j))
 rims={v[0][0]:v[0][1] for v in e.values() if len(v)==1}
 s=[min(rims)]
 while rims[s[-1]]!=s[0]:s.append(rims[s[-1]])
 assert len(s)==len(rims)
 assert all(len(v)==1 or (len(v)==2 and v[0]==v[1][::-1]) for v in e.values())
 return s
outer=rings(F[:n][M]); inner=rings(sf)
assert len(outer)==108 and len(inner)>=8
W=np.vstack([V,sv,inter])
L=len(V); IL=L+len(sv)
b=np.r_[F[:n][~M],F[n:]].tolist()+[[int(i+L) for i in s] for s in sf]
nxt=[]
for pair in [(outer,list(range(IL,len(W)))[::-1]),(list(range(IL,len(W))),[L+i for i in inner[::-1]])]:
 C=ogr.Geometry(ogr.wkbPolygon)
 o2={}
 for ids in pair:
  r=ogr.Geometry(ogr.wkbLinearRing)
  for i in ids:
   x,y=W[i,:2];r.AddPoint_2D(x,y);o2[tuple(np.round([x,y],7))]=i
  r.CloseRings();C.AddGeometry(r)
 assert C.IsValid()
 for t in tris2(C):
  f=[o2[tuple(np.round(p,7))] for p in t];assert len(set(f))==3
  nxt.append(f)
b+=nxt
E=collections.defaultdict(list)
for f in b:
 for i,j in zip(f,f[1:]+f[:1]):E[min(i,j),max(i,j)].append((i,j))
assert all(len(v)==2 and v[0]==v[1][::-1] for v in E.values())
used=np.unique(b); remap={int(a):i+1 for i,a in enumerate(used)}
name='Fisher-Fine-Arts-south-strip-corrected-envelope.obj'
p=D/name
p.write_text('# Measured south roof strip integrated only in a bounded rectangle; no game materials.\no Fisher_South_Roof_Integrated\n'+ ''.join('v %.7f %.7f %.7f\n'%tuple(W[i]) for i in used)+''.join('f %d %d %d\n'%tuple(remap[i] for i in f) for f in b))
origkeep=np.r_[F[:n][~M],F[n:]]
assert len(origkeep)==len(F)-M.sum()
raw_def=hashlib.sha256(W[np.asarray(b[:len(origkeep)])].astype('<f8').tobytes()).hexdigest()
unchanged=hashlib.sha256(V[origkeep].astype('<f8').tobytes()).hexdigest();assert unchanged==raw_def
(D/'strip-stitch.json').write_text(json.dumps({'bbox_min_max':(B0.tolist(),B1.tolist()),'synthetic_collar_triangles':len(nxt),
 'retained_exterior_faces':len(origkeep),'roof_old_faces_replaced':int(M.sum()),'replacement_new_face_count':len(sf)+len(nxt),'same_exact_exterior_triangle_stream_sha256_f64':unchanged,
 'retained_profile_weight':retained_weight,'intermediate_pinned_old_collar_vertices':len(inter),'inner_measured_strip_triangles':len(sf),'fixed_outer_seam_edges':len(outer),'full_v_f_paired_edges':[len(used),len(b),len(E)],'candidate_obj_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2)+'\n')
print(len(used),len(b),len(E),len(nxt))
