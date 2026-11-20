"""Read only: audit indexed topology and exact geometric triangles from far-mesh FBX."""
import collections,hashlib,json,math,sys
from pathlib import Path
from io_scene_fbx import parse_fbx
d,out=map(Path,sys.argv[sys.argv.index('--')+1:])
def one(o,k):
    x=[n for n in o.elems if n.id==k]
    if len(x)!=1:raise ValueError(k)
    return x[0]
def vec(a,b):return tuple(i-j for i,j in zip(a,b))
def cross(x,y):return (x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0])
def inspect(p):
    r,v=parse_fbx.parse(str(p));g=one(one(r,b'Objects'),b'Geometry')
    v,b=[one(g,k).props[0] for k in (b'Vertices',b'PolygonVertexIndex')]
    V=[tuple(v[i:i+3]) for i in range(0,len(v),3)]
    assert all(math.isfinite(x) for x in v)
    if len(b)%3 or any((x<0)!=(i%3==2) for i,x in enumerate(b)):
        return {'nontriangular':True}
    S=collections.defaultdict(list); E=collections.defaultdict(list)
    zero=[]; adj=collections.defaultdict(set)
    for i in range(0,len(b),3):
        z=list(b[i:i+3]); z[-1]=-1-z[-1]
        c=[V[j] for j in z]
        if sum(x*x for x in cross(vec(c[1],c[0]),vec(c[2],c[0])))<1e-18:zero.append(i//3)
        k=tuple(sorted(c));S[k].append((i//3, int(min((c[j:]+c[:j] for j in range(3)))==sorted(c))))
        for a,bx in zip(z,z[1:]+z[:1]):
            E[tuple(sorted((a,bx)))].append(a<bx);adj[a].add(bx);adj[bx].add(a)
    remaining=set(adj)
    components=[]
    while remaining:
        q=[remaining.pop()];n=0
        while q:
            i=q.pop();n+=1
            new=adj[i]&remaining;q.extend(new);remaining-=new
        components.append(n)
    return {'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'triangle_count':len(b)//3,'vertex_count':len(V),
            'degenerate_triangle_ids':zero,'open_edges':sum(len(x)==1 for x in E.values()),
            'multi_face_edges':sum(len(x)>2 for x in E.values()),'same_winding_edge_count':sum(len(x)==2 and x[0]==x[1] for x in E.values()),
            'exact_same_direction_geometry':[list(i for i,orient in rows) for rows in S.values() if len(rows)>1 and len({orient for i,orient in rows})==1],
            'exact_opposed_geometry':[list(i for i,orient in rows) for rows in S.values() if len({orient for i,orient in rows})>1],
            'component_vertex_counts':sorted(components)}
rows={p.name:inspect(p) for p in sorted(d.glob('*.fbx'))}
out.write_text(json.dumps(rows,indent=2)+'\n')
print('TOPOLOGY',len(rows),{k:{n:row[n] for n in ('degenerate_triangle_ids','open_edges','multi_face_edges','same_winding_edge_count','exact_same_direction_geometry','exact_opposed_geometry') if row[n]} for k,row in rows.items() if any(row.get(n) for n in ('degenerate_triangle_ids','open_edges','multi_face_edges','same_winding_edge_count','exact_same_direction_geometry','exact_opposed_geometry'))})
