execute at @s run loot spawn ~ ~100 ~ loot jodek:player_head
$data modify storage $(target):root data.player_name set from entity @e[type=item,nbt={Item:{components:{"minecraft:custom_data":{jodek.player_name:1b}}}},limit=1] Item.components."minecraft:profile".name
kill @e[type=item,nbt={Item:{components:{"minecraft:custom_data":{jodek.player_name:1b}}}}]