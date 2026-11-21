from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
D=Path(__file__).parent
I=Image.new('RGB',(1300,760),'#eef4f7');g=ImageDraw.Draw(I)
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def tx(x,y,s,n=25,col='#183647',b=False):
 g.text((x,y),s,font=ImageFont.truetype(F.replace('Regular','Bold') if b else F,n,index=2),fill=col)
tx(42,26,'宾大 Irvine Auditorium',49,b=True);tx(45,105,'远景 LOD2  ·  整合候选包的尖塔接缝修复',28,'#41677b')
g.rounded_rectangle((45,162,630,617),radius=15,fill='white')
g.rounded_rectangle((654,162,1254,617),radius=15,fill='white')
tx(66,179,'修复后外观：保留原贴图',25,b=True)
z=Image.open(D/'repaired.png').convert('RGBA');z.thumbnail((550,390)); I.paste(z,(65+(540-z.width)//2,224),z)
tx(678,179,'尖塔接缝剖面示意',25,b=True)
for x,before in [(702,True),(982,False)]:
 tx(x,232,'修复前' if before else '修复后',24,b=True)
 g.line([(x+65,484),(x+65,365),(x+110,281),(x+155,365),(x+155,484)],fill='#30566a',width=6)
 g.line([(x+30,511),(x+30,482),(x+190,482),(x+190,511)],fill='#30566a',width=6)
 if before:
  g.line((x+69,383,x+151,383),fill='#b94c32',width=6)
  g.line((x+69,393,x+151,393),fill='#c27a46',width=6)
 else:
  g.line((x+71,388,x+149,388),fill='#68a8a2',width=2)
  for y in range(378,393,7):g.line((x+108,y,x+108,y+3),fill='#68a8a2',width=3)
 tx(x,535,'内部双盖重合' if before else '移除内盖，焊接边环',20,'#8a4a31' if before else '#165e56')
tx(677,580,'接缝高度 40.5 m（模型坐标）',18,'#587685')
g.rounded_rectangle((45,639,1254,704),radius=15,fill='#123c50')
tx(70,652,'108 → 96 三角面',27,'white',True);tx(545,655,'5 个方向外表面抽检一致，保留原 UV',22,'#d8ebed')
tx(46,722,'仅离线验证。未改变建筑比例、近中景或游戏内材质。',20,'#456777')
I.save(D/'Irvine-LOD2-consolidated-seam.webp',quality=94)
I.thumbnail((880,680));I.save(D/'proof.png')
