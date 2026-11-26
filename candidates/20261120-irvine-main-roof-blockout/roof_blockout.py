"""Form a detached Irvine main roof shell against independent observed sections."""
from pathlib import Path
import json,math
import numpy as np
from scipy.optimize import least_squares
D=Path(__file__).parent
a=np.load(D/'irvine-cropped-points.npz')['data']
ref=json.loads((D/'irvine-roof-plane-fit.json').read_text())
C=np.array(ref['plane_meeting_utm_xy']); E=np.array(ref['local_east_axis_utm']); N=np.array(ref['local_north_axis_utm'])
L=(a[:,:2]-C)@np.column_stack([E,N]);z=a[:,2]
valid=(a[:,3]==1)&(a[:,5]==1)
held=np.isin(a[:,4],[19,20]); R={}
basis={'east':(0,+1),'west':(0,-1),'north':(1,+1),'south':(1,-1)}
pred=lambda x,r: r[0]+r[1]*x+r[2]*np.maximum(0,x-r[3])
for label,(ax,k) in basis.items():
 d=L[:,ax]*k; c=L[:,1-ax]
 mask=valid&(abs(c)<1.25)&(d>1.55)&(d<8.35)&(z>52.7)&(z<65)
 train=mask&~held;val=mask&held
 dtr,ztr=d[train],z[train]
 assert len(dtr)>90 and val.sum()>30
 low=(61,-2.8,0.0,4.25);high=(70,-.8,2.2,7.8)
 fit=least_squares(lambda r:pred(dtr,r)-ztr,[65.5,-1.55,.7,6.4],bounds=(low,high),loss='soft_l1',f_scale=.11).x
 ev=np.abs(pred(d[val],fit)-z[val]); er=np.abs(pred(dtr,fit)-ztr)
 R[label]=dict(params=fit.tolist(),profile='Z=c+s*r+delta*max(0,r-break_r)',
  train=int(train.sum()),holdout=int(val.sum()),holdout_residual_quantiles_m=np.quantile(ev,[.5,.9,.95]).tolist(),
  holdout_within_0p45m=int(np.sum(ev<=.45)),train_median_residual_m=float(np.median(er)))
print('Fits',json.dumps(R,indent=1))
# Use how far the measured roof quadrant remains above 52.8 m in each axial strip.
# Exclude isolated near-vertical cladding hits by looking for stable contiguous bins.
eave={}
for name,(ax,k) in basis.items():
 d=L[:,ax]*k; other=L[:,1-ax]
 v=valid&(abs(other)<1.2)&(d>7)&(d<9.5)&(z>=52.8)&(z<=54.4)&~held
 assert v.sum()>20
 q=np.quantile(d[v],[.9,.97,.99])
 eave[name]=dict(outer_coord_m=float(q[1]),training_hits=int(v.sum()),radial_quantiles_m=q.tolist(),accepted_eave_height_m=float(np.median(z[v&(d>q[0])])))
print('Eaves',json.dumps(eave,indent=1))
# Three rings: local collar (not the geometric finial), measured roof-slope break,
# and eave. For coherent corner geometry blend the two independently fitted sides.
names=('east','north','west','south')
collar=1.50  # Support cutoff of this test blockout only, not a measured spire base.
collar_ring={n:[collar,float(pred(collar,R[n]['params']))] for n in names}
eave_ring={n:[eave[n]['outer_coord_m'],eave[n]['accepted_eave_height_m']] for n in names}
break_ring={n:[R[n]['params'][3],float(pred(R[n]['params'][3],R[n]['params']))] for n in names}
q=[]
for r in (eave_ring,break_ring,collar_ring):
 face=lambda h,v,sg,tg:(sg*r[h][0],tg*r[v][0],(r[h][1]+r[v][1])/2)
 q += [(r['east'][0],0,r['east'][1]),face('east','north',1,1),
       (0,r['north'][0],r['north'][1]),face('west','north',-1,1),
       (-r['west'][0],0,r['west'][1]),face('west','south',-1,-1),
       (0,-r['south'][0],r['south'][1]),face('east','south',1,-1)]
F=[]
for b in (0,8):
 for i in range(8):
  j=(i+1)%8
  F.extend(((b+i,b+j,b+8+j),(b+i,b+8+j,b+8+i)))
# Close the standalone reference object without interpreting caps as exterior.
bottom=len(q);q += [(x,y,52.0) for x,y,z in q[:8]]
for i in range(8):
 j=(i+1)%8;F.extend(((i,bottom+i,bottom+j),(i,bottom+j,j)))
topcenter=len(q);q.append((0,0,sum(z for x,y,z in q[16:24])/8))
basecenter=len(q);q.append((0,0,52.0))
for i in range(8):
 j=(i+1)%8
 F.append((basecenter,bottom+j,bottom+i))
 F.append((topcenter,16+i,16+j))
q=np.array(q)
from collections import defaultdict
E0=defaultdict(list)
for f in F:
 for i,j in zip(f,f[1:]+f[:1]):E0[tuple(sorted([i,j]))].append((i,j))
assert all(len(z)==2 and z[0]==z[1][::-1] for z in E0.values())
assert min(np.linalg.norm(np.cross(q[f[1]]-q[f[0]],q[f[2]]-q[f[0]])) for f in F)>1e-6
# Evaluate finished roof top on held-out 2D coordinates against its actual triangle geometry.
def heights(xxy):
 h=np.full(len(xxy),np.nan)
 for f in F[:32]:
  s=q[list(f)]
  t=np.column_stack([s[1,:2]-s[0,:2],s[2,:2]-s[0,:2]])
  w=(xxy-s[0,:2])@np.linalg.inv(t).T
  bary=np.c_[1-w.sum(1),w]
  k=(bary.min(1)>=-1e-10);h[k]=(bary@s[:,2])[k]
 return h
report={}
for label,(ax,k) in basis.items():
 d=L[:,ax]*k;c=L[:,1-ax]
 val=held&valid&(abs(c)<1.0)&(d>2)&(d<8.1)&(z>52.7)&(z<65)
 zh=heights(L[val]); good=np.isfinite(zh);err=np.abs(zh[good]-z[val][good]);assert good.mean()>.85 and len(err)>20
 report[label]=dict(test_n=len(err),held_median_m=float(np.median(err)),held_p90_m=float(np.quantile(err,.9)),within_0p75m=float((err<=.75).mean()))
diag=held&valid&(np.max(abs(L),axis=1)>2.)&(np.max(abs(L),axis=1)<8.05)&(abs(abs(L[:,0])-abs(L[:,1]))<1.2)&(z>53)&(z<65)
e=heights(L[diag]); ok=np.isfinite(e);d=np.abs(e[ok]-z[diag][ok])
report['off_axis_diagonal_diagnostic']={'subset_n':int(diag.sum()),'observed_n':len(d),
 'held_median_m':float(np.median(d)),'held_p90_m':float(np.quantile(d,.9)),'within_0p75m':float((d<=.75).mean()),
 'caution':'Includes genuine features missing from detached massing; not part of the four axis strip fit.'}
print('Finished mesh holdout',report)
assert max(report[k]['held_median_m'] for k in basis)<.25
status='geometry_reference_only'
O=D/'roof-blockout';out=O/'Irvine-main-roof-sectional-blockout.obj'
with out.open('w') as f:
 f.write('# Diagnostic upper roof only; no installed asset. X/Y are local axes, Z relative to 14.4m NAVD88.\n')
 f.write('o Irvine_Roof_Shape_Reference\n')
 for x,y,z in q:f.write(f'v {x:.6f} {y:.6f} {z-14.4:.6f}\n')
 for a,b,c in F:f.write(f'f {a+1} {b+1} {c+1}\n')
(O/'blockout-evidence.json').write_text(json.dumps(dict(status=status,fit_profiles=R,eave_estimates=eave,finished_mesh_scan_holdout=report,
 near_grade_navd88_m=14.4,model_utm_center=C.tolist(),model_axes_utm=ref['local_east_axis_utm'],roofs='central only',
 output_points=len(q),output_triangles=len(F),closed_oriented_edges=len(E0),unmeasured_collar_radius_m=collar,
 note='The bottom cap and collar are diagnostic closure only. Material, walls, protruding side structures and true spire not included. Historic center feature not rescaled.'),indent=2)+'\n')
