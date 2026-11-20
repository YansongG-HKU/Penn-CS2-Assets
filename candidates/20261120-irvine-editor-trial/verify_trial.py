"""Reimport the exact unzipped Irvine payload and render base-color LOD comparisons."""
from pathlib import Path
import collections,json,sys,math
import bpy
from mathutils import Vector
asset,renders,report=(Path(x).resolve() for x in sys.argv[sys.argv.index('--')+1:])
stem='NA_IrvineAuditorium_7x7'
expected={'':19196,'_LOD1':16088,'_LOD2':96,'_Win':518,'_LOD1_Win':518}
data={}
renders.mkdir()
def pull(suffix):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    p=asset/(stem+suffix+'.fbx')
    bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False)
    ob,=[o for o in bpy.context.scene.objects if o.type=='MESH']
    m=ob.data;m.calc_loop_triangles()
    if not m.uv_layers.active or len(m.loop_triangles)!=expected[suffix]:raise ValueError('Mesh/UV unexpected')
    coords=[ob.matrix_world@v.co for v in m.vertices]
    if not all(math.isfinite(c) for p in coords for c in p):raise ValueError('Nonfinite geometry')
    if any((coords[t.vertices[1]]-coords[t.vertices[0]]).cross(coords[t.vertices[2]]-coords[t.vertices[0]]).length_squared<=1e-18 for t in m.loop_triangles):
        raise ValueError('Degenerate geometry')
    if suffix=='_LOD2':
        E=collections.defaultdict(list)
        for poly in m.polygons:
            f=list(poly.vertices)
            for x,y in zip(f,f[1:]+f[:1]):E[tuple(sorted((x,y)))].append((x,y))
        if len(E)!=144 or any(len(x)!=2 or x[0]!=x[1][::-1] for x in E.values()):raise ValueError('Open far shell')
    if suffix.endswith('_Win') and len(m.materials):raise ValueError('Unexpected window preview binding')
    bbox=[[op(t[k] for t in coords) for k in range(3)] for op in (min,max)]
    imgs={}
    for im in bpy.data.images:
        if im.source!='FILE':continue
        f=Path(bpy.path.abspath(im.filepath)).resolve()
        if f.parent!=asset or not f.is_file():raise ValueError('Unexpected image resolve path')
        im.reload();_=im.pixels[0];imgs[f.name]=list(im.size)
    d=(1024 if suffix=='_LOD2' else 4096)
    expected_imgs={f'{stem}{suffix if suffix=="_LOD2" else ""}_{n}.png' for n in ('BaseColor','Normal','Emissive')} if suffix in ('','_LOD1','_LOD2') else set()
    if set(imgs)!=expected_imgs or any(v!=[d,d] for v in imgs.values()):raise ValueError('Unexpected exact image inventory')
    data[p.name]={'triangles':len(m.loop_triangles),'bounds_m':bbox,'images':imgs}
    return ob,bbox

def render(o,stem_suffix):
    sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU'
    sc.cycles.samples=4;sc.cycles.use_denoising=False
    sc.render.threads_mode='FIXED';sc.render.threads=2
    sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
    sc.render.resolution_x=640;sc.render.resolution_y=430;sc.render.resolution_percentage=100
    sc.view_settings.view_transform='Standard'
    mat=bpy.data.materials.new('neutral_base_color_comparison');mat.use_nodes=True
    nodes=mat.node_tree.nodes;nodes.clear();t=nodes.new('ShaderNodeTexImage')
    t.image=next(i for i in bpy.data.images if i.filepath.endswith('_BaseColor.png'))
    e=nodes.new('ShaderNodeEmission');o2=nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(t.outputs['Color'],e.inputs[0]);mat.node_tree.links.new(e.outputs[0],o2.inputs[0])
    o.data.materials.clear();o.data.materials.append(mat)
    c=bpy.data.cameras.new('comparison');c.type='ORTHO';c.ortho_scale=108;c.clip_end=1000
    cam=bpy.data.objects.new('comparison',c);sc.collection.objects.link(cam);sc.camera=cam
    aim=Vector((0,0,20))
    for key,pos in {'front':(58,-127,49),'aerial':(51,-73,113)}.items():
        c.ortho_scale=109 if key=='aerial' else 92
        cam.location=pos;cam.rotation_euler=(aim-cam.location).to_track_quat('-Z','Y').to_euler()
        sc.render.filepath=str(renders/f'{stem_suffix}-{key}.png')
        bpy.ops.render.render(write_still=True)

for suffix in expected:
    ob,bbox=pull(suffix)
    if suffix in ('','_LOD1','_LOD2'):render(ob,suffix[1:] or 'LOD0')
bpy.ops.wm.read_factory_settings(use_empty=True)
decoded={}
for f in sorted(asset.glob('*.png')):
    im=bpy.data.images.load(str(f),check_existing=False);_=im.pixels[0]
    size=1024 if '_LOD2_' in f.name else 4096
    if list(im.size)!=[size,size]:raise ValueError('PNG dimensions unexpected')
    decoded[f.name]=list(im.size)
    bpy.data.images.remove(im)
if len(decoded)!=10:raise ValueError('Missing packaged PNG file')
sasset=json.loads((asset/'settings.json').read_text())['sharedAssets']
if len(sasset)!=5 or not all((asset/v).is_file() and not (asset/k).exists() and '_LOD1_' in k for k,v in sasset.items()):
    raise ValueError('LOD1 texture alias broken')
if list(asset.glob('*_Gls.fbx')):raise ValueError('Empty glass placeholders accidentally packaged')
report.write_text(json.dumps({'separate_FBX':data,'all_PNGs_decoded':decoded,
 'scope':'Offline package, base-color-only body renders, independent window import not combined shader or Editor test'},indent=2)+'\n')
print('IRVINE_TRIAL_PACKAGE_READBACK_PASS',len(data),len(decoded))
