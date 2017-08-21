Chat packets
============

.. note ::
	This is a read-the-docs port of the original google docs `lu_packet_structs <https://docs.google.com/document/d/1v9GB1gNwO0C81Rhd4imbaLN7z-R0zpK5sYJMbxPP3Kc>`_, written by humanoid, lcdr and others, ported by `@Xiphoseer <https://twitter.com/Xiphoseer>`_. This is currently a proof of concept and is not guaranteed to reflect the latest changes.

Server-to-Client
----------------

[53-02-00-01] (chat message)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u64]**: - ???
| **[u8]**: - chat channel, always 0x04 for public-chat so far.
| **[u8]**: - this seems to be chat message length
| 	(including null terminator, so bytelength is this * 2) , but the chat message is a wstring, why would it need a length specifier? also it seems not to have any effect if you change this (probably due to the way the client wstring parser works)
| **[L:3]** - ???, still message length ?
| **[wstring]** - Sender name, empty string is treated as System message
| **[u64]** - Sender objectID
| **[u16]** - ???
| **[bool]** - is sender a mythran, if true, chat shows “Mythran” instead of real name
| **[wstring variable length]** - Chat message

[53-02-00-02] (private chat message)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u64]** - ???, always 0?
| **[u8]** - chat channel
| **[u8]** - this seems to be chat message length
| 	(including null terminator, so bytelength is this * 2) , but the chat message is a wstring, why would it need a length specifier? also it seems not to have any effect if you change this (probably due to the way the client wstring parser works)
| **[L:3]** - ???, still message length ?
| **[wstring]** - Sender name
| **[s64]** - Sender objectID
| **[u16]** - ???
| **[bool]** - is sender a mythran, if true, chat shows “Mythran” instead of real name
| **[wstring]** - Recipient name
| **[bool]** - is recipient a mythran, if true, chat shows “Mythran” instead of real name
| **[u8]** - return code
| **[wstring variable length]** - Chat message
    			
return code values:
	- 0: Success
	- 1: Not online
	- 2: Error/Failure
	- 3: Occurred in packets but i have no idea what it does (seems like success), seems like this always is in incoming packets (not sent from local char)


.. note :: sender name, sender objectID needs to be set by the server before broadcasting

Client-to-Server
----------------

[53-02-00-07] (add friend request)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u64]** - ???, always 0?
| **[wstring]** - Name of person to be added as friend
| **[bool]** - is request best friend request

[53-02-00-08] (add friend response)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u64]** - ???, always 0?
| **[u8]** - return code, values:		
| **[wstring]** - Name of person to be added as friend

return code values:
	- 0: Accepted
	- 1: Declined
	- 3: Invite window closed 

[53-02-00-09] (remove friend)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u64]** - ???, always 0?
| **[wstring]** - name of friend to be removed

[53-02-00-0a] (get friends list)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u64]** - ???, always 0? (was always 0 in the captures)

respond to this with 53-05-00-1e Friends list

[53-02-00-0f] (team invite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u64]** - ???, always 0?
| **[wstring]** - Invited person's name

[53-02-00-10] (team invite response)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **[u64]** - ???, always 0?
| **[bool]** - is invite denied
| **[s64]** - Inviter's object ID
