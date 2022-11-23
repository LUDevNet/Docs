Character Component (4)
-----------------------

This component does not have any client database table associated with it, as it
represents and manages the state of the character of some player. It holds information
such as the lego score (U-Score), account information and the passport statistics.

There is a very strange struct in the serialization, notably the `TransitionState` in the Character Component.
It is a 2 bit enum defined as the following:

| **[uint2_t]** - TransitionState
| if TransitionState == 1
|   **[uint16_t]** - lastCustomBuildParts (presumably the rocket they are arriving on)
|     **[wchar]** - wCharacterOfTheAboveString

Component Dependencies
......................

| :doc:`110-possession-control`
| :doc:`109-level-progression`
| :doc:`106-player-forced-movement`

Component Construction
......................

| :ref:`Possession Control <110-construction>`
| :ref:`Level Progression <109-construction>`
| :ref:`Player Forced Movement <106-construction>`
| :packet:`raknet/client/replica/character/struct.CharacterConstruction`

Component Serialization
.......................

| :ref:`Possession Control <110-serialization>`
| :ref:`Level Progression <109-serialization>`
| :ref:`Player Forced Movement <106-serialization>`
| :packet:`raknet/client/replica/character/struct.CharacterSerialization`

Character XML Format
....................

| :samp:`obj` - The root object of the data.
| :samp:`attr v` - Version? Always 1?
|   :samp:`buff` - Buffs applied to the player? CheekyMonkey's chardata contained this but was empty, while ShastaFantastic didn't have this element at all. If you find a sample that has more information, please add content.
|   :samp:`dest` - Destroyable info
|   :samp:`attr am` - Maximum armor
|   :samp:`attr ac` - Current armor
|   :samp:`attr d` - Dead?
|   :samp:`attr hc` - Current health
|   :samp:`attr hm` - Maximum health
|   :samp:`attr ic` - Current imagination
|   :samp:`attr im` - Maximum imagination
|   :samp:`attr imm` - Immunity?
|   :samp:`attr rsh` - ReSpawn Health
|   :samp:`attr rsi` - ReSpawn Imagination
|   :samp:`inv` - The inventory of the player. This is actually a collection of storage and does not only represent the backpack (e.g Vault items are also in here).
|   :samp:`attr csl` - LOT of the item in the consumable slot (“consumable slot lot”?)
|   :samp:`bag` - Storage containers.
|     :samp:`b` - A storage container
|     :samp:`attr m` - Size of the bag. (Maximum number of slots)
|     :samp:`attr t` - Type of the bag. :packet:`world/gm/enum.InventoryType`
|   :samp:`grps` - User Item groups. This is used to selectively display models or bricks.
|     :samp:`grp` - A group.
|     :samp:`attr id` - ID of the group. In the captures this was usually the literal string "user_group" and a unique number.
|     :samp:`attr l` - LOTs of the items in this group, separated by spaces.
|     :samp:`attr n` - Displayed name of the group
|     :samp:`attr t` - Type of the group. :packet:`world/gm/enum.InventoryType`
|     :samp:`attr u` - Unlocked?
|   :samp:`items` - The contents of the "bags"/storage containers. These don't actually have to be items, e.g models and bricks are listed here too.
|   :samp:`attr nn` - Unknown
|     :samp:`in` - Items in the storage container specified by the t attribute of this element.
|     :samp:`attr t` - Type of the bag. :packet:`world/gm/enum.InventoryType`
|       :samp:`i` - An item.
|       :samp:`attr b` - Boolean whether the item is bound. If it isn't, this attribute isn't there at all, if it is, it's set to 1.
|       :samp:`attr c` - Number of items for this stack of items.
|       :samp:`attr eq` - Boolean whether the item is equipped. If it isn't, this attribute isn't there at all, if it is, it's set to 1.
|       :samp:`attr id` - Object ID of the item.
|       :samp:`attr l` - LOT of the item. See cdclient for correct values.
|       :samp:`attr s` - Slot of the item. (0-indexed)
|       :samp:`attr sk` - Subkey of an item.  Generally this is how the client distinguishes items of the same LOT.  For example, custom behaviors use this value to distinguish themselves since all custom behaviors have the same LOT of 7965.
|         :samp:`x` - Extra LDF info.  Any of these can be left out if they do not apply to this item in the inventory. ex. pets do not need :samp:`ma` so dont need to save this ldfdata.
|         :samp:`attr b` - Unknown, an ObjectID of some kind.
|         :samp:`attr ma` - Module assembly info. U16string of signed 32 bit LOTS delimited by +
|         :samp:`attr ub` - UGC has behavior bool
|         :samp:`attr ud` - UGC description u16string
|         :samp:`attr ui` - Same as SubKey ObjId - only found 1 in a CheekyMonkey packet capture.  If more are found please confirm this.
|         :samp:`attr um` - userModelMod - int32_t
|         :samp:`attr un` - UGC? Name u16string
|         :samp:`attr uo`- UGC userModelOpt - bool
|         :samp:`attr up` - UGC physics type int32_t
|   :samp:`mf` - Minifig data
|   :samp:`attr cd` - Chest decal
|   :samp:`attr es` - Eyebrow style
|   :samp:`attr ess` - Eye style
|   :samp:`attr hc` - Hair color
|   :samp:`attr hd` - Head
|   :samp:`attr hdc` - Head color
|   :samp:`attr hs` - Hair style
|   :samp:`attr l` - Pants color
|   :samp:`attr lh` - Left hand
|   :samp:`attr ms` - Mouth style
|   :samp:`attr rh` - Right hand
|   :samp:`attr t` - Shirt color
|   :samp:`char` - Character data
|   :samp:`attr acct` - account ID
|   :samp:`attr cc` - Currency
|   :samp:`atrr cm` - Maximum Currency
|   :samp:`attr co` - Unknown
|   :samp:`attr edit` - Unknown, Maybe related to HF editor?
|   :samp:`attr ft` - FreeToPlay status?
|   :samp:`attr gid` - Guild ID
|   :samp:`attr gm` - GM level
|   :samp:`attr gn` - Guild name
|   :samp:`attr lcbp` - modular info of last used rocket
|   :samp:`attr llog` - Timestamp of last login as this character
|   :samp:`attr lrx` - Last respawn point position x
|   :samp:`attr lry` - Last respawn point position y
|   :samp:`attr lrz` - Last respawn point position z
|   :samp:`attr lrrw` - Last respawn point rotation w
|   :samp:`attr lrrx` - Last respawn point rotation x
|   :samp:`attr lrry` - Last respawn point rotation y
|   :samp:`attr lrrz` - Last respawn point rotation z
|   :samp:`attr ls` - Lego score/Universe score.
|   :samp:`attr lzcs` - Last Zone Check Sum, stored as an int32_t
|   :samp:`attr lzid` - The last zone clone ID, instance ID and zone ID concatenated into 1 64 bit number.
|   :samp:`attr lzrw` - Last world rotation w
|   :samp:`attr lzrx` - Last world rotation x
|   :samp:`attr lzry` - Last world rotation y
|   :samp:`attr lzrz` - Last world rotation z
|   :samp:`attr lzx` - Last world position x
|   :samp:`attr lzy` - Last world position y
|   :samp:`attr lzz` - Last world position z
|   :samp:`attr mldt` - "Prop mod last display time"
|   :samp:`attr stt` - Player stats. Stored as a string with each variable separated with “;”
|   :samp:`attr time` - Total time played, in seconds.
|   :samp:`attr ttip` - Unknown, always 16777216?
|   :samp:`attr v` - Unknown, maybe version?  Always 3 in caps
|   :samp:`attr vd` - Unknown, packet cap values are 15368, 15318, 15367
|     :samp:`ue` - Unlocked emotes.
|       :samp:`e` - An unlocked emote.
|       :samp:`attr id` - Emote ID.
|     :samp:`vl` - Visited worlds.
|       :samp:`l` - A visited world.
|       :samp:`attr cid` - Clone ID (used for properties, 0 if not a property)
|       :samp:`attr id` - World ID.
|     :samp:`zs` - World Statistics.
|       :samp:`s` - Statistics for a world
|       :samp:`attr ac` - Achievements collected
|       :samp:`attr bc` - Bricks collected
|       :samp:`attr cc` - Coins collected
|       :samp:`attr es` - Enemies smashed
|       :samp:`attr map` - ID of the world the statistics are for
|       :samp:`attr qbc` - Quick build count
|   :samp:`lvl` - Player level information
|   :samp:`attr cv` - Unknown
|   :samp:`attr l` - Base player level
|   :samp:`attr sb` - The base player speed
|   :samp:`flag` - The flags of the player.  A flag index is calculated as follows: flagId / 64.  The flags position at that index is calculated as follows: flagId % 64.
|     :samp:`f` - A flag value
|     :samp:`attr id` - The flag index
|     :samp:`attr v` - The flag index value
|     :samp:`s` - Unknown
|   :samp:`pet` - Pets of the player
|   :samp:`attr a` - Unknown, Always zero?
|     :samp:`p` - A pet
|     :samp:`attr id` - Pet ObjectID in storage container
|     :samp:`attr l` - Pet LOT
|     :samp:`attr m` - Moderation status (0 - denied, 1 - pending, 2 - approved)
|     :samp:`attr n` - Pet Name
|     :samp:`attr t` - Unknown, Always zero?
|   :samp:`mis` - Missions and Achievements
|     :samp:`cur` - Current missions and achievements
|       :samp:`m` - A currently active mission/achievement
|       :samp:`attr id` - ID of the mission/achievement
|       :samp:`attr o` - A missions spot in the UI.  The client needs this to know how to order missions in the tracker action script.  If this is not present / if there are duplicate values, the script will order by missionID.  With this value, the bigger it is, the farther right it goes in the list.
|         :samp:`sv` - Progress for a task. For achievements like collecting flags, there is one of this that has the displayed progress N, and N other sv elements that seem to have a bitflag in the id?
|         :samp:`attr v` - Value of the progress.
|     :samp:`done` - Completed missions and achievements
|       :samp:`m` - A completed mission/achievement
|       :samp:`attr cct` - Amount of times completed (this can be more than 1 for repeatable missions)
|       :samp:`attr cts` - Timestamp of last completion in seconds
|       :samp:`attr id` - ID of the mission/achievement
|     :samp:`ts` - Unknown
|       :samp:`type` - Unknown
|       :samp:`attr v` - Unknown, can be of values "", General, Play, Build
|         :samp:`st` - Unknown, A subType maybe?
|         :samp:`attr sub` - Unknown, Always the string equivalent of a zone name
|         :samp:`attr val` - Unknown, Always 1
|   :samp:`mnt` - Unknown, related to mounts?
|   :samp:`attr a` - Unknown, something related to last mounted item?
|   :samp:`skil` - Skills of the player? (What kind of skills, active ones? Why would they be saved? Action bar skills and skill uses are handled using different packets, so what would this be?) This was empty in the packet, if you find a sample that isn't empty please add content.
