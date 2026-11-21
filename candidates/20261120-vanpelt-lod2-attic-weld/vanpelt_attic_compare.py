from PIL import Image
from pathlib import Path
import numpy as np,sys,json
src,report=map(Path,sys.argv[1:])
result={}
for mode in ('base','lit'):
 for view in ('front','rear','aerial'):
  a,b=[np.array(Image.open(src/f'{x}-{mode}-{view}.png').convert('RGBA'),np.int16) for x in ('before','after')]
  df=np.abs(a-b);mask=(a[:,:,3]>=128)&(b[:,:,3]>=128)
  px=df[:,:,:3].max(axis=2)[mask]
  sil=int(np.count_nonzero((a[:,:,3]>=128)!=(b[:,:,3]>=128)))
  row={'silhouette_delta_px':sil,'joint_foreground_px':len(px),'joint_foreground_q50_q95_q99_max_channel_delta':np.quantile(px,[.5,.95,.99,1]).tolist(),'joint_foreground_gt12_px':int((px>12).sum())}
  if sil or (mode=='base' and row['joint_foreground_q50_q95_q99_max_channel_delta'][-1]>2) or (mode=='lit' and row['joint_foreground_gt12_px']>1):
   raise ValueError((mode,view,row))
  result[f'{mode}-{view}']=row
report.write_text(json.dumps(result,indent=2)+chr(10))
print(result)
