"""Fresh Blender readback with exact unchanged attributes, closed bound and visual ray metrics."""
from pathlib import Path
import bpy, math, json, collections, sys, hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
D=Path(sys.argv[sys.argv.index('--')+1]).resolve()
A=json.loads((D/'raw.json').read_text())
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(x, asset):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.fbx(filepath=str(x),use_image_search=False)
 ob,=[a for a in bpy.context.scene.objects if a.type=='MESH'];m=ob.data; m.calc_loop_triangles()
 assert not m.validate(verbose=True,clean_customdata=False)
 scene={i.name:(Path(i.filepath).name,tuple(i.size)) for i in bpy.data.images if i.source=='FILE'}
 field=[[[tuple(m.uv_layers.active.data[j].uv),tuple(m.corner_normals[j].vector)] for j in f.loop_indices] for f in m.polygons]
 m.calc_tangents()
 field=[(ff,[(tuple(m.loops[j].tangent),float(m.loops[j].bitangent_sign),tuple(m.loops[j].bitangent)) for j in f.loop_indices],f.material_index,f.use_smooth) for ff,f in zip(field,m.polygons)]
 v=[o.matrix_world@z.co for z in m.vertices for o in [ob]]; tf=[tuple(t.vertices) for t in m.loop_triangles]; ids=[t.polygon_index for t in m.loop_triangles]
 assert len(ids)==len(tf)
 return v,tf,field,scene,[tuple(f.vertices) for f in m.polygons],ids
def e(F):
 E=collections.defaultdict(list)
 for ff in F:
  for a,b in zip(ff,ff[1:]+ff[:1]):E[min(a,b),max(a,b)].append((a,b))
 return E
def HN(E):return dict(collections.Counter(map(len,E.values())))
def evalhit(B,V,F,U,P,d):
 q,_,ix,_=B.ray_cast(P,d,200)
 if q is None:return None,None,ix
 a,b,c=[V[k] for k in F[ix]]
 sub=lambda a,b:tuple(float(x)-float(y) for x,y in zip(a,b));s=sub(b,a);t=sub(c,a);p=sub(q,a)
 dot=lambda a,b:sum(x*y for x,y in zip(a,b))
 aa,ab,bb=dot(s,s),dot(s,t),dot(t,t);pa,pb=dot(p,s),dot(p,t);n=aa*bb-ab*ab;assert n>0
 r=(pa*bb-pb*ab)/n;w=(pb*aa-pa*ab)/n
 y=[a[0] for a in U[ix][0]];uv=tuple(a*(1-r-w)+b*r+c*w for a,b,c in zip(*y))
 return q,uv,ix
rel='WistarInstitute/fbx/split/NA_WistarInstitute_17x8_LOD2.fbx'
old,new=(D/a/rel for a in ('old','fresh'))
assert H(old)==A['source_sha256'] and H(new)==A['patch_sha256']
v,f,a,im,p,ip=load(old,A);w,g,b,ims,q,iq=load(new,A)
assert v==w and im==ims and len(ims)==3 and all(s==[1024,1024] or s==(1024,1024) for _,s in ims.values())
assert len(f)==36 and len(g)==44 and len(w)==24
for j,i in enumerate(A['untouched_old_face_ids']):assert p[i]==q[j] and a[i]==b[j],(j,i)
Ee=e(g);assert len(Ee)==66 and all(len(p)==2 and p[0]==p[1][::-1] for p in Ee.values())
T0=BVHTree.FromPolygons(v,f,all_triangles=True);T1=BVHTree.FromPolygons(w,g,all_triangles=True)
# Translate per-polygon loops to per-triangle UV; only quads and triangles, all corner positions preserved.
z0=[tuple(a[k][0][p[k].index(i)][0] for i in ff) for k,ff in zip(ip,f)]
z1=[tuple(b[k][0][q[k].index(i)][0] for i in ff) for k,ff in zip(iq,g)]
def prep(row):return [([[(u[0],u[1]),None] for u in pp],) for pp in row]
b0,b1=prep(z0),prep(z1)
def hit(o,d):
 p0,u0,_=evalhit(T0,v,f,b0,o,d);p1,u1,_=evalhit(T1,w,g,b1,o,d)
 assert (p0 is None)==(p1 is None)
 if p0 is None:return None
 return math.dist(p0,p1),math.dist(u0,u1),p0.z,p1.z
out=[]
C=Vector((0,0,16))
for z in [(1,0,0),(0,1,0),(0,0,1),(0,0,-1),(1,-1,.28),(-.7,-1,.61),(1,1,-.3)]:
 d=Vector(z).normalized();P=d.cross(Vector((0,0,1)))
 if P.length<.01:P=Vector((1,0,0))
 P.normalize();Q=d.cross(P).normalized()
 for i in range(-42,43):
  for j in range(-42,43):
   o=C+d*169+P*(i*1.91+.12)+Q*(j*1.64+.351)
   p1=hit(o,-d)
   if p1:out.append(p1)
assert max(x[0] for x in out)<.00009 and max(x[1] for x in out)<.000004
led=[]
for i in range(171):
 for j in range(87):
  X=-68+(i+.261)*136/171;Y=-32+(j+.122)*64/87
  if (4.99<=X<=60.01 and -22.01<=Y<=22.01) or (-60.01<=X<=-4.99 and -18.01<=Y<=18.01):continue
  rr=hit(Vector((X,Y,.21)),Vector((0,0,-1)))
  assert rr and abs(rr[2])<1e-5 and abs(rr[3])<1e-5
  led.append(rr)
assert max(x[0] for x in led)<1e-5 and max(x[1] for x in led)<1e-6
internal=[]
for x0,x1,y0,y1,Z in [(-60,-5,-18,18,32),(5,60,-22,22,20.5)]:
 rr=[]
 for i in range(21):
  for j in range(17):
   X=x0+(i+.311)*(x1-x0)/21;Y=y0+(j+.271)*(y1-y0)/17
   a0,_,_=evalhit(T0,v,f,b0,Vector((X,Y,-.025)),Vector((0,0,1)))
   a1,_,_=evalhit(T1,w,g,b1,Vector((X,Y,-.025)),Vector((0,0,1)))
   assert a0 and a1 and abs(a0.z)<8e-6 and abs(a1.z-Z)<8e-6
   rr.append((a0.z,a1.z))
 internal.append([len(rr),min(x[1] for x in rr),max(x[1] for x in rr)])
t=[[list(v[i]) for i in ff] for ff in p];r=[[list(w[i]) for i in ff] for ff in q]
o=dict(reimport_triangles=[36,44],paired_edges=66,original_geometry_model_bounds=[(min(y),max(y)) for y in zip(*v)],untouched_exact_corner_faces=15,
 image_sha256={x.name:H(x) for x in sorted((D/'fresh'/'WistarInstitute'/'textures').glob('*.png'))}, directions=7,exterior_trials=85*85*7,
 exterior_hits=len(out),outside_max_delta_m=max(p[0] for p in out),outside_max_uv_delta=max(p[1] for p in out),
 exposed_plate_rays=len(led),plate_ray_max_uv_delta=max(p[1] for p in led),inside_rays=internal,
 z0_original_polys=[x for x in t if all(abs(w[2])<1e-5 for w in x)],z0_new_polys=[x for x in r if all(abs(w[2])<1e-5 for w in x)])
(D/'verified.json').write_text(json.dumps(o,indent=2)+'\n');print({k:v for k,v in o.items() if not k.startswith('z0')})
