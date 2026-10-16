# Quad (Cope & Stewardson 1895-1912) Jacobean Revival kit: red brick, limestone belts/quoins/copings, steep slate gables, tall chimneys.
FL=3.4; Z0=0.9
def quoins(x,y,z0,z1,sx,sy):
    k=0; z=z0
    while z+0.6<=z1:
        L=1.0 if k%2==0 else 0.6
        box((x-sx*L/2+sx*0.0,y,z),(L,0.10,0.6),'Limestone',I) if False else None
        box((x+sx*(L/2-0.05),y-sy*0.05,z),(L,0.10,0.6),'Limestone')
        box((x+sx*0.05,y+sy*(L/2-0.05),z),(0.10,L,0.6),'Limestone')
        z+=0.6+0.6; k+=1
def jblock(x0,x1,y0,y1,nfl,roof=True,gab_x=True,chim=(),dorm_front=(),dorm_back=(),win_front=(),win_back=(),win_side=(),arch_front=()):
    ZE=Z0+nfl*FL-0.6+0.4
    boxr(x0,x1,y0,y1,0,Z0-0.3,'Granite'); boxr(x0,x1,y0,y1,Z0-0.3,ZE,'Brick')
    # belt courses (between window rows; never cross glass)
    for f in range(1,nfl):
        z=Z0+f*FL-0.25; boxr(x0-0.04,x1+0.04,y0-0.04,y1+0.04,z,z+0.22,'Limestone')
    boxr(x0-0.25,x1+0.25,y0-0.25,y1+0.25,ZE-0.4,ZE,'LimeDark')
    for (x,sx) in ((x0,1),(x1,-1)):
        for (y,sy) in ((y0,1),(y1,-1)):
            k=0; z=Z0
            while z+0.55<ZE-0.5:
                L=0.9 if k%2==0 else 0.5
                boxr(min(x,x+sx*L),max(x,x+sx*L),y-sy*0.06 if sy>0 else y,y if sy>0 else y+0.06,z,z+0.5,'Limestone') if False else None
                box((x+sx*L/2,y-sy*0.03,z),(L,0.06,0.5),'Limestone'); box((x-sx*0.03,y+sy*L/2,z),(0.06,L,0.5),'Limestone')
                z+=1.0; k+=1
    Ff=frame(((x0+x1)/2,y0,0),pi); Fb=frame(((x0+x1)/2,y1,0),0); cx=(x0+x1)/2
    for f in range(nfl):
        z=Z0+f*FL+0.35
        for x in win_front:
            if f==0 and x in arch_front: archwin(Ff,-(x-cx),z-0.2,2.2,2.5,'Limestone',k=8)
            else: window(Ff,-(x-cx),z,1.9,1.8,None,0.1,'Limestone')
        for x in win_back: window(Fb,x-cx,z,1.7,1.8,None,0.1,'Limestone')
        for y in win_side:
            window(frame((x0,(y0+y1)/2,0),pi/2),-(y-(y0+y1)/2) if False else (y-(y0+y1)/2),z,1.6,1.8,None,0.1,'Limestone')
            window(frame((x1,(y0+y1)/2,0),-pi/2),-(y-(y0+y1)/2),z,1.6,1.8,None,0.1,'Limestone')
    if roof:
        d=(y1-y0)/2; yc=(y0+y1)/2; R=frame((x0-0.4,yc,0),-pi/2)  # local x=-world y... use prism extruded along world x
        Fr=Matrix.Translation((0,yc,0))@Matrix.Rotation(pi/2,4,'Z')
        h=0.75*d
        prism([(-d-0.5,ZE),(d+0.5,ZE),(0.0,ZE+h)],-x1-0.3,-x0+0.3,'Roof',Fr)
        # gable end coping (stone) at both ends
        for (xe,s) in ((x0,-1),(x1,1)):
            prism([(-d-0.15,ZE),(d+0.15,ZE),(0,ZE+h-0.1)],-xe-0.12*s if s<0 else -xe-0.12,-xe+0.12 if s<0 else -xe+0.12,'Brick',Fr) if False else None
            prism([(-d-0.3,ZE),(-d,ZE),(0,ZE+h-0.15),(0,ZE+h+0.25)],-xe-0.35,-xe+0.35,'Limestone',Fr)
            prism([(d,ZE),(d+0.3,ZE),(0,ZE+h+0.25),(0,ZE+h-0.15)],-xe-0.35,-xe+0.35,'Limestone',Fr)
        for (x,side) in [(x,-1) for x in dorm_front]+[(x,1) for x in dorm_back]:
            yw=yc+side*(d-0.3); w=3.0; hd=2.6
            box((x,yw+side*(-0.0),ZE),(w,1.4,hd),'Brick',I) if False else None
            boxr(x-w/2,x+w/2,min(yw,yw-side*2.2),max(yw,yw-side*2.2),ZE-0.4,ZE+hd,'Brick')
            Fd=frame((x,yw,0),pi if side<0 else 0)
            prism([(-w/2-0.25,ZE+hd),(w/2+0.25,ZE+hd),(0,ZE+hd+1.9)],-2.3,0.05,'Limestone',Fd)
            prism([(-w/2+0.1,ZE+hd),(w/2-0.1,ZE+hd),(0,ZE+hd+1.5)],-2.4,0.2,'Brick',Fd)
            window(Fd,0,ZE+0.3,1.5,1.7,None,0.1,'Limestone')
        for (x,y) in chim:
            boxr(x-0.9,x+0.9,y-0.6,y+0.6,ZE-1,ZE+h+2.6,'Brick'); boxr(x-1.05,x+1.05,y-0.75,y+0.75,ZE+h+2.6,ZE+h+2.9,'Limestone')
    return ZE
def onion(x,y,z,r,m='Copper'):
    lathe((x,y,z),[(r,0),(r*1.18,r*0.55),(r*1.05,r*1.1),(r*0.6,r*1.65),(r*0.18,r*2.0),(0.12,r*2.3),(0.05,r*2.9)],16,m)
def paving(LX,LY,lawn=None):
    boxr(-LX,LX,-LY,LY,-0.05,0,'Paving')
    if lawn: boxr(*lawn,0,0.08,'Lawn')
def ar(a,b,s): return [round(float(x),2) for x in np.arange(a,b+0.01,s)]
