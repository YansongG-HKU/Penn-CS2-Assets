from PIL import Image,ImageDraw
from pathlib import Path
import csv,gzip,json,colorsys
import numpy as np
d=Path(__file__).resolve().parent
with gzip.open(d/'irvine-office-lidar.csv.gz','rt') as f:
 reader=csv.DictReader(f); data=np.array([[float(r[k]) for k in ('X','Y','Z','Classification','PointSourceId','ReturnNumber')] for r in reader])
data=np.unique(data,axis=0)
ortho=np.array(Image.open(d/'ortho-2025-full.png').convert('RGB'))
e=json.loads((d/'ortho-2025-full-extent.json').read_text())['extent'];mm=(e['xmax']-e['xmin'])/740
p=np.stack([(data[:,0]-e['xmin'])/mm-.5,(e['ymax']-data[:,1])/mm-.5],axis=1)
idx_ok=(data[:,3]==1)&(data[:,2]>20)&(data[:,2]<94)&(data[:,5]==1)
sample=data[idx_ok];pos=p[idx_ok]
colors={z:np.array(tuple(int(t*255) for t in colorsys.hsv_to_rgb(max(0., min(.76,.75-(z-22)/60)),.85,.98))) for z in range(22,83)}
im=Image.fromarray(ortho).convert('RGBA'); vis=Image.new('RGBA',im.size); draw=ImageDraw.Draw(vis)
for (x,y),z in zip(pos[np.argsort(sample[:,2])],np.sort(sample[:,2])):
 k=int(np.clip(z,22,82));draw.point((x,y),fill=(*colors[k],220))
a=Image.alpha_composite(im,vis).crop((163,160,530,540)).resize((734,760))
b=ImageDraw.Draw(a)
for i,z in enumerate(range(22,83,5)):
 x=15+i*51; b.rectangle((x,12,x+43,22),fill=tuple(colors[z]));b.text((x+2,25),str(z),fill='white')
a.convert('RGB').save(d/'irvine-point-height-preview.jpg',quality=92)
print('raw uniq',len(data),'filtered',len(sample),'source ids',np.unique(sample[:,4],return_counts=True))
print('raw kept Z quantile',np.quantile(sample[:,2],[0,.01,.1,.25,.5,.75,.9,.95,.99,.999,1]))
np.savez_compressed(d/'irvine-cropped-points.npz',data=data,ref_px=p)
