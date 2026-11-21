import sys,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
d,report,path=map(Path,sys.argv[1:])
O=Image.new('RGB',(960,720),(53,60,71));P=ImageDraw.Draw(O)
R={}
for i,view in enumerate(('front','rear','aerial')):
 for mode in ('base','lit'):
  b=[]
  for j,s in enumerate(('before','after')):
   img=Image.open(d/f'{s}-{mode}-{view}.png').convert('RGBA');b.append(np.asarray(img).astype(int))
   if mode=='base':
    img.thumbnail((480,240));O.paste(img,(j*480,i*240),img);P.text((j*480+8,i*240+4),f'{s} / {view}',fill='white')
  c=np.max(abs(b[0]-b[1]),axis=-1)
  masks=[x[:,:,3]>=128 for x in b]
  vol=int((masks[0]!=masks[1]).sum()); assert not vol
  R[view+'-'+mode]={'changed_gt2':int((c>2).sum()),'max_channel_diff':int(c.max()),'silhouette_different_px':vol}
O.save(path,quality=93)
report.write_text(json.dumps(R,indent=2)+'\n')
print(R)
