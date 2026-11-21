"""Build the Fisher roof-crown reference as a continuous closed shell, with observed upper aperture.
All ornamental massing is representative, not as-built certification."""
import collections,hashlib,json,sys
from pathlib import Path
import numpy as np
from osgeo import ogr
from mesh import clean_surfaces
from geos import flat,tris2
ogr.UseExceptions()
d=Path(__file__).resolve().parent
c=json.loads((d/'calibration.json').read_text()); a=json.loads((d/'crest-stations.json').read_text())
zref=17.1; zbase=42.95
def ring(xy):
 r=ogr.Geometry(ogr.wkbLinearRing)
 for x,y in xy:r.AddPoint_2D(float(x),float(y))
 r.CloseRings();return r
def poly(xy):
 p=ogr.Geometry(ogr.wkbPolygon);p.AddGeometry(ring(xy));return p
def rect(w,e,s,n):return poly([(w,s),(e,s),(e,n),(w,n)])
def geom(g):
 if g is None or g.IsEmpty() or g.GetDimension()!=2:return []
 if g.GetGeometryName()=='POLYGON':return [g]
 return [t for q in g for t in geom(q)]
def simplify(p):
 r=[]
 for i,z in enumerate(p):
  k=np.asarray(z.GetPoints())[:-1,:2]
  k=np.round(k,5)
  k=k[np.any(k!=np.roll(k,1,axis=0),axis=1)]
  if (flat(k)>0)!=(i==0):k=k[::-1]
  assert len(k)>=3 and abs(flat(k))>5e-7
  r.append(k)
 g=poly(r[0])
 for k in r[1:]:g.AddGeometry(ring(k))
 assert g.IsValid(),g.ExportToWkt()
 return g,r
def const(h):return lambda v:np.full(len(v),h)
w,e,s,n=np.round(c['rim_midline_bounds_W_E_S_N'],5)
ix=np.round(c['inner_roof_bounds'],5); W,E,S,N=ix
mains=rect(w-.50,e+.47,s-.43,n+.43)
tur=np.round(c['upper_crown_bounded_rectangle'],5)
x0,x1,y0,y1=tur;X=(x0+x1)/2;Y=(y0+y1)/2
# A dark central aperture is seen overhead, not its full depth. Its opening dimensions are provisional
# from relative image proportions, and open-through is a deliberately synthetic cut, not a shaft survey.
holebounds=[round(v,5) for v in c['training_gap_supported_provisional_aperture']]
upper=rect(*tur); hole=rect(*holebounds)
assert upper.Contains(hole)
big=mains.Union(upper).Difference(hole)
base=big.GetArea()
um=upper.Difference(hole)
region=[('upper_rim',um,const(c['upper_crown_elevation_m']))]
core0=rect(*ix); ledge=mains.Difference(core0).Difference(upper)
assert ledge.IsValid()
offsets={}
for j,p in enumerate(a['stations']):
 side=p['side']; t=float(p['plan_station_m']); top=float(p['train_z_median'])
 aa=.29
 if side=='west':r=rect(w-.39,w+.47,t-aa,t+aa); dim=1
 elif side=='east':r=rect(e-.47,e+.40,t-aa,t+aa); dim=1
 elif side=='north':r=rect(t-aa,t+aa,n-.38,n+.38);dim=0
 else:r=rect(t-aa,t+aa,s-.38,s+.36);dim=0
 r=r.Intersection(ledge)
 if r.GetArea()<.05:continue
 ledge=ledge.Difference(r)
 # Keep the roof-top visible station as a stylized sloped crest, not a replica of every ornament.
 divs=[[max(t-aa,-1e8),t-.105,-1],[t-.105,t+.105,0],[t+.105,t+aa,1]]
 offsets[j]={'side':side,'station':t,'plan_area_m2':r.GetArea(),'top_m_NAVD88':top}
 for lo,hi,which in divs:
  band=rect(lo,hi,-100,100) if dim==0 else rect(-100,100,lo,hi)
  p0=r.Intersection(band)
  if not geom(p0):continue
  def zq(v,t=t,dim=dim,top=top):
   # Keep vertical decorated wall height at the lowest available sample, then rise to the top band.
   a=np.clip((abs(v[:,dim]-t)-.105)/.185,0,1)
   return top-.32*a
  region.append((f'crest_{j}',p0,zq))
ledgeh=float(c['ledge_estimate_m'])
region.append(('ledge',ledge,const(ledgeh)))
ea,pt,hx,hy=c['hip_coeffs_eave_apex_U0_V0']; peak=np.array([round(hx,5),round(hy,5)])
loop=np.array([[W,S],[E,S],[E,N],[W,N]])
for j,(aa,bb) in enumerate(zip(loop,np.roll(loop,-1,axis=0))):
 wing=poly([aa,bb,peak]); part=wing.Difference(upper)
 direction=('y','x','y','x')[j];dim=int(direction=='y')
 bound=(S,E,N,W)[j]; dd=peak[dim]-bound
 fun=lambda u,dm=dim,b=bound,den=dd:ea+(pt-ea)*(u[:,dm]-b)/den
 region.append(('hip',part,fun))
assert abs(sum(p.GetArea() for k,p,f in region)-base)<1e-5
sur=[]; seg=[]
for name,g,zfun in region:
 for p in geom(g):
  g,r=simplify(p)
  for t in tris2(g):
   sur.append((name,np.c_[t,zfun(t)]))
   sur.append(('cut_base',np.c_[t[::-1],np.full(3,zbase)]))
  for k in r:
   for u,v in zip(k,np.roll(k,-1,axis=0)):
    seg.append((u,v,zfun,name))
pts=np.unique(np.array([q for i in seg for q in i[:2]]),axis=0)
ed=collections.defaultdict(list)
for u,v,f,name in seg:
 vec=v-u; t=((pts-u)@vec)/(vec@vec)
 near=np.linalg.norm(pts-u-t[:,None]*vec,axis=1)<1.5e-5
 sel=(t>1e-6)&(t<1-1e-6)&near
 pp=[u,*pts[sel][np.argsort(t[sel])],v]
 for a,b in zip(pp,pp[1:]):
  p,q=tuple(a),tuple(b)
  ed[tuple(sorted([p,q]))].append((p,q,f,name))
for vals in ed.values():
 assert len(vals)<=2,len(vals)
 if len(vals)==2:assert vals[0][0]==vals[1][1] and vals[0][1]==vals[1][0],vals
 vals.sort(key=lambda it:float(np.mean(it[2](np.array(it[:2])))),reverse=True)
 a,b,ff,name=vals[0]; xy=np.array([a,b]); h=ff(xy)
 l=vals[1][2](xy) if len(vals)==2 else np.full(2,zbase)
 assert min(h-l)>-.00009,(h,l,vals)
 if max(abs(h-l))<.00009:continue
 z=np.array([[*a,h[0]],[*a,l[0]],[*b,l[1]],[*b,h[1]]])
 if h[0]-l[0]>.00009:sur.append(('wall_'+name,z[[0,1,2]]))
 if h[1]-l[1]>.00009:sur.append(('wall_'+name,z[[0,2,3]]))
v,f,tags=clean_surfaces(sur)
e0=collections.defaultdict(list)
for i,a in enumerate(f):
 for x,y in zip(a,a[1:]+a[:1]):e0[tuple(sorted((x,y)))].append((x,y))
bad=[(v[list(k)].tolist(),r) for k,r in e0.items() if len(r)!=2 or r[0]!=r[-1][::-1]]
print('verts',len(v),'faces',len(f),'edges',len(e0),'bad',len(bad),bad[:7])
assert not bad
tt=np.radians(c['rotation_local_deg']); v[:,:2]=v[:,:2]@np.array([[np.cos(tt),np.sin(tt)],[-np.sin(tt),np.cos(tt)]])
v[:,2]-=zref
p=d/'Fisher-west-tower-crown-geometry.obj'
layers={'hip':'roof_surface_unknown_finish','ledge':'masonry_reference','upper_rim':'higher_crown_reference','cut_base':'synthetic_cut_base'}
cls=lambda lab: ('crest_station_reference' if lab.startswith('crest_') else layers.get(lab,'vertical_reference'))
data=['# Local XY in the same east/north frame as the City envelope; z=0 means 17.10 m NAVD88.\n',
      '# Standalone upper roof slice only; not a CS2 asset.\n','mtllib Fisher-west-tower-crown-materials.mtl\n','o Fisher_West_Tower_Crown_Reference\n']
data.extend('v %.6f %.6f %.6f\n'%tuple(row) for row in v)
prev=''
for q,nm in zip(f,map(cls,tags)):
 if nm!=prev:data.append(f'usemtl {nm}\n');prev=nm
 data.append('f %d %d %d\n'%tuple(i+1 for i in q))
p.write_text(''.join(data))
mats={'roof_surface_unknown_finish':(.14,.18,.21),'masonry_reference':(.50,.23,.16),
      'higher_crown_reference':(.64,.32,.20),'synthetic_cut_base':(.33,.30,.29),'crest_station_reference':(.68,.39,.24),'vertical_reference':(.51,.26,.18)}
(d/'Fisher-west-tower-crown-materials.mtl').write_text(''.join(f'newmtl {n}\nKd {m[0]} {m[1]} {m[2]}\nKs 0.06 0.06 0.06\nNs 32\nillum 2\n\n' for n,m in mats.items()))
r={'vertices':len(v),'triangles':len(f),'opposed_two_face_edges':len(e0),'lower_cut_Navd88_is_synthetic':zbase,'local_model_z0_NAVD88':zref,
 'upper_cap_hole_extents_xy_in_rotated_frame':holebounds,'opening_creation_note':'Present in 2025 orthophoto. Size provisional and constrained to a gap in four training passes. Model through-cut is artificial, not surveyed aperture depth or interior.',
 'crest_station_count_is_not_historical_ornament_count':len(offsets),'crest_spatial_fit':'All stations selected from 2022 training passes; test only where there are withheld points',
 'upper_faces_annotated':dict(collections.Counter(map(cls,tags))), 'roof_z_min_max': [float(v[:,2].min()),float(v[:,2].max())],
 'envelope_union_area_m2':base,'reference_obj_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(d/'build.json').write_text(json.dumps(r,indent=2)+'\n')
