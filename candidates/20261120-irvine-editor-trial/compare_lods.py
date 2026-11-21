"""Compare body-only orthographic silhouettes under a neutral material."""
import itertools,json,sys
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
d,report,preview=map(Path,sys.argv[1:])
R={};im=Image.new('RGB',(960,468),(47,56,68));p=ImageDraw.Draw(im)
for j,v in enumerate(('front','aerial')):
 views=[Image.open(d/f'LOD{i}-{v}.png').convert('RGBA') for i in range(3)]
 masks=[np.asarray(f)[:,:,3]>=128 for f in views]
 for i in range(2):
  a,b=masks[i:i+2]
  R[f'{v}-LOD{i}-to-{i+1}']={'relative_silhouette_delta_pct':round(100*int(np.sum(a!=b))/int(np.sum(a|b)),4)}
 for i,img in enumerate(views):
  img.thumbnail((320,216)); im.paste(img,(i*320,18+j*234),img);p.text((11+i*320,4+j*234),f'LOD{i} / {v}',fill='white')
report.write_text(json.dumps(R,indent=2)+'\n')
im.save(preview,quality=90)
print(R)
