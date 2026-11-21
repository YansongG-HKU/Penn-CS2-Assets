"""Rebase all three proved interior contacts onto the canonical Van Pelt split LOD2."""
import sys,json,collections,math,hashlib
from pathlib import Path
from io_scene_fbx import parse_fbx,encode_bin
p,o,t=map(Path,sys.argv[sys.argv.index('--')+1:])
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert h(p)=='0a9c0209d9a2834ae9746e6e63c571e0863d5c68b3eff15dbb74922f2762789a' and not o.exists()
def one(e,k):
 a=[x for x in e.elems if x.id==k];assert len(a)==1,(k,len(a));return a[0]
def val(e,k):return one(e,k).props[0]
r,ver=parse_fbx.parse(str(p));assert ver==7400
g=one(one(r,b'Objects'),b'Geometry')
assert {x.id for x in g.elems}=={b'Properties70',b'GeometryVersion',b'Vertices',b'PolygonVertexIndex',b'Edges',b'LayerElementSmoothing',b'LayerElementNormal',b'LayerElementUV',b'LayerElementMaterial',b'Layer'}
V,I,E=map(lambda k:val(g,k),(b'Vertices',b'PolygonVertexIndex',b'Edges'))
U=one(g,b'LayerElementUV');N=one(g,b'LayerElementNormal');S=one(g,b'LayerElementSmoothing')
uv,ui=val(U,b'UV'),val(U,b'UVIndex');nn,ni=val(N,b'Normals'),val(N,b'NormalsIndex'); smooth=val(S,b'Smoothing')
assert all(val(x,b'MappingInformationType')==b'ByPolygonVertex' and val(x,b'ReferenceInformationType')==b'IndexToDirect' for x in (U,N))
assert val(S,b'MappingInformationType')==b'ByPolygon' and val(one(g,b'LayerElementMaterial'),b'MappingInformationType')==b'AllSame'
v=list(zip(*[iter(V)]*3));f=[[x if x>=0 else -1-x for x in I[j:j+4]] for j in range(0,len(I),4)]
assert len(v)==32 and len(f)==24 and all((i%4==3)==(x<0) for i,x in enumerate(I))
edges=lambda f:list(zip(f,f[1:]+f[:1]))
new=[]; io=[];ino=[];sm=[]; added_uv=list(uv);weld={};check=[]
def xy(i):return v[i][:2]
def signed_area(poly):
 return .5*sum(a[0]*b[1]-a[1]*b[0] for a,b in edges([xy(k) for k in poly]))
def append(f0,u0,n0,s0):
 new.append(f0); io.extend(u0); ino.extend(n0);sm.append(s0)
for k,row in enumerate(f):
 if k not in (5,10,11,16,17,22):append(row,list(ui[4*k:4*k+4]),list(ni[4*k:4*k+4]),smooth[k])
for top,btm,z in [(5,10,0.0),(11,16,4.8),(17,22,22.0)]:
 A=f[top];B=f[btm];a0=signed_area(A);b0=-signed_area(B);assert a0>=b0>0
 assert max(abs(v[i][2]-z) for i in A+B)<1e-6
 for li,poly in enumerate((A,B)):
  for i,j in edges(poly):
   owners=[k for k,q in enumerate(f) if k not in (top,btm) and (j,i) in edges(q)]
   k,=owners
   assert {math.copysign(1,v[q][2]-v[poly[0]][2]) for q in f[k] if v[q][2]!=v[poly[0]][2]}==({-1} if li==0 else {1})
 extent=lambda ff:[(min(v[i][j] for i in ff),max(v[i][j] for i in ff)) for j in (0,1)]
 ea,eb=extent(A),extent(B)
 same=ea==eb
 assert a0==math.prod(b-a for a,b in ea) and b0==math.prod(b-a for a,b in eb)
 assert len({xy(i) for i in A})==len({xy(i) for i in B})==4
 field_residual=0.
 if same:
  assert set(xy(i) for i in A)==set(xy(i) for i in B)
  weld.update({b:next(a for a in A if xy(a)==xy(b)) for b in B})
 else:
  assert all(a0<b0<b1<a1 for (a0,a1),(b0,b1) in zip(ea,eb))
  def corner_label(i,e):return tuple(abs(v[i][k]-e[k][1])<1e-10 for k in (0,1))
  by={corner_label(i,eb):i for i in B}; inside=[by[corner_label(a,ea)] for a in A]
  topU=list(ui[4*top:4*top+4]); topN=list(ni[4*top:4*top+4]);assert len(set(topN))==1
  mapping={corner_label(i,ea):tuple(uv[2*j:2*j+2]) for i,j in zip(A,topU)}
  def interp(i):
   s,t=[(v[i][k]-u0)/(u1-u0) for k,(u0,u1) in enumerate(ea)]
   return [sum(v2[ix]*(s if a else 1-s)*(t if b else 1-t) for (a,b),v2 in mapping.items()) for ix in (0,1)]
  ds=tuple(mapping[0,0][j]+mapping[1,1][j]-mapping[0,1][j]-mapping[1,0][j] for j in (0,1))
  field_residual=math.hypot(*ds);assert field_residual<1.3e-7
  nu=[]
  for i in inside:nu.append(len(added_uv)//2);added_uv.extend(interp(i))
  ring=[]
  for i in range(4):
   j=(i+1)%4; row=[A[i],A[j],inside[j],inside[i]]; ring.append(row)
   append(row,[topU[i],topU[j],nu[j],nu[i]],topN,smooth[top])
  assert abs(sum(signed_area(q) for q in ring)-(a0-b0))<1e-9 and all(signed_area(q)>0 for q in ring)
 check.append({'plane_z_m':z,'outer_m2':a0,'original_opposite_coverage_m2':[b0,b0],'visible_annulus_m2':a0-b0,'after_opposite_coverage_m2':[0,0],
   'old_quad_uv_mixed_term_norm':field_residual,'vertical_ring_mismatch_m':abs(v[A[0]][2]-v[B[0]][2])})
order=[i for i in range(len(v)) if i not in weld];reidx={k:i for i,k in enumerate(order)}
new=[[reidx[weld.get(x,x)] for x in row] for row in new]
edge=collections.defaultdict(list); edgeindices=[]
for k,f0 in enumerate(new):
 for j,(a,b) in enumerate(edges(f0)):
  key=min(a,b),max(a,b)
  if not edge[key]:edgeindices.append(k*4+j)
  edge[key].append((a,b))
assert len(order)==28 and len(new)==26 and len(edge)==52
assert all(len(x)==2 and x[0]==x[1][::-1] for x in edge.values())
gph=collections.defaultdict(set)
for a,b in edge:gph[a].add(b);gph[b].add(a)
left=set(range(1,len(order))); st=[0]
while st:
 latest=gph[st.pop()]&left;left-=latest;st.extend(latest)
assert not left
patches=[(V,[q for j in order for q in v[j]],g,b'Vertices'),(I,[q if i<3 else -q-1 for row in new for i,q in enumerate(row)],g,b'PolygonVertexIndex'),
 (E,edgeindices,g,b'Edges'),(uv,added_uv,U,b'UV'),(ui,io,U,b'UVIndex'),(ni,ino,N,b'NormalsIndex'),(smooth,sm,S,b'Smoothing')]
def assign(dst,src):dst[:]=type(dst)(dst.typecode,src)
oldvalues=[list(b) for b,*_ in patches]
for a,b,_,_ in patches:assign(a,b)
methods=dict(zip(b'BCZYILFDRSifdlbc',('add_bool','add_char','add_int8','add_int16','add_int32','add_int64','add_float32','add_float64','add_bytes','add_string','add_int32_array','add_float32_array','add_float64_array','add_int64_array','add_bool_array','add_byte_array')))
def clone(x):
 e=encode_bin.FBXElem(x.id)
 for k,v in zip(x.props_type,x.props):getattr(e,methods[k])(v)
 e.elems=[clone(y) for y in x.elems];return e
def sig(x):return(x.id,bytes(x.props_type),tuple(x.props),tuple(sig(y) for y in x.elems))
with encode_bin.FBXElem.enable_multithreading_cm():payload=clone(r)
encode_bin.write(str(o),payload,ver)
A,ver1=parse_fbx.parse(str(o));assert ver1==ver and sig(A)==sig(r)
for (a,*_),value in zip(patches,oldvalues):assign(a,value)
assert sig(r)==sig(parse_fbx.parse(str(p))[0])
q={'source_sha256':h(p),'candidate_sha256':h(o),'export_version':ver,'old_triangles':48,'new_triangles':52,'new_vertices':28,
 'one_closed_connected_component':True,'paired_edges_on_quads':52,'unmodified_face_corner_uv_and_normals':18,'seams':check}
t.write_text(json.dumps(q,indent=2)+'\n');print(q)
