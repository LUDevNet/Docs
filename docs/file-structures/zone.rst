Zone (.luz)
^^^^^^^^^^^

| **[u32]** - version number, always one of 0x24, 0x26, 0x27, 0x28, 0x29?
|	the file format differs depending on the version
| if version >= 0x24:
| 	**[u32]** - versioncontrol????
| **[u32]** - World ID
| if version >= 0x26:
| 	**[float]** - Spawnpoint position x
| 	**[float]** - Spawnpoint position y
| 	**[float]** - Spawnpoint position z
| 	**[float]** - Spawnpoint rotation x
| 	**[float]** - Spawnpoint rotation y
| 	**[float]** - Spawnpoint rotation z
| 	**[float]** - Spawnpoint rotation w
| **[if version < 0x25 u8, if version >= 0x25 u32]**: count of scenes
| 	**[u8]** - length
| 		**[char]** -filename
| 	**[u8]** - scene id?, length unclear
| 	**[L:3]** - ???, always == 0?
| 	**[u8]** - is audio scene?
| 	**[L:3]** - ???, always == 0?
| 	**[u8]** - length
| 		**[char]** - scene name
| 	**[L:3]** - seems to be skipped in code
| **[u8]** - ???, always == 0?
| **[u8]** - length
| 	**[char]** - map/terrain filename
| **[u8]** - length
| 	**[char]** - map/terrain name
| **[u8]** - length
| 	**[char]** - map/terrain description
| if version >= 0x20:
| 	**[u32]** - count of scene transitions
| 		if version < 0x25:
| 			**[u8]** - length
| 				**[char]** - scene transition name
| 		if version <= 0x21 or version >= 0x27:
| 			loop_times = 2
| 		else:
| 			loop_times = 5
| 		**[loop_times]**
| 			**[u64]** - scene id
| 			**[float]** - transition point position x
| 			**[float]** - transition point position y
|			**[float]** - transition point position z
| if version >= 0x23:
| 	**[u32]** - length of rest of file (everything after this) in bytes
| 		**[char]** - path data (see below)


Path Data
---------

| **[u32]** - ???, always 1?
| **[u32]** - count
| 	**[u32]** - path version
| 	**[u8]** - count
| 		**[wchar]** - path name
| 	**[u32]** - path type,
| 		0 = Movement,
| 		1 = Moving platform,
| 		2 = Property,
| 		3 = Camera,
| 		4 = Spawner,
| 		5 = Showcase,
| 		6 = Race,
| 		7 = Rail
| 	**[u32]** - ???
| 	**[u32]** - PathBehavior (0: Loop, 1: Bounce, 2: Once)
| 	if path type == 1:
| 		if path version >= 18:
| 			**[u8]** - ???
| 		elif path version >= 13:
| 			**[u8]** - count
| 				**[wchar]** - moving platform travel sound?
| 	elif path type == 2:
| 		**[s32]** - ???
| 		**[s32]** - price
| 		**[s32]** - rental time
| 		**[u64]** - associated zone
| 		**[u8]** - count
| 			**[wchar]** - display name
| 		**[u32]** - count
| 			**[wchar]** - display description
| 		**[s32]** - ???
| 		**[s32]** - clone limit
| 		**[float]** - reputation multiplier
| 		**[s32]** - rental time unit,
| 			0 = forever,
| 			1 = seconds,
| 			2 = minutes,
| 			3 = hours,
| 			4 = days,
| 			5 = weeks,
| 			6 = months,
| 			7 = years
| 		**[s32]** - achievement required
| 			0 = none,
| 			1 = builder,
| 			2 = craftsman,
| 			3 = senior builder,
| 			4 = journeyman,
| 			5 = master builder,
| 			6 = architect,
| 			7 = senior architect,
| 			8 = master architect,
| 			9 = visionary,
| 			10 = exemplar
| 		**[float]** - player zone coordinate x
| 		**[float]** - player zone coordinate y
| 		**[float]** - player zone coordinate z
| 		**[float]** - max building height
| 	elif path type == 3:
| 		**[u8]** - count
| 			**[wchar]** - next path
| 		if path version >= 14:
| 			**[u8]** - ???, boolean? Always either 0 or 1 so far?
| 	elif path type == 4:
| 		**[u32]** - spawned lot
| 		**[u32]** - respawn time
| 		**[s32]** - max to spawn (-1 for infinity)
| 		**[u32]** - number to maintain
| 		**[s64]** - spawner object id, note that this does not get added bits in the captures
| 		**[u8]** - activate spawner network on load
| 	**[u32]** - waypoint count
| 		**[float]** - position x
| 		**[float]** - position y
| 		**[float]** - position z
| 		if path type == 1:
| 			**[float]** - rotation w
| 			**[float]** - rotation x
| 			**[float]** - rotation y
| 			**[float]** - rotation z
| 			**[u8]** - lock player until next waypoint
| 			**[float]** - speed
| 			**[float]** - wait
| 			if path version >= 13:
| 				**[u8]** - count
| 					**[wchar]** - depart sound
| 				**[u8]** - count
| 					**[wchar]** - arrive sound
| 		elif path type == 3:
| 			**[float]** - ???
| 			**[float]** - ???
| 			**[float]** - ???
| 			**[float]** - ???
| 			**[float]** - time (seconds)
| 			**[float]** - ???
| 			**[float]** - tension
| 			**[float]** - continuity
| 			**[float]** - bias
| 		elif path type == 4:
| 			**[float]** - rotation w
| 			**[float]** - rotation x
| 			**[float]** - rotation y
| 			**[float]** - rotation z
| 		elif path type == 6:
| 			**[float]** - rotation w
| 			**[float]** - rotation x
| 			**[float]** - rotation y
| 			**[float]** - rotation z
| 			**[u8]** - ???
| 			**[u8]** - ???
| 			**[float]** - ???
| 			**[float]** - ???
| 			**[float]** - ???
| 		elif path type == 7:
| 			**[float]** - ???
| 			**[float]** - ???
| 			**[float]** - ???
| 			**[float]** - ???
| 			if path version >= 17:
| 				**[float]** - ???
| 		if path type in (0, 4, 7):
| 			**[u32]** - count
| 				**[u8]** - count
| 					**[wchar]** - config name
| 				**[u8]** - count
| 					**[wchar]** - config type and value