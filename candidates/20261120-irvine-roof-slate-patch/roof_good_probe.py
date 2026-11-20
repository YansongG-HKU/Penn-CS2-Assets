from roof_map_probe import *
good=valid&(A[:,:,:3].mean(-1)<50)&(bn[:,:,:3].mean(-1)<50)
buf=Image.fromarray(np.where(good,255,0).astype(np.uint8))
for tag in ('MaskMap','ControlMask','Normal'):
 a,b=load(tag);c=a[good]
 print(tag,np.quantile(c,[.01,.1,.5,.9,.99],axis=0),collections.Counter(map(tuple,c.tolist())).most_common(4))
np.savez_compressed(out/'roof-atlas-probe.npz',target=label,blocked=blocked,far_face_id=F,donor_iy=iy,donor_ix=ix,valid=valid,good=good)
