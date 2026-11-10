# If a player if fixated on Herobrine then make him teleport to them and jumpscare them. (Only if GHC is enabled.)
execute if data storage lunareclipse.watching:config_options {options:{give_him_control:"true"}} unless score teleport_jumpscared watching.global_values matches 1 if predicate lunareclipse.watching:chances/1 as @r[predicate=lunareclipse.watching:checks/fixated] at @s run return run function lunareclipse.watching:sightings/player_spotted/spotted/teleport_jumpscare

# If he was spotted through glass place a sign in his place.
execute if score spotted_sign watching.global_values matches 1 as @e[type=#lunareclipse.watching:herobrine,tag=watching.ai] at @s run function lunareclipse.watching:signs/init_place

# Play the smoke particle if enabled.
execute unless data storage lunareclipse.watching:global_values {sightings:{type:"haunted_herd"}} unless data storage lunareclipse.watching:global_values sightings.slip_behind as @e[type=#lunareclipse.watching:herobrine,tag=watching.ai] at @s run function lunareclipse.watching:sightings/player_spotted/shrouded_specter/start with storage lunareclipse.watching:config_options options
# Run the cleanup function.
execute as @e[type=#lunareclipse.watching:herobrine,tag=watching.herobrine] at @s run function lunareclipse.watching:sightings/cleanup

# Teleport the no sleep husk and the mannequin into the void.
execute as @e[type=minecraft:husk,tag=watching.herobrine] at @s run tp ~ -512 ~
execute as @e[type=minecraft:mannequin,tag=watching.herobrine] at @s run tp ~ -512 ~

# Send a message.
execute if entity @e[type=#lunareclipse.watching:herobrine,tag=watching.herobrine] run function lunareclipse.watching:debug/message {message: "Sighting Removed", status: "1", info: {}, info_list: []}

# DatapackCompat: the mannequin dies next tick instead. This tick's Herobrine loop may still reach it and write its
# rotation, and a mannequin that has just died can't be read while it's dying, which logs an NbtPredicate serialization
# error. Without its tags the loop skips it.
tag @e[type=minecraft:mannequin,tag=watching.herobrine] add datapackcompat.removed
tag @e[type=minecraft:mannequin,tag=datapackcompat.removed] remove watching.mannequin
tag @e[type=minecraft:mannequin,tag=datapackcompat.removed] remove watching.herobrine
schedule function datapackcompat:from_the_fog/kill_removed 1t

# Kill all herobrine entities.
kill @e[type=#lunareclipse.watching:herobrine,tag=watching.herobrine]