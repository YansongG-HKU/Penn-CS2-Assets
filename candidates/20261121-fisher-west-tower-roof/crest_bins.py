"""Train-only crest station support. No readback data used to select candidates."""
import sys,json
from pathlib import Path
import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
d=Path(__file__).resolve().parent; sys.path.insert(0,str(d.parent));from frame import loc
c=json.loads((d/'calibration.json').read_text());a=np.load(d.parent/'points.npz')['a']; W=loc(a[:,:2]);az=np.deg2rad(c['rotation_local_deg']);W=W@np.array([[np.cos(az),-np.sin(az)],[np.sin(az),np.cos(az)]])
x,y=W.T; z=a[:,2]; w,e,s,n=c['rim_midline_bounds_W_E_S_N']; box=c['upper_crown_bounded_rectangle']; S=np.isin(a[:,4],[59,60,61,62])&(a[:,3]==1)&(a[:,5]==1); h=np.isin(a[:,4],[19,20])&(a[:,3]==1)&(a[:,5]==1)
C=[]
for tag,val,orth,center,rnge in [('west',y,x,w,(s+.27,n-.27)),('east',y,x,e,(s+.27,n-.27)),('south',x,y,s,(w+.27,e-.27)),('north',x,y,n,(w+.27,e-.27))]:
 gate=(abs(orth-center)<.72)&(z>=45.52)&(z<=46.02)
 if tag=='north':gate&=((x<box[0]-.19)|(x>box[1]+.19))
 bins=np.arange(rnge[0],rnge[1]+.101,.10)
 k,_=np.histogram(val[gate&S],bins); mid=(bins[1:]+bins[:-1])*.5
 curve=gaussian_filter1d(k.astype(float),1.5)
 peaks,details=find_peaks(curve,distance=7,prominence=.9,height=1.5)
 found=[]
 for idx in peaks:
  g=gate&(abs(val-mid[idx])<.26)
  tr=g&S; hd=g&h
  if sum(tr)<5 or len(set(a[tr,4]))<2:continue
  cand={'side':tag,'plan_station_m':float(mid[idx]),'train_z_median':float(np.median(z[tr])),'train_count':int(sum(tr)),'held_count':int(sum(hd))}
  if sum(hd):cand['hold_z_abs_m_p50_p90']=np.quantile(abs(z[hd]-cand['train_z_median']),[.5,.90]).tolist()
  found.append(cand)
 print(tag,[(round(p['plan_station_m'],2),p['train_count'],p['held_count']) for p in found],flush=True)
 C.extend(found)
(d/'crest-stations.json').write_text(json.dumps({'quality_note':'Training-gated observed stations of high crest returns, not an exact ornament count or complete preservation schedule. Held points not used to tune station positions.','stations':C},indent=2)+'\n')
