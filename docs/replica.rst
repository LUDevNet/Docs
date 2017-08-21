Replica Packets
=============== 

.. note ::
	This is a read-the-docs port of the original google docs `lu_replica_packets <https://docs.google.com/document/d/1V_yhtj91QG0VBfMnmD5zC44DXwCRqjbBN98HoXXC7qs>`_, written by humanoid, lcdr and others, ported by `@Xiphoseer <https://twitter.com/Xiphoseer>`_. This is currently a proof of concept and is not guaranteed to reflect the latest changes.

.. note ::
	- most structures can be omitted if they are optional, so you do not have to implement everything
	- grey colored structs didn’t occur in a packet yet
	- for investigations in raw replica packets, an advanced hex editor that can do bit operations on the data is very much recommended since there tend to be a lot of bit shifts in one packet
	- a sample packet viewer is provided at https://bitbucket.org/lcdr/utils/src captureviewer.pyw (needs the client database converted as per fdb_to_sqlite.py)
	- the original server seems to have used the first iteration of RakNet’s Replica(Manager) class instead of the second one (as evidenced by the structure of the Construction header), so the Replica2 and ReplicaManager2 classes should not be used to emulate the original traffic

Packet composition
------------------

**[0x24]** - Replica Manager Construction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[bit]** - flag (automatically added by the replica manager)
| **[u16]** - networkID (automatically created and added by the replica manager)
| **[base data]**

**[0x27]** - Replica Manager Serialization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u16]** - networkID
| 	(you can use this to identify which object it is by finding the creation packet and looking up the LOT)
| **[base data]**

**[0x25]** - Replica Manager Destruction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u16]** - networkID, didn’t come across a packet that contained more data than this

Base Data ($+731C30)
^^^^^^^^^^^^^^^^^^^^
seems to be included for every object

| *Creation only*
| **[s64]** - objectID
| **[s32]** - LOT
| **[u8]** - wstring length (# of letters)
| 	Note: even though this technically allows long strings, the client has a bug which only allocates 32 wchars. Never use names longer than 32 wchars, otherwise your client will crash.
|	**[wchar_t]** - name
| **[u32]** - time_since_created_on_server?
| **[bit]** - flag
| 	**[u32]** - size of following struct
| 		**[x]** - compressed data, x bytes according to prev struct

contains LDF with the following keys and data formats:
	- blueprintid: 9
	- componentWhitelist: 1
	- modelBehaviors: 5
	- modelType: 1
	- propertyObjectID: 7
	- userModelID: 9

Note: this also can contain a script, like for example on pets, to whitelist specific components.

| **[bit]** - trigger_id (even though the name says id it’s a bool…)
| 	Seems like this being true causes a new replica index to be appended, see trigger component below
| **[bit]** - flag
| 	**[s64]** - objectID of the spawner object
| 		needed, for example, by bouncers because they need to know what bounce power they have which they parse from the lvl files and they look for the spawnerID to identify the object
| **[bit]** - flag
| 	**[u32]** - spawner_node_id
| **[bit]** - flag
| 	**[float]** - object scale
| **[bit]** - flag
| 	**[u8]** - objectWorldState?
| **[bit]** - flag
| 	**[u8]** - gmlevel?
| 		You can parse the gmlevel from the LVL Files if you want. Since this never appeared in the packets so far it then is optional
| *End of Creation only*
|
| **[bit]** - flag
| **[bit]** - flag
| **[s64]** - parent? object id
| **[bit]** - ???
| **[bit]** - flag
| **[u16]** - count
| **[s64]** - child? objects ids
| **[component serialization data]**

Component serialization
-----------------------

Introduction
^^^^^^^^^^^^
- Every object consists of components, which define its behavior (e.g. RenderComponent means that the object should be rendered and is visible in the game).
- Like the general object data, components have data that needs to be broadcast to every player (e.g. health value for DestructibleComponent) which is serialized.
- Components consist of indices (inofficial name) which allow structures to be broken up further and to be reused (e.g. DestructibleComponent consists of the general destructible index and the stats index, which handles object stats like health, armor and imagination. This stats index is also used by the Collectible and Rebuild components.)
- If an object has for example both Destructible and Collectible indices, the stats index is “shared”, that is, the second occurrence is removed and both Destructible and Collectible take their information from this single remaining stats index. This prevents redundancy and saves network bandwidth.
- As with game messages, not all components are used in network traffic but internally within the client. The non-networked ones are of no use in this documentation but for completeness sake we’ll list the ones that we could identify so far as well (ids only)


Component List (networked)
^^^^^^^^^^^^^^^^^^^^^^^^^^
In the following the components and the indices they use are listed, in the format
``[cdclient id] <Component name>: Index names``.


The order in which they are listed are the order they are serialized. Make sure to write the components in this order (omitting components that are not listed for the according object in the cdclient database of course), otherwise the client will not be able to read them.

- **[108]** ???: Component 108
- **[61]** ModuleAssembly: ModuleAssembly
- **[1]** ControllablePhysics: ControllablePhysics
- **[3]** SimplePhysics: SimplePhysics
- **[20]** RigidBodyPhantomPhysics: RigidBodyPhantomPhysics
- **[30]** VehiclePhysics: VehiclePhysics
- **[40]** PhantomPhysics: PhantomPhysics
- **[7]** Destructible: Destructible, Stats
- **[23]** Collectible: Stats, Collectible
- **[26]** Pet: Pet
- **[4]** Character: Character (Part 1-4)
- **[17]** Inventory: Inventory
- **[5]** Script: Script
- **[9]** Skill: Skill
- **[60]** BaseCombatAI: BaseCombatAI
- **[48]** Rebuild: Stats, Rebuild
- **[25]** Moving Platform: Moving Platform
- **[49]** Switch: Switch
- **[16]** Vendor: Vendor
- **[6]** Bouncer: Bouncer
- **[39]** ScriptedActivity: ScriptedActivity
- **[71]** RacingControl: RacingControl
- **[75]** Exhibit: Exhibit
- **[42]** Model: Model
- **[2]** Render: Render
- **[107]** ???: Component 107
- **[69]** Trigger: Trigger

Example
"""""""
An object with ControllablePhysics and Destructible components has the following indices in this order:

- ControllablePhysics
- Destructible
- Stats

Component List (non-networked)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
12, 31, 35, 36, 45, 55, 56, 64, 65, 68, 73, 104, 113, 114

- 61 = AssemblyComponent


Index serialization data
------------------------

Collectible (todo: address)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u16]** - Collectible ID (can be parsed from LVL files)


Bouncer ($+7D6620)
^^^^^^^^^^^^^^^^^^
| **[bit]** - flag
| 	**[bit]** - petNotRequired????


Component 107 ($+7D6690)
^^^^^^^^^^^^^^^^^^^^^^^^
| **[bit]** - flag
| 	**[s64]** - ???


RigidBodyPhantomPhysics ($+7D90C0)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[bit]** - flag
| 	**[float]** - position x
| 	**[float]** - position y
| 	**[float]** - position z
| 	**[float]** - rotation x
| 	**[float]** - rotation y
| 	**[float]** - rotation z
| 	**[float]** - rotation w


Character
^^^^^^^^^
Part 1 ($+7DBCE0)
"""""""""""""""""
| **[bit]** - flag
| 	**[bit]** - flag
| 		**[s64]** - driven vehicle object id
| 	**[u8]** - ???

Part 2 ($+863BD0)
"""""""""""""""""
| **[bit]** - flag
| 	**[u32]** - level

Part 3 ($+7DC480)
"""""""""""""""""
| **[bit]** - flag
| 	**[bit]** - ???
| 	**[bit]** - ???

Part 4 ($+8A3A40)
"""""""""""""""""
| *Creation only*
| **[bit]** - flag
| 	**[u64]** - ???, could be “co” from xml data
| **[bit]** - flag
| 	**[u64]** - ???
| **[bit]** - flag
| 	**[u64]** - ???
| **[bit]** - flag
| 	**[u64]** - ???
| **[u32]** - hair color (“hc” from xml data)
| **[u32]** - hair style (“hs” from xml data)
| **[u32]** - ???, could be “hd” or “hdc” from xml data
| **[u32]** - shirt color (“t” from xml data)
| **[u32]** - pants color (“l” from xml data)
| **[u32]** - ???, could be “cd” from xml data
| **[u32]** - ???, could be “hdc” or “hd” from xml data
| **[u32]** - eyebrows style (“es” from xml data)
| **[u32]** - eyes style (“ess” from xml data)
| **[u32]** - mouth style (“ms” from xml data)
| **[u64]** - accountID (in xml data and chardata packet)
| **[u64]** - “llog” from xml data
| **[u64]** - ???
| **[u64]** - lego score (from xml data)
| **[bit]** - is player free to play
| *the following 27 structs are stats table values (“stt” from xml data)*
| **[u64]** - Total Amount of Currency Collected
| **[u64]** - Number of Bricks Collected
| **[u64]** - Number of smashables smashed
| **[u64]** - Number of Quick Builds Completed
| **[u64]** - Number of enemies smashed
| **[u64]** - Number of Rockets used
| **[u64]** - Number of missions completed
| **[u64]** - Number of Pets tamed
| **[u64]** - Number of Imagination power-ups collected
| **[u64]** - Number of Life Power-Ups Collected
| **[u64]** - Number of Armor power-ups collected
| **[u64]** - Total Distance Traveled (in meters)
| **[u64]** - Number of times smashed
| **[u64]** - Total damage taken
| **[u64]** - Total damage Healed
| **[u64]** - Total Armor Repaired
| **[u64]** - Total Imagination Restored
| **[u64]** - Total Imagination used
| **[u64]** - Total Distance Driven (in meters)
| **[u64]** - Total Time Airborne in a Race Car (in seconds)
| **[u64]** - Number of Racing Imagination power-ups collected
| **[u64]** - Number of Racing Imagination Crates Smashed
| **[u64]** - Number of Times Race Car Boost Activated
| **[u64]** - Number of Wrecks in a Race Car
| **[u64]** - Number of Racing Smashables smashed
| **[u64]** - Number of Races finished
| **[u64]** - Number of 1st Place Race Finishes
| **[bit]** - ???, flag for data?
| **[bit]** - is player landing by rocket
| 	**[u16]** - count of characters
| 		**[wchar_t]** - LDF info of rocket modules, sample: “1:9746;1:9747;1:9748;”
| *End of Creation only*
| **[bit]** - flag
| 	**[bit]** - flag for data?
| 	**[bit]** - ???
| 	**[u8]** - ???
| 	**[bit]** - ???
| 	**[u8]** - ???
| **[bit]** - flag
| 	**[u32]** - if this is 1 the character's head glows
| **[bit]** - flag (this and below was in a separate function in the code)
| 	**[s64]** - ???
| 	**[u8]** - ??? (count for next struct?)
| 	**[bit]** - ???
| 	**[s32]** - ???


Component 108 ($+7DC1F0)
^^^^^^^^^^^^^^^^^^^^^^^^
(something vehicle related)

| **[bit]** - flag
| 	**[bit]** - flag
| 		**[s64]** - driver object id
| 	**[bit]** - flag
| 		**[u32]** - ???
| 	**[bit]** - ???


Vendor ($+7E1CB0)
^^^^^^^^^^^^^^^^^
| **[bit]** - flag
| 	**[bit]** - ???
| 	**[bit]** - ???


SimplePhysics ($+7E4B00)
^^^^^^^^^^^^^^^^^^^^^^^^
| *Creation only*
| **[bit]** - ???
| **[float]** - ???
| *End of Creation only*
| **[bit]** - flag
| 	**[float]** - ???
| 	**[float]** - ???
| 	**[float]** - ???
| 	**[float]** - ???
| 	**[float]** - ???
| 	**[float]** - ???
| **[bit]** - flag
| 	**[u32]** - ???
| **[bit]** - flag
| 	**[float]** - position x
| 	**[float]** - position y
| 	**[float]** - position z
| 	**[float]** - rotation x
| 	**[float]** - rotation y
| 	**[float]** - rotation z
| 	**[float]** - rotation w


VehiclePhysics ($+7FD4D0)
^^^^^^^^^^^^^^^^^^^^^^^^^
| **[Part read by $+7F5A10]**
| 	seems $+7F5A10 is also called for ControllablePhysicsComponent and is the part that gets included in position update packets?
| *Creation only*
| **[u8]** - ???
| **[bit]** - ???
| *End of Creation only*
| **[bit]** - flag
| 	**[bit]** - ???


Skill ($+806270)
^^^^^^^^^^^^^^^^
| *Creation only*
| **[bit]** - flag
| 	**[u32]** - count for following structs
| 		**[u32]** - ???
| 		**[u32]** - ???
| 		**[u32]** - ???
| 		**[u32]** - ???
| 		**[u32]** - count for following structs
| 			**[u32]** - ???
| 			**[u32]** - ???, seems to be something in BehaviorTemplate?
| 			**[u32]** - ???
| 			**[u32]** - ???, always 18?
| 			**[s64]** - ???, always the objectID of the minifig so far?
| 			**[s64]** - ???, always the objectID of the minifig so far?
| 			**[s64]** - ???, always 0?
| 			**[bit]** - ???, always 0?
| 			**[float]** - ???, always 0?
| 			**[u32]** - ???, always 0?
| 			**[u32]** - ???, always 0?
| *End of Creation only*


Switch ($+80EBF0)
^^^^^^^^^^^^^^^^^
| **[bit]** - since this is a switch it’s likely it’s the switch state (on/off)


BaseCombatAI ($+824290)
^^^^^^^^^^^^^^^^^^^^^^^
| **[bit]** - flag
| 	**[u32]** - action? 0 = nothing; 1=attacking; 2=releasing; 3=?;??
| 	**[s64]** - target objectID (Probably causes projectiles fired by the enemy to seek the target client sided)


PhantomPhysics ($+834DB0)
^^^^^^^^^^^^^^^^^^^^^^^^^
| **[bit]** - flag
| 	**[float]** - position x
| 	**[float]** - position y
| 	**[float]** - position z
| 	**[float]** - rotation x
| 	**[float]** - rotation y
| 	**[float]** - rotation z
| 	**[float]** - rotation w
| **[bit]** - flag
| 	**[bit]** - is physics effect active
| 		**[u32]** - physics effect type
| 		**[float]** - physics effect amount
| 		**[bit]** - flag
| 			**[u32]** - ???
| 			**[u32]** - ???
| 		**[bit]** - flag
| 			**[float]** - physics effect direction x * effect amount
| 			**[float]** - physics effect direction y * effect amount
| 			**[float]** - physics effect direction z * effect amount


Render ($+840310)
^^^^^^^^^^^^^^^^^
| *Creation only*
| **[u32]** - number of currently active FX effects
| 	**[u8]** - string length (# of letters)
| 		**[char]** - effect name
| 	**[u32]** - effect ID
| 	**[u8]** - wstring length (# of letters)
| 		**[wchar]** - effect type
| 	**[float]** - scale or priority?
| 	**[s64]** - secondary?
| *End of Creation only*


ControllablePhysics ($+845770)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| *Creation only*
| **[bit]** - flag, related to jetpack?
| 	**[u32]** - jetpack effect id
| 	**[bit]** - ???
| 	**[bit]** - ???
| **[bit]** - flag
| 	**[u32]** - ???
| 	**[u32]** - ???
| 	**[u32]** - ???
| 	**[u32]** - ???
| 	**[u32]** - ???
| 	**[u32]** - ???
| 	**[u32]** - ???
| *End of Creation only*
| **[bit]** - flag
| 	**[float]** - ???
| 	**[float]** - ???
| **[bit]** - flag
| 	**[u32]** - ???
| 	**[bit]** - ???
| **[bit]** - flag
| 	**[bit]** - flag
| 		**[u32]** - ???
| 		**[bit]** - ???
| **[bit]** - flag
| *The structures below are in 53-04-00-16 position update (excluding the serialization only part)*
| 	**[float]** - player pos x
| 	**[float]** - player pos y
| 	**[float]** - player pos z
| 	**[float]** - player rotation x (or z)
| 	**[float]** - player rotation y
| 	**[float]** - player rotation z (or x)
| 	**[float]** - player rotation w
| 	**[bit]** - is player on ground
| 	**[bit]** - ???
| 	**[bit]** - flag
| 		**[float]** - velocity x
| 		**[float]** - velocity y
| 		**[float]** - velocity z
| 	**[bit]** - flag
| 		**[float]** - angular velocity x
| 		**[float]** - angular velocity y
| 		**[float]** - angular velocity z
| 	**[bit]** - flag
| 		Seems like this is sent when on a moving platform?
| 		**[s64]** - ???, seemed like an object id in the 53-04-00-16 captures
| 		**[float]** - ???
| 		**[float]** - ???
| 		**[float]** - ???
| 		**[bit]** - flag
| 			**[float]** - ???
| 			**[float]** - ???
| 			**[float]** - ???
| 	*Serialization only*
| 	**[bit]** - flag for data?
| 	*End of Serialization only*

Exhibit ($+863790)
^^^^^^^^^^^^^^^^^^
| **[bit]** - flag
| 	**[s32]** - exhibited LOT

Script ($+87CDF0)
^^^^^^^^^^^^^^^^^
| *Creation only*
| **[bit]** - flag
| 	**[same structure as the chardata packet]**
| *End of Creation only*


Pet ($+8D1270)
^^^^^^^^^^^^^^
| **[bit]** - flag
| 	**[u32]** - ???
| 	**[u32]** - ???
| 	**[bit]** - flag
| 		**[s64]** - ???
| 	**[bit]** - flag
| 		**[s64]** - Owner Object ID
| 	**[bit]** - flag
| 		**[u32]** - petModerationStatus?
| 		**[u8]** - length
| 			**[u16]** - Pet Name
| 		**[u8]** - length
| 			**[u16]** - Owner Name


ScriptedActivity ($+9002B0)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[bit]** - flag
| 	**[u32]** - count 
| 		**[u64]** - Player Object ID
| 		// constant size 10 loop
| 		*These seem to be custom parameters based on the activity (e.g. score in survival)*
| 		**[float]** - ???
| 		**[float]** - ???
| 		**[float]** - ???
| 		**[float]** - ???
| 		**[float]** - ???
| 		**[float]** - ???
| 		**[float]** - ???
| 		**[float]** - ???
| 		**[float]** - ???
| 		**[float]** - ???


Rebuild ($+90AE10)
^^^^^^^^^^^^^^^^^^
| **[Scripted Activity structures]**
| **[bit]** - flag
| 	**[u32]** - rebuild state
| 		open = 0
| 		completed = 2
| 		resetting = 4
| 		building = 5
| 		incomplete = 6
| 	**[bit]** - success
| 	**[bit]** - enabled
| 	**[float]** - time since start of rebuild
| 	**[float]** - a time related to paused rebuilds?
| *Creation only*
| 	**[bit]** - ???
| 		**[u32]** - ???
| 	**[float]** - Build Activator position X
| 	**[float]** - Build Activator position Y
| 	**[float]** - Build Activator position Z
| 	**[bit]** - ???
| *End of Creation only*


ModuleAssembly ($+913F30)
^^^^^^^^^^^^^^^^^^^^^^^^^
| *Creation only*
| **[bit]** - flag
| 	**[bit]** - flag
| 		**[s64]** - ???
| 	**[bit]** - ???
| 	**[u16]** - wstring length
| 		**[wchar_t]** - ???
| *End of Creation only*


Stats ($+92BBD0)
^^^^^^^^^^^^^^^^
| *Creation only*
| **[bit]** - flag
| 	**[u32]** - ???
| 	**[u32]** - ???
| 	**[u32]** - ???
| 	**[u32]** - ???
| 	**[u32]** - ???
| 	**[u32]** - ???
| 	**[u32]** - ???
| 	**[u32]** - ???
| 	**[u32]** - ???
| *End of Creation only*
| **[bit]** - flag
| 	**[u32]** - current health
| 	**[float]** - ??? (same number as max health but changing it had no effect)
| 	**[u32]** - current armor
| 	**[float]** - ??? (same number as max armor but changing it had no effect)
| 	**[u32]** - current imagination
| 	**[float]** - ??? (same number as max imagination but changing it had no effect)
| 	**[u32]** - ???
| 	**[bit]** - ???
| 	**[bit]** - ???
| 	**[bit]** - ???
| 	**[float]** - max health
| 	**[float]** - max armor
| 	**[float]** - max imagination
| 	**[u32]** - count
| 		**[s32]** - faction id
| 	trigger=**[bit]** - is smashable
| *Creation only*
| 	**[bit]** - flag for data?
| 	**[bit]** - flag for data?
| 	**[trigger]**
| 		**[bit]** - ???
| 		**[bit]** - flag
| 			**[u32]** - ???
| *End of Creation only*
| **[bit]** - flag
| 	**[bit]** - ???


Destructible ($+939820)
^^^^^^^^^^^^^^^^^^^^^^^
| *Creation only*
| **[bit]** - flag
| 	**[u32]** - count for following structs
| 		**[u32]** - ???
| 		**[bit]** - flag
| 			**[u32]** - ???
| 		**[bit]** - ???
| 		**[bit]** - ???
| 		**[bit]** - ???
| 		**[bit]** - ???
| 		**[bit]** - ???
| 		**[bit]** - ???
| 		**[bit]** - ???
| 		**[bit]** - ???
| 		trigger=**[bit]** - ???, seems to toggle **[s64]** below?
| 		**[bit]** - ???
| 		if trigger:
| 			**[s64]** - ???
| 		**[u32]** - ???
| *End of Creation only*


Moving Platform
^^^^^^^^^^^^^^^
| flag=**[bit]** - flag
| **[bit]** - flag
| 	**[bit]** - ???
| 		**[u16-wstring]** - path name
| 		**[u32]** - ???
| 		**[bit]** - ???
| if flag:
| 	**[bit]** - ???
| 		subcomponent_type=**[u32]** - subcomponent type, 4 - mover, 5 - simple mover?
| 		if subcomponent_type == 4:
| 			**[bit]** - ???
| 				**[u32]** - state
| 				**[s32]** - ???
| 				**[bit]** - ???
| 				**[bit]** - based on this and some other criteria some other things are also included?
| 				**[float]** - ???
| 
| 				**[float]** - target position x
| 				**[float]** - target position y
| 				**[float]** - target position z
| 
| 				**[u32]** - current waypoint index
| 				**[u32]** - next waypoint index
| 
| 				**[float]** - idle time elapsed
| 				**[u32]** - ???
| 		if subcomponent_type == 5:
| 			**[bit]** - flag
| 				**[bit]** - flag
| 					**[float]** - position x?
| 					**[float]** - position y?
| 					**[float]** - position z?
| 					**[float]** - rotation x?
| 					**[float]** - rotation y?
| 					**[float]** - rotation z?
| 					**[float]** - rotation w?
| 			**[bit]** - flag
| 				**[u32]** - ???
| 				**[u32]** - ???
| 				**[bit]** - ???


Racing Control ($+949620)
^^^^^^^^^^^^^^^^^^^^^^^^^
| *start of something*
| ScriptedActivity content here
| **[bit]** - flag
| 	**[u16]** - ???
| **[bit]** - flag
| 	while True:
| 		not_break=**[bit]** - flag
| 		if not not_break:
| 			break
| 		**[s64]** - player object id
| 		**[s64]** - car object id
| 		**[u32]** - ???
| 		**[bit]** - ???
| **[bit]** - flag
| 	while True:
| 		not_break=**[bit]** - flag
| 		if not not_break:
| 			break
| 		**[s64]** - player object id
| 		**[u32]** - ???
| *end of something*
| **[bit]** - flag
| 	**[u16]** - remaining laps?
| 	**[u16]** - length
| 		**[u16]** - path name
| **[bit]** - flag
| 	**[bit]** - flag
| 		**[s64]** - ???
| 		**[float]** - ???
| 		**[float]** - ???


Inventory ($+952860)
^^^^^^^^^^^^^^^^^^^^
| **[bit]** - flag
| 	**[u32]** - number of items equipped
| 		**[s64]** - objectID of item
| 		**[s32]** - LOT of item
| 		**[bit]** - flag
| 			**[s64]** - ???
| 		**[bit]** - flag
| 			**[u32]** - item count
| 		**[bit]** - flag
| 			**[u16]** - slot in inventory
| 		**[bit]** - flag
| 			**[u32]** - ???, always 4?
| 		**[bit]** - flag
| 			**[u32]** - size of following struct
| 				**[x]** - compressed data, x bytes according to prev struct
| 					contains LDF with the following keys and data formats:
| 					_Metric_Currency_Delta_Int: 1
| 					_Metric_Mail_ID_Int64: 8
| 					_Metric_Mission_ID_Int: 1
| 					_Metric_Souce_LOT_Int: 1
| 					_Metric_Transaction_ID_Int64: 9
| 					assemblyPartLOTs: 0
| 		**[bit]** - ???
| 			(perhaps a flag that specifies if the item gets loaded or if data needs to be retrieved from the cdclient database?)
| **[bit]** - flag
| 	**[u32]** - ??? (count for next struct?)


Trigger Component
^^^^^^^^^^^^^^^^^
Seems like this component is append when there is a trigger_id entry in the luz-lvl
See also documentation for lvl files
See also documentation for .lutriggers files

| **[bit]** - flag
| 	**[s32]** - trigger id

