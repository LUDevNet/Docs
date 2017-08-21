File Structures
===============

.. note ::
	This is a read-the-docs port of the original google docs `lu_file_structs <https://docs.google.com/document/d/1ZlgGv5gVI7Rx6kGNUwoXDHhOKJNjHkfQcuzpCL_fgjw>`_, written by humanoid, lcdr and others, ported by `@Xiphoseer <https://twitter.com/Xiphoseer>`_. This is currently a proof of concept and is not guaranteed to reflect the latest changes.

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

Manifest (.txt) 
^^^^^^^^^^^^^^^
(in :file:`/versions` folder)

| **[files]** section:
| 	Every line represents a file entry which consists of six values (in ASCII format), separated by a :samp:`,`
| 	
| 	1) filename
| 	2) filesize
| 	3) md5 hash of file
| 	4) compressed filesize
| 	5) md5 hash of compressed file
| 	6) md5 hash of values 1) to 5) (includes ‘,’ separators except the one preceding this value)


Catalog (.pki)
^^^^^^^^^^^^^^
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

Pack (.pk)
^^^^^^^^^^
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

Database (.fdb)
^^^^^^^^^^^^^^^

.. note ::
	There is a converter from fdb to sqlite available, see the tools section. This file type has no relation to firebird database files of the same extension.

:table_count=[u32]:		number of tables
:[u32]:					address pointer to table header in file

-> table header
"""""""""""""""

:[table_count]:
:[u32]:					address pointer to column header in file

-> column header
""""""""""""""""
:column_count=[u32]:	number of columns
:[L\:4]:				name of table, DATA_TYPE::TEXT
:[u32]:					address pointer to column data in file

-> column data
""""""""""""""
:[column_count]:	
    
    	:[u32]:			data type of column
    
    	:[L\:4]:		name of column, DATA_TYPE::TEXT

:[u32]:					address pointer to row top header in file

-> row top header
"""""""""""""""""
:row_count=[u32]:		row count, an allocated number
:[s32]:					address pointer to row header in file (-1 means invalid there are a lot of those)

-> row header
"""""""""""""
:[row_count]:
		:[s32]:			address pointer to row info in file

-> row info
"""""""""""
:[s32]:					address pointer to row data header in file
:[s32]:					address pointer to a linked row info in file, doesn’t count as a row in row_count and it seems that all rows with a key id greater than row_count get linked to the row with a key id modulo row_count, rows with the same key id also get linked together, otherwise this is an invalid pointer

-> row data header
""""""""""""""""""
:column_count=[s32]:	number of columns (that’s right, this is included again for every row, what a waste of space)
:[s32]:					address pointer to row data in file (finally)

-> row data
"""""""""""
:[column_count]:
        
        :[s32]:			data type of column, s32
   		
   		:[s32]:			data, DATA_TYPE


extra notes for fdb format
""""""""""""""""""""""""""
* todo: write some notes regarding the weird block allocation sizes for the structures
* since our conventional format wasn’t exactly suited for documenting this format I introduced the “address following” which basically first gets defined by name in a structure description (as underlined text) and is afterwards mentioned whenever that address should be accessed in the file structure when parsing the structure (indicated by an arrow prefix to the underlined name)
* address pointers can be -1 which most likely means an invalid address (just skip those)
* strings types (TEXT and VARCHAR) are always null-terminated (with some over allocated bytes afterwards it seems, apparently string length are filled to be modulo 4 = 0?)
* strings and int64 (BIGINT) types are always stored with an additional address pointer, like this: [pointer]->[data]

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

.zal, .ast
^^^^^^^^^^
| plain text, lists paths to additional files (to load?), one line for each file
| zal = zone asset list?

.evc
^^^^
plain text, xml structure, environment-config?

.lutriggers
^^^^^^^^^^^
plain text, xml structure

:trigger: 	A trigger

	:id: 	as referenced in in the .lvl

	:event: event type on which the trigger should fire 

		:id:		One EventID value
		:command:	command to be executed on trigger
            
			:id: command type todo: document possible values
			:target: “self” for the trigger, “target” for the object that triggered it, “objGroup” which instantiates another attribute called targetName
			:args: command-specific arguments todo:
    		

Possible Values (EventIDs)
""""""""""""""""""""""""""
* OnDestroy
* OnCustomEvent
* OnEnter
* OnExit
* OnCreate
* OnHit
* OnTimerDone
* OnRebuildComplete
* OnActivated
* OnDeactivated
* OnArrived
* OnArrivedAtEndOfPath
* OnZoneSummaryDismissed
* OnArrivedAtDesiredWaypoint
* OnPetOnSwitch
* OnPetOffSwitch
* OnInteract

Possible Values (Commands)
""""""""""""""""""""""""""

============================  =======================================================================================================
Command                       Parameters
============================  =======================================================================================================
zonePlayer                    [zone ID],(0 for non-instanced, 1 for instanced), (x, y, z position), (y rotation), (spawn point name)
fireEvent                     (String to send to the recipient)
destroyObj                    (0 for violent, 1 for silent)
toggleTrigger                 [0 to disable, 1 to enable]
resetRebuild                  (0 for normal reset, 1 for "failure" reset)
setPath                       [new path name],(starting point index),(0 for forward, 1 for reverse)
setPickType                   [new pick type, or -1 to disable picking]
moveObject                    [x offset],[y offset],[z offset]
rotateObject                  [x rotation],[y rotation],[z rotation]
pushObject                    [x direction],[y direction],[z direction]
repelObject                   (force multiplier)
setTimer                      [timer name],[duration in seconds]
cancelTimer                   [timer name]
playCinematic                 [cinematic name],(lead-in in seconds),("wait" to wait at end),("unlock" to NOT lock the player controls),("leavelocked" to leave player locked after cinematic finishes),("hideplayer" to make player invisible during cinematic
toggleBBB                     ("enter" or "exit" to force direction)
updateMission                 [taskType],[targetid],[value1],[value2],[wsValue]
setBouncerState               ["on" to activate bouncer or "off" to deactivate bouncer]
bounceAllOnBouncer            No Parameters Required
turnAroundOnPath              No Parameters Required
goForwardOnPath               No Parameters Required
goBackwardOnPath              No Parameters Required
stopPathing                   No Parameters Required
startPathing                  No Parameters Required
LockOrUnlockControls          ["lock" to lock controls or "unlock" to unlock controls]
PlayEffect                    [nameID],[effectID],[effectType],[priority(optional)]
StopEffect                    [nameID]
activateMusicCue              DEPRECATED.  Does nothing.
deactivateMusicCue            DEPRECATED.  Does nothing.
flashMusicCue                 DEPRECATED.  Does nothing.
setMusicParameter             DEPRECATED.  Does nothing.
play2DAmbientSound            DEPRECATED.  Does nothing.
stop2DAmbientSound            DEPRECATED.  Does nothing.
play3DAmbientSound            DEPRECATED.  Does nothing.
stop3DAmbientSound            DEPRECATED.  Does nothing.
activateMixerProgram          DEPRECATED.  Does nothing.
deactivateMixerProgram        DEPRECATED.  Does nothing.
CastSkill                     [skillID]
displayZoneSummary            [1 for zone start, 0 for zone end]
SetPhysicsVolumeEffect        ["Push", "Attract", "Repulse", "Gravity", "Friction"],[amount],(direction x, y, z),("True" or "False")(min distance)(max distance)
SetPhysicsVolumeStatus        [“On”, “Off”]
setModelToBuild               [template ID]
spawnModelBricks              [amount, from 0 to 1],[x],[y],[z]
ActivateSpawnerNetwork        [Spawner Network Name]
DeactivateSpawnerNetwork      [Spawner Network Name]
ResetSpawnerNetwork           [Spawner Network Name]
DestroySpawnerNetworkObjects  [Spawner Network Name]
Go_To_Waypoint                [Waypoint index],("true" to allow direction change, otherwise "false"),("true" to stop at waypoint, otherwise "false")
ActivatePhysics               "true" to activate and add to world, "false" to deactivate and remove from the world
============================  =======================================================================================================

Zone (.luz)
^^^^^^^^^^^

| **[u32]** - version number, always one of 0x24, 0x26, 0x27, 0x28, 0x29?
|	the file format differs depending on the version
| if version >= 0x24:
| 	**[u32]** - versioncontrol????
| **[u32]** - World ID
| if version >= 0x26:
| 	**[float]** - Spawnpoint position x
| 	**[float]** - Spawnpoint position y
| 	**[float]** - Spawnpoint position z
| 	**[float]** - Spawnpoint rotation x
| 	**[float]** - Spawnpoint rotation y
| 	**[float]** - Spawnpoint rotation z
| 	**[float]** - Spawnpoint rotation w
| **[if version < 0x25 u8, if version >= 0x25 u32]**: count of scenes
| 	**[u8]** - length
| 		**[char]** -filename
| 	**[u8]** - scene id?, length unclear
| 	**[L:3]** - ???, always == 0?
| 	**[u8]** - is audio scene?
| 	**[L:3]** - ???, always == 0?
| 	**[u8]** - length
| 		**[char]** - scene name
| 	**[L:3]** - seems to be skipped in code
| **[u8]** - ???, always == 0?
| **[u8]** - length
| 	**[char]** - map/terrain filename
| **[u8]** - length
| 	**[char]** - map/terrain name
| **[u8]** - length
| 	**[char]** - map/terrain description
| if version >= 0x20:
| 	**[u32]** - count of scene transitions
| 		if version < 0x25:
| 			**[u8]** - length
| 				**[char]** - scene transition name
| 		if version <= 0x21 or version >= 0x27:
| 			loop_times = 2
| 		else:
| 			loop_times = 5
| 		**[loop_times]**
| 			**[u64]** - scene id
| 			**[float]** - transition point position x
| 			**[float]** - transition point position y
|			**[float]** - transition point position z
| if version >= 0x23:
| 	**[u32]** - length of rest of file (everything after this) in bytes
| 	**[u32]** - ???, always 1?
| 	**[u32]** - count
| 		**[u32]** - path version
| 		**[u8]** - count
| 			**[wchar]** - path name
| 		**[u32]** - path type,
| 			0 = Movement,
| 			1 = Moving platform,
| 			2 = Property,
| 			3 = Camera,
| 			4 = Spawner,
| 			5 = Showcase,
| 			6 = Race,
| 			7 = Rail
| 		**[u32]** - ???
| 		**[u32]** - PathBehavior (0: Loop, 1: Bounce, 2: Once)
| 		if path type == 1:
| 			if path version >= 18:
| 				**[u8]** - ???
| 			elif path version >= 13:
| 				**[u8]** - count
| 					**[wchar]** - ???
| 		elif path type == 2:
|			**[s32]** - ???
| 			**[s32]** - ???
| 			**[s32]** - ???
| 			**[u64]** - ???
| 			**[u8]** - count
| 				**[wchar]** - ???
| 			**[u32]** - count
| 				**[wchar]** - ???
| 			**[s32]** - ???
| 			**[s32]** - ???
| 			**[float]** - ???
| 			**[s32]** - ???
| 			**[s32]** - ???
| 			**[float]** - ???
| 			**[float]** - ???
| 			**[float]** - ???
| 			**[float]** - ???
| 		elif path type == 3:
| 			**[u8]** - count
| 				**[wchar]** - ???
| 			if path version >= 14:
| 				**[u8]** - ???
| 		elif path type == 4:
| 			**[u32]** - spawned lot
| 			**[u32]** - ???
| 			**[s32]** - ???
| 			**[u32]** - ???
| 			**[s64]** - spawner object id, note that this does not get added bits in the captures
| 			**[u8]** - ???
| 		**[u32]** - count
| 			**[float]** - position x
| 			**[float]** - position y
| 			**[float]** - position z
| 			if path type == 1:
| 				**[float]** - rotation w
| 				**[float]** - rotation x
| 				**[float]** - rotation y
| 				**[float]** - rotation z
| 				**[u8]** - ???
| 				**[float]** - moveTime????
| 				**[float]** - idle Time????
| 				if path version >= 13:
| 					**[u8]** - count
| 						**[wchar]** - audioUUID???
| 					**[u8]** - count
| 						**[wchar]** - audioUUID???
| 				elif path type == 3:
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
|				elif path type == 4:
| 					**[float]** - rotation w
| 					**[float]** - rotation x
| 					**[float]** - rotation y
| 					**[float]** - rotation z
| 				elif path type == 6:
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[u8]** - ???
| 					**[u8]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 				elif path type == 7:
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					**[float]** - ???
| 					if path version >= 17:
| 						**[float]** - ???
| 				if path type in (0, 4, 7):
| 					**[u32]** - count
| 						**[u8]** - count
| 							**[wchar]** - config name
| 						**[u8]** - count
| 							**[wchar]** - config type and value

Level (.lvl)
^^^^^^^^^^^^

.. todo ::

	* It seems the structure is split in chunks marked by “CHNK”, somewhat similar to the IFF file format
	* It seems Chunks can only begin on addresses % 16 == 0, if the chunk wouldn’t start on one padding is inserted until it matches 
	* Padding always seems to be the 0xcd byte, but that’s probably just a side effect of not writing data to it

Chunk Header
""""""""""""

| if **[L:4]** - ``CHNK`` in ascii :
| 	**[u32]** - chunk type, one of 1000, 2000, 2001, 2002 (see below)
| 	**[u16]** - ???
| 	**[u16]** - ???
| 	**[u32]** - Chunk length (starting from the ``CHNK``)
| 	**[u32]** - Address of start of data
| 		**[L:V]** - padding
| 	**[Chunk Structure as referred]**
| else: (Older file)
| **[L:265]** - ???
| **[std::string]** - skybox
| **[std::string]** - “(invalid)”
| **[std::string]** - “(invalid)”
| **[std::string]** - “(invalid)”
| **[std::string]** - “(invalid)”
| **[std::string]** - “(invalid)”
| **[L:4]** - ???
| **[u32]** - count
|	**[float]** - ???
| 	**[float]** - ???
| 	**[float]** - ???
| **[Chunk 2001 Structure]**

Chunk Type 1000
"""""""""""""""

| **[u32]** - lvl version?
| **[u32]** - ???
| **[u32]** - ???
| **[u32]** - ???
| **[u32]** - ???

Chunk Type 2000
"""""""""""""""

| **[u32]** - size of data
| 	**[u32]** - address of sky section
| 	**[u32]** - address of other section
| 	*the rest of this section seems to consist solely of floats (possibly always 25? Seems like it was 24 in beta, but could have also been 25)*
| 	**[float]** * ((size of data-8) / 4) - ???
| **[u32]** - id count?
| 	**[u32]** - id? (starting with 0? Looking at beta lvl files it could also start with 1)
| 	**[float]** - ???
| 	**[float]** - ???
| *Not sure if the rest of this section always consists of 2*3 floats (checked a few different lvl files), it’s very weird/inconsistent in the beta files though (at least for gnarled forest it seems like its 2*3 + 2*2 + 3 there, judging by their order of magnitude)*
| **[float]** * 3 - ???
| **[float]** * 3 - ???

**Sky section**

| **[u32]** - length
| 	**[char]** - filepath
| *the following filepaths are always “(invalid)”*
| **[u32]** - length
| 	**[char]** - filepath
| **[u32]** - length
| 	**[char]** - filepath
| **[u32]** - length
| 	**[char]** - filepath
| **[u32]** - length
| 	**[char]** - filepath
| **[u32]** - length
| 	**[char]** - filepath

**Other section**

| **[u32]** - length of following
| todo: investigate

Chunk Type 2001
"""""""""""""""

| **[u32]** - number of objects
| 	**[u64]** - object id, but some bits are missing
| 		-> these ids show up in the traffic (mostly for spawner LOTs but others as well with game messages) with the 46th bit enabled, I guess that bit means its a local object?
| 	**[s32]** - LOT
| 	if version >= 0x26:
| 		**[u32]** - ???, accepted values seem to be 0 to 10 inclusive?
| 	if version >= 0x20:
| 		**[u32]** - ???
| 	**[float]** - position x
| 	**[float]** - position y
| 	**[float]** - position z
| 	*Note: The w,x,y,z order here is different from the x,y,z,w order in the replica packets*
| 	**[float]** - rotation w
| 	**[float]** - rotation x
| 	**[float]** - rotation y
| 	**[float]** - rotation z
| 	**[float]** - scale
| 	**[u32]** - length
| 		**[wchar]**  - object settings variables in LDF format
| 			``spawntemplate``
| 				*describes the LOT to be spawned for Spawner objects, use the same position/rotation as Spawner object for those*
| 			``trigger_id``
| 				``scene_id:trigger_id``, *See also the documentation for .lutriggers files*
|	if version >= 7:
|		**[u32]** - ???, always == 0?

Chunk Type 2002
"""""""""""""""

.. todo :: investigate (seems to be related to environmental effects?)

.raw
^^^^

.. note ::
	
	Used for terrain data.
	See also: http://legouniverse.wikia.com/wiki/User_blog:Jamesster.LEGO/Terrain_files 

| **[L:0x423b]** - chunk of data (seems to be always the same size?), needs to be further picked apart
| **[u32]** - size specifier for the following data
| 		*(shift amount, actual size is calculated by shifting 4 left, by two times the amount of zeroes before the bit of the specifier, e.g size specifier = 0x40 -> has 6 zeros -> size = 4 << (2*6)), should always be a power of two number?*
| 	**[u8]** - data
| 
| **[u32]** - ???
|	*(tocheck: is this value dependant on the size specifier? was 0xb38 for 0x40 and 0x338 for 0x20)*
| 
| **[chunkWidth * chunkHeight * images (always 2 so far)]**
| 	**[DDS_File] - [‘D’-’D’-’S’-0x20]** specifier followed by DDS Header info and image data

.. todo :: the rest of this, seems like there are a bunch more DDS_Files and more of that other data with the size specifiers, the only question is if they are in any particular order or random (possibly specified in the initial chunk of data)

* Portabello: 18 dds files in total
* Avant gardens: 242 dds files in total, so far they are ordered in chunk of image 1, chunk of image 2, chunk of image 1, chunk of image 2, ...

Animations (.gfx)
^^^^^^^^^^^^^^^^^

.. note ::
	Used for small animations, such as minifig faces. Essentially a .swf flash file, with a different file header. To convert to a .swf file, change the “GFX” in the beginning of the file header to “FWS”.
	See also: http://wwwimages.adobe.com/content/dam/Adobe/en/devnet/swf/pdf/swf-file-format-spec.pdf
