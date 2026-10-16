import sys,glob
from PIL import Image
for p in glob.glob(sys.argv[1]+'/NA_*_BaseColor.png')+glob.glob(sys.argv[1]+'/NA_*_Normal.png'):
    im=Image.open(p)
    if im.mode=='RGBA' and im.getchannel('A').getextrema()==(255,255): im.convert('RGB').save(p,optimize=True); print('rgb',p)
