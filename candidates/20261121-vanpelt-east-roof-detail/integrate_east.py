"""Refine only the verified east raised roof surfaces; keep outline and all other base tiers."""
from segment_east import *
from east_mesh_builder import build
d0=BASE/'deliver/measurements.json'
if not d0.exists():d0=BASE/'measurements.json'
baseline=json.loads(d0.read_text())
roofs=baseline['obj_build']['roof_patches']; h=dict((r['name'],r['z_m']) for r in roofs)
raised=[];report=[]
for lo,hi in [(46.31,46.88),(47.91,48.36)]:
 for p,z,e in prep_band(lo,hi):
  ok=e['held_all_abs_error_p50_p90_p95'][1]<=.40 and e['held_n']/e['held_all_n']>=.84
  e['integrated']=ok
  if ok:raised.append(('east_raised_%02d'%(len(raised)+1),p,z))
  report.append(e)
assert len(raised)>=5
for i,(tag,p,z) in enumerate(raised):
 assert attic.Contains(p) and not p.Intersects(east_high_roof)
 assert all(p.Distance(q)>.015 for _,q,_ in raised[i+1:])
# Keep the original roof controls and outer walls; only partition the existing attic plane.
r=build(h['low_outer'],h['connected_middle'],h['east_attic'],h['west_penthouse'],h['east_high_platform'],baseline['metre_frame']['z0_south_approach_m'],out/'Van-Pelt-east-rooftop-refinement.obj',raised)
# Global held checks across all mapped east attic points; keep a consistent all-Z metric and note floors/equipment.
who=np.flatnonzero(held&use); xy=m[who]
sel,_=inside_d(ringpoints(attic.GetGeometryRef(0)),xy)
fields=who[sel]; xy=m[fields]
def contains(g,x):
 q,_=inside_d(ringpoints(g.GetGeometryRef(0)),x)
 for r in list(g)[1:]:
  l,_=inside_d(ringpoints(r),x)
  q&=~l
 return q
existing=np.where(contains(east_high_roof,xy),h['east_high_platform'], h['east_attic'])
pred=existing.copy()
for n,p,z in raised:
 f=contains(p,xy)
 pred[f]=z
moved=existing!=pred
qa=lambda ar:np.quantile(ar,[.5,.9,.95]).tolist()
q_before=abs(Z[fields]-existing);q_after=abs(Z[fields]-pred)
assert np.mean(q_after[moved])<np.mean(q_before[moved])*.45
report0=dict(status='Offline roof surface refinements from 2022; no named room or equipment assignments, no Editor',
  old_measurement_sha=baseline['obj_build']['sha256'], held_source_ids=[19,20], integrated_patch_count=len(raised),
  total_detail_surface_area_m2=sum(p.GetArea() for _,p,_ in raised),  model=r,
  all_east_attic_held_all_elevations_n=len(fields),all_east_attic_held_abs_p50_p90_p95_before_m=qa(q_before),all_east_attic_held_abs_p50_p90_p95_after_m=qa(q_after),
  affected_held_n=int(sum(moved)),affected_held_abs_p50_p90_p95_before_m=qa(q_before[moved]),affected_held_abs_p50_p90_p95_after_m=qa(q_after[moved]),
  raised_patches=report,
  cross_epoch='2025 west-sample LAS consistency only. No east sample from bounded LAS ranges. 2025 orthophoto geometry guide only. November 2026 visitor plan not same-layer registration, no green roof or terrace geometry inferred.')
(out/'east-detail-measurements.json').write_text(json.dumps(report0,indent=2)+'\n')
print('EAST_DETAIL',[(k,report0[k]) for k in report0 if k not in ('raised_patches','model')],r['sha256'])
