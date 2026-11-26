"""Read georegistered pavement samples, not door sills, from NOAA 2022 DTM."""
from osgeo import gdal
from pyproj import Transformer
from pathlib import Path
from sys import argv
import hashlib,json,numpy as np
inp,out=map(Path,argv[1:]);gdal.UseExceptions()
g=gdal.Open(str(inp))
if g.GetGeoTransform()!=(2684610.0,3.0,0.0,236341.0,0.0,-3.0):raise ValueError('Unexpected crop grid')
b=g.GetRasterBand(1);xyz=Transformer.from_crs(26918,6565,always_xy=True)
lonlat=Transformer.from_crs(26918,4326,always_xy=True)
positions={'stair_foot_walk':(514,545,True),'southern_walk':(516,565,True),
           'east_paved_approach':(682,554,True),
           'southeast_access_direction_approx':(653,531,False),
           'stair_top_building_edge_rejected':(518,519,False),
           'stair_mid_interpolation_check':(516,528,False)}
patch={}
for key,(x,y,use) in positions.items():
    q=(483323+(x+.5)*.25,4422620-(y+.5)*.25)
    e,n=xyz.transform(*q)
    col,row=int((e-2684610)/3),int((236341-n)/3)
    data=b.ReadAsArray(col-1,row-1,3,3)
    if data.shape!=(3,3) or not np.all(np.isfinite(data)&(data!=b.GetNoDataValue())):raise ValueError('Incomplete ground data')
    r=np.percentile(data,[0,10,50,90,100])
    patch[key]={'use_as_paved_approach_control':use,'ortho_pixel_xy':[x,y],'utm18_EPSG26918_m':q,
                'lonlat':lonlat.transform(*q),'state_plane_EPSG6565_ft':[e,n],
                'center_ft':float(data[1,1]),'samples':9,'percentiles_min_p10_p50_p90_max_ft':r.tolist(),'median_m':float(r[2])*1200/3937}
out.write_text(json.dumps({'asset':'Van Pelt–Dietrich Library Center / BIN 1386251',
    'dem':'NOAA 2022 Philadelphia ground-only, EPSG:6565 + NAVD88 EPSG:6360, U.S. survey ft',
    'ortho':'PASDA PhiladelphiaImagery2025 export bbox EPSG26918 483323,4422400,483554,4422620 size 924,880',
    'crop_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),'patches':patch,
    'controlled_approaches_height_diff_m':patch['stair_foot_walk']['median_m']-patch['east_paved_approach']['median_m'],
    'notes':'3 ft grid. Neither doorway sill nor roof is measured; positions are matched visually on dated orthophoto.'},ensure_ascii=False,indent=2)+chr(10))
print([(k,round(v['median_m'],3)) for k,v in patch.items()])
