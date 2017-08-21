File Structures
===============

.. note ::
	This is a read-the-docs port of the original google docs `lu_file_structs <https://docs.google.com/document/d/1ZlgGv5gVI7Rx6kGNUwoXDHhOKJNjHkfQcuzpCL_fgjw>`_, written by humanoid, lcdr and others, ported by `@Xiphoseer <https://twitter.com/Xiphoseer>`_. This is currently a proof of concept and is not guaranteed to reflect the latest changes.

Introduction
------------

The purpose of this document is to list and protocol all the information about the client files of the game LEGO Universe (at least the ones that might be helpful for the process of creating a private server).
Note that usually most of the client files are packed into :file:`.pk` files which are stored in the :file:`client/res/pack` folder and need to be extracted first to be able to work on them (see Tools section for a link to a simple extractor).

.. _tools:

Tools
-----

* Extract PK files: `LUPKExtractor <http://www.mediafire.com/download.php?vh6c80y5jzgjaog>`_ (source code included, linked to from `here <https://factionlu.wordpress.com/2012/01/23/my-personal-giveaway/>`_, `original post (most likely) <http://forum.xentax.com/viewtopic.php?f=10&t=4500>`_)
* Decompress sd0 compressed files: https://bitbucket.org/lcdr/utils/src decompress_sd0.py 
* Find keys for fsb files: http://hcs64.com/files/guessfsb03.zip (linked to from `here <http://forum.xentax.com/viewtopic.php?f=17&t=5700>`_)
* View .nif files http://sourceforge.net/projects/niftools/ (linked to from `here <https://factionlu.wordpress.com/2012/01/23/my-personal-giveaway/>`_)
* Convert FDB to SQLite: https://bitbucket.org/lcdr/utils/src fdb_to_sqlite.py

Compression formats
-------------------

Segmented (sd0)
^^^^^^^^^^^^^^^

There is a decompressor available, see the tools section.

| **[L:5]** - header, ‘s’-‘d’-‘0’-01-ff
| repeated:
| 	**[L:4]** - length of compressed chunk
| 		*a chunk usually consists of 1024*256 uncompressed bytes*
| 	**[L:V]** - compressed (deflate) chunk


File format structures
----------------------

.. include :: file-structures/manifest.rst

.. include :: file-structures/catalog.rst

.. include :: file-structures/pack.rst

.. include :: file-structures/database.rst

.zal, .ast
^^^^^^^^^^
| plain text, lists paths to additional files (to load?), one line for each file
| zal = zone asset list?

.evc
^^^^
plain text, xml structure, environment-config?

.. include :: file-structures/lutriggers.rst

.. include :: file-structures/zone.rst

.. include :: file-structures/level.rst

.. include :: file-structures/raw.rst

Animations (.gfx)
^^^^^^^^^^^^^^^^^

.. note ::
	Used for small animations, such as minifig faces. Essentially a .swf flash file, with a different file header. To convert to a .swf file, change the “GFX” in the beginning of the file header to “FWS”.
	See also: http://wwwimages.adobe.com/content/dam/Adobe/en/devnet/swf/pdf/swf-file-format-spec.pdf
