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
| 	**[u32]** - ???, always 1?
| 	**[u32]** - count
| 		**[u32]** - path version
| 		**[u8]** - count
| 			**[wchar]** - path name
| 		**[u32]** - path type,
| 			0 = Movement,
| 			1 = Moving platform,
| 			2 = Property,
| 			3 = Camera,
| 			4 = Spawner,
| 			5 = Showcase,
| 			6 = Race,
| 			7 = Rail
| 		**[u32]** - ???
| 		**[u32]** - PathBehavior (0: Loop, 1: Bounce, 2: Once)
| 		if path type == 1:
| 			if path version >= 18:
| 				**[u8]** - ???
| 			elif path version >= 13:
| 				**[u8]** - count
| 					**[wchar]** - ???
| 		elif path type == 2:
|			**[s32]** - ???
| 			**[s32]** - ???
| 			**[s32]** - ???
| 			**[u64]** - ???
| 			**[u8]** - count
| 				**[wchar]** - ???
| 			**[u32]** - count
| 				**[wchar]** - ???
| 			**[s32]** - ???
| 			**[s32]** - ???
| 			**[float]** - ???
| 			**[s32]** - ???
| 			**[s32]** - ???
| 			**[float]** - ???
| 			**[float]** - ???
| 			**[float]** - ???
| 			**[float]** - ???
| 		elif path type == 3:
| 			**[u8]** - count
| 				**[wchar]** - ???
| 			if path version >= 14:
| 				**[u8]** - ???
| 		elif path type == 4:
| 			**[u32]** - spawned lot
| 			**[u32]** - ???
| 			**[s32]** - ???
| 			**[u32]** - ???
| 			**[s64]** - spawner object id, note that this does not get added bits in the captures
| 			**[u8]** - ???
| 		**[u32]** - count
| 			**[float]** - position x
| 			**[float]** - position y
| 			**[float]** - position z
| 			if path type == 1:
| 				**[float]** - rotation w
| 				**[float]** - rotation x
| 				**[float]** - rotation y
| 				**[float]** - rotation z
| 				**[u8]** - ???
| 				**[float]** - moveTime????
| 				**[float]** - idle Time????
| 				if path version >= 13:
| 					**[u8]** - count
| 						**[wchar]** - audioUUID???
| 					**[u8]** - count
| 						**[wchar]** - audioUUID???
| 				elif path type == 3:
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
|				elif path type == 4:
| 					**[float]** - rotation w
| 					**[float]** - rotation x
| 					**[float]** - rotation y
| 					**[float]** - rotation z
| 				elif path type == 6:
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[u8]** - ???
| 					**[u8]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 				elif path type == 7:
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					if path version >= 17:
| 						**[float]** - ???
| 				if path type in (0, 4, 7):
| 					**[u32]** - count
| 						**[u8]** - count
| 							**[wchar]** - config name
| 						**[u8]** - count
| 							**[wchar]** - config type and value
