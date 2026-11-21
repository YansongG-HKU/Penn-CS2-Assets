from vanpelt_controls import *
from geos import tris2
from mesh import clean_surfaces
ogr.UseExceptions()
def rect(x0,x1,y0,y1):return polygon(np.array([[x0,y0],[x1,y0],[x1,y1],[x0,y1]]))
def ringpoints(r):return np.round(np.asarray(r.GetPoints())[:-1,:2],5)
def oriented(poly):
 rings=[]
 for i,r in enumerate(poly):
  r=ringpoints(r)
  if (flat(r)>0)!=(i==0):r=r[::-1]
  assert len(r)>=3 and abs(flat(r))>.001
  rings.append(r)
 g=polygon(rings[0])
 for r in rings[1:]:
  g.AddGeometry(polygon(r).GetGeometryRef(0))
 assert g.IsValid(),g.ExportToWkt()
 return g,rings
def geom_polys(g):
 if g is None or g.IsEmpty():return []
 if g.GetGeometryName()=='POLYGON':return [g]
 assert g.GetGeometryName() in ('MULTIPOLYGON','GEOMETRYCOLLECTION'),g.GetGeometryName()
 return [x for y in g if y.GetDimension()==2 for x in geom_polys(y)]
# Low stair projection is mapped only as measurement reference, not straight up to roof.
# Do not trim south wall to a rounded threshold outside the projection.
stairclip=rect(19.9,27.8,-32,-21.428)
north_gap_clip=rect(-17.85,.85,13.85,33)
body0=foot.Difference(stairclip).Difference(north_gap_clip)
body0=body0.SimplifyPreserveTopology(.025)
body,body_rings=oriented(body0)
assert len(body_rings)==1 and body.GetArea()>5300
def inside_d(p,xy):
 x,y=xy.T; b=np.zeros(len(x),bool); ds=np.full(len(x),1e6)
 for s,t in zip(p,np.roll(p,-1,axis=0)):
  v=t-s; dv=xy-s
  if abs(v[1])>1e-9:b^=((t[1]>y)!=(s[1]>y))&(x<(y-s[1])*v[0]/v[1]+s[0])
  d=dv-np.clip((dv@v)/(v@v),0,1)[:,None]*v
  ds=np.minimum(ds,np.einsum('ij,ij->i',d,d))
 return b,ds
# XY plane partitions picked from the 2025 orthophoto and training-source transects.
mid_xy=np.array([[-66.8,-4.55],[-21.8,-4.55],[-21.8,3.5],[4.05,3.5],[4.05,-20.30],[66.25,-20.30],
 [66.25,18.62],[4.05,18.62],[4.05,12.87],[-21.8,12.87],[-21.8,21.05],[-66.8,21.05]])
well=rect(-66.2,-56.25,3.95,12.1)
mid=(polygon(mid_xy).Intersection(body.Buffer(-.25))).Difference(well)
assert mid.IsValid() and mid.GetGeometryName()=='POLYGON'
attic=rect(10.2,57.95,-13.35,12.72)
west_penthouse=rect(-49.2,-40.35,4.05,12.52)
assert mid.Contains(attic) and mid.Contains(west_penthouse)
east_high_roof=rect(17.25,29.35,-3.42,4.34)
assert attic.Contains(east_high_roof)
def build(zlow,zmid,zattic,zwest,zeast_high,z0,out):
 regs=[('low_outer',body.Difference(mid),zlow),('connected_middle',mid.Difference(attic).Difference(west_penthouse),zmid),
   ('east_attic',attic.Difference(east_high_roof),zattic),('west_penthouse',west_penthouse,zwest),
   ('east_high_platform',east_high_roof,zeast_high)]
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
if __name__=='__main__':
 import tempfile
 with tempfile.TemporaryDirectory() as tmp: print(build(38.37,42.03,44.50,46.60,48.99,19.33,Path(tmp)/'test.obj'))
