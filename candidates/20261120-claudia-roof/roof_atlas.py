"""Retile an existing LOD2 slate sample into the former flat-roof UV chart."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, PngImagePlugin

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def build(source, candidate, evidence):
    data = json.loads(evidence.read_text())
    x0,y0,x1,y1 = data['new_uv_region_pixel_bottom_left']
    sx0,sy0,sx1,sy1 = data['atlas_slate_donor_region']
    outputs=[]
    names={'BaseColor','Normal','MaskMap','ControlMask','Emissive'}
    matches={p.stem.rsplit('_',1)[-1]:p for p in source.glob('*_LOD2_*.png')}
    assert set(matches)==names
    for layer, path in sorted(matches.items()):
        with Image.open(path) as old:
            assert old.size==(1024,1024)
            assert old.mode in ('RGB','RGBA')
            old.load()
            baseline=np.array(old)
            donor=baseline[1024-sy1:1024-sy0,sx0:sx1]
            tiled=np.tile(donor,((y1-y0-1)//len(donor)+1,
                                 (x1-x0-1)//donor.shape[1]+1,1))[:y1-y0,:x1-x0]
            tiles=Image.fromarray(tiled)
            packed=old.copy()
            packed.paste(tiles,(x0,1024-y1))
            target=candidate/path.name
            meta=PngImagePlugin.PngInfo()
            for key,value in old.info.items():
                if isinstance(value,str):
                    meta.add_text(key,value)
            options={k:old.info[k] for k in ('dpi','icc_profile','transparency') if k in old.info}
            packed.save(target,pnginfo=meta,compress_level=9,**options)
            with Image.open(target) as after:
                assert (after.mode,after.size)==(old.mode,old.size)
                new=np.asarray(after)
                assert np.array_equal(new[1024-y1:1024-y0,x0:x1],tiled)
                mask=np.ones(new.shape[:2],dtype=bool)
                mask[1024-y1:1024-y0,x0:x1]=False
                assert np.array_equal(new[mask],baseline[mask])
                outputs.append({'file':path.name,'before_sha256':sha(path),'after_sha256':sha(target),
                                'pixels_changed':int(np.any(new!=baseline,axis=2).sum()),
                                'bytes_before':path.stat().st_size,'bytes_after':target.stat().st_size,
                                'dimensions':list(old.size),'mode':old.mode,
                                'unchanged_outside_patch':True})
    (evidence.parent/'claudia-roof-textures.json').write_text(json.dumps(outputs,indent=2)+'\n')
    print('VERIFIED channels',len(outputs),'outside-region exact')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path)
    p.add_argument('candidate',type=Path)
    p.add_argument('geometry_evidence',type=Path)
    a=p.parse_args()
    build(a.source,a.candidate,a.geometry_evidence)
