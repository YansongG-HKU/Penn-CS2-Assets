import json,sys,types,collections
from pathlib import Path
import numpy as np
m=types.ModuleType('io_scene_fbx');m.__path__=['/usr/share/blender/scripts/addons_core/io_scene_fbx'];sys.modules[m.__name__]=m
from io_scene_fbx import parse_fbx
one=lambda n,key:next(q for q in n.elems if q.id==key)
def prop(n,key):return one(n,key).props[0]
def read(p):
 r,_=parse_fbx.parse(str(p));g=one(one(r,b'Objects'),b'Geometry')
 u=one(g,b'LayerElementUV')
 x=np.asarray(prop(g,b'Vertices')).reshape(-1,3)
 a=np.asarray(prop(g,b'PolygonVertexIndex'),dtype=np.int32).reshape(-1,3);a[:,2]=-1-a[:,2]
 uv=np.asarray(prop(u,b'UV')).reshape(-1,2)
 ix=np.asarray(prop(u,b'UVIndex'),dtype=np.int32).reshape(-1,3)
 return x,a,uv,ix
if __name__=='__main__':
 d=Path(__file__).resolve().parent
 R={}
 for f in (d/'extracted-final/IrvineAuditorium').glob('*.fbx'):
  x,a,u,ix=read(f); print(f.name,len(a),len(x))
  if 'LOD2' not in f.name:continue
  for j,v in enumerate(a):
   xx=x[v]
   if xx[:,1].max()<28:continue
   cross=np.cross(xx[1]-xx[0],xx[2]-xx[0]); norm=cross/np.linalg.norm(cross)
   print(j, np.round(xx,2).tolist(),np.round(norm,4).tolist(), 'UV',np.round(u[ix[j]],5).tolist())
