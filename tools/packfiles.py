"""Effective files of a data pack for one pack format: base files, then each matching overlay in order."""

import json
import zipfile
from pathlib import Path


class FolderPack:
    """An unpacked data pack, read like a zip file."""

    def __init__(self, root: Path):
        self.root = Path(root)

    def namelist(self) -> list:
        return [p.relative_to(self.root).as_posix() for p in sorted(self.root.rglob("*")) if p.is_file()]

    def read(self, name: str) -> bytes:
        return (self.root / name).read_bytes()


def matching_overlays(meta: dict, fmt: int) -> list:
    out = []
    for entry in meta.get("overlays", {}).get("entries", []):
        lo, hi = entry.get("min_format"), entry.get("max_format")
        formats = entry.get("formats")
        if lo is None and formats is not None:
            if isinstance(formats, list):
                lo, hi = formats[0], formats[-1]
            elif isinstance(formats, dict):
                lo, hi = formats.get("min_inclusive"), formats.get("max_inclusive")
            else:
                lo = hi = formats
        lo = lo[0] if isinstance(lo, list) else lo
        hi = hi[0] if isinstance(hi, list) else hi
        if lo <= fmt <= hi:
            out.append(entry["directory"])
    return out


def effective(path: str, fmt: int = 121) -> tuple:
    """Open a pack (zip or folder) and map each file the game would load to (overlay or "base", name in the pack)."""
    pack = FolderPack(path) if Path(path).is_dir() else zipfile.ZipFile(path)
    meta = json.loads(pack.read("pack.mcmeta"))
    every = [entry["directory"] for entry in meta.get("overlays", {}).get("entries", [])]
    names = [n for n in pack.namelist() if not n.endswith("/")]
    files = {}
    for name in names:
        if not any(name.startswith(d + "/") for d in every):
            files[name] = ("base", name)
    for d in matching_overlays(meta, fmt):
        for name in names:
            if name.startswith(d + "/"):
                files[name[len(d) + 1:]] = (d, name)
    return pack, files
