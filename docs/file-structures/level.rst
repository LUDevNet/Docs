Level (.lvl)
^^^^^^^^^^^^

.. note ::

	* It seems the structure is split in chunks marked by “CHNK”, somewhat similar to the IFF file format
	* It seems Chunks can only begin on addresses % 16 == 0, if the chunk wouldn’t start on one padding is inserted until it matches 
	* Padding always seems to be the 0xcd byte, but that’s probably just a side effect of not writing data to it

.. kaitai:: ../res/lu_formats/files/lvl.ksy

Old Format
""""""""""

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
| **[Chunk 2001 (Objects) Structure]**
