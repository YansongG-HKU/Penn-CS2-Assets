"""Produce independently evaluated height controls and a closed, non-game study shell."""
from roof_shell_core import *
from point_diagnostics import a,X,Y,Z,m,source,first,points,xy_box
out=D/'deliver';out.mkdir(exist_ok=True)
held=np.isin(source,[19,20]); fits={}
def quant(a,Q=[.5,.9,.95]):return [float(i) for i in np.quantile(a,Q)]
def fit(name,boxes,band):
 domain=np.logical_or.reduce([xy_box(*r) for r in boxes])&first
 accepted=domain&(Z>=band[0])&(Z<=band[1]); tr=accepted&~held; te=accepted&held; allte=domain&held
 assert sum(tr)>200 and sum(te)>100 and sum(te)/sum(allte)>.72,(name,sum(tr),sum(te),sum(allte))
 h=round(float(np.median(Z[tr])),2)
 fits[name]={'controls_local_xy_boxes_m':boxes,'selected_height_band_m':band,'fitted_height_navd88_m':h,
 'train_in_band':int(sum(tr)),'held_in_band':int(sum(te)),'held_all_heights':int(sum(allte)),
 'held_in_band_absolute_p50_90_95_m':quant(abs(Z[te]-h)),
 'held_without_z_screen_absolute_p50_90_95_m':quant(abs(Z[allte]-h))}
 return h
z0=19.331369165057666
lo=fit('low_perimeter',[[-60,-30,23,26]], [38.10,38.61])
midz=fit('main_deck_and_connector',[[-59,-30,13,18],[-17,1,6.2,11.7], [12,58,-19,-17.8]], [41.75,42.26])
hi=fit('east_high_deck',[ [50,57,6.9,10.5],[40,56,-12,-7] ], [44.24,44.74])
w=fit('west_local_penthouse',[[ -47.9,-41.1,5.55,10.65 ]],[46.30,46.90])
eh=fit('east_high_platform',[[18.0,28.0,-1.55,3.0]],[48.75,49.20])
def region_scores(poly,z):
 ok=held&first
 x=m[ok]; q=Z[ok]; sel,dist=inside_d(ringpoints(poly.GetGeometryRef(0)),x)
 for ring in list(poly)[1:]:
  inside,ds=inside_d(ringpoints(ring),x); sel&=~inside;dist=np.minimum(dist,ds)
 test=sel&(dist>.4**2)
 r=abs(q[test]-z)
 assert len(r)>30
 return dict(n=int(len(r)), all_z_held_abs_p50_p90_p95_m=quant(r),fraction_within_half_m=float(np.mean(r<=.5)))
body_regions=[('low',body.Difference(mid),lo),('middle',mid.Difference(attic).Difference(west_penthouse),midz),('attic',attic.Difference(east_high_roof),hi),('west_penthouse',west_penthouse,w),('east_high_platform',east_high_roof,eh)]
metrics={k:[region_scores(p,z) for p in geom_polys(g) if p.GetArea()>25] for k,g,z in body_regions}
gap=xy_box(-16.5,-1.2,16,19)
gapmeasure={'all_first_return_n':int(sum(first&gap)),'held_first_return_n':int(sum(first&gap&held)),
  'held_return_5_50_95_z_m':quant(Z[first&gap&held],[.05,.5,.95]),
  'ground_class2_median_m':float(np.median(Z[(a[:,3]==2)&gap])), 'action':'removed the above-ground roof slab in this pocket; below-grade extent unmodeled'}
r=build(lo,midz,hi,w,eh,z0,out/'Van-Pelt-survey-roof-massing.obj')
receipt={'notice':'Offline closed roof reconstruction with synthetic wall and base closure; not production FBX, UV, materials, LOD or game validation',
 'sources':{'city_footprint':'https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/LI_BUILDING_FOOTPRINTS/FeatureServer/0',
  'city_bin':'1386251','footprint_json_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
  'photograph':'https://www.pasda.psu.edu/uci/DataSummary.aspx?dataset=7157','point_ept':'https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/entwine/geoid18/9848',
  'point_catalog':'https://www.fisheries.noaa.gov/inport/item/70174','qgis_crop_gzip_sha256':hashlib.sha256(points.read_bytes()).hexdigest(),
  'crop':json.loads((D/'vanpelt-ground-roofs.json').read_text())},
 'metre_frame':{'horizontal_epsg':6347,'source_vertical':'EPSG5703 NAVD88 GEOID18','origin_EN':o.tolist(),'axes_rows_EN':axes.tolist(),'z0_south_approach_m':z0,
  'full_footprint_span_m':np.ptp(P,axis=0).tolist(),'body_span_after_low_layer_clips_m':np.ptp(body_rings[0],axis=0).tolist(),
  'city_footprint_area_m2':foot.GetArea()},
 'flightline_holdout_source_IDs':[19,20], 'distinct_source_points':len(a), 'height_fits':fits,'roof_extent_test_all_returns_no_height_cut':metrics,
 'north_recess':gapmeasure,'shape_limits':['roof plan has primary partitions but interior patch boundaries approximate','eastern high deck is underlying representative plane, omits equipment and additional facets distinct at 44.9–48.3 m; measured 49 m patch is represented as a closed rectangular mass, material and purpose unresolved','south stair and canopy group separate, excluded from the model','one provisional z0, no ground/entrance surfaces are certified','nominal existing lot 18x6 144x48 m cannot cover full 56.69 m width at 1:1; 18x8 arithmetic with stairs only, not access/Editor proof'],
 'obj_build':r}
(out/'measurements.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ('height_fits','roof_extent_test_all_returns_no_height_cut','north_recess','obj_build')},indent=2))
