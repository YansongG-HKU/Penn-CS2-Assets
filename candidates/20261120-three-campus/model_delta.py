"""Build or replay exact candidate mesh changes against cloned LFS originals."""
import argparse
import hashlib
import json
from pathlib import Path

import zstandard

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('build','apply'))
    parser.add_argument('repository', type=Path)
    parser.add_argument('candidates', type=Path)
    parser.add_argument('delta', type=Path)
    parser.add_argument('--geometry-evidence', type=Path)
    parser.add_argument('--shader-evidence', type=Path)
    args = parser.parse_args()
    if args.mode == 'build':
        args.delta.mkdir(parents=True,exist_ok=False)
        manifest = []
        replacements = {}
        if args.geometry_evidence:
            evidence = json.loads(args.geometry_evidence.read_text())
            for asset, entries in evidence.items():
                for entry in entries:
                    replacements[asset, entry['fbx']] = {
                        'verified_baseline_sha256': entry['old_sha256'],
                        'zero_area_triangles_removed': entry['removed_zero_area_triangles'],
                    }
        if args.shader_evidence:
            for receipt in sorted(args.shader_evidence.glob('*.json')):
                row = json.loads(receipt.read_text())
                uv = {x['file']:x['corner_uv_triangles_repaired'] for x in row.get('glass_uv_repair',[])}
                for record in row.get('special_shader_material_bindings_removed', []):
                    name = record['file']
                    replacements[row['asset'], name] = {
                        'preview_material_removed': True,
                        'glass_zero_area_uv_triangles_repaired': uv.get(name,0),
                        'expected_candidate_sha256': row['files'][name]['sha256'],
                    }
        for (asset, name), changes in sorted(replacements.items()):
            path = Path(asset)/'fbx/split'/name
            destination = Path(asset)/name
            original = (args.repository/path).read_bytes()
            candidate = (args.candidates/destination).read_bytes()
            before, after = digest(original), digest(candidate)
            assert changes.pop('verified_baseline_sha256',before) == before
            assert changes.pop('expected_candidate_sha256',after) == after
            patch = zstandard.ZstdCompressor(level=10,dict_data=zstandard.ZstdCompressionDict(
                original,dict_type=zstandard.DICT_TYPE_RAWCONTENT)).compress(candidate)
            patch_name = name + '.zst'
            (args.delta/patch_name).write_bytes(patch)
            manifest.append({'base':path.as_posix(),'candidate':destination.as_posix(),'patch':patch_name,
                             'before_sha256':before,'after_sha256':after,
                             'patch_sha256':digest(patch),'bytes':len(candidate),**changes})
        (args.delta/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    else:
        args.candidates.mkdir(parents=True,exist_ok=False)
        for row in json.loads((args.delta/'manifest.json').read_text()):
            original,patch = (args.repository/row['base']).read_bytes(),(args.delta/row['patch']).read_bytes()
            assert digest(original) == row['before_sha256'] and digest(patch) == row['patch_sha256']
            dictionary = zstandard.ZstdCompressionDict(original,dict_type=zstandard.DICT_TYPE_RAWCONTENT)
            new = zstandard.ZstdDecompressor(dict_data=dictionary).decompress(patch,max_output_size=row['bytes'])
            assert len(new) == row['bytes'] and digest(new) == row['after_sha256']
            file = args.candidates/row['candidate']
            file.parent.mkdir(parents=True,exist_ok=True)
            file.write_bytes(new)
            print(row['candidate'],row['after_sha256'])

if __name__ == '__main__':
    main()
