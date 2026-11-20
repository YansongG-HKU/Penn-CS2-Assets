"""Conservative same-surface correction of Irvine's 795 attributable slate texels."""
import hashlib,json,shutil
from pathlib import Path
import numpy as np
from PIL import Image
d=Path(__file__).parent; source=d/'extracted-final/IrvineAuditorium'; out=d/'roof-candidate/IrvineAuditorium'
shutil.copytree(source,out)
n=np.load(d/'roof/roof-atlas-probe.npz')
T=n['target']; face=n['far_face_id']; blocked=n['blocked']; good=n['good']
assert T.sum()==795 and not (T&blocked).any()
st='NA_IrvineAuditorium_7x7'
def q(label,far):
 file=source/(st+('_LOD2' if far else '')+'_'+label+'.png')
 return file,Image.open(file)
def read(label):
 return np.array(q(label,True)[1].convert('RGBA'))
mask=read('MaskMap'); cm=read('ControlMask'); normal=read('Normal')
# Actual same-face far slate has different roughness encoding from LOD1. Use verified
# local far material codes and normal direction, not raw tangent values from LOD1.
G=good&(mask==[170,0,0,127]).all(-1)&(cm==[0,0,255,0]).all(-1)&(normal[:,:,2]>=244)
dy,dx=np.where(T)
ny,nx=np.zeros_like(dy),np.zeros_like(dx)
max_d=0
for i in np.unique(face[T]):
 yy,xx=np.where(G&(face==i)); I=np.flatnonzero(face[T]==i)
 assert len(xx)>0
 DD=(yy[None,:]-dy[I,None])**2+(xx[None,:]-dx[I,None])**2
 p=np.argmin(DD,axis=1); ny[I]=yy[p];nx[I]=xx[p]
 max_d=max(max_d,int(np.max(np.min(DD,axis=1))))
assert max_d<=35**2,max_d
sha=lambda b:hashlib.sha256(b).hexdigest()
report={}
for label in ('BaseColor','MaskMap','ControlMask','Normal','Emissive'):
 f,s=q(label,True); a=np.array(s.convert('RGBA'));b=a.copy()
 if label=='BaseColor':
  near=np.asarray(q(label,False)[1].convert('RGBA'))
  ys,xs=n['donor_iy'][T],n['donor_ix'][T]
  b[T]=near[ys,xs]
 elif label!='Emissive':b[T]=a[ny,nx]
 active=np.any(a!=b,axis=-1)
 assert not (active & ~T).any()
 if np.any(active):
  Image.fromarray(b,'RGBA').convert(s.mode).save(out/f.name,optimize=False,**{k:v for k,v in s.info.items() if k in ('exif','dpi','icc_profile')})
 reread=np.asarray(Image.open(out/f.name).convert('RGBA'));assert np.array_equal(b,reread)
 report[label]={'before_sha256':sha(f.read_bytes()),'after_sha256':sha((out/f.name).read_bytes()),'after_rgba_sha256':sha(b.tobytes()),'exact_pixels_changed':int(active.sum())}
print('max donor distance',max_d**.5,report)
(d/'roof/roof-texture-receipt.json').write_text(json.dumps(dict(manual_sources_check='Penn southeast color view and full 2025 roof crop, no geometry scaling',
 same_face_far_slate_max_donor_dist_pixel=max_d**.5,mask_selection_texels=int(T.sum()),texture_results=report),indent=2)+'\n')
