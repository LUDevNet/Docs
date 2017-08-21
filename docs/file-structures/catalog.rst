Catalog (.pki)
^^^^^^^^^^^^^^
| **[u32]** - version?, has to be 3
| **[u32]** - count
| 	**[u32]** - length
| 		**[char]** - pk filename, char
| 	**[u32]** - count
| 		**[s32]** - pk index (from pk file)
| 		**[s32]** - index of a binary tree node (-1 for no child, root node is [count] / 2)
| 		**[s32]** - index of a binary tree node (-1 for no child, root node is [count] / 2)
| 		**[u32]** - 0-based index of file in the file list above
| 		**[u32]** - mostly 268515584, sometimes 1
