"""Validate the exact screenshot set and the integrity of PNG chunks."""

import pathlib
import struct
import sys
import zlib

EXPECTED = {f"{theme}-{screen}.png" for theme in ("light", "dark") for screen in ("home", "settings")}
SIGNATURE = bytes.fromhex("89504e470d0a1a0a")


def validate_png(path):
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
            if end != len(data):
                # A complete PNG can be recovered without modifying any image data.
                print(f"{path.name}: removing {len(data) - end} bytes after verified IEND")
                path.write_bytes(data[:end])
            print(f"{path.name}: {dimensions[0]}x{dimensions[1]}, {end} bytes")
            return
        offset = end
    raise ValueError(f"missing complete IEND chunk ({len(data)} bytes)")


def main():
    root = pathlib.Path(sys.argv[1])
    actual = {p.name for p in root.iterdir()}
    if actual != EXPECTED:
        raise SystemExit(f"Missing: {sorted(EXPECTED - actual)}; unexpected: {sorted(actual - EXPECTED)}")
    for name in sorted(EXPECTED):
        try:
            validate_png(root / name)
        except (ValueError, OSError) as exc:
            raise SystemExit(f"{name}: {exc}") from exc


if __name__ == "__main__":
    main()
