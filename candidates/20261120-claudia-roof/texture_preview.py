"""Render same-camera LOD2 albedo using actual FBX triangles and atlas UVs."""
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roof_geometry import ASSET, file_snapshot, save_image, sha

def sample(path):
    snap = file_snapshot(path)
    matches = [im for im in bpy.data.images if '_LOD2_BaseColor' in im.name]
    assert len(matches) == 1 and list(matches[0].size)==[1024,1024]
    pixels = np.empty(1024*1024*4,dtype=np.float32)
    matches[0].pixels.foreach_get(pixels)
    return snap, pixels.reshape(1024,1024,4)

def view(snap, tex, direction):
    tree=BVHTree.FromPolygons([tuple(v) for v in snap['world']],snap['ids'].tolist(),all_triangles=True)
    outward=Vector(direction).normalized()
    right=Vector((0,0,1)).cross(outward).normalized()
    up=outward.cross(right).normalized()
    light=(outward*.70+up*.60-right*.20).normalized()
    start=Vector((0,0,10.8))+outward*72
    width,height=360,236
    view=np.zeros((height,width,4),dtype=np.float32)
    view[:,:,3]=1
    plane=snap['world'][snap['ids']]
    e,f=plane[:,1]-plane[:,0],plane[:,2]-plane[:,0]
    e2=np.einsum('ij,ij->i',e,e)
    f2=np.einsum('ij,ij->i',f,f)
    ef=np.einsum('ij,ij->i',e,f)
    den=e2*f2-ef*ef
    for y in range(height):
        row=start+up*((height/2-y-.5)*72/width)
        for x in range(width):
            p,n,i,d=tree.ray_cast(row+right*((x+.5-width/2)*72/width),-outward,216)
            if i is None:
                view[y,x,:3]=(.075,.09,.11)
                continue
            v=np.array(p)-plane[i,0]
            ve=v@e[i];vf=v@f[i]
            b=(ve*f2[i]-vf*ef[i])/den[i]
            c=(vf*e2[i]-ve*ef[i])/den[i]
            uv=(1-b-c)*snap['uv'][i,0]+b*snap['uv'][i,1]+c*snap['uv'][i,2]
            u,v=np.clip((uv*1024).astype(int),0,1023)
            view[y,x,:3]=tex[v,u,:3]*(.52+.48*max(0,n.dot(light)))
    return view

def main():
    old,new,report=map(lambda p:Path(p).resolve(),sys.argv[sys.argv.index('--')+1:])
    name=ASSET+'_LOD2.fbx'
    base,original=sample(old/name)
    changed,current=sample(new/name)
    angles=((1,-1,.58),(-1,1,.48),(0,-1,.18))
    im=np.concatenate([np.concatenate([view(s,t,d) for d in angles],axis=1)
                       for s,t in ((base,original),(changed,current))],axis=0)
    save_image(report/'claudia-albedo-same-views.png',im)
    for candidate in new.glob('*.fbx'):
        snap=file_snapshot(candidate)
        assert not snap['zeros']
        if candidate.name != name:
            assert sha(candidate)==sha(old/candidate.name)
    print('Read back full final split package',len(list(new.glob('*.fbx'))),flush=True)

if __name__=='__main__':
    main()
