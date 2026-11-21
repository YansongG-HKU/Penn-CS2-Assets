"""Weld the two contiguous identical-width Van Pelt LOD2 base sections."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
from io_scene_fbx import parse_fbx, encode_bin

SOURCE='07cbdfa1ef67521cd9b4982cbb813a7f2c94fd5384b95b910ce4399073a321d4'
REMOVE={11,16,35,40}
WELD={16:9,18:11,20:13,22:15}
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
    p.add_argument('input',type=Path);p.add_argument('output',type=Path);p.add_argument('report',type=Path)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    inp,out,report=(q.resolve() for q in (args.input,args.output,args.report))
    if out==report or out.exists() or report.exists() or digest(inp)!=SOURCE:
        raise ValueError('Source must be pinned and output/report must be new')
    root,version=parse_fbx.parse(str(inp))
    g=item(item(root,b'Objects'),b'Geometry')
    v,l,e=(prop(g,k) for k in (b'Vertices',b'PolygonVertexIndex',b'Edges'))
    if version!=7400 or len(v)!=96 or len(l)!=144 or any((x<0)!=(i%3==2) for i,x in enumerate(l)):
        raise ValueError('Unexpected pinned triangular FBX layout')
    xyz=[tuple(v[i:i+3]) for i in range(0,len(v),3)]
    rows=[tuple(x if x>=0 else -1-x for x in l[i:i+3]) for i in range(0,len(l),3)]
    deltas=[abs(xyz[a][1]-xyz[b][1]) for a,b in WELD.items()]
    if not all(xyz[a][0::2]==xyz[b][0::2] for a,b in WELD.items()) or max(deltas)>1e-6:
        raise ValueError('The two equal-width sections do not overlap as expected')
    match=lambda f: [WELD.get(i,i) for i in rows[f]]
    # The two flat caps may use opposite diagonals. Their rectangular borders must
    # match in reverse order; internal diagonals must have degree two within each cap.
    def border(cap):
        e=steered_edges([tuple(match(i)) for i in cap])
        return {rows[0][:2] for rows in e.values() if len(rows)==1}
    lower,upper=border((11,35)),border((16,40))
    if len(lower)!=4 or lower!={(b,a) for a,b in upper}:
        raise ValueError('Not two opposing matched rectangular caps')
    kept=[i for i in range(len(rows)) if i not in REMOVE]
    ids=[i for i in range(len(xyz)) if i not in WELD]
    remap={i:j for j,i in enumerate(ids)}
    newrows=[tuple(remap[WELD.get(x,x)] for x in rows[i]) for i in kept]
    newedges=steered_edges(newrows)
    if any(len(x)!=2 or x[0][:2]!=x[1][:2][::-1] for x in newedges.values()):
        raise ValueError('Weld would create a boundary, multiedge or inconsistent winding')
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
            'max_vertical_snap_m':max(deltas),'new_indexed_edge_incidence':dict(Counter(map(len,newedges.values()))),
            'same_corner_normals_tangents_binormals_and_uv_by_construction':True}
    report.write_text(json.dumps(result,indent=2)+'\n')
    print('VAN_PELT_WELD_PASS',result)

if __name__=='__main__':main()
