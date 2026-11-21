"""Build survey-constrained upper surfaces only, not complete Irvine FBX."""
import sys, json, hashlib, gzip
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np
from scipy.optimize import least_squares
from scipy.spatial import ConvexHull

def fit(A,z):
    return least_squares(lambda q:A@q-z,np.linalg.lstsq(A,z,rcond=None)[0],
                         loss='soft_l1',f_scale=.10).x

def stats(x):
    return np.quantile(np.abs(x),[.50,.90,.95]).round(5).tolist()

def constraint(q):
    return np.c_[q[:,0]-17,q[:,1],np.ones(len(q))]

def clip(poly,coef):
    """Keep A@coef <= 0, splitting exact segment intersections."""
    res=[]
    for x,y in zip(poly,np.roll(poly,-1,axis=0)):
        ax,ay=constraint(np.array([x,y]))@coef
        if ax<=1e-8:
            res.append(x)
        if (ax<-1e-8 and ay>1e-8) or (ax>1e-8 and ay<-1e-8):
            res.append(x+(y-x)*ax/(ax-ay))
    return np.array(res)

def signed_area(p):
    q=np.roll(p,-1,axis=0)
    return (p[:,0]@q[:,1]-p[:,1]@q[:,0])*.5

def inside(xy,ring):
    h=ConvexHull(ring)
    return np.all(xy@h.equations[:,:2].T+h.equations[:,2]<1e-7,axis=1)

csv=Path(sys.argv[1]); ref=json.loads(Path(sys.argv[2]).read_text()); out=Path(sys.argv[3]);out.mkdir(parents=True,exist_ok=True)
with gzip.open(csv,'rt') as f:
    a=np.unique(np.loadtxt(f,delimiter=',',skiprows=1,usecols=range(6)),axis=0)
assert len(a)==205337
C=np.array(ref['plane_meeting_utm_xy']); E=ref['local_east_axis_utm']; N=ref['local_north_axis_utm']
L=(a[:,:2]-C)@np.column_stack([E,N]); z=a[:,2]; valid=(a[:,3]==1)&(a[:,5]==1)
held=np.isin(a[:,4],[19,20]); series={}
text=['# Irvine secondary roof survey surfaces. Open at original evidence cutoffs.',
      '# Same metre basis as existing main roof prototype; Z=0 at provisional 14.4 NAVD88.']
mesh={} ; offset=0
for name,(axis,sign) in {'west':(0,-1),'east':(0,1),'south':(1,-1)}.items():
    rc=L[:,[axis,1-axis]]*np.array([sign,1])
    r,c=rc.T
    A=constraint(rc)
    series[name]={}
    def export(tag,polys,evalz):
        global offset
        v=[]; seen={}; f=[]
        for poly in polys:
            loc=np.zeros_like(poly);loc[:,axis]=poly[:,0]*sign;loc[:,1-axis]=poly[:,1]
            if signed_area(loc)<0:
                loc=loc[::-1]; poly=poly[::-1]
            # Centroid fan avoids near-collinear fan roots while preserving every seam vertex.
            loc=np.vstack([loc,loc.mean(axis=0)])
            poly=np.vstack([poly,poly.mean(axis=0)])
            zs=evalz(poly)
            ii=[]
            for (x,y),g in zip(loc,zs):
                key=tuple(np.round([x,y,g-14.4],5))
                if key not in seen:
                    seen[key]=len(v);v.append(key)
                ii.append(seen[key])
            ri=ii[:-1]
            for k in range(len(ri)):
                t=(ii[-1],ri[k],ri[(k+1)%len(ri)])
                tp=np.asarray([v[l] for l in t])
                assert len(set(t))==3
                assert np.linalg.det(np.c_[tp[1,:2]-tp[0,:2],tp[2,:2]-tp[0,:2]])>1e-7
                f.append(t)
        edges=defaultdict(list)
        for q in f:
            for i,j in zip(q,q[1:]+q[:1]):edges[tuple(sorted((i,j)))].append((i,j))
        assert all(len(x)==1 or (len(x)==2 and x[0]==x[1][::-1]) for x in edges.values())
        boundary=[k for k,x in edges.items() if len(x)==1]; n=Counter(j for b in boundary for j in b)
        assert n and set(n.values())=={2}
        graph=defaultdict(list)
        for i,j in boundary:graph[i].append(j);graph[j].append(i)
        visited=set(); stack=[boundary[0][0]]
        while stack:
            u=stack.pop()
            if u not in visited:visited.add(u);stack.extend(graph[u])
        assert len(visited)==len(n) # one open perimeter, no unsoldered ridge cuts
        text.append('o '+name+'_'+tag)
        text.extend('v %.5f %.5f %.5f' % p for p in v)
        text.extend('f %d %d %d' % tuple(j+offset+1 for j in f0) for f0 in f)
        offset+=len(v)
        mesh[name+'_'+tag]={'vertices':len(v),'triangles':len(f),'perimeter_edges':len(boundary),
         'interior_edges':len(edges)-len(boundary),'plan_area_m2':float(sum(abs(signed_area(k)) for k in polys))}
    k=valid&(r>9.40)&(r<14.0)&(abs(c)<6.6)
    clean=k&(z>42.19)&(z<42.78)
    def deck_m(q):return np.c_[q[:,0]-11.7,abs(q[:,1]),np.ones(len(q))]
    deck=fit(deck_m(rc[clean&~held]),z[clean&~held])
    dee=lambda q:deck_m(q)@deck
    zcheck=dee(rc[k&held])-z[k&held]
    clean_zcheck=dee(rc[clean&held])-z[clean&held]
    assert abs(np.median(zcheck))<.12 and np.mean(abs(zcheck)<.25)>.86
    polys=[np.array([[9.4,t],[14.0,t],[14.0,b],[9.4,b]]) for t,b in [(-6.6,0),(0,6.6)]]
    export('flat_deck',polys,dee)
    series[name]['deck']={'model_r_minus11p7_abs_cross_intercept':deck.tolist(),
       'training_n':int((clean&~held).sum()),'withheld_inside_all_first_class1_n':len(zcheck),
       'withheld_all_abs_p50_p90_p95_m':stats(zcheck),'withheld_all_within_25cm':float(np.mean(abs(zcheck)<.25)),
       'withheld_in_band_n':len(clean_zcheck),'withheld_in_band_abs_p50_p90_p95_m':stats(clean_zcheck)}
    specs={'radial_outer_pitch':(r>=18)&(r<22.5)&(abs(c)<.85),
           'left_pitch':(r>=15.95)&(r<=17.5)&(c<-1.3)&(c>-4.15),
           'right_pitch':(r>=15.95)&(r<=17.5)&(c>1.3)&(c<4.15)}
    ps=[]; plane_report={}
    for tag,q in specs.items():
        mask=valid&q&(z>=33)&(z<=43.1)
        train=mask&~held;t=mask&held; v=fit(A[train],z[train]); ps.append(v)
        e=A[t]@v-z[t]
        assert int(t.sum())>=35 and np.median(abs(e))<.18 and np.quantile(abs(e),.9)<.45
        plane_report[tag]={'model_r_minus17_cross_intercept':v.tolist(),'training_n':int(train.sum()),
                           'withheld_n':int(t.sum()),'withheld_abs_p50_p90_p95_m':stats(e)}
    # Many returns between the main slopes are below every previous plane:
    # check two additional diagonal facets in explicit flank windows.
    lower=np.min(A@np.array(ps).T,axis=1)-z
    for side in (-1,1):
        region=valid&(r>=18.5)&(r<22)&(c*side>=1.35)&(c*side<4.8)&(z>32)&(z<41.5)
        train=region&~held&(lower>.65)&(lower<3.2)
        assert sum(train)>40
        p=fit(A[train],z[train])
        tag='diagonal_negative_cross' if side<0 else 'diagonal_positive_cross'
        t=region&held&(lower>.65)&(lower<3.2)
        plane_report[tag]={'model_r_minus17_cross_intercept':p.tolist(),'training_n':int(train.sum()),
                           'withheld_residual_selected_n':int(t.sum()),
                           'withheld_residual_selected_abs_p50_p90_p95_m':stats(A[t]@p-z[t])}
        ps.append(p)
    P=np.array(ps)
    ev=lambda q:np.min(constraint(q)@P.T,axis=1)
    near=valid&(r>=15.85)&(r<=23.7)&(abs(c)<6.2)&(z>=31)&(z<=43.1)
    train=near&~held&(abs(np.min(A@P.T,axis=1)-z)<.25)
    cells=defaultdict(list)
    for xy,sid in zip(rc[train],a[train,4]):
        cells[tuple(np.floor(xy/.45).astype(int))].append((xy,sid))
    pts=np.array([np.mean([x for x,s in q],axis=0) for q in cells.values()
                 if len(q)>=3 and len({s for x,s in q})>=2])
    # Convex cell hull trimmed towards the centre; trim ridge/edge ends instead of guessing eaves.
    hull=pts[ConvexHull(pts).vertices]
    centre=np.mean(hull,axis=0); vec=hull-centre; hull=centre+vec*(1-.35/np.linalg.norm(vec,axis=1))[:,None]
    polys=[]
    for i,p in enumerate(P):
        poly=hull
        for j,q in enumerate(P):
            if i!=j:poly=clip(poly,p-q)
        assert len(poly)>2
        polys.append(poly)
    assert abs(sum(signed_area(q) for q in polys)-signed_area(hull))<1e-5
    # Every triangle is on the minimum of the fitted planes, including exact shared seams.
    export('outer_hip_sample',polys,ev)
    bbox=(r>15.4)&(r<24.1)&(abs(c)<6.6)
    vv=np.flatnonzero(valid&held&bbox); vv=vv[inside(rc[vv],hull)]
    er=ev(rc[vv])-z[vv]; rr=er[(z[vv]>=31)&(z[vv]<43.1)]
    cross=np.linalg.solve(np.c_[P[:3,:2],-np.ones(3)],-P[:3,2])+np.array([17,0,0])
    series[name]['hip']={'plane_fits':plane_report,'meet_radial_cross_navd88_m':cross.tolist(),
       'train_cell_count':len(pts),'hold_all_first_class1_n':len(er),'hold_all_abs_p50_p90_p95_m':stats(er),
       'hold_all_within_0p5m':float(np.mean(abs(er)<.5)),
       'hold_z_range_n':len(rr),'hold_z_range_abs_p50_p90_p95_m':stats(rr),
       'footprint_local_radial_cross_m':hull.tolist()}
    print('combined check',name,stats(er),np.mean(abs(er)<.5),file=sys.stderr)
    assert np.median(abs(er))<.11 and np.mean(abs(er)<.5)>.98
obj=out/'Irvine-secondary-roof-surfaces.obj';obj.write_text('\n'.join(text)+'\n')
report={'status':'measured partial surface only; no importer or published asset',
        'source':'NOAA 2022 EPT 9848 / EPSG:6347, NAVD88 GEOID18 m',
        'source_csv_gz_sha256':hashlib.sha256(csv.read_bytes()).hexdigest(),
        'crop_xy_epsg6347_m':[483481,4422287,483550,4422356],
        'analysis_distinct_points':len(a),'held_whole_point_source_ids':[19,20],
        'utm_origin':C.tolist(),'E_axis_utm':E,'N_axis_utm':N,'reference_zero_navd88_m':14.4,
        'surfaces':series,'mesh':mesh,'obj_sha256':hashlib.sha256(obj.read_bytes()).hexdigest()}
(out/'secondary-roof-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({n:{'deck_hold':q['deck']['withheld_all_abs_p50_p90_p95_m'],'hip_hold':q['hip']['hold_all_abs_p50_p90_p95_m'],'hip_within_half':q['hip']['hold_all_within_0p5m'],'hip_meet':q['hip']['meet_radial_cross_navd88_m']} for n,q in series.items()},indent=1))
print(mesh)

