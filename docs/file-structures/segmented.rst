Segmented (.sd0/.si0)
=====================

To download content as needed from the server while playing the game, LEGO introduced a
custom `segmented` file format. The actual files lived in :any:`ff-sd0` files, while the
compression process also generated :any:`ff-si0` files to be used when creating the :doc:`catalog`.

.. _ff-sd0:

Segmented Data (.sd0)
^^^^^^^^^^^^^^^^^^^^^

.. note :: There is a decompressor available, see the :any:`tools` section.

| **[L:5]** - header, ‘s’-‘d’-‘0’-01-ff
| repeated:
| 	**[L:4]** - length of compressed chunk
| 		*a chunk usually consists of 1024*256 uncompressed bytes*
| 	**[L:V]** - compressed (zlib) chunk

.. _ff-si0:

Segmented Index (.si0)
^^^^^^^^^^^^^^^^^^^^^^

The first line is a header of the following form:

:samp:`%s%s:%08x:%s:%08x\r`

with the following data:

| 1) the file extension 'si0'
| 2) the magic bytes 0x01 0xff
| 3) the total size of the input
| 4) the MD5 hash of the input
| 5) the chunk size


The rest of the file is one line for every compressed block, in the following form:

:samp:`%08x:%08x:%s:%s:%08x:%08x:%s\r`

with the following data:

| 1) start of the block in the raw file
| 2) size of the block
| 3) Adler32 of the raw bytes modulo 0xFFFFFFFF, as hex, with the first two and last letters removed
| 4) MD5 hash of the raw bytes
| 5) number of bytes already written to compressed file (without magic bytes)
| 6) number of compressed bytes
| 7) MD5 hash of compressed bytes
