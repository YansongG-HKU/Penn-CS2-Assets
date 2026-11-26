"""Inverse atlas validation and mid model correspondence for Irvine roof texels."""
from roof_probe import *
from PIL import Image,ImageDraw,ImageFilter
d=Path(__file__).parent; out=d/'roof'; source=d/'extracted-final/IrvineAuditorium'
info=json.loads((out/'slope-pixel-report.json').read_text()); ids=set(info['far_slate_faces'])
far=source/'NA_IrvineAuditorium_7x7_LOD2.fbx'; mid=source/'NA_IrvineAuditorium_7x7_LOD1.fbx'
x,f,uv,iu=read(far); tex=uv[iu]
xx=x[f]; width=1024
F=np.full((width,width),-1,dtype=np.int32); occupy=np.zeros(F.shape,np.int16)
farxyz=np.zeros(F.shape+(3,))
ig=np.indices(F.shape).transpose(1,2,0)[...,::-1]
# Include a two-pixel check around all non-target triangles; they must never acquire any changed texels.
blocked_img=Image.new('L',(width,width))
blocked_draw=ImageDraw.Draw(blocked_img)
for i,A in enumerate(tex):
 Q=np.c_[width*A[:,0],width*(1-A[:,1])]
 if i not in ids:
  blocked_draw.polygon([tuple(t) for t in Q],fill=255)
  continue
 a,b,c=Q
 T=np.column_stack((b-a,c-a))
 low=np.maximum(0,np.floor(Q.min(0)).astype(int)); high=np.minimum(width-1,np.ceil(Q.max(0)).astype(int))
 x0,y0=low; x1,y1=high;r=np.s_[y0:y1+1,x0:x1+1]
 bary=(ig[r]+.5-a)@np.linalg.inv(T).T
 bary=np.concatenate([(1-np.sum(bary,axis=-1))[...,None],bary],axis=-1)
 inside=bary.min(axis=-1)>-1e-9
 F[r][inside]=i;occupy[r][inside]+=1
 farxyz[r][inside]=(bary@xx[i])[inside]
blocked=np.asarray(blocked_img.filter(ImageFilter.MaxFilter(7)))>0
mask=(F>=0)&(occupy==1)&(~blocked)
nb=np.load(out/'roof-proj-raw.npz')
gx=np.rint((farxyz[:,:,0]+18)/.05-.5).astype(int).clip(0,719)
gz=np.rint((farxyz[:,:,2]+18)/.05-.5).astype(int).clip(0,719)
mf=nb['mid_f'][gz,gx]; mh=nb['mid_h'][gz,gx]; mu=nb['mid_uv'][gz,gx]
mx,mtri,*_=read(mid);mxyz=mx[mtri];M=np.cross(mxyz[:,1]-mxyz[:,0],mxyz[:,2]-mxyz[:,0]);M=M/np.maximum(1.e-10,np.linalg.norm(M,axis=1,keepdims=True))
valid=mask&(mf>=0)&(M[mf,1]>.45)&(abs(mh-farxyz[:,:,1])<2)&(mh>=29.)
def load(suffix):
 b='NA_IrvineAuditorium_7x7'
 return [np.asarray(Image.open(source/(b+t+'_'+suffix+'.png')).convert('RGBA')) for t in ('_LOD2','')]
A,B=load('BaseColor');ix=(4096*mu[:,:,0]).astype(int).clip(0,4095);iy=(4096*(1-mu[:,:,1])).astype(int).clip(0,4095)
bn=B[iy,ix]
label=valid&(A[:,:,:3].mean(-1)>65)&(bn[:,:,:3].mean(-1)<50)
rect=tuple(int(op(x)) for x,op in zip((np.where(label)[1],np.where(label)[0],np.where(label)[1],np.where(label)[0]),(min,min,max,max)))
print('counts',int(mask.sum()),int(valid.sum()),int(label.sum()),rect)
t={}
for tag in ('BaseColor','MaskMap','ControlMask','Normal','Emissive'):
 a,b=load(tag); u=a[label];v=b[iy[label],ix[label]]
 q=lambda p:np.quantile(p,[.01,.5,.99],axis=0).round(2).tolist()
 t[tag]={'far':q(u),'mid':q(v),'exact':float((u==v).all(axis=-1).mean())}
 print(tag,t[tag])
(out/'roof-atlas-precise.json').write_text(json.dumps(dict(eligible_owned_target=int(mask.sum()),matched_candidate=int(valid.sum()),
 selected_texels=int(label.sum()),selection_bbox=rect,target_triangles=sorted(ids),paired_atlas_channels=t),indent=2)+'\n')
np.savez_compressed(out/'roof-atlas-probe.npz',target=label,blocked=blocked,far_face_id=F,donor_iy=iy,donor_ix=ix)
