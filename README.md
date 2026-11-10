# DatapackCompat

A data pack that makes the packs on my Leaf 26.3 server work together, the load order they need, and tools to find conflicts and set the order.

When two packs define the same file, the one loaded later wins and the other's version is lost. The load order settles most conflicts; this pack merges the two that no order can. It also stops From the Fog's NbtPredicate log errors and makes three head lookups search items only.

| File | Merges | Without it |
| --- | --- | --- |
| `data/minecraft/loot_table/entities/silverfish.json` | 5555ff lib's silverfish loot (vanilla drops, the Mob Heads head, Name Tag's tag) with Incendium's gravel from Nether silverfish | Either silverfish never drop heads and name tags, or Nether silverfish drop no gravel |
| `data/mob_heads/function/reset_all.mcfunction` | Mob Heads' reset with the Tropical Fish add-on's | Resetting clears either the main collection or the fish collection, not both |

## From the Fog's serialization errors

From the Fog ticks each Herobrine entity in one loop, and any of them can remove Herobrine. When that happens before the loop reaches his mannequin, the loop still writes the dead mannequin's rotation. A mannequin that has died can't be read while it's dying, so the server logs `NbtPredicate` serialization errors ending in `Failed to encode value 'DYING' to field 'pose'`. This pack's copy of `data/lunareclipse.watching/function/sightings/models/remove.mcfunction` takes the mannequin's From the Fog tags off and kills it a tick later, outside the loop; `datapackcompat:from_the_fog/kill_removed` does the kill and also runs on load.

## Item-only head lookups

5555ff lib and Player Drops Head find a player's name by spawning a head item and searching for it with an NBT selector, which serialises every entity in the loaded chunks. These copies add `type=item`, which finds the same head and serialises only items:

| File | From |
| --- | --- |
| `data/jodek/function/api/data/get/player_name.mcfunction` | 5555ff lib 1.3.3.0 |
| `data/player_drops_head/function/config/player/build_array.mcfunction` | Player Drops Head 3.7.1 |
| `data/player_drops_head/function/config/player/kill_player_head.mcfunction` | Player Drops Head 3.7.1 |

Built for Incendium Legacy 5.5.4, 5555ff lib 1.3.3.0, Mob Heads 5.3.1, Tropical Fish 1.0.1.2, Player Drops Head 3.7.1 and From the Fog 1.11.3. Check it again when any of them updates. 1.2.0 dropped the copy of Sleep's lookup along with Sleep: it names Sleep's loot table, so it fails to load without the pack.

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
| DatapackCompat | above all of them | It replaces the files it merges and the four it fixes |

The rest have no files in common.

The server adds a pack it hasn't seen before at the top of the order, so a new version of this pack, with a new file name, lands above everything on its own.

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
python3 -I tools/package.py dist/DatapackCompat-1.2.0.zip
```

## Licence

[PolyForm Noncommercial 1.0.0](LICENSE.md) for this repo's own work. The merged and fixed files carry parts of Jodek's packs (MIT), Incendium (Stardust Labs licence) and From the Fog (CC BY-NC-SA 4.0), listed in [NOTICE.md](NOTICE.md).
