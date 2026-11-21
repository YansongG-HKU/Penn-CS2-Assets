import hashlib,json,collections
from pathlib import Path
import numpy as np
from pyproj import Transformer
from osgeo import ogr
D=Path(__file__).parent
src=D/'vanpelt-philadelphia-bin1386251.json'
f,=json.loads(src.read_text())['features']
assert f['attributes']['bin']=='1386251'
r,=f['geometry']['rings']
r=np.array(r); assert np.allclose(r[0],r[-1],rtol=0,atol=1e-9)
T=Transformer.from_crs(26918,6347,always_xy=True)
XY=np.array(T.transform(*r[:-1].T)).T
d=np.roll(XY,-1,axis=0)-XY;l=np.linalg.norm(d,axis=1)
# Parallel EW edges: axis from geometric longest nearly EW line and weighted confirmation.
ew=abs(d[:,0])>4*abs(d[:,1]); ew[:]&=l>8
dd=d[ew]*np.sign(d[ew,0])[:,None]
east=dd.sum(axis=0);east/=np.linalg.norm(east); north=east[::-1]*[-1,1]
axes=np.array([east,north]); o=XY.mean(axis=0)
P=(XY-o)@axes.T; o=o+(.5*(P.min(axis=0)+P.max(axis=0)))@axes
local=lambda a:(a-o)@axes.T
P=local(XY)
def polygon(q):
 s=ogr.Geometry(ogr.wkbLinearRing)
 for x,y in q:s.AddPoint_2D(float(x),float(y))
 s.CloseRings(); p=ogr.Geometry(ogr.wkbPolygon);p.AddGeometry(s);return p
foot=polygon(P)
assert foot.IsValid()
def flat(a):return float(np.sum(a[:,0]*np.roll(a[:,1],-1)-a[:,1]*np.roll(a[:,0],-1))*.5)
print('origin',o,'axes',axes,'span',np.ptp(P,axis=0),'area',foot.GetArea(), 'EW segment count', int(sum(ew)))
print('lengths',np.round(np.sort(l)[-10:],3))
