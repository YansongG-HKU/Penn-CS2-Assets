import bpy,math,collections,json,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
D=Path(sys.argv[sys.argv.index('--')+1]).resolve()
raw=json.loads((D/'quad-raw.json').read_text())
def load(f):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.fbx(filepath=str(f),use_image_search=False)
 o,=[x for x in bpy.context.scene.objects if x.type=='MESH'];m=o.data;m.calc_loop_triangles()
 assert not m.validate(verbose=True,clean_customdata=False)
 v=[o.matrix_world@x.co for x in m.vertices]
 uv=[tuple(x.uv) for x in m.uv_layers.active.data]
 N=[tuple((o.matrix_world.to_3x3()@m.corner_normals[i].vector).normalized()) for i in range(len(m.loops))]
 F=[tuple(t.vertices) for t in m.loop_triangles];U=[tuple(uv[i] for i in t.loops) for t in m.loop_triangles]
 A=[([tuple(v[i]) for i in f.vertices], [uv[i] for i in f.loop_indices],[N[i] for i in f.loop_indices],f.use_smooth,f.material_index) for f in m.polygons]
 E=collections.defaultdict(list)
 for a in F:
  for i,j in zip(a,a[1:]+a[:1]):E[min(i,j),max(i,j)].append((i,j))
 return v,F,U,A,E,sorted(Path(i.filepath).name for i in bpy.data.images if i.source=='FILE')
def pull(B,V,F,U,o,d):
 q,_,i,_=B.ray_cast(o,d,250.)
 if q is None:return q,None
 f=F[i];a,b,c=[V[k] for k in f]
 sub=lambda u,v:tuple(float(i)-float(j) for i,j in zip(u,v));ab=sub(b,a);ac=sub(c,a);ap=sub(q,a)
 dot=lambda a,b:sum(float(x)*float(y) for x,y in zip(a,b))
 A,B,C=dot(ab,ab),dot(ab,ac),dot(ac,ac);D,E=dot(ap,ab),dot(ap,ac)
 t=A*C-B*B;assert t>0
 s=(C*D-B*E)/t;t=(A*E-B*D)/t;row=U[i]
 return q,tuple(row[0][j]*(1-s-t)+row[1][j]*s+row[2][j]*t for j in (0,1))
def compare(name,r):
 v,f,u,A,e,ims=load(D/'input'/(name+'.fbx'));B0=BVHTree.FromPolygons(v,f,all_triangles=True)
 w,g,uu,AA,ee,ims1=load(D/'quad-fixed'/(name+'.fbx'));B1=BVHTree.FromPolygons(w,g,all_triangles=True)
 assert len(f)==40 and len(g)==r['new_triangles']==48
 assert len(ee)==72 and all(len(q)==2 and q[0]==q[1][::-1] for q in ee.values())
 assert ims==ims1
 ext=lambda v:[tuple(map(q,zip(*v))) for q in (min,max)]
 assert ext(v)==ext(w)
 assert len(r['unchanged_face_mapping'])==13
 for a,b in r['unchanged_face_mapping']:assert A[a]==AA[b],(name,a,b)
 for a in (6,8):
  b=r['donor_face_mapping'].index(a)
  assert all(x==y[:2]+y[3:] for x,y in zip(A[a][:3],AA[b][:3]))
  assert A[a][3:]==AA[b][3:]
 def cmp(o,d):
  p,x=pull(B0,v,f,u,o,d);q,y=pull(B1,w,g,uu,o,d)
  assert (p is None)==(q is None),(name,o,d)
  if p is None:return None
  return math.dist(p,q),math.dist(x,y)
 rad=math.dist(*ext(v))/2
 C=Vector([(a+b)/2 for a,b in zip(*ext(v))]);R=rad+1.;X0,Y0,X1,Y1,X2,Y2,H1,H2=r['dims_m']
 rays=[]; n=0
 for ss in [(1,0,0),(0,1,0),(0,0,1),(0,0,-1),(-1,-1,.28),(1,-1,.61),(1,1,-.16)]:
  d=Vector(ss).normalized();p=d.cross(Vector((0,0,1)))
  if p.length<.01:p=Vector((1,0,0))
  p.normalize(); q=d.cross(p).normalized();step=R/24
  for i in range(-24,25):
   for j in range(-24,25):
    o=C+d*(rad*2+20)+p*((i+.259)*step)+q*((j+.439)*step)
    e=cmp(o,-d);n+=1
    if e is not None:rays.append(e)
 # Trace from close outside at the actual ledges rather than trusting silhouette rays alone.
 proven={}
 for tag,X,Y,IX,IY,z,s in [('floor',X0,Y0,X1,Y1,0,1),('eaves',X2,Y2,X1,Y1,H1,-1)]:
  local=[]
  for j in range(1,23):
   frac=(j+.241)/24
   for k in range(1,9):
    mix=(k+.319)/10
    for sign in (-1,1):
     for x,y in [(sign*(IX+mix*(X-IX)),(2*frac-1)*Y),((2*frac-1)*X,sign*(IY+mix*(Y-IY)))]:
      o=Vector((x,y,z+.041*s));d=Vector((0,0,-s))
      p,_=pull(B0,v,f,u,o,d);assert p and abs(p.z-z)<1e-5,(name,tag,o,p)
      local.append(cmp(o,d))
  assert all(x is not None for x in local)
  proven[tag]={'samples':len(local),'max_shift_m':max(x for x,y in local),'max_uv_delta':max(y for x,y in local)}
  assert proven[tag]['max_shift_m']<2e-5 and proven[tag]['max_uv_delta']<5e-6,(name,tag,proven)
 shift=max(x for x,y in rays); uv=max(y for x,y in rays)
 # Rays at exterior hits use single-precision BVH intersection and double-precision UV barycentrics.
 assert shift<.00009 and uv<.00008,(name,shift,uv)
 # Interior changes must be physical, not merely absence of index duplicates.
 inside=[]
 for label,o,d,z in [
  ('inside_plate',Vector((.01,.03,-.025)),Vector((0,0,1)),0.),
  ('inside_wall',Vector((.013,.029,H1/2)),Vector((0,0,1)),H1),
  ('south_attic_across_y0',Vector((.013,-Y2*.4,H1+.2*(H2-H1))),Vector((0,1,0)),None)]:
  a,_=pull(B0,v,f,u,o,d);b,_=pull(B1,w,g,uu,o,d);assert a and b
  j=2 if z is not None else 1
  assert abs(a[j]-(z or 0))<1e-5 and b[j]>a[j]+.02,(name,label,a,b)
  inside.append([label,list(a),list(b)])
 return dict(aabb_m=ext(w),outside_trials=n,outside_hits=len(rays),outside_max_shift_m=shift,outside_max_uv_delta=uv,ledge=proven,
  inside=inside,reimport_triangles=len(g),paired_oriented_edges=len(ee),unchanged_faces=13,material_image_paths=ims1)
out={}
for name,r in raw.items():
 out[name]=compare(name,r);print('Verified',name,out[name]['outside_max_shift_m'],out[name]['outside_max_uv_delta'],flush=True)
(D/'quad-verified.json').write_text(json.dumps(out,indent=2)+'\n')
