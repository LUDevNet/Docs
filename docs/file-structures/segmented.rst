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

Not documented yet