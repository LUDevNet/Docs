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

.. kaitai:: ../res/lu_formats/files/fdb.ksy

.. note ::
	* Address pointers can be -1 which most likely means an invalid address (just skip those)
	* Strings types (TEXT and VARCHAR) are always null-terminated (with some over allocated bytes afterwards it seems, apparently string length are filled to be modulo 4 = 0?)
	* Strings and int64 (BIGINT) types are always stored with an additional address pointer, like this: [pointer]->[data]

SQLite Conversion
'''''''''''''''''

lcdr's tools rely on https://www.sqlite.org/datatype3.html#determination_of_column_affinity to assign the type
of columns in SQLite while preserving the original type:

.. code-block :: py

	SQLITE_TYPE = {}
	SQLITE_TYPE[0] = "none"
	SQLITE_TYPE[1] = "int32"
	SQLITE_TYPE[3] = "real"
	SQLITE_TYPE[4] = "text_4"
	SQLITE_TYPE[5] = "int_bool"
	SQLITE_TYPE[6] = "int64"
	SQLITE_TYPE[8] = "text_8"
