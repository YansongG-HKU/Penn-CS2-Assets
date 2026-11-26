import ctypes as ct
import numpy as np
from osgeo import ogr
def flat(a):return float(np.sum(a[:,0]*np.roll(a[:,1],-1)-a[:,1]*np.roll(a[:,0],-1))*.5)
L=ct.CDLL('libgeos_c.so.1')
def fun(name,types,re):
    o=getattr(L,name);o.restype=re;o.argtypes=types;return o
ptr=ct.c_void_p; i32=ct.c_int
ctx=fun('GEOS_init_r',[],ptr)()
reader=fun('GEOSWKTReader_create_r',[ptr],ptr)(ctx)
writer=fun('GEOSWKTWriter_create_r',[ptr],ptr)(ctx)
read=fun('GEOSWKTReader_read_r',[ptr,ptr,ct.c_char_p],ptr)
write=fun('GEOSWKTWriter_write_r',[ptr,ptr,ptr],ptr)
free=fun('GEOSFree_r',[ptr,ptr],None)
destroy=fun('GEOSGeom_destroy_r',[ptr,ptr],None)
tr=fun('GEOSConstrainedDelaunayTriangulation_r',[ptr,ptr],ptr)
def tris2(p):
    a=read(ctx,reader,p.ExportToWkt().encode())
    b=tr(ctx,a)
    assert b
    s=write(ctx,writer,b);g=ogr.CreateGeometryFromWkt(ct.string_at(s).decode())
    free(ctx,s);destroy(ctx,b);destroy(ctx,a)
    ans=[]
    for o in g:
        z=np.array(o.GetGeometryRef(0).GetPoints())[:-1,:2]
        assert len(z)==3
        ans.append(z if flat(z)>0 else z[::-1])
    return ans

