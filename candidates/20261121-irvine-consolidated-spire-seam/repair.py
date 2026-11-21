"""Remove only the single fully covered opposing interface in authoritative split Irvine LOD2."""
import sys,json,collections,hashlib,math
from pathlib import Path
from io_scene_fbx import parse_fbx,encode_bin
src,out,rep=map(Path,sys.argv[sys.argv.index('--')+1:])
hashp=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert hashp(src)=='89aaa473cf65f76bb3a2a96b3b11b34312535f6766a5e84bdc1ddf82fce71dac' and not out.exists()
R,ver=parse_fbx.parse(str(src));assert ver==7400
def one(e,k):
 found=[v for v in e.elems if v.id==k]; assert len(found)==1,(k,len(found)); return found[0]
def val(e,k):return one(e,k).props[0]
g=one(one(R,b'Objects'),b'Geometry')
assert {v.id for v in g.elems}=={b'Properties70',b'GeometryVersion',b'Vertices',b'PolygonVertexIndex',b'Edges',b'LayerElementSmoothing',b'LayerElementNormal',b'LayerElementUV',b'LayerElementMaterial',b'Layer'}
V,I,E=(val(g,k) for k in (b'Vertices',b'PolygonVertexIndex',b'Edges'))
UV=one(g,b'LayerElementUV');N=one(g,b'LayerElementNormal');smooth=one(g,b'LayerElementSmoothing')
u,n,sm=val(UV,b'UVIndex'),val(N,b'NormalsIndex'),val(smooth,b'Smoothing')
assert all(val(s,b'MappingInformationType')==b'ByPolygonVertex' and val(s,b'ReferenceInformationType')==b'IndexToDirect' for s in (N,UV))
assert val(smooth,b'MappingInformationType')==b'ByPolygon' and val(smooth,b'ReferenceInformationType')==b'Direct'
assert val(one(g,b'LayerElementMaterial'),b'MappingInformationType')==b'AllSame'
vv=list(zip(*[iter(V)]*3)); faces=[];corners=[]; f=[]; cc=[]
for j,i in enumerate(I):
 f.append(i if i>=0 else -1-i);cc.append(j)
 if i<0:faces.append(f);corners.append(cc);f=[];cc=[]
assert len(vv)==64 and len(faces)==42 and sum(len(f)-2 for f in faces)==108
lo,hi=[i for i,f in enumerate(faces) if all(vv[v][2]==40.5 for v in f)]
assert (lo,hi)==(36,41)
a,b=faces[lo],faces[hi]
assert len(a)==len(b)==8 and set(a).isdisjoint(b)
A=[vv[i] for i in a];B=[vv[i] for i in b]
assert set(A)==set(B) and any(A==yr[-j:]+yr[:-j] for yr in [B[::-1]] for j in range(8))
fold={i:a[A.index(vv[i])] for i in b}
edges=lambda f:list(zip(f,f[1:]+f[:1]))
ring={tuple(sorted((vv[i],vv[j]))) for i,j in edges(a)}
for li,face in enumerate((a,b)):
 for i,j in edges(face):
  owners=[k for k,o in enumerate(faces) if k not in (lo,hi) and (j,i) in edges(o)]
  k,=owners
  signs={math.copysign(1,vv[v][2]-40.5) for v in faces[k] if vv[v][2]!=40.5}
  assert signs==({-1} if li==0 else {1})
# Prove original caps are hidden with opposite orientation and full mutual coverage.
area=abs(sum(p[0]*q[1]-p[1]*q[0] for p,q in zip(A,A[1:]+A[:1]))/2)
assert 7.23<area<7.25
order=[i for i in range(len(vv)) if i not in set(b)];nmap={i:j for j,i in enumerate(order)}
nr=[];ui=[];ni=[];s0=[]
for k,f in enumerate(faces):
 if k in (lo,hi):continue
 nr.append([nmap[fold.get(i,i)] for i in f])
 assert [vv[order[i]] for i in nr[-1]]==[vv[i] for i in f]
 ui.extend(u[i] for i in corners[k]);ni.extend(n[i] for i in corners[k]);s0.append(sm[k])
es=collections.defaultdict(list);iem=[]; offset=0
for row in nr:
 for j,(a0,b0) in enumerate(edges(row)):
  key=tuple(sorted((a0,b0)))
  if not es[key]:iem.append(offset+j)
  es[key].append((a0,b0))
 offset+=len(row)
assert len(order)==56 and len(nr)==40 and sum(len(f)-2 for f in nr)==96
assert all(len(x)==2 and x[0]==x[1][::-1] for x in es.values())
assert len(es)==88
edset={tuple(sorted((vv[order[i]],vv[order[j]]))) for i,j in es}
assert edset>=ring
pfx=lambda old,new:old.__setitem__(slice(None),type(old)(old.typecode,new))
for dest,content in [(V,(x for i in order for x in vv[i])),(I,(i if j<len(f)-1 else -1-i for f in nr for j,i in enumerate(f))),
   (E,iem),(u,ui),(n,ni),(sm,s0)]:pfx(dest,content)
methods=dict(zip(b'BCZYILFDRSifdlbc',('add_bool','add_char','add_int8','add_int16','add_int32','add_int64',
 'add_float32','add_float64','add_bytes','add_string','add_int32_array','add_float32_array','add_float64_array','add_int64_array','add_bool_array','add_byte_array')))
def clone(x):
 e=encode_bin.FBXElem(x.id)
 for t,v in zip(x.props_type,x.props):getattr(e,methods[t])(v)
 e.elems=[clone(y) for y in x.elems];return e
def state(x):return(x.id,bytes(x.props_type),tuple(x.props),tuple(state(y) for y in x.elems))
# Keep the official archive layout and precise existing relative references: no new paths.
with encode_bin.FBXElem.enable_multithreading_cm():payload=clone(R)
encode_bin.write(str(out),payload,ver)
T,v2=parse_fbx.parse(str(out));assert v2==ver and state(T)==state(R)
orig,_=parse_fbx.parse(str(src));go=one(one(orig,b'Objects'),b'Geometry')
for e,k,o in [(g,b'Vertices',go),(g,b'PolygonVertexIndex',go),(g,b'Edges',go),
 (UV,b'UVIndex',one(go,b'LayerElementUV')),(N,b'NormalsIndex',one(go,b'LayerElementNormal')),(smooth,b'Smoothing',one(go,b'LayerElementSmoothing'))]:
 pfx(val(e,k),val(o,k))
assert state(orig)==state(R)
rep.write_text(json.dumps({'source_sha256':hashp(src),'candidate_sha256':hashp(out),'raw_export_version':ver,'old_triangles':108,'new_triangles':96,
 'retained_polygons':40,'paired_polygon_edges':len(es),'new_vertices':56,'merged_coincident_ring_pairs':8,'both_caps_each_covered_m2':area,
 'old_coplanar_z_m':40.5,'opposite_coverage_areas_after_m2':[0,0],'kept_vertices_uv_normals_smoothing_material_paths':'exact'},indent=2)+'\n')
print(rep.read_text())
