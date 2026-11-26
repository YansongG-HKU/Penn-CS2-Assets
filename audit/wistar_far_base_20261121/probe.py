import types,sys,collections,json
m=types.ModuleType('io_scene_fbx');m.__path__=['/usr/share/blender/scripts/addons_core/io_scene_fbx'];sys.modules[m.__name__]=m
from io_scene_fbx import parse_fbx
from pathlib import Path
def one(e,k):
 a=[x for x in e.elems if x.id==k];assert len(a)==1,(k,len(a));return a[0]
def val(e,k):return one(e,k).props[0]
def read(p):
 r,z=parse_fbx.parse(str(p));obs=one(r,b'Objects')
 g,=[x for x in obs.elems if x.id==b'Geometry' and x.props[2]==b'Mesh']
 P,I=map(lambda k:val(g,k),(b'Vertices',b'PolygonVertexIndex'));v=list(zip(*[iter(P)]*3));f=[];row=[]
 for i in I:
  row.append(i if i>=0 else -i-1)
  if i<0:f.append(row);row=[]
 return r,z,g,v,f
if __name__=='__main__':
 r,z,g,v,f=read(Path(sys.argv[1]))
 print(z,len(v),len(f),[(x.id,[y.id for y in x.elems]) for x in g.elems if x.id.startswith(b'Layer')]);print(f[584],f[1224])
 # List any full triangle eating into the prism, and any triangle owning adjacent vertex indices.
 bb=[(23.5999,23.7601),(24.2749,24.5251),(.5999,10.8001)]
 # Raw FBX may have a rotated coordinate system; derive bounds from target indexed positions.
 vv=[v[j] for k in [582,583,584,585,1222,1223,1224,1225] for j in f[k]]
 bb=[(a-.00005,b+.00005) for a,b in zip(map(min,zip(*vv)),map(max,zip(*vv)))];print(bb)
 for i,row in enumerate(f):
  q=[v[j] for j in row]
  pos=[j for j in row if all(a<=k<=b for (a,b),k in zip(bb,v[j]))]
  if pos:print(i,len(pos),row,q)
