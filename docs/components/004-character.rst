Character Component (4)
-----------------------

This component does not have any client database table associated with it, as it
represents and manages the state of the character of some player. It holds information
such as the lego score (U-Score), account information and the passport statistics.

Relevant Game Messages
......................

* `gm-update-player-statistics`
* :gm:client:`ModifyLegoScore`
* :gm:server:`SetEmotesEnabled`

XML Serialization :samp:`<char>`
................................

This component is serialized to XML to store its data.

:acct: Account ID
:cc: Currency Current
:cm: Currency Max (?)
:co: (?)
:edit: Is Editor (?)
:ft: FreeToPlay status (?)
:gid: Group ID (?)
:gm: GM level
:gn: (?)
:lcbp: modular info of last used rocket (?)
:llog: Timestamp of last login as this character (?)
:lrx: Last respawn point position x (?)
:lry: Last respawn point position y (?)
:lrz: Last respawn point position z (?)
:lrrw: Last respawn point rotation w (?)
:lrrx: Last respawn point rotation x (?)
:lrry: Last respawn point rotation y (?)
:lrrz: Last respawn point rotation z (?)
:ls: Lego score/Universe score.
:lzcs: (?)
:lzid: Information about the last world?
:lzrw: Last world rotation w
:lzrx: Last world rotation x
:lzry: Last world rotation y
:lzrz: Last world rotation z
:lzx: Last world position x
:lzy: Last world position y
:lzz: Last world position z
:mldt: (?)
:stt: Player stats
:time: Total time played, in seconds
:ttip: (?)
:v: (?)
:vd: (?)

.. note ::
  | This seems to be a binary concatenation of world ID, world instance and world clone, e.g:
  | lzid = :samp:`2341502167811299`
  | hex representation of lzid = :samp:`00 08 51 95 74 f4 04 e3`
  | hex representation of lzid, byte reversed (= packet byte order) = :samp:`e3 04 f4 74 95 51 08 00`
  | World ID = :samp:`e3 04`
  | World Instance = :samp:`f4 74`
  | World Clone = :samp:`95 51 08 00`

Unlocked Emotes :samp:`<ue>`
''''''''''''''''''''''''''''
An unlocked emote :samp:`<e>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:id: Emote ID.

Visited levels :samp:`<vl>`
'''''''''''''''''''''''''''

Level :samp:`<l>`
~~~~~~~~~~~~~~~~~
:cid: Clone ID (used for properties, 0 if not a property)
:id: World ID.

Zone Statistics :samp:`<zs>`
''''''''''''''''''''''''''''

Statistics :samp:`<s>`
~~~~~~~~~~~~~~~~~~~~~~
:ac: Achievements collected.
:bc: Bricks collected.
:cc: Coins collected.
:es: Enemies smashed.
:map: ID of the world the statistics are for.
:qbc: Quick build count.
