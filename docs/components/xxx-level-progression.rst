Level Progression Component (?)
-------------------------------

This component handles the progression in levels for the local player. It is
unknown which ID this component has, as it was introduced in a version we don't
have the list for. See also :wiki:`Player Leveling <Player_Leveling>`
in the wiki.

Relevant Data Tables
....................

* :doc:`../database/LevelProgressionLookup`

Relevant Game Messages
......................

* :gm:client:`ModifyLegoScore`
* :gm:client:`NotifyLevelRewards`

XML Serialization :samp:`<lvl>`
...............................

This component is serialized to XML to store its data.

:cv: (?)
:l: Base Player Level
:sb: (?)
