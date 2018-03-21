Air Movement (56)
=================

Details unknown

Parameters
----------

.. list-table ::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - goto_target
     - ???
   * - gravity_scale
     - ???
   * - ground_action
     - ???
   * - hit_action
     - ???
   * - hit_action_enemy
     - ???
   * - move_target
     - ???
   * - stop_input
     - ???
   * - timeout_action
     - ???
   * - timeout_ms
     - ???
   * - use_collision_delay
     - ???
   * - x_velocity
     - ???
   * - y_velocity
     - ???
   * - z_velocity
     - ???

BitStream Serialization
-----------------------

.. todo :: investigate

.. note ::
   like Attack Delay, this causes SyncSkill messages, which use the behavior handle as ID
   but have the behavior to execute specified in the SyncSkill bitstream

| **[u32]** - behavior handle
| *SyncSkill structure:*
| **[u32]** - behavior id
| **[u64]** - target object id
