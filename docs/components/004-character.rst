Character Component (4)
-----------------------

This component does not have any client database table associated with it, as it
represents and manages the state of the character of some player. It holds information
such as the lego score (U-Score), account information and the passport statistics.

There is a very strange struct in the serialization, notably the `TransitionState` in the Character Component.
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
| :packet:`raknet/client/replica/character/struct.CharacterConstruction`

Component Serialization
.......................

| :ref:`Possession Control <110-serialization>`
| :ref:`Level Progression <109-serialization>`
| :ref:`Player Forced Movement <106-serialization>`
| :packet:`raknet/client/replica/character/struct.CharacterSerialization`
