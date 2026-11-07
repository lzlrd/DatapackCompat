"""List the files two or more data packs both define, which the higher pack in the load order wins.

Usage: python3 -I tools/overlap.py [--format N] PACK [PACK ...]

PACKs are zips or folders. Tags are left out unless one of them replaces the others, since tags otherwise merge.
The pack format defaults to 121 (26.3) and picks which overlays apply.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from packfiles import effective  # noqa: E402


def main() -> None:
    args = sys.argv[1:]
    fmt = 121
    if args[:1] == ["--format"]:
        fmt, args = int(args[1]), args[2:]
    owners, sources = {}, {}
    for pack in args:
        archive, files = effective(pack, fmt)
        name = Path(pack).name
        for rel, (_, inner) in files.items():
            if rel.startswith("data/"):
                owners.setdefault(rel, []).append(name)
                sources[(name, rel)] = (archive, inner)
    groups = {}
    for rel, names in owners.items():
        if len(names) < 2:
            continue
        if "/tags/" in rel:
            if not any(json.loads(sources[(n, rel)][0].read(sources[(n, rel)][1])).get("replace") for n in names):
                continue
            rel += " (replace)"
        groups.setdefault(tuple(names), []).append(rel)
    for names, files in sorted(groups.items(), key=lambda item: -len(item[1])):
        print(f"{len(files):5d}  {' + '.join(names)}")
        for rel in sorted(files)[:6]:
            print(f"         {rel}")
    if not groups:
        print("no files in common")


if __name__ == "__main__":
    main()
