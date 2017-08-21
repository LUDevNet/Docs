File Structures
===============

Introduction
------------

The purpose of this document is to list and protocol all the information about the client files of the game LEGO Universe (at least the ones that might be helpful for the process of creating a private server).
Note that usually most of the client files are packed into :file:`.pk` files which are stored in the :file:`client/res/pack` folder and need to be extracted first to be able to work on them (see Tools section for a link to a simple extractor).

Tools
-----

* Extract PK files: `LUPKExtractor <http://www.mediafire.com/download.php?vh6c80y5jzgjaog>`_ (source code included, linked to from `here <https://factionlu.wordpress.com/2012/01/23/my-personal-giveaway/>`_, `original post (most likely) <http://forum.xentax.com/viewtopic.php?f=10&t=4500>`_)
* Decompress sd0 compressed files: https://bitbucket.org/lcdr/utils/src decompress_sd0.py 
* Find keys for fsb files: http://hcs64.com/files/guessfsb03.zip (linked to from `here <http://forum.xentax.com/viewtopic.php?f=17&t=5700>`_)
* View .nif files http://sourceforge.net/projects/niftools/ (linked to from `here <https://factionlu.wordpress.com/2012/01/23/my-personal-giveaway/>`_)
* Convert FDB to SQLite: https://bitbucket.org/lcdr/utils/src fdb_to_sqlite.py

Compression formats
-------------------

sd0
^^^

There is a decompressor available, see the tools section.

:[L\:5]:	header, ‘s’-‘d’-‘0’-01-ff
:repeated:
			:[L\:4]:	length of compressed chunk (a chunk consists of max 1024*256  uncompressed bytes?)
			:[L\:V]:	compressed (deflate) chunk


File format structures
----------------------

.txt (in /versions folder)
^^^^^^^^^^^^^^^^^^^^^^^^^^
[files] section:
Every line represents a file entry which consists of six values (in ASCII format), separated by a :samp:`,`

1. filename
2. filesize
3. md5 hash of file
4. compressed filesize
5. md5 hash of compressed file
6. md5 hash of values 1) to 5) (includes ‘,’ separators except the one preceding this value)


.pki
^^^^
:[u32]: version?, has to be 3

:[u32]: count

		:[u32]:	length

				:[char]:	pk filename, char

:[u32]: count
    	
		:[s32]:	pk index (from pk file)

		:[s32]:	index of a binary tree node (-1 for no child, root node is [count] / 2)

		:[s32]:	index of a binary tree node (-1 for no child, root node is [count] / 2)
		
		:[u32]:	0-based index of file in the file list above
		
		:[u32]:	mostly 268515584, sometimes 1

.pk
^^^
:[L\:7]:			header info (are the last 3 bytes part of it?), seems to be always [‘n’-‘d’-‘p’-‘k’-01-ff-00]
:[L\:V+5]*#Files:	raw file data, it seems that every packed file is always terminated with [ff-00-00-dd-00] (obviously not part of the packed file but the pk structure)
:[u32]:	number of records (and with that, number of files packed in the pk file)
    	
		:[s32]:		pk index
    	
		:[s32]:		index of a binary tree node (-1 for no child, root node is [number of records] / 2)
    	
		:[s32]:		index of a binary tree node (-1 for no child, root node is [number of records] / 2)
    	
		:[u32]:		original file size
    
		:[L\:32]:	md5 hash of original file, string
    
		:[L\:4]:	??? (could be padding caused by a possible null character of the previous string?)

		:[u32]:		compressed file size

		:[L\:32]:	md5 hash of compressed file, string

		:[L\:4]:	??? (could be padding caused by a possible null character of the previous string?)

		:[u32]:		pointer to file data in the pk file, u32

		:[bool]:	flag whether packed file is compressed or not (if true the packed data should match with the compressed size/hash)

		:[L\:3]:	???

:[u32]:		pointer to [number of records] in the pk file (only reliable way to obtain useful info about the pk file?)

:[u32]:		???
