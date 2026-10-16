D='/workspace/penn_campus/HoustonHall'
SASHM='Iron'
exec(open('/workspace/penn_campus/_pipe/geo_lib.py').read())
# Houston Hall (Hays & Medary / Frank Miles Day, 1894-96; McGoodwin 1936; VSBA 2000). OSM way 51469194: PCA 84.0 x 37.3 m.
# Collegiate (Tudor) Gothic, grey schist with buff trim, slate gables; 4 floors. Front (Spruce St) = -Y. Lot 11x5 (88x40).
LX,LY=44.0,20.0
def walls(x0,x1,y0,y1,ze):
    boxr(x0-0.25,x1+0.25,y0-0.25,y1+0.25,0,0.8,'Granite'); boxr(x0,x1,y0,y1,0,ze,'Rustic')
    for (a,b) in ((0.8,1.1),(ze-0.5,ze)): boxr(x0-0.04,x1+0.04,y0-0.04,y1+0.04,a,b,'LimeDark')
def groof(x0,x1,y0,y1,ze,h,axis):
    if axis=='Y':
        xc=(x0+x1)/2; prism([(x0,ze),(x1,ze),(xc,ze+h)],y0-0.05,y1+0.05,'Rustic')
        prism([(x0-0.5,ze-0.15),(x1+0.5,ze-0.15),(xc,ze+h+0.4)],y0+0.05,y1-0.05,'Roof')
        boxr(xc-0.3,xc+0.3,y0-0.12,y0+0.4,ze+h-0.2,ze+h+0.5,'LimeDark')
    else:
        yc=(y0+y1)/2; Rz=Matrix.Rotation(pi/2,4,'Z')
        prism([(y0-0.5,ze-0.15),(y1+0.5,ze-0.15),(yc,ze+h+0.4)],-(x1),-(x0),'Roof',Rz)
# central range (ridge along X)
walls(-26,26,-7,11,11.0); groof(-26,26,-7,11,11.0,6.0,'X')
# end gabled wings projecting to the street (ridge along Y)
for (x0,x1) in ((-42,-26),(26,42)):
    walls(x0,x1,-14,15,11.5); groof(x0,x1,-14,15,11.5,9.5,'Y')
    # gable-end on rear too
    xc=(x0+x1)/2
# central entrance bay with shaped gable
walls(-4.5,4.5,-9.5,-7,12.8); prism([(-4.5,12.8),(4.5,12.8),(0,15.2)],-9.55,-7,'Rustic'); boxr(-0.4,0.4,-9.7,-9.3,14.9,15.6,'LimeDark')
# chimneys
for x in (-20,20): boxr(x-0.9,x+0.9,1.0,2.8,14,19.5,'Rustic'); boxr(x-1.05,x+1.05,0.85,2.95,19.5,19.8,'LimeDark')
# facades
Ff=frame((0,-7,0),pi); Fb=frame((0,11,0),0); Fe=frame((0,-9.5,0),pi)
for x in (-22,-17,-12,12,17,22):
    window(Ff,x,1.6,2.4,2.1,None,0.1,'LimeDark'); window(Ff,x,5.2,2.4,2.2,None,0,'LimeDark'); window(Ff,x,8.4,2.2,1.8,None,0,'LimeDark')
for x in (-8,8):
    window(Ff,x,1.6,2.4,2.1,None,0.1,'LimeDark'); window(Ff,x,5.2,2.4,2.2,None,0,'LimeDark')
for x in (-22,-16,-10,-4,4,10,16,22):
    window(Fb,x,1.6,2.2,2.1,None,0.1,'LimeDark'); window(Fb,x,5.2,2.2,2.2,None,0,'LimeDark'); window(Fb,x,8.4,2.0,1.8,None,0,'LimeDark')
door(Fe,0,2.0,3.0,1.1,None,y=0.12); window(Fe,0,5.4,2.6,2.2,None,0,'LimeDark'); window(Fe,0,9.0,1.6,1.6,None,0,'LimeDark')
for xc in (-34,34):
    Fw=frame((xc,-14,0),pi); Fwb=frame((xc,15,0),0)
    for F in (Fw,Fwb):
        # two-storey oriel-like bay of mullioned windows + gable window
        boxr(-3.6,3.6,0,1.2,0.8,9.8,'Rustic',F); boxr(-3.8,3.8,0,1.4,9.8,10.2,'LimeDark',F)
        for z,h in ((1.8,2.6),(5.6,2.8)): window(F,0,z,5.2,h,None,1.22,'LimeDark')
        window(F,-5.8,5.6,1.4,2.4,None,0,'LimeDark'); window(F,5.8,5.6,1.4,2.4,None,0,'LimeDark')
        window(F,0,13.5,2.4,2.0,None,0,'LimeDark'); window(F,0,17.0,1.2,1.2,None,0,'LimeDark')
    for xs,ang in ((xc-8 if xc<0 else xc+8,pi/2 if xc<0 else -pi/2),):
        Fs=frame((xs,0.5,0),ang)
        for x in (-10,-5,0,5,10): window(Fs,x,1.6,1.8,2.1,None,0.1,'LimeDark'); window(Fs,x,5.2,1.8,2.2,None,0,'LimeDark'); window(Fs,x,8.6,1.6,1.8,None,0,'LimeDark')
# entrance terrace steps
for i in range(5): boxr(-6+0.3*i,6-0.3*i,-14.5+0.5*i,-9.5,0,0.18*(i+1),'Granite')
# site
boxr(-LX,LX,-LY,LY,-0.05,0,'Paving')
boxr(-25,-6.5,-19,-9.5,0,0.06,'Granite'); boxr(-24.8,-6.7,-18.8,-9.7,0,0.08,'Lawn')
boxr(6.5,25,-19,-9.5,0,0.06,'Granite'); boxr(6.7,24.8,-18.8,-9.7,0,0.08,'Lawn')
finalize(D)
