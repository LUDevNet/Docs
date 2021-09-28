Flag System
-----------

The flag system is used to track various YES or NO decisions within the game for each
player. This includes information on the :doc:`kit-factions`, the minimap, ingame objects
that the player interacted with, the last VE-mission and more.

The flags are stored into a 12008 bit number as taskmask. Because there is no numberic datatype,
which can hold up to 12008 bits, the taskmask is split up into tiny parts, each 64 bits.

Derived Flag Numbers
^^^^^^^^^^^^^^^^^^^^

The flag ids used for binoculars and story plaques is generally
derived from the current zone ID and an additional index:

ZZNN
    | The player has looked through binocular NN on zones ZZ…
    | Source: :script:`02_client/map/general/l_binoculars_client.lua`
10000+Z+N
    | The player has read story plaque N in zone Z
    | Source: :script:`02_client/map/general/l_story_box_interact_client.lua`

Known Flags
^^^^^^^^^^^

.. role:: raw-html(raw)
    :format: html

.. csv-table::
    :header-rows: 1
    :widths: 5, 80, 15

    Flag, Description, Source
    1, player has entered pet ranch, 1.1.18 client
    2, minimap unlocked, 1.1.18 client
    3, activity rebuilding fail time, 1.1.18 client
    4, activity rebuilding fail range, 1.1.18 client
    5, activity shooting gallery help, 1.1.18 client
    6, help walking controls, 1.1.18 client
    7, first smashable, 1.1.18 client
    8, first imagination pickup, 1.1.18 client
    9, first damage, 1.1.18 client
    10, first item, 1.1.18 client
    11, first brick, 1.1.18 client
    12, first consumable, 1.1.18 client
    13, first equippable, 1.1.18 client
    14, chat help, 1.1.18 client
    15, first pet taming minigame, 1.1.18 client
    16, first pet on switch, 1.1.18 client
    17, first pet jumped on switch, 1.1.18 client
    18, first pet found treasure, 1.1.18 client
    19, first pet dug treasure, 1.1.18 client
    20, first pet owner on pet bouncer, 1.1.18 client
    21, first pet despawn no imagination, 1.1.18 client
    22, first pet selected enough bricks, 1.1.18 client
    23, first emote unlocked, 1.1.18 client
    24, GF - Pirate Rep, 1.1.18 client
    25, AG - bpb cinematic event, 1.1.18 client
    26, help jumping controls, 1.1.18 client
    27, help double jump controls, 1.1.18 client
    28, help camera controls, 1.1.18 client
    29, help rotate controls, 1.1.18 client
    30, help smash, 1.1.18 client
    31, Monument Intro Music Played, 1.1.18 client
    32, Beginning Zone Summary Displayed, 1.1.18 client
    33, AG - Finish Line Built, 1.1.18 client
    34, AG - Boss Area Found, 1.1.18 client
    35, AG - Landed in Battlefield, 1.1.18 client
    36, GF - Player has been to the ravine, 1.1.18 client
    37, Modular Build Started, 1.1.18 client
    38, Modular Build Finished click button, 1.1.18 client
    39, Thinking Hat received go to modular build area, 1.1.18 client
    40, Build Area entered mod NOT activated put on Hat, 1.1.18 client
    41, Hat on inside of mod build equip a module from LEG, 1.1.18 client
    42, Module equipped place on glowing blue spot, 1.1.18 client
    43, First module placed correctly now do the rest, 1.1.18 client
    44, Rocket complete now launch from pad, :doc:`../database/Preconditions`
    45, joined a faction, 1.1.18 client
    46, The player has joined the **Venture League** :doc:`kit faction <kit-factions>`, 1.1.18 client
    47, The player has joined the **Assembly** :doc:`kit faction <kit-factions>`, 1.1.18 client
    48, The player has joined the **Paradox** :doc:`kit faction <kit-factions>`, 1.1.18 client
    49, The player has joined the **Sentinel** :doc:`kit faction <kit-factions>`, 1.1.18 client
    50, LUP World Access, 1.1.18 client
    51, AG first flag collected, 1.1.18 client
    52, tooltip talk to skyland to get hat, 1.1.18 client
    53, modular build player places first model in scratch, 1.1.18 client
    54, modular build first arrow display for module, 1.1.18 client
    55, "AG beacon QB, so the player can always build them", 1.1.18 client
    56, GF Pet Dig Flag 1, 1.1.18 client
    57, GF Pet Dig Flag 2, 1.1.18 client
    58, GF Pet Dig Flag 3, 1.1.18 client
    59, Suppress Spaceship Cinematic Flythrough, 1.1.18 client
    60, GF Player Fall Death, 1.1.18 client
    61, GF Player can get Flag 1, 1.1.18 client
    62, GF Player can get Flag 2, 1.1.18 client
    63, GF Player can get Flag 3, 1.1.18 client
    64, Enter BBB from Property Edit confirmation dialog, 1.1.18 client
    65, AG First Combat Complete, 1.1.18 client
    66, AG - Complete Bob Mission, :script:`client/mission_bob.lua`
    67, Player can tame the lion pet, 1.1.18 client
    68, FV On Free the Ninjas Mission, 1.1.18 client
    69, First manual pet hibernate, 1.1.18 client
    70, First time in pet taming while having a pet out, 1.1.18 client
    71, Defeated maelstrom on small AG property, 1.1.18 client
    72, Player has completed the hammer mission, 1.1.18 client
    73, Placed first model on AG small property, 1.1.18 client
    79, Player secured property, 1.1.18 client
    80, Hat ON inside Property Edit, 1.1.18 client
    81, *Can do the Panda Race*:raw-html:`<br>` Player has completed all missions for :lot:`Brickmaster Clang <7423>`, :doc:`../database/Preconditions`
    82, Player has tamed a panda, 1.1.18 client
    83, First 'Out of Imagination', 1.1.18 client
    84, Delete Item from Inventory confirmation dialog, 1.1.18 client
    85, Completed Nimbus Station Race, 1.1.18 client
    86, First pickup when bag is full, 1.1.18 client
    87, First model, 1.1.18 client
    88, First behavior, 1.1.18 client
    89, First booster pack, 1.1.18 client
    90, First :doc:`package <../database/PackageComponent>`, 1.1.18 client
    92, Delete Model from Inventory confirmation dialog, 1.1.18 client
    93, Delete Brick from Inventory confirmation dialog, 1.1.18 client
    94, Delete Behavior from Inventory confirmation dialog, 1.1.18 client
    95,	Delete Property from Inventory confirmation dialog, 1.1.18 client
    96, Player tutorial mode, 1.1.18 client
    97, Defeat maelstrom from small NS property, 1.1.18 client
    98, Defeat maelstrom from small GF property, 1.1.18 client
    99, Defeat maelstrom from small FV property, 1.1.18 client
    101, Place 1st model on Property, 1.1.18 client
    102, place 2nd model on property, 1.1.18 client
    103, place 3rd model on property, 1.1.18 client
    104, place 4th model on property, 1.1.18 client
    105, Placed first model on NS small property, 1.1.18 client
    106, Placed first model on GF small property, 1.1.18 client
    107, Placed first model on FV small property, 1.1.18 client
    108, Claimed AG Small Property, 1.1.18 client
    109, Pick Up a Model, 1.1.18 client
    110, Rotate a Model, 1.1.18 client
    111, Put Away a Model, 1.1.18 client
    112, Have played the LS intro cinematic, 1.1.18 client
    113, Player has finished AG property tutorials, 1.1.18 client
    114, Player can now see the news screen, 1.1.18 client
    115, Player is in a Foot Race, 1.1.18 client
    117, The player has powered the (RtVE?) launcher with the console, :doc:`../database/Preconditions`
    801, :lot:`Elephant Pet - 3050 <3050>`, 1.1.18 client
    802, Not used, 1.1.18 client
    803, :lot:`Triceratops Pet - 3195 <3195>`, 1.1.18 client
    804, Reindeer - not in live 1, 1.1.18 client
    805, not used, 1.1.18 client
    806, Skunk Pet -, 1.1.18 client
    807, Cat Pet, 1.1.18 client
    808, Not Used, 1.1.18 client
    809, Not Used, 1.1.18 client
    810, Reindeer - not in Live 1, 1.1.18 client
    811, Terrier Pet, 1.1.18 client
    812, Random unused pet, 1.1.18 client
    813, bunny - not used, 1.1.18 client
    814, Doberman Pet, 1.1.18 client
    815, Buffalo Pet, 1.1.18 client
    816, Robot Dog Pet, 1.1.18 client
    817, Not Used, 1.1.18 client
    818, European Dragon Pet, 1.1.18 client
    819, Tortoise Pet, 1.1.18 client
    820, Asian Dragon pet, 1.1.18 client
    821, Mantis Pet, 1.1.18 client
    822, Panda Pet, 1.1.18 client
    823, Warthog Pet, 1.1.18 client
    824, Crab Pet, 1.1.18 client
    825, Lion Pet, 1.1.18 client
    826, Crocodile Pet, 1.1.18 client
    827, Goat Pet, 1.1.18 client
    828, Coalessa's lion Cant Tame, 1.1.18 client
    1001, AG Space Ship Binoc at launch, 1.1.18 client
    1002, AG Space Ship Binoc at launch platform, 1.1.18 client
    1003, AG Space Ship Binoc on platform to left of start, 1.1.18 client
    1004, AG Space Ship Binoc on platform to right of start, 1.1.18 client
    1005, AG Space Ship Binoc at Bob, 1.1.18 client
    1101, AG Battle Binoc for triceretops, 1.1.18 client
    1102, AG Battle Binoc at Paradox, 1.1.18 client
    1103, AG Battle Binoc at mission giver, 1.1.18 client
    1104, AG Battle Binoc at Beck, 1.1.18 client
    1105, AG Monument Binoc Intro, 1.1.18 client
    1106, AG Monument Binoc Outro, 1.1.18 client
    1107, AG Launch Binoc Intro, 1.1.18 client
    1108, AG Launch Binoc Bison, 1.1.18 client
    1109, AG Launch Binoc Shark, 1.1.18 client
    1201, NS Binoc Concert Transition, 1.1.18 client
    1202, NS Binoc Race Place Transition, 1.1.18 client
    1203, NS Binoc Brick Annex Transition, 1.1.18 client
    1204, NS Binoc GF Launch, 1.1.18 client
    1205, NS Binoc FV Launch, 1.1.18 client
    1206, NS Binoc Brick Annex Water, 1.1.18 client
    1207, NS Binoc AG Launch at Race Place, 1.1.18 client
    1208, NS Binoc AG Launch at Brick Annex, 1.1.18 client
    1209, NS Binoc AG Launch at Plaza, 1.1.18 client
    1210, NS Binoc TBA, 1.1.18 client
    1211, NS Binoc in Brick Annex looking at Pet Rock, 1.1.18 client
    1212, NS Flag Collectable 2 - under concert bridge, 1.1.18 client
    1213, NS Flag Collectable 3 - by FV launch, 1.1.18 client
    1214, NS Flag Collectable 4 - in plaza behind building, 1.1.18 client
    1215, NS Flag Collectable 5 - by GF launch, 1.1.18 client
    1216, NS Flag Collectable 6 - by Duck SG, 1.1.18 client
    1217, NS Flag Collectable 7 - by LUP launch, 1.1.18 client
    1218, NS Flag Collectable 8 - by NT luanch, 1.1.18 client
    1219, NS Flag Collectable 9 - by race build, 1.1.18 client
    1220, NS Flag Collectable 10 - on AG launch path, 1.1.18 client
    1221, NS Binoc TBA, 1.1.18 client
    1251, PR Binoc at launch pad, 1.1.18 client
    1252, PR Binoc at beginning of island B, 1.1.18 client
    1253, PR Binoc at first pet bouncer, 1.1.18 client
    1254, PR Binoc on by crows nest, 1.1.18 client
    1261, PR Pet Dig at beginning of Island B, 1.1.18 client
    1262, PR Pet Dig at the location of old bounce back, 1.1.18 client
    1263, PR Pet Dig under QB bridge, 1.1.18 client
    1264, PR Pet Dig back side by partner bounce, 1.1.18 client
    1265, PR Pet Dig by launch pad, 1.1.18 client
    1266, PR Pet Dig by first pet bouncer, 1.1.18 client
    1301, GF Binoc on Landing pad, 1.1.18 client
    1302, GF Binoc at Ravine Start, 1.1.18 client
    1303, GF Binoc on top of Ravine Head, 1.1.18 client
    1304, GF Binoc at Turtle Area, 1.1.18 client
    1305, GF Binoc in tunnel to Elephants, 1.1.18 client
    1306, GF Binoc in Elephants area, 1.1.18 client
    1307, GF Binoc in racing area, 1.1.18 client
    1308, GF Binoc in croc area, 1.1.18 client
    1309, GF Binoc in jail area, 1.1.18 client
    1310, GF Binoc telescope next to captain jack, 1.1.18 client
    1401, FV Binoc at the gate, 1.1.18 client
    1402, FV Binoc at the tree, 1.1.18 client
    1403, FV Binoc in the tree, 1.1.18 client
    1404, FV Binoc at Panda Paw, 1.1.18 client
    1405, FV Binoc at the tree (behind), 1.1.18 client
    1406, FV Binoc looking at Brick Fury, 1.1.18 client
    1407, FV Binoc above the facility, 1.1.18 client
    1408, FV Binoc looking up the cliff, 1.1.18 client
    1409, FV Binoc at the facility, 1.1.18 client
    1410, FV Binoc at the dragon crevice, 1.1.18 client
    1601, LUP Station Binoc 1, 1.1.18 client
    1602, LUP Station Binoc 2, 1.1.18 client
    1900, :zone:`Nexus Tower <1900>` needs no more bricks to be finished, :doc:`../database/Preconditions`
    11001, SS Plaque 1, 1.1.18 client
    11002, SS Plaque 2, 1.1.18 client
    11003, SS Plaque 3, 1.1.18 client
    11101, AG Plaque 1, 1.1.18 client
    11102, AG Plaque 2, 1.1.18 client
    11103, AG Plaque 3, 1.1.18 client
    11104, AG Plaque 4, 1.1.18 client
    11105, AG Plaque 5, 1.1.18 client
    11201, NS Plaque 1, 1.1.18 client
    11202, NS Plaque 2, 1.1.18 client
    11203, NS Plaque 3, 1.1.18 client
    11204, NS Plaque 4, 1.1.18 client
    11205, NS Plaque 5, 1.1.18 client
    11301, GF Plaque 1, 1.1.18 client
    11302, GF Plaque 2, 1.1.18 client
    11303, GF Plaque 3, 1.1.18 client
    11304, GF Plaque 4, 1.1.18 client
    11305, GF Plaque 5, 1.1.18 client
    11401, FV Plaque 1, 1.1.18 client
    11402, FV Plaque 2, 1.1.18 client
    11403, FV Plaque 3, 1.1.18 client
    11404, FV Plaque 4, 1.1.18 client
    11405, FV Plaque 5, 1.1.18 client
    11406, FV Plaque 6, 1.1.18 client
    11407, FV Plaque 7, 1.1.18 client
    11501, PC Plaque 1, 1.1.18 client
    11502, PC Plaque 2, 1.1.18 client