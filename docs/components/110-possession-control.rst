Possession Control Component (110)
----------------------------------

Represents an entity that can possess other entities.
Generally used by players.

Relevant Game Messages
......................

* :gm:client:`SetMountInventoryId`
* :gm:client:`VehicleUnlockInput`
* :gm:client:`SetStunned`
* :gm:client:`SetPlayerControlScheme`

.. _110-construction:

Component Construction
......................

:packet:`raknet/client/replica/possession_control/struct.PossessionControlConstruction`

.. _110-serialization:

Component Serialization
.......................

:packet:`raknet/client/replica/possession_control/type.PossessionControlSerialization`
