"""Build a compact measured envelope for the long south raised roof element (material unassigned)."""
import json,sys,math,hashlib
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
from scipy.spatial import cKDTree
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D.parent))
from frame import loc
p=np.load(D.parent/'points.npz')['a']; xy=loc(p[:,:2]); x,y=xy.T;z=p[:,2]
train=np.isin(p[:,4],[59,60,61,62]); hold=np.isin(p[:,4],[19,20]); ok=(p[:,3]==1)&(p[:,5]==1)
bounds=(-11.08,15.14,-31.12,-27.95)
west,east,south,north=bounds
core=ok&(x>west+.30)&(x<east-.30)&(y>south)&(y<north)&(z>30.7)&(z<35.0)
frame=np.array([2,-29.58])
design=lambda a:np.c_[np.ones(len(a)),a-frame]
K=design(xy)
domains=[
 ('south_ramp',-30.98,-29.94,32.76,34.17,(-.012,.014),(.68,1.28),None),
 ('crest',-29.80,-29.47,33.94,34.32,(-.015,.015),(-.14,.10),None),
 ('north_ramp',-29.31,-28.56,32.66,34.19,(-.02,.02),(-1.85,-.85),(34.11,-1.21,.48)),
 ('north_shoulder',-28.45,-27.99,32.51,33.10,(-.010,.014),(-.91,-.32),None)]
coefs={}; tv={}; evals={}
for name,sy,ny,l,h,xb,yb,ref in domains:
 q=core&(y>sy)&(y<ny)&(z>l)&(z<h)
 if ref:q&=(abs(z-ref[0]-ref[1]*(y+29.58))<ref[2])
 assert sum(q&train)>130 and sum(q&hold)>45
 m=least_squares(lambda a:K[q&train]@a-z[q&train],[34.,0.,np.mean(yb)],bounds=([32.5,xb[0],yb[0]],[35.1,xb[1],yb[1]]),loss='soft_l1',f_scale=.10).x
 coefs[name]=m.tolist()
 tv[name]=q
 evals[name]={'train':int(sum(q&train)),'hold':int(sum(q&hold)),'plane_hold_abs_p50_p90_p95_m':np.quantile(abs(K[q&hold]@m-z[q&hold]),[.5,.9,.95]).tolist()}
print('fit',coefs)
M=[np.array(coefs[name]) for name,*_ in domains]
def meet(x,A,B):
 a=A-B;return frame[1]-(a[0]+a[1]*(x-frame[0]))/a[2]
F=[];V=[];stations=[]
for xedge in (west,east):
 ys=np.array([south,*[meet(xedge,A,B) for A,B in zip(M,M[1:])],north])
 zz=[float(m@np.array([1,xedge-frame[0],yedge-frame[1]])) for m,yedge in zip([M[0],*M],ys)]
 # zip for bottom then each outgoing plane: line intersections have identical heights either side.
 assert np.all(np.diff(ys)>.065),(ys,zz)
 stations.append(list(zip(ys.tolist(),zz)))
 V.extend((xedge,y,h-17.10) for y,h in zip(ys,zz))
V.extend([(west,south,31.95-17.1),(east,south,31.95-17.1),(east,north,31.95-17.1),(west,north,31.95-17.1)])
for i in range(4):F.extend([(i,i+5,i+6),(i,i+6,i+1)])
# Side closures with subdivisions exactly matching the roof and no invented visible shape outside the sampled XY.
# Split the two long vertical polygon faces with an interior fan.
for seq in ([0,1,2,3,4,13,10],[5,11,12,9,8,7,6]):
 h=len(V); V.append(tuple(np.mean(np.asarray(V)[seq],axis=0)))
 F.extend((h,a,b) for a,b in zip(seq,seq[1:]+seq[:1]))
F.extend([(0,10,11),(0,11,5),(4,9,12),(4,12,13),(10,13,12),(10,12,11)])
import collections
E=collections.defaultdict(list)
for f in F:
 for a,b in zip(f,f[1:]+f[:1]):E[min(a,b),max(a,b)].append((a,b))
assert all(len(f)==2 and f[0]==f[1][::-1] for f in E.values())
out=D/'Fisher-south-raised-roof-strip.obj'
out.write_text('# Closed roof element only, synthetic bottom, local axes z0 17.10m NAVD88. Unknown current material.\no Fisher_South_Raised_Roof_Reference\n'+''.join('v %.7f %.7f %.7f\n'%v for v in V)+''.join('f %d %d %d\n'%tuple(x+1 for x in f) for f in F))
outp=D/'strip-fit.json'
outp.write_text(json.dumps({'bounds':bounds,'training_plane_coefs':coefs,'fit_evaluation':evals,'roof_cross_section_end_stations_y_NAVD88':stations,'vertices':len(V),'triangles':len(F),
 'artificial_bottom_z_NAVD88':31.95,'object_sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2)+'\n')
helds=[]
for k,v in tv.items():
 helds.extend((k,*[float(b) for b in r]) for r in np.c_[xy[v&hold],z[v&hold]-17.1])
(D/'strip-held.csv').write_text('part,x,y,z_local\n'+''.join(f'{k},{x:.6f},{y:.6f},{z:.6f}\n' for k,x,y,z in helds))
print('station',stations,'triangles',len(F))
