"""Apply the exact Claudia Cohen LOD2 change to the preceding isolated package."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

import zstandard

def sha(data):
    return hashlib.sha256(data).hexdigest()

def make_replay(source, output, patch):
    source=source.resolve(strict=True)
    output=output.resolve()
    if output.exists() or output.is_relative_to(source) or source.is_relative_to(output):
        raise ValueError('Choose a fresh output outside the original folder')
    entries=json.loads((patch/'manifest.json').read_text())['files']
    blobs={}
    for name,row in entries.items():
        if Path(name).name != name:
            raise ValueError(name)
        before=(source/name).read_bytes()
        assert len(before)==row['before_bytes'] and sha(before)==row['before_sha256']
        if not row.get('patch'):
            continue
        compressed=(patch/row['patch']).read_bytes()
        assert sha(compressed)==row['patch_sha256']
        dictionary=zstandard.ZstdCompressionDict(before,dict_type=zstandard.DICT_TYPE_RAWCONTENT)
        new=zstandard.ZstdDecompressor(dict_data=dictionary).decompress(compressed,max_output_size=row['after_bytes'])
        assert len(new)==row['after_bytes'] and sha(new)==row['after_sha256']
        blobs[name]=new
    output.mkdir(parents=True)
    for name in entries:
        if name in blobs:
            (output/name).write_bytes(blobs[name])
        else:
            shutil.copyfile(source/name,output/name)
    for name,row in entries.items():
        assert sha((output/name).read_bytes())==row['after_sha256']
    print(f'{len(entries)} assets files verified, {len(blobs)} replacements')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('baseline',type=Path)
    p.add_argument('output',type=Path)
    p.add_argument('--delta',type=Path,default=Path(__file__).resolve().parent/'delta')
    a=p.parse_args()
    make_replay(a.baseline,a.output,a.delta)
