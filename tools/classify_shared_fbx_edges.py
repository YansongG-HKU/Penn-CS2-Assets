import bpy, collections, json, math, sys
from pathlib import Path
from itertools import combinations
from mathutils.geometry import area_tri
src,dst=sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=src,use_image_search=False)
def cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def overlap(a,b,n):
    k=max(range(3),key=lambda q:abs(n[q]))
    p=[tuple(v[j] for j in range(3) if j!=k) for v in a]
    q=[tuple(v[j] for j in range(3) if j!=k) for v in b]
    if cross(*q)<0:q=q[::-1]
    for x,y in zip(q,q[1:]+q[:1]):
        out=[]
        for u,v in zip(p[-1:]+p[:-1],p):
            eu,ev=cross(x,y,u),cross(x,y,v)
            if (eu>=0)!=(ev>=0):
                t=eu/(eu-ev);out.append(tuple(i+(j-i)*t for i,j in zip(u,v)))
            if ev>=0:out.append(v)
        p=out
        if len(p)<3:return 0.0
    return abs(sum(cross(p[0],u,v) for u,v in zip(p[1:],p[2:])))/(2*abs(n[k]))
result={}
for obj in bpy.context.scene.objects:
    if obj.type!='MESH':continue
    m=obj.data
    co=[obj.matrix_world@v.co for v in m.vertices]
    edge_faces=collections.defaultdict(list)
    for f in m.polygons:
        for a,b in f.edge_keys:edge_faces[tuple(sorted((a,b)))].append(f)
    modes=collections.Counter(); cases=[]
    for key,faces in edge_faces.items():
        if len(faces)<=2:continue
        flags=set(); overlaps=[]
        for a,b in combinations(faces,2):
            t,u=[[co[i] for i in f.vertices] for f in (a,b)]
            if len(t)!=3 or len(u)!=3:flags.add('non_triangular');continue
            n=(t[1]-t[0]).cross(t[2]-t[0]); m2=(u[1]-u[0]).cross(u[2]-u[0])
            if n.length<1e-10 or m2.length<1e-10:flags.add('degenerate'); continue
            n.normalize();m2.normalize();d=n.dot(m2)
            if abs(d)<1-1e-6 or max(abs(n.dot(x-t[0])) for x in u)>1e-5:continue
            ar=overlap(t,u,n)
            if ar<=1e-6:continue
            coverage=ar/min(area_tri(*t),area_tri(*u))
            flags.add('same_direction_overlap' if d>0 else 'opposed_skin_overlap')
            overlaps.append([a.index,b.index,round(ar,7),round(coverage,6),a.material_index,b.material_index,'same' if d>0 else 'opposed'])
        if not flags:flags.add('no_positive_coplanar_overlap_at_edge')
        tag="+".join(sorted(flags));modes[tag]+=1
        cases.append(dict(edge=list(key),endpoints=[[round(x,6) for x in co[i]] for i in key],faces=[a.index for a in faces],classification=tag,face_pairs=overlaps))
    result[obj.name]=dict(summary=dict(modes),count=len(cases),cases=cases)
print(json.dumps({o:(v['count'],v['summary']) for o,v in result.items()}))
Path(dst).write_text(json.dumps(result,indent=2)+'\n')
