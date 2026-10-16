import os,json,shutil,numpy as np
R='/workspace/penn_campus'
HDR="D='{D}'\nSASHM='Iron'\nexec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())\nexec(open('/workspace/penn_campus/_pipe/quad_lib.py').read())\n"
def ar(a,b,s): return [round(float(x),2) for x in np.arange(a,b+0.01,s)]
B={}
# ---- Memorial Tower (OSM way 320602388, 22.1 x 21.6 m) ----
B['QuadMemorialTower']=dict(lot=(3,3),osm='OSM way 320602388: PCA 22.1 x 21.6 m (~267 m2 core)',refs=('Quad_3.jpg','Quad_1.jpg'),
desc='War Memorial Tower (Cope & Stewardson, 1901): gateway tower with three onion-domed towers, red brick with limestone bands/quoins.',
body='''
jblock(-11,11,0,10.6,4,chim=((-8,5.3),(8,5.3)),win_back=ar(-9,9,3.0),dorm_back=(-5,5))
# three towers: centre taller
for (x,w,H,r) in ((-7.2,6.0,26.0,2.7),(7.2,6.0,26.0,2.7),(0,8.4,30.0,3.6)):
    y0,y1=-10.8,0.4
    if x!=0: y0,y1=-9.6,0.4
    boxr(x-w/2,x+w/2,y0,y1,0,0.6,'Granite'); boxr(x-w/2,x+w/2,y0,y1,0.6,H,'Brick')
    for z in np.arange(3.6,H-1,3.4): boxr(x-w/2-0.05,x+w/2+0.05,y0-0.05,y1+0.05,z,z+0.3,'Limestone')
    for (xx,s) in ((x-w/2,1),(x+w/2,-1)):
        for z in np.arange(0.6,H-1.0,1.0): box((xx+s*0.45,y0-0.03,z),(0.9 if int(z)%2==0 else 0.5,0.06,0.5),'Limestone')
    # scalloped stone parapet + merlons
    boxr(x-w/2-0.3,x+w/2+0.3,y0-0.3,y1+0.3,H,H+0.5,'LimeDark')
    for k in range(int(w/1.2)+1):
        xm=x-w/2+k*w/int(w/1.2); box((xm,y0-0.15,H+0.5),(0.5,0.3,0.8),'Limestone'); box((xm,y1+0.15,H+0.5),(0.5,0.3,0.8),'Limestone')
    boxr(x-w/2+0.2,x+w/2-0.2,y0+0.2,y1-0.2,H,H+0.9,'Brick')
    onion(x,(y0+y1)/2,H+0.9,r)
    F=frame((x,y0,0),pi)
    for z in np.arange(4.3,H-3.5,3.4):
        if x==0:
            if z<7.5: continue
            window(F,-1.6,z,1.5,2.1,None,0.1,'Limestone'); window(F,1.6,z,1.5,2.1,None,0.1,'Limestone')
        else: window(F,0,z,1.5,2.1,None,0.1,'Limestone')
    pass
# gateway arch
Fg=frame((0,-10.8,0),pi); door(Fg,0,3.6,4.4,0.6,None,y=0.1)
paving(12,12)
''',lod2='''boxr(-12,12,-12,12,-0.05,0)
boxr(-11,11,0,10.6,0,15.0); wedge(-11,11,0,5.3,15.0,19.5); wedge(-11,11,10.6,5.3,15.0,19.5)
boxr(-10.2,-4.2,-9.6,0.4,0,26.5); boxr(4.2,10.2,-9.6,0.4,0,26.5); boxr(-4.2,4.2,-10.8,0.4,0,30.5)
cyl(-7.2,-4.6,26.5,3.0,6.0,8); cyl(7.2,-4.6,26.5,3.0,6.0,8); cyl(0,-5.2,30.5,4.0,8.0,8)
''',cams={"lot":[24,24],"day":{"render_01_front34.png":[[-34,-48,14],[0,-3,14],34],"render_02_aerial.png":[[36,-34,48],[0,0,14],32],"render_03_closeup.png":[[-4,-22,3],[0,-11,6],34]},"night":[[-34,-48,14],[0,-3,14],34],"nightlights":[[[0,-20,8],[60,0,0],6000,22]]})
# ---- generic dorm houses ----
def dorm(name,lot,osm,X,Y,nfl,step,dorms,chim,extra='',arch=False,lawn=None):
    wf=ar(-X+2.0,X-2.0,step); ws=ar(-Y+2.5,Y-2.5,3.2)
    a=f"arch_front={wf}" if arch else ""
    body=f'''
ZE=jblock({-X},{X},{-Y},{Y},{nfl},chim={chim},win_front={wf},win_back={wf},win_side={ws},dorm_front={dorms},dorm_back={dorms},{a})
Fe=frame((0,{-Y},0),pi); door(Fe,0,2.0,2.6,0.6,None,y=0.12)
for i in range(3): boxr(-2.0-0.3*i,2.0+0.3*i,{-Y}-0.9-0.9*i,{-Y}-0.0,0,0.6-0.2*i,'Granite')
{extra}
paving({lot[0]*4},{lot[1]*4})
'''
    ZE=0.9+nfl*3.4-0.2; h=0.75*Y
    lod2=f'''boxr({-lot[0]*4},{lot[0]*4},{-lot[1]*4},{lot[1]*4},-0.05,0)
boxr({-X},{X},{-Y},{Y},0,{ZE:.2f}); wedge({-X-0.3},{X+0.3},{-Y-0.5},0,{ZE:.2f},{ZE+h:.2f}); wedge({-X-0.3},{X+0.3},{Y+0.5},0,{ZE:.2f},{ZE+h:.2f})
'''
    L=max(lot)*8
    cams={"lot":[lot[0]*8,lot[1]*8],"day":{"render_01_front34.png":[[-L*0.95,-L*1.15,L*0.32],[0,-2,ZE*0.6],34],"render_02_aerial.png":[[L*0.9,-L*0.8,L*0.95],[0,0,ZE*0.5],32],"render_03_closeup.png":[[-4,-Y-11,3],[0,-Y,5.5],34]},"night":[[-L*0.95,-L*1.15,L*0.32],[0,-2,ZE*0.6],34],"nightlights":[[[0,-Y-8,8],[2*X+20,0,0],6000,22]]}
    B[name]=dict(lot=lot,osm=osm,refs=('Quad_0.jpg','Quad_1.jpg'),desc=f'{name[4:]} House, The Quadrangle (Cope & Stewardson 1895-1912): Jacobean Revival red brick, limestone belts/quoins/coped gables, slate roof, gabled dormers, tall chimneys. {nfl} floors.',body=body,lod2=lod2+extra_l2.get(name,''),cams=cams)
extra_l2={'QuadWard':"cyl(-11.8,-11.6,0,3.0,19.5,8)\n"}
dorm('QuadSpeakman',(7,3),'OSM way 320602397: PCA 51.2 x 17.5 m (~698 m2)',25.6,8.75,4,3.2,(-18,-6,6,18),((-25.6+3.5,0),(0,0),(25.6-3.5,0)))
dorm('QuadMcClelland',(6,3),'OSM way 320602420: PCA 45.6 x 18.8 m (~624 m2); ground-floor arcade lounge',22.8,9.4,3,3.4,(-15,0,15),((-19,0),(19,0)),arch=True)
dorm('QuadWard',(4,4),'OSM way 320602400: PCA 23.6 x 23.3 m (~308 m2); corner house',11.8,11.6,4,3.2,(-5,5),((0,0),),extra='''lathe((-11.8,-11.6,0),[(2.6,0),(2.6,ZE+2.0)],8,'Brick')
lathe((-11.8,-11.6,ZE+2.0),[(2.9,0),(2.9,0.4)],8,'Limestone')
lathe((-11.8,-11.6,ZE+2.4),[(2.9,0),(0.1,5.0)],8,'Roof')''')
dorm('QuadFitler',(3,3),'OSM way 320602405: PCA 16.7 x 16.2 m (~145 m2); typical Quad house unit',8.35,8.1,4,3.2,(-3.5,3.5),((5.5,0),))
# ---- batch: remaining Quad houses (OSM API 0.6 map, PCA) ----
import math
REST=[('QuadMcKean',320602389,33.5,22.6),('QuadBaldwinW',320602390,16.9,16.9),('QuadBaldwinE',320602391,14.9,13.5),('QuadFoerderer',320602392,24.0,12.0),
('QuadFranklin',320602393,24.6,15.8),('QuadLeidy',320602394,23.4,15.7),('QuadBrooks',320602395,23.1,15.8),('QuadClassOf28',320602396,21.4,16.2),
('QuadButcher',320602398,35.5,14.2),('QuadChestnut',320602399,17.5,16.5),('QuadNewYorkAlumni',320602401,19.0,13.0),('QuadCarruth',320602402,14.9,13.3),
('QuadCraig',320602403,20.3,17.5),('QuadBaird',320602404,16.7,16.4),('QuadHopkinson',320602406,16.6,16.3),('QuadSmith',320602407,16.6,15.9),
('QuadLippincott',320602408,17.1,16.1),('QuadMorgan',320602409,25.0,12.1),('QuadWilson',320602410,18.6,14.7),('QuadEFSmith',320602411,23.7,14.1),
('QuadCoxe',320602412,24.1,14.3),('QuadRodney',320602413,24.6,16.3),('QuadBishopWhite',320602414,23.7,14.2),('QuadAshhurst',320602415,22.3,14.3),
('QuadMagee',320602416,27.9,17.4),('QuadCleemann',320602417,28.1,10.7),('QuadMorris',320602418,30.7,19.7),('QuadBodine',320602419,22.5,15.7),('QuadWarwick',320602421,30.0,14.0)]
BATCH=[]
if os.environ.get('QBATCH'):
    for k in list(B): del B[k]
    for (n,i,w,h) in REST:
        X,Y=round(w/2,2),round(h/2,2); lot=(math.ceil((w+1.2)/8),math.ceil((h+6)/8))
        nd=max(1,round(w/10)); dm=[round(-X+X/nd+2*X/nd*k,2) for k in range(nd)] if w>14 else [0.0]
        ch=((round(-X+2.5,2),0.0),(round(X-2.5,2),0.0)) if w>20 else ((round(X-2.2,2),0.0),)
        dorm(n,lot,f'OSM way {i}: PCA {w} x {h} m',X,Y,4,3.2,tuple(dm),ch)
        BATCH.append((n,f"NA_{n}_{lot[0]}x{lot[1]}",i,w,h,f"{lot[0]}x{lot[1]}"))
    for n,b in B.items(): pass

EN={'BRICKCOL':'0.36,0.14,0.09','ROOFCOL':'0.24,0.25,0.28','CARVECOL':'0.55,0.42,0.30','LIMECOL':'0.80,0.76,0.66','SASHM':'Iron','IRONCOL':'0.10,0.10,0.10','IRONMET':'0'}
for n,b in B.items():
    D=f'{R}/{n}'; os.makedirs(D,exist_ok=True); AN=f"NA_{n}_{b['lot'][0]}x{b['lot'][1]}"
    open(D+'/build.py','w').write(HDR.format(D=D)+'# '+b['desc']+'\n# '+b['osm']+'\nfrom numpy import arange\n'+b['body']+'\nfinalize(D)\n')
    open(D+'/lod2.py','w').write(b['lod2']); json.dump(b['cams'],open(D+'/cams.json','w'))
    open(D+'/SOURCES.txt','w').write(f"{AN} - {b['desc']}\nFully procedural. {b['osm']} (c) OpenStreetMap contributors, ODbL. Building split from The Quadrangle (Fisher Hassenfeld/Ware/Riepe college houses).\nRef photos: Wikimedia Commons ({', '.join(b['refs'])} in _audit/ref). No 3D vegetation.\n")
    for i,r in enumerate(b['refs']): shutil.copy(f'{R}/_audit/ref/{r}',f'{R}/_audit/ref/{n}_{i}.jpg')
    env=' '.join(f'{k}={v}' for k,v in EN.items())
    open(f'{R}/_pipe/run_{n}.sh','w').write(f'''#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/penn_campus/_pipe
cd /workspace/penn_campus/{n}
export BD=$PWD AN={AN} {env}
rm -f render.log stage.txt
blender -b -P build.py > build.log 2>&1; echo BUILD $? > stage.txt
blender -b -P $P/bake.py -- 4096 > bake.log 2>&1; echo BAKE $? >> stage.txt
blender -b -P $P/finish.py > finish.log 2>&1; echo FINISH $? >> stage.txt
blender -b $AN.blend -P $P/lodcheck.py > lodcheck.log 2>&1; echo LODCHECK $? >> stage.txt
blender -b $AN.blend -P $P/render.py -- 32 > render.log 2>&1; echo ALLDONE >> render.log; echo RENDER >> stage.txt
'''); os.chmod(f'{R}/_pipe/run_{n}.sh',0o755)
    print(n,AN)
json.dump(BATCH,open('/workspace/penn_campus/_pipe/qbatch.json','w'))
