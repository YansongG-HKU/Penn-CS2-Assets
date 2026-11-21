from vanpelt_controls import *
points=D/'vanpelt-ground-roofs.csv.gz'
a=np.unique(np.loadtxt(points,delimiter=',',skiprows=1,usecols=range(6)),axis=0)
m=local(a[:,:2]); X,Y=m.T; Z=a[:,2]; source=a[:,4].astype(int); first=(a[:,3]==1)&(a[:,5]==1)
print('n',len(a),'source IDs',dict(collections.Counter(source)),'classification',dict(collections.Counter(a[:,3])))
regions={'west open deck southwest':(-60,-30,-8,-2),'west open deck north':(-62,-30,13,20),'west outer north edge':(-62,-30,23,26),'western connecting roof':(-16,-2,0,8),
 'east lower outer south':(13,58,-19.8,-17.7),'east lower east band':(61,67,-14,9),'east attic south roof':(13,56,-14,-10),'east attic center':(13,54,-4,5),
 'east lower outer north':(11,59,16,19),'south entrance projection':(20.8,26.8,-27.6,-21.9)}
def xy_box(a,b,c,d):return (X>a)&(X<b)&(Y>c)&(Y<d)
def summary(mask):
 hh,ee=np.histogram(Z[mask],bins=np.arange(14,65.001,.10)); idx=np.argsort(hh)[-12:][::-1]
 return [(float(round(ee[i],2)),int(hh[i])) for i in idx if hh[i]]
for n,r in regions.items():
 b=xy_box(*r); print(n, ' -> n',sum(b&first),np.quantile(Z[b&first],[.05,.5,.95]).round(3).tolist(),summary(b&first))
print('ground',summary(a[:,3]==2))
if __name__=='__main__':
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,ax=plt.subplots(figsize=(18,8),layout='constrained')
 v=np.argsort(Z[first]); x=X[first][v];y=Y[first][v];z=Z[first][v]
 im=ax.scatter(x,y,c=z,vmin=17,vmax=53,s=1.5,linewidths=0,cmap='turbo')
 r=np.r_[P,P[:1]];ax.plot(*r.T,color='black',lw=.7);ax.set(xlim=(-76,76),ylim=(-34,34),xticks=np.arange(-75,76,5),yticks=np.arange(-30,31,5),aspect='equal'); ax.grid(alpha=.25)
 ax.set_title('Van Pelt: 2022 NOAA first returns plotted high over low; City footprint and local metre frame')
 fig.colorbar(im,ax=ax,label='NAVD88 m');fig.savefig(D/'vanpelt-lidar-xy.jpg',dpi=120);plt.close(fig)
