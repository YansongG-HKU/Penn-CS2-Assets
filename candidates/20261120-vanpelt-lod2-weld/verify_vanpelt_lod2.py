"""Independent Blender readback and same-view baked-base-color comparison inputs."""
import bpy,sys,collections,json,math
from pathlib import Path
from mathutils import Vector
old,new,report,render=(Path(x).resolve() for x in sys.argv[sys.argv.index('--')+1:])
remove={11,16,35,40}
def load(f):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=str(f),use_image_search=False)
    o,=[x for x in bpy.context.scene.objects if x.type=='MESH']
    m=o.data
    faces=[]; edges=collections.defaultdict(list)
    for p in m.polygons:
        ids=list(p.vertices)
        if len(ids)!=3:raise ValueError('nontriangular readback')
        coords=[list(o.matrix_world@m.vertices[i].co) for i in ids]
        uv=[list(m.uv_layers.active.data[i].uv) for i in p.loop_indices]
        normals=[list((o.matrix_world.to_3x3()@m.corner_normals[i].vector).normalized()) for i in p.loop_indices]
        if ((Vector(coords[1])-Vector(coords[0])).cross(Vector(coords[2])-Vector(coords[0]))).length<=1e-9:
            raise ValueError('Degenerate face')
        faces.append((coords,uv,normals,p.material_index))
        for a,b in zip(ids,ids[1:]+ids[:1]):
            edges[tuple(sorted((a,b)))].append((a,b))
    if any(len(x)!=2 or x[0]!=x[1][::-1] for x in edges.values()):raise ValueError('Open or misdirected indexed edge')
    imgs={}
    for im in bpy.data.images:
        if im.source=='FILE':
            q=Path(bpy.path.abspath(im.filepath)).resolve()
            if q.parent!=f.parent or not q.is_file():raise ValueError('Missing local texture '+str(q))
            im.reload();_=im.pixels[0];imgs[q.name]=list(im.size)
    expected={f.stem+'_'+n+'.png' for n in ('BaseColor','Normal','Emissive')}
    if set(imgs)!=expected:raise ValueError('Unexpected baked image set')
    return o,faces,imgs,len(edges),len(m.vertices)

def images(o,tag):
    sc=bpy.context.scene
    sc.render.engine='CYCLES'
    sc.cycles.device='CPU';sc.cycles.samples=4;sc.cycles.use_denoising=False
    sc.render.threads_mode='FIXED';sc.render.threads=2
    sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
    sc.render.resolution_x=640;sc.render.resolution_y=320;sc.render.resolution_percentage=100
    sc.view_settings.view_transform='Standard'
    mat=bpy.data.materials.new('bake_readback_comparison');mat.use_nodes=True
    nodes=mat.node_tree.nodes; nodes.clear()
    tex=nodes.new('ShaderNodeTexImage')
    tex.image=next(i for i in bpy.data.images if i.filepath.endswith('BaseColor.png'))
    emi=nodes.new('ShaderNodeEmission');output=nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(tex.outputs['Color'],emi.inputs['Color'])
    mat.node_tree.links.new(emi.outputs[0],output.inputs['Surface'])
    o.data.materials.clear();o.data.materials.append(mat)
    c=bpy.data.cameras.new('cmp_camera');c.type='ORTHO';c.ortho_scale=157;c.clip_end=1000
    camera=bpy.data.objects.new('cmp_camera',c);sc.collection.objects.link(camera);sc.camera=camera
    aim=Vector((0,0,13))
    for k,pos in {'front':(91,-192,56),'rear':(-85,170,64),'aerial':(13,-82,186)}.items():
        camera.location=pos;camera.rotation_euler=(aim-camera.location).to_track_quat('-Z','Y').to_euler()
        sc.render.filepath=str(render/(tag+'-'+k+'.png'))
        bpy.ops.render.render(write_still=True)

o,b,b_img,b_edge,b_v=load(old)
render.mkdir()
images(o,'before')
o,n,n_img,n_edge,n_v=load(new)
if len(b)!=48 or len(n)!=44 or b_img!=n_img:raise ValueError('Unexpected independent readback totals')
delta=[0.0,0.0,0.0]
for f,g in zip([f for i,f in enumerate(b) if i not in remove],n):
    if f[3]!=g[3]:raise ValueError('Material index differs')
    for k in range(3):
        delta[k]=max(delta[k],max(math.dist(a,b) for a,b in zip(f[k],g[k])))
angular=math.degrees(2*math.asin(delta[2]/2))
# File-level loop normals must remain exact (repair script); Blender import may
# recalculate custom normal frames following the weld. Cap readback drift at 0.01°.
if delta[0]>2e-6 or delta[1]!=0 or angular>0.01:
    raise ValueError('Surviving face attributes differ '+str(delta))
images(o,'after')
r={'before':[len(b),b_edge,b_v],'after':[len(n),n_edge,n_v],
   'max_world_position_m_delta':delta[0],'max_UV_delta':delta[1],'max_Blend_corner_normal_delta':delta[2],
   'max_Blender_corner_normal_angle_degrees':angular,
   'before_after_closed_consistently_oriented_indexed_edges':True,'decoded_image_sizes':n_img,
   'scope':'orthographic BaseColor-only Blender comparison; other PBR channels not shaded and no game import'}
report.write_text(json.dumps(r,indent=2)+'\n')
print('VAN_PELT_READBACK_PASS',r)
