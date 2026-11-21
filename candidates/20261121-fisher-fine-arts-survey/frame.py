from pathlib import Path
import numpy as np,json
from osgeo import ogr
D=Path(__file__).resolve().parent
f,=json.loads((D/'city-point.json').read_text())['features']
assert f['attributes']['bin']=='1443619' and f['attributes']['building_name']=='Fisher Fine Arts Library'
rr,=f['geometry']['rings']; X=np.asarray(rr)
assert np.allclose(X[0],X[-1],rtol=0,atol=1e-8)
X=X[:-1]
edge=np.roll(X,-1,axis=0)-X; mag=np.linalg.norm(edge,axis=1)
# Dominant building axis along long near-N/S east curb; calculate perpendicular as local east.
n=edge[np.argmax(mag)];n*=np.sign(n[1]);n/=np.linalg.norm(n);e=n[::-1]*[1.,-1.]
T=np.array([e,n]); O=X.mean(axis=0);P=(X-O)@T.T
O=O+((P.max(axis=0)+P.min(axis=0))*.5)@T
loc=lambda x:(x-O)@T.T
P=loc(X)
def ring(xy):
 r=ogr.Geometry(ogr.wkbLinearRing)
 for x,y in xy:r.AddPoint_2D(x,y)
 r.CloseRings();p=ogr.Geometry(ogr.wkbPolygon);p.AddGeometry(r);return p
assert ring(P).IsValid()
if __name__=='__main__':
 D.joinpath('frame.json').write_text(json.dumps({'origin_epsg6347':O.tolist(),'axes_east_north':T.tolist(),'extent_xy_aligned_m':np.ptp(P,axis=0).tolist(),'ring_xy':P.tolist(),'BIN':'1443619'},indent=2)+'\n')
 print('origin',O,'axes',T,'area',ring(P).GetArea(),'span',np.ptp(P,axis=0), '\npoints',P.round(2))
