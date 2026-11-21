from pathlib import Path
import sys,collections,json
D=Path(__file__).parent
BASE=next(p for p in (D.parent,D.parent/'20261121-vanpelt-survey-roof') if (p/'roof_shell_core.py').exists())
sys.path.insert(0,str(BASE))
from roof_shell_core import *
from point_diagnostics import a,X,Y,Z,m,source,first,points,xy_box
from scipy.ndimage import label,binary_closing,binary_fill_holes
from osgeo import gdal
out=Path(__file__).parent/'deliver';out.mkdir(exist_ok=True)
held=np.isin(source,[19,20]); use=first&(X>9.8)&(X<58.2)&(Y>-13.5)&(Y<12.95)
BX=np.arange(9.0,59.01,.50);BY=np.arange(-14.0,14.01,.50)
def counts(sel):return np.histogram2d(X[sel],Y[sel],bins=[BX,BY])[0]
den=counts(use&~held)
dom=attic.Buffer(-.22).Difference(east_high_roof.Buffer(.20))
def prep_band(lo,hi):
 z=counts(use&~held&(Z>=lo)&(Z<=hi))
 s=label((z>=3)&(z>=.53*den))[0]; ns=np.bincount(s.ravel())[1:]
 polys=[]
 for index in list(ns.argsort()[::-1][:9]):
  if ns[index]<14:continue
  ok=(s==index+1)
  ok=binary_fill_holes(binary_closing(ok,structure=np.ones((3,3))))|ok
  # GDAL memory raster in the same N-up metre frame, single connected label and tiny rings ignored.
  ds=gdal.GetDriverByName('MEM').Create('',len(BX)-1,len(BY)-1,1,gdal.GDT_Byte)
  ds.SetGeoTransform([BX[0],.5,0,BY[-1],0,-.5]); raster=ds.GetRasterBand(1)
  raster.WriteArray(ok.T[::-1].astype('uint8'))
  vs=ogr.GetDriverByName('Memory').CreateDataSource('p')
  ly=vs.CreateLayer('components',geom_type=ogr.wkbPolygon)
  gdal.Polygonize(raster,raster,ly,-1,[])
  for ft in ly:
   p=ft.GetGeometryRef().Clone()
   if not p.IsValid():p=p.Buffer(0)
   for q in geom_polys(p.Intersection(dom).SimplifyPreserveTopology(.38)):
    if q.GetArea()<4.:continue
    outer, rings=oriented(q); r=rings[0]
    sel,D2=inside_d(r,m);start=sel.copy()
    for line in rings[1:]:
     hit,wd=inside_d(line,m);sel&=~hit;D2=np.minimum(D2,wd)
    inside=sel&first&(D2>.20**2)
    tt=inside&(Z>=lo)&(Z<=hi)
    v=tt&~held; w=tt&held; alltest=inside&held
    if sum(v)<40 or sum(w)<25 or sum(w)/sum(alltest)<.67:continue
    h=round(float(np.median(Z[v])),2)
    qa=lambda z:[float(k) for k in np.quantile(z,[.5,.9,.95])]
    receipt=dict(area_m2=outer.GetArea(), envelope=list(outer.GetEnvelope()), z_band_m=[lo,hi],fit_n=int(sum(v)),held_n=int(sum(w)),held_all_n=int(sum(alltest)),
      fitted_height_navd88=h,in_band_p50_p90_p95=qa(abs(Z[w]-h)),held_all_abs_error_p50_p90_p95=qa(abs(Z[alltest]-h)),
      baseline_same_held_abs_error_p50_p90_p95=qa(abs(Z[alltest]-44.49)),
      planar_rings_local_m=[z.tolist() for z in rings])
    polys.append((outer,h,receipt))
 return polys
if __name__=='__main__':
 patches=[]
 for lo,hi in [(46.31,46.88),(47.91,48.36)]:
  for p,h,q in prep_band(lo,hi):
   patches.append(q); print('patch',np.round(q['envelope'],3).tolist(),round(q['area_m2'],2),'height',h,'train,held',q['fit_n'],q['held_n'],q['held_all_n'],'unscreened',np.round(q['held_all_abs_error_p50_p90_p95'],3))
 (out/'east-segments-probe.json').write_text(json.dumps(patches,indent=2)+'\n')
