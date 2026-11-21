"""Locate pairs of coincident opposing horizontal four-corner caps in FBX meshes."""
import collections, hashlib,itertools,json,sys
from pathlib import Path
from io_scene_fbx import parse_fbx

def one(p,k):
    xs=[n for n in p.elems if n.id==k]
    if len(xs)!=1:raise ValueError(str(k))
    return xs[0]
def edge(a,b):return tuple(sorted((a,b)))
def ring(faces):
    e=collections.defaultdict(list)
    for f in faces:
        for a,b in zip(f,f[1:]+f[:1]):e[edge(a,b)].append((a,b))
    return [x[0] for x in e.values() if len(x)==1]
def scan(p):
    r,v=parse_fbx.parse(str(p)); g=one(one(r,b'Objects'),b'Geometry')
    a=one(g,b'Vertices').props[0]; b=one(g,b'PolygonVertexIndex').props[0]
    xyz=[tuple(a[i:i+3]) for i in range(0,len(a),3)]
    if len(b)%3 or any((x<0)!=(i%3==2) for i,x in enumerate(b)):return {'skip':'nontriangular source'}
    faces=[tuple(x if x>=0 else -1-x for x in b[i:i+3]) for i in range(0,len(b),3)]
    hh=collections.defaultdict(list)
    for i,f in enumerate(faces):
        a,b,c=[xyz[j] for j in f]
        if max(a[1],b[1],c[1])-min(a[1],b[1],c[1])>1e-7:continue
        orient=(b[0]-a[0])*(c[2]-a[2])-(b[2]-a[2])*(c[0]-a[0])
        if abs(orient)<1e-8:continue
        hh[(a[1],orient>0)].append(i)
    caps=collections.defaultdict(list)
    for (y,side),ids in hh.items():
        ee=collections.defaultdict(list)
        for i in ids:
            f=faces[i]
            for a,b in zip(f,f[1:]+f[:1]):ee[edge(a,b)].append(i)
        pairs={tuple(sorted(pair)) for pair in ee.values() if len(pair)==2}
        for i,j in sorted(pairs):
            f,h=faces[i],faces[j]; s=set(f+h)
            if len(s)!=4:continue
            px={(xyz[k][0],xyz[k][2]):k for k in s}
            if len(px)!=4 or len({x for x,z in px})!=2 or len({z for x,z in px})!=2:continue
            pp=tuple(sorted(px))
            caps[pp].append((y,side,(i,j),px))
    out=[]
    for r,cs in caps.items():
        for (y,s,i,a),(Y,S,j,b) in itertools.combinations(cs,2):
            if s==S or abs(y-Y)>1e-6 or set(a.values())&set(b.values()):continue
            lo,hi=(a,b) if y<=Y else (b,a)
            wf={lo[p]:hi[p] for p in r}
            f,g=[{tuple(e) for e in ring([faces[k] for k in ids])} for ids in (i,j)]
            if {(wf.get(y,y),wf.get(x,x)) for x,y in f}!={(wf.get(x,x),wf.get(y,y)) for x,y in g}:continue
            out.append({'source_heights':[y,Y],'height_delta_m':abs(y-Y),'caps':[i,j],
                        'weld':wf,'XZ':r})
    return {'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'faces':len(faces),'verts':len(xyz),'pairs':out}
folder,out=sys.argv[sys.argv.index('--')+1:]
results={p.name:scan(p) for p in sorted(Path(folder).glob('*.fbx'))}
Path(out).write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results))
