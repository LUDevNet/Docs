Level (.lvl)
^^^^^^^^^^^^

.. todo ::

	* It seems the structure is split in chunks marked by “CHNK”, somewhat similar to the IFF file format
	* It seems Chunks can only begin on addresses % 16 == 0, if the chunk wouldn’t start on one padding is inserted until it matches 
	* Padding always seems to be the 0xcd byte, but that’s probably just a side effect of not writing data to it

Chunk Header
""""""""""""

| if **[L:4]** - ``CHNK`` in ascii :
| 	**[u32]** - chunk type, one of 1000, 2000, 2001, 2002 (see below)
| 	**[u16]** - ???
| 	**[u16]** - ???
| 	**[u32]** - Chunk length (starting from the ``CHNK``)
| 	**[u32]** - Address of start of data
| 		**[L:V]** - padding
| 	**[Chunk Structure as referred]**
| else: (Older file)
| **[L:265]** - ???
| **[std::string]** - skybox
| **[std::string]** - “(invalid)”
| **[std::string]** - “(invalid)”
| **[std::string]** - “(invalid)”
| **[std::string]** - “(invalid)”
| **[std::string]** - “(invalid)”
| **[L:4]** - ???
| **[u32]** - count
|	**[float]** - ???
| 	**[float]** - ???
| 	**[float]** - ???
| **[Chunk 2001 Structure]**

Chunk Type 1000
"""""""""""""""

| **[u32]** - lvl version?
| **[u32]** - ???
| **[u32]** - ???
| **[u32]** - ???
| **[u32]** - ???

Chunk Type 2000
"""""""""""""""

| **[u32]** - size of data
| 	**[u32]** - address of sky section
| 	**[u32]** - address of other section
| 	*the rest of this section seems to consist solely of floats (possibly always 25? Seems like it was 24 in beta, but could have also been 25)*
| 	**[float]** * ((size of data-8) / 4) - ???
| **[u32]** - id count?
| 	**[u32]** - id? (starting with 0? Looking at beta lvl files it could also start with 1)
| 	**[float]** - ???
| 	**[float]** - ???
| *Not sure if the rest of this section always consists of 2*3 floats (checked a few different lvl files), it’s very weird/inconsistent in the beta files though (at least for gnarled forest it seems like its 2*3 + 2*2 + 3 there, judging by their order of magnitude)*
| **[float]** * 3 - ???
| **[float]** * 3 - ???

**Sky section**

| **[u32]** - length
| 	**[char]** - filepath
| *the following filepaths are always “(invalid)”*
| **[u32]** - length
| 	**[char]** - filepath
| **[u32]** - length
| 	**[char]** - filepath
| **[u32]** - length
| 	**[char]** - filepath
| **[u32]** - length
| 	**[char]** - filepath
| **[u32]** - length
| 	**[char]** - filepath

**Other section**

| **[u32]** - length of following
| todo: investigate

Chunk Type 2001
"""""""""""""""

| **[u32]** - number of objects
| 	**[u64]** - object id, but some bits are missing
| 		-> these ids show up in the traffic (mostly for spawner LOTs but others as well with game messages) with the 46th bit enabled, I guess that bit means its a local object?
| 	**[s32]** - LOT
| 	if version >= 0x26:
| 		**[u32]** - ???, accepted values seem to be 0 to 10 inclusive?
| 	if version >= 0x20:
| 		**[u32]** - ???
| 	**[float]** - position x
| 	**[float]** - position y
| 	**[float]** - position z
| 	*Note: The w,x,y,z order here is different from the x,y,z,w order in the replica packets*
| 	**[float]** - rotation w
| 	**[float]** - rotation x
| 	**[float]** - rotation y
| 	**[float]** - rotation z
| 	**[float]** - scale
| 	**[u32]** - length
| 		**[wchar]**  - object settings variables in LDF format
| 			``spawntemplate``
| 				*describes the LOT to be spawned for Spawner objects, use the same position/rotation as Spawner object for those*
| 			``trigger_id``
| 				``scene_id:trigger_id``, *See also the documentation for .lutriggers files*
|	if version >= 7:
|		**[u32]** - ???, always == 0?

Chunk Type 2002
"""""""""""""""

.. todo :: investigate (seems to be related to environmental effects?)

