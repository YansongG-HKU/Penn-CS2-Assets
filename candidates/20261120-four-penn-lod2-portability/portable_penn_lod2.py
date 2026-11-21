"""Create and independently read back four pinned Penn far-detail FBX candidates."""
import argparse, hashlib, json, shutil, sys
from pathlib import Path
import bpy
from io_scene_fbx import parse_fbx, encode_bin

PINS = {
 'HillCollegeHouse': ('NA_HillCollegeHouse_10x6_LOD2','a78a7ce74162bf5ddb07d05ae1724c13cfeb522fb21e9ad486b8065bd986b1b3',72),
 'IrvineAuditorium': ('NA_IrvineAuditorium_7x7_LOD2','d936739218c7a3e133e63340d76b49ab6a64c2f7cecb711a9797f6d19161757e',108),
 'SteinbergDietrich': ('NA_SteinbergDietrich_16x10_LOD2','9b6b7e409732f275253a3baa6ba37665828aab7b1a6e179bd2ec5368cf3f78c8',72),
 'WistarInstitute': ('NA_WistarInstitute_17x8_LOD2','cf54205617d398522ebdc8067071452b588d65540b84f51a5e778ce34a407eb1',36),
}
PICS = ('BaseColor','ControlMask','Emissive','MaskMap','Normal')
FBXPICS = {'BaseColor','Normal','Emissive'}
PATHFIELDS={b'FileName',b'Filename',b'RelativeFilename'}
METHODS=dict(zip(b'BCZYILFDRSifdlbc',('add_bool','add_char','add_int8','add_int16','add_int32',
 'add_int64','add_float32','add_float64','add_bytes','add_string','add_int32_array',
 'add_float32_array','add_float64_array','add_int64_array','add_bool_array','add_byte_array')))
def digest(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def snapshot(n):
    return n.id,bytes(n.props_type),tuple(n.props),tuple(snapshot(e) for e in n.elems)
def clone(n):
    a=encode_bin.FBXElem(n.id)
    for k,v in zip(n.props_type,n.props):getattr(a,METHODS[k])(v)
    a.elems=[clone(c) for c in n.elems]
    return a
def normalize(node,expected,changes):
    if node.id in PATHFIELDS:
        if len(node.props)!=1 or not isinstance(node.props[0],bytes):raise ValueError('Unexpected FBX path')
        original=node.props[0]; basename=original.replace(b'\\',b'/').rsplit(b'/',1)[-1]
        if basename.decode() not in expected:raise ValueError('Unknown expected map')
        if original!=basename:
            changes.append([original.decode(),basename.decode()])
            node.props[0]=basename
    for c in node.elems:normalize(c,expected,changes)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('reference','output','clean','pins'):p.add_argument('--'+n,required=True,type=Path)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    root,out,clean,pins=(args.reference.resolve(),args.output.resolve(),args.clean.resolve(),args.pins.resolve())
    if any(q.exists() or q.is_relative_to(root) for q in (out,clean)) or out.is_relative_to(clean) or clean.is_relative_to(out):
        raise ValueError('Require two separate fresh directories outside reference')
    inventory=json.loads(pins.read_text())
    expected_pins={f'{b}/textures/{stem}_{c}.png' for b,(stem,_,_) in PINS.items() for c in PICS}
    if set(inventory)!=expected_pins:raise ValueError('Unexpected texture pin set')
    for f,h in inventory.items():
        if digest(root/f)!=h:raise ValueError('Texture SHA-256 mismatch: '+f)
    receipts={}
    for b,(stem,h,n) in PINS.items():
        src=root/b/'fbx/split'/(stem+'.fbx')
        if digest(src)!=h:raise ValueError('FBX SHA-256 mismatch: '+b)
        d=out/b;d.mkdir(parents=True)
        for c in PICS:
            f=stem+'_'+c+'.png';shutil.copyfile(root/b/'textures'/f,d/f)
        r,v=parse_fbx.parse(str(src));changes=[]
        wanted={stem+'_'+c+'.png' for c in FBXPICS}
        normalize(r,wanted,changes)
        if len(changes)!=6 or {z for _,z in changes}!=wanted:raise ValueError('Unexpected paths to normalize: '+str(changes))
        dest=d/src.name
        with encode_bin.FBXElem.enable_multithreading_cm():payload=clone(r)
        encode_bin.write(str(dest),payload,v)
        rt,ver=parse_fbx.parse(str(dest))
        if ver!=v or snapshot(rt)!=snapshot(r):raise ValueError('Non-path FBX data changed: '+b)
        receipts[b]={'original_sha256':h,'new_sha256':digest(dest),'version':v,'edited_paths':changes}
    shutil.copytree(out,clean)
    for b,(stem,h,n) in PINS.items():
        d=clean/b;f=d/(stem+'.fbx')
        if digest(f)!=receipts[b]['new_sha256']:raise ValueError('Clean copy differs')
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.fbx(filepath=str(f),use_image_search=False)
        ob,=[o for o in bpy.context.scene.objects if o.type=='MESH']
        m=ob.data;m.calc_loop_triangles()
        if len(m.loop_triangles)!=n or not m.uv_layers.active:raise ValueError('Geometry or UV not present')
        degenerate=0
        for tri in m.loop_triangles:
            A,B,C=[ob.matrix_world@m.vertices[k].co for k in tri.vertices]
            degenerate+=int((B-A).cross(C-A).length_squared<=1e-18)
        if degenerate:raise ValueError('Degenerate geometry found')
        imported={}
        for im in bpy.data.images:
            if im.source!='FILE':continue
            f=Path(bpy.path.abspath(im.filepath)).resolve()
            if f.parent!=d:raise ValueError('Texture resolved outside of clean copy')
            im.reload();_=im.pixels[0];imported[f.name]=list(im.size)
        if set(imported)!={stem+'_'+c+'.png' for c in FBXPICS}:raise ValueError('Wrong image set imported')
        sidecar={}
        for c in set(PICS)-FBXPICS:
            f=d/(stem+'_'+c+'.png')
            im=bpy.data.images.load(str(f),check_existing=False)
            _=im.pixels[0];sidecar[f.name]=list(im.size)
        if any(s!=[1024,1024] for s in (*imported.values(),*sidecar.values())):raise ValueError('Unexpected texture dimensions')
        receipts[b].update(triangles=n,geometry_degenerate=degenerate,images_fbx=imported,sidecars_decoded=sidecar)
        print('READBACK',b,n,len(imported),len(sidecar))
    manifest={str(f.relative_to(out)):digest(f) for f in sorted(out.rglob('*')) if f.is_file()}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (out/'offline-readback.json').write_text(json.dumps(receipts,indent=2)+'\n')
if __name__=='__main__':main()
