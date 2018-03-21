Stun (15)
=========

Temporarily removes the characters ability to do certain things

Parameters
----------

.. list-table ::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - cant_attack
     - If the player is blocked from attacking
   * - cant_equip
     - If the player is blocked from equipping gear
   * - cant_interact
     - If the player is blocked from interacting
   * - cant_jump
     - If the player is blocked from jumping
   * - cant_move
     - If the player is stopped from moving
   * - cant_turn
     - If the player is stopped from turning
   * - cant_use_item
     - If the player is blocked from using items
   * - dont_terminate_interact
     - If the stun will exit existing interactions
   * - ignore_immunity
     - If the behavior will ignore immunity
   * - stun_caster
     - Whether to stun the caster

Possibly deprecated
^^^^^^^^^^^^^^^^^^^

.. list-table ::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - action
     - The next action to execute
   * - duration
     - How long the stun will take
   * - radius
     - In which radius targets will be stunned
   * - target_enemy
     - Whether to target enemies
   * - target_friend
     - Whether to target friends

Likely typos
^^^^^^^^^^^^

.. list-table ::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - can't_equip
     - Misspelling of `cant_equip`
   * - can't_interact
     - Misspelling of `cant_interact`
   * - can't_move
     - Misspelling of `cant_move`
   * - can't_turn
     - Misspelling of `cant_turn`

BitStream Serialization
-----------------------

.. todo:: investigate

| if target != self:
| 	note that for some reason this does not work for projectiles
| 	**[bit]** - ???, always False?