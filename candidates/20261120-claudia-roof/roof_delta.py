"""Apply the exact Claudia Cohen LOD2 change to the preceding isolated package."""
import argparse
import hashlib
import json
from pathlib import Path

import zstandard

def sha(data):
    return hashlib.sha256(data).hexdigest()

def checked(label, data, size, digest):
    if (size is not None and len(data) != size) or sha(data) != digest:
        raise ValueError(f"{label}: size or SHA-256 mismatch")

def make_replay(source, output, patch):
    source=source.resolve(strict=True)
    output=output.resolve()
    if output.exists() or output.is_relative_to(source) or source.is_relative_to(output):
        raise ValueError('Choose a fresh output outside the original folder')
    entries=json.loads((patch/'manifest.json').read_text())['files']
    blobs={}
    for name,row in entries.items():
        if name in ('.', '..') or Path(name).name != name:
            raise ValueError(name)
        before=(source/name).read_bytes()
        checked(f"{name} baseline", before, row["before_bytes"], row["before_sha256"])
        patch_name = row.get('patch')
        if not patch_name:
            checked(f"{name} unchanged output", before, row["after_bytes"], row["after_sha256"])
            blobs[name] = before
            continue
        if not isinstance(patch_name, str) or patch_name in ('.', '..') or Path(patch_name).name != patch_name:
            raise ValueError(f"{name}: invalid delta filename")
        compressed=(patch/patch_name).read_bytes()
        checked(f"{name} delta", compressed, None, row["patch_sha256"])
        dictionary=zstandard.ZstdCompressionDict(before,dict_type=zstandard.DICT_TYPE_RAWCONTENT)
        new=zstandard.ZstdDecompressor(dict_data=dictionary).decompress(compressed,max_output_size=row['after_bytes'])
        checked(f"{name} replay output", new, row["after_bytes"], row["after_sha256"])
        blobs[name]=new
    output.mkdir(parents=True)
    for name, data in blobs.items():
        (output/name).write_bytes(data)
    for name, row in entries.items():
        checked(f"{name} written output", (output/name).read_bytes(), row["after_bytes"], row["after_sha256"])
    replaced = sum(bool(row.get('patch')) for row in entries.values())
    print(f'{len(entries)} asset files verified, {replaced} replacements')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('baseline',type=Path)
    p.add_argument('output',type=Path)
    p.add_argument('--delta',type=Path,default=Path(__file__).resolve().parent/'delta')
    a=p.parse_args()
    make_replay(a.baseline,a.output,a.delta)
