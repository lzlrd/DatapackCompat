"""Put a world's data packs in a given load order by rewriting its level.dat. Run it only while the server is stopped:
a running server writes its own list back over the file.

Usage: python3 -I tools/reorder.py LEVEL_DAT ORDER_FILE OUT_LEVEL_DAT

ORDER_FILE lists pack IDs (such as file/Terralith_v2.6.5+26.3.zip), one per line, from lowest to highest priority;
blank lines and lines starting with # are skipped. Those packs end up last in the enabled list, in that order, and
come off the disabled list. Enabled packs the file doesn't name (vanilla, paper, plugin packs) keep their order
below them. Needs nbtlib (pip install nbtlib).
"""

import sys

import nbtlib
from nbtlib.tag import List, String


def main() -> None:
    source, order_file, target = sys.argv[1:4]
    wanted = [line.strip() for line in open(order_file, encoding="utf-8")
              if line.strip() and not line.lstrip().startswith("#")]
    if len(set(wanted)) != len(wanted):
        raise SystemExit("ORDER_FILE names a pack twice")
    level = nbtlib.load(source)
    data = level["Data"] if "Data" in level else level[""]["Data"]
    packs = data["DataPacks"]
    enabled = [str(name) for name in packs["Enabled"]]
    disabled = [str(name) for name in packs["Disabled"]]
    kept = [name for name in enabled if name not in wanted]
    for name in kept:
        if name.startswith("file/"):
            print(f"warning: {name} is enabled but not in the order file, so it stays below the ordered packs")
    for name in wanted:
        if name not in enabled:
            print(f"enabling {name}")
    packs["Enabled"] = List[String]([String(name) for name in kept + wanted])
    packs["Disabled"] = List[String]([String(name) for name in disabled if name not in wanted])
    level.save(target)
    print("enabled, lowest priority first:")
    for name in kept + wanted:
        print(f"  {name}")


if __name__ == "__main__":
    main()
