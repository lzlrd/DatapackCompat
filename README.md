# DatapackCompat

A data pack that makes the packs on my Leaf 26.3 server work together, the load order they need, and tools to find conflicts and set the order.

When two packs define the same file, the one loaded later wins and the other's version is lost. The load order settles most conflicts; this pack merges the two that no order can.

| File | Merges | Without it |
| --- | --- | --- |
| `data/minecraft/loot_table/entities/silverfish.json` | 5555ff lib's silverfish loot (vanilla drops, the Mob Heads head, Name Tag's tag) with Incendium's gravel from Nether silverfish | Either silverfish never drop heads and name tags, or Nether silverfish drop no gravel |
| `data/mob_heads/function/reset_all.mcfunction` | Mob Heads' reset with the Tropical Fish add-on's | Resetting clears either the main collection or the fish collection, not both |

Built for Incendium Legacy 5.5.4, 5555ff lib 1.3.3.0, Mob Heads 5.3.1 and Tropical Fish 1.0.1.2. Check it again when any of them updates.

## Load order

`server-order.txt` is my server's order, lowest priority first. What forces it:

| Pack | Must load | Why |
| --- | --- | --- |
| Terralith ReStoned | above Terralith | It turns back on the andesite, diorite and granite blobs Terralith turns off; below Terralith it does nothing |
| Terraphilic | above Terralith and Geophilic | It merges the 24 biomes both change |
| zRemove_SDL_Intro | above Terralith, Incendium and Nullscape | It replaces their intro toast functions |
| The Dungeons and Taverns overhauls | above Dungeons and Taverns | They replace its witch hut base, monument pillars and some loot |
| 5555ff lib | above Incendium, below Jodek's other packs | Its silverfish loot replaces Incendium's; its empty Mob Heads and Name Tag loot tables are placeholders those packs replace |
| Tropical Fish | above Mob Heads | It is the add-on |
| DatapackCompat | above all of them | It replaces the files it merges |

The rest have no files in common.

## Tools

Find the files packs share, lowest priority first:

```sh
python3 -I tools/overlap.py PACK ...
```

Put a world's packs in order. Stop the server first, or it writes its own list back over `level.dat`, and keep a copy of the original:

```sh
pip install nbtlib
python3 -I tools/reorder.py world/level.dat server-order.txt level.dat.new
```

Build the pack:

```sh
python3 -I tools/package.py dist/DatapackCompat-1.0.0.zip
```

## Licence

[PolyForm Noncommercial 1.0.0](LICENSE.md) for this repo's own work. The merged files carry parts of Jodek's packs (MIT) and Incendium (Stardust Labs licence), listed in [NOTICE.md](NOTICE.md).
