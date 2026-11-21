from frame import *
from PIL import Image,ImageDraw,ImageFont
import collections
source=np.unique(np.loadtxt(D/'fisher-points.csv.gz',delimiter=',',skiprows=1),axis=0)
LC=loc(source[:,:2]); Z=source[:,2]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
xmin,ymax,scale=-31,42,9
im=Image.new('RGB',(558,765),'#e9eef1');draw=ImageDraw.Draw(im)
pix=lambda p:(int((p[0]-xmin)*scale),int((ymax-p[1])*scale))
poly=ring(P)
bounds=lambda a:poly.Contains(ogr.CreateGeometryFromWkt(f'POINT ({a[0]} {a[1]})'))
M=(source[:,3]==1)&(source[:,5]==1)
q=collections.defaultdict(list)
for a,z in zip(LC[M],Z[M]): q[tuple(np.floor(a/.65))].append(z)
for k,zz in q.items():
 x,y=np.array(k)*.65
 if not bounds((x+.3,y+.3)):continue
 zj=np.quantile(zz,.70); c=int(np.clip((zj-19)*8,0,255));w=int(np.clip((zj-35)*11,0,255))
 draw.rectangle((pix((x,y+.65)),pix((x+.65,y))),fill=(c,int((255-c)*.60+w*.32),int((255-c)*.70)))
xy=list(map(pix,P));draw.line(xy+xy[:1],fill='white',width=2)
for x in range(-30,31,5):draw.line((pix((x,42)),pix((x,-43))),fill='#696f76');draw.text(pix((x,41)),str(x),fill='black',font=font)
for y in range(-40,41,5):draw.line((pix((-31,y)),pix((31,y))),fill='#696f76');draw.text(pix((-30.8,y)),str(y),fill='black',font=font)
im.save(D/'height-grid.jpg')
print('point count',len(source),'classes',collections.Counter(source[:,3]),'passes',collections.Counter(source[:,4]))
for a,b,c,d,name in [(-25,-20,-14,6,'western border'),(-25,-22,-8,-5,'west entry outer'),(-24,-8,5,16,'x wide'),(-22,-5,-10,7,'western Tower'),(-10,14,15,34,'apse'),(-16,17,-32,-13,'south'),(10,22,-18,22,'east'),(-12,12,-20,22,'central roof'),(-22,-9,-4,9,'top tower')]:
 w=(LC[:,0]>a)&(LC[:,0]<c)&(LC[:,1]>b)&(LC[:,1]<d)
 for m,k in ((M,'first-return'),(source[:,3]==2,'ground')):
  iz=Z[w&m];print(name,k,len(iz),np.quantile(iz,[.05,.25,.5,.75,.9,.99,1]).round(2) if len(iz) else '')
np.savez_compressed(D/'points.npz',a=source)
