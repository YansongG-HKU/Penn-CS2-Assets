"""Extract bounded NOAA QGIS EPT point queries, rejecting a silently truncated quadrant."""
from pathlib import Path
import collections,csv,gzip,json,sys
from qgis.core import QgsApplication,QgsPointCloudLayer,QgsGeometry,QgsRectangle,QgsDoubleRange
meta,output,*raw=sys.argv[1:]
x0,y0,x1,y1=map(float,raw)
xc=(x0+x1)*.5;yc=(y0+y1)*.5
q=QgsApplication([],False);q.initQgis();q.setMaxThreads(2)
l=QgsPointCloudLayer(meta,'QGIS local EPT','ept');assert l.isValid(), l.error().message()
p=l.dataProvider();assert p.hasValidIndex()
Z=QgsDoubleRange(-10,120)
fields=('X','Y','Z','Classification','PointSourceId','ReturnNumber','NumberOfReturns','Overlap')
r=[]
with gzip.open(output+'.csv.gz','wt',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
 for a,c in ((x0,xc),(xc,x1)):
  for b,d in ((y0,yc),(yc,y1)):
   s=(a,b,c,d);g=QgsGeometry.fromRect(QgsRectangle(*s))
   points=p.identify(.22,g,Z,40000);assert 0<len(points)<40000,(s,len(points))
   assert all(a-1e-5<=v['X']<=c+1e-5 and b-1e-5<=v['Y']<=d+1e-5 for v in points)
   for v in points: writer.writerow({k:v.get(k) for k in fields})
   print(s,len(points),collections.Counter(v['Classification'] for v in points),flush=True)
   r.append(dict(bbox=s,points_returned=len(points),maximum_requested=40000,classes=dict(collections.Counter(v['Classification'] for v in points))))
Path(output+'.json').write_text(json.dumps({'index_file':Path(meta).name,'query_maxerror_m':.22,'vertical_range_m':[-10,120],
 'compound_srs':'EPSG 6347 horizontal / EPSG 5703 NAVD88 GEOID18 vertical (source SRS; QGIS WKT not assigned a simple code)',
 'queries':r},indent=2)+'\n')
del p,l
q.exitQgis()
