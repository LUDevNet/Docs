Database (.fdb)
^^^^^^^^^^^^^^^

You can use the tools collection from `assembly <https://crates.io/crates/assembly-data>`_ to work with FDB files.

.. note ::
	There is a converter from fdb to sqlite available, see the :ref:`tools` section. This file type has no relation to firebird database files of the same extension.

.. note ::
	It seems like:
		* Tables are sorted by their name in ascii representation. Uppercase letters then underscore then lowercase letters.
		* Tables themselves are hash maps. Use `id % row_count` to get the appropriate `row_info`, then follow the `linked_row_info` until all entries with that ID are found.
		* When the primary key is a string, a dedicated hash function is used to determin the index of the `row_info` slot.
		* Strings are stored spearately for each row, even if they have the same content. This makes for a great amount of redundancy in the file, but keeps editing simple.

| table_count= **[u32]** - number of tables
| **[u32]** - address pointer to table header in file

-> table header
"""""""""""""""

| **[table_count]**
| 	**[u32]** - address pointer to column header in file
| 	**[u32]** - address pointer to bucket header in file

-> column header
""""""""""""""""
| column_count= **[u32]** - number of columns
| **[L\:4]** - name of table, DATA_TYPE::TEXT
| **[u32]** - address pointer to column data in file

-> column data
""""""""""""""
| **[column_count]**
| 	**[u32]** - data type of column
| 	**[L\:4]** - name of column, DATA_TYPE::TEXT

-> bucket header
"""""""""""""""""
| bucket_count= **[u32]** - row count, an allocated number
| **[s32]** - address pointer to row header in file (-1 means invalid there are a lot of those)

-> row header
"""""""""""""
| **[bucket_count]**
| 	**[s32]** - address pointer to first row info in bucket

-> row info
"""""""""""
| **[s32]** - address pointer to row data header in file
| **[s32]** - address pointer to the next row info in bucket
| 	doesn’t count as a row in row_count and it seems that all rows with a key id greater than row_count get linked to the row with a key id modulo row_count, rows with the same key id also get linked together, otherwise this is an invalid pointer

-> row data header
""""""""""""""""""
| column_count= **[s32]**	number of columns (that’s right, this is included again for every row, what a waste of space)
| **[s32]** - address pointer to row data in file (finally)

-> row data
"""""""""""
| **[column_count]** - 
| 	**[s32]** - data type of column, s32
| 	**[s32]** - data, DATA_TYPE

.. todo :: Write some notes regarding the weird block allocation sizes for the structures

.. note :: Since our conventional format wasn’t exactly suited for documenting this format I introduced the “address following” which basically first gets defined by name in a structure description (as underlined text) and is afterwards mentioned whenever that address should be accessed in the file structure when parsing the structure (indicated by an arrow prefix to the underlined name)

.. note ::
	* Address pointers can be -1 which most likely means an invalid address (just skip those)
	* Strings types (TEXT and VARCHAR) are always null-terminated (with some over allocated bytes afterwards it seems, apparently string length are filled to be modulo 4 = 0?)
	* Strings and int64 (BIGINT) types are always stored with an additional address pointer, like this: [pointer]->[data]

.. code-block :: c

	enum DATA_TYPE {
	    NOTHING = 0,  // can’t remember if those are just skipped/ignored or even showed up
	    INTEGER,
	    UNKNOWN1,     // never used?
	    FLOAT,
	    TEXT,         // called STRING in MSSQL?
	    BOOLEAN, 
	    BIGINT,       // or DATETIME?
	    UNKNOWN2,     // never used?
	    VARCHAR       // called TEXT in MSSQL?
	};
