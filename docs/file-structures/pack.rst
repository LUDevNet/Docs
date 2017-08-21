Pack (.pk)
^^^^^^^^^^
| **[L\:7]** - header info (are the last 3 bytes part of it?), seems to be always [‘n’-‘d’-‘p’-‘k’-01-ff-00]
| **[L:V+5]**\*#Files: - raw file data
| 	it seems that every packed file is always terminated with [ff-00-00-dd-00] (obviously not part of the packed file but the pk structure)
| **[u32]** - number of records (and with that, number of files packed in the pk file)
| 	**[s32]** - pk index
| 	**[s32]** - index of a binary tree node (-1 for no child, root node is [number of records] / 2)
| 	**[s32]** - index of a binary tree node (-1 for no child, root node is [number of records] / 2)
| 	**[u32]** - original file size
| 	**[L:32]** - md5 hash of original file, string
| 	**[L:4]** - ??? (could be padding caused by a possible null character of the previous string?)
| 	**[u32]** - compressed file size
| 	**[L:32]** - md5 hash of compressed file, string
| 	**[L:4]** - ??? (could be padding caused by a possible null character of the previous string?)
| 	**[u32]** - pointer to file data in the pk file, u32
| 	**[bool]** - flag whether packed file is compressed or not
| 		(if true the packed data should match with the compressed size/hash)
| 	**[L:3]** - ???
| **[u32]** - pointer to [number of records] in the pk file
| 	(only reliable way to obtain useful info about the pk file?)
| **[u32]** - ???
