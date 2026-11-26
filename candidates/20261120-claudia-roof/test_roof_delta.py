"""Exercise fail-closed replay with and without optimized Python."""
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

class Replay(unittest.TestCase):
    def test_replay_and_corrupt_inputs(self):
        script = Path(__file__).with_name("roof_delta.py")
        for flags in ([], ["-O"]):
            for case in ("valid", "baseline", "delta", "output_sha", "output_size",
                         "unchanged_sha", "unchanged_size", "path"):
                with self.subTest(flags=flags, case=case), tempfile.TemporaryDirectory() as work:
                    root = Path(work)
                    src, patch, dest = [root / name for name in ("source", "patch", "dest")]
                    src.mkdir()
                    patch.mkdir()
                    old, new, untouched = b"original_" * 32, b"candidate_" * 32, b"unchanged"
                    dictionary = zstandard.ZstdCompressionDict(old, dict_type=zstandard.DICT_TYPE_RAWCONTENT)
                    delta = zstandard.ZstdCompressor(dict_data=dictionary).compress(new)
                    rows = {
                        "model.fbx": dict(before_bytes=len(old), before_sha256=sha(old), after_bytes=len(new),
                                          after_sha256=sha(new), patch="model.zst", patch_sha256=sha(delta)),
                        "texture.png": dict(before_bytes=len(untouched), before_sha256=sha(untouched),
                                            after_bytes=len(untouched), after_sha256=sha(untouched)),
                    }
                    if case == "baseline":
                        old += b"bad"
                    elif case == "delta":
                        delta += b"bad"
                    elif case == "output_sha":
                        rows["model.fbx"]["after_sha256"] = "0" * 64
                    elif case == "output_size":
                        rows["model.fbx"]["after_bytes"] += 1
                    elif case == "unchanged_sha":
                        rows["texture.png"]["after_sha256"] = "0" * 64
                    elif case == "unchanged_size":
                        rows["texture.png"]["after_bytes"] += 1
                    elif case == "path":
                        rows["model.fbx"]["patch"] = "../model.zst"
                    (src / "model.fbx").write_bytes(old)
                    (src / "texture.png").write_bytes(untouched)
                    (patch / "model.zst").write_bytes(delta)
                    (patch / "manifest.json").write_text(json.dumps({"files": rows}))
                    result = subprocess.run([sys.executable, *flags, str(script), str(src),
                                             str(dest), "--delta", str(patch)],
                                            capture_output=True, text=True)
                    if case == "valid":
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertEqual((dest / "model.fbx").read_bytes(), new)
                        self.assertEqual((dest / "texture.png").read_bytes(), untouched)
                    else:
                        self.assertNotEqual(result.returncode, 0)
                        self.assertIn("ValueError", result.stderr)
                        self.assertFalse(dest.exists())

if __name__ == "__main__":
    unittest.main()
