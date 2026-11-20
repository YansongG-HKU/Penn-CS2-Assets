"""Irvine diagnostic city-outline shell sampled from coincident NOAA observations.
Not construction documents or a texture/LOD prefab.
"""
import collections,ctypes as ct,json,hashlib,sys
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from osgeo import ogr
ogr.UseExceptions()
point_path,foot_path,frame_path,out=map(Path,sys.argv[1:]);out.mkdir(exist_ok=True)
source=json.loads(foot_path.read_text()); ref=json.loads(frame_path.read_text())
raw=np.array(source['local_footprint'][:-1]); points=np.load(point_path)['data']
assert len(points)==205337 and source['source_bin']=='1385697'
# Keep the authoritative chain; remove under 1.5 cm back-to-back slivers only.
foot=[raw[0]]
for s in raw[1:]:
    if np.linalg.norm(foot[-1]-s)>.015:foot.append(s)
if np.linalg.norm(foot[-1]-foot[0])<.015:foot=foot[:-1]
foot=np.array(foot)
z0=14.4; hidden_base=13.75; step=.64
def flat(P):
    q=np.roll(P,-1,axis=0)
    return float(np.sum(P[:,0]*q[:,1]-P[:,1]*q[:,0])/2)
if flat(foot)<0:foot=foot[::-1]
def poly(p):
    ring=ogr.Geometry(ogr.wkbLinearRing)
    for x,y in p:ring.AddPoint_2D(float(x),float(y))
    ring.CloseRings();g=ogr.Geometry(ogr.wkbPolygon);g.AddGeometry(ring);return g
P=poly(foot)
assert P.IsValid() and abs(P.GetArea()-source['area_plan_m2'])<.015
def geos():
    g=ct.CDLL('libgeos_c.so.1');ptr=ct.c_void_p
    def fn(name,args,r):
        f=getattr(g,name);f.argtypes=args;f.restype=r;return f
    c=fn('GEOS_init_r',[],ptr)();rd=fn('GEOSWKTReader_create_r',[ptr],ptr)(c);ht=fn('GEOSWKTWriter_create_r',[ptr],ptr)(c)
    fs=[fn('GEOSWKTReader_read_r',[ptr,ptr,ct.c_char_p],ptr),fn('GEOSConstrainedDelaunayTriangulation_r',[ptr,ptr],ptr),
        fn('GEOSWKTWriter_write_r',[ptr,ptr,ptr],ptr),fn('GEOSFree_r',[ptr,ptr],None),fn('GEOSGeom_destroy_r',[ptr,ptr],None)]
    return c,rd,ht,fs
ctx,reader,writer,(gread,gtri,gwrite,gfree,gclose)=geos()
def simple_tris(s):
    n=read=gread(ctx,reader,s.ExportToWkt().encode());td=gtri(ctx,n);assert td
    st=gwrite(ctx,writer,td);o=ogr.CreateGeometryFromWkt(ct.string_at(st).decode())
    gfree(ctx,st);gclose(ctx,td);gclose(ctx,n)
    for t in o:
        a=np.array(t.GetGeometryRef(0).GetPoints())[:-1,:2]
        assert len(a)==3
        yield a if flat(a)>0 else a[::-1]
V=[]; iv={}; F=[]; patches=[]
def iof(pt):
    k=tuple(np.round(pt,7))
    if k not in iv:iv[k]=len(V);V.append(k)
    return iv[k]
def hit(g,q):
    # Input polygon may cause tiny disjoint clipped slivers; preserve all nonzero area.
    if g.GetGeometryName()=='POLYGON':
        if g.GetArea()<1e-9:return
        for U in simple_tris(g):
            f=tuple(map(iof,U))
            assert len(set(f))==3 and flat(U)>1.e-9
            F.append(f);patches.append(q)
    elif g.GetGeometryName() in ('MULTIPOLYGON','GEOMETRYCOLLECTION'):
        for x in g:hit(x,q)
lo=np.floor(foot.min(0)/step).astype(int);hi=np.ceil(foot.max(0)/step).astype(int)
for i in range(lo[0],hi[0]):
    for j in range(lo[1],hi[1]):
        b=poly(np.array([[i,j],[i+1,j],[i+1,j+1],[i,j+1]])*step)
        if not P.Intersects(b):continue
        hit(P.Intersection(b),(i,j))
V=np.array(V); F=np.array(F)
pt=points
LC=(pt[:,:2]-ref['plane_meeting_utm_xy'])@np.column_stack([ref['local_east_axis_utm'],ref['local_north_axis_utm']])
z=pt[:,2]; held=np.isin(pt[:,4],[19,20])
def inside_and_edge(X):
    b=np.zeros(len(X),bool);d=np.full(len(X),99999.)
    x,y=X.T
    for u,v in zip(foot,np.roll(foot,-1,axis=0)):
        h=v-u
        if abs(h[1])>1.e-8:b^=((y>v[1])!=(y>u[1]))&(x<u[0]+(y-u[1])*h[0]/h[1])
        q=X-u;t=np.clip(q@h/(h@h),0,1);dt=q-t[:,None]*h
        d=np.minimum(d,np.einsum('ij,ij->i',dt,dt))
    return b,np.sqrt(d)
within, edge=inside_and_edge(LC)
good=within&(pt[:,3]==1)&(pt[:,5]==1)&(z>=24.5)&(z<77)
k=cKDTree(LC[good&~held]); hits=z[good&~held]
dd,nn=k.query(V,k=22)
assert dd.max()<6 and len(nn)==len(V)
W=np.exp(-.5*(dd/np.maximum(.29,dd[:,[8]]))**2)
local=hits[nn]
sim=np.exp(-.5*((local[:,:,None]-local[:,None,:])/.58)**2)
m=np.argmax(np.einsum('ijk,ik->ij',sim,W),axis=1)
level=local[np.arange(len(V)),m]
ms=np.abs(local-level[:,None])<=1.05
U=LC[good&~held][nn]-V[:,None,:]
X=np.concatenate([np.ones((len(V),22,1)),U],axis=2)
w=W*ms
par=np.empty((len(V),3))
for i in range(len(V)):
    q=X[i]; weights=w[i]; 
    # Stabilise the inferred slope close to edges at sampled spatial support only.
    A=q.T@(weights[:,None]*q)+np.diag([0.00001,.16,.16]); c=q.T@(weights*local[i]); par[i]=np.linalg.solve(A,c)
    if not np.isfinite(par[i]).all():raise RuntimeError(i)
Z=np.clip(par[:,0],level-.45,level+.45)
assert np.all(Z>=24.25) and Z.max()<77.1
Q=np.c_[V,Z-z0]
E=collections.defaultdict(list)
for face in F:
    for a,b in zip(face,np.roll(face,-1)):E[tuple(sorted((a,b)))].append((a,b))
bnd=[q[0] for q in E.values() if len(q)==1]
assert set(collections.Counter(i for e in bnd for i in e).values())=={2}
assert all(len(q)==1 or (len(q)==2 and q[0]==q[1][::-1]) for q in E.values())
bottom=sorted({i for f in bnd for i in f}); ids={i:len(Q)+j for j,i in enumerate(bottom)}
Q=np.vstack([Q,np.c_[V[bottom],np.full(len(bottom),hidden_base-z0)]])
tail={a:b for a,b in bnd}
start=bottom[0]; p=start; loop=[]
while not loop or p!=start:
    loop.append(p);p=tail[p]
    assert len(loop)<=len(bottom)
assert set(loop)==set(bottom)
F0=list(map(tuple,F))
for a,b in bnd:
    F0.extend(((b,a,ids[a]),(b,ids[a],ids[b])))
g=poly(V[loop])
basename={tuple(V[i]):i for i in loop}
for t in simple_tris(g):
    face0=[]
    for p in t[::-1]:
        ii=basename.get(tuple(np.round(p,7)))
        assert ii is not None
        face0.append(ids[ii])
    F0.append(tuple(face0))
edges=collections.defaultdict(list)
for f in F0:
    for a,b in zip(f,f[1:]+f[:1]):edges[tuple(sorted((a,b)))].append((a,b))
assert all(len(c)==2 and c[0]==c[1][::-1] for c in edges.values())
assert all(np.linalg.norm(np.cross(Q[b]-Q[a],Q[c]-Q[a]))>1e-9 for a,b,c in F0)
obj=out/'Irvine-footprint-lidar-survey-envelope.obj'
obj.write_text('# 2022 LiDAR survey envelope, separate from the original trial.\n# Horizontal extent is Philadelphia BIN 1385697, local grade 14.40 NAVD88 provisional.\n'+'o Irvine_survey_envelope\n'+
               ''.join('v %.7f %.7f %.7f\n'%tuple(p) for p in Q)+
               ''.join('f %d %d %d\n'%tuple(x+1 for x in f) for f in F0))
# Spatially bucket holdout and intersect the exact mesh roof triangles.
testids=np.flatnonzero(good&held&(edge>.20))
arr=LC[testids]; bucket=collections.defaultdict(list)
for i,p in enumerate(np.floor(arr/step).astype(int)):bucket[tuple(p)].append(i)
check=np.full(len(arr),np.nan)
for f,b in zip(F,patches):
    j=np.asarray(bucket.get(b,[]),dtype=int)
    if not len(j):continue
    t=Q[f]; B=(t[1:,:2]-t[0,:2]).T;weights=(arr[j]-t[0,:2])@np.linalg.inv(B).T
    weights=np.c_[1-weights.sum(1),weights]
    ok=weights.min(1)>=-1e-7
    k0=weights[ok]@t[:,2]+z0
    assert np.all(np.isnan(check[j[ok]])|(np.abs(check[j[ok]]-k0)<3e-4))
    check[j[ok]]=k0
m=np.isfinite(check);errs=np.abs(check[m]-z[testids[m]])
forecast=check[m]
local_ids=testids[m];tp=pt[local_ids]
# Expose residual on every level, including junctions where the single-height mesh cannot fit both faces.
breaks=[(24.5,31),(31,41),(41,48),(48,54),(54,67),(67,77)]
st={}
for b,e in breaks:
 g=(tp[:,2]>=b)&(tp[:,2]<e)
 st[f'{b}-{e}']={'n':int(g.sum()),'abs_p50_p90_p95_m':np.quantile(errs[g],[.50,.90,.95]).tolist()} if any(g) else None
assert m.mean()>.99 and len(errs)>10000 and np.median(errs)<.35
report={'status':'standalone survey-envelope reference, not CS2 asset','footprint_sha256':source['source_sha256'],
 'input_npz_sha256':hashlib.sha256(point_path.read_bytes()).hexdigest(),'obj_sha256':hashlib.sha256(obj.read_bytes()).hexdigest(),
 'local_axes_origin_utm':ref['plane_meeting_utm_xy'],'holdout_point_source_ids':[19,20],
 'source_point_count':len(points),'height_sample_filter':'first class-1 inside footprint from 24.5m to below77m NAVD88; excludes grade/ground artifacts',
 'top_build_mesh':'0.64m triangulated grid clipped to city exterior; robust locally fitted height under spatial support; interpolation is NOT wall position',
 'polygon_source_vertices':len(raw),'polygon_used_vertices':len(foot),'footprint_preserved_area_m2':P.GetArea(),
 'roof_xy_extent_m':np.ptp(V,axis=0).tolist(),'roof_z_navd88_min_max_m':[float(Z.min()),float(Z.max())],
 'mesh_vertices':len(Q),'mesh_triangles':len(F0),'mesh_roof_triangles':len(F),'mesh_boundary_skirt_vertices':len(loop),
 'mesh_closed_two_face_edges':len(edges),'roof_max_neighbour_dist_m':float(dd[:,0].max()),
 'roof_99pct_neighbour_dist_m':float(np.quantile(dd[:,0],.99)),
 'z0_navd88_m':z0,'hidden_model_bottom_navd88_m':hidden_base,
 'train_n':int(sum(good&~held)),'holdout_filtered_n':len(m),'holdout_triangle_intersections':len(errs),
 'held_abs_p50_p90_p95_m':np.quantile(errs,[.50,.90,.95]).tolist(),
 'held_within_0p5m':float(np.mean(errs<=.5)),'held_by_height_navd88':st }
(out/'survey-envelope.json').write_text(json.dumps(report,indent=2)+'\n')
(out/'roof-face-count.txt').write_text(str(len(F))+'\n')
print(json.dumps(report,indent=2))

