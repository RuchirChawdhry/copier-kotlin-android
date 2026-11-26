"""Fast checks of generated project tooling; no Android SDK required."""
import importlib.util
import json
import pathlib
import struct
import subprocess
import tempfile
import tomllib
import unittest
import zlib

ROOT = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "validate-screenshots.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))


class ToolingTest(unittest.TestCase):
    def test_shell_syntax(self):
        for path in ROOT.glob("*.sh"):
            subprocess.run(["bash", "-n", str(path)], check=True)

    def test_python_syntax(self):
        for path in ROOT.glob("*.py"):
            compile(path.read_text(), str(path), "exec")

    def test_catalog(self):
        catalog = tomllib.loads((ROOT.parent / "gradle/libs.versions.toml").read_text())
        self.assertIn("agp", catalog["versions"])
        self.assertIn("datastore", catalog["libraries"])

    def test_manifest_and_png(self):
        expected_count = len(validator.MANIFEST['themes']) * sum(
            len(spec['screens']) for spec in validator.LAYOUTS.values()
        )
        self.assertEqual(expected_count, len(validator.EXPECTED))
        self.assertEqual({"phone", "rail", "wide", "landscape"}, set(validator.LAYOUTS))
        png = (
            validator.SIGNATURE
            + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"\x00\x00\x00\x00"))
            + chunk(b"IEND", b"")
        )
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / "test.png"
            path.write_bytes(png)
            validator.validate_png(path)
            path.write_bytes(png[:-1])
            with self.assertRaises(ValueError):
                validator.validate_png(path)

    def test_device_help(self):
        subprocess.run(["python3", str(ROOT / "device.py"), "--help"], check=True, capture_output=True)


if __name__ == "__main__":
    unittest.main()
