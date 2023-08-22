Force Movement (40)
===================

Details unknown

Parameters
----------

.. list-table::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - collide_with_faction
     - ???
   * - duration
     - ???
   * - forward
     - ???
   * - hit_action
     - ???
   * - hit_action_enemy
     - ???
   * - hit_action_faction
     - ???
   * - ignore_projectile_collision
     - ???
   * - left
     - ???
   * - move_target
     - ???
   * - relative
     - ???
   * - timeout_action
     - ???
   * - yaw
     - ???
   * - yaw_abs
     - ???

BitStream Serialization
-----------------------

| if any of “hit_action”, “hit_action_enemy”, “hit_action_faction” is not 0:
| 	**[u32]** - behavior handle
| 	-> SyncSkill, see AirMovement for details

