"""Validate the exact screenshot set and the integrity of PNG chunks."""

import json
import pathlib
import struct
import sys
import zlib

MANIFEST = json.loads(pathlib.Path(__file__).with_name("screenshot-scenarios.json").read_text())
LAYOUTS = MANIFEST["layouts"]
SIGNATURE = bytes.fromhex("89504e470d0a1a0a")


def expected_names(layouts, themes):
    unknown_layouts = set(layouts) - LAYOUTS.keys()
    unknown_themes = set(themes) - set(MANIFEST["themes"])
    if unknown_layouts or unknown_themes or not layouts or not themes:
        raise ValueError(f"unknown or missing screenshot selection: {unknown_layouts}, {unknown_themes}")
    return {
        f"{theme}-{layout}-{screen}.png"
        for theme in themes
        for layout in layouts
        for screen in LAYOUTS[layout]["screens"]
    }


EXPECTED = expected_names(list(LAYOUTS), MANIFEST["themes"])


def validate_png(path, expected_dimensions=None):
    data = path.read_bytes()
    if not data.startswith(SIGNATURE):
        raise ValueError(f"invalid PNG signature ({len(data)} bytes; header={data[:16].hex()})")
    offset = len(SIGNATURE)
    types = []
    dimensions = None
    while offset + 12 <= len(data):
        size, kind = struct.unpack_from(">I4s", data, offset)
        end = offset + 12 + size
        if end > len(data):
            raise ValueError(f"truncated {kind!r} chunk at byte {offset}")
        body = data[offset + 8 : end - 4]
        crc = struct.unpack_from(">I", data, end - 4)[0]
        if zlib.crc32(kind + body) != crc:
            raise ValueError(f"CRC mismatch for {kind!r} at byte {offset}")
        types.append(kind)
        if kind == b"IHDR":
            if size != 13:
                raise ValueError("invalid IHDR length")
            dimensions = struct.unpack_from(">II", body)
        if kind == b"IEND":
            if size or types[0] != b"IHDR" or b"IDAT" not in types or not dimensions or not all(dimensions):
                raise ValueError("invalid PNG structure")
            if expected_dimensions is not None and dimensions != expected_dimensions:
                raise ValueError(f"unexpected dimensions {dimensions}; expected {expected_dimensions}")
            if end != len(data):
                # A complete PNG can be recovered without modifying any image data.
                print(f"{path.name}: removing {len(data) - end} bytes after verified IEND")
                path.write_bytes(data[:end])
            print(f"{path.name}: {dimensions[0]}x{dimensions[1]}, {end} bytes")
            return
        offset = end
    raise ValueError(f"missing complete IEND chunk ({len(data)} bytes)")


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--names":
        layout = sys.argv[2]
        print(" ".join(f"{layout}-{screen}" for screen in LAYOUTS[layout]["screens"]))
        return
    if sys.argv[1] == "--layouts":
        print(" ".join(LAYOUTS))
        return
    if sys.argv[1] == "--themes":
        print(" ".join(MANIFEST["themes"]))
        return
    if sys.argv[1] == "--display":
        spec = LAYOUTS[sys.argv[2]]
        print(spec["size"], spec["density"], spec["rotation"])
        return
    if sys.argv[1] == "--selected":
        root = pathlib.Path(sys.argv[2])
        layouts = sys.argv[3].split()
        themes = sys.argv[4].split()
    else:
        root = pathlib.Path(sys.argv[1])
        layouts = list(LAYOUTS)
        themes = MANIFEST["themes"]
    try:
        expected = expected_names(layouts, themes)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    actual = {p.name for p in root.iterdir()}
    if actual != expected:
        raise SystemExit(f"Missing: {sorted(expected - actual)}; unexpected: {sorted(actual - expected)}")
    for name in sorted(expected):
        try:
            layout = next(layout for layout in LAYOUTS if f"-{layout}-" in name)
            expected_dimensions = tuple(map(int, LAYOUTS[layout]["size"].split("x")))
            validate_png(root / name, expected_dimensions)
        except (ValueError, OSError) as exc:
            raise SystemExit(f"{name}: {exc}") from exc


if __name__ == "__main__":
    main()
