Character Component (4)
-----------------------

This component does not have any client database table associated with it, as it
represents and manages the state of the character of some player. It holds information
such as the lego score (U-Score), account information and the passport statistics.

There is a very strange struct in the serialization, notably the :samp:`TransitionState` in the Character Component.
It is a 2 bit enum defined as the following:

| **[uint2_t]** - TransitionState
| if TransitionState == 1
|   **[uint16_t]** - lastCustomBuildParts (presumably the rocket they are arriving on)
|     **[wchar]** - wCharacterOfTheAboveString

Component Dependencies
......................

| :doc:`110-possession-control`
| :doc:`109-level-progression`
| :doc:`106-player-forced-movement`

Component Construction
......................

| :ref:`Possession Control <110-construction>`
| :ref:`Level Progression <109-construction>`
| :ref:`Player Forced Movement <106-construction>`
| :packet:`Character <raknet/client/replica/character/struct.CharacterConstruction>`

Component Serialization
.......................

| :ref:`Possession Control <110-serialization>`
| :ref:`Level Progression <109-serialization>`
| :ref:`Player Forced Movement <106-serialization>`
| :packet:`Character <raknet/client/replica/character/struct.CharacterSerialization>`

Relevant Game Messages
......................

Server received
_______________
| :gm:server:`ModifyPlayerZoneStatistic`
| :gm:server:`UpdatePlayerStatistic`
| :gm:server:`SetEmotesEnabled`

Component XML Format
............................

|   :samp:`char` - Character Component data
|   :samp:`attr acct` - account ID
|   :samp:`attr cc` - Currency
|   :samp:`atrr cm` - Maximum Currency
|   :samp:`attr co` - Unknown, related to claim codes?
|   :samp:`attr edit` - Unknown, Maybe related to HF editor?
|   :samp:`attr ft` - FreeToPlay status?
|   :samp:`attr gid` - Guild ID
|   :samp:`attr gm` - GM level
|   :samp:`attr gn` - Guild name
|   :samp:`attr lcbp` - modular info of last used rocket
|   :samp:`attr llog` - Timestamp of last login as this character
|   :samp:`attr lrx` - Last respawn point position x
|   :samp:`attr lry` - Last respawn point position y
|   :samp:`attr lrz` - Last respawn point position z
|   :samp:`attr lrrw` - Last respawn point rotation w
|   :samp:`attr lrrx` - Last respawn point rotation x
|   :samp:`attr lrry` - Last respawn point rotation y
|   :samp:`attr lrrz` - Last respawn point rotation z
|   :samp:`attr ls` - Lego score/Universe score.
|   :samp:`attr lzcs` - Last Zone Check Sum, stored as an int32_t
|   :samp:`attr lzid` - The last zone clone ID, instance ID and zone ID concatenated into 1 64 bit number. See :ref:`this footnote <lzid_foot_note>` for more info.
|   :samp:`attr lzrw` - Last world rotation w
|   :samp:`attr lzrx` - Last world rotation x
|   :samp:`attr lzry` - Last world rotation y
|   :samp:`attr lzrz` - Last world rotation z
|   :samp:`attr lzx` - Last world position x
|   :samp:`attr lzy` - Last world position y
|   :samp:`attr lzz` - Last world position z
|   :samp:`attr mldt` - "Prop mod last display time"
|   :samp:`attr stt` - Player stats. See :ref:`this footnote <character_stats_footnote>` for more information about the format.
|   :samp:`attr time` - Total time played, in seconds.
|   :samp:`attr ttip` - "tool tip flags"
|   :samp:`attr v` - Unknown, maybe version?  Always 3 in caps
|   :samp:`attr vd` - Unknown, some packet cap values are 15368, 15318, 15367
|     :samp:`ue` - Unlocked emotes
|       :samp:`e` - An unlocked emote
|       :samp:`attr id` - Emote ID
|     :samp:`vl` - Visited worlds
|       :samp:`l` - A visited world
|       :samp:`attr cid` - Clone ID (used for properties, 0 if not a property)
|       :samp:`attr id` - World ID.
|     :samp:`zs` - World Statistics
|       :samp:`s` - Statistics for a world
|       :samp:`attr ac` - Achievements collected
|       :samp:`attr bc` - Bricks collected
|       :samp:`attr cc` - Coins collected
|       :samp:`attr es` - Enemies smashed
|       :samp:`attr map` - ID of the world the statistics are for
|       :samp:`attr qbc` - Quick build count

.. _lzid_foot_note:

.. note ::
  | :samp:`lzid` a binary concatenation of world ID, world instance and world clone, e.g:
  | lzid = :samp:`2341502167811299`
  | hex representation of lzid = :samp:`00 08 51 95 74 f4 04 e3`
  | hex representation of lzid, byte reversed (= packet byte order, Little Endian) = :samp:`e3 04 f4 74 95 51 08 00`
  | World ID = :samp:`e3 04`
  | World Instance = :samp:`f4 74`
  | World Clone = :samp:`95 51 08 00`

.. _character_stats_footnote:

Character Statistics Format
...........................

| The character statistics are formatted as follows with a semicolon delimiting each statistic, including the last one. Fill in empty statistics with a zero.
| Example:
| :samp:`10809;543;106;43;257;3;41;0;532;236;123;32403;1;58;7;55;101;111;0;0;0;0;0;0;0;0;0;`
| All stats are :samp:`uint64_t` except where noted otherwise:

| CurrencyCollected
| BricksCollected (:samp:`int64_t`)
| SmashablesSmashed
| QuickBuildsCompleted
| EnemiesSmashed
| RocketsUsed
| MissionsCompleted
| PetsTamed
| ImaginationPowerUpsCollected
| LifePowerUpsCollected
| ArmorPowerUpsCollected
| MetersTraveled
| TimesSmashed
| TotalDamageTaken
| TotalDamageHealed
| TotalArmorRepaired
| TotalImaginationRestored
| TotalImaginationUsed
| DistanceDriven
| TimeAirborneInCar
| RacingImaginationPowerUpsCollected
| RacingImaginationCratesSmashed
| RacingCarBoostsActivated
| RacingTimesWrecked
| RacingSmashablesSmashed
| RacesFinished
| FirstPlaceRaceFinishes
