"""Replace Wistar's full top plate with its exact exposed two-hole surface."""
from probe import one,val,read
from io_scene_fbx import parse_fbx,encode_bin
from pathlib import Path
from collections import defaultdict
from scipy.spatial import Delaunay
from osgeo import ogr
import math,numpy as np,hashlib,json
D=Path(__file__).resolve().parent;src=D.parent/'cs2-penn-portable'/'far-area'/'input'/'WistarInstitute.fbx'
dst=D/'new'/'NA_WistarInstitute_17x8_LOD2.fbx';dst.parent.mkdir(exist_ok=True)
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert H(src)=='dee11affdd028dc8b207a8e58815740e8a7ebce694a815341c6e1e7f88b53cfc'
r,ver,g,v,f=read(src);assert ver==7400 and len(v)==24 and len(f)==18 and all(len(p)==4 for p in f)
assert {x.id for x in g.elems}=={b'Properties70',b'GeometryVersion',b'Vertices',b'PolygonVertexIndex',b'Edges',b'LayerElementSmoothing',b'LayerElementNormal',b'LayerElementUV',b'LayerElementMaterial',b'Layer'}
def edges(x):return list(zip(x,x[1:]+x[:1]))
def area(x):return .5*sum(v[a][0]*v[b][1]-v[a][1]*v[b][0] for a,b in edges(x))
assert [area(f[k]) for k in (5,10,16)]==[8704.,-2420.,-1980.]
fix=[5,10,16];pts=[p for n in fix for p in f[n]];assert len(set(pts))==12 and all(v[i][2]==0 for i in pts)
def pg(ids):
 e=ogr.Geometry(ogr.wkbLinearRing)
 for i in ids:e.AddPoint_2D(*v[i][:2])
 e.CloseRings();g=ogr.Geometry(ogr.wkbPolygon);g.AddGeometry(e);assert g.IsValid();return g
outer,q0,q1=map(lambda i:pg(f[i]),fix)
assert not q0.Intersects(q1) and outer.Contains(q0) and outer.Contains(q1)
want=outer.Difference(q0).Difference(q1)
assert want.IsValid() and want.GetGeometryCount()==3 and want.GetArea()==4304.
new=[]
for row in Delaunay([v[i][:2] for i in pts]).simplices:
 ids=[pts[i] for i in row];assert area(ids)!=0
 if area(ids)<0:ids.reverse()
 q=pg(ids);area_here=q.GetArea()
 if want.Intersection(q).GetArea()==area_here:new.append(ids)
 else:assert q0.Intersection(q).GetArea()==area_here or q1.Intersection(q).GetArea()==area_here
new=[min(t,t[1:]+t[:1],t[2:]+t[:2]) for t in new];new.sort()
u=ogr.Geometry(ogr.wkbMultiPolygon)
for q in new:u.AddGeometry(pg(q))
assert len(new)==14 and sum(area(x) for x in new)==4304. and want.SymDifference(u.UnionCascaded()).GetArea()==0
U,N,S,M=[one(g,b'LayerElement'+k) for k in (b'UV',b'Normal',b'Smoothing',b'Material')]
for k,m,q in [(U,b'ByPolygonVertex',b'IndexToDirect'),(N,b'ByPolygonVertex',b'IndexToDirect'),(S,b'ByPolygon',b'Direct'),(M,b'AllSame',b'IndexToDirect')]:
 assert val(k,b'MappingInformationType')==m and val(k,b'ReferenceInformationType')==q
uv,ui=val(U,b'UV'),val(U,b'UVIndex');ni=val(N,b'NormalsIndex');smooth=val(S,b'Smoothing')
vm=list(uv);normal=ni[5*4:6*4];assert len(set(normal))==1
indices={vtx:ui[5*4+i] for i,vtx in enumerate(f[5])}
X=np.array([[*v[i][:2],1] for i in f[5]])
Y=np.array([uv[indices[i]*2:indices[i]*2+2] for i in f[5]])
a,_,rank,_=np.linalg.lstsq(X,Y,rcond=None);err=float(np.abs(X@a-Y).max());assert rank==3 and err<1e-7,err
for i in pts:
 if i not in indices:
  indices[i]=len(vm)//2;vm.extend((np.array([*v[i][:2],1])@a).tolist())
unchanged=[i for i in range(18) if i not in fix]
F=[f[i] for i in unchanged]+new
norms=[ni[4*i+j] for i in unchanged for j in range(4)]+[normal[0] for t in new for i in t]
uvinds=[ui[4*i+j] for i in unchanged for j in range(4)]+[indices[i] for t in new for i in t]
sm=[smooth[i] for i in unchanged]+[smooth[5] for t in new]
E=defaultdict(list);ei=[];lo=0;G=defaultdict(set)
for t in F:
 for j,(a,b) in enumerate(edges(t)):
  k=min(a,b),max(a,b)
  if not E[k]:ei.append(lo+j)
  E[k].append((a,b));G[a].add(b);G[b].add(a)
 lo+=len(t)
assert all(len(q)==2 and q[0]==q[1][::-1] for q in E.values()) and len(G)==24
todo=[0];left=set(range(1,len(v)))
while todo:
 u=todo.pop();a=G[u]&left;todo+=list(a);left-=a
assert not left and len(E)==51 and len(F)==29
c=[(val(g,b'PolygonVertexIndex'),[x if i<len(t)-1 else -x-1 for t in F for i,x in enumerate(t)]),(val(g,b'Edges'),ei),(uv,vm),(ui,uvinds),(ni,norms),(smooth,sm)]
def assign(d,q):d[:]=type(d)(d.typecode,q)
s0=[list(a) for a,b in c]
for a,b in c:assign(a,b)
methods=dict(zip(b'BCZYILFDRSifdlbc',('add_bool','add_char','add_int8','add_int16','add_int32','add_int64','add_float32','add_float64','add_bytes','add_string','add_int32_array','add_float32_array','add_float64_array','add_int64_array','add_bool_array','add_byte_array')))
def clone(x):
 e=encode_bin.FBXElem(x.id)
 for k,v in zip(x.props_type,x.props):getattr(e,methods[k])(v)
 e.elems=[clone(j) for j in x.elems];return e
def sig(x):return(x.id,bytes(x.props_type),tuple(x.props),tuple(sig(y) for y in x.elems))
with encode_bin.FBXElem.enable_multithreading_cm():payload=clone(r)
encode_bin.write(str(dst),payload,ver)
q,n=parse_fbx.parse(str(dst));assert n==ver and sig(q)==sig(r)
for (a,b),z in zip(c,s0):assign(a,z)
assert sig(r)==sig(parse_fbx.parse(str(src))[0])
o=dict(source_sha256=H(src),patch_sha256=H(dst),old_triangles=36,new_triangles=sum(len(f)-2 for f in F),untouched_old_face_ids=unchanged,
  new_plate_triangles=new,full_plate_m2=8704,removed_contacts_m2=[2420,1980],new_exposed_plate_m2=4304,max_affine_uv_fit_error=err,connected_closed_native_vertices=24,paired_edges_before_triangulation=51)
(D/'raw.json').write_text(json.dumps(o,indent=2)+'\n');print(o)
