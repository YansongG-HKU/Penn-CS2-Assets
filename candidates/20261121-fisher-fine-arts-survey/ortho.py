from frame import *
from PIL import Image,ImageDraw,ImageFont
im=Image.open(D/'ortho-2025.png').convert('RGB')
size=(640,860); x0,y0=-30,40;s=.1
def p2(u,v):
 a=np.array([u,v])@T+O
 return np.array([(a[0]-483503)*8,(4422449-a[1])*8])
U=p2(x0,y0); M=np.array([p2(x0+s,y0)-U,p2(x0,y0-s)-U,U]).T.flatten()
z=im.transform(size,Image.Transform.AFFINE,M,Image.Resampling.BICUBIC)
z.save(D/'ortho-rectified.png')
t=lambda p:(int((p[0]-x0)/s),int((y0-p[1])/s))
dd=ImageDraw.Draw(z)
for x in range(-25,26,5):
 dd.line([t((x,-38)),t((x,38))],fill='#70bb9c');dd.text(t((x,39)),str(x),fill='white')
for y in range(-35,36,5):
 dd.line([t((-29,y)),t((29,y))],fill='#70bb9c');dd.text(t((-29,y+1)),str(y),fill='white')
dd.line([t(a) for a in np.r_[P,P[:1]]],fill='#ffdc86',width=2)
dd.rectangle([t((-10.95,14.38)),t((-8.02,11.50))],outline='#ff4238',width=3)
z.save(D/'ortho-overlays.jpg',quality=93)
