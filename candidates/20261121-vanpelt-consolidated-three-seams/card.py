from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
D=Path(__file__).parent
I=Image.new('RGB',(1300,800),'#eef4f7');g=ImageDraw.Draw(I)
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def tx(x,y,s,n=25,col='#183647',b=False):g.text((x,y),s,font=ImageFont.truetype(F.replace('Regular','Bold') if b else F,n,index=2),fill=col)
tx(44,25,'宾大 Van Pelt Library',51,b=True);tx(46,107,'远景 LOD2  ·  修复整合版的三层接缝',28,'#41677b')
g.rounded_rectangle((44,165,651,624),radius=15,fill='white');g.rounded_rectangle((677,165,1257,624),radius=15,fill='white')
tx(68,187,'修复后外观：原贴图保持不变',24,b=True)
z=Image.open(D/'repaired.png').convert('RGBA');z.thumbnail((585,345)); I.paste(z,(55+(590-z.width)//2,270),z)
tx(702,187,'剖面示意：去除内盖，保留外沿',24,b=True)
for x,before in [(712,True),(971,False)]:
 tx(x,246,'修复前' if before else '修复后',24,b=True)
 # Illustrative section; no statement of measured depth/shape.
 p=[(x+9,485),(x+9,464),(x+29,464),(x+29,337),(x+48,337),(x+48,293),
    (x+165,293),(x+165,337),(x+185,337),(x+185,464),(x+205,464),(x+205,485),(x+9,485)]
 g.line(p,fill='#31586a',width=5)
 if before:
  for y,a,b in [(337,49,165),(416,30,185),(463,30,185)]:
   g.line((x+a,y-2,x+b,y-2),fill='#ad492f',width=4)
   g.line((x+a,y+5,x+b,y+5),fill='#c67948',width=4)
 else:
  for xx in [9,29,165,185]:
   if xx in (29,165):g.line((x+xx,337,x+xx+19,337),fill='#248177',width=5)
   else:g.line((x+xx,464,x+xx+20,464),fill='#248177',width=5)
 tx(x,512,'三层内部重叠面' if before else '一个闭合远景外壳',20,'#8b4b36' if before else '#155f5b')
tx(701,575,'外部体量与两圈可见外沿保持',19,'#506d7e')
g.rounded_rectangle((44,650,1257,723),radius=15,fill='#123c50')
tx(72,667,'48 → 52 三角面',28,'white',True);tx(499,669,'三处反向重叠面积复查归零，原 UV 保留',24,'#d8ebed')
tx(45,749,'不是测绘版重建；未改变原地块，也未做 CS2 游戏内验收。',21,'#456777')
I.save(D/'Van-Pelt-LOD2-three-seams.webp',quality=94)
I.thumbnail((900,700));I.save(D/'proof.png')
