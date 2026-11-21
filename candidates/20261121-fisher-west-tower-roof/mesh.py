import numpy as np
split_tolerance=.00014
def clean_surfaces(items):
    V=[]; vi={}; F=[]; tags=[]
    def vertex(p):
        k=tuple(np.round(p,5))
        if k in vi:return vi[k]
        vi[k]=len(V);V.append(k);return vi[k]
    for label,*ts in items:
        for vv in ts:
            ff=tuple(map(vertex,vv))
            assert len(set(ff))==3
            F.append(ff);tags.append(label)
    P=np.array(V); new=[]; lab=[]
    # Noding of existing T-junctions only; no averaging, no wrong-plane stitching.
    # Do not split with points below/above true measured edge endpoints.
    for tag,f in zip(tags,F):
        border=[]; split=False
        for i,j in zip(f,f[1:]+f[:1]):
            u=P[i];g=P[j]-u
            rel=P-u;t=(rel@g)/(g@g)
            ds=np.linalg.norm(rel-t[:,None]*g,axis=1)
            c=np.flatnonzero((t>1e-5)&(t<1-1e-5)&(ds<split_tolerance))
            c=sorted(c,key=lambda k:t[k]);border.extend((i,*c))
            split|=bool(c)
        if split:
            ix=vertex(np.mean(P[list(f)],axis=0))
            for i,j in zip(border,border[1:]+border[:1]):
                new.append((ix,i,j));lab.append(tag)
        else:new.append(f);lab.append(tag)
    return np.array(V),new,lab
