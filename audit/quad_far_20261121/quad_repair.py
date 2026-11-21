"""Repair only the proved, exact 28-vertex split Quad LOD2 massing template."""
import sys,types,json,hashlib,math,collections
from pathlib import Path
import numpy as np
mod=types.ModuleType('io_scene_fbx');mod.__path__=['/usr/share/blender/scripts/addons_core/io_scene_fbx'];sys.modules[mod.__name__]=mod
from io_scene_fbx import parse_fbx,encode_bin
D=Path(__file__).resolve().parent
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def one(e,k):
 a=[x for x in e.elems if x.id==k];assert len(a)==1,(k,len(a));return a[0]
def val(e,k):return one(e,k).props[0]
def edges(f):return list(zip(f,f[1:]+f[:1]))
def tol(q,n=1e-9):return abs(q)<n
def repair(p,o,source_sha):
 assert H(p)==source_sha
 r,ver=parse_fbx.parse(str(p));assert ver==7400
 g=one(one(r,b'Objects'),b'Geometry')
 assert {x.id for x in g.elems}=={b'Properties70',b'GeometryVersion',b'Vertices',b'PolygonVertexIndex',b'Edges',b'LayerElementSmoothing',b'LayerElementNormal',b'LayerElementUV',b'LayerElementMaterial',b'Layer'}
 V,I,E=map(lambda k:val(g,k),(b'Vertices',b'PolygonVertexIndex',b'Edges'))
 U=one(g,b'LayerElementUV');N=one(g,b'LayerElementNormal');S=one(g,b'LayerElementSmoothing')
 uv,ui=val(U,b'UV'),val(U,b'UVIndex');nn,ni=val(N,b'Normals'),val(N,b'NormalsIndex');smooth=val(S,b'Smoothing')
 assert all(val(x,b'MappingInformationType')==b'ByPolygonVertex' and val(x,b'ReferenceInformationType')==b'IndexToDirect' for x in (U,N))
 assert val(S,b'MappingInformationType')==b'ByPolygon' and val(one(g,b'LayerElementMaterial'),b'MappingInformationType')==b'AllSame'
 f=[]; addr=[];row=[];at=[]
 for j,i in enumerate(I):
  row.append(i if i>=0 else -i-1);at.append(j)
  if i<0:f.append(row);addr.append(at);row=[];at=[]
 v=list(zip(*[iter(V)]*3));assert len(v)==28 and len(f)==22
 assert f==[[0,1,3,2],[2,3,7,6],[6,7,5,4],[4,5,1,0],[2,6,4,0],[7,3,1,5],[8,9,11,10],[10,11,15,14],[14,15,13,12],[12,13,9,8],[10,14,12,8],[15,11,9,13],[16,19,18,17],[16,17,21,20],[17,18,21],[16,20,19],[19,20,21,18],[22,23,24,25],[22,26,27,23],[23,27,24],[22,25,26],[25,24,27,26]]
 H1=v[9][2];H2=v[20][2]
 A,B=v[7][:2];P,Q=v[15][:2];R,T=v[23][:2]
 assert 0<P<R<A and 0<Q<T<B and 0<H1<H2
 expected=[]
 for x,y in [(-A,-B),(-A,B),(A,-B),(A,B)]:expected.extend([(x,y,v[0][2]),(x,y,0.)])
 assert -.051<v[0][2]<-.049
 for x,y in [(-P,-Q),(-P,Q),(P,-Q),(P,Q)]:expected.extend([(x,y,0.),(x,y,H1)])
 expected +=[(-R,-T,H1),(R,-T,H1),(R,0.,H1),(-R,0.,H1),(-R,0.,H2),(R,0.,H2),(-R,T,H1),(R,T,H1),(R,0.,H1),(-R,0.,H1),(-R,0.,H2),(R,0.,H2)]
 assert v==expected,'changed dimensions or off-center model'
 v +=[(-P,0.,H1),(P,0.,H1)]
 weld={24:18,25:19,26:20,27:21};assert all(v[k]==v[j] for k,j in weld.items())
 kept=[];new=[];io=[];ino=[];sm=[];added_uv=list(uv);err=[];maps=[]
 def append(ids,orig,exact=False):
  orig_idx={i:j for i,j in zip(f[orig],addr[orig])}
  u={i:ui[j] for i,j in orig_idx.items()}
  n={i:ni[j] for i,j in orig_idx.items()}
  if not all(i in u for i in ids):
   ax=[i for i in range(3) if len({v[j][i] for j in f[orig]})>1]; assert len(ax)==2
   Y=np.asarray([uv[2*u[j]:2*u[j]+2] for j in f[orig]])
   X=np.asarray([[v[j][k] for k in ax]+[1] for j in f[orig]])
   t,_,rank,_=np.linalg.lstsq(X,Y,rcond=None);assert rank==3
   e=float(np.abs(X@t-Y).max());assert e<2.5e-7,(p,orig,e);err.append(e)
   assert len(set(n.values()))==1
   for j in ids:
    if j not in u:
     u[j]=len(added_uv)//2
     added_uv.extend((np.asarray([v[j][k] for k in ax]+[1])@t).tolist())
     n[j]=next(iter(n.values()))
  if exact:kept.append([orig,len(new)])
  maps.append(orig);new.append(ids);io.extend(u[j] for j in ids);ino.extend(n[j] for j in ids);sm.append(smooth[orig])
 for k,row in enumerate(f):
  if k in (5,10,11,12,16,17,21):continue
  if k in (6,8):append(row[:2]+[28 if k==6 else 29]+row[2:],k)
  else:append(row,k,True)
 # Preserve the positive top plate outside the body; all original plate corners remain.
 outer=f[5];inner=[14,10,8,12]
 for i,j in zip(range(4),[1,2,3,0]):append([outer[i],outer[j],inner[j],inner[i]],5)
 # Retain downward roof overhang, with independent old UV charts from each original half.
 outer=[16,19,22,23,24,17];inner=[9,28,11,15,29,13]
 # Upper chart has source vertex 25 (rather than its welded equivalent 19).
 for i,j in zip(range(6),[1,2,3,4,5,0]):
  k=12 if i in (0,4,5) else 17
  ids=[outer[i],outer[j],inner[j],inner[i]]
  if k==12:ids=[18 if x==24 else x for x in ids]
  else:ids=[25 if x==19 else x for x in ids]
  append(ids,k)
 order=[i for i in range(len(v)) if i not in weld];reidx={k:i for i,k in enumerate(order)}
 new=[[reidx[weld.get(x,x)] for x in row] for row in new]
 edge=collections.defaultdict(list);edgeindices=[];loop=0
 for row in new:
  for j,(a,b) in enumerate(edges(row)):
   key=min(a,b),max(a,b)
   if not edge[key]:edgeindices.append(loop+j)
   edge[key].append((a,b))
  loop+=len(row)
 assert len(order)==26 and len(new)==25 and all(len(x)==2 and x[0]==x[1][::-1] for x in edge.values())
 gph=collections.defaultdict(set)
 for a,b in edge:gph[a].add(b);gph[b].add(a)
 assert len(gph)==26
 rem=set(range(1,len(order)));todo=[0]
 while todo:
  u=gph[todo.pop()]&rem;rem-=u;todo.extend(u)
 assert not rem
 patches=[(V,[q for j in order for q in v[j]]),(I,[q if i<len(row)-1 else -q-1 for row in new for i,q in enumerate(row)]),(E,edgeindices),(uv,added_uv),(ui,io),(ni,ino),(smooth,sm)]
 def assign(dst,src):dst[:]=type(dst)(dst.typecode,src)
 back=[list(a) for a,b in patches]
 for a,b in patches:assign(a,b)
 methods=dict(zip(b'BCZYILFDRSifdlbc',('add_bool','add_char','add_int8','add_int16','add_int32','add_int64','add_float32','add_float64','add_bytes','add_string','add_int32_array','add_float32_array','add_float64_array','add_int64_array','add_bool_array','add_byte_array')))
 def clone(x):
  e=encode_bin.FBXElem(x.id)
  for k,v in zip(x.props_type,x.props):getattr(e,methods[k])(v)
  e.elems=[clone(y) for y in x.elems];return e
 def sig(x):return(x.id,bytes(x.props_type),tuple(x.props),tuple(sig(y) for y in x.elems))
 with encode_bin.FBXElem.enable_multithreading_cm():payload=clone(r)
 encode_bin.write(str(o),payload,ver)
 a,t=parse_fbx.parse(str(o));assert t==ver and sig(a)==sig(r)
 for (a,b),row in zip(patches,back):assign(a,row)
 assert sig(r)==sig(parse_fbx.parse(str(p))[0])
 return dict(original_sha256=source_sha,candidate_sha256=H(o),old_triangles=40,new_triangles=sum(len(f)-2 for f in new),vertices=len(order),unchanged_face_mapping=kept,donor_face_mapping=maps,affine_fit_max_uv=max(err),
  original_pos_area_floor_m2=4*P*Q,original_pos_area_roof_m2=4*P*Q,original_pos_area_ridge_m2=2*R*(H2-H1),new_visible_floor_m2=4*(A*B-P*Q),new_visible_eaves_m2=4*(R*T-P*Q),dims_m=[A,B,P,Q,R,T,H1,H2])
if __name__=='__main__':
 src=D/'input';dest=D/'quad-fixed';dest.mkdir(exist_ok=True)
 w=json.loads((D/'screen.json').read_text())['assets'];result={}
 for name,row in w.items():
  if not (name.startswith('Quad') and row['triangles']==40):continue
  try:result[name]=repair(src/(name+'.fbx'),dest/(name+'.fbx'),row['sha256'])
  except Exception as e:
   import traceback;traceback.print_exc();print(name,str(e));break
 print('rebuilt',len(result));(D/'quad-raw.json').write_text(json.dumps(result,indent=2)+'\n')
 assert len(result)==32
