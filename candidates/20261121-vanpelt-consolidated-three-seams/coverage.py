"""Independent normal-specific bidirectional full-polygon overlaps from Blender world space."""
from pathlib import Path
import json,sys
from osgeo import ogr
q=Path(sys.argv[1]); d=json.loads(q.read_text())
def poly(x):
 p=[(round(a,4),round(b,4)) for a,b,z in x]
 ar=.5*sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1]))
 r=ogr.Geometry(ogr.wkbLinearRing)
 for v in p:r.AddPoint_2D(*v)
 r.CloseRings(); z=ogr.Geometry(ogr.wkbPolygon);z.AddGeometry(r)
 assert z.IsValid() and z.GetArea()==abs(ar);return ar>0,z
def groups(p):
 pp=[];nn=[]
 for x in p:
  plus,z=poly(x);(pp if plus else nn).append(z)
 return pp,nn
def union(items):
 v=ogr.Geometry(ogr.wkbMultiPolygon)
 for z in items:v.AddGeometry(z)
 return v.UnionCascaded() if items else v
def sums(against,items):return sum(x.Intersection(against).GetArea() for x in items)
out={}
for z,rows in d['reread_polygons_on_planes'].items():
 a,b=groups(rows['before']);p,n=groups(rows['after']); assert len(a)==len(b)==1 and not n
 A,B=a[0],b[0]; C,D=union(p),union(n); target=A.Difference(B)
 bound=A.GetArea()
 assert C.SymDifference(target).GetArea()==0.,z
 assert sum(a.GetArea() for a in p)==C.GetArea()
 out[z]={'normal_direction_pairwise_original_m2':[sums(B,a),sums(A,b)],'normal_direction_pairwise_repaired_m2':[sums(D,p),sums(C,n)],
  'retained_outward_coverage_m2':C.GetArea(),'visible_target_symmetric_difference_m2':C.SymDifference(target).GetArea(),
  'within_normal_new_overlap_m2':sum(a.GetArea() for a in p)-C.GetArea(),'readback_world_plane_tolerance_m':1e-5,'XY_snap_for_area_m':1e-4}
assert [d['retained_outward_coverage_m2'] for d in out.values()]==[2288,0,368]
Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print(out)
