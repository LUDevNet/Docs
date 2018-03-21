Switch (29)
===========

Details unknown

Parameters
----------

.. list-table ::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - action_false
     - ???
   * - action_true
     - ???
   * - distance
     - ???
   * - faction
     - ???
   * - imagination
     - ???
   * - isEnemyFaction
     - ???
   * - target_has_buff
     - ???

BitStream Serialization
-----------------------

.. todo:: investigate

| state = True
| if “imagination” parameter > 0 or not “isEnemyFaction” parameter:
| 	state= **[bit]** - switch state
| if state:
| 	-> action_true
| else:
| 	-> action_false
