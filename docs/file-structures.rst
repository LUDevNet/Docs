Introduction
------------

.. note ::
	This is a read-the-docs port of the original google docs `lu_file_structs <https://docs.google.com/document/d/1ZlgGv5gVI7Rx6kGNUwoXDHhOKJNjHkfQcuzpCL_fgjw>`_, written by humanoid, lcdr and others, ported by `@Xiphoseer <https://twitter.com/Xiphoseer>`_. This is currently a proof of concept and is not guaranteed to reflect the latest changes.


The purpose of this document is to list and protocol all the information about the client files of the game LEGO Universe (at least the ones that might be helpful for the process of creating a private server).
Note that usually most of the client files are packed into :file:`.pk` files which are stored in the :file:`client/res/pack` folder and need to be extracted first to be able to work on them (see Tools section for a link to a simple extractor).

.. _tools:

Tools
^^^^^

* Extract PK files: `LUPKExtractor <http://www.mediafire.com/download.php?vh6c80y5jzgjaog>`_ (source code included, linked to from `here <https://factionlu.wordpress.com/2012/01/23/my-personal-giveaway/>`__, `original post (most likely) <http://forum.xentax.com/viewtopic.php?f=10&t=4500>`_)
* Decompress sd0 compressed files: https://bitbucket.org/lcdr/utils/src decompress_sd0.py 
* Find keys for fsb files: http://hcs64.com/files/guessfsb03.zip (linked to from `here <http://forum.xentax.com/viewtopic.php?f=17&t=5700>`__)
* View .nif files http://sourceforge.net/projects/niftools/ (linked to from `here <https://factionlu.wordpress.com/2012/01/23/my-personal-giveaway/>`__)
* Convert FDB to SQLite: https://bitbucket.org/lcdr/utils/src fdb_to_sqlite.py

Resources
^^^^^^^^^
*  There are scripts, which require stuff from an “TestAndExample” folder, which is missing, you can get it from
   `here <http://dl.coolgametube.net/LU%20missing%20folder,%20TestAndExample.zip>`__.
* `Official LXFML Documentation <https://news.lugnet.com/cad/ldd/?n=140>`_ from the LEGO Group back from 2007
