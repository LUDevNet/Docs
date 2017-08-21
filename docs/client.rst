Client packets
==============

.. note ::
	This is a read-the-docs port of the original google docs `lu_client_packets <https://docs.google.com/document/d/1CoZJGGYMld_D05iNtFUs4q6HeG9sUVYvqe-5F1yN2QY>`_, written by humanoid, lcdr and others, ported by `@Xiphoseer <https://twitter.com/Xiphoseer>`_. This is currently a proof of concept and is not guaranteed to reflect the latest changes.

General
-------

[53-00-00-00] (global - handshake)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:[u32]:		Game/Network version, this has to match with the server version, latest one is 171022
:[u32]:		???, is always 0?
:[u32]:		remote connection type (this is for some reason a u32, although the packet header only has space for a u16, so 2 bytes are wasted), this is always 5?
:[u32]:		process id of the client
:[u16]:		local port
:[string]:	unused for client? this would normally be a local ip, is this only used for server?

To Auth
-------

[53-01-00-00] (login info)
^^^^^^^^^^^^^^^^^^^^^^^^^^

:[wstring]: Username
:[L\:82]: 	Password, wstring
:[u16]: 	COMLANG, language id
:[u8]: 		???, could be a count for something (maybe the following info)? it could also be an identifier for the platform (I encountered something like that in the code for values 2 and 1: “mac” or “pc”), seems to be always 1
:[L\:512]:	process memory info of the client, wstring (see GetProcessMemoryInfo() on MSDN for more info, the values get constructed to a wstring in the client code)
:[L\:256]:	client graphics card (driver) info, wstring
:[u32]:		SYSTEM_INFO.dwNumberOfProcessors
:[u32]:		SYSTEM_INFO.dwProcessorType
:[u16]:		SYSTEM_INFO.dwProcessorLevel
:[u16]:		SYSTEM_INFO.dwProcessorRevision
:[u32]:		???, doesn’t seem to be part of the above/below struct (but is apparently written as constant (0x114) in the packet?)

(the following structures can be skipped or does the client abort packet creation if that happens?)

:[u32]: 	OSVERSIONINFO.dwMajorVersion
:[u32]: 	OSVERSIONINFO.dwMinorVersion
:[u32]: 	OSVERSIONINFO.dwBuildNumber
:[u32]: 	OSVERSIONINFO.dwPlatformId


To World
--------

[53-04-00-01] (user session info)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:[wstring]:	username
:[wstring]:	user key from auth
:[L\:32]:	some hashed string?, string
:[L\:1]:	???, is either 0 or 1 (so we can’t assume this the final null from prev string?)


[53-04-00-02] (minifigure list request)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automatically sent from the client when it connects from auth, also sent whenever the client needs the character list


[53-04-00-03] (minifigure create request)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:[wstring]:	Name of new minifigure (since you can only enter up to 24 characters in the client the last 16 bytes will be always unallocated?)
:[u32]:		First part of predef name, taken from minifigname_first.txt (line number-1)
:[u32]:		Second part of predef name, taken from minifigname_middle.txt
:[u32]:		Third part of predef name, taken from minifigname_last.txt
:[L\:9]:	???
:[u32]:		Shirt color
:[u32]:		Shirt style
:[u32]:		Pants color
:[u32]:		Hair style
:[u32]:		Hair color
:[u32]:		“lh”, see “<mf />” row in the xml data from chardata packet (no idea what it is)
:[u32]:		“rh”, see “<mf />” row in the xml data from chardata packet (no idea what it is)
:[u32]:		Eyebrows
:[u32]:		Eyes
:[u32]:		Mouth
:[u8]:		???

[53-04-00-04] (user wants to join world)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:[s64]:		object ID of selected Minifig


[53-04-00-05] (client game message)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
See the dedicated game message document for more information


[53-04-00-06] (character delete request)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:[s64]:		ID of minifig to delete


[53-04-00-07] (character rename request)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:[s64]:		ID of minifig to rename
:[wstring]:	New name


[53-04-00-0e] (chat message)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:[L\:3]:		 ???, probably something like chat channel
:[L\:4?]:		 length of message (including null terminator, as characters (meaning this * 2 = actual binary length)
:[A\:0x0f,L\:V]: chat message


[53-04-00-13] (clientside load complete)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:[u16]:		zone ID
:[u16]:		map instance
:[u32]:		map clone


[53-04-00-15] (some kind of indicator that this packet should be routed)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:[u32]:		length of following
:[byte]:	normal packet but without the first (0x53) byte


[53-04-00-16] (position/rotation updates)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
seems like this is exactly the same as a part of controllable physics component,
for the structure definition see the marked section in the lu_replica_packets document


[53-04-00-17] (Mail stuff)
^^^^^^^^^^^^^^^^^^^^^^^^^^
:[u32]:			Mail stuff ID
:[ID specific]:	ID specific

todo: investigate [A:0x0c,u32]

Mail stuff IDs
""""""""""""""
	* 0x00 - Mail send
	* 0x03 - Mail data request
	* 0x05 - Mail attachment collect
	* 0x07 - Mail delete
	* 0x09 - Mail read
	* 0x0b - mail notification request?

Mail send
"""""""""
:[L\:100]:	Mail subject, wstring
:[L\:800]:	Mail body, wstring
:[L\:64]:	Recipient name, wstring
:[u64]:		???
:[s64]:		attachment item object id
:[u16]:		attachment item count
:[u16]:		COMLANG, language id
:[u32]:		???

Mail data request
"""""""""""""""""
Always 53 04 00 17 00 00 00 00 03 00 00 00

Mail attachment collect
"""""""""""""""""""""""
:[A\:0x0c,u32]:	???
:[s64]:			ID of mail from which the attachment is to be collected
:[s64]:			player object id

respond to this with attachment remove confirm

Mail delete
"""""""""""
:[A\:0x0c,u32]:	???
:[s64]:			ID of mail to be deleted
:[s64]:			player object id

respond to this with delete confirm

Mail read
"""""""""
:[A\:0x0c,u32]:	???
:[s64]:			ID of read mail

respond to this with read confirm


[53-04-00-19] (whitelist request)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:[u8]:			Super chat level
:[u8]:			Request ID (incremented per request)
:[L\:84]:		If private chat, name of receiver, wstring
:[A\:0x5e,u16]: Length of string
:[L\:V]:		String to be checked against the whitelist (e.g chat input, mail input) (2-byte char)


[53-04-00-1b] (model preview request?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This gets sent if :samp:`UGCUSE3DSERVICES` in :file:`boot.cfg` is 0, when a HTTP UGC request would be sent.

:[s64]:		Model ID?
:[u8]:	 	??? Request type?


[53-04-00-1e] (“handle funness” in client enum)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Seems to be sent when client is laggy? (Easier reproducible when launching via debugger)
:[u64]:		???


[53-04-00-20] (“request free trial refresh”)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
todo - reproduce (this gets sent one times at the end of the first world traffic of the newly created minifigure traffic (didn’t see it in other traffics…)


[53-04-00-78] (ugc download failed)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
todo - analyze/reproduce (this gets sent multiple times at the end of one world traffic (didn’t see it in other traffics…)
