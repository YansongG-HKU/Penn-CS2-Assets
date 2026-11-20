"""Top-down local depth/atlas audit for the Irvine sloped main roof."""
from roof_probe import *
from PIL import Image,ImageDraw
d=Path(__file__).parent; out=d/'roof'; source=d/'extracted-final/IrvineAuditorium'
step=.05; length=720
xy=(np.arange(length)+0.5)*step-length*step/2
def ras(path):
 x,f,uv,iu=read(path); pts=x[f]; uv=uv[iu]
 max_y=np.full((length,length),-100.)
 idx=np.full((length,length),-1,dtype=np.int32)
 tex=np.zeros((length,length,2),float)
 nn=np.cross(pts[:,1]-pts[:,0],pts[:,2]-pts[:,0]); norm=nn/np.maximum(1e-10,np.linalg.norm(nn,axis=-1)[:,None])
 for j,(a,b,c) in enumerate(pts):
  if max(a[1],b[1],c[1])<27 or norm[j,1]<.1:continue
  cand=np.array([a,b,c])[:,[0,2]]
  low=np.clip(np.floor((cand.min(0)-xy[0])/step).astype(int),0,length-1); high=np.clip(np.ceil((cand.max(0)-xy[0])/step).astype(int),0,length-1)
  if np.any(high<low):continue
  x0,y0=low;x1,y1=high
  t1,t2=cand[1]-cand[0],cand[2]-cand[0];T=np.column_stack([t1,t2])
  if abs(np.linalg.det(T))<1e-10:continue
  X,Y=np.meshgrid(xy[x0:x1+1],xy[y0:y1+1]); M=np.stack([X,Y],axis=-1)
  B=(M-cand[0])@np.linalg.inv(T).T
  C=np.concatenate([(1-np.sum(B,axis=-1))[...,None],B],axis=-1)
  Y2=C@pts[j,:,1]
  r=np.s_[y0:y1+1,x0:x1+1]
  mask=(C.min(axis=-1)>-1e-8)&(Y2>max_y[r])
  max_y[r][mask]=Y2[mask]
  idx[r][mask]=j
  tex[r][mask]=(C@uv[j])[mask]
 return max_y,idx,tex,norm,pts
def img(name):
 return np.array(Image.open(source/('NA_IrvineAuditorium_7x7'+name+'.png')).convert('RGBA'))[:,:,:3]
def sample(tex,UV):
 h,w=tex.shape[:2]
 x=np.minimum(w-1,np.maximum(0,(w*UV[...,0]).astype(np.int32)))
 y=np.minimum(h-1,np.maximum(0,(h*(1-UV[...,1])).astype(np.int32)))
 return tex[y,x]
L1=ras(source/'NA_IrvineAuditorium_7x7_LOD1.fbx');L2=ras(source/'NA_IrvineAuditorium_7x7_LOD2.fbx')
q=(L2[3][:,1]>.75)&(L2[3][:,1]<.85)&(L2[4][:,:,1].min(1)==29)&(L2[4][:,:,1].max(1)==40.5)
rf=np.flatnonzero(q);assert len(rf)==16
mask=np.isin(L2[1],rf)
s2=sample(img('_LOD2_BaseColor'),L2[2]); s1=sample(img('_BaseColor'),L1[2])
v2=s2.mean(axis=-1);v1=s1.mean(axis=-1)
n1=L1[3][np.maximum(0,L1[1])]
ys=L1[0]-L2[0]
# Operational ranges only for QA categories, not a surface decision by color alone.
valid=mask&(L1[1]>=0)&(n1[:,:,1]>.45)
bright=mask&(v2>65)
mid_dark=valid&(v1<50)
metric={}
for l,b in [('far_roof',mask),('geometrically_matched_mid_tilt',valid),('far_bright',bright),('far_bright_mid_dark',bright&mid_dark),
 ('far_bright_mid_dark_ywithin_1m',bright&mid_dark&(abs(ys)<1.0)),
 ('far_bright_mid_dark_ywithin_2m',bright&mid_dark&(abs(ys)<2.0))]:
 metric[l]={'pixels':int(b.sum()),'fraction_far_roof':float(b.sum()/mask.sum()),'median_mid_minus_far_Y_m':float(np.median(ys[b]))}
print(metric)
(out/'slope-pixel-report.json').write_text(json.dumps(dict(far_slate_faces=rf.tolist(),grid_spacing_m=step,metrics=metric),indent=2)+'\n')
D=np.zeros((length,length,3),np.uint8);D[mask]=[32,39,52];D[valid]=[85,100,120];D[bright]=[230,169,40];D[bright&mid_dark]=[218,50,66]
for n,x in [('mid',s1),('far',s2),('classified',D)]:
 image=np.zeros_like(x)+28
 image[mask]=x[mask];Image.fromarray(image).save(out/f'roof-proj-{n}.png')
np.savez_compressed(out/'roof-proj-raw.npz',mid_h=L1[0],mid_f=L1[1],mid_uv=L1[2],far_h=L2[0],far_f=L2[1],far_uv=L2[2],far_slate=mask)
