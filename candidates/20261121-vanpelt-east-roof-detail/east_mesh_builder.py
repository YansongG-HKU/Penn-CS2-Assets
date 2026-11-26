"""Extended mesh builder preserving the pinned original roof-control partitions."""
from segment_east import *
def build(zlow,zmid,zattic,zwest,zeast_high,z0,out,raised_detail):
 regs=[('low_outer',body.Difference(mid),zlow),('connected_middle',mid.Difference(attic).Difference(west_penthouse),zmid),
   ('east_attic',attic.Difference(east_high_roof),zattic),('west_penthouse',west_penthouse,zwest),
   ('east_high_platform',east_high_roof,zeast_high)]
 for tag,p,z in raised_detail:
  n,og,gh=regs[2]; regs[2]=(n,og.Difference(p),gh); regs.append((tag,p,z))
 assert abs(sum(x[1].GetArea() for x in regs)-body.GetArea())<.002
 sur=[]; faces=[]; segments=[]
 zbase=z0-2.5
 for label,p,h in regs:
  for q in geom_polys(p):
   qr,rings=oriented(q)
   sur.append((label,*[np.c_[t,np.full(3,h)] for t in tris2(qr)]))
   sur.append(('base',*[np.c_[t[::-1],np.full(3,zbase)] for t in tris2(qr)]))
   for r in rings:
    for u,v in zip(r,np.roll(r,-1,axis=0)):
     segments.append((u,v,h,label))
 # Node seams by XY to ensure edge matching when one section subdivides a shared line.
 pts=np.unique(np.array([q for s in segments for q in s[:2]]),axis=0)
 ed=collections.defaultdict(list)
 for u,v,h,label in segments:
  e=v-u;t=((pts-u)@e)/(e@e);d=np.linalg.norm(pts-u-t[:,None]*e,axis=1)
  mask=(t>1e-6)&(t<1-1e-6)&(d<.00005)
  chain=[u,*pts[mask][np.argsort(t[mask])],v]
  for a,b in zip(chain,chain[1:]):
   p,q=tuple(a),tuple(b);ed[tuple(sorted([p,q]))].append((p,q,h,label))
 for k,els in ed.items():
  assert len(els)<=2,els
  a,b,h,n=max(els,key=lambda x:x[2])
  low=zbase if len(els)==1 else min(e[2] for e in els)
  if len(els)==2:
   assert els[0][0]==els[1][1] and els[0][1]==els[1][0],els
  if abs(h-low)<.00001:continue
  q=np.array([[*a,h],[*a,low],[*b,low],[*b,h]],float)
  sur.append(('wall:'+n,q[[0,1,2]],q[[0,2,3]]))
 V,F,T=clean_surfaces(sur)
 E=collections.defaultdict(list)
 for j,f in enumerate(F):
  for a,b in zip(f,f[1:]+f[:1]):E[tuple(sorted((a,b)))].append((a,b,j))
 bad=[(V[list(k)].tolist(),[(a,b,T[j]) for a,b,j in v]) for k,v in E.items() if len(v)!=2 or v[0][:2]!=v[-1][:2][::-1]]
 print('mesh',len(V),len(F),len(E),'errors',len(bad),bad[:12]); assert not bad
 V[:,2]-=z0
 A=V[np.asarray(F)]
 areas=np.linalg.norm(np.cross(A[:,1]-A[:,0],A[:,2]-A[:,0]),axis=1)*.5
 vol=float((A[:,0]*np.cross(A[:,1],A[:,2])).sum()/6.); assert vol>20000 and min(areas)>1e-6,(vol,min(areas))
 out.write_text('# Van Pelt-Dietrich Library: offline roof massing from NOAA/Philadelphia sources.\n# Synthetic vertical walls and hidden skirt. Excludes south steps and other facade detail.\no Van_Pelt_Roof_Massing\n'+
   ''.join('v %.5f %.5f %.5f\n'%tuple(x) for x in V)+''.join('f %d %d %d\n'%tuple(i+1 for i in row) for row in F))
 return dict(verts=len(V),tris=len(F),oriented_edges=len(E),bad_edges=0,min_face_area_m2=float(min(areas)),signed_volume_m3=vol,
  extent_m=[V.min(axis=0).tolist(),V.max(axis=0).tolist()],sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
  retained_footprint_area_m2=body.GetArea(),body_vs_full_difference_m2=body.SymDifference(foot).GetArea(),
  roof_patches=[dict(name=n,area_m2=g.GetArea(),z_m=h) for n,g,h in regs])
