"""Independently verify the candidate and compare two render passes."""
import bpy,sys,collections,json,math
from pathlib import Path
from mathutils import Vector
old,new,report,render=(Path(x).resolve() for x in sys.argv[sys.argv.index('--')+1:])
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
    for suffix in ('BaseColor','Normal'):
        q=f.parent/(f.stem+'_'+suffix+'.png')
        im=next(i for i in bpy.data.images if Path(bpy.path.abspath(i.filepath)).resolve()==q)
        _=im.pixels[0];imgs[q.name]=list(im.size)
        if not len(im.pixels)==1024*1024*4:raise ValueError('Texture decode failed')
    return o,faces,imgs,len(edges),len(m.vertices)

def images(o,tag,lit):
    sc=bpy.context.scene
    sc.render.engine='CYCLES'
    sc.cycles.device='CPU';sc.cycles.samples=32 if lit else 4;sc.cycles.use_denoising=False
    sc.render.threads_mode='FIXED';sc.render.threads=2
    sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
    sc.render.resolution_x=640;sc.render.resolution_y=320;sc.render.resolution_percentage=100
    sc.view_settings.view_transform='Standard'
    mat=bpy.data.materials.new('bake_readback_comparison');mat.use_nodes=True
    nodes=mat.node_tree.nodes; nodes.clear()
    tex=nodes.new('ShaderNodeTexImage')
    tex.image=next(i for i in bpy.data.images if Path(i.filepath).name==old.stem+'_BaseColor.png')
    output=nodes.new('ShaderNodeOutputMaterial')
    if not lit:
        emi=nodes.new('ShaderNodeEmission')
        mat.node_tree.links.new(tex.outputs['Color'],emi.inputs['Color'])
        mat.node_tree.links.new(emi.outputs[0],output.inputs['Surface'])
    else:
        pb=nodes.new('ShaderNodeBsdfPrincipled')
        pb.inputs['Roughness'].default_value=0.7
        texn=nodes.new('ShaderNodeTexImage')
        texn.image=next(i for i in bpy.data.images if Path(i.filepath).name==old.stem+'_Normal.png')
        texn.image.colorspace_settings.name='Non-Color'
        normal=nodes.new('ShaderNodeNormalMap')
        mat.node_tree.links.new(tex.outputs['Color'],pb.inputs['Base Color'])
        mat.node_tree.links.new(texn.outputs['Color'],normal.inputs['Color'])
        mat.node_tree.links.new(normal.outputs[0],pb.inputs['Normal'])
        mat.node_tree.links.new(pb.outputs[0],output.inputs['Surface'])
        world=bpy.data.worlds.new('comparison light');sc.world=world;world.use_nodes=True
        world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.55,.55,.55,1)
        world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.55
        sun=bpy.data.lights.new('sun',type='SUN');sun.energy=2.;sun.angle=0
        so=bpy.data.objects.new('sun',sun);sc.collection.objects.link(so)
        so.rotation_euler=(.25,-.5,-.6)
    if not o.data.materials: raise ValueError('Missing FBX material')
    o.data.materials[0]=mat
    sc.cycles.seed=123
    c=bpy.data.cameras.new('cmp_camera');c.type='ORTHO';world=[o.matrix_world@v.co for v in o.data.vertices]
    bounds=[Vector([op(p[j] for p in world) for j in range(3)]) for op in (min,max)]
    aim=Vector((0,0,34)); ext=48
    c.ortho_scale=1.15*ext;c.clip_end=1000
    camera=bpy.data.objects.new('cmp_camera',c);sc.collection.objects.link(camera);sc.camera=camera
    for k,pos in {'front':(1.6,-2.1,.7),'rear':(-1.4,1.9,.66),'aerial':(.25,-.84,2.5)}.items():
        camera.location=aim+ext*Vector(pos);camera.rotation_euler=(aim-camera.location).to_track_quat('-Z','Y').to_euler()
        sc.render.filepath=str(render/(tag+'-'+('lit' if lit else 'base')+'-'+k+'.png'))
        bpy.ops.render.render(write_still=True)


def geometry_stats(o):
    m=o.data; world=[o.matrix_world@x.co for x in m.vertices]
    adj=collections.defaultdict(set)
    for e in m.edges:
        a,b=e.vertices;adj[a].add(b);adj[b].add(a)
    remaining=set(range(len(world))); batches=[]
    while remaining:
        todo=[remaining.pop()];group=todo.copy()
        while todo:
            i=todo.pop()
            for j in adj[i]&remaining:
                remaining.remove(j);todo.append(j);group.append(j)
        batches.append(len(group))
    return {'components':sorted(batches),'bounds':[[op(c[j] for c in world) for j in range(3)] for op in (min,max)]}

render.mkdir()
report_data={}
for filename,tag in ((old,'before'),(new,'after')):
    for lit in (False,True):
        o,faces,imgs,edges,vertices=load(filename)
        tris,edge,vert=len(faces),edges,vertices
        g=geometry_stats(o)
        report_data[tag]={'triangles':tris,'edges_all_degree_two':edges,'vertices':vert,'decoded_textures':imgs,**g}
        images(o,tag,lit)
if report_data['before']['bounds']!=report_data['after']['bounds'] or report_data['before']['decoded_textures']!=report_data['after']['decoded_textures']:
    raise ValueError('Overall bounds or images differ')
if report_data['before']!=report_data['after']:
    raise ValueError('Expected one shell join')
report.write_text(json.dumps(report_data,indent=2)+chr(10))
print('IRVINE_ROOF_CANDIDATE_READBACK_PASS',report_data)
