"""Sample only recognizable exterior paving, not roof, sill or drawing datum."""
import json,sys,statistics
from pathlib import Path
from osgeo import gdal
from pyproj import Transformer
d=Path(__file__).parent
O=json.loads((d/'ortho-2025-full-extent.json').read_text()); e=O['extent']
T=Transformer.from_crs(26918,6565,always_xy=True)
g=gdal.Open(str(d/'irvine-ground-2022.tif'));gt=g.GetGeoTransform(); band=g.GetRasterBand(1)
data={}
for key,(x,y) in {'Spruce sidewalk south of building':(387,518),'34th Street west sidewalk east of building':(512,428),
                  'Upper north service area pavement':(492,174),'West-side exterior paved path':(168,425),
                  'Southeast approach footpath (not threshold)':(483,503)}.items():
 m=e['xmin']+(e['xmax']-e['xmin'])*(x+.5)/O['width']
 n=e['ymax']-(e['ymax']-e['ymin'])*(y+.5)/O['height']
 rx,ry=T.transform(m,n);ix=int((rx-gt[0])/gt[1]);iy=int((ry-gt[3])/gt[5])
 raw=band.ReadAsArray(ix-1,iy-1,3,3).ravel().tolist(); z=[v*(1200/3937) for v in raw if band.GetNoDataValue()!=v]
 assert len(z)==9
 data[key]=dict(orthophoto_pixel=[x,y],utm18_m=[m,n],median_navd88_m=statistics.median(z),range_navd88_m=[min(z),max(z)])
R=dict(source='NOAA 2022 Philadelphia 3-foot bare earth DEM, EPSG:6565 horizontal, US survey feet NAVD88 elevations', samples=data,
 caveat='Paving control only: not door sill, roof, 1926 drawing datum, or exact building base. 3x3 raster unless footpath slopes interior; no terrain or fit edit from this alone.')
(d/'irvine-ground-control.json').write_text(json.dumps(R,indent=2)+'\n');print(json.dumps(R,indent=2))
