"""Calibrate mutually distinct Fisher tower crest/rim and hidden-but-observed inner roof from 2022 returns."""
import collections,sys,json
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
F=Path(__file__).resolve().parent.parent
a=np.load(F/'points.npz')['a']
f=json.loads((F/'frame.json').read_text()); S=(a[:,:2]-f['origin_epsg6347'])@np.array(f['axes_east_north']).T
X,Y=S.T; Z=a[:,2]
train=np.isin(a[:,4],[59,60,61,62]); hold=np.isin(a[:,4],[19,20]); first=(a[:,3]==1)&(a[:,5]==1)
regions=[
 ('west',(-15.7,-13.7),(3.6,11.35),'x'),
 ('east',(-5.0,-3.28),(4.2,11.0),'x'),
 ('south',(-13.25,-5.4),(2.22,3.28),'y'),
 ('north_L',(-14.2,-11.20),(11.70,13.20),'y'),
 ('north_R',(-7.85,-4.65),(11.85,13.20),'y')]
mask=lambda x,y,b,c:(x>b[0])&(x<b[1])&(y>c[0])&(y<c[1])
sides={}
for n,s,t,_ in regions:
 sides[n]=first&mask(X,Y,s,t)&(Z>=45.28)&(Z<46.1)
# Preserve a common local perpendicular frame; solve one rotation jointly by removing side medians.
def tf(v,ang):
 c,s=np.cos(ang),np.sin(ang); return v@np.array([[c,-s],[s,c]])
def resid(p):
 W=tf(S,p[0]); vv=[]
 for j,(n,_,__,k) in enumerate(regions):
  b=sides[n]&train; dim=0 if k=='x' else 1; r=W[b,dim]-p[j+1]
  vv.extend((r*(100/len(r))**.5).tolist())
 return np.array(vv)
g=least_squares(resid,[0.,-14.6,-4.2,2.7,12.45,12.48],loss='soft_l1',f_scale=.23,bounds=([-0.1,-18,-8,0.,10.,10.],[.1,-11,-1,5.,15.,15.]))
ang=g.x[0]; uv=tf(S,ang); U,V=uv.T
report={}; toph=[]
def qtl(v):return np.quantile(v,[.5,.9,.95]).tolist()
for n,_,__,k in regions:
 m=sides[n]; dim=0 if k=='x' else 1
 off=float(np.median(uv[m&train,dim])); ht=float(np.median(Z[m&train])); toph.append(ht)
 report[n]={'plane_center_m':off,'median_train_z_m':ht,'train_n':int(sum(m&train)),'held_n':int(sum(m&hold)),'hold_cross_plane_m':qtl(abs(uv[m&hold,dim]-off)),'hold_z_abs_m':qtl(abs(Z[m&hold]-ht))}
print('rotation',float(np.degrees(ang)),'reports',json.dumps(report,indent=2))
bookend=[report[n]['plane_center_m'] for n in ('west','east','south','north_L','north_R')]
assert abs(bookend[3]-bookend[4])<.6
w,e,s,n=*bookend[:3],float(np.average(bookend[3:])); rim=float(np.median(toph))
# On each side use two vertical bands from a common crest and narrower ledge. These are independently measured height modes, not building height.
ledges={}
for name,xb,yb,dim in regions:
 b=first&mask(X,Y,xb,yb)&(Z>=44.58)&(Z<=45.08)
 avg=float(np.median(Z[b&train]))
 ledges[name]={'z_train':avg,'n_train':int(sum(b&train)),'n_hold':int(sum(b&hold)),'p50_p90_p95_hold':qtl(abs(Z[b&hold]-avg))}
ledge=float(np.median([r['z_train'] for r in ledges.values()]))
# Hip roof is identified in the 2025 aerial image. Model outline is conservatively inset inside the measured rim.
inset=.69
inner=[w+inset,e-inset,s+inset,n-inset]
def hip(u,v,p):
 eave,peak,u0,v0=p
 W,E,S,N=inner
 r=np.maximum.reduce([(u0-u)/(u0-W),(u-u0)/(E-u0),(v0-v)/(v0-S),(v-v0)/(N-v0)])
 return eave+(peak-eave)*(1-np.clip(r,0,1))
minor=first&mask(U,V,(inner[0]+.40,inner[1]-.40),(inner[2]+.65,inner[3]-.65))&(Z>42.98)&(Z<45.03)
hq=least_squares(lambda p:hip(U[minor&train],V[minor&train],p)-Z[minor&train],[43.4,45.,(w+e)/2,(s+n)/2],
 bounds=([42.8,44.65,w+2.2,s+2.6],[44.0,46.0,e-2.2,n-2.6]),loss='soft_l1',f_scale=.17).x
assert hq[1]>hq[0]
crestbox=first&mask(X,Y,(-11.15,-7.8),(11.40,14.52))&(Z>=49.80)&(Z<51)
tt=uv[crestbox&train];hh=uv[crestbox&hold]; assert len(tt)>155 and len(hh)>60
broad=first&mask(X,Y,(-11.23,-7.84),(11.30,14.59))&(Z>=48.00)&(Z<51)&train
bounds=np.quantile(uv[broad],[.007,.993],axis=0)
ml=bounds[0]-.07; mh=bounds[1]+.07
# Aperture: image confirms existence, not accurate width after orthorectification. Locate the
# continuously empty core in all training passes; keep it provisional and leave the upper perimeter measured.
av=(ml+mh)/2; holes=[]
for x in np.arange(av[0]-.35,av[0]+.351,.035):
 for y in np.arange(av[1]-.35,av[1]+.351,.035):
  for ax0 in np.arange(.30,.461,.03):
   for ay0 in np.arange(.30,.461,.03):
    if not .78<=ax0/ay0<=1.22:continue
    m=(abs(tt[:,0]-x)<ax0)&(abs(tt[:,1]-y)<ay0)
    if m.sum()>1:continue
    candidate=(ax0*ay0-.018*np.hypot(x-av[0],y-av[1])-.018*sum(m),x,y,ax0,ay0,int(sum(m)))
    holes.append(candidate)
assert holes
_,x,y,ax0,ay0,count=max(holes)
aperture=[float(v) for v in (x-ax0,x+ax0,y-ay0,y+ay0)]

cz=float(np.median(Z[crestbox&train])); shape=[ml[0],mh[0],ml[1],mh[1]]
zerrs=qtl(abs(Z[crestbox&hold]-cz))
rpt={'rotation_local_deg':float(np.degrees(ang)),'rim_midline_bounds_W_E_S_N':list(map(float,(w,e,s,n))),
 'rim_side_holdout':report,'rim_elevation_m':rim,'ledge_estimate_m':ledge,'ledge_per_side':ledges,'band_note':'Band gates are feature-conditioning, not absolute all-point/site validation',
 'inner_roof_bounds':inner,'inner_roof_inset_m_nominal_image_ratio':inset,'hip_coeffs_eave_apex_U0_V0':hq.tolist(),
 'inner_historical_roof_n_train':int(sum(minor&train)),'inner_roof_n_hold':int(sum(minor&hold)),
 'inner_hip_hold_abs_p50_p90_p95_m':qtl(abs(Z[minor&hold]-hip(U[minor&hold],V[minor&hold],hq))),
 'upper_crown_elevation_m':cz,'upper_crown_bounded_rectangle':shape,'upper_outline_sampling_train_n':int(sum(broad)),'training_gap_supported_provisional_aperture':aperture,'aperture_high_training_pts_in_area':count,'upper_crown_train_n':len(tt),'upper_crown_hold_n':len(hh),
 'upper_crown_held_abs_p50_p90_p95_m':zerrs,'upper_crown_hold_horizontal_rect_contains_fraction':float(np.mean(np.all((hh>=ml)&(hh<=mh),axis=1)))}
(Path(__file__).parent/'calibration.json').write_text(json.dumps(rpt,indent=2)+'\n')
held_out={'roof':np.c_[uv[minor&hold],Z[minor&hold]].tolist(),'upper':np.c_[hh,Z[crestbox&hold]].tolist(),'lower':{n:np.c_[uv[m&hold],Z[m&hold]].tolist() for n,m in sides.items()}}
(Path(__file__).parent/'held-tower.json').write_text(json.dumps(held_out,separators=(',',':'))+'\n')
print(json.dumps(rpt,indent=2))
