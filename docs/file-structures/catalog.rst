Catalog (.pki)
^^^^^^^^^^^^^^

.. note ::

	* The game had the majority of its data files packed in a custom dynamic archive. Within that system, each file was identified by the CRC-32 value of its filename relative to the installation root.
	* The crc value uses the standard CRC-32 polynomial `0x04C11DB7`, an init value of `0xFFFFFFFF`, no output XOR and reverses neither input nor output. The filenames are processed in lowercase, with Win32 ``\`` delimiters and a padding of 4 `0x00` bytes at the end.
	* Both filetypes include a representation of a binary tree for all their entries. The root node is always at ``size / 2``. Each entry has a field for a left and a right child entry. Both filetypes have their main entry list sorted by the crc value, making it possible to use binary search.

| **[u32]** - version?, has to be 3
| **[u32]** - count
| 	**[u32]** - length
| 		**[char]** - pk filename, char
| 	**[u32]** - count
| 		**[s32]** - crc of filename
| 		**[s32]** - index of left child (or -1)
| 		**[s32]** - index of right child (or -1)
| 		**[u32]** - 0-based index of file in the file list above
| 		**[u32]** - mostly 268515584, sometimes 1, sometimes something else (~ 20 possible values)
