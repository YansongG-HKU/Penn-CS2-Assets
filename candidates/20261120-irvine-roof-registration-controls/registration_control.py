"""Record the draft-only modern plan and historical height controls without fitting asset scale."""
import json,math,statistics
from pathlib import Path
from pyproj import Transformer
d=Path(__file__).resolve().parent
r=lambda f:json.loads((d/f).read_text())
c=r('orthocorner-provisional.json')
a=r('section-scale-control.json')
o=r('ortho-2025-full-extent.json')
g=r('irvine-ground-control.json')
e=o['extent']; px=c['m_per_pixel']
def en(v):
 x,y=v;return(e['xmin']+(x+.5)*px,e['ymax']-(y+.5)*px)
to_ll=Transformer.from_crs(26918,4326,always_xy=True)
roof=[en(v) for v in c['corner_px_top_left_coordinates']]
roof_shape=list(map(lambda p:list(to_ll.transform(*p)),roof)); roof_shape.append(roof_shape[0])
f=[{"type":"Feature","geometry":{"type":"Polygon","coordinates":[roof_shape]},"properties":
 {'role':'visual 2025 main upper slate slope envelope, not surveyed roof footprint','input_pixel_corners':c['corner_px_top_left_coordinates'],
  'image_resolution_m_per_px':px,'manual_pick_uncertainty_px':c['estimated_visual_pick_uncertainty_px'],
  'ground_control_not_roof_xyz':True}}]
for k,q in g['samples'].items():
 f.append({'type':'Feature','geometry':{'type':'Point','coordinates':list(to_ll.transform(*q['utm18_m']))},
           'properties':{'role':k,'floor_control_only':True,'z_navd88_m':q['median_navd88_m'],'z_range_navd88_m':q['range_navd88_m']}})
(d/'irvine-registration-controls.geojson').write_text(json.dumps({'type':'FeatureCollection','features':f},indent=2)+'\n')
z=a['approx_elevations_m_from_printed_grade']; base=(z['main_eave_left']+z['main_eave_right'])/2
h=[base,z['slope_to_spire_cladding'],z['finial_crossbar']]
b=[29.,40.5,56.5]
history_spans=[h[i+1]-h[i] for i in range(2)];model_spans=[b[i+1]-b[i] for i in range(2)]
result={
'historical_span_m':{'slate_roof_rise':history_spans[0],'from_rough_spire_cladding_break_to_finial_crossbar':history_spans[1]},
'raw_model_span_m':{'slate_roof_rise':model_spans[0],'from_slope_upper_join_to_top':model_spans[1]},
'historical_to_model_interval_ratios':[q/a for a,q in zip(model_spans,history_spans)],
'outline_orientation_EPSG26918_degrees_clockwise_from_E':math.degrees(math.atan2(roof[0][1]-roof[1][1],roof[1][0]-roof[0][0])),
'nearby_paving_site_min_max_navd88_m':[op(q['median_navd88_m'] for q in g['samples'].values()) for op in (min,max)],
'policy':'Use interval comparisons and planar shape to triage. Do not apply shift or rescale from non-homologous ortho and 1926 anchors; acquire roof heights in same vertical datum and register corresponding walls, roof breaks, and entry threshold.'
}
(d/'irvine-registration-summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
