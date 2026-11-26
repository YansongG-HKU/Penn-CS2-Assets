"""Weld only pre-verified exact opposing planar caps."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
from io_scene_fbx import parse_fbx, encode_bin

METHODS=dict(zip(b'BCZYILFDRSifdlbc',('add_bool','add_char','add_int8','add_int16','add_int32',
    'add_int64','add_float32','add_float64','add_bytes','add_string','add_int32_array',
    'add_float32_array','add_float64_array','add_int64_array','add_bool_array','add_byte_array')))

def item(n,key):
    xs=[x for x in n.elems if x.id==key]
    if len(xs)!=1:raise ValueError('Unexpected FBX element: '+str(key))
    return xs[0]

def prop(n,key):return item(n,key).props[0]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def clone(n):
    r=encode_bin.FBXElem(n.id)
    for t,p in zip(n.props_type,n.props):getattr(r,METHODS[t])(p)
    r.elems=[clone(c) for c in n.elems]
    return r

def value(n):
    return (n.id,bytes(n.props_type),tuple(n.props),tuple(value(c) for c in n.elems))

def steered_edges(rows):
    out={}
    for i,r in enumerate(rows):
        for k,(a,b) in enumerate(zip(r,r[1:]+r[:1])):
            out.setdefault(tuple(sorted((a,b))),[]).append((a,b,i*3+k))
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path);p.add_argument('output',type=Path);p.add_argument('plans',type=Path)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    args.output.mkdir()
    for name,plan in json.loads(args.plans.read_text()).items():
        if 'McClelland' in name:
            # This structure's exterior is known to require a redesigned mesh.
            continue
        repair(args.directory/name,args.output/name,args.output/(name+'.json'),plan)

def repair(inp,out,report,plan):
    if plan['third_party_intersections']:raise ValueError('Cap integrity not established')
    SOURCE=plan['sha256']; WELD={int(a):b for a,b in plan['exact_weld'].items()}
    REMOVE=set(sum(plan['caps'],[]))
    if out==report or out.exists() or report.exists() or digest(inp)!=SOURCE:
        raise ValueError('Source must be pinned and output/report must be new')
    root,version=parse_fbx.parse(str(inp))
    g=item(item(root,b'Objects'),b'Geometry')
    v,l,e=(prop(g,k) for k in (b'Vertices',b'PolygonVertexIndex',b'Edges'))
    if version!=7400 or len(v)!=3*plan["old_vertices"] or len(l)!=3*plan["old_triangles"] or any((x<0)!=(i%3==2) for i,x in enumerate(l)):
        raise ValueError('Unexpected pinned triangular FBX layout')
    xyz=[tuple(v[i:i+3]) for i in range(0,len(v),3)]
    rows=[tuple(x if x>=0 else -1-x for x in l[i:i+3]) for i in range(0,len(l),3)]
    if not all(xyz[a]==xyz[b] for a,b in WELD.items()):
        raise ValueError('Refuse any positional movement')
    match=lambda f: [WELD.get(i,i) for i in rows[f]]
    def border(cap):
        e=steered_edges([tuple(match(i)) for i in cap])
        return {rows[0][:2] for rows in e.values() if len(rows)==1}
    a,b=map(border,plan['caps'])
    if len(a)!=len(WELD) or a!={(j,i) for i,j in b}:
        raise ValueError('Opposing cap borders do not match')
    kept=[i for i in range(len(rows)) if i not in REMOVE]
    ids=[i for i in range(len(xyz)) if i not in WELD]
    remap={i:j for j,i in enumerate(ids)}
    newrows=[tuple(remap[WELD.get(x,x)] for x in rows[i]) for i in kept]
    newedges=steered_edges(newrows)
    if any(len(x)!=2 or x[0][:2]!=x[1][:2][::-1] for x in newedges.values()):
        raise ValueError('Weld would create a boundary, multiedge or inconsistent winding')
    if len(newedges)!=plan['closed_oriented_edges'] or len(newrows)!=plan['new_triangles']:
        raise ValueError('Closed edge count changed')
    normal=item(g,b'LayerElementNormal')
    ni=prop(normal,b'NormalsIndex')
    if prop(normal,b'MappingInformationType')!=b'ByVertice' or len(ni)!=len(xyz) or prop(normal,b'ReferenceInformationType')!=b'IndexToDirect':
        raise ValueError('Unexpected vertex normal mapping')
    original_ni=tuple(ni)
    item(normal,b'MappingInformationType').props[0]=b'ByPolygonVertex'
    repl=lambda a,b: a.__setitem__(slice(None),type(a)(a.typecode,b))
    repl(ni,(original_ni[j] for i in kept for j in rows[i]))
    repl(v,(n for i in ids for n in xyz[i]))
    repl(l,(x if k<2 else -1-x for r in newrows for k,x in enumerate(r)))
    repl(e,(r[0][2] for r in newedges.values()))
    for layer,key,stride in ((b'LayerElementSmoothing',b'Smoothing',1),(b'LayerElementUV',b'UVIndex',3),
            (b'LayerElementBinormal',b'Binormals',9),(b'LayerElementTangent',b'Tangents',9)):
        arr=prop(item(g,layer),key)
        if len(arr)!=len(rows)*stride:raise ValueError('Unexpected corner/face attribute')
        repl(arr,(val for i in kept for val in arr[i*stride:(i+1)*stride]))
    with encode_bin.FBXElem.enable_multithreading_cm():payload=clone(root)
    encode_bin.write(str(out),payload,version)
    reread,ver=parse_fbx.parse(str(out))
    if ver!=version or value(reread)!=value(root):
        raise ValueError('Serialized FBX differs from planned patch')
    result={'input_sha256':SOURCE,'output_sha256':digest(out),'removed_opposite_cap_faces':sorted(REMOVE),
            'old_triangles':len(rows),'new_triangles':len(newrows),'welded_vertex_count':len(WELD),
            'max_vertical_snap_m':0.0,'new_indexed_edge_incidence':dict(Counter(map(len,newedges.values()))),
            'same_corner_normals_tangents_binormals_and_uv_by_construction':True}
    report.write_text(json.dumps(result,indent=2)+'\n')
    print('CAP_WELD_PASS',result)

if __name__=='__main__':main()
