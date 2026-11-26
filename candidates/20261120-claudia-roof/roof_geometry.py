"""Restore Claudia Cohen Hall's two matching roof components into its LOD2 FBX."""
import array
from collections import Counter
import json
import os
from pathlib import Path
import sys

import bpy
from io_scene_fbx import encode_bin, parse_fbx
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import numpy as np

sys.path.insert(0, os.environ['CS2_CANDIDATE_TOOLS'])
from portable_readback import encode_node, sha, typed_tree_hash
from glass_uv import overlap

ASSET = 'NA_ClaudiaCohenHall_7x5'
ROOF_BASE = 16.5
PATCH = (464, 565, 656, 733)  # bottom-left origin in the 1024² atlas
DONOR = (647, 634, 668, 655)  # inset from existing slate patch
BANDS = [([(-22.21,22.21),(-14.31,14.31)],22.0),
         ([(-7.31,7.31),(-17.71,-12.79)],23.0)]

def get(root, identifier):
    return next(n for n in root.elems if n.id == identifier)

def file_snapshot(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=str(path),use_image_search=False)
    ob, = (o for o in bpy.data.objects if o.type=='MESH')
    me=ob.data;me.calc_loop_triangles()
    position=np.array([tuple(v.co) for v in me.vertices])
    transform=np.array(ob.matrix_world)
    world=position@transform[:3,:3].T+transform[:3,3]
    loops=np.array([t.loops for t in me.loop_triangles])
    ids=np.array([t.vertices for t in me.loop_triangles])
    uv=np.array([tuple(u.vector) for u in me.uv_layers.active.uv])[loops]
    images={im.name:Path(bpy.path.abspath(im.filepath)).resolve() for im in bpy.data.images if im.source=='FILE'}
    assert all(p.is_file() and p.is_relative_to(path.parent) for p in images.values())
    return {'position':position,'transform':transform,'world':world,'ids':ids,'uv':uv,'images':images,
            'materials':[m.name for m in me.materials], 'zeros':sum(t.area<=1e-10 for t in me.loop_triangles)}

def selected_roofs(snap):
    verts=snap['world'][snap['ids']]
    parts=[]
    for limits,height in BANDS:
        found=[]
        for face in verts:
            if abs(face[:,2].max()-height)>1e-4 or abs(face[:,2].min()-ROOF_BASE)>1e-4:
                continue
            if all(face[:,axis].min()>=a and face[:,axis].max()<=b for axis,(a,b) in enumerate(limits)):
                found.append(face)
        assert len(found)==6,(height,len(found))
        parts.append(found)
    return np.array([f for component in parts for f in component])

def soffit(roof):
    """Close the eaves at the shared source datum without overlapping the cross roof."""
    main, cross = roof[:6], roof[6:]
    main_min, main_max = main.min(axis=(0,1)), main.max(axis=(0,1))
    cross_min, cross_max = cross.min(axis=(0,1)), cross.max(axis=(0,1))
    cross_max[1] = main_min[1]
    triangles = []
    for lo, hi in [(main_min,main_max),(cross_min,cross_max)]:
        z = float(lo[2])
        assert abs(z-ROOF_BASE)<1e-4
        a=(lo[0],lo[1],z); b=(lo[0],hi[1],z); c=(hi[0],hi[1],z); d=(hi[0],lo[1],z)
        triangles.extend(((a,b,c),(a,c,d)))
    return np.array(triangles)

def oriented(corners, places=4):
    keys=[tuple(float(round(x,places)) for x in row) for row in corners]
    return min(tuple(keys[offset:]+keys[:offset]) for offset in range(3))

def chart(verts, face):
    edge=verts[[1,2,0]]-verts
    t=edge[np.argmax(np.linalg.norm(edge,axis=1))].copy()
    t/=np.linalg.norm(t)
    n=np.cross(verts[1]-verts[0],verts[2]-verts[0])
    n/=np.linalg.norm(n)
    b=np.cross(n,t)
    uv=verts@np.column_stack((t,b))
    uv-=uv.min(axis=0)
    uv*=28/max(uv.max(axis=0))
    x,y,_,_=PATCH
    return (uv+np.array([x+(face%4)*48+7,y+(face//4)*42+7]))/1024

def check_unrelated_uv(uv):
    x0,y0,x1,y1=(p/1024 for p in PATCH)
    a,b,c,d=[Vector(v) for v in [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]]
    assert all(overlap([Vector(v) for v in t],[a,b,c]) < 1e-10
               and overlap([Vector(v) for v in t],[a,c,d]) < 1e-10 for t in uv)

def updated_fbx(path, out, old, roof):
    tree, version=parse_fbx.parse(str(path))
    assert version==7500
    geo=get(get(tree,b'Objects'),b'Geometry')
    verts = get(geo,b'Vertices').props[0]
    triangles = get(geo,b'PolygonVertexIndex').props[0]
    raw=np.asarray(triangles).reshape(-1,3).copy()
    raw[:,2]=~raw[:,2]
    assert np.array_equal(raw,old['ids'])
    assert np.allclose(np.asarray(verts).reshape(-1,3),old['position'],atol=1e-5)
    positions=old['world'][raw]
    retain=~np.all(abs(positions[:,:,2]-ROOF_BASE)<1e-4,axis=1)
    assert int((~retain).sum())==4
    check_unrelated_uv(old['uv'][retain])

    axis=old['transform'][:3,:3]
    offset=old['transform'][:3,3]
    roof_local=(roof-offset)@np.linalg.inv(axis).T
    assert np.isfinite(roof_local).all()
    charts = np.array([chart(face,i) for i,face in enumerate(roof)])
    polygons = [[Vector(v) for v in u] for u in charts]
    assert all(overlap(a,b) < 1e-10 for i,a in enumerate(polygons) for b in polygons[i+1:])
    d1,d2=roof_local[:,1]-roof_local[:,0],roof_local[:,2]-roof_local[:,0]
    normal=np.cross(d1,d2)
    normal/=np.linalg.norm(normal,axis=1)[:,None]
    ab,ac=charts[:,1]-charts[:,0],charts[:,2]-charts[:,0]
    det=ab[:,0]*ac[:,1]-ab[:,1]*ac[:,0]
    tangent=(d1*ac[:,1,None]-d2*ab[:,1,None])/det[:,None]
    tangent/=np.linalg.norm(tangent,axis=1)[:,None]
    bitangent=(d2*ab[:,0,None]-d1*ac[:,0,None])/det[:,None]
    bitangent/=np.linalg.norm(bitangent,axis=1)[:,None]
    assert np.all(np.abs(np.sum(tangent*bitangent,axis=1))<1e-5)

    points_start=len(verts)//3
    verts.extend(roof_local.flatten())
    extra=np.arange(points_start,points_start+len(roof)*3).reshape(-1,3)
    changed=np.concatenate([raw[retain],extra])
    encoded=changed.copy();encoded[:,2]=~encoded[:,2]
    triangles[:]=array.array(triangles.typecode,encoded.flatten())
    edges=get(geo,b'Edges').props[0]
    unique={}
    for i,row in enumerate(changed.tolist()):
        for j in range(3):
            unique.setdefault(tuple(sorted((row[j],row[(j+1)%3]))),i*3+j)
    edges[:]=array.array(edges.typecode,unique.values())

    sm=get(get(geo,b'LayerElementSmoothing'),b'Smoothing').props[0]
    sm[:]=array.array(sm.typecode,np.asarray(sm)[retain].tolist()+[0]*len(roof))
    for layer_id,label,added in [(b'LayerElementTangent',b'Tangents',tangent),
                                  (b'LayerElementBinormal',b'Binormals',bitangent)]:
        layer=get(geo,layer_id)
        assert get(layer,b'MappingInformationType').props[0]==b'ByPolygonVertex'
        data=get(layer,label).props[0]
        data[:]=array.array(data.typecode,np.concatenate([np.asarray(data).reshape(-1,3,3)[retain],
                                                         np.repeat(added[:,None,:],3,axis=1)]).flatten())
    n_layer=get(geo,b'LayerElementNormal')
    assert get(n_layer,b'MappingInformationType').props[0]==b'ByVertice'
    n_data=get(n_layer,b'Normals').props[0]
    n_idx=get(n_layer,b'NormalsIndex').props[0]
    assert len(n_idx)==points_start
    for n in normal:
        n_idx.extend([len(n_data)//3]*3)
        n_data.extend(n.tolist())
    u_layer=get(geo,b'LayerElementUV')
    assert get(u_layer,b'MappingInformationType').props[0]==b'ByPolygonVertex'
    uv_data=get(u_layer,b'UV').props[0]
    uv_index=get(u_layer,b'UVIndex').props[0]
    start=len(uv_data)//2
    uv_data.extend(charts.flatten())
    uv_index[:]=array.array(uv_index.typecode,np.asarray(uv_index).reshape(-1,3)[retain].flatten().tolist()+
                                              list(range(start,start+3*len(roof))))
    expected=typed_tree_hash(tree)
    with encode_bin.FBXElem.enable_multithreading_cm():
        compiled=encode_node(tree)
    encode_bin.write(str(out),compiled,version)
    audit, new_version=parse_fbx.parse(str(out))
    assert typed_tree_hash(audit)==expected and new_version==7500
    return positions[retain],old['uv'][retain],charts

def snapshot_model(snap, travel, center, span):
    verts=[tuple(v) for v in snap['world']]
    faces=snap['ids'].tolist()
    tree=BVHTree.FromPolygons(verts,faces,all_triangles=True)
    outward=Vector(travel).normalized()
    right=Vector((0,0,1)).cross(outward).normalized()
    up=outward.cross(right).normalized()
    light=(outward*.66+up*.48-right*.25).normalized()
    start=Vector(center)+outward*span
    width,height=320,210
    rgb=np.zeros((height,width,4),dtype=np.float32)
    for y in range(height):
        row=start+up*((height/2-y-.5)*span/width)
        for x in range(width):
            _p,n,i,_d=tree.ray_cast(row+right*((x+.5-width/2)*span/width),-outward,span*3)
            intensity=.08 if i is None else .33+.55*max(0,n.dot(light))
            rgb[y,x,:]=[intensity*.91,intensity*.96,intensity,1]
    return rgb

def save_image(path, graphic):
    im=bpy.data.images.new('same_camera',graphic.shape[1],graphic.shape[0],alpha=True)
    im.pixels.foreach_set(graphic[::-1].flatten())
    im.filepath_raw=str(path)
    im.file_format='PNG'
    im.save()

def main():
    source, candidate, report=map(lambda x:Path(x).resolve(),sys.argv[sys.argv.index('--')+1:])
    original=file_snapshot(source/(ASSET+'_LOD2.fbx'))
    near=file_snapshot(source/(ASSET+'.fbx'))
    mid=file_snapshot(source/(ASSET+'_LOD1.fbx'))
    roof=selected_roofs(near)
    assert Counter(map(oriented,roof))==Counter(map(oriented,selected_roofs(mid)))
    outer_roof_count=len(roof)
    roof=np.concatenate((roof,soffit(roof)))
    output=candidate/(ASSET+'_LOD2.fbx')
    kept, uv, new_uv=updated_fbx(source/output.name,output,original,roof)
    preserved=np.concatenate([kept,roof])
    preserved_uv=np.concatenate([uv,new_uv])
    after=file_snapshot(output)
    assert not after['zeros'] and original['materials']==after['materials']
    assert set(p.name for p in after['images'].values())==set(p.name for p in original['images'].values())
    assert Counter(oriented(np.concatenate([pos,uv],axis=1)) for pos,uv in zip(preserved,preserved_uv))==Counter(
        oriented(np.concatenate([pos,uv],axis=1)) for pos,uv in zip(after['world'][after['ids']],after['uv']))
    joined=BVHTree.FromPolygons([tuple(v) for v in after['world']],after['ids'].tolist(),all_triangles=True)
    tests=[]
    for a,b,c,d in [(-21.99,21.99,-13.99,13.99),(-6.99,6.99,-17.49,-14.01)]:
        for x in np.linspace(a,b,13):
            for y in np.linspace(c,d,11):
                p,_n,_idx,_d=joined.ray_cast(Vector((x,y,30)),Vector((0,0,-1)),30)
                assert p is not None and p.z>ROOF_BASE,(x,y,p)
                tests.append(round(p.z,5))
    assert abs(after['world'][:,2].max()-23)<1e-4
    angles=((1,-1,.58),(-1,1,.48),(0,-1,.18))
    center=(0,0,10.8);span=72
    graphic=np.concatenate([np.concatenate([snapshot_model(snap,a,center,span) for a in angles],axis=1)
                            for snap in (original,after)],axis=0)
    save_image(report/'claudia-roof-same-views.png',graphic)
    payload={'asset':ASSET,'project':'cross-LOD silhouette only','fbx_version':7500,
             'old_fbx_sha256':sha(source/output.name),'new_fbx_sha256':sha(output),
             'near_fbx_sha256':sha(source/(ASSET+'.fbx')),'mid_fbx_sha256':sha(source/(ASSET+'_LOD1.fbx')),
             'old_triangles':len(original['ids']),'new_triangles':len(after['ids']),
             'old_roof_plate_triangles_removed':4,'new_roof_triangles':outer_roof_count,'soffit_triangles':len(roof)-outer_roof_count,
             'dominant_roof_geometry_from_equal_near_and_mid':True,'preserved_triangles_with_uv_exact_to_1e4':len(kept),
             'old_height_m':float(original['world'][:,2].max()),'new_height_m':float(after['world'][:,2].max()),
             'roof_cover_rays':len(tests),'min_cover_hit_m':min(tests),'max_cover_hit_m':max(tests),
             'shaders_and_texture_paths':sorted(p.name for p in after['images'].values()),
             'new_uv_region_pixel_bottom_left':PATCH,'atlas_slate_donor_region':DONOR}
    (report/'claudia-roof-readback.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps(payload),flush=True)

if __name__=='__main__':
    main()
