"""Trim the covered intermediate roof and stitch the Van Pelt LOD2 attic."""
import argparse, array, json, sys
from collections import Counter
from pathlib import Path
here=Path(__file__).resolve().parent
sys.path[:0]=[str(here),str(here.parent/"20261120-vanpelt-lod2-weld")]
from repair_vanpelt_lod2 import clone,digest,item,prop,steered_edges,value,parse_fbx,encode_bin
from mathutils import Vector
SOURCE='f7ae9508db53af547c17c2e20f43f521c62ed22b77e03f32ca16b64ca9f3fe7a'
O=(17,16,18,19);I=(22,20,24,26)  # same cyclic order in X Z
TOP=(15,37); BOTTOM=(20,42)
def cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def clip(poly,tri):
    orient=1 if cross(*tri)>0 else -1
    for a,b in zip(tri,tri[1:]+tri[:1]):
        out=[]
        for q,p in zip(poly[-1:]+poly[:-1],poly):
            u,v=orient*cross(a,b,q),orient*cross(a,b,p)
            if (u>=0)!=(v>=0):
                t=u/(u-v);out.append(tuple(x+(y-x)*t for x,y in zip(q,p)))
            if v>=0:out.append(p)
        poly=[]
        for q in out:
            if not poly or q!=poly[-1]:poly.append(q)
        if len(poly)>1 and poly[0]==poly[-1]:poly.pop()
        if len(poly)<3:return []
    return poly
def weights(p,t):
    a,b,c=t;d=cross(a,b,c)
    return cross(p,b,c)/d,cross(a,p,c)/d,cross(a,b,p)/d
def triangles(poly):
    for i in range(1,len(poly)-1):
        t=(poly[0],poly[i],poly[i+1])
        if abs(cross(*t))>1e-9:yield t
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('source','out','report'):p.add_argument(k,type=Path)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    src,out,rep=[getattr(a,k).resolve() for k in ('source','out','report')]
    if out==rep or out.exists() or rep.exists() or digest(src)!=SOURCE:
        raise ValueError('Use fixed input and fresh output/report')
    r,v=parse_fbx.parse(str(src));g=item(item(r,b'Objects'),b'Geometry')
    vv,l,e=[prop(g,k) for k in (b'Vertices',b'PolygonVertexIndex',b'Edges')]
    xyz=[tuple(vv[i:i+3]) for i in range(0,len(vv),3)]
    xy=lambda i:(xyz[i][0],xyz[i][2])
    rows=[tuple(x if x>=0 else -1-x for x in l[i:i+3]) for i in range(0,len(l),3)]
    assert len(xyz)==28 and len(rows)==44
    assert {x for i in TOP for x in rows[i]}==set(O)
    assert {x for i in BOTTOM for x in rows[i]}==set(I)
    assert all(xyz[i][1]==22.0 for i in O+I)
    uv=item(g,b'LayerElementUV'); normal=item(g,b'LayerElementNormal')
    uv_direct=prop(uv,b'UV');uv_index=prop(uv,b'UVIndex')
    normal_direct=prop(normal,b'Normals');normal_index=prop(normal,b'NormalsIndex')
    tan=prop(item(g,b'LayerElementTangent'),b'Tangents')
    bino=prop(item(g,b'LayerElementBinormal'),b'Binormals')
    smooth=prop(item(g,b'LayerElementSmoothing'),b'Smoothing')
    assert prop(normal,b'MappingInformationType')==b'ByPolygonVertex'
    assert len(normal_index)==len(uv_index)==len(l) and len(tan)==len(bino)==3*len(l)
    old_layer=(tuple(uv_direct),tuple(uv_index),tuple(normal_direct),tuple(normal_index),tuple(tan),tuple(bino),tuple(smooth))
    src_corner=lambda f,i:(old_layer[1][f*3+i],old_layer[3][f*3+i],old_layer[4][f*9+3*i:f*9+3*i+3],old_layer[5][f*9+3*i:f*9+3*i+3])
    def xyz_array(a,i,n):return a[i*n:(i+1)*n]
    def interp(f,ws):
        for i,w in enumerate(ws):
            if w>=1-1e-10:return src_corner(f,i)
        c=[src_corner(f,i) for i in range(3)]
        full=[(xyz_array(old_layer[0],u,2),xyz_array(old_layer[2],n,3),t,b) for u,n,t,b in c]
        vals=[tuple(sum(w*x for x,w in zip(z,ws)) for z in zip(*(a[j] for a in full))) for j in range(4)]
        # Keep the source normals as fixed directions at old corners. Normalize only new interpolants.
        U,N,T,B=vals
        nv=Vector(N).normalized(); tv=Vector(T)-nv*Vector(T).dot(nv)
        if tv.length<1e-8:raise ValueError('Unstable tangent interpolation')
        tv.normalize()
        bv=nv.cross(tv).normalized()*(1 if nv.dot(tv.cross(Vector(B)))>0 else -1)
        ui,ni=len(uv_direct)//2,len(normal_direct)//3
        uv_direct.extend(U);normal_direct.extend(nv)
        return ui,ni,tuple(tv),tuple(bv)
    idx={(round(xy(i)[0],9),round(xy(i)[1],9)):i for i in O+I}
    def vertex(p):
        key=tuple(round(q,9) for q in p)
        if key not in idx:
            idx[key]=len(xyz);xyz.append((p[0],22.0,p[1]))
        return idx[key]
    replacement=[]
    area=0
    for i in range(4):
        j=(i+1)%4
        trapezoid=[xy(O[i]),xy(O[j]),xy(I[j]),xy(I[i])]
        for f in TOP:
            cap=[xy(q) for q in rows[f]]
            for t in triangles(clip(trapezoid,cap)):
                if cross(*t)>=0:raise ValueError('Annulus winding failure')
                area+=abs(cross(*t))/2
                replacement.append((tuple(vertex(p) for p in t),tuple(interp(f,weights(p,cap)) for p in t),old_layer[6][f]))
    expected_area=136*34-133*32
    if abs(area-expected_area)>1e-7:raise ValueError((area,expected_area))
    # Split the small roof's vertical sides where the lower cap old UV diagonal meets the inner rim.
    boundary={}
    for a,b in zip(I,I[1:]+I[:1]):
        A,B=xy(a),xy(b); dx,dy=B[0]-A[0],B[1]-A[1]; n2=dx*dx+dy*dy; hits=[]
        for vtx in idx.values():
            if vtx<28:continue
            p=xy(vtx)
            s=((p[0]-A[0])*dx+(p[1]-A[1])*dy)/n2
            if 1e-8<s<1-1e-8 and abs(cross(A,B,p))<1e-6:
                hits.append((s,vtx))
        if hits:
            boundary[(a,b)]=sorted(hits)
            boundary[(b,a)]=sorted((1-s,j) for s,j in hits)
    changed_walls=0; outfaces=[]
    for f,row in enumerate(rows):
        if f in TOP+BOTTOM:continue
        a,b,c=row; hits=[]
        for i in range(3):
            A,B,C=row[i],row[(i+1)%3],row[(i+2)%3]
            if (A,B) in boundary:hits.append((i,A,B,C))
        if not hits:
            outfaces.append((row,tuple(src_corner(f,i) for i in range(3)),old_layer[6][f]))
            continue
        if len(hits)!=1:raise ValueError('Ambiguous wall segment')
        changed_walls+=1
        i,A,B,C=hits[0]; j,k=(i+1)%3,(i+2)%3
        chain=[(A,src_corner(f,i))]
        for s,vtx in boundary[(A,B)]:
            ws=[0.0]*3;ws[i]=1-s;ws[j]=s
            chain.append((vtx,interp(f,ws)))
        chain.append((B,src_corner(f,j)))
        for (First,fa),(Second,sa) in zip(chain,chain[1:]):
            outfaces.append(((First,Second,C),(fa,sa,src_corner(f,k)),old_layer[6][f]))
    if changed_walls!=2:raise ValueError('Expected intersections on two inner rim edges')
    outfaces.extend(replacement)
    newrows=[q[0] for q in outfaces]; edges=steered_edges(newrows)
    if any(len(z)!=2 or z[0][:2]!=z[1][:2][::-1] for z in edges.values()):
        bad={k:q for k,q in edges.items() if len(q)!=2 or q[0][:2]!=q[1][:2][::-1]}
        raise ValueError('Boundary/manifold regression: '+str(bad))
    verts_used={v for rr in newrows for v in rr}
    if verts_used!=set(range(len(xyz))):raise ValueError('Loose vertices remain')
    repl=lambda a,b:a.__setitem__(slice(None),type(a)(a.typecode,b))
    repl(vv,(n for p in xyz for n in p))
    repl(l,(x if k<2 else -1-x for row in newrows for k,x in enumerate(row)))
    repl(e,(rr[0][2] for rr in edges.values()))
    fattrs=[c for _,attrs,_ in outfaces for c in attrs]
    repl(uv_index,(x[0] for x in fattrs));repl(normal_index,(x[1] for x in fattrs))
    repl(tan,(n for x in fattrs for n in x[2]));repl(bino,(n for x in fattrs for n in x[3]))
    repl(smooth,(x[2] for x in outfaces))
    with encode_bin.FBXElem.enable_multithreading_cm():p=clone(r)
    encode_bin.write(str(out),p,v)
    rt,ver=parse_fbx.parse(str(out))
    if ver!=v or value(rt)!=value(r):raise ValueError('Serialization differs')
    report={'old_sha256':SOURCE,'candidate_sha256':digest(out),'old_triangles':len(rows),'candidate_triangles':len(newrows),
            'cap_faces_removed':list(TOP+BOTTOM),'annular_triangles':len(replacement),'wall_faces_split':changed_walls,
            'exposed_ring_area_m2':area,'closed_oriented_edges':len(edges),'new_vertices':len(xyz)-28}
    rep.write_text(json.dumps(report,indent=2)+'\n')
    print('ATTIC_JOIN_PASS',report)
if __name__=='__main__':main()
