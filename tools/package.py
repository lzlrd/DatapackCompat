"""Build the data pack's zip: pack.mcmeta and data/, sorted and with fixed timestamps so builds match.

Usage: python3 -I tools/package.py OUT.zip
"""

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAMP = (2026, 1, 1, 0, 0, 0)


def main() -> None:
    out = Path(sys.argv[1])
    out.parent.mkdir(parents=True, exist_ok=True)
    files = [ROOT / "pack.mcmeta", ROOT / "LICENSE.md", ROOT / "NOTICE.md"]
    files += sorted(p for p in (ROOT / "data").rglob("*") if p.is_file())
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as pack:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(ROOT).as_posix(), STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            pack.writestr(info, path.read_bytes())
    print(f"{len(files)} files written to {out}")


if __name__ == "__main__":
    main()
