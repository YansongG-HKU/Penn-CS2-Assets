"""Fit four roof slopes to 2022 LiDAR and withhold whole flight source IDs."""
import json
from pathlib import Path
import numpy as np
D=Path(__file__).parent; data=np.load(D/'irvine-cropped-points.npz')['data']
B=json.loads((D/'ortho-2025-full-extent.json').read_text())['extent']
P=np.array(json.loads((D/'orthocorner-provisional.json').read_text())['corner_px_top_left_coordinates'])
mm=(B['xmax']-B['xmin'])/740
G=np.c_[B['xmin']+mm*(P[:,0]+.5),B['ymax']-mm*(P[:,1]+.5)]
C=G.mean(0)
E=(G[1]-G[0])+(G[2]-G[3]);E/=np.linalg.norm(E)
N=np.array([-E[1],E[0]])
orthocenter=C.copy(); z=data[:,2]
held=np.isin(data[:,4],[19,20])
ortho_local=(data[:,:2]-C)@np.column_stack([E,N])
center_data=(data[:,3]==1)&(data[:,5]==1)&(z>69)&(z<77)&(np.abs(ortho_local).max(axis=1)<7)&~held
assert center_data.sum()>=20
C=np.median(data[center_data,:2],axis=0)
L=(data[:,:2]-C)@np.column_stack([E,N]); x,y=L.T
m=(data[:,3]==1)&(data[:,5]==1)&(z>48)&(z<68)&(abs(x)<8.1)&(abs(y)<8.1)
# Exclude all near-diagonal, central spire, and eave seam margins.
sectors={'east':(x>2.0)&(x>abs(y)+.9),'west':(x<-2.0)&(-x>abs(y)+.9),
 'north':(y>2.0)&(y>abs(x)+.9),'south':(y<-2.0)&(-y>abs(x)+.9)}
R={}; rng=np.random.default_rng(319)
fitA=np.c_[L,np.ones(len(z))]
# Reserve two full cross-pass scan IDs, not random neighboring points.
held=np.isin(data[:,4],[19,20])
for name,cond in sectors.items():
 sel=m&cond; train=np.flatnonzero(sel&~held); val=np.flatnonzero(sel&held)
 assert len(train)>200 and len(val)>200,(name,len(train),len(val))
 M=fitA[train]; Z=z[train]; best=None
 for q in range(500):
  k=rng.choice(len(Z),3,replace=False); A=M[k]
  if abs(np.linalg.det(A))<.15:continue
  v=np.linalg.solve(A,Z[k]); err=np.abs(M@v-Z)
  cand=(int((err<.18).sum()),-float(np.minimum(err,.5).sum()),v)
  if best is None or cand[:2]>best[:2]:best=cand
 a=best[2]
 for _ in range(4):
  ok=np.abs(M@a-Z)<.18;a=np.linalg.lstsq(M[ok],Z[ok],rcond=None)[0]
 err=np.abs(M@a-Z)
 ev=np.abs(fitA[val]@a-z[val])
 # Other roof facets/turrets can lie in a plan sector; report all errors separately.
 ti=err<.18;vi=ev<.25
 row=dict(local_xy_plane_a_b_c=a.tolist(),dip_deg=float(np.degrees(np.arctan(np.linalg.norm(a[:2])))),
  train_n=len(Z),train_plane_inliers=int(ti.sum()),withheld_n=len(val),withheld_plane_inliers=int(vi.sum()),
  withheld_all_abs_residual_quantiles_m=np.quantile(ev,[.1,.5,.9,.95]).tolist(),
  withheld_inlier_abs_residual_p95_m=float(np.quantile(ev[vi],.95)),
  distributions_inlier_height_m=np.quantile(Z[ti],[.01,.1,.5,.9,.99]).tolist())
 assert ti.mean()>.5 and vi.mean()>.5,(name,row)
 R[name]=row
A=np.array([v['local_xy_plane_a_b_c'] for v in R.values()])
meeting=np.linalg.lstsq(np.c_[A[:,:2],-np.ones(4)],-A[:,2],rcond=None)[0]
dmeet=A@np.r_[meeting[:2],1]-meeting[2]
highest=(data[:,3]==1)&(data[:,5]==1)&(np.linalg.norm(L-meeting[:2],axis=1)<1.6)
N0=json.loads((D/'irvine-ground-control.json').read_text())
B0=[v['median_navd88_m'] for v in N0['samples'].values()]
R=dict(source='2022 NOAA EPT 9848, EPSG6347 horizontal / EPSG5703 NAVD88 GEOID18 m',body_center_local_origin_utm=C.tolist(),
 local_east_axis_utm=E.tolist(),local_north_axis_utm=N.tolist(),inlier_selection='first returns unclassified, four sectors exclude center/eaves and diagonal, 0.18m train threshold and 0.25m withheld diagnostic',
 unique_input_points=len(data),holdout_source_ids=[19,20],orthophoto_center_utm=orthocenter.tolist(),train_observed_center_shift_m=float(np.linalg.norm(orthocenter-C)),planes=R,plane_meeting_utm_xy=(C+np.column_stack([E,N])@meeting[:2]).tolist(),
 plane_meeting_m_navd88=float(meeting[2]),four_plane_residuals_m=dmeet.tolist(),spatial_central_return_count=int(highest.sum()),
 highest_central_observed_m_navd88=float(z[highest].max()),nearby_paving_navd88_m=[min(B0),max(B0)],
 note='Plane intersection is extrapolated convergence, not a measured spire/roof join; highest central observed class1 point is not a survey finial height. Sector assignment from approximate 2025 ortho with parallax review.')
(D/'irvine-roof-plane-fit.json').write_text(json.dumps(R,indent=2)+'\n')
print(json.dumps(R,indent=2))
