"""Independent fresh Blender world polygon area on z=0."""
from pathlib import Path
import json
from osgeo import ogr
D=Path(__file__).resolve().parent
q=json.loads((D/'verified.json').read_text())
def pg(poly):
 p=[(round(a,4),round(b,4)) for a,b,z in poly]
 ar=.5*sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1]))
 r=ogr.Geometry(ogr.wkbLinearRing)
 for v in p:r.AddPoint_2D(*v)
 r.CloseRings(); z=ogr.Geometry(ogr.wkbPolygon);z.AddGeometry(r)
 assert z.IsValid() and z.GetArea()==abs(ar)
 return z,ar>0
def union(g):
 m=ogr.Geometry(ogr.wkbMultiPolygon)
 for p in g:m.AddGeometry(p)
 return m.UnionCascaded()
old=[pg(r) for r in q['z0_original_polys']];new=[pg(r) for r in q['z0_new_polys']]
pos,=[p for p,v in old if v];neg=[p for p,v in old if not v]
assert len(neg)==2 and sorted(x.GetArea() for x in neg)==[1980,2420.]
N=union(neg);assert N.GetArea()==4400
out=union([p for p,v in new if v]);assert len(new)==14 and all(v for p,v in new)
assert sum(p.GetArea() for p,v in new)==out.GetArea()==4304
expected=pos.Difference(N)
a=out.SymDifference(expected).GetArea();assert a==0
b=[out.Intersection(m).GetArea() for m in neg];assert b==[0,0.]
o=dict(original_forward_and_reverse_m2=[[pos.Intersection(p).GetArea(),p.Intersection(pos).GetArea()] for p in neg],post_reimport_overlap_on_each_footprint_m2=b,
 visible_4304_m2_symmetric_difference=a,retained_positive_area_m2=out.GetArea(),z_tolerance_m=1e-5,XY_measure_snap_m=1e-4)
(D/'area.json').write_text(json.dumps(o,indent=2)+'\n');print(o)
