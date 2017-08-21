Server Packets
==============

.. note ::
	This is a read-the-docs port of the original google docs `lu_server_packets <https://docs.google.com/document/d/1D1Ao6SPkbqLExXyFUIVyXL3OnUe5JOmAQJRJei7OfA0>`_, written by humanoid, lcdr and others, ported by `@Xiphoseer <https://twitter.com/Xiphoseer>`_. This is currently a proof of concept and is not guaranteed to reflect the latest changes.

General
-------

[53-00-00-00] (global - connection init, handshake)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u32]** - Game/Network version
| 	*this has to match with the client version (otherwise client disconnects), latest one is 171022*
| **[u32]** - ???, is always 0x93?
| **[u32]** - remote connection type
| 	*(this is for some reason a u32, although the packet header only has space for a u16, so 2 bytes are wasted), tells the client what number he has to put in the header for his next packets (after the init sequence), for auth this is 1, otherwise its 4*
| **[u32]** - process id (I assume from the server?)
| **[u16]** - local port???, is always 0xff?
| 	*This would be the local port for the client, but since the client already knows this, it could be filler*
| **[string]** - local IP of the server?
| 	*has the range of an internal IP (always?), it doesn’t seem to be important (perhaps try it with a server that is non-local?)*

[53-00-00-01] (disconnect notify)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| **[u32]** - disconnect id
| 	Possible values:
| 		todo: list others from client code
| 		0x00 -> unknown server error
| 		0x04 -> duplicate login
| 		0x05 -> server shutdown
| 		0x06 -> server unable to load map
| 		0x07 -> invalid session key
| 		0x08 -> account was not in pending list
| 		0x09 -> character not found
| 		0x0a -> character corruption
| 		0x0b -> kick
| 		0x0d -> free trial expired
| 		0x0e -> play schedule time done

[53-00-00-02] (general notify)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Artificial packet

| **[u32]** - notify id
| 	Possible values:
| 		0x00 -> logged off duplicate account


Sent by Auth
------------

[53-05-00-00] (login info)
^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u8]** - login return code, values are
| 	0x00, 0x03, 0x04, 0x0f-0xff -> logs General Failed (+error code)
| 		shows “We could not sign you in to LEGO Universe” message ingame
| 	0x01 -> Success
| 	0x02 -> Account is banned
| 	0x05 -> Account permissions not high enough
| 		(if a custom message is included in the packet it will be displayed in frontend, otherwise the message for “General Failed” will be shown)
| 	0x06 -> Invalid Username or Password
| 	0x07 -> Account is currently locked (wrong password entered too many times)
| 	0x08 -> same as 0x06, perhaps just “Invalid Username”?
| 		(since 0x06 appeared in the logged traffic due to an invalid password)
| 	0x09 -> Account Activation Pending (shows the same ingame message as 0x06/0x08)
| 	0x0a -> Account is disabled (shows the same message ingame as 0x06/0x08)
| 	0x0b -> Game Time Expired
| 	0x0c -> Free Trial Has Ended
| 	0x0d -> Play schedule not allowing it
| 	0x0e -> Account not activated
| **[string]** - seems to be always “Talk_Like_A_Pirate”
| 		no idea what it is for and if the whole 33 length is reserved for it (or even more than that, like the next structs up to the next u16)
| **[string]**\*7 - ???
| 	reserved for 7 other strings? or does it actually contain relevant data, it seems every 33rd byte is mostly != 0 but in between are always zeroes
|
| 	(not relevant for current server but still interesting: **[A:0x4b,wstring]** and **[A:0x8d,u16]** are IP and port for the beta client)
| 
| 	*Client version number is used for feature gating, if you don’t write the latest (1.10.64) version certain features will be disabled*
| **[u16]** - client version number major
| **[u16]** - client version number current
| **[u16]** - client version number minor
| **[wstring]** - user key, newly generated with every login?
| **[string]** - IP to redirect to a char instance
| **[string]** - ChatIP (according to a debug message in the client)
| **[u16]** - port number of next instance
| **[u16]** - ChatPort (according to a debug message in the client)
| **[string]** - ???, reserved for another IP (perhaps an alternative one)? was always 0 so far
| **[L:37]** - ???, some kind of UUID?
| 	seems to be always “00000000-0000-0000-0000-000000000000” (has same format as a GUID, see Visual Studio->Tools->Create GUID), string
| **[u32]** - ???, always 0?
| **[L:3]** - localization
| 	“US” and “IT” occur in the available captures, probably have to guess other values (can they be 3 characters long or is that last byte reserved for 0?) [when booting with german, it will use US], string
| **[bool]** - if set to 1
| 	it shows a screen that indicates that its the first time the user logged in with a subscription (only shows up again after restarting client)
| **[bool]** - is FTP
| **[u64]** - ???, always 0?
| **[u16]** - length of custom error message (not actual byte length)
| 	**[L:V]** - custom error message, only visible with login code 0x05, wstring
| **[u32]** - count
| 	how much more bytes there are which are occupied by x stamp structures so its easily calculable, for some reason the 4 bytes from this structure seem to be included
| 	**[u32]** - id of stamp
| 		see client log for names or server source for enum, these stamps seem to be logs of what happened in the server, thats why the number of stamps isn’t always the same (in case of failed login, etc?)
| 	**[s32]** - number in brackets
| 		can be negative, see client log for structure of stamps
| 	**[u32]** - number after brackets, “...at [number]”
| 		this seems to be a timestamp in seconds (see client log), the same number for most stamps but sometimes +/-1 compared to the other stamp values (if thats the case then its also “start+1” or “last+1” in the client log?)
| 	**[u32]** - ???, always 0?


[53-05-00-01] (logout response)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Theoretical packet, this seems to have no effect at all?


Sent by World
-------------

[53-05-00-02] (world info?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u16]** - zone ID
| **[u16]** - map instance (name from crash log)
| **[u32]** - map clone (name from crash log)
| **[u32]** - map checksum
| **[u16]** - ???
| **[float]** - player position x
| **[float]** - player position y
| **[float]** - player position z
| **[u32]** - 4 if is activity world, 0 otherwise
| 	(Look at ‘Activities’ table in CDClient for more information)

(player position is probably for preloading content in the vicinity of the player)

[53-05-00-03] (“create object”)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Theoretical packet, this seems to have no effect at all?

[53-05-00-04] (detailed user info)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u32]** - size of following data
| **[bool]** - is content compressed, always 1 so far
| 	**[u32]** - size of uncompressed data
| 	**[u32]** - size of the following (compressed) data
| **[L:V]** - compressed data in LDF format

.. note ::
	
	* The compression algorithm used is “deflate”, as used by zlib
	* The only keys needed for world loading are “template” and “objid”.
	* The position and rotation values don’t affect the player’s position (and are actually optional), the ones that do are in the replica packets.

All keys (and datatypes) from this packet in the captured traffics
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. hlist ::
	:columns: 3

	* ``accountID``: ``8``
	* ``bbbAutosaveDirty``: ``7``
	* ``chatmode``: ``1``
	* ``editor_enabled``: ``7``
	* ``editor_level``: ``1``
	* ``freetrial``: ``7``
	* ``gmlevel``: ``1``
	* ``legoclub``: ``7``
	* ``levelid``: ``8``
	* ``matchTeam``: ``1``
	* ``matching.droppedItem``: ``9``
	* ``matching.matchKey``: ``8``
	* ``matching.matchPlayers``: ``1``
	* ``matching.matchStamp``: ``8``
	* ``matching.matchTeam``: ``1``
	* ``name``: ``0``
	* ``objid``: ``9``
	* ``position.x``: ``3``
	* ``position.y``: ``3``
	* ``position.z``: ``3``
	* ``propertycloneid``: ``1``
	* ``propertycloneid``: ``5``
	* ``reputation``: ``8``
	* ``requiresrename``: ``7``
	* ``rotation.w``: ``3``
	* ``rotation.x``: ``3``
	* ``rotation.y``: ``3``
	* ``rotation.z``: ``3``
	* ``rspPosX``: ``3``
	* ``rspPosY``: ``3``
	* ``rspPosZ``: ``3``
	* ``template``: ``1``
	* ``transfer_use_pos``: ``7``
	* ``transferspawnpoint``: ``0``
	* ``txfring``: ``7``
	* ``xmlData``: ``13``


[53-05-00-05] (“create character extended”)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Theoretical packet, this seems to have no effect at all?


[53-05-00-06] (minifigure list of user)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| character_count=**[u8]** - Number of characters (00 - 04)
| **[u8]** - Index of character in the front
| **[character_count]**
| 	**[s64]** - Character ID (=object ID from replica packets = objID in xml data from chardata)
| 	**[u32]** - ???
| 	**[wstring]** - Name of character
| 	**[wstring]** - Name that shows up in parentheses in the client (probably for not yet approved custom names?)
| 	**[bool]** - is name-moderation rejected
| 	**[bool]** - is FTP
| 		if this set but the account FreeToPlay flag in the login response packet isn’t, it asks whether you’d like to change your FreeToPlay name to a custom name
| 	**[L:10]** - ???
| 	**[u32]** - Shirt color
| 	**[u32]** - Shirt style???
| 	**[u32]** - Pants color
| 	**[u32]** - Hair style
| 	**[u32]** - Hair color
| 	**[u32]** - “lh”, see “<mf />” row in the xml data from chardata packet (no idea what it is)
| 	**[u32]** - “rh”, see “<mf />” row in the xml data from chardata packet (no idea what it is)
| 	**[u32]** - Eyebrows
| 	**[u32]** - Eyes
| 	**[u32]** - Mouth
| 	**[u32]** - ???
| 	**[u16]** - last map/zone/world ID - Note: If this is 0 the client will play the venture explorer into cinematic.
| 	**[u16]** - last map instance
| 	**[u32]** - last map clone
| 	**[u64]** - last login or logout timestamp of character in seconds?
| 		(xml is “llog” so both could be possible)
| 	**[u16]** - number of items to follow
| 		**[u32]** - equipped item LOTs
|			(order of items doesn’t matter? I think it reads them in order so if we accidentally put 2 shirts the second one will be the one shown.)


[53-05-00-07] (minifigure creation response)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
this should come with an updated character list packet

| **[u8]** - Creation response ID

Creation response IDs
	- 0x00 - Success
	- 0x01 - (this ID isn’t working)
	- 0x02 - Name not allowed
	- 0x03 - Predefined name already in use
	- 0x04 - Custom name already in use


[53-05-00-08] (character rename)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet

| **[u8]** - character rename response ID

Rename response IDs
	- 0x00 - Success
	- 0x01 - Unknown error
	- 0x02 - Name unavailable
	- 0x03 - Name already in use


[53-05-00-09] (chat service response)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet

| **[u8]** - Chat service response (0x00 -> success)


[53-05-00-0a] (account stuff?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet

| **[u8]** - account creation return code

Possible values:
	- 0x00 -> Successfully created account
	- 0x01 -> Failed to create account
	- 0x02 -> Failed to create account. User login already exists
	- other -> Failed to create account. Unknown Response


[53-05-00-0b] (character delete response)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
upon receival the client sends a character list request

| **[u8]** - deletion return code?
| 	(in the one sample we have, this is 0x01 (=Success? ))


[53-05-00-0c] (server game message)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
See the dedicated game message document for more information


[53-05-00-0d] (“chat connect”)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Theoretical packet, this seems to have no effect at all?


[53-05-00-0e] (redirection to new server)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[string]** - IP of the next instance
| 	again not sure if all 33 bytes are reserved for this but it would make sense
| **[u16]** - port number of next instance
| **[bool]** - if true, an announcement “Mythran Dimensional Shift Succeeded” is displayed
| 	(the announcement displays “succeeded” regardless of whether the redirect worked or not)


[53-05-00-0f] (map reload notification?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet


[53-05-00-10] (GMlevel change)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet

| **[bool]** - was change successful
| **[u16]** - Highest GMlevel possible (printed when not successful)
| **[u16]** - Previous GMlevel
| **[u16]** - Current GMlevel


[53-05-00-11] (“HTTP monitor info response”)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet

| **[u16]** - Port number
| **[bool]** - open "sum" page in browser (0x01 opens in browser)
| **[bool]** - is “sum” page supported
| **[bool]** - is “detail” page supported
| **[bool]** - is “who” page supported
| **[bool]** - is “objects” page supported


[53-05-00-12] (push map response (happy flower stuff))
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet


[53-05-00-13] (pull map response (happy flower stuff))
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet


[53-05-00-14] (lock map response (happy flower stuff))
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet


[53-05-00-15] (“blueprint save response”)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| **[s64]** - objectID of something
| 	not sure about that but it had the value range of a non-player objectID in the packet that I checked (8th byte was 0x4)
| **[u32]** - ???, was 0 in the packet that I checked
| **[u32]** - ???, was 1 in the packet that I checked
| **[s64]** - could be ID of object
| 	(similar, if not the same, to the one in 53-05-00-0c, the range would fit with the 8th byte being 0x10)
| **[u32]** - size of the following data
| **[sd0 struct]** - compressed data seems to contains lxfml data
| 	(for structure definition see lu_file_struct document)


[53-05-00-17] (“blueprint load response itemID”)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
todo: investigate


[53-05-00-1a] (debug output)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet

| **[u32]** - Length of message
| **[L:V]** - Message


[53-05-00-1b] (Friend/Best friend request)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[wstring]** - Name of friend who requested
| **[bool]** - is best friend request


[53-05-00-1c] (friend request response)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u8]** - response code

Response codes:
	- 0x00 - "<name> is now your Friend."
	- 0x01 - "<name> is already your Friend."
	- 0x02 - "<name> is not a valid player name."
	- 0x03 - "Unable to add <name> to your Friends." (default for error)
	- 0x04 - "Sorry, your Friends List is already full."
	- 0x05 - "<name>'s Friends List is full."
	- 0x06 - MSG_FRIEND_DECLINEND(_BESTFRIEND)_INVITE
	- 0x07 - MSG_FRIEND_NAME_IS_BUSY
	- 0x08 - MSG_FRIEND_NOT_ONLINE_FAILURE
	- 0x09 - MSG_FRIEND_WAITING_APPROVAL
	- 0x0a - MSG_FRIEND_COULD_NOT_ADD_MYTHRAN
	- 0x0b - MSG_FRIEND_NAME_HAS_CANCELLED
	- 0x0c - MSG_FRIEND_COULD_NOT_ADD_FREE_TRIAL

| **[bool]** - is player online
| **[wstring]** - player
| **[s64]** - minifig ID
| **[u16]** - World ID
| **[L:6]** - World instance
| **[L:6]** - World clone
| **[bool]** - is player best friend
| **[bool]** - is player FTP


[53-05-00-1d] (remove friend response)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[bool]** - is successful
| **[wstring]** - Name of friend to be removed


[53-05-00-1e] (friends list)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u8]** - ???
| **[u16]** - Length of packet - 1
| **[u16]** - Amount of friends
| 	**[bool]** - is online
| 	**[bool]** - is best friend
| 	**[bool]** - is FTP
| 	**[L:5]** - ???
| 	**[u16]** - World ID
| 	**[u16]** - World Instance
| 	**[u32]** - World Clone
| 	**[s64]** - Friend’s minifig ID
| 	**[wstring]** - Friend name
| 	**[L:6]** - ???


[53-05-00-1f] (friend update)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
chat notification is displayed if log in/out and friend is updated in friends list

| **[u8]** - update type

Update types
	- 0 - friend logged out
	- 1 - friend logged in
	- 2 - friend changed world/ updated

| **[wstring]** - Name of friend
| **[u16]** - World ID
| **[u16]** - World Instance
| **[u32]** - World Clone
| **[bool]** - is best friend
| **[bool]** - is FTP


[53-05-00-20] (add blocked)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet

| **[L:?]** - Name of player being added


[53-05-00-21] (remove blocked)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet

| **[L:?]** - Name of player being removed


[53-05-00-22] (block list)
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. todo ::
	analyze (comes together with [53-05-00-1e] during the first few packets of world join?)
	seems to be similar to friends list but with less information

| **[u8]** - ???
| **[u16]** - Length of entire packet - 1
| **[u16]** - Amount of blocked players
| 		**[L:?]** - data for blocked player


[53-05-00-23] (team invite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[wstring]** - Name of player who sent the invite
| **[s64]** - ID of player who sent the invite


[53-05-00-24] (team invitation response?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet


[53-05-00-25] (guild creation response?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet
displayed “guild could not be created” in testing


[53-05-00-27] (guild invitation?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet
displayed "MSG_GUILD_NAME_WANTS_YOU_TO_BE_IN_NAME_GUILD" in testing


[53-05-00-28] (guild invitation response?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet
displayed “Could not invite <player>” (replace <player> of course) in testing


[53-05-00-29] (guild invitation response again?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet
displayed “CLIENTMSG_COULD_NOT_INVITE_NAME” in testing


[53-05-00-31] ( Mail stuff)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u32]** - ID
| **[ID specific]** - ID specific

Mail system IDs
	- 0x01 - Mail send response
	- 0x02 - Mail notification
	- 0x04 - Mail data
	- 0x06 - Mail attachment collect confirm
	- 0x08 - Mail delete confirm
	- 0x0a - Mail read confirm

Mail send response
""""""""""""""""""

| **[A:0x0c,u32]** - response code

values:
    - 0 - success
    - 1 - not enough money
    - 2 - attached item not found
    - 3 - item cannot be mailed
    - 4 - cannot mail yourself
    - 5 - recipient not found
    - 6 - different faction
    - 7 - unknown failure
    - 8 - moderation failure
    - 9 - mute
    - 10 - unknown failure
    - 11 - recipient is ignored
    - 12 - unknown failure
    - 13 - recipient is FTP

Mail notification
"""""""""""""""""

| **[A:0x0c,u32]** - type of notification,
| 	0 is normal mail notification, other values are unused auction things?
| if type is 0:
| **[L:32]** - ???
| **[u32]** - Amount of new mails
| **[u32]** - ???

Mail data
"""""""""
| **[A:0x0c,u32]** - return code, 0 = success, 1 = throttled
| if the return code is 1, the only following data should be 4 bytes (they don’t seem to be read though)
| if the return code is 0:
| mails_length=**[u16]** - Amount of mails
| **[u16]** - ???
| **[mails_length]**
| 	**[s64]** - Mail ID
| 	**[L:100]** - Mail subject, wstring
| 	**[L:800]** - Mail body, wstring
| 	**[L:64]** - Mail sender, wstring
| 	**[u32]** - ???
| 	**[u64]** - ???
| 	**[s64]** - Attachment object id
| 	**[s32]** - Attachment LOT (if no attachment then -1)
| 	**[u32]** - ???
| 	**[s64]** - Attachment subkey (whatever that is)
| 	**[s16]** - Amount of attachment
| 	**[L:6]** - ???
| 	**[u64]** - Send time (in seconds since 1970)? which one is real?
| 	**[u64]** - Send time (in seconds since 1970)
| 	**[bool]** - is read
| 	**[u8]** - ???
| 	**[u16]** - ???
| 	**[u32]** - ???

Mail attachment collect confirm
"""""""""""""""""""""""""""""""

| **[A:0x0c,u32]** - ???
| **[s64]** - ID of mail from which the attachment is collected

Mail delete confirm
"""""""""""""""""""

| **[A:0x0c,u32]** - ???
| **[s64]** - ID of deleted mail

Mail read confirm
"""""""""""""""""

| **[A:0x0c,u32]** - ???
| **[s64]** - ID of read mail


[53-05-00-33] (overview of online players?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet; prints amount of online players in chat

| **[bool]** - ??? some kind of boolean
|
| if previous byte is set to 0:
| 	**[A:0x09,L:2]** - Total players, u16
| 	**[A:0x0b,L:?]** - anything in here lags out the client
|
| if the byte is set to 1:
| 	**[A:0x09,s32]** - Real online players
| 	**[A:0x0d,s32]** - Simulated online players


[53-05-00-34] (player location command response ?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet

| **[bool]** - is player online, bool
| **[u16]** - Zone
| **[u16]** - I (Instance?)
| **[A:0x11,L:?]** - Player name, wstring

displays "`Player:<x> Zone:<y> (I:<z>)`" (replace variables in angle brackets) chat notification


[53-05-00-35] (chat message send failure response?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet

| **[L:1?]** - response type

Response types:
	- 0x00 - "Chat is currently disabled."
	- 0x01 - "Upgrade to a full LEGO Universe Membership to chat with other players."

[53-05-00-38] (deny chat message?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet
displayed “Sorry, that phrase isn’t acceptable in LEGO Universe” in testing


[53-05-00-39] (minimum chat mode response)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u16]** - ??? (was always 00-08 so far and only occurred in instances (survival etc) )


[53-05-00-3a] (minimum chat mode response private)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
todo: investigate


[53-05-00-3b] (chat moderation response)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[bool]** - is whole request accepted
| **[u16]** - ???
| **[u8]** - moderation request ID
| **[u8]** - ???
| **[L:66?]** - if private chat, name of recipient
| **[A:0x61,u8]** - start index of string that was not accepted
| **[u8]** - length of string that was not accepted

following this are more start/length structures, haven’t found out the total count yet


[53-05-00-3c] (ugc manifest response)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[s64]** - model id
| **[u8]** - asset type, 0 -> lxfml, 1 -> nif, 2 -> hkx


[53-05-00-3e] (server state/status?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u8]** - ???, always 1?, possibly 0 for maintenance?


[53-05-00-3f] (GM ended private chat)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial packet
displayed “The Mythran has ended your private chat session” in testing
