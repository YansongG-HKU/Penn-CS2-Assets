"""Verify full planar opposing cap border, adjacent directions and third-party surface clearance."""
import collections,hashlib,json,sys
from pathlib import Path
from io_scene_fbx import parse_fbx
d,topology,output=map(Path,sys.argv[sys.argv.index('--')+1:])
from repair_batch import item,prop,steered_edges
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def overlap(p,q):
 if cross(*q)<0:q=q[::-1]
 for a,b in zip(q,q[1:]+q[:1]):
  new=[]
  for x,y in zip(p[-1:]+p[:-1],p):
   u,v=cross(a,b,x),cross(a,b,y)
   if (u>=0)!=(v>=0):new.append(tuple(i+(j-i)*u/(u-v) for i,j in zip(x,y)))
   if v>=0:new.append(y)
  p=new
 return abs(sum(cross(p[0],a,b) for a,b in zip(p[1:],p[2:])))/2
def interior(p,q,ring):
 lo,hi=0.,1.
 for a,b in zip(ring,ring[1:]+ring[:1]):
  x,z=cross(a,b,p)-1e-7,cross(a,b,q)-1e-7
  if x<0 and z<0:return False
  if x*z<0:
   t=x/(x-z)
   if x<0:lo=max(lo,t)
   else:hi=min(hi,t)
  if lo>hi:return False
 return True
def scan(p,axis,capA,capB):
 r,ver=parse_fbx.parse(str(p));g=item(item(r,b'Objects'),b'Geometry')
 v,l=[prop(g,k) for k in (b'Vertices',b'PolygonVertexIndex')]
 assert len(l)%3==0 and all((x<0)==(i%3==2) for i,x in enumerate(l))
 V=[tuple(v[i:i+3]) for i in range(0,len(v),3)]
 F=[tuple(x if x>=0 else -1-x for x in l[i:i+3]) for i in range(0,len(l),3)]
 E=steered_edges(F); assert all(len(x)==2 and x[0][:2]==x[1][:2][::-1] for x in E.values())
 drop=set(capA+capB)
 s=[{i for k in cap for i in F[k]} for cap in (capA,capB)]
 pts=[{V[i]:i for i in group} for group in s]
 assert len(pts[0])==len(s[0]) and len(pts[1])==len(s[1]) and not s[0]&s[1] and pts[0].keys()==pts[1].keys()
 weld={pts[0][q]:pts[1][q] for q in pts[0]}
 Y,=set(q[axis] for q in pts[0])
 R=[]; sides=[]
 flat=lambda a:tuple(v for j,v in enumerate(a) if j!=axis)
 for cap in (capA,capB):
  edge=steered_edges([F[k] for k in cap])
  border=set();side=set(); h={}
  for k,v in edge.items():
   if len(v)==2:continue
   assert len(v)==1
   a,b=v[0][:2]
   other,=[i//3 for x,y,i in E[k] if i//3 not in drop]
   x,=[V[x][axis]-Y for x in F[other] if x not in k]
   assert abs(x)>1e-7
   border.add((V[a],V[b]));side.add(x>0);h[str(other)]=x
  assert len(side)==1 and len(border)==len(s[len(R)])
  R.append(border);sides.append(h)
 assert R[0]=={(b,a) for a,b in R[1]}
 assert (next(iter(sides[0].values()))>0)!=(next(iter(sides[1].values()))>0)
 successor={flat(a):flat(b) for a,b in R[0]}; cur=min(successor);ring=[]
 for _ in successor:ring.append(cur);cur=successor[cur]
 assert cur==ring[0] and len(set(ring))==len(successor)
 if cross(*ring[:3])<0:ring.reverse()
 assert all(cross(ring[i-2],ring[i-1],ring[i])>1e-8 for i in range(len(ring)))
 cap_tri=[[flat(V[i]) for i in F[j]] for j in capA]
 check=[]
 for j,f in enumerate(F):
  if j in drop:continue
  vv=[V[i] for i in f]; zz=[p[axis]-Y for p in vv]
  if all(abs(z)<1e-9 for z in zz):
   if any(overlap(q,list(map(flat,vv)))>1e-8 for q in cap_tri):check.append([j,'coplanar_overlap'])
   continue
  q=[]
  for a,b,z,w in zip(vv,vv[1:]+vv[:1],zz,zz[1:]+zz[:1]):
   if abs(z)<1e-9:q.append(flat(a))
   if z*w<0:q.append(tuple(x+z/(z-w)*(y-x) for x,y in zip(flat(a),flat(b))))
  if q and interior(q[0],q[-1],ring):check.append([j,'pierces_open_cap'])
 new=steered_edges([tuple(weld.get(k,k) for k in f) for i,f in enumerate(F) if i not in drop])
 assert all(len(x)==2 and x[0][:2]==x[1][:2][::-1] for x in new.values())
 return dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),axis=axis,plane_m=Y,caps=[capA,capB],exact_weld=weld,
  attachments=sides,third_party_intersections=check,old_triangles=len(F),new_triangles=len(F)-len(drop),
  old_vertices=len(V),new_vertices=len(V)-len(weld),closed_oriented_edges=len(new))
S={}
for p in sorted(d.glob('*.fbx')):
 if 'Quad' in p.name:
  t=json.loads(topology.read_text())[p.name]['exact_opposed_geometry']
  if len(t)!=2:continue
  S[p.name]=scan(p,2,[i[0] for i in t],[i[1] for i in t])
 elif 'IrvineAuditorium' in p.name:
  S[p.name]=scan(p,1,[36,90,91,92,93,94],[41,103,104,105,106,107])
output.write_text(json.dumps(S,indent=2)+'\n')
print({k:v['third_party_intersections'] for k,v in S.items()})
