Introduction
============

.. note ::
	This is a read-the-docs port of the original google docs `lu_packet_structs <https://docs.google.com/document/d/1v9GB1gNwO0C81Rhd4imbaLN7z-R0zpK5sYJMbxPP3Kc>`_, written by humanoid, lcdr and others, ported by `@Xiphoseer <https://twitter.com/Xiposeer>`_. This is currently a proof of concept and is not guaranteed to reflect the latest changes.

Quick notes to get started
--------------------------

Client
^^^^^^

* This documentation is targeted towards the latest publicly released client (1.10.64) which you can download in its original form `here <https://mega.nz/#!zpQyzAyA!az8Omzz-mH-03nOT1-H5jpjm75x2ZyDAv9BikCUHxG8>`_ (recommended) or in its unpacked form `here <https://mega.nz/#!zhRzBa4C!B5eY94-6vYmjJYqXkDXDM5hiqkPhZ7yb9ShCHG3Lgo8>`_.
* To redirect the client to a different server simply change the :samp:`AUTHSERVERIP` host info in the :file:`boot.cfg` file to a new host.
* The client stores an additional config and a log file from the last session in the :file:`{SystemDrive}:\\Users\\{User}\\AppData\\Local\\LEGO Software\\LEGO Universe\\` folder.

Server
^^^^^^

* The client uses the RakNet network library (v3.25) to communicate with the server, therefore it is recommended to use it in the server if you want to work on one and are new to this project.
* You can download it `here <http://www.raknet.com/raknet/downloads/RakNet-3.25.zip>`_ (documentation and sample projects are included), note that later versions of the library won’t work due to changes in the network protocol. Alternatively lcdr wrote a python version with the minimum features needed to run a server for the game implemented, available `here <https://bitbucket.org/lcdr/pyraknet>`_ (no documentation yet so not recommended for inexperienced users)
* The listening port for the Authentication Server is hardcoded to 1001 (UDP), the ports for the following instances (char, world) depend on what the Authentication Server sends to the client but the port range used for the original servers was 2001-2200 (UDP)
* In order for the server to establish a working connection with the client it is required to set up a pre-set password in RakNet by calling :samp:`SetIncomingPassword("3.25 ND1", 8);` for the `RakPeerInterface` instance before listening for packets
* It seems that the server used the :samp:`SYSTEM_PRIORITY` and :samp:`RELIABLE_ORDERED` options for all outgoing packets to the client (though that's probably not a requirement)

Packet Captures
---------------

Thanks to pwjones we have access to quite a lot of (partial) traffic sessions of the original server which serve as a basis for this documentation, if you want to dig into them yourself, here is a `download link <https://mega.co.nz/#F!yxIyxCpR!rNJ5Uub4RJNL8c6ZgM-Q0w>`_.

Since the original captures (`*.pcap` files) were encrypted by RakNet it was required to decrypt them again (`*.bin` files stored in `*.zip` archives where each archive represents a session) which was only possible using a piece of information that RakNet exchanges at the beginning of a traffic.

However since more than half of the captured traffics only consist of a fraction of the entire session this information is missing for those captures (marked as `*_unresolved.pcap`), making them undecryptable at this point (they’re still included in the archives though, so all available captures are in one place).

There are a few exceptions where it was possible to decrypt them using the same information from other traffic sessions but the remaining ones can’t be decrypted with this method so they’ll remain unreadable for the time being.

The naming format used is:
:file:`[packet number]_[source port]-[destination port]_[packet header]_[optional].bin`
where :samp:`[optional]` is used to display game message ids or network ids and LOTs in round brackets for the according packet types.

Extracting the entire .zip capture(s) is not recommended, since this many files (several ten thousand) will have a huge overhead on the file system (because of things like last modified info, which isn’t applicable here anyways), resulting in a much larger file space consumption and slower access times when trying to list the files in the explorer.
If you want to search multiple captures for specific files, use this script: https://bitbucket.org/lcdr/utils/src find_packets.py

(The script also yields the binary content of the packets, which can be useful for further filtering or logging)
If you want to look at the raw data of a packet yourself (not recommended for inexperienced users) you can of course extract single files from the .zip archive using an archive extractor of your choice (I recommend 7-Zip).
Then you can open the extracted `*.bin` file(s) using a hex editor of your choice (for some packet types it might be useful to have an editor that can shift the bits in the data, no recommendation here).
Alternatively a graphical viewer for capture files is available at https://bitbucket.org/lcdr/utils/src/ captureviewer.py (takes the entire .zip archive of a traffic as input, no need to extract anything)

Packet Documentation
--------------------

At this point all the structures are interpretation dependent which means that the data types (and with that the length) of each structure are not necessarily correct and should only be corrected if they are proven to be wrong (or if they make more sense).

* All strings that have a reserved space are null terminated, if the string doesn’t occupy the whole space, the bytes after the null terminator can be random.
* Variable strings are not null terminated but honor null termination if a null character is inserted.
* If any single hex numbers are used they should be marked as such (preceding 0x), for consecutive numbers that are taken directly from the data (like packet headers) this doesn’t have to be the case.
* All integers and floating point numbers are in little endian meaning that you have to read the occupied space in reverse to get the number, if you think there are some numbers that are in big endian, mark them as such.

Reference
^^^^^^^^^

.. glossary ::
	
	[xx-xx-xx-xx]
		first 4 bytes of the header (to go conform with decrypted packet file names)
	
	Artificial packet
		Packet was not captured in traffic logs, but tests with the ID show that it is recognized by the client.

	Theoretical packet
		Packet was not captured in traffic logs, but there is evidence in the client executable that the packet has this purpose. For server packets, once tests with the ID show that the client reacts to the packet, this should be changed to Artificial packet. For client packets, once we manage to get the client to send a packet of this type, this should be changed to normal packet.

	u8
		unsigned char (1 byte)
	
	u16
		unsigned short (2 bytes)

	u32
		unsigned long (4 bytes)

	u64
		unsigned long long (8 bytes)

	s32
		signed long (4 bytes)

	s64
		signed long long (8 bytes)

	bool
		boolean, can either be 1 or 0 (1 byte)
	
	bit
		“true” boolean, can either be 0 or 1, if there is a “flag” specifier then this defines whether a part of a packet (all structures that are indented one additional level) is included or not (1 bit)

	string
		char sequence (x bytes, null terminated (zero at the end)), 33 bytes long

	wstring
		wide char sequence (2*x bytes, null terminated (double zero at the end)), 66 bytes long
		(there are variants of these string types that are variable-length, they should be explicitly stated as variable length or somehow else be distinguished from the types above)

	LDF
		Lego data format, our unofficial name for the data format used in packets and configuration files (so far in binary, xml and config variations), see Appendix for definition

	LOT
		”Lego Object Template”?, determines the kind of object (whether it’s a player, an NPC, a tree, etc) and which components the object has (4 bytes)

	Object ID
		ID to distinguish each object in the game (e.g. player characters) (8 bytes)
	
	Network ID
		Temporary ID added by Raknet’s ReplicaManager, this is handled automatically and usually not important. Used to internally address objects for updates/destruction

	???
		this is unknown and should be investigated if possible

	L:n
		length specifier for n amounts of bytes, usually only temporarily used in the documentation to specify an unknown chunk of data (and replaced once the structure of that chunk is better known), in some instances the amount V is used to specify a variable amount of bytes

Packet Header
^^^^^^^^^^^^^

[u8] RakNet packet ID
	typically 0x53 for packets that are not being handled by RakNet (which are practically all packets that will be listed here)

if packet id is 0x53:

[u16] type of the remote connection
	is exchanged in the first two packets of the real traffic, should be one of these values: 0 (general), 1 (auth), 2 (chat), 4 (server), 5 (client)

[u32] packet ID
	to be able to identify what the packet contains (which will also be done in this document), could be that the latter 2 bytes are another u16 struct but they have always been 0 so far

[u8] ???
	is always 0? could be padded data

Packet List
-----------

Format
^^^^^^

[header]
	according enum name taken from the client executable ( - more descriptive name)

Packet Color Index
^^^^^^^^^^^^^^^^^^

:green: is available in the captured traffics (or could be reproduced to be sent from the client)
:yellow: is not available but self-created ones were effectively tested (Artificial packet)
:red: is not available and no testing was done yet or it had no effect (Theoretical packet)

All Servers
^^^^^^^^^^^
prefix = :samp:`MSG_SERVER_`

===========  ===================  ==========================================
53-00-00-00  VERSION_CONFIRM      Handshake (both client and server)
53-00-00-01  DISCONNECT_NOTIFY    Disconnect notify
53-00-00-02  GENERAL_NOTIFY       General notify
===========  ===================  ==========================================

Chat
^^^^
prefix = :samp:`MSP_CHAT_`

===========  =======================================  ===================================
53-02-00-00  LOGIN_SESSION_NOTIFY
53-02-00-01  GENERAL_CHAT_MESSAGE                     Public chat message
53-02-00-02  PRIVATE_CHAT_MESSAGE                     Private chat message
53-02-00-03  USER_CHANNEL_CHAT_MESSAGE
53-02-00-04  WORLD_DISCONNECT_REQUEST
53-02-00-05  WORLD_PROXIMITY_RESPONSE
53-02-00-06  WORLD_PARCEL_RESPONSE
53-02-00-07  ADD_FRIEND_REQUEST
53-02-00-08  ADD_FRIEND_RESPONSE
53-02-00-09  REMOVE_FRIEND
53-02-00-0a  GET_FRIENDS_LIST
53-02-00-0b  ADD_IGNORE
53-02-00-0c  REMOVE_IGNORE
53-02-00-0d  GET_IGNORE_LIST
53-02-00-0e  TEAM_MISSED_INVITE_CHECK
53-02-00-0f  TEAM_INVITE
53-02-00-10  TEAM_INVITE_RESPONSE
53-02-00-11  TEAM_KICK
53-02-00-12  TEAM_LEAVE
53-02-00-13  TEAM_SET_LOOT
53-02-00-14  TEAM_SET_LEADER
53-02-00-15  TEAM_GET_STATUS
53-02-00-16  GUILD_CREATE
53-02-00-17  GUILD_INVITE
53-02-00-18  GUILD_INVITE_RESPONSE
53-02-00-19  GUILD_LEAVE
53-02-00-1a  GUILD_KICK
53-02-00-1b  GUILD_GET_STATUS
53-02-00-1c  GUILD_GET_ALL
53-02-00-1d  SHOW_ALL
53-02-00-1e  BLUEPRINT_MODERATED
53-02-00-1f  BLUEPRINT_MODEL_READY
53-02-00-20  PROPERTY_READY_FOR_APPROVAL
53-02-00-21  PROPERTY_MODERATION_CHANGED
53-02-00-22  PROPERTY_BUILDMODE_CHANGED
53-02-00-23  PROPERTY_BUILDMODE_CHANGED_REPORT
53-02-00-24  MAIL
53-02-00-25  WORLD_INSTANCE_LOCATION_REQUEST
53-02-00-26  REPUTATION_UPDATE
53-02-00-27  SEND_CANNED_TEXT
53-02-00-28  GMLEVEL_UPDATE
53-02-00-29  CHARACTER_NAME_CHANGE_REQUEST
53-02-00-2a  CSR_REQUEST
53-02-00-2b  CSR_REPLY
53-02-00-2c  GM_KICK
53-02-00-2d  GM_ANNOUNCE
53-02-00-2e  GM_MUTE
53-02-00-2f  ACTIVITY_UPDATE
53-02-00-30  WORLD_ROUTE_PACKET
53-02-00-31  GET_ZONE_POPULATIONS
53-02-00-32  REQUEST_MINIMUM_CHAT_MODE
53-02-00-33  REQUEST_MINIMUM_CHAT_MODE_PRIVATE
53-02-00-34  MATCH_REQUEST
53-02-00-35  UGCMANIFEST_REPORT_MISSING_FILE
53-02-00-36  UGCMANIFEST_REPORT_DONE_FILE
53-02-00-37  UGCMANIFEST_REPORT_DONE_BLUEPRINT
53-02-00-38  UGCC_REQUEST
53-02-00-39  WHO
53-02-00-3a  WORLD_PLAYERS_PET_MODERATED_ACKNOWLEDGE
53-02-00-3b  ACHIEVEMENT_NOTIFY                       Chat Achievement notify
53-02-00-3c  GM_CLOSE_PRIVATE_CHAT_WINDOW
53-02-00-3d  UNEXPECTED_DISCONNECT
53-02-00-3e  PLAYER_READY
53-02-00-3f  GET_DONATION_TOTAL
53-02-00-40  UPDATE_DONATION
53-02-00-41  PRG_CSR_COMMAND
53-02-00-42  HEARTBEAT_REQUEST_FROM_WORLD
53-02-00-43  UPDATE_FREE_TRIAL_STATUS
===========  =======================================  ===================================

Client Auth
^^^^^^^^^^^
prefix = :samp:`MSG_AUTH_`

===========  =============================  =============================
53-01-00-00  LOGIN_REQUEST                  Login info
53-01-00-01  LOGOUT_REQUEST
53-01-00-02  CREATE_NEW_ACCOUNT_REQUEST
53-01-00-03  LEGOINTERFACE_AUTH_RESPONSE
53-01-00-04  SESSIONKEY_RECEIVED_CONFIRM
53-01-00-05  RUNTIME_CONFIG
===========  =============================  =============================

Client World
^^^^^^^^^^^^
prefix = :samp:`MSG_WORLD_`

id 00

===========  ======================================  ========================
53-04-00-01  CLIENT_VALIDATION                       Session info
53-04-00-02  CLIENT_CHARACTER_LIST_REQUEST
53-04-00-03  CLIENT_CHARACTER_CREATE_REQUEST
53-04-00-04  CLIENT_LOGIN_REQUEST                    Character selected
53-04-00-05  CLIENT_GAME_MSG
53-04-00-06  CLIENT_CHARACTER_DELETE_REQUEST
53-04-00-07  CLIENT_CHARACTER_RENAME_REQUEST
53-04-00-08  CLIENT_HAPPY_FLOWER_MODE_NOTIFY
53-04-00-09  CLIENT_SLASH_RELOAD_MAP                 Reload map cmd
53-04-00-0a  CLIENT_SLASH_PUSH_MAP_REQUEST           Push map req cmd
53-04-00-0b  CLIENT_SLASH_PUSH_MAP                   Push map cmd
53-04-00-0c  CLIENT_SLASH_PULL_MAP                   Pull map cmd
53-04-00-0d  CLIENT_LOCK_MAP_REQUEST
53-04-00-0e  CLIENT_GENERAL_CHAT_MESSAGE             General chat message
53-04-00-0f  CLIENT_HTTP_MONITOR_INFO_REQUEST
53-04-00-10  CLIENT_SLASH_DEBUG_SCRIPTS              Debug scripts cmd
53-04-00-11  CLIENT_MODELS_CLEAR
53-04-00-12  CLIENT_EXHIBIT_INSERT_MODEL
53-04-00-13  CLIENT_LEVEL_LOAD_COMPLETE              Character data request
53-04-00-14  CLIENT_TMP_GUILD_CREATE
53-04-00-15  CLIENT_ROUTE_PACKET                     Social?
53-04-00-16  CLIENT_POSITION_UPDATE                  Position update
53-04-00-17  CLIENT_MAIL
53-04-00-18  CLIENT_WORD_CHECK                       Whitelist word check
53-04-00-19  CLIENT_STRING_CHECK                     Whitelist string check
53-04-00-1a  CLIENT_GET_PLAYERS_IN_ZONE
53-04-00-1b  CLIENT_REQUEST_UGC_MANIFEST_INFO
53-04-00-1c  CLIENT_BLUEPRINT_GET_ALL_DATA_REQUEST
53-04-00-1d  CLIENT_CANCEL_MAP_QUEUE
53-04-00-1e  CLIENT_HANDLE_FUNNESS                   Performance issue?
53-04-00-1f  CLIENT_FAKE_PRG_CSR_MESSAGE
53-04-00-20  CLIENT_REQUEST_FREE_TRIAL_REFRESH
53-04-00-21  CLIENT_GM_SET_FREE_TRIAL_STATUS
===========  ======================================  ========================

// unsure about the next 3, depends on whether only MSG_WORLD_CLIENT_* names were used for packets or generally MSG_WORLD_* names (though the former wouldn’t make sense with the id 78 and leave it unoccupied)

===========  ======================================  ========================
53-04-00-22  Top 5 issues request                    Theoretical packet
53-04-00-23  UGC download failed?                    Theoretical packet
===========  ======================================  ========================

id from 24 to 77

===========  ======================================  ==============================================
53-04-00-78  UGC download failed                     (ID would fit with the biggest enum available)
===========  ======================================  ==============================================

World Server
^^^^^^^^^^^^
prefix = :samp:`MSG_CLIENT_`

===========  ======================================  ==================================
53-05-00-00  LOGIN_RESPONSE
53-05-00-01  LOGOUT_RESPONSE
53-05-00-02  LOAD_STATIC_ZONE                        World info
53-05-00-03  CREATE_OBJECT
53-05-00-04  CREATE_CHARACTER                        Character data
53-05-00-05  CREATE_CHARACTER_EXTENDED
53-05-00-06  CHARACTER_LIST_RESPONSE                 Character list
53-05-00-07  CHARACTER_CREATE_RESPONSE
53-05-00-08  CHARACTER_RENAME_RESPONSE               Character rename
53-05-00-09  CHAT_CONNECT_RESPONSE                   Chat service response
53-05-00-0a  AUTH_ACCOUNT_CREATE_RESPONSE
53-05-00-0b  DELETE_CHARACTER_RESPONSE
53-05-00-0c  GAME_MSG                                Server Update
53-05-00-0d  CONNECT_CHAT
53-05-00-0e  TRANSFER_TO_WORLD                       Redirection
53-05-00-0f  IMPENDING_RELOAD_NOTIFY
53-05-00-10  MAKE_GM_RESPONSE                        GMlevel change
53-05-00-11  HTTP_MONITOR_INFO_RESPONSE
53-05-00-12  SLASH_PUSH_MAP_RESPONSE                 Push map
53-05-00-13  SLASH_PULL_MAP_RESPONSE                 Pull map
53-05-00-14  SLASH_LOCK_MAP_RESPONSE                 Lock map
53-05-00-15  BLUEPRINT_SAVE_RESPONSE
53-05-00-16  BLUEPRINT_LUP_SAVE_RESPONSE
53-05-00-17  BLUEPRINT_LOAD_RESPONSE_ITEMID
53-05-00-18  BLUEPRINT_GET_ALL_DATA_RESPONSE
53-05-00-19  MODEL_INSTANTIATE_RESPONSE
53-05-00-1a  DEBUG_OUTPUT
53-05-00-1b  ADD_FRIEND_REQUEST                      Friend request
53-05-00-1c  ADD_FRIEND_RESPONSE                     Friend request response
53-05-00-1d  REMOVE_FRIEND_RESPONSE                  Remove friend response
53-05-00-1e  GET_FRIENDS_LIST_RESPONSE               Friends list
53-05-00-1f  UPDATE_FRIEND_NOTIFY                    Friend update
53-05-00-20  ADD_IGNORE_RESPONSE                     Add blocked
53-05-00-21  REMOVE_IGNORE_RESPONSE                  Remove blocked
53-05-00-22  GET_IGNORE_LIST_RESPONSE                Blocked list
53-05-00-23  TEAM_INVITE
53-05-00-24  TEAM_INVITE_INITIAL_RESPONSE
53-05-00-25  GUILD_CREATE_RESPONSE
53-05-00-26  GUILD_GET_STATUS_RESPONSE               Guild get status
53-05-00-27  GUILD_INVITE
53-05-00-28  GUILD_INVITE_INITIAL_RESPONSE
53-05-00-29  GUILD_INVITE_FINAL_RESPONSE
53-05-00-2a  GUILD_INVITE_CONFIRM
53-05-00-2b  GUILD_ADD_PLAYER
53-05-00-2c  GUILD_REMOVE_PLAYER
53-05-00-2d  GUILD_LOGIN_LOGOUT                      Guild login/logout
53-05-00-2e  GUILD_RANK_CHANGE
53-05-00-2f  GUILD_DATA
53-05-00-30  GUILD_STATUS
53-05-00-31  MAIL
53-05-00-32  DB_PROXY_RESULT
53-05-00-33  SHOW_ALL_RESPONSE                       Online player list
53-05-00-34  WHO_RESPONSE                            Player location response
53-05-00-35  SEND_CANNED_TEXT                        Chat message send failure response
53-05-00-36  UPDATE_CHARACTER_NAME
53-05-00-37  SET_NETWORK_SIMULATOR
53-05-00-38  INVALID_CHAT_MESSAGE
53-05-00-39  MINIMUM_CHAT_MODE_RESPONSE
53-05-00-3a  MINIMUM_CHAT_MODE_RESPONSE_PRIVATE
53-05-00-3b  CHAT_MODERATION_STRING
53-05-00-3c  UGC_MANIFEST_RESPONSE
53-05-00-3d  IN_LOGIN_QUEUE
53-05-00-3e  SERVER_STATES                           Server states/status
53-05-00-3f  GM_CLOSE_TARGET_CHAT_WINDOW             GM quit private chat
53-05-00-40  GENERAL_TEXT_FOR_LOCALIZATION
53-05-00-41  UPDATE_FREE_TRIAL_STATUS
===========  ======================================  ==================================

Chat packets
------------

Server-to-Client
^^^^^^^^^^^^^^^^

[53-02-00-01] (chat message)
""""""""""""""""""""""""""""
:[u64]:			???
:[u8]:			chat channel, always 0x04 for public-chat so far.
:[u8]:			this seems to be chat message length (including null terminator, so bytelength is this * 2) , but the chat message is a wstring, why would it need a length specifier? also it seems not to have any effect if you change this (probably due to the way the client wstring parser works)
:[L\:3]:			???, still message length ?
:[wstring]:		Sender name, empty string is treated as System message
:[u64]:			Sender objectID
:[u16]:			???
:[bool]:		is sender a mythran, if true, chat shows “Mythran” instead of real name
:[wstring variable length]: Chat message

[53-02-00-02] (private chat message)
""""""""""""""""""""""""""""""""""""
:[u64]: 		???, always 0?
:[u8]:			chat channel
:[u8]:			this seems to be chat message length (including null terminator, so bytelength is this * 2) , but the chat message is a wstring, why would it need a length specifier? also it seems not to have any effect if you change this (probably due to the way the client wstring parser works)
:[L\:3]:		???, still message length ?
:[wstring]:		Sender name
:[s64]:			Sender objectID
:[u16]:			???
:[bool]:		is sender a mythran, if true, chat shows “Mythran” instead of real name
:[wstring]:		Recipient name
:[bool]:		is recipient a mythran, if true, chat shows “Mythran” instead of real name
:[u8]:			return code
    			values:
			    	:0: Success
			    	:1: Not online
			    	:2: Error/Failure
			    	:3: Occurred in packets but i have no idea what it does (seems like success), seems like this always is in incoming packets (not sent from local char)

:[wstring variable length]: Chat message

.. note :: sender name, sender objectID needs to be set by the server before broadcasting

Client-to-Server
^^^^^^^^^^^^^^^^

[53-02-00-07] (add friend request)
""""""""""""""""""""""""""""""""""
:[u64]:		???, always 0?
:[wstring]:	Name of person to be added as friend
:[bool]:	is request best friend request

[53-02-00-08] (add friend response)
"""""""""""""""""""""""""""""""""""
:[u64]:		???, always 0?
:[u8]:		return code, values:

			:0: Accepted
			:1: Declined
			:3: Invite window closed 
:[wstring]: Name of person to be added as friend

[53-02-00-09] (remove friend)
"""""""""""""""""""""""""""""
:[u64]:		???, always 0?
:[wstring]:	name of friend to be removed

[53-02-00-0a] (get friends list)
""""""""""""""""""""""""""""""""
:[u64]:		???, always 0? (was always 0 in the captures)
			respond to this with 53-05-00-1e Friends list

[53-02-00-0f] (team invite)
"""""""""""""""""""""""""""
:[u64]:		???, always 0?
:[wstring]:	Invited person's name

[53-02-00-10] (team invite response)
""""""""""""""""""""""""""""""""""""
:[u64]:		???, always 0?
:[bool]:	is invite denied
:[s64]:		Inviter's object ID


Appendix A: LEGO data format and data type IDs
----------------------------------------------

LDF is used in boot.cfg, client xml settings, .luz and .lvl files, and the binary part of the chardata packet.

This binary data format is used in various packets, for example the chardata packet.

:[u32]: number of keys

	:[u8]: key length in bytes
	:[wchar]: key
	:[u8]: data type (see below)
	:[according to data type]: data

The text format has the format: :samp:`key=type:value`

:0:   String (variable wstring?)
:1:   s32
:2:   ??? (haven’t found an occurrence of this type so far)
:3:   Float (32bit, signed)
:4:   ??? (Location&Size, appeared on lwo_override.xml)
:5:   u32
:6:   ??? (haven’t found an occurrence of this type so far)
:7:   Boolean (8bit, 0 or 1)
:8:   s64
:9:   s64, Used only for (object?) IDs?
:10:  ??? (haven’t found an occurrence of this type so far)
:11:  ??? (haven’t found an occurrence of this type so far)
:12:  ??? (haven’t found an occurrence of this type so far)
:13:  in chardata this was XML data, in client settings checksum, in lvl files strings/GUIDs (maybe it's for bytes)

Appendix B: Maps info and checksum
----------------------------------

Here are the checksums I found.  Probably need to go back through and find the different map instances if I can.

==========================  ==========  ==================================
Map Name                    Zone ID     Checksum
==========================  ==========  ==================================
Venture Explorer            1000        7c 08 b8 20
Return to Venture Explorer  1001        3c 0a 68 26
Avant Gardens               1100        11 55 52 49
Avant Gardens Survival      1101        e2 14 82 53
Spider Queen Battle         1102        da 03 d4 0f
Block Yard                  1150        da 03 d4 0f
Avant Grove                 1151        03 03 89 0a
Nimbus Station              1200        30 6b 1e da
Pet Cove                    1201        30 13 6e 47
Vertigo Loop Racetrack      1203        02 05 fc 10
Battle of Nimbus Station    1204        58 02 d4 07
Nimbus Rock                 1250        91 01 8d 05
Nimbus Isle                 1251        5d 04 4f 09
Frostburgh                  1260        currently disabled in the client
Gnarled Forest              1300        90 c2 ea 12
Canyon Cove                 1302        ef 02 77 0b
Keelhaul Canyon             1303        todo
Chantey Shantey             1350        5c 01 b6 04
Forbidden Valley            1400        0d 76 19 85
Forbidden Valley Dragon     1402        87 01 f5 02
Dragonmaw Chasm             1403        4e 0f 85 81
Raven Bluff                 1450        26 01 f0 03
Starbase 3001               1600        ee 02 c2 07
Deep Freeze                 1601        06 01 32 02
Robot City                  1602        7f 03 93 07
Moon Base                   1603        ad 01 3b 04
Portabello                  1604        dd 07 15 18
LEGO Club                   1700        38 01 04 02
Crux Prime                  1800        99 a3 17 4b
Nexus Tower                 1900        3c f4 4a 9e
Ninjago                     2000        74 2c 69 4d
Frakjaw Battle              2001        ef 00 eb 09
==========================  ==========  ==================================
