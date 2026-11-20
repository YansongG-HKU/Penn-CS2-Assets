"""Regression test: replay checks must remain enabled with python -O."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import zstandard


def sha(data):
    return hashlib.sha256(data).hexdigest()


class ReplayChecks(unittest.TestCase):
    def test_exact_and_corrupted_manifests(self):
        script = Path(__file__).with_name('model_delta.py')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = root / 'base'
            patches = root / 'patches'
            base.mkdir()
            patches.mkdir()
            data = bytes(range(256)) * 4
            (base / 'base.fbx').write_bytes(data)
            expected = data + b'candidate'
            dictionary = zstandard.ZstdCompressionDict(data, dict_type=zstandard.DICT_TYPE_RAWCONTENT)
            patch = zstandard.ZstdCompressor(dict_data=dictionary).compress(expected)
            (patches / 'candidate.zst').write_bytes(patch)
            row = dict(base='base.fbx', candidate='candidate.fbx', patch='candidate.zst',
                       before_sha256=sha(data), patch_sha256=sha(patch),
                       after_sha256=sha(expected), bytes=len(expected))
            for opt in ([], ['-O']):
                for idx, field in enumerate((None, 'before_sha256', 'patch_sha256', 'after_sha256', 'bytes')):
                    with self.subTest(optimized=bool(opt), corrupted_field=field):
                        case = row.copy()
                        if field:
                            case[field] = row[field] + 1 if field == 'bytes' else '0' * 64
                        (patches / 'manifest.json').write_text(json.dumps([case]))
                        dest = root / f'output-{len(opt)}-{idx}'
                        result = subprocess.run([sys.executable, '-B', *opt, str(script), 'apply',
                                                 str(base), str(dest), str(patches)],
                                                capture_output=True, text=True, check=False)
                        target = dest / 'candidate.fbx'
                        if field:
                            self.assertNotEqual(result.returncode, 0)
                            self.assertIn('ValueError', result.stderr)
                            self.assertFalse(target.exists())
                        else:
                            self.assertEqual(result.returncode, 0, result.stderr)
                            self.assertEqual(target.read_bytes(), expected)


if __name__ == '__main__':
    unittest.main()
